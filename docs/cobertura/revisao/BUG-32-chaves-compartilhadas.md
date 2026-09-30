# BUG-32 — Varredura de CHAVE COMPARTILHADA (nota que mente para outros donos)

Ferramenta: **`tools/check_chave_compartilhada.py`** (novo, stdlib, somente leitura)
Rodada de referência: **30/09/2026**, contra `docs/cobertura/*.csv`.
Fonte das chaves: `BetterTooltips/Patches/LocalizePatch.cs` (lido em modo leitura — **nenhum arquivo existente foi alterado**; este relatório e a ferramenta são as únicas criações).

---

## 1. O defeito que esta varredura cobre

O BetterTooltips corrige tooltips (`TextFixes`) e acrescenta notas (`TextAppends`) por **chave de TEXTO**, não por entidade. O lookup é pelo texto exato da frase — e o **mesmo texto pode servir a várias entidades do jogo** (skills, status, itens, afixos, powerups). Uma nota escrita para um dono passa a aparecer no tooltip de TODOS os donos do mesmo texto — e mente para os outros.

**Caso real (BUG-31, confirmado):** o texto `Max Health increased by 10%.` é usado pelo status `Consumption` (10% **por stack**) e pela skill `Endurance I` (bônus **fixo**). A nota do Consumption caiu nos dois e mente para o Endurance. É a mesma família do **INC-1** (chave duplicada), mas a colisão é no JOGO, no texto de várias entidades — não no nosso dicionário.

## 2. Como a varredura funciona

1. Lê os CSVs do censo em `docs/cobertura/` (todo `*.csv` com coluna `descricao`; hoje: skills, status, itens, afixos, powerups, acoes).
2. Acha todo texto usado por **mais de uma entidade** em dois critérios:
   - **EXATA** — mesmo texto caractere a caractere (é o critério do lookup do mod);
   - **VARIANTE** — textos que só diferem em espaço duplo/espaço no fim. O mod colapsa `"  "` → `" "` no fim do postfix (renderiza igual), mas **não apara o fim** e o lookup das tabelas é pelo texto original — então a nota pega um e não o outro. Hoje dá **0 casos reais**; a classe foi provada capaz de disparar com um caso sintético (`"Max Health increased by 10%. "` vs `"Max Health increased by 10%."` → sinalizado).
3. Cruza com as **286 chaves** com correção/nota do `LocalizePatch` (`TextFixes` 86 + `TextAppends` 200 — contagem confere com `check_dupes.py` e `check_fix_keys.py`).
4. Imprime as suspeitas (chave + donos + nota aplicada + linha do `.cs`) e um resumo contado. **Exit 0 sempre** — é AVISO, não reprova.

**Limite conhecido:** o censo cobre tooltips de skills/status/itens/afixos/powerups; texto de UI, dicas de loading e chaves de localização (ex.: `Resist Divine`) não têm como ser checados quanto a compartilhamento.

## 3. Números da rodada (30/09)

| o que | valor |
|---|---|
| entidades com descrição no censo | **1552** (skills 451, status 545, itens 192, afixos 285, powerups 79) |
| textos usados por 2+ entidades (exato) | **88** (dos quais **4** cruzam categorias) |
| chaves com nota/correção no patch | **286** (86 `TextFixes` + 200 `TextAppends`) |
| **SUSPEITAS** (chave com nota + 2+ donos exatos) | **16** |
| variantes de espaço | 0 (classe provada capaz de disparar) |
| chaves limpas (1 dono exato, sem variante) | 266 |
| chaves fora do censo | 4 (UI/loading/localização — esperado, ver §5) |

**Veredito consolidado das 16:** **6 defeitos** (`Dodging incoming attacks.`, `Healed.`, `Restores *0 health per turn.`, `Cannot move or perform actions.`, `Max Health increased by 10%.` [= BUG-31], `Shielded from [0] damage.`) · **1 a verificar** (`Deals *0 cold damage per turn while in the aura.`) · **9 OK**.

---

## 4. As 16 suspeitas e o veredito de cada uma

> Formato da nota no `.cs`: valor iniciado por `\n<color=#C8B090>` e fechado com `</color>` — o patch acrescenta esse bloco no fim do tooltip (a cor é trocada pela cor do jogo em runtime).

### 1. `Deals *0 cold damage per turn while in the aura.` — ⚠️ VERIFICAR (risco baixo)
- **Tabela:** `TextAppends` l.437 (`{ "Deals *0 cold damage per turn while in the aura.", ... }`).
- **Donos:** status `Aura Of Frost`, status `Aura of Frost` (nome duplicado com "O" maiúsculo — dado do jogo), status `Chilling Aura`.
- **Nota aplicada:** `The aura reaches 3 hexes from its source, and it damages enemies that start their turns inside it.`
- **Veredito:** a 1ª metade vale para todos — o dump de status traz `aura=sim | raio=3` nos três. A 2ª metade ("damages enemies that **start their turns** inside it") tem fonte só no texto da skill `Aura Of Frost` (*"Deals *0 cold damage to enemies that start their turns within 3 hexes of your character."*); para `Chilling Aura` **nenhum texto do censo declara o gatilho** — se o gatilho dela não for início de turno (a `Aura of Lightning`, por exemplo, dispara quando a vítima age), a frase engana nesse tooltip. Fechar o gatilho da Chilling Aura (ação/código) antes de manter a frase como está.

### 2. `Dodging incoming attacks.` — ❗ DEFEITO
- **Tabela:** `TextAppends` l.290.
- **Donos:** status `Enduring Evasion`, status `Evasion`, status `Uncanny Evasion`.
- **Nota aplicada:** `Guarantees a dodge (100% chance) of the next 2 incoming attacks; each dodge spends one charge.`
- **Risco:** a nota foi escrita para o Enduring Evasion. Os textos das skills donas dizem:
  - `Enduring Evasion`: *"Gain 100% @dodge chance@ for the next **2 attacks**."* → nota certa;
  - `Evasion`: *"Gain 100% @dodge chance@ for the next **attack**."* → a nota promete **2**;
  - `Uncanny Evasion`: *"Gain 100% @dodge chance@ for the next **attack**. Increases @Counter Attack Damage@ by 50% for 1 turn."* → a nota promete **2**.
  O número é propriedade da carga concedida pela skill, não do status; o tooltip do status não pode afirmar "2" para todos. **Correção sugerida (não aplicada):** nota sem número ("Guarantees a dodge (100% chance) of your next incoming attacks; each dodge spends one charge.") — a contagem já está no texto de cada skill.

### 3. `Healed.` — ❗ DEFEITO
- **Tabela:** `TextAppends` l.272.
- **Donos:** status `Greater Heal`, status `Heal`, status `Lesser Heal`.
- **Nota aplicada:** `Restores the target to full health (heal equal to their Max Health).`
- **Risco:** o dump mostra que só o Greater Heal cura até a vida cheia:
  - `Greater Heal`: `TargetStored['Healing'] = Target['MaxHealth']` → "full health" **certo**;
  - `Heal`: `TargetStored['Healing'] = Source.SpellPower('Light') * 1.0f` → cura **por Spell Power**, não full;
  - `Lesser Heal`: `TargetStored['Healing'] = Source.SpellPower('Light') * .5f` → idem.
  **Correção sugerida (não aplicada):** nota genérica ("Restores health; the amount depends on the effect that applied it.") ou mover a frase para o texto da skill `Greater Heal`, que tem texto próprio.

### 4. `Restores *0 health per turn.` — ❗ DEFEITO
- **Tabela:** `TextAppends` l.221.
- **Donos:** status `Lingering Light`, status `Regenerate`, status `Seal of Salvation`.
- **Nota aplicada:** `It reaches allies within 3 hexes of the seal's bearer.`
- **Risco:** a nota é **do Seal of Salvation** (o dump traz `aura=sim | raio=3 | auraAli=sim` nele). `Lingering Light` e `Regenerate` têm `aura=nao` — a frase "seal's bearer" não existe nesses tooltips. É pior que ruído: cria um "selo" que não está lá. **Correção sugerida (não aplicada):** tirar a frase desta chave; se quiser manter, prender a um texto exclusivo do Seal (o texto da skill `Seal of Salvation` já diz "All allies within 3 hexes of you heal for *0 per turn.").

### 5. `*0 fire damage dealt to enemies within the aura.` — ✅ OK
- **Tabela:** `TextAppends` l.443. **Donos:** status `Aura of Flame`, status `Burning Aura`.
- **Nota:** `The aura reaches 3 hexes from its source.` — dump: `aura=sim | raio=3` nos dois. Confirmado também pela skill `Aura of Flame` ("within 3 hexes of your character").

### 6. `*0 lightning damage dealt to enemies within the aura each time they perform an action.` — ✅ OK
- **Tabela:** `TextAppends` l.434. **Donos:** status `Aura of Lightning`, status `Shocking Aura`.
- **Nota:** `The aura reaches 3 hexes from its source.` — dump: `aura=sim | raio=3` nos dois.

### 7. `Attackers lifesteal for [0]%.` — ✅ OK
- **Tabela:** `TextAppends` l.428. **Donos:** status `Blood Howl`, status `Dire Howl`.
- **Nota:** `Lasts 2 turns.` — dump: `dur=2` nos dois; os textos das skills (`Blood Howl`/`Dire Howl`) também dizem "for 2 turns".

### 8. `Cannot move or perform actions.` — ❗ DEFEITO
- **Tabela:** `TextAppends` l.392.
- **Donos:** status `Frozen`, status `Stunned` (a linha `Stunned` cujo texto é este; existe OUTRA linha `Stunned` com texto `Stunned.`, que recebe a nota própria "Cannot move or perform actions.").
- **Nota aplicada:** `While frozen the target also ignores Chilled: no new stacks can be applied.`
- **Risco:** a frase é do `Frozen` — o dump confirma que só ele tem `ImmunityChilled:Set:1`; o `Stunned` tem apenas `Rooted:Set:1, Disabled:Set:1`. No tooltip do Stunned a nota fala de "frozen" e de "Chilled", que não têm relação. **Correção sugerida (não aplicada):** escopar a frase (ex.: "Frozen only: ...") ou removê-la da chave compartilhada — não há texto exclusivo do Frozen para recebê-la.

### 9. `Deals *0 weapon damage to all enemies within a line.` — ✅ OK
- **Tabela:** `TextAppends` l.483. **Donos:** skill `Crushing Slam`, skill `Slam`.
- **Nota:** `The line reaches 5 hexes from you.` — o dump de `ActionProps` das DUAS ações é idêntico: `blast=Source.Cell != Cell && Cell.Distance(Source.Cell) <= 5 && ... Cell.DistanceFromLine(...) < 3f/2f`. A mesma entrada serve às duas (é o caso histórico do INC-1, agora verificado como correto).

### 10. `Grants 10% @mana steal@.  Sacrifices 10% maximum health per turn.` — ✅ OK
- **Tabela:** `TextFixes` l.872 (correção de terminologia: `maximum health` → `max health`). **Donos:** skill `Hunger` (Shadow T3) e status `Hunger` — o mesmo texto nos dois, mesma mecânica. A correção é terminológica e serve aos dois.

### 11. `Increases damage dealt by 30%.` — ✅ OK
- **Tabela:** `TextAppends` l.341. **Donos:** status `Battle Fury`, status `Rage of the Dwarf King`.
- **Nota:** `Lasts 3 turns.` + `Also increases the healing you do by the same percentage.` — dump: os dois têm `DamageMod:Base:30, ModelScaleMultiplier:Base:10`, `dur=3`, `maxStk=1`. Mesmo atributo, mesma duração; a regra "DamageMod também aumenta a cura" é do motor (vale para os dois).

### 12. `Invincible.` — ✅ OK
- **Tabela:** `TextAppends` l.260. **Donos:** status `Invincible`, status `Swan Song`.
- **Nota:** `Cannot take damage.` — dump: os dois têm `Invincible:Set:1`.

### 13. `Max Health increased by 10%.` — ❗ DEFEITO CONFIRMADO (é o BUG-31 do KANBAN)
- **Tabela:** `TextAppends` l.422.
- **Donos:** skill `Endurance I` (Monk T1, passiva) e status `Consumption`.
- **Nota aplicada:** `Each stack grants another 10% Max Health; you gain one stack per enemy hit.`
- **Risco:** a nota é do `Consumption` (status com stack por inimigo atingido; dump: `maxStk=100`). O `Endurance I` é `attr=MaxHealth:Percentage:10,` — bônus **fixo**, sem stack. No tooltip do Endurance I a nota descreve um empilhamento que não existe. **Direção já decidida no KANBAN (BUG-31):** mover a explicação para uma chave EXCLUSIVA do Consumption (a skill `Consumption` tem texto próprio: *"Devour the life force of all enemies within 2 hexes dealing *0 Shadow Damage and giving you 10% @Maximum Health@ for each enemy effected."*) ou remover a nota da chave compartilhada.

### 14. `Physical damage increased by [0].` — ✅ OK
- **Tabela:** `TextAppends` l.545. **Donos:** skill `Huntsman I`, skill `Huntsman II`.
- **Nota:** `Scales with your character level.` — dump: as duas usam a mesma curva (`DamageFlatPhysical:Base:Source.GetFlatDamageValue * 1.2f` / `* 1.8f`), e o próprio comentário do `.cs` (l.539-541) diz que a chave cobre as duas de propósito.

### 15. `Shielded from [0] damage.` — ❗ DEFEITO
- **Tabela:** `TextAppends` l.218.
- **Donos:** status `Shield of Light`, status `Shield of Retribution`.
- **Nota aplicada:** `When the shield is depleted it explodes, dealing holy damage to foes within 3 hexes.`
- **Risco:** a nota é do `Shield of Retribution` (dump: `efeitos=ShieldOfRetribution:Base:Source.SpellPower("Light") * 3f * Source.DamageModHealing`). O `Shield of Light` não tem efeito nenhum (`efeitos` vazio; a skill só diz *"Calls down a shield that protects the target absorbing *0 damage."*) — o tooltip dele ganha uma explosão que não existe. Nota registrada no livro (`ANTES-E-DEPOIS.md` l.134) já com o alvo trocado. **Correção sugerida (não aplicada):** tirar da chave compartilhada; o texto da skill `Shield of Retribution` já descreve a explosão.

### 16. `[0] fire damage dealt to enemies within the aura.` — ✅ OK
- **Tabela:** `TextAppends` l.440. **Donos:** status `Aura of Flame` (linha `[0]`), status `Burning Aura` (linha `[0]`).
- **Nota:** `The aura reaches 3 hexes from its source.` — dump: `aura=sim | raio=3` nos dois (mesma família do item 5; o texto com `[0]` é a variante da linha).

---

## 5. Conferência extra pedida pelo BUG-31: as outras chaves da Consumption

O BUG-31 mandou conferir também a chave `@Maximum health@ reduced by 20%` (l.424-426). Resultado da varredura:

| chave | linha | donos | situação |
|---|---|---|---|
| `@Maximum health@ reduced by 20%.` | `TextAppends` l.425 | 1 — status `Consumption` | **não compartilhada** (limpa) |
| `@Maximum health@ reduced by 10%.` | `TextAppends` l.419 | 1 — status `Consumption` | **não compartilhada** (limpa) |
| `Max Health increased by 10%.` | `TextAppends` l.422 | 2 — `Endurance I` + `Consumption` | **compartilhada → é o BUG-31** (item 13 acima) |

Ou seja: só a terceira tem o problema de dono; as duas de "reduced by X%" são exclusivas do Consumption (o conteúdo delas quanto a stacks/gatilho continua sendo decisão da revisão do status, fora do escopo do BUG-32).

### Chaves fora do censo (4) — esperado
`Resist Divine` / `Resistance Divine` (chaves de localização do motor — RV-13) e duas dicas de loading (`Shops are refreshed...`, `A well timed healing or mana potion...`). Não são texto de tooltip do censo; a varredura não tem como julgar compartilhamento nelas.

---

## 6. Anexo A — os 72 textos compartilhados que AINDA NÃO têm nota (mapa de risco futuro)

Estes textos são usados por 2+ entidades e **não** têm entrada no patch. Uma nota/correção NOVA sobre qualquer um deles atinge todos os donos listados — é aqui que o próximo BUG-32 nasce. (Os 16 itens da §4 + estes 72 = os 88 compartilhados.)

- `Gain Added Return Damage Physical equal to 2% of your Armor.` — 6 dono(s) [itens]: Band of Blades (itens); Bladed Great Helm (itens); Crimson Guard (itens); Iron Thorn Cuirass (itens); Mourning Star (itens); Razor Wire (itens)
- `Basic attacks have a 25% chance to proc an additional attack once per turn.` — 4 dono(s) [itens]: Golden Valkyrie Helm (itens); Golden Valkyrie Plate (itens); Last Word (itens); Winged Axe (itens)
- `Cold skill damage increased` — 4 dono(s) [afixos]: Cold (afixos); Frigid (afixos); Glacial (afixos); Icy (afixos)
- `Deals *0 weapon damage to target. ` — 4 dono(s) [skills]: Melee Attack (skills); Ranged Attack (skills); Staff Attack (skills); Unarmed Attack (skills)
- `Dexterity increased` — 4 dono(s) [afixos]: Agile (afixos); Nimble (afixos); Quick (afixos); Swift (afixos)
- `Elemental skill damage increased` — 4 dono(s) [afixos]: Magician's (afixos); Magus' (afixos); Sorcerer's (afixos); Wizard's (afixos)
- `Fire skill damage increased` — 4 dono(s) [afixos]: Burning (afixos); Scorching (afixos); Searing (afixos); Smouldering (afixos)
- `Healing skill power increased` — 4 dono(s) [afixos]: Holy (afixos); Imbued (afixos); Radiant (afixos); Savior's (afixos)
- `Intelligence increased` — 4 dono(s) [afixos]: Bright (afixos); Brilliant (afixos); Clever (afixos); Gifted (afixos)
- `Lightning skill damage increased` — 4 dono(s) [afixos]: Charged (afixos); Electrified (afixos); Shocking (afixos); Static (afixos)
- `Might increased` — 4 dono(s) [afixos]: Herculean (afixos); Mighty (afixos); Powerful (afixos); Strong (afixos)
- `Physical damage increased` — 4 dono(s) [afixos]: Crushing (afixos); Mangling (afixos); Pulverizing (afixos); Smashing (afixos)
- `Reflex increased` — 4 dono(s) [afixos]: Elusive (afixos); Evasive (afixos); Ghostly (afixos); Immaterial (afixos)
- `Shadow skill damage increased` — 4 dono(s) [afixos]: Blighted (afixos); Darkened (afixos); Gloomy (afixos); Umbra (afixos)
- `Summon damage increased` — 4 dono(s) [afixos]: Lich's (afixos); Master's (afixos); Summoner's (afixos); Trainer's (afixos)
- `Summon health increased.` — 4 dono(s) [afixos]: Embalmer's (afixos); Gravekeeper's (afixos); Mortician's (afixos); Necromancer's (afixos)
- `Vitality increased` — 4 dono(s) [afixos]: Fit (afixos); Healthy (afixos); Hearty (afixos); Immortal (afixos)
- `Adds [0] damage to elemental attacks.` — 3 dono(s) [status]: Elemental Equilibrium: Cold (status); Elemental Equilibrium: Fire (status); Elemental Equilibrium: Lightning (status)
- `Crit damage increased` — 3 dono(s) [afixos]: Deadly (afixos); Fatal (afixos); Lethal (afixos)
- `Damage taken reduced by 25%.` — 3 dono(s) [status]: Diamond Protection (status); Emerald Protection (status); Ruby Protection (status)
- `Damaged.  ` — 3 dono(s) [status]: Damage (status); Greater Damage (status); Lesser Damage (status)
- `Health cannot drop below 1.` — 3 dono(s) [status]: Cursed Coin (status); Dark Ritual (status); Tadashi's Ritual (status)
- `Targets in burning ground receive *0 fire damage.` — 3 dono(s) [status]: Burning Ground (status); Ignite (status); Meteor (status)
- `Weapon attacks apply 2 stacks of bleeding.` — 3 dono(s) [itens]: Bone Cleaver (itens); Crimson Slayer (itens); Executioner Axe (itens)
- `10% chance to cast Hide in Shadows whenever an enemy dies.` — 2 dono(s) [itens]: Assassin's Garb (itens); Assassin's Mask (itens)
- `10% chance to cast Level [level value] {SKL=Blinding Light} when hitting with any ability.` — 2 dono(s) [itens]: Sunstone Necklace (itens); Sunstone Ring (itens)
- `10% chance to cast Stealth on turn start.` — 2 dono(s) [itens]: Stalker's Hood (itens); Stalker's Leather (itens)
- `15% chance to cast Stealth on turn start.` — 2 dono(s) [itens]: Shadowstalker Body Armor (itens); Shadowstalker Mask (itens)
- `20% chance to cast Stealth on turn start.` — 2 dono(s) [itens]: Night Stalker Leathers (itens); Night Stalker Mask (itens)
- `@Dodge chance@ increased by 50%.` — 2 dono(s) [status]: Smoke Bomb (status); Smoke Cloud (status)
- `@Resistance@ lowered by 20%.` — 2 dono(s) [status]: Dispelling Fracture (status); Fracture (status)
- `A key` — 2 dono(s) [status]: Test Event Status - Boss Event (status); Test Event Status - Test Key (status)
- `Absorbs the next attack.` — 2 dono(s) [status]: Ghost Armor (status); Tadashi's Armor (status)
- `All damage and healing dealt to one target is also dealt to the linked target.` — 2 dono(s) [skills, status]: Soul Link (skills); Soul Link (status) ← cruza categorias
- `Armor increased by 15%` — 2 dono(s) [afixos]: Artisan (afixos); Fortified (afixos)
- `Armor increased by 25%` — 2 dono(s) [afixos]: Indestructible (afixos); Journeyman (afixos)
- `Attacks apply 1 stack of poison.` — 2 dono(s) [itens]: Plague Jacket (itens); Plague Mask (itens)
- `Basic attacks have a 20% chance to proc an additional attack once per turn.` — 2 dono(s) [itens]: Bagh nakha (itens); Marksman's Cap (itens)
- `Cannot move.` — 2 dono(s) [status]: Chained (status); Immobilized (status)
- `Cannot take damage.` — 2 dono(s) [status]: Invincible (status); Transcendence (status)
- `Chance of suffering critical strikes increased by 8%. Damage taken increased by 15%.` — 2 dono(s) [status]: Bounty Hunter's Mark (status); Tracker's Mark (status)
- `Charm the enemy target for 1 turn.  Cannot target bosses.` — 2 dono(s) [skills]: Cupid Shot (skills); Mind Blossom (skills)
- `Charmed` — 2 dono(s) [status]: Cupid Shot (status); Mind Blossom (status)
- `Cold resistance increased` — 2 dono(s) [afixos]: Insulated (afixos); Insulating (afixos)
- `Deals *0 weapon damage and lowers target's @Healing@ received by 50% for 2 turns.` — 2 dono(s) [skills]: Cursed Bite (skills); Dire Bite (skills)
- `Deals *0 weapon damage to target.   When targeting an ally, heals for *0.` — 2 dono(s) [skills]: Melee Attack (skills); Ranged Attack (skills)
- `Deals *0 weapon damage.  Applies 2 stacks of {STA=Bleeding}.` — 2 dono(s) [skills]: Bleeding Shot (skills); Gouge (skills)
- `Each time a damage or healing skill is cast, it receives a random effectiveness modifier from 50% up to 250%. ` — 2 dono(s) [skills]: Fickle Flame (skills); Perturb (skills)
- `Fire resistance increased` — 2 dono(s) [afixos]: Fireproof (afixos); Retardant (afixos)
- `Gain Additional Weapon Damage equal to 30% of your Dexterity.` — 2 dono(s) [itens]: Griffin Horn (itens); Naginata (itens)
- `Grants an additional Action Point.` — 2 dono(s) [itens, status]: Energizing Elixir (itens); Ruby Rancor (status) ← cruza categorias
- `Heals target ally for *0.    When targeting an enemy, deals *0 Holy Damage.` — 2 dono(s) [skills]: Staff Attack (skills); Unarmed Attack (skills)
- `Howl causing *0 physical damage to all enemies within 2 hexes.  Applies a debuff that causes all attackers to lifesteal for [1]% against this target for 2 turns.` — 2 dono(s) [skills]: Blood Howl (skills); Dire Howl (skills)
- `Increase all Damage and Healing by 8%. ` — 2 dono(s) [skills]: Hot Head I (skills); Warmonger I (skills)
- `Lightning resistance increased` — 2 dono(s) [afixos]: Diffusing (afixos); Grounding (afixos)
- `Might increased by [0].` — 2 dono(s) [status]: Might (status); Verse of Valor (status)
- `Physical resistance increased` — 2 dono(s) [afixos]: Defending (afixos); Protecting (afixos)
- `Recovery reduced by 30%.` — 2 dono(s) [status]: Wilting (status); Witch's Brew (status)
- `Reduces healing received by 50%.` — 2 dono(s) [status]: Cursed Bite (status); Gore (status)
- `Summon Damage increased by [10]%` — 2 dono(s) [afixos]: Feral (afixos); Necromancer (afixos)
- `Summon Damage increased by [12]%` — 2 dono(s) [afixos]: Lich (afixos); Primal (afixos)
- `Summon Damage increased by [4]%` — 2 dono(s) [afixos]: Conjurer (afixos); Untamed (afixos)
- `Summon Damage increased by [6]%` — 2 dono(s) [afixos]: Instinctual (afixos); Summoner (afixos)
- `Summon Damage increased by [8]%` — 2 dono(s) [afixos]: Occultist (afixos); Wild (afixos)
- `Summon Health increased by [10]%` — 2 dono(s) [afixos]: Caretaker's (afixos); Undertaker (afixos)
- `Summon Health increased by [12]%` — 2 dono(s) [afixos]: Death Hunter (afixos); Keeper's (afixos)
- `Summon Health increased by [4]%` — 2 dono(s) [afixos]: Mortician (afixos); Trainer's (afixos)
- `Summon Health increased by [6]%` — 2 dono(s) [afixos]: Gravekeeper (afixos); Tamer's (afixos)
- `Summon Health increased by [8]%` — 2 dono(s) [afixos]: Embalmer (afixos); Handler's (afixos)
- `Target takes *0 fire damage per turn.` — 2 dono(s) [status]: Immolate (status); Smelt (status)
- `Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.` — 2 dono(s) [status]: Contagion (status); Poisoned (status)
- `Vitality increased by [0].` — 2 dono(s) [status]: Tenacity of the Forest (status); Vitality (status)

---

## 7. Anexo B — PROPOSTA de passo novo no `tools/release-check.sh` (**NÃO APLICADO**)

> **Isto é texto para decisão — nada foi editado em `release-check.sh`.** O passo roda a ferramenta como AVISO (a ferramenta sai 0 sempre) e nunca reprova a release; só falha se a ferramenta não rodar.

**Onde inserir:** depois do bloco `== PASSO 4/5 — NOTAS REDUNDANTES ... ==` (logo antes do `== PASSO 5/5 — CICLO DO JOGO ... ==`).

**Trecho proposto:**

```bash
# ======================= 5. CHAVE COMPARTILHADA (BUG-32) =====================
# AVISO, nao reprova. A nota/correcao e por TEXTO: o mesmo texto pode servir a
# varias entidades do jogo (skills/status/itens) e uma nota escrita para um dono
# mente para os outros - caso real BUG-31 (nota do status Consumption caiu tambem
# no Endurance I porque "Max Health increased by 10%." e compartilhado).
# A ferramenta SEMPRE sai com exit 0 (a decisao e humana); o passo so falha se
# ela nao rodar. Relatorio: docs/cobertura/revisao/BUG-32-chaves-compartilhadas.md
echo
echo "== PASSO 5/6 - CHAVE COMPARTILHADA (aviso; a ferramenta sempre sai 0) =="
SAIDA_COMP="$($PYTHON tools/check_chave_compartilhada.py 2>&1)"; rc=$?
printf '%s\n' "$SAIDA_COMP" | sed 's/^/   /'
N_SUSP=$(printf '%s\n' "$SAIDA_COMP" \
         | grep -aoE 'SUSPEITAS \(nota em texto com mais de um dono\) \. [0-9]+' \
         | grep -oE '[0-9]+' | head -1)
if [ "$rc" -ne 0 ] || [ -z "$N_SUSP" ]; then
  passo_fail "5. COMPARTILHADA" "check_chave_compartilhada.py NAO RODOU (exit $rc) - aviso BUG-32 nao verificado"
else
  if [ "$N_SUSP" != "0" ]; then
    echo
    echo "   AVISO (nao reprova): $N_SUSP suspeita(s) de chave compartilhada - a nota pode"
    echo "   estar mentindo para outro dono do texto. Revisar:"
    echo "   docs/cobertura/revisao/BUG-32-chaves-compartilhadas.md"
  fi
  passo_ok "5. COMPARTILHADA" "$N_SUSP suspeita(s) (aviso; nunca reprova)"
fi
```

**Ajustes de renumeração que o trecho exige (também não aplicados):**
1. `== PASSO 5/5 — CICLO DO JOGO + ANALISE DO LOG ==` → `== PASSO 6/6 — ...`;
2. `== PASSO 6 — PASSO HUMANO ... ==` → `== PASSO 7 — ...`;
3. o bloco de comentário do topo do arquivo (lista "1. BUILD … 5. HUMANO") ganha o passo novo entre DUPLICADAS/NOTAS e o CICLO;
4. se o label `"5. CICLO"` for renumerado para `"6. CICLO"`, o `case "$f"` do resumo final tem que acompanhar (senão o detalhe da falha some).

**Validação feita sobre o trecho:** o `grep` do contador foi testado contra a saída real da ferramenta nesta rodada e devolveu `16` (a linha do resumo NÃO tem dígito antes do número — foi reescrita para `mais de um dono` justamente por isso; `>1` fazia o extrator pegar o "1").

---

## 8. Como reprocessar

```bash
python tools/check_chave_compartilhada.py        # saida completa (exit 0 sempre)
python tools/check_chave_compartilhada.py -v     # + lista das chaves limpas (1 dono)
```

Fontes de evidência usadas nos vereditos: os CSVs do censo (`docs/cobertura/*.csv`) e o dump de boot do RoguelikeDebugger no `LogOutput.log` do perfil (campos `efeitos`, `dur`, `maxStk`, `aura/raio` das linhas de `[Status]` e `alvos` das linhas de `[ActionProps]`).
