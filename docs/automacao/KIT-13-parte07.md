# KIT-13 — checkpoint 07 (run661)

Readback de logs confirmado: Harness Ran17 failures0; Python Ran14 OK; baseline 204 fontes com live_changed=[]/copy_mismatch=[]/no_git=true. Achado na própria ferramenta: glob da lista de DLLs em verification.json não enumerava subdiretórios net6/netstandard; corrigido antes da prova final (nenhum hash inventado).

Teste JSON reforçado: duplicata agora parte de pacote de resto válido; anterior JSON incompleto poderia reprovar por falta de campos e mascarar remoção do guard de duplicatas. prove_mutations.py novo fornece 17 mutações C# +14 Python +2 extra (Standalone/CoreBridge), cada uma baseline0->mutante1->restaurado0, SHA byte a byte, build mutante obrigatoriamente exit0. Erro de compilação/timeout não conta como vermelho. Não mexe nos fontes vivos.

CoreBridge usa ICoreEvento e Json do Core existente em projeto separado; CoreHarness fake confirma disabled/observado, não jogo. Descoberta dirigida confirma EventosImpl é internal, logo vínculo ao CorePlugin requer facade explícita, não cast inventado. Será entregue binding por callbacks dos métodos públicos.

Prova final e mutações ainda pendentes. Revisão independente não realizada pelo implementador.
