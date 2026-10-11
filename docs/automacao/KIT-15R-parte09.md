# KIT-15R — parte 09: continuidade sem duplicação

Revisor default/run685. kanban_show(t_d83f3ef6) confirma que KIT-15F já foi criado por run678, permanece todo e depende de t_effde07f. Não criar outro conserto. Seu escopo F1..F12 exige revisão nativa independente antes de conclusão. Os três gates precisam receber KIT-15F como pai antes da conclusão deste parecer.

Lidos test_review_kit15.py (1..110), test_extra_kit15.py (completo), run_review.py (completo), partes05..07. Os testes operam em diretórios temporários e fontes sandbox; não executam jogo/build/deploy. O harness run_review.py regrava evidências históricas, portanto NÃO será reexecutado diretamente: nesta retomada os scripts serão copiados para scratch/kit/KIT-15R-run685, com outputs próprios e staging preservado, sem editar oráculos históricos.

Critérios provisórios sustentados pela leitura dos oráculos e histórico (aguardam rerun próprio):
- Integridade/rollback/propriedade/scan/paths: ACHADO. Asserções medem bytes resultantes ou presença real de arquivo; retorno rc0 não é suficiente.
- Positivos P1..P5: prova prévia com controles plantados; P1 inicial ERROR explicitamente inválido, substituído por defeito de bytes em control-P1-bytes.json. Não contar erro de setup como falha de contrato.
- Independência do ambiente: os testes limpam KIT15_RAIZ, KIT_RSTV_RAIZ, KIT08_KIT09 e PYTHONPATH para comandos extraídos.
- F11: o próprio runner do autor reportou 7/7 enquanto log-07 contém Ran 0 tests/ERROR. Preservar esse falso verde como achado, não como teste aprovado.

Próximo bloco: conferir schema resumido de inventário/resultados e scripts restantes, criar coleta própria não destrutiva, rerodar suite de 27 + extra de 3 + positivo/negativo específico. Nenhum arquivo de produto foi modificado.
