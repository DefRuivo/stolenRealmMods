# Changelog — BetterCombatText

## 0.1.0

Primeira versao.

- **Contorno/halo suave no texto de combate**: contorno `_OutlineWidth` + `_OutlineSoftness` (alto = halo borrado, o "sombreamento radial" pedido) com **cor preta a 10% de alfa** por padrao, mais sombra difusa `_Underlay` (offset, dilate, softness) opcional.
- **Alvos, cada um com liga/desliga proprio no `.cfg`**:
  - **Nomes de inimigos em combate** — `BossHealthbar.BossName` (barra de chefe) e `PlayerInfoWindow.playerName` (janela de hover sobre o inimigo). Ambos `TextMeshProUGUI` → halo suave.
  - **Rotulos/stacks de buff e debuff em combate** — `StatusIcon.stackCount` ("x3") e `StatusIcon.turnCount`. Sao `UnityEngine.UI.Text` **legado**, sem distance field: recebem contorno duro (`Outline`), sombra e **negrito**. Halo suave e **impossivel** ali (registrado no README e no log de arranque).
  - **Texto do dado nos eventos** — `DiceVisualSetup.DiceNumbers` (numero na face do dado), `DiceRoller.TargetText/ResultText/ModifierValueText`. `TextMeshPro`/`TextMeshProUGUI` → halo suave. Grupo proprio, independente do combate.
  - **Tooltip de status (nome do buff)** — **desligado por padrao**: o nome do buff so aparece no tooltip generico do jogo, cujo componente (`Tooltip.Title`/`Description`) e o mesmo dos tooltips de skill/item/powerup; ligar espalha o halo por todos os tooltips.
  - **Numero de vida sobre as unidades** — extra, **desligado por padrao**, fora do pedido original.
- **Seguranca do material**: o efeito e aplicado numa **copia do material por componente** (`TMP_Text.fontMaterial`, que internamente faz `new Material(shared)` — confirmado no IL do `TextMeshProUGUI.GetMaterial`). `fontSharedMaterial` nunca e escrito, entao a interface inteira **nao** ganha contorno.
- **Falha-segura**: tudo em `try/catch`; se o shader nao for distance field (`_OutlineWidth` ausente), o mod **nao altera** aquele material e loga o motivo. Patches Harmony sao **por tipo** de metodo com `__instance` — nenhum parametro posicional `ref __N`.
- **Diagnostico no log**: por superficie, o mod registra objeto, componente, fonte TMP, material compartilhado de origem, shader e se e SDF; mais um inventario da cena (`N TMP_Text`, `M TextMesh` legado) e os materiais de fonte em uso com contagem.
- **Verificado rodando o jogo**: patches aplicados sem nenhum `PatchError`; todos os alvos TMP confirmados em `TextMeshPro/Mobile/Distance Field` com `_OutlineWidth` presente (halo suave viavel); o numero do dado confirmado como `TextMeshPro` (140 faces, 0 `TextMesh` legado); e os rotulos de stack confirmados como `UnityEngine.UI.Text` legado (124 `StatusIcon`).
- **Com o mod DESLIGADO (`Ativar = false`) o jogo roda original**: testado — o log mostra so a linha de "DESLIGADO no config" e nenhum patch e aplicado.
- **Desligar tudo em 1 linha**: `Ativar = false` na secao `1. Geral` — nenhum patch e aplicado e o jogo roda original.
- **Sem alteracao de gameplay** e sem tocar em arquivo do jogo. Nada de Bard/musica.
