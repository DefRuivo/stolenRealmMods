# KIT-09F — parte 01: orientação, inventário e plano de correção

Cartão `t_01f65801` (KIT-09F). Implementação corretiva OFFLINE. Instância nova, diferente do
reviewer `t_0564b789` run637 e do autor inicial `t_a4ca00f9` run635. Perfil `default` (único
disponível). Nada de jogo/perfil/save/probe/deploy/publicação neste cartão.

## Fonte do problema

Parecer independente: `docs/automacao/KIT-09R-revisao.md` (REPROVADO, F1–F7).
Suite independente imutável do reviewer (a ser reexecutada sobre o fonte corrigido):
`scratch/kit/KIT-09R-run637/test_review_kit09.py` — 30 testes, 19 FAIL / 11 OK, zero
ERROR/skip, exit1 (`suite-review.log`, `review-summary.json`, `measurements.json`).

## SHA256 vivos conferidos na abertura (leitura)

| Arquivo | SHA256 |
| --- | --- |
| tools/automacao/cenarios/kit09.py | a4f7587641174960affab6be73590071fe181c86de919dbb87cceb28025f6586 |
| tools/automacao/cenarios/test_kit09.py | e1b05706f164b4c6a94a87bb7265e7f49942693ea46fb3ffa19a02827d50fd28 |
| tools/automacao/runtime/coletor.py | 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d |
| tools/automacao/cenarios/rstv.py | f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7 |

Todos batem com os declarados no corpo do cartão. Dependências `rstv.py` (CIC-3) e
`coletor.py` (runtime) permanecem intocadas nesta frente.

## F1–F7 → onde o defeito vive

- F1 — procedência sintética/fixture/contraditória gera `OK` + `prova_runtime` + `runtime_exercitado`.
  Local: `kit09.py:761–805` (avaliar_cenarios), `kit09.py:819–842` (resumir), CLI 855–865;
  fechamento herdado `rstv.py:_fecha` / `_procedencia`.
- F2 — guardas pai/índice/duplicata leem o topo (`o.get`/presença) e ignoram o bloco `campos`
  NORMALIZADO do coletor real → NAO_EXERCITADO inclusive em defeito medido.
  Local: `kit09.py:319–338`, `kit09.py:341–367`; `coletor.py:normalizar_observacao`.
- F3 — ausência/linhas ausentes e mapas vazios viram zero; T5 sem Dependency vira ausência
  legítima; aresta T5 inventada pulada no critério específico.
  Local: `kit09.py:376–429`, `432–465`, `468–491`.
- F4 — iguais malformados (`[]`/`[]`, `bad`/`bad`, `-1`/`-1`) e `inf`/`inf` aprovam.
  Local: `kit09.py:327–332`, `249–256`; primitiva `RC._numerico` checa tipo, não finitude.
- F5 — `clique_fisico.alvo` não é confrontado com alvo independente declarado.
  Local: `kit09.py:570–589`.
- F6 — sessão velha reprova só o meta; demais critérios seguem OK/`prova_runtime`.
  Local: `kit09.py:624–643`, `773–805`, `839`.
- F7 — CONTROLES com 21 linhas/20 IDs (falta render-observado); guard de render ausente
  neutralizado mantém a suite do autor verde. Local: `test_kit09.py:249–294`, `307–317`,
  `508–531`; `kit09.py:279–295`.

## Plano de correção (ordem)

1. Leitor de contrato real (topo + bloco `campos` normalizado) — F2/F4.
2. Validação de tipo/domínio/finitude ANTES de igualdade — F4.
3. Ausência ≠ zero; T5 completo; aresta T5 no critério específico — F3.
4. Alvo esperado declarativo do clique físico — F5.
5. Sessão esperada em cada qualificação — F6.
6. Procedência sintética/contraditória falha fechado em API/envelope/lista/CLI — F1.
7. Cobertura exata de 21 IDs + RED seletivo — F7.

Cada correção entra com prova RED (teste que reprova antes) e restauração byte a byte nas
demonstrações de mutação.

## Limites declarados

Runtime/UIUX/desempenho NÃO_EXERCITADO. Fronteira `test_rstv.py` (filtro de alvo de outro
mod) permanece vermelha e NÃO será mascarada aqui — frente separada CIC-3F.
