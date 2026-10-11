# KIT-14 — checkpoint 17 / run702

## Rodada REAL concluída (parcial)
Terminal coleta_readonly.py attempt02: exit 0. Frente adquirida; perfil e junction preparados; Steam launch exit 0; PID criado 16064 identificado pelo caminho Stolen Realm.exe, fechado graciosamente; KIT16 verificar/restaurar exit 0; KIT03 rollback exit 0; frente liberada.

Sessão: KIT14-run702-readonly-20261010-135444. Probe JSON CONCLUIDO/fase concluido; DLL carregada calculada no runtime = DLL instalada/build run699: 679365e2b0496a33b1c9bb77a7e561b40438ae1443d4120f661b2c5f6845dc57. JSON SHA256 fe5d834631e0255716cae7f104b5509ba0e8e09378579cadab5ef534a0cb3cb1.

Log real: 1 plugin (somente AUT4Probe 0.1.0), gancho GUIManager.Update/OptionsManager.Localize e PlayerLoop ativos, 24 observações, 2 prints. Não há mod RSTV instalado nesta rodada.

## Quadro × PNG
Leitura no frame 158. 01-ui pedido 158/conclusão 163, 2493394 bytes, SHA256 a2520d4b807ce7dcb6ec9800baafba54d210fe7bb86a0be0471cb4d840c161ad. 02-final pedido 163/conclusão 169, 2493318 bytes, SHA256 5b5a9766fc80a0b975f0ddbebcad3b855fadfbbbc552dd714f627e65481c4a66.

PNG 01-ui efetivamente aberto com ferramenta de visão: LOADING com dica 'Shrines', não janela RSTV nem Select Party. Metadado CurrentGuiState=ChoosingCharacter não comprova a tela desenhada. aplicacao.cena_ativa vem vazio no arranque: não inventar cena coletada.

## Preservação observada
Diff da cópia isolada: somente Player.log/Player-prev.log e rotação de 4 arquivos analytics; nenhum Character/GlobalSaveData/SaveFile alterado. Diretório pessoal restaurado: 111 antes/111 depois, igual=true, zero novos/removidos/alterados. Efeito lido do disco, não só retorno do comando. Reconferência independente de registro/perfil/fontes ainda será feita.

## Métricas cruas e lacunas
7 amostras do PID entre t+3.688 e t+17.633s. RSS/PrivateMemory/CPU disponíveis no JSON bruto process-samples.json; não são delta de recorder nem janela de gameplay comparável. FPS/frame/disco de recorder com/sem recorder continuam NAO_EXERCITADO. UI ponta a ponta/Runner/clique e segundo ambiente continuam NAO_EXERCITADO; não fechar o cartão por esta coleta parcial.
