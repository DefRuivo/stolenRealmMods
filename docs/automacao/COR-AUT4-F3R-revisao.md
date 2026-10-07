# COR-AUT4-F3R — revisão independente do endurecimento de `evidencia_runtime`

Revisor: subagente `default` (autor ≠ revisor). Data: **2026-10-06**. Card: `t_732b85ed`; tarefa-mãe
`t_dbb4a228` (COR-AUT4-F3).
Escopo: **bytes + execução própria sobre cópias fora do repo** (`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4f3r/`).
Nada instalado, jogo não aberto, nada publicado/commitado, nenhum `git add`; `estilo/**`, `aceite/**`,
fontes dos mods e `lib/Assembly-CSharp.dll` não tocados.

---

## 0. Veredito por item

| # | item | veredito |
|---|---|---|
| 1 | sha256 antes/depois (não mexeu no repo) | **OK** — mesma hash nas duas medições (§1) |
| 2 | planta o defeito (`is False` cru) em cópia fora do repo → suite e contra-prova VERMELHAS; sem defeito, VERDES | **OK** — medi por execução própria (§2) |
| 2b | alguma das 16 iscas é decorativa? | **OK — nenhuma** (15 reprovam nos 2 lados; 1 flipa com o defeito) (§4) |
| 3 | varredura de borda: alguma forma errada ainda confirma? algum falso-negativo? | **ACHADO** (falso-OK residual de baixa severidade, §7) + **OK** no resto: só `ausente` e bool `true` confirmam (§3) |
| 4 | julgamento do desvio declarado (ausente = runtime) | **OK — fidelidade ao artefato real, não é mudança de critério** (§5) |
| 5 | não-regressão nos 4 consumidores | **OK** — exit 0 nos dois lados; única diferença = linha de tempo do unittest (§6) |
| — | lacunas em jogo (rodada real, PNG, Tooltip, rollback) | **NUNCA OK** — seguem NÃO EXERCITADAS (§8) |

---

## 1. sha256 medidos pelo revisor (antes e depois)

Medido **antes** de qualquer cópia/execução e **depois** (idêntico). O revisor não editou o repo; só leu e copiou.

```
ANTES:
b92c46c3386428c6e75e77511e91ac61b71bf6980f3e3cae21a7ec9b0420fa89  tools/automacao/runtime/coletor.py
dba7c0272bde6fcf722488bf255d1fdfc37fd99e301d09746a8e8567de3a19c4  .../testes/t_aut4_costura_probe.py
53db56e97c5e461790f348156d89313c8aa760dd756fe0db63d3e852f55259f1  .../contra-prova/cp_aut5_isca_evidencia_runtime_forma_errada_ok.py
2d417e861d152cf6cd508413a7eca54ff3b0a4e3b462f1f908f7a6bf417aeda2  docs/automacao/AUT-4-estado.json
d7604b2306df7dfde417702671cb13142eb2eec63ec78d0bb470f1153fc6366a  docs/automacao/AUT-4-preparacao.md

DEPOIS (mesma medição, bytes inalterados):
b92c46c3386428c6e75e77511e91ac61b71bf6980f3e3cae21a7ec9b0420fa89  tools/automacao/runtime/coletor.py
dba7c0272bde6fcf722488bf255d1fdfc37fd99e301d09746a8e8567de3a19c4  .../testes/t_aut4_costura_probe.py
53db56e97c5e461790f348156d89313c8aa760dd756fe0db63d3e852f55259f1  .../contra-prova/cp_aut5_isca_evidencia_runtime_forma_errada_ok.py
2d417e861d152cf6cd508413a7eca54ff3b0a4e3b462f1f908f7a6bf417aeda2  docs/automacao/AUT-4-estado.json
d7604b2306df7dfde417702671cb13142eb2eec63ec78d0bb470f1153fc6366a  docs/automacao/AUT-4-preparacao.md
```

O sha256 de `coletor.py` que **eu** medi casa com o medido pelo PAI
(`b92c46c3…`) e com o declarado no relatório do autor.

Arquivos que o relatório diz **não** ter tocado — conferidos byte a byte contra o declarado, **todos iguais**:

```
769ec5cab2ba5eadbc69535fe85588c618c74727f9625a31fa50fa191ab81f59  tools/automacao/runtime/roda_testes_runtime.py
9b8893ef55d5d79f8ceb6332bacd4f3186eaba22f14c31a0231bdebcd6de7051  tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json
5a51abaa439b90263e3b202e01a0b2b3b343fabc8cb71c9de8b3ac97b343bdd3  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs
fd774259b5e8813f2f3b29e2ff805f12cb0cdab4c277116fcc8bbb7e7e3bffdd  tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll
```

Diff `original (155b8ffe) × corrigido (b92c46c3)` lido pelo revisor: **3 hunks, todos do F3** — o
mapeamento `evidencia_runtime_presente`, a docstring do F3 e o bloco de decisão. A mudança é
cirúrgica: nada fora do `consolidar_probe`/`_mapear_saida_probe` foi alterado.

O bytes ORIGINAL usado na não-regressão é `155b8ffe58ebdeda6d191d1b789fe3731a5d56c58962631216f0f2adf8b3f578`
(= hash medido na revisão COR-AUT4-F2R pré-F3), recuperável da cópia pré-edição.

---

## 2. Planto do defeito (reprodução própria) — comandos + saída literal + exit

Cópia própria em `…/cor-aut4f3r/repo` (bytes corrigidos) e `…/cor-aut4f3r/defeito` (defeito plantado
por mim). Planto: substituí o bloco novo por `rotulado_fixture = (declarada == "fixture" or ev_valor is False)`
(assert de que o bloco novo aparece exatamente 1×; `is False` cru = defeito pré-F3).

```
$ python revisor_planta.py
bloco novo encontrado 1 vez(es) (exige 1)
DEFEITO PLANTADO (is False cru): a2fd3fbf3fc514f60c1cc02c9731768d70653a72c0eebe0123f6d6a52455e64f

[FIX (corrigido)] [suite]        exit=0   -> VEREDITO: VERDE (exit 0) — 9 teste(s)
[FIX (corrigido)] [contra-prova] exit=0   -> VEREDITO: VERDE (exit 0) — 16 teste(s)
[DEFEITO (is False cru)] [suite] exit=1   -> [REPROVOU] t_aut4_costura_probe.py: "A3 (F3): evidencia_runtime='false' (forma nao-canonica) NAO pode confirmar"; VEREDITO: VERMELHO (exit 1)
[DEFEITO (is False cru)] [contra-prova] exit=1 -> [PROVA FALHOU (passou quando devia reprovar)] cp_aut5_isca_evidencia_runtime_forma_errada_ok.py; VEREDITO: VERMELHO (exit 1)
```

Comandos exatos (cwd = raiz da cópia):

```
python tools/automacao/runtime/roda_testes_runtime.py                 # suite
python tools/automacao/runtime/roda_testes_runtime.py --contra-prova  # contra-prova
```

**Leitura:** vermelho→verde medido por execução própria, não auto-relatado. Com o defeito, o runner
fica VERMELHO (exit 1) e a isca nova **PASSA** (não reprova), que é exatamente o comportamento
vermelho-para-verde prometido. Sem o defeito, VERDE (exit 0) nos dois modos.

---

## 3. Varredura de borda (fix × defeito) — `revisor_borda.py`

Artefato = fixture `probe-saida-exemplo` sem `procedencia`/`rotulo_fixture`, variando só `evidencia_runtime`.

```
FORMA                  | FIX                        | DEFEITO(is False cru)
AUSENTE (sem chave)    | CONFIRMADA   exit=0   ev=True  | CONFIRMADA   exit=0   ev=True
bool true              | CONFIRMADA   exit=0   ev=True  | CONFIRMADA   exit=0   ev=True
bool false             | FIXTURE      exit=2   ev=False | FIXTURE      exit=2   ev=False
string 'false'         | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string 'False'         | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string 'FALSE'         | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string ' false '       | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
ent 1                  | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
ent 0                  | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
ent 2                  | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string '0'             | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string '1'             | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string 'true'          | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string 'True'          | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
null                   | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
lista []               | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
dict {}                | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string ''              | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True
string 'no'            | FIXTURE      exit=2   ev=False | CONFIRMADA   exit=0   ev=True

FIX   confirma SO em: ['AUSENTE (sem chave)', 'bool true']
DEF   confirma em:   [AUSENTE, bool true, 'false','False','FALSE',' false ',1,0,2,'0','1','true','True',None,[],{},'','no']
```

- **Nenhuma forma errada PRESENTE confirma** no FIX: qualquer forma ≠ bool `True` → `FIXTURE`/exit 2, e o
  campo declarado **nunca** é invertido para `true`. Isso cobre inclusive formas que o autor não listou
  (`'FALSE'`, `' true '`, lista, dict, `''`, `'no'`).
- **Sem falso-negativo**: os dois caminhos de runtime legítimo (chave AUSENTE e bool `true`) continuam
  `CONFIRMADA`/exit 0. Varredura mais ampla que a do autor; resultado coincide.
- **A coluna DEFEITO reproduz o defeito da COR-AUT4-F2R**: no código antigo, *toda* forma exceto o bool
  `false` confirmava (18 de 19 casos), não só a string `"false"`.

---

## 4. Iscas — reais × decorativas (16/16 medidas uma a uma)

Corri cada `cp_*` isolada nas duas cópias e comparei os exit codes:

```
resultado: 15 iscas reprovam (exit 1) nos DOIS lados  -> reais, não decorativas
            1 isca   (cp_aut5_isca_evidencia_runtime_forma_errada_ok.py) -> FIX exit 1 / DEF exit 0
                      = a única que FLIPA com o defeito (prova o defeito)
DECORATIVAS (exit 0 nos dois lados): NENHUMA
```

A isca nova **não é decorativa**: ela passa (exit 0) quando o defeito está plantado e reprova (exit 1)
com a correção — é a contra-prova real da COR-AUT4-F3. As outras 15 continuam válidas para as travas
anteriores (reprovam nos dois lados).

---

## 5. Julgamento do desvio declarado — chave AUSENTE = runtime

**Veredito: OK — é fidelidade ao artefato real, NÃO é mudança de critério de aceite disfarçada de
conserto.** Fundamentos medidos por mim:

1. `grep -c "evidencia_runtime" tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` → **0**;
   `grep -a -c` no `AUT4Probe.dll` → **0**. O probe C# real **não emite** a chave; o artefato real chega
   sem ela.
2. O caminho real `executar_rodada` → `consolidar_probe(saida, …)` (coletor.py l.1018) consome esse
   artefato; no mapeamento, `evidencia_runtime_presente = ("evidencia_runtime" in dados)` → `False` para
   o probe real → `declara_runtime=True` → runtime. Se a ausência fosse recusada, **toda** rodada real
   sairia `FIXTURE`/exit 2 — quebraria o caminho feliz que a própria tarefa exige preservar.
3. A semântica do campo é uma **auto-declaração** de proveniência: ausência = nenhuma declaração (nem
   runtime nem fixture). O defeito original era aceitar uma *forma errada de não-runtime* como runtime;
   ausência não é "forma errada" — não há valor nenhum para estar errado. O conserto preserva o
   comportamento pré-F3 para a ausência (o `is False` antigo também tratava ausente como runtime), ou
   seja **não muda critério** — só recusa mais.
4. O que *seria* mudança de critério é recusar a ausência; o autor **parou e declarou** em vez de decidir
   sozinho — conduta correta. Não escalo para o dono: a leitura implementada é a única coerente com o
   artefato real e com a intenção declarada ("não quebre o caminho feliz"). Se o dono quiser runtime
   somente com chave presente e `true`, isso exigiria o probe C# passar a emitir a chave (mudança de
   instrumento, fora do escopo offline) — registrado como opção, **não como pendência bloqueante**.

---

## 6. Não-regressão nos 4 consumidores (bytes originais × corrigidos)

Cópia própria `orig/` (coletor `155b8ffe…`) × `repo/` (coletor `b92c46c3…`), `cwd` na raiz de cada cópia:

```
tools/automacao/cenarios/test_rstv.py            ORIGINAL exit=0 | CORRIGIDO exit=0 | saida IDENTICA
tools/automacao/aut5/test_aut5.py                ORIGINAL exit=0 | CORRIGIDO exit=0 | saida IDENTICA
tools/automacao/aut6/test_regressoes_cor_aut6.py ORIGINAL exit=0 | CORRIGIDO exit=0 | saida DIFERE
tools/automacao/ciclo/test_decisao.py            ORIGINAL exit=0 | CORRIGIDO exit=0 | saida IDENTICA
```

A única diferença no aut6 é a linha de tempo do `unittest` (não-determinística):

```
@@ -31 +31 @@
-Ran 26 tests in 0.463s
+Ran 26 tests in 0.339s
```

Tudo o mais byte a byte idêntico. Não há regressão funcional nos 4 consumidores.

---

## 7. ACHADO — falso-OK residual via chave interna `evidencia_runtime_presente` (baixa severidade)

**Repro literal** (artefato = fixture sem `procedencia`/`rotulo_fixture`, com as chaves abaixo):

```
presente=false + ev='false' (auto-contraditorio)  -> ('CONFIRMADA', 0, True)
presente=false + ev=0                             -> ('CONFIRMADA', 0, True)
presente=0     + ev='false'                       -> ('CONFIRMADA', 0, True)
presente=true  + ev='false'                       -> ('FIXTURE', 2, False)   # ok
```

Ou seja: um artefato que traz `evidencia_runtime: "false"` **e** também
`"evidencia_runtime_presente": false` (ou `0`) confirma como runtime, porque o mapeamento
(`_mapear_saida_probe`, l.475–478) **confia na chave de presença vinda do próprio artefato** para
decidir se a chave estava ausente.

**Avaliação de severidade:** a chave `evidencia_runtime_presente` é **interna** — não é emitida pelo
probe C# (grep 0 no `.cs` e na `.dll`), pela fixture, nem por nenhum outro produtor do repo (varredura
`grep -rn evidencia_runtime_presente` só acha o próprio `coletor.py` e a documentação). Para explorar o
buraco é preciso um artefato que **se autocontradiz** injetando um campo de implementação que nada no
pipeline produz. Não é o defeito da F2R reaberto para artefato algum do pipeline real.

**Classificação:** ACHADO **não bloqueante** desta revisão, mesma classe (forma que o jogo não produz
passando como válida), mas exige fabricação dupla. **Recomendação** (endurecimento futuro, curto): não
confiar na presença vinda do JSON — derivar a presença internamente (ex.: marcar dicts já mapeados com
um sentinela privado, ou, na segunda passagem, tratar "presente=False mas `evidencia_runtime` presente e
≠ `True`" como fixture). Não é mudança de critério de trava; é fechar uma borda a mais.

---

## 8. Lacunas declaradas que NUNCA são OK

- **Nada em jogo foi exercitado.** Toda a prova é OFFLINE (bytes + artefatos JSON). Rodada runtime real,
  PNG pela API do Unity, `Tooltip.ShowTooltip`, owners Harmony vivos e rollback em jogo seguem
  **NÃO EXERCITADOS** e dependem de autorização explícita do dono (**CIC-5, `t_431dba37`**). **Não tratei
  como OK** e esta revisão não os cobre.
- A entrega **não** fecha o DoD nem substitui o aceite humano.

---

## 9. Veredito final

**APROVADO** — com 1 ressalva não bloqueante (§7) a registrar.

O que foi verificado por execução própria do revisor:
- sha256 do objeto inalterado antes/depois; o conserto é cirúrgico e casa com o declarado;
- defeito `is False` cru plantado por mim → suite exit 1 e contra-prova exit 1 (isca nova PASSA);
  sem defeito → suite exit 0 (9) e contra-prova exit 0 (16);
- nenhuma das 16 iscas é decorativa; a isca nova prova o defeito (flip real);
- borda: só `ausente` e bool `true` confirmam; toda forma errada PRESENTE → FIXTURE/exit 2; sem falso-negativo;
- desvio declarado (ausente = runtime) **justificado pelo artefato real**, sem decisão do dono pendente;
- não-regressão OK nos 4 consumidores (exit 0 nos dois lados; só a linha de tempo do unittest difere).

**O que falta (não bloqueia este aceite):** considerar, numa tarefa de endurecimento, não confiar na
chave interna `evidencia_runtime_presente` vinda do artefato (§7). E o que **sempre** segue pendente e
não pode ser dado como OK: exercício em jogo (rollback/PNG/Tooltip), sob autorização do dono (CIC-5).
