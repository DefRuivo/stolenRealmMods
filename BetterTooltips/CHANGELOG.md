# Changelog — BetterTooltips

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
