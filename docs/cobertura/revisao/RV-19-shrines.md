# RV-19 — Tooltips dos SHRINES: auras, escala (`Shrine Effect Bonus`) e o dano do Flame Shrine

Data: 30/09/2026 · Status: **investigação fechada; notas propostas (NADA aplicado no mod)**
Fontes: `Assembly-CSharp.dll` (build atual do jogo) + `resources.assets` (1,7 GB) + censo (`docs/cobertura/*.csv`) + dump de boot no `LogOutput.log`.
Referência de linhas: decompilado completo do build atual (`Assembly-CSharp.decompiled.cs`, 371.804 linhas; classe `CompiledDynamicExpresso` em l.49965).

---

## 0. Veredito rápido

1. **A família de auras de shrine escala por `ShrineEffectBonus`.** No motor o padrão é
   `Mathf.Round(BASE * (1 + (X["ShrineEffectBonus"] / 100)))`, com `X = Target` (quem recebe a aura) na maioria e
   `X = Source` nas duas auras de perigo (Decay/Flame). Confirmado nos assets (strings dos próprios status) e no
   cache de expressões compiladas do assembly (l.66061–66428) — mesmas strings, byte a byte.
2. **O dano do Flame Shrine não é fixo, nem escala por nível, nem por Might.** É uma **% do Max Health do alvo**
   (o atacante), com a % variando por **tipo de inimigo**, multiplicada por `(1 + Source["ShrineEffectBonus"]/100)`,
   com mínimo 1. A fórmula mora na **AÇÃO `Flame Aura Proc`** (campo `Effects[0].Action`), não no status.
   O Decay é o irmão exato (`Decay Aura Proc`, por turno).
3. O texto de hoje **não diz a cadeia do Shrine Effect Bonus** em nenhuma aura, e o `Flame Shrine Aura` **não tem
   número nenhum** ("Attackers take Fire Damage."). Proposta de notas na seção 6.
4. **O que não deu para fechar** (registrado na seção 7): qual campo do status dispara a ação (`ActionsOnTick`?
   `SkillTriggers`? mecânica de aura?) e o binding exato de `Source`/`Target` no momento do dano — o dump atual de
   status não expõe esses campos.

---

## 1. Como reconferir (ferramentas + ARMADILHA de encoding)

- Decompilado: `"$HOME/.dotnet/tools/ilspycmd" -t <Tipo> "E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed/Assembly-CSharp.dll"` (nunca `-o`). Tipos-chave: `CompiledDynamicExpresso`, `GameLogic`, `GroundEffect`, `GroundEffectInfo`, `SkillTrigger`, `Burst2Flame.ActionStatusInfo`.
- **ARMADILHA (nova):** no `resources.assets`, os objetos de AÇÃO são serializados pelo Odin e guardam **strings em
  UTF-16LE** (cada letra seguida de `\0`). Um grep ASCII não acha NADA dessas fórmulas. Os STATUSES das auras, por
  outro lado, estão em UTF-8 normal. Exemplo que custou tempo: `grep -a "GetValueByEnemyType" resources.assets` dá
  **0 hits**, mas `b"G\x00e\x00t\x00V\x00a\x00l..."` acha as 2 fórmulas do jogo inteiro. Scripts usados:
  `%LOCALAPPDATA%\hermes\cache\scratch\scan_proc_actions.py` e `scan_utf16.py`.
- Offsets citados = recursos de `resources.assets` (busca por byte; confirme com o script `scan_proc_actions.py`).

---

## 2. A família de auras de shrine (12 statuses em assets)

Base = o número dentro de `Mathf.Round(BASE * (1 + (X["ShrineEffectBonus"] / 100)))`. Offsets no `resources.assets`
(cluster de status ~1517,1M). Linha = entrada correspondente no cache compilado do assembly.

| Status (nome no jogo) | Texto de hoje (chave exata) | BASE | X | Fórmula/linha do cache |
|---|---|---|---|---|
| Warrior Aura | `Damage increased by [0]%. ` (espaço no fim) | 20 | Target | l.66061 |
| Guardian Aura | `Reduces Damage taken by [0]%. ` | 20 | Target | l.66061 |
| Conqueror Aura | `Critical hit chance increased by [0]%.` | 20 | Target | l.66061 |
| Rogue Aura | `Increases dodge chance by [0]%.` | 20 | Target | l.66061 |
| Reaper Aura | `Lifesteal increased by [0]%.` | 8 | Target | l.66348 |
| Seraph Aura | `Recover [0]% of maximum health each turn. ` | 10 | Target | l.66389 |
| Shaman Aura | `Recover [0]% of maximum mana each turn. ` | 10 | Target | l.66389 |
| Energy Aura | `Decreases the cost of mana using abilities by [0]%.` | 50 (exibe +50; efeito `ManaCostMod` = −50×fator) | Target | l.66184 (exibição) + l.66143 (efeito) |
| Fury (Goblin Battle Standard) | `Damage increased by [0]%. Damage taken increased by [0]%. ` | 25 / −25 | Target | l.66266 / l.66307 |
| Dwarven Aura (Dwarven Totem) | `Your attacks have a [0]% chance to stun the target.` | 20 | Target | l.66061 |
| **Decay Shrine Aura** | `Take [0]% of your Max Health in Shadow Damage per turn.` | **10** | **Source** | l.66102 (expressão) |
| **Flame Shrine Aura** | `Attackers take Fire Damage.` | **5** | **Source** | l.66225 (a fórmula do dano está na ação — seção 4) |

Detalhes dos assets (strings completas, para auditoria):

- Warrior/Guardian/Conqueror/Rogue: a fórmula `Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))` aparece
  **2×** no objeto do status — uma é o `AttributeEffects[0].Amount` (o efeito real, confirmado no censo:
  `DamageMod`/`DamageReduction`/`CritChance`/`DodgeChance`) e a outra é a `DescriptionExpressions[0]` (o `[0]` do texto).
- Energy Aura: duas fórmulas distintas — `+50` (exibição) e `-50` (efeito `ManaCostMod`). O texto exibe 50 e o efeito
  reduz o custo; coerente.
- Fury: `+25` (2×) e `-25` (efeito `DamageReduction`).
- Dwarven e Decay/Flame também têm strings de **condição** no objeto (campo não exposto pelo dump — ver seção 7):
  `Source.IsEnemy(Target)` + `Cell.IsCurrentHex(Target)` (Dwarven, Flame) e `Cell.IsCurrentHex(Source)` (Decay).
- Status irmãos vindos dos mesmos assets de ground effect: `Conqueror Shrine Explosion` → "Might of the Conqueror"
  (próxima ação com 100% de crítico); `Guardian Shrine Explosion` → "Guardian Shield" (dano tomado −50%);
  `Reaper Shrine Explosion` → "Marked for Death" (dano tomado +50%); `Warrior Shrine Explosion` → "Warrior's Blade"
  (dano +50%); `Goblin Battle Standard Explosion` → "Frenzy" (+1 AP). Esses NÃO escalam por ShrineEffectBonus
  (valores fixos) — fora do escopo das notas.

### 2.1 Os assets dos shrines (GroundEffectInfo, cluster ~1520,8M)

`Conqueror Shrine`, `Decay Shrine`, `Dwarven Totem`, `Energy Coil`, `Flame Shrine`, `Goblin Battle Standard`,
`Guardian Shrine`, `Reaper Shrine`, `Rogue Shrine`, `Seraph Shrine`, `Shaman Shrine`, `Warrior Shrine`
(+ variantes `(Destructible)`). O tooltip do shrine mostra `ActionStatuses[0].Description` (l.214180) — por isso
"Attackers take Fire Damage." aparece ao passar o mouse no Flame Shrine (observação do usuário, bate com o código).

---

## 3. Quem dá o `ShrineEffectBonus` (a cadeia)

| Fonte | Valor | Texto de hoje |
|---|---|---|
| `Omnism I` (Chaos, tier 1) | `ShrineEffectBonus:Base:8` | "Increases the effectiveness of shrines by 8%." |
| `Omnism II` (Chaos, tier 2) | `ShrineEffectBonus:Base:20` | "Increases the effectiveness of shrines by an additional 12%." |
| `Horn of Devotion` (Fortune, Legendary) | `ShrineEffectBonus:Base:{50,100}` | "Increases the effect of Shrines by {50,100}%." |

- Provas: skills.csv/log (attrs acima) + testes de integração do próprio jogo:
  `LearnAndExpectAttributeDelta(Caster, "CHAOS_1_P1_Omnism I", "ShrineEffectBonus", 8f)` (l.183426) e
  `… "CHAOS_2_P1_Omnism II", "ShrineEffectBonus", 20f` (l.183505). Os tiers somam: 8 + 12 = 20 (o "additional 12%"
  é o incremento do tier 2; o attr do tier 2 já vale 20).
- O atributo se chama **"Shrine Effect Bonus"** na localização (chave própria).
- Localização ainda tem a chave `"100% increased effect from Shrines"` (roll máximo do Horn) e a dica de loading:
  *"Add stunning chance to all your attacks by standing in a Dwarven Totem or force your enemies to lose life in
  the Decay Shrine."* (Seção `Shrines` das dicas.)
- **O número exibido nas auras já vem multiplicado**: as `DescriptionExpressions` de cada aura são a PRÓPRIA fórmula
  (com o fator `1 + ShrineEffectBonus/100`), e o caminho do tooltip as avalia com o personagem do jogador —
  status tooltip em l.213903+ (`Source`/`Target` do status) e tooltip do shrine em l.214180
  (`Source = NetworkingManager…Root.WorldCharacter`, sem Target). ⚠ confirmação in-game = RV-20; aqui é evidência de código.

---

## 4. O DANO do Flame Shrine (e do Decay) — onde mora e a fórmula real

### 4.1 A cadeia

`GroundEffectInfo "Flame Shrine"` → status **`Flame Shrine Aura`** (texto + condição) → **AÇÃO `Flame Aura Proc`**
→ `Effects[0].Action` = **fórmula do dano** → `GetActionDamage` (l.38588) converte `TargetStored["FireDamage"]` em dano.

As duas ações existem no cluster de ações (~1519,5M) e são irmãs (`Decay Aura Proc` @1519517560,
`Flame Aura Proc` @1519544376; cada uma com `Targets` = tipos Odin + condições ASCII
`Cell.InRange(SelectedCell, 10) && Cell.HasEnemy(Source)` e `Cell == Target.Cell`).

### 4.2 A fórmula (Flame) — string exata, no asset e no assembly

Asset: `Flame Aura Proc`, campo `Effects[0].Action`, **UTF-16** em `resources.assets` @1519546098:

```
TargetStored["FireDamage"] = Mathf.Max(1,  Mathf.Round((Target["MaxHealth"] * Target.GetValueByEnemyType(.025f, .08f, .1f, .12f, .14f, .05f)) * (1 + (Source["ShrineEffectBonus"] / 100))))
```

(dois espaços após `Max(1,` — é do asset; a mesma string está no cachê compilado, l.87156/87158)

Decay: `Decay Aura Proc`, `Effects[0].Action`, UTF-16 @1519519282:

```
TargetStored["ShadowDamage"] = Mathf.Round((Target["MaxHealth"] * Target.GetValueByEnemyType(.05f, .1f, .12f, .15f, .2f, .1f)) * (1 + (Source["ShrineEffectBonus"] / 100)))
```

### 4.3 As porcentagens (por tipo de inimigo)

`Character.GetValueByEnemyType(boss, champion, elite, soldier, fodder, player)` (l.38351):
não-AI → `player`; AI → pelo `EnemyType` (enum l.99774: Fodder=0, Soldier=1, Elite=2, Champion=4, Boss=3).

| Aura | Boss | Champion | Elite | Soldier | Fodder | Player |
|---|---|---|---|---|---|---|
| **Flame Shrine** (Fire, mín. 1) | 2,5% | 8% | 10% | 12% | 14% | **5%** |
| **Decay Shrine** (Shadow, por turno) | 5% | 10% | 12% | 15% | 20% | **10%** |

A ponte com o texto/exibição: a base do asset (5 no Flame, 10 no Decay) **é igual ao valor "player"** da fórmula
(5%/10%) — o texto de hoje do Decay ("Take [0]% of your Max Health…") é exatamente essa % do alvo; e o valor que o
tooltip mostra (`[0]`) já vem multiplicado pelo bônus (seção 3). Para o Flame o texto não tem `[0]` — por isso o
jogador não vê número nenhum: a informação só existe no código.

### 4.4 O que isso significa em jogo

- **Flame Shrine Aura**: quem **ataca** um personagem dentro da aura leva dano de fogo = `Máx(1, MaxHealth(quem atacou)
  × % por tipo × (1 + bônus de shrine))`. É um efeito de retaliação ("Attackers take Fire Damage."): a condição do
  status (`Source.IsEnemy(Target)`) e a ação (`Cell.HasEnemy(Source)` na seleção de alvo) apontam para "inimigo do
  portador da aura".
- **Decay Shrine Aura**: quem **fica dentro** perde `% do próprio Max Health em Shadow` por turno (o texto diz isso);
  a dica de loading confirma o uso ("force your enemies to lose life in the Decay Shrine").

---

## 5. Censo — status com "Shrine" no nome e a coluna `efeitos`

`docs/cobertura/status.csv` (12 linhas contêm "Shrine"; só DUAS têm "Shrine" no NOME):

| Linha | Nome | `efeitos` | `efeitosDano` |
|---|---|---|---|
| 121 | `Decay Shrine Aura` | **VAZIO** | **VAZIO** (nEfeitosDano=0) |
| 189 | `Flame Shrine Aura` | **VAZIO** | **VAZIO** (nEfeitosDano=0) |

- As outras 10 linhas ("Conqueror Aura", "Energy Aura", "Fury", "Guardian Aura", "Horn of Devotion", "Reaper Aura",
  "Rogue Aura", "Seraph Aura", "Shaman Aura", "Warrior Aura") só contêm "Shrine" na coluna `efeitos` (fórmula) —
  **exceção:** é a família, mas o nome não tem "Shrine".
- **Por que vazio:** o `efeitos` do dump lê `AttributeEffects` e o `efeitosDano` lê `Effects` (GeneralEffect.Action) —
  o Flame/Decay não têm nenhum dos dois: o dano mora na AÇÃO `* Aura Proc` (seção 4), que o censo de status não vê.
  Ou seja, **o vazio é legítimo, não é falha de dump** para essas duas colunas.
- Sibling fora do filtro: `Dwarven Aura` também está com `efeitos` VAZIO (mesma família, mesmo padrão de asset).
- No `LogOutput.log` o dump completo tem ainda `aura=nao | raio=3 | auraAli=nao | auraIni=nao` para todas as auras
  (o `raio=3` é só o default da classe; esses status NÃO são do tipo `IsAura` — o raio do shrine vem do GroundEffect).

---

## 6. PROPOSTA de notas (`TextAppends`) — **não aplicado**

Padrão do mod: chave = texto EXATO do jogo (conferido contra o censo/LogOutput), valor = `\n<color=#C8B090>…</color>`
(o `#C8B090` vira a cor especial do tooltip em runtime, e o bloco é movido para o fim com linha em branco pelo
`CorEOrdemDoTooltip`). **As notas NÃO usam `[N]`** — o pipeline de expressões roda depois do `Localize` e
interpretaria o token (regra do projeto).

### 6.1 Entradas novas (9 chaves livres)

```csharp
// RV-19 shrines — famílias de aura de shrine: base + cadeia do Shrine Effect Bonus.
// A chave do Flame não tem número no texto: a nota carrega o dano real (ação "Flame Aura Proc").
{ "Attackers take Fire Damage.",
  "\n<color=#C8B090>Deals fire damage equal to 5% of the attacker's Max Health (2.5% for bosses up to 14% for fodder; 5% for players), minimum 1. Scales with the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
{ "Take [0]% of your Max Health in Shadow Damage per turn.",
  "\n<color=#C8B090>Base 10% of Max Health; varies by enemy type (5% for bosses up to 20% for fodder). The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
{ "Damage increased by [0]%. ",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
{ "Reduces Damage taken by [0]%. ",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
{ "Critical hit chance increased by [0]%.",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
{ "Increases dodge chance by [0]%.",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
{ "Lifesteal increased by [0]%.",
  "\n<color=#C8B090>Base 8%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
{ "Decreases the cost of mana using abilities by [0]%.",
  "\n<color=#C8B090>Base 50%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
{ "Your attacks have a [0]% chance to stun the target.",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>" },
```

⚠ todas as 9 chaves foram conferidas: **1 dono cada** no `status.csv` (sem risco de chave compartilhada) e **nenhuma
das 9 existe hoje** em `TextFixes` nem em `TextAppends` (checado por script em `LocalizePatch.cs`, 30/09).

### 6.2 Casos especiais (decisão necessária antes de aplicar)

1. **Seraph Aura — `"Recover [0]% of maximum health each turn. "`** já tem `TextFixes` (RV-14: `maximum health` → `max health`, linha 848). `TextFixes`/`TextAppends` são mutuamente exclusivos → a nota teria de ser **fundida no `TextFixes`**:
   `"Recover [0]% of max health each turn. \n<color=#C8B090>Base 10%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>"`
2. **Shaman Aura — `"Recover [0]% of maximum mana each turn. "`** idem (RV-14, linha 818):
   `"Recover [0]% of max mana each turn. \n<color=#C8B090>Base 10%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; Horn of Devotion).</color>"`
3. **Fury — `"Damage increased by [0]%. Damage taken increased by [0]%. "`** já tem `TextAppends` (RV-9, linha 281:
   "Also increases the healing you do by the same percentage."). Esta é a aura do **Goblin Battle Standard**
   (`DamageMod` +25 / `DamageReduction` −25 — **não** tem componente de cura no censo). Proposta: **estender** o valor
   existente com a segunda frase OU deixar como está — decisão do usuário; conferir no BUG-32 (varredura de chave
   compartilhada) se a nota RV-9 veio de outro dono deste texto.

---

## 7. O que falta (para fechar o que ficou indeterminado)

Indeterminado: **(a)** qual campo do status `Flame Shrine Aura`/`Decay Shrine Aura` dispara a ação `* Aura Proc`
(candidatos: `ActionsOnTick` + `ActionsOnTickCondition`/`ActionsOnTickTargets`, `SkillTriggers`, ou a mecânica de
`AuraSourceStatus`/`AuraTriggerStatus`); **(b)** o binding exato de `Source`/`Target` no momento do dano — a fórmula
usa `Source["ShrineEffectBonus"]` e o shrine é criado sem bônus (`CreateNewGroundEffectCharacter`, l.143758:
`TeamIndex = 2`, nada herdado); no caminho do TOOLTIP o mesmo símbolo resolve para o **personagem do jogador**
(l.214180). Se o dano rodar com `Source` = shrine, o fator `(1 + bônus)` seria ×1 na prática — é exatamente o tipo de
divergência que o projeto registra em vez de "corrigir".

Para fechar (dump): no `RoguelikeDebugger`, o dump de status (`ActionStatusInventoryPatch`) **deveria exportar**
`TooltipDamageInfoRefAction`, `TooltipDamageInfoRefStatus`, `DamageExpressionOverrides`, `TickTargets`,
`ActionsOnTick` (nomes) + `ActionsOnTickCondition` + `ActionsOnTickTargets`, `StatusEffectsOnTick*`,
`SkillTriggers` (TriggerType/Condition/Targets/GeneralEffects) e `AuraSourceStatus`/`AuraTriggerStatus` (nomes).
E o dump de AÇÕES (`SkillInventoryPatch`) hoje só cobre ações ligadas a skills — as ações soltas
(`Flame Aura Proc`, `Decay Aura Proc`, `Energy Coil Static Field`, `* Shrine Explosion`) não entram; varrer
`Game.Instance.Actions` inteiro (ou pelo menos as `* Aura Proc`) com `Effects[].Action` fecharia os dois itens de uma vez.

Confirmação em jogo (escopo do RV-20): (i) hover no shrine com/sem `Omnism` — o número do `[0]` muda? (esperado: sim);
(ii) o dano do Flame para "attackers" escala com o SEU bônus? (a fórmula diz que sim/fator; o binding é a dúvida).

---

## 8. Apêndice — offsets e comandos usados

- Statuses das auras (UTF-8 em `resources.assets`): Conqueror @1517112096 · Decay @1517113960 · Dwarven @1517115056 ·
  Energy Coil @1517116232 · **Flame @1517120720** · Goblin Battle Standard @1517121808 · Guardian's @1517124568 ·
  Reaper's @1517127576 · Rogue @1517128536 · Seraph's @1517129496 · Shaman @1517130552 · Warrior's @1517133224.
- Ações: `Decay Aura Proc` @1519517560 (fórmula UTF-16 @1519519282) · `Flame Aura Proc` @1519544376
  (fórmula UTF-16 @1519546098).
- GroundEffects: Flame Shrine @1520832880 · Decay Shrine @1520830600 (…demais shrines no mesmo cluster ~1520,8M).
- Cache compilado (linhas do decompilado): 20→66061 · 10-Source→66102 · −50→66143 · +50→66184 · 5-Source→66225 ·
  25→66266 · −25→66307 · 8→66348 · 10→66389 · dano Shadow→87116/87118 · dano Fire→87156/87158.
- Código: `GetValueByEnemyType` 38351 · `EnemyType` 99774 · `GetActionDamage` 38588 · `GetExpression` (lookup exato)
  49971+ · tick de status (`ActionsOnTick`) 38470–38510 · mecânica de aura 40900–40942 ·
  `CreateNewGroundEffectCharacter` 143758 · tooltips 213903 / 214180 · testes Omnism 183426 / 183505.
- Scripts: `%LOCALAPPDATA%\hermes\cache\scratch\scan_proc_actions.py`, `scan_utf16.py`, `check_keys_mod.py`,
  `scan8_full.py` (varredura de bytes do install inteiro: `GetValueByEnemyType` só existe no Assembly-CSharp.dll).
