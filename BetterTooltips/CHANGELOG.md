# Changelog — BetterTooltips

## 0.1.1

Conserto de **texto/rotulo** nos tooltips de shrine. **Nenhum numero, formula ou logica de calculo mudou** — a auditoria independente confirmou 9/9 dos valores das auras de buff (mais Flame e Decay).

- **RV-43 — a nota do `Fury` era a unica das 9 auras de shrine sem a base e sem a cadeia do bonus.** Causa: a chave `Damage increased by [0]%. Damage taken increased by [0]%. ` estava em `TextAppends` com a nota antiga do `RV-9` (so a frase de cura) — nao dizia que e aura de shrine, nao dava a base e nao citava o *Shrine Effect Bonus*. Conserto: a nota passou a `Base 25% damage and +25% damage taken. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).` e a **frase de cura ficou** (nao era falsa: o motor soma `DamageMod` a cura) — a nota agora tambem cobre o shrine. A base 25/25 sai do asset (`status.csv:205`: `DamageMod:Base:Mathf.Round(25 * (1 + Target["ShrineEffectBonus"]/100))` e o `DamageReduction` espelhado em -25). A chave continua **so** em `TextAppends`: o texto original do jogo nao mudou, entao nada migrou para `TextFixes` (a mesma chave nas duas tabelas derruba o mod — INC-1; `check_chave_compartilhada.py --estrito` = 0).
- **RV-43 — o rotulo de `ManaCostMod` (Energy Coil) quebrava com total POSITIVO.** Causa: `Format` fazia `"Mana Costs reduced by " + (-v)`, assumindo total negativo. Existem fontes POSITIVAS reais do mesmo atributo — `Forbidden Power` `ManaCostMod:Base:50` (`status.csv:191`) e `Fuel for the Flames I/II` +20/+30 (`skills.csv:178-179`): um personagem de Fire com +70 dentro do Energy Coil (-50) tem total **+20** e a linha imprimia `Mana Costs reduced by -20%`. Conserto: total <= 0 = `Mana Costs reduced by |v|`; total > 0 = `Mana Costs increased by v`.
- **RV-43 — a mesma classe de sinal nos outros atributos (defeito latente).** Causa: `DamageMod`, `CritChance`, `DodgeChance`, `LifeOnHit`, `HealthPerTurnPercent` e `ManaPerTurnPercent` montavam `+` fixo e imprimiriam `+ -X%` com total negativo. Conserto: todos passam pelo mesmo helper de sinal (`+` para positivo/zero, `−` para negativo), no formato do rotulo de atributo desconhecido. **O texto do total positivo — o comportamento correto de hoje — nao mudou.**
- **RV-43 — a nota do `Flame Shrine` se contradizia.** Causa: a nota afirmava que a vida maxima usada nao era a de quem esta na aura, mas a lista por alvo usa exatamente o `MaxHealth` do ocupante — o mod projeta cada ocupante COMO SE fosse o atacante, porque no hover nao se sabe quem vai atacar (hipotese explicita, aceita pelo dono). Conserto: a clausula agora diz `the number is the projection of THIS character as the attacker - if this character attacked` e a frase contraditoria saiu; a escala, a marca "antes das reducoes" e a origem do bonus ficaram como estavam.
- **Versao:** 0.1.0 -> **0.1.1** nos tres lugares (`<Version>` do `.csproj`, `version_number` do `manifest.json`, literal do `[BepInPlugin(...)]` no `Plugin.cs`).

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
