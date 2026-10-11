# KIT-14 — runbook residual do dono (run710)

## Agora: somente restaurar Steam Cloud

Stolen Realm foi encerrado nas três instâncias de teste. A conferência final real confirmou: diretório de dados original sem junction,111/111 arquivos idênticos ao snapshot KIT-16,BepInEx pessoal53/53 idênticos,registro restaurado e frente livre. Cloud do app1330000 permanece OFF; não foi religada pelo agente porque input de sistema é bloqueado nesta sessão.

1. Na Steam,abra Biblioteca → Stolen Realm → Propriedades → Geral e religue Steam Cloud SOMENTE desse jogo. Não altere a opção global.
2. Confirme visualmente o toggle ligado e responda “Cloud religada”. A retomada deve ler o bloco app1330000 em sharedconfig.vdf e comprovar cloudenabled=1;tempo de remotecache sozinho não vale como prova. Não declarar restauração antes da leitura.

Não abra/carregue o jogo pessoal para tentar completar a evidência de RSTV: o mod-alvo não foi instalado nesta rodada,não existe instância de teste viva e a coleta foi encerrada.

## Depois: clique físico em nova sessão isolada preparada

Esse passo NÃO deve ser feito agora no perfil real. Antes,um executor técnico precisa fornecer e revisar o roteiro menu→personagem descartável→Skills,instalar a build RSTV identificada APENAS no perfil temporário e disponibilizar a trilha runtime do recorder. A autorização KIT-G2 e decisões A/B já existem;não pedir novamente consentimento genérico ou limiares.

Na sessão isolada preparada,o dono fará somente o residual físico:
- clicar no botão Skills visível do RSTV;
- confirmar abertura e posição da janela,conteúdo e tooltip legíveis,contraste/sobreposição/clipping;
- marcar um problema no relatório/visualizador e exportar pela UI,se esse caminho estiver implementado.

A coleta deve ligar a cada ação:sessão,hash DLL/fonte/config,personagem DESCARTÁVEL,evento e frame,estado antes/depois,PNG correspondente e hash do export. Handler invocado não substitui clique físico/alcance do mouse. Alterações de registro/dados devem voltar e ser conferidas antes de religar Cloud.

## Encaminhamento técnico (não é tarefa visual do dono)

- Core/Adapter agora carregam na ordem correta e o Adapter não acusa a NRE antiga;isso não prova recorder eficaz.
- Aumentar NavegarTentativasMax para3600 chegou ao MENU PRINCIPAL com10 botões;Skills continua ausente. Falta navegar Play/criação/seleção descartável e preparar o mod-alvo. Não culpar o botão RSTV por ausência quando o mod não está instalado.
- Consumir/ler ResultadoFinal/eventos reais do recorder e comprovar arquivo/contagem;não usar o arquivo gerado pelo harness sintético como prova do jogo.
- Recoletar objetos APÓS a navegação;na captura tardia,objetos são do frame157 e PNG do1352–1356. Não vincular texto de loading ao screenshot do menu como se fossem simultâneos.
- Só depois executar Runner positivo/negativo,mod sem kit e medições comparáveis com/sem recorder. FPS/frame/I-O não medidos permanecem NAO_EXERCITADO. Performance é exploratória,sem limiares/veredito.

Prova/estado final: scratch/kit/KIT-14-run710/final/verification.json. Relatório: docs/automacao/KIT-14-entrega-run710.md. Revisão independente preexistente:t_9ce7d260,não duplicar.
