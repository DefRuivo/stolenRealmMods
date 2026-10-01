# Changelog — BetterCombatText

## 0.1.1

**Nenhuma linha de codigo mudou: o que muda e a REFERENCIA e a doc.** O defeito que motivou a
versao e de interacao, e sem ela o pacote publicado entrega metade do recurso.

- **Dependencia do Thunderstore: `DefRuivo_StolenRealmMods-BetterFont-1.0.1` -> `1.0.2`.** A 1.0.1
  esta publicada e e imutavel, e o portao de material dela **recusava o material dos textos de
  combate** (variante de shader diferente: os alvos usam `TextMeshPro/Distance Field Overlay` e
  `Distance Field (Surface)`; a fonte serifada sai com `Mobile/Distance Field`) — com os dois mods
  ligados, os textos de combate ficavam na **fonte original**. O conserto e o **BetterFont 1.0.2**
  (variante diferente virou copia best-effort, propriedade por propriedade com `HasProperty`). Sem
  bumpar esta referencia, o gerenciador instalaria a 1.0.1 ao lado deste mod e o defeito continuaria
  em campo. A regra `DEP_EXTRAS` do `tools/audita_docs.py` exige exatamente isto: quem declara outro
  mod deste repo aponta a versao que ele tem HOJE no manifest.
- **Ordem de envio (nao inverter):** primeiro o **BetterFont 1.0.2**; depois este **0.1.1**. O upload
  da Thunderstore **resolve** cada referencia (`PackageReferenceValidator(resolve=True)`) e recusa a
  que nao existe com `No matching package found for reference` — a versao declarada aqui precisa
  estar no ar antes.
- **Doc corrigida:** o README (secao "Together with BetterFont" e o resumo em portugues) afirmava que
  os textos de combate "podem manter a fonte original" com os dois mods ligados. Isso descrevia o
  comportamento da 1.0.1 do BetterFont, nao o desta versao: com o **BetterFont 1.0.2** o texto de
  combate fica com **a serifa e o halo/sombra**.

## 0.1.0

Primeira versao publicada.

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
- **Convivência com o BetterFont**: com os dois ligados, os textos de combate ganham a **serifa e o efeito** (halo/sombra) a partir do **BetterFont 1.0.2** — variante de shader diferente não é mais recusa lá. Na **1.0.1** eles ficavam com a **fonte original** (o portão do BetterFont recusava o material dos textos de combate; era o defeito que o BF-2 consertou). O BetterFont troca a fonte e reaplica no material por componente o efeito que já estava naquele texto; quando esse efeito não pode ser reproduzido (textura de face, bevel, glow), aquele texto fica **intocado** — a escolha segura, não um defeito, e o motivo sai nomeado no log do BetterFont. Cosmetico, nada quebra.
- **Desligar tudo em 1 linha**: `Ativar = false` na secao `1. Geral` — nenhum patch e aplicado e o jogo roda original.
- **Sem alteracao de gameplay** e sem tocar em arquivo do jogo. Nada de Bard/musica.

### Dependência declarada neste manifest

- `dependencies`: `BepInEx-BepInExPack-5.4.2305` + **`DefRuivo_StolenRealmMods-BetterFont-1.0.1`** — é aqui que o estilo dos textos de combate volta; a referência aponta a versão **nova** para o gerenciador não instalar o mesmo pacote em duas versões (mesmo GUID = erro no BepInEx).
- **A dependência é UMA DIREÇÃO — `BetterCombatText 0.1.0` → `BetterFont 1.0.1` — e só ela.** O `BetterFont` 1.0.1 declara **apenas** o BepInExPack; quem aponta para a outra ponta é este mod. A mão dupla (os dois se declarando) foi trocada por esta direção única no commit `ac0210f`.
- **Por que a mão dupla não sobe (provado no código da Thunderstore):** no upload a plataforma **resolve** cada referência (`DependencyField` usa `PackageReferenceValidator(resolve=True)`) e **recusa** a referência que não existe, com `No matching package found for reference`. Com os dois lados se referenciando, cada lado apontava para uma versão **inédita** (o `BetterFont 1.0.1` e este `0.1.0`, nenhuma das duas no ar) — não havia ordem de envio válida: quem subisse primeiro falhava. Não é preferência de estilo, é o upload recusando.
- **Ordem de envio que funciona:** primeiro o `BetterFont 1.0.1` (sem dependência de volta), depois este `0.1.0` declarando o `BetterFont 1.0.1` — a mesma ordem registrada em [`release/mods.json`](../release/mods.json).
- **Opção do dono (não é plano, não existe hoje):** se quiser o **ciclo** de verdade, com os dois se referenciando, o caminho é um **`BetterFont 1.0.2` depois**, declarando este `BetterCombatText 0.1.0` já publicado.

