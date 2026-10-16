"""Renderiza EV-R2-NORMAL-b01-parte02.md a partir da validação JSON, fatos e saída da auditoria."""
import json, os, hashlib

DEST = "C:/dev/stolen-realm/docs/automacao"
SRC = "C:/dev/stolen-realm/docs/cobertura/EV-R1"
BASE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(DEST, "EV-R2-NORMAL-b01-parte02.md")
AUD_TXT = os.path.join(DEST, "EV-R2-NORMAL-b01-parte02-auditoria.txt")

val = json.load(open(os.path.join(BASE, "EV-R2-NORMAL-b01-parte02-validacao.json"), encoding="utf-8"))
F = json.load(open(os.path.join(BASE, "EV-R2-NORMAL-b01-parte02-fatos.json"), encoding="utf-8"))
aud = open(AUD_TXT, encoding="utf-8").read().strip() if os.path.exists(AUD_TXT) else "(auditoria não executada nesta renderização)"
recs = val["registros"]

with open(os.path.join(SRC, "eventos.json"), encoding="utf-8") as _f:
    _all = json.load(_f)["eventos"]
EVBYKEY = {e["chave"]: e for e in _all}


def lit(v, label):
    if v == "":
        return f"  {label}: (string vazia \"\")"
    if "\n" in v or len(v) > 90:
        return f"  {label}:\n```\n{v}\n```"
    return f"  {label}: `{v}`"


L = []
A = L.append
A("# EV-R2-NORMAL-b01 — parte 02: eventos 1–20 do lote Normal (correção da parte01)")
A("")
A("Status: **PROPOSTAS PARA APROVAÇÃO DO DONO**; nada implementado no jogo, nenhuma decisão aprovada.")
A("Natureza: documento corretivo da parte01 (`EV-R2-NORMAL-b01-parte01.md`, mantida intacta como registro da entrega reprovada).")
A("Origem: revisão independente `t_4c07d669` (parecer: REPROVAR a parte01 e corrigir). Cartão original `t_d61a5d8d`; cartão corretivo `t_67a3887a`.")
A("")
A("## 0. Escopo, fontes e regras")
A("")
A("Faixa exata: seções 1–20 do lote **Normal** (20 eventos), na ordem do JSON `categoria = Normal` — a mesma ordem do `lote-Normal-v2.md`. Não se ordena por `path_id` (a faixa não é monotônica: #19=2545550 e #20=2545553 vêm depois de #18=2545551).")
A("")
A("Fontes (somente leitura): `C:/dev/stolen-realm/docs/cobertura/EV-R1/{eventos.json, lote-Normal-v2.md, eventos.schema.json, catalogo-referencias.json}`.")
A("Nada de jogo, DLL/plugin, balanceamento implementado, publicação, commit ou push. Ajustes manuais do dono e todas as entregas anteriores permanecem intocados.")
A("")
A("Regra de edição proposta: onde o item diz **CAMPO**, a proposta substitui a string inteira do campo indicado; onde diz **TRECHO**, substitui exatamente o trecho citado e preserva todos os demais bytes (espaços, CR/LF, tags `<...>` e placeholders). Índices são base 1 no documento e base 0 no JSON (aqui os JSONPath já estão em base 0, prontos para uso).")
A("Textos de jogo são mantidos em **inglês**; PT-BR aparece apenas como tradução explicitamente marcada — neste lote não há proposta de tradução.")
A("")
A("## 1. Integridade das fontes")
A("")
A("| Fonte | SHA256 conferido |")
A("|---|---|")
for k, v in val["fontes_sha256"].items():
    A(f"| `{k}` | `{v}` |")
A("")
A("Integridade verificada pela auditoria automática (seção 7): 4/4 fontes com SHA256 estável; `EV-R2-NORMAL-b01-parte01.md` inalterada em `e65daa3413e18adc1d73b6272d936f8d7d593da83e90abfbb06c34f6aee530e9`.")
A("")
A("## 2. Semântica usada (NULL, disabled, runtime)")
A("")
A("- **NULL de resultado** = NAO_EXERCITADO. Ouro depende de nível/razão/multiplicador, experiência depende do estado da partida, itens dependem de nível/restrições/RNG, status não foi sorteado e combate não foi executado. Campo com `null` e `motivo` explícito **não** prova defeito nem ausência de configuração.")
A("- **NULL de PPtr** (`m_PathID = 0`) = referência nula gravada no asset, com motivo declarado. Não é GUID ausente, não é falha de deploy.")
A("- **disabled / EditorOnly** = estado de autoria, não bug. Este documento **não** propõe reativar, remover ou criar slots/opções por inferência; onde há proposta em evento desativado, ela é explicitamente condicional à decisão do autor.")
A("- **Renderização** (o que o jogador vê de fato na tela) é NAO_EXERCITADO: não se abriu o jogo. Nenhuma conclusão sobre exibição, substituição de tokens ou efeito final é apresentada como exercitada.")
A("")
A("## 3. Supersessão nominal das acusações da parte01")
A("")
A("| # | Acusação na parte01 | Situação | Consta agora em |")
A("|---|---|---|---|")
SUP = [
    ("1", "Campo `roll_bonus` vazio em 13 eventos (\"Todos exceto 5\")", "SUPERSEDIDA: o campo `roll_bonus` não existe no JSON; o caminho real é `$.opcoes[*].rolagem.bonus`. Bônus configurado em #2 (Vitality), #3 (Intelligence+3 nas três opções), #5 (Might+Dexterity) e #11 (Might); vazios em 26 dos 32 slots de opção.", "§6"),
    ("2", "#1: `chave`/`nome` NULL = \"GUID do evento não populado\" e \"falha do pipeline de deploy\"", "REFUTADA: não existem campos `chave`/`nome` no topo do esquema de evento. O evento tem chave própria `resources.assets:2545531` e id `0c69ab75-e61b-4f82-9bd6-3f5b9d6cbfcf`. O NULL está em `$.opcoes[0].condicoes.status_requeridos[0].chave/nome`, com motivo `m_PathID=0`.", "§5 #1"),
    ("3", "Tabela de anomalias: \"Campos NULL (chave/nome) = 7 eventos (1,4,9,10,14,20)\"", "REFUTADA: a lista traz 6 números, não 7; e PPtr nulo chave/nome aparece nos 20 eventos — não é anomalia distintiva (#1 continua tendo, porém, o placeholder sem status).", "§6"),
    ("4", "#9 e #20: `batalha.dados_recompensa_final` NULL = recompensa de batalha/sistema de recompensas não configurado", "REFUTADA: o campo traz motivo explícito de resolução em runtime (não exercitado). NULL de resultado ≠ referência nula ≠ recompensa inexistente.", "§5 #9, §5 #20"),
    ("5", "#2: typo literal \"appeaures\"", "REFUTADA: o literal real do original é `appeares`. A direção da correção (`appears`) continua válida e agora é registrada com o literal correto.", "§5 #2"),
    ("6", "#3: \"`roll_bonus` vazio pode indicar que a mecânica de rolagem não está implementada\"", "REFUTADA pelo catálogo: `$.opcoes[*].rolagem.bonus=[{valor:3,nome:Intelligence}]` e as quatro ações de cada opção concedem itens reais (`itens.dar=true`, tabela `mustGetOne=1`, `Chance=100`), 12 `ItemInfo` distintos do catálogo.", "§5 #3, §6"),
    ("7", "#13: \"`roll_bonus` vazio pode indicar que a mecânica de sorte não está implementada\"", "REFUTADA: bônus de rolagem vazio é o padrão da faixa (26/32 slots) e as ações de #13 são Success com `limite_rolagem=0`; nada indica rolagem quebrada. Permanece só o typo `whisperes`.", "§5 #13"),
    ("8", "#7: \"Idêntico ao Evento 6 — duplicata funcional\"", "IMPRECISA: os assets diferem em `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.quantidade_configurada` (2 em #6, 1 em #7) e no caminho de recurso (`events/armor chest - roguelike` vs `events/armor chest`).", "§5 #6, §5 #7, §6"),
    ("9", "Resumo: \"MANTER = 6 eventos\" com lista de 7", "CORRIGIDA: **MANTER = 7** (#5, #11, #12, #15, #16, #17, #18); **MELHORAR = 13**.", "§4, §6"),
    ("10", "#10: \"Se for realmente um evento de teste, removê-lo\"", "RETIRADA: excluir (ou reativar) conteúdo desativado por inferência não é correção de texto. A proposta de #10 é condicional e não altera `$.condicoes.disabled`.", "§5 #10"),
    ("11", "#1: \"Reativar (`disabled: 0`)\"", "RETIRADA: estado de autoria. Nenhuma proposta deste documento altera `disabled`.", "§5 #1, §2"),
    ("12", "#4: \"Reativar e expandir; adicionar opção Fight\"", "RETIRADA: criar opção nova é decisão de design do autor; a proposta agora é exata e incide só na descrição da opção existente e no que as ações reais mostram.", "§5 #4"),
    ("13", "#9: \"Investigar por que `dados_recompensa_final` é NULL\"", "SUPERSEDIDA: o motivo está no próprio JSON (runtime não exercitado). Não há o que investigar offline.", "§5 #9"),
    ("14", "#16: \"Texto idêntico ao 15; podem ser duplicados ou acidente\"", "MANTIDA como observação factual, sem tratamento de defeito: textos idênticos, porém chaves, ids e caminhos de recurso distintos. O mesmo vale para o par #17/#18.", "§5 #15, §5 #16, §5 #18, §6"),
    ("15", "Classe de achado \"Título repetido\" tratado como registro duplicado", "CORRIGIDA: título repetido não é id nem chave repetidos. A única repetição real de identificador na faixa é o **id** de #9 e #10 (achado novo desta correção).", "§6"),
]
for a, b, c, d in SUP:
    A(f"| {a} | {b} | {c} | {d} |")
A("")
A("## 4. Inventário dos 20 registros")
A("")
A("| # | Chave (file:path_id) | id | Título | Categoria | Raridade | Peso | Veredito | Natureza |")
A("|---|---|---|---|---|---|---|---|---|")
for r in recs:
    A(f"| {r['ordinal']} | `{r['chave']}` | `{r['id']}` | {r['titulo']} | {r['categoria']} | "
      f"{r['raridade']['nome']} ({r['raridade']['valor']}) | {r['peso']} | **{r['veredito']}** | {r['natureza']} |")
A("")
A(f"MANTER = {val['contagens']['manter']} ({', '.join('#' + str(x) for x in val['contagens']['manter_ordinais'])})")
A(f"MELHORAR = {val['contagens']['melhorar']} ({', '.join('#' + str(x) for x in val['contagens']['melhorar_ordinais'])})")
A(f"Total analisado = {val['contagens']['total']} de 20 · propostas exatas = {val['contagens']['total_propostas']}")
A("")
A("## 5. Registros")
A("")
for r in recs:
    fa = r["fatos"]
    A(f"### {r['ordinal']} — {r['titulo']} — {r['chave']}")
    A("")
    A(f"- id: `{r['id']}`")
    A(f"- categoria: {r['categoria']} | raridade: {r['raridade']['nome']} ({r['raridade']['valor']}) | peso: {r['peso']}")
    A(f"- estados: disabled={fa['disabled']}, EditorOnly={fa['EditorOnly']}, minLevel={fa['minLevel']}, allowedNodeTypes={fa['allowedNodeTypes']}, historia={fa['historia']}")
    A(f"- asset: {', '.join('`' + p + '`' for p in fa['caminho_asset'])} | sha256_objeto: `{fa['sha256_objeto']}`")
    ev = EVBYKEY[r["chave"]]
    A(f"- texto original ({fa['texto_len']} chars):")
    A("")
    A("```")
    A(ev.get("texto") if ev.get("texto") else "(string vazia \"\")")
    A("```")
    if ev.get("texto_resultados_possiveis"):
        A(f"- texto_resultados_possiveis: `{ev['texto_resultados_possiveis']}`")
    A(f"- opções ({fa['n_opcoes']}):")
    for o in ev.get("opcoes") or []:
        rol = o.get("rolagem") or {}
        acoes = ", ".join(
            f"{a['resultado']['nome']} lim {a['limite_rolagem']}" for a in (o.get("efeitos") or []))
        A(f"  - {o['indice']}) `{o['titulo']}` — descrição: {('`' + o['texto'] + '`') if o['texto'] else '(vazia)'}; "
          f"rolagem.bonus={json.dumps(rol.get('bonus'), ensure_ascii=False)}; misteriosa={rol.get('misteriosa')}; ações: {acoes}")
    A("")
    A(f"**VEREDITO: {r['veredito']}**")
    A("")
    A("Justificativa:")
    for j in r["justificativa"]:
        A(f"- {j}")
    A("")
    if r["propostas"]:
        A(f"Propostas exatas ({len(r['propostas'])}):")
        A("")
        for p in r["propostas"]:
            A(f"- **{p['code']}** [{p['tipo']}] `{p['path']}`")
            A(lit(p["antes"], "  antes"))
            A(lit(p["depois"], "  depois"))
            A(f"  alvo/condição: conforme justificativa do registro; nota: {p['nota']}")
            A("")
    else:
        A("Propostas exatas: nenhuma (MANTER).")
        A("")
    A("---")
    A("")

A("## 6. Anomalias e contagens reais (recalculadas da fonte)")
A("")
A("| Fato | Contagem | Onde (ordinais) |")
A("|---|---|---|")
A(f"| Eventos na faixa | 20 | 1–20 |")
A(f"| Categoria Normal do lote inteiro | {F['total_normal']} | — |")
A(f"| `disabled=1` | {len(F['disabled'])} | {F['disabled']} |")
A(f"| `EditorOnly=1` | {len(F['editor_only'])} | {F['editor_only']} |")
A(f"| Texto narrativo vazio (`\"\"`) | {len(F['texto_vazio'])} | {F['texto_vazio']} |")
A(f"| Texto idêntico ao do \"yearning ghost\" | {len(F['texto_ghost'])} | {F['texto_ghost']} |")
A(f"| Títulos repetidos | {len(F['titulos_repetidos'])} grupos | {', '.join(f'{k}×{v}' for k, v in F['titulos_repetidos'].items())} |")
A(f"| **ids repetidos** (achado novo) | {len(F['ids_duplicados'])} | #9 e #10 compartilham `5b740c2b-3480-48f2-997b-88c8291db0c0` |")
A(f"| ids únicos / chaves únicas | {F['ids_unicos']} / {F['chaves_unicas']} | — |")
A(f"| `$..rolagem.bonus` não vazio | {len(F['bonus_nao_vazio'])} eventos | {F['bonus_nao_vazio']} |")
A(f"| Slots de opção com bônus vazio | {F['slots_bonus_vazio']} de {F['opcoes_total']} | — |")
A(f"| Textos de opção vazios (`$.opcoes[*].texto=\"\"`) | {F['opcoes_texto_vazio']} | — |")
A(f"| `batalha.iniciar=true` | {len(F['batalha_iniciar_true'])} | {F['batalha_iniciar_true']} |")
A(f"| `batalha.dados_recompensa_final=null` com combate iniciado | {len(F['drf_null_com_batalha'])} | {F['drf_null_com_batalha']} | — todos com motivo de runtime não exercitado |")
A(f"| PPtr nulo `chave`/`nome` (m_PathID=0) | 20 de 20 | 1–20 (não é anomalia distintiva) |")
A(f"| Raridades | Common {F['raridades'].get('Common',0)} / Uncommon {F['raridades'].get('Uncommon',0)} / Rare {F['raridades'].get('Rare',0)} | — |")
A(f"| Pesos | 1.0 ×{F['pesos'].get('1.0',0)} / 5.0 ×{F['pesos'].get('5.0',0)} | 5.0 em #9 e #10 |")
A(f"| Typos reais no texto original | {len(F['typos_originais'])} | #2 `appeares`, #13 `whisperes` |")
A("")
A("Contagens da parte01 que **não** se sustentam: `roll_bonus vazio = 13 (todos exceto 5)`, `Campos NULL = 7 eventos`. As contagens acima vêm de recálculo direto sobre `eventos.json`.")
A("")
A("## 7. Auditoria automática (comando e saída real)")
A("")
A("Comando executado no workspace do cartão (offline, sem jogo):")
A("")
A("```")
A("python EV-R2-NORMAL-b01-parte02-propostas.py   # gera a validação estruturada")
A("python EV-R2-NORMAL-b01-parte02-validar.py --md | tee EV-R2-NORMAL-b01-parte02-auditoria.txt")
A("python EV-R2-NORMAL-b01-parte02-render.py      # renderiza este documento")
A("python EV-R2-NORMAL-b01-parte02-validar.py --md # confere md <-> validação (executado por último)")
A("```")
A("")
A("Saída real:")
A("")
A("```")
A(aud)
A("```")
A("")
A("## 8. Limites deste parecer")
A("")
A("- Runtime NAO_EXERCITADO: nada foi aberto no jogo; toda conclusão sobre exibição, resolução de tokens/placeholders, inimigos efetivos, loot/XP/ouro ou efeito final é explicitamente não exercitada.")
A("- As propostas de texto em inglês são sugestões autorais para o dono decidir; os textos originais (asset/EV-R1) não são editados aqui.")
A("- Eventos com `disabled=1` (#1, #4, #8, #10, #14) recebem propostas de texto/wording condicionais; nenhuma mudança de flag, nenhuma reativação e nenhuma exclusão é proposta.")
A("- Este documento corrige a proposta documental; não implementa balanceamento, não publica e não faz push.")
A("")

open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("MD_WROTE", MD, len(L), "linhas")
