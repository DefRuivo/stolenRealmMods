# KIT-12 — Revisao independente (run668) — parte 02

## 4. Execucao propria na entrega viva (bytes do implementador)

Ambiente: repo C:/dev/stolen-realm, HEAD d82894e, `BH_AGENT_WORKSPACE` nao definido (sandbox vai para %LOCALAPPDATA%\hermes\cache\scratch, fora do repo). Nenhum arquivo de produto editado por mim.

### 4.1 Suite do autor (`python tools/automacao/kit12/test_kit12_integracao.py`)

    Ran 18 tests in 10.082s
    OK
    exit=0

Log: scratch/kit/KIT-12R-run668-rev/suite-entrega.txt (18 testes, 12 `test_neg_*`, 2 `test_positivo_*`, 3 idempotencia/determinismo, 1 mapeamento).

### 4.2 Isca (`--isca`) — mutacao seletiva real no fonte

    ISCA|fixture_pode_aprovar|test_neg_identidade_insuficiente|exit=1
    ISCA|fila_executa_campo|test_neg_campo_executavel|exit=1
    ISCA|invalidacao_desligada|test_neg_config_mudou|exit=1
    ISCA|nunca_incompleto|test_neg_correcao_controlada|exit=1
    ISCA|sem_progresso_desligado|test_neg_limite|exit=1
    ISCA|sem_anexar_cadeia|test_positivo_cadeia_completa|exit=1
    ISCA|controle_restaurado|test_positivo|exit=0
    ISCA|mutacoes_discriminadas=6/6|falhas=0
    exit=0

Cada mutante derruba exatamente o teste-regressao nomeado (nao AssertionError artificial: o fonte mutado e um replace textual real). Log: isca-entrega.txt.

### 4.3 CLI integrada em sandbox com fixture marcada + erro -> correcao -> revalidacao

`python tools/automacao/kit12/prove_ciclo.py --out scratch/kit/KIT-12R-run668-rev`

    1-fixture-marcada                    | exit=2 | estado=INCOMPLETO
    2-defeito-plantado                   | exit=1 | estado=REPROVADO
    3-correcao-controlada                | exit=2 | estado=INCOMPLETO
    4-verificar-apos-mudanca-de-config   | exit=3 | estado=None
    PROVA|PASSOU|.../scratch/kit/KIT-12R-run668-rev/prova.json
    exit=0

Confere com o handoff (exits 2->1->2->3) e com o `prova.json` de run667 lido por mim. A fixture MARCADA nunca vira OK (`com_prova_runtime=0` em todos os passos) e o defeito plantado faz o criterio virar REPROVADO com causa/caminho na fila.

## 5. Status

- [x] hashes conferidos (5/5 do handoff + entrega.md)
- [x] leitura fria do produto (952 linhas), do pertinencia.json, do prove_ciclo.py e da suite (489 linhas)
- [x] suite 18/18 OK exit 0 reproduzida por mim
- [x] isca 6/6 mutacoes discriminadas, controle restaurado exit 0
- [x] CLI em sandbox: 2 -> 1 -> 2 -> 3, PROVA PASSOU, sem runtime fingido
- [ ] travas do repo (check_segredos/check_padroes_segredo/check_dupes/audita_docs)
- [ ] sondas adversariais proprias (R1 fila/criterio, R2 normalizacao, R4 verificar sem config, R6 fixture, fonte/DLL)
- [ ] veredito por criterio
