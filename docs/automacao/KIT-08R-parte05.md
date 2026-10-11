# KIT-08R — parte 05: preservação e travas finais

`python verify_review.py` (subprocess, timeout120) -> exit0, saída em scratch/kit/KIT-08R-run648/verify-final.log; JSON em final-verification.json.

Preservação: 27 arquivos originais da cópia inicial comparados SHA256 tanto vivo quanto sandbox; mismatch=[] (inclui fontes/fixtures entregues e dependências). Contagem calculada, não estimada: suíte própria34=10OK/24FAIL, ERROR0/SKIP0; adicional4=4FAIL, ERROR0/SKIP0; 10 mutações seletivas;24 negativos individuais.

Runner shell: abordagem diferente por `bash -c 'PYTHON=<interpretador real> bash tools/automacao/kit08/roda_testes_kit08.sh'` também exit2 pois command -v não resolve o path de Python nessa subshell. Prova em author-runner-explicit-command.log. Não repetir. Estado final do invólucro INDETERMINADO/infra exit2; etapas suíte e contra-prova direta PASSOU conforme logs, não confundir.

Scanners REAIS reusados por motores com lista explícita129 arquivos, não CLI git (a sandbox não tem índice Git):
- check_segredos/PADROES: zero hits; controle negativo sintético em memória DETECTADO.
- check_padroes_segredo/FORMATOS+entropia: nove hits heurísticos mantidos, zero formato de segredo; controle negativo em memória DETECTADO. Estado bruto ACHADO, não maquiado como verde. Hits em fontes/testes KIT09 e saída HTML, associados ao id público do critério da linha953 `KIT09-RSTV25b-sem-aresta-inventada` (34 chars), não credencial. Motor não alterado nem exceções adicionadas. Diagnóstico imprimia apenas localização/tamanho, nunca valor suspeito.
A primeira execução de verificação terminou exit1 ao exigir zero hits; essa falha foi preservada em verify.log. Ajustei SOMENTE harness próprio para registrar honestamente achados heurísticos e seguir a auditoria, sem afrouxar scanner ou produto. Reexecução válida preserva status ACHADO no JSON.

audita_docs global não rodado: mistura outros mods/índice git e não cobre os novos untracked desta frente; links/linhas/hashes do parecer serão verificados explicitamente. Demais travas de DLL/pacote/tradução não se aplicam a esta revisão Python/HTML. Nenhum build/deploy/jogo/publicação/commit.

Próximo passo concreto: emitir parecer REPROVADO com grupos F1–F9, criar KIT-08F para nova instância no perfil default existente, exigir reconferência independente via handoff nativo e adicionar gate desse conserto aos dependentes KIT-12/KIT-15 ANTES de fechar a revisão.
