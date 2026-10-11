# KIT-10G — correção do request_changes do KIT-10R2 (F5/F6/F7)

Implementador: run659 (perfil default, instância nova) ≠ revisores run651/run657.
Escopo: OFFLINE. Ferramenta/teste em `tools/automacao/kit10/`. Nenhum mod/gameplay tocado.

## Objetivo desta rodada

Corrigir 3 defeitos que produzem FALSO OK no aspecto A (`_asp_contexto_dano`,
`KIT-10/shrines/contexto-dano-fonte-receptor`), sem enfraquecer guardas existentes
(F1/F2/F3 da rodada 1 preservadas) e preservando o dobro do gatilho (DWA-2).

- **F5 (ALTO)** `dano_observado` AUSENTE não entra em guarda nenhuma → com
  `fonte_bonus=0` e sem `aura_buff`, `defeito=[]` → OK/prova_runtime=True afirmando
  "dano bate com o oráculo" SEM nenhum dano medido. Correção: `dano_observado`
  ausente → NAO_EXERCITADO (lacuna), nunca OK.
- **F6 (MÉDIO)** `receptor_bonus` ausente vira `0` (l.244). Com bônus 0 as leituras
  `Source` e `Target` dão o MESMO valor → o eixo (ponto do aspecto A) não é exercitado,
  mas fechava OK. Correção: `receptor_bonus` ausente → NAO_EXERCITADO (eixo não exercitado).
- **F7 (BAIXO)** `fonte_bonus` ausente vira REPROVADO (campo não medido rotulado FALHOU).
  Correção: distinguir NAO_EXERCITADO (não medido) de FALHOU. Só `fonte_bonus` medido e
  não-zero é defeito.

## Itens a cobrir

1. Ler fonte viva `tools/automacao/kit10/kit10_cenarios.py` (aspecto A l.224-321).
2. Ler 3 probes do revisor (`scratch/kit/KIT-10R2-run657/probe_revisor2.py`,
   `probe_revisor3.py`) para reproduzir os casos R3/R8/R9/R10.
3. Editar `_asp_contexto_dano` com as 3 guardas novas (dano/fonte/receptor ausentes → lacuna).
4. Acrescentar controles negativos novos à suíte (`test_kit10_cenarios.py`).
5. Prova-RED durável das guardas novas (mutar cada guarda → deve voltar a OK/prova_runtime=True).
6. Reexecutar o probe do revisor (R8/R9 → NAO_EXERCITADO; R10 dano errado → REPROVADO).
7. Reexecutar suíte, isca, RED antigo (5/5), RED rodada 1 (3/3), CLI fixture, reuso CIC-4, travas.
8. Fechamento em `KIT-10-entrega-final2.md` com paths + hashes; pedir nova revisão independente.

## Progresso

- [x] Orientação (kanban_show): 3 defeitos F5/F6/F7 e probes de repro identificados.
- [ ] (em andamento) leitura dirigida do aspecto A e dos probes.
