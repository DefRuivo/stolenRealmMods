# KIT-09R — parte 01: orientação e critérios

Revisor: t_0564b789, run 637, sessão 20261009_213534_0e7231, perfil default. Implementador: t_a4ca00f9, run 635, sessão 20261009_212534_16b45a. Instâncias distintas; não participei da implementação.
Data local medida: 2026-10-09T21:35:49.958361-03:00.

## Escopo e limites
Revisão independente offline do pacote Python de cenários RSTV KIT-09. Sem alterar produto, instalar, publicar, executar jogo, salvar ou deploy. Builds não aplicáveis até descobrir necessidade concreta; pre-flight obrigatório se houver build. Fixtures nunca comprovam jogo/pixels/desempenho. Parecer final será docs/automacao/KIT-09R-revisao.md; partes incrementais preservam histórico.

## Inventário inicial
Comando: cd "$HERMES_KANBAN_WORKSPACE" && pwd && git status --short && git branch --show-current && python -c (data/sessão e existência de artefatos KIT-09R).
Exit 0; workspace /c/dev/stolen-realm; branch ci-validate-test. Múltiplas alterações/untracked pré-existentes, inclusive kit09.py/test_kit09.py/fixtures e rstv.py/coletor.py modificados. Nenhum artefato KIT-09R existia. Alterações manuais são excluídas de autoria desta revisão e serão preservadas.
Lidos docs/SUPERVISAO.md (1–220) e docs/PROCESSO-REVISAO.md (completo); regras seriais/econômicas do cartão prevalecem sobre paralelismo/janelas legados.
Pai KIT-09 confirmado done, run635; handoff é alegação a reconferir, não prova desta revisão.

## Critérios a conferir
1. Reuso AUT-5/CIC-3 e rastreabilidade de esperado independente — INDETERMINADO.
2. Abrir/fechar, anti-duplicação — INDETERMINADO.
3. Personagem correto e skills/pontos antes/depois sem mutação — INDETERMINADO.
4. Tooltip sem placeholders, pai/índice restaurados — INDETERMINADO.
5. Dependency real governa arestas; ausência legítima sem conector — INDETERMINADO.
6. Geometria/clipping sem falsa qualificação — INDETERMINADO.
7. Handler versus clique físico; ativo não prova desobstrução — INDETERMINADO.
8. Adaptadores sobre saída real do coletor e rejeição de malformado/ausente/fixture/dado velho — INDETERMINADO.
9. Caminho positivo, defeito plantado e restauração em sandbox — NÃO_EXERCITADO.
10. Identidade viva/hashes, travas pertinentes, preservação e handoff — INDETERMINADO.
11. Runtime/UI/UX humano/publicação — NÃO_EXERCITADO (não autorizados; não são aprovados pelo parecer offline).

Próximo bloco: ler entrega e fontes dirigidos, inventariar hashes e criar sandbox sem .git/credenciais/perfil.
