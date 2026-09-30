# Changelog — RoguelikeSkillTreeVisualizer

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
