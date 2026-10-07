# RSTV 0.3.3 — roteiro curto de conferência em jogo

> **Para o dono, na tela, sem abrir código.** Mod: `RoguelikeSkillTreeVisualizer`
> (`com.gumatos.roguelikeskilltreevisualizer`). Alvo: **0.3.3**. Publicação **não** faz parte deste
> roteiro (segue no PUB-1). Este é o roteiro curto: barra de baixo, visibilidade, fechar/somente
> leitura e a contagem do boot. O roteiro longo (casos de risco a–g) é o
> `RSTV-6-PACOTE-DE-ACEITE.md`, anexo do cartão `t_ea40e86e`.

---

## 0. Uma pré-condição só: a build certa no perfil

**Isto não pressupõe que a build já esteja instalada.** Se a DLL no perfil do r2modman for anterior a
esta entrega, instale a build atual — é um passo local e explícito (não é publicar):

```
cd C:/dev/stolen-realm
dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj -p:DeployToBepInEx=true
```

Abra pelo **r2modman → Start modded** e leia no
`<perfil>/BepInEx/LogOutput.log` a linha:

```
RSTV: patches Harmony aplicados (N/N ganchos, M metodos do jogo).
```

| o que aparece | o que significa | o que fazer |
|---|---|---|
| **`15/15 ganchos, … metodos do jogo`** | build **atual** (fonte de hoje: 15 ganchos) | ✅ prossiga |
| **`17/17`** | DLL **antiga** ainda no perfil (o perfil tinha a build de 06/10 15:08, com os 2 ganchos da Select Party) | ❌ feche o jogo, repita o passo acima e reinicie |
| nada | o plugin não carregou | ❌ pare e reporte |

Anote o N visto: `____/____`.

**Ligar/desligar (se precisar):** `<perfil>/BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`,
seção `[Geral]` → `AtivarBotaoNaRun=false` desliga só o botão da run; `AtivarBotao=false` é a
chave-mestra (desliga os três botões: run, janela de level-up e modal). Reinicie depois de editar.

---

## 1. Barra de baixo — onde o botão está

| ✔ | o que olhar | esperado |
|---|---|---|
| ☐ | canto **inferior esquerdo** do HUD, na linha do **inventário** e do botão de **skills** | um quadradinho **a mais**, com o **ícone nativo de árvore de skills**, logo à direita do botão de skills e **antes das setas** que giram a barra de skills |
| ☐ | os botões que já existiam (inventário, skills, fortunas, pause, setas) | **no mesmo lugar e do mesmo tamanho**; nada se sobrepõe; o HUD não se re-arruma |
| ☐ | hover no botão novo | reage como um botão do jogo; sem texto novo/estranho |

## 2. Visibilidade — o defeito que motivou a mudança

| ✔ | o que fazer | esperado |
|---|---|---|
| ☐ | ande no **mapa** e entre/saia da **cidade** | o botão **continua lá** — ele não aparece só em combate |
| ☐ | deixe **outro personagem/inimigo agir** e não tire o olho do botão | **não pisca** e **não desaparece** (é o defeito antigo) |
| ☐ | durante a ação do outro, veja o log | no máximo a linha `... VISIVEL na barra de baixo e SEM clique agora — <motivo>`; o botão **continua na tela** |
| ☐ | abrir/fechar o inventário só para comparar | nada muda no botão novo |

**Quando ele não aparece é esperado:** só quando o jogo esconde a **própria linha de baixo do HUD**
(menus, evento, level-up, loja, criação/escolha de personagem). Ele espelha o botão nativo de skills:
se os botões nativos não estão na tela, ele também não está.

## 3. Fechar e somente leitura

Ao clicar, o log diz `RSTV-16: abrindo a visualizacao read-only -> '<nome>' (nivel N)...`.

| ✔ | o que fazer | esperado |
|---|---|---|
| ☐ | **antes:** anote os pontos **não gastos** e **quais** skills o personagem em foco tem | anotado: pontos ____ / skills ______________ |
| ☐ | abra a árvore pelo botão, navegue pelas abas/classes, **tente clicar num nó** | o clique no nó **não faz nada**; nenhum ponto vai para a lista |
| ☐ | procure o botão de **reset/respect** | **não aparece** (o mod esconde) |
| ☐ | feche com o **X** | fecha; log: `RSTV-16: modo somente leitura encerrado (nada foi gravado no personagem).` |
| ☐ | abra de novo e feche com **Esc** | fecha igual; nada fica preso na tela |
| ☐ | **depois:** compare com o que anotou | **mesmos** pontos, **mesmas** skills — nada gasto, nada aprendido, nada resetado |

## 4. Quando o botão fica sem clique (o botão NÃO desaparece)

Com uma **mira de skill/hex** armada, com **outra janela de UI aberta** ou no **posicionamento
inicial** da batalha: o botão **continua visível** e **não clica**; o log diz o motivo. Botão
**sumindo** nesses casos = FALHA (é o defeito que a 0.3.3 conserta).

## 5. FALHA = exceção, NullReference ou o botão sumindo

Se qualquer linha acima não bater, mande: o passo (número e estado), o esperado e o que você viu
(captura de tela ajuda) + o `N/N` do boot e as linhas do RSTV no `LogOutput.log`. Exceção/NullReference
do RSTV no log = FALHA. Comportamento de tela que este roteiro não decide (abrir duas vezes, turno
avançando com a árvore aberta) está detalhado nos casos (d)–(f) do pacote longo.
