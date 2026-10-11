# KIT-10R — run663 — parte06: discriminação dos testes e cobertura faltante

## Testes próprios mostrados reprovando — PASSOU

`python scratch/kit/KIT-10R-run663/prova_controles.py`, exit0:
`CONTROLS|total=35|passou=35|RESTORED_SHA=8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092`.
Para CADA um dos 35 testes anteriormente verdes: execução individual unittest no mutante sandbox retornou exit1, Ran1, FAILED(failures=1), sem ERROR/skip; fonte restaurado byte a byte, mesmo teste retornou exit0 Ran1 OK. Logs individuais em controls/*.txt, resultados em controls-results.json. Mutação deliberadamente grosseira do fechamento (`_fechar` promovido sempreOK para negativos, sempreREPROVADO para positivos), não uma suposta correção nem prova de todas as guardas individuais. Complementa RED seletivo7/7 do autor vigente.
Os dez novos defeitos já mostraram os testes falhando no FONTE ORIGINAL, não só no mutante. Nenhum fonte vivo editado.

## F11 — Fixture no envelope descartada — ACHADO/FALHOU

`python scratch/kit/KIT-10R-run663/test_wrapper_metadata.py` (exit capturado1): `Ran 4 tests in 0.169s`, FAILED(failures=4), ERROR0 skip0.
Envelope `{'procedencia':'fixture','rotulo_fixture':true,'observacoes':[observacao_simulada_com_cadeia]}` faz os quatro aspectos A/B/C/D retornarem OK/prova_runtime=true. Readback de wrapper-results.json confirma os quatro. A lista de observações é extraída sem transportar o rótulo do envelope; simulação/fixture passa a se afirmar runtime. Não alterar reuso compartilhado cegamente: solução local KIT-10 deve preservar rótulos e testar API/CLI.

## F12 — BetterStats base/final não completado — ACHADO de cobertura

Readback do probe e código AUT-7:
- sem texto: AUT-7/BetterStats/runtime-base-vs-final = NAO_EXERCITADO;
- com texto10(15) e campos extras SIMULADOS saved_map Strength10 e atributos_final Strength15: mesmo id = INDETERMINADO, motivo continua afirmando valores ausentes;
- código AUT-7 linhas1078–1097 tem retorno incondicional INDETERMINADO após detectar texto; não consulta NENHUM valor extra, portanto preencher inputs não torna comparação exercitável. Nomes dos extras são apenas ilustração, NÃO esquema oficial inferido. Prova principal é ausência de ramo de comparação no fonte e delegação literal no KIT-10.
Esse comportamento é honesto (não falsoOK), mas não cumpre completar cenário baseSavedMap/final nem o positivo/negativo. Correção deve definir contrato mínimo independente + adaptador/testes offline; coleta real continua sujeita à autorização humana, sem alterar probe/mod/gameplay nesta correção.

## Contagem consolidada

Duas suites próprias: 45 casos (10FAIL/35OK) +4 casos (4FAIL), total49, 14FAIL/35OK, zeroERROR/skip. São 14 falsosOK medidos em quatro grupos F8/F9/F10/F11, mais lacuna de cobertura F12. RED original obsoleto = ressalva F13, não execução verde. Nenhum gatehumano satisfeito.
