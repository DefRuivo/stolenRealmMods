# KIT-15R — revisão independente de KIT-15

Cartão: t_effde07f. Data: 10/10/2026.
Implementador: default/run677, t_10584ca5.
Revisor inicial: default/run678; retomada e fechamento: default/run685, instância distinta do implementador, sem participação no produto.
Workspace: C:/dev/stolen-realm, branch ci-validate-test.

## Parecer: REPROVADO

A revisão foi executada e concluída; o pacote KIT-15 NÃO está aprovado. Há 12 grupos de achados F1..F12, inclusive perda de arquivos/propriedade, rollback falsamente bem-sucedido, ausência de dependências e escrita/remoção fora do destino. O conserto já registrado é KIT-15F t_d83f3ef6; exige nova implementação seguida de revisão nativa independente antes de conclusão. Não criar outra revisão duplicada.

Nenhum arquivo de produto foi editado. Instalações/remoções dos testes ocorreram SOMENTE em sandbox temporária do revisor. Nenhum jogo foi aberto/fechado, nenhum save carregado, nenhum perfil real instalado, nenhum build/deploy/publicação/commit/push executado. Política/modelos/crons/prioridades intactos. Gates humanos/DoD não satisfeitos por este parecer.

## 1. Escopo, identidade e preservação — OK / PASSOU

Lidos SUPERVISAO.md, PROCESSO-REVISAO.md, entrega e checkpoints existentes; retomada conservou partes01..07 e evidências run678 após interrupção por quota. Novos checkpoints partes08..11 e evidências run685, sem apagar histórico.

Comando de coleta própria: `python scratch/kit/KIT-15R-run685/test_resume_review.py` (exit0 do coletor). Ele leu inventory-before.json e comparou SHA256 antes/depois: `LIVE_INVENTORY 535 CHANGED []`. São os 535 arquivos inventariados, NÃO uma afirmação sobre todo arquivo do repositório. Sandbox copiada com fontes tracked/untracked existentes, sem .git/remote/credenciais/perfil. Nenhuma DLL utilizada nos testes; plantas binárias são bytes sintéticos, não DLL proprietária.

A ferramenta de coleta não altera o produto nem regrava oráculos históricos; os dois oráculos foram copiados com identidade byte a byte:

- test_review_kit15.py: SHA256 1efb6c1850482c27b2eb0ec52a1042411061229195c28590f6d9abab7476a449
- test_extra_kit15.py: SHA256 e68eb481a618f700c373f6d418d85f503d9fe46823a27416833a307ee95a9d56

Provas: scratch/kit/KIT-15R-run685/verification.json e finish-verification.json; inventário original scratch/kit/KIT-15R-run678/inventory-before.json.

## 2. Instalar / atualizar / remover / rollback — ACHADO / FALHOU

O caminho nominal funciona parcialmente, mas não satisfaz as garantias do instalador.

Positivos reais P1..P3: instalar41 com hash individual, remover restaurando arquivo do usuário DIFERENTE do payload e preservando alheio; atualizar1/41 e rollback retorna os bytes anteriores; hash corrompido na cópia gera rollback sem payload parcial. Os três PASSOU são limitados aos cenários medidos, não aprovação do critério inteiro.

F3 — atomicidade: OSError sintético na terceira cópia deixa dois fontes instalados e recibo null. `instalador.py:309..372` copia antes de persistir journal/recibo. Teste test_F3_copy_exception_must_not_leave_partial, effects em verification.json; FAIL/AssertionError, não ERROR. Esperado: ausência de instalação parcial e estado anterior recuperável.

F4 — rollback da remoção: instalar41 → remover → rollback informa rc0/problemas[]; observado0 payload restaurados e status DIVERGENTE/41 faltantes. `instalador.py:399` marca arquivos apagados como criado; `:257..259` os apaga novamente na reversão. Teste test_F4_rollback_removal_restores_all_files, FAIL; CLI separada run678/logs/cli-rollback-removal.txt e cli-status-after-rollback.txt confirma efeito, não apenas API.

F5 — propriedade: arquivo preexistente IDÊNTICO é apagado; instalar→atualizar→remover deixa Json.cs antigo do próprio kit em vez do estado inicial ausente; atualizar sem opcionais deixa cinco arquivos órfãos, recibo36. `instalador.py:332..343` não preserva origem de propriedade corretamente; `:362..368` substitui a lista sem tratar retirados; `:391..399` remove segundo backup, não propriedade original. Três testes test_F5_* FAIL.

F6 — backup corrompido: remover restaura literalmente `corrupted backup` e declara rc0/problemas[]. `instalador.py:215..222,391..395` calcula SHA de restore mas não confronta identidade original na remoção. Teste test_F6_remove_refuses_corrupted_original_backup FAIL. Esperado: falhar fechado e preservar recuperação, sem substituir destino por backup inválido.

## 3. Manifesto / recibo / integridade — ACHADO / FALHOU

F2: manifesto não é autoridade. Fonte adulterado aceito, Core obrigatório ausente aceito (instala29), arquivo não listado instalado, ZIP adulterado com CRC válido aprovado, ZIP contendo somente manifesto{} aprovado e recibo{garbage:true} recebe INSTALADO/0 arquivos/pacote null.

Fontes: `instalador.py:103..110` valida apenas campo schema; `:129..167` enumera disco e recalcula SHA, ignorando lista/hashes declarados; `:194..201,419..433` não valida contrato do recibo; `pacote.py:216..234` só verifica CRC/scan/presença do nome manifesto. Oráculos test_F2_* (cinco na suíte principal + recibo na extra), todos FAIL sem ERROR/skip.

Esperado: validar schema/tipos, obrigatórios, fechamento exato de payload e hashes declarados antes de efeitos; recibo inválido não vira instalação válida.

## 4. Confinamento de caminhos — ACHADO / FALHOU, alta severidade

F12: manifesto com componente id `../../outside` modifica Json.cs sintético fora de --destino e retorna0; recibo rel `../outside.txt` apaga arquivo sintético externo e retorna0. Ambos ocorreram dentro da raiz temporária de teste; nenhum arquivo real do usuário foi alvo.

Fontes: `instalador.py:165,328,385..397` concatena IDs/rel sem validar confinamento. Testes extras test_F12_manifest_id_confined_to_target e test_F12_receipt_cannot_delete_outside_target: FAIL/AssertionError. effects extra-results.json: foreign_changed=true; foreign_exists=false.

Esperado: rejeitar traversal/absolutos/drive/UNC e escapes de origem/destino/backups/recibos antes de escrita/remoção. Não ampliar exploração ao perfil real.

## 5. Dependências reais e uso fora do ambiente do autor — ACHADO / FALHOU

F8: em árvore extraída sem layout do repo/variáveis do autor, teste_kit15.py e pacote.py montar retornam infra2; shell publicado retorna2. `pacote.py:45..54` exige tools/automacao, que não existe no layout distribuído. Oráculos test_F8_* FAIL; os exits2 dos produtos são ausência de exercício, NÃO verdes.

F9: Runner procura components/runtime/coletor.py ausente (distribuído em recorder); Viewer não encontra cenarios/kit09.py; Integração não resolve ciclo/decisao/kit10/aceite nem pertinencia.json; ProjectReference do Adapter aponta components/KIT04Core/KIT04Core.csproj ausente, enquanto pasta entregue chama core. Quatro test_F9_* FAIL em extração real. Teste de ProjectReference é resolução lexical, NÃO compilação C#.

SDK contém somente KitSdk.csproj e RegistryV1.cs; exemplos/contratos/schema não são distribuídos. Compatibilidade/versionamento descritivos não eliminam dependências transitivas faltantes. Core/Adapter não foram transformados em dependências obrigatórias de mods existentes.

Uso sem Hermes/IA/rede/credenciais/assinatura: PASSOU para comandos offline de arquivo executados com Python stdlib, sem essas dependências. Uso funcional básico SEM Python/SDK: NAO_EXERCITADO; modo manual só copia fontes/scripts e compara tamanhos. Não prova execução do kit, portanto critério amplo não aprovado.

## 6. Descoberta / seleção sem usuário fixo — OK / PASSOU limitado

Suíte do autor18/18 inclui test15/test16. Execução própria de descoberta com HOME/USERPROFILE/APPDATA/KIT_RSTV_CONFIG sintéticos e KIT_RSTV_HOME explícito: exit0, destino_origem=ambiente:KIT_RSTV_HOME, destino_kit exatamente a pasta sintética. Log run685/logs/discovery.txt. Detectou caminho existente do jogo por descoberta, mas não abriu jogo, leu save nem instalou perfil; perfil_bepinex=null.

`descoberta.py:60..98` deriva config/raiz do ambiente; nenhum nome de usuário fixo no fonte KIT-15. Este PASSOU é da fonte viva, NÃO valida o arquivo antigo distribuído no ZIP (F1).

## 7. Documentação PT-BR / EN / primeiro uso / exemplos / changelog / compatibilidade — ACHADO / FALHOU

Presença: PT/EN/primeiro-uso/changelog OK, verificada por membros do ZIP. Compatibilidade honestamente distingue Python3.14.7/Windows11 medidos de Unity/BepInEx/ModAPI e Linux/macOS NÃO_MEDIDOS nesta rodada; runtime não exercitado.

F7: comando documentado `python tools/pacote.py verificar <zip>` sem --json levanta KeyError zip_membros/exit1; test_F7_verifier_documented_cli FAIL. Com --json nominal retorna0 (histórico run678/logs/verifier-json.txt), diferença não justificada nos guias.

F9 documental: `README.md:12` distribuído sob docs aponta docs/docs/primeiro-uso.md inexistente. Primeiro-uso:35 publica comando F7; :74 promete comparação com manifesto, mas input é rehashado; :75..76 promete atomicidade refutada por F3; :107 promete rollback remoção refutado por F4; :118 promete preservar preexistente refutado por F5. :143..144 menciona contrato/exemplo SDK não distribuídos. :125..137 modo manual não comprova funcionamento sem Python, nem equivalência de integridade por comparação de tamanho.

## 8. ZIP / release candidato local — ACHADO / FALHOU

F1: pacote entregue é diferente das fontes vivas. Medição própria compara TODOS41 payloads com suas origens; exatamente um diverge, tools/descoberta.py. O 42º membro é manifesto gerado, não fonte com origem direta. `finish-verification.json/member_identity` contém hashes individuais e caminhos.

ZIP autor: scratch/kit/KIT-15-run677/cli/pacote/kit-rstv-0.1.0.zip
SHA256 126e367b059562ff248d469201ac325142a3d5342ec84458fb75201bdf5708cb
164881 bytes;42 membros;CRC/testzip null;zero DLL.

ZIP tools/descoberta.py: a04ffc59125cff05ce2b994049709cb6375ca7fdfc4118150cdae0913dae0f97
Fonte viva:10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86
Diferença no comportamento raiz_efetiva, não apenas timestamp. Fonte vivo `descoberta.py:89..98`.

Montagem própria run678 gerou42 membros CRCnull, scan0, SHA256 a524746a8292d3be417c209a9e493c8a07295f22f46ac9c511633e7c7bd352ad, preservada em pacote-proprio. Instalar a partir de ZIP41 funcionou offline, porém rollback/uso extraído falham como acima. Candidato local não é distribuição aprovada.

## 9. Scan de segredos/conteúdo e DLL proprietária — ACHADO / FALHOU

P4/P5 positivos: nominal0 → segredo AWS sintético detectado1 → removido0; DLL sintética em ZIP detectada. ZIP nominal sem DLL foi reaberto independentemente. Esses cenários PASSOU não aprovam a cobertura completa.

F10: chave JSON password entre aspas passa; diretorio bin/Assembly-CSharp.dll é ignorado; PermissionError de input vira achados[]. `scan.py:31,79,89..90`. Três test_F10_* FAIL sem ERROR; segredo sintético nunca é credential real. Corrigir formatos reais e distinguir erroIO infra2 de limpo.

Travas próprias `check_segredos.py`, `check_padroes_segredo.py`, `check_dupes.py`, `audita_docs.py`: exit0 cada. Logs run685/logs/gate-*.txt. Scanners Git cobrem escopo versionado, não aprovam automaticamente novo KIT-15 untracked nem eliminam F10.

## 10. Testes reais / positivos e controles negativos — execução PASSOU; garantia do autor FALHOU

Comandos reais da retomada:

- python scratch/kit/KIT-15R-run685/test_resume_review.py → coletor0; review27 testes22FAIL/5OK (exit1), extra3 testes3FAIL (exit1), autor18OK (exit0).
- Mutante real do restore P1 →1FAIL/0ERROR/0skip (exit1), removida mutação →1OK (exit0).
- Oráculos próprios total30:25FAIL/5OK, zeroERROR/skip. Estes25FAIL são achados de contrato, não falha de infraestrutura.
- Histórico run678:22 negativos individualmente, cada um1FAIL/0ERROR/skip/exit1; cinco positivos discriminados por mutantes, cada1FAIL/0ERROR/skip/exit1; baseline restaurada5OK/exit0. Contagens conferidas programaticamente nesta retomada. P1 inicialERROR não foi contado; control-P1-bytes substitui prova inválida, sem apagá-la. Shell inicial com127 foi corrigido no ORÁCULO do revisor, histórico preservado; nova medição retorna infra2, não127.

F11 reproduzido por `python scratch/kit/KIT-15R-run685/test_finish_review.py` (coletor0): contra limpa baselineTrue/6de7/exit1; após C# sintético inerte em sandbox/Core/bin, contra reporta7de7/exit0. Porém log-07: `setUpModule ... ERROR`, `Ran 0 tests`, `FAILED (errors=1)`. Falso verde do autor confirmado. `contra_prova_kit15.py:108,170..175` não exige N>0/alvoFalhou/0ERROR/skip. Esta ocorrência NÃO prova que teste rodou ou defeito foi pego. Isca removida depois.

## 11. Hashes dos arquivos vivos

Os12 hashes, inclusive docs/runner, estão integralmente em run685/finish-verification.json/source_hashes, calculados nesta instância. Identidades principais:

instalador.py 81243659708035c77b68de14eecb6018ffbf5858b2445440701283604e1b9596
pacote.py c006c0ff1061ae2117691207cca9e0ad39a7fc5e58e6297e02ec7c8406b964cd
scan.py a9fe0bfff406356607a54947174247244f4d6d5d14624b7490bfd53244c11dba
manifesto.json 37096997a661627e70313056597454cfa721ca0947e3c2b99db9a0e13d5fc0a1
contra_prova_kit15.py c2910ac29213bcb2ea27383a6b8a3b7f29b5349bad7c1d2e4c6cb57c8702b12d
teste_kit15.py 14e0b537f38ff05d735a5d35d8e22911af8a0395c9f4b60ec45543f6db831019

## 12. Lacunas, autorização e próximo passo

NAO_EXERCITADO: buildC#/preflightdeploy, carga real BepInEx/Unity, jogo/personagem/evento/frame/pixels/UIUX, save/perfil do dono, desempenho, segundo host/SO, uso funcional sem Python/SDK, gates humanos e publicação. Não houve build porque preflight não foi exercitado; não buscar bibliotecas do jogo nem chamar build sem travas. Dados sintéticos não provam runtime. Nenhuma autorização tácita de instalar/publicar foi inferida.

Nenhum push/tag/GitHubRelease/Thunderstore/publicar:true executado: OK no escopo desta revisão. Nenhuma declaração de versão publicada.

Conserto existente KIT-15F t_d83f3ef6 deve resolver F1..F12 por nova instância implementadora, preservar oráculos/baselines e entregar hashes novos com `kanban_request_review`, seguido de revisor diferente por item. Só complete de correção revisada libera os dependentes.

Arestas adicionadas e lidas de volta por kanban_show(t_d83f3ef6): KIT-15F → KIT-G2 t_f19310d3, KIT-14 t_a1f38855 e KIT-G4 t_b001720d. Sem desbloquear gate nem alterar autorização. A autorização G2 registrada em09/10/2026 continua com seu escopo, mas não transforma parecer REPROVADO em aprovação do pacote.

Encerrar t_effde07f significa PARECER ENTREGUE, não aprovação técnica do produto nem aceite humano/DoD. O histórico permanece e a correção é o próximo trabalho, não execução nesta instância revisora.
