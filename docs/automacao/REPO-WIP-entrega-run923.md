# REPO-WIP — entrega de preservação nominal run923

Cartão: `t_fd245b7f`. Data local: 12/10/2026. Repositório: `C:/dev/stolen-realm`. Branch autorizado e usado: `ci-validate-test`.

## Resultado e alcance

Versionados 16 caminhos entregues, em sete commits independentes por frente. Conteúdo físico preservado byte a byte por SHA256 antes/depois; conjuntos de paths e blobs de cada commit relidos. Documentos em review e checkpoints parciais são preservação documental, NÃO aceite de propostas, correção runtime ou fechamento dos cartões de origem. Este relatório terá commit exclusivo adicional, cujo hash fica no handoff do cartão para evitar autorreferência.

Estado inicial real às 15:28:02: 17 caminhos (3 modificados, 14 não rastreados), índice vazio, HEAD `aea1e583128ae3795cfaff64305606cc05e3a220`. A fotografia do corpo estava desatualizada: b04 e b06 já existiam. Às 15:32:28 eram 18 caminhos: surgiu também o arquivo vazio `%(objectname`. Depois, às 15:35:45, apareceu WIP novo da guarda em outra frente. Não é uma árvore quieta; o status abaixo é uma medição com horário, não promessa de que outros workers pararam.

## Classificação individual

(a) Entregável: versionar. (b) Scratch/derivado: não versionar; não criar ignore sem necessidade. (c) WIP ativo: preservar e deixar ao cartão proprietário.

| Caminho | Classe | Cartão de origem e motivo |
|---|---|---|
| `docs/automacao/EV-R2-NORMAL-b02-parte01.md` | a | `t_d06fd366`, review/run917: proposta entregue; alteração do documento já tracked preservada, sem aprovar mérito |
| `docs/automacao/EV-R2-NORMAL-b03-parte01.md` | a | `t_03f30973`, review/run919: proposta anexada no handoff, não scratch |
| `docs/automacao/EV-R2-NORMAL-b04-parte01.md` | a | `t_fd20ddc4`, review/run920: análise/inventário entregues |
| `docs/automacao/EV-R2-NORMAL-b06-parte01.md` | c | `t_d8fe364d`, running/run922: documento parcial com PENDENTE e sem handoff da rodada; implementação em andamento, commit não assumido por esta frente |
| `docs/automacao/KIT-14-entrega-run916.md` | a | `t_a1f38855`, todo aguardando `t_f067088e`: entrega parcial histórica explícita, não qualificação integral |
| `docs/automacao/KIT-14-parte45.md` | a | `t_a1f38855`, checkpoint run913; prova/preparo já escrito, não fonte runtime em edição |
| `docs/automacao/KIT-14-parte46.md` | a | `t_a1f38855`, checkpoint run916 de contexto e limites |
| `docs/automacao/KIT-14-parte47.md` | a | `t_a1f38855`, checkpoint run916 de dependência técnica discriminada |
| `docs/automacao/KIT-14-parte48.md` | a | `t_a1f38855`, contra-prova offline e hashes da entrega run916 |
| `docs/automacao/KIT-14G-SEG2-parte02.md` | a | `t_139f714f`, done: relatório histórico do preparo run885/handle |
| `docs/automacao/KIT-14G-SEG2-parte03.md` | a | `t_139f714f`, done: relatório dos três boots run895 e limites; título incompleto registra aquela rodada, não reabre o diagnóstico encerrado depois |
| `docs/automacao/ORG-AUT5-DIAG-parte01.md` | a | `t_ceceef6b`, done/revisão run858: diagnóstico offline revisado |
| `docs/automacao/ORG-AUT5-DIAG-parte02.md` | a | `t_ceceef6b`, done: hashes, preservação e handoff revisados |
| `docs/automacao/ORG-AUT5-FIX-parte01.md` | a | `t_2d9f22b1`, done/revisão run871: contrato corrigido e aprovado offline |
| `docs/automacao/ORG-AUT5-FIX-parte02.md` | a | `t_2d9f22b1`, done: prova RED-GREEN e limites; contagens históricas de linhas não corrigidas aqui |
| `tools/automacao/aut5/test_aut5.py` | a | `t_2d9f22b1`, done: bytes atuais coincidem com hash revisado `01a57737b9208073b640859904937c49b7feb343b4cb6e5968fa58d2807e7b78` |
| `tools/automacao/aut5/test_snapshot_modal.py` | a | `t_2d9f22b1`, done: bytes atuais coincidem com hash revisado `9fac95e50bd9f2b6cb6e0fabb3399b9e12736058e7d8fb4abc97afea094fce90` |
| `%(objectname` | b | Arquivo de zero bytes, criado durante a rodada. Sem conteúdo entregável; origem INDETERMINADA, nenhum cartão localizado por busca literal nos comentários. Não foi apagado, movido, stageado nem ignorado |
| `tools/check_deploy_optin.py` | c | `t_8331c57c`, running/run925: alteração concorrente da guarda dentro do escopo ORG-R6; primeiro diff lido adicionava `import hashlib`, cartão prevê commit próprio depois das contra-provas |

Balanço dos 19 caminhos encontrados até 15:35:45: 16(a), 1(b), 2(c). O relatório próprio é um novo entregável adicional, não um resíduo preexistente.

Não inventei justificativa individual de ausência de commit para b02/b03/b04: os handoffs consultados entregaram documentos para review sem registrar commit. KIT-14 e SEG2 declaravam explicitamente nenhum commit nas suas rodadas. DIAG/FIX também registravam nenhuma operação git add/commit; REPO-PRESERVA havia feito snapshot privado e proposto checkpoint condicionado a autorização separada. A autorização nominal para versionar agora vem DESTE cartão/operador, não do snapshot privado.

## Commits das frentes

| Frente | Hash completo | Caminhos |
|---|---|---:|
| EV-R2-NORMAL-b02 | `669ce4a8701824245658aba27b909199adb9be7a` | 1 |
| EV-R2-NORMAL-b03 | `d86ce064b7ecc5709457c23bc3ebd9b4f76a462c` | 1 |
| EV-R2-NORMAL-b04 | `a753312391abddd4c8b00800f7d3aca96366702a` | 1 |
| KIT-14 checkpoints/entrega parcial | `a8c6758ca9f0661218c678f80d2b2d76d3520b2f` | 5 |
| KIT14G-SEG2 evidências históricas | `c8f4e6ba428b3c4393042208a25c3b0f1b21cbe8` | 2 |
| ORG-AUT5-DIAG | `50fec923526aa3193a9311d35595d7f0743545ef` | 2 |
| ORG-AUT5-FIX | `9f4399db905086f2c48b9e8c18d808a75704bc9e` | 4 |

Cada commit usa paths explícitos, origem nomeada no corpo e verificação de paths/blob/SHA256 após escrita. Nenhum `git add -A`, commit -a, push, limpeza, movimento ou reescrita de histórico.

## Prova executada

AUT5 reexecutado antes dos commits, com `AUT5_LOG_REAL=0`, `AUT5_AUTORIZA_COMPILACAO=0`, `python -B` e manifesto/logs no workspace deste cartão:

- `python -B C:/dev/stolen-realm/tools/automacao/aut5/test_aut5.py`: exit 2; `RESULTADO|INCOMPLETO|aut5-rstv|suite OFFLINE ... PASSOU em 16 grupos`.
- `python -B C:/dev/stolen-realm/tools/automacao/aut5/test_aut5.py --contra-prova`: exit 0; `CONTRA-PROVA|PASSOU|aut5-rstv`.
- Manifesto parseado: 16 grupos executados; exatamente `log-real` e `snapshot-modal-CSharp` NÃO_EXERCITADOS, ambas autorizações false. Não se declara suíte completa verde, compilação C#, leitura runtime ou deploy.
- SHA256 de .gitignore, eventos.json, catalogo-referencias.json e EV-R1-entrega.zip idênticos antes/depois. Não executei ORG-R5-DADOS.
- Fonte AUT4Probe permaneceu `beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193`; DLL `7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee`. Avaliador e fixture histórica também intactos.
- 16 arquivos físicos entregues preservados, apesar dos avisos Git de LF/CRLF. Blobs textuais conferidos com normalização LF somente em memória.

Receitas/inventário da auditoria ficam no workspace `C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_fd245b7f`: `inspect_and_test.py`, `commit_deliveries.py`, `inventory-before.json`, `origins-before.json`, `commits.json`, `post-commits.json`, `test-results.json` e logs AUT5. São material de trabalho desta verificação, fora da árvore do produto; os resultados e hashes entregues estão neste relatório versionado e no handoff.

## Status residual e concorrência

Readback `git status --porcelain=v1 --untracked-files=all` às 15:35:45 -03:00:

    M tools/check_deploy_optin.py
    ?? %(objectname
    ?? docs/automacao/EV-R2-NORMAL-b06-parte01.md

A primeira linha tem status Git ` M` (modificado não-stageado). Índice vazio. Nenhum entregável histórico da classe (a) acima sobrou fora do git. WIP da guarda e b06 pertencem a cartões ativos; preservar, não transformar em ignore. O arquivo vazio de classe (b) é anômalo e sem origem provada: proposta é manter fora do versionamento, sem regra de .gitignore nesta tarefa. Higienização, se desejada, requer identificação/autorização; esta tarefa proíbe excluir/mover.

Uma tentativa de commit --only foi recusada durante o merge concorrente de LEVEL-R2-LAND: `fatal: cannot do a partial commit during a merge`. Não criei commit geral nem abortei/resettei o merge. Readback seguinte mostrou merge `be537bdc63dfcbefa06fea528ae5dcf70b39210c`, MERGE_HEAD ausente e índice vazio; confirmei que o blob b02 nesse merge era idêntico ao aea1e58, sem absorver minha entrega. Acrescentei guarda de MERGE_HEAD antes de staging e executei os sete commits nominais só depois. O merge é de outro cartão e NÃO consta como commit criado por mim.

Hotspots comunicados: `C:/dev/stolen-realm/.git/index` (LEVEL-R2-LAND `t_6ecff37a`, ORG-R6 `t_8331c57c`) e `tools/automacao/aut5/test_aut5.py` (ORG-AUT5-FIX/AUT5-F1/F2). Nenhum fonte foi editado para resolver colisão; preservação apenas.

## Defeito de processo e cartões consultados

Defeito comprovado: entregáveis de cartões já DONE ainda estavam sem commit: `t_139f714f` (2 docs), `t_ceceef6b` (2 docs) e `t_2d9f22b1` (2 docs + 2 testes modificados). DONE/revisão/anexo/snapshot privado não asseguraram que os bytes entrassem na junção Git. Este cartão corrigiu precisamente essa lacuna, com commits acima; não há outra implementação de processo executada nem nova tarefa duplicando o saneamento já feito.

Cartões de origem consultados por kanban_show: `t_d06fd366`, `t_03f30973`, `t_fd20ddc4`, `t_d8fe364d`, `t_a1f38855`, `t_139f714f`, `t_ceceef6b`, `t_2d9f22b1`, `t_8331c57c`. Estado de concorrência LEVEL-R2-LAND `t_6ecff37a` lido em consulta SQLite read-only e comunicado por comentários; nenhuma mutação do board por SQL.

O handoff final registra o status mais recente após o commit exclusivo deste relatório e prevalece sobre esta fotografia se outros workers produzirem WIP depois. Aceite da preservação não libera runtime, não atualiza main, não publica e não fecha cartões de origem.
