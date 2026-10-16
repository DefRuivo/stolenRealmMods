# KIT-14 — entrega parcial run1014: candidato R2 auditado offline

Cartão: t_a1f38855. Implementação/coleta desta retomada: default/run1014, instância diferente do autor upstream run1010. Data local conferida: 12/10/2026, 21:08–21:12 BRT. Estado: NÃO CONCLUÍDO, task_accepted=false. Revisão final KIT14R t_9ce7d260 permanece pendente e dependente; não criada revisão duplicada.

## 1. Avanço real, sem repetir as rodadas prontas

Lidos os handoffs atuais de SEG2-FIX t_f067088e e SEG1-RT t_a41dd22d, o filho KIT14R e a entrega run916. SEG2-FIX encerrou implementação OFFLINE R2 no clone; a revisão R1 havia encontrado desvio de alvo exato bloqueado para banner/substring e evidência incorreta da configuração efetiva. Reexecutei o candidato R2 e suas contra-provas em sandbox próprio, sem apenas adotar os resultados do implementador.

Não repeti a qualificação do livro geral run911: ela já está entregue e revisada, com 1 inicializacao e passivo zero. Sua conclusão não cobre o marco RSTV, alimentação passiva ou Runner.

## 2. Pacote, identidade e isolamento

Pacote upstream lido:
%USERPROFILE%/AppData/Local/hermes/kanban/attachments/t_f067088e/KIT14G-SEG2-FIX-offline-r2.zip

- SHA256 a4511b9a9f38ecbd273d904627851e206fe8483fd1a2586685339d3063f04d9d.
- 197316 bytes; 46 entradas; CRC íntegro (testzip=null).
- Manifesto contém 45 payloads: todos conferidos por bytes/SHA256, sem faltantes/extras. O próprio manifesto é a entrada restante.
- Extração nova em scratch/kit/KIT-14-run1014/upstream-r2; checados caminhos absolutos/traversal antes de extrair. Scripts upstream inspecionados, não executados cegamente.
- Fonte R2: 547d10ec2a07f98718f742ee037930c474c6cae42fc22c871e955ffe056c695e, 113942 bytes.
- DLL R2 do pacote: 1cacad9269927ec9a802691ab477abad055b2a779cda44331770af0338ad7879, 80896 bytes.
- Fonte principal: beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193, 109397 bytes; continua sem EsperarInteractable.
- Core principal fonte: 192e463675e2056f3476df2bd3f094e4795e67a130c4392c973c63619b282c59; DLL: 0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d, 34304 bytes.

Sandbox próprio: scratch/kit/KIT-14-run1014/offline-sandbox. Copiados e conferidos 41 arquivos de entrada: bibliotecas locais, binários Core/Adapter/harness, candidato e mutantes. Sem .git/remoto/credenciais/perfil pessoal; temporários e saídas redirecionados para a própria bancada. Referências proprietárias ficaram somente locais, sem anexar/publicar.

Limitação: o harness foi copiado da build upstream e sua identidade registrada no input-manifest.json; NÃO fiz rebuild independente nem novas builds. Não executei preflight de deploy nesta retomada porque nenhum build foi iniciado. Não atribuir a esta entrega prova de compilação independente do harness ou deploy.

## 3. Comando executado e resultados

Comando próprio:
python scratch/kit/KIT-14-run1014/verify_r2.py

Exit real: 0. O driver executou nove processos de harness, gravando stdout/stderr e exit de cada um em scratch/kit/KIT-14-run1014/execution/executions.json.

Partes verdes iniciais:
- parte1: 10 OK, 0 FALHA, 1 NAO_EXERCITADO; exit0.
- parte2: 5 OK, 0 FALHA, 1 NAO_EXERCITADO; exit0.
- parte3: 21 OK, 0 FALHA, 3 NAO_EXERCITADO; exit0.
- parte4: 14 OK, 0 FALHA, 2 NAO_EXERCITADO; exit0.
- parte5: 52 OK, 0 FALHA, 1 NAO_EXERCITADO; exit0.
- Agregado calculado: 102 OK, zero falhas, 8 declarações NAO_EXERCITADO. Estas últimas NÃO contam como aprovação runtime.

Controles negativos executados contra DLLs mutantes separadas:
- default inseguro: exit1, 28 asserts falhos; alcançou DEFAULT sem chave: ativo=true/interactable=false NAO invoca.
- seleção antiga: exit1, 6 asserts falhos; alcançou EXATO bloqueado NAO desvia para substring pronta.
- evidência errada: exit1, 3 asserts falhos; alcançou CONFIG default-seguro valores efetivos.
- Nenhum negativo passou por exceção inesperada. Artefatos do candidato não foram substituídos pelos mutantes.
- Retorno ao candidato após os três negativos: parte5 exit0, 52 OK/zero falhas/1 NAO_EXERCITADO.

Logs novos são execução efetiva OFFLINE; não são boots, não são Runner em jogo, nem medição de overhead.

## 4. Veredito limitado sobre os achados upstream

PASSOU OFFLINE — espera segura: gate real compilado chama o predicado exercitado pelo harness e lê interactable/IsInteractable/isActiveAndEnabled; erros bloqueiam. Fonte candidata, AUT4ProbePlugin.cs:1257 e :1280–1310, inspecionada diretamente.

PASSOU OFFLINE — exato ativo bloqueado não desvia para banner: guarda bloqueadoIdx<0 na segunda passagem, fonte candidata AUT4ProbePlugin.cs:1379–1397. Harness demonstrou espera/etapa zero, liberação posterior somente de Play e preservação de substring quando exato ativo ausente; mutante de seleção reprovou.

PASSOU OFFLINE — configuração efetiva: harness exercitou ConfiguracaoClique, clique_eventos e marcos nos modos default seguro, false/false e false/true; vínculo com Finalizar/RegistrarClique conferido por IL. Finalizar não foi invocado fora do jogo. Lidos de volta três documentos da última rodada verde em final-config-readback.json:
- default: esperar=true, gate_fisico=false, exigir=true, fallback=false.
- false/false: esperar=false, gate=false, exigir=false, fallback=true.
- false/true: esperar=false, gate=true, exigir=true, fallback=false.

config-readback.json registra 15 documentos gerados ao longo das execuções, incluindo negativos. Não misturar esses documentos com o trio final verde, nem tratar clique_eventos da costura offline como clique físico.

NAO_EXERCITADO — eliminação do crash nativo: nenhum boot novo. As evidências físicas run897 e sintéticas anteriores não eram A/B binariamente equivalente; nenhuma causalidade ntdll/0xc0000005 foi isolada aqui.

## 5. Preservação e estado resultante

Quatro arquivos do principal monitorados antes/depois por SHA256 (probe fonte, Core fonte/DLL, AUT-4-estado.json) ficaram idênticos, em main-before.json/main-after.json. git diff --check e git diff --cached --check: exit0. Status final manteve os untracked EV-R2 preexistentes e acrescentou apenas nossos documentos KIT-14; nenhum produto editado/commitado.

Readback de estado às 21:12:09 BRT, gravado em execution/game-processes.stdout.log e state-executions.json: game_processes=0. front-unica.sh status: Lock ativo NAO, disponível. Não adquiri/reconfigurei lock nem montei junction.

Nenhum novo boot, build, instalação, clique de sistema, navegação real, save, alteração de Cloud, publicação ou commit. Cloud não foi consultada novamente nesta retomada: OFF do pai é histórico, não prova estado atual. Antes de futuro boot será obrigatório readback específico e snapshot pessoal IMEDIATO.

Não gerei novos totais dos saves/perfil nem alego preservação antes/depois de uma rodada de jogo inexistente. Não restaurar deriva legítima do dono para manifesto antigo.

## 6. Cobertura dos critérios KIT-14

- Identidade do pacote/candidato offline: PASSOU nesta retomada. Identidade instalada/carregada desse R2 em jogo: NAO_EXERCITADO.
- Livro geral inicializacao: PASSOU upstream run911/revisão912, não refeito aqui.
- Recorder passivo real >0: NAO_EXERCITADO; zero no último arquivo runtime conhecido.
- Clique físico -> janela RSTV -> conteúdo/tooltip -> PNG/relatório: NAO_EXERCITADO nesta retomada.
- Marcar problema e exportar a cadeia real: NAO_EXERCITADO nesta retomada; arquivos offline não substituem.
- Runner positivo e controle negativo runtime: NAO_EXERCITADO. Mutantes do harness não são Runner.
- Mod funcionando sem kit: NAO_EXERCITADO em runtime nesta retomada.
- Uso básico sem Hermes/IA/credenciais: NAO_EXERCITADO em runtime nesta retomada.
- Install/update/remove/rollback da candidata atual: NAO_EXERCITADO; provas históricas continuam limitadas às respectivas versões.
- Saves reais intactos durante rodada atual: não houve rodada; prova antes/depois nova NAO_EXERCITADO.
- Performance comparável com/sem recorder: NAO_EXERCITADO; limiares dispensados por B, coleta exploratória sem veredito passa/falha. Nenhum número sintético.
- Segundo ambiente independente: não usado, portabilidade NÃO comprovada.
- Revisão visual/aceite final humano/publicação: pendentes, não derivados do verde offline.

## 7. Bloqueio atual e runbook mínimo

Os pais estão satisfeitos no grafo, mas seus handoffs explicitamente não autorizam novos boots. t_f067088e/run1010 afirma que os três boots antigos estão consumidos e que runtime exige NOVA autorização específica. O pedido genérico de trabalhar o cartão não identifica orçamento/rota nem revoga esse limite.

Pedido mínimo ao operador: registrar autorização de nova rodada isolada KIT-14, com número máximo de boots e cenários/rota descartável permitidos (R2/RSTV, com/sem recorder, Runner positivo/negativo e mod sem kit). NÃO pedir novamente limiares/B nem consentimento genérico A/Cloud.

Ordem de retomada:
1. Integrar identificadamente o R2 no HEAD atual, somente após revisar o diff contra ponte/edições manuais; recalcular identidade fonte/DLL/config/estado/preparação/runbook. O principal ainda antigo é fato medido, não integração concluída. Não sincronizar clone integralmente.
2. Antes de qualquer build, executar preflight de deploy positivo e negativo em sandbox; builds somente com DeployToBepInEx=false. Não instalar no perfil pessoal.
3. Respeitar o orçamento novo registrado, frente livre/jogo fechado, Cloud específica lida OFF, snapshot SHA256 imediato de dados/perfil/PlayerPrefs e isolamento fail-closed.
4. Capturar recorder/ResultadoFinal e saídas RSTV ANTES do rollback, correlacionando sessão/quadro/hash/config e contexto descartável. Medir somente dados reais com cenário/duração/config comparáveis.
5. Encerrar somente PID próprio; restaurar/conferir ambiente por leitura resultante. Religamento de Cloud ao término da campanha segue responsabilidade/autorização do operador, sem clique OS headless.
6. Se clique físico for necessário: dono clica Skills no contexto descartável previamente preparado; agente coleta quadro/estado pós-ação. Não testar no save pessoal. CliqueFisico é nome de gate do handler, NÃO prova mouse/oclusão.

Hotspot preservado: tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs compartilha gate/identidade com a ponte INT-R1-C2-I1. Nenhuma escrita nele nesta auditoria; integração pendente deve preservar a ponte e alterações alheias.

## 8. Handoff e provas

verification.json: SHA256 7a9d0c37838f406257c8991ddfbf91a5d3603f749aefb381429858265d29ae6b; task_accepted=false; offline_verified=true; runtime_exercised=false; builds=0; new_boots=0.

Provas: C:/dev/stolen-realm/scratch/kit/KIT-14-run1014/execution. Driver: C:/dev/stolen-realm/scratch/kit/KIT-14-run1014/verify_r2.py. Checkpoints: docs/automacao/KIT-14-parte49.md, -parte50.md, -parte51.md.

Não concluir KIT-14 nem liberar KIT14R com critérios runtime faltantes. Registrar needs_input pelo orçamento/escopo explícito; revisão final permanece na instância independente precriada quando a qualificação integral terminar. Nenhuma tarefa nova/política/modelo/cron criado ou alterado.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
