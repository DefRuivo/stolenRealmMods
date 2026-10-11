# KIT-07R — parecer independente de KIT-07

## Identidade, escopo e conclusão

REPROVADO: nove achados F1–F9 confirmados por execução offline e leitura do estado resultante. Revisão concluída não significa entrega KIT-07 aprovada, aceite humano nem publicação/DoD.

- Implementador: t_c364710f, run634, perfil default.
- Revisor: t_96d0c463, run636, perfil default, instância independente que não participou da implementação.
- Data local de abertura: 2026-10-09T21:36:05.504283-03:00 (terminal); repo C:/dev/stolen-realm, branch ci-validate-test.
- Nenhum produto alterado pelo revisor; apenas docs KIT-07R e provas/scripts em scratch/kit/KIT-07R-run636. Sem commit, push, publicação, jogo, save real, build, instalação ou deploy.
- Sandbox própria copia 11 arquivos do escopo vivo tracked/untracked e dependências, sem .git/perfil/credenciais. Repo auxiliar dos scanners tem .git novo local sem remote e caminhos explicitamente indexados, nunca git add -A.
- SUPERVISAO e PROCESSO-REVISAO lidos; política serial/econômica vigente do cartão preservada. Gates humanos não autorizados.

## Veredito por critério de aceite

| Critério | Veredito | Prova / lacuna |
|---|---|---|
| Identidade viva e autoria independente | OK / PASSOU | 11 identidades coincidem entre origem/cópia/handoff; baseline614 tools sem mudança/remoção no fechamento; runs636 !=634 |
| JSON + PNG + logs selecionados | ACHADO / FALHOU | Nominal funciona, mas JSON escapado fica inválido (F2), log BepInEx selecionado é descartado (F9), pacotes repetidos retêm arquivos não selecionados (F4) |
| Manifest, hashes e diagnóstico | ACHADO / FALHOU | Nominal hashes conferem; colisão manifest.json/relatorio.md quebra hashes (F5); manifest ignora resíduos (F4); bytes diagnósticos24 != disco1045 (F7) |
| Excluir saves e assemblies proprietários | OK no cenário exercitado | slot.es3, saves/slot.json e Assembly-CSharp.dll excluídos; prova negativa específica. Não é prova universal de detectar DLL renomeada. F9 é exclusão indevida, não vazamento de assembly |
| Sanitizar genericamente texto/logs, minimizar nomes/caminhos | ACHADO / FALHOU | Conteúdo nominal redigido; filename/manifest vazam prefixo/nome local (F1); credencial JSON pontuada/escapada sobrevive (F2) |
| Screenshots: aviso e revisão/exclusão sem promessa perfeita | OK em exportação nova; ACHADO na reexportação | PNG off por padrão, lista de revisão, aviso de nomes/chat e imagem marcada não sanitizada conferidos; PNG velho continua no disco após opt-in off (F4). Pixels/revisão humana NAO_EXERCITADO |
| Sem upload por padrão | OK / PASSOU offline | Upload True recusado antes da escrita; audit hook não detectou socket/subprocess/os.system no caminho nominal; mutação de socket foi refutada. Não prova contra código fonte futuro alterado |
| Limites de disco | ACHADO / FALHOU | Tetos contam entrada e ignoram saída/metadata, aceitam24->1045 e6->7 bytes; erro deixa pacote parcial (F7) |
| Exclusão segura / origem intacta | ACHADO / FALHOU | Nominal separado e pasta sem marcador seguros; origem marcada igual ao destino é alterada e destino filho aceito (F3); marcador inválido apaga pasta alheia (F6) |
| Fictícias sem valor/prefixo em stdout/stderr/JSON/relatório | ACHADO / FALHOU | Nominal do autor passa; prefixo em manifest/nome físico (F1), sufixo em JSON (F2) e traceback bruto em stderr (F8) reproduzidos. Provas da revisão só guardam booleanos/counts/hashes, não saídas brutas vazadas |
| Caminho positivo, defeito plantado e controle falso-verde | PASSOU discriminação exercitada | Suite autor14 OK,12 mutações, controle falso-verde recusado;9 positivos próprios mostrados FAIL individual em cópias mutadas; lacuna origem do autor completada por negativo adicional. Não prova modo individual sob toda adulteração possível |
| Runtime/pixels/desempenho/interferência | NAO_EXERCITADO | Offline/sintético não valida jogo; autorização específica ausente |

## Achados, fonte e efeito independente

### F1 — credenciais e dados pessoais em nomes / metadata

Fonte: tools/automacao/kit07/exportador.py:217, tools/automacao/kit07/exportador.py:223, tools/automacao/kit07/exportador.py:248, tools/automacao/kit07/exportador.py:288, tools/automacao/kit07/exportador.py:303.
Esperado: paths compartilhados e metadados sem valor/prefixo, nomes pessoais minimizados, referências consistentes.
Observado: prefix_in_manifest=true e prefix_in_physical_names=true; nomes_extras não minimiza metadata. Comentário em tools/automacao/kit07/exportador.py:302 diz que manifest é saneado, mas escrita não chama saneador. Dois testes próprios FAIL.
Correção: mapeamento genérico seguro de nomes/metadados, tratamento de colisões, integridade das referências; não apenas sanitizar JSON serializado e quebrar paths.

### F2 — regex em JSON vaza credencial e quebra estrutura

Fonte: tools/automacao/kit07/exportador.py:103; tools/automacao/offline/aut3_lib.py:51; tools/automacao/offline/aut3_lib.py:94.
Esperado: chave de credencial genérica redigida integralmente, JSON válido.
Observado: password: mantém valor; password com aspa escapada conserva sufixo, valid_json=false. Dois FAIL. Reconhecimento pelo autor na entrega não corrige o aceite.
Correção: sanitização estrutural/regras genéricas robustas e falha segura; se tocar lib compartilhada, conferir consumidores e contra-provas sem enfraquecimento. Não prometer anonimato/segredo perfeito.

### F3 — caminho de saída pode alterar a origem

Fonte: tools/automacao/kit07/exportador.py:201; tools/automacao/kit07/exportador.py:239; tools/automacao/kit07/exportador.py:257.
Esperado: origem nunca escrita; rejeitar igualdade e sobreposição canônicas antes de criar destino.
Observado: origem marcada==destino reescrita, hash e3904d4f820116fc0dd7045e11c2bdb0687b8d5d79510d3ff555791802df1e45 -> 87c309d1bc2c91a96cca16ac974a78579095acdb02828205e4c61d85f9b05a18; destino filho aceito. Probe filho usou orçamento por arquivo0 para limitar recursão; recursão ilimitada não foi executada. Dois FAIL.

### F4 — PNG/log antigo fica fora do manifest novo

Fonte: tools/automacao/kit07/exportador.py:201; tools/automacao/kit07/exportador.py:225; tools/automacao/kit07/exportador.py:297.
Esperado: exportação bem-sucedida contém só seleção/política vigente, ou reuso é recusado sem sucesso falso.
Observado: current_opt_in=false, png_in_manifest=false, png_on_disk=true. Log removido da origem permanece no destino. Dois FAIL; avisar/revisar imagem não basta se excluí-la logicamente deixa pixels no pacote.

### F5 — arquivos reservados sobrescritos após hashing

Fonte: tools/automacao/kit07/exportador.py:260; tools/automacao/kit07/exportador.py:304; tools/automacao/kit07/exportador.py:307.
Observado: hashes_match.manifest.json=false e hashes_match.relatorio.md=false. Um FAIL.
Correção: reservar/renomear destinos de metadata com regra explícita; manifesto/hash/bytes devem corresponder ao estado final, sem perda silenciosa de evidência.

### F6 — marcador inválido permite apagar pasta alheia

Fonte: tools/automacao/kit07/exportador.py:355; tools/automacao/kit07/exportador.py:358; tools/automacao/kit07/exportador.py:372.
Esperado: limpeza só de pacote próprio reconhecido, nunca pasta arbitrária/origem.
Observado: marcador de texto inválido suficiente; keep.txt e marcador removidos (2 arquivos), pasta alheia removida. Um FAIL em dados sintéticos exclusivamente.
Correção: validar identidade/conteúdo/proveniência/escopo e tratar links/arquivos alheios de forma segura. Nominal sem marcador passou, mas não comprova todos os alvos.

### F7 — limites não medem disco e falha deixa restos

Fonte: tools/automacao/kit07/exportador.py:229; tools/automacao/kit07/exportador.py:234; tools/automacao/kit07/exportador.py:270; tools/automacao/kit07/exportador.py:304.
Observado: budget24 / input24 / diagnostic24 / package1045; porarquivo6 / entrada6 / saída7. Ao exceder total, a.txt parcial fica sem marcador e limpeza nominal não o reconhece. Três FAIL.
Correção: tetos em bytes reais de saída/overhead com contrato claro, montagem atômica e rollback. Orçamento insuficiente pode recusar com ErroExportacao, sem parcial; não é obrigatório caber metadata em24 bytes.

### F8 — erro de I/O imprime traceback e credencial

Fonte: tools/automacao/kit07/exportador.py:240; tools/automacao/kit07/exportador.py:414; tools/automacao/kit07/exportador.py:416.
Observado: destino existente como arquivo -> exit1, FileExistsError/traceback, stderr_has_prefix=true. Um FAIL. Stderr bruto não foi persistido nem exibido pelo revisor.
Correção: capturar/sanear também I/O/paths em saídas de falha, distinguir domínio/infra0/1/2 e nunca aceitar etapa ausente como verde.

### F9 — exclusão indevida do log selecionado

Fonte: tools/automacao/kit07/exportador.py:67; tools/automacao/kit07/exportador.py:157.
Observado: BepInEx/LogOutput.log não existe no pacote; motivo assembly_proprietario apesar de ser texto. Um FAIL.
Correção: permitir logs selecionados/sanitizados sem permitir saves/assemblies/binários proibidos; não classificar todos os conteúdos do segmento como assembly.

## Comandos, resultados e evidências

Base de provas: scratch/kit/KIT-07R-run636/ (arquivos locais desta revisão, não ferramentas novas do produto).

1. Terminal na isolated: `bash tools/automacao/kit07/roda_testes_kit07.sh` -> exit0, Ran14 OK;12 mutações recusadas e falso-verde recusado. Log author-runner-verified.log. Modo individual contém14 pares e13 alvos únicos; origem_intacta não estava coberta pelos negativos do autor.
2. `python scratch/kit/KIT-07R-run636/run_review_checks.py` -> harness exit0 (coleta correta, NÃO produto aprovado); subprocess suite exit1, Ran24 /15 FAIL /9 OK /zero ERROR/skip;9/9 negativos próprios exatos. review-results.json, review-suite.log, negative-*.log.
3. `python scratch/kit/KIT-07R-run636/measure_effects.py` -> exit0; métricas acima em observed-effects.json, inputs/pacotes sintéticos removidos ao final de cada probe.
4. `python scratch/kit/KIT-07R-run636/final_verify.py` -> exit0; suite final exit1, Ran24 in0.231s, FAILED(failures=15); negativo extra de origem do autor Ran1/FAIL exato/exit1; identity_mismatch=[] e tools_changed=[]. verification-final.json, review-suite-final.log, negative-author-source-preservation.log.
5. Scanners reais check_segredos/check_padroes_segredo em repo auxiliar: nominais exit0, credencial plantada exit1, sem valor/prefixo nos logs; planta removida e remotes vazios. Logs scan-positive/negative-*.log. Complemento final de scanner/zip será emitido em parte nova, sem sobrescrever este parecer.

Histórico de obstáculos preservado nas partes03/05: launcher bash via Python falhou2 vezes (127) por path do host; mudou abordagem para terminal. Primeiro negativo reviewer porarquivo gerou IndexError (8/9), não verde; só teste do revisor ajustado e negativo passou a FAIL específico (9/9). Suite final aceita recusa segura do teto24 sem restos; produto ainda mostra mesma falha.

## Hashes vivos conferidos

- tools/automacao/kit07/exportador.py: c5fc715b083685ec209138d0dc56e0f9dc19abcabd9e430493746d6f2a625382
- tools/automacao/kit07/teste_exportador_kit07.py: 2dc7ea39e0834041f7176969aced4c58a19be200e4c84137289b895f65fb4f51
- tools/automacao/kit07/contra_prova_kit07.py: e4cc31d4a46e224c1287f66ea5dad8ef131d41d24353b3b9ea1a97310605272e
- tools/automacao/kit07/roda_testes_kit07.sh: 26ceff5dcdbeae4715052741f8bce02a48724a952acdb04a85b1ad5a6fd5f17d
- tools/automacao/offline/aut3_lib.py: 04f37b8e285ad7d429d0d01cd846523323ca0a403ce64203890e3c0538d6dc1a
- docs/automacao/KIT-07-entrega.md: 3991d8aa9e86c550600c3f008d1d4d2e10affadc9a70231c98a40dc52b099d58
- scratch/kit/KIT-07R-run636/test_review_kit07.py (suite final independente): e54a6be2ee2f94bd19a8a912036ce23b34ec75790f7ceac1a4a481da0001f6b1
- Demais identidades em identity-before.json e verification-final.json.

## Limitações / invariantes

Sem validação de pixels reais, runtime, desempenho, filesystem race/links ou anonimato universal. PNGs da suite são bytes sintéticos, não prova de captura em jogo. Tests offline não substituem gates humanos. Scanner de segredos limita-se aos padrões e arquivos selecionados na cópia, não exportações arbitrárias. Build/travas de mod/versionamento/pacotes Thunderstore não aplicáveis ao exportador Python sem alteração de mod; auditoria global de docs não reexecutada. Referências deste parecer serão conferidas por caminho/linha e hashes em fechamento.

## Handoff / próximo passo concreto

Correção KIT-07F t_a7318a33 criada no perfil existente default, obrigatoriamente por nova instância/autoria, não reviewer636. Sem especialista adicional registrado; perfil default é o do implementador original e não implica autoexecução nesta revisão. Foi conferido por readback SQLite read-only:
- t_96d0c463 -> t_a7318a33 (correção depende deste parecer).
- t_a7318a33 -> t_e2107a63 (KIT-08).
- t_a7318a33 -> t_10584ca5 (KIT-15).

Os consumidores não ficam liberados com produto reprovado. Comentário496 no pai original t_c364710f registra achados/rejeição e foi relido. Implementador deve corrigir F1–F9, reproduzir RED no antigo e GREEN no novo, entregar hashes e request_review no MESMO cartão de correção. Revisor diferente confirma critérios antes de concluir KIT-07F; não apagar história, enfraquecer travas ou duplicar revisão. Esta revisão encerra só seu parecer com review_outcome=rejected.
