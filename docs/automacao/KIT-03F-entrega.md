# KIT-03F — Entrega: correções da revisão KIT-03R

Tarefa: `t_160668bd` (KIT-03F) · Data: 2026-10-09 · Rodada **OFFLINE** (sandbox)
Implementador: perfil `default` (run desta sessão) · Revisor: perfil `default` (run separada)

## 1. Objetivo e escopo

Corrigir os 8 itens apontados pela revisão independente KIT-03R (`docs/automacao/KIT-03R-revisao.md`,
parecer REPROVADO, 3 FALHOU / 5 ACHADO / 1 NÃO_EXERCITADO), provar cada correção por execução
real — incluindo **controle negativo plantado** — e devolver para recontra-revisão.

Tocados: `scratch/kit/*.sh` (6 arquivos + 2 novos) e `docs/automacao/KIT-03-entrega.md`.
**Não** tocados: mods, `Assembly-CSharp.dll`, Bard, gameplay, travas, perfil do dono, saves.
Nada instalado/publicado; jogo não aberto/encerrado; nenhum save carregado; sem commit.

## 2. Correções por achado (com a prova executada)

| # | Achado KIT-03R | Correção | Prova (execução real) |
|---|----------------|----------|------------------------|
| 1 | C8 GRAVE — runner morre em `((TOTAL++))` (linha 59), exit 1, **nenhum teste roda** | contadores por atribuição (`TOTAL=$((TOTAL+1))`); `skip` conta SKIP (nunca PASS); exit fiel (falha **ou** skip ⇒ 1) | `Total: 6 / Passou: 6 / Falhou: 0 / Pulados: 0` → **exit 0** |
| 2 | C4 GRAVE — `prove-isolation` tautológico, conclusão fixa, exit 0 no ramo FALHOU | conclusão **derivada** da comparação real de caminhos (containment); exit 1 quando o save de teste cai dentro de `SAVES_DIR` | legítimo: exit 0; `SAVES_DIR=scratch/kit/isolated-saves`: **exit 1** + `Isolamento: FALHOU` |
| 3 | C5 GRAVE — lock lê `tail -1` (worker) como PID; 2º acquire passa por cima | lock de **1 linha** `ts\|holder\|worker\|caller`; processo-**sentinela** mantém o lock VIVO; 2º acquire recusado; `--force` com efeito | 1º acquire exit 0 (holder vivo); 2º acquire **exit 1**; `check` exit 1; `release` mata o sentinela |
| 4 | C3 — rollback só apaga lista global; `hashes-antes.txt` nunca conferido | rollback por **DIFF** contra o snapshot + conferência de hashes; **falha (exit 1)** se o estado não voltar exato | `new2.dll` e `plugins/new.dll` (não listados) removidos; arquivo apagado recriado; snapshot adulterado ⇒ **exit 1** |
| 5 | C2/C6 — `detect-env.sh` depende do cwd; JSON fora de `KITS_DIR`; `Player.log` errado; cadeia morta do CIC | caminhos por `$(dirname "$0")`/`KITS_DIR`; JSON em `$KITS_DIR/detect-env-result.json`; `Player.log` = `%LOCALAPPDATA%LocalLow\...`; CIC em `if/elif/else` | roda da raiz **e** de outro cwd (exit 0, `pass_count=12`, `fail_count=0`, `player_log_encontrado=true`) |
| 6 | C6 — `C:/Users/Pichau/...` fixo + 4 scripts ignorando `KITS_DIR` | caminhos derivados do próprio script; removido caminho do dono | `grep -rn "C:/Users/Pichau" scratch/kit/*.sh` → só comentário |
| 7 | C1 — entregável com “Hashes SHA256: A preencher” e saves em caminho inexistente | hashes reais preenchidos; caminhos alinhados ao que o script valida; história preservada em “Correção KIT-03F” | ver §4 (hashes) e §3 (caminhos) |
| 8 | C9/C10 — Teste 6 apontava para `scratch/tools/...`; zero reuso; pre-flight de build só em prosa | Teste 6 aponta para `tools/automacao/...` e **executa** o harness existente; novo `build-preflight.sh` com `-p:DeployToBepInEx=false` em cópia isolada | harness `roda_testes_runtime.py`: **VERDE, 15 testes**; build isolado exit 0, perfil **INTACTO** |

## 3. Caminhos validados por execução (existem no disco)

- Jogo: `E:\SteamLibrary\steamapps\common\Stolen Realm` (existe; `Stolen Realm.exe`)
- Perfil r2modman: `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx` (existe)
- Logs: `<perfil>\LogOutput.log` (existe) e
  `%LOCALAPPDATA%LocalLow\Burst2Flame Entertainment\Stolen Realm\Player.log` (existe, ~1,6 MB)
- Saves: `%LOCALAPPDATA%\Abyssus\Saved\SaveGames` (existe — `Profile1.sav`, `GameSettings.sav`,
  `Profile1_Temp.sav`, `SAVE_GAME_SESSION_SLOT.sav`, `steam_autocloud.vdf`)
- Caminho de saves **errado** que o entregável declarava antes
  (`%LOCALAPPDATA%Low\Burst2Flame Entertainment\Stolen Realm\Saved\`) **não existe** — corrigido.

## 4. Hashes SHA256 (medidos 2026-10-09, estado final entregue)

```
66085afcfcaa623bc91b390ba5144ed370b1515bd59fc02a58ca13e26e01198d  scratch/kit/run-isolation-tests.sh
20df7c170f486c6579952d7acdf4086dd4ec6d0da2c8ffe2223bcb14b80835ae  scratch/kit/detect-env.sh
37387df0d67cd1ba8bd28c5a48c9810dfbc99cf2ecae694bf3449d8d0e9c77b7  scratch/kit/snapshot.sh
fee48264e02a1e5c27d3590ccfedf0df4ca86f0a7b592b378687b7d163e2ecaa  scratch/kit/isolacao.sh
fbf15da9f148162e8b06d4a3d61bcdb7400be3491c58e5ed6984c8eeb1e8dd1e  scratch/kit/front-unica.sh
44eb7ecc72317d4bb90ce69a0f3f271ab30eb793df28d46c19466530aab4787b  scratch/kit/controle-negativo-kit.sh   (NOVO)
7813b74784dadea41174fc7cb49c21a062775cf51f1f9b7498cba36dec3e28b3  scratch/kit/build-preflight.sh        (NOVO)
65590bf943e99e787bd4d4f5455be66876ecd4edfcf0162b549c25075c6888aa  docs/automacao/KIT-03-entrega.md
```
(não constam aqui os hashes deste próprio `KIT-03F-entrega.md` — auto-referência é impossível;
o hash é calculado pelo revisor a partir do disco).

Hashes do estado **anterior** (citados pela KIT-03R) preservados no entregável como histórico:
`9faa67e5…` runner, `de87e727…` isolacao, `cddcfd35…` front-unica, `4f826b1a…` snapshot,
`996fa18e…` detect-env, `d7203e67…` KIT-03-entrega.md.

## 5. Controle negativo (exigência central do aceite)

`scratch/kit/controle-negativo-kit.sh` copia os scripts para a sandbox
`scratch/kit-sandbox/` (mantendo a profundidade para o `REPO_ROOT` continuar correto), planta
**um** defeito da KIT-03R e roda o runner com `KITS_DIR` na sandbox:

| Caso | Defeito plantado | Resultado |
|------|------------------|-----------|
| A | nenhum (sandbox limpa) | **VERDE** (exit 0) |
| B | C8: `set -e` + `((PASSED++))` | **VERMELHO** (exit 1, morre no 1º contador) |
| C | C4: containment cego (`inside` sempre NO) | **VERMELHO** — `Teste 4` FAIL |
| D | C5: lock volta a ler `tail -1` como PID | **VERMELHO** — `Teste 5` FAIL (`2º acquire NAO foi recusado`) |
| E | C3: rollback ignora diff e conferência | **VERMELHO** — `Teste 2` FAIL (`new2.dll SOBREVIVEU`) |

`Casos OK: 5/5` · `VEREDITO: OK` · exit 0.

## 6. Evidências (arquivos)

- `scratch/kit/negativo/FINAL-verificacao.txt` — execução consolidada (runner + controle negativo + pre-flight + hashes)
- `scratch/kit/negativo/A-sandbox-limpa.log` … `E-C3-rollback-nao-exato.log` — saída de cada caso
- `scratch/kit/logs/test001-detect-env.log`, `test004-isolation.log`(+`-negativo`),
  `test005-acquire2.log`, `test006-runtime.log`, `test002/003-*.log` — logs por teste (agora **existem**)
- `scratch/kit/logs/build-preflight-*.log` — build isolado
- `scratch/kit/results/results-*.json` — resultado JSON do runner (PASS/6)
- `scratch/kit/backups/<ts>/` — snapshots reais com `arquivos-antes.txt`, `diretorios-antes.txt`, `hashes-antes.txt`, `files/`
- `docs/automacao/KIT-03F-parte01.md`, `-parte02.md`, `-parte03.md` — registro por bloco

## 7. O que NÃO foi feito (limites honestos)

- Nenhum teste em jogo (instalar/abrir/save) — fora do escopo autorizado desta rodada.
- O build pre-flight foi exercitado com **ReloadProbe** (build independente do jogo);
  mods do produto não foram buildados e nada foi deployado (`-p:DeployToBepInEx=false`).
- Nada foi instalado no perfil do dono; a checagem do perfil é por hash de listagem
  (`arquivo|tamanho|mtime`) de `scripts/` e `plugins/` antes/depois do build.
- Não houve commit/`git add`; scripts ficam em `scratch/kit/` (área ignorada pelo git).

## 8. Nota de fato (não é defeito)

O default `SAVES_DIR=%LOCALAPPDATA%\Abyssus\Saved\SaveGames` **existe** e contém
`Profile1.sav`/`GameSettings.sav` — o caminho do script estava certo; o errado era o
entregável, agora alinhado. `Player.log` fica em **LocalLow** (o script apontava para
`Local/Low`, inexistente) e `LogOutput.log` fica na raiz do perfil BepInEx.

## 9. Encaminhamento

Devolvido para reconferência independente (run separada) via `kanban_request_review`,
com implementador e revisor preenchidos. **Não** autoaprovado. Os cartões dependentes
(KIT-G1 `t_49c93c37`) permanecem bloqueados até a aprovação da revisão.
