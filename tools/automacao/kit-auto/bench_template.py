"""KIT-AUTO bench: native handlers on disposable party; no OS input.
Flattened from the exercised KIT16/F3/F5 recipe. Never import this template.
ROOT/OUT/OLD/EXPECTED/SESSION and callbacks are supplied by runner.py.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime

KITS = ROOT / 'scratch/kit'
DLL = OLD / 'AUT4Probe.dll'
PROFILE = OUT / 'bepinex-iso/BepInEx'
DATAISO = OUT / 'dados-iso'
REAL = Path.home() / 'AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm'
GAME = Path('E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm.exe')
ENV = dict(os.environ, PROBE_DLL=str(DLL), ISO_DIR=str(PROFILE.parent),
           ISO_BEPINEX=str(PROFILE), ISO_ROOT=str(DATAISO),
           EVID_DIR=str(OUT / 'isolamento'), WORKER_ID=SESSION,
           HASHES_ANTES=str(OUT / 'bepinex-antes.txt'),
           CRIADOS=str(OUT / 'bepinex-criados.txt'),
           SAVES_MANIFEST_DIR=str(OUT / 'saves-antes'))
OUT.mkdir(parents=True, exist_ok=False)
ENV['REG_PATH'] = r'HKCU\Software\Burst2Flame Entertainment\Stolen Realm'
# Bind every path explicitly; inherited fixture overrides cannot weaken the real guards.
for _key in ('GAME_RUNNING_OVERRIDE','KIT16_FIXTURE','STUB_OMITE_MARCADOR','SAVES_DIR','SAVES_DIRS',
             'LOCK_FILE','PID_FILE','KITS_DIR','SAVES_LOCALLOW','SAVES_ABYSSUS'):
    ENV.pop(_key,None)
ENV.update(REAL_DIR=str(REAL), R2MODMAN_PROFILE=str(Path.home()/'AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx'),
           PYTHON=sys.executable)
STEPS = []
SAMPLES = []
RESULT = {'sessao': SESSION, 'scope': 'empty-test-boot-roteiro-boot01-window-120s',
          'limiares': 'DISPENSADOS', 'comparacao_recorder': 'NAO_EXERCITADO'}


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def command(label, args, require=True, timeout=45):
    p = subprocess.run(args, cwd=ROOT, env=ENV, capture_output=True, timeout=timeout)
    (OUT / (label + '.stdout.log')).write_bytes(p.stdout)
    (OUT / (label + '.stderr.log')).write_bytes(p.stderr)
    STEPS.append({'label': label, 'args': args, 'exit': p.returncode})
    save('commands.json', STEPS)
    print(label, 'exit', p.returncode, flush=True)
    if require and p.returncode:
        raise RuntimeError(label + ' exit ' + str(p.returncode))
    return p


def kit(label, script, action, require=True):
    return command(label, ['C:/Program Files/Git/bin/bash.exe', (KITS / script).as_posix(), action], require=require)


def ps(text):
    p = subprocess.run(['powershell.exe', '-NoProfile', '-Command', text],
                       capture_output=True, timeout=15)
    if p.returncode:
        raise RuntimeError('PowerShell read/close failed rc=' + str(p.returncode))
    return p.stdout.decode('utf-8', errors='replace').strip()


def processes():
    text = ps("ConvertTo-Json -Compress -InputObject @(Get-Process -Name 'Stolen Realm' -ErrorAction SilentlyContinue | Select-Object Id,Path,WorkingSet64,PrivateMemorySize64,CPU)")
    return json.loads(text or '[]')


locked = False
profile_prepared = False
data_attempted = False
pid = None
launched = False
started = None
try:
    if processes():
        raise RuntimeError('Foreign/existing game process; refused')
    if PROFILE.parent.exists() or DATAISO.exists():
        raise RuntimeError('Refusing to reuse isolated roots')
    if sha(DLL) != EXPECTED:
        raise RuntimeError('Probe build hash changed; refused')
    inputs = json.loads((OLD.parent / 'inputs.json').read_text(encoding='utf-8'))
    for name, expected in inputs['files'].items():
        if sha(OLD / name) != expected:
            raise RuntimeError('Identified input drift: ' + name)
    RESULT['input_identity'] = inputs
    RESULT['cloud_start'] = require_cloud_off()
    kit('front-check', 'front-unica.sh', 'check')
    kit('front-acquire', 'front-unica.sh', 'acquire')
    locked = True
    _baseline = baseline(OUT)
    profile_prepared = True
    kit('bepinex-preparar', 'runtime-isolado.sh', 'preparar')
    installed = PROFILE / 'plugins/KitRuntimeProbe/AUT4Probe.dll'
    if SEM_PROBE:
        import shutil as _sh
        for _pl in (PROFILE / 'plugins').iterdir():
            if _pl.is_dir():
                _sh.rmtree(str(_pl))
            else:
                _pl.unlink()
        RESULT['probes_removidos'] = True
        RESULT['plugins_restantes'] = [p.name for p in (PROFILE / 'plugins').iterdir()]
    else:
        if sha(installed) != EXPECTED:
            raise RuntimeError('Installed hash mismatch')
        RESULT['installed_dll_sha256'] = sha(installed)
    sys.path.insert(0, str(ROOT / 'tools/automacao/runtime'))
    import coletor
    config = coletor.derivar_config(str(PROFILE), str(OUT / 'probe'), True,
                                   dll_probe=str(installed), navegar=True, orcamento=90,
                                   max_textos=400, sessao=SESSION, demostrar=False,
                                   autoriza_escrita=False)
    cfg = PROFILE / 'config/com.gumatos.aut4probe.cfg'
    coletor.escrever_cfg(str(cfg), config)
    with open(str(cfg), 'a', encoding='utf-8') as _fh:
        _fh.write('\nNavegarTentativasMax = ' + NAV_TETO + '\n'
                  + 'NavegarRota = ' + NAV_ROTA + '\n'
                  + 'NavegarAlvoNome = ' + NAV_ALVO + '\n')
    with cfg.open('a', encoding='utf-8') as fh:
        fh.write('EsperarInteractable = true\nCliqueFisico = true\nCliqueFisicoEstavel = 10\n')
    save('config-declarada.json', config)
    RESULT['config_sha256'] = sha(cfg)
    setup_plugins(PROFILE, RESULT, SESSION, 'with-passive')
    data_attempted = True
    kit('dados-preparar', 'kit16-save-isolado.sh', 'preparar')
    state = ps("(Get-Item -LiteralPath '" + str(REAL) + "').LinkType")
    if state != 'Junction':
        raise RuntimeError('Junction not active before boot')
    if processes():
        raise RuntimeError('External process appeared before launch; refused')
    prepare_empty(DATAISO, REAL, RESULT, ps, save)
    RESULT['immediate_baseline_at_boot'] = verify_baseline(_baseline, OUT, backed_up=True)
    if not (DATAISO / 'registro-antes.reg').is_file():
        raise RuntimeError('Registry backup absent: refuse boot')
    RESULT['cloud_before_boot'] = require_cloud_off()
    started = time.monotonic()
    command('steam-launch', ['C:/Program Files (x86)/Steam/steam.exe', '-applaunch', '1330000',
                            '--doorstop-enabled', 'true', '--doorstop-target-assembly',
                            str(PROFILE / 'core/BepInEx.Preloader.dll'),
                            '--doorstop-mono-dll-search-path-override', str(PROFILE / 'core')])
    launched = True
    while time.monotonic() - started < 120:
        procs = processes()
        if len(procs) > 1 and pid is not None:
            _fim = time.monotonic() + 30
            while len(procs) > 1 and time.monotonic() < _fim:
                time.sleep(1)
                procs = processes()
            RESULT.setdefault('duplicata_transitoria', []).append(
                {'observada_em_s': round(time.monotonic() - started, 1),
                 'pids_finais': [p['Id'] for p in procs]})
            if len(procs) > 1 or all(p['Id'] != pid for p in procs):
                raise RuntimeError('Multiple game processes; cannot assume ownership')
        elif len(procs) > 1:
            raise RuntimeError('Multiple game processes; cannot assume ownership')
        if procs:
            proc = procs[0]
            if Path(proc['Path']).resolve() != GAME.resolve():
                raise RuntimeError('Unexpected game exe path')
            if pid is None:
                pid = proc['Id']
                RESULT['created_pid'] = pid
            if proc['Id'] != pid:
                raise RuntimeError('PID changed')
            SAMPLES.append(dict(proc, elapsed_seconds=time.monotonic() - started))
            save('process-samples.json', SAMPLES)
        elif pid is not None:
            RESULT['processo_sumiu_em_s'] = round(time.monotonic() - started, 1)
            break
        if pid is not None:
            live_step(pid, PROFILE, SESSION, RESULT, ps, save)
        evidence = OUT / 'probe/aut4probe.json'
        if evidence.exists():
            try:
                observed = json.loads(evidence.read_text(encoding='utf-8-sig'))
                RESULT['observed_status'] = observed.get('status')
                RESULT['observed_fase'] = observed.get('fase')
                if observed.get('fase') == 'concluido' or observed.get('status') in ['CONCLUIDO', 'ERRO', 'SEM_UI', 'ORCAMENTO_ESTOURADO']:
                    RESULT['terminal_probe_seen'] = True
                    if 'terminal_since' not in globals(): terminal_since = time.monotonic()
                    if time.monotonic() - terminal_since >= 3 and auto_state['done']:
                        live = PROFILE.parent / 'recorder'
                        RESULT['recorder_files_before_close'] = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in live.glob('*') if p.is_file()}
                        break
            except (json.JSONDecodeError, OSError):
                pass  # Writer may be between truncate and flush; bounded by 120s.
        time.sleep(0.25)
    RESULT['elapsed_seconds'] = time.monotonic() - started
    RESULT['probe_json_exists'] = (OUT / 'probe/aut4probe.json').exists()
    if not auto_state['done']:
        # Named, not generic: the bench window closed before the kit dispatch completed.
        _tel = auto_state['telemetry']
        raise Blocked('bench_window_exhausted',
            'janela da bancada (%.0fs) terminou sem concluir o despacho do kit: acoes=%s, '
            'fase=%s, foco_no_jogo=%s, heartbeat_max_stale=%.1fs'
            % (RESULT['elapsed_seconds'], auto_state['actions'],
               RESULT.get('observed_fase'),
               (auto_state.get('guard').focus_seen if auto_state.get('guard') else None),
               _tel.get('max_stale_ms', 0.0) / 1000),
            {'elapsed_s': round(RESULT['elapsed_seconds'], 1),
             'actions': list(auto_state['actions']),
             'probe_fase': RESULT.get('observed_fase'),
             'focus_seen': (auto_state.get('guard').focus_seen if auto_state.get('guard') else None),
             'live_engine': dict(_tel)})
    RESULT['pngs'] = [{'name': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)}
                      for p in (OUT / 'probe').glob('*.png')]
except Exception as e:
    RESULT['error'] = type(e).__name__ + ': ' + str(e)
    # KIT-AUTO: environment/timing prerequisite must be distinguishable from a real failure.
    if getattr(e, 'blocked_reason', None):
        RESULT['blocked_reason'] = e.blocked_reason
        RESULT['blocked_kind'] = getattr(e, 'blocked_kind', 'environment')
        RESULT['blocked_detail'] = str(e)
        RESULT['environment'] = getattr(e, 'environment', None)
finally:
    def cleanup_step(name, fn):
        try:
            return fn()
        except Exception as e:
            RESULT.setdefault('cleanup_errors', {})[name] = type(e).__name__ + ': ' + str(e)
            return None
    def own_lock():
        f = KITS / 'lock.txt'
        if not f.exists():
            return False
        fields = f.read_text(encoding='utf-8').strip().split('|')
        return len(fields) == 4 and fields[2] == ENV['WORKER_ID']
    try:
        current = processes()
        if launched and pid is None and len(current) == 1 and Path(current[0]['Path']).resolve() == GAME.resolve():
            pid = current[0]['Id']
            RESULT['created_pid'] = pid
        if pid is not None:
            cleanup_step('close', lambda: ps("$p=Get-Process -Id " + str(pid) + " -ErrorAction SilentlyContinue; if ($p -and $p.Path -eq '" + str(GAME) + "') {$p.CloseMainWindow() | Out-Null}; exit 0"))
            end = time.monotonic() + 30
            while processes() and time.monotonic() < end:
                time.sleep(1)
        if processes() and pid is not None:
            cleanup_step('close-retry', lambda: ps("$p=Get-Process -Id " + str(pid) + " -ErrorAction SilentlyContinue; if ($p -and $p.Path -eq '" + str(GAME) + "') {$p.CloseMainWindow() | Out-Null}; exit 0"))
            end = time.monotonic() + 30
            while processes() and time.monotonic() < end:
                time.sleep(1)
        closed = not processes()
        RESULT['game_closed'] = closed
        if not closed:
            raise RuntimeError('Game remains alive: KEEP link/profile/lock; no unsafe rollback')
        RESULT['cloud_end_before_restore'] = cloud_state()
        if locked and not own_lock():
            raise RuntimeError('Lost own lock: refuse external state writes')
        def preserve():
            dest = OUT / 'preserved'
            dest.mkdir(exist_ok=False)
            if (PROFILE / 'LogOutput.log').exists():
                shutil.copy2(PROFILE / 'LogOutput.log', dest / 'LogOutput-isolado.txt')
            if (PROFILE.parent / 'recorder').exists():
                shutil.copytree(PROFILE.parent / 'recorder', dest / 'recorder')
            if (PROFILE / 'config').exists():
                shutil.copytree(PROFILE / 'config', dest / 'config')
            for name in ('Player.log', 'Player-prev.log'):
                src = DATAISO / 'dados-do-jogo' / name
                if src.exists():
                    shutil.copy2(src, dest / name)
        if profile_prepared:
            cleanup_step('preserve', preserve)
        if data_attempted:
            backup = REAL.parent / 'Stolen Realm.kit16-real'
            if backup.exists():
                cleanup_step('data-verify', lambda: kit('dados-verificar', 'kit16-save-isolado.sh', 'verificar'))
                cleanup_step('data-restore', lambda: kit('dados-restaurar', 'kit16-save-isolado.sh', 'restaurar'))
            if backup.exists() or not REAL.is_dir() or REAL.is_junction():
                raise RuntimeError('Data NOT restored: KEEP profile/lock')
        if (DATAISO / 'registro-antes.reg').exists():
            if sha(DATAISO / 'registro-antes.reg') != sha(DATAISO / 'registro-depois.reg'):
                raise RuntimeError('PlayerPrefs not restored')
            RESULT['playerprefs_export_equal'] = True
        if '_baseline' in globals():
            RESULT['immediate_baseline_after'] = cleanup_step('baseline-after', lambda: verify_baseline(_baseline, OUT))
        if profile_prepared:
            cleanup_step('bepinex-rollback', lambda: kit('bepinex-rollback', 'runtime-isolado.sh', 'rollback'))
            if PROFILE.parent.exists():
                raise RuntimeError('Profile remains: KEEP own lock')
        if data_attempted and DATAISO.exists():
            kit('dados-limpar', 'kit16-save-isolado.sh', 'limpar')
            if DATAISO.exists():
                raise RuntimeError('Disposable data remains')
        if locked:
            if not own_lock():
                raise RuntimeError('Lock ownership changed before release')
            kit('front-release', 'front-unica.sh', 'release')
            RESULT['own_lock_released'] = not (KITS / 'lock.txt').exists()
        RESULT['final_state'] = {'game_processes': processes(), 'production_junction': REAL.is_junction(),
                                 'production_backup_exists': (REAL.parent / 'Stolen Realm.kit16-real').exists(),
                                 'isolated_profile_exists': PROFILE.parent.exists(),
                                 'cloud': require_cloud_off()}
    except Exception as e:
        RESULT['cleanup_error'] = type(e).__name__ + ': ' + str(e)
    try:
        RESULT['live_contract'] = LIVE_CONTRACT
        RESULT['live_engine'] = json.loads(json.dumps(auto_state.get('telemetry', {})))
        RESULT['auto_actions'] = list(auto_state.get('actions', []))
    except NameError:
        pass
    save('result.json', RESULT)
    print(json.dumps(RESULT, ensure_ascii=False, indent=2), flush=True)

# exit 3 = environment prerequisite unmet (the bench never reached the assertions)
if RESULT.get('blocked_reason') and not RESULT.get('cleanup_error') and not RESULT.get('cleanup_errors'):
    sys.exit(3)
sys.exit(1 if RESULT.get('error') or RESULT.get('cleanup_error') or RESULT.get('cleanup_errors') else 0)
