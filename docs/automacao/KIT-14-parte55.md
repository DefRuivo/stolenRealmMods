# KIT-14 — run1442, checkpoint 55

Pré-check Cloud real às 10:10:27 BRT: sharedconfig.vdf, app 1330000, app_cloudenabled=['0'], configuration_off=true. remotecache mtime 13/10/2026 17:15:12 BRT; isto não prova estado remoto. Não alterar Cloud de OFF para ON automaticamente sem execução suportada; preservar estado inicial e declarar eventual residual ao operador.

Lidos integralmente o driver expandido run911 e o suporte de dados vazios do run704; lidos contratos dos scripts de isolamento e da frente única. Preparação usa cópia descartável e rename do real; prepare_empty coloca a cópia pessoal em quarentena fora do caminho de jogo. Nenhum save pessoal será selecionado ou usado como semente. PlayerPrefs será tratado no ramo exato do jogo, não no pai que incluiria outros dados.

Bancada nova precisa: identidade R2 no lugar do gate antigo; manifestos imediatos; captura/preservação do recorder antes de apagar perfil; fechamento somente de PID próprio; recusa de rollback com processo vivo; validação do estado final. O driver antigo não será executado sem essas adaptações dirigidas. Continua sem boot/instalação nesta retomada.
