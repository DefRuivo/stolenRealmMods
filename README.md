# Stolen Realm — QoL Mods (BepInEx)

Quality-of-life mods for **Stolen Realm** (Steam AppID `1330000`), loaded by **BepInEx 5**.
No mod touches the game's content, balance or files: each one is a **separate DLL** dropped into
`BepInEx\plugins\`. Nothing in `Assembly-CSharp.dll` is ever modified.

**English** · [Português (BR)](#português-br)

## Index

| | Section | |
|---|---|---|
| **EN** | [What each mod does](#what-each-mod-does) | the useful part for a player |
| | [Install with r2modman](#install-with-r2modman-recommended) | 10 minutes, no terminal |
| | [Manual install](#manual-install-without-r2modman) | without the mod manager |
| | [How to know it worked](#how-to-know-it-worked) | read the log |
| | [Uninstall](#uninstall) | nothing is left behind |
| | [FAQ](#faq) | game won't open, mod seems missing… |
| | [Mod identifiers](#mod-identifiers) | GUIDs, log names, versions |
| | [For developers: building, packaging, testing, publishing](#for-developers-building-packaging-testing-and-publishing) | from source to a release |
| **PT** | [O que cada mod faz](#o-que-cada-mod-faz-para-você) | a parte que interessa ao jogador |
| | [Instalação pelo r2modman](#instalação-pelo-r2modman-recomendado) | 10 minutos, sem terminal |
| | [Instalação manual](#instalação-manual-sem-r2modman) | sem o gerenciador |
| | [Como saber que funcionou](#como-saber-que-funcionou) | ler o log |
| | [Como desfazer](#como-desfazer-desinstalar) | nada fica para trás |
| | [Perguntas frequentes](#perguntas-frequentes) | jogo não abre, mod não aparece… |
| | [Identificadores internos](#identificadores-internos) | GUIDs, nomes no log, versões |
| | [Para quem vai mexer no código](#para-quem-vai-mexer-no-código-compilar-empacotar-testar-e-publicar) | do código até o release |
| — | [Build ritual (dev)](docs/README.md) | the full internal ritual, step by step |
| — | [Thunderstore packaging & publishing](docs/PUBLICACAO.md) | the pipeline and the human gates |
| — | [CI](docs/CI.md) | the two workflows and every check |
| — | [Environment](docs/AMBIENTE.md) | validated versions and paths |

---

# English

> Result you should end up with: **one folder per mod** inside `BepInEx\plugins\`, each with its
> DLL inside — `...\BepInEx\plugins\BetterTooltips\BetterTooltips.dll`.

## What each mod does

| Mod | What it does for you |
|---|---|
| **BetterTooltips** | Makes skill, status and item tooltips **accurate and complete**: it fixes descriptions that "lied by omission" (missing duration, stack limit, range, whether it stacks with the party…) and appends a short **explanation of how the mechanic actually works** at the end of the tooltip, in the game's own special text colour. |
| **BetterStats** | Shows your attributes as **`base (combined)`** — the raw value you invested and, in brackets, the final value with powerups, gear and skills. Works on the character sheet and on the level-up screen. It also fixes the value column alignment, which used to overflow the panel. |
| **BetterFont** | Swaps the game font for a **serif** one (Times New Roman; Georgia or Liberation Serif as fallback). The original font stays as a fallback, so icons and symbols keep rendering (no boxes). |
| **RoguelikeDebugger** | **NOT a player mod.** It is a **development tool** of ours: instead of improving the screen, it dumps internal game data into the log file (skill, item, affix, powerup and status inventories). It is used to investigate mechanics. If you just want to play, **do not install it** — it fills the log with thousands of lines. |

## Prerequisites

1. **Windows** and **Stolen Realm installed through Steam** (AppID `1330000`).
2. **r2modman** (the mod manager, which installs BepInEx for you):
   download `r2modman-Setup-x.y.z.exe` from <https://github.com/ebkr/r2modmanPlus/releases>.
3. About **10 minutes**. You do **not** need the .NET SDK, Visual Studio or a terminal.

## Install with r2modman (recommended)

1. **Install and open r2modman**. On first run it may ask about importing old profiles — you can skip.
2. **Pick the game**: click **"Select game"** and choose **Stolen Realm**.
3. **Pick the profile**: select **`Default`** (the one this project uses) or create your own.
4. **Install BepInEx**: go to the **"Online"** tab and install **`BepInExPack`** with dependencies.
   Validated version here: **BepInExPack 5.4.2305** = **BepInEx 5.4.23.5**. Skip if already installed.
5. **Click "Start modded", wait for the game to open, then CLOSE the game.** This step is what
   creates the BepInEx folders the mods need — the most common beginner mistake is skipping it.
6. **Open the profile folder**: r2modman → **Settings (gear)** → **"Browse profile folder"**.
7. **Go into `BepInEx` and then `plugins`**.
8. **Copy the mods into `plugins`** — one **folder per mod**, with the DLL **inside** it:

   ```text
   ...\BepInEx\plugins\
   ├── BetterTooltips\
   │   └── BetterTooltips.dll
   ├── BetterStats\
   │   └── BetterStats.dll
   └── BetterFont\
       └── BetterFont.dll
   ```

   Where do those DLLs come from? Either the ready-made package (see
   [Packaging](#packaging) / [Publishing](#publishing) below) or by
   compiling from source: `dotnet build -p:DeployToBepInEx=false` inside each mod folder produces
   `<Mod>\bin\Debug\netstandard2.1\<Mod>.dll`. **The flag keeps the build local** — without it the
   `DeployToBepInEx` target also installs the DLL into this machine's r2modman profile.

   ⚠️ **The DLL cannot sit loose in `plugins\`** — it must be inside the mod's folder. And because
   BepInEx scans that folder **recursively**, **never** keep DLL copies/backups
   (`*.dll.bak`, `*.disabled`, old copies) inside `plugins\`.
9. **Always launch the game from r2modman**, with the **"Start modded"** button. Launching from
   Steam does **not** inject the mods — the game opens normally, with no mods loaded.

## Manual install (without r2modman)

1. Download **BepInEx 5 `win_x64`** (5.4.23.5 or the latest 5.4.23.x) from
   <https://github.com/BepInEx/BepInEx/releases>.
2. **Extract the whole zip into the game folder** (the one with `Stolen Realm.exe`). A
   **`winhttp.dll`** must appear next to it.
3. **Launch the game through Steam once and close it.** This creates `BepInEx\` and
   `BepInEx\plugins\`.
4. **Copy the mod folders** into `...\steamapps\common\Stolen Realm\BepInEx\plugins\` —
   again, one folder per mod with the DLL inside.
5. **Launch the game normally.** Done.

> ⚠️ **Backups:** **NEVER** put DLL backups inside `plugins\` (not `.bak`, not `.dll.old`, not a
> `backup` subfolder). BepInEx scans `plugins\` recursively and tries to load **every** `.dll` it
> finds as a mod — the backup loads too, the same fixes are applied twice and things break.
> Keep backups **outside** `plugins\`.

> ⚠️ **Never modify `Assembly-CSharp.dll`** (in `Stolen Realm_Data\Managed\`). Mods are always a
> separate DLL: touching the game's DLL breaks the game, breaks the other mods and is undone by the
> next Steam update.

## How to know it worked

BepInEx writes everything to a file called **`LogOutput.log`**:

- **r2modman install** — in the profile's `BepInEx` folder:
  `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\LogOutput.log`
- **manual install** — in the game folder: `...\BepInEx\LogOutput.log`

Open it with Notepad and search for `carregado.` — there must be **one line per installed mod**:

```text
[Message:   BepInEx] BepInEx 5.4.23.5 - Stolen Realm
[Info   :   BepInEx] Loading [Better Font 1.0.0]
[Info   :Better Font] Better Font carregado.
[Info   :   BepInEx] Loading [Better Tooltips 0.1.0]
[Info   :Better Tooltips] Better Tooltips carregado.
[Message:   BepInEx] Chainloader startup complete
```

Read it like this: the `Loading [...]` line means BepInEx **found** the DLL; the `... carregado.`
line means the mod **started working**. If the first appears and the second does not, something
failed at load time (and the reason shows up right after it, in the same or the following lines).

In game: the font becomes serif; tooltips get an extra line at the end in a different colour; the
character sheet shows `12 (17)` instead of a single number.

## Uninstall

Nothing in the game is changed, so uninstalling is just deleting files.

1. Close the game.
2. Delete the mod's folder inside `BepInEx\plugins\<ModName>\` (or untick it in r2modman's
   **"Installed"** tab — unticking is reversible, deleting is not). Each mod is independent:
   removing one **does not affect the others**.
3. To remove everything (100% clean game), also delete the whole `BepInEx\` folder plus
   `winhttp.dll` and `doorstop_config.ini` from the game folder. No need to reinstall or verify
   files through Steam.

The `BepInEx\config\` folder keeps mod settings (e.g. `com.gumatos.roguelikeqol.cfg`). It is
harmless and only read if the mod is installed.

## FAQ

**1. The game no longer opens / opens and closes immediately.**
Usually wrong or incomplete BepInEx (manual installs must use the **`win_x64` 5.x** package).
Fix: delete `BepInEx\`, `winhttp.dll` and `doorstop_config.ini` from the game folder — the game
opens again — and redo it with r2modman. With r2modman, untick the mods and hit **"Start vanilla"**
to confirm the game opens without mods, then re-enable them one at a time.

**2. The game opens but no mod shows up.**
Check, in order: the path must be exactly `...\BepInEx\plugins\<ModName>\<ModName>.dll` (a
loose DLL in `plugins\` is mistake #1); you must launch through **"Start modded"**; look for the
`... carregado.` line in the log.
And if you had the old `BetterTexts`, delete that folder: it was renamed to **BetterTooltips**,
and having both applies the same fixes twice.

**3. How do I go back to vanilla?** Delete the mod folders inside `BepInEx\plugins\`. Since no
game file is modified, there is nothing else to undo.

**4. Do I always have to launch through r2modman?** Yes, if you installed that way: it is what
performs the "modded" startup. Launching from Steam runs the game without the mods, silently.

**5. Can I use it together with other Thunderstore mods?** Yes — each mod is an independent DLL and
BepInEx loads them all. Just avoid installing two mods that fix the same thing, and check the log.

**6. Can I play with RoguelikeDebugger?** Not worth it: it is a development tool, it draws nothing
on screen and floods `LogOutput.log`. Only install it to investigate mechanics.

## Mod identifiers

Useful to confirm what loaded in the log:

| Mod | GUID (BepInEx internal name) | Name in the log | Version |
|---|---|---|---|
| BetterTooltips | `com.gumatos.bettertooltips` | `Better Tooltips` | 0.1.0 |
| BetterStats | `com.gumatos.betterstats` | `Better Stats` | 1.0.0 |
| BetterFont | `com.gumatos.betterfont` | `Better Font` | 1.0.0 |
| RoguelikeDebugger | `com.gumatos.roguelikedebugger` | `Roguelike Debugger` | 0.1.0 |

---

## For developers: building, packaging, testing and publishing

This part is for someone who opens the repository without knowing anything about it. It is the
short version — every step here exists because of a real incident, and the full ritual (with the
reason for each step) is in [docs/README.md](docs/README.md); the pipeline is in
[docs/CI.md](docs/CI.md) and [docs/PUBLICACAO.md](docs/PUBLICACAO.md).

**What you need:** Windows, the game installed through Steam, the **.NET SDK 6** and **Python 3**
(measured here on 30/09/2026: `dotnet --version` → `6.0.428`, `python --version` → `3.14.7`), plus
a `lib/` folder at the repository root with the *game's* assemblies (`Assembly-CSharp.dll`,
`BepInEx.dll`, `UnityEngine*`, `0Harmony.dll`, `Sirenix.*`, 15 DLLs in total). That folder is
**gitignored** and holds game-owned files, so it is never committed — see
[docs/AMBIENTE.md](docs/AMBIENTE.md) for the validated versions and paths.

> **Close the game before building.** A build **without** `-p:DeployToBepInEx=false` runs the
> `DeployToBepInEx` target, which copies the DLL into the r2modman profile; that copy fails while
> the file is in use.

### Building

```bash
cd C:/dev/stolen-realm
LC_ALL=C dotnet build BetterTooltips/BetterTooltips.csproj -p:DeployToBepInEx=false --nologo -v q -clp:ErrorsOnly
```

- builds **Debug**: the DLL goes to `<Mod>/bin/Debug/netstandard2.1/<Mod>.dll`. The
  `-p:DeployToBepInEx=false` is what keeps this build **local** — **without it the
  `DeployToBepInEx` target runs and copies the DLL to `...\BepInEx\plugins\<Mod>\<Mod>.dll` in the
  r2modman profile**, i.e. installs it on the machine that built;
- `-clp:ErrorsOnly` prints **nothing** when it works — any line is a problem, so stop there;
- swap the project for the mod you touched: `BetterStats`, `BetterFont`,
  `RoguelikeDebugger` or `RoguelikeSkillTreeVisualizer` (all 6 use the same layout).

To build **Release** (what packages are made of) *without* touching the installed DLL:

```bash
LC_ALL=C dotnet build BetterTooltips/BetterTooltips.csproj -c Release -p:DeployToBepInEx=false --nologo -v q -clp:ErrorsOnly
```

The DLL comes out in `<Mod>/bin/Release/netstandard2.1/<Mod>.dll`. The flag
`-p:DeployToBepInEx=false` is **mandatory** whenever the mod is installed and under test:
without it, the build overwrites the DLL that is being tested in the profile.

### Packaging

Two packages, for two audiences:

| Audience | Command | Output |
|---|---|---|
| **friends** (no account, no terminal) | `bash tools/pack-for-friends.sh` | `dist/StolenRealm-Mods-<date>.zip` (see [docs/MODS-PARA-AMIGOS.md](docs/MODS-PARA-AMIGOS.md)) |
| **Thunderstore / r2modman** | `python tools/pack-thunderstore.py [Mod]`, or `.\scripts\package.ps1 <Mod>`, or `bash tools/publish-thunderstore.sh` | `dist/gumatos-<Mod>-<version>.zip` |

Both build in **Release** with `-p:DeployToBepInEx=false`, so making a package never overwrites the
DLL installed in the profile. `python tools/pack-thunderstore.py --listar-nomes` prints the mods the
packager knows (measured 30/09/2026, in this order): `BetterCombatText`, `BetterFont`, `BetterStats`,
`BetterTooltips`, `RoguelikeDebugger`, `RoguelikeSkillTreeVisualizer` — **6 mods**
(the count is the one the packager returns; the first is the newest mod).

The Thunderstore zip is **4 files at the package root** (`manifest.json`, `README.md`,
`CHANGELOG.md`, `icon.png`) plus `plugins/<Mod>/<Mod>.dll`. The packager has a **pre-flight that
aborts instead of producing a broken zip**: missing manifest/README/CHANGELOG, an icon that is not
a real 256×256 PNG, a DLL that was not built in the requested configuration, or a version that
disagrees between `.csproj`, `manifest.json` and `Plugin.cs`.

The version has **one source** — the `<Version>` in `<Mod>/<Mod>.csproj` — and two mirrors checked
automatically. To bump it: edit the `.csproj`, then run **once**
`python tools/pack-thunderstore.py --sincronizar-versao <Mod>` (it rewrites the two mirrors only
when they disagree) and package.

### Testing

Minimum before calling anything done:

```bash
bash tools/release-check.sh
```

It runs the automatable steps in order — secrets, build with 0 errors, fix keys, duplicate keys,
redundant notes, shared key, one game cycle reading the log — and then prints the human step (what
only an eye in game can check). At the end it says **APROVADO** or **REPROVADO**, naming what failed.

The rule read straight from the log: after launching the game through the profile, `LogOutput.log`
must have one `... carregado.` line per installed mod and **zero** `ArgumentException`,
`TypeInitializationException` and `[Error` lines.

The same checks run in CI on every `push`/`pull_request` to `main`
([`.github/workflows/validate.yml`](.github/workflows/validate.yml), described in
[docs/CI.md](docs/CI.md)). A red check there is the same gate as the local `release-check.sh`.

### Publishing

The Thunderstore version is **immutable**: after it is accepted nothing can be edited, so any change
— even README text — requires a **new version number**. Nothing is published by guessing:

1. **[`release/mods.json`](release/mods.json)** is the versioned gate. A mod with `"publicar": false`
   is **never** sent, not even when you pick it by hand (the run fails on purpose and shows the
   `motivo`). On 30/09/2026 all **6** mods were `false` and the `team` field was empty on purpose —
   so the pipeline fails *before* touching anything.
2. **A GitHub Environment with required reviewers** is the human gate: the approval is a click in
   *Review deployments*, not a label or a variable.

Two ways to actually send:

- **Local — the simplest today:** `bash tools/publish-thunderstore.sh` is a **dry-run by default**
  and only uploads with `--go`. It runs the secret gate and the whole `release-check.sh` first, and
  refuses a token file that lives inside the repository.
- **GitHub Actions:** [`.github/workflows/publish.yml`](.github/workflows/publish.yml) — manual
  dispatch, with a `mod` input, the approval gate and a pre-flight that refuses a repeated version.
  It does **not** build: it ships the `.zip` produced on the development machine.

The step-by-step, the platform rules and the known traps are in
[docs/PUBLICACAO.md](docs/PUBLICACAO.md).

---

# Português (BR)

## O que cada mod faz para você

| Mod | O que ele faz de útil para o jogador |
|---|---|
| **BetterTooltips** | Deixa os tooltips de skills, status e itens **corretos e completos**: conserta descrições que omitiam informação (faltava duração, número de stacks, alcance, se acumula com a party…) e acrescenta, no fim do tooltip, uma **explicação curta de como a mecânica realmente funciona**, na cor de texto especial do próprio jogo. |
| **BetterStats** | Mostra seus atributos no formato **`base (combinado)`** — o valor puro que você investiu e, entre parênteses, o valor final já com powerups, equipamento e skills. Vale para a ficha de personagem e para a tela de level up. Também corrige o alinhamento da coluna de valores, que vazava para fora do painel. |
| **BetterFont** | Troca a fonte do jogo por uma **serifada** (Times New Roman; se não existir, Georgia ou Liberation Serif). A fonte original fica como reserva, então ícones e símbolos continuam aparecendo (sem quadradinhos). |
| **RoguelikeDebugger** | **NÃO é um mod de jogador.** É uma **ferramenta de desenvolvimento** nossa: em vez de melhorar a tela, ela despeja dados internos do jogo no arquivo de log (inventários de skills, itens base, afixos, powerups e status). Serve para investigar mecânicas. Se você só quer jogar, **não instale** — ele deixa o log com milhares de linhas. |

Nenhum mod altera `Assembly-CSharp.dll` (o arquivo do jogo): nada nos arquivos do jogo é
modificado, substituído ou apagado. As únicas coisas gravadas são a pasta `BepInEx\` e o
arquivo de log/configuração dela, do lado de fora dos arquivos do jogo.

> **Ferramenta interna (não instale):** existe também o projeto `ReloadProbe` (só na máquina de desenvolvimento, FORA do
> repositório), um
> *harness* de teste que vai para `BepInEx\scripts` para validar recarga de código durante o
> desenvolvimento. Ele não é mod de jogador.

Identificadores internos (úteis para conferir no log):

| Mod | GUID (nome interno do BepInEx) | Nome no log | Versão |
|---|---|---|---|
| BetterTooltips | `com.gumatos.bettertooltips` | `Better Tooltips` | 0.1.0 |
| BetterStats | `com.gumatos.betterstats` | `Better Stats` | 1.0.0 |
| BetterFont | `com.gumatos.betterfont` | `Better Font` | 1.0.0 |
| RoguelikeDebugger | `com.gumatos.roguelikedebugger` | `Roguelike Debugger` | 0.1.0 |

---

## Pré-requisitos

1. **Windows** e o **Stolen Realm instalado pela Steam** (AppID `1330000`).
   - Em muitos PCs o jogo fica em `...\steamapps\common\Stolen Realm\` — a pasta onde está o
     `Stolen Realm.exe`.
2. **r2modman** (o gerenciador de mods, que é quem instala o BepInEx para você):
   baixe o instalador `r2modman-Setup-x.y.z.exe` em
   <https://github.com/ebkr/r2modmanPlus/releases>.
3. Uns **10 minutos** e nada mais. Você **não** precisa de .NET SDK, Visual Studio nem terminal.

Se você preferir não usar o r2modman, existe o [caminho manual](#instalação-manual-sem-r2modman).

---

## Instalação pelo r2modman (recomendado)

> Resultado final esperado: uma **pasta por mod** dentro de `BepInEx\plugins\`, com a DLL dentro.
> `...\BepInEx\plugins\BetterTooltips\BetterTooltips.dll`

1. **Instale e abra o r2modman** (o instalador baixado no pré-requisito 2). Na primeira execução
   ele pergunta se você quer importar perfis antigos — pode pular.

2. **Escolha o jogo**: clique em **"Select game"** e escolha **Stolen Realm** na lista.

   ![Escolhendo o jogo Stolen Realm no r2modman](docs/img/r2modman-escolher-jogo.png)

3. **Escolha o perfil**: selecione o perfil **`Default`** (é o que este projeto usa) ou crie um
   com qualquer nome, ex.: `MeusMods`.

4. **Instale o BepInEx**: vá na aba **"Online"**, pesquise por **`BepInExPack`**
   (pacote `BepInEx-BepInExPack`), clique nele e depois em **"Download with dependencies"**.
   - Se o perfil já tiver o BepInEx instalado, pule este passo.
   - Versão usada e validada neste projeto: **BepInExPack 5.4.2305** = **BepInEx 5.4.23.5**.

   ![Instalando o BepInExPack na aba Online](docs/img/r2modman-instalar-bepinex.png)

5. **Clique em "Start modded" e espere o jogo abrir; depois FECHE o jogo.**
   Esse passo é o que cria as pastas do BepInEx que os mods vão usar. É aqui que a maioria dos
   leigos trava: sem abrir o jogo uma vez pelo r2modman, a pasta `BepInEx\plugins` pode nem existir.

   ![Botão Start modded destacado no r2modman](docs/img/r2modman-start-modded.png)

6. **Abra a pasta do perfil**: no r2modman, clique na **engrenagem (Settings)** e depois em
   **"Browse profile folder"**. Vai abrir a pasta do perfil no Explorer.

   ![Settings → Browse profile folder](docs/img/r2modman-browse-profile-folder.png)

7. **Entre na pasta `BepInEx` e depois em `plugins`**.

8. **Copie os mods para dentro de `plugins`** — uma **pasta por mod**, com a DLL **dentro** dela:

   ```text
   ...\BepInEx\plugins\
   ├── BetterTooltips\
   │   └── BetterTooltips.dll
   ├── BetterStats\
   │   └── BetterStats.dll
   └── BetterFont\
       └── BetterFont.dll
   ```

   De onde vem essas DLLs? Duas opções:
   - **Pacote pronto** (3 mods de jogador): o zip `dist\StolenRealm-Mods-<data>.zip`, gerado no
     repositório com `bash tools/pack-for-friends.sh`. Dentro dele já vem a pasta `BepInEx\plugins`
     com a estrutura acima;
   - **Compilando do código** (quem for mexer no código): `dotnet build -p:DeployToBepInEx=false`
     dentro da pasta de cada mod gera `<Mod>\bin\Debug\netstandard2.1\<Mod>.dll`. **A flag mantém o
     build local** — sem ela o target `DeployToBepInEx` também instala a DLL no perfil do r2modman
     desta máquina.

   ⚠️ **A DLL não pode ficar solta em `plugins\`** — ela tem que estar dentro da pasta do mod.
   E, como o BepInEx varre a pasta **recursivamente**, **nunca** guarde cópias/backups de DLL
   (`BetterTooltips.dll.bak`, `*.disabled`, cópias antigas) dentro de `plugins\`.

   ![Pasta plugins com uma pasta por mod](docs/img/bepinex-plugins-estrutura.png)

9. **Sempre inicie o jogo pelo r2modman**, no botão **"Start modded"**. Abrir o jogo direto pela
   Steam **não** injeta os mods — pode até abrir normal, mas sem mod nenhum carregado.

---

## Instalação manual (sem r2modman)

Serve para quem não quer o gerenciador. O BepInEx passa a ficar **na própria pasta do jogo**.

1. Baixe o **BepInEx 5, versão `win_x64`** (5.4.23.5 ou o 5.4.23.x mais recente) em
   <https://github.com/BepInEx/BepInEx/releases> — arquivo tipo `BepInEx_win_x64_5.4.23.x.zip`.

   ![Release do BepInEx: escolher o arquivo win_x64](docs/img/bepinex-release-win-x64.png)

2. **Extraia todo o conteúdo do zip dentro da pasta do jogo**, em
   `...\steamapps\common\Stolen Realm\` (a pasta onde está o `Stolen Realm.exe`).
   Deve aparecer um arquivo **`winhttp.dll`** ao lado do `Stolen Realm.exe`.

   ![winhttp.dll ao lado de Stolen Realm.exe](docs/img/manual-winhttp-na-pasta-do-jogo.png)

3. **Abra o jogo pela Steam uma vez e feche.** Isso cria as pastas `BepInEx\` e `BepInEx\plugins\`.

4. **Copie as pastas dos mods** para:

   ```text
   ...\steamapps\common\Stolen Realm\BepInEx\plugins\
   ```

   Ou seja, o mesmo formato do caminho com r2modman: **uma pasta por mod, com a DLL dentro**.

   ```text
   ...\BepInEx\plugins\BetterTooltips\BetterTooltips.dll
   ...\BepInEx\plugins\BetterStats\BetterStats.dll
   ...\BepInEx\plugins\BetterFont\BetterFont.dll
   ```

5. **Abra o jogo normalmente** (pela Steam). Pronto.

> ⚠️ **Atenção com backups.** **NUNCA** coloque backup de DLL dentro de `plugins\`
> (nem `.bak`, nem `.dll.old`, nem uma pasta `backup` lá dentro). O BepInEx **varre a pasta
> `plugins\` recursivamente** e tenta carregar **todo** arquivo `.dll` que encontrar como se fosse
> um mod — o backup é carregado junto e as correções são aplicadas duas vezes, dando erro e
> comportamento estranho. Guarde backups **fora** de `plugins\`, por exemplo em
> `Documentos\backup-mods\`.

> ⚠️ **Nunca modifique o `Assembly-CSharp.dll`** (o arquivo do jogo, em
> `Stolen Realm_Data\Managed\`). Os mods são sempre DLL separada: qualquer alteração na DLL do jogo
> quebra o jogo, quebra os outros mods e é perdida na próxima atualização do Steam.

> Neste PC, por exemplo, a pasta do jogo é `E:\SteamLibrary\steamapps\common\Stolen Realm\`
> (o caminho varia conforme a biblioteca Steam que você escolheu na instalação).

---

## Como saber que funcionou

### 1. O arquivo de log

O BepInEx escreve tudo num arquivo chamado **`LogOutput.log`**:

- **Instalação pelo r2modman** — fica na pasta `BepInEx` do **perfil** do r2modman:

  ```text
  %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\LogOutput.log
  ```

  (`%APPDATA%` = `C:\Users\<seu-usuário>\AppData\Roaming`; se o seu perfil tem outro nome, troque
  `Default`.)

- **Instalação manual** — fica na pasta do jogo:

  ```text
  ...\steamapps\common\Stolen Realm\BepInEx\LogOutput.log
  ```

### 2. O que deve aparecer no log

Abra o arquivo com o Bloco de Notas e procure por `carregado.`. Deve haver **uma linha para cada
mod instalado** — este é o formato exato:

```text
[Message:   BepInEx] BepInEx 5.4.23.5 - Stolen Realm
[Info   :   BepInEx] Loading [Better Font 1.0.0]
[Info   :Better Font] Better Font carregado.
[Info   :   BepInEx] Loading [Better Stats 1.0.0]
[Info   :Better Stats] Better Stats carregado.
[Info   :   BepInEx] Loading [Better Tooltips 0.1.0]
[Info   :Better Tooltips] Better Tooltips carregado.
[Message:   BepInEx] Chainloader startup complete
```

Leia assim: a linha `Loading [...]` diz que o BepInEx **achou** a DLL; a linha `... carregado.` diz
que o mod **entrou em funcionamento**. Se a primeira aparece e a segunda não, algo deu errado no
carregamento (e o motivo aparece logo depois, na mesma linha ou nas seguintes).

![LogOutput.log com as linhas "carregado."](docs/img/logoutput-carregado.png)

### 3. Dentro do jogo

- **BetterFont**: o menu e todos os textos ficam com a fonte **serifada** (estilo Times New Roman).
- **BetterTooltips**: passe o mouse numa skill/status — no fim da descrição aparece uma **linha
  extra** explicando a mecânica, em cor diferente do corpo do texto.
- **BetterStats**: na ficha de personagem e no level up os atributos aparecem como **`12 (17)`**
  (base e combinado) em vez de só um número.

![Tooltips antes e depois](docs/img/ingame-tooltips-antes-depois.png)

---

## Como desfazer (desinstalar)

Nada no jogo original é alterado, então desinstalar é só apagar arquivos.

**Se você instalou pelo r2modman:**

1. Feche o jogo.
2. No r2modman, na aba **"Installed"**, **desmarque** o mod que quer tirar (ou apague a pasta dele)
   — desmarcar é reversível, apagar não;
3. Ou, direto no disco: apague a pasta do mod dentro de
   `...\BepInEx\plugins\<NomeDoMod>\` (ex.: apague `plugins\BetterFont\`).
   Cada mod é independente: tirar um **não afeta os outros**.

**Se você instalou manualmente:**

1. Feche o jogo.
2. Para tirar um mod: apague a pasta dele em `...\BepInEx\plugins\<NomeDoMod>\`.
3. Para **tirar tudo** (voltar ao jogo 100% limpo): apague também a pasta `BepInEx\` inteira e os
   arquivos que o BepInEx colocou na pasta do jogo (`winhttp.dll` e `doorstop_config.ini`).
   Não é preciso reinstalar nem revalidar nada no Steam para o jogo voltar a funcionar.
4. O jogo não precisa ser reinstalado em nenhum caso.

**O que pode sobrar:** a pasta `BepInEx\config\` guarda as configurações dos mods (ex.:
`com.gumatos.roguelikeqol.cfg`). Ela é inofensiva e só é lida se o mod estiver instalado. Se
apagar e reinstalar, os mods voltam no padrão.

---

## Perguntas frequentes

**1. O jogo não abre mais / abre e fecha sozinho.**
Na maioria dos casos é BepInEx errado ou incompleto (na instalação manual, tem que ser o pacote
**`win_x64` da versão 5.x** — o x86 é para outro tipo de jogo). Como recuperar:
- instalação manual: apague a pasta `BepInEx\`, o `winhttp.dll` e o `doorstop_config.ini` da pasta
  do jogo (o jogo volta a abrir normalmente) e refaça pelo
  [passo a passo do r2modman](#instalação-pelo-r2modman-recomendado);
- instalação pelo r2modman: no r2modman, desmarque os mods, clique em **"Start vanilla"** para
  confirmar que o jogo abre sem mods, e depois religue um mod por vez para achar o culpado;
- se o jogo já abria torto antes dos mods, atualize/valide os arquivos pelo Steam.

**2. O jogo abre, mas nenhum mod aparece / nada mudou.**
Confira na ordem:
- **O mod não está no lugar certo.** O caminho final tem que ser exatamente
  `...\BepInEx\plugins\<NomeDoMod>\<NomeDoMod>.dll` — uma **pasta por mod**, com a DLL **dentro**.
  DLL solta em `plugins\` costuma ser o erro nº 1.
- **Você abriu o jogo pela Steam em vez do r2modman.** Na instalação gerenciada, os mods só são
  injetados quando o jogo é iniciado pelo botão **"Start modded"** do r2modman.
- **O mod carregou?** Abra o `LogOutput.log` e procure a linha `... carregado.`
  (veja [Como saber que funcionou](#como-saber-que-funcionou)). Sem essa linha, o BepInEx não
  encontrou/carregou a DLL.
- **Você tinha a versão antiga do mod de textos.** O `BetterTexts` mudou de nome para
  `BetterTooltips`: se a pasta `BetterTexts` ainda estiver em `plugins\`, **apague-a** antes de usar
  a nova — com as duas instaladas, as mesmas correções são aplicadas duas vezes.

**3. Como voltar ao original (jogo sem mod nenhum)?**
Apague a pasta do mod (ou todas as pastas de mods) dentro de `BepInEx\plugins\`. Se quiser tirar
o BepInEx também, veja [Como desfazer](#como-desfazer-desinstalar). Como nenhum arquivo do jogo é
modificado, não existe "desfazer" além de apagar as pastas de mod — o jogo volta sozinho ao normal.

**4. Preciso abrir o jogo sempre pelo r2modman?**
Sim, se você instalou pelo r2modman: é ele que faz a inicialização "modded". Se você abrir pela
Steam, o jogo roda sem os mods (e sem aviso).

**5. Posso usar junto com outros mods da Thunderstore?**
Pode. Cada mod é uma DLL independente e o BepInEx carrega todas. Só cuide de dois pontos: não
instalar **dois mods que consertam a mesma coisa** (ver o caso do `BetterTexts` acima) e conferir
no log se todos carregaram.

**6. Posso usar o RoguelikeDebugger para jogar?**
Não vale a pena: ele é ferramenta de desenvolvimento, não mostra nada na tela e enche o
`LogOutput.log` de milhares de linhas. Só instale se for investigar mecânicas junto com quem
mantém o projeto.

## Identificadores internos

Útil para conferir no log o que carregou:

| Mod | GUID (nome interno do BepInEx) | Nome no log | Versão |
|---|---|---|---|
| BetterTooltips | `com.gumatos.bettertooltips` | `Better Tooltips` | 0.1.0 |
| BetterStats | `com.gumatos.betterstats` | `Better Stats` | 1.0.0 |
| BetterFont | `com.gumatos.betterfont` | `Better Font` | 1.0.0 |
| RoguelikeDebugger | `com.gumatos.roguelikedebugger` | `Roguelike Debugger` | 0.1.0 |

---

## Para quem vai mexer no código: compilar, empacotar, testar e publicar

Esta é a versão curta, para quem chega no repositório sem saber nada. Cada passo existe por causa de
um incidente real; o ritual completo (com o porquê de cada passo) está em
[docs/README.md](docs/README.md), e o pipeline em [docs/CI.md](docs/CI.md) e
[docs/PUBLICACAO.md](docs/PUBLICACAO.md).

**O que você precisa:** Windows, o jogo instalado pela Steam, o **.NET SDK 6** e o **Python 3**
(medido aqui em 30/09/2026: `dotnet --version` → `6.0.428`, `python --version` → `3.14.7`), além da
pasta `lib/` na raiz com as *assemblies do jogo* (`Assembly-CSharp.dll`, `BepInEx.dll`,
`UnityEngine*`, `0Harmony.dll`, `Sirenix.*` — 15 DLLs). Essa pasta é **gitignored** (arquivo do jogo
nunca entra no repositório) — versões e caminhos validados em [docs/AMBIENTE.md](docs/AMBIENTE.md).

> **Feche o jogo antes de compilar.** Um build **sem** `-p:DeployToBepInEx=false` roda o target
> `DeployToBepInEx`, que copia a DLL para o perfil do r2modman; essa cópia falha com o arquivo em
> uso.

### Compilando

```bash
cd C:/dev/stolen-realm
LC_ALL=C dotnet build BetterTooltips/BetterTooltips.csproj -p:DeployToBepInEx=false --nologo -v q -clp:ErrorsOnly
```

- compila em **Debug**: a DLL sai em `<Mod>/bin/Debug/netstandard2.1/<Mod>.dll`. A
  `-p:DeployToBepInEx=false` é o que mantém este build **local** — **sem ela o target
  `DeployToBepInEx` roda e copia a DLL para `...\BepInEx\plugins\<Mod>\<Mod>.dll` no perfil do
  r2modman**, ou seja, instala na máquina que compilou;
- `-clp:ErrorsOnly` não imprime **nada** quando dá certo — qualquer linha é problema, pare aí;
- troque o projeto pelo mod que você mexeu: `BetterStats`, `BetterFont`,
  `RoguelikeDebugger` ou `RoguelikeSkillTreeVisualizer` (os 6 usam a mesma estrutura).

Para compilar em **Release** (de onde saem os pacotes) **sem** tocar na DLL instalada:

```bash
LC_ALL=C dotnet build BetterTooltips/BetterTooltips.csproj -c Release -p:DeployToBepInEx=false --nologo -v q -clp:ErrorsOnly
```

A DLL sai em `<Mod>/bin/Release/netstandard2.1/<Mod>.dll`. A flag `-p:DeployToBepInEx=false` é
**obrigatória** quando o mod está instalado e em teste: sem ela o build sobrescreve a DLL que está
sendo testada no perfil.

### Empacotando

Dois pacotes, para dois públicos:

| Público | Comando | Saída |
|---|---|---|
| **amigos** (sem conta e sem terminal) | `bash tools/pack-for-friends.sh` | `dist/StolenRealm-Mods-<data>.zip` (ver [docs/MODS-PARA-AMIGOS.md](docs/MODS-PARA-AMIGOS.md)) |
| **Thunderstore / r2modman** | `python tools/pack-thunderstore.py [Mod]`, ou `.\scripts\package.ps1 <Mod>`, ou `bash tools/publish-thunderstore.sh` | `dist/gumatos-<Mod>-<versao>.zip` |

Os dois compilam em **Release** com `-p:DeployToBepInEx=false`, então gerar pacote **nunca**
sobrescreve a DLL do perfil. `python tools/pack-thunderstore.py --listar-nomes` lista os mods que o
empacotador conhece (medido em 30/09/2026, nesta ordem): `BetterCombatText`, `BetterFont`,
`BetterStats`, `BetterTooltips`, `RoguelikeDebugger`,
`RoguelikeSkillTreeVisualizer` — **6 mods** (a contagem é a que o empacotador devolve; o primeiro
é o mod mais novo).

O zip do Thunderstore são **4 arquivos na raiz do pacote** (`manifest.json`, `README.md`,
`CHANGELOG.md`, `icon.png`) mais `plugins/<Mod>/<Mod>.dll`. O empacotador tem um **pre-flight que
aborta em vez de gerar zip quebrado**: falta de manifest/README/CHANGELOG, ícone que não é PNG
256×256 de verdade, DLL de configuração errada ou versão divergente entre `.csproj`,
`manifest.json` e `Plugin.cs`.

A versão tem **uma fonte** — o `<Version>` do `<Mod>/<Mod>.csproj` — e dois espelhos conferidos
automaticamente. Para subir: edite o `.csproj` e rode **uma** vez
`python tools/pack-thunderstore.py --sincronizar-versao <Mod>` (ele reescreve os espelhos só quando
divergem) e empacote.

### Testando

Mínimo antes de considerar pronto:

```bash
bash tools/release-check.sh
```

Ele roda os passos automatizáveis na ordem — segredos, build com 0 erros, chaves, duplicadas, notas,
chave compartilhada, um ciclo do jogo lendo o log — e depois imprime o passo humano (o que só um
olho em jogo confere). No fim diz **APROVADO** ou **REPROVADO**, apontando o que falhou.

A regra lida direto do log: depois de abrir o jogo pelo perfil, o `LogOutput.log` tem de ter uma
linha `... carregado.` por mod instalado e **zero** `ArgumentException`,
`TypeInitializationException` e linhas `[Error`.

Os mesmos checks rodam no CI a cada `push`/`pull_request` na `main`
([`.github/workflows/validate.yml`](.github/workflows/validate.yml), descrito em
[docs/CI.md](docs/CI.md)). Um check vermelho lá é a mesma trava do `release-check.sh` local.

### Publicando

A versão na Thunderstore é **imutável**: depois de aceita não se edita nada, então qualquer mudança
— até texto de README — exige uma **versão nova**. Nada é publicado por adivinhação:

1. **[`release/mods.json`](release/mods.json)** é o gate versionado. Um mod com `"publicar": false`
   **nunca** é enviado, nem escolhido a dedo no disparo (o run falha de propósito e mostra o
   `motivo`). Em 30/09/2026 os **6** mods estavam `false` e o campo `team` vazio de propósito — por
   isso o pipeline falha *antes* de tocar em qualquer coisa.
2. **Um GitHub Environment com revisores obrigatórios** é o gate humano: a aprovação é um clique em
   *Review deployments*, não é label nem variável de ambiente.

Dois caminhos para enviar de verdade:

- **Local — o mais simples hoje:** `bash tools/publish-thunderstore.sh` é **dry-run por padrão** e só
  sobe com `--go`. Ele roda a trava de segredo e o `release-check.sh` inteiro antes, e recusa token
  que esteja dentro do repositório.
- **GitHub Actions:** [`.github/workflows/publish.yml`](.github/workflows/publish.yml) — disparo
  manual, com input de `mod`, o gate de aprovação e um pre-flight que recusa versão repetida. Ele
  **não** compila: transporta o `.zip` gerado na máquina de desenvolvimento.

O passo a passo, as regras da plataforma e as armadilhas estão em
[docs/PUBLICACAO.md](docs/PUBLICACAO.md).

---

*Projeto de mods feito pela comunidade; não é afiliado aos desenvolvedores do Stolen Realm.
Jogo: [Stolen Realm](https://store.steampowered.com/app/1330000/) (Steam AppID 1330000).*
