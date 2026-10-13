# Estrutura e política do repositório

Política de manutenção derivada do plano ORG-R1 partes 01..04 e dos gates de organização de 11/10/2026. Este documento descreve os destinos mantidos; não autoriza novas migrações, exclusões ou publicação. Decisões e edições manuais do dono prevalecem. O [índice de documentação](README.md), o [ambiente](AMBIENTE.md), o [CI](CI.md) e a [publicação](PUBLICACAO.md) detalham os respectivos rituais.

## 1. Layout canônico: fonte, dados, artefatos e estado privado

Os seis mods **liberados** para distribuição ficam diretamente na raiz: `BetterCombatText/`, `BetterFont/`, `BetterStats/`, `BetterTooltips/`, `RoguelikeDebugger/` e `RoguelikeSkillTreeVisualizer/`. `RoguelikeUnlimitedLevelProgression/` entra como **pacote descoberto e bloqueado** desde 12/10/2026 (LEVEL-PACOTE-CONTRATO): fonte, metadados e `icon.png` versionados, `publicar: false` com motivo em [`release/mods.json`](../release/mods.json) enquanto *runtime e aceite humano* estiverem pendentes. Esta lista delimita o layout aprovado, não congela a descoberta de pacotes nem o total de arquivos do projeto. A descoberta executável é `python tools/pack-thunderstore.py --listar-nomes`; versões vêm dos projetos e espelhos, não de uma tabela estática nesta política.

| Caminho na raiz | Papel e versionamento | Regra de manutenção |
|---|---|---|
| `<Mod>/` | Fonte C#, projeto e metadados próprios do pacote versionados; `bin/` e `obj/` são saídas locais ignoradas. | Um projeto/pacote por mod, sem camada nova de `src/` ou migração das pastas existentes. |
| `api/` | API própria RealmApi: fonte, contratos, ferramentas e evidências versionados; outputs de build ignorados. | Módulo separado, não um sétimo pacote descoberto na raiz. Ver [API própria](../api/README.md). |
| `tools/` | Ferramentas mantidas, fixtures, dados de referência e provas versionadas. | Não confundir uma entrada de teste ou contra-prova com o cache gerado ao executá-la. |
| `scripts/` | Wrappers mantidos, inclusive `package.ps1`, versionados. | Reutilizar a validação/descoberta de `tools/`, sem outra lista independente de mods. |
| `docs/` | Documentação, datasets, revisão e evidências entregues versionados conforme as regras e exceções do índice. | Preservar dados e curadoria; não é uma árvore descartável de outputs. |
| `release/mods.json` | Gate de publicação VERSIONADO, com decisão humana, motivo, ordem de envio e registro de publicação. | Não é cache. Conferir seu conjunto contra a descoberta dos pacotes; aprovação de build não libera upload. |
| `dist/` | ZIPs gerados locais/ignorados; SOMENTE `dist/.gitkeep` é versionado. | Um pacote ignorado pode ser entrega ou rollback. Regenerabilidade não autoriza sobrescrever/apagar versões antigas. |
| `lib/` | Referências locais privadas do jogo/BepInEx/Unity, ignoradas e necessárias ao build. | Obter do ambiente autorizado; nunca versionar ou redistribuir assemblies/assets de terceiros. |
| `.worktrees/` | Worktrees locais ignorados, gerenciados pelo Git; não são gitlinks do projeto. | Inspecionar com `git worktree list`; não apagar por filesystem nem por limpeza genérica. |
| `scratch/` | Bancada privada ignorada; apenas o shim legado `scratch/test-cycle.sh` é tracked. | A implementação mantida vive em `tools/test-cycle.sh`. Sandboxes, backups, logs e screenshots locais continuam privados. |
| `.github/` | Workflows e scripts de validação/publicação versionados. | Validação offline não distribui referências privadas nem substitui revisão humana. |
| `Directory.Build.props` | Contrato versionado de deploy desligado por padrão. | Todos os alvos que escrevem no perfil devem exigir o opt-in explícito. |

A [regra efetiva de ignore](../.gitignore) é a fonte verificável dos padrões, não uma licença de descarte. Ela ignora notas avulsas Markdown por padrão e reinclui documentação e metadados deliberados; dumps `DUMP-*.md` de cobertura permanecem ignorados. Há exceções nominais para fixtures/provas `.log` e para um guia mantido de ferramenta. Não ampliar globalmente exceções de logs, nem adicionar regras globais de DLL/ZIP/JSON/DB para esconder entregáveis. Arquivos de instrução de IA permanecem fora do versionamento por decisão do dono (INST-1); não usá-los como substitutos da documentação mantida.

`ReloadProbe/` é harness local gitignored, não versionado; não é um mod distribuível nem requisito de fonte presente num clone. Banco local do quadro, sidecars, caches, configuração de editor, credenciais e notas de trabalho também ficam privados. Não presumir que todo arquivo local sob `docs/` foi entregue: conferir índice, ignore e consumidores.

## 2. Evidência não é dump nem cache

- Dataset entregue: os CSVs de `docs/cobertura/` e os dados/schema/ZIP de `docs/cobertura/EV-R1/` são entradas e entregáveis. Seus índices explicam procedência e limites. Censo de boot não prova, por si só, texto servido em todas as telas nem runtime atual.
- Fixture/prova `.log`: arquivos deliberadamente rastreados em `tools/fixtures/`, `tools/testes/` e `tools/automacao/aut5/fixtures/` são entradas reproduzíveis e registros de contra-prova, inclusive casos que devem REPROVAR. As exceções de `.gitignore` são por caminho. Conferir o conjunto vivo com `git ls-files '*.log'`; não fixar aqui um total que envelhece a cada rodada.
- Dump/log privado: log integral do perfil, dumps de bancada, saídas de agente e screenshots não entram no índice automaticamente. Antes de promover uma amostra, verificar origem, direitos, dados sensíveis, consumidores e escopo nominal; uma fixture nunca vira prova de jogo somente por ser versionada.
- Cache regenerável: `__pycache__/`, `.pyc`, `bin/`, `obj/` e caches de SDK são derivados, mas apagar exige autorização e fonte/reprodução disponível. Um bytecode órfão não é regenerável demonstrado; o órfão do kit10 foi preservado pela limpeza ORG-R4.

Não usar `git rm --cached` só porque uma extensão casa com ignore. Isso remove a entrada do próximo clone sem apagar o histórico e pode tirar uma prova necessária. O plano ORG-R1 aprovou zero desindexações; a limpeza autorizada E3 foi nominal, somente dos caches com fonte listados no manifesto. Não transformar esse aceite passado em permissão recorrente de limpar árvores.

### Fotografias e hashes históricos são imutáveis

Relatórios de rodada, inventários, suites de evidência e hashes descrevem uma fotografia datada de um commit/ambiente. Mesmo quando o número, caminho ou diagnóstico deixou de representar o presente, conservar os bytes da fotografia. Resultado cacheado não é teste recém-executado; igualdade de hash não torna duas entregas de contextos diferentes descartáveis.

Correções e novas provas são artefatos incrementais: criar NOVO arquivo numerado (`parteNN`/rodada) e explicar qual fotografia complementa ou corrige. Não reescrever relatório histórico para parecer verde. Links operacionais dos índices vivos apontam para o destino mantido; comandos e caminhos em snapshots continuam históricos. O shim legado permite resolver o caminho antigo do ciclo sem editar essas fotografias.

Relatórios gerados com trecho manual curado seguem o contrato da ferramenta, por exemplo o marcador `<!-- fim-gerado -->` e a guarda de `tools/preserva_curado.py`. Reler a curadoria antes de executar gerador/build; não substituir ajustes manuais por conteúdo de um clone antigo. Proveniência nominal com hash em `tools/audita_docs_proveniencia.json` explica ocorrências congeladas; não é whitelist de pastas nem autorização para alterar snapshots, auditor ou detector de segredos.

### Retenção e restauração antes de mover/remover entregáveis

EV-R1, backups privados, ZIPs de `dist/`, instrumentos congelados, screenshots e fontes locais não receberam autorização de descarte nesta organização. Tamanho, nome “old”, ignore, duplicação byte a byte ou presença parcial de membros soltos não bastam para excluir.

Uma futura proposta deve, ANTES de qualquer movimento ou remoção:

1. Inventariar caminhos nominais, tamanho e SHA-256, estado tracked/ignored e consumidores (docs, ferramentas, projetos, workflows e referências locais pertinentes).
2. Registrar decisão explícita do dono/cartão sobre cada classe de entregável, período/critério de retenção e destino privado durável quando necessário. Não assumir que workspace temporário é backup.
3. Fazer backup privado íntegro, fora de `plugins/` e fora do que seria publicado; registrar manifesto e localização de recuperação sem segredos/PII no relatório público.
4. Exercitar restauração numa pasta isolada NOVA, conferir hashes/membros e entradas necessárias à reprodução. Guardar prova real de restauração e rollback.
5. Só então executar o escopo aprovado, corrigir referências ativas no mesmo passo e verificar consumidores/build/checks. Se uma referência histórica precisa permanecer, declarar sua procedência e preservar compatibilidade, sem adulterar a fotografia.

Backups de DLL nunca ficam em `BepInEx/plugins/`: o loader varre subpastas e pode carregá-los como outro plugin. Terceiros continuam privados mesmo quando contidos em backup ou ZIP; não anexar/copiar essas bibliotecas para uma entrega pública de evidências. `.worktrees/` exige ainda conferência de branches, mudanças não commitadas e estado de integração pelo Git antes de qualquer decisão de aposentadoria.

## 3. Como adicionar um mod ou frente

### Novo mod

1. Criar `<Mod>/` na raiz, com nome estável compatível com a descoberta/validação existentes, `<Mod>.csproj`, `Plugin.cs`, fonte própria e GUID `com.gumatos.*` único. Usar o alvo de framework/referências adequados ao projeto; assemblies de terceiros ficam em `lib/` com `Private=false`, não no pacote.
2. Para ser pacote, fornecer `manifest.json`, `README.md`, `CHANGELOG.md` e `icon.png` na pasta. Manter alinhados `<Version>` do csproj (fonte), `version_number` do manifest, literal/const do plugin e versão do README. Metadados, ícone e dependências devem passar a validação existente; dependências novas exigem decisão/contrato explícitos, não burlar o checker.
3. Reutilizar `Directory.Build.props`: deploy desligado e qualquer alvo que copie ao perfil condicionado a `DeployToBepInEx == 'true'`. Build comum, Release ou empacotamento não instala. Conferir com `python tools/check_deploy_optin.py` antes de construir.
4. Atualizar o conjunto e a ordem de dependências em `release/mods.json` para acompanhar `--listar-nomes`, iniciando o novo pacote com `publicar: false` e motivo. Liberação exige revisão independente e decisão humana; não copiar uma autorização antiga de outro mod.
5. Acrescentar links/descrição aos índices pertinentes, sem contagens permanentes de arquivos ou resultados inventados; executar auditoria, workflow local e build sem deploy. Conferir pacote em bancada isolada, sem sobrescrever ZIPs preservados. Seguir [publicação](PUBLICACAO.md) somente quando os gates e o dono autorizarem.

Não executar sincronização automática de versões sobre edições paralelas sem reler e conferir o diff: o sincronizador altera espelhos. Não modificar `Assembly-CSharp.dll`; extensões são plugins separados.

### Nova frente de ferramenta, dado ou investigação

Definir primeiro se a entrega é fonte mantida (`tools/`, `scripts/`, `api/`), dataset/evidência (`docs/` ou módulo próprio) ou experimento privado (`scratch/`). Nomear contrato, entradas, consumidores, origem/licença, validação, rollback e retenção no cartão; evitar segunda fonte da verdade. Criar relatórios/evidências numerados novos, inserir links pertinentes e stage somente dos caminhos da frente. Não promover fonte local, dump ou terceiro por conveniência do layout.

Uma frente = um commit exclusivo nominal. Nunca `git add -A` nem `git commit -a`. Reler arquivos e índice imediatamente antes de stage/commit; se houver mudança do dono ou outra frente, preservar e separar, nunca resetar/restaurar em massa.

## 4. Verificação sem agir no jogo

As referências privadas precisam estar disponíveis em `lib/` antes de compilar. Essa pasta vive na **raiz do checkout** e é resolvida por caminho relativo a ele (nunca por caminho absoluto do dono nem pela profundidade de um worktree): o checkout canônico compila sem argumento extra, e clone/worktree isolado sem `lib/` falha no alvo `ValidateCommonLibDir` com a mensagem `LEVEL-LIB`, exigindo o override autorizado `-p:CommonLibDir=<caminho absoluto da lib>`. Não existe fallback silencioso e as DLLs do jogo não são copiadas nem versionadas para satisfazer um build. O RSTV consome a API própria por HintPaths de Release: construir a API ANTES dele, inclusive quando o build do mod for Debug. A API de terceiros não é substituto dessas referências.

Da raiz do repo, os builds de verificação ficam explicitamente sem deploy:

```bash
python tools/check_deploy_optin.py
dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=false --nologo
dotnet build <Mod>/<Mod>.csproj -c Release -p:DeployToBepInEx=false --nologo
python tools/audita_docs.py
bash tools/release-check.sh
```

O projeto Plugin da API constrói Core/Hooks pelas referências de projeto; o [guia da API](../api/README.md) detalha os demais projetos e contratos. Repetir o build para cada mod descoberto. Reproduzir TODOS os comandos de [validate.yml](../.github/workflows/validate.yml), inclusive `--estrito`, cobertura `--prova` e o empacotador guardado. Usar clone/bancada com índice Git para testar os documentos novos (a auditoria lê arquivos rastreados), adicionar apenas esses documentos ao índice da cópia e manter `PYTHONDONTWRITEBYTECODE=1` para não recriar caches durante a conferência.

Num clone sem DLL o guard valida descoberta; com DLL Release ele gera ZIPs. Exercitar os dois ramos em cópia NOVA, com referências privadas só para compilação e outputs locais, não copiando DLLs de build antigo como prova. No repo do dono, não executar empacotamento que sobrescreva entregáveis antigos para satisfazer um check: testar o ramo com escrita em bancada e usar `--so-conferir` para o pre-flight sem escrever em `dist/`. Check de notas pode regenerar relatório; conferir previamente a curadoria e os hashes. A [ordem do workflow](CI.md) é a referência viva; esta política não mantém outra numeração de passos.

Exit 0 dos checks/builds/release-check normal prova somente o escopo executado. Não equivale a run remoto de GitHub Actions, teste em Ubuntu/Python 3.11, instalação, ciclo do jogo, observação runtime `ui.localized` ou conferência visual humana. Esses passos ficam PENDENTES/NAO_EXERCITADOS até execução autorizada com evidência correspondente; fixture offline não os substitui. O ciclo mantido `tools/test-cycle.sh` e o modo explícito de instalação têm efeitos no perfil/jogo e não são chamados para validar esta política.

## 5. Origem das decisões e gates

- [ORG-R1 parte 01 — inventário e layout](automacao/ORG-R1-parte01.md), [parte 02 — índice/retenção proposta](automacao/ORG-R1-parte02.md), [parte 03 — erratas e saneamentos](automacao/ORG-R1-parte03.md) e [parte 04 — decisão final](automacao/ORG-R1-parte04.md). Em divergência com a medição preliminar, vale a decisão final/errata, não o primeiro total medido.
- [Gate R2 — ignore/índice](automacao/ORG-R2-GATE-parte01.md) e [gate R3 — movimento/compatibilidade](automacao/ORG-R3-GATE-parte01.md).
- [ORG-R4 limpeza nominal](automacao/ORG-R4-LIMPA-parte01.md). O gate original R4 deve conferir limpeza e esta política juntos; documentação não repete remoções nem fecha o gate humano de release.
