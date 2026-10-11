# KIT-05R — parte 01: abertura da revisão independente

Cartão t_43675d2e; reviewer run 630, perfil default, instância independente do implementer run 629 (KIT-05 t_e9e569f8). Data de referência: 2026-10-09. Revisão exclusivamente OFFLINE. Este checkpoint não aprova a entrega.

## Contexto conferido

Lidos com as ferramentas: cartão KIT-05R, cartão KIT-05, docs/SUPERVISAO.md (linhas 1–240), docs/PROCESSO-REVISAO.md integral e docs/automacao/KIT-05-entrega.md integral. O cartão permite testes em sandbox, não jogo/deploy/save/publicação.

Comando inicial real: `cd "$HERMES_KANBAN_WORKSPACE" && pwd && git status --short && git branch --show-current && python -c ...`. Exit 0. Workspace C:/dev/stolen-realm; branch ci-validate-test; há alterações tracked/untracked preexistentes. Nenhum KIT-05R* existia no inventário inicial. HERMES_KANBAN_TASK não está definido no terminal; por isso as transições serão dirigidas explicitamente a t_43675d2e. Não se declarou repositório limpo.

## Critérios a conferir (estado inicial: INDETERMINADO)

1. Identidade dos fontes vivos e independência de autoria.
2. Clique recebido; janela de fato aberta/fechada; tooltip.
3. Falha clique-sem-janela com motivo/timeout e correlação correta.
4. Evento/dados/quadro após atualização visual; refutar captura fora do evento e falso sucesso visual.
5. Não afirmar simultaneidade inexistente.
6. Passividade: sem cliques/saves/equipamentos/modificações.
7. Deduplicação por mudança, fila limitada e retenção.
8. Teto de capturas; pausa segura; degradação explícita.
9. Sem captura contínua indiscriminada; refutar spam e interferência.
10. Testes positivos, negativos e defeitos plantados independentes em sandbox.
11. Uso das infraestruturas existentes e escopo efetivamente entregue.
12. Desempenho/runtime: NAO_EXERCITADO nesta revisão; nenhuma fixture comprova jogo.
13. Parecer por item, correções roteadas ao implementador e handoff nativo.

## Primeira hipótese a refutar

O relatório do autor reconhece que o Core C# ainda usa lista sem teto e que o módulo Python é uma especificação executável (entrega linhas 94–99). A integração não implementada não pode ser tratada como mera falta de autorização runtime: conferir os call sites vivos e separar lógica offline de funcionalidade implementada. Os PASSOU do relatório não foram endossados nesta abertura.

## Próximo bloco

Inventário/hash; leitura dirigida do módulo, testes e runner; criar cópia sandbox sem .git/credenciais/perfil e executar controles próprios. Nenhum arquivo de implementação será editado pelo reviewer.
