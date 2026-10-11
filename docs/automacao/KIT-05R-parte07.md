# KIT-05R — parte 07: falso verde provado e encaminhamento

## F9 — contra-prova entregue aceita falha de outro teste

Comando real: `PYTHONDONTWRITEBYTECODE=1 python scratch/kit/KIT-05R-run630/controle_falso_verde.py`, exit 0 do auditor (não da aprovação).

O reviewer carregou a contra-prova original da sandbox e atribuiu o defeito SOMENTE de fila a todas as sete iscas, sem editar o fonte vivo. Resultado ORIGINAL: sete mensagens OK, `VEREDITO: VERDE (todas as iscas reprovaram)`, FALSE_GREEN_EXIT 0. Mas o log real da suite tem apenas `FAIL: test_fila_limitada_descarta_e_declara`; `test_rejeita_tipo_ativo ... ok`. O discriminador aceita presença do nome verbose mesmo quando o alvo passa (contra_prova.py:91–94). Prova: isolated/cp-falso-verde.log e cp-falso-verde-suite-real.log. Achado confirmado, não conjectura.

Após as iscas, suite original inalterada restaurada: `Ran 19 tests ... OK`, exit0, fonte SHA256 e3e89d5b2600a4d495465c55a612d60b48ba8746e59ad61b5a0e4ed6ffaac713. Log suite-restaurada.log; hashes de todos os logs no controles-finais.json. Nenhum runtime/jogo/perfil.

## Correção criada (leitura de retorno ainda pendente)

kanban_create retornou t_467952ea, título KIT-05F: Corrigir captura sem efeito, pausa, spam, limites e integrar observação passiva; assignee default (único perfil existente), status todo, gated_by t_43675d2e. Corpo com F1–F9, comandos/provas, fontes/hash, escopo offline e obrigação de revisão independente na nova instância antes de conclusão. Não será corrigido pelo reviewer run630.

Três kanban_link retornaram ok para KIT-05F como pai adicional de KIT-06 t_66ff87b5, KIT-09 t_a4ca00f9 e KIT-07 t_c364710f. A existência e gating efetivos serão lidos no alvo antes de conclusão. Esse roteamento preserva histórico e não concede aceite técnico/runtime/humano nem prioridade nova.

## Próximo passo do reviewer

Ler de volta cartão criado e três consumidores, conferir hashes/conservação finais, gravar parecer final único docs/automacao/KIT-05R-revisao.md e completar SOMENTE este trabalho de revisão com veredito REPROVADO. Completar revisão não equivale a aprovar o kit; consumidores continuarão dependentes de correção revisada.
