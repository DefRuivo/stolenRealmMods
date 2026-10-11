# KIT-12R — parte 05: controles próprios e limite da primeira mutação

Comando real `PYTHONDONTWRITEBYTECODE=1 python scratch/kit/KIT-12R-run674/review_controls.py` exit 1. Fonte mutado EXCLUSIVAMENTE sandbox/tools/automacao/kit12/integracao.py e restaurado byte a byte em finally. Oráculo test_review_kit12.py não alterado.

Resultado lido: 10/11 controles discriminaram 0->1->0, cada fase Ran1 test, mutante com AssertionError e sem ERROR/skip. own-mutants.json registra cada fase, próprios logs em own-mutants/.

Controle inicial de fixture NÃO discriminou (0->0->0): remover só o rebaixamento adicional de KIT-12 não produz falso verde, pois KIT-10 já marca fixture, e outros critérios incompletos protegem. Não registrar como teste verde/discriminante. Próxima abordagem: mutação efetiva na classificação de lacunas promovendo INCOMPLETO para APROVADO_OFFLINE, para refutar diretamente ausência/fixture verde. Logs desta primeira tentativa permanecem intactos.

Inspeção do reuso CIC-1 confirmou que montar_fila só emite REPROVADO e fila_da_decisao só falhas_automaticas. Logo critério OK válido não gera item, escapando do saneamento no loop KIT-12 de itens — raiz do F5R. Em critério OK não foi observado qualquer subprocess arbitrário: achado é campo executável residual, não execução.

Travas e efeitos JSON dos achados ainda pendentes. Sem alteração viva de produto/arquivo do dono, jogo ou build. Scanners Git cobrem versionados; revisão dos untracked exige scan dirigido adicional, não aceitar vazio como cobertura.
