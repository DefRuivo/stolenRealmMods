# KIT-12 — revisao independente RODADA 2 (run670), lente EXECUTION

Cartao revisado: `t_0a434c97` (KIT-12 "Integrar alteracao, evidencia, correcao e revalidacao").
Rodada 1 (run668, lente Artifact) pediu correcao de F1/F2 -> implementador run669 corrigiu e pediu
reconferencia. Esta rodada 2 NAO repete a rodada 1: o metodo e **checkout e execucao propria**
(build/testes/CLI rodados por mim), conferindo empiricamente cada afirmacao do handoff run669,
inclusive as quatro afirmacoes-refutacao listadas em `KIT-12F-entrega.md` secao 6.

Revisor: instancia run670 (default) != implementador run669 != revisor de origem run668.
Papel: revisor. **Nenhum arquivo de produto foi editado por mim** — codigo do revisor fica em
`scratch/kit/KIT-12R-run670-rev/` e o parecer em `docs/automacao/`.

## Perguntas desta rodada (falsificacao por execucao)

| # | Afirmacao do handoff run669 | Como vou medir |
|---|---|---|
| A0 | hashes 4/4 do handoff batem com o disco | sha256sum dos 4 arquivos |
| A1 | suite `Ran 24 tests OK` exit 0 | rodar a suite em copia isolada |
| A2 | isca `9/9` mutacoes discriminadas + controle restaurado | rodar `--isca` |
| A3 | CLI sandbox: exits 2 -> 1 -> 2 -> 2 -> 3, `PROVA|PASSOU` | rodar `prove_ciclo.py` |
| F1a | coleta com `hash_fonte` de OUTROS bytes -> INCOMPLETO/exit 2 (era APROVADO/exit 0) | sonda propria |
| F1b | coleta SEM `hash_fonte` -> INCOMPLETO/exit 2 (fail-closed) | sonda propria |
| F1c | criterio declarando `fonte_sha`/`dll_sha` de bytes antigos -> NAO_EXERCITADO/exit 2 | sonda S8 do revisor run668, reexecutada |
| F1d | contra-prova: coleta declarando o hash DA RODADA -> OK offline SOBREVIVE (nao virou trava cega) | sonda propria |
| F2 | campo executavel removido do CRITERIO (nao so do item da fila) | sonda S1 do revisor run668 + varredura dos JSON |
| T1 | travas do repo continuam verdes | check_segredos, check_padroes_segredo, check_dupes, audita_docs |

## Veredito (preenchido ao final)

- [ ] A0 hashes
- [ ] A1 suite
- [ ] A2 isca
- [ ] A3 CLI sandbox
- [ ] F1a / F1b / F1c / F1d
- [ ] F2
- [ ] T1 travas

NAO_EXERCITADO (por natureza do cartao): jogo/probe/save/perfil real, runtime AUT-4, UI/UX/pixels,
build C#, pre-flight de deploy, instalacao, publicacao, aceite humano/DoD. Fixture nao comprova runtime.
