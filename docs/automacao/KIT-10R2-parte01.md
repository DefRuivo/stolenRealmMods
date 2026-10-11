# KIT-10R2 — Revisao independente da rodada 2 (lente: EXECUTION)

- Cartao: t_bbad760d (KIT-10)
- Rodada de revisao: 2 (houve 1 `changes_requested` — run651). Revisor desta rodada: run657, instancia nova.
- Implementador desta rodada: run655 (KIT-10F, correcao do F1/F2/F3/F4 do KIT-10R).
- Lente obrigatoria da rodada 2: **Execution** — clonar/rodar o entregavel, verificar cada claim empiricamente.

## Objetivo da revisao

Verificar independentemente se a correcao KIT-10F resolveu os 3 falsos-OK (F1/F2/F3) e
redeclarou F4, SEM enfraquecer o que ja passava (CIC-4/AUT-7 reuso, controles negativos, isca).

## Reproducao — rodada 1 (baseline de trabalho, FEITO)

- SHA dos 4 arquivos conferem byte a byte com o handoff run655:
  - `tools/automacao/kit10/kit10_cenarios.py` = a46cf76f011947c58f8ca87c4579c13c8b24ff8b5c6caf674570d83ddaab1414 OK
  - `tools/automacao/kit10/test_kit10_cenarios.py` = 30ca0c493d2fe018a64818c06555591f3afe7da12e74b9fcb4eb73ebe6feb427 OK
  - `scratch/kit/KIT-10-run655/prova_red_kit10_guardas.py` = 84d5601873820f86599244e587f267aee808dc3f1ec7b64f9ed1359b85b27a87 OK
  - `scratch/kit/KIT-10-run/prova_red_kit10.py` (intocado) = b01919cf... OK
- `git status` confirma: KIT-10 so criou `tools/automacao/kit10/` (untracked) + `docs/automacao/KIT-10*`.
  Nenhum mod/gameplay/`t_*` tocado por esta frente.

## Checagens de execucao (a preencher)

- [ ] suite `test_kit10_cenarios.py` — esperado 24/24 exit0
- [ ] `--isca` — esperado exit0 com defeito plantado detectado
- [ ] probe do revisor run651 (`scratch/kit/KIT-10R-run651/probe_revisor.py`) — esperado P2/P3/P3b/P4 de OK/True para NAO_EXERCITADO/False
- [ ] RED antigo 5/5 + RED novo 3/3
- [ ] F4: `test_estilo_atributos.py` exit real na arvore viva
- [ ] CLI em fixture — exit2, OK=0, com_prova_runtime=0
- [ ] reuso CIC-4 `test_tooltips_shrines.py` — 28/28 exit0
- [ ] travas do repo (check_segredos/check_padroes_segredo/check_dupes/audita_docs)

## Veredito

(pendente)
