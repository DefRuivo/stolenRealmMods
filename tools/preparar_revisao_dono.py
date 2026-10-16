"""Material documental LANG-C4; nunca modifica os arquivos-fonte."""
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ATT = Path('C:/Users/Pichau/AppData/Local/hermes/kanban/attachments')
SOURCE = ATT / 't_2a6474ff/LANG-R1-entrega-final.zip'
PROPOSALS = ATT / 't_a1ccc2dd/LANG-C4-propostas-dados01.json'
PACKAGE = ATT / 't_a1ccc2dd/LANG-C4-propostas-entrega01.zip'
OUT = ROOT / 'docs/automacao/LANG-C4-REVISAO-DONO.md'
RECEIPT = ROOT / 'docs/automacao/LANG-C4-REVISAO-DONO-verificacao.json'
EXPECTED_SOURCE_HASH = '4d509f13280cd9e210593cfce08420dd8e48a75b4261f9faefee2e6afb6bf161'
EXPECTED_PACKAGE_HASH = '3d9baa58073f5a1928e4533cde48479644969654885c28b46b24c5531038f6a6'
CODES = {'tags_quebradas', 'tags_divergentes'}
INPUTS = [SOURCE, PROPOSALS, PACKAGE]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def q(value):
    return json.dumps(value, ensure_ascii=False)


raw = {str(p): p.read_bytes() for p in INPUTS}
initial_hashes = {p: sha(data) for p, data in raw.items()}
proposal = json.loads(raw[str(PROPOSALS)].decode('utf-8-sig'))
with zipfile.ZipFile(io.BytesIO(raw[str(SOURCE)])) as z:
    members = {name: z.read(name) for name in (
        'entrega02/localizacao-ptbr.json',
        'entrega02/revisao-formatacao.csv',
        'entrega02/suspeitos.json',
    )}
source = json.loads(members['entrega02/localizacao-ptbr.json'])
records = {r['id']: (index, r) for index, r in enumerate(source['registros'])}
suspects = json.loads(members['entrega02/suspeitos.json'])
alerts = [a for a in suspects['ocorrencias'] if a['codigo'] in CODES]
# StringIO newline='' evita normalizar os CR/LF contidos nas células do CSV.
rows = list(csv.DictReader(io.StringIO(members['entrega02/revisao-formatacao.csv'].decode('utf-8-sig'), newline=''), delimiter=';'))
items = proposal['items']
changes = [x for x in items if x['veredito_proposto'] == 'CORRIGIR']
keeps = [x for x in items if x['veredito_proposto'] == 'MANTER']
by_id = {x['id']: x for x in items}


def risk(x):
    if x['id'] == 'LANG-00914':
        return (0, x['id'])
    if x['id'] == 'LANG-07329':
        return (1, x['id'])
    if x['id'] == 'LANG-00766' or '<rainb>' in x['chave']:
        return (2, x['id'])
    return (3, x['id'])


tag_changes = sorted([x for x in changes if x['natureza'] == 'tag'], key=risk)
format_changes = sorted([x for x in changes if x['natureza'] != 'tag'], key=lambda x: x['id'])
ordered = tag_changes + format_changes


def reason(x):
    id_ = x['id']
    if id_ == 'LANG-00914':
        return 'Trocar o delimitador de nome que parece uma tag por gold/incr/b da origem, sem alterar nenhuma palavra, vírgula ou quebra.'
    if id_ == 'LANG-00404':
        return 'Restaurar somente o negrito de Dano; o fechamento cruzado </i></color> herdado fica intacto, fora desta proposta.'
    if id_ == 'LANG-00713':
        return 'Restaurar itálico e cinza na primeira frase, fechando apenas as tags novas em ordem inversa; preservar a redação e as quebras.'
    if '<rainb>' in x['chave']:
        return 'Restaurar rainb como na origem, inclusive a presença ou ausência de fechamento; não reescrever a tradução.'
    if id_ == 'LANG-07575':
        return 'Acrescentar uma única quebra antes de Entre os seus espólios roubados, separando o parágrafo sobre o diário.'
    return x['justificativa']


def consequence(x):
    id_ = x['id']
    if id_ == 'LANG-00914':
        return 'Tag: permanece a aparente tag <Sully Walker, a mestra caçadora>, sem gold/incr/b; há risco de interpretação indevida do nome e perda do destaque. Não foi demonstrado sumiço em tela; restaurar incr pode aumentar a ocupação horizontal.'
    if id_ == 'LANG-07329':
        return 'Layout/estilo: a assinatura continua sem size=15 da origem. Não foi demonstrado estouro; a proposta também pode mudar legibilidade/altura e requer verificação visual posterior.'
    if id_ == 'LANG-00766':
        return 'Tag/estilo: permanece ausente shake; a marca do efeito da origem não chega ao texto pt-BR. Efeito em tela não exercitado, sem quebra de frase ou variável documentada.'
    if '<rainb>' in x['chave']:
        return 'Tag/estilo: permanece ausente rainb em relação à origem. O efeito visual é apenas esperado, não confirmado; não há quebra de sentido ou variável demonstrada.'
    if id_ in {'LANG-00497', 'LANG-00504'}:
        return 'Tag/estilo: o rótulo continua sem a cor #CBB396 da origem; o valor permanece igual. Não há perda de variável demonstrada nem estouro de layout comprovado.'
    if id_ == 'LANG-00404':
        return 'Tag/estilo: Dano continua sem o negrito da origem; nada prova quebra funcional. O alerta herdado de </i></color> não é corrigido por esta mudança.'
    if id_ == 'LANG-00713':
        return 'Tag/estilo: a primeira frase continua sem itálico/cinza da origem; não há erro de sentido ou quebra de frase demonstrados.'
    if id_ == 'LANG-07575':
        return 'Formatação: o início do diário segue separado apenas por uma quebra, não uma linha em branco. Não há perda de palavras; a proposta acrescenta altura e pode afetar a janela, sem medição visual.'
    raise AssertionError(id_)


def render():
    lines = [
        '# LANG-C4 — revisão do dono: só o que muda', '',
        '## Resumo executivo', '',
        f'- Mudam: {len(changes)} IDs — {len(tag_changes)} de tag e {len(format_changes)} de formatação. MANTER: {len(keeps)}.',
        '- Variável: 0 propostas. Sentido: 0 propostas. Não há grupos artificiais nem correções linguísticas acrescentadas a este lote.',
        f'- Universo conferido: {len(items)} IDs únicos / {len(alerts)} alertas; 59 tags_quebradas + 26 tags_divergentes, com sobreposição de 2 IDs. Alertas não são a quantidade de mudanças.',
        '- Maior impacto: LANG-00914 (Sully Walker), que substitui uma aparente tag de nome por gold/incr/b. Depois: LANG-07329 (tamanho da assinatura), oito restaurações rainb e uma shake. LANG-07575 acrescenta uma quebra de parágrafo e exige atenção à altura.',
        '- Ordem de leitura: tags por risco/impacto (Sully primeiro, tamanho, efeitos, demais destaques); em seguida formatação. Dentro de cada patamar, ID crescente. Os riscos são documentais/esperados, não resultados de teste visual.',
        '- Status: propostas CORRIGIR do lote já revisado tecnicamente, ainda sem aprovação humana. Este documento não implementa, não publica e não autoriza aplicação.', '',
        '## Como ler os textos literais', '',
        'Os blocos JSON guardam a string completa, sem paráfrase e sem reticências. As aspas externas são delimitadores; \\n é quebra de linha, \\r é retorno de carro e \\" é aspas no conteúdo. Para copiar a string, decodifique o JSON; não cole as aspas/escapes como texto. Isso conserva espaços e controles sem depender da renderização Markdown.',
        'ATUAL significa o snapshot da fonte abaixo, não uma leitura do jogo em execução. A chave inglesa é imutável e serve de endereço, não é proposta de tradução. Todos os alvos deste digest são entradas_ptbr[0].Value; não alterar outras entradas, gênero ou chaves por busca parcial de nome.', '',
        '## Prova e proveniência', '',
        f'- Fonte original: `{SOURCE.as_posix()}`.',
        f'- SHA-256 do ZIP fonte: `{initial_hashes[str(SOURCE)]}`.',
        '- Membro literal: `entrega02/localizacao-ptbr.json`; origem declarada no dump: `resources.assets`, path_id 2547158, `Localization/LocalizationDataPortugueseBrazil`. Os assets do jogo não foram abertos nem revalidados neste cartão.',
        f'- SHA-256 do JSON fonte: `{sha(members["entrega02/localizacao-ptbr.json"])}`.',
        f'- Propostas copiadas sem reescrita: `{PROPOSALS.as_posix()}`; SHA-256 `{initial_hashes[str(PROPOSALS)]}`. Pacote de origem: `LANG-C4-propostas-entrega01.zip` do cartão t_a1ccc2dd.',
        '- Conferência executada: json.loads do membro original; índice por id sem normalização; igualdade Python == de chave, en e ptbr_atual com o registro e com entradas_ptbr[indice_entrada][campo]. Repetida nos blocos ATUAL efetivamente renderizados neste digest. PROPOSTO comparado literalmente com proposta_exata do lote revisado.',
        '- Contagem independente: filtragem por tags_quebradas/tags_divergentes em suspeitos.json, nos alertas dos registros originais e em revisao-formatacao.csv; comparação dos multiconjuntos (ID, código), sem duplicar os dois IDs sobrepostos. Resultado esperado e testado: 83 IDs / 85 alertas.',
        '- Os MANTER aparecem somente como número no resumo. Sua relação, chaves e textos foram omitidos. A regra do dono os considera aprovados por padrão; nenhum campo de aprovação foi escrito por este cartão.',
        '- Proteção de ajustes pessoais: se o texto vigente diferir do ATUAL, não sobrescrever; preservar o vigente e reapresentar o ajuste ao dono. Esta entrega apenas recorta propostas existentes, sem inferir autoria ou auditar alterações posteriores ao snapshot.',
        '- Reproduzir a prova: `python tools/preparar_revisao_dono.py --verify-only` a partir deste workspace. Recibo com hashes, contagens e número de linhas: `docs/automacao/LANG-C4-REVISAO-DONO-verificacao.json`.',
        '- NAO_EXERCITADO: runtime, interpretação das tags, substituição dinâmica de variáveis, layout/legibilidade, jogo, deploy, publicação e aprovação humana. Nenhuma correção aplicada; nenhuma fonte alterada.', '',
    ]
    for heading, group in [('Tag — maior risco primeiro', tag_changes), ('Formatação — separação de parágrafo', format_changes)]:
        lines.extend(['## ' + heading, ''])
        for x in group:
            idx, record = records[x['id']]
            rank = 'ALTO — aparente tag introduzida na tradução' if x['id'] == 'LANG-00914' else 'MÉDIO — ' + ('altura/separação de parágrafo' if x['id'] == 'LANG-07575' else 'paridade de estilo, sem defeito visual comprovado')
            lines.extend([
                f'### {x["id"]}', '',
                f'Tipo/risco: {x["natureza"]}; {rank}.',
                f'Endereço exato: `entrega02/localizacao-ptbr.json → registros[{idx}] → entradas_ptbr[{x["indice_entrada"]}].{x["campo"]}`; `id = {x["id"]}`. Índices são base zero.',
                'Chave literal (lookup exato; não editar):', '```json', q(record['chave']), '```',
                'ATUAL — literal da fonte:', '```json', q(record['entradas_ptbr'][x['indice_entrada']][x['campo']]), '```',
                'PROPOSTO — literal da proposta revisada:', '```json', q(x['proposta_exata']), '```',
                'Motivo: ' + reason(x),
                'Se não corrigir: ' + consequence(x),
                'Variáveis: ' + x['risco']['variavel_consumida'],
                f'Rastreio: proposta em `{x["parte"]}`; ATUAL conferido por igualdade literal com o caminho acima.', '',
            ])
    lines.extend(['## DECISAO', '', 'Marque uma opção por ID. AJUSTAR exige o texto ou instrução exata na segunda linha; nenhum campo vem marcado. A decisão humana é registrada no cartão LANG-C4 (t_ec66f0bb), não inferida deste digest.', ''])
    for x in ordered:
        lines.extend([f'{x["id"]}: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR', 'Ajuste/observação do dono: ____________________________________________________________'])
    return '\n'.join(lines) + '\n'


def document_blocks(text):
    main = text.split('## DECISAO\n')[0]
    chunks = re.split(r'^### (LANG-\d{5})\n', main, flags=re.M)
    result = {}
    for i in range(1, len(chunks), 2):
        if chunks[i] in result:
            raise AssertionError('ID duplicado no digest')
        result[chunks[i]] = [json.loads(v) for v in re.findall(r'```json\n(.*?)\n```', chunks[i + 1], re.S)]
    return result


class Proof(unittest.TestCase):
    def test_01_source_hash(self):
        self.assertEqual(initial_hashes[str(SOURCE)], EXPECTED_SOURCE_HASH)
        self.assertEqual(initial_hashes[str(PACKAGE)], EXPECTED_PACKAGE_HASH)
        for name, data in members.items():
            self.assertEqual(sha(data), proposal['source']['members'][name.split('/')[-1]]['sha256'])

    def test_02_source_counts_independent(self):
        self.assertEqual(len(alerts), 85)
        self.assertEqual(len({a['id'] for a in alerts}), 83)
        self.assertEqual(collections.Counter(a['codigo'] for a in alerts), {'tags_quebradas': 59, 'tags_divergentes': 26})
        broken = {a['id'] for a in alerts if a['codigo'] == 'tags_quebradas'}
        different = {a['id'] for a in alerts if a['codigo'] == 'tags_divergentes'}
        self.assertEqual(broken & different, {'LANG-00404', 'LANG-00914'})

    def test_03_counts_three_sources(self):
        signature = lambda xs: collections.Counter((a['id'], a['codigo']) for a in xs)
        from_records = [dict(a, id=r['id']) for r in source['registros'] for a in r['alertas'] if a['codigo'] in CODES]
        self.assertEqual(signature(alerts), signature(rows))
        self.assertEqual(signature(alerts), signature(from_records))
        from_proposals = [dict(a, id=x['id']) for x in items for a in x['alertas']]
        self.assertEqual(signature(alerts), signature(from_proposals))

    def test_04_selection(self):
        self.assertEqual(len(items), 83)
        self.assertEqual(len(by_id), 83)
        self.assertEqual(set(by_id), {a['id'] for a in alerts})
        self.assertEqual(len(changes), 16)
        self.assertEqual(len(keeps), 67)
        self.assertEqual(len(tag_changes), 15)
        self.assertEqual(len(format_changes), 1)
        self.assertTrue(all(x['ptbr_atual'] == x['proposta_exata'] for x in keeps))
        self.assertTrue(all(x['ptbr_atual'] != x['proposta_exata'] for x in changes))

    def test_05_all_83_before_literal(self):
        for x in items:
            _, r = records[x['id']]
            self.assertEqual(x['chave'], r['chave'])
            self.assertEqual(x['en'], r['en'])
            self.assertEqual(x['ptbr_atual'], r['ptbr'])
            self.assertEqual(x['ptbr_atual'], r['entradas_ptbr'][x['indice_entrada']][x['campo']])
            self.assertEqual((x['indice_entrada'], x['campo']), (0, 'Value'))

    def test_06_proposal_package_parity(self):
        with zipfile.ZipFile(io.BytesIO(raw[str(PACKAGE)])) as z:
            self.assertEqual(z.read('docs/automacao/LANG-C4-propostas-dados01.json'), raw[str(PROPOSALS)])

    def test_07_rendered_literal_and_addresses(self):
        text = OUT.read_text(encoding='utf-8')
        blocks = document_blocks(text)
        self.assertEqual(list(blocks), [x['id'] for x in ordered])
        for x in ordered:
            idx, r = records[x['id']]
            self.assertEqual(blocks[x['id']], [r['chave'], r['entradas_ptbr'][0]['Value'], x['proposta_exata']])
            self.assertIn(f'registros[{idx}] → entradas_ptbr[0].Value', text)

    def test_08_no_keep_details(self):
        text = OUT.read_text(encoding='utf-8')
        for x in keeps:
            self.assertNotIn(x['id'], text)
        self.assertEqual(len(document_blocks(text)), 16)

    def test_09_decision_two_lines_per_item(self):
        block = OUT.read_text(encoding='utf-8').split('## DECISAO\n')[1]
        decision_lines = [v for v in block.splitlines() if v.startswith('LANG-') or v.startswith('Ajuste/observação')]
        self.assertEqual(len(decision_lines), 32)
        for i, x in enumerate(ordered):
            self.assertEqual(decision_lines[i * 2], f'{x["id"]}: [ ] APROVAR  [ ] REJEITAR  [ ] AJUSTAR')
            self.assertTrue(decision_lines[i * 2 + 1].startswith('Ajuste/observação do dono: ____'))
        self.assertNotIn('[x]', block.lower())

    def test_10_preserve_lexical_content_and_variables(self):
        strip_tags = lambda t: re.sub(r'<[^>]*>', '', t)
        token_pattern = r'\{[^{}]*\}|\[[^\[\]]*\]|\*\d+|Get\w*\([^)]*\)'
        for x in ordered:
            a, b = x['ptbr_atual'], x['proposta_exata']
            self.assertEqual(re.findall(token_pattern, a), re.findall(token_pattern, b))
            if x['id'] == 'LANG-00914':
                self.assertEqual(b, a.replace('<Sully Walker, a mestra caçadora>', '<gold><incr><b>Sully Walker, a mestra caçadora</b></incr></gold>'))
            elif x['id'] == 'LANG-07575':
                self.assertEqual(b, a.replace('\nEntre os seus espólios roubados', '\n\nEntre os seus espólios roubados', 1))
            else:
                self.assertEqual(strip_tags(a), strip_tags(b))

    def test_11_empty_approval_fields(self):
        for x in items:
            for key in ('decisao_dono', 'texto_aprovado', 'observacoes'):
                self.assertEqual(x[key], '')

    def test_12_inputs_unchanged(self):
        self.assertEqual(initial_hashes, {str(p): sha(p.read_bytes()) for p in INPUTS})

    def test_13_risk_and_required_fields(self):
        self.assertEqual(ordered[0]['id'], 'LANG-00914')
        self.assertEqual(ordered[1]['id'], 'LANG-07329')
        self.assertEqual(ordered[-1]['id'], 'LANG-07575')
        text = OUT.read_text(encoding='utf-8')
        self.assertEqual(text, render())
        for label in ('Motivo:', 'Se não corrigir:', 'Variáveis:', 'Rastreio:'):
            self.assertEqual(text.count(label), 16)
        self.assertIn('Variável: 0 propostas. Sentido: 0 propostas.', text)


if __name__ == '__main__':
    if '--verify-only' not in sys.argv:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        # Nunca sobrescrever silenciosamente uma edição do dono.
        if OUT.exists() and OUT.read_text(encoding='utf-8') != render():
            raise SystemExit('Documento existente diferente: preservar e revisar antes de sobrescrever.')
        if not OUT.exists():
            OUT.write_text(render(), encoding='utf-8', newline='\n')
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Proof)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    print(stream.getvalue())
    report = {
        'task_id': 't_58bc3d48',
        'scope': 'Somente material de aprovação; nenhuma correção aplicada ou aprovação humana presumida.',
        'document': OUT.as_posix(),
        'document_sha256': sha(OUT.read_bytes()),
        'document_lines': len(OUT.read_bytes().splitlines()),
        'source_archive': SOURCE.as_posix(),
        'source_archive_sha256': initial_hashes[str(SOURCE)],
        'source_member_hashes': {name: sha(data) for name, data in members.items()},
        'proposals': PROPOSALS.as_posix(),
        'input_hashes_before': initial_hashes,
        'input_hashes_after': {str(p): sha(p.read_bytes()) for p in INPUTS},
        'counts': {'ids': len(items), 'alerts': len(alerts), 'broken_tags': 59, 'different_tags': 26, 'change': len(changes), 'keep': len(keeps), 'tag_changes': len(tag_changes), 'format_changes': len(format_changes), 'variable_changes': 0, 'meaning_changes': 0},
        'literal_before_verified_ids': [x['id'] for x in ordered],
        'literal_comparison': 'json.loads + Python == contra registros[index].entradas_ptbr[0].Value; blocos JSON do Markdown decodificados e comparados outra vez; nenhuma normalização.',
        'tests_run': result.testsRun,
        'tests_passed': result.wasSuccessful(),
        'test_output': stream.getvalue(),
        'owner_gate': {'task_id': 't_ec66f0bb', 'modified': False, 'approval_recorded': False},
        'not_exercised': ['runtime', 'renderização/tags', 'substituição dinâmica', 'layout', 'jogo', 'deploy', 'publicação', 'aprovação humana'],
        'items': [{'id': x['id'], 'source_record_index': records[x['id']][0], 'field': 'entradas_ptbr[0].Value', 'before_utf8_sha256': sha(x['ptbr_atual'].encode('utf-8')), 'proposed_utf8_sha256': sha(x['proposta_exata'].encode('utf-8'))} for x in ordered],
    }
    RECEIPT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: report[k] for k in ('document', 'document_lines', 'counts', 'tests_run', 'tests_passed')}, ensure_ascii=False, indent=2))
    sys.exit(0 if result.wasSuccessful() else 1)
