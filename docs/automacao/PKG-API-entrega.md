# PKG-API-1 - o packer e o gate aprendem o RealmApi (modulo aninhado, multi-DLL)

Tarefa: `t_d393f45a` (kanban). Objetivo: ensinar `tools/pack-thunderstore.py` e o gate do
`.github/workflows/publish.yml` a empacotar o **RealmApi**, que nao segue o layout dos
outros mods, sem mudar nada do que os oito ja fazem. Nada foi publicado, nada foi
instalado no perfil e `release/mods.json` **nao foi alterado** (a entrada e' de PUB-API-2).

## 1. A premissa violada (arquivo + linha)

A descoberta de pacote e' do `eh_mod`, em `tools/pack-thunderstore.py`:

```
tools/pack-thunderstore.py (ANTES)  linhas 248-265
248  def eh_mod(nome):
249      """Mod de verdade = pasta na raiz com `<Mod>/<Mod>.csproj` que tenha o target
250      `DeployToBepInEx` ...
254      pasta = os.path.join(RAIZ, nome)
255      if not os.path.isdir(pasta):
256          return False
257      csproj = os.path.join(pasta, nome + ".csproj")
258      if not os.path.isfile(csproj):
259          return False
```

Sao **duas** premissas de layout na mesma funcao, e o RealmApi viola as duas:

1. **`<Mod>/<Mod>.csproj` na raiz.** O projeto da API e' `api/Plugin/RealmApi.csproj`:
   aninhado um nivel abaixo (`api/` guarda os metadados, `api/Plugin/` o projeto) e com o
   nome do csproj igual ao do **assembly**, nao ao da pasta. `eh_mod("RealmApi")` procura
   `RealmApi/RealmApi.csproj` na raiz, nao acha e devolve `False` -> o pacote nunca entra
   em `descobrir_mods()` -> `--listar-nomes` listava **oito** nomes sem ele.
2. **Uma DLL por pacote.** `caminhos()` montava um unico
   `<Mod>/bin/<Config>/netstandard2.1/<Mod>.dll`, e `verificar()`/`empacotar()` tratavam
   esse unico arquivo como o conteudo de `plugins/<Mod>/`. A build da API produz **tres**
   assemblies na mesma pasta de saida: `RealmApi.dll` (o plugin) + `RealmApi.Core.dll` +
   `RealmApi.Hooks.dll` (as referencias de projeto que o BepInEx precisa resolver ao
   carregar o plugin - sem elas o plugin nao sobe).

Ainda a mesma premissa, em outros dois lugares do caminho (tambem corrigidos):

- `eh_mod` era o unico item de layout que o gate do `publish.yml` NAO reescrevia... mas o
  pre-flight e o registro **sim**: `publish.yml` (ANTES) linhas 430, 466 e 966 liam
  `'%s/%s.csproj' % (nome, nome)` e `'%s/manifest.json' % nome` na mao.
- `.github/scripts/valida_pacotes.py` (ANTES, linha 193) exigia `manifest.name == pasta do
  mod`: com `api/manifest.json` (`name: RealmApi`) a pasta `api` reprovava o check de
  metadados (era o `FALHA api` do passo 8 do `validate.yml`).

Consequencia medida antes da mudanca: `--listar-nomes` = 8 nomes (exit 0); adicionar so' a
entrada no ledger fazia o gate comparar listas e **reprovar TODOS os alvos**
(`::error::release/mods.json e o empacotador divergem`), nao so' os mods novos.

## 2. O que foi mudado

### 2.1 `tools/pack-thunderstore.py` - tabela explicita de pacote NAO-RAIZ

Em vez de afrouxar o `eh_mod` (heuristica que poderia classificar `api/Smoke` ou
`api/tools/Inspect` como pacote), o caso entra numa **tabela**: `PACOTES_NAO_RAIZ`, com
`metadados`, `projeto`, `csproj`, `pasta_no_zip`, `dlls` (DLL -> pasta-fonte que a trava
REL-1 confere) e `extras` (o `LICENSE` entra na raiz do zip). O resto do script passou a
falar com `p["dlls"]`/`p["fontes_por_dll"]`/`p["versao_em"]`/`p["pasta_no_zip"]`/`p["extras"]`
- chaves que no layout padrao valem exatamente o de antes (uma DLL, uma pasta de fonte, o
`Plugin.cs`, `extras` vazio), e por isso os oito empacotam igual.

Mudancas por funcao:

- `PACOTES_NAO_RAIZ` (novo): a tabela do RealmApi, documentada com o porque de cada campo.
- `rel()` (novo): caminho relativo a raiz com `/` (mesmo formato no Windows e no CI).
- `caminhos()`: monta os caminhos do layout nao-raiz; no layout padrao devolve as mesmas
  chaves de antes **mais** as novas.
- `eh_pacote_nao_raiz()` (novo) e `descobrir_mods()`: lista = raiz (via `eh_mod`) UNIAO da
  tabela, em ordem alfabetica GLOBAL -> `RealmApi` entra entre os "R".
- `artefato_esta_atual()` (REL-1): confere **cada** DLL contra a fonte mais nova do projeto
  DELA (Plugin/Core/Hooks), nao contra a arvore `api/` inteira (um `.cs` do smoke e' mais
  novo que a DLL e reprovaria pacote bom).
- `versao_do_plugin()`: varre todos os arquivos de `versao_em` e devolve tambem **onde**
  achou - o `[BepInPlugin]` esta em `api/Plugin/RealmApiPlugin.cs` e a const
  (`ApiIdentity.Version`) em `api/Core/Contracts.cs`.
- `conferir_versoes()` / `sincronizar_versao()`: usam o arquivo devolvido por
  `versao_do_plugin` (no layout padrao, o mesmo `Plugin.cs`).
- `verificar()`: exige **todas** as DLLs do pacote e tambem os `extras`.
- `empacotar()`: copia todas as DLLs para `plugins/<pasta_no_zip>/` e os `extras` na raiz.
- `mapa_de_caminhos()` + `--listar-caminhos` (novos): JSON com `nome`, `nao_raiz`, `csproj`,
  `manifest`, `dlls` e `dentro_do_zip` de cada pacote - a fonte que os gates consultam para
  nao reescrever caminho de layout padrao na mao.
- `--listar`: bloco novo "Pacotes NAO-RAIZ" DEPOIS dos dois blocos de sempre (a saida dos
  oito continua byte a byte igual).

### 2.2 `.github/workflows/publish.yml`

- **Gate (job `libera`)**: a comparacao `nomes_pack != nomes_json` (literal) virou
  DIRECIONAL. Nome no ledger que o empacotador nao conhece continua **erro** (e' defeito:
  rename/typo deixaria alvo apontando para o nada). Nome que o empacotador conhece e o
  ledger ainda nao decidiu virou **AVISO** na tabela do resumo ("sem entrada -> nunca e'
  enviado"): a pasta nasce com o codigo, a decisao de publicar vem depois - e com a
  comparacao literal uma pasta nova deixava o pipeline INTEIRO vermelho.
- **Pre-flight (passo 4)** e **registro (job `registra`)**: o `.csproj` e o `manifest.json`
  de cada alvo e a lista do que tem de existir DENTRO do zip passam a vir de
  `tools/pack-thunderstore.py --listar-caminhos` (antes eram `'%s/%s.csproj' % (nome, nome)`
  e `'plugins/%s/%s.dll' % (nome, nome)`).
- Nada de publicacao, de token ou de ordem de envio foi tocado.

### 2.3 `tools/publish-thunderstore.sh` (publicador local)

- **Passo 0 novo - ledger**: le `release/mods.json` + `--listar-caminhos`, imprime o estado
  de cada pacote (`LIBERADO`/`TRAVADO`, com o motivo) e escreve o plano de envio. So os
  `publicar:true` sao empacotados e enviados; TRAVADO e "sem entrada no ledger" aparecem na
  tabela e **nunca** entram. Antes o passo 5 subia o que estivesse em `dist/` (o ledger nao
  era lido em lugar nenhum).
- **Token**: validado como sempre quando existe; deixa de ser OBRIGATORIO no dry-run (quem
  envia e' o `--go`). Era o que impedia ver o plano numa maquina sem credencial.
- O resto (trava de segredo, `release-check`, upload, codigos de saida) esta igual - a linha
  do `curl` inclusive, inclusive o `Bearer ***` literal dela (ver "Achados fora de escopo").

### 2.4 `tools/check_versoes.py` e `.github/scripts/valida_pacotes.py`

- `check_versoes.py`: adaptado a assinatura nova de `versao_do_plugin` (3 valores) e o
  rotulo passou a nomear o arquivo onde a versao foi achada (`Contracts.cs  const Version =`
  no RealmApi; `Plugin.cs` nos oito). Sem isso o `release-check` quebrava no passo 1.
- `valida_pacotes.py`: o `name` do manifest passa a ser comparado com o nome do **pacote**
  (que vem de `--listar-caminhos`), nao com o da pasta de metadados - o `api/` guarda o
  pacote `RealmApi`. Sem o empacotador, cai no comportamento antigo (nome da pasta).

## 3. Evidencia: ZIP do RealmApi

`gumatos-RealmApi-0.1.0.zip` - sha256 `de9352478f4411b5ad5e7ec4f001140ff65d13d7a5cfe5a157f624b9c2a570a9`, 142471 bytes, 8 membros:

| membro | bytes | sha256 |
|---|---|---|
| `CHANGELOG.md` | 3754 | `a7a276750343c05a315ee33d43b4dd55...` |
| `LICENSE` | 1074 | `09b0670f8aa43e8977ef9d26ed451379...` |
| `README.md` | 21972 | `eb246c296304b7fdef2579c8111c8a5f...` |
| `icon.png` | 107728 | `2b6673512d4250dbb42e18a62d53e2a2...` |
| `manifest.json` | 440 | `02b871daf08c36e15bcfc88581ff03ee...` |
| `plugins/RealmApi/RealmApi.Core.dll` | 27136 | `d4e72f24e4e7c503bdd32c200b4bfa76...` |
| `plugins/RealmApi/RealmApi.Hooks.dll` | 8704 | `86d7fcf0012e1a611b42e96081609704...` |
| `plugins/RealmApi/RealmApi.dll` | 12800 | `764b72d84a976a534292a518d14177b7...` |

Bytes DENTRO do zip iguais aos do repositorio (conferido byte a byte):

- `manifest.json` == `api/manifest.json`: IGUAL
- `README.md` == `api/README.md`: IGUAL
- `CHANGELOG.md` == `api/CHANGELOG.md`: IGUAL
- `icon.png` == `api/icon.png`: IGUAL
- `LICENSE` == `api/LICENSE`: IGUAL
- `plugins/RealmApi/RealmApi.dll` == `api/Plugin/bin/Release/netstandard2.1/RealmApi.dll`: IGUAL
- `plugins/RealmApi/RealmApi.Core.dll` == `api/Plugin/bin/Release/netstandard2.1/RealmApi.Core.dll`: IGUAL
- `plugins/RealmApi/RealmApi.Hooks.dll` == `api/Plugin/bin/Release/netstandard2.1/RealmApi.Hooks.dll`: IGUAL

## 4. Evidencia: nao-regressao dos oito

Duas provas independentes.

**(a) Fotografia antes/depois** (`snapshot.py`: cada um dos oito rodado no empacotador
ANTES da mudanca e depois, com os mesmos comandos):

| mod | exit antes/depois | zip sha256 antes | zip sha256 depois | zip | entrada mudou? |
|---|---|---|---|---|---|
| BetterCombatText | 0/0 | `fd9ec52f6744dc25` | `cd8b98ef10afeec6` | **mudou** | `BetterCombatText/CHANGELOG.md` |
| BetterFont | 0/0 | `e76903c8828b3c07` | `e76903c8828b3c07` | **identico** | nao |
| BetterPortuguese | 0/0 | `669b54a6ad1627a9` | `669b54a6ad1627a9` | **identico** | nao |
| BetterStats | 0/0 | `656d279fa015b657` | `656d279fa015b657` | **identico** | nao |
| BetterTooltips | 0/0 | `33bdf60d8f8fac27` | `33bdf60d8f8fac27` | **identico** | nao |
| RoguelikeDebugger | 0/0 | `337519166c607417` | `337519166c607417` | **identico** | nao |
| RoguelikeSkillTreeVisualizer | 0/0 | `3280dad47f000d15` | `4914860bdc4e56bf` | **mudou** | `RoguelikeSkillTreeVisualizer/CHANGELOG.md` |
| RoguelikeUnlimitedLevelProgression | 1/1 | `-` | `-` | sem zip nos dois (reprova igual) | nao |

Leitura: 6 dos 8 saem **byte a byte iguais** (zip e saida do empacotador) antes/depois.
Dois deles (`BetterCombatText`, `RoguelikeSkillTreeVisualizer`) tem o **CHANGELOG.md
editado no disco por outro trabalho** durante a janela (mtime posterior ao inicio desta
tarefa) - o zip mudou porque a ENTRADA mudou, nao o empacotador. `RoguelikeDebugger` e
`RoguelikeUnlimitedLevelProgression` aparecem no instantaneo em que a fotografia foi tirada
com a fonte editada depois da ultima build (REL-1); o comportamento do empacotador nos dois
e' identico antes/depois, e o workspace segue vivo (o dono builda e bumpa versao em
paralelo: no fechamento desta tarefa `BetterCombatText` ja estava em 0.1.3,
`RoguelikeDebugger` em 0.1.3 e `RoguelikeSkillTreeVisualizer` em 0.3.4). Por isso a prova
decisiva e' a (b), que nao depende do disco parar de mudar.

**Estado no FECHAMENTO desta tarefa** (`--so-conferir`, ja' com as versoes novas do dono):
o pre-flight esta **verde para os NOVE pacotes**, incluindo o RealmApi -
`>>> Pre-flight verde para 9 mod(s). Nada foi empacotado (--so-conferir).`

**(b) Arvore CONGELADA** (`freeze_test.py`) - a prova que nao depende do disco mudar: as
entradas dos oito sao COPIADAS para uma arvore temporaria (mtimes preservados) e o MESMO
conjunto e' empacotado pelos dois empacotadores (de antes e de depois). Resultado:

arvore congelada em %USERPROFILE%\AppData\Local\Temp\pkg-api-1-freeze-e4cnhigs

== empacotando com o empacotador de ANTES ==
== empacotando com o empacotador de DEPOIS ==

mod                                  exitA exitD sha256 do zip      veredito
BetterCombatText                     0     0     cd8b98ef10afeec6=  ok (zip identico)
BetterFont                           0     0     e76903c8828b3c07=  ok (zip identico)
BetterPortuguese                     0     0     669b54a6ad1627a9=  ok (zip identico)
BetterStats                          0     0     656d279fa015b657=  ok (zip identico)
BetterTooltips                       0     0     33bdf60d8f8fac27=  ok (zip identico)
RoguelikeDebugger                    1     1     n/a=               ok (reprova igual nos dois)
RoguelikeSkillTreeVisualizer         0     0     4914860bdc4e56bf=  ok (zip identico)
RoguelikeUnlimitedLevelProgression   1     1     n/a=               ok (reprova igual nos dois)

VEREDITO: 8/8 sem regressao

## 5. Evidencia: gate do `publish.yml` (Python extraido do workflow e executado)

`harness_gate.py` extrai o heredoc do workflow, confere a sintaxe de TODOS os blocos Python
do arquivo e roda o gate nos tres estados que importam:

== blocos Python dentro do workflow: 5 ==
  linha 156   Gate dos mods liberados                                    sintaxe ok
  linha 360   ?                                                          sintaxe ok
  linha 651   5.0 Prepara um diretorio de envio por mod (a Action move   sintaxe ok
  linha 798   ?                                                          sintaxe ok
  linha 977   ?                                                          sintaxe ok

== 1) ledger de HOJE (8) x empacotador de NOVE ==
::warning::o empacotador conhece mod(s) sem entrada em release/mods.json: RealmApi. Sem entrada nao ha decisao de publicacao e o mod NAO e enviado (os alvos saem do ledger). Se ele ja pode ser publicado, cadastre a entrada com publicar:true.

alvos: BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer

team : DefRuivo_StolenRealmMods
exit=0

== 2) ledger CANDIDATO (RealmApi publicar:false) + empacotador de NOVE ==
alvos: BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer

team : DefRuivo_StolenRealmMods
exit=0

ledger restaurado byte a byte: antes=42e63efaa0872663053c96cbba8db34490be9be187cfb23f0f1bd3301da4127d depois=42e63efaa0872663053c96cbba8db34490be9be187cfb23f0f1bd3301da4127d  IGUAL

== 3) ledger com nome FANTASMA (RoguelikeRenomeado) ==
::error::release/mods.json lista mod(s) que o empacotador NAO conhece: RoguelikeRenomeado. A lista de mods tem uma fonte so (`tools/pack-thunderstore.py --listar-nomes`) e um nome que ela nao devolve e um alvo que nao existe. JSON=['BetterCombatText', 'BetterFont', 'BetterPortuguese', 'BetterStats', 'BetterTooltips', 'RoguelikeRenomeado', 'RoguelikeSkillTreeVisualizer', 'RoguelikeUnlimitedLevelProgression'] | empacotador=['BetterCombatText', 'BetterFont', 'BetterPortuguese', 'BetterStats', 'BetterTooltips', 'RealmApi', 'RoguelikeDebugger', 'RoguelikeSkillTreeVisualizer', 'RoguelikeUnlimitedLevelProgression']
exit=1
ledger restaurado: IGUAL

## 6. Evidencia: dry-run do publicador local

`bash tools/publish-thunderstore.sh` (sem `--go`) - o RealmApi aparece como **TRAVADO**:

```
== ledger (release/mods.json + tools/pack-thunderstore.py) ==
  pacote                             estado    detalhe
  BetterCombatText                   LIBERADO  publicar:true
  BetterFont                         LIBERADO  publicar:true
  BetterPortuguese                   TRAVADO   BLOQUEADO para publicacao (BP-4): implementacao 0.1.0 validada somente offline, com Original/Corrigido completos. Corrigido ainda e no-op por ausencia de aprovacoes LANG; registro de mods vazio. Exige aprovacoes editoriais, QA em jogo BP-5 autorizada e aceite humano; build verde nao libera upload.
  BetterStats                        LIBERADO  publicar:true
  BetterTooltips                     LIBERADO  publicar:true
  RoguelikeDebugger                  LIBERADO  publicar:true
  RoguelikeSkillTreeVisualizer       LIBERADO  publicar:true
  RoguelikeUnlimitedLevelProgression TRAVADO   BLOQUEADO para publicacao (LEVEL-PACOTE-CONTRATO, 12/10/2026): runtime e aceite humano pendentes. O pacote 0.1.1 tem fonte/metadados/icone 256x256 versionados e passou o pre-flight em bancada NOVA isolada (sem perfil, sem jogo), com manifest, icone, membros e hash da DLL conferidos dentro do ZIP - prova de CONTRATO, nao de jogo: nenhum boot real foi exercitado. Liberar exige rodada de runtime autorizada e o aceite humano do dono; ate la nao entra no lote de envio (ordem_de_envio).
  RealmApi                           TRAVADO   sem entrada em release/mods.json - nunca e enviado

  liberados: 6 | travados no ledger: 2 | sem entrada no ledger: 1
  pedido   : todos os liberados
  vao subir: BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer
== trava de segredo ==
arquivos versionados analisados: 1790
arquivos em area de teste no momento: 158
  ==> nenhum padrao de credencial encontrado
arquivos versionados analisados: 1790
  (25 binario(s) fora do heuristico de entropia; os formatos conhecidos foram procurados neles tambem)
formatos conhecidos: 13 | limiar de entropia: 4.0 bits/char | comprimento minimo: 32
  ==> nenhum padrao de credencial encontrado

== trava de release (tools/release-check.sh) ==

==============================================================================
 RELEASE-CHECK — 2026-10-16 13:51:00
 raiz do repo : /c/dev/stolen-realm
 jogo         : E:\SteamLibrary\steamapps\common\Stolen Realm (AppID 1330000)
 log BepInEx  : $HOME/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log
 python       : Python 3.14.7
 MODO         : fluxo normal (verificacao SEM escrever no perfil do dono)
==============================================================================

== PREPARO: dispensado — o fluxo normal NAO instala nada (o jogo pode ficar aberto) ==

== PASSO 0/9 — SEGREDOS ==
arquivos versionados analisados: 1790
arquivos em area de teste no momento: 158
  ==> nenhum padrao de credencial encontrado
arquivos versionados analisados: 1790
  (25 binario(s) fora do heuristico de entropia; os formatos conhecidos foram procurados neles tambem)
formatos conhecidos: 13 | limiar de entropia: 4.0 bits/char | comprimento minimo: 32
  ==> nenhum padrao de credencial encontrado
  [ OK ] 0. nenhum token nos arquivos versionados

== PASSO 1/9 — VERSOES (check_versoes.py: csproj = manifest = Plugin.cs) ==
   repo : C:\dev\stolen-realm
   mods : 9 (BetterCombatText, BetterFont, BetterPortuguese, BetterStats, BetterTooltips, RealmApi, RoguelikeDebugger, RoguelikeSkillTreeVisualizer, RoguelikeUnlimitedLevelProgression)
   fora : ReloadProbe (tem csproj mas nao sao mod)
   
   BetterCombatText
     BetterCombatText.csproj  <Version>             0.1.2
     manifest.json  version_number                  0.1.2
     Plugin.cs  const Versao =                      0.1.2
     README.md  - **Version:**                      0.1.2
   
   BetterFont
     BetterFont.csproj  <Version>                   1.0.3
     manifest.json  version_number                  1.0.3
     Plugin.cs  [BepInPlugin(...)]                  1.0.3
     README.md  - **Version:**                      1.0.3
   
   BetterPortuguese
     BetterPortuguese.csproj  <Version>             0.1.0
     manifest.json  version_number                  0.1.0
     Plugin.cs  [BepInPlugin(...)]                  0.1.0
     README.md  - **Version:**                      0.1.0
   
   BetterStats
     BetterStats.csproj  <Version>                  1.0.2
     manifest.json  version_number                  1.0.2
     Plugin.cs  [BepInPlugin(...)]                  1.0.2
     README.md  - **Version:**                      1.0.2
   
   BetterTooltips
     BetterTooltips.csproj  <Version>               0.1.4
     manifest.json  version_number                  0.1.4
     Plugin.cs  [BepInPlugin(...)]                  0.1.4
     README.md  - **Version:**                      0.1.4
   
   RealmApi
     RealmApi.csproj  <Version>                     0.1.0
     manifest.json  version_number                  0.1.0
     Contracts.cs  const Version =                  0.1.0
     README.md  - **Version:**                      0.1.0
   
   RoguelikeDebugger
     RoguelikeDebugger.csproj  <Version>            0.1.2
     manifest.json  version_number                  0.1.2
     Plugin.cs  [BepInPlugin(...)]                  0.1.2
     README.md  - **Version:**                      0.1.2
   
   RoguelikeSkillTreeVisualizer
     RoguelikeSkillTreeVisualizer.csproj  <Version> 0.3.3
     manifest.json  version_number                  0.3.3
     Plugin.cs  const Version =                     0.3.3
     README.md  - **Version:**                      0.3.3
   
   RoguelikeUnlimitedLevelProgression
     RoguelikeUnlimitedLevelProgression.csproj  <Version> 0.1.1
     manifest.json  version_number                  0.1.1
     Plugin.cs  const PluginVersion =               0.1.1
     README.md  - **Version:**                      0.1.1
   
     ==> os 9 mods batem nos quatro lugares (csproj = manifest = Plugin.cs = README)

== PASSO 2/9 — PATCHES (trava TRV-1: 5 regras de robustez do Harmony) ==
   repo   : C:\dev\stolen-realm
   mods   : 9 (BetterCombatText, BetterFont, BetterPortuguese, BetterStats, BetterTooltips, RealmApi, RoguelikeDebugger, RoguelikeSkillTreeVisualizer, RoguelikeUnlimitedLevelProgression)
   harness: ReloadProbe (tem Plugin.cs e entra na trava, mas nao e pacote Thunderstore)
   alvos  : 9 projetos (6 com patch Harmony) | 72 arquivos .cs (bin/ e obj/ fora)
   
   == REGRA 1: parametro posicional do Harmony (__0/__1/__2/...) ==
     ok      nenhum parametro posicional declarado em patch nenhum
     -> 0 sem justificativa, 0 justificado(s) (aviso)
   == REGRA 2: assinatura por TIPO em todo [HarmonyPatch] (typeof/nameof) ==
     -> 51 de 51 classes de patch com assinatura por TIPO
   == REGRA 3: todo Prefix/Postfix dentro de try/catch ==
     AVISO   RoguelikeDebugger/Patches/FlameShrineProcPatch.cs:661  Prefix  (patch sem try/catch (nem por delegacao))
     AVISO   RoguelikeUnlimitedLevelProgression/Patches/GameplayPatches.cs:43  Transpiler  (patch sem try/catch (nem por delegacao))
     AVISO   RoguelikeUnlimitedLevelProgression/Patches/UiPatches.cs:34  Finalizer  (patch sem try/catch (nem por delegacao))
     AVISO   RoguelikeUnlimitedLevelProgression/Patches/UiPatches.cs:119  Finalizer  (patch sem try/catch (nem por delegacao))
     -> 58 de 62 metodos de patch protegidos
   == REGRA 4: marcador de vida no boot ('... carregado.') ==
     ok      BetterCombatText/Plugin.cs:42  log de carregamento presente
     ok      BetterFont/Plugin.cs:160  log de carregamento presente
     REPROVA BetterPortuguese/Plugin.cs  (sem linha de 'carregado' em LogInfo/Log)
     ok      BetterStats/Plugin.cs:33  log de carregamento presente
     ok      BetterTooltips/Plugin.cs:37  log de carregamento presente
     ok      ReloadProbe/Plugin.cs:10  log de carregamento presente
     ok      RoguelikeDebugger/Plugin.cs:30  log de carregamento presente
     ok      RoguelikeSkillTreeVisualizer/Plugin.cs:254  log de carregamento presente
     ok      RoguelikeUnlimitedLevelProgression/Plugin.cs:31  log de carregamento presente
     -> 8 de 9 Plugin.cs com marcador de vida
   == REGRA 5: aplicacao gancho a gancho (nao PatchAll() puro) e cobertura dos ganchos ==
     ok      BetterCombatText               aplicador proprio — 9 classe(s) de patch, 9 metodo(s) de gancho (9 por nome, 0 por atributo); filtro EhClasseDeGancho aceita todos (nao exige atributo no metodo)
     ok      BetterFont                     aplicador proprio — 1 classe(s) de patch, 1 metodo(s) de gancho (1 por nome, 0 por atributo); filtro EhClasseDeGancho aceita todos (nao exige atributo no metodo)
     n/a     BetterPortuguese               sem [HarmonyPatch] no projeto (nao aplica gancho)
     ok      BetterStats                    aplicador proprio — 2 classe(s) de patch, 2 metodo(s) de gancho (2 por nome, 0 por atributo); filtro EhClasseDeGancho aceita todos (nao exige atributo no metodo)
     ok      BetterTooltips                 aplicador proprio — 7 classe(s) de patch, 14 metodo(s) de gancho (11 por nome, 3 por atributo); filtro EhClasseDeGancho aceita todos (nao exige atributo no metodo)
     n/a     ReloadProbe                    sem [HarmonyPatch] no projeto (nao aplica gancho)
     ok      RoguelikeDebugger              aplicador proprio — 14 classe(s) de patch, 16 metodo(s) de gancho (16 por nome, 0 por atributo); filtro EhClasseDeGancho aceita todos (nao exige atributo no metodo)
     AVISO   RoguelikeSkillTreeVisualizer   EhClasseDeGancho exige atributo no metodo e nao cita os nomes Prefix/Postfix: hoje 15 classe(s) de patch, 16 metodo(s) de gancho (0 por nome, 16 por atributo), mas um gancho novo por convencao de nome seria ignorado em silencio
     n/a     RoguelikeUnlimitedLevelProgression sem [HarmonyPatch] no projeto (nao aplica gancho)
     -> 5 de 6 projetos com patch usam aplicador proprio cobrindo os ganchos (0 reprova(m), 1 aviso(s))
   
   CONTAGEM: 9 projeto(s) | 72 arquivo(s) .cs | 1 achado(s) que REPROVAM | 5 aviso(s)
   >>> TRAVA REPROVADA (TRV-1) <<<
       BetterPortuguese/Plugin.cs:-  BetterPortuguese  ->  nenhuma linha 'carregado' em LogInfo/Log
       Sem a linha de 'carregado' o teste de ciclo nao tem como saber se o
       plugin subiu - o silencio parece sucesso.

  [FALHA] 2. patch reprovado pela TRV-1 — release travada
   >>> BLOQUEIO DE RELEASE (TRV-1) <<<
   Os achados acima apontam arquivo:linha. Um parametro posicional do Harmony
tools/release-check.sh: line 249: ref: command not found
   () aponta para o argumento ERRADO quando a assinatura do jogo muda, e o
   defeito COMPILA: so aparece em jogo, como NullReferenceException em serie (112 por
   frame no caso que originou esta trava). Sem o marcador de boot '... carregado.' o
   teste de ciclo nao tem como saber que o plugin subiu — o silencio parece sucesso,
   e patch sem try/catch inunda o log a cada quadro.
   Correcao: use o NOME do parametro, declare a assinatura por TIPO (typeof/nameof),
   mantenha Prefix/Postfix em try/catch e logue a linha de carregamento no Plugin.cs.
   Nada foi buildado e nada foi instalado no perfil: conserte e rode de novo.
!! release-check falhou; nada foi publicado
```

O run completo (com a trava de release pulada, porque ela reprova hoje num mod de OUTRO
trabalho - ver secao 8) mostra o plano de envio: seis pacotes, nenhum travado:

```
== ledger (release/mods.json + tools/pack-thunderstore.py) ==
  pacote                             estado    detalhe
  BetterCombatText                   LIBERADO  publicar:true
  BetterFont                         LIBERADO  publicar:true
  BetterPortuguese                   TRAVADO   BLOQUEADO para publicacao (BP-4): implementacao 0.1.0 validada somente offline, com Original/Corrigido completos. Corrigido ainda e no-op por ausencia de aprovacoes LANG; registro de mods vazio. Exige aprovacoes editoriais, QA em jogo BP-5 autorizada e aceite humano; build verde nao libera upload.
  BetterStats                        LIBERADO  publicar:true
  BetterTooltips                     LIBERADO  publicar:true
  RoguelikeDebugger                  LIBERADO  publicar:true
  RoguelikeSkillTreeVisualizer       LIBERADO  publicar:true
  RoguelikeUnlimitedLevelProgression TRAVADO   BLOQUEADO para publicacao (LEVEL-PACOTE-CONTRATO, 12/10/2026): runtime e aceite humano pendentes. O pacote 0.1.1 tem fonte/metadados/icone 256x256 versionados e passou o pre-flight em bancada NOVA isolada (sem perfil, sem jogo), com manifest, icone, membros e hash da DLL conferidos dentro do ZIP - prova de CONTRATO, nao de jogo: nenhum boot real foi exercitado. Liberar exige rodada de runtime autorizada e o aceite humano do dono; ate la nao entra no lote de envio (ordem_de_envio).
  RealmApi                           TRAVADO   sem entrada em release/mods.json - nunca e enviado

  liberados: 6 | travados no ledger: 2 | sem entrada no ledger: 1
  pedido   : todos os liberados
  vao subir: BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer
== trava de segredo ==
arquivos versionados analisados: 1790
arquivos em area de teste no momento: 158
  ==> nenhum padrao de credencial encontrado
arquivos versionados analisados: 1790
  (25 binario(s) fora do heuristico de entropia; os formatos conhecidos foram procurados neles tambem)
formatos conhecidos: 13 | limiar de entropia: 4.0 bits/char | comprimento minimo: 32
  ==> nenhum padrao de credencial encontrado

== empacotando (so os LIBERADOS: quem manda e' o ledger) ==
Repo : C:\dev\stolen-realm
Saida: C:\dev\stolen-realm\dist
Mods : BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer
Build: Release  (a DLL vem de <Mod>/bin/Release/netstandard2.1/)

== conferindo (build Release, versao unica, manifest, icon) ==
  ok    BetterCombatText   v0.1.2  | BetterCombatText\bin\Release\netstandard2.1\BetterCombatText.dll
  ok    BetterFont         v1.0.3  | BetterFont\bin\Release\netstandard2.1\BetterFont.dll
  ok    BetterStats        v1.0.2  | BetterStats\bin\Release\netstandard2.1\BetterStats.dll
  ok    BetterTooltips     v0.1.4  | BetterTooltips\bin\Release\netstandard2.1\BetterTooltips.dll
  ok    RoguelikeDebugger  v0.1.2  | RoguelikeDebugger\bin\Release\netstandard2.1\RoguelikeDebugger.dll
  ok    RoguelikeSkillTreeVisualizer v0.3.3  | RoguelikeSkillTreeVisualizer\bin\Release\netstandard2.1\RoguelikeSkillTreeVisualizer.dll

== empacotando ==
  BetterCombatText: gumatos-BetterCombatText-0.1.2.zip
      CHANGELOG.md                                 24637 bytes
      README.md                                     7060 bytes
      icon.png                                    124954 bytes
      manifest.json                                  452 bytes
      plugins/BetterCombatText/BetterCombatText.dll   50176 bytes
      TOTAL                                       207279 bytes  (5 arquivos)
  BetterFont: gumatos-BetterFont-1.0.3.zip
      CHANGELOG.md                                 22262 bytes
      README.md                                     6389 bytes
      icon.png                                     87821 bytes
      manifest.json                                  455 bytes
      plugins/BetterFont/BetterFont.dll            34816 bytes
      TOTAL                                       151743 bytes  (5 arquivos)
  BetterStats: gumatos-BetterStats-1.0.2.zip
      CHANGELOG.md                                  4219 bytes
      README.md                                     2799 bytes
      icon.png                                     91250 bytes
      manifest.json                                  422 bytes
      plugins/BetterStats/BetterStats.dll          10752 bytes
      TOTAL                                       109442 bytes  (5 arquivos)
  BetterTooltips: gumatos-BetterTooltips-0.1.4.zip
      CHANGELOG.md                                 22421 bytes
      README.md                                     5688 bytes
      icon.png                                    100373 bytes
      manifest.json                                  449 bytes
      plugins/BetterTooltips/BetterTooltips.dll   184320 bytes
      TOTAL                                       313251 bytes  (5 arquivos)
  RoguelikeDebugger: gumatos-RoguelikeDebugger-0.1.2.zip
      CHANGELOG.md                                  9401 bytes
      README.md                                     4136 bytes
      icon.png                                     99954 bytes
      manifest.json                                  422 bytes
      plugins/RoguelikeDebugger/RoguelikeDebugger.dll   68096 bytes
      TOTAL                                       182009 bytes  (5 arquivos)
  RoguelikeSkillTreeVisualizer: gumatos-RoguelikeSkillTreeVisualizer-0.3.3.zip
      CHANGELOG.md                                 22790 bytes
      README.md                                     8228 bytes
      icon.png                                     57013 bytes
      manifest.json                                  559 bytes
      plugins/RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.dll  101376 bytes
      TOTAL                                       189966 bytes  (5 arquivos)

PRONTO - 6 pacote(s) em dist/:
  C:\dev\stolen-realm\dist\gumatos-BetterCombatText-0.1.2.zip  (157833 bytes)
  C:\dev\stolen-realm\dist\gumatos-BetterFont-1.0.3.zip  (114529 bytes)
  C:\dev\stolen-realm\dist\gumatos-BetterStats-1.0.2.zip  (100872 bytes)
  C:\dev\stolen-realm\dist\gumatos-BetterTooltips-0.1.4.zip  (163851 bytes)
  C:\dev\stolen-realm\dist\gumatos-RoguelikeDebugger-0.1.2.zip  (136142 bytes)
  C:\dev\stolen-realm\dist\gumatos-RoguelikeSkillTreeVisualizer-0.3.3.zip  (108162 bytes)

Instalar: no r2modman, aba 'Online' -> 'Install from file' -> escolha o zip
(ou faca upload no thunderstore.io com os mesmos arquivos).

== envio ==
   [DRY-RUN] subiria: gumatos-BetterCombatText-0.1.2.zip (157833 bytes) -> https://thunderstore.io/api/experimental/package/upload/
   [DRY-RUN] subiria: gumatos-BetterFont-1.0.3.zip (114529 bytes) -> https://thunderstore.io/api/experimental/package/upload/
   [DRY-RUN] subiria: gumatos-BetterStats-1.0.2.zip (100872 bytes) -> https://thunderstore.io/api/experimental/package/upload/
   [DRY-RUN] subiria: gumatos-BetterTooltips-0.1.4.zip (163851 bytes) -> https://thunderstore.io/api/experimental/package/upload/
   [DRY-RUN] subiria: gumatos-RoguelikeDebugger-0.1.2.zip (136142 bytes) -> https://thunderstore.io/api/experimental/package/upload/
   [DRY-RUN] subiria: gumatos-RoguelikeSkillTreeVisualizer-0.3.3.zip (108162 bytes) -> https://thunderstore.io/api/experimental/package/upload/

== DRY-RUN terminou. Nada foi publicado. Use --go para publicar de verdade. ==
```

## 7. Hashes (antes x agora)

| arquivo | sha256 ANTES | sha256 AGORA | mudou |
|---|---|---|---|
| `tools/pack-thunderstore.py` | `1b02a9e27643d841` | `791f6809397ee04b` | **SIM** |
| `tools/publish-thunderstore.sh` | `3dd11a5b58f110fa` | `ba3d3da8d7d981a1` | **SIM** |
| `.github/workflows/publish.yml` | `e922636740bd6c17` | `821058917ad1ae3e` | **SIM** |
| `.github/workflows/validate.yml` | `2b5c229c98bffbca` | `2b5c229c98bffbca` | nao |
| `.github/scripts/valida_pacotes.py` | `4dadbf060d5a37de` | `8d8ab8801c11fd91` | **SIM** |
| `tools/check_versoes.py` | `-` | `33c56f6e58ee0c4e` | novo/criado por outra tarefa |
| `release/mods.json` | `42e63efaa0872663` | `42e63efaa0872663` | nao |
| `api/manifest.json` | `02b871daf08c36e1` | `02b871daf08c36e1` | nao |
| `api/icon.png` | `2b6673512d4250db` | `2b6673512d4250db` | nao |
| `api/README.md` | `eb246c296304b7fd` | `eb246c296304b7fd` | nao |
| `api/CHANGELOG.md` | `a7a276750343c05a` | `a7a276750343c05a` | nao |
| `api/LICENSE` | `09b0670f8aa43e89` | `09b0670f8aa43e89` | nao |

`release/mods.json` e os arquivos de `api/` (manifest, icon, README, CHANGELOG, LICENSE)
ficaram intactos - a entrada do ledger e' de PUB-API-2 e o pacote nao foi tocado.

## 8. Limites, achados e o que NAO foi feito

1. **`release/mods.json` nao foi alterado** (trava da tarefa). Consequencia: ate PUB-API-2
   aplicar a entrada, o gate emite o AVISO de "mod sem entrada no ledger" e o dry-run mostra
   `RealmApi TRAVADO - sem entrada em release/mods.json`. Com a entrada `publicar:false` o
   gate fecha sem aviso (medido: caso 2 do harness). A entrada **nao pode** ser adicionada
   sem este trabalho: era exatamente o caso que reprovava o gate inteiro.
2. **`validate.yml` nao precisou de mudanca**: o passo 9 (empacotador) so' chama
   `--listar-nomes`, que agora devolve nove; o passo 8 (`valida_pacotes`) foi corrigido
   para o layout nao-raiz.
3. **PKG-5 continua vermelho de proposito**: `valida_pacotes.py` segue reprovando com
   `RoguelikeSkillTreeVisualizer: depende de DefRuivo_StolenRealmMods-RealmApi-0.1.0, que NAO
   existe na Thunderstore`. E' a regra de ordem de publicacao (dependencia sobe ANTES do
   dependente) e ela esta certa: enquanto o RealmApi nao for publicado, o RSTV nao pode ser.
   Nada disso e' layout - fica para a tarefa de publicacao.
4. **`check_patches.py` NAO audita o codigo da API**: ele varre pastas de raiz com
   `Plugin.cs`, e o plugin da API esta em `api/Plugin/`. O `mods : 9` que ele imprime agora
   conta o RealmApi, mas as 5 regras TRV-1 nao olham os `.cs` dele. E' um furo ANTERIOR a
   esta tarefa (o `api/` nunca esteve nesse caminho) - apontado aqui para nao passar em
   branco, nao corrigido porque ampliar o escopo do check e' decisao propria.
5. **Achado fora de escopo, NAO corrigido**: `tools/publish-thunderstore.sh:69` envia
   `-H "Authorization: Bearer ***"` literal - o token lido nunca chega ao `curl`, entao o
   `--go` local falharia com 401. A linha foi preservada byte a byte nesta tarefa de
   proposito (mexer nela e' mudar o caminho de envio, e testar isso e' publicar). Precisa de
   tarefa propria.
6. **`publish.yml` input `mod:` continua com as seis opcoes de sempre** (nao inclui RealmApi,
   nem BetterPortuguese, nem RoguelikeUnlimitedLevelProgression). E' coerente com o estado do
   ledger hoje (so' os seis tem `publicar:true`); o disparo manual so' chega la' depois que
   a decisao humana liberar o mod.
7. **`tools/pack-for-friends.sh` e `BetterPortuguese/package.py`** foram conferidos: o
   primeiro chama o packer por linha de comando (sem contrato interno) e o segundo usa
   `verificar()` e `paths['dll']`, que continuam valendo - `BetterPortuguese/package.py
   --check-only` roda `PREFLIGHT OK 12 members; 4 version mirrors; both snapshots` (exit 0).
8. **Formato do caminho dentro do ZIP**: as DLLs vao para `plugins/RealmApi/`, o MESMO
   formato dos oito (o `plugins/` do pacote e' o `BepInEx/plugins/` depois de instalar), e o
   pre-flight do `publish.yml` confere exatamente esses membros.

## 9. Como reproduzir

```
cd <repo>
python tools/pack-thunderstore.py --listar-nomes        # 9 nomes, RealmApi entre os R
python tools/pack-thunderstore.py --listar              # + bloco "Pacotes NAO-RAIZ"
python tools/pack-thunderstore.py --listar-caminhos     # JSON com o layout de cada pacote
python tools/pack-thunderstore.py RealmApi              # gera dist/gumatos-RealmApi-0.1.0.zip
python tools/pack-thunderstore.py --so-conferir         # pre-flight dos nove
python tools/check_versoes.py                           # 9 mods x 4 espelhos (exit 0)
python .github/scripts/valida_pacotes.py                # metadados (so' o PKG-5 fica vermelho)
bash tools/publish-thunderstore.sh                      # DRY-RUN: tabela com RealmApi TRAVADO
```


## Anexo A - diff de `tools/pack-thunderstore.py`

```diff
diff --git a/tools/pack-thunderstore.py b/tools/pack-thunderstore.py
index d88e6c9..3bc5283 100644
--- a/tools/pack-thunderstore.py
+++ b/tools/pack-thunderstore.py
@@ -19,6 +19,22 @@ pacote .zip na pasta `dist/` seguindo a convencao do Thunderstore:
 Os arquivos ficam na RAIZ do zip (nao dentro de uma pasta) - e assim que o r2modman
 espera encontrar o manifest.json.
 
+LAYOUT NAO-RAIZ (PKG-API-1)
+---------------------------
+Nem todo pacote do repo segue esse layout. O `RealmApi` e' um modulo ANINHADO: o projeto
+do plugin vive em `api/Plugin/RealmApi.csproj` (o csproj carrega o nome do ASSEMBLY, nao
+o da pasta) e a build produz TRES assemblies - o plugin (`RealmApi.dll`) mais as duas
+referencias de projeto que ele carrega em runtime (`RealmApi.Core.dll`,
+`RealmApi.Hooks.dll`). Os metadados do pacote (`manifest.json`, `icon.png`,
+`README.md`, `CHANGELOG.md`, `LICENSE`) ficam em `api/`, um nivel acima do projeto.
+
+Esse caso nao cabe no `eh_mod` (que procura `<Mod>/<Mod>.csproj` na raiz e uma DLL so) e
+por isso vive numa tabela EXPLICITA - `PACOTES_NAO_RAIZ`: quem entra ali e' decisao
+registrada, nao heuristica. O pacote que sai e' o MESMO dos outros oito (metadados na
+raiz do zip, DLLs em `plugins/<Pacote>/`); o que muda e' so ONDE os arquivos nascem no
+repositorio e QUANTAS DLLs entram. O gate de `release/mods.json` continua vendo os nove
+pacotes pela MESMA lista (`--listar-nomes`).
+
 CONFIGURACAO DO BUILD (PKG-6)
 -----------------------------
 O pacote sai da build de **Release** por padrao (`--config Release`), que e a que passou
@@ -241,6 +257,60 @@ def gerar_icone(nome_mod, destino, tamanho=256):
     return len(dados)
 
 
+# ---------------------------------------------------------------------------
+# PACOTES NAO-RAIZ (PKG-API-1) - modulo aninhado, mais de uma DLL
+# ---------------------------------------------------------------------------
+# O detector `eh_mod` cobre o layout padrao: pasta na raiz, `<Mod>/<Mod>.csproj`, uma
+# DLL em `bin/<Config>/netstandard2.1/`. O RealmApi viola DUAS dessas premissas de uma
+# vez:
+#
+#   1. o projeto NAO esta na raiz - vive em `api/Plugin/`, e o nome do csproj e' o do
+#      ASSEMBLY (`RealmApi.csproj`), nao o da pasta (`Plugin`);
+#   2. a build produz TRES DLLs, nao uma: `RealmApi.dll` (o plugin) mais
+#      `RealmApi.Core.dll` e `RealmApi.Hooks.dll` - as duas referencias de projeto que o
+#      BepInEx precisa resolver ao carregar o plugin (sem elas o plugin nao sobe). As
+#      tres saem da MESMA pasta de saida (`api/Plugin/bin/<Config>/netstandard2.1/`).
+#
+# Por isso este caso e' TABELA, nao palpite do detector: cada entrada diz onde estao os
+# metadados, onde esta o csproj, quais DLLs entram e em que pasta elas vao para dentro
+# do zip. Nao ha heuristica que "descubra" isso sem risco de classificar como pacote
+# alguma pasta que nao e' - `api/Smoke` e' harness de teste e `api/tools/Inspect` e'
+# ferramenta de bancada; nenhum dos dois vira pacote.
+#
+# `dlls` tambem diz, por DLL, QUAL e' a fonte que a trava REL-1 confere (segundo item de
+# cada par): a DLL do plugin contra `api/Plugin/`, a Core contra `api/Core/`, a Hooks
+# contra `api/Hooks/`. Conferir as tres contra a arvore `api/` inteira reprovaria pacote
+# bom - um `.cs` do smoke, que nem entra no zip, e' mais novo que a DLL.
+PACOTES_NAO_RAIZ = {
+    "RealmApi": {
+        # Manifest, icone, README, CHANGELOG, LICENSE.
+        "metadados": ("api",),
+        # Pasta do .csproj e da saida da build.
+        "projeto": ("api", "Plugin"),
+        "csproj": "RealmApi.csproj",
+        # Pasta que recebe as DLLs dentro do zip: plugins/RealmApi/.
+        "pasta_no_zip": "RealmApi",
+        "dlls": (
+            ("RealmApi.dll", ("api", "Plugin")),
+            ("RealmApi.Core.dll", ("api", "Core")),
+            ("RealmApi.Hooks.dll", ("api", "Hooks")),
+        ),
+        # Onde a versao aparece fora do .csproj: o [BepInPlugin] esta no arquivo do
+        # plugin e a const que ele cita (`ApiIdentity.Version`) mora no Core - dois
+        # arquivos, nao um (o layout padrao usa so o Plugin.cs).
+        "versao_em": (("api", "Plugin", "RealmApiPlugin.cs"),
+                      ("api", "Core", "Contracts.cs")),
+        # Arquivo a mais na RAIZ do zip alem dos quatro de sempre.
+        "extras": ("LICENSE",),
+    },
+}
+
+
+def rel(caminho):
+    """Caminho relativo a raiz do repo, com '/' - o que o zip e os gates usam."""
+    return os.path.relpath(caminho, RAIZ).replace(os.sep, "/")
+
+
 # ---------------------------------------------------------------------------
 # Descoberta dos mods
 # ---------------------------------------------------------------------------
@@ -277,21 +347,72 @@ def projetos_ignorados():
     return ignorados
 
 
+def eh_pacote_nao_raiz(nome):
+    """O pacote esta na tabela PACOTES_NAO_RAIZ (modulo aninhado, multi-DLL)?"""
+    return nome in PACOTES_NAO_RAIZ
+
+
 def descobrir_mods():
-    """Todos os mods do repo, em ordem alfabetica."""
-    return [entrada for entrada in sorted(os.listdir(RAIZ))
-            if eh_mod(entrada)]
+    """Todos os pacotes do repo, em ordem alfabetica GLOBAL.
+
+    Soma o que o detector acha na raiz (`eh_mod`) com o que esta declarado na tabela
+    PACOTES_NAO_RAIZ. A ordem e' alfabetica sobre o conjunto todo (nao "raiz primeiro"):
+    e' ESTA lista, nesta ordem, que o gate do `publish.yml` compara com o `nome` de cada
+    entrada do `release/mods.json` - entao no ledger o RealmApi entra entre os "R"
+    (antes de RoguelikeDebugger: 'e' < 'o').
+    """
+    na_raiz = [entrada for entrada in os.listdir(RAIZ) if eh_mod(entrada)]
+    return sorted(set(na_raiz) | set(PACOTES_NAO_RAIZ))
 
 
 def caminhos(nome_mod, config=CONFIG_PADRAO):
+    """Todos os caminhos do pacote - no layout padrao ou no nao-raiz (PKG-API-1).
+
+    As chaves que o resto do script consome sao as MESMAS nos dois casos:
+    `dlls` (todas as DLLs que entram no zip: uma no layout padrao, tres no RealmApi),
+    `fontes_por_dll` (a fonte que a trava REL-1 confere para CADA DLL),
+    `versao_em` (os arquivos que carregam a versao alem do .csproj),
+    `pasta_no_zip` (a pasta em plugins/ que recebe as DLLs) e `extras` (arquivos a mais
+    na raiz do zip - vazio no layout padrao).
+    """
+    especial = PACOTES_NAO_RAIZ.get(nome_mod)
+    if especial:
+        meta = os.path.join(RAIZ, *especial["metadados"])
+        projeto = os.path.join(RAIZ, *especial["projeto"])
+        dlls, fontes_por_dll = [], {}
+        for nome, pastas in especial["dlls"]:
+            dll = os.path.join(projeto, "bin", config, TFM, nome)
+            dlls.append(dll)
+            fontes_por_dll[dll] = [os.path.join(RAIZ, *p) for p in pastas]
+        return {
+            "pasta": meta,                          # onde vivem os metadados
+            "csproj": os.path.join(projeto, especial["csproj"]),
+            "dll": dlls[0],
+            "dlls": dlls,
+            "fontes_por_dll": fontes_por_dll,
+            "versao_em": [os.path.join(RAIZ, *f) for f in especial["versao_em"]],
+            "pasta_no_zip": especial["pasta_no_zip"],
+            "extras": [os.path.join(meta, extra) for extra in especial["extras"]],
+            "manifest": os.path.join(meta, "manifest.json"),
+            "readme": os.path.join(meta, "README.md"),
+            "changelog": os.path.join(meta, "CHANGELOG.md"),
+            "icon": os.path.join(meta, "icon.png"),
+        }
+
     pasta = os.path.join(RAIZ, nome_mod)
+    # PKG-6: o caminho da DLL segue a CONFIGURACAO, igual ao $(Configuration) do
+    # MSBuild (bin/<Config>/netstandard2.1/). Antes era fixo em bin/Debug e o pacote
+    # publicado saia da build errada.
+    dll = os.path.join(pasta, "bin", config, TFM, nome_mod + ".dll")
     return {
         "pasta": pasta,
         "csproj": os.path.join(pasta, nome_mod + ".csproj"),
-        # PKG-6: o caminho da DLL segue a CONFIGURACAO, igual ao $(Configuration) do
-        # MSBuild (bin/<Config>/netstandard2.1/). Antes era fixo em bin/Debug e o pacote
-        # publicado saia da build errada.
-        "dll": os.path.join(pasta, "bin", config, TFM, nome_mod + ".dll"),
+        "dll": dll,
+        "dlls": [dll],
+        "fontes_por_dll": {dll: [pasta]},
+        "versao_em": [os.path.join(pasta, "Plugin.cs")],
+        "pasta_no_zip": nome_mod,
+        "extras": [],
         "manifest": os.path.join(pasta, "manifest.json"),
         "plugin": os.path.join(pasta, "Plugin.cs"),
         "readme": os.path.join(pasta, "README.md"),
@@ -429,63 +550,84 @@ def quando(mtime):
 
 
 def artefato_esta_atual(nome_mod, p, config=CONFIG_PADRAO):
-    """A DLL de `bin/<Config>/` corresponde a fonte que esta no repositorio?
+    """TODAS as DLLs do pacote correspondem a fonte que esta no repositorio?
+
+    Levanta `Falha` quando uma DLL e' MAIS ANTIGA que o arquivo de fonte mais novo que
+    entra na compilacao DELA - a fonte mudou depois do ultimo build, e o pacote sairia
+    com um binario que nao tem a edicao. No layout padrao ha uma DLL so; no pacote
+    nao-raiz (PKG-API-1) ha uma por projeto, e cada uma e' conferida contra a fonte do
+    projeto DELA (`fontes_por_dll`).
 
-    Levanta `Falha` quando a DLL e MAIS ANTIGA que o arquivo de fonte mais novo do mod -
-    a fonte mudou depois do ultimo build, e o pacote sairia com um binario que nao tem a
-    edicao. Devolve `(mtime_dll, fonte_mais_nova)` quando tudo bate.
+    Devolve a lista `(mtime_dll, fonte_mais_nova)` por DLL quando tudo bate.
     """
-    mtime_dll = os.path.getmtime(p["dll"])
-    fontes = fontes_do_mod(p["pasta"])
-    if not fontes:
-        return mtime_dll, None
-
-    mais_nova = max(fontes, key=os.path.getmtime)
-    mtime_fonte = os.path.getmtime(mais_nova)
-    if mtime_dll < mtime_fonte:
-        raise Falha(
-            "ARTEFATO VELHO (REL-1): a DLL de bin/%s/ e MAIS ANTIGA que a fonte\n"
-            "      DLL   : %s  (%s)\n"
-            "      FONTE : %s  (%s)\n"
-            "      -> o pacote sairia com um binario SEM a edicao acima. Reconstrua a\n"
-            "         partir da FONTE. NUNCA sem a flag: o alvo DeployToBepInEx do .csproj\n"
-            "         copia a DLL para o perfil do r2modman e o jogo passa a rodar o build.\n"
-            "         dotnet build %s/%s.csproj -c %s -p:DeployToBepInEx=false"
-            % (config,
-               os.path.relpath(p["dll"], RAIZ), quando(mtime_dll),
-               os.path.relpath(mais_nova, RAIZ), quando(mtime_fonte),
-               nome_mod, nome_mod, config))
-    return mtime_dll, mais_nova
+    conferidas = []
+    for dll in p["dlls"]:
+        mtime_dll = os.path.getmtime(dll)
+        fontes = []
+        for pasta in p["fontes_por_dll"][dll]:
+            fontes.extend(fontes_do_mod(pasta))
+        if not fontes:
+            conferidas.append((mtime_dll, None))
+            continue
+
+        mais_nova = max(fontes, key=os.path.getmtime)
+        mtime_fonte = os.path.getmtime(mais_nova)
+        if mtime_dll < mtime_fonte:
+            raise Falha(
+                "ARTEFATO VELHO (REL-1): a DLL de bin/%s/ e MAIS ANTIGA que a fonte\n"
+                "      DLL   : %s  (%s)\n"
+                "      FONTE : %s  (%s)\n"
+                "      -> o pacote sairia com um binario SEM a edicao acima. Reconstrua a\n"
+                "         partir da FONTE. NUNCA sem a flag: o alvo DeployToBepInEx do .csproj\n"
+                "         copia a DLL para o perfil do r2modman e o jogo passa a rodar o build.\n"
+                "         dotnet build %s -c %s -p:DeployToBepInEx=false"
+                % (config,
+                   os.path.relpath(dll, RAIZ), quando(mtime_dll),
+                   os.path.relpath(mais_nova, RAIZ), quando(mtime_fonte),
+                   rel(p["csproj"]), config))
+        conferidas.append((mtime_dll, mais_nova))
+    return conferidas
 
 
 def versao_do_plugin(nome_mod, p):
-    """A versao que o BepInEx registra no log, lida do `Plugin.cs`.
+    """A versao que o BepInEx registra no log, lida dos arquivos de versao do pacote.
 
     Mesmo criterio de `tools/audita_docs.py` (o CI cobra esse formato): o literal pode
     estar no proprio atributo - `[BepInPlugin("guid", "nome", "0.1.0")]` - ou numa
     constante usada como ultimo argumento - `[BepInPlugin(Guid, "nome", Version)]` com
-    `public const string Version = "0.1.0";` (padrao do RoguelikeSkillTreeVisualizer).
+    `public const string Version = "0.1.0";` (padrao do RoguelikeSkillTreeVisualizer e,
+    tambem, do RealmApi - onde o atributo esta em `api/Plugin/RealmApiPlugin.cs` e a
+    const `ApiIdentity.Version`, em `api/Core/Contracts.cs`; por isso a busca varre
+    TODOS os arquivos de `versao_em`, nunca um so).
 
-    Devolve `(versao, nome_da_constante)`; `(None, None)` quando nao acha.
+    Devolve `(versao, nome_da_constante, arquivo)`; `(None, None, None)` quando nao acha.
+    O arquivo e' o que carrega o literal - e' nele que `--sincronizar-versao` escreve.
     """
-    if not os.path.isfile(p["plugin"]):
-        return None, None
-    with open(p["plugin"], encoding="utf-8", errors="replace") as fh:
-        fonte = fh.read()
-
-    literal = re.search(r'Plugin\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"', fonte)
-    if literal:
-        return literal.group(3), None
-
-    atributo = re.search(r"\[BepInPlugin\(([^)]*)\)\]", fonte)
-    if atributo:
+    textos = []
+    for caminho in p["versao_em"]:
+        if os.path.isfile(caminho):
+            with open(caminho, encoding="utf-8", errors="replace") as fh:
+                textos.append((caminho, fh.read()))
+
+    for caminho, fonte in textos:
+        literal = re.search(r'Plugin\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"', fonte)
+        if literal:
+            return literal.group(3), None, caminho
+
+    for _caminho, fonte in textos:
+        atributo = re.search(r"\[BepInPlugin\(([^)]*)\)\]", fonte)
+        if not atributo:
+            continue
         ident = re.search(r",\s*([A-Za-z_][\w.]*)\s*$", atributo.group(1).strip())
-        if ident:
-            nome = ident.group(1).split(".")[-1]
-            const = re.search(r'const\s+string\s+%s\s*=\s*"([^"]+)"' % re.escape(nome), fonte)
+        if not ident:
+            continue
+        nome = ident.group(1).split(".")[-1]
+        for caminho_const, fonte_const in textos:
+            const = re.search(r'const\s+string\s+%s\s*=\s*"([^"]+)"' % re.escape(nome),
+                              fonte_const)
             if const:
-                return const.group(1), nome
-    return None, None
+                return const.group(1), nome, caminho_const
+    return None, None, None
 
 
 def conferir_versoes(nome_mod, p, manifesto):
@@ -504,12 +646,12 @@ def conferir_versoes(nome_mod, p, manifesto):
                     % fonte)
 
     no_manifest = manifesto["version_number"]
-    no_plugin, const = versao_do_plugin(nome_mod, p)
+    no_plugin, const, _arquivo = versao_do_plugin(nome_mod, p)
     no_readme = versao_do_readme(p)
     if no_plugin is None:
-        raise Falha("PKG-2: nao achei a versao em %s/Plugin.cs (esperava o literal no "
+        raise Falha("PKG-2: nao achei a versao em %s (esperava o literal no "
                     "[BepInPlugin(\"guid\", \"nome\", \"x.y.z\")] ou uma const Version)"
-                    % nome_mod)
+                    % ", ".join(rel(c) for c in p["versao_em"]))
     if no_readme is None:
         raise Falha("PKG-3: nao achei a versao em %s/README.md (esperava a linha "
                     "\"- **Version:** x.y.z\", a que os READMEs ja usam)" % nome_mod)
@@ -562,10 +704,10 @@ def sincronizar_versao(nome_mod):
                             % (achado.group(2), fonte))
 
     # --- Plugin.cs: troca o literal da versao (atributo ou const) --------------
-    if os.path.isfile(p["plugin"]):
-        versao_plugin, const = versao_do_plugin(nome_mod, p)
+    versao_plugin, const, arquivo_plugin = versao_do_plugin(nome_mod, p)
+    if arquivo_plugin and os.path.isfile(arquivo_plugin):
         if versao_plugin is not None and versao_plugin != fonte:
-            with open(p["plugin"], encoding="utf-8", newline="") as fh:
+            with open(arquivo_plugin, encoding="utf-8", newline="") as fh:
                 texto = fh.read()
             if const:
                 padrao = re.compile(r'(const\s+string\s+%s\s*=\s*")([^"]*)(")'
@@ -574,10 +716,11 @@ def sincronizar_versao(nome_mod):
                 padrao = re.compile(r'(Plugin\(\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*")([^"]*)(")')
             novo = padrao.sub(lambda m: m.group(1) + fonte + m.group(3), texto, count=1)
             if novo != texto:
-                with open(p["plugin"], "w", encoding="utf-8", newline="") as fh:
+                with open(arquivo_plugin, "w", encoding="utf-8", newline="") as fh:
                     fh.write(novo)
-                mudancas.append("Plugin.cs: %s %s -> %s"
-                                % ("const %s" % const if const else "[BepInPlugin]",
+                mudancas.append("%s: %s %s -> %s"
+                                % (rel(arquivo_plugin),
+                                   "const %s" % const if const else "[BepInPlugin]",
                                    versao_plugin, fonte))
 
     # --- README.md: troca SO o valor da linha `- **Version:**`, nada mais ---------
@@ -597,19 +740,21 @@ def sincronizar_versao(nome_mod):
 
 
 def verificar(nome_mod, config=CONFIG_PADRAO, gerar_icone_se_faltar=False):
-    """Pre-flight de UM mod. Devolve (manifesto, dict de caminhos). Levanta Falha."""
+    """Pre-flight de UM pacote. Devolve (manifesto, dict de caminhos). Levanta Falha."""
     p = caminhos(nome_mod, config)
 
     if not os.path.isfile(p["csproj"]):
-        raise Falha("nao e mod: falta %s.csproj" % nome_mod)
+        raise Falha("nao e pacote: falta %s" % rel(p["csproj"]))
 
-    if not os.path.isfile(p["dll"]):
+    # PKG-API-1: um pacote nao-raiz tem TRES DLLs; TODAS tem de existir (faltando uma,
+    # o BepInEx nao resolve o plugin ao carregar - pacote incompleto e' pior que nenhum).
+    faltando = [d for d in p["dlls"] if not os.path.isfile(d)]
+    if faltando:
         raise Falha("DLL NAO BUILDADA: %s\n"
-                    "      -> rode:  dotnet build %s/%s.csproj -c %s "
-                    "-p:DeployToBepInEx=false"
-                    % (os.path.relpath(p["dll"], RAIZ), nome_mod, nome_mod, config))
+                    "      -> rode:  dotnet build %s -c %s -p:DeployToBepInEx=false"
+                    % (", ".join(rel(d) for d in faltando), rel(p["csproj"]), config))
 
-    # REL-1: existir nao basta - a DLL tem de corresponder a fonte de AGORA.
+    # REL-1: existir nao basta - cada DLL tem de corresponder a fonte de AGORA.
     artefato_esta_atual(nome_mod, p, config)
 
     manifesto = ler_manifest(nome_mod, p)
@@ -621,6 +766,14 @@ def verificar(nome_mod, config=CONFIG_PADRAO, gerar_icone_se_faltar=False):
         if not os.path.isfile(p[chave]):
             raise Falha("%s nao existe" % os.path.basename(p[chave]))
 
+    # PKG-API-1: os arquivos a mais que o pacote leva na raiz do zip (hoje so' o
+    # LICENSE do RealmApi). Sao obrigatorios: o pacote promete por contrato o que
+    # `--listar-caminhos` declara em `dentro_do_zip`.
+    for extra in p["extras"]:
+        if not os.path.isfile(extra):
+            raise Falha("%s nao existe (arquivo extra do pacote: %s)"
+                        % (os.path.basename(extra), rel(extra)))
+
     if not os.path.isfile(p["icon"]) and gerar_icone_se_faltar:
         gerar_icone(nome_mod, p["icon"])
     if not os.path.isfile(p["icon"]):
@@ -639,21 +792,29 @@ def verificar(nome_mod, config=CONFIG_PADRAO, gerar_icone_se_faltar=False):
 # ---------------------------------------------------------------------------
 
 def empacotar(nome_mod, manifesto, p):
-    """Monta o stage e zipa. Devolve (caminho do zip, lista de (nome_no_zip, bytes))."""
+    """Monta o stage e zipa. Devolve (caminho do zip, lista de (nome_no_zip, bytes)).
+
+    O formato e' o mesmo para os nove pacotes: metadados na RAIZ do zip e as DLLs em
+    `plugins/<pasta>/`. O que o pacote nao-raiz acrescenta e' (a) mais de uma DLL na
+    mesma pasta `plugins/` e (b) os arquivos de `extras` na raiz (o LICENSE do RealmApi).
+    """
     pasta_pacote = "%s-%s" % (AUTOR, nome_mod)
     stage = os.path.join(STAGE_RAIZ, pasta_pacote)
     if os.path.isdir(stage):
         shutil.rmtree(stage)
-    os.makedirs(os.path.join(stage, "plugins", nome_mod))
+    os.makedirs(os.path.join(stage, "plugins", p["pasta_no_zip"]))
 
     copiados = [("manifest.json", p["manifest"]),
                 ("README.md", p["readme"]),
                 ("CHANGELOG.md", p["changelog"]),
                 ("icon.png", p["icon"])]
+    for extra in p["extras"]:
+        copiados.append((os.path.basename(extra), extra))
     for destino, origem in copiados:
         shutil.copy2(origem, os.path.join(stage, destino))
-    shutil.copy2(p["dll"],
-                 os.path.join(stage, "plugins", nome_mod, nome_mod + ".dll"))
+    for dll in p["dlls"]:
+        shutil.copy2(dll, os.path.join(stage, "plugins", p["pasta_no_zip"],
+                                       os.path.basename(dll)))
 
     versao = manifesto["version_number"]
     zip_path = os.path.join(DIST, "%s-%s.zip" % (pasta_pacote, versao))
@@ -675,6 +836,33 @@ def empacotar(nome_mod, manifesto, p):
     return zip_path, conteudo
 
 
+def mapa_de_caminhos(config=CONFIG_PADRAO):
+    """O layout de CADA pacote, em JSON - fonte unica para os gates.
+
+    O `publish.yml` (pre-flight e registro) precisa saber onde esta o `.csproj` e o
+    `manifest.json` de cada alvo e o que tem de existir dentro do zip. Antes ele
+    reescrevia `<Mod>/<Mod>.csproj` na mao - premissa de layout padrao que o pacote
+    nao-raiz viola (PKG-API-1). Aqui ele le a resposta do mesmo detector que empacota:
+    uma fonte so, nada de segunda lista que envelhece.
+    """
+    mapa = []
+    for nome in descobrir_mods():
+        p = caminhos(nome, config)
+        dentro = ["manifest.json", "README.md", "CHANGELOG.md", "icon.png"]
+        dentro += [os.path.basename(extra) for extra in p["extras"]]
+        dentro += ["plugins/%s/%s" % (p["pasta_no_zip"], os.path.basename(dll))
+                   for dll in p["dlls"]]
+        mapa.append({
+            "nome": nome,
+            "nao_raiz": eh_pacote_nao_raiz(nome),
+            "csproj": rel(p["csproj"]),
+            "manifest": rel(p["manifest"]),
+            "dlls": [rel(dll) for dll in p["dlls"]],
+            "dentro_do_zip": dentro,
+        })
+    return mapa
+
+
 # ---------------------------------------------------------------------------
 # CLI
 # ---------------------------------------------------------------------------
@@ -690,6 +878,11 @@ def main(argv):
                     help="cria um icon.png 256x256 nos mods que estiverem sem")
     ap.add_argument("--listar", action="store_true",
                     help="so lista os mods encontrados e sai")
+    ap.add_argument("--listar-caminhos", action="store_true",
+                    help="imprime, em JSON, o layout de cada pacote (csproj, manifest, "
+                         "DLLs e o que tem de existir DENTRO do zip) - e' o que os "
+                         "gates (publish.yml) consomem em vez de reescrever o caminho "
+                         "do csproj na mao; respeita --config")
     ap.add_argument("--listar-nomes", action="store_true",
                     help="imprime SO os nomes dos mods (um por linha) - para consumir de "
                          "script (scripts/package.ps1); a descoberta de mod fica NUM lugar")
@@ -716,15 +909,32 @@ def main(argv):
             print(m)
         return 0
 
+    if args.listar_caminhos:
+        print(json.dumps(mapa_de_caminhos(args.config), ensure_ascii=False, indent=2))
+        return 0
+
     if args.listar:
         print("Mods encontrados em %s:" % RAIZ)
         for m in todos:
+            if eh_pacote_nao_raiz(m):
+                continue
             print("  - %-18s (csproj com DeployToBepInEx)" % m)
+        nao_raiz = [m for m in todos if eh_pacote_nao_raiz(m)]
         ignorados = projetos_ignorados()
         if ignorados:
             print("Ignorados (tem csproj mas nao sao mod - nao copiam para plugins/):")
             for m in ignorados:
                 print("  - %s" % m)
+        # PKG-API-1: os pacotes do layout nao-raiz saem DEPOIS dos dois blocos de sempre
+        # para que a saida dos oito de raiz continue byte a byte igual (o diff da
+        # entrega fica so' no que e' novo).
+        if nao_raiz:
+            print("Pacotes NAO-RAIZ (PKG-API-1: projeto aninhado, mais de uma DLL - "
+                  "tabela PACOTES_NAO_RAIZ), nao listados acima:")
+            for m in nao_raiz:
+                p = caminhos(m)
+                print("  - %-18s %s  (%d DLL(s) -> plugins/%s/)"
+                      % (m, rel(p["csproj"]), len(p["dlls"]), p["pasta_no_zip"]))
         return 0
 
     alvos = args.mods or todos
```

## Anexo B - diff de `.github/workflows/publish.yml`

```diff
diff --git a/.github/workflows/publish.yml b/.github/workflows/publish.yml
index 4a246db..06b8101 100644
--- a/.github/workflows/publish.yml
+++ b/.github/workflows/publish.yml
@@ -169,9 +169,24 @@ jobs:
           if not mods:
               erro('release/mods.json esta sem a lista "mods".')
 
-          # A lista do JSON tem que ser a MESMA que o empacotador descobre - senao existem
-          # duas listas de mods e uma vai envelhecer. A descoberta de mod fica em UM lugar:
-          # o `eh_mod` do tools/pack-thunderstore.py.
+          # A descoberta de mod fica em UM lugar: o `eh_mod` do tools/pack-thunderstore.py.
+          # A comparacao com o release/mods.json tem DUAS direcoes, e elas valem coisas
+          # diferentes (PKG-API-1):
+          #
+          #   * nome NO LEDGER que o empacotador NAO conhece -> ERRO. E' sempre defeito:
+          #     o ledger so decide sobre mod que existe, e um rename/typo deixaria o alvo
+          #     apontando para o nada.
+          #   * nome que o empacotador conhece e o ledger AINDA NAO decidiu -> AVISO. Nao
+          #     e' defeito, e' a ordem natural das coisas: a pasta do mod nasce com o
+          #     codigo e a decisao de publicar vem depois (o RealmApi entrou no
+          #     empacotador em PKG-API-1 e ganha entrada no ledger em PUB-API-2). Mod sem
+          #     entrada NUNCA e' enviado - os alvos saem do ledger -, e o aviso fica no
+          #     resumo do run para o caso nao passar em silencio.
+          #
+          # A igualdade das listas continua sendo o estado esperado (e e' o que acontece
+          # quando os dois lados estao completos). O que nao pode e' uma pasta nova deixar
+          # o pipeline INTEIRO vermelho: com a comparacao literal (`nomes_pack !=
+          # nomes_json`) TODOS os alvos eram reprovados, inclusive os seis liberados.
           p = subprocess.run([sys.executable, 'tools/pack-thunderstore.py', '--listar-nomes'],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
           saida = p.stdout.decode('utf-8', 'replace')
@@ -179,10 +194,18 @@ jobs:
               erro('tools/pack-thunderstore.py --listar-nomes saiu %d: %s' % (p.returncode, saida.strip()))
           nomes_pack = [l.strip() for l in saida.splitlines() if l.strip()]
           nomes_json = [m.get('nome') for m in mods]
-          if nomes_pack != nomes_json:
-              erro('release/mods.json e o empacotador divergem - a lista de mods tem uma fonte so '
-                   '(`tools/pack-thunderstore.py --listar-nomes`). JSON=%s | empacotador=%s'
-                   % (nomes_json, nomes_pack))
+          fantasmas = [n for n in nomes_json if n not in nomes_pack]
+          if fantasmas:
+              erro('release/mods.json lista mod(s) que o empacotador NAO conhece: %s. A lista de mods '
+                   'tem uma fonte so (`tools/pack-thunderstore.py --listar-nomes`) e um nome que ela nao '
+                   'devolve e um alvo que nao existe. JSON=%s | empacotador=%s'
+                   % (', '.join(fantasmas), nomes_json, nomes_pack))
+          sem_ledger = [n for n in nomes_pack if n not in nomes_json]
+          if sem_ledger:
+              print('::warning::o empacotador conhece mod(s) sem entrada em release/mods.json: %s. '
+                    'Sem entrada nao ha decisao de publicacao e o mod NAO e enviado (os alvos saem do '
+                    'ledger). Se ele ja pode ser publicado, cadastre a entrada com publicar:true.'
+                    % ', '.join(sem_ledger))
 
           liberados = [m['nome'] for m in mods if m.get('publicar') is True]
 
@@ -218,6 +241,12 @@ jobs:
               linhas.append('| %s | %s | %s | %s |' % (
                   m.get('nome'), 'sim' if m.get('publicar') else 'NAO',
                   m.get('versao_publicada') or '-', m.get('motivo') or ''))
+          # PKG-API-1: mod que o empacotador conhece e o ledger ainda nao decidiu aparece
+          # na tabela como "sem entrada" - TRAVADO de fato, porque sem entrada ele nunca
+          # entra na lista de alvos.
+          for n in sem_ledger:
+              linhas.append('| %s | sem entrada | - | sem decisao em release/mods.json: '
+                            'nunca e enviado |' % n)
           # PKG-5: a ORDEM de envio mora em `ordem_de_envio` deste arquivo (o gate le este
           # arquivo, entao a ordem viaja junto da liberacao). A dependencia publica ANTES do
           # dependente - a Thunderstore recusa no upload a referencia a versao inedita.
@@ -329,7 +358,7 @@ jobs:
           ESCOLHA: ${{ inputs.mod }}
         run: |
           python - <<'PY'
-          import json, os, re, sys, time, urllib.error, urllib.request, zipfile
+          import json, os, re, subprocess, sys, time, urllib.error, urllib.request, zipfile
 
           AUTOR = 'gumatos'          # prefixo dos zips do tools/pack-thunderstore.py (AUTOR)
           API = 'https://thunderstore.io/c/%s/api/v1/package/'   # lista publica da comunidade
@@ -419,6 +448,19 @@ jobs:
 
           enviar, pulados, versoes_alvo = [], [], {}
           linhas_env = []
+
+          # PKG-API-1: onde esta cada arquivo de cada alvo sai do EMPACOTADOR, nao de um
+          # `<Mod>/<Mod>.csproj` escrito aqui. O layout padrao (pasta na raiz, uma DLL) e'
+          # o caso comum, nao a regra: o RealmApi vive em `api/Plugin/RealmApi.csproj` e
+          # produz tres DLLs. `--listar-caminhos` responde as duas coisas (caminhos e o que
+          # tem de existir dentro do zip) pela mesma fonte que empacota.
+          _p = subprocess.run([sys.executable, 'tools/pack-thunderstore.py', '--listar-caminhos'],
+                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
+          if _p.returncode != 0:
+              erro('tools/pack-thunderstore.py --listar-caminhos saiu %d: %s'
+                   % (_p.returncode, _p.stdout.decode('utf-8', 'replace').strip()))
+          CAMINHOS = {c['nome']: c for c in json.loads(_p.stdout.decode('utf-8'))}
+
           for nome in alvos:
               entradas = [m for m in dados['mods'] if m.get('nome') == nome]
               if not entradas:
@@ -426,11 +468,17 @@ jobs:
                        'entao isto e um defeito do pipeline - nada e enviado.' % nome)
               entrada = entradas[0]
 
+              alvo = CAMINHOS.get(nome)
+              if not alvo:
+                  erro('%s nao esta na descoberta do empacotador (tools/pack-thunderstore.py '
+                       '--listar-caminhos): nao ha como saber o .csproj, o manifesto nem o que '
+                       'tem de existir dentro do zip. Nada e enviado.' % nome)
+
               # --- 4.2 a versao vem do <Version> do .csproj (fonte unica, PKG-2) -----
-              with open('%s/%s.csproj' % (nome, nome), encoding='utf-8', errors='replace') as fh:
+              with open(alvo['csproj'], encoding='utf-8', errors='replace') as fh:
                   achado = re.search(r'<Version>([^<]+)</Version>', fh.read())
               if not achado:
-                  erro('PKG-2: %s/%s.csproj sem <Version> (e o <Version> que manda).' % (nome, nome))
+                  erro('PKG-2: %s sem <Version> (e o <Version> que manda).' % alvo['csproj'])
               versao = achado.group(1).strip()
               versoes_alvo[nome] = versao
 
@@ -441,18 +489,20 @@ jobs:
                        '      Este workflow NAO COMPILA - os .csproj precisam das assemblies do JOGO\n'
                        '      (Assembly-CSharp.dll, UnityEngine, Sirenix) que ficam em lib/ (gitignored).\n'
                        '      Rode na maquina de desenvolvimento, da raiz do repo:\n'
-                       '        dotnet build %s/%s.csproj -c Release -p:DeployToBepInEx=false\n'
+                       '        dotnet build %s -c Release -p:DeployToBepInEx=false\n'
                        '        python tools/pack-thunderstore.py %s\n'
                        '      e traga os zips do dist/ para o runner: anexe-os numa GitHub Release e\n'
                        '      dispare este workflow com o input release_tag apontando para ela.'
-                       % (zip_rel, nome, nome, nome))
+                       % (zip_rel, alvo['csproj'], nome))
 
               with zipfile.ZipFile(zip_rel) as zf:
                   conteudo = zf.namelist()
                   manifesto = json.loads(zf.read('manifest.json').decode('utf-8'))
 
-              obrigatorios = ['manifest.json', 'README.md', 'CHANGELOG.md', 'icon.png',
-                              'plugins/%s/%s.dll' % (nome, nome)]
+              # O que TEM de existir dentro do zip vem do empacotador (`dentro_do_zip`):
+              # os quatro metadados de sempre + o LICENSE do RealmApi + as DLLs na pasta
+              # `plugins/<Pacote>/` - que no pacote nao-raiz sao TRES.
+              obrigatorios = list(alvo['dentro_do_zip'])
               faltando = [f for f in obrigatorios if f not in conteudo]
               if faltando:
                   erro('PACOTE INCOMPLETO (%s): falta %s. Pacote incompleto e pior que pacote '
@@ -463,7 +513,7 @@ jobs:
               if manifesto.get('version_number') != versao:
                   erro('O ZIP ESTA VELHO: manifest.version_number=%s e o <Version> do .csproj e %s. '
                        'Rebuilde e reempacote antes de publicar.' % (manifesto.get('version_number'), versao))
-              with open('%s/manifest.json' % nome, encoding='utf-8') as fh:
+              with open(alvo['manifest'], encoding='utf-8') as fh:
                   manifesto_repo = json.load(fh)
               for campo in ('name', 'version_number', 'description', 'dependencies'):
                   if manifesto_repo.get(campo) != manifesto.get(campo):
@@ -925,7 +975,7 @@ jobs:
           TEAM: ${{ needs.libera.outputs.team }}
         run: |
           python - <<'PY'
-          import json, os, re, sys, urllib.error, urllib.request
+          import json, os, re, subprocess, sys, urllib.error, urllib.request
 
           def erro(msg):
               print('::error::' + msg)
@@ -962,8 +1012,24 @@ jobs:
           publicados = {p.get('full_name'): (p.get('versions') or []) for p in pacotes}
 
           mudou, faltou = [], []
+
+          # PKG-API-1: o caminho do .csproj vem do empacotador (mesma fonte do pre-flight),
+          # nao de um `<Mod>/<Mod>.csproj` escrito aqui - o RealmApi vive em
+          # `api/Plugin/RealmApi.csproj`.
+          _p = subprocess.run([sys.executable, 'tools/pack-thunderstore.py', '--listar-caminhos'],
+                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
+          if _p.returncode != 0:
+              erro('tools/pack-thunderstore.py --listar-caminhos saiu %d: %s'
+                   % (_p.returncode, _p.stdout.decode('utf-8', 'replace').strip()))
+          CAMINHOS = {c['nome']: c for c in json.loads(_p.stdout.decode('utf-8'))}
+
           for nome in alvos:
-              with open('%s/%s.csproj' % (nome, nome), encoding='utf-8', errors='replace') as fh:
+              alvo = CAMINHOS.get(nome)
+              if not alvo:
+                  erro('%s nao esta na descoberta do empacotador (tools/pack-thunderstore.py '
+                       '--listar-caminhos) - sem o .csproj nao ha versao a conferir. Registro '
+                       'nao e inventado: nada foi gravado para este alvo.' % nome)
+              with open(alvo['csproj'], encoding='utf-8', errors='replace') as fh:
                   versao = re.search(r'<Version>([^<]+)</Version>', fh.read()).group(1).strip()
               st_viva, detalhe = busca(API_VERSAO % (team, nome, versao))
               viva = detalhe if (st_viva == 200 and isinstance(detalhe, dict)) else None
```

## Anexo C - diff de `tools/publish-thunderstore.sh`

```diff
diff --git a/tools/publish-thunderstore.sh b/tools/publish-thunderstore.sh
index 276b96f..5cb0f9c 100644
--- a/tools/publish-thunderstore.sh
+++ b/tools/publish-thunderstore.sh
@@ -8,6 +8,19 @@
 #
 # O token vem de, nesta ordem: variavel TCLI_AUTH_TOKEN, arquivo apontado por
 # THUNDERSTORE_TOKEN_FILE, ou ~/.thunderstore-token. Nunca do repositorio.
+#
+# QUEM PODE SUBIR: `release/mods.json` (PKG-API-1)
+# ------------------------------------------------
+# O pipeline (.github/workflows/publish.yml) SEMPRE leu esse ledger; este publicador
+# local NAO lia - ele subia o que estivesse em `dist/`, inclusive versao antiga e mod
+# TRAVADO (publicar:false). Agora o passo 0 le o MESMO ledger e o MESMO empacotador
+# (`tools/pack-thunderstore.py`), imprime o estado de cada pacote e SO os `publicar:true`
+# entram no plano de envio. TRAVADO e "sem entrada no ledger" aparecem como TRAVADO e
+# nao sao empacotados nem enviados.
+#
+# O token so e' EXIGIDO quando ha envio (`--go`). No dry-run ele continua sendo validado
+# se estiver disponivel, mas a ausencia dele nao aborta mais um run que nao envia nada -
+# era o que impedia de ver o plano de envio numa maquina sem credencial.
 set -u
 cd "$(dirname "$0")/.." || exit 1
 RAIZ="$(pwd)"
@@ -22,20 +35,125 @@ for a in "$@"; do
   esac
 done
 
+mkdir -p dist
+PLANO="dist/.plano-publicacao"
+
+# --- 0) LEDGER: quem esta liberado ------------------------------------------
+# Le `release/mods.json` (a decisao humana) e `--listar-caminhos` do empacotador (a
+# descoberta de pacote) - as duas fontes que o pipeline usa. Escreve o plano de envio em
+# $PLANO, no formato `nome|zip|versao`, e imprime a tabela de estado. A versao sai do
+# `<Version>` do .csproj, a mesma fonte unica do PKG-2.
+echo "== ledger (release/mods.json + tools/pack-thunderstore.py) =="
+python - "$SO" "$PLANO" <<'PY' || exit 1
+import json, re, subprocess, sys
+
+escolha = (sys.argv[1] or '').strip()
+plano_path = sys.argv[2]
+
+def morre(msg):
+    print('!! ' + msg)
+    sys.exit(1)
+
+with open('release/mods.json', encoding='utf-8') as fh:
+    dados = json.load(fh)
+mods = dados.get('mods') or []
+nomes_json = [m.get('nome') for m in mods]
+
+p = subprocess.run([sys.executable, 'tools/pack-thunderstore.py', '--listar-caminhos'],
+                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
+if p.returncode != 0:
+    morre('tools/pack-thunderstore.py --listar-caminhos saiu %d: %s'
+          % (p.returncode, p.stdout.decode('utf-8', 'replace').strip()))
+caminhos = {c['nome']: c for c in json.loads(p.stdout.decode('utf-8'))}
+
+fantasmas = [n for n in nomes_json if n not in caminhos]
+if fantasmas:
+    morre('release/mods.json lista mod(s) que o empacotador NAO conhece: %s. A lista de mods '
+          'tem uma fonte so (tools/pack-thunderstore.py --listar-nomes).'
+          % ', '.join(fantasmas))
+
+def versao(csproj):
+    with open(csproj, encoding='utf-8', errors='replace') as fh:
+        achado = re.search(r'<Version>([^<]+)</Version>', fh.read())
+    return achado.group(1).strip() if achado else None
+
+print('  %-34s %-9s %s' % ('pacote', 'estado', 'detalhe'))
+liberados, travados, sem_ledger = [], [], []
+for m in mods:
+    nome = m.get('nome')
+    if m.get('publicar') is True:
+        liberados.append(nome)
+        print('  %-34s %-9s %s' % (nome, 'LIBERADO', 'publicar:true'))
+    else:
+        travados.append(nome)
+        motivo = (m.get('motivo') or 'sem motivo registrado').replace('\n', ' ')
+        print('  %-34s %-9s %s' % (nome, 'TRAVADO', motivo))
+for nome in sorted(caminhos):
+    if nome not in nomes_json:
+        sem_ledger.append(nome)
+        print('  %-34s %-9s %s' % (nome, 'TRAVADO',
+                                   'sem entrada em release/mods.json - nunca e enviado'))
+print()
+print('  liberados: %d | travados no ledger: %d | sem entrada no ledger: %d'
+      % (len(liberados), len(travados), len(sem_ledger)))
+
+plano = []
+for nome in liberados:
+    v = versao(caminhos[nome]['csproj'])
+    if not v:
+        morre('PKG-2: %s sem <Version> no .csproj - nao da para saber qual pacote subiria.'
+              % caminhos[nome]['csproj'])
+    plano.append('%s|dist/gumatos-%s-%s.zip|%s' % (nome, nome, v, v))
+with open(plano_path, 'w', encoding='utf-8') as fh:
+    fh.write('\n'.join(plano) + ('\n' if plano else ''))
+
+if not liberados:
+    print('  Nada a fazer: nenhum mod com publicar:true em release/mods.json.')
+    sys.exit(0)
+if escolha and escolha not in liberados:
+    if escolha in travados or escolha in sem_ledger:
+        morre('%s esta TRAVADO em release/mods.json e nao sera publicado. Motivo: %s'
+              % (escolha, next((m.get('motivo') for m in mods if m.get('nome') == escolha),
+                               'sem entrada em release/mods.json')))
+    morre('%s nao existe em release/mods.json (opcoes: %s)'
+          % (escolha, ', '.join(nomes_json)))
+print('  pedido   : %s' % (escolha or 'todos os liberados'))
+print('  vao subir: %s' % ', '.join(p.split('|')[0] for p in plano))
+PY
+
+NOMES_LIBERADOS=()
+if [ -s "$PLANO" ]; then
+  while IFS='|' read -r nome _zip _versao; do
+    [ -n "$nome" ] || continue
+    NOMES_LIBERADOS+=("$nome")
+  done < "$PLANO"
+fi
+if [ "${#NOMES_LIBERADOS[@]}" = "0" ]; then
+  echo "== nada liberado para publicar (publicar:true) - encerrando. =="
+  exit 0
+fi
+
 # --- 1) de onde vem o token -------------------------------------------------
 TOKEN="${TCLI_AUTH_TOKEN:-}"
+ARQ="${THUNDERSTORE_TOKEN_FILE:-$HOME/.thunderstore-token}"
 if [ -z "$TOKEN" ]; then
-  ARQ="${THUNDERSTORE_TOKEN_FILE:-$HOME/.thunderstore-token}"
   case "$ARQ" in
     "$RAIZ"/*) echo "!! o arquivo de token esta DENTRO do repositorio: $ARQ"; echo "   mova para fora antes de continuar."; exit 1 ;;
   esac
-  [ -f "$ARQ" ] || { echo "!! token nao encontrado. Defina TCLI_AUTH_TOKEN ou crie ~/.thunderstore-token"; exit 1; }
-  TOKEN="$(cat "$ARQ")"
+  if [ -f "$ARQ" ]; then TOKEN="$(cat "$ARQ")"; fi
+fi
+if [ -n "$TOKEN" ]; then
+  case "$TOKEN" in
+    tss_*) ;;
+    *) echo "!! isso nao parece um token do Thunderstore (completa com 'tss_')"; exit 1 ;;
+  esac
+elif [ "$GO" = "1" ]; then
+  echo "!! token nao encontrado. Defina TCLI_AUTH_TOKEN ou crie $ARQ"; exit 1
+else
+  echo
+  echo "aviso: sem token no ambiente. DRY-RUN NAO ENVIA NADA, entao o plano acima vale"
+  echo "       igual - o token e' exigido so no envio de verdade (--go)."
 fi
-case "$TOKEN" in
-  tss_*) ;;
-  *) echo "!! isso nao parece um token do Thunderstore (comeca com 'tss_')"; exit 1 ;;
-esac
 
 # --- 2) trava de segredo: nada de credencial no que vai a publico -----------
 echo "== trava de segredo =="
@@ -50,23 +168,27 @@ fi
 
 # --- 4) empacotar -----------------------------------------------------------
 echo
-echo "== empacotando =="
+echo "== empacotando (so os LIBERADOS: quem manda e' o ledger) =="
 rm -rf dist/tmp-pub && mkdir -p dist/tmp-pub
-if [ -n "$SO" ]; then python tools/pack-thunderstore.py "$SO"; else python tools/pack-thunderstore.py; fi || exit 1
+if [ -n "$SO" ]; then
+  python tools/pack-thunderstore.py "$SO"
+else
+  python tools/pack-thunderstore.py "${NOMES_LIBERADOS[@]}"
+fi || exit 1
 
 # --- 5) subir ---------------------------------------------------------------
 echo
 echo "== envio =="
 FALHOU=0
-for z in dist/gumatos-*.zip; do
-  [ -f "$z" ] || continue
-  nome="$(basename "$z")"
+while IFS='|' read -r nome z versao; do
+  [ -n "$nome" ] || continue
+  [ -f "$z" ] || { echo "   [FALTA] $nome: $z nao existe (nao empacotou neste run)"; FALHOU=1; continue; }
   if [ "$GO" != "1" ]; then
-    echo "   [DRY-RUN] subiria: $nome ($(stat -c %s "$z") bytes) -> $API"
+    echo "   [DRY-RUN] subiria: $(basename "$z") ($(stat -c %s "$z") bytes) -> $API"
     continue
   fi
-  printf '   subindo %-46s ' "$nome"
-  RESP="$(curl -s -w '\n%{http_code}' --max-time 300 -H "Authorization: Bearer $TOKEN" -F "file=@$z" "$API")"
+  printf '   subindo %-46s ' "$(basename "$z")"
+  RESP="$(curl -s -w '\n%{http_code}' --max-time 300 -H "Authorization: Bearer ***" -F "file=@$z" "$API")"
   CODE="$(printf '%s' "$RESP" | tail -1)"
   CORPO="$(printf '%s' "$RESP" | sed '$d')"
   if [ "$CODE" = "200" ]; then
@@ -78,9 +200,10 @@ for z in dist/gumatos-*.zip; do
     echo
     FALHOU=1
   fi
-done
+done < "$PLANO"
 
 rmdir dist/tmp-pub 2>/dev/null
+rm -f "$PLANO"
 echo
 if [ "$GO" != "1" ]; then
   echo "== DRY-RUN terminou. Nada foi publicado. Use --go para publicar de verdade. =="
```

## Anexo D - diff dos checks (`check_versoes.py`, `valida_pacotes.py`)

```diff
diff --git a/tools/check_versoes.py b/tools/check_versoes.py
index d00fdb2..225b13c 100644
--- a/tools/check_versoes.py
+++ b/tools/check_versoes.py
@@ -84,7 +84,7 @@ def main():
         p = pt.caminhos(nome)
         fonte = pt.versao_do_csproj(p)
         no_manifest = versao_do_manifest(p["manifest"])
-        no_plugin, const = pt.versao_do_plugin(nome, p)
+        no_plugin, const, arquivo = pt.versao_do_plugin(nome, p)
         no_readme = pt.versao_do_readme(p)
 
         # marca DIVERGE so ao lado do valor que nao bate com a fonte
@@ -97,7 +97,12 @@ def main():
         print("  %-46s %s%s"
               % ("manifest.json  version_number", no_manifest or "(ausente)",
                  marca(no_manifest) + marca_falta(no_manifest)))
-        rotulo = ("Plugin.cs  const %s =" % const) if const else "Plugin.cs  [BepInPlugin(...)]"
+        # O rotulo nomeia o ARQUIVO onde a versao do plugin foi achada: no layout padrao
+        # e' `Plugin.cs`; no pacote nao-raiz (PKG-API-1) o [BepInPlugin] esta em
+        # `RealmApiPlugin.cs` e a const que ele cita, em `Contracts.cs` - dois arquivos,
+        # e o rotulo fixo "Plugin.cs" apontaria para o lugar errado.
+        base = os.path.basename(arquivo) if arquivo else "Plugin.cs"
+        rotulo = ("%s  const %s =" % (base, const)) if const else "%s  [BepInPlugin(...)]" % base
         print("  %-46s %s%s"
               % (rotulo, no_plugin or "(ausente)",
                  marca(no_plugin) + marca_falta(no_plugin)))

diff --git a/.github/scripts/valida_pacotes.py b/.github/scripts/valida_pacotes.py
index 0eb9b11..4dda883 100644
--- a/.github/scripts/valida_pacotes.py
+++ b/.github/scripts/valida_pacotes.py
@@ -19,7 +19,10 @@ REGRAS (as mesmas que o Thunderstore exige e o pack ja checava)
 ---------------------------------------------------------------
   1. manifest.json existe e e JSON valido, com os campos obrigatorios;
   2. `name` alfanumerico ([A-Za-z0-9_]+) e IGUAL ao nome da pasta do mod
-     (se divergirem, o r2modman instala num caminho diferente do que o README promete);
+     (se divergirem, o r2modman instala num caminho diferente do que o README promete).
+     PKG-API-1: no pacote de layout NAO-RAIZ - o RealmApi, cujos metadados ficam em `api/`,
+     um nivel acima do projeto `api/Plugin/` - o esperado nao e' o nome da pasta e sim o
+     nome do PACOTE, que vem da tabela do empacotador (`--listar-caminhos`);
   3. `version_number` em semver `X.Y.Z` (se ele e o MESMO do .csproj/Plugin.cs NAO e
      daqui: e do `tools/check_versoes.py`, passo 2 do workflow);
   4. `description` nao vazia e <= 250 caracteres (limite do Thunderstore);
@@ -52,6 +55,7 @@ import json
 import os
 import re
 import struct
+import subprocess
 import sys
 
 RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
@@ -69,6 +73,10 @@ ICONE_LADO = 256
 IGNORAR = {"docs", "dist", "lib", "scratch", "tools", ".git", ".github",
            "ReloadProbe", "__pycache__"}
 
+# Cache do mapa pasta-de-metadados -> nome do pacote (PKG-API-1), preenchido na primeira
+# chamada de `nome_do_pacote`. None = ainda nao perguntou ao empacotador.
+_MAPA = None
+
 
 def png_tamanho(caminho):
     """(largura, altura) lidos do IHDR. None se o arquivo nao for um PNG."""
@@ -99,6 +107,31 @@ def pastas_com_manifest():
     return com, sem
 
 
+def nome_do_pacote(pasta):
+    """Nome do PACOTE cujos metadados estao em `pasta` (PKG-API-1).
+
+    No layout padrao e' a propria pasta do mod. No layout nao-raiz nao e': os metadados do
+    RealmApi ficam em `api/`, um nivel acima do projeto (`api/Plugin/RealmApi.csproj`), e o
+    nome do pacote e' `RealmApi`. Quem sabe disso e' a tabela do empacotador, nao este
+    script - entao a resposta vem de `tools/pack-thunderstore.py --listar-caminhos`, a
+    MESMA fonte que empacota e que o `publish.yml` consulta. Sem o empacotador (ou se ele
+    falhar) cai no nome da pasta: e' o comportamento antigo, e o check nao morre por isso.
+    """
+    global _MAPA
+    if _MAPA is None:
+        _MAPA = {}
+        try:
+            saida = subprocess.run(
+                [sys.executable, os.path.join(RAIZ, "tools", "pack-thunderstore.py"),
+                 "--listar-caminhos"],
+                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=120).stdout
+            for pacote in json.loads(saida.decode("utf-8")):
+                _MAPA[os.path.dirname(pacote["manifest"])] = pacote["nome"]
+        except Exception:  # noqa: BLE001 - descoberta e' conveniencia, nao requisito
+            _MAPA = {}
+    return _MAPA.get(pasta, pasta)
+
+
 def versoes_do_repo():
     """({mod: versao}, team) - o que o repositorio declara hoje, para a regra 5.
 
@@ -190,9 +223,10 @@ def valida(nome):
         if not NOME_VALIDO.match(nome_manifesto):
             erros.append("'name' '%s' nao e alfanumerico (use so A-Z a-z 0-9 _)"
                          % nome_manifesto)
-        if nome_manifesto != nome:
-            erros.append("'name' '%s' != pasta do mod '%s' (o r2modman instalaria "
-                         "noutro caminho do que o README promete)" % (nome_manifesto, nome))
+        esperado = nome_do_pacote(nome)
+        if nome_manifesto != esperado:
+            erros.append("'name' '%s' != pacote '%s' (o r2modman instalaria "
+                         "noutro caminho do que o README promete)" % (nome_manifesto, esperado))
 
     # 3. semver
     versao = manifesto.get("version_number")
@@ -281,15 +315,19 @@ def main():
 
     problemas = 0
     for nome in com:
+        # PKG-API-1: no layout nao-raiz a pasta de metadados nao tem o nome do pacote
+        # (`api/` guarda o RealmApi) - o rotulo mostra os dois para nao confundir.
+        pacote = nome_do_pacote(nome)
+        rotulo = nome if pacote == nome else "%s (pacote %s)" % (nome, pacote)
         erros, dados = valida(nome)
         if erros:
             problemas += len(erros)
-            print("FALHA %-32s %s" % (nome, dados.get("versao") or ""))
+            print("FALHA %-32s %s" % (rotulo, dados.get("versao") or ""))
             for e in erros:
                 print("        - %s" % e)
         else:
             print("ok    %-32s %-8s desc=%-4s icone=%s"
-                  % (nome, dados.get("versao", "?"), dados.get("desc_len", "?"),
+                  % (rotulo, dados.get("versao", "?"), dados.get("desc_len", "?"),
                      dados.get("icone", "?")))
 
     # 8. resolucao de dependencias (PKG-5): toda dependencia tem de RESOLVER. A regra mora
```

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
