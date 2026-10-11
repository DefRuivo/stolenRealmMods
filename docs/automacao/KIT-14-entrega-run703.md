# KIT-14 — entrega PARCIAL run703 / capacidade desktop bloqueada

Cartão t_a1f38855; implementador default/run703; revisor independente PENDENTE (KIT-14R t_9ce7d260, já existente e inspecionado). Complementa histórico run698/699/702, sem sobrescrever. Medição desta rodada: 10/10/2026 14:47:45 -03.

## Resultado e impedimento específico

A decisão A do dono autoriza desligar temporariamente Steam Cloud do Stolen Realm e religar com verificação. Não é necessário pedir essa autorização novamente. A decisão B também permanece: performance exploratória, sem limiares inventados.

A execução está impedida pela política da sessão headless, não por falta dessas decisões: a tentativa real de selecionar Stolen Realm na biblioteca Steam pelo computer_use foi recusada ANTES de executar:

    BLOCKED: computer_use `click` requires approval but single-query mode (-q) runs without a user present to approve it.

Não contornei a recusa com outro emissor de input nem alterei approvals/config Hermes. Não parei o Steam (a captura mostra Abyssus rodando), não editei VDF com Steam ativo presumindo efeito e não desliguei Cloud global.

Nenhum jogo foi aberto/fechado, save carregado/escrito, plugin instalado, build/pacote repetido, publicação ou commit efetuado nesta rodada. Cloud não foi modificada; portanto não há desligamento/restauração executados a declarar. Navegação e novos cenários runtime permanecem NAO_EXERCITADO.

## Evidência real desta rodada

Script novo readonly: scratch/kit/KIT-14-run703/verificar_preflight.py. Executado com `python scratch/kit/KIT-14-run703/verificar_preflight.py`, exit 0. Reusa o leitor tree_snapshot.py existente; não implementa outro isolamento. Resultado gravado, relido e comparado pelo próprio script:

    scratch/kit/KIT-14-run703/preflight.json
    SHA256 2a159de9185a89fcedc57146e6118c2fb692b9b651deb08c56d1d8bc4b922d06

Este exit 0 significa que leituras/preservação local passaram, NÃO que KIT-14/runtime/Cloud passaram.

Comandos subordinados e stdout/stderr próprios estão na mesma pasta; todos exit 0:

- processes: `[]` — nenhum Stolen Realm ativo.
- junction_state: LinkType=null, Target=[] — diretório real, não junction.
- front_check: lock disponível/OK — não adquirido, nenhuma sessão iniciada.
- git_head: d82894ebe95d97f26b7989a848372c691dcb8ef6.
- git_index: vazio — nenhum add/commit.

A tentativa anterior de terminal inline foi recusada por parser/payload; não executou. Mudança de abordagem para arquivo Python legível, executado uma vez com sucesso. execute_code também foi recusado na orientação e substituído por terminal permitido. Essas recusas não são execução nem teste verde.

## Cloud no início e no fim

Leitura dirigida apenas do bloco 1330000, nunca export do localconfig integral:

- Arquivo: C:/Program Files (x86)/Steam/userdata/37602317/config/localconfig.vdf.
- Campo cloud.last_sync_state: synchronized.
- CloudEnabled/cloud_enabled: nenhum valor encontrado no bloco; ausência NÃO é toggle off.
- autocloud.lastlaunch=1791651294; lastexit=1791651315.
- Cache: C:/Program Files (x86)/Steam/userdata/37602317/1330000/remotecache.vdf.
- mtime medido: 2026-10-10 13:55:15.586295 -03.
- Mesmos metadados dirigidos nas duas leituras (cloud_metadata_same=true).
- Cloud desligada efetivamente: NAO_COMPROVADO. Informação fornecida pelo operador no cartão: Cloud ATIVA. Não navegar/escrever até provar off.

Existência/mtime do cache e synchronized provam participação recente, não isoladamente um toggle atual. Não confundidos com prova de desligamento nem restauração. Estado preservado por não intervenção; não alego hash completo do config ou upload remoto.

## Dados reais preservados contra KIT-16

Baseline histórico real utilizado, não criado depois para produzir verde:

    scratch/kit/KIT-16-run700/run-real-3/antes.manifest
    SHA256 62e0aeea556478d34d16af59d93a0d1370ac275bf5c6d69246c9401a27c3ac61

Árvore C:/Users/Pichau/AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm: 111 antes / 111 depois; novos=[], removidos=[], alterados=[]; equal=true. Conferidos bytes/tamanho/SHA por arquivo. Esta é prova de preservação local nesta rodada readonly, não prova Cloud segura numa futura navegação nem nova escrita de save isolado.

## Identidade histórica reconferida

Sem rebuild:

- lib/Assembly-CSharp.dll: 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a.
- tools/automacao/runtime/coletor.py: 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d.
- tools/automacao/cenarios/rstv.py: f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7.
- KIT-14-entrega-run702.md: 0405d8cfe34f018f0a24b086e8553d7750bf1b6f813821298cb3b68e564abefa.
- run702/final/verification.json: 236dc3888d285b678b7b076c83b1b01e538e96b4749f468f28eb202a6d5d1982.
- run702/final/seal.json: 502339c4f7d5473bc5e164be2c71b372d59f1b39b3d2d02cbfaf2300e848c4e8.

A reconferência dos arquivos de selo/relatório não equivale a revalidar todos os payloads run702 nesta rodada. Histórico não foi reiniciado nem promovido a novo runtime.

## Pesquisa de alternativa e limites

Steam Support FAQ 68d2-35ab-09a9-7678 foi lida via browser (inglês): desligamento individual documentado em Biblioteca → propriedades do jogo → General → Cloud Synchronization. Steamworks /doc/features/cloud também acessado. Nesta consulta não se estabeleceu comando CLI confiável/equivalente para controlar e ler o toggle efetivo por app.

A extração web_extract não estava disponível no backend; browser foi a alternativa. Uma expressão JS falhou por escape de newline; leitura com slice em nova chamada funcionou. Sem tentativas repetidas de input recusado. O checkpoint parte23 antecipou a descrição da pesquisa; ela foi efetivamente realizada neste bloco, antes desta entrega final. Não apresentar consulta parcial como auditoria completa das APIs Steam.

## Cobertura e próximo passo concreto

PASSOU (leitura/preservação): pré-condições de processo/frente; 111 dados reais contra snapshot KIT-16; identidade dos seis arquivos históricos; índice vazio.

NAO_EXERCITADO nesta rodada: Cloud off/on; clique físico → janela → conteúdo/tooltip → PNG; marcação via UI; Runner ativo/controle em jogo; produto sem kit; baseline comparável com/sem recorder e FPS/frame/memória/disco; segundo ambiente; aceite humano/publicação. Nenhum dado sintético; nenhum limiar/veredito de performance.

Retomada necessária: operador executar esta tarefa numa sessão em que a aprovação de ações desktop possa ocorrer (sem mudar política silenciosamente), OU preparar o toggle específico do Stolen Realm desligado e prover modo permitido de interação para os cliques de jogo. Confirmar off antes de preparar junction/boot; manter Abyssus e demais apps intactos; no fim, fechar só PID próprio, restaurar dados/registro/perfil, comparar com baseline KIT-16 e somente depois religar/verificar Cloud específica. Se a sessão continuar sem input aprovado, apenas desligar Cloud não resolve a futura prova de clique físico.

Não pedir novamente B1–B6 ou tolerâncias. Não completei KIT-14 nem liberei seu filho KIT-14R com critérios faltantes. Não criei revisão duplicada ou follow-up autoatribuído. Artefatos novos deste run: partes21–23, script readonly, preflight.json/logs e este relatório. Produto, fontes prévias, política/modelos/crons e perfis pessoais não editados.
