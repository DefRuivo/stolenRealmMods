# KIT-05R — revisão independente de KIT-05

## Parecer

**REPROVADO para o aceite KIT-05. Revisão concluída; produto/kit NÃO aprovado.**

Cartão de revisão: t_43675d2e; reviewer: **run 630, perfil default, instância independente**. Implementer: KIT-05 t_e9e569f8, **run 629, perfil default**. Data de referência: 2026-10-09. Lente: leitura fria dos fontes vivos + execução independente OFFLINE em sandbox + defeitos plantados. Nenhum runtime novo autorizado ou executado.

A suite nominal de 19 testes passa, mas 10 verificações independentes falham. Foram provados falso sucesso de captura, captura fora do quadro, pausa incompleta, dedup incorreta/spam, crescimento sem limite, timeout apagado por janela tardia e integração não entregue. A contra-prova entregue também aceita falha de teste não-alvo como sucesso. Correção **KIT-05F t_467952ea** criada para F1–F9; consumidores KIT-06/07/09 dependem desse conserto revisado. Encerrar este parecer não concede aceite humano, runtime, instalação, deploy ou publicação.

## 1. Identidade, isolamento e preservação — OK / PASSOU no escopo medido

Workspace original C:/dev/stolen-realm, branch ci-validate-test, alterações tracked/untracked preexistentes inventariadas por git status --short. A revisão não declara repo limpo. Lidos docs/SUPERVISAO.md e docs/PROCESSO-REVISAO.md.

Sandbox definitiva: **C:/Users/Pichau/AppData/Local/hermes/cache/scratch/kit/KIT-05R-run630-sandbox**, fora do repo, sem .git em nenhum ancestral. Cópia dirigida de todos os fontes pertinentes tracked/untracked (24 arquivos, incluindo Core/Adapter .cs/.csproj, sem bin/obj), sem credenciais, perfil ou saves. Provas duráveis: **C:/dev/stolen-realm/scratch/kit/KIT-05R-run630/isolated/**. Scripts de bancada desta revisão: scratch/kit/KIT-05R-run630/, não são novos módulos do produto.

Manifest com pares origem/cópia e SHA256: isolated/manifest.json. Conservação verificada em isolated/verification.json: baseline_tools_count=397; changed_or_removed=[]; manifest_count=24; manifest_mismatch=[]. Isso cobre os fontes/configs/scripts da baseline tools e os 24 arquivos dirigidos, não todo disco/perfil. Nenhuma implementação viva foi alterada pelo reviewer.

| Arquivo vivo | SHA256 medido |
|---|---|
| tools/automacao/runtime/observacao_passiva.py | e3e89d5b2600a4d495465c55a612d60b48ba8746e59ad61b5a0e4ed6ffaac713 |
| tools/automacao/kit05/teste_observacao_passiva.py | bf7ae0e59901503be7f1a564f88da8bf4dcc4996bd9ee15557370f2ba9d496c6 |
| tools/automacao/kit05/roda_testes_kit05.sh | 05bc6a34b233c2c78f7b8e8a073470175b74c6a04a24bf32eb048fb6affd80a3 |
| tools/automacao/runtime/fixtures/kit05-observacao.entrada.json | 6802717c901416f826fc5a020485893409871279c1559dd62d4134884f37cf73 |
| scratch/kit/KIT-05/contra_prova.py | 027e6ee37bcfbfe8f58510f18aadea8002c31b2982a449dc03e5e9b23a8b68a0 |
| docs/automacao/KIT-05-entrega.md | bf4c18e8c0fad79c3ebec75ef12853e0d2f0a6e9285516630277dc59228b505d |
| tools/automacao/runtime/KIT04Core/CorePlugin.cs | 8a415edb92693a37f39cebfa92295b5fa9e120fa544bcf2c247c672ba97ce905 |
| tools/automacao/runtime/KIT04Adapter.SR/SRAdapterPlugin.cs | 9687dbd4fc81399cf94808a5a14fa955b43e5cb327426da811380c5339662b01 |

Os cinco hashes de implementação/testes declarados pelo autor conferem byte a byte; identidade não é o defeito.

## 2. Veredito por critério do aceite

OP abaixo significa tools/automacao/runtime/observacao_passiva.py; os números são linhas do fonte vivo identificado acima. Resultados positivos são limitados à lógica sintética offline.

| Critério | Veredito | Prova / limite |
|---|---|---|
| Clique recebido | ACHADO / FALHOU como observação implementada | aceita dados sintéticos com id/sessão, mas falta produtor/ponte observacional F8 |
| Janela de fato aberta/fechada | ACHADO / FALHOU | parsing nominal OK; tipo informado não prova fato; integração ausente F8 e dedup confunde janelas F3 |
| Tooltip | ACHADO / FALHOU no conjunto integrado | aceita texto informado; não há ligação com emissão real RSTV F8 |
| Falha clique-sem-janela com motivo/timeout | ACHADO / FALHOU | fronteira/motivo/clique_id OK, mas janela tardia apaga vencimento F5 e pausa produz falsa conclusão F2 |
| Relacionar evento/dados/quadro após atualização visual | ACHADO / FALHOU | F1: PNG ausente e quadro anterior são marcados confirmados |
| Não afirmar simultaneidade inexistente | OK / PASSOU na lógica entregue | campos false; teste positivo e mutação específica; isso NÃO valida atualização/pixels F1 |
| Sem clicks/saves/equipamentos/modificações no passivo | OK / PASSOU no módulo Python | positivos rejeitam todos os TIPOS_ATIVOS/CHAVES_ATIVAS; nenhum comando de jogo no módulo; runtime não medido |
| Deduplicação por mudança | ACHADO / FALHOU | F3: perde janela B e gera 200 eventos em 100 ciclos de estados constantes |
| Fila limitada | OK / PASSOU para _eventos; ACHADO para pipeline total | teste fila2 mantém2 eventos; F4 auxiliares ilimitados, F6 replay paralelo |
| Retenção | ACHADO / FALHOU para pipeline total | idade/tamanho de _eventos OK com expirar explícito; auxiliares/replay escapam F4/F6 |
| Teto de capturas | OK / PASSOU para contador nominal; efeito não aprovado | teste nominal/mutação OK; contador incrementa sem PNG e em pausa F1/F2 |
| Pausa segura | ACHADO / FALHOU | registrar bloqueado, mas captura e timeout seguem F2 |
| Degradação explícita | OK para motivos nominais; ACHADO para limites | fila_cheia/pausado/teto existem; uma degradação por repetição pode acumular sem limite F4 |
| Sem captura contínua indiscriminada | OK para ausência de captura automática Python; INDETERMINADO no runtime | CLI fixture captura0; registrar_captura depende de chamada explícita, mas confirmação/pausa quebradas; não há cadeia integrada F8 |
| Testes offline reais | OK quanto à execução; FALHOU para cobertura do aceite | autor19/19 OK; reviewer16 com10 FAIL e6 OK; F9 discriminador falso verde |
| Desempenho runtime e interferência em jogo | NAO_EXERCITADO / INDETERMINADO | sem autorização específica; nenhuma fixture/readback sintético comprova sessão viva |
| Reuso/Core/Adapter para estender coleta | ACHADO / FALHOU | F8: somente especificação executável desconectada, não pipeline instalado no instrumento |
| Independência e encaminhamento | OK / PASSOU | reviewer630 != implementer629; F1–F9 roteados em novo conserto com revisão independente obrigatória |

## 3. Achados e contraprovas

### F1 — captura é afirmação, não efeito (bloqueante)

OP:291–321 grava apos_atualizacao_visual=True e captura_apos_atualizacao_visual=True sem checar arquivo, hash, sessão, atualização ou sequência real de quadros. Controle independente evento quadro100 + captura quadro1 retornou captura confirmada; controle caminho png-inexistente.png + quadro101 também confirmou. Não existe PNG produzido por esses controles. O teste original em tools/automacao/kit05/teste_observacao_passiva.py:228–238 apenas verifica os próprios campos que o método escreve. Prova: isolated/suite-reviewer.log, dois FAIL test_F1_*. Pedido deve ficar separado de captura confirmada; dado ausente/velho/fora do evento nunca deve virar evidência visual.

### F2 — pausa incompleta e conclusão com observação interrompida (bloqueante)

OP:180–182 bloqueia apenas registrar; OP:253–289 e OP:291–321 não consultam pausa. Reviewer registrou evento, pausou e conseguiu captura; clique com prazo100, pausa, t=200 gera falha_clique_sem_janela embora o intervalo não tenha sido observado. Dois FAIL test_F2_* no log. Correção deve bloquear novos pedidos/confirmações indevidas e invalidar/degradar pendências cujo intervalo perdeu observação; não gerar falsa falha ao retomar.

### F3 — chave perde identidade e dedup global gera spam (bloqueante)

OP:85–91 e OP:205–214 ignoram argumento janela; só há _ultima_chave global. Janela A seguida de B com dados iguais: B é descartada. Alternar janela aberta A e tooltip constante 100 vezes gera200 eventos. Dois FAIL test_F3_*. Esperado independente: fatos de janelas distintas preservados; estados iguais por origem não viram mudanças só por intercalar outro tipo; cliques discretos continuam distintos e fechamento/reabertura legítimos sobrevivem.

### F4 — fila pequena não limita estado auxiliar (bloqueante)

OP:114–122, OP:128–137, OP:185–203, OP:237–251: degradações/rejeitados/pendentes/resolvidos não possuem teto/retensão. Com fila_max=2 e retencao_max=2:1000 cliques deixam1000 pendentes;1000 estados repetidos +1000 ações rejeitadas deixam1999 degradações e1000 rejeitados. Dois FAIL test_F4_*; não é medição de desempenho de jogo, é prova offline de crescimento e código sem limite. O teste usa2 como sentinela: NÃO impõe o mesmo teto para todos os buffers; correção pode definir limites explícitos próprios, desde que finitos, testados e com descarte/degradação agregados. Resolução/evicção/expiração também devem limpar referências.

### F5 — janela tardia suprime falha vencida (bloqueante)

OP:241–251 resolve pendência sem comparar prazo. Clique t=0 prazo100; janela t=101; verificar_timeouts retorna0 falhas, esperado1. FAIL test_F5_*. Controle positivo janela errada não resolve; fronteira exata em100 sem janela gera uma falha e não duplica. Abrir depois do vencimento não pode reescrever histórico de timeout.

### F6 — replay/exportação escapa da retenção (bloqueante)

OP:398–428 acumula eventos/falhas em listas paralelas; OP:448–450 exporta-as em vez do estado retido.1000 eventos de roteiro + limites2 -> payload1000, resumo eventos_total2; FAIL test_F6_*. Campo resumo usa fila limitada, mas JSON/memória retêm descarte. Correção deve manter contagem/IDs/export coerentes com política declarada, sem outra lista ilimitada. CLI nominal da fixture, isoladamente, não detecta esse cenário.

### F7 — runner depende de .git e prova descartável (ACHADO)

tools/automacao/kit05/roda_testes_kit05.sh:10 exige git rev-parse e :24 referencia scratch/kit/KIT-05/contra_prova.py. No isolamento definitivo, com PYTHON explícito: runner exit2, `fatal: not a git repository`. Prova: isolated/runner-sem-git.log. Não foi criado .git falso para passar. Resolver raiz pelo layout e manter contra-prova durável junto às ferramentas; nenhuma ausência/etapa pulada pode ser verde.

### F8 — integração não entregue; não confundir com runtime não exercitado (bloqueante)

Varredura completa dirigida de112 fontes .py/.cs/.sh de tools/automacao (sem bin/obj/__pycache__),42 hits para observacao_passiva/ObservacaoPassiva/clique_recebido/falha_clique_sem_janela: SOMENTE módulo/suite/runner KIT-05. isolated/usos.json contém paths/linhas. CorePlugin.cs:206–221 continua Lista/Add sem política limitada; SRAdapterPlugin.cs:50–75 emite tela_detectada/personagens_lidos por Update, não o conjunto RSTV desta entrega. A própria entrega KIT-05:94–99 reconhece especificação e lista C# sem teto. Falta ligação executável em código; autorização runtime não é necessária para implementá-la/prová-la offline. Não se reabriu revisão KIT-04 nem se modificou produto: registra-se o trabalho KIT-05 ausente. Correção deve reutilizar infraestrutura atual e provar ponte/harness offline, opt-in e passiva; sessão real permanece NAO_EXERCITADO.

### F9 — contra-prova aceita alvo que passa (bloqueante de prova)

scratch/kit/KIT-05/contra_prova.py:91–94 considera exit!=0 + presença do nome no output. Nomes também aparecem em testes que passam. No controle adversarial reviewer atribuiu defeito SOMENTE de fila às7 iscas: script original declarou7 verdes/exit0, mas a suite real tem apenas FAIL de fila; test_rejeita_tipo_ativo passa. Provas: isolated/cp-falso-verde.log e cp-falso-verde-suite-real.log. Correção deve exigir FAIL/Assertion específico do alvo, exit1, sem ERROR/skip/timeout; teste adversarial 'alvo PASSA/outro FALHA' precisa reprovar o discriminador. As7 iscas originais foram verificadas separadamente por nós e de fato falham: isso não torna seguro seu oráculo.

## 4. Execuções reais, exits e caminhos

Comandos abaixo são do reviewer, não reprodução textual do relatório do autor. Driver `python scratch/kit/KIT-05R-run630/preparar_e_executar.py` prepara cópia dirigida, chama subprocessos e preserva stdout/stderr; exit0 do driver significa coleta de resultados, NÃO aceite global. CWD de subprocessos é a sandbox definitiva indicada na seção1.

| Execução | Resultado real | Log/manifest em isolated/ |
|---|---|---|
| python tools/automacao/kit05/teste_observacao_passiva.py | Ran19 tests, OK, exit0 | suite-autores.log |
| python scratch/kit/KIT-05/contra_prova.py |7 iscas originais, exit0 | contra-prova-autores.log |
| Reexecução de cada isca original com leitura de FAIL específico |7 casos exit1, alvo FAIL e zero ERROR | mutation-A..G*.log; results.json |
| bash tools/automacao/kit05/roda_testes_kit05.sh | NAO_EXERCITADO pelo runner, exit2 sem Git | runner-sem-git.log |
| python tools/automacao/runtime/observacao_passiva.py --entradas tools/automacao/runtime/fixtures/kit05-observacao.entrada.json --out cli-fixture.json | exit0, replay sintético, capturas0, simultaneidade false | cli-fixture.log |
| python test_revisao_kit05.py -v | Ran16 tests;6 OK,10 FAIL, zero ERROR/skip, exit1 | suite-reviewer.log; verification.json |
| python scratch/kit/KIT-05R-run630/contra_prova_19.py |19/19 testes do autor mostrados reprovando: por caso Ran1 test, exit1, FAIL alvo, zero ERROR; driver exit0 | reviewer-mutations-targeted.json e19 logs individuais |
| python scratch/kit/KIT-05R-run630/controle_falso_verde.py | discriminador original falsamente VERDE/0; controle verifica erro; auditor exit0 | cp-falso-verde*.log; controles-finais.json |
| Suite original após todas as iscas, fonte restaurado/hash original | Ran19 tests, OK, exit0 | suite-restaurada.log |
| python tools/audita_docs.py | exit0, nenhuma inconsistência encontrada | audita-docs.log |

Audita_docs cobre arquivos VERSIONADOS, não estes novos docs untracked; não se usou o verde dele como prova deste parecer. Hashes dos logs guardados em verification.json/controles-finais.json (o último é snapshot antes do log audita-docs). Fechamento dirigido confere a seguir fontes, paths/linhas citados e manifesto final de artefatos. Builds, travas de pacotes/versões e suite AUT-4 inteira NÃO reexecutados: nenhum código/DLL/pacote de produto mudou, escopo entregue é Python puro; não afirmar não-regressão runtime com esse dado. Nenhum build foi permitido sem preflight.

## 5. Obstáculos e histórico preservados

- A primeira cópia ficava sob scratch do repo: runner conseguiu ascender ao .git real e falhou também por PATH de python (exit1, internos127). Não vale como isolamento; provas iniciais preservadas na raiz scratch/kit/KIT-05R-run630/. A abordagem mudou para cópia fora do repo, PYTHON explícito, sem Git ancestral; aí exit2 do runner foi confirmado.
- Primeira rodada reviewer de19 mutações na suite inteira:17/19 limpas, exit1 porque2 tinham ERROR colateral de outros testes. Não verde. Nova abordagem executou só o alvo em cópias novas:19/19 FAIL específicos limpos. Primeiros logs reviewer-mutation-*.log e reviewer-mutations.json preservados.
- Nenhum resultado de fixture implica runtime, pixels, desempenho, ausência de interferência ou comportamento do personagem. Identidades de personagens/versão DLL/config runtime não existem nesta coleta sintética: NAO_EXERCITADO, não preenchidas ficticiamente.

## 6. Correção e gate operacional confirmados

Criado **KIT-05F t_467952ea**, assignee default (único perfil confirmado por hermes profile list), parent t_43675d2e, revisão independente obrigatória no MESMO cartão após correção por nova instância. Escopo/casos F1–F9/paths/hashes constam do corpo. Reviewer run630 não realizará a implementação.

Leitura de volta de cartão e três alvos confirmou t_467952ea nos parents e unsatisfied_parents de:

- KIT-06 t_66ff87b5 — acesso sem terminal/observar/pausar/marcar;
- KIT-07 t_c364710f — exportação privada/retensão;
- KIT-09 t_a4ca00f9 — cenários RSTV.

Os três seguem todo e não avançam só porque este parecer foi concluído. Próximo passo concreto: controlador serial despacha KIT-05F; implementador corrige e mostra positivos/negativos; kanban_request_review com autoria nativa e nova instância; reviewer refuta F1–F9, e só aprovação da correção permite concluir seu cartão. Não há R duplicado nem histórico apagado.

## 7. Limites e segurança

Sem abrir/fechar/navegar jogo, carregar save, instalar, deploy, publicação, git add/commit/stash, alteração de mod/gameplay/Bard/Assembly-CSharp, política/modelo/cron/prioridade. Arquivos criados pelo reviewer: docs/automacao/KIT-05R-parte01..08.md, este parecer e provas/scripts de bancada sob scratch/kit/KIT-05R-run630; cópias descartáveis no scratch gerenciado Hermes. Desempenho/interferência/fluxo visual e aceite humano do DoD permanecem NAO_EXERCITADO. Encerrar a revisão não fecha entrega do kit nem mod para publicação.
