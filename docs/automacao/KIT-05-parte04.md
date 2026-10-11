# KIT-05 — parte 04: integração, CLI end-to-end e contra-prova

Cartão `t_e9e569f8` · 2026-10-09 · offline.

## Decisão de integração (importante)

O teste do KIT-05 **não** foi colocado em `tools/automacao/runtime/testes/`:
aquela pasta tem **inventário travado** pelo front AUT-4 — `t_aut4_estado_docs.py`
(A7) compara a lista de testes declarada em `AUT-4-estado.json` com o disco, e
`t_aut4_runbook.py` trava a contagem no runbook. Adicionar um teste lá obrigaria a
editar **documentos de outro front** (AUT-4/R0F, ainda pendentes de commit), o que
esta frente não deve fazer.

Solução: suite KIT-05 **autocontida** em `tools/automacao/kit05/`, com execução
própria. O módulo de produção fica em `tools/automacao/runtime/observacao_passiva.py`
(não é arquivo `t_`/`cp_`, então não entra no inventário travado).

Rodar:
```
python tools/automacao/kit05/teste_observacao_passiva.py
```

Verificação de não-regressão (suite vizinha AUT-4 continua verde, 16/16, exit 0):
```
python tools/automacao/runtime/roda_testes_runtime.py   ->  VERDE, 16 teste(s), exit 0
```

## CLI end-to-end (roteiro de exemplo)

`tools/automacao/runtime/fixtures/kit05-observacao.entrada.json` +
`observacao_passiva.py --entradas ... --out ...` reproduz um roteiro observado.

Resultado real (exit 0):
- `eventos_por_tipo`: `clique_recebido: 2`, `janela_aberta: 1`, `tooltip: 1`,
  `falha_clique_sem_janela: 1`, `janela_fechada: 1`;
- `degradacoes_motivos`: `['pausado', 'sem_mudanca', 'tipo_ativo']`
  (janela_aberta repetida = `sem_mudanca`; tooltip em pausa = `pausado`;
  `clique_emitido` = `tipo_ativo` rejeitado);
- `rejeitados: 1`; `simultaneidade_afirmada: False`.

Isto exercita, de ponta a ponta no disco: registro dos 4 tipos observados,
dedup por mudança, pausa segura, trava de modo passivo e a falha
clique-sem-janela derivada por timeout.

## Contra-prova (defeito plantado)

`scratch/kit/KIT-05/contra_prova.py` planta **um defeito por regra numa CÓPIA** do
módulo (nunca no original) e exige que o teste correspondente **REPROVE**. Exit 0
real com 7/7 iscas reprovando:

```
[A_trava_modo_passivo        ] OK (reprovou: test_rejeita_tipo_ativo)
[B_dedup_por_mudanca         ] OK (reprovou: test_estado_repetido_nao_vira_evento)
[C_fila_limitada             ] OK (reprovou: test_fila_limitada_descarta_e_declara)
[D_teto_capturas             ] OK (reprovou: test_teto_de_capturas)
[E_pausa_segura              ] OK (reprovou: test_pausa_descarta_e_retoma)
[F_sem_simultaneidade        ] OK (reprovou: test_nenhum_evento_afirma_simultaneidade)
[G_timeout_clique_sem_janela ] OK (reprovou: test_timeout_gera_falha_com_motivo)
VEREDITO: VERDE (todas as iscas reprovaram)
```

## Mapeamento runtime (C#) — declarado, NÃO_EXERCITADO

O Core C# (`KIT04Core`) tem hoje `ICoreEvento.RegistrarEvento(tipo, detalhe, dados)`
numa lista sem teto. O pipeline deste módulo é a **especificação executável** que o
lado C# deve reusar: dedup por mudança, fila/retenção/teto, pausa, degradação e
correlação de quadro. A emissão real em jogo depende de rodada autorizada (gate do
dono) e está **NÃO_EXERCITADA** aqui.

## Evidências (caminhos)
- `scratch/kit/KIT-05/resumo.json` — saída do CLI;
- `scratch/kit/KIT-05/cli-out.txt` — stdout do CLI;
- `scratch/kit/KIT-05/contra-prova-out.txt` — contra-prova;
- `scratch/kit/KIT-05/suite-runtime-out.txt` — suite AUT-4 vizinha (não-regressão).
