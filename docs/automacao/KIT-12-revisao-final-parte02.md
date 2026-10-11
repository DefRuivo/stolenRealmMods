# KIT-12 revisao rodada 2 (run670) — parte02: conferencia de hashes e execucao propria

Metodo: a copia isolada `scratch/kit/KIT-12R-run670-rev/repo/` (tools/ copiado sem `.git`, `bin`,
`obj`, `__pycache__`) e o `git init` proprio do `prove_ciclo.py` em
`%LOCALAPPDATA%\hermes\cache\scratch\kit12-demo-sandbox`. O produto no repo NAO foi tocado.

## A0 — hashes do handoff x disco

    $ sha256sum tools/automacao/kit12/{integracao.py,test_kit12_integracao.py,prove_ciclo.py,pertinencia.json}
    ae61678c7b5cca65295693ef2f0611865dca651ed7b39a352407d58236a0d13b  integracao.py
    78f09d5b1a5bfda8324e8ae4cebe711aa4a61de209fffdfb1e082ec8723cec4f  test_kit12_integracao.py
    494c70b66714ae58ebba99784e430fb6ab794664f3841e0f5802de29f8a69897  prove_ciclo.py
    b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320  pertinencia.json

**4/4 batem com o handoff run669** (inclusive `integracao.py` = ae61678c… != f49a0d40… da rodada 1).
O `prova.json` reemitido por mim carimba os mesmos 4 hashes + os 2 JSON de coleta.
VEREDITO A0: PASSOU.

## A1 — suite (execucao minha, na copia isolada)

    $ cd scratch/kit/KIT-12R-run670-rev
    $ python repo/tools/automacao/kit12/test_kit12_integracao.py     -> exit 0
    Ran 24 tests in 9.164s
    OK
    Log: scratch/kit/KIT-12R-run670-rev/suite-run670.txt

24 testes, 0 falhas, 0 erros, 0 skip (nao ha linha "skipped"). Os 2 ultimos casos do log sao
justamente os das correcoes: `test_positivo_coleta_com_hash_conferido_mantem_o_ok`
(contra-prova F1) e o caso de cadeia anexada.
VEREDITO A1: PASSOU.

## A2 — isca (mutacao seletiva), execucao minha

    $ python repo/tools/automacao/kit12/test_kit12_integracao.py --isca      -> exit 0
    ISCA|fixture_pode_aprovar|test_neg_identidade_insuficiente|exit=1
    ISCA|fila_executa_campo|test_neg_campo_executavel|exit=1
    ISCA|invalidacao_desligada|test_neg_config_mudou|exit=1
    ISCA|nunca_incompleto|test_neg_correcao_controlada|exit=1
    ISCA|sem_progresso_desligado|test_neg_limite|exit=1
    ISCA|sem_anexar_cadeia|test_positivo_cadeia_completa|exit=1
    ISCA|coleta_contraditoria_ignorada|test_neg_coleta_hash_contraditorio|exit=1
    ISCA|declaracao_do_criterio_sobrescrita|test_neg_criterio_com_hash_de_bytes_antigos|exit=1
    ISCA|criterio_nao_sanitizado|test_neg_campo_executavel_nao_sobrevive|exit=1
    ISCA|controle_restaurado|test_positivo|exit=0
    ISCA|mutacoes_discriminadas=9/9|falhas=0
    Log: scratch/kit/KIT-12R-run670-rev/isca-run670.txt

As 3 mutacoes novas das correcoes derrubam exatamente o teste-alvo (exit 1 = teste falhou sob
mutacao, isto e, a mutacao foi DETECTADA), e o controle restaurado volta a exit 0 — a isca nao e
carimbo: ela separa o teste que pega cada defeito. NAO ha "skipped": cada mutacao produziu veredito.
VEREDITO A2: PASSOU.

## A3 — CLI integrada em sandbox (execucao minha)

    $ python repo/tools/automacao/kit12/prove_ciclo.py --out .../cli-run670   -> exit 0
    1-fixture-marcada                 | exit=2 | INCOMPLETO
    2-defeito-plantado                | exit=1 | REPROVADO
    3-correcao-controlada             | exit=2 | INCOMPLETO
    3b-coleta-hash-de-outros-bytes    | exit=2 | INCOMPLETO
    4-verificar-apos-mudanca-de-config| exit=3 | (INVALIDADO)
    PROVA|PASSOU|.../cli-run670/prova.json

`prova.json`: `veredito=PASSOU`, `problemas=[]`, `sandbox_tem_git=true`, sandbox em
`%LOCALAPPDATA%\hermes\cache\scratch\kit12-demo-sandbox` (fora do repo, sem remoto/perfil).
Etapa 3b le a lacuna `cadeia/coleta-contraditoria/hash_fonte` com a coleta declarando `0*64`
contra `fonte_sha=25a4517d842ef518…` da rodada: `OK=0`, `com_prova_runtime=0`, exit 2.
O defeito plantado produz a fila com roteamento `causa` e caminho real; a correcao controlada
derruba REPROVADO e NAO promove o criterio a OK (`REPROVADO=0`, `OK=0`).
VEREDITO A3: PASSOU.

Falha de percurso registrada (nao do produto): na 1a execucao passei `--out "$PWD/..."` (caminho
MSYS `/c/...`), que o python nativo resolveu como `C:\c\dev\...`; os artefatos foram para
`C:\c\dev\stolen-realm\scratch\kit\KIT-12R-run670-rev\cli-run670\` (existe). Reexecutei com caminho
nativo `C:/dev/...` e o log acima e o desta segunda execucao.
