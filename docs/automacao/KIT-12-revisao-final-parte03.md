# KIT-12 revisao rodada 2 (run670) — parte03: sondas proprias, travas e escopo

Sondas: `scratch/kit/KIT-12R-run670-rev/sondas_run670.py` (escrito por mim, nao importa a suite do
implementador; carrega o produto por caminho da COPIA ISOLADA).
Saida: `scratch/kit/KIT-12R-run670-rev/sondas-run670-saida.txt` -> `SONDAS_OK|6`, exit 0.
JSON: `scratch/kit/KIT-12R-run670-rev/sondas-run670.json`.

## F2 — campo executavel nao sobrevive (S1 e S1b)

    SONDA|S1-campo-executavel-no-criterio|{"campos_residuais_no_criterio": [],
      "criterio_sanitizado": true, "propostas": 3, "campos_executaveis_no_item": [],
      "execucao_automatica": false}
    SONDA|S1b-cadeia-inteira-sem-campo-executavel|{"culpados": [],
      "sanitizados": ["offline/sujo"], "propostas_registradas": 2}

S1: criterio com `comando`/`argv`/`script_correcao` -> o criterio sai LIMPO, marcado
`criterio_sanitizado=true`, as 3 propostas ficam em `propostas_nao_executadas`, o item da fila nao
tem campo executavel e `execucao_automatica=false`.
S1b: pelo caminho COMPLETO `cadeia()`, varri `resultado["criterios"]` E `resultado["fila_correcao"]`
contra `CAMPOS_EXECUTAVEIS` -> `culpados=[]`. (Na rodada 1 o criterio mantinha os residuais.)
VEREDITO F2: PASSOU.

## F1 — procedencia confrontada, fail-closed (S2a/S2b/S8/S9)

    SONDA|S2-hash-de-outros-bytes|{"estado": "INCOMPLETO", "exit": 2, "OK": 0, "prova_runtime": 0,
      "lacuna_presente": true, "lacunas": ["cadeia/coleta-contraditoria/hash_fonte"],
      "criterio_estado_final": "NAO_EXERCITADO", "hash_fonte_confronto": "contraditoria"}
    SONDA|S2-hash-ausente|{"estado": "INCOMPLETO", "exit": 2, "OK": 0, "prova_runtime": 0,
      "lacuna_presente": true, "lacunas": ["cadeia/coleta-ausente/hash_fonte"],
      "criterio_estado_final": "NAO_EXERCITADO", "hash_fonte_confronto": "ausente"}

S2a: coleta declarando `hash_fonte=0*64` contra a identidade `8f3eee4ac1ec3a71…` (medida por mim na
propria rodada). Rodada 1 (run668) media **APROVADO_OFFLINE / exit 0 / OK=1** neste mesmo cenario;
agora e **INCOMPLETO / exit 2 / OK=0**, com a lacuna nomeada `cadeia/coleta-contraditoria/hash_fonte`
e o criterio rebaixado a NAO_EXERCITADO.
S2b: coleta SEM `hash_fonte` -> mesma trava (`cadeia/coleta-ausente/hash_fonte`), fail-closed.
O valor estaleiro NAO e mais o unico vestigio: a contradicao entra em `criterios` e em
`criterio["coleta"]["hash_fonte_confronto"] = "contraditoria"` / `"ausente"`.

    SONDA|S8-criterio-declara-bytes-antigos|{"cru_severidade": ["REPROVADO"],
      "cru_motivo": ["hash fonte_sha refere bytes antigos/errados: aprovacao anter"],
      "costura_estado": "INCOMPLETO", "costura_exit": 2,
      "costura_criterio_estado": "NAO_EXERCITADO",
      "declaracoes_contraditorias": [{"criterio": "offline/hash-antigo", "campo": "fonte_sha",
        "declarado": "deaddead…", "identidade": "8f3eee4ac1ec3a71…"}, {... "campo": "dll_sha" ...}],
      "declaracao_sobrescrita": true, "lacunas": ["cadeia/declaracao-contraditoria/…"], "OK": 0}

S8: o mesmo criterio `estado=OK` declarando `fonte_sha`/`dll_sha` de bytes antigos tem os dois
caminhos coerentes agora:
 (a) CRU: o CIC-2 emite `REPROVADO` ("hash fonte_sha refere bytes antigos/errados") — esperado;
 (b) pela COSTURA (que na rodada 1 dava `falhas_automaticas=0` -> `APROVADO_OFFLINE`/exit 0):
     agora `INCOMPLETO`/exit 2, o criterio fica `NAO_EXERCITADO`, a declaracao NAO e perdida
     (`declaracoes_contraditorias` preserva `dead*64` e a identidade real campo a campo) e a lacuna
     `cadeia/declaracao-contraditoria/offline/hash-antigo/{fonte_sha,dll_sha}` e declarada.

CONTRA-PROVA (exigida pelo proprio handoff, item 4): a correcao nao virou trava cega —

    SONDA|S9-contra-prova-coleta-confere|{"hash_declarado": "8f3eee4ac1ec3a71…",
      "estado": "APROVADO_OFFLINE", "exit": 0, "OK": 1, "hash_fonte_confronto": "confere",
      "lacunas_cadeia": [], "criterio_estado": "OK"}

Coleta declarando o hash DA PROPRIA RODADA -> nenhuma lacuna de cadeia, `hash_fonte_confronto=confere`
e o OK offline SOBREVIVE (APROVADO_OFFLINE/exit 0). A trava e seletiva, nao um carimbo vermelho.
VEREDITO F1 (a/b/c + contra-prova): PASSOU.

## Aceite do cartao, conferido por leitura do estado resultante (nao por mensagem)

- hash/versao/config/sessao atravessam a cadeia: `identidade` = {fonte_sha, dll_sha, config_sha,
  versao 1.0.2, sessao, cadeia_sha}; os 6 campos estao presentes e iguais em cada criterio
  (`criterios[*]`); o item da fila carrega `cadeia_sha`.
- mudanca invalida aprovacao anterior: etapa 4 da CLI -> exit 3 (INVALIDADO) apos mudar a config;
  `tentativas` traz `invalidou_anterior`/`motivo_invalidacao`.
- fila declarativa com paths/criterio/prova: item medido =
  `{criterio: KIT-10/atributos/base-vs-final/Attributes_Text, roteamento: causa,
    causa: BetterStats/Plugin.cs, caminhos: [...], prova: [coleta…, BetterStats/Plugin.cs],
    execucao_automatica: false, quem_executa: agente}`.
- limite de tentativas / sem progresso: `tentativas = {numero, limite: 5, sem_progresso,
  sem_progresso_seguidas, sem_progresso_motivo}` no resultado.
- validacao/relatorio deterministas sem IA permanente: `relatorio` (dict) + `relatorio_texto`
  ("AUT-7 - RELATORIO DE ACEITE POR MOD (DoD)") gerados pelo `relatorio_aceite.py` reusado; os
  `limites` declarados no proprio resultado incluem "a fila e DECLARATIVA: nao ha caminho de
  execucao de comando neste modulo".
- lacuna tecnica volta ao agente, humano so residual: `pendencias_humanas` = 1 item com
  `tipo=julgamento_visual` (aceite visual), `propostas_nao_executadas=[]`.

## T1 — travas do repo

    python tools/check_segredos.py          -> exit 0  "nenhum padrao de credencial encontrado"
    python tools/check_padroes_segredo.py   -> exit 0  "nenhum padrao de credencial encontrado"
    python tools/check_dupes.py             -> exit 0  "TextFixes 101 | duplicadas: nenhuma"
    python tools/audita_docs.py             -> exit 0  "nenhuma inconsistencia encontrada"
    Logs: scratch/kit/KIT-12R-run670-rev/<trava>-run670.txt

## Escopo — nada fora de F1/F2 foi tocado

Varredura de mtime de todo o repo (excluindo .git/__pycache__/bin/obj/scratch) para arquivos
modificados DEPOIS da rodada 1 (00:40): apenas

    00:43:19 tools/automacao/kit12/integracao.py
    00:43:51 tools/automacao/kit12/test_kit12_integracao.py
    00:46:44 tools/automacao/kit12/prove_ciclo.py
    (+ docs/automacao/KIT-12F-parte01..03.md e KIT-12F-entrega.md)

`pertinencia.json` permanece com mtime 00:18 (inalterado, hash identico ao da rodada 1).
Nenhum outro arquivo de produto, mod, csproj, patch ou trava foi modificado. `git rev-parse HEAD`
= d82894e95d97f26b7989a848372c691dcb8ef6 (inalterado); nao houve git add/commit/push.
