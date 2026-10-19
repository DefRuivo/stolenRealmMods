"""Flatten only already exercised bench text; never execute historical modules."""
from pathlib import Path
import ast, json
W=Path(__file__).resolve().parent
R=Path('C:/dev/stolen-realm')
s=(W/'run02/positive/recorder-on/expanded.py').read_text(encoding='utf-8')
tree=ast.parse(s); lines=s.splitlines(keepends=True)
for node in reversed(tree.body):
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'ROOT','OUT','OLD','EXPECTED','SESSION'} for t in node.targets):
        del lines[node.lineno-1:node.end_lineno]
s=''.join(lines);s=s[s.index('from pathlib'):]
s='"""KIT-AUTO bench: native handlers on disposable party; no OS input.\nFlattened from the exercised KIT16/F3/F5 recipe. Never import this template.\nROOT/OUT/OLD/EXPECTED/SESSION and callbacks are supplied by runner.py.\n"""\n'+s
s=s.replace("WORKER_ID='KITAUTO-positive'",'WORKER_ID=SESSION')
ast.parse(s)
(W/'bench_template.py').write_text(s,encoding='utf-8')
head='''"""KIT-AUTO support, extracted from exercised KIT16 recipe.
No imports of historical workspaces. Cloud is read-only; baseline is immediate.
"""
from pathlib import Path
from datetime import datetime
import hashlib, json, re, shutil
REAL = Path.home() / 'AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm'
DONO = Path.home() / 'AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx'
OTHER = Path.home() / 'AppData/Local/Abyssus/Saved/SaveGames'
STEAM_USER = Path('C:/Program Files (x86)/Steam/userdata/37602317')
def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()
'''
extracts=[('scratch/kit/KIT-14-run916/upstream911/roda911.py',{'manifest','compare','baseline','verify_baseline'}),('scratch/kit/KIT-14-run704/suporte.py',{'app_blocks','cloud_state','require_cloud_off'}),('scratch/kit/KIT-14-run704/coleta.py',{'prepare_empty'})]
for rel,names in extracts:
    src=(R/rel).read_text(encoding='utf-8')
    head+='\n\n'+'\n\n'.join(ast.get_source_segment(src,n) for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name in names)+'\n'
ast.parse(head)
(W/'bench_support.py').write_text(head,encoding='utf-8')
orig=json.loads((R/'scratch/kit/KIT-14F5/cases/on7/recorder-on/inputs.json').read_text())
keep=['AUT4Probe.dll','AUT4ProbePlugin.cs','KIT04Core.dll','CorePlugin.cs','RoguelikeSkillTreeVisualizer.dll','RealmApi.dll','RealmApi.Core.dll','RealmApi.Hooks.dll','PartyDriver.cs','Json.cs','IdentidadeDoProbe.cs','LeituraAgregados.cs','RstvPostRender.cs']
frozen={k:orig['files'][k] for k in keep}
(W/'frozen-inputs.json').write_text(json.dumps({'schema':'KIT-AUTO/frozen-inputs/1','files':frozen,'origin':'Reviewed F5 consumer/F3 Core/RSTV0.3.3, measured locally; not latest release candidate'},indent=2),encoding='utf-8')
print('Created bench_template.py, bench_support.py, frozen-inputs.json')
