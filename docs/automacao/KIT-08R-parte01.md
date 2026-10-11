# KIT-08R — parte 01: abertura e critérios da revisão independente

Revisor: t_70608c71, run648, instância independente da implementação t_e2107a63/run643. Mesmo perfil default, autoria por instância diferente. Data local obtida no terminal: 2026-10-09T22:25:45-03:00.

Escopo: auditoria OFFLINE do visualizador KIT-08, sem modificar produto, instalar, publicar, acessar jogo/save/perfil ou navegar. Li docs/SUPERVISAO.md (1–220), docs/PROCESSO-REVISAO.md e entrega KIT-08. Política atual do cartão prevalece sobre janela/paralelismo legados.

Inventário real: terminal `cd "$HERMES_KANBAN_WORKSPACE" && pwd && git status --short && git branch --show-current && python -c ...`, exit 0. Workspace C:/dev/stolen-realm; branch ci-validate-test. Há alterações manuais e untracked anteriores; serão preservados. Nenhum KIT-08R existente no inventário. Código entregue: tools/automacao/kit08/{visualizador.py,teste_visualizador_kit08.py,contra_prova_kit08.py,roda_testes_kit08.sh} e três fixtures. Nenhum build é necessário para esta ferramenta Python; deploy preflight/build não exercitados e não serão considerados verdes.

## C1 — Identidade viva, independência e preservação
INDETERMINADO: inventário inicial obtido; hashes e sandbox ainda pendentes.

## C2 — HTML local utilizável sem servidor/conta/Hermes
NAO_EXERCITADO: gerar por CLI e examinar HTML resultante na sandbox.

## C3 — Campos por caso/mod (esperado, observado, prova, imagem, sessão/build/config, lacunas)
NAO_EXERCITADO: confrontar HTML e entradas; dados sintéticos não comprovam runtime.

## C4 — Comparação somente com contexto compatível
NAO_EXERCITADO: negativos com diferenças/ausências de identidade.

## C5 — Fonte alterada invalida aprovação stale
NAO_EXERCITADO: positivos e negativos por identidade.

## C6 — Escape/XSS e ausência de execução de JS
NAO_EXERCITADO: analisar HTML/CSP e entradas hostis sem browser/runtime autorizado.

## C7 — Referências locais seguras, imagens/provas exportadas
NAO_EXERCITADO: caminhos adversariais e identidade/ausência da prova.

## C8 — Separação de aceite humano/publicação e vereditos honestos
NAO_EXERCITADO: fixture, timeout, ausência e skip não podem ser PASSOU.

## C9 — Reuso de decisão/relatório e coletor real quando disponível
NAO_EXERCITADO: verificar API/schema real e origem das entradas. Coleta AUT-4 em jogo não autorizada.

## C10 — Execução positiva, defeito plantado e controles negativos
NAO_EXERCITADO: rodar suíte entregue e testes próprios em sandbox independente.

## Parecer provisório
INDETERMINADO. Relatório do implementador é contexto, não prova desta revisão. Fechamento será escrito uma vez em KIT-08R-revisao.md; checkpoints adicionais em partes novas, preservando histórico.
