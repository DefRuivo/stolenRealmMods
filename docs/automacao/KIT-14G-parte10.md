# KIT-14G — parte 10: correção dos 3 defeitos de EVIDÊNCIA da revisão run715

Rodada: **run716** (implementador `default/run716`). Responde à revisão **run715**
(rodada 2, lente EXECUTION) = CHANGES REQUESTED com escopo curto: **correções de evidência e
rotulagem**, não de produto.

Produto **intocado** nesta rodada: `AUT4ProbePlugin.cs` = `594c8add…`, `bin/Release/AUT4Probe.dll`
= `1d496dbc…` (nenhuma das 3 correções abaixo exige rebuild — o revisor dispensou explicitamente).

Estado por máquina desta rodada: `scratch/kit/KIT-14G-run716/verification.json`
(sha256 **`9a684d6f3dcce43cca46527c769e0b378bdc3a4cb3901106a1ceb15d3d15b1bc`**), gerado por
`scratch/kit/KIT-14G-run716/gera_verification.py` a partir dos artefatos
**medidos** (nada digitado à mão — as contagens de teste são lidas do próprio log).

O `verification.json` do run714 **não foi sobrescrito** (regra de artefato incremental): ele fica
como histórico, e o campo `supersedes` do novo arquivo aponta para ele e para o motivo.

---

## Correção 1 — `eventlog_run714` era rótulo FALSO (cumulativo/truncado passando por janela)

**Defeito medido (revisor run715):** o campo `eventlog_run714` do
`scratch/kit/KIT-14G-run714/verification.json` tinha **26 entradas** e atribuía crash a boots que
**VIVERAM** — `C-sem-nada` (6), `D-probe-play` (4), `E-sem-navegar` (3) — todas com hora
**anterior** ao início do boot e algumas delas são crashes do **run712**.

**Causa no código:** `scratch/kit/KIT-14G-run714/gera_verification.py:78`, função
`eventlog_janela(minutos, prefixo)`, **ignora os dois parâmetros** e apenas concatena todos os
arquivos `*-eventlog.json`. E esses exports são listas **“N mais recentes”** no instante do export
(A=6, B=7, C=6, D=4, E=3 = 26): **cumulativos e truncados**, nunca janelas do boot.

**Correção aplicada (duas partes):**

1. **Campo agregado agora é FILTRADO pela janela real de cada boot** — mesmo critério de
   `_janela()`: `result.json.cloud_start.measured_at` … `cloud_end_before_restore.measured_at`.
   Campo novo: `eventlog_crash_na_janela_do_boot_agregado`.

   Resultado medido agora: **n = 2** entradas — `A-sem-passivo` às **19:36:18** e `B-semeado` às
   **19:37:56** — e **vazio** para `C`/`D`/`E` (que viveram). Bate **exatamente** com a leitura
   independente do revisor no run715 (A 19:36:18, B 19:37:56; zero nas janelas de C/D/E).

2. **O bruto foi preservado, mas RENOMEADO e DECLARADO** — campo
   `exports_eventlog_por_boot_acumulados`, com `n_total = 26` e, por boot, a declaração
   “export *N mais recentes* … **CUMULATIVO e TRUNCADO**; inclui crashes anteriores ao boot;
   **NÃO é a janela do boot**”, e cada entrada marcada com `antes_do_boot: true/false`.

Prova colhida no estado por máquina:

```
eventlog_crash_na_janela_do_boot_agregado.n = 2   boots = [A-sem-passivo, B-semeado]
ab_causa_do_encerramento.C_sem_nada.eventlog_crash_na_janela_do_boot = []
ab_causa_do_encerramento.D_probe_play.eventlog_crash_na_janela_do_boot = []
ab_causa_do_encerramento.E_sem_navegar.eventlog_crash_na_janela_do_boot = []
exports_eventlog_por_boot_acumulados.n_total = 26  (declarado cumulativo/truncado)
```

É o mesmo tipo de defeito que o item 4 da rodada 1 (run713) mandou corrigir, ainda presente no
artefato canônico — agora fechado. O campo sério ao lado
(`ab_causa_do_encerramento.*.eventlog_crash_na_janela_do_boot`) já estava certo e foi mantido.

---

## Correção 2 — `testes_executados: []` e logs ausentes

**Defeito:** o `verification.json` do run714 deixava `testes_executados` **vazio**
(`gera_verification.py:166`) apesar do handoff afirmar 7 comandos; e em `scratch/kit/KIT-14G-run714/`
**não existiam** os logs da suite 16/16 nem da contra-prova 33/33 (só o harness + 4 travas).

**Correção:** nova bancada `scratch/kit/KIT-14G-run716/roda_travas.py` roda **os 7 comandos**,
grava `logs-<nome>.log` e `exit-codes.json` (do retorno real do processo), e
`gera_verification.py` **lê a contagem do próprio log**. O campo `testes_executados` passa a ter
comando + log + contagem + exit por teste:

| comando | contagem (lida do log) | exit |
|---|---|---|
| `dotnet run --project tools/automacao/runtime/harness-passivo -c Release` | 29 OK / 0 FALHA | 0 |
| `python tools/automacao/runtime/roda_testes_runtime.py` | 16 testes — VERDE | 0 |
| `python tools/automacao/runtime/roda_testes_runtime.py --contra-prova` | 33 testes — VERDE | 0 |
| `python tools/check_segredos.py` | — | 0 |
| `python tools/check_padroes_segredo.py` | — | 0 |
| `python tools/check_dupes.py` | — | 0 |
| `python tools/audita_docs.py` | — | 0 |

Logs (agora existem, nesta rodada):
`scratch/kit/KIT-14G-run716/logs-{harness-passivo,suite-runtime,contra-prova,check_segredos,check_padroes_segredo,check_dupes,audita_docs}.log`
mais `exit-codes.json`.

---

## Correção 3 — `classificacao` afirmava mais do que a medição

**Defeito:** a `classificacao` do run714 dizia *“DEFEITO CORRIGIVEL do caminho de clique do
instrumento; NAO e limitacao de ambiente”* — mais forte que o medido. O revisor lembrou que o
mecanismo do `c0000005` **não** foi isolado e que `B-semeado` morreu **com o dado real do dono**
dentro, o que é igualmente compatível com “não dá para iniciar run neste arranjo isolado”
(hipótese (ii) do `KIT-14G-parte08.md §5`, ainda viva).

**Correção (só a linha; nenhuma medição do A/B foi alterada):**

> **GATILHO MEDIDO** = chegar ao estágio do clique `Accept` mata o processo.
> **MECÂNICA NÃO ISOLADA**: onde o `c0000005` nasce continua aberto (hipótese (ii) segue viva).
> **DISCRIMINADOR PENDENTE**: o clique **FÍSICO** (etapa visual do dono, KIT-14).
> Não se afirma “defeito do instrumento” nem “limitação de ambiente”.

O campo traz também `o_que_esta_medido_e_o_que_nao`:
**medido** = todos os boots que clicaram até `Accept` morreram; `E` (Navegar=false) e `D` (sem
`Accept`) viveram ~122 s; assinatura do SO `ntdll.dll / 0xc0000005 / 0x4a612` nos que morreram,
zero nos que viveram. **não medido** = a instrução exata do `c0000005`; se a morte é do instrumento,
do jogo no isolado, ou de ambos.

---

## O que NÃO foi exercitado (inalterado, e nenhum número inventado)

HUD da run / botão do RSTV; `recorder.eventos_total > 0`; clique físico / aceite UI‑UX (dono);
Runner positivo/negativo; RSTV sem kit; **FPS/frame/IO** (limiares dispensados pelo dono — nenhum
número medido ou inventado); ponto exato do `c0000005` dentro do caminho de clique.
Itens 1–2 do escopo seguem **NAO_EXERCITADO no runtime** pelo gatilho medido acima; o item 3 do
escopo (recoleta após navegar) está OK no mecanismo desde o run712.

## Ambiente ao fim desta rodada (medido)

Dados do dono **111/111 byte a byte** (`production_diff().equal = True`), **sem junction**,
**0 processos** “Stolen Realm”, perfil sem `plugins/AUT4Probe` e sem `plugins/KitPassive`,
**Cloud do app 1330000 segue OFF** (a janela do dono também cobre a etapa visual; só pedir
religação quando a janela inteira terminar). Sem commit, sem deploy, sem publicação — a rodada é
só de evidência/rotulagem.
