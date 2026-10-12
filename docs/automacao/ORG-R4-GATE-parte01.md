# ORG-R4 — gate de limpeza e política, parte 01

Cartão t_c00ce910; revisão independente em 11/10/2026. Baseline principal e8efaca02e23a6ee2bd0d594aadc2d7e6806c48f, branch ci-validate-test. LIMPEZA E POLÍTICA CONFERIDAS; ACEITE GLOBAL NÃO LIBERADO: release-check normal do principal continua RC=1. Este relatório novo não altera fotografias anteriores nem implementa o saneamento de outra frente.

## 1. Commits e exclusão nominal conferidos

- ab125c1: somente docs/automacao/ORG-R4-LIMPA-parte01.md; e8efaca: somente docs/ESTRUTURA.md, docs/README.md e docs/automacao/ORG-R4-DOC-parte01.md. Ambos são ancestrais do baseline; conteúdo dos quatro caminhos conferido contra seus blobs Git e SHA-256 do disco. Zero reaplicações de limpeza ou migração neste gate.
- Manifesto nominal aprovado na evidência durável ORG-R1: 109 caches, 3.324.108 bytes históricos, todos com fonte. Conferência atual: 109 ausentes, 109 fontes presentes e 109 recompilações py_compile aprovadas em bancada nova, fora do repo. Nenhum .pyc tracked. Não foi feita nova remoção e a ausência medida não significa cache permanentemente proibido.
- Preservado tools/automacao/kit10/__pycache__/_red_mutante.cpython-314.pyc: 51.889 bytes, SHA-256 bd7ff71d95a921608aecd92ff7232a6a5280e59e1a0a2715f165228f69513ec4; fonte correspondente continua ausente. Não fabricar fonte nem classificar órfão como regenerável.
- Varredura literal dos 109 caminhos nos arquivos versionados de documentação/fonte/projetos/scripts/workflows: duas ocorrências, ambas na linha 29 do relatório histórico da limpeza; zero consumidores operacionais encontrados nesse escopo. As quatro menções ao órfão também estão em documentos históricos, não em imports de ferramenta.
- Inventário físico ORG-R1 de 57.619 caminhos versus disco: 109 ausências fora de .git, todas do manifesto; zero ausências não-pyc e zero caminhos ausentes fora da lista aprovada. Esta comparação revalida o escopo histórico, não atribui a este gate exclusões que o executante já realizou.
- Quatro fontes diferem da fotografia ORG-R1: tools/check_omissao.py, tools/check_padroes_segredo.py e os dois testes AUT5 já modificados no baseline deste gate. As duas primeiras têm alterações em commits posteriores ao plano; as outras duas são edições paralelas preservadas. Não declarar que todas as fontes ainda têm o hash de 15:11: os 1.756 hashes protegidos deste gate, medidos agora, ficaram iguais durante a bateria.

## 2. Política e decisões posteriores

A política em docs/ESTRUTURA.md cobre fonte/dado entregue/artefato/efêmero, layout canônico, ignore nominal, lib privada, dist, worktrees, shim legado, retenção/restauração, novo mod/frente, commit nominal e deploy opt-in. O índice docs/README.md tem link ativo; a conferência contra e8efaca preservou a curadoria existente. Não houve alteração em política, ignore, ferramentas, fontes ou projetos neste gate.

DECISÃO posterior do dono em 11/10/2026 supera a retenção integral de EV-R1 descrita no plano/política anterior: manter docs/cobertura/EV-R1/eventos.json versionado; tirar somente do índice e ignorar docs/cobertura/EV-R1/catalogo-referencias.json e docs/cobertura/EV-R1/EV-R1-entrega.zip, SEM remover do disco. Execução pertence a ORG-R5-DADOS (t_b0ef7bc0), não a este gate; os três arquivos e os demais 30 arquivos do diretório foram preservados por hash. A política anterior não deve ser usada para contrariar a decisão do cartão R5.

## 3. Execução independente, sem jogo nem deploy

Bancada gate-clean01 no workspace t_c00ce910: clone sem hardlinks, checkout destacado do baseline, core.autocrlf=false. PYTHONDONTWRITEBYTECODE=1; Python 3.14.7; Git Bash por executável absoluto; SDK .NET 6.0.428. lib copiada privadamente somente para compilar; nenhuma DLL de build anterior copiada como prova, nenhuma referência de terceiro ou ZIP de pacote anexado às evidências.

Registro anterior a este relatório: 35 comandos concluídos, 33 RC=0 e dois RC=1 reais no principal. Os dois RC=1 são a guarda ampla de deploy e o release-check normal, não sucessos mascarados por serem falhas esperadas. Os comandos, argv, RC, duração, logs e hashes estão em validation-results01.json e continued-results01.json da bancada; verification-summary01.json agrega por código, não por contagem mental.

- Todos os 12 blocos normais run de .github/workflows/validate.yml extraídos e executados sem reescrever comandos/condições no clone: sanidade e passos 1–10, incluindo 7b, todos RC=0. Handler de falha não rodou; actions de checkout/setup não foram simuladas como run remoto.
- Ramo sem DLL do empacotador exercitado antes do build; zero .pyc gerado no clone pela bateria do workflow. Depois, mesmo bloco com DLL Release: RC=0, seis ZIPs somente no dist da cópia. Cinco membros esperados por ZIP, integridade e DLL byte-idêntica ao build conferidos programaticamente.
- API api/Plugin/RealmApi.csproj e seis mods da raiz compilados em Release em AMBAS as árvores: 14 builds diretos RC=0. API antes de RSTV; todos com -p:DeployToBepInEx=false e --nologo. Análise da guarda sobre os projetos mantidos não achou problema; isso NÃO dispensa a falha da varredura ampla. Nenhum fonte foi editado para compilar.
- Clone: release-check normal RC=0. Principal: audita_docs RC=0, check_segredos RC=0, empacotador --so-conferir RC=0 e git diff --check RC=0. O ramo que escreve pacotes ficou exclusivamente na bancada; dist principal preservado.
- O timeout externo de terminal encerrou a primeira chamada após 420 s, com 33 comandos completos já registrados; não é reprovação de check. Não havia processo gate_validate01 ativo na inspeção. A continuação numerada executou somente o release-check principal e diff-check faltantes, guardando saídas em arquivos novos; os logs completos anteriores não foram sobrescritos.

A inclusão nominal deste relatório requer nova auditoria/segredos no índice da cópia e no principal antes do commit; seus resultados ficam separados em final-results01.json, não incorporados retroativamente ao total de 35 acima.

## 4. Falha real e impedimento do grafo

O release-check principal chega ao passo 3 BUILD e REPROVA antes de construir: tools/check_deploy_optin.py encontra três projetos privados congelados. check_segredos passou; portanto este incidente não é achado de segredo. Paths exatos:

1. scratch/kit/KIT-14-run699/deploy-negative/ruim.csproj — alvo DeployToBepInEx sem Condition.
2. scratch/kit/KIT-14-run710/deploy-negative/ruim.csproj — mesma isca sem Condition.
3. scratch/kit/KIT-14-run699/instalacao-local-resume/.kit-rstv-backups/20261010-131456-355-33328-0001/components/adapter/KIT04Adapter.SR.csproj — XML inválido.

Os três permaneceram intactos. Não ignorar scratch por curinga, apagar provas, editar iscas, dispensar a guarda ou chamar o sucesso do clone de verde do principal. A correção nominal e contra-prova pertencem ao cartão preexistente ORG-R6-GUARDA (t_8331c57c). Sua redação menciona segredos, mas a evidência real delimita guarda de DEPLOY; o executor deve provar também que um alvo sem opt-in num caminho comum continua detectado, sem enfraquecer o detector de segredos.

Grafo vivo conferido por kanban_show: R4 -> R5-DADOS -> R6-GUARDA; R6 só fica pronto depois de R5, que espera este gate. A liberação administrativa concedida ao escopo documental E4 não autoriza declarar o gate global R4 verde. A ordem atual impede executar o saneamento antes deste aceite. Necessária decisão do operador: reordenar o R6 para rodar antes do aceite R4, ou autorizar explicitamente encerramento deste cartão apenas como conferência de limpeza/política, mantendo a falha global registrada e delegada. Não criar tarefa duplicada, não mudar dependências nem executar R5/R6 fora de escopo.

## 5. Preservação e limites

Fotografia inicial: 1.648 tracked, dois testes AUT5 modificados e cinco documentos pendentes alheios; índice vazio. Depois da bateria, 1.756 arquivos protegidos com hashes iguais, status e worktree list iguais. Proteções incluem lib (16), dist principal (28), EV-R1 (30), scratch/backups (34), plugins do perfil (21), screenshots presentes e as três iscas. Esses totais são da fotografia datada, não promessas de contagem permanente.

Uma frente = um commit somente deste relatório. Sem git add -A, commit -a, push, deploy, jogo, remoção de arquivo/árvore, alterações na política anterior ou saneamento de ferramenta. Provas ORG-R1 e E4 conferidas por integridade do ZIP e hash; snapshots históricos imutáveis. CI remoto/Ubuntu/Python 3.11 não executados; runtime ui.localized, ciclo e conferência humana continuam pendentes.

Veredito: limpeza e política aceitas na revisão; workflow local do clone e builds aprovados. PRINCIPAL NÃO GLOBALMENTE VERDE e gate R4 NÃO LIBERADO até decisão/saneamento e nova prova. Não completar o cartão como se todos os critérios tivessem passado.
