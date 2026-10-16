# DOC-REV — revisão da documentação viva

Cartão: `t_d9d74e4d`. Data: 16/10/2026. Repositório: `C:/dev/stolen-realm`.
Nenhum jogo foi aberto, nenhum build/deploy foi rodado, nenhuma publicação foi feita, nenhum
manifest/CHANGELOG de mod foi editado e nada de `docs/automacao/**` ou `docs/cobertura/**` foi revisado.

## 0. Cobertura

- **Arquivos do escopo revisados: 20 de 20** (a lista nominal do cartão).
  `README.md`, `STATUS.md`; `docs/README.md`, `AMBIENTE.md`, `ESTRUTURA.md`, `CI.md`, `PUBLICACAO.md`,
  `SUPERVISAO.md`, `PROCESSO-REVISAO.md`, `PLANO-DE-TESTES.md`, `MODS-PARA-AMIGOS.md`, `DEBUGGER.md`,
  `DBG-PROVENIENCIA.md`; `api/README.md`, `api/docs/README.md`; `ITEM_INVENTORY.md`,
  `ITEM_MOD_INVENTORY.md`, `STATUS_INVENTORY.md`, `SKILL_INVENTORY.md`, `TOOLTIP_SWEEP.md`.
- Contexto do repositório, medido: **670 arquivos `.md` versionados** (`git ls-files '*.md'`),
  **950 arquivos versionados só em `docs/automacao/`** (arquivo, fora do escopo) e
  **135 arquivos `.md`/`.json`/`.txt` versionados fora de `automacao/`+`cobertura/`**.
  Dos 20 revisados, **11 exigiam correção**; 9 não tinham problema factual e não foram tocados.
- Revisão anterior deste cartão morreu por *rate limit* (run 1593) deixando as edições em disco, sem
  commit e sem entrega. As edições foram relidas, reverificadas contra o disco de 16/10/2026 e
  completadas nesta rodada; o que mudou depois da coleta original está anotado na seção 3.

Legenda de classe: **1** afirmação falsa sobre o estado atual · **2** contradição entre documentos ·
**3** instrução que não funciona · **4** link quebrado interno · **5** falta de informação essencial.

## 1. Correções feitas (arquivo | linha | problema | classe | ação)

### `README.md` (raiz)

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| README.md | 4-6 | "No mod touches the game's content, balance or files" — falso: o repositório tem mod de progressão (RLP) que muda gameplay, além de projetos não publicados | 1 | corrigido: separa mods publicados (QoL) de projetos não publicados |
| README.md | 49 | "BetterCombatText … depends on BetterFont" — falso depois da DEP-REV (16/10): o manifest do BCT declara só `BepInExPack` | 1 | corrigido |
| README.md | 49-52 | tabela de mods listava 4 mods; faltavam BetterCombatText, RSTV, BetterPortuguese e RLP | 1, 5 | linhas acrescentadas, marcando os não publicados |
| README.md | 92-95, 111-114 | "a DLL **não pode** ficar solta em `plugins\`" e "o BepInEx carrega **todo** `.dll`, inclusive `.bak`" — o loader procura `*.dll`; `.dll.disabled`/`.bak`/`.old` não casam | 1 | corrigido (convenção de pasta ≠ exigência; backup fora de `plugins\`) |
| README.md | 153-155 | "Check dependencies first: BetterCombatText requires BetterFont" | 1 | corrigido para a dependência real (RSTV → RealmApi) |
| README.md | 172-173 | troubleshooting mandava a DLL estar em pasta por mod como causa de não carregar | 1 | corrigido |
| README.md | 192-199 | tabela de identificadores com versões 0.1.1/1.0.1/1.0.2/0.1.1 (reais: 0.1.4/1.0.2/1.0.3/0.1.2) e sem os pacotes novos | 1 | corrigido; nota de que versão no fonte ≠ ZIP publicado |
| README.md | 353-360 e 628-635 | as mesmas versões erradas repetidas na metade PT-BR e no fim do arquivo | 1, 2 | corrigidas |

### `STATUS.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| STATUS.md | 11-13 | "o log existente de 16/10/2026 lista 10 plugins" — o cabeçalho do `LogOutput.log` registra a rodada de **12/09/2026 21:34**; a data do arquivo não é a data da sessão | 1 | corrigido (data da leitura + data do cabeçalho) |
| STATUS.md | 16-17 | não dizia que `gh` não existe nesta máquina | 3 | acrescentado |

### `docs/README.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| docs/README.md | 28 | a linha do `img/LEIA-ME.txt` afirmava que o README da raiz usa "notas de captura pendente, sem links para PNG inexistentes" — o README tem **9** `![](docs/img/*.png)` sem arquivo | 1, 2 | corrigido para o estado real (9 links quebrados até a captura) |
| docs/README.md | 32-40 | "na raiz, uma pasta por mod … (e `RoguelikeBalance`, que ainda não virou mod)" — hoje a descoberta tem **8** nomes e `RoguelikeBalance` não existe na árvore | 1 | corrigido |
| docs/README.md | 32-40 | nada dizia que a API existe em `api/` e é consumida pelo RSTV | 5 | acrescentado (com o limite: não é descoberta pelo empacotador) |
| docs/README.md | 235 | bloco bash usava `%APPDATA%` — no Git Bash é sintaxe de cmd.exe e **não expande** | 3 | trocado por `cygpath -u "$APPDATA"` (comando executado) |
| docs/README.md | 238-242 | "DLL solta em `plugins/` não carrega" | 1 | corrigido |
| docs/README.md | 393-404 | tabela "Os 6 mods" com versões e estado de publicação de 01/10 (BCT 0.1.1 "não publicado", RSTV 0.3.2, etc.) | 1 | reescrita: 8 descobertos, 6 publicados em 07/10/2026 |
| docs/README.md | 407-411 | "conferido contra a API pública em 01/10/2026" | 1 | reconferido por endpoint em 16/10/2026 |
| docs/README.md | 435 | dependência declarada como `BetterCombatText 0.1.1 → BetterFont 1.0.2`; o estado real é `RSTV 0.3.3 → RealmApi-0.1.0` (não resolvível) | 1, 2 | reescrito |

### `docs/AMBIENTE.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| AMBIENTE.md | 28 | "Plugins que carregam no perfil `Default` (**8**)" e "log de 16/10/2026" — o log lido tem **10** plugins e o cabeçalho é de 12/09 | 1 | corrigido (10; `LogOutput.log` lido em 16/10) |
| AMBIENTE.md | 41, 44 | versões carregadas desatualizadas (Better Combat Text 0.1.1, RSTV 0.2.0, Better Tooltips 0.1.1) | 1 | corrigidas pelo log real (+ CAP-1 Probe, RLP 0.1.1) |
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
| CI.md | 88-135 | tabela de passos desatualizada: faltavam `check_versoes`, `check_patches`, `cobertura_ui_localized --prova` e o passo do empacotador; `checa_citacoes.py` era citado como passo 10 **do YAML**, onde ele não está | 1, 3 | reescrita contra o `validate.yml` real (conferido passo a passo) |
| CI.md | 137-146 | mandava colar um bloco no `validate.yml` "num PAT com escopo `workflow`" como instrução corrente | 3 | rebaixado a proposta histórica, sem diagnóstico de credencial |

### `docs/PUBLICACAO.md`

| arquivo | linha | problema | classe | ação |
|---|---|---|---|---|
| PUBLICACAO.md | 9-18 | "o projeto tem 6 mods e os SEIS estão publicados … `release/mods.json` com as 6 entradas" como estado de hoje | 1 | corrigido (8 entradas, 6 publicadas em 07/10) + foto de 01/10 preservada |
| PUBLICACAO.md | 99-101 | "Hoje o repo **não tem** LICENSE e **nenhum** README/manifest menciona licença" — `api/LICENSE` é MIT e o README da API declara isso | 1 | corrigido (licença do módulo ≠ licença dos demais mods) |
| PUBLICACAO.md | 338-341 | os dois `gh release create` do documento sem avisar que `gh` **não está instalado** nesta máquina | 3 | aviso acrescentado (`which gh` → nada, 16/10/2026) |
| PUBLICACAO.md | 374-382 | `tools/publish-thunderstore.sh` recomendado como "o caminho mais curto hoje" — ele não lê o gate, itera **todos** os `dist/gumatos-*.zip` e o header de autorização não usa a variável `TOKEN` lida no início | 1, 3 | corrigido como envio **legado** e não seguro; script não foi executado |

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
| PLANO-DE-TESTES.md | 14-17 | "podem rodar em CI quando o `lib/` estiver disponível lá" — contradiz `docs/CI.md` (o CI não usa `lib/` e não deve receber a pasta) | 2 | corrigido |
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

## 2. Revisado sem alteração

| arquivo | por quê |
|---|---|
| `api/docs/README.md` | 21 linhas, atual: os dois comandos citados existem (`api/tools/Inspect/Inspect.csproj`, `api/tools/check_ui_contract.py`) e o texto já declara o limite "runtime NÃO_EXERCITADO". Nada factual a corrigir. |
| `STATUS.md` | **Não versionado por desenho** (`.gitignore:18-21`: `*.md` na raiz fica fora do git, exceto `README.md`). É nota de trabalho local: as correções desta frente existem em disco e **não** entram em commit. |
| `ITEM_INVENTORY.md`, `ITEM_MOD_INVENTORY.md`, `STATUS_INVENTORY.md`, `SKILL_INVENTORY.md`, `TOOLTIP_SWEEP.md` | Inventários/dumps da raiz, **também ignorados pelo git por decisão explícita** (mesmo bloco do `.gitignore`). Totais conferidos programaticamente e **batem** com os títulos: 905 itens (60+118+98+66+83+81+62+33+3+301), 285 afixos, 600 status (497/83/14/6), 453 skills (somas por classe conferidas). Nada factual a corrigir; nenhum arquivo foi tocado. |
| `TOOLTIP_SWEEP.md` | Declara "patch notes mais recentes: v1.3.1, 15/09/2026". Confirmado: o v1.3.1 é a última nota de patch (a novidade mais recente no Steam News é "Stolen Realm 2 Announced", 01/10/2026, que não é patch). |
| `api/README.md` | **Revisado, não commitado**: já estava modificado por outra frente quando esta tarefa começou (`hotspot` registrado em comentário no cartão). O diff preexistente não foi incluído em nenhum commit desta frente (ver seção 4). |

## 3. O que mudou entre a coleta original (13:22) e a entrega (13:5x)

A tarefa `t_6ac74f0f` (DEP-REV) concluiu **depois** da fotografia usada pela rodada anterior e alterou
dois manifests, sem commit:

1. `BetterCombatText/manifest.json` — dependência `DefRuivo_StolenRealmMods-BetterFont-1.0.3` **removida**
   (era dependência de pacote sem dependência de código).
2. `RoguelikeSkillTreeVisualizer/manifest.json` — `DefRuivo_StolenRealmMods-RealmApi-0.1.0` **acrescentada**.

Isso invalidou afirmações que a rodada anterior havia escrito (BCT "depends on BetterFont", "RSTV não
declara RealmApi"): as quatro ocorrências foram corrigidas nesta rodada (`README.md:49`, `docs/README.md:397`,
`docs/PLANO-DE-TESTES.md:35`, `docs/PROCESSO-REVISAO.md:31-33`; `docs/README.md:435` também reescrita).
Os manifests e CHANGELOGs **não** foram tocados por esta frente, conforme a trava do cartão.

## 4. Provas coletadas (comandos reais, 16/10/2026)

| comando | resultado |
|---|---|
| `python tools/pack-thunderstore.py --listar-nomes` | **8** nomes no empacotador versionado: BetterCombatText, BetterFont, BetterPortuguese, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer, RoguelikeUnlimitedLevelProgression. **RealmApi não aparece.** Na árvore de trabalho às 13:5x a mesma chamada já imprimia **9** (com `RealmApi`) por causa da frente PKG-API-1 em andamento — ver seção 6. |
| `python tools/check_versoes.py` | exit 0; csproj = manifest = Plugin.cs = README em todos os 8 (0.1.2/1.0.3/0.1.0/1.0.2/0.1.4/0.1.2/0.3.3/0.1.1). A ferramenta não cobre a API. |
| `python tools/check_dependencias.py --local` (via DEP-REV) | exit 1: `DefRuivo_StolenRealmMods-RealmApi-0.1.0` não resolve — o upload do RSTV seria recusado hoje |
| API por pacote (`/api/experimental/package/DefRuivo_StolenRealmMods/<nome>/`) | HTTP 200 para os 6 publicados, com `latest.version_number` = tabela do cartão e data 07/10/2026; HTTP 404 para BetterPortuguese, RoguelikeUnlimitedLevelProgression e RealmApi |
| `python tools/audita_docs.py` (antes e depois das edições) | mesmas 4 pendências nas duas execuções — nenhuma introduzida por esta frente (ver seção 5) |
| `which gh` | vazio — **`gh` não está instalado nesta máquina** |
| `ls LICENSE` (raiz) | não existe; `api/LICENSE` = MIT (Copyright 2026 Gumatos) |
| `ls RoguelikeDebugger/Patches/*.cs` | 10 arquivos; tags no fonte: `[Status] [Action] [Skill] [Item] [ItemMod] [Powerup] [Loot] [Event] [LifeSteal] [Dmg] [Gold] [Exp] [ExpInimigo] [Efeitos] [Proveniencia]` |
| `grep BepInDependency RoguelikeSkillTreeVisualizer/Plugin.cs` | `[BepInDependency(ApiGuid, ApiVersionMinima)]` — hard, mínimo 0.1.0 |
| `git diff --check` nos arquivos desta frente | sem erro |
| `git check-ignore -v STATUS.md` | `.gitignore:20:*.md` — `STATUS.md` e os cinco inventários da raiz **não são versionados** (decisão do repo: notas de trabalho na raiz ficam fora do git) |
| Links relativos dos 20 documentos | 93 links, **9 quebrados**, todos `docs/img/*.png` (capturas pendentes declaradas) |

## 5. O que PRECISA DE DECISÃO DO DONO

1. **9 capturas pendentes (classe 4).** `README.md:388,398,404,409,438,452,458,535,545` aponta para
   `docs/img/*.png` que não existem (a pasta tem só `LEIA-ME.txt` e dois PNG de ícone, sem nenhuma captura
   de uso). O próprio `docs/img/LEIA-ME.txt` declara esse estado como pendente, então **não apaguei nem
   converti em nota**: decidir entre tirar as 9 capturas (nomes já especificados no LEIA-ME.txt) ou
   remover os links.
2. **`tools/audita_docs.py` está reprovando o repositório correto.** A regra `DEP_EXTRAS`
   (linhas 360-369) exige `BetterCombatText → BetterFont` no manifest. Depois da DEP-REV isso é
   falso permanente: o auditor acusa "dependencia do Thunderstore fora do padrao" e não reconhece
   `RSTV → RealmApi`. O próprio script pede ("Falso positivo de regra: ajuste a regra AQUI"). **Não editei
   `tools/`** (fora do escopo documental) — precisa de tarefa própria.
3. **`release/mods.json` contradiz a documentação corrigida.** Os `motivo` e `caso_de_hoje` ainda falam
   "PUBLICAR 0.1.1"/"BetterFont 1.0.2 ainda não está no ar" (versões de 01/10) e o arquivo **não registra
   RealmApi**. Não editei (é o gate, com frente própria; a DEP-REV §8.3 também apontou). Enquanto isso,
   valem os campos estruturados — está escrito em `docs/PUBLICACAO.md` e `docs/README.md`.
4. **`api/manifest.json` é novo e não versionado**, e o `audita_docs` o reprova com "api: versao diverge
   entre manifest/csproj/plugin" — falso positivo de layout: o auditor procura `<Mod>/<Mod>.csproj` e
   `<Mod>/Plugin.cs` na raiz da pasta, e a API tem `api/Plugin/RealmApi.csproj`. Decidir se o auditor e o
   empacotador passam a entender o layout da API (é o mesmo bloqueio do item 2 da DEP-REV §8).
5. **`api/README.md` tem diff preexistente de outra frente** (preparação do pacote RealmApi) — não entrou
   em commit desta frente. Se aquele texto contiver afirmação falsa, a correção é da frente dona.
6. **`docs/BETTERPORTUGUESE-ARQUITETURA.md:37,286`** cita `evidence/audit_sources.py`, que não existe no
   repositório (é ferramenta de workspace). É a quarta pendência do auditor. O arquivo **não está na lista
   do cartão** — reportado em vez de editado.
7. **`BetterCombatText/README.md:9,43-49`** ainda declara a dependência de BetterFont e menciona 1.0.2
   contra 1.0.3 do manifest antigo — resíduo apontado pela própria DEP-REV, com a filha `t_d00f2bc6`
   encarregada de alinhar. Fora da minha trava (é README de mod).
8. **Fotografias datadas mantidas de propósito:** `docs/README.md:455-463` e `README.md:267,691`
   ("empacotador conhece 6 mods, medido em 30/09/2026"), `docs/README.md:427-442` (bloco "6 mods,
   01/10/2026"). São verdadeiras para a data declarada e ficam ao lado do estado corrente; decidir se vale
   carimbá-las mais explicitamente como foto.
9. **`tools/publish-thunderstore.sh`** (envio local) não lê o gate, envia todos os `dist/gumatos-*.zip` e
   usa `Authorization: Bearer …` sem a variável `TOKEN` lida no início. A doc agora diz para não usar como
   caminho seguro; corrigir/testar o script é tarefa própria.
10. **Seis arquivos do escopo não são versionados** (`.gitignore:18-21`): `STATUS.md` e os cinco
   inventários da raiz. O cartão os trata como "documentação viva", mas quem clona o repositório não os
   recebe — as correções desta frente em `STATUS.md` valem só nesta máquina. Decidir se esse é o desenho
   desejado (nota local) ou se algum deles deve passar a versionado.

## 6. Colisões e trabalho em andamento (hotspot)

Durante esta revisão, três arquivos de `tools/`/CI **já estavam sendo alterados por outra frente**
(PKG-API-1, que ensina o empacotador a reconhecer o layout aninhado da RealmApi): `tools/pack-thunderstore.py`,
`tools/publish-thunderstore.sh` e `.github/workflows/publish.yml`. Na árvore de trabalho,
`python tools/pack-thunderstore.py --listar-nomes` já devolve **9** nomes (com `RealmApi`) enquanto o
empacotador versionado devolve 8 e o gate `release/mods.json` continua com 8.

Por isso as linhas de documentação que falam do empacotador foram escritas para o **estado versionado**
com a nota explícita da frente em andamento — nenhuma afirmação depende de código não commitado:

- `README.md:197-200` ("the versioned packager does not discover that module…");
- `docs/README.md:32-43` (o parágrafo dos 8 nomes + o aviso da árvore de trabalho);
- `docs/ESTRUTURA.md:12` (linha do `api/` no layout canônico);
- `docs/PUBLICACAO.md:375-383` (envio local legado).

**Quando a PKG-API-1 fechar, revisar essas quatro passagens** (o número "8" e a frase "não é descoberta
pelo empacotador" passam a valer só para o gate). Hotspot declarado em comentário no cartão.

## 7. Travas respeitadas

- Nada de código de mod, manifest, CHANGELOG, ícone ou `.csproj` foi editado.
- `git add -A` não foi usado: os commits desta frente listam caminho explícito de arquivo.
- `docs/automacao/**` (fora deste arquivo de entrega) e `docs/cobertura/**` não foram revisados nem tocados.
- Não houve build, deploy, ciclo de jogo, publicação, push de release nem criação de tarefa.
- Alterações de outras frentes encontradas no checkout (manifests, CHANGELOGs, ícones, código do RLP,
  `api/*`, relatórios históricos, `harness-out/`, `kanban.db`, `tools/preparar_revisao_dono.py`) foram
  preservadas intactas e ficaram fora do stage.
