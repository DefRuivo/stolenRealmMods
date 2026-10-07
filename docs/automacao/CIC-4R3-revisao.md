# CIC-4R3 — revisão independente do COR-CIC4 (2ª superfície e contra-prova autenticada) — `t_9f5f2a53`

Revisor: worker `default`, run 427 (tarefa `t_9f5f2a53`), **não autor**: o produto revisado é do
`t_278bbb07` (COR-CIC4) e o parecer que o originou é do `t_fa36c892` (CIC-4R2). Revisão **por
execução**, não por leitura de relatório: cada veredito abaixo tem comando, saída literal e exit code
reais, medidos em 2026-10-06 ~14:35–14:50.

O que **não** foi feito nesta rodada, por regra do projeto (`.hermes.md`) e do cartão: nada de jogo,
save, probe, build, instalação, deploy, publicação, `git add`, edição do produto, enfraquecimento de
trava, `Assembly-CSharp.dll` ou qualquer coisa de Bard. Nada foi mutado no Kanban do produto — este
documento **registra** o veredito; quem o aplica é o **pai**.

Escritas desta rodada (únicas): **este documento** e `docs/automacao/CIC-4R3-evidencias/` (saídas
literais). Bancadas rodadas em **caminho de cópia fora do repo**
(`…/hermes/kanban/workspaces/t_9f5f2a53/bench/`), nunca dentro dele.

Método: (1) medir os bytes do disco; (2) rodar a suíte, a isca, a CLI e os consumidores; (3) refazer
a medição nos dois sentidos (bytes antigos × novos) com **sonda própria** (não só a bancada do autor);
(4) **caso negativo obrigatório** — neutralizar a trava em cópia fora do repo e mostrar o ciclo
vermelho; (5) tentar refutar cada uma das 4 afirmações do autor; (6) declarar o que ficou por medir.

---

## (a) Estado lido — sha256 medido por mim

Medido com `sha256sum` nos bytes do disco, **antes** de qualquer execução (`git status` do repo não
foi alterado por esta rodada; os arquivos desta frente estão com mtime de 14:00–14:06, nenhum
tocado desde então):

```
65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199  tools/automacao/cenarios/tooltips_shrines.py
8fcba1c3ba8af9ff8bcf4b3db115a333e6799d364ea3fe8102cfbf971b9df885  tools/automacao/cenarios/test_tooltips_shrines.py
3f934a8c8bd0f3ee9a812cf23a024fca52f226247515c9a68319a0485b62a671  tools/automacao/cenarios/shrines-controle-negativo.json
6ef205481d874a3587d07ca433b41565eef29f3323a14259c978cde263f77c52  tools/automacao/cenarios/shrines-casos.json             (inalterado)
969b1c693956ee1c3f2de4a3ccb42a9724f502f623d91bd71030867a5e23cdec  tools/automacao/cenarios/shrines-observacoes.exemplo.json (inalterado)
8bc29b5729be6de5cb082e51cc7414d9b935ea9e445f9911078f49e5113839f2  docs/automacao/COR-CIC4-correcao.md
a000cc178b2f93007dbf8c948ca553a1c8e9593e37aca52177bcde82e6900296  tools/checa_shrines.py            (fonte/oráculo, intacto)
1ef67649463eeab2b113f1423c8c6667ff24b9162c89633608e6c2a51bf9c562  tools/testes/regras_shrine.py      (oráculo, intacto)
d58ee0c931fb5efdff08189f48cbb4085a06c0fc03072c9f3fb9dcae83de5dcc  tools/gera_shrines_esperado.py    (fonte, intacta)
836f2833d2ef50e0ee14aaebe17b551f9ed7f6a09fc029771ffced5c048824ce  tools/dados/shrines-esperado.csv   (gerado)
99174e006dd7d70560142012d1d752ce7b43113d68751c7b47f7836929e549b2  tools/dados/shrines-percentuais.csv (gerado)
d6de959e73a090e43da2b5438a12ba1739d32be2bd9494c0fe9f0d84d9163933  tools/automacao/ciclo/decisao.py      (CIC-2, consumidor)
d6a1b1e9a7b987b6e5d18e9b3fe3122afadab77f76707f786f76cb7d33c06205  tools/automacao/ciclo/test_decisao.py (não editado)
690e40bf7b274d7c7804f8185a67764755cd96918d2f695cfadbf887e79bfac1  tools/automacao/ciclo/ciclo.py        (CIC-1; derivou em outra frente)
6467698a6a893f16663ab2a725f1775e8c32edd609c8c45c89f5c32656acb0c1  docs/automacao/CIC-4-entrega.md       (o declarado a cumprir; não reescrito)
b72889239c21ca1483a9eece8ddd35e9916a12ce7b81f701308653940fd6be4e  docs/automacao/CIC-4R2-revisao.md     (parecer de origem)
b063dfef3c359bde7bee340b5cd527b1f547903080afebdbf73b5edb2510d3b2  docs/automacao/CICLO-VALIDACAO-escopo.md
```

Confronto com o que o autor declara (`COR-CIC4-correcao.md` §5) e com o que o CIC-4R2 mediu
(`CIC-4R2-revisao.md:31-48`): **idênticos nos três arquivos do produto**, idênticos também nos cinco
itens do "item 12 / R3" (fonte, oráculo, gerador e os dois CSVs) e nos dois consumidores. O
`ciclo.py` **derivou** (`690e40bf…` ≠ `169c8084…` do parecer) — o autor declara isso (§4) e o módulo
desta frente não o importa; confirmei por `grep`: `tooltips_shrines.py` só importa
`checa_shrines`/`regras_shrine`/tabelas, não o orquestrador.

Bytes congelados usados na prova RED (anexo do cartão `t_278bbb07`) — medidos por mim:

```
df3258e841f7ca9f3f81f41b277f69c63c08b0d4308dcd7c4412afff9b2ddbef  tooltips_shrines_antes.py      (= 65c0f3b2 "antes"; confere)
0d60f709d4252d9ff59a08bb1f5e2d4c0697b128601c60f0e538bde57ea6857a  shrines-controle-negativo.antes.json (7 casos)
fdc0a5e108e0326102cdc5041186edd258af5cc76af759bfae7b841cdce77f4e  bench.py
1a7c3567bfd7d5b8fca7a2c16420e297a1e43f4461a60dc16e11b933b7a2b616  reconfirma.py
```

Contagem de controles negativos por execução própria do JSON: **antes = 7** (`N1…N7`), **atual = 9**
(`N1…N9`, com `N8-sem-contra-prova-tooltip` e `N9-contra-prova-de-fixture` novos em
`tools/automacao/cenarios/shrines-controle-negativo.json:115` e `:138`).

**Diff antes→depois é puramente aditivo** (evidência `11-diff-antes-depois.txt`): docstring do
cenário 2 (:44), os dois helpers `_achar_tooltip` (:503) e `_contra_prova_autenticada` (:511), as
marcas `observado.feed_vs_tooltip` (:682 `IGUAL`, `:685` `SEM_TOOLTIP`, mais `DIVERGE`/`TOOLTIP_SEM_ITEM`)
e as duas guardas novas (:690 e :696). **Nenhuma linha removida, nenhuma trava afrouxada** — era o
risco número um a procurar (§ "Regras do projeto": enfraquecer trava é o pior defeito possível) e ele
**não** ocorreu.

---

## (b) Comandos exatos, saída literal e exit code

Saídas completas em `docs/automacao/CIC-4R3-evidencias/` (nome do arquivo citado em cada item).
Bancada em `…/hermes/kanban/workspaces/t_9f5f2a53/bench/` (cópia fora do repo).

### 1. Suíte do produto — 28/28, exit 0 (`01-suite-produto.txt`)

```
$ python tools/automacao/cenarios/test_tooltips_shrines.py
RESULTADO|PASSOU|sem-tooltip-nao-fecha-ok|ok
RESULTADO|PASSOU|contra-prova-fixture-nao-autentica|ok
RESULTADO|PASSOU|contra-prova-outra-build-indeterminado|ok
RESULTADO|PASSOU|contra-prova-outra-sessao-indeterminado|ok
TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0
EXIT=0
```

### 2. Isca (prova de fogo do próprio teste) — exit 0 (`02-isca.txt`)

```
$ python tools/automacao/cenarios/test_tooltips_shrines.py --isca
ISCA|OK|defeito plantado detectado: N1-dois-personagens-somados: S-dois-personagens-rogue/receptor/bonus=0 esperado=OK obtido=REPROVADO
EXIT=0
```

`t_controle_negativo` também exige **9** controles (`test_tooltips_shrines.py:538`) e passa — os 9
defeitos plantados são pegos com o estado certo.

### 3. CLI só-fixture — nada de verde, exit 2 (`03-cli-fixture.txt`)

```
$ python tools/automacao/cenarios/tooltips_shrines.py --observacoes tools/automacao/cenarios/shrines-observacoes.exemplo.json
  OK=7, REPROVADO=0, NAO_EXERCITADO=0, INDETERMINADO=0
  com prova runtime: 0  · exit=2
EXIT=2
```

### 4. Medição nos dois sentidos (`04-bench-antes-RED.txt`, `05-bench-depois-GREEN.txt`)

```
$ python …/bench/bench.py --modulo …/attachments/t_278bbb07/tooltips_shrines_antes.py --suite
MODULO …/tooltips_shrines_antes.py
[OK ]    V0-completa              … exit=0 | ciclo: por_mod=OK ok_vinculantes=7 … pronto=True -> VERDE
[FALHA]  V1-sem-tooltip           … exit=0 | ciclo: por_mod=OK ok_vinculantes=7 … pronto=True -> VERDE  (esperado VERMELHO)
[FALHA]  V3-tooltip-fixture       … exit=0 | ciclo: por_mod=OK ok_vinculantes=7 … pronto=True -> VERDE  (esperado VERMELHO)
[FALHA]  V3b-tooltip-outra-build  … exit=0 | ciclo: por_mod=OK ok_vinculantes=7 … pronto=True -> VERDE  (esperado VERMELHO)
   SUITE: passaram=23 reprovaram=5
TOTAL falhas=8
RED CONFIRMADO: o modulo sob prova NAO satisfaz as regras dos achados A/B
EXIT=1
```

```
$ python …/bench/bench.py --modulo C:/dev/stolen-realm/tools/automacao/cenarios/tooltips_shrines.py --suite
[OK ] V0-completa              modulo: OK=7 com_prova_runtime=7 total=7 exit=0 | por_mod=OK ok_vinculantes=7 pronto=True -> VERDE
[OK ] V1-sem-tooltip           modulo: NAO_EXERCITADO=2 OK=5 exit=2 | por_mod=NAO_EXERCITADO ok_vinculantes=5 falhas_automaticas=2 pendencias_humanas=0 pronto=False -> VERMELHO
      S-dois-personagens-rogue/receptor/bonus=0 NAO_EXERCITADO | sem a superficie TOOLTIP do personagem 'ChkRA' bonus=0: o criterio e 'feed vs tooltip' e faltou a segunda superficie - NAO_EXERCITADO, nunca OK
[OK ] V3-tooltip-fixture       modulo: NAO_EXERCITADO=2 OK=5 exit=2 | por_mod=NAO_EXERCITADO … pronto=False -> VERMELHO
      S-dois-personagens-rogue/receptor/bonus=0 NAO_EXERCITADO | contra-prova (TOOLTIP) de 'ChkRA' NAO autenticada: procedencia='fixture' - o criterio 'feed vs tooltip' so fecha com a segunda superficie da MESMA rodada de runtime
[OK ] V3b-tooltip-outra-build  modulo: INDETERMINADO=2 OK=5 exit=2 | por_mod=NAO_EXERCITADO … pronto=False -> VERMELHO
   SUITE: passaram=28 reprovaram=0
GREEN CONFIRMADO: o modulo sob prova satisfaz as regras dos achados A/B
EXIT=0
```

### 5. Sonda própria do revisor — mesmos números, código independente (`06-sonda-independente.txt`)

Escrevi uma sonda nova (não reusa o `bench.py` do autor; carrega o módulo por caminho e monta as
observações do zero) e rodei **nos dois sentidos**. Exit `1` no primeiro (divergências nos bytes
antigos), exit `0` no segundo:

```
$ python …/bench/cic4r3_probe.py                       (bytes NOVOS 65c0f3b2)
  P8-completa-OK               estado=OK              prova_runtime=True  exit=2  feed_vs_tooltip=IGUAL
  P1-feed-vs-tooltip-DIVERGE   estado=REPROVADO       prova_runtime=False exit=1  feed_vs_tooltip=DIVERGE
  P2-sem-tooltip               estado=NAO_EXERCITADO  prova_runtime=False exit=2  feed_vs_tooltip=SEM_TOOLTIP
  P3-tooltip-fixture           estado=NAO_EXERCITADO  prova_runtime=False exit=2  feed_vs_tooltip=IGUAL
  P4-tooltip-outra-build       estado=INDETERMINADO   prova_runtime=False exit=2  feed_vs_tooltip=IGUAL
  P5-tooltip-outra-sessao      estado=INDETERMINADO   prova_runtime=False exit=2  feed_vs_tooltip=IGUAL
  P6-sem-tooltip+feed-sem-hash estado=NAO_EXERCITADO  prova_runtime=False exit=2  (precedencia da cadeia do FEED)
  P7-sem-tooltip+feed-hash-errado estado=INDETERMINADO prova_runtime=False exit=2 (precedencia da cadeia do FEED)
DIVERGENCIAS: []      EXIT=0
```

```
$ python …/bench/cic4r3_probe.py --modulo …/tooltips_shrines_antes.py    (bytes ANTIGOS df3258e8)
  P2-sem-tooltip               estado=OK              prova_runtime=True    <- ACHADO A reproduzido por sonda própria
  P3-tooltip-fixture           estado=OK              prova_runtime=True    <- ACHADO B (fixture)
  P4-tooltip-outra-build       estado=OK              prova_runtime=True    <- ACHADO B (outra build)
  P5-tooltip-outra-sessao      estado=OK              prova_runtime=True    <- ACHADO B (outra sessão)
ESTADOS: ['OK', 'REPROVADO', 'OK', 'OK', 'OK', 'OK', 'NAO_EXERCITADO', 'INDETERMINADO']
DIVERGENCIAS: [2, 3, 4, 5]      EXIT=1
```

### 6. Consumidores (travas de integração) — exit 0 cada (`08-consumidores.txt`)

```
$ python tools/automacao/ciclo/test_decisao.py    total: 127 | falhas: 0        EXIT=0
$ python tools/automacao/ciclo/test_ciclo.py      Ran 48 tests in 23.053s  OK  EXIT=0
$ python tools/automacao/cenarios/test_rstv.py    RESULTADO|PASSOU|cic3-rstv|… EXIT=0
```

### 7. Itens 1–7, 10 e 11 do CIC-4R (`09-reconfirma.txt`)

```
$ python …/bench/reconfirma.py
  [OK ] E1-feed-99 REPROVADO   E2-flame-40 REPROVADO   E3-flame-14 OK (14.0, 'Source')
  [OK ] I3-sem-identidade NAO_EXERCITADO   I4-outra-build INDETERMINADO
  [OK ] D1-feed-x-tooltip REPROVADO        N7-regressao ('REPROVADO', False, 'BUG-34')
  [OK ] 11-sem-pedido-humano  nenhum
TOTAL itens com divergencia=0        EXIT=0
```

---

## (c) Caso negativo obrigatório — a trava é load-bearing (`07-negativo-obrigatorio.txt`)

Exigido pelo cartão de correção ("remover a superfície TOOLTIP tem de deixar o ciclo VERMELHO").
Feito em **cópia fora do repo**, sem tocar o produto:

1. cópia fiel do módulo → `…/bench/copia/tooltips_shrines_copia.py`
   (sha `65c0f3b2…` = **IDENTICA** ao produto);
2. cópia **neutralizada** → `…/bench/copia/tooltips_shrines_neutro.py`
   (sha `a7c11da1…`), desligando a guarda do achado A (`:690`) e a autenticação do achado B (`:520`);
3. medir; 4. restaurar (a cópia fiel) e medir de novo.

```
$ python …/bench/neutro.py
PRODUTO  65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199  …/tooltips_shrines.py
COPIA    65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199  …/copia/tooltips_shrines_copia.py  (copia fiel: IDENTICA)
NEUTRO   a7c11da176df3a3c2bc6ad818221f1123988b94b7d68bca84be1c182a5cc1c4e  …/copia/tooltips_shrines_neutro.py
tooltips_shrines_neutro.py:520:     return (None, None)  # NEUTRALIZADO CIC-4R3 - achado B … desligada
tooltips_shrines_neutro.py:691:         if False:  # NEUTRALIZADO CIC-4R3 - achado A … desligada

$ python …/bench/bench.py --modulo …/copia/tooltips_shrines_neutro.py --suite
[FALHA] V1-sem-tooltip          … por_mod=OK ok_vinculantes=7 pronto=True -> VERDE  (esperado VERMELHO)
[FALHA] V3-tooltip-fixture      … por_mod=OK ok_vinculantes=7 pronto=True -> VERDE  (esperado VERMELHO)
[FALHA] V3b-tooltip-outra-build … por_mod=OK ok_vinculantes=7 pronto=True -> VERDE  (esperado VERMELHO)
   SUITE: passaram=23 reprovaram=5
TOTAL falhas=8
RED CONFIRMADO …        EXIT=1

$ python …/bench/bench.py --modulo …/copia/tooltips_shrines_copia.py --suite
[OK ] V1-sem-tooltip  NAO_EXERCITADO=2 OK=5 exit=2 · V3 NAO_EXERCITADO=2 · V3b INDETERMINADO=2
   SUITE: passaram=28 reprovaram=0
TOTAL falhas=0
GREEN CONFIRMADO …      EXIT=0
```

Leitura: **com a trava, VERMELHO (exit 1); sem a trava, VERDE (exit 0) — na mesma build, no mesmo
harness, na mesma rodada.** A correção é o que separa o ciclo do falso verde; não é artefato dos
bytes congelados do autor (a minha sonda própria chegou ao mesmo resultado de forma independente).

---

## (d) Veredito por item

### Item A — "superfície TOOLTIP ausente não vira `NAO_EXERCITADO`" → **OK (com prova)**

* Regra declarada: `docs/automacao/CIC-4-entrega.md:79-81` e `tooltips_shrines.py:44`.
* Implementação: `tooltips_shrines.py:690` (o FEED sem tooltip deixa de fechar OK) + `:685`
  (`observado.feed_vs_tooltip = "SEM_TOOLTIP"`).
* Prova por execução própria: `P2` → `NAO_EXERCITADO`, `prova_runtime=False`, `exit=2`; bench `V1` nos
  bytes novos → `por_mod=NAO_EXERCITADO`, `ok_vinculantes=5`, `falhas_automaticas=2`,
  **`pendencias_humanas=0`**, `pronto_para_decisao=False`. Nos bytes antigos a mesma rodada dava
  `OK`/`exit=0`/`pronto=True` — **defeito A reproduzido e fechado**.
* A lacuna volta **ao ciclo** (falha automática, fila de agente), não ao dono — conforme
  `CICLO-VALIDACAO-escopo.md:32`.
* Nenhum critério fecha OK com a dimensão não lida **no caso em que a dimensão é declarada**
  (`S-dois-personagens-rogue`, receptor e source). Ver (e) para a fronteira declarada.

### Item B — "a contra-prova (tooltip) não é autenticada" → **OK (com prova)**

* Implementação: `_contra_prova_autenticada` (`tooltips_shrines.py:511`) exige procedência `runtime`,
  a mesma cadeia (`sessao` + hash confrontado com a identidade + evidência do artefato lido) **e** a
  mesma sessão do FEED; `_achar_tooltip` (`:503`) é o único ponto de busca da 2ª superfície.
* Prova por execução própria: `P3` tooltip `fixture` → **`NAO_EXERCITADO`** (e `feed_vs_tooltip=IGUAL`
  — a *comparação* continua sendo medida, o *critério* é que não fecha); `P4` outra build →
  **`INDETERMINADO`**; `P5` outra sessão → **`INDETERMINADO`**. Nos bytes antigos os três davam
  `OK`/`prova_runtime=True`.
* Item 7 preservado: rodada de fixture nunca ganha `prova_runtime=True` (`C4` da sonda 2:
  `OK` com `prova_runtime=False`, `com_prova_runtime=0`).
* Nota de rigor no código (não é defeito): a checagem de sessão (`:533`) só compara quando **as duas**
  sessões são não-vazias — mas `_contra_prova_autenticada` só é alcançada com `estado=="OK"`, o que já
  implica `_cadeia_runtime` aprovado para o FEED **e** para a TOOLTIP, e essa cadeia recusa sessão
  vazia (`tooltips_shrines.py:460`). Logo não há caminho em que a sessão ausente escape.

### Afirmações do autor — tentativa de refutação, uma a uma

| # | afirmação | veredito | prova |
|---|---|---|---|
| 1 | sem tooltip ⇒ `NAO_EXERCITADO`; fixture ⇒ `NAO_EXERCITADO`; outra build/sessão ⇒ `INDETERMINADO` | **CONFIRMADO** | `P2/P3/P4/P5` da sonda própria + `V1/V3/V3b` do bench (saída acima) |
| 2 | divergência segue `REPROVADO` e a cadeia do FEED mantém precedência (N3/N4) | **CONFIRMADO** | `P1` → `REPROVADO`/`exit=1`; `P6` → `NAO_EXERCITADO` e `P7` → `INDETERMINADO` **mesmo sem tooltip** (o defeito de cadeia vem antes); `N3`/`N4` do controle negativo seguem sendo pegos (suíte 28/28) |
| 3 | suíte 28/28, 9 controles negativos (N8/N9 novos), isca reprovando | **CONFIRMADO** | `01/02` acima; contagem por leitura do JSON: 7 → 9; `test_tooltips_shrines.py:538` exige 9 |
| 4 | medição nos dois sentidos com os mesmos números (23/5 × 28/28) | **CONFIRMADO** | `04/05/06` acima, com sonda **independente** do harness do autor |

Nenhuma das quatro foi refutada. Não encontrei divergência entre o que o relatório afirma e o que a
execução devolve.

---

## (e) Lacunas declaradas — o que NÃO é OK

1. **Runtime real continua `NAO_EXERCITADO`.** Nada de jogo, save, probe ou ferramenta viva: as
   variantes são **sintéticas e rotuladas** e medem o **avaliador e o ciclo**, não o campo. Nenhuma
   conclusão de gameplay sai daqui.
2. **Fronteira declarada pelo autor, medida por mim (`10-sonda2-fronteira.txt`).** A exigência da 2ª
   superfície vale só para o critério **"feed vs tooltip"** (caso `atributo`). Numa rodada de runtime
   completa **sem nenhuma tooltip de personagem**, os outros critérios seguem
   `OK`/`prova_runtime=True`:
   `S-dois-personagens-dwarven/chkdw0|chkdw20|chkdw` (3) + `S-perigo-flame/ChkGob` +
   `S-regressao-bug34-armor` = **5 OK com prova de runtime**; só `S-dois-personagens-rogue/receptor|source`
   saem `NAO_EXERCITADO`. Esses cinco **não carregam** o campo `observado.feed_vs_tooltip` — eles não
   comparam tooltip, então a dimensão não está declarada neles. É a mesma fronteira que o próprio
   relatório declara (`COR-CIC4-correcao.md` §1, nota 2: "não estendido").
   **Ressalva de redação, para o pai decidir:** o texto do cenário 2 no entregável
   (`CIC-4-entrega.md:79-81`) é genérico — "O valor do **FEED** … e o da **TOOLTIP** … têm de bater
   entre si … Faltando uma superfície, o que falta sai `NAO_EXERCITADO`" — e não enumera a quais casos
   se aplica. Pelo cartão eu **não amplio** o escopo e **não reprovo** por isso (o parecer CIC-4R2
   ancorou o achado A em `_caso_atributo`, `CIC-4R2-revisao.md:71-77`); registro a assimetria como
   **decisão em aberto do pai** (esticar a exigência para Dwarven/Flame é item novo, não esta
   correção). Idem para a observação **combinada** (`C1`): um mesmo objeto com `feed` + `personagem` +
   `texto_renderizado` satisfaz as duas superfícies — é medição legítima (mesma cadeia), mas vale
   saber que o contrato não exige dois objetos distintos.
3. **Item C (backlog) — estado do registro.** O achado C (`CIC-4R2-revisao.md:68`) está documentado
   com escopo em `COR-CIC4-correcao.md` §6 (as duas metades: `_evidencia_obs` não valida caminho
   declarado; `evidencia` apontando para o esperado/produto). O `KANBAN.md:9` registra que "item C vai
   para backlog sem bloquear" — mas **não existe ainda linha própria na seção "🔵 Backlog"**
   (`KANBAN.md:21`), que só tem itens antigos arquivados. Como `KANBAN.md` é escrito **só pelo pai**
   (`CICLO-VALIDACAO-escopo.md:13`), a vaga é dele; **isto não é repro** (aceite #6:
   `CICLO-VALIDACAO-escopo.md:28`). Estado: **documentado; não registrado como item de backlog**.
4. **Documento do entregável desatualizado de propósito.** `CIC-4-entrega.md:46` ainda declara "24
   casos" e "7 defeitos plantados" (`:133-135`); a suíte agora tem 28 e 9. O autor explica (§5, nota de
   leitura) que o CIC-4R2 ancora nesse documento e ele não foi reescrito — mesma prática do
   `COR-CIC3-correcao.md`. Registro como **lacuna de documento**, não de produto.
5. **Revisão de UI/UX não se aplica** (ferramenta offline, sem tela) e o **DoD de mod não entra** —
   isto não é mod e não houve publicação.

---

## (f) Veredito final

**APROVADO** para o que esta correção se propôs: fechar os achados **A** e **B** do parecer CIC-4R2
**no produto**, com prova de que a trava é load-bearing (vermelho sem ela, verde com ela) e sem
enfraquecer nenhuma trava existente.

O que falta — e **não** é desta correção (declarado, nunca OK):

* verificação em jogo / rodada de runtime real: **`NAO_EXERCITADO`** (gate separado);
* publicação: não houve e não podia haver nesta rodada;
* item **C**: documentado em `COR-CIC4-correcao.md` §6, ainda **sem linha própria no backlog** do
  `KANBAN.md` (vaga do pai);
* decisão do pai sobre esticar a exigência da 2ª superfície a `Dwarven`/`Flame` (hoje 5 critérios
  fecham `OK`+`prova_runtime` sem tooltip, por desenho declarado).

Esta revisão **não fecha o DoD** de nada, **não publica**, **não instala** e **não muta o Kanban do
produto**; ela apenas registra, por item, o que foi medido.

### Travas de documento (repo) — `12-travas-documento.txt`

Rodei as duas travas de documento do repositório para medir o efeito **deste** documento (o CIC-4R2
rodou as mesmas duas):

```
$ python tools/audita_docs.py
!! 4 PENDENCIAS:
   - docs/README.md: o titulo de docs/cobertura/revisao diz 48 relatorios, a pasta tem 51
   - docs/README.md: o relatorio …/RSTV-26R-revisao.md nao esta listado no indice
   - docs/README.md: o relatorio …/RSTV-27R-body.md nao esta listado no indice
   - docs/README.md: o relatorio …/RSTV-27R-revisao.md nao esta listado no indice
EXIT=1
$ python tools/checa_citacoes.py
checa_citacoes: 174 citacao(oes)/mencao(oes) de arquivo em 127 documento(s) - 170 conferidas, 4 pendencia(s)
   - docs/automacao/AUT-4-preparacao.md:56 cita …/AUT4ProbePlugin.cs (nao existe)
   - docs/cobertura/revisao/RSTV-27R-body.md:15 cita …Assembly-CSharp.decompiled.cs (nao existe)
   - docs/cobertura/revisao/RSTV-27R-revisao.md:32 cita …Assembly-CSharp.decompiled.cs (nao existe)
   - docs/cobertura/revisao/RSTV-27R-revisao.md:32 cita um dump decompilado do RSTV-26 (nao existe)
EXIT=1
```

**Nenhuma das pendências é deste documento**: todas são **pré-existentes e fora desta frente** (índice
do `docs/README.md` e os arquivos do RSTV-27R, já vivos antes desta rodada; a do
`AUT-4-preparacao.md:56` é a mesma que o CIC-4R2 registrou). O `checa_citacoes` conferiu 174 citações
em 127 documentos e as citações novas desta revisão — `tooltips_shrines.py:44/460/503/511/533/682/685/690/696`,
`test_tooltips_shrines.py:125/133/409/435/453/463/538`, `shrines-controle-negativo.json:115/138`,
`CIC-4-entrega.md:79-81`, `CIC-4R2-revisao.md:66-68`, `CICLO-VALIDACAO-escopo.md:13/28` — **passaram
todas** (li cada uma no disco antes de citar).

## Evidência desta rodada (`docs/automacao/CIC-4R3-evidencias/`)

| arquivo | o que contém |
|---|---|
| `01-suite-produto.txt` | suíte 28/28 + exit |
| `02-isca.txt` | isca do próprio teste |
| `03-cli-fixture.txt` | CLI só-fixture (exit 2) |
| `04-bench-antes-RED.txt` | bench nos bytes antigos (RED, exit 1) |
| `05-bench-depois-GREEN.txt` | bench nos bytes novos (GREEN, exit 0) |
| `06-sonda-independente.txt` | sonda própria, nos dois sentidos |
| `07-negativo-obrigatorio.txt` | cópia fiel × cópia neutralizada (VERDE × VERMELHO) |
| `08-consumidores.txt` | `test_decisao.py` / `test_ciclo.py` / `test_rstv.py` |
| `09-reconfirma.txt` | itens 1–7/10/11 do CIC-4R |
| `10-sonda2-fronteira.txt` | cantos + fronteira declarada (5 OK sem tooltip) |
| `11-diff-antes-depois.txt` | diff aditivo antes→depois do módulo |

Scripts do revisor (cópia em `docs/automacao/CIC-4R3-evidencias/`; as bancadas rodaram fora do repo, em
`…/hermes/kanban/workspaces/t_9f5f2a53/bench/`): `cic4r3_probe.py`, `cic4r3_probe2.py`, `neutro.py` —
reproduzem tudo acima sem tocar o produto. `bench.py` e `reconfirma.py` são os anexos do cartão
`t_278bbb07` (sha medido por mim em (a)).
