# ORG-R4 — documentação/política, parte 01

Tarefa t_6b569699; execução em 11/10/2026. Baseline: 94d39e6af737ccbd6d6cd1901202e6e2f514804e, branch ci-validate-test. Veredito desta fotografia: POLÍTICA IMPLEMENTADA, ACEITE GLOBAL BLOQUEADO no repo principal. Não liberar o gate original t_c00ce910 como verde enquanto a falha local abaixo não tiver decisão/saneamento e nova prova.

## Entrega e escopo nominal

Criado docs/ESTRUTURA.md: layout canônico dos seis mods na raiz e API própria; separação de fonte/dataset/evidência/cache/estado privado; release/mods.json versionado; dist com somente .gitkeep tracked; lib privada; worktrees Git-managed; scratch privado com apenas shim legado tracked. Guia de novo mod/frente, versões alinhadas, API Release antes de RSTV, deploy opt-in, retenção/restauração prévia e proteção de terceiros documentados.

Em docs/README.md foi acrescentada somente a linha de link ativo para ESTRUTURA na tabela inicial. O restante da curadoria/ritual e dos links da implementação E2 permanece intacto. Não há nova migração, exclusão ou atualização do auditor/detector/guarda. Este relatório é NOVO; relatórios históricos ORG-R1/R2/R3/limpeza, fotografias e seus hashes não foram reescritos.

## Bancada e automação executada

Workspace: C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_6b569699. Clone independente doc-clean01, checkout limpo de 94d39e6, core.autocrlf=false. Copiados privadamente apenas lib para compilar e os documentos desta frente; nenhuma DLL de build antigo foi copiada. Documentos adicionados nominalmente ao índice da cópia para a auditoria realmente lê-los. Bibliotecas do jogo e pacotes não compõem as evidências entregues.

Scripts locais da bancada: doc_setup01.py, doc_validate01.py e doc_continue01.py. São instrumentos deste workspace, não ferramentas novas do repositório. Ambiente executado: Python 3.14.7, .NET SDK 6.0.428, Git Bash por caminho absoluto, PYTHONDONTWRITEBYTECODE=1. Nenhum run remoto/Ubuntu/Python 3.11 foi alegado.

Primeira rodada registrada em proofs01/validation-results01.json: 45 subprocessos, 43 com RC=0 e dois com RC=1 (guarda ampla e release-check normal no donor). Esse total é desta rodada ANTES do relatório, não uma contagem permanente de checks ou uma declaração de verde global.

- Clone: todos os blocos run de validate.yml foram extraídos e executados sem reescrever suas condições, passos 0–10 inclusive 7b. Sem DLL, guarda do empacotador validou descoberta. Após API + seis builds Release sem deploy, o MESMO bloco rodou com DLL e gerou seis ZIPs somente na cópia. Estrutura de cinco membros e DLL igual à compilada foram conferidas por Python. audita_docs, guarda de deploy e release-check normal do clone: RC=0.
- Repo principal: passos 0–8 inclusive 7b executados, todos RC=0; audita_docs pré-stage RC=0. API e os seis projetos tracked da raiz construídos em Release com -p:DeployToBepInEx=false: RC=0. Empacotador --so-conferir RC=0; o ramo que escreve ZIPs ficou somente na cópia para não sobrescrever os pacotes preservados de dist.
- Antes dos builds diretos do principal, diagnóstico por analisa_arquivo da guarda REAL sobre Directory.Build.props, seis projetos tracked e projetos api: zero achados. Isso só delimita os projetos mantidos que foram compilados; NÃO dispensa nem transforma em verde a guarda ampla que falhou.

Comandos de build executados em cada árvore:

    dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=false --nologo
    dotnet build <Mod>/<Mod>.csproj -c Release -p:DeployToBepInEx=false --nologo
    bash tools/release-check.sh

Mods construídos: BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger e RoguelikeSkillTreeVisualizer. O harness ReloadProbe é local gitignored/não versionado e foi preservado. A asserção inicial que esperava seis em glob físico encontrou o harness adicional e parou ANTES dos builds; o script de bancada passou a selecionar os seis pelo índice Git. Nenhuma ferramenta do projeto foi modificada para isso.

A auditoria/segredos depois da inclusão nominal deste relatório e da política no principal e na cópia são condição do commit; seus argv/RC/logs ficam no registro final-validation01.json, separado do total da primeira rodada. O índice da frente deve conter somente docs/ESTRUTURA.md, docs/README.md e este arquivo.

## Bloqueio real: guarda varre snapshots privados

O principal não está globalmente verde: tools/check_deploy_optin.py varre os projetos físicos inclusive scratch/kit, sem podar essa árvore privada (analisa_raiz, linhas 155–159). O conteúdo da guarda é igual ao HEAD; ela não foi alterada pela documentação. Há três achados preservados, anteriores a esta tarefa:

| Caminho privado | Achado | mtime local medido |
|---|---|---|
| scratch/kit/KIT-14-run699/deploy-negative/ruim.csproj | isca de deploy sem Condition | 10/10/2026 13:11:55 -03:00 |
| scratch/kit/KIT-14-run710/deploy-negative/ruim.csproj | isca de deploy sem Condition | 10/10/2026 17:46:55 -03:00 |
| scratch/kit/KIT-14-run699/instalacao-local-resume/.kit-rstv-backups/20261010-131456-355-33328-0001/components/adapter/KIT04Adapter.SR.csproj | backup com XML inválido | 10/10/2026 13:14:56 -03:00 |

Guarda ampla RC=1, confirmada pelo release-check NORMAL real RC=1 no principal: passo 3 BUILD bloqueado pela guarda, sem builds dentro desse script. Os builds diretos acima foram executados separadamente, não são prova de sucesso do passo 3. No clone sem scratch privado a mesma guarda e o release-check passaram. Não repetir a alegação upstream de verde como se cobrisse o estado físico deste donor.

Os dois ruim.csproj têm SHA-256 9d32e5619fa2f8307819138f67e6023cbb25a181fa6dedbfaafd71c0b8ac5429; o backup tem SHA-256 32e6f75e7a4336ce36499dcc7e86b4b92e4fa685555086f1141900d9ff24ab98. Caminho, tamanho, mtime e hash estão em donor-private-fixtures01.json. Não apagar/mover snapshots, editar iscas para passar, alterar guarda ou invocar waiver nesta frente. Uma decisão de saneamento do escopo da guarda deve preservar a capacidade de pegar deploy indevido e provar o caso negativo, sem liberar remoção de entregáveis.

O único perfil existente retornado por hermes profile list foi default. Não inventar assignee especialista nem criar cartão duplicado de R4; registrar necessidade de decisão no board e bloquear este aceite por needs_input. O gate original fica dependente, não é fechado por esta implementação parcial.

## Preservação e limites

Fotografia inicial donor-before.json: 1.646 arquivos tracked, dois fontes AUT5 modificados e cinco documentos locais pendentes de outras frentes. Proteções fotografadas por SHA-256: lib (16 arquivos), dist principal (28), plugins do perfil (21), scratch/backups (34) e screenshots locais. Esses números pertencem ao baseline datado, não à política permanente.

A conferência intermediária após os checks encontrou somente docs/README.md diferente no conjunto tracked original; nenhuma edição alheia mudou. A prova final de preservação deve comparar novamente o conjunto completo e recusar alteração/remoção fora dos três documentos nominais, incluindo ferramentas, cs/csproj/workflows, EV-R1, fotografias e perfil. Arquivo ignored não foi tratado como lixo.

Sem git add -A, commit -a, push, publicação, alteração de ignore, deploy, lançamento/encerramento de jogo ou remoção adicional de caches. Nenhum entregável/terceiro foi eliminado ou redistribuído. PYTHONDONTWRITEBYTECODE evita recriação desta rodada, sem afirmar que caches de outras frentes não possam reaparecer.

Runtime ui.localized: NAO_EXERCITADO; ciclo do jogo: NÃO RODOU; conferência visual humana: PENDENTE. Prova offline --prova tem 11 testes, zero falhas, mas fixture não substitui jogo. Release-check principal REPROVADO e clone APROVADO apenas na automação; nenhum dos dois autoriza release pronto.
