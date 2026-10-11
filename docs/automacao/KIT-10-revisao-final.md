# KIT-10 - PARECER FINAL de revisao independente (rodada 3, lente CONTRACT)

Task revisada: **t_bbad760d** (KIT-10). Revisor: **run 662** (instancia nova, sessao separada).
Implementador da rodada 3: **run 659**. Revisores anteriores: run 651 (rodada 1), run 657 (rodada 2).
Nenhum arquivo do implementador foi editado por este revisor. Workspace proprio:
`scratch/kit/KIT-10-run662-rev/`.

## VEREDITO: **APROVADO**

Entregavel `tools/automacao/kit10/kit10_cenarios.py` + `test_kit10_cenarios.py` +
`scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py` atendem ao corpo original. Todas as
correcoes pedidas nas rodadas 1 (F1-F4) e 2 (F5-F7) aterrissaram, sao load-bearing e nao
enfraqueceram a deteccao de defeito medido. Nenhum falso-OK remanescente foi encontrado na
varredura campo-a-campo do revisor.

## Criterios do corpo (mapeados a prova real) - todos PASSOU
1. Tooltip/contexto/dano e eixo fonte x receptor em shrines - aspecto A; base OK/True e 9 campos
   removidos -> NAO_EXERCITADO (probe proprio).
2. Worship confirmado preservado; dobro NAO removido - aspecto B; R7/N-B-dobro -> REPROVADO.
3. BetterStats base SavedMap/final - reuso AUT-7 (t_reuso_cic4_aut7 exige `AUT-7/BetterStats/`).
4. BetterFont/BCT por EVENTO, nao prefab de boot - aspecto C; boot -> REPROVADO; inventado -> NAO_EX.
5. Debugger contrato sem truncar - aspecto D; D-defeito-truncado / D-defeito-pipe -> REPROVADO.
6. Criterios independentes rastreaveis - t_esperado_rastreavel_kit10 exige fonte no esperado.
7. Varias superficies + controles negativos - CIC-4 + AUT-7 + 4 aspectos; 5 controles + 9 guardas + 2 iscas.
8. Runtime ausente nao recebe OK - fixture exit 2; CLI fixture OK=0/NAO_EXERCITADO=19; RED 7/7.
9. Nao modificar mods/gameplay - git status: so `tools/automacao/kit10/` + `docs/automacao/KIT-10*`.

## Execucoes reais nesta rodada (exit codes reais, sem pipe)
| Check | Comando | Resultado |
|---|---|---|
| Suite KIT-10 | `python tools/automacao/kit10/test_kit10_cenarios.py` | 28/28, **exit 0** |
| Isca | `... --isca` | ISCA|OK defeito detectado, **exit 0** |
| RED run659 | `python scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py` | 7/7 mutacoes, **exit 0** |
| Probe revisor1 | `scratch/kit/KIT-10R-run651/probe_revisor.py` | P2/P3/P3b/P4/P5 NAO_EXERCITADO, **exit 0** |
| Probe revisor2 | `scratch/kit/KIT-10R2-run657/probe_revisor2.py` | R1 OK; R2/R3 NAO_EX; R5/R7 REPROVADO, **exit 0** |
| Probe revisor3 | `scratch/kit/KIT-10R2-run657/probe_revisor3.py` | R8/R9 NAO_EX; R10 REPROVADO, **exit 0** |
| Probe proprio R3 | `scratch/kit/KIT-10-run662-rev/probe_r3_ausentes.py` | PROBE-R3|PASSOU, **exit 0** |
| CLI fixture | `... --observacoes scratch/kit/KIT-10-run/fixture.json` | OK=0 NAO_EX=19, **exit 2** |
| Reuso CIC-4 | `python tools/automacao/cenarios/test_tooltips_shrines.py` | 28/28, **exit 0** |
| Travas repo | check_segredos / check_padroes_segredo / check_dupes / audita_docs | **4/4 exit 0** |

## Hashes conferidos (batem com o handoff run659)
- `tools/automacao/kit10/kit10_cenarios.py` = 8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092
- `tools/automacao/kit10/test_kit10_cenarios.py` = 6cc5003e0d9facd42cf967b2da480216243b6d902376f5fc20d9c49d9e8db6e2
- `scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py` = aa9f232b78b0e4cda8ca6de63bcda417cb1b5c79b635ad6235151177c834c6ff
- artefatos do revisor: probe_r3_ausentes.py = 76f0700492e0f011cfe43c5dc078073370e389ac99dac22dac21e6ea8f22c487

## CAVEATS (nao bloqueiam o aceite)
- **F4 (redeclaracao instavel):** `tools/automacao/estilo/test_estilo_atributos.py` medido por mim
  deu **exit 1** ("BetterFont devia ter provas da suite pura"); na MESMA sessao, minutos antes, deu
  `falhas: 0 / TUDO OK`. O proprio teste imprime "drift na arvore viva"; causa confirmada em
  `git status` (AUT4Probe/*.cs e oraculo fixture alterados por OUTRA frente). O exit e
  **NAO-DETERMINISTICO e NAO e do KIT-10**. O valor honesto da declaracao e INDETERMINADO (0 ou 1),
  nao "exit 0" fixo. Isto NAO afeta nenhum criterio do KIT-10.
- **Runtime/UIUX/desempenho/build/deploy/pacote/publicacao: NAO_EXERCITADO.** Esta revisao e offline.
  Aprovacao tecnica NAO equivale a aceite humano (DoD) nem aos gates KIT-G1/G2/G3/G4.
- Suite e fixtures sao offline: provam o avaliador, nao o runtime.

## Passo seguinte
Aprovar tecnicamente; liberar o cartao de revisao independente downstream (t_896796be) e os gates
humanos. Se o dono quiser o exit estavel do `test_estilo_atributos.py`, tratar como causa EXTERNA
ao KIT-10 (frente de mods), nao neste cartao.

## Caminhos
- docs/automacao/KIT-10R3-parte01.md, KIT-10R3-parte02.md, KIT-10-revisao-final.md
- scratch/kit/KIT-10-run662-rev/{suite,isca,red,cic4,estilo,cli}.out, probe_r3_ausentes.py, probe_r3.out
