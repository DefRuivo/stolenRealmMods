# KIT-05R — parte 03: primeira execução e ajuste do isolamento

## Execução real

`PYTHONDONTWRITEBYTECODE=1 python scratch/kit/KIT-05R-run630/preparar_e_executar.py` terminou exit 0 como driver que registra todos os resultados; isso NÃO é aprovação da entrega.

Cópia inicial: 24 arquivos com SHA256 origem=cópia, incluindo todos os fontes cs/csproj do Core/Adapter (sem bin/obj), além da entrega KIT-05. Suite do autor: `Ran 19 tests ... OK`, exit 0. Contra-prova do autor exit 0; reexecução com logs completos confirmou 7 mutações com exit 1 e FAIL do teste esperado, zero ERROR. CLI da fixture exit 0, capturas=0 (não houve prova de captura).

Suite independente `test_revisao_kit05.py`: `Ran 16 tests ... FAILED (failures=10)`, exit 1; 6 controles positivos passaram. Resultados/logs em scratch/kit/KIT-05R-run630/. São dados sintéticos offline, não jogo.

## Achados reproduzidos (provisórios, reexecução isolada a seguir)

F1: PNG inexistente e quadro 1 anterior ao evento 100 são aceitos como captura após atualização visual.
F2: captura aceita durante pausa; timeout gera evento de falha durante período sem observação.
F3: janela B é deduplicada após A com mesmos dados; 100 ciclos A/tooltip constantes geram 200 eventos, não apenas 2 mudanças iniciais.
F4: fila de 2 não limita 1000 pendentes; 1000 repetições + ações rejeitadas deixam 1999 degradações e 1000 rejeitados.
F5: janela no instante 101 resolve clique de prazo 100 e suprime timeout (0 falhas, esperado 1).
F6: replay exporta 1000 eventos mesmo quando resumo retém apenas 2.

## Obstáculo de isolamento identificado e tratado sem esconder

A primeira sandbox estava sob scratch do próprio repo. Apesar de não conter .git, `git rev-parse` do runner subiu para o repo real, logo a execução do runner NÃO comprova isolamento. Além disso, o bash invocado por subprocess não encontrou `python` (suite=127, contra-prova=127, runner exit 1). Esses resultados serão preservados, sem repetir a mesma abordagem.

Próxima execução usa sandbox FORA da árvore do repo (scratch gerenciado Hermes), verificará ausência de .git em todos os ancestrais e passará PYTHON explicitamente. Reexecutar suite, mutações e CLI antes de concluir. Não houve build/deploy/jogo. O reviewer não corrigiu o produto.
