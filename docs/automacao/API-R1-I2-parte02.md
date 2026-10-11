# API-R1-I2 (INT-R1-C1) — familia UI na API propria — parte 02

## 6. Onde o codigo vive (e por que NAO em Core)

Medido, nao suposto: `RealmApi.Core` mira `netstandard2.0` e os assemblies Unity do jogo
(`lib/UnityEngine.CoreModule.dll`, `lib/UnityEngine.UI.dll`) miram **netstandard2.1**. Uma referencia direta
falha na compilacao:

    CSC : error CS1705: Assembly "UnityEngine.CoreModule" ... usa "netstandard, Version=2.1.0.0" ...
          que tem uma versao mais recente do que o assembly referenciado "netstandard" 2.0.0.0

E o mesmo limite aparece em runtime: um executavel net472 que carregue `UnityEngine.CoreModule` morre com
`FileNotFoundException: netstandard, Version=2.1.0.0` (ensaio feito em scratch). Consequencia pratica:
assinar os 5 tipos com tipos Unity exige um projeto netstandard2.1, e o smoke (net472, com Harmony/MonoMod
reais) **nao** pode carregar nem o plugin netstandard2.1 nem os assemblies Unity. Logo:

| Camada | Onde | Conteudo |
|---|---|---|
| `Gumatos.RealmApi` (Core, netstandard2.0) | `api/Core/Ui/UiFamily.cs`, `api/Core/Ui/UiOperations.cs`, `api/Core/Skills/SkillTree.cs` | requisitos/vinculo/guardas/estado e delegacao — **sem UnityEngine**, exercitavel no CLR |
| `Gumatos.RealmApi.UI` (RealmApi.dll, netstandard2.1) | `api/Plugin/Ui/*.cs` | os 5 tipos publicos com as assinaturas EXATAS do inventario, usando UnityEngine |

O projeto do plugin passou a referenciar `UnityEngine.UI` (`api/Plugin/RealmApi.csproj`) e **nao** referencia
Assembly-CSharp (o teste `no-game-assembly-dependency` continua verde). Nao foi criado projeto novo: o aceite
exige 5 projetos Release.

## 7. Catalogo de requisitos (17) — todos medidos no jogo

`api/Core/Ui/UiFamily.cs::UiRequirements.All`. Cada membro foi conferido em `lib/Assembly-CSharp.dll` por
`ilspycmd -t <Tipo>` e e verificado de novo, a cada execucao do smoke, pelo teste
`actual-game-ui-requirements-metadata` (Mono.Cecil, assinatura exata) — **PASS**.

| Familia | Requisitos |
|---|---|
| `UIFactory` | host `GUIManager`; `GUIManager::instance` (prop. estatica -> GUIManager) |
| `ActionBarUI` | host `CurrentCharacterUI`; `CurrentCharacterUI::Instance` (estatica); `CurrentCharacterUI::ActiveSkillbar` (prop. -> Skillbar); `Skillbar::HasAvailableSlot` -> bool; `Skillbar::RefreshSkillBar` -> void |
| `SkillTreeUI` | host `SkillTreeManager`; `SkillTreeManager::IsNotNullAndIsActive` (estatica -> bool); `SkillTreeManager::UpdateSkillTreeItems` -> void |
| `MenuUI` | host `MenuTabManager`; `MenuTabManager::RefreshSelected` -> void |
| `TooltipHelper` | host `GUIManager`; `GUIManager::instance`; `GUIManager::tooltip` (campo -> Tooltip); `Tooltip::HideTooltip` -> void |

## 8. Regras de falha fechada implementadas

(ver `api/Core/Ui/UiFamily.cs`)

1. **Vinculo integral (`Bind`)**: resolve TODOS os 17 requisitos; alvo ausente = `MissingMemberException`,
   assinatura divergente = `MissingMethodException`, hospedeiro de tipo errado = `ArgumentException`.
   O vinculo so e publicado depois de tudo resolvido: **nao existe vinculo parcial**, e um `Bind` que falha
   nao altera o vinculo vigente.
2. **Chamada sem vinculo** = `InvalidOperationException` em qualquer metodo das 5 familias.
3. **Opt-in de mutacao**: `Bind(..., allowMutation:true)`. Sem ele, `AddButton`/`RemoveButton`/`UpdateIcon`/
   `AddTab`/`RemoveTab`/`BindClick`/`SetText`/`SetIcon`/`Clone`/`CloneComponent`/`CopyRectLayout`/
   `DisableAllText`/`DisableChildLayouts`/`Destroy`/`ShowTooltip`/`HideTooltip` lancam. `HasTab`/`FindChild`
   sao leitura: exigem vinculo e thread, nao exigem o opt-in.
4. **Thread**: o vinculo grava o `ManagedThreadId`; uso de outro thread lanca (UI do Unity nao e thread-safe).
5. **Hospedeiro ausente** (`UiHosts` sem o objeto da familia) = `InvalidOperationException` na familia.
6. **Sem stubs**: nenhum metodo publico tem corpo vazio — o smoke checa isso por metadados
   (`ui-public-surface-in-plugin-metadata`, instrucoes por metodo).

## 9. Evidencia medida nesta rodada (comandos reprodutiveis)

    dotnet build api/Core/RealmApi.Core.csproj   -c Release   # 0 avisos / 0 erros
    dotnet build api/Hooks/RealmApi.Hooks.csproj -c Release   # 0 avisos / 0 erros
    dotnet build api/Plugin/RealmApi.csproj      -c Release   # 0 avisos / 0 erros
    dotnet build api/Smoke/RealmApi.Smoke.csproj -c Release   # 0 avisos / 0 erros
    dotnet build api/tools/Inspect/Inspect.csproj -c Release  # 0 avisos / 0 erros
    api/Smoke/bin/Release/net472/RealmApi.Smoke.exe \
      C:/dev/stolen-realm/lib/Assembly-CSharp.dll \
      C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll
    # -> Ran 62 tests; failures: 0 ; exit 0   (base: 25 testes; +37 desta entrega)

Casos novos por tipo (5 tipos x 4 naturezas, exigidos pelo aceite) + delegacao real em CLR:
`ui-UIFactory-target-present|target-absent|member-absent|signature-divergent|unbound-fails-closed`,
idem `ActionBarUI`, `SkillTreeUI`, `MenuUI`, `TooltipHelper`; mais
`ui-mutation-requires-optin`, `ui-host-absent-fails-closed`, `ui-host-wrong-type-rejected`,
`ui-failed-bind-is-atomic`, `ui-thread-guard`, `ui-unbind-clears-family-state`,
`ui-tooltip-delegation-1para1`, `ui-action-bar-delegation`, `ui-skill-tree-delegation`,
`ui-menu-delegation`, `ui-public-surface-in-plugin-metadata`, `actual-game-ui-requirements-metadata`.

## 10. Onde trabalhar (medido, com correcao de rota)

A convencao do repo manda usar `git worktree add`. Foi tentado:

    git worktree add -b wt/t_9fa61e7e C:/dev/stolen-realm/.worktrees/t_9fa61e7e   # ok
    ls .worktrees/t_9fa61e7e/api                                                 # VAZIO

Motivo medido: `git status --short api/` -> `?? api/` — **o modulo `api/` da frente API-R1 esta UNTRACKED**
(nunca foi commitado). Worktree so materializa conteudo versionado, entao o worktree nasce sem a base da API
e o trabalho nao pode ser feito la sem duplicar/commitar trabalho de outro cartao. Decisao: implementar no
proprio `C:/dev/stolen-realm/api/` (caminhos reais abaixo), mantendo a arvore intacta quanto a historico.

Arquivos desta entrega:

- `api/Core/Ui/UiFamily.cs` (novo), `api/Core/Ui/UiOperations.cs` (novo), `api/Core/Skills/SkillTree.cs` (novo)
- `api/Plugin/Ui/UIFactory.cs`, `ActionBarUI.cs`, `SkillTreeUI.cs`, `MenuUI.cs`, `TooltipHelper.cs` (novos)
- `api/Plugin/RealmApi.csproj` (referencia a `UnityEngine.UI`)
- `api/Smoke/Program.cs` (37 testes novos + fixtures)
- `api/README.md`, `api/docs/*` (evidencias), `docs/automacao/API-R1-I2-parte01.md`, `-parte02.md`

Nota de conformidade com o aceite: o grep de vazamento
`grep -ril -E 'StolenRealmMod(ding|API)' api/ docs/automacao/API-R1-*.md` devolve **1** arquivo —
`docs/automacao/API-R1-R1-parte01.md`, que **cita o proprio comando** (auto-referencia; artefato de outro
cartao). Excluindo esse arquivo o resultado e 0, e nenhum artefato desta entrega adiciona ocorrencia.
