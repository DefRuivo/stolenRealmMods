"""Offline regressions for the live-bench contract (`live_guard.py`).

Never launches the game: drives LiveGuard with synthetic samples so the two
failure modes that broke the R1 review are pinned by an assertion:
  * focus never granted  -> Blocked('focus_not_granted') naming the cause;
  * stalled heartbeat    -> TRANSIENT while bounded, Blocked('live_engine_stalled') past it.
Also pins the "does it still bite" side: a healthy sample sequence must NOT block.
"""
from pathlib import Path
import json, unittest

HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))
import live_guard as LG


def ctx(foco=True, chat=False, digitando=False, remapeando=False, janela=None):
    return {'janela': janela, 'chat_aberto': chat, 'digitando': digitando,
            'remapeando': remapeando, 'foco_no_jogo': foco}


class LivenessTests(unittest.TestCase):
    def test_fresh_heartbeat_is_fresh(self):
        g = LG.LiveGuard()
        r = g.heartbeat(1000, 1200)
        self.assertTrue(r['fresh'])
        self.assertFalse(r['transient'])
        self.assertEqual(g.telemetry['max_stale_ms'], 0.0)

    def test_transient_stall_is_tolerated_then_recovers(self):
        g = LG.LiveGuard(stale_ms=5000, tolerance=8)
        now = 10_000
        g.heartbeat(now, now)                      # fresh baseline
        for i in range(1, 6):                      # 5 stale samples: under tolerance
            g.heartbeat(now, now + 6000 + i * 500)
        self.assertEqual(g.telemetry['transient_stale'], 5)
        self.assertFalse(g.telemetry['stale_samples'] == 0)
        g.heartbeat(now + 12000, now + 12500)      # heartbeat resumes
        self.assertEqual(g.stale_streak, 0)
        self.assertTrue(g.heartbeat(now + 13000, now + 13100)['fresh'])

    def test_stall_past_tolerance_blocks_named(self):
        g = LG.LiveGuard(stale_ms=5000, tolerance=3)
        now = 10_000
        g.heartbeat(now, now)
        with self.assertRaises(LG.Blocked) as caught:
            for i in range(1, 10):
                g.heartbeat(now, now + 6000 + i * 500, probe_fase='navegando', frame=270)
        e = caught.exception
        self.assertEqual(e.blocked_reason, 'live_engine_stalled')
        self.assertEqual(e.blocked_kind, 'environment')
        self.assertIn('PostLateUpdate', str(e))
        self.assertEqual(e.environment['tolerance_samples'], 3)

    def test_never_fresh_blocks_named(self):
        g = LG.LiveGuard(stale_ms=5000, fresh_wait_s=3)
        start = 10_000
        with self.assertRaises(LG.Blocked) as caught:
            for i in range(0, 10):
                g.heartbeat(start - 60_000, start + i * 500)
        self.assertEqual(caught.exception.blocked_reason, 'live_engine_never_fresh')

    def test_warmup_is_not_a_failure(self):
        g = LG.LiveGuard(fresh_wait_s=45)
        for i in range(0, 6):                      # game booting: no fresh heartbeat yet
            self.assertFalse(g.heartbeat(1000 + i * 500 - 60_000, 1000 + i * 500)['fresh'])
        self.assertTrue(g.heartbeat(9000, 9100)['fresh'])


class FocusGateTests(unittest.TestCase):
    def test_focused_context_passes(self):
        g = LG.LiveGuard()
        self.assertTrue(g.gate(ctx(foco=True), 1000))

    def test_unfocused_context_refuses_dispatch(self):
        g = LG.LiveGuard(focus_wait_s=60)
        self.assertFalse(g.gate(ctx(foco=False, janela='HUD'), 1000))

    def test_focus_never_granted_blocks_named(self):
        g = LG.LiveGuard(focus_wait_s=5)
        with self.assertRaises(LG.Blocked) as caught:
            for i in range(1, 20):
                g.gate(ctx(foco=False, janela=None), 1000 + i * 1000, probe_fase='concluido')
        e = caught.exception
        self.assertEqual(e.blocked_reason, 'focus_not_granted')
        self.assertIn('foco_no_jogo', str(e))
        self.assertEqual(e.environment['bloqueadores'], ['foco_no_jogo'])
        self.assertEqual(e.environment['foco_esperado_s'], 5)
        self.assertEqual(e.environment['probe_fase'], 'concluido')
        self.assertIn('acao_humana', e.environment)

    def test_chat_open_refuses_even_with_focus(self):
        g = LG.LiveGuard(focus_wait_s=5)
        self.assertFalse(g.gate(ctx(foco=True, chat=True), 1000))

    def test_focus_lost_mid_run_blocks_named(self):
        """Focus granted, then stolen by another window: must abort named, not fail generically."""
        g = LG.LiveGuard(focus_wait_s=3)
        self.assertTrue(g.gate(ctx(foco=True), 1000))
        with self.assertRaises(LG.Blocked) as caught:
            for i in range(1, 10):
                g.gate(ctx(foco=False, janela=None), 1000 + i * 1000)
        e = caught.exception
        self.assertEqual(e.blocked_reason, 'focus_lost')
        self.assertTrue(e.environment['foco_ja_visto'])

    def test_focus_after_wait_does_not_abort(self):
        g = LG.LiveGuard(focus_wait_s=10)
        for i in range(1, 8):                              # 3.5 s of unfocused samples
            self.assertFalse(g.gate(ctx(foco=False), 1000 + i * 500))
        self.assertTrue(g.gate(ctx(foco=True), 9000))     # arrived late but inside budget
        self.assertTrue(g.gate(ctx(foco=True), 9500))


class TelemetryTests(unittest.TestCase):
    def test_telemetry_is_json_serializable(self):
        g = LG.LiveGuard(stale_ms=5000, tolerance=2, focus_wait_s=3)
        g.heartbeat(1000, 1100)
        g.heartbeat(1000, 9000)
        g.gate(ctx(foco=False), 1200)
        json.dumps(g.telemetry)
        for key in ('polls', 'stale_samples', 'transient_stale', 'max_stale_ms',
                    'focus_false_samples', 'focus_wait_s'):
            self.assertIn(key, g.telemetry)


if __name__ == '__main__':
    unittest.main(verbosity=2)
