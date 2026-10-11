# KIT-12F2 — entrega da correcao dos achados F1R–F5R (KIT-12R)

Cartao: `t_51ca208a`. Pai: `t_811b1717` (KIT-12R, REPROVADO run674).
Autor: **instancia implementadora default/run675** (`!=` revisor run674).
Natureza: **OFFLINE** — nada de jogo, build, deploy, instalacao, publicacao, perfil do dono, Bard,
`Assembly-CSharp.dll` ou gameplay. Sem `git add/commit/push`. Nenhum mod/dado/politica alterado.

Nome "KIT-12F2": `KIT-12F-*` ja existe (rodada run669, cartao `t_0a434c97`) e nao foi sobrescrito,
conforme "nao sobrescrever existentes / nome final novo".

## 1. Veredito por achado (medido, nao por mensagem)

| Achado | Situacao | Prova (arquivo:exit) |
|---|---|---|
| **F1R** config requerida ausente aprova | **CORRIGIDO** | oraculo `test_missing_required_config_never_green` 17OK; sondas `F1R.*` (6/6); `oracle-fix.txt` exit0 |
| **F2R** relatorio indisponivel aprova | **CORRIGIDO** | oraculo `test_report_dependency_missing/throw_never_green`; `oracle-fix.txt` exit0 |
| **F3R** probe solicitado ilegivel cai em fallback | **CORRIGIDO** | oraculo `test_requested_probe_missing_not_silently_green`; sondas `F3R.*` (5/5) |
| **F4R** coleta malformada aborta a CLI | **CORRIGIDO** | oraculo `test_malformed_observations_integer_closed`; sondas `F4R.*` (12/12) |
| **F5R** saneamento nao alcanca OK | **CORRIGIDO** | oraculo `test_commands_sanitized_all_states`; sondas `F5R.*` (15/15) |

Nenhuma trava foi enfraquecida; nenhuma prova faltante foi marcada verde.

## 2. Alvo, hashes e exits

    tools/automacao/kit12/integracao.py           480a9a02b7a2f13bb51d4bce32c29897ff944cfca00fd6431a924877a44da25c
      (baseline revisado run674)                  7785d8c1f624ff263b4ac89ad36e3ab9952db17d5a233d12affada091da8af87
    tools/automacao/kit12/test_kit12_integracao.py 25284c7075633042efc6445a5856d5a24e40d152ccdb593d6cb94d661e96da8c (INALTERADO)
    tools/automacao/kit12/prove_ciclo.py           4fc01b81572bdfbbea4cc3af33f1fb845659f23bc689cc94068e2d85b973b750 (INALTERADO)
    tools/automacao/kit12/pertinencia.json         b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320 (INALTERADO)
    oraculo do revisor (IMUTAVEL)                  cf5966527ac0276fbe827aeab0def2c7825deb5bc4fd27744d216d854c83f2c6 (INALTERADO)
    docs/automacao/KIT-12F2-parte01.md             5cb775bdcd4a51f546ce5ba2e82dc8deab1f66f93a67d8b40a3f6a3b441db235
    docs/automacao/KIT-12F2-parte02.md             be4fe1798f8904abc80735473cd0c7e9b38bfd5b8d6f104bfbf15506b452385b
    docs/automacao/KIT-12F2-parte03.md             843d10ae6f7b9fcbc2fef16684cf46ccd21726bbea9812bd8f5392edc655a2d2
    scratch/.../probes_kit12f2.py                  abcc8665d5afd8d8297d0a8342aff178e22b62a4bcc4dc938122d12280939e1d

Pacote de evidencias: `scratch/kit/KIT-12F2-run675-evidencias.zip`
`eb43bfca0e08b4ac52f5f8b9a00ba60736c12a9666c4590976e24f7ad0c92608` (contem
`rev674/sandbox/.../integracao.py` == `480a9a...` e `baseline-oracle/sandbox/.../integracao.py`
== `7785d8...`).

Execucoes (exit entre parenteses):

    oraculo revisor BASELINE  : Ran 17 - 11 OK / 6 FAIL, ERROR0/skip0   (1)  oracle-baseline.txt
    oraculo revisor CORRIGIDO : Ran 17 - 17 OK,           ERROR0/skip0   (0)  oracle-fix.txt
    suite autor               : Ran 30 OK                               (0)  suite.txt
    isca autor                : 14/14 discriminadas, controle restaurado (0)  isca.txt
    CLI real prove_ciclo      : PROVA|PASSOU, etapas 2->1->2->2->2->2->3  (0)  cli.txt / cli2/prova.json
    controles do revisor      : 11 mutacoes identicas ao baseline        (1*) rev674/own-mutants.json
       (*) o script sai 1 de proposito porque a 1a mutacao fixture e redundante (0->0->0), ja
           documentada em KIT-12R e preservada — NAO e regressao.
    sondas IRMAS              : 38/38 OK                                (0)  probes.txt / probes-resultado.json
    travas check_segredos/check_padroes_segredo/check_dupes/audita_docs (0) cada  gate-*.txt

## 3. Reproducao do alvo

`baseline-oracle/` roda o MESMO oraculo contra o produto `7785d8...` (extraido do ZIP de
evidencias do revisor) -> 6 FAIL; `rev674/` roda contra o produto `480a9a...` -> 17 OK. O ZIP
`scratch/kit/KIT-12R-run674-evidencias.zip` prova que o baseline usado e o bytes do revisor. O
oraculo `test_review_kit12.py` nao foi editado. A sandbox do revisor foi **restaurada** ao baseline
apos a medicao; os controles do revisor rodaram numa copia (`rev674/`).

## 4. Escopo do que mudou

Somente `tools/automacao/kit12/integracao.py` (5 blocos: `_validar_observacoes`; lacunas
config/instrumento em `criterios_da_cadeia`; saneamento global + `propostas_do_resultado` em
`montar_fila`; relatorio-antes-da-classificacao em `cadeia`; docstring item 6). Detalhe na parte 02.

## 5. Pedido ao revisor (instancia independente, != run675)

Tentar refutar, item a item, medindo EFEITO (nao relendo este texto):

1. **F1R**: alguma combinacao de configs (solicitada ausente, multiplas com falta parcial) ainda
   produz OK/exit0? Config nao fornecida continua opcional (nao virou trava)?
2. **F2R**: injetar ausencia e OSError do modulo de relatorio — ainda existem caminhos de
   APROVADO_OFFLINE sem relatorio? O motivo e preservado sem texto inventado?
3. **F3R**: `--probe-dll` ilegivel/ausente cai em `dll_sha` em algum caminho? O instrumento apenas
   DECLARADO (sem `--probe-dll`) segue permitido? Medido coerente positivo sobrevive?
4. **F4R**: outros tipos/formas de `observacoes` (nulo/objeto/string/lista com lixo/ausente) ainda
   abortam a CLI ou viram zero verde? Formatos legitimamente aceitos foram quebrados?
5. **F5R**: algum dos QUATRO estados ainda transporta campo executavel em `criterios`? A auditoria
   da proposta foi apagada(nao — fica em `propostas_nao_executadas`)? Algum comando proposto foi
   executado?
6. **Nao-regressao**: o positivo OFFLINE legitimo, a suite autor, as 14 iscas, a CLI e as travas
   continuam valendo; o oraculo nao foi afrouxado; F3/F4 historicos seguem divida separada.

Alteracao de produto, se houver, no MESMO cartao. Aprovacao tecnica NAO e aceite humano nem DoD.
