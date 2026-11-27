# FollowUpMod

Raises the character you pick for a co-op Roguelike party up to the level of the first character already accepted in that party — the same number the game itself compares — with the game's own level rewards. A level-1 character joining a group whose first accepted member is level 18 enters at level 18 — skills, items and attributes included. Characters **above** that reference level are never touched.

- **GUID:** `com.gumatos.followupmod`
- **Version:** 0.1.0
- **Works with:** Stolen Realm 1.4.9 (Steam public, buildid 26878331), Roguelike co-op
- **Needs:** BepInEx 5 — r2modman installs it for you. Nothing else: no ModAPI, no BetterStats.
- **BepInEx display name:** `FollowUpMod`

---

## REQUIREMENTS — READ THIS BEFORE PLAYING

**1. THE MOD MUST BE INSTALLED ON THE PLAYER WHO BRINGS THE UNDER-LEVELED CHARACTER.** That client is the one that raises the level before the game compares the party. No mod on that machine = nothing changes on that machine.

**2. THE HOST DOES NOT NEED THE MOD, BUT SHOULD HAVE IT.** The host publishes the group minimum into the Steam lobby (`followup.level`). That entry is a *marker and a diagnostic number*: its presence tells a modded client that the host is modded too. The promotion itself is always computed locally, from the party the server has already synced (the first accepted member's level), so a host without the mod does not stop a modded client from adjusting — the log calls that path *client mode* — and the game still decides whether to accept the character.

**3. EVERY PLAYER WHO HAS THE MOD MUST USE THE SAME VERSION.** Nothing checks the version: two different builds answer the same lobby key and may pick different targets, and no line in the log warns about it.

**4. ROGUELIKE CO-OP ONLY.** The gate tests exactly two things: the session reports multiplayer and the run is Roguelike. Campaign and singleplayer keep the original rules. It does **not** look at the Hardcore flag, so a hardcore character picked in a Roguelike co-op party would be adjusted like any other — that case was never exercised in game.

**5. THE MOD NEVER LOWERS A CHARACTER.** A character at or above the reference level is left exactly as it is; whether it is accepted stays the game's own rule, with its original level tolerance (±2 levels in 1.4.9, `RoguelikeSettings.MaxLevelVariance`).

**6. THE PROMOTED LEVEL IS NOT SAVED.** While a character is promoted its save is not written at all: the promoted level, the skills/items of that group and the rest of that session's progress for that character (loot, gold, XP) all stay in memory and are gone when the session ends. When the session ends the character is back to its original level. Other characters in the party keep saving normally.

---

## What it does

- **Level up before the check.** The adjustment happens in the prefix of `CharacterChoiceManager.ToggleSelectedCharacter`, before the game compares levels, so the original rule decides acceptance with the corrected level.
- **Native rewards.** Each level granted opens the game's own level-up flow (skill, item and attribute choices) — nothing is invented or skipped.
- **Auto-revert when the character leaves.** If the character does not stay in the party, its level is restored immediately and its pending level-up entries are removed from the game's queue, so it does not owe attribute/skill/item choices for a promotion that never applied.
- **Ceiling aware.** The promotion never goes past `Character.MaxLevel`, the game's global level cap (30 in 1.4.9). That is **not** the Roguelike cap of 20 (`RoguelikeSettings.RoguelikeMaxLevel`, which limits the rewards inside a run): a vanilla party tops out at 20, so the ceiling never binds there and the log only marks `ceiling_limited` when another mod raises the global cap.

### Level-up order

The native flow repeats *skills → items → attributes* for every level in the queue. With 17 levels that meant 17 cycles. FollowUpMod resolves the queue by **stage** instead:

1. all skill choices for every granted level,
2. all item choices,
3. a single attributes block,
4. done.

Rerolls keep the native single-stage path, and if the character has no unspent stat points the attributes block is skipped. Because the attribute points of every granted level accumulate in the character, one block spends exactly what the native loop would have asked for one level at a time.

The stage order itself is written at `RoguelikeManager.Start` (`Skills > Items > Attributes`, keeping a `Currency` stage if a future build has one). In 1.4.9 the prefab already ships that order, so the write is a guard, not a change — the log shows `ordem de subida: Skills>Items>Attributes -> Skills>Items>Attributes`.

## Install

r2modman → **Online** → **Install from file** → pick the zip. Manual install also works: copy `plugins/FollowUpMod/` into `BepInEx/plugins/`.

## Verify it is working

`BepInEx/LogOutput.log` (lines from the recorded 1.4.9 session):

```
FollowUpMod 0.1.0 ativo: 8/8 patches; metodos patcheados=8 [...]
FU: gate nivel=1 ancora=18 minimo=18 promove=True delta=17
FU: promovido nivel 1->18 (Level=18) niveis=17
```

`FU: inerte (not_multiplayer)` / `FU: inerte (not_roguelike)` mean the gate refused to act and the game is running vanilla.

`BepInEx/FollowUpMod.diag.log` keeps a per-event trace: `prefix entrou`, `contexto mp=... rog=... regra=...`, `snapshot ancora=...`, `clique tile=...` and `nivel: confirmar fase=...`.

## Not verified in game yet

The 0.1.0 session that was played ran in **client mode** (`contexto ... regra=False`, `host sem regra: modo cliente`) with a level-1 character promoted to 18, every reward granted in stage order and the level restored when the character left. These paths are written but were **not observed** in a real session:

- the host announcing the rule (`FU: lobby anunciado min=... ok=...`) — the recorded log has no announce line at all, so that branch never ran;
- two machines, both modded, agreeing on the same reference level at the same time;
- `ceiling_limited`: with the vanilla global cap at 30 and a Roguelike party capped at 20, that branch cannot be reached without another mod;
- a hardcore character (see REQUIREMENTS 4 — the gate has no Hardcore check);
- the game *refusing* a character above the reference level: the recorded session never produced that refusal (no `Cannot Add To Party` line), so it is still the native rule read from the code (`MaxLevelVariance = 2`), not something seen on screen.

## Build

From the repository root, with the game installed and `lib/` present:

```bash
dotnet build FollowUpMod/FollowUpMod.csproj -c Release -p:DeployToBepInEx=false
```

---

## Português (BR)

Sobe o personagem escolhido para a party de co-op Roguelike até o nível do **primeiro personagem já aceito** no grupo — o mesmo número que o jogo compara — usando as recompensas nativas do jogo. Um personagem nível 1 entrando num grupo cujo primeiro aceito é nível 18 entra como 18, com skills, itens e atributos. Personagem **acima** desse nível de referência nunca é alterado.

### REQUISITOS — LEIA ANTES DE JOGAR

**1. O MOD PRECISA ESTAR INSTALADO EM QUEM TRAZ O PERSONAGEM DE NÍVEL BAIXO.** É o cliente dessa pessoa que ajusta o nível antes da comparação do jogo. Sem o mod nessa máquina, nada muda.

**2. O DONO DA SALA NÃO PRECISA, MAS DEVE TER.** O host publica o mínimo do grupo no lobby da Steam (`followup.level`). Essa entrada é **marcador e número de diagnóstico**: a presença dela diz a um cliente com o mod que o host também tem. A promoção em si é sempre calculada localmente, a partir da party que o servidor já sincronizou (o nível do primeiro aceito) — então host sem o mod **não** impede o cliente com mod de ajustar (o log chama isso de *modo cliente*), e o jogo continua decidindo se aceita.

**3. TODOS QUE TIVEREM O MOD DEVEM USAR A MESMA VERSÃO.** Nada confere a versão: duas builds diferentes respondem pela mesma chave do lobby e podem escolher alvos diferentes, sem nenhuma linha de log avisando.

**4. SOMENTE CO-OP ROGUELIKE.** O portão testa exatamente duas coisas: a sessão reporta multiplayer e a run é Roguelike. Campanha e singleplayer ficam com as regras originais. Ele **não** olha a flag Hardcore, então um personagem hardcore escolhido numa party de co-op Roguelike seria ajustado como qualquer outro — esse caso nunca foi exercitado em jogo.

**5. O MOD NUNCA REBAIXA PERSONAGEM.** No nível de referência ou acima, permanece como está; a aceitação continua sendo a regra do jogo, com a tolerância original (±2 níveis na 1.4.9, `RoguelikeSettings.MaxLevelVariance`).

**6. O NÍVEL PROMOVIDO NÃO É GRAVADO.** Enquanto promovido, o save daquele personagem **não é escrito**: o nível promovido, as skills/itens daquele grupo e o resto do progresso da sessão daquele personagem (loot, ouro, XP) ficam só na memória e somem quando a sessão termina. Ao fim da sessão ele volta ao nível de antes. Os demais personagens da party continuam salvando normalmente.

Se o personagem não ficar na party, o nível é devolvido na hora e as escolhas de nível pendentes dele são removidas da fila do jogo.

### Ainda não verificado em jogo

A sessão da 0.1.0 rodou em **modo cliente** (`contexto ... regra=False`, `host sem regra: modo cliente`), com um personagem nível 1 promovido a 18, todas as recompensas na ordem por etapa e o nível devolvido quando ele saiu. Estes caminhos existem no código mas **não foram observados** numa sessão real:

- o host anunciando a regra (`FU: lobby anunciado min=... ok=...`) — o log gravado não tem nenhuma linha de anúncio, ou seja esse ramo nunca rodou;
- duas máquinas, as duas com o mod, concordando no mesmo nível de referência ao mesmo tempo;
- `ceiling_limited`: com o teto global vanilla em 30 e a party Roguelike limitada a 20, esse ramo não é alcançável sem outro mod;
- personagem hardcore (ver REQUISITO 4 — o portão não confere Hardcore);
- o jogo **recusando** um personagem acima do nível de referência: a sessão gravada nunca produziu essa recusa (nenhuma linha `Cannot Add To Party`), então isso continua sendo a regra nativa lida no código (`MaxLevelVariance = 2`), não algo visto na tela.

---

**Source, issues and forks:** <https://github.com/DefRuivo/stolenRealmMods> — contributions are welcome.
**Código-fonte, issues e forks:** <https://github.com/DefRuivo/stolenRealmMods> — contribuições são bem-vindas.
