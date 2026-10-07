# RSTV-26R — Revisão independente (RSTV-26)

- **Objeto:** RSTV-26 — dano/expressões da tooltip do hover da janela read-only do RSTV (modal *Remove Skill Trees*, Party Select) saíam como `'*0'` LITERAL.
- **Cartão:** t_bcd20b4d (status `blocked`, aguardando validação humana em jogo do dono).
- **Revisor:** subagente de revisão (NÃO é o autor). Modo: REFUTAR, não confirmar.
- **Escopo:** somente leitura do repo. Única escrita: este arquivo. Sem jogo, sem deploy, sem commit, sem publicação, sem tocar em `Assembly-CSharp.dll`, sem alterar cartão/kanban.
- **Data:** 06/10/2026.

## Hashes lidos (sha256)

| Arquivo | sha256 |
|---|---|
| `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs` | `ecb75898ba136e9ab13eda9113694153ad6a9703fd0dcf0cf2e08d36b9d53624` |
| `RoguelikeSkillTreeVisualizer/Patches.cs` | `5f0d27f62e0aa0e9a3f5e0b5072c1665a91871c6220c45cf3d0bd64b00455b49` |
| `RoguelikeSkillTreeVisualizer/SkillTreeReadOnly.cs` | `ec6851c50b0111b85ba697be2e05b30ad7b421d9386d9151def4b946c958d6a7` |
| `RoguelikeSkillTreeVisualizer/RunTargets.cs` | `4ab9db9531c7a86fb976ef94bdcb79fb4615f8a91b9cecd4e83d60356cae2a12` |
| `RoguelikeSkillTreeVisualizer/RunButton.cs` | `d6b47e52d791a939b1862cfdfaa1b2db0fd33f06390f21eaead23e57173fe044` |
| `RoguelikeSkillTreeVisualizer/RemovalWindowSkillsButton.cs` | `a12fb2980b20d88b0890a5e0c072d9c71c5beeff9e8beb60c841c4f53be49f17` |
| `RoguelikeSkillTreeVisualizer/SkillTreesWindow.cs` | `36df428a93437180189f58d1d1a32e41ccc91733f344cff2873b56b5f22ab935` |
| `tools/testes/regras_rstv26.py` | `64a5d01b45a784be3a651886f3a368331bca7846306c7a01fa49d393fdcef870` |
| `tools/testes/testes/puros/t_rstv26_tooltip_personagem.py` | `73fb33d4e385dead90fa612e8e1d240d6b7ccaa6c90ee8c62fd66381afd77bba` |
| `lib/Assembly-CSharp.dll` | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |
| decompilado `Tooltip` (prévio, cache) | `7b5bd4c1e6e5cf7f882d65511726e1f600fe43a4c7d1e7c481c3682d1e755cfc` |
| decompilado `Tooltip` (REFEITO agora de `lib/Assembly-CSharp.dll`) | `faaf4888e8fde440de160475ce41493bf06cd6deb460022d3073a925866c1268` |

Os dois hashes dos arquivos-sede batem com os do vigia (`ecb75898…` e `5f0d27f6…`) — leitura sobre o estado correto.

> **Fonte de prova do motor:** o `Assembly-CSharp.decompiled.cs` indicado no enunciado (371.804 linhas, em `scratch/cs/`) **não existe mais** (podado). Em substituição usei o decompilado por-classe em `scratch/ilspy-game2/` e, para não depender de cache alheio, **refiz o decompilado do tipo `Tooltip` com `ilspycmd` a partir de `lib/Assembly-CSharp.dll`** (o DLL real do jogo). As duas fontes coincidem nas linhas-chave (1308, 1434, 1472, 1589, 1594, 2212…), o que valida o decompilado usado.

## Separação de frentes (o que é RSTV-26 e o que NÃO é)

`git diff` sobre os dois arquivos-sede (ambos com alterações NÃO commitadas de outras frentes):

- **`SkillTreesTab.cs`** — 5 hunks. Os hunks em ~l.1914/1926/1935 são **AUT5-F1** (log `RSTV-24b` passou a contar linhas por tier) — **não** são RSTV-26. O hunk ~l.2103 é doc-comment. O hunk ~l.2126 é o **único** trecho de código do RSTV-26 (`Character alvo = ReadOnlySession.Target; … ShowSkillTooltip(Item.SkillInfo, alvo, showCanLevelDetail: false)` + o armamento do RSTV-27 `ComAlvo/SemAlvo`).
- **`Patches.cs`** — 1 hunk (~l.698-792): o patch `TooltipCharacterRodapePatch` = **RSTV-27**, **não** RSTV-26. Não há nenhuma alteração de RSTV-26 em `Patches.cs`.
- `SkillTreesWindow.cs`, `RemovalWindowSkillsButton.cs`, `RunTargets.cs`, `RunButton.cs`, `SkillTreeReadOnly.cs`: **sem diff** (`git diff --quiet` → UNCHANGED). Só `Patches.cs` (+91) e `SkillTreesTab.cs` (+63/−5) estão modificados na pasta.

## Item por item

### (a) O alvo passado é o personagem do MODAL (não o do jogo) — **OK**

Prova (cadeia, arquivo+linha):
- `RemovalWindowSkillsButton.cs:336` — `Character alvo = janela != null ? janela.CurrentCharacter : null;` (o personagem **do modal**); `:346` — `SkillTreesTab.AbrirJanela(alvo, ReadOnlyContext.RemocaoDeArvores, janela.transform);`.
- `SkillTreesTab.cs:528` — `_alvoDoPedido = alvo;` ; `:679-685` (em `IniciarSessaoReadOnly`) — `Character pedido = _alvoDoPedido; _alvoDoPedido = null; if (pedido != null) { alvo = pedido; … }` ; `:705` — `ReadOnlySession.Begin(alvo, _contextoPendente);`.
- `SkillTreeReadOnly.cs:41,48` — `Target { get; private set; }` recebe esse `target`. Ou seja **`ReadOnlySession.Target` = `janela.CurrentCharacter`** (o do modal), consumido UMA vez no `Begin`.
- `SkillTreesTab.cs:2166` — `Character alvo = ReadOnlySession.Target;` é exatamente esse objeto.

Refutação tentada: o `Begin` só usaria o personagem do jogo se `_alvoDoPedido` fosse nulo — mas `AbrirJanela` só é chamado por `RemovalWindowSkillsButton.OnClick`, que já guarda `alvo == null` (`:337`). Falha.

### (b) Os placeholders (`*N`/`[N]`) resolvem contra o ARGUMENTO `character` (não o singleton) — **OK**

Prova no motor real (`Tooltip` decompilado de `lib/Assembly-CSharp.dll`):
- Assinatura existe: `Tooltip.cs:1308` — `public void ShowSkillTooltip(SkillInfo skill, Character character, bool showCanLevelDetail, bool fromLink = false, bool showTierData = false)`. O `showCanLevelDetail:` nomeado do mod casa com ela.
- O **corpo** usa o ARGUMENTO `character`:
  - `:1321` `skill.ObtainedByItem(character)`; `:1326` `skill.ObtainedByStatus(character)`; `:1345` `ParseGetFlatDamageValue(original, character?.Level ?? 1, …)`.
  - `:1434` `GetDamageString(original, skill.TooltipDamageInfoRefAction, character, …)`; `:1438/1443` idem; `:1445-1448` `ApplyDescriptionExpressions(original, skill.DescriptionExpressions, new GameFunctionParameters { Source = character }, …)`.
- O `*` é resolvido por `GetDamageString` (`Tooltip.cs:2254` — `while (text2.Contains("*")) { … Character.GetActionDamage(source, …) }`), que é chamado **só dentro** de `if (character != null)` (`Tooltip.cs:1352`).
- O overload de 1 argumento (o do defeito) passa o **singleton**: `Tooltip.cs:1594` — `ShowSkillTooltip(skillInfo, TooltipCharacter, showCanLevelDetail: true)`; e `Tooltip.cs:192-198` — `TooltipCharacter => GameLogic.instance.CurrentlySelectedCharacter` (getter; get-only).
- `SkillTreesTab.cs:2172` — `gui.tooltip.ShowSkillTooltip(Item.SkillInfo, alvo, showCanLevelDetail: false);` (o argumento é o alvo do modal).

Refutação tentada: o corpo ainda leria o singleton? Falha — todos os resolvers do corpo (`ObtainedBy*`, `GetDamageString`, `ApplyDescriptionExpressions`) recebem `character`, o parâmetro. O singleton só aparece no **rodapé** (`:1472 tooltipCharacter = TooltipCharacter`) — que é justamente o objeto do RSTV-27, fora do escopo deste cartão. Com `character == null` o bloco `:1352` é pulado e o texto cru (`*0`) fica — reproduz o defeito relatado; com o alvo não-nulo, o bloco roda e resolve. **Coerente.**

### (c) A janela continua read-only DE VERDADE — **OK**

- O caminho novo **só lê**: lê `ReadOnlySession.Target` e chama `ShowSkillTooltip` (ver (b), tudo leitura) + `TooltipCharacterRodapePatch.ComAlvo/SemAlvo` (escrevem um `static` próprio, `Patches.cs:747,753`) + o postfix do RSTV-27 grava só o `__result` do getter (`Patches.cs:776`). Nenhuma escrita no personagem.
- `showCanLevelDetail: false` **desliga** o bloco de custo: em `Tooltip.cs:1352-1358` o bloco `Skill Point Cost`/`Select To Learn`/`CanLevel` só roda `if (flag)`, e `flag = showCanLevelDetail` (`:1347`). Sem esse caminho, **não há chamada a `CanLevel` nem acesso a `LoadableUIWindow<SkillTreeManager>.Instance`** nessa branch.
- Blindagens do read-only **intactas** em `Patches.cs`: `AcceptSkillChanges` higienizado (prefixo devolve snapshot união dono+jogo → lista de remoção vazia; `:134-204`), `Initialize` reafirma estado (`:214-266`), `RespecButton` escondido (`:276-295`), `ToggleAddToSkillToAddList` bloqueado (`:305-357`), `ResetSkillPoints` bloqueado (`:371-408`).
- **Nenhum método de FECHAMENTO é bloqueado**: os postfixes de `SkillTreeManager.OnDisable` (`:450-468`) e `CharacterMenusManager.CloseSkillTreeMenu` (`:484-502`) **apenas** chamam `ReadOnlySession.End()`, sem `return false`.
- `Character.GetActionDamage(Character source, …)` (`Character.cs:9524`) é o mesmo helper estático que o próprio jogo usa ao montar qualquer tooltip de skill (usado em `Character.cs:9468/9518` e no `ShowSkillTooltip` normal do inventário). Se fosse caminho de escrita, corromperia o jogo a cada hover — não é.

### (d) Re-parent / janela preservados — **OK**

- `SkillTreesWindow.cs` **não tem diff** (`git diff --quiet` → UNCHANGED). O `AbrirJanela`/`SairDoModoJanela`/`AoFecharJanela`/`Garantir` (`SkillTreesTab.cs:516-599`) **não estão em nenhum hunk** — o diff mexe só nas l.2103/2126 (tooltip). O re-parent e o dono/ciclo de vida (aprovados na RSTV-11b/21) seguem intactos.
- Testes de regressão de janela seguem verdes: `rstv11b-botao-janela-levelup` PASSOU e `rstv21-janela-propria` PASSOU (saída abaixo).

### (e) Regressão no INVENTÁRIO (onde `CurrentlySelectedCharacter` existe e deve vencer) — **OK**

- No caminho do inventário o alvo explícito **é** o `CurrentlySelectedCharacter`: `SkillTreesTab.Abrir(..., contexto)` (`:434`, vindo de `RunButton.OpenForTarget:402-423`) e `SelecionarEMostrar` (`:635`) caem em `IniciarSessaoReadOnly` → `RunTargets.Resolve` (`RunTargets.cs:353-366` devolve `gl.CurrentlySelectedCharacter` quando não-nulo). Logo `ReadOnlySession.Target == CurrentlySelectedCharacter` no caso normal → resultado idêntico ao anterior.
- Se `Resolve` devolvesse `null` (jogo sem seleção), o guard `if (alvo != null)` é falso → cai no `else` `gui.tooltip.ShowSkillTooltip(Item);` (`SkillTreesTab.cs:2181`), que usa o `TooltipCharacter` do jogo = comportamento antigo. **Sem regressão.**
- O gancho do RSTV-27 (rodapé) **reforça** o mesmo: `Patches.cs:763-767` — `if (__result != null) return;` (o valor do JOGO vence). No inventário `__result != null` → o gancho é no-op.
- Ver também `tools/testes/regras_rstv26.py:87` (`personagem_do_motor("Raven","Outro") == "Raven"`) — o modelo encoda que o alvo explícito vence, e o teste `rstv27-rodape-valor` cobre "no inventário o valor do JOGO vence".

## Testes (saída literal)

Comando: `python tools/testes/roda_testes.py --puros` (em `C:/dev/stolen-realm`).

Resumo literal:

```
 RESUMO
   rodaram:    88
   passaram:   88
   reprovaram: 0
   nao rodaram:0
   EXCLUIDOS por categoria (1): jogo=1
       -> NAO foram executados. Nao contam como verde: este modo os exclui de proposito.

 VEREDITO: VERDE (exit 0)
```

Linhas do RSTV-26 (e vizinhas) literais:

```
[PASSOU ] rstv26-tooltip-personagem           RSTV-26: o hover da janela read-only passa o personagem do MODAL (ReadOnlySession.Target) ao ShowSkillTooltip, com `showCanLevelDetail: false`; o motor resolve o '*N'/'[N]' contra ele (sem o TooltipCharacter null) e o alvo null cai no comportamento antigo — o defeito SEM o alvo explicito republica o '*0'
[PASSOU ] rstv27-rodape-personagem            RSTV-27: ...
[PASSOU ] rstv27-rodape-valor                 RSTV-27 pelo VALOR: ...
```

**Ressalva sobre o teste do RSTV-26** (para não superestimar a cobertura): `t_rstv26_tooltip_personagem.py` é **estrutural** — lê o fonte AO VIVO e checa a presença/ligação do `ReadOnlySession.Target`, do guard e da chamada de 3 argumentos, além de um **modelo puro** que transcreve a decisão do motor (`regras_rstv26.py:81-97`). Ele **não** exercita a DLL. A prova de que o corpo resolve contra `character` e de que `*` é resolvido por `GetDamageString` foi feita **por mim** contra o decompilado do `lib/Assembly-CSharp.dll` (item (b)) — é a parte que o teste não cobre e que esta revisão confirmou.

Não há contra-prova dedicada ao RSTV-26 em `tools/testes/contra-prova/` (o diretório lista `cp_rstv*` de 8/11/12/13/14/16/18/19/21, nenhum de 26). A "prova de fogo" vive dentro do próprio `t_rstv26_…py:69-79` (planta o hover antigo e exige que `falhas_do_hover` reprove).

## O que NÃO consegui exercitar / INDETERMINADO

- **Validação em jogo (tela):** INDETERMINADO por natureza — só o dono, em tela, confirma que o número **aparece** no lugar do `*0` no modal Party Select, e que nada some/re-parenteia errado. Sem jogo nesta revisão (por regra). É o **gate de publicação**; continua pendente.
- **Runtime da DLL do mod:** não recompilei/instalei (por regra: proibido `dotnet build` sem a flag e proibido build/instalação no perfil do dono; e `build`/`release-check` declarados pesados pelo autor). Logo não exercitei a Harmony aplicando de fato os patches em runtime — validei assinaturas/linhas por leitura do fonte e do decompilado, não por execução.
- **Divergência `ReadOnlySession.Target` × `CurrentlySelectedCharacter` durante troca de seleção com a aba aberta:** não reproduzível fora do jogo. Ver risco residual.

## Risco residual

- **Baixo — staleness do alvo no inventário.** `ReadOnlySession.Target` é fixado no `Begin`; a chamada do RSTV-26 o usa **incondicionalmente** no corpo (diferente do rodapé/RSTV-27, que só preenche `null`). Se — hipoteticamente — `CurrentlySelectedCharacter` mudasse com a aba do RSTV ainda selecionada, o corpo passaria a resolver contra o alvo antigo em vez do novo. Na prática a sessão morre quando a aba deixa de ser a selecionada (`SkillTreesTab.cs:782-789`) e o inventário é por-personagem, então o cenário é improvável; ainda assim fica registrado. Mitigação já existente: no caso `Target == null` cai no comportamento antigo.
- **Muito baixo — nível do alvo.** Em `Tooltip.cs:1345` o nível vem de `character?.Level` (agora o do modal); é o comportamento pretendido pela correção, não um defeito.

## Veredito

| Item | Veredito |
|---|---|
| (a) alvo = personagem do MODAL | **OK** (prova l.336/346 de RemovalWindow…; SkillTreesTab.cs:528/679-705/2166; SkillTreeReadOnly.cs:41) |
| (b) corpo resolve contra o argumento `character` | **OK** (Tooltip.cs:1308/1321/1326/1345/1434-1448; `*` em :2254 dentro de `if(character!=null)` :1352; singleton em :1594/:192-198; chamada :2172) |
| (c) read-only de verdade | **OK** (só leitura; guard de custo desligado :1347/:1352; Patches.cs:134-408; fechamento não bloqueado :450-502) |
| (d) re-parent/janela preservados | **OK** (SkillTreesWindow.cs sem diff; AbrirJanela/AoFecharJanela fora dos hunks; rstv11b/rstv21 PASSOU) |
| (e) sem regressão no inventário | **OK** (RunTargets.cs:353-366; fallback :2181; gancho do jogo vence :763-767) |
| Testes puros | **VERDE** 88/88, incl. `rstv26-tooltip-personagem` PASSOU |
| Validação em jogo (dono) | **INDETERMINADO / pendente** (gate de publicação) |
| Runtime da DLL do mod | **INDETERMINADO** (build/instalação não executados por regra) — assinaturas validadas por leitura |

**ACHADOS bloqueantes: nenhum.** O conserto do RSTV-26 está correto e o read-only está preservado; o defeito é refutavelmente explicado pela fonte do jogo e a correção o endereça. Publicação continua **bloqueada** até a verificação humana em jogo do dono.
