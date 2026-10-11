# KIT-10R — parecer independente adicional (run663)

Tarefa: t_896796be. Parecer: REPROVADO / REQUEST_CHANGES na entrega KIT-10 vigente.
Revisão concluída não significa aprovação do produto, aceite humano, DoD ou autorização de runtime/publicação.
Data da execução: 09/10/2026, início observado23:35:48 e conferência Git23:46:41 UTC-03.
Revisor: default run663, instância nova, não participou de implementação run646/run655/run659 nem das revisões run651/run657/run662. Upstream t_bbad760d concluído foi relido; histórico anterior preservado. Este cartão R é revisão adicional precriada, não repetição de handoff.

## Escopo, identidade e preservação — OK / PASSOU

Cópia própria: C:/dev/stolen-realm/scratch/kit/KIT-10R-run663/sandbox.
`python scratch/kit/KIT-10R-run663/prepare_sandbox.py` exit0: 1156 arquivos de fontes/dados/docs tracked e untracked, 1156 SHA iguais, NO_GIT True, NO_DLL True. Cópia dirigida suficiente ao avaliador Python, não réplica para buildC#.
Manifesto: scratch/kit/KIT-10R-run663/manifest.json. Verificação final inicial: verification.json, baseline_files1156, live_changed=[], sandbox_changed=[]. Todas as entradas preservadas, inclusive alterações manuais existentes. Nenhuma edição de mod, gameplay, probe ou avaliador original. Só documentos desta revisão e scripts/resultados sandbox; mutações temporárias exclusivamente sandbox e restauradas byte a byte.
`git diff --stat -- tools/automacao/kit10` sem difftracked (módulo é untracked preexistente), `git status --short` dirigido confirma novas partes02–07. A prova de preservação efetiva é SHA, não ausência de diff de untracked. Sem gitadd/commit/push.

SHA256 dos arquivos vivos/copias confrontados com handoffvigente:

| arquivo | sha256 |
|---|---|
| tools/automacao/kit10/kit10_cenarios.py | 8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092 |
| tools/automacao/kit10/test_kit10_cenarios.py | 6cc5003e0d9facd42cf967b2da480216243b6d902376f5fc20d9c49d9e8db6e2 |
| tools/automacao/cenarios/tooltips_shrines.py | 65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199 |
| tools/automacao/estilo/estilo_atributos.py | 49cd80b641bff189f822ca28d89a6c9f659ccf845092a47f468ee82c518cc975 |
| tools/testes/regras_shrine.py | 1ef67649463eeab2b113f1423c8c6667ff24b9162c89633608e6c2a51bf9c562 |
| tools/testes/regras_debugger.py | 9e1cdd00b142a8b28aa0f06e8a129229a37702c381e30627054d223f6d1e30e7 |
| scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py | aa9f232b78b0e4cda8ca6de63bcda417cb1b5c79b635ad6235151177c834c6ff |

Suites novas do reviewer (imutáveis para reconferência):
- scratch/kit/KIT-10R-run663/test_review_kit10.py SHA e7eddb6f366213fe09d296f1de74cd4fdbc6d3e7d23c252bc1774129729dd71e.
- scratch/kit/KIT-10R-run663/test_wrapper_metadata.py SHA 2d3a40b5f6099dc2d954bb4222953bcfe5a8946486bd625540a181da90a51799.
- prova_controles.py SHA 582c50d22dd6209923cdf7fa594ae98f84a87452796c7fc1d4ff380a328de078.

## Critério1 — tooltip/contexto/dano, Source e Target — ACHADO / FALHOU (F8)

Esperado rastreado em regras_shrine.dano/escala e tabelas independentes. Controle próprio correto: FlameFodder MaxHealth200 ->28 no Source0; RogueDodge receptor100 ->40 noTarget. Alterar Source100, dano56 ou contribuição20 é REPROVADO; os valores esperados não são derivados do texto observado. Guardas anteriores de falta de campo foram confirmadas por execução e RED.

F8 ALTO: kit10_cenarios.py linhas248–287 e332 não exigem finitude. Três provas próprias `nan_A_fonte_bonus`, `nan_A_dano_observado`, `nan_A_contrib_observada`: string JSON válida `NaN` em um campo por vez -> OK/prova_runtimeTrue. `abs(float('NaN')-esperado)>1e-9` não acusa divergência; fonte não finita também passa como zero. Critério afirma dano correto/Target correto sem número comparável.
Correção: validar tipo e finitude de todas medições numéricas usadas (e esperados), preservando Source/Target e distinção ausência/defeito. NaN/inf/bool/valor inválido nuncaOK. Testes positivo, negativo e guarda loadbearing.

## Critério2 — Worship e dobro confirmado — ACHADO / FALHOU (F9)

Controle positivo com Dwarven2instâncias/2itens e Rogue2instâncias/1item passou. Remover dobroDwarven -> REPROVADO; regra efeito_de_gatilho reusada e nenhum gameplay alterado.

F9 ALTO: kit10_cenarios.py linhas384–397 usa defaultinstancias1, max(1,int(...)), desconhecido como atributo e int(got). Cinco falsosOK/provaTrue:
- vivaDwarven sem instancias e item1;
- Dwarven instancias0 e item1;
- Dwarven instancias2 e itens2.9 (truncado para2);
- auraInventada instancias2 e item1;
- só Dwarven instancias1 e item1: não distingue política de contaruma de contarporinstância, mas motivo afirma dobro preservado.
Correção: contagem inteira positiva explicitamente medida, aura canônica; zero/fracionário/bool/ausente/desconhecido nunca prova válida. Sem gatilho repetido, aspecto de preservação do dobro não foi exercitado e deve declarar lacuna. Manter dobro real do gatilho e desduplicação de atributo.

## Critério3 — BetterStats baseSavedMap/final — ACHADO de cobertura (F12); runtime NAO_EXERCITADO

KIT-10 só delega em kit10_cenarios.py linhas561–568. AUT-7 em estilo_atributos.py linhas1078–1097 retorna NAO_EXERCITADO sem texto e SEMPRE INDETERMINADO com texto; não tem ramo que consulte valores de SavedMap/final e compare números. Probe próprio: semtexto ->NAO_EXERCITADO; com10(15)+extrasnuméricos simulados ->INDETERMINADO. Os nomes de extras do probe são ilustração, não um esquema oficial inventado; o ponto é que nenhum campoextra pode ser consumido por esse ramo.

F12 MÉDIO: honestidade da lacuna PASSOU, mas completar cenário/campos e demonstrar positivo/negativo de base/final não foi entregue. Reuso de ids não basta. Adaptador mínimo local deve documentar entradas necessárias por atributo/personagem e comparar leituras independentes SavedMapbase/finalmotor com display. Coleta real ausente continua lacuna técnica; não editar probe/mod/runtime sem autorização específica.

## Critério4 — estilo/material/keywords/cores e superfícies por evento — PASSOU parcial; runtime NAO_EXERCITADO

Reuso literal AUT-7 e regrasBCT confirmado no código; whitelist do novo aspecto está presente em kit10_cenarios.py linhas428–486. Controle combate/eventoid/BossHealthbar passa; boot reprova; estagiobanana e eventoid ausente ->NAO_EXERCITADO. Múltiplas superfícies constam na infraestrutura BCT/AUT-7 reusada. Novo aspecto C só mede EVENTO, não afirma validar material/cores por si só; materiais/keywords/cores não foram observados em jogo nesta revisão. Sem autorização, não são verdes.
Ressalva F11 (abaixo) também contamina a autenticidade de C; por isso não aprova o critério completo nem entrega.

## Critério5 — Debugger contrato/texto sem truncar — ACHADO / FALHOU (F10)

Linha válida própria passa; campo apósdesc e pipecolado em outrovalor reprovam. Parser/oráculo real reusado.
F10 ALTO: kit10_cenarios.py linhas507–531 filtra somente censo.LINE e não checa pipe no desc (regras_debugger.py linhas162–168 explicitamente pula desc). Dois falsosOK/provaTrue:
- desc="texto|cortado" ->falhas[];
- log com linha válida e outra [Status] Foo |desc="sumiu" (nome semaspas) ->linhas_reconhecidas1/falhas[], descartou justamente linha defeituosa.
AUT-7 já conhece essas classes em estilo_atributos.py linhas1168 e1179–1180, mas o novo aspecto não as aplica. Conferir toda linha declarada dump, desc incluída; logs normais não-dump não devem virar defeito. Sem esperado textual independente não se afirma completude semântica da descrição; a falha aqui é contrato literal verificável.

## Critério6 — rastreabilidade, negativos e ausência/fixture nunca verdes — ACHADO / FALHOU (F11)

Critérios têm id/expected/observado/estado/evidência e reusam esperado independente. HashDLL errado e evidência adulterada nuncaOK nos quatro aspectos, marcasfixture NA OBSERVAÇÃO também nuncaOK. Esses controles foram mostrados reprovando por mutação.

F11 ALTO: kit10_cenarios.py linhas142–150 e545–548 extraem observacoes do envelope sem preservar procedencia/rotulo_fixture. Suiteextra4/4FAIL comprova envelope proceduralmente fixture contendo observação com cadeia simulada ->todos A/B/C/D OK/provaTrue. Fontehash, DLLhash e arquivoevidência coerentes não anulam uma declaração explícita de fixture. Corrigir propagação failclosed em API/CLI e testar marcas de envelope/observação sem alterar input.

Todas as cadeias usadas nesta revisão são SIMULAÇÕES OFFLINE. Arquivos JSON/evidência realmente escritos, hasheados e lidos; não são coleta de jogo. `procedencia=runtime` serve só para exercitar ramo de validação. DLLhash declarado é fictício e explicitamente identificado no teste; nenhum arquivoDLL foi utilizado. Os falsosOK são defeitos do AVALIADOR, não prova sobre mods ativos.

## Execuções reais e veredito por prova

Comandos do autor/CIC4/CLI executados com cwd sandbox; travas Git com cwdrepo. Logs completos e argumentos/exits em scratch/kit/KIT-10R-run663/executions.json. Drivers shell que capturam exit1 saíram0 apenas para apresentar o resumo; o código efetivo do teste está abaixo e não foi mascarado.

| comando/prova | saída real / exit | avaliação |
|---|---|---|
| python tools/automacao/kit10/test_kit10_cenarios.py | TOTAL rodaram28 reprovaram0 nao_rodaram0 /0 | PASSOU, não pega achadosnovos |
| mesmo --isca | ISCA OK defeitoplantado detectado /0 | PASSOU |
| python scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py | PROVA-RED PASSOU7mutacoes /0 | PASSOU guardasvigentes |
| python scratch/kit/KIT-10-run/prova_red_kit10.py | trechosAfonte/Adano nãoencontrados /1 | FALHOU execução obsoleta, F13 ressalva |
| python tools/automacao/cenarios/test_tooltips_shrines.py | TOTAL rodaram28 reprovaram0 nao_rodaram0 /0 | PASSOU reuso |
| python scratch/kit/KIT-10R-run663/test_review_kit10.py | Ran45 FAILED failures10, ERROR0 skip0 /1 | REPROVADO entrega:35OK/10FAIL |
| python scratch/kit/KIT-10R-run663/test_wrapper_metadata.py | Ran4 FAILED failures4, ERROR0 skip0 /1 | REPROVADO:fixtureEnvelope |
| python scratch/kit/KIT-10R-run663/prova_controles.py | total35 passou35, SHArestaurado /0 | PASSOU discriminação |
| CLI kit10_cenarios.py --observacoes fixture.json --out cli-fixture-output.json | total22 OK0 NAO_EXERCITADO22 prova0 /2 | NAO_EXERCITADO runtime; fechamentofixture PASSOU |
| check_segredos/check_padroes_segredo/check_dupes/audita_docs |4exits0, outputs próprios /0 | PASSOU escopoGit; não aprovauntracked sozinho |

Contagem consolidada calculada pelos scripts:49 testes próprios,14FAIL/35OK, ERROR0 skip0. Os14FAIL são exatamente14 falsosOK (F8=3,F9=5,F10=2,F11=4); F12 é lacuna de cobertura separada.
35 casos verdes foram executados INDIVIDUALMENTE no mutante de fechamento: cada um Ran1 FAIL1/exit1; restaurado byte-exato, cadaum Ran1 OK/exit0, semERROR/skip. Quatro positivos e31negativos. Mutação grosseira do fechamento é declarada, não disfarçada de35guardas específicas. RED7/7 acrescenta discriminação seletiva das guardas antigas.
F13 não bloqueia sozinho: driveroriginal é obsoleto e deve ser redeclarado como superado, nunca contadoverde; conserto deve deixar driver atual durável dos quatroaspectos/guardasnovas.

## Higiene e lacunas — estados explícitos

Scanner dirigido reusa motores check_padroes_segredo/check_segredos em lista explícita de novos arquivos, não sóGit. Primeira passagem203arquivos: formatos0 e heurístico2 (exit1 BRUTO). Um é rótulo público concatenado aoSHA na parte06; outro era controleliteral sintético do harness, movido para montagem em memória. Nenhum scannerproduto editado. verification-package.json registrará nova passagem, incluindo classificação EXATA do candidato público e controles em memória detectados; qualquer candidato bruto mantém exit1, não alegar scannerverde por classificação. ZIP íntegro/noDLL/noGit/totais/SHA registrados em zip-verification.json após empacotamento.
F4 testeestilo historicamente variável: NÃO reexecutado nesta rodada. Não alego exit0 atual nem atribuo sua causa sem prova própria; INDETERMINADO. Revisão das propriedades de estilo em jogo, geometria/pixels/UIUX, performance, novas builds, preflightdeploy, instalação, perfildoDono, saves, publicação e gatesKIT-G1/G2/G3/G4: NAO_EXERCITADO. Sem moddependendo deHermes/IA/assinatura, sem alteração depolítica/modelo/cron/prioridade.

## Encaminhamento e conclusão

Conserto criado: t_48b78ecb, “KIT-10F: Corrigir falsos OK e cobertura encontrados no KIT-10R (F8–F12)”, assignee default (único perfil real descoberto), NOVA instância !=run663. Evidência e suiteimmutable fornecidas; positivo/negativo antigo/corrigido, regressões preservadas e nova revisão independente exigidos antes decomplete. Implementador usa handoffnativo kanban_request_review com identidades implementer/reviewer porRUN e hashes/outputs. Revisor atual não conserta nem autoaprova.
Gates adicionais escritos: t_48b78ecb -> KIT12 t_0a434c97 e ->KIT14 t_a1f38855; readback nativo obrigatório antes de fechar. Esta revisão conclui REPROVADA e libera apenas tarefa corretiva; consumidores permanecem dependentes do conserto. História run651/657/662, entregaFinal2 e partes01–07 ficam no disco.
Parecer independente desfavorável não altera retroativamente a avaliação run662: registra novas refutações no mesmo fontehash e impede consumo pela nova dependência.

Artefatos de suporte: partes02–07 deste cartão, manifest.json, review-output.txt/review-results.json, wrapper-output.txt/wrapper-results.json, controls-results.json+controls/*.txt, executions.json+outputs, verification.json/verification-package.json e zip-verification.json. ZIP: C:/dev/stolen-realm/scratch/kit/KIT-10R-run663-evidencias.zip. Não é pacoteThunderstore nem autorização de instalação.
