"""Fail-closed consumer of REAL KIT-AUTO exports and Debugger logs.
Exit 0: bounded export criterion only; 1: assertions failed; 2: unusable evidence.
This never grants KIT-14/14R/human/release acceptance.
"""
from pathlib import Path
import hashlib, json, re

def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def manifest(root):
    root=Path(root)
    if not root.is_dir() or root.is_junction() or root.is_symlink(): raise ValueError('Invalid restored root')
    result={}
    for p in root.rglob('*'):
        if p.is_junction() or p.is_symlink(): raise ValueError('Reparse point in restored tree')
        if p.is_file(): result[p.relative_to(root).as_posix()]=[p.stat().st_size,sha(p)]
    return result

def evaluate(boot):
    boot=Path(boot); checks=[]; report={'schema':'KIT-AUTO/evaluation/1','criterion':'export_evidence',
        'scope':'Internal action dispatch/export with independent Debugger asset identity; no physical input or kit verdict',
        'kit_verdict':'NOT_GRANTED','runtime_proof':False,'checks':checks,'boot':str(boot)}
    def check(name,condition,detail=None):
        checks.append({'id':name,'ok':bool(condition),'detail':detail})
    try:
        result=read(boot/'result.json'); ident=read(boot.parent/'inputs.json')
        control=read(boot/'preserved/recorder/controle-runtime.json')
        probe=read(boot/'probe/aut4probe.json')
        bepinex_log=(boot/'preserved/LogOutput-isolado.txt').read_text(encoding='utf-8-sig',errors='replace')
        # BepInEx may close its disk listener before quitting handlers; Unity retains the footer.
        log=(boot/'preserved/Player.log').read_text(encoding='utf-8-sig',errors='replace')
        check('logs_same_debugger_boot',len([x for x in bepinex_log.splitlines() if '[Proveniencia] DBG-PROV-V1 inicio |' in x])==1 and all(x in log for x in bepinex_log.splitlines() if '[Proveniencia] DBG-PROV-V1 inicio |' in x))
        session=result['sessao']; engine=control['engine']; pid=result.get('created_pid')
        report.update(session=session,pid=pid,adapter_sha256=engine.get('adapter_sha256'))
        check('driver_completed',result.get('auto_complete') is True and not any(result.get(k) for k in ('error','cleanup_error','cleanup_errors')))
        check('game_closed',result.get('game_closed') is True and result.get('final_state',{}).get('game_processes')==[])
        final=result.get('final_state',{})
        check('isolation_clean',all(final.get(k) is False for k in ('production_junction','production_backup_exists','isolated_profile_exists')) and result.get('own_lock_released') is True and not (boot/'dados-iso').exists())
        check('owner_baseline_unchanged',bool(result.get('immediate_baseline_after')) and all(x.get('equal') is True for x in result['immediate_baseline_after'].values()))
        # Readback is the RUN-TIME recorded re-hash of the restored trees (baseline-after.json),
        # not a live re-hash: the owner's saves are mutable state, so re-hashing them here would
        # turn "owner played later" into a kit failure and make replay of this evidence impossible.
        private=read(boot/'private-baseline.json'); after=read(boot/'baseline-after.json')
        restoration={k:{'count':len(private[k]['files']),'before':v.get('before'),'after':v.get('after'),
            'equal':v.get('equal') is True and not any(v.get(x) for x in ('new','removed','changed'))
                    and v.get('before')==len(private[k]['files'])==v.get('after')}
            for k,v in after.items() if k in private}
        restore_log=(boot/'dados-restaurar.stderr.log').read_text(encoding='utf-8-sig',errors='replace')
        check('owner_readback_unchanged',set(restoration)==set(private) and bool(restoration)
            and all(v['equal'] for v in restoration.values())
            and result.get('immediate_baseline_after')==after
            and 'RESTAURAR: OK' in restore_log and 'BYTE A BYTE identico' in restore_log,restoration)
        check('playerprefs_restored',result.get('playerprefs_export_equal') is True)
        check('cloud_off_preserved',result['cloud_start']['app_cloudenabled']==['0']==final['cloud']['app_cloudenabled'])
        check('input_hashes',all(sha(boot.parent/'inputs'/n)==h for n,h in ident['files'].items()))
        check('engine_identity',engine.get('pid')==pid and pid is not None and engine.get('sessao')==session and engine.get('adapter_sha256')==ident['files']['KIT04Adapter.SR.dll'])
        check('probe_identity',probe.get('sessao')==session and probe.get('hash_fonte')==ident['files']['AUT4Probe.dll'])
        check('no_keyboard_claim',control.get('leituras_teclado')==[] and result.get('physical_click') is False and (probe.get('rstv_coleta') or {}).get('physical_input') is False)
        check('auto_optin',control.get('auto_habilitado') is True)
        commands=control.get('comandos_auto',[])
        check('guarded_dispatch',len(commands)>=2 and all(x.get('origem')=='KIT-AUTO/acao-interna/1' and x.get('evento') and x['contexto'].get('foco_no_jogo') is True and all(x['contexto'].get(k) is False for k in ('chat_aberto','digitando','remapeando')) and x['engine'].get('pid')==pid and x['engine'].get('sessao')==session for x in commands))
        # Independent oracle: actual Debugger log, same game assembly and installed DLL.
        starts=[line for line in log.splitlines() if '[Proveniencia] DBG-PROV-V1 inicio |' in line]
        ends=[line for line in log.splitlines() if '[Proveniencia] DBG-PROV-V1 fim |' in line]
        states=[line for line in log.splitlines() if '[Proveniencia] DBG-PROV-V1 estado |' in line]
        check('debugger_session_complete',len(starts)==len(ends)==len(states)==1 and 'estadoDump=FECHADO' in ends[0] and 'estadoDump=ABERTO' in states[0], {'start_count':len(starts),'end_count':len(ends),'state_count':len(states)})
        start=starts[0] if starts else ''
        check('debugger_build_matches','sha256Dll='+ident['files']['RoguelikeDebugger.dll'] in start and 'sha256Alvo='+ident['game_sha256'] in start)
        skill=probe.get('rstv_skill_viva') or {}
        oracle=[line for line in log.splitlines() if "[Skill] '"+str(skill.get('nome'))+"' |" in line and 'skid='+str(skill.get('guid')) in line]
        check('debugger_skill_matches_live_target',bool(skill.get('guid')) and len(oracle)==1,oracle)
        report['oracle']={'kind':'Debugger boot asset inventory, NOT loot/exp battle nor HUD visibility','skill':skill,'lines':oracle,'provenance':starts+states+ends}
        collected=probe.get('rstv_coleta') or {}
        check('post_render_collection_complete',collected.get('status')=='CONCLUIDO' and collected.get('same_character_reference') is True)
        events={x['event']:x['frame'] for x in collected.get('events',[])}
        check('post_render_frame_order',events.get('tooltip_observed',-1)>events.get('hover_handler',-1)>=0 and events.get('open_observed',-1)>events.get('before_open',-1)>=0)
        exports=list((boot/'preserved/recorder/exports').glob('*.json'))
        check('export_file_exists',len(exports)==1,{'count':len(exports)})
        # If absent, that one missing signal is the actual negative; never invent a document.
        if exports:
            doc=read(exports[0]); mark=doc.get('marcacoes',[]); exp=[x for x in commands if x['acao']=='exportar']
            check('one_export_dispatch',len(exp)==1 and exp[0]['evento'].get('acao')=='exportar')
            check('export_schema',doc.get('esquema')=='KIT-07/export/1' and doc.get('runtime_exercitado') is True and doc.get('modo')=='passivo')
            check('export_session',doc.get('sessao')==session and doc.get('correlacao',{}).get('sessao_controle')==session==doc.get('correlacao',{}).get('sessao_coleta'))
            eng=doc.get('contexto',{}).get('engine',{})
            check('export_engine',eng.get('pid')==pid and eng.get('sessao')==session and eng.get('adapter_sha256')==engine['adapter_sha256'] and eng.get('frame')==exp[0]['engine'].get('frame'))
            check('checkpoint_mark_retained',len(mark)==1 and mark[0].get('sessao')==session and skill.get('guid','MISSING') in mark[0].get('descricao',''))
            check('same_retained_marks',mark==control.get('marcacoes'))
            check('pipeline_linked',doc.get('coleta',{}).get('pipeline_ligado') is True)
            check('export_no_side_effect_claim',doc.get('consome_input') is False and doc.get('foco_forcado')==0 and doc.get('encerrou_sessao') is False)
            report['export']={'path':str(exports[0]),'sha256':sha(exports[0]),'bytes':exports[0].stat().st_size,'engine_frame':eng.get('frame'),'mark_count':len(mark),'mark_window':mark[0].get('janela') if mark else None,'note':'checkpoint after close, not proof of marking the live target'}
        report['failures']=[c['id'] for c in checks if not c['ok']]
        report['exit']=1 if report['failures'] else 0
        report['runtime_proof']=report['exit']==0
    except (OSError,ValueError,KeyError,TypeError,IndexError) as e:
        report['exit']=2; report['error']=type(e).__name__+': '+str(e)
        report['failures']=[c['id'] for c in checks if not c['ok']]+['evidence_unusable']
    return report
