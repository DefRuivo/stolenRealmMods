# RSTV-30 — o botão `Skills` da run: barra de baixo e visibilidade sem piscar

> Tarefa `t_2cef3e03`. **Mod:** `RoguelikeSkillTreeVisualizer` (`com.gumatos.roguelikeskilltreevisualizer`).
> Este documento é a **decisão de UI/UX** e a **procedência de cada número** usado no reposicionamento
> (o DoD pede as duas coisas). Nada aqui foi medido no jogo: as medidas são **do prefab** (leitura de
> asset, `resources.assets`) e o mod **mede em runtime** os mesmos lados antes de posicionar.
> **Nada foi instalado nem publicado** por esta tarefa.

---

## 1. O que o dono pediu (06/10, em jogo)

> "o botão de skills nem sempre está visível, quando alguém toma alguma ação o botão some e depois
> reaparece, também ele não aparece enquanto estamos fora de combate. Faça com que ele, ao invés de
> ser renderizado ao lado do botão de marcar o hex, seja renderizado na barra de baixo na esquerda ao
> lado dos botões de inventário e skills e entre o botão de rotacionar a barra de skills"

E a evidência do log da sessão de 06/10 16:59: as únicas linhas do botão da run eram de **esconder**
(`GUIState ChoosingCharacter fora da whitelist da run`, `fora do modo Roguelike`) — nenhuma de
"VISÍVEL e clicável". Ou seja: as **guardas** escondiam o botão onde ele deveria estar.

---

## 2. Onde o botão mora agora (com a procedência dos nomes)

Caminho medido no prefab do HUD — `Current Character UI` **[556345]** →
`Skillbar Layout PC` **[526615]** → **`Skillbar Buttons` [526621]**, cujos filhos, na **ordem de
irmão**, são:

| # | filho de `Skillbar Buttons` | chamada do clique (lida do RAW do prefab) | `path_id` |
|---|---|---|---|
| 0 | `Pause Menu Btn` | `CurrentCharacterUI.ButtonPressedPauseMenu` | 526619 |
| 1 | **`Character Btn`** — o de **inventário** | `CurrentCharacterUI.ButtonPressedCharacter` | 526620 |
| 2 | **`Skills Tree Btn`** — o de **skills** (`CurrentCharacterUI.skillsBtn`) | `CurrentCharacterUI.ButtonPressedSkillTree` | 98294 |
| 3 | `Fortunes Btn` | `CurrentCharacterUI.ButtonPressedFortunes` | 526622 |

Irmãos de `Skillbar Buttons` dentro de `Skillbar Layout PC` (o **vizinho da direita** é o rotador da
barra de skills):

| filho de `Skillbar Layout PC` | o que é | `path_id` |
|---|---|---|
| `End Turn Button`, `Confirm Placement For All` | fim de turno / confirmar posicionamento | 690493, 469783 |
| `Ping/Flee` → `End Turn Button BG` → `Ping Button` | onde o botão morava **até a RSTV-29** | 367672, 91812, 41073 |
| **`Skillbar Buttons`** | a linha dos botões de inventário e de skills | 526621 |
| **`Skillbar Index Controls`** | `Up`/`Down` chamam `Skillbar.IncrementSkillbarIndex` — **o botão de rotacionar a barra de skills** | 526618 |
| `Skillbar` | as casas de ação | 556343 |

**Como os nomes foram fixados (nada por palpite):**

* as chamadas de clique acima saem do **RAW** dos `MonoBehaviour` do prefab — o nome do método fica
  gravado no dado do botão (mesma técnica da RSTV-5/RSTV-10). A string
  `"CurrentCharacterUI, Assembly-CSharp"` + `"ButtonPressedSkillTree"` aparece no `Skills Tree Btn`;
  `"Skillbar, Assembly-CSharp"` + `"IncrementSkillbarIndex"` aparece em `Up` e `Down`;
* a **classe** de cada componente (para saber quem tem `LayoutGroup`) sai do `m_ClassName` dos
  `MonoScript`, resolvido pelo `m_Script` do componente (o typetree dos `MonoBehaviour` deste build
  não abre — achado da RSTV-5/RSTV-10);
* ferramenta: **UnityPy 1.25.3** sobre
  `E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm_Data\resources.assets`. Bancada:
  `probe_hud.py`, `probe_classes.py`, `probe_raw2.py`, `probe_onclick.py` (workspace da tarefa;
  os scripts são descartáveis, a receita está descrita aqui).

---

## 3. Os números da colocação (e de onde cada um vem)

Tudo no **espaço local de `Skillbar Buttons`** — o espaço que `container.InverseTransformPoint`
devolve, cuja **origem é o PIVOR do container** (o centro: `pivot (0.5,0.5)`, `sd.x = 111.3`). Os
filhos nativos usam `aMin = aMax = (0,1)` (âncora no canto superior esquerdo do container), o que
**não** muda a origem do espaço local.

| número | valor (no espaço local) | de onde vem |
|---|---|---|
| largura/altura de um botão nativo | **27.02 × 35.0 px** | `RectTransform` de `Character Btn` / `Skills Tree Btn` no prefab |
| borda **esquerda** do container | **≈ −55.7 px** | `rect.xMin` com o pivor no centro (`−sd.x/2 = −55.65`) |
| borda **direita** dos nativos | **≈ +55.7 px** | os 4 botões nativos **preenchem** o container (`sd = 111.3`: 4 × 27.02 + espaçamento ≈1.07). No referencial da borda esquerda esse MESMO ponto era "111.3 px" |
| borda **esquerda** do rotador | **≈ +78.7 px** | `Skillbar Index Controls` [526618] (`ap x = 149.15`, `sd = 21.7`): contando a partir da borda esquerda do container ela fica a **134.3 px**; no espaço local, `134.3 + rect.xMin (−55.65) = 78.65` |
| vão livre | **≈ 23.0 px** | `78.65 − 55.65` — o mesmo `134.3 − 111.3` do referencial da borda esquerda (a diferença não depende da origem) |
| margem de respiro | **2.0 px por lado** | decisão do mod (constante `Margem`), não medida: é o que garante que a medida nunca encoste |
| largura final do clone | **≈ 19.0 px** | `min(largura do molde, vão − 2×margem)` |

**RSTV-30F — um só referencial (defeito achado na revisão `t_089af31b`, consertado no cartão
`t_8a606dc3`).** A conta de `ColocarNaLinha` **misturava** os dois referenciais das linhas acima: o
`fimDosNativos` vinha de `container.InverseTransformPoint` (espaço **local**, origem no pivor ⇒
+55.7) e o `limite` era a diferença de dois `pai.InverseTransformPoint` (medido a partir da **borda
esquerda** ⇒ 134.3). Alimentada assim, a mesma fórmula dava `vão = 134.3 − 55.7 − 2×2 = 74.6` (em vez
de 19.0), `largura = min(27.02, 74.6) = 27.02` e `centro ≈ 118.8`, ou seja o clone caía em ≈
105…132 — **depois** do `Skillbar Index Controls` (que ocupa ≈79…100), e não no vão livre. O limite
agora é medido com o **MESMO** `container.InverseTransformPoint`, então `fimDosNativos`, `limite`,
`vão` e `centro` falam a mesma língua (todo `InverseTransformPoint` do método tem de ter o
`container` como receptor — travado em `regras_rstv30.falhas_da_fonte` e na isca 6 da prova de fogo).

`Skillbar Layout PC` tem `HorizontalLayoutGroup` **DESLIGADO** no prefab (`m_Enabled = 0`, lido do
byte 12 do componente), então as posições do prefab **são** as de runtime; `Skillbar Buttons` tem
`HorizontalLayoutGroup` **LIGADO** — e é por isso que o clone entra com
**`LayoutElement.ignoreLayout = true`**: ele sai da conta do grupo, **nenhum botão nativo muda de
tamanho ou de posição**.

### O algoritmo (não há posição digitada no código)

`RunButton.ColocarNaLinha` mede, em runtime, **no espaço local do container** (os quatro itens abaixo
saem do MESMO referencial):

1. as bordas do **molde** (`GetWorldCorners` + `InverseTransformPoint`);
2. a **borda direita dos nativos** (máximo entre os filhos ativos, ignorando o nosso clone);
3. o **limite da direita** = a menor borda esquerda entre os **irmãos do container no pai** que
   ficam à direita dele (é o `Skillbar Index Controls`; o nome medido vai para o log — **nenhum nome
   fica fixo no código**), medida com `container.InverseTransformPoint` — o mesmo espaço do item 2;
4. `largura = min(largura do molde, limite − fim − 2×margem)` e `centro = limite − margem − largura/2`,
   **nunca** antes de `fim + margem + largura/2` (o clone não entra por cima de ninguém);

O teste puro `t_rstv30_barra_de_baixo.py` prova a conta em 4 cenários com vão + o caso degenerado
(vão ≤ 0: o clone fica logo depois dos nativos e o **AVISO** vai para o log) e exige que o corpo do
método **não tenha literal de posição** (só `0f`, `1f`, `0.5f`). A fixture em
`regras_rstv30.PREFAB` carrega os números crus (com o referencial de origem anotado) **e** os
convertidos; o teste confere a travessia entre os dois e alimenta o modelo puro só com os
convertidos — mais a **isca do referencial** (o par misturado tem de reprovar, e reprova).

**Log de diagnóstico (para a conferência do dono):** cada número medido sai numa linha só —
`RSTV-30: botao 'Skills' injetado na BARRA DE BAIXO (largura=… px (nativo … px), altura=… px; borda
direita dos nativos=… px, limite do vizinho '<nome>'=… px, vao livre=… px, margem=… px no espaco
local de '<container>')`.

---

## 4. Decisão de UI/UX (o que o DoD exige)

| aspecto | decisão | por quê |
|---|---|---|
| **colocação** | mesma linha dos botões de inventário e de skills, no **vão livre à direita** do último botão dessa linha e **à esquerda** do controle que rotaciona a barra de skills | é literalmente o pedido ("ao lado dos botões de inventário e skills e entre o botão de rotacionar a barra de skills"); é a única região com espaço **sem mover nada** |
| **tamanho** | altura = a da linha nativa (35 px); largura = o que couber no vão (≈19 px, contra 27 px de um botão nativo) | o vão medido é mais estreito que um botão; **não encolher nem empurrar botão nativo** tem prioridade sobre o tamanho (era o defeito da receita antiga) |
| **aparência** | clone do **botão nativo da própria linha** (`Skills Tree Btn`): fundo, sprite, estados e o **ícone nativo** da árvore de skills. Sem rótulo de texto | a esse tamanho um glifo lê melhor que "Skills"; o hover nativo (`ButtonTextOnHover`) continua identificando o botão |
| **contraste / não sobreposição** | nenhum pixel novo de cor: tudo vem do prefab do jogo; a colocação é provada **sem sobreposição** pelo teste (4 cenários + degenerado) | manter a identidade visual do jogo e a promessa do pedido |
| **badge de pontos** | desligado (o filho `Text BG`) | o mod **não** conta pontos: o badge é do botão nativo |
| **visibilidade** | a do HUD — o clone é filho da barra de baixo | "visível sempre que o HUD da run está visível", inclusive fora de combate e durante a ação de outro personagem |
| **clique** | continua com portão, mas ele **não esconde mais**: só tira o clique e diz o motivo no log | manter as proteções de dano real (mira, janela aberta, posicionamento) sem o piscar |

### Riscos assumidos (e o que os cobre)

1. **o vão pode mudar** numa atualização do jogo (outro tamanho de botão nativo, mais um botão na
   linha): o mod **mede** a cada injeção e escreve o resultado no log; se o vão não couber, o
   `AVISO` aparece na linha de injeção (o botão fica com o que cabe, **sem** sobrepor ninguém).
2. **o molde mudou de `Ping Button` para `Skills Tree Btn`**: a persistente do `onClick` agora é
   `ButtonPressedSkillTree` (abriria a árvore **escrevível** nativa). A troca da instância do evento
   (`NativeUiHelpers.ClearClickListeners`, RSTV-12) continua sendo feita **antes** de instalar o
   nosso listener — isso está travado por teste (`t_rstv12`), com o perfil do molde novo.
3. **visual final aos olhos** não é provável por teste: é a **conferência do dono** (§6).

---

## 5. Visibilidade: por que o botão não pisca mais

| quem decide | antes (até a RSTV-29) | agora (RSTV-30) |
|---|---|---|
| **aparecer/sumir** | `RunButton.Mirror` chamava `Hide` quando `RunTargets.GateOk` recusava — e o portão olhava estado de **batalha** | o **HUD**: o clone é filho da barra de baixo, então sai/volta com o HUD inteiro (`GUIManager.Update` l.120485). Só espelha o **próprio botão nativo** (se o jogo esconder só ele) |
| **clicar** | o mesmo portão (escondia junto) | a **regra nativa do jogo** (`skillsBtn.interactable`, `GUIManager.Update` l.120491) **E** o portão da run — o portão recusa apenas onde abrir causaria dano real |

Guardas **removidas** (cada uma com o defeito que causava) e guardas **que ficaram** (com a
justificativa no código, marcadas `GUARDA n`): ver o cabeçalho de `RunTargets.cs` e a família de
testes `tools/testes/regras_rstv30.py`. O teste `t_rstv30_sem_piscar.py` **conta as piscadas**: numa
rodada (mapa → setup → meu turno → eu agindo → inimigo agindo → inimigo andando → meu turno) a
visibilidade **antiga** alterna **4 vezes**; a nova, **0** — e no cenário exato do dono ("outro
personagem age") a antiga esconde e a nova mantém.

---

## 6. Conferência do dono (roteiro, em jogo)

1. **Onde ele está:** abra uma run e olhe a **barra de baixo, à esquerda**: o botão deve estar
   **na mesma linha do inventário e do botão de skills**, à direita deles e **antes das setas que
   rotacionam a barra de skills**. É um quadradinho com o **ícone de árvore de skills**.
2. **Não empurrou nada:** os botões nativos (inventário, skills, fortunas, pause) e as setas de
   rotação continuam **no mesmo lugar e do mesmo tamanho**. Nada se sobrepõe.
3. **Piscar (o defeito principal):** deixe um inimigo agir / mover e **não** tire o olho do botão —
   ele **não pode desaparecer** (nos logs, a linha do botão deve continuar existindo, no máximo
   trocando por `... VISIVEL na barra de baixo e SEM clique agora — <motivo>`).
4. **Fora de combate:** ande no **mapa** e volte para a **cidade** — o botão continua lá.
5. **Clique:** com o botão clicável, o clique abre a árvore read-only do personagem em foco; a
   árvore fecha com **X** e **Esc** e nada é gasto (segue sendo somente leitura).
6. **Sem clique nos momentos de risco:** com uma **mira de skill** armada, ou com uma **janela de UI
   aberta**, ou no **posicionamento inicial** da batalha, o botão **continua na tela** mas **não
   clica** — e o `LogOutput.log` diz o motivo.
7. **Desligar, se incomodar:** `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg` →
   `AtivarBotaoNaRun=false` (ou a chave-mestra `AtivarBotao=false`).

Se algo do que está acima não bater, **o número que interessa é a linha de injeção no
`LogOutput.log`**: ela traz a largura final, a borda direita dos nativos, o limite medido do vizinho
e o vão livre. Com ela em mãos o ajuste é de constante, não de chute.

---

## 7. O que ficou fora desta tarefa

* **Instalar e publicar** — fora do escopo (o pacote no ar continua o 0.3.2 de 04/10).
* **Re-baseline da automação AUT-5** — a lista de guardas da run mudou (saíram três): o registro em
  `tools/automacao/aut5/log_rstv.py` + `cenarios-rstv.json` foi atualizado nesta tarefa; o
  **fixture de log** e os cenários da frente AUT-5 precisam de rodada autorizada (outro cartão).
