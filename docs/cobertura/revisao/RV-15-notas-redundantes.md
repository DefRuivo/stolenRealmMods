# RV-15 - Notas redundantes / duplicadas nos tooltips

Gerado por `tools/check_notas_redundantes.py` a partir de `BetterTooltips/Patches/LocalizePatch.cs`.

O que a ferramenta **gera** termina na linha `<!-- fim-gerado -->`; tudo o que vier
depois dela e escrito a mao e **nunca** e reescrito (ver `tools/preserva_curado.py`).

Uma nota existe para dizer o que o texto **nao** diz. Quando ela repete o proprio texto,
o jogador le a mesma frase duas vezes e a explicacao perde credito - foi o que o usuario
reportou em 30/09 (`Blinding Lights` duplicado, `Blind`/`Sleep` redundantes,
`Praying Shot`/`Chok` na mesma familia).

## Resumo

| caso | quantas | o que significa |
|---|---|---|
| nota == chave | **0** | texto e nota sao a MESMA frase: aparece duplicado na tela |
| nota contida na chave | **0** | a nota inteira ja esta no texto: nao acrescenta nada |
| nota ecoa >= 6 palavras da chave | **0** | repete o inicio do texto em sequencia |
| notas unicas (OK) | 197 | dizem algo que o texto nao diz |
| nota **sem o tom do nivel 2** (COR-1/COR-2) | **0** | sai no tom do corpo do tooltip em vez do tom das explicacoes |

Total de notas analisadas: **197** (mais **24** valor(es) de `TextFixes` com cor, com
**25** bloco(s) de nota do nivel 2; o resto e a linha do jogo com o markup dela).

A convencao dos tres niveis de cor (branco / tom mais escuro / azul), com a procedencia
declarada de cada cor, esta em [`docs/TEXTO-TOOLTIPS.md`](../../TEXTO-TOOLTIPS.md).

## 1. Nota identica a chave (DUPLICADO na tela)

Nenhum caso. 

## 2. Nota inteiramente contida na chave (redundante)

Nenhum caso. 

## 3. Nota que ecoa o texto

Nenhum caso. 

## 4. Nota sem o tom do nivel 2 (COR-1; cobertura fechada no COR-2)

O que a trava olha (COR-2, 01/10): **todo** valor de `TextAppends` e **todo** valor de
`TextFixes`, em **qualquer** formato de cor — a primeira versao so olhava as notas
fundidas no formato `\n\n<color=#...>` e deixava 10 das 21 entradas com cor de fora
(duas delas notas de SHRINE). Regras:

- cor no valor que **nao** seja `#C8B090` e que o **jogo nao tenha escrito na chave** -> caso;
- cor que o jogo ja escrevia na chave (o `#808080` de citacao dos status) -> **legitima**;
- valor que e, no mesmo texto, a correcao da linha do jogo **e** a nota (`explicacao E
  efeito`) -> a parte corrigida nao ganha cor, a nota carrega o marcador.

Conferido nesta execucao: **197** valor(es) de `TextAppends`, **24** valor(es) de
`TextFixes` com cor (**25** bloco(s) de nota do nivel 2).

Nenhum caso: toda nota acrescentada pelo mod carrega o marcador `#C8B090` ou uma cor que
o proprio jogo escreveu (a cor de explicacao e resolvida em runtime pelo campo
`Tooltip.specialDescColor`, lido pelo gancho das notas — ver §7 da convencao).

## 5. Comprimento das notas (medida — NAO reprova)

Notas com **quebra de linha interna** (o que o dono chama de parede de texto) e o
comprimento de cada uma. O criterio esta em `docs/TEXTO-TOOLTIPS.md` §4: comprimento nao
reprova (as notas aprovadas pelo dono tem tamanhos diferentes); a cor nao muda nenhum
comprimento. Quem decide encurtar e o dono.

| notas medidas | com quebra interna | maior nota (caracteres) |
|---|---|---|
| 220 | **49** | 302 |

- **302 car., 2 quebra(s)** — `TextFixes` — Gain the ability to shapeshift into a powerful elemental @Dr
  - Shapeshift into a powerful elemental Dragonkin. Empowers basic attack, grants new abilities, and resistance based on the color you choose. Increases Armor by [0]. / Scales with your character level. /

- **277 car., 2 quebra(s)** — `TextFixes` — Movement increased by 3 Action Points increased by 1 Max Hea
  - Movement increased by 3. Action Points increased by 1. Max Health reduced by 25%. Damage reduced by 25%. / Also reduces the healing this character does by the same percentage. / Current health is redu

- **258 car., 2 quebra(s)** — `TextAppends` — RV-9 buffs: Overflowing Energy - Power of Mana increases the
  - Power of Mana increases the damage and healing of abilities that cost Mana. / It does not change how much Mana they cost, it does nothing for abilities that cost no Mana, / and it does not change the 

- **258 car., 2 quebra(s)** — `TextAppends` — "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lug
  - Power of Mana increases the damage and healing of abilities that cost Mana. / It does not change how much Mana they cost, it does nothing for abilities that cost no Mana, / and it does not change the 

- **258 car., 2 quebra(s)** — `TextAppends` — "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lug
  - Power of Mana increases the damage and healing of abilities that cost Mana. / It does not change how much Mana they cost, it does nothing for abilities that cost no Mana, / and it does not change the 

- **258 car., 2 quebra(s)** — `TextAppends` — "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lug
  - Power of Mana increases the damage and healing of abilities that cost Mana. / It does not change how much Mana they cost, it does nothing for abilities that cost no Mana, / and it does not change the 

- **240 car., 3 quebra(s)** — `TextFixes` — Increases damage dealt and max life by 15%. Increases damage
  - Increases damage dealt and max health by 15%. Increases damage taken by 15%. /  / Current health is increased by the same percentage and goes back down when the status ends. / Also increases the heali

- **237 car., 5 quebra(s)** — `TextAppends` — Summons a Bear, Moose, or Panther to fight for you.
  - One is summoned at random: / - Bear (a Grizzly): Stunning Slam, Wild Cleave / - Moose: Melee Attack, Ground Slam / - Panther: Melee Attack, Shadow Walk / Does not copy your attributes. / Your Might ra

- **219 car., 5 quebra(s)** — `TextAppends` — Fonte: os assets do jogo, via dump. `ActionInfo.Summons` é a
  - One is summoned at random: / - Raven: Melee Attack, Evasion / - Raccoon: Melee Attack, Steal Action / - Coyote: Melee Attack, Cripple / Does not copy your attributes. / Your Might raises its damage; y

- **212 car., 5 quebra(s)** — `TextAppends` — Summons a Stag, Wolf, or Boar to fight for you.
  - One is summoned at random: / - Stag: Melee Attack, Stunning Kick / - Wolf: Melee Attack, Howl / - Boar: Melee Attack, Fracture / Does not copy your attributes. / Your Might raises its damage; your Int

- **208 car., 2 quebra(s)** — `TextFixes` — Devour the life force of all enemies within 2 hexes dealing 
  - Devour the life force of all enemies within 2 hexes dealing *0 Shadow Damage and giving you 10% Max Health for each enemy effected. /  / Each stack grants another 10% Max Health; you gain one stack pe

- **194 car., 3 quebra(s)** — `TextFixes` — Summon a skeletal mage to fight by your side.
  - Raise a skeletal mage to fight by your side. / Skeletal Mage: Frost Nova, Fireball, Twister, Ghost Armor / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **193 car., 3 quebra(s)** — `TextFixes` — Raise a Undead Wizard to fight by your side.
  - Raise an Undead Wizard to fight by your side. / Undead Wizard: Bone Explosion, Consumption, Ghost Armor / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **181 car., 2 quebra(s)** — `TextAppends` — Restores *0 health to all allies within 2 hexes of target.
  - Healing scales with your Attack Power and Holy Power. / Reduced by effects that lower the target's healing received. / The 2-hex area is centred on the chosen TARGET, not on the caster.

- **180 car., 2 quebra(s)** — `TextFixes` — Removes all negative statuses from friendly target but infli
  - Removes all negative statuses from friendly target but inflicts 10% of target's max health as fire damage. Can be used when Disabled. /  / This cannot reduce the target below 1 health.

- **178 car., 3 quebra(s)** — `TextFixes` — Summon a skeletal warrior to fight by your side.
  - Raise a skeletal warrior to fight by your side. / Skeletal Warrior: Melee Attack, Cleave / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **169 car., 3 quebra(s)** — `TextFixes` — Summon a skeletal archer to fight by your side.
  - Raise a skeletal archer to fight by your side. / Skeletal Archer: Ranged Attack / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **166 car., 3 quebra(s)** — `TextFixes` — Summons a Timber Wolf to fight for you
  - Summons a Timber Wolf to fight for you. / Timber Wolf: Melee Attack, Cripple / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **164 car., 3 quebra(s)** — `TextFixes` — The caster reaches out in aid healing 30% of target's maximu
  - The caster reaches out in aid healing 30% of target's max health. /  / Healing scales with your Holy Power. / Reduced by effects that lower the target's healing received.

- **164 car., 3 quebra(s)** — `TextFixes` — Raise a Mighty Iron Golem to fight for you.
  - Raise a Mighty Iron Golem to fight by your side. / Iron Golem: Ground Slam / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **162 car., 1 quebra(s)** — `TextAppends` — RV-9 buffs: Overgrow - Current health is increased by the sa
  - Current health is increased by the same percentage and goes back down when the status ends. / Also increases the healing this character does by the same percentage.

- **159 car., 3 quebra(s)** — `TextFixes` — Maximum health increased by 25% Deals more damage at lower h
  - Max health increased by 25% Deals more damage at lower health /  / Lasts 3 turns. / The bonus is your missing health as a percentage: up to +100% damage at 1 health.

- **150 car., 3 quebra(s)** — `TextFixes` — Increases damage dealt by 25%. Increases max life and damage
  - Increases damage dealt by 25%. Increases max health and damage taken by 15%. /  / Lasts 3 turns. / Also increases the healing you do by the same percentage.

- **140 car., 1 quebra(s)** — `TextAppends` — RV-9 buffs: Patient Hunter - Gains a stack at the end of you
  - Gains a stack at the end of your turn, and moving removes the status. / Also increases the healing this character does by the same percentage.

- **137 car., 2 quebra(s)** — `TextAppends` — Raise an Undead Ranger to fight by your side.
  - Undead Ranger: Ranged Attack, Hide In Shadows / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **135 car., 3 quebra(s)** — `TextFixes` — @Maximum health@ and @Damage Dealt@ increased by 6% per stac
  - Max health and Damage Dealt increased by 6% per stack. /  / Stacks up to 5 times. / Also increases the healing you do by the same percentage.

- **135 car., 1 quebra(s)** — `TextAppends` — Expel a powerful celestial light blinding enemies and dealin
  - Damage and healing scale with your Attack Power and Holy Power. / Healing is reduced by effects that lower the target's healing received.

- **135 car., 1 quebra(s)** — `TextAppends` — Breathe out a stream of holy light dealing *0 holy damage to
  - Damage and healing scale with your Attack Power and Holy Power. / Healing is reduced by effects that lower the target's healing received.

- **132 car., 2 quebra(s)** — `TextFixes` — @Maximum health@ and @maximum mana@ increased by 10%. @Damag
  - Max health and max mana increased by 10%.  Damage dealt increased by 10%. /  / Also increases the healing you do by the same percentage.

- **131 car., 2 quebra(s)** — `TextFixes` — Maximum health reduced by 15%.
  - Max health reduced by 15%. /  / Current health is reduced by the same percentage and comes back when the status ends. This cannot kill.

- **127 car., 2 quebra(s)** — `TextAppends` — Summons a Dire Wolf to fight for you.
  - Dire Wolf: Melee Attack, Blood Howl / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **127 car., 2 quebra(s)** — `TextAppends` — Summon a grizzly to fight your enemies.
  - Grizzly: Stunning Slam, Wild Cleave / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **125 car., 2 quebra(s)** — `TextAppends` — Raise an Undead Berserker to fight by your side.
  - Undead Berserker: Bleeding Cleave / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **123 car., 2 quebra(s)** — `TextAppends` — Summons a Tundra Wolf to fight for you.
  - Tundra Wolf: Melee Attack, Howl / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **120 car., 2 quebra(s)** — `TextAppends` — Summon a Raven to fight your enemies. 
  - Raven: Melee Attack, Evasion / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **116 car., 2 quebra(s)** — `TextAppends` — Summon a wolf to fight your enemies.
  - Wolf: Melee Attack, Howl / Does not copy your attributes. / Your Might raises its damage; your Intelligence, its health.

- **114 car., 1 quebra(s)** — `TextAppends` — Touch of Chaos: REVERTIDO a pedido do usuario (29/09). A arv
  - Healing scales with your Attack Power and Holy Power. / Reduced by effects that lower the target's healing received.

- **114 car., 1 quebra(s)** — `TextAppends` — Target restores *0 health per turn. 
  - Healing scales with your Attack Power and Holy Power. / Reduced by effects that lower the target's healing received.

- **114 car., 1 quebra(s)** — `TextAppends` — All allies within 3 hexes of you heal for *0 per turn. 
  - Healing scales with your Attack Power and Holy Power. / Reduced by effects that lower the target's healing received.

- **113 car., 1 quebra(s)** — `TextFixes` — Increases damage and summon damage by 10%
  - Increases damage and summon damage by 10%. / Also increases the healing this character does by the same percentage.

- **106 car., 1 quebra(s)** — `TextFixes` — Recover [0]% of maximum health each turn. 
  - Recover [0]% of max health each turn.  / Base 10%; the value shown already includes the Shrine Effect Bonus.

- **104 car., 1 quebra(s)** — `TextFixes` — Recover [0]% of maximum mana each turn. 
  - Recover [0]% of max mana each turn.  / Base 10%; the value shown already includes the Shrine Effect Bonus.

- **103 car., 2 quebra(s)** — `TextFixes` — @Maximum health@ reduced by 20%.
  - Max health reduced by 20%. /  / Each stack grants another 10% Max Health; you gain one stack per enemy hit.

- **103 car., 2 quebra(s)** — `TextFixes` — @Maximum health@ reduced by 10%.
  - Max health reduced by 10%. /  / Each stack grants another 10% Max Health; you gain one stack per enemy hit.

- **97 car., 1 quebra(s)** — `TextAppends` — Restores the target to full health.
  - Healing scales with your Holy Power. / Reduced by effects that lower the target's healing received.

- **95 car., 1 quebra(s)** — `TextFixes` — Ranged spells deal damage the closer you are. Calculates how
  - Increases damage by 50%. / Also increases the healing this character does by the same percentage.

- **72 car., 1 quebra(s)** — `TextAppends` — RV-9 buffs: Destructive - Lasts 3 turns. Also increases the 
  - Lasts 3 turns. / Also increases the healing you do by the same percentage.

- **72 car., 1 quebra(s)** — `TextAppends` — RV-9 buffs: Blood Frenzy - Lasts 2 turns. Also increases the
  - Lasts 2 turns. / Also increases the healing you do by the same percentage.

- **72 car., 1 quebra(s)** — `TextAppends` — RV-9 buffs: Battle Fury - Lasts 3 turns. Also increases the 
  - Lasts 3 turns. / Also increases the healing you do by the same percentage.

<!-- fim-gerado -->
