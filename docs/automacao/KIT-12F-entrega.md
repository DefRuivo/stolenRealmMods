# KIT-12F — entrega da correcao F1/F2 da revisao independente run668

Cartao: `t_0a434c97` (KIT-12 "Integrar alteracao, evidencia, correcao e revalidacao")
Frente: correcao dos achados da revisao run668 (lente Artifact + execucao propria), rodada 1.
Autor desta correcao: instancia implementadora worker **run669** (independente do revisor run668).
Natureza: **OFFLINE**. Nada de jogo, build, deploy, instalacao, publicacao ou perfil do dono.

## 1. Veredito por achado

| Achado | Situacao | Como foi corrigido | Prova |
|---|---|---|---|
| **F1 (bloqueante)** procedencia declarada nao confrontada; hash declarado pelo criterio sobrescrito | **CORRIGIDO** | `confrontar_coleta` + `confrontar_cadeia_declarada` + lacunas nomeadas + rebaixamento (fail-closed) | suite 24 OK; S2 e S8 do revisor reexecutadas; CLI etapa 3b |
| **F2 (acionavel)** campo executavel sobrevive no CRITERIO | **CORRIGIDO** | `montar_fila` passa a `pop`ar o campo do criterio, marcando `criterio_sanitizado` | sondas S1 do revisor: `campos_residuais_no_criterio: []`; 2 testes novos |
| F3 (divida) REPROVADO com classe/procedencia incoerente vira lacuna | **DIVIDA mantida** (fail-closed, original preservado em `declaracoes_incoerentes`) | nao alterado nesta rodada | sonda S5 do revisor inalterada |
| F4 (divida) `--verificar` sem `--config` = exit 3 mesmo sem mudanca real | **DIVIDA mantida** (fail-closed; falso INVALIDADO operacional) | nao alterado nesta rodada | sonda S3 do revisor inalterada |

Nenhum comportamento fora dos dois achados foi alterado; nenhuma trava foi enfraquecida.

## 2. O que mudou (produto `tools/automacao/kit12/integracao.py`)

F1 — PROCEDENCIA CONFRONTADA, sem sobrescrita silenciosa:
- `confrontar_coleta(coleta_meta, ident)` (l.493): `coleta_meta["hash_fonte"]` contra
  `ident["fonte_sha"]` da rodada. Divergencia -> `tipo="contraditoria"`; ausencia de `hash_fonte`
  -> `tipo="ausente"`; identidade sem `fonte_sha` -> nao ha o que confrontar (a identidade
  insuficiente ja derruba o OK e e declarada).
- `confrontar_cadeia_declarada(criterios, ident)` (l.514): percorre `CAMPOS_CADEIA`
  (`fonte_sha`, `dll_sha`, `config_sha`, `versao`, `sessao`) e registra todo campo que o CRITERIO
  declara diferente da identidade; o valor declarado fica preservado no criterio
  (`declaracoes_contraditorias`) e o criterio e marcado com `declaracao_sobrescrita=True`.
- Em `criterios_da_cadeia`, bloco `(2c)` (l.656), ANTES de `anexar_cadeia`: cada achado vira
  LACUNA nomeada (`cadeia/coleta-contraditoria/hash_fonte`, `cadeia/coleta-ausente/hash_fonte`,
  `cadeia/declaracao-contraditoria/<id>/<campo>`) e o OK correspondente cai - `rebaixar_ok`
  (rodada inteira, contradicao da coleta) ou novo `rebaixar_criterio` (l.469, criterio especifico).
- `criterio["coleta"]["hash_fonte_confronto"]` passa a declarar `confere` / `contraditoria` /
  `ausente` / `sem-identidade`, para a evidencia dizer o que foi confrontado.

F2 — SANITIZACAO DO CRITERIO (`montar_fila`, l.715-745):
- na passada de origem `criterio`, o campo executavel e REMOVIDO do criterio (`fonte.pop(campo)`),
  o criterio recebe `criterio_sanitizado=True` e o registro continua em
  `propostas_nao_executadas` com `origem="criterio"` (nada e executado; nao existe caminho de
  execucao no modulo).

Documentacao do modulo atualizada (itens 3 e 4 do cabecalho). Testes: 6 novos casos.
`prove_ciclo.py` ganhou a etapa 3b (coleta declarando bytes de outra rodada) e passou a ser
**repetivel** sem apagar evidencia (resultados anteriores vao para `<out>/anterior/`).

## 3. Provas reais (exit e caminhos; nada por mensagem)

    python tools/automacao/kit12/test_kit12_integracao.py      -> Ran 24 tests OK        exit 0
       log scratch/kit/KIT-12F-run669-suite.txt
    python tools/automacao/kit12/test_kit12_integracao.py --isca -> 9/9 discriminadas, controle restaurado exit 0
       log scratch/kit/KIT-12F-run669-isca.txt
    python tools/automacao/kit12/prove_ciclo.py --out scratch/kit/KIT-12F-run669
       1 fixture-marcada exit=2 INCOMPLETO | 2 defeito-plantado exit=1 REPROVADO |
       3 correcao-controlada exit=2 INCOMPLETO | 3b coleta-hash-de-outros-bytes exit=2 INCOMPLETO |
       4 verificar-apos-mudanca-de-config exit=3 INVALIDADO  -> PROVA|PASSOU  exit 0
       prova.json scratch/kit/KIT-12F-run669/prova.json (2a execucao no mesmo --out: PASSOU tambem)
    Sondas do PROPRIO revisor reexecutadas contra o produto corrigido
       scratch/kit/KIT-12F-run669-rev/sondas-saida.txt  -> SONDAS_OK|8
       scratch/kit/KIT-12F-run669-rev/sonda-s8-saida.txt -> costura: NAO_EXERCITADO, exit 2,
         lacunas cadeia/declaracao-contraditoria/... (antes APROVADO_OFFLINE/exit 0)
    Travas: check_segredos, check_padroes_segredo, check_dupes, audita_docs -> exit 0 cada

Varredura dos 4 resultados JSON da CLI: `campos_executaveis_em_criterios = []` em todos.

## 4. Hashes (sha256)

    tools/automacao/kit12/integracao.py            ae61678c7b5cca65295693ef2f0611865dca651ed7b39a352407d58236a0d13b
    tools/automacao/kit12/test_kit12_integracao.py 78f09d5b1a5bfda8324e8ae4cebe711aa4a61de209fffdfb1e082ec8723cec4f
    tools/automacao/kit12/prove_ciclo.py           494c70b66714ae58ebba99784e430fb6ab794664f3841e0f5802de29f8a69897
    tools/automacao/kit12/pertinencia.json         b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320  (INALTERADO)
    (entrega anterior, run667, integracao.py: f49a0d4059af33002ce52b463ad6be7091063ee6d661d746498072545c1a3599)

HEAD do repo inalterado (d82894e); nenhum `git add/commit/push`.

## 5. Limites e lacunas (deliberadamente NAO maquiadas)

- NAO_EXERCITADO: jogo/probe/save/perfil real, runtime AUT-4, UI/UX/pixels, build C#,
  pre-flight de deploy, instalacao, publicacao, aceite humano e DoD. Fixture marcada NAO e prova
  de runtime (`com_prova_runtime=0` em todos os passos).
- Dividas F3 e F4 permanecem (nao bloqueiam; ambas do lado fail-closed).
- Achados de terceiros (nao deste cartao, registrados sem correcao):
  `kit10_cenarios._criterio(obs=None)` levanta `AttributeError` no caminho de oraculo indisponivel;
  AUT-7 emite `classe=runtime` com `procedencia=execucao` (falso vermelho) - a costura normaliza em
  lacuna nomeada preservando o original.
- A coluna `criterios_que_apontam_contradicao` das sondas do revisor aparece com o mesmo id duas
  vezes porque a sonda soma `criterios` + `falhas_automaticas`; nao ha criterio duplicado.

## 6. Pedido ao revisor (rodada 2)

Tentar refutar, medindo efeito e nao mensagem:
1. coleta declarando `hash_fonte` de OUTROS bytes (ou SEM `hash_fonte`) ainda virando OK/aprovacao;
2. criterio declarando `fonte_sha`/`dll_sha` de bytes antigos escapando do rebaixamento;
3. campo executavel (`comando`/`argv`/`script_correcao`) sobrevivendo no `resultado["criterios"]`;
4. a correcao tendo virado trava cega (OK offline legitimo tem de continuar sobrevivendo quando a
   coleta declara o hash DA RODADA);
5. a suite/isca sendo carimbo (cada mutacao nova tem de derrubar o teste-alvo).
Veredito por criterio no cartao; alteracao de produto no mesmo cartao, se houver.
