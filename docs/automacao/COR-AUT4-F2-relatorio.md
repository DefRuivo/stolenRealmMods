# COR-AUT4-F2 — fechamento dos achados A1/A2/A3/A6 da revisão COR-AUT4R

Objeto: **COR-AUT4-F2** (`t_ecc83c8f`) — fechar os 4 achados que a revisão independente **COR-AUT4R**
(`t_d99241fd`, `docs/automacao/COR-AUT4R-revisao.md`, veredito **CHANGES REQUESTED**) abriu sobre a
entrega COR-AUT4 (`t_b62359c3`).

Autor: agente `default`. Data: **2026-10-06**.
Escopo: **só bytes + execução OFFLINE sobre cópia fora do repo** (scratch em
`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4f2/`). Nenhum jogo aberto/encerrado, nenhum
save tocado, nenhum probe instalado, nenhum deploy, nenhum build, nenhum commit/push. Nada tocado em
`lib/Unity.TextMeshPro.dll`, `tools/automacao/estilo/**`, `tools/automacao/aceite/**`,
`RoguelikeSkillTreeVisualizer/**` nem `tools/testes/*rstv*`.

Arquivos mexidos: **só `tools/automacao/runtime/**` e `docs/automacao/AUT-4-*.{json,md}` + este relatório
+ `docs/automacao/COR-AUT4-F2-evidencias/`** (mesma restrição declarada em `AUT-4-estado.json`).

---

## 0. Veredito por item (o que o pai pediu)

| item | severidade (COR-AUT4R) | veredito | resumo |
|---|---|---|---|
| **A1-c** | baixo | **FECHADO** | a prova (c) agora exige que o print seja **posterior ao lançamento** (`mtime >= lancamento_epoca`); PNG de rodada anterior no `out_dir` reusado → `INDETERMINADO`/exit 1 |
| **A2** | grave | **FECHADO** | `_estado_do_campo` trata **vazio** (`""` / só-espaços / `[]` / `{}`) como **AUSENTE = não lido`; a fixture e o stub da regressão passaram a usar a **forma REAL** do artefato (`texto_renderizado: ""`, não `null`) |
| **A3** | médio | **FECHADO** | `evidencia_runtime: false` **sozinho** já é declaração de fixture → `FIXTURE`/exit 2 (nunca mais é invertido para `runtime`/`true`) |
| **A6** | médio | **FECHADO** | a prova de ida-e-volta exige o **marcador gerado pelo driver**; `{conferiu: true}` sem marcador (ou com outro) não confere → `INDETERMINADO`/exit 1 |
| A2 (secundário) | — | **FECHADO** | `executar_rodada` valida o plano **antes** de instalar/lançar; `campos_alvo` inválido → `PLANO_INVALIDO`/exit 2 sem tocar no perfil |
| A4 / A5 / A7 | — | **intocados** (já OK na COR-AUT4R) | — |

Nenhum critério de aceite foi afrouxado: todas as mudanças **reforçam** a trava (só criam mais lacuna /
mais exigência / mais recusa). O runner ficou verde (9/9 e 15/15) **depois** de cada correção ter sido
vista reprovando com o defeito plantado.

---

## 1. (a) Arquivos alterados — caminho:linha

| arquivo | o que mudou (linha no disco final) |
|---|---|
| `tools/automacao/runtime/coletor.py` | `_estado_do_campo` — vazio = AUSENTE: `l.197` (docstring), `l.207` (string vazia/só-espaços), `l.210` (`[]`/`{}`) |
| 〃 | `provas_de_execucao` — print datado: `l.813` (`fresco` = mtime ≥ lançamento), `l.818` (`prints_ok` exige `posterior_ao_lancamento`) |
| 〃 | `consolidar_probe` — A3: `l.531` (`evidencia_runtime is False` basta, sem `rotulo`) |
| 〃 | `executar_rodada` — plano validado antes de tocar o perfil: `l.893` (`plano = validar_plano(plano)` → `PLANO_INVALIDO`/exit 2) |
| 〃 | `executar_rodada` — A6 marcador obrigatório: `l.1001` (`marcador == marcador_ida_volta`) |
| `tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json` | `l.43` `texto_renderizado: ""` (forma REAL, era `null`); `l.52` `owners` do objeto inativo = mesma lista do ativo (o probe emite **uma** lista global por rodada — `AUT4ProbePlugin.cs` `OwnersDosFunils()` passado a toda `Leitura()`) |
| `tools/automacao/runtime/testes/t_aut4_execucao.py` | stub: `l.105` flag `--print-velho`, `l.130` inativo com `""`, `l.151` flag `--ida-volta-sem-marcador`; testes: `l.368` (A1c), `l.413` (A6m), `l.422` (A2-sec) |
| `tools/automacao/runtime/testes/t_aut4_costura_probe.py` | `l.167` (A3 F2: `evidencia_runtime=false` sozinho → `FIXTURE`), `l.213` (A2 F2: `""`/`[]`/`{}` → lacuna) |
| `tools/automacao/runtime/testes/contra-prova/cp_aut5_isca_print_velho_ok.py` | **novo** — isca A1-c (arquivo inteiro) |
| `tools/automacao/runtime/testes/contra-prova/cp_aut5_isca_alvo_vazio_ok.py` | **novo** — isca A2 (arquivo inteiro) |
| `tools/automacao/runtime/testes/contra-prova/cp_aut5_isca_evidencia_runtime_false_ok.py` | **novo** — isca A3 (arquivo inteiro) |
| `tools/automacao/runtime/testes/contra-prova/cp_aut5_isca_ida_volta_sem_marcador.py` | **novo** — isca A6 (arquivo inteiro) |
| `docs/automacao/AUT-4-estado.json` | lista de iscas 11→15, `iscas_reprovaram_como_deviam` 15, `driver_sha256` novo, bloco `achados_cor_aut4r_fechados_f2` |
| `docs/automacao/AUT-4-preparacao.md` | contagens `11 iscas`→`15 iscas` + nota COR-AUT4-F2 |
| `docs/automacao/COR-AUT4-F2-evidencias/` | `adv_f2.py`, `adv_base.log`, `adv_final.log`, `planta_cor_aut4f2.py`, `planta_cor_aut4f2.log`, `suite-final.log`, `contra-prova-final.log`, `hashes.txt` |

---

## 2. (d) sha256 do que eu medi

```
155b8ffe58ebdeda6d191d1b789fe3731a5d56c58962631216f0f2adf8b3f578  tools/automacao/runtime/coletor.py
9b8893ef55d5d79f8ceb6332bacd4f3186eaba22f14c31a0231bdebcd6de7051  tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json
afe6131ff9d1596cbaf575417a01a6e5d9284700c769754efeddf342f156309f  tools/automacao/runtime/testes/t_aut4_execucao.py
bd6e2dee763ce6fa91fab92c08ae98a2629efbb10003cbb941575166ab252f97  tools/automacao/runtime/testes/t_aut4_costura_probe.py
93ce41fc13b2b8ff8b59c238668898afd5cfd7c035babdb9c2a7ba6e5484e799  .../contra-prova/cp_aut5_isca_print_velho_ok.py
36e4c45a2b69add76eafff7c16e546888612c95d6c94cec19fd4cb5a3b402181  .../contra-prova/cp_aut5_isca_alvo_vazio_ok.py
e25b633f0b9c873f0e2f85263999c81d9ad42bf7640f5f48d9834e6cc0fd81d8  .../contra-prova/cp_aut5_isca_evidencia_runtime_false_ok.py
0df7a56b911fd119934c331588f1c433da41c8eb8823454d39101e6a45361170  .../contra-prova/cp_aut5_isca_ida_volta_sem_marcador.py
5ed26c540a8cf95f17884b0cb4d3bef75ae10fbb15517894c0f0e51dc01476f9  docs/automacao/AUT-4-estado.json
3bb7e34c7f764609146ca5189ca89d4bb4fffecfc0b753b27ec2f522d1df65e4  docs/automacao/AUT-4-preparacao.md
769ec5cab2ba5eadbc69535fe85588c618c74727f9625a31fa50fa191ab81f59  tools/automacao/runtime/roda_testes_runtime.py   (runner: NÃO alterado)
fd774259b5e8813f2f3b29e2ff805f12cb0cdab4c277116fcc8bbb7e7e3bffdd  tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll  (NÃO alterado)
5a51abaa439b90263e3b202e01a0b2b3b343fabc8cb71c9de8b3ac97b343bdd3  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs  (NÃO alterado)
```

Cópia de execução: `C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4f2/{base,fix}` — conferida
byte a byte contra o repo (`cmp`, **sem diferenças**) antes de cada medição.

---

## 3. (b/c) Comandos exatos + saída literal + exit code

### 3.1 Baseline (bytes ORIGINAIS, antes da correção)

```
$ cd <copia-base> && python tools/automacao/runtime/roda_testes_runtime.py
 VEREDITO: VERDE (exit 0) — 9 teste(s)          EXIT=0
$ ... --contra-prova
 VEREDITO: VERDE (exit 0) — 11 teste(s)         EXIT=0
```

### 3.2 Árvore corrigida (bytes finais)

```
$ cd <copia-fix> && python tools/automacao/runtime/roda_testes_runtime.py
[PASSOU] t_aut4_autorizacao.py … t_aut4_probe_contrato.py   (9/9)
 VEREDITO: VERDE (exit 0) — 9 teste(s)          EXIT=0
$ ... --contra-prova
[PROVA OK (reprovou como devia)] … as 15 iscas
 VEREDITO: VERDE (exit 0) — 15 teste(s)         EXIT=0
$ echo $?
0
```
Logs literais: `COR-AUT4-F2-evidencias/suite-final.log` (exibe `SUITE_EXIT=0`) e
`contra-prova-final.log` (`CP_EXIT=0`).

### 3.3 Contra-prova de VERDADE — defeito plantado por mim (`planta_cor_aut4f2.py`)

Reverte a correção de cada achado numa cópia descartável e mede o runner. Trecho literal do log
(`COR-AUT4-F2-evidencias/planta_cor_aut4f2.log`):

```
DEFEITO PLANTADO: A1c  ->  suite exit=1 | contra-prova exit=1
   [REPROVOU] testes\t_aut4_execucao.py
   | RESULTADO|REPROVOU|aut4-execucao|A1c: print ANTERIOR a rodada nao vale (mesmo existindo com bytes>0): esperado False, obtido True
   [PROVA FALHOU (passou quando devia reprovar)] testes\contra-prova\cp_aut5_isca_print_velho_ok.py
   VEREDITO: VERMELHO (exit 1)

DEFEITO PLANTADO: A2   ->  suite exit=1 | contra-prova exit=1
   [REPROVOU] testes\t_aut4_costura_probe.py
   | RESULTADO|REPROVOU|aut4-costura-probe|B3: inativo declara rendered como N/A: esperado 'NAO_APLICAVEL', obtido 'PRESENTE'
   [REPROVOU] testes\t_aut4_execucao.py
   | RESULTADO|REPROVOU|aut4-execucao|A2/I: objeto inativo com alvo nao lido NAO pode consolidar CONFIRMADA
   [PROVA FALHOU (passou quando devia reprovar)] cp_aut5_isca_alvo_nao_lido_ok.py
   [PROVA FALHOU (passou quando devia reprovar)] cp_aut5_isca_alvo_vazio_ok.py
   VEREDITO: VERMELHO (exit 1)

DEFEITO PLANTADO: A3   ->  suite exit=1 | contra-prova exit=1
   [REPROVOU] testes\t_aut4_costura_probe.py
   | RESULTADO|REPROVOU|aut4-costura-probe|A3 (F2): evidencia_runtime=false sozinho tem de sair FIXTURE: esperado 'FIXTURE', obtido 'CONFIRMADA'
   [PROVA FALHOU (passou quando devia reprovar)] cp_aut5_isca_evidencia_runtime_false_ok.py
   VEREDITO: VERMELHO (exit 1)

DEFEITO PLANTADO: A6   ->  suite exit=1 | contra-prova exit=1
   [REPROVOU] testes\t_aut4_execucao.py
   | RESULTADO|REPROVOU|aut4-execucao|A6m: autodeclaracao SEM o marcador do driver NAO pode conferir: esperado False, obtido True
   [PROVA FALHOU (passou quando devia reprovar)] cp_aut5_isca_ida_volta_sem_marcador.py
   VEREDITO: VERMELHO (exit 1)

SEM DEFEITO (arvore final)  ->  suite exit=0 | contra-prova exit=0
   suite:     VEREDITO: VERDE (exit 0) — 9 teste(s)
   contra:    VEREDITO: VERDE (exit 0) — 15 teste(s)
```

**Leitura:** cada defeito plantado derruba o runner para **exit 1** (VERMELHO) e faz a isca do achado
**PASSAR** — isca decorativa não é: ela só é verde quando o defeito existe. Sem o defeito, exit 0.

### 3.4 Sondas adversariais da COR-AUT4R re-medidas (`adv_f2.py`)

Reproduzi as repro da COR-AUT4R (S1/V1/S3/S4) com uma sonda própria, contra os **bytes originais** e
contra a **árvore corrigida** (`adv_base.log` / `adv_final.log`):

```
### BASE (bytes originais)                         ### FINAL (corrigida)
S1  PNG VELHO  : CONCLUIDO    exit=0               S1  PNG VELHO  : INDETERMINADO exit=1  (print datado)
S1c controle   : CONCLUIDO    exit=0               S1c controle   : CONCLUIDO     exit=0  (não regrediu)
V1  rend=''    : CONFIRMADA   exit=0 lacunas=[]    V1  rend=''    : INCOMPLETO    exit=1 lacunas=['texto_renderizado']
V1c rend=None  : INCOMPLETO   exit=1               V1c rend=None  : INCOMPLETO    exit=1
V(owners  ) [] : PRESENTE lacunas=[]               V(owners  ) [] : AUSENTE       lacunas=['owners']
V(keywords) {} : PRESENTE lacunas=[]               V(keywords) {} : AUSENTE       lacunas=['keywords']
V(cores   ) {} : PRESENTE lacunas=[]               V(cores   ) {} : AUSENTE       lacunas=['cores']
S3  ev_runtime=false: CONFIRMADA exit=0 evr=True    S3  ev_runtime=false: FIXTURE exit=2 evr=False
S4  sem masc   : CONCLUIDO    exit=0 ida_ok=True    S4  sem masc   : INDETERMINADO exit=1 ida_ok=False
S4  com masc   : CONCLUIDO    exit=0 ida_ok=True    S4  com masc   : CONCLUIDO     exit=0 ida_ok=True  (controle+)
S4  masc errado: INDETERMINADO exit=1 ida_ok=False  S4  masc errado: INDETERMINADO exit=1 ida_ok=False
```

A coluna BASE **reproduz exatamente** a repro da COR-AUT4R (S1 `CONCLUIDO/0`, V1 `CONFIRMADA/0`, V( )=
`PRESENTE`, S3 `CONFIRMADA/0 evr=True`, S4 sem marcador `CONCLUIDO/0`). A coluna FINAL fecha todas, e os
controles positivos (S1c, S4 com marcador correto) continuam verdes.

---

## 4. O que mudou, por achado

### A1-c — datar os prints
`provas_de_execucao` passou a exigir, para **cada** arquivo de `prints`, `mtime + 1e-3 >= lancamento_epoca`
(o `out_dir` é reusado por desenho; um `01-ui.png` de rodada anterior não vale). Novo teste em
`t_aut4_execucao.py` (caso A1c) e isca `cp_aut5_isca_print_velho_ok.py`.

### A2 — vazio é não lido (e a fixture usa a forma REAL)
`_estado_do_campo`: string vazia/só-espaços e contêiner vazio (`[]`, `{}`) → `AUSENTE`; alvo nesse estado
(ou no fallback `NAO_APLICAVEL`) vira **lacuna** → `INCOMPLETO`. Fixture
`probe-saida-exemplo.entrada.json` passou a codificar `texto_renderizado: ""` (a forma que o probe C#
emite — `GetParsedText()` → `string.Empty`; `Trunc` só devolve `null` para entrada `null`) e o stub da
regressão (`t_aut4_execucao.py`, `--inativo`) também. Assertivas novas em `t_aut4_costura_probe.py` e
`t_aut4_execucao.py`; isca `cp_aut5_isca_alvo_vazio_ok.py`.

> **Nota de fidelidade (auditável):** o campo `owners` da observação INATIVA da fixture passou de `[]`
> para a mesma lista da observação ativa. Motivo **medido no fonte do probe**: `owners` é a **mesma**
> lista global de funis (`OwnersDosFunils()` em `ColetarObservacoes`, passada a toda `Leitura()`,
> `AUT4ProbePlugin.cs` l.405/413/452) — logo toda observação traz o mesmo `owners`. Deixar `[]` no
> inativo era infiel ao artefato. A regra "vazio = não lido" **não perdeu cobertura**: `owners=[]`,
> `keywords={}` e `cores={}` são checados explicitamente na suíte e na isca nova.

### A2 (secundário) — validar o plano antes de agir
`executar_rodada` chama `validar_plano` logo após o portão de autorização e **antes** de instalar/escrever
o `.cfg`/lançar: `campos_alvo` inválido → `PLANO_INVALIDO`/exit 2, perfil intacto (o teste A2-sec prova
que o stub **não** rodou e que nem probe nem `.cfg` nasceram).

### A3 — precedência do "não é runtime"
`consolidar_probe`: `rotulado_fixture = (procedencia == "fixture") or (evidencia_runtime is False)` — o
`rotulo_fixture` deixou de ser pré-requisito. Artefato que só declara `evidencia_runtime: false` sai
`FIXTURE`/exit 2, sem inverter o próprio campo. Teste em `t_aut4_costura_probe.py` + isca
`cp_aut5_isca_evidencia_runtime_false_ok.py`.

### A6 — exigir o marcador do driver
`executar_rodada`: `conferiu = bool(ida_volta.get("conferiu")) and str(ida_volta.get("marcador") or "") == str(marcador_ida_volta)`.
Marcador **ausente** ou **diferente** não confere → `INDETERMINADO`/exit 1. Teste em `t_aut4_execucao.py`
(caso A6m) + isca `cp_aut5_isca_ida_volta_sem_marcador.py`.

---

## 5. Não-regressão — outros consumidores do `coletor.py`

O `coletor.py` é importado por outras frentes (`aut5`, `aut6`, `cenarios`, `ciclo`, `estilo`). Para garantir
que a correção do A2 (vazio = não lido) e a fidelidade da fixture **não regridem** esses consumidores,
rodei as 4 suítes que chamam `normalizar_observacao`/`consolidar_probe` sobre uma **cópia completa do
repo** (314 MB, fora do repo), com o coletor+fixture **originais** e depois com os **corrigidos**:

```
                                         BASE (originais)   FINAL (corrigidos)
tools/automacao/cenarios/test_rstv.py    exit 0             exit 0     (saída IDÊNTICA)
tools/automacao/aut5/test_aut5.py        exit 0             exit 0     (saída IDÊNTICA)
tools/automacao/aut6/test_regressoes_cor_aut6.py  exit 0    exit 0     (saída IDÊNTICA; só o tempo difere)
tools/automacao/ciclo/test_decisao.py    exit 0             exit 0     (saída IDÊNTICA)
```

`tools/automacao/estilo/**` (frente COR-AUT7-F2, viva) **não foi tocado**; ela usa só `validar_plano`/
`planejar_rodada` do coletor, que **não mudaram** nesta entrega. Logs em
`COR-AUT4-F2-evidencias/cons-*`.

---

## 6. Lacunas declaradas (NUNCA OK)

- **Nada em jogo foi exercitado.** Toda a prova é OFFLINE (byte + stub de lançamento). Leitura real do
  objeto vivo, PNG pela API do Unity, `owners` Harmony vivos, `Tooltip.ShowTooltip` real e o rollback em
  jogo seguem **NÃO EXERCITADOS** — dependem de autorização explícita do dono (CIC-5).
- A porta opt-in de ida-e-volta existe no fonte **e** no binário, e agora o driver **exige** o marcador —
  mas continua **nunca executada** em sessão viva.
- Esta entrega **não** fecha o DoD e **não** substitui o aceite humano. A revisão fica com o pai
  (COR-AUT4-F2R).
