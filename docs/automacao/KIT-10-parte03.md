# KIT-10 — parte 03: correção dos F1/F2/F3 do KIT-10R (request_changes)

Cartão: `t_bbad760d` (KIT-10). Rodada: implementador run655 (correção pedida pela revisão
independente run651 em `docs/automacao/KIT-10R-parte01.md`).

## Contexto

A revisão independente KIT-10R **reproduziu e aprovou** o entregue (SHA dos 3 arquivos batem;
suite 17/17 exit0; isca exit0; prova-RED 5/5 exit0; fixture exit2; reuso CIC-4 exit0) mas
**pediu mudanças** por três guardas que produzem FALSO OK:

- **F1 (ALTO)** `_asp_por_evento`: só existe blacklist de boot. `estagio="banana"` + `evento_id`
  cai no ramo final → **OK/prova_runtime=True**. Falta a whitelist `ESTAGIOS_DE_EVENTO`.
- **F2 (ALTO)** `_asp_worship_dobro`: `if got is None: continue` — aura viva sem item observado
  (`itens_observados={}`) sobra `defeito=[]` → **OK/prova_runtime=True**. Viola "runtime ausente
  não recebe OK" (mesma classe do F3 do KIT-09R).
- **F3 (MÉDIO)** `_asp_contexto_dano`: com `aura_buff` fora da tabela (guarda da linha 281 não
  roda) a tooltip do receptor não é medida e ainda assim devolve **OK/prova_runtime=True**.
- **F4 (handoff)** o resumo declarava `test_estilo_atributos.py exit 0`; na árvore viva o revisor
  obteve **exit 1** (`BetterFont devia ter provas da suite pura`), por escritores concorrentes
  de outra frente. Reconferir e redeclarar o exit REAL, sem atribuir ao KIT-10.

## Plano de correção (item a item)

1. F1 — exigir `estagio in ESTAGIOS_DE_EVENTO`; qualquer estágio fora da whitelist (e fora da
   blacklist de boot) → NAO_EXERCITADO, com motivo explícito.
2. F2 — aura viva SEM item observado passa a registrar lacuna → NAO_EXERCITADO (nunca OK);
   novo controle negativo (item ausente por aura viva) no teste e na prova-RED.
3. F3 — `aura_buff` declarado fora da tabela OU `contrib` ausente → NAO_EXERCITADO
   (tooltip não medida não fecha OK); novo controle negativo correspondente.
4. F4 — medir o exit REAL de `tools/automacao/estilo/test_estilo_atributos.py` na árvore viva e
   redeclarar (com a causa, se for de outra frente).
5. Novo caso de teste para cada guarda nova (F1/F2/F3) + controles negativos novos.
6. Reexecutar: suite KIT-10, isca, prova-RED (guardas novas load-bearing), CLI em fixture.

## Achados/execução

(será preenchido ao longo dos blocos; próximo arquivo: `KIT-10-parte04.md`)
