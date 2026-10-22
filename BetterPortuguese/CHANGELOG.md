# Changelog — BetterPortuguese

> Dates use ISO 8601 (BRT, UTC−03:00). Preparation dates are not publication dates.
> CHG-REV documentation audit: 2026-10-16. No publication performed.
> BP-6 packaging: 2026-10-17 (BRT). Release package built and pre-flighted; nothing published.

## 0.2.0 — in preparation (2026-10-21)

- **Textos que não passavam pelo funil de localização agora são traduzidos no display.** As linhas de
  efeito dos eventos (`★ Reroll a skill`, `★ Level up Fortunes`) vêm do asset do evento e são escritas
  direto no TMP por `EventOptionSelectionItem.PopulateResultEffects` / `EventResultEffect.SetEventAction`;
  passam a ser traduzidas por correspondência exata (`Role novamente uma habilidade`, `Aumente o nível das
  suas Fortunas`). O rótulo do nó de batalha no mapa (`NavNodeVotingButton`) sai em inglês pelo mesmo
  motivo: `Battle` → `Batalhar`, `Hard Battle` → `Batalha Difícil`, `Rest` → `Descanso`. Rótulo ou linha
  desconhecida é registrada uma vez no log (`BP-EVENTO` / `BP-TEXTO`) com `Diagnostico=true`, nunca inventada.
- **Dataset: 1.412 chaves corrigidas** (eram 1.319). Correções aprovadas pelo dono nesta rodada:
  - `Steal Action` "Ação de Roubo" → **"Roubar Ação"**.
  - `Resume` "Currículo" → **"Continuar"** (botão de retomar, não currículo).
  - `Battle` "Batalha" → **"Batalhar"** (verbo, como o botão pede).
  - `Level up all your owned Fortunes…`: concordância de gênero → "Eleve **todas as suas** Fortunas possuídas…".
  - **"pilha" → "acúmulo" em 133 entradas** (stack de efeito), com concordância refeita
    (`um acúmulo`, `os acúmulos`, `novos acúmulos`, particípios masculinos). Pilhas FÍSICAS preservadas
    ("Pilha de Ouro", "pilha de tesouros", "pilhas de mapas", "pilha de cinzas").
  - Redação das linhas de acúmulo (8 chaves): "consome todas as cargas de Petrificação",
    "Ganhe um acúmulo ao final de cada turno; qualquer movimento remove todos eles",
    "aplicado aos inimigos", "para cada acúmulo de Resfriado/Calor nos alvos".
  - Quatro chaves com template `@tag@` (`LANG-02954/03154/05592/07135`) passaram a ser `addEntry`
    no diff — como `edit` elas derrubavam o parse e desligavam a camada base inteira.
- **Adaptador BP↔BetterTooltips fixado em BetterTooltips 0.1.6** (constante e `modVersion` do
  `pt-BR.mods.json`, 177 regras).
- Nenhum asset do jogo é editado; tudo é sobreposição em runtime.

## 0.1.1 — in preparation (2026-10-19)

- Fix rarity gender agreement when composing item names, for example `Lendário Varinha` → `Lendária Varinha`.
- Fix the composed `Healing` label: `Cura de Dano` → `Cura por Dano`.
- These are runtime composition patches, not dataset changes. The same 1,319 owner-approved dataset corrections remain byte-for-byte unchanged.
- Versioned BP-MODS-1 adapter for the optional BetterTooltips 0.1.5 (177 rules in `pt-BR.mods.json`): BP's localized origin is preserved, BT regroups its English block identities, and only BT-owned note/header/aura/fragment text is translated last. Missing or unhomologated BT disables this layer alone, with a warning; no `Update` hook and no BT/game asset edit. Native menu skill/status captures and disabled/English controls are recorded in the task report; live-combat aura/synergy lists are not claimed as runtime-verified.
- Package preparation only: no installation or publication. Publication requires the owner's explicit go-ahead; offline validation does not replace an in-game check of this exact build.

## 0.1.0 — in preparation (implementation recorded on 2026-10-13)

- Independent BetterPortuguese project, GUID com.gumatos.betterportuguese; no game assets edited.
- Two complete Original/Corrigido snapshots, embedded and accompanied by auditable copies/hashes in the package.
- Corrigido is the default; Original mode returns the game's localization exactly as recorded in the snapshot.
- **Dataset:** 1,314 owner-approved corrections applied (text edits to existing entries plus `addEntry` for records the game left empty). The offline suite asserts that count and the packager recomputes it as `contentState`; per-file SHA-256 lives in `plugins/BetterPortuguese/Data/manifest.json`, not in this changelog.
- Only owner-approved corrections are applied, and approval is not the same thing as runtime proof. The in-game acceptance run recorded so far exercised an earlier, 14-correction build (`BetterPortuguese.dll` SHA-256 `2fc17bf4ed46300a4973c63d8ee6f892a7bf5bbcb6ec6ec138bc394062ac05b4`); **the in-game round for this 0.1.0 package is pending**. Approval, build, packing and runtime validation are separate gates, and a green build never authorizes publication.
- Strict parser, diff/approval validation, ordinal lookup, full baseline and clones on override. An approved `addEntry` can create one neutral value for a record the game left empty, keeping that record's functional tokens/tags; populated lists, gender variants and removals are refused.
- Main-thread configuration/queue, runtime .cfg reading, targeted UI refresh and safe failure/capped logging.
- Separate, empty mod registry; no approved translations/adapters in this snapshot.
- **Icon:** the local artwork changed after `917c20a`; this does not modify the snapshots or imply editorial approval.
- Debug/Release and offline core/API/resource/Harmony test bench. The runner takes the expected changed-key count from `plugins/BetterPortuguese/Data/manifest.json` (`coverage.changedKeys`), so the documented command runs without flags; `--expected-changes N` only overrides it for experimental candidates. Nothing published in this delivery; publication requires the owner's explicit go-ahead.
