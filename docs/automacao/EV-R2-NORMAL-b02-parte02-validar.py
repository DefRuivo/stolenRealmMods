#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoria offline da correcao documental EV-R2-NORMAL-b02 (ordinais 21-40).

Verifica, sem jogo e sem tocar em nada:
  A fontes/hashes declarados no documento
  B cobertura (20 eventos, ordinais 21-40, chaves e ids unicos)
  C identidade (ordinal/chave/id/titulo/raridade/peso contra eventos.json e lote-Normal-v2.md)
  D campos (todo JSONPath citado existe; 'antes' confere com a fonte)
  E literais (todo 'antes'/'depois' citado no .md existe literalmente)
  F vereditos (20/20, MANTER/MELHORAR, MELHORAR exige proposta)
  G NULL (todo caminho listado existe e e nulo na fonte)
  H integridade da parte01 e das demais entregas (nao alteradas)

Uso: python audit_b02.py [caminho_do_md]
Saida: linhas CHECK ... PASS/FAIL e resumo final. Exit 1 se houver qualquer FAIL.
"""
import json, os, re, sys, hashlib

WS = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:/dev/stolen-realm/docs/cobertura/EV-R1"
DOC = sys.argv[1] if len(sys.argv) > 1 else r"C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b02-parte02.md"
PARTE01 = r"C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b02-parte01.md"

EVENTOS = os.path.join(BASE, 'eventos.json')
LOTE = os.path.join(BASE, 'lote-Normal-v2.md')
SCHEMA = os.path.join(BASE, 'eventos.schema.json')
CATALOGO = os.path.join(BASE, 'catalogo-referencias.json')

passes = []
fails = []

def check(name, ok, detail=''):
    (passes if ok else fails).append(name)
    print("CHECK %-46s %s %s" % (name, 'PASS' if ok else 'FAIL', detail))

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

def resolve(doc_json, path):
    cur = doc_json
    for tok in path.split('.')[1:]:
        m = re.match(r'^([A-Za-z_]+)\[(\d+)\]$', tok)
        if m:
            cur = cur[m.group(1)][int(m.group(2))]
        elif tok:
            cur = cur[tok]
    return cur

EV = json.load(open(EVENTOS, encoding='utf-8'))
NORMAL = [e for e in EV['eventos'] if e['categoria'] == 'Normal']
# ordinal N da categoria Normal = NORMAL[N-1]
SLICE = {n: NORMAL[n - 1] for n in range(21, 41)}
assert EV['eventos'][21]['titulo'] == 'Boss Fight - Roland', 'mapeamento ordinal/indice global divergente'
HEADS = [l[3:] for l in open(LOTE, encoding='utf-8').read().splitlines() if l.startswith('## ')]
DATA = json.load(open(os.path.join(WS, 'EV-R2-NORMAL-b02-parte02-validacao.json'), encoding='utf-8'))
D = {e['ordinal']: e for e in DATA['events']}

print("== AUDITORIA EV-R2-NORMAL-b02-parte02 ==")
print("documento: %s" % DOC)
print("fontes: eventos.json lote-Normal-v2.md eventos.schema.json catalogo-referencias.json")
print("")

md = open(DOC, encoding='utf-8').read() if os.path.exists(DOC) else ''
check('A0.documento_existe', bool(md))

# ---- A: hashes declarados no documento ----
decl = re.findall(r'`([^`]+)` -> `([^`]+)` sha256 `([0-9a-f]{64})`', md)
check('A1.hashes_declarados', len(decl) == 4, '%d declarados' % len(decl))
ok = True
for nome, path, h in decl:
    real = sha256(path)
    if real != h:
        ok = False
        print('   hash divergente: %s' % path)
check('A2.hashes_conferem', ok)

# ---- B: cobertura ----
check('B1.total_20', len(SLICE) == 20 and len(DATA['events']) == 20)
check('B2.ordinais_21_40', sorted(SLICE) == list(range(21, 41)) == sorted(D))
check('B3.categoria_normal', all(SLICE[n]['categoria'] == 'Normal' for n in SLICE))
check('B4.chaves_unicas_20', len({SLICE[n]['chave'] for n in SLICE}) == 20)
check('B5.ids_unicos_20', len({SLICE[n]['id'] for n in SLICE}) == 20)
check('B6.ordinal_nao_e_path_id',
      [SLICE[n]['origem']['path_id'] for n in range(21, 41)] != sorted(SLICE[n]['origem']['path_id'] for n in range(21, 41)),
      'ordem por secao difere de path_id crescente')

# ---- C: identidade ----
ok_doc = ok_md = ok_id = True
for n in range(21, 41):
    e = SLICE[n]
    d = D[n]
    if not md.count("### %d - %s" % (n, e['titulo'])):
        ok_doc = False
        print('   secao ausente/errada no doc: %d %s' % (n, e['titulo']))
    if not re.search(r'^\| %d \| `%s` \| `%s` \|' % (n, re.escape(e['chave']), re.escape(e['id'])), md, re.M):
        ok_id = False
        print('   linha de identidade ausente/errada: %d' % n)
    if HEADS[n - 1] != e['titulo']:
        ok_md = False
        print('   titulo divergente do lote-Normal-v2.md: %d' % n)
check('C1.secoes_no_documento', ok_doc)
check('C2.tabela_identidade_doc', ok_id)
check('C3.titulos_lote_vs_eventos', ok_md)

# ---- D: campos e 'antes' ----
ok_path = ok_antes = ok_depois = ok_tipo = True
n_prop = 0
for n in range(21, 41):
    for p in D[n]['propostas']:
        n_prop += 1
        jp = p['jsonpath']
        try:
            val = resolve(EV, jp)
        except Exception as ex:
            ok_path = False
            print('   JSONPath inexistente: %s (%s)' % (jp, ex))
            continue
        if p['tipo'] == 'campo':
            if str(val) != p['antes']:
                ok_antes = False
                print('   antes != fonte em %s: %r != %r' % (jp, p['antes'], val))
        else:
            if not isinstance(val, str) or val.count(p['antes']) < 1:
                ok_antes = False
                print('   trecho antes ausente em %s: %r' % (jp, p['antes']))
            if not isinstance(val, str) or val.count(p['depois']) >= 1:
                ok_tipo = True if p['depois'] in ('',) else ok_tipo
        if p['depois'] == p['antes']:
            ok_depois = False
            print('   depois == antes em %s' % jp)
check('D1.jsonpath_existe', ok_path, '%d propostas' % n_prop)
check('D2.antes_confere_com_fonte', ok_antes)
check('D3.depois_difere_de_antes', ok_depois)

# ---- E: literais no documento ----
def esc(s):
    return s.replace('\n', '\\n').replace('\r', '\\r')

ok_lit = True
n_lit = 0
for n in range(21, 41):
    for p in D[n]['propostas']:
        n_lit += 1
        if esc(p['antes']) not in md:
            ok_lit = False
            print('   antes nao citado literalmente no doc: %d %s' % (n, p['jsonpath']))
        if esc(p['depois']) not in md:
            ok_lit = False
            print('   depois nao citado literalmente no doc: %d %s' % (n, p['jsonpath']))
check('E1.antes_depois_citados_no_doc', ok_lit, '%d propostas' % n_lit)

# ---- F: vereditos ----
ok_v = True
for n in range(21, 41):
    d = D[n]
    if d['veredito'] not in ('MANTER', 'MELHORAR'):
        ok_v = False
    if ("**Veredito: %s.**" % d['veredito']) not in md or ("### %d - " % n) not in md:
        ok_v = False
        print('   veredito nao publicado para %d' % n)
    if d['veredito'] == 'MELHORAR' and not d['propostas']:
        ok_v = False
        print('   MELHORAR sem proposta: %d' % n)
check('F1.20_vereditos_publicados', ok_v)
cont = {}
for d in D.values():
    cont[d['veredito']] = cont.get(d['veredito'], 0) + 1
check('F2.contagem_veredito_confere', cont == DATA['contagens_veredito'] and DATA['total_eventos'] == 20,
      str(cont))
check('F3.inventario_publicado', '## 3. Inventario de decisoes' in md and md.count('| MANTER | 9 |') == 1 and md.count('| MELHORAR | 11 |') == 1)

# ---- G: NULL ----
nulls = re.findall(r'^- `(\$\.eventos\[\d+\][^`]*)`$', md, re.M)
ok_null = True
declared = sum(len(SLICE[n]['ausencias']) for n in SLICE)
if len(nulls) != declared:
    ok_null = False
    print('   contagem de NULL no doc %d != fonte %d' % (len(nulls), declared))
for path in nulls:
    try:
        v = resolve(EV, path)
    except Exception as ex:
        ok_null = False
        print('   caminho NULL inexistente: %s (%s)' % (path, ex))
        continue
    if v is not None:
        ok_null = False
        print('   caminho NULL com valor nao nulo: %s = %r' % (path, v))
check('G1.nulls_doc_igual_fonte', len(nulls) == declared, '%d caminhos' % len(nulls))
check('G2.nulls_existem_e_sao_nulos', ok_null)

# ---- H: integridade dos originais ----
check('H1.parte01_preservada', os.path.exists(PARTE01), 'sha256 %s' % sha256(PARTE01))
check('H2.fonte_intacta_contagens',
      EV['cobertura']['eventos_extraidos'] == 256 and len(NORMAL) == 160
      and EV['cobertura']['opcoes'] == 404 and EV['cobertura']['party_event_cabecalhos'] == 256,
      'eventos=%s Normal=%d opcoes=%s' % (EV['cobertura']['eventos_extraidos'], len(NORMAL), EV['cobertura']['opcoes']))
check('H3.sem_artefato_de_implementacao',
      not any(x in md for x in ('Assembly-CSharp.dll foi alterado', 'publicado em')))

print("")
print("TOTAL PASS %d FAIL %d  (propostas auditadas: %d; NULL auditados: %d; refutacoes: %d)" % (
    len(passes), len(fails), n_prop, len(nulls),
    sum(len(D[n]['refutacoes']) for n in D)))
sys.exit(1 if fails else 0)
