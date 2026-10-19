"""KIT-AUTO support, extracted from exercised KIT16 recipe.
No imports of historical workspaces. Cloud is read-only; baseline is immediate.
"""
from pathlib import Path
from datetime import datetime
import hashlib, json, os, re, shutil
REAL = Path.home() / 'AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm'
DONO = Path.home() / 'AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx'
OTHER = Path.home() / 'AppData/Local/Abyssus/Saved/SaveGames'
STEAM_USER = Path('C:/Program Files (x86)/Steam/userdata/37602317')
def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def manifest(root):
    root = Path(root)
    if not root.is_dir() or root.is_junction() or root.is_symlink():
        raise RuntimeError('Invalid manifest root: ' + str(root))
    data = {}
    for parent, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(parent) / name
            if p.is_junction() or p.is_symlink():
                raise RuntimeError('Reparse point in production tree: ' + str(p))
        for name in files:
            p = Path(parent) / name
            data[p.relative_to(root).as_posix()] = [p.stat().st_size, sha(p)]
    return dict(sorted(data.items()))

def compare(a, b):
    added = sorted(set(b) - set(a))
    removed = sorted(set(a) - set(b))
    changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    return {'before': len(a), 'after': len(b), 'new': added, 'removed': removed,
            'changed': changed, 'equal': not (added or removed or changed)}

def baseline(out):
    roots = {'production': REAL, 'profile': DONO}
    if OTHER.is_dir():
        roots['other-game'] = OTHER
    data = {key: {'root': str(root), 'files': manifest(root)} for key, root in roots.items()}
    (out / 'private-baseline.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    return data

def verify_baseline(before, out, backed_up=False):
    result = {}
    for key, value in before.items():
        root = Path(value['root'])
        if backed_up and key == 'production':
            root = REAL.parent / 'Stolen Realm.kit16-real'
        result[key] = compare(value['files'], manifest(root))
    (out / ('baseline-at-boot.json' if backed_up else 'baseline-after.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
    if not all(v['equal'] for v in result.values()):
        raise RuntimeError('Immediate baseline diverged: ' + json.dumps(result))
    return result


def app_blocks(text):
    blocks = []
    for match in re.finditer(r'"1330000"\s*\{', text):
        start = match.end() - 1
        depth = 0
        quoted = False
        escaped = False
        for i in range(start, len(text)):
            ch = text[i]
            if quoted:
                if escaped:
                    escaped = False
                elif ch == '\\':
                    escaped = True
                elif ch == '"':
                    quoted = False
                continue
            if ch == '"':
                quoted = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    blocks.append(text[start:i + 1])
                    break
        else:
            raise RuntimeError('Malformed Steam app block')
    return blocks

def cloud_state():
    shared = STEAM_USER / '7/remote/sharedconfig.vdf'
    fields = []
    for block in app_blocks(shared.read_text(encoding='utf-8')):
        fields.extend(re.findall(r'"cloudenabled"\s*"([^"]*)"', block, re.I))
    cache = STEAM_USER / '1330000/remotecache.vdf'
    return {'measured_at': datetime.now().astimezone().isoformat(),
            'sharedconfig_path': str(shared), 'app_id': '1330000',
            'app_cloudenabled': fields, 'configuration_off': fields == ['0'],
            'cache_path': str(cache),
            'cache_mtime_ns': cache.stat().st_mtime_ns if cache.exists() else None,
            'cache_mtime_local': datetime.fromtimestamp(cache.stat().st_mtime).astimezone().isoformat() if cache.exists() else None,
            'note': 'Per-app config readback plus operator confirmation, not remote-server inspection.'}

def require_cloud_off():
    state = cloud_state()
    if not state['configuration_off']:
        raise RuntimeError('Cloud app config is not explicitly off')
    return state


def prepare_empty(DATAISO, REAL, RESULT, ps, save):
    require_cloud_off()
    iso = DATAISO / 'dados-do-jogo'
    if ps("(Get-Item -LiteralPath '" + str(REAL) + "').LinkType") != 'Junction':
        raise RuntimeError('Not junction; refuse to touch copied data')
    targets = json.loads(ps("ConvertTo-Json -Compress -InputObject @((Get-Item -LiteralPath '" + str(REAL) + "').Target)"))
    if len(targets) != 1 or Path(targets[0]).resolve() != iso.resolve():
        raise RuntimeError('Unexpected junction target')
    # Preserve the copied personal data locally, outside the path consumed by the game.
    quarantine = DATAISO / 'copia-nao-usada-privada'
    quarantine.mkdir(exist_ok=False)
    for child in list(iso.iterdir()):
        shutil.move(str(child), str(quarantine / child.name))
    if list(iso.iterdir()):
        raise RuntimeError('Isolated data did not become empty')
    RESULT['empty_test_data_verified'] = True
    RESULT['personal_save_selected'] = False
    save('empty-data-check.json', {'empty': True, 'target': str(iso),
                                 'personal_copy_used': False})
