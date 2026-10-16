# KIT-14F3R — revisão independente

Cartão t_59d49835; revisor run1523, diferente do implementador run1519 e do coletor run1498. Início: 15/10/2026 16:15 BRT (terminal). Escopo: revisão técnica somente; não modificar produto, instalar, publicar, autoaprovar ou conceder DoD/aceite humano.

## Parte 01 — entrada e limites

Lidos docs/SUPERVISAO.md, entrega docs/automacao/KIT-14F3-parte14.md e recibos de scratch/kit/KIT-14F3-run1519/final. Os resultados declarados pelo autor ainda NÃO são veredito do revisor. Branch main; alterações concorrentes preexistentes preservadas.

Candidato declarado: build/candidate/KIT04Adapter.SR.dll SHA256 010de6a67671f0a2a03654e54aebb3ca7ae64c11d50270c50c73b568e9dc72c9. Mutante declarado: 42f035340c1fdf44ca482b29a3baf123a74d68e870813f465435c49940ec4032. Identidades serão calculadas independentemente.

Pontos a refutar: lifecycle; leitura real da engine; três opt-ins e ausência; unicidade/remoção do PlayerLoop; correlação sessão/evento/frame/painel/PNG antes de rollback; integridade dos snapshots imediatos/config/PlayerPrefs; deploy opt-in; preservação do gate full-rstv. Testes novos devem ler prova real congelada e demonstrar reprovação pelo mesmo detector, sem fabricar runtime.

Estado inicial: INDETERMINADO em todos os itens. Não foi aberto jogo nem instalado plugin. A limitação declarada de render/tooltip/Runner/clique físico/performance pertence à retomada KIT14; não será silenciosamente aprovada.

Comandos executados nesta parte: git status --short; git branch --show-current; date -Iseconds; leitura de final-receipt.json e verification.json. Exit terminal 0; isso só prova leitura/contexto, não sucesso funcional.

## Parecer final — 15/10/2026, run1523

APROVADO TECNICAMENTE no escopo KIT-14F3: produtor passivo e evidência real existente. Nenhum defeito funcional bloqueante demonstrado. Libera a retomada do KIT14 para integrar o instrumento e executar a campanha remanescente; NÃO equivale a KIT14 integral, clique físico, revisão humana, UI/UX final, publicação ou DoD de mod. O revisor não instalou plugin, não abriu jogo e não alterou produto/fontes principais/evidência antiga.

Abreviações: BASE = scratch/kit/KIT-14F3-run1519/final; REV = scratch/kit/KIT-14F3R-run1523. Os caminhos e SHA256 de 69 arquivos efetivamente lidos estão em REV/review-identities.json. O candidato revisado é exatamente o da campanha, não a recompilação posterior.

### Identidades calculadas pelo revisor

- Candidato BASE/build/candidate/KIT04Adapter.SR.dll: 010de6a67671f0a2a03654e54aebb3ca7ae64c11d50270c50c73b568e9dc72c9.
- Mutante BASE/build/mutant/KIT04Adapter.SR.dll: 42f035340c1fdf44ca482b29a3baf123a74d68e870813f465435c49940ec4032.
- Pacote BASE/KIT-14F3-implementation-v2.zip: 2e856e813dd681ab8e031fd5a30ab27c3a28853019f2fd7a213197f4019a3dc8; 144 entradas únicas, manifest/CRC/tamanhos/SHA conferidos.
- Patch BASE/instrument-crlf.patch: 4642ef3e6ee4804a83c11fb061448c68564211854889619d24da877a00eed0c3. git apply --check exit0; NÃO aplicado.
- Gate histórico scratch/kit/KIT-14-run1498/postprocess/unchanged-gate/gate.py: ca3d859a25fc40415987082f32a3d1e30d06f88c3bbc8ae6d104b4b7f25fa2b4, preservado.

### Veredito por requisito

1. OK — causa de lifecycle. BASE/cases/on/boot01/preserved/LogOutput-isolado.txt:21,44,77 prova instalação1, OnDestroy frame0/Update0 e remoção após670 callbacks; adapter-runtime.json registra Unity-null=true/CLR-null=false, frame destruído1 e Update0/Destroy1. Fonte SRAdapterPlugin.cs:162–175 e assembly decompilado REV/plugin-resolved.cs:128–145 correspondem. O produtor antigo dependia desse Update morto. Não se afirma a causa interna do Destroy na engine; a causa operacional do passivo0 está demonstrada. Detector próprio on exit0; mutante real exit1.

2. OK — produtor observa engine real. BASE/sandbox/tools/automacao/runtime/KIT04Adapter.SR/SRPassiveRuntime.cs:115–148 e REV/candidate-resolved.cs:164–209 contêm Time.frameCount, GameObject.Find, activeInHierarchy, GetInstanceID, caminho de Transform e Input.GetMouseButtonDown. Evento preservado contém motor/sessão/frame/painel; API pública de bools não é usada como prova runtime. Fonte e assembly do host incluem RstvAllSkillTreesPanel. O mutante retira a observação do Tick e reprova o MESMO detector próprio; medidor autoral repetido também mutante1/ON0.

3. OK — opt-ins Core/Adapter/Passivo e ausência. SRAdapterPlugin.cs:240–245 e REV/plugin-resolved.cs:211–218 exigem os três. Seis controles reais: off, absent-flags, core-off, adapter-off, passive-off, adapter-absent; cada auditoria própria exit0, sem instalação de motor, eventos passivos ou arquivos de recorder. Configs antes/depois conferidas por seção/chave/valor; BepInEx reserializa comentários/CRLF e adiciona somente defaults false às chaves ausentes. Adapter ausente é comprovado também pela lista instalada e log. Zero efeitos significa zero coleta/callback/arquivos passivos; não significa zero mensagem de carga ou zero reserialização de .cfg.

4. OK na campanha observada — callback único/removido. Fonte SRPassiveRuntime.cs:39–59,63–112,120–123; assembly REV/candidate-resolved.cs:127–180. ON: uma instalação,670 callbacks,0 duplicados,0 pendentes ao final,0 motores após remoção e assinatura quitting removida. Mutante preserva lifecycle mas não eventos. Corrupção em memória callbacks_duplicados=1 reprova1 no item callbacks_unique. Não foi ensaiado hot-reload nem liga/desliga dinâmico no mesmo processo; não há promessa de ausência universal de vazamentos fora da campanha.

5. OK — evento→frame→janela→PNG→sessão antes do rollback. Sessão KIT14F3-run1519-final-on-20261015-155512; evento a06417bd08394e0994aa677f1c5b38f1; frame452; painel GUI Manager/Character Menu Manager Window/RstvAllSkillTreesPanel, instance_id -297694; captura cap-f6672b9b confirmada454. PNG real1920x1080,1920328 bytes, SHA256 d130380c44f831384676b3315a558054f3fef9c22a0ba2cb3249992094d3b515. O arquivo foi inspecionado: aba All Trees/Fire e árvore visíveis. recibo recorder_files_before_close confere esse PNG antes de fechar/restaurar. IDs/sessão/hash/frame do recorder e do probe congelado confrontados; runtime permanece literalmente NAO_EXERCITADO. Corrupções isoladas de sessão, frame e hash reprovaram1 nos itens próprios. NÃO se afirma simultaneidade nem leitura textual pós-render.

6. OK — isolamento e restauração. Nos oito boots: comandos de restauração/rollback/limpeza/release exit0 e ordem conferida; snapshots imediatos antes do launch e após restauração com115/53/5 arquivos, conjuntos/tamanhos/SHA e nenhum novo/removido/alterado. Comparador histórico run916/upstream911/roda911.py:35–77 recalcula árvore e recusa reparse points. Auditoria independente atual confrontou as três árvores reais contra TODOS os oito manifests iniciais e repetiu confronto após o build do revisor: igualdade. PlayerPrefs exportado somente para calcular hash, sem importar/modificar; temporário removido. SHA atual ce6049dd4c3f5394efff6ed1bedeb6399fd58fbb9a4d4bba913e30e8cf0944ee coincide com os dois hashes textuais de cada boot. Processo atual vazio, lock ausente, nenhuma junction/backup/perfil/dados descartáveis remanescentes. Registros atuais corroboram a coleta imediata original, não são um novo boot independente.

7. OK — Cloud inicial preservada. Quatro readbacks por boot mantêm app cloudenabled0 no sharedconfig; revisor confirmou estado atual0. Nenhuma escrita no toggle/VDF. O cache mudou durante a campanha e NÃO representa estado do servidor; sincronização remota não foi inspecionada.

8. OK — build/deploy protegido. REV/integrity-build.json exit0 (173 checagens): fixture XML insegura rejeitada pelo scanner (resultado1), sandbox seguro exit0; build novo Release --no-incremental -p:DeployToBepInEx=false exit0,75 avisos/0 erros. DLL nova08902a4aefac7fc025f234e9256ad1f7c0dd0220ce3d22d049304fffce66aacc não foi instalada e não substitui a candidata da campanha. Decompilação resolvida do runtime novo é byte a byte igual à decompilação resolvida do candidato. Não foi executado deploy=true no perfil do dono: o positivo solicitado é o scanner/build seguro, não uma instalação proibida ao revisor.

9. OK — produto, handler e trava preservados. Inputs de todos os casos recalculados: probe ba0f22b2608fc6b548cb12a9db433a51e3e9b0dfa726f0aacee32224c775f012, Core0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d e RSTV1d0b85e8d0f30d10c4fe7c4e044d30380537e8801a7d39875192459a2e51d5cc congelados. Um handler final RstvRunSkillTreeButton, party1/HUD ativo, physical_click=false. Gate histórico executado novamente com rstv-full: exit1/FALHOU_ACEITE_INCOMPLETO. Nada foi afrouxado, renomeado ou promovido a físico.

10. INDETERMINADO / fora deste aceite — campanha KIT14 integral: render/texto pós-frame, tooltip/ciclo, marcação/export in-game, Runner, controles físicos, performance ativa e segundo ambiente. Permanecem na tarefa KIT14; não são lacunas que desaparecem por aprovação do produtor. Também não há aceite humano/Thunderstore/UI/UX final.

### Testes próprios e limites de interpretação

REV/review.py leu a prova runtime congelada diretamente, sem importar o detector autoral. REV/test-execution.json conserva comandos/expected/exit. Foram14 execuções,869 predicados avaliados, incluindo reprovações esperadas; NÃO869 sucessos. Sequência principal: mutante1 antes de ON0, seis OFF/ausente0; cinco corrupções em memória1; evidência ausente2. As corrupções são exclusivamente testes negativos do detector, não fixtures apresentadas como runtime. A primeira versão do detector falhou por formato .cfg e recorder OFF sem sessao; os resultados estão preservados em REV/first-red. O detector foi corrigido, nunca a evidência.

Comandos principais realmente executados (cwd C:/dev/stolen-realm):

    python scratch/kit/KIT-14F3R-run1523/review.py mutant
    python scratch/kit/KIT-14F3R-run1523/review.py on
    python scratch/kit/KIT-14F3R-run1523/integrity-build.py
    python scratch/kit/KIT-14F3R-run1523/final-checks.py
    ilspycmd -r C:/dev/stolen-realm/lib -t KIT04Adapter.SR.SRPassiveRuntime <DLL>
    python scratch/kit/KIT-14-run1498/postprocess/unchanged-gate/gate.py rstv-full

Scripts/saídas usam raízes novas e recusam sobrescrever resultados; não repetir cegamente o mesmo destino. final-checks.py exit0: confronto pós-build/PlayerPrefs, mesma decompilação, gate histórico1 e detectores autorais mutante1/ON0. Não houve timeout/skip contado como verde.

Observação documental, não reprovação funcional: isolamento/registro.json é recibo textual chave=valor e isolamento/restauracao.json tem escapes Windows inválidos para JSON. Extensão .json não foi tratada como contrato válido. Hashes de registro, manifests, comandos e result.json válidos sustentam a conclusão por fontes independentes. Evidência histórica não foi reformatada. O leitor que quiser consumir esses dois arquivos deve tratá-los como recibos textuais; json.loads reprova e isso está documentado na parte03. Não se abre retrabalho para reescrever prova imutável.

### Encaminhamento

Concluir somente a revisão técnica t_59d49835 para liberar o filho KIT14 t_a1f38855. O patch continua sandbox, aplicável e não aplicado; a integração e coleta remanescente pertencem à retomada, não foram realizadas furtivamente nesta revisão. Sem commit, push, deploy ou publicação.

Partes de acompanhamento: KIT-14F3R-parte02.md até parte07.md; resultados e identidades em REV. O parecer presente é o veredito consolidado.
