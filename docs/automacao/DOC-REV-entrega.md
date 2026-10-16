# DOC-REV — revisão da documentação viva

Cartão: `t_d9d74e4d`. Data: 16/10/2026 (Hora oficial do Brasil, UTC-03:00). Repositório: `C:/dev/stolen-realm`.
Nenhum jogo foi aberto, nenhum build/deploy foi rodado, nenhuma publicação foi feita, nenhum
manifest/CHANGELOG de mod foi editado e nada de `docs/automacao/**` ou `docs/cobertura/**` foi revisado
(este arquivo de entrega é a única exceção).

**Rodadas.** Rodada 1 (implementação, commit `844bba8`) revisou os 20 documentos do escopo e corrigiu 11.
Rodada 2 (revisão independente, run 1603) pediu mudanças: 5 afirmações falsas/contraditórias que
escaparam (`A1`–`A5`), âncoras de linha erradas nesta entrega (`A6`) e contagens desatualizadas (`A7`).
Rodada 3 (run 1605, commits `0afd6ea` + `7653410`) fechou `A1`–`A7` e as derivações encontradas
durante o fechamento (`A8`–`A10`).
Rodada 4 (esta, run 1609) fecha o achado `B1` da rodada 2 (execução): a família de afirmações
"o gate `release/mods.json` tem 8 entradas / não tem `RealmApi`" era falsa **no arquivo da árvore de
trabalho**. Em vez de continuar escrevendo para o estado de `HEAD` sem dizer isso, cada passagem
passou a **carimbar o referente** (`HEAD` × árvore de trabalho).

## 0. Cobertura

- **Arquivos do escopo revisados: 20 de 20** (a lista nominal do cartão) — 20 existem, 20 lidos.
  `README.md`, `STATUS.md`; `docs/README.md`, `AMBIENTE.md`, `ESTRUTURA.md`, `CI.md`, `PUBLICACAO.md`,
  `SUPERVISAO.md`, `PROCESSO-REVISAO.md`, `PLANO-DE-TESTES.md`, `MODS-PARA-AMIGOS.md`, `DEBUGGER.md`,
  `DBG-PROVENIENCIA.md`; `api/README.md`, `api/docs/README.md`; `ITEM_INVENTORY.md`,
  `ITEM_MOD_INVENTORY.md`, `STATUS_INVENTORY.md`, `SKILL_INVENTORY.md`, `TOOLTIP_SWEEP.md`.
- Contexto do repositório, medido em **16/10/2026 14:20**, no commit `fc24267` (rodada 4) + árvore de
  trabalho: **672 arquivos `.md` versionados** (`git ls-files '*.md'`), **956 arquivos versionados em
  `docs/automacao/`** (arquivo histórico, fora do escopo) e **135 arquivos `.md`/`.json`/`.txt`
  versionados fora de `automacao/`+`cobertura/`.
  As três contagens deram **o mesmo valor** no commit `39852b7` (base do A7, 16/10 13:58) e agora:
  esta frente só **editou** arquivos existentes, não criou nem apagou nenhum. Elas, porém, **andam
  sozinhas**: as frentes paralelas commitam relatórios em `docs/automacao/` durante o dia (670 → 671 →
  672 `.md` ao longo da tarefa, e 950 → 951 → 956 arquivos em `automacao/`).
  Quem reconferir depois verá outro valor sem que nada tenha ficado errado.
- Dos 20 do escopo, **11 exigiam correção** e foram corrigidos; 9 não tinham problema factual.
- Revisão anterior deste cartão morreu por *rate limit* (run 1593) deixando as edições em disco, sem
  commit e sem entrega; elas foram relidas e reverificadas nas rodadas seguintes.

Legenda de classe: **1** afirmação falsa sobre o estado atual · **2** contradição entre documentos ·
**3** instrução que não funciona · **4** link quebrado interno · **5** falta de informação essencial.

## 1. Rodada 3 — fechamento das mudanças pedidas pela revisão independente

| item | arquivo | linha (estado final) | problema | classe | o que foi feito |
|---|---|---|---|---|---|
| A1 | `docs/PUBLICACAO.md` | 241-243 e **266-274** | "O caso de hoje: o `BetterCombatText 0.1.1` depende do **`BetterFont 1.0.2`**, que ainda **não está no ar** (a última publicada é a `1.0.1`)" — falso: o manifest do BCT declara **só** `BepInEx-BepInExPack-5.4.2305` desde 16/10 (DEP-REV) e o `BetterFont` no ar é **1.0.3** (07/10) | 1, 2 | reescrito: "O caso de hoje (16/10/2026) **não é** o desse exemplo…" — nenhum mod declara dependência de pacote a outro mod de jogo; a **única** dependência real é `RoguelikeSkillTreeVisualizer 0.3.4 → RealmApi-0.1.0`, que **não resolve** (404 na API) e faz o `check_dependencias.py --local` reprovar; o `ordem_de_envio.caso_de_hoje` do gate fica declarado como fotografia de 01/10 (frente própria). O exemplo acima (241-243) passou a ser **condicional** ("Se um mod declara… `BetterFont-1.0.2`") em vez de citar o par que não existe mais. |
| A2 | `docs/PUBLICACAO.md` | **283-286** | o bloco `json` apresentado como "o `release/mods.json` é o substituto versionado" mostrava `BetterFont: publicar:false, versao_publicada:null` — o real é `publicar:true`, `"1.0.3"`, `publicado_em 2026-10-07T21:24:48.179123Z` | 1 | substituído por **trecho real** do arquivo (com o `motivo` abreviado) + nota de que as duas travas (`BetterPortuguese`, RLP) são as **únicas** com `publicar:false`/`null`. |
| A3 | `docs/README.md` | **552-555** | "quem **pode** sair é o gate versionado `release/mods.json` (**6** entradas, todas com `publicar: true`)" — o gate tem **8** entradas: 6 `true` + 2 `false` (`BetterPortuguese`, `RoguelikeUnlimitedLevelProgression`) | 1, 2 | corrigido para "**8** entradas: **6** com `publicar: true` … e **2** com `publicar: false`, `BetterPortuguese` e `RoguelikeUnlimitedLevelProgression`"; o mesmo arquivo já dizia 8 nas linhas 32-43. Na rodada 4, `B1.2` acrescentou o carimbo: **8 em `HEAD`** e **9 na árvore de trabalho**. |
| A4 | `docs/AMBIENTE.md` | **38** | `Better Combat Text 0.1.1 | projeto (depende do Better Font)` — quinta ocorrência da dependência já removida | 1, 2 | virou "o **par carregado** no perfil é BCT + `Better Font`; o manifest corrente do BCT **não** declara dependência de pacote — foi removida em 16/10/2026 (DEP-REV)". A tabela descreve **o que o log carregou** (rodada de 12/09), não o manifest de hoje. |
| A5 | `docs/README.md` **387**, **484-489**, **566-570**; `README.md` **268**, **321-325**, **694**, **748-752**; `docs/CI.md` **84-86**; `docs/PUBLICACAO.md` **588** | — | `tools/publish-thunderstore.sh --go` apresentado como caminho de publicação/empacotamento ("o mais simples hoje", "continua valendo como caminho alternativo"), contradizendo `docs/PUBLICACAO.md` §4 (envio **legado**, não lê o gate, itera todos os `dist/gumatos-*.zip`, header de auth sem a variável `TOKEN`) | 2 | os nove pontos foram alinhados à mesma trava e ao mesmo aviso: **legado, não é caminho seguro**, não lê o gate, sem aprovação humana, sobe todos os `dist/gumatos-*.zip`; o caminho de hoje é o `publish.yml`. Conferido em `git show HEAD:tools/publish-thunderstore.sh` (laço `for z in dist/gumatos-*.zip`; header de autorização literal, sem a variável `TOKEN`). |
| A6 | esta entrega | §4 e §5 | a coluna "linha" tinha âncoras erradas: PNG do README em 388…545 (eram 390…547) e `docs/README.md` 393-404/407-411/435 (eram 397-407/412-417/439) | 4 | todas as âncoras foram **remedidas com `grep -n`** depois das edições desta rodada. **Remedidas de novo na rodada 4** (as correções de `B1` somaram linhas acima delas): PNG do README em **394, 404, 410, 415, 444, 458, 464, 541, 551**; `docs/README.md` tabela dos 8 mods **401-412**, "reconferido nos endpoints" **416-419**, linha de `dependencies` **447**; nota da PUB-ALL-1 **420-422**. |
| A7 | esta entrega | §0 | contagens "670 `.md` versionados / 950 em `docs/automacao/`" contra 671/951 medidos pelo revisor | 1 | remedidas e **carimbadas** (672 / 956 em 16/10/2026, commit `39852b7`) com a explicação de que a contagem cresce a cada commit das frentes paralelas. **Rodada 4:** remedidas no commit `fc24267` (16/10 14:20) — mesmos **672 / 956 / 135** (esta revisão só editou arquivos existentes). |

### Derivações encontradas ao fechar A1–A7 (não estavam na revisão)

| item | arquivo | linha | problema | classe | o que foi feito |
|---|---|---|---|---|---|
| A8 | `README.md` (3 tabelas), `docs/README.md` | 210-212, 362-364, 637-639; 405/410/411, 420-422, 447 | **deriva do dia**: o commit `39852b7` (PUB-ALL-1, 13:58) bumpou `BetterCombatText 0.1.2→0.1.3`, `RoguelikeDebugger 0.1.2→0.1.3` e `RSTV 0.3.3→0.3.4` nos quatro lugares — **depois** do commit da rodada 1 (13:49) e depois da revisão independente. Toda "versão no fonte/disco" das docs passou a mentir por um bump; a dependência do RSTV também era citada como `0.3.3` | 1 | tabelas do README atualizadas para 0.1.3/0.1.3/0.3.4; tabela dos 8 mods descobertos atualizada na coluna "Versão no disco"; linha de `dependencies` para `RoguelikeSkillTreeVisualizer 0.3.4`; acrescentado o parágrafo 420-422 declarando que a versão no disco está **à frente** da publicada (nada foi publicado nesse bump). Conferido contra `*/manifest.json`, `python tools/check_versoes.py` (exit 0) e a API. |
| A9 | `docs/README.md` | 425-434 | o adendo datado de 12/10 ("o projeto tem um **sétimo** pacote descoberto", "conjunto esperado pelo workflow passa a ser **7** nomes", "a tabela acima (6 mods)") contradizia a tabela de **8** mods descobertos (16/10) logo acima | 2 | adendo mantido como fotografia datada, com o estado corrente ao lado: "7 nomes então; **8** desde 16/10/2026, com o `BetterPortuguese`", e a frase final reescrita para não alegar que a tabela de cima tem 6 mods. |
| A10 | `docs/PUBLICACAO.md` | 57-58, 64 | o adendo de 12/10 dizia "o `release/mods.json` tem **7** entradas" e "o conjunto esperado … (7 nomes)", contra as **8** do cabeçalho do mesmo arquivo (linha 9) | 2 | "passou a ter 7 entradas (oito desde 16/10/2026, com o `BetterPortuguese`)" e "(7 nomes então; **8** desde 16/10/2026 …)". |

## 1B. Rodada 4 — `B1`: carimbar o referente (`HEAD` × árvore de trabalho)

O achado `B1` da rodada 2 (execução, run 1608) apontou **8 passagens** que descreviam o gate
`release/mods.json` como corrente, quando o texto valia só para o estado **commitado**. Medido nesta
rodada (`C:/dev/stolen-realm`, 16/10/2026):

- `git show HEAD:release/mods.json` → **8** entradas de mod (6 `publicar: true` + 2 `false`:
  `BetterPortuguese`, `RoguelikeUnlimitedLevelProgression`);
- `release/mods.json` na **árvore** → **9** entradas (6 `true` + **3** `false`; a nona é `RealmApi`,
  `publicar: false`, `versao_publicada: null`, entrada de preparação da `PUB-API-2`);
- `python tools/pack-thunderstore.py --listar-nomes` na árvore → **9** (bate com o gate da árvore).

| item | arquivo | linha (estado final) | problema | classe | o que foi feito |
|---|---|---|---|---|---|
| B1.1 | `docs/README.md` | 32-43 | "a mesma lista de oito nomes está no gate `release/mods.json`" e o bloco do aviso, que se declara sobre a **árvore**, dizia "o gate segue com oito … nenhum RealmApi" — falso na árvore | 1, 2 | carimbado: "o empacotador **versionado** (`HEAD`)"; "os mesmos oito nomes estão no gate **em `HEAD`**: 6 `true` + 2 `false`"; o aviso passou a dizer que na árvore `--listar-nomes` imprime **nove** e o gate local tem **nove** entradas (a nona travada), com "estado versionado = 8/8; estado da árvore = 9/9". |
| B1.2 | `docs/README.md` | 552-556 | "o gate versionado `release/mods.json` (**8** entradas: 6 `true` + **2** `false`)" — sem dizer que é `HEAD`; na árvore são 3 `false` | 1 | "(**8** entradas **em `HEAD`** … e **2** com `publicar: false`; na **árvore de trabalho** de 16/10 o gate local já tem **9**, com a entrada travada do `RealmApi` — preparação, não autoriza envio)". |
| B1.3 | `docs/PUBLICACAO.md` | 9-18 | "`--listar-nomes` e `release/mods.json` têm **8** entradas … a API ainda não é descoberta nem consta do gate" — os dois têm 9 na árvore e o `RealmApi` **consta** (travado) | 1, 5 | "o empacotador **versionado** (`HEAD`) e o gate **em `HEAD`**"; acrescentado o estado da árvore (9 nomes em `--listar-nomes`, 9 entradas no gate local, a nona travada e sem autorizar envio) e que a API segue **fora da Thunderstore** (`HTTP 404`). |
| B1.4 | `docs/PUBLICACAO.md` | 287-290 | "as **duas** entradas travadas … são **as únicas** com `publicar: false` e `versao_publicada: null`" — na árvore são **três** | 1 | "são **2 em `HEAD`** — `BetterPortuguese` e `RoguelikeUnlimitedLevelProgression` — e **3 na árvore de trabalho** de 16/10, onde a entrada de preparação do `RealmApi` já consta". |
| B1.5 | `docs/ESTRUTURA.md` | 7 | "Em 16/10/2026, a descoberta e o gate têm oito nomes" — verdade na versão, falso na árvore | 1 | "a descoberta **versionada** (`HEAD`) e o gate **em `HEAD`** têm oito nomes (a **árvore de trabalho** tem nove: PKG-API-1/PUB-API-2 já ensinam o empacotador e já deixaram no gate local uma entrada travada, de preparação)". |
| B1.6 | `docs/ESTRUTURA.md` | 12 | `api/` "**não** está nos oito nomes … nem no gate de publicação … o gate continua com oito até decisão própria" — a decisão já foi tomada na árvore | 1 | "não está nos oito nomes do empacotador **versionado** nem nas oito entradas do gate **em `HEAD`** (na árvore: nove nomes e uma nona entrada travada; ela **não** autoriza envio e a API segue fora da Thunderstore)". |
| B1.7 | `README.md` | 195-201 | "the versioned packager does not discover that module, and `release/mods.json` does not gate it … the gate stays the authority" — sem o carimbo, e a árvore já tem a entrada | 1 | "`release/mods.json` **at `HEAD`** does not gate it (in the local working tree the packager already recognizes this layout and the local gate already carries a locked `RealmApi` entry — nine names and nine entries there — but that entry is preparation only, **not** authorization to publish: the package is still `HTTP 404` on Thunderstore)". |
| B1.8 | esta entrega | §4 e §6 | "o empacotador **versionado** devolve **8** e o gate `release/mods.json` continua com 8" — a segunda metade sem o qualificador "versionado" | 1 | §4 e §6 agora dizem "o gate **em `HEAD`** tem 8; o gate **da árvore** tem 9". |

**Nada do gate foi reescrito** (`release/mods.json` continua fora da trava desta frente — a entrada do
`RealmApi` é da `PUB-API-2`, não desta revisão) e nenhum manifest/CHANGELOG/código foi tocado.

## 2. Rodada 1 — correções de conteúdo (arquivo | linha final | problema | classe | ação)

> A coluna `linha` é a posição **depois** das correções (as edições deslocam linhas entre si). As
> âncoras de `docs/README.md` e `README.md` foram **remedidas na rodada 4** (ver `A6` e §1B).

### `README.md` (raiz)

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| README.md | 4-6 | "No mod touches the game's content, balance or files" — falso: o repositório tem mod de progressão (RLP) que muda gameplay, além de projetos não publicados | 1 | corrigido: separa mods publicados (QoL) de projetos não publicados |
| README.md | 49 | "BetterCombatText … depends on BetterFont" — falso depois da DEP-REV (16/10): o manifest do BCT declara só `BepInExPack` | 1 | corrigido |
| README.md | 49-52 | tabela de mods listava 4 mods; faltavam BetterCombatText, RSTV, BetterPortuguese e RLP | 1, 5 | linhas acrescentadas, marcando os não publicados |
| README.md | 92-95, 111-114 | "a DLL **não pode** ficar solta em `plugins\`" e "o BepInEx carrega **todo** `.dll`, inclusive `.bak`" — o loader procura `*.dll`; `.dll.disabled`/`.bak`/`.old` não casam | 1 | corrigido (convenção de pasta ≠ exigência; backup fora de `plugins\`) |
| README.md | 153-155 | "Check dependencies first: BetterCombatText requires BetterFont" | 1 | corrigido para a dependência real (RSTV → RealmApi) |
| README.md | 172-173 | troubleshooting mandava a DLL estar em pasta por mod como causa de não carregar | 1 | corrigido |
| README.md | 205-214, 357-366, 632-641 | tabela de identificadores com versões 0.1.1/1.0.1/1.0.2/0.1.1 (reais na rodada 1: 0.1.4/1.0.2/1.0.3/0.1.2) e sem os pacotes novos — **e, na rodada 3, o bump da PUB-ALL-1 desatualizou 3 linhas de novo (A8)** | 1, 2 | corrigidas nas três tabelas; nota de que versão no fonte ≠ ZIP publicado. Linhas remedidas na rodada 4. |
| README.md | 268, 321-325, 694, 748-752 | envio local apresentado como "o mais simples hoje" | 2 | alinhados ao aviso de legado (A5). Linhas remedidas na rodada 4. |

### `STATUS.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| STATUS.md | 11-13 | "o log existente de 16/10/2026 lista 10 plugins" — o cabeçalho do `LogOutput.log` registra a rodada de **12/09/2026 21:34**; a data do arquivo não é a data da sessão | 1 | corrigido (data da leitura + data do cabeçalho) |
| STATUS.md | 16-17 | não dizia que `gh` não existe nesta máquina | 3 | acrescentado |

### `docs/README.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| docs/README.md | 28 | a linha do `img/LEIA-ME.txt` afirmava que o README da raiz usa "notas de captura pendente, sem links para PNG inexistentes" — o README tem **9** links para `docs/img/*.png` sem arquivo | 1, 2 | corrigido para o estado real (9 links quebrados até a captura) |
| docs/README.md | 32-43 | "na raiz, uma pasta por mod … (e `RoguelikeBalance`, que ainda não virou mod)" — hoje a descoberta tem **8** nomes e `RoguelikeBalance` não existe na árvore | 1 | corrigido |
| docs/README.md | 32-43 | nada dizia que a API existe em `api/` e é consumida pelo RSTV | 5 | acrescentado (com o limite: não é descoberta pelo empacotador versionado) |
| docs/README.md | 240-243 | bloco bash usava `%APPDATA%` — no Git Bash é sintaxe de cmd.exe e **não expande** | 3 | trocado por `cygpath -u "$APPDATA"` (comando executado). Linha remedida na rodada 4. |
| docs/README.md | 246-250 | "DLL solta em `plugins/` não carrega" | 1 | corrigido. Linhas remedidas na rodada 4. |
| docs/README.md | 401-412 | tabela "Os 6 mods" com versões e estado de publicação de 01/10 (BCT 0.1.1 "não publicado", RSTV 0.3.2, etc.) | 1 | reescrita: 8 descobertos, 6 publicados em 07/10/2026 (+ nota da PUB-ALL-1 em 420-422). Linhas remedidas na rodada 4. |
| docs/README.md | 416-419 | "conferido contra a API pública em 01/10/2026" | 1 | reconferido por endpoint em 16/10/2026 |
| docs/README.md | 447 | dependência declarada como `BetterCombatText 0.1.1 → BetterFont 1.0.2`; o estado real é `RSTV → RealmApi-0.1.0` (não resolvível) | 1, 2 | reescrito |
| docs/README.md | 387, 484-489, 552-556, 566-570 | linha de ferramenta + bloco bash do envio local + contagem do gate | 1, 2 | A5 e A3 (a contagem do gate ganhou o carimbo `HEAD` × árvore em `B1.2`). Linhas remedidas na rodada 4. |

### `docs/AMBIENTE.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| AMBIENTE.md | 28 | "Plugins que carregam no perfil `Default` (**8**)" e "log de 16/10/2026" — o log lido tem **10** plugins e o cabeçalho é de 12/09 | 1 | corrigido (10; `LogOutput.log` lido em 16/10) |
| AMBIENTE.md | 38, 41, 44 | dependência do BCT (removida) e versões carregadas desatualizadas (Better Combat Text 0.1.1, RSTV 0.2.0, Better Tooltips 0.1.1) | 1, 2 | corrigidas pelo log real (+ CAP-1 Probe, RLP 0.1.1); linha 38 na rodada 3 (A4) |
| AMBIENTE.md | 106-111 | "nenhum mod depende da ModAPI … o ciclo fecha com 6 plugins e zero erro" apresentado como estado atual | 1 | marcado como rodada histórica + distinção da RealmApi própria |
| AMBIENTE.md | 149-168 | checklist com `%APPDATA%` e `find` sobre caminho não expandido — não roda no Git Bash | 3 | reescrito em `$APPDATA`/Python e **executado** (rc=0) |

### `docs/ESTRUTURA.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| ESTRUTURA.md | 7 | "6 mods liberados + `RoguelikeUnlimitedLevelProgression` bloqueado" — hoje são 6 `publicar:true` + **dois** bloqueados (`BetterPortuguese 0.1.0` e RLP 0.1.1) | 1 | corrigido |
| ESTRUTURA.md | 12 | `api/` descrita como "módulo separado" sem dizer que não entra nos 8 nomes nem no gate | 1, 5 | corrigido |
| ESTRUTURA.md | 79 | "clone sem `lib/` falha no `ValidateCommonLibDir` com `LEVEL-LIB`, exigindo `-p:CommonLibDir`" como regra geral — só RLP (`LEVEL-LIB`) e BetterPortuguese (`BP-LIB`) têm esse alvo; os 6 antigos usam HintPath `..\lib\` | 1 | corrigido (conferido nos `.csproj`) |

### `docs/CI.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| CI.md | 25-31 | "**Não empacota.** O `pack-thunderstore.py` … fica fora" — o `validate.yml` tem passo do empacotador, guardado por presença de DLL Release | 1 | corrigido |
| CI.md | 30-31 | "o workflow é a mesma trava do `tools/release-check.sh`" — não é o mesmo conjunto (o release-check também compila) | 1, 2 | corrigido |
| CI.md | 84-86 | envio local "continua valendo como caminho alternativo" | 2 | A5: rebaixado a **legado** |
| CI.md | 93-106 | tabela de passos desatualizada: faltavam `check_versoes`, `check_patches`, `cobertura_ui_localized --prova` e o passo do empacotador; `checa_citacoes.py` era citado como passo 10 **do YAML**, onde ele não está | 1, 3 | reescrita contra o `validate.yml` real (conferido passo a passo) |
| CI.md | 137-170 | mandava colar um bloco no `validate.yml` "num PAT com escopo `workflow`" como instrução corrente | 3 | rebaixado a proposta histórica, sem diagnóstico de credencial |

### `docs/PUBLICACAO.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| PUBLICACAO.md | 9-21 | "o projeto tem 6 mods e os SEIS estão publicados … `release/mods.json` com as 6 entradas" como estado de hoje | 1 | corrigido (8 entradas, 6 publicadas em 07/10) + foto de 01/10 preservada |
| PUBLICACAO.md | 57-58, 64 | adendo de 12/10 dizendo "7 entradas" / "7 nomes" | 2 | A10 |
| PUBLICACAO.md | 105-106 | "Hoje o repo **não tem** LICENSE e **nenhum** README/manifest menciona licença" — `api/LICENSE` é MIT e o README da API declara isso | 1 | corrigido (licença do módulo ≠ licença dos demais mods) |
| PUBLICACAO.md | 241-243, 266-274 | "caso de hoje" com o par BCT→BetterFont, e o exemplo acima afirmando o mesmo par removido | 1, 2 | A1 |
| PUBLICACAO.md | 283-286 | amostra JSON do gate mentindo sobre o arquivo real | 1 | A2 |
| PUBLICACAO.md | 345-353 | os dois `gh release create` do documento sem avisar que `gh` **não está instalado** nesta máquina | 3 | aviso acrescentado (`which gh` → nada, 16/10/2026) |
| PUBLICACAO.md | 389-400, 588 | `tools/publish-thunderstore.sh` recomendado como caminho de envio | 1, 3 | A5 (declarado legado e não seguro; script não foi executado) |

### `docs/SUPERVISAO.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| SUPERVISAO.md | 50 | "**Toda tarefa executada exige uma tarefa de revisão**" — contradiz o fluxo real (revisão no mesmo cartão ou filho preexistente) | 2 | corrigido + ponteiro para `PROCESSO-REVISAO.md` |
| SUPERVISAO.md | 136 | "Nunca `dotnet build -c Release` sem `-p:DeployToBepInEx=false`: sem a flag o alvo **copia a DLL** para o perfil" — desde DEPLOY-2 o deploy é opt-in | 1 | corrigido (`Directory.Build.props:24`) |
| SUPERVISAO.md | 191-194 | "subagente não consegue criar tarefa no Kanban" (impreciso: é o subagente de `delegate_task`; worker do dispatcher usa `kanban_*`) | 1 | corrigido |

### `docs/PROCESSO-REVISAO.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| PROCESSO-REVISAO.md | 3 | "toda tarefa … gera uma tarefa de revisão independente", contradizendo a mecânica do kanban (`request_review` no mesmo cartão / filho preexistente) | 2 | corrigido |
| PROCESSO-REVISAO.md | 31-33 | invariante "BetterCombatText → BetterFont no manifest" | 1 | corrigido |
| PROCESSO-REVISAO.md | 51-57 | formato da tarefa de revisão (título `REV-<n>` + cartão novo) contradizia o processo de mesmo cartão | 2 | corrigido e preservado como opção para revisão separada já no grafo |

### `docs/PLANO-DE-TESTES.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| PLANO-DE-TESTES.md | 14-17 | "podem rodar em CI quando o `lib/` estiver disponível lá" — contradiz `docs/CI.md` (o CI não usa `lib/`) | 2 | corrigido |
| PLANO-DE-TESTES.md | 35 | invariante 3 com a dependência BCT→BetterFont | 1 | corrigido |

### `docs/MODS-PARA-AMIGOS.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| MODS-PARA-AMIGOS.md | 102-108 | "Todo mod referencia `..\lib\` — nenhum mod depende da pasta de outro" e o zip "de uma DLL por mod" apresentado como distribuição suficiente | 1, 5 | corrigido: RSTV atual referencia `api/` em Release e não é distribuível por esse zip |
| MODS-PARA-AMIGOS.md | 115-117 | "`DeployToBepInEx=false` é **obrigatória**, senão o build sobrescreve a DLL instalada" | 1 | corrigido (opt-in desde DEPLOY-2) |

### `docs/DEBUGGER.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| DEBUGGER.md | 19-25 | "9 categorias … São **9 arquivos** de gancho" — hoje são 13 categorias + `[Efeitos]` + carimbo `[Proveniencia]` e **10** arquivos `.cs` (conferido no fonte) | 1 | corrigido |
| DEBUGGER.md | 55-58 | medições de 01/10 apresentadas como estado atual | 1 | marcadas como fotografia histórica |
| DEBUGGER.md | 99-106 | mandava conferir o decompilado cacheado `%LOCALAPPDATA%\hermes\cache\scratch\cs\Assembly-CSharp.decompiled.cs`, que **não existe** mais | 1, 3 | corrigido: regerar com `ilspycmd lib/Assembly-CSharp.dll` (o CLI está instalado, conferido) |
| DEBUGGER.md | 212-216 | "o ciclo é `dotnet build` (que copia para o perfil)" | 1 | corrigido para `-p:DeployToBepInEx=true` |

### `docs/DBG-PROVENIENCIA.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| DBG-PROVENIENCIA.md | 53 | veredito `COMPLETO` "**só este libera** ler ausência de dado como ausência de fato" — o carimbo não cobre presets de inimigo nem localização (também não cobre categorias de combate dependentes de caminho) | 1 | corrigido para o alcance real |
| DBG-PROVENIENCIA.md | 57-61 | "avisos **não** mudam o veredito" como regra geral — identidade incompleta produz `TRUNCADO`; só `modoLeitura=ativo` é nota informativa | 1 | corrigido |

## 3. Revisado sem alteração

| arquivo | por quê |
|---|---|
| `api/docs/README.md` | 21 linhas, atual: os dois comandos citados existem (`api/tools/Inspect/Inspect.csproj`, `api/tools/check_ui_contract.py`) e o texto já declara o limite "runtime NÃO_EXERCITADO". Nada factual a corrigir. |
| `STATUS.md` | **Não versionado por desenho** (`.gitignore:18-21`: `*.md` na raiz fica fora do git, exceto `README.md`). É nota de trabalho local: as correções desta frente existem em disco e **não** entram em commit. |
| `ITEM_INVENTORY.md`, `ITEM_MOD_INVENTORY.md`, `STATUS_INVENTORY.md`, `SKILL_INVENTORY.md`, `TOOLTIP_SWEEP.md` | Inventários/dumps da raiz, **também ignorados pelo git por decisão explícita** (mesmo bloco do `.gitignore`). Totais conferidos programaticamente e **batem** com os títulos: 905 itens (60+118+98+66+83+81+62+33+3+301), 285 afixos, 600 status (497/83/14/6), 453 skills (somas por classe conferidas). Nada factual a corrigir; nenhum arquivo foi tocado. |
| `TOOLTIP_SWEEP.md` | Declara "patch notes mais recentes: v1.3.1, 15/09/2026". Confirmado: o v1.3.1 é a última nota de patch (a novidade mais recente no Steam News é "Stolen Realm 2 Announced", 01/10/2026, que não é patch). |
| `api/README.md` | **Revisado, não commitado**: já estava modificado por outra frente quando esta tarefa começou (`hotspot` registrado em comentário no cartão). O diff preexistente não foi incluído em nenhum commit desta frente (ver §6). |

## 4. Provas coletadas (comandos reais, 16/10/2026)

| comando | resultado |
|---|---|
| `python tools/pack-thunderstore.py --listar-nomes` | **9** nomes na árvore de trabalho (com `RealmApi`, frentes PKG-API-1/PUB-API-2 não commitadas); o empacotador **versionado** devolve **8**, o gate `release/mods.json` **em `HEAD`** tem **8** entradas e o gate **da árvore** tem **9**. Ver §6. |
| `python tools/check_versoes.py` | exit 0; na árvore de trabalho cobre **9** pacotes (inclui `api`/`RealmApi`) e reporta os quatro lugares alinhados — `0.1.3 / 1.0.3 / 0.1.0 / 1.0.2 / 0.1.4 / 0.1.3 / 0.3.4 / 0.1.1 / api 0.1.0`. O arquivo está sob edição de outra frente (sem commit). |
| `python tools/check_dependencias.py --local` | exit 1: `FALHA RoguelikeSkillTreeVisualizer: depende de DefRuivo_StolenRealmMods-RealmApi-0.1.0, que NAO existe na Thunderstore` — o upload do RSTV seria recusado hoje |
| API por pacote (`/api/experimental/package/DefRuivo_StolenRealmMods/<nome>/`) | HTTP **200** para os 6 publicados — `BetterCombatText 0.1.2`, `BetterFont 1.0.3`, `BetterStats 1.0.2`, `BetterTooltips 0.1.4`, `RoguelikeDebugger 0.1.2`, `RSTV 0.3.3`; HTTP **404** para `BetterPortuguese`, `RoguelikeUnlimitedLevelProgression` e `RealmApi` |
| `python tools/audita_docs.py` (antes e depois das edições) | **as mesmas 4 pendências** nas duas execuções — nenhuma introduzida por esta frente (ver §5) |
| `which gh` | vazio — **`gh` não está instalado nesta máquina** |
| `ls LICENSE` (raiz) | não existe; `api/LICENSE` = MIT (Copyright 2026 Gumatos) |
| `ls RoguelikeDebugger/Patches/*.cs` | 10 arquivos; tags no fonte: `[Status] [Action] [Skill] [Item] [ItemMod] [Powerup] [Loot] [Event] [LifeSteal] [Dmg] [Gold] [Exp] [ExpInimigo] [Efeitos] [Proveniencia]` |
| `grep BepInDependency RoguelikeSkillTreeVisualizer/Plugin.cs` | `[BepInDependency(ApiGuid, ApiVersionMinima)]` — hard, mínimo 0.1.0 |
| `git diff --check` nos arquivos desta frente | sem erro (só o aviso LF/CRLF do git no Windows) |
| `git check-ignore -v STATUS.md` | `.gitignore:20:*.md` — `STATUS.md` e os cinco inventários da raiz **não são versionados** |
| Links relativos dos 12 documentos vivos editados | **105 links, 9 quebrados**, todos `docs/img/*.png` no `README.md`, nas linhas **394, 404, 410, 415, 444, 458, 464, 541, 551** (carimbado na rodada 4, 16/10/2026; medido com o mesmo script sobre `HEAD:arquivo` e sobre a árvore — deu **105/9 nos dois**, então as edições desta frente não criaram nem removeram link; a contagem antiga de "103" estava com escopo/regex diferente) |
| `git show HEAD:tools/publish-thunderstore.sh` | confirmado: laço `for z in dist/gumatos-*.zip` e header de autorização literal — a base do texto "legado" |
| `git log --format='%h %ci %s' -3` | `39852b7 2026-10-16 13:58:21 PUB-ALL-1 …` e `844bba8 2026-10-16 13:49:58 DOC-REV …` — a base do A8 |

## 5. O que PRECISA DE DECISÃO DO DONO

1. **9 capturas pendentes (classe 4).** `README.md` linhas **394, 404, 410, 415, 444, 458, 464, 541, 551**
   apontam para `docs/img/*.png` que não existem (a pasta tem só `LEIA-ME.txt` e dois PNG de fonte de
   ícone, sem nenhuma captura de uso). O próprio `docs/img/LEIA-ME.txt` declara esse estado como
   pendente, então **não apaguei nem converti em nota**: decidir entre tirar as 9 capturas (nomes já
   especificados no `LEIA-ME.txt`) ou remover os links.
2. **`tools/audita_docs.py` está reprovando o repositório correto.** A regra `DEP_EXTRAS`
   (linhas 360-369) exige `BetterCombatText → BetterFont` no manifest. Depois da DEP-REV isso é
   falso permanente: o auditor acusa "dependencia do Thunderstore fora do padrao" e não reconhece
   `RSTV → RealmApi`. O próprio script pede ("Falso positivo de regra: ajuste a regra AQUI"). **Não editei
   `tools/`** (fora do escopo documental) — precisa de tarefa própria.
3. **`release/mods.json` contradiz a documentação corrigida.** Os campos `motivo` e
   `ordem_de_envio.caso_de_hoje` ainda falam de `BetterCombatText 0.1.1` → `BetterFont 1.0.2` (leva de
   01/10/2026). O **registro** do `RealmApi` existe na **árvore** desde 16/10 (entrada `publicar: false`
   da `PUB-API-2`, ver `B1`), mas **em `HEAD` não existe** — foi exatamente o que gerou o achado `B1`:
   a doc tem de dizer de qual dos dois estados está falando. Não editei o gate (é frente própria; a
   DEP-REV §8.3 também apontou o texto velho). A doc agora diz isso de forma explícita (A1 e §1B), em
   vez de repetir o texto velho.
4. **`api/manifest.json` é novo e não versionado**, e o `audita_docs` o reprova com "api: versao diverge
   entre manifest/csproj/plugin" — falso positivo de layout: o auditor procura `<Mod>/<Mod>.csproj` e
   `<Mod>/Plugin.cs` na raiz da pasta, e a API tem `api/Plugin/RealmApi.csproj`. O `check_versoes.py`
   (em edição por outra frente) já entende o layout. Decidir se o auditor e o empacotador passam a
   entender o layout da API (mesmo bloqueio do item 2 da DEP-REV §8).
5. **`api/README.md` tem diff preexistente de outra frente** (preparação do pacote RealmApi) — não entrou
   em commit desta frente. Se aquele texto contiver afirmação falsa, a correção é da frente dona.
6. **`docs/BETTERPORTUGUESE-ARQUITETURA.md:37,286`** cita `evidence/audit_sources.py`, que não existe no
   repositório (é ferramenta de workspace). É a quarta pendência do auditor. O arquivo **não está na lista
   do cartão** — reportado em vez de editado.
7. **`BetterCombatText/README.md:9,43-49`** ainda declara a dependência de BetterFont — resíduo apontado
   pela própria DEP-REV, com a filha `t_d00f2bc6` (PUB-ALL-1) encarregada de alinhar. Fora da minha trava
   (é README de mod).
8. **PUB-ALL-1 bumpou 3 mods sem publicar** (`BetterCombatText 0.1.3`, `RoguelikeDebugger 0.1.3`,
   `RSTV 0.3.4`): a doc agora diz explicitamente que a versão no disco está à frente da publicada
   (`docs/README.md:420-422`). Quando o lote sair, essas tabelas precisam de nova passada — é o mesmo
   risco de deriva do A8.
9. **Fotografias datadas mantidas de propósito:** `docs/README.md:425-434` (adendo de 12/10),
   `docs/README.md:470-475` (aviso de cache da API, 30/09), `docs/README.md:437-452` (bloco "6 mods,
   01/10/2026") e `README.md:698` ("empacotador conhece 6 mods, medido em 30/09/2026"). São verdadeiras
   para a data declarada e ficam ao lado do estado corrente; decidir se vale carimbá-las mais
   explicitamente como foto.
10. **`tools/publish-thunderstore.sh`** (envio local) não lê o gate, envia todos os `dist/gumatos-*.zip`
    e usa o header de autorização sem a variável `TOKEN` lida no início. Há frente em andamento
    (PKG-API-1, **não commitada** em 16/10) que faz o script ler o ledger. A doc diz para **não** usar
    como caminho seguro até essa frente estar commitada e provada; testar/corrigir o script é tarefa própria.
    Pelo mesmo motivo, **`release/mods.json` está `M` na árvore** (nona entrada, `RealmApi`, da
    `PUB-API-2`, não commitada) — decidir o que fazer com o carimbo `HEAD` × árvore quando a entrada
    subir de verdade, e se o `motivo`/`ordem_de_envio.caso_de_hoje` do gate (item 3) serão regerados.
11. **Seis arquivos do escopo não são versionados** (`.gitignore:18-21`): `STATUS.md` e os cinco
    inventários da raiz. O cartão os trata como "documentação viva", mas quem clona o repositório não os
    recebe — as correções desta frente em `STATUS.md` valem só nesta máquina. Decidir se esse é o desenho
    desejado (nota local) ou se algum deles deve passar a versionado.

## 6. Colisões e trabalho em andamento (hotspot)

Quatro arquivos de `tools/`/CI **já estavam sendo alterados por outra frente** (PKG-API-1: ensina o
empacotador a reconhecer o layout aninhado da RealmApi) quando esta revisão começou:
`tools/pack-thunderstore.py` (+352 linhas), `tools/publish-thunderstore.sh` (+155),
`tools/check_versoes.py` (+7) e `.github/workflows/publish.yml` (+100). Nenhum deles está commitado.
Na árvore de trabalho, `python tools/pack-thunderstore.py --listar-nomes` já devolve **9** nomes (com
`RealmApi`), enquanto o empacotador versionado devolve 8.

**`release/mods.json` entra nesta lista na rodada 4** (o achado `B1` nasceu justamente porque ele não
estava aqui): está `M` na árvore desde as 14:06 de 16/10, com a nona entrada (`RealmApi`,
`publicar: false`) acrescentada pela `PUB-API-2`. Portanto: gate **em `HEAD`** = **8** entradas
(6 `true` + 2 `false`); gate **da árvore** = **9** (6 `true` + 3 `false`); `--listar-nomes` **da árvore**
= **9** (bate com o gate da árvore). O gate **não** foi reescrito por esta revisão.

Por isso as linhas de documentação que falam do empacotador/gate foram escritas para o **estado
versionado** com o carimbo explícito do referente e a nota da frente em andamento — nenhuma afirmação
depende de código não commitado:

- `README.md:195-201` ("the versioned packager does not discover that module… `at HEAD` does not gate it");
- `docs/README.md:32-43` (o parágrafo dos 8 nomes + o aviso da árvore de trabalho: 9/9);
- `docs/README.md:552-556` (a contagem do gate);
- `docs/ESTRUTURA.md:7` e `:12` (a descoberta e o gate; linha do `api/` no layout canônico);
- `docs/PUBLICACAO.md:9-18` e `:287-290` (estado conferido e travas do gate);
- `docs/PUBLICACAO.md:389-400` (envio local legado);
- `docs/README.md:387` (a linha do `publish-thunderstore.sh` na tabela de ferramentas).

**Quando a PKG-API-1 e a PUB-API-2 forem commitadas, revisar essas passagens** — o número "8" e a frase
"não é descoberta pelo empacotador" passam a valer só para `HEAD`, e o carimbo pode voltar a ser um
número único. Hotspot declarado em comentário no cartão.

## 7. Travas respeitadas

- Nada de código de mod, manifest, CHANGELOG, ícone ou `.csproj` foi editado.
- `git add -A` não foi usado: os commits desta frente listam caminho explícito de arquivo.
- `docs/automacao/**` (fora deste arquivo de entrega) e `docs/cobertura/**` não foram revisados nem tocados.
- Não houve build, deploy, ciclo de jogo, publicação, push de release nem criação de tarefa.
- Alterações de outras frentes encontradas no checkout (manifests, CHANGELOGs, ícones, código do RLP,
  `api/*`, `tools/*`, `.github/*`, `release/mods.json` — a nona entrada do `RealmApi`, da `PUB-API-2` —,
  relatórios históricos, `harness-out/`, `kanban.db`,
  `tools/preparar_revisao_dono.py`) foram preservadas intactas e ficaram fora do stage.
