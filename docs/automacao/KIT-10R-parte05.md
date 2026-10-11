# KIT-10R — run663 — parte05: regressões existentes e encaminhamento

## Outputs reais

Comando `python scratch/kit/KIT-10R-run663/run_checks.py` (driver exit0; cada filho com seu exit em executions.json):
- autor: `TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0`, exit0.
- isca: `ISCA|OK|defeito plantado detectado: N-A-source: esperado=OK estados=['REPROVADO']`, exit0.
- RED guardas vigente run659: `PROVA-RED|PASSOU|7 mutacoes|todas as guardas sao load-bearing`, exit0. Guardas F1/F2/F3/F5/F6/F7/G7 realmente discriminam lacuna.
- RED original run646: exit1, falhou nas mutações A-contexto-fonte/A-contexto-dano por TRECHO NÃO ENCONTRADO; três outros aspectos discriminaram. É driver obsoleto, NÃO green. Não repeti comando falho, próxima abordagem será controle próprio seletivo sobre fonte atual.
- CIC-4: 28/28 sem NAO_RODOU, exit0.
- CLI fixture própria com quatro aspectos: exit2, JSON lido do disco: total22 OK0 REPROVADO0 NAO_EXERCITADO22 INDETERMINADO0 prova_runtime0. Difere do total19 do handoff porque input desta rodada inclui quatro aspectos; nenhum total inferido.
- check_segredos/check_padroes_segredo/check_dupes/audita_docs no repo vivo: quatro exits0, outputs salvos. Escopo Git/versionados das travas NÃO cobre automaticamente novos untracked; inspeção dirigida adicional pendente.

## Refutações confirmadas por readback de review-results.json

Os dez asserts que falharam correspondem exatamente a critérios retornados como `OK/prova_runtime=true` com:
1. fonte_bonus='NaN';
2. dano_observado='NaN';
3. contrib_observada='NaN';
4. Dwarven viva sem instancias, item1;
5. Dwarven com instancias0, item1;
6. Dwarven instancias2, itens2.9;
7. aura Inventada instancias2, item1;
8. Dwarven instancias1, item1 (não mede o dobro, mas motivo afirma preservá-lo);
9. desc='texto|cortado';
10. log com linha válida + linha [Status] sem aspas no nome e desc=, que foi ignorada.

Não são timeout/exceções: suite própria Ran45 FAIL10 ERROR0 skip0. Reuso e oráculos independentes existem, mas não fecham esses buracos.

## Grafo e autoria

Filhos existentes inspecionados: KIT-12 t_0a434c97 e KIT-14 t_a1f38855, ambos todo e dependentes de KIT-10R. Não liberar consumo sem gate corretivo novo. `hermes profile list` real retornou apenas perfil default (modelo configurado deepseek-flash), portanto é o único assignee válido descoberto. O revisor run663 não fará correção nem mudará modelo/política/prioridade. Abrir conserto para nova instância default com revisão independente same-card; adicionar como gate dos consumidores antes de completar esta REVISÃO REPROVADA.

Runtime/build/deploy/UIUX/publicação permanecem NAO_EXERCITADO. Histórico anterior run651/657/662 não apagado.
