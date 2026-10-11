# INT-R1 — parte 04: revisão mod a mod (as duas ferramentas novas)

Método: para cada mod do repo, seis campos obrigatórios (a)..(f) do adendo 2. **A pergunta é só uma:** as
ferramentas novas (API própria do API-R1 e debugger aprimorado do DBG-R1) tornam isto mais simples, mais
barato ou mais confiável? **Nada aqui propõe mudar escopo ou comportamento de mod.**

Duas premissas medidas (parte 01):
1. A API 0.1.0 tem **4 hooks observacionais** e **não** altera argumento nem resultado.
2. O "debugger aprimorado" do DBG-R1 é **proposta auditada**, não código: as 7 partes terminam com
   "As propostas não estão implementadas" (`DBG-R1-parte07.md` §5) e **nenhum cartão de implementação foi
   criado**. Onde o campo (c) depender dele, isso está dito e o cartão correspondente é o C3.

Prova comum aos 7 mods: **nenhum** tem `BepInDependency` (grep por `BepInDependency` em cada pasta: 0
ocorrências) — todos são standalone hoje, e é isso que a coluna (d) tem de preservar.

## 1. BetterCombatText — 1.844 linhas

| Campo | Conteúdo |
|---|---|
| (a) hoje / mecanismo | Harmony direto em **9 alvos de UI**: `BossHealthbar.set_BossCharacter`, `DiceRoller.StartRollVisuals`, `DiceRollingManager.RollDice(int)`, `GUIManager.Update`, `Healthbar.Update`, `OptionsManager.Localize`, `PlayerInfoWindow.ShowPlayerInfoWindow`, `StatusIcon.UpdateStatusIcon`, `Tooltip.ShowActionStatusTooltip` (12 `HarmonyPatch` em `Patches.cs`+`DiagnosticoArranque.cs`+`Plugin.cs`). Não é observação: ele **muta a apresentação** |
| (b) com a API | Nada. Nenhum desses alvos está no catálogo (4 hooks) nem nas 7 famílias do inventário (`UI` = `UIFactory`/`ActionBarUI`/`MenuUI`/`SkillTreeUI`/`TooltipHelper`, nenhum de healthbar/dado/roll) |
| (c) com o debugger aprimorado | Nada direto: o dump do debugger não cobre healthbar/dado/roll. O achado DBG-R1 "traduzir o wire direto quebra consumidores" não se aplica (o mod não consome wire) |
| (d) dependência | **Continua standalone** |
| (e) ganho × risco/custo | Ganho **0**; risco/custo > 0 (mexer em mod estável sem retorno) |
| (f) veredito | **[NADA A FAZER]** — sem cartão |

## 2. BetterFont — 1.721 linhas

| Campo | Conteúdo |
|---|---|
| (a) hoje / mecanismo | Um **único** alvo: `OptionsManager.Localize` como **gatilho** de `FontUpdater.Ensure()` + varredura de `TMP_Text`. Nada mais é patcheado |
| (b) com a API | Trocaria 1 postfix por 1 `Subscribe` no hook `ui.localized` — o alvo é literalmente o mesmo (`api/Core/Contracts.cs:63`) |
| (c) com o debugger aprimorado | Nada: não é medição, é apresentação |
| (d) dependência | **Continua standalone.** Migrar criaria dependência dura de `RealmApi`; com o gate fail-closed, qualquer update do jogo desliga a API — e levaria o mod de fonte junto, exatamente quando o usuário precisa de legibilidade |
| (e) ganho × risco/custo | Ganho ~0 (1 patch, sem boilerplate relevante); risco de acoplamento + perda de robustez |
| (f) veredito | **[NADA A FAZER]** — sem cartão. Registro: existe **coincidência de alvo** com o hook `ui.localized` (e com o BetterTooltips); é duplicação benigna de ponto de patch, não de mecanismo — necessidades diferentes |

## 3. BetterStats — 402 linhas

| Campo | Conteúdo |
|---|---|
| (a) hoje / mecanismo | Postfix em `InventoryManager.UpdateStats` e `RoguelikeManager.UpdateAttributes`; lê `SavedMap[attr.Guid]` (valor puro) e `character[LevelableCharacterAttributesFinal[i].name]` (valor final) para escrever "BASE (COMBINADO)" |
| (b) com a API | Nada. `Data` no inventário é `CharacterData` (persistência por mod: `GetBool`/`Has`/`GetGuid`), `ModConfig`, `ModData` — leitura/gravação de dados de mod, **não** a tela de atributos |
| (c) com o debugger aprimorado | Nada hoje. `RoguelikeManager.UpdateAttributes` não está nos 14 ganchos do debugger; o debugger mede XP/loot/ouro/lifesteal/shrine/event-roll |
| (d) dependência | **Continua standalone** |
| (e) ganho × risco/custo | Ganho **0** |
| (f) veredito | **[NADA A FAZER]** — sem cartão |

## 4. BetterTooltips — 9.251 linhas

| Campo | Conteúdo |
|---|---|
| (a) hoje / mecanismo | Harmony próprio em `OptionsManager.Localize` (transforma/isenta o texto), `Tooltip.ApplyDescriptionExpressions`, `Tooltip.ShowUniversalTooltip`, `Root.SendMessageWindowMessage`, `OverheadMessageDisplay.SpawnOverheadMessage`; 11 arquivos de patch, `Priority.High` deliberado (BT-9b), 2 usos de `TargetMethod`/`AccessTools`. Ele **reescreve o resultado** do jogo |
| (b) com a API | O patch **fica**: `api/README.md:42,145-146` proíbe mudar resultado/argumentos nesta base. O ganho é outro: o hook `ui.localized` dá um **canal de observação** do texto servido pelo jogo, contra o qual as tabelas (`TextFixes`, `TextAppends`) podem ser conferidas por medição em vez de só por censo estático (`tools/check_fix_keys.py`, `tools/check_dupes.py`) |
| (c) com o debugger aprimorado | Indireto e real: as tabelas são validadas hoje contra o **censo** (dump de boot). Com proveniência de build (C3) a conferência passa a saber **de qual build** veio o texto, que é a falha silenciosa clássica quando o jogo muda |
| (d) dependência | **Continua standalone** (não pode virar dependente: precisa reescrever `__result`) |
| (e) ganho × risco/custo | Ganho médio-baixo (cobertura/regressão vira medição); risco baixo (`Signal.Publish` isola assinante exceção, `Contracts.cs:91-96`); custo baixo |
| (f) veredito | **[SIMPLIFICAR SEM DEPENDER]** — cartão **C6** |

## 5. RoguelikeDebugger — 2.690 linhas, 14 classes Harmony em 10 arquivos

| Campo | Conteúdo |
|---|---|
| (a) hoje / mecanismo | Harmoniza os getters de asset (`Game.get_Skills/get_Items/get_ActionStatuses/get_RoguelikePowerups`), `Game.EvalVoid`, `Character.GetActionDamage`, `Character.GetExpValue`, `GetValueByEnemyType`, `GameLogic.ApplyGoldModifiers/GetCharacterLootDropModifier/GetTotalExpValue`, `MessageWindowManager.CreateBattleLogMessage` + `FlameShrineProcPatch` (4 patches). O dump de boot é o que alimenta `docs/cobertura/*.csv` |
| (b) com a API | O ganho da API aqui **não é trocar gancho**: é o **gate de identidade/proveniência** (`ApiIdentity.Matches` + `api/docs/target-game.json`) e o barramento com isolamento de assinante. Isso responde à lacuna nº 1 da própria auditoria: "saber **qual DLL observou**, se o dump terminou, o que não foi alcançado e se uma leitura era realmente passiva" (`DBG-R1-parte07.md` §1) |
| (c) com o debugger aprimorado | É o objeto da auditoria P0..P3 (`DBG-R1-parte05-matriz.csv`: 8 P0/8 P1/3 P2/1 P3, propostas não implementadas). Achado que **não** é para consertar aqui mas precisa constar: a matriz Flame **não é observação passiva estrita** (chama `EvalVoid` e altera `MissingExpressions`) |
| (d) dependência | **Dependência explícita e OPCIONAL** de `RealmApi`: o debugger não pode ficar inútil quando a API estiver ausente ou desligada (`EnableHooks=false`) |
| (e) ganho × risco/custo | Ganho **alto** (diagnóstico deixa de ser anônimo; é a base para confiar na regeneração dos censos); risco baixo se opcional; custo médio |
| (f) veredito | **[SIMPLIFICAR SEM DEPENDER]** — cartão **C3** |

## 6. RoguelikeSkillTreeVisualizer — 6.946 linhas, 15 `HarmonyPatch`

| Campo | Conteúdo |
|---|---|
| (a) hoje / mecanismo | Harmony em `CharacterChoiceManager.ToggleSelectedCharacter`, `CharacterMenusManager.OpenWindow/CloseSkillTreeMenu`, `CurrentCharacterUI.InitSingleton`, `KeybindManager.Update`, `PlayerMovement.ProcessLeftMouseClick`, `RoguelikeManager.OpenSkillSelectWindow`, `RoguelikeSkillTreeRemovalWindow.Open`, `SkillTreeItem.ToggleAddToSkillToAddList`, `SkillTreeManager.OnDisable/Initialize/AcceptSkillChanges` + shortcuts. E **plumbing de UI escrito à mão** em `NativeUiHelpers.cs` (clone de botão nativo, cópia de layout, bind de clique), `RunButton`, `RemovalWindowSkillsButton`, `LevelUpWindowButton`, `SkillTreesTab`, `SkillTreeReadOnly` |
| (b) com a API | A família **`UI`** do inventário cobre literalmente o que o mod escreve à mão: `UI.UIFactory.Clone/CloneComponent/CopyRectLayout/FindChild/BindClick/SetText/SetIcon/DisableChildLayouts`, `UI.ActionBarUI.AddButton/RemoveButton/UpdateIcon` (é o RSTV-30: "botão que foi para a BARRA DE BAIXO"), `UI.SkillTreeUI.AddTab/RemoveTab/HasTab`, `UI.TooltipHelper`, `UI.MenuUI`. Além disso, o hook já existente `ui.skill-tree.updated` (`SkillTreeManager::UpdateSkillTreeItems`) dá o ponto de **observação** para provar o read-only |
| (c) com o debugger aprimorado | Nada direto do DBG-R1 (a auditoria é do debugger). O valor para o RSTV é o **hook de observação** do skill tree + o antirregressivo de "fechar o viewer nativo **comita**" (risco registrado no KANBAN, RSTV-1: l.48494/108137) |
| (d) dependência | **DEPENDENTE da API (declarar)** se migrar para a família `UI` — e a regra do dono é dependência sempre explícita |
| (e) ganho × risco/custo | Ganho **alto** (a plumbing de UI é a parte mais cara e mais frágil do mod); risco médio (a API passa a ser contrato de terceiro para o mod); custo alto — e **bloqueado hoje**: a família `UI` **não existe** (`api/README.md:67-68`) |
| (f) veredito | **[MIGRAR]** (condicional, escopo fechado) — cartão **C4**, filho do cartão **C1** (implementar a família `UI`) |

## 7. ReloadProbe — 67 linhas

| Campo | Conteúdo |
|---|---|
| (a) hoje / mecanismo | **Zero** `HarmonyPatch`, zero patch, um `Plugin.cs`. Probe de hot-reload abandonado (INFRA-3/4/5 arquivadas: o `Update()` do plugin não dispara neste jogo) |
| (b) com a API | Nada a migrar: a função (observar recarga) foi absorvida por `scratch/test-cycle.sh` e, na observação em jogo, pelo `AUT4Probe` |
| (c) com o debugger aprimorado | Nada |
| (d) dependência | Standalone **inerte** |
| (e) ganho × risco/custo | — |
| (f) veredito | **[DEFASADO]** — mas **já tratado**: `git check-ignore -v ReloadProbe/ReloadProbe.csproj` → `.gitignore:45:ReloadProbe/`, e `git ls-files ReloadProbe` → **0** arquivos. Nada a fazer, sem cartão (parte 03 §1) |

## 8. Resumo dos vereditos (7 mods)

| Mod | Veredito | Cartão |
|---|---|---|
| BetterCombatText | NADA A FAZER | — |
| BetterFont | NADA A FAZER | — |
| BetterStats | NADA A FAZER | — |
| BetterTooltips | SIMPLIFICAR SEM DEPENDER | C6 |
| RoguelikeDebugger | SIMPLIFICAR SEM DEPENDER | C3 |
| RoguelikeSkillTreeVisualizer | MIGRAR (condicional) | C4 (filho de C1) |
| ReloadProbe | DEFASADO (já tratado) | — |

## 9. NAO_EXERCITADO desta parte

- Nenhum mod foi compilado nesta rodada; nenhum foi instalado; o jogo não foi aberto.
- A migração do RSTV (C4) **não pode começar** antes de a família `UI` existir no código da API — o contrato
  está inventariado (`api/docs/contract-inventory.json`), mas implementação e runtime são `NAO_EXERCITADO`.
