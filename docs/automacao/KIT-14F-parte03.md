# KIT-14F — parte 03: o defeito 3 estava VERDE FALSO (rodada 2)

Cartao: `t_c46abdf7` · run708 · implementador `default` (≠ revisor run707)
Evidencia anterior: `docs/automacao/KIT-14F-parte01.md`, `KIT-14F-parte02.md`,
revisao de run707 no proprio cartao (bloqueante).
Este arquivo NAO substitui os anteriores: sao o historico da rodada 1.

## 1. O que a revisao derrubou (e por que ela esta certa)

A rodada 1 declarou o defeito 3 corrigido com 7OK/0 no harness. O revisor mostrou que
o verde nao vinha do PRODUTO:

* `TentarNavegar()` tinha **UM unico call site** (`AUT4ProbePlugin.cs:413`), dentro do
  `case F_LEITURA` — uma fase de **quadro unico** — que terminava com
  `Ir(F_PRINT1, "print-01")` **incondicional** na linha 415.
* Em producao `tentativa` chegava a **1** com `teto=12`: o ramo `aguardando` era o
  unico alcancavel e o ramo `esgotado` / o teto **nunca** aconteciam. A rotina seguia
  sendo de quadro unico — exatamente o defeito do run704 (tela de LOADING,
  `botoes_ativos=0`).
* O verde da parte3 vinha do **harness**, que chamava `TentarNavegar` 12x num laco
  manual (`Program.cs:684-690`) e 10x num probe novo (`:743`). O harness fabricava o
  laco que o produto nao tinha. Isso e verde falso: o teste media o harness, nao o
  produto.

O objetivo do cartao — "a navegacao por handlers in-process **encontra os alvos** (o kit
dependia disso para nao precisar de clique de OS)" — nao foi atingido na rodada 1.

## 2. Correcao (a) — o PRODUCTO passa a reinvocar quadro a quadro

Mudanca no fonte do probe (`tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs`):

1. **Nova fase `F_NAVEGACAO = 5`**, declarada junto das outras (`= 0..4`).
2. **`F_LEITURA` deixa de transitar incondicionalmente.** Ao fim da leitura:
   * `TentarNavegar()` e chamado **uma** vez (como antes);
   * se `NavegacaoTerminou()` (alvo invocado **ou** teto esgotado) → segue para o
     print, como antes;
   * senao → `Ir(F_NAVEGACAO, "navegando")`: a fase **fica viva**.
3. **`case F_NAVEGACAO`** chama `TentarNavegar()` **uma vez por quadro** — quem
   reinvoca e o **proprio driver** (`Tick -> Passo`, um `Passo` por quadro).
   Quando `NavegacaoTerminou()`, pede o print e vai para `F_PRINT1`.
4. **`NavegacaoTerminou()` / `TetoNavegacao()`** concentram a regra de parada:
   `_navegacaoConcluida || _navegacaoTentativas >= teto`. O `teto` continua vindo de
   `_navTentativasMax` (`NavegarTentativasMax`, default 12).

Efeito no jogo: a tela de LOADING nao encerra mais a navegacao no primeiro quadro — o
driver tenta de novo a cada quadro ate o botao `Skills` aparecer **ou** o teto esgotar
(com `estado=esgotado` e `motivo` declarado, e o roteiro seguindo para o print em vez
de travar).

## 3. Correcao (b) — o teste passa a exercitar o DRIVER REAL

`tools/automacao/runtime/harness-kit14f/Program.cs`, parte 3 reescrita:

* monta o plugin REAL por reflexao (`GetUninitializedObject` + `LigarBaseUnityPlugin`),
  como antes;
* **inicializa o estado que o driver usa** (`_res`, `_passos`, `_observacoes`,
  `_marcos`, `_arquivosDePrint`, `_eventosFrame`, `_printsDetalhe`, `_dir`,
  `_navegar=true`, `_demostrar=false`) — sem isso o corpo do `case F_LEITURA`
  estourava em `NullReferenceException` antes de chegar na navegacao;
* **avanca QUADROS chamando `Passo()`** — o passo por quadro do PRODUTO. O harness
  **nao** chama `TentarNavegar` nenhuma vez;
* cenario A (alvo aparece no 3o quadro): exige que o **produto** tenha tentado mais de
  uma vez, achado o alvo, invocado **exatamente uma** vez e transitado para `F_PRINT1`;
* cenario B (nunca aparece): exige que o **produto** esgote o teto **e saia da fase
  sozinho** (nao trava), com `estado=esgotado` + `motivo`;
* cenario C (defeito original): partindo de `F_LEITURA`, exige que o produto **nao**
  pule para `F_PRINT1` no primeiro quadro — e entre em `F_NAVEGACAO`.

O vermelho passa a vir do mesmo teste apontado para a DLL **pre-conserto**.

## 4. Achados secundarios da revisao (corrigidos junto)

* `Program.cs:496-505` chamava `TentarVincular` **duas vezes por iteracao**
  (`Invocar` + `vincular.Invoke` direto), entao "3 quadros simulados" eram 6 chamadas.
  Agora e **uma chamada por quadro** e o rotulo nao mente.
* `baseline-probe/` veio de `git show HEAD:` — **nao** e o working tree pre-KIT-14F
  (que tem KIT-R0F/F3/F5 nao commitadas). Isso passa a estar **declarado** na
  evidencia, e a rodada 2 usa como "ANTES" principal a build do **working tree da
  rodada 1** (`scratch/kit/KIT-14F-run706/_atual-probe.cs`, sha
  `947826cd375060bb104c81e67cb8ac4a7a153ff00a6e1d5fe24e7a7c7890b23e`) — que e o
  conserto REJEITADO por run707, o "antes" honesto DESTE cartao.

## 5. NAO_EXERCITADO (mantidos da rodada 1 + o que esta rodada acrescenta)

Mantidos: Chainloader real ordenando plugins em jogo; recorder capturando de jogo real
em execucao; navegacao clicando `Button` REAL da engine (aqui o alvo vem da porta
injetavel — offline nao ha engine); Harmony patchando de verdade; overhead do recorder;
build instalada no perfil do dono / aceite humano de UI.

Acrescentado nesta rodada:
* **o `_navTentativasMax` (ConfigEntry do .cfg) nao e lido de um .cfg real** — offline o
  campo fica `null` e o `TentarNavegar` cai no default `NavegarTentativasMax=12`, que e
  o mesmo teto do jogo sem `.cfg`:
  `12` e o valor DEFAULT do produto, nao um valor inventado pelo teste.
* **`ScreenCapture` / `Time.frameCount` reais**: o `case F_NAVEGACAO` nao os usa; a
  transicao para `F_PRINT1` chama `PedirPrint`, cuja unica parte que precisa da engine
  (`ScreenCapture.CaptureScreenshot`) e o unico trecho declarado como nao exercitado
  daquela transicao.

Nada instalado no perfil do dono. Nenhum clique de sistema. Nenhum commit.
