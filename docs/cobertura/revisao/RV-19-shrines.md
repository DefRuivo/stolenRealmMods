# RV-19 — Tooltips dos SHRINES: auras, escala (`Shrine Effect Bonus`) e o dano do Flame Shrine

Data: 30/09/2026 · Status: **investigação fechada; notas APLICADAS** (as chaves da família estão no `LocalizePatch.cs`)
Revisão **RV-24 (30/09/2026, auditoria independente)**: 4 correções de fato (marcadas com ⚠RV-24 abaixo) + tabela de
números finais (§2.2) + 1 pendência para o **RV-22** (nota do Dwarven no `.cs` — o doc não edita código).
Revisão **RV-33/RV-34 (30/09/2026, consertos em código)**: **Decay e Flame ESCALAM**. Os 6 pontos que diziam o contrário
foram corrigidos aqui (§0.1, §0.2, §2.2, §4.3, §4.4, §6.1), com as provas no §0.5; as limitações que **permanecem**
estão no §9 e o roteiro de conferência em jogo no §10. Referência viva das notas: `BetterTooltips/Patches/LocalizePatch.cs`
e `BetterTooltips/Patches/ShrineAuraPatch.cs`.
Fontes: `Assembly-CSharp.dll` (build atual do jogo) + `resources.assets` (1,7 GB) + censo (`docs/cobertura/*.csv`) + dump de boot no `LogOutput.log`.
Referência de linhas: decompilado completo do build atual (`Assembly-CSharp.decompiled.cs`, 371.804 linhas; classe `CompiledDynamicExpresso` em l.49965).

---

## 0. Veredito rápido

1. **As 9 auras de BUFF da família escalam por `ShrineEffectBonus`**. No motor o
   padrão é `Mathf.Round(BASE * (1 + (X["ShrineEffectBonus"] / 100)))`, com `X = Target` (quem recebe a aura) nessas
   9 — Warrior, Guardian, Conqueror, Rogue, Reaper, Seraph, Shaman, Energy e Fury. Confirmado nos assets (strings dos
   próprios status) e no cache de expressões compiladas do assembly (l.66061–66428) — mesmas strings, byte a byte.
   **`Decay` e `Flame` TAMBÉM escalam** (⚠RV-33/RV-34 — substitui a conclusão ⚠RV-24). A expressão dos dois usa
   `X = Source`, e o `Source` que o hover do shrine entrega é vazio — mas o **prefix do mod** troca esse `Source` pelo
   **personagem avaliado**; no Decay o bônus é o do **próprio personagem NA AURA** (item 2). O `Dwarven` usa `X = Target`
   e escala — a nota em código já foi corrigida (§2.2/§6.1).
2. **O dano do Flame Shrine não é fixo, nem escala por nível nem por Might.** É uma
   **% do Max Health do alvo** (o atacante) **multiplicada pelo `ShrineEffectBonus`** (⚠RV-33/RV-34 — a versão ⚠RV-24
   dizia "não escala com o bônus"), com a % variando por **tipo de inimigo**, com mínimo 1. A fórmula mora na
   **AÇÃO `Flame Aura Proc`** (campo `Effects[0].Action`), não no status. O Decay é o irmão exato (`Decay Aura Proc`,
   por turno). ⚠RV-33/RV-34 (substitui a conclusão ⚠RV-24): a fórmula carrega o fator `(1 + Source["ShrineEffectBonus"]/100)`
   **e ele vale de verdade**. O hover do shrine entrega `Source = WorldCharacter` **VAZIO**, mas o prefix do mod preenche
   `Source`/`Target` vazios com o personagem avaliado — no Decay, quem fornece o bônus é o **próprio personagem NA AURA**
   (é ele que o proc acerta e é o `ShrineEffectBonus` DELE que o fator lê). No Flame o fator também entra, mas o hover
   **projeta** cada ocupante da área como atacante: *de quem* é o bônus no proc real (atacante ou portador da aura) está
   **INDETERMINADO** até a medição em jogo do dano de retorno (§9/§10).
3. O texto do JOGO não diz a cadeia do Shrine Effect Bonus em nenhuma aura, e o `Flame Shrine Aura` **não tem número
   nenhum** ("Attackers take Fire Damage."). As notas do mod da §6 estão **aplicadas**; o número do Flame vem da nota mais
   da lista por alvo, não do texto do jogo.
4. **Causa raiz do número travado na BASE (⚠RV-24 → CORRIGIDO no RV-33/RV-34):** não é "`Target` vazio" — o motor já
   resolve `if (Target == null) Target = Source` (decompilado l.215241–215243). A causa era o **`Source`**: no hover do
   shrine ele é `Root.WorldCharacter`, um `Character` **VAZIO** (`Observable.New<Character>()`, l.143680–143684; só
   `.Level` é atribuído, l.155836) → `ShrineEffectBonus` = 0, e o `[0]` saía sempre na base. **Estado de hoje:** o prefix
   do mod (RV-22/RV-34) preenche os parâmetros VAZIOS com o personagem avaliado e troca o `Source` quando ele é
   *exatamente* esse personagem vazio — o `[0]` passa a sair com o bônus REAL, inclusive nas duas auras de perigo. O que
   **continua** em aberto (seção 7) é só **qual campo do status dispara a ação** (`ActionsOnTick`? `SkillTriggers`?
   mecânica de aura?) — o dump de status não expõe esses campos.
5. **Provas dos consertos RV-33/RV-34** (a MEDIÇÃO em jogo vence a leitura de asset — hierarquia de fontes do projeto):
   - **medição do dono do jogo (30/09):** com o perk `Worship` (+100 em `ShrineEffectBonus`, um **PERK DO PERSONAGEM**) o
     dano por turno do Decay **DOBRA** — 10% → 20%. Logo o fator vale 2 e quem ele lê é o personagem **na aura**.
   - **log do próprio jogo (30/09):** a marca `RV-31 acumulado: ... char=Raven bonus=100` saiu **ao lado** de
     `RV-33 linha do Decay: Raven MaxHealth=233 -> ... (23 damage per turn for you)` — 23 = 10% de 233, ou seja o número
     **sem o fator** com o bônus 100 já presente no MESMO personagem (a aura de buff do mesmo Raven saiu ×2: Life Steal
     +16 = base 8 × 2). O log expôs a contradição; o RV-34 corrigiu a conta (as duas auras de perigo avaliam com
     `Source` = `Target` = o personagem avaliado).

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

⚠RV-24 — as **AURAS** da família (não os GroundEffectInfo) ocupam os pids **2543233–2543253** nos assets, 12 objetos:
as 9 auras de buff + `Decay Shrine Aura` + `Flame Shrine Aura` + `Dwarven Totem Aura Status`.

### 2.2 Números finais por aura — e quem realmente escala (⚠RV-24)

Os cinco valores possíveis do `ShrineEffectBonus` hoje são **0, +8 (`Omnism I`), +20 (`Omnism II`, que *substitui* a I
— §3), +50 e +100 (`Horn of Devotion`)**. Com o `Mathf.Round` do jogo (half-to-even), cada BASE vale:

| BASE (auras) | 0 | +8 | +20 | +50 | +100 | Escala com o bônus do jogador? |
|---|---|---|---|---|---|---|
| 20 (Warrior, Guardian, Conqueror, Rogue) | 20 | 22 | 24 | 30 | 40 | **sim** — `X = Target` |
| 8 (Reaper) | 8 | 9 | 10 | 12 | 16 | **sim** |
| 10 (Seraph, Shaman) | 10 | 11 | 12 | 15 | 20 | **sim** |
| 50 (Energy — exibição; o EFEITO é −50) | 50 | 54 | 60 | 75 | 100 | **sim** (efeito: −50 / −54 / −60 / −75 / −100) |
| 25 e −25 (Fury, no mesmo texto) | 25 | 27 | 30 | 38 | 50 | **sim** (negativo: −25 / −27 / −30 / −38 / −50) |
| 20 (Dwarven) | 20 | 22 | 24 | 30 | 40 | **sim** — nota em código já corrigida (§6.1) |
| 5 (Flame, por ataque — a % que multiplica a vida do ATACANTE) | 5 | 5 | 6 | 8 | 10 | **sim** (⚠RV-33/RV-34) |
| 10 (Decay, por turno — a % que multiplica a vida do PORTADOR) | 10 | 11 | 12 | 15 | 20 | **sim** (⚠RV-33/RV-34) |

Caveat: "escala" acima é o **efeito real** (o `AttributeEffects` das auras, que usa `Target` = quem recebe a aura). No
**hover do SHRINE** o número saía sempre na BASE para toda a família, pelo `Source` vazio (§0.4/§3) — ⚠RV-33/RV-34: o
prefix que preenche os parâmetros vazios (e troca o `Source` vazio do shrine) **já está no mod**, então o número do hover
passa a sair com o bônus do personagem em foco. Nas duas auras de perigo o fator entra **até na conta do dano** (medição
do dono em jogo: com `Worship` o dano por turno do Decay dobrou, 10% → 20%).

**Dwarven — RESOLVIDO (RV-24 → RV-22, já aplicado):** o asset do `Dwarven Totem Aura Status` (pid 2543235) **tem** a
fórmula com `Target`: `Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`, **2×** (`resources.assets`
@1517115395 e @1517115647 = offset +340 e +592 dentro do status) — reconferido por byte scan em 30/09. A nota em código
já é a correta: `"Base 20%. The value shown already includes the Shrine Effect Bonus"` (chave
`"Your attacks have a [0]% chance to stun the target."` em `BetterTooltips/Patches/LocalizePatch.cs`). O que o usuário
viu em jogo ("o número não muda com Omnism") se explicava pelo **`Source` vazio do hover**, não pelo efeito — e o
`Source` vazio é justamente o que o prefix do RV-22/RV-34 corrige.

---

## 3. Quem dá o `ShrineEffectBonus` (a cadeia)

| Fonte | Valor | Texto de hoje |
|---|---|---|
| `Omnism I` (Chaos, tier 1) | `ShrineEffectBonus:Base:8` | "Increases the effectiveness of shrines by 8%." |
| `Omnism II` (Chaos, tier 2) | `ShrineEffectBonus:Base:20` | "Increases the effectiveness of shrines by an additional 12%." |
| `Horn of Devotion` (Fortune, Legendary) | `ShrineEffectBonus:Base:{50,100}` | "Increases the effect of Shrines by {50,100}%." |

- Provas: skills.csv/log (attrs acima) + testes de integração do próprio jogo:
  `LearnAndExpectAttributeDelta(Caster, "CHAOS_1_P1_Omnism I", "ShrineEffectBonus", 8f)` (l.183426) e
  `… "CHAOS_2_P1_Omnism II", "ShrineEffectBonus", 20f` (l.183505).
- ⚠RV-24 — **os tiers NÃO somam: com as duas tiers o total é 20, não 28.** O filtro de `Character.Skills` **descarta
  uma skill quando o personagem conhece alguma listada em `SkillsThatReplace`**, e `Omnism I` é *substituída* pela
  `Omnism II` — por isso o conjunto efetivo nunca traz as duas ao mesmo tempo. O "additional 12%" do texto é apenas a
  diferença 8 → 20, **não** um incremento a somar. A conta está fechada pelo teste do próprio jogo:
  `LearnAndExpectAttributeDelta(..., "CHAOS_2_P1_Omnism II", "ShrineEffectBonus", 20f)` (l.183505).
- ⚠RV-24 — **as fontes do atributo são 5 e TODAS positivas** (`Horn of Devotion` {50,100}, `Omnism I` 8, `Omnism II`
  20, a `CharacterInfo` `T2_Worshiper` e 1 byte-run). **Não existe fonte negativa** no asset, logo **não há caso de
  borda de bônus negativo** a considerar hoje (varredura do asset, 30/09).
- O atributo se chama **"Shrine Effect Bonus"** na localização (chave própria).
- Localização ainda tem a chave `"100% increased effect from Shrines"` (roll máximo do Horn) e a dica de loading:
  *"Add stunning chance to all your attacks by standing in a Dwarven Totem or force your enemies to lose life in
  the Decay Shrine."* (Seção `Shrines` das dicas.)
- **O número exibido no tooltip**: as `DescriptionExpressions` de cada aura são a PRÓPRIA fórmula (com o fator
  `1 + ShrineEffectBonus/100`), mas ⚠RV-24 — **no hover do SHRINE esse número saía sempre na BASE**. O caminho é o
  `ShowGroundEffectTooltip` (l.214180), que monta `Source = NetworkingManager…Root.WorldCharacter` e deixa `Target`
  nulo; o `WorldCharacter` é um `Character` **VAZIO** (`Observable.New<Character>()`, l.143680–143684; só `.Level` é
  atribuído, l.155836) → `ShrineEffectBonus` = 0. Não é "`Target` vazio": o motor já faz `if (Target == null) Target
  = Source` (l.215241–215243) — era o **`Source`** que não tinha atributo nenhum. ⚠RV-33/RV-34 — **corrigido no mod**:
  um prefix em `Tooltip.ApplyDescriptionExpressions` (o funil de TODOS os tooltips, o hover do ground effect incluído)
  preenche os parâmetros VAZIOS com o personagem avaliado e troca o `Source` quando ele é *exatamente* o personagem
  vazio do shrine (nunca toca o `Source` de skill/status, que é o caster de verdade). O **efeito real** de cada aura já
  escalava (usa `Target`); agora o **número exibido** também sai com o bônus.

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
(5%/10%) — o texto de hoje do Decay ("Take [0]% of your Max Health…") é exatamente essa % do alvo. ⚠RV-33/RV-34
(substitui a conclusão ⚠RV-24) — o `[0]` do Decay é avaliado com **`X = Source`**, e o prefix do mod entrega ali o
**personagem avaliado** (não o personagem vazio do shrine): o `[0]` sai com o bônus REAL (com `Worship`: 20, não 10) e
**o dano de verdade escala igual** — o mesmo fator `(1 + bônus)` está nas duas pontas, no `[0]` e na ação. Prova: a
medição do dono em jogo (com `Worship` o dano por turno DOBRA). No log do jogo isso ficou visível antes do conserto: a
linha do Decay saiu `23 damage per turn for you` (10% de 233) **ao lado** de `char=Raven bonus=100` — o número sem o
fator. Para o Flame o texto do jogo não tem `[0]` — por isso o jogador não vê número nenhum ali: a informação só existe
no código (e na nota + lista por alvo que o mod acrescenta).

### 4.4 O que isso significa em jogo

- **Flame Shrine Aura**: quem **ataca** um personagem dentro da aura leva dano de fogo = `Máx(1, MaxHealth(quem leva o
  dano) × % do tipo dele × (1 + bônus dele/100))` — ⚠RV-33/RV-34: o fator **ENTRA** (quem o lê é o personagem avaliado,
  §4.2), então o dano **cresce** com `Omnism`/`Horn`/`Worship`. É um efeito de retaliação ("Attackers take Fire
  Damage."): a condição do status (`Source.IsEnemy(Target)`) e a ação (`Cell.HasEnemy(Source)` na seleção de alvo)
  apontam para "inimigo do portador da aura". No hover o atacante é DESCONHECIDO: cada ocupante da área é **projetado**
  como atacante (§9).
- **Decay Shrine Aura**: quem **fica dentro** perde `% do próprio Max Health em Shadow` por turno (o texto diz isso); a
  dica de loading confirma o uso ("force your enemies to lose life in the Decay Shrine"). Aqui o bônus é o do **próprio
  portador da aura** — é ele que o proc acerta no começo do turno dele e é o `ShrineEffectBonus` DELE que o fator lê — e
  o dano **escala** (medido em jogo: com `Worship`, 10% → 20%).

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
  ⚠RV-24 — **"efeitos vazio" no dump NÃO significa "não escala"**: o asset do `Dwarven Totem Aura Status` tem a
  fórmula com `Target` (§2.2). O dump só não lê aquele campo.
- No `LogOutput.log` o dump completo tem ainda `aura=nao | raio=3 | auraAli=nao | auraIni=nao` para todas as auras
  (o `raio=3` é só o default da classe; esses status NÃO são do tipo `IsAura` — o raio do shrine vem do GroundEffect).

---

## 6. As notas (`TextAppends`) — **APLICADAS no `LocalizePatch.cs`**

Padrão do mod: chave = texto EXATO do jogo (conferido contra o censo/LogOutput), valor = `\n<color=#C8B090>…</color>`
(o `#C8B090` vira a cor especial do tooltip em runtime, e o bloco é movido para o fim com linha em branco pelo
`CorEOrdemDoTooltip`). **As notas NÃO usam `[N]`** — o pipeline de expressões roda depois do `Localize` e
interpretaria o token (regra do projeto).

### 6.1 Chaves da família (aplicadas no `LocalizePatch.cs`)

```csharp
// RV-19 shrines — famílias de aura de shrine: base + cadeia do Shrine Effect Bonus.
// ⚠RV-33/RV-34 — as DUAS notas de perigo abaixo foram REESCRITAS em 30/09: a versão ⚠RV-24 (Flame e Decay
// "Does not scale with the Shrine Effect Bonus") está MORTA. O texto VIVO (copiado do LocalizePatch.cs) é:
{ "Attackers take Fire Damage.",
  "\n<color=#C8B090>Raw damage, before damage reduction: the percentage and the Shrine Effect Bonus of the attacker that triggers the aura - the character that attacks someone standing inside it - multiply that attacker's Max Health, never the Max Health of the character standing in the aura, and no armor, resistances or other mitigation is applied. The percentage follows the attacker's own enemy type: 2.5% boss, 8% champion, 10% elite, 12% soldier, 14% fodder, 5% player. Bonus sources: Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion - with Worship the number doubles. Minimum 1.</color>" },
// ⚠RV-34 — a nota do Flame diz "bônus do ATACANTE" porque é ele o `Target` da fórmula; a MEDIÇÃO em jogo do
// dano de RETORNO com `Worship` ainda não foi feita (§9(ii) — se o bônus for o do PORTADOR da aura, o texto muda).
{ "Take [0]% of your Max Health in Shadow Damage per turn.",
  "\n<color=#C8B090>Raw damage, before damage reduction: your own enemy type's percentage multiplied by your Max Health and by your Shrine Effect Bonus - the percentage and the number shown already include the bonus. Bonus sources: Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion. Your enemy type gives 10% for a player (5% boss, 10% champion, 12% elite, 15% soldier, 20% fodder for an AI carrier); no armor, resistances or other mitigation, and no minimum, so it can be 0.</color>" },
{ "Damage increased by [0]%. ",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>" },
{ "Reduces Damage taken by [0]%. ",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>" },
{ "Critical hit chance increased by [0]%.",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>" },
{ "Increases dodge chance by [0]%.",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>" },
{ "Lifesteal increased by [0]%.",
  "\n<color=#C8B090>Base 8%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>" },
{ "Decreases the cost of mana using abilities by [0]%.",
  "\n<color=#C8B090>Base 50%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>" },
// ⚠RV-24 → RESOLVIDO (RV-22 aplicado): o asset do `Dwarven Totem Aura Status` TEM a fórmula com Target (§2.2), logo
// ele ESCALA; a observação in-game ("o número não mudava com Omnism") era o `Source` vazio do hover, não o efeito.
// A nota em CÓDIGO já está corrigida — hoje é literalmente a linha abaixo ("already includes the Shrine Effect Bonus").
{ "Your attacks have a [0]% chance to stun the target.",
  "\n<color=#C8B090>Base 20%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>" },
```

⚠ todas as 9 chaves foram conferidas: **1 dono cada** no `status.csv` (sem risco de chave compartilhada) e, na data da
proposta, **nenhuma das 9 existia** em `TextFixes` nem em `TextAppends` (checado por script em `LocalizePatch.cs`,
30/09). **Hoje as 9 estão APLICADAS** — o `LocalizePatch.cs` é a fonte viva destas notas; onde o texto de lá divergir
deste bloco, vale o `LocalizePatch.cs`.

⚠RV-24 → ⚠RV-33/RV-34 — o trecho "The value shown already includes the Shrine Effect Bonus" das **8 auras de buff** é
verdade no **tooltip do STATUS** e, desde o prefix do RV-22/RV-34, também no **hover do SHRINE** (§0.4/§3). As duas notas
da família de PERIGO foram reescritas em 30/09 e **a conclusão ⚠RV-24 ("Does not scale") caiu**: o texto vivo é o
`Raw damage, before damage reduction: ...` do bloco acima, que diz que o fator **JÁ ESTÁ incluído**. O `LocalizePatch.cs`
é a fonte viva; este bloco é a cópia de conferência.

### 6.2 Casos especiais (resolvidos — os textos abaixo são os VIVOS no `LocalizePatch.cs`)

1. **Seraph Aura — `"Recover [0]% of maximum health each turn. "`** já tinha `TextFixes` (RV-14: `maximum health` → `max health`). `TextFixes`/`TextAppends` são mutuamente exclusivos → a nota foi **fundida no `TextFixes`**:
   `"Recover [0]% of max health each turn. \n<color=#C8B090>Base 10%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>"`
2. **Shaman Aura — `"Recover [0]% of maximum mana each turn. "`** idem (RV-14):
   `"Recover [0]% of max mana each turn. \n<color=#C8B090>Base 10%. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).</color>"`
3. **Fury — `"Damage increased by [0]%. Damage taken increased by [0]%. "`**: decisão tomada — o valor foi **estendido**.
   Era a ÚNICA das 9 chaves de aura sem a base e sem a cadeia do bônus, e a frase de cura do RV-9 (que continua
   verdadeira: o motor soma `DamageMod` à cura) foi mantida. Texto VIVO (RV-43, 01/10):
   `"\n<color=#C8B090>Base 25% damage and +25% damage taken. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion). Also increases the healing you do by the same percentage.</color>"`
   A chave segue só em `TextAppends` (o texto do jogo não mudou) e `check_chave_compartilhada.py --estrito` = 0.

---

## 7. O que falta (para fechar o que ficou indeterminado)

Indeterminado: **(a)** qual campo do status `Flame Shrine Aura`/`Decay Shrine Aura` dispara a ação `* Aura Proc`
(candidatos: `ActionsOnTick` + `ActionsOnTickCondition`/`ActionsOnTickTargets`, `SkillTriggers`, ou a mecânica de
`AuraSourceStatus`/`AuraTriggerStatus`).

**(b) FECHADO (RV-34) — com uma correção de rumo no meio do caminho.** O binding é o previsto — o shrine é criado sem
bônus (`CreateNewGroundEffectCharacter`, l.143758: `TeamIndex = 2`, nada herdado) e o caminho do TOOLTIP mostra por que o
`[0]` saía na base: o `Source` da avaliação é `Root.WorldCharacter`, um `Character` **VAZIO**
(`Observable.New<Character>()`, l.143680–143684; só `.Level` é atribuído, l.155836) → `Source["ShrineEffectBonus"]` = 0.
"`Target` vazio" **não** é a explicação: o motor já faz `if (Target == null) Target = Source` (l.215241–215243). O ⚠RV-24
concluiu daí que o fator era **×1 "na prática"** — isso estava **ERRADO como afirmação sobre o DANO**: quem executa a
fórmula é o personagem avaliado (as ações avaliam `Source` = `Target` = o personagem), e o fator lê o bônus DELE. O prefix
troca o `Source` vazio do shrine pelo receptor e o fator passou a valer também no número exibido (RV-34). A lição ficou
registrada: **medição em jogo vence leitura de asset** (§0.5).

Para fechar (dump): no `RoguelikeDebugger`, o dump de status (`ActionStatusInventoryPatch`) **deveria exportar**
`TooltipDamageInfoRefAction`, `TooltipDamageInfoRefStatus`, `DamageExpressionOverrides`, `TickTargets`,
`ActionsOnTick` (nomes) + `ActionsOnTickCondition` + `ActionsOnTickTargets`, `StatusEffectsOnTick*`,
`SkillTriggers` (TriggerType/Condition/Targets/GeneralEffects) e `AuraSourceStatus`/`AuraTriggerStatus` (nomes).
E o dump de AÇÕES (`SkillInventoryPatch`) hoje só cobre ações ligadas a skills — as ações soltas
(`Flame Aura Proc`, `Decay Aura Proc`, `Energy Coil Static Field`, `* Shrine Explosion`) não entram; varrer
`Game.Instance.Actions` inteiro (ou pelo menos as `* Aura Proc`) com `Effects[].Action` fecharia os dois itens de uma vez.

Confirmação em jogo — o que o RV-33/RV-34 fecharam e o que sobrou: (i) hover no shrine com/sem `Omnism` — o número do
`[0]` muda? **Agora muda, por construção** (o prefix preenche os parâmetros: §0.4/§3), mas a conferência VISUAL dessas
linhas ainda não foi feita — roteiro na §10; (ii) o dano do Decay escala com o bônus? **SIM — MEDIDO em jogo pelo dono
(30/09): com o perk `Worship` o dano por turno DOBRA (10% → 20%)**; (iii) o dano de retorno do Flame escala com o bônus
de quem o leva? A fórmula/fator são os mesmos, mas **falta a medição em jogo do dano de RETORNO com `Worship`** para
fechar se o bônus é o do atacante ou o do portador da aura — **INDETERMINADO**, §9(ii).

---

## 8. Apêndice — offsets e comandos usados

- Statuses das auras (UTF-8 em `resources.assets`): Conqueror @1517112096 · Decay @1517113960 · Dwarven @1517115056 ·
  Energy Coil @1517116232 · **Flame @1517120720** · Goblin Battle Standard @1517121808 · Guardian's @1517124568 ·
  Reaper's @1517127576 · Rogue @1517128536 · Seraph's @1517129496 · Shaman @1517130552 · Warrior's @1517133224.
  ⚠RV-24 — Dwarven: a fórmula `... (Target["ShrineEffectBonus"] ...)` está **dentro** desse status, em
  @1517115395 (= +340) e @1517115647 (= +592).
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
- ⚠RV-24 — como reconferir a tabela da §2.2 sem decompilar: `grep -abo "ShrineEffectBonus" .../resources.assets` dá
  **24** ocorrências ASCII — 23 nos 12 statuses da família (2 por aura em geral; **3** no Fury, que tem `+25` ×2 e
  `−25`; **1** só no Decay e **1** só no Flame, porque usam `Source`) + 1 no asset de atributo. Dumpar o contexto
  imprimível de cada offset (script `%LOCALAPPDATA%\hermes\cache\scratch\rv24_dump.py`) mostra a fórmula e o nome do
  status ao lado.

---

## 9. Limitações conhecidas (o que o mod NÃO consegue ou NÃO fecha)

1. **A linha `Your active shrine auras:` mostra o TOTAL do personagem, não a contribuição da aura.** O valor lido é o
   indexador do motor (`Character[atributo]`), o MESMO número da ficha (BetterStats) — inclui base, gear e skills, então
   pode **exceder** o número do shrine. Efeito visível: **Warrior e Fury colapsam no mesmo item**, porque a linha tem
   **um item por ATRIBUTO** e os dois mexem `DamageMod` (`Format("DamageMod")` → `Damage +X%`). Confirma que o valor é o
   total: ele pode ser **positivo onde a aura empurra para baixo** (Energy Coil −50 + `Forbidden Power` +50 = total 0) —
   o rótulo do total é o comportamento correto e não muda (RV-43, 01/10).
2. **O FLAME é uma PROJEÇÃO — e falta a medição do dano de RETORNO.** No hover **não se sabe quem vai atacar**: o mod
   projeta **cada ocupante da área** como atacante e mostra "o dano se ele atacasse" (vida máxima DELE × a % do tipo DELE
   × o bônus DELE). **INDETERMINADO**: falta a medição em jogo do dano de RETORNO do Flame com `Worship` para fechar se o
   bônus que multiplica é o do **atacante** ou o do **portador da aura** — a nota de hoje afirma "do atacante" (§6.1) e
   **tem de mudar se a medição disser o contrário**.
3. **A linha do Decay depende do receptor resolver.** A cadeia é `Tooltip.TooltipCharacter` → `Root.WorldCharacter` →
   `Source` existente (o `WorldCharacter` é o personagem VAZIO do shrine). Se o `TooltipCharacter` vier vazio, o fallback
   é o personagem vazio → `MaxHealth` = 0 → a linha **some sem erro**: o método devolve `null`, o texto do jogo fica
   intacto e o log diz o motivo. Já foi visto funcionando no log do dono (30/09), mas é **ponto de fragilidade**: a
   linha do Decay não tem prova de existência independente do foco da UI.

Nota de método: nada aqui é estimado. Atributo ausente no build, personagem fora da aura ou expressão não avaliável =
**nenhum número** é exibido (é o comportamento declarado no `CHANGELOG.md` do mod).

---

## 10. Como conferir em jogo (roteiro)

Objetivo: a **conferência visual** das linhas que ainda não foram olhadas na tela (a linha do Decay, a lista do Flame e o
bloco `Your active shrine auras:`), nos **três casos por aura** — bônus 0, `Omnism II` (+20) e o perk `Worship` (+100).

| Aura | bônus 0 | `Omnism II` (+20) | `Worship` (+100) |
|---|---|---|---|
| Warrior / Guardian / Conqueror / Rogue | 20 | 24 | 40 |
| Reaper | 8 | 10 | 16 |
| Seraph / Shaman | 10 | 12 | 20 |
| Energy (exibição; o EFEITO é o custo) | 50 / −50 | 60 / −60 | 100 / −100 |
| Fury | +25 / −25 | +30 / −30 | +50 / −50 |
| Dwarven | 20 | 24 | 40 |
| Decay (o `[0]`; e o dano/turno com 100 de vida) | 10% / 10 | 12% / 12 | 20% / 20 |
| Flame (a % do tipo; com 100 de vida o dano é o mesmo número) | 5 | 6 | 10 |

1. Entrar em jogo com um personagem **sem** bônus (caso 0), outro com `Omnism II` (Chaos tier 2 — ela **substitui** a I,
   §3) e outro com o perk `Worship`. O `Horn of Devotion` cobre +50/+100 (roll) e é o mesmo teste do `Worship` quando cai
   100.
2. **Auras de buff**: hover no shrine com o personagem **dentro** da área — o número tem de bater com a tabela acima na
   coluna do caso.
3. **Decay**: com o personagem na área, a linha do jogo ganha `(N damage per turn for you)`, com `N` = a % do tipo dele ×
   a vida máxima DELE × o bônus DELE (100 de vida: 10 / 12 / 20). Log: `[Shrine RV-23] RV-34 linha do Decay: <char>
   MaxHealth=... bonus=... -> '...'`.
4. **Flame**: hover com personagens na área — um item por ocupante (`In the aura now (raw damage it takes as the
   attacker, ...): nome dano; ...`). Log por alvo: `[Shrine RV-23] RV-34 Flame alvo '...': MaxHealth=... tipo=...
   bonus=... dano=...`. **A medição que falta** (§9(ii)): deixar um personagem COM `Worship` **apanhar** de dentro do
   Flame e comparar o dano de tela com/sem o perk — é o que diz se o bônus é do atacante ou do portador da aura.
5. **Linha `Your active shrine auras:`**: no hover, com o personagem dentro de qualquer aura de shrine, ela lista **todas**
   as auras vivas dele (um item por atributo) e **SOME quando ele sai da aura** (filtro do RV-29 — é o passo que prova o
   filtro). Log: `[Shrine RV-23] RV-31 acumulado: auras=[...] char=... bonus=... -> ...`; o `bonus=` é a única entrada que
   multiplica a aura e sai do atributo do próprio personagem.

Se algum número não bater, o que se corrige é **este relatório contra o jogo** (a medição vence a leitura de asset —
§0.5), nunca o contrário.
