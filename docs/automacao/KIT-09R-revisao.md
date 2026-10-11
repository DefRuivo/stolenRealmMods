# KIT-09R — revisão independente: REPROVADO

## Identidade e alcance
Cartão t_0564b789, reviewer run637, perfil default, sessão 20261009_213534_0e7231. Implementer t_a4ca00f9, run635, sessão 20261009_212534_16b45a. Instâncias/autorias distintas. Data local medida na orientação: 09/10/2026 21:35:49 UTC-03.
Revisão OFFLINE dos bytes vivos e do avaliador, não validação do Skill Tree Visualizer em jogo. Sem mod/probe/perfil/save/jogo/deploy/publicação/commit alterados. Parecer preserva entrega inicial e partes01–05; não reescreve história.

## Resultado executivo
REPROVADO para a entrega KIT-09. Sete grupos de achados F1–F7; 30 testes próprios executados, 19 falhas de asserção/11 OK/zero ERROR/zero skip, exit1. Suite do autor verde não refuta as falhas. Há regras úteis que discriminam placeholder, gasto, mutação, clipping, handler e atividade; há também falsa qualificação runtime, perda de guardas normalizadas, dados inválidos e alvo errado aprovados.
Correção aberta: t_01f65801 (KIT-09F). Os quatro dependentes KIT-10/11/13/14 foram vinculados ao conserto e links persistidos conferidos. Concluir ESTE parecer não aprova KIT-09 nem permite liberar a cadeia sem correção revisada.

## Arquivos vivos e SHA256 conferidos
Todos os pares abaixo recompostos dos bytes, iguais à entrega do implementador:

| Arquivo | SHA256 |
| --- | --- |
| tools/automacao/cenarios/kit09.py | a4f7587641174960affab6be73590071fe181c86de919dbb87cceb28025f6586 |
| tools/automacao/cenarios/test_kit09.py | e1b05706f164b4c6a94a87bb7265e7f49942693ea46fb3ffa19a02827d50fd28 |
| tools/automacao/cenarios/kit09-verdade.entrada.json | 596681293039face875a14ca0a25f573c8623fe26f94553778910eebe9c0ad9c |
| tools/automacao/cenarios/kit09-la.entrada.json | 95fd09336b179c04ce9af4ba95fea25a6bf9340f84d0f7e73e95d8b7e23923f0 |
| tools/automacao/cenarios/kit09-velho.entrada.json | 218dd5018516de1a854d201310921464cfd6bd882ca07c3930eb4935a14686e0 |
| tools/automacao/cenarios/kit09-identidade.json | 9c7983b0a061106b565f2caee3cdd753549f6fb9a1016e4ef4d76d29dac1c7b3 |
| scratch/kit/k09/prova-red-kit09.py | 3b6348791c8a6aa7c8972f9842a6057603dfae88b3ca838903fa9dd9e6410543 |
| tools/automacao/cenarios/rstv.py (dependência intocada) | f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7 |
| tools/automacao/runtime/coletor.py (dependência intocada) | 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d |
| tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json | bb37d9a2e4fddec8d955aa5b1354e6672d45063fe8256fb616b25c17d7262754 |

Sandbox nova: scratch/kit/KIT-09R-run637/sandbox. Preparação preservou 456 arquivos do escopo tools tracked/untracked + entrega/RED, sem .git, remoto, credenciais/perfil. baseline.json identifica os arquivos. Comparação posterior com repo vivo: LIVE_CHANGED_OR_REMOVED [] (apenas o escopo inventariado, não alegação de repo limpo). A revisão só cria relatórios e provas próprias.

## Execuções reais e evidências
Diretório-base das provas: scratch/kit/KIT-09R-run637/.

| Comando / execução | Resultado | Arquivo de prova |
| --- | --- | --- |
| python scratch/kit/KIT-09R-run637/preparar.py | exit0, sandbox preservada; subexecuções abaixo | baseline.json |
| python tools/automacao/cenarios/test_kit09.py (sandbox) | RESULTADO\|PASSOU, exit0 | suite-autor.log |
| mesma suite --contra-prova | 21 controles passam na isca sempreOK, exit0 | contra-autor.log |
| python scratch/kit/k09/prova-red-kit09.py (sandbox) | verde0 -> defeito placeholder -> vermelho1 específico -> hash restaurado -> verde0; driver0 | red-autor.log |
| python scratch/kit/KIT-09R-run637/test_review_kit09.py | Ran 30 tests, FAILED (failures=19), exit1; zero ERROR/skip | suite-review.log, review-summary.json, measurements.json |
| python scratch/kit/KIT-09R-run637/prova_controles.py | 21 controles próprios verdes; 21/21 neutralizações específicas derrubam teste correspondente; restaurados 21 verdes; driver0 | own-controls-green.log, own-control-red-00.log até own-control-red-20.log, own-controls-restored.log, controls-proof.json |
| suite autor com guard de render ausente neutralizado em arquivo na sandbox | PASSOU/exit0 apesar de render-observado sem render virar OK | render-mutant-author.log |
| suite autor restaurada após mutante | PASSOU/exit0, SHA original | suite-autor-final.log |
| python tools/automacao/cenarios/test_rstv.py (sandbox) | REPROVOU/exit1, esperado OK/obtido NAO_EXERCITADO | fronteira-cic3.log |

No teste seletivo em memória, cada regra individual foi substituída por uma regra que ignora defeitos, mantendo o fechamento real; cada unittest caiu em AssertionError do alvo, não erro/timeout/skip. O defeito on-disk de render removeu só `if not render`, SHA mutante 823e7cda15505ced3efa0a9d1e42019434ac824e96885926663b2a3a56499825; finalmente restaurado ao SHA a4f75876… original. Isso demonstra discriminação dos controles próprios e falta de discriminação da suite entregue.

## Achados e correção exigida

### F1 — fixture explicitamente sintética vira prova runtime — FALHOU (bloqueante)
CLI REAL sobre kit09-verdade.entrada.json + kit09-identidade.json: exit0, contagem {OK:21}, runtime_exercitado=true, critérios prova_runtime=true. Entrada declara sintetico=true e rotulo_fixture e admite que não existe build medida. O envelope/observação pode contradizer isso com procedencia=runtime, e a qualificação ignora os marcadores. Não é acusação de jogo inventado pelo implementador (o texto da entrega admite simulação); é o OUTPUT executável contaminando consumidores automáticos. Fixture explicitamente procedencia=fixture é recusada, controle positivo da proteção parcial.
Local: kit09.py:761–805, kit09.py:819–842, kit09.py:855–865; fechamento/procedência herdados rstv.py:229–231 e rstv.py:462–530; desempacotar rstv.py:1093–1117. Provas: cli-synthetic-result.json e dois FAIL da suite própria.
Correção: origem sintética/fixture/contraditória deve prevalecer ou invalidar qualificação em API/envelope/lista/CLI. Nenhum rótulo sintético produz prova_runtime; defeito observado em fixture continua podendo reprovar. Não basta trocar valores da fixture ou editar a prosa.

### F2 — adaptador não lê guardas já emitidas no output real — FALHOU
normalizar_observacao do coletor real conserva pai/índice/duplicata em campos. Três positivos E três defeitos dessas dimensões viram NAO_EXERCITADO; os defeitos não reprovam. Em contraste, snapshots normalizados detectam pontos5->3 e skills Fireball->Other, provando que não foi perda genérica da normalização.
Local: kit09.py:319–338 e kit09.py:341–367 leem `o.get`/presença no topo; coletor.py:103–105 e coletor.py:343–376 colocam os dados em campos. Provas: measurements.json labels normalized-parent/index/duplicate-positive/defect e snapshot; 6 FAIL específicos.
Correção: usar leitor do contrato real (estado+valor), forma crua e normalizada equivalentes; defeito medido não pode desaparecer como ausência. Ampliar costura positiva/negativa sobre campos que já existem no coletor.

### F3 — Dependency/arestas convertem lacuna em zero e pulam T5 — FALHOU
Cinco controles dão OK indevido: linhas ausentes; linhas string; dois mapas vazios; T5 sem Dependency medido; linha inventada T5 no critério sem-aresta-inventada. Ausência legítima requer leitura explícita zero/zero, não default. Mesmo quando outro item reprova o roll-up, o falso OK individual permanece inválido.
Local: kit09.py:387–411, kit09.py:432–465 (T5 ignorado) e kit09.py:468–491 (`linhas={}`/get(t,0)). Provas: labels absent-lines, malformed-lines, empty-maps-edges, missing-t5-dependency, t5-invented-edge.
Correção: validar confronto por tier completo e mensurável; ausencia≠zero; detectar aresta T5 em todos critérios que afirmam inexistência; manter ausência legítima explícita válida.

### F4 — malformados iguais/infinito são aprovados — FALHOU
Pai []/[], índice bad/bad, índice -1/-1 e pontos inf/inf retornam OK. Igualdade não valida leitura. O último foi exercitado pela API Python (não é valor legítimo de pontos).
Local: kit09.py:327–332, kit09.py:249–256; a primitiva RC._numerico testa tipo, não finitude. Provas: parent-malformed-equal, index-malformed-equal, index-negative-equal, points-infinite.
Correção: tipo/domínio/forma/finitude antes da igualdade. Malformado/ausente nunca OK; sem enfraquecer detecção de gasto/mutação.

### F5 — clique no botão errado comprova clique Skills da run — FALHOU
clique_fisico={recebido:true,alvo:MainMenu/QuitButton} sai OK. Só se exige alvo não vazio; não se confronta o alvo do cenário independente. Handler/clique separados são uma proteção real, mas alvo incorreto vence o critério específico.
Local: kit09.py:570–589. Prova: wrong-click-target.
Correção: declarar alvo esperado rastreável antes da leitura e confrontá-lo; errado reprova, esperado ausente não comprova alvo. Não impor path universal a todos jogos; preservar contrato declarativo e distinção handler/clique.

### F6 — sessão velha continua qualificando capacidades da rodada atual — FALHOU (qualificação individual)
Meta KIT09-sessao-atual REPROVADO com DADO VELHO (controle PASSOU), mas pontos/skills/etc permanecem OK/prova_runtime=true para review-previous com identidade review-current. CLI global reprova quando meta reprova; portanto não alego bypass do exit global. Há saída contraditória aproveitável por consumidor por-capacidade e runtime_exercitado ainda true.
Local: kit09.py:624–643, kit09.py:773–805 e kit09.py:839. Provas: old-session-meta/old-session-capability.
Correção: amarrar sessão esperada em cada qualificação sem apagar defeitos observáveis; nenhuma prova_runtime da sessão velha descreve rodada atual.

### F7 — 21 controles não cobrem os 21 critérios; mutante passa — FALHOU
CONTROLES tem 21 linhas/20 IDs únicos: falta KIT09-RSTV26-render-observado, personagem duplicado. Desabilitar o guard específico de render ausente deixa suite entregue verde e critério sem render OK. O teste do autor exige runtime=true para a fixture sintética, reforçando F1. Isca global sempreOK e RED único de placeholder não provam controles seletivos para todos os itens.
Local: test_kit09.py:249–294, test_kit09.py:307–317 e test_kit09.py:508–531; kit09.py:279–295. Provas: controls-proof.json/render-mutant-author.log e 21 controles próprios.
Correção: conjunto de cobertura exato, controle de ausência do render, casos adversariais F1–F6 e prova RED seletiva específica + restauração. Não depender somente de script descartável sob scratch para a suite durável.

## Parecer por critério pequeno (qualificação OFFLINE, não runtime)
F1 contamina qualificação runtime de todos; abaixo separo lógica funcional de cada critério para não esconder o que funciona.

| Critério KIT09-… | Veredito da lógica conferida |
| --- | --- |
| RSTV21-abre | OK/PASSOU: false reprova; positivo simulado avaliado |
| RSTV21-fecha | OK/PASSOU: false reprova (não prova fechamento em jogo) |
| RSTV21-fecha-x | OK/PASSOU: false reprova; campo ainda não emitido pelo probe |
| RSTV21-fecha-esc | OK/PASSOU: false reprova; campo ainda não emitido pelo probe |
| RSTV6-personagem | OK para confronto nome esperado/lido; INDETERMINADO para independência temporal do alvo do dono; F1 na procedência |
| RSTV6-skills-sem-mutacao | OK/PASSOU: mutação normalizada detectada; F6 na sessão |
| RSTV6-pontos-sem-mutacao | ACHADO/FALHOU F4/F6; gasto normalizado detectado |
| RSTV26-render-observado | Regra atual recusa render ausente; ACHADO/FALHOU F7 cobertura |
| RSTV26-sem-placeholder | OK/PASSOU: *0/[2]/@power@ detectados no render, RED real |
| RSTV21-tooltip-pai | ACHADO/FALHOU F2/F4 |
| RSTV21-tooltip-indice | ACHADO/FALHOU F2/F4 |
| RSTV21-sem-duplicata | ACHADO/FALHOU F2 |
| RSTV25b-arestas | ACHADO/FALHOU F3; conector T1 faltante é detectado |
| RSTV25b-sem-aresta-inventada | ACHADO/FALHOU F3; T1 excedente detectado, T5 indevido ignorado |
| RSTV25b-ausencia-legitima | ACHADO/FALHOU F3; zero explícito funciona, ausência fabricada também |
| RSTV-geo-medida | OK/PASSOU: dimensão0 reprova, NaN não OK |
| RSTV-geo-clipping | OK/PASSOU: x+largura2000>1920 reprova |
| RSTV5-handler | OK/PASSOU: false reprova, sem clique não comprova clique |
| RSTV5-clique-fisico | ACHADO/FALHOU F5; recebido=false reprova |
| RSTV5-sem-obstrucao | OK/PASSOU: ativo sozinho não comprova; obstruído reprova |
| sessao-atual | OK no meta; ACHADO/FALHOU F6 na qualificação das outras capacidades |

Reuso e esquema: OK estático para import/contrato CIC-3 e 21 definições/roll-up; AUT-5 conferido em tools/automacao/aut5/cenarios-rstv.json. A string esperado_origem é rastreável, mas não atesta por si que personagem/alvo foi declarado independentemente ANTES da observação — essa garantia temporal é INDETERMINADA neste pacote offline. Não substituí o esperado pelo resultado do próprio avaliador.

## Travas, fronteira e lacunas
Travas no repo vivo em leitura: python tools/check_segredos.py exit0 (874 versionados); check_padroes_segredo.py exit0; check_dupes.py exit0 (101/197 entradas sem duplicadas); audita_docs.py exit0. Logs completos e gates-summary.json nas provas. Segredo/docs versionados não cobrem estes novos untracked: não alego que esse verde aprovou os artefatos novos. Conferência dirigida adicional e manifest final acompanham o arquivo de provas.
Build C#/deploy-preflight/pacote/versões e suite global runtime NÃO_EXERCITADOS/não aplicáveis ao escopo de revisão Python/docs; nunca contados verdes. Nenhum build foi tentado.
Fronteira preexistente test_rstv.py está vermelha por confronto do teste com o filtro de alvo RSTV (owners de outro mod na fixture do probe); não alterei filtro/suite/fixture para mascarar vermelho. Registrar e reconciliar em frente própria sem atribuir regressão a kit09.py novo.
Runtime/pixels/clique físico real/ciclo real/impacto FPS/memória/disco/aceite UIUX humano: NÃO_EXERCITADOS. Nenhuma build carregada/config/personagem real foi medida aqui. Nada no parecer substitui KIT-G2/KIT-14 ou os gates do dono/publicação.

## Encaminhamento obrigatório
KIT-09F t_01f65801 contém F1–F7, comandos/provas/aceites e disciplina incremental. Nova instância implementa; nova revisão independente compara critério por critério, com controles RED e hashes, antes de complete do conserto. Parecer inicial permanece histórico.
Leitura de volta do alvo externo confirmou id/título/status todo/assignee default/workspace e F1–F7 no corpo. routing-readback.json confirma gates reais para t_bbad760d, t_f2129aea, t_adc1fbfa, t_a1f38855. Não criei revisão duplicada nem modifiquei políticas/modelos/crons/prioridades. Revisão concluída = parecer entregue; produto REPROVADO.
