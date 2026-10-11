# KIT-14G — parte06: causa REAL do encerramento (Event Log) e correção dos rótulos falsos

Cartão `t_0e656658`, run714 (implementador, respondendo à revisão run713). Complementa parte01–05.
Fonte de verdade por máquina desta parte: `scratch/kit/KIT-14G-run714/verification.json` (criado no fim da rodada).
Este arquivo NÃO sobrescreve nenhum artefato anterior.

A revisão run713 pediu 4 correções. Esta parte fecha as de **número 2 e 4** e traz a **prova dura
da causa da morte do processo (item 1)**. As partes seguintes fecham o item 3 e o A/B restante.

---

## 1. Prova dura da morte do processo: Windows Event Log (item 1 da revisão)

O handoff do run712 dizia "causa provável: premissa 'dados vazios'". Isso era **hipótese**.
A revisão pediu a razão real. Ela existe e foi colhida agora, do log de eventos do Windows
(`Application`, provedor `Application Error` / `Windows Error Reporting`), em modo somente leitura:

```
powershell -NoProfile -Command "Get-WinEvent -FilterHashtable @{LogName='Application';
  ProviderName='Application Error'; StartTime=(Get-Date).AddHours(-4)} |
  Where-Object { $_.Message -match 'Stolen Realm' } | Select TimeCreated,Message"
```

Cinco entradas, **uma por boot que entrou na run** — e nenhuma para os boots que ficaram no menu:

| Evento (hora local) | boot | módulo com falha | exceção | deslocamento | PID |
|---|---|---|---|---|---|
| 19:15:50 | roteiro3 | `ntdll.dll` | `0xc0000005` | `0x4a612` | 0x87E4 |
| 19:16:56 | roteiro3b | `ntdll.dll` | `0xc0000005` | `0x4a612` | 0x7E28 |
| 19:18:24 | roteiro4 | `ntdll.dll` | `0xc0000005` | `0x4a612` | 0x8798 |
| 19:19:55 | roteiro5 | `ntdll.dll` | `0xc0000005` | `0x4a612` | 0x2EE8 |
| 19:22:07 | roteiro6 | `ntdll.dll` | `0xc0000005` | `0x4a612` | 0x3F5C |

Leitura: **`ACCESS_VIOLATION` (0xc0000005) em `ntdll.dll`, SEMPRE no mesmo offset `0x4a612`**,
no processo `Stolen Realm.exe` (Unity `2022.3.62.28864`, caminho
`E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm.exe`). Não é "o driver encerrou o
jogo": é o **próprio processo do jogo violando acesso** — crash nativo, determinístico (mesmo
offset em 5 execuções independentes). O boot `mapa`, `roteiro1` e `roteiro2`, que não entraram na
run, **não** geram entrada nenhuma.

Isso **corrige** a redação do run712 ("crash medido" era certo; "premissa de dados vazios" era
palpite sem prova) e dá a base objetiva para o item 1 da revisão.

### 1.1 Comparação dos `Player.log` (a prova que a revisão apontou e que não foi usada)

- boots que **entraram na run** (`roteiro3/3b/4/5/6`): `dados-iso/dados-do-jogo/Player.log` =
  **4.516 B**, termina no meio da carga de cena, na linha
  `Unloading 17 unused Assets to reduce memory usage. Loaded Objects now: 42277.` seguida de
  `Total: 21.622400 ms ...` — **sem** o relatório de desligamento do Unity;
- boots que **não** entraram (`mapa/roteiro1/roteiro2`): 17.997 / 18.029 / 18.071 B, terminando com
  o bloco `Allocator` / `[ALLOC_*]` = **relatório de encerramento limpo** do Unity.

Ou seja: os boots que morreram **não tiveram shutdown** — o log para no meio. Os que viveram
tiveram. É o par de evidências que sustenta "morte abrupta" sem depender de ausência de linha.

### 1.2 O "processo irmão" do guard é o **crash handler**, não a causa

`scratch/kit/KIT-14G-run712/proc_log.txt` (amostragem externa a cada ~1 s) mostra, para o boot
`roteiro4`: PID `34712` começa em `19:17:58` e desaparece em `19:18:32` (~34 s). **No instante da
morte** aparece um segundo PID (`18780`) que some junto. Em `roteiro5`: PID `12008` de `19:19:30`
até `19:20:00`, com `11768` aparecendo em `19:19:55`. Ou seja: **o irmão nasce no mesmo quadro da
morte** — é o *relator de falha* (Windows Error Reporting / crashpad) tratando o crash, não um
segundo jogo. O guard do driver lê isso como "Multiple game processes" e aborta.

Correção de rota explícita: na parte05 §3 a divisão era "boots 3/3b/4 = guarda abortou" vs
"roteiro5/6 = CRASH medido". **A divisão era falsa**: nos 5 boots `result.json` termina com o
MESMO `RuntimeError: Multiple game processes; cannot assume ownership`. A diferença real é só
*quando* o guard viu:
- `roteiro3/3b/4`: guard sem a tolerância (driver antigo) → abortou no 1º instante em que o irmão
  apareceu, ou seja, **no instante do crash**;
- `roteiro5/6`: guard com tolerância (o próprio run712 patchou `roda.py`) → esperou até 30 s e
  registrou `duplicata_transitoria: [{"observada_em_s": 33.9 / 33.7, "pids_finais": []}]`.
  `pids_finais: []` = **depois da espera não havia nenhum processo do jogo** — morreram os dois.
  Foi só então que o driver levantou o erro (mensagem enganosa: ele fala em "múltiplos
  processos", mas o que mediu foi "nosso pid também sumiu").

O Event Log §1 é o que decide a questão: a morte é do **jogo**, com `c0000005`, e o guard é
consequência, não causa.

---

## 2. Correção dos rótulos falsos de evidência (item 4 da revisão) — CONFIRMADO

### 2.1 `sandbox/` NÃO é "cópia do produto antes do primeiro boot"

Medido agora, byte a byte:

| arquivo | produto (`tools/automacao/runtime/AUT4Probe/…`) | `KIT-14G-run712/sandbox/…` | igual |
|---|---|---|---|
| `AUT4ProbePlugin.cs` | `594c8add…` | `594c8add…` | SIM |
| `LeituraAgregados.cs` | `f3985436…` | `f3985436…` | SIM |
| `IdentidadeDoProbe.cs` | `c23574f3…` | `c23574f3…` | SIM |
| `Json.cs` | `ae30a1ac…` | `ae30a1ac…` | SIM |
| `AUT4Probe.csproj` | `347770d0…` | `347770d0…` | SIM |
| `bin/Release/AUT4Probe.dll` | `1d496dbc…` | `1d496dbc…` | SIM |

E a `mtime` de `sandbox/…/AUT4ProbePlugin.cs` é `2026-10-10 19:09:21`, **posterior** ao primeiro
boot (`mapa`, 19:03–19:06, que rodou a DLL antiga `687b72f1…`).

Veredito: o rótulo `verification.json` / parte04 §1 ("cópia do produto **antes** do primeiro
boot") é **falso**. O `sandbox` contém o produto **pós-correção** e o `diff` contra a árvore atual
é **vazio**. O que o `sandbox` prova legitimamente é outra coisa, e é assim que passa a ser
rotulado: *"cópia de trabalho do produto **idêntica à árvore atual** no fim da rodada — o que a
rodada executou de fato foi a DLL `1d496dbc…` (conferida por `sha256` antes de cada boot pelo
próprio `roda.py`)"*. O que ele **não** prova é anterioridade.

### 2.2 O `manifest` do `roteiro2` acusa `recorder.json` como `FileNotFoundException` — e o arquivo existe

`roteiro2/probe/aut4probe.json` traz, no mesmo documento:

- bloco `recorder`: `"status": "LIDO"`, `"arquivo_bytes": 1447`,
  `"arquivo_sha256": "614896952a8dd3dea02d81e8ad20e8566c7c242a509621c090bc30791dbaf7ea"`;
- bloco `manifest`: `{"arquivo": "recorder.json", "erro": "FileNotFoundException"}`.

Os dois não podem estar certos. O arquivo existe em disco (1.447 B) e casa com o sha do bloco
`recorder`. Leitura correta: o `manifest` é montado **antes** de `recorder.json` ser gravado (ordem
de escrita), então o `FileNotFoundException` é artefato da ordem do manifesto, **não** ausência do
arquivo. Rótulo corrigido: o manifesto deve ser lido como *fotografia anterior à gravação do
recorder*; a prova de existência é o par `arquivo_bytes`/`arquivo_sha256` do bloco `recorder`.

---

## 3. Por boot, o que foi MEDIDO (item 2 da revisão)

Todos os `aut4probe.json` dos boots que **não finalizaram** (`roteiro3/3b/4/5/6`) estão
**congelados no mesmo ponto**: `"status": "INICIADO"`, `"fase": "navegando"` e **sem** as chaves
`marcos`, `eventos_frame`, `recoleta`, `recorder`, `manifest`, `prints` (conferido por inspeção das
chaves). A revisão está certa: não há `aut4probe.json` terminal nesses boots — o probe foi morto
junto com o jogo.

| boot | rota | artefatos que existem | `result.json` terminal | Player.log | Event Log |
|---|---|---|---|---|---|
| `mapa` | `Play` | aut4probe + 2 PNG + `LogOutput-isolado` | sem `error`; `game_closed: true` | 17.997 B, com shutdown | — |
| `roteiro1` | `Play` | aut4probe + 2 PNG | sem `error` | 18.029 B, com shutdown | — |
| `roteiro2` | `Play;Roguelike` | aut4probe + 2 PNG + `recorder.json` | sem `error` | 18.071 B, com shutdown | — |
| `roteiro3` | `…;Accept` | só `probe/aut4probe.json` (INICIADO) | `error: Multiple game processes` | 4.516 B, sem shutdown | **19:15:50 `c0000005`** |
| `roteiro3b` | `…;Accept` | só `probe/aut4probe.json` (INICIADO) | `error: Multiple game processes` | 4.516 B, sem shutdown | **19:16:56 `c0000005`** |
| `roteiro4` | `…;Accept` | só `probe/aut4probe.json` (INICIADO) | `error: Multiple game processes` | 4.516 B, sem shutdown | **19:18:24 `c0000005`** |
| `roteiro5` | `…;Accept` | `aut4probe.json` + `saves-antes/` + `bepinex-iso/` | `error: Multiple game processes` + `duplicata_transitoria[33.9s, pids_finais=[]]` + `cleanup_error: PowerShell read/close failed rc=1` | 4.516 B, sem shutdown | **19:19:55 `c0000005`** |
| `roteiro6` | `…;Accept;__nunca_casa__` | idem `roteiro5` | idem, `[33.7s, []]` | 4.516 B, sem shutdown | **19:22:07 `c0000005`** |

Duas correções de afirmação, portanto:
1. **Não** houve "crash medido" *em oposição a* "aborto da guarda": houve **crash do jogo** nos 5,
   e a guarda abortou **por causa** do crash. A prova que sustenta "crash" é o Event Log (§1) e o
   `Player.log` de 4.516 B sem shutdown (§1.1) — não a ausência de linhas.
2. A frase da parte05 §2 ("recoleta ... OK para todo boot que finalizou") **não** se estende aos
   boots que entraram na run: eles não têm `recoleta` nenhuma no JSON, porque não têm JSON
   terminal. A afirmação vale **só** para `mapa`, `roteiro1`, `roteiro2`.

---

## 4. Sem número inventado

Nada de FPS/frame/IO foi medido — permanece **NAO_EXERCITADO** (o dono dispensou limiares).
Nenhum limiar de performance foi estimado nesta parte. O único número novo aqui é de log
(offset de crash, tamanho de `Player.log`, PIDs), que é medição, não estimativa.
