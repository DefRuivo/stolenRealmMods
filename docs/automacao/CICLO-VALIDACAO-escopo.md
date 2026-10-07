# Ciclo automatico antes da decisao humana

Objetivo do dono: reduzir revisao humana repetitiva por um ciclo alteracao -> validacao -> falhas acionaveis -> correcao por agente -> revalidacao -> decisao humana. Nao criar novo DoD nem endurecimento secundario sem falha no aceite.

Reutilizar AUT-3 offline, AUT-4 coletor, suites existentes e CAP-1. Trabalho desta rodada: executaveis e testes reais, nao apenas planos. Preparacao runtime nao autoriza instalar probe, iniciar/fechar jogo ou carregar save. Uma unica frente runtime futura quando autorizada. Publicacao e aceite humano sao estados separados.

## Divisao exclusiva dos arquivos
- CIC-1: tools/automacao/ciclo/ciclo.py, seu teste test_ciclo.py. Orquestrar AUT-3 numa copia e emitir fila de falhas/revalidacao ligada a identidade de fonte. Nao editar bancada offline.
- CIC-2: tools/automacao/ciclo/decisao.py, seu teste test_decisao.py. Consolidar evidencia por mod e roteiro residual humano; nao editar orquestrador.
- CIC-3: tools/automacao/cenarios/rstv.py, teste test_rstv.py e dados rstv-*.json. Adaptador/cenarios para AUT-5 existente; nao editar produto ou probe.
- CIC-4: tools/automacao/cenarios/tooltips_shrines.py, teste test_tooltips_shrines.py e dados shrines-*.json. Adaptador/cenarios AUT-6 existente reusando checa_shrines/oraculos; nao editar produto ou probe.
- AUT-4R: revisar coletor atual somente leitura, parecer em docs/automacao/AUT-4R-revisao.md; apontar o necessario para integrar, sem infraestrutura nova.
- Pai: tarefas, KANBAN.md, integracao final e revisoes; unico escritor desses arquivos.

## Contrato de integracao minimo (v1)
Cada modulo de cenarios expoe avaliar(observacoes, identidade) -> lista de criterios. Identidade e dict com fonte_sha e dll_sha (podem faltar: nunca OK sem identidade suficiente). Observacoes e uma lista de dict; adaptadores traduzem formato AUT-4 real, nao impor ao coletor formato inventado. Criterio: id, mod, estado (OK/REPROVADO/NAO_EXERCITADO/INDETERMINADO), classe (offline/runtime), procedencia (execucao/runtime/fixture), esperado, observado, evidencia (lista de caminhos), motivo, tarefa_origem. Pode incluir campos extras rastreaveis. Fixture testa avaliador, nao comprova runtime.

Decisao expoe consolidar(criterios, identidade, aceite_humano=None) -> dict com por_mod, falhas_automaticas, pendencias_humanas, pronto_para_decisao, aceite_humano, publicacao. Criterios de fixture nao contam como prova runtime. Pendencias tecnicas automatizaveis nao sao transferidas ao humano. Roteiro humano so julgamento visual/residual ou autorizacao necessaria, com motivo e instrucoes concretas.

Ciclo usa decisoes quando modulo existir, deve operar mesmo antes da integracao com resultado estruturado. CLI recebe --repo, --trabalho externo e --resultado; roda validacao real em copia com AUT-3 --ancora origem --jogo (essa suite e OFFLINE). Estado nao e aprovado se fonte atual mudar desde a rodada. Fila de correcao e declarativa para supervisor/agentes: caminhos/tarefa/falha/evidencia/criterio e requer nova rodada apos correcoes. Limite de tentativas, detectar sem progresso, nada de comandos de correcao arbitrarios executados automaticamente. Demonstrar falha -> correcao controlada em scratch -> revalidacao. Nao implementar backend LLM separado; supervisor Hermes usa fila.

## Aceite
1. Comando(s) exercitados e outputs reais; testes positivos e controles negativos.
2. Resultado ligado aos bytes atuais, nao log velho; mudanca invalida aprovacoes anteriores.
3. Falha automatica volta ao ciclo, nao ao usuario; apos limite, escalar motivo especifico.
4. Relatorio curto para humano mostra somente residual, sem esconder falhas tecnicas.
5. Sem deploy/jogo/save/publicacao nesta rodada; builds -p:DeployToBepInEx=false em copia isolada, max 6 por rodada com um unico escritor.
6. Revisao independente focada em aceite e integracao apos entrega; secundario vai backlog sem bloquear.

## Correcoes funcionais da primeira integracao
- Contrato positivo runtime: criterio inclui prova_runtime=true, sessao, fonte_sha, dll_sha e config_sha quando config for relevante, evidencia em arquivo existente com hashes; esses valores devem ser confrontados com identidade/manifest da coleta, nao derivados somente de um rotulo runtime. Ausencia/falha de cadeia => NAO_EXERCITADO/INDETERMINADO, nunca OK. Fixtures seguem fixtures mesmo quando todos valores combinam.
- Lacuna de probe/campo/coleta/preparacao e falha automatizavel => falhas_automaticas/fila de agente. Somente autorizacao realmente necessaria (autorizacao_necessaria=true, tipo_pendencia=autorizacao) e julgamento visual explicitamente indicado vao ao dono. Nao classificar todo runtime ausente como humano por padrao.
- Reuso de resultado AUT-3: comparar snapshot do resultado contra caminhos/bytes atuais, sem assinar log velho com fonte_sha nova. Snapshot insuficiente => nova rodada necessaria. Estado/exit do ciclo devem incorporar decisao e identidade DLL, sem APROVADO paralelo a falhas automaticas.
- Estas sao correcoes do objetivo central (falso verde e transferencia indevida de trabalho ao humano), nao uma nova rodada de hardening. Demonstracao final deve terminar sem falhas ambientais escondidas dentro do proprio ciclo.
