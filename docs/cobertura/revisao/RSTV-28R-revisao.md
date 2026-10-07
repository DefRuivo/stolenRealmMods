# RSTV-28R — Revisão independente do conserto do botão 'Skills' na tela Select Party

Revisor != autor. Leitura somente; nenhuma escrita no repo além deste arquivo. Sem jogo, sem deploy, sem instalação, sem commit, sem publicação, sem tocar em `lib/Assembly-CSharp.dll`, sem editar fonte do mod nem `tools/testes/*rstv28*`, sem tocar em `tools/automacao/**`. Nada aqui fecha cartão, publica ou commita — a **verificação humana em jogo do dono** e a **publicação** seguem como gates pendentes.

- Data da revisão: 06/10/2026 (UTC-03:00).
- Repo: `C:/dev/stolen-realm` (branch `ci-validate-test`, HEAD `f526fe9b71f5e7b946c1e699612cb1e9a3a08810`).
- Cartão: `t_af84b22e` (RSTV-28, status `ready`) — lido via `hermes kanban show t_af84b22e`.
- Ferramentas usadas: `sha256sum`, `grep -n`, `stat`, `python tools/testes/roda_testes.py`, a bancada de sandbox do autor, um **probe de sabotagem próprio** (fora do repo) e `ilspycmd` sobre a **DLL real** `lib/Assembly-CSharp.dll` (decompilado por tipo e assembly inteira) e sobre a **nossa Release**.
- O dump cacheado citado (`.../cache/scratch/cs/Assembly-CSharp.decompiled.cs`) **não existe mais** (podado). Regenerei tudo por símbolo com `ilspycmd` — inclusive os números de linha, que batem com o citado no código (ver §3.0).

## 0. Hashes lidos (sha256) — antes E depois (não mudei nada)

| Arquivo | sha256 |
|---|---|
| `RoguelikeSkillTreeVisualizer/Patches.cs` | `38d60f278f353b9aea56e78d44e9310eb2d8c13587730a7f17b0bf9c6efbeed1` |
| `RoguelikeSkillTreeVisualizer/SelectPartyButton.cs` | `1b23b43e4b2da44bc4d19b9c32238f1e83d0b8e5768515ec936d405e7b682191` |
| `tools/testes/regras_rstv28.py` | `03de80e07c9e3e5fb86b1a913ce1b3ab7e154bfb33ba831af5bf8e9552b0aba0` |
| `tools/testes/prova-sandbox-rstv28.py` | `3454825a447a77a4452856bf6c165535470480245d904057e3d9b47fc8d74e80` |
| `tools/testes/testes/puros/t_rstv28_tela_select_party.py` | `bb447d8f89dd55b581aaa4d919844ac59b49b7e9403c591bc59dbef4e7f9bbf5` |
| `tools/testes/rstv28-prova-reprovando.log` | `39413959d382f0f859ddbdd534c6c42e1175085a913f9d3903e2dd3c849a032b` |
| `tools/testes/arcabouco.py` | `08b4dd51c1d2bd851cf0d5d2b2f038dbe3f1094ab4c625ed63a7a4dc97c20afb` |
| `lib/Assembly-CSharp.dll` | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |
| `RoguelikeSkillTreeVisualizer/bin/Release/netstandard2.1/RoguelikeSkillTreeVisualizer.dll` | `40e620e6108299cc15d3f50064b5264bc2d6e6e79b5c0d095f50d40ce9114da2` |

Os sha256 medidos **no fim da revisão batem byte a byte com os do início** → o revisor não tocou em nada. `git status --porcelain` dos arquivos lidos não mudou.

---

## 1. O que foi reproduzido por execução própria

### 1.1 Bancada do autor — `python tools/testes/prova-sandbox-rstv28.py` → **exit 0**

Saída literal (trecho fiel; linhas longas cortadas):

```
RSTV-28 - CONTRA-PROVA EM SANDBOX FORA DO REPO
repo (NAO e' tocado): C:\dev\stolen-realm
sandbox:              C:\Users\Pichau\AppData\Local\Temp\rstv28-sandbox
teste:                tools/testes/testes/puros/t_rstv28_tela_select_party.py

[FONTE DE VERDADE] a copia do conserto, no sandbox
  Patches.cs           sha256 38d60f278f353b9aea56e78d44e9310eb2d8c13587730a7f17b0bf9c6efbeed1
  SelectPartyButton.cs sha256 1b23b43e4b2da44bc4d19b9c32238f1e83d0b8e5768515ec936d405e7b682191
  [sem defeito] exit=0 (esperado 0)
      [PASSOU ] rstv28-tela-select-party RSTV-28: o botao 'Skills' e' injetado na tela Select Party em TODA via de abertura ...

  [(a) Patches.cs SEM o gancho de OpenWindow (a causa da RSTV-28)] exit=1 (esperado 1)
      [REPROVOU] rstv28-tela-select-party o injetor da tela Select Party nao cobre toda abertura (1 ponto(s)): Patches.cs NAO tem gancho em `CharacterChoiceManager.OpenWindow` ...
      restaurado byte a byte: True (38d60f278f353b9a)

  [(b) SelectPartyButton.cs SEM a reinjecao do Mirror] exit=1 (esperado 1)
      [REPROVOU] rstv28-tela-select-party o `Mirror` nao se recupera do botao ausente (1 ponto(s)): o ramo `_button == null` do `Mirror` NAO tenta reinjetar (`Ensure(manager)`) ...
      restaurado byte a byte: True (1b23b43e4b2da44b)

  [(c) ESTADO ANTERIOR COMPLETO (os 2 defeitos juntos)] exit=1 (esperado 1)
      [REPROVOU] rstv28-tela-select-party o injetor da tela Select Party nao cobre toda abertura (1 ponto(s)): Patches.cs NAO tem gancho em `CharacterChoiceManager.OpenWindow` ...
      restaurado byte a byte: True

[REPO INTACTO] True
  38d60f278f353b9a RoguelikeSkillTreeVisualizer/Patches.cs
  1b23b43e4b2da44b RoguelikeSkillTreeVisualizer/SelectPartyButton.cs

VEREDITO: PROVA OK - sem defeito PASSA (exit 0); os 3 defeitos plantados REPROVAM (exit 1), inclusive o ESTADO ANTERIOR completo; cada um restaurado byte a byte; o repo nao foi tocado.
EXIT=0
```

Conferido: a bancada **realmente planta** os 3 casos (a) `Patches.cs` sem o gancho de `OpenWindow`, (b) `SelectPartyButton.cs` sem a reinjecão, (c) os dois juntos. Em todos deu `exit=1`, com **restauração byte a byte** confirmada e `[REPO INTACTO] True`. O log versionado `tools/testes/rstv28-prova-reprovando.log` (sha `3941…`) é **fiel**: reproduzi e a saída é idêntica.

### 1.2 A isca — o teste MORDE mesmo? (probe de sabotagem próprio, fora do repo)

Suspeita legítima: "bancada que passa nos dois lados = decoração". Provei o contrário com um probe independente (`…/cache/scratch/rstv28-probe-revisor.py`) que **golpeia** o fonte vivo em memória e mede se as regras reprovam. Resultado literal:

```
{'OpenCharacterChoiceManager': True, 'OpenWindow': True, 'ToggleSelectedCharacter': False}   # fonte vivo
mirror_reinjecta: True ; falhas_dos_ganchos: [] ; falhas_do_mirror: []

(a) removido: hooks DEPOIS = [('OpenCharacterChoiceManager', True), ('ToggleSelectedCharacter', False)]  -> falha no OpenWindow
(b) removido: 'Ensure(manager);' no fonte vivo = 1 ocorrencia; bloco _button==null ainda contem? False   -> falha no Mirror
a1: gancho existe mas SEM SelectPartyButton.Ensure -> falha OCM
a2: nameof trocado por metodo inexistente          -> falha OpenWindow
a3: classe do gancho antigo removida               -> falha OCM
b1: 'Ensure(manager);' -> 'NaoReinjeta(manager);'  -> falha Mirror
extra: gancho OpenWindow SEM Ensure                -> falha "o gancho de `CharacterChoiceManager.OpenWindow` existe mas NAO chama `SelectPartyButton.Ensure(__instance)`"
```

**O plantio (a) remove SÓ a classe nova** (27 linhas, do `[HarmonyPatch…OpenWindow` ao fim do bloco de classe), deixando o gancho antigo e o `ToggleSelectedCharacter` intactos. **O plantio (b) remove a única ocorrência** de `Ensure(manager);` do fonte (grep: 1 só), e ela vive dentro do bloco `_button == null` do `Mirror`. Todas as sabotagens reprovam pelo motivo certo → **o teste não é isca**.

### 1.3 Teste da suíte, rodado direto

- Invocação **ingênua** (`python tools/testes/testes/puros/t_rstv28_tela_select_party.py`) → **exit 1**
  `ModuleNotFoundError: No module named 'regras_rstv28'` (o teste importa `regras_rstv28`/`arcabouco`, que moram em `tools/testes/`, e o caminho só entra via `PYTHONPATH`).
- Invocação **como o runner faz** (é o que `arcabouco.executar_arquivo` monta: `PYTHONPATH=<tools/testes>`, `PYTHONIOENCODING=utf-8`):
  `PYTHONPATH="C:/dev/stolen-realm/tools/testes" python tools/testes/testes/puros/t_rstv28_tela_select_party.py` → **exit 0**
  `RESULTADO|PASSOU|rstv28-tela-select-party|RSTV-28: o botao 'Skills' e' injetado …`
- Pelo runner, focado: `python tools/testes/roda_testes.py --teste tools/testes/testes/puros/t_rstv28_tela_select_party.py` → **VERDE, exit 0** (1 rodou / 1 passou).
- Suíte pura inteira: `python tools/testes/roda_testes.py --puros` → **exit 0**, `rodaram: 89 / passaram: 89 / reprovaram: 0`, `rstv28-tela-select-party` consta PASSOU.

*(O exit code "cru" do arquivo, sem o `PYTHONPATH` do runner, é 1 — não é defeito do teste: é o mesmo contrato de todos os testes da pasta, que importam `arcabouco`/`regras_*` por nome. O runner é quem injeta o caminho.)*

---

## 2. Refutação da causa e do conserto — por **símbolo** (não por linha)

### 2.0 Os números de linha citados são reais
O dump citado não existe mais, mas regenerando a **assembly inteira** (`ilspycmd lib/Assembly-CSharp.dll > FULL.cs`, 496.228 linhas) as linhas citadas batem **exatamente**: `l.120027` = `if (value == GUIState.ChoosingCharacter && CharacterChoiceManager.Instance == null)`, `l.120035` = `CharacterChoiceManager.Instance.OpenWindow();`, `l.139831` = `public void InitPlayer(byte networkID, bool loadingSavedGame, bool hasCharactersAlreadyInParty = false)`, `l.139883` = `GUIManager.instance.CurrentGuiState = (… ? GUIState.CreatingCharacter : GUIState.ChoosingCharacter);`, `l.329032` = `public override void OpenWindow()` (o do `CharacterChoiceManager`). Única discrepância: `OpenCharacterChoiceManager` está em **l.328695** no meu dump (citado `l.328703`, off-by-8 — diferença de versão do decompilador). **A numeração do autor é a de um dump real da mesma DLL.**

### 2.1 A causa alegada está CONFIRMADA por símbolo → **OK**
- `CharacterChoiceManager : UIWindow` (l.9 do tipo). `OpenCharacterChoiceManager()` (l.193 do tipo) faz `GUIManager.instance.CurrentGuiState = GUIState.ChoosingCharacter;` (l.195) — e o **setter** de `CurrentGuiState` é quem chama `CharacterChoiceManager.Instance.OpenWindow()` (l.120035).
- O override `CharacterChoiceManager.OpenWindow()` (l.530 do tipo): `base.OpenWindow(); base.gameObject.SetActive(value: true); ControlFooter.instance.Show();` — **NÃO** chama `OpenCharacterChoiceManager`.
- `MainMenu.InitPlayer` (l.139831) põe `GUIState.ChoosingCharacter` (l.139883) quando `AllMyCharacters.Count == 0` — o caminho do "Continue".
- O enunciado diz "`OpenCharacterChoiceManager` chegava ao `OpenWindow` via setter": **procede** — mas justamente porque `OpenCharacterChoiceManager` passa pelo setter, ele também chega ao `OpenWindow`. Logo ancorar em `OpenWindow` é o ponto comum. ✅

### 2.2 Existe OUTRO caminho de abertura sem gancho? → **OK** (com 1 ressalva INDETERMINADA)
Varredura de **toda** a assembly:
- **Todos** os chamadores de `OpenCharacterChoiceManager` (`FULL.cs` l.98184, 120972, 330405 via `Instance`; 156587, 169136, 332588 via `ForcedInstance` — que é `=> Instance`, l.328574; 184089, 232956, 263291) chamam **o mesmo método**, que passa pelo setter → `OpenWindow`. Cobertos pelos dois ganchos.
- **Único** chamador direto de `CharacterChoiceManager.Instance.OpenWindow()` é o próprio setter (l.120035). Coberto.
- **Nenhum** `CharacterChoiceManager.*.gameObject.SetActive(true)` em nenhum lugar (o único `SetActive` na instância é `inputBlocker.SetActive(false)`, l.149850 — não é abertura).
- `GUIManager.CurrentGuiState = GUIState.ChoosingCharacter` aparece também em l.47965 e l.110806 → todos passam pelo setter → `OpenWindow`. `FadeToCharacterSelect` (l.1559) usa `ShowLoadingScreen(..., GUIState.ChoosingCharacter)` → setter. Cobertos.
- `ResetCharacterChoice()` (chamado **depois** do `OpenWindow` no setter, l.638) só faz `RefreshCharacters()` + `AcceptedParty = false` — **não** destrói nem recria o botão. O clone sobrevive à abertura. ✅

**Ressalva (INDETERMINADO):** eventos Unity serializados no **prefab** (um botão/`m_OnClick` chamando `OpenCharacterChoiceManager` ou `OpenWindow` direto) não dá para enumerar sem abrir o jogo/prefab — mas ambos os métodos-alvo estão ganchados, então um clique de prefab nesses métodos também é coberto; só um `GameObject.SetActive(true)` cru por UnityEvent escaparia, e para isso há a rede do `Mirror`.

### 2.3 A assinatura Harmony está correta? → **OK**
Fonte: `[HarmonyPatch(typeof(CharacterChoiceManager), nameof(CharacterChoiceManager.OpenWindow), new Type[0])]` com `[HarmonyPostfix] private static void Postfix(CharacterChoiceManager __instance)` — **tipo explícito + nome + array de tipos vazio** (nada por índice `__N`). O método real é `public override void OpenWindow()` **sem parâmetros** → casa.
Confirmado **na DLL Release compilada** (não só na fonte): `ilspycmd -t RoguelikeSkillTreeVisualizer.CharacterChoiceOpenWindowPatch bin/Release/netstandard2.1/RoguelikeSkillTreeVisualizer.dll` devolve
`[HarmonyPatch(typeof(CharacterChoiceManager), "OpenWindow", new Type[] { })]` + `Postfix(CharacterChoiceManager __instance)` chamando `RstvHost.Ensure(); SelectPartyButton.Ensure(__instance);`. Idêntico à fonte.

### 2.4 Idempotência e risco de laço → **OK**
- `SelectPartyButton.Ensure` sai cedo com `if (_owner == manager && _button != null) return;` e, além disso, reusa o filho por nome (`parent.Find(ButtonName)`) — não cria um segundo botão. `RstvHost.Ensure` é singleton. Chamar duas vezes (gancho antigo + novo) é **no-op**. ✅
- `Mirror`, no ramo `_button == null`, **não faz laço**: é limitado por `_triedFor == manager && Time.realtimeSinceStartup < _proximaTentativa` (1 tentativa a cada `IntervaloDeReinjecao = 2f`). No máximo **uma** reinserção por instância a cada 2 s. `Fail` só loga quando o motivo muda. ✅ (Presente na Release: `_proximaTentativa`, `IntervaloDeReinjecao = 2f`, `Time.realtimeSinceStartup + 2f`.)

### 2.5 O teto de 2 s pode deixar a tela sem botão por 2 s? → **ACHADO** (comportamento; impacto em jogo INDETERMINADO)
**Sim, pode** — de forma limitada e de baixa probabilidade: se a **primeira** tentativa de injeção falhar (ex.: `roguelikePowerupButton` ainda nulo no instante do gancho), o `Mirror` só tenta de novo após 2 s. No caminho normal o botão entra **na hora** (o postfix de `OpenWindow` chama `Ensure` na abertura; na sessão real o botão nativo estava "presente", então `Ensure` converge). O atraso de até 2 s só ocorre se `Ensure` **falhar** na abertura e a condição só se resolver depois. **Não é laço nem travamento**, mas é uma janela de até 2 s sem botão que só a verificação em jogo mede. → **ACHADO (menor)**, impacto **INDETERMINADO sem jogo**.

### 2.6 O gancho novo pode disparar antes do clone e o diagnóstico seguir "desconhecido"? → **OK**
`_reason` é gravado por **todo** caminho de falha (`Fail`) e zerado no sucesso (`_reason = null`). Logo `motivo=desconhecido` (que é `_reason != null ? _reason : "desconhecido"`, `SelectPartyButton.DumpDiagnosis`) só aparece quando **`Ensure` nunca rodou**. Com o gancho em `OpenWindow`, o `Ensure` roda em **toda** abertura; se o botão nativo ainda não existe, `Fail("o botao nativo … nao existe nesta tela")` grava um motivo **real** → o diagnóstico mostra o motivo real, não "desconhecido". ✅ Consistente com a linha real do log (`motivo=desconhecido` ⇔ injetor nunca chamado). *(Só observa-se "desconhecido" de novo se o `Ensure` jamais rodar nesse caminho — o que o conserto elimina.)*

---

## 3. Suíte e build

- **Suíte pura** (`--puros`): `89/89`, `VEREDITO: VERDE (exit 0)`.
- **Compilação:** não rodei `dotnet build` (para não mexer em `obj/`/`bin/` do repo). A prova é o **artefato**: a Release `RoguelikeSkillTreeVisualizer.dll` (sha `40e620e6…`) tem mtime **`2026-10-06 15:08:11`**, **posterior** a `Patches.cs` (`15:05:21`) e `SelectPartyButton.cs` (`15:08:05`) → satisfaz a trava artefato×fonte. Decompilei **da própria Release** a classe `CharacterChoiceOpenWindowPatch` e o `Mirror` do `SelectPartyButton` — o código compilado é **idêntico à fonte** (assinatura por tipo+nome, `Ensure`, teto de 2 s, `_proximaTentativa`). Ou seja, a Release **corresponde** ao conserto.
- **Ressalva:** não há log literal do `dotnet build` no disco (evidência = artefato decompilado). Se o critério exigir o log da compilação, este item vira NAO_EXERCITADO quanto ao log.

---

## 4. O que NÃO dá para verificar sem jogo (marcado honestamente)

- **INDETERMINADO / NAO_EXERCITADO:** o **log real sem o aviso `RSTV DIAG` na cena reproduzida** (abrir a tela pelo "Continue" e conferir a ausência da linha `motivo=desconhecido`). Exige abrir o jogo e carregar save — **não exercitado nesta revisão** (por instrução). O que se prova aqui é o **modelo** (a via `OpenWindow` passa a injetar) e a **cobertura de código**; o comportamento em runtime com Harmony/`fake null`/prefab é gate do dono.
- **INDETERMINADO:** se o `prefab` dispara alguma abertura por UnityEvent (ver §2.2) e se o teto de 2 s (§2.5) chega a morder em uso real.
- **NAO_EXERCITADO:** log literal do `dotnet build` (§3).
- **Não fiz:** instalar, publicar, commitar, `git add`, abrir o jogo, mexer no Kanban, alterar fonte do mod, `lib/Assembly-CSharp.dll` ou `tools/automacao/**`.

---

## 5. Veredito por item

| Item | Veredito |
|---|---|
| Reproduzir a bancada (sem defeito passa; 3 defeitos reprovam; restore byte a byte; repo intacto) | **OK** (exit 0 literal) |
| A bancada é isca que passa nos dois lados? | **OK** — não é isca (probe de sabotagem próprio: a1/a2/a3/b1 + OpenWindow-sem-Ensure reprovam) |
| Teste da suíte rodado direto — exit code real | **OK** (runner: exit 0; ingênuo: exit 1 por import, declarado) |
| Causa `OpenWindow` (por símbolo, não por linha) | **OK** (confirmada; linhas citadas batem no dump regenerado) |
| Existe outro caminho de abertura sem gancho? | **OK** (nenhum encontrado; ressalva de prefab/UnityEvent = INDETERMINADO) |
| Assinatura Harmony (tipo explícito, sem posicional) | **OK** (confirmada também na DLL Release) |
| Idempotência / risco de laço de reinjecão | **OK** |
| `motivo=desconhecido` eliminado pelo gancho novo | **OK** (por código/modelo) |
| Teto de 2 s pode deixar a tela sem botão por 2 s | **ACHADO (menor)** — pode, de forma limitada; impacto real **INDETERMINADO** sem jogo |
| Compilação (artefato Release corresponde à fonte) | **OK**; log de build literal **NAO_EXERCITADO** |
| Log real sem o aviso `RSTV DIAG` na cena reproduzida | **INDETERMINADO / NAO_EXERCITADO** (precisa do jogo) |

---

## 6. O que falta (lista exata)

1. **Verificação humana em jogo do dono** (gate): abrir a tela Select Party pelo **"Continue"** (carregar save sem ninguém na party) e conferir no `LogOutput.log`: (a) a linha `RSTV-28: gancho do 'OpenWindow' da tela Select Party ATIVO …` e (b) a **ausência** de `RSTV DIAG: a tela Select Party esta aberta e o botao 'Skills' NAO foi injetado … motivo=desconhecido`. Repetir abrindo a tela várias vezes / trocando party.
2. **Publicação** na Thunderstore (gate; a versão publicada é imutável) — não é desta revisão.
3. **Confrontar §2.5 em jogo** (o teto de 2 s chega a morder?):
4. Nada pendente do lado do revisor: hashes conferidos antes/depois, bancada e suíte reproduzidas, causa refutada por símbolo.

*Sem fechamento de tarefa, sem publicação, sem instalação, sem commit, sem alteração de cartão do kanban, sem tocar em `lib/Assembly-CSharp.dll`.*
