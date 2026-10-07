# COR-CIC4 — corrigir os achados A e B do parecer CIC-4R2 (`t_278bbb07`)

> Herança: o parecer independente `docs/automacao/CIC-4R2-revisao.md` **não aprovou** o CIC-4 como
> âncora de ciclo completo: o módulo fechava **verde** sem a segunda superfície (TOOLTIP) existir
> (achado **A**, `docs/automacao/CIC-4R2-revisao.md:66`) e sem autenticar a superfície que serviria
> de contra-prova (achado **B**, `docs/automacao/CIC-4R2-revisao.md:67`). Este documento entrega a
> correção **no produto** (`tools/automacao/cenarios/tooltips_shrines.py` e o seu teste) com prova
> executada de **defeito reprovando nos bytes antigos** e **passando nos bytes novos**.
>
> **Nada de jogo, save, probe, build, instalação, deploy ou publicação nesta rodada** — tudo abaixo é
> offline/sintético rotulado. Runtime continua **NAO_EXERCITADO**. Escopo estrito: os arquivos desta
> frente + este doc. O item **C** (secundário) vai para **backlog sem bloquear**, pelo aceite #6 do
> `docs/automacao/CICLO-VALIDACAO-escopo.md:28` — ver §6. A revisão desta correção (**CIC-4R3**) é
> criada pelo **pai**; este documento não se aprova sozinho.

## 1. O que mudou, por achado

| # | regra que passou a valer | onde (arquivo:linha) |
|---|---|---|
| **A** | O critério do cenário 2 é **"feed vs tooltip"** (`docs/automacao/CIC-4-entrega.md:79-81`): sem observação da **TOOLTIP** do personagem, o critério do FEED sai **`NAO_EXERCITADO`** (nunca OK) e o ciclo **não fecha**; o `observado.feed_vs_tooltip` registra `SEM_TOOLTIP` | `tools/automacao/cenarios/tooltips_shrines.py:655` (bloco da 2ª superfície), `:685` (marca `SEM_TOOLTIP`), `:690` (a exigência), `:44` (docstring) |
| **B** | A TOOLTIP é **contra-prova** e tem de **autenticar**: mesma cadeia da rodada (`sessao` + hash confrontado com a identidade + evidência do artefato lido) **e** a **mesma sessão do FEED**. `fixture` ⇒ `NAO_EXERCITADO`; outra build ⇒ `INDETERMINADO`; outra sessão ⇒ `INDETERMINADO` | `tooltips_shrines.py:503` (`_achar_tooltip`), `:511` (`_contra_prova_autenticada`), `:682` (a comparação continua medida) |

Duas notas de desenho, para o revisor atacar se discordar:

1. **Precedência**: o defeito de **cadeia do FEED** continua à frente da ausência da contra-prova
   (`tooltips_shrines.py:686-694`) — foi o que preservou os controles negativos **N3**
   (`NAO_EXERCITADO`) e **N4** (`INDETERMINADO`) da fixture, que são FEED-only de propósito. A
   divergência medida entre as duas superfícies (**N6**) continua `REPROVADO` e vem antes de tudo.
2. **Não estendido**: a exigência da 2ª superfície vale para o critério **"feed vs tooltip"**
   (caso `atributo`). Os casos `sem_atributo` (Dwarven) e `perigo` (Flame) **não** comparam tooltip
   hoje e **não** foram ampliados — o parecer não os pede (`CIC-4R2-revisao.md:66-67`) e ampliar
   seria endurecimento secundário, que o escopo proíbe. Se o pai quiser a 2ª superfície também ali,
   é item novo, não esta correção.

## 2. Prova: o ciclo REPROVA nos bytes antigos e PASSA nos novos

Bancada fora do repo (`bench.py`, em anexo no cartão) — carrega o módulo por **texto** com
`__file__` no lugar real do produto, roda as variantes e mede **módulo + ciclo**:

```
  V0  rodada runtime COMPLETA (FEED + TOOLTIP autenticadas)   -> TEM de fechar VERDE
  V1  SEM a superficie TOOLTIP (achado A)                     -> TEM de REPROVAR
  V3  TOOLTIP declarada `fixture` (achado B)                  -> TEM de REPROVAR
  V3b TOOLTIP de OUTRA build/sessao (achado B)                -> TEM de REPROVAR
```

**Bytes antigos** (`df3258e8…`, cópia congelada `tooltips_shrines_antes.py`) — o defeito é real e
não foi inventado no teste; reproduz o V1/V3/V3b do parecer, mesmo número e mesma decisão:

```
$ python bench.py --modulo .../tooltips_shrines_antes.py --suite
MODULO .../tooltips_shrines_antes.py
[OK ] V0-completa              modulo: OK=7 com_prova_runtime=7 total=7 exit=0 | ciclo: por_mod=OK ok_vinculantes=7 falhas_automaticas=0 pendencias_humanas=0 pronto=True -> VERDE  (esperado VERDE)
[FALHA] V1-sem-tooltip           modulo: OK=7 com_prova_runtime=7 total=7 exit=0 | ciclo: por_mod=OK ok_vinculantes=7 ... pronto=True -> VERDE  (esperado VERMELHO)
      S-dois-personagens-rogue/receptor/bonus=0 OK | valor bateu com o esperado independente e a cadeia de runtime fecha (...)
      S-dois-personagens-rogue/source/bonus=100 OK | valor bateu com o esperado independente e a cadeia de runtime fecha (...)
[FALHA] V3-tooltip-fixture       modulo: OK=7 com_prova_runtime=7 total=7 exit=0 | ciclo: por_mod=OK ok_vinculantes=7 ... pronto=True -> VERDE  (esperado VERMELHO)
[FALHA] V3b-tooltip-outra-build  modulo: OK=7 com_prova_runtime=7 total=7 exit=0 | ciclo: por_mod=OK ok_vinculantes=7 ... pronto=True -> VERDE  (esperado VERMELHO)
      SUITE|REPROVOU|controle-negativo|controle negativo NAO pego: N8-sem-contra-prova-tooltip: S-dois-personagens-rogue/receptor/bonus=0 esperado=NAO_EXERCITADO obtido=OK; N9-contra-prova-de-fixture: ... obtido=OK
      SUITE|REPROVOU|sem-tooltip-nao-fecha-ok|rodada sem a superficie TOOLTIP devia NAO_EXERCITADO, veio OK (...)
      SUITE|REPROVOU|contra-prova-fixture-nao-autentica|contra-prova de fixture fechou o criterio: OK
      SUITE|REPROVOU|contra-prova-outra-build-indeterminado|tooltip de outra build devia INDETERMINADO, veio OK (...)
      SUITE|REPROVOU|contra-prova-outra-sessao-indeterminado|contra-prova de outra sessao devia INDETERMINADO, veio OK (...)
   SUITE: passaram=23 reprovaram=5
TOTAL falhas=8
RED CONFIRMADO: o modulo sob prova NAO satisfaz as regras dos achados A/B
```

**Bytes novos** (`65c0f3b2…`) — o mesmo teste, o mesmo defeito, agora **vermelho**; e a rodada
completa **restaurada** segue verde (é o ciclo que o dono tinha antes, sem falso verde):

```
$ python bench.py --modulo tools/automacao/cenarios/tooltips_shrines.py --suite
[OK ] V0-completa              modulo: OK=7 com_prova_runtime=7 total=7 exit=0 | ciclo: por_mod=OK ok_vinculantes=7 falhas_automaticas=0 pendencias_humanas=0 pronto=True -> VERDE  (esperado VERDE)
[OK ] V1-sem-tooltip           modulo: NAO_EXERCITADO=2 OK=5 com_prova_runtime=5 total=7 exit=2 | ciclo: por_mod=NAO_EXERCITADO ok_vinculantes=5 falhas_automaticas=2 pendencias_humanas=0 pronto=False -> VERMELHO  (esperado VERMELHO)
      S-dois-personagens-rogue/receptor/bonus=0 NAO_EXERCITADO | sem a superficie TOOLTIP do personagem 'ChkRA' bonus=0: o criterio e 'feed vs tooltip' e faltou a segunda superficie - NAO_EXERCITADO, nunca OK (lacun...
      S-dois-personagens-rogue/source/bonus=100 NAO_EXERCITADO | sem a superficie TOOLTIP do personagem 'Raven' bonus=100: ...
[OK ] V3-tooltip-fixture       modulo: NAO_EXERCITADO=2 OK=5 ... exit=2 | ciclo: por_mod=NAO_EXERCITADO ok_vinculantes=5 falhas_automaticas=2 pendencias_humanas=0 pronto=False -> VERMELHO  (esperado VERMELHO)
      S-dois-personagens-rogue/receptor/bonus=0 NAO_EXERCITADO | contra-prova (TOOLTIP) de 'ChkRA' NAO autenticada: procedencia='fixture' - o criterio 'feed vs tooltip' so fecha com a segunda superficie da MESMA rod...
[OK ] V3b-tooltip-outra-build  modulo: INDETERMINADO=2 OK=5 ... exit=2 | ciclo: por_mod=NAO_EXERCITADO ok_vinculantes=5 falhas_automaticas=2 pendencias_humanas=0 pronto=False -> VERMELHO  (esperado VERMELHO)
   SUITE: passaram=28 reprovaram=0
TOTAL falhas=0
GREEN CONFIRMADO: o modulo sob prova satisfaz as regras dos achados A/B
```

Leitura: nas três variantes o **fail-closed** correto é o que aparece — `NAO_EXERCITADO`/`INDETERMINADO`,
`exit=2`, `por_mod=NAO_EXERCITADO` e **0 pendências humanas** (a lacuna volta ao ciclo como falha
automática, não ao dono). Sem a correção, os três casos davam `exit=0`, `ok_vinculantes=7` e
`pronto_para_decisao=True`.

## 3. O que ficou pinado no teste (e onde o teste REPROVOU antes)

`tools/automacao/cenarios/test_tooltips_shrines.py` — suíte do produto: **28 casos, 0 reprovações**.
Quatro casos novos pinam a regra e **os quatro reprovam nos bytes antigos**:

| caso (arquivo:linha) | o que exige |
|---|---|
| `sem-tooltip-nao-fecha-ok` (`test_tooltips_shrines.py:409`) | FEED completo+identificado **sem** TOOLTIP ⇒ `NAO_EXERCITADO`, `prova_runtime=False`, `exit!=0`, `decisao` não fecha o mod e **não** gera pendência humana |
| `contra-prova-fixture-nao-autentica` (`:435`) | TOOLTIP `fixture` fecha a **comparação** (`feed_vs_tooltip=IGUAL`) e **não** o critério |
| `contra-prova-outra-build-indeterminado` (`:453`) | TOOLTIP com hash de outra build ⇒ `INDETERMINADO` |
| `contra-prova-outra-sessao-indeterminado` (`:463`) | TOOLTIP de outra sessão (mesma build) ⇒ `INDETERMINADO` |

Os dois defeitos plantados **N8** (`shrines-controle-negativo.json:115`) e **N9**
(`:138`) entram no controle negativo da suíte — que passou de 7 para **9 casos**
(`test_tooltips_shrines.py:538`) — e é exatamente o par de casos que o avaliador antigo **não**
pegava. Helpers das duas superfícies em `test_tooltips_shrines.py:125` e `:133`.

Travas rodadas (saída literal, 2026-10-06 ~14:00-14:05):

```
python tools/automacao/cenarios/test_tooltips_shrines.py          TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0   exit 0
python tools/automacao/cenarios/test_tooltips_shrines.py --isca   ISCA|OK|defeito plantado detectado: N1-... (esperado=OK obtido=REPROVADO)  exit 0
python tools/automacao/cenarios/tooltips_shrines.py --observacoes .../shrines-observacoes.exemplo.json
                                                                  OK=7 ... com prova runtime: 0                exit 2
python tools/automacao/ciclo/test_decisao.py                      total: 127 | falhas: 0                       exit 0
python tools/automacao/ciclo/test_ciclo.py                        Ran 48 tests ... OK                          exit 0
python tools/automacao/cenarios/test_rstv.py                       PASSOU (cic3-rstv)                          exit 0
```

## 4. Itens declarados 1-7, 10 e 11 reconfirmados nos bytes novos

O CIC-4R2 diz que esses itens "seguem válidos e podem ser reconfirmados"; refiz **por execução
própria** as sondas nomeadas no parecer da rodada 1 (E1-E3, C1-C3, D1, L, I, G, N7,
`reconfirma.py` em anexo):

```
  [OK ] 1-contrato-campos / estados / procedencias      obtido=todos / ['OK'] / ['fixture']
  [OK ] E1-feed-99  REPROVADO     E2-flame-40  REPROVADO     E3-flame-14  OK  (esperado 14.0, eixo Source)
  [OK ] I3-sem-identidade  NAO_EXERCITADO    I4-outra-build  INDETERMINADO
  [OK ] C1-receptor-com-40 REPROVADO   C2-source-com-20 REPROVADO   C3-bonus-trocados NAO_EXERCITADO/NAO_EXERCITADO
  [OK ] D1-feed-x-tooltip REPROVADO          L-char-combinado  NAO_EXERCITADO
  [OK ] I-sem-observacao  (OK=0, NAO_EXERCITADO=7, exit=2)
  [OK ] G-fixture-prova-runtime 0   G-fixture-exit 2   G-decisao-sem-prova (ok_vinculantes=0, nao_conta_como_prova=7, pronto=False)
  [OK ] N7-regressao  ('REPROVADO', reabre_bug=False, 'BUG-34')
  [OK ] 11-sem-pedido-humano  nenhum motivo empurra tarefa automatizavel ao dono
TOTAL itens com divergencia=0
```

**Item 12 / R3 (fonte, oráculo e tabelas intactos)** — medido depois da correção: `sha256` de
`tools/checa_shrines.py` (`a000cc17…`), `tools/testes/regras_shrine.py` (`1ef67649…`),
`tools/gera_shrines_esperado.py` (`d58ee0c9…`), `tools/dados/shrines-esperado.csv` (`836f2833…`) e
`tools/dados/shrines-percentuais.csv` (`99174e00…`) — **idênticos** aos declarados no
`docs/automacao/CIC-4R2-revisao.md:40-44`. Os consumidores `tools/automacao/ciclo/decisao.py` e
`test_decisao.py` seguem nos bytes que o parecer leu (`d6de959e…` / `d6a1b1e9…`); o
`tools/automacao/ciclo/ciclo.py` **derivou por outra frente** (`690e40bf…` ≠ `169c8084…` do parecer)
— fora desta frente, cujos arquivos não o importam.

## 5. Arquivos e sha256 (bytes escritos nesta rodada)

```
65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199  tools/automacao/cenarios/tooltips_shrines.py
8fcba1c3ba8af9ff8bcf4b3db115a333e6799d364ea3fe8102cfbf971b9df885  tools/automacao/cenarios/test_tooltips_shrines.py
3f934a8c8bd0f3ee9a812cf23a024fca52f226247515c9a68319a0485b62a671  tools/automacao/cenarios/shrines-controle-negativo.json
6ef205481d874a3587d07ca433b41565eef29f3323a14259c978cde263f77c52  tools/automacao/cenarios/shrines-casos.json             (inalterado)
969b1c693956ee1c3f2de4a3ccb42a9724f502f623d91bd71030867a5e23cdec  tools/automacao/cenarios/shrines-observacoes.exemplo.json (inalterado)
```

Bytes de partida (cópia congelada usada na prova RED, sha declarado no parecer):
`df3258e841f7ca9f3f81f41b277f69c63c08b0d4308dcd7c4412afff9b2ddbef` (`tooltips_shrines.py`) e
`0b6436783a9c779d37c970a88af34b3af4d5d365b73b70f88e74bb698b1ced95` (`test_tooltips_shrines.py`).
Os sha256 que o `docs/automacao/CIC-4-entrega.md:140-144` declara para esses dois arquivos passam a
ser **históricos** (aquela entrega é o estado anterior a esta correção; nada foi reescrito lá).

Não tocados: `shrine`-casos/exemplo, `tools/checa_shrines.py`, `tools/testes/regras_shrine.py`,
`tools/gera_shrines_esperado.py`, `tools/dados/**`, `tools/automacao/ciclo/decisao.py`,
`tools/automacao/ciclo/ciclo.py`, `tools/automacao/cenarios/rstv.py`, produto, probe e bancada.

Nota de leitura: o `docs/automacao/CIC-4-entrega.md` declara **24 casos** e **7 defeitos plantados**
(`:46`, `:120`, `:133-135`) — números do estado **anterior** a esta correção; a suíte passa a ter
**28 casos** e **9 controles negativos** (§3). Aquele documento não foi reescrito (o parecer CIC-4R2
ancora nele), como já foi feito no `COR-CIC3-correcao.md:164-167` para a entrega do CIC-3.

## 6. Item C — backlog (aceite #6), sem bloquear

O achado **C** (`docs/automacao/CIC-4R2-revisao.md:68`) fica **em backlog**, com o escopo do que
seria preciso, para o pai decidir a vaga (o parecer já o classifica como **menor**):

1. **`evidencia` declarada não é validada**: `_evidencia_obs` (`tooltips_shrines.py:580`) devolve os
   caminhos declarados **crus**; só `objeto` é conferido contra o disco. Uma rodada pode declarar
   `tools/dados/nao-existe.log` e o **módulo** ainda sai `exit 0`, enquanto o `decisao.py` reprova
   (`V2c` do parecer). O caso negativo não está pinado.
2. **`evidencia` apontando para o esperado ou para o produto** (`V2`/`V2d`) segue aceito como
   `OK_VINCULANTE` — o rótulo "artefato lido" não vale nesses dois casos.

Nada disso foi corrigido aqui: o cartão pede **A e B** e manda tratar C pelo aceite #6. Nenhum
critério de trava foi enfraquecido nesta correção — toda mudança **endurece** (nenhuma capacidade
passa a fechar OK com menos prova do que antes).

## 7. Limites e residual

* **Runtime NAO_EXERCITADO**: nenhum jogo, save, probe, build, install ou publicação. As variantes
  V0/V1/V3/V3b são **sintéticas e rotuladas** — elas medem o **avaliador e o ciclo**, não o jogo.
* **Revisão independente**: quem revisa esta correção é outra tarefa (**CIC-4R3**), criada pelo
  **pai**. Este documento não se aprova; nada foi aprovado nem publicado.
* Evidência bruta anexada ao cartão `t_278bbb07`: `bench.py`, `reconfirma.py`,
  `tooltips_shrines_antes.py` (bytes congelados), `saida_antes.txt`, `saida_antes_suite.txt`,
  `saida_depois.txt`, `saida_reconfirma.txt` — o revisor reproduz rodando os dois comandos da §2.
