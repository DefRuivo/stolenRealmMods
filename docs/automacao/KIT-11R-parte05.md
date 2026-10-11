# KIT-11R — parte 05: CLI real e roteamento

## Refutação pela CLI (exit real e estado resultante em disco)
Comando: python scratch/kit/KIT-11R-run653/tools/automacao/kit11/executor.py --plano scratch/kit/KIT-11R-run653/cli-plan-denied.json --estado scratch/kit/KIT-11R-run653/cli-state.json --saida scratch/kit/KIT-11R-run653/cli-denied-result.json.
Resultado lido do JSON: exit 0; veredito OBSERVADO; permissões observacao_autorizada=False/permite_observar=False/status=NAO_EXERCITADO; frente=None. C7/C3 FALHOU pela CLI efetiva, não só teste unitário.
CLI com plano sem timeout e fonte falsa: subprocess.run timeout=.5 gera TimeoutExpired. Encerrado exclusivamente o filho Python isolado criado pelo reviewer, não processo do jogo. C1/C2 FALHOU para falta de limite; este timeout de harness é prova de lacuna, nunca teste verde nem runtime comprovado. cli-proofs.json registra comandos/resultados e cli-denied.log saída integral.

## Contagens/hashes conferidos em Python
PARSED_COUNTS 36 {'ok': 12, 'FAIL': 24, 'ERROR': 0, 'skipped': 0}.
LIVE_UNCHANGED True para os cinco fontes inventariados. Suite reviewer cdd8b12a4cbb641b206cbd87ca534695a292109c4962f46e0cf06ee6e4a22143; driver mutações 9ed78c5f144844e6cd775e8ea6e76dbb3798e804c138a563ce59e67116522dc2; review-final.log d3ded609f24aa724de88d14b25fed0e6cfd79791d307cae02e40b48619060df8; mutation-results.json fd5abae20a262c737edfd636cf2c93e533a81584178780c31799649e1a3c31db.

## Grafo lido antes do encerramento
Filhos KIT-12 t_0a434c97, KIT-13 t_adc1fbfa, KIT-14 t_a1f38855, todos todo. KIT-13 seria liberado ao concluir este R sem gate de conserto; será criada correção dependente deste parecer, vinculada como pai adicional dos três consumidores antes de complete.
hermes profile list (exit 0) confirma somente default. Assignee de correção usa o perfil existente default, mas instancia implementadora NOVA diferente do reviewer run653; não execução de conserto nesta revisão.

## C12 — handoff nativo
Kanban upstream t_f2129aea confirma complete run649 liberando R preexistente. Isto é o mecanismo correto do grafo (não duplicar review no mesmo cartão). Relatório KIT-11-entrega-final.md:7-8/55 afirma request_review, evento que não existe: ACHADO documental, corrigir por complemento sem apagar histórico. Identidade do autor válida no metadata nativo; parecer deste reviewer será entregue no complete com implementer/reviewer e review_outcome=rejected.

Próximo bloco: travas read-only aplicáveis, pacote com provas e lista de correções F1–F9; nada alterado no produto.
