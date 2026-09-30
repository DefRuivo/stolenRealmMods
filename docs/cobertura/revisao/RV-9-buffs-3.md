# RV-9 - Buffs: arquivo de trabalho (393 entradas)

Gerado do `status.csv`. **Descricoes COMPLETAS** (ja errei com texto truncado, RV-8c).
`dur` = duracao em turnos e `maxStk` = cap de stacks (campos `Duration`/`MaxStacks` do asset, l.319141/319149);
`VAR` = existem assets HOMONIMOS com valores diferentes - nesse caso confira por ASSET, nao por nome.

> ATENCAO: o nome NAO identifica o status. Assets homonimos tem papeis diferentes.

## Growing Hatred  [Common]
- efeitos: `ExtraTurnActionPoints:Base:1, ModelScaleMultiplier:Base:25`
- dur=20 | maxStk=2
- descricao (completa): Grants 1 additional Action Point. Increases Damage Taken by 25%.
- ja no mod: nao

## Guardian Aura  [Common]
- efeitos: `DamageReduction:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Reduces Damage taken by [0]%.
- ja no mod: nao

## Guardian Flask  [Common]
- efeitos: `Armor:Base:800`
- dur=5 | maxStk=100
- descricao (completa): Armor increased by 800.
- ja no mod: nao

## Guardian Shield  [Common]
- efeitos: `DamageReduction:Base:50`
- dur=1 | maxStk=100
- descricao (completa): Damage taken decreased by 50%.
- ja no mod: nao

## Guile of the Rogue  [Rare]
- efeitos: `DexterityBase:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): @Dexterity@ increased by {5,25}.  <i><color=#808080>"Justice is not always a path of righteousness walked in the light. Sometimes, it is a road shrouded in darkness, a route navigated by the quiet flicker of rebellion."</i></color>
- ja no mod: nao

## Harmonize  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=100
- descricao (completa): Your actions spread Harmony to nearby allies.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `DexterityBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Dexterity per stack.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `IntelligenceBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Intelligence per stack.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `MightBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Might per stack.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `ReflexBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Reflex per stack.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `VitalityBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Vitality per stack.
- ja no mod: nao

## Heal  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * 1.0f`
- dur=0 | maxStk=100
- descricao (completa): Healed.
- ja no mod: nao

## Holy Ground  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Target.TeamIndex == 1 ? Target.FodderHealthAtLevel * .3f : Source.SpellPower('Light') * 1f`
- dur=3 | maxStk=100
- descricao (completa): Targets in holy ground receive healing.
- ja no mod: nao

## Holy Ground  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower() * .75f`
- dur=3 | maxStk=100
- descricao (completa): Targets in holy ground are healed *0 per turn.
- ja no mod: nao

## Holy Ground  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['HolyDamage'] = Source.SpellPower() * .75f`
- dur=3 | maxStk=100
- descricao (completa): Taking *0 Holy Damage per turn while in Holy Ground.
- ja no mod: nao

## Honor of the Ymir  [Mythic]
- efeitos: `PerHexRangeDamageBonus:Base:Source.HasWeaponType("Staff")`
- dur=0 | maxStk=1
- descricao (completa): Every hex between you and your target increases damage dealt by an additional @12%@ when wielding a Staff, Bow, or Two Handed Gun.  <i><color=#808080>You carry the Speed of the Ymir!</color></i>
- ja no mod: nao

## Horn of Devotion  [Legendary]
- efeitos: `ShrineEffectBonus:Base:{50,100}`
- dur=0 | maxStk=1
- descricao (completa): Increases the effect of Shrines by {50,100}%.  <i><color=#808080>"Given to great warriors to aid them in battle."</i></color>
- ja no mod: nao

## Hunger  [Common]
- efeitos: `ManaOnHit:Base:10`
- efeitosDano: `TargetStored['ShadowDamage'] = Target.MaxHealth * .1f`
- dur=3 | maxStk=1
- descricao (completa): Grants 10% @mana steal@.  Sacrifices 10% maximum health per turn.
- ja no mod: nao

## Hunger for Vengeance  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## Hunger of Ksvaldir  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['ShadowDamage'] = Target.MaxHealth * .1f`
- dur=3 | maxStk=1
- descricao (completa): Sacrifices 10% maximum health per turn.
- ja no mod: nao

## Ice Crystal  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>The magic crystal emanates cold.</color></i>  Allows you to summon a @level@ {1,30} Ice Golem to fight for you. Benefits from your @Cold Damage@.
- ja no mod: nao

## Immunity  [Common]
- efeitos: `Invincible:Set:1, ImmunityMovementImpairing:Set:1, ImmunityDisabled:Set:1, ImmunitySlow:Set:1`
- dur=10 | maxStk=10
- descricao (completa): Can only be harmed by destroying Soul Fetishes.  Immune to movement imparing effects.
- ja no mod: nao

## Improvise  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=100
- descricao (completa): Songs no longer clear each other's Crescendo.
- ja no mod: nao

## Incalculable Rage  [Common]
- efeitos: `ExtraTurnActionPoints:Base:1, TurnFreeMovementPoints:Base:-6, ModelScaleMultiplier:Base:20`
- dur=3 | maxStk=1
- descricao (completa): Grants 1 additional Action Points. Lowers movement points by 6.
- ja no mod: nao

## Increased Armor  [Common]
- efeitos: `Armor:Base:5 * Source.Level, MagicArmor:Base:5 * Source.Level`
- dur=2 | maxStk=100
- descricao (completa): @Armor@ and @Magic Armor@ increased by [0].
- ja no mod: nao

## Increased Damage and Healing by 10%  [Common]
- efeitos: `DamageMod:Base:10`
- dur=2 | maxStk=100
- descricao (completa): Increases Damage and Healing by 10%.
- ja no mod: nao

## Increased Damage and Healing by 100%  [Common]
- efeitos: `DamageMod:Base:100`
- dur=2 | maxStk=100
- descricao (completa): Increases Damage and Healing by 100%.
- ja no mod: nao

## Increased Damage and Healing by 1000%  [Common]
- efeitos: `DamageMod:Base:1000`
- dur=5 | maxStk=100
- descricao (completa): Increases Damage and Healing by 1000%.
- ja no mod: nao

## Increased Damage and Healing by 25%  [Common]
- efeitos: `DamageMod:Base:25`
- dur=2 | maxStk=100
- descricao (completa): Increases Damage and Healing by 25%.
- ja no mod: nao

## Indestructible  [Common]
- efeitos: `Armor:Percentage:10, MagicArmor:Percentage:10, DamageReturnedMod:Base:10`
- dur=1 | maxStk=10
- descricao (completa): @Armor@, @Magic Armor@, and @Return Damage@ increased by 10% per stack.
- ja no mod: nao

## Inner Warmth  [Common]
- efeitos: `ImmunityFrozen:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Cannot be frozen.  Caused by being recently frozen.
- ja no mod: nao

## Inspiration  [Common]
- efeitos: `ResistPhysical:Base:1, ResistCold:Base:1, ResistFire:Base:1, ResistLightning:Base:1, ResistDivine:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Inspiration: +1% to all Resistance per stack.
- ja no mod: nao

## Inspiration  [Common]
- efeitos: `ResistPhysical:Base:2, ResistCold:Base:2, ResistFire:Base:2, ResistLightning:Base:2, ResistDivine:Base:2`
- dur=2 | maxStk=1000
- descricao (completa): Inspiration: +2% to all Resistance per stack.
- ja no mod: nao

## Inspiring Aura  [Common]
- efeitos: `DamageMod:Base:60`
- dur=4 | maxStk=100
- descricao (completa): Damage increased by 60%.
- ja no mod: nao

## Intelligence  [Common]
- efeitos: `IntelligenceBase:Base:Mathf.Round(1f+(0.2f*IslandLevel))`
- dur=0 | maxStk=100
- descricao (completa): Intelligence increased by [0].
- ja no mod: nao

## Invincible  [Common]
- efeitos: `Invincible:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Cannot take damage.
- ja no mod: nao

## Invincible  [Common]
- efeitos: `Invincible:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Invincible.
- ja no mod: nao

## Ivory Dragon Scale  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Gain the ability to shapeshift into a White Dragonkin.  <i><color=#808080>"Imbued with a gentle radiance, it serves as a testament to the enduring strength of the forces of light"</i></color>
- ja no mod: nao

## Lady of the Well  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): Search the Forest at night for the Lady of the Well, vanquish her, and bring her <quest>Shadow-Drenched Heart</quest> to The Paladin.
- ja no mod: nao

## Leech Dexterity  [Common]
- efeitos: `DexterityBase:Base:2 * (.1f * Target.Level)`
- dur=2 | maxStk=10
- descricao (completa): [0] @dexterity@ absorbed per stack.  Stacks up to 10 times.
- ja no mod: nao

## Leech Intelligence  [Common]
- efeitos: `IntelligenceBase:Base:2 * (.1f * Target.Level)`
- dur=2 | maxStk=10
- descricao (completa): [0] @intelligence@ absorbed per stack.  Stacks up to 10 times.
- ja no mod: nao

## Leech Might  [Common]
- efeitos: `MightBase:Base:2 * (.1f * Target.Level)`
- dur=2 | maxStk=10
- descricao (completa): [0] @might@ absorbed per stack.  Stacks up to 10 times.
- ja no mod: nao

## Legacy of the Mad Mage  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): What have you unleashed upon the world?
- ja no mod: nao

## Lesser Heal  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * .5f`
- dur=0 | maxStk=100
- descricao (completa): Healed.
- ja no mod: nao

## Lightning Shield  [Common]
- efeitos: `ResistLightning:Base:10`
- dur=3 | maxStk=100
- descricao (completa): @Lightning resistance@ increased by 10%.   Attackers take *0 lightning damage.
- ja no mod: nao

## Lingering Light  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * .4f`
- dur=3 | maxStk=100
- descricao (completa): Restores *0 health per turn.
- ja no mod: nao

## Living Armor  [Common]
- efeitos: `Armor:Base:3.5f * Source.Level, MagicArmor:Base:3.5f * Source.Level`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * .5f`
- dur=3 | maxStk=100
- descricao (completa): @armor@ and @magic armor@ increased by [0].   Regenerate *0 of @health@ each turn.
- ja no mod: nao

## March of the Warrior  [Rare]
- efeitos: `TurnFreeMovementPoints:Base:{1,4, dr}`
- dur=0 | maxStk=1
- descricao (completa): @Movement Points@ increased by [0].  <i><color=#808080>"Your courage must not be reckless, but calculated. Do not fear death; for it is an eventual certainty. "</i></color>
- ja no mod: nao

## Mark of the Alpha  [Mythic]
- efeitos: `SummonDamageMod:Base:{5,25}, SummonHealthMod:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>"Look at me, I'm the alpha now!</i></color>   Changes your @Nature Summons@ into @Pack Summons@. Increases Summon Damage and Health by {5,25}%
- ja no mod: nao

## Martial Prowess  [Rare]
- efeitos: `DamageModPhysical:Base:{5,20}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Physical Damage@ by {5,20}%.
- ja no mod: nao

## Masochism  [Common]
- efeitos: `DamageMod:Base:2`
- dur=1 | maxStk=100
- descricao (completa): Damage or healing increased by 2%.
- ja no mod: nao

## Masochism  [Common]
- efeitos: `DamageMod:Base:5`
- dur=1 | maxStk=100
- descricao (completa): Damage or healing increased by 5%.
- ja no mod: nao

## Master of Rage  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): Slay the nearby Wendigo.
- ja no mod: nao

## Master of the Blade  [Mythic]
- efeitos: `DamageModPhysical:Base:{8,40}`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>A true master of the blade.</color></i>  Increases @Physical Damage@ by {8,40}%. Physical damage you deal applies 1 stack of @Bleeding@.
- ja no mod: nao

## Might  [Common]
- efeitos: `MightBase:Base:Mathf.Round(1f+(0.2f*IslandLevel))`
- dur=0 | maxStk=100
- descricao (completa): Might increased by [0].
- ja no mod: SIM

## Might of the Conqueror  [Common]
- efeitos: `CritChance:Set:100`
- dur=4 | maxStk=100
- descricao (completa): Your next action has 100% Critical Hit Chance.
- ja no mod: nao

## Might of the Iceclaw  [Common]
- efeitos: `DamageMod:Base:50, ModelScaleMultiplier:Base:15`
- dur=4 | maxStk=100
- descricao (completa): Damage increased by 50%.
- ja no mod: nao

## Might of the Warrior  [Rare]
- efeitos: `MightBase:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): @Might@ increased by {5,25}.  <i><color=#808080>"Your strength lays in your conviction, your unyielding belief that this fight is right. The blade you wield is an extension of this conviction, a physical manifestation of your oath."</i></color>
- ja no mod: nao

## Miniature  [Common]
- efeitos: `TurnFreeMovementPoints:Base:3, ExtraTurnActionPoints:Base:1, MaxHealth:Percentage:-25, DamageMod:Base:-25, ModelScaleMultiplier:Base:-25`
- dur=3 | maxStk=100
- descricao (completa): Movement increased by 3 Action Points increased by 1 Max Health reduced by 25% Damage reduced by 25%
- ja no mod: nao

## Mirror Shard  [Legendary]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Summon a Dark clone of yourself but it fights for you.   <i><color=#808080>You hold a shard of your shattered reflection!</color></i>
- ja no mod: nao

## Molten Crystal  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>The magic crystal emanates heat.</color></i>  Allows you to summon a @level@ {1,30} Molten Golem to fight for you. Benefits from your @Fire Damage@.
- ja no mod: nao

## Molten Plating  [Common]
- efeitos: `DamageReduction:Base:60`
- dur=1 | maxStk=10
- descricao (completa): Damage taken reduced by 60%.
- ja no mod: nao

## Momentum  [Common]
- efeitos: `DamageMod:Base:Target["MomentumValue"]`
- dur=1 | maxStk=100
- descricao (completa): Damage or healing of your next action is increased by [0]%.
- ja no mod: nao

## Muse  [Common]
- efeitos: `ManaCostMod:Base:-10`
- dur=1 | maxStk=1
- descricao (completa): Mana costs reduced.
- ja no mod: nao

## Necromantic  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Summons a Skeletal Warrior on death
- ja no mod: nao

## Necronomicon  [Mythic]
- efeitos: `SummonDamageMod:Base:{5,25}, SummonHealthMod:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>You carry the Necronomicon!</i></color>   Changes your @Skeletal Summons@ into something... stronger. Increases Summon Damage and Health by {5,25}%
- ja no mod: nao
