# Changelog — BetterTooltips

## RV-46 (30/09) — os dois defeitos da linha azul das auras de shrine (saiu na **0.1.1**, no ar desde 01/10)

> **Historico do titulo:** esta secao nasceu como "Nao publicado" (bc394e7, 30/09) — e o RV-46 era mesmo
> inedito quando a nota foi escrita; o que envelheceu foi o titulo. O RV-46 foi empacotado dentro da
> **0.1.1** (publicada em 01/10/2026, substituindo a 0.1.0) e o zip publicado carrega este changelog
> verbatim, com `AurasUnicas`, `RV-46` e `instancias=` na DLL.

Conserto de **dois defeitos** na linha `Your active shrine auras:`. **Nenhuma formula de dano, nenhuma
convencao de formatacao (o Ceil do RV-45, o sinal unico do 46acd97) e nenhuma das 12 notas de texto
mudaram** — o que mudou foi QUAL numero entra em cada item e QUAIS auras viram item.

- **RV-46 — a contribuicao das auras estava MULTIPLICADA (`Dodge +120%` com a aura valendo 40).** Causa
  provada: `AurasVivas` devolve TODAS as entradas de `Character.ActionStatuses` que casam com a familia e
  a contribuicao somava por ENTRADA — e a lista viva carrega a **MESMA aura repetida**, porque cada
  (re)entrada na area do ground effect cria um status NOVO (`GroundEffect.AddGroundEffectedPlayer`) e o
  motor so remove status `Infinite` (a aura do shrine nao e). No log do jogo do dono (30/09) o mesmo hover
  mostra a lista com `Rogue Aura` **tres** vezes e `aura=+120%`, com o `RV-44 soma` dizendo `stacks=1` em
  cada instancia: 3 × 40. **Nao era stack.** Conserto: a contribuicao conta **cada aura UMA vez**
  (`AurasUnicas`) — 40, que e o numero da linha branca do proprio shrine e o que o motor avalia na
  expressao do asset. **O total continua o do motor** (`Character[atributo]`): ele para em 75 porque os
  atributos do jogo tem TETO (`CharacterAttribute.HasMax`; `DodgeChance` **MaxValue 75** e
  `DamageReduction` **MaxValue 50** no asset) e o motor corta o total ali (`Character.GetAttribute`).
  As repeticoes e o teto vao para o LOG (`instancias=[Nome xN]`, `RV-46 teto`), nunca para o numero.
- **RV-46 — aura viva fora da lista: o Dwarven nao aparecia.** Causa: os itens saem por ATRIBUTO de
  personagem e o efeito do Dwarven **nao e atributo** — o valor mora na **chance do gatilho**
  (`OnHittingDamaging` -> `Stunned`, `SkillTriggers[].ActionStatusChanceEquations`): no asset
  (`Dwarven Totem Aura Status`, `resources.assets` @1517115056) a formula
  `Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))` aparece 2× (@1517115395, ao lado da
  descricao, e @1517115647, dentro do gatilho) e o valor com `Worship` e 40 — o mesmo da linha branca do
  shrine. Conserto: item proprio **`Stun chance +40%`**, avaliado pelo motor com o personagem em foco.
  Pela mesma regra entraram as outras duas das 12 auras sem atributo de personagem: Decay
  (`Shadow damage per turn N`) e Flame (`Fire damage to attackers: …`).
- **Regra que fica (dono, 30/09):** a linha se chama "Your active shrine auras" e se apresenta como
  COMPLETA — aura viva que nao virar item sai no LOG com o motivo (`RV-46 AVISO`), nunca em silencio.
- **Conferencia mecanica:** `tools/checa_shrines.py` passou a ler o campo `instancias=`, os itens sem
  atributo e o `RV-46 teto`; o caso do **Dwarven deixou de ser `NAO-VER`** (compara o item com a coluna
  `contribuicao_esperada` da tabela) e o hover com varias auras (o do print do dono) passa a ser
  conferivel. Contra-prova em `tools/fixtures/shrines-rv46-dedupe.log` (exit 0).

## 0.1.1

Conserto de **texto/rotulo** nos tooltips de shrine (RV-43). **Nenhum numero, formula ou logica de calculo mudou NESTES consertos de texto** — a auditoria independente confirmou 9/9 dos valores das auras de buff (mais Flame e Decay). **A 0.1.1 que está no ar leva mais que rotulo:** o RV-44 (bullet abaixo) e o RV-46 (secao acima) entraram nesta MESMA versao e mudaram QUAL numero entra na linha — a versao nao subiu de novo; a frase "nada de calculo mudou" envelheceu e vale só para os consertos de texto.

- **RV-43 — a nota do `Fury` era a unica das 9 auras de shrine sem a base e sem a cadeia do bonus.** Causa: a chave `Damage increased by [0]%. Damage taken increased by [0]%. ` estava em `TextAppends` com a nota antiga do `RV-9` (so a frase de cura) — nao dizia que e aura de shrine, nao dava a base e nao citava o *Shrine Effect Bonus*. Conserto: a nota passou a `Base 25% damage and +25% damage taken. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).` e a **frase de cura ficou** (nao era falsa: o motor soma `DamageMod` a cura) — a nota agora tambem cobre o shrine. A base 25/25 sai do asset (`status.csv:205`: `DamageMod:Base:Mathf.Round(25 * (1 + Target["ShrineEffectBonus"]/100))` e o `DamageReduction` espelhado em -25). A chave continua **so** em `TextAppends`: o texto original do jogo nao mudou, entao nada migrou para `TextFixes` (a mesma chave nas duas tabelas derruba o mod — INC-1; `check_chave_compartilhada.py --estrito` = 0).
- **RV-43 — o rotulo de `ManaCostMod` (Energy Coil) quebrava com total POSITIVO.** Causa: `Format` fazia `"Mana Costs reduced by " + (-v)`, assumindo total negativo. Existem fontes POSITIVAS reais do mesmo atributo — `Forbidden Power` `ManaCostMod:Base:50` (`status.csv:191`) e `Fuel for the Flames I/II` +20/+30 (`skills.csv:178-179`): um personagem de Fire com +70 dentro do Energy Coil (-50) tem total **+20** e a linha imprimia `Mana Costs reduced by -20%`. Conserto: total <= 0 = `Mana Costs reduced by |v|`; total > 0 = `Mana Costs increased by v`.
- **RV-43 — a mesma classe de sinal nos outros atributos (defeito latente).** Causa: `DamageMod`, `CritChance`, `DodgeChance`, `LifeOnHit`, `HealthPerTurnPercent` e `ManaPerTurnPercent` montavam `+` fixo e imprimiriam `+ -X%` com total negativo. Conserto: todos passam pelo mesmo helper de sinal (`+` para positivo/zero, `−` para negativo), no formato do rotulo de atributo desconhecido. **O texto do total positivo — o comportamento correto de hoje — nao mudou.**
- **RV-43 — a nota do `Flame Shrine` se contradizia.** Causa: a nota afirmava que a vida maxima usada nao era a de quem esta na aura, mas a lista por alvo usa exatamente o `MaxHealth` do ocupante — o mod projeta cada ocupante COMO SE fosse o atacante, porque no hover nao se sabe quem vai atacar (hipotese explicita, aceita pelo dono). Conserto: a clausula agora diz `the number is the projection of THIS character as the attacker - if this character attacked` e a frase contraditoria saiu; a escala, a marca "antes das reducoes" e a origem do bonus ficaram como estavam.
- **RV-44 — a linha `Your active shrine auras:` mostrava o TOTAL do personagem, não o que as auras entregam.** Causa (provada no código): o item saía direto do indexador do motor, `Character[atributo]` (`ShrineAuraPatch.cs`, `AcumuladoShrines` — era `float valor = receptor[nome];`), que é o total final da ficha (base + gear + skills + auras). Numa aura de 25% a linha dizia o total do personagem, o que na tela lê como "a aura dá 50%". Prints do dono (30/09): Goblin Battle Standard (Fury) sem `Worship` -> tooltip do shrine `25%` / linha `Damage +50%` e `Damage taken +5%`; com `Worship` -> `50%` / `Damage +75%` e `Damage taken +30%`; Rogue Shrine com `Worship` -> tooltip `40%` / linha `Dodge +57%`. Conserto: cada item passou a ser **`<o que as auras entregam> (total <o total do personagem>%)`** — `Damage +25% (total +50%)`, `Damage taken +25% (total +5%)`, `Dodge +40% (total +57%)` —, com a contribuição saindo do **`AttributeEffects` real de cada aura VIVA** (a MESMA expressão que o tooltip do shrine mostra: `Mathf.Round(20 * (1 + Target["ShrineEffectBonus"]/100))` etc., avaliada pelo motor), e **duas auras no mesmo atributo somam as contribuições** (Warrior + Fury em `Damage`), nunca o total da ficha. O total continua entre parênteses, lido do indexador: é o número da ficha (BetterStats). **Nenhuma fórmula de aura, texto ou nota mudou** — a nota do Rogue (`Increases dodge chance by [0]%.` -> `Base 20%. The value shown already includes the Shrine Effect Bonus (...)`) é a mesma da 0.1.1 e continua correta na tela. Fallback: sem contribuição separável (efeito `Multiplicative`/`Set` — a família não tem nenhum: as 9 auras de buff, todas as que têm `AttributeEffects`, são `Base`), o item sai com o total, como antes.
- **Versão:** 0.1.0 -> **0.1.1** nos três lugares (`<Version>` do `.csproj`, `version_number` do `manifest.json`, literal do `[BepInPlugin(...)]` no `Plugin.cs`).

## 0.1.0

Primeira versão publicada.

- **Reescreve tooltips de skills e status que eram omitidos**: quando o texto oficial esconde algo que muda a decisão do jogador (de que atributo depende o número, limite de stacks, duração, quem é afetado, gatilho, número de golpes), a explicação que falta é acrescentada ao fim do tooltip.
- **Corrige defeitos objetivos de texto** — grafia (`benefical`, `additonal`), pontuação e espaço duplo — por tabela de correção casada pelo texto exato.
- A nota de mecânica entra na **cor de texto especial do próprio jogo** e é posicionada **depois dos custos e do alcance**, no fim do corpo do tooltip.
- **Sem qualquer alteração de gameplay**: o mod só reescreve strings no funil de localização (`OptionsManager.Localize`).

### Números dinâmicos de shrine

O texto do jogo para as auras de shrine mostrava **sempre o valor base**, mesmo para quem tinha o bônus que multiplica a aura. O mod passou a calcular com o **bônus real do personagem em foco** (30/09):

- **Auras de buff (as 12 chaves da família)**: o valor da linha sai já multiplicado pelo *Shrine Effect Bonus* do personagem — **Omnism I/II** (Chaos), o perk **`Worship`** do Worshiper (`100% increased effect from Shrines`) e o **Horn of Devotion**. Uma base fixa de `20%` deixa de ser exibida como `20%` para quem tem o bônus.
- **Linha `Your active shrine auras:`**: um bloco próprio (na cor especial do jogo) que lista **todas as auras de shrine vivas no personagem em foco**, um item por atributo. Ela só aparece para quem **está de fato** dentro da aura — quem está fora não vê linha nenhuma. O valor lido é o total final do personagem (`Character[atributo]`), o mesmo número que a ficha mostra: o mod **não soma nem aplica o fator por fora**.
- **Decay Shrine — dano por turno com número**: a linha `Take [0]% of your Max Health in Shadow Damage per turn.` ganha o **dano literal** ao lado (ex.: `20 damage per turn for you`), calculado com a **vida máxima** e o **Shrine Effect Bonus** do próprio personagem (com `Worship`, o dobro).
- **Flame Shrine — dano por alvo**: no hover ainda não se sabe **quem vai atacar**, então um número único por atacante é impossível (limitação do jogo). O que sai é a lista de **cada personagem que está na área da aura** (party e inimigos), com o dano calculado sobre a vida máxima, o **tipo** e o **bônus dele**.
- **Fator do `Worship`**: com o perk `Worship` o dano das duas auras de perigo **dobra**. Isso foi **medido em jogo** pelo autor (30/09) — a mesma aura vale 10% para um personagem e 20% para o Worshiper. O `Source` vazio do shrine deixou de ser usado na conta: o fator é lido do **próprio personagem avaliado**.
- **Marca "antes das reduções"**: as duas notas (Decay e Flame) começam com **`Raw damage, before damage reduction:`** e dizem que o fator já está incluído — sem armadura, resistência ou qualquer mitigação posterior.
- **Cura dinâmica do `Sustenance I/II`**: o tooltip de todo **globule** (Health, Mana, Cleansing, Energy, Power, Refreshing) e dos **pickups de poção** (Minor / Healing / Major, vida e mana) passa a mostrar a cura real, sobre a vida e a mana máximas do personagem em foco. A porcentagem sai das tiers que **o jogo tem ativas** (`Character.Skills`, já resolvida por `SkillsThatReplace`): 8% com só a I, 20% com só a II (se a II substitui a I) ou 28% com as duas (se não substitui) — o mod não decide qual é o caso, ele mostra o que está ativo.
- **Quando não há prova, o texto do jogo fica intacto**: atributo ausente neste build, personagem fora da aura ou expressão não avaliável = **nenhum número** é exibido e o log diz o motivo. O mod não estima.

### Não entra neste mod

- A árvore do **Chaos** é omitida de propósito: ela sorteia um resultado e o texto não revela quais são — é a graça da árvore, não um defeito.
- O mod **não mostra número quando não há prova** — prefere deixar o texto original a inventar um valor.
- O mod **não aplica mitigação** ao número que exibe: ele é o cru da fórmula do jogo.

### Conferência

Os números foram escritos contra o decompilado e os assets do jogo. O **fator do `Worship` (o dano dobra)** foi **medido em jogo** pelo autor em 30/09. O que falta é a **conferência visual final em jogo** das linhas novas (a linha do Decay, a lista do Flame e o bloco `Your active shrine auras:`) depois da última revisão — o conjunto de tooltips de shrine ainda não foi revalidado olhando a tela.
