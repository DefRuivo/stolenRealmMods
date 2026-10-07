# COR-AUT4-F2R — revisão independente por execução do fechamento de A1-c/A2/A3/A6

Objeto: **COR-AUT4-F2** (`t_ecc83c8f`, em review) — fechamento dos 4 achados que a revisão
**COR-AUT4R** (`docs/automacao/COR-AUT4R-revisao.md`, CHANGES REQUESTED) abriu sobre a COR-AUT4.

Revisor: agente independente (`default`, tarefa `t_57dc92bc`) — **não é o autor**.
Data: **2026-10-06 15:33→15:41 (-03:00)**. HEAD do repo lido: `b94cb17`.
Escopo: **só leitura de bytes + execução OFFLINE sobre cópias fora do repo**
(`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4f2r/`). Nenhum jogo aberto, nenhum
probe instalado, nenhum deploy, nenhum build, nenhum commit/push, nenhum `git add`. Nada tocado em
`tools/automacao/estilo/**`, `tools/automacao/aceite/**`, `lib/Assembly-CSharp.dll` nem nos fontes dos mods.
Meus únicos arquivos no repo: este parecer + `docs/automacao/COR-AUT4-F2R-evidencias/`.

---

## 0. Veredito por item (sem "aprovado no geral")

| item | gravidade (COR-AUT4R) | veredito | uma linha |
|---|---|---|---|
| **A1-c** | baixo | **OK (com prova)** | print datado (`mtime ≥ lançamento`): PNG velho no `out_dir` reusado → `INDETERMINADO`/exit 1; planta do defeito derruba a suíte |
| **A2** | grave | **OK (com prova)** | vazio (`""`/só-espaços/`[]`/`{}`) = NÃO LIDO em **todas** as superfícies; fixture e stub usam a forma REAL (`""`); artefato vazio/forjado não confirma |
| **A3** | médio | **OK (com prova)** | `evidencia_runtime=false` (bool) sozinho → `FIXTURE`/exit 2, nunca invertido p/ runtime |
| **A6** | médio | **OK (com prova)** | marcador do driver obrigatório; `{conferiu:true}` sem marcador → `INDETERMINADO`/exit 1 |
| **A4** | médio | **OK (com prova) — intacto** | planta do defeito A4 derruba a suíte (`A4: probe ERRO/erro nao pode consolidar CONFIRMADA`) |
| **A5** | médio | **OK (com prova) — intacto** | planta do defeito A5 derruba a suíte (`A5/L: pasta pre-existente ... removida`) |
| **A7** | documental | **OK (com prova) — intacto** | planta do defeito A7 derruba `t_aut4_estado_docs` |

**Veredito final: APROVADO** (fechamento **offline** dos 4 achados). Ressalva não-bloqueante em §5.
A rodada runtime EM JOGO segue **NÃO EXERCITADA** (gate humano CIC-5) e **não** é tratada como OK (§6).

---

## 1. (a) sha256 que EU medi

Medidos **antes** da revisão e **depois** de toda a execução: **idênticos** (prova de que a revisão não
mexeu no repo). Batem byte a byte com os declarados em `COR-AUT4-F2-evidencias/hashes.txt`. Cópia completa
em `COR-AUT4-F2R-evidencias/hashes_revisor.txt`.

```
155b8ffe58ebdeda6d191d1b789fe3731a5d56c58962631216f0f2adf8b3f578  tools/automacao/runtime/coletor.py
9b8893ef55d5d79f8ceb6332bacd4f3186eaba22f14c31a0231bdebcd6de7051  tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json
769ec5cab2ba5eadbc69535fe85588c618c74727f9625a31fa50fa191ab81f59  tools/automacao/runtime/roda_testes_runtime.py   (runner, NÃO alterado)
afe6131ff9d1596cbaf575417a01a6e5d9284700c769754efeddf342f156309f  tools/automacao/runtime/testes/t_aut4_execucao.py
bd6e2dee763ce6fa91fab92c08ae98a2629efbb10003cbb941575166ab252f97  tools/automacao/runtime/testes/t_aut4_costura_probe.py
93ce41fc13b2b8ff8b59c238668898afd5cfd7c035babdb9c2a7ba6e5484e799  .../contra-prova/cp_aut5_isca_print_velho_ok.py
36e4c45a2b69add76eafff7c16e546888612c95d6c94cec19fd4cb5a3b402181  .../contra-prova/cp_aut5_isca_alvo_vazio_ok.py
e25b633f0b9c873f0e2f85263999c81d9ad42bf7640f5f48d9834e6cc0fd81d8  .../contra-prova/cp_aut5_isca_evidencia_runtime_false_ok.py
0df7a56b911fd119934c331588f1c433da41c8eb8823454d39101e6a45361170  .../contra-prova/cp_aut5_isca_ida_volta_sem_marcador.py
5ed26c540a8cf95f17884b0cb4d3bef75ae10fbb15517894c0f0e51dc01476f9  docs/automacao/AUT-4-estado.json
3bb7e34c7f764609146ca5189ca89d4bb4fffecfc0b753b27ec2f522d1df65e4  docs/automacao/AUT-4-preparacao.md
5a51abaa439b90263e3b202e01a0b2b3b343fabc8cb71c9de8b3ac97b343bdd3  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs  (NÃO alterado)
fd774259b5e8813f2f3b29e2ff805f12cb0cdab4c277116fcc8bbb7e7e3bffdd  tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll  (NÃO alterado)
7a92222822044ad53944bb818017de4e55ab7b0016b8bc9ea9b4e234103bc461  docs/automacao/COR-AUT4-F2-relatorio.md
4666280391d309579a82178fd33276c2d42bae38863d5cc94031feb477debd4b  docs/automacao/COR-AUT4R-revisao.md
88620fc7f35db0091e10d86626475f7a53cba25d05b1f6139b14b69ee254d9a9  docs/SUPERVISAO.md
```

Bytes **ORIGINAIS** (pré-COR-AUT4-F2) usados na não-regressão, recuperados da cópia da COR-AUT4R
(`scratch/cor-aut4r/copia/`) — o `coletor.py` original casa com o `c7032285…` que a COR-AUT4R mediu:

```
c7032285e2e9828d8b3c3c9ffd41420f3a0ccebe0f75440a0b67533135f8ddae  coletor.py (ORIGINAL)
725965af1714ab4ed3bc126e7ad17632373cc5f4739011b6b913797bcbfef6f0  probe-saida-exemplo.entrada.json (ORIGINAL)
```

Método: `cp -r` de `tools/` + `docs/automacao/` (para a suíte) e do repo completo exceto `.git`/`scratch`
(para não-regressão) para fora do repo; toda execução rodou com `cwd` na cópia.

---

## 2. (b) Comandos exatos + saída literal + exit code

### 2.1 Baseline na cópia com os bytes ATUAIS (verde)

```
$ cd <copia>/base && python tools/automacao/runtime/roda_testes_runtime.py
[PASSOU] testes\t_aut4_autorizacao.py … testes\t_aut4_probe_contrato.py   (9/9)
 VEREDITO: VERDE (exit 0) — 9 teste(s)            EXIT=0
$ ... --contra-prova
[PROVA OK (reprovou como devia)] ... as 15 iscas
 VEREDITO: VERDE (exit 0) — 15 teste(s)           EXIT=0
```

Log literal: `COR-AUT4-F2R-evidencias/base-suite.log`, `base-cp.log`. Confere com o que a entrega alega
(9 e 15) e com o que o PAI reconferiu.

### 2.2 Contra-prova REAL — defeito plantado por MIM, um por achado

Para **cada** achado reverti a correção na cópia (arquivo:linha do disco atual) e medi. Todos:

| defeito plantado | coletor.py (linha atual) | suite | contra-prova |
|---|---|---|---|
| **A1-c** `fresco = bool(existe)` (sem datar) | l.813-814 | **exit 1** | **exit 1** |
| **A2** `_estado_do_campo` volta a só `None`/`AUSENTES` | l.207/210-211 | **exit 1** | **exit 1** |
| **A3** exige `rotulo_fixture` junto de `evidencia_runtime is False` | l.530-531 | **exit 1** | **exit 1** |
| **A6** volta o escape `not ida_volta.get("marcador")` | l.1001-1002 | **exit 1** | **exit 1** |
| **A4** desliga o rebaixe de status/fase de falha | l.556-568 | **exit 1** | **exit 1** |
| **A5** `preservar = []` no rollback | l.677 | **exit 1** | **exit 1** |
| **A7** remove 1 isca da lista declarada no estado | `AUT-4-estado.json` l.41 | **exit 1** | exit 0 (A7 é trava de suíte) |

Saída literal do `A1-c` (log `def_a1c-suite.log`):

```
[REPROVOU] testes\t_aut4_execucao.py
   | RESULTADO|REPROVOU|aut4-execucao|A1c: print ANTERIOR a rodada nao vale (mesmo existindo com bytes>0): esperado False, obtido True
 VEREDITO: VERMELHO (exit 1)
[PROVA FALHOU (passou quando devia reprovar)] testes\contra-prova\cp_aut5_isca_print_velho_ok.py
 VEREDITO: VERMELHO (exit 1)
```

`A2`: `aut4-costura-probe|B3: inativo declara rendered como N/A: esperado 'NAO_APLICAVEL', obtido 'PRESENTE'`
e `aut4-execucao|A2/I: objeto inativo com alvo nao lido NAO pode consolidar CONFIRMADA`; iscas
`cp_aut5_isca_alvo_nao_lido_ok.py` **e** `cp_aut5_isca_alvo_vazio_ok.py` passaram (vermelho).

`A3`: `aut4-costura-probe|A3 (F2): evidencia_runtime=false sozinho tem de sair FIXTURE: esperado 'FIXTURE', obtido 'CONFIRMADA'`;
isca `cp_aut5_isca_evidencia_runtime_false_ok.py` passou (vermelho).

`A6`: `aut4-execucao|A6m: autodeclaracao SEM o marcador do driver NAO pode conferir: esperado False, obtido True`;
isca `cp_aut5_isca_ida_volta_sem_marcador.py` passou (vermelho).

`A4`: `aut4-costura-probe|A4: probe ERRO/erro nao pode consolidar CONFIRMADA`; isca `…status_erro_confirma.py` passou.
`A5`: `aut4-execucao|A5/L: pasta do probe PRE-EXISTENTE nao pode ser removida no rollback`; isca `…dir_pre_existente_removido.py` passou.
`A7`: `aut4-estado-docs|A7: a lista de iscas declarada tem de ser IGUAL a do disco` (esperado 15, obtido 14).

Removido o defeito, todos voltam a **exit 0** (a cópia `base` acima). Logs: `def_*-suite.log` / `def_*-cp.log`.

### 2.3 Sondas adversariais próprias (`adv_rev.py`, `adv_borda.py`)

Saída literal (`COR-AUT4-F2R-evidencias/adv_rev.log`):

```
BLOCO 1 - _estado_do_campo: VAZIO = NAO LIDO em todas as formas
  valor='' -> AUSENTE   '   ' -> AUSENTE   '\t' -> AUSENTE   '\n' -> AUSENTE
  valor=[] -> AUSENTE   {} -> AUSENTE   () -> AUSENTE   set() -> AUSENTE   frozenset() -> AUSENTE
  CONTROLE 'x' -> PRESENTE   [1] -> PRESENTE   {'a':1} -> PRESENTE

BLOCO 2 - cada campo-alvo VAZIO vira LACUNA
  texto_renderizado='' / texto_bruto='  ' / owners=[] / keywords={} / cores={} / fonte='' / material='' /
  shader='' / objeto='' / caminho='' / geometria={}  -> lacuna=True ok=False (todos)
  objeto INATIVO com texto_renderizado='' E texto_bruto='' -> estado=AUSENTE lacuna=True (NÃO vira N/A)

BLOCO 3 - artefato VAZIO/FORJADO nao confirma
  (a) observacoes=[] + runtime + CONCLUIDO      -> NAO_EXERCITADO exit=2
  (b) 1 obs com TODOS os alvos vazios           -> INCOMPLETO     exit=1
  (c) obs status=OK com rendered vazio          -> RECUSOU ObservacaoInvalida
  (d) runtime SEM sessao/hash                   -> RECUSOU ObservacaoInvalida
  (+) CONTROLE obs ativa completa               -> CONFIRMADA      exit=0

BLOCO 4 - A3: evidencia_runtime=false (bool) sozinho -> FIXTURE exit=2 evid_runtime=False
  caller forca procedencia=runtime              -> FIXTURE exit=2 evid_runtime=False
```

`adv_borda.log` (borda de robustez, §5): `evidencia_runtime=False` → FIXTURE/2; `"false"`/`0` → tratados
como runtime.

---

## 3. (c) Veredito por item, com prova

**A1-c — OK (com prova).** `coletor.provas_de_execucao` l.813-818 exige `mtime + 1e-3 >= lancamento_epoca`
para cada arquivo de `prints`; `lancamento_epoca = time.time()` é fixado no lançamento (l.958). Prova
vermelho→verde: com `fresco = bool(existe)` a suíte cai no caso `A1c` (saída literal em §2.2) e a isca
print-velho PASS; sem o defeito, verde. Controle positivo no mesmo teste: rodada `B` com print fresco passa
(`prints_ok=True`). **Rejeita mesmo PNG velho com `out_dir` reusado**: sim.

**A2 — OK (com prova).** Choke point único `_estado_do_campo` (l.194-212) é chamado para **cada** campo em
`CAMPOS_TODOS` (l.253-255) — não há caminho alternativo de classificação de presença (confirmado por
varredura: só l.255 e l.261 usam a função). Prova de **todas as superfícies**: bloco 1/2 da sonda (string
vazia/só-espaços, `[]`, `{}`, `()`, `set()`, `frozenset()` → AUSENTE; 11 campos-alvo vazios → lacuna). O
fallback `NAO_APLICAVEL` só dispara se o alvo é AUSENTE **e** `texto_bruto` é PRESENTE (l.260-261) — objeto
inativo com ambos vazios fica AUSENTE/lacuna (bloco 2). **Forma REAL**: fixture l.43 `texto_renderizado: ""`
(era `null`), stub `t_aut4_execucao.py` l.130 idem. **Não burlável por artefato vazio/forjado**: bloco 3
(vazio → NAO_EXERCITADO/2; todos-os-alvos-vazios → INCOMPLETO/1; `status:OK` com campo vazio → recusa;
runtime sem sessão/hash → recusa). Planta A2 derruba 2 testes + a isca nova (§2.2).

**A3 — OK (com prova).** `consolidar_probe` l.530-531: `rotulado_fixture = (declarada == "fixture" or
saida.get("evidencia_runtime") is False)`; o rótulo deixou de ser pré-requisito. Prova: o campo declarado
**não** é invertido e sai `FIXTURE`/exit 2, inclusive com o chamador forçando `procedencia="runtime"`
(bloco 4). Planta A3 derruba `t_aut4_costura_probe` + a isca nova. **`evidencia_runtime=false` nunca mais
vira CONFIRMADA por inferência**: sim (bool). Borda não-bloqueante em §5.

**A6 — OK (com prova).** `executar_rodada` l.1001-1002: `conferiu = bool(conferiu) and str(marcador or "")
== str(marcador_ida_volta)`; `marcador_ida_volta = "AUT4-IDA-E-VOLTA-<sessão>"` só existe quando
`exigir_ida_volta` (l.911-912), e o check só roda nesse ramo — não há furo de marcador vazio. Prova: caso
`A6m` e a isca sem-marcador; controle positivo `A6/K` (`--ida-volta`) fecha `CONCLUIDO`/exit 0. Planta A6
derruba a suíte.

**A4 / A5 / A7 — OK (com prova), intactos.** As três travas seguem vivas: plantar o defeito correspondente
derruba a suíte com a mensagem esperada (§2.2). As travas do A4 (status/fase de falha + silêncio → rebaixa,
l.556-568), do A5 (`preservar` no rollback, l.677/696) e do A7 (`t_aut4_estado_docs` casa listas/hashes com
o disco) **não** foram afrouxadas.

---

## 4. (d) Iscas: reais × decorativas

- Runner `--contra-prova`: **15 iscas**, todas reprovam como deviam (contagem real, não auto-relato).
- **4 iscas novas (A1-c/A2/A3/A6): reais, NÃO decorativas.** Cada uma foi vista **PASSANDO** exatamente
  quando o defeito do seu achado foi plantado e reprovando sem ele — prova vermelho→verde individual (§2.2).
  Nenhuma passa nos dois lados.
- **11 iscas pré-existentes (A4/A5/A6 + AUT-4R2): reais.** Provei A4/A5 por planta própria (as iscas
  `status_erro_confirma` e `dir_pre_existente_removido` passaram com o defeito plantado). As demais seguem
  como a COR-AUT4R as validou; o runner confirma que **todas as 15** reprovam no estado atual.
- **Nenhuma isca decorativa encontrada.**

---

## 5. Ressalva não-bloqueante (robustez, não ACHADO)

`consolidar_probe` usa `is False` (identidade com o bool Python). Se um artefato trouxesse
`"evidencia_runtime": "false"` (string) ou `0` — em vez do bool JSON `false` — o campo **não** é lido como
declaração de fixture e o artefato pode virar runtime (medido em `adv_borda.log`: `CONFIRMADA/exit 0`).
O contrato do probe C# e a fixture usam o **bool** (`false`), e o probe nem emite essa chave (ela é rótulo
de fixture) — logo **nenhum artefato real do probe dispara a borda**. Recomendação (não bloqueia o
fechamento): endurecer para `str(v).strip().lower() in ("false","0")` se quiser cobrir entrada não-canônica.
Não é a inversão do A3 (que era `false` bool virando runtime) — aquela está fechada.

---

## 6. (e) Lacunas declaradas — NUNCA OK

- **Rodada runtime EM JOGO: NÃO EXERCITADA.** Leitura real de objetos vivos, PNG pela API do Unity, owners
  Harmony vivos, `Tooltip.ShowTooltip` real e rollback **em jogo**: nada disso foi exercitado — revisão
  100% offline, como a entrega. Depende de **autorização explícita do dono** (CIC-5, `t_431dba37`). **Não
  tratei como OK.**
- **Ida-e-volta em jogo: NÃO EXERCITADA.** A porta existe (fonte+binário) e o driver a exige (A6 fechado),
  mas nunca rodou em sessão viva.
- **Gate de autorização do probe**: provado no contrato do driver (offline) — não em execução real.
- Esta revisão **não fecha o DoD** nem substitui o aceite humano/publicação (gates separados).

---

## 7. (f) Veredito final

**APROVADO** — os 4 achados (A1-c/A2/A3/A6) estão fechados com prova por execução própria
(vermelho→verde por achado), A4/A5/A7 seguem intactos, e a não-regressão confere. Nada a corrigir
para o fechamento offline.

O que **falta** (fora do escopo desta correção; gates separados, **não** OK):
1. Rodada runtime **em jogo** (CIC-5, `t_431dba37`) — autorização explícita do dono.
2. Aceite humano e publicação (DoD).

Opcional (robustez, §5): tratar `evidencia_runtime` não-booleano como fixture. **Não bloqueia.**

---

## 8. Não-regressão (o `coletor.py` é importado por outras frentes)

Cópia completa do repo (exceto `.git`/`scratch`), com `coletor.py`+fixture **corrigidos** × **originais**
(`c7032285…`/`725965af...`), `cwd` na cópia:

```
                                     CORRIGIDO   ORIGINAL   saida
cenarios/test_rstv.py                exit 0      exit 0     IDENTICA
aut5/test_aut5.py                    exit 0      exit 0     IDENTICA (16 casos)
aut6/test_regressoes_cor_aut6.py     exit 0      exit 0     IDENTICA (26 testes OK; so o tempo difere)
ciclo/test_decisao.py                exit 0      exit 0     IDENTICA (127/127, 0 falhas)
```

Nenhuma diferença de resultado; só a linha de tempo do `unittest` do aut6 (`2.022s`→`0.606s`) muda — a
diferença explicável que a regra de TRAVAS permite. Logs: `nonreg-fixed-*.log` / `nonreg-base-*.log`.
`tools/automacao/estilo/**` e `aceite/**` não foram tocados (o `coletor.py` não mudou `validar_plano`/
`planejar_rodada`, que são o que elas usam).

---

## 9. Evidências (em `docs/automacao/COR-AUT4-F2R-evidencias/`)

| arquivo | o que é |
|---|---|
| `hashes_revisor.txt` | sha256 antes/depois (produto, réguas, probe) + bytes originais usados na não-regressão |
| `base-suite.log` / `base-cp.log` | suíte 9/9 e contra-prova 15/15 (exit 0) sobre a cópia com os bytes atuais |
| `def_a1c|a2|a3|a6|a4|a5|a7-{suite,cp}.log` | cada defeito plantado por mim → runner VERMELHO (exit 1) e isca PASSANDO |
| `adv_rev.py` / `adv_rev.log` | sonda própria: `""` em todas as superfícies + burla por artefato vazio/forjado |
| `adv_borda.py` / `adv_borda.log` | borda de robustez do A3 (string/0) |
| `nonreg-{fixed,base}-*.log` | os 4 consumidores do `coletor.py`, corrigido × original |

Reprodução: copiar `tools/` + `docs/automacao/` (suíte) e o repo sem `.git`/`scratch` (não-regressão) para
fora do repo, aplicar os bytes originais em `tools/automacao/runtime/{coletor.py,fixtures/probe-saida-exemplo.entrada.json}`
e rodar com `python` a partir da cópia.
