# KIT-03R — parte 03: front única, detecção de ambiente, infraestrutura e resíduos

## C5 — Front única / PID: FALHOU (o lock não exclui nada)

Comando (sandbox, arquivos de lock isolados):
```
LOCK_FILE=kit/lock-rev.txt PID_FILE=kit/pid-rev.txt bash kit/front-unica.sh acquire
  → [default] Lock adquirido: PID=332, Worker=default   EXIT1=0
  conteúdo de kit/lock-rev.txt:  linha1=2026-10-09 12:22:02  linha2=332  linha3=default
LOCK_FILE=kit/lock-rev.txt PID_FILE=kit/pid-rev.txt bash kit/front-unica.sh acquire   (2ª vez!)
  → ALERTA: Lock stale detectado (PID default inativo) → Lock adquirido: PID=337   EXIT2=0
LOCK_FILE=... bash kit/front-unica.sh check (com o lock de PID 337 ativo)
  → "Pode executar: lock stale detectado" / "OK (stale)"   EXIT_CHECK=0
```
**Achado A13 (grave, contraria "uma única frente runtime")**: o arquivo de lock tem 3 linhas
(tempo, PID, worker) mas o leitor usa `tail -1` como PID — lê `default` (worker), `kill -0 default`
falha, então **todo lock é tratado como stale** e a segunda execução adquire o lock por cima da
primeira. O controle de `acquire`/`check` nunca recusa; a "garantia de front única" é decorativa.
Somam-se: (a) o PID gravado é `$$` do próprio script, que morre no fim do comando — mesmo lido
corretamente o lock nasceria stale; (b) `--force` é parseado e nunca usado; (c) `do_release` rotula
o timestamp como "PID" no log.

## C2 — Detecção de ambiente: ACHADO (funciona só na raiz do repo; caminho de log/save errado no doc)

Comando: `bash kit/detect-env.sh` com cwd = `scratch/kit-revisao/sandbox` → **EXIT=1**, `Passou: 7 / Falhou: 5`:
```
[PASS] Jogo (Unity): E:/SteamLibrary/steamapps/common/Stolen Realm
[PASS] Perfil r2modman: %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx
[PASS] LogOutput.log: <perfil>\LogOutput.log
[FAIL] Player.log: C:\Users\Pichau\AppData\Local/Low/Burst2Flame Entertainment/Stolen Realm/Player.log
[PASS] Diretorio de saves: C:\Users\Pichau\AppData\Local/Abyssus/Saved/SaveGames
[FAIL] tools/automacao ... [FAIL] CAP-1: scratch/cap1/rotina-cap1.sh
[FAIL] AUT-4Probe: tools/automacao/runtime/coletor.py ... [FAIL] CIC-1: tools/automacao/cic-1.sh
[WARNING] Muitos componentes nao encontrados!   (exit 1, JSON NÃO é gravado)
```
- A14: `detect-env.sh` é **dependente do cwd** (usa `docs/automacao`, `tools/...`, `scratch/kit` relativos)
  e grava o JSON em `scratch/kit/detect-env-result.json` **sem** usar `KITS_DIR`. Rodado de fora da raiz
  (testado em `/tmp`) → exit 1 e nenhum artefato.
- A15: `PLAYER_LOG="$LOCALAPPDATA/Low/..."` — errado: `$LOCALAPPDATA` já termina em `\AppData\Local`,
  o correto é `LocalLow`. Verificado no disco: o Player.log real está em
  `C:\Users\Pichau\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm\` (existe), e o caminho do
  script NÃO existe → o [FAIL] é do script, não do ambiente.
- A16: **o entregável declara os saves no lugar errado**. `KIT-03-entrega.md` linha 91 diz
  `%LOCALAPPDATA%Low\Burst2Flame Entertainment\Stolen Realm\Saved\`; o disco mostra que os saves reais
  (`Profile1.sav`, `GameSettings.sav`, `SAVE_GAME_SESSION_SLOT.sav`, 30/07) estão em
  `C:\Users\Pichau\AppData\Local\Abyssus\Saved\SaveGames` — que é o caminho usado por `detect-env.sh`.
  Doc e implementação se contradizem; qualquer isolamento de saves guiado pelo doc apontaria para pasta
  inexistente e falharia em silêncio (`cp -r` de origem inexistente → "NENHUM SAVE PARA ISOLAR").

## C9 — Reuso de infraestrutura: ACHADO

Caminhos reais existem: `scratch/cap1/rotina-cap1.sh`, `tools/automacao/runtime/coletor.py`,
`tools/automacao/runtime/roda_testes_runtime.py`, `tools/checa_shrines.py` (todos OK); `tools/automacao/cic-1.sh` NÃO existe.
O runner `run-isolation-tests.sh` procura em `$KITS_DIR/../tools/...` = `scratch/tools/...` (inexistente) → Teste 6
mede caminhos errados e por isso marca skip. Não há reuso efetivo: `grep -n "roda_testes_runtime\|controle_negativo\|pytest\|unittest" scratch/kit/*.sh` → **nenhuma ocorrência**.
KIT-03 escreveu um runner paralelo ao harness já entregue (`tools/automacao/runtime/roda_testes_runtime.py`,
exit 0/1/2, e `controle_negativo.py`), sem aproveitá-lo — apesar de o cartão exigir reuso e não duplicação.

## C10 — Build isolado `-p:DeployToBepInEx=false`: NAO_EXERCITADO + ACHADO

`grep -rn DeployToBepInEx scratch/kit/ docs/automacao/KIT-03-entrega.md` só encontra as duas menções em
prosa no entregável (linhas 29 e 114). Nenhum script executa build nem implementa o **pre-flight de
deploy** que o cartão manda bloquear; `scratch/kit/build/` é um par de diretórios vazios (stub).
Não houve build isolado nem gate — apenas política escrita.

## C7 — Resíduos de instalação / perfil do dono: OK (nenhum resíduo atribuível a KIT-03)

- `find <perfil>/plugins -iname '*test*' -o -iname '*kit*' -o -iname '*backup*'` → vazio.
- Itens do perfil com mtime recente: `plugins/CapProbe/CapProbe.dll` (08/10 22:58),
  `plugins/RoguelikeClassesMod/RoguelikeClassesMod.dll` (09/10 00:55), `LogOutput.log` (09/10 01:13) —
  pertencem a CAP-1/outras frentes runtime, não à janela offline do KIT-03.
- Os únicos artefatos do KIT-03 são stubs/binários de teste sob `scratch/kit/` (ignorado pelo git:
  `.gitignore:49 scratch/`) e o entregável untracked `docs/automacao/KIT-03-entrega.md`.
  Nenhuma DLL de plugin foi instalada no perfil pelo KIT-03.

## C11 — Escopo: OK

Nada foi publicado, instalado, buildado com deploy, nem o jogo foi aberto por esta revisão; nenhum
arquivo de produto/`Assembly-CSharp.dll` foi tocado. Trabalho desta revisão: somente leitura no produto
e escrita sob `docs/automacao/KIT-03R-parte*.md` e `scratch/kit-revisao/`.
