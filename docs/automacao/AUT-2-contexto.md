# AUT-2 — contexto do inventário e da matriz de cobertura

Tarefa: `t_9f420f69` · gerado em modo **somente leitura** (nenhum build/teste/commit/deploy/publicação,
nenhum runtime de jogo). Fonte de verdade dos dados: `docs/automacao/AUT-2-matriz.json`.

## Método

- Inventário por parsing robusto de `git status --porcelain -z --untracked-files=all` (separador NUL),
  sem exclusão silenciosa. Cada arquivo recebeu `sha256` do conteúdo no disco.
- Snapshots de partida e final gravados (`.git-snapshot-*.status*.z`, efêmeros — removidos ao final);
  o conjunto inventariado foi reconciliado entre os dois (veredito no JSON).
- Categorias: **código / teste / doc / dados**; `mod` é campo separado.
- Procedência: **indeterminado** para alterações de working tree (sem prova de autoria/commit nesta
  rodada). `release/mods.json` é registro **local**, nunca prova online.

## Números verificados (working tree, HEAD `f526fe9`, branch `ci-validate-test`)

- **78 alterações de produto**: 37 modificadas (M) + 41 novas (??). Excluídos os **2** entregáveis do
  próprio `docs/automacao/` (`AUT-2-contexto.md` e `AUT-2-matriz.json`), registrados em
  `excluidos_da_coleta`; nenhum outro arquivo foi excluído.
- Por categoria: **código 3 · teste 45 · doc 17 · dados 13**.
- Por mod: BetterTooltips 48 · transversal 23 · RSTV 3 · BetterCombatText/BetterFont/BetterStats/RoguelikeDebugger 1 cada.
- **12 alterações sem tarefa mapeada** (arrays `tarefa:["nao_mapeada"]`) — não foram inventadas tarefas.
- Reconcilição partida↔final: **sem drift na leitura da coleta** (conjuntos idênticos) → inventário estável;
  **não re-verificável** (snapshots `.z` removidos) — ver errata abaixo.

## Código alterado (os 3)

| arquivo | tarefa | estado real |
|---|---|---|
| `BetterTooltips/Patches/LocalizePatch.cs` | BUG-34a (+RV-43/TX-1) | contexto de feed `[ThreadStatic]` + patches em `Root.SendMessageWindowMessage`; bin/perfil 05/10 13:36 |
| `BetterTooltips/Patches/ShrineAuraPatch.cs` | RV-50/RV-49/RV-30/RV-44 | trabalho de shrine local (04/10 00:24) |
| `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs` | RSTV-26a | hover usa `ReadOnlySession.Target` + `showCanLevelDetail:false`; bin/perfil 05/10 13:32 |

## Estados separados (Fonte · Release · Perfil · Online)

`bin/Release == perfil` para os seis; `dll-do-zip == bin/perfil` só para **4 mods**
(BetterCombatText 0.1.1, BetterFont 1.0.2, BetterStats 1.0.1, RoguelikeDebugger 0.1.1).

**Divergência material (versão igual ≠ bytes iguais):**
- `BetterTooltips`: bin/perfil `270f311b…` ≠ dll do zip 0.1.3 `80bba454…`.
- `RoguelikeSkillTreeVisualizer`: bin/perfil `454587a0…` ≠ dll do zip 0.3.2 `c2ce4862…`.

Ou seja: BUG-34 e RSTV-26 estão **deployados localmente e não empacotados/publicados**.
Publicação online: **NÃO VERIFICADA** nesta rodada (exigiria consulta por pacote na API da Thunderstore).

## Cobertura exigida — todos no JSON

- **Seis mods** (M1–M6): BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RSTV.
- **RSTV-6** (bateria entregue), **RSTV-21** (bump 0.3.2 feito; 21a/21c abertos no KANBAN; online só local),
  **RSTV-25b** (diagnóstico adicionado — **INDETERMINADO**; o log existe, mas o marcador `RSTV-25:` não foi
  localizado e a causa da ausência é **INDETERMINADA**), **RSTV-26** (fix local+deployado, não publicado).
- **RV-26/27/28/29/31/33/34** (S-*): implementados no fonte/CHANGELOG; conferência por `checa_shrines.py`; falta revalidação em jogo e o **RV-49** trava os números das auras de perigo.
- **BUG-34**: aceite humano em 05/10 (KANBAN l.506) — **não reabrir**; restam revisão independente/regressão e entrega.
- **Reuso de infraestrutura**: CAP-1 (`scratch/cap1/rotina-cap1.sh`, `consolida.py`, `CapProbe`), runner único `tools/testes/roda_testes.py` (exit 0/1/2), conferidor `tools/checa_shrines.py` (exit 0/1/2/3), gerador `tools/gera_shrines_esperado.py`, OCR `tools/ocr_tela.ps1`.

## Lacunas e humano residual (resumo)

- Bytes FONTE↔DLL **não provados** (mtime só sugere build após a edição) → prova na bancada AUT-3.
- Nenhum build/suite/conferidor executado nesta tarefa → AUT-3 roda e prova; AUT-4/5/6 coletam em jogo.
- **RV-49** e **RSTV-25b** dependem de medição/estado do jogo → só humano/rotina autorizada.
- **Aprovação de envio (publicação)** é decisão do dono; automação não substitui aceite humano.

## Plano mínimo AUT-3 / AUT-4

- **AUT-3** (bancada estática/build, sem deploy): `dotnet build … -p:DeployToBepInEx=false` dos 3 mods com
  código alterado + `tools/testes/roda_testes.py --puros` + `checa_shrines.py` sobre log de fixture +
  contra-provas em sandbox; saída JSON com exit code real. Provar FONTE→DLL por hash pós-build.
- **AUT-4** (coleta runtime): estender CAP-1 (`rotina-cap1.sh`/`consolida.py`) para ler do objeto vivo
  (texto/estado/fonte/material/cor/geometria) com espera de estado, controle negativo e restauração;
  consumir no AUT-5 (RSTV-6/21/26, T4→T5) e AUT-6 (RV-26…34 + BUG-34), uma única frente controlando o jogo.

## Errata — correção pós-revisão independente AUT-2R (2026-10-05)

Revisão fonte (preservada, somente leitura; histórico **não** apagado): `docs/automacao/AUT-2R-revisao.md`.
Correções documentais aplicadas a este contexto e ao `AUT-2-matriz.json`. **IDs, caminhos, categorias, mods
e sha256 dos 78 registros não foram regenerados nem alterados** (nenhum `git status` foi reexecutado nesta
correção, para não contaminar a matriz com artefatos de outros agentes).

- **Exclusões**: eram **2** (não 6) — os entregáveis `AUT-2-contexto.md` e `AUT-2-matriz.json`, agora
  registrados explicitamente em `excluidos_da_coleta`.
- **RSTV-25b**: `LogOutput.log` **existe** (`…\profiles\Default\BepInEx\LogOutput.log`, 1.234.333 B, 05/10
  14:32; RSTV-20/21 presentes), mas o marcador `RSTV-25:` **não** foi localizado. A causa da ausência é
  **INDETERMINADA** — não se afirma categoricamente que o caminho de linhas de dependência não foi exercido.
- **BetterTooltips**: **48** alterações locais (não 37 — 37 é o total **global** de arquivos M).
- **Drift**: o "sem drift" passa a ser **leitura da coleta**, **não re-verificável** (snapshots `.z` removidos);
  o fato atual do revisor fica separado em `reconciliacao_snapshots.revisao_aut2r`.
- **Hash da matriz**: antes `e43e8ce0…30292` → depois `8503010272d79753f6267c5f020b82721767de19e7c0f5276ae9544745be5d05`.
