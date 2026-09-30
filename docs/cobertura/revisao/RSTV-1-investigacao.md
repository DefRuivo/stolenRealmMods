# RSTV-1 — Investigação obrigatória (13 pontos)

> Entregue 30/09 — tarefa `t_1b74de83` (RSTV-1). **Nenhuma linha de código de mod escrita.**
> A especificação (item 54, 77 itens) manda investigar ANTES de implementar; todo o bloco RSTV depende disto.
>
> **Fonte:** `%LOCALAPPDATA%\hermes\cache\scratch\cs\Assembly-CSharp.decompiled.cs` (decompilado canônico do
> projeto, 371.804 linhas). **Todos os números de linha abaixo são DESSE arquivo.**
> **Reconferência:** cada tipo citado foi re-decompilado por tipo (`ilspycmd -t <Tipo>`) contra a DLL VIVA do jogo
> (`E:\SteamLibrary\...\Stolen Realm_Data\Managed\Assembly-CSharp.dll`) e os nomes batem. Nada foi inventado.
> **ModAPI:** os tipos `StolenRealmModAPI.UI.SkillTreeUIPatches` e `SkillTreeUI` foram decompilados do DLL 0.1.0
> (backup) e entram no fim como MAPA de técnica — a API está quebrada no build atual (ver seção), **nunca** como dependência.

## Veredito geral

| # | ponto | veredito |
|---|---|---|
| 1 | controller da tela (Roguelike → Select Party) | **PROVADO** — `CharacterChoiceManager : UIWindow` (l.208094) |
| 2 | init/refresh da tela | **PROVADO** — `OpenCharacterChoiceManager` (l.208278) + `RefreshCharacters` (l.208420) / `ExecuteRefreshCharacters` (l.208320) |
| 3 | botão `Choose Powerups` (hierarquia/RectTransform/listener) | **PARCIAL** — campo, tipo, visibilidade e handler provados (l.208096/208236/208244); hierarquia/âncoras/dimensões/fiação do UnityEvent vivem no PREFAB → probe de runtime |
| 4 | botão pequeno do canto dos cards (referência visual) | **PROVADO** — `skillTreeRemovalBtn` (l.207666) + `CharacterTileStyle` (l.49667) + `UIButtonController` (l.215682) |
| 5 | sprite do ícone (reutilizar o original) | **PARCIAL** — campos provados (`SkillTreeIconSprite` l.49721; `TreeIcons` l.136564 via `GetTreeIcon` l.165094); nome do asset do glifo = probe de runtime |
| 6 | método real de ADD character | **PROVADO** — cadeia `OnPointerClick` (l.208072) → `MouseDown` (l.207978) → `SelectCharacterTile` (l.208605) → `ToggleSelectedCharacter` (l.208425) |
| 7 | método de REMOVE | **PROVADO** — mesmo `ToggleSelectedCharacter`, ramo false (l.208434); exclusão `DeleteCharacter` (l.208587); in-game `RemoveCharacterFromGame` (l.143576) |
| 8 | identidade do jogador LOCAL / ownership | **PROVADO** — `Character.Owned` (l.32261) via `NetworkId`; `AllMyCharacters` (l.107707); `MyCharacters` (l.144804); `ControllerPlayerId` (l.31087, set l.208471) |
| 9 | controller do `Campaign → Change Skills` | **PROVADO** — `CharacterMenusManager.OpenSkillTreeMenu` (l.48443); `Character.ShowSkillTree` (l.119314) |
| 10 | método que abre o viewer + parâmetros + Character + estado global | **PROVADO** — `SkillTreeManager.Initialize` (l.172380); Character **NÃO** é parâmetro (vem de `GameLogic.CurrentlySelectedCharacter`, l.108082) |
| 11 | read-only | **PROVADO (com nuance)** — NÃO existe flag nativa; freios parciais já existem e as superfícies que persistem estão mapeadas |
| 12 | rastreio do último Character LOCAL | **ESTRATÉGIA** definida sobre base provada (hook l.208425/208605; filtro l.32261/207980; fallback l.140418/140373; vazio desabilita l.208237) |
| 13 | divisão da largura do `Choose Powerups` | **ESTRATÉGIA** + precedente REAL no jogo (`ApplyConnectionWidth` l.207893) ; layout do prefab = probe de runtime |

**9 dos 13 pontos fechados com classe/método/linha (1, 2, 4, 6, 7, 8, 9, 10, 11); o 12 é estratégia sobre base provada;
os pontos 3, 5 e 13 têm o núcleo provado e um item cada que mora no PREFAB/asset** — geometria/fiação do `Choose Powerups`,
nome do asset do glifo e layout da linha — e só um probe de runtime fecha (receita no fim).

---

## 1. Controller/MonoBehaviour da tela "Select Party"

**Classe real: `CharacterChoiceManager : UIWindow` (l.208094)** — é ELA que tem o botão `Choose Powerups`.

- `public static CharacterChoiceManager Instance` / `ForcedInstance` (l.208155/208157); carregada sob demanda por
  `ReferenceLoader.CharacterChoiceManagerReference` (l.162614) + `LoadReference(...)` (l.208215).
- O botão roguelike só aparece nessa tela: `roguelikePowerupButton.gameObject.SetActive(Root.PlayingRoguelike)` (l.208236).
- Estado de tela: `GUIManager.instance.CurrentGuiState = GUIState.ChoosingCharacter` (l.208280) — a "Select Party" do roguelike.
- O fluxo aceita party em roguelike com ramo próprio (l.208549-208556) e filtra personagens por `IsRoguelikeCharacter` (l.208376).
- Chamada de inúmeros lugares: l.97358, 119349, 151591, 163992, 178347, 188451, 192818, 209988, 212171.

Vizinhos na mesma janela (campos públicos): `skillTreeRemovalWindow` (l.208098), `acceptBtn` (l.208130),
`togglePartyBtn` (l.208124), `unreadyBtn` (l.208126), `mainMenuBtn` (l.208128), `characterChoicePrefab` (l.208106),
`partyHolder` / `notInPartyHolder` (l.208108/208110).

## 2. Inicialização / refresh da tela

- **Entrada:** `OpenCharacterChoiceManager()` (l.208278) → seta `GUIState.ChoosingCharacter`, chama `RefreshCharacters()`,
  ativa o GameObject, `inputBlocker` off, `ControlFooter.Show()`.
- **Refresh:** `RefreshCharacters()` (l.208420) → `StartCoroutine(ExecuteRefreshCharacters())` (l.208320). A coroutine
  espera `partyChar.IsNetworkLoaded` (l.208326-208340), instancia/reaproveita os cards (`Object.Instantiate(characterChoicePrefab, partyHolder)` l.208360),
  reordena os de fora por `LastTimePlayed` (l.208375-208379), popula `partySlots` com `partyChars[j]` (l.208388) e no fim
  liga o accept (`acceptBtn.interactable = ... MyCharacters.Where(SelectedForBattle).Count() > 0 && num <= 6`, l.208417).
- **Outros pontos de vida:** `Start()` (l.208225), `Update()` (l.208231 — roda TODO FRAME: `ShowPendingSkillTreeRemovalPrompt`,
  visibilidade do `roguelikePowerupButton`, `acceptBtn.interactable`), `ResetCharacterChoice()` (l.208219), `DeleteTiles()` (l.208287),
  `OpenWindow()`/`CloseWindow()` override (l.208615/208622).
- ⚠️ `ExecuteRefreshCharacters` é **coroutine** (IEnumerator, l.208320): patch Harmony nela é ruim; os pontos de postfix
  práticos são `OpenCharacterChoiceManager` (l.208278) e `RefreshCharacters` (l.208420).

## 3. O botão `Choose Powerups` — o que dá e o que não dá para provar no assembly

**Provado:**
- Campo: `public Button roguelikePowerupButton` (l.208096) — é um `UnityEngine.UI.Button` serializado do prefab.
- Visibilidade: recalculada **a cada frame** por `Root.PlayingRoguelike` (l.208236) — fora do roguelike ele some.
- Ação do clique: `CharacterChoiceManager.OpenRoguelikePowerupWindow()` (l.208244) → `RoguelikePowerupWindow.ForcedInstance.OpenPowerupWindow()`
  (l.164675: `OpenWindow(); SetActive(true); ControlFooter.Hide()`).
- O rótulo é texto de prefab localizado por `PrefabLocalizer` (l.156288): o `Awake` (l.156290) varre TODOS os `Text`/`TMP_Text`
  filhos e registra em `OptionsManager.AddUITextToLocalize` / `LocalizeUIText` (l.156306-156311).
- **Não existe** `roguelikePowerupButton.onClick.AddListener(...)` em lugar nenhum do assembly (grep: só 2 ocorrências do
  campo — declaração e o `SetActive`). A fiação é **UnityEvent persistente do prefab**.

**SEM PROVA (prefab/instância, não assembly):** hierarquia exata, pai (linha/container), `RectTransform`/anchors/pivot,
width/height, se o pai tem `HorizontalLayoutGroup`/`VerticalLayoutGroup`, e o listener persistente (`GetPersistentEventCount()`/`GetPersistentMethodName(0)`).
→ probe de runtime (receita no fim). Nada disso impede o RSTV-3; só confirma na hora de injetar.

## 4. O botão pequeno do canto superior direito dos cards (referência visual)

**Classe real: `CharacterChoiceItem : MonoBehaviour` (l.207638), campo `skillTreeRemovalBtn` (l.207666).**

- Prefab: o card é `CharacterChoiceManager.characterChoicePrefab` (l.208106); o botão é filho do card.
- Posição/tamanho vêm do asset `CharacterTileStyle` (l.49667), aplicados em `ApplySkillTreeButtonStyle()` (l.207908):
  - âncoras: `anchorMin = anchorMax = (1,1)`, `pivot = (1,1)` (l.207915-207917) → **canto superior direito**;
  - `sizeDelta = Style.SkillTreeButtonSize` (l.207918) — default **24×24** (l.49708);
  - `anchoredPosition = Style.SkillTreeButtonOffset` (l.207919) — default **(−4,−4)** (l.49711);
  - placa: `skillTreeRemovalBtnPlate` (l.207675) recebe `Style.SkillTreeButtonSprite` (l.49714), tipo `Image.Type.Sliced`,
    `pixelsPerUnitMultiplier = Style.SkillTreeButtonPixelsPerUnitMultiplier` (l.207926-207927);
  - cor/estados: `UIButtonController.UIButtonColor = Style.SkillTreeButtonColor` (l.207929-207933);
  - ícone: `skillTreeRemovalBtnIcon` (l.207678) recebe `Style.SkillTreeIconSprite` (l.49721), `Style.SkillTreeIconColor`,
    padding uniforme `SkillTreeIconPadding` (default 5, l.49724) via offsets (l.207941-207945);
  - liga/desliga sem tocar no prefab: `Style.ShowSkillTreeButton` (l.49706), usado na condição l.207823.
- **Transições nativas:** `UIButtonController` (l.215682) escreve o `ColorBlock` do Button com as cores do `MiscSettings`
  (normal/highlighted/selected/pressed/disabled — l.215699-215724; enum `UIButtonColor` l.215727) e adiciona
  `ButtonHoverDectector` (l.215689-215692). O sprite padrão do botão é `Button_Rect_Foreground` — "o botão padrão do jogo,
  que precisa de ao menos 20×20 no multiplicador 1" (tooltip do próprio campo, l.49713).
- **Função original:** `CharacterChoiceItem.OpenSkillTreeRemovalWindow()` (l.207949) → `CharacterChoiceManager.OpenSkillTreeRemovalWindow(character)`
  (l.208249) → `RoguelikeSkillTreeRemovalWindow.Open(character)` (l.165571). Só aparece se `RoguelikeSkillTreeRemoval.CanConfigure(Character)`
  (l.207823; definição l.165085: `character.Owned && PlayingRoguelike && RemovalPointsOwned > 0`).
- Tooltip do botão: `DisabledButtonTooltip` (l.210103) no próprio botão, com `HoverText` trocado em runtime
  ("View Removed Trees"/"Remove Skill Trees", l.207828-207833). `DisabledButtonTooltip` mostra `DisabledText` quando não
  interativo e `HoverText` quando `ShowHoverText` (l.210129-210142) → é a infraestrutura pronta para o tooltip "Skill Trees".

## 5. Sprite do ícone — reutilizar o ORIGINAL

- **Glifo (ícone):** `CharacterTileStyle.SkillTreeIconSprite` (l.49721) — o glifo da árvore usado no botão do card.
- **Alternativa/segunda fonte no jogo:** `MiscSettings.TreeIcons` (l.136564) exposto pelo helper
  `RoguelikeSkillTreeRemoval.GetTreeIcon(SkillType)` (l.165094-165107: `miscSettings.TreeIcons[SkillTabTypes.IndexOf(skillType)]`);
  é o que as tabs usam (l.173756).
- **Placa (sprite do botão):** `CharacterTileStyle.SkillTreeButtonSprite` (l.49714) — o tooltip do campo nomeia
  **`Button_Rect_Foreground`** (l.49713), o sprite padrão de botão do jogo.
- Veredito: dá para reutilizar SEM copiar asset para o repo (ler o `Sprite` da instância nativa em runtime).
  **SEM PROVA:** o NOME do asset do glifo (não aparece em código; é atribuído no asset `CharacterTileStyle`) → probe de runtime.

## 6. Método REAL de ADD character na party

Cadeia completa (mouse):
1. `CharacterChoiceItem.OnPointerClick(PointerEventData)` (l.208072): `pointerId == -1` (esquerdo) → `MouseDown(playerId)`;
   `pointerId == -2` (direito) → menu de opções.
2. `CharacterChoiceItem.MouseDown(int controllerPlayerId)` (l.207978) — **gate de dono**: só segue se
   `Character == null || GameLogic.instance.AllMyCharacters.Contains(Character)` (l.207980).
3. `CharacterChoiceManager.SelectCharacterTile(this, toggle: true, controllerPlayerId)` (l.208605) → `ToggleSelectedCharacter(controllerPlayerId)` (l.208610).
4. **`CharacterChoiceManager.ToggleSelectedCharacter(int controllerPlayerId)` (l.208425)** — o ADD é o ramo else (l.208440):
   `CanAddCharacter` (l.208442; definição l.208189: `SelectedForBattle.Length < partyMax(6)`), validação de variância de
   nível no roguelike (l.208449-208453), hardcore (l.208454-208463), `Root.AddToCharacterList(character)` se ainda não
   estiver em `AllCharacters` (l.208466; definição do método l.144124), **`character.SelectedForBattle = true`** (l.208470),
   **`character.ControllerPlayerId = controllerPlayerId`** (l.208471).

O que "estar na party" significa no modelo de dados:
- `Root.CharactersInBattle` = `AllCharacters` onde `SelectedForBattle` (l.140373).
- `Root.PartyCharactersUnaccepted` = `CharactersInBattle` onde `!IsAI` (l.140418) — é a lista que a tela usa (`partyChars` l.208322).
- `Root.PartyCharacters` (party ACEITA) = `CharactersInBattle` onde `!IsAI && CharacterType.Normal && AcceptedPartyByConnection[OwnerID]` (l.140412).
- Confirmação oficial: `CharacterChoiceManager.AcceptCharacterChoices()` (l.208545) → `GameLogic.instance.AcceptCharacterChoices()` (l.108681)
  → `Root.ChangeAcceptedPartyStateFromServer(NetworkId, true)` (l.108687; definição l.144465) → coroutine `ExecuteAcceptCharacterChoices`
  (l.108710) que espera `Root.AcceptedPartyByConnection[NetworkId]` (l.108713) e `MyPartyCharacters.Count() > 0` (l.108717)
  → `CurrentlySelectedCharacter = NetworkingManager.Instance.MyPartyCharacters.First()` (l.108727).

**Corolário para o RSTV-4:** o "add" do jogador local é observável em `ToggleSelectedCharacter`/`SelectCharacterTile` com o
personagem-alvo (o filtro de dono já está no `MouseDown`, l.207980).

## 7. Método de REMOVE

- Mesmo `ToggleSelectedCharacter` (l.208425), ramo `if (SelectedForBattle)` (l.208432): `Character.SelectedForBattle = false`
  (l.208434) + `RefreshCharacters()` (l.208437) → o personagem sai de `CharactersInBattle` e portanto de `PartyCharactersUnaccepted`.
- Exclusão definitiva do personagem: `CharacterChoiceManager.DeleteCharacter()` (l.208587) → `character.DeleteCharacter()` (l.208593).
- Remoção in-game (desconexão/morte): `Root.RemoveCharacterFromGame(Character, bool addToUnusedPool = false)` (l.143576; só no servidor, l.143578).
- Ao reabrir a seleção: `OpenChooseCharacterMenu()` (l.119347) reseta `AcceptedPartyByConnection[meuId] = false` (l.119359) e
  desmarca mortos em hardcore (l.119360-119367) + `RefreshCharacters()` (l.119368).

**Corolário para o RSTV-4:** a invalidação de histórico tem que escutar o ramo false do toggle e a exclusão; o objeto
Unity pode continuar vivo (o card some, o `Character` não).

## 8. Como o jogo identifica o jogador LOCAL e o ownership do Character

- **Ownership:** `Character.Owned` (l.32261-32271): `OwnerID == NetworkingManager.Instance.NetworkManager.NetworkId && !IsAI`.
  - `Character.OwnerID` (l.31084; auto-propriedade observável); `Character.ControllerPlayerId` (l.31087).
  - `OwnerID` é atribuído na criação local (l.108843), em massa no load ("cada AllMyCharacter recebe meu NetworkId", l.144690-144693)
    e no re-merge de party (l.144684).
- **Quem é o jogador local:** `NetworkingManager : MonoBehaviour` (l.144748) → `NetworkManager.NetworkId` (byte) e
  `NetworkingManager.Instance.NetworkManager.NetworkId`; `IsServer => NetworkManager.NetworkId == 0` (l.144847);
  `IsPlayingAsSinglePlayer` (l.144810).
- **Listas "minhas":** `NetworkingManager.MyCharacters` = `Root.AllCharacters` onde `Owned` (l.144804);
  `NetworkingManager.MyPartyCharacters` (l.144807) = `Root.MyPartyCharacters` = `PartyCharacters` onde `Owned` (l.140415);
  `MyPartyCharactersUnaccepted` (l.144841); `GameLogic.AllMyCharacters` (l.107707 — lista local mantida no cliente, ver add em l.108845).
- **Controller local dentro da conexão:** `MouseDown(controllerPlayerId)` → `ToggleSelectedCharacter(controllerPlayerId)` grava
  `Character.ControllerPlayerId` (l.208471); o id do ponteiro vem de `PlayerPointerEventData.playerId` (l.259139); o jogo usa
  `ControllerPlayerId` para mapear por controle (`MyPartyControllerPlayerIdToCharacters`, l.144823) e para a cor do card
  (`GetPlayerControllerColor(OwnerID, ControllerPlayerId)`, l.140907; uso l.207721).
- **Gates reais de UI:** o card do PRÓPRIO personagem é clicável (l.207980); o menu de opções exige `Character.Owned` (l.208038);
  o botão de remoção exige `Owned` (l.165085); `CurrentlySelectedCharacter` recusa value não-`Owned` (l.108117).

## 9. O controller que o `Campaign → Change Skills` usa

- **`CharacterMenusManager : UIWindow` (l.48271)** — a janela com as abas (`TabCharacter` l.48293, **`TabSkillTree` l.48295**, `TabFortunes` l.48297).
- Entradas: `Character.ShowSkillTree()` (l.119314: campanha → `OpenSkillTree(CurrentlySelectedCharacter.SkillsFromPoints.ToList())` l.119334)
  e `Character.OpenSkillTree(List<SkillInfo>)` (l.119480) → `CharacterMenusManager.Instance.OpenSkillTreeMenu(learnedSkills)` (l.48482).
- **`OpenSkillTreeMenu(List<SkillInfo> learnedSkills, bool ignoreOwnedCheck = false)` (l.48443)** — o método central:
  - exige `AllMyCharacters.Contains(CurrentlySelectedCharacter)` salvo `ignoreOwnedCheck` (l.48445);
  - abre a janela se preciso (l.48449-48452), seleciona a aba `TabSkillTree` (l.48453);
  - **ramo ROGUELIKE** (`Burst2Flame.Game.Instance.RoguelikeModeActive`, l.48456): instancia `SkillTreeManagerRoguelike`
    (l.48458-48465) e chama `ShowRoguelikeSkillTree(CurrentlySelectedCharacter)` (l.48467);
  - **ramo CAMPANHA** (l.48469-48484): instancia `SkillTreeManager` (l.48473), `Initialize(learnedSkills, unspentPoints, creating)` (l.48481),
    `SetActive(true)` (l.48482), som de menu (l.48483).
- `CloseSkillTreeMenu()` (l.48490): **o fechamento do jogo COMMITA** — `SkillTreeManager.AcceptSkillChanges(closeMenu: true)` (l.48494).
- `ToggleSkillTreeMenu()` (l.48502); tabs via `MenuTabManager.SelectButton(TabSkillTree)` (l.48453); `SkillTreeManager` vem de
  `ReferenceLoader.SkillTreeManagerReference` (l.162626).

## 10. Método que ABRE o viewer: parâmetros, Character e estado global

- **`SkillTreeManager.Initialize(List<SkillInfo> learnedSkills, int unspentPoints, bool creating = false)` (l.172380).**
  - `creating=false` → skills vão para `SkillsOnEnter`, fader off (l.172416-172427), `needsAccept = true` (l.172382).
  - O **Character NÃO é parâmetro** — o viewer lê `GameLogic.instance.CurrentlySelectedCharacter` por dentro:
    l.172388 (popup de reorganização), l.172505/172516/172525 (`AcceptSkillChanges`), l.172665 (`BeginRespec`), l.172823 (`RefreshRespecFooter`).
  - `creating` alimenta `GUIManager.instance.CurrentGuiState` no chamador (l.48480-48481) e decide o modo de criação.
- **Estado global envolvido:** `GameLogic.CurrentlySelectedCharacter` (l.108082) — inclusive `GUIState.ChoosingCharacter` da Party Select;
  `GUIManager.instance.CurrentGuiState` (l.48480 e l.172506); `MenuTabManager.SelectButton(TabSkillTree)` (l.48453); `ControlFooter`
  (l.48485-48486); `AnyWindowOpen()` (l.48487); e a instância `LoadableUIWindow<SkillTreeManager>` (l.172045 / `ReferenceLoader` l.162626).
- **Contraponto importante (dois precedentes de API que ACEITAM o Character por parâmetro):**
  - `SkillTreeManagerRoguelike.ShowRoguelikeSkillTree(Character character)` (l.173328; usa `character.SkillsFromPoints` l.173357).
  - `RoguelikeSkillTreeRemovalWindow.Open(Character character)` (l.165571; guarda `CurrentCharacter`, l.165509/165575).
- ⚠️ **Armadilha do modo roguelike:** chamar `CharacterMenusManager.OpenSkillTreeMenu` durante a run cai no ramo roguelike (l.48456)
  e abre o `SkillTreeManagerRoguelike`, NÃO o `SkillTreeManager` do Campaign → Change Skills. Para o mod, o caminho é
  **replicar o ramo campanha** (l.48469-48484): garantir a instância (l.48473) + `Initialize(character.SkillsFromPoints.ToList(), character.UnspentSkillPoints, creating: false)` (como o jogo faz l.108164) + `SetActive(true)`.
- ⚠️ **Abrir para OUTRO personagem**: o setter de `CurrentlySelectedCharacter` (l.108088-108179) recusa não-`Owned` (l.108117),
  **commita** pendências do skill tree se ele estiver ativo (`AcceptSkillChanges()` l.108137), **re-inicializa** o viewer com os
  dados do novo valor (l.108164) e mexe em camera/IsPartyLeader/estado de movimento (l.108121-108157). Trocar o global "na marra"
  no clique é a opção mais arriscada; a alternativa cirúrgica é patchear apenas as leituras internas do viewer enquanto a nossa
  sessão estiver ativa (as linhas acima são TODAS as leituras).

## 11. Read-only: existe modo nativo? O que persiste?

- **NÃO existe flag nativa.** Busca no decompilado por `readOnly`/`ReadOnly`/`preview`/`inspect`/`allowChanges`/`editingEnabled`/
  `IsViewOnly`/`viewOnly` só retorna coisas alheias (Sirenix, `ReadOnlyCollection` de PlayFab/Skills registry). O viewer não tem
  preview/inspect/readonly. → **estratégia: reusar a interface e bloquear SÓ o que persiste.**
- **Freios que JÁ existem (a nosso favor):**
  - `RefreshRespecFooter()` (l.172821): `RespecButton.SetActive(active)` só para character local (l.172824/172867) e
    `interactable = CanRespecSkills(character)` (l.172871); **`CanRespecSkills` exige `GUIManager.instance.CurrentGuiState == GUIState.InTown`**
    (l.172640-172651). Na Party Select o estado é `ChoosingCharacter` → respec NASCE desligado.
  - `ApplyButton`/`ResetAllButton` só interagem em `InRespecMode` (l.172876-172881); `BeginRespec` exige `CanRespecSkills` (l.172665).
  - `AcceptSkillChanges` sai cedo quando `needsAccept == false` (l.172496-172499) — há um freio interno.
  - `SkillTreeItem.ToggleAddToSkillToAddList()` (l.171967): fora do respec mode, clicar em skill já aprendida é no-op (l.171979-171999).
- **O que PERSISTE (os alvos do bloqueio):**
  - acúmulo de `SkillsToAdd` pelo clique (l.172022);
  - `AcceptSkillChanges` (l.172494) → `CurrentlySelectedCharacter.RemoveSkills(...)` + `AddSkills(SkillsToAdd)` (l.172525-172526);
  - `ApplyRespec` (l.172709) → `CommitSkillChanges` (l.172791) → `RemoveSkills`/`AddSkills` (l.172797-172798);
  - `ResetAllSkills` (l.172733), `ResetSkillPoints` (l.173274) → `Character.ResetSkills()` (l.37474);
  - os gravadores no Character: `AddSkill`/`AddSkills`/`RemoveSkill(s)` (l.37494-37547, todos com `QueueCharacterSave()`), `ResetSkills` (l.37474) e `QueueCharacterSave` (l.37480/37499/37511/37525/37541).
- **Fechar/voltar sem alterar nada:** o fechamento nativo COMMITA (`CloseSkillTreeMenu` → `AcceptSkillChanges(closeMenu:true)` l.48494).
  O mod precisa: manter `SkillsToAdd` vazio (ou limpar no fechamento), e garantir que `AcceptSkillChanges`/`ApplyRespec`/
  `ResetAllSkills`/`ResetSkillPoints` não rodem na nossa sessão. Campos públicos úteis: `closeButton` (l.172059), `backBtn` (l.172069),
  `acceptButton` (l.172055), `resetButton` (l.172057), `SkillsToAdd`/`SkillsOnEnter` (l.172083-172085), `InRespecMode` (l.172211).
- Navegação/leitura que NÃO persiste e deve continuar: `ChooseTree` (l.172559), `PopulateTree` (l.172583), tooltips
  (`SkillTreeItem` hover l.171950-171958), `SwitchSelectedTree` (l.172357), backgrounds/zoom (estilo l.173105+).

## 12. Rastrear o último Character LOCAL (com fallback)

Base provada (não é chute):
- **Ponto de hook:** `CharacterChoiceManager.ToggleSelectedCharacter(int controllerPlayerId)` (l.208425) — ou o anterior
  `SelectCharacterTile` (l.208605). É o único lugar onde o estado "acabei de adicionar" nasce (`SelectedForBattle = true`, l.208470)
  com o dono já filtrado a montante (l.207980 `AllMyCharacters.Contains`).
- **Filtro de local:** `Character.Owned` (l.32261) / `GameLogic.instance.AllMyCharacters.Contains(character)` (l.207980, l.108271).
  Não usar ordem de `Root.MyPartyCharacters` (ordem = `CharactersInBattle`, não ordem de add, l.140412-140415) nem "último global".
- **Histórico + validação no clique:** manter lista (do mais recente para o mais antigo). Validar no clique: `character != null`,
  objeto Unity válido, `Owned`, e ainda em `Root.PartyCharactersUnaccepted` (l.140418, cuja condição é `SelectedForBattle`, l.140373).
- **Fallback:** primeiro item do histórico que ainda passa na validação; **party vazia → `button.interactable = false`**.
  Precedente do próprio jogo para gate por party local: `acceptBtn.interactable = ... MyPartyCharactersUnaccepted.Count > 0` (l.208237).
- **Invalidação no REMOVE:** ramo false do toggle (l.208434), `DeleteCharacter` (l.208587), `RemoveCharacterFromGame` (l.143576).

## 13. Dividir a largura do `Choose Powerups`

Estratégia (com o precedente REAL do jogo):
- Medir em runtime a largura atual de `roguelikePowerupButton` (`RectTransform.rect.width`) — é `availableWidth`.
- `newChoosePowerupsWidth = availableWidth − larguraDoBotaoClonado − spacing` (largura do clonado = do próprio botão nativo clonado;
  a referência do card é 24×24, l.49708 — não inventar número, ler do clone).
- O jogo JÁ faz esse tipo de "abrir espaço para o botão" no card: `CharacterChoiceItem.ApplyConnectionWidth(bool)` (l.207893-207906)
  desloca `rectTransform.offsetMax` do texto usando `Style.SkillTreeButtonOffset.x - Style.SkillTreeButtonSize.x - Style.ConnectionButtonGap`
  (l.207902) e ainda aplica `TextOverflowModes.Ellipsis` (l.207904). É o padrão a imitar (nada de coordenada global fixa).
- Se a linha do `Choose Powerups` tiver layout group, o jeito idiomático do jogo é `LayoutElement.preferredWidth/minHeight`
  (padrão em `SkillTreeManager.ApplyActionButtonStyle`, l.172969-172975) — decidir `sizeDelta` vs `preferredWidth` SÓ depois de ler o prefab.
- Piso de tamanho para o sprite padrão `Button_Rect_Foreground`: **≥20×20 no multiplicador 1** (l.49713) — o RSTV-3 deve
  respeitar isso ao encolher.
- **SEM PROVA:** se o pai tem `HorizontalLayoutGroup`/`VerticalLayoutGroup` e os valores atuais de width/anchors → probe de runtime.

---

## Riscos

### Multiplayer
- Ownership é por DONO DA CONEXÃO: `OwnerID == NetworkManager.NetworkId` (l.32265). `OwnerID` é reatribuído no load (l.144684/144692)
  e o `NetworkId` é byte por conexão — nada de deduzir "meu" por posição na lista.
- **`CurrentParty.Last()` não existe no código** (grep "CurrentParty" só acha `CurrentPartyEventPending`); o equivalente errado no
  modelo REAL é `Root.MyPartyCharacters.Last()` / `PartyCharacters.Last()`, que ordenam por `CharactersInBattle` (ordem de
  `AllCharacters`, l.140373) — **não é ordem de adição**. O cenário P1 add August, P2 add Aragorn, P1 add Wyatt, P2 add Necrodancer
  (RSTV-4) só funciona com histórico por jogador, filtrado por `Owned`.
- O add local passa por `Root.AddToCharacterList` (l.208466 → l.144124), que é replicado pela rede; o ACCEPT é por conexão
  (`AcceptedPartyByConnection`, l.140412/144845) e `ChangeAcceptedPartyStateFromServer` (l.144465). O clique de OUTRO jogador
  NUNCA chega no nosso `ToggleSelectedCharacter` (o card dele nem é clicável, l.207980) — o risco é ler estado compartilhado
  (`CharactersInBattle`, l.140373) e achar que ele é "meu".
- Desconexão mexe em ownership: `OnClientDisconnected` (l.144696+) reatribui `OwnerID` dos personagens (l.144715). Validar
  o histórico no clique cobre isso.

### Duplicação do botão
- A janela é PERSISTENTE: `CharacterChoiceManager` é carregada uma vez por `ReferenceLoader.LoadReference` (l.208215) e
  reaproveitada; `OpenCharacterChoiceManager` (l.208278) é chamada a cada entrada na tela.
- O `roguelikePowerupButton` tem `SetActive` recalculado **todo frame** (l.208231-208236) — o nosso botão deve seguir a mesma
  visibilidade (ou reagir ao mesmo `Root.PlayingRoguelike`), senão aparece "sozinho" fora do roguelike ou some com o painel.
- `ExecuteRefreshCharacters` (l.208320) instancia cards em várias voltas e é chamada repetidas vezes — nada no fluxo garante
  "1 botão por janela", então: nome fixo (ex.: `RoguelikeSkillTreeVisualizer_Button`), checagem de existência ANTES de criar
  (busca por nome no parent do `roguelikePowerupButton`), e destruir junto com a janela.
- O clique do botão nativo NÃO é rewired em código (só a UnityEvent do prefab) — ao clonar, é obrigatório remover TODOS os
  listeners antigos (`onClick.RemoveAllListeners()`) antes de adicionar o nosso (o clonado herdaria o `OpenRoguelikePowerupWindow`).

### Persistência (read-only)
- Não há flag read-only (ver ponto 11). O fechamento nativo **commita**: `CloseSkillTreeMenu` → `AcceptSkillChanges(closeMenu:true)`
  (l.48494); `AcceptSkillChanges` grava via `Character.AddSkills/RemoveSkills` (l.172525-172526 → l.37503/37533) e
  `QueueCharacterSave` (l.37500+). `ApplyRespec`/`CommitSkillChanges` (l.172709/172791), `ResetAllSkills` (l.172733) e
  `ResetSkillPoints` (l.173274 → `Character.ResetSkills` l.37474) são as outras portas.
- `needsAccept = true` é setado por `Initialize` (l.172382) — o mod deve manter `SkillsToAdd` vazio e/ou neutralizar as portas acima
  durante a sessão de visualização; senão "navegar e ler" vira "salvar sem querer" pelo simples fechamento.
- Trocar `GameLogic.CurrentlySelectedCharacter` para abrir o viewer de outro personagem tem efeito colateral: o setter COMMITA
  pendências do skill tree ativo (l.108137), re-inicializa o viewer (l.108164) e ainda recusa não-`Owned` (l.108117). Se o mod
  precisar apontar o viewer para outro personagem, o caminho seguro é substituir SÓ as leituras listadas no ponto 10.

---

## Referência: o que a StolenRealmModAPI (0.1.0) já faz (mapa, NUNCA dependência)

DLL examinada: `scratch/backups/StolenRealmModding-StolenRealmModAPI.0.1.0.bak/StolenRealmModAPI.dll`
(cópia de trabalho em `$TMPDIR/rstv/ModAPI.dll`; decompilada só com `-t`, sem `-o`).

- **`StolenRealmModAPI.UI.SkillTreeUIPatches`** — patch Harmony em `SkillTreeManager.UpdateSkillTreeItems` (o nosso `UpdateSkillTreeItems`, l.172294):
  - `Prepare()` → `ReflectionHelper.FindType("SkillTreeManager") != null` (gate de segurança por nome);
  - `TargetMethod()` → `AccessTools.Method(type, "UpdateSkillTreeItems")`;
  - `Postfix(object __instance)` → `SkillTreeUI.OnUpdateSkillTreeItems(__instance)`, com try/catch.
- **`StolenRealmModAPI.UI.SkillTreeUI`** — registra tabs extras e injeta de forma preguiçosa no primeiro `UpdateSkillTreeItems`.
  Lê por reflexão os campos REAIS do manager: `skillTabTypes` (l.172089), `skillTreeTabs` (l.172168, componentes `SkillTreeTab` l.173685),
  `skillTreeShowers` (l.172087, componentes `SkillTreeShower` l.212851) e `skillItemContainer` (l.172065);
  clona a última tab (`UIFactory.Clone`) como `SkillTreeTab_<Nome>`, seta o campo `skillType`; clona o último shower como
  `SkillTree_<Nome>`, seta o campo `Type` e adiciona em `skillItemContainer`.
  → Confirma os PONTOS DE EXTENSÃO da árvore nativa (conecta com os pontos 9/10 deste relatório).
- **Atenção:** a API está QUEBRADA no build atual (o `SkillRegistryPatches.GameAwakePatch` mira `Game.Awake` via
  `AccessTools.Method` e o patch falha no boot — TargetMethod null). Reproduzido no exame: `Prepare()` por nome + `TargetMethod()`
  por string é a TÉCNICA correta a imitar, mas a API não pode virar dependência runtime deste mod (RSTV-2 é BepInEx+Harmony puro).

## O que ainda é SEM PROVA (e como fechar — NÃO feito aqui de propósito)

Três itens vivem no PREFAB/asset e são proibidos de provar por código sem abrir o jogo (a regra do RSTV-1 era só investigar):
1. **Ponto 3**: hierarquia/pai/âncoras/width/height do `roguelikePowerupButton` e o listener persistente
   (`Button.onClick.GetPersistentEventCount()` / `GetPersistentMethodName(0)`).
2. **Ponto 5**: NOME do asset do glifo (`CharacterTileStyle.SkillTreeIconSprite.name`) — ler da instância do card em runtime.
3. **Ponto 13**: se a linha usa `HorizontalLayoutGroup`/`VerticalLayoutGroup` e a largura original a preservar.

Probe sugerido (RSTV-2/3, no primeiro ciclo de jogo — o RoguelikeDebugger já é o canal): dumpar, ao abrir a tela,
- `CharacterChoiceManager.Instance.roguelikePowerupButton` → caminho no hierarchy, pai, `RectTransform` (anchors, pivot, sizeDelta, width),
  componentes do pai (layout groups), `onClick` persistente, texto do filho TMP;
- `partySlots[0].skillTreeRemovalBtn` (ou o card de `partyHolder`) → `style.SkillTreeButtonSprite.name`, `style.SkillTreeIconSprite.name`;
- `GUIManager.instance.CurrentGuiState` no clique (confirmar `GUIState.ChoosingCharacter`).

## Como reconferir (sem abrir o jogo)

```bash
# 1) o decompilado canônico do projeto (linhas citadas aqui)
grep -n "class CharacterChoiceManager"          scratch/cs/Assembly-CSharp.decompiled.cs
grep -n "ToggleSelectedCharacter\|OpenRoguelikePowerupWindow\|roguelikePowerupButton" scratch/cs/Assembly-CSharp.decompiled.cs

# 2) contra a DLL viva, por tipo (NUNCA -o)
"$HOME/.dotnet/tools/ilspycmd" "E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed/Assembly-CSharp.dll" -t CharacterChoiceManager
# ... e os outros: CharacterChoiceItem, CharacterTileStyle, SkillTreeManager, SkillTreeManagerRoguelike,
#                 CharacterMenusManager, RoguelikeSkillTreeRemoval, RoguelikePowerupWindow, ReferenceLoader

# 3) a referência da ModAPI (só técnica)
"$HOME/.dotnet/tools/ilspycmd" "%LOCALAPPDATA%\hermes\cache\scratch\rstv\ModAPI.dll" -t StolenRealmModAPI.UI.SkillTreeUIPatches
"$HOME/.dotnet/tools/ilspycmd" "%LOCALAPPDATA%\hermes\cache\scratch\rstv\ModAPI.dll" -t StolenRealmModAPI.UI.SkillTreeUI
```

**Conclusão curta:** os 4 pontos que mais erram têm resposta no código — (a) ownership real = `OwnerID == NetworkId`
(`Character.Owned` l.32261), não ordem de lista; (b) o contexto é resolvido no clique porque o viewer lê o global
`CurrentlySelectedCharacter` a cada uso (l.172380+); (c) read-only = bloquear as portas que persistem (l.172494/172709/172733/173274/37474+),
sem flag nativa; (d) o botão nativo (clone do `skillTreeRemovalBtn`, l.207666) precisa de anti-duplicação por nome porque a
janela persiste e o `Update` da tela mexe na visibilidade todo frame (l.208231-208236).
