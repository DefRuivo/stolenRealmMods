# KIT-15F — correção da instalação/rollback/integridade/pacote (parte 01)

Cartão: t_d83f3ef6. Data: 10/10/2026. Instância: default/run686 (NOVA, nem reviewer678 nem 685).
Parecer de origem: docs/automacao/KIT-15R-revisao.md (REPROVADO), reviewer default/run685.

## Escopo desta correção

Corrigir os 12 grupos F1..F12 do parecer KIT-15R sobre o produto vivo
`tools/automacao/kit15/` (mais os componentes empacotados de `tools/automacao/runtime`,
`kit11`, `kit08`, `kit12`) e provar com os oráculos imutáveis do revisor, sem enfraquecê-los.

## Oráculos imutáveis (cópia byte a byte, hash preservado)

- scratch/kit/KIT-15R-run678/test_review_kit15.py
- scratch/kit/KIT-15R-run678/test_extra_kit15.py

O `KIT_REVIEW_MODULE` aponta para o módulo vivo corrigido; o `pacote-proprio/staging`
da minha rodada é regerado por `pacote.py` a partir das fontes congeladas (corrigidas).

## Restrição de identidade do pacote (importante)

O oráculo P1 exige recibo com **41 arquivos** (29 de componentes + 8 de ferramenta + 4 de docs).
Isso fixa a composição do pacote: a correção NÃO pode adicionar membros de payload.
Portanto o fechamento de dependências (F9) é feito tornando os componentes autossuficientes,
não empacotando novos módulos — decisão registrada para a revisão.

## Plano de correção por achado

- F1: regenerar o ZIP a partir das fontes congeladas e comparar TODOS os membros com a origem viva.
- F2: manifesto/recibo autoritativos (schema/tipos/obrigatórios/fechamento/hashes declarados).
- F3: transação registrada antes da cópia; falha IO reverte e não deixa payload sem journal.
- F4: ação reversa da remoção restaura de fato o estado anterior.
- F5: propriedade preservada (preexistente idêntico, atualização, seleção sem órfãos).
- F6: backup original corrompido/ausente faz remover falhar fechado e preserva o recibo.
- F7: `pacote.py verificar` sem `--json` conserta saída/exit.
- F8: suíte/contra/empacotamento executáveis no layout distribuído sem repo.
- F9: fechar closures reais (runner→recorder, viewer, integração, ProjectReference do adapter).
- F10: scanner cobre JSON entre aspas, diretório bin/ e erro de IO (não vira LIMPO).
- F11: contra-prova exige N>0, alvo falhando, 0 ERROR/skip, conjunto esperado.
- F12: confinamento de todos os caminhos (origem/destino/backup/recibo) antes de efeitos.

Checkpoints seguintes: KIT-15F-parteNN.md; entrega em KIT-15F-entrega.md.
