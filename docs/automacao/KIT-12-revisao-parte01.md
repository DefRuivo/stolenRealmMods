# KIT-12 — Revisao independente (run668)

Tarefa: t_0a434c97 — "KIT-12: Integrar alteracao, evidencia, correcao e revalidacao".
Revisor: default run668 (instancia nova; != implementador run667; != revisores dos pais run648/run653/run658/run660/run663/run666).
Lente desta rodada: **Artifact** (rodada 1: 0 `changes_requested` no historico) — leitura fria do entregavel ANTES do resumo do implementador; depois confronto com o handoff.

## 1. Identidade do que foi lido (hash conferido contra o handoff)

| arquivo | sha256 | bytes | handoff |
|---|---|---|---|
| tools/automacao/kit12/integracao.py | f49a0d4059af33002ce52b463ad6be7091063ee6d661d746498072545c1a3599 | 42987 | confere |
| tools/automacao/kit12/pertinencia.json | b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320 | 1956 | confere |
| tools/automacao/kit12/test_kit12_integracao.py | c57ad7980754ab53c2bbc18368ced23acda0bf6b6649a35d4bf8955814870b77 | 26678 | confere |
| tools/automacao/kit12/prove_ciclo.py | 1748f7c5da3180540f18562d99ab72004839ed04e1581bb9abbb03912175e64b | 10411 | confere |
| scratch/kit/KIT-12-run667/prova.json | 8a6f165c3225a2e9469be6d22047165c75aac376f9219b96bb8a22f1f5ca9bc4 | 9791 | confere |
| docs/automacao/KIT-12-entrega.md | 39cdbf86a66f1701db959f77cbec316db9055cc7e4b1db095a94c6c5b951d4f6 | 12029 | (nao declarado no handoff) |

Escopo `?? tools/automacao/kit12/` + `?? docs/automacao/KIT-12-entrega.md` (untracked); HEAD d82894e intacto.

## 2. Leitura fria do produto (integracao.py, 952 linhas) — julgamento proprio

O modulo e uma COSTURA: importa por caminho ciclo.py (CIC-1), decisao.py (CIC-2), kit10_cenarios.py e relatorio_aceite.py; nao reimplementa avaliador/fila/relatorio. Sem rede, sem IA, stdlib. Estrutura:

1. pertinencia (mapa declarativo + arquivos sem mapa -> lacuna)
2. identidade unica (fonte_sha/dll_sha/config_sha/versao/sessao -> cadeia_sha)
3. coleta (envelope/lista; fixture propagada fail-closed)
4. criterios (avaliador real + lacunas + filtro de pertinencia + normalizacao de declaracao incoerente)
5. fila declarativa (reuso CIC-1 + sanitizacao de campo executavel)
6. invalidacao da aprovacao anterior (fonte/dll/config/versao)
7. estado/exit (OK=0, REPROVADO/ESCALADO=1, INCOMPLETO=2, INVALIDADO=3)
8. relatorio (AUT-7)

### Refutacoes que vou tentar (lente Artifact, hipoteses da leitura fria)

- **R1 (fila)** — em `montar_fila`, `item.pop(campo) if campo in item else fonte.get(campo)`: se o campo executavel estiver no CRITERIO (nao no item), ele e registrado em `propostas_nao_executadas` mas NAO e removido do criterio (o `crit` continua com o campo, e o criterio viaja inteiro no resultado). Se confirmado, "qualquer campo executavel ... e MOVIDO" e verdadeiro para a fila e FALSO para a origem criterio.
- **R2 (normalizar_declaracoes)** — rebaixa criterio com `classe=runtime`/`procedencia=execucao` para NAO_EXERCITADO. Se um criterio REPROVADO real caisse nesse par, ele viraria lacuna (exit 2 em vez de 1). Preciso ver se o par e alcancavel por entrada REAL do avaliador e se a regra vem mesmo do CIC-2.
- **R3 (filtro de pertinencia)** — criterio de mod CONHECIDO e nao selecionado sai de `criterios`; so sobrevive em `fora_da_pertinencia`. Conferir que o criterio transversal e o de mod desconhecido nunca somem.
- **R4 (invalidacao)** — `verificar` sem `--config` produz config_sha None vs hash guardado: fail-closed ou falso INVALIDADO? Conferir direcao do erro.
- **R5 (avaliacao vazia)** — `classificar_estado` com 0 criterios = INCOMPLETO/2 (nao 0). Exercitar.
- **R6 (fixture)** — fixture marcada nunca vira OK: reproduzir com observacao de mod pertinente e identidade completa.

## 3. Status

- [x] hashes conferidos
- [x] leitura fria do produto
- [ ] leitura dirigida do pertinencia.json / suite / prove_ciclo
- [ ] execucao propria: suite do autor, isca, CLI em sandbox propria
- [ ] sondas adversariais proprias R1-R6
- [ ] veredito por criterio
