# KIT-05R — parte 05: integração e dependentes conferidos

## Uso real do módulo: ACHADO F8

Comando real: `hermes profile list` e varredura Python de fontes .py/.cs/.sh de tools/automacao, excluindo bin/obj/__pycache__, com termos observacao_passiva, ObservacaoPassiva, clique_recebido e falha_clique_sem_janela. Exit 0. Output: FILES_SCANNED 112; HIT_COUNT 42; HIT_PATHS SOMENTE módulo Python, suite e runner KIT-05. Log estruturado: scratch/kit/KIT-05R-run630/isolated/usos.json.

Leitura fria dos fontes vivos: CorePlugin.cs:206–221 continua Lista/Add sem política de fila/pausa/dedup/retensão; SRAdapterPlugin.cs:50–75 emite tela_detectada/personagens_lidos a cada Update, não os eventos RSTV desta entrega. Portanto não se trata apenas de runtime não exercitado: a cadeia está ausente no código entregue. Aceitar sintéticos não registra janela DE FATO aberta/fechada. Não se revisou novamente o aceite KIT-04; registra-se a integração faltante de KIT-05. Reusar Core/CAP/AUT-4 em vez de chamar módulo desconectado de implementação pronta.

## Roteamento

Cartões dependentes inspecionados: KIT-06 t_66ff87b5, KIT-09 t_a4ca00f9 e KIT-07 t_c364710f, todos todo, tendo t_43675d2e como pai. Não há child de revisão/QA precriado: são consumidores da entrega reprovada. Ao fechar este parecer, não podem ser liberados como se houve aprovação. Será criado conserto único KIT-05F (sem nova revisão duplicada), vinculado como gate adicional dos três, com revisão independente no mesmo cartão de conserto antes da conclusão.

Perfil disponível confirmado por comando: SOMENTE default. Logo o conserto deverá ir a default, mas por NOVA instância implementadora, e a revisão por outra instância/run, nunca por quem corrige. Nenhuma política/modelo/cron/prioridade alterada.

## Próximas provas e limites

Completar contraprovas dos 19 testes do autor (7 já reprovados de forma específica); verificar conservação byte a byte dos fontes vivos em relação à baseline registrada e hashes de logs; emitir parecer final por critério. Suite AUT-4 inteira e desempenho de jogo não serão afirmados como reexecutados. Builds NÃO foram necessários (Python puro entregue); integração C# corrigida no próximo cartão deverá exigir preflight e build isolado, deploy false, antes da revisão. Não haverá correção de produto pelo reviewer.
