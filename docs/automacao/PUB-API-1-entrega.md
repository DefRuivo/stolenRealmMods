# PUB-API-1 — preparação do RealmApi (16/10/2026)

## Rodada 2 (FINAL) — pacote montado e pre-flight verde

A rodada 1 parou porque o empacotador não conhecia o módulo. O pré-requisito foi resolvido na tarefa **PKG-API-1** (`t_d393f45a`), que ensinou packer/gate a lidar com o módulo aninhado de três DLLs. Esta rodada revalidou a preparação, corrigiu o que ficou desatualizado e **gerou o pacote**. Nada foi publicado, instalado ou enviado; `publicar` permanece `false`.

### Descoberta do pacote (executada primeiro)

```text
$ python tools/pack-thunderstore.py --listar-nomes
BetterCombatText
BetterFont
BetterPortuguese
BetterStats
BetterTooltips
RealmApi
RoguelikeDebugger
RoguelikeSkillTreeVisualizer
RoguelikeUnlimitedLevelProgression
exit=0
```

`RealmApi` aparece na ordem alfabética correta, entre `BetterTooltips` e `RoguelikeDebugger`.

### Pre-flight oficial (saída literal)

```text
$ python tools/pack-thunderstore.py --so-conferir
Repo : C:\dev\stolen-realm
Build: Release  (a DLL vem de <Mod>/bin/Release/netstandard2.1/)
Modo : --so-conferir  (pre-flight inteiro, NADA e empacotado)

== conferindo (artefato x fonte, build Release, versao unica, manifest, icon) ==
  ok    BetterCombatText   v0.1.3  | BetterCombatText\bin\Release\netstandard2.1\BetterCombatText.dll
  ok    BetterFont         v1.0.3  | BetterFont\bin\Release\netstandard2.1\BetterFont.dll
  ok    BetterPortuguese   v0.1.0  | BetterPortuguese\bin\Release\netstandard2.1\BetterPortuguese.dll
  ok    BetterStats        v1.0.2  | BetterStats\bin\Release\netstandard2.1\BetterStats.dll
  ok    BetterTooltips     v0.1.4  | BetterTooltips\bin\Release\netstandard2.1\BetterTooltips.dll
  ok    RealmApi           v0.1.0  | api\Plugin\bin\Release\netstandard2.1\RealmApi.dll
  ok    RoguelikeDebugger  v0.1.3  | RoguelikeDebugger\bin\Release\netstandard2.1\RoguelikeDebugger.dll
  ok    RoguelikeSkillTreeVisualizer v0.3.4  | RoguelikeSkillTreeVisualizer\bin\Release\netstandard2.1\RoguelikeSkillTreeVisualizer.dll
  ok    RoguelikeUnlimitedLevelProgression v0.1.1  | RoguelikeUnlimitedLevelProgression\bin\Release\netstandard2.1\RoguelikeUnlimitedLevelProgression.dll

Pre-flight verde para 9 mod(s). Nada foi empacotado (--so-conferir).
exit=0

$ python tools/pack-thunderstore.py RealmApi --so-conferir
  ok    RealmApi           v0.1.0  | api\Plugin\bin\Release\netstandard2.1\RealmApi.dll
Pre-flight verde para 1 mod(s). Nada foi empacotado (--so-conferir).
exit=0
```

O pre-flight cobriu versão única, manifest, ícone e atualidade artefato × fonte — para o pacote isolado e para os nove juntos.

### Empacotamento (saída literal)

```text
$ python tools/pack-thunderstore.py RealmApi
== empacotando ==
  RealmApi: gumatos-RealmApi-0.1.0.zip
      CHANGELOG.md                                  3851 bytes
      LICENSE                                       1074 bytes
      README.md                                    21943 bytes
      icon.png                                    107728 bytes
      manifest.json                                  440 bytes
      plugins/RealmApi/RealmApi.Core.dll           27136 bytes
      plugins/RealmApi/RealmApi.Hooks.dll           8704 bytes
      plugins/RealmApi/RealmApi.dll                12800 bytes
      TOTAL                                       183676 bytes  (8 arquivos)

PRONTO - 1 pacote(s) em dist/:
  C:\dev\stolen-realm\dist\gumatos-RealmApi-0.1.0.zip  (142513 bytes)
exit=0
```

### Nome exato do pacote

| Campo | Valor |
|---|---|
| `name` no manifest | `RealmApi` (mínimo 3 caracteres, só alfanumérico — validado) |
| Nome completo na Thunderstore | `DefRuivo_StolenRealmMods-RealmApi-0.1.0` (o namespace vem do **token**, não do zip) |
| Arquivo local | `dist/gumatos-RealmApi-0.1.0.zip`, 142513 bytes |
| SHA-256 do ZIP | `e13e725be6b84fd07b662a276d62285d1c7a6a0b5fdc88078e6fa7bbf3d4ee8b` |

O ZIP anterior (`de9352478f4411b5…`, gerado pelo PKG-API-1) foi substituído porque o README e o CHANGELOG mudaram nesta rodada; os 32 outros ZIPs de `dist/` ficaram **byte a byte iguais** (diff `dist-antes.txt` × `dist-depois.txt` = só a linha do RealmApi).

### Entrega — arquivos, bytes e SHA-256 (finais)

| Ação | Caminho absoluto | Bytes | SHA-256 |
|---|---|---:|---|
| Criado (rodada 1) | `C:/dev/stolen-realm/api/manifest.json` | 440 | `02b871daf08c36e15bcfc88581ff03ee34c8cce3c8156046becf73a8b0717493` |
| Instalado pelo dono | `C:/dev/stolen-realm/api/icon.png` | 107728 | `2b6673512d4250dbb42e18a62d53e2a283c82d9e1632dbf1087696fc25b03beb` |
| Editado (rodada 2) | `C:/dev/stolen-realm/api/CHANGELOG.md` | 3851 | `26d354098b2aa3b5b83c7f9a71f4b8ad318bb3fbc31aed1766bd6cd657b49058` |
| Editado (rodada 2) | `C:/dev/stolen-realm/api/README.md` | 21943 | `8d7a4fc236ec8a74d6dc826aad57e133b9bb83f8bac0dce29bb4d77774cd13d0` |
| Gerado (rodada 2) | `C:/dev/stolen-realm/dist/gumatos-RealmApi-0.1.0.zip` | 142513 | `e13e725be6b84fd07b662a276d62285d1c7a6a0b5fdc88078e6fa7bbf3d4ee8b` |

**Ícone do dono preservado.** `api/icon.png` continua com 107728 bytes e SHA-256 `2b6673512d4250dbb42e18a62d53e2a283c82d9e1632dbf1087696fc25b03beb` — o placeholder RA não existe mais em lugar nenhum. O mesmo arquivo entrou no ZIP (hash interno idêntico, dimensões 256×256 confirmadas nos bytes do IHDR).

### O que a rodada 2 mudou (e por quê)

1. `api/README.md`, bloco de pré-lançamento: dizia que “o empacotador ainda precisa reconhecer os três assemblies”. Já foi integrado pelo PKG-API-1 — agora afirma que o ZIP sai com os três em `plugins/RealmApi/`.
2. `api/README.md`, parágrafo do ícone: dizia ser **placeholder RA**. Substituído pela declaração do ícone oficial do autor.
3. `api/CHANGELOG.md`, bullet de identidade: a frase citava nominalmente a **API de terceiros** que o dono usava. Removido o nome, mantido o sentido (“identidade própria e independente”), pela regra do projeto de não referenciar o original em texto público.
4. `api/CHANGELOG.md`, bullet do ícone e parágrafo final: atualizados para ícone oficial e para o empacotador já integrado (antes dizia que o pacote dependia dessa integração).

Nada mais foi tocado: nenhum `.cs` da API, nenhum outro manifest, nem packer/gate/workflow/ledger — conferido por SHA-256 e por mtime (todos ≤ 13:45, anteriores ao início desta rodada às 14:00).

### Procedência das três DLLs (conferência própria, não confiança no log)

O packer busca as três em `api/Plugin/bin/Release/netstandard2.1/` (tabela `PACOTES_NAO_RAIZ`). Conferência byte a byte dos dois lados:

| DLL no ZIP | SHA-256 (16 hex) | Fonte real | Confere? |
|---|---|---|---|
| `plugins/RealmApi/RealmApi.dll` | `764b72d84a976a53` | `api/Plugin/bin/Release/netstandard2.1/RealmApi.dll` | sim |
| `plugins/RealmApi/RealmApi.Core.dll` | `d4e72f24e4e7c503` | saída real de `api/Core` (`bin/Release/netstandard2.0/`), cópia do plugin | sim |
| `plugins/RealmApi/RealmApi.Hooks.dll` | `86d7fcf0012e1a61` | saída real de `api/Hooks` (`bin/Release/netstandard2.0/`), cópia do plugin | sim |

`api/Core` e `api/Hooks` são `netstandard2.0`; a cópia em `api/Plugin/bin/Release/netstandard2.1/` bate exatamente com a saída real de cada um. Há um resíduo antigo `api/Core/bin/Release/netstandard2.1/RealmApi.Core.dll` (11264 bytes, 03:14) que **não** vai para o ZIP — nenhum artefato obsoleto foi empacotado. Nenhuma DLL do jogo, BepInEx, Harmony, Smoke ou Inspect entrou.

### Manifest e categoria (revalidados ao vivo)

- `name=RealmApi`, `version_number=0.1.0` (igual aos três `.csproj`, a `ApiIdentity.Version` e ao README — `tools/check_versoes.py` fechou com `os 9 mods batem nos quatro lugares`, exit 0), `dependencies=["BepInEx-BepInExPack-5.4.2305"]` (idêntico aos outros manifests), `website_url` = repositório do projeto, `extra.author="gumatos"`.
- Descrição própria em inglês, 165 caracteres (limite da plataforma: 250). Não copiada de terceiro.
- Categoria `["mods"]` revalidada no endpoint oficial: `GET https://thunderstore.io/api/experimental/community/stolen-realm/category/` → HTTP 200 com `[Audio, Misc, Libraries, Tools, Modpacks, Mods]` e slug `mods`. A listagem `GET https://thunderstore.io/c/stolen-realm/api/v1/package/` (26 pacotes) mostra 21 já publicados como `Mods`. **Enviar a categoria no metadata do upload continua sendo passo de publicação** — a chave no manifest não substitui isso.

### O que NÃO ficou pronto (e o motivo)

1. **`release/mods.json` sem entrada do RealmApi.** É o escopo do cartão filho **PUB-API-2** (`t_c15cf9d8`), que está destravado por este fechamento. O gate do `publish.yml` compara a lista completa e ordenada do ledger com a do empacotador **antes** de filtrar `publicar:true`; por isso a entrada tem de entrar junto com a descoberta já integrada, com `publicar:false`, `versao_publicada:null` e sem entrar em `ordem_de_envio`.
2. **Passo de envio no workflow.** Os seis uploads existentes do `publish.yml` não incluem o RealmApi: falta `choice` do mod no input, upload explícito e a categoria `mods` no metadata. Publicação é ato separado e não foi autorizada.
3. **Ordem de publicação.** `RoguelikeSkillTreeVisualizer` declara `DefRuivo_StolenRealmMods-RealmApi-0.1.0` e essa versão não existe publicada — a plataforma recusa dependência não resolvida, então o RealmApi sobe antes do RSTV. É ordenação, não layout.
4. **`tools/publish-thunderstore.sh:69` envia `Bearer ***` literal** (herança do PKG-API-1, fora do escopo aqui): precisa de tarefa própria antes de qualquer envio real.
5. **Runtime em jogo.** Nada foi instalado no perfil nem executado no jogo; BepInEx/Unity, gameplay, saves e multiplayer continuam não exercitados nesta preparação.

`publicar` permanece `false`; nada foi publicado, instalado, enviado ou empurrado.

---

> **Histórico — rodada 1 (12:44, superseded pelos itens acima).** Mantido como registro do bloqueio que originou o PKG-API-1. Onde este histórico diz que o pacote/pre-flight não existem, vale o resultado da rodada 2.

## Resultado

Preparados `api/manifest.json`, `api/icon.png`, `api/CHANGELOG.md` e a adaptação de `api/README.md` para uma página de pacote (apresentação, requisitos, instalação prevista, configuração, remoção, consumidores e limites). As referências à API de origem foram removidas do texto público. A documentação técnica existente foi preservada, com distinção entre caminhos do repositório e conteúdo de distribuição.

**Não há ZIP publicável e o pre-flight oficial não passou.** O empacotador não conhece o módulo. Conforme a regra da tarefa (“se não conhecer, diga o que falta em vez de forçar”), não foi alterado o packer nem criada uma pasta/projeto falso na raiz. Não houve compilação, instalação, upload, push ou alteração de código da API nesta rodada.

## Nome e versão

- Nome preparado no manifest: `RealmApi`.
- Versão real: `0.1.0`, igual nos três `.csproj`, em `ApiIdentity.Version`, no README e no atributo BepInEx da DLL existente (assembly version `0.1.0.0`).
- GUID: `com.gumatos.realmapi`.
- ZIP esperado segundo o prefixo do packer: `gumatos-RealmApi-0.1.0.zip` — **não gerado**.
- O nome não é, hoje, uma opção reconhecida pelo packer. Portanto não se afirma que exista nome aceito pelo empacotador para a API.
- Namespace de publicação registrado para o projeto: `DefRuivo_StolenRealmMods`. Isso não é uma publicação realizada nem uma confirmação de disponibilidade remota do nome.

## Arquivos entregues e SHA-256

| Ação | Caminho absoluto | Bytes | SHA-256 |
|---|---|---:|---|
| Criado | `C:/dev/stolen-realm/api/manifest.json` | 440 | `02b871daf08c36e15bcfc88581ff03ee34c8cce3c8156046becf73a8b0717493` |
| Criado | `C:/dev/stolen-realm/api/icon.png` | 942 | `c1ac80c0338a58c9b465ccf2080a7d3d9f8afd369ccc390696498c1da06fa095` |
| Criado | `C:/dev/stolen-realm/api/CHANGELOG.md` | 2328 | `ef3255793f11829b60fa975afad32571cf1d6fdbd296b5c4bedc5aaf3d952bf9` |
| Adaptado | `C:/dev/stolen-realm/api/README.md` | 21972 | `eb246c296304b7fdef2579c8111c8a5f364cee4ed35494aed3d0f975631227b6` |

Ícone: placeholder original RA, fundo e moldura simples, 256×256 RGB. Usa o gerador existente do packer com glifo A fornecido apenas em memória nesta execução; o arquivo do packer não foi alterado. Dimensões, CRCs e descompressão do PNG conferidos; inspeção visual também realizada. Não é arte final nem logotipo do jogo.

Manifest: descrição própria em inglês (165 caracteres), dependência exata `BepInEx-BepInExPack-5.4.2305`, website do repositório, `categories: ["mods"]` e `extra.author: "gumatos"`, seguindo a convenção de autor dos outros manifests.

A categoria foi reconferida por GET anônimo no endpoint oficial `https://thunderstore.io/api/experimental/community/stolen-realm/category/`: HTTP 200, entre os resultados `{"name":"Mods","slug":"mods"}`. O JSON bruto está nas evidências (`categories-live.json`). **A chave no manifest não substitui o envio da categoria no metadata de publicação.** A integração futura deve enviar `mods` para `stolen-realm` explicitamente; não foi criado passo de upload nesta tarefa.

## Saída literal da descoberta — executada antes das alterações

Comando, na raiz `C:/dev/stolen-realm`:

```text
python tools/pack-thunderstore.py --listar-nomes
```

Exit 0:

```text
BetterCombatText
BetterFont
BetterPortuguese
BetterStats
BetterTooltips
RoguelikeDebugger
RoguelikeSkillTreeVisualizer
RoguelikeUnlimitedLevelProgression
```

A descoberta foi repetida e continuou sem a API.

## Saída literal do pre-flight oficial

```text
python tools/pack-thunderstore.py RealmApi --so-conferir
```

Exit 2:

```text
!! nao existe mod com esse nome: RealmApi
   mods disponiveis: BetterCombatText, BetterFont, BetterPortuguese, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer, RoguelikeUnlimitedLevelProgression
```

A recusa acontece na seleção do alvo, **antes** de `verificar()`; não é um pre-flight de pacote aprovado.

## Saída literal do empacotamento

```text
python tools/pack-thunderstore.py RealmApi
```

Exit 2:

```text
!! nao existe mod com esse nome: RealmApi
   mods disponiveis: BetterCombatText, BetterFont, BetterPortuguese, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer, RoguelikeUnlimitedLevelProgression
```

Nenhum ZIP da API em `dist/`. Não houve chamada a `empacotar()` com caminhos forçados.

## Checagens suplementares (não substituem o pre-flight)

O script de auditoria das evidências retornou:

```text
Supplemental checks: 22 passed; 0 failed. Official packer remains blocked before validation.
```

Inclui JSON/campos/descrição/dependência/autor/categoria; coerência de versão fonte/manifest/README/DLL; PNG válido; ausência de referência à API de origem nos textos públicos; consumidores documentados; e preservação dos arquivos protegidos. Conferência UI com metadados extraídos de novo: 5 tipos, 21 métodos, zero divergências, controle negativo encontrou 2 problemas. A ferramenta existente de comparação foi importada e usada sem sobrescrever suas evidências no repositório.

Smoke offline executado sobre as DLLs já existentes, sem rebuild:

```text
api/Smoke/bin/Release/net472/RealmApi.Smoke.exe C:/dev/stolen-realm/lib/Assembly-CSharp.dll C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll
```

Exit 0, final da saída:

```text
Ran 62 tests; failures: 0
NAO_EXERCITADO: BepInEx/Unity runtime, gameplay, saves, multiplayer; somente CLR fixtures + metadados locais.
```

`git diff --check -- api`: exit 0. A comparação SHA-256 com a fotografia inicial confirmou que, dentre os arquivos preexistentes da API e os manifests/packer/gate/workflow protegidos, somente `api/README.md` mudou. Os três arquivos novos são os explicitamente pedidos. Alterações de outras frentes já presentes no repositório não foram revertidas nem incorporadas.

Hashes das DLLs existentes (não foram recompiladas nem incluídas em pacote):

| DLL em `api/Plugin/bin/Release/netstandard2.1/` | SHA-256 |
|---|---|
| `RealmApi.dll` | `764b72d84a976a534292a518d14177b76fdede070bf9979e649efc5df25d19d7` |
| `RealmApi.Core.dll` | `d4e72f24e4e7c503bdd32c200b4bfa7635a1529b09451e2a35b5400547d32fb2` |
| `RealmApi.Hooks.dll` | `86d7fcf0012e1a611b42e96081609704a23a0129cc9918b3f1004c14a816778a` |

## O que falta no packer e pipeline

1. **Descoberta e caminhos lógicos.** `eh_mod()` / `descobrir_mods()` só aceitam `<Nome>/<Nome>.csproj` na raiz. O projeto real é `api/Plugin/RealmApi.csproj`, com metadados em `api/`. É necessário mapear `RealmApi` explicitamente a essa estrutura sem renomear código ou fabricar `RealmApi/RealmApi.csproj`.
2. **Três assemblies, dois TFMs.** `caminhos()` e `empacotar()` hoje presumem uma DLL por pacote em `<Nome>/bin/Release/netstandard2.1/`. A API exige `RealmApi.dll`, `RealmApi.Core.dll` e `RealmApi.Hooks.dll` juntos em `plugins/RealmApi/`. Core e Hooks têm fonte/build em `netstandard2.0`; os três também estão copiados na saída do plugin. É preciso escolher e validar a origem de cada um, sem incluir DLLs do jogo, BepInEx, Harmony, Smoke ou Inspect. A distribuição MIT também deve preservar o aviso de licença existente (`api/LICENSE`), por inclusão do arquivo ou do texto apropriado.
3. **Versão do plugin.** `versao_do_plugin()` procura `Plugin.cs` e a constante dentro do mesmo arquivo. O real é `api/Plugin/RealmApiPlugin.cs`, com atributo usando `ApiIdentity.Version`, declarado em `api/Core/Contracts.cs`. Esse caminho não pode ser resolvido com a regex atual.
4. **Atualidade dos três artefatos.** A trava de artefato/fonte precisa cobrir as fontes e os projetos transitivos de Core/Hooks/Plugin, não só a pasta do plugin ou o `api/` inteiro incluindo as ferramentas.
5. **Gate de release sem liberação.** `release/mods.json` **ainda não tem entrada RealmApi**. Não existe, portanto, um literal `publicar:false` da API para afirmar que foi preservado. Nenhum `true` foi criado e o gate foi mantido byte a byte. Registrar apenas a entrada agora quebraria a igualdade entre lista JSON e descoberta que o workflow exige. Quando a descoberta for integrada, cadastrar `RealmApi` na mesma mudança, em ordem, com `publicar:false`, `versao_publicada:null`, `publicado_em:null` e motivo explícito. Não incluir em `ordem_de_envio`.
6. **Workflow.** O workflow também presume `<Nome>/<Nome>.csproj` e `<Nome>/manifest.json` em vários passos, não oferece RealmApi no input nem possui passo de envio dele. A futura integração deve usar os caminhos canônicos da API e levar `categories: mods` no envio. Adicionar um nome/booleano isolado não resolve esses pontos. Nada disso foi habilitado ou executado nesta preparação.

## Limites e roteamento

ZIP, pre-flight oficial verde, registro literal `publicar:false` e integração no pipeline permanecem pendentes pelos motivos acima. Não se afirma que o mod esteja pronto para upload. Runtime no jogo continua fora do escopo e não foi executado.

A tarefa pede relatar a falta do empacotador, não forçá-lo. Uma continuação de engenharia do packer/gate precisa de escopo e roteamento próprios. `hermes profile list` retornou apenas `default`, o perfil deste executor; não foi inventado um especialista nem atribuída uma filha ao próprio executor. As evidências e os arquivos preparados ficam disponíveis para essa decisão.

Evidências brutas: `C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_daf5efde/` contém `discovery.stdout.txt`, `preflight.stdout.txt`, `pack.stdout.txt`, os JSONs de comandos/exit codes, `smoke.stdout.txt`, `plugin-metadata.stdout.txt`, `ui-metadata.stdout.txt`, `categories-live.json`, `verification.json`, `baseline.json`, o README anterior para comparação e `verify_package_prep.py`. Esses são arquivos locais da execução; o anexo de evidências do cartão preserva uma cópia, sem ser pacote de instalação.
