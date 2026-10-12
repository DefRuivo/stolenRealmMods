# LEVEL-PACOTE-CONTRATO — parte 01: ícone e gate `publicar:false` para o RLP

Cartão: `t_4056b88f` (perfil `default`). Branch de integração: `ci-validate-test` (base `06564ce`).
Data: 12/10/2026. Frente: **contrato de descoberta/metadados/release** do `RoguelikeLevelProgression`
(RLP) **depois** do LAND (`t_6ecff37a`) e das referências portáteis (`t_bca2b1b9`).

Este documento registra o que foi medido. Ele **não** é aprovação: runtime, publicação e push continuam
`NAO_EXERCITADO`.

## 1. O que mudou

| Caminho | Mudança | Por quê |
|---|---|---|
| `RoguelikeLevelProgression/icon.png` | **novo**, PNG 256x256, 943 bytes (`sha256 e5974920…fb591`) | era o único pacote descoberto sem ícone — o pre-flight do empacotador e o passo 8 do CI (`valida_pacotes.py`) reprovavam por isso |
| `release/mods.json` | entrada nova do RLP: `publicar:false`, `versao_publicada:null`, `publicado_em:null`, motivo *runtime e aceite humano pendentes* | o gate do `publish.yml` exige que a lista do JSON seja **a mesma** que `--listar-nomes`; sem a entrada o gate reprovava por divergência (6 x 7) |
| `tools/pack-thunderstore.py` | glifo `L` em `GLIFOS` + cor própria do RLP em `CORES_ICONE` | as iniciais `RL` caíam no glifo `?` da fonte 5x7; nenhum ícone já existente é regerado |
| `docs/ESTRUTURA.md` | §1 passa a citar o RLP como pacote descoberto **e bloqueado** | a política dizia "os seis mods distribuíveis"; a descoberta executável já listava 7 |
| `docs/README.md`, `docs/PUBLICACAO.md` | adendos datados de 12/10/2026 | as fotos de 01/10/2026 ("6 mods", "nenhum fora do ar") continuam preservadas; o adendo diz o que é verdade hoje |
| `docs/automacao/LEVEL-PACOTE-CONTRATO-parte01.md` | este relatório | evidência numerada nova, sem reescrever fotografia |

Nada foi copiado dos seis mods liberados: as entradas de `release/mods.json` deles ficaram **byte a byte
iguais**, o registro remoto (`release 3d73e07`) não foi substituído por versão antiga, e `api/` (RealmApi)
continua módulo separado — sem manifest, sem `dist/` e sem virar pacote.

## 2. Descoberta, versões e metadados (árvore canônica)

```
$ python tools/check_versoes.py
mods : 7 (BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeLevelProgression, RoguelikeSkillTreeVisualizer)
  ==> os 7 mods batem nos quatro lugares (csproj = manifest = Plugin.cs = README)   [rc=0]
```

```
$ python tools/pack-thunderstore.py --listar-nomes
BetterCombatText
BetterFont
BetterStats
BetterTooltips
RoguelikeDebugger
RoguelikeLevelProgression
RoguelikeSkillTreeVisualizer
```

```
$ python .github/scripts/valida_pacotes.py
ok    RoguelikeLevelProgression        0.1.1    desc=201  icone=256x256, 943 bytes
pacotes validados: 7 | com problema: 0        [rc=0]
```

```
$ python tools/check_dependencias.py --local
mods deste repo: … RoguelikeLevelProgression …
  ok    RoguelikeLevelProgression: BepInEx-BepInExPack-5.4.2305 (ja publicada)
  ==> todas as dependencias resolvem      [rc=0]
```

Não foi criada segunda lista estática: `--listar-nomes`, `check_versoes`, `valida_pacotes`,
`check_dependencias` e o gate do workflow todos leem a **mesma** descoberta (`eh_mod`).

## 3. Gate de publicação (`release/mods.json`)

O código do passo *Gate dos mods liberados* foi **extraído do próprio `publish.yml`** (o heredoc
`python - <<'PY'` da seção 1 do workflow) e executado local por um script **de rodada, fora do repo**
(`C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_4056b88f\ev\gate_release.py`: recorta o
heredoc, ajusta o recuo e roda com `MOD`/`GITHUB_OUTPUT` definidos — é a mesma fonte, não uma
reimplementação). As duas respostas:

```
$ python gate_release.py . todos
alvos: BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer
team : DefRuivo_StolenRealmMods                                             rc=0

$ python gate_release.py . RoguelikeLevelProgression
::error::RoguelikeLevelProgression esta com publicar:false em release/mods.json e NAO sera publicado.
Motivo registrado: BLOQUEADO para publicacao (LEVEL-PACOTE-CONTRATO, 12/10/2026): runtime e aceite
humano pendentes. …                                                    rc=1
```

Ou seja: o RLP **não** entra em `alvos` no disparo `todos` (seis seguem saindo) e é **recusado pelo nome**
com o motivo visível — `BLOQUEADO para publicação`, não "publicável por engano".

### Provas negativas (o teste tem de poder reprovar)

* **Sem o ícone** (ícone movido de lado na bancada): `--so-conferir` → `FALHA … icon.png nao existe`
  (`rc=1`) e `valida_pacotes.py` → `pacotes validados: 7 | com problema: 1` (`rc=1`). Foi esse o estado
  do repositório **antes** desta frente no passo 8 do CI.
* **Com a fotografia anterior de `release/mods.json`** (6 entradas, sem o RLP):
  `::error::release/mods.json e o empacotador divergem - a lista de mods tem uma fonte so
  (tools/pack-thunderstore.py --listar-nomes). JSON=[6 nomes] | empacotador=[7 nomes]` (`rc=1`).

## 4. Bancada NOVA, sem perfil e sem jogo

Bancada: `C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_4056b88f\bancada` — cópia **nova** do
repositório (fontes, `tools/`, `release/`, `api/`, `tests/`, `.github/`, `Directory.Build.props`), com
`bin/`, `obj/`, `__pycache__/`, `dist/` e `lib/` **ausentes** e **nenhuma DLL** antes do build.

```
$ python tools/check_deploy_optin.py     -> 8 alvo(s) de deploy, todos com Condition="'$(DeployToBepInEx)' == 'true'"   [rc=0]

# bancada sem lib/ e sem override (negativo, reproduzido):
$ dotnet build RoguelikeLevelProgression/RoguelikeLevelProgression.csproj -c Release -p:DeployToBepInEx=false
  error : LEVEL-LIB: lib de referencias nao encontrada em '…\bancada\RoguelikeLevelProgression\..\lib' …   [rc=1, 1 erro, 0 avisos, 0,75s]

# ORDEM: API Release ANTES do RSTV (o RSTV consome ..\api\Plugin\bin\Release\…)
$ dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=false -p:GameLibDir=C:/dev/stolen-realm/lib
  0 Erro(s)                                                                                              [rc=0]

$ dotnet build <Mod>/<Mod>.csproj -c Release -p:DeployToBepInEx=false -p:CommonLibDir=C:/dev/stolen-realm/lib
  RLP rc=0 | (via junction lib→C:\dev\stolen-realm\lib, sem copiar assembly privada para a bancada)
  BetterCombatText rc=0 | BetterFont rc=0 | BetterStats rc=0 | BetterTooltips rc=0 |
  RoguelikeDebugger rc=0 | RoguelikeSkillTreeVisualizer rc=0                                  (0 erros CS cada)

$ dotnet build tests/RoguelikeLevelProgression.Harness/… -c Release -p:DeployToBepInEx=false -p:CommonLibDir=…   [rc=0]

$ python tools/pack-thunderstore.py --so-conferir
  ok    RoguelikeLevelProgression v0.1.1 | …\bin\Release\netstandard2.1\RoguelikeLevelProgression.dll
  Pre-flight verde para 7 mod(s). Nada foi empacotado (--so-conferir).                                   [rc=0]

$ python tools/pack-thunderstore.py
PRONTO - 7 pacote(s) em dist/   (destino NOVO: a bancada; o dist/ do dono não foi tocado)

# NENHUM alvo de deploy rodou em nenhum build acima (opt-in ausente + -p:DeployToBepInEx=false).
```

### O que foi lido DENTRO do ZIP (pacote do RLP)

```
ZIP: gumatos-RoguelikeLevelProgression-0.1.1.zip   33097 bytes
     sha256 b4eba1db9ebf2343362d0b121868873b1e4eba39869aa298542b3130a551d542
  testzip: integridade ok
  membros (5):
    CHANGELOG.md                                                  6924 bytes
    README.md                                                     8131 bytes
    icon.png                                                       943 bytes   (IHDR 256x256)
    manifest.json                                                  471 bytes
    plugins/RoguelikeLevelProgression/RoguelikeLevelProgression.dll 57856 bytes
  manifest: name=RoguelikeLevelProgression version=0.1.1 deps=['BepInEx-BepInExPack-5.4.2305'] desc_len=201
  hash DLL no ZIP : 2990176db7e602b578c61eb628a2b10d7568764f3792acee67fd4d61fe6ff865
  hash DLL build  : 2990176db7e602b578c61eb628a2b10d7568764f3792acee67fd4d61fe6ff865   IDENTICOS
```

Os **sete** ZIPs da bancada têm 5 membros cada, `testzip` íntegro, ícone 256x256 e hash da DLL igual ao
da build correspondente; a varredura por **assembly privada** (Assembly-CSharp, BepInEx.dll, 0Harmony,
UnityEngine*, Sirenix*, RealmApi, Newtonsoft, System.*) devolveu `NENHUM` membro proibido.

### Dist do dono: bytes preservados

`sha256sum dist/*.zip` antes e depois: **27 arquivos idênticos** (`diff` limpo), nenhum ZIP sobrescrito e
nenhum pacote novo criado no repositório canônico. Empacotamento só aconteceu na cópia isolada, com
destino novo.

## 5. Limites desta prova (o que NÃO foi exercitado)

* **Runtime:** nenhum boot, nenhuma instalação, nenhum `LogOutput.log`. "Passou" aqui é pre-flight,
  build sem deploy e estrutura de pacote — **não** é "o mod funciona em jogo".
* **Perfil/saves/DLLs do dono:** intocados; nenhum build com `-p:DeployToBepInEx=true`.
* **Publicação/push/deploy:** nenhum. O RLP segue `publicar:false` e o trabalho está no branch de
  integração `ci-validate-test`, não em `main` (aterrissagem é frente própria, autorizada).
* **CI remoto:** o gate foi executado pelo código extraído do `publish.yml`, localmente; nenhum run de
  GitHub Actions foi disparado.
* **Estética do ícone:** é o ícone **gerado pelo próprio empacotador** (fundo sólido + borda + iniciais
  `RL`), como já previsto em `--gerar-icones`. Como o mod não vai ser publicado, o dono pode desenhar um
  ícone próprio depois; trocar o arquivo é o suficiente (o pacote sai do mesmo caminho).
* **Não** foi usada a palavra "PASSOU" para runtime não autorizado.
