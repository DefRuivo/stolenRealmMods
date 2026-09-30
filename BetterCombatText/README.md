# BetterCombatText

Mod **BepInEx 5** para **Stolen Realm** que deixa o **texto de combate legivel**: um **contorno/halo suave em volta das letras** (padrao: **preto a 10% de alfa** — o "sombreamento radial de 10%") nos **nomes dos inimigos** e nos **rotulos/stacks de buff e debuff**, mais o **texto do dado nos eventos de rolagem**. **Nao altera gameplay.**

- **GUID:** `com.gumatos.bettercombattext`
- **Versao:** 0.1.0
- **Compativel com:** Stolen Realm **v1.3.1** (versao mais recente do jogo em 30/09/2026).
- **Dependencias:** nenhuma alem do BepInEx 5 (que o r2modman ja instala no perfil).

## O que ele faz

Cada superficie e ligada/desligada **de forma independente** no `.cfg`, e o efeito usa **sempre** uma **copia do material por componente** (`TMP_Text.fontMaterial`) — **nunca** o material compartilhado da fonte. Isso e o que garante que a interface inteira **nao** ganhe contorno.

| Superficie | O que recebe | Componente real no jogo |
|---|---|---|
| **Nomes de inimigos em combate** | contorno/halo suave + sombra difusa | `BossHealthbar.BossName` (barra de chefe) e `PlayerInfoWindow.playerName` (janela que abre ao passar o mouse no inimigo) |
| **Rotulos de buff/debuff em combate** | contorno duro + sombra + negrito | `StatusIcon.stackCount` ("x3") e `StatusIcon.turnCount` (turnos restantes) |
| **Texto do dado nos eventos** | contorno/halo suave + sombra | `DiceVisualSetup.DiceNumbers` (o numero na face do dado) e `DiceRoller.TargetText/ResultText/ModifierValueText` |
| **Numero de vida** (extra, **desligado** por padrao) | contorno/halo suave | `Healthbar.healthbarText` |

### Limitacao honesta: os rotulos de buff/debuff NAO ganham halo suave

Os rotulos `xN` e o contador de turnos dos icones de status sao **`UnityEngine.UI.Text` (o texto legado do Unity)**, e nao `TextMeshPro` — o campo e literalmente `public Text stackCount;` no decompilado (l.174764). Texto legado desenha com **atlas de bitmap**, sem *distance field*: nao existe `_OutlineWidth`/`_OutlineSoftness` para borrar. Ali o mod aplica o que **existe**: contorno duro (componente `Outline`, 4 copias) + sombra dura + **negrito** + tamanho opcional. Para esses rotulos terem halo **suave** seria preciso trocar os componentes `UI.Text` por `TextMeshProUGUI` no prefab — mudanca grande e arriscada, fora do escopo deste mod. Está tudo explicado na secao `3.` do `.cfg`.

## Como configurar

Arquivo: `BepInEx\config\com.gumatos.bettercombattext.cfg` (editavel no Notepad).

- **Desligar TUDO em 1 linha:** na secao `1. Geral`, `Ativar = false`. O mod nao aplica nem patch — o jogo roda 100% original.
- **Contorno mais forte/fraco:** `LarguraContorno` (espessura) e `AlfaContorno` (opacidade, padrao `0.10` = os 10%).
- **Halo mais suave ou mais duro:** `SuavidadeContorno` — **alto** = halo suave, `0` = contorno duro.
- **Sombra difusa:** `Sombra = true/false` + `SombraOffsetX` / `SombraOffsetY` / `SombraSuavidade` / `AlfaSombra`.
- **Tamanho da fonte:** `TamanhoFonteExtra` — **`0` = nao mexe no tamanho** (padrao).
- **So os eventos:** `4. Eventos (texto do dado)` > `Ativar = false` desliga apenas o dado e mantem o combate.
- **Diagnostico de arranque:** `1. Geral` > `DiagnosticoNoArranque` (padrao `true`). Ligue para testar: no boot o mod varre a cena (uma vez a cada 5s) e escreve no log a fonte/material/shader dos alvos — somente leitura, nada e alterado. `false` = **nenhuma varredura de cena** (custo zero) e o log so registra que o diagnostico esta desligado. A varredura **para sozinha no primeiro alvo que aparece em cena** (ou aos 240s, se nenhum aparecer).
- Mudou o `.cfg`? **Reinicie o jogo** — os valores sao lidos no boot.

## Convivência com o BetterFont (com os dois ligados)

O **BetterFont** troca a fonte da interface pela serifada, mas **pula** o texto cujo material **em uso** não é o material padrão da fonte dele (`BetterFont/Plugin.cs:441`, com a regra em `EhEstilizado`, `:537-560`) — é a proteção dele para não apagar a cor/contorno/sombra do jogo. Este mod cria uma **cópia de material por componente**, e essa cópia deixa de ser "o material da fonte" — então, com os dois ligados, **os textos de combate (nomes de inimigo, rótulos/stacks de buff e o texto do dado) tendem a manter a fonte ORIGINAL enquanto o resto da interface fica serifada**. Depende de quem passa primeiro naquele componente: o texto que este mod já estilizou é pulado pelo BetterFont (`PularTextosEstilizados = true`, o padrão dele).

**Não quebra nada** — é puramente cosmético, e é o comportamento padrão dos dois mods. Se você quiser a serifa também nesses textos, ponha `PularTextosEstilizados = false` no `.cfg` do BetterFont: aí ele troca a fonte deles e transporta o estilo por cópia (pode ser preciso reabrir/fechar a tela para o resultado assentar).

## Log

No `BepInEx\LogOutput.log`. O mod aplica os ganchos **um a um** e escreve **uma linha por gancho** mais um resumo com a **contagem real** (sao 9 ganchos, em `Patches.cs` e `DiagnosticoArranque.cs`) — e por esse resumo que se descobre, lendo o log, que um gancho nao entrou:

```text
[Info   :Better Combat Text] Better Combat Text 0.1.0 carregado (GUID com.gumatos.bettercombattext).
[Info   :Better Combat Text] Better Combat Text: gancho aplicado — PatchNomeDoChefe (1 metodo(s) do jogo).
[Info   :Better Combat Text] Better Combat Text: gancho aplicado — ... (uma linha por gancho, com o nome dele)
[Info   :Better Combat Text] Better Combat Text: patches Harmony aplicados (9/9 ganchos, 9 metodos do jogo).
[Info   :Better Combat Text] Better Combat Text: alvos dos ganchos (por TIPO, sem parametro posicional): ...
[Info   :Better Combat Text] Better Combat Text: contorno cor=000000 alfa=0,1 largura=0,1 softness=0,6 sombra=True; eventos(dado) ativo=True; numero de vida=False; diagnostico no arranque=True.
[Info   :Better Combat Text] Better Combat Text: gatilho 'OptionsManager.Localize' vivo (primeira chamada) — o patch esta rodando.
[Info   :Better Combat Text] Better Combat Text: alvo encontrado em cena — diagnostico encerrado (nada mais e varrido).
```

E o **diagnostico de arranque** (somente leitura, `DiagnosticoNoArranque = true`), em trecho **capturado** de uma execucao do mod no jogo (30/09/2026):

```text
[Info   :Better Combat Text] Better Combat Text: --- diagnostico de arranque (somente leitura, nada alterado) ---
[Info   :Better Combat Text] Better Combat Text: PlayerInfoWindow.playerName (NOME DO INIMIGO no hover em combate) -> objeto='Target Name', tipo=TextMeshProUGUI, fonte='Title Font (Trajan Pro Regular) SDF Info', material compartilhado='Title Font (Trajan Pro Regular) SDF Material', shader='TextMeshPro/Distance Field Overlay', distance field (tem _OutlineWidth)=True
[Info   :Better Combat Text] Better Combat Text: BossHealthbar.BossName (NOME DO INIMIGO na barra de chefe) -> objeto='Target Name (1)', tipo=TextMeshProUGUI, fonte='Title Font (Trajan Pro Regular) SDF Info', material compartilhado='Title Font (Trajan Pro Regular) SDF Material', shader='TextMeshPro/Distance Field Overlay', distance field (tem _OutlineWidth)=True
[Info   :Better Combat Text] Better Combat Text: DiceVisualSetup.DiceNumbers (NUMERO NA FACE DO DADO) -> objeto='2', tipo=TextMeshPro, fonte='Title Font (Trajan Pro Regular) SDF Dice', material compartilhado='Title Font (Trajan Pro Regular) SDF Material', shader='TextMeshPro/Distance Field (Surface)', distance field (tem _OutlineWidth)=True
[Info   :Better Combat Text] Better Combat Text: faces de dado (TextMeshPro) encontradas: 140 em 7 DiceVisualSetup.
[Info   :Better Combat Text] Better Combat Text: StatusIcon em cena: 124 (124 com stackCount).
[Info   :Better Combat Text] Better Combat Text: tipo REAL do rotulo de stack = 'UnityEngine.UI.Text' — UI.Text LEGADO: halo SUAVE e impossivel ali; aplicado contorno duro + sombra + negrito.
[Info   :Better Combat Text] Better Combat Text: TextMesh legado (3D) em cena: 0 — esse tipo (usado por DieSideAwareTextDie) NAO e tocado pelo mod; ...
[Info   :Better Combat Text] Better Combat Text: total de TMP_Text em cena: 1145 (so os alvos sao tocados).
[Info   :Better Combat Text] Better Combat Text: --- fim do diagnostico ---
```

(Nessa execucao as linhas de `Tooltip.Title` e `DiceRoller.ResultText` sairam como *"nenhuma instancia em cena agora"* — normal antes de abrir o tooltip ou a tela do evento. As contagens de cena mudam de tela para tela e de boot para boot.)

### O que esta confirmado — e o que NAO esta (30/09/2026)

O que existe de artefato e o **diagnostico de arranque executado no jogo** (o trecho acima, copiado do `LogOutput.log`). Ele prova **viabilidade tecnica**:

- **O material dos alvos TMP e distance field:** os tres alvos de texto do combate/dado usam variantes `TextMeshPro/Distance Field*` (`Overlay`, `(Surface)`, `Distance Field`) e o teste em runtime `HasProperty("_OutlineWidth")` deu `True` em todos — logo o halo **suave** e viavel nesses componentes.
- **O texto do dado E TextMeshPro:** 140 faces em 7 `DiceVisualSetup`, todas `TextMeshPro`. A variante legada `DieSideAwareTextDie` (`TextMesh`) tem **0** instancias em cena neste build.
- **Os rotulos de stack SAO `UnityEngine.UI.Text` legado**, confirmado pelo tipo real em runtime (124 `StatusIcon`, todos com `stackCount`). Ali o halo suave nao existe; o mod aplica contorno duro + sombra + negrito.
- **Nesta execucao havia 1145 `TMP_Text` em cena** (o numero varia com a tela): editar o material compartilhado pintaria todos. Por isso a regra de clonar por componente e o que mantem o efeito so nos alvos.

**O que NAO esta confirmado:** o **efeito visual**. Ninguem olhou a tela com o mod ligado — o diagnostico prova que o halo e *possivel* (material distance field), nao que ele *aparece*, nem que ficou bom. **Depende do dono ver em jogo** (abrir um combate e um evento de dado e olhar). Nao ha log de "antes/depois" nem captura de tela no repositorio.

## Instalar

**Pelo r2modman (recomendado):** instale o pacote no perfil do Stolen Realm — a DLL vai para `BepInEx\plugins\BetterCombatText\BetterCombatText.dll`.

**Manual:** copie a pasta `BetterCombatText` para `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\`.

## Como desfazer

Apague a pasta `BepInEx\plugins\BetterCombatText\` (ou desabilite o pacote no r2modman) e abra o jogo. O texto volta ao original no proximo boot: o mod **nao modifica nenhum arquivo do jogo** nem deixa residuo. (Alternativa sem desinstalar: `Ativar = false` no `.cfg`.)

## Compilar do fonte

```powershell
cd BetterCombatText
dotnet build
```

Saida: `bin\Debug\netstandard2.1\BetterCombatText.dll`. As DLLs de referencia vem de `..\lib\` e **nunca sao distribuidas** — a `Assembly-CSharp.dll` e propriedade do jogo.
