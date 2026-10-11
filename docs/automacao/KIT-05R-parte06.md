# KIT-05R — parte 06: contraprovas completas e preservação

## Todos os testes do autor foram mostrados reprovando

Comando real: `PYTHONDONTWRITEBYTECODE=1 python scratch/kit/KIT-05R-run630/contra_prova_19.py` -> `MUTATIONS_VERIFIED 19 / 19`, exit 0.

O driver enumerou AST das 19 funções test_* do fonte vivo, verificou igualdade com a lista de casos e, para cada uma, executou `python -m unittest teste_observacao_passiva.<Classe>.<teste> -v` numa cópia defeituosa exclusiva. Todos: exit 1, FAIL do teste alvo, zero ERROR, `Ran 1 test`. Logs/sha em isolated/reviewer-mutations-targeted.json e reviewer-mutation-targeted-*.log. Nenhuma etapa pulada/timeout promovida a verde.

Histórico preservado: a tentativa anterior de 19 mutações rodava a suite inteira, teve 17/19 verificadas e exit 1 porque 2 iscas causaram também ERROR em testes não-alvo. Não conta como contraprova limpa desses dois; a abordagem mudou para execução unitária do alvo, sem modificar nem enfraquecer teste/fonte vivo. Logs reviewer-mutation-*.log e reviewer-mutations.json guardam a primeira tentativa.

## Conservação dos arquivos vivos conferida por bytes

Comando Python real de fechamento, exit 0: baseline de 397 fontes/configs/scripts existentes de tools; changed_or_removed=[]; manifest dirigido de 24 arquivos; manifest_mismatch=[]. Dados finais do log do reviewer foram contados por regex, não de memória: reviewer_total=16, reviewer_passed=6, reviewer_failed=10, soma conferida. 50 logs SHA256 inventariados em isolated/verification.json neste instante.

Isso prova preservação dos arquivos da baseline de tools e dos 24 do escopo, não de toda a árvore de disco/perfil. Nenhum arquivo do jogo/save/perfil foi lido/escrito para construir estes testes. Git status inicial preservado como contexto de alterações preexistentes; não se realizou add/commit/stash.

## Conferência adicional para fechar

Refutar o discriminador da contra-prova entregue, que usa qualquer erro + nome do teste em output (nomes aparecem mesmo quando os testes passam). Preparar controle adversarial offline, repetir suite limpa restaurada e emitir parecer com correção gateando KIT-06/07/09. Não corrigir implementação nesta revisão.
