"""Plant real defects in the live contract and require the regressions to go RED.

Copies `live_guard.py` + `test_live_contract.py` into a disposable tree, breaks one rule
at a time, and requires `test_live_contract.py` to fail and to name the pinning test.
No game, no network, no source edit: the original file hash is checked before and after.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys

HERE = Path(__file__).resolve().parent
OUT = HERE / 'live-contract-proof'
SRC = HERE / 'live_guard.py'
TEST = HERE / 'test_live_contract.py'

MUTATIONS = {
    'no_focus_deadline': (
        "        if waited > self.focus_wait_s:\n",
        "        if False:  # MUTATION: no focus deadline\n",
        "test_focus_never_granted_blocks_named"),
    'no_focus_lost': (
        "            reason = 'focus_lost' if self.focus_seen else 'focus_not_granted'\n",
        "            reason = 'focus_not_granted'  # MUTATION: does not distinguish focus lost\n",
        "test_focus_lost_mid_run_blocks_named"),
    'no_stall_abort': (
        "            if self.stale_streak <= self.tolerance:\n",
        "            if True:  # MUTATION: never aborts on a stall\n",
        "test_stall_past_tolerance_blocks_named"),
    'no_warmup_deadline': (
        "                if waited > self.fresh_wait_s:\n",
        "                if False:  # MUTATION: waits forever for the first heartbeat\n",
        "test_never_fresh_blocks_named"),
}

original_hash = hashlib.sha256(SRC.read_bytes()).hexdigest()
if OUT.exists():
    shutil.rmtree(OUT)
results = {}


def run_case(name, source_text):
    case = OUT / name
    (case / 'mod').mkdir(parents=True)
    (case / 'mod' / 'live_guard.py').write_text(source_text, encoding='utf-8')
    shutil.copy2(TEST, case / 'mod' / 'test_live_contract.py')
    p = subprocess.run([sys.executable, 'test_live_contract.py'], cwd=str(case / 'mod'),
                       capture_output=True, timeout=120)
    text = (p.stdout + p.stderr).decode(errors='replace')
    (case / 'tests.log').write_text(text, encoding='utf-8')
    return {'exit': p.returncode,
            'failures': sorted({line.split()[1] for line in text.splitlines()
                                if line.startswith(('FAIL:', 'ERROR:'))})}


results['baseline'] = run_case('baseline', SRC.read_text(encoding='utf-8'))
for name, (old, new, expected_test) in MUTATIONS.items():
    text = SRC.read_text(encoding='utf-8')
    assert text.count(old) == 1, (name, text.count(old))
    results[name] = dict(run_case(name, text.replace(old, new)),
                         expected_test=expected_test)

assert results['baseline']['exit'] == 0, results['baseline']
for name, expected_test in ((k, v[2]) for k, v in MUTATIONS.items()):
    r = results[name]
    assert r['exit'] != 0, (name, 'mutation did not bite', r)
    assert expected_test in r['failures'], (name, 'wrong test failed', r)
assert hashlib.sha256(SRC.read_bytes()).hexdigest() == original_hash, 'source changed!'
(OUT / 'RESULTADO.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
