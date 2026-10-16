# KIT-14F3R — parte 05: execução independente GREEN e build

Reteste corrigiu somente pressupostos de formato do detector próprio, sem modificar prova/candidato/produto. test-execution.json: mutante real1; ON0; seis controles OFF/ausente0; cinco corrupções em memória (sessão/snapshot/duplicado/frame/hash PNG)1; prova ausente2. Cada corrupção foi isolada e reprovou o item correspondente, sem contaminar a evidência original. Isso é ensaio do detector, não novo runtime.

integrity-build.py executado realmente com exit0, 173 checagens. Build Release novo em sandbox do revisor, DeployToBepInEx=false, exit0. Scanner deploy: fixture insegura1 esperada, sandbox seguro0. git apply --check do patch0, sem aplicar. ZIP: 144 entradas únicas, CRC e manifest SHA/tamanho conferidos. Candidato/mutante/pacote correspondem exatamente aos hashes declarados.

Auditoria atual read-only: conjuntos/tamanhos/SHA das três árvores reais iguais aos oito manifests iniciais (production115/profile53/other-game5). Nenhum jogo atual, lock ausente, todas as oito raízes de perfil/dados descartáveis removidas, sem reparse point nas árvores reais. Cloud do app1330000 permanece0, lida somente do bloco próprio de sharedconfig; não houve inspeção de servidor Cloud. Esses resultados fortalecem recibos históricos, não substituem snapshot imediato dos boots.

Quatro decompilações novas com ilspycmd deram0: runtime candidato, runtime mutante, plugin e telas. Leitura semântica dos arquivos gerados ainda está em curso. DLL recompilada tem outro hash por ser build em outro caminho; NÃO é confundida com DLL carregada na campanha.
