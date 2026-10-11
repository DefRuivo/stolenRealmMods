# KIT-12 — Revisao independente (run668) — parte 03

## 6. Travas do repo (executadas por mim no escopo novo)

    python tools/check_segredos.py        exit=0
    python tools/check_padroes_segredo.py exit=0
    python tools/check_dupes.py           exit=0
    python tools/audita_docs.py           exit=0   ("nenhuma inconsistencia encontrada")

Logs: scratch/kit/KIT-12R-run668-rev/{check_segredos,check_padroes_segredo,check_dupes,audita_docs}.txt

## 7. Sondas adversariais proprias (fora da suite do implementador)

Script: scratch/kit/KIT-12R-run668-rev/sondas_run668.py (sandbox propria, avaliador INJETADO; saida JSON em sondas-run668.json).

| sonda | medicao | resultado |
|---|---|---|
| S1 | campo executavel no CRITERIO (`comando`/`argv`/`script_correcao`) | **ACHADO**: os 3 campos PERMANECEM no criterio; sao apenas *registrados* em `propostas_nao_executadas` (origem `criterio`). O item da fila fica limpo. Contrato docstring: "campo executavel ... e MOVIDO para propostas_nao_executadas" — vale para a fila, NAO para o criterio. |
| S2 | coleta declarando `hash_fonte` CONTRADITORIO (0*64 vs fonte_sha da rodada 256490c4…) | **ACHADO**: estado APROVADO_OFFLINE / exit 0 com **zero** criterios ou falhas apontando a contradicao; `criterio["coleta"]["hash_fonte"]` carrega o valor estaleiro sem confronto. Sem `hash_fonte` nenhum tambem aprova. |
| S3 | `--verificar` sem `--config` | valido=false exit 3 (fail-closed; motivo "config mudou ... agora=None"); com config valido=true exit 0. Sem falso verde. |
| S4 | `--verificar` apos mudar FONTE e apos mudar DLL | fonte mudada -> exit 3 "fonte mudou"; DLL mudada -> exit 3. Invalida de fato (nao so a mensagem). |
| S5 | criterio REPROVADO com classe runtime/procedencia execucao (incoerente) | vira NAO_EXERCITADO -> INCOMPLETO/exit 2; original preservado (True). Fail-closed (nunca verde), mas um vermelho real cairia para lacuna. Direcao registrada, sem pedido de correcao obrigatorio. |
| S6 | criterio transversal e de mod desconhecido | ambos sobrevivem na avaliacao; nada some em silencio. |
| S7 | avaliacao vazia | INCOMPLETO / exit 2 (nunca aprova). |

Detalhe S2 (valores lidos do resultado, nao da mensagem):

    coleta_hash_declarado      = 0000...0000 (64 zeros)
    fonte_sha_da_rodada        = 256490c4686aa5fed6433862b938d7e46becac3376ef66e0c8e5f82d1b872aaf
    declarado_bate_com_a_rodada= false
    criterios_que_apontam_contradicao = []
    estado/exit                = APROVADO_OFFLINE / 0

Base do mecanismo: `decisao.py` (CIC-2) CONFRONTA hash declarado pelo criterio com a identidade
("hash X refere bytes antigos/errados: aprovacao anterior invalidada"), mas a costura
`anexar_cadeia` SOBRESCREVE `fonte_sha`/`dll_sha`/`sessao` do criterio com os da rodada
(`integracao.py:428-442`) e o `hash_fonte` declarado pelo ENVELOPE da coleta nunca e confrontado
com `ident["fonte_sha"]`. Sonda S8 mede esse contraste.

## 8. Status

- [x] travas do repo exit 0
- [x] sondas S1-S7 medidas por execucao propria
- [ ] sonda S8 (criterio declarando bytes antigos: cru vs costura)
- [ ] veredito por criterio + parecer final
