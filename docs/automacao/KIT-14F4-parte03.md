# KIT-14F4 — parte03: provas RED/GREEN (hashes e artefatos)

## Identidades

| artefato | sha256 |
|---|---|
| fonte do consumidor corrigido (`RstvPostRender.cs`, sandbox) | `e3f58b31d8f2792ccb6af563b1bc898e97eaa2aaecac1ef6fc3559fd58ea4d16` |
| fonte base F2 (`RstvPostRender-baseline1525.cs`) | `048b6a6f69d844542e584fc201e670a54f61838b99b20d40bca60438a2adce4f` |
| DLL candidata `candidate6/bin/AUT4Probe.dll` | `c5fadede1b762b5ec6ee6e62453a83406cb576451d9788fb40e66a6bc0b06040` |
| DSS candidata `candidate5` (mesma lógica, pré-captura do alvo) | `9612011bd3638204a53e01f1eaffc5559dd68a0db34fa322caea591351bbe7aa` |
| patch de integração (não aplicado) | `scratch/kit/KIT-14F4-1533/patch-integracao.diff` (479 linhas) |
| gate full-rstv (inalterado) | `ca3d859a25fc40415987082f32a3d1e30d06f88c3bbc8ae6d104b4b7f25fa2b4` |

## Preflight de deploy (antes de compilar, por candidata)

`tools/check_deploy_optin.py`: controle negativo RED (`exit=1`, csproj insegura inerte, apenas
escaneada) e controle positivo GREEN (`exit=0`) — registrados em
`build/candidate*/commands.json` + `guard-red/guard-green` logs. Build sempre
`-p:DeployToBepInEx=false`, saída para a sandbox. `deployed=false`.

## RED

* `on1-detect.json` — boot `on1` (run1525) com o consumidor anterior: `exit=1`, 22 itens reprovados
  (nenhuma capacidade exercitada; `status=TIMEOUT`).
* `red-historical.json` — saída histórica congelada avaliada pelo MESMO detector: `exit=1`.
* Gate full-rstv: `exit=1`, `weakened=false` (não foi enfraquecido nesta entrega).

## GREEN (on6)

`python detect.py cases/on6/recorder-on/boot01 on6-detect.json` → `exit=1` (por 1 achado real de
geometria e 1 leitura ausente), com as capacidades cobertas exercitadas:

    RSTV-6-readonly-skills-pontos : OK
    RSTV-21-janela-ciclo          : OK
    RSTV-21-tooltip-restauracao   : OK
    RSTV-26-placeholders          : OK
    RSTV-6-readonly-personagem    : NAO_EXERCITADO (interface, não humano)
    RSTV-25b-dependencia          : NAO_EXERCITADO (não emitido pelo consumidor)
    RSTV-geometria-clipping       : REPROVADO (tooltip fora da tela sob hover sem ponteiro físico)

Eventos do ciclo (quadros, JSON real): `before_open 451`, `open_observed 453`,
`hover_handler 453`, `tooltip_observed 455`, `tooltip_png_requested 455`,
`tooltip_png_completed 461`, `close_handler 461`, `close_observed 465`, `reopen_handler 465`,
`reopen_observed 467`, `close_handler 467`, `close_observed 469` — 32 amostras em
`tree_after_open` (15), `tooltip_after_hover` (2), `tree_after_reopen` (15).

Texto real lido (amostra de árvore): `UnityEngine.UI.Text` "Fire", "Lightning", "Cold", …
(11 classes) e tooltip TMP `Fireball` / `Hurls a ball of flame dealing 20-27 fire damage…`.
Skill viva do hover: `Fireball`, guid `bc0660c5-3a8c-48be-a437-880b2541871c`, tipo `Fire`,
handler `RoguelikeSkillTreeVisualizer.RstvSkillHover.OnPointerEnter`,
caminho `…/RstvAllSkillTreesPanel/RstvTreeArea/RstvNodeContainer/RstvItem_Fire_T2_1`.

## Teardown por boot (verificado, não afirmado)

Cada `boot01` termina com `game_processes: []`, `production_junction: false`,
`production_backup_exists: false`, `isolated_profile_exists: false`, `own_lock_released: true`,
Cloud (`app_cloudenabled: ["0"]`) preservado como estava, e diff de restauração de
PlayerPrefs/conjunto `equal: true`.
