# DOC-REV — revisão da documentação viva

Cartão: `t_d9d74e4d`. Data: 16/10/2026 (Hora oficial do Brasil, UTC-03:00). Repositório: `C:/dev/stolen-realm`.
Nenhum jogo foi aberto, nenhum build/deploy foi rodado, nenhuma publicação foi feita, nenhum
manifest/CHANGELOG de mod foi editado e nada de `docs/automacao/**` ou `docs/cobertura/**` foi revisado
(este arquivo de entrega é a única exceção).

**Rodadas.** Rodada 1 (implementação, commit `844bba8`) revisou os 20 documentos do escopo e corrigiu 11.
Rodada 2 (revisão independente, run 1603) pediu mudanças: 5 afirmações falsas/contraditórias que
escaparam (`A1`–`A5`), âncoras de linha erradas nesta entrega (`A6`) e contagens desatualizadas (`A7`).
Rodada 3 (esta, run 1605) fechou `A1`–`A7` e as derivações encontradas durante o fechamento (`A8`–`A10`).

## 0. Cobertura

- **Arquivos do escopo revisados: 20 de 20** (a lista nominal do cartão) — 20 existem, 20 lidos.
  `README.md`, `STATUS.md`; `docs/README.md`, `AMBIENTE.md`, `ESTRUTURA.md`, `CI.md`, `PUBLICACAO.md`,
  `SUPERVISAO.md`, `PROCESSO-REVISAO.md`, `PLANO-DE-TESTES.md`, `MODS-PARA-AMIGOS.md`, `DEBUGGER.md`,
  `DBG-PROVENIENCIA.md`; `api/README.md`, `api/docs/README.md`; `ITEM_INVENTORY.md`,
  `ITEM_MOD_INVENTORY.md`, `STATUS_INVENTORY.md`, `SKILL_INVENTORY.md`, `TOOLTIP_SWEEP.md`.
- Contexto do repositório, medido em **16/10/2026 14:2x**, no commit `39852b7` + árvore de trabalho:
  **672 arquivos `.md` versionados** (`git ls-files '*.md'`), **956 arquivos versionados em
  `docs/automacao/`** (arquivo histórico, fora do escopo) e **135 arquivos `.md`/`.json`/`.txt`
  versionados fora de `automacao/`+`cobertura/`.
  A contagem **anda sozinha**: as frentes paralelas commitam relatórios em `docs/automacao/` durante o
  dia (670 → 671 → 672 `.md` ao longo desta tarefa, e 950 → 951 → 956 arquivos em `automacao/`).
  O número acima é a medida no commit `39852b7`; quem reconferir depois verá outro valor sem que nada
  tenha ficado errado.
- Dos 20 do escopo, **11 exigiam correção** e foram corrigidos; 9 não tinham problema factual.
- Revisão anterior deste cartão morreu por *rate limit* (run 1593) deixando as edições em disco, sem
  commit e sem entrega; elas foram relidas e reverificadas nas rodadas seguintes.

Legenda de classe: **1** afirmação falsa sobre o estado atual · **2** contradição entre documentos ·
**3** instrução que não funciona · **4** link quebrado interno · **5** falta de informação essencial.

## 1. Rodada 3 — fechamento das mudanças pedidas pela revisão independente

| item | arquivo | linha (estado final) | problema | classe | o que foi feito |
|---|---|---|---|---|---|
| A1 | `docs/PUBLICACAO.md` | 236-238 e **261-269** | "O caso de hoje: o `BetterCombatText 0.1.1` depende do **`BetterFont 1.0.2`**, que ainda **não está no ar** (a última publicada é a `1.0.1`)" — falso: o manifest do BCT declara **só** `BepInEx-BepInExPack-5.4.2305` desde 16/10 (DEP-REV) e o `BetterFont` no ar é **1.0.3** (07/10) | 1, 2 | reescrito: "O caso de hoje (16/10/2026) **não é** o desse exemplo…" — nenhum mod declara dependência de pacote a outro mod de jogo; a **única** dependência real é `RoguelikeSkillTreeVisualizer 0.3.4 → RealmApi-0.1.0`, que **não resolve** (404 na API) e faz o `check_dependencias.py --local` reprovar; o `ordem_de_envio.caso_de_hoje` do gate fica declarado como fotografia de 01/10 (frente própria). O exemplo acima (236-238) passou a ser **condicional** ("Se um mod declara… `BetterFont-1.0.2`") em vez de citar o par que não existe mais. |
| A2 | `docs/PUBLICACAO.md` | **278-284** | o bloco `json` apresentado como "o `release/mods.json` é o substituto versionado" mostrava `BetterFont: publicar:false, versao_publicada:null` — o real é `publicar:true`, `"1.0.3"`, `publicado_em 2026-10-07T21:24:48.179123Z` | 1 | substituído por **trecho real** do arquivo (com o `motivo` abreviado) + nota de que as duas travas (`BetterPortuguese`, RLP) são as **únicas** com `publicar:false`/`null`. |
| A3 | `docs/README.md` | **552-555** | "quem **pode** sair é o gate versionado `release/mods.json` (**6** entradas, todas com `publicar: true`)" — o gate tem **8** entradas: 6 `true` + 2 `false` (`BetterPortuguese`, `RoguelikeUnlimitedLevelProgression`) | 1, 2 | corrigido para "**8** entradas: **6** com `publicar: true` … e **2** com `publicar: false`, `BetterPortuguese` e `RoguelikeUnlimitedLevelProgression`"; o mesmo arquivo já dizia 8 nas linhas 32-43. |
| A4 | `docs/AMBIENTE.md` | **38** | `Better Combat Text 0.1.1 | projeto (depende do Better Font)` — quinta ocorrência da dependência já removida | 1, 2 | virou "o **par carregado** no perfil é BCT + `Better Font`; o manifest corrente do BCT **não** declara dependência de pacote — foi removida em 16/10/2026 (DEP-REV)". A tabela descreve **o que o log carregou** (rodada de 12/09), não o manifest de hoje. |
| A5 | `docs/README.md` **383**, **480-486**, **562-565**; `README.md` **266**, **319-323**, **692**, **746-750**; `docs/CI.md` **84-86**; `docs/PUBLICACAO.md` **582** | — | `tools/publish-thunderstore.sh --go` apresentado como caminho de publicação/empacotamento ("o mais simples hoje", "continua valendo como caminho alternativo"), contradizendo `docs/PUBLICACAO.md` §4 (envio **legado**, não lê o gate, itera todos os `dist/gumatos-*.zip`, header de auth sem a variável `TOKEN`) | 2 | os sete pontos foram alinhados à mesma trava e ao mesmo aviso: **legado, não é caminho seguro**, não lê o gate, sem aprovação humana, sobe todos os `dist/gumatos-*.zip`; o caminho de hoje é o `publish.yml`. Conferido em `git show HEAD:tools/publish-thunderstore.sh` (laço `for z in dist/gumatos-*.zip`; header de autorização literal, sem a variável `TOKEN`). |
| A6 | esta entrega | §4 e §5 | a coluna "linha" tinha âncoras erradas: PNG do README em 388…545 (eram 390…547) e `docs/README.md` 393-404/407-411/435 (eram 397-407/412-417/439) | 4 | todas as âncoras foram **remedidas com `grep -n`** depois das edições desta rodada; as do README dos PNGs mudaram para **392,402,408,413,442,456,462,539,549** porque as próprias correções de `A5` somaram 2 linhas acima delas (ver §4 e §5 item 1). |
| A7 | esta entrega | §0 | contagens "670 `.md` versionados / 950 em `docs/automacao/`" contra 671/951 medidos pelo revisor | 1 | remedidas e **carimbadas** (672 / 956 em 16/10/2026, commit `39852b7`) com a explicação de que a contagem cresce a cada commit das frentes paralelas. |

### Derivações encontradas ao fechar A1–A7 (não estavam na revisão)

| item | arquivo | linha | problema | classe | o que foi feito |
|---|---|---|---|---|---|
| A8 | `README.md` (3 tabelas), `docs/README.md` | 208-210, 360-362, 635-637; 401/406/407, 416-418, 443 | **deriva do dia**: o commit `39852b7` (PUB-ALL-1, 13:58) bumpou `BetterCombatText 0.1.2→0.1.3`, `RoguelikeDebugger 0.1.2→0.1.3` e `RSTV 0.3.3→0.3.4` nos quatro lugares — **depois** do commit da rodada 1 (13:49) e depois da revisão independente. Toda "versão no fonte/disco" das docs passou a mentir por um bump; a dependência do RSTV também era citada como `0.3.3` | 1 | tabelas do README atualizadas para 0.1.3/0.1.3/0.3.4; tabela dos 8 mods descobertos atualizada na coluna "Versão no disco"; linha de `dependencies` para `RoguelikeSkillTreeVisualizer 0.3.4`; acrescentado o parágrafo 416-418 declarando que a versão no disco está **à frente** da publicada (nada foi publicado nesse bump). Conferido contra `*/manifest.json`, `python tools/check_versoes.py` (exit 0) e a API. |
| A9 | `docs/README.md` | 421-430 | o adendo datado de 12/10 ("o projeto tem um **sétimo** pacote descoberto", "conjunto esperado pelo workflow passa a ser **7** nomes", "a tabela acima (6 mods)") contradizia a tabela de **8** mods descobertos (16/10) logo acima | 2 | adendo mantido como fotografia datada, com o estado corrente ao lado: "7 nomes então; **8** desde 16/10/2026, com o `BetterPortuguese`", e a frase final reescrita para não alegar que a tabela de cima tem 6 mods. |
| A10 | `docs/PUBLICACAO.md` | 52-53, 57-58 | o adendo de 12/10 dizia "o `release/mods.json` tem **7** entradas" e "o conjunto esperado … (7 nomes)", contra as **8** do cabeçalho do mesmo arquivo (linha 9) | 2 | "passou a ter 7 entradas (oito desde 16/10/2026, com o `BetterPortuguese`)" e "(7 nomes então; **8** desde 16/10/2026 …)". |

## 2. Rodada 1 — correções de conteúdo (arquivo | linha final | problema | classe | ação)

> A coluna `linha` é a posição **depois** das correções (as edições deslocam linhas entre si).

### `README.md` (raiz)

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| README.md | 4-6 | "No mod touches the game's content, balance or files" — falso: o repositório tem mod de progressão (RLP) que muda gameplay, além de projetos não publicados | 1 | corrigido: separa mods publicados (QoL) de projetos não publicados |
| README.md | 49 | "BetterCombatText … depends on BetterFont" — falso depois da DEP-REV (16/10): o manifest do BCT declara só `BepInExPack` | 1 | corrigido |
| README.md | 49-52 | tabela de mods listava 4 mods; faltavam BetterCombatText, RSTV, BetterPortuguese e RLP | 1, 5 | linhas acrescentadas, marcando os não publicados |
| README.md | 92-95, 111-114 | "a DLL **não pode** ficar solta em `plugins\`" e "o BepInEx carrega **todo** `.dll`, inclusive `.bak`" — o loader procura `*.dll`; `.dll.disabled`/`.bak`/`.old` não casam | 1 | corrigido (convenção de pasta ≠ exigência; backup fora de `plugins\`) |
| README.md | 153-155 | "Check dependencies first: BetterCombatText requires BetterFont" | 1 | corrigido para a dependência real (RSTV → RealmApi) |
| README.md | 172-173 | troubleshooting mandava a DLL estar em pasta por mod como causa de não carregar | 1 | corrigido |
| README.md | 203-212, 355-364, 630-639 | tabela de identificadores com versões 0.1.1/1.0.1/1.0.2/0.1.1 (reais na rodada 1: 0.1.4/1.0.2/1.0.3/0.1.2) e sem os pacotes novos — **e, na rodada 3, o bump da PUB-ALL-1 desatualizou 3 linhas de novo (A8)** | 1, 2 | corrigidas nas três tabelas; nota de que versão no fonte ≠ ZIP publicado |
| README.md | 266, 319-323, 692, 746-750 | envio local apresentado como "o mais simples hoje" | 2 | alinhados ao aviso de legado (A5) |

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
| docs/README.md | 235-237 | bloco bash usava `%APPDATA%` — no Git Bash é sintaxe de cmd.exe e **não expande** | 3 | trocado por `cygpath -u "$APPDATA"` (comando executado) |
| docs/README.md | 238-242 | "DLL solta em `plugins/` não carrega" | 1 | corrigido |
| docs/README.md | 397-408 | tabela "Os 6 mods" com versões e estado de publicação de 01/10 (BCT 0.1.1 "não publicado", RSTV 0.3.2, etc.) | 1 | reescrita: 8 descobertos, 6 publicados em 07/10/2026 (+ nota da PUB-ALL-1 em 416-418) |
| docs/README.md | 412-415 | "conferido contra a API pública em 01/10/2026" | 1 | reconferido por endpoint em 16/10/2026 |
| docs/README.md | 443 | dependência declarada como `BetterCombatText 0.1.1 → BetterFont 1.0.2`; o estado real é `RSTV → RealmApi-0.1.0` (não resolvível) | 1, 2 | reescrito |
| docs/README.md | 383, 480-486, 552-555, 562-565 | linha de ferramenta + bloco bash do envio local + contagem do gate | 1, 2 | A5 e A3 |

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
| PUBLICACAO.md | 9-18 | "o projeto tem 6 mods e os SEIS estão publicados … `release/mods.json` com as 6 entradas" como estado de hoje | 1 | corrigido (8 entradas, 6 publicadas em 07/10) + foto de 01/10 preservada |
| PUBLICACAO.md | 52-53, 57-58 | adendo de 12/10 dizendo "7 entradas" / "7 nomes" | 2 | A10 |
| PUBLICACAO.md | 100-101 | "Hoje o repo **não tem** LICENSE e **nenhum** README/manifest menciona licença" — `api/LICENSE` é MIT e o README da API declara isso | 1 | corrigido (licença do módulo ≠ licença dos demais mods) |
| PUBLICACAO.md | 236-238, 261-269 | "caso de hoje" com o par BCT→BetterFont, e o exemplo acima afirmando o mesmo par removido | 1, 2 | A1 |
| PUBLICACAO.md | 278-284 | amostra JSON do gate mentindo sobre o arquivo real | 1 | A2 |
| PUBLICACAO.md | 340-348 | os dois `gh release create` do documento sem avisar que `gh` **não está instalado** nesta máquina | 3 | aviso acrescentado (`which gh` → nada, 16/10/2026) |
| PUBLICACAO.md | 383-394, 582 | `tools/publish-thunderstore.sh` recomendado como caminho de envio | 1, 3 | A5 (declarado legado e não seguro; script não foi executado) |

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
| `python tools/pack-thunderstore.py --listar-nomes` | **9** nomes na árvore de trabalho (com `RealmApi`, frente PKG-API-1 não commitada); o empacotador **versionado** devolve **8** e o gate `release/mods.json` continua com 8. Ver §6. |
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
| Links relativos dos 12 documentos vivos editados | **103 links, 9 quebrados**, todos `docs/img/*.png` no `README.md`, nas linhas **392, 402, 408, 413, 442, 456, 462, 539, 549** (âncoras remedidas depois das edições desta rodada; `grep -n "docs/img/" README.md`) |
| `git show HEAD:tools/publish-thunderstore.sh` | confirmado: laço `for z in dist/gumatos-*.zip` e header de autorização literal — a base do texto "legado" |
| `git log --format='%h %ci %s' -3` | `39852b7 2026-10-16 13:58:21 PUB-ALL-1 …` e `844bba8 2026-10-16 13:49:58 DOC-REV …` — a base do A8 |

## 5. O que PRECISA DE DECISÃO DO DONO

1. **9 capturas pendentes (classe 4).** `README.md` linhas **392, 402, 408, 413, 442, 456, 462, 539, 549**
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
   01/10) e o arquivo **não registra** `RealmApi`. Não editei (é o gate, com frente própria; a DEP-REV
   §8.3 também apontou). A doc agora diz isso de forma explícita (A1), em vez de repetir o texto velho.
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
   (`docs/README.md:416-418`). Quando o lote sair, essas tabelas precisam de nova passada — é o mesmo
   risco de deriva do A8.
9. **Fotografias datadas mantidas de propósito:** `docs/README.md:421-430` (adendo de 12/10),
   `docs/README.md:466-471` (aviso de cache da API, 30/09), `docs/README.md:433-448` (bloco "6 mods,
   01/10/2026") e `README.md:696` ("empacotador conhece 6 mods, medido em 30/09/2026"). São verdadeiras
   para a data declarada e ficam ao lado do estado corrente; decidir se vale carimbá-las mais
   explicitamente como foto.
10. **`tools/publish-thunderstore.sh`** (envio local) não lê o gate, envia todos os `dist/gumatos-*.zip`
    e usa o header de autorização sem a variável `TOKEN` lida no início. Há frente em andamento
    (PKG-API-1, **não commitada** em 16/10) que faz o script ler o ledger. A doc diz para **não** usar
    como caminho seguro até essa frente estar commitada e provada; testar/corrigir o script é tarefa própria.
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
`RealmApi`), enquanto o empacotador versionado devolve 8 e o gate `release/mods.json` continua com 8.

Por isso as linhas de documentação que falam do empacotador foram escritas para o **estado versionado**
com a nota explícita da frente em andamento — nenhuma afirmação depende de código não commitado:

- `README.md:197-199` ("the versioned packager does not discover that module…");
- `docs/README.md:32-43` (o parágrafo dos 8 nomes + o aviso da árvore de trabalho);
- `docs/ESTRUTURA.md:12` (linha do `api/` no layout canônico);
- `docs/PUBLICACAO.md:383-394` (envio local legado);
- `docs/README.md:383` (a linha do `publish-thunderstore.sh` na tabela de ferramentas).

**Quando a PKG-API-1 fechar, revisar essas cinco passagens** (o número "8" e a frase "não é descoberta
pelo empacotador" passam a valer só para o gate). Hotspot declarado em comentário no cartão.

## 7. Travas respeitadas

- Nada de código de mod, manifest, CHANGELOG, ícone ou `.csproj` foi editado.
- `git add -A` não foi usado: os commits desta frente listam caminho explícito de arquivo.
- `docs/automacao/**` (fora deste arquivo de entrega) e `docs/cobertura/**` não foram revisados nem tocados.
- Não houve build, deploy, ciclo de jogo, publicação, push de release nem criação de tarefa.
- Alterações de outras frentes encontradas no checkout (manifests, CHANGELOGs, ícones, código do RLP,
  `api/*`, `tools/*`, `.github/*`, relatórios históricos, `harness-out/`, `kanban.db`,
  `tools/preparar_revisao_dono.py`) foram preservadas intactas e ficaram fora do stage.
