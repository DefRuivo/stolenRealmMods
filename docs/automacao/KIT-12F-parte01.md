# KIT-12 — correcao F1/F2 da revisao run668 (parte 01)

Cartao: t_0a434c97 (KIT-12 "Integrar alteracao, evidencia, correcao e revalidacao")
Autor: instancia implementadora (run669). Produto alvo: `tools/automacao/kit12/integracao.py`.
Base: entrega do run667 (sha integracao.py `f49a0d4059af33002ce52b463ad6be7091063ee6d661d746498072545c1a3599`).

## O que a revisao run668 pediu

F1 (BLOQUEANTE) — a procedencia declarada nao e confrontada e o hash declarado pelo criterio e SOBRESCRITO.
- Sonda S2: coleta com `hash_fonte = 0*64` contra `ident.fonte_sha = 256490c4...` -> APROVADO_OFFLINE / exit 0, sem marcacao; coleta SEM `hash_fonte` tambem aprovava.
- Sonda S8: criterio `estado=OK` declarando `fonte_sha`/`dll_sha` de bytes antigos -> cru o CIC-2 REPROVA; pela costura a declaracao era sobrescrita pela identidade -> APROVADO_OFFLINE / exit 0.
- Correcao exigida: confrontar `coleta_meta["hash_fonte"]` x `ident["fonte_sha"]` e o hash declarado pelo CRITERIO x identidade; na divergencia declarar lacuna/falha (rebaixar OK) em vez de sobrescrever; teste cobrindo os dois casos (a suite nao cobria nenhum).

F2 (ACIONAVEL) — campo executavel sobrevive no CRITERIO.
- `montar_fila` registrava o campo em `propostas_nao_executadas` mas NAO o removia do criterio; o criterio com `comando`/`argv`/`script_correcao` viajava em `resultado["criterios"]`, apesar da docstring prometer "MOVIDO".
- Correcao exigida: sanitizar o criterio tambem (mantendo o registro) ou declarar o limite, com teste que inspecione `criterios`.

F3/F4 seguem como divida registrada (nao bloqueiam).

## Plano deste bloco

1. `confrontar_coleta(coleta_meta, ident)` — divergencia/ausencia de `hash_fonte` => lacuna declarada + `rebaixar_ok` (fail-closed).
2. `confrontar_cadeia_declarada(criterios, ident)` — campo da cadeia declarado pelo criterio e diferente da identidade => lacuna nomeada + rebaixamento do criterio (declaracao preservada, nunca sobrescrita em silencio).
3. `montar_fila` — remover o campo executavel TAMBEM do criterio, marcando `criterio_sanitizado`.
4. Testes novos para os dois defeitos; isca e CLI reexecutadas; relatorio final.

Status: em andamento.
