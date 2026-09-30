# Changelog — BetterTooltips

## 0.1.0

Primeira versão publicada.

- **Reescreve tooltips de skills e status que mentiam por OMISSÃO**: quando o texto oficial esconde algo que muda a decisão do jogador (de que atributo depende o número, limite de stacks, duração, quem é afetado, gatilho, número de golpes), a explicação que falta é acrescentada ao fim do tooltip.
- **Corrige defeitos objetivos de texto** — grafia (`benefical`, `additonal`), pontuação e espaço duplo — por tabela de correção casada pelo texto exato.
- A nota de mecânica entra na **cor de texto especial do próprio jogo** e é posicionada **depois dos custos e do alcance**, no fim do corpo do tooltip.
- **Sem qualquer alteração de gameplay**: o mod só reescreve strings no funil de localização (`OptionsManager.Localize`).

### Não entra neste mod

- A árvore do **Bard** é intocável (regra do projeto).
- A árvore do **Chaos** é omitida de propósito: ela sorteia um resultado e o texto não revela quais são — é a graça da árvore, não um defeito.
