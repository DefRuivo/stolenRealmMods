# RoguelikeUnlimitedLevelProgression

Lets a Roguelike run go past level 20 — **singleplayer only, v0.1**.

- **GUID:** `com.gumatos.roguelikeunlimitedlevelprogression`
- **Harmony owner id:** the same GUID (the mod unpatches by id, never by type).
- **Version:** 0.1.1
- **Works with:** Stolen Realm (Roguelike mode).
- **Needs:** BepInEx 5 (r2modman installs it for you) and nothing else — no ModAPI, no BetterStats.
- **BepInEx display name:** `Roguelike Unlimited Level Progression`

## What it does

In the Roguelike mode the game stops granting a level once
`character.Level < settings.RoguelikeMaxLevel` is false (`RoguelikeSettings.RoguelikeMaxLevel`
ships as **20** in the game's asset). This mod replaces that single comparison and keeps the
rest of the flow — the XP curve, the level-up queue, the UI — coherent above 20.

- **One level per victory.** Above 20 the reward stage is still one entry per victory: the
  comparison that decides whether the character levels becomes
  `Policy.CanAdvance(Character, RoguelikeSettings)`.
- **Loading a saved character never loses levels.** `Character.Load(int)` clamps the saved level
  with `Mathf.Min(Character.MaxLevel, CharacterSaveFile.ExperienceLevel)`, and `Character.MaxLevel`
  is exactly the getter this mod patches — before that assignment the character's own level is
  still ~1, so it cannot protect the save. While a character is loading (`IsLoaded == false`) the
  patched getter is therefore floored by the saved `CharacterSaveFile.ExperienceLevel`, on **every**
  path including the vanilla fallback (so a save above level 30 is never truncated to 30).
- **Extended XP after 20 (linear, O(1)).** `F(20)`/`D(20)` are read from the game itself
  (`Character.GetExperienceFloorForLevel(20)` and `(21)`), and for `level > 20`
  `F(L) = F20 + D20 * (L - 20)`. Nothing is hardcoded: if those numbers are unusable
  (`NaN`, non-finite, `D20 <= 0`) the mod stays vanilla instead of guessing.
- **Skills, Items, Attributes stay eligible.** When the skill pool is exhausted the stage is
  skipped and a **durable receipt** (S) is written under
  `<BepInEx config>/com.gumatos.roguelikeunlimitedlevelprogression/receipts/<character-guid>.json`;
  S is subtracted from the level-up queue count so the skipped skill is not silently lost.
  If the receipt cannot be written, the stage is **not** skipped (no reward is consumed).
  Items/attributes keep coming after that. No fake skills are invented.
- **Item/skill reward queries stay at level 20** (`Rewards.RewardQueryLevel`) so loot quality
  does not extrapolate past the vanilla curve.
- **UI:** the level-up bar and the "Max" label are recalculated only for the extended scope,
  so they do not show a false maximum or `NaN`.

**Nothing else changes.** No new areas, no endless mode, no invented gold, no meta powerup
increase, no item/fortune cap removal, no Bard/music (its tree arrives with a later game
update), no forced achievements, no campaign changes.

## Configuration

| Key | Default | Meaning |
| --- | --- | --- |
| `General.Enabled` | `true` | Master switch. `false` reproduces the vanilla behaviour exactly. |
| `Progression.MaxLevel` | `0` | Voluntary ceiling. `0` = no gameplay ceiling. A value `>= 21` caps the extended levels; **lowering it never lowers a character that is already above it**. |
| `Rewards.RewardQueryLevel` | `20` | Level used for item/skill reward queries (1..30). |
| `Diagnostics.Verbose` | `false` | Extra logging. |

## Scope and fail-closed behaviour

- **Singleplayer only.** In `PlayingMultiplayer` the vanilla branch is kept and a warning is
  logged: extended saves/ledger are not supported yet.
- **Campaign and AI characters are outside the extended scope** and keep the exact vanilla
  comparison.
- The gameplay patch group is **all-or-nothing**: if any Harmony target is missing, if any
  patch throws or if the critical transpiler refuses the target, every patch of the mod is
  reverted (`Harmony.UnpatchID(guid)`), so the game never runs half-patched.
- The critical patch matches the IL **structurally** (member signatures + a unique window) and
  requires exactly one match; labels/exception blocks are preserved. No local index or IL
  offset is hardcoded.

## Build

```
dotnet build RoguelikeUnlimitedLevelProgression/RoguelikeUnlimitedLevelProgression.csproj -p:DeployToBepInEx=false
dotnet build tests/RoguelikeUnlimitedLevelProgression.Harness/RoguelikeUnlimitedLevelProgression.Harness.csproj -p:DeployToBepInEx=false
```

The game/BepInEx assemblies are **not versioned**: they are read from the private `lib/` folder at the
**root of the checkout** (`<checkout>/lib`, gitignored — see [`docs/ESTRUTURA.md`](../docs/ESTRUTURA.md)).
Both the mod and the harness resolve that folder **relative to the checkout they belong to**, so the
same source builds at any depth: no absolute path of the owner's machine, no dependency on where a
worktree happens to live. A canonical checkout (`C:/dev/stolen-realm`) therefore builds with no extra
argument.

There is **no silent fallback**: an isolated clone/worktree that does not have its own `lib/` fails
with a single clear error and needs the owner-authorized override —

```
dotnet build RoguelikeUnlimitedLevelProgression/RoguelikeUnlimitedLevelProgression.csproj -p:CommonLibDir=<absolute path of a lib folder>
```

```
LEVEL-LIB: lib de referencias nao encontrada em '<...>\lib'. Rode o build na raiz do checkout
canonico (lib/ e local, gitignored) ou passe o override autorizado: -p:CommonLibDir=<caminho>.
```

Never copy the game DLLs into the repository or into a worktree to satisfy a build.

Deploying into the r2modman profile is **opt-in**: `dotnet build -p:DeployToBepInEx=true`
copies the DLL to `.../profiles/Default/BepInEx/plugins/RoguelikeUnlimitedLevelProgression/`.

## Not exercised yet

The v0.1 code was built and exercised in an isolated harness (the mod's own sources compiled
into a test executable that feeds the **real transpiler** the **real IL** of
`Root.SendGameCompleteFromServer` read from the reference `Assembly-CSharp.dll`), plus the
policy/XP/ledger suites. It has **not** been run inside the game yet: applying the patches at
runtime, gameplay at levels 21..31, the real runtime `F20`/`D20`, the owner's save/reload and
multiplayer remain to be verified in game.

---

# RoguelikeUnlimitedLevelProgression (português)

Remove o teto de nível 20 do modo Roguelike **em singleplayer (v0.1)**: um nível por vitória,
XP estendido depois do 20 (linear, `F(L) = F20 + D20·(L-20)`, com `F20`/`D20` lidos do próprio
jogo) e recompensas de Skills/Itens/Atributos que continuam funcionando quando um pool esgota
— o skill pulado vira um **recibo durável** (sidecar JSON por personagem) e é subtraído da
contagem da fila, para não ser perdido em silêncio.

Nada mais muda: sem áreas novas, sem endless, sem ouro inventado, sem remover teto de item ou
de fortune, sem Bard/música, sem conquista forçada e sem alteração de campanha. Campanha e IA
ficam **fora** do escopo ampliado e mantêm a comparação vanilla; em multiplayer o branch
vanilla é preservado com aviso. O grupo de patches de gameplay é **tudo-ou-nada**: qualquer
alvo ausente, exceção ou recusa do transpiler reverte o mod inteiro.

Build: as DLLs do jogo ficam em `lib/` na **raiz do checkout** (gitignored, nunca versionadas nem
copiadas para o repositório/worktree) e são resolvidas por caminho relativo ao próprio checkout,
sem caminho absoluto do computador do dono. Um clone/worktree isolado sem `lib/` própria falha com
`LEVEL-LIB: lib de referencias nao encontrada em '<...>\lib'` e exige o override autorizado
`-p:CommonLibDir=<caminho absoluto>`; não existe fallback silencioso.

O código foi **compilado e exercitado** em bancada isolada (harness que compila os fontes reais
do mod e alimenta o transpiler real com a IL real de `Root.SendGameCompleteFromServer`). A
execução dentro do jogo — aplicar os patches, jogar nos níveis 21..31, `F20`/`D20` reais,
save/reload do dono e multiplayer — ainda é **NAO_EXERCITADO** nesta fase.
