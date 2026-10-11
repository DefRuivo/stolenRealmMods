# KIT-07R — parte 05: controles negativos e scanners reais

## Suite independente persistida — FALHOU produto / PASSOU coleta
Comando `python scratch/kit/KIT-07R-run636/run_review_checks.py`, execução final exit 0 do harness de evidência (NÃO aprovação do produto). review-suite.log e review-results.json: subprocess da suite exit 1, Ran 24 tests in 0.241s, FAILED (failures=15), 9 OK, zero ERROR/skip. As 15 falhas são o mesmo conjunto da primeira execução.

## Controles negativos dos positivos — PASSOU (discriminação real)
Nove mutações isoladas; cada positivo mostrou Ran 1 test / FAIL do alvo exato / AssertionError / exit 1 / zero ERROR/skip. Cobrem hash, save, PNG off, honestidade PNG opt-in, upload, limpeza nominal, limpeza alheia, teto por arquivo e passividade com audit hook. `OWN_NEGATIVES_EXACT 9 / 9`.
Histórico honesto: na primeira tentativa, negativo de limite por arquivo produziu IndexError e 8/9, harness exit 1. Foi corrigido só o TESTE DO REVISOR: assert direto em excluidos[0] virou assert explícito de qualquer exclusão por motivo. Segunda execução deu FAIL específico, não ERROR. Nada alterado no produto.

## Scanners reais — PASSOU no escopo copiado
Repo de scanner isolado scratch/kit/KIT-07R-run636/scanner-git, git init e git add APENAS caminhos explícitos, sem commit e sem remote (git remote -v vazio, exit 0). Fontes entregues e docs KIT-07/KIT-07R presentes até parte04 analisados com check_segredos.py e check_padroes_segredo.py: ambos exit 0. Credencial plantada em arquivo exclusivo do scanner: ambos exit 1 com planted.txt; mensagens usam REDACTED/FORMATO, não valor nem prefixo. Arquivo plantado removido e retirado do índice. Saídas nos logs scan-positive/negative-*.log; comandos/exit em review-results.json.

Os scanners cobrem padrões nos arquivos versionados da cópia de auditoria, não provam exportação arbitrária segura. Produto continua REPROVADO pelos vazamentos, mutação da origem, resíduos, hashes incorretos, exclusão inválida, tetos e perda de log selecionado.

Próximo bloco: métricas observadas sem valores sensíveis; contraprová final de identidade; inspecionar filhos do cartão e preparar correção/reconferência sem liberar dependentes em cima de entrega reprovada. Nenhum runtime/build/deploy/publicação.
