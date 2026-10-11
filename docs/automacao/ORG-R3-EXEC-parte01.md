# ORG-R3 — execução E2, parte 01: test-cycle promovido com compatibilidade

Tarefa t_c299dd97; implementação para o gate preexistente t_873a563d. Execução em 11/10/2026, no repo C:/dev/stolen-realm, branch ci-validate-test, base ab125c158c167ab663e09c1245b025b8310dd2d6. Plano lido: ORG-R1 partes 01..04. Este documento é novo; não substitui fotografias anteriores.

## Mudança entregue, sem ampliar o escopo

Foi executado `git mv -- scratch/test-cycle.sh tools/test-cycle.sh`. A implementação mantida passou para tools/. Foi criado no caminho antigo um shim tracked de cinco linhas: resolve sua própria pasta, chama `exec bash` para o destino e encaminha `"$@"`. O diretório de trabalho de quem chama não precisa ser a raiz do repo. O código de saída do destino é preservado.

Os dois caminhos coexistem por projeto. Por isso a apresentação padrão do diff é origem modificada + destino adicionado; com `git diff --cached --find-copies --summary`, o Git reconheceu `copy {scratch => tools}/test-cycle.sh (78%)`. Não é uma segunda implementação: o arquivo antigo contém somente delegação. A chamada git mv foi executada antes de criar o shim; o histórico anterior permanece consultável.

Arquivos da frente, no mesmo commit nominal:

- scratch/test-cycle.sh: shim de compatibilidade.
- tools/test-cycle.sh: implementação promovida e lookup privado de screenshot corrigido.
- tools/release-check.sh: comentário, anúncio e chamada do modo explícito apontam para o destino.
- tools/check_omissao.py: instrução para produzir o log aponta para o destino.
- docs/AMBIENTE.md: as duas referências operacionais apontam para tools/.
- docs/README.md: três comandos corrigidos, nota de compatibilidade/captura opcional e entrada na tabela de ferramentas.
- docs/cobertura/README.md: comando de regeneração corrigido.
- docs/automacao/ORG-R3-EXEC-parte01.md: esta evidência incremental.

A exceção nominal para o shim no .gitignore foi conservada. O .gitignore já tinha alteração paralela não staged ao iniciar esta rodada; ela não foi editada nem incluída nesta frente. Também foram preservadas as alterações paralelas dos dois testes AUT5 e os documentos não tracked do dono/outras frentes. Nenhum .cs, .csproj ou workflow foi alterado.

## Captura opcional: contrato preservado

Na implementação antiga, SCRIPT_DIR era scratch/. Na promovida, SCRIPT_DIR é tools/; REPO_DIR sai da pasta-pai e ARTIFACT_DIR usa `${TEST_CYCLE_ARTIFACT_DIR:-$REPO_DIR/scratch}`. A condição de presença e os parâmetros `-File`/`-Path` usam ARTIFACT_DIR. Assim:

- O default continua procurando o script local privado shot.ps1 e escrevendo shot.png em scratch/.
- O script local continua opcional: ausência imprime a mensagem de pulo, sem exigir novo arquivo no clone.
- TEST_CYCLE_ARTIFACT_DIR permite outra pasta privada absoluta, inclusive com espaços.
- shot.ps1/shot.png não foram movidos, versionados nem executados nesta rodada.
- O restante do ciclo foi preservado; não houve refatoração do comportamento do jogo.

## Varredura antes/depois e classificação de todos os resíduos

Bancada local privada, fora de tools/: C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_c299dd97. O script de bancada audit_movement.py grava before-audit.json, after-audit.json e a saída integral de cada busca Git; textos grandes de JSON não foram reduzidos antes de registrar a prova. Apenas a apresentação no terminal foi limitada.

Comandos Git, repetidos antes e depois:

    git -C C:/dev/stolen-realm grep -n -I -F 'scratch/test-cycle.sh' -- .
    git -C C:/dev/stolen-realm grep -n -I -F 'scratch\test-cycle.sh' -- .
    git -C C:/dev/stolen-realm grep -n -I -F 'scratch\\test-cycle.sh' -- .

A busca adicional por expressão `scratch[/\\]+test-cycle\.sh` examinou textos locais e versionados, inclusive sandboxes privados em scratch/. Excluiu metadados .git/.worktrees e diretórios derivados bin/obj/node_modules/.vs/__pycache__; não abriu DLLs, assets ou ZIPs como fonte textual. Antes: 42.041 arquivos de texto examinados, 272 linhas em 149 arquivos, zero erros de leitura. Depois: 42.042 textos, 263 linhas em 145 arquivos, zero erros. Estas são fotografias ANTES de acrescentar este relatório; a própria evidência naturalmente introduz novas menções ao caminho antigo.

Na árvore versionada, as buscas registraram 34 linhas em 19 arquivos antes, e 25 linhas em 15 arquivos depois. As dez linhas operacionais antigas foram corrigidas; uma menção nova em docs/README.md explica expressamente o shim. Não se declara falsamente zero referências históricas.

Classificação do residual versionado pós-movimento, antes deste relatório:

| Categoria | Linhas | Caminhos / tratamento |
|---|---:|---|
| Compatibilidade, não chamada antiga ativa | 2 | .gitignore mantém a exceção nominal; docs/README.md explica o shim |
| Histórico INT-R1 | 3 | docs/automacao/INT-R1-parte02.md:17, parte03.md:13 e parte04.md:87; bytes preservados |
| Histórico de revisão | 3 | docs/cobertura/revisao/BT-18-passivas-inimigo.md:433, RV-8b-0f-propriedades.md:84 e RV-8b-2e-fechamento.md:45; comandos antigos resolvem pelo shim |
| Snapshot congelado | 1 | docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json; identidade/hashes da rodada preservados |
| Plano/fotografias ORG anteriores | 16 | ORG-R1 partes 01..04 e ORG-R2 EXEC/GATE parte01; explicam origem, destino, ignore e medições anteriores |

São 25 linhas. O único resultado contendo separador Windows nesta amostra foi a instrução de busca de ORG-R1-parte03.md:42; é plano histórico, não consumidor executável. Não houve referência antiga direta em .csproj nem .yml.

Residual privado adicional: 238 linhas fora do índice, das quais 235 em scratch/ e 3 no quadro interno KANBAN.md, que é local/gitignored, não documento entregue no repo. São históricos, cópias de sandbox, logs/notas locais e scripts privados compatíveis com o shim; não foram reescritos. As 235 incluem oito cópias privadas do snapshot congelado. Em particular, scratch/bct-test-cycle.sh:3 contém um comentário, e scratch/limpa-historico.sh:3,24 guarda referência/exclusão legada. O segundo é ferramenta local de rewrite histórico: NÃO foi executado e não recebe autorização por esta migração. O quadro interno também não foi usado para alterar tarefas desta frente.

Nenhum consumidor operacional mantido ficou apontando para caminho ausente. O comando novo é canônico; o legado é compatibilidade declarada, não autorização para executar o jogo nesta tarefa.

## Prova offline real, sem executar o ciclo

`bash -n` passou nos dois scripts test-cycle e em tools/release-check.sh. O script de bancada offline_contract_test.py, fora de tools/ no workspace acima, executou somente uma cópia do shim contra destino stub e um recorte seguro da inicialização/condicional de screenshot. Nenhum trecho de encerramento, lançamento, limpeza de log ou espera foi executado.

Resultado: oito casos passaram, registrados em offline-contract-results.json:

1. Shim desde a raiz da sandbox: oito argumentos, incluindo vazio, Unicode, espaços, pipe, metacaracteres, caminho Windows e LF interno; retorno 37 preservado.
2. Shim desde outra pasta: argumentos, ambiente e cwd preservados.
3. Shim sem argumentos: argc zero e retorno 37.
4. Entrada canônica contra o mesmo stub: contrato equivalente.
5. Script de captura presente na pasta scratch: stub PowerShell recebeu -File e -Path nessa pasta.
6. Script ausente em scratch, com isca na pasta tools: captura pulada; não procurou junto da implementação promovida.
7. Override privado com espaços: lookup e output na pasta alternativa.
8. Override inexistente: captura pulada, sem tornar o arquivo requisito.

Errata instrumental transparente: a primeira tentativa de passar LF interno diretamente por subprocess do Python para o argv Windows foi dividida na fronteira Python/Windows/Git Bash. Essa tentativa não é prova do shim. O transporte foi corrigido para entrada NUL-delimitada carregada por array Bash, e os oito casos foram exercitados novamente em sandbox nova; a implementação não foi alterada para mascarar o problema. PowerShell foi função stub, sem captura real.

## Identidade: nova fotografia, nunca reescrever snapshot antigo

A função real fotografia_suite de tools/automacao/estilo/estilo_atributos.py foi executada antes/depois, apenas para fotografar a árvore, sem rodar a suite nem runtime. Gerou novas evidências privadas before-fotografia.json e after-fotografia.json no workspace. A função cobre caminhos, não apenas conteúdo; sua lista de raízes já inclui tools/ e scratch/, portanto não exige mudar o instrumento de identidade.

Resultado: 46.687 → 46.688 entradas de arquivo. A nova chave é tools/test-cycle.sh. Mudaram os hashes de scratch/test-cycle.sh, tools/release-check.sh, tools/check_omissao.py e docs/cobertura/README.md, todos dentro da frente. Consequência: cache vinculado à fotografia anterior NÃO é prova da árvore promovida; deve ser invalidado/reproduzido quando se executar aquela suite. Não se atribuem resultados antigos à nova identidade, nem se afirma ter rodado toda a suite AUT-7 nesta tarefa.

O snapshot histórico suite-vinculo.json permaneceu com SHA-256 d5f6fe068ae12e72f6f615148cdb72db628242552212cded836ac1b133dd7a2a. INT-R1 e os relatos de revisão acima também ficaram byte a byte preservados.

## Builds e validação exercitados na cópia isolada

Clone Git novo em C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_c299dd97/isolated, com core.autocrlf=false, conteúdo tracked ao vivo copiado e shim explicitamente incluído no índice da cópia. Copiadas privadamente as 16 referências de lib/; nenhuma DLL de terceiro incluída na entrega. Não foram copiados outputs de build do repo principal. A cópia incorporou as edições tracked ao vivo do dono, sem escrevê-las de volta.

Ferramenta de bancada validate_isolated.py, fora de tools/ no workspace, gravou logs e registros de argv/exit/duração em validation-*.json. Comandos reais:

    dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=false --nologo
    dotnet build <Mod>/<Mod>.csproj -c Release -p:DeployToBepInEx=false --nologo
    bash tools/release-check.sh

A API foi compilada PRIMEIRO, construindo Core e Hooks pelas ProjectReference. Depois compilaram, em Release, BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger e RoguelikeSkillTreeVisualizer: seis de seis RC=0, nenhum erro de compilação. O release-check normal também compilou os seis em Debug, RC=0. Não foi usado --instalar-no-perfil.

Todos os comandos de validação do workflow .github/workflows/validate.yml foram reproduzidos localmente: segredos; versões; patches; chaves; duplicadas; notas; compartilhada --estrito; cobertura --prova; metadados de pacote; empacotador guardado; audita_docs. Todos retornaram 0. A guarda check_deploy_optin também retornou 0. O ramo sem DLL foi exercitado com --listar-nomes antes dos builds; o ramo com DLL produziu seis ZIPs reais apenas em dist/ da cópia isolada.

`python tools/audita_docs.py` terminou com nenhuma inconsistência. O relatório foi incluído nominalmente no índice da cópia para a conferência documental final antes do commit, não ocultado por ser novo. A entrega guarda logs reais, não uma execução remota inventada: Python local 3.14.7 / .NET SDK 6.0.428 / Git Bash; não houve run GitHub Actions nem prova de Ubuntu/Python 3.11 nesta rodada.

release-check-normal.txt: RC=0, APROVADO na automação, seis builds sem deploy, perfil medido intacto. Mantém pendentes, corretamente: observação ui.localized em jogo, ciclo e conferência humana. Os avisos herdados (duas observações de patches, quatro chaves fora do censo, doze suspeitas compartilhadas) não viraram prova de runtime.

## Preservação e handoff

O inventário SHA-256 comparou todos os caminhos originalmente tracked: apenas os seis arquivos antigos desta frente mudaram, mais a adição do destino. Nenhuma fonte C# mudou. Também foram comparados lib/ (16 arquivos), dist/ principal (28 arquivos), os artefatos opcionais de captura existentes e plugins do perfil (21 arquivos): conteúdo preservado. As três alterações tracked paralelas já existentes mantiveram seus hashes. Nenhum deploy, abertura/fechamento de jogo, remoção de LogOutput.log, push, publicação, movimento de EV-R1 ou limpeza de scratch inteiro.

Stage nominal, conferido com diff do índice e --check, sem git add -A nem commit -a. O commit exclusivo reúne movimento, shim, referências ativas e esta evidência. O gate t_873a563d recebe a implementação pronta para conferir independentemente: NÃO repetir git mv, NÃO reescrever fotografia histórica, NÃO abrir jogo por causa da conferência. A política final continua pertencendo ao cartão E4 após esse gate.
