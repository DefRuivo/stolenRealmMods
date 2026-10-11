# KIT-09F — parte 05: tabela da prova RED seletiva (12 guardas)

Driver: `tools/automacao/cenarios/prova_red_kit09.py` (durável, no repositório).
Mutação in-memory com conferência de SHA256 do fonte antes/depois; `PROVA-RED|PASSOU|12
mutacoes|falhas=0` (exit 0). Coluna "neutralizado reprova" = a checagem normativa FALHA
quando SÓ aquela guarda é neutralizada (é a prova RED exigida por item).

| Mutação | Critério | Verde no original | Neutralizado reprova |
| --- | --- | --- | --- |
| F1-rotulo-na-observacao | KIT09-RSTV6-personagem | PASSA | SIM |
| F1-envelope-sintetico | KIT09-RSTV26-render-observado | PASSA | SIM |
| F6-sessao-esperada | KIT09-RSTV6-pontos-sem-mutacao | PASSA | SIM |
| F2-leitura-normalizada | KIT09-RSTV21-tooltip-pai | PASSA | SIM |
| F4-validacao-de-caminho | KIT09-RSTV21-tooltip-pai | PASSA | SIM |
| F4-finitude-dos-pontos | KIT09-RSTV6-pontos-sem-mutacao | PASSA | SIM |
| F3-mapas-vazios | KIT09-RSTV25b-arestas | PASSA | SIM |
| F3-t5-no-criterio-especifico | KIT09-RSTV25b-sem-aresta-inventada | PASSA | SIM |
| F3-ausencia-nao-e-zero | KIT09-RSTV25b-ausencia-legitima | PASSA | SIM |
| F5-alvo-do-clique | KIT09-RSTV5-clique-fisico | PASSA | SIM |
| F7-render-igual-ao-template | KIT09-RSTV26-render-observado | PASSA | SIM |
| F7-render-ausente | KIT09-RSTV26-render-observado | PASSA | SIM |

Prova de suíte (o caso que a revisão usou): mutante em disco só com o guard
`if not render` neutralizado → **suite do autor exit 1 (REPROVOU)**; byte original
restaurado → **exit 0 (PASSOU)**; `sha restaurado == original: True`
(`F7-render-ausente` em `prova-red-f.json`). Ou seja: o falso verde que o reviewer
demonstrou (mutante `823e7cda…`) não existe mais.
