# KIT-08R — revisão independente: REPROVADO

Cartão t_70608c71, reviewer run648 (perfil default, NOVA instância); implementador t_e2107a63/run643. Independência por instância/autoria: 648 != 643. Revisão OFFLINE realizada em 09/10/2026, data local inicial obtida no terminal 22:25:45 UTC-03.

Parecer concluído NÃO aprova KIT-08 nem DoD humano. Correção criada: **t_ac0f78f7 / KIT-08F**, em nova instância de implementação, com reconferência independente no mesmo cartão. Gates reais criados e lidos de volta: KIT-08F -> KIT-12 t_0a434c97; KIT-08F -> KIT-15 t_10584ca5. Concluir este cartão encerra o PARECER REPROVADO, não libera consumo do produto reprovado.

## 1. Identidade viva e preservação — OK / PASSOU

Workspace C:/dev/stolen-realm, branch ci-validate-test, estado com mudanças manuais/untracked preexistentes inventariado por `git status --short` antes da revisão. Nenhum fonte de produto editado; docs novos e harness/provas próprios somente. Sem commit/push/git add. Sem tocar mods, Assembly-CSharp.dll, gameplay, perfil/save, crons/modelos/política/prioridades.

Sandbox própria: `scratch/kit/KIT-08R-run648/sandbox/`. Cópia byte a byte de 27 arquivos tracked/untracked do escopo e dependências, sem .git/remotes/credenciais/perfil nem assemblies proprietários. Prova: identity-before.json + final-verification.json; SHA256 dos 27 arquivos vivo e copiado conferidos no fim, mismatch=[].

Identidades SHA256:
- tools/automacao/kit08/visualizador.py: 3d6d2983a845d1423859ef75f7f8e658cde7c14c0d4fe3ee23194d08a9789701
- tools/automacao/kit08/teste_visualizador_kit08.py: 840f62e9da178ea6c21af5f8a37e0fc0022b14999832bbfbc3395d5dfe079e7e
- tools/automacao/kit08/contra_prova_kit08.py: 9555233e989e76e691b42d3977063ab9399623f0593110294d3076476c876551
- tools/automacao/kit08/roda_testes_kit08.sh: 37de9d8de93f65b74eaf2df6296a63e9298a557479b78d3a08b4e3a1407db394
- tools/automacao/cenarios/kit09.py: 55f01e024e5e5ffd0c28b98ef492e2790c606d57d1dab4ae9d0258fba05feabb
- scratch/kit/KIT-08R-run648/test_review_kit08.py: 597b5ab38129d059e00ea17b50ba7a3b07e76a5ad904960d4f23e5b5cf435c14
- scratch/kit/KIT-08R-run648/review_controls.py: 575f2c4cec59b46b1f540f5c4ae325c9967e34710fc5d818f97b268eacf901cd

## 2. HTML fora do jogo, sem servidor/conta/Hermes — OK parcial

PASSOU: CLI gera HTML estático real, somente stdlib; inspeção estrutural não encontra script/iframe/object/embed/base/link externos nos casos positivos. Não exige servidor, conta ou Hermes para gerar/ler o arquivo.

FALHOU a alegação de arquivo autocontido quando há imagem: F8, imagem não embutida/copiada, dependente de caminho que pode não existir na pasta de saída. Browser/layout/acessibilidade visual NÃO exercitados nesta autorização.

## 3. Campos por caso/mod — ACHADO / FALHOU F8

Esperado/observado/motivo/prova/contexto/lacunas aparecem nos casos nominais. Contudo sessão string é descartada em tools/automacao/kit08/visualizador.py:371: variável recebe {} antes de testar isinstance(str) em 372. Teste Identity.test_session_string_preserved reprovou: SESSION_UNIQUE ausente no HTML.

Imagem local existente relativa à entrada (`assets/capture.png`) não resolve quando `--saida` vai a outra pasta. Código visualizador.py:293 mantém string sem resolver/copiar/embutir e em :298 usa como src relativo ao HTML. Teste Integration.test_image_reference_resolves_from_output reprovou pela inexistência do recurso resolvido, CLI exit0; stdout/hash e HTML reais em cli/image-location/. O arquivo de imagem do harness é um marcador sintético; teste comprova resolução/existência, NÃO pixels/decodificação PNG.

Correção: preservar sessão nas formas aceitas, resolver evidências e imagens com raiz do input/pacote e confinamento, copiar/embutir ou declarar lacuna sem dizer autocontido.

## 4. Comparação só com contexto compatível — ACHADO / FALHOU F3/F4/F7

PASSOU controle: jogo diferente é recusado, mesmo contexto nominal é comparável. Ambos testes mostrados FAIL sob defeito plantado seletivo.

F4: visualizador.py:131 compara campo somente quando ambas pontas têm valor. Config/personagem declarados só de um lado são aceitos. `mod` nem entra no contexto (:114, :237), ModA vs OTHER é comparável. Identity.test_one_sided_config_not_compatible, test_one_sided_character_not_compatible e test_different_mod_not_compatible reprovam. Correção: identidade/contexto suficiente por caso e simetria do declarado; não impedir automaticamente diferenças de fonte/DLL esperadas em uma candidata.

F3: visualizador.py:245 cria dict por id, ocultando duplicatas; :250 não aplica origem_sintetica(doc), mesmo quando a renderização dos casos aplica. Docs explicitamente rotulados fixture mostram baseline=PASSOU e candidata=PASSOU na comparação. Regressão é calculada pelo estado cru (:254), não pela qualificação efetiva: PASSOU -> INDETERMINADO por perda de prova retorna estado OK; remoção de caso e zero casos também OK. Provas:
- HonestVerdicts.test_fixture_comparison_never_passes
- test_duplicate_id_not_silent_overwrite
- test_lost_runtime_proof_is_regression
- test_removing_criterion_not_ok
- test_empty_cases_not_ok
Todos FAIL individual exato, ERROR0/skip0. observed-effects.json conserva o resultado real, inclusive regressoes=[].

F7: CLI ignora resultado da comparação no exit (visualizador.py:550–561). Integration.test_cli_incompatible_baseline_not_exit0 e test_cli_missing_criterion_not_exit0 reprovam. Saída literal resumida: candidata contagem={"PASSOU":1}, stale=False, EXIT0 apesar de comparação recusada/ausência. HTML cli/incompatible/out.html SHA256 62be783e8ee64a88838f551f94d2c1d1fe9a373dc6da67fc1bb708067b49a3b2; cli/removed/out.html SHA256 17dc921faa62f9434083e02c25d2227575426db52547cdb76b3210b0e524423b. Correção: agregado/exit acompanha TODAS as etapas pedidas, sem tratar ausência/INDETERMINADO como verde.

## 5. Fonte alterada invalida aprovação stale — ACHADO / FALHOU F2

PASSOU o caminho nominal de hash de fonte divergente -> STALE; teste Positive.test_stale_changed_source mostrado FAIL sob mutação que ignora stale.

F2 crítico de apresentação: SEM aprovação ou aprovacao={} aparece **VIGENTE**. Em visualizador.py:448–453, mesmo dict vazio recebe stale=False/motivos=[], ficando truthy; _secao_aprovacao (:350) não reconhece ausência. Registro sem hashes, de outro mod, ou rotulado fixture com hashes iguais também VIGENTE (:145 valida somente hashes presentes, :355 presume vigente quando não stale).

Provas próprias: Identity.test_approval_without_hash_not_vigente e test_approval_different_mod_not_vigente; adicionais Extra.test_no_approval_is_not_vigente, test_empty_approval_is_not_vigente, test_synthetic_approval_not_vigente. Todos FAIL com texto `<b class="">VIGENTE</b>` real, não hipótese. Correção: ausência não é aprovação; registro suficiente, identidade/mod/origem coerentes; incompleto/sintético inválido ou INDETERMINADO. Não fabricar aprovação nem misturar com aceite humano.

## 6. Texto escapado e JS dos logs — OK / PASSOU no escopo estrutural

visualizador.py:69 usa html.escape quote=True. Testei payloads script/img/onerror em id/mod/esperado/observado/motivo/sessão/lacuna. HTMLParser não encontrou tag script nem atributo on* proveniente do dado. CSP contém `script-src 'none'` e `base-uri 'none'`. Testes Positive.test_escape_adversarial_fields e test_csp_effective_and_no_external_resources PASSOU; cada um FAIL exato sob escape desligado/CSP alterada.

Esse PASSOU é geração/estrutura/escape. Browser real/CSP aplicada em file://, pixels, SVG e execução engine NÃO exercitados; não é afirmação de invulnerabilidade universal. Aceitação insegura de URI local é F1, não XSS comprovado.

## 7. Referências locais seguras — ACHADO / FALHOU F1

Literal `../private.png`, remotas/esquemas/UNC recusados nos positivos/suíte autor; controle literal mostrou FAIL com mutação que aceita tudo.

F1: visualizador.py:84–101 verifica string crua, sem confrontar URL/path decodificado ou raiz real. `%2e%2e/private.png` e `img/%2e%2e%2f%2e%2e%2fprivate.png` aceitos. observed-effects.json: accepted=true, URL `file:///sandbox/package/%2e%2e/private.png`, unquote -> `/sandbox/package/../private.png`. A referência sai do confinamento lexical quando decodificada. Security.test_percent_encoded_traversal e test_percent_encoded_separator_traversal FAIL. Correção: tratamento URL/caminho consistente e confinement/existência reais; rejeitar ambiguidades, não apenas HTML escape.

Security.test_percent_encoded_absolute_drive e test_query_fragment_not_filepath também FAIL (aceitação demonstrada); efeito/exploração no browser é **INDETERMINADO** e estes dois são hardening, não exfiltração comprovada. Não houve navegação nem acesso a arquivo privado.

## 8. Vereditos honestos e separação humana — ACHADO / FALHOU F3/F5/F7; humano OK

PASSOU seção Aceite HUMANO/PUBLICACAO permanece PENDENTE mesmo com input aceite_humano/publicado=True; Positive.test_technical_human_separate mostrado FAIL sob mutação. Nenhum ato humano/publicação feito.

F5: visualizador.py:197 usa bool(prova_runtime), portanto string "false" vira True; evidencia=[] não impede PASSOU; critério com fonte_sha diferente ou sessão OLD contradiz contexto atual mas ainda PASSOU; rotulo_fixture em identidade é ignorado pela origem_sintetica (:169). Provas HonestVerdicts.test_nonboolean_false_cannot_pass, test_missing_evidence_cannot_pass, test_stale_criterion_vs_current_identity, test_fixture_nested_identity_cannot_pass e Extra.test_criterion_session_disagrees_with_document. Falhas reais de consistência/tipo/ausência, sem pedir novo autenticador criptográfico. Não é apenas artefato inteiramente forjado, limitação já declarada pelo autor; há contradições explícitas dentro do input apresentado como prova atual.

Correção: validação de tipo/schema/identidade/origem e qualificação fail-closed reutilizando cadeia existente. F3/F7 também contaminam apresentação/exit (ver seção4). Fixture da própria entrega nunca é validação runtime desta revisão.

## 9. Reuso e integração do coletor/avaliador — ACHADO / FALHOU F6/F9; runtime NAO_EXERCITADO

PASSOU reuso efetivo de tools/automacao/cenarios/kit09.py + rstv.py; fixture rotulada gera21 critérios sem PASSOU. Positive.test_kit09_reuse_labelled_fixture mostrado FAIL sob mutação que apaga resumo. Não criei outro avaliador de regras de jogo.

F6: CLI monta/avalia documento em visualizador.py:522 ANTES de mesclar --identidade (:526–532). Harness remove identidade do envelope sintético, fornece mesma identidade por CLI; API com identidade já mesclada contém PASSOU, CLI devolve21 NAO_EXERCITADO/exit2. Integration.test_cli_supplied_identity_used_before_evaluation FAIL. Output real cli/identity-order/out.html SHA256 5bc5ba13b74f7911026aa2dbf7a6e72f2b597dfcd0c29a97922d9e98aa367292. Dados são construção offline para discriminar ordem, NÃO prova de jogo. Correção: validar/mesclar inputs antes de avaliar; equivalência CLI/API.

F9: _ler opcionais fora do try (:526–536). --identidade inexistente gera traceback/exit1, não diagnóstico controlado/infra exit2. Integration.test_missing_optional_file_infra_exit2 FAIL; cli/missing-extra/{stderr.txt,exit.txt}. Correção: entradas opcionais e malformadas tratadas fail-safe, sem confundir infra e defeito.

Formato do coletor AUT4 lido dirigidamente (tools/automacao/runtime/coletor.py:305–394) e fixture existente identificada. Não havia exemplo medido do jogo no escopo entregue; não usei dados do dono nem autorizei nova coleta. Coletor real/round-trip em runtime **NAO_EXERCITADO**, não PASSOU parcial. Imagens/evento/quadro/personagem reais/desempenho/interferência idem.

## 10. Execuções e contra-provas — OK / PASSOU como auditoria, produto REPROVADO

Comandos realizados via terminal em sandbox, subprocess com timeout120 e stdout/stderr/returncode conservados (wrapper python-c exit0 não substitui exit do filho):
- `python tools/automacao/kit08/teste_visualizador_kit08.py`: Ran21 tests, OK, exit0 -> author-suite.log.
- `python tools/automacao/kit08/contra_prova_kit08.py`: controle base OK,7 mutações +1 falso-verde recusados,8/8 exato, exit0 -> author-contra.log.
- `python test_review_kit08.py`: Ran34 tests, FAILED(failures=24),10OK, ERROR0/skip0, exit1 -> review.log.
- `python review_controls.py`: 10 mutações seletivas/10 alvos positivos;24 negativos próprios individualmente, cada subprocess Ran1/FAIL1 exato/exit1/ERROR0/skip0; adicional Extra Ran4/FAIL4/ERROR0/skip0. Harness discriminador exit0 -> controls-run.log, controls-summary.json, extra.log, controls/*.log.
- `python verify_review.py`: comparação hashes27+mismatch=[] e contagem exata, exit0 -> verify-final.log/final-verification.json. Primeira execução falhou na exigência incorreta de zero hits heurísticos; prova preservada verify.log. Corrigi só harness para manter ACHADO do scanner, não enfraqueci trava.

Todos os dez testes positivos próprios foram mostrados reprovando sob defeito plantado; as24 falhas negativas originais também têm processo individual com conjunto exato. Os quatro adicionais falham em lote sem ERROR/skip. Nada foi corrigido no produto pelo reviewer.

Runner shell entregue permaneceu **INDETERMINADO (infra exit2)**: subshell Bash não encontra python, nem com argumento explícito contendo path real. Duas tentativas iniciais preservadas, mudança de abordagem para etapas diretas efetivamente executadas; tentativa diferente explícita também exit2 e encerrada sem repetir. Logs author-runner.log, author-runner-absolute-python.log, author-runner-explicit-command.log. Não marcar runner verde por inferência das etapas.

## 11. Travas e limites honestos

Motores reais check_segredos/PADROES e check_padroes_segredo/FORMATOS+entropia sobre lista explícita129 arquivos (não CLI git de índice inexistente). Padrões:0 hits; genérico:9 hits de entropia mantidos, associados ao id público KIT09-RSTV25b-sem-aresta-inventada em fonte/testes/HTML, não valores de credenciais. Estado bruto genérico ACHADO preservado. Ambos detectam controle sintético em memória; não se grava/exibe segredo/token. Scanners não editados, sem nova exceção. Prova final-verification.json e verify-final.log. Não equivale a anonimato universal.

Não executei audita_docs global: mistura outros mods/índice e não cobre untracked novos; referências do parecer verificadas explicitamente no fechamento. Travas DLL/versões/pacote/tradução não aplicáveis a este escopo Python/HTML. Build/preflight deploy NÃO exercitados e desnecessários (nenhum build). UI/UX visual em browser/jogo, gate humano, performance, concorrência de filesystem e cadeia coletor medida NÃO exercitados.

Histórico incremental preservado docs/automacao/KIT-08R-parte01.md … parte05.md; primeira parte escrita antes de exploração profunda. Nenhum relatório do implementador usado como única prova.

## 12. Próximo passo / handoff

KIT-08F t_ac0f78f7 contém F1–F9, baseline/hash, suíte imutável, limites e exigência RED/corrigido/reconferência em nova instância. Somente default existe no inventário de perfis; atribuição usa perfil real sem inventar especialista ou mudar política. Reviewer648 não fará conserto.

Implementador do conserto deve chamar kanban_request_review com identidade implementer/run/sessão, outputs/paths/hashes; outra instância revisa no mesmo cartão e tenta refutar F1–F9. Não abrir R duplicado, não apagar histórico. KIT-12 e KIT-15 permanecem gated por KIT-08F até aprovação técnica. Aprovação técnica NÃO autoriza instalação/publicação/gates humanos nem fecha DoD de mod.

Artefatos finais: este parecer, diretório de provas e ZIP `scratch/kit/KIT-08R-run648-evidencias.zip`; integridade/manifest de entrega em delivery-verification.json gerado no fechamento. ZIP apenas provas/fonte Python público/fixtures sintéticas, sem .git, pycache, assemblies proprietários ou perfil.
