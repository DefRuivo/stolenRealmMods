# NULL-1 — varredura do "fake null" (o gancho que dispara e volta calado)

Escopo: os 6 mods do pacote (BetterCombatText, BetterFont, BetterStats, BetterTooltips,
RoguelikeDebugger, RoguelikeSkillTreeVisualizer). **Nada foi instalado no perfil do r2modman,
commitado, empacotado ou publicado.**

Baseline: working tree de 01/10/2026 14:04 (md5 de todos os `.cs`). Depois disso a UNICA
mutacao de fonte foi minha (`RoguelikeSkillTreeVisualizer/RunButton.cs`) — conferido por md5.

> Nota (FIX-6, 01/10): depois desta varredura o unico `.cs` tocado foi `BetterFont/Plugin.cs` — o
> valor de `TetoDiagEscape`, de 700 para 900 (achado 2 da REV-56). Aquela mudanca foi feita **sem
> alterar o numero de linhas do arquivo**, de proposito. O que envelheceu as citacoes `arquivo:linha`
> desta tabela foram as insercoes de tarefas POSTERIORES (nao do FIX-6), que deslocaram
> `BetterFont/Plugin.cs` e `BetterCombatText/TextStyler.cs`: a DOC-15 (01/10) reconferiu cada uma
> linha a linha, no arquivo, e reescreveu todas com o IDENTIFICADOR do trecho ao lado da linha (em
> `TextStyler.cs` o deslocamento NAO e uniforme; em `Plugin.cs` e +8 (exceto +2 na declaracao de
> `Instance`, que era a l.322). (`tools/checa_citacoes.py` confere a faixa; a conferencia linha a linha
> continua sendo leitura humana.)

## 0. O que decide a classificacao

1. **O fake null so existe para `UnityEngine.Object`** (MonoBehaviour, GameObject, Component,
   Transform/RectTransform, TMP_Text, Material, Shader, Font/TMP_FontAsset, Button, Image...).
   `Character` **NAO** e objeto da Unity: no decompilado e `Character : CharacterBase : Observable`
   (l.29615 / l.476520 / l.450567) — classe C# pura. Todo `character == null`, `alvo == null`,
   `atual == null`, `receptor == null` do pacote e o null do CLR e **nao pode** virar fake null.
2. **So a referencia GUARDADA pode estar destruida.** Um local lido agora de um objeto vivo nao
   tem como estar morto. A varredura separa: (a) **estado guardado em campo** — **49 referencias**
   `arquivo:linha` (a secao 1 as lista uma a uma) — a UNIDADE desta fatia e a REFERENCIA da tabela,
   nao a comparacao solta: o "39" das versoes anteriores nao saia de regra declarada nenhuma e a
   propria secao cita 49 (correcao do FIX-6, achado 4 da REV-56), unica superficie onde a armadilha
   pode morder (secao 1); (b) **referencia obtida na hora** — 520 comparacoes (secao 2).
3. Classes: **L** = LEGITIMA (o operador da Unity e a pergunta certa, ou nao e objeto da Unity);
   **S** = SUSPEITA; **A** = AMBIGUA (motivo escrito).

### Numeros

| | n |
|---|---|
| comparacoes `== null`/`!= null` encontradas | 571 |
| em codigo | 559 |
| em comentario/doc (nao executam) | 12 |
| **sobre objeto da Unity** | **203** |
| sobre tipo NAO-Unity (`string`, array, `List<>`, `Character`, assets, delegates, `ConfigEntry`) | 356 |
| dessas, **estado guardado em campo** | **49 referencias** (secao 1) |
| **SUSPEITA confirmada** | **1** |
| dentro de `Prefix`/`Postfix` | 85 |

**Onde a armadilha NAO esta:** os ganchos do pacote usam `== null` como guarda de ENTRADA em
**tres** lugares — e os tres sao SEGUROS, porque o objeto comparado esta VIVO na propria chamada e
nao e estado guardado de algo que a cena possa destruir: `BetterStats/Plugin.cs:154`
(`character == null || __instance == null || __instance.AttributesValuesMainHolder == null`, num
Postfix — `Character` e classe C# pura, `__instance` e o objeto DA CHAMADA e o membro e de objeto
vivo), `RoguelikeDebugger/Patches/EventRollDebugPatch.cs:23` (`__result == null`: o retorno do
proprio metodo patchado) e `RoguelikeDebugger/Patches/ExpDebugPatch.cs:45` (`__instance == null`, de
novo sobre `Character`). A frase que estava aqui — "nenhum gancho do pacote usa `== null` como guarda
de ENTRADA" — era FALSA e foi corrigida no FIX-6 (achado 4 da REV-56); os tres casos estao
classificados na secao 2. As 85 comparacoes dentro de ganchos sao `!Plugin.Ativo` / valor de config
(bool estatico), parametros `__instance`/`__result`/`__2` (vivos na chamada) e `ReadOnlySession.Active`.
O padrao que produziu a licao errada (guarda sobre a instancia do plugin) **nao existe nos 6 mods**.

---

## 1. Estado guardado em campo — as 49 referencias que decidem

| arquivo:linha | comparacao | onde | classe | o que faz / por que |
|---|---|---|---|---|
| `BetterFont/Plugin.cs:452` (`Create()`) | `Instance != null` | Create() | **L** | O updater que ESTE mod cria uma vez. `!= null` = 'ja existe um VIVO'. Com um updater DESTRUIDO o operador devolve falso e o metodo cai na criacao — que e o comportamento desejado. **Trocar por ReferenceEquals AQUI introduziria a armadilha** (sairia cedo com um updater morto). |
| `BetterFont/Plugin.cs:464` (`Ensure()`) | `Instance == null` | Ensure() | **L** | O conserto padrao da armadilha: destruido (fake null) -> verdadeiro -> `Create()`. Vivo -> nao cria e so faz a varredura. |
| `BetterFont/Plugin.cs:491` (`OnDestroy()`) | `Instance == this` | OnDestroy() | **A** | A intencao e IDENTIDADE ('a estatica aponta para mim?'), nao vida. Com o operador da Unity funciona (compara InstanceID) e o pior caso (nao zerar) e inofensivo porque a l.464 recria. `ReferenceEquals(Instance, this)` seria a forma exata; nao trocado por nao haver defeito. |
| `BetterFont/Plugin.cs:472` (`Ensure()`) | `Instance?.MaybeSweep()` | Ensure() | **A** | `?.` usa o null do CLR e **nao** protege contra objeto destruido. Inalcancavel com objeto morto na pratica: a l.464 recria o updater ANTES desta linha. A protecao vem da l.464 — registrado para ninguem 'simplificar' isso tirando a l.464. |
| `BetterFont/Plugin.cs:554, 557, 564, 753` (`FontSweep()`; `RegistrarFallback()`) | `_serifFont == null`, `_serifFont.fallbackFontAssetTable == null` | FontSweep()/RegistrarFallback() | **L** | `_serifFont` e o asset NOSSO, criado em runtime por `CreateFontAsset`: nao morre em troca de cena (vive enquanto o updater vive). `fallbackFontAssetTable` vem null em asset criado em runtime — a checagem e literal. |
| `BetterFont/Plugin.cs:794, 870, 1221, 1401, 1422, 1499, 1526` (`EhEstilizado()`; `EstiloTransportavel()`; `UsaMaterialDaFonteNova()`; `OrcamentoDoDiagnosticoPorCena()`; `CatalogoDoMaterialNovo()`) | `_serifFont != null` | varios | **L** | Leitura do nosso asset; a l.554 ja garantiu que nao e nulo. |
| `BetterTooltips/Patches/LocalizePatch.cs:528, 610, 613` (`ComACorDoJogo()`, `CorDaLinhaDeAuras()`) | `_corEspecialDoJogo == null`, `_corAuraDoJogo == null` | `ComACorDoJogo()` / `CorDaLinhaDeAuras()` (esta le a cor por `LerCorAzulDoJogo()`) | **L** | Sao **string** (cache de cor lida do jogo), nao objeto da Unity: `== null` e o null do CLR. |
| `BetterTooltips/Patches/GlobulePatch.cs:178` | `_cacheTiers != null` | PctDasTiersAtivas() | **L** | `List<string>`. A outra ponta do cache (`_cacheChar`) e `Character` — classe pura. |
| `BetterTooltips/Patches/StatusSkillSynergyPatch.cs:275` | `_indice != null` | montagem do indice | **L** | Lista montada pelo mod. |
| `RoguelikeSkillTreeVisualizer/RstvHost.cs:31` | `_instance != null` | Ensure() | **L** | O driver do mod criado uma vez. Destruido -> fake null -> recria. **Trocar por ReferenceEquals devolveria o host MORTO** e mataria o Update de todo o mod. |
| `RoguelikeSkillTreeVisualizer/RunButton.cs:97` | `_owner == ui && _button != null` | EnsureInternal() | **L** | Idempotencia por instancia: 'o clone ainda esta VIVO?'. Clone destruido -> operador falso -> reinjeta. Operador da Unity e a pergunta certa. |
| `RoguelikeSkillTreeVisualizer/RunButton.cs:193` | `_button == null` | Mirror() | **S — CORRIGIDA** | ERA A SUSPEITA: com o MESMO HUD e o clone destruido, caia num `return` sem UMA linha de log e o botao nunca voltava. Corrigida: reinjeta (no maximo 1x/2 s) e escreve o motivo. Ver secao 3. |
| `RoguelikeSkillTreeVisualizer/RunButton.cs:216, 291, 296` | `_button == null`, `_button != null` | Mirror()/Hide() | **L** | Rechecagem logo apos a reinjecao (a falha ja foi logada por `Ensure`/`Fail`) e protecao do Hide: mexer so no clone VIVO. |
| `RoguelikeSkillTreeVisualizer/SelectPartyButton.cs:66` | `_owner == manager && _button != null` | Ensure() | **L** | Mesmo caso do RunButton.cs:97. |
| `RoguelikeSkillTreeVisualizer/SelectPartyButton.cs:165` | `_button == null` | Mirror() | **A** | Detecta o clone destruido, mas o ramo apenas DIAGNOSTICA (log unico por tela) e volta: quem (re)injeta e o gancho de abertura da tela. Nao e calado; ficou como esta (o do RunButton, que era calado, foi corrigido). |
| `RoguelikeSkillTreeVisualizer/SkillTreeReadOnly.cs:199, 468` | `_pendingTarget == null`, `_selectionAnterior != null` | Tick()/RestoreSelection() | **L** | `Character` — classe pura. |
| `RoguelikeSkillTreeVisualizer/SkillTreeReadOnly.cs:523, 540` | `_interceptor != null`, `_interceptorAnterior != null` | Install/RemoveCancelInterceptor() | **L** | `Func<bool>` — delegate, nao objeto da Unity. |
| `RoguelikeSkillTreeVisualizer/SkillTreeReadOnly.cs:852` | `_movedBranch != null` | ZOrder.Restore() | **L** | `Transform` guardado pelo mod: destruido -> nao restaura e o `finally` zera. **ReferenceEquals voltaria a mexer num Transform MORTO.** |
| `RoguelikeSkillTreeVisualizer/Patches.cs:69` | `__instance.selectedCharacterChoiceItem != null` | captura de `_subject` | **L** | Objeto vivo no gancho. O cache estatico `_subject` guarda `Character` — classe pura, imune. |
| `BetterCombatText/TextStyler.cs:67` (`AplicarTmp()`) | `nosso != null && nosso == compartilhadoAntes` | AplicarTmp() | **L** | Cache de Material por InstanceID que **se cura**: material destruido reprova no `!= null` e o mod reinjeta. Operador da Unity e o certo. |
| `BetterCombatText/TextStyler.cs:204` (`AplicarTextoLegado()`) | `TextosLegadosTratados.Contains(id)` | AplicarTextoLegado() | **A** | Cache 'ja tratei este rotulo' por `GetInstanceID()`. Id RECICLADO = rotulo NOVO pulado em silencio (a classe exata do defeito). A doc da Unity garante id unico apenas entre objetos VIVOS; o reuso pos-destruicao esta documentado para o **EntityId** (Unity 6.4+), nao para o `int`. Risco teorico, **nao medido em jogo** — nao trocado (proibido trocar por trocar). |
| `BetterCombatText/TextStyler.cs:182` (`AplicarTamanho()`) | `TamanhoOriginal[id]` | AplicarTamanho() | **A** | Mesma chave por InstanceID. Com id reciclado o 'tamanho original' viria do componente morto (numero errado, nao silencio). Nao medido. |
| `BetterStats/Plugin.cs:147, 148` | `_loggedBox`, `_shiftedValues` | InventoryStatPatch | **A** | Latch ESTATICO de sessao (`bool`, nao vira fake null). Se o InventoryManager fosse recriado na sessao, o deslocamento de coluna nao rodaria de novo e nada seria logado. Padrao IRMAO (estado estatico que sobrevive a instancia), nao uma comparacao com null. |
| `BetterStats/Plugin.cs:154, 319` | `Game.Instance.LevelableCharacterAttributes` (SEM guarda) | InventoryStatPatch / RoguelikeStatPatch | **A** | Unico ponto do pacote que usa `Game.Instance` sem checar. Falha e RUIDOSA (try/catch -> LogWarning), nunca calada. |
| `BetterTooltips/Patches/ShrineAuraPatch.cs:447, 789, 811, 1057, 1151` | `Burst2Flame.Game.Instance?.GetAttribute(...)` | varios | **A** | `?.` nao detecta objeto destruido — chamaria metodo num Game morto. Dentro de try/catch: falha ruidosa. O conserto, se incomodar algum dia, e checar `Game.Instance` com o operador da Unity ANTES do `?.`. |
| `RoguelikeDebugger/Patches/LootModifierDebugPatch.cs:24` | `NetworkingManager.Instance?.MyPartyCharacters` | Postfix | **A** | Idem `?.` sobre objeto da Unity; em try/catch; mod de diagnostico. Mesmo padrao em `RoguelikeDebugger/Patches/GoldModifierDebugPatch.cs:22`. |
| `RoguelikeDebugger/EfeitosInfo.cs:102, 257` | `o != null` / `uo != null` | Conta()/Valor() | **L** | **Comentario explicito no fonte**: 'o != null aqui e o operador da Unity: asset destruido conta como null'. Intencional. |

---

## 2. Referencia obtida na hora — 520 comparacoes

Regra: se o objeto foi obtido no proprio ponto (parametro do gancho, `__instance`, `__result`,
`__2`, campo de um objeto vivo como `ui.pingBtn`, elemento de colecao, item de
`Resources.FindObjectsOfTypeAll`) entao `== null` responde exatamente **"foi destruido / nao existe?"**
— que e a pergunta certa. Nao ha nada a consertar; a troca por `ReferenceEquals` seria um defeito
(passaria a aceitar objetos destruidos).

Dentro deste grupo, os casos com nuances:

| caso | arquivos:linhas | classe | por que |
|---|---|---|---|
| itens de `Resources.FindObjectsOfTypeAll<T>()` | BetterFont/Plugin.cs:583 e mais; BetterCombatText/DiagnosticoArranque.cs:117,120,123,126,133,139,144,157,192,194,207,226,228; BetterCombatText/TextStyler.cs:358, 371, 396 | L | a lista inclui objetos destruidos; pular e a intencao. |
| guardas de ENTRADA do gancho (`__instance`/`__result`) | BetterStats/Plugin.cs:154; RoguelikeDebugger/Patches/EventRollDebugPatch.cs:23; RoguelikeDebugger/Patches/ExpDebugPatch.cs:45 | L | o que se compara esta VIVO na chamada: `__result` e o retorno do metodo patchado (asset do jogo), `__instance` e o objeto da chamada e `character`/`AttributesValuesMainHolder` sao `Character` (classe C# pura) e membro de objeto vivo. Ver a correcao da frase na secao 0. |
| membros de objetos vivos (`X.gameObject`, `X.transform`, `X.font`, `X.material`, `X.tooltip`, `X.shader`, `X.atlasTexture`) | varias | L | se o membro morreu, 'nao usar' e o certo. |
| singletons do JOGO (`GameLogic.instance`, `GUIManager.instance`, `PauseMenu.instance`, `UIWindowManager.Instance`, `CurrentCharacterUI.Instance`, `NetworkingManager.Instance`, `HexCellManager.instance`, `CharacterChoiceManager.Instance`, `LoadableUIWindow<T>.Instance`) | varias | L | ausente/destruido = caminho alternativo correto. O proprio jogo usa `_Instance == null` para re-buscar (`UIWindowManager.Instance`, l.336409) e `LoadableUIWindow<T>.OnDestroy` faz `Instance = default(T)` — ou seja, nulo ali significa 'nao carregado' de VERDADE. |


---

## 3. Correcao aplicada (a unica SUSPEITA)

`RoguelikeSkillTreeVisualizer/RunButton.cs` — `Mirror()`.

**Antes** (`_button == null && _triedFor != ui` + `if (_button == null || _owner != ui) return;`):
com o HUD da run ainda VIVO (`_triedFor == ui`) e o clone destruido (fake null, `_button == null`
verdadeiro), o metodo caia no `return` da segunda condicao **sem escrever nada** — o gancho
disparava 10x/s, via o clone morto e voltava calado; o botao nao voltava para o resto daquele HUD.
E o sintoma exato desta tarefa: indistinguivel, no log, de 'o gancho nao roda'.

**Depois**: um unico ramo `if (_button == null)` que (a) em HUD NOVO tenta na hora (como antes,
uma tentativa por instancia via `_triedFor`) e (b) no MESMO HUD **reinjeta**, no maximo uma vez a
cada 2 s (`_proximaTentativa` / `IntervaloDeReinjecao`), e escreve o motivo pelo `Fail()` — que ja
loga **uma vez por motivo** (nao a cada 0,1 s). O `return` silencioso deixou de existir.

Por que o operador da Unity fica: `_button == null` e a pergunta certa ('o clone foi destruido?').
A troca para `ReferenceEquals` seria o defeito — passaria a tratar o clone MORTO como presente e o
mod mexeria num GameObject inexistente. O conserto nao e trocar o teste, e sim **parar de sair
calado** depois dele.

Compila: `dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj --no-incremental
-p:DeployToBepInEx=false` -> 0 erros; a string nova foi conferida DENTRO da DLL com `ilspycmd`.
Nao instalado no perfil (a escotilha `-p:DeployToBepInEx=false` foi usada; o md5 da DLL do perfil
segue o antigo).

---

## 4. O que ficou como esta, e por que

Todas as **A** da secao 1, resumidas:

- `BetterFont/Plugin.cs:491` (`OnDestroy()`) `Instance == this` — identidade, nao vida; funciona, `ReferenceEquals` seria mais exato, sem defeito observado.
- `BetterFont/Plugin.cs:472` (`Ensure()`) `Instance?.MaybeSweep()` — `?.` nao pega destruido, mas a l.464 recria antes. Nao 'simplificar' tirando a l.464.
- `TextStyler.cs:182/204` — caches por `GetInstanceID()`; reuso pos-destruicao NAO e documentado para o `int`; risco teorico, nao medido; a regra do projeto proibe trocar por trocar.
- `BetterStats/Plugin.cs:147/148` — latches estaticos de sessao (padrao IRMAO: estado que sobrevive a instancia), nao comparacao com null.
- `BetterStats/Plugin.cs:154/319` e as `Game.Instance?.GetAttribute` do ShrineAuraPatch/`NetworkingManager.Instance?.` do Debugger — falha RUIDOSA (try/catch), nunca calada.
- `SelectPartyButton.cs:165` — detecta o clone destruido e DIAGNOSTICA; nao e calado.

**Nao ha nenhum caminho calado remanescente** que eu tenha encontrado: todo `return` por objeto
ausente/destruido no pacote ou (a) e o comportamento correto (nao ha tela/janela), ou (b) escreve
no log, ou (c) recria o objeto.

### Padrao IRMAO (driver/updater criado uma vez)

| driver | guarda | veredito |
|---|---|---|
| `BetterFont` — `FontUpdater.Instance` (BetterFont/Plugin.cs:324) | `!= null` em `Create()`, `== null` em `Ensure()`, `_everDestroyed` em `OnDestroy` | **ja protegido** (recria; `_everDestroyed` so muda a mensagem). Correcao veio junto do BF-1/BF-2 (working tree de hoje). |
| `RSTV` — `RstvHost._instance` (RstvHost.cs:24) | `if (_instance != null) return _instance;` | **ja protegido** (destruido -> recria). |
| `RSTV` — `RunButton._button` | ver secao 3 | **era a falha; corrigida agora.** |
| `RSTV` — `SelectPartyButton._button` | `== null` -> diagnostico | aceito. |
| `BetterStats` — `_shiftedValues` / `_loggedBox` | latch bool de sessao | nao e fake null; registrado. |
| `BetterCombatText` / `BetterTooltips` / `RoguelikeDebugger` | nao criam driver/updater | n/a. |

---

## 5. Apendice — as 203 comparacoes sobre objeto da Unity, por arquivo

### BetterCombatText/DiagnosticoArranque.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 123 | `t` | ? | L |
| 139 | `if (primeiraFace` | TMP_Text | L |
| 144 | `if (primeiraFace` | TMP_Text | L |
| 157 | `if (icone` | ? | L |
| 157 | `icone.stackCount` | ? | L |
| 192 | `alvo` | TMP_Text | L |
| 207 | `if (alvo` | TMP_Text | L |
| 223 | `mat` | ? | L |
| 226 | `(alvo.font` | TMP_Text | L |
| 227 | `(mat` | ? | L |
| 228 | `(mat` | ? | L |
| 228 | `mat.shader` | ? | L |

### BetterCombatText/Patches.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 103 | `icone` | StatusIcon | L |

### BetterCombatText/TextStyler.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 48 · `AplicarTmp()` | `if (tmp` | TMP_Text | L |
| 60 · `AplicarTmp()` | `if (compartilhadoAntes` | ? | L |
| 67 · `AplicarTmp()` | `nosso` | ? | L |
| 74 · `AplicarTmp()` | `if (mat` | Material | L |
| 82 · `AplicarTmp()` | `shader` | ? | L |
| 192 · `AplicarTextoLegado()` | `if (txt` | Text | L |
| 214 · `AplicarTextoLegado()` | `graphics` | ? | L |
| 221 · `AplicarTextoLegado()` | `if (contorno` | ? | L |
| 240 · `AplicarTextoLegado()` | `if (sombra` | ? | L |
| 312 · `DetalharAlvo()` | `tmp.font` | TMP_Text | L |
| 313 · `DetalharAlvo()` | `compartilhadoAntes` | ? | L |
| 358 · `InventarioDeCena()` | `if (t` | TMP_Text | L |
| 371 · `InventarioDeCena()` | `m` | Material | L |
| 396 · `Nome()` | `return t` | ? | L |
| 396 · `Nome()` | `t.gameObject` | TMP_Text | L |

### BetterFont/Plugin.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 452 · `Create()` | `if (Instance` | ? | L |
| 464 · `Ensure()` | `if (Instance` | ? | L |
| 554 · `FontSweep()` | `if (_serifFont` | TMP_FontAsset | L |
| 557 · `FontSweep()` | `if (_serifFont` | TMP_FontAsset | L |
| 564 · `FontSweep()` | `if (_serifFont.fallbackFontAssetTable` | TMP_FontAsset | L |
| 583 · `FontSweep()` | `if (t` | TMP_Text | L |
| 671 · `FontSweep()` | `antigo` | Material | L |
| 675 · `FontSweep()` | `if (novo` | mais | L |
| 753 · `RegistrarFallback()` | `if (_serifFont.fallbackFontAssetTable` | TMP_FontAsset | L |
| 757 · `RegistrarFallback()` | `if (t.font` | TMP_Text | L |
| 782 · `EhEstilizado()` | `if (antigo` | Material | L |
| 787 · `EhEstilizado()` | `if (fonteAntiga` | TMP_FontAsset | L |
| 787 · `EhEstilizado()` | `fonteAntiga.material` | TMP_FontAsset | L |
| 794 · `EhEstilizado()` | `_serifFont` | TMP_FontAsset | L |
| 795 · `EhEstilizado()` | `if (padraoNovo` | Material | L |
| 834 · `EstiloTransportavel()` | `if (antigo` | Material | L |
| 870 · `EstiloTransportavel()` | `_serifFont` | TMP_FontAsset | L |
| 871 · `EstiloTransportavel()` | `if (padraoNovo` | Material | L |
| 914 · `TemEfeitoNoMaterial()` | `if (m` | Material | L |
| 964 · `TexturaDeEfeito()` | `if (tex` | Texture | L |
| 1171 · `RegistrarDiferenca()` | `if (antigo` | Material | L |
| 1171 · `RegistrarDiferenca()` | `novo` | mais | L |
| 1221 · `UsaMaterialDaFonteNova()` | `_serifFont` | TMP_FontAsset | L |
| 1222 · `UsaMaterialDaFonteNova()` | `if (m` | Material | L |
| 1222 · `UsaMaterialDaFonteNova()` | `atlas` | do | L |
| 1227 · `UsaMaterialDaFonteNova()` | `return tex` | ? | L |
| 1244 · `NomeObjeto()` | `return t` | ? | L |
| 1244 · `NomeObjeto()` | `t.gameObject` | TMP_Text | L |
| 1387 · `OrcamentoDoDiagnosticoPorCena()` | `antigo` | Material | L |
| 1401 · `OrcamentoDoDiagnosticoPorCena()` | `_serifFont` | TMP_FontAsset | L |
| 1403 · `OrcamentoDoDiagnosticoPorCena()` | `(materialNovo` | Material | L |
| 1421 · `OrcamentoDoDiagnosticoPorCena()` | `(fonteAntiga` | TMP_FontAsset | L |
| 1422 · `OrcamentoDoDiagnosticoPorCena()` | `(_serifFont` | TMP_FontAsset | L |
| 1423 · `OrcamentoDoDiagnosticoPorCena()` | `(antigo` | Material | L |
| 1453 · `ReverterTexto()` | `if (fonteAntiga` | TMP_FontAsset | L |
| 1464 · `ReverterTexto()` | `if (antigo` | Material | L |
| 1499 · `CatalogoDoMaterialNovo()` | `_serifFont` | TMP_FontAsset | L |
| 1500 · `CatalogoDoMaterialNovo()` | `if (m` | Material | L |
| 1526 · `CatalogoDoMaterialNovo()` | `(_serifFont` | TMP_FontAsset | L |
| 1577 · `CreateSerifFont()` | `if (fileFont` | Font | L |
| 1582 · `CreateSerifFont()` | `if (asset` | TMP_FontAsset | L |
| 1603 · `CreateSerifFont()` | `if (osFont` | Font | L |
| 1608 · `CreateSerifFont()` | `if (asset` | TMP_FontAsset | L |

### BetterStats/Plugin.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 154 | `__instance` | InventoryManager | A |
| 154 | `__instance.AttributesValuesMainHolder` | InventoryManager | A |
| 173 | `((child` | Transform | L |
| 174 | `if (component` | TextMeshProUGUI | L |
| 206 | `if (holderRt` | RectTransform | L |
| 310 | `if (__instance` | InventoryManager | L |
| 310 | `__instance.StatValues` | InventoryManager | L |

### BetterTooltips/Patches/LocalizePatch.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 533 · `ComACorDoJogo()` | `t != null` | Tooltip | L |
| 636 · `LerCorAzulDoJogo()` | `if (t != null` | Tooltip | L |
| 2288 · `AplicarNotasDoFunil()` | `if (original == null \|\| __result == null` | string | L |

> Reconferido em 01/10 (DOC-11): os tres numeros desta tabela apontavam para outro conteudo
> (o deslocamento veio das insercoes de COR-1/COR-2/COR-3 e RV-17 no mesmo arquivo) e passaram a
> vir com o **IDENTIFICADOR do trecho** ao lado da linha — numero de linha de `.cs` que muda toda
> hora envelhece sozinho, e o `checa_citacoes.py` so confere que a linha EXISTE, nunca que o
> conteudo bate.

### BetterTooltips/Patches/ShrineAuraPatch.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 497 | `if (t` | Tooltip | L |
| 501 | `if (t` | Tooltip | L |

### RoguelikeDebugger/EfeitosInfo.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 103 | `if (o` | UnityEngine.Object | L |
| 187 | `if (o` | UnityEngine.Object | L |

### RoguelikeDebugger/Patches/LootModifierDebugPatch.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 41 | `if (root` | ? | L |
| 42 | `root.RoguelikePowerupsByConnection` | ? | L |

### RoguelikeSkillTreeVisualizer/Patches.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 69 | `__instance` | CharacterChoiceManager | L |
| 69 | `__instance.selectedCharacterChoiceItem` | CharacterChoiceManager | L |
| 139 | `__instance` | CharacterChoiceManager | L |
| 215 | `__instance` | CharacterChoiceManager | L |
| 277 | `__instance` | CharacterChoiceManager | L |
| 277 | `__instance.RespecButton` | CharacterChoiceManager | L |
| 330 | `__instance` | CharacterChoiceManager | L |
| 330 | `__instance.SkillInfo` | CharacterChoiceManager | L |

### RoguelikeSkillTreeVisualizer/RstvHost.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 31 | `if (_instance` | RstvHost | L |

### RoguelikeSkillTreeVisualizer/RunButton.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 70 | `if (ui` | CurrentCharacterUI | L |
| 85 | `if (original` | Button | L |
| 91 | `if (original.transform` | Button | L |
| 91 | `original.transform.parent` | Button | L |
| 97 | `_button` | GameObject | L |
| 104 | `if (srcRt` | RectTransform | L |
| 123 | `if (existing` | Transform | L |
| 137 | `if (newRt` | RectTransform | L |
| 153 | `if (button` | Button | L |
| 182 | `if (ui` | CurrentCharacterUI | L |
| 193 | `if (_button` | GameObject | L |
| 216 | `if (_button` | GameObject | L |
| 228 | `if (original` | Button | L |
| 256 | `if (button` | Button | L |
| 291 | `if (_button` | GameObject | L |
| 296 | `if (_button` | GameObject | L |
| 299 | `if (button` | Button | L |
| 395 | `cloneButton` | Button | L |
| 396 | `if (fundo` | Graphic | L |
| 396 | `original` | Button | L |
| 407 | `if (g` | Graphic | L |
| 429 | `(fundo` | Graphic | L |
| 449 | `if (label` | TextMeshProUGUI | L |
| 468 | `if (rt` | RectTransform | L |
| 478 | `if (novo` | TextMeshProUGUI | L |
| 533 | `return button` | ? | L |

### RoguelikeSkillTreeVisualizer/RunTargets.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 64 | `if (nm` | NetworkingManager | L |
| 64 | `nm.NetworkManager` | NetworkingManager | L |
| 86 | `return root` | ? | L |
| 105 | `if (gui` | GUIManager | L |
| 133 | `if (hcm` | HexCellManager | L |
| 147 | `if (wm` | UIWindowManager | L |
| 154 | `if (root` | Root | L |
| 213 | `if (gl` | GameLogic | L |
| 256 | `if (nm` | NetworkingManager | L |

### RoguelikeSkillTreeVisualizer/SelectPartyButton.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 40 | `if (manager` | CharacterChoiceManager | L |
| 54 | `if (original` | Button | L |
| 60 | `if (original.transform` | Button | L |
| 60 | `original.transform.parent` | Button | L |
| 66 | `_button` | GameObject | L |
| 73 | `if (srcRt` | RectTransform | L |
| 92 | `if (existing` | Transform | L |
| 106 | `if (newRt` | RectTransform | L |
| 113 | `if (cloneLabel` | TextMeshProUGUI | L |
| 126 | `if (button` | Button | L |
| 160 | `if (manager` | CharacterChoiceManager | L |
| 165 | `if (_button` | GameObject | A |
| 184 | `if (original` | Button | L |
| 196 | `if (button` | Button | L |
| 237 | `manager` | CharacterChoiceManager | L |
| 237 | `manager.gameObject` | CharacterChoiceManager | L |
| 238 | `manager` | CharacterChoiceManager | L |
| 238 | `manager.gameObject` | CharacterChoiceManager | L |
| 240 | `manager` | CharacterChoiceManager | L |
| 241 | `original` | Button | L |
| 241 | `original.transform` | Button | L |
| 248 | `(original` | Button | L |
| 249 | `(parent` | Transform | L |
| 290 | `if (le` | LayoutElement | L |
| 318 | `group` | layout | L |
| 319 | `group` | layout | L |
| 321 | `if (group` | layout | L |
| 352 | `(parent as RectTransform` | ? | L |
| 357 | `if (rect` | RectTransform | L |
| 370 | `if (row` | RectTransform | L |
| 381 | `if (child` | RectTransform | L |
| 428 | `if (parent` | Transform | L |
| 434 | `if (group` | layout | L |
| 440 | `if (grandParent` | Transform | L |
| 443 | `if (up` | HorizontalOrVerticalLayoutGroup | L |
| 454 | `if (parent` | Transform | L |
| 460 | `return group` | ? | L |
| 466 | `return le` | ? | L |
| 475 | `if (component` | Component | L |
| 485 | `if (behaviour` | Behaviour | L |

### RoguelikeSkillTreeVisualizer/SkillTreeReadOnly.cs

| linha | comparacao | tipo | classe |
|---|---|---|---|
| 92 | `if (instance` | SkillTreeManager | L |
| 98 | `if (loader` | ReferenceLoader | L |
| 205 | `if (instance` | SkillTreeManager | L |
| 232 | `if (instance` | SkillTreeManager | L |
| 232 | `instance.gameObject` | SkillTreeManager | L |
| 234 | `return "a instancia nativa da arvore nao esta mais ativa (instance` | SkillTreeManager | L |
| 238 | `if (gui` | GUIManager | L |
| 282 | `return screen` | ? | L |
| 282 | `screen.gameObject` | CharacterChoiceManager | L |
| 289 | `instance` | SkillTreeManager | L |
| 328 | `if (instance` | SkillTreeManager | L |
| 368 | `return hud` | ? | L |
| 454 | `if (gl` | GameLogic | L |
| 576 | `if (wm` | UIWindowManager | L |
| 576 | `instance` | SkillTreeManager | L |
| 624 | `if (instance` | SkillTreeManager | L |
| 630 | `wm` | UIWindowManager | L |
| 669 | `if (instance` | SkillTreeManager | L |
| 669 | `instance.gameObject` | SkillTreeManager | L |
| 675 | `wm` | UIWindowManager | L |
| 699 | `if (instance` | SkillTreeManager | L |
| 751 | `if (wm` | UIWindowManager | L |
| 763 | `if (topo` | UIWindow | L |
| 769 | `if (nossa` | SkillTreeManager | L |
| 809 | `if (above` | Transform | L |
| 815 | `if (common` | Transform | L |
| 822 | `if (branchAbove` | Transform | L |
| 822 | `branchReference` | Transform | L |
| 852 | `if (_movedBranch` | Transform | L |
| 871 | `t` | Transform | L |
| 876 | `t` | Transform | L |
| 890 | `while (current` | Transform | L |


---

## 6. Impacto na Release do REL-1 (o que precisa de rebuild)

**Medido, nao presumido** (01/10 14:10):

1. O pipeline do REL-1 **nao compila** — ele consome `dist/gumatos-<Mod>-<versao>.zip`, gerado na
   maquina de desenvolvimento (`.github/workflows/publish.yml`, passo 4.3: "Este workflow NAO COMPILA").
   Logo, o que a guarda chama de "pacote velho" e o zip do `dist/`.
2. Estado dos zips contra a fonte (mtime do zip x .cs mais novo):

| mod | zip em dist/ | fonte mais nova | veredito |
|---|---|---|---|
| BetterCombatText | `gumatos-BetterCombatText-0.1.0.zip` (30/09 22:27) | Plugin.cs 01/10 13:13 | **VELHO** |
| BetterFont | `gumatos-BetterFont-1.0.1.zip` (30/09 22:27) | Plugin.cs 01/10 14:03 | **VELHO** |
| BetterStats | `gumatos-BetterStats-1.0.1.zip` (30/09 20:51) | Plugin.cs 30/09 20:43 | ok |
| BetterTooltips | `gumatos-BetterTooltips-0.1.1.zip` (30/09 22:52) | LocalizePatch.cs 01/10 13:34 | **VELHO** |
| RoguelikeDebugger | `gumatos-RoguelikeDebugger-0.1.1.zip` (30/09 20:51) | ActionStatusInventoryPatch.cs 01/10 13:38 | **VELHO** |
| RoguelikeSkillTreeVisualizer | `gumatos-RoguelikeSkillTreeVisualizer-0.2.0.zip` (30/09 20:31) | **RunButton.cs 01/10 14:06 (minha correcao)** | **VELHO** |

3. Portanto: **5 dos 6 pacotes precisam ser refeitos** antes de publicar (BetterStats e o unico
   consistente). O RSTV entra nessa lista **por causa desta tarefa** alem do que ja estava pendente.
   Comando, por mod (a partir da raiz do repo; `-c Release` como no workflow, e **sem** deploy para
   o perfil):

```bash
dotnet build <Mod>/<Mod>.csproj -c Release -p:DeployToBepInEx=false
python tools/pack-thunderstore.py <Mod>
```

4. **A versao publicada nao pode ser reaproveitada**: a Thunderstore recusa versao repetida
   (imutavel), e o gate `release/mods.json` + `tools/check_versoes.py` amarra `<Version>` do
   `.csproj` == `version_number` do `manifest.json` == literal do `Plugin.cs`. Cada um dos 5 mods
   refeitos precisa de bump de PATCH antes de empacotar.
5. Nao confundir com o perfil do r2modman: as DLLs do perfil estao velhas em 5 dos 6 (esperado —
   nao instalei nada, por regra da tarefa). As DLLs de `bin/` **estao todas em dia** (build de
   14:06–14:07 com `-p:DeployToBepInEx=false`), entao um novo `pack-thunderstore.py` pega fonte nova.
6. O que a guarda do REL-1 vai acusar se nada for feito: pacote do `dist/` mais velho que a fonte
   (nos 5 mods), e no RSTV a DLL dentro do zip sem a correcao desta tarefa.

---

## 7. A citacao `arquivo:linha` conferida a maquina (proposta do FIX-6)

Esta e a **terceira** citacao quebrada do dia (as duas primeiras foram nos relatorios de revisao), e
a familia e sempre a mesma: um numero que existe em OUTRO arquivo, colado da tabela vizinha (os
348/361/386 do `TextStyler.cs` no cabecalho do `DiagnosticoArranque.cs`, que tem 252 linhas — a
tabela de `TextStyler.cs` de onde esses numeros vieram e a do apendice, hoje 358/371/396), uma
linha deslocada (`LootModifierDebugPatch.cs:22` com o constructo na 24) e um caminho encurtado (os
titulos dos `Patches/` sem o segmento de pasta, em tres arquivos).

A proposta e o irmao estreito do `audita_docs.py` para LINHA — `tools/checa_citacoes.py`:

```bash
python tools/checa_citacoes.py          # exit 0 = toda citacao aponta para algo que existe
```

Ele responde, por citacao, as duas perguntas que a maquina responde sem opiniao:

1. o **arquivo** existe no repositorio? (caminho exato; nome-base so quando e unico no repo — um
   nome-base ambiguo e pendencia, porque o leitor nao sabe de qual arquivo se fala);
2. a **linha** esta dentro do arquivo? (`1 <= linha <= total`; le `12`, `12, 34`, `12, 34 e 56` e
   as faixas `12-34`).

O que ele NAO faz, de proposito: julgar se a linha CERTA foi citada — isso e leitura humana, e o
risco de uma heuristica de conteudo e acusar em massa (o projeto ja pagou por isso). O que a maquina
garante e que a citacao nao aponta para o vazio. Nesta rodada ele achou exatamente as pendencias
deste achado (as tres linhas fora do arquivo, a linha deslocada e os tres caminhos sem o `Patches/`);
consertadas, ele sai **exit 0**. Fica PROPOSTA a entrada dele no `.github/workflows/validate.yml`,
ao lado do `audita_docs.py` — e o mesmo valor daquele passo: a doc parar de citar o que nao existe.
