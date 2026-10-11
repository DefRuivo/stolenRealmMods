# INT-R1 — parte 05: cartões criados, grafo de dependência e o que NÃO vale migrar

Nada foi migrado. Esta parte é o registro do que **passou a existir** no board por causa desta análise, e do
que ficou **deliberadamente de fora** — com motivo, como o dono pediu.

## 1. Cartões criados (6) — ids reais, verificados no board

| Código | Cartão (id) | Natureza | Modelo / provider | Balde que originou | Dependência explícita no grafo |
|---|---|---|---|---|---|
| C1 | `t_9fa61e7e` — **API-R1-I2: implementar a família UI do inventário na API própria** | implementação | `deepseek-flash` / `deepseek` | DUPLICADO→SIMPLIFICAVEL (RSTV) | `t_b7f6fc4a` (API-R1, done) |
| C2 | `t_2ea91249` — **arquitetura do contrato único entre SDK do kit (KIT-13) e núcleo da API** | arquitetura/decisão | `gpt-6.1-sol` / `openai-codex` | DUPLICADO (item 3 do checklist) | `t_adc1fbfa` (KIT-13) + `t_b7f6fc4a` (API-R1) |
| C3 | `t_3b7c681b` — **DBG-R2: proveniência/identidade no RoguelikeDebugger via gate da API** | implementação | `deepseek-flash` / `deepseek` | SIMPLIFICAVEL (debugger + censos) | `t_9e2325d7` (DBG-R1, em review) + `t_b7f6fc4a` — **gated** |
| C4 | `t_84ca88d4` — **RSTV migra a plumbing de UI para a família UI da API** | implementação | `deepseek-flash` / `deepseek` | SIMPLIFICAVEL→MIGRAR (adendo 2) | `t_9fa61e7e` (C1) — **gated** (a família não existe hoje) |
| C5 | `t_c6b435f8` — **instrumento de cobertura das tabelas do BetterTooltips via hook `ui.localized`** | implementação | `deepseek-flash` / `deepseek` | SIMPLIFICAVEL (adendo 2) | `t_b7f6fc4a` (API-R1) |
| C6 | `t_ee99ccc4` — **regenerar a parte chaveada dos dumps de tooltips a partir da tabela do LANG-R1** | implementação | `deepseek-flash` / `deepseek` | DEFASADO (item 1 do checklist) | `t_2a6474ff` (LANG-R1) — **gated** |

Grafo (produtor → consumidor, como o dono exige: dependência SEMPRE explícita):

```
t_b7f6fc4a API-R1 (done) ─┬─> C1 t_9fa61e7e (família UI) ──> C4 t_84ca88d4 (RSTV consome)
                         ├─> C3 t_3b7c681b (DBG-R2) <── t_9e2325d7 DBG-R1 (review)
                         ├─> C5 t_c6b435f8 (cobertura BetterTooltips)
                         └─> C2 t_2ea91249 (arquitetura) <── t_adc1fbfa KIT-13 (done)
t_2a6474ff LANG-R1 ──────────> C6 t_ee99ccc4 (dumps regenerados)
```

Notas de grafo que importam:
- **C4 é o único consumidor que passa a DEPENDER da API** — e ele só destrava quando C1 fechar. Antes disso a
  migração seria inventar API.
- **C3 e C6 nascem `gated`** (`gated_by` = `t_9e2325d7` e `t_2a6474ff`): não faz sentido regenerar dump de
  localização antes de o LANG-R1 fechar, nem mexer no debugger antes do parecer do DBG-R1.
- **C1 e C5 nascem `ready`** porque o pai (`t_b7f6fc4a`, API-R1) está `done`. Isso é intencional: são as duas
  frentes que **não** esperam ninguém.

Modelo por natureza, conforme a regra do controlador: as cinco implementações ficaram em
`deepseek-flash`/`deepseek`; a única decisão de arquitetura (C2) ficou em `gpt-6.1-sol`/`openai-codex`.

## 2. O que NÃO vale migrar — e por quê

### 2.1 Frentes que pareciam candidatas óbvias e foram recusadas

| Frente | Por que NÃO migrar |
|---|---|
| **O patch do `BetterTooltips` em `OptionsManager.Localize`** | O ponto de patch coincide com o hook `ui.localized`, mas o mod **reescreve o resultado** (`__result`) e a API 0.1.0 é observacional por contrato (`api/README.md:42,145-146`). Migrar o patch exigiria uma **extensão de forma** da API (postfix que transforma retorno) — frente nova, não migração. O que a API entrega de graça é o **instrumento de cobertura** (C5), e isso não muda o mod |
| **`BetterFont`** | Um patch de **gatilho**. Trocar por `Subscribe` custa uma dependência dura em cima de um gate **fail-closed**: basta o jogo atualizar para a API recusar hooks e o mod de fonte cair junto. Ganho ~0, risco real |
| **`BetterStats` e `BetterCombatText`** | Nenhum alvo deles está nos 4 hooks nem nas 7 famílias do inventário, e os dois **mutam** UI (fora do escopo observacional). O inventário não tem família de healthbar/dado/roll/tela de atributos |
| **Os 14 ganchos do `RoguelikeDebugger`** | O ganho da API para o debugger **não é trocar gancho** — é proveniência/identidade (C3). Reescrever 14 classes Harmony em cima de 4 hooks deixaria o instrumento **pior** |
| **O clique/navegação do `AUT4Probe`** (`t_139f714f`) | Não existe família de input no inventário e a API não dirige entrada. O defeito `0xc0000005` continua sendo do instrumento, sem relação com a API |
| **Os censos `docs/cobertura/*.csv`** | A hipótese do operador ("regerar em vez de manter à mão") está **refutada**: já são gerados por `tools/census.py` a partir do dump de boot, com a coluna curada preservada por `tools/preserva_curado.py`. O que faltava era **proveniência do instrumento**, e isso é o C3 — não um cartão novo de censo |
| **Os ~26 scripts de `tools/*.py`** | São offline (CSV/assembly). A API é in-game e observacional; não há interseção |
| **`docs/cobertura/auditoria-tooltips.md`** | Auditoria de **conteúdo/mecânica** (RV-8b, fechada em 2.280/2.280 vereditos). LANG-R1 não toca número de skill; não há o que regenerar |
| **Gates humanos vivos** (EV-R2×5, LANG-C1..C5, `t_b001720d` KIT-G4) | Aprovação humana. A API **não** muda a resolução de string (hook observacional em `OptionsManager.Localize`) nem decide conteúdo de evento |
| **KIT-14, KIT-14R, KIT14G-SEG1-RT, KIT14G-SEG2, KIT-00 e LEVEL-R2/R3** | São prova/entrega/aceite **do próprio kit e do mod de progressão**. O que muda é o **instrumento por baixo**, exatamente como o operador suspeitava — a entrega não perde sentido |
| **`ReloadProbe/`** | [DEFASADO] **já tratado**: `git check-ignore -v ReloadProbe/ReloadProbe.csproj` → `.gitignore:45:ReloadProbe/`; `git ls-files ReloadProbe` → **0**. Criar cartão seria trabalho fantasma |
| **Notas de IA da raiz** (`ITEM_INVENTORY.md`, `ITEM_MOD_INVENTORY.md`, `SKILL_INVENTORY.md`, `STATUS_INVENTORY.md`, `TOOLTIP_SWEEP.md`) | [DEFASADO] **já tratado** pelo INFRA-12 (`git ls-files` não as lista; superadas pelo censo). Só registro |
| **Famílias `Combat`, `Skills`, `Quests`, `Enemies`, `Data` do inventário** | **Não pedir implementação agora**: nenhuma frente viva precisa delas. Pedir API por antecipação é o oposto do objetivo desta tarefa (não manter dois mecanismos). `UI` é a única com consumidor nomeado (RSTV) |

### 2.2 Fora do escopo de INT-R1 (recomendação ao controlador, não cartão)

- **P0/P1/P2/P3 restantes do DBG-R1** (i18n do debugger, sidecars, presets de inimigo, localização, eventos,
  trace causal): `DBG-R1-parte07.md` §5 registra que **nenhum cartão de implementação foi criado** porque só
  existe o perfil `default`. A fatia de proveniência/identidade que a API simplifica virou o **C3**; o resto é
  do dono/controlador decidir. Motivo de não virar cartão aqui: o adendo pediu migração **para as ferramentas
  novas**, e esses itens não são simplificados por nenhuma delas.
- **Aceite humano dos 5 cartões LANG-C**: é do dono, não de agente.

## 3. Estado do board depois desta rodada

- Cartões vivos antes: **21** (parte 01 §2.1). Depois: **27** — os 21 + C1..C6; nenhum cartão existente foi
  alterado, arquivado ou reatribuído.
- Nada foi migrado, nenhum arquivo de mod foi editado, nenhum deploy, nenhum jogo.
- Artefatos desta análise: `docs/automacao/INT-R1-parte01.md` … `INT-R1-parte06.md` (novos; nenhum arquivo
  existente sobrescrito).

## 4. NAO_EXERCITADO desta parte

- Os 6 cartões criados **não foram executados**: os vereditos `[MIGRAR]`/`[SIMPLIFICAR]` são análise.
- C1 e C4 não têm prova de runtime: a família `UI` da API é contrato inventariado, não código
  (`api/README.md:67-68`).
