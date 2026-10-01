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
dado faltava. Era a causa das duas ultimas entradas "indeterminado" do censo.

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

> **Numeracao das linhas:** os `l.NNNN` desta tabela sao do decompilado **regerado em 01/10** com
> ilspycmd 8.2.0 (**496.253** linhas). As revisoes antigas (RV-13b, RV-19) citam outro decompile
> (`Assembly-CSharp.decompiled.cs`, 371.804 linhas, que nao esta mais no cache) — os numeros
> divergem; o nome do campo e a chave estavel para reconferir.

| campo no dump | campo do motor (decompilado `Assembly-CSharp.decompiled.cs`) | medicao |
|---|---|---|
| `expr=` | `ActionStatusInfo.DescriptionExpressions` (l.441015) | 138/421 |
| `danoExpr=` | `DamageExpressionOverrides` (l.441020) | 1/421 (`Chaos Curse`) |
| `refAcao=` / `refStatus=` | `TooltipDamageInfoRefAction` / `TooltipDamageInfoRefStatus` (l.441022/441024) | 19 / 7 |
| `tick=` | `TickTargets` (l.441035), `ActionsOnTickCondition` (441042), `ActionsOnTickTargets` (441045), `ActionsOnTick` (441047), `ActionsOnTickProcTriggers` (441049), `StatusEffectsOnTickCondition` (441052), `StatusEffectsOnTickTargets` (441055), `StatusEffectsOnTick` (441057), `StatusEffectsOnTickOverrides` (441059) | so `StatusEffectsOnTick`: 6/421 (`Freeze Earth`, `Ice Storm`, `Faerie Swarm`, `Blood Mist`, `Slow Poison Aura`, `The Bad Bloom`). Os outros campos: **0/421** — o `tick=-` de toda linha e a medida de que o proc das auras de shrine NAO passa por aqui |
| `auraSts=` | `AuraSourceStatus` / `AuraTriggerStatus` / `AuraTriggerStatusOverrides` (l.441108/441110/441112) | 40/421 — sempre junto de `IsAura=1` (os 40 batem; `IsAura` e o sinal barato do censo de auras). As auras de SHRINE **nao** estao nesses 40 |
| `trigEf=...~alvos=` | `SkillTrigger.Targets` (l.46590) | 39/421 statuses tem gatilho |

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
