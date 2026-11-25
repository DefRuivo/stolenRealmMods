"""Verify the tooltip geometry contract on a real, isolated Unity run.

Input: receipt.json and probe.tsv from the SR live validation probe. No Unity
assemblies, saves, or profile contents are read here. Exit 2 means missing evidence;
exit 1 means the captured run actually violates the contract.
"""
import argparse
import base64
import json
from pathlib import Path

RSTV = 'com.gumatos.roguelikeskilltreevisualizer'
NATIVE_PARENT = 'GUI Manager/Tooltips / Popups'
OVERLAY = 'RstvSkillTreesWindow'


def parse(run):
    receipt = json.loads((run / 'receipt.json').read_text(encoding='utf-8-sig'))
    assert receipt.get('probe_result') == 'ok' and not receipt['errors'], receipt['errors']
    for flag in ('player_prefs_byte_equal', 'game_files_equal', 'final_cloud_off', 'no_personal_save_selected'):
        assert receipt.get(flag) is True, ('isolation', flag)
    assert receipt['identity']['steam_build'] == ['26878331'], 'different game build'
    geom, plugins = {}, {}
    for line in (run / 'probe.tsv').read_text(encoding='utf-8-sig').splitlines():
        cols = line.split('\t')
        if cols[:2] not in (['event', 'geom'], ['event', 'plugin']):
            continue
        a = [base64.b64decode(v, validate=True).decode('utf-8') for v in cols[4:]]
        out = geom if cols[1] == 'geom' else plugins
        assert a[0] not in out, ('duplicate label', a[0])
        out[a[0]] = a[1:]
    return geom, plugins


# geometry fields after label: parent, sibling, localScale, lossyScale,
# main local/lossy scales, rect width/height, projected width/height,
# resolution, canvas scale, active, title, description, font size, text width, DPI.
def verify(run, reference, expect_rstv, sha256):
    geo, plugins = parse(run)
    control, reference_plugins = parse(reference)
    assert (RSTV in plugins) == expect_rstv and RSTV not in reference_plugins, 'wrong RSTV arm'
    assert {g: d[:2] for g, d in plugins.items() if g != RSTV} == {
        g: d[:2] for g, d in reference_plugins.items() if g != RSTV
    }, 'different probe or other plugins'
    if sha256:
        assert plugins[RSTV][1] == sha256, 'different RSTV DLL'

    steps = {
        'potion-native-item-tooltip': False,
        'bard-before': False,
        'bard-window-open': True,
        'bard-after-close-same-size': False,
        'bard-resized-after-close': False,
        'bard-back-at-original-size': False,
        **{f'cycle-{i}-{phase}': phase == 'open' for i in range(4) for phase in ('open', 'closed')},
        'resize-open-before': True,
        'resize-open-small': True,
        'resize-small-after-close': False,
        'resize-original-open': True,
        'resize-original-after-owner-close': False,
        'potion-after-window': False,
    }
    assert set(geo) == steps.keys() == set(control), ('missing or extra trace steps', sorted(set(steps) ^ set(geo)), sorted(set(steps) ^ set(control)))
    assert geo['resize-open-before'][10] != geo['resize-open-small'][10], 'no resolution change while open'
    assert geo['resize-open-before'][10] == geo['resize-original-open'][10], 'did not return to original resolution'
    failures = []
    for label, opened in steps.items():
        a, b = geo[label], control[label]
        if a[10] != b[10]:
            failures.append(f'{label}: resolution {a[10]} != {b[10]}')
        wants_overlay = opened and expect_rstv
        correct_parent = a[0].split('/')[0] == OVERLAY if wants_overlay else a[0] == NATIVE_PARENT and a[1] == b[1]
        if not correct_parent or a[12] != 'True':
            failures.append(f'{label}: parent/sibling/active = {a[0:2]} / {a[12]}')
        if a[2] != b[2]:
            failures.append(f'{label}: localScale {a[2]} != {b[2]}')
        if abs(float(a[8]) - float(b[8])) > .5 or a[3] != b[3]:
            failures.append(f'{label}: width/scale {a[8]}px {a[3]} != {b[8]}px {b[3]}')
        if a[13:15] != b[13:15]:
            failures.append(f'{label}: title or description changed')
        print(f'{label}: {a[8]}px vs {b[8]}px at {a[10]} / {a[0]} / local {a[2]}')
    # Height is intentionally not an invariant: the tooltip may grow with Rich Text/layout.
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('reference', type=Path)
    parser.add_argument('--reference-only', action='store_true')
    parser.add_argument('--dll-sha256')
    a = parser.parse_args()
    try:
        failures = verify(a.run, a.reference, not a.reference_only, a.dll_sha256)
    except (OSError, ValueError, AssertionError, KeyError) as e:
        print('UNVERIFIED:', e)
        return 2
    for error in failures:
        print('FAIL:', error)
    print('RESULT', 'FAIL' if failures else 'PASS', 'inGame=true', 'failures=', len(failures))
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
