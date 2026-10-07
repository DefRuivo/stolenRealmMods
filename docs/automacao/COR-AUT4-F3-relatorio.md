# COR-AUT4-F3 — endurecer a FORMA de `evidencia_runtime` no `consolidar_probe`

Objeto: **COR-AUT4-F3** (`t_dbb4a228`) — ressalva **não bloqueante** da revisão independente
**COR-AUT4-F2R** (`t_57dc92bc`, `docs/automacao/COR-AUT4-F2R-revisao.md` §5): `consolidar_probe`
decidia com `evidencia_runtime is False`, então um artefato que trouxesse a **string** `"false"`
(ou `0`, `"0"`, `null`) escapava do `is False` e era consolidado como **runtime** — a forma errada
CONFIRMAVA em vez de ser recusada (mesma classe do A2 da COR-AUT4-F2: forma que o jogo não produz
passando como válida).

Autor: agente `default`. Data: **2026-10-06**.
Escopo: **só bytes + execução OFFLINE sobre cópias fora do repo**
(`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4f3/`). Nenhum jogo aberto/encerrado, nenhum
save tocado, nenhum probe instalado, nenhum deploy, nenhum build, nenhum commit/push, nenhum `git add`.
Nada tocado em `tools/automacao/estilo/**`, `tools/automacao/aceite/**`, `RoguelikeSkillTreeVisualizer/**`,
`BetterTooltips/**` nem `lib/Assembly-CSharp.dll`.

---

## 0. Veredito por item

| item | veredito | uma linha |
|---|---|---|
| Recusar string `"false"` / `0` / `"0"` / `null` | **OK (com prova)** | qualquer forma PRESENTE ≠ bool `True` → `FIXTURE`/exit 2; nunca `CONFIRMADA` (borda medida base×fix) |
| Não quebrar o caminho feliz (bool `True`) | **OK (com prova)** | `evidencia_runtime: true` → `CONFIRMADA`/exit 0 (controle positivo na suíte) |
| Regressão com a FORMA ERRADA de verdade | **OK (com prova)** | `t_aut4_costura_probe.py` usa `"false"`/`0`/`"0"`/`null` reais; isca nova idem |
| Contra-prova (defeito plantado → VERMELHO) | **OK (com prova)** | `is False` cru em cópia fora do repo → suite exit 1 e contra-prova exit 1 |
| Suite completa verde | **OK (com prova)** | `roda_testes_runtime.py` → 9/9 exit 0; `--contra-prova` → 16/16 exit 0 |
| Não-regressão dos 4 consumidores | **OK (com prova)** | exit 0 nos dois lados (original × corrigido); só o tempo do `unittest` muda |
| **"ausente" também recusar** | **ACHADO — desvio declarado** | não recusei a chave **ausente**: o probe C# **não emite** a chave e o caminho real depende disso (§5) |

Nenhum critério de aceite foi afrouxado: a mudança só **recusa mais** (endurece). O runner ficou verde
**depois** de ter sido visto VERMELHO com o defeito plantado.

---

## 1. (a) Arquivos alterados — caminho:linha

| arquivo | o que mudou (linha no disco final) |
|---|---|
| `tools/automacao/runtime/coletor.py` | `_mapear_saida_probe`: **l.475–478** (`evidencia_runtime_presente` — preserva se a CHAVE existia, para não confundir `null` com ausente) |
| 〃 | `consolidar_probe` docstring: **l.517–528** (regra da FORMA) |
| 〃 | `consolidar_probe` decisão: **l.540–561** — **l.547** `declarada_ev`, **l.549** `declara_runtime = (not declarada_ev) or (ev_valor is True)`, **l.550** `rotulado_fixture`; **l.552–561** o motivo nomeia a forma recusada |
| `tools/automacao/runtime/testes/t_aut4_costura_probe.py` | **l.230–259** — bloco A3 (F3): `"false"`/`0`/`"0"`/`null`/`"False"`/`1`/`"true"` → `FIXTURE`/exit 2 + controles (bool `True` e chave ausente → `CONFIRMADA`/exit 0) |
| `tools/automacao/runtime/testes/contra-prova/cp_aut5_isca_evidencia_runtime_forma_errada_ok.py` | **novo** (arquivo inteiro) — isca da FORMA errada (afirma o FALSO: forma errada vira runtime) |
| `docs/automacao/AUT-4-estado.json` | **l.19** `driver_sha256` novo; **l.40** nova isca na lista; **l.74** `iscas_reprovaram_como_deviam` 15→16; **l.157–164** bloco `achados_cor_aut4_f3_corrigidos` |
| `docs/automacao/AUT-4-preparacao.md` | **l.70** `15 iscas`→`16 iscas`; **l.79–83** nota COR-AUT4-F3 |
| `docs/automacao/COR-AUT4-F3-evidencias/` | logs + sondas (listados na §7) |
| `docs/automacao/COR-AUT4-F3-relatorio.md` | este relatório |

Nada mais foi tocado: `tools/automacao/runtime/roda_testes_runtime.py`, a fixture
`probe-saida-exemplo.entrada.json`, o fonte do probe (`AUT4ProbePlugin.cs`) e a `AUT4Probe.dll` seguem
com o **mesmo** sha256 (§2). `estilo/**` e `aceite/**` seguem com mtime antigo (14:00–14:40), anterior a
esta tarefa.

---

## 2. (d) sha256 do que eu medi (bytes em disco)

```
b92c46c3386428c6e75e77511e91ac61b71bf6980f3e3cae21a7ec9b0420fa89  tools/automacao/runtime/coletor.py   (ALTERADO)
dba7c0272bde6fcf722488bf255d1fdfc37fd99e301d09746a8e8567de3a19c4  tools/automacao/runtime/testes/t_aut4_costura_probe.py  (ALTERADO)
53db56e97c5e461790f348156d89313c8aa760dd756fe0db63d3e852f55259f1  .../contra-prova/cp_aut5_isca_evidencia_runtime_forma_errada_ok.py  (NOVO)
769ec5cab2ba5eadbc69535fe85588c618c74727f9625a31fa50fa191ab81f59  tools/automacao/runtime/roda_testes_runtime.py  (NAO alterado)
9b8893ef55d5d79f8ceb6332bacd4f3186eaba22f14c31a0231bdebcd6de7051  tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json  (NAO alterado)
5a51abaa439b90263e3b202e01a0b2b3b343fabc8cb71c9de8b3ac97b343bdd3  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs  (NAO alterado)
fd774259b5e8813f2f3b29e2ff805f12cb0cdab4c277116fcc8bbb7e7e3bffdd  tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll  (NAO alterado)
2d417e861d152cf6cd508413a7eca54ff3b0a4e3b462f1f908f7a6bf417aeda2  docs/automacao/AUT-4-estado.json  (ALTERADO)
d7604b2306df7dfde417702671cb13142eb2eec63ec78d0bb470f1153fc6366a  docs/automacao/AUT-4-preparacao.md  (ALTERADO)
```

Bytes **ORIGINAIS** (pré-F3) usados na não-regressão (recuperados da cópia `base`, feita antes de editar;
casa com o `driver_sha256` que a COR-AUT4-F2R mediu, `155b8ffe…`):

```
155b8ffe58ebdeda6d191d1b789fe3731a5d56c58962631216f0f2adf8b3f578  coletor.py (ORIGINAL)
```

Medição completa em `COR-AUT4-F3-evidencias/hashes.txt`.

---

## 3. (b/c) Comandos exatos + saída literal + exit code

### 3.1 Baseline ANTES (bytes originais, cópia `base/`)

```
$ cd <base> && python tools/automacao/runtime/roda_testes_runtime.py
 VEREDITO: VERDE (exit 0) — 9 teste(s)                                    EXIT=0
$ ... --contra-prova
 VEREDITO: VERDE (exit 0) — 15 teste(s)                                   EXIT=0
```

### 3.2 DEPOIS (bytes corrigidos, cópia `final/`)

```
$ cd <final> && python tools/automacao/runtime/roda_testes_runtime.py
[PASSOU] t_aut4_autorizacao.py … t_aut4_probe_contrato.py     (9/9)
 VEREDITO: VERDE (exit 0) — 9 teste(s)                                    EXIT=0
$ ... --contra-prova
[PROVA OK (reprovou como devia)] … as 16 iscas
 VEREDITO: VERDE (exit 0) — 16 teste(s)                                   EXIT=0
```

Logs literais: `COR-AUT4-F3-evidencias/fix-suite.log`, `fix-cp.log`, `base-suite.log`, `base-cp.log`.

### 3.3 Borda da FORMA — base × fix (`adv_borda.py`, saída literal)

```
### BASE (bytes originais)                              ### FIX (corrigido)
PRESENTE =False     -> FIXTURE   exit=2 evid=False      PRESENTE =False     -> FIXTURE   exit=2 evid=False
PRESENTE 'false'    -> CONFIRMADA exit=0 evid=True      PRESENTE 'false'    -> FIXTURE   exit=2 evid=False
PRESENTE 0          -> CONFIRMADA exit=0 evid=True      PRESENTE 0          -> FIXTURE   exit=2 evid=False
PRESENTE '0'        -> CONFIRMADA exit=0 evid=True      PRESENTE '0'        -> FIXTURE   exit=2 evid=False
PRESENTE None       -> CONFIRMADA exit=0 evid=True      PRESENTE None       -> FIXTURE   exit=2 evid=False
PRESENTE True       -> CONFIRMADA exit=0 evid=True      PRESENTE True       -> CONFIRMADA exit=0 evid=True
PRESENTE 'true'     -> CONFIRMADA exit=0 evid=True      PRESENTE 'true'     -> FIXTURE   exit=2 evid=False
PRESENTE 1          -> CONFIRMADA exit=0 evid=True      PRESENTE 1          -> FIXTURE   exit=2 evid=False
PRESENTE 'False'    -> CONFIRMADA exit=0 evid=True      PRESENTE 'False'    -> FIXTURE   exit=2 evid=False
AUSENTE a chave     -> CONFIRMADA exit=0 evid=True      AUSENTE a chave     -> CONFIRMADA exit=0 evid=True
False + chamador='runtime' -> FIXTURE exit=2            False + chamador='runtime' -> FIXTURE exit=2
```

A coluna BASE **reproduz o defeito da COR-AUT4-F2R** (a string `"false"`/`0`/`null` confirmava). A coluna
FIX recusa todas as formas não-canônicas e **preserva** o bool `True` e a chave ausente.

### 3.4 CONTRA-PROVA de verdade — defeito plantado em cópia fora do repo

`planta_defeito.py` reverte a correção (volta a
`rotulado_fixture = (declarada == "fixture" or ev_valor is False)`) numa cópia `defeito/` e mede:

```
DEFEITO PLANTADO: `rotulado_fixture = (declarada == 'fixture' or ev_valor is False)` (cru)

[suite]        exit=1   -> [REPROVOU] testes\t_aut4_costura_probe.py
                            RESULTADO|REPROVOU|aut4-costura-probe|A3 (F3): evidencia_runtime='false'
                            (forma nao-canonica) NAO pode confirmar
                           VEREDITO: VERMELHO (exit 1)
[contra-prova] exit=1   -> [PROVA FALHOU (passou quando devia reprovar)]
                            testes\contra-prova\cp_aut5_isca_evidencia_runtime_forma_errada_ok.py
                           VEREDITO: VERMELHO (exit 1)

SEM o defeito (cópia final): suite exit=0 | contra-prova exit=0
```

**Leitura:** com o defeito, a isca nova **PASSA** (não é decorativa) e o runner fica **VERMELHO** (exit 1);
sem o defeito, **VERDE** (exit 0). A regressão da suíte e a isca caem/sobem exatamente com o defeito —
vermelho→verde medido, não auto-relatado. Logs: `planta_defeito.log`, `defeito-suite.log`, `defeito-cp.log`.

### 3.5 Não-regressão — outros consumidores do `coletor.py`

Cópia completa do repo (315 MB, fora do repo), com o `coletor.py` **corrigido** (`b92c46c3…`) e depois com
o **original** (`155b8ffe…`), `cwd` na cópia:

```
                                        ORIGINAL   CORRIGIDO   saida
tools/automacao/cenarios/test_rstv.py   exit 0     exit 0      IDENTICA
tools/automacao/aut5/test_aut5.py       exit 0     exit 0      IDENTICA (16 casos)
tools/automacao/aut6/test_regressoes_cor_aut6.py  exit 0  exit 0  IDENTICA, exceto "Ran 26 tests in 0.363s/0.444s"
tools/automacao/ciclo/test_decisao.py   exit 0     exit 0      IDENTICA (127/127, 0 falhas)
```

Única diferença: a linha de tempo do `unittest` do aut6 (o resto byte a byte idêntico) — a diferença
explicável que a regra de TRAVAS permite. Logs: `nonreg-{base,fixed}-*.log`.

---

## 4. O que mudou (a regra)

`consolidar_probe` agora:

1. preserva se a **chave** `evidencia_runtime` existia no artefato
   (`_mapear_saida_probe` → `evidencia_runtime_presente`; idempotente);
2. só trata o artefato como **runtime** quando a chave está **AUSENTE** (o probe C# real **não emite** a
   chave) **ou** o valor é exatamente o bool `True`;
3. qualquer outra forma **PRESENTE** — bool `False`, string `"false"`/`"0"`/`"False"`/`"true"`, inteiro
   `0`/`1`, `null`, ou valor não-canônico — **RECUSA** como `FIXTURE`/exit 2, com o motivo nomeando a forma
   recusada. **Nunca** `CONFIRMADA`/runtime, nunca o campo invertido para `true`.

---

## 5. Desvio declarado — "ausente" NÃO é recusado (decisão do dono)

A tarefa listava `ausente` entre as formas a recusar. **Não recusei a chave ausente**, e a razão é medida,
não preferência:

- o probe C# **não grava** `evidencia_runtime` (varredura em `AUT4ProbePlugin.cs`: 0 ocorrências; as
  chaves gravadas são `status`/`fase`/`sessao`/`hash_fonte`/`observacoes`/`prints`/`ida_e_volta`/…);
- o caminho real `executar_rodada` → `consolidar_probe(saida, plano, …)` consome esse artefato **sem** a
  chave, e a suíte (`_saida_runtime(fx)` em `t_aut4_costura_probe.py`, e o stub de `t_aut4_execucao.py`)
  exige `CONFIRMADA`/exit 0 nesse caso;
- recusar a chave ausente faria **toda** rodada real sair `FIXTURE`/exit 2 e derrubaria o caminho feliz —
  o oposto do que a mesma tarefa exige ("não quebre o caminho feliz", "suíte verde").

Portanto implementei a leitura **coerente**: runtime = chave **ausente** OU bool `True`; toda forma
**presente** ≠ bool `True` é recusada. Isso cobre `"false"`, `0`, `"0"`, `null` (presente) e mais
(`"true"`, `1`, `"False"`, listas, …). Se a intenção do dono for **recusar a chave ausente também**, isso
é mudança de **critério de aceite** (não de trava) e deve voltar a ele: **PARO e declaro** em vez de
enfraquecer/endurecer sozinho. Ver veredito "ACHADO — desvio declarado" na §0.

---

## 6. Lacunas declaradas (NUNCA OK)

- **Nada em jogo foi exercitado.** Toda a prova é OFFLINE (bytes + stub, sem jogo). Leitura real de objetos
  vivos, PNG pela API do Unity, owners Harmony vivos e rollback em jogo seguem **NÃO EXERCITADOS** —
  dependem de autorização explícita do dono (CIC-5, `t_431dba37`). **Não tratei como OK.**
- Esta entrega **não** fecha o DoD nem substitui o aceite humano. A revisão independente fica com o pai
  (**COR-AUT4-F3R**).

---

## 7. Evidências (em `docs/automacao/COR-AUT4-F3-evidencias/`)

| arquivo | o que é |
|---|---|
| `hashes.txt` | sha256 dos arquivos medidos + o `coletor.py` ORIGINAL usado na não-regressão |
| `base-suite.log` / `base-cp.log` | ANTES: suíte 9/9 e contra-prova 15/15 (exit 0), bytes originais |
| `fix-suite.log` / `fix-cp.log` | DEPOIS: suíte 9/9 e contra-prova 16/16 (exit 0), bytes corrigidos |
| `adv_borda.py` / `adv_borda-base.log` / `adv_borda-fix.log` | a borda da FORMA (base × fix), saída literal |
| `planta_defeito.py` / `planta_defeito.log` | planta o defeito (`is False` cru) na cópia `defeito/` → runner VERMELHO |
| `defeito-suite.log` / `defeito-cp.log` | suíte exit 1 e contra-prova exit 1 com o defeito plantado |
| `nonreg-{base,fixed}-*.log` | os 4 consumidores do `coletor.py`, original × corrigido |

Reprodução: copiar `tools/` + `docs/automacao/` (suíte) e o repo sem `.git`/`scratch` (não-regressão) para
fora do repo; para o defeito, trocar o bloco da §4 por
`rotulado_fixture = (declarada == "fixture" or ev_valor is False)` e rodar `python` a partir da cópia.
