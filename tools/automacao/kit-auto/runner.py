"""KIT-AUTO: two fresh isolated boots, internal kit action dispatch, JSON result.
Local bench adapter: seven pinned repo helpers and identified frozen inputs.
No dependency on historical task workspaces.
No computer_use, OS input, production deploy, publication or kit acceptance.
"""
from pathlib import Path
import argparse, ast, contextlib, hashlib, importlib.util, json, os, shutil, subprocess, sys, time

HERE = Path(__file__).resolve().parent

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def cmd(args, out, label, env=None, timeout=300):
    p = subprocess.run(args, capture_output=True, timeout=timeout, env=env)
    (out / (label + '.stdout.log')).write_bytes(p.stdout)
    (out / (label + '.stderr.log')).write_bytes(p.stderr)
    return {'args': args, 'exit': p.returncode}

def build(repo, out):
    source = HERE / 'candidate'
    sandbox = out / 'build-sandbox'
    shutil.copytree(source, sandbox, ignore=shutil.ignore_patterns('bin','obj','__pycache__'))
    env = dict(os.environ)
    home = out / 'build-home'; home.mkdir()
    for key, sub in [('USERPROFILE','user'),('APPDATA','roaming'),('LOCALAPPDATA','local')]:
        env[key] = str(home / sub); Path(env[key]).mkdir()
    env['DOTNET_CLI_HOME'] = str(home)
    env['TEMP']=env['TMP']=str(home/'temp'); (home/'temp').mkdir()
    gate = load('deploy_gate', repo / 'tools/check_deploy_optin.py')
    unsafe = out / 'unsafe.csproj.fixture'
    unsafe.write_text('<Project><Target Name="Bad"><Copy SourceFiles="x.dll" DestinationFolder="$(USERPROFILE)/BepInEx/plugins" /></Target></Project>')
    if not gate.analisa_arquivo(str(unsafe)):
        raise RuntimeError('Deploy preflight negative did not bite')
    steps = [cmd([sys.executable,str(repo/'tools/check_deploy_optin.py'),'--raiz',str(sandbox),'--json'],out,'preflight',env)]
    if steps[-1]['exit'] != 0: raise RuntimeError('Unsafe build refused')
    project = sandbox / 'tools/automacao/runtime/KIT04Adapter.SR/KIT04Adapter.SR.csproj'
    steps.append(cmd(['dotnet','build',str(project),'-c','Release','--no-incremental',
        '-p:DeployToBepInEx=false','-p:USERPROFILE='+env['USERPROFILE'],
        '-p:APPDATA='+env['APPDATA'],'-p:LOCALAPPDATA='+env['LOCALAPPDATA'],
        '-p:RefLibDir='+str(repo/'lib'),
        '-p:GameManaged=E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed',
        '-o',str(out/'build')],out,'build',env))
    write(out/'build.json',{'steps':steps,'candidate_sources':{p.relative_to(source).as_posix():sha(p) for p in source.rglob('*') if p.is_file() and not any(x in p.parts for x in ('bin','obj','__pycache__'))}})
    if steps[-1]['exit'] != 0: raise RuntimeError('Build failed; see build.stdout.log')
    harness=sandbox/'tools/automacao/runtime/harness-controle/HarnessControle.csproj'
    hb=cmd(['dotnet','build',str(harness),'-c','Release','-p:DeployToBepInEx=false','-o',str(out/'harness')],out,'harness-build',env)
    if hb['exit']!=0: raise RuntimeError('Harness build failed')
    tests=cmd(['dotnet',str(out/'harness/HarnessControle.dll')],out,'harness-tests',env)
    write(out/'harness.json',{'build':hb,'tests':tests})
    if tests['exit']!=0: raise RuntimeError('Control/guard tests failed')

def verify_dependencies(repo):
    expected=read(HERE/'dependencies.json')['files']
    for rel,digest in expected.items():
        if sha(repo/rel)!=digest: raise RuntimeError('Bench dependency drift: '+rel)
    frozen=read(HERE/'frozen-inputs.json')['files']
    for name,digest in frozen.items():
        if sha(HERE/'frozen-inputs'/name)!=digest: raise RuntimeError('Frozen input drift: '+name)


def preflight(repo):
    verify_dependencies(repo)
    support=load('auto_bench_support',HERE/'bench_support.py')
    p=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "ConvertTo-Json -Compress -InputObject @(Get-Process -Name 'Stolen Realm' -ErrorAction SilentlyContinue | Select-Object Id,Path)"],capture_output=True,timeout=20,check=True)
    games=json.loads(p.stdout.decode('utf-8-sig').strip() or '[]')
    state={'games':games,'cloud':support.require_cloud_off(),
        'junction':support.REAL.is_junction(),
        'backup_exists':(support.REAL.parent/'Stolen Realm.kit16-real').exists(),
        'lock_exists':(repo/'scratch/kit/lock.txt').exists()}
    if games or state['junction'] or state['backup_exists'] or state['lock_exists']:
        raise RuntimeError('Runtime preflight refused: '+str(state))
    return state


def boot(repo, out, case):
    support=load('auto_bench_support',HERE/'bench_support.py')
    initial=preflight(repo)
    case_dir=out/case; case_dir.mkdir(exist_ok=False)
    target=case_dir/'recorder-on'; target.mkdir()
    inputs=target/'inputs'; inputs.mkdir()
    frozen=read(HERE/'frozen-inputs.json')
    for name,h in frozen['files'].items():
        p=HERE/'frozen-inputs'/name
        if sha(p)!=h: raise RuntimeError('Frozen runtime input drift: '+name)
        shutil.copy2(p,inputs/name)
    ident={'files':dict(frozen['files']),
        'core_source_sha256':frozen['files']['CorePlugin.cs'],
        'rstv_dll_sha256':frozen['files']['RoguelikeSkillTreeVisualizer.dll'],
        'builds_this_run':1}
    project = HERE/'candidate/tools/automacao/runtime/KIT04Adapter.SR'
    replacements = {p.name:p for p in project.glob('*.cs')}
    replacements['KIT04Adapter.SR.dll'] = out/'build/KIT04Adapter.SR.dll'
    replacements['RoguelikeDebugger.dll'] = repo/'RoguelikeDebugger/bin/Release/netstandard2.1/RoguelikeDebugger.dll'
    for name, p in replacements.items():
        shutil.copy2(p, inputs/name); ident['files'][name] = sha(inputs/name)
    ident['source_set_sha256'] = hashlib.sha256(json.dumps({n:h for n,h in ident['files'].items() if n.endswith('.cs')},sort_keys=True).encode()).hexdigest()
    ident['note'] = 'KIT-AUTO candidate; unchanged F5 probe/F3 Core/RSTV; current identified Debugger; no owner deploy'
    ident['game_sha256'] = sha(Path('E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed/Assembly-CSharp.dll'))
    write(target/'inputs.json',ident)
    def setup(profile, result, session, ignored):
        names=('KIT04Core.dll','KIT04Adapter.SR.dll','RoguelikeSkillTreeVisualizer.dll',
            'RealmApi.dll','RealmApi.Core.dll','RealmApi.Hooks.dll','RoguelikeDebugger.dll')
        dst=profile/'plugins/KitAuto'; dst.mkdir()
        installed={}
        for name in names:
            shutil.copy2(inputs/name,dst/name)
            if sha(dst/name)!=ident['files'][name]: raise RuntimeError('Installed input drift: '+name)
            installed[name]=sha(dst/name)
        result['installed_plugins_sha256']=installed
        core=('[Modo]\nhabilitado = true\nidSessao = '+session+
            '\nambiente = KIT-AUTO-disposable\nhashFonteDeclarado = '+ident['core_source_sha256']+
            '\ncaminhoSaida = '+str(profile.parent/'recorder')+
            '\norcamentoSegundos = 120\nmaxAmostras = 400\nmaxEventos = 1000\n'
            '[Passivo]\nfilaMax = 400\nretencaoMax = 400\ntetoCapturas = 20\ntimeoutJanelaMs = 1500\n')
        adapter='[Modo]\nhabilitado = true\npassivoHabilitado = true\ncaminhoSaida = '+str(profile.parent/'recorder')+'\n'
        (profile/'config/com.gumatos.kit04.core.cfg').write_text(core,encoding='utf-8')
        (profile/'config/com.gumatos.kit04.adapter.sr.cfg').write_text(adapter,encoding='utf-8')
        (profile/'config/com.gumatos.realmapi.cfg').write_text('[Safety]\nEnableHooks = false\n',encoding='utf-8')
        result['physical_click']=False
        result['preflight']=initial
        with (profile/'config/com.gumatos.aut4probe.cfg').open('a',encoding='utf-8') as f:
            f.write('RstvCiclo = true\nRstvSkillNome = Fireball\n')
        with (profile/'config/com.gumatos.kit04.adapter.sr.cfg').open('a',encoding='utf-8') as f:
            f.write('\n[Controle]\nhabilitado = true\niniciarObservando = false\n\n[AutoAvaliacao]\nhabilitado = true\nidiomaIngles = true\n')
        result['input_kind']='internal kit action in existing PlayerLoop; no synthetic keyboard/mouse'
        result['auto_case']=case
        result['auto_complete']=False
    ns={'__name__':'__main__','ROOT':repo,'OUT':target/'boot01','OLD':inputs,
        'EXPECTED':ident['files']['AUT4Probe.dll'],
        'SESSION':'KITAUTO-'+case+'-'+__import__('datetime').datetime.now().strftime('%Y%m%d-%H%M%S'),
        'require_cloud_off':support.require_cloud_off,'cloud_state':support.cloud_state,
        'setup_plugins':setup,'prepare_empty':support.prepare_empty,
        'baseline':support.baseline,'verify_baseline':support.verify_baseline,
        'SEM_PROBE':False,'NAV_TETO':'3600',
        'NAV_ROTA':'Play;Roguelike;Accept;@PartyCharacter;@PartyAccept;Accept;@HudInitialize',
        'NAV_ALVO':'=RstvRunSkillTreeButton'}
    state = {'pending':None,'seq':0,'done':False,'actions':[]}
    def live_step(pid, profile, session, result, ps, save):
        path = profile.parent/'recorder/controle-runtime.json'
        try: d = read(path)
        except (ValueError,OSError): return
        e = d.get('engine',{})
        if e.get('pid')!=pid or e.get('sessao')!=session or e.get('adapter_sha256')!=ident['files']['KIT04Adapter.SR.dll']:
            raise RuntimeError('Live identity mismatch')
        if abs(time.time()*1000-e.get('utc_unix_ms',0))>5000:
            raise RuntimeError('Stale live engine heartbeat')
        if state['pending'] is not None:
            matches = [x for x in d.get('comandos_auto',[]) if x['seq']==state['pending']]
            if not matches: return
            response=matches[0]
            save('auto-response-'+str(state['pending'])+'.json',response)
            if not response.get('evento'): raise RuntimeError('Kit refused internal action: '+str(response))
            state['actions'].append(response['acao']); state['pending']=None
        if state['done']: return
        ctx=d.get('contexto',{})
        safe=ctx.get('foco_no_jogo') is True and all(ctx.get(k) is False for k in ('chat_aberto','digitando','remapeando'))
        if not safe: return # no focus forcing and no fabricated guard flags
        if 'observar' not in state['actions']:
            action='observar'; description='KIT-AUTO collection start'
        else:
            try: probe=read(profile.parent.parent/'probe/aut4probe.json')
            except (ValueError,OSError): return
            if (probe.get('rstv_coleta') or {}).get('status')!='CONCLUIDO': return
            skill=probe.get('rstv_skill_viva') or {}
            if not skill.get('guid'): raise RuntimeError('Actual skill identity absent')
            description='checkpoint asset '+skill['nome']+' '+skill['guid']+' (tree already closed; not a live target mark)'
            if 'marcar_problema' not in state['actions']: action='marcar_problema'
            elif case=='no-export' or 'exportar' in state['actions']:
                state['done']=True; result['auto_complete']=True
                save('auto-live-final.json',d); return
            else: action='exportar'
        state['seq']+=1
        request='|'.join([session,str(state['seq']),action,description])
        dest=path.parent/'auto-command.txt'; tmp=dest.with_suffix('.tmp')
        tmp.write_text(request,encoding='utf-8'); tmp.replace(dest)
        state['pending']=state['seq']
        save('auto-request-'+str(state['seq'])+'.json',{'request':request,'engine_before':e,'case':case})
    ns['live_step']=live_step; ns['auto_state']=state
    source=(HERE/'bench_template.py').read_text(encoding='utf-8')
    ast.parse(source); (target/'expanded.py').write_text(source,encoding='utf-8')
    exec(compile(source,str(target/'expanded.py'),'exec'),ns)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=['run','boot','evaluate'])
    ap.add_argument('--repo',type=Path,default=Path('C:/dev/stolen-realm'))
    ap.add_argument('--out',type=Path,help='New directory; default run creates a timestamped evidence root')
    ap.add_argument('--case',choices=['positive','no-export'],default='positive')
    args=ap.parse_args(); args.repo=args.repo.resolve()
    if args.out is None:
        if args.command!='run': ap.error('--out is required for boot/evaluate')
        args.out=args.repo/'scratch/kit/KIT-AUTO'/('run-'+__import__('datetime').datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    args.out=args.out.resolve()
    if args.command=='boot': boot(args.repo,args.out,args.case); return 0
    evaluator=load('auto_evaluator',HERE/'evaluate.py')
    if args.command=='evaluate':
        r=evaluator.evaluate(args.out); print(json.dumps(r,ensure_ascii=True)); return r['exit']
    args.out.mkdir(parents=True,exist_ok=False)
    result={'schema':'KIT-AUTO/result/1','kit_verdict':'NOT_GRANTED','task_accepted':False,'cases':{}}
    try:
        result['preflight']=preflight(args.repo)
        build(args.repo,args.out)
        for case in ('positive','no-export'):
            call=cmd([sys.executable,str(Path(__file__).resolve()),'boot','--repo',str(args.repo),'--out',str(args.out),'--case',case],args.out,case,timeout=360)
            b=args.out/case/'recorder-on/boot01'
            report=evaluator.evaluate(b)
            write(args.out/(case+'-evaluation.json'),report)
            result['cases'][case]={'boot':str(b),'driver_exit':call['exit'],'evaluation':report}
            if call['exit']!=0: raise RuntimeError('Boot/cleanup failed: '+case)
            expected=0 if case=='positive' else 1
            if report['exit']!=expected: raise RuntimeError('Unexpected evaluation exit: '+case)
            if case=='no-export' and report['failures']!=['export_file_exists']:
                raise RuntimeError('Negative has collateral failures: '+str(report['failures']))
        result['evaluation_exercised']=True
        result['counterproof_exercised']=True
        result['exit']=0
    except Exception as e:
        result['exit']=2; result['error']=type(e).__name__+': '+str(e)
    write(args.out/'RESULTADO.json',result)
    print(json.dumps(result,ensure_ascii=True))
    return result['exit']

if __name__=='__main__': sys.exit(main())
