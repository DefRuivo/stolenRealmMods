# KIT-14F3R — parte 04: primeira execução própria (RED)

Detector novo: scratch/kit/KIT-14F3R-run1523/review.py. Execução real arquivada em test-execution.json e *-audit.json; o agregado saiu1. O mutante real reprovou, mas ON também reprovou e três OFF resultaram2. Portanto este primeiro lote NÃO é verde.

Inspeção independente mostrou dois erros do detector, não defeitos do candidato: comparação byte a byte de .cfg ignora reserialização de comentários/CRLF pelo BepInEx, enquanto as seções/chaves/valores declarados são idênticos; recorder desligado retorna apenas status, legitimamente sem sessao. Config ausente ganha somente as três chaves false esperadas. A correção do detector usará equivalência semântica das configs e preservará a exigência dos opt-ins reais; comparação de sessão completa continuará obrigatória ON. Resultados RED serão mantidos em diretório próprio antes do reteste.

Os snapshots brutos iniciais têm conjuntos/tamanhos/SHA por arquivo. Comparador histórico (run916/upstream911/roda911.py:35–77) recalcula árvore completa, recusa reparse points, compara listas de novos/removidos/alterados e só aceita igualdade. Recibos pós mantêm diff e contagens, não segunda lista bruta completa. Não confundir este nível de evidência histórica com uma segunda coleta independente em jogo.
