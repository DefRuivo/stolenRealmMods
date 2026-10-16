# KIT-05F — parte 02: correções F1–F7 provadas por execução

Run 631 (implementer, perfil `default`, instância ≠ autor 629 e ≠ reviewer 630).
Tudo offline: sem jogo, sem save, sem deploy, sem publicação. Fontes originais
preservadas em `scratch/kit/KIT-05F/backup/`.

## F1–F6 — `tools/automacao/runtime/observacao_passiva.py` (reescrito)

| Achado | O que mudou no fonte | Prova |
|---|---|---|
| F1 | `registrar_captura` virou **PEDIDO** (`estado="solicitada"`, nunca marca `captura_apos_atualizacao_visual`); nova `confirmar_captura` exige evento existente, sessão/evento coincidentes, **arquivo PNG real em disco**, quadro **estritamente posterior** ao evento e hash SHA256 do arquivo. | `test_pedido_nao_confirma_captura`, `test_confirmacao_exige_png_real`, `test_confirmacao_exige_quadro_posterior`, `test_pedido_com_quadro_anterior_e_recusado`, `test_confirmacao_exige_sessao_e_evento_coerentes`, `test_confirmacao_com_png_e_quadro_posterior_confirma` |
| F2 | `pausar` bloqueia `registrar`, `registrar_captura`, `confirmar_captura` **e** `verificar_timeouts`; pendências do intervalo não observado são invalidadas com **lacuna explícita** (`observacao_interrompida`, `lacunas`) e não viram falha ao retomar. | `test_pausa_bloqueia_pedido_e_confirmacao_de_captura`, `test_pausa_invalida_pendencia_nao_observada` |
| F3 | Estado lembrado **por fonte** (janela/contexto) com assinatura `(tipo, janela, dados)`; cliques seguem discretos. | `test_janelas_distintas_com_dados_iguais_coexistem`, `test_intercalacao_constante_nao_gera_spam`, `test_abrir_fechar_reabrir_sobrevive` |
| F4 | `limite_aux` explícito para degradações, rejeitados, pendentes, memória de dedup, pedidos, capturas e lacunas; contadores agregados (`*_total`, `*_descartados`, `*_por_motivo`); evicção/expiração limpam referências órfãs. | `test_todo_estado_auxiliar_e_limitado_sob_milhares` (3000 entradas), `test_limite_aux_explicito_pode_ser_maior_finito` |
| F5 | `_processa_abertura` materializa vencimentos **antes** da abertura; `_resolve_janela` só resolve `agora <= prazo`; abertura tardia registra `janela_tardia_sem_resolucao`. | `test_fronteira_exata_gera_uma_falha_e_nao_duplica`, `test_janela_tardia_nao_apaga_vencimento`, `test_janela_de_outra_identidade_nao_resolve` |
| F6 | `_correr_entradas` devolve o **estado retido** (sem lista paralela); CLI exporta `eventos_retidos`/`falhas_retidas` coerentes com `eventos_total` e rotula `origem=fixture-offline`, `runtime=NAO_EXERCITADO`, `runtime_exercitado=false`. | `test_replay_respeita_retencao_no_payload_final`, `test_replay_nao_guarda_lista_paralela_de_falhas`, `test_cli_rotula_fixture_offline_e_nao_promove_runtime` |

Execuções reais:

```
$ python tools/automacao/kit05/teste_observacao_passiva.py          # no repo e em sandbox
Ran 37 tests in 0.054s
OK                                                                  EXIT=0

$ python test_revisao_kit05.py      # suite INDEPENDENTE do reviewer KIT-05R (run630)
Ran 16 tests in 0.026s
OK                                                                  EXIT=0
```

Antes da correção essa mesma suite independente dava `16 testes, 10 FAIL, 6 OK,
exit 1` (parecer KIT-05R). Ela foi reexecutada **contra o novo módulo**, sem
alterar o script do reviewer (`scratch/kit/KIT-05R-run630/test_revisao_kit05.py`),
em `scratch/kit/KIT-05F/sandbox-nova/`.

## F9 — `tools/automacao/kit05/contra_prova_kit05.py` (duração + discriminador estrito)

* Discriminador exige: `exit == 1`, `FAIL:` **do alvo**, conjunto **exato** de
  testes que falharam, `AssertionError` presente, **ausência** de `ERROR:`, de
  skip e de execução vazia; timeout/erro de execução é recusado.
* `CONTROLE_falso_verde`: defeito plantado derruba **outro** teste e o alvo
  declarado (`test_ids_unicos`) **passa**. O discriminador estrito **RECUSA** e o
  oráculo antigo (exit != 0 + nome no output verbose) **aceitaria** — as duas
  informações saem no mesmo log, provando o falso verde do F9 e sua correção.
* `--individual`: os **37** testes da suite são mostrados reprovando
  individualmente (cada um rodando sozinho contra a mutação declarada em
  `TABELA_REPROVACAO`, descoberta empiricamente por `--descobrir`).

```
$ python tools/automacao/kit05/contra_prova_kit05.py
[A..R + CONTROLE_falso_verde] VEREDITO REGRAS: VERDE (todas as iscas reprovaram;
controle falso-verde recusado)                                          EXIT=0

$ python tools/automacao/kit05/contra_prova_kit05.py --individual
VEREDITO TESTES: VERDE (37 teste(s) reprovando individualmente)         EXIT=0
```

O script antigo (`scratch/kit/KIT-05/contra_prova.py`) permanece intacto como
histórico; suas 7 iscas legítimas foram re-verificadas pelo reviewer e continuam
reprovando — a correção é do **oráculo**, não das iscas.

## F7 — `tools/automacao/kit05/roda_testes_kit05.sh`

* Raiz resolvida pelo **layout** (`$AQUI/../../..`), sem `git rev-parse`, com
  caminho nativo para o python (`pwd -W`); `PYTHON` configurável; `exit 2` para
  layout/interpretador ausente; nenhuma etapa ausente vira verde.
* Contra-prova durável passa a viver em `tools/automacao/kit05/` (nada de
  `scratch/` descartável).

```
$ bash tools/automacao/kit05/roda_testes_kit05.sh    # no repo
VEREDITO KIT-05F: VERDE (exit 0)                                        EXIT=0

# sandbox FORA do repo, SEM .git em nenhum ancestral
$ cd $HOME/AppData/Local/hermes/cache/scratch/kit/KIT-05F-sandbox
$ bash tools/automacao/kit05/roda_testes_kit05.sh
VEREDITO KIT-05F: VERDE (exit 0)                                        EXIT=0

$ bash tools/automacao/kit05/roda_testes_kit05-ANTIGO.sh   # runner pré-correção
fatal: not a git repository (or any of the parent directories): .git    EXIT=2

$ PYTHON=/nao/existe/python bash tools/automacao/kit05/roda_testes_kit05.sh
ERRO KIT-05F: interpretador '/nao/existe/python' nao encontrado          EXIT=2
```

Logs: `scratch/kit/KIT-05F/runner-kit05f-green.log`,
`runner-sandbox.log`, `runner-sandbox-antigo.log`.

## Limites declarados

* Runtime/desempenho em jogo continuam **NAO_EXERCITADO** (nenhuma sessão viva).
* O `--descobrir` do F9 é auxiliar de bancada; a tabela embutida é resultado
  medido, não hipótese.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
