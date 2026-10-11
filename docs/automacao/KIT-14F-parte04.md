# KIT-14F — parte 04: RODADA 2 (o defeito 3 consertado no PRODUTO, com prova executada)

Cartao `t_c46abdf7`, run708. Parte 01 (`KIT-14F-parte01.md`) e parte 02 (`-parte02.md`)
ficam como historico da rodada 1 (rejeitada). Parte 03 (`-parte03.md`) e o diagnostico
do bloqueante. ESTE arquivo e a evidencia da rodada 2.

## 1. O bloqueante da revisao run707 (repetido aqui para rastreio)

O verde da rodada 1 vinha do HARNESS: `Program.cs` chamava `TentarNavegar()` num laco
manual 12x (linha ~684) e 10x (~743). No PRODUTO, `TentarNavegar()` tinha um UNICO call
site (`AUT4ProbePlugin.cs:413`), dentro do `case F_LEITURA` de QUADRO UNICO, seguido de
`Ir(F_PRINT1)` **INCONDICIONAL** — o teto e o ramo `esgotado` eram INALCANCAVEIS. O
objetivo do cartao (a navegacao por handlers in-process ENCONTRA os alvos) nao tinha
sido atingido.

## 2. Conserto no PRODUTO (rastro por arquivo)

`tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs`
(sha256 `21586beb01063bb2e2a64ca9ad21948397d83282382ddc1a0fc9ab024b058d1d`):

1. **Nova fase `F_NAVEGACAO = 5`** + **`Passo()` virou DESPACHANTE**: cada fase e um
   passo nomeado (`PassoEsperaUi`/`PassoLeitura`/`PassoNavegacao`/`PassoPrint1`/
   `PassoFinal`/`PassoPrint2`). Os corpos foram MOVIDOS INTEIROS (mesmo comportamento);
   a unica mudanca de fluxo e a do item 2.
2. **O roteiro pos-leitura virou um passo nomeado e condicional**:
   `FaseDepoisDaLeitura()` → com `Navegar=true` chama `TentarNavegar()` UMA vez e, se
   `NavegacaoTerminou()` for falso, devolve **`F_NAVEGACAO`**; senao devolve `F_PRINT1`.
   `PassoLeitura()` termina com `Ir(proximaFase, ...)` — **uma** avaliacao (avaliar duas
   vezes chamaria `TentarNavegar` duas vezes no mesmo quadro).
3. **`PassoNavegacao()`**: `TentarNavegar()` **uma vez por QUADRO**, chamado pelo PROPRIO
   driver (`Tick -> Passo`). Quando `NavegacaoTerminou()`, o print e pedido dentro de
   `try` (efeito best-effort: uma falha no print NAO pode prender o roteiro na fase) e o
   roteiro segue para `F_PRINT1`.
4. **`TetoNavegacao()` / `NavegacaoTerminou()`**: a regra de parada num lugar so
   (`_navegacaoConcluida || _navegacaoTentativas >= teto`).
5. **`NavegarTentativasMax`** e ligada no `Awake` (`Config.Bind`): antes a
   `ConfigEntry _navTentativasMax` existia e NUNCA era ligada (nem no `.cfg`) — o teto
   era uma constante sem porta. Default do produto: `12`.
6. Achado secundario da revisao: `PassoNavegacao` NAO chama `TentarVincular` — o problema
   das 2 chamadas por quadro era do HARNESS (ver §4).

O trecho que o cartao exigia — "a navegacao por handlers in-process encontra os alvos" —
agora tem, no PRODUTO, o laco que faltava: a fase fica viva e o driver a reinvoca a cada
quadro ate o alvo aparecer ou o teto esgotar (e entao segue o roteiro, com `motivo`).

## 3. ANTES x DEPOIS — O MESMO TESTE, EXECUTADO

Harness: `tools/automacao/runtime/harness-kit14f` (`Program.cs`
`46e0869422e6d2e9e8e65345507c5fb75f98dd56fd4887f8f39150e9720b1dfe`).
A parte3 NAO chama `TentarNavegar` nem `PassoLeitura`: ela monta o plugin REAL e **avanca
QUADROS chamando `Passo()`** (o passo por quadro do produto). Logs em
`scratch/kit/KIT-14F-run708/`.

| verificacao (parte3) | ANTES (run706) | DEPOIS |
|---|---|---|
| fase propria de navegacao (`F_NAVEGACAO`) | FALHA (ausente) | OK (=5) |
| roteiro pos-leitura nomeado (`FaseDepoisDaLeitura`) | FALHA (ausente) | OK |
| (A0) sem alvo, o roteiro vai para `F_NAVEGACAO` (nao para o print) | FALHA (NRE: roteiro trancado) | OK |
| (IL) `PassoLeitura` chama `FaseDepoisDaLeitura` | FALHA | OK |
| (IL) `Passo` despacha `F_NAVEGACAO` -> `PassoNavegacao` | FALHA | OK |
| (A) driver avancou >1 quadro; releu a fonte de botoes | FALHA (1 quadro, 0 consultas) | OK (3 quadros, 3 consultas) |
| (A) handler do alvo invocado EXATAMENTE 1x | FALHA (0) | OK (1) |
| (A) driver SAiu da fase sozinho, para o print | FALHA | OK (fase final = F_PRINT1) |
| (A) resumo `invocado` com `tentativas=3` e `tentativas_max=12` | FALHA (sem resumo) | OK |
| (B) sem alvo: esgota o teto e SAI (nao trava) | FALHA | OK (12 quadros) |
| (B) resumo `esgotado` + `motivo` | FALHA | OK |
| (C) teto=4 vindo do `.cfg` (`NavegarTentativasMax`) | FALHA | OK (4 quadros) |
| **agregado parte3** | **4 OK / 16 FALHA — exit 1** | **21 OK / 0 FALHA / 3 NAO_EX — exit 0** |

* VERMELHO: `--parte3 --probe-bin=scratch/kit/KIT-14F-run708/baseline-probe-run706`
  (`AUT4Probe.dll` `2f3e0f7e930517ef0b9598e57a74f4dedf8fafdda304b64e9dbfa85114d15fab`,
  buildada do fonte da rodada 1 `scratch/kit/KIT-14F-run706/_atual-probe.cs`, sha256
  `947826cd375060bb104c81e67cb8ac4a7a153ff00a6e1d5fe24e7a7c7890b23e` — o conserto
  REJEITADO). Log: `log-baseline-probe-run706-parte3.txt`, **exit 1**.
* VERDE: harness sem argumentos, DLL `5781417af99a45fd9066b52e2e52ceeb72047413c237980869c6fb80a8da68e7`.
  Log: `log-consertado-todas.txt` — parte1 10 OK, parte2 5 OK, parte3 21 OK,
  `RESULTADO|PASSOU|`, **exit 0**.
* O "ANTES" de HEAD tambem foi rodado (`--probe-bin=scratch/kit/KIT-14F-run706/baseline-probe`,
  DLL buildada de `git show HEAD:`) → 5 OK / 15 FALHA, log
  `log-baseline-probe-HEAD-parte3.txt`. **Proveniencia declarada**: essa build vem do
  HEAD, que NAO e o working tree pre-KIT-14F (tem KIT-R0F/F3/F5 nao commitadas). Ela
  serve so como referencia adicional; o "ANTES" **principal** desta rodada e a build
  run706 acima, que e exatamente o estado rejeitado por run707.

Defeitos 1 e 2 (inalterados nesta rodada) seguem com o mesmo par ANTES/DEPOIS:
`--adapter-bin=scratch/kit/KIT-14F-run706/baseline-adapter` → parte1 1 OK/4 FALHA
(`NullReferenceException ... SRAdapterPlugin.Awake()`, `deps=[]`, `_estadoVinculo=` vazio),
parte2 0 OK/2 FALHA, exit 1 (`log-baseline-adapter-parte1e2.txt`); contra a build
consertada, parte1 10 OK e parte2 5 OK.

## 4. Achados secundarios da revisao (corrigidos junto)

1. **`Program.cs` chamava `TentarVincular` 2x por iteracao** (`Invocar` + `vincular.Invoke`
   direto): "3 quadros simulados" eram 6 chamadas e o rotulo mentia. Agora e **uma
   chamada por quadro** (helper `InvocarRetorno`, que devolve o retorno sem reinvocar), com
   a verificacao nova "um quadro = UMA chamada a TentarVincular (3 quadros = 3 chamadas)".
2. **`baseline-probe/` do run706 veio de `git show HEAD:`** — nao e o working tree
   pre-KIT-14F. Declarado aqui (§3) e substituido como "ANTES" principal pela build do
   working tree da rodada 1.

## 5. Achado TECNICO novo desta rodada (e como o teste contorna)

Fora do jogo, **um metodo do probe que CHAME uma funcao de engine nao pode nem ser
carregado pelo CLR**: `SecurityException: ECall methods must be packaged into a system
module` (a engine so e "system module" dentro do proprio jogo). MEDIDO aqui, nao suposto:
`ColetarObservacoes()`, `Evento(string)` e o `Passo()` de switch unico da rodada 1 morrem
nesse pre-carregamento; `Passo()` despachante + `PassoNavegacao()` + `TentarNavegar()`
rodam.

Consequencia para o teste, declarada em vez de mascarada:
* a parte3 dirige o `Passo()` REAL a partir de **`F_NAVEGACAO`** (a fase engine-free que
  implementa o laco) e **exercita** o roteiro pos-leitura chamando
  `FaseDepoisDaLeitura()` (o MESMO metodo que `PassoLeitura` chama);
* o elo `PassoLeitura -> FaseDepoisDaLeitura` e provado **no IL do binario exercitado**
  (leitura direta dos bytes, `call`/`callvirt` para o token do metodo);
* o corpo de `PassoLeitura()` rodando offline fica **NAO_EXERCITADO com motivo medido**.

## 6. NAO_EXERCITADO (rodada 2 — a lista completa)

Herdados da rodada 1: Chainloader real do BepInEx ordenando os plugins em jogo; recorder
capturando de um jogo real; Harmony patchando de verdade; overhead do recorder; build
instalada no perfil do dono / aceite humano de UI.

Desta rodada:
1. **navegacao clicando um `Button` REAL da engine** — o alvo vem da porta injetavel
   (`PortaDeBotoes`); `Recursos<Button>()` + `onClick.Invoke()` nao rodam offline.
2. **o teto lido de um `.cfg` REAL em disco** — o `.cfg` do probe nasce no perfil do dono
   (proibido nesta rodada); a `ConfigEntry` aqui e criada pelo MESMO `Bind` do `Awake`,
   em memoria. O teto usado nos cenarios e o do PROPRIO produto (`NavegacaoTentativasMax`),
   nunca um numero do teste.
3. **`PassoLeitura()` (fase de LEITURA) rodando offline** — motivo medido em §5.
4. **`NavegarTentativasMax` sendo ESCRITA no `.cfg` pelo driver** — a chave existe no
   probe (default 12) e esta documentada no runbook (`AUT-4-runbook-rodada-autorizada.md`),
   mas `coletor.py: CFG_CHAVES` nao foi tocada nesta rodada (tocar mudaria o sha256 do
   driver, congelado no runbook/estado). Efeito pratico: o driver nao expoe a opcao; vale
   o default do probe. Declarado como pendencia, nao como feito.
5. **`PassoLeitura -> FaseDepoisDaLeitura -> F_NAVEGACAO` de ponta a ponta** — so no jogo
   (o KIT-14 re-executa depois deste cartao).

## 7. Suite do proprio repositorio

`python tools/automacao/runtime/roda_testes_runtime.py` → **VERDE, 16 testes, exit 0**
(`scratch/kit/KIT-14F-run708/log-testes-runtime.txt`). O rebuild do probe invalidou as
identidades congeladas e elas foram RE-DECLARADAS com os valores medidos:
`docs/automacao/AUT-4-estado.json` (`probe_fonte_sha256`, `probe_dll_sha256`) e
`docs/automacao/AUT-4-runbook-rodada-autorizada.md` (fonte do probe, DLL do probe, e a
linha nova da chave `NavegarTentativasMax`). Os docs de entrega antigos (KIT-14-entrega,
KIT-G2-*) mantem os hashes HISTORICOS da rodada em que foram escritos.

Nenhum clique de sistema, nada instalado no perfil do dono, nenhum commit.
