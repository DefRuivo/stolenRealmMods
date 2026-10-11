# KIT-12 — Revisao independente (run668) — PARECER FINAL

- Tarefa: t_0a434c97 — "KIT-12: Integrar alteracao, evidencia, correcao e revalidacao"
- Revisor: default run668 — instancia nova, nao e o implementador (run667) nem os revisores dos pais.
- Rodada: 1 (0 `changes_requested` no historico) — lente **Artifact**, reforcada por execucao propria.
- Produto: tools/automacao/kit12/ (integracao.py, pertinencia.json, test_kit12_integracao.py, prove_ciclo.py)
- Veredito: **REPROVADO — requer correcao (2 achados acionaveis: F1 e F2)**. Nada foi publicado, instalado, aberto em jogo ou commitado.

## 1. Identidade conferida

| arquivo | sha256 (conferido pos-execucao) |
|---|---|
| tools/automacao/kit12/integracao.py | f49a0d4059af33002ce52b463ad6be7091063ee6d661d746498072545c1a3599 |
| tools/automacao/kit12/pertinencia.json | b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320 |
| tools/automacao/kit12/test_kit12_integracao.py | c57ad7980754ab53c2bbc18368ced23acda0bf6b6649a35d4bf8955814870b77 |
| tools/automacao/kit12/prove_ciclo.py | 1748f7c5da3180540f18562d99ab72004839ed04e1581bb9abbb03912175e64b |
| docs/automacao/KIT-12-entrega.md | 39cdbf86a66f1701db959f77cbec316db9055cc7e4b1db095a94c6c5b951d4f6 |

Os 5 hashes do handoff batem; os 4 produtos permanecem byte-identicos APOS todas as minhas execucoes (nenhum arquivo de implementacao foi editado pelo revisor). HEAD d82894e intacto; nenhum `git add/commit/push`; nenhum mod tocado (`git status`: so `?? tools/automacao/kit12/`).

## 2. O que eu reproduzi por execucao propria (e confere)

| prova | comando | resultado medido |
|---|---|---|
| suite do autor | `python tools/automacao/kit12/test_kit12_integracao.py` | `Ran 18 tests` `OK` exit 0 |
| isca (mutacao seletiva real) | `... --isca` | 6/6 mutantes derrubam o teste nomeado; controle restaurado exit 0 |
| CLI em sandbox com fixture marcada | `python tools/automacao/kit12/prove_ciclo.py --out scratch/kit/KIT-12R-run668-rev` | exits 2 -> 1 -> 2 -> 3, `PROVA|PASSOU`, exit 0; `com_prova_runtime=0` |
| travas do repo | check_segredos / check_padroes_segredo / check_dupes / audita_docs | exit 0 cada |

Logs: scratch/kit/KIT-12R-run668-rev/{suite-entrega,isca-entrega,prove-saida,...}.txt; sondas em sondas-run668.json e sonda-s8.json.

Tambem confere: avaliacao vazia -> INCOMPLETO/2; `--verificar` sem `--config` fail-closed (exit 3); mudanca de FONTE e de DLL invalidam de fato (exit 3, motivo lido do arquivo); criterio transversal/desconhecido nunca some; fixture marcada nunca vira OK.

## 3. ACHADOS

### F1 (bloqueante) — procedencia declarada NAO e confrontada; a costura SOBRESCREVE o hash declarado pelo criterio

Onde: `integracao.py` `anexar_cadeia` (l.428-442) e `criterios_da_cadeia` (l.508-606, uso de `coleta_meta["hash_fonte"]` em l.590-591).

Como reproduzir (sondas proprias, fora da suite do autor):

1. **S2** — coleta cujo envelope declara `hash_fonte = 0*64` enquanto `ident["fonte_sha"] = 256490c4686aa5fe…`:
   estado `APROVADO_OFFLINE`, exit 0, `criterios_resumo.OK = 1`, e **nenhum** criterio/falha apontando
   a contradicao (`criterios_que_apontam_contradicao = []`); o valor estaleiro fica apenas em
   `criterio["coleta"]["hash_fonte"]`. Sem `hash_fonte` nenhum, tambem aprova.
2. **S8** — o mesmo criterio (`estado=OK`, evidencia real) declarando `fonte_sha`/`dll_sha` de bytes
   ANTIGOS:
   - **cru** -> `decisao.consolidar` emite `falhas_automaticas=1`, `severidade=REPROVADO`,
     motivo "hash fonte_sha refere bytes antigos/errados: aprovacao anterior invalidada" (regra do CIC-2);
   - **pela costura** -> `anexar_cadeia` SOBRESCREVE `fonte_sha`/`dll_sha` do criterio com os da rodada
     (`declaracao_sobrescrita=true`; criterio passa a `2c85716cda90…`): `decisao` -> `falhas_automaticas=0`;
   - **caminho completo** `cadeia()` -> `APROVADO_OFFLINE` / exit 0, com `coleta.hash_fonte` ainda
     contradizendo a rodada.

Por que viola a tarefa: o aceite exige "Hash/versao/config/sessao atravessam toda cadeia; mudanca invalida
aprovacao anterior" e "Evidencia identifica sessao, ... hash DLL/fonte/config quando pertinente". A
propagacao existe, mas no ponto coleta/criterio -> decisao a declaracao divergente e normalizada em
silencio: um resultado que declara bytes DIFERENTES dos atuais chega a APROVADO_OFFLINE/exit 0. E
exatamente a classe de falso verde que o CIC-2 ja rejeita quando o criterio nao e reescrito.

Correcao minima esperada: confrontar a procedencia declarada com a identidade da rodada
(`coleta_meta["hash_fonte"]` x `ident["fonte_sha"]`; hash declarado pelo criterio x identidade) e, na
divergencia, declarar lacuna/falha (rebaixar OK) em vez de sobrescrever a declaracao; cobrir com teste
que olhe o criterio e a coleta contraditoria (a suite atual nao cobre nenhum dos dois).

### F2 (acionavel) — campo executavel permanece no CRITERIO (a fila e sanitizada, o criterio nao)

Onde: `integracao.py` `montar_fila` (l.613-646). Em `item.pop(campo) if campo in item else fonte.get(campo)`,
quando o campo vem do CRITERIO ele e **registrado** em `propostas_nao_executadas` (origem `criterio`) mas
**nao e removido do criterio**.

Prova: sonda S1 — criterio com `comando`, `argv`, `script_correcao` -> `campos_residuais_no_criterio =
["argv","comando","script_correcao"]` enquanto o item da fila fica limpo. O criterio (com o campo
executavel) viaja inteiro em `resultado["criterios"]` e alimenta a decisao/relatorio. O contrato do
proprio modulo (docstring l.30-33: "qualquer campo executavel ... e MOVIDO para propostas_nao_executadas")
vale para a fila, nao para o criterio; o teste do autor afirma apenas `assertNotIn(campo, item)`.

Correcao minima esperada: sanitizar tambem o criterio (remover/anonimizar o campo no criterio, mantendo o
registro em `propostas_nao_executadas`) ou declarar explicitamente o limite; teste que inspecione
`criterios`, nao so a fila.

### F3 (observacao registrada, NAO bloqueante)

Criterio `REPROVADO` com par classe/procedencia incoerente (p. ex. `classe=runtime` + `procedencia=execucao`)
e rebaixado a `NAO_EXERCITADO` -> INCOMPLETO/exit 2 (sonda S5), com o original preservado em
`declaracoes_incoerentes`. Direcao fail-closed (nunca vira verde, nada e apagado), mas um vermelho real
declarado nesse par deixa de ser vermelho. Registrado para quem for endurecer o AUT-7; nao pede correcao
nesta rodada.

### F4 (observacao registrada, NAO bloqueante)

`--verificar` sem o mesmo conjunto de `--config` da rodada gera exit 3 mesmo sem nenhuma mudanca real
(motivo "config mudou ... agora=None", sonda S3). Fail-closed (nao ha falso verde), mas a CLI produz um
falso INVALIDADO se o operador esquecer o `--config`; documentar no `KIT-12-entrega.md` ou aceitar um
manifesto de configs no proprio resultado.

## 4. Verificacao do que o handoff pediu para refutar

| pedido | resultado |
|---|---|
| fixture marcada virando verde | NAO refutado: fixture nunca vira OK (suite + prova + sonda) |
| fila executando campo de comando | NAO refutado quanto a execucao (nenhum `subprocess` roda item de fila; o item sai limpo) — mas o campo sobrevive no CRITERIO (**F2**) |
| invalidacao ignorada (fonte/DLL/config/versao) | NAO refutado no eixo `--verificar` (S3/S4) — **porem** a procedencia declarada pela coleta/criterio nao e confrontada (**F1**) |
| criterio transversal sumindo na filtragem | NAO refutado (S6) |
| avaliacao vazia aprovando | NAO refutado (S7) |

## 5. Limites desta revisao

Runtime real, jogo, probe, save, perfil do dono, UI/UX, build C#, pre-flight de deploy, instalacao,
publicacao, aceite humano e DoD: **NAO_EXERCITADO**. Fixture nao comprova runtime. Aprovar/reprovar
tecnicamente aqui NAO e aceite humano nem publicacao. Nenhum arquivo de implementacao foi editado pelo
revisor (separacao de papeis preservada); nenhuma dependencia compartilhada alterada; nenhum `git add`.

## 6. Passo seguinte

Implementador (mesma familia de autoria, nova rodada): tratar F1 e F2, reexecutar suite + isca + prova de
CLI e registrar no artefato novo; `kanban_request_review` novamente. F3/F4 ficam registrados como divida.
