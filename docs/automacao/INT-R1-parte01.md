# INT-R1 — parte 01: método, fontes e o que a API-R1 oferece HOJE

Cartão: `t_ecb8f32d` (INT-R1). Pai: `t_b7f6fc4a` (API-R1, done). Rodada: run 762.
Escopo desta rodada: **analisar e criar cartões**. Nenhuma migração executada, nenhum arquivo de mod
editado, nenhum deploy, jogo não aberto.

## 1. Método e regra de leitura

O aceite pede, por frente: (a) como é hoje; (b) como fica com a API; (c) ganho; (d) risco; (e) custo de
migração. Toda afirmação abaixo vem com **caminho de arquivo + linha/contagem** ou comando reprodutível.
O que não foi exercitável está marcado `NAO_EXERCITADO` com o motivo.

Esta parte fixa a premissa que decide quase todos os vereditos: **a API 0.1.0 é observacional**. Sem isso
não se entende por que a maioria dos candidatos "óbvios" a migração NÃO migra.

### 1.1 O que existe de fato na base 0.1.0 (prova)

| Prova | Arquivo | Conteúdo medido |
|---|---|---|
| Catálogo de hooks | `api/Core/Contracts.cs:58-66` | `HookCatalog.All` = **4** descritores: `game.awake`, `ui.skill-tree.updated`, `ui.localized`, `combat.turn-started` |
| Barramento | `api/Core/Contracts.cs:106-111` | `RealmHooks.Observed` é `Signal<HookNotification>`; `Emit` só **publica** |
| Regra de forma | `api/README.md:42` | "O pacote observa e **não** muda resultado nem argumentos do jogo — todo postfix é observacional" |
| Limite explícito | `api/README.md:145-146` | "Nada de patches de modificação de comportamento nesta base: a API 0.1.0 é observacional. Qualquer cancelamento/substituição de argumentos é uma frente separada" |
| Leitura pontual | `api/Core/Contracts.cs:113-126` | `RealmAccess.ReadProperty(assembly, typeName, propertyName, instance)` — só propriedade de leitura, sem cache de `UnityEngine.Object` |
| Gate de identidade | `api/Core/Contracts.cs:14-31` | `ApiIdentity.Matches(version, sha256)` fail-closed: appid 1330000, jogo 1.3.1, build 25240684, sha256 `8bb4a7c5…855a` |
| Estado dos hooks | `api/README.md:72-77` | `EnableHooks` padrão **false**; com `true` ainda exige versão **e** sha256 do `Assembly-CSharp` do processo atual |
| Smoke | `api/docs/smoke-result.json` | `ran: 25, failures: 0, exitCode: 0`; `notExercised`: carga pelo BepInEx, gameplay, perfil r2modman |

### 1.2 O que NÃO existe (e o adendo trata como se existisse)

`api/docs/contract-inventory.json` tem `counts = {types: 57, methods: 271, fields: 143, properties: 50,
events: 13}`, com as famílias `Combat` (10 tipos), `Skills` (12), `Quests` (13), `Enemies` (8), `UI` (5),
`Data` (3), `ContractReference` (6). Isso é **inventário de superfície inspecionada** (anonimizado por
metadados), **não implementação**: `api/README.md:67-68` diz literalmente que as famílias restantes
"não estão implementadas — não há stub silencioso e não há promessa de compatibilidade".

Comandos de reprodução usados nesta parte:

```bash
sed -n '58,126p' /c/dev/stolen-realm/api/Core/Contracts.cs
python -c "import json;d=json.load(open('api/docs/contract-inventory.json',encoding='utf-8'));print(d['counts'])"
```

**Consequência para o resto do relatório:** um veredito `[MIGRAR]` só é honesto quando (i) o ponto
necessário já está nos **4 hooks**, ou (ii) o ponto é da família inventariada **e** o cartão de migração
depende de um cartão de **implementação dessa família** na API. Toda migração que exigir alterar o
comportamento do jogo (reescrever `__result`, cancelar dano, mudar argumento) está **fora** da 0.1.0.

## 2. Inventário do que está vivo (medido nesta rodada)

### 2.1 Board (fonte: `~/.hermes/kanban.db`)

`553` cartões no banco: `424` arquivados, `108` done, **`21` vivos** — `12` blocked, `4` running,
`3` todo, `1` review, `1` triage. Comando:

```bash
python -c "import sqlite3;c=sqlite3.connect(r'C:\Users\Pichau\AppData\Local\hermes\kanban.db');[... ]"
```

Vivos: EV-R2×5 (`t_004ed4b0`, `t_34205427`, `t_55517882`, `t_8e74c724`, `t_b10171fa`), LANG-C1..C5
(`t_71e4b22a`, `t_15176486`, `t_0bddb861`, `t_ec66f0bb`, `t_4da3d8a7`), `t_b001720d` KIT-G4,
`t_9e2325d7` DBG-R1 (review), `t_2a6474ff` LANG-R1 (running), `t_cda5afa8` LEVEL-R3,
`t_d87ea54d` API-R1-R1, `t_ecb8f32d` INT-R1, `t_9ce7d260` KIT-14R, `t_a1f38855` KIT-14,
`t_a41dd22d` KIT14G-SEG1-RT, `t_dc6125a6` KIT-00 (triage), `t_139f714f` KIT14G-SEG2.

### 2.2 Repo (medido nesta rodada)

| Frente | Caminho | Tamanho medido |
|---|---|---|
| 7 mods | `BetterCombatText/`, `BetterFont/`, `BetterStats/`, `BetterTooltips/`, `RoguelikeDebugger/`, `RoguelikeSkillTreeVisualizer/`, `ReloadProbe/` | 1.844 / 1.721 / 402 / 9.251 / 2.690 / 6.946 / 67 linhas de `.cs` |
| API própria | `api/` (Core, Hooks, Plugin, Smoke, tools/Inspect, docs) | `Contracts.cs` 127 · `HookInstallation.cs` 69 · `RealmApiPlugin.cs` 45 · `Program.cs` 106 |
| Kit de automação | `tools/automacao/` (18 subpastas, incl. `runtime/AUT4Probe`, `kit13/SDK`) | — |
| Censos | `docs/cobertura/*.csv` | skills 452 · skills-detalhe 454 · status 561 · itens 906 · afixos 286 · acoes 288 · powerups 80 · invocacoes 19 (linhas físicas, contando cabeçalho) |
| Dumps de revisão | `docs/cobertura/DUMP-TOOLTIPS-REVISAO.md` (4.516 linhas), `auditoria-tooltips.md` (3.528 bytes), `DUMP-DEBUFFS-REVISAO.md`, `DUMP-PASSIVAS-REVISAO.md` | — |
| Ferramentas de censo | `tools/census.py` (lê o dump de boot do RoguelikeDebugger no `LogOutput.log`), `tools/preserva_curado.py` | — |
| Entregas em anexo (fora da árvore) | `…\kanban\attachments\t_2a6474ff\LANG-R1-entrega-final.zip` (23.660.374 B), `localizacao-ptbr.csv` (3.355.263 B), `relatorio-suspeitos.md` (1.057.456 B); `…\attachments\t_9e2325d7\DBG-R1-entrega.zip` (98.550 B), `DBG-R1-parte07.md` | — |

### 2.3 Duas entregas recentes que mudam o cálculo

**LANG-R1 (`t_2a6474ff`)** entregou a tabela completa de localização: `9090/9090` chaves pt-BR, `8097`
entradas, união com EN de `9095` chaves, colunas
`id; presente_tabela_ptbr; chave; en; ptbr; num_entradas; alertas; contextos; chave_json; ptbr_json;
decisao_dono; texto_aprovado; observacoes` (prova: cabeçalho do CSV em anexo; `relatorio-suspeitos.md`
com contagens por regra: 1293 chave_sem_traducao, 268 identico_ingles, 59 tags_quebradas, 26
tags_divergentes, 371 texto_longo). Declarado `NAO_EXERCITADO`: jogo/runtime, renderização/layout e
revisão linguística humana.

**DBG-R1 (`t_9e2325d7`)** entregou **auditoria**, não implementação: 7 partes, matriz de 20 linhas
(8 P0 / 8 P1 / 3 P2 / 1 P3), catálogo de 654 ocorrências string em 12 fontes C# e **14 classes Harmony
em 10 arquivos** (`DBG-R1-parte07.md` §3). Achados que tocam esta tarefa:
- "**saber qual DLL observou, se o dump terminou, o que não foi alcançado e se uma leitura era realmente
  passiva**" (`DBG-R1-parte07.md` §1) — é exatamente o que o gate de identidade da API-R1 responde.
- A matriz Flame **não é observação passiva estrita** (chama `EvalVoid` e altera `MissingExpressions`).
- "Traduzir o wire direto quebra consumidores: `nivel→level` perdeu o nível no parser real".
- **Não criou cartões de implementação** (só existe o perfil `default`) — as propostas P0..P3 estão
  órfãs de dono. Parte 03 e 05 deste relatório tratam disso.

## 3. NAO_EXERCITADO desta parte

- Runtime: BepInEx carregando `RealmApi` (ou qualquer mod) no processo do jogo — **não exercitado**
  (nenhuma rodada de jogo autorizada; `api/docs/smoke-result.json` declara o mesmo).
- Deploy no perfil r2modman: **não exercitado** (opt-in `-p:DeployToBepInEx=true` não usado).
- Comportamento da 4ª hook (`combat.turn-started`) em jogo: **não exercitado** (só metadados e smoke CLR).
- Contagens do debugger em jogo: só foram contadas as fontes C# e os CSVs atuais, por leitura
  (`DBG-R1-parte07.md` §5 admite o mesmo).
