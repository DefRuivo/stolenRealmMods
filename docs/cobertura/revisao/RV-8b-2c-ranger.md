# RV-8b-2c — lote **Ranger** (40 skills) · 29/09

> Primeiro lote feito com a bancada pronta (`tools/verify_tree.py`), o que permitiu
> confrontar **texto × código** skill por skill em vez de ler prosa. Método de
> triangulação do projeto: **≥2 fontes independentes + coerência com o código, e o
> código vence em divergência**.

## Resultado: 40 skills

| veredito | quantas |
|---|---:|
| `revisado` (texto confirmado pelo código e coerente com a wiki) | **21** |
| `corrigido` (defeito de grafia/espaço achado no lote 2a) | **16** |
| **aberto** (o texto afirma algo que nenhuma fonte fecha) | **3** |

## Onde o CÓDIGO ganhou da wiki (a wiki é da v.19 e está velha)

A wiki deu o segundo lado para quase tudo, mas em três casos ela **contradiz o jogo
atual** — e o código manda:

| Skill | Wiki (v.19) | Jogo agora | Quem está certo |
|---|---|---|---|
| `Patient Hunter` | "10% Increased Damage per stack" | status: *"Damage increased by 10%, **Range increased by 1** per stack"* (`DamageMod:10, RangeTypeAdderRanged`) | **a tooltip** — a wiki omite o alcance |
| `Stalker's Mark` | 20% dano / 10% crítico | status: `DamageMod:25, CritChance:12` | **a tooltip** (25%/12%) |
| `Crippling Shot` | aplica **Crippled** | aplica **Slow** (`MovementCostPerHexMod:Set:100` → "Movement costs doubled") | **a tooltip** — o status foi trocado depois da v.19 |

Também: a wiki lista `Impaling Shot` e `Call of the Wild`, que **não existem** mais na
árvore atual, e não tem `Cupid Shot` nem `Force Shot` — sinal claro de que ela parou
na v.19.

## Os 3 abertos — o que falta para fechar

Nenhum é "suspeito de bug": são afirmações que **não têm como ser conferidas com o dump
de hoje**, porque não são `AttributeEffects` nem `DescriptionExpressions` — são
propriedades da **ação** (quantos alvos, quanto movimento, escala por hex).

| Skill | Tooltip diz | Wiki diz | Por que ficou aberto |
|---|---|---|---|
| `Rally` | movimento **+3** | **+2** | o efeito é nos aliados (não entra no `attr` do caster) |
| `Volley` | até **5** alvos | até **3** | é um limite de alvos da ação |
| `Marked Prey` | "**Attacks** now apply…" | "**Basic attacks** now apply…" | a wiki diz básico, a tooltip diz qualquer ataque; o gatilho está no `SkillTrigger`, que o dump **não trazia à época** — o RD-2R passou a publicar `SkillTriggers[].Targets` (`~alvos=`, ver `docs/DEBUGGER.md`), então dá para reconferir hoje |

O `Marked Prey` é o mais relevante dos três: se o gatilho for só ataque básico, a
tooltip **promete mais do que o jogo faz** — que é justamente o defeito que este RV
existe para achar. Os outros dois são divergência de número.

## Habilitador que isso revelou — `RV-8b-0f`

Para fechar os 3 (e a mesma classe em outras árvores) o dump precisa das **propriedades
da ação**: limite de alvos, movimento concedido, knockback/alcance e a escala por hex
(há um campo `RangeAdderAttributes` no `ActionInfo` que cheira a isso). É a diferença
entre "não verificável" e "verificado" para tudo que não é atributo.

## Fontes usadas

- Wiki, árvore Ranger — https://stolen-realm.fandom.com/wiki/Ranger_Skill_Tree
  (**v.19, desatualizada** — usar só como segunda opinião, nunca como verdade)
- Wiki, Status Effects (fechou `Marked Prey`) — https://stolen-realm.fandom.com/wiki/Status_Effects
- Patch notes datados (SteamDB) — https://steamdb.info/patchnotes/8583704 (v0.17),
  https://steamdb.info/patchnotes/9906437 (v0.20)
  → Nota útil: o v0.17 mudou `Quick Hands` para **100%**, mas a wiki da v.19 e a tooltip
  atual dizem **50%** — ou seja, houve mudança posterior; a tooltip está coerente com a v.19.

## Próximo lote

Ordem por tamanho: **Nature 39 → Warrior 39 → Thief 38 → Light 36 → Monk 36 → Chaos 33 →
Fire 32 → Cold 31 → Lightning 30 → Basic 15 → Innate 10** (Bard intocável).
Receita: `python tools/verify_tree.py <arvore>` → ler a ficha → triangular → marcar.
