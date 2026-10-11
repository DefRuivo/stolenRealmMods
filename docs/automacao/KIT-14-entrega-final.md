# KIT-14 — entrega consolidada PARCIAL do run699

Cartão: t_a1f38855. Implementador: default/run699. Data: 10/10/2026; último estado operacional medido às 13:17:26 -03. Este documento complementa a entrega do run698 sem a sobrescrever. NÃO conclui a validação ponta a ponta, NÃO aprova DoD e NÃO autoriza publicação.

## Resultado e decisão vigente

Preparação, build e ferramentas OFFLINE exercitadas com sucesso após uma falha corrigida somente no harness. A rodada EM JOGO não foi iniciada: o mecanismo entregue isola BepInEx, mas não demonstra isolamento preventivo do save/caminho persistente consumido pela aplicação.

A decisão B do dono (corpo/comentários do cartão, 10/10/2026 13:05) está aplicada: limiares prévios de performance DISPENSADOS. A coleta futura será exploratória, sem PASSOU/FALHOU de performance. Não pedir novamente tolerâncias ou consentimento genérico. KIT-G2 B1–B6 autoriza somente instância/perfil/save descartáveis, sem estado pessoal/publicação.

## O que realmente rodou

### 1. Inventário, sandbox e guarda antes de build

- `preparar.py`, terminal exit0: 874 tracked + 470 untracked; 1343 arquivos copiados com hashes iguais, única exclusão explícita `nul` (dispositivo Windows preexistente). Não foi editado esse arquivo nem alterações manuais do dono.
- .git/remote/credenciais ausentes da sandbox; referências DLL locais copiadas exclusivamente para compilação, fora de qualquer pacote redistribuível.
- Três documentos ignorados necessários ao pacote foram suplementados, byte a byte, na sandbox: CHANGELOG.md, README.en.md, docs/primeiro-uso.md do KIT-15. Fonte vivo intocado; `ignored-supplement.json` registra identidade.
- `check_deploy_optin.py --raiz <sandbox> --json`: exit0, 6 targets, sem_optin=[]. Reexecutada antes de cada build. XML negativo sem opt-in: exit1 e achado real. Não houve build antes do preflight.
- USERPROFILE/APPDATA/LOCALAPPDATA redirecionados no ambiente dos subprocessos e MSBuild; DeployToBepInEx=false explícito. Esses envs não são apresentados como isolamento do save runtime.

### 2. Builds identificadas, sem deploy

`dotnet build <csproj-sandbox> -c Release --no-incremental -p:DeployToBepInEx=false ...` — exit0 para AUT4Probe e KIT04Adapter.SR, este incluindo Core.

| DLL em sandbox | SHA256 medido | Bytes | Estado |
|---|---|---:|---|
| AUT4Probe.dll | 679365e2b0496a33b1c9bb77a7e561b40438ae1443d4120f661b2c5f6845dc57 | 56320 | Build, NÃO carregada |
| KIT04Adapter.SR.dll | ab2da7587436b9457d152b110ef50014567d430747f85794678e0ab08456f3b0 | 31744 | Build, NÃO carregada |
| KIT04Core.dll | 4b318522f51b2ec4ed212f24a15861a0fd907104e561a07e27f300c3fc714eb3 | 33792 | Build transitiva, NÃO carregada |

AUT4Probe: 0 erros/1 aviso; Adapter+Core: 0 erros/65 avisos. Avisos nullable/System.Net.Http preservados, não corrigidos fora do escopo. Logs brutos em `scratch/kit/KIT-14-run699/logs/build-*.stdout.log`.

O rebuild gera identidade nova; não fingir igualdade com o probe congelado anteriormente no KIT-G2. Nenhuma dessas DLLs foi instalada. A DLL do jogo na instalação e a lib de referência foram lidas/hashadas: ambas 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a (7712768 bytes), intocadas e não redistribuídas.

### 3. Pacote e lifecycle local executados pelo CLI real

Candidato local `pacote-resume/kit-rstv-0.1.0.zip`: 175059 bytes, 42 membros/41 payload; SHA256 d5f42854a5f852b813f181d302bdbcc2a90498493e7d0f3da1af0a54bf606bf7. Sem DLL/PDB/EXE. Montar=PACOTE_LIMPO/exit0; verificar=OK/exit0, problemas=[], testzip sem erro; hashes lidos de volta.

O pacote é fonte/ferramentas, não pacote binário publicado. Os nove hashes vivos KIT-15 confrontados com o handoff run691 coincidem; não alegar identidade do ZIP entre montagens, pois inclui metadado temporal.

Ferramentas extraídas executadas sem Hermes/IA/credenciais fornecidas no subprocesso:

- Suíte autor: Ran 18 tests, 0 failure/error/skip, exit0.
- Contra-prova: baseline=True, recusados=7/7, exit0. Mutações reais, saídas individuais registradas; não são controles de jogo.
- Instalar → status INSTALADO → leitura/confronto dos 41 hashes.
- Arquivo instalado adulterado → status DIVERGENTE. CLI status exit0 não confundido com sucesso funcional.
- Atualizar → bytes reparados/INSTALADO. Mesma versão; upgrade entre versões NÃO exercitado.
- Remover → AUSENTE e todos os payloads removidos; sentinela alheia intacta.
- Rollback da remoção → INSTALADO e 41 hashes restituídos.
- Remover novamente → AUSENTE; journals/backups previstos pelo contrato permanecem. Não afirmar pasta vazia.
- ZIP com membro adulterado → verificar ACHADO/exit1; original intacto → OK/exit0. Controle negativo OFFLINE.

### 4. Falha inicial preservada, sem falso verde

Primeiro `test_qualificar.py`: exit1, Ran 7 tests, 2 failures/2 errors/0 skip. O harness confundiu veredito de montar (PACOTE_LIMPO) com o de verificar (OK), interrompendo extração; demais failures/errors foram cascata. Produto não foi alterado. Montagem inicial tinha 39 membros por omitir três documentos ignorados; não foi promovida a candidata correta.

Retomada dirigida `test_continuar.py`: exit0, Ran 5 tests, 0 failure/error/skip, em 71.912s. Não recompilou nem reiniciou etapas já prontas. A execução inicial continua conservada em qualification.log/offline-result.json; a retomada, em qualification-resume.log/offline-result-resume.json. Não somar as duas como suíte única verde.

### 5. Preservação e travas

Reconferência por caminhos+SHA após as operações: 1343 arquivos vivos sem modificação/removal; árvores pessoais BepInEx 53 arquivos, LocalLow 111, Abyssus 5, exatamente iguais à baseline. Snapshot privado em personal-before.json permanece local, não é conteúdo de save distribuído.

Travas gerais em leitura: check_segredos/check_padroes_segredo/check_dupes/audita_docs exit0 cada; escopo versionado explicitado, não aprovação universal dos untracked. Nenhuma trava enfraquecida.

Reconferência às 13:17:26: jogo FECHADO (STOLEN_PROCESS_COUNT=0), front-unica check OK/exit0, HEAD d82894ebe95d97f26b7989a848372c691dcb8ef6, índice vazio. Nenhum git add/commit/push, instalação pessoal, boot/encerramento de jogo, navegação/save/publicação ou mudança de modelo/política/cron/prioridade.

## Impedimento runtime — prova e próximo passo

- `runtime-isolado.sh` isola core/plugins/config/log do BepInEx e fotografa saves pessoais; seu próprio contrato diz não carregar save. Lançamento run usa Steam/instalação normal, sem save descartável encanado ao processo.
- `isolacao.sh` copia saves/cria marcador e testa containment, mas não redireciona o caminho que o jogo consome. Não executar save-restore: escreveria no local pessoal.
- `coletor.py:1593–1879` recebe perfil_dir para BepInEx e usa Popen(cmd) com doorstop; não oferece nessa rota redirecionamento do caminho persistente do jogo.
- Decompilações dirigidas, exit0: FileSystem.persistentDataPath = _cachedPersistentDataPath ?? Application.persistentDataPath; GlobalSaveDataManager.Filename = Path.Combine(FileSystem.persistentDataPath, "GlobalSaveData.json"). Evidência conservada em compiled-*.txt/compiled-results.json. Leitura dirigida, não dump completo nem DLL modificada.
- Busca UTF-8 dirigida sobre tools/automacao e helpers scratch/kit/cap1 examinados não encontrou mecanismo pronto que demonstre save isolado consumido. A busca tem escopo declarado em baseline.json, não afirma inexistência universal de alternativas.

PASSO SEGUINTE: fornecer ambiente/conta/instância descartável com caminho persistente comprovadamente separado, ou encaminhar isolamento preventivo de save a uma frente especializada, com revisão independente e controle negativo antes do boot. Não trocar/restaurar save pessoal, não patchar Assembly-CSharp, não introduzir alteração de gameplay nesta auditoria. Perfil real disponível para atribuição: apenas default; não inventar especialista nem autoatribuir seguimento.

## Cobertura por critério

| Critério | Estado desta execução | Limite |
|---|---|---|
| Autorização B1–B6 e dispensa B | PASSOU documental | Não amplia escopo pessoal |
| Preflight de deploy e controle negativo | PASSOU offline | CLI real, antes de build |
| Build/identidade/pacote | PASSOU offline | DLL carregada: NAO_EXERCITADO |
| Install/update/remove/rollback | PASSOU offline, escopo limitado | Reparação mesma versão; nenhum lifecycle em jogo |
| Ferramentas básicas sem Hermes/IA/credenciais | PASSOU offline | Funcionalidade em jogo: NAO_EXERCITADO |
| Saves/fontes pessoais intactos | PASSOU na comparação byte a byte | Nenhum boot; não prova preservação após runtime |
| Clique físico → janela → tooltip/conteúdo → PNG | NAO_EXERCITADO | Sem instância descartável comprovada |
| Relatório → marcar problema → exportar | NAO_EXERCITADO ponta a ponta | Sem evidência UI/runtime nova |
| Runner ativo e erro/controle negativo em jogo | NAO_EXERCITADO | Controles offline não substituem jogo |
| Mod funcionando sem kit | NAO_EXERCITADO | Sem boot/comparação funcional |
| FPS/tempo de quadro média/p95 | NAO_EXERCITADO | Nenhum dado bruto; não estimado |
| Memória/disco com e sem recorder | NAO_EXERCITADO | Bytes de ZIP/DLL NÃO são impacto do recorder |
| Segundo ambiente runtime/portabilidade | NAO_EXERCITADO | Diretórios offline não equivalem a segundo host/perfil jogado |
| Revisão técnica/visual independente | PENDENTE | Filho KIT-14R existente, não liberado |
| Aceite humano/publicação | PENDENTE/NAO_EXERCITADO | Gates/DoD separados |

Cenários pre-registrados: RSTV-6-readonly-personagem, RSTV-6-readonly-skills-pontos, RSTV-21-janela-ciclo, RSTV-21-tooltip-restauracao, RSTV-26-placeholders, RSTV-25b-dependencia, RSTV-geometria-clipping, tooltips_shrines e C1–C7 AUT-4: todos NAO_EXERCITADO em jogo. C0 e fixtures/controles de lógica somente offline não são promovidos a runtime. Personagem, evento/frame/config runtime e esperado independente de gameplay não foram medidos nesta rodada.

Coleta exploratória futura: mesma cena/cenário, duração e configuração com/sem recorder, registros crus e identidade da build; limiares DISPENSADOS. Sem medição disponível: NAO_EXERCITADO, não estimativa e não aceite de performance.

## Evidências e hashes

Raiz: `C:/dev/stolen-realm/scratch/kit/KIT-14-run699/`.

- baseline.json: 295e4e4d63f29f8955e4d347915f60fb46cf516b7f1f2953d4bd684d939798aa.
- offline-result.json (execução inicial falha): 3163a479b951403c394cf259aea7f68505f4e04a5f5b79c2e967634717a42aa9.
- offline-result-resume.json: d7a8927f38b3f22e267c97c51103e480d9c69bce40adaf8834fc1e1b47defeec.
- Pacote candidato e builds: hashes nas seções acima, readback em identity-readback.json.
- Harnesses: preparar.py, test_qualificar.py, test_continuar.py; outputs reais em logs/ e logs-resume/.
- Checkpoints novos: docs/automacao/KIT-14-parte03.md até parte10.md; anteriores preservados.
- Inventário final de hashes/estado: verification-final.json, a ser gerado pelo selamento imediatamente após este relatório. O selamento não executa runtime nem concede aceite.

Estado operacional adequado: BLOQUEADO por falta de ambiente runtime com save preventivamente isolado, não por limiares. KIT-14R t_9ce7d260 permanece dependente; não concluir o cartão apenas porque as ferramentas offline passaram.
