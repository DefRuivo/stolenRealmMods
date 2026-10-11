# KIT-15R — parte 06: falhas individuais e controles medidos

Comando python scratch/kit/KIT-15R-run678/run_review.py exit0 (harness de coleta, não aprovação). Todos os subprocessos têm exits próprios e logs em scratch/kit/KIT-15R-run678/logs/. Resumo: execution-summary.json.

Suíte própria recapturada após corrigir path/assert do teste shell: Ran27,22FAIL/5OK,ERROR0/skip0,exit1. Todos22 negativos também individualmente: Ran1,FAIL1,ERROR0/skip0,exit1 (22/22). Shell extraído agora efetivamente rodado: erro layout/exit2, não127.

5 controles dos positivos em cópias mutantes próprias: P2/P3/P4/P5 = Ran1 FAIL1 ERROR0/skip0 exit1; P1 inicialmente deu ERROR1 porque o defeito plantado apagou o arquivo e a leitura levantou FileNotFoundError. P1 NÃO contado como prova válida, escolher novo defeito de bytes retornados antes do fechamento. Baseline restaurado: Ran5 OK exit0. Nenhum teste/produto do autor editado.

## F11 ACHADO — contra-prova aceita zero testes como RED
Autor suíte: Ran18 OK exit0. Contra limpa:6/7, D7 SEM-EFEITO,exit1. Plantei somente sandbox/Core/bin/reviewer-isca.cs (texto C# inerte), executei contra novamente e removi planta. Resultado:7/7 OK exit0; porém log-07.txt tem ERROR setUpModule, Ran 0 tests. A validação :108 e :170 da contra-prova considera qualquer 'Ran ' + exit1 suficiente, sem exigir N>0/falha de asserção/alvo. Esse verde foi refutado por leitura do log, não é aprovação D7. Evidência em contra-author-planted/contra-prova.json e log-07.txt.

## CLI real do ZIP em árvore limpa
ZIP próprio extraído em12 níveis fora da sandbox de fontes: instalar ZIP41/hash lido de volta exit0;statusINSTALADO exit0;remover exit0;rollback remoção exit0/problemas[];statusDIVERGENTE41 faltantes exit0. Falha F4 confirmada também CLI, não apenas API. Conferir efeito final não sucesso do comando.

## Paths e scans/travas
descoberta extraída com HOME/APPDATA e KIT_RSTV_HOME sintéticos =exit0, sem usuário fixo; uso sem Python ainda não demonstrado (só fontes/scripts). Verificar --json e scan ZIP nominal =exit0. check_segredos/check_padroes_segredo/check_dupes/audita_docs =exit0; os scanners Git cobrem874 versionados, NÃO os fontesKIT15 untracked. As falhas F10 em scan dedicado permanecem abertas apesar dessas travas verdes.

Próximo: controle P1 sem ERROR, segurança de paths do instalador, hash final/preservação e parecer com correção/reconferência encaminhados.
