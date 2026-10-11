# KIT-05F — ENTREGA: correção dos achados F1–F9 (KIT-05R) + integração da trilha passiva

Cartão `t_467952ea` · perfil `default` · implementer **run 631** (≠ autor 629, ≠ reviewer 630)
Data 2026-10-09 · **offline**: sem jogo, sem save, sem instalar/deploy/publicar.

## 0. Veredito por achado

| Achado (KIT-05R) | Situação | Prova principal (execução real) |
|---|---|---|
| F1 captura sem efeito | **CORRIGIDO** | pedido ≠ confirmação; confirmação exige PNG real + quadro posterior + hash (`test_confirmacao_*`) |
| F2 pausa parcial | **CORRIGIDO** | pausa barra captura/confirmação/timeout e invalida pendência com lacuna (`test_pausa_*`) |
| F3 dedup global/spam | **CORRIGIDO** | estado por fonte; A/B coexistem; abrir→fechar→reabrir sobrevive |
| F4 limites ausentes | **CORRIGIDO** | `limite_aux` em TODO estado auxiliar + contadores agregados (3000 entradas) |
| F5 janela tardia | **CORRIGIDO** | só resolve dentro do prazo; vencimento materializado antes da abertura |
| F6 replay/export | **CORRIGIDO** | `_correr_entradas` = estado retido; CLI rotulado fixture/offline |
| F7 runner sem `.git` | **CORRIGIDO** | layout + `PYTHON` + exit 0/1/2; sandbox sem `.git`: novo=0, antigo=2 |
| F8 integração ausente | **CORRIGIDO (offline)** | `PipelinePassivo.cs` + `PontePassivaRSTV.cs` ligados no `CorePlugin`/`SRAdapterPlugin`, opt-in `false`; harness offline 29/29; build isolado 0 erros |
| F9 falso verde do oráculo | **CORRIGIDO** | discriminador estrito + controle adversarial recusado; 37 testes reprovando individualmente |

## 1. Arquivos entregues (com SHA256 medidos por `sha256sum`)

```
63124b86ccea6a5b46494836f41c0d48011987c4aaaf2fa5261a84f757e1b869  tools/automacao/runtime/observacao_passiva.py
454823e60043646177fd2aab14ade36c457c3636d2aa93606c5187fcb73eb638  tools/automacao/kit05/teste_observacao_passiva.py
dbda5bc626a4c1d625db7fe86752c7565283f50f7cdd5022385a702c4357829d  tools/automacao/kit05/contra_prova_kit05.py
380e41b89e1347db5852fcab2953b1268383e8ec72d7cdd80bfec6cf2d62778c  tools/automacao/kit05/roda_testes_kit05.sh
8aec5b8aaaf5da39035864cf1d850a10536c00c51a6e16032167eae62eaed10c  tools/automacao/runtime/KIT04Core/PipelinePassivo.cs
77e2d1cb31cf83d471f47c0d6b20d1f337ebcaca103b9775b25144b622095234  tools/automacao/runtime/KIT04Core/CorePlugin.cs
0fd696e62144203580ed4187887f57c7d9ccd90a9b886fe0e10b10d65c404e65  tools/automacao/runtime/KIT04Adapter.SR/PontePassivaRSTV.cs
5029329e960449239bcf8986512b60234c933498644f3b10198b1c840b9647e2  tools/automacao/runtime/KIT04Adapter.SR/SRAdapterPlugin.cs
8c0d7b3dde8480c43687e01cd61380a13c9aa1fc610aa1aee4887a5054f6de13  tools/automacao/runtime/KIT04Adapter.SR/SRScreenManager.cs
9f1511bdc19a796dc0a2f86d0ef1e9427827609797ddae0e219bd7f00bf00bc0  tools/automacao/runtime/KIT04Adapter.SR/KIT04Adapter.SR.csproj
2ff7d152fcb687be8ad0db9f6c5f7fc582c6c4473e2d8e8112082ad51e652318  tools/automacao/runtime/harness-passivo/Program.cs
```
Lista completa (inclui logs) em `scratch/kit/KIT-05F/hashes-kit05f.txt`.
Fontes pré-correção preservados em `scratch/kit/KIT-05F/backup/`; hashes de
partida em `scratch/kit/KIT-05F/baseline-sha256.txt`.

## 2. F8 — integração (o que foi implementado e como foi provado)

* `KIT04Core/PipelinePassivo.cs` (novo, **sem dependência de Unity/BepInEx**):
  mesmo contrato do pipeline Python — dedup por fonte, fila/retenção, teto de
  pedidos de captura, pausa com lacuna, timeout com motivo, captura em duas
  fases, limites auxiliares com contadores de descarte e limpeza de órfãos.
* `CorePlugin.cs`: `EventosImpl` deixou de ser lista sem teto (`maxEventos`,
  contador `Descartados`); `Passivo` (pipeline do Core), `RegistrarEventoPassivo`,
  `ResumoPassivo`, `EventosPassivos`, `VerificarTimeoutsPassivos`, e o resumo
  entra em `ResultadoFinal()`.
* `KIT04Adapter.SR/PontePassivaRSTV.cs` (novo): traduz observação REAL em eventos
  RSTV — transições de `SRScreenManager.TelasMonitoradas` → `janela_aberta`/
  `janela_fechada`; clique observado no input (`Input.GetMouseButtonDown`) →
  `clique_recebido`; alimenta o **pipeline do Core** (não cria outro). Opt-in
  `passivoHabilitado=false`: com a flag desligada `Observar` devolve vazio e nada
  é registrado. Nada clica/salva/equipa/modifica gameplay.
* `SRAdapterPlugin.Update`: caminho passivo (opt-in separado) e o caminho legado
  passou a emitir só em **mudança de estado** (fim do spam por frame apontado em
  F8). Referência `UnityEngine.InputLegacyModule` acrescentada ao `.csproj`.

Provas:

```
$ dotnet run --project tools/automacao/runtime/harness-passivo
 verificacoes: 29 OK, 0 FALHA
 VEREDITO HARNESS: VERDE (exit 0)                                     EXIT=0

$ dotnet run --project tools/automacao/runtime/harness-passivo -- --defeito opt_in
[FALHA ] opt-in false => Observar devolve nada -> eventos=2
[FALHA ] opt-in false => pipeline inerte (0 eventos) -> eventos_total=2
 verificacoes: 27 OK, 2 FALHA
 VEREDITO HARNESS: VERDE do controle negativo (defeito detectado)     EXIT=0
```

O harness compila por LINK os fontes reais (`PipelinePassivo.cs` +
`PontePassivaRSTV.cs`) e prova ligação/estado **sem abrir o jogo**. O controle
negativo mostra o harness REPROVANDO uma ponte que ignora o opt-in.

Build isolado (preflight de deploy exercitado antes de compilar; C# em cópia):

```
$ dotnet build <copia>/tools/automacao/runtime/KIT04Adapter.SR/KIT04Adapter.SR.csproj \
      -c Release -p:DeployToBepInEx=false
    65 Aviso(s)
    0 Erro(s)                                                        EXIT=0
# DLLs geradas DENTRO da cópia: KIT04Adapter.SR.dll, KIT04Core.dll
PERFIL (r2modman Default) ANTES/DEPOIS: 23 arquivos, hash idêntico  -> PERFIL_INALTERADO=OK
```

## 3. Execuções reais (comando → exit)

| Comando | Resultado |
|---|---|
| `python tools/automacao/kit05/teste_observacao_passiva.py` | Ran 37 tests, OK, exit 0 |
| `python test_revisao_kit05.py` (suite do reviewer, módulo novo) | Ran 16 tests, OK, exit 0 (antes: 10 FAIL/6 OK, exit 1) |
| `python tools/automacao/kit05/contra_prova_kit05.py` | 20 iscas + controle; VERDE, exit 0 |
| `python tools/automacao/kit05/contra_prova_kit05.py --individual` | 37/37 reprovando sozinhos; VERDE, exit 0 |
| `bash tools/automacao/kit05/roda_testes_kit05.sh` | VERDE, exit 0 (repo e sandbox sem `.git`) |
| runner pré-correção na sandbox sem `.git` | exit 2, `fatal: not a git repository` |
| `PYTHON=/nao/existe/python bash .../roda_testes_kit05.sh` | exit 2 (nenhuma ausência verde) |
| `dotnet run --project tools/automacao/runtime/harness-passivo` | 29/29 OK, exit 0 |
| `dotnet build ... -p:DeployToBepInEx=false` (cópia isolada) | 0 erros, perfil inalterado |

CLI real do pipeline (execução medida; log `scratch/kit/KIT-05F/cli-fixture-f.log`,
json `cli-fixture-f.json`):
`python tools/automacao/runtime/observacao_passiva.py --entradas tools/automacao/runtime/fixtures/kit05-observacao.entrada.json --out scratch/kit/KIT-05F/cli-fixture-f.json`
→ exit 0, `origem=fixture-offline`, `runtime=NAO_EXERCITADO`,
`eventos_total=6 == len(eventos_retidos)=6`, `falhas_retidas=1`,
`capturas_solicitadas=0`/`capturas_confirmadas=0` (sem pedido explícito),
`simultaneidade_afirmada=false`, `degradacoes_motivos=[pausado, sem_mudanca, tipo_ativo]`.

## 4. O que NÃO foi feito (limites honestos)

* **Nenhuma execução de jogo**: runtime, desempenho, pixels reais e interferência
  permanecem **NAO_EXERCITADO** — exigem rodada autorizada do dono.
* O clique observado é o do **input do engine** (passivo); não se fez patch em
  método de jogo, não se emitiu clique e não se alterou gameplay.
* Nada foi instalado no perfil r2modman, nada publicado, nenhum `git add`/commit.
* `Assembly-CSharp.dll`, Bard/música, gates, modelos, política, crons e
  prioridades: intocados. KIT-06/07/09 **não** foram implementados; seguem presos
  a este cartão até a revisão independente.
* A suíte AUT-4 não foi reexecutada; não se alega não-regressão runtime.

## 5. Próximo passo

Revisão independente no MESMO cartão (`kanban_request_review`), com instância
≠ 631, refutando F1–F9 item a item e conferindo os hashes acima. Só a aprovação
libera KIT-06/07/09; nada aqui autoriza gate humano, runtime ou publicação.
