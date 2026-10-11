# KIT-12F — parte 03: provas reais desta rodada (exit e caminhos)

Todos os comandos rodados em `C:/dev/stolen-realm` nesta sessao (worker run669). Nenhum jogo,
build, deploy, instalacao ou publicacao foi tocado. Nenhum `git add/commit/push`.

## 1. Suite de testes (unittest)

    python tools/automacao/kit12/test_kit12_integracao.py
    -> Ran 24 tests ... OK      exit 0
    log: scratch/kit/KIT-12F-run669-suite.txt

6 testes novos (3 negativos de procedencia + 1 contra-prova + 2 de fila/criterio):
`test_neg_coleta_hash_contraditorio_nao_aprova`, `test_neg_coleta_sem_hash_declarado_nao_aprova`,
`test_positivo_coleta_com_hash_conferido_mantem_o_ok`,
`test_neg_criterio_com_hash_de_bytes_antigos_e_rebaixado_e_preservado`,
`test_neg_campo_executavel_nao_sobrevive_no_criterio`,
`test_neg_campo_executavel_do_avaliador_nao_vaza_no_resultado`.

## 2. Isca (mutacoes seletivas: cada guard deve derrubar seu teste)

    python tools/automacao/kit12/test_kit12_integracao.py --isca
    -> ISCA|mutacoes_discriminadas=9/9|falhas=0   exit 0
    log: scratch/kit/KIT-12F-run669-isca.txt
    (9 mutacoes, cada uma exit=1 no teste-alvo; controle restaurado exit=0)

3 mutacoes novas desta correcao: `coleta_contraditoria_ignorada`,
`declaracao_do_criterio_sobrescrita`, `criterio_nao_sanitizado`.

## 3. CLI integrada em SANDBOX externa (fixture marcada; sem fingir runtime)

    python tools/automacao/kit12/prove_ciclo.py --out scratch/kit/KIT-12F-run669
    1-fixture-marcada                | exit=2 | INCOMPLETO
    2-defeito-plantado               | exit=1 | REPROVADO
    3-correcao-controlada            | exit=2 | INCOMPLETO
    3b-coleta-hash-de-outros-bytes   | exit=2 | INCOMPLETO   (NOVO: F1)
    4-verificar-apos-mudanca-de-config | exit=3 | INVALIDADO_POR_MUDANCA
    -> PROVA|PASSOU    exit 0
    prova.json: scratch/kit/KIT-12F-run669/prova.json
Segunda execucao no mesmo `--out`: tambem exit 0 / PASSOU (os resultados anteriores sao movidos
para `anterior/`, nada e apagado) - log: scratch/kit/KIT-12F-run669-prove-rerun.txt.

Varredura dos 4 resultados JSON: `campos_executaveis_em_criterios = []` em todos.

## 4. Sondas ADVERSARIAIS do proprio revisor (run668), reexecutadas contra o produto corrigido

    python scratch/kit/KIT-12F-run669-rev/sondas_run668.py   -> SONDAS_OK|8   exit 0
    python scratch/kit/KIT-12F-run669-rev/sonda_s8_hash_antigo.py -> exit 0
    logs: scratch/kit/KIT-12F-run669-rev/sondas-saida.txt, sonda-s8-saida.txt
(copias em scratch/kit/KIT-12F-run669-rev/, com OUT redirecionado; o diretorio original do
revisor NAO foi sobrescrito)

- S1 (campo executavel no criterio): `campos_residuais_no_criterio: []` -> F2 SANADO.
- S2 hash estaleiro: `estado=INCOMPLETO, exit=2, OK=0`, lacuna `cadeia/coleta-contraditoria/hash_fonte`.
- S2 hash ausente: idem com `cadeia/coleta-ausente/hash_fonte`.
- S8: pela costura o criterio fica `NAO_EXERCITADO`, `exit=2`, com
  `cadeia/declaracao-contraditoria/offline/hash-antigo/fonte_sha|dll_sha` (antes: APROVADO_OFFLINE/exit 0).
- S3/S4/S5/S6/S7 inalteradas (dividas F3/F4 seguem registradas, ver entrega).

## 5. Travas do repositorio

    python tools/check_segredos.py        -> exit 0
    python tools/check_padroes_segredo.py -> exit 0
    python tools/check_dupes.py           -> exit 0
    python tools/audita_docs.py           -> exit 0
    logs: scratch/kit/KIT-12F-run669-check_*.txt, scratch/kit/KIT-12F-run669-audita_docs.txt

## 6. Hashes do produto (sha256)

    integracao.py               ae61678c7b5cca65295693ef2f0611865dca651ed7b39a352407d58236a0d13b
    test_kit12_integracao.py    78f09d5b1a5bfda8324e8ae4cebe711aa4a61de209fffdfb1e082ec8723cec4f
    prove_ciclo.py              494c70b66714ae58ebba99784e430fb6ab794664f3841e0f5802de29f8a69897
    pertinencia.json            b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320 (inalterado)

NAO_EXERCITADO: jogo/probe/save/perfil, runtime AUT-4, UI/UX/pixels, build C#, pre-flight de
deploy, instalacao, publicacao, aceite humano/DoD.
