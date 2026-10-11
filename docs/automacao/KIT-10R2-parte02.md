# KIT-10R2 — parte02: execucao real e achados novos (lente Execution)

Revisor run657 (instancia nova) != implementador run655. Nenhum arquivo do implementador editado.

## Execucoes reais (com exit)

| Checagem | Comando | Resultado |
|---|---|---|
| SHA 4 arquivos | `sha256sum ...` | batem byte a byte com o handoff run655 |
| Suite kit10 | `python tools/automacao/kit10/test_kit10_cenarios.py` | **24/24 PASSOU, exit 0** |
| Isca | `... --isca` | `ISCA|OK|defeito plantado detectado`, **exit 0** |
| Probe run651 (o que ACHOU F1/F2/F3) | `python scratch/kit/KIT-10R-run651/probe_revisor.py` | P2/P3/P3b/P4 de `OK/True` -> **`NAO_EXERCITADO/False`**; P5 segue `NAO_EXERCITADO`; exit 0 |
| RED antigo | `python scratch/kit/KIT-10-run/prova_red_kit10.py` | 5/5 load-bearing, **exit 0** |
| RED novo (guardas F1F2F3) | `python scratch/kit/KIT-10-run655/prova_red_kit10_guardas.py` | 3/3 (original NAO_EXERCITADO/False -> neutralizado OK/True), **exit 0** |
| CLI fixture | `python tools/automacao/kit10/kit10_cenarios.py --observacoes scratch/kit/KIT-10-run/fixture.json --json` | `exit 2`, OK=0, NAO_EXERCITADO=19, **com_prova_runtime=0** |
| Reuso CIC-4 | `python tools/automacao/cenarios/test_tooltips_shrines.py` | **28/28 exit 0** |
| Travas repo | check_segredos / check_padroes_segredo / check_dupes / audita_docs | **4/4 exit 0** |

Conclusao parcial: as 3 correcoes pedidas pelo KIT-10R (F1/F2/F3) ESTAO presentes e o proprio
probe que as encontrou agora as mostra corrigidas. Positivos e negativos preservados.

## Achados NOVOS (rodada 2, lente Execution) — reproducao propria

Probe: `scratch/kit/KIT-10R2-run657/probe_revisor2.py` e `probe_revisor3.py` (saidas reais abaixo).

### F5 (ALTO) — `dano_observado` AUSENTE ainda vira OK/prova_runtime=True
`_asp_contexto_dano` (kit10_cenarios.py ~l.249/269): `dano_observado` nao entra em NENHUMA guarda.
Com `fonte_bonus=0` e sem `aura_buff`, o conjunto sai com `defeito=[]` e o fechamento promove a
`OK/True`. O `motivo` passa a afirmar "dano do ground effect bate com o oraculo" **sem nenhum dano
medido**. Viola o cartao: "runtime ausente nao recebe OK".

Reproducao real:
```
R8 dano AUSENTE -> [('sem-dano','OK',True,'dano do ground effect bate com o oraculo no eixo `Source` (bonus 0) ...')]
R9 dano AUSENTE + buff medido -> [('sem-dano-buff','OK',True,'dano do ground effect bate ...')]
R10 dano errado (CONTROLE) -> [('dano-errado','REPROVADO',False,'dano observado=17 e esperado=10 ...')]
```
R10 prova que a checagem de dano FUNCIONA quando o dano existe — mas e' puramente `if dano is not
None`, entao a AUSENCIA do dano escapa. Correcao minima: `dano_observado` ausente -> `NAO_EXERCITADO`
(nunca OK), + controle negativo novo na suite + guarda RED.

### F6 (MEDIO) — `receptor_bonus` ausente assume 0 e a afirmacao do eixo Target fica vazia
`receptor = float(_campo(obs,"receptor_bonus") or 0)` (l.244). Ausente == 0. Com `contrib_observada`
coerente com bonus 0, o criterio fecha `OK/True` e afirma "a tooltip de buff le o bonus do RECEPTOR
(eixo Target)" — afirmacao indecidivel: com bonus 0 a leitura por `Source` e por `Target` dao o
MESMO valor, entao o eixo (que e o PONTO do aspecto A) nao foi exercitado.
Reproducao: `R3 receptor ausente -> [('receptor-ausente','OK',True)]`.
Correcao minima: `aura_buff` declarado + `receptor_bonus` ausente -> `NAO_EXERCITADO`.

### F7 (BAIXO, observacao de classificacao) — `fonte_bonus` ausente vira REPROVADO
`R2 fonte ausente -> [('fonte-ausente','REPROVADO',False)]`: campo ausente (nao medido) e' rotulado
como defeito DETECTADO (FALHOU), nao como NAO_EXERCITADO. Nao e' falso-OK (nao e' OK), mas confunde
FALHOU com NAO_EXERCITADO, que o cartao manda distinguir.

## F4 (redeclaracao) — `test_estilo_atributos.py`
Em curso nesta arvore viva (suite longa/bloqueada em buffering). Ver parte03.
