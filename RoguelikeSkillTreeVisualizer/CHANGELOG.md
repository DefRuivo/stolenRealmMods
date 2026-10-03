# Changelog — RoguelikeSkillTreeVisualizer

## 0.3.0 — aba "All Skill Trees" + botão/atalho + escala/posição nativa (RSTV-13..19)

**RSTV-13 — o botao `Skills` do HUD volta a APARECER passeando no MAPA-MUNDO.** O `RunTargets.GateOk`
aplicava ao mapa portoes que descrevem UMA BATALHA: `Root.SpawnPlacementActive` (so existe no setup da
batalha, l.112152 liga / l.112165 desliga) e `HexCellManager.CurrentState == PlayerState.Action` (a
mira de skill) eram checados em QUALQUER estado — no mapa eles escondiam o botao justamente enquanto o
jogador passeia (sintoma 5 do dono). O `IsPlayerTurnAndReady` ja estava dentro do ramo `InBattle`, mas
a separacao estava implicita. Agora ela e explicita: os portoes de batalha (mira, posicionamento
inicial, turno, `AnyActingCharactersInBattle`, `AnyMovingCharactersInBattle`) moram DENTRO do ramo
`if (estado == GUIState.InBattle)`; no mapa/cidade valem so os universais (modo de apontar o hex, UI
aberta, alvo). A seguranca EM BATALHA nao mudou — cada portao continua bloqueando la.

**RSTV-14 — o botao DENTRO da janela do level-up segue o CICLO DE VIDA (deixa de "voar").** O
`LevelUpWindowButton` era criado SO no postfix de `OpenSkillSelectWindow` e nunca reavaliado: o jogo
troca o estagio do level-up SEM fechar a janela (`CurLevelUpStage`, l.168697, liga
`SkillSection`/`ItemSectionInventory`/`AttributeSection`), o painel `Content` muda de metragem e o
clone — filho do `SkillSelectWindow` — continuava visivel no estagio de ATRIBUTOS, preso ao canto
ANTIGO do painel (sintoma 3). Agora um `LevelUpWindowButton.Refresh()` (chamado a cada quadro pelo
`RstvHost.Update` e tambem no fim do `Ensure`) mostra o clone SO com a janela ativa, da mesma
instancia, no estagio `LevelUpStage.Skills` — nos outros estagios (Items/Attributes/Currency) ele
some, e ao VOLTAR ao estagio de skills ele e re-ancorado no canto atual do `Content`. O `Ensure`
recusa injetar com a janela fechada ("nao injetar fora de hora"). O sintoma (6) ("aperto Skills e o
botao some") e o flapping do portao de "janela aberta", tratado na RSTV-5: a arvore read-only nao
deixa a janela presa em `UIWindowManager.OpenedWindows`, entao o botao do HUD VOLTA ao fechar.

- **Testes**: `t_rstv13_gate_mapa.py` (suite pura; modelo puro do portao por estado) e
  `t_rstv14_botao_ciclo_levelup.py` (suite pura; ciclo de vida + opcoes de estagio). Iscas:
  `cp_rstv13_batalha_no_mapa.py`, `cp_rstv14_refresh_morto_no_host.py`,
  `cp_rstv14_refresh_sem_estagio.py`. Prova de fogo FISICA: os tres defeitos foram plantados nos
  fontes REAIS (`RunTargets.cs`, `RstvHost.cs`, `LevelUpWindowButton.cs`), o teste saiu `REPROVOU`
  (exit 1) pelo motivo certo e os arquivos foram restaurados byte a byte (sha256 conferido). Log:
  `tools/testes/rstv13-14-prova-reprovando.log`. A RSTV-8 teve o modelo do portao ajustado (mira e
  spawn agora contam como portoes de batalha no cenario puro).

## Nao publicado (RSTV-12) — **precisa de conferencia em jogo**

**RSTV-12 — o clique dos botoes `Skills` passa a chegar ao mod (nao ao `onClick` do prefab).** O log
de 02/10 mostrou os dois sintomas: o botao do HUD **pingava** em vez de abrir a arvore, e o da janela
do level-up disparava `ConfirmLevelUpSelection` (**11 NullReferenceException**). Causa raiz lida do IL
de `UnityEngine.CoreModule.dll` deste build: o `UnityEvent` guarda DUAS listas — `m_PersistentCalls`
(os listeners serializados no prefab, ex.: `ButtonPressedPing`/`ConfirmLevelUpSelection`) e
`m_RuntimeCalls` (os de script) — e `RemoveAllListeners()` chama `InvokableCallList.Clear()`, que
esvazia **so** a de runtime. Pior: `PrepareInvoke()` concatena as persistentes **antes** das de
runtime, entao o listener do jogo roda primeiro e, se ele lancar, o `Invoke()` **aborta** e o nosso
nem chega a rodar.

- **Conserto**: novo helper `SelectPartyButton.ClearClickListeners(Button)` — troca a **instancia** do
  evento (`button.onClick = new Button.ButtonClickedEvent()`), descartando junto a lista persistente
  serializada; o listener do mod e instalado no evento limpo. Aplicado nos **tres** clones (HUD, janela
  do level-up e tela Select Party).
- **Nao era** sobreposicao/raycast (o log mostra o NOSSO `OpenForTarget` sendo chamado no clone do HUD)
  **nem** re-bind de componente (`UIButtonController`, l.336107, so troca cores — nao mexe em onClick).
- **Testes**: `t_rstv12_onclick_roteamento.py` (suite pura) + `cp_rstv12_clique_no_original.py` (isca).
  O modelo puro do `UnityEvent` reproduz o clique que cai no original (`pingou` no HUD / `levelup-nre`
  no level-up) e aprova o conserto (`abriu`). Prova de fogo fisica: o defeito foi plantado no
  `RunButton.cs` e no `LevelUpWindowButton.cs` REAIS, o teste saiu `REPROVOU` (exit 1) e os fontes
  foram restaurados byte a byte (sha256 conferido). Log: `tools/testes/rstv12-prova-reprovando.log`.

## Nao publicado (RSTV-11b) — **precisa de conferencia em jogo**

**RSTV-11b — o botao `Skills` passa a existir DENTRO da janela do level-up.** O re-parent da RSTV-9 foi
**aposentado**: o clone do HUD nao muda mais de casa (a entrada da RSTV-9 abaixo fica como historico). No
lugar dele, o postfix de `RoguelikeManager.OpenSkillSelectWindow` clona o `AcceptButton` como filho
**direto** do `SkillSelectWindow` (TELA CHEIA), **fora** do filho `Content` — que tem `VerticalLayoutGroup`
+ `ContentSizeFitter`, e um filho ali reflui o painel inteiro. O botao nasce no canto superior direito do
painel visivel (o `Content`, ~293x536 px), com o `onClick` SERIALIZADO limpo (`RemoveAllListeners` — ele
chamava `ConfirmLevelUpSelection`, escrita) e apontando para o `RunButton.OpenForTarget`. O `Ensure` e
**idempotente por janela** (o gancho roda de novo a cada personagem da fila de level-up, sobre o mesmo
`SkillSelectWindow`).

**RSTV-11b — `RunButton.OpenForTarget()` e o corpo unico.** Extraido do antigo `OnClick`, e reusado pelo
botao do HUD, pelo botao da janela do level-up e pelo atalho F10 (RSTV-11a), que antes duplicava o corpo.
A maquinaria do re-parent (`HomeInLevelUp`/`HomeInRow`/`CaptureHome`, campos `_home*`, constante
`LadoMinimoLevelUp`) saiu do `RunButton`.

**Testes:** `t_rstv11b_botao_janela_levelup.py` (suite pura) + `cp_rstv11b_sem_idempotencia.py` e
`cp_rstv11b_clone_no_content.py` (iscas). Os dois defeitos — 'sem idempotencia' (2o botao) e 'clone no
Content' (reflow) — foram plantados **no fonte real**, o teste saiu `REPROVOU` (exit 1) e o arquivo foi
restaurado byte a byte (sha256 conferido). Log: `tools/testes/rstv11b-prova-reprovando.log`.

## Historico (RSTV-8 + RSTV-9) — **precisa de conferencia em jogo**

**RSTV-8 — o botao da run deixa de ser escondido no level-up.** O portao `RunTargets.GateOk` escondia o
botao com `if (RoguelikeManager.IsNotNullAndIsActive) return false`, mas isso significa "o manager foi
CARREGADO" — o GameObject dele fica ativo a run inteira depois do primeiro level-up. A janela de verdade
e o filho `SkillSelectWindow.activeSelf` (o mesmo criterio que o jogo usa em `GUIManager.Update`).
Agora o level-up **libera** o botao, e o alvo passa a sair do PROPRIO manager
(`CurrentRoguelikeSkillSelectingCharacter`, fallback `CharactersWaitingForLevelUp[0].Character`), nunca
do `CurrentlySelectedCharacter` que ele troca. Os demais portoes (mira/ping/janela/spawn/turno/animacao)
continuam.

**RSTV-9 — o botao RENDERIZAR durante o level-up (caso a parte). [SUPERADO pela RSTV-11b — o re-parent
abaixo foi APOSENTADO; o level-up agora tem um botao PROPRIO dentro da janela, `LevelUpWindowButton`.]**
Achado critico da RSTV-8: nesse
instante o jogo desliga o HUD INTEIRO (`GUIManager.Update`, l.120492, faz
`CurrentCharacterUI.gameObject.SetActive(false)` enquanto `SkillSelectWindow` esta ativo) e o clone da
RSTV-5 e filho desse HUD — o portao liberar era NECESSARIO, mas o botao NAO renderizava. Agora, enquanto
a janela do level-up esta aberta, o `RunButton` realoca o clone para DENTRO do `SkillSelectWindow`
(canto superior direito, ultimo irmao para desenhar/clicar por cima, lado no minimo `LadoMinimoLevelUp`
= 44 px) e o devolve para a linha do Ping Button quando ela fecha, restaurando a geometria original
(sem reaplicar o `ApplySquareLayout`). **O caso normal — tela Select Party e run no mapa-mundo E em
combate — NAO muda**: a realocacao so ocorre dentro do ramo de level-up; o tamanho da linha (Ping
Button) segue intacto.

**Testes:** `t_rstv9_render_levelup.py` (suite pura) + `cp_rstv9_botao_no_hud_desligado.py` (isca). A
prova de fogo fisica plantou o defeito no `RunButton.cs` real (o teste saiu `REPROVOU`, exit 1) e
restaurou o fonte byte a byte.

## 0.2.0

**RSTV-5 — o botão `Skills` agora existe DURANTE A RUN**, ancorado no **Ping Button** (o botão de
apontar o hex) do HUD, ao lado dele, na mesma linha. A janela é a MESMA Skill Tree nativa, no mesmo
modo somente leitura. **Nada disto foi conferido em jogo ainda** — o roteiro está no `README.md`.

- **Botão no HUD da run**: clone do botão nativo `CurrentCharacterUI.pingBtn` (l.209464, handler
  `ButtonPressedPing` l.210027 → `GUIManager.TogglePingMode` l.119299), injetado como irmão à direita
  dele com a mesma compensação de largura já validada na tela de party (reusa o
  `SelectPartyButton.ApplySquareLayout` nos 3 modos de layout). Injeção 1× pelo postfix de
  `CurrentCharacterUI.InitSingleton` (l.209626, o ponto em que o jogo instancia o HUD) e espelhamento
  no `RstvHost.Update` do mod — **nunca** no `Update`/`UIUpdate` do próprio HUD (l.209655, que roda
  todo frame e mexe no `endTurnButton`).
- **Alvo resolvido no clique**: o personagem **selecionado no momento**; se o jogo estiver sem
  ninguém selecionado, o **primeiro personagem local da party** (fallback documentado).
- **Portão de segurança (sempre ativo, mesmo com o botão ligado)**: o botão **some e recusa a
  abertura**, com o motivo no log, quando há **mira de skill ativa** (`HexCellManager.CurrentState ==
  Action`), **modo de apontar hex ligado**, **não é o turno do jogador**, alguém **agindo/movendo**,
  **posicionamento inicial**, **level-up pendente** (`RoguelikeManager`), **janela de UI aberta** ou
  `GUIState` fora de `InBattle`/`InWorldMap`/`InTown`. Em dúvida (até numa exceção ao ler o estado),
  não abre.

### Blindagens implementadas (cada uma com a linha do decompilado no código)

1. **Ciclo de vida** — a guarda deixou de ser "a tela de party está aberta" (durante a run ela está
   desligada e a árvore fecharia no frame seguinte): agora é "a instância nativa ainda está ativa" +
   whitelist de `GUIState` para o contexto de run; a checagem da tela de party continua só no
   contexto de party.
2. **Escrita de `GameLogic.CurrentlySelectedCharacter`** (setter l.108082) — só escreve quando é
   **inofensivo**: se o alvo **já é** o selecionado (o setter retorna cedo, l.108097 → zero efeito) ou
   se o jogo está **sem ninguém selecionado** (a metade perigosa do setter só roda com um personagem
   anterior). O valor anterior é **guardado e devolvido** no fechamento (padrão do próprio jogo,
   l.163711/163942). Com **outro** personagem selecionado, a abertura é **recusada** — se não, o
   setter marcaria `IsPartyLeader`, travaria a câmera, **forçaria `HexCellManager.CurrentState =
   Movement`** (cancelando a mira) e chamaria `NotifyPlayerOfTheirTurn` em outro personagem.
3. **Slot único de `CancelInterceptor`** (`UIWindowManager.CancelInterceptor`, l.215982) — o mod
   **fotografa** quem tinha o slot antes de abrir (antes do `SetActive(true)`, que dispara o
   `OnEnable` do jogo, l.172890) e **devolve esse delegate** no fechamento (antes deixava `null`).
   O Esc **deixa de ser consumido** quando a janela do topo não é a nossa, a `CharacterMenusManager`
   ou a tela de party (mesmo critério do jogo, l.172924) — a mochila por cima continua fechando no Esc.
4. **Portão do botão** — ver acima.
5. **Clique do hex** — o branch de **Action** do `PlayerMovement.ProcessLeftMouseClick` (l.153393-153397)
   **não** checa `PointerOverUIObject` (o de movimento checa, l.153342). Duas camadas: a janela passa a
   ser registrada em `UIWindowManager.OpenedWindows` (→ `GUIManager.InMenus`, l.118297, faz
   `ProcessUpdateInputs` l.152986 retornar antes do clique) **e** um prefixo Harmony em
   `ProcessLeftMouseClick(HexCell)` (l.153277) consome o clique enquanto a sessão está ativa. Uma rede
   de segurança no host retira a entrada de `OpenedWindows` se a janela fechar por fora, para o input
   de batalha não ficar morto.
6. **Troca de personagem / de estado** — se o jogo trocar o personagem selecionado ou sair de
   `InBattle`/`InWorldMap`/`InTown`, a sessão é **fechada** (nada de janela read-only com contexto errado).

### Config

- `Geral` → **`AtivarBotaoNaRun`** (padrão `true`): liga/desliga **só** o botão da run. O portão 4
  vale mesmo com `true`.
- `Geral` → **`AjustarZOrder`** (padrão `true`): ajusta o índice de irmão para a árvore ficar por cima
  do HUD na run. Desligue se o tooltip do jogo aparecer atrás da árvore.
- `Geral` → `AtivarBotao` continua sendo o da tela Select Party (inalterado).

### Outras mudanças

- **Ganchos**: 8 → **10** (novos: postfix de `CurrentCharacterUI.InitSingleton`, prefixo de
  `PlayerMovement.ProcessLeftMouseClick`). A contagem do boot vira `10/10 ganchos, 10 metodos do jogo`.
- **Diagnóstico**: o botão da run diz **por que** está escondido, com throttle de 5 s por motivo, e
  avisa quando volta a aparecer; a abertura registra a geometria da linha, o `targetGraphic` do clone
  e quantos gráficos herdados foram desligados.
- `SkillTreeReadOnly` ganhou contexto (`PartyScreen`/`Run`) e a sessão ganhou as guardas de
  ciclo de vida, a devolução da seleção e a limpeza de `OpenedWindows`.

## 0.1.0

Primeira versão. O mod **ainda não foi conferido em jogo** — a conferência está no roteiro do `README.md`.

- **Botão `Skills` na tela Select Party** do modo Roguelike: quadrado, na mesma linha e colado à direita do *Choose Powerups*. É um clone do **botão nativo** (mesmo sprite e estados); a largura do *Choose Powerups* encolhe só o necessário, a linha **não cresce** e o *Accept Party* não muda de tamanho.
- **Abre a Skill Tree NATIVA** do jogo (a mesma de *Campaign → Change Skills*) com o contexto **real** do personagem: nível, equipamento, atributos e estado das skills. A janela nativa é reaproveitada — o mod **não reimplementa** a árvore.
- **Modo somente leitura de verdade**: tooltips (com os números do personagem certo), zoom, troca de abas e requisitos continuam funcionando; **nada é aprendido, removido ou gasto**. O clique no nó é bloqueado, o *Respec Build* fica escondido e o rodapé mostra `0 points available`.
- **Alvo do botão**: o **último personagem que VOCÊ adicionou** à party, resolvido **no clique** (nível e equipamento sempre atuais, sem cache). Cada jogador usa os seus; party local vazia = botão desabilitado.
- **Config**: `Geral` → `AtivarBotao` em `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg` (padrão `true`). Só serve para **desligar** o botão — quem não abrir o arquivo não vê diferença.
- **Diagnóstico**: cada gancho Harmony é aplicado e logado **individualmente** (um gancho que falha não derruba os outros — antes o `PatchAll()` era tudo-ou-nada); o resumo do boot traz a **contagem real** (`RSTV: patches Harmony aplicados (8/8 ganchos, 8 metodos do jogo)`); e se o botão não for injetado o log diz **por quê** (botão nativo ausente, sem `RectTransform`, exceção, config desligado) com o estado da tela.

### Correções da auditoria estática (contra o decompilado do jogo, sem rodar o jogo)

- **Segundo ponto de gravação fechado:** `SkillTreeManager.ResetSkillPoints()` (l.173274) chama
  `Character.ResetSkills()` — que zera todas as skills do personagem e enfileira o save (l.37474) —
  **sem passar pelo `AcceptSkillChanges`**. É gancho novo (8º) e é bloqueado no modo somente leitura.
- **Árvore órfã:** se a tela Select Party fechar por fora com a árvore aberta (aceitar a party muda o
  `GUIState` e o jogo fecha a tela em l.118416/l.133307/l.215520), nada no jogo fechava o
  `SkillTreeManager` — a árvore ficaria por cima do mapa com o interceptor de Esc instalado. Agora o
  host fecha a árvore quando a tela de party não está mais aberta.
- O que **não** mudou de propósito (precisa de teste em jogo, está em *Riscos conhecidos* do
  `README.md`): `CheckSkillDependancies(Character)` (l.172328, sem chamador no assembly),
  `resetButton`/`closeButton` (ligados só no prefab) e o slot único de `CancelInterceptor`.

### Notas de implementação

- O jogo **não** tem um modo somente leitura nativo: a garantia vem de **higienizar o ponto de gravação antes que ele execute**, e não de bloqueá-lo. Se essa higienização falhar, o mod **não deixa o original rodar** e fecha a janela por conta própria — zero escrita em qualquer estado.
- Nenhum arquivo do jogo é modificado; desinstalar é apagar a pasta do mod.
- Compatibilidade declarada: Stolen Realm **v1.3.1**.
- Ícone: arte do autor redimensionada para 256×256. O original de 1254×1254 **não está versionado** no repositório (ver a seção *Ícone* do `README.md`).
