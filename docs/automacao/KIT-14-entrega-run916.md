# KIT-14 — entrega parcial da retomada run916

Cartão t_a1f38855. Autor default/run916. Data: 12/10/2026, consultas locais 04:56–05:00 BRT.
Estado: NÃO CONCLUÍDO; dependência técnica e autorização específica de novos boots pendentes. Nenhum boot, build, instalação, clique, save, alteração de Cloud, commit ou publicação nesta retomada.

## Resultado que avançou
O bloqueio antigo do livro geral de eventos foi resolvido pelo pai KIT14G-SEG1-RT t_a41dd22d, revisado por run912. Nesta retomada, não apenas repeti o resumo: extraí o pacote anexado, conferi seu SHA256/CRC, executei o verificador existente e li recorder.json diretamente.

Pacote upstream:
- Caminho: C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_a41dd22d/KIT14G-SEG1-RT-run911-evidencias.zip
- SHA256: 1027d5bcf43efbfccb6a7e1c9bffed1fd122741e2a4e2cda84ccec718ee44ba1
- 1327346 bytes, 45 entradas, testzip retornou null (nenhum CRC inválido).
- Extração própria: scratch/kit/KIT-14-run916/upstream911.

Execução real nesta retomada, sem lançar jogo:
- python scratch/kit/KIT-14-run916/upstream911/verifica_evidencia.py scratch/kit/KIT-14-run916/upstream911: exit0, 28/28 checks verdadeiros, accepted=true SOMENTE para o aceite upstream.
- python scratch/kit/KIT-14-run916/upstream911/test_evidencia911.py: exit0, Ran 11 tests, OK. Dez mutações offline rejeitadas por critérios distintos; nenhuma mutação tratada como coleta runtime.
- Saídas preservadas em scratch/kit/KIT-14-run916/{verify,tests}.{stdout,stderr}.log e executions.json.

Leitura direta da prova do boot upstream:
- Sessão KIT14G-run911-boot01-20261012-041433.
- recorder.json: 1580 bytes, SHA256 de6530df64cc3d927433d36bdb94e6cf4ff617cf8679d8e1f1c9419452ccd45e.
- eventos: lista com 1 inicializacao. Core carregado: 0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d.
- Passivo: eventos_total=0, runtime=NAO_EXERCITADO, capturas_confirmadas=0. clique_eventos=[].
- Portanto o evento de Awake NÃO prova alimentação passiva, RSTV, navegação, interação física ou overhead. Nenhuma conclusão integral KIT-14 foi herdada do accepted upstream.

## Impedimento atual, não o histórico já resolvido
KIT14G-SEG2-FIX t_f067088e está em revisão independente run915 (status RUNNING na consulta), após implementação offline run907. O conserto seguro por default ainda não foi promovido ao principal e não foi validado em runtime.

Hashes calculados diretamente:
- Fonte principal tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs: beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193, 109397 bytes; não contém EsperarInteractable.
- Fonte do clone t_f067088e/repo/tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs: 21744e54fed562d76fb761f709b1a46f6688b04c33dea383eaf443b88da4bd37, 112193 bytes; contém EsperarInteractable. Nenhum arquivo copiado/promovido por mim.
- Core principal fonte192e463675e2056f3476df2bd3f094e4795e67a130c4392c973c63619b282c59 e DLL0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d conferidos.

O principal ainda usa o caminho histórico: Config.Bind CliqueFisico=false em AUT4ProbePlugin.cs:175; MotivoDeBloqueio retorna null quando exigir=false em :1221; verifica interactable em :1226 somente quando o gate está ligado. Handler é invocado em :1372/:1392. Estabilidade em :1310–1311 conta chamadas. A correção desse instrumento pertence à frente existente, não a esta qualificação.

O corpo e o handoff de t_f067088e declaram expressamente: os três boots da rodada anterior foram consumidos; nova comprovação exige autorização específica. Não reutilizei KIT-G2/A/B como autorização ilimitada nem iniciei boot com o instrumento pendente. O run911 sem navegação já entregue não autoriza nova rodada com Accept/RSTV.

Registrada edge t_f067088e -> t_a1f38855 para impedir retomada prematura. Não criar conserto/revisão duplicada nem mudar modelos/política/crons. Após a revisão, ainda serão necessárias integração identificada e autorização específica da rodada.

## Estado local read-only
Às 05:00:42 BRT, readonly-state.json registra:
- processo Stolen*: [];
- diretório de dados: Directory, NotContentIndexed, sem ReparsePoint;
- backups Stolen Realm*.kit16-real: [];
- Steam Cloud app1330000: cloudenabled=[0], configuration_off=true;
- remotecache.vdf mtime 12/10/2026 04:15:15.119572 -03:00, correspondente ao boot upstream, não cache imutável;
- front-unica.sh status às04:58: Lock ativo NAO, disponível.

Cloud não foi alterada nesta retomada. Sua configuração OFF é leitura local, não inspeção do servidor remoto. Religamento ON permanece residual do dono/operador ao término da campanha isolada; não tentar clique de OS nesta sessão headless.

Não medi novamente o conteúdo dos saves nem alego novos totais de preservação pessoal: não houve runtime/intervenção. O pai revisado traz preservação antes/depois do seu próprio boot; não transfiro aquela prova para uma nova rodada inexistente. Alterações manuais prévias em AUT5 e documentos foram preservadas, sem editar produto.

## Cobertura e lacunas
- Livro geral inicializacao: PASSOU na prova real upstream, reconferida offline aqui; novo runtime nesta retomada NAO_EXERCITADO.
- Alimentação passiva efetiva: NAO_EXERCITADO, zero eventos no arquivo upstream.
- Clique físico -> janela RSTV -> conteúdo/tooltip -> PNG/relatório -> marcar problema/export: NAO_EXERCITADO nesta retomada; relato humano run897 alcançou HUD/Skills, mas probe estava inerte, sem cadeia recorder equivalente.
- Runner autorizado/controle negativo runtime: NAO_EXERCITADO; controles offline do verificador não são Runner em jogo.
- Mod funcionando sem Core/Adapter e sem IA/credenciais: NAO_EXERCITADO em runtime nesta retomada; não promover documentação/inspeção estática a efeito.
- Install/update/remove/rollback atual: NAO_EXERCITADO nesta retomada; provas históricas limitadas às versões/sessões declaradas.
- Performance com/sem recorder no mesmo cenário: NAO_EXERCITADO; limites dispensados por decisão B, sem inventar números nem dar veredito passa/falha.
- Segundo ambiente independente: não disponível nesta execução, portabilidade NÃO comprovada.
- Revisão visual/aceite humano/publicação: não realizados; não são consequência do verificador upstream.

## Runbook de retomada — pedido mínimo ao operador
1. Concluir correção e revisão t_f067088e; integrar somente o diff aprovado, preservando alterações alheias e a ponte atual. Conferir nova fonte/DLL/config por hash; receita antiga congelada não representa o conserto do clone.
2. Registrar autorização específica de nova rodada KIT-14 com orçamento de boots e rota de teste descartável: RSTV com/sem recorder, Runner positivo/negativo e mod sem kit. Não pedir limiares de performance outra vez; B permanece coleta exploratória.
3. Antes de montar: jogo fechado/frente livre, Cloud app OFF e snapshot SHA256 recursivo IMEDIATO dos dados/perfil/PlayerPrefs. Nenhuma restauração de deriva legítima para baseline histórico.
4. Durante a rodada autorizada: capturar resultado/recorder ANTES do rollback, correlacionando sessão/quadro/objeto/DLL/config; ler saídas reais de janela/tooltip/PNG/export. Medir somente números realmente capturados no mesmo cenário/duração/config com/sem recorder.
5. Ao encerrar: somente PID próprio, restauração fail-closed e readback de árvores/registro/junction/perfil/lock; Cloud ON pelo mecanismo autorizado quando a campanha terminar, com readback.
6. Somente se for necessária prova de mouse: dono clica no botão Skills do RSTV no contexto descartável preparado; agente registra estado e quadro pós-ação. Handler in-process NÃO prova clique físico/oclusão. Isso não pede acesso ao save pessoal.

## Handoff
Revisão KIT-14R t_9ce7d260 inspecionada: TODO, dependente deste cartão; mantida sem liberação, pois critérios KIT-14 ainda faltam. Implementação/checkpoint desta retomada: default/run916; reviewer independente do KIT-14 pendente. task_accepted=false. Nenhuma tarefa nova criada.

Artefatos novos: docs/automacao/KIT-14-parte46.md, KIT-14-parte47.md, KIT-14-entrega-run916.md; provas em scratch/kit/KIT-14-run916. Bloquear por dependência real, não fechar tarefa incompleta nem solicitar revisão duplicada.
