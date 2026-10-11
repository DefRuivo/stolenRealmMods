# ORG-R1 — parte 01: inventário medido e layout canônico

Tarefa t_adbb8f0d. Auditoria de C:/dev/stolen-realm, em 11/10/2026 às 15:11:47 -03:00. Fotografia de HEAD 097f950677a02e964f7b43fc1b2998b8daa48c3c, branch ci-validate-test. Esta tarefa entrega um plano: nenhum movimento, exclusão, alteração do .gitignore ou remoção do índice foi executado.

## Método e limites dos números

Fonte: audit_inventory.py, inventory.json e inventory.csv no workspace C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_adbb8f0d. Comandos executados: `git -C C:/dev/stolen-realm ls-files -z`, `git -C C:/dev/stolen-realm ls-files -ci --exclude-standard -z`, `git -C C:/dev/stolen-realm ls-files --others --exclude-standard -z`, `git -C C:/dev/stolen-realm ls-files --others --ignored --exclude-standard -z`; enumeração física recursiva com os.walk/stat, sem seguir links de diretório. Nenhum erro de leitura; nenhum arquivo tracked ausente.

Bytes são tamanho lógico dos arquivos, não blocos alocados; MiB = bytes / 1.048.576. Tracked significa no índice do repo PRINCIPAL. Não tracked (NT) = arquivos físicos menos tracked, incluindo ignorados e arquivos internos de repos/worktrees aninhados. Ignorados (I) conta apenas os caminhos que o Git principal enumerou como ignorados. Em scratch há sandboxes com .git: 8.407 arquivos NT não enumerados como ignorados pelo Git principal NÃO são 8.407 arquivos `??` na raiz. `git status --short` reportou somente `?? .worktrees/` e `?? nul`. Metadados .git não são conteúdo candidato a versionamento.

## Primeiro nível completo

| Caminho | Arquivos físicos | Bytes | MiB | Tracked | NT | I | Natureza / decisão |
|---|---:|---:|---:|---:|---:|---:|---|
| raiz, arquivos soltos | 18 | 485892 | 0,463 | 3 | 15 | 14 | .gitignore, Directory.Build.props e README.md versionados; notas/editor/logs locais preservados |
| .git/ | 2794 | 79170055 | 75,502 | 0 | 2794 | 0 | metadados Git; NÃO reorganizar nem limpar manualmente |
| .github/ | 4 | 110467 | 0,105 | 3 | 1 | 1 | workflows e validador de pacote; 1 cache Python |
| .worktrees/ | 964 | 33461044 | 31,911 | 0 | 964 | 0 | worktree Git independente; ignorar no repo principal, preservar |
| BetterCombatText/ | 42 | 683718 | 0,652 | 10 | 32 | 32 | fonte/metadados de mod + bin/obj locais |
| BetterFont/ | 38 | 572381 | 0,546 | 6 | 32 | 32 | fonte/metadados de mod + bin/obj locais |
| BetterStats/ | 38 | 368958 | 0,352 | 6 | 32 | 32 | fonte/metadados de mod + bin/obj locais |
| BetterTooltips/ | 48 | 1769026 | 1,687 | 16 | 32 | 32 | fonte/metadados de mod + bin/obj locais |
| NuGet/ | 1 | 0 | 0,000 | 0 | 1 | 1 | marcador local de migração; gitignored, não versionado |
| ReloadProbe/ | 34 | 202741 | 0,193 | 0 | 34 | 34 | harness local gitignored, não versionado; contém 2 fontes, não só lixo |
| RoguelikeDebugger/ | 50 | 780270 | 0,744 | 18 | 32 | 32 | fonte de ferramenta de desenvolvimento distribuível + bin/obj locais |
| RoguelikeSkillTreeVisualizer/ | 51 | 1166099 | 1,112 | 19 | 32 | 32 | fonte/metadados de mod + bin/obj locais |
| api/ | 223 | 5477038 | 5,223 | 29 | 194 | 194 | Core/Hooks/Plugin/Smoke/Inspect + documentação e outputs locais |
| dist/ | 28 | 2856432 | 2,724 | 1 | 27 | 27 | 27 pacotes locais; somente .gitkeep tracked; preservar versões existentes |
| docs/ | 1056 | 141337819 | 134,790 | 972 | 84 | 84 | documentação, dados entregues, evidências; não tratar como cache |
| lib/ | 16 | 11306920 | 10,783 | 0 | 16 | 16 | referências locais do jogo/Unity/BepInEx; necessárias ao build, não redistribuir |
| release/ | 1 | 7103 | 0,007 | 1 | 0 | 0 | release/mods.json: decisão humana/gate de publicação; NÃO é pasta de zips |
| scratch/ | 51055 | 4493468499 | 4285,305 | 1 | 51054 | 42647 | sandboxes, testes, cópias privadas, backups e outputs; 1 ferramenta tracked a promover |
| scripts/ | 2 | 14253 | 0,014 | 2 | 0 | 0 | automação PowerShell de build/empacotamento |
| tools/ | 1156 | 16536984 | 15,771 | 541 | 615 | 615 | ferramentas, testes, fixtures, fontes C# auxiliares e outputs locais |

São 19 diretórios de primeiro nível, incluindo .git/, mais os arquivos soltos. Conteúdo principal sem .git/ e .worktrees/: 53.861 arquivos, 4.677.144.600 bytes. Índice principal: 1.628 arquivos, 148.509.662 bytes físicos. As próximas partes ORG-R1 são novos arquivos e NÃO integram esta fotografia histórica.

## As oito áreas obrigatórias

| Caminho | Arquivos / tracked | Bytes | Observação verificável |
|---|---:|---:|---|
| docs/cobertura/EV-R1/ | 30 / 30 | 98414502 | entrega completa; zip 45598179; catalogo-referencias.json 27834612; eventos.json 14343841; eventos-originais.json 2956196 |
| scratch/ | 51055 / 1 | 4493468499 | 4,185 GiB; scratch/kit/ sozinho tem 42050 arquivos e 3956568790 bytes |
| .worktrees/ | 964 / 0 | 33461044 | .worktrees/level-r2, HEAD d1de4eae68ff4f692effe34046bbf5706ad43ab6, branch wt/t_918314e9, identificado por git worktree list --porcelain |
| dist/ | 28 / 1 | 2856432 | 27 zips ignorados e .gitkeep; o maior zip tem 164563 bytes |
| release/ | 1 / 1 | 7103 | release/mods.json, lido pelo pipeline; manter localização |
| lib/ | 16 / 0 | 11306920 | Assembly-CSharp.dll 7712768 bytes; restante Unity/BepInEx/Harmony/Sirenix; manter privado e local |
| NuGet/ | 1 / 0 | 0 | NuGet/Migrations/1, marcador ignorado; não produz ganho relevante de espaço |
| ReloadProbe/ | 34 / 0 | 202741 | harness gitignored não versionado: Plugin.cs 272 bytes, .csproj 2063 bytes; restantes são bin/obj/marcador local |

## Layout canônico decidido para esta rodada

Manter os SEIS mods no primeiro nível, com nomes exatos existentes. NÃO criar mods/ nem mudar namespaces/GUIDs/assemblies. tools/pack-thunderstore.py:7-17, release/mods.json:23, .github/workflows/validate.yml:182 e tools/release-check.sh:274-276 dependem da descoberta no primeiro nível. Mover todos os mods seria uma migração funcional muito maior, sem benefício necessário nesta frente.

    <Mod>/                  fonte C#, csproj, manifest, icon, README, CHANGELOG
    api/                    fontes da API própria e suas docs
    tools/                  ferramentas mantidas, testes/fixtures e geradores
    tools/test-cycle.sh     destino aprovado da ferramenta hoje em scratch
    scripts/                entradas PowerShell mantidas; sem migração cosmética
    docs/                   guias, resultados, evidências e dados entregues
    docs/automacao/          relatórios incrementais e evidências de execução
    docs/cobertura/         censos e datasets consultáveis, incluindo EV-R1
    release/mods.json       gate/registro de publicação versionado
    dist/                   outputs privados de empacotamento; só .gitkeep tracked
    lib/                    referências locais não distribuíveis; ignorado
    scratch/                trabalho local ignorado; somente shim legado rastreado
    .worktrees/             worktrees geridos pelo Git, ignorados no repo principal

A única mudança de caminho APROVADA nesta rodada é scratch/test-cycle.sh → tools/test-cycle.sh, com shim de compatibilidade no caminho antigo e correção dos consumidores ativos; especificação na parte 03. A pasta scratch/ já concentra os temporários: não será movida inteira nem apagada, porque a varredura encontrou 1.418 linhas com scratch/ em 432 arquivos da amostra. Scratch fora do versionamento não significa fora do disco.

## Dados pesados: separar sem perder entrega

docs/cobertura/EV-R1/ continua canônico e inteiro nesta rodada. Aprovação de mover/deletar/desindexar seus 30 arquivos: ZERO. Futuro layout possível: guias/schema/índices no repo, JSONs em docs/cobertura/EV-R1/dados/, pacote integral em armazenamento privado durável com manifesto de hashes e procedimento de restauração. Isso é uma OPÇÃO CONDICIONAL, não autorização para ORG-R2/R3/R4; envolve atualizar leitores e revalidar offline a entrega.

A leitura de zip_inventory.json encontrou 74 membros regulares no zip, 1.527.831.827 bytes descomprimidos; 32 coincidem byte a byte com caminhos existentes na raiz do repo e 42 não existem nesses caminhos. O LEIA-ME.md da raiz do zip também coincide com docs/cobertura/EV-R1/LEIA-ME.md, portanto a contagem de 42 é de caminhos, não de conteúdos exclusivos. Há scripts de reprodução e evidências que NÃO estão soltos no repo. O zip NÃO é mera duplicata dos 29 arquivos soltos da pasta: contém evidencias/assets/globalgamemanagers-v1.json (1402449173 bytes) e evidencias/codigo/Assembly-CSharp.decompiled.cs (12530363 bytes). Não extrair automaticamente, não apagar, não publicar como pacote público; preservar revisão privada e verificar autorização de redistribuição separadamente.

As duplicatas de evidência em docs/automacao/ serão listadas, mas permanecerão: igualdade de hash não prova redundância de proveniência. Não reescrever snapshots/hashes históricos para fazê-los parecer atuais.

## Continuação

- Parte 02: política de índice/.gitignore e candidatos de limpeza com consumidores.
- Parte 03: referências, movimentos, ordem segura, baseline executado e cartões.
