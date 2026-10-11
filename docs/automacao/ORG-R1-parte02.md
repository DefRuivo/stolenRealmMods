# ORG-R1 — parte 02: versionamento, .gitignore e limpeza permitida

Tarefa t_adbb8f0d; fotografia de 11/10/2026, HEAD 097f950677a02e964f7b43fc1b2998b8daa48c3c. Plano, não execução. Fontes: inventory.json, references.json, duplicates.json e o .gitignore de 85 linhas, no workspace registrado na parte 01.

## O índice real contradiz a hipótese de lixo tracked

`git ls-files -ci --exclude-standard -z` encontrou 33 caminhos tracked que CASAM com alguma regra de ignore. São scratch/test-cycle.sh e 32 arquivos .log em tools/. Isso NÃO prova que deveriam sair do índice: fixtures e evidências deliberadas também casam com *.log. Inventário do índice por categoria:

| Categoria examinada | Tracked encontrados | Decisão / comando |
|---|---:|---|
| diretórios bin/ e obj/ | 0 | nenhum `git rm --cached`; manter regras existentes |
| DLLs/PDBs, incluindo terceiros | 0 | nenhum `git rm --cached`; lib/ e scratch/backups/ já ignorados |
| bancos .db/.sqlite, inclusive kanban/kanban.db | 0 | nenhum `git rm --cached`; o caminho isca não existe no disco desta fotografia |
| .bak/.old/.tmp/.cache e diretórios backup/cache/__pycache__ | 0 | nenhum `git rm --cached`; não inventar remoção de arquivo ausente |
| pacote ZIP | 1 | docs/cobertura/EV-R1/EV-R1-entrega.zip: entregável protegido, manter |
| .log em tools/ | 32 | fixtures/provas, manter nesta rodada com exceções explícitas |
| script mantido em scratch/ | 1 | scratch/test-cycle.sh: manter no índice até `git mv` na frente de movimentos |

LISTA APROVADA DE `git rm --cached`: VAZIA (0 itens). Não executar comando recursivo genérico. Não usar `--ignore-unmatch` para fingir que havia arquivos; registrar 0 remoções como resultado real da frente. Se surgirem arquivos novos nas categorias proibidas, isso é mudança de escopo: comparar a nova fotografia com este plano e registrar decisão antes de desindexar.

Comandos RECUSADOS: `git rm -r --cached -- scratch` retiraria a ferramenta usada em tools/release-check.sh:529; `git rm --cached -- tools/fixtures/*.log` retiraria dados de teste; retirar docs/cobertura/EV-R1/ retiraria a entrega sem autorização. Um arquivo já ignorado e NT não precisa de git rm --cached. Desindexar não apaga blobs do histórico, nem desfaz eventual exposição passada; não reescrever histórico nesta frente.

## .gitignore proposto, mínimo e justificado

Preservar as 85 linhas existentes, salvo o ajuste pontual da regra geral de scratch e o comentário que explica a ferramenta promovida. Não substituir o arquivo por template genérico. Não adicionar *.dll, *.zip, *.json ou *.db globais: ignorariam entregas/fixtures de forma indiscriminada.

1. TROCAR a linha 49 `scratch/` por `/scratch/*`. A antiga regra ignorava o diretório inteiro; a nova ignora o conteúdo e permite uma exceção de arquivo sem reincluir sandboxes.
2. Manter scratch/old/, scratch/backups/ e as demais regras específicas existentes. Na descrição de test-cycle, explicar que ORG-R3 promove a implementação a tools/ e conserva apenas o shim de compatibilidade em scratch/.
3. ACRESCENTAR ao final este bloco. Cada exceção de log protege exatamente um dos 32 caminhos auditados, não abre uma árvore inteira de dumps:

```gitignore
# ORG-R2: worktrees locais sao repos independentes, nunca gitlinks do repo principal.
/.worktrees/
# ORG-R2: impedir o banco-isca local e sidecars de entrarem no indice; hoje ausentes.
/kanban/kanban.db*
# ORG-R2: arquivo reservado criado por redirecionamento local; ignorar, nao apagar.
/nul
# ORG-R2: ferramenta mantida; depois de ORG-R3 sera somente shim legado.
!/scratch/test-cycle.sh
# ORG-R2: fixtures e provas intencionais, nao dumps efemeros. Escopo por arquivo.
!/tools/automacao/aut5/fixtures/log-completo.log
!/tools/fixtures/bf-shaders-em-jogo.log
!/tools/fixtures/bf-varredura-em-jogo.log
!/tools/fixtures/shrines-exemplo.log
!/tools/fixtures/shrines-piso-cru.log
!/tools/fixtures/shrines-rv46-dedupe.log
!/tools/testes/bancada2-prova-linha-antes-do-range.log
!/tools/testes/bct-prova-reprovando.log
!/tools/testes/bct2-sombra-prova-reprovando.log
!/tools/testes/bct3-sombra-visivel-prova-reprovando.log
!/tools/testes/bct4-contraste-prova-reprovando.log
!/tools/testes/bct5-polaridade-fonte-prova-reprovando.log
!/tools/testes/bf-fix8-reset-e-teto.log
!/tools/testes/bf-prova-reprovando.log
!/tools/testes/bt10-reaper-prova.log
!/tools/testes/bt11-13-prova-de-fogo.log
!/tools/testes/bt12f-prova-de-fogo.log
!/tools/testes/formato4-prova-regras-bf-343.log
!/tools/testes/formato5-prova-regras-bf-343.log
!/tools/testes/formato7-prova-faixa.log
!/tools/testes/formato8-prova-casadores.log
!/tools/testes/formato9-prova-janela.log
!/tools/testes/man2-prova-de-fogo.log
!/tools/testes/niv3-texto-prova.log
!/tools/testes/parser1-prova-comentario.log
!/tools/testes/rstv11-prova-reprovando.log
!/tools/testes/rstv11b-prova-reprovando.log
!/tools/testes/rstv12-prova-reprovando.log
!/tools/testes/rstv13-14-prova-reprovando.log
!/tools/testes/rstv15-prova-reprovando.log
!/tools/testes/rstv19-prova-reprovando.log
!/tools/testes/rv28-globule-prova-de-fogo.log
```

As regras existentes bin/, obj/, lib/, NuGet/, __pycache__/, *.pyc, *.log, dist/* e !dist/.gitkeep permanecem. ReloadProbe/ permanece um harness gitignored, não versionado; não adicionar a fonte local ao índice para satisfazer um detector documental. As regras de segredos não serão enfraquecidas.

Aceite de ORG-R2: `git ls-files -ci --exclude-standard` deve cair de 33 para 0 sem reduzir os 1.628 caminhos da fotografia; os novos documentos aumentarão o total, por isso comparar o conjunto original, não só o total. `git check-ignore --no-index -v -- scratch/um-dump.json .worktrees/level-r2/.git kanban/kanban.db nul` deve apontar regras pertinentes. Conferir separadamente o conjunto de exceções com check-ignore: uma linha negada significa REINCLUSÃO, não falha da regra. Confirmar dist/.gitkeep tracked; lib/Assembly-CSharp.dll ignorado; todos os 33 originais no disco e no índice. Stage somente .gitignore e relatório incremental da própria frente.

## Consumidores dos logs: por que não desindexar por extensão

- tools/automacao/aut5/fixtures/log-completo.log é entrada de fixture no componente aut5; tools/automacao/aut5/ contém 4 caches derivados, mas isso não transforma a fixture em cache.
- tools/fixtures/ contém seis fixtures (43.255 bytes ao todo), incluindo casos de shrines e dumps de fonte/shader usados para bancada. A busca de tools/fixtures/ encontrou 102 linhas em 38 arquivos da amostra: desindexar a árvore deixaria a bancada sem entrada no clone.
- tools/testes/ contém 260 caminhos tracked, incluindo 25 logs de prova. A busca de tools/testes/ encontrou 4.017 linhas em 326 arquivos da amostra. Logs de contra-prova não são saída descartável só por terminarem em .log: representam histórico de comportamento do instrumento. Retenção conservadora de todos os 25; não autorizamos eliminar prova negativa.
- Os 84 arquivos NT ignorados em docs/ NÃO devem ser apagados. Há logs locais referidos por entregas em docs/automacao/, como LogOutput-copia.log. Auditar preservação/futura inclusão é questão separada da limpeza: estar ignorado não significa estar obsoleto.

## Exclusões: autorização estrita

E1 APROVADO: somente os 110 arquivos *.pyc sob diretórios __pycache__ de tools/ e .github/ presentes no manifesto desta fotografia; total 3.375.997 bytes. Não remover diretórios com outros arquivos; não tocar em docs/, api/, scratch/, lib/, dist/ ou bin/obj de probes congelados. São bytecodes derivados dos fontes Python, regenerados pela importação; o conjunto tracked da categoria é 0. A frente deve reproduzir a lista física, comparar com o manifesto, confirmar ausência no índice, excluir APENAS os caminhos enumerados e executar importações/testes com `PYTHONDONTWRITEBYTECODE=1`. Fontes Python devem manter hashes. Se um .pyc tiver fonte ausente, conservar e reportar, não apagar o único bytecode de um módulo.

| Grupo de caches permitido | Arquivos | Bytes |
|---|---:|---:|
| .github/scripts/__pycache__/ | 1 | 19342 |
| tools/__pycache__/ | 19 | 406422 |
| tools/automacao/aceite/__pycache__/ | 2 | 100471 |
| tools/automacao/aut5/__pycache__/ | 4 | 154476 |
| tools/automacao/aut6/__pycache__/ | 5 | 114932 |
| tools/automacao/cenarios/__pycache__/ | 6 | 306925 |
| tools/automacao/ciclo/__pycache__/ | 4 | 224804 |
| tools/automacao/estilo/__pycache__/ | 4 | 249326 |
| tools/automacao/kit05/__pycache__/ | 1 | 23796 |
| tools/automacao/kit06/__pycache__/ | 1 | 15833 |
| tools/automacao/kit07/__pycache__/ | 3 | 83607 |
| tools/automacao/kit08/__pycache__/ | 1 | 53353 |
| tools/automacao/kit10/__pycache__/ | 3 | 132124 |
| tools/automacao/kit11/__pycache__/ | 2 | 76048 |
| tools/automacao/kit12/__pycache__/ | 2 | 155536 |
| tools/automacao/kit13/__pycache__/ | 1 | 12558 |
| tools/automacao/kit15/__pycache__/ | 4 | 94606 |
| tools/automacao/offline/__pycache__/ | 3 | 74848 |
| tools/automacao/offline/testes/__pycache__/ | 5 | 74858 |
| tools/automacao/runtime/__pycache__/ | 5 | 223962 |
| tools/automacao/runtime/testes/__pycache__/ | 7 | 95813 |
| tools/testes/__pycache__/ | 20 | 597434 |
| tools/testes/contra-prova/__pycache__/ | 2 | 6612 |
| tools/testes/testes/puros/__pycache__/ | 5 | 78311 |

Candidatos NÃO APROVADOS (nenhuma exclusão delegada):

| Candidato | Medição | Justificativa / consumidores que impedem apagar agora |
|---|---|---|
| scratch/kit/ | 42050 arquivos; 3956568790 bytes | grande fonte de espaço, mas guarda sandboxes, dados privados e provas KIT; referências em docs/automacao/ e instrumentos; requer inventário por rodada, fechamento dos cartões e backup/restauração |
| scratch/backups/ | 34 arquivos; 1678528 bytes | backups, inclusive DLL de terceiro mencionada em .gitignore:55-61; retenção privada e rollback, sem autorização de descarte |
| scratch/old/ | 11 arquivos; 126227 bytes | nome sugere antiguidade mas não prova inutilidade; notas fora do Git, referências históricas e fontes locais exigem revisão; caminho gitignored não versionado |
| ReloadProbe/bin/ e obj/ | parte dos 34 arquivos do harness gitignored não versionado | regeneráveis, mas inspeção/estilo e check_deploy_optin detectam o harness local; manter até decisão sobre aposentadoria; não apagar Plugin.cs/.csproj |
| dist/*.zip | 27 arquivos; total dist/ 2856432 bytes | versões anteriores podem ser rollback/entrega; pacote atual não comprova preservação de releases antigas |
| docs/cobertura/EV-R1/EV-R1-entrega.zip | 45598179 bytes, 74 membros | dados + reprodução + evidências não soltas; entregável protegido, não é duplicata eliminável |
| JSONs grandes de EV-R1 | catalogo 27834612; eventos 14343841; originais 2956196 bytes | dataset de consulta e roundtrip, referenciado por índices/schema; sem decisão de armazenamento privado não retirar |
| NuGet/Migrations/1 | 1 arquivo; 0 bytes | cache regenerável mas sem ganho de espaço, potencial regeneração pelo SDK; manter |
| lib/*.dll | 16 arquivos; 11306920 bytes | HintPath dos csproj; deletar quebra build local; manter privado |
| .worktrees/level-r2 | 964 arquivos; 33461044 bytes | registrado por git worktree list; não remover por filesystem nem git clean; depende de merge/estado/decisão do dono |
| nul | entrada de raiz; stat comum devolve 0 bytes e mtime=0 | nome reservado Windows pode resolver dispositivo em vez de arquivo; NÃO interpretar stat como prova de arquivo vazio eliminável; somente ignorar agora |

## Duplicatas byte a byte: reportadas, não apagadas

audit_details.py agrupou arquivos tracked de docs/ e tools/ por tamanho e SHA-256. Encontrou 14 grupos de conteúdo idêntico. Exemplo: quatro suite-contra-prova.json (29.176 bytes cada) em docs/automacao/AUT-7-evidencias/cor-aut7/, AUT-7-evidencias/, COR-AUT7-F2-evidencias/ e COR-AUT7-evidencias/, SHA-256 275e6da19ac33c1aa18b725ec51d712c313a013041c610a58ae4cb071eb4320e. Representam entregas em contextos/rodadas diferentes: não são backups descartáveis por hash.

Outro exemplo: docs/automacao/INT-R1-C2-I1-evidencias/suite-17-testes-baseline.json, tools/automacao/kit13/ApiBridgeHarness/evidencia-api-bridge.json e tools/automacao/kit13/evidencia-api-bridge.json são idênticos (1.671 bytes, SHA-256 d12f8b9a00339ae4fb55d2813acfcaf2b3126b45d83c15d98baceb4dae3044e1). Documento preserva o resultado da rodada, ferramentas preservam outputs de bancada. Qualquer normalização futura exige corrigir consumidores e distinguir snapshot de cache. O arquivo duplicates.json preserva os 14 grupos completos. Aprovações de exclusão em docs/: ZERO.

## Política de segurança

O baseline de check_segredos reprova o estado herdado por heurística de entropia (sem padrão conhecido de credencial encontrado). Não afirmar vazamento confirmado e não ignorar o alerta. Resolver por triagem especializada de cada achado, sem imprimir possíveis valores secretos, sem whitelist ampla de docs/ e sem reduzir limiar global. Nenhum push/publicação/rewrite de histórico nesta tarefa. A parte 03 registra a dependência de saneamento antes de liberar execução.
