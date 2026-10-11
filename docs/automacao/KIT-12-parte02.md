# KIT-12 — parte02: desenho da integracao (decisoes tomadas)

## 6. Levantamento do que JA existe (nao duplicar)

- `tools/automacao/ciclo/ciclo.py` (CIC-1, 1334 linhas): identidade `fonte_sha`/`dll_sha` dos
  bytes atuais, `confrontar_snapshot` do AUT-3, `montar_fila` (fila DECLARATIVA, `execucao_automatica:false`),
  `avaliar_tentativas` (numero/limite/sem-progresso), `avaliar_escalonamento` (destino supervisor
  tecnico), `avaliar_invalidacao`, `verificar_resultado` (fonte/DLL -> INVALIDADO), lock de area.
- `tools/automacao/ciclo/decisao.py` (CIC-2): `consolidar(criterios, identidade)` ->
  `por_mod/falhas_automaticas/pendencias_humanas/roteiro_humano/pronto_para_decisao`; exige
  `prova_runtime`+`sessao`+`fonte_sha`+`dll_sha`(+`config_sha` se `config_relevante`) para OK de runtime.
- `tools/automacao/aceite/relatorio_aceite.py` (AUT-7): `montar_relatorio` + `texto_do_relatorio` +
  `markdown_do_relatorio` (relatorio por mod, tecnico x humano x publicacao).
- `tools/automacao/kit10/kit10_cenarios.py`: `avaliar(observacoes, identidade)` -> criterios do
  contrato v1, com marca de fixture propagada fail-closed.
- `tools/automacao/kit11/executor.py`: frente unica, `CAMPOS_EXECUTAVEIS` (vocabulario de
  comando que NUNCA se executa a partir de dado).
- `tools/automacao/kit13/*`: pacote de cenario JSON (somente dado) + SDK C#.
- `tools/automacao/runtime/coletor.py` (CIC-5): coleta AUT-4, `consolidar_probe`, prova de atualidade.

NAO existe hoje: (a) mapa declarativo "mod/arquivo alterado -> cenarios pertinentes"; (b) costura
unica que leve identidade -> pertinencia -> coleta -> avaliadores -> relatorio -> fila do ciclo.

## 7. Decisoes de desenho (KIT-12)

Novo modulo `tools/automacao/kit12/` (nada existente e editado):

1. `pertinencia.json` — DADO declarativo: `mod -> {cenarios:[...], frentes:[...], criterios:[prefixos]}`.
   Mudar a pertinencia nao exige codigo.
2. `integracao.py` — a costura; REUSA (import por caminho) `ciclo.py`, `decisao.py`,
   `kit10_cenarios.py` e `relatorio_aceite.py`. Nao reimplementa avaliacao, fila, tentativas nem
   relatorio.
3. `test_kit12_integracao.py` — suite unittest (positivo + controles negativos).
4. `prove_ciclo.py` — demonstracao CLI em sandbox: fixture MARCADA -> defeito -> correcao
   controlada no sandbox -> revalidacao, sem fingir runtime.

Contrato da costura (`cadeia()` devolve dict):

- `identidade`: `fonte_sha`, `dll_sha`, `config_sha`, `versao`, `sessao` (a mesma identidade
  atravessa pertinencia, coleta, avaliadores, fila e relatorio).
- `pertinencia`: mods alterados -> cenarios/frentes; mod sem mapa ou arquivo alterado sem mod
  conhecido => LACUNA declarada (nunca verde).
- `coleta`: observacoes do probe/arquivo, com procedencia (`runtime` so com cadeia completa;
  fixture declarada permanece fixture).
- `criterios`: saida de `kit10.avaliar` filtrada pela pertinencia + criterios de lacuna.
- `decisao`: `decisao.consolidar(criterios, identidade)`; lacuna tecnica -> falha automatica
  (volta ao agente); humano so recebe autorizacao/julgamento residual.
- `fila`: declarativa, com `criterio/caminhos/prova/instrucao/tarefa_origem`,
  `execucao_automatica: false`. Guarda: qualquer campo executavel (`comando/argv/shell/exec/...`)
  proposto por agente/LLM e MOVIDO para `proposta_nao_executada` — nada e executado.
- `tentativas`: numero/limite/sem-progresso (reuso CIC-1) + escalonamento ao supervisor.
- `invalidacao`: comparacao de `fonte_sha`/`dll_sha`/`config_sha` contra rodada anterior guardada;
  mudanca invalida a aprovacao anterior.
- `relatorio`: `relatorio_aceite.montar_relatorio` + `texto_do_relatorio` (texto curto para humano).
- `estado`/`exit`: 0 sem falha automatica e sem pendencia offline · 1 com falha/escalonamento ·
  2 incompleto (inclui residual de runtime nao exercitado) · 3 invalidado por mudanca;
  FIXTURE nunca produz prova de runtime.

Determinismo: stdlib apenas, sem rede/IA; a cadeia nao imprime tempo relativo nem ordem
nao-deterministica (sem `set` na saida). Prova: duas execucoes com a mesma entrada geram o mesmo
JSON canonico (exceto o campo de tempo, excluido no comparativo).

Status: B2 concluido; implementacao (B3) a seguir.
