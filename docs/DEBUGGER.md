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

## Backlog auditado (o que falta exportar)

Da auditoria das auras (`docs/cobertura/revisao/RV-19-shrines.md`, secao 7), conferido no codigo
hoje — **zero ocorrencias** no debugger:

- `ActionsOnTick`, `ActionsOnTickCondition`, `ActionsOnTickTargets`
- `StatusEffectsOnTick*`
- `AuraSourceStatus`, `AuraTriggerStatus`
- `TickTargets`
- `DamageExpressionOverrides` (este **ja** e exportado — 5 ocorrencias)

Correcao da propria revisao: `SkillTriggers` **ja** era exportado; o que faltava era o campo
`Targets`, que **nao existe** em `SkillTrigger`. Registrado para ninguem pedir campo inexistente.

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
