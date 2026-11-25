# Changelog — BetterPortuguese

> Dates use ISO 8601 (BRT, UTC−03:00). Preparation dates are not publication dates.
> CHG-REV documentation audit: 2026-10-16. No publication performed.
> BP-6 packaging: 2026-10-17 (BRT). Release package built and pre-flighted; nothing published.

## 0.2.2 — 2026-11-25

- **BP-CTX-1: revisão contextual do PT-BR aprovada pelo dono, aplicada ao dataset.** 56 entradas passam a usar o
  vocabulário do jogo: `Might` como atributo vira **Força** (sem tocar em `Power`/Poder, nomes próprios nem o verbo
  modal); `Party` vira **Grupo** nos retratos e eventos; a duração de efeito passa a dizer **turno** em vez de "virar";
  o Bardo fica padronizado em **canção** e **acúmulo**, preservando alcance, custo de mana e a diferença entre tocar
  de novo e repetir no início do turno.
- O diff aprovado passa de 1412 para 1464 chaves; 4 chaves já aprovadas foram reaprovadas com o texto novo. Nada de
  loot, XP, escolha de recompensa ou mecânica foi alterado.
- **Pendente:** 31 chaves que só existem na beta 1.4.9 (Bardo) não estão no snapshot LANG-R1 e precisam da
  reextração do snapshot antes de poderem ser aplicadas.

## 0.2.1 — 2026-11-23

- **Compatibilidade com a nova versão beta do jogo: 1.4.8 / buildid 26767595 (Bard Pack).** As mudanças abaixo existem para o mod funcionar nessa build; o comportamento na 1.3.1 estável é preservado.

- **Identidade de build atualizada para a beta 1.4.8** (`Assembly-CSharp` sha256 `6e97d5f5…d7a`): a camada compilada (BP-COMP) voltou a ser aceita, em vez de recusada pelo pin da 1.3.1. A recusa continua fail-closed quando o hash não bate, e a mensagem agora traz medido e esperado.
- Ver `docs/automacao/SR-BETA-06-pin.md`.

## 0.2.0 — in preparation (2026-10-21)

- **SR-BETA-06 — trava de assembly re-pinada para a build em uso (1.4.8).** `Composition.AssemblySha256` passa a
  `6e97d5f543b631443af6b5c9b4737c46ce72bf3b4b2bd909abc8f478b2782d7a` (medido no `Assembly-CSharp.dll` instalado,
  branch `open_beta`, build 26767595). Mesma política do RealmApi: pin único e exato, não faixa; se o hash não bater,
  BP-COMP/BP-MODS continuam sendo **recusados** e a mensagem agora mostra medido **e** esperado. O dataset pt-BR e
  `Core/ResourceHashes.cs` continuam os da extração 1.3.1 — re-extrair contra 1.4.8 é passo do dono.

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
