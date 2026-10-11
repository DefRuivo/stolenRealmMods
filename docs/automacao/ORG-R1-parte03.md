# ORG-R1 — parte 03: erratas de validação, movimentos e execução roteada

Tarefa t_adbb8f0d. Complemento incremental das partes 01 e 02; não as sobrescreve. Auditoria sem reorganização de C:/dev/stolen-realm. Quando houver conflito, esta parte prevalece sobre a parte 02.

## Errata E1: cache sem fonte NÃO é descarte autorizado

A parte 02 mediu 110 arquivos *.pyc (3.375.997 bytes) e condicionou descarte à fonte presente. A verificação caminho a caminho encontrou UMA exceção: tools/automacao/kit10/__pycache__/_red_mutante.cpython-314.pyc, 51.889 bytes, SHA-256 bd7ff71d95a921608aecd92ff7232a6a5280e59e1a0a2715f165228f69513ec4. O correspondente tools/automacao/kit10/_red_mutante.py não existe. PRESERVAR esse bytecode. Autorização final E1: 109 arquivos, 3.324.108 bytes, 0 tracked, todos com fonte correspondente existente. Na tabela da parte 02 o grupo kit10/ tem 3 arquivos/132.124 bytes medidos; APROVADOS são só 2/80.235 bytes. Demais grupos permanecem como medidos. Não criar fonte inventado nem assumir que mutante é lixo. cleanup-manifest.json registra source_exists por item; o executante deve filtrar e revalidar antes de apagar.

## .gitignore validado só na cópia isolada

verify_plan.py aplicou o texto da parte 02 APENAS no clone de teste. `git ls-files -ci --exclude-standard` caiu de 33 para 0 sem remover arquivo do índice. A verificação NUL-delimitada de check-ignore --no-index -v -z --stdin validou 39 caminhos: 34 re-inclusões (script + 32 logs + dist/.gitkeep), 5 ignores (dump scratch, worktree, banco isca, nul, lib). Resultado em ignore-simulation-v2.json, exit 0, asserts satisfeitos.

Errata instrumental: a primeira versão, via subprocess text=True e linhas LF, chegou ao Git Windows com CR nos nomes, produzindo 6 linhas sobre caminhos incorretos. ignore-simulation.txt é tentativa INVALIDA para provar exceções. Mudança de abordagem para bytes NUL resolveu; somente v2 é aceite. Não levar CR literal nos comandos do worker.

Consumidores confirmados por basename em log-consumers.json: aut5/test_aut5.py:28 aponta a fixture log-completo.log; tools/testes/regras_bct.py:1196 aponta bf-shaders-em-jogo.log; todos os 32 logs têm referências na amostra versionada. Os logs tools/testes/ são citados como provas históricas, não todos como inputs de parser. Retenção permanece sem desindexar. Os seis arquivos de tools/fixtures/ incluem 5 logs e 1 JSON; portanto são 6 fixtures, NÃO 6 logs. Os 32 logs totais dividem-se em 1 aut5 + 5 fixtures + 26 tools/testes/. Correção das contagens narrativas da parte 02: onde diz 25 logs em tools/testes/, leia 26. O bloco de 32 exceções por caminho da parte 02 está correto.

## Movimento M1, único aprovado

Origem: scratch/test-cycle.sh (2.389 bytes tracked). Destino: tools/test-cycle.sh. Executar `git mv -- scratch/test-cycle.sh tools/test-cycle.sh`; não desindexar a origem antes do movimento. Em scratch/test-cycle.sh criar shim de compatibilidade versionado que encaminha TODOS os argumentos ao destino usando exec. A exceção no .gitignore da parte 02 mantém apenas esse shim, não dados privados.

Detalhe que impede um mv cego: scratch/test-cycle.sh:8 e :52-53 derivam SCRIPT_DIR e procuram shot.ps1/shot.png ao lado do script. Esses dois arquivos são locais ignorados. Após promover a implementação, resolver lookup de screenshot pela pasta scratch da raiz OU por variável de diretório privado com default compatível. Não mover/versionar shot.ps1 e não transformar screenshot opcional em requisito. Testes de delegação devem usar stub offline, não executar o ciclo real que abre/fecha jogo e remove LogOutput.log.

### Varredura inicial e tratamento obrigatório por consumidor

references.json (fotografia ANTES dos relatórios ORG-R1): 20 linhas em 14 arquivos com scratch/test-cycle.sh; 17 linhas estão em caminhos tracked, 3 em scripts locais NT. Não houve referência direta a esse caminho em .csproj ou .yml na amostra. O worker deve refazer a busca após novas docs/edições do dono; esses números não são meta permanente.

| Caminho / linhas da fotografia | Tipo | Tratamento no MESMO commit de M1 |
|---|---|---|
| tools/release-check.sh:62,528,529 | comentário, anúncio e chamada executável | apontar para tools/test-cycle.sh; jamais usar modo instalar-no-perfil nesta frente |
| tools/check_omissao.py:109 | instrução operacional | apontar comando ao destino |
| docs/AMBIENTE.md:56,58 | guia atual | corrigir referência ativa |
| docs/README.md:95,241,247 | guia atual | corrigir os três comandos |
| docs/cobertura/README.md:67 | guia atual do censo | corrigir comando |
| docs/cobertura/revisao/BT-18-passivas-inimigo.md:433 | relato de revisão | preservar histórico; shim resolve execução antiga; classificar residual |
| docs/cobertura/revisao/RV-8b-0f-propriedades.md:84 | relato de revisão | mesma política histórica, shim resolve |
| docs/cobertura/revisao/RV-8b-2e-fechamento.md:45 | relato de revisão | mesma política histórica, shim resolve |
| docs/automacao/INT-R1-parte02.md:17; parte03.md:13; parte04.md:87 | fotografia histórica de harness local gitignored não versionado | preservar a fotografia; nova errata/nota de migração, sem recontar como estado atual |
| docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json:1 | identidade/hashes congelados da rodada | NÃO reescrever JSON/hash histórico; produzir fotografia NOVA quando for testar a árvore reorganizada |
| scratch/bct-test-cycle.sh:3 | comentário de script local NT | não sobrescrever fonte local sem escopo; shim evita comando quebrado |
| scratch/limpa-historico.sh:3,24 | script local NT de rewrite histórico | NÃO executar; deixar registrado como histórico, não autoriza limpar/rewrite |

Comando de referência a repetir: `git grep -n -I -F 'scratch/test-cycle.sh' -- .` e variante `scratch\\test-cycle.sh`, além de busca em fontes locais pertinentes e raízes docs/scripts/tools/.github/. Todo resultado residual deve ser classificado: shim, histórico, plano de movimento ou erro atual. Não alegar zero se os arquivos históricos preservados ainda citarem origem. Ao final, nenhum comando ativo aponta para lugar ausente; o shim é compatibilidade declarada, não implementação duplicada.

### Movimentos condicionais, NÃO delegados

- EV-R1 JSONs → subpasta dados/: demanda varrer quatro ocorrências de catalogo-referencias.json em quatro arquivos da amostra, índices/schema/guia, referências em documentos EV-R1 e leitores que só estão no ZIP; atualizar testes e repetir roundtrip. Não há autorização desta rodada.
- ZIP integral EV-R1 → arquivo privado durável: demanda atualizar docs/cobertura/EV-R1/ENTREGA-E-LOCALIZACAO.md:21,51 e relatórios de localização, verificar hash/restauração e decidir retenção; não basta link temporário. Proibido mover/desindexar/apagar agora.
- scratch inteiro → fora do repo: demanda 1.418 linhas/432 arquivos da amostra, scripts e contratos de identidade em tools/automacao/estilo/estilo_atributos.py:365. Já ignorado; não compensa quebra de caminho em massa. Adiado.
- aposentadoria do harness ReloadProbe gitignored não versionado: 153 linhas/91 arquivos na amostra, incluindo estilo_atributos.py:365, ferramentas de deploy/patches e testes que condicionam presença. Não remover fonte local nem ignorar consumidores por chamá-lo abandonado.
- worktree .worktrees/level-r2 → outro local: somente Git worktree move após consulta de estado/branch/merge; nenhuma referência operacional direta encontrada em tools/scripts/api/.github na amostra. `git status --short` nesse worktree saiu vazio na rodada; clean NÃO prova dispensável. Adiado.

## Baseline executado: já havia vermelho, não mascarar

Ambiente de teste: C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_adbb8f0d/baseline, clone Git independente com fontes tracked copiadas do estado ao vivo e lib/ local copiada privadamente. Python 3.14.7 / .NET SDK 6.0.428. Donor C:/dev/stolen-realm não recebeu build, deploy, pacote, mudanças de fonte, ignore, mv ou rm. source-hashes.json conferiu 1.628 hashes do donor antes/depois: ZERO mudanças durante os testes. Foram feitas cópias, não restauração sobre edições humanas.

| Comando / prova na cópia | Resultado real | Consequência |
|---|---|---|
| python tools/audita_docs.py | exit 1, 35 pendências antes de organização | saneamento documental necessário; não afirmar CI verde |
| python tools/check_deploy_optin.py | exit 0, 8 alvos com opt-in | builds isolados não pediram deploy |
| python tools/check_segredos.py | exit 1, entropia suspeita; nenhum padrão conhecido | triagem especializada antes de execução/publicação |
| python tools/check_versoes.py | exit 0, 6 mods alinhados | manter fontes/metadados |
| python tools/check_patches.py | exit 0, 2 avisos no snapshot com harness local não versionado | avisos não são erros; não refatorar patches nesta frente |
| python tools/check_fix_keys.py | exit 0, 298 chaves, 4 fora do censo como aviso | não confundir aviso com censo completo |
| python tools/check_dupes.py | exit 0 | nenhuma chave duplicada |
| python tools/check_notas_redundantes.py | exit 0 | relatório regenerado só na cópia |
| python tools/check_chave_compartilhada.py --estrito | exit 0 | relatório regenerado só na cópia |
| python tools/cobertura_ui_localized.py --prova | exit 0, 11 testes, 0 failures | offline, não comprova runtime |
| python .github/scripts/valida_pacotes.py | exit 0, 6 pacotes, 0 problemas | metadados alinhados |
| dotnet build dos seis mods, --nologo -c Release -p:DeployToBepInEx=false | 6/6 exit 0 depois de API própria | zero erros CS finais; warnings existentes preservados |
| dotnet build api/Plugin/RealmApi.csproj --nologo -c Release -p:DeployToBepInEx=false | exit 0, Core/Hooks/Plugin produzidos | PRÉ-REQUISITO antes do RSTV, não mover bin/API nem publicar DLL de terceiro |
| python tools/pack-thunderstore.py | exit 0, 6 zips só no dist/ da cópia, após API e RSTV | empacotamento local exercitado, sem envio |
| python tools/pack-thunderstore.py --listar-nomes | exit 0, seis nomes | caminho sem DLL do workflow exercitado como comando de descoberta |
| bash tools/release-check.sh, Git Bash correto, SEM flags | exit 1 no passo 0 por entropia | build/ciclo seguintes abortados; release não aprovado |
| bash -n scratch/test-cycle.sh | exit 0 | só sintaxe, nenhum ciclo foi aberto |
| python -B tools/automacao/aut5/test_aut5.py | exit 1, divergências de contrato/identidade | achado extra fora de validate.yml, não alterar instrumento congelado |

Limitações/erratas de execução: o primeiro build RSTV falhou com dois CS0246 por ausência de RealmApi no clone limpo. Releitura de RoguelikeSkillTreeVisualizer.csproj:75-83 mostrou pré-requisito já documentado. Compilar API e repetir RSTV resolveu, sem editar .csproj. O primeiro pack então sem DLL falhou; repetição após build completo passou. O primeiro release-check invocado pelo subprocess Python encontrou Windows bash/WSL em vez de Git Bash (cygpath ausente e alternate object path inválido): tentativa não vale como diagnóstico do repo. Reexecução pelo Git Bash do terminal confirmou a FALHA REAL de segredos no passo 0. Nada foi escondido no baseline-results.json: tentativas iniciais e logs corretivos separados acompanham evidências.

Não houve push nem execução GitHub Actions/Ubuntu Python 3.11. A verificação é dos comandos do workflow localmente, não de um run remoto. A guarda sem DLL foi conferida por --listar-nomes; o ramo com DLL foi empacotado de verdade na cópia. Audita_docs e segredos impedem dizer que validate.yml está verde; isso é HERDADO, anterior à organização, e foi roteado como pré-requisito real.

As 35 pendências documentais se dividem em 7 ferramentas de bancada mal classificadas, 1 link tools/automacao/kit15/README.md → primeiro-uso.md e 27 menções ao harness ReloadProbe gitignored não versionado. Não versionar ferramenta local para silenciar detector. Possíveis falsos positivos de entropia também exigem demonstração, não whitelist ampla.

## Cartões criados, pins e grafo real

Perfil default confirmado por `hermes profile list`. Pins por natureza verificados na skill hermes-agent (roteamento local do dono): deepseek-flash/deepseek para ação mecânica; gpt-6.1-sol/openai-codex para segurança, contratos e síntese. Não trocar pin por inferência automática de título.

| Frente nova | ID | Pin explícito | Pais efetivos |
|---|---|---|---|
| saneamento de segredos herdados | t_5c8f7f57 | gpt-6.1-sol / openai-codex | ORG-R1 t_adbb8f0d |
| saneamento de docs herdadas | t_d803c318 | gpt-6.1-sol / openai-codex | ORG-R1 t_adbb8f0d |
| gitignore + cached (0 remoções aprovadas) | t_f03077f4 | deepseek-flash / deepseek | ORG-R1 + t_5c8f7f57 + t_d803c318 |
| movimento test-cycle + shim/referências | t_c299dd97 | gpt-6.1-sol / openai-codex | ORG-R1 + R2 t_a5b7b22a |
| limpeza nominal de 109 caches | t_8dba747f | deepseek-flash / deepseek | ORG-R1 + R2 t_a5b7b22a |
| política/documentação final | t_6b569699 | gpt-6.1-sol / openai-codex | ORG-R1 + R3 t_873a563d + t_8dba747f |
| diagnóstico AUT5, sem tocar probe congelado | t_ceceef6b | gpt-6.1-sol / openai-codex | ORG-R1, independente da organização |

Três cartões de execução R2/R3/R4 JÁ tinham sido criados pelo dono. Para cumprir decomposição em quatro frentes sem execução duplicada, foram preservados como gates de conferência/integração do trabalho específico recebido, com comentário explícito e dependência real, não prose-only:

- R2 t_a5b7b22a: pais R0 t_071b445f + ORG-R1 + E1 t_f03077f4. Confere o único commit recebido, sem aplicar .gitignore duas vezes.
- R3 t_873a563d: pais ORG-R1 + R2 + E2 t_c299dd97. Confere movimento/referências/build, sem segundo git mv.
- R4 t_c00ce910: pais ORG-R1 + E3 t_8dba747f + E4 t_6b569699. Confere limpeza/política, sem nova exclusão. E4 depende de R3, então o fechamento final é serial ao movimento.

## Ordem segura e paralelismo

1. Concluir este plano e preservar documentos/evidências. Não executar reorganização no cartão ORG-R1.
2. SEG e DOC de baseline podem trabalhar em paralelo, possuindo arquivos diferentes. Mantêm provas históricas e testes negativos. Se suspeita de segredo real, bloqueio humano/rotação; sem publicar.
3. E1 aplica somente .gitignore e registra 0 cached removidos, um commit nominal. R2 confere o resultado antes de liberar próximos passos.
4. E2 move script/corrige refs ativas; E3 remove só lista de caches com fonte presente. Podem executar em paralelo, mas testes de ambos devem ser isolados, com bytecode desligado, para não regenerar cache enquanto E3 limpa. Nenhum dos dois toca o arquivo de posse do outro.
5. R3 verifica E2. E4 só começa depois de R3 e E3, para documentar layout realmente exercitado, não desejado. R4 confere as duas entregas e as validações finais.
6. A cada frente, um commit exclusivo, com `git add -- <lista-nominal>` e diff do índice antes de commit. NUNCA git add -A ou git commit -a. Se o dono alterou arquivo no intervalo, reler/mesclar, não restaurar nem sobrescrever. Não push automático.
7. Builds em ordem API própria → seis mods, sempre DeployToBepInEx=false; ferramentas validate.yml e audita_docs devem terminar 0; release-check normal, nunca instalar-no-perfil. Separar runtime/humano pendente de prova offline.

Nenhum cartão pode ampliar exclusão a backups/entregas/zip/worktree/probe/DLL privada por economia de espaço. Movimentos condicionais permanecem pendentes de decisão registrada. Não existe autorização de excluir 4 GiB de scratch só porque a tabela mostra esse tamanho.
