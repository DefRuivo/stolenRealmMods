"""BP-MODS offline evidence: actual table corpus and verbatim BT order code.
No game binary is loaded/patched. The CLR host is explicitly synthetic.
"""
from pathlib import Path
import hashlib,importlib.util,json,re

def prepare(repo,out):
    path=repo/'tools/tabelas.py'
    spec=importlib.util.spec_from_file_location('bpmods_tables',path)
    table=importlib.util.module_from_spec(spec);spec.loader.exec_module(table)
    source=repo/'BetterTooltips/Patches/LocalizePatch.cs'
    text=source.read_text(encoding='utf-8-sig')
    rows=[];counts={}
    for name in ['TextAppends','TextFixes']:
        block,pos=table.bloco(text,name)
        entries=list(table.entradas(block,text[:pos].count('\n')+1));counts[name]=len(entries)
        for line,comment,key,value in entries:
            # These are ordinary C# strings; their escape grammar is compatible here.
            value=json.loads('"'+value+'"')
            for note in re.findall(r'<color=#C8B090>(.*?)</color>',value,re.S):
                rows.append(dict(table=name,line=line,note=note))
    assert counts['TextAppends']>=190 and counts['TextFixes']>=100 and len(rows)>200
    corpus=out/'mod-corpus.json';corpus.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    # Contiguous, verbatim methods, not a Python reimplementation of their behavior.
    start=text.index('            private static void Prefix(ref string description)')
    end=text.index('\n        }\n        /// <summary>\n        /// NIVEL 2',start)
    snippet=text[start:end]
    assert 'private static int InicioDoSeparador' in snippet and snippet.rstrip().endswith('}')
    generated=out/'BTOrder.generated.cs'
    generated.write_text('using System;\nusing System.Collections.Generic;\npublic static partial class BTOrder\n{\n'+snippet+'\n}\n',encoding='utf-8')
    report=dict(source='BetterTooltips/Patches/LocalizePatch.cs',sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),verbatimStartLine=text[:start].count('\n')+1,verbatimEndLine=text[:end].count('\n')+1,verbatimSha256=hashlib.sha256(snippet.encode()).hexdigest(),tableCounts=counts,coloredNoteOccurrences=len(rows),uniqueNotes=len({r['note'] for r in rows}))
    (out/'bt-source-provenance.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return corpus,generated

def execute(repo,here,out,deps,probe,csc,framework,run,generated):
    command=['dotnet',csc,'-nologo','-noconfig','-nostdlib+','-langversion:10','-target:exe',f'-out:{probe/"ModsHarmonyProbe.exe"}']
    command += [f'-r:{framework/name}' for name in ['mscorlib.dll','System.dll','System.Core.dll']]
    command += [f'-r:{deps/"0Harmony.dll"}',here/'ModsHarmonyProbe.cs',here/'StubTypes.cs',repo/'BetterPortuguese/Runtime/Bindings.cs',repo/'BetterPortuguese/Runtime/BetterTooltipsAdapter.cs',generated]
    command += sorted((repo/'BetterPortuguese/Core').glob('*.cs'))
    run(command,out/'build-mods-clr.log')
    return run([probe/'ModsHarmonyProbe.exe',repo/'BetterPortuguese/Data/pt-BR.mods.json'],out/'mods-harmony-tests.log')
