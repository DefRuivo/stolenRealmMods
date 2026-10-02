# O RoguelikeDebugger como fonte de informação

## A regra deste projeto

**Antes de pedir qualquer leitura humana, verifique se o debugger consegue extrair o dado sozinho.**
Se não conseguir, **estenda o dump** — não peça para o dono ler a tela e transcrever.

O dono é o último recurso, não o primeiro. Toda vez que uma tarefa precisa de um número, um campo
ou uma relacao do jogo, a pergunta inicial e: *isso sai do jogo ou do codigo sem ninguem olhar?*
A conferencia visual continua sendo dele — o que **nao** pode continuar sendo dele e a **coleta**.

Exemplo que originou a regra: o checklist de shrines (RV-35..RV-46) pedia que o dono passasse por
cada aura, lesse o valor na tooltip e comparasse de cabeca com tres casos. A linha do Flame nasceu
com o sujeito errado e so foi descoberta porque alguem mediu em jogo. O valor estava no motor e no
asset o tempo todo.

## Estado atual (medido, nao presumido)

Categorias que o dump ja publica: `[Status]`, `[Action]`, `[Skill]`, `[Item]`, `[ItemMod]`,
`[Powerup]`, `[Loot]`, `[Event]`, `[LifeSteal]`, alem do resumo `[Efeitos]`. Sao 9 arquivos de
gancho em `RoguelikeDebugger/Patches/`.

## Por que ele E extensivel (e nao por otimismo)

`RoguelikeDebugger/EfeitosInfo.cs` (RV-8b-0g) descreve arrays de efeito por **reflexao**, sem
referenciar **nenhum tipo do jogo**: ele percorre `System.Array`, imprime `indice:Tipo{campo=valor}`
e resume por tipo concreto. O proprio cabecalho do arquivo diz o proposito: *se aparecer um terceiro
implementador de `IEffectInfo`, ele sai no dump sem recompilar*.

Foi esse desenho que consertou um defeito real: o dump antigo fazia `e as GeneralEffect` sobre
`IEffectInfo[]` — interface **vazia** com duas implementacoes — e todo elemento do segundo tipo
(`CharacterVariableEffectInfo`) desaparecia **com o tipo junto**, o que impedia ate de saber que o
dado faltava.

> **CORRECAO (DOC-8, 01/10) — o veredito do censo esta certo; a causa que esta frase dava estava
> errada.** O paragrafo acima dizia que aquele defeito era *a causa* das duas ultimas entradas
> `indeterminado`. **As duas que RESTAM nao sao aquelas.** O censo fecha com **2** `indeterminado`
> — `Champion of Blood` e `Frenzy` (`docs/cobertura/status.csv`) — e as duas seguem, no dump de
> boot, `nEfeitosTot=0` / `efTipos=` / `nTrig=0`, com **0** gatilho e **0** `descExpr` na passagem
> offline dos 421 assets. O motivo de continuarem abertas e o da secao 7 (RV-13c) §7.5 do
> `docs/cobertura/revisao/RV-13b-fechamento.md`: o numero mora **fora do status**, em campo de
> efeito serializado por **referencia de interface** — `ActionStatusInfo.Effects` / `ActionInfo.Effects`
> (`IEffectInfo[]`) — que o node de typetree gerado **nao inclui** (no `Champion of Blood`, o
> `CharacterInfo` do invocado carrega o elo) — **nao** o cast `as GeneralEffect`. O historico de como
> as duas chegaram la fica registrado: nasceram `indeterminado` no RV-13, o RV-13b §4.3 manteve 16
> com o motivo nomeado no lugar da duvida, e o RV-13c §7 leu o asset e fechou 14 — sobraram estas
> duas.

## Backlog auditado — fechado no RD-2 (01/10)

O que a auditoria das auras (`docs/cobertura/revisao/RV-19-shrines.md`, secao 7) pedia e nao
salia no dump. **Tudo entrou no dump de status** (`ActionStatusInventoryPatch`), campo antes do
`desc=`, valor saneado. A coluna "medicao" e a contagem de statuses que REALMENTE preenchem o
campo — medida nos 421 `ActionStatusInfo` dos assets (resources.assets + os outros 7 arquivos,
lidos pelo asset com UnityPy; nenhum outro arquivo tem status).

> **Caveat da medicao:** ha **424** objetos com o script de `ActionStatusInfo`; 421 sao legiveis
> pelo leitor offline (UnityPy + typetree gerado da `Assembly-CSharp.dll`) e **3 nao** (o blob
> Odin deles dessincroniza o leitor — um deles e o `Dwarven Totem Aura Status`, pathID 2543235;
> os bytes dele foram lidos a mao). Isso e limite do LEITOR OFFLINE, nao do dump: o mod le os
> campos pela API do C# (`s.TickTargets`, `s.SkillTriggers[].Targets`), que nao dessincroniza.
> O que ficou fora da contagem: os 3 objetos acima.

> **Denominador: o dump NAO tem 421 statuses, tem 600.** Todo `X/421` da tabela abaixo e a passagem
> OFFLINE do asset (os 424 objetos, os 421 legiveis). O dump de boot imprime **600** — medido no
> `LogOutput.log` de 01/10: `[Status] Inventário: 600 status carregados.` e 600 linhas `[Status] '`.
> Os outros **176** (600 − 424) sao **SINTETICOS**: `LoadListActionStatuses` (l.134750-134863) cria um
> `ActionStatusInfo` em RUNTIME para CADA `EventStatus` (`ScriptableObject.CreateInstance` + copia de
> `name`/`Description`/`AttributeEffects`/`SkillTriggers`/..., com `Duration = "0"` e `Infinite =
> true`). Eles saem no dump como qualquer outro (ex.: `Oculus Gem`, `Phoenix Feather` — o tipo
> `Fortune`), mas **nao tem par** na passagem offline: um `X/421` nao conta esses 176 nem diz o que
> eles preenchem.
>
> **Terceiro denominador (DOC-8, 01/10): o censo dedupa para 560.** As 600 linhas `[Status]` do boot
> viram **560** entradas em `docs/cobertura/status.csv`, por (nome, descricao) — 73 linhas caem em
> pares repetidos. E de 560 que saem as 2.280 do RV-13 (5 arquivos). Ou seja, os tres numeros medem
> coisas diferentes — **600** (dump de boot, com os 176 sinteticos: `LoadListActionStatuses` recria
> `ActionStatusInfo` para cada `EventStatus`), **424/421** (objetos no asset / legiveis offline pelo
> UnityPy) e **560** (censo dedupado) — e **nao** se converte um no outro. Nao re-derivar o censo dos
> 421 nem procurar os 2.280 entre os 600 (detalhe no §8.2 item 4 do
> `docs/cobertura/revisao/RV-13b-fechamento.md`).

> **O que NUNCA aparece no dump: acao que nao e concedida por skill nem e `Actions` de gatilho de
> status.** O `[Action]` filtra por skill (a propria linha do boot diz "277 acoes concedidas por
> skills") e o gatilho de status publica as `Actions` dele DENTRO do gatilho (`~acoes=`, RD-2R). Acao
> que nao vem por nenhum dos DOIS caminhos continua fora de tudo: a familia `* Shrine Explosion`
> (RV-19 secao 7 — `Warrior Shrine Explosion`, `Conqueror Shrine Explosion`, ... e os `... Status`)
> da **0** ocorrencias no log de boot inteiro (453 skills + 277 acoes + 600 statuses + 905 itens). Um
> `X/421` tambem nao cobre isso.

> **Numeracao das linhas:** os `l.NNNN` desta tabela sao do decompilado **regerado em 01/10** com
> ilspycmd 8.2.0. O arquivo que existe hoje (`%LOCALAPPDATA%\hermes\cache\scratch\cs\Assembly-CSharp.decompiled.cs`)
> tem **496.253** linhas — contadas com `wc -l` (e `grep -c ""`, que da o mesmo) em 01/10/2026 — e esse
> numero muda se o cache for **regerado** (a versao anterior, de 371.804 linhas, nao esta mais no
> cache): conferir a contagem do arquivo ANTES de citar. As revisoes antigas (RV-13b, RV-19) citam
> aquele outro decompile — os numeros divergem; o nome do campo e a chave estavel para reconferir.

| campo no dump | campo do motor (decompilado `Assembly-CSharp.decompiled.cs`) | medicao |
|---|---|---|
| `expr=` | `ActionStatusInfo.DescriptionExpressions` (l.441015) | 138/421 |
| `danoExpr=` | `DamageExpressionOverrides` (l.441020) | 1/421 (`Chaos Curse`) |
| `refAcao=` / `refStatus=` | `TooltipDamageInfoRefAction` / `TooltipDamageInfoRefStatus` (l.441022/441024) | 19 / 7 |
| `tick=` | `TickTargets` (l.441035), `ActionsOnTickCondition` (441042), `ActionsOnTickTargets` (441045), `ActionsOnTick` (441047), `ActionsOnTickProcTriggers` (441049), `StatusEffectsOnTickCondition` (441052), `StatusEffectsOnTickTargets` (441055), `StatusEffectsOnTick` (441057), `StatusEffectsOnTickOverrides` (441059) | so `StatusEffectsOnTick`: 6/421 (`Freeze Earth`, `Ice Storm`, `Faerie Swarm`, `Blood Mist`, `Slow Poison Aura`, `The Bad Bloom`). Os outros campos: **0/421** — o `tick=-` de toda linha e a medida de que o proc das auras de shrine NAO passa por aqui |
| `auraSts=` | `AuraSourceStatus` / `AuraTriggerStatus` / `AuraTriggerStatusOverrides` (l.441108/441110/441112) | 40/421 — sempre junto de `IsAura=1` (os 40 batem; `IsAura` e o sinal barato do censo de auras). As auras de SHRINE **nao** estao nesses 40 |
| `trigEf=...~alvos=` | `SkillTrigger.Targets` (l.46590) | 39/421 statuses tem gatilho |

> **RESSALVA (DOC-8, 01/10) — nenhum destes campos novos esta no log de boot ainda.** O que esta
> tabela mede e o **fonte** e a passagem **offline do asset** — nao o dump que roda hoje. A DLL que
> o perfil carrega e de **30/09 21:22** (md5 `28b7959a8e77411b0c88ad8cdfbcbc32`), anterior ao RD-2R:
> as **600** linhas `[Status]` do `LogOutput.log` de 01/10 saem no formato antigo
> (`… | nEfeitosTot=0 | efTipos= | nAttrEf=… | attrTipos=… | nTrig=0 | trigEf= | desc="…"`) e **nao**
> tem `expr=`, `danoExpr=`, `tick=`, `auraSts=`, `~alvos=` nem `~acoes=`. (O `expr=` / `danoExpr=` que
> o log de 01/10 mostra e o das linhas `[Skill]`/`[Action]` — 453 + 287 = 740 ocorrencias —, nao
> dos status.) Ou seja: **campo novo nao aparece no log enquanto a DLL nao for deployada e o jogo
> bootar** — propagar um campo novo para os CSVs de `docs/cobertura/` exigiria esse ciclo
> (deploy + boot), o que e **decisao do dono**, nao desta rodada. Nao procurar `expr=`/`tick=`/
> `~alvos=` nas linhas `[Status]` do boot de hoje: ainda nao estao no ar (medicao e conflito
> completos no §8.2 item 1 do `docs/cobertura/revisao/RV-13b-fechamento.md`).

**CORRECAO DE UM FATO ERRADO DA VERSAO ANTERIOR DESTE DOC:** ele dizia que `SkillTrigger` NAO
tinha campo `Targets`, e a instrucao era "nao invente". O campo existe — `[TextArea] public
string Targets;` na l.46590 — e e **ele** que fecha a pergunta aberta das auras de shrine. Lido
do asset (`resources.assets`): `Flame Shrine Aura` (pathID 2543240) tem
`SkillTriggers[0].Targets = "Cell.IsCurrentHex(Target)"`, `TriggerType = 1`,
`Condition = "Source.IsEnemy(Target)"`, `Actions = [2544297 "Flame Aura Proc"]`; o
`Decay Shrine Aura` (2543234) tem `Targets = "Cell.IsCurrentHex(Source)"` com `TriggerType = 4`
(`Actions = [2544288 "Decay Aura Proc"]`). Nem `ActionsOnTick` nem `AuraSourceStatus` aparecem
nesses dois statuses. O que faltava era o campo sair no dump: `SkillTriggers` **ja** era
exportado, mas publicava so TriggerType/cond/status.

A formula das auras tambem nao estava visivel: ela mora em `DescriptionExpressions` do STATUS
(`Flame` = `Mathf.Round(5 * (1 + (Source["ShrineEffectBonus"] / 100)))`; `Decay` = base 10;
`Warrior` = base 20 com `Target[...]`), que era justamente um dos campos nao exportados.

O `Dwarven Aura` (pathID 2543235) e o terceiro caso do mesmo padrao, lido dos BYTES do asset
(o leitor offline nao converte esse objeto inteiro; ver o caveat acima): `Name = "Dwarven Aura"`,
`Duration = "3"`, descricao `"Your attacks have a [0]% chance to stun the target."`,
`DescriptionExpressions[0] = AttributeEffects[0].Amount = Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`
e um gatilho com `Condition = "Source.IsEnemy(Target)"` e **`Targets = "Cell.IsCurrentHex(Target)"`**
— o gatilho que o dump agora publica e que explica o "stun" que o RV-13b nao achava em acao nenhuma.

O `[Action]` do `Flame Aura Proc`/`Decay Aura Proc` continua fora do inventario de acoes (eles
nao sao concedidos por skill) — mas os efeitos deles passaram a sair **dentro do gatilho**
(`~acoes=Nome{ef=...}`), que e onde a pergunta se faz. Nao foi preciso varrer `Game.Actions`.

## Por que os CSVs de `docs/cobertura/` NAO ganharam coluna no RD-2

Decisao, com motivo (o pedido previa as duas saidas):

1. `docs/cobertura/status.csv` tem **13** colunas hoje; o header do `census.py` para `Status`
   tem **9**. As outras (`revisao`, `beneficio`, `dur`, `maxStk`) foram somadas pelo caminho
   proprio do projeto: imersores que escrevem o CSV NO LUGAR lendo o log
   (`tools/importa_beneficio.py` e o modelo; `censo_status.py`). Uma rodada do `census.py`
   REESCREVE o CSV com o header dele — ou seja, mexer no header do census e mexer no
   instrumento de revisao (schema), nao exportar campo, e o trabalho de revisao morre junto.
2. O log e a fonte que TODAS as ferramentas leem (`census.py`, `censo_status.py`,
   `importa_beneficio.py`, os `check_*`). Os campos novos saem la e chegam a uma coluna pelo
   mesmo caminho de sempre: um imersor (mesmo padrao do `importa_beneficio.py`).
3. `status.csv` e a ficha de revisao de TEXTO (nome/tipo/raridade/efeitos/classe/descricao);
   mecanica (gatilho/tick/aura) foi consumida dos assets e do log nas investigacoes — a
   coluna nao e onde esse dado se usa. Se a frente das auras quiser um `ganchos`, o lugar e
   um imersor, como no item 2.

## O que o dump de status GARANTE (RD-2F): falha de campo nao trunca

Ate 01/10 o `ActionStatusInventoryPatch` tinha **um unico** `try/catch`, em volta do laco dos statuses
INTEIRO, e o catch era um `LogWarning`: excecao em UM campo abortava o laco, o dump ficava **truncado
dali para diante** (o `_dumped` ja estava marcado — nao existia segunda passada, nao existia
retentativa) e o resto dos statuses sumia do log EM SILENCIO. O requisito era o oposto e nao estava
cumprido. Agora, campo a campo:

- **Todo campo da linha sai por `Campo(nome, leitura)`**
  (`RoguelikeDebugger/Patches/ActionStatusInventoryPatch.cs`). A leitura que estoura vira **marcador no
  proprio campo** — `!erro:<Tipo>` (ex.: `!erro:NullReferenceException`) — com um `LogWarning`
  nomeando o campo; a linha daquele status e TODAS as seguintes continuam saindo. O marcador nao tem
  `|`, aspas nem quebra de linha, entao o parser do censo nao quebra (os blocos que montam texto
  viraram lambda de `Campo`: `efeitos`, `efeitosDano`, `modelo`).
- **O laco itera uma COPIA da lista** (`new List<ActionStatusInfo>(__result)`): uma `Add` do jogo
  durante a iteracao (outro jeito de abortar o laco) nao derruba mais o dump.
- **O `catch` externo virou `LogError`** e diz que a falha foi FORA de campo, com o tipo e a mensagem:
  como campo problematico sai com marcador, chegar ali e o outro modo de falha (ex.: memoria) — e o
  SILENCIO e que nao pode existir.

Consequencia para quem le o dump: uma linha com `!erro:` e dado AUSENTE, nao valor; e o laco NAO deve
abortar — `[Status]` que para no meio continua sendo defeito, e o erro do catch externo e o que o
denuncia.

## Como estender sem quebrar o censo

1. Campo novo entra **antes** do `desc=` na linha (o parser do censo exige `desc` por ultimo).
2. Valor nunca com `|`, aspas ou quebra de linha — passe pelo saneador (`Limpa`).
3. Prefixo de categoria **estavel** e nome de campo fixo: e o que permite uma ferramenta ler.
4. Se o dado vier de um tipo concreto conhecido, prefira o padrao do `EfeitosInfo` (reflexao) em vez
   de cast: cast erra em silencio quando aparece um tipo novo, reflexao nao.
5. Campo novo que precise entrar nos CSVs de `docs/cobertura/` exige tambem a chave na whitelist de
   `tools/census.py` — senao ele aparece no **log** mas nao no CSV.
6. Verificacao: o dump sai no boot (nao precisa entrar em partida). Ler o `LogOutput.log` **na mesma
   sessao** — ele e truncado a cada inicio.
7. **A DLL do dump so aparece DEPOIS do deploy (ressalva declarada).** Editar o `.cs` de um patch NAO
   muda o dump: quem roda no jogo e a DLL em
   `<perfil>\BepInEx\plugins\RoguelikeDebugger\RoguelikeDebugger.dll`, e um `dotnet build` sem o
   target `DeployToBepInEx` nao a atualiza. O ciclo e `dotnet build` (que copia para o perfil) →
   abrir o jogo → ler o `LogOutput.log`. Campo novo que "nao aparece no log" quase sempre e uma DLL
   que nao chegou ao perfil — e o `-p:DeployToBepInEx=false` do empacotador builda **de proposito**
   sem instalar (por isso o `dotnet build` da publicacao nao serve para testar o dump).
