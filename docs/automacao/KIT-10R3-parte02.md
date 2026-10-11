# KIT-10R3 - parte02: verificacao campo-a-campo e criterios do corpo original

## Lente CONTRACT (rodada 3)
Corpo original relido; cada criterio de aceite mapeado a prova real.

| Criterio do corpo (KIT-10) | Prova nesta rodada | Veredito |
|---|---|---|
| Relacionar tooltip/contexto/dano e fonte/receptor em shrines | aspecto A `_asp_contexto_dano` (kit10_cenarios.py l.224-358); probe proprio `probe_r3_ausentes.py` (base OK/True, 9 campos removidos -> NAO_EXERCITADO) | PASSOU |
| Preservar Worship confirmado; nao remover dobro | aspecto B; controle R7 dobro-removido -> REPROVADO (probe revisor2 reexecutado); N-B-dobro -> REPROVADO (suite) | PASSOU |
| BetterStats base SavedMap/final | reuso AUT-7 `estilo_atributos.py` (t_reuso_cic4_aut7 exige ids `AUT-7/BetterStats/`); BCT idem | PASSOU |
| BetterFont/BCT material/keywords/cores e superficies POR EVENTO, nao prefab de boot | aspecto C; probe: estagio=boot -> REPROVADO, estagio inventado -> NAO_EXERCITADO; N-C-boot -> REPROVADO | PASSOU |
| Debugger contrato sem truncar | aspecto D (reusa regras_debugger); suite D-defeito-truncado / D-defeito-pipe -> REPROVADO | PASSOU |
| Criterios independentes rastreaveis | t_esperado_rastreavel_kit10 exige fonte (regras_shrine/RV-/DWA-2/census) no esperado | PASSOU |
| Varias superficies + controles negativos | CIC-4 + AUT-7 + 4 aspectos; 5 controles negativos + 9 guardas anti-falso-OK + 2 iscas | PASSOU |
| Runtime ausente nao recebe OK | t_fixture_nao_prova_runtime (exit 2); CLI fixture OK=0/NAO_EXERCITADO=19 exit2; RED 7/7 | PASSOU |
| Nao modificar mods/gameplay | git status: esta frente so cria `tools/automacao/kit10/` + `docs/automacao/KIT-10*` | PASSOU |

## Correcoes das rodadas anteriores (todas aterrissaram e sao load-bearing)
- F1 (rodada 1): `_asp_por_evento` whitelist em TODOS os ramos (l.457-469); RED F1 e G1; probe P2.
- F2 (rodada 1): `_asp_worship_dobro` aura viva sem item -> `faltando` -> NAO_EXERCITADO (l.392-396); G2; probe P3/P3b.
- F3 (rodada 1): `_asp_contexto_dano` buff fora da tabela/contrib ausente -> lacuna (l.313-326); G3; probe P4.
- F5 (rodada 2): `dano_observado` ausente -> lacuna (l.281-286); G4; probe R8/R9.
- F6 (rodada 2): `receptor_bonus` ausente/0 -> lacuna (l.244-304); G5; probe R3.
- F7 (rodada 2): `fonte_bonus` ausente -> lacuna, so medido !=0 vira defeito RV-34 (l.270-278); G6.
- Extra G7: `aura_buff` ausente -> lacuna (l.307-312).
RED driver run659: 7/7 neutralizacoes (NAO_EXERCITADO/False -> OK/True). Defeito MEDIDO continua vencendo lacuna (R10 dano errado -> REPROVADO). Correcoes NAO enfraqueceram a deteccao.

## Refutacao propria (novo)
`scratch/kit/KIT-10-run662-rev/probe_r3_ausentes.py`: caso BASE valido fecha OK/True (controle
positivo). Removendo UM campo por vez em A (aura_dano, tipo_alvo, maxhealth, fonte_bonus,
receptor_bonus, dano_observado, aura_buff, atributo, contrib_observada) e em C (estagio, evento_id,
objeto): TODOS -> NAO_EXERCITADO/False. Nenhum FALSO OK. `PROBE-R3|PASSOU`.

## F4 - test_estilo_atributos.py (REDECLARACAO DO IMPLEMENTADOR IMPRECISA)
Medido por mim nesta rodada: **exit 1** (`total: 28 | falhas: 1`, "BetterFont devia ter provas da
suite pura"); a mesma suite imprimiu `falhas: 0 / TUDO OK` alguns minutos antes, na MESMA sessao.
O proprio teste imprime "(sem criterio de suite: drift na arvore viva - repetindo a rodada)".
Causa confirmada por `git status`: escritores de OUTRA frente alteram
`tools/automacao/runtime/AUT4Probe/*.cs` e `tools/testes/fixtures/geradores/oraculo_excesso_shrine/Program.cs`.
=> O exit e NAO-DETERMINISTICO e NAO e causado pelo KIT-10 (esta frente nao toca mod nem familia
`t_*`). O handoff run659 declarar "exit 0" e verdadeiro-so-condicionalmente; o valor honesto e
INDETERMINADO (0 ou 1 conforme o estado volatil da arvore viva).

## Prova e caminhos
- scratch/kit/KIT-10-run662-rev/{suite,isca,red,cic4,estilo,cli}.out
- scratch/kit/KIT-10-run662-rev/probe_r3_ausentes.py + probe_r3.out
