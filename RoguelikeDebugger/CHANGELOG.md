# Changelog — RoguelikeDebugger

> Ferramenta de **desenvolvimento**, não mod de jogador.

## 0.1.2

**Nada muda no jogo: o que muda é o TEXTO do log.** Esta versão leva o que ficou pronto depois de a 0.1.1 subir (01/10) — o dump de status mais completo e resistente, a instrumentação de uma investigação aberta e o texto público em inglês.

- **O dump de status não trunca mais por campo (RD-2F).** Antes havia um `try/catch` ÚNICO em volta do laço inteiro: uma exceção em qualquer campo (os campos novos leem arrays `IEffectInfo[]` por reflexão) abortava o laço e **o resto dos statuses sumia do log em silêncio**. Agora cada campo sai sob guarda e a falha vira um **marcador no próprio campo** (`!erro:<Tipo>`) — a linha e todas as seguintes saem normalmente. O laço também itera uma **CÓPIA** da lista (uma inserção durante a iteração tinha o mesmo efeito). O corte por tamanho (`90`/`110` chars) saiu de vez: ele cortava a mecânica.
- **Campos novos no `[Status]` (RD-2):** `expr` (`DescriptionExpressions`), `danoExpr` (`DamageExpressionOverrides`), `refAcao`/`refStatus` (`TooltipDamageInfoRefAction`/`RefStatus`), `tick` (`TickTargets` + `ActionsOnTick*` + `StatusEffectsOnTick*`) e `auraSts` (`AuraSourceStatus`/`AuraTriggerStatus`). Dentro do `trigEf` do status: `~alvos=` (o campo `SkillTrigger.Targets`), `~acoes=` (as ações do gatilho **com os efeitos delas** — ação de gatilho nunca entra no inventário `[Action]`), `~chances=` e `~cd=`. Foi o `~alvos=` que respondeu a seção 7 do RV-19: `Flame Shrine Aura` dispara com `Targets="Cell.IsCurrentHex(Target)"` (`TriggerType=1`) e `Decay Shrine Aura` com `"Cell.IsCurrentHex(Source)"` (`TriggerType=4`) — o proc **não** passa pelo caminho de tick.
- **Medição desses campos no asset do jogo** (leitor offline, **não** em jogo): 421 dos 424 `ActionStatusInfo` legíveis; `expr` em 138, `refAcao`/`refStatus` em 19/7, `StatusEffectsOnTick` em 6, `auraSts` em 40 e `TickTargets`/`ActionsOnTick*` em **0**.
- **Instrumentação `[FlameRV49]` (RV-49) — NÃO EXERCITADA EM JOGO.** Quando o proc de uma aura de shrine de perigo (Decay/Flame) dispara, o log ganha a expressão avaliada, **quem o motor colocou em `Source` e em `Target`**, o percentual resolvido, o dano final e uma **matriz** que reavalia a mesma expressão com o `ShrineEffectBonus` fixado em 0 / 8 / 20 / 100 (Omnism I/II, Horn of Devotion). É instrumentação de diagnóstico para uma pergunta ainda aberta: nenhum personagem é alterado (a matriz usa dicionários novos e devolve `Game.CurrentGameFunctionParameters` ao valor anterior). Filtro: só a expressão que cita `ShrineEffectBonus` gera linha.
- **Instruções de build (DEPLOY-2):** o deploy no perfil do r2modman virou **opt-in explícito** — `dotnet build` sozinho **não instala mais nada**; instalar é `-p:DeployToBepInEx=true`.
- **Texto público em inglês:** o README passa a ser em inglês (com a seção final em português, como nos outros mods) e a **descrição da listagem**, que na 0.1.1 saiu em português, passa a sair em inglês. O README declara o que ainda **não** foi exercitado em jogo.

### O que esta versão NÃO prova

- **Nenhum campo novo desta versão foi lido numa sessão de jogo.** O `[FlameRV49]` é instrumentação nova e o RV-49 continua pendente de rodada autorizada do dono; os campos do RD-2 foram medidos no asset pelo leitor offline. Quem abrir o jogo é quem confere.

## 0.1.1

**Correção do aplicador de ganchos: a 0.1.0 publicada carregava a ferramenta e não aplicava gancho nenhum — nenhum dump saía.**

- A troca do `PatchAll()` por **aplicação gancho a gancho** veio acompanhada de um filtro de classe de gancho que exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no método**. Este mod declara os 10 ganchos pela **convenção de nome** do Harmony (método `Postfix` em cada classe de `Patches/`), que o Harmony aceita exatamente como o atributo — o filtro recusava as 10 classes: a ferramenta **carregava, logava "carregado." e não dumpava nada** (o silêncio parecendo sucesso; era o defeito A-1 da REV-2, em 4 mods).
- O filtro agora exige só `[HarmonyPatch]` **no TIPO** — o mesmo conjunto de classes que o `PatchAll()` processava. Medido invocando o filtro real da DLL construída: **10 de 10 classes de patch aceitas e 10 métodos de gancho dentro** (antes: 0 de 10). Em todo o projeto, os 4 mods afetados passaram de 0/14 para **14/14** classes de patch aceitas.
- **Ganchos aplicados um a um** (mesmo endurecimento, mesma release): `CreateClassProcessor(...).Patch()` por classe de gancho, uma linha de log por gancho e resumo com a **contagem real** — um gancho que falhe não derruba os outros nove.
- **Ícone definitivo** (arte do dono em `docs/img/roguelikedebugger-icon-fonte.png`, 1254x1254): redimensionado para os **256x256** que a Thunderstore exige e embutido no pacote. Sai o **placeholder** de 946 bytes com as iniciais que o empacotador gerava (`--gerar-icones`), que era o que estava indo no zip. A arte-fonte continua versionada em `docs/img/` — o repositório guarda as duas.

### Dump: efeitos por TIPO CONCRETO (RV-8b-0g)

- Os arrays `Effects` (de status e de ação) são `IEffectInfo[]`, interface vazia: o cast `e as GeneralEffect` que o dump usava para ler o `Action` devolve `null` em todo elemento de outro tipo, e o dado desaparecia do dump (2 entradas do censo de tooltips ficaram `indeterminado` por isso). Agora:
  - campos novos `nEfeitosTot` / `efTipos` (status e ação): tamanho do array e **tipo concreto + campos de cada elemento**, lidos por reflexão;
  - `nAttrEf` / `attrTipos` (status e skill) e `consEf` (item) para os `AttributeEffects` e a ação de consumível;
  - `nTrig` / `trigEf` no `[Status]`: os gatilhos do status (tipo, efeitos, condição, status) — antes não saíam;
  - linha de resumo por categoria, `[Efeitos] resumo (...): total= | porTipo= | naoGeneralEffect=`.
  - `desc=` continua por último e nenhum valor contém `|` ou aspas: o formato antigo não muda.
- **A versão subiu (0.1.0 → 0.1.1) por causa da correção do aplicador acima:** a 0.1.0 que estava no ar carrega o defeito e versão publicada na Thunderstore é imutável. Este dump novo é o mesmo que estava em "Não lançado".

### Dump: ganchos de tempo/aura, gatilho e expressões do status (RD-2)

- Campos novos no `[Status]`, todos antes do `desc=`: `expr` (`DescriptionExpressions`), `danoExpr` (`DamageExpressionOverrides`), `refAcao`/`refStatus` (`TooltipDamageInfoRefAction`/`RefStatus`), `tick` (`TickTargets` + `ActionsOnTick*` + `StatusEffectsOnTick*`) e `auraSts` (`AuraSourceStatus`/`AuraTriggerStatus`).
- O `trigEf` do status passou a publicar o **`Targets` de cada `SkillTrigger`** (`~alvos=`) e as ações do gatilho **com os próprios efeitos** (`~acoes=Nome{ef=...}`). É o que fecha a pergunta do proc das auras de shrine: `Flame Shrine Aura` → `TriggerType=1`, `Targets="Cell.IsCurrentHex(Target)"`, `Actions=[Flame Aura Proc]`; `Decay Shrine Aura` → `TriggerType=4`, `Targets="Cell.IsCurrentHex(Source)"`.
- **A versão NÃO muda** (0.1.1 segue): são campos do mesmo dump ainda não lançado.
- Medição no build (421 dos 424 `ActionStatusInfo` do asset — 3 não são legíveis pelo leitor offline): `expr` em 138, `refAcao`/`refStatus` em 19/7, `StatusEffectsOnTick` em 6, `auraSts` em 40 (sempre junto de `IsAura=1`) e `TickTargets`/`ActionsOnTick*` em **0** — ou seja, o proc das auras de shrine não passa pelo caminho de tick. Detalhe e `arquivo:linha`: `docs/DEBUGGER.md`.

## 0.1.0

Primeira versão publicada.

- **Dump dos dados internos do jogo no `LogOutput.log`** (apenas logs, nenhuma alteração de gameplay):
  - **Skills**: inventário com nome, descrição, expressões de descrição, ações concedidas, efeitos de atributo e gatilhos.
  - **Ações** (`[ActionProps]` / `[Trigger]`): tipo, alvos, alcance máximo, knockback, número de golpes, cooldown, cargas, condições de uso, chances e status aplicados.
  - **Status**: inventário de buffs/debuffs com efeitos de atributo e descrição.
  - **Itens e afixos**: tipo, raridade, descrição opcional, atributos, proporção de armadura e ação de consumível.
  - **Powerups**: inventário do roguelike, uma linha por nível.
  - **Loot, ouro e experiência**: os rolls, os modificadores aplicados e os valores concedidos.
- É a fonte dos CSVs de cobertura em `docs/cobertura/` usados pelos outros mods do projeto.
- **Não distribuir para amigos**: enche o log com milhares de linhas a cada boot.

