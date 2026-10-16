# DEP-REV — dependências reais dos nove pacotes

Data: 16/10/2026. Cartão: `t_6ac74f0f`. Repositório: `C:/dev/stolen-realm`.

## 1. Resultado e escopo

**Dois manifests corrigidos, sem bump, build, instalação ou publicação:**

1. `RoguelikeSkillTreeVisualizer/manifest.json:6-9`: acrescentada `DefRuivo_StolenRealmMods-RealmApi-0.1.0`. O RSTV já exige a API no código e no atributo BepInEx; faltava a instalação automática pelo gerenciador.
2. `BetterCombatText/manifest.json:6-8`: removida `DefRuivo_StolenRealmMods-BetterFont-1.0.3`. Era uma dependência de pacote sem dependência obrigatória de código. Os dois mods podem atuar nos mesmos componentes de texto, mas isso não faz o BCT chamar o BetterFont. A combinação visual permanece possível, não obrigatória.

Os outros sete manifests foram conferidos e mantidos. Todos preservam `BepInEx-BepInExPack-5.4.2305`. Não foi adicionado vínculo artificial com a API comunitária `biblioteca-de-terceiros`.

**Grafo obrigatório local corrigido não significa lote publicável hoje.** A versão exata do RealmApi ainda responde HTTP 404 e o packer não reconhece o nome. Os gates oficiais de dependências falharam, corretamente, por esse pré-requisito não publicado. A correção não é apagar a dependência do RSTV: é preparar/publicar a API antes, nas tarefas seguintes e somente com autorização.

### Método e cobertura

- Examinados os oito diretórios de mods e os projetos `api/Core`, `api/Hooks`, `api/Plugin`: **93 arquivos `.cs`/`.csproj`**, contados programaticamente (6 BCT, 2 BF, 9 BP, 2 BS, 12 BT, 14 RD, 15 RSTV, 19 ULLP, 14 API).
- Cruzados: chamadas em fonte, todos os `Reference`/`ProjectReference`, namespaces/imports, `BepInDependency`, reflexões/carregamento de assemblies e menções aos demais mods. Comentários e textos de log não foram contados como chamada.
- Lidos com Mono.Cecil, sem executar plugins, os metadados de **11 assemblies Release existentes**: os oito mods e os três assemblies da API. Corroboram o grafo de fontes; não são um rebuild nem uma prova de runtime/atualidade de todos os binários.
- `bin`, `obj`, testes/harnesses, backups e probes em `tools/automacao` não são mods de distribuição desta tabela. Há consumidores reais da API nos probes/bridges do kit (por exemplo `tools/automacao/kit13/ApiBridge/RealmHooksBinding.cs` e `tools/automacao/runtime/LocalizedProbe/LocalizedProbePlugin.cs`); não são pacotes com manifest entre os nove alvos e não justificam dependência dos mods de jogador.
- Inventário completo, hits com linha e referências XML estão em `source-inventory.json`, `dependency-source-hits.json` e `project-references.json` nas evidências do cartão.

## 2. Tabela código versus manifest

Legenda: **B** = `BepInEx-BepInExPack-5.4.2305`; **F** = `DefRuivo_StolenRealmMods-BetterFont-1.0.3`; **A** = `DefRuivo_StolenRealmMods-RealmApi-0.1.0`.

Todos os plugins precisam do loader BepInEx e de assemblies providos pelo jogo/Unity. Harmony vem no BepInExPack; não é necessário inventar outro pacote para `0Harmony.dll`. Os requisitos do jogo não são pacotes Thunderstore.

| Mod / versão local preservada | Dependência obrigatória de código, além do jogo/Unity | Manifest antes | Descasamento antes | Manifest depois / ação |
|---|---|---|---|---|
| BetterCombatText 0.1.2 | BepInEx + Harmony; nenhum assembly de outro mod | B + F | Declara **a mais** F em relação ao grafo obrigatório | **B**; removida F |
| BetterFont 1.0.3 | BepInEx + Harmony; nenhum outro mod | B | Nenhum | B; mantido |
| BetterPortuguese 0.1.0 | BepInEx + Harmony; componentes Core/Runtime são fontes do próprio assembly | B | Nenhum | B; mantido |
| BetterStats 1.0.2 | BepInEx + Harmony; nenhum outro mod | B | Nenhum | B; mantido |
| BetterTooltips 0.1.4 | BepInEx + Harmony; nenhum outro mod | B | Nenhum | B; mantido |
| RoguelikeDebugger 0.1.2 | BepInEx + Harmony; integração **opcional por reflexão** com `ApiIdentity` | B | Nenhum hard faltante; a integração opcional não exige A | B; mantido |
| RoguelikeSkillTreeVisualizer 0.3.3 | BepInEx + Harmony + **RealmApi.dll e RealmApi.Core.dll**; plugin API mínimo 0.1.0 | B | Declara **a menos** A; hard já existe no plugin | **B + A**; adicionada A |
| RoguelikeUnlimitedLevelProgression 0.1.1 | BepInEx + Harmony; nenhum outro mod | B | Nenhum | B; mantido |
| RealmApi 0.1.0 (`api/manifest.json`) | BepInEx; plugin → Core + Hooks; Hooks → Core + Harmony, todos internos ao pacote/API e loader | B | Nenhum pacote externo faltante | B; mantido; distribuir os três assemblies juntos |

A classificação de F como excedente é sobre **necessidade de código**, não erro de sintaxe nem versão inexistente. O README do BCT havia escolhido instalar os dois juntos como política de apresentação; isso está separado da exigência técnica e explicitado na seção 4.

### Evidência de BepInEx/Harmony por mod

| Mod | Uso real do loader e do patcher |
|---|---|
| BetterCombatText | `BetterCombatText/Plugin.cs:27-28` (`BepInPlugin`, `BaseUnityPlugin`); `:116` (`new Harmony`) |
| BetterFont | `BetterFont/Plugin.cs:65-66`; `:209` (`new Harmony`) |
| BetterPortuguese | `BetterPortuguese/Plugin.cs:16-17`; `:66,77` (`new Harmony`, `Patch`) |
| BetterStats | `BetterStats/Plugin.cs:25-26`; `:50` (`new Harmony`) |
| BetterTooltips | `BetterTooltips/Plugin.cs:22-23`; `:57` (`new Harmony`) |
| RoguelikeDebugger | `RoguelikeDebugger/Plugin.cs:15-16`; `:83` (`new Harmony`) |
| RSTV | `RoguelikeSkillTreeVisualizer/Plugin.cs:49,57`; `:285` (`new Harmony`) |
| ULLP | `RoguelikeUnlimitedLevelProgression/Plugin.cs:16-17`; `:51` (`new Harmony`) |
| RealmApi | `api/Plugin/RealmApiPlugin.cs:12-14`; `api/Hooks/HookInstallation.cs:18,40` (`new Harmony`, `Patch`) |

Os metadados dos plugins apontam para `BepInEx, Version=5.4.23.5`; os consumidores Harmony e `RealmApi.Hooks` apontam para `0Harmony, Version=2.9.0.0`. Referências de compilação a Unity/TMP/Sirenix/Assembly-CSharp são bibliotecas locais do jogo, não outros mods. Não devem ser distribuídas nem traduzidas em dependências de pacotes fictícios.

## 3. Prova das arestas reais

### 3.1 RSTV → RealmApi: hard, não comentário

O atributo em `RoguelikeSkillTreeVisualizer/Plugin.cs:56` é `[BepInDependency(ApiGuid, ApiVersionMinima)]`. As constantes em `:63,67` são `com.gumatos.realmapi` e `0.1.0`. O construtor BepInEx com versão estabelece dependência hard e versão mínima (fonte oficial [S5], linhas 117-124 da cópia auditada).

Referências de compilação reais: `RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj:77-84` aponta para `RealmApi.dll` e `RealmApi.Core.dll`, ambas `Private=false`. Por isso a DLL da API não é copiada para o pacote RSTV: o pacote próprio deve fornecê-la.

**Todos os pontos de uso direto da API pela ponte** em `RoguelikeSkillTreeVisualizer/RstvApiUi.cs`:

| Linhas | Uso real | Assembly fornecedor |
|---|---|---|
| 61,74 | `UiFamily.IsBound` | RealmApi.Core |
| 81-87 | `new UiHosts` e `GuiManager` | RealmApi.Core |
| 91 | `UiFamily.Bind(typeof(GUIManager).Assembly, hosts, allowMutation: true)` | RealmApi.Core |
| 116 | `UIFactory.Clone(molde, pai, nome)` | RealmApi |
| 131 | `UIFactory.BindClick(alvo, acao)` | RealmApi |

Os `using` em `:3-4` identificam namespaces, mas a prova não depende deles: são as chamadas acima que exigem os assemblies. A string de log em `:95` isoladamente não provaria nada.

**Todos os chamadores da ponte** (não só um wrapper morto):

- `RoguelikeSkillTreeVisualizer/RunButton.cs:191`: clone do botão da run.
- `RoguelikeSkillTreeVisualizer/RemovalWindowSkillsButton.cs:232,280`: clone e listener.
- `RoguelikeSkillTreeVisualizer/SkillTreesWindow.cs:435,547`: clones de título/botão.
- `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs:1334,1386`: clone e clique dos botões de classe.

No binário Release existente, Mono.Cecil confirmou as referências `RealmApi`/`RealmApi.Core` 0.1.0.0 e o atributo com os argumentos `com.gumatos.realmapi`, `0.1.0`. Não há referência direta de RSTV a `RealmApi.Hooks`; ela é transitiva pelo pacote API.

### 3.2 RoguelikeDebugger ⇢ RealmApi: uso real, mas opcional

Não é correto descartar como simples string o `GetType("Gumatos.RealmApi.ApiIdentity", ...)` em `RoguelikeDebugger/Proveniencia.cs:395`:

- `:74` chama `SondaApi` no fluxo de proveniência.
- `:390-395` percorre assemblies **já carregados** e busca o tipo.
- `:409-413` lê as constantes `Version`, `AssemblySha256`, `SteamBuildId`, consulta config e chama `MatchesDaApi`.
- `:438,447,451` resolve/lê os campos; `:467-474` resolve `Matches` e faz `MethodInfo.Invoke`.
- `:493` aponta ao `.cfg` da API, outra integração real de diagnóstico.

Mas `:371` inicia com `Identidade="local"`, `:403-406` retorna sem erro se o tipo não existir e `:425-429` guarda falhas de reflexão. `:418-420` só escolhe a identidade API quando `EnableHooks` é `sim`.

O `.csproj` não referencia RealmApi; o assembly RD também não tem `AssemblyRef` da API nem `BepInDependency`. Portanto o debugger pode funcionar sem a API e a lista de dependências hard permanece só B. Uma declaração `SoftDependency` poderia ordenar carregamento numa evolução futura, mas não existe hoje e não foi adicionada: isso seria alteração de código fora do escopo.

### 3.3 Assemblies internos de RealmApi

- `api/Plugin/RealmApi.csproj:10-11`: projetos Core e Hooks.
- `api/Hooks/RealmApi.Hooks.csproj:5`: projeto Core e referência ao Harmony do loader.
- `api/Plugin/RealmApiPlugin.cs:29,31`: chamada real de `ApiIdentity.Matches` (Core), `HookInstallation.Install` (Hooks) e `HookCatalog.All` (Core); `:39` descarta a instalação.
- `api/Hooks/HookInstallation.cs:21,57`: usa o contrato `HookDescriptor` e publica via `RealmHooks.Emit`, ambos Core.
- Na família UI, o plugin chama Core: `api/Plugin/Ui/UIFactory.cs:30,41,51,64,73,83,92,103,111,119,126`; `ActionBarUI.cs:18,24,30`; `MenuUI.cs:17,23`; `SkillTreeUI.cs:17,23,29`; `TooltipHelper.cs:18,27` (todos sob `api/Plugin/Ui/`). São `UiFamily`/`UiOperations`, não chamadas a outro mod de jogador.

O Core não depende de outro mod/loader (só netstandard). Core e Hooks **não são dois pacotes Thunderstore independentes**. O requisito de composição é entregar `RealmApi.dll`, `RealmApi.Core.dll`, `RealmApi.Hooks.dll` juntos em `plugins/RealmApi/`; não adicionar dependências inexistentes `RealmApi_Core`/`RealmApi_Hooks`. O alvo opt-in já enumera os três em `api/Plugin/RealmApi.csproj:35-37`.

## 4. Arestas falsas e o caso BetterFont

**Não foi encontrada chamada entre BCT e BetterFont, em qualquer direção.** BCT não tem referência XML/AssemblyRef ao BetterFont, atributo de dependência, reflexão por nome nem import do namespace. O único hit nominal em fonte BCT é `BetterCombatText/Plugin.cs:101`, um comentário sobre o padrão de patching adotado no repositório.

O caminho real do efeito está em `BetterCombatText/TextStyler.cs:51,64,84,94-104,114-127`: trabalha diretamente com `TMP_Text`, material, shader e propriedades de contorno/sombra. Não chama um tipo BetterFont. A mudança da fonte pelo BF e o transporte de estilo podem interagir com os mesmos objetos Unity, mas essa convivência não é vínculo de assemblies.

Outras menções que **não criam dependência**:

- `BetterFont/Plugin.cs:205,276`: comentários comparando padrão de patching com RSTV/BetterTooltips.
- `BetterStats/Plugin.cs:45,118`: mesma espécie de comentário.
- `BetterTooltips/Patches/AtributoPercentualPatch.cs:52-53`, `ConvercaoAtributoPatch.cs:25,216`, `ReaperTollPatch.cs:46`, `ShrineAuraPatch.cs:128-129,1191,1337`: referências explicativas a BetterStats/debugger; não chamadas aos seus tipos.
- `RoguelikeDebugger/Plugin.cs:41,77,156` e `Patches/FlameShrineProcPatch.cs:130`: precedentes/comparações, não uso de API ou BetterTooltips.
- `RoguelikeSkillTreeVisualizer/Patches.cs:714`, `RunButton.cs:694`, `RunTargets.cs:101`: comentários sobre precedentes/diagnóstico.

**Resíduo documental conhecido:** `BetterCombatText/README.md:9` diz “Needs … BetterFont” e `:43-49` descreve a dependência/integração (inclusive menciona 1.0.2 enquanto o manifest antigo apontava 1.0.3). Isso explica a política anterior, não prova obrigação de código. O README não foi alterado nesta tarefa, focada em manifests; a filha `t_d00f2bc6` recebeu comentário explícito para alinhá-lo como integração opcional na preparação da nova versão. Não se deve empacotar essa divergência como se a documentação estivesse coerente. CHANGELOG pertence à tarefa paralela `t_a115a139` e não foi editado por este executor.

## 5. Grafos

Seta `X → Y`: X **precisa** de Y. Seta pontilhada: integração opcional.

```text
BetterCombatText ------------------→ BepInExPack 5.4.2305
BetterFont ------------------------→ BepInExPack 5.4.2305
BetterPortuguese ------------------→ BepInExPack 5.4.2305
BetterStats -----------------------→ BepInExPack 5.4.2305
BetterTooltips --------------------→ BepInExPack 5.4.2305
RoguelikeDebugger -----------------→ BepInExPack 5.4.2305
RoguelikeUnlimitedLevelProgression → BepInExPack 5.4.2305
RealmApi --------------------------→ BepInExPack 5.4.2305
RoguelikeSkillTreeVisualizer -------→ BepInExPack 5.4.2305
RoguelikeSkillTreeVisualizer -------→ RealmApi 0.1.0
RoguelikeDebugger ..................→ RealmApi (sonda opcional)
```

Grafo interno do pacote API:

```text
RSTV.dll → RealmApi.dll → RealmApi.Hooks.dll → RealmApi.Core.dll
    └───────────────────────────────────────→ RealmApi.Core.dll
                RealmApi.dll ───────────────→ RealmApi.Core.dll
                RealmApi.Hooks.dll ─────────→ 0Harmony.dll (BepInExPack)
```

Todos os plugins também têm requisitos de jogo/Unity; esses foram omitidos do desenho de **pacotes** para não confundi-los com mods instaláveis. Não há ciclo entre pacotes, aresta obrigatória BCT→BF, aresta BF→BCT nem pacote API→RSTV.

## 6. BepInEx: pacote, perfil e exigência da API

### A versão está certa nos nove manifests? Sim

São representações diferentes do **mesmo build**, não um typo:

- Thunderstore: `BepInEx-BepInExPack-5.4.2305`.
- Assembly e boot do loader: `BepInEx 5.4.23.5`.
- `%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/mods.yml:2,16-20`: pack instalado 5.4.2305 e habilitado.
- `.../BepInEx/LogOutput.log:1`: boot informa 5.4.23.5. O cabeçalho contém uma data do executável, não uma prova da data desta auditoria. O log antigo não foi usado como prova de versão atual dos plugins.

Para não depender só do YAML/log, comparei três arquivos: `lib/BepInEx.dll`, o `BepInEx/core/BepInEx.dll` do perfil e o extraído do ZIP remoto da versão exata 5.4.2305. Todos têm assembly version **5.4.23.5** e SHA-256 idêntico:

```text
8255b28902886085c578b9e427d3073c97002db85176d2090cdeda90ef14ce70
```

O ZIP foi baixado **apenas para o workspace**, sem instalação. A API remota da versão exata retornou HTTP 200; o endpoint por pacote também informou 5.4.2305 como `latest` nesta consulta, em 16/10/2026 às 16:21 UTC. A justificativa principal é a identidade do pack com o perfil e as referências de build, não simplesmente ser a última versão.

### RealmApi precisa de outra versão mínima especial de BepInEx?

Não foi encontrada guarda de versão própria do loader em `RealmApiPlugin`, `Contracts` ou projetos. O plugin herda `BaseUnityPlugin`, usa configuração/log do BepInEx 5, e compila contra a DLL 5.4.23.5. Portanto mantém-se o pack **verificado**, 5.4.2305. Não foi inventado requisito de BepInEx 6 nem provada compatibilidade com builds anteriores. A versão mínima **0.1.0** do atributo do RSTV refere-se ao plugin RealmApi, não ao loader.

### E o hash do Assembly-CSharp?

O gate observacional real está em `api/Plugin/RealmApiPlugin.cs:21-31`:

1. Hooks desligados por padrão (`Safety.EnableHooks=false`): retorna sem instalação.
2. Com opt-in: calcula SHA-256 do assembly do jogo carregado.
3. Chama `ApiIdentity.Matches(Application.version, hash)`; divergência recusa todos os hooks.

Em `api/Core/Contracts.cs:19-26`, o alvo é:

```text
GameVersion = 1.3.1
SteamBuildId = 25240684
AssemblySha256 = 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a
```

`Matches` compara **versão + hash**, não consulta o SteamBuildId. Calculei o hash da `lib/Assembly-CSharp.dll` e da DLL instalada em `E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed/Assembly-CSharp.dll`: ambos coincidem com o alvo. Isso não é um novo teste em jogo.

**Não virar dependência Thunderstore.** Dependências são referências de pacote com namespace/nome/versão existente, não hashes de DLL proprietária, versão da Steam nem `Assembly-CSharp`. Preservar/documentar o gate runtime e não distribuir a DLL do jogo. A família UI tem gate **separado**, por membros/assinaturas e opt-in de mutação em `api/Core/Ui/UiFamily.cs:174-204,221-226`; RSTV usa `Bind` em `RstvApiUi.cs:91`. Usar a UI não exige ligar os hooks observacionais nem transforma o hash em dependência instalável.

## 7. Ordem de envio, item por item

**É uma ordem técnica para candidatos elegíveis, não autorização para publicar os nove.** As versões abaixo são as atuais auditadas; não foram aumentadas. Onde a versão já existe, não tentar reenviá-la: a preparação posterior decide bump, textos e gates. Pular os inalterados.

Pré-requisito externo: `BepInEx-BepInExPack-5.4.2305` já existe (HTTP 200); não é upload nosso.

| Ordem proposta | Pacote / versão auditada | Justificativa e condição |
|---:|---|---|
| 1 | RealmApi 0.1.0 | Primeira publicação (pacote e versão exata HTTP 404). Deve existir **antes do RSTV**. Exige resolver descoberta/empacotamento dos três assemblies e gates de publicação. |
| 2 | BetterFont 1.0.3 | Independente; já publicado. Só enviar versão nova se tiver mudança real. Estar antes do BCT é apenas convenção, não mais requisito hard. |
| 3 | BetterCombatText 0.1.2 | Independente de BF após a correção. Versão já publicada; manifest mudou, portanto precisa de nova versão e README alinhado na preparação posterior. |
| 4 | BetterStats 1.0.2 | Independente; já publicado; só nova versão se houver mudança real. |
| 5 | BetterTooltips 0.1.4 | Independente; já publicado; só nova versão se houver mudança real. |
| 6 | RoguelikeDebugger 0.1.2 | A API é opcional; poderia antecedê-la. Colocado depois por conveniência. Já publicado; diferenças de fonte/publicado serão tratadas na preparação. |
| 7 | RoguelikeSkillTreeVisualizer 0.3.3 | **Somente depois de confirmar RealmApi-0.1.0 resolvendo no índice**. RSTV 0.3.3 já publicado; código/manifest local corrigidos exigem nova versão na tarefa de preparação. |
| 8 | RoguelikeUnlimitedLevelProgression 0.1.1 | Independente da API/RSTV. Primeira publicação (404), condicionada aos próprios gates/aceite, não à ordem dos demais. |
| 9 | BetterPortuguese 0.1.0 | Independente, primeira publicação (404), mas **fora do envio enquanto os gates humanos LANG estiverem abertos**. A posição é apenas topológica, não liberação. |

**Única precedência nova obrigatória entre nossos pacotes: RealmApi → envio do RSTV.** O resto pode ser reordenado sem violar este grafo; mesmo o passo 1 só é necessário antes do dependente, não antes de todo mod independente.

Por que não basta enviar os ZIPs em sequência: o serializer oficial usa `DependencyField` com `PackageReferenceValidator(require_version=True, resolve=True)` [S1-S3]. A versão referida tem de resolver quando o dependente for validado. Enviar API, confirmar sucesso e disponibilidade da **versão exata** por GET; apenas então enviar RSTV. Se a API falhar ou ainda não resolver, não seguir com RSTV. Não criar dependência reversa API→RSTV, que produziria deadlock entre versões inéditas.

## 8. Manifestos finais e verificação executada

Dependências finais literais:

```json
// BetterCombatText/manifest.json
"dependencies": ["BepInEx-BepInExPack-5.4.2305"]

// RoguelikeSkillTreeVisualizer/manifest.json
"dependencies": [
  "BepInEx-BepInExPack-5.4.2305",
  "DefRuivo_StolenRealmMods-RealmApi-0.1.0"
]
```

Os arquivos reais são JSON válido (os comentários acima são apenas indicação dos caminhos no relatório). SHA-256 após edição:

| Manifest | SHA-256 |
|---|---|
| BetterCombatText/manifest.json | `0d887399df932c2bda1c5af2239ac7bc8f28876512703781f501183d5cc5de7d` |
| RoguelikeSkillTreeVisualizer/manifest.json | `b193935242eb109b61b6cbee8d2f4b2e39c8754f969af7c6241742e816e774a1` |

Comandos reais, sem instalação/publicação:

| Comando | Exit / resultado |
|---|---|
| `python verify-dependencies.py` (workspace) | **0; 85 checks PASS, 0 FAIL**. Nove manifests, campos/versões preservados, apenas duas listas alteradas, fontes/projetos estáveis desde a fotografia, referências XML/11 DLLs, BepInEx byte-idêntico, hash do jogo, grafo/ordem, controles negativos. |
| `python tools/check_versoes.py` | **0**; oito mods batem nos quatro lugares. A ferramenta não cobre API; seus três projetos e manifest foram conferidos separadamente (0.1.0). |
| `git diff --check -- BetterCombatText/manifest.json RoguelikeSkillTreeVisualizer/manifest.json` | **0**. |
| `python tools/check_dependencias.py --local` | **1**; uma dependência não resolve: `DefRuivo_StolenRealmMods-RealmApi-0.1.0`. |
| `python tools/check_dependencias.py --api` | **1**; mesmo bloqueio confirmado remotamente. |
| `python tools/pack-thunderstore.py --listar-nomes` | **0**, lista os oito mods, **sem RealmApi**. |
| `python tools/pack-thunderstore.py RealmApi --so-conferir` | **2**, `nao existe mod com esse nome: RealmApi`. Nenhum pre-flight de pacote aprovado. |

Trecho literal do gate (ambos os modos):

```text
FALHA RoguelikeSkillTreeVisualizer: depende de DefRuivo_StolenRealmMods-RealmApi-0.1.0, que NAO existe na Thunderstore (No matching package found for reference)
==> 1 dependencia(s) NAO resolvem - o upload seria recusado pela Thunderstore (No matching package found).
```

A checagem suplementar de grafo usa a função pura `resolver` da ferramenta oficial com **entradas normalizadas em memória pelo manifest.name**, BepInEx já publicado e um lote hipoteticamente autorizado. Esse cenário passa e põe API antes de RSTV; os controles de API ausente e ciclo falham como devem. **Não alterou flags reais nem equivale ao gate oficial verde**.

### Bloqueios posteriores, explicitamente não corrigidos aqui

1. `tools/check_dependencias.py:114-147` identifica entradas pela pasta (`api`), não `manifest.name` (`RealmApi`). Assim não reconhece a API como produtora local da dependência. O gate imprime uma lista mesmo depois da falha, com `api` no fim: **não usar essa lista inválida como plano de envio**. A ordem correta está na seção 7.
2. `tools/pack-thunderstore.py` só descobre o layout `<Mod>/<Mod>.csproj`; API está em `api/Plugin/RealmApi.csproj`. É preciso suportar o layout real e os três assemblies, não criar projeto falso nem duplicar API dentro do RSTV.
3. `release/mods.json` ainda não registra RealmApi e guarda a ordem histórica de seis pacotes. O workflow/gate deve ser integrado pela frente própria; esta tarefa não alterou esse arquivo nem habilitou publicação.
4. README BCT tem a política antiga de requisito BetterFont; alinhar antes do novo pacote, conforme comentário na filha.
5. Alterar manifests locais não modifica versões já publicadas/ZIPs anteriores. Não houve repack nesta auditoria. Bump/CHANGELOG/ZIP ficam para as frentes próprias.

## 9. Fontes primárias e evidências

Consultas públicas anônimas realizadas em 16/10/2026; respostas brutas e fontes oficiais foram salvas no workspace, não inferidas de memória. O primeiro caminho tentado para validators (`repository/validation/validators.py`) deu 404; corrigido pelo import real para `repository/validators.py`, que retornou 200. O 404 de caminho incorreto **não** foi usado como prova de regra da plataforma.

- [S1] Thunderstore, `package_manifest.py`, `ManifestV1Serializer.dependencies`, linhas 70-74; rejeição de versão já existente em 96-99: `https://github.com/thunderstore-io/Thunderstore/blob/master/django/thunderstore/repository/package_manifest.py`.
- [S2] Thunderstore, `serializer_fields.py:45-56`, `DependencyField`: `https://github.com/thunderstore-io/Thunderstore/blob/master/django/thunderstore/repository/serializer_fields.py`.
- [S3] Thunderstore, `validators.py:13-28`, resolução obrigatória e recusa de referência ausente: `https://github.com/thunderstore-io/Thunderstore/blob/master/django/thunderstore/repository/validators.py`.
- [S4] Thunderstore, `package_reference.py`, parser/lookup por namespace, nome e versão: `https://github.com/thunderstore-io/Thunderstore/blob/master/django/thunderstore/repository/package_reference.py`.
- [S5] BepInEx **tag v5.4.23.5**, `BepInEx/Contract/Attributes.cs:68-124`: `https://github.com/BepInEx/BepInEx/blob/v5.4.23.5/BepInEx/Contract/Attributes.cs`.
- [S6] GET da versão exata do loader, HTTP 200: `https://thunderstore.io/api/experimental/package/BepInEx/BepInExPack/5.4.2305/`.
- [S7] GET do pacote e versão exata da API própria, ambos HTTP 404: `https://thunderstore.io/api/experimental/package/DefRuivo_StolenRealmMods/RealmApi/` e `https://thunderstore.io/api/experimental/package/DefRuivo_StolenRealmMods/RealmApi/0.1.0/`.
- [S8] GETs por pacote dos nove alvos em `https://thunderstore.io/api/experimental/package/DefRuivo_StolenRealmMods/<nome>/`: seis HTTP 200 nas versões da tabela; BP, ULLP e RealmApi HTTP 404. O BCT remoto 0.1.2 ainda declara BF-1.0.3; o RSTV remoto 0.3.3 ainda declara só BepInEx. A edição foi apenas local.

Evidências da execução: `%LOCALAPPDATA%/hermes/kanban/workspaces/t_6ac74f0f/`, incluindo inventário, fotografia anterior dos manifests, hashes de fonte, metadados Cecil, script reexecutável de validação, consultas HTTP e saídas completas dos gates. Uma cópia textual compacta dessas evidências está anexada ao cartão (não é pacote instalável e não contém DLLs/ZIPs do jogo/loader).

**Limites preservados:** nenhuma publicação, push, instalação, bump, alteração de código dos mods ou edição de CHANGELOG por esta tarefa. O checkout já tinha alterações de outras frentes; foram preservadas. Os CHANGELOGs mudaram em paralelo pela tarefa própria, não foram restaurados nem incluídos como trabalho desta auditoria.
