# KIT-09F — entrega: correção dos falsos OK, adaptador normalizado e cobertura RSTV

Cartão `t_01f65801` (gate de KIT-10/11/13/14). Implementação OFFLINE por instância NOVA,
diferente do reviewer `t_0564b789` (run637) e do autor original `t_a4ca00f9` (run635).
Perfil `default`. Nenhum jogo/save/perfil/probe/deploy/publicação/commit exercitado.
Revisão independente deste conserto é OBRIGATÓRIA antes de `kanban_complete`
(esta entrega é o pedido de revisão; não há autoaprovação).

## Resultado executivo

Os 7 achados (F1–F7) do parecer `docs/automacao/KIT-09R-revisao.md` foram corrigidos no
fonte e comprovados pelo **script independente imutável do reviewer**, reexecutado sem
edição sobre sandbox nova com o fonte corrigido:

- `python scratch/kit/KIT-09F-run639/test_review_kit09.py` →
  `{"total": 30, "failed": [], "errors": [], "skipped": [], "passed": 30}`, **exit 0**
  (antes da correção: 19 FAIL / 11 OK, exit 1).
- Suite do autor: `RESULTADO|PASSOU|kit09-rstv`, **exit 0**.
- Prova RED por guarda (durável): `PROVA-RED|PASSOU|12 mutacoes|falhas=0`, **exit 0**.
- Contra-prova (isca "sempre OK"): **exit 0** com 24 controles deixando de reprovar.
- Fronteira `test_rstv.py`: **exit 1**, MESMA falha pré-existente (filtro de alvo de outro
  mod) — intocada, não mascarada.

## Veredito por achado

| Achado | Correção | Prova |
| --- | --- | --- |
| F1 — sintético/fixture virava prova runtime | `_guarda_origem`: marcas na observação E no envelope, mais contradição de procedência; CLI passa o envelope; `runtime_exercitado` exige ausência de marca; saída conserva origem/sessão/lacunas | `test_cli_synthetic_fixture_must_not_claim_runtime`, `test_fixture_label_on_observation_not_runtime` OK; CLI do artefato sintético **exit 2** com zero OK; `_sintetico_nao_qualifica`; RED `F1-rotulo-na-observacao`, `F1-envelope-sintetico` |
| F2 — guardas ignoravam o bloco `campos` normalizado | leitura por `RC._campo` nas guardas pai/índice/duplicata (e sessão/arestas) | 6 testes `normalized-*` OK (3 positivos OK, 3 defeitos REPROVADO); `_normalizado_defeito_reprova`; RED `F2-leitura-normalizada` |
| F3 — ausência virava zero / T5 pulado | `_reg_dep_arestas` exige os DOIS lados por tier e mapas não vazios; T5 pela regra geral; `_reg_sem_aresta_inventada` julga T5; `_reg_ausencia_legitima` não inventa zero | `absent-lines`/`malformed-lines` fora do OK; `empty-maps-edges` INDETERMINADO; `missing-t5-dependency` INDETERMINADO; `t5-invented-edge` REPROVADO; RED `F3-mapas-vazios`, `F3-t5-no-criterio-especifico`, `F3-ausencia-nao-e-zero` |
| F4 — malformado/igual e `inf` aprovavam | validadores de caminho/índice ANTES da igualdade; finitude antes de comparar pontos | `parent-malformed-equal`, `index-malformed-equal`, `index-negative-equal`, `points-infinite` fora do OK; RED `F4-validacao-de-caminho`, `F4-finitude-dos-pontos` |
| F5 — clique no botão errado aprovava | `ALVO_BOTAO_RUN` declarado e VALIDADO (path/id), sobrescrevível; observado != esperado REPROVA; esperado ausente/inválido não julga; handler/clique seguem distintos e "ativo" não prova desobstrução | `wrong-click-target` REPROVADO; `test_handler_no_physical_inference` e `test_active_not_unobstructed` OK; controle `clique-alvo-errado`; RED `F5-alvo-do-clique` |
| F6 — sessão velha ainda qualificava capacidades | `_guarda_sessao` por critério (nenhum OK/`prova_runtime` de outra rodada) sem suprimir defeito | `old-session-capability` NAO_EXERCITADO com `prova_runtime=false`; `_dado_velho` estendido; RED `F6-sessao-esperada` |
| F7 — cobertura 21 linhas/20 IDs e render sem controle | `CONTROLES` cobre o conjunto EXATO dos 21 IDs (+3 adversariais), nova tabela `AUSENCIA` dos 21, defeito próprio de render-observado, guard de ausência de render, e driver RED durável | `_cobertura_exata`; `render-nao-aconteceu` REPROVADO; suite do autor REPROVA com o mutante `if not render` neutralizado e volta a PASSAR restaurado byte a byte; RED `F7-render-*` |

## Contrato novo — declarado, não mascarado

O artefato `kit09-verdade.entrada.json` (declarado `sintetico=true`/`rotulo_fixture`) NÃO
fecha mais OK: a suite do autor deixou de exigir `exit 0` para ele (agora **exit 2**, zero
OK, `runtime_exercitado=false`) e o caminho OK passou a ser exercitado por uma simulação
positiva NÃO rotulada. Também em `_adaptador_coletor` o input do bloco `campos` passou a
usar o alvo DECLARADO `BottomBar/SkillsButton` (alvo diferente do declarado agora REPROVA,
e ganhou controle próprio). Nenhuma asserção foi enfraquecida: os IDs cobertos por defeito
e por ausência são conferidos por igualdade EXATA com os 21 critérios.

## Arquivos e SHA256

| Arquivo | SHA256 |
| --- | --- |
| tools/automacao/cenarios/kit09.py (corrigido) | 55f01e024e5e5ffd0c28b98ef492e2790c606d57d1dab4ae9d0258fba05feabb |
| tools/automacao/cenarios/test_kit09.py (corrigido) | b4696c8137bca92afd5e96c67c4b8d1b068fc59333e669303c0b6533f0ec87a0 |
| tools/automacao/cenarios/prova_red_kit09.py (novo, durável) | ace59363a82f93c3c64918040c30560cee2333af467d4350cec0471dfc9c882c |
| tools/automacao/runtime/coletor.py (INTOCADO) | 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d |
| tools/automacao/cenarios/rstv.py (INTOCADO) | f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7 |
| tools/automacao/cenarios/test_rstv.py (INTOCADO) | 460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262 |
| scratch/kit/KIT-09R-run637/test_review_kit09.py (imutável, copiado sem edição) | 8411c73f5b532b25c1c149b477518bb989fbf0cc7c4a5815a5cc316dfb7f4075 |

Provas: `scratch/kit/KIT-09F-run639/{baseline-f.json, resumo-verificacao-f.json,
suite-autor.log, contra-autor.log, suite-review-f.log, review-summary.json, measurements.json,
prova-red-f.log, prova-red-f.json, prova-red-f-sandbox.log, red-antigo-autor.log,
fronteira-cic3.log}`. Scripts: `preparar_f.py`, `verificar_f.py`.
Docs: partes 01–05 + esta entrega. Nada de segredo em artefato/log/handoff.

## Preservação e limites

- Nenhum parecer anterior foi reescrito: `docs/automacao/KIT-09R-*` e `KIT-09-entrega.md`
  permanecem como entregues. As alterações manuais do dono em arquivos vivos não foram
  tocadas (só `kit09.py`, `test_kit09.py` e o novo driver entraram nesta frente).
- Travas no repo vivo: `check_segredos.py`, `check_padroes_segredo.py`, `check_dupes.py`,
  `audita_docs.py` — todos exit 0 (não cobrem os untracked novos; não se alega o contrário).
- Fronteira CIC-3 `test_rstv.py` continua vermelha com a MESMA falha pré-existente
  (`esperado 'OK', obtido 'NAO_EXERCITADO'`), sem remover o filtro legítimo de outro mod —
  frente separada `t_fa708909`.
- Runtime/UIUX/desempenho/build/deploy/pacote: **NÃO_EXERCITADO**. Nada aqui substitui
  KIT-G1/G2, o aceite humano (DoD) ou os gates de publicação.
- Este trabalho NÃO conclui o cartão: ele vai para revisão independente
  (`kanban_request_review`), e o reviewer deve tentar refutar F1–F7 por conta própria.
