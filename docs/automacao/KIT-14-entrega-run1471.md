# KIT-14 — entrega parcial run1471: runtime identificado, não qualificação integral

Tarefa t_a1f38855. Autor/coletor: default/run1471. Data14/10/2026,14:16–14:35 BRT. Estado: NÃO CONCLUÍDO; task_accepted=false. Revisão independente final: pendente KIT14R t_9ce7d260; não liberada nem duplicada. Filhos BP5 t_49686933 e LEVEL-RT-INGAME t_fc484826 inspecionados; nenhum escopo deles executado.

## Resultado principal

Recuperei a rodada real que run1442 executou após o checkpoint56, identifiquei por que o marco RSTV não ocorreu, corrigi SOMENTE a montagem da bancada e rodei três boots sequenciais reais. RSTV0.3.3 agora carrega com RealmApi0.1.0 e aplica15/15 ganchos, inclusive sem AUT4/Core/Adapter. Todas as três rodadas restauraram dados/perfil/PlayerPrefs; leitura independente das árvores atuais confirmou integridade.

Isso NÃO prova janela RSTV, tooltip, mark/export ou Runner. A rota do driver só chega Select Party com party vazia. O gate real rstv-full REPROVA exit1; sete capacidades do avaliador canônico são NAO_EXERCITADO, não verdes.

## 1. Causa recuperada e correção da bancada

run1442 sessão KIT14-run1442-boot01-20261014-101617, PID22132, rodou em10:16–10:17, apesar de não haver entrega final. Não repeti esse boot por engano. LogOutput-isolado.txt:21 rejeita RSTV por com.gumatos.realmapi ausente. Probe termina CONCLUIDO, mas navegação esgotou3600 tentativas e recorder ficou1 inicializacao/passivo0. Dois PNG idênticos mostram Select Party, não a janela solicitada.

Plugin.cs:49..67 confirma dependência hard RealmApi>=0.1.0; Plugin.cs:22..25 declara botão Select Party REMOVIDO. Ajuste foi adicionar os três assemblies reais RealmApi.dll/Core/Hooks na bancada descartável. Nenhum produto/fonte principal alterado; fonte principal do probe continua beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193, sem promoção automática de R2.

Driver novo scratch/kit/KIT-14-run1471/driver.py reutiliza infraestrutura KIT16/run1442; snapshot IMEDIATO, dados pessoais em quarentena fora do caminho do jogo, Cloud OFF lida antes do boot, lock único, fechamento de PID próprio, captura antes do rollback, recusa de restaurar com processo vivo. Nenhum build: preflight de build/deploy não executado nem alegado como aprovação; apenas cópias identificadas no perfil temporário. Nenhum commit/push/publicação/deploy no Default.

## 2. Identidades dos binários de entrada

- AUT4Probe R2 DLL:1cacad9269927ec9a802691ab477abad055b2a779cda44331770af0338ad7879; fonte547d10ec2a07f98718f742ee037930c474c6cae42fc22c871e955ffe056c695e.
- Core DLL:0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d; fonte192e463675e2056f3476df2bd3f094e4795e67a130c4392c973c63619b282c59.
- Adapter DLL:d1b383c6cfeae198e77f96047ead39c1a54678f24888c110fed60a9561dded50.
- RSTV DLL:1d0b85e8d0f30d10c4fe7c4e044d30380537e8801a7d39875192459a2e51d5cc.
- RealmApi.dll:764b72d84a976a534292a518d14177b76fdede070bf9979e649efc5df25d19d7.
- RealmApi.Core.dll:d4e72f24e4e7c503bdd32c200b4bfa7635a1529b09451e2a35b5400547d32fb2.
- RealmApi.Hooks.dll:86d7fcf0012e1a611b42e96081609704a23a0129cc9918b3f1004c14a816778a.

Probe/Core calculam hash do próprio assembly carregado nos JSON e conferem com entradas. RSTV/API: hashes de cópia/entrada e versão/log de carga conferidos; NÃO alegar hash calculado do assembly RSTV carregado nem correspondência com todas as fontes atuais. Não gerar pacote público sobre esses binários antigos. ZIP R2 upstream já auditado run1014: a4511b9a9f38ecbd273d904627851e206fe8483fd1a2586685339d3063f04d9d; não reexecutado nesta retomada.

## 3. Execuções reais

Comandos executados e consoles em scratch/kit/KIT-14-run1471:

    python test_driver.py --mutant: exit1,6 testes/1 failure (recorder religado em sandbox).
    python test_driver.py: exit0,6 testes verdes após negativo.
    python driver.py recorder-on: exit0,PID8844,sessão KIT14-run1471-recorder-on-20261014-142325.
    python driver.py recorder-off: exit0,PID15920,sessão KIT14-run1471-recorder-off-20261014-142550.
    python driver.py without-kit: exit0,PID8740,sessão KIT14-run1471-without-kit-20261014-142726.
    python audit.py: exit0,readback do escopo limitado.
    python test_audit.py --mutant: exit1,6 testes/2 failures (falso positivo de janela).
    python test_audit.py: exit0,6 testes verdes após negativo.
    python gate.py rstv-full: exit1,FALHOU_ACEITE_INCOMPLETO sobre prova REAL.
    python gate.py bounded: exit0,PASSOU_ESCOPO_LIMITADO;task_accepted=false.

Paths reais dos comandos usam prefixo scratch/kit/KIT-14-run1471/ desde a raiz do repo. Contra-provas mutam somente memória/arquivos descartáveis, nunca prova runtime original/produto.

ON/OFF: mesmos assemblies5 plugins; configuração resultante BepInEx confirma Core/Adapter true/true versus false/false. API Safety.EnableHooks=false nos três casos, explicitamente; plumbing UI é independente desses hooks opcionais. Ambiente cfg herdado KIT14-run1442-disposable permaneceu; sessão e caminhos são run1471 e essa diferença não é escondida.

Sem kit: BepInEx lista exatamente2 plugins (API/RSTV),15/15 patches RSTV, nenhum instrumento. Comprova carregamento/patches sem dependência do kit, NÃO comportamento da janela nem ausência do host Hermes ativo. Não li/usei credenciais; isso não é teste autônomo com Hermes desligado.

## 4. Performance: dados crus, sem limiares/causalidade

Decisão B de10/10 respeitada. Select Party OCIOSA, tentativas3000..3600,21 marcadores por intervalo, frameCount/realtime reais:

| Medida | Recorder ON | Recorder OFF |
|---|---:|---:|
| Frames de início/fim |1112/1312|1157/1357|
| Realtime de início/fim, s |33.111/38.445|32.039/37.372|
| Frames/duração do intervalo |200/5.334s|200/5.333s|
| FPS médio do intervalo |37.495313|37.502344|
| ms/frame médio do intervalo |26.670|26.665|
| Pico WorkingSet64, bytes, boot inteiro |2136485888|2138525696|
| Pico PrivateMemorySize64, bytes, boot inteiro |3299631104|3282313216|
| Amostras de memória, boot inteiro |27|22|
| Duração boot observada, s |64.547443|52.932820|
| Bytes persistidos da pasta probe |3216251|3209309|
| Recorder eventos gerais/passivos |1/0|0/ausente|

FPS é delta frames/delta realtime; ticks do probe NÃO são frames. Endpoints arredondados em ms. Sem distribuição por frame/p95; sem counters I/O do disco. Memória inclui loading, não corresponde à janela pareada. Bytes são artefatos persistidos (PNG/JSON/markers), não só recorder nem I/O total. Personagem descartável tem nome aleatório entre boots, sem repetição estatística. Recorder ON teve zero passivo; NÃO medir como custo de recorder em atividade nem concluir overhead nulo pelo número parecido. Cenário RSTV real/performance ativa permanece não exercitado.

## 5. Integridade/restauração e inspeção visual

Cada boot registrou snapshots115 arquivos dados reais/53 perfil/5 outro jogo iguais antes/depois, zero novos/removidos/alterados, e export PlayerPrefs igual. Auditor independente do driver recalculou bytes/SHA256 sobre árvores atuais contra último snapshot IMEDIATO:115/53/5 intactos. Não comparar com snapshot antigo nem reverter deriva legítima do dono.

Readback final14:35 BRT: GAME_PROCESS_COUNT=0; dados LinkType=null/Target=[]; backup Stolen Realm.kit16-real ausente; perfis/dados descartáveis removidos; front-unica status:lock ausente/disponível. git diff --check e cached --check:exit0 (warning CRLF no WIP documental preexistente, preservado).

Cloud app1330000 em sharedconfig.vdf:toggle0 antes/durante/depois. Não alterei toggle. NÃO religa ao fim porque já estava OFF no início; religamento da campanha permanece residual operacional. Steam escreveu remotecache mesmo OFF; mtime mudou. Não alegar estado remoto/cache imutáveis.

Player.log: zero padrões Error/Fatal e exceções nomeadas procuradas, zero Screen/Window position out of view frustum;1 advertência Convex Mesh e1 DontDestroyOnLoad por boot. Padrões exatos gravados em verification.json; não afirmar log totalmente limpo.

PNG run1442 e ON/run1471 visualmente lidos: Select Party, personagemLv1 disponível, party vazia, sem loading/Skills/janela RSTV. PNG ON mostra Peyton. Não é revisão UI/UX do viewer nem prova clique físico.

## 6. Cobertura por critério

- Binários identificados/carga RSTV+API:PASSOU escopo limitado; loaded hash RSTV/pacote novo:NAO_EXERCITADO.
- Navegação handlers Play/Roguelike/Accept:PASSOU até Select Party; superfície RSTV:NAO_EXERCITADO.
- Clique físico→janela→conteúdo/tooltip→PNG/relatório:NAO_EXERCITADO; PNG nativo não fecha a cadeia.
- Marcar problema/exportar e Runner positivo/negativo runtime:NAO_EXERCITADO.
- Recorder passivo:NAO_EXERCITADO (ON zero), não aprovado.
- Mod sem kit:PASSOU carga/patches; comportamento funcional:NAO_EXERCITADO.
- Básico sem Hermes/IA/credenciais:NAO_EXERCITADO como campanha autônoma.
- Install/remove/rollback:PASSOU perfil temporário/snapshots; update/rollback de versão/pacote:NAO_EXERCITADO.
- Saves reais intactos:PASSOU nesta campanha, com readback independente.
- Performance ON/OFF:COLETA_EXPLORATORIA na tela ociosa; recorder ativo/mesma janela RSTV:NAO_EXERCITADO.
- Segundo ambiente:NAO_EXERCITADO; perfil temporário nesta máquina não prova portabilidade.
- Revisão independente/visual/aceite final/publicação:pendentes, não derivados dos verdes limitados.

Avaliador canônico CIC3 RSTV executado com lista vazia de observações da janela (porque ela não abriu), identidade do probe identificada:7/7 NAO_EXERCITADO. Não passar textos de menu como viewer para obter verdes irrelevantes.

## 7. Bloqueio e próximo passo

Não existe Button de seleção de personagem na rota atual; driver só mapeia Button.onClick. É lacuna TÉCNICA de instrumento/rota, não nova autorização de runtime nem defeito comprovado do mod. Clique OS não permitido nesta sessão headless; não tentar contorno.

O próximo trabalho é extensão do driver por handler real do seletor/entrada na run, revisão independente, prova de recorder/Runner/mark-export e campanha autônoma. Perfil listado: somente default; não inventar especialista, alterar modelos ou atribuir o follow-up ao próprio coletor. Operador deve rotear essa frente separada. Depois disso, residual genuinamente humano é clique físico e julgamento UI/UX/aceite. Roteiro dirigido:docs/automacao/KIT-14-runbook-residual-run1471.md.

KIT14R precriado permanece dependente; não concluir qualificação incompleta para liberá-lo. Esta entrega parcial não é revisão independente nem DoD.

## 8. Artefatos/hashes

Raiz provas:C:/dev/stolen-realm/scratch/kit/KIT-14-run1471. Checkpoints57..64. Auditor verification.json SHA25606cc53c3a914469ca1a698497d5df09be870913b532d28f973a717d9bf7f9d90. Driver638511b3af5872717fa2ad2f3905d4454eead81b3064ef9bb5a5ba2f3bec15c4; auditor119f0b0bdca33ac6db353de7c2925b0f65d614cd8d7a8f1d1c0e29435cb82a6b.

Pacote local de evidências e selo serão gravados nesta raiz com seleção explícita, sem dados pessoais/.reg/baselines privados/DLL proprietárias. O selo fornece tamanho/SHA256 e CRC do pacote, sem alegar pacote de release ou upload remoto.
