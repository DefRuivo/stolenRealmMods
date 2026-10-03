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
| `PROCESSO-REVISAO.md` | mantenedor | O **padrão de revisão do projeto**: toda tarefa executada gera uma revisão **independente** (feita por quem não escreveu a mudança, com prova: commit, arquivos e saída das ferramentas) **antes** de qualquer validação ou aprovação humana. |
| `TEXTO-TOOLTIPS.md` | mantenedor | A **convenção de texto e cor das tooltips**: os **três níveis** (branco = descrição curta com os valores dinâmicos; tom mais escuro = explicação de termos e cálculos; azul = acúmulo das auras de shrine e efeitos provenientes de skills), a **procedência declarada de cada cor** (campo de cor do próprio jogo lido em runtime — cor sem procedência é número inventado) e o teste de comprimento do nível 2 medido pelo `tools/check_notas_redundantes.py`. |
| `CI.md` | mantenedor | Os **dois workflows** de GitHub Actions: `validate.yml` (só **valida**, a cada `push`/PR na `main`) e `publish.yml` (**manual**, com gate humano), os 7 passos do CI na ordem, como rodar tudo na mão e as armadilhas. |
| `PUBLICACAO.md` | mantenedor | Publicação na Thunderstore: as regras da plataforma, o gate versionado `release/mods.json`, o Environment `thunderstore`, o passo a passo de um release e as armadilhas. |
| `AMBIENTE.md` | mantenedor | Ambiente reproduzível: versões validadas (BepInEx, Unity, .NET, Python), caminhos do jogo e do perfil do r2modman, a decisão sobre a `StolenRealmModAPI` e a regra de backup de DLL. |
| `MODS-PARA-AMIGOS.md` | mantenedor | Os dois lados da distribuição: como gerar o pacote (`tools/pack-for-friends.sh` → `dist/StolenRealm-Mods-<data>.zip`) e o que o amigo faz com ele. Diz o que **entra** e o que **não entra** no zip. |
| `LEIA-ME.txt` | usuário final | Instruções de instalação em 5 minutos (r2modman ou BepInEx na mão) + os 3 problemas mais comuns. É este arquivo que vai **dentro** do zip distribuído. |
| `img/LEIA-ME.txt` | mantenedor | Lista das **capturas de tela pendentes** que o `README.md` da raiz espera nesta pasta (`docs/img/<nome>.png`) — nomes exatos, como capturar e onde cada uma entra. |
| `RSTV-ANALISE.md` | mantenedor | Pontos de ancoragem do `RoguelikeSkillTreeVisualizer` (RSTV-1) no **decompilado** do jogo: onde a UI que o mod toca é montada, com `arquivo:linha` em cada afirmação. É análise, não implementação. |
| `cobertura/` | mantenedor | O **censo** do que existe para revisar (CSVs) e os relatórios de revisão. Ver §2. |

O repositório tem, na raiz, uma pasta por mod — `BetterCombatText`, `BetterFont`,
`BetterStats`, `BetterTooltips`, `RoguelikeDebugger` e
`RoguelikeSkillTreeVisualizer` (e `RoguelikeBalance`, que ainda não virou mod — `BAL-1`).
Cada um é um projeto independente, com `DeployToBepInEx` próprio no
`.csproj`, e os **6** são pacotes Thunderstore completos (`manifest.json`, `README.md`,
`CHANGELOG.md`, `icon.png`). A descrição de cada mod e o que ele **não** faz está no
`README.md` da pasta do mod; o que cada um faz em uma linha, a versão no disco e o estado
de publicação estão na tabela de *Pacote Thunderstore*, mais abaixo. `ReloadProbe`
(`com.gumatos.reloadprobe`) **não** entra nessa conta: é o **harness de bancada** que mede
o custo de recarregar, vive no disco e é ignorado pelo git (`.gitignore`, `ReloadProbe/`).

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

### `cobertura/revisao/` — 48 relatórios de revisão

O número é o **total de `.md` desta pasta** e o `tools/audita_docs.py` (**passo 7 do CI**)
confere ele: o total do título, o `Nº` de cada linha (nomes listados na linha), todo nome
citado existindo na pasta e todo `.md` da pasta citado nesta tabela. Relatório novo entra na
pasta **e** aqui, senão o CI reprova — foi assim que 5 relatórios entraram sem passar pelo
índice (o título dizia 37 com 42 na pasta).

| Grupo | Arquivos | Nº |
|---|---|---:|
| **Fichas por árvore** (texto × código, uma por árvore) | `ficha-basic`, `ficha-chaos`, `ficha-cold`, `ficha-fire`, `ficha-innate`, `ficha-light`, `ficha-lightning`, `ficha-monk`, `ficha-nature`, `ficha-ranger`, `ficha-shadow`, `ficha-thief`, `ficha-warrior` | 13 |
| **RV-8b** (auditoria de skills) | `RV-8b-0f-propriedades`, `RV-8b-2c-ranger`, `RV-8b-2e-fechamento`, `RV-8b-shadow`, `RV-8b-shadow-lote2` | 5 |
| **RV-9** (buffs/debuffs/status) | `RV-9-censo`, `RV-9-buffs`, `RV-9-buffs-1`, `RV-9-buffs-2`, `RV-9-buffs-3`, `RV-9-buffs-4`, `RV-9-buffs-5`, `RV-9-buffs-6`, `RV-9-debuffs`, `RV-9-debuffs-1`, `RV-9-debuffs-2`, `RV-9-debuffs-3`, `RV-9-debuffs-4`, `RV-9-numeros` | 14 |
| **Relatórios de caso e de fechamento** | `ANTES-E-DEPOIS.md` (o livro de correções, gerado por `tools/review_ledger.py` a partir do fonte do mod), `BT-18-passivas-inimigo.md`, `BUG-32-chaves-compartilhadas.md`, `CHK-1-shrines-conferencia-mecanica.md`, `escala.md`, `omissoes.md`, `REVISAR-AO-FINAL.md` (checklist de fechamento), `RSTV-1-investigacao.md`, `RSTV-5-confirmacao-prefab.md` (confirmação do INDETERMINADO do RSTV-3 — o X do prefab), `RSTV-10-confirmacao-prefab.md`, `RV-13-auditoria-cobertura.md`, `RV-13b-fechamento.md`, `RV-14-terminologia.md`, `RV-15-notas-redundantes.md`, `RV-19-shrines.md`, `RV-35-40-shrines-conferencia.md` | 16 |

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
LC_ALL=C dotnet build BetterTooltips/BetterTooltips.csproj -p:DeployToBepInEx=false --nologo -v q -clp:ErrorsOnly
```

A `-p:DeployToBepInEx=false` é o que mantém este passo **local**: **sem ela o target
`DeployToBepInEx` roda e copia a DLL para o perfil do r2modman** (`plugins\<Mod>\`) — é isso que
instala, e é por que um `dotnet build` comum escreve no ambiente do dono.

Troque pelo mod que você mexeu (`BetterStats/BetterStats.csproj`,
`BetterFont/BetterFont.csproj`,
`RoguelikeDebugger/RoguelikeDebugger.csproj`, `RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj`,
`BetterCombatText/BetterCombatText.csproj`). Saída esperada: **nada** (o
`-clp:ErrorsOnly` só imprime erro). Qualquer linha vermelha = **pare aqui**.

### Passo 2 — `check_fix_keys`: as chaves existem no censo?

```bash
python tools/check_fix_keys.py
```

As tabelas `TextFixes`/`TextAppends` do `BetterTooltips` casam por texto **exato**.
Uma chave com um espaço a mais — ou escrita de memória em vez de copiada do asset —
**nunca dispara**: a falha é silenciosa. Saída medida em 30/09/2026 (17:21): **291 chaves,
287 no censo, 4 fora** — as 4 de fora são textos de UI/dica de loading, que o censo do RV-7
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
"certa"); por isso o `check_dupes` existe. Saída medida em 01/10/2026 (14:36), depois do lote
ARM-1 (as duas notas de família de arma):
`TextFixes 101 entradas | duplicadas: nenhuma` e `TextAppends 197 entradas | duplicadas: nenhuma`
(o `tools/audita_docs.py`, passo 7, compara estes dois números com o `LocalizePatch.cs` — é por
ele que um `TextAppends N entradas` escrito de memória vira CI vermelho). **Limite conhecido
deste check:** ele só confere a forma `TextFixes N entradas` / `TextAppends N entradas`; contagem
escrita em prosa («N notas», *Passo 4*) **não** é conferida. Foi assim que a doc trazia
`206 notas` enquanto a ferramenta dizia **205** (antes do lote de terminologia do RV-14) e o
`audita_docs.py` saía `0` mesmo assim — número em prosa também precisa ser conferido à mão
contra a ferramenta, e a ferramenta é que manda.

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

Relatório: `docs/cobertura/revisao/RV-15-notas-redundantes.md`. Estado em 01/10/2026 (ARM-1):
**197 notas analisadas, 0 casos** — e a mesma saída passa a valer como trava da **cor do nível
2** (nota sem o marcador `#C8B090` sai como caso) e como **medida de comprimento** (as notas com
quebra de linha interna são listadas; comprimento não reprova — quem decide encurtar é o dono,
ver `TEXTO-TOOLTIPS.md` §4). **Quem manda é a ferramenta** — o número em prosa sempre foi
divergência quando não bateu com o que ela imprime (o valor mudou 205 → 195 quando o lote de
terminologia do RV-14 moveu entradas de `TextAppends` para `TextFixes`).

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

**Este passo escreve no ambiente do dono.** O destino é `BepInEx\plugins\<Mod>\` dentro do
perfil do r2modman (`%APPDATA%\r2modmanPlus-local\...`). O build já traz o target
`DeployToBepInEx` (INFRA-1) que copia a DLL sozinho **por padrão** — é justamente isso que os
passos anteriores desligam com `-p:DeployToBepInEx=false` para não instalar sem querer. Se
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
`bash scratch/test-cycle.sh 20 "Better Font carregado|Better Tooltips carregado"`.

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

### Passo 8 — Release: só quando for **empacotar** (PKG-5)

O dia a dia continua em **Debug**: `dotnet build <Mod>/<Mod>.csproj` (sem `-c`) compila em
`<Mod>/bin/Debug/netstandard2.1/<Mod>.dll` e o alvo `DeployToBepInEx` copia essa DLL para o perfil
do r2modman. **Nada disso mudou.**

O que passou a existir é o build de **Release** para gerar o artefato que vai para o `dist/`. É o
mesmo fonte — nenhum arquivo dos 6 mods usa `#if DEBUG` (conferido com
`grep -rn "#if DEBUG" BetterFont/ BetterStats/ BetterTooltips/ RoguelikeDebugger/ RoguelikeSkillTreeVisualizer/ BetterCombatText/`,
30/09/2026: **nenhuma ocorrência**) —
então muda só otimização/pdb/nome da pasta de saída.

```bash
cd C:/dev/stolen-realm
LC_ALL=C dotnet build BetterTooltips/BetterTooltips.csproj -c Release -p:DeployToBepInEx=false --nologo -v q -clp:ErrorsOnly
```

- a DLL sai em **`<Mod>/bin/Release/netstandard2.1/<Mod>.dll`** (a pasta de Debug fica intacta);
- **`-p:DeployToBepInEx=false` desliga o deploy** — é o que impede um build de Release de
  sobrescrever a DLL que está instalada no perfil do r2modman (obrigatório quando o mod está aberto
  em teste). O alvo `DeployToBepInEx` dos 7 `.csproj` ganhou
  `Condition="'$(DeployToBepInEx)' != 'false'"`: **sem a flag o comportamento é o de sempre** (copia),
  e a cópia continua usando `$(TargetPath)`, ou seja, a DLL da configuração que foi buildada.

Saída literal medida em 30/09/2026 (os dois mods mais simples; os outros 4 usam o mesmo `.csproj` e
a mesma receita):

| mod | comando | resultado |
|---|---|---|
| BetterFont | `dotnet build BetterFont/BetterFont.csproj -c Release -p:DeployToBepInEx=false` | `Compilação com êxito.` / `1 Aviso(s)` / `0 Erro(s)` → `BetterFont/bin/Release/netstandard2.1/BetterFont.dll` |
| BetterStats | `dotnet build BetterStats/BetterStats.csproj -c Release -p:DeployToBepInEx=false` | `Compilação com êxito.` / `2 Aviso(s)` / `0 Erro(s)` → `BetterStats/bin/Release/netstandard2.1/BetterStats.dll` |

Conferência de que o deploy ficou desligado de verdade: nenhuma linha `Deploy:`/`copiado para` na
saída e o MD5 das DLLs do perfil **não mudou** depois do build.

O aviso é o `MSB3277` **pré-existente** (`System.Net.Http`: o `Assembly-CSharp.dll` do jogo aponta
para 4.2.0.0 e o `netstandard2.1` traz 4.1.2.0). Ele aparece igual em Debug e Release e não é erro.

**Resolvido em 30/09 (PKG-6 + PKG-2 + PKG-3).** Quem consome a DLL para empacotar passou a ler a
build de **Release**: o caminho é resolvido por configuração, como o `$(Configuration)` do MSBuild
— `<Mod>/bin/<Config>/netstandard2.1/<Mod>.dll`. No `tools/pack-thunderstore.py` isso é o
`--config` (padrão **Release**; `--config Debug` ou `PACK_CONFIG=Debug` ficam para conferência) e
no `tools/pack-for-friends.sh` é a variável `CONFIG` (padrão **Release**). Os dois buildam com
`-p:DeployToBepInEx=false`, para que gerar pacote **nunca** sobrescreva a DLL instalada no perfil.
O comentário do `.github/scripts/valida_pacotes.py` acompanhou.

Efeito colateral esperado: mod **sem** build de Release passa a ser recusado no pre-flight
(`DLL NAO BUILDADA` + o comando exato para resolver) em vez de entrar no zip com a DLL de Debug —
pacote de configuração errada era o defeito.

Saída literal medida em 30/09/2026 (`python tools/pack-thunderstore.py BetterFont`):

```
  ok    BetterFont         v1.0.0  | BetterFont\bin\Release\netstandard2.1\BetterFont.dll
  BetterFont: gumatos-BetterFont-1.0.0.zip
      plugins/BetterFont/BetterFont.dll             9216 bytes
      TOTAL                                       100592 bytes  (5 arquivos)
```

e no zip (`unzip -l dist/gumatos-BetterFont-1.0.0.zip`): `manifest.json`, `README.md`,
`CHANGELOG.md` e `icon.png` na **raiz** + `plugins/BetterFont/BetterFont.dll`, 5 arquivos.

---

## 4. `tools/` — o que cada script faz (e **quando** rodar)

Cada ferramenta de `tools/` está aqui; a coluna *Quando rodar* diz o gatilho — os passos do
ritual (§3), os passos do CI ([`CI.md`](CI.md)) ou o momento de manutenção. Trava = o passo
reprova e a release para.

| Script | O que faz | Quando rodar |
|---|---|---|
| `census.py` | Lê o dump de boot do `RoguelikeDebugger` no log e gera os CSVs de `docs/cobertura/` (preserva a coluna `status`). | Manutenção do censo, depois de um ciclo de jogo que produziu o dump. |
| `censo_status.py` | Cria/mantém o censo de revisão dos **status** (RV-9). | Junto do `census.py`, ao revisar status (buff/debuff). |
| `gera_shrines_esperado.py` | **CHK-1:** GERA (não digita) `tools/dados/shrines-esperado.csv` e `tools/dados/shrines-percentuais.csv` — as bases das 12 auras de shrine saem do censo (`docs/cobertura/status.csv`, coluna `efeitos`) e do `resources.assets` (Dwarven/Decay/Flame e as % por tipo), cada uma com a citação `arquivo:linha` / `assets@offset`. **FALHA** (exit 1) se uma base não tiver fonte — nunca chuta. `--check` compara a tabela versionada com o que as fontes geram. | Depois de mexer em censo/asset ou quando o `--check` acusar diferença; antes de uma rodada de conferência dos shrines. |
| `checa_shrines.py` | **CHK-1:** confere o `LogOutput.log` (linhas `[Shrine RV-23]`) e o dump do `RoguelikeDebugger` contra `tools/dados/shrines-esperado.csv`: **OK / ACHADO / AUSENTE / NAO-VER** por aura × caso (0, +20, +100), com observado, esperado e diferença; cross-check da base contra o dump do próprio jogo; checagem de aditividade do `resto` (total − aura). **Lista o que não foi exercitado** — ausência não vira aprovação (exit 0 só com tudo exercitável verde; 1 = achado; 3 = incompleto). | Depois de cada rodada em jogo nos shrines (roteiro no `revisao/CHK-1-shrines-conferencia-mecanica.md`). |
| `check_fix_keys.py` | Confere as chaves de `TextFixes`/`TextAppends` contra o censo. | **Passo 2 do ritual**; passo 2 do CI. As 4 chaves de UI/loading fora do censo são **aviso**, não erro. |
| `check_dupes.py` | Chave **duplicada** nas tabelas do `LocalizePatch` (`INC-1`). | **Passo 3 do ritual — TRAVA**; passo 3 do CI. |
| `tabelas.py` | O **parser único** das tabelas `TextFixes`/`TextAppends` do `LocalizePatch.cs`: `bloco()` (acha o dicionário pelo `NOME = new Dictionary` e casa as chaves de fechamento) e `entradas()` (lê os pares) pulando comentário de **linha** (`//`) e de **bloco** (`/* */`) em todo passo. É a **fonte da verdade** da contagem oficial — os leitores que aparecem nesta tabela são **wrappers/consumidores** dele (`check_chave_compartilhada`, `check_dupes`, `check_notas_redundantes`, `check_fix_keys`, `check_omissao`, `check_scaling`, `review_ledger`, `regras_cor`), e o `t_parser_comentario_na_chave.py` cross-verifica os oito. | Não roda sozinho: é **importado**. `python tools/tabelas.py` roda a prova local (as entradas com comentário de linha e de bloco TÊM de ser vistas). |
| `check_versoes.py` | **PKG-2 (só olha o repositório, sem build):** confere se a versão de cada mod bate nos **quatro** lugares — `<Mod>/<Mod>.csproj` (`<Version>`, a fonte), `<Mod>/manifest.json` (`version_number`), `<Mod>/Plugin.cs` (`[BepInPlugin(...)]`) e `<Mod>/README.md` (`- **Version:**`). Importa o parser do `pack-thunderstore.py`, então o gate e o empacotador nunca discordam sobre "qual é a versão". | **Passo 1 do `release-check.sh`** (aborta na hora, como segredos e patches) e **passo 2 do CI** (`validate.yml`); também roda à mão quando se quer a trava de versão antes de empacotar. |
| `check_dependencias.py` | **PKG-5:** toda dependência de cada `manifest.json` tem de **resolver** — a versão referida já está publicada (`--api`, endpoint por versão, fresco, sem token) ou sai no **mesmo lote** com a dependência **antes** do dependente (`--local`, sem rede, lê `release/mods.json`); calcula a **ordem de envio** e reprova **mão dupla entre versões inéditas** (ciclo). É a regra que o `.github/scripts/valida_pacotes.py` importa (regra 8), então o push já a confere. | Antes de liberar/publicar um lote de mods com dependência entre si; no push, dentro do passo 6 do CI. |
| `verify_tree.py` | Bancada por árvore: junta o texto da skill com o código (`attr`, `expr`, `danoExpr`, ações, status) → `docs/cobertura/revisao/ficha-<arvore>.md`. | Revisão de uma árvore de skills (gera a ficha). |
| `audit_tooltips.py` | Auditoria de conteúdo das skills (RV-8b) → `docs/cobertura/auditoria-tooltips.md`. | Revisão de conteúdo das skills (RV-8b). |
| `scan_tokens.py` | Varredura da gramática de texto (RV-8a) → `docs/cobertura/alerta-tokens.md`. | Revisão da gramática de texto (RV-8a). |
| `check_omissao.py` | A tooltip omite algo que muda a decisão do jogador? → `revisao/omissoes.md`. Desde o PARSER-1 (01/10) a coluna "o que o mod já cobre" lê o parser único (`tools/tabelas.py`): o regex antigo varria o arquivo inteiro e colhia **4 chaves fantasma** de inicializadores fora dos blocos (`Armor increased by 5%`, `Increased Armor`, `Elemental resistance reduced by 5% per stack`, `Life Steal`), **duas delas casando com o censo** — o relatório antigo tinha 2 "já cobertas" **falsas**. O total caiu de 302 para **298** (as entradas reais das duas tabelas): a mudança é para **mais estrito** e é ganho, não perda de cobertura. | Revisão de conteúdo, quando a dúvida é "falta informação". |
| `check_notas_redundantes.py` | A nota **repete** o que o texto já diz? (RV-15: `nota == chave` — duplicado na tela; nota contida na chave; nota que ecoa ≥ 6 palavras; e a família contextual — nota de Armor em texto onde Armor é *fonte* de dano). Mede **197** notas e sai com exit 1 se achar caso. Desde o COR-1 (01/10) confere também a **cor do nível 2**; **desde o COR-2 (01/10) a cobertura é fechada**: confere **toda cor de todo valor** de `TextAppends` e de `TextFixes` (em **qualquer** formato — a primeira versão só olhava `\n\n<color=#…>` e ignorava 10 das 21 entradas com cor, incluindo **duas das 12 notas de shrine**), com a regra “cor que o **jogo já escrevia na chave** é legítima” (o `#808080` de citação) e o critério “**explicação E efeito**” (correção + nota no mesmo valor); o parser passou a ler as entradas com **comentário dentro do `{`** (o formato “chave em linha própria”); e **mede o comprimento** das notas (as com quebra interna saem listadas; comprimento não reprova — ver `TEXTO-TOOLTIPS.md` §4). A cor é aplicada **pelo gancho das notas** (§7), então a ordem de gancho não decide nada. | **Passo 4 do ritual**; passo 4 do CI. **Regenera** `docs/cobertura/revisao/RV-15-notas-redundantes.md` a cada execução (`--fonte OUTRO.cs` confere outra fonte e **não** regrava o relatório — é o que a isca em `tools/testes/contra-prova/` usa). |
| `preserva_curado.py` | Guarda do trecho **curado a mão** dos relatórios que a ferramenta reescreve: relê a parte escrita à mão (marcador `<!-- fim-gerado -->`) e a regrava **idêntica**, abortando com `CuradoPerdido` se ela sumir. Não é chamado pelo CI: é **importado** pelo `check_notas_redundantes.py` e pelo `check_terminologia.py`. | Junto desses dois checks (a guarda roda dentro deles) e às mãos quando se quer conferir a preservação sem rodar a varredura. |
| `check_chave_compartilhada.py` | Varredura de **chave compartilhada** (BUG-32) contra o censo: (a) **a mesma chave nas duas tabelas** — `TextFixes` executa e `TextAppends` nunca roda, a nota não existe em jogo sem erro no log → **exit 1 com `--estrito`** (**passo 5 do ritual, trava**); (b) **suspeitas** (texto com nota usado por 2+ entidades) → aviso que **não** reprova, decisão humana. `--fonte OUTRO.cs` aponta o parser para outro fonte (teste do detector). O **parser único** do `LocalizePatch.cs` é o `tools/tabelas.py` (a fonte da verdade); este script é um **wrapper** migrado sobre ele (o `check_dupes.py` o importa por contrato histórico) e a contagem oficial de `TextFixes`/`TextAppends` sai do `tabelas.py` — todos os leitores chegam à mesma definição. | **Passo 5 do ritual — TRAVA** (`BUG-32`); passo 5 do CI. Os dois chamam `--estrito`. |
| `check_scaling.py` | A skill escala com algo que a tooltip não diz? → `revisao/escala.md`. Desde o PARSER-1 (01/10) a lista "já resolvido pelo mod" lê o parser único (`tools/tabelas.py`): o regex antigo varria o arquivo inteiro e colhia 4 chaves fantasma (duas casando com o censo), então o relatório antigo tinha 2 "já cobertas" **falsas**; o total caiu de 302 para **298** e a mudança é para **mais estrito** (ganho, não perda de cobertura). | Revisão de conteúdo, quando a dúvida é "escala sem dizer". |
| `check_status_numeros.py` | Os números da descrição do status existem nos efeitos? (RV-9) | Revisão de status (RV-9). |
| `check_terminologia.py` | Consistência de **termos** no jogo inteiro (RV-14, regra da maioria). | Revisão de terminologia (RV-14). |
| `analisa_conferir.py` | Desmonta os itens "conferir" de uma ficha: o que o código diz sobre aquele número. | Ao fechar uma ficha, para resolver cada "conferir". |
| `review_ledger.py` | Gera `docs/cobertura/revisao/ANTES-E-DEPOIS.md` a partir do fonte do mod. | Ao fechar um lote de correções (o livro de correções). |
| `importa_beneficio.py` | Traz a classificação buff/debuff do log para o `status.csv`. | Ao atualizar a coluna `beneficio` do `status.csv`. |
| `pack-for-friends.sh` | Compila (**Release**, com `-p:DeployToBepInEx=false` para não tocar na DLL do perfil) e empacota os mods distribuíveis em `dist/`. Configuração: `CONFIG` (padrão `Release`). | Distribuição para amigos (ver [`MODS-PARA-AMIGOS.md`](MODS-PARA-AMIGOS.md)). |
| `pack-thunderstore.py` | Gera o pacote no padrão do Thunderstore (4 arquivos na raiz + `plugins/<Mod>/<Mod>.dll`) a partir de `<Mod>/bin/<Config>/` (`--config`, padrão **Release**), com pre-flight que **aborta** em vez de gerar pacote inválido: DLL buildada, manifest, README/CHANGELOG, icon 256x256 real e a **versão única** (`.csproj` × `manifest.json` × `Plugin.cs` × `README.md`; `--sincronizar-versao` conserta os espelhos a partir do `.csproj`). `--listar-nomes` dá a lista de mods para scripts. | Empacotar para publicação; `--sincronizar-versao <Mod>` depois de subir o `<Version>` do `.csproj`. |
| `check_segredos.py` | **Trava de segredo:** varre os arquivos **versionados** procurando credencial (token do Thunderstore, PAT do GitHub, chave privada) e, em seguida, chama o `check_padroes_segredo.py`. Exit 1 e o release para. | **Passo 0 do `release-check.sh`** e **passo 1 do CI**; também roda dentro do `publish-thunderstore.sh` e do job de publicação. |
| `check_padroes_segredo.py` | O **motor genérico** de credencial: formatos conhecidos (GitHub, Thunderstore, Slack, OpenAI, AWS, Google, GitLab, npm, PEM) **+** string longa de alta entropia, para pegar o que ainda não tem nome. Não guarda valor de token — só formato e medida. | Rodado **pelo** `check_segredos.py` (por isso é parte do passo 0 do `release-check` e do passo 1 do CI). Direto, só para a varredura mais ampla à mão. |
| `publish-thunderstore.sh` | Publica os pacotes pela API. **Dry-run por padrão** — só sobe com `--go`. Tira o token de `TCLI_AUTH_TOKEN`, de `$THUNDERSTORE_TOKEN_FILE` ou de `~/.thunderstore-token`; recusa se o arquivo do token estiver dentro do repositório. | Publicação local, quando o envio sai pela mão (ver [`PUBLICACAO.md`](PUBLICACAO.md)); é o caminho enquanto não se usa o `publish.yml`. |
| `release-check.sh` | **A trava de release:** roda os passos automatizados 0–7 (segredos → versões → patches → build 0 erros → chaves → duplicadas → notas → chave compartilhada `--estrito`), o passo 8 (**ciclo do jogo**, só no modo explícito `--instalar-no-perfil`) e imprime o **passo 9, humano** (conferência visual em jogo, não automatizável); no fim diz APROVADO/REPROVADO e lista quem falhou. **Não** para no primeiro erro — os passos 0 (segredos), 1 (versões) e 2 (patches TRV-1) **abortam na hora**; os outros acumulam para o relatório. Travas objetivas: duplicadas (`INC-1`), chave nas duas tabelas (`BUG-32`) e versão única (`PKG-2`). | Antes de **qualquer** release ou empacotamento (e é chamada pelo `publish-thunderstore.sh`). |
| `audita_docs.py` | **Auditoria das docs contra o disco:** contagens declaradas, versão de cada mod (manifest/csproj/plugin), ferramentas citadas x existentes em `tools/`, links relativos, caminhos que saíram do repo e a dependência do Thunderstore. Sai `exit 1` quando alguma afirmação não bate — é o **passo 7 do CI**. Descobre a raiz do repo a partir do próprio arquivo (roda de qualquer diretório) e **marca** os falsos positivos que já conhece (referência histórica ao `BetterTexts`, tabela que diz "não instale", a linha que explica que o `KANBAN.md` não é versionado, script de bancada em `scratch/`) em vez de reprovar. | **Passo 7 do CI**; depois de mexer em qualquer doc (é ele que confere contagem, versão, ferramenta e link). |

---

## Pacote Thunderstore / r2modman

**Decisao do usuario (30/09):** os mods ficam **separados** — cada um e um pacote independente no
Thunderstore, com seus proprios `manifest.json`, `README.md`, `CHANGELOG.md` e `icon.png` (que vivem
DENTRO da pasta do mod). Nao existe pasta `src/` nem `thunderstore/`: a estrutura atual ja entrega o
mesmo resultado e mover quebraria o pack script, as regras `!*/manifest.json` do `.gitignore` e o alvo
`DeployToBepInEx` dos csproj.

### Os 6 mods do projeto — o que faz, versão no disco e o que está no ar

| Mod | O que faz (uma linha) | Versão no disco | Na Thunderstore |
|---|---|---|---|
| `BetterCombatText` | Contorno/halo suave nos **nomes de inimigos** e nos **rótulos de buff/debuff**, mais o texto do dado nos eventos de rolagem (cada superfície liga/desliga no `.cfg`; não altera gameplay). | 0.1.1 | **PUBLICADO 0.1.0** (`DefRuivo_StolenRealmMods-BetterCombatText`, 01/10/2026) — a **0.1.1 no disco não foi publicada**: nenhuma linha de código mudou, ela bumpa a **dependência para o `BetterFont 1.0.2`** (sem isso o gerenciador instala a 1.0.1, cujo portão de material deixava os textos de combate na fonte original) e corrige o README. **Ordem de envio: o `BetterFont 1.0.2` primeiro.** |
| `BetterFont` | Troca a fonte da interface pela **serifada** (Times New Roman, com Georgia/Liberation Serif de reserva), preservando cor, contorno e sombra dos textos — **inclusive nos textos de combate** (nome do inimigo, número do dado), que usam outra variante de shader. | 1.0.2 | **PUBLICADO 1.0.1** (`DefRuivo_StolenRealmMods-BetterFont`, 01/10/2026) — a 1.0.0, de 30/09, foi substituída na vitrine. A **1.0.2 no disco não foi publicada**: é o BF-2, que conserta o portão de material (variante de shader deixou de ser recusa) e fecha os buracos de propriedade. |
| `BetterStats` | Mostra os atributos no formato **`base (combinado)`** na ficha de personagem e na tela de level up. | 1.0.1 | **PUBLICADO 1.0.1** (`DefRuivo_StolenRealmMods-BetterStats`, 01/10/2026). |
| `BetterTooltips` | Conserta tooltips de skill/status que "mentiam por omissão" e acrescenta ao fim a explicação da mecânica. | 0.1.1 | **PUBLICADO 0.1.1** (`DefRuivo_StolenRealmMods-BetterTooltips`, 01/10/2026). |
| `RoguelikeDebugger` | Ferramenta de **desenvolvimento**: despeja o inventário interno do jogo (skills, status, itens, loot) no `LogOutput.log` — é o dump que gera o censo. | 0.1.1 | **PUBLICADO 0.1.1** (`DefRuivo_StolenRealmMods-RoguelikeDebugger`, 01/10/2026) — categoria **Tools**. |
| `RoguelikeSkillTreeVisualizer` | Botão ao lado de *Choose Powerups* que abre a Skill Tree nativa em **modo somente leitura**, com o contexto real do personagem e sem gastar ponto. | 0.2.0 | **PUBLICADO 0.2.0** (`DefRuivo_StolenRealmMods-RoguelikeSkillTreeVisualizer`, 01/10/2026); o mod ainda **não foi conferido em jogo** pelo autor (roteiro no `README.md` dele). |

A versão no disco é a do `<Version>` do `.csproj` (fonte única — confere `manifest.json` e
`Plugin.cs`; ver *Fonte única de versão*). O que está no ar é o `versao_publicada` do
[`release/mods.json`](../release/mods.json), conferido contra a API pública em 01/10/2026
(`curl -s https://thunderstore.io/api/experimental/package/DefRuivo_StolenRealmMods/<Mod>/`).
Os nomes publicados são o namespace do team: `DefRuivo_StolenRealmMods-<Mod>`.

**Os parametros que o Thunderstore exige, conferidos um a um nos 6 mods** (contagens medidas com
`python .github/scripts/valida_pacotes.py`, 01/10/2026: `6 pacotes validados | 0 com problema`):

| parametro | regra | estado |
|---|---|---|
| `name` | alfanumerico/underscore, ate 128, estavel entre releases | OK |
| `version_number` | semver MAJOR.MINOR.PATCH, ate 16 chars | OK |
| `description` | ate 250 chars | OK (172..212) |
| `website_url` | URL valida | OK |
| `icon.png` | PNG 256x256, até 1 MB | OK (256x256; 57013..124954 bytes — todos abaixo de 1 MB) |
| `dependencies` | `Autor-Pacote-Versao` | `BepInEx-BepInExPack-5.4.2305` — e **uma** dependência entre mods deste repo, em **direção única**: `BetterCombatText 0.1.1` → `BetterFont 1.0.2` (o `BetterFont` não aponta de volta; o porquê está em `release/mods.json`) |
| arquivos | README.md e CHANGELOG.md na raiz do pacote | OK |

**A dependencia foi VERIFICADA, nao inventada:** a comunidade `stolen-realm` do Thunderstore tem 5
pacotes, e o pack do BepInEx e `BepInEx-BepInExPack` na versao **5.4.2305** — exatamente a que o perfil
do r2modman deste PC usa. Consulta: `curl -s https://thunderstore.io/c/stolen-realm/api/v1/package/`.
`StolenRealmModding-StolenRealmModAPI` tambem existe la, mas **nenhum mod nosso depende dela** (esta
desativada e falha neste build do jogo) — por isso ela nao entra em nenhum manifest.

**Estrutura do ZIP** (conferida com `unzip -l`): os 4 arquivos na RAIZ do pacote + `plugins/<Mod>/<Mod>.dll`.
O r2modman mapeia `plugins/` para `BepInEx/plugins/`, entao a DLL cai no lugar certo.


### Publicação — credencial e namespace

**O namespace — RESOLVIDO EM 30/09 (`PUB-3`).** O primeiro token de service account pertencia ao team
`Stolen_Realm_Mods`; o token novo pertence a um team **diferente**, `DefRuivo_StolenRealmMods`. Como o
namespace do pacote **é o team** e nome de pacote publicado **não se renomeia**, qual dos dois publica
era uma **decisão a tomar antes do primeiro upload** (`PUB-3`) — e ela foi tomada: quem publica é
**`DefRuivo_StolenRealmMods`** (registrado no `team` do [`release/mods.json`](../release/mods.json)).
Os **seis** mods do projeto estão **no ar** sob esse namespace — o `BetterCombatText`, o último que
faltava, saiu na leva de 01/10/2026. O nome na URL é `DefRuivo_StolenRealmMods-<Mod>`.

> **Ao conferir na API:** a listagem da comunidade (`/c/stolen-realm/api/v1/package/`) é **cache** e
> ainda devolvia os 5 pacotes antigos (`BepInEx-BepInExPack`, `StolenRealmModding-StolenRealmModAPI`,
> `StolenRealmModding-Player_Limit_Mod`, `ebkr-r2modman`, `Kesomannen-GaleModManager`) depois da
> publicação, em 30/09/2026. O pacote nosso aparece em
> `https://thunderstore.io/api/experimental/package/DefRuivo_StolenRealmMods/<Mod>/` (o
> `BetterCombatText` também responde `200` desde 01/10/2026 — os seis pacotes estão publicados).

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

### Fonte única de versão (PKG-2)

A versão tem **uma** fonte e três espelhos conferidos automaticamente — o Thunderstore recusa
versão repetida, e pacote com versão divergente é publicado errado sem ninguém perceber:

| arquivo | papel |
|---|---|
| `<Mod>/<Mod>.csproj` — `<Version>` | **FONTE** (autoritativa) |
| `<Mod>/manifest.json` — `version_number` | espelho — o que o Thunderstore lê |
| `<Mod>/Plugin.cs` — `[BepInPlugin(..., "x.y.z")]` | espelho — o que o log do BepInEx mostra |
| `<Mod>/README.md` — `- **Version:** x.y.z` | espelho — o que o usuário lê |

O pre-flight do `tools/pack-thunderstore.py` compara os quatro **antes de zipar**: se divergir,
nenhum pacote é gerado e a mensagem mostra qual está fora (seta `DIVERGE`) com o comando que
resolve. O `Plugin.cs` é lido nos dois formatos que o repo usa: literal no atributo (os mods mais
antigos) ou `public const string Version = "x.y.z"` usada como último argumento
(`RoguelikeSkillTreeVisualizer`) — o **mesmo critério** do `tools/audita_docs.py` (passo 7 do CI),
para não criar uma segunda regra de leitura.

**Subir a versão, na prática:** edite o `<Version>` do `.csproj` e rode **uma** vez
`python tools/pack-thunderstore.py --sincronizar-versao <Mod>` — ele reescreve o `manifest.json`, o `Plugin.cs`
e o `README.md` **só quando divergem** (se já batiam, os três arquivos ficam byte-a-byte iguais) e
não empacota nada. Depois é só empacotar.

> **Por que os espelhos não viraram código gerado** (a alternativa era um `VersaoMod.g.cs` escrito
> pelo MSBuild a partir do `<Version>`): o `tools/audita_docs.py`, passo 7 do CI, lê o literal
> **de dentro do `Plugin.cs`** — com a constante gerada em outro arquivo a auditoria perde o par e
> reprova. Com o pre-flight no empacotamento + o sincronizador, a divergência não chega ao zip nem
> ao site, e a edição manual por release caiu de quatro arquivos para um.

### Empacotar no Windows: `scripts/package.ps1` (PKG-3)

`.\scripts\package.ps1 <Mod>` faz o caminho completo em um comando e **não reimplementa nada**:
compila em `Release` com o deploy desligado, chama o `tools/pack-thunderstore.py` (fonte única da
validação) e confere o `dist/gumatos-<Mod>-<versao>.zip` gerado, com a versão lida do
`manifest.json`.

```powershell
.\scripts\package.ps1 BetterTooltips   # um mod
.\scripts\package.ps1                  # todos (lista vinda de --listar-nomes, não de uma 2a lista)
.\scripts\package.ps1 -Listar          # só lista os mods que o empacotador conhece
.\scripts\package.ps1 BetterStats -Config Debug    # empacotar a build de Debug
```

Faltando manifest/README/CHANGELOG/icon 256x256/DLL buildada, quem reclama é o Python — a
mensagem aponta o arquivo exato — e o `package.ps1` devolve o mesmo código de saída: **não existem
duas listas de regras** (era o risco de reimplementar a validação em PowerShell). Nenhum caminho
absoluto da máquina de ninguém: a raiz do repo sai do `$PSScriptRoot`, e a lista de mods sai do
próprio empacotador (`--listar-nomes`).

**Gerar o pacote pela linha de comando:** `python tools/pack-thunderstore.py` (ou passando nomes de
mods para empacotar só alguns; `--config Debug` para conferir sem Release buildada).
Os zips saem em `dist/` com pre-flight: sem manifest valido, README, CHANGELOG, icone 256x256 real,
DLL buildada **na configuração pedida** ou versão única ele **sai com erro sem gerar pacote quebrado**.

**Testar antes de publicar (r2modman):** `Import local mod` no perfil -> conferir que a DLL caiu em
`BepInEx/plugins/<Mod>/` -> abrir pelo "Start modded" -> conferir `<Mod> carregado.` no `LogOutput.log`.

**Publicar** — o pipeline existe e está descrito em [`PUBLICACAO.md`](PUBLICACAO.md): quem **pode**
sair é o gate versionado [`release/mods.json`](../release/mods.json) (hoje com **6** entradas, todas
com `publicar: true` e **publicadas** na leva de 01/10/2026 — BetterFont **1.0.1**, BetterStats
**1.0.1**, BetterTooltips **0.1.1**, RoguelikeDebugger **0.1.1**, RoguelikeSkillTreeVisualizer **0.2.0**,
BetterCombatText **0.1.0**); a lista tem de bater
com o `tools/pack-thunderstore.py --listar-nomes`, senão o gate **falha**), o envio é o workflow
[`.github/workflows/publish.yml`](../.github/workflows/publish.yml)
(**manual**, com aprovação num GitHub Environment) e o envio **local** continua sendo
`bash tools/publish-thunderstore.sh` (**dry-run** por padrão; só sobe com `--go`). Os dois
workflows já estão no remoto — factual verificado em 30/09/2026, ver [`CI.md`](CI.md). A versão nao pode
repetir uma ja publicada — a **PKG-2** resolveu isso: a versão tem uma fonte (o `<Version>` do
`.csproj`) e o empacotamento **recusa** pacote quando `manifest.json`, `Plugin.cs` ou `README.md` divergem dela
(ver § *Fonte única de versão*).
