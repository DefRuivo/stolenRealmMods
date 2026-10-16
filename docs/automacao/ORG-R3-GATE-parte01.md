# ORG-R3 — gate independente, parte 01

Tarefa t_873a563d; conferência em 11/10/2026. Implementação recebida de t_c299dd97: commit 30c1cba4239bcae755e5f7fe01ae4f5c4eea5af5. Veredito: ACEITO no escopo de organização. Este gate não repete a migração; a política final pertence a t_6b569699, e o fechamento da limpeza/política a t_c00ce910.

## Escopo e evidência independente

O plano ORG-R1 partes 01..04 aprovou somente a promoção de scratch/test-cycle.sh para tools/test-cycle.sh, conservando o shim legado tracked e o screenshot privado/opcional. Nenhuma nova reorganização foi feita neste gate.

Foi criado um clone próprio, sem outputs de build copiados, com core.autocrlf=false e checkout limpo do commit exato recebido. Bancada: %USERPROFILE%/AppData/Local/hermes/kanban/workspaces/t_873a563d/gate-clean01. As referências locais de lib foram copiadas privadamente para compilar; não integram a entrega nem foram redistribuídas.

O diff do commit recebido contém oito caminhos nominais, zero deleções e nenhuma alteração em fontes C#, projetos ou workflows. Git reconhece C078 de scratch para tools: a origem continua existindo por contrato, agora com cinco linhas de delegação. O handoff registra a execução de git mv antes de recriar o shim; Git guarda os snapshots, não o comando executado. Conferi a continuidade do conteúdo e do histórico, sem alegar que o diff sozinho prova a chamada git mv.

A comparação direta do script promovido com a versão anterior mostrou somente: comandos de uso atualizados, resolução da pasta do script/repo e procura do screenshot na pasta privada. Os trechos de limpeza de log, lançamento, espera, filtro e encerramento ficaram idênticos. Não foi executado o ciclo real.

## Referências antes/depois, reproduzidas por revisão Git

Comandos executados para cada revisão (30c1cba^ e 30c1cba), preservados nos logs de reference-before-after02.json:

    git -C C:/dev/stolen-realm grep -n -I -F 'scratch/test-cycle.sh' <revisao> -- .
    git -C C:/dev/stolen-realm grep -n -I -F 'scratch\test-cycle.sh' <revisao> -- .
    git -C C:/dev/stolen-realm grep -n -I -F 'scratch\\test-cycle.sh' <revisao> -- .
    git -C C:/dev/stolen-realm grep -n -I -F 'scratch\\\\test-cycle.sh' <revisao> -- .

A união das linhas foi deduplicada programaticamente: antes, 34 linhas em 19 arquivos; depois, 31 linhas em 16 arquivos. Uma busca independente sobre git ls-files com regex de separadores também retornou 31 linhas em 16 arquivos. O quarto comando cobre a busca escapada citada no próprio relatório de execução; sem ele a busca literal retorna 30, não 31. Os dois resultados e a correção instrumental foram conservados, sem ocultar a diferença.

Classificação das 31 linhas do commit recebido: duas de compatibilidade (.gitignore e explicação do shim em docs/README.md), sete históricas/congeladas e 22 de plano/evidência. Zero consumidores operacionais antigos em tools, workflows ou projetos. Os comandos ativos nos documentos de ambiente, índice e cobertura usam tools. Ambos os caminhos existem no commit; nenhum consumidor mantido aponta para destino ausente. Esta contagem é da revisão 30c1cba, antes deste relatório, não uma promessa de contagem permanente.

## Contrato exercitado sem jogo, em bancada nova

Oito de oito casos passaram em offline-contract01; resultados em offline-eight-tests.json. O shim real foi copiado para a bancada e seu destino substituído por stub que retorna 37. Nenhum script de ciclo real foi chamado.

- Shim desde a raiz e desde outra pasta: argumentos vazios, espaços, Unicode, pipe, metacaracteres, caminho Windows e LF interno preservados; cwd, ambiente e retorno 37 preservados.
- Shim sem argumentos: argc zero e retorno 37.
- Entrada canônica contra o mesmo stub: contrato equivalente.
- Screenshot default presente em scratch: parâmetros corretos para a pasta privada.
- Default ausente com isca em tools: captura pulada, sem procurar junto da implementação.
- Override privado com espaços: parâmetros na pasta alternativa.
- Override inexistente: captura pulada, sem requisito novo.

Os quatro testes de screenshot executaram somente o prefixo de resolução de caminhos e o bloco condicional extraídos do script. powershell.exe foi função stub. Nenhum screenshot real, Steam, taskkill, espera ou remoção de log foi executado. bash -n também passou no script promovido, shim e release-check.

## Builds e workflow reproduzidos localmente

gate_validate02.py executou 28 comandos, todos RC=0; argv, cwd, duração e logs integrais em gate-validation-results02.json. Ambiente local: Python 3.14.7, .NET SDK 6.0.428 e Git Bash. Não houve execução remota do GitHub Actions nem prova de Ubuntu/Python 3.11.

    dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=false --nologo
    dotnet build <Mod>/<Mod>.csproj -c Release -p:DeployToBepInEx=false --nologo
    bash tools/release-check.sh

API compilada primeiro, com Core/Hooks pelas referências de projeto. Release: BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger e RoguelikeSkillTreeVisualizer, seis de seis aprovados. release-check no fluxo normal também aprovou os seis builds Debug; guarda de deploy verde e perfil medido intacto. Nenhum --instalar-no-perfil.

Reproduzidos os comandos de validate.yml: ambiente, segredos, versões, patches, chaves, duplicadas, notas, compartilhada --estrito, cobertura --prova, metadados, empacotador guardado e audita_docs. Os dois ramos do bloco original do empacotador foram executados: sem DLL antes dos builds e com DLL depois. Foram gerados seis ZIPs apenas no dist da cópia; conferidos manifest, README, CHANGELOG, icon e DLL no caminho plugins correto, com conteúdo igual à DLL compilada.

Também passaram audita_docs e segredos no repo principal antes do relatório. A tentativa instrumental gate_validate01.py interrompeu na sanidade: a resolução Windows de bash selecionou WSL e não encontrou python. Não foi falha do repo. A abordagem mudou para o executável absoluto de Git Bash, sem alterar ferramenta do projeto; proofs01 conserva a falha e proofs02 os resultados válidos.

## Preservação, concorrência e limites do aceite

A fotografia upstream foi reconciliada com a fotografia inicial deste gate: seis arquivos antigos mudaram (somente os nominais da implementação), duas adições (script promovido e relatório da execução) e zero remoções. Snapshot histórico COR-AUT7-F2 preservado com SHA-256 d5f6fe068ae12e72f6f615148cdb72db628242552212cded836ac1b133dd7a2a. Nenhuma fotografia antiga foi reescrita, nem resultado de suite cacheada tratado como prova nova.

Durante a conferência apareceu o commit concorrente 11313e3 (INST-1), somente em .gitignore. O conteúdo ao vivo desse arquivo manteve o SHA-256 0548348fe87e973b36d2ec9edb68e6130c01258ae4ea3a1ffa3964f018f07720 da fotografia inicial; mudou de edição pendente para commit de outra frente. Não o reverti, editei nem incluí neste commit. As duas edições tracked AUT5 e os documentos locais pendentes foram preservados.

Inventário protegido medido neste gate: lib com 16 arquivos, dist principal com 28 e plugins do perfil com 21, além dos artefatos locais de screenshot. Comparação final de hashes integra as provas. EV-R1, fontes, projetos, snapshots e demais entregáveis não foram movidos nem removidos. Este gate versiona somente este relatório novo, com stage nominal; sem git add -A, commit -a, deploy, jogo, push ou publicação.

O release-check conserva corretamente as pendências de observação ui.localized, ciclo real e conferência humana. Seus avisos herdados (patches, chaves fora do censo e suspeitas compartilhadas) não foram convertidos em validação de runtime. ACEITO significa organização e automação verificadas, não release pronto nem validação visual em jogo.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
