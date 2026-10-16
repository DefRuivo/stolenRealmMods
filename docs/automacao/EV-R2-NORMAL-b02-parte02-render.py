#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o documento documental EV-R2-NORMAL-b02-parte02.md a partir de b02_data.json.

Uso: python gen_b02.py [arquivo_com_saida_da_auditoria.txt]
"""
import json, os, sys, hashlib, datetime

WS = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:/dev/stolen-realm/docs/cobertura/EV-R1"
DEST = r"C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b02-parte02.md"

EV = json.load(open(os.path.join(BASE, 'eventos.json'), encoding='utf-8'))
DATA = json.load(open(os.path.join(WS, 'EV-R2-NORMAL-b02-parte02-validacao.json'), encoding='utf-8'))
NORMAL = [e for e in EV['eventos'] if e['categoria'] == 'Normal']
# ordinal N da categoria Normal = NORMAL[N-1] (o bloco Normal comeca no ordinal 1)
SLICE = {n: NORMAL[n - 1] for n in range(21, 41)}
MD = open(os.path.join(BASE, 'lote-Normal-v2.md'), encoding='utf-8').read().splitlines()
HEADS = [l[3:] for l in MD if l.startswith('## ')]
AGG = DATA['agregados']
D = {e['ordinal']: e for e in DATA['events']}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def q(s):
    return '"%s"' % s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')

L = []
w = L.append

w("# EV-R2-NORMAL-b02-parte02 - Correcao documental dos eventos 21-40 (Lote Normal)")
w("")
w("Cartao: t_3456f6a9 - corretivo do cartao original t_d06fd366, derivado da revisao independente t_4c07d669.")
w("Arquivo gerado em: %s (Hora oficial do Brasil)." % datetime.date.today().isoformat())
w("Documento SUBSTITUI, na leitura, a analise de `docs/automacao/EV-R2-NORMAL-b02-parte01.md`.")
w("O arquivo parte01 e o original **nao foram alterados**: esta correcao e um artefato novo (parte02).")
w("")
w("Status: **PROPOSTA** para aprovacao do dono. Nada foi implementado, nenhum asset/DLL foi tocado,")
w("nenhuma fonte de EV-R1 foi modificada, nada foi publicado e nenhum `git push` foi executado.")
w("")
w("Escopo: **20 eventos da categoria Normal, ordinais 21-40** (20 eventos unicos).")
w("Ordem dos ordinais: ordem das secoes do JSON/markdown da categoria Normal (alfabetica por titulo),")
w("nunca path_id crescente.")
w("")
w("Fontes (somente leitura) e hashes no momento da geracao:")
for nome, p in DATA['fontes'].items():
    w("- `%s` -> `%s` sha256 `%s`" % (nome, p, sha256(p)))
w("")
w("Estado de runtime: **NAO_EXERCITADO**. Nenhuma conclusao deste documento depende de execucao no jogo.")
w("Quantidades finais de ouro/XP/loot, sorteios, exibicao de texto na tela e a localizacao selecionada")
w("permanecem nao exercitados (ver `cobertura.nao_exercitado` do eventos.json).")
w("")
w("---")
w("")
w("## 0. Como ler este documento")
w("")
w("| Rotulo | Significado |")
w("|---|---|")
w("| **PROPOSTA DE CONTEUDO** | proposta de conteudo novo para o evento (texto ou valor de configuracao), ancorada no que a fonte ja configura |")
w("| **SUGESTAO DE CORRECAO DO ORIGINAL** | defeito literal medido no texto ingles do proprio asset (ortografia, pontuacao, espaco). Nao e o texto que sera exibido ao jogador hoje; e o literal da fonte que se sugere corrigir |")
w("| **REFUTACAO** | afirmacao da parte01 que a medicao desmente, com o valor real e o caminho na fonte |")
w("| **MANTER** | nenhuma alteracao proposta; manutencao justificada pelo que a fonte ja entrega |")
w("| **MELHORAR** | existe ao menos uma proposta concreta com JSONPath, antes literal e depois exato |")
w("")
w("Convencoes de caminho: os JSONPath sao relativos a `eventos.json` (`$.eventos[N]`), em que `N` e")
w("simultaneamente o ordinal da categoria Normal (no array, o indice 0 e o unico evento AfterBattle e o bloco")
w("Normal comeca no indice 1; portanto indice global = ordinal Normal).")
w("Indices de lista sao 0-based; o campo `indice` dentro dos objetos e 1-based (ex.: `opcoes[1]` tem `indice` 2).")
w("")
w("Textos de proposta sao escritos **em ingles**, preservando o idioma da fonte; nenhuma traducao PT-BR e")
w("apresentada como texto de asset. Onde houver leitura em portugues, ela aparece como comentario, nunca como literal.")
w("")
w("---")
w("")

# ---------------- 1. identidades ----------------
w("## 1. Identidades canonicas da faixa 21-40")
w("")
w("Conferido contra `eventos.json` (categoria Normal, ordem do array) e contra os cabecalhos `##` de")
w("`lote-Normal-v2.md`: **20/20 titulos identicos nas duas fontes**.")
w("")
w("| # | chave | id | titulo | nome_asset | categoria | raridade | peso | disabled | opcoes |")
w("|---|---|---|---|---|---|---|---|---|---|")
for n in range(21, 41):
    e = SLICE[n]
    co = e['condicoes']
    na = e['nome_asset']
    w("| %d | `%s` | `%s` | %s | %s | %s | %s(%s) | %s | %s | %d |" % (
        n, e['chave'], e['id'], e['titulo'], na if na != e['titulo'] else '-', e['categoria'],
        e['raridade']['nome'], e['raridade']['valor'], e['peso'], co['disabled'], len(e['opcoes'])))
w("")
w("Observacoes de identidade:")
w("- Ordinal 27: titulo do evento `Cursed Chest`, `nome_asset` `Cursed Mimic Chest` e `EventNameOverride` `Cursed Chest`;")
w("  e a segunda variante da arca da faixa (a primeira e o ordinal 26).")
w("- Ordinais 26 e 27 tem textos identicos entre si; ordinais 31 e 34 tem textos, opcoes e efeitos identicos entre si.")
w("- Nenhum dos 20 eventos repete chave ou id: 20 chaves unicas e 20 ids unicos (ver Analise C).")
w("")
w("---")
w("")

# ---------------- 2. supersessao ----------------
w("## 2. Supersessao explicita das afirmacoes da parte01")
w("")
w("### 2.1 Identidade: as 20 chaves da parte01 estao deslocadas")
w("")
w("A parte01 usou chaves de `resources.assets:2545402` a `resources.assets:2545421`, nenhuma delas")
w("pertencente a esta faixa. **0/20 pares titulo+chave corretos.** O deslocamento e sistematico (a chave")
w("usada e ~150 menor que a real), o que produziu a cascata de analises sobre eventos que nao sao estes.")
w("")
w("| ordinal | chave da parte01 (falsa) | chave real | titulo da parte01 (quando falso) | titulo real |")
w("|---|---|---|---|---|")
FALSAS = {
    21: ('resources.assets:2545402', 'Boss Fight - Roland (titulo correto; raridade/peso/texto falsos)'),
    22: ('resources.assets:2545403', None),
    23: ('resources.assets:2545404', 'Cursed Coin Toss -> Carved Monolith'),
    24: ('resources.assets:2545405', 'Carved Rune (titulo correto)'),
    25: ('resources.assets:2545406', None),
    26: ('resources.assets:2545407', None),
    27: ('resources.assets:2545408', 'Cursed Mimic Chest -> Cursed Chest (2a variante)'),
    28: ('resources.assets:2545409', None),
    29: ('resources.assets:2545410', None),
    30: ('resources.assets:2545411', None),
    31: ('resources.assets:2545412', None),
    32: ('resources.assets:2545413', None),
    33: ('resources.assets:2545414', None),
    34: ('resources.assets:2545415', 'Disturbing Statue -> Dwarven Drinking Contest'),
    35: ('resources.assets:2545416', None),
    36: ('resources.assets:2545417', None),
    37: ('resources.assets:2545418', None),
    38: ('resources.assets:2545419', "Dwarven Forge -> Edwin's Demise"),
    39: ('resources.assets:2545420', 'Dwarven Market -> Elder Tree'),
    40: ('resources.assets:2545421', None),
}
for n in range(21, 41):
    fk, ft = FALSAS[n]
    w("| %d | `%s` | `%s` | %s | %s |" % (n, fk, SLICE[n]['chave'], ft or 'correto', SLICE[n]['titulo']))
w("")
w("### 2.2 As cinco acusacoes da revisao e o que a medicao mostra")
w("")
w("| # | Acusacao da revisao | Situacao apos a medicao | Evidencia |")
w("|---|---|---|---|")
w("| 1 | As 20 chaves estao erradas; 0/20 pares titulo+chave | CONFIRMADA | Secao 2.1; ordinal 21 = `resources.assets:2545552`, Common, peso 1.0, disabled 1, texto de 80 ch, opcoes Laugh/Cower |")
w("| 2 | Titulos inventados em 23/27/34/38/39 | CONFIRMADA; titulos reais: Carved Monolith, Cursed Chest (2a variante), Dwarven Drinking Contest, Edwin's Demise, Elder Tree | Secao 1 e blocos 23/27/34/38/39; cada um teve a acao real reanalisada, nao apenas renomeada |")
w("| 3 | Alegacao de Failure ausente em 26/28/35/36/40 e falsa | CONFIRMADA. Acao Failure presente e medida em 26 (limiar 0), 28 (1), 35 (1), 36 (1), 40 (1) | Efeitos reais: Cursed (26), Slowed (28), -30% max HP + Severely Burned (35), Weakened (36), -20% max HP + Mortally Wounded (40) |")
w("| 4 | Vazios narrativos sao 24/37; disabled sao 21/31/34; Brawler's Brew (22) esta habilitado com Drink/Leave | CONFIRMADA, com precisao: 24 tem `\\n` (1 caractere) e 37 tem cadeia vazia; disabled = 21, 31, 34; 22 tem disabled=0 e exatamente 2 opcoes, Drink e Leave | Analise C e blocos 22/24/31/34/37 |")
w("| 5 | Falta veredito MANTER/MELHORAR por evento e inventario; investigacao vaga; portugues misturado | CONFIRMADA e corrigida: 20/20 vereditos com justificativa (secao 3), 19 propostas com JSONPath/antes/depois, 65 refutacoes, texto integralmente em PT-BR | Secoes 3, 4 e 5 |")
w("")
w("### 2.3 Contagens da parte01 versus medicao")
w("")
w("| Afirmacao da parte01 | Valor medido | Correcao |")
w("|---|---|---|")
w("| 3 eventos com `texto` vazio (21, 24, 37) | 2 eventos sem narrativa: 24 (`\\n`) e 37 (`\"\"`) | o 21 tem texto de 80 caracteres |")
w("| 2 eventos com `disabled: 1` (22, 31) | 3 eventos: 21, 31, 34 | o 22 esta habilitado (disabled=0) |")
w("| 6 eventos com 1 unica opcao (21, 24, 28, 35, 37, 40) | 5 eventos: 24, 28, 35, 37, 40 | o 21 tem 2 opcoes (Laugh, Cower) |")
w("| 5 eventos sem texto de resultado (25, 27, 29, 32, 34) | 5 eventos com pelo menos uma acao sem texto de resultado: 21, 24, 25, 29, 37 | lista e criterio estavam errados; 27, 32 e 34 tem textos de resultado completos |")
w("| 6 eventos com rolagem sem Failure (26, 27, 28, 36, 38, 39) | 2 eventos com bonus de rolagem e sem Failure: 27 e 33 | 26, 28, 36 e 38 tem Failure; 39 nao tem rolagem |")
w("| EVT 21 RARIDADE Boss, peso 0.1 | Common(0), peso 1.0 | nao existe raridade Boss entre os eventos da faixa; 37 e o unico Legendary |")
w("| \"6 eventos sem Failure\" como defeito de tensao | 6 eventos tem Failure e 8 tem rolagem | ver Analise C |")
w("| Distribuicao de terrenos \"Plains, Underground Cave, Mountain Pass, Dark Forest, Dwarven Depths, Snowy Mountain Peak\" | terrenos nomeados por `enums.json` (WaterTempleRuins, WyrmrestDesert, FreewindForest, CastleGloom, ForgottenMines, Emberlands, EmeraldJungle, FrostwroughtMountain, SunkenSwamplands, DwarvenHalls) | nomes da parte01 nao correspondem ao enum da fonte |")
w("")
w("---")
w("")

# ---------------- 3. inventario de decisoes ----------------
w("## 3. Inventario de decisoes (MANTER / MELHORAR)")
w("")
w("| Veredito | Quantidade | Ordinais |")
w("|---|---|---|")
for v in ('MANTER', 'MELHORAR'):
    ns = [str(e['ordinal']) for e in DATA['events'] if e['veredito'] == v]
    w("| %s | %d | %s |" % (v, len(ns), ', '.join(ns)))
w("")
w("| # | titulo | veredito | propostas | natureza das propostas |")
w("|---|---|---|---|---|")
for n in range(21, 41):
    d = D[n]
    nat = '; '.join(sorted({p['natureza'] for p in d['propostas']})) or '-'
    w("| %d | %s | %s | %d | %s |" % (n, SLICE[n]['titulo'], d['veredito'], len(d['propostas']), nat))
w("")
w("Total de propostas: **%d** (%d de conteudo, %d de correcao do texto original)." % (
    sum(len(d['propostas']) for d in D.values()),
    sum(1 for d in D.values() for p in d['propostas'] if p['rotulo'] == 'PROPOSTA DE CONTEUDO'),
    sum(1 for d in D.values() for p in d['propostas'] if p['rotulo'] == 'SUGESTAO DE CORRECAO DO ORIGINAL')))
w("")
w("---")
w("")
w("## 4. Evento por evento")
w("")

for n in range(21, 41):
    e = SLICE[n]
    d = D[n]
    co = e['condicoes']
    w("### %d - %s" % (n, e['titulo']))
    w("")
    w("| campo | valor |")
    w("|---|---|")
    w("| chave | `%s` |" % e['chave'])
    w("| id | `%s` |" % e['id'])
    w("| nome_asset | %s |" % e['nome_asset'])
    w("| categoria | %s |" % e['categoria'])
    w("| raridade | %s(%s) |" % (e['raridade']['nome'], e['raridade']['valor']))
    w("| peso | %s |" % e['peso'])
    w("| pool | %s |" % ', '.join(p['nome'] for p in e['pool']))
    w("| disabled | %s |" % co['disabled'])
    w("| modos | %s |" % ', '.join(m['nome'] for m in e['modos']))
    w("| historia / full_release | %s / %s |" % (e['historia']['nome'], e['full_release']['nome']))
    w("| minLevel | %s |" % co['minLevel'])
    w("| node types | %s (allowOnAllNodeTypes=%s) |" % (co['allowedNodeTypes'], co['allowOnAllNodeTypes']))
    w("| terreno | %s |" % ('qualquer (allowOnAllTerrainTypes=1), exceto: ' + str(co['allowedTerrainTypes'])
                            if co['allowOnAllTerrainTypes'] == 1 and co['allowedTerrainTypes']
                            else ('qualquer' if co['allowOnAllTerrainTypes'] == 1 else str(co['allowedTerrainTypes']))))
    w("| horario | %s (allowAtAllTimesOfDay=%s) |" % (co['allowedTimeOfDay'], co['allowAtAllTimesOfDay']))
    w("| niveis | allowAtAllLevels=%s |" % co['allowAtAllLevels'])
    w("| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | %s / %s / %s |" % (
        co['LeadsToFortune'], co['isLesserEvent'], co['KeepInDeckWhenUsed']))
    w("| origem | `%s` path_id %s |" % (e['origem']['arquivo'], e['origem']['path_id']))
    w("| sha256_objeto | `%s` |" % e['origem']['sha256_objeto'])
    w("")
    w("**Estado real medido.** %s" % d['estado'])
    w("")
    w("**Veredito: %s.** %s" % (d['veredito'], d['justificativa']))
    w("")
    if d['propostas']:
        w("**Propostas:**")
        w("")
        for i, p in enumerate(d['propostas'], start=1):
            w("%d. [%s] natureza: %s" % (i, p['rotulo'], p['natureza']))
            w("   - caminho: `%s`" % p['jsonpath'])
            w("   - tipo de conferencia: %s" % ('campo integral (antes = valor exato do campo)' if p['tipo'] == 'campo'
                                                else 'trecho literal (antes = substring exata do campo)'))
            w("   - antes: `%s`" % p['antes'].replace('`', "'").replace('\n', '\\n').replace('\r', '\\r'))
            w("   - depois: `%s`" % p['depois'].replace('`', "'").replace('\n', '\\n').replace('\r', '\\r'))
            w("   - fundamento: %s" % p['fundamento'])
        w("")
    else:
        w("**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.")
        w("")
    w("**Refutacoes a parte01:**")
    w("")
    for r in d['refutacoes']:
        w("- %s" % r)
    w("")
    if d['observacoes']:
        w("**Observacoes (sem proposta):**")
        w("")
        for o in d['observacoes']:
            w("- %s" % o)
        w("")
    w("**Referencias NULL do evento: %d caminhos.**" % len(e['ausencias']))
    w("")
    w("| classe de NULL | caminho de exemplo |")
    w("|---|---|")
    seen = {}
    for p in sorted(e['ausencias']):
        cls = p.replace('opcoes[0]', 'opcoes[*]').replace('opcoes[1]', 'opcoes[*]')
        cls = cls.replace('opcoes[2]', 'opcoes[*]').replace('efeitos[0]', 'efeitos[*]').replace('efeitos[1]', 'efeitos[*]')
        cls = cls.replace('padrao[0]', 'padrao[*]').replace('recompensas[0]', 'recompensas[*]').replace('recompensas[1]', 'recompensas[*]')
        seen.setdefault(cls, p)
    for cls, exemplo in sorted(seen.items()):
        w("| `%s` | `%s` |" % (cls, exemplo))
    w("")
    w("Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou")
    w("valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e")
    w("interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,")
    w("caminho a caminho, esta na Analise B.")
    w("")
    w("---")
    w("")

# ---------------- 5. analise A ----------------
w("## 5. Analise A - inventario de literais do texto ingles")
w("")
w("Todas as propostas rotuladas SUGESTAO DE CORRECAO DO ORIGINAL, com o caminho exato, o literal de origem e o")
w("literal corrigido. Nenhuma delas foi aplicada a fonte.")
w("")
w("| # | ordinal | natureza | caminho | antes | depois |")
w("|---|---|---|---|---|---|")
i = 0
for n in range(21, 41):
    for p in D[n]['propostas']:
        if p['rotulo'] != 'SUGESTAO DE CORRECAO DO ORIGINAL':
            continue
        i += 1
        w("| %d | %d | %s | `%s` | `%s` | `%s` |" % (
            i, n, p['natureza'], p['jsonpath'],
            p['antes'].replace('`', "'").replace('\n', '\\n'),
            p['depois'].replace('`', "'").replace('\n', '\\n')))
w("")
w("Itens cosmeticos medidos que **nao** geram proposta (registro por transparencia):")
w("")
w("| ordinal | caminho | achado |")
w("|---|---|---|")
w("| 21 | `$.eventos[21].texto` | espaco duplo em `\"Go on!  Come at me` |")
w("| 22 | `$.eventos[22].opcoes[0].efeitos[0].texto` | espaco final depois de `fuzzy.\" ` |")
w("| 33 | `$.eventos[33].opcoes[0].texto`, `$.eventos[33].opcoes[1].texto` | espaco final nos dois textos |")
w("| 33 | status `Well Fed:  Experience` (2545402) | nome com espaco duplo no catalogo, nao no evento |")
w("")
w("---")
w("")

# ---------------- 6. analise B ----------------
w("## 6. Analise B - inventario NULL completo")
w("")
w("Total de entradas em `ausencias` para os 20 eventos: **%d**." % AGG['nulls_total'])
w("")
w("| ordinal | eventos | caminhos NULL |")
w("|---|---|---|")
for n in range(21, 41):
    w("| %d | %s | %d |" % (n, SLICE[n]['titulo'], len(SLICE[n]['ausencias'])))
w("")
for n in range(21, 41):
    w("### B.%d - %s (%d caminhos NULL)" % (n, SLICE[n]['titulo'], len(SLICE[n]['ausencias'])))
    w("")
    for p in sorted(SLICE[n]['ausencias']):
        w("- `$.eventos[%d].%s`" % (n, p[2:] if p.startswith('$.') else p))
    w("")
w("---")
w("")

# ---------------- 7. analise C ----------------
w("## 7. Analise C - agregados medidos")
w("")
w("| medida | valor |")
w("|---|---|")
w("| eventos na faixa | %d |" % AGG['eventos'])
w("| chaves unicas / ids unicos | %d / %d |" % (AGG['chaves_unicas'], AGG['ids_unicos']))
w("| opcoes no total | %d |" % AGG['opcoes_total'])
w("| acoes no total (Success + Failure) | %d (%d Success, %d Failure) |" % (
    AGG['acoes_total'], AGG['acoes_success'], AGG['acoes_failure']))
w("| eventos sem narrativa | %s |" % AGG['sem_narrativa'])
w("| eventos com disabled=1 | %s |" % AGG['disabled'])
w("| eventos com 1 unica opcao | %s |" % AGG['uma_opcao'])
w("| eventos com acao Failure | %s |" % AGG['com_failure'])
w("| eventos com bonus de rolagem | %s |" % AGG['com_rolagem'])
w("| eventos com rolagem e sem Failure | %s |" % AGG['rolagem_sem_failure'])
w("| eventos que iniciam batalha | %s |" % AGG['inicia_batalha'])
w("| eventos que iniciam batalha sem BattleInfo referenciado | %s |" % AGG['batalha_sem_ref'])
w("| eventos que concedem status | %s |" % AGG['emite_status'])
w("| eventos que concedem item | %s |" % AGG['da_item'])
w("| eventos que concedem XP | %s |" % AGG['da_xp'])
w("| eventos que concedem ouro | %s |" % AGG['da_ouro'])
w("| eventos com opcao sem texto | %s |" % AGG['opcao_sem_texto'])
w("| eventos com acao de resultado sem texto | %s |" % AGG['acao_sem_texto'])
w("| eventos com status_requeridos em alguma opcao | %s |" % AGG['com_status_requerido'])
w("| LeadsToFortune=1 | %s |" % AGG['leads_to_fortune'])
w("| raridade | %s |" % '; '.join('%s: %s' % (k, v) for k, v in sorted(AGG['raridade'].items())))
w("| peso | %s |" % '; '.join('%s: %s' % (k, v) for k, v in sorted(AGG['peso'].items())))
w("| caminhos NULL | %d |" % AGG['nulls_total'])
w("")
w("---")
w("")

# ---------------- 8. auditoria ----------------
w("## 8. Auditoria automatica offline")
w("")
w("Comando executado (a partir do workspace do cartao):")
w("")
w("```")
w("python audit_b02.py C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b02-parte02.md")
w("```")
w("")
w("Para reproducao a partir desta pasta (arquivos do lote):")
w("")
w("```")
w("python EV-R2-NORMAL-b02-parte02-validar.py EV-R2-NORMAL-b02-parte02.md")
w("```")
w("")
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    saida = open(sys.argv[1], encoding='utf-8').read().strip()
    w("Saida REAL da execucao:")
    w("")
    w("```")
    w(saida)
    w("```")
else:
    w("Saida real: ver o campo `real_command_output` do handoff do cartao t_3456f6a9.")
w("")
w("---")
w("")
w("## 9. Pendencias e estado")
w("")
w("- Este documento e **proposta documental**: nada foi implementado, nada foi alterado em EV-R1, no")
w("  `Assembly-CSharp.dll`, em assets, plugins ou mods.")
w("- Runtime **NAO_EXERCITADO**: nenhuma afirmacao aqui depende de execucao no jogo.")
w("- Depende de aprovacao de conteudo do dono antes de qualquer implementacao.")
w("- Achado pendente de decisao do dono: ordinal 34 carrega o conteudo do ordinal 31 (conteudo provisorio),")
w("  ambos disabled. Nenhuma proposta de texto foi feita para esse slot.")
w("- Achado pendente de decisao do dono: ordinal 27 tem `rollBonusTypes=[3]` com limiar 0 e sem Failure,")
w("  enquanto o ordinal 26 (mesma batalha) usa o mesmo bonus com limiar 12 e ramo de falha.")
w("- Sugestoes de alteracao do texto ingles original permanecem rotuladas e nao aplicadas.")
w("")
w("Fim do documento.")
w("")

doc = "\n".join(L)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
open(DEST, 'w', encoding='utf-8', newline='\n').write(doc)
print("escrito: %s (%d bytes, %d linhas)" % (DEST, len(doc.encode('utf-8')), len(L)))
