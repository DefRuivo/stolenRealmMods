# KIT-14 — checkpoint 02: requisito humano ainda não resolvido

Implementador default/run698; t_a1f38855. Nenhuma execução ativa iniciada.

## Reconferência atual, não só handoff
- kanban_show(t_f19310d3): gate done. Comentário registra autorização do dono em 09/10/2026, aplicada em 10/10/2026; escopo isolado e descartável, sem publicação. O corpo exige limites de performance antes da rodada.
- O cartão KIT-14 exige limites acordados, não números inventados. Seus comentários atuais não fornecem limiares nem dispensam esse requisito.
- KIT-G2-entrega.md, itens 6 e 10: limite de performance LACUNA; a fixar pelo dono antes da rodada.
- KIT-G2-parte03.md, item 1.1: comparação com/sem recorder, mesmo cenário/janela, FPS e tempo de quadro média/p95, memória residente e bytes escritos; fonte bruta Windows/probe. Não existe limiar acordado registrado no documento. O texto admite reportar a lacuna no KIT-14, mas não resolve o requisito explícito de limites antes da rodada nem declara dispensa do dono.
- Busca dirigida em docs/automacao/KIT-*.md por limite/limiar/teto e FPS/frame/quadro/memória/disco/performance: 58 linhas retornadas, incluindo contexto. Não apresentou acordo numérico de performance. Limites internos de filas/arquivos não equivalem a aceite de impacto em jogo. A busca é dirigida, não uma alegação de leitura de todos os arquivos do repo.
- kanban_show(t_9ce7d260): KIT-14R todo, depende deste cartão; não será liberado artificialmente enquanto a coleta real estiver incompleta. Não foi criada revisão duplicada.
- Skills in-game-verification e stolen-realm-modding carregadas. Confirmam separação de runtime/fixture, preflight obrigatório de deploy, identidade da DLL instalada e preservação do ambiente pessoal.
- SUPERVISAO.md lido até o fim; PROCESSO-REVISAO.md integralmente. Política serial atual do cartão prevalece sobre paralelismo/horário legados.

## Decisão necessária (sem inferir consentimento)
O dono deve definir os limites tolerados para queda de FPS/elevação de tempo de quadro (média/p95), memória adicional e escrita em disco, com unidade e base de comparação; alternativamente deve dispensar explicitamente os limiares prévios e autorizar rodada exploratória sem veredito de performance. A segunda opção altera apenas a exigência de pre-registro se aprovada pelo dono, não vira PASSOU.

## Estado honesto
Reconferência de requisitos executada. Runtime/instalação/build/PNG/relatório funcional/performance/rollback em jogo NAO_EXERCITADO. O consentimento B1–B6 existe; o bloqueio não pede autorização genérica novamente, pede resolver o critério específico que continua pendente.
