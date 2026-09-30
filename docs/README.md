# Documentação do repositório — índice

Este é o **índice** da documentação do projeto. A documentação de `docs/` é
**versionada** (ver `ENT-2` no `KANBAN.md`): o `.gitignore` ignora `*.md` como regra
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
`BetterFont`, `RoguelikeQoL`, `RoguelikeDebugger` (e `RoguelikeBalance`, que ainda não
virou mod). Cada um é um projeto independente, com `DeployToBepInEx` próprio no
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
(`INC-1`/`INC-3` no `KANBAN.md`). Nenhum passo pode ser pulado — inclusive o passo 3,
que é o que trava a release.

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
`TextFixes 72 entradas | duplicadas: nenhuma` e `TextAppends 195 entradas | duplicadas: nenhuma`.

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

Relatório: `docs/cobertura/revisao/RV-15-notas-redundantes.md`. Estado em 30/09: **195 notas
analisadas, 0 casos** (as duas notas redundantes que existiam — `Blind` e `Sleep` — foram
removidas).

### Passo 5 — instalar a DLL no perfil do r2modman

O build já traz o target `DeployToBepInEx` (INFRA-1) que copia a DLL sozinho. Se
precisar fazer na mão (ou para conferir que a cópia aconteceu):

```bash
cp BetterTooltips/bin/Debug/netstandard2.1/BetterTooltips.dll \
   "%USERPROFILE%/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/plugins/BetterTooltips/"
```

Destino correto, sempre: **uma pasta por mod, com a DLL dentro dela** —
`plugins\<Mod>\<Mod>.dll`. DLL solta em `plugins/` não carrega; e **backup de DLL
nunca vai para dentro de `plugins/`** (o BepInEx varre a pasta recursivamente e carrega
o backup como se fosse mod — ver `AMBIENTE.md`).

### Passo 6 — ciclo do jogo e leitura do log

```bash
bash scratch/test-cycle.sh 12 "padrão1|padrão2"
```

O script encerra a instância anterior, limpa o `LogOutput.log`, lança o jogo pela Steam
com o doorstop do perfil, espera o plugin carregar, filtra o log pelo padrão que você
passou e fecha o jogo. O segundo argumento é um `grep -E` — ex.:
`bash scratch/test-cycle.sh 20 "QoL fonte|Better Tooltips"`.

**Critério de aprovação — no `LogOutput.log` do perfil:**

```bash
LOG="%USERPROFILE%/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log"
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
| `check_notas_redundantes.py` | A nota **repete** o que o texto já diz? (RV-15: `nota == chave` — duplicado na tela; nota contida na chave; nota que ecoa ≥ 6 palavras; e a família contextual — nota de Armor em texto onde Armor é *fonte* de dano). Lê as 195 notas e sai com exit 1 se achar caso. |
| `check_scaling.py` | A skill escala com algo que a tooltip não diz? → `revisao/escala.md`. |
| `check_status_numeros.py` | Os números da descrição do status existem nos efeitos? (RV-9) |
| `check_terminologia.py` | Consistência de **termos** no jogo inteiro (RV-14, regra da maioria). |
| `analisa_conferir.py` | Desmonta os itens "conferir" de uma ficha: o que o código diz sobre aquele número. |
| `review_ledger.py` | Gera `docs/cobertura/revisao/ANTES-E-DEPOIS.md` a partir do fonte do mod. |
| `importa_beneficio.py` | Traz a classificação buff/debuff do log para o `status.csv`. |
| `pack-for-friends.sh` | Compila e empacota os mods distribuíveis em `dist/`. |
