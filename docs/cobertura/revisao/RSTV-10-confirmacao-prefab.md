# RSTV-10 — Confirmação no PREFAB da hierarquia de UI que decide o botão da skill tree

> Tarefa `t_948e2cf0`. O brainstorm (4 propostas + árbitro + advogado do diabo) convergiu em **C+D**
> (botão dentro do `SkillSelectWindow` + atalho F10), aposentando o re-parent da RSTV-9. O advogado do
> diabo marcou tudo como "risco, não fato" porque hierarquia/rect/ORDEM vivem no **prefab**, não no
> decompilado. Este relatório abre o prefab e transforma risco em fato.
>
> **Nada foi alterado.** Somente leitura. Nenhum commit, nenhuma publicação, nenhuma instalação.

**Fonte:**
- `E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm_Data\resources.assets` (1.723.507.220 B) — os **prefabs**.
- `...\Stolen Realm_Data\level1` (2.472.012 B) — a **cena** do jogo, onde ficam o Canvas e os **placeholders**.
- `globalgamemanagers.assets` — os `MonoScript` (as classes dos componentes foram resolvidas pelo externo `fileID 1`).
- Ferramenta: **UnityPy 1.25.3**. Decompilado: `%LOCALAPPDATA%\hermes\cache\scratch\cs\Assembly-CSharp.decompiled.cs`.
- Receita reproduzível: `rstv10_c.py` (maps) → `rstv10_k.py` (componentes + cena) → `rstv10_m.py`/`rstv10_n.py`
  (índices de irmão e classes), todos em `%LOCALAPPDATA%\hermes\cache\scratch\`.

---

## 0. Como o prefab vira UI em jogo (a peça que permite ler o resto)

`ReferenceLoader.ApplyPlaceholderDetails` (l.168068-168079) — o instanciador **de todos** os managers:

```
prefab.transform.parent = placeholder.parent;
prefab.transform.SetSiblingIndex(placeholder.GetSiblingIndex());
component.anchorMin/anchorMax/anchoredPosition/sizeDelta/rotation/localScale = <os do placeholder>;
```

Ou seja: o **rect do ROOT** do prefab instanciado é **sobrescrito pelo placeholder**, e o **índice de
irmão no pai do placeholder** vira o índice de desenho. Os filhos internos do prefab **não** são tocados
— o rect deles é o do prefab. Isso é o que torna a pergunta 2 (ordem dos placeholders) decisiva.

---

## 1. `SkillSelectWindow` — é TELA CHEIA, não painel

Campo: `RoguelikeManager.SkillSelectWindow` (`public GameObject`, l.168597); `CG` = `SkillSelectWindow.GetComponent<CanvasGroup>()` (l.168691).

Filhos do prefab **`Roguelike Manager` [680571]** (root; comps `CanvasRenderer, RectTransform, PrefabLocalizer, RoguelikeManager`):

| GO | `path_id` | comps | é? |
|---|---|---|---|
| `Level Up Sequence Window (Keep Inactive)` | **680553** | CanvasRenderer, RectTransform, **CanvasGroup**, Image, UIWindow | **`SkillSelectWindow`** |
| `Skill Reroll Window` | 680577 | CanvasRenderer, RectTransform, **CanvasGroup**, UIWindow, Image | **`SkillRerollSection`** (l.168637/168872/169183-169200) |
| `Roguelike Level Up Menus (Keep Active)` | 680554 | CanvasRenderer, RectTransform | **sem CanvasGroup** ⇒ não pode ser o `SkillSelectWindow` |

**Como o `SkillSelectWindow` foi fixado (não é adivinhação):** o único par de candidatos com `CanvasGroup`
é {680553, 680577}; 680577 casa com o campo `SkillRerollSection` (a janela de re-roll que o jogo liga e
desliga sozinha); e **680554 não tem `CanvasGroup`** — se fosse `SkillSelectWindow`, `CG.alpha = 0f`
(l.168925, no caminho `zeroOutAlpha: true` de l.168866) estouraria `NullReferenceException` na primeira
subida de nível. Logo **`SkillSelectWindow` = [680553] `Level Up Sequence Window (Keep Inactive)`**.

**RectTransform do `SkillSelectWindow` [680553]:**

```
anchorMin = (0.000, 0.000)   anchorMax = (1.000, 1.000)
pivot     = (0.50, 0.50)     anchoredPosition = (0.0, 0.0)     sizeDelta = (20.0, 20.0)
```

⇒ **TELA CHEIA** (stretch total no canvas). **Não é um painel contido.**

**O painel que o jogador VÊ é descendente, e é pequeno:**

`Roguelike Level Up Menus (Keep Active)` [680554] — anchors `(0.5,0.5)`, `sd (0.0, 154.6)`
→  `Content` [680573] — `aMin (0.000,0.500) aMax (1.000,0.500)`, `ap (0.0,-4.0)`, `sd (293.2, 535.6)`,
comps **`VerticalLayoutGroup + ContentSizeFitter + Image`**.

⇒ o painel visível do level-up mede **≈ 293 × 536 px, centralizado**. O `SkillSelectWindow` que o cerca é
a tela inteira.

> **Consequência dura:** ancorar um filho em `(1,1)` do `SkillSelectWindow` (é exatamente o que
> `RunButton.HomeInLevelUp()` faz hoje: `rt.SetParent(destino)` com o rect do `SkillSelectWindow` e
> `anchorMin=anchorMax=pivot=(1,1)`) coloca o botão no **canto superior direito da TELA**, não no canto do
> painel. Se a intenção era "canto do painel", o pai certo é `Content` [680573] — que tem
> `VerticalLayoutGroup` e `ContentSizeFitter`, então um filho ali **reflui o painel e re-dimensiona o
> `ContentSizeFitter`**.

O `SkillSelectWindow` **não tem LayoutGroup** — um filho livre ali fica livre (sem reflow). Ele tem
`CanvasGroup`, então herda o fade (`alpha` 0→1, l.168925-168927).

---

## 2. ORDEM dos placeholders sob a raiz compartilhada — HUD **antes** da janela do level-up

**Raiz compartilhada = `GUI Manager` [3210] na cena `level1`** — e ela **é o Canvas**:
comps `Canvas, GUIManager, GraphicRaycaster, CanvasScaler`. Rect todo zero (rect de Canvas).
Pai de `GUI Manager` = nenhum (é root de cena).

Ordem dos filhos (`m_Children` = índice de irmão) — os dois que importam:

| placeholder | `path_id` | índice de irmão | rect |
|---|---|---|---|
| `Current Character UI Placeholder` | **581** | **6 de 56** | `aMin(0,0) aMax(1,1) piv(0.5,0.5) ap(0,0) sd(0,0)` |
| `Roguelike Manager Placeholder` | **871** | **24 de 56** | `aMin(0,0) aMax(1,1) piv(0.5,0.5) ap(0,0) sd(0,0)` |

Em uGUI **irmão posterior desenha (e recebe raycast) por cima**. Combinado com `SetSiblingIndex(placeholder.GetSiblingIndex())`:

⇒ **em runtime o `CurrentCharacterUI` fica no índice 6 e o `RoguelikeManager` no índice 24 do Canvas.**
A janela do level-up **desenha POR CIMA do HUD**. Este é o furo transversal que o advogado do diabo
apontou, e ele é **fato de prefab**, não risco.

Para completude: o ramo da árvore (`Skill Tree Placeholder` [1874]) **não** é filho direto do Canvas —
é filho de `Character Menu Manager Window` [3942], que é o **filho 31** de `GUI Manager`. Ou seja, o ramo
da árvore está **acima** do ramo do `RoguelikeManager` (24) no nível do Canvas; a instância da árvore, quando
carregada, é irmã dentro de [3942] e desenha por cima da janela do level-up. (Se `[3942]` está ativo num dado
instante é runtime, não prefab — é o que a RSTV-11a trata por outro caminho.)

---

## 3. A raiz compartilhada é mesmo NUNCA desligada? — **premissa da proposta A confirmada (com ressalva)**

- `GUI Manager` [3210] é o **Canvas** e carrega o componente **`GUIManager`**.
- O código que esconde o HUD no level-up é `GUIManager.Update` (l.120492-120496) e ele chama
  `SetActive` **apenas em `CurrentCharacterUI.Instance.gameObject`** — nunca no Canvas.
- Varredura do decompilado inteiro (496.253 linhas): **nenhum** `SetActive` em
  `GUIManager.instance.gameObject` / em uma raiz de canvas do GUIManager. Os `canvas.SetActive(...)` que
  existem são de outro helper (l.4734-6530) e de `PathCanvas` (l.166021+) — canvases alheios.

⇒ **Durante a run, o Canvas/GUI Manager não é desligado por código.** A premissa da proposta A se sustenta.

**Ressalva honesta (o que NÃO deu para provar):** os `MonoBehaviour` deste build **não têm typetree**
(`read()` tipado falha), então **campos serializados** não podem ser lidos — se algum componente de cena
guardasse uma referência serializada ao Canvas e o desligasse, isso não apareceria na busca por código.
Também não afirmo nada sobre **transições de cena** (o canvas obviamente some com a cena). Dentro de uma
run, não há evidência de desligamento.

---

## 4. `AcceptButton` — hierarquia, filhos, componentes

Campo `RoguelikeManager.AcceptButton` (l.168601) + `AcceptButtonText` (l.168603).

```
Accept Btn [503691]                                   aMin(0.5,0.0) aMax(0.5,0.0) piv(0.5,0.0) ap(0.0,16.9) sd(121.9,28.3)
  <- Content [680573]                                 aMin(0.0,0.5) aMax(1.0,0.5) ap(0.0,-4.0)  sd(293.2,535.6)   {VerticalLayoutGroup, ContentSizeFitter, Image}
  <- Roguelike Level Up Menus (Keep Active) [680554]  aMin(0.5,0.5) aMax(0.5,0.5) ap(0.0,0.0)   sd(0.0,154.6)
  <- Level Up Sequence Window (Keep Inactive) [680553] = SkillSelectWindow
  <- Roguelike Manager [680571]
```

- Componentes de [503691]: `CanvasRenderer, RectTransform, **UIButtonController, Image, Button, ButtonHoverDectector, LayoutElement**`.
  **Sem `CanvasGroup`; sem `LayoutGroup` próprio.**
- **Filhos: exatamente UM** — `Text` [79195] (`aMin(0,0) aMax(1,1) sd(-10,-10)`, um `TextMeshProUGUI`).

**Armadilhas para clonar (proposta C):**
1. o **PAI** (`Content` [680573]) tem `VerticalLayoutGroup` + `ContentSizeFitter`: clonar o `AcceptButton`
   **para dentro de `Content`** reflui o painel inteiro e re-dimensiona o `ContentSizeFitter`. Clonar para
   dentro do `SkillSelectWindow` [680553] (que **não** tem layout group) evita isso;
2. o clone herda o `Button.onClick` serializado do original — tem de `RemoveAllListeners()` (mesma
   disciplina do `RunButton`/`SelectPartyButton`).

---

## 5. `CurrentCharacterUI` e o seu pai — rect e CanvasGroup

**Prefab root `Current Character UI` [556345]:** comps
`CanvasRenderer, RectTransform, **PrefabLocalizer, HorizontalLayoutGroup, Image, CurrentCharacterUI, MaximumAspectRatioFitter**`
→ **NÃO tem `CanvasGroup`.**

| | rect |
|---|---|
| `Current Character UI` [556345] (no prefab) | `aMin(0,0) aMax(1,1) piv(0.5,0.5) ap(0,0) sd(-0.6,0.0)` — tela cheia |
| `Current Character UI Placeholder` [581] (a fonte do rect em runtime) | `aMin(0,0) aMax(1,1) piv(0.5,0.5) ap(0,0) sd(0,0)` — tela cheia |
| pai em runtime = `GUI Manager` [3210] (Canvas) | tudo zero; **sem `CanvasGroup`, sem `LayoutGroup`** |

- O **único** `CanvasGroup` do ramo do HUD está no filho **`In Game GUI` [97870]**
  (`aMin(0.0,1.0) aMax(0.0,1.0) piv(0.5,0.5) ap(0.0,-250.0) sd(0.0,500.0)`; comps `RectTransform, CanvasGroup`).
- Um **clone irmão do `CurrentCharacterUI`** (filho do Canvas) **não** é afetado pelos layout groups do
  HUD. Mas um clone filho **do próprio** `CurrentCharacterUI` está sob o **`HorizontalLayoutGroup`** +
  `MaximumAspectRatioFitter` do root — que é justamente o caso do botão atual (ancorado na linha do
  `Ping Button`, dentro do HUD).

---

## VEREDITO por abordagem (só com os fatos acima)

### C — botão dentro do `SkillSelectWindow` → **VIÁVEL**, com uma correção de alvo
- O `SkillSelectWindow` [680553] **não tem LayoutGroup** ⇒ um filho livre ali fica com o rect que você der,
  sem reflow. Ele tem `CanvasGroup` ⇒ o botão acompanha o fade da janela. E **ele só existe/está ativo
  enquanto o level-up está aberto** (é o GameObject que `OpenSkillSelectWindow`/`Close` liga e desliga) —
  então este caminho é uma **casa do level-up**, não o botão permanente da run.
- **Correção de fato:** `(1,1)` do `SkillSelectWindow` = **canto da TELA** (ele é tela cheia); o painel
  visível é `Content` [680573], ≈293×536 px centralizado. Se o alvo é "canto do painel do level-up", o pai
  tem de ser `Content` [680573] — e aí o `VerticalLayoutGroup`/`ContentSizeFitter` dele **vai reflowar** o
  painel. Não há opção "canto do painel, sem reflow" entre os ancestrais: `Content` é o único que tem o
  rect do painel e o layout group.
- Clonar o `AcceptButton` [503691] como molde é seguro **desde que** o clone seja paiado **fora** de
  `Content` e com `onClick` limpo.

### D — atalho F10 → **VIÁVEL, e independente do prefab**
O prefab não impõe nenhum bloqueio a um handler de input. Nada aqui contradiz a RSTV-11a.

### A — botão como IRMÃO do HUD sob o Canvas compartilhado → **viável só com índice explícito; o "vizinho do HUD" NÃO funciona**
- A **premissa se sustenta** (§3): o Canvas/GUI Manager não é desligado por código durante a run, e ele
  **não tem LayoutGroup** ⇒ um irmão com rect manual fica no rect manual.
- **Mas a ordem de prefab mata a versão ingênua** (§2): o HUD está no índice **6** e o `RoguelikeManager` no
  **24**. Um botão posto junto do HUD (índice ~7) fica **ABAIXO** da janela do level-up — coberto pelo
  `SkillSelectWindow` (tela cheia) e pelo filho `Fade` [680576] (tela cheia, `Image`). Ele **não renderiza
  nem é clicável** durante o level-up, exatamente o caso que motivou a feature.
- Para o A funcionar ele teria de ser inserido **depois do índice 24** (acima do RoguelikeManager, abaixo
  de `Tooltips / Popups` [53] / `Pause Menu` [54] / `Confirm Window` [55]). Isso é um **índice explícito,
  não "irmão do HUD"** — e passa a flutuar acima de tudo o que o prefab põe entre 25 e 52.

### B — **NÃO CONFIRMÁVEL AQUI**
A definição da proposta B não veio em nenhum artefato que eu recebi (nem em `RSTV-10.md`, nem em
`RSTV-11a.md`, nem no kanban). Se B for "Canvas/overlay próprio com sortingOrder alto", o prefab **não**
oferece um canvas pronto: os canvases da cena são `GUI Manager` (o do jogo), os dois `Canvas` de
ferramenta e o `CursorCanvas` — criar uma camada própria em runtime é possível e **não depende** dos fatos
acima; diga-me o texto de B e eu fecho o veredito dele com o mesmo método.

### O que continua NÃO confirmado (limites desta leitura)
1. **Nenhum `MonoBehaviour` tem typetree** ⇒ **não li nenhum campo serializado** (quem é o
   `SkillSelectWindow` **pelas referências do prefab** é inferência por eliminação + `CanvasGroup` +
   o campo `SkillRerollSection`; pelos **nomes** dos GameObjects não existe um GO chamado
   "SkillSelectWindow" — o nome real é `Level Up Sequence Window (Keep Inactive)`).
2. Comportamento em runtime (posição em pixels, se o `Fade` [680576] bloqueia raycast) não foi observado
   em jogo — é leitura de asset.
3. Nada foi alterado no jogo nem no repositório além deste documento; nenhum commit.
