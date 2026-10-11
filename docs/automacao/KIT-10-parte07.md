# KIT-10G — parte 07: prova-RED das guardas e regressões

## Prova-RED durável (scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py)

Discriminador: original `NAO_EXERCITADO/False` → guarda neutralizada `OK/True` (a lacuna escapa).
Cobre as 3 guardas da rodada 1 (F1/F2/F3 do KIT-10R) e as 3+1 novas (F5/F6/F7 do KIT-10R2 +
tooltip/`aura_buff`). Saída real: **PROVA-RED|PASSOU|7 mutacoes|todas as guardas sao load-bearing**, exit 0.

```
PROVA-RED|OK|F1-estagio-desconhecido|original=NAO_EXERCITADO/False neutralizado=OK/True
PROVA-RED|OK|F2-itens-ausentes|original=NAO_EXERCITADO/False neutralizado=OK/True
PROVA-RED|OK|F3-contrib-ausente|original=NAO_EXERCITADO/False neutralizado=OK/True
PROVA-RED|OK|F5-dano-ausente|original=NAO_EXERCITADO/False neutralizado=OK/True
PROVA-RED|OK|F6-receptor-ausente|original=NAO_EXERCITADO/False neutralizado=OK/True
PROVA-RED|OK|F7-fonte-ausente|original=NAO_EXERCITADO/False neutralizado=OK/True
PROVA-RED|OK|G7-buff-ausente|original=NAO_EXERCITADO/False neutralizado=OK/True
```

Nota honesta: o driver da rodada 1 (`scratch/kit/KIT-10-run655/prova_red_kit10_guardas.py`) foi
**superado** pela renomeação `lacuna` → `lacunas` (guardas passaram a acumular várias lacunas). Ele
ainda cobre F1/F2 (`PROVA-RED|OK`) mas o G3-contrib sai `FALHOU|trecho a mutar nao encontrado no
fonte: 'elif lacuna:'` (exit 1) porque o marcador foi para `elif lacunas:`. O driver novo cobre o
G3-contrib com o marcador correto. Nada foi escondido.

## Regressões reexecutadas (rodada 659)

- probe_revisor (rodada 1, KIT-10R-run651): P2/P3/P3b/P4/P5 → NAO_EXERCITADO/False, exit 0.
- probe_revisor2/3 (rodada 2, KIT-10R2-run657): R1 OK/True; R2/R3/R8/R9 NAO_EXERCITADO/False;
  R10 REPROVADO; R4/R5/R6/R7 inalterados — exit 0. Saída: `scratch/kit/KIT-10-run659-probe-revisor.txt`.
- CLI em fixture (`scratch/kit/KIT-10-run/fixture.json`): exit 2, `OK=0, NAO_EXERCITADO=19`,
  `com prova runtime: 0`.
- Reuso CIC-4 `tools/automacao/cenarios/test_tooltips_shrines.py`: 28/28 exit 0.
- Travas do repo: check_segredos / check_padroes_segredo / check_dupes / audita_docs → 4/4 exit 0.
- F4 (`tools/automacao/estilo/test_estilo_atributos.py`): medido nesta rodada = **exit 0**
  (`total: 28 | falhas: 0`, "TUDO OK"; saída `scratch/kit/KIT-10-run659-estilo.txt`). O `exit 1`
  visto no run655/run657 era estado transitório de OUTRA frente (escritores concorrentes); a
  árvore viva hoje fecha 28/28. KIT-10 não toca o mod BetterFont.
