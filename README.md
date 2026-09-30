# Stolen Realm — Mods de QoL (BepInEx)

Mods de **qualidade de vida (QoL)** para o jogo **Stolen Realm** (Steam, AppID `1330000`),
carregados pelo **BepInEx 5**. Nenhum mod mexe no conteúdo, no balanceamento ou nos arquivos
originais do jogo: cada um é uma **DLL separada**, colocada em `BepInEx\plugins\`.

Se você nunca instalou um mod na vida, siga o **[passo a passo com o r2modman](#instalação-pelo-r2modman-recomendado)** —
são 10 minutos e você não precisa saber programar nem abrir terminal.

---

## O que cada mod faz para você

| Mod | O que ele faz de útil para o jogador |
|---|---|
| **BetterTooltips** | Deixa os tooltips de skills, status e itens **corretos e completos**: conserta descrições que "mentiam por omissão" (faltava duração, número de stacks, alcance, se acumula com a party…) e acrescenta, no fim do tooltip, uma **explicação curta de como a mecânica realmente funciona**, na cor de texto especial do próprio jogo. |
| **BetterStats** | Mostra seus atributos no formato **`base (combinado)`** — o valor puro que você investiu e, entre parênteses, o valor final já com powerups, equipamento e skills. Vale para a ficha de personagem e para a tela de level up. Também corrige o alinhamento da coluna de valores, que vazava para fora do painel. |
| **BetterFont** | Troca a fonte do jogo por uma **serifada** (Times New Roman; se não existir, Georgia ou Liberation Serif). A fonte original fica como reserva, então ícones e símbolos continuam aparecendo (sem quadradinhos). |
| **RoguelikeQoL** | Mostra um **HUD no canto superior esquerdo** com os modificadores da run em andamento: **Treasure Find**, **Gold Find** e o **Exp Mod** da batalha atual, somados de toda a party. Vem **desligado por padrão** — veja [como ligar](#perguntas-frequentes). |
| **RoguelikeDebugger** | **NÃO é um mod de jogador.** É uma **ferramenta de desenvolvimento** nossa: em vez de melhorar a tela, ela despeja dados internos do jogo no arquivo de log (inventários de skills, itens base, afixos, powerups e status). Serve para investigar mecânicas. Se você só quer jogar, **não instale** — ele deixa o log com milhares de linhas. |

Nenhum mod altera `Assembly-CSharp.dll` (o arquivo do jogo): nada nos arquivos do jogo é
modificado, substituído ou apagado. As únicas coisas gravadas são a pasta `BepInEx\` e o
arquivo de log/configuração dela, do lado de fora dos arquivos do jogo.

> **Ferramenta interna (não instale):** existe no repositório também o projeto `ReloadProbe`, um
> *harness* de teste que vai para `BepInEx\scripts` para validar recarga de código durante o
> desenvolvimento. Ele não é mod de jogador.

Identificadores internos (úteis para conferir no log):

| Mod | GUID (nome interno do BepInEx) | Nome no log | Versão |
|---|---|---|---|
| BetterTooltips | `com.gumatos.bettertooltips` | `Better Tooltips` | 0.1.0 |
| BetterStats | `com.gumatos.betterstats` | `Better Stats` | 1.0.0 |
| BetterFont | `com.gumatos.betterfont` | `Better Font` | 1.0.0 |
| RoguelikeQoL | `com.gumatos.roguelikeqol` | `Roguelike QoL` | 0.1.0 |
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
   - **Compilando do código** (quem for mexer no código): `dotnet build` dentro da pasta de cada mod
     gera `<Mod>\bin\Debug\netstandard2.1\<Mod>.dll`.

   ⚠️ **A DLL não pode ficar solta em `plugins\`** — ela tem que estar dentro da pasta do mod.
   E, como o BepInEx varre a pasta **recursivamente**, **nunca** guarde cópias/backups de DLL
   (`BetterTooltips.dll.bak`, `*.disabled`, cópias antigas) dentro de `plugins\`.

   ![Pasta plugins com uma pasta por mod](docs/img/bepinex-plugins-estrutura.png)

9. **Sempre inicie o jogo pelo r2modman**, no botão **"Start modded"**. Abrir o jogo direto pela
   Steam **não** injeta os mods — pode até abrir normal, mas sem mod nenhum carregado. Se você
   instalou o `RoguelikeQoL` e quiser o HUD ligado, veja o [FAQ](#perguntas-frequentes) antes de abrir.

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
- **RoguelikeQoL**: se você ligou o HUD, no canto superior esquerdo da tela aparecem
  `Treasure Find: +X%` / `Gold Find: +X%` / `Exp Mod: +X%` — só dentro de uma run com personagens
  no grupo.

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
- **RoguelikeQoL especificamente**: o HUD vem **desligado**. Abra
  `...\BepInEx\config\com.gumatos.roguelikeqol.cfg` num editor de texto e mude
  `AtivarHUD = false` para `AtivarHUD = true`, salve e reabra o jogo. (O arquivo só existe depois
  que você abriu o jogo pelo menos uma vez com o mod instalado.)
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

---

## Install (English summary)

**Stolen Realm QoL mods (BepInEx 5)** — small, separate DLLs that improve the game's text without
touching gameplay or the game files (`Assembly-CSharp.dll` is never modified).

- **BetterTooltips** — rewrites skill/status/item tooltips so they are complete instead of
  misleading, and appends a short explanation of how each mechanic actually works, in the game's
  own "special text" colour.
- **BetterStats** — shows attributes as `base (combined)` on the character sheet and level-up
  screen.
- **BetterFont** — swaps the game font for a serif one (Times New Roman), with the original font
  kept as a fallback.
- **RoguelikeQoL** — optional HUD with the current run's Treasure Find / Gold Find / Exp Mod
  (disabled by default; set `AtivarHUD = true` in `BepInEx\config\com.gumatos.roguelikeqol.cfg`).
- **RoguelikeDebugger** — **developer tool only**, not for players: it dumps internal game data
  into the log file.

Install:

1. Install **r2modman** (<https://github.com/ebkr/r2modmanPlus/releases>) and pick **Stolen Realm**.
2. In the **Online** tab, install **BepInExPack** (5.4.2305 validated here) with dependencies.
3. Click **Start modded** once, let the game open, then close it (this creates the folders).
4. **Settings → Browse profile folder**, open `BepInEx\plugins`, and copy each mod folder in —
   one folder per mod, with the DLL inside: `BepInEx\plugins\<ModName>\<ModName>.dll`.
5. Launch the game with **Start modded** (launching from Steam will not load the mods).

Verify: open `BepInEx\LogOutput.log` (profile folder if you use r2modman, the game folder if you
installed BepInEx manually) and look for `[Info   :Better Tooltips] Better Tooltips carregado.`
one line per mod.

Uninstall: delete the mod folders inside `BepInEx\plugins\`. **Never** keep DLL backups inside
`plugins\` — BepInEx scans that folder recursively and would try to load them as mods.

---

*Projeto de mods feito pela comunidade; não é afiliado aos desenvolvedores do Stolen Realm.
Jogo: [Stolen Realm](https://store.steampowered.com/app/1330000/) (Steam AppID 1330000).*
