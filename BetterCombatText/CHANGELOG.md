# Changelog — BetterCombatText

## 0.1.0

Primeira versao — **ainda NAO publicada** (por isso a versao nao sobe: esta e a primeira build candidata).

- **Aplicador de ganchos corrigido antes da primeira publicacao**: o filtro de classe de gancho copiado do RoguelikeSkillTreeVisualizer exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no metodo** e este mod declara os **9 ganchos pela convencao de nome** do Harmony (metodo `Postfix`) — teria pulado os 9 em silencio. O filtro agora exige so `[HarmonyPatch]` **no TIPO** (o mesmo conjunto que o `PatchAll()` processava) e os ganchos sao aplicados **um a um**, com log por gancho e resumo com a contagem real.
- **Diagnostico de arranque mais barato**: a varredura de cena passou de 2s para 5s e **para no primeiro alvo que aparece em cena** (chave propria no `.cfg`), em vez de varrer todas as superficies sempre.

- **Contorno/halo suave no texto de combate**: contorno `_OutlineWidth` + `_OutlineSoftness` (alto = halo borrado, o "sombreamento radial" pedido) com **cor preta a 10% de alfa** por padrao, mais sombra difusa `_Underlay` (offset, dilate, softness) opcional.
- **Alvos, cada um com liga/desliga proprio no `.cfg`**:
  - **Nomes de inimigos em combate** — `BossHealthbar.BossName` (barra de chefe) e `PlayerInfoWindow.playerName` (janela de hover sobre o inimigo). Ambos `TextMeshProUGUI` → halo suave.
  - **Rotulos/stacks de buff e debuff em combate** — `StatusIcon.stackCount` ("x3") e `StatusIcon.turnCount`. Sao `UnityEngine.UI.Text` **legado**, sem distance field: recebem contorno duro (`Outline`), sombra e **negrito**. Halo suave e **impossivel** ali (registrado no README e no log de arranque).
  - **Texto do dado nos eventos** — `DiceVisualSetup.DiceNumbers` (numero na face do dado), `DiceRoller.TargetText/ResultText/ModifierValueText`. `TextMeshPro`/`TextMeshProUGUI` → halo suave. Grupo proprio, independente do combate.
  - **Tooltip de status (nome do buff)** — **desligado por padrao**: o nome do buff so aparece no tooltip generico do jogo, cujo componente (`Tooltip.Title`/`Description`) e o mesmo dos tooltips de skill/item/powerup; ligar espalha o halo por todos os tooltips.
  - **Numero de vida sobre as unidades** — extra, **desligado por padrao**, fora do pedido original.
- **Seguranca do material**: o efeito e aplicado numa **copia do material por componente** (`TMP_Text.fontMaterial`, que internamente faz `new Material(shared)` — confirmado no IL do `TextMeshProUGUI.GetMaterial`). `fontSharedMaterial` nunca e escrito, entao a interface inteira **nao** ganha contorno.
- **Falha-segura**: tudo em `try/catch`; se o shader nao for distance field (`_OutlineWidth` ausente), o mod **nao altera** aquele material e loga o motivo. Patches Harmony sao **por tipo** de metodo com `__instance` — nenhum parametro posicional `ref __N` — e sao aplicados **um a um** (`CreateClassProcessor(...).Patch()` por classe de gancho, com uma linha de log por gancho e um resumo com a **contagem real**): um gancho que falhe nao derruba os outros, e o log diz qual foi.
- **Diagnostico no log**: por superficie, o mod registra objeto, componente, fonte TMP, material compartilhado de origem, shader e se e SDF; mais um inventario da cena (`N TMP_Text`, `M TextMesh` legado) e os materiais de fonte em uso com contagem. Tem chave propria no `.cfg` (`1. Geral` > `DiagnosticoNoArranque`, padrao `true`; `false` = nenhuma varredura de cena) e a varredura **para sozinha no primeiro alvo que aparece em cena**.
- **Diagnostico de arranque executado no jogo**: o que esta confirmado e **viabilidade tecnica**, lida do proprio diagnostico — todos os alvos TMP usam variantes `TextMeshPro/Distance Field` (`Overlay`, `(Surface)`, `Distance Field`) com `_OutlineWidth` presente (halo suave viavel); o numero do dado e `TextMeshPro` (140 faces em 7 `DiceVisualSetup`, 0 `TextMesh` legado); e os rotulos de stack sao `UnityEngine.UI.Text` legado (124 `StatusIcon`).
- **Efeito visual: NAO CONFIRMADO** — depende do dono ver em jogo (abrir um combate/evento e olhar). O diagnostico prova que o halo e possivel, nao que ele aparece nem que ficou bom; nao ha log de antes/depois nem captura no repositorio.
- **Com o mod DESLIGADO (`Ativar = false`) o jogo roda original**: e um early-return no `Awake` — nenhum gancho e aplicado (no log aparece so a linha de "DESLIGADO no config") e nenhum alvo e tocado.
- **Convivência com o BetterFont**: com os dois ligados, os textos de combate tendem a manter a **fonte original** enquanto o resto da UI fica serifada — o BetterFont pula texto com material estilizado (`PularTextosEstilizados = true`) e este mod clona o material por componente. Cosmetico, nada quebra; detalhe no README.
- **Desligar tudo em 1 linha**: `Ativar = false` na secao `1. Geral` — nenhum patch e aplicado e o jogo roda original.
- **Sem alteracao de gameplay** e sem tocar em arquivo do jogo. Nada de Bard/musica.

### Dependência declarada neste manifest

- `dependencies`: `BepInEx-BepInExPack-5.4.2305` + **`DefRuivo_StolenRealmMods-BetterFont-1.0.1`** — é aqui que o estilo dos textos de combate volta; a dependência amarra a versão **nova** dos dois lados para o gerenciador não instalar o mesmo pacote em duas versões (mesmo GUID = erro no BepInEx).
- **Ordem de envio importa:** a referência é validada no upload (o validador resolve o pacote: `No matching package found for reference`) e os dois pacotes se referenciam entre si — a primeira publicação do par precisa de um dos lados apontando para uma versão já publicada.

