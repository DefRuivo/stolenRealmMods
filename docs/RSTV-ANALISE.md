# RSTV — Análise dos pontos de ancoragem (RoguelikeSkillTreeVisualizer)

**Escopo desta fase:** localizar no decompilado onde a UI que o mod precisa tocar é montada.
Não é implementação. Cada afirmação tem `arquivo:linha`.

**Fonte única:** `%USERPROFILE%\AppData\Local\hermes\cache\scratch\cs\Assembly-CSharp.decompiled.cs`
(371.804 linhas, decompilado do `Assembly-CSharp.dll` do jogo v1.3.1). Abaixo, `l.N` = essa linha.
Não foi lido inteiro — só `grep -n` com contexto. **Nenhum asset foi aberto** (`resources.assets`, 1,7 GB).

---

## 1. A tela "Roguelike → Select Party" é a classe `CharacterChoiceManager`

| o quê | onde |
|---|---|
| `public class CharacterChoiceManager : UIWindow` | l.208094 |
| Interface do modo Roguelike (o botão de powerups só existe aqui) | l.208096, l.208236 |
| Slots da Current Party (`partyHolder`) e dos não-escolhidos (`notInPartyHolder`) | l.208112, l.208114 |
| Capacidade da party: `partyMax = 6` | l.208124 |
| Botão `Accept Party` — campo `public Button acceptBtn` | l.208130 |
| Estado "aceitou a party": `AcceptedParty { get; set; }` | l.208157 |
| A party em si: `partyChars = NetworkingManager.Instance.PartyCharactersUnaccepted` | l.208322 |
| Os meus (Owned): `NetworkingManager.Instance.MyPartyCharactersUnaccepted` | l.208237 |
| Personagens fora da party, ordenados por `LastTimePlayed descending` | l.208375–208379 |
| Tela **aberta**: `public void OpenCharacterChoiceManager()` (seta `GUIState.ChoosingCharacter`, chama `RefreshCharacters()`, `SetActive(true)`) | l.208278 |
| Tela **resetada** a cada abertura: `ResetCharacterChoice()` → `RefreshCharacters(); AcceptedParty = false;` | l.208219 |
| Redesenho completo: `private IEnumerator ExecuteRefreshCharacters()` / `public void RefreshCharacters()` | l.208320 / l.208420 |
| `Update()` da tela (liga/desliga botões, inclusive o de powerups) | l.208231 |

**Consequência para o mod:** a injeção do botão tem um gancho público e idempotente por abertura de tela
(`OpenCharacterChoiceManager`, l.208278) — melhor que a `Update()` (l.208231), que roda todo frame
e já mexe em `acceptBtn`/`roguelikePowerupButton`.

## 2. O botão "Choose Powerups"

| o quê | onde |
|---|---|
| Campo serializado `public Button roguelikePowerupButton;` — **é o único botão de roguelike da tela** | l.208096 |
| Ligado/desligado por modo: `roguelikePowerupButton.gameObject.SetActive(Root.PlayingRoguelike);` dentro do `Update()` | l.208236 |
| **Handler do clique:** `public void OpenRoguelikePowerupWindow()` → `RoguelikePowerupWindow.ForcedInstance.OpenPowerupWindow();` | l.208244 (corpo l.208246) |
| Janela que ele abre: `public class RoguelikePowerupWindow : LoadableUIWindow<RoguelikePowerupWindow>` | l.164569 |
| `public void OpenPowerupWindow()` → `OpenWindow(); SetActive(true); ControlFooter.instance.Hide();` | l.164675 |
| `ForcedInstance` (carrega a referência sob demanda) | l.164583 |

Este é o **modelo de precedente obrigatório** para o botão novo: mesma tela, mesmo tipo de janela
(`LoadableUIWindow<T>`), mesmo padrão de carga preguiçosa — e já provado em jogo que funciona com o
`CharacterChoiceManager` aberto.

**Tipo/prefab/posição:** o `roguelikePowerupButton` é uma **referência de cena serializada** (`Button` do
UGUI, l.208096). Sprite, estados, âncora, tamanho e o `HorizontalLayoutGroup` da linha **não estão no
assembly** — vivem no prefab dentro de `resources.assets`, que não foi aberto. O plano do README
(“clonar um botão nativo, encolher o `Choose Powerups` o necessário, a linha não cresce”) é
implementável em runtime sem ler o asset: clonar o próprio `roguelikePowerupButton`
(`Instantiate`), inserir como irmão à direita via `RectTransform`/`LayoutElement` e travar a linha.

## 3. A tela NATIVA de Skill Trees (`Campaign → Change Skills`) é o `SkillTreeManager`

| o quê | onde |
|---|---|
| `public class SkillTreeManager : LoadableUIWindow<SkillTreeManager>` (`[ExecuteAlways]`) | l.172045 |
| Botão `Change Skills` do menu de personagem (campanha) → `public void OpenSkillTreeMenu()` | l.48424 |
| Sobrecarga que recebe as skills: `public async void OpenSkillTreeMenu(List<SkillInfo> learnedSkills, bool ignoreOwnedCheck = false)` | l.48443 |
| Como ela carrega a janela se ainda não existe: `LoadableUIWindow<SkillTreeManager>.LoadInstanceReference(loader.SkillTreeManager.gameObject, loader.SkillTreeManagerPlaceholder)` + `while (Instance == null) await UniTask.DelayFrame(1);` | l.48471–48480 |
| **Chamada real que inicializa:** `Instance.Initialize(learnedSkills, unspentPoints, GUIManager.instance.CurrentGuiState == GUIState.CreatingCharacter)` | l.48481 |
| `CloseSkillTreeMenu()` chama `AcceptSkillChanges(closeMenu: true)` — **este é o caminho de ESCRITA** | l.48490 (corpo l.48492) |
| Atalho de teclado do jogo: `GUIManager.ShowSkillTree()` (no Roguelike abre a árvore *Roguelike*, não esta) | l.119314 |
| **API central:** `public void Initialize(List<SkillInfo> learnedSkills, int unspentPoints, bool creating = false)` | l.172380 |
| `public void AcceptSkillChanges(bool closeMenu = false)` (faz `RemoveSkills`/`AddSkills` no personagem) | l.172494 |
| `public static bool CanRespecSkills(Character)` — só `true` em `GUIState.InTown` e se for personagem `AllMyCharacters` | l.172640 |
| `public void BeginRespec()` / `InRespecMode` | l.172663 / l.172211 |
| `LoadableUIWindow<T>`: `Instance`, `LoadInstanceReference`, `OnDestroy → Instance = default` | l.131974 / l.131978 / l.132000 |
| Preload: `LoadingScreen.LoadStateBasedResources(GUIState)` cria o `SkillTreeManager` **incondicionalmente** (antes dos testes de estado) | l.132870, bloco l.132890–132898 |
| Referências do asset: `ReferenceLoader.SkillTreeManagerReference` / `SkillTreeManagerPlaceholder` | l.162626 / l.162628 |

### O que a tela exige como contexto do personagem (isto é o nó do problema)

O `SkillTreeManager` **não recebe o `Character` por parâmetro**. `Initialize` só recebe
`learnedSkills` + `unspentPoints` (l.172380); o resto ele lê de **`GameLogic.instance.CurrentlySelectedCharacter`**:

| leitura implícita do contexto | onde |
|---|---|
| `NeedsSkillChangeNotificationList.Contains(GameLogic.instance.CurrentlySelectedCharacter)` | l.172388 |
| `RemoveSkills`/`AddSkills` no fechamento | l.172494–172526 |
| `CanRespecSkills(GameLogic.instance.CurrentlySelectedCharacter)` no rodapé | l.172665, l.172823 |
| `ResetSkills()` | l.173276 |

Ou seja: para mostrar o contexto **real** de um personagem da party, ou se define
`GameLogic.instance.CurrentlySelectedCharacter` antes de abrir (propriedade **pública**, l.108082 —
setter com efeitos colaterais: `IsPartyLeader`, câmera, fecha/repopula outras janelas, l.108090–108180,
e **`if (!value.Owned) return;`** em l.108124 — personagem de outro jogador é recusado), ou o
`SkillTreeManager` mostraria o personagem "selecionado" global, que não é o da party.
`SkillsFromPoints` (a lista que o `Initialize` espera) é público: l.33078.

## 4. "Somente leitura" — o jogo NÃO tem esse conceito pronto

Varredura por `readOnly` / `viewOnly` / `IsReadOnly` / `preview mode` no assembly: **zero flags de
UI somente-leitura**. O que existe são estados parciais, que é o material com que se constrói o
read-only:

| mecanismo existente | onde | serve? |
|---|---|---|
| `creatingMode` (privado) — ativa o `fader` e desvia as skills para `SkillsToAdd` | l.172158, l.172383, l.172416 | não é read-only: em criação dá pra comprar skill |
| `InRespecMode` (privado, `set`) — modo de reespec, só entra via `BeginRespec()` e só se `CanRespecSkills` | l.172211, l.172663 | é o oposto de read-only |
| `RespecButton.SetActive(active)` — `active = !creatingMode && character != null && AllMyCharacters.Contains(character)` | l.172821–172867 | **este é o único gate de permissão de escrita já existente** |
| `lockTiers` / `maxTier` / `tierLimits` | l.172099, l.172100, l.172107 | limita tier, não escreve |
| **Clique no nó da árvore** (compra/descompra) = `SkillTreeItem.ToggleAddToSkillToAddList()` | l.171967 | precisa ser neutralizado |
| `SkillInfo.CanLevel(learnedSkills, freeSkillPoints)` — o gate do clique: `EnoughSkillPoints = freeSkillPoints >= skillsTierCosts[Tier-1]` | l.322947 (l.322961) | com `unspentPoints = 0` **todo** clique de compra já é no-op |
| `AcceptSkillChanges` só age se `needsAccept` (setado `true` por `Initialize`) — é ele que grava | l.172494–172497 | **ponto de bloqueio do único caminho que persiste** |
| Render do nó (cinza / "CannotObtain") | `SkillTreeItem.UpdateSkillTreeItem()` l.171934 | continua funcionando — é o que se quer manter |

**Leitura correta:** dá para montar read-only com (a) `unspentPoints = 0` no `Initialize`,
(b) esconder/desabilitar o rodapé de reespec (`RespecButton`, l.172867) e (c) neutralizar
`AcceptSkillChanges` (l.172494) e `ToggleAddToSkillToAddList` (l.171967) por prefixo Harmony.
Navegação, zoom, abas e tooltips (`Tooltip.ShowSkillTooltip`, l.214240) seguem intactos.

## 5. Contexto do personagem na tela de party (para "o último que EU adicionei")

| o quê | onde |
|---|---|
| Adicionar/remover da party: `public void ToggleSelectedCharacter(int controllerPlayerId)` | l.208425 |
| A escrita que marca entrada: `character.SelectedForBattle = true; character.ControllerPlayerId = controllerPlayerId;` | l.208470–208471 |
| Entrada pelo clique no tile: `public void SelectCharacterTile(...)` | l.208605 |
| A fonte da party: `Root.PartyCharactersUnaccepted => CharactersInBattle.FastWhere(!IsAI)` e `CharactersInBattle => AllCharacters.FastWhere(SelectedForBattle)` | l.140418 / l.140373 |
| Só os meus: `MyPartyCharactersUnaccepted => PartyCharactersUnaccepted.FastWhere(x => x.Owned)` | l.144841 |
| `Character.Owned` | l.32261 |

**O jogo NÃO guarda ordem de adição** — a party é derivada de `AllCharacters` filtrado por
`SelectedForBattle` (l.140373/140418), então "o último que eu adicionei" **não existe como dado**:
o mod precisa registrar o evento de adição (postfix em `ToggleSelectedCharacter`, l.208425, contando
apenas quando o personagem é `Owned` e o `ControllerPlayerId` é local). Isto confirma a regra do
README ("nunca o último global") e diz **onde** implementá-la.

## 6. O que NÃO deu para determinar (e por quê)

1. **Layout do botão** (sprite, tamanho, âncora, se a linha usa `HorizontalLayoutGroup`/`LayoutElement`):
   mora no prefab em `resources.assets` — arquivo não aberto nesta fase. Só o *campo* `Button` está no assembly (l.208096).
2. **Texto do botão** — a string "Choose Powerups" não está no assembly (localização vive nos assets);
   o que liga o campo ao botão é o uso exclusivo em modo roguelike (l.208236) + o handler (l.208244).
3. **Se abrir o `SkillTreeManager` estando a tela de party aberta é seguro** (empilhamento de
   `UIWindowManager.OpenedWindows` / `ControlFooter`): não há chamada no assembly que faça isso hoje —
   é o teste de jogo da próxima fase. O precedente mais próximo é `RoguelikePowerupWindow` (l.164675)
   e a janela de remoção, que é aberta **por cima** desta tela com um `Character` explícito
   (`CharacterChoiceManager.OpenSkillTreeRemovalWindow(Character)` l.208249 → `RoguelikeSkillTreeRemovalWindow.Open(character)`
   l.165571, guardando `CurrentCharacter = character` em l.165575):
   **é o único precedente de "janela com contexto de personagem aberta a partir da Select Party"**.
4. **Se o `fader` do `SkillTreeManager` cobre a tela** (l.172416, `fader.SetActive(creating)`) — só em
   criação; irrelevante para o nosso `creating = false`, mas confirmar em jogo.
5. **Custo de `SkillsFromPoints` em personagem de roguelike** (a árvore roguelike usa
   `SkillsFromPoints` também: `ShowRoguelikeSkillTree` l.173328, laço em l.173357) — não validei se a lista bate 1:1 com a árvore nativa; validar em jogo.

## 7. Próximo passo concreto (implementação)

1. **Botão:** postfix em `CharacterChoiceManager.OpenCharacterChoiceManager` (l.208278) — criar
   **uma vez** por instância: `Instantiate(characterChoiceManager.roguelikePowerupButton, parentDoBotão)`,
   renomear, trocar o `onClick.RemoveAllListeners()` + `AddListener(OpenSkillTreeReadOnly)`,
   e inserir à direita **sem crescer a linha** (herdar `RectTransform`/`LayoutElement` do original,
   encolher o `Choose Powerups` só o necessário). Guardar flag anti-duplicação por instância.
   Ligar/desligar junto do original (`Root.PlayingRoguelike`, l.208236). Botão **desabilitado** com
   `interactable = false` quando a party local está vazia.
2. **Rastreio do personagem:** postfix em `CharacterChoiceManager.ToggleSelectedCharacter` (l.208425),
   registrando `selectedCharacterChoiceItem.Character` quando `Owned` (l.32261) e
   `ControllerPlayerId` local; ao remover (l.208431–208440), cair para o último local ainda em
   `MyPartyCharactersUnaccepted` (l.144841).
3. **Abrir a tela nativa:** `LoadableUIWindow<SkillTreeManager>.LoadInstanceReference(ReferenceLoader.Instance.SkillTreeManager.gameObject, ReferenceLoader.Instance.SkillTreeManagerPlaceholder)`
   seguindo l.48471–48480, depois
   `GameLogic.instance.CurrentlySelectedCharacter = alvo;` (l.108082 — checar o `Owned` de l.108124)
   `Instance.Initialize(alvo.SkillsFromPoints.ToList(), 0, creating: false)` (l.48481/l.172380) e
   `Instance.gameObject.SetActive(true)` (l.48482).
4. **Read-only:** prefixo Harmony em `SkillTreeManager.AcceptSkillChanges` (l.172494) e em
   `SkillTreeItem.ToggleAddToSkillToAddList` (l.171967) quando o modo read-only estiver ativo;
   `unspentPoints = 0` já torna `CanLevel` falso (l.322961); `RespecButton` escondido (l.172867).
   **Nunca** chamar `CloseSkillTreeMenu()` (l.48490) — ele é o caminho que aceita mudanças.
5. **Testar** abrindo o jogo com a tela de party e conferindo `LogOutput.log` (marcador de vida no
   postfix), como manda o ritual de build do repo (`docs/README.md`).