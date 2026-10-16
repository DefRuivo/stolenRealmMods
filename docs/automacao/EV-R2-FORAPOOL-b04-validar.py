from pathlib import Path
import argparse,json,re,hashlib,subprocess,copy,unittest,io,sys,collections
P='EV-R2-FORAPOOL-b04-'
BASE=Path(__file__).resolve().parent
DOC=BASE/'docs/automacao' if (BASE/'docs/automacao').exists() else BASE
R=BASE/'fontes' if (BASE/'fontes').exists() else Path('C:/dev/stolen-realm/docs/cobertura/EV-R1')
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ptr(obj,path):
 for bit in path.strip('/').split('/'):
  obj=obj[int(bit)] if isinstance(obj,list) else obj[bit.replace('~1','/').replace('~0','~')]
 return obj
def flat(obj):
 stack=[('',obj)]
 while stack:
  p,v=stack.pop(); yield p,v
  if isinstance(v,dict): stack.extend((p+'/'+k.replace('~','~0').replace('/','~1'),q) for k,q in v.items())
  elif isinstance(v,list): stack.extend((p+'/'+str(i),q) for i,q in enumerate(v))
def tokens(text): return collections.Counter(re.findall(r'\[[^\]]+\]|\{[^{}]+\}|<[^>]+>',text))
REPORT=load(DOC/(P+'propostas-auditadas.json'))
SOURCE=load(R/'eventos.json')
SOURCES={e['chave']:e for e in SOURCE['eventos']}
SECTIONS=re.split(r'(?m)^## ',(R/'lote-NotInEventPool-v2.md').read_text(encoding='utf-8'))[1:]
KEYS=[re.search(r'resources.assets:[0-9]+',s).group() for s in SECTIONS[63:84]]
CAT_BYTES=(R/'catalogo-referencias.json').read_bytes() if (R/'catalogo-referencias.json').exists() else subprocess.check_output(['git','-C','C:/dev/stolen-realm','show','097f950:docs/cobertura/EV-R1/catalogo-referencias.json'])
CAT=json.loads(CAT_BYTES)
SNAP=load(DOC/(P+'fontes-eventos.json'))
REFS=load(DOC/(P+'referencias-auditadas.json'))
def validate(report):
 assert len(report['eventos'])==21
 assert [x['chave'] for x in report['eventos']]==KEYS
 assert [x['numero'] for x in report['eventos']]==list(range(64,85))
 for x in report['eventos']:
  e=SOURCES[x['chave']]
  for field in ['titulo','categoria','raridade','peso','nome_asset','origem','condicoes','modos','historia','full_release']:
   assert x[field]==e[field],(x['numero'],field)
  assert x['guid']==e['id']
  assert x['aprovacao']=='PENDENTE'
  assert x['recompensa']==x['condicao']=='MANTER'
  assert x['veredito_proposto']==('MELHORAR' if x['propostas'] else 'MANTER')
  seen=set()
  for ch in x['propostas']:
   p=ch['campo']; assert p not in seen; seen.add(p)
   assert re.fullmatch(r'/(texto|texto_resultados_possiveis)|/campos_originais/promptToSelectCharacter|/opcoes/\d+/(titulo|texto)|/opcoes/\d+/efeitos/\d+/texto',p),p
   assert ch['antes']==ptr(e,p)
   assert ch['antes'] and ch['proposta']!=ch['antes']
   assert tokens(ch['antes'])==tokens(ch['proposta']), (x['numero'],p,'tokens')
   intermediate=ch['antes']
   for sub in ch['substituicoes']:
    assert intermediate.count(sub['antes'])==1
    intermediate=intermediate.replace(sub['antes'],sub['depois'],1)
   assert intermediate==ch['proposta']
   assert ch['justificativas'] and all(ch['justificativas'])
  for t in x['textos_auditados']: assert t['atual']==ptr(e,t['campo'])
  expected={p for p,v in flat(e) if v is None}
  assert expected=={v['campo'] for v in x['nulls']}
  for v in x['nulls']:
   assert ptr(e,v['campo']) is None
   assert ptr(e,v['campo'].rsplit('/',1)[0])['motivo']==v['motivo']
   assert v['tipo'] in ['NAO_EXERCITADO','REFERENCIA_NULA_ASSET']
  for o,orig in zip(x['configuracao'],e['opcoes'],strict=True):
   assert o['titulo']==orig['titulo'] and o['condicoes']==orig['condicoes'] and o['rolagem']==orig['rolagem']
   assert o['hideOptionEffectText']==orig['campos_originais']['hideOptionEffectText']
   for a,oa in zip(o['acoes'],orig['efeitos'],strict=True):
    assert a=={k:([{q:v for q,v in eff.items() if q!='campos_originais'} for eff in oa[k]] if k=='efeitos' else oa[k]) for k in a}
 return True
class Checks(unittest.TestCase):
 def test_01_scope_order_unique(self):
  self.assertEqual(len(SECTIONS),84); self.assertEqual(len(set(KEYS)),21); self.assertEqual([x['chave'] for x in REPORT['eventos']],KEYS)
 def test_02_full_contract(self): self.assertTrue(validate(REPORT))
 def test_03_snapshot_exact(self): self.assertEqual(SNAP['eventos'],[SOURCES[k] for k in KEYS])
 def test_04_sources_unchanged(self):
  for p,desc in REPORT['fontes'].items():
   if p.startswith('C:'): self.assertEqual(sha(R/Path(p).name),desc['sha256'])
 def test_05_catalog_exact_provenance(self):
  f=REPORT['fontes']['git:097f950:docs/cobertura/EV-R1/catalogo-referencias.json']
  self.assertEqual(hashlib.sha256(CAT_BYTES).hexdigest(),f['sha256']); self.assertEqual(len(CAT['registros']),2399); self.assertEqual(len(CAT['resumos']),3214)
 def test_06_historical_crlf_only(self):
  b=(R/'eventos-git097f950.json').read_bytes() if (R/'eventos-git097f950.json').exists() else subprocess.check_output(['git','-C','C:/dev/stolen-realm','show','097f950:docs/cobertura/EV-R1/eventos.json'])
  self.assertEqual(json.loads(b),SOURCE); self.assertEqual(b.replace(b'\r\n',b'\n'),(R/'eventos.json').read_bytes().replace(b'\r\n',b'\n'))
 def test_07_literal_before_original_mirrors(self):
  for x in REPORT['eventos']:
   e=SOURCES[x['chave']]
   for ch in x['propostas']:
    p=ch['campo']; before=ch['antes']
    if p=='/texto': raw=e['campos_originais']['encounterText']
    elif p=='/texto_resultados_possiveis': raw=e['campos_originais']['encounterPossibleResultsText']
    elif p.startswith('/campos_originais/'): raw=ptr(e,p)
    else:
     parts=p.split('/'); o=e['opcoes'][int(parts[2])]
     raw=o['campos_originais']['title' if parts[-1]=='titulo' else 'description'] if len(parts)==4 else o['efeitos'][int(parts[4])]['campos_originais']['activationText']
    self.assertEqual(before,raw)
 def test_08_proposals_in_markdown(self):
  for x in REPORT['eventos']:
   part=2 if x['numero']<=70 else 3 if x['numero']<=77 else 4
   text=(DOC/(P+f'parte{part:02d}.md')).read_text(encoding='utf-8')
   for ch in x['propostas']:
    self.assertIn(json.dumps(ch['antes'],ensure_ascii=False,indent=2),text); self.assertIn(json.dumps(ch['proposta'],ensure_ascii=False,indent=2),text)
 def test_09_metadata_inventories(self):
  initial=(DOC/(P+'parte01.md')).read_text(encoding='utf-8'); final=(DOC/(P+'parte05.md')).read_text(encoding='utf-8')
  rows=[l.split('|') for l in initial.splitlines() if re.match(r'^\|\d+\|',l)]
  self.assertEqual(len(rows),21)
  for row,x in zip(rows,REPORT['eventos'],strict=True):
   e=SOURCES[x['chave']]; self.assertEqual(int(row[1]),x['numero']); self.assertEqual(row[2],e['chave']); self.assertEqual(row[3],e['titulo']); self.assertEqual(row[4],e['categoria']); self.assertEqual(float(row[6]),e['peso']); self.assertEqual(int(row[7]),e['condicoes']['disabled']); self.assertEqual(int(row[8]),len(e['opcoes']))
   self.assertIn('|'+str(x['numero'])+'|'+x['chave']+'|',final)
 def test_10_counts_independent(self):
  c=REPORT['contagens']; self.assertEqual(c['eventos'],21); self.assertEqual(c['MELHORAR_wording'],19); self.assertEqual(c['MANTER'],2)
  self.assertEqual(c['opcoes'],sum(len(SOURCES[k]['opcoes']) for k in KEYS)); self.assertEqual(c['acoes'],sum(len(o['efeitos']) for k in KEYS for o in SOURCES[k]['opcoes']))
  self.assertEqual(c['campos_propostos'],sum(len(x['propostas']) for x in REPORT['eventos'])); self.assertEqual(c['substituicoes'],sum(len(ch['substituicoes']) for x in REPORT['eventos'] for ch in x['propostas']))
 def test_11_null_counts_partition(self):
  nulls=[v for x in REPORT['eventos'] for v in x['nulls']]; c=REPORT['contagens']; self.assertEqual(len(nulls),336); self.assertEqual(c['nulls_runtime']+c['nulls_referencia'],len(nulls))
  self.assertEqual(c['nulls_com_motivo'],sum(sum(v is None for _,v in flat(SOURCES[k])) for k in KEYS))
 def test_12_no_rewards_or_conditions_changes(self):
  self.assertEqual(REPORT['contagens']['mudancas_recompensa'],0); self.assertEqual(REPORT['contagens']['mudancas_condicao'],0)
  self.assertTrue(all(x['recompensa']==x['condicao']=='MANTER' for x in REPORT['eventos']))
 def test_13_no_hidden_options_or_overrides(self):
  c=REPORT['contagens']; self.assertEqual(c['opcoes_ocultas_configuradas'],0); self.assertEqual(c['hideOptionEffectText_ativo'],0); self.assertEqual(c['overrides'],0)
 def test_14_three_no_options_epilogues(self):
  self.assertEqual([x['numero'] for x in REPORT['eventos'] if not x['configuracao']],[68,69,70])
 def test_15_disabled_variants_preserved(self):
  self.assertEqual([x['numero'] for x in REPORT['eventos'] if x['condicoes']['disabled']==1],[83,84]); self.assertEqual(REPORT['eventos'][20]['configuracao'][0]['acoes'][0]['evento_encadeado']['chave'],'resources.assets:2545783')
 def test_16_failure_loop_and_empty_effects(self):
  self.assertEqual(REPORT['eventos'][9]['configuracao'][0]['acoes'][1]['evento_encadeado']['chave'],'resources.assets:2545762'); self.assertEqual(REPORT['eventos'][10]['configuracao'][0]['acoes'][1]['efeitos'],[])
 def test_17_residual_battle_not_activation(self):
  a=REPORT['eventos'][17]['configuracao'][0]['acoes'][0]; self.assertFalse(a['batalha']['iniciar']); self.assertEqual(a['batalha']['override']['VictoryEvent']['m_PathID'],2545547)
 def test_18_catalog_snapshot_consistency(self):
  self.assertFalse(REFS['nao_resolvidas']); self.assertEqual(len(REFS['resumos']),51)
  for k,v in REFS['resumos'].items(): self.assertEqual(v,CAT['resumos'][k])
  for x in REPORT['eventos']:
   for ref in x['referencias_projetadas']: self.assertEqual(ref['nome'],CAT['resumos'][ref['chave']]['name'])
 def test_19_incoming_exact_independent_scan(self):
  actual={k:set() for k in KEYS}
  objs=[(e['chave'],'PartyEvent',e['campos_originais']) for e in SOURCE['eventos']]+[(e['file']+':'+str(e['path_id']),e['script'],e['data']) for e in CAT['registros']]
  for key,typ,obj in objs:
   for p,v in flat(obj):
    if isinstance(v,dict) and set(v)=={'m_FileID','m_PathID'} and v['m_FileID']==0 and v['m_PathID']:
     target='resources.assets:'+str(v['m_PathID'])
     if target in actual: actual[target].add((key,typ,p,target))
  for x in REPORT['eventos']:
   self.assertEqual(actual[x['chave']],{(v['origem'],v['tipo'],v['campo'],v['destino']) for v in x['referencias_entrantes']})
  self.assertEqual(sum(map(len,actual.values())),45)
 def test_20_empty_fields_and_pptr_counts(self):
  self.assertEqual(REPORT['contagens']['textos_vazios_auditados'],sum(t['atual']=='' for x in REPORT['eventos'] for t in x['textos_auditados']))
  self.assertEqual(REPORT['contagens']['pptr_nulos_literais'],sum(sum(isinstance(v,dict) and set(v)=={'m_FileID','m_PathID'} and v['m_PathID']==0 for _,v in flat(SOURCES[k])) for k in KEYS))
 def test_21_english_and_tokens_preserved(self):
  for x in REPORT['eventos']:
   for ch in x['propostas']: self.assertEqual(tokens(ch['antes']),tokens(ch['proposta']))
  for n in [83,84]:
   ch=next(x for x in REPORT['eventos'][n-64]['propostas'] if x['campo']=='/texto'); self.assertIn('</incr></b></gold>',ch['proposta'])
 def test_22_human_pending_limits(self):
  self.assertEqual(REPORT['contagens']['aprovacoes'],0)
  for part in range(1,6):
   text=(DOC/(P+f'parte{part:02d}.md')).read_text(encoding='utf-8'); self.assertIn('PENDENTE',text); self.assertIn('NAO_EXERCITADO',text)
 def test_23_negative_missing_event(self):
  d=copy.deepcopy(REPORT); d['eventos'].pop()
  with self.assertRaises(AssertionError): validate(d)
 def test_24_negative_fabricated_reward(self):
  d=copy.deepcopy(REPORT); d['eventos'][0]['configuracao'][0]['acoes'][0]['efeitos'][0]['recompensas']['ouro']['quantidade_final']=0
  with self.assertRaises(AssertionError): validate(d)
 def test_25_negative_wrong_literal_before(self):
  d=copy.deepcopy(REPORT); d['eventos'][0]['propostas'][0]['antes']='invented text'
  with self.assertRaises(AssertionError): validate(d)
 def test_26_negative_missing_placeholder(self):
  d=copy.deepcopy(REPORT)
  text=next(t for t in d['eventos'][2]['textos_auditados'] if t['campo']=='/campos_originais/characterSelectedText')
  self.assertIn('[name]',text['atual']); text['atual']=text['atual'].replace('[name]','')
  with self.assertRaises(AssertionError): validate(d)
 def test_27_negative_reward_path_proposal(self):
  d=copy.deepcopy(REPORT); d['eventos'][0]['propostas'][0]['campo']='/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/razao'
  with self.assertRaises(AssertionError): validate(d)
 def test_28_negative_reordered_key(self):
  d=copy.deepcopy(REPORT); d['eventos'][0],d['eventos'][1]=d['eventos'][1],d['eventos'][0]
  with self.assertRaises(AssertionError): validate(d)
if __name__=='__main__':
 parser=argparse.ArgumentParser(); parser.add_argument('--evidence',default=P+'validacao.json'); args=parser.parse_args()
 stream=io.StringIO(); result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
 output=stream.getvalue(); print(output)
 ev={'testes_executados':result.testsRun,'falhas':len(result.failures),'erros':len(result.errors),'sucesso':result.wasSuccessful(),'saida_real':output,'schema_integral':'NAO_EXERCITADO: biblioteca jsonschema indisponível; apenas contrato/asserções documentais próprias','runtime':'NAO_EXERCITADO: tarefa proíbe jogo','contagens_verificadas':REPORT['contagens'],'fontes_sha256':REPORT['fontes'],'documentos_sha256':{p.name:sha(p) for p in DOC.glob(P+'*') if p.suffix in ['.md','.json'] and 'validacao' not in p.name}}
 target=DOC/args.evidence
 with target.open('x',encoding='utf-8',newline='\n') as f: f.write(json.dumps(ev,ensure_ascii=False,indent=2)+'\n')
 print('EVIDENCE',str(target)); sys.exit(0 if result.wasSuccessful() else 1)
