"""Live-bench liveness/focus contract for KIT-AUTO — offline-testable.

The bench drives the kit's INTERNAL action path (`MainThreadPostfix` -> `ProcessarAcao`),
which goes through the SAME guard as the hotkey, including `Application.isFocused`.
This module only observes; it never forces focus (SetForegroundWindow/click would be
synthetic OS input and stays forbidden).

Two states the bench must tell apart:
  * TRANSIENT: the game stops ticking for a moment (scene load, asset hitch) -> heartbeat
    age spikes. Tolerated for a bounded number of consecutive polls.
  * BLOCKED: a real environment prerequisite is missing (no fresh heartbeat, focus never
    granted). Raised as `Blocked`, naming the cause, so the run is NOT reported as an
    evaluation failure.
"""

STALE_MS = 5000                  # heartbeat older than this is stale
STALE_TOLERANCE_SAMPLES = 8      # consecutive stale polls tolerated (~4-5 s of load hitch)
FRESH_WAIT_SECONDS = 45          # adapter must produce ONE fresh heartbeat within this window
FOCUS_WAIT_SECONDS = 60          # real OS focus on the game window must arrive within this window

SAFE_FLAGS = ('chat_aberto', 'digitando', 'remapeando')


class Blocked(RuntimeError):
    """Environment/timing prerequisite unmet: the bench never reached its assertions."""
    blocked_kind = 'environment'

    def __init__(self, reason, detail, environment=None):
        super().__init__(detail)
        self.blocked_reason = reason
        self.environment = environment or {}


class LiveGuard:
    def __init__(self, stale_ms=STALE_MS, tolerance=STALE_TOLERANCE_SAMPLES,
                 fresh_wait_s=FRESH_WAIT_SECONDS, focus_wait_s=FOCUS_WAIT_SECONDS):
        self.stale_ms = stale_ms
        self.tolerance = tolerance
        self.fresh_wait_s = fresh_wait_s
        self.focus_wait_s = focus_wait_s
        self.fresh_seen = False
        self.first_poll_at = None
        self.stale_streak = 0
        self.focus_seen = False
        self.focus_false_first = None
        self.telemetry = {
            'polls': 0, 'stale_samples': 0, 'transient_stale': 0, 'max_stale_ms': 0.0,
            'first_fresh_s': None, 'focus_false_samples': 0, 'focus_wait_s': None,
            'focus_seen_s': None,
        }

    # ------------------------------------------------------------------ liveness --
    def heartbeat(self, engine_ms, now_ms, probe_fase=None, frame=None, janelas=None):
        """Classify one heartbeat sample; raise `Blocked` when the contract is broken."""
        tel = self.telemetry
        tel['polls'] += 1
        if self.first_poll_at is None:
            self.first_poll_at = now_ms
        age = abs(now_ms - engine_ms)
        if age > self.stale_ms:
            self.stale_streak += 1
            tel['stale_samples'] += 1
            tel['max_stale_ms'] = round(max(tel['max_stale_ms'], age), 1)
            detail = {'heartbeat_age_ms': round(age, 1), 'stale_streak': self.stale_streak,
                      'probe_fase': probe_fase, 'frame': frame, 'janelas_ativas': janelas}
            if not self.fresh_seen:
                waited = (now_ms - self.first_poll_at) / 1000
                tel['waiting_first_heartbeat_s'] = round(waited, 1)
                if waited > self.fresh_wait_s:
                    raise Blocked('live_engine_never_fresh',
                        'nenhum heartbeat fresco do adapter em %.0fs (idade do ultimo=%.1fs, '
                        'frame=%s, fase=%s)' % (waited, age / 1000, frame, probe_fase),
                        {'waited_s': round(waited, 1), 'heartbeat_age_ms': round(age, 1),
                         'probe_fase': probe_fase, 'fresh_wait_limit_s': self.fresh_wait_s})
                return {'fresh': False, 'transient': True, 'phase': 'warmup'}
            if self.stale_streak <= self.tolerance:
                tel['transient_stale'] += 1
                return {'fresh': False, 'transient': True, 'phase': 'load-hitch'}
            raise Blocked('live_engine_stalled',
                'heartbeat parado ha %.1fs por %d amostras consecutivas (limite %d amostras, '
                'idade tolerada %sms); fase=%s frame=%s — o loop de PostLateUpdate do jogo '
                'nao esta tickando' % (age / 1000, self.stale_streak, self.tolerance,
                                       self.stale_ms, probe_fase, frame),
                dict(detail, tolerance_samples=self.tolerance, stale_ms=self.stale_ms))
        self.stale_streak = 0
        if not self.fresh_seen:
            self.fresh_seen = True
            tel['first_fresh_s'] = round((now_ms - self.first_poll_at) / 1000, 1)
        return {'fresh': True, 'transient': False}

    # --------------------------------------------------------------------- focus --
    def gate(self, contexto, now_ms, probe_fase=None, janelas=None):
        """True when the kit guard would let the action through; NEVER forces focus.

        Raises `Blocked('focus_not_granted', ...)` when the window never gets real focus
        within `focus_wait_s`.
        """
        tel = self.telemetry
        ctx = contexto or {}
        safe = ctx.get('foco_no_jogo') is True and all(ctx.get(k) is False for k in SAFE_FLAGS)
        if safe:
            if not self.focus_seen:
                self.focus_seen = True
                tel['focus_seen_s'] = tel['focus_wait_s'] or 0.0
            return True
        if self.focus_false_first is None:
            self.focus_false_first = now_ms
        waited = (now_ms - self.focus_false_first) / 1000
        tel['focus_false_samples'] += 1
        tel['focus_false_streak_s'] = tel['focus_wait_s'] = round(waited, 1)
        if self.focus_seen:
            tel['focus_lost_count'] = tel.get('focus_lost_count', 0) + 1
        # Deadline counts CONSECUTIVE unfocused time (focus lost mid-run counts too): the kit
        # refuses the action while the window is unfocused, so the bench cannot make progress.
        if waited > self.focus_wait_s:
            reason = 'focus_lost' if self.focus_seen else 'focus_not_granted'
            blocked_ctx = {k: ctx.get(k) for k in ('janela',) + SAFE_FLAGS + ('foco_no_jogo',)}
            blockers = [k for k in ('foco_no_jogo',) + SAFE_FLAGS
                        if not (ctx.get(k) is True if k == 'foco_no_jogo' else ctx.get(k) is False)]
            raise Blocked(reason,
                'guard do kit recusaria a acao por %.0fs consecutivos em %d amostras '
                '(bloqueadores=%s, janela=%s, fase do probe=%s, foco ja visto=%s); o dispatch '
                'interno usa o MESMO guard do atalho e a bancada NAO forca foco '
                '(SetForegroundWindow/clique = input sintetico, proibido pela trava)'
                % (waited, tel['focus_false_samples'], blockers, ctx.get('janela'), probe_fase,
                   self.focus_seen),
                {'contexto': blocked_ctx, 'bloqueadores': blockers, 'probe_fase': probe_fase,
                 'foco_esperado_s': self.focus_wait_s, 'janelas_ativas': janelas,
                 'foco_ja_visto': self.focus_seen,
                 'acao_humana': 'traga a janela do jogo ao primeiro plano e nao interaja com '
                                'outras janelas durante o run; o runner espera ate %ds por foco '
                                'real e aborta nomeando o motivo' % self.focus_wait_s})
        return False
