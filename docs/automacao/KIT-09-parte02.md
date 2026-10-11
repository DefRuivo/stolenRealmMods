# KIT-09 — parte 02 — desenho dos cenarios pequenos (decisoes do implementador)

Cartao `t_a4ca00f9` · offline · nada de jogo/save/build publicavel/publicacao.

## 0. O que ja existe e o que falta (inventario verificado)

| artefato vivo | papel | estado |
|---|---|---|
| `tools/automacao/cenarios/rstv.py` (CIC-3, sha256 ver na entrega) | avaliador com **7 capacidades macro** (`CAPACIDADES`), adaptador das DUAS formas do AUT-4/CIC-5 (`campos` normalizado + campos planos), `_fecha` com fixture/hash/sessao | completo, **nao editado** |
| `tools/automacao/cenarios/test_rstv.py` | suite do CIC-3 | verde, **nao editada** |
| `tools/automacao/aut5/cenarios-rstv.json` | plano de cenarios AUT-5 (`S1`..`S5`) + `origem_do_esperado` | completo, **nao editado** |
| `tools/automacao/aut5/aut5.py` | condutor AUT-5 (`RSTV-5`/`RSTV-30` = botao da run; guardas) | completo, **nao editado** |
| `tools/testes/arcabouco.py` | runner de teste do projeto (`RESULTADO\|PASSOU\|<nome>`, exit 0/1/2) | usado como base |

**Lacuna do KIT-09:** o quadro de 7 capacidades e *macro*. O cartao pede criterios **pequenos e
rastreaveis**: abrir ≠ fechar (≠ fechar por X ≠ fechar por Esc), handler ≠ clique fisico,
"ativo" ≠ ausencia de obstrucao, e "dado velho" como controle que reprova. Falta tambem ligar
cada criterio pequeno a um **esperado independente** (origem declarada, nunca lido da mesma
observacao julgada) e provar que os **adaptadores aceitam a coleta real** (formato do coletor
CIC-5) tambem nesses criterios pequenos.

## 1. Decisoes (implementador)

- **D1 — nao duplicar avaliacao.** `kit09.py` importa `rstv.py` por caminho e reusa
  `_campo`/`_texto` (adaptador das duas formas), `_fecha` (fixture nunca OK, identidade
  obrigatoria, cadeia de hash, sessoes), `_extras`, `_criterio`, `_selecionar_alvos`,
  `_contagem_observada`, `_numerico`, `_lista_de_str`, `_numero_finito`, `_bbox`, `_marcadores`,
  `_RE_TELA`. Nenhum arquivo de outra frente e editado.
- **D2 — criterios pequenos com pai explicito.** Cada criterio pequeno carrega
  `capacidade_pai` (uma das 7 macro de `CAPACIDADES`, ou o grupo novo `KIT09-RSTV5-botao-run`) e
  `cenario_origem` (`S1`..`S5` do plano AUT-5) — rastreabilidade ponta a ponta.
- **D3 — esperado independente.** Todo criterio carrega `esperado_origem` textual; o valor
  *nunca* e derivado do campo observado. Invariante dura: definicao sem `esperado_origem` =
  falha de construcao (fail-closed), nao criterio silencioso.
- **D4 — roll-up preservado.** `por_capacidade()` agrega o pior estado por pai, de modo que a
  decisao existente (CIC-1/2) continua consumindo o quadro das 7 capacidades.
- **D5 — campos novos declarados (contrato KIT-09), nao inventados como ja emitidos.** O probe
  de hoje NAO emite `janela.fechado_x`/`fechado_esc`, `handler_invocado`, `clique_fisico`,
  `obstrucao`. Declarar o contrato e a entrega; a ausencia sai `NAO_EXERCITADO` com
  `lacuna_probe` + `tipo_pendencia='tecnica'` (nunca OK, nunca "maquiado como emitido").
- **D6 — handler e clique fisico sao criterios separados.** `handler_invocado=True` fecha
  `KIT09-RSTV5-handler` sem tocar `KIT09-RSTV5-clique-fisico`; este so fecha com
  `clique_fisico.recebido=True` e o alvo nomeado. Uma prova nunca substitui a outra.
- **D7 — "ativo" nao prova ausencia de obstrucao.** `KIT09-RSTV5-sem-obstrucao` so fecha com
  `obstrucao.avaliada=True` E `obstrucao.obstruido=False`. `ativo_na_hierarquia=True` sem o bloco
  `obstrucao` sai `NAO_EXERCITADO` com motivo nomeando exatamente essa falacia.
- **D8 — dado velho reprova.** `KIT09-sessao-atual`: quando a identidade declara
  `sessao_esperada`, observacao de outra sessao e `REPROVADO` (dado velho), nao "INDETERMINADO
  generico". Sem `sessao_esperada` na identidade o criterio nao julga (`NAO_EXERCITADO`).
- **D9 — dependencia real governa arestas; ausencia legitima nao inventa conector.**
  `KIT09-RSTV25b-arestas` confronta por tier (linhas == Dependency, contagens validas dos dois
  lados), `KIT09-RSTV25b-sem-aresta-inventada` exige contagem observada `== 0`, e
  `KIT09-RSTV25b-ausencia-legitima` fecha OK quando o tier tem Dependency 0 **e** 0 linhas
  (nao vira conector inventado nem defeito).
- **D10 — runtime NAO_EXERCITADO.** Nada aqui abre o jogo; a rodada continua dependendo de
  KIT-G1/G2 e de autorizacao do dono. Fixture testa o AVALIADOR.

## 2. Criterios pequenos (planejados)

| id | pai | cenario | o que fecha OK |
|---|---|---|---|
| KIT09-RSTV21-abre | RSTV-21-janela-ciclo | S1/S4 | `janela.aberta is True` |
| KIT09-RSTV21-fecha | RSTV-21-janela-ciclo | S1/S4 | `janela.fechada is True` |
| KIT09-RSTV21-fecha-x | RSTV-21-janela-ciclo | S1/S4 | `janela.fechado_x is True` |
| KIT09-RSTV21-fecha-esc | RSTV-21-janela-ciclo | S1/S4 | `janela.fechado_esc is True` |
| KIT09-RSTV6-personagem | RSTV-6-readonly-personagem | S1/S3/S4 | personagem == alvo declarado |
| KIT09-RSTV6-skills-sem-mutacao | RSTV-6-readonly-skills-pontos | S1/S4 | par antes/depois igual |
| KIT09-RSTV6-pontos-sem-mutacao | RSTV-6-readonly-skills-pontos | S1/S4 | par antes/depois igual |
| KIT09-RSTV26-render-observado | RSTV-26-placeholders | S5 | texto RENDERIZADO presente |
| KIT09-RSTV26-sem-placeholder | RSTV-26-placeholders | S5 | render sem literal |
| KIT09-RSTV21-tooltip-pai | RSTV-21-tooltip-restauracao | S1 | pai antes == depois |
| KIT09-RSTV21-tooltip-indice | RSTV-21-tooltip-restauracao | S1 | indice antes == depois |
| KIT09-RSTV21-sem-duplicata | RSTV-21-tooltip-restauracao | S1/S4 | `janelas_duplicadas == 0` (contagem valida) |
| KIT09-RSTV25b-arestas | RSTV-25b-dependencia | S5 | linhas por tier == Dependency |
| KIT09-RSTV25b-sem-aresta-inventada | RSTV-25b-dependencia | S5 | contagem de inventadas == 0 |
| KIT09-RSTV25b-ausencia-legitima | RSTV-25b-dependencia | S5 | tier com Dependency 0 e 0 linhas |
| KIT09-RSTV-geo-medida | RSTV-geometria-clipping | S5 | bbox finita, largura/altura > 0 |
| KIT09-RSTV-geo-clipping | RSTV-geometria-clipping | S5 | bbox dentro da tela |
| KIT09-RSTV5-handler | KIT09-RSTV5-botao-run | S4 | `handler_invocado is True` |
| KIT09-RSTV5-clique-fisico | KIT09-RSTV5-botao-run | S4 | clique recebido + alvo nomeado |
| KIT09-RSTV5-sem-obstrucao | KIT09-RSTV5-botao-run | S4 | `obstrucao.avaliada` + nao obstruido |
| KIT09-sessao-atual | (meta) | todas | sessao == `sessao_esperada` da identidade |

## 3. Progresso

- [x] parte01 (esqueleto) · [x] parte02 (desenho)
- [ ] `tools/automacao/cenarios/kit09.py` (modulo)
- [ ] `tools/automacao/cenarios/test_kit09.py` (suite + `--contra-prova`)
- [ ] controles negativos (malformado/ausente/fixture/dado velho/handler-sem-clique/ativo-sem-obstrucao)
- [ ] prova RED (defeito plantado mostrado reprovando) e restaurcao byte a byte
- [ ] `docs/automacao/KIT-09-entrega.md` + hashes
