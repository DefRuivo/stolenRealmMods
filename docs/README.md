# Documentação do repositório — índice

Este é o **índice** da documentação do projeto. A documentação de `docs/` é
**versionada**: o `.gitignore` ignora `*.md` como regra
geral — as notas de trabalho na raiz (`KANBAN.md`, `*_INVENTORY.md`, `TOOLTIP_SWEEP.md`)
seguem **fora** do git de propósito — e re-inclui `docs/**/*.md` mais `README.md`,
`CHANGELOG.md`, `manifest.json` e `icon.png` na raiz de cada mod.

Leia este arquivo nesta ordem: **§1** para saber o que existe, **§3 (o ritual de
build)** se você vai compilar e instalar alguma coisa. O ambiente de máquina
(versões, caminhos, decisões) está em [`AMBIENTE.md`](AMBIENTE.md).

---

## 1. O que tem em `docs/`

| Arquivo | Para quem | O que é |
|---|---|---|
| `README.md` | mantenedor | **Este índice** + o ritual de build. |
| `AMBIENTE.md` | mantenedor | Ambiente reproduzível: versões validadas (BepInEx, Unity, .NET, Python), caminhos do jogo e do perfil do r2modman, a decisão sobre a `StolenRealmModAPI` e a regra de backup de DLL. |
| `MODS-PARA-AMIGOS.md` | mantenedor | Os dois lados da distribuição: como gerar o pacote (`tools/pack-for-friends.sh` → `dist/StolenRealm-Mods-<data>.zip`) e o que o amigo faz com ele. Diz o que **entra** e o que **não entra** no zip. |
| `LEIA-ME.txt` | usuário final | Instruções de instalação em 5 minutos (r2modman ou BepInEx na mão) + os 3 problemas mais comuns. É este arquivo que vai **dentro** do zip distribuído. |
| `img/LEIA-ME.txt` | mantenedor | Lista das **capturas de tela pendentes** que o `README.md` da raiz espera nesta pasta (`docs/img/<nome>.png`) — nomes exatos, como capturar e onde cada uma entra. |
| `cobertura/` | mantenedor | O **censo** do que existe para revisar (CSVs) e os relatórios de revisão. Ver §2. |

O repositório tem, na raiz, uma pasta por mod — `BetterTooltips`, `BetterStats`,
`BetterFont`, `RoguelikeQoL`, `RoguelikeDebugger`, e — em implementação —
`RoguelikeSkillTreeVisualizer` (e `RoguelikeBalance`, que ainda não virou mod). Cada um é um projeto independente, com `DeployToBepInEx` próprio no
`.csproj`. A descrição de cada mod e o que ele **não** faz está no `README.md` da
pasta do mod.

## 2. `docs/cobertura/` — o censo e os relatórios

O censo responde "**o que** existe para revisar" — sem ele, "revisar todas as tooltips"
não é conferível. Os números fechados (29/09/2026) estão em
[`cobertura/README.md`](cobertura/README.md), que é o documento de referência das
colunas, do vocabulário de `status` e do critério de "revisado".

### CSVs (gerados por `tools/census.py` e `tools/censo_status.py`)

| Arquivo | Linhas | Entradas | O que é |
|---|---:|---:|---|
| `skills.csv` | 452 | **451** | Skills/spells (31 são da árvore **Bard → intocável**) |
| `skills-detalhe.csv` | 454 | **453** | O que o jogo **calcula** para cada skill (`expr`, `danoExpr`, `acts`, `pstat`…) — é aqui que se confere se o número da tooltip bate |
| `status.csv` | 561 | **560** | Buffs/debuffs/status (coluna `classe` e `beneficio`) |
| `itens.csv` | 906 | **905** | Itens base |
| `afixos.csv` | 286 | **285** | Prefixos/sufixos de item |
| `acoes.csv` | 277 | **276** | Ações (a fórmula de dano que a skill concede) |
| `powerups.csv` | 80 | **79** | Powerups (uma linha por **nível**, porque o tooltip é por nível) |
| `invocacoes.csv` | 19 | **18** | Invocações |

(Entradas = linhas − 1 cabeçalho.) Cada CSV tem a coluna **`status`**, que é o
checklist: `pendente` / `revisado` / `corrigido` / `sem-explicacao` / `intocavel`. A
coluna **sobrevive à regeneração** — o `census.py` carrega os status do arquivo
anterior antes de reescrever.

### Relatórios

| Arquivo | O que é |
|---|---|
| `cobertura/README.md` | Referência do censo: colunas, vocabulário de `status`, critério de revisado, gramática dos textos (`[N]`, `[[X]]`, `@x@`), o que o censo ainda **não** cobre. |
| `cobertura/alerta-tokens.md` | Saída de `tools/scan_tokens.py` (RV-8a): onde o `[...]` do texto pode virar `Parsing Error` em jogo. |
| `cobertura/auditoria-tooltips.md` | Saída de `tools/audit_tooltips.py` (RV-8b): dano sem tipo declarado, número fixo onde há valor dinâmico, área não mencionada, descrições curtas. |

### `cobertura/revisao/` — 37 relatórios de revisão

| Grupo | Arquivos | Nº |
|---|---|---:|
| **Fichas por árvore** (texto × código, uma por árvore) | `ficha-basic`, `ficha-chaos`, `ficha-cold`, `ficha-fire`, `ficha-innate`, `ficha-light`, `ficha-lightning`, `ficha-monk`, `ficha-nature`, `ficha-ranger`, `ficha-shadow`, `ficha-thief`, `ficha-warrior` | 13 |
| **RV-8b** (auditoria de skills) | `RV-8b-0f-propriedades`, `RV-8b-2c-ranger`, `RV-8b-2e-fechamento`, `RV-8b-shadow`, `RV-8b-shadow-lote2` | 5 |
| **RV-9** (buffs/debuffs/status) | `RV-9-censo`, `RV-9-buffs` (+`-1`..`-6`), `RV-9-debuffs` (+`-1`..`-4`), `RV-9-numeros` | 14 |
| **Outros** | `ANTES-E-DEPOIS.md` (o livro de correções, gerado por `tools/review_ledger.py` a partir do fonte do mod), `escala.md`, `omissoes.md`, `RV-14-terminologia.md`, `REVISAR-AO-FINAL.md` (checklist de fechamento) | 5 |

**Como regerar o censo** (nenhuma leitura manual — sai do dump de boot do
`RoguelikeDebugger`):

```bash
bash scratch/test-cycle.sh 30 "Inventário"   # abre o jogo, coleta o dump, fecha
python tools/census.py                       # regrava os CSVs de docs/cobertura/
```

---

## 3. O RITUAL DE BUILD (obrigatório)

Ordem **inegociável**. Cada passo existe por causa de um incidente real
(`INC-1`/`INC-3`/`BUG-32`, registrados no quadro de trabalho interno do projeto). Nenhum passo pode ser pulado — inclusive os passos 3 e 5,
que são os que **travam** a release.

> **Antes de tudo:** feche o jogo. A cópia da DLL para o perfil falha se o arquivo
> estiver em uso.

### Passo 0 — pré-requisitos

- A pasta `lib/` na raiz do repositório precisa ter as referências de compilação:
  `Assembly-CSharp.dll`, `BepInEx.dll`, `UnityEngine.dll`, `UnityEngine.CoreModule.dll`,
  `0Harmony.dll` e os `Sirenix.*`. Ela é **gitignored** (são DLLs do jogo) — ver
  [`AMBIENTE.md`](AMBIENTE.md).
- Toolchain: .NET SDK 6 (alvo dos mods `netstandard2.1`) e Python 3.

### Passo 1 — compilar com **0 erros**

```bash
cd C:/dev/stolen-realm
LC_ALL=C dotnet build BetterTooltips/BetterTooltips.csproj --nologo -v q -clp:ErrorsOnly
```

Troque pelo mod que você mexeu (`BetterStats/BetterStats.csproj`,
`BetterFont/BetterFont.csproj`, `RoguelikeQoL/RoguelikeQoL.csproj`,
`RoguelikeDebugger/RoguelikeDebugger.csproj`). Saída esperada: **nada** (o
`-clp:ErrorsOnly` só imprime erro). Qualquer linha vermelha = **pare aqui**.

### Passo 2 — `check_fix_keys`: as chaves existem no censo?

```bash
python tools/check_fix_keys.py
```

As tabelas `TextFixes`/`TextAppends` do `BetterTooltips` casam por texto **exato**.
Uma chave com um espaço a mais — ou escrita de memória em vez de copiada do asset —
**nunca dispara**: a falha é silenciosa. Saída esperada hoje: **264 chaves, 260 no
censo, 4 fora** — as 4 de fora são textos de UI/dica de loading, que o censo do RV-7
não cobre. Fora do censo **não é erro por si**; o que não pode é uma chave de
skill/status/item/afixo que você *achou* que existia.

### Passo 3 — `check_dupes`: **TRAVA OBRIGATÓRIA**

```bash
python tools/check_dupes.py     # exit 1 se houver chave duplicada
```

**Por que este passo não é opcional (`INC-1`):** `Dictionary<string,string>` em C# não
aceita chave repetida — o `Add` estoura `ArgumentException`, e como as tabelas são
`static readonly` a exceção vira `TypeInitializationException`: **a classe inteira não
carrega e o mod todo morre** (não se perde só a entrada nova). Aconteceu com `Slam` e
`Crushing Slam`, que têm o **texto idêntico** e viraram duas chaves iguais. O
`check_fix_keys` **não pega** esse caso (com chave repetida a contagem continua
"certa"); por isso o `check_dupes` existe. Saída esperada hoje:
`TextFixes 86 entradas | duplicadas: nenhuma` e `TextAppends 206 entradas | duplicadas: nenhuma`.

### Passo 4 — `check_notas_redundantes`: a nota **repete** o texto?

```bash
python tools/check_notas_redundantes.py    # exit 1 se achar nota redundante
```

Uma nota existe para dizer o que o texto **não** diz. Quando ela repete o próprio texto, o
jogador lê a mesma frase duas vezes e a explicação perde crédito. A varredura caça três
famílias: **nota == chave** (duplicado na tela), **nota inteiramente contida na chave** e
**nota que ecoa ≥ 6 palavras seguidas**. Também acusa a família *contextual* — nota de Armor
em texto onde Armor é **fonte** de dano e não mitigação (casos `Battle Ready` e `Diamond
Ice`, barrados no código por `ArmorValueSourceRegex`).

Relatório: `docs/cobertura/revisao/RV-15-notas-redundantes.md`. Estado em 30/09: **206 notas
analisadas, 0 casos** (as duas notas redundantes que existiam — `Blind` e `Sleep` — foram
removidas).

### Passo 5 — `check_chave_compartilhada --estrito`: **TRAVA OBRIGATÓRIA** (`BUG-32`)

```bash
python tools/check_chave_compartilhada.py --estrito   # exit 1 = release travada
```

O mod casa tooltip por **texto exato**, e o lookup é `if/else if` na **mesma chave**: se a
mesma chave existir em `TextFixes` **e** em `TextAppends`, a entrada de `TextAppends`
**nunca roda** — a nota não existe em jogo, em silêncio, **sem nenhum erro no log**. É
defeito objetivo, não opinião; por isso `--estrito` sai 1, e é esse o modo que o
`release-check.sh` usa. Caso real (30/09): a nota de *stack* de `Consumption`
(`TextAppends` l.431) está morta — quem executa é o fix de terminologia
(`maximum`→`max`) da `TextFixes` l.907.

A **mesma** varredura lista também as **SUSPEITAS** (texto com correção/nota usado por 2+
entidades — 12 em 30/09) e essas seguem **aviso que não reprova**, nos dois modos: se a
nota mente para os outros donos depende da mecânica que ela cita — decisão humana.

Correção no `LocalizePatch.cs`: **uma entrada por texto** — fundir o valor da `TextAppends`
no valor da `TextFixes` que executa (as duas coisas passam a valer) e apagar a duplicada.

Sem a flag o script é relatório puro (`python tools/check_chave_compartilhada.py`, sempre
exit 0). Relatório: `docs/cobertura/revisao/BUG-32-chaves-compartilhadas.md`. Para testar o
detector sem tocar no `LocalizePatch.cs`: `--estrito --fonte OUTRO.cs`.

### Passo 6 — instalar a DLL no perfil do r2modman

O build já traz o target `DeployToBepInEx` (INFRA-1) que copia a DLL sozinho. Se
precisar fazer na mão (ou para conferir que a cópia aconteceu):

```bash
cp BetterTooltips/bin/Debug/netstandard2.1/BetterTooltips.dll \
   "%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/plugins/BetterTooltips/"
```

Destino correto, sempre: **uma pasta por mod, com a DLL dentro dela** —
`plugins\<Mod>\<Mod>.dll`. DLL solta em `plugins/` não carrega; e **backup de DLL
nunca vai para dentro de `plugins/`** (o BepInEx varre a pasta recursivamente e carrega
o backup como se fosse mod — ver `AMBIENTE.md`).

### Passo 7 — ciclo do jogo e leitura do log

```bash
bash scratch/test-cycle.sh 12 "padrão1|padrão2"
```

O script encerra a instância anterior, limpa o `LogOutput.log`, lança o jogo pela Steam
com o doorstop do perfil, espera o plugin carregar, filtra o log pelo padrão que você
passou e fecha o jogo. O segundo argumento é um `grep -E` — ex.:
`bash scratch/test-cycle.sh 20 "QoL fonte|Better Tooltips"`.

**Critério de aprovação — no `LogOutput.log` do perfil:**

```bash
LOG="%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log"
grep -acE "ArgumentException|TypeInitializationException|\[Error" "$LOG"   # tem que dar 0
grep -a "plugins to load" "$LOG"                                            # 6 plugins no perfil Default
grep -a "carregado\." "$LOG"                                                # 1 linha por mod do projeto
```

- **zero** `ArgumentException`;
- **zero** `TypeInitializationException`;
- **zero** linhas `[Error`;
- uma linha `... carregado.` por mod do projeto.

Só depois disso a alteração conta como instalada e testada.

---

## 4. `tools/` — o que cada script faz

| Script | O que faz |
|---|---|
| `census.py` | Lê o dump de boot do `RoguelikeDebugger` no log e gera os CSVs de `docs/cobertura/` (preserva a coluna `status`). |
| `censo_status.py` | Cria/mantém o censo de revisão dos **status** (RV-9). |
| `check_fix_keys.py` | Confere as chaves de `TextFixes`/`TextAppends` contra o censo. **Passo 2 do ritual.** |
| `check_dupes.py` | Chave duplicada nas tabelas do `LocalizePatch`. **Passo 3 do ritual (trava).** |
| `verify_tree.py` | Bancada por árvore: junta o texto da skill com o código (`attr`, `expr`, `danoExpr`, ações, status) → `docs/cobertura/revisao/ficha-<arvore>.md`. |
| `audit_tooltips.py` | Auditoria de conteúdo das skills (RV-8b) → `docs/cobertura/auditoria-tooltips.md`. |
| `scan_tokens.py` | Varredura da gramática de texto (RV-8a) → `docs/cobertura/alerta-tokens.md`. |
| `check_omissao.py` | A tooltip omite algo que muda a decisão do jogador? |
| `check_notas_redundantes.py` | A nota **repete** o que o texto já diz? (RV-15: `nota == chave` — duplicado na tela; nota contida na chave; nota que ecoa ≥ 6 palavras; e a família contextual — nota de Armor em texto onde Armor é *fonte* de dano). Lê as 206 notas e sai com exit 1 se achar caso. |
| `check_chave_compartilhada.py` | Varredura de **chave compartilhada** (BUG-32) contra o censo: (a) **a mesma chave nas duas tabelas** — `TextFixes` executa e `TextAppends` nunca roda, a nota não existe em jogo sem erro no log → **exit 1 com `--estrito`** (**passo 5 do ritual, trava**); (b) **suspeitas** (texto com nota usado por 2+ entidades) → aviso que **não** reprova, decisão humana. `--fonte OUTRO.cs` aponta o parser para outro fonte (teste do detector). |
| `check_scaling.py` | A skill escala com algo que a tooltip não diz? → `revisao/escala.md`. |
| `check_status_numeros.py` | Os números da descrição do status existem nos efeitos? (RV-9) |
| `check_terminologia.py` | Consistência de **termos** no jogo inteiro (RV-14, regra da maioria). |
| `analisa_conferir.py` | Desmonta os itens "conferir" de uma ficha: o que o código diz sobre aquele número. |
| `review_ledger.py` | Gera `docs/cobertura/revisao/ANTES-E-DEPOIS.md` a partir do fonte do mod. |
| `importa_beneficio.py` | Traz a classificação buff/debuff do log para o `status.csv`. |
| `pack-for-friends.sh` | Compila e empacota os mods distribuíveis em `dist/`. |
| `pack-thunderstore.py` | Gera o pacote no padrão do Thunderstore (4 arquivos na raiz + `plugins/<Mod>/<Mod>.dll`), com pre-flight que **aborta** em vez de gerar pacote inválido. |
| `check_segredos.py` | **Trava de segredo:** varre os arquivos versionados procurando credencial (token do Thunderstore, PAT do GitHub, chave privada). Exit 1 e o release para. |
| `publish-thunderstore.sh` | Publica os pacotes pela API. **Dry-run por padrão** — só sobe com `--go`. Tira o token de `TCLI_AUTH_TOKEN`, de `$THUNDERSTORE_TOKEN_FILE` ou de `~/.thunderstore-token`; recusa se o arquivo do token estiver dentro do repositório. |
| `release-check.sh` | **A trava de release:** roda os 7 passos de uma vez (segredos → build 0 erros → chaves → duplicadas → notas → chave compartilhada `--estrito` → ciclo do jogo → conferência visual humana) e para no primeiro que falhar. Duas travas objetivas até aqui: duplicadas (`INC-1`) e chave nas duas tabelas (`BUG-32`). |

---

## Pacote Thunderstore / r2modman

**Decisao do usuario (30/09):** os mods ficam **separados** — cada um e um pacote independente no
Thunderstore, com seus proprios `manifest.json`, `README.md`, `CHANGELOG.md` e `icon.png` (que vivem
DENTRO da pasta do mod). Nao existe pasta `src/` nem `thunderstore/`: a estrutura atual ja entrega o
mesmo resultado e mover quebraria o pack script, as regras `!*/manifest.json` do `.gitignore` e o alvo
`DeployToBepInEx` dos csproj.

**Os parametros que o Thunderstore exige, conferidos um a um nos 5 mods:**

| parametro | regra | estado |
|---|---|---|
| `name` | alfanumerico/underscore, ate 128, estavel entre releases | OK |
| `version_number` | semver MAJOR.MINOR.PATCH, ate 16 chars | OK |
| `description` | ate 250 chars | OK (139..160) |
| `website_url` | URL valida | OK |
| `icon.png` | PNG 256x256, ate 1 MB | OK (256x256, ~940 bytes) |
| `dependencies` | `Autor-Pacote-Versao` | `BepInEx-BepInExPack-5.4.2305` |
| arquivos | README.md e CHANGELOG.md na raiz do pacote | OK |

**A dependencia foi VERIFICADA, nao inventada:** a comunidade `stolen-realm` do Thunderstore tem 5
pacotes, e o pack do BepInEx e `BepInEx-BepInExPack` na versao **5.4.2305** — exatamente a que o perfil
do r2modman deste PC usa. Consulta: `curl -s https://thunderstore.io/c/stolen-realm/api/v1/package/`.
`StolenRealmModding-StolenRealmModAPI` tambem existe la, mas **nenhum mod nosso depende dela** (esta
desativada e falha neste build do jogo) — por isso ela nao entra em nenhum manifest.

**Estrutura do ZIP** (conferida com `unzip -l`): os 4 arquivos na RAIZ do pacote + `plugins/<Mod>/<Mod>.dll`.
O r2modman mapeia `plugins/` para `BepInEx/plugins/`, entao a DLL cai no lugar certo.


### Publicação — credencial e namespace

**O namespace — ATENÇÃO, MUDOU EM 30/09.** O primeiro token de service account pertencia ao team
`Stolen_Realm_Mods`; o token novo pertence a um team **diferente**, `DefRuivo_StolenRealmMods`. Como o
namespace do pacote **é o team** e nome de pacote publicado **não se renomeia**, qual dos dois publica
é uma **decisão a tomar antes do primeiro upload** (tarefa `PUB-3`). Os 6 nomes de pacote estão
**livres** na comunidade (conferido na API pública em 30/09/2026, que naquele momento listava 5
pacotes: `BepInEx-BepInExPack`, `StolenRealmModding-StolenRealmModAPI`,
`StolenRealmModding-Player_Limit_Mod`, `ebkr-r2modman` e `Kesomannen-GaleModManager`), então qualquer
um dos dois teams pode reivindicá-los.

**O token nunca entra no repositório.** Ele é lido, nesta ordem, de `TCLI_AUTH_TOKEN`, de um arquivo
apontado por `THUNDERSTORE_TOKEN_FILE`, ou de `~/.thunderstore-token` (fora da árvore do git). Duas
travas protegem isso: a regra de credencial no `.gitignore` (`.thunderstore-token`, `*.token`,
`*.pem`, `*.key`) e o `tools/check_segredos.py`, que é o **passo 0** do `release-check.sh` — um
release que contenha token nem chega a compilar.

```bash
bash tools/publish-thunderstore.sh          # dry-run: mostra o que subiria
bash tools/publish-thunderstore.sh --go     # publica de verdade
bash tools/publish-thunderstore.sh --go BetterTooltips   # um mod só
```

O script roda a trava de segredo e o `release-check.sh` antes de qualquer envio (para pular a parte
do ciclo do jogo em publicação automatizada: `PULAR_RELEASE_CHECK=1`, use com consciência).

> **Token colado em chat é token exposto.** O do Thunderstore e o PAT do GitHub foram passados por
> mensagem: os dois devem ser **rotacionados** no painel de cada serviço depois de usados.

**Gerar o pacote:** `python tools/pack-thunderstore.py` (ou passando nomes de mods para empacotar so alguns).
Os zips saem em `dist/` com pre-flight: sem manifest valido, README, CHANGELOG, icone 256x256 real ou DLL
buildada ele **sai com erro sem gerar pacote quebrado**.

**Testar antes de publicar (r2modman):** `Import local mod` no perfil -> conferir que a DLL caiu em
`BepInEx/plugins/<Mod>/` -> abrir pelo "Start modded" -> conferir `<Mod> carregado.` no `LogOutput.log`.

**Publicar:** ainda manual no site do Thunderstore (o CI de release e a tarefa PKG-4). A versao nao pode
repetir uma ja publicada — por isso a PKG-2 (fonte unica de versao) importa.
