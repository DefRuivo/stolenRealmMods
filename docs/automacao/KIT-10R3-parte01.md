# KIT-10R3 - revisao independente (rodada 3, lente CONTRACT)

Task: t_bbad760d | run 662 (revisor) != implementador run659 != revisores run651/run657
Workspace proprio de prova: scratch/kit/KIT-10-run662-rev/

## Objeto
Auditar o entregavel `tools/automacao/kit10/kit10_cenarios.py` (e suite + driver RED) do run659
contra o CORPO ORIGINAL do cartao e confirmar, item a item, que TODAS as correcoes pedidas nas
rodadas 1 (F1-F4) e 2 (F5-F7) de fato aterrissaram e continuam load-bearing.

## Provas ja executadas nesta rodada (exit codes reais, sem pipe)
- suite test_kit10_cenarios.py: **exit 0** (TOTAL rodaram=28 reprovaram=0)
- isca: **exit 0** (ISCA|OK|defeito plantado detectado)
- RED driver run659 prova_red_kit10_guardas2.py: **exit 0** (7/7 mutacoes load-bearing)
- reuso CIC-4 test_tooltips_shrines.py: **exit 0** (TOTAL 28/28)
- CLI fixture: exit 2, OK=0, NAO_EXERCITADO=19, prova_runtime=0

## SHA conferidos (batem com o handoff do run659)
- kit10_cenarios.py 8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092
- test_kit10_cenarios.py 6cc5003e0d9facd42cf967b2da480216243b6d902376f5fc20d9c49d9e8db6e2
- scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py aa9f232b78b0e4cda8ca6de63bcda417cb1b5c79b635ad6235151177c834c6ff

## Probes dos revisores anteriores reexecutados por MIM (independente)
- run651/probe_revisor.py: P2/P3/P3b/P4/P5 -> NAO_EXERCITADO/False (exit 0)
- run657/probe_revisor2.py: R1 OK/True; R2/R3 NAO_EXERCITADO; R4 OK; R5 REPROVADO (prefab);
  R6 OK; R7 REPROVADO (dobro removido) (exit 0)
- run657/probe_revisor3.py: R8/R9 NAO_EXERCITADO; R10 REPROVADO (dano errado) (exit 0)

## Pendente nesta rodada
- F4: exit real de test_estilo_atributos.py (run659 declara exit 0)
- travas do repo (check_segredos/check_padroes_segredo/check_dupes/audita_docs)
- escopo git (somente kit10 + docs KIT-10)
- refutacao propria: novo probe de lacunas AUSENTE->OK em TODOS os aspectos
