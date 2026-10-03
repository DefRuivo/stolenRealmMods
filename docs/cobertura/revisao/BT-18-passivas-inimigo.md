# BT-18 — Passivas de inimigo (`SpecialEffect`): onde mora o valor e como mostrar no tooltip

**Tarefa:** BT-18 (pedido do dono, 02/10). Exemplo dado: *"Redemptive deve informar quanto cura"*.
**Tipo:** investigação **somente-leitura** (não alterei código de mod, não build, não instalei, não abri o jogo, não publiquei, não mexi no kanban, não commitei).
**Data:** 03/10/2026
**Jogo:** Stolen Realm (Unity 2022.3.62, Mono) — `E:\SteamLibrary\steamapps\common\Stolen Realm`
**Fontes:**
- Decompilado de referência: `%LOCALAPPDATA%\hermes\cache\scratch\cs\Assembly-CSharp.decompiled.cs` (linhas citadas como `l.NNNNNN`).
- Cópia local do enum: `scratch/sac1/SpecialEffect.cs` · `scratch/sac1/EnemyMod.cs`
- Data do jogo: `Stolen Realm_Data/resources.assets` (1.723.507.220 bytes) — offsets absolutos citados como `@NNNNNNNNN`.
- Probes de leitura criados para esta investigação: `scratch/bt18/*.py` (não tocam o jogo).

---

## 0. TL;DR (o que o dono precisa saber)

1. **O enum `SpecialEffect` NÃO tem valor nenhum no código.** Ele é uma **etiqueta de exibição**: 90 valores, cada um só com um `[Description]`. A **única** vez que o código lê um valor específico do enum é `SpecialEffect.ManaShield` (l.156807, para esconder a mana bar). Não existe `switch`/`if` que dê número a `Redemptive`, `Regenerating`, `ReflectsDamage`, etc.
2. **O valor de cada passiva vive na DATA**, nos assets `EnemyMod` (`resources.assets`, pasta de Resources **"Enemy Mods"**, carregados por `Game.Instance.EnemyMods = Resources.LoadAll<EnemyMod>("Enemy Mods")`, l.443074). Cada `EnemyMod` tem:
   - `effects` (`CharacterEffectInfo[]`) → contribuição de **atributo**, com `Amount` = **expressão em string** avaliada em runtime por `Game.Eval<float>(amount, {Source=personagem})` (l.37308; aplicado em l.41603-41613 e atributos em l.38314).
   - `skillTriggers` (`SkillTrigger[]`) → comportamentos (`OnDeath`, `OnGettingHitAny`, …), com `Actions` (`ActionInfo[]`), `GeneralEffects`, `ActionStatuses`.
3. **Só 43 dos 90 valores do enum têm um asset `EnemyMod` próprio** (a lista é alfabética de `Beastly Bosses I` a `Vengeful`). Os outros 47 são etiquetas de nível de inimigo (`CharacterInfo.SpecialEffects`) cuja mecânica vive nos atributos/skills daquele inimigo — são "sem valor no código" e também sem asset de mod.
4. **Redemptive:** asset `EnemyMod` com `name="Redemptive"`, `Guid=a2c12466-5127-457b-ad07-f0cbe69b634c`, `description="Heals allies on death"`. **Não há NENHUM literal numérico** para ele na data — o "quanto cura" é delegado a um `skillTrigger` cujas `Actions` referenciam objetos de ação separados (`path_id` 2543785 **"Mass Cure"** e 2543782 **"Holy Ground"**). Ou seja: para o tooltip mostrar o número, o mod tem que **resolver a ação do gatilho em runtime** (ou fixar uma tabela depois de medir em jogo).
5. **Tooltip:** a string `"Heals allies on death"` **não é** o `Description` do enum (esse é `"Redemptive"`, l.179616). É a **chave de localização** `enemyMod-description-<guid>` (valor em inglês = a própria chave), exibida por `Tooltip.ShowUniversalTooltip(Localize(enemyMod.name), "", Localize(enemyMod.description))` em **`ExamineWindow.Update`, l.105319**.
6. **Onde injetar:** o caminho mais cirúrgico é o postfix que o `BetterTooltips` **já usa** (`OptionsManager.Localize`, `BetterTooltips/Patches/LocalizePatch.cs`) para a nota de texto, **e/ou** um prefix/postfix em **`Tooltip.ShowUniversalTooltip`** (definição l.334459) — que é o método que o tooltip do link de passiva de inimigo chama.

---

## 1. O enum `SpecialEffect` — 90 valores, só etiqueta

- Definição: **l.179534-179716** (`public enum SpecialEffect { … }`). Cópia local em `scratch/sac1/SpecialEffect.cs`.
- Cada valor tem um `[Description("…")]`. Contagem: **90 valores** (conferida por script).
- A lista completa (com o texto do `[Description]` e onde mora o valor) está na **§7**.

### 1.1. Prova de que o código nunca dá valor ao enum

Busca por `SpecialEffect` em todo o decompilado (496.253 linhas) devolve **35 ocorrências**, nenhuma atribuindo número. As que importam:

| Ocorrência | Linha | O que faz |
|---|---|---|
| `SpecialEffect[] specialEffects = CharacterInfo.SpecialEffects;` | l.32702 | copia a lista do `CharacterInfo` |
| `Burst2Flame.Game.Instance.SpecialEffectConditions` | l.32707 | acrescenta/remove etiquetas por **condição** |
| `playerInfoWindow … LocalizeEnum(calculatedSpecialEffect, …)` | l.156826 / l.156839 | monta o **texto** (só nome) |
| `examineWindow … LocalizeEnum(list[j], …)` | l.105274 | idem |
| **`SpecialEffect.ManaShield`** | **l.156807** | **única leitura nominal do enum no código** — esconde a mana bar de bosses |
| `HasSpecialEffect(string)` | l.442138-442140 | comparador por `ToString()`; **não é chamado em lugar nenhum** (0 usos) |

Ou seja: **"quanto o Redemptive cura" não existe no enum nem em nenhum método que consuma o enum.**

---

## 2. Como a lista de passivas de um inimigo é montada

`Character.CalculatedSpecialEffects` (getter, **l.32690-32727**):

```csharp
SpecialEffect[] specialEffects = CharacterInfo.SpecialEffects;   // l.32702  (etiquetas do inimigo)
foreach (...) _CalculatedSpecialEffects.Add(item);               // l.32703-32705
foreach (SpecialEffectCondition c in Burst2Flame.Game.Instance.SpecialEffectConditions)  // l.32707
{
    if (!string.IsNullOrEmpty(c.Condition)) {
        bool flag = Burst2Flame.Game.Eval<bool>(c.Condition, new GameFunctionParameters { Source = this }); // l.32711-32714
        if (!Contains(c.SpecialEffect) && flag)  Add(c.SpecialEffect);   // l.32715-32717
        if ( Contains(c.SpecialEffect) && !flag) Remove(c.SpecialEffect); // l.32719-32721
    }
}
```

- `SpecialEffectCondition` = `{ SpecialEffect SpecialEffect; [TextArea] string Condition; }` — **l.444197-444203**.
- `Game.SpecialEffectConditions` é campo `List<SpecialEffectCondition>` — **l.442385**.
- Esses `Condition` são **expressões** avaliadas pelo motor (`Game.Eval<bool>`) e podem adicionar/remover etiquetas dinamicamente.

**Consequência para o tooltip:** a lista exibida não é necessariamente a do asset — pode ganhar/perder etiquetas por condição.

---

## 3. Onde mora o VALOR de cada passiva

### 3.1. `EnemyMod` (asset ScriptableObject do inimigo)

Classe: **l.100097-100098** (`[CreateAssetMenu(menuName="EnemyMod")] public class EnemyMod : SerializedScriptableObject`); cópia local `scratch/sac1/EnemyMod.cs`. Campos relevantes:

```csharp
public string name;              // chave de localização (ex.: "Redemptive")
public string description;       // chave de localização (ex.: "Heals allies on death")
public float experienceModifier;
public float lootModifier;
public bool isAura;
public bool hideInName;
public CharacterEffectInfo[] effects;     // ← VALOR (atributo) AQUI
public SkillTrigger[] skillTriggers;      // ← COMPORTAMENTO (on death, on hit, …) AQUI
public SpecialEffect[] specialEffects;    // etiquetas do mod
...
```

Carga: `Game.Instance.EnemyMods` **l.443067-443084** = `Resources.LoadAll<EnemyMod>("Enemy Mods")` (ordenado por nome). Também em l.172707-172712 (mesma pasta).

**Onde `effects`/`skillTriggers` são aplicados ao personagem:**
- `Character.SetValues` — `effects` → `Effects.Add(unusedCharacterEffectFromPool2.SetValues(characterEffectInfo, …))` — **l.41603-41613**.
- Coleta de atributos — `AccumulateStaticContributors(fromEnemyModDict.effects, characterAttribute, method, …)` — **l.38314** (origem rotulada `"EnemyMods." + mod.name`).
- Triggers — `globalSkillTriggers = enemyMod.skillTriggers;` — **l.34493-34507**.
- Debug/atributo — valor de `Amount` avaliado por `Game.Eval<float>(characterEffectInfo7.Amount, new GameFunctionParameters { Source = this })` — **l.37308-37311**.

### 3.2. `CharacterEffectInfo` — o vetor numérico (`EnemyMod.effects`)

Classe **l.441785-441803**:

```csharp
public EffectTarget EffectTarget;
public CharacterAttribute CharacterAttribute;   // QUAL atributo
public CharacterEffectMethod CharacterEffectMethod; // Base / Percentage / Multiplicative
[Multiline(5)] public string Amount;            // ← EXPRESSÃO (string!)
...
```

- `Amount` **não é um float**: é uma string de expressão (ex.: `"Source.GetFlatDamageValue * 5"`) avaliada por `Game.Eval<T>` (público, **l.443899**), com `GameFunctionParameters { Source, Target, SourceStored, TargetStored, … }` (**l.444204-444229**).

### 3.3. `SkillTrigger` — os comportamentos (é aqui que mora o "on death")

Classe **l.46548-46587**; enum `TriggerType` **l.46513-46546** (30 valores: `OnHittingDamaging=0`, `OnDeath=9`, `AfterMyDeath=15`, `OnAnyDeath=12`, `OnGettingHitAny=21`, …):

```csharp
public TriggerType TriggerType;
[TextArea] public string Condition;        // expressão (ex.: "Cell.IsCurrentHex(Source)")
public ActionInfo[] Actions;               // ← as ações executadas
public string[] ActionChanceEquations;
public GeneralEffect[] GeneralEffects;
public ActionStatusInfo[] ActionStatuses;
...
```

O valor de um comportamento "on death"/"on hit" mora dentro da `ActionInfo` (ou do status) referenciada — **não** no `EnemyMod`.

---

## 4. Prova na DATA (`resources.assets`)

Os assets `EnemyMod` estão em `resources.assets`, **não comprimidos**, serializados pelo Odin (`SerializedScriptableObject`). Formato por bloco: **nome** (UTF-8, com prefixo de comprimento) → **`Guid`** (16 bytes crus) → **`description`** → condições/`Amount` → eventualmente referências (`PPtr`/`ReferencedUnityObjects`).

### 4.1. Localização dos blocos

Região dos `EnemyMod`: **@1520115600 … @1520134408** (ordem **alfabética**, de `Beastly Bosses I` a `Vengeful`). Antes disso há `CharacterInfo` de inimigos (Ghoul/Medusa/Xotec…), depois vêm `EnemySet1..5`.

### 4.2. Tabela extraída (nome → descrição → valor)

Cada linha cita o offset da string `Amount`/descrição como prova.

| EnemyMod (`name`) | `description` (linhas) | Valor / `Amount` | Offset |
|---|---|---|---|
| Beastly Bosses I | 25% increased Health and Damage | `25` | @1520115768 |
| Beastly Bosses II | 50% increased Health and Damage | `50` | @1520116140 |
| Beastly Bosses III | 100% increased Health and Damage | `100` | @1520116508 |
| **Berserking** | Maximum health increased by 25% / Deals more damage at lower health | `Source.HealthRatioInverse * 100` ; `25` | @1520116904 / @1520116976 |
| Burning | Burning Aura | *(sem número — aura/condição)* | @1520117220 (`Cell.IsCurrentHex(Source)` @1520117348) |
| Calamitous Champions I/II/III | 25/50/100% increased Health and Damage | `25`/`50`/`100` | @1520117760 / @1520118136 / @1520118512 |
| Chilling | Chilling Aura | *(sem número)* | @1520118796 |
| Cursed | Applies Curse on striking and when struck | *(sem número)* | @1520119244 |
| Destructive | Damage increased by 50% | `50` | @1520120132 |
| Earthshatter | Casts Earthshatter | *(sem número)* | @1520120384 |
| Elusive | Dodge Chance increased by 25% | `25` | @1520120912 |
| **Explosive** | Explodes on death | *(sem número — ação no gatilho)* | @1520121160 |
| **Freezing** | Freezes all enemies on death | *(sem número)* | @1520121636 |
| Furious Fodder I/II/III | 25/50/100% increased Health and Damage | `25`/`50`/`100` | @1520122192 / @1520122564 / @1520122932 |
| Giant | Damage and Health increased by 25% / Size increased by 25% | `25` ; `25` | @1520123312 / @1520123356 |
| Ice Tomb | Casts Ice Tomb | *(sem número)* | @1520123604 |
| Ignite | Casts Ignite | *(sem número)* | @1520124052 |
| Inspiring | Inspiring Aura | *(sem número)* | @1520124504 |
| Miniature | Movement increased by 3 / Action Points increased by 1 / Max Health reduced by 25% / Damage reduced by 25% | `-25` ; `-25` | @1520125192 / @1520125236 |
| Monstrous Momentum I/II/III | Movement Points increased by 1/2/2 | floats | @1520125496 / @1520125828 / @1520126156 |
| Necromancer | Summons Skeletons. | *(sem número)* | @1520126472 |
| Necromantic | Summons a Skeletal Warrior on death | *(sem número — ação)* | @1520126928 |
| Rampaging | Increased damage by 50% / All resistances lowered by 25% | `50` ; `-25`×4 | @1520127592 / @1520127636… |
| **Redemptive** | **Heals allies on death** | **sem número** (ver §5) | @1520128064 |
| **Regenerating** | Regenerates health every turn. | **`Source.GetFlatDamageValue * 5`** | @1520128628 |
| Resilient | All Resistances increased by 25% | `25`×5 | @1520128980… |
| Savage Soldiers I/II/III | 25/50/100% increased Health and Damage | `25`/`50`/`100` | @1520129492 / @1520129860 / @1520130228 |
| Shocking | Shocking Aura | *(sem número)* | @1520130508 |
| Storm Caller | Casts Storm Call | *(sem número)* | @1520130960 |
| Teleporting | Teleports randomly when struck | *(sem número)* | @1520131416 |
| Toxic | Applies poison when striking / when struck | *(sem número)* | @1520132012 / @1520132041 |
| Undying | Applies Dark Ritual on death | *(sem número)* | @1520132748 |
| Vampire Lord | Vampire Lord Aura | *(sem número)* | @1520133224 |
| Vampiric | Life Steal increased | `50` | @1520133740 |
| Vengeful | Gains increased damage for each ally killed | *(sem número)* | @1520133988 |

> Nota: `Berserking` é o único caso em que o valor **escala com o portador** (`Source.HealthRatioInverse * 100`); `Regenerating` usa `Source.GetFlatDamageValue * 5`. A maioria dos "stat-passives" tem número **fixo** (25/50/100 etc.) e o próprio `description` já o traz.

### 4.3. Como reproduzir a extração

- Strings da região: `python scratch/bt18/strings.py 1520100000 1520134400`
- Despejo por objeto (via `UnityPy`): `python scratch/bt18/obj_dump.py <path_id>`
- Chaves de localização: `python scratch/bt18/keys.py <termo>`

(Há `UnityPy 1.25.3` instalado; o typetree das MonoBehaviours Odin **não** reconstrói — por isso a leitura é feita por strings/offsets.)

---

## 5. `Redemptive` em detalhe (o caso do dono)

**Fatos confirmados:**

1. **Enum:** `SpecialEffect.Redemptive` — l.179616-179617; `[Description("Redemptive")]`. Sem valor.
2. **Chaves de localização** (`resources.assets`, dicionário JSON do `LocalizationData`):
   - `"Redemptive"` (nome; value em chinês 救赎, etc.) — @1101871740
   - `"Heals allies on death"` (a **chave**; value em outros idiomas) — @1102786976
   - `"Redemptive-Code"` (planilha de tradução do enum) — @1136754369
   - `"enemyMod-name-a2c12466-5127-457b-ad07-f0cbe69b634c"` = **"Redemptive"** — @1139114470
   - `"enemyMod-description-a2c12466-5127-457b-ad07-f0cbe69b634c"` = **"Heals allies on death"** — @1139114621
3. **Asset `EnemyMod`** (objeto Unity `path_id=2545350`, `byte_start=1520127944`, `byte_size=484`):
   - `name` = `"Redemptive"` — @1520127976
   - `Guid` = bytes `66 24 c1 a2 27 51 7b 45 ad 07 f0 cb e6 9b 63 4c` (**a2c12466-5127-457b-ad07-f0cbe69b634c**, Guid em little-endian) — @1520128007
   - `description` = `"Heals allies on death"` — @1520128064
   - condição do gatilho = **`"Cell.IsCurrentHex(Source)"`** — @1520128216
   - **Nenhum `Amount` numérico** entre a descrição e a condição → o "on death" é comportamental.
   - O objeto referencia **2 objetos Unity** (`ReferencedUnityObjects`): `path_id` **2543785 = "Mass Cure"** e `path_id` **2543782 = "Holy Ground"** (candidatos às `Actions` do `skillTrigger`).

**Conclusão para o dono:** *"Heals allies on death"* é só a descrição; **o número da cura não está nem no enum, nem na descrição, nem como literal no asset do mod** — está na ação referenciada (a cura provavelmente vem da ação/status de "Mass Cure"/"Holy Ground"). Para o tooltip informar o valor há dois caminhos: **(a)** resolver a ação do gatilho em runtime (ler `skillTriggers[].Actions[].…`/`GeneralEffects`/`ActionStatuses` e avaliar as expressões); ou **(b)** medir uma vez em jogo e gravar uma tabela estática no mod (mais simples e estável para poucos casos).

> **Ressalva honesta:** não consegui extrair estaticamente o número exato da cura do `Redemptive` (a `ActionInfo`/status da ação está em outro objeto, com o conteúdo dentro de blob Odin — o typetree não reconstrói no UnityPy). O valor exato só sai por runtime-probe ou leitura da árvore de ações no jogo.

---

## 6. Tooltip: como é montado de verdade e onde injetar

### 6.1. Funil de nomes: `OptionsManager.LocalizeEnum<T>`

**l.153419-153422**:

```csharp
public static string LocalizeEnum<T>(T original, LanguageGender languageGender = LanguageGender.None)
    => Localize(GUIManager.SpaceOutString(original.ToString()), languageGender);
```

→ para `SpecialEffect.Redemptive`, gera `Localize("Redemptive")` = "Redemptive" (em inglês, `Localize` devolve a própria chave). **Nenhum número.**

### 6.2. `PlayerInfoWindow` (o painel de vida/nome do inimigo)

Classe **l.156739**. Método **`ShowPlayerInfoWindow(Character)` l.156801**. Bloco do texto das passivas — **l.156820-156848**:

```csharp
string text = "";
List<SpecialEffect> list = new List<SpecialEffect>();
if (currentCharacter.CalculatedSpecialEffects != null) {
    foreach (SpecialEffect e in currentCharacter.CalculatedSpecialEffects)
        text += OptionsManager.LocalizeEnum(e, ...) + ", ";               // l.156826  ← SÓ NOME
    list.AddRange(currentCharacter.CalculatedSpecialEffects);
}
if (currentCharacter.EnemyMods != null && currentCharacter.EnemyMods.Count > 0) {
    foreach (EnemyMod enemyMod in currentCharacter.EnemyMods)
        foreach (SpecialEffect original in enemyMod.specialEffects)
            text += "<color=#" + ColorUtility.ToHtmlStringRGB(enemyMod.nameColor) + ">"
                  + OptionsManager.LocalizeEnum(original, ...) + "</color>, ";  // l.156839  ← SÓ NOME
}
specialText.text = text;                                                  // l.156848
```

### 6.3. `ExamineWindow` (painel EXAMINE — o da imagem do dono)

Classe **l.105133**. Método **`ShowCharacterExamine(Character)` l.105180**.

- Lista de passivas de skill + **links dos EnemyMods** — **l.105249-105261**:
  ```csharp
  passiveSkillText.text += "<link=" + idx + "><color=#FFFFFF>[" + OptionsManager.Localize(enemyMod.name) + "]</color></link> "; // l.105259
  ```
- **Texto das passivas especiais (SpecialText)** — **l.105263-105282**: só `LocalizeEnum(list[j])` unido por `"\n"` (**l.105274**). **Nenhum número.**
- **Tooltip do link do EnemyMod** (é o "REDEMPTIVE + Heals allies on death" da imagem) — **l.105316-105320**:
  ```csharp
  else if (passiveLinkList[currentLinkID].enemyMod != null) {
      EnemyMod enemyMod = passiveLinkList[currentLinkID].enemyMod;
      GUIManager.instance.tooltip.ShowUniversalTooltip(
          OptionsManager.Localize(enemyMod.name), "", OptionsManager.Localize(enemyMod.description)); // l.105319
  }
  ```

Ou seja: o par **título = `Localize(enemyMod.name)`** + **corpo = `Localize(enemyMod.description)`** é exatamente o que o dono viu. **O título "REDEMPTIVE" vem do estilo do tooltip e o corpo "Heals allies on death" da chave `enemyMod-description-<guid>`. O `[Description]` do enum (`"Redemptive"`) não é a origem dessa frase.**

### 6.4. `Tooltip.ShowUniversalTooltip` (onde o corpo nasce)

Definição: **l.334459**:

```csharp
public void ShowUniversalTooltip(string title, string subtitle, string description,
        Vector3? targetPos = null, ControlGlyphInfo? controlGlyphInfo = null, string footerText = null)
{ string description2 = ApplyAttributeTextTags(description); ... }
```

### 6.5. Os 3 pontos de injeção possíveis

| # | Ponto | Vantagem | Limite |
|---|---|---|---|
| **A** | Postfix em **`OptionsManager.Localize`** (já usado por `BetterTooltips/Patches/LocalizePatch.cs`, `[HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]`) → muda `__result` quando `original` casar uma chave conhecida | Reusa a arquitetura do mod (tabela `TextFixes`/`TextAppends`); cobre PlayerInfoWindow e ExamineWindow de uma vez | O funil só recebe **a string**, não o personagem → só serve para valor **fixo** ou resolvido por fora |
| **B** | Prefix/Postfix em **`Tooltip.ShowUniversalTooltip`** (assinatura explícita de 6 tipos) | Tem `title`/`description` e pode reescrever o `description` | Idem: sem o `Character` no escopo — precisa casar `description` com `Game.Instance.EnemyMods` |
| **C** | Postfix em **`ExamineWindow.ShowCharacterExamine(Character)`** e **`PlayerInfoWindow.ShowPlayerInfoWindow(Character)`** | Tem o **`Character`** → dá para resolver `effects[].Amount` com `Game.Eval` e anexar valor por passiva | Reescreve o `Text`/`specialText` (mais invasivo); só cobre os dois painéis |

---

## 7. Tabela completa das 90 passivas (com valor/alvo + fonte)

Legenda: **Valor** = o que existe; **Fonte** = prova (l. = decompilado; @ = offset em `resources.assets`). "sem valor no código" = etiqueta pura; a mecânica vive nos atributos/skills do inimigo.

| # | Identificador | `[Description]` | Valor / alvo | Fonte |
|---:|---|---|---|---|
| 1 | AttacksOfOpportunity | Attacks of Opportunity | sem valor no código (etiqueta) | l.179536-179537 |
| 2 | PhysicalResistant | Physical Resistant | sem valor no código | l.179538-179539 |
| 3 | FireResistant | Fire Resistant | sem valor no código | l.179540-179541 |
| 4 | ColdResistant | Cold Resistant | sem valor no código | l.179542-179543 |
| 5 | LightningResistant | Lightning Resistant | sem valor no código | l.179544-179545 |
| 6 | ElementalResistant | Elemental Resistant | sem valor no código | l.179546-179547 |
| 7 | WeakToPhysical | Weak to Physical | sem valor no código | l.179548-179549 |
| 8 | WeakToFire | Weak to Fire | sem valor no código | l.179550-179551 |
| 9 | WeakToCold | Weak to Cold | sem valor no código | l.179552-179553 |
| 10 | WeakToLightning | Weak to Lightning | sem valor no código | l.179554-179555 |
| 11 | WeakToElemental | Weak to Elemental Attacks | sem valor no código | l.179556-179557 |
| 12 | **Explosive** | Explodes on Death | asset EnemyMod "Explosive": "Explodes on death" (sem número — ação do gatilho) | l.179558-179559 · @1520121160 |
| 13 | HealsAllies | Heals Allies | sem valor no código | l.179560-179561 |
| 14 | Armored | Armored | sem valor no código | l.179562-179563 |
| 15 | **Berserking** | Berserking | "Maximum health increased by 25%" / "Deals more damage at lower health"; `Source.HealthRatioInverse * 100` | l.179564-179565 · @1520116904 |
| 16 | ManaShield | Mana Shield | **único valor lido pelo código** (esconde mana bar de boss) | l.179566-179567 · **l.156807** |
| 17 | Critical | High Critical Hit Chance | sem valor no código | l.179568-179569 |
| 18 | LifeSteal | Life Steal | sem valor no código (a mecânica é por-skill no jogo) | l.179570-179571 |
| 19 | **Regenerating** | Regenerating | "Regenerates health every turn." → `Source.GetFlatDamageValue * 5` | l.179572-179573 · @1520128628 |
| 20 | ReflectsDamage | Reflects Damage | sem valor no código (etiqueta; dano de retorno é atributo/status do inimigo) | l.179574-179575 |
| 21 | Summoner | Summons Allies | sem valor no código | l.179576-179577 |
| 22 | Ambusher | Deals Increased Damage to Isolated Targets | sem valor no código | l.179578-179579 |
| 23 | Stealth | Stealths | sem valor no código | l.179580-179581 |
| 24 | Indestructible | Indestructible | sem valor no código | l.179582-179583 |
| 25 | Glory | Glory | sem valor no código | l.179584-179585 |
| 26 | **Teleporting** | Teleporting | "Teleports randomly when struck" (sem número) | l.179586-179587 · @1520131416 |
| 27 | ControlResistance | Control Resistance | sem valor no código (aparece como rótulo dentro do mod Rampaging) | l.179588-179589 · @1520127527 |
| 28 | Summon | Summon | sem valor no código | l.179590-179591 |
| 29 | Abyssal | Abyssal | sem valor no código | l.179592-179593 |
| 30 | **Giant** | Giant | "Damage and Health increased by 25%" / "Size increased by 25%" (25/25) | l.179594-179595 · @1520123312 |
| 31 | **Miniature** | Miniature | "Movement +3 / AP +1 / Max Health −25% / Damage −25%" (−25/−25) | l.179596-179597 · @1520125192 |
| 32 | **Cursed** | Cursed | "Applies Curse on striking and when struck" (sem número) | l.179598-179599 · @1520119244 |
| 33 | **Destructive** | Destructive | "Damage increased by 50%" (50) | l.179600-179601 · @1520120132 |
| 34 | TakesDamage | Takes Increased Damage | sem valor no código | l.179602-179603 |
| 35 | **Elusive** | Elusive | "Dodge Chance increased by 25%" (25) | l.179604-179605 · @1520120912 |
| 36 | **Freezing** | Freezing | "Freezes all enemies on death" (sem número) | l.179606-179607 · @1520121636 |
| 37 | **Vampiric** | Vampiric | "Life Steal increased" (50) | l.179608-179609 · @1520133740 |
| 38 | **Necromantic** | Necromantic | "Summons a Skeletal Warrior on death" (sem número) | l.179610-179611 · @1520126928 |
| 39 | ExtraAction | Extra Action | sem valor no código | l.179612-179613 |
| 40 | ExtraMovement | Extra Movement | sem valor no código | l.179614-179615 |
| 41 | **Redemptive** | Redemptive | "Heals allies on death" — **sem número** (ação do gatilho; ver §5) | l.179616-179617 · @1520128064 |
| 42 | **Burning** | Burning | "Burning Aura" (aura/condição, sem número) | l.179618-179619 · @1520117220 |
| 43 | **Chilling** | Chilling | "Chilling Aura" (sem número) | l.179620-179621 · @1520118796 |
| 44 | **Shocking** | Shocking | "Shocking Aura" (sem número) | l.179622-179623 · @1520130508 |
| 45 | **Toxic** | Toxic | "Applies poison when striking / when struck" (sem número) | l.179624-179625 · @1520132012 |
| 46 | **Undying** | Undying | "Applies Dark Ritual on death" (sem número) | l.179626-179627 · @1520132748 |
| 47 | **Inspiring** | Inspiring | "Inspiring Aura" (sem número) | l.179628-179629 · @1520124504 |
| 48 | **FuriousFodderI** | Furious Fodder I | "25% increased Health and Damage" (25) | l.179630-179631 · @1520122192 |
| 49 | **FuriousFodderII** | Furious Fodder II | "50% increased Health and Damage" (50) | l.179632-179633 · @1520122564 |
| 50 | **FuriousFodderIII** | Furious Fodder III | "100% increased Health and Damage" (100) | l.179634-179635 · @1520122932 |
| 51 | **SavageSoldiersI** | Savage Soldiers I | "25% increased Health and Damage" (25) | l.179636-179637 · @1520129492 |
| 52 | **SavageSoldiersII** | Savage Soldiers II | "50% increased Health and Damage" (50) | l.179638-179639 · @1520129860 |
| 53 | **SavageSoldiersIII** | Savage Soldiers III | "100% increased Health and Damage" (100) | l.179640-179641 · @1520130228 |
| 54 | **CalamitousChampionsI** | Calamitous Champions I | 25% (25) | l.179642-179643 · @1520117760 |
| 55 | **CalamitousChampionsII** | Calamitous Champions II | 50% (50) | l.179644-179645 · @1520118136 |
| 56 | **CalamitousChampionsIII** | Calamitous Champions III | 100% (100) | l.179646-179647 · @1520118512 |
| 57 | **BeastlyBossesI** | Beastly Bosses I | 25% Health+Damage (25) | l.179648-179649 · @1520115768 |
| 58 | **BeastlyBossesII** | Beastly Bosses II | 50% (50) | l.179650-179651 · @1520116140 |
| 59 | **BeastlyBossesIII** | Beastly Bosses III | 100% (100) | l.179652-179653 · @1520116508 |
| 60 | **MonstrousMomentumI** | Monstrous Momentum I | "Movement Points increased by 1" | l.179654-179655 · @1520125496 |
| 61 | **MonstrousMomentumII** | Monstrous Momentum II | "Movement Points increased by 2" | l.179656-179657 · @1520125828 |
| 62 | **MonstrousMomentumIII** | Monstrous Momentum III | "Movement Points increased by 2" | l.179658-179659 · @1520126156 |
| 63 | **Rampaging** | Rampaging | "Increased damage by 50% / All resistances lowered by 25%" (50; −25×4) | l.179660-179661 · @1520127592 |
| 64 | **Resilient** | Resilient | "All Resistances increased by 25%" (25×5) | l.179662-179663 · @1520128980 |
| 65 | BleedImmunity | Bleed Immunity | sem valor no código | l.179664-179665 |
| 66 | PoisonImmunity | Poison Immunity | sem valor no código | l.179666-179667 |
| 67 | HeatImmunity | Heat Immunity | sem valor no código | l.179668-179669 |
| 68 | ShockImmunity | Shock Immunity | sem valor no código | l.179670-179671 |
| 69 | ChillImmunity | Chill Immunity | sem valor no código | l.179672-179673 |
| 70 | PackHunter | Pack Hunter | sem valor no código | l.179674-179675 |
| 71 | BleedsFire | Bleeds Fire | sem valor no código | l.179676-179677 |
| 72 | Hellfire | Hellfire | sem valor no código | l.179678-179679 |
| 73 | Rampage | Rampage | sem valor no código | l.179680-179681 |
| 74 | BuffsAllies | Buffs Allies | sem valor no código | l.179682-179683 |
| 75 | Cannibal | Cannibal | sem valor no código | l.179684-179685 |
| 76 | GlobalFire | Deals Global Fire Damage | sem valor no código | l.179686-179687 |
| 77 | Icefall | Icefall | sem valor no código | l.179688-179689 |
| 78 | Blind | Chance to Blind | sem valor no código | l.179690-179691 |
| 79 | ObsidianPlating | Obsidian Plating | sem valor no código | l.179692-179693 |
| 80 | SandstonePlating | Sandstone Plating | sem valor no código | l.179694-179695 |
| 81 | Explodes | Explodes | sem valor no código | l.179696-179697 |
| 82 | MoltenPlating | Molten Plating | sem valor no código | l.179698-179699 |
| 83 | **VampLord** | Vampire Lord | "Vampire Lord Aura" (sem número) | l.179700-179701 · @1520133224 |
| 84 | **StormCall** | Storm Caller | "Casts Storm Call" (sem número) | l.179702-179703 · @1520130960 |
| 85 | **Earthshatter** | Earthshatter | "Casts Earthshatter" (sem número) | l.179704-179705 · @1520120384 |
| 86 | **Necromancer** | Necromancer | "Summons Skeletons." (sem número) | l.179706-179707 · @1520126472 |
| 87 | **Vengeful** | Vengeful | "Gains increased damage for each ally killed" (sem número) | l.179708-179709 · @1520133988 |
| 88 | **IceTomb** | Ice Tomb | "Casts Ice Tomb" (sem número) | l.179710-179711 · @1520123604 |
| 89 | **Ignite** | Ignite | "Casts Ignite" (sem número) | l.179712-179713 · @1520124052 |
| 90 | Unpredictable | Unpredictable | sem valor no código | l.179714-179715 |

**Contagem:** 43 valores com asset `EnemyMod` próprio; 47 sem (etiqueta pura / mecânica em atributo ou skill do inimigo). Dentre os 43, os que trazem **número** na própria descrição/`amount`: Berserking, Regenerating, Giant, Miniature, Destructive, Elusive, Vampiric, Rampaging, Resilient, os 12 "tiers" (Furious Fodder I–III, Savage Soldiers I–III, Calamitous Champions I–III, Beastly Bosses I–III = 12) e Monstrous Momentum I–III. Os demais são comportamentais ("Casts X", "Summons X", auras, on-death).

---

## 8. Plano de implementação (para o `BetterTooltips`, mod BT-x)

> **Regra de ouro do projeto:** um mod, uma responsabilidade. Isto é **texto de tooltip** → `BetterTooltips`. Nada de balanceamento. Não tocar em assets.

### 8.1. Estratégia recomendada (em 2 ondas)

**Onda 1 — passivas com número fixo/conhecido (barata, cobre a maioria).**
- Arquivo novo: `BetterTooltips/Patches/PassivaInimigoPatch.cs`.
- **Postfix** em `OptionsManager.Localize` (mesmo padrão do `LocalizePatch`, `BetterTooltips/Patches/LocalizePatch.cs` l.19-20), com uma **tabela** `chave → sufixo` para as descrições de enemy-mod que **já contêm** o número (nada a fazer) e, principalmente, para **anexar contexto** onde falta.
- **Prefixo/Postfix em `Tooltip.ShowUniversalTooltip`** (assinatura explícita de 6 tipos: `string, string, string, Vector3?, ControlGlyphInfo?, string` — l.334459), casando `description` com as chaves de enemy-mod que interessam e anexando a nota. Vantagem: é exatamente o método que o link do `ExamineWindow` chama (l.105319), então cobre o caso da imagem sem tocar em `ExamineWindow`.

**Onda 2 — passivas comportamentais (`Redemptive`, `Explosive`, `Freezing`, `Teleporting`, "Casts X").**
- Para `Redemptive` o número **não existe** na data do mod: só sai resolvendo a ação do gatilho. Duas opções:
  - **(risco baixo, recomendado)** rodar **um** probe em jogo no Cave Golem (BT-18 já prevê "probe de runtime só se estritamente necessário") para medir a cura e então gravar uma **tabela estática** chave→texto no mod. É o mesmo padrão já usado pelo `ShrineAuraPatch` (valores de shrine fixados após verificação em jogo).
  - **(risco alto)** resolver em runtime: ler `character.EnemyMods` → `skillTriggers[]` → `Actions[]`/`GeneralEffects[]`/`ActionStatuses[]` e avaliar com `Game.Eval<float>(…)`. Mais fiel, porém mais frágil.

### 8.2. Onde exatamente plugar (assinaturas provadas)

| Alvo | Assinatura / patch | Fonte |
|---|---|---|
| `OptionsManager.Localize` | `[HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]` — postfix `(string original, ref string __result)` | `LocalizePatch.cs` l.19-20 · l.153419 |
| `Tooltip.ShowUniversalTooltip` | `(string title, string subtitle, string description, Vector3? targetPos, ControlGlyphInfo? controlGlyphInfo, string footerText)` | l.334459 |
| `ExamineWindow.ShowCharacterExamine(Character)` | postfix com `Character __0` para ler `EnemyMods`/`CalculatedSpecialEffects` | l.105180 |
| `PlayerInfoWindow.ShowPlayerInfoWindow(Character)` | postfix com `Character __0` | l.156801 |
| Leitura dos values | `Burst2Flame.Game.Instance.EnemyMods` (l.443067) · `Game.Eval<float>(effect.Amount, new GameFunctionParameters{ Source = character })` (l.443899 / l.37308) | — |

### 8.3. Cuidados (aprendidos nas cicatrizes do projeto)

- **Encoding:** as strings do `EnemyMod` em `resources.assets` são **UTF-8** (prefixo de comprimento). A armadilha do **UTF-16LE** vale para `ActionInfo`/ações Odin — ao buscar fórmulas de ações, repetir a busca com `utf-16-le`.
- **Não travar a UI:** a resolução de `Amount` deve ser preguiçosa e com `try/catch`; `Game.Eval` já engole exceção, mas cachear por `EnemyMod`+`character`.
- **Não duplicar:** se o número já está na descrição (Beastly Bosses etc.), **não** anexar de novo — anexar só onde a descrição não traz o valor.
- **Marcador de vida:** o `LocalizePatch` só loga quando muda algo; ao criar o patch novo, logar 1× na primeira chamada que passar dos early-returns (regra do projeto), senão "mod morto" é indistinguível de "nada casou".
- **Ancorar no `ExamineWindow` vs `Localize`:** para o valor que depende do **personagem** (ex.: passiva que escala), só o caminho C (pós-`ShowCharacterExamine`) tem o `Character` no escopo.

### 8.4. Teste/validação

- `bash scratch/test-cycle.sh 30 "<padrão de log do patch>"` (abre, coleta, fecha) e inspeção visual do painel EXAMINE no Cave Golem Lv3.
- Conferir `LogOutput.log` (é sobrescrito a cada boot — o antes/depois tem de ser na mesma sessão).
- Lembrar: build de verificação leva `-p:DeployToBepInEx=false`; instalar é ato explícito (`tools/release-check.sh --instalar-no-perfil`).

---

## 9. O que ficou em aberto (limites honestos)

1. **Número exato do `Redemptive`** não foi extraído estaticamente (ação em blob Odin; typetree não reconstrói). Os dois objetos referenciados pelo mod (`path_id` 2543785 "Mass Cure" e 2543782 "Holy Ground") são **candidatos**, não prova; confirmar em runtime.
2. **Onde estão as mecânicas dos 48 valores "sem valor no código"** (Armored, ReflectsDamage, LifeSteal, Summons Allies, etc.): não há asset `EnemyMod` com esse nome — a mecânica deve estar nos atributos/skills do `CharacterInfo` de cada inimigo. Não foi rastreada caso a caso (fora do escopo de "tooltip de passiva").
3. **`ControlResistance`**: aparece como rótulo dentro do bloco do `Rampaging` (@1520127527); não foi possível determinar se é um `SpecialEffectCondition`/rótulo auxiliar sem um probe em jogo.
4. **`SpecialEffectConditions`**: o dado (a lista de `SpecialEffect`+`Condition`) tem seu asset em outro lugar (não localizado); a lógica está provada em l.32690-32727, mas a **origem dos dados** não.

---

## Anexo — Comandos/probes criados (somente leitura)

```
scratch/bt18/probe.py        # strings no resources.assets (UTF-8)
scratch/bt18/probe2.py       # ocorrências de chaves vs. asset
scratch/bt18/probe3.py       # GUID do enemy mod
scratch/bt18/probe4.py       # contexto de uma string, marca o que é chave de localização
scratch/bt18/strings.py A B  # todas as strings imprimíveis numa faixa de offsets
scratch/bt18/hexdump.py A B  # hexdump + varredura de floats
scratch/bt18/keys.py <termo> # chaves do dicionário de localização (6.644 distintas)
scratch/bt18/find_mods.py    # busca nomes de passiva/asset
scratch/bt18/find_expr.py    # busca expressões (HasSpecialEffect etc.)
scratch/bt18/up_types.py     # (UnityPy) contagem de tipos de objeto em resources.assets
scratch/bt18/up_find.py      # (UnityPy) localiza o objeto por offset (Redemptive → path_id 2545350)
scratch/bt18/up_ref.py       # (UnityPy) strings de objetos referenciados por path_id
scratch/bt18/obj_dump.py     # (UnityPy) dump de um objeto
```

---

## 10. Achado adicional — verificação independente (leitura crua, sem UnityPy)

> Acrescentado numa **segunda passada** independente (mesmo decompilado/DLL, `resources.assets`
> lido por `mmap` + bytes crus, sem UnityPy). Confirma os pontos acima e **acrescenta** três coisas:
> (i) as **condições/expressões exatas** de cada `EnemyMod`; (ii) a **tabela de localização
> `enemyMod-description-<GUID>`** — que traz **números que a descrição do asset não tem** — e a
> divergência entre as duas; (iii) a prova aritmética do índice do enum no array `specialEffects`.

### 10.1. Correção de nuance no §5 (de onde sai o corpo "Heals allies on death")

O campo `description` do asset do `Redemptive` é a **string inglesa literal**
`"Heals allies on death"` (não a chave GUID). Prova byte a byte em `resources.assets`
(@15.201.280.60): `15 00 00 00 48 65 61 6c 73 20 61 6c 6c 69 65 73 20 6f 6e 20 64 65 61 74 68 00`
= prefixo de tamanho `0x15`=21 + `"Heals allies on death"`. O que acontece é que **o proprio
texto tambem existe como chave** na tabela de localizacao (`"Key":"Heals allies on death"`, 13
copias). O `ShowUniversalTooltip` (l.105319) faz `Localize(enemyMod.description)`, que devolve o
texto (traduzido). Alem disso existe a chave `enemyMod-description-<GUID>` (mesmo texto em ingles,
outros idiomas traduzidos) — mas **nenhum caminho do `Assembly-CSharp` constroi essa chave**
(grep por `"enemyMod-"` no decompilado: 0 ocorrencias); ela provavelmente serve a ferramenta de
build/bestiario. Ou seja: o texto exibido vem do **campo `description` do asset**, nao da chave GUID.

### 10.2. Condições / expressões exatas por `EnemyMod` (a prova de "onde mora o valor")

Strings extraídas do grupo de assets (@15.201.156.00–15.201.344.08). O texto entre crases é um
`SkillTrigger.Condition` (expressão avaliada por `Game.Eval<bool>`) ou o `Amount` de um efeito
(expressão avaliada por `Game.Eval<float>`).

| EnemyMod | Condição / expressão (o número) | @offset |
|---|---|---|
| Berserking | `Source.HealthRatioInverse * 100` | 15.201.169.04 |
| Burning | `Cell.IsCurrentHex(Source)` | 15.201.173.48 |
| Chilling | `Cell.IsCurrentHex(Source)` | 15.201.189.28 |
| Cursed | `ActionProperties.IsHarmful && Target.HasNoStatus("SHD_Status_Curse")` + `Cell.IsCurrentHex(Target)` (×2) | 15.201.193.20 |
| Earthshatter | `Cell.IsCurrentHex(Source)` | 15.201.205.20 |
| Explosive | `Cell.IsCurrentHex(Source)` | 15.201.213.08 |
| Freezing | `Cell.IsCurrentHex(Source)` | 15.201.217.80 |
| Ice Tomb | `Cell.IsCurrentHex(Source)` | 15.201.237.36 |
| Ignite | `Cell.IsCurrentHex(Source)` | 15.201.241.80 |
| Inspiring | `Cell.IsCurrentHex(Source)` | 15.201.246.36 |
| Necromancer | `Cell.IsCurrentHex(Source)` | 15.201.266.08 |
| Necromantic | `Source == Target` + `Source.IsDeathCell(Cell)` | 15.201.270.40 |
| **Redemptive** | `Cell.IsCurrentHex(Source)` (sem `Amount`) | 15.201.282.16 |
| **Regenerating** | `Source.GetFlatDamageValue * 5` | 15.201.286.28 |
| Shocking | `Cell.IsCurrentHex(Source)` | 15.201.306.40 |
| Storm Caller | `Cell.IsCurrentHex(Source)` | 15.201.310.92 |
| Teleporting | `!Source.IsRooted && !Source.IsStunned` + `Source.RandomEnemy != null && Cell == Source.RandomEmptyCellByCharacterWithinRange(Source.RandomEnemy, 3)` | 15.201.314.80 / 15.201.316.04 |
| Toxic | `Source.IsEnemy(Target)`, `Cell.IsCurrentHex(Target)` (×2) | 15.201.321.00 … 15.201.324.20 |
| Undying | `Cell.IsCurrentHex(Source)` | 15.201.328.92 |
| Vampire Lord | `Cell.IsCurrentHex(Source)` | 15.201.333.60 |
| Vengeful | `Target.IsAlly(Source)` + `Cell.IsCurrentHex(Source)` | 15.201.340.64 / 15.201.341.72 |

### 10.3. Prova do índice no array `specialEffects` (Redemptive = 40)

No registro do `Redemptive`, logo após a lista de efeitos, há `28 00 00 00` (@15.201.283.28) = **40**
= índice de `SpecialEffect.Redemptive` no enum (contado a partir de `AttacksOfOpportunity=0`;
`scratch/sac1/SpecialEffect.cs`). Isto confirma que `EnemyMod.specialEffects` guarda **índices do
enum** — o array é o elo entre o asset e o rótulo do tooltip, e não carrega número nenhum.

### 10.4. Tabela de localização `enemyMod-description-<GUID>` — números que o asset não mostra

39 chaves `enemyMod-name-<GUID>` / `enemyMod-description-<GUID>` no dicionário de localização
(`resources.assets`, ~@1.139.100.000; 13 cópias = 13 idiomas). **Vários valores com número que a
descrição do asset não traz.** Exemplos (nome :: descrição localizada):

```
Berserking      :: Maximum health increased by 25%\nDeals more damage at lower health
Destructive     :: Damage increased by 100%\nHealth reduced by 35%
Elusive         :: Dodge Chance increased by 35%\nHealth reduced by 20%
Giant           :: Damage and Health increased by 25%\nSize increased by 25%
Miniature       :: Movement increased by 3\nAction Points increased by 1\nMax Health reduced by 20%
Rampaging       :: Increased damage by 50%\nMovement Points increased by 3\nAlways Enraged\nAll resistances lowered by 25%
Regenerating    :: Regenerates 20% of Max Health per turn\nMax Health reduced by 30%.
Resilient       :: All Resistances increased by 25%
Redemptive      :: Heals allies on death            <- SEM número (o caso do dono)
Necromantic     :: Summons a Skeletal Warrior on death
Explosive       :: Explodes on death
Freezing        :: Freezes all enemies on death
Undying         :: Applies Dark Ritual on death
Toxic           :: Applies poison when striking\nApplies poison when struck
Teleporting     :: Teleports randomly when struck
Vengeful        :: Gains increased damage for each ally killed
```

**Divergência entre asset e localização por GUID** (mesmo GUID, textos diferentes):

| Mod | `description` no asset (@offset) | `enemyMod-description-<GUID>` |
|---|---|---|
| Elusive | `Dodge Chance increased by 25%` (@15.201.208.36) | `Dodge Chance increased by 35%\nHealth reduced by 20%` |
| Destructive | `Damage increased by 50%` (@15.201.200.64) | `Damage increased by 100%\nHealth reduced by 35%` |
| Miniature | `... Max Health reduced by 25% / Damage reduced by 25%` | `... Max Health reduced by 20%` |
| Regenerating | `Regenerates health every turn.` (@15.201.285.52) | `Regenerates 20% of Max Health per turn\nMax Health reduced by 30%.` |

O código atual (DLL idêntica à do jogo) chama `Localize(enemyMod.description)` → usa o **asset**.
As chaves por GUID são mais ricas, mas **nenhum caminho do `Assembly-CSharp` as constrói** (§10.1).
Fica como **ponto a confirmar em jogo**: qual das duas o jogador vê.

### 10.5. Implicação para o plano (§8)

- Para as passivas cujo **asset** já traz número (tiers 25/50/100, Elusive 25, Destructive 50,
  Resilient 25, Vampiric, Giant, Miniature, Monstrous Momentum, Rampaging, Berserking) **nada a
  fazer**: o texto exibido já tem o número.
- Para as **comportamentais sem número** (`Redemptive`, `Explosive`, `Freezing`, `Teleporting`,
  `Casts X`, auras, `Vengeful`), o número **não está em texto nenhum** — só resolvendo a ação do
  gatilho em runtime (Onda 2 do §8).
- A chave `enemyMod-description-<GUID>` (§10.4) é uma **fonte extra** de número para alguns casos,
  mas como o código aparentemente não a usa, **não** vale como base de implementação sem confirmação
  em tela.

**Método (reprodutível, somente leitura):** leitura de `resources.assets` com `mmap` + busca de
bytes (strings, GUIDs em ordem `Guid.ToByteArray()`, prefixos de tamanho); nenhuma execução do
jogo, nenhum build, nenhum commit/push.
