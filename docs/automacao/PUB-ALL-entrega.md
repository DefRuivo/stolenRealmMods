# PUB-ALL-1 — preparação das novas versões de todos os mods (bump + CHANGELOG + pacote)

**Cartão:** `t_d00f2bc6` (kanban) · **Data:** 2026-10-16 · **Alvo:** um único disparo do pipeline depois desta frente.
**Modo:** PREPARAR E EMPACOTAR. Nada foi publicado, nada foi instalado no perfil do dono, nada foi empurrado para o
remoto e `release/mods.json` **não** foi tocado (é da frente PUB-API-2). `publicar` continua como estava.

---

## 1. Tabela por mod

| Mod | Versão antiga → nova | DLL (`bin/Release/netstandard2.1/`) sha256 | ZIP em `dist/` | sha256 do ZIP | Pre-flight |
|---|---|---|---|---|---|
| **BetterCombatText** | 0.1.2 → **0.1.3** | `024831980fb99ba88c3e4c447010929d36152258444d658f754efd711b9409f7` | `dist/gumatos-BetterCombatText-0.1.3.zip` | `ef6f1bd8c393ddcac92c54961cbf19f7d51ab7f3d42a3dfbd7723c2d4e747208` | **ok** |
| **RoguelikeDebugger** | 0.1.2 → **0.1.3** | `43aa414e300de4cd525ca5a636ffb301a3cb6642dd646a4144f9d6f6d6ccff96` | `dist/gumatos-RoguelikeDebugger-0.1.3.zip` | `c615a868ed7a34f0364b6bdae8da39d39a1d0a275517a8b9db490ca3ee298a84` | **ok** |
| **RoguelikeSkillTreeVisualizer** | 0.3.3 → **0.3.4** | `cd1517f38fcfca957124d3e4d69d836906f43031f89d261e2319a5f8ec0fe346` | `dist/gumatos-RoguelikeSkillTreeVisualizer-0.3.4.zip` | `cc2f0a2e94137071609657bbaba3a05fec1ae0178352a4ff2348ad19458dd225` | pacote **ok**; trava de dependência **vermelha** (ver §3) |
| **RoguelikeUnlimitedLevelProgression** | 0.1.1 (sem bump — ver §2) | `bff477bd26a85df06f0f1ee7887da429e3053a7c91b7434eb7ab158fe287e4e3` | `dist/gumatos-RoguelikeUnlimitedLevelProgression-0.1.1.zip` | `ed42ec6de5ebcb07a0442aaf44f86881a53c4e61fe7b92e01b60bc35087af429` | **ok** |
| **RealmApi** | 0.1.0 (primeira publicação, sem bump) | `plugins/RealmApi/RealmApi.dll` `764b72d84a976a534292a518d14177b76fdede070bf9979e649efc5df25d19d7` · `RealmApi.Core.dll` `d4e72f24e4e7c503bdd32c200b4bfa7635a1529b09451e2a35b5400547d32fb2` · `RealmApi.Hooks.dll` `86d7fcf0012e1a611b42e96081609704a23a0129cc9918b3f1004c14a816778a` | `dist/gumatos-RealmApi-0.1.0.zip` | `de9352478f4411b5ad5e7ec4f001140ff65d13d7a5cfe5a157f624b9c2a570a9` | **ok** (pacote da frente PKG-API-1 — ver §2.4) |

Leitura da tabela: o de-para é `antiga -> nova`; o hash da DLL é o do artefato que entrou no ZIP (conferido lendo o
ZIP, `PUB-ALL-evidencias/zips.json`); "Pre-flight" = `python tools/pack-thunderstore.py --so-conferir`.

### 1.1 Os três (quatro) lugares da versão, por mod

Todos foram bumpados **nos quatro** lugares que carregam a versão, e o `tools/check_versoes.py` fecha verde
(`os 9 mods batem nos quatro lugares`):

| Mod | `.csproj <Version>` | `manifest.json version_number` | literal no código | `README.md - **Version:**` |
|---|---|---|---|---|
| BetterCombatText | 0.1.3 | 0.1.3 | `Plugin.Versao` = 0.1.3 | 0.1.3 |
| RoguelikeDebugger | 0.1.3 | 0.1.3 | `[BepInPlugin(..., "0.1.3")]` | 0.1.3 |
| RoguelikeSkillTreeVisualizer | 0.3.4 | 0.3.4 | `Plugin.Version` = 0.3.4 | 0.3.4 |

### 1.2 CHANGELOG por mod (o que mudou NESTA versão)

- **BetterCombatText 0.1.3** — a seção `## Unreleased` do CHG-REV virou `## 0.1.3 — 2026-10-16`: o `manifest.json`
  deixou de declarar `DefRuivo_StolenRealmMods-BetterFont-1.0.3` (DEP-REV: nenhum código do BCT referencia o
  BetterFont, só um comentário) e o README foi alinhado — a linha *Needs* dizia "BepInEx 5 **and BetterFont**" e a
  seção *Together with BetterFont* dizia "a dependência deste pacote aponta para aquela versão". Ambas passaram a
  dizer o que o manifest diz: só BepInEx, com o BetterFont como integração **opcional**. O código visual não mudou.
- **RoguelikeDebugger 0.1.3** — `## Unreleased` → `## 0.1.3 — 2026-10-16`. É a proveniência do dump
  (`DBG-PROV-V1`, commit `097f950`): cabeçalho de identidade do jogo/DLL antes dos patches, estado ABERTO/PARCIAL
  com os ganchos realmente aplicados, rodapé FECHADO em `Application.quitting`; RealmApi segue **opcional** (sondada
  por reflexão); a matriz Flame é classificada como leitura **ativa** (`Game.EvalVoid`), não observação passiva.
- **RoguelikeSkillTreeVisualizer 0.3.4** — `## Unreleased` → `## 0.3.4 — 2026-10-16`: a plumbing de UI passa a vir
  da família `UI` do RealmApi (`UIFactory.Clone` / `UIFactory.BindClick`, `UiFamily.Bind(..., allowMutation: true)`),
  com **dependência HARD** nova (`[BepInDependency] com.gumatos.realmapi >= 0.1.0`) e o manifest declarando
  `DefRuivo_StolenRealmMods-RealmApi-0.1.0`. A ordem de envio (API antes do RSTV) está escrita no próprio changelog.
- **RoguelikeUnlimitedLevelProgression 0.1.1** — sem bump (ver §2); a seção `0.1.1` foi ajustada para registrar que
  o pacote foi reconstruído da fonte atual (o texto dizia "alterações locais ainda sem commit").
- **BetterFont / BetterStats / BetterTooltips** — sem versão nova, portanto sem entrada nova (ver §2.1).

---

## 2. O que NÃO foi preparado, e por quê

### 2.1 BetterFont 1.0.3, BetterStats 1.0.2, BetterTooltips 0.1.4 — nenhuma versão nova

Critério do cartão: *"a DLL publicada é idêntica ao rebuild (REL-1) — só precisam de versão nova se o **texto
público** mudou"*. Medido hoje:

- **Código/DLL:** nada mudou depois do que está no ar. REL-1 (`t_8703b3a4`) e HYG-2 (`t_e24fefaf`) confirmaram por
  recompilação forçada e comparação de SHA-256 que as DLLs dos três são idênticas às publicadas; nada nos três foi
  editado desde então (`git status` limpo para `.cs`, `.csproj`, `manifest.json` e `README.md`).
- **Texto público (a página do pacote):** `README.md` e a `description` do manifest **não** mudaram → o que o usuário
  lê na Thunderstore continua igual.
- **O que mudou neles:** só o `CHANGELOG.md`, corrigido pela auditoria documental CHG-REV (`t_a115a139`) — que
  registra em cada arquivo *"These repository corrections do not modify previously published ZIPs"*. Publicar uma
  versão nova de cada um só para reemitir um changelog corrigido entrega a mesma DLL de novo (ruído no índice).

**Ponto de decisão explícito para o dono:** se ele quiser que o changelog corrigido chegue às páginas publicadas, a
mudança é trivial — bumpar o PATCH dos três e reempacotar (2 comandos por mod, sem tocar em código). Não foi feito
porque o critério do cartão é o texto público e a versão publicada é imutável; o custo é uma versão nova com DLL
byte-idêntica.

### 2.2 BetterPortuguese 0.1.0 — não preparado (bloqueio humano conhecido)

Gates de tradução abertos (`LANG-C1..C5`) e `publicar: false` em `release/mods.json`. O cartão manda não publicar
sem o dono resolver os gates; nada foi bumpado nem empacotado.

**Achado lateral que importa para o pipeline:** a trava global `bash tools/release-check.sh` **aborta no passo
2/TRV-1** por causa dele — `BetterPortuguese/Plugin.cs` não tem a linha literal `carregado` exigida pela regra 4
(o `LogInfo` da linha 61 diz o estado sem a palavra). O passo nunca chega ao build, então o ritual global fica
vermelho por um motivo que **não** é desta frente e que não foi consertado aqui: é código de um mod bloqueado, com
cartão próprio aberto (`BP-6`, `t_36c75af4`). Conserto mínimo, se o dono quiser destravar o ritual: uma linha
`LogInfo("BetterPortuguese <versao> carregado.")` no `Awake` (mesma convenção dos outros 8 mods).

### 2.3 Os itens fora do escopo desta frente

- `release/mods.json` — **não tocado** (é da PUB-API-2 / PUB-ALL-2).
- `tools/pack-thunderstore.py`, `.github/workflows/publish.yml`, `.github/scripts/valida_pacotes.py`,
  `tools/publish-thunderstore.sh` — **não tocados** (frente PKG-API-1, `t_d393f45a`, está com eles em mãos).
- Nada foi instalado em `<perfil>\BepInEx\plugins\` (todos os quatro builds foram
  `-c Release --no-incremental -p:DeployToBepInEx=false -p:DeployToScripts=false`).

### 2.4 RealmApi 0.1.0 — preparado pela frente irmã, não duplicado aqui

O RealmApi é primeira publicação e passa no pre-flight, com o ZIP já em `dist/gumatos-RealmApi-0.1.0.zip` (manifest
`name: RealmApi`, `version_number: 0.1.0`, 3 DLLs em `plugins/RealmApi/`, 8 arquivos, sha256 `de935247…`). A
preparação dele tem frente própria: **PKG-API-1** (`t_d393f45a`, ensina o packer/gate a empacotar o módulo aninhado
multi-DLL) e **PUB-API-1** (`t_daf5efde`, metadados/README/ícone) — este cartão **não** reempacotou o API para não
disputar `dist/` nem o mesmo arquivo com uma tarefa que está rodando em paralelo na mesma árvore. O que esta frente
faz é conferir: pre-flight **ok**, metadados **ok**, versão **ok**. O que falta para ele subir é o cadastro em
`release/mods.json` (PUB-API-2) e a autorização do dono (PUB-API-3).

### 2.5 RoguelikeUnlimitedLevelProgression — preparado, mas **sem bump** (e continua `publicar: false`)

- **Por que sem bump:** a 0.1.1 **nunca foi publicada nem distribuída** — o pacote anterior (LEVEL-PACOTE-CONTRATO)
  foi montado em bancada isolada, prova de contrato, não de release. Não existe versão no ar a superar, então o bump
  seria um número sem significado. O que mudou desde aquele pacote de bancada foi **a própria fonte** (a correção do
  `OnDestroy` RLP-1/RLP-2, provada em jogo em 16/10: `politica: allow=True ... nivel=20 capVanilla=20`,
  `gameplay=20/20` após o OnDestroy), e o ZIP foi **reconstruído da fonte atual** — que é exatamente o que o
  pre-flight cobra (REL-1: artefato mais novo que a fonte).
- **Segue travado:** `publicar: false` em `release/mods.json`. O ZIP está pronto, mas liberar exige rodada de
  runtime autorizada + aceite humano do dono (motivo já registrado no ledger). Esta frente **não** alterou isso.

---

## 3. Pre-flight: saída

### 3.1 `python tools/pack-thunderstore.py --so-conferir` — verde (9/9, exit 0)

```text
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
EXIT=0
```

Antes do rebuild desta frente, este mesmo comando **reprovava** o ULLP por artefato velho
(`a DLL de bin/Release/ e MAIS ANTIGA que a fonte` — DLL 2026-10-15 19:51 x `Runtime/Policy.cs` 2026-10-16
11:22); o rebuild da §4 fechou essa reprovação.

### 3.2 `python tools/check_versoes.py` — verde (exit 0)

```text
  ==> os 9 mods batem nos quatro lugares (csproj = manifest = Plugin.cs = README)
EXIT=0
```

### 3.3 `python .github/scripts/valida_pacotes.py` (o gate do CI) — **reprova em 1 item** (exit 1)

```text
ok    BetterCombatText                 0.1.3    desc=191  icone=256x256, 124954 bytes
ok    BetterFont                       1.0.3    desc=212  icone=256x256, 87821 bytes
ok    BetterPortuguese                 0.1.0    desc=181  icone=256x256, 121749 bytes
ok    BetterStats                      1.0.2    desc=178  icone=256x256, 91250 bytes
ok    BetterTooltips                   0.1.4    desc=190  icone=256x256, 100373 bytes
ok    RoguelikeDebugger                0.1.3    desc=172  icone=256x256, 99954 bytes
ok    RoguelikeSkillTreeVisualizer     0.3.4    desc=238  icone=256x256, 57013 bytes
ok    RoguelikeUnlimitedLevelProgression 0.1.1    desc=201  icone=256x256, 104131 bytes
ok    api (pacote RealmApi)            0.1.0    desc=165  icone=256x256, 107728 bytes

FALHA dependencias (resolucao PKG-5) - o upload seria recusado pela Thunderstore (No matching package found)
        - RoguelikeSkillTreeVisualizer: depende de DefRuivo_StolenRealmMods-RealmApi-0.1.0, que NAO existe na Thunderstore (No matching package found for reference)

pacotes validados: 9 | com problema: 1
EXIT=1
```

Todos os **metadados** dos 9 pacotes passam (nome, semver, descrição, ícone 256x256, README/CHANGELOG). A única
reprovação é a resolução da dependência — a mesma coisa que `python tools/check_dependencias.py --local` mostra:

```text
  ok    RoguelikeSkillTreeVisualizer: BepInEx-BepInExPack-5.4.2305 (ja publicada)
  FALHA RoguelikeSkillTreeVisualizer: depende de DefRuivo_StolenRealmMods-RealmApi-0.1.0, que NAO existe na Thunderstore
ordem de envio (dependencia ANTES do dependente): ... 7. RoguelikeSkillTreeVisualizer ... 9. api
==> 1 dependencia(s) NAO resolvem
```

**O que falta, exatamente (não é consertável nesta frente):** o pacote `DefRuivo_StolenRealmMods-RealmApi-0.1.0`
precisa **existir na Thunderstore** antes de o RSTV 0.3.4 subir. Isso exige (a) a entrada do RealmApi no
`release/mods.json` — frente **PUB-API-2**, que este cartão não pode editar — e (b) a publicação dele — frente
**PUB-API-3**, gate do dono. O ZIP do API está pronto (§2.4) e o empacotador já o conhece. Enquanto isso, a ordem de
envio que o próprio gate imprime põe o API por último porque a lista dele é alfabética e não conhece a frente nova;
a ordem correta é: **RealmApi antes de RoguelikeSkillTreeVisualizer**, e o resto em qualquer ordem (nenhum outro
pacote declara dependência deste repositório — o BCT **deixou** de declarar o BetterFont nesta frente).

### 3.4 `bash tools/release-check.sh` (ritual global) — **reprova no passo 2/TRV-1** (exit 1)

```text
== PASSO 2/9 — PATCHES (trava TRV-1: 5 regras de robustez do Harmony) ==
     REPROVA BetterPortuguese/Plugin.cs  (sem linha de 'carregado' em LogInfo/Log)
   >>> TRAVA REPROVADA (TRV-1) <<<
  [FALHA] 2. patch reprovado pela TRV-1 — release travada
   Nada foi buildado e nada foi instalado no perfil: conserte e rode de novo.
```

Pré-existente e alheio a esta frente (BetterPortuguese, §2.2): REL-1 já tinha medido o mesmo vermelho. O ritual
morre **antes** do build, então ele não diz nada sobre os mods desta frente — quem cobre isso é o pre-flight de
pacote (verde, §3.1) e `check_versoes` (verde, §3.2). Passo 1/9 (versões) fechou verde; 5 avisos de
try/catch/`EhClasseDeGancho` são os mesmos que o repositório já carregava.

---

## 4. Como cada pacote foi construído (reprodutível)

```bash
# 1) rebuild Release SEM instalar no perfil (o alvo DeployToBepInEx é opt-in)
cd /c/dev/stolen-realm
for m in BetterCombatText RoguelikeDebugger RoguelikeSkillTreeVisualizer RoguelikeUnlimitedLevelProgression; do
  dotnet build $m/$m.csproj -c Release --no-incremental -p:DeployToBepInEx=false -p:DeployToScripts=false
done   # 4/4 com 1 aviso (MSB3277 System.Net.Http 4.1.2 x 4.2.0, herdado do Assembly-CSharp); 0 erros

# 2) pre-flight (todos os mods antes de zipar qualquer um)
python tools/pack-thunderstore.py --so-conferir

# 3) pacote
python tools/pack-thunderstore.py BetterCombatText RoguelikeDebugger \
       RoguelikeSkillTreeVisualizer RoguelikeUnlimitedLevelProgression
```

Saída do empacotador (cada ZIP com 5 arquivos: `manifest.json`, `README.md`, `CHANGELOG.md`, `icon.png` e
`plugins/<Mod>/<Mod>.dll`):

```text
gumatos-BetterCombatText-0.1.3.zip                 (dist:  158144 bytes)
gumatos-RoguelikeDebugger-0.1.3.zip                (dist:  136247 bytes)
gumatos-RoguelikeSkillTreeVisualizer-0.3.4.zip     (dist:  108237 bytes)
gumatos-RoguelikeUnlimitedLevelProgression-0.1.1.zip (dist: 141819 bytes)
```

### 4.1 A DLL mudou de verdade? (artefato publicado x artefato novo)

Conferido por SHA-256 tirando a DLL **de dentro** do ZIP antigo de `dist/` (os seis ZIPs de `dist/` são idênticos
aos downloads publicados — REL-1) e comparando com a DLL recém-buildada:

| Mod | DLL publicada | DLL nova | Iguais? |
|---|---|---|---|
| BetterCombatText | `d3fc0c1b…34009e1` | `02483198…1b9409f7` | não (só o literal de versão muda) |
| RoguelikeDebugger | `7465a7e0…e86f51f4` | `43aa414e…d6d6ccff96` | não (proveniência DBG-PROV-V1) |
| RoguelikeSkillTreeVisualizer | `329fbf71…fb3ad2c1` | `cd1517f3…5f8ec0fe346` | não (integração RealmApi UI) |

---

## 5. Estado final / próximos passos (para o pipeline)

1. Esta frente: **pronto para o disparo**, com as ressalvas abaixo. Nada publicado, nada instalado, nada empurrado.
2. **Ordem obrigatória de envio:** `RealmApi 0.1.0` **antes** de `RoguelikeSkillTreeVisualizer 0.3.4`. Os demais
   (`BetterCombatText 0.1.3`, `RoguelikeDebugger 0.1.3`) não declaram dependência de repositório e podem subir em
   qualquer ordem.
3. **Bloqueios abertos:** `release/mods.json` ainda não lista o RealmApi (PUB-API-2) e não tem as versões novas
   liberadas; `RoguelikeUnlimitedLevelProgression` e `BetterPortuguese` seguem `publicar: false`.
4. **Decisão pendente do dono:** reemitir ou não BetterFont/BetterStats/BetterTooltips só para publicar os
   CHANGELOGs corrigidos (§2.1).
5. `RoguelikeUnlimitedLevelProgression`: runtime autorizado + aceite humano continuam necessários antes de qualquer
   envio (§2.5).

### Evidências

- `docs/automacao/PUB-ALL-evidencias/pre-flight-saida.txt` — saída crua dos quatro gates (packer, versões,
  valida_pacotes, dependências).
- `docs/automacao/PUB-ALL-evidencias/release-check-saida.txt` — saída crua do ritual global (reprovação pré-existente).
- `docs/automacao/PUB-ALL-evidencias/dll-hashes.json` — hash da DLL nova x publicada, por mod.
- `docs/automacao/PUB-ALL-evidencias/zips.json` — sha256, tamanho, contagem de arquivos, manifest e hash de cada DLL
  lidos de **dentro** de cada ZIP de `dist/`.
