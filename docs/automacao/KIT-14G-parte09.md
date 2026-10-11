# KIT-14G — parte09: resposta à revisão run713, item por item, com as provas

Cartão `t_0e656658`, run714 (implementador `default/run714` ≠ revisor `default/run713`).
Artefatos desta rodada: `KIT-14G-parte06.md` (crash + rótulos falsos), `-parte07.md` (recorder),
`-parte08.md` (A/B da causa). Máquina: `scratch/kit/KIT-14G-run714/verification.json`
(sha256 `4603fdd78a92270df3c7acbaa1f5e595212fc06736f232ed035719f99c57b881`, gerado por
`gera_verification.py` a partir dos artefatos medidos).
Bancada: `scratch/kit/KIT-14G-run714/roda714.py` + boots `A-sem-passivo`, `B-semeado`,
`C-sem-nada`, `D-probe-play`, `E-sem-navegar`.

O produto **não foi tocado**: `AUT4ProbePlugin.cs` continua `594c8add…` e a DLL `1d496dbc…`
(conferido no topo do `verification.json`). Nenhum `.cfg` do perfil do dono, nenhum commit,
nenhum deploy, nenhuma publicação.

---

## Correção 1 — "provar a causa real da morte do processo" — ATENDIDA (e o resultado inverte o diagnóstico)

- **Event Log colhido** (a prova que faltava): 5 entradas `Application Error` id 1000 para
  `Stolen Realm.exe`, uma por boot que morreu, TODAS com módulo `ntdll.dll`, exceção `0xc0000005`
  (ACCESS_VIOLATION), deslocamento `0x4a612`; nenhuma para os boots que viveram.
  Ver `KIT-14G-parte06.md` §1 e `verification.json.causa_da_morte_eventlog_run712`.
- **A/B executado** — na verdade 5 bancadas novas (A–E), não 2 (ver `KIT-14G-parte08.md`):
  - **(a) "dados isolados vazios" → ELIMINADO.** Boot `B-semeado`: diretório isolado semeado com
    **cópia somente-leitura** do snapshot do dono (96 itens, `Character0..16.json`,
    `GlobalSaveData.json`, `ItemStash.json`…); o save real nunca é escrito (fica renomeado ao lado
    durante a rodada). **Morreu igual**, mesma assinatura.
  - **(b) "isolamento" → ELIMINADO.** Boot `C-sem-nada`: bancada isolada com **0 plugins**
    (`LogOutput`: "*0 plugins to load*") — o jogo **viveu 118,0 s** com desligamento limpo e
    **zero** entradas de crash na janela do boot.
  - **(b') "mods instrumentais (Core/Adapter)" → ELIMINADO.** Boot `A-sem-passivo`: só o probe
    (`mods_carregados.total = 1`) — **morreu igual**.
  - **Gatilho isolado:** boot `E-sem-navegar` (mesma rota declarada, `Navegar=false`, o probe só
    observa) **viveu 121,9 s**; boot `D-probe-play` (rota sem `Accept`, navegando) **viveu 122,3 s**.
    Todo boot em que a navegação **clicou** até `Accept` morreu.
- **Conclusão:** é **defeito CORRÍGIVEL do caminho de clique do instrumento** (`onClick.Invoke()`,
  `AUT4ProbePlugin.cs:1030`), **não** limitação de ambiente e **não** a premissa de dados vazios.
  Porta que fica aberta, declarada: **onde** o `c0000005` nasce dentro do caminho do clique. O
  discriminador é o **clique físico** — que é, por desenho, a etapa visual do dono do KIT-14; ela
  passa a ter valor diagnóstico direto (com clique físico a run sobe ⇒ defeito nosso; também morre
  ⇒ defeito do jogo/ambiente).

## Correção 2 — "os 5 boots não sustentam a divisão guarda×crash" — ATENDIDA

`KIT-14G-parte06.md` §3 traz a tabela por boot (o que existe de artefato, o `result.json`
terminal, o tamanho/desfecho do `Player.log`, a entrada de Event Log). Correções aceitas:
- os `aut4probe.json` de `roteiro3/3b/4/5/6` estão congelados (sem `marcos`/`eventos_frame`/
  `recoleta`/`recorder`) — conferido e registrado no `verification.json`;
- os 5 terminam com o **mesmo** `RuntimeError: Multiple game processes; cannot assume ownership`:
  a divisão "guarda abortou" vs "crash medido" era **falsa**; a diferença real é só *quando* a
  guarda viu (sem tolerância em 3/3b/4; com tolerância de 30 s em 5/6, que registraram
  `duplicata_transitoria` com `pids_finais: []` = **os dois processos sumiram**);
- uso explícito do par de `Player.log` (4.516 B sem shutdown × 17.997–18.071 B com shutdown);
- a frase da parte05 §2 ("recoleta OK para todo boot que finalizou") vale **só** para
  `mapa/roteiro1/roteiro2` — corrigida.

## Correção 3 — "por que o recorder deu 0" — ATENDIDA, com veredito novo

`KIT-14G-parte07.md`. O recorder é **cego a clique sintético por construção**: só ganha evento por
(i) transição das 6 telas de `SRScreenManager.TelasConhecidas` e (ii) `Input.GetMouseButtonDown(0)`;
a navegação do probe é `botao.onClick.Invoke()` (não passa pelo `Input`). Com `passivoHabilitado=true`
o caminho legado (`tela_detectada`) nem roda. **Veredito: bloqueado-por-design**, citando os dois
gates. Prova executada: `dotnet run --project tools/automacao/runtime/harness-passivo` →
**29 OK / 0 FALHA, exit 0** (`scratch/kit/KIT-14G-run714/logs-harness-passivo.log`), incluindo
`clique observado vira clique_recebido` e `resumo nao promove runtime`.
**Achado separado, declarado como defeito candidato de PRODUTO (Core), fora do escopo do KIT-14G:**
nos três boots que finalizaram, com o Core habilitado, `ResultadoFinal().eventos` vem **vazio** —
o livro `_eventos` só nasce no 1º `Update()` do Core, logo o `Update()` do Core não tickou. Não
corrigi o produto nesta rodada; fica para cartão próprio, com o reprodutor exato.

## Correção 4 — "dois rótulos falsos de evidência" — ATENDIDA

`KIT-14G-parte06.md` §2, com sha256 medidos:
- `sandbox/` **não** é "cópia do produto antes do primeiro boot": os 5 fontes e a DLL batem
  byte a byte com a árvore atual (`594c8add…`/`1d496dbc…`), `mtime` 19:09 (depois do 1º boot, 19:03).
  Rótulo corrigido para o que ele prova de fato;
- `manifest` do `roteiro2` acusa `recorder.json` como `FileNotFoundException` **embora o arquivo
  exista** (1.447 B, sha `61489695…`, e o bloco `recorder` do mesmo documento o lê como `LIDO`):
  é artefato de **ordem de escrita** do manifesto, e passa a ser lido assim.

## Aceite do escopo (o que o cartão pediu)

| item | estado |
|---|---|
| 1. recorder eficaz com prova real | **PARCIAL**: consumidor provado (arquivo + identidade + contagem lida) e a razão do `0` **provada e classificada** (gate de projeto + defeito candidato do Core). `eventos_total > 0` segue NAO_EXERCITADO: exige o HUD da run, que morre ao ser aberto. |
| 2. navegação até Skills | **PARCIAL/NAO_EXERCITADO**: rota `Play → Roguelike → CreatingCharacter` provada por handler com mapa real de botões; chegar até o botão do RSTV é impedido pelo defeito da correção 1, agora **localizado** (o clique que inicia a run) em vez de atribuído a "dados vazios". |
| 3. recoleta pós-navegação | **OK no mecanismo**: `recoleta.apos_navegacao=true` e `recoleta.frame == eventos_frame.png_01-ui_solicitado` (mesmo instante; run710 era 157 × 1352). |
| 4. Runner pos/neg, mod sem kit, medições | **NAO_EXERCITADO** (depende de 1–2). Nenhum número de performance foi medido ou inventado; o dono dispensou limiares. |

## NÃO EXERCITADO (declarado, sem número inventado)

HUD da run / botão do RSTV; `recorder.eventos_total > 0`; clique físico / aceite UI-UX (dono);
Runner positivo/negativo; RSTV sem kit; FPS/frame/IO comparáveis; segundo ambiente; e o ponto
exato do `c0000005` dentro do caminho de clique.

## Testes e travas executados nesta rodada (todos verdes)

| comando | resultado |
|---|---|
| `dotnet run --project tools/automacao/runtime/harness-passivo -c Release` | 29 OK / 0 FALHA, exit 0 |
| `python tools/automacao/runtime/roda_testes_runtime.py` | **VERDE exit 0 — 16 testes** |
| `python tools/automacao/runtime/roda_testes_runtime.py --contra-prova` | **VERDE exit 0 — 33 testes** |
| `python tools/check_segredos.py` | exit 0 — nenhum padrão de credencial |
| `python tools/check_padroes_segredo.py` | exit 0 — nenhum padrão de credencial |
| `python tools/check_dupes.py` | exit 0 — nenhuma duplicada |
| `python tools/audita_docs.py` | exit 0 — nenhuma inconsistência |

Logs em `scratch/kit/KIT-14G-run714/*.log`. Ambiente ao fim: dados do dono **111/111 byte a byte**,
`production_diff().equal = True`, **sem junction**, **0 processos**, perfil do dono **sem**
`plugins/AUT4Probe` e **sem** `plugins/KitPassive`, Cloud do app `1330000` **OFF**.

## Correção de processo entregue de lambuja (e que causou o resíduo do run712)

O `finally` do driver abortava a limpeza inteira no primeiro `PowerShell rc=1` (`ps()` levanta
quando o PID já morreu — `Get-Process -ErrorAction SilentlyContinue` deixa `$?` falso). Era isso
que deixava o `bepinex-iso` do `roteiro5/6` para trás. `roda714.py` blinda cada passo de
restauração em try/except: nos 5 boots novos, `dados-verificar`, `dados-restaurar`,
`bepinex-rollback` e `front-release` saíram **exit 0** — inclusive nos que morreram.
Também acrescenta `processo_sumiu_em_s`, para o silêncio da janela não passar por sobrevivência.
