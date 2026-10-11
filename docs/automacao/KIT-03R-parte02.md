# KIT-03R — parte 02: execução no sandbox (runner, snapshot, isolamento)

Sandbox: `scratch/kit-revisao/sandbox/` (cópia de `scratch/kit`, `scratch/cap1`, `docs/automacao/AUT-5/6/7`).
Bash desta sessão: GNU bash 5.2.37 (msys). Nenhum arquivo do produto modificado.

## C8 — Runner `run-isolation-tests.sh`: FALHOU (não roda nenhum teste)

Comando (raiz do sandbox): `KITS_DIR=kit bash kit/run-isolation-tests.sh`
Saída real (exit code do processo = **1**):
```
========================================
  KIT-03: TESTES DE ISOLAMENTO
  Timestamp: 20261009_122117
========================================
EXIT_REAL=1
```
Trace `bash -x` mostra que a execução para exatamente aqui:
```
+ echo ''
+ (( TOTAL++ ))
```
Confirmação de causa: `set -euo pipefail` (linha 4) + `((TOTAL++))` (linha 59) com `TOTAL=0` →
o valor devolvido pelo pós-incremento é 0, status de saída 1, o shell executa `exit` por `set -e`.
Efeito colateral verificado: `kit/results/` vazio (nenhum `results-*.json`) e `kit/logs/` vazio
(nenhum `test001-*.log`); o relatório "TODOS OS TESTES DE ISOLAMENTO PASSARAM" do entregável
**não é reprodutível** — o runner morre antes do Teste 1.

Achado A5 confirmado no código: no Teste 6 o ramo "Alguns componentes faltam" chama `skip()` mas
incrementa `PASSED`; e o exit final é 0 quando `FAILED==0`, logo *etapa pulada vira verde*.
Achado A4 confirmado: `$KITS_DIR/../tools/...` = `scratch/tools/...` (inexistente) contra o real
`tools/...`; `$KITS_DIR/../cap1/...` = `scratch/cap1/...` (existe) — o Teste 6 nunca passa de 3/6.

## C3 — Snapshot/rollback: OK PARCIAL + ACHADOS

Comando real (raiz do sandbox, `BACKUP_DIR`/`ARQUIVOS_CRIADOS` isolados):
```
BACKUP_DIR=kit/backups-rev ARQUIVOS_CRIADOS=kit/arq-criados-test.txt \
  bash kit/snapshot.sh snapshot t3      → EXIT=0, "Snapshot criado: kit/backups-rev/20261009_122132"
... altera t3/plugins/test.dll, cria t3/plugins/new.dll, lista new.dll em arquivos-criados ...
BACKUP_DIR=kit/backups-rev ARQUIVOS_CRIADOS=kit/arq-criados-test.txt \
  bash kit/snapshot.sh rollback t3 20261009_122132  → EXIT=0
  test.dll agora: test-plugin-v1.dll   (restaurou: OK)
  new.dll existe? NAO                  (removeu o listado: OK)
```
Controle negativo (arquivo criado NÃO listado em `arquivos-criados.txt`):
```
echo NEW2 > t3/plugins/new2.dll ; rollback → EXIT=0 ; new2.dll persiste? SIM
```
→ **ACHADO A11 (rollback "exato" não é exato)**: o rollback só apaga o que estiver na lista
**global** `scratch/kit/arquivos-criados.txt` (um único arquivo para todos os testes, mantido à mão).
Arquivo novo não listado sobrevive e o script **não reporta** a sobra; `hashes-antes.txt` é gravado
mas **nunca conferido**, então o critério "rollback exato / mesmo em falha parcial" fica sem prova.

## C4 — Prova de isolamento: ACHADO (tautologia + falso-verde) — A2 confirmado

Positivo: `bash kit/isolacao.sh prove-isolation` → EXIT=0, imprime "PASSOU: Save descartavel esta
ISOLADO fora de .../Abyssus/Saved/SaveGames" e a conclusão fixa.
Controle negativo (fiz o save descartável CAIR DENTRO do suposto SAVES_DIR):
```
SAVES_DIR=kit/isolated-rev bash kit/isolacao.sh prove-isolation → EXIT=0
  FALHOU: Save descartavel esta DENTRO de kit/isolated-rev
  3. Isolamento: SAVE DISCARDABLE ESTA FORA DOS SAVES PRINCIPAIS     <-- impresso MESMO com FALHOU
  5. Conclusao: NAO PODE PRESUMIR que r2modman isola saves           <-- idem
  Sao diretorios diferentes: NAO
```
Prova de que a "comprovação" é falso-verde: (a) a linha comparada é `test_save_dir` vs `SAVES_DIR`
onde `test_save_dir` é criado sob `ISOLATED_SAves_DIR` — verdadeiro por construção; (b) a conclusão
"ESTA FORA DOS SAVES PRINCIPAIS" é **string fixa** (linha 212), independente do resultado;
(c) o script **nunca sai com código diferente de 0**, nem no ramo FALHOU. Todos os greps do runner
(`CONCLUSAO DO TESTE DE ISOLAMENTO`, `SAVE DISCARDABLE...`, `NAO PODE PRESUMIR`) passariam sempre.

## Caminhos fixos/pessoais (C6) — achados adicionais em execução

- A12: `snapshot.sh`/`isolacao.sh`/`front-unica.sh`/`detect-env.sh` **ignoram `KITS_DIR`**: gravam em
  `scratch/kit/backups`, `scratch/kit/logs`, `scratch/kit/isolated-saves`, `scratch/kit/pid.txt`,
  `scratch/kit/detect-env-result.json` relativos ao cwd. Com `KITS_DIR` diferente (como o próprio
  runner usa no Teste 3: `ls "$KITS_DIR/backups"`), o snapshot vai para outro lugar que o runner lê →
  rollback/falha. Os scripts só funcionam se o cwd for a raiz do repo *e* os defaults não forem trocados.
- A3 confirmado em execução: `SAVES_DIR` default = `...\AppData\Local/Abyssus/Saved/SaveGames`
  (placeholder de outro produto; o entregável declara `%LOCALAPPDATA%Low\Burst2Flame ...`).
- `detect-env.sh` linha 12: `PLAYER_LOG="$LOCALAPPDATA/Low/..."` → o correto é `LocalLow`
  (a variável já termina em `\AppData\Local`); caminho errado.
- `isolacao.sh` linha 187: fallback **hardcoded** `C:/Users/Pichau/AppData/Roaming/...` (usuário fixo).
- `detect-env.sh` linha 147: o fallback de CIC está em cadeia morta (`... && PASS=.. || FAIL=.. || check ...`):
  o `|| check` só rodaria se a atribuição `FAIL=$((FAIL+1))` retornasse não-zero, o que nunca ocorre.

## Próximo bloco

Exercitar `front-unica.sh` (controle de concorrência com defeito plantado), `detect-env.sh` no sandbox
e checar resíduos de instalação/perfil do dono (C5, C7, C2). Depois fechar o parecer.
