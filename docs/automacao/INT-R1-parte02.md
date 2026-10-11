# INT-R1 — parte 02: matriz frente × API × ganho × risco

Legenda de veredito (regra do adendo 2): `[MIGRAR]` · `[SIMPLIFICAR SEM DEPENDER]` · `[NADA A FAZER]`.
Eixo "API" = `API-0.1.0-hoje` (4 hooks, observacional) ou `API-inventário` (família existe só como
contrato em `api/docs/contract-inventory.json`, **não implementada** — ver parte 01 §1.2).

## 1. Matriz principal

| # | Frente | Como é hoje (prova) | Como fica com a API | Ganho | Risco | Custo | Veredito |
|---|---|---|---|---|---|---|---|
| F1 | **BetterTooltips** (9.251 linhas) | postfix próprio em `OptionsManager.Localize` (alvo igual ao hook `ui.localized`) + `Tooltip.ApplyDescriptionExpressions`, `Tooltip.ShowUniversalTooltip`, `Root.SendMessageWindowMessage`, `OverheadMessageDisplay.SpawnOverheadMessage`; **reescreve `__result`** e usa `Priority.High` (BT-9b) | API **não** pode reescrever resultado (`api/README.md:42,145-146`) → o patch próprio **fica**; o que a API passa a dar é um **canal de observação** dos textos servidos pelo jogo (`ui.localized`) para conferir cobertura das tabelas | Médio-baixo: cobertura/regressão das tabelas vira medição, não inspeção manual; zero mudança de comportamento | Baixo: assinante do `Signal` é isolado (`Contracts.cs:91-96`) | Baixo: um `Subscribe` + comparador contra `check_fix_keys.py`/`check_dupes.py` | **SIMPLIFICAR SEM DEPENDER** |
| F2 | **BetterFont** (1.721 linhas) | único patch = `OptionsManager.Localize` (só como **gatilho** para `FontUpdater.Ensure()`) | trocaria 1 postfix por 1 `Subscribe` ao hook `ui.localized` | ~0: não há boilerplate relevante a remover | **Alto relativo**: viraria dependência dura de `RealmApi`; o gate fail-closed da API fecha em qualquer update do jogo — e a fonte do mod cairia junto | Baixo em linhas, alto em acoplamento | **NADA A FAZER** |
| F3 | **BetterStats** (402 linhas) | postfix em `InventoryManager.UpdateStats` e `RoguelikeManager.UpdateAttributes`; lê `SavedMap[attr.Guid]` e o valor final | nenhum dos dois alvos está nos 4 hooks nem na família inventariada (`Data` = `CharacterData`, `ModConfig`, `ModData`) | 0 hoje | — | — | **NADA A FAZER** |
| F4 | **BetterCombatText** (1.844 linhas) | 9 alvos de UI: `BossHealthbar.set_BossCharacter`, `DiceRoller.StartRollVisuals`, `DiceRollingManager.RollDice`, `GUIManager.Update`, `Healthbar.Update`, `PlayerInfoWindow.ShowPlayerInfoWindow`, `StatusIcon.UpdateStatusIcon`, `Tooltip.ShowActionStatusTooltip`, `OptionsManager.Localize` | nenhum desses alvos existe no catálogo nem no inventário; o mod **muta a UI** (não é observação) | 0 | — | — | **NADA A FAZER** |
| F5 | **RoguelikeDebugger** (2.690 linhas, **14 classes Harmony em 10 arquivos**) | instrumento de observação; dump de boot alimenta os censos; `DBG-R1-parte07.md` §1: falta saber **qual DLL observou, se o dump terminou e o que não foi alcançado** | o gate `ApiIdentity.Matches` + a proveniência (`api/docs/target-game.json`) respondem exatamente a essa lacuna; os 4 hooks podem substituir os pontos que coincidem | Alto: diagnóstico deixa de ser "dump anônimo" e passa a ter identidade verificável (fail-closed) | Baixo se opcional: o debugger **não** pode ficar inútil quando a API não estiver instalada (regra do dono: dependência sempre explícita) | Médio: declarar dependência opcional, ler identidade, marcar nos sidecars | **SIMPLIFICAR SEM DEPENDER** (parcial, escopo fechado) |
| F6 | **RSTV** (6.946 linhas) | plumbing de UI à mão: `NativeUiHelpers` (clone de botão nativo, cópia de layout, bind de clique), `RunButton`, `RemovalWindowSkillsButton`, `LevelUpWindowButton`, `SkillTreeReadOnly`, `SkillTreesTab`; patches em `SkillTreeManager.Initialize`, `CharacterMenusManager.OpenWindow`, etc. | a família **UI** do inventário cobre isso literalmente: `UI.UIFactory` (`Clone`, `CloneComponent`, `CopyRectLayout`, `FindChild`, `BindClick`, `SetText`, `SetIcon`, `DisableChildLayouts`), `UI.ActionBarUI` (`AddButton`/`RemoveButton`/`UpdateIcon`), `UI.SkillTreeUI` (`AddTab`/`RemoveTab`/`HasTab`), `UI.MenuUI`, `UI.TooltipHelper` | Alto: o trabalho mais caro do mod (replicar UI nativa sem literal de posição) vira chamada de API; RSTV-30 é o caso-limite | Médio: muda comportamento de terceiros se a API evoluir; exige o cartão de implementação da família antes | Alto (a família não existe) — por isso dependência explícita em cadeia | **MIGRAR** (bloqueado pela família UI) |
| F7 | **ReloadProbe** (67 linhas) | **zero** `HarmonyPatch`; probe abandonado (INFRA-3/4/5 arquivadas: hot-reload não viável neste jogo) | nada a migrar — a função foi absorvida por `scratch/test-cycle.sh` + inspeção de log e, na observação, pelo `AUT4Probe` | — | — | Trivial | **DEFASADO** → remover do rastreamento |
| F8 | **Kit SDK KIT-13** (`Gumatos.KitSdk.V1`) | núcleo próprio de eventos/leitura/veredito/registro: `IExtensionV1`, `EventV1`, `ReadingV1`, `VerdictV1`, `RegistryV1` (`tools/automacao/kit13/SDK`, cabeçalho de `KIT-13-entrega-final.md`), sem Unity/BepInEx | `RealmApi.Core` tem o mesmo tipo de núcleo: `Signal<T>` + `HookNotification` + gate de identidade | Alto: **um** contrato versionado em vez de dois núcleos que vão divergir | Médio: unificar agora é decisão de arquitetura, não código | Médio: ponte (produtor→consumidor), não reescrita | **DUPLICADO** → decidir quem é dependência de quem |
| F9 | **AUT4Probe / CAP-1** (`tools/automacao/runtime/AUT4Probe`) | driver+coletor in-game: navega por roteiro, clica, grava `probe/recorder.json`; defeito aberto `t_139f714f` (clique sintético mata o jogo com `0xc0000005`) | a API cobre **observação** (4 pontos) e **não dirige input** (nenhuma família de input no inventário) | Médio: a parte observacional do probe pode emitir os eventos do kit pela API em vez de reflection própria | Baixo | Baixo-médio | **SIMPLIFICAR SEM DEPENDER** (observação; **o clique continua INTACTO** — a API não resolve `t_139f714f`) |
| F10 | **Censos** `docs/cobertura/*.csv` | **já** gerados por `tools/census.py` a partir do dump de boot do debugger; a única parte manual é a coluna de veredito, preservada por `tools/preserva_curado.py` | a API não gera censo; o que ela acrescenta é a **garantia de qual build observou** (fail-closed) | Baixo-médio: confiança na regeneração | Baixo | 0 (nenhuma mudança de mecanismo) | Ver parte 03 §3.2 (hipótese do operador **refutada**) |
| F11 | **Scripts de dump/revisão** (`tools/census.py`, `audit_tooltips.py`, `verify_tree.py`, `analisa_conferir.py`, `check_*.py` — ~26 scripts) | operam sobre CSVs e o assembly, 100% offline | nada muda: a API é in-game e observacional | 0 | — | — | **NADA A FAZER** |
| F12 | **Dumps de revisão de tooltips** (`DUMP-TOOLTIPS-REVISAO.md` 4.516 linhas, `DUMP-DEBUFFS-REVISAO.md`, `DUMP-PASSIVAS-REVISAO.md`) | gerados a partir do censo para revisão humana | `LANG-R1` entregou a tabela completa `chave→texto` pt-BR/EN (9.090 chaves) → para o **texto chaveado** o dump é regenerável da tabela | Médio: some a geração manual da parte chaveada | Baixo | Baixo | **DEFASADO PARCIAL** → regenerar a parte chaveada |
| F13 | `docs/cobertura/auditoria-tooltips.md` | auditoria de **conteúdo/método** das skills (RV-8b: checagens A..H, todas 0 exceto 1+2 candidatas); 2.280/2.280 vereditos fechados (`docs/cobertura/auditoria-cobertura.md`) | LANG-R1 não toca mecânica de skill — a auditoria não depende de texto localizado | 0 | — | — | **INTACTO** (a suspeita do operador é **refutada** — parte 03 §3.1) |
| F14 | **Gates humanos vivos** (EV-R2×6, LANG-C1..C5, `t_b001720d` KIT-G4) | aprovação humana de texto/evento/aceite | a API não muda a **resolução** de string: o hook `ui.localized` é postfix observacional sobre `OptionsManager.Localize` e não altera chave, tabela nem resultado | 0 | — | — | **INTACTO** |
| F15 | **KIT-14, KIT-14R, KIT14G-SEG1-RT, KIT14G-SEG2, KIT-00** | provas ponta-a-ponta do **próprio kit**; SEG1-RT prova `eventos > 0` em boot real; SEG2 é defeito do instrumento de clique | muda o **instrumento por baixo**, não a entrega | 0 (para a entrega) | — | — | **INTACTO** (confirma a suspeita do operador — parte 03 §3.5) |
| F16 | **LEVEL-R2 / LEVEL-R3** | mod `RoguelikeLevelProgression` + revisão independente; transpiler de `CanAdvance` | a API 0.1.0 não expõe progressão de nível; a família `Skills.SkillRegistry` do inventário é criação de skill, não teto de nível | 0 | — | — | **INTACTO** |
| F17 | **API-R1 base 0.1.0** | 4 hooks observacionais + gate; smoke 25/25; runtime `NAO_EXERCITADO` | é a **referência** desta revisão | — | — | — | É o insumo, não a frente |
| F18 | **Deploy opt-in / runbook** (`api/…/DeployToBepInEx`, `docs/automacao/API-R1-runbook-runtime.md`, `API-R1-I1-evidencias/`) | deploy condicionado a `-p:DeployToBepInEx=true`; perfil intocado (hash antes/depois igual) | nada muda | 0 | — | — | **INTACTO** |

## 2. Priorização por ganho × risco

1. **F8 — unificar os dois núcleos de contrato (DUPLICADO).** Maior ganho estrutural e o único que
   **cresce com o tempo**: cada frente nova escolhe um dos dois núcleos e a divergência se multiplica.
   Risco médio, e é decisão de arquitetura (não implementação).
2. **F6 — RSTV sobre a família UI (MIGRAR).** Maior ganho de código real (a plumbing de UI é a parte mais
   cara e mais frágil do mod), mas **não executável hoje**: depende de a família `UI` existir.
3. **F5 — debugger com identidade/proveniência (SIMPLIFICAR).** Ganho alto e imediato (resolve a lacuna nº 1
   do `DBG-R1-parte07.md` §1), risco baixo se a dependência for opcional.
4. **F12 — dump de tooltips regenerado da tabela LANG-R1 (DEFASADO parcial).** Ganho médio, risco baixo,
   e destrava trabalho humano repetitivo.
5. **F1/F9 — observação alimentando cobertura do BetterTooltips e do probe (SIMPLIFICAR).** Ganho médio-baixo,
   risco baixo; barato.
6. **F7 — remover o ReloadProbe do rastreamento.** Trivial, mas é dívida declarada.
7. **F2/F3/F4/F10/F11/F13/F14/F15/F16/F18 — nada a fazer.** Registrados na parte 03/05 com motivo.

## 3. O que a matriz **não** autoriza

- Nenhuma linha acima foi executada: `LIMITES: nao migrar nada nesta tarefa`.
- F6 e F8 não podem virar `[MIGRAR]` "para ontem": F6 exige a família `UI` implementada e F8 exige decisão
  de arquitetura de quem depende de quem. Por isso os dois cartões saem com **dependência explícita no
  grafo** (parte 05).
- F5 não autoriza deploy nem jogo: o cartão é de preparação offline.
