# BetterPortuguese

- **Version:** 0.1.0
- **Author:** gumatos
- **GUID:** `com.gumatos.betterportuguese`
- **Works with:** Stolen Realm v1.3.1 (Steam build 25240684, Unity 2022.3.62f2).
- **Needs:** BepInEx 5 (r2modman installs it for you).
- **Status:** package built and under release review; nothing is published and publication requires the owner's explicit go-ahead. The in-game round for this exact build is still pending (see *Validation state* below).

An independent BepInEx mod for Stolen Realm. It does not change gameplay, game files or other plugins. It includes complete **Original** and **Corrigido** snapshots, selectable through configuration. It does not require another mod from this project or a third-party library.

## What is inside the package — two complete sets

The package carries **both** snapshots, and you can switch between them at any time:

| Set | What it contains | When to use it |
| --- | --- | --- |
| `Original` | the game's Portuguese exactly as it is today, recorded as a complete snapshot (9,095 records from the union of the tables) | to confirm the game is untouched, or to compare against the corrected text |
| `Corrigido` | the same 9,095 records, with the approved corrections applied | normal play (default) |

`Original` is not a partial list and it is not "the mod turned off": it is a whole snapshot shipped inside the DLL, so restoring it never depends on the game still having the same text. Switching is a configuration change (see below), not a reinstall.

## What it does

Provides a Brazilian Portuguese localization overlay with a switch between **Original** and **Corrigido**, while preserving the game's live output whenever an override is not approved or its baseline does not match. The technical configuration keys and snapshot names below are literal names, not translated labels.

## How many corrections are in it — read the manifest, not this page

`plugins/BetterPortuguese/Data/manifest.json` ships inside the package next to the two snapshots. It is the authoritative record: the SHA-256 of every data file and the `coverage` block (records, pt-BR keys, changed keys). This README deliberately does not restate that number, because the number changes whenever a corrections batch is applied.

### Validation state — approval vs. what was actually run

What the number always means: `Corrigido` carries only text **approved by the owner**. Nothing is applied on the fly and no proposal file is ever loaded as a correction. Approval and runtime verification are separate gates, and this page keeps them separate too:

- **Approval** covers every correction present in `Corrigido` — the owner signed off on each batch, and `correcoes.diff.json` records the approved change for each key.
- **Runtime verification** is recorded per release, for one exact build. The in-game acceptance run recorded so far exercised an **earlier, 14-correction build** (`BetterPortuguese.dll` SHA-256 `2fc17bf4ed46300a4973c63d8ee6f892a7bf5bbcb6ec6ec138bc394062ac05b4`), not this 0.1.0 package. **The in-game round for this build is pending.**
- A green build, a packed ZIP or a passing offline suite does not authorize publication.

Both snapshots describe the same 9,095 records from the union of the tables, with 9,090 pt-BR keys present and two manual records preserved without approved pt-BR text. These totals describe the dataset, not coverage of every screen/string in the game, and never mean all 9,090 keys are nonempty translations. A `Corrigido` that adds text to records the game left empty will hold more entries than `Original` while keeping the same 9,095 records — `Original` is that baseline, not a copy of `Corrigido`.

`pt-BR.mods.json` is empty in this snapshot. `IntegracaoMods=true` reserves the setting for that layer, but **does not enable any adapter in this version**. There is no approved translation/composition of BetterTooltips notes, synergies or other mod text. Text emitted by another plugin is preserved. New translations require an approved dataset, a versioned binding and their own tests; adding proposals to pendencias.json is not enough.

## What it does not do

- Does not change gameplay, mechanics or numbers, and does not write materials, fonts, colors, PlayerPrefs or a global dictionary.
- Does not edit Assembly-CSharp.dll/resources.assets or other game assets.
- Does not translate other mods without approved content and adapters.
- Does not claim that offline builds/tests validate Mono/Unity, every open window, Portuguese rendering/fonts or publication readiness.
- Does not disable other plugins. Original removes BP changes, not other mods' notes/changes; disable those separately for a fully vanilla game.

## Configuration and returning to Original

File: `BepInEx/config/com.gumatos.betterportuguese.cfg`. The plugin creates it when run in an authorized environment; the initial delivery did NOT install the mod or launch the game.

```ini
[Geral]
Ativo = true
Conjunto = Corrigido
IntegracaoMods = true
Diagnostico = false
```

- `Conjunto = Original`: leaves the game's current output intact. The bundled original snapshot remains available for auditing; it does not impose old Portuguese text on an updated game.
- `Conjunto = Corrigido`: applies only keys actually changed in the validated snapshot, comparing the entire current list against the original baseline. A key the game no longer produces, or whose text changed with an update, is left alone instead of being forced.
- `Ativo = false`: disables the BP layers, not other mods.
- `IntegracaoMods = false`: disables only BP's mod-content layer; it does not change the selected base snapshot.
- `Diagnostico = true`: includes refresh logging, without per-frame logs.

You can edit/save the `.cfg` while the game is running. The driver in `GUIManager.Update` checks the file every second of real time; changes are queued and published on the main thread. Invalid configuration, such as `Conjunto = Corrigdo` or a numeric ordinal, disables overrides until the file is corrected. Reading does not rewrite manual comments/text in the `.cfg`. Changes made by a configuration manager also go through the queue.

Refresh is targeted: only text already registered by the game whose original key belongs to approved corrections is sent to `OptionsManager.LocalizeUIText`. It runs on the main thread when the effective layer enters or leaves Corrigido; diagnosis/integration-only changes (with an empty registry) do not rebuild the UI. It does not call `LocalizeUI(force: true)` or relocalize manual components/language objects that BP does not change. This avoids repeating native Screen/Window diagnostics on every configuration switch, without suppressing logs or patching the game's parser. If the native private registry changes signature, automatic refresh fails with a warning; lookup remains intact and the UI can be reopened. Tooltips/dynamic data need the next hover/refresh. **Visual updates of every open window have not been tested**, nor have Portuguese rendering/fonts. Original removes BP changes but not notes/changes from other mods: disable those separately for a fully vanilla game.

## Architecture and safety limits

The postfix uses the exact signature `OptionsManager.GetLocalizationEntryList(string original, LanguageChoice languageChoice, bool fallbackToTranslatorKey)`, returning `List<LocalizationEntry>`. Both the query and effective language must be PortugueseBrazil. Keys are compared with `StringComparer.Ordinal`: no trimming, case changes or tag removal. The game still handles highlighting/gender, selects the first nonblank entry and resolves placeholders/numbers.

The core does not mutate asset lists/objects: it creates its own list and objects only for an override. A key changed by an update or an unknown plugin is not overwritten; conflicts are logged by ID with a log cap. A later postfix can still change the output: precedence over unknown plugins is not promised.

Strict UTF-8 JSON files are embedded in the DLL and distributed as auditable copies in `plugins/BetterPortuguese/Data/`. Each resource's SHA-256 is pinned in the code. Duplicate JSON members/IDs/keys, an invalid schema, identity drift, an unapproved diff or token loss cause the catalog to be rejected. Proposals in `pendencias.json` are NOT loaded as corrections.

The 0.1.0 loader applies two kinds of approved correction: a text edit to an existing entry (`Value`/`Feminine`/`Masculine`/`Neutral`), and `addEntry` — one neutral `Value` for a known record whose original list is empty or absent, with the functional tokens/tags of the English key preserved. It never appends to a populated list, never invents gender variants, and does not remove entries. Manual translations, tag/token changes and a mod adapter still require new implementation and their own validation, and fail safely in this version.

BP writes no material, font, color, number, mechanic, PlayerPrefs or global dictionary. Assembly-CSharp.dll/resources.assets remain intact. The game's native refresh may run its own UI mechanisms; that is not a BP styling patch.

## Install

**Nothing here is published.** Publication requires the owner's explicit go-ahead; building, testing or packing the mod does not authorize it.

**r2modman (recommended):** install this package in the Stolen Realm profile — the DLL and its `Data` folder go to `BepInEx\plugins\BetterPortuguese\`.

**Manual:** install BepInEx 5 x64 (or press "Start modded" once in r2modman to create the folders), then copy the `BetterPortuguese` folder to:

```text
%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
```

The file must end up as `...\plugins\BetterPortuguese\BetterPortuguese.dll`, with `Data\` beside it. Do not distribute game/Unity/BepInEx reference DLLs or load them as plugins. Do not put DLL backups inside `plugins`: the loader scans recursively and would load them as mods.

## Uninstall

To remove a future authorized installation, disable the mod in the profile or remove only `BepInEx/plugins/BetterPortuguese/`. The original game needs no restoration because no asset is edited. You may keep the configuration. Do not put DLL backups inside plugins: the loader scans recursively.

## Build and verify — without installing

Private local references must exist in the repository root's `lib/`. Never distribute game/Unity/BepInEx DLLs or load them as plugins.

```bash
dotnet build BetterPortuguese/BetterPortuguese.csproj -c Debug -p:DeployToBepInEx=false
dotnet build BetterPortuguese/BetterPortuguese.csproj -c Release -p:DeployToBepInEx=false
python tests/BetterPortuguese.Offline/run.py
```

The runner uses the .NET 6 SDK for the core/binding and the Windows desktop CLR to execute local HarmonyX with the same production core. The test bench's HarmonyX 2.9.0.0 DLL did not work on the net6 host (`AccessTools/MethodInvoker`); the desktop CLR alternative was actually executed, not a Harmony mock. Fixtures are explicitly synthetic and do not enter the distributed snapshots.

Checks include the lossless corpus, approval/diff, negative parser cases, clones/rollback/conflicts, queue/configuration, real API metadata and each resource's bytes in the Debug and Release DLLs, plus actual execution of decoy postfixes in two registration orders, an absent/unknown owner and a cycle. This **does not** test the plugin in Mono/Unity, the UI or mod notes. The builds have an MSB3277 warning for System.Net.Http from the Assembly-CSharp reference; there are no compilation errors in the initial delivery's recorded builds.

## Auditable package

After building/testing, use the dedicated packager, which reuses the repository's metadata validation and includes the external JSON files required by BP-1:

```bash
python BetterPortuguese/package.py --output dist/gumatos-BetterPortuguese-0.1.0-auditado.zip
```

It refuses to replace an existing ZIP and does not install or publish. The repository's generic packager produces a DLL with embedded resources but does not add the Data copies; **use this command for the auditable delivery**. `Data/manifest.json` describes the snapshots; it is not the root Thunderstore manifest. The packer re-checks the metadata, the pinned resource hashes, both snapshot corpora, the icon (whole PNG, 256×256) and whether the DLL is newer than every source/data file — that last check is what stops a stale binary from shipping.

## Keeping it working when the game updates

The mod reads both snapshots from inside the DLL and matches the game's Portuguese text by exact ordinal key. When Stolen Realm updates:

- **It cannot break the game.** An override happens only while the game's current list still equals the recorded baseline. Anything that no longer matches is passed through untouched, so a changed or new text simply stays exactly as the game wrote it.
- **The visible signal is the text itself.** A line that still appears in English (or in the old wording) no longer matched its key and was skipped — nothing is rewritten silently. `Diagnostico = true` plus the BepInEx log name the conflict by ID.
- **A new game version needs a re-measurement, not just a rebuild.** This release targets Stolen Realm **v1.3.1**, Steam build **25240684**, Unity **2022.3.62f2**, measured against `Assembly-CSharp.dll` SHA-256 `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`. That identity is recorded in the `source` block of `Data/pt-BR.original.json` and in `api/docs/target-game.json`. After an update: re-extract both snapshots, re-pin the resource hashes, rerun the offline suite and the in-game check, then ship a new version — a published version is immutable, so a version bump is the fix.

**How to help:** if a line is still untranslated (or wrong) in game, copy the exact English text and, with `Diagnostico = true`, the matching BepInEx log line. The English line is the key every correction is matched against, so a paraphrase cannot be applied.

## Provenance

BP-1 architecture decision; BP-2 lossless Original; BP-3 Corrigido snapshot without approvals (since superseded by the approved corrections recorded in `Data/manifest.json`). Canonical source: LANG-R1 `entrega02/localizacao-ptbr.json`. Full hashes and pending items accompany Data/; the reference assembly is identified by the snapshot source, not redistributed. Editorial approvals and authorized runtime validation remain separate gates; a green build does not authorize publication.

---

## Português (BR)

Mod independente para alternar entre Original e Corrigido sem mudar gameplay nem arquivos do jogo. O pacote traz os dois conjuntos completos: Original (o texto do jogo como está hoje) e Corrigido (o mesmo corpus com as correções aprovadas). A contagem exata de correções está em `Data/manifest.json`, não neste texto. As chaves de configuração permanecem em português; build verde não autoriza publicação — publicar exige a palavra do dono.

O texto português original foi preservado integralmente abaixo como registro da entrega inicial, não como uma nova medição do dataset/runtime atual.

<details>
<summary>Texto original em português — registro integral da captura inicial</summary>

# BetterPortuguese

- **Version:** 0.1.0
- **Author:** gumatos
- **GUID:** `com.gumatos.betterportuguese`
- **Status:** implementação inicial, validação offline; NÃO aprovado para publicação ou instalação automática.

Mod BepInEx independente para Stolen Realm, sem alterar gameplay, arquivos do jogo ou outros plugins. Contém os conjuntos completos **Original** e **Corrigido**, selecionáveis pela configuração. Não precisa de nenhum outro mod do projeto nem de biblioteca de terceiros.

## Estado editorial desta versão — importante

Esta captura contém **ZERO correções aprovadas**. Os gates humanos LANG-C1..C5 ainda estavam pendentes na entrega BP-3. Por isso Corrigido contém os mesmos textos/entradas do Original (a única diferença no JSON é `variant`). O padrão `Corrigido` é a escolha do conjunto, não uma alegação de que o português já foi melhorado.

Os dois snapshots têm 9.095 registros da união das tabelas, 9.090 chaves pt-BR presentes, 8.097 entradas, 1.286 listas vazias e cinco ausências explícitas. Há dois registros manuais preservados, sem pt-BR aprovado. Esses totais descrevem o dataset, não cobertura de toda tela/string do jogo nem 9.090 traduções não vazias.

`pt-BR.mods.json` está vazio. `IntegracaoMods=true` reserva a configuração dessa camada, mas **não ativa nenhum adaptador nesta versão**. Não há tradução/composição aprovada das notas de BetterTooltips, de synergies nem de outros textos de mods. Texto emitido por outro plugin é preservado. Novas traduções precisam de dataset aprovado, binding versionado e testes próprios; não basta acrescentar propostas a pendencias.json.

## Configuração e volta ao original

O arquivo é `BepInEx/config/com.gumatos.betterportuguese.cfg`. O plugin cria este arquivo quando executado no ambiente autorizado; esta entrega NÃO instalou nem abriu o jogo.

```ini
[Geral]
Ativo = true
Conjunto = Corrigido
IntegracaoMods = true
Diagnostico = false
```

- `Conjunto = Original`: deixa o resultado vigente do jogo passar intacto. O snapshot original embarcado continua disponível para auditoria; não impomos um português antigo sobre um jogo atualizado.
- `Conjunto = Corrigido`: aplica somente chaves efetivamente alteradas no snapshot validado, comparando integralmente a lista vigente com a baseline original. Nesta captura não há chaves alteradas.
- `Ativo = false`: desliga as camadas BP; não desliga outros mods.
- `IntegracaoMods = false`: desliga só a camada BP de conteúdo de mods; não muda a escolha do conjunto base.
- `Diagnostico = true`: inclui registro de refresh, sem log por frame.

É possível editar/salvar o `.cfg` enquanto o jogo está aberto. O driver no `GUIManager.Update` verifica o arquivo a cada segundo de tempo real; mudanças são enfileiradas e publicadas na thread principal. Config com valor inválido, como `Conjunto = Corrigdo` ou um ordinal numérico, desativa overrides até o arquivo ser corrigido. A leitura não regrava comentários/textos manuais do `.cfg`. Mudanças feitas por um gerenciador de configuração também passam pela fila.

O refresh é dirigido: somente textos já registrados pelo jogo cuja chave original pertence às correções aprovadas são enviados a `OptionsManager.LocalizeUIText`. Ele roda na thread principal quando a camada efetiva entra ou sai de Corrigido; mudanças apenas de diagnóstico/integração (registro vazio) não refazem a UI. Não chama `LocalizeUI(force: true)` nem relocaliza componentes manuais/objetos de idioma que o BP não altera. Isso evita repetir diagnósticos nativos Screen/Window a cada troca de configuração, sem suprimir logs nem remendar o parser do jogo. Se o registro privado nativo mudar de assinatura, o refresh automático falha com aviso; o lookup segue preservado e a UI pode ser reaberta. Tooltips/dados dinâmicos precisam de próximo hover/refresh. **Não foi testada atualização visual de toda janela aberta**, nem renderização/fontes em português. Original remove alterações BP, mas não remove notas/alterações dos outros mods: para o jogo totalmente vanilla é preciso desativá-los separadamente.

## Arquitetura e limites de segurança

O postfix usa a assinatura exata de `OptionsManager.GetLocalizationEntryList(string original, LanguageChoice languageChoice, bool fallbackToTranslatorKey)`, retorno `List<LocalizationEntry>`. Consulta e idioma efetivo precisam ser PortugueseBrazil. Chaves são comparadas com `StringComparer.Ordinal`: sem trim, mudança de caixa ou remoção de tags. O jogo continua processando destaque/gênero, escolhendo a primeira entrada não branca e resolvendo placeholders/números.

O core não muta listas/objetos do asset: cria uma lista e objetos próprios somente no override. Uma chave alterada por update ou plugin desconhecido não é sobrescrita; conflito é registrado por ID com teto de logs. Outro postfix posterior continua podendo mudar a saída: não há promessa de precedência sobre plugins desconhecidos.

JSONs UTF-8 estritos são embutidos na DLL e distribuídos como cópias auditáveis em `plugins/BetterPortuguese/Data/`. SHA-256 de cada recurso é fixado no código. Membros JSON/IDs/chaves duplicados, schema inválido, drift de identidade, diff sem aprovação ou perda de tokens recusam o catálogo. Propostas de `pendencias.json` NÃO são carregadas como correções.

O loader 0.1.0 suporta alterações aprovadas de Value/Feminine/Masculine/Neutral em entradas existentes. Mudança de lista/ausência, tradução manual, alteração de tags/tokens ou adaptador de mods requer implementação/validação nova e falha de modo seguro nesta versão. Esse limite não perde registros do snapshot; restringe operações aplicáveis no runtime atual.

Nenhum material, fonte, cor, número, mecânica, PlayerPrefs ou dicionário global é escrito pelo BP. Assembly-CSharp.dll/resources.assets permanecem intactos. O refresh nativo do jogo pode executar os seus próprios mecanismos de UI; isso não é um patch de estilo do BP.

## Compilar e verificar — sem instalar

Referências locais privadas devem existir na `lib/` da raiz. Nunca distribuir DLLs do jogo/Unity/BepInEx nem carregá-las como plugins.

```bash
dotnet build BetterPortuguese/BetterPortuguese.csproj -c Debug -p:DeployToBepInEx=false
dotnet build BetterPortuguese/BetterPortuguese.csproj -c Release -p:DeployToBepInEx=false
python tests/BetterPortuguese.Offline/run.py
```

O runner usa o SDK .NET 6 para o core/binding e o CLR desktop do Windows para executar HarmonyX local com o mesmo core de produção. A DLL HarmonyX 2.9.0.0 desta bancada não funcionou no host net6 (`AccessTools/MethodInvoker`); a alternativa CLR desktop foi executada, não um mock do Harmony. Fixtures são explicitamente sintéticas e não entram nos snapshots distribuídos.

As verificações incluem corpus lossless, aprovação/diff, parser negativo, clones/rollback/conflito, fila/config, metadata da API real e bytes de cada recurso nas DLLs Debug e Release, além de execução de postfixes-isca reais em duas ordens de registro, owner ausente/desconhecido e ciclo. Isso **não** testa o plugin em Mono/Unity, a UI ou notas dos mods. Os builds têm um warning MSB3277 de System.Net.Http pela referência Assembly-CSharp; nenhum erro de compilação.

## Pacote auditável

Após build/testes, use o empacotador específico, que reutiliza a validação de metadados do repositório e inclui os JSONs externos exigidos por BP-1:

```bash
python BetterPortuguese/package.py --output dist/gumatos-BetterPortuguese-0.1.0-auditado.zip
```

Ele recusa substituir um ZIP já existente e não instala/publica. O empacotador genérico do repositório produz DLL com recursos embutidos, mas não acrescenta as cópias Data; **para a entrega auditável use este comando**. `Data/manifest.json` descreve os snapshots, não é o manifest Thunderstore da raiz.

Para remover uma futura instalação autorizada, desative o mod no perfil ou remova somente `BepInEx/plugins/BetterPortuguese/`. O jogo original não precisa de restauração porque nenhum asset é editado. A configuração pode ser mantida. Não colocar backups de DLL dentro de plugins: o loader é recursivo.

## Proveniência

Decisão de arquitetura BP-1; Original lossless BP-2; captura Corrigido sem aprovações BP-3. Fonte canônica: LANG-R1 `entrega02/localizacao-ptbr.json`. Os hashes completos e as pendências acompanham Data/; o assembly de referência é identificado pela fonte dos snapshots, não redistribuído. Aprovações editoriais e runtime autorizado BP-5 ainda são gates separados; build verde não libera publicação.

</details>
