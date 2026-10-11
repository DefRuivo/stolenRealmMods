# KIT-09F — parte 04: execuções reais (sandbox nova, offline)

Sandbox: `scratch/kit/KIT-09F-run639/sandbox` (sem `.git`; 464 arquivos inventariados em
`baseline-f.json`). Script independente do reviewer copiado SEM edição:
`scratch/kit/KIT-09F-run639/test_review_kit09.py`, SHA256
`8411c73f5b532b25c1c149b477518bb989fbf0cc7c4a5815a5cc316dfb7f4075` (idêntico ao original
em `scratch/kit/KIT-09R-run637/test_review_kit09.py`).

Bateria: `scratch/kit/KIT-09F-run639/verificar_f.py` → `resumo-verificacao-f.json`.

| Execução | Comando | Resultado | Log |
| --- | --- | --- | --- |
| Suite do autor | `python tools/automacao/cenarios/test_kit09.py` (cwd sandbox) | `RESULTADO\|PASSOU\|kit09-rstv`, **exit 0** | `suite-autor.log` |
| Contra-prova (isca sempreOK) | `... test_kit09.py --contra-prova` | `CONTRA-PROVA\|PASSOU\|... 24 controles`, **exit 0** | `contra-autor.log` |
| **Suite independente do reviewer** | `python test_review_kit09.py` (fonte corrigido) | `SUMMARY {"total": 30, "failed": [], "errors": [], "skipped": [], "passed": 30}`, **exit 0** (antes: 19 FAIL/11 OK, exit 1) | `suite-review-f.log`, `review-summary.json`, `measurements.json` |
| Prova RED por guarda | `python tools/automacao/cenarios/prova_red_kit09.py` | `PROVA-RED\|PASSOU\|12 mutacoes\|falhas=0`, **exit 0** | `prova-red-f.log`, `prova-red-f.json`, `prova-red-f-sandbox.log` |
| Prova RED antiga do autor | `python scratch/kit/k09/prova-red-kit09.py` (sandbox) | defeito → exit 1; restaurado byte a byte → exit 0, **exit 0** | `red-antigo-autor.log` |
| Fronteira CIC-3 | `python tools/automacao/cenarios/test_rstv.py` | `REPROVOU\|cic3-rstv\|hash_fonte == dll_sha ... esperado 'OK', obtido 'NAO_EXERCITADO'`, **exit 1** (pré-existente, INTOCADA) | `fronteira-cic3.log` |

Resumo: `{"suite-autor": 0, "contra-autor": 0, "red-antigo-autor": 0, "fronteira-cic3": 1,
"suite-review-indep": 0, "prova-red": 0}`.

## Catálogo de medições da suite do reviewer (o que cada achado virou)

- F1 — `test_cli_synthetic_fixture_must_not_claim_runtime` OK; `test_fixture_label_on_observation_not_runtime`
  OK (`ORIGEM DECLARADA SINTETICA/FIXTURE (rotulo_fixture='offline-test')`).
- F2 — `normalized-parent/index/duplicate` positivo OK; defeito `REPROVADO`
  (`tooltip pai NAO restaurado: antes='Original/Tooltip', depois='Wrong/Parent'`).
- F3 — `absent-lines`/`malformed-lines` NAO_EXERCITADO; `empty-maps-edges` INDETERMINADO;
  `missing-t5-dependency` INDETERMINADO; `t5-invented-edge` REPROVADO.
- F4 — `parent-malformed-equal`, `index-malformed-equal`, `index-negative-equal` NAO_EXERCITADO;
  `points-infinite` NAO_EXERCITADO.
- F5 — `wrong-click-target` REPROVADO (`esperado 'BottomBar/SkillsButton', observado 'MainMenu/QuitButton'`).
- F6 — `old-session-meta` REPROVADO; `old-session-capability` NAO_EXERCITADO com `prova_runtime=false`.
- F7 — `render` coberto por controle próprio e por mutação específica (ver parte 03).

## Travas do repositório vivo (leitura)

`python tools/check_segredos.py` exit 0 · `check_padroes_segredo.py` exit 0 ·
`check_dupes.py` exit 0 · `audita_docs.py` exit 0.
