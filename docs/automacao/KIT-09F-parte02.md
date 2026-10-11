# KIT-09F — parte 02: correção do fonte (F1–F7) em `kit09.py`

Bloco de implementação. Arquivo único editado: `tools/automacao/cenarios/kit09.py`
(dependências `rstv.py` e `coletor.py` NÃO tocadas — SHA conferido abaixo).

## O que mudou, por achado

- F1 (origem declarada) — novas `_marcas_de_origem`/`_guarda_origem`; marcas de
  `sintetico=true`/`rotulo_fixture`/`simulado` na observação OU no envelope, e
  procedência do envelope CONTRADIZENDO a da observação, entram como MOTIVO em todos os
  critérios (nunca OK/prova_runtime). Defeito observado continua REPROVANDO (precedência
  do defeito). `avaliar_cenarios(..., envelope=None)`; CLI passa o envelope;
  `resumir` conserva `origem`/`procedencias`/`sessoes_observadas`/`lacunas` e só marca
  `runtime_exercitado` sem marca de origem.
- F2 (adaptador normalizado) — `_reg_tooltip_campo` e `_reg_sem_duplicata` passam a ler
  por `RC._campo` (topo + bloco `campos` do coletor real) em vez de `o.get`/`in`;
  `_reg_sessao_atual` e `_reg_sem_aresta_inventada` idem.
- F3 (ausência ≠ zero / T5) — `_reg_dep_arestas` exige leitura dos DOIS lados por tier
  (tier presente em um só lado = motivo), mapas vazios = motivo, T5 julgado pela regra
  geral; `_reg_sem_aresta_inventada` julga TODOS os tiers (o `continue` de T5 saiu);
  `_reg_ausencia_legitima` não inventa zero para linhas ausentes/string.
- F4 (malformado/domínio/finitude) — validadores `_valor_caminho`/`_valor_indice`
  aplicados ANTES da igualdade; finitude (`RC._numero_finito`) antes de comparar pontos.
- F5 (alvo do clique) — `ALVO_BOTAO_RUN` declarado (AUT-5 S4/RSTV-30), sobrescrevível por
  `clique_fisico_alvo_esperado`/`alvo_botao_run`; alvo esperado é VALIDADO como path/id;
  observado != esperado REPROVA; alvo esperado ausente/inválido não julga.
- F6 (sessão esperada por critério) — `_guarda_sessao`: observação de sessão diferente da
  `sessao_esperada` nunca qualifica (motivo), sem suprimir defeito observável.
- F7 (cobertura) — `_reg_render_observado` ganha defeito medido próprio (render idêntico
  ao template cru com token do motor) e a leitura de ausência de render passa a ser um
  guard próprio (`if not render: ... continue`).

## SHA256 depois da correção

| Arquivo | SHA256 |
| --- | --- |
| tools/automacao/cenarios/kit09.py | 55f01e024e5e5ffd0c28b98ef492e2790c606d57d1dab4ae9d0258fba05feabb |
| tools/automacao/cenarios/test_kit09.py | b4696c8137bca92afd5e96c67c4b8d1b068fc59333e669303c0b6533f0ec87a0 |
| tools/automacao/cenarios/prova_red_kit09.py | ace59363a82f93c3c64918040c30560cee2333af467d4350cec0471dfc9c882c |
| tools/automacao/runtime/coletor.py (intocado) | 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d |
| tools/automacao/cenarios/rstv.py (intocado) | f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7 |
| tools/automacao/cenarios/test_rstv.py (intocado) | 460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262 |
