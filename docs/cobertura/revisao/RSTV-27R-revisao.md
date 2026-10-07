# RSTV-27R — Revisão independente do conserto do RODAPÉ da tooltip read-only

Revisor != autor. Leitura somente; nenhuma escrita no repo além deste arquivo. Sem jogo, sem deploy, sem commit, sem publicação, sem tocar em `Assembly-CSharp.dll`. Nada aqui fecha cartão, publica, instala ou commita — a **verificação humana em jogo do dono** e a **publicação** seguem como gates pendentes.

- Data da revisão: 06/10/2026 (UTC-03:00).
- Repo: `C:/dev/stolen-realm`.
- Ferramentas usadas: `sha256sum`, `grep -n`, `python tools/testes/roda_testes.py`, as duas bancadas de sandbox, e `ilspycmd` sobre a **DLL real** `lib/Assembly-CSharp.dll` (IL) e sobre a nossa Release.
- PROVA DO JOGO: medida por `ilspycmd -il` na `lib/Assembly-CSharp.dll` (não por leitura de arquivo decompilado alheio).

## 0. Hashes lidos (sha256)

| Arquivo | sha256 |
|---|---|
| `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs` | `ecb75898ba136e9ab13eda9113694153ad6a9703fd0dcf0cf2e08d36b9d53624` |
| `RoguelikeSkillTreeVisualizer/Patches.cs` | `5f0d27f62e0aa0e9a3f5e0b5072c1665a91871c6220c45cf3d0bd64b00455b49` |
| `tools/testes/regras_rstv27.py` | `756156f3f237466883adce874d568465c2464a082674bb29a8b47491923adceb` |
| `tools/testes/regras_rstv27_valor.py` | `6286399ab5e3129c56d0f7fd060abfa08408bccff36014bc916a0fc2e0f9ddc3` |
| `tools/testes/testes/puros/t_rstv27_rodape_personagem.py` | `72826f5f7e27ff7d75f9ed5bc0ff3dce289e57f3ba37011f5a2ce2b9a97cde54` |
| `tools/testes/testes/puros/t_rstv27_rodape_valor.py` | `d93efcabeff16891df665136120e53939dabc0a794de3f1ea38950b4432027c9` |
| `tools/testes/prova-sandbox-rstv27.py` | `3735b392b241a0f1cd338b6fda3b3bb95af4e5e859ce73f4c0dceb2903b8e5ac` |
| `tools/testes/prova-sandbox-rstv27-valor.py` | `ab03de7b5941c947df7e69eec5389ce334669b35253b2c6e522a643045a65469` |
| `tools/testes/rstv27-rodape-prova-reprovando.log` | `d7ffe5e4a103a8ea3cabc51804356765003a5085673c682d58387dca40b8490b` |
| `tools/testes/rstv27-valor-prova-reprovando.log` | `f4020195bbf12e54b7669a4110b6edd709f423955ff69d8d744c7f16f0dc3338` |
| `tools/testes/fixtures/rstv27-rodape-valor.esperado.json` | `06d5d1be112034c0f39054db702e36d8cefc283d13573a4dc77e35106a8726d2` |
| `tools/testes/fixtures/rstv27-rodape-valor.entrada.json` | `b421f1e079d45e4723e359f407e14fc31506f987790b647a3852cb27d77d4f5d` |
| `RoguelikeSkillTreeVisualizer/bin/Release/netstandard2.1/RoguelikeSkillTreeVisualizer.dll` | `3d684b0847f54b2488dc6f24496be0e26454aca6d8547c3a3df31ddbcce6172b` |
| `lib/Assembly-CSharp.dll` | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |

**Os dois hashes declarados pelo autor BATEM** com o disco (SkillTreesTab.cs e Patches.cs acima).

### ACHADO A1 (documentação desatualizada, não é defeito do conserto)
O caminho de decompilado citado no enunciado/nota, `C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cs/Assembly-CSharp.decompiled.cs` (371.804 linhas), **não existe hoje** nesse disco. O decompilado disponível é por-tipo: `.../cache/scratch/rstv26/dec/Tooltip.decompiled.cs` (sha `7b5bd4c1e6e5cf7f882d65511726e1f600fe43a4c7d1e7c481c3682d1e755cfc`, 2.371 linhas). Para não depender de arquivo alheio, **refiz o IL eu mesmo** com `ilspycmd -il -t Tooltip lib/Assembly-CSharp.dll`. As citações abaixo vêm das duas fontes e batem.

---

## 1. Escopo 1 — perguntas (a)..(f), item por item

### (a) `Tooltip.TooltipCharacter` é GET-ONLY e o rodapé lê esse singleton, não o parâmetro `character` → **OK**

IL real da DLL do jogo (`ilspycmd -il -t Tooltip lib/Assembly-CSharp.dll`), método `get_TooltipCharacter`:

```
.method public hidebysig specialname
    instance class Character get_TooltipCharacter () cil managed
{
    // Code size: 35 (0x23)
    IL_0000: call class GUIManager GUIManager::get_instance()
    IL_0005: callvirt instance valuetype GUIState GUIManager::get_CurrentGuiState()
    IL_000a: ldc.i4.1
    IL_000b: beq.s IL_0018
    IL_000d: call class GameLogic GameLogic::get_instance()
    IL_0012: callvirt instance class Character GameLogic::get_CurrentlySelectedCharacter()
    IL_0017: ret
    IL_0018: call class PresetManager PresetManager::get_Instance()
    IL_001d: callvirt instance class Character PresetManager::get_CreationCharacter()
    IL_0022: ret
} // end of method Tooltip::get_TooltipCharacter
```

- **Não há `set_TooltipCharacter`** em nenhum lugar: a propriedade é **get-only** (só o getter existe no IL). Confere com o decompilado `scratch/rstv26/dec/Tooltip.decompiled.cs`, l.192-202 (só o acessador `get`, que devolve `GameLogic.instance.CurrentlySelectedCharacter`, ou `PresetManager.Instance.CreationCharacter` quando o GUI está em `CreatingCharacter`; na Party Select é o primeiro, **null**).
- O **rodapé lê esse singleton**: `Tooltip.ShowSkillTooltip(SkillInfo skill, Character character, bool showCanLevelDetail, ...)` está na **l.1308** do decompilado (tem o parâmetro `character`). Mas o trecho do rodapé, a partir da **l.1459**, monta um local **próprio** — **l.1472: `tooltipCharacter = TooltipCharacter;`** — e lê TODO o rodapé dele:
  - **l.1473** `num2 = ((tooltipCharacter == null) ? actionInfo2.GetManaCost() : actionInfo2.GetManaCost(tooltipCharacter));`
  - **l.1474** cooldown idem (`GetActionCooldown()` x `GetActionCooldown(tooltipCharacter)`);
  - **l.1478** alcance (`GetSimpleRange(TargetInfo)` x `GetSimpleRange(tooltipCharacter, Targets[0])`);
  - blast (l.~1508) e duração (`Game.Eval` de `Duration`/`GroundDuration`, l.~1533/1540) idem.
  O parâmetro `character` **não é usado** nesse trecho — o IL do call site confirma: em `ShowSkillTooltip` a chamada é `IL_0c46: call instance class Character Tooltip::get_TooltipCharacter()` (bate com o comentário do repo, Patches.cs l.708). Ou seja, o conserto da RSTV-26 (personagem como ARGUMENTO) realmente não alcança o rodapé. **Pergunta (a) confirmada.**

### (b) O postfix preenche o alvo em TODOS os caminhos read-only e NÃO sobrescreve o valor do jogo (zero regressão no inventário) → **OK**

- **Só existe UM caminho read-only que mostra tooltip de skill**: `grep -rn ShowSkillTooltip --include=*.cs RoguelikeSkillTreeVisualizer/` retorna exatamente **duas** linhas, ambas em `RstvSkillHover.OnPointerEnter`:
  - `SkillTreesTab.cs:2172  gui.tooltip.ShowSkillTooltip(Item.SkillInfo, alvo, showCanLevelDetail: false);` — o ramo COM alvo (`ReadOnlySession.Target != null`), que arma o gancho;
  - `SkillTreesTab.cs:2181  gui.tooltip.ShowSkillTooltip(Item);` — o ramo sem alvo (fallback intencional: comportamento antigo).
  Não há outra classe de hover (`grep IPointerEnterHandler` = só `RstvSkillHover`, l.2136). Logo, o alvo é preenchido em **todo** caminho read-only que TEM alvo; o ramo sem alvo cai no comportamento do jogo de propósito (fallback).
- **Não sobrescreve o valor do jogo**: `Patches.cs` l.763-767 — `if (__result != null) { return; }` sai do gancho sem tocar. No inventário `CurrentlySelectedCharacter != null` → o gancho é no-op. O gancho é POSTFIX (l.758-759 `[HarmonyPostfix] private static void Postfix(ref Character __result)`), com a assinatura por tipo (`[HarmonyPatch(typeof(Tooltip), "get_TooltipCharacter")]`, l.735) e parâmetro por **nome** (`__result`), nunca por índice.
- Cobertura de teste: `t_rstv27_rodape_valor.py` l.115-119 prende o valor do jogo vencendo (inventário) e o item (b) do teste estrutural. **Pergunta (b) confirmada.**

### (c) O try/finally desarma SEMPRE (inclusive se a chamada lançar) → **OK**

`SkillTreesTab.cs` l.2166-2182:

```
2166  Character alvo = ReadOnlySession.Target;
2167  if (alvo != null)
2168  {
2169      TooltipCharacterRodapePatch.ComAlvo(alvo);
2170      try
2171      {
2172          gui.tooltip.ShowSkillTooltip(Item.SkillInfo, alvo, showCanLevelDetail: false);
2173      }
2174      finally
2175      {
2176          TooltipCharacterRodapePatch.SemAlvo();
2177      }
2178  }
```

`SemAlvo()` zera `_alvoDoModal` (Patches.cs l.753-756). Um `finally` roda mesmo quando o `try` lança: se `ShowSkillTooltip` estourar, o desarme acontece antes de a exceção subir. Toda a `OnPointerEnter` ainda está num `try` externo (l.2143) com `catch` que loga `"RSTV-16: falha ao mostrar o tooltip da skill"` (l.2198-2201) — fail-safe em duas camadas. Os `return` de guarda (l.2145-2154) acontecem **antes** do `ComAlvo`, então não deixam estado armado. Checagem estrutural correspondente: `regras_rstv27.py` l.184-190 exige exatamente `ComAlvo(...); try { ShowSkillTooltip(...); } finally { SemAlvo(); }`. **Pergunta (c) confirmada.**

### (d) O teste prende a SAÍDA (o VALOR resolvido para o alvo do modal, com fallback) — não só a existência da chamada → **OK (a SAÍDA está presa; o teste é híbrido, ver limite)**

O teste `tools/testes/testes/puros/t_rstv27_rodape_valor.py` **compara os NÚMEROS campo a campo** contra o valor DERIVADO DO ALVO, não a existência da chamada:

- l.66-69: pega `base = esperado["sem_personagem"]`, `por = esperado["por_personagem"]`, `alvo`, `jogo` da fixture versionada;
- l.72-78: exige que o cenário **morda** (`base[campo] != por[alvo][campo]` para todo campo);
- **l.86-94**: `if valores[campo] != por[alvo][campo]: divergencias.append(...)` e `arc.exigir(not divergencias, "o rodape da Party Select read-only NAO monta os NUMEROS do ALVO DO MODAL: ...")` — a asserção é sobre o **VALOR** (`mana`/`cooldown`/`alcance`);
- l.108-113: fallback por valor (alvo nulo → BASE);
- l.115-119: valor do jogo vence no inventário.

A fixture `rstv27-rodape-valor.esperado.json` separa de fato alvo de base: `sem_personagem {mana:10, cooldown:3, alcance:4}` × `Raven {8, 1, 5}` × `Outro {15, 3, 4}` (números gerados por oráculo C# `tools/testes/fixtures/geradores/oraculo_rstv27`, procedência declarada no JSON).

**Prova de que a SAÍDA morde (não é decoração)**: a contra-prova pelo valor REPROVA citando os números — log `rstv27-valor-prova-reprovando.log` l.34:

```
[REPROVOU] rstv27-rodape-valor ... MANA: esperado 8 (o NUMERO do alvo 'Raven'), obtido 10 - IGUAL ao valor de BASE, o defeito do RSTV-27 | COOLDOWN: esperado 1 ... obtido 3 ... | ALCANCE: esperado 5 ... obtido 4 ...
```

**LIMITE declarado honestamente pelo próprio teste** (docstring l.42-44 e log): a ligação com o motor é uma transcrição (oráculo C# + decompilado) — o teste **lê a fonte** para decidir QUEM o rodapé consulta e escolhe um dos dois lados da fixture; ele **não executa o C# do mod nem o do jogo**. Ainda assim prende o VALOR (a SAÍDA), não só a chamada. **Pergunta (d) respondida com OK, com o limite acima explicitado.**

### (e) A contra-prova em sandbox FORA do repo demonstra os 4 defeitos plantados reprovando e restaura o repo byte a byte (sha256 final igual) → **OK (rodei eu mesmo as duas bancadas)**

Rodei `python tools/testes/prova-sandbox-rstv27.py` e `python tools/testes/prova-sandbox-rstv27-valor.py` no repo. Saída literal (bancada estrutural, a dos 4 defeitos):

```
RSTV-27 - CONTRA-PROVA EM SANDBOX FORA DO REPO
repo (NAO e' tocado): C:\dev\stolen-realm
sandbox:              C:\Users\Pichau\AppData\Local\Temp\rstv27-sandbox
  [sem defeito] exit=0 (esperado 0)
  [(a) hover sem armar o alvo do modal] exit=1 (esperado 1)   restaurado byte a byte: True (ecb75898ba136e9a)
  [(b) gancho sem preenchimento] exit=1 (esperado 1)          restaurado byte a byte: True (5f0d27f62e0aa0e9)
  [(c) gancho sem o fallback] exit=1 (esperado 1)             restaurado byte a byte: True (5f0d27f62e0aa0e9)
  [(d) gancho sobrescrevendo o valor do jogo] exit=1 (esperado 1) restaurado byte a byte: True (5f0d27f62e0aa0e9)
[REPO INTACTO] True
  ecb75898ba136e9a RoguelikeSkillTreeVisualizer/SkillTreesTab.cs
  5f0d27f62e0aa0e9 RoguelikeSkillTreeVisualizer/Patches.cs
VEREDITO: PROVA OK - sem defeito PASSA (exit 0); os 4 defeitos plantados REPROVAM (exit 1); cada um restaurado byte a byte; o repo nao foi tocado.
```

A bancada pelo VALOR (2 defeitos que mudam o número) também passou, com restauração byte a byte e `[REPO INTACTO] True`. Os dois sandboxes ficam em `C:\Users\Pichau\AppData\Local\Temp\...`, **fora de `C:\dev\stolen-realm`**; as bancadas leem o sha256 dos dois fontes do repo no início e no fim e confirmam igual (o "sha256 final" é o dos dois `.cs` do repo = os hashes da seção 0). As iscas plantadas usam as MESMAS âncoras que o teste lê; uma âncora sumida faria a bancada gritar `ANCORA NAO ACHADA: prova INVALIDA`. **Pergunta (e) confirmada.**

### (f) Risco residual (inlining do JIT do Mono) → **INDETERMINADO — plausibilidade BAIXA**

Se o JIT do Mono **inlinar** `Tooltip.get_TooltipCharacter` dentro de `ShowSkillTooltip`, o detour do Harmony não pega a cópia inlinada e o rodapé volta à base **em silêncio** (a suíte continua verde porque lê a FONTE). Isso é **irrefutável offline** com os meios permitidos (sem rodar o jogo) → **INDETERMINADO**.

Avaliação de plausibilidade (medida, não palpite):
- **IL do getter** (real, `ilspycmd -il`): **code size 35 bytes / ~10 instruções**, com **2 retornos** e **6 chamadas** (`get_instance`, `get_CurrentGuiState`, `get_instance`, `get_CurrentlySelectedCharacter`, `get_Instance`, `get_CreationCharacter`) + 1 desvio (`beq.s`). O inliner do Mono é conservador por padrão justamente com métodos que fazem chamadas e têm múltiplos blocos básicos — este não é um getter "de uma instrução".
- **Precedente no repo, em jogo**: o RoguelikeDebugger patcheia getters minúsculos do jogo (`Game.get_Skills`, code size ~7 na DLL) e o censo do projeto foi **gerado EM JOGO** com esses ganchos ativos — ou seja, pelo menos getters menores que este pegam. (Ressalva: isso prova que o detour pega o getter; não prova por si que o call site interno do jogo não tenha a cópia inlinada.)
- **Fechamento correto**: o próprio conserto loga, na 1ª resolução, `"RSTV-27: rodape da tooltip resolvido pelo personagem do MODAL (TooltipCharacter era null) - alvo=<nome>."` (Patches.cs l.778-784). Se essa linha aparecer no `LogOutput.log` do dono **e** o número na tela for o do personagem do modal, o gancho pegou (não houve inlining efetivo no caminho); se não aparecer, o risco se materializou. É o gate certo — **não** um teste offline.

**Conclusão de (f): plausibilidade BAIXA, mas o fato é INDETERMINADO offline; o log novo em jogo + o número na tela é que fecham.**

---

## 2. Suíte (rodei eu mesmo)

`python tools/testes/roda_testes.py --puros` (exit 0), trecho do RESUMO literal:

```
 RESUMO
   rodaram:    88
   passaram:   88
   reprovaram: 0
   nao rodaram:0
   EXCLUIDOS por categoria (1): jogo=1
 VEREDITO: VERDE (exit 0)
```

Os dois testes do RSTV-27 constam como PASSOU: `rstv27-rodape-personagem` e `rstv27-rodape-valor`. Rodando-os focados (`--teste ...`), cada um dá `1 rodaram / 1 passaram / VERDE (exit 0)`. Não rodei `dotnet build` nem `release-check.sh` (pesados e já provados pelo autor, conforme instruído).

---

## 3. Escopo 2 — dois cartões presos (veredito no disco de HOJE)

### t_4db38da9 — "Teste que prende o VALOR do rodapé resolvido para o alvo do modal" → **SATISFEITO**

Critério: *um teste que prenda a SAÍDA — o valor numérico do rodapé resolvido para `ReadOnlySession.Target` — e não a existência da chamada.*

- Arquivo: `tools/testes/testes/puros/t_rstv27_rodape_valor.py` (sha `d93efc…`).
- Prova do VALOR: **l.86-94** compara `mana`/`cooldown`/`alcance` contra a fixture derivada do alvo (`por[alvo][campo]`), com a mensagem `"o rodape da Party Select read-only NAO monta os NUMEROS do ALVO DO MODAL: ..."`; fallback por valor em **l.108-113**; regra do inventário em **l.115-119**.
- Fixture: `tools/testes/fixtures/rstv27-rodape-valor.esperado.json` (`base 10/3/4` × `Raven 8/1/5` × `Outro 15/3/4`).
- Prova de que MORDE: `rstv27-valor-prova-reprovando.log` l.34 REPROVA **pelo número** (`MANA: esperado 8 ... obtido 10 - IGUAL ao valor de BASE`).
- Está na suíte e verde: `rstv27-rodape-valor` = PASSOU (88/88); rodado focado = VERDE exit 0.
- Ressalva (não desqualifica): o teste é **híbrido** — lê a fonte para decidir QUEM o rodapé consulta e escolhe o lado da fixture; não roda o C#. A SAÍDA (o número) está presa mesmo assim.

### t_29871204 — "Contra-prova em sandbox fora do repo e build Release" → **SATISFEITO (com 1 ressalva registrada)**

Critério: *contra-prova registrada com comandos+saída+veredito explícito (defeito confirmado / não reproduzido) **e** evidência de build Release e suíte focada.*

- **Contra-prova registrada com comando + saída + veredito**: 
  - `tools/testes/rstv27-rodape-prova-reprovando.log` (sha `d7ffe5…`): `Comando: python tools/testes/prova-sandbox-rstv27.py`, saída literal das 5 rodadas (sem defeito + 4 defeitos, cada `exit=1`, `restaurado byte a byte: True`), e `VEREDITO: PROVA OK - ... os 4 defeitos plantados REPROVAM (exit 1) ...` (l.50).
  - `tools/testes/rstv27-valor-prova-reprovando.log` (sha `f40201…`): idem pelo VALOR, com o veredito na l.45.
  - Reproduzi as duas bancadas eu mesmo: ambas `VEREDITO: PROVA OK`, `[REPO INTACTO] True`.
- **Evidência de build Release**: `RoguelikeSkillTreeVisualizer/bin/Release/netstandard2.1/RoguelikeSkillTreeVisualizer.dll` existe (mtime `2026-10-06 14:00:10`), **posterior** às duas fontes (Patches.cs `13:46:42`, SkillTreesTab.cs `13:53:21`) → satisfaz a trava REL-1 de artefato×fonte. Decompilei a `TooltipCharacterRodapePatch` **da própria DLL Release** (`ilspycmd -t RoguelikeSkillTreeVisualizer.TooltipCharacterRodapePatch ...`) e o código compilado é **idêntico à fonte**: `[HarmonyPostfix] Postfix(ref Character __result)` com `if (__result != null) return;` → `alvoDoModal = _alvoDoModal;` → `if (alvoDoModal != null) { __result = alvoDoModal; <log> }` dentro de `try { } catch`. Ou seja, a Release **corresponde** ao conserto.
- **Suíte focada**: rodei os dois testes do RSTV-27 focados — cada um `VERDE (exit 0)`; e a suíte pura inteira `88/88 VERDE`.
- **RESSALVA**: não há no disco um **log** do `dotnet build -c Release -p:DeployToBepInEx=false` em si; a evidência de build Release é o **artefato** (DLL presente, mais nova que a fonte, com a classe do patch e o corpo compilado conferido). Se o critério exigir o log literal da compilação, este item vira PARTIAL; pelo artefato medido, está satisfeito.

---

## 4. O que NÃO foi exercitado / gates pendentes

- **Não rodei** `dotnet build` nem `bash tools/release-check.sh` (instrução explícita: pesados e já provados pelo autor). Não há `obj/Release` de build log. `INDETERMINADO` só quanto ao **log literal** da compilação — o **artefato** Release foi conferido por decompilação.
- **Não rodei o jogo** (sem BepInEx/carregamento de save): não exerci o Harmony em runtime no `ShowSkillTooltip`. Portanto (f) — inlining do Mono — fica **INDETERMINADO**.
- Não instalei, não deployei, não commitei, não publiquei, não criei/alterei cartão do kanban, não toquei em `Assembly-CSharp.dll`.
- **GATES PENDENTES (não fechados por esta revisão)**: (1) **verificação humana em jogo do dono** — hover no modal "Remove Skill Trees" (Party Select), conferir os números do rodapé do personagem exibido e a linha `RSTV-27: rodape da tooltip resolvido pelo personagem do MODAL (TooltipCharacter era null) - alvo=<nome>.` no `LogOutput.log`; (2) **publicação** na Thunderstore (a versão publicada é IMUTÁVEL).
- **Risco residual**: inlining (f), plausibilidade baixa, fechado só pelo log/verificação em jogo.

---

## 5. Veredito por item

| Item | Veredito |
|---|---|
| (a) propriedade get-only + rodapé lê o singleton (não o parâmetro) | **OK** |
| (b) postfix preenche todo caminho read-only + valor do jogo vence (sem regressão no inventário) | **OK** |
| (c) try/finally desarma sempre (mesmo lançando) | **OK** |
| (d) o teste prende a SAÍDA (valor p/ o alvo + fallback) | **OK** (teste híbrido, limite declarado) |
| (e) contra-prova em sandbox fora do repo: 4 defeitos reprovam + repo byte a byte intacto | **OK** |
| (f) risco residual do inlining do Mono | **INDETERMINADO** (plausibilidade BAIXA) |
| ACHADO A1 decompilado citado no enunciado não existe no caminho indicado | **ACHADO** (doc; não afeta o conserto) |
| t_4db38da9 | **SATISFEITO** |
| t_29871204 | **SATISFEITO** (ressalva: evidência de build é o artefato, não um log de compilação) |

Sem fechamento de tarefa, sem publicação, sem instalação, sem commit, sem alteração de cartão do kanban. Verificação humana em jogo e publicação continuam pendentes.
