# BUMP-2 — entrega para revisão

Data da preparação: 2026-10-19. Cartão: `t_241bb80c`.

Escopo: preparar quatro versões e seus ZIPs locais. **Nada foi publicado, enviado para GitHub/Thunderstore ou instalado no perfil.** Não foi disparado workflow nem alterado o gate de publicação. Publicar continua sendo ato separado do dono, por mod, com aprovação no Environment.

## Versões e SHA-256 dos pacotes

Os hashes abaixo são dos ZIPs completos em `dist/`, não das DLLs. A coluna “antes” usa o pacote local da versão anterior, congelado no começo da tarefa; não afirma que houve download ou consulta da versão publicada.

| Mod | Versão antiga | Nova | 4 lugares casam? | SHA-256 antes → depois |
|---|---|---|---|---|
| RoguelikeDebugger | 0.1.3 | 0.1.4 | Sim: csproj, manifest, BepInPlugin e README | `e1b99240125f50e4bcc7741244fe01fd41f7ca0c884970229547a149908638bf` → `ad19b2d613987a00b9e6be71ea054337ab8d225544b01b723870d5d6f4ed301a` |
| RoguelikeSkillTreeVisualizer | 0.3.4 | 0.3.5 | Sim: csproj, manifest, const Version e README | `cc2f0a2e94137071609657bbaba3a05fec1ae0178352a4ff2348ad19458dd225` → `8a01f86d06ffff8e93182c85f54f1dc5768b729ff6b24e784f519d9a63059e12` |
| RoguelikeUnlimitedLevelProgression | 0.1.1 | 0.1.2 | Sim: csproj, manifest, const PluginVersion e README | `40dd861ce5940b2a5816fa39f6d94a78784fe5f4da5a909bf4ec6f6c824bf5dc` → `f508b8e0f92a64e9e78e6725ce106f22093be614b3c0ba4d1d9c015536168c81` |
| RealmApi | 0.1.0 | 0.1.1 | Sim; também nos três csproj/assemblies e em ApiIdentity.Version | `503846842740d0c14279c60d7b400c05a6ca869c7f1da1f43e792554c5cb997e` → `395aa80d526bc0db1df21ad59bdcf26343f546b8a35786c7a976babf76fe8862` |

Pacotes gerados:

- `dist/gumatos-RoguelikeDebugger-0.1.4.zip` — 136377 bytes, 5 entradas.
- `dist/gumatos-RoguelikeSkillTreeVisualizer-0.3.5.zip` — 108642 bytes, 5 entradas.
- `dist/gumatos-RoguelikeUnlimitedLevelProgression-0.1.2.zip` — 142293 bytes, 5 entradas.
- `dist/gumatos-RealmApi-0.1.1.zip` — 144104 bytes, 8 entradas.

As versões anteriores foram preservadas. Os nomes `gumatos-...zip` são a convenção do empacotador/publish.yml; o namespace das dependências continua sendo `DefRuivo_StolenRealmMods`.

## RSTV: pin e ordem de envio — decisão anunciada antes de empacotar

Alteração aplicada e registrada no comentário do cartão antes do empacotamento:

- Manifest: `DefRuivo_StolenRealmMods-RealmApi-0.1.0` → **`DefRuivo_StolenRealmMods-RealmApi-0.1.1`**.
- `RoguelikeSkillTreeVisualizer/Plugin.cs`: `ApiVersionMinima = "0.1.1"`, mantendo o `[BepInDependency(ApiGuid, ApiVersionMinima)]` hard.
- README: requisitos em inglês e português atualizados para 0.1.1.
- O piso acompanha o pacote deste lote; não declara uma quebra de API nem uma família UI nova. A família existe desde 0.1.0.

Ordem recomendada para o dono, depois da revisão:

1. Publicar **somente RealmApi 0.1.1** (`mod=RealmApi`), com aprovação humana no Environment.
2. Confirmar que a **versão exata 0.1.1** está disponível no destino. Uma aprovação ou um step verde não substitui essa leitura.
3. Só então publicar **RoguelikeSkillTreeVisualizer 0.3.5** (`mod=RoguelikeSkillTreeVisualizer`), com nova aprovação humana.
4. RoguelikeDebugger 0.1.4 e ULLP 0.1.2 não declaram dependência da RealmApi e podem ser enviados individualmente em qualquer posição; para uma fila simples, depois dos dois acima.

**Não usar `mod=todos` para este lote.** O `publish.yml` atual tem o envio do RSTV em **5.5** e o da RealmApi em **5.7**: a ordem física dos steps coloca o dependente antes da nova versão da dependência. Não alterei o workflow nem o ledger neste cartão. O passo 5.7 já usa `dist/gumatos-RealmApi-${VERSAO}.zip`; não precisa transformar o pacote em projeto de raiz ou reduzir suas três DLLs a uma.

## O que entrou nos changelogs

As quatro entradas novas estão em inglês, identificadas como **in preparation**, sem inventar data de publicação. Todas registram o bloco do README com link do repositório para contribuir, abrir issues ou fazer fork.

- RD: documentação/versão; nenhuma mudança nova de instrumentação.
- RSTV: documentação, versão e alinhamento explícito da dependência mínima/pin. Nenhuma mudança de layout foi inventada neste bump.
- ULLP: documentação/versão e o esclarecimento já presente no README sobre singleplayer testado e multiplayer ainda não testado. Não foi acrescentado suporte multiplayer.
- RealmApi: versões dos três projetos/assemblies e da identidade alinhadas. Os dois logs que tinham `RealmApi 0.1.0` fixo agora usam `ApiIdentity.Version`. O smoke de metadados deixou de exigir `0.1.0.0` fixo e passa a derivar a versão esperada da mesma identidade.

Base de comparação: `b1fa441ce6d11bea002aef98b7d15a525b9a408a`. Os quatro alvos estavam sem alterações locais no começo. Entre a preparação anterior (`a8e2f62`) e essa base não havia alteração de `.cs`/`.csproj` desses alvos; havia documentação e metadados/ícone da API.

A comparação de metadados/IL das DLLs dos ZIPs anteriores com as dos novos ZIPs encontrou somente os rótulos de versão nos `Awake` do RSTV, ULLP e plugin RealmApi. Nenhum outro corpo de método mudou. Isso é evidência estática do escopo do bump, **não** teste de comportamento no jogo.

## RealmApi: as três DLLs, não só o manifest

O pacote tem exatamente:

```text
CHANGELOG.md
LICENSE
README.md
icon.png
manifest.json
plugins/RealmApi/RealmApi.Core.dll
plugins/RealmApi/RealmApi.Hooks.dll
plugins/RealmApi/RealmApi.dll
```

Foram conferidos por metadados os **seis** binários extraídos dos quatro ZIPs. Na API, cada assembly tem `AssemblyVersion` e `AssemblyFileVersion` **0.1.1.0** e `AssemblyInformationalVersion` **0.1.1**. A constante compilada `ApiIdentity.Version` e o `[BepInPlugin]` valem **0.1.1**. As referências internas entre os assemblies da API também apontam para 0.1.1.0. No RSTV, o atributo compilado exige `com.gumatos.realmapi` **0.1.1** e as DLLs da API **não** são incluídas em seu ZIP.

### SHA-256 das DLLs: anterior → nova

| DLL | Anterior | Nova |
|---|---|---|
| RoguelikeDebugger.dll | `43aa414e300de4cd525ca5a636ffb301a3cb6642dd646a4144f9d6f6d6ccff96` | `28caed97b4f53d60747184bd34a6b4551d5bf618d9bd6b0b93c9453482a45f48` |
| RoguelikeSkillTreeVisualizer.dll | `cd1517f38fcfca957124d3e4d69d836906f43031f89d261e2319a5f8ec0fe346` | `65cfec276ccf548693c7b8bd20dd8ddfccfd006f1f3160ef9d6455516be47ff1` |
| RoguelikeUnlimitedLevelProgression.dll | `bff477bd26a85df06f0f1ee7887da429e3053a7c91b7434eb7ab158fe287e4e3` | `92313b7618933424f81df1d2fba3da154ede00e4851b6deb908ba37df0a69dde` |
| RealmApi.dll | `764b72d84a976a534292a518d14177b76fdede070bf9979e649efc5df25d19d7` | `2c9661584d5a3c9f393b1af598b7b0fbc35da21012f8bd4a6a201e3deaf0bcb8` |
| RealmApi.Core.dll | `d4e72f24e4e7c503bdd32c200b4bfa7635a1529b09451e2a35b5400547d32fb2` | `375ebc4a71f187a7e67afbe6d5a7e24bb89aa3c184960deaa0764e36778dac33` |
| RealmApi.Hooks.dll | `86d7fcf0012e1a611b42e96081609704a23a0129cc9918b3f1004c14a816778a` | `0be96b4106e2773f5079a88cf77cf370fc5211bd4dc22b40752a1e1d465a3a7c` |

## Execução e verificações reais

Saídas literais e resultados estruturados: `docs/automacao/BUMP-2-evidencias/` (**evidência local gitignored**, também entregue em arquivo no cartão; não são arquivos prometidos dentro dos ZIPs dos mods).

- `commands.json`: **12 comandos, todos exit 0**, com argv e hash do log.
- Quatro builds com `.NET SDK 6.0.428`, `-c Release -p:DeployToBepInEx=false --no-incremental`. **Zero erros**; API sem avisos, RD/RSTV/ULLP com um **MSB3277** cada (conflito de referência `System.Net.Http` 4.1.2.0/4.2.0.0 vindo das referências do jogo). Esses avisos não foram ocultados ou “corrigidos” fora do escopo.
- `python tools/check_versoes.py`: exit 0, **os 9 mods batem nos quatro lugares**. Esse gate lê o csproj do plugin da API; a inspeção adicional acima é que cobre também Core/Hooks compilados.
- Smoke da API reconstruído com o teste atualizado: **62 testes, zero falhas**, exit 0; só fixtures CLR e metadados, sem abrir o jogo.
- `python tools/pack-thunderstore.py <Mod> --so-conferir --config Release`: exit 0 para cada um dos quatro alvos.
- Empacotamento dos quatro alvos pelo empacotador existente: exit 0.
- `verification.json`: **101 verificações passaram, zero falhas**. Inclui quatro lugares, lista exata/CRC dos ZIPs, igualdade dos metadados e DLLs empacotadas com os arquivos de origem, versões compiladas, pin/mínimo do RSTV e comparação de IL limitada às strings de versão.
- Contraprovas em cópia isolada: base limpa exit 0; README propositalmente divergente exit 1; `ApiIdentity.Version` divergente exit 1. Fontes canônicos não foram usados para plantar defeitos.
- **41 arquivos de `plugins/` e `config/` do perfil idênticos antes/depois**, inclusive tamanho, SHA-256 e mtime. As **29 alterações/arquivos não rastreados alheios** encontrados no início foram preservados byte a byte; todos os ZIPs preexistentes de `dist/` permaneceram idênticos.
- `git diff --check` dos alvos: exit 0.

### Como reproduzir o caminho de build/pack

Na raiz do repositório, compilar a API **antes** do RSTV, pois ele referencia os assemblies Release da API:

```text
dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=false --no-incremental
dotnet build RoguelikeDebugger/RoguelikeDebugger.csproj -c Release -p:DeployToBepInEx=false --no-incremental
dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj -c Release -p:DeployToBepInEx=false --no-incremental
dotnet build RoguelikeUnlimitedLevelProgression/RoguelikeUnlimitedLevelProgression.csproj -c Release -p:DeployToBepInEx=false --no-incremental
python tools/check_versoes.py
python tools/pack-thunderstore.py RealmApi RoguelikeDebugger RoguelikeSkillTreeVisualizer RoguelikeUnlimitedLevelProgression --so-conferir --config Release
python tools/pack-thunderstore.py RealmApi RoguelikeDebugger RoguelikeSkillTreeVisualizer RoguelikeUnlimitedLevelProgression --config Release
```

O empacotador não faz ZIP determinístico por data: um novo rebuild/repack pode alterar o hash do contêiner. Para enviar **esta entrega**, usar os quatro arquivos identificados na tabela; após qualquer edição nova, reconstruir, reempacotar e recapturar os hashes.

## Limites e próximo ato

Não executei o jogo, não validei UI/gameplay/saves/multiplayer e não rodei o release-check completo do repositório. A entrega passou nos gates de versão/build/pacote e no smoke offline descritos, não equivale a uma homologação nova em jogo. As limitações anteriores dos READMEs não foram promovidas a testes concluídos.

A tarefa fica em revisão. Não haverá publicação automática decorrente desta entrega. Antes de publicar, o dono precisa trabalhar com a revisão aprovada, disponibilizar os ZIPs corretos como assets da Release e disparar cada mod separadamente, aprovando o Environment de cada envio. O ledger não foi atualizado com versões ou datas fictícias de publicação.
