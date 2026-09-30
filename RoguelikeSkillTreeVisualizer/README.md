# RoguelikeSkillTreeVisualizer

**Status: IMPLEMENTADO (RSTV-2 + RSTV-5 + fase de diagnóstico).** O botão e a árvore somente leitura
estão prontos e o mod **ainda não foi conferido em jogo** pelo autor.

- **GUID:** `com.gumatos.roguelikeskilltreevisualizer`
- **Versão:** 0.2.0
- **Compatível com:** Stolen Realm **v1.3.1** (versão mais recente do jogo em 30/09/2026).
- **Dependências:** nenhuma além do BepInEx 5 (que o r2modman já instala no perfil).

Este mod já é um **pacote Thunderstore**: a pasta tem o `manifest.json`, o `icon.png` (256×256, que o
Thunderstore exige), o `README.md`, o `CHANGELOG.md` e o código:

| arquivo | papel |
|---|---|
| `Plugin.cs` | `[BepInPlugin]`, config (`AtivarBotao`, `AtivarBotaoNaRun`, `AjustarZOrder`) e aplicação dos ganchos **um a um**, com contagem real no log (o `Awake` NÃO cria GameObject: isso roda no chainloader) |
| `Patches.cs` | os 10 ganchos Harmony, cada um com a linha do decompilado no comentário |
| `SelectPartyButton.cs` | RSTV-2a: clona o `roguelikePowerupButton`, encolhe a linha, trata o clique e **diagnostica por que** o botão não entrou |
| `RunButton.cs` | RSTV-5: o mesmo botão **no HUD da run**, ancorado no **Ping Button**, com o **portão 4** |
| `RunTargets.cs` | RSTV-5: alvo do clique na run e o **portão de segurança** (estado do jogo) |
| `PartyTargets.cs` | RSTV-2b: ordem de adição local (o jogo não guarda essa ordem) |
| `SkillTreeReadOnly.cs` | RSTV-2c/2d + RSTV-5: abre a Skill Tree nativa e mantém a sessão somente leitura |
| `RstvHost.cs` | `MonoBehaviour` criado de forma preguiçosa (Update do mod) |

Seguindo o padrão dos outros mods do repositório: uma pasta na raiz, com o `.csproj`,
o `Plugin.cs` e o alvo `DeployToBepInEx` (não existe `src/`, decisão registrada na PKG-1).

**Alvo de compatibilidade:** Stolen Realm **v1.3.1** (versão mais recente do jogo em 30/09/2026) — é a
versão que o `manifest.json` deste pacote declara.

## Para quem vai usar

**O que o botão faz**

- Aparece como um botão quadrado **`Skills`**, colado à direita do **`Choose Powerups`**, na mesma
  linha (o `Choose Powerups` encolhe o necessário e a linha não cresce; o `Accept Party` não muda).
- **RSTV-5 — o mesmo botão existe DURANTE A RUN**, colado à direita do **Ping Button** (o botão de
  apontar o hex) do HUD, na mesma linha. Ele só aparece quando é **seguro** abrir: com o portão 4
  fechado (ver *Portão do botão* abaixo).
- Abre a árvore de skills **do personagem certo**: na tela de party, o **último que VOCÊ adicionou**;
  na run, o **personagem selecionado no momento** (resolvido **no clique** — o nível e o equipamento
  mostrados são os de agora, sem cache).
- Dentro da árvore dá para **navegar, dar zoom, trocar de aba e ler os tooltips** com os números do
  seu personagem. As skills já aprendidas aparecem acesas; o resto cinza/`CannotObtain`.
- Na tela de party o botão fica **desabilitado quando a sua party está vazia** e só aparece em modo
  Roguelike (segue o `Choose Powerups`).

**Portão do botão (RSTV-5 — só vale para o botão da RUN)**

O botão da run **some e recusa a abertura** (com o motivo no log) enquanto qualquer uma destas
condições valer — em dúvida, não abre:

| condição | por quê |
|---|---|
| `HexCellManager.CurrentState == PlayerState.Action` | você está **mirando** uma skill; abrir a árvore cancelaria o apontar hex |
| `GUIManager.PingModeActive` | modo de apontar o hex ligado (o clique do ping atravessaria a janela) |
| `Root.IsPlayerTurnAndReady == false` (em batalha) | não é o seu turno |
| `Root.AnyActingCharactersInBattle` / `AnyMovingCharactersInBattle` | alguém está executando ação/andando |
| `Root.SpawnPlacementActive` | posicionamento inicial |
| `RoguelikeManager` ativo | level-up/reroll pendente: o jogo troca o personagem selecionado sozinho |
| `UIWindowManager.OpenedWindows` não vazio | já há uma janela aberta (mochila, opções...) — não empilhar |
| `GUIState` fora de `InBattle`/`InWorldMap`/`InTown` | estados fora da run |

As checagens de **turno/agindo/movendo** valem **só em batalha**: fora dela `IsPlayerTurnAndReady`
fica com o último valor do combate (o jogo o zera no fim do turno, l.110300) e bloquearia o botão no
mapa do mundo inteiro.

**O que o botão NÃO faz**

- **Não gasta ponto de skill** — o rodapé mostra `0 points available`.
- **Não aprende nem remove skill** — clicar num nó é bloqueado (`read-only`) e o `Respec Build` fica
  escondido.
- **Não altera** o `Accept Party`, a Current Party, os Powerups, o GameMode nem as regras do
  Roguelike. Nenhum arquivo do jogo é modificado.
- **Não mistura jogadores** — cada jogador usa os **seus próprios** personagens; o que o outro
  adiciona à party não muda o que você vê.

O mod **não reimplementa** as Skill Trees: ele resolve o personagem certo e entrega a instância
real para o sistema nativo. Não há compra de skill, gasto de ponto nem qualquer escrita.

### Instalar

**Pelo r2modman (recomendado):** instale este pacote no perfil do Stolen Realm — o r2modman coloca a
DLL em `BepInEx\plugins\RoguelikeSkillTreeVisualizer\`.

**Manual:**

1. Instale o **BepInEx 5 x64** no jogo (ou dê "Start modded" uma vez no r2modman, que cria a pasta).
2. Copie a pasta `RoguelikeSkillTreeVisualizer` para:
   ```text
   %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
   ```
   Deve ficar: `...\plugins\RoguelikeSkillTreeVisualizer\RoguelikeSkillTreeVisualizer.dll`
3. Abra o jogo. No `LogOutput.log` deve aparecer:
   ```text
   Roguelike Skill Tree Visualizer 0.1.0 carregado (RSTV-2: botao ao lado do Choose Powerups + skill tree read-only).
   RSTV: patches Harmony aplicados (8/8 ganchos, 8 metodos do jogo).
   ```
   Se vier `7/8` (ou menos), o log diz **qual** gancho não entrou — veja *Diagnóstico* abaixo.
4. Vá em **Roguelike → Select Party**: o botão `Skills` fica colado à direita do `Choose Powerups`.

> **Só funciona no modo Roguelike** e o botão só aparece na tela **Select Party**. Não é preciso
> entrar em partida.

### Config (opcional)

`BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`:

| seção | chave | padrão | o que faz |
|---|---|---|---|
| `Geral` | `AtivarBotao` | `true` | `false` = o mod carrega, registra os ganchos, mas **não cria botão nenhum** na tela de party |
| `Geral` | `AtivarBotaoNaRun` | `true` | `false` = não cria o botão no HUD da run (o da tela de party continua normal). O **portão 4** vale mesmo com `true` |
| `Geral` | `AjustarZOrder` | `true` | ajusta o índice de irmão da janela nativa para a árvore ficar **por cima do HUD** na run. Desligue se o tooltip do jogo aparecer atrás da árvore |

O padrão é o comportamento de sempre: quem não abrir o arquivo de config vê os botões ligados (com
todas as guardas).

### Desinstalar

1. Feche o jogo.
2. Apague a pasta do mod em `BepInEx/plugins/RoguelikeSkillTreeVisualizer/` (no perfil do r2modman
   ou na instalação manual). Nada é criado fora dela.
3. Opcional: apague `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`.

Desinstalar não deixa resíduo no jogo e não afeta save.

## Diagnóstico — como saber o que aconteceu

O mod **não falha em silêncio**: cada gancho é aplicado e logado individualmente e cada caminho de
falha escreve o motivo. No `LogOutput.log`:

| linha | significa |
|---|---|
| `Roguelike Skill Tree Visualizer 0.2.0 carregado ...` | o plugin carregou |
| `RSTV: gancho aplicado — <Classe> (N metodo(s) do jogo).` | um gancho entrou (uma linha por gancho) |
| `RSTV: patches Harmony aplicados (10/10 ganchos, 10 metodos do jogo).` | **contagem real** de ganchos aplicados; se vier `9/10`, o mesmo erro termina com `GANCHOS QUE FALHARAM:` e os nomes |
| `RSTV: FALHA ao aplicar o gancho <Classe> — <motivo>` | aquele gancho não entrou (assinatura que mudou de versão, por exemplo) |
| `RSTV DIAG: botao 'Skills' da tela Select Party HABILITADO/DESABILITADO ...` | o config foi lido (as duas chaves de botão) |
| `RSTV-2: botao 'Skills' injetado (NxN px) ... largura da linha A -> B px` | o botão foi criado; as duas larguras devem ser iguais |
| `RSTV DIAG: botao 'Skills' NAO injetado — <motivo>` | **por que** o botão não apareceu (botão nativo ausente, sem `RectTransform`, exceção, config desligado) |
| `RSTV DIAG: a tela Select Party esta aberta e o botao 'Skills' NAO foi injetado. motivo=...` | resumo com o estado da tela quando a injeção falha |
| `RSTV-2: clique no botao 'Skills' -> '<nome>' (nivel N).` | o clique resolveu o personagem |
| `RSTV-5: botao 'Skills' injetado no HUD (...) a direita do Ping Button` | o botão da run foi criado (com a geometria da linha) |
| `RSTV DIAG: botao 'Skills' do HUD escondido — <motivo>` | **por que** o botão da run está escondido agora (portão 4, uma linha por motivo) |
| `RSTV DIAG: botao 'Skills' do HUD VISIVEL e clicavel — alvo '<nome>'` | o portão reabriu |
| `RSTV-5: clique RECUSADO — <motivo>` | o clique chegou com o portão fechado (reavaliado na hora) |
| `RSTV-5: clique no botao 'Skills' do HUD -> '<nome>' (nivel N).` | o clique resolveu o personagem selecionado |
| `RSTV: skill tree read-only aberta para '<nome>' (... contexto=Run)` | a árvore abriu (contexto de party ou de run) |
| `RSTV-5: o jogo JA tem '<nome>' como personagem selecionado` | **nenhuma** escrita em `GameLogic.CurrentlySelectedCharacter` |
| `RSTV-5: abertura RECUSADA — o jogo tem '<A>' selecionado e o alvo e '<B>'` | a árvore mostraria o contexto errado: não abriu |
| `RSTV-5: nenhum personagem estava selecionado — definindo '<nome>'` | o mod escreveu a seleção (valor anterior guardado e devolvido no fim) |
| `RSTV-5: personagem selecionado devolvido ao valor de antes da abertura` | a blindagem 2 desfez a escrita |
| `RSTV-5: janela registrada em UIWindowManager.OpenedWindows` | camada 1 do bloqueio do clique do hex (o jogo passa a considerar "menu aberto") |
| `RSTV-5: clique no hex CONSUMIDO enquanto a arvore read-only esta aberta` | camada 2 (prefixo no `ProcessLeftMouseClick`) |
| `RSTV-5: Esc NAO consumido — a janela do topo e '<Classe>'` | o Esc foi deixado para quem está por cima (mochila/opções) |
| `RSTV-5: fechando a skill tree read-only — <motivo>` | a guarda de ciclo de vida fechou a árvore (tela de party fechou, saiu de `InBattle`/`InWorldMap`/`InTown`, o jogo trocou o personagem) |
| `RSTV-2: clique na arvore BLOQUEADO (read-only)` | o clique no nó foi barrado |
| `RSTV-2: ResetSkillPoints BLOQUEADO (read-only)` | o clique num botão que zeraria as skills do personagem foi barrado |
| `RSTV: modo somente leitura encerrado (nada foi gravado no personagem)` | fechou limpo |

## O que o mod faz (técnico)

Adiciona um **visualizador de Skill Trees** na tela **Roguelike → Select Party**: um botão
quadrado **à direita** do `Choose Powerups` que abre a interface de Skill Trees **nativa do jogo**
(a mesma do `Campaign → Change Skills`), em modo **somente leitura**, com o contexto **real** do
personagem — Level, equipamento, atributos e estado das skills atuais.

## Regras que já estão decididas

| regra | o que significa |
|---|---|
| **Personagem** | o **último que o jogador local adicionou** à Current Party — nunca o último global |
| **Multiplayer** | cada jogador usa os **seus próprios** personagens; a ação de outro jogador não muda o meu contexto |
| **Remoção** | se o último for removido, cai para o último local **ainda na party**; party vazia = botão desabilitado |
| **Contexto** | resolvido **no clique**, não quando a tela abre (Level/equipamento sempre atuais, sem cache) |
| **Read-only** | navegar, zoom, tooltips e requisitos continuam funcionando; nada que persista muda |
| **Intocáveis** | `Accept Party`, a Current Party, os Powerups, o GameMode e as regras do Roguelike |
| **UI** | o botão é **clonado de um botão nativo** (mesmo sprite/estados); a largura do `Choose Powerups` encolhe o necessário e a linha **não cresce** |
| **Falha** | nenhum caminho pode falhar calado: ou o log diz **por que** o botão/gancho não entrou, ou o estado duvidoso é fechado |

## Ícone

`icon.png` (256×256) é o ícone de pacote do Thunderstore — **arte de verdade do autor**
(redimensionada de uma arte 1254×1254), não um ícone genérico gerado pelo script do empacotador.
É PNG válido (RGBA) e passa na checagem de 256×256 do `tools/pack-thunderstore.py`.

**Pendente:** o arquivo **original de 1254×1254 não está versionado** neste repositório (dos outros
mods os originais ficaram em `scratch/icons-orig/`, mas o do RSTV não está lá). Se precisar
reexportar ou cortar outra versão, a arte-fonte tem de ser pedida de novo ao autor — nada de gerar
um PNG falso no lugar.

## Especificação e aceite

A especificação completa (77 itens: investigação obrigatória, estratégia de injeção, rastreio de
personagem, testes por caso) e os critérios de aceite estão registrados no quadro interno do projeto (não versionado).

## Roteiro de conferência em jogo (RSTV-2)

1. Compilar e instalar: `dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj`
   (sem a propriedade `DeployToBepInEx=false` ele copia a DLL para o perfil do r2modman).
2. Abrir o jogo modded e ir em **Roguelike → Select Party**. No `LogOutput.log` devem aparecer
   `RSTV: patches Harmony aplicados (10/10 ganchos, 10 metodos do jogo)` e
   `RSTV-2: botao 'Skills' injetado ... largura da linha N -> N px` (as duas larguras devem bater).
   Se o botão **não** aparecer, o log já diz o motivo (`RSTV DIAG: ...`, com a tela, o botão nativo e
   a party local) — não precisa adivinhar.
3. Adicionar 2 personagens meus à party (clique nos tiles) → o log diz qual virou o alvo; clicar num
   terceiro e removê-lo → o alvo volta para o último que ficou.
4. Clicar no botão quadrado **Skills** (colado à direita do `Choose Powerups`). Esperado:
   `RSTV-2: skill tree read-only aberta para '<nome>' (nivel N, M skills, 0 pontos)` e a árvore nativa
   por cima da tela de party, com as skills aprendidas acesas e o resto cinza/`CannotObtain`.
5. Na árvore: passar o mouse nos nós (tooltip com os números do personagem real), trocar de aba,
   tentar clicar num nó → `RSTV-2: clique na arvore BLOQUEADO (read-only)`. O botão `Respec Build` não
   aparece; o rodapé mostra `0 points available`.
6. Fechar (X ou Esc) → `RSTV-2: modo somente leitura encerrado (nada foi gravado no personagem)`.
   Conferir que `Accept Party`, a Current Party e os Powerups continuam intactos.
7. Repetir abrindo/fechando 3× e depois aceitar a party — a árvore não pode aparecer presa atrás
   nem empurrar a UI.
8. Opcional (config): com `AtivarBotao = false` no `.cfg`, a tela abre normal e **sem** botão nenhum;
   o log diz `RSTV DIAG: botao 'Skills' DESABILITADO nesta sessao`.

## Roteiro de conferência em jogo (RSTV-5 — o botão na run)

> Nada disto foi executado ainda: o mod não foi aberto em jogo. Cada passo diz o que **prova**.

1. **Boot:** `RSTV: patches Harmony aplicados (10/10 ganchos, 10 metodos do jogo)` e
   `RSTV-5: gancho do HUD da run ATIVO (CurrentCharacterUI.InitSingleton)`.
2. **Entrar numa run e olhar o HUD:** em **batalha, turno do jogador, sem mira** o log imprime
   `RSTV-5: botao 'Skills' injetado no HUD (NxN px) a direita do Ping Button — largura da linha A -> B`.
   *Prova:* o botão existe, é quadrado e a linha não cresceu (A == B).
3. **Aparência:** o botão deve ter o **fundo** do botão nativo e o texto **`Skills`**; o **ícone do
   ping** não pode aparecer. O log diz quantos gráficos herdados foram desligados e qual é o
   `targetGraphic`. Se o rótulo não existir (Ping Button é só ícone), o log diz que o rótulo foi
   montado a partir de qual botão-molde (ou que ficou sem rótulo — defeito a reportar).
4. **Clicar em `Skills`:** `RSTV-5: clique no botao 'Skills' do HUD -> '<nome>' (nivel N)` +
   `RSTV-5: o jogo JA tem '<nome>' como personagem selecionado` (é o caso seguro, **sem escrita**) +
   `RSTV: skill tree read-only aberta para '<nome>' (... contexto=Run)` +
   `RSTV-5: janela registrada em UIWindowManager.OpenedWindows`.
   *Provas:* o contexto é do personagem selecionado; a árvore aparece **por cima do HUD**; o clique do
   hex passa a ser consumido.
5. **Com a árvore aberta, clicar num hex do chão e depois num inimigo.** Esperado (log):
   `RSTV-5: clique no hex CONSUMIDO ...` e **nada acontece no jogo** — nenhum movimento, nenhuma ação,
   nenhum dano. *Prova da blindagem 5.* Se algo acontecer, é defeito grave: reportar com o log.
6. **Com a árvore aberta, apertar Esc.** Esperado: `RSTV-5: Esc/B consumido` +
   `RSTV: modo somente leitura encerrado`. A câmera, o personagem selecionado e o turno continuam
   como estavam.
7. **Portão 4:** selecionar uma skill (entrar em **mira**) → o botão `Skills` **some** e o log diz
   `RSTV DIAG: botao 'Skills' do HUD escondido — mira de skill ativa ...`. Cancelar a mira (Esc/right
   click) → o botão volta: `RSTV DIAG: botao 'Skills' do HUD VISIVEL e clicavel — alvo '<nome>'`.
   Repetir com: turno do inimigo (`nao e o turno do jogador`), personagem andando/agindo, level-up
   pendente (`RoguelikeManager ativo`) e com a mochila aberta (`ja existe uma janela de UI aberta`).
   *Prova:* o botão só aparece quando é seguro.
8. **Trocar de personagem com a árvore aberta** (tecla de trocar personagem, se houver, ou clique no
   personagem não selecionado): esperado `RSTV-5: fechando a skill tree read-only — o jogo trocou o
   personagem selecionado ...` e a árvore fecha. *Prova da blindagem 6.*
9. **Esc com a mochila aberta por cima da árvore:** abrir a mochila com a árvore aberta e apertar Esc
   → o log diz `RSTV-5: Esc NAO consumido — a janela do topo e 'InventoryManager'` e **a mochila
   fecha** (a árvore continua atrás). *Prova da blindagem 3.*
10. **Tooltips:** com a árvore aberta na run, passar o mouse nas skills → o tooltip tem de aparecer
    **por cima da árvore**. Se aparecer atrás, desligar `AjustarZOrder` no `.cfg` e conferir de novo.
11. **Voltar ao mapa do mundo / town com a árvore aberta:** a árvore pode ficar aberta (está na
    whitelist); **cutscene** fecha. *Prova da blindagem 1 + whitelist.*
12. **Sair do turno / fim de batalha com a árvore aberta:** o `GUIState` muda para `InWorldMap` e
    **nada quebra** (a janela continua, o input volta ao jogo quando ela fechar).
13. **Config:** `AtivarBotaoNaRun = false` → o log diz `RSTV DIAG: botao 'Skills' da run desativado —
    AtivarBotaoNaRun=false` e o HUD fica sem o botão (o da tela de party continua normal).

## Riscos conhecidos (não verificáveis sem abrir o jogo)

- O sprite/âncora/`LayoutGroup` da linha vivem no prefab (`resources.assets`, 1,7 GB, não aberto):
  o mod mede em runtime, compensa a largura e **loga** o modo de layout usado. Se o log mostrar
  `childForceExpandWidth`, a linha não cresce mas os botões vizinhos se redistribuem.
- Z-order: a Skill Tree é instanciada sob outro ramo do canvas. O mod compara os índices de irmão e,
  se a árvore estiver atrás da tela de party, move o ramo para o fim e restaura ao fechar (logado).
- `GameLogic.CurrentlySelectedCharacter` é ajustado para o personagem alvo (é de onde `SkillTreeManager`
  e o `Tooltip` leem o contexto). Isso também marca aquele personagem como `IsPartyLeader` e libera o
  lock da câmera — o mesmo que o jogo faz ao selecionar um personagem no mundo.
- **Fechamento de emergência:** se a higienização do commit falhar, o mod **não deixa o original
  rodar** e fecha a janela por conta própria (zero escrita) em vez de arriscar a gravação. Só
  acontece num caminho de exceção, mas vale conferir que a tela de party volta ao normal depois
  (o log diz `RSTV: falha ao higienizar AcceptSkillChanges ...`).
- **Segundo caminho de gravação** (achado na auditoria estática): `SkillTreeManager.ResetSkillPoints()`
  (l.173274) é público, sem parâmetro e chama `Character.ResetSkills()`, que **zera todas as skills** do
  personagem e enfileira o save dele (l.37474) — sem passar pelo `AcceptSkillChanges`. O mod agora o
  **bloqueia** em read-only (gancho 8). O que **fica para medir em jogo**: qual botão do prefab chama
  esse método (o campo `resetButton`, l.172057, não está ligado em código) e se existe algum botão que
  chame `CheckSkillDependancies(Character)` (l.172328), que também grava (l.172344/172352) mas não tem
  nenhum chamador no assembly — esse **não** foi bloqueado de propósito (bloqueá-lo às cegas poderia
  atrapalhar um caminho legítimo do jogo).
- **Interceptor de Esc é um slot único** (`UIWindowManager.CancelInterceptor`, l.215982). O
  `InventoryManager.OnEnable` (l.125301) também o ocupa. **RSTV-5:** o mod agora **fotografa** quem
  tinha o slot ANTES de abrir (`CaptureInterceptorOwner`, antes do `SetActive(true)` que dispara o
  `OnEnable` do `SkillTreeManager`, l.172890) e **devolve esse delegate** no fechamento — não deixa
  mais `null` no lugar de quem estava lá. Além disso, o Esc **deixa de ser consumido** quando a
  janela do topo (`OpenedWindows`) não é a nossa, a `CharacterMenusManager` ou a tela de party
  (blindagem 3). *Fica para medir em jogo:* se o delegate devolvido é o do `SkillTreeManager` (o
  caso esperado, porque o `OnEnable` dele roda no `SetActive(true)` uma linha antes), o `OnDisable`
  do próprio jogo (l.172899) faz a limpeza normal e o slot termina em `null` — igual ao vanilla.
- **Largura da linha com `childForceExpandWidth`:** o mod hoje não compensa a largura nesse modo
  ("o próprio grupo acomoda o filho"). Isso só vale se a linha tiver largura fixa; se ela for
  dimensionada pelo conteúdo (um `ContentSizeFitter` acima), ela **cresce** com o clone e o log
  mostra `largura da linha A -> B` com A ≠ B. É exatamente o que a linha do log serve para flagrar
  no primeiro teste em jogo.

### Correções da auditoria estática (contra o decompilado, sem rodar o jogo)

- Gancho 8: `SkillTreeManager.ResetSkillPoints` bloqueado em read-only (segundo ponto de gravação).
- A árvore agora fecha sozinha se a tela Select Party fechar por fora (aceitar a party muda o
  `GUIState` e o jogo fecha a tela em l.118416/l.133307/l.215520 sem fechar o `SkillTreeManager`):
  antes ela ficaria desenhada por cima do mapa, com o interceptor de Esc instalado.

### Riscos do botão na run (RSTV-5 — estáticos, precisam de conferência em jogo)

- **Aparência do clone**: o `Ping Button` é um botão de **ícone** e o `resources.assets` não foi
  aberto. O mod cloneia o botão nativo, desliga os gráficos herdados que **não** são o `targetGraphic`
  (o ícone do ping) e cria um rótulo `Skills` a partir de outro texto do mesmo HUD. Se o
  `targetGraphic` do Ping Button **for** o próprio ícone, o botão novo aparece com o ícone do ping —
  o log diz qual é o `targetGraphic`, então isso se resolve com uma linha a mais, sem adivinhação.
- **Janela registrada em `OpenedWindows`** (camada 1 contra o clique atravessando a janela): enquanto
  a árvore está aberta, `GUIManager.InMenus` é `true`, o que também desliga o input de hex legítimo e
  limpa o `CurrentlyHoveringHexCell`. É o comportamento desejado (a janela cobre a tela), mas **mexe
  no `OpenedWindows` do jogo** — se o registro falhar, o log avisa e a camada 2 (prefixo no
  `ProcessLeftMouseClick`) continua valendo. Se a árvore for fechada por fora, a rede de segurança do
  host retira a entrada (uma vez por segundo) para o jogo não ficar com o input morto.
- **Z-order vs. tooltip**: a árvore é instanciada em outro ramo do canvas; na run o mod a empurra
  para cima do HUD (`AjustarZOrder`). Se o tooltip do jogo passar a aparecer **atrás** da árvore,
  desligar `AjustarZOrder` no `.cfg` e conferir.
- **Escolha do alvo na run**: se o jogo estiver com **outro** personagem selecionado, a abertura é
  **recusada** (a árvore mostraria o contexto de tooltip errado — `Tooltip.TooltipCharacter`,
  l.213124). Se o jogo estiver **sem** ninguém selecionado, o mod usa o primeiro personagem local da
  party (fallback documentado) e **devolve a seleção ao valor anterior** ao fechar. O caso de o jogo
  tolerar a seleção voltar a `null` no meio da run precisa de conferência em jogo (é o mesmo estado
  de antes da abertura, mas quem escreveu foi o mod).
- **Checagens de turno só em batalha**: fora de batalha o `IsPlayerTurnAndReady` fica no último valor
  do combate, e usá-lo fora da batalha bloquearia o botão no mapa do mundo. Se em jogo aparecer
  alguma janela ruim fora de batalha, a whitelist de `GUIState` é o lugar de apertar.
- **`CurrentCharacterUI.skillsBtn` / `chooseSkillsBtn`**: o jogo tem campos de botão de skills no HUD
  (`skillsBtn`, l.209436, e `chooseSkillsBtn`, l.209462 — este último **nunca referenciado em código**,
  logo tem `onClick` ligado só no prefab, provavelmente `ButtonPressedSkillTree`, l.209994). No modo
  Roguelike o caminho nativo de skills abre `SkillTreeManagerRoguelike` (l.173293 / `GUIManager.ShowSkillTree`,
  l.119313) — que é a árvore de **level-up**, com escrita. Fica para conferir em jogo se algum desses
  botões aparece na run e se convive com o nosso (o nosso é somente leitura e não os substitui).

