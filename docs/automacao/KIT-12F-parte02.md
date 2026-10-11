# KIT-12F — parte 02: correcao aplicada, suite verde

## O que foi feito (produto `tools/automacao/kit12/integracao.py`)

F1 — procedencia confrontada (fail-closed), sem sobrescrita silenciosa:
- nova `confrontar_coleta(coleta_meta, ident)`: `hash_fonte` da coleta vs `fonte_sha` da identidade da rodada;
  divergencia -> `tipo="contraditoria"`; ausencia -> `tipo="ausente"`.
- nova `confrontar_cadeia_declarada(criterios, ident)`: percorre `CAMPOS_CADEIA` (fonte_sha/dll_sha/config_sha/versao/sessao)
  e registra o que o CRITERIO declara diferente da identidade (`declaracoes_contraditorias` + `declaracao_sobrescrita=True`).
- em `criterios_da_cadeia`, antes do `anexar_cadeia`: cada achado vira LACUNA nomeada
  (`cadeia/coleta-contraditoria/hash_fonte`, `cadeia/coleta-ausente/hash_fonte`,
  `cadeia/declaracao-contraditoria/<id>/<campo>`) e o OK correspondente cai (`rebaixar_ok` / novo `rebaixar_criterio`).
- `criterio["coleta"]["hash_fonte_confronto"]` passa a declarar `confere`/`contraditoria`/`ausente`/`sem-identidade`.

F2 — sanitizacao do CRITERIO:
- `montar_fila` agora faz `fonte.pop(campo)` quando a origem e o CRITERIO (antes so o item da fila era limpo),
  marca `crit["criterio_sanitizado"] = True` e mantem o registro em `propostas_nao_executadas` com `origem="criterio"`.
- docstring do modulo atualizada (item 3 e novo item 4).

## Provas desta rodada

- Suite: `python tools/automacao/kit12/test_kit12_integracao.py` -> **Ran 24 tests ... OK, exit 0**
  (6 testes novos: coleta contraditoria, coleta ausente, contra-prova OK com hash conferido, criterio com bytes antigos,
  campo executavel no criterio, campo executavel do avaliador ponta a ponta).
  Log: `scratch/kit/KIT-12F-run669-suite.txt`.
- Isca: 3 mutacoes novas (`coleta_contraditoria_ignorada`, `declaracao_do_criterio_sobrescrita`,
  `criterio_nao_sanitizado`) somadas as 6 originais.

Pendente neste bloco: isca completa, CLI em sandbox, travas do repo, relatorio final.
