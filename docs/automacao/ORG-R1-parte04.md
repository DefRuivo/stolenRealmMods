# ORG-R1 — parte 04: fechamento do plano e critérios de passagem

Tarefa t_adbb8f0d, 11/10/2026. Esta parte é aditiva; partes 01..03 permanecem como registros da investigação, inclusive suas erratas. Nada de reorganização foi executado no repo C:/dev/stolen-realm. Só foram adicionados os quatro relatórios ORG-R1; dados de medição e testes foram produzidos na bancada do workspace da tarefa.

## Decisão final que vale para os executantes

- Layout: seis mods na raiz; api/, tools/, scripts/, docs/, release/mods.json mantidos. Lib privada e dist local permanecem nos lugares atuais.
- .gitignore: bloco nominal da parte 02; 32 exceções de logs e shim test-cycle, .worktrees local, banco-isca e nul. Nenhuma regra global nova de DLL/ZIP/JSON/DB e nenhuma redução da proteção de segredos.
- Remoções aprovadas do índice (`git rm --cached`): ZERO. A auditoria encontrou 0 bin/obj, DLL/PDB, banco, backups ou caches tracked. Os 33 tracked que casam com ignore são ferramenta + fixtures/provas e devem permanecer tracked.
- Movimento aprovado: UM, scratch/test-cycle.sh → tools/test-cycle.sh, com shim legado, referências ativas corrigidas e screenshot privado ainda opcional. Não executar o jogo para testar movimento.
- Exclusão aprovada: 109 caches *.pyc com fonte existente, 3.324.108 bytes, listados por caminho/hash/fonte no manifesto. Excluir SOMENTE os 109, não árvores. PRESERVAR tools/automacao/kit10/__pycache__/_red_mutante.cpython-314.pyc (51.889 bytes) sem fonte correspondente.
- Exclusão/movimento/desindexação de docs/cobertura/EV-R1/, backups, pacotes dist, .worktrees, lib, fontes locais de harness gitignored não versionado e instrumentos congelados: ZERO autorizados. Candidato não é permissão.
- Política final fica em docs/ESTRUTURA.md, escrita depois dos movimentos/limpeza, com guia para novo mod/frente, retenção de entregáveis e distinção entre dataset/evidência/cache.

Contagem corrigida dos logs: 1 tools/automacao/aut5/fixtures/ + 5 tools/fixtures/ + 26 tools/testes/ = 32. A lista nominal da parte 02 corresponde ao conjunto auditado. A narrativa inicial de 25 foi corrigida na parte 03, sem alterar os caminhos.

## Auditoria dos novos documentos: sem alegar verde

Depois de escrever as partes 01..03, elas foram copiadas para a bancada e incluídas nominalmente no índice do clone para que tools/audita_docs.py realmente as examinasse. Resultado em audita-with-plan-3.txt: exit 1, 37 pendências, NENHUMA pendência herdada resolvida por acaso.

Comparação por lista de problemas com baseline-audita.txt:

- 35 já existiam antes da organização, documentadas na parte 03.
- 2 novas são enquadramento do relatório: a menção a audit_details.py como produtor da medição (script de bancada fora de tools/) foi lida como ferramenta inexistente; a instrução de manter a regra scratch/old/ foi lida como citação de caminho removido, apesar de ser pasta local gitignored não versionada. Esses dois diagnósticos foram encaminhados ao cartão de saneamento documental t_d803c318, comentário 608. Não adicionar ferramenta artificial em tools/, não sobrescrever artefato incremental e não criar isenção ampla para escapar do checker.

A parte 04 não declara que a auditoria esteja verde. O teste final sobre as quatro partes deve comparar novamente a lista completa; se acrescentar outra inconsistência, registrá-la e roteá-la, não escondê-la. A entrega do PLANO é distinta da aprovação do estado do repo para execução/publicação.

Em relação ao requisito de validate.yml/audita_docs verdes: ele não era verdadeiro no baseline medido. Os cartões de execução ficaram com dependências REAIS de saneamento t_5c8f7f57 (segurança) e t_d803c318 (docs), via E1. Não há permissão para ignorar etapa, chamar vermelho de aviso ou publicar. Sem push, run GitHub Actions ou prova de Python 3.11/Ubuntu; os comandos foram exercitados localmente com Python 3.14.7. Builds finais 6/6 e empacotamento de seis zips na cópia passaram após API própria, mas isso não torna CI/release-check global verde.

## Evidência reexecutável e retenção

Workspace de bancada: C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_adbb8f0d. O pacote ORG-R1-evidencias.zip será preservado como attachment desta tarefa, não apenas como link temporário. Não contém DLLs/assets do jogo nem as saídas de pacote dos mods.

Arquivos principais da bancada/pacote:

- inventory.json: cada arquivo físico, tamanho, estado no índice e timestamp; inventory.csv: tabela por diretório.
- audit_inventory.py e audit_details.py: scripts de bancada da coleta, não ferramentas de tools/; verify_baseline.py e verify_plan.py: comandos/asserções de verificação isolada.
- references.json e log-consumers.json: referências por termo/path/linha; a busca é literal na amostra versionada e nas fontes locais selecionadas, não prova ausência em assets ou codegen.
- duplicates.json: 14 grupos de hash idêntico em docs/tools; nenhum apagado.
- zip_inventory.json: 74 membros do entregável EV-R1, tamanhos e hashes; members path full versus local ROOT devem ser comparados pela raiz do repo, não pela subpasta EV-R1. A primeira coleta usou lookup relativo à subpasta para matches_loose_file: somente LEIA-ME casou nessa abordagem; a conferência correta da parte 01 usou ROOT/nome-do-membro e encontrou 32 paths idênticos, 0 divergentes e 42 paths não soltos. Isso NÃO permite apagar o ZIP.
- cleanup-manifest.json: 110 candidatos medidos com source_exists; aprovação é filtro source_exists true = 109. Um bytecode órfão foi preservado.
- proposed.gitignore, ignore-simulation-v2.json: proposta validada na cópia, 39 caminhos e 0 tracked-ignored finais; ignore-simulation.txt inicial CR/LF é tentativa inválida preservada para transparência.
- baseline-results.json e logs individuais: 19 checagens/tentativas iniciais, com falhas; logs corretivos de build API/RSTV, pack e Git Bash preservados separadamente. baseline-test-aut5.txt não é prova do workflow, é diagnóstico extra roteado para t_ceceef6b.
- source-hashes.json: 1.628 caminhos tracked do donor, hashes anteriores e lista vazia de mudanças durante execução de baseline.

Os scripts apontam C:/dev/stolen-realm porque esta é auditoria local autorizada, não ferramenta portátil de publicação. Não executar verify_baseline.py sobre uma pasta baseline existente: ele recusa overwrite por projeto. Reproduzir numa bancada NOVA, conferir estado vivo antes e comparar com a fotografia; não substituir edições do dono por cópia histórica. O conteúdo de scratch pode ter sido criado por outras frentes depois da fotografia; os números são datados, não invariantes.

## Coordenação final

Criados 7 cartões: 4 frentes de execução, 2 saneamentos de baseline e 1 diagnóstico AUT5. IDs, pins e pais constam da parte 03 e foram conferidos por leitura do board. Três gates preexistentes R2/R3/R4 receberam dependências e instrução para não duplicar implementação. Ao fechar ORG-R1, liberam-se apenas os saneamentos/diagnóstico; E1 segue aguardando SEG+DOC, e as demais frentes seguem gated pelo grafo.

A ordem efetiva é: SEG e DOC em paralelo → E1 → gate R2 → E2 e E3 em paralelo → gate R3 e fim E3 → E4 → gate R4. Diagnóstico AUT5 é independente e não autoriza tocar o instrumento congelado. Commit de cada frente é exclusivo e nominal; stage de fonte do dono é proibido. Frentes com semântica/contratos usam gpt-6.1-sol/openai-codex; ignore/limpeza mecânicos usam deepseek-flash/deepseek, perfil default real.

Nenhuma decisão de exclusão de entregável foi inventada para satisfazer ganho de espaço. Scratch mede 4.493.468.499 bytes, mas o plano aprova descarte somente dos 3.324.108 bytes de caches nominados fora de scratch. Preservação vence estética da árvore.
