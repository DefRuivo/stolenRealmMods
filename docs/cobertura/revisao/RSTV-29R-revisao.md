# RSTV-29R — revisão independente da remoção da superfície do botão "Skills" na tela Select Party

- **Cartão:** `t_ea839722` (RSTV-29R) — revisão independente do `t_743240ac` (RSTV-29).
- **Revisor:** perfil `default`, execução `470`. **Autor da RSTV-29 ≠ revisor desta rodada.**
- **Data/hora da revisão:** 06/10/2026, 18:20–18:35 (−03:00).
- **Nota de reconciliação:** este arquivo foi escrito em **duas passagens da MESMA revisão**. A primeira
  (18:32) produziu os itens 1–8 e os achados A/B/C; a segunda reverificou tudo por execução, manteve os
  achados válidos, **corrigiu o item 3** (o nome do teste no cartão confere — ver adiante) e
  **acrescentou os achados documentais D/E**, que a primeira não tinha visto. Tudo abaixo foi medido.
- **Postura:** tentativa de **REFUTAÇÃO** item por item. Nada foi corrigido, instalado, publicado,
  commitado ou rodado em jogo. Nenhum arquivo de fonte do mod foi editado.
- **Contra-prova em cópia FORA do repo:** `C:/Users/Pichau/AppData/Local/hermes/cache/scratch/rstv29-sandbox-revisor`
  (+ sonda própria `…/cache/scratch/sonda-revisor-rstv29.py`). O repo não foi tocado em nenhuma delas.

## 0. Estado lido (sha256 — o arquivo que eu li, não o que o autor diz)

`sha256sum RoguelikeSkillTreeVisualizer/*.cs` (13 `.cs`; `SelectPartyButton.cs` **não existe no disco**,
a deleção está registrada **não-staged** no índice do git):

| arquivo | sha256 (12 primeiros) |
|---|---|
| `LevelUpWindowButton.cs` | `7262051e436f` |
| `NativeUiHelpers.cs` (novo, `??`) | `567d78dc7d4f` |
| `PartyTargets.cs` | `76a0f08489b9` |
| `Patches.cs` | `37304ad54550` |
| `Plugin.cs` | `c6805e6617b1` |
| `RemovalWindowSkillsButton.cs` | `37ffe4a4b5e7` |
| `RstvHost.cs` | `1f3503a3f9fa` |
| `RunButton.cs` | `dd4caccf3754` |
| `RunTargets.cs` | `4ab9db9531c7` |
| `SkillTreeReadOnly.cs` | `ec6851c50b01` |
| `SkillTreeShortcut.cs` | `6144d069dc01` |
| `SkillTreesTab.cs` | `22e03b237818` |
| `SkillTreesWindow.cs` | `aa6eda370227` |

Os 5 hashes que o pai mediu (`Patches`, `RstvHost`, `RunButton`, `Plugin`, `NativeUiHelpers`) batem
**byte a byte** com o que eu li. Nada mudou embaixo de mim durante a revisão (sha refeito no fim:
idêntico). `git log -1` = `34f929a` (o mesmo do início), `git diff --cached --name-only` **vazio**
(nada `git add`-ado), nenhum commit novo.

## 1. AUSÊNCIA REAL — nenhuma superfície viva da tela Select Party — **OK**

Menções a `SelectPartyButton` em **fonte do mod** (grep com o padrão, saída literal, `bin/obj` fora):

```
$ grep -rn "SelectPartyButton" --include="*.cs" RoguelikeSkillTreeVisualizer/ | grep -v "/bin/\|/obj/"
RoguelikeSkillTreeVisualizer/NativeUiHelpers.cs:11:    /// HISTORICO: estes estaticos nasceram dentro de <c>SelectPartyButton</c> — o botao da tela
RoguelikeSkillTreeVisualizer/NativeUiHelpers.cs:18:    /// O que morava no <c>SelectPartyButton</c> e era ESPECIFICO da tela de party (Ensure, Mirror,
RoguelikeSkillTreeVisualizer/Patches.cs:16:    // superficie: o botao da tela de escolha de grupo nao existe mais e o `SelectPartyButton.cs` foi
RoguelikeSkillTreeVisualizer/Plugin.cs:25:    /// o <c>SelectPartyButton</c> foi apagado e os ganchos daquela tela sumiram (ver `Patches.cs`).
```

**As 4 ocorrências são comentário** (3 de documentação XML `///`, 1 comentário de bloco `//`) — nenhuma
linha de código. `Ensure`/`Mirror` (grep no mod inteiro, sem `bin/obj`) só existem em
`RunButton` (`Ensure`/`Mirror`), `LevelUpWindowButton.Ensure`, `RemovalWindowSkillsButton.Ensure`,
`SkillTreesTab.Ensure` e `RstvHost.Ensure` — **nenhum** deles é da tela de party. Nenhum `RSTV DIAG`
da tela de party sobrou (`RSTV DIAG` hoje aparece só no HUD da run, no modal, no level-up e na linha de
boot da chave-mestra). Nenhum gancho Harmony aponta para a tela:

```
$ grep -rn "OpenCharacterChoiceManager\|OpenWindow" --include="*.cs" RoguelikeSkillTreeVisualizer/ | grep -v "/bin/\|/obj/"
Patches.cs:13-15,21   (comentário do cabeçalho RSTV-29)
Patches.cs:397-404,416,424   CharacterMenusManager.OpenWindow  ← aba do INVENTÁRIO (RSTV-16), não a tela de party
RunTargets.cs:179, SkillTreeShortcut.cs:24, SkillTreesTab.cs:64  (comentário)
```

O único gancho de `CharacterChoiceManager` que **fica** é `CharacterChoiceTogglePatch`
(`ToggleSelectedCharacter`, l.39-100), que não injeta botão: alimenta o `PartyTargets` do atalho.
**Refutação tentada e falhada:** procurei código efetivo remanescente (não comentário) da superfície —
não existe. `SelectPartyButton.cs` não está no disco (`ls` → *No such file or directory*), mas está no
índice como deleção não-staged (`git ls-files --deleted` → `RoguelikeSkillTreeVisualizer/SelectPartyButton.cs`).

## 2. CONFIG `AtivarBotao` como chave-mestra — **OK com ACHADO (comportamento + diagnóstico)**

Código (lido, `Plugin.cs` l.103-124):

```
BotaoLigado         = AtivarBotao == null || AtivarBotao.Value                             // l.105
RunBotaoLigado      = BotaoLigado && (AtivarBotaoNaRun == null || AtivarBotaoNaRun.Value)  // l.111
RemocaoBotaoLigado  = BotaoLigado && (AtivarBotaoNaRemocao == null || AtivarBotaoNaRemocao.Value) // l.123
AtalhoLigado        = AtalhoSkillTree == null || AtalhoSkillTree.Value                     // l.117
```

**Matriz de estados (BotaoLigado × chave específica), conferida contra os consumidores reais**
(`grep -rn "BotaoLigado\|AtalhoLigado" *.cs`, sem `bin/obj`):

| AtivarBotao | AtivarBotaoNaRun | HUD da run (`RunButton.cs:93,217`) | Botão do level-up (`LevelUpWindowButton.cs:86`) | Modal (`RemovalWindowSkillsButton.cs:103`) |
|---|---|---|---|---|
| true | true | liga | liga | — |
| true | false | desliga | desliga | — |
| false | true | **desliga** | **desliga** | **desliga** |
| false | false | desliga | desliga | desliga |

(análogo para `AtivarBotaoNaRemocao`; com a mestra `false` **toda** superfície de botão fica desligada,
inclusive o botão do level-up, que passou a ser coberto por `RunBotaoLigado`). **Nenhum caminho ficou
impossível de ligar**: `(true, true)` liga cada superfície individualmente; `(false, *)` é o "desliga
tudo" pretendido. O **atalho F10** (`AtalhoLigado`) **não** passa pela mestra — igual ao comportamento
anterior (antes da RSTV-29 `AtalhoLigado` também ignorava `AtivarBotao`), então não é regressão.

**ACHADO A (leve, comportamento) — a mudança atinge quem já tinha `AtivarBotao=false` no `.cfg`.**
Antes da RSTV-29, `RunBotaoLigado`/`RemocaoBotaoLigado` eram **só** a chave específica
(`git show HEAD:…/Plugin.cs` l.99-101 e l.111-113) e `AtivarBotao` controlava **só** o botão da tela de
party. Agora a mesma chave, mantido o nome, passou a desligar **também** o HUD da run e o modal. Quem
tivesse `AtivarBotao=false` no arquivo (para tirar o botão da tela de party, mantendo os outros) perde
os outros dois botões sem mexer em nada. É decisão deliberada e está documentada (CHANGELOG l.14-16,
`Plugin.cs` l.57-64, `KANBAN.md` l.315-316), e **na máquina do dono hoje não tem efeito** — o `.cfg` do
perfil está com `AtivarBotao = true` (lido em
`…/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`).
Registro como achado porque o cartão manda registrar regressão nas superfícies que **ficaram**, não
porque eu considere ser defeito a corrigir.

**ACHADO B (leve, diagnóstico mentiroso quando a mestra desliga).** Com `AtivarBotao=false` e as
específicas `true`, o mod grava no log o motivo **errado**:

```
RunButton.cs:96                Fail("AtivarBotaoNaRun=false no arquivo de config", false);
RunButton.cs:219               Hide("AtivarBotaoNaRun=false no arquivo de config", false);
LevelUpWindowButton.cs:89      Fail("AtivarBotaoNaRun=false no arquivo de config", false);
RemovalWindowSkillsButton.cs:106  Fail("AtivarBotaoNaRemocao=false no arquivo de config", false);
```

A causa real é `AtivarBotao=false`; o texto afirma que a chave específica está `false`. Isso contraria a
regra do projeto ("cada caminho de falha escreve no log **por que** falhou") e é **introduzido por esta
mudança** (antes o texto era verdadeiro, porque só a chave específica podia causar aquilo). Mitigação
parcial: a linha de boot (`Plugin.cs` l.197-205) informa a mestra e as específicas com o valor real.
Correção de uma linha (ex.: citar as duas chaves), fora do escopo desta revisão.

## 3. Gancho removido (`CharacterChoiceManager.OpenWindow`) — **OK**

- **O que dependia dele:** nada além da injeção. `PartyTargets` continua alimentado pelo
  `CharacterChoiceTogglePatch` (`Patches.cs` l.77-92: `IsLocal`/`NoteAddition`/`NoteRemoval`/`Resolve`);
  `ReadOnlyContext.PartyScreen` continua declarado (`RunTargets.cs:12`) e **usado**
  (`SkillTreeShortcut.cs:228`).
- **`RstvHost`:** o diff remove `private float _nextMirror;` e o bloco `SelectPartyButton.Mirror()`
  (era o único consumidor de `_nextMirror`); sobra `_nextRunMirror`, usado no `Update` (l.54-60) com
  `RunButton.Mirror()`. Nada órfão — e o build confirma (0 erros).
- **F10 na tela de party CONTINUA:** `SkillTreeShortcut.Abrir` (l.204-230) mantém o ramo
  `CharacterChoiceManager.IsNotNullAndIsActive → PartyTargets.Resolve() → SkillTreesTab.Abrir(alvo,
  ReadOnlyContext.PartyScreen)`, com a recusa explícita quando não há alvo local; `ChoosingCharacter`
  segue fora da lista de bloqueio do `Liberado` (comentário l.23-28 explica).
- **Quem prende esse ramo (CORREÇÃO do item):** o cartão cita `rstv16-aba-arvores` e o cartão **está
  certo** — `t_rstv16_aba_arvores.py:67` chama `regras_rstv16.falhas_do_readonly_e_atalho`, que exige
  `"SkillTreesTab.Abrir("` dentro de `SkillTreeShortcut.Abrir` (`regras_rstv16.py:326-333`). Há ainda um
  **segundo** cadeado, mais completo: `t_rstv11_atalho_f10.py` + `regras_rstv11.py` (l.307-320) exige os
  trechos vivos `CharacterChoiceManager.IsNotNullAndIsActive`, `PartyTargets.Resolve()`,
  `ReadOnlyContext.PartyScreen`, `RunButton.OpenForTarget` **e a ORDEM** party-antes-de-run. *(A primeira
  passagem desta revisão havia dito que "o nome do teste no cartão está trocado"; a reverificação mostra
  que o nome está CORRETO e há **dois** testes prendendo o ramo — fica registrada a correção.)* Se o F10
  tivesse ficado dependente de algo removido, ambos estariam vermelhos.

## 4. A checagem de ausência é real (não decorativa)? — **OK, com ACHADO de cobertura**

- **Lê o FONTE AO VIVO:** `regras_rstv28.le_arquivos_cs()` faz `os.listdir` + `open` da pasta do mod
  achada por `arcabouco.raiz_do_repo()` (sobe até achar `.git`/`docs/PLANO-DE-TESTES.md`) — nenhuma
  cópia, nenhuma constante. Confirmei por execução: a bancada copia o repo para o sandbox **fora** dele
  e o runner passa a ler a cópia (a planta na cópia reprova, o repo não muda).
- **Distingue código de comentário:** `recorte.codigo_efetivo` remove `//` e `/* */` (preservando
  literais). Prova nos dois sentidos, medida por mim: com `SelectPartyButton` **só em comentário** de
  linha e **só em comentário de bloco** → **não reprova**; com a mesma citação em **código vivo**
  (`RstvHost.cs`, arquivo que o autor **não** usou nas plantas dele) → **reprova**.
- **Prova de fogo — o vermelho rodado por mim:**
  `python tools/testes/prova-sandbox-rstv28.py` → **exit 0**, com
  `[(a) a chamada SelectPartyButton.Ensure de volta] exit=1` (motivo literal: *"Patches.cs ainda cita
  `SelectPartyButton` no codigo efetivo — vestigio da superficie removida"*), `restaurado byte a byte:
  True (37304ad54550e396)`, `[(b) o arquivo/classe … de volta] exit=1`, `arquivo removido de novo: True`,
  `[REPO INTACTO] True (13 .cs conferidos por sha256)`. Rodei de novo com `--sandbox` na pasta que o
  cartão exige (`…/hermes/cache/scratch/rstv29-sandbox-revisor`) → mesmo resultado, exit 0.
- **Plantas embutidas:** 4 (`arquivo/classe`, `chamada Ensure`, `gancho OpenWindow`, `linha de boot`),
  cada uma tem de reprovar pela marca certa, e cada `com_*_de_volta` é conferido como "mudou algo"
  antes (senão reprova por âncora não achada). O teste **já reprovou de verdade** — não é decoração.

**ACHADO C (leve→médio, furo de cobertura) — gancho em FORMA DE STRING passa batido.**
A regra 3 procura literalmente `nameof(CharacterChoiceManager.OpenWindow)` /
`nameof(CharacterChoiceManager.OpenCharacterChoiceManager)` e a lista `VESTIGIOS` casa **nomes** de
classe. Uma reinjeção escrita como `[HarmonyPatch(typeof(CharacterChoiceManager), "OpenWindow",
new Type[0])]` com classe de nome neutro **não é vista**. Provei com sonda própria (memória, repo
intocado):

```
gancho OpenWindow em string, classe neutra            reprovou=False  (esperado True ) *** DIVERGENCIA ***
gancho OpenCharacterChoiceManager em string           reprovou=False  (esperado True ) *** DIVERGENCIA ***
```

O projeto usa bastante a forma por string em outros ganchos, então o furo é plausível na prática. Não
invalida o veredito de ausência **atual** (o item 1 foi provado por grep direto), mas a propriedade
"nenhum Harmony apontando para aquela tela" não está fechada por teste. Sugestão (fora do escopo):
procurar também o par `CharacterChoiceManager` + `"OpenWindow"`/`"OpenCharacterChoiceManager"` no código
efetivo, independente do nome da classe.

**Observação 2 (cobertura):** a bancada **física** planta 2 dos 4 pedaços (a chamada e o arquivo); o
`OpenWindow` e a linha de boot só são plantados **em memória**. É aceitável (a bancada física é o custo
alto), mas quem ler o docstring *"PLANTA de volta, UM POR VEZ, cada pedaco"* pode achar que são 4.

## 5. Não-enfraquecimento dos testes — **OK (nenhum critério de superfície VIVA ficou mais fraco)**

"Antes" obtido de duas formas: `git show HEAD:<arquivo>` para os rastreados, e para a família
**rstv28** (não rastreada — `??`) a cópia **pré-RSTV-29** deixada pelo autor em
`C:/Users/Pichau/AppData/Local/Temp/rstv28-sandbox/tools/testes/`, cujo
`prova-sandbox-rstv28.py` tem sha `3454825a447a…` — **exatamente o sha registrado** na revisão
RSTV-28R (`docs/cobertura/revisao/RSTV-28R-revisao.md` l.18), o que prova que aquela cópia é o estado
original e não uma sobra ambígua.

| teste/regra | o que travava ANTES | o que trava AGORA | critério perdido? |
|---|---|---|---|
| `t_rstv28_tela_select_party.py` | **existência** da injeção: 2 ganchos da tela chamando `SelectPartyButton.Ensure`, `Mirror` reinjetando, modelo do `motivo=desconhecido` | **ausência** da superfície: arquivo/classe, 2 ganchos da tela, textos do config/boot + controle positivo do botão do modal | só o que a decisão do dono removeu (a injeção). **Justificado.** |
| `regras_rstv28.py` | `falhas_dos_ganchos`, `falhas_do_mirror`, `injeta_ao_abrir`, `motivo_do_diagnostico`, `patches_sem_gancho_janela`, `botao_sem_reinjecao` | `falhas_da_ausencia` + 4 plantios | idem (tudo da feature removida). |
| `regras_rstv12.py` | helper em `SelectPartyButton`, 3 clones limpando o onClick (`RunButton`, `LevelUpWindowButton`, `SelectPartyButton`), classe-de-defeito fechada, modelo do `UnityEvent` | helper em `NativeUiHelpers`, **2** clones (run + level-up), classe-de-defeito fechada, **mesmo** modelo do `UnityEvent` | perdeu **só** o clone da tela de party (classe apagada). Os 2 clones que FICAM continuam presos, incluindo "limpa ANTES de instalar o listener". **Justificado.** |
| `regras_rstv11b.py` / `t_rstv11b…py` | `SelectPartyButton.ClearClickListeners(button)` | `NativeUiHelpers.ClearClickListeners(button)` | nenhum — rename, mesma asserção (troca de INSTÂNCIA do evento, proibição de `RemoveAllListeners()`). |
| `regras_rstv16.py` | citação de `SelectPartyButton.ClearClickListeners` | citação de `NativeUiHelpers.ClearClickListeners` | nenhum — rename em comentário/doc. |
| `cp_rstv12_clique_no_original.py` | planta `limpeza antiga` nos 2 clones + `helper antigo` em `SelectPartyButton.cs` | idem, com `NativeUiHelpers.cs` | nenhum. |
| `prova-sandbox-rstv28.py` | 3 plantas físicas (gancho removido; `Mirror` sem reinjeção; os dois) | 2 plantas físicas (chamada de volta; arquivo/classe de volta) | **menos casos físicos**, mas o alvo mudou: não há mais "gancho sem Ensure"/"Mirror sem reinjeção" para plantar (o código saiu). O conjunto de 4 plantas em memória cobre o resto. Aceito. |
| `t_rstv11_atalho_f10.py` / `regras_rstv11.py` | ramo da tela de party do atalho (fonte vivo + ordem) | **inalterados** (não estão na lista de modificados) | nenhum — e continuam verdes, o que é a prova de que o F10 de party não regrediu. |

Nenhuma **trava** (`tools/check_*.py`) foi afrouxada: os diffs de `tools/check_padroes_segredo.py` e
`tools/check_segredos.py` são de **outra** frente (não tocam RSTV-28/29) e os 4 checks pedidos seguem
`exit 0` (item 7). Nenhum critério que protegia superfície **viva** passou a proteger menos.

## 6. Docs — **OK**

- `README.md` (l.14-28, e a seção PT-BR l.104-114): o botão da tela *Select Party* é descrito como
  **removido na RSTV-29**, e o texto lista só modal + HUD da run + atalho F10. Nada afirma que existe
  botão na tela de party.
- `CHANGELOG.md` (l.3-28): seção **"Não publicado (RSTV-29)"** com a decisão do dono, o que saiu e o
  que ficou. As menções ao botão da tela de party em l.251/267/270/279 estão dentro de
  `## 0.2.0` (l.194-262) → **histórico**, correto preservar.
- `RoguelikeSkillTreeVisualizer.csproj` (l.15) e `manifest.json` (`description`): reescritos sem citar
  a tela de party; só descrevem modal + HUD + atalho.
- `KANBAN.md` (l.312-322): a RSTV-29 registra a remoção e o que fica. Sem contradição com o que ficou.
- **Versão:** `csproj <Version>0.3.2` = `manifest.json version_number 0.3.2` = `Plugin.cs const Version
  "0.3.2"` = `README.md - **Version:** 0.3.2` → **0.3.2, sem bump indevido** (`tools/check_versoes.py`
  exit 0, "os 6 mods batem nos quatro lugares").
**ACHADO D (média) — `docs/CONFERENCIA-DONO-06-10.md:45` ainda manda o dono olhar o botão removido.**
*"Na tela de escolha de party do roguelike, o botão quadrado `Skills` fica à direita do `Choose Powerups`."*
É o **roteiro de conferência humana** que o dono usa em jogo: ele vai abrir a tela de party, **não** achar o
botão e registrar "falhou". Contradiz a decisão de 06/10 e queima a rodada de validação (o DoD exige
verificação humana em jogo). Correção sugerida: reescrever a seção 2 para a superfície que **ficou** (o
botão do **modal Remove Skill Trees**, aberto a partir dessa tela) e/ou marcar que o F10 atende a tela. Doc
— merece cartão próprio; o revisor não edita.

**ACHADO E (baixa) — `docs/README.md:386` descreve o mod pelo botão removido.**
*"`RoguelikeSkillTreeVisualizer` | Botão ao lado de *Choose Powerups* … | 0.2.0 …"*. Tabela-inventário do
repo; o `git diff` desse arquivo **não** tem linha de RSTV/party (a RSTV-29 não o tocou). A versão ali
(`0.2.0`) é desatualização pré-existente, não causada pela RSTV-29. Correção sugerida: atualizar a descrição
para modal+HUD e a coluna de versão. Não vai no pacote.

- **Observação 3 (fora do escopo, mas registrada):** `dist/gumatos-RoguelikeSkillTreeVisualizer-0.3.2.zip`
  é de **04/10 02:15**, anterior a esta mudança — a fonte de 0.3.2 já **divergiu** do zip publicado. O
  CHANGELOG marca o RSTV-29 como não publicado, então nada foi publicado errado; mas empacotar de novo
  sob 0.3.2 mudaria silenciosamente um artefato publicado (o mesmo risco do REL-1 que a NULL-1 já
  levantou). Decisão de bump/publicação é do dono, não desta revisão.

## 7. Build / suíte / travas — reproduzido por execução — **OK**

```
$ dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj -p:DeployToBepInEx=false
  RoguelikeSkillTreeVisualizer -> …\bin\Debug\netstandard2.1\RoguelikeSkillTreeVisualizer.dll
  Compilação com êxito.   1 Aviso(s)   0 Erro(s)   EXIT=0
  (o aviso é o MSB3277 de System.Net.Http — pré-existente, não relacionado)
```

```
$ python tools/testes/roda_testes.py --puros
  rodaram: 91 | passaram: 91 | reprovaram: 0 | nao rodaram: 0
  EXCLUIDOS por categoria (1): jogo=1
  VEREDITO: VERDE (exit 0)
```

Travas (todas `exit 0`, lendo o estado resultante e não a mensagem):

- `tools/check_versoes.py` → "os 6 mods batem nos quatro lugares (csproj = manifest = Plugin.cs = README)".
- `tools/check_patches.py` → `0 achado(s) que REPROVAM | 2 aviso(s)`; `51/51` classes de patch com
  assinatura por TIPO; `51/52` métodos protegidos; `7/7` `Plugin.cs` com marcador de vida.
- `tools/check_dupes.py` → nenhuma duplicada (TextFixes 101, TextAppends 197).
- `tools/check_dependencias.py` → "todas as dependencias resolvem".
- `trava-artefato-fonte` (teste puro) → PASSOU. (Ela constrói o próprio plantio; **não** compara a
  Release do repo com a fonte. Estado real do disco: `bin/Release/…dll` mtime 15:08:11 vs `Patches.cs`
  18:18 — a Release está **velha em relação à fonte**, o que é esperado enquanto o RSTV-29 não é
  empacotado, e é exatamente o risco do item 6/Observação 3.)

## 8. Perfil, publicação, commit, `Assembly-CSharp.dll` — **OK**

- **Nada instalado.** A DLL do perfil é **byte-idêntica** à `bin/Release` do repo e **anterior** à
  mudança: `40e620e6108299cc15d3f50064b5264bc2d6e6e79b5c0d095f50d40ce9114da2` (perfil) =
  `40e620e6108299cc…` (repo), mtime `2026-10-06 15:08:11` (= o build da RSTV-28). Ou seja, o jogo do
  dono **ainda tem o botão antigo** até um deploy explícito (`-p:DeployToBepInEx=true`), como manda o
  fluxo opt-in.
- **Nada publicado.** `dist/` não tem zip novo: o mais recente do RSTV é `…-0.3.2.zip` de **04/10
  02:15** (anterior a esta mudança).
- **Nada commitado:** `git log -1` = `34f929a` (inalterado), `git diff --cached` vazio, as modificações
  estão todas em *working tree* e a deleção do `SelectPartyButton.cs` está **não-staged**.
- **`Assembly-CSharp.dll` intocado:** `E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm_Data\
  Managed\Assembly-CSharp.dll`, mtime `2026-09-12 21:34:42`,
  sha256 `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` — data de instalação do jogo.
- Nada foi rodado em jogo, nenhum token/PAT foi lido ou escrito, nenhuma tarefa do Kanban foi criada
  ou mutada por mim.

## Veredito por item

| # | item | veredito |
|---|---|---|
| 1 | Ausência real da superfície no código efetivo | **OK** (grep literal + `Ensure/Mirror`/ganchos/DIF) |
| 2 | `AtivarBotao` como chave-mestra | **OK** — matriz completa, nenhum caminho impossível — com **ACHADO A** (mudança de comportamento para `.cfg` existente com `false`) e **ACHADO B** (motivo do log mente quando a mestra desliga) |
| 3 | Gancho `OpenWindow` removido sem dependentes; F10 de party intacto | **OK** (dependência viva = `PartyTargets`/`ReadOnlyContext.PartyScreen`; presa por `rstv16-aba-arvores` **e** por `rstv11-atalho-f10` — o nome no cartão está correto) |
| 4 | A checagem de ausência é real e reprova o vermelho | **OK** (rodado por mim, exit 0; fonte ao vivo; comentário não conta; código conta) com **ACHADO C** (gancho em forma de string + classe de nome neutro passa batido) |
| 5 | Não-enfraquecimento de `rstv11b/12/16/28` | **OK** — só perdeu critério sobre a feature removida; nada de superfície viva perdeu proteção; nenhum teste deletado |
| 6 | Docs coerentes, versão 0.3.2 sem bump | **OK** para os 5 arquivos do item; **ACHADO D** e **ACHADO E** (docs fora da lista que ainda apontam o botão removido) |
| 7 | Build / suíte / travas reproduzidos | **OK** (exit 0 em tudo) |
| 8 | Perfil/modificações/publicação/commit/`Assembly-CSharp.dll` | **OK** |

**Veredito geral: APROVADO COM ACHADOS.** São **5 achados que não bloqueiam** — 1 de comportamento
documentado (A), 1 de diagnóstico (B), 1 furo de cobertura do teste (C) e 2 **documentais** (D, E — sendo D
o mais relevante por mirar a rodada de validação do dono) — mais as observações de estado.

**INDETERMINADO / NÃO EXERCITADO (declarado, não é verde):** o comportamento **em jogo** (a tela de
party de fato sem botão, o F10 de party abrindo a árvore, o modal e o HUD seguindo ligados) exige rodar
o jogo no deploy do dono — fora das regras desta revisão. O que esta revisão prova é fonte, testes,
build, travas e estado do disco.

### Achados, em uma linha cada (para virar cartão, se o dono quiser)

- **A** — `AtivarBotao=false` (chave-mestra) agora também desliga o HUD da run, o botão do level-up e o
  modal, mudando o efeito de um `.cfg` que já existia; deliberado e documentado, sem efeito no perfil do
  dono (`true`). `Plugin.cs:103-124`.
- **B** — com a mestra `false`, o log diz `"AtivarBotaoNaRun=false"`/`"AtivarBotaoNaRemocao=false"` sem
  que a específica esteja `false`: `RunButton.cs:96,219`, `LevelUpWindowButton.cs:89`,
  `RemovalWindowSkillsButton.cs:106`.
- **C** — `regras_rstv28.falhas_da_ausencia` não vê gancho em **forma de string** com classe de nome
  neutro (medido por sonda própria); o teste prende a ausência por *nome* + `nameof(...)`, não pela
  propriedade "nenhum patch aponta para a tela". `tools/testes/regras_rstv28.py:106-111`.
- **D** — `docs/CONFERENCIA-DONO-06-10.md:45` manda o dono procurar o botão `Skills` "à direita do
  `Choose Powerups`" na tela de party (que não existe mais): é o roteiro de validação humana, agora
  mentiroso. Correção sugerida: descrever a superfície que ficou (botão do modal) e/ou o F10.
- **E** — `docs/README.md:386` descreve o mod como "Botão ao lado de *Choose Powerups*" (e versão 0.2.0):
  tabela-inventário do repo que a RSTV-29 não atualizou.
