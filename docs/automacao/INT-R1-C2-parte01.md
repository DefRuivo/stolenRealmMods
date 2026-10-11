# INT-R1-C2 — parte 01: método, fontes congeladas e o mapa tipo-a-tipo dos dois núcleos

Cartão: `t_2ea91249` (INT-R1-C2, arquitetura/decisão). Pais: `t_adc1fbfa` (KIT-13, done) e `t_b7f6fc4a`
(API-R1, done). Rodada: run 780, modelo `deepseek-flash`/`deepseek` (escalado pelo controlador de economia
após 3 tentativas `rate_limited` de `gpt-6.1-sol`).
Escopo desta rodada: **decidir e documentar**. Nenhum código de produção alterado, nenhum mod editado,
nada instalado, jogo não aberto, nada publicado.

Regra de prova desta rodada: toda afirmação técnica vem com **caminho:linha**, **contagem medida** ou
**comando reproduzível**. O que não é exercitável está marcado `NAO_EXERCITADO` com o motivo — nunca
estimado.

---

## 1. Fontes congeladas (o mapa vale para estes hashes, não para "o repo em geral")

| Papel | Arquivo | Linhas | sha256 |
|---|---|---|---|
| Núcleo do kit (SDK) | `tools/automacao/kit13/SDK/RegistryV1.cs` | 153 | `9f2eabdd5da1a3796e7c191f241ff5687d9fb876d51a0bd03117ed1789187700` |
| Núcleo da API (contratos) | `api/Core/Contracts.cs` | 127 | `7970780440d1682a7b3bb3d09ddc4812c7371ae5a85edf141e575caf7d48cb62` |
| Instalação Harmony da API | `api/Hooks/HookInstallation.cs` | 69 | `179fde71c304ba81efff984610216e180bbc160728d6edcdb7061e5ed88b240a` |
| Plugin da API (gate + config) | `api/Plugin/RealmApiPlugin.cs` | 45 | `b255c9eebfc6549e77121906764d9c590f8098747a395f15c93c60d704869d43` |
| Ponte do kit para o Core **KIT-04** (não é a API) | `tools/automacao/kit13/CoreBridge/CoreEventsExtension.cs` | 33 | `7f127d98a091d104538f11735972dd59ef03846848bc7b0e1057fc1dcda1d183` |
| Instrumento de observação in-game (AUT-4) | `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | 1957 | `ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2` |

Comando que produziu a tabela:

```bash
cd /c/dev/stolen-realm && wc -l tools/automacao/kit13/SDK/RegistryV1.cs api/Core/Contracts.cs \
  api/Hooks/HookInstallation.cs api/Plugin/RealmApiPlugin.cs \
  tools/automacao/kit13/CoreBridge/CoreEventsExtension.cs \
  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs && sha256sum tools/automacao/kit13/SDK/RegistryV1.cs \
  api/Core/Contracts.cs api/Hooks/HookInstallation.cs api/Plugin/RealmApiPlugin.cs \
  tools/automacao/kit13/CoreBridge/CoreEventsExtension.cs \
  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs
```

Nota de estado do repositório: `git status --porcelain` mostra vários arquivos `M` de **outros** cartões em
voo (RoguelikeSkillTreeVisualizer, AUT4Probe, aut5, cenarios). Nenhum deles pertence a esta rodada; o último
commit é `d82894e` (Wed Oct 7). O produto desta rodada são apenas os arquivos
`docs/automacao/INT-R1-C2-parteNN.md` — arquivos **novos**, criados aqui.

---

## 2. Mapa tipo-a-tipo: o núcleo do kit (`Gumatos.KitSdk.V1`)

Assembly `Gumatos.KitSdk`, `netstandard2.1`, `<Version>1.0.0</Version>`, **sem** Unity, BepInEx ou jogo
(`tools/automacao/kit13/SDK/KitSdk.csproj:3-8`; a única `Reference` do projeto é nenhuma — não há
`ItemGroup` de referências). O csproj ainda impõe build offline:
`Kit13OfflinePreflight` erra se `$(DeployToBepInEx) != 'false'` (`KitSdk.csproj:9-11`).

| Tipo | Linhas | O que faz | Papel |
|---|---|---|---|
| `EventV1` | `RegistryV1.cs:8-21` | DTO imutável `Session`/`Frame`/`Kind`/`Data`; valida `session≤128`, `frame≥0`, `kind≤128`, `data≤4096`; lança `ArgumentException("evento v1 invalido")` | **transporte** de um evento observado |
| `ReadingV1` | `RegistryV1.cs:23-33` | `Status` ∈ {`OBSERVADO`,`AUSENTE`,`NAO_EXERCITADO`,`FALHOU_FECHADO`} + `Value≤4096` | **leitura** de estado, com taxonomia de ausência |
| `VerdictV1` | `RegistryV1.cs:35-45` | `Status` ∈ {`PASSOU`,`FALHOU`,`NAO_EXERCITADO`,`FALHOU_FECHADO`} + `Reason≤512` | **veredito** contra um esperado externo |
| `IExtensionV1` | `RegistryV1.cs:49-54` | `OnEvent(EventV1)`, `Read(string)`, `Validate(string,ReadingV1,string)` | **contrato de extensão** |
| `RegistryV1` | `RegistryV1.cs:56-152` | registro com `lock`, ID `[a-z][a-z0-9.-]{0,63}`, limite 64, lease `IDisposable`, guarda de reentrância, isolamento de exceção, `Diagnostics()` limitado a 64 | **barramento + ciclo de vida** |

Detalhes que só o kit tem (e que são comportamento observável, não estilo):

- versão de API **exata** no registro: `if (apiVersion != ApiVersion) throw new NotSupportedException("API_INCOMPATIVEL: esperado " + ApiVersion)` (`RegistryV1.cs:92`), com `ApiVersion = "1.0.0"` (`RegistryV1.cs:58`);
- diagnóstico **não guarda mensagem**: `diagnostics.Enqueue(id + ":" + operation + ":" + error.GetType().Name)` com o comentário explícito de que a mensagem pode conter segredo (`RegistryV1.cs:79-84`);
- reentrância recusada: `EVENTO_REENTRANTE` (`RegistryV1.cs:114`);
- `Dispose()` serializa no monitor: "once Dispose returns, no old callback is in flight" (`RegistryV1.cs:149-151`);
- ausência de extensão vira `AUSENTE` na leitura (`RegistryV1.cs:133`) e `NAO_EXERCITADO` no veredito (`RegistryV1.cs:143-144`).

## 3. Mapa tipo-a-tipo: o núcleo da API (`Gumatos.RealmApi`)

Assembly `RealmApi.Core` (`api/Core/RealmApi.Core.csproj`), namespace `Gumatos.RealmApi`, versão do
**pacote** `0.1.0` (`Contracts.cs:17`). `api/Core/Contracts.cs` declara 7 tipos públicos
(`grep -n "public static class|public sealed class|public interface" api/Core/Contracts.cs`):

| Tipo | Linhas | O que faz | Papel |
|---|---|---|---|
| `ApiIdentity` | `Contracts.cs:13-27` | `Guid/Name/Version` do pacote + `SteamAppId=1330000`, `GameVersion="1.3.1"`, `SteamBuildId="25240684"`, `AssemblySha256="8bb4a7c5…855a"`; `Matches(version, sha256)` é **fail-closed** | **gate de identidade do alvo** |
| `HookDescriptor` | `Contracts.cs:30-55` | assinatura exata (FullName do tipo, nome do método, `IsStatic`, tipo de retorno, lista ordenada de parâmetros); `Resolve` exige **1** alvo e não procura em outros assemblies | **contrato do ponto de observação** |
| `HookCatalog` | `Contracts.cs:58-66` | **4** hooks: `game.awake`, `ui.skill-tree.updated`, `ui.localized`, `combat.turn-started` | **catálogo** observado |
| `HookNotification` | `Contracts.cs:69-77` | `HookId`, `Instance`, `Arguments` (cópia **rasa** da lista), `Result` | **transporte** de um hook observado |
| `Signal<T>` | `Contracts.cs:80-103` | `Subscribe(handler)` → `IDisposable`; `Publish` itera snapshot e isola exceção por listener via `Action<Exception> report` | **barramento** |
| `RealmHooks` | `Contracts.cs:106-111` | `Observed : Signal<HookNotification>` (público, só leitura) + `Emit` **internal** | **ponto de consumo** |
| `RealmAccess` | `Contracts.cs:114-126` | `ReadProperty(assembly, typeName, propertyName, instance)`; só propriedade de leitura, sem indexer, sem cache de `UnityEngine.Object` | **leitura reflexiva pontual** |

Fora de `Contracts.cs`, o núcleo da API ainda publica a família de requisitos de UI
(`api/Core/Ui/UiFamily.cs`: `UiMemberKind`, `UiRequirement`, `UiHosts`, `UiRequirements`, `UiFamily`) e o
enum `Skills.SkillTree` (`api/Core/Skills/SkillTree.cs:8`) — todos com a **mesma regra de exatidão** do
`HookDescriptor.Resolve` (`UiFamily.cs:17-21`), e ainda `HookInstallation`
(`api/Hooks/HookInstallation.cs:10`, instalação Harmony real, só postfix observacional) e o plugin de boot
`RealmApiPlugin` (`api/Plugin/RealmApiPlugin.cs:14`).

---

## 4. Lado a lado: o que faz o mesmo, o que só um faz

Comparação por **função**, não por nome. "Só um faz" = não existe equivalente no outro núcleo
(verificado por leitura dos dois arquivos inteiros e por `grep` dos tipos públicos).

| Função | Kit (`Gumatos.KitSdk.V1`) | API (`Gumatos.RealmApi`) | Veredito |
|---|---|---|---|
| Transporte de um evento observado | `EventV1` (`RegistryV1.cs:8`) | `HookNotification` (`Contracts.cs:69`) | **mesmo papel** |
| Barramento de observadores | `RegistryV1.Publish` (`RegistryV1.cs:108`) | `RealmHooks.Observed` = `Signal<HookNotification>` (`Contracts.cs:106-108`) | **mesmo papel** |
| Registro/assinatura | `Register(id, apiVersion, ext)` → `IDisposable` (`RegistryV1.cs:87`) | `Signal<T>.Subscribe(handler)` → `IDisposable` (`Contracts.cs:85`) | **mesmo papel** |
| Isolamento de erro de extensão | `try/catch` por extensão + `Diagnostics()` (`RegistryV1.cs:121-122,79-85`) | `try/catch` por listener + `report(ex)` (`Contracts.cs:91-96`) | **mesmo papel**, granularidade diferente (o kit categoriza *status*; a API só reporta) |
| Leitura de estado | `IExtensionV1.Read` → `ReadingV1` com taxonomia (`RegistryV1.cs:23-33,128-137`) | `RealmAccess.ReadProperty` (reflexão direta) + `HookNotification.Arguments` (`Contracts.cs:114-126`) | **mesmo papel**, sem taxonomia na API |
| Autorização de observação | vem do **host**, como `Func<bool>` (`CoreBridge/CorePluginBinding.cs:11-16`) | `Safety.EnableHooks` (config BepInEx) + gate de identidade (`RealmApiPlugin.cs:21-31`) | **mesmo papel**, donos diferentes |
| Veredito contra esperado | `VerdictV1` + `Validate` (`RegistryV1.cs:35,138`) | **não existe** | **só o kit** |
| Taxonomia de ausência (`OBSERVADO`/`AUSENTE`/`NAO_EXERCITADO`/`FALHOU_FECHADO`) | `ReadingV1`/`VerdictV1` (`RegistryV1.cs:29,41`) | **não existe** | **só o kit** |
| Diagnóstico sem mensagem (anti-segredo) | `RegistryV1.cs:79-84` + teste `event-isolation` (`Harness/Program.cs:34`) | **não existe** (a API loga a exceção inteira) | **só o kit** |
| Limite de inscrições | 64 (`RegistryV1.cs:96`) | **não existe** | **só o kit** |
| Recusa de reentrância | `EVENTO_REENTRANTE` (`RegistryV1.cs:114`) | **não existe** (snapshot evita enumerar durante mutação, não publica recusa) | **só o kit** |
| Pacote declarativo (JSON `KIT13/scenario/1`, sem código) | `packages.py:15,51`, `scenario-v1.schema.json:9` | **não existe** | **só o kit** |
| Executabilidade sem o jogo | todo o SDK é `netstandard2.1` puro (`KitSdk.csproj:3`) | `Core` é puro, mas `Hooks`/`Plugin` exigem Harmony/BepInEx (`api/Hooks/HookInstallation.cs:5`) | **assimetria essencial** |
| Saber **qual** jogo é observado | nada — o kit não conhece o jogo | `ApiIdentity` + `HookDescriptor.Resolve` (`Contracts.cs:14-55`) | **só a API** |
| Instalar observação no processo do jogo | nada (não usa Harmony) | `HookInstallation` (`HookInstallation.cs:21-48`) | **só a API** |
| Produzir o evento na origem | nada (o kit é alimentado por host) | postfixes Harmony (`HookInstallation.cs:49-58`) | **só a API** |

### 4.1 O eixo "versão" não é o mesmo nos dois — e essa é a raiz do conflito

- No kit, a versão é **do protocolo de extensão**: `RegistryV1.ApiVersion = "1.0.0"`, conferida no
  `Register` (`RegistryV1.cs:58,92`), e repetida no pacote declarativo
  (`scenario-v1.schema.json:9` com `{"const": "1.0.0"}`, `packages.py:15,51`).
- Na API, a versão é **do alvo do jogo**: `ApiIdentity.Version = "0.1.0"` é a versão do pacote/plugin
  (`Contracts.cs:17`) e o que barra a instalação é `Matches(Application.version, sha256)`
  (`Contracts.cs:24-26`, usado em `RealmApiPlugin.cs:29-30`).

Ou seja: os dois núcleos já têm uma regra de "recusa fechada por string exata", mas sobre **coisas
diferentes**. Qualquer unificação que misture os dois eixos numa única string está errada por construção —
ver a regra de versionamento na parte 02.

### 4.2 A duplicação concreta de hoje (não teórica)

| Dado | Kit | API | Instrumento |
|---|---|---|---|
| Patch em `OptionsManager.Localize` | — | hook `ui.localized` no catálogo (`Contracts.cs:63`, estático, retorno `System.String`, `(System.String, LanguageGender, Gender)`) | `AUT4ProbePlugin.cs:251` (`GanchoTodos("OptionsManager","Localize")`, **todos** os overloads) |
| Contagem de eventos | `RegistryV1.Read("id","events.count")` (`CoreBridge/CoreEventsExtension.cs:21-26`) | — | reflexão própria: `Tipo`/`Membro`/`Estatico` varrendo **todos** os assemblies (`AUT4ProbePlugin.cs:1824-1859`) |
| Donos dos patches | — | — | lê `Harmony.GetPatchInfo` em 4 funis próprios (`AUT4ProbePlugin.cs:952-1000`) |

Isto é o `[DUPLICADO]` do INT-R1 (`docs/automacao/INT-R1-parte03.md:18-19`) com endereço: o mesmo método
(`OptionsManager.Localize`) é patcheado por dois donos diferentes e a contagem de eventos é feita por duas
contabilidades independentes.

---

## 5. `NAO_EXERCITADO` declarado já nesta parte

- **Runtime do jogo (BepInEx carregando `RealmApi.dll` e instalando os 4 hooks), com `EnableHooks=true`:
  NAO_EXERCITADO** — o jogo não foi aberto nesta rodada (`RealmApiPlugin.cs:21` mantém o padrão `false`;
  API-R1 declarou o mesmo limite).
- **Carregamento da ponte nova em jogo: NAO_EXERCITADO** — ela não existe ainda (é escopo da parte 03).
- **Comportamento do clique/navegação do AUT4Probe (`t_139f714f`, `0xc0000005`): NAO_EXERCITADO** — fora do
  escopo desta decisão e não resolvido pela API (`docs/automacao/INT-R1-parte03.md:20`).
- **Os números do smoke da API nesta rodada**: ver parte 02/04 — a evidência gravada é
  `api/docs/smoke-result.json` (`ran: 62, failures: 0, exitCode: 0`, `runAt 2026-10-11T04:38:20-03:00`,
  gerado pelo API-R1-I2). Não re-executei o smoke nesta rodada; o que eu executei está listado na parte 04.
