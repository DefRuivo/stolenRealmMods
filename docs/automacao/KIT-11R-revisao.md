# KIT-11R — parecer independente final

Cartão t_79c1525f. Parecer: **REPROVADO** para aceitar o executor KIT-11; revisão offline concluída, não produto aprovado.
Reviewer: run653, perfil default, sessão 20261009_224034_f92728.
Implementer original: t_f2129aea, run649, sessão 20261009_222533_fe8c04. Instâncias distintas; reviewer não participou da implementação nem corrigiu produto.
Data local inicial medida: 09/10/2026 22:40:48 -03:00. Escopo autorizado: revisão OFFLINE; sem gates humanos/runtime.

## Identidade dos arquivos vivos e isolamento

Root C:/dev/stolen-realm; branch ci-validate-test, inventariada via git. Alterações manuais tracked/untracked preexistentes preservadas; repo não declarado limpo.
Sandbox: C:/dev/stolen-realm/scratch/kit/KIT-11R-run653. Cópia dirigida de arquivos do escopo, incluindo untracked, byte a byte; sem .git/remotos/credenciais/perfil do dono. Não copiado jogo, DLL proprietária, save ou segredo.

| Arquivo | SHA-256 | Bytes |
|---|---|---:|
| tools/automacao/kit11/executor.py | 65284edd248d3bf1117529b366d150b7cb8578c0ae03c64fcd7358cdbb75b6e2 | 24137 |
| tools/automacao/kit11/test_kit11_executor.py | 1d72ae071ceea8086c49b7d11523fbda1c908eee7f772e44290d38adbf071a02 | 14998 |
| tools/automacao/runtime/coletor.py | 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d | 104102 |
| tools/automacao/runtime/controle_acesso.py | 379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457 | 34265 |
| tools/testes/arcabouco.py | 08b4dd51c1d2bd851cf0d5d2b2f038dbe3f1094ab4c625ed63a7a4dc97c20afb | 12519 |

Hashes executados via hashlib e reconferidos antes de fechar: PRESERVED 5 live/source copies; no_git True. Mutações do reviewer aconteceram somente em memória do módulo sandbox; nunca alteraram esses bytes.

## Execuções reais e resultados

Comandos abaixo relativos ao root; logs na sandbox. Exits dos filhos capturados explicitamente; exit0 do wrapper apenas salva evidência, nunca muda FAIL para PASS.

1. `python scratch/kit/KIT-11R-run653/tools/automacao/kit11/test_kit11_executor.py`: 12 teste(s), 0 falha(s), exit0; author-baseline.log.
2. `python scratch/kit/KIT-11R-run653/test_kit11_review.py`: Ran 36 tests in 0.164s; FAILED (failures=24), exit1; review-final.log. Contagem programática: 12 OK,24 FAIL,0 ERROR,0 skip.
3. `python scratch/kit/KIT-11R-run653/test_mutations.py`: 12 mutações seletivas do fonte capturadas pelos testes correspondentes sem ERROR/skip; depois Ran 12 tests in 0.078s / OK no fonte restaurado, driver exit0. Um teste possui 6 subtestes de campos executáveis, todos vermelhos no guard neutralizado. red-test_*.log, restored-controls.log, mutation-results.json.
4. Suite autor com `--isca`: 13 teste(s),1 falha(s),exit1; author-isca.log. A isca lança AssertionError incondicional, não modifica nem testa comportamento do executor (ACHADO F9).
5. CLI efetiva: `python scratch/kit/KIT-11R-run653/tools/automacao/kit11/executor.py --plano scratch/kit/KIT-11R-run653/cli-plan-denied.json --estado scratch/kit/KIT-11R-run653/cli-state.json --saida scratch/kit/KIT-11R-run653/cli-denied-result.json`: saída lida de volta em disco retorna OBSERVADO/exit0 embora permite_observar=False/status=NAO_EXERCITADO; frente=None.
6. CLI com timeout omitido e fonte falsa: harness subprocess.run timeout=.5 gera TimeoutExpired. Apenas o filho Python isolado do reviewer foi encerrado pelo harness. Ausência de conclusão é prova da lacuna, não verde. cli-proofs.json guarda os resultados.
7. `python tools/check_segredos.py`, `python tools/check_padroes_segredo.py`, `python tools/check_dupes.py`, `python tools/audita_docs.py`: cada exit0; quatro logs e guards.json. Cobrem versionados, não aprovam os novos untracked.
8. `python scratch/kit/KIT-11R-run653/finalize_evidence.py`: preservação, contagem e scanners dirigidos exercitados. Primeiro scan:46 arquivos,0 hits; dois motores detectam credencial sintética gerada só em memória (sem gravar/imprimir valor). Reexecução final/pacote registrada no manifest final. Não enfraquecidas travas.

## Parecer por critério

| Critério | Veredito | Prova e limite |
|---|---|---|
| C1 espera menu/tela/condição | ACHADO / FALHOU | Arquivos reais e polling com mudança de estado passam; ausência de prazo permite espera indefinida, F3. Navegação no jogo NAO_EXERCITADO. |
| C2 handlers/diagnóstico/timeout | ACHADO / FALHOU | Fonte arquivo atende menu/tela/condição; timeout real/arquivo ausente nunca verde. Resposta inválida promove satisfação, JSON quebrado não dá diagnóstico estruturado, prazo sem teto, F2/F3. |
| C3 frente única | ACHADO / FALHOU | RACE 2 acquisitions []; frente opcional e CLI sem lock, F4. Lock ocupado sequencial/token de outro são recusados e controles ficam vermelhos com mutação. |
| C4 cancelamento/rollback/encerramento | ACHADO / FALHOU | F5–F8: PID externo recebe fechamento no driver falso; rollback destrutivo; perdas de veredito; exceções vazam lock; cancelamento tardio ignorado. |
| C5 autorização ativa separada | ACHADO / FALHOU | Caso booleano negado recusa sem leitura; override string 'false' concede permite_agir=True/PASSOU, F1. Nenhuma ação real executada. |
| C6 perfil/save de teste | OK / PASSOU restrito à comparação declarada offline; identidade real INDETERMINADA | Igualdade válida e divergência testadas; mutação da comparação reprova. Fonte não comprova perfil/save do jogo nem atualidade; F2 fragiliza formato de leitura. |
| C7 observação não concede ação | ACHADO / FALHOU | Mesmo obs=False lê e vira OBSERVADO/CLI exit0; observação gera shutdown sem autorização ativa, F1/F5. |
| C8 config/desconhecido/versão falham fechado | ACHADO / FALHOU | Versão/tipo/condição/campo executável conhecidos recusados; coercões/string/NaN/inf/timeout omitido aceitos, F1–F3. |
| C9 não executar comandos arbitrários de cenário | OK / PASSOU offline | Seis campos conhecidos recusados, fonte não lança comando do plano; 6 subtestes vermelhos quando guard neutralizado. Driver fixo de encerramento tem F5, não é comando arbitrário do cenário. |
| C10 positivo/falha/cancelamento/controles | ACHADO na suficiência da entrega; execução independente PASSOU como auditoria | Autor12/12 verde enquanto reviewer24 FAIL. Doze controles seletivos mostrados vermelhos e restaurados. Stub não comprova runtime; F9. |
| C11 reuso da infraestrutura | OK parcial / ACHADO F9 | Coletor e arcabouco realmente usados; controle_acesso.py citado mas não importado/usado. Reuso do rollback omite mecanismos já existentes de diretórios/estado final. |
| C12 handoff/identidade/preservação | OK nativo / ACHADO documental F9 | Upstream complete libera R precriado corretamente; relatório diz request_review inexistente. Este parecer usa native complete com implementer/reviewer explícitos e outcome rejected. |

## Achados acionáveis (F1–F9)

### F1 — permissões ignoradas e coerções não seguras
Local: tools/automacao/kit11/executor.py:159-168 e tools/automacao/kit11/executor.py:173-195, tools/automacao/kit11/executor.py:391-400.
Esperado: autorização negada impede leitura/efeitos; todas as entradas e overrides tipados; observação não concede ação/encerramento.
Observado: src.calls=[('menu','MainMenu')] mesmo obs=False, resultado OBSERVADO; override ativa_autorizada='false' -> permite_agir=True/PASSOU; requer_acao='false' convertido para True.
Testes: test_neg_observation_permission_denied, test_neg_override_false_string, test_neg_requer_acao_non_boolean; três FAIL. CLI real reproduz leitura autorizacionalmente negada com exit0.
Correção: validar tipos sem bool coercivo; interromper antes de efeitos/leitura; separar escopos e exits NAO_EXERCITADO/recusa.

### F2 — fonte inválida promove verde ou perde diagnóstico
Local: tools/automacao/kit11/executor.py:199-208 e tools/automacao/kit11/executor.py:221-237.
Esperado: satisfeito estritamente booleano; fonte ausente/inválida nunca satisfeita; erros estruturados.
Observado: satisfeito='false' gera OBSERVADO tanto no método injetado quanto no JSON real; JSON malformado lança JSONDecodeError em vez de resultado fechado com diagnóstico.
Testes: test_neg_invalid_satisfeito_string, test_neg_file_satisfeito_string, test_neg_file_invalid_json; três FAIL. Arquivo ausente com prazo é FALHOU como esperado (controle OK + mutação detectada).
Correção: validar contrato de resposta/JSON e converter falhas em estado explícito, sem inventar satisfação.

### F3 — timeout facultativo/não finito e sleep não limitado
Local: tools/automacao/kit11/executor.py:158-163 e tools/automacao/kit11/executor.py:328-360.
Esperado: cada passo tem limite finito positivo (ou default finito seguro explícito); polling respeita orçamento restante e cancelamento.
Observado: ausente/None/NaN/inf aceitos; CLI sem limite permanece rodando até timeout do harness; dormir(5) recebido sob limite.02.
Testes: test_neg_timeout_missing, test_neg_timeout_none, test_neg_timeout_nan, test_neg_timeout_infinity, test_neg_poll_clamped_to_deadline; cinco FAIL.
Correção: limite obrigatório ou default finito, rejeitar não finitos e limitar espera ao restante. Timeout de leitura bloqueante/desempenho runtime não foi medido.

### F4 — frente única não atômica e bypassável
Local: tools/automacao/kit11/executor.py:286-310, tools/automacao/kit11/executor.py:411-419, tools/automacao/kit11/executor.py:519.
Esperado: aquisição exclusiva atômica em todas as entradas; sem lock válido não executar.
Observado: dois threads sincronizados após exists original obtêm o mesmo lock (2 successes,0 errors); API/CLI aceitam frente=None.
Testes: test_neg_lock_atomic e test_neg_lock_required; dois FAIL. Concorrência exercitada com arquivo lock real na sandbox, sem processo do dono.
Correção: ownership/exclusão atômicos e não opcionais; retomada stale não pode apagar lock novo de terceiro.

### F5 — encerramento não comprova criação e força na dúvida
Local: tools/automacao/kit11/executor.py:434-435 e tools/automacao/kit11/executor.py:479-486; dependência tools/automacao/runtime/coletor.py:1488-1508 e tools/automacao/runtime/coletor.py:1573-1588.
Esperado: encerrar apenas processo criado por esta execução sob autorização específica; dúvida não autoriza força.
Observado: executor só observa, não lança processo, mas delta {100}->{100,200} dispara CloseMainWindow(PID200); obs=False também dispara. pid_vivo=None escala para taskkill /F /PID 200.
Output: EXTERNAL_PID_TARGETS [200] commands 1; comandos capturados exclusivamente por driver falso, nada encerrado no jogo.
Testes: test_neg_external_pid_never_owned, test_neg_shutdown_requires_permission, test_neg_unknown_liveness_never_forces; três FAIL.
Correção: registro de criação/ownership/instância, gates por efeito, sem fallback coercivo na ausência de medição. Preferir guard/adaptação restrita no executor; coletor é arquivo compartilhado, sinalizar hotspot se modificá-lo.

### F6 — cleanup destrói o veredito terminal
Local: tools/automacao/kit11/executor.py:471-502.
Esperado: fase cleanup não substitui sucesso/falha/cancelamento; restauração/encerramento falhos agregam erro sem mascarar causa.
Observado: OBSERVADO, FALHOU e CANCELADO todos viram ROLLBACK ao usar area_trabalho/relativos; com imagem vira ENCERRAMENTO. _fecha não mapeia fases para resultado original.
Testes: test_neg_cleanup_preserves_success, test_neg_cleanup_preserves_timeout, test_neg_cleanup_preserves_cancel; três FAIL.
Correção: separar estado/fase/resultado terminal; conferir estado pós-cleanup/exits.

### F7 — rollback remove coisas preexistentes
Local: tools/automacao/kit11/executor.py:424-433 e tools/automacao/kit11/executor.py:473-491; mecanismos disponíveis tools/automacao/runtime/coletor.py:1194-1206 e tools/automacao/runtime/coletor.py:1259-1279.
Esperado: remover somente objetos próprios, preservar árvores e dados preexistentes; provar efeito final.
Observado: diretório vazio existente desaparece após remover arquivo criado dentro dele; dir_backup informado com owner.txt preexistente é apagado inteiro pelo rmtree. Restauração byte a byte de arquivo selecionado simples passa, mas não prova árvore exata.
Testes: test_neg_preexisting_empty_dir_preserved, test_neg_preexisting_backup_preserved; dois FAIL.
Correção: reusar snapshot_dirs/preservar/verificar_sem_residuo, backup dedicado possuído pela rodada, validação de fronteiras; não inferir sucesso pelas ações retornadas.

### F8 — exceções vazam lock e cancelamento tardio ignorado
Local: tools/automacao/kit11/executor.py:425-437 e tools/automacao/kit11/executor.py:471-491, tools/automacao/kit11/executor.py:335-351.
Esperado: cleanup/liberação independentes inclusive em erro; cancelamento lido antes de retorno/efeitos.
Observado: OSError plantado no snapshot anterior ao try deixa lock; OSError plantado no rollback pula liberar; fonte seta cancelado durante última leitura satisfeita e resultado OBSERVADO.
Testes: test_neg_setup_exception_releases_lock, test_neg_cleanup_exception_releases_lock, test_neg_cancel_during_last_read; três FAIL.
Correção: guards/finally desde aquisição, etapas cleanup isoladas e falhas estruturadas; rechecagem de cancelamento com regressões por cenário.

### F9 — cobertura insuficiente e documentação inexata
Local: tools/automacao/kit11/test_kit11_executor.py:318-319; docs/automacao/KIT-11-entrega-final.md:7-8, docs/automacao/KIT-11-entrega-final.md:25-27, docs/automacao/KIT-11-entrega-final.md:55.
Observado: isca incondicional não injeta defeito; suite autor12/12 aprova apesar de24 violações independentes. AST do executor: imports argparse,importlib.util,json,os,shutil,sys,tempfile,time,uuid; nenhuma importação/uso do controle_acesso. Evento native upstream é complete->R precriado (correto pelo grafo), relatório declara request_review que não aconteceu.
Correção: regressões seletivas com prova RED/GREEN no fonte antigo/corrigido; complementar documentação/reuso factual sem apagar histórico. As mutações de versão/lock do autor foram corroboradas com provas próprias seletivas; a isca incondicional não substitui isso.

## Limites honestos

- Navegação real/clique físico, janela/tooltip/pixels/UIUX, probe/jogo, perfil/save real e desempenho: NAO_EXERCITADO. Nenhum fixture promovido a runtime.
- Positivos de modo ativo demonstram política/comparação/espera offline, não ação de navegação executada; runtime_exercitado=False permanece verdadeiro na evidência.
- Build/preflight/deploy/plugin/pacote/versões de mod: NAO_EXERCITADO; não necessário à revisão de Python. Nenhum build sem preflight realizado.
- A suite runtime global não foi rodada nesta revisão: inclui leitura do perfil do dono; cobertura relevante exercitada em cópias/drivers falsos. Não repetir resultado upstream como prova própria.
- Nenhum arquivo do produto, Assembly-CSharp, mod, Bard/gameplay, save, perfil, política, modelo, cron ou prioridade editado. Sem instalação/publicação/git add/commit/push.
- Falhas F1–F8 provam lógica e efeitos de arquivos sandbox/dispatch capturado, não dano ocorrido no jogo.

## Entrega e próximo passo nativo

Criado t_2a38d1d3 (KIT-11F), nova instância implementadora, com F1–F9 e obrigação de kanban_request_review independente no próprio cartão; não executado conserto pelo reviewer.
Leitura de volta kanban_show(t_2a38d1d3) confirmou parent t_79c1525f e children t_0a434c97 KIT-12, t_adc1fbfa KIT-13, t_a1f38855 KIT-14. Os consumidores não são liberados antes do conserto/reconferência; conclusão desta R só encerra parecer.
Aceite do conserto: suite reviewer preservada (hash abaixo) contra original e novo fonte, controles seletivos e casos derivados; qualquer ajuste de contrato mapeado explicitamente sem enfraquecer proteção. Histórico parte01..06 e upstream preservados.

Arquivos de prova:
- docs/automacao/KIT-11R-parte01.md até KIT-11R-parte06.md;
- scratch/kit/KIT-11R-run653/inventory.json, runs.json, guards.json, cli-proofs.json, final-verification.json;
- suite reviewer sha cdd8b12a4cbb641b206cbd87ca534695a292109c4962f46e0cf06ee6e4a22143;
- driver mutações sha 9ed78c5f144844e6cd775e8ea6e76dbb3798e804c138a563ce59e67116522dc2;
- review-final.log sha d3ded609f24aa724de88d14b25fed0e6cfd79791d307cae02e40b48619060df8;
- mutation-results.json sha fd5abae20a262c737edfd636cf2c93e533a81584178780c31799649e1a3c31db;
- pacote final C:/dev/stolen-realm/scratch/kit/KIT-11R-run653-evidencias.zip, a gerar/verificar após este parecer; hash/contagem lidos de volta registrados em zip-verification.json e handoff nativo.

**REPROVADO.** Parecer independente entregue; não aceite humano, publicação ou aprovação técnica do executor.
