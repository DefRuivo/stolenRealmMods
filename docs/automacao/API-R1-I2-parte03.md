# API-R1-I2 (INT-R1-C1) — familia UI na API propria — parte 03 (fecho)

## 11. Aceite, item por item (tudo medido nesta rodada, 2026-10-11T04:38-03:00)

| Item do aceite | Resultado medido | Prova |
|---|---|---|
| 5 projetos Release, 0 avisos / 0 erros | `Core`, `Hooks`, `Plugin`, `Smoke`, `tools/Inspect`: `0 Aviso(s)` / `0 Erro(s)` cada | `api/docs/smoke-result.json` -> `buildsBeforeRun` |
| Smoke `Ran N tests; failures: 0` com >= 1 caso novo por tipo | `Ran 62 tests; failures: 0`, exit 0 (base: 25) | `api/docs/smoke-output.txt`; `smoke-result.json` -> `uiFamilyTests` (37) |
| Casos por tipo: alvo presente / ausente / assinatura divergente / isolamento de erro | 5 x `ui-<Tipo>-target-present`, `-target-absent`, `-member-absent`, `-signature-divergent`, `-unbound-fails-closed` (Tipo = UIFactory, ActionBarUI, SkillTreeUI, MenuUI, TooltipHelper) = 25 casos, + 12 de familia/estado | `api/docs/smoke-output.txt` |
| `grep -ril -E 'StolenRealmMod(ding|API)' api/ docs/automacao/API-R1-*.md` = 0 | **1** arquivo, e o proprio comando citado em `docs/automacao/API-R1-R1-parte01.md:28` (auto-referencia, artefato de outro cartao). Excluindo-o: 0. Nenhum arquivo desta entrega adiciona ocorrencia | comando abaixo |
| README atualizado | `api/README.md`: estrutura, "como usar" (familia UI + travas), tabela de alvos, secao nova "Familia UI (API-R1-I2)", smoke (62), "como atualizar" (8 passos) e "NÃO exercitado" (familia UI). `api/docs/README.md`: evidencias novas | `api/README.md`, `api/docs/README.md` |
| Runtime em jogo declarado NAO_EXERCITADO | `smoke-result.json` -> `scope.notExercised[3]` e `api/README.md` secao final | idem |
| Assinaturas EXATAS do inventario | 21 assinaturas / 5 tipos / 1 enum: `CONFORME`, 0 divergencias, com controle negativo acusando 2 problemas (nao-vacuidade) | `api/docs/ui-contract-diff.json` |

Comandos exatos do fecho:

    for p in Core Hooks Plugin Smoke tools/Inspect; do dotnet build api/$p/*.csproj -c Release; done
    api/Smoke/bin/Release/net472/RealmApi.Smoke.exe C:/dev/stolen-realm/lib/Assembly-CSharp.dll \
      C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll      # Ran 62 tests; failures: 0
    dotnet run --project api/tools/Inspect/Inspect.csproj -c Release --no-build -- ui \
      api/Plugin/bin/Release/netstandard2.1/RealmApi.dll \
      api/Core/bin/Release/netstandard2.0/RealmApi.Core.dll > api/docs/ui-contract.json
    python api/tools/check_ui_contract.py                                        # CONFORME; exit 0
    grep -ril -E 'StolenRealmMod(ding|API)' api/ docs/automacao/API-R1-*.md | wc -l   # 1 (ver tabela)

## 12. O que muda de natureza (registro exigido pelo escopo, item 5)

`AddButton`, `RemoveButton`, `UpdateIcon`, `AddTab`, `RemoveTab`, `BindClick`, `SetText`, `SetIcon`,
`Clone`, `CloneComponent`, `CopyRectLayout`, `DisableAllText`, `DisableChildLayouts`, `Destroy`,
`ShowTooltip`, `HideTooltip` **MUTAM** a UI do jogo: sao comportamento, nao observacao. Decisao de
arquitetura declarada (`api/README.md`, secao "Familia UI (API-R1-I2)"):

- a familia UI **nao** entra no barramento observacional (`RealmHooks.Observed`), nao e postfix Harmony e nao
  altera resultado/argumentos de metodo do jogo;
- ela e isolada por **vinculo explicito** (`UiFamily.Bind`, 17 requisitos resolvidos por metadados exatos),
  **opt-in de mutacao** (`allowMutation:true`) e **guarda de thread** (main thread do Unity);
- onde nao ha membro nativo 1:1, a API registra o pedido e **delega a mutacao visual ao hospedeiro nativo**
  do jogo; os caminhos visuais que exigem Unity puro ficam `NAO_EXERCITADO` (item 11 do README);
- `UIFactory.CopyRectLayout` tambem e mutacao (copia layout no alvo), embora nao esteja na lista do cartao.

## 13. Limites respeitados

Nada de RSTV (INT-R1-C4), nada instalado no perfil (`-p:DeployToBepInEx` nao usado), jogo nao aberto, nenhum
deploy, nenhuma edicao em `Assembly-CSharp.dll`, nenhum patch de modificacao de comportamento de jogo,
nada publicado. O plugin continua sem referenciar Assembly-CSharp (`no-game-assembly-dependency` verde) e o
alvo de deploy continua copiando **tres** assemblies (`UnityEngine.UI.dll` e referencia com `Private=false`
fornecida pelo proprio jogo).

## 14. Riscos e o que fica para a frente seguinte

1. **TextMeshPro**: `SetText`/`SetIcon` cobrem `UnityEngine.UI.Text`/`Image`. O jogo usa muito TMP; quem
   migrar o RSTV precisa ou do suporte a TMP (extensao declarada) ou de continuar escrevendo TMP a mao.
2. **Composicao visual**: criar o botao/aba do zero a partir de um prefab nativo nao esta implementado; hoje a
   API registra e pede a reconstrucao ao hospedeiro. Migrar o RSTV (INT-R1-C4) e o teste natural disso.
3. **Hospedeiros ao vivo**: o consumidor informa `UiHosts`; se o dono quiser descoberta automatica
   (`GUIManager.instance`, `LoadableUIWindow<SkillTreeManager>.Instance`, `OptionsManager` -> `MenuTabManager`),
   isso e uma frente separada (exige runtime em jogo).
4. **`api/` nao esta versionado** (`git status` -> `?? api/`): a entrega fica como arquivos na arvore de
   trabalho. Se o dono quiser historico/alca, isso e um passo separado (commit), fora deste cartao.
