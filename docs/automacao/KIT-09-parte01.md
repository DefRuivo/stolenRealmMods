# KIT-09 — parte 01 — esqueleto e inventario inicial

Cartao: t_a4ca00f9 (KIT-09) — "Completar pacote de cenarios RSTV para o primeiro marco".
Revisao prevista: t_0564b789 (KIT-09R), ja criado como filho.
Autorizacao vigente: dono, 07/10/2026 ("prossiga com as implementacoes"), offline, fila serial.
Runtime, jogo, save, instalacao, publicacao: NAO autorizados — NAO_EXERCITADO por definicao.

## Objetivo

Reusar AUT-5 (t_76a41ea7) e CIC-3 (t_7fdce47f) para cobrir observacao e teste do Skill Tree
Visualizer (RSTV) com criterios pequenos e rastreaveis, estendendo artefatos existentes sem
reabrir o aceite funcional anterior dos mods.

## Itens a cobrir (do corpo do cartao)

1. Cenarios abrir/fechar.
2. Personagem correto.
3. Tooltip sem placeholders.
4. Anti-duplicacao.
5. Skills/pontos antes-depois sem mutacao.
6. Pai/indice do tooltip restaurados.
7. Geometria/clipping.
8. Dependency real governa arestas; ausencia legitima nao inventa conector.
9. Handler e clique fisico sao testes distintos; ativo nao prova ausencia de obstrucao.
10. Esperado independente rastreavel.
11. Adaptadores aceitam output real da coleta; controles malformado/ausente/fixture/dado velho reprovam.
12. Runtime fica NAO_EXERCITADO ate KIT-G2/KIT-14.

## Inventario inicial (nao exaustivo)

- tools/automacao/cenarios/rstv.py (1152 linhas), test_rstv.py (703), tooltips_shrines.py (978),
  test_tooltips_shrines.py (630), rstv-*.entrada.json.
- tools/automacao/aut5/aut5.py (963), log_rstv.py (594), test_aut5.py (850), cenarios-rstv.json (122).
- tools/testes/regras_rstv*.py e tools/testes/testes/puros/t_rstv*.py (modificados e untracked).
- docs/automacao/AUT-5*.md, CIC-3*.md.

## Status

EM ANDAMENTO — parte 01 gravada antes da exploracao profunda (regra artefato-primeiro).
Proximos blocos: ler contratos AUT-5/CIC-3, mapear o que ja existe, identificar lacunas do pacote
de cenarios, implementar/extender offline, provar com execucao real (exit + caminhos + hashes).
