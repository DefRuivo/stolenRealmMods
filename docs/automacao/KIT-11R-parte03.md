# KIT-11R — parte 03: refutação independente inicial

Execução real em sandbox: python -c subprocess.run([python, scratch/kit/KIT-11R-run653/test_kit11_review.py], capture_output=True, timeout=30). Log integral: scratch/kit/KIT-11R-run653/review-baseline.log.
Output unittest: Ran 36 tests in 0.221s; FAILED (failures=23); subprocess exit 1. Wrapper preserva o exit explicitamente no output e não converte reprovação em aprovação (wrapper exit 0 só significa captura concluída). Nenhum ERROR/skip.

## ACHADOS já reproduzidos (FALHOU)
C1/C2/C8: aceita timeout ausente/None/NaN/inf, satisfeito='false' torna estado satisfeito, JSON inválido lança exceção não estruturada. Poll pedido de 5 s excede teto de .02 s (sleep capturado [5.0]).
C3: dois callers competindo obtêm o mesmo lock (output RACE 2 acquisitions []); executar sem frente aceita e retorna frente=None. Race foi induzida sincronizando o exists original em dois threads; escrita de lock real em sandbox.
C4: delta de PIDs sem processo criado pelo executor gera fechamento de PID200 (output EXTERNAL_PID_TARGETS [200] commands 1). Driver falso capturou CloseMainWindow; nenhum processo real afetado. Mesmo observação negada gera fechamento. pid_vivo=None escala a taskkill no driver falso (coletor.py:1585-1588).
C4: rollback altera veredito para ROLLBACK e perde OBSERVADO/FALHOU/CANCELADO. Remove diretório vazio preexistente e conteúdo preexistente do dir_backup. Exceção no snapshot antes do try e no rollback dentro do finally deixam lock existente. Cancelamento na última leitura é ignorado e retorna OBSERVADO.
C5/C7/C8: observacao_autorizada=False ainda lê ('menu', 'MainMenu') e retorna OBSERVADO; override ativa_autorizada='false' gera permite_agir=True/PASSOU.

## Controle de qualidade do reviewer
O teste de requer_acao não booleano inicialmente recusava por ambiente ausente, não pelo campo: falso positivo identificado e corrigido SOMENTE no teste sandbox, fornecendo ambiente válido antes de reconferir. Isso não altera executor vivo ou sandbox nem contagem inicial acima; contagem final será publicada após nova execução.
Testes positivos de fonte de arquivo (menu/tela/condição, polling com estado alterado em disco), timeout com relógio real, cancelamento pré-leitura, versão, campos executáveis, autorização ativa recusada, ambiente divergente, lock ocupado/token e restauração byte-a-byte passaram. Arquivo ausente também nunca vira verde. Serão plantadas mutações independentes para comprovar sensibilidade desses positivos/controles que passaram.

C6 valida igualdade declarada offline, mas identidade real do perfil/save continua NAO_EXERCITADO. Sem jogo, plugin, deploy, UI ou publicação.
Próximo bloco: mutações de fonte em memória na sandbox (sem modificar produto), execução final e roteamento de conserto ao implementador com nova conferência.
