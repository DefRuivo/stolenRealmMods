# KIT-14 — parte37 / diagnóstico tardio real separa loading de roteiro faltante

coleta_tardia.py exit0,mesma build sandbox35e845c0… e opt-ins,apenas NavegarTentativasMax=3600 no cfg temporário; orçamento total60s mantido. Sessão KIT14-run710-late-with-passive-readonly-20261010-175251; PID ainda não relido do result.json. Duração60.964099600038026s.

Leitura do probe:tentativa3600,teto3600,10 botões ativos,Skills=false,estado esgotado. PNG01 inspecionado de fato: MENU PRINCIPAL (Play,Online,Options,Backers,Exit Game),não loading e não RSTV. Não houve invocação. Isso refuta “só esperar mais resolve”: o alvo Skills não existe no menu; faltam handlers intermediários/cenário descartável e instalar mod-alvo.

Correlação:observações/estado capturados no frame157; PNG01 solicitado1352/concluído1356,PNG02 em1356/1361. Texto/CurrentGuiState inicial não descreve automaticamente a tela do PNG tardio. Os3600 incrementos de tentativas cobrem1195 frames Unity entre leitura/pedido; não chamar contador interno de3600 quadros de renderização,FPS ou desempenho.

Core→Adapter e vínculo normal também nesta condição; Player.log leitura dirigida só2 hits KIT04 (linhas45/46),sem exceção nesses resultados. Caminho recorder continua ausente; eventos em memória não lidos,não afirmar zero. Config declarada/teto salva em probe-cfg-measured.txt local antes do rollback.

Nada foi consertado no produto para tornar a auditoria verde. Pós-processamento deve declarar menu apenas no diagnóstico tardio e loading nas condições iniciais; avaliações sobre objetos são de captura inicial,não prova de pixels/UI. Clique OS/Cloud ON residual permanecem runbook. Próximo bloco: ler PID certo,agregar números/guardas/restauração,detector positivo-negativo-fixture/avaliador/viewer/export com leitura dos arquivos resultantes.
