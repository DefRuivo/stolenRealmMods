# KIT-05 — parte 03: implementação do pipeline e prova de testes

Cartão `t_e9e569f8` · 2026-10-09 · offline.

## Artefatos criados

| Arquivo | Papel |
|---|---|
| `tools/automacao/runtime/observacao_passiva.py` | Pipeline de observação passiva (lógica pura) |
| `tools/automacao/runtime/testes/t_kit05_observacao_passiva.py` | 19 testes offline reais (unittest) |

## Primeiro conjunto de eventos RSTV (implementado)

- `clique_recebido` — clique FOI RECEBIDO pelo jogo (só observação);
- `janela_aberta` — janela de fato abriu;
- `janela_fechada` — janela de fato fechou;
- `tooltip` — tooltip apareceu/restaurado;
- `falha_clique_sem_janela` — DERIVADO: clique recebido sem janela dentro do
  timeout, com `motivo` + `timeout_ms` + `clique_id` de origem.

## Regras implementadas (com teste cada)

| Regra | Método | Teste |
|---|---|---|
| Modo passivo: rejeita tipo ATIVO | `registrar` | `test_rejeita_tipo_ativo` |
| Rejeita tipo desconhecido | `registrar` | `test_rejeita_tipo_desconhecido` |
| Rejeita chave de AÇÃO nos dados | `registrar` | `test_rejeita_dado_ativo` |
| Dedup por MUDANÇA (estado repetido) | `_chave_estado`/`registrar` | `test_estado_repetido_nao_vira_evento` |
| Clique NÃO deduplica (evento discreto) | `registrar` | `test_clique_nao_deduplica` |
| Fila limitada + degradação `fila_cheia` | `_enfileira` | `test_fila_limitada_descarta_e_declara` |
| Retenção por IDADE (explícita) | `expirar` | `test_retencao_por_idade` |
| Retenção por TAMANHO (automática) | `_enfileira` | `test_retencao_por_tamanho` |
| Teto de capturas + degradação | `registrar_captura` | `test_teto_de_capturas` |
| Captura de evento inexistente | `registrar_captura` | `test_captura_evento_inexistente` |
| Pausa segura (descarta + degradação) | `pausar`/`retomar` | `test_pausa_descarta_e_retoma` |
| Falha clique-sem-janela (motivo/timeout) | `verificar_timeouts` | `test_timeout_gera_falha_com_motivo` |
| Janela resolve e NÃO gera falha | `_resolve_janela` | `test_janela_resolve_e_nao_gera_falha` |
| Timeout antes do prazo não gera falha | `verificar_timeouts` | `test_timeout_antes_do_prazo_nao_gera_falha` |
| Correlação captura APÓS atualização visual | `registrar_captura` | `test_captura_apos_atualizacao_visual` |
| NUNCA afirma simultaneidade | `registrar`/`registrar_captura` | `test_nenhum_evento_afirma_simultaneidade` |
| IDs únicos | `registrar` | `test_ids_unicos` |

## Prova de execução real (offline)

```
$ python tools/automacao/runtime/testes/t_kit05_observacao_passiva.py
Ran 19 tests in 0.001s
OK
EXIT=0
```

Primeira execução (antes do ajuste de retenção por tamanho): `Ran 19 tests`,
`FAILED (failures=1)` em `test_retencao_por_tamanho`, `EXIT=1` — o teste
REPROVOU de verdade e dirigiu a correção (`_enfileira` passou a aplicar o teto de
retenção por tamanho). Registrado como prova de teste que falha.

## O que NÃO foi exercitado (declarado)
- Emissão real pelo Core C# em jogo: NÃO_EXERCITADO (sem autorização de runtime).
- Desempenho runtime: só se mede em rodada autorizada — fora do escopo.
