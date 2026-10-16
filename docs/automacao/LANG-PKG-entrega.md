# LANG-PKG — entrega (padrão de idioma do que entra no ZIP do lote)

Cartão: **t_4167fdc4 (LANG-PKG)** — 2026-10-16.
Escopo: os **cinco pacotes do lote** que vão subir agora. O README e o CHANGELOG dentro do ZIP são
**imutáveis** depois do upload; esta entrega acerta o idioma **antes** do empacotamento.

## 1. O padrão aplicado

Verbatim de `BetterStats/CHANGELOG.md:11` (a definição do padrão):

> **The package page is now in English.** The description and the README were rewritten in English, in the same
> shape as the other packages of this project (what it does, what it does not do, install, uninstall, build).
> A short Portuguese summary stays at the end of the README.

- **README do pacote:** inglês completo (o que faz / o que não faz / configuração / instalar / desinstalar /
  compilar) e, no fim, uma **seção curta em português**. Referências conformes: `RoguelikeSkillTreeVisualizer/README.md`
  (`## Português (BR)` no fim), `RoguelikeUnlimitedLevelProgression/README.md` (bloco final em português) e o
  `README.md` da raiz (`# English` … `# Português (BR)`).
- **CHANGELOG:** inglês. Referências conformes: `BetterTooltips/CHANGELOG.md` e `RoguelikeSkillTreeVisualizer/CHANGELOG.md`.
- Para o **RealmApi** (`api/README.md`, que é README de API) a forma é a de ferramenta/desenvolvedor — o que é /
  o que promete / o que **não** promete / como usar / como construir / como testar —, e não a de mod de jogador.

## 2. Tabela de mudanças

Métricas medidas com o mesmo script para antes (`git show HEAD:<arquivo>`) e depois (disco).
"palavrasPT/palavrasEN" contam um dicionário curto de palavras funcionais de cada idioma — é uma medida
**aproximada**, serve para mostrar a virada de idioma, não é um juiz linguístico.

| arquivo | idioma antes | idioma depois | o que mudou |
|---|---|---|---|
| `BetterCombatText/CHANGELOG.md` | corpo em PT + trechos já em EN (palavrasPT 1073 / palavrasEN 105; 208 tokens acentuados) | **EN** (palavrasPT 107 / palavrasEN 1132; 3 tokens acentuados) | corpo inteiro traduzido (0.1.3, 0.1.1, BCT-2..BCT-5, R2, 0.1.0 e o bloco de dependência histórica). O único trecho acentuado que sobrou é uma **citação literal de log** (`cor da LETRA no alvo='#CBB396'…`). `git diff --numstat`: 206+/207− |
| `RoguelikeDebugger/CHANGELOG.md` | corpo em PT (palavrasPT 411 / palavrasEN 22; 177 tokens acentuados) | **EN** (palavrasPT 45 / palavrasEN 402; **0** token acentuado) | 0.1.3, 0.1.2, 0.1.1, "What this version does NOT prove", nota histórica do RD-2 e 0.1.0 traduzidos; cabeçalho de auditoria traduzido. 41+/42− |
| `RoguelikeUnlimitedLevelProgression/CHANGELOG.md` | PT, inclusive o cabeçalho (palavrasPT 352 / palavrasEN 7; 178 tokens acentuados) | **EN** (palavrasPT 47 / palavrasEN 345; 1 token acentuado) | todas as seções traduzidas (RLP-1/RLP-2, identidade do pacote, proteção de carga R3-01, compatibilidade, 0.1.0, baseline histórico do harness, correções da bancada). O token acentuado restante é o literal de log `carregado.`. 101+/101− |
| `api/CHANGELOG.md` | PT (palavrasPT 108 / palavrasEN 2; 81 tokens acentuados) | **EN** (palavrasPT 16 / palavrasEN 137; 1 token acentuado) | 10 bullets + fecho traduzidos; cabeçalho de auditoria traduzido. 14+/14− |
| `api/README.md` | **inteiramente em PT** (palavrasPT 703 / palavrasEN 24; 352 tokens acentuados) | **EN + seção curta PT no fim** (palavrasPT 227 / palavrasEN 863) | reescrito na forma do padrão: acrescentadas as seções **What it does** e **What it does not do** (derivadas do texto que já existia — nada inventado), todo o resto traduzido (alvo do jogo, como usar, família UI, config, construir, smoke, atualizar, contribuir, não exercitado, licença) e a seção `## Português (BR)` no fim (linha 355 de 392). 307+/242− |

**Não tocados (já conformes, conferidos)** — a regra era não traduzir o que já está no padrão:

| arquivo | veredito |
|---|---|
| `RoguelikeSkillTreeVisualizer/README.md` | conforme: seções EN `What the button does` / `What it does not do` / `Configuration` / `Install` / `Uninstall` / `Build from source` e `## Português (BR)` no fim |
| `RoguelikeSkillTreeVisualizer/CHANGELOG.md` | conforme: **0** linha com acento PT em 311 linhas (verificado por grep) |
| `RoguelikeUnlimitedLevelProgression/README.md` | conforme: EN + bloco final em português |
| `BetterCombatText/README.md`, `BetterTooltips/CHANGELOG.md`, `BetterStats/CHANGELOG.md`, `README.md` (raiz) | conformes (usados como referência do padrão) |

## 3. Prova de que a tradução não mexeu no que não podia mexer

Script de conferência sobre as 5 versões antes (HEAD) × depois (disco):

- **Identificadores** (caminhos, nomes de arquivo `.csproj/.dll/.json/.py/.md/.cs/.txt/.cfg/.png/.zip/.acf`,
  hashes hex, nomes com ponto tipo `Game.EvalVoid`, `Character.Load`): **0 ausentes** em cada arquivo —
  40/40, 11/11, 28/28, 25/25 e 84/84.
- **Literais numéricos** (`sha256`, versões, GUIDs, offsets, medidas): **0 perdidos** nos cinco arquivos. As três
  diferenças que o comparador acusa (`1.0.1`, `2,`, `2.1,`) são **pontuação adjacente** virando parte do token
  (ex.: `1.0.1,` → `1.0.1`), conferidas linha a linha: a contagem de ocorrências por linha é idêntica.
- **Estrutura**: contagem de cabeçalhos (`^#`) e de bullets (`^- `) **idêntica** nos quatro CHANGELOGs
  (12/8/11/2 cabeçalhos; 52/20/23/10 bullets). No `api/README.md` a contagem sobe de 14 para 17 — exatamente
  as **três** seções novas exigidas pelo padrão: `What it does`, `What it does not do` e `## Português (BR)`.
- **Cabeçalhos de auditoria da CHG-REV**: preservados nos **5** arquivos (a linha `> CHG-REV documentation audit:
  2026-10-16 …`), traduzidos junto com o resto.
- **Seções de configuração e chaves**: os nomes reais de seção/chave do `.cfg` (`1. Geral`, `2. Nomes de inimigos
  (combate)`, `CorSombraClara`, `EnableHooks`, …) ficaram **como estavam** — são literais lidos do arquivo, não prosa.

## 4. ZIPs reempacotados (de-para de hash)

Feito: rebuild Release **sem** deploy (`dotnet build -c Release --no-incremental -p:DeployToBepInEx=false`, 6
projetos: os 3 mods de raiz + `api/Core`, `api/Hooks`, `api/Plugin`, todos **0 erro**) e reempacote com
`python tools/pack-thunderstore.py <mod>`. Pre-flight oficial antes de empacotar:
`python tools/pack-thunderstore.py <4 mods> --so-conferir` → **verde para 4 mod(s)**.

| pacote | zip em `dist/` | sha256 antes | sha256 depois |
|---|---|---|---|
| BetterCombatText 0.1.3 | `gumatos-BetterCombatText-0.1.3.zip` (157846 B) | `ef6f1bd8c393ddcac92c54961cbf19f7d51ab7f3d42a3dfbd7723c2d4e747208` | `148adf1443ab4ac48b07f1cf274da4d669f3d8335a1f708578a8ffc5c4c54f11` |
| RoguelikeDebugger 0.1.3 | `gumatos-RoguelikeDebugger-0.1.3.zip` (136099 B) | `c615a868ed7a34f0364b6bdae8da39d39a1d0a275517a8b9db490ca3ee298a84` | `e1b99240125f50e4bcc7741244fe01fd41f7ca0c884970229547a149908638bf` |
| RoguelikeUnlimitedLevelProgression 0.1.1 | `gumatos-RoguelikeUnlimitedLevelProgression-0.1.1.zip` (141552 B) | `ed42ec6de5ebcb07a0442aaf44f86881a53c4e61fe7b92e01b60bc35087af429` | `40dd861ce5940b2a5816fa39f6d94a78784fe5f4da5a909bf4ec6f6c824bf5dc` |
| RealmApi 0.1.0 | `gumatos-RealmApi-0.1.0.zip` (143595 B) | `e13e725be6b84fd07b662a276d62285d1c7a6a0b5fdc88078e6fa7bbf3d4ee8b` | `503846842740d0c14279c60d7b400c05a6ca869c7f1da1f43e792554c5cb997e` |
| RoguelikeSkillTreeVisualizer 0.3.4 | `gumatos-RoguelikeSkillTreeVisualizer-0.3.4.zip` | `cc2f0a2e94137071609657bbaba3a05fec1ae0178352a4ff2348ad19458dd225` | `cc2f0a2e94137071609657bbaba3a05fec1ae0178352a4ff2348ad19458dd225` (**inalterado** — nada mudou, não reempacotado) |

Prova **dentro do ZIP** (sha256 dos membros, antes × depois) de que só o texto mudou:

| pacote | membro | antes (16 primeiros) | depois |
|---|---|---|---|
| BetterCombatText | `CHANGELOG.md` | `d935fcc745ab42c2` | `e26ff9e90e0f17e1` |
| | `README.md`, `icon.png`, `manifest.json`, `plugins/BetterCombatText/BetterCombatText.dll` | `01cb378a2d8e6a15`, `9b3d2701937f0e62`, `ff0cf60586cfceef`, `024831980fb99ba8` | **iguais** |
| RoguelikeDebugger | `CHANGELOG.md` | `7c62dc1a3c854586` | `98022e628d781e4b` |
| | `README.md`, `icon.png`, `manifest.json`, `plugins/RoguelikeDebugger/RoguelikeDebugger.dll` | `b469a218a5908f37`, `9e8d822619dd8456`, `f784e4c839f0947f`, `43aa414e300de4cd` | **iguais** |
| RoguelikeUnlimitedLevelProgression | `CHANGELOG.md` | `b4b7b381335dbc2e` | `406d8895199bbcf8` |
| | `README.md`, `icon.png`, `manifest.json`, `plugins/…/RoguelikeUnlimitedLevelProgression.dll` | `b412e5a920031962`, `a93cfacdaed6bd98`, `3de31bb6e4a34b37`, `bff477bd26a85df0` | **iguais** |
| RealmApi | `CHANGELOG.md` | `26d354098b2aa3b5` | `50a84862c6352197` |
| | `README.md` | `8d7a4fc236ec8a74` | `bc8c767ea7036218` |
| | `LICENSE`, `icon.png`, `manifest.json`, `plugins/RealmApi/RealmApi.dll`, `RealmApi.Core.dll`, `RealmApi.Hooks.dll` | `09b0670f8aa43e89`, `2b6673512d4250db`, `02b871daf08c36e1`, `764b72d84a976a53`, `d4e72f24e4e7c503`, `86d7fcf0012e1a61` | **iguais** |

Ou seja: o pacote mudou **só** no CHANGELOG (e, no RealmApi, também no README). Nenhuma DLL, ícone, LICENSE ou
manifest foi tocado — o rebuild Release é reprodutível byte a byte para o mesmo fonte.

Também conferido: o `CHANGELOG.md`/`README.md` **dentro** de cada ZIP é byte a byte igual ao do repositório
(sha256 comparado um a um; 7/7 `IGUAL`), e a seção `## Português (BR)` do README do RealmApi está na **linha 355
de 392** do que foi zipado — no fim, como o padrão pede.

## 5. Confirmação: os 5 pacotes do lote estão no padrão

| pacote | README | CHANGELOG | veredito |
|---|---|---|---|
| BetterCombatText | EN + seção curta PT no fim (já conforme, conferido) | EN (traduzido nesta entrega) | **no padrão** |
| RoguelikeDebugger | EN + seção curta PT no fim (já conforme) | EN (traduzido nesta entrega, 0 acento) | **no padrão** |
| RoguelikeUnlimitedLevelProgression | EN + bloco final PT (já conforme, não mexido) | EN (traduzido nesta entrega) | **no padrão** |
| RealmApi (`api/`) | EN completo + `## Português (BR)` no fim (reescrito nesta entrega) | EN (traduzido nesta entrega) | **no padrão** |
| RoguelikeSkillTreeVisualizer | EN + `## Português (BR)` (já conforme) | EN (já conforme, 0 acento) | **no padrão** (conferido, não reescrito por gosto) |

## 6. Gates executados depois da mudança

| gate | resultado |
|---|---|
| `python tools/check_versoes.py` | **verde** — "os 9 mods batem nos quatro lugares (csproj = manifest = Plugin.cs = README)" |
| `python tools/pack-thunderstore.py <4 mods> --so-conferir` | **verde** (pre-flight completo, nada empacotado) |
| `python .github/scripts/valida_pacotes.py` | 9 pacotes validados; **1 problema pré-existente**: RSTV depende de `DefRuivo_StolenRealmMods-RealmApi-0.1.0`, que ainda não existe na Thunderstore (regra PKG-5 de ordem de envio — resolvido pelo lote, não por este cartão) |
| `python tools/audita_docs.py` | **mesmas 11 pendências de antes desta entrega** — conferido rodando o script com os 5 arquivos **revertidos a HEAD** e comparando a lista (idêntica, 11 itens): a tradução **não acrescentou pendência nenhuma**. Os 11 itens são pré-existentes e de outros assuntos (ferramenta citada que não existe, dependências esperadas × manifest, caminho `ReloadProbe` citado em 2 docs, "api: versao diverge" — este último é o estado conhecido de preparação do RealmApi) |
| `python tools/check_segredos.py` / `python tools/check_patches.py` | falham por motivos **pré-existentes e fora do escopo deste cartão** (entropia em `docs/automacao/EV-R2-*`, `KIT-14-*`; teste de ciclo em código-fonte `.cs`). Grep nos dois relatórios: **nenhum** dos 5 arquivos deste cartão aparece como achado |
| `python tools/check_fix_keys.py`, `check_dupes.py`, `check_notas_redundantes.py` | verdes |

## 7. O que NÃO foi feito (traças respeitadas)

- **Não publiquei** nada e **não dei push** — a mudança está só no disco.
- **Não instalei** no perfil do r2modman (todos os builds foram `-p:DeployToBepInEx=false`).
- **Não mexi em `release/mods.json`** (segue intocado; quem libera envio é o dono).
- **Não reescrevi** o que já estava conforme (RoguelikeSkillTreeVisualizer, os READMEs de BetterCombatText e
  RoguelikeUnlimitedLevelProgression).
- **Não toquei em `docs/`** além do **único arquivo desta entrega** (`docs/automacao/LANG-PKG-entrega.md`).
  A documentação interna continua em português.
- Não traduzi a documentação interna (`docs/**`, relatórios): o padrão vale só para o que entra no ZIP.

## 8. Ressalvas

- A tradução é do agente. **O dono é o revisor de texto** deste projeto; se algum wording não agradar, o custo de
  corrigir agora é editar o `.md` e **reempacotar** (barato) — depois do upload, custa uma versão nova por mod.
- As métricas PT/EN da seção 2 são **aproximadas** (dicionário curto de palavras funcionais): servem para mostrar
  a virada de idioma, não como veredito linguístico.
- `dist/` é artefato de build e está no `.gitignore`: os ZIPs e os hashes desta entrega **não entram no git** —
  por isso o de-para de hashes fica registrado aqui.
- Os 11 itens do `audita_docs.py` e as duas falhas de `check_segredos.py`/`check_patches.py` **não foram
  consertados** por este cartão: são de frentes anteriores e mexer neles seria fora do escopo (e alguns são
  justamente o estado que as outras tarefas do quadro estão tratando).
