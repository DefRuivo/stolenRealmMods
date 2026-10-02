# RV-13b — Fechamento da fila de revisão do censo (34 pendentes + 22 indeterminadas)

> **Tarefa:** fechar o ciclo do RV-13 — resolver as **34 `pendente`** e revisar as **22
> `indeterminado`** do `status.csv`, e provar por **contagem** a cobertura final.
> Continua o `RV-13-auditoria-cobertura.md` (que deixou §6.1, §6.2 e §8 em aberto) e o ticket
> `RV-13b` (`t_2ce8a190`); o RV-13 é o `t_533f2bf0`.
> **Data:** 30/09/2026. Método: contagem por script (`csv` do Python, nunca a olho) + leitura do
> `resources.assets` do install atual por **byte scan** (mesma técnica do `RV-19`) + `Assembly-CSharp.dll`.
> **O mod NÃO foi editado nesta rodada** (nenhum `.cs`, nenhum build): as correções deste relatório
> estão **decididas e registradas**, não aplicadas.

---

## 1. Veredito em números

| item | antes | depois |
|---|---:|---:|
| `pendente` | **34** | **0** |
| `indeterminado` | 22 | **16** (5 promovidas + 1 reclassificada) |
| `revisado` | 470 | 504 |
| `corrigido` | 15 | 19 |
| `sem-explicacao` | 19 | 21 |
| **total** | **560** | **560** |

As duas colunas de revisão do `status.csv` (`status` e `revisao`) receberam o **mesmo** veredito —
ferramentas diferentes leem colunas diferentes (convenção já registrada no commit `05c05a4`).

**Cobertura final do censo (RV-13): 2.280 de 2.280 entradas com veredito (100%).**
2.249 revisáveis (2.280 − 31 `intocavel` da árvore Bard). As 16 `indeterminado` **não** são
pendência: são linhas revisadas, com o ponto aberto **nomeado e localizado** (§6), no mesmo
critério que o RV-13 já usava.

| categoria (arquivo) | entradas | revisado | corrigido | sem-explicacao | intocavel | indeterminado | **pendente** |
|---|---:|---:|---:|---:|---:|---:|---:|
| Skills (`skills.csv`) | 451 | 309 | 102 | 9 | 31 | 0 | **0** |
| Status (`status.csv`) | 560 | 504 | 19 | 21 | 0 | 16 | **0** |
| Itens (`itens.csv`) | 905 | 782 | 9 | 113 | 0 | 1 | **0** |
| Afixos (`afixos.csv`) | 285 | 277 | 8 | 0 | 0 | 0 | **0** |
| Powerups (`powerups.csv`) | 79 | 79 | 0 | 0 | 0 | 0 | **0** |
| **TOTAL** | **2.280** | **1.951** | **138** | **143** | **31** | **17** | **0** |

Conferência aritmética: 1.951 + 138 + 143 + 31 + 17 = **2.280**. Cobertas = 2.280 − 0 = **2.280**;
1.951+138+143+17 = 2.249 revisáveis (as 31 do Bard saem do denominador).

> O RV-13 §6.1 dizia "34 pendentes"; aqui elas são **0**. O RV-13 §6.2 (propagação das colunas) já
> tinha sido fechado no commit `05c05a4` (2.123 → 34).

---

## 2. As 34 `pendente` — veredito uma a uma

Critério do projeto: mecânica conferida **no código/asset** (fonte da verdade) + ≥2 artefatos
independentes; divergência → o código vence; o texto do asset é lido **inteiro** antes da nota.
Fontes proibidas (wiki Fandom) não foram usadas — as provas são o `status.csv` (efeito do asset),
o `resources.assets` (fórmula/descrição do próprio objeto), o cache de expressões compiladas do
`Assembly-CSharp.dll` e as falas/testes do **próprio jogo** no assembly.

**`corrigido` (4)** — o texto precisa mudar:

| entrada | prova | estado |
|---|---|---|
| `Berserker's Rage` | `LocalizePatch.cs` — entrada do `TextFixes` sob o comentário `RV-14 terminologia: Berserker's Rage` (**l.1470**) já troca `max life` → `max health` (RV-14, regra da maioria) | **já aplicado** no mod |
| `Immortal Night` | `LocalizePatch.cs` — entrada do `TextFixes` sob o comentário `RV-14 terminologia: Immortal Night` (**l.1498**) troca `@Maximum health@` → `@Max health@` na variante **"…per stack."** (a variante sem "per stack" é a `Soul Fracture`, **l.1489**) | **já aplicado** no mod |
| `Raise Skeletal Lackey` (variante "Max Health, Damage, Armor, and Dodge Chance reduced by 50%.") | o efeito do asset tem **5** atributos: `MaxHealth:Multiplicative:.5, DamageMod:Multiplicative:.5, Armor:Multiplicative:.5, DodgeChance:Multiplicative:.5, **MagicArmor:Multiplicative:.5**, ModelScaleMultiplier:Set:-40`. O texto lista 4 e **omite o Magic Armor** — a omissão muda a leitura de quem leva o debuff (duas mitigações caem, não uma). `Multiplicative:.5` = −50% está provado pelo irmão `Transcendence` ("Reduces @Max Health@ by {50,35}%" = `MaxHealth:Multiplicative:{.5,.65}`, já `revisado`) | **PENDENTE no mod** (§5) |
| `Warrior's Blade` | `DamageMod:Base:50`; o texto é "Damage increased **50%.**" — falta o `by`. Os irmãos de efeito idêntico escrevem com a preposição: `Destructive` ("Damage increased **by** 50% ", `revisado`), `Empowered Blood` ("Increases damage dealt **by** 50%.", `revisado`). O RV-19 §2 confirma que este status é o `Warrior Shrine Explosion` (+50%, valor fixo) | **PENDENTE no mod** (§5) |

**`sem-explicacao` (1):** `Rune of Exploding` — descrição **vazia** no asset (`descricao=''`),
`efeitos` vazios; é o status invisível do rune (a skill `Rune of Exploding` é quem explica a
mecânica, em `skills.csv` l.338). Não há texto a revisar e chave vazia não serve ao mod (casaria
qualquer descrição vazia — precedente do `Test Fortune`, RV-9).

**`revisado` (29)** — o texto está de pé. As provas, agrupadas por tipo:

- **Texto idêntico a um asset JÁ revisado (mesma chave, mesmo dono de família)** — `Burning Aura`
  ×2 (`Aura of Flame`, revisado, e o mod já carrega a nota "The aura reaches 3 hexes from its
  source." nessas duas chaves exatas), `Chilling Aura` (`Aura of Frost` ×2), `Chained`
  (`Immobilized`; ambos `Rooted:Set:1`), `Ignite` (`Burning Ground`/`Meteor`), `Tadashi's Armor`
  (`Ghost Armor`, e o asset do Ghost Armor prova a mecânica: a porta é
  `Target["GhostArmorValue"] <= 0`), `Tadashi's Ritual` (`Dark Ritual`/`Cursed Coin`, todos
  `DarkRitual:Set:1`), `Witch's Brew` (`Wilting`, `Recovery:Percentage:-30` idêntico).
- **Efeito confere número por número**: `Berserker's`-familiares `Emperor's Blessing`
  (MaxHealth/MaxMana/DamageMod 10), `Edwin's Enchantment` Common (`DamageMod:{50,50}` +
  `MaxHealth:{-50,-50}` — e "Damage **and healing**" está certo: `DamageMod` entra na cura pelo
  `DamageModHealing`, l.31751-31762), `Dwarf King's Rage` (irmão `Rage of the Dwarf King`, mesmo
  efeito, `revisado`), `Marked Prey`, `Pirate's Rum`, `Blackbeard's Curse` (irmãos `Invincible` /
  `Cannot take damage.`, `Invincible:Set:1`; `ModifyHealth` retorna antes do dano, l.40341-40343),
  `Edwin's Enchantment` Fortune (`ManaPowerMod:{25,50}` + `HealthAsManaCost:Set:{100,100}`: o
  teste do próprio jogo diz "Fireball costs no mana on this caster" quando o `HealthAsManaCost`
  pega — o mana passa a ser pago em vida), `Marked Prey`/`Immortal Night` ("per stack" com
  `maxStk` explícito).
- **`[0]`/`*0` com expressão real no asset**: `Vengeful Shadows` — o objeto
  `Enemy_Status_Vengeful Shadows` traz `Source.SpellPower() * 1f * Source.DamageModShadow` como
  expressão da descrição (e a skill passiva homônima concede
  `DamageReturnedFlatShadow:Base:Source.GetFlatDamageValue * 3`, `revisado` com "Grants [0] Return
  Shadow Damage."). `Freeze Earth` — a skill diz "applying 1 stack of Chilled to enemies that
  enter" (mesmo "1"), e `Chilled` existe e empilha (5 stacks = congelado). `Frost Nova` — o status
  aplicado é `Rooted:Set:1`, igual ao `Immobilized` revisado.
- **Chance/trigger provados fora do status**: `Cupid Shot` e `Mind Blossom` ("Charmed",
  `TeamIndexOverride:Set:Source.TeamIndex + 1`): o teste do JOGO no assembly diz
  `RNG_5_A3_Cupid Shot | RNG_Status_Cupid Shot | TeamIndexOverride is … on the charmed enemy |
  PASS: Cupid Shot charmed the target` — o alvo passa a lutar pelo seu time, que é o que "Charmed"
  diz; a skill já dá a duração ("Charm the enemy target for 1 turn", `dur=1`). `Stoney Visage` —
  o status `Petrification` existe e é documentado ("Each stack lowers Movement by 1 and increases
  Damage Taken by 20%. When you reach 5 stacks you become Petrified"), consistente com "1 stack"
  por golpe. `Brawler's Brew` — `MightBase:{12,60}` bate com "@Might@ increased by {12,60}"
  (irmão `Might of the Warrior`, `revisado`); a segunda frase é gatilho (Blind no início do turno),
  não atributo.
- **Famílias de "Mark"** (`Bounty Hunter's Mark`, `Tracker's Mark`, `Stalker's Mark`): os dois
  números do texto são exatamente os dois campos do asset (`CritChanceTarget:8/12` →
  "Chance of suffering critical strikes increased"; `DamageReduction:-15/-25` →
  "Damage taken increased", a camada é `1 − (DamageReduction+…)/100`, l.39472). Os três escrevem a
  mesma frase com os números trocando junto com os campos — o instrumento (o campo) e o texto
  concordam em três assets homólogos, que é o padrão de prova usado nos lotes do RV-9.

---

## 3. Artifacto achado no caminho: o nome de asset cruzado dos "Slow Poison Aura"

Os dois `pendente` chamados **`Slow Poison Aura`** (`Applies bleeding…` e `Slows and applies
poison…`) e o `Blood Mist` **não** são o mesmo objeto, e os nomes no asset estão cruzados:

| objeto no `resources.assets` | nome do status | texto |
|---|---|---|
| `[RisenWitch] Blood Aura` (@1517437088) | **Slow Poison Aura** | "Applies bleeding to enemies in range." |
| `[RisenWitch] Blood Aura_Trigger` (@1517437916) | **Blood Mist** | "Applies Bleeding to enemies in range." |
| `[Witch] Slow Poison Aura` (@1517439760) | **Slow Poison Aura** | "Slows and applies poison to enemies in range." |

Ou seja: o nome "Slow Poison Aura" foi reaproveitado num objeto que **não** é o de veneno, e o
texto (fonte da verdade do tooltip) está **certo em cada objeto** — quem confere por *nome* se
engana, quem confere por *texto* acerta. Registro de dado, não defeito de texto: as duas linhas
saem `revisado` e o censo continua casando por texto (não renomear nada — o mod e o censo casam
por descrição).

---

## 4. As 22 `indeterminado` — o que foi promovido e com que prova

Regra aplicada para não fazer do `indeterminado` um depósito de dúvida: **promove-se quando algum
artefato do install afirma o mesmo número/mecânica que o texto**; mantém-se quando um **número
mecânico afirmado pelo texto não tem artefato nenhum** (o resto é declarado em §6).

### 4.1 Promovidas a `revisado` (5) — prova nova, byte scan no `resources.assets`

| entrada | prova (artefato × texto) |
|---|---|
| `Decay Shrine Aura` — "Take [0]% of your Max Health in Shadow Damage per turn." | fórmula da AÇÃO `Decay Aura Proc` (UTF-16 @1519519282, idem RV-19 §4.2): `TargetStored["ShadowDamage"] = Mathf.Round((Target["MaxHealth"] * Target.GetValueByEnemyType(.05f,.1f,.12f,.15f,.2f,.1f)) * (1 + Source["ShrineEffectBonus"]/100))` — o `[0]` é a % da **vida máxima do alvo**, 10% para player (= a base do asset) e por turno. Confirmado no cache compilado do assembly (RV-19, l.87116/87118). |
| `Curse of Death` — "Cursed to die when this status expires." | o objeto `Enemy_Status_Curse of Death` (@1517243661) traz, no campo de expressão **da própria descrição**, `Target["Health"] = 0` — é literalmente morrer quando expira. Era o "efeito de expirar não está em campo nenhum" do RV-13 §5. |
| `Ruby of Rancor` (Common) — "3 extra Action Points granted. Mana Costs reduced by {25,100}%. Die at the end of your turn." | (a) `Target["ActionPoints"] = Target["ActionPoints"] + 3` na ação @1519438336, ao lado do nome "Ruby of Rancor"; (b) `Source.Kill()` dentro do mesmo status (@1517259112) = "die at the end of your turn"; (c) `ManaCostMod:Set:{-25,-100}` = o `{25,100}%` do texto. |
| `Poison Thorns` — "Attackers take 2 stacks of poison." | o objeto do status (`Enemy_Status_Poison Thorns`) e, em segundo artefato, a habilidade que o aplica — `[Twisted Soul] Poison Thorns` (@1519365489 — ação, com o par `Cell.HasEnemy(Source) && Cell.InRange(Target.Cell, 2)`) cuja descrição completa, escrita pelo jogo, é "Wreaths the target in poisonous thorns.  **Attackers take 2 stacks of poison.**" O irmão `Venomous Skin` (3 stacks) é provado por teste do jogo (RV-9, l.194858). |
| `Everlasting Sacrifice` — "@Holy Power@ increased by {50,100}%. Take 20% of your Max Health in Holy Damage each turn." | (a) o status (@1520168296) tem `DamageModHealing:Base:{50,100}` = o "Holy Power" e o texto completo; (b) a AÇÃO `Everlasting Sacrifice Proc` (@1519413720) traz `TargetStored["HolyDamage"] = Target.MaxHealth * .2f` — os 20% por turno, exatamente. Era o "campo seria a ação de tick, que o dump não exporta". |

### 4.2 Reclassificada (1)

- `Burning Demon Hearts` — `indeterminado` → **`sem-explicacao`**: `QuestItem/Common` com
  descrição **vazia**, `efeitos` vazios, `dur=0`; nenhum item/afixo/expressão do jogo com esse
  nome. É marcador de quest sem texto — a mesma família dos 19 `sem-explicacao` já registrados
  (RV-13 §5). Não havia o que indeterminar: não existe texto a revisar.

### 4.3 Mantidas `indeterminado` (16) — agora com o motivo localizado

O motivo comum do RV-13 ("não há campo") foi **substituído por um motivo nomeado**, e isso agrupa
as 16 em 4 lacunas de dump/fonte (é isto que o próximo ciclo precisa exportar/ler):

**(a) campo `Charges`/`Cooldown` das Fortunes — 6 entradas, a maior lacuna** — `Phoenix Feather`
("1 charge per Quest"; os 20% **estão provados**: `Source["Health"] = Source["MaxHealth"] * 0.2f`
dentro do próprio asset @1520179216, o que fecha a ponta solta do RV-9), `Rune of Refreshment`
("1 charge per battle"; o custo **está provado**: `["MaxMana"] * .75f` + `Source.ManaRatio > .75f`
na ação @1519439256, e o `Character.ResetCooldowns` do RV-9 para o "reset all cooldowns"),
`Ruby of Rancor` (Mythic — "1 charge"; os outros três fatos do texto estão provados na entrada
Common, §4.1), `Transcendence` ("4 charges per battle"; o `{50,35}%` já estava provado por
`MaxHealth:Multiplicative:{.5,.65}`), `Oculus Gem` ("4 turn cooldown"; o *teleporte ao ser
atingido* está provado pela ação `[Oculus Gem] Teleport` @1519492521, com target `ClosestOpenSpace`),
`Elixir of the Scarlet Ox` ("1 additional Action Point and 3 Movement Points… 1 charge" — a Fortune
tem `efeitos` vazios e a ação @1519408608 só dá os flags de alvo).
**O que falta:** exportar no `RoguelikeDebugger` os campos de carga/recarga da Fortune (o dump de
`[Item]` não lista as Fortunes). Um único campo fecha 6 das 16.

**(b) `MaxStacks` por asset — 2 entradas** (`Anthulk Venom` Common "Stacks up to 10 times." e
Mythic "Stacks up to 5 times."): a coluna `maxStk` sai **`VAR`** porque existem assets homônimos com
valores diferentes e o dump não separa por asset (o campo é `ActionStatusInfo.MaxStacks`, l.319149).
**O que falta:** o dump passar a exportar `MaxStacks` **por guid** (não agregado por nome).

**(c) valor dentro de trigger/efeito serializado (chance ou cura) — 3 entradas** —
`Anthulk Carapace` ("50% chance to cast Anthulk Spines when struck.": o objeto
`Enemy_Anthulk Carapace` @1517239830 tem `Effects` (referências `Burst2Flame.IEffectInfo` + ação)
mas **nenhum texto de gatilho**, e "Anthulk Spines" não existe como nome de ação em lugar nenhum do
install), `Champion of Blood` ("heals the Countess for 10% of her Max Health" — o objeto
`Enemy_Champion of Blood Status` @1517241790 não tem fórmula de cura e "Countess" só aparece em
diálogo de quest), `Frenzy` ("Action Points Increase by 1." — o objeto é o
`Goblin Battle Standard Explosion Status` @1517122904, efeitos vazios; a ação
`Goblin Battle Standard Explosion` @1519553208 existe mas não publica valor de AP; nenhuma
expressão `["ActionPoints"] + 1` existe no jogo — só a do Executioner e a do Ruby of Rancor `+3`).
**O que falta:** dump de `SkillTriggers`/`ActionsOnTick` + `Effects[].Action` das ações soltas
(itens de RV-19 §7, ainda abertos).

**(d) stats da forma — 5 entradas** (`Shapeshift: Black/Blue/Green/Red/White Dragonkin`): "Gain new
abilities" está provado (as skills da forma vêm do `ModelChangeCharacter`), mas *"Armor and X
Resistance increased"* não tem par: o status tem `AttributeEffects` vazios (o efeito é o
`ModelChangeCharacter`) e os números vivem no `CharacterInfo` substituído. Byte scan do
`Shape Red Dragonkin` (@1633826336) confirma que a forma usa `Enemy Prefabs\Summons\Dragonkin
**Red**` (o par cor↔prefab está certo), mas os atributos do `CharacterInfo` são campos binários.
**O que falta:** dump dos stats do `CharacterInfo` da forma. O caso `Red` continua sendo o mais
suspeito (as habilidades são de fogo e o texto diz "Cold Resistance" — cópia literal do Azul),
e é **decisão humana**: nenhuma das duas redações tem campo que a confirme.

---

## 5. Correções decididas que ficaram para o mod (`corrigido`, não aplicadas)

Nada de código foi tocado nesta rodada. Para o próximo agente que editar o
`BetterTooltips/Patches/LocalizePatch.cs` (e rodar o passo 3/4/5 do ritual: `check_dupes`,
`check_notas_redundantes`, `check_chave_compartilhada --estrito`):

```csharp
// RV-13b: Raise Skeletal Lackey | o efeito reduz CINCO coisas e o texto listava quatro (falta Magic Armor)
{ "Max Health, Damage, Armor, and Dodge Chance reduced by 50%.",
  "Max Health, Damage, Armor, Magic Armor, and Dodge Chance reduced by 50%." },
// RV-13b: Warrior's Blade | preposicao doente na familia (Destructive/Empowered Blood escrevem "increased by 50%")
{ "Damage increased 50%.",
  "Damage increased by 50%." },
```

Conferências antes de commitar: **1 dono cada** (checado agora — `status.csv` tem exatamente uma
linha com cada texto, então não há risco de chave compartilhada / BUG-32), e **nenhuma das duas
chaves existe hoje** em `TextFixes` nem em `TextAppends` (varredura do `LocalizePatch.cs`).
As outras duas `corrigido` (`Berserker's Rage`, `Immortal Night`) **já têm a entrada no mod** —
RV-14, linhas 1470 e 1498 — e só faltava o veredito no CSV.

> As 5 promoções de §4.1 e as 3 que só tiveram o motivo refinado **não** pedem edição de texto: o
> texto delas é verdadeiro. O que o RV-19 §6.1 propõe (notas para a família de shrines, incluindo
> `Decay Shrine Aura`) continua sendo **proposta de RV-19/RV-22**, não deste fechamento.

---

## 6. Cobertura final — como os números saíram

Script de contagem (`%LOCALAPPDATA%\hermes\cache\scratch\rv13\`): `dump.py` (fila bruta),
`sib.py` (irmãos por efeito/texto), `modgrep.py` (chave já no mod), `scan*.py`/`asset*.py`/`act.py`
(byte scan no `resources.assets`), `dll.py` (strings UTF-16 do `Assembly-CSharp.dll`),
`apply.py` (grava os vereditos, com asserção de que a fila tocada é **exatamente** 34+22 e que o
resíduo são as 16 mantidas por nome). O `apply.py` aborta se um nome/descrição casar 0 ou 2 linhas
— foi assim que os pares homônimos (`Burning Aura`, `Slow Poison Aura`, `Raise Skeletal Lackey`,
`Edwin's Enchantment`, `Ruby of Rancor`, `Anthulk Venom`) foram casados por **asset**, e não por nome.

**Distribuição de `revisao` no `status.csv` antes × depois:**
`revisado 470 → 504` · `corrigido 15 → 19` · `sem-explicacao 19 → 21` ·
`indeterminado 22 → 16` · `pendente 34 → 0`.

**Medido agora nos 5 CSVs do "X de X"** (`scratch/rv13/conta.py`, módulo `csv`):
`skills.csv` 451 → `revisado 309 · corrigido 102 · intocavel 31 · sem-explicacao 9` ·
`status.csv` 560 → `504 · 19 · 21 · 16` ·
`itens.csv` 905 → `782 · 9 · 113 · indeterminado 1` ·
`afixos.csv` 285 → `277 · 8` ·
`powerups.csv` 79 → `79 revisado` ·
**total 2.280 → 1.951 revisado + 138 corrigido + 143 sem-explicacao + 31 intocavel + 17
indeterminado, com `pendente = 0` em todas as cinco.** Revisáveis = 2.249 (2.280 − 31).

**Corpora de apoio (fora do "X de X", RV-13 §7.4):** `acoes.csv` (276) e `invocacoes.csv` (18)
seguem com `status = pendente` e `skills-detalhe.csv` (453) não tem a coluna — os três com **0
descrições não-vazias**, confirmado agora. Nunca foram checklist de tooltip (servem à conferência
do `*N` das skills); "cobertura total" vale para as 5 categorias, como o RV-13 já declarava.

**O critério de pronto do ticket (RV-13 §8):**

| critério | estado agora |
|---|---|
| "Nenhum item do censo sem status" | **CUMPRIDO na planilha**: 0 `pendente` nas 5 categorias (451 + 560 + 905 + 285 + 79 = 2.280) |
| "Relatório final com contagem" | **este documento**: 2.280 de 2.280 (100%); 2.249 de 2.249 revisáveis |
| "Lista das exceções conscientes" | 31 Bard `intocavel` + 143 `sem-explicacao` + **16 `indeterminado`** (§4.3, com a lacuna nomeada) + a decisão adiada dos 67 textos com espaço no fim |
| "Registrar no quadro" | **fora desta rodada**: o KANBAN é nota de trabalho não versionada e um subagente não altera o quadro — cabe ao pai/humano anotar o número |

**Continua fora do censo (escopo declarado, RV-12):** tutoriais/mensagens de sistema, strings de
UI, texto de quests/eventos fora dos 20 status `Quest`/`QuestItem` e descrições de ação. E a
**conferência visual humana** (passo 5 do `release-check`, tabela A do `REVISAR-AO-FINAL.md`) segue
sendo passo humano, não cobertura.

---

## 7. RV-13c — fechamento por ASSET das 16 `indeterminado` (leitura direta do `resources.assets`)

> **Rodada:** 30/09/2026. Método: leitura do `resources.assets` do install por **typetree gerado
> dos DLLs do jogo** (`UnityPy 1.25.3` + `TypeTreeGeneratorAPI 0.10`, com os `.dll` de
> `…/Stolen Realm_Data/Managed/`), mais **byte scan dentro do objeto** (mesma técnica do RV-13/RV-19).
> Bancada: `%LOCALAPPDATA%\hermes\cache\scratch\rv13c\` (`q.py`/`q2.py` leitura tolerante,
> `nameindex2.py` índice nome→asset das 314.468 `MonoBehaviour`, `inv_status.py` inventário dos 424
> `ActionStatusInfo`). **O mod NÃO foi editado** (nenhum `.cs`, nenhum build): mudou só o
> `docs/cobertura/status.csv` e esta seção.

**Aviso de método (endereços):** os `@NNN` do RV-13b são o offset da **string** no
`resources.assets`, não do objeto (o objeto começa antes: `Shape Red Dragonkin` string
@1633826336 → objeto @1633826304, 552 B). Aqui todo endereço é o `byte_start` do objeto; onde a
prova é um campo, o deslocamento é `rel` (relativo ao `byte_start`).

| veredito | antes | depois | quais |
|---|---:|---:|---|
| `revisado` | 504 | **517** | 13 das 16 |
| `corrigido` | 19 | **20** | `Shapeshift: Red Dragonkin` |
| `indeterminado` | 16 | **2** | `Champion of Blood`, `Frenzy` |

### 7.1 As 6 Fortunes — carga/recarga (grupo a) — **fechado**

O campo que o dump não exportava é o do **`ActionInfo`**: `HasCharges`, `MaxCharges`,
`InitialCharges`, `ChargesPerBattle`, `ChargesPerTurn`, `StartingBattleCharges`
(l.317259-317266 do decompilado). Para Fortune implementada como `EventStatus`, o número mora no
`SkillTrigger` (`MaxNumUses`, `Cooldown`).

| entrada | asset (nome do objeto · pid · byte_start · tam.) | campo = valor | texto |
|---|---|---|---|
| `Rune of Refreshment` | `Rune of Refreshment` · 2544260 · 1519439224 · 2920 B | `HasCharges=1`, `MaxCharges="1"`, `InitialCharges="1"`, `ChargesPerBattle="1"`, `StartingBattleCharges="1"`, `Cooldown="0"` | "1 charge per battle." ✔ |
| `Transcendence` | `Transcendence` · 2544265 · 1519452800 · 2636 B | `MaxCharges/InitialCharges/ChargesPerBattle/StartingBattleCharges = "4"` (e `Cooldown="1"`) | "Grants 4 charges … per battle." ✔ |
| `Elixir of the Scarlet Ox` | `Elixir of the Scarlet Ox` · 2544249 · 1519408576 · 3164 B | os cinco campos `= "1"` | "1 charge." ✔ |
| `Ruby of Rancor` (Mythic) | `Rune of Energy` (ação) · 2544259 · 1519438336→objeto @1519436376 · 2848 B | `HasCharges=1`, `MaxCharges/InitialCharges/ChargesPerBattle/StartingBattleCharges="1"`, `ActionNameOverride="Ruby of Rancor"`, `StatusEffects=[2543378]` | "Grants 1 charge of Ruby of Rancor" ✔ |
| `Oculus Gem` | `Oculus Gem` (EventStatus) · 2545458 · 1520177624 · 576 B | `SkillTriggers[0]`: `Cooldown=4.0`, `TriggerType=1` (OnGettingHitDamaging), `Actions=[2544279 "[Oculus Gem] Teleport"]` | "Teleports you randomly when struck. 4 turn cooldown." ✔ |
| `Phoenix Feather` | `Phoenix Feather` (EventStatus) · 2545461 · 1520179184 · 660 B | `SkillTriggers[0]`: `MaxNumUses="1"`, `Cooldown=0.0`, `TriggerType=9` (OnDeath), `Condition="Source.HasDied"` | "1 charge" ✔ (ver ressalva) |

Cadeia do Ruby of Rancor: `EventStatus "Ruby of Rancor"` (2545465) → `GrantedSkills=[2547708]` →
`SkillInfo "Rune of Energy"` (`SkillName="Ruby of Rancor"`) → `ActionsGranted=[2544259]` → a
`ActionInfo` da tabela acima.

**Ressalva (`Phoenix Feather`, "per Quest"):** o `SkillTrigger.ReplenishMaxUseFrequency` do asset
é **2 (`PersistentDurationType.Battle`)** — e nos 26 triggers dos 424 `ActionStatusInfo`
inventariados **só existe** esse valor (2), que também é o *default* da classe (l.45824). O campo
portanto não distingue Quest × Battle e **não** refuta o "per Quest" do texto; o que o asset
afirma é o número ("1"). A linha entra `revisado` com este registro.

### 7.2 `MaxStacks` por asset (grupo b) — **fechado**

A coluna `maxStk` saía `VAR` porque o censo agrega por **nome** e existem **dois** assets com
`Name = "Anthulk Venom"` (raridades diferentes):

| objeto | pid | byte_start | tam. | `Name` | `Description` | `MaxStacks` |
|---|---:|---:|---:|---|---|---:|
| `Anthulk Venom Status` | 2543254 | 1517134152 | 968 B | Anthulk Venom | "…Stacks up to 10 times." | **10.0** em `rel604` (`00 00 20 41`) |
| `Event_Status_Claw of the Anthulk` | 2543372 | 1517252640 | 1020 B | Anthulk Venom | "…Stacks up to 5 times." | **5.0** em `rel656` (`00 00 A0 40`) |

Prova do offset: o bloco `[Infinite=1][Duration="3"][ExpireType][TickType][StackBonusMultiplier=0.0]
[MaxStacks]` é o mesmo do `Enemy_Champion of Blood Status` (2543361), que o node lê **EXATO** byte
a byte e cujo `MaxStacks` é `1.0` — nos dois assets acima o mesmo bloco termina em `10.0` e `5.0`.
As duas linhas ficaram `revisado` e a coluna `maxStk` recebeu o valor **por asset** (10 e 5), que
é o que o RV-13b §4.3(b) pedia ("exportar `MaxStacks` por guid").

### 7.3 Chance/cura dentro de trigger (grupo c) — 1 de 3 fechado

**(c1) `Anthulk Carapace` — FECHADO.** O valor não está no status: `Enemy_Anthulk Carapace`
(2543359, 1517239792, 820 B) tem `SkillTriggers=[]`, `AttributeEffects=[]`, `EffectOverrides=[]`,
`MaxStacks=1.0`. Está no **`CharacterInfo` da criatura `Anthulk`** (2545015, 1519781040, 1712 B),
`SkillTriggers[1]`:

- `TriggerType = 1` = **OnGettingHitDamaging** ("when struck"; enum em l.45741)
- `Actions = [2544014 "Anthulk Spine Explosion"]`
- `ActionChanceEquations = ["50"]` — bytes do array em `rel1020..1031`: `01 00 00 00 | 02 00 00 00 | "50"`

No mesmo `CharacterInfo`, `SkillTriggers[0]` (OnHittingDamaging, condição
`ActionProperties.IsAttackPowerBased && Source.IsEnemy(Target)`) aplica
`ActionStatuses=[2543254 "Anthulk Venom Status"]` — o par ataque→veneno do inimigo. → `revisado`.

**(c2) `Champion of Blood` — não fechou (campo nomeado).** O status (`Enemy_Champion of Blood
Status`, 2543361, 1517241752, 848 B) não tem fórmula: `SkillTriggers=[]`, `AttributeEffects=[]`,
`EffectOverrides=[]`, `ActionsOnTick=[]`, e o único PPtr é o `ActionStatusVisualSet`. O elo está no
`CharacterInfo` do invocado (`Champion of Blood`, 2545036, 1519805784, 1072 B): `SkillTriggers[0]` =
`TriggerType 0` (OnHittingDamaging), `Condition="Source.SummonMaster != null"`,
`Actions=[2544142 "[Countess] Vampire Hit Heal"]`, `Targets="Cell == Source.SummonMaster.Cell"` —
ou seja "striking enemies" + "heals the Countess" estão provados; `CharacterEffects = [LifeSteal 100
(Base), OpportunityAttack Set 1]`.

**Falta o "10%".** Não está em nenhum campo do status, do `CharacterInfo` nem da `ActionInfo`
2544142 (2980 B: nenhum PPtr e nenhuma string de fórmula — só os alvos `Cell == Target.Cell` e
`Cell.InRange(Target.Cell, 3)…`). O campo é **`ActionInfo.Effects`** (§7.5). → continua
`indeterminado` com esse motivo.

**(c3) `Frenzy` — não fechou (campo nomeado).** O status é o `Goblin Battle Standard Explosion
Status` (2543242, 1517122872, 808 B; `Name="Frenzy"`, `Description="Action Points Increase by 1."`):
os bytes do objeto **não têm nenhum PPtr para `CharacterAttribute`** e `AttributeEffects=[]`,
`SkillTriggers=[]`, `ActionsOnTick=[]`, `EffectOverrides=[]`. A ação que aplica o status (`Goblin
Battle Standard Explosion`, 2544300, 1518747520, 2860 B) só referencia 2543242 (o próprio status) e
o `ActionStatusVisualSet` — o `Effects` dela também é invisível ao node.

A forma canônica do "+1 AP" no jogo, provada em quatro irmãos: `AttributeEffects =
[{CharacterAttribute = **2544324 `ExtraTurnActionPoints`**, Method = Base, Amount = "1"}]` em
`Incalculable Rage` (2543365), `Rampage` (2543367 e 2543567), `Growing Hatred` (2543464) e
`Ruby Rancor Enemy` (2543476). No `Frenzy` esse array está vazio → o número não está no asset do
status. → continua `indeterminado` com esse motivo.

### 7.4 Stats da forma (grupo d) — **fechado** (4 `revisado` + 1 `corrigido`)

O status não carrega os números (`AttributeEffects=[]`, como o RV-13b suspeitava); quem carrega é o
**`CharacterInfo` apontado por `ModelChangeCharacter`**, no campo `CharacterEffects[]`
(`CharacterAttribute` + `CharacterEffectMethod` + `Amount`):

| entrada | status (pid) | `ModelChangeCharacter` | `CharacterEffects` (Amount) | texto |
|---|---|---|---|---|
| Black | `NAT_Status_ShapeshiftBlackDragonkin` (2543452) | **2548207** `Shape Black Dragonkin` | `Armor 6*Source.Level` + **`LifeOnHit 8`** + `DamageReduction 20` | "Armor and Damage Reduction increased." |
| Blue | `…BlueDragonkin` (2543453) | **2548208** `Shape Blue Dragonkin` | `Armor 6*Source.Level` + **`ResistCold 30`** (`BasicEffects.coldResist` ainda = 20) | "Armor and Cold Resistance increased." ✔ |
| Green | `…GreenDragonkin` (2543455) | **2548210** `Shape Green Dragonkin` | `Armor 6*Source.Level` + **`ResistLightning 30`** | "Armor and Lightning Resistance increased." ✔ |
| **Red** | `…RedDragonkin` (2543456) | **2548211** `Shape Red Dragonkin` | `Armor 6*Source.Level` + **`ResistFire 30`** | "Armor and **Cold** Resistance increased." ✗ |
| White | `…WhiteDragonkin` (2543459) | **2548213** `Shape White Dragonkin` | `Armor 6*Source.Level` + `DamageReduction 20` | "Armor and Damage Reduction increased." ✔ |

Atributos resolvidos pelo pathID: 2544401 `Armor`, 2544414 `DamageReduction`, 2544459 `LifeOnHit`,
2544495 `ResistCold`, 2544498 `ResistFire`, 2544499 `ResistLightning`.

- **`Shapeshift: Red Dragonkin` → `corrigido`.** A forma concede `ResistFire 30`; o texto diz "Cold
  Resistance" — é o texto do Azul. Correção **decidida e não aplicada** (entra no dicionário do
  `BetterTooltips/Patches/LocalizePatch.cs`, não nesta rodada):
  `"Armor and Cold Resistance increased."` → `"Armor and Fire Resistance increased."`
- **`Shapeshift: Black Dragonkin` → `revisado` com registro.** As duas stats que o texto nomeia
  existem (`Armor`, `DamageReduction`), mas a forma concede **também `LifeOnHit 8`**, que o texto não
  menciona (omissão — mesma família do caso `Raise Skeletal Lackey` do §2). Fica como **decisão
  humana**, registrado como o **segundo caso mais suspeito** da lista (depois do Red).
- Azul/Verde/Branco: campo e texto concordam número por número → `revisado`.

### 7.5 O que ficou aberto e como fechar (próximo ciclo)

Os 2 `indeterminado` restantes têm **uma causa só**: o node de typetree gerado a partir do
`Assembly-CSharp.dll` do install **não inclui os campos de efeito serializados por referência de
interface**:

- **`ActionStatusInfo.Effects`** e **`ActionInfo.Effects`** (`IEffectInfo[]`, l.317229 do
  decompilado): a classe declara, o node não tem (node do `ActionStatusInfo` = 98 campos de nível 1;
  node do `ActionInfo` = 168; `Effects` não está em nenhum dos dois; `ActionStatusInfo.Guid` também
  não). O asset **tem** conteúdo nesse campo — prova: em `Anthulk Venom Status` (2543254) a string
  `"ActionStatus.GetFlatDamageValue * .5f"` aparece **duas** vezes, em `rel360`
  (`DescriptionExpressions`) e em `rel520` (dentro do array de `Effects`, precedida do PPtr para
  **2544358 `DamageFlatPhysicalTarget`**). É esse elemento que desalinha a leitura do objeto a partir
  daí (`read_typetree` estoura o `byte_size`); onde o array é vazio — `Enemy_Anthulk Carapace` — o
  node lê o objeto **o byte a byte, exato**.
- **Como destravar:** (1) no `RoguelikeDebugger`, exportar `s.Effects.Length` **e o tipo concreto de
  cada elemento** (`s.Effects[i].GetType().Name`) + o `CharacterAttribute` do elemento — o dump atual
  só publica `GeneralEffect.Action` (`efeitosDano`), e o cast `as GeneralEffect` devolve `null`
  justamente nesses elementos (por isso `efeitosDano` sai vazio em `Anthulk Carapace` e `Frenzy`);
  ou (2) ler `Effects` pelo registro de referências (`references`/`ManagedReferencesRegistry` no fim
  do objeto) com o UnityPy, como foi feito aqui.

---

*Fontes: `docs/cobertura/*.csv` (os 8), `docs/cobertura/revisao/` (RV-9 buffs/debuffs, RV-13,
RV-14, RV-19, BUG-32-chaves-compartilhadas), `BetterTooltips/Patches/LocalizePatch.cs`,
`resources.assets` do install atual (byte scan por offset; os offsets citados são do arquivo de
30/09), `Assembly-CSharp.dll` (strings UTF-16), e as ferramentas `censo_status.py`,
`check_fix_keys.py`, `check_dupes.py`, `check_chave_compartilhada.py`, `audita_docs.py`.
**§7 (RV-13c):** `resources.assets` lido por **typetree gerado** dos `.dll` de
`Stolen Realm_Data/Managed/` (UnityPy 1.25.3 + TypeTreeGeneratorAPI 0.10) e os scripts de bancada em
`%LOCALAPPDATA%\hermes\cache\scratch\rv13c\`.*

---

## 8. Reverificação (01/10/2026) — os 5 CSVs × o dump estendido (RD-2R)

> **Rodada somente-leitura nos CSVs.** O que o cartão `t_2ce8a190` (RV-13b) pedia — propagar os
> vereditos de RV-9..RV-12 para as 5 categorias — **já está no disco** e é o que esta seção confere
> contra o dump de hoje. Nenhum campo de descrição foi tocado e **nenhum veredito foi alterado**;
> os conflitos achados ficam registrados aqui (§8.2), não "arrumados".

**Medido agora** (`csv` do Python, os 5 arquivos de `docs/cobertura/`) — `pendente` = **0** em todos:

| arquivo | entradas | revisado | corrigido | sem-explicacao | intocavel | indeterminado | pendente |
|---|---:|---:|---:|---:|---:|---:|---:|
| `skills.csv` | 451 | 309 | 102 | 9 | 31 | 0 | **0** |
| `status.csv` | 560 | 517 | 20 | 21 | 0 | 2 | **0** |
| `itens.csv` | 905 | 782 | 9 | 113 | 0 | 1 | **0** |
| `afixos.csv` | 285 | 277 | 8 | 0 | 0 | 0 | **0** |
| `powerups.csv` | 79 | 79 | 0 | 0 | 0 | 0 | **0** |
| **TOTAL** | **2.280** | **1.964** | **139** | **143** | **31** | **3** | **0** |

`status.csv` bate com o §7 (517/20/21/2) e as duas colunas de revisão seguem idênticas
(`status == revisao` em 0 divergências). **Cruzamento com as fontes** (scripts em
`%LOCALAPPDATA%\hermes\cache\scratch\`): 905/905, 285/285 e 79/79 casaram 1:1 com
`scratch/rv10-12-vereditos.json` (`nota`→`revisado`) e 560/560 com `rv9-buffs-vereditos.json`
(393 buffs) + os 133 debuffs + a fila `?`/`Neutro` (34) — **0 divergência**. E as **descrições** dos
5 CSVs continuam **iguais às do `LogOutput.log`** (0 diferenças por multiconjunto): a propagação
tocou só a coluna `status`.

### 8.1 O instrumento (o que NÃO foi rodado, e por quê)

`census.py` reescreve o `status.csv` com o header de **9** colunas (nome…status); as extras de hoje
(**13** colunas: `revisao`, `beneficio`, `dur`, `maxStk`) **não sobrevivem** a uma rodada dele. Por
isso **nada foi rodado**: `census.py`, `censo_status.py` e `importa_beneficio.py` **não** foram
executados nesta rodada. Se algum campo novo do dump tiver de virar coluna, o caminho do projeto é
um **imersor** no lugar (`importa_beneficio.py` é o modelo; `censo_status.py` preserva as colunas
existentes e só acrescenta `revisao`) — **nunca** mexer no header do `census.py`.

### 8.2 Conflitos registrados (não resolvidos aqui)

1. **Os campos novos do RD-2R não estão no artefato que o censo lê.** A DLL do perfil
   (`…\plugins\RoguelikeDebugger\RoguelikeDebugger.dll`) é de **30/09 21:22** (md5 `28b7959a…`);
   os builds do repo com os campos novos são de **01/10** (`bin/Debug` 13:38, `bin/Release` 14:55).
   O `LogOutput.log` de 01/10 (600 `[Status]`) **não tem** `expr=`, `tick=`, `auraSts=`, `~alvos=`
   nem `~acoes=` — só o formato antigo (`nTrig=… | trigEf=…~cond=~status=`). Ou seja: os dados novos
   existem no **fonte** e no log sintético de bancada, **não** no log de boot. Propagar campo novo
   para CSV hoje exigiria deploy + boot (fora do escopo desta tarefa).
2. **`docs/DEBUGGER.md` atribui ao `EfeitosInfo` o fecho das "duas últimas entradas `indeterminado`"
   — as duas que restam não são aquelas.** `Champion of Blood` e `Frenzy` seguem `nEfeitosTot=0` /
   `efTipos=` / `nTrig=0` no dump e `0` gatilho e `0` `descExpr` na passagem offline dos 421 assets.
   O motivo de continuarem abertas é o do §7.5 (o número mora no `CharacterInfo` / em
   `ActionInfo.Effects`, fora do status), **não** o cast `as GeneralEffect`. O veredito
   `indeterminado` está certo; a narrativa causal do doc é que conflita.
3. **A evidência de RV-9 para as auras de shrine citou `ActionsOnTick`; o RD-2R mediu `0/421` e
   provou `SkillTriggers[].Targets`.** `Decay Shrine Aura`, `Flame Shrine Aura` e `Dwarven Aura`
   seguem `revisado` (o texto é verdadeiro) — o que envelheceu é a **evidência** gravada no JSON/
   workfile ("o proc mora em `ActionsOnTick`, campo que o dump não exporta"): o proc é
   `SkillTriggers[0]` (`Flame` `OnGettingHitDamaging` + `Cell.IsCurrentHex(Target)`; `Decay`
   `TriggerType=4` + `Cell.IsCurrentHex(Source)`). Não usar "provado por `ActionsOnTick`" para
   reconferir. Mesmo caso de `RV-8b-2c-ranger.md` ("o gatilho está no `SkillTrigger`, que o dump não
   traz"): com o `~alvos=` o dump passou a trazer.
4. **Denominadores diferentes (600 × 424 × 421).** O dump imprime **600** statuses; 424 são objetos
   de asset (421 legíveis offline) e ~176 são **sintéticos** criados no boot a partir de `EventStatus`
   (`LoadListActionStatuses`). O censo dedupa para **560** por (nome, descrição) e os 2.280 do RV-13
   saem daí. Os `X/421` do `DEBUGGER.md`/RV-19 e as contagens do RV-13 partem de bases diferentes —
   não re-derivar o censo dos 421.
5. **A família `* Shrine Explosion` (ações) continua fora do dump.** Os *statuses* irmãos
   (`Warrior's Blade`, `Guardian Shield`, `Marked for Death`, `Might of the Conqueror`, `Frenzy`)
   **estão** no censo e com veredito; nenhum veredito depende da ação que não sai. `acoes.csv` e
   `invocacoes.csv` (corpora de apoio, 0 descrições não-vazias) seguem `pendente` — fora do "X de X",
   como o RV-13 §7.4 já declarava.

**Travas no fim desta rodada:** `tools/testes/roda_testes.py` → **20/20, VERDE (exit 0)`;
`check_dupes`, `check_fix_keys` (298 chaves · 294 no censo · 4 fora), `check_notas_redundantes`,
`check_chave_compartilhada --estrito`, `audita_docs`, `checa_citacoes` → **exit 0**.

*md5 dos 5 CSVs nesta rodada (para provar que não foram tocados):*
`skills b8ea3ba3552db6fd585ed6617c92f0ec` · `status 6717cc883680a1a2e9f0de0d1dd123fb` ·
`itens 0d60e284c3add6bf5c10274bac325fb3` · `afixos e320797deb8d709b231bfc415bfd78b6` ·
`powerups 529aa4f6ce4abac864ee0be04a2d7476`.
