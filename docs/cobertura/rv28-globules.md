# RV-28 (passo 1) — a família dos globules: lista FECHADA e PROVADA

> **Para que serve este arquivo.** O `RV-28` (cura dinâmica do `Sustenance I/II` no tooltip do
> globule) começou pelo censo de status, onde existe **um só** registro de globule: `Power Globule`
> (`docs/cobertura/status.csv:370`). O pedido do dono fala de **TODOS** os globules, então a família
> tinha de ser fechada **antes** de escrever texto — e com prova citável, nunca com nome inventado.
> Esta é a lista-insumo da implementação (`t_a0544760`) e do seu aceite.

Data da medição: **06/10/2026**. Build do jogo conferido contra os bytes do disco (hashes em §9).

---

## 1. Veredito em uma frase

A família de **globules do jogo tem exatamente SEIS membros** — `Cleansing`, `Energy`, `Health`,
`Mana`, `Power` e `Refreshing Globule` — todos `GroundEffectInfo` de `GroundEffectType.Pickup`; e a
regra de cura do `RV-28` vale para **todos os seis** (o `Power Globule` **inclusive**, apesar de ele
ser buff de dano: a cura dispara ao **consumir** o globule, qualquer que seja o efeito dele).

Além deles, o **mesmo gatilho** alcança **seis pickups de poção** (`Minor`/`Healing`/`Major Healing
Potion` e `Minor`/`Mana`/`Major Mana Potion`), que o `RV-32` já instrumenta — eles **não** são
"globules" pelo nome, e por isso vêm em tabela separada (§3).

---

## 2. Como a lista foi fechada (o argumento de fechamento)

Não é "procurei e achei estes": é uma **enumeração exaustiva** da palavra no jogo.

1. **A varredura.** `grep -abo "Globule"` em `resources.assets` (1.723.507.220 bytes) devolve **324
   ocorrências**, que reduzem a **26 strings distintas** (§2.1). Nenhuma outra entidade do jogo tem
   "Globule" no nome.
2. **A palavra só existe ali.** A mesma varredura em **todo o resto dos dados do jogo** — `*.assets`,
   `globalgamemanagers*`, `level0/1/2`, todos os `*.resS`, os `*.resource` e `StreamingAssets` — dá
   **zero**. Em `Managed/Assembly-CSharp.dll` há **duas** ocorrências, ambas **símbolos de código**
   (`OnGlobulePickup` e `IncrementGlobulePickupCountAchievementStat`) — nenhum texto de tela.
3. **O cluster dos `GroundEffectInfo`.** Os seis aparecem, um por um, no mesmo cluster de
   `resources.assets` (@1520817976–@1520829572), **cada um duas vezes** (o `m_Name` do asset e o campo
   `Name` do `GroundEffectInfo`) e **seguido da descrição** que o tooltip mostra — a mesma estrutura
   que os pickups de poção logo ao lado, o que ancora a leitura (`Pickup Health 10` → `Name` "Minor
   Healing Potion" → `Description` "Restores 10% health", @1520825016/@1520825328/@1520825352).
4. **O gatilho confirma o tipo.** `GroundEffectType` é um enum de **três** valores —
   `Pickup`, `Shrine`, `Destructable` (`GroundEffectType`, ilspycmd) — e é `Pickup` que dispara o
   gatilho do `Sustenance` (§5). Os seis globules estão nesse cluster de pickups, ao lado das poções
   de pickup; os crates/shrines do mesmo cluster **não** contêm a palavra.

### 2.1 As 26 strings distintas (a lista crua, para auditoria)

A soma da coluna "ocorrências" dá **324** — bate com o `wc -l` da varredura, então nada ficou de fora.

| Ocorrências | String | Papel |
|---:|---|---|
| 80 | `Consuming any Globule heals you for ` | prefixo (EN) da descrição do `Sustenance` I/II |
| 35 | `Power Globule` | **nome de exibição** |
| 32 | `Refreshing Globule` | **nome de exibição** |
| 32 | `Mana Globule` | **nome de exibição** |
| 32 | `Health Globule` | **nome de exibição** |
| 32 | `Energy Globule` | **nome de exibição** |
| 32 | `Cleansing Globule` | **nome de exibição** |
| 27 | `Produce a random Globule on the target hex.` | descrição da skill `Magic Hat III` |
| 3 | `importe quel Globule vous soigne de ` | tradução **FR** do prefixo do `Sustenance` |
| 3 | `Consumir qualquer Globule cura voc…` | tradução **PT** do prefixo do `Sustenance` |
| 1 | `Produisez un Globule al…` | tradução **FR** da descrição do `Magic Hat III` |
| 1 | `Power Globule Status` | o **status** aplicado pelo globule (§4) |
| 1 | `Cleansing Globule Pickup` | nome de prefab/efeito |
| 1 | `Energy Globule Pickup` | nome de prefab/efeito |
| 1 | `Power Globule Pickup` | nome de prefab/efeito |
| 1 | `Refreshing Globule Pickup` | nome de prefab/efeito |
| 1 | `Cleansing Globule End` | nome de efeito de fim |
| 1 | `Energy Globule End` | nome de efeito de fim |
| 1 | `Power Globule End` | nome de efeito de fim |
| 1 | `Refreshing Globule End` | nome de efeito de fim |
| 1 | `Globule purificateur` | tradução **PT** de `Cleansing Globule` |
| 1 | `Globule de Puissance` | tradução **FR** de `Power Globule` |
| 1 | `Globule Rafra…` | tradução **FR** de `Refreshing Globule` |
| 1 | `Globule de sant…` | tradução **PT** de `Health Globule` |
| 1 | `Globule de mana` | tradução **PT** de `Mana Globule` |
| 1 | `Globule d…` | tradução **FR** de `Energy Globule` |

Nenhuma linha desta tabela é um sétimo globule: são os **seis nomes**, os textos que os citam, os
nomes de prefab/efeito e as **traduções** (que não criam membro novo).

---

## 3. As duas tabelas

### 3.1 Os SEIS globules (a família do pedido)

Cada linha tem: nome **exato** como o jogo o exibe (não normalizado), a prova, o efeito real e a
decisão. Offsets em `resources.assets` deste build; os pares de offset são `Name` (campo do
`GroundEffectInfo`, é o **título** do tooltip) e `Description` (é o **corpo**).

| Nome exato | Prova (asset) | Efeito real | Entra na regra de cura? | Justificativa |
|---|---|---|---|---|
| `Cleansing Globule` | `Name` @1520818292 + `Description` "Cleanses all debuffs" @1520818316 (o nome ocorre também @1520817976) | limpa todos os debuffs | **SIM** | "Consuming any **Globule** heals you for …" não distingue efeito — o gatilho é o consumo (§5) |
| `Energy Globule` | `Name` @1520823512 + `Description` "Grants an additional Action Point" @1520823532 (nome também @1520823200) | +1 Action Point | **SIM** | idem |
| `Health Globule` | `Name` @1520824128 + `Description` "Heals for 50% of Max Health" @1520824148 (nome também @1520823816) | cura 50% da vida máxima | **SIM** | idem (é o caso que o dono descreveu) |
| `Mana Globule` | `Name` @1520824732 + `Description` "Restores 50% of Max Mana" @1520824748 (nome também @1520824424) | restaura 50% da mana máxima | **SIM** | idem |
| `Power Globule` | `Name` @1520828936 + `Description` "Increases all damage by 10%" @1520828956 (nome também @1520828624); status em §4 | buff: +10% de dano (e de dano de invocação) | **SIM** — decisão em §4 | **não é cura**, mas a cura do `Sustenance` dispara ao **consumir qualquer** globule; excluí-lo seria mentir no tooltip dele |
| `Refreshing Globule` | `Name` @1520829548 + `Description` "Lowers Cooldowns by 1" @1520829572 (nome também @1520829232) | -1 de cooldown | **SIM** | idem |

**Divergência declarada vs. o texto do card:** o card do `RV-28` supunha que o `Power Globule`
"provavelmente **não**" entraria. A leitura do asset do `Sustenance` + o gatilho mostram o
contrário; a decisão está escrita e justificada em §4.

### 3.2 Os SEIS pickups de poção (mesmo gatilho — regra do `RV-32`)

Não são "globules" pelo nome; entram na **mesma regra de cura** porque são `GroundEffectType.Pickup`
e portanto disparam `OnGlobulePickup` (§5). A descrição de cada um é **exclusiva do pickup** — o
**item** de mesmo nome diz outra coisa (ex.: `Minor Healing Potion` item = "Restores 75 health.").

| Nome exato (título do tooltip) | Prova (asset) | Efeito real | Entra na regra de cura? | Justificativa |
|---|---|---|---|---|
| `Minor Healing Potion` | `Pickup Health 10` @1520825016 → `Name` @1520825328 + `Description` "Restores 10% health" @1520825352 | cura 10% da vida | **SIM** (`RV-32`) | mesmo gatilho; frase própria ("Picking this up also heals you for …") |
| `Healing Potion` | `Pickup Health 15` @1520825616 → `Name` @1520825928 + `Description` "Restores 15% health" @1520825948 | cura 15% da vida | **SIM** (`RV-32`) | idem |
| `Major Healing Potion` | `Pickup Health 20x 1` @1520826216 → `Name` @1520826532 + `Description` "Restores 20% health" @1520826556 | cura 20% da vida | **SIM** (`RV-32`) | idem |
| `Minor Mana Potion` | `Pickup Mana 10` @1520826824 → `Name` @1520827136 + `Description` "Restores 10% mana" @1520827160 | restaura 10% da mana | **SIM** (`RV-32`) | idem |
| `Mana Potion` | `Pickup Mana 15` @1520827424 → `Name` @1520827736 + `Description` "Restores 15% mana" @1520827752 | restaura 15% da mana | **SIM** (`RV-32`) | idem |
| `Major Mana Potion` | `Pickup Mana 20x 1` @1520828016 → `Name` @1520828332 + `Description` "Restores 20% mana" @1520828356 | restaura 20% da mana | **SIM** (`RV-32`) | idem |

Os seis textos de descrição aparecem **uma única vez** cada em todo o `resources.assets` — nenhuma
outra entidade os usa (é por isso que a nota entra pela **descrição** e o item não é tocado).

---

## 4. Decisão explícita: o `Power Globule` ENTRA (e é buff, não cura)

**O que ele é.** `Name` `Power Globule` (@1520828936, descrição do ground effect: "Increases all
damage by 10%"). Ele **aplica um status**, cujo asset é `Power Globule Status` (@1517346632), com
`Name` "Power Globule" (@1517346856) e `Description` "Increases damage and summon damage by 10%"
(@1517346876) — que é exatamente a linha do censo (`docs/cobertura/status.csv:370`) e o texto que o
`RV-9` já enriqueceu (`BetterTooltips/Patches/LocalizePatch.cs:1564`). **Não cura nada.**

**Por que entra mesmo assim.** O que cura é o `Sustenance`, e o texto dele no asset da própria skill
é literal: *"Consuming any Globule heals you for 8% of max life and mana."* (`Sustenance I`,
`resources.assets` @1633612592) e *"…for 20%…"* (`Sustenance II`, @1633615572). O sujeito é **qualquer
globule**, não "globules de cura". Deixar o `Power Globule` de fora seria uma **lacuna visível**: o
jogador com `Sustenance` ativa consome um `Power Globule`, recebe cura real, e o tooltip do globule
é o único que não explica de onde veio a cura — justamente o defeito que o `RV-28` existe para
fechar.

**Ressalva honesta (registrada, não escondida).** O corpo do tooltip do ground effect é
`ActionStatuses[0].Description` **quando existe**, senão `GroundEffectInfo.Description`
(`Tooltip.ShowGroundEffectTooltip`, ilspycmd) — e **qual dos dois** o `Power Globule` usa **não é
legível por varredura de bytes** (é uma lista de `PPtr`, não texto). Por isso a implementação
registra a chave nas **duas** descrições dele (`GlobulePatch.cs:75` e `GlobulePatch.cs:76`), o que é
correto em qualquer um dos casos.

O ecossistema do status já reconhece a ligação com cura no sentido inverso: a nota do `RV-9` no
status diz *"Also increases the healing this character does by the same percentage."*
(`BetterTooltips/Patches/LocalizePatch.cs:1566`). As duas leituras se completam, não se contradizem.

---

## 5. O gatilho `TriggerType.OnGlobulePickup` cobre a lista inteira?

**Cobre — por construção, e o jogo testa a fiação das duas tiers por conta própria.**

1. **Quem dispara.** `GroundEffect.ExecuteActionOnEnter`, no fim da entrada no hex:
   ```csharp
   if (GroundEffectInfo != null && GroundEffectInfo.GroundEffectType == GroundEffectType.Pickup)
   {
       player.ProcessSkillTriggers(null, default(ActionProperties), TriggerType.OnGlobulePickup);
       Root.IncrementGlobulePickupCountAchievementStat((byte)player.OwnerID);
   }
   ```
   (tipo `GroundEffect`, ilspycmd — o corpo acima é o trecho do `ExecuteActionOnEnter`.)
   O teste é o **tipo do ground effect**, não o nome: **todo** `Pickup` da lista (§3.1 e §3.2)
   dispara o gatilho; nenhum globule da lista é `Shrine` ou `Destructable`.
2. **Quem cura.** Os procs são `Sustenance I Proc` (`Target.MaxHealth * .08f`, `Target.MaxMana * -.08f`)
   e `Sustenance II Proc` (`.20f` / `-.20f`) — `docs/cobertura/acoes.csv:255` e
   `docs/cobertura/acoes.csv:256`. Ou seja: 8% e 20% da vida **e** da mana máxima, exatamente como a
   descrição do asset promete.
3. **O teste do próprio jogo (a prova de que a fiação existe).** No tipo `ChaosSkillTest` (ilspycmd):
   - `AssertTriggerWiring("CHAOS_1_P2_Sustenance I", TriggerType.OnGlobulePickup, "Sustenance I Proc")`
     — método `SustenanceI`;
   - `AssertTriggerWiring("CHAOS_2_P2_Sustenance II", TriggerType.OnGlobulePickup, "Sustenance II Proc")`
     — método `SustenanceII`.
   Os dois ids citados existem no asset: `CHAOS_1_P2_Sustenance I` @1633612464 e
   `CHAOS_2_P2_Sustenance II` @1633615440.
   **Limite do teste:** ele afirma o **gatilho**, não o **valor** — para `Sustenance` o jogo não tem
   teste de número (diferente do `Omnism`, que tem). Por isso a dúvida "8% ou 20% ou 28%" **não** se
   resolve aqui: a implementação lê a lista **ativa** (`Character.Skills`) e mostra o que o jogo
   tiver ligado, sem cravar tier nem somar (`GlobulePatch.cs:176`).
4. **A skill que *cria* globule usa a mesma família.** `Magic Hat III` — descrição "Produce a random
   Globule on the target hex." (@1101649793; o nome/título em @1101649628) — e o `Fabricate`
   ("When you consume a globule you have a 50% chance to spawn a random globule within a 6 hex area
   of you.", @1101651136, com `AssertTriggerWiring(..., TriggerType.OnGlobulePickup, ...)` no mesmo
   `ChaosSkillTest`). Nada aqui introduz um sétimo globule: é spawn/consumo da mesma lista.

---

## 6. O que o mod já faz com esta lista (estado em 06/10)

- A família está instrumentada em `BetterTooltips/Patches/GlobulePatch.cs:68` (as sete chaves das
  seis descrições — o `Power Globule` comparece com duas) e `GlobulePatch.cs:91` (as seis descrições
  dos pickups de poção).
- A nota entra pelo postfix do `OptionsManager.Localize`: `BetterTooltips/Patches/LocalizePatch.cs:2775`.
- A nota é **por personagem em foco** e com a % das tiers que o jogo tem ativas
  (`GlobulePatch.cs:109`, `GlobulePatch.cs:176`); sem skill ativa, sem número (texto do jogo intacto).
- Registro no changelog: `BetterTooltips/CHANGELOG.md:123`.
- Aceite do dono: comentado no card `t_2bd1a32c` em 06/10 — *"Globule, Decay estão corretos durante a
  run"*. Gate restante do `RV-28` é **publicação**, não texto.

---

## 7. Limites desta prova (o que eu **não** provei)

1. **Qual descrição o `Power Globule` mostra** (`GroundEffectInfo.Description` × `ActionStatuses[0].Description`):
   é lista de `PPtr`, ilegível por byte scan. Resolvido por **cobertura dupla** na implementação
   (§4), não por prova.
2. **O vínculo prefab↔globule para `Health`/`Mana`.** A tabela de nomes tem
   `Cleansing/Energy/Power/Refreshing Globule Pickup`, mas **não** existe `Health Globule Pickup` nem
   `Mana Globule Pickup`; há `Pickup Health` @1634622296 e `Pickup Mana` @1634622536 no mesmo
   índice de nomes. **Não afirmo** que sejam os prefabs desses dois globules — a lista **não depende
   disso** (a prova é `Name` + `Description` no cluster dos `GroundEffectInfo`, §2.3).
3. **A composição exata do array `BattleDrops`** (`BattleManager.BattleDrops`, o sorteio dos drops de
   batalha: `BattleManager.SpawnPickup`) e do pool equivalente (`GroundEffectInfo.BattleDropChance`)
   não é legível byte a byte. O que está provado é o **gatilho por tipo** (todo `Pickup` dispara),
   que é o que a regra de cura precisa.
4. **8% × 20% × 28%** continua **indeterminado** para o `Sustenance` (é o mesmo ponto aberto do
   `RV-24`). Esta lista não depende dele: a implementação lê as tiers **ativas**.
5. O `Power Globule` do censo (`docs/cobertura/status.csv:370`) está marcado **`corrigido`**, não
   `pendente` — o texto do card (`pendente/pendente`) está desatualizado nesse ponto.

---

## 8. Como reproduzir (comandos, não afirmações)

```bash
# 1) A varredura de fechamento (é ela que prova "só existem seis")
cd "E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data"
grep -abo "Globule" resources.assets | wc -l            # 324
grep -aboE "[A-Za-z ]{0,22}Globule[A-Za-z ]{0,30}" resources.assets | sort -t: -k2 -u

# 2) O cluster dos GroundEffectInfo (nome + descrição, com o offset de cada string)
python <repo>/scratch/rv28/region.py 1520817000 14000 4    # ver §9 para o script

# 3) Os tipos decompilados (o dump monolitico foi podado — regenerar por tipo)
"$HOME/.dotnet/tools/ilspycmd" -t GroundEffect    <repo>/lib/Assembly-CSharp.dll
"$HOME/.dotnet/tools/ilspycmd" -t GroundEffectInfo <repo>/lib/Assembly-CSharp.dll
"$HOME/.dotnet/tools/ilspycmd" -t Tooltip          <repo>/lib/Assembly-CSharp.dll   # ShowGroundEffectTooltip
"$HOME/.dotnet/tools/ilspycmd" -t ChaosSkillTest   <repo>/lib/Assembly-CSharp.dll   # SustenanceI / SustenanceII
"$HOME/.dotnet/tools/ilspycmd" -t BattleManager    <repo>/lib/Assembly-CSharp.dll   # BattleDrops / SpawnPickup
```

O `region.py` usado é um leitor de strings por offset (seek + 4 KB de contexto), sem UnityPy; ele
vive fora do repo versionado (`~/.hermes/cache/scratch/rv28/region.py`) porque é bancada.

---

## 9. Hashes do que foi medido (para o aceite ser reconferível)

| Arquivo | Tamanho | sha256 |
|---|---:|---|
| `Stolen Realm_Data/resources.assets` | 1.723.507.220 | `cbdfcd0fa8ecc338029024acfeb6f939593aa99a1f291ae65f4776fcb0dbc012` |
| `Stolen Realm_Data/Managed/Assembly-CSharp.dll` | 7.712.768 | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |

`StreamingAssets/build_info`: *"Build from JJS_DESKTOP at 09/10/2026 14:39:09"*.
Os offsets desta página foram **remedidos neste build** e batem, um a um, com os citados no
comentário de `BetterTooltips/Patches/GlobulePatch.cs:13-18` — nenhuma divergência a registrar.

**Citações de `arquivo:linha` deste documento** apontam para arquivos do repositório e são
verificadas por `python tools/checa_citacoes.py docs/cobertura/rv28-globules.md`. Referências ao
decompilado do jogo aparecem como **tipo + membro** (e não como `arquivo:linha`) porque o dump
monolítico foi podado do repositório — o comando de regeneração está em §8.
