# KIT-03G1 — Prova runtime EM JOGO — parte 04: execução, evidência bruta e veredito

Cartão: `t_09e856b1` (KIT-03G1) · Worker: perfil `default` · 2026-10-09 18:00–18:04 BRT.
Dá sequência a `KIT-03G1-parte03.md` (reconhecimento/plano). Rodada **autorizada pelo dono** (ver parte 03 §1).

## 1. Resultado em uma linha

`bash scratch/kit/runtime-isolado.sh run` executado **DUAS vezes** com o jogo FECHADO: as duas
**VEREDITO: OK (exit 0)** — o jogo abriu, o BepInEx subiu A PARTIR DA CÓPIA ISOLADA, o mod-probe
apareceu no `LogOutput` DA CÓPIA, o perfil/saves do dono ficaram com hash bit-a-bit idêntico, e o
jogo foi fechado pelo PID que a própria prova abriu. O modo `run` deixou de ser NAO_EXERCITADO.

## 2. Rodada 1 — `runtime-isolado.sh run` (18:00:42 → 18:01:02)

Log: `scratch/kit/logs/G1-run-20261009-180042.log`
(sha256 `cbb84d53b7cf51a854e3f2b000ed03234c6704305668fa533c9becdf95a5eb13`)

Trecho literal, do início ao veredito:

    [18:00:42] === PROVA RUNTIME REAL (KIT-03G1) ===
    [18:00:43] OK: copia isolada criada (core/ + plugins/ + config/)
    [18:00:44] OK: containment /c/dev/stolen-realm/scratch/kit/runtime-iso/BepInEx FORA de ...\profiles\Default\BepInEx
    [18:00:44] OK: probe INSTALADO (ReloadProbe.dll)
    [18:00:44] Lancando o jogo via Steam (...steam.exe) com doorstop na COPIA:
    [18:00:44]   --doorstop-target-assembly .../runtime-iso/BepInEx/core/BepInEx.Preloader.dll
    [18:00:55] OK: LogOutput isolado existe (.../runtime-iso/BepInEx/LogOutput.log)
    [18:00:55] OK: marcador encontrado no log ISOLADO
    [18:00:55] OK: log usado != log do dono
    [18:00:56] OK: plugins/ do dono INTACTO
    [18:00:56] OK: core/ do dono INTACTO
    [18:00:56] OK: LogOutput do dono INTACTO
    [18:00:56] OK: saves do dono INTACTOS
    [18:00:56] VERIFICAR: OK (0 falhas)
    [18:00:56] Fechando SOMENTE o PID que abrimos (22640) via CloseMainWindow
    [18:01:02] OK: rollback removeu a area isolada (.../runtime-iso)
    [18:01:02] OK: perfil e saves do dono intactos apos o rollback
    [18:01:02] VEREDITO: OK

Do lançamento ao boot completo do BepInEx: **11 segundos**. Nenhum save é carregado (a prova vai só
até o boot/menu).

## 3. Rodada 2 — reprodução + evidência BRUTA preservada (18:01:57 → 18:02:17)

O `run` apaga a área isolada no rollback, então a rodada 1 não deixou o `LogOutput` da cópia no
disco. Para que o artefato de prova sobrevivesse, esta rodada foi executada sob um observador
externo (`scratch/kit/G1-evidencia-run.sh`, arquivo NOVO, não altera o entregável): ele roda a
prova e, no instante em que o marcador aparece, copia a área isolada para fora antes do rollback.

Resultado: `run_exit=0`, `capturou_log_isolado=sim`.

**Evidência BRUTA — `scratch/kit/logs/G1-evidencia-20261009-180156/BepInEx/LogOutput.log`**
(sha256 `640966e58fb7c44bc0cbde7835a796d4bb21c41d8f3f98ced60a0c39c21786f4`) — conteúdo integral:

    [Message:   BepInEx] BepInEx 5.4.23.5 - Stolen Realm (12/09/2026 21:34:42)
    [Info   :   BepInEx] Running under Unity v2022.3.62.7762112
    [Info   :   BepInEx] CLR runtime version: 4.0.30319.42000
    [Message:   BepInEx] Preloader started
    [Info   :   BepInEx] Loaded 1 patcher method from [BepInEx.Preloader 5.4.23.5]
    [Info   :   BepInEx] 1 patcher plugin loaded
    [Info   :   BepInEx] Patching [UnityEngine.CoreModule] with [BepInEx.Chainloader]
    [Message:   BepInEx] Preloader finished
    [Message:   BepInEx] Chainloader ready
    [Message:   BepInEx] Chainloader started
    [Info   :   BepInEx] 1 plugin to load
    [Info   :   BepInEx] Loading [Reload Probe 1.0.0]
    [Info   :Reload Probe] ReloadProbe v1 carregado.
    [Message:   BepInEx] Chainloader startup complete

Isso é a prova de que **o BepInEx rodou com raiz na CÓPIA** (o `Preloader` carregado é o da cópia),
que **o mod-probe instalado na cópia foi o único plugin carregado** (`1 plugin to load` →
`Loading [Reload Probe 1.0.0]` → `ReloadProbe v1 carregado.`) e que o `LogOutput` foi escrito
**dentro da cópia** — nenhum log foi escrito no perfil do dono (ver §5).

Complementares da mesma rodada:
- `scratch/kit/logs/G1-evidencia-20261009-180156/listagem-area-isolada.txt`
  (sha256 `4d4c4e345a5983660fd5f9b99c3f00c2638cda082e1f7d5cf596002c28a91fa4`, 23 arquivos):
  contém `./BepInEx/plugins/KitRuntimeProbe/ReloadProbe.dll` — o probe existe **na cópia**, e o
  `find` do perfil do dono não tem esse caminho.
- `scratch/kit/logs/G1-evidencia-20261009-180156/Player.log` — log do Unity da sessão (prova
  independente de que o processo do jogo REALMENTE subiu: `Mono path[0] = 'E:/SteamLibrary/...`,
  `Initialize engine version: 2022.3.62f2`).
- Log da rodada: `G1-evidencia-run-20261009-180156.log`
  (sha256 `b5a25f4734f3024381377f904b4cc9238e1811ee1af84c1073d658fb76d91c07`), com PID 6428 fechado
  por `CloseMainWindow` e `VEREDITO: OK`.

## 4. Isolamento medido nas TRÊS pontas

Hashtirado com a MESMA função (`hash_tree`) do script, antes / depois da rodada 1 / depois da rodada 2:

| Superfície | Antes (18:00:35) | Depois R1 (18:01:43) | Depois R2 (18:04) |
|---|---|---|---|
| `core/` do dono | `b1594200…` | `b1594200…` | `b1594200…` |
| `plugins/` do dono | `6eae7a3c…` | `6eae7a3c…` | `6eae7a3c…` |
| `LogOutput.log` do dono | `\9bedadac…` | `\9bedadac…` | `\9bedadac…` |
| árvore de saves | `04ef12fa…` | `04ef12fa…` | `04ef12fa…` |

O `LogOutput` do dono segue com **mtime 17:55:48 / 1.744.007 bytes**, congelado desde antes da
rodada; os `.sav` seguem com **mtime de 08/10**. Medição independente (não só o script):

    find <perfil do dono> -newermt '2026-10-09 17:56' -type f   ->  VAZIO

Ou seja: **nenhum arquivo do perfil do dono foi escrito depois que a sessão dele terminou.**
O `ReloadProbe.dll` que aparece em `<perfil>/scripts/` é de **29/09** (pré-existente, do
ScriptEngine) — não foi tocado nem usado por esta rodada.

## 5. Sobre o `-p:DeployToBepInEx=true` (opt-in) — decisão registrada

O opt-in de deploy **não foi acionado** e não precisava ser: a tarefa é *isolar* a prova runtime, e
o desenho instala o probe **na cópia** (`runtime-iso/BepInEx/plugins/KitRuntimeProbe/`), nunca no
perfil do dono. Isso é a política 3.4 do `KIT-03-entrega.md` ("nunca buildar direto no perfil do
dono; deploy manual só após aprovação humana"). O `ReloadProbe.dll` usado já existia, buildado em
`scratch/kit/build/20261009_152651/` com `-p:DeployToBepInEx=false` (preflight do KIT-03F). Se o
dono queria também uma instalação REAL no perfil do dono, isso é outra prova (perfil do dono +
r2modman) e não é o escopo deste cartão — fica registrado para não haver dúvida.
`Assembly-CSharp.dll` não foi tocado em nenhum passo; nada foi publicado.

## 6. Achado colateral da parte 02 §2 — CONFIRMADO E RESOLVIDO

A parte 02 registrou como **hipótese** que o Teste 6 do runner estaria vermelho só por causa da
sessão viva do dono escrevendo no `LogOutput`. Medido agora, com o jogo fechado:

    bash scratch/kit/run-isolation-tests.sh
      Total: 6 / Passou: 6 / Falhou: 0 / Pulados: 0
      [PASS] Teste 6: Reuso da infraestrutura existente (harness runtime)   (15 testes verdes)
      VEREDITO: VERDE — 6/6 testes        (exit 0)

Hipótese **confirmada**: o vermelho era do ambiente (sessão viva), não da entrega do KIT-03F. Nenhum
arquivo de `tools/automacao/**` nem dos scripts do KIT-03F foi alterado para isso — o mesmo runner,
inalterado, agora passa.

## 7. Frente única respeitada

As duas rodadas foram seriais, cada uma com `lock acquire` → `release` do `front-unica.sh`; entre e
depois delas o lock mede "Lock ativo: NAO / Lock disponivel". Nenhuma segunda instância do jogo
existiu em nenhum momento (medido por `tasklist` antes, entre e depois das rodadas).

## 8. Veredito

**PROVA RUNTIME EM JOGO: OK (exit 0, reproduzida duas vezes).** O modo `run` do
`scratch/kit/runtime-isolado.sh` (sha256 `60495a3f…`, inalterado) está EXERCITADO e provado:

- instala o mod **na cópia isolada** e o jogo carrega essa cópia;
- verifica pelo **LOG da cópia** (`LogOutput.log` bruto preservado);
- confere hashes do dono antes/depois (perfil, plugins, core, log e saves) — intactos;
- fecha **somente o PID que ela mesma abriu** (`CloseMainWindow`);
- faz rollback exato da área isolada.

Sem pendências para o escopo do cartão. Nenhum arquivo de mod, do perfil do dono ou de
`tools/automacao/**` foi modificado; só foram criados arquivos novos em `scratch/kit/` e
`docs/automacao/`.
