# Changelog — BetterCombatText

## 0.1.2

**Documentation release. No code change** — this build behaves exactly like 0.1.1; the DLL differs only in the version string it reports.

- **The build instructions were wrong about the deploy.** They said that a bare `dotnet build` would also copy the mod into the mod-manager profile. That is no longer true: the deploy is **opt-in** — a bare `dotnet build` installs **nothing**, and only `-p:DeployToBepInEx=true` copies the DLL into `<profile>\BepInEx\plugins\BetterCombatText\`.
- **The README described the wrong outline for the enemy names.** It said "soft outline/halo, default black at 10% alpha". That was true of the first release, not of 0.1.1: since then the enemy name gets a **hard, opaque black outline** (`LarguraContorno` 0.22, `SuavidadeContorno` 0.05, `AlfaContorno` 0.95), the **10% is the buff/debuff label**, and the enemy name's shadow is short and visible (`AlfaSombra` 0.75, offset ±0.35, softness 0.05), with its side following the background and the letter's brightness deciding when `Fundo = auto`. The table of surfaces and the configuration section now state the real defaults.
- **Still not verified on screen.** The visual result of this mod has never been confirmed in game — a startup diagnostic proved the effect is *possible* on those texts, but nobody has confirmed it on the screen. This release does **not** change that, and the README and the package description keep saying it.

## 0.1.1 — contorno preto duro/opaco (UI/UX) + sombra adaptativa por contraste

O nome do inimigo (cor de qualidade) ganhou **contorno preto DURO e OPACO** (`_OutlineWidth` 0.22, `_OutlineSoftness` 0.05 — era 0.50, o defeito que borrava o contorno até sumir, `_OutlineColor` alfa 0.95) e a **sombra** virou um seguro curto (`_Underlay` offset ±0.35 — era ±2, fora do range ±1 do shader — alfa 0.75, softness 0.05). A sombra adaptativa escolhe o lado pelo **contraste com a FONTE** (fonte clara → sombra escura, e vice-versa). Revisão de UI/UX: a cor de preenchimento **não muda** — é a linguagem de raridade (`QualityColors[EnemyType]`).

## BCT-5 (02/10) — a sombra CONTRASTA com a FONTE: a letra manda o LADO (fonte clara → sombra escura)

**Defeito relatado pelo dono:** a sombra do nome do inimigo continuava "da mesma cor da fonte".
Investigação fechada em três achados:

1. **O `.cfg` do perfil tinha um valor ERRADO (a causa do "mesma cor").** A linha
   `CorSombraClara = CBB396` do `BepInEx/config/com.gumatos.bettercombattext.cfg` foi herdada de um
   build antigo: o `#CBB396` é a **própria cor de texto do jogo** (`highlightedColor`/
   `specialDescColor`) e a cor comum do nome do inimigo. O BepInEx **não reescreve uma chave que já
   existe** quando o default do código muda — então o default novo do BCT-4 (`FFFFFF`) nunca chegou
   à instalação, e o "balde claro" continuava ligado na cor da própria fonte. (A DLL do perfil
   **era** a mais recente — sha256 idêntico ao `bin/Release`; o problema não era build.)
2. **O limiar do BCT-4 tinha um furo.** `UsaSombraClara` só virava o balde quando a cor escolhida
   ficava a menos de `ContrasteMinimo` (0.2) da letra. O bege `#CBB396` contra o branco `#FFFFFF`
   difere **0.283** — passava, e a letra CLARA do nome recebia a sombra CLARA (clara sobre clara).
   Com o `CBB396` herdado o mesmo furo atingia a letra **branca** (`CharacterNameColor =
   Color.white`), que ganhava o bege.
3. **O alfa estava baixo.** `alfaSombra = 0.35` nos Nomes: a sombra escura a 35% sobre o campo
   ficava translúcida e se confundia com o próprio glifo.

**A REGRA (BCT-5) — a letra manda o LADO:**

- A sombra tem de ficar do **lado oposto** da luminância da fonte: **letra CLARA → sombra ESCURA
  `#000000`; letra ESCURA → sombra CLARA `#FFFFFF`**. Sem limiar: o LADO decide (o limiar do BCT-4
  fica só como rede contra um balde mal configurado).
- O `Fundo` continua **propondo** a polaridade (BCT-3), mas leva o **VETO DA LETRA** quando põe a
  sombra do mesmo lado da fonte. Era isso que o dono cobria: com fundo escuro e letra clara, a
  sombra saía clara — "da mesma cor da fonte". Agora a letra `#CBB396` (nome do inimigo) ganha a
  sombra **ESCURA**.
- **Cores da paleta:** a sombra clara é o branco `#FFFFFF` (`physicalColor` da fixture do jogo) e a
  escura é o preto neutro `#000000` (o mesmo tom do contorno padrão). Nada de hex inventado.
- **Visibilidade:** `alfaSombra` dos Nomes sobe de **0.35 → 0.65**.
- **Conserto no perfil:** `CorSombraClara  CBB396 → FFFFFF` e `AlfaSombra 0.35 → 0.65` (seção
  `2. Nomes de inimigos (combate)`) do `.cfg` do r2modman (backup em `.bak-bct5`). Com o veto, o
  valor herdado deixou de ser uma armadilha, mas o arquivo é a mensagem que o dono lê.
- **Invariante testado:** para TODA cor da paleta × TODO `Fundo`, a sombra sai do lado oposto da
  letra e contrasta com ela. Novos vérticos: `t_bct_sombra_polaridade_fonte.py` (seção 14 de
  `regras_bct.py`) + o alfa mínimo. Provado reprovando:
  `tools/testes/bct5-polaridade-fonte-prova-reprovando.log` (o "veto arrancado" e o "alfa 0.35"
  REPROVAM pelo motivo certo; o fonte é restaurado byte a byte).

## BCT-4 (02/10) — a sombra CONTRASTA com a LETRA: o `#CBB396` deixa de ser a sombra clara (working tree; nada publicado)

**Defeito relatado pelo dono:** a sombra do nome do inimigo ficou invisível/"blob". O log de 02/10
(l.3359) fecha a conta: `cor da LETRA no alvo='#CBB396' (luminância 0.717 → letra CLARA); sombra que
FICOU no material=_UnderlayColor '#CBB396 alfa=0.35'`. A sombra CLARA era o `#CBB396` — a **MESMA
cor da letra** do inimigo (que é o `highlightedColor` do jogo). Sombra igual à letra = contraste
zero.

- **A regra do BCT-3 presumia LETRA ESCURA.** Ele escolhia a cor só pelo FUNDO ("fundo escuro →
  sombra clara `#CBB396`") sem olhar a LETRA — mas a letra do nome do inimigo é CLARA e é
  `#CBB396`: a sombra saía idêntica à letra.
- **A LEI nova (BCT-4):** a sombra tem de **contrastar com a LETRA** (o glifo está encostado nela)
  **e com o FUNDO** (a sombra cai sobre ele). A POLARIDADE continua saindo do FUNDO (BCT-3) e o
  `auto` continua saindo da LETRA (BCT-2); o que muda é que, se a cor do balde escolhido **não
  contrastar com a LETRA** (diferença de luminância < `ContrasteMinimo` = 0.2), **o balde VIRA**.
- **A sombra CLARA passa a ser o BRANCO PURO (`#FFFFFF`).** O `#CBB396` era a própria cor de texto
  do jogo (e a cor comum do nome do inimigo). Com a letra `#CBB396` em fundo escuro: sombra
  `#FFFFFF` — contraste com o bege da letra (0.28 ≥ 0.2) **e** visível no campo escuro. Chave
  `CorSombraClara` (default `FFFFFF`; quem preferir o `#CBB396` de volta edita o `.cfg`).
- **Invariante testado:** para TODA cor da paleta do jogo × TODO valor de `Fundo`, a sombra
  escolhida contrasta com a letra (≥ 0.2). A regra antiga violava exatamente no caso relatado.
- **Diagnóstico:** a linha do alvo passa a imprimir o limiar do contraste junto da cor da letra e do
  `_UnderlayColor` que ficou no material.
- **Testes:** `tools/testes/testes/puros/t_bct_sombra_contraste_letra.py` (novo) + a seção 14 de
  `regras_bct.py`; `t_bct_sombra_visivel_fundo_escuro.py` e `t_bct_sombra_adaptativa.py`
  atualizados (a sombra clara agora é o `#FFFFFF`). Provado reprovando:
  `tools/testes/bct4-contraste-prova-reprovando.log`.

### R2 — NÃO é o BCT: a "sombra grossa" do "Select Attributes" é do BetterFont

O dono também relatou que o rótulo de seção da **janela de level-up** ("Select Attributes",
`RoguelikeManager.SectionLabelText`, l.168605) ficou com "sombra muito grossa". Investigação
fechada (prefab + log + código):

- **O BCT não toca nessa tela.** Ele patcheia 7 métodos de 7 tipos (nome de inimigo, rótulos de
  status, texto do dado, tooltip, número de vida) — nenhum é o `RoguelikeManager` — e escreve
  SEMPRE no material POR COMPONENTE (`fontMaterial`). Não há caminho para alcançar o
  `SectionLabelText`. Trava disso: `tools/testes/testes/puros/t_bct_sem_vazamento_no_levelup.py`.
- **A causa raiz é o BetterFont.** Lido o PREFAB com UnityPy (`Roguelike Manager` [680571] →
  `Label` [680588] → o TMP que o campo `SectionLabelText` aponta): o material em uso é o
  `Regular Font (Minion Pro Regular) SDF Material`, com `_UnderlayColor` preto **alfa 0.5**,
  `_UnderlaySoftness`/`_UnderlayDilate`/`_UnderlayOffsetX`/`_UnderlayOffsetY` = **0** e o keyword
  **`UNDERLAY_ON` DESLIGADO** (`m_ValidKeywords == []`) — uma sombra **INERTE**, que o jogo NÃO
  desenha. O `CopiarEstilo` do BetterFont decide "sombra em uso" por `_UnderlayColor.a > 0.001`
  (o alfa é 0.5) **sem olhar o keyword**, liga o `UNDERLAY_ON` no material novo e copia os valores:
  a sombra que o jogo nunca desenhava passa a aparecer — o "sombra muito grossa" relatado. O
  `AcceptButtonText` do mesmo prefab mostra o mesmo padrão com o `Title Font (Trajan Pro Regular)
  SDF Material` (alfa 0.906).
- **Conserto (fora do BCT):** o BetterFont deve só habilitar `UNDERLAY_ON` quando o material de
  origem já tinha o keyword (ou quando o offset/dilate não for zero), em vez de inferir "sombra em
  uso" do alfa da cor.

## BCT-3 (02/10) — a sombra fica VISIVEL: o FUNDO manda (working tree; nada publicado)

**Defeito relatado pelo dono:** "não ve NENHUMA sombra nos nomes de inimigo" (campo de
batalha escuro). Investigação fechada e conserto:

- **A sombra ERA escrita — o defeito era a COR.** O log de 02/10 traz
  `[Nomes (combate)] APLICADO ... sombra=on` (l.3270) e **não** traz o aviso `sem-underlay`
  (que o mod imprime quando o shader não expõe `_UnderlaySoftness`): logo o ramo `temUnderlay`
  rodou e o `_UnderlayColor` foi escrito. O `sombra=on` é só a chave do config — não provava
  nada sobre a cor.
- **A letra é CLARA, o fundo é ESCURO.** `PlayerInfoWindow.playerName.color` =
  `CharacterNameColor` (= `#` + `GetEnemyQualityColor(EnemyType)`) ou `Color.white`
  (l.156815/156849/156850); o `BossHealthbar.BossName` usa a cor do prefab (l.26641). Pela
  regra do BCT-2 (sombra pela luminância **da letra**), letra clara → sombra **`#000000`**:
  preto sobre o campo escuro = **contraste zero**, a sombra existe e não aparece.
- **A REGRA MUDA (registrado):** um drop shadow só aparece quando contrasta com o que está
  **atrás** dele — o FUNDO, não a letra. Nova chave `Fundo` por superfície
  (`escuro` / `claro` / `auto`):
  - `escuro` → sombra **CLARA `#CBB396`** (a que aparece no campo de batalha);
  - `claro` → sombra **ESCURA `#000000`**;
  - `auto` → a regra do BCT-2 (luminância da LETRA), **preservada** para quem não declara fundo.
  A superfície **`2. Nomes de inimigos (combate)` nasce com `Fundo = escuro`** (o dono confirmou
  o campo escuro). As outras superfícies (dado, rótulos, tooltip) ficam em `auto` — **nenhuma
  mudança de comportamento** no que já estava aprovado. É uma chave nova no `.cfg`; a regra de
  cores do BCT-2 continua viva no modo `auto`.
- **Diagnóstico de cor no log (novo):** o diagnóstico de arranque e o detalhe do alvo passam a
  imprimir a **cor da LETRA** do alvo (`#RRGGBB`, alfa e luminância) e a cor de sombra que
  **ficou no material** (`_UnderlayColor`). Antes só saía `sombra=on` (a chave do config) — foi
  por essa lacuna que "a sombra não aparece" ficou sem número para conferir.
- **Testes:** `tools/testes/testes/puros/t_bct_sombra_visivel_fundo_escuro.py` + a seção 13 de
  `regras_bct.py` — o fundo `escuro` dando sombra clara à letra clara (o conserto), o `auto`
  preservando a regra do BCT-2, os defaults por superfície e a regra no fonte. Provado
  reprovando: com o fundo das NOMES de volta em `auto` e com a regra deixando de ligar fundo
  escuro à sombra clara (`tools/testes/bct3-sombra-visivel-prova-reprovando.log`).

## BCT-2 (02/10) — sombra ADAPTATIVA no texto de combate (working tree; nada publicado)

A sombra deixa de ser **fixa e igual ao contorno** e passa a **acompanhar a cor da letra**.

- **A regra.** A cor REAL da letra e lida do proprio componente (`TMP_Text.color` no TMP e
  `UI.Text.color` no caminho legado) e a luminancia e a `Color.grayscale` do Unity
  (`0.299R + 0.587G + 0.114B`):
  - **letra ESCURA** (luminancia **< 0.5**) → sombra **CLARA `CBB396`** (o
    `specialDescColor`/`highlightedColor` do jogo);
  - **letra CLARA** (luminancia **>= 0.5**) → sombra **ESCURA `000000`** (o preto neutro de
    antes).
  Na paleta do jogo (lida do prefab, `tools/testes/fixtures/cores-do-jogo.entrada.json`) so o
  `shadowColor` #F000FF (~0.395, magenta escuro) cai na sombra clara; fire #FF5353 (~0.527),
  cold #00D7FF (~0.609), lightning #EFFF00 (~0.867), healing #6BFF6F (~0.762), mana #66A8FF
  (~0.620) e physical #FFFFFF (1.000) caem na sombra escura.
- **REAVALIACAO SEM RE-INSTANCIAR.** O guarda de idempotencia por InstanceID **continua** (o
  material nunca e re-instanciado). Mas o jogo pode **REUSAR** o mesmo componente trocando a
  cor (o dado que vira fogo e depois gelo): a cada chamada o mod **rele a cor** e, se o **balde**
  virar, atualiza **SO a cor da sombra** — `_UnderlayColor` no TMP, `Shadow.effectColor` no
  legado — sem `new Material`/`AddComponent`. Um texto reusado nao fica mais com a sombra da
  primeira cor.
- **CFG-1 — TRES chaves NOVAS na secao `1. Geral`** (nenhuma chave existente foi tocada):
  - `SombraAdaptativa` (bool, padrao **true**) — `false` volta ao comportamento **FIXO** de
    antes (sombra = cor do contorno, independente da letra);
  - `CorSombraClara` (string, padrao **`CBB396`**) — sombra da letra escura;
  - `CorSombraEscura` (string, padrao **`000000`**) — sombra da letra clara.
- **Testes:** `tools/testes/testes/puros/t_bct_sombra_adaptativa.py` + secao 12 de
  `regras_bct.py` — a regra pura (cor → luminancia → balde → hex) lendo a paleta da fixture, as
  tres chaves, a leitura da cor e o **reuso** (balde que vira) no modelo de idempotencia. Provado
  reprovando: com a "sombra fixa que ignora a luminancia" e com a reavaliacao arrancada
  (`tools/testes/bct2-sombra-prova-reprovando.log`).

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

