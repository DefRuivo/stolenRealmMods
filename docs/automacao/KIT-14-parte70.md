# KIT-14 — run1498: auditoria independente do driver e limites

Auditor próprio audit1498.py executado em somente leitura, exit0 para ESCOPO LIMITADO (rota/identidades/restauração), task_accepted=false. Recalculou árvores ATUAIS contra snapshot IMEDIATO da última rodada:115/53/5 iguais, zero novos/removidos/alterados. Não comparou o save atual contra baseline de dias atrás.

Os dois boots instrumentados completaram party1/HUD/alvo exato, CFG ON/OFF lidos de volta e identidades conferidas. Sem-kit carregou exatamente RealmApi0.1.0 + RSTV0.3.3,15/15 ganchos; não há prova de navegação sem instrumento. Avaliador canônico alimentado SOMENTE com observação real associada ao RstvAllSkillTreesTab:7 NAO_EXERCITADO (render vazio, snapshots/ciclo ausentes). Estado não foi pintado de verde por PNG visível.

Performance exploratória da MESMA sequência Play→handler RSTV, não janela pareada/recorder ativo:
- ON:236 frames/13.664s,17.271662763466043 FPS de intervalo,57.898305084745765ms/frame médio;
- OFF:227 frames/13.501s aproximados,16.81356936523221 FPS de intervalo,59.475770925110126ms/frame médio.
Inclui menus/transições/loading, sem replicação, personagens/nome diferentes; não inferir overhead/causalidade/p95. Dados brutos preservados. Picos WS ON2335907840/OFF2336165888 bytes incluem boot inteiro; bytes probe6401418/6607990 são arquivos persistidos, não I/O do disco. Nenhuma tolerância inventada.

Varredura Player.log por assinaturas explícitas: Error/Fatal0 e exceções nomeadas0; Convex Mesh ON2/OFF1/sem-kit1 e DontDestroyOnLoad1 cada, frustum0. Não alegar log totalmente limpo.

Inspeção adicional do contrato do PipelinePassivo.cs:395 mostrou runtime="NAO_EXERCITADO" CONSTANTE, mesmo se houver eventos. Logo um auditor não pode exigir a string hipotética "EXERCITADO" como forma positiva. Ajustar apenas NOSSO auditor para contar eventos reais correlacionados e livro passivo, sem mudar produto/contrato; continua reprovando a observação real ON0. A ressalva literal runtime será preservada, nunca reescrita.
