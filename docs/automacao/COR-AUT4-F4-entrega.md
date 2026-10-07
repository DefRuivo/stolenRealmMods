# COR-AUT4-F4 — entrega: presença de `evidencia_runtime` derivada internamente

Rodada: COR-AUT4-F4 (achado residual não bloqueante do parecer independente COR-AUT4-F3R).
Escopo: `tools/automacao/runtime/coletor.py`. **Não** foram instalados mods, **não** se abriu o
jogo, **não** se publicou, **não** se commitou (`git add` nenhum; nada em stage). Nenhum arquivo
em `tools/automacao/estilo/**`, `aceite/**` ou fontes de mods foi tocado.

---

## 1. Defeito

O `consolidar_probe` decidia o próprio veredito por uma chave **interna que o artefato carrega**:

`coletor.py:547` (estado pré-conserto): `declarada_ev = bool(saida.get("evidencia_runtime_presente"))`,
onde `evidencia_runtime_presente` vinha do `_mapear_saida_probe`, que **confiava no valor do próprio
dado de entrada**:

```python
"evidencia_runtime_presente": (
    bool(dados["evidencia_runtime_presente"])
    if "evidencia_runtime_presente" in dados
    else "evidencia_runtime" in dados),
```

Um artefato com `evidencia_runtime: "false"` (forma errada) **e** `evidencia_runtime_presente: false`
(ou `0`) declarava "sem evidência" → a presença caía para `False` → o caminho legítimo
"chave ausente = runtime" era tomado de empréstimo → **CONFIRMADA, exit 0**, com o campo invertido
para `true`. O artefato governava o próprio veredito.

Reprodução direta (script fora do repo, `repro_f4.py`), estado **pré-conserto**:

```
status   = CONFIRMADA
exit     = 0
campo ev = True
VEREDITO = DEFEITO VIVO (confirmou como runtime)
EXIT=1
```

---

## 2. Conserto — arquivo:linha

Arquivo: **`tools/automacao/runtime/coletor.py`**

- `coletor.py:51` — classe `_MarcaMapeado` (sentinel de **identidade**, `__copy__`/`__deepcopy__`
  devolvem a mesma instância; não é serializável para JSON).
- `coletor.py:70-71` — `_CHAVE_MAPEADO = "_cor_aut4_mapeado"` e `_MARCA_MAPEADO = _MarcaMapeado()`.
- `coletor.py:502-505` (dentro de `_mapear_saida_probe`, agora em `coletor.py:477`) — a presença
  passa a ser derivada **internamente** da entrada crua:

  ```python
  if dados.get(_CHAVE_MAPEADO) is _MARCA_MAPEADO:
      presente = bool(dados.get("evidencia_runtime_presente"))
  else:
      presente = "evidencia_runtime" in dados
  ```

- `coletor.py:517` — o dict mapeado recebe o marcador `_CHAVE_MAPEADO: _MARCA_MAPEADO`.
- `coletor.py:579` e `coletor.py:584` — comentários citando **COR-AUT4-F4** na docstring de
  `_mapear_saida_probe` (a partir de `coletor.py:484`) e no bloco de decisão do `consolidar_probe`.

**Regra que fica valendo (não enfraquece trava nenhuma — mantém o julgado OK na COR-AUT4-F3R):**

| entrada | presença | veredito |
|---|---|---|
| dict cru do probe, chave `evidencia_runtime` AUSENTE | `False` | runtime (CONFIRMADA / exit 0) |
| dict já mapeado (2ª passagem), chave ausente | `False` (preservada) | runtime (CONFIRMADA / exit 0) |
| JSON lido do arquivo, chave ausente | `False` | runtime (CONFIRMADA / exit 0) |
| `evidencia_runtime: true` (bool legítimo) | `True` | runtime (CONFIRMADA / exit 0) |
| `evidencia_runtime: false` (bool) | `True` | FIXTURE / exit 2 |
| forma errada (`"false"`, `0`, `"0"`, `null`, `1`, `"true"`) | `True` | FIXTURE / exit 2 |
| forma errada **+ `evidencia_runtime_presente: false`/`0`** | `True` (entrada crua) | **FIXTURE / exit 2** |

### Pitfall da idempotência — resolvido explicitamente

O dict **já mapeado** SEMPRE tem a chave `evidencia_runtime` (com `None` quando o probe real não a
emite); re-derivar de `"evidencia_runtime" in dados` transformaria "chave ausente = runtime" em
FIXTURE na 2ª passagem. Por isso o marcador de **identidade** `_MARCA_MAPEADO`: um JSON/artefato
nunca o traz (não é valor JSON), então só o dict produzido pelo próprio mapeador é tratado como
"já mapeado", e a presença derivada na 1ª passagem é preservada. Demonstração literal nos três
caminhos (`demo_f4_presenca.py`, contra o repo corrigido):

```
dict CRU do probe (chave ausente)              presenca=False -> CONFIRMADA exit=0
dict JA MAPEADO (2a passagem, chave ausente)   presenca=False -> CONFIRMADA exit=0
    -> chave interna no mapeado: <mapeado-pelo-coletor>
JSON lido do arquivo (chave ausente)           presenca=False -> CONFIRMADA exit=0
artefato mente presente=false (chave real AUSENTE) presenca=False -> CONFIRMADA exit=0
artefato FORMA ERRADA + presente=false         presenca=True  -> FIXTURE    exit=2
bool True legitimo                             presenca=True  -> CONFIRMADA exit=0
EXIT=0
```

Mesmo script contra a cópia **com o defeito plantado** (comportamento pré-conserto):

```
artefato FORMA ERRADA + presente=false         presenca=False -> CONFIRMADA exit=0   <-- defeito
```

---

## 3. Comandos exatos, saída literal e exit code

### 3.1 RED — antes do conserto (repo, regressão nova já no lugar)

```
$ python tools/automacao/runtime/roda_testes_runtime.py
==========================================================================
 AUT-4 runtime — suite offline
 raiz: C:\dev\stolen-realm\tools\automacao\runtime
==========================================================================
[PASSOU                                    ] testes\t_aut4_autorizacao.py
[PASSOU                                    ] testes\t_aut4_controle_negativo.py
[REPROVOU                                  ] testes\t_aut4_costura_probe.py
        | RESULTADO|REPROVOU|aut4-costura-probe|F4: campo presente em forma errada + presente=False tem de sair FIXTURE: esperado 'FIXTURE', obtido 'CONFIRMADA'
[PASSOU                                    ] testes\t_aut4_estado_docs.py
[PASSOU                                    ] testes\t_aut4_execucao.py
[PASSOU                                    ] testes\t_aut4_manifest_rollback.py
[PASSOU                                    ] testes\t_aut4_observacao.py
[PASSOU                                    ] testes\t_aut4_plano.py
[PASSOU                                    ] testes\t_aut4_probe_contrato.py
==========================================================================
 VEREDITO: VERMELHO (exit 1)
EXIT=1
```

### 3.2 GREEN — depois do conserto

```
$ python tools/automacao/runtime/roda_testes_runtime.py
...
[PASSOU                                    ] testes\t_aut4_costura_probe.py
...
 VEREDITO: VERDE (exit 0) — 9 teste(s)
EXIT=0
```

```
$ python tools/automacao/runtime/testes/t_aut4_costura_probe.py     # direto, repo corrigido
RESULTADO|PASSOU|aut4-costura-probe|topo->observacao (B1), extras preservados (B2), alvo por cenario governa o veredito (A2), procedencia do artefato vence (A3), status de falha rebaixa (A4)
EXIT=0
```

### 3.3 Controle positivo / negativo do conserto (script isolado)

```
# antes (repo pré-conserto): status=CONFIRMADA exit=0 campo ev=True
# depois (repo corrigido):
$ python .../scratch/repro_f4.py
status   = FIXTURE
exit     = 2
campo ev = False
VEREDITO = OK (FIXTURE/exit2)
EXIT=0
```

### 3.4 Regressão nova

Adicionada como bloco novo **COR-AUT4-F4** em `tools/automacao/runtime/testes/t_aut4_costura_probe.py:263-330`
(arquivo já existente — evita renomear a lista de testes declarada em
`docs/automacao/AUT-4-estado.json`, que é cobrada por `t_aut4_estado_docs.py`). Cobre:

- forma autocontraditória de verdade: `evidencia_runtime: "false"` + `evidencia_runtime_presente: false`/`0` → FIXTURE / exit 2 (linhas 268-278);
- bool `false` canônico + `presente=false` → FIXTURE / exit 2 (linhas 281-285);
- artefato mentindo `presente=true` para chave **ausente** → continua runtime (linhas 288-295);
- idempotência: dict cru, JSON de arquivo e dict **já mapeado** sem a chave → runtime (linhas 297-323);
- dict mapeado do artefato autocontraditório → FIXTURE / exit 2 (linhas 324-328).

A regressão **falhou antes** (§3.1) e **passa depois** (§3.2): não é teste que nunca falhou.

---

## 4. Contra-prova em cópia FORA do repo

Cópias em `C:/Users/Pichau/AppData/Local/hermes/cache/scratch/` (fora de `C:/dev/stolen-realm`):

- `cp_f4_sem_defeito/` — árvore `tools/` + `docs/automacao/` com o **conserto**.
- `cp_f4_com_defeito/` — mesma árvore com o **defeito plantado** (presença lida da chave do próprio
  artefato, o código pré-conserto).

```
$ cd cp_f4_com_defeito && python tools/automacao/runtime/roda_testes_runtime.py
[REPROVOU                                  ] testes\t_aut4_costura_probe.py
        | RESULTADO|REPROVOU|aut4-costura-probe|F4: campo presente em forma errada + presente=False tem de sair FIXTURE: esperado 'FIXTURE', obtido 'CONFIRMADA'
 VEREDITO: VERMELHO (exit 1)
EXIT_COM_DEFEITO=1

$ cd cp_f4_sem_defeito && python tools/automacao/runtime/roda_testes_runtime.py
...
 VEREDITO: VERDE (exit 0) — 9 teste(s)
EXIT_SEM_DEFEITO=0
```

Iscas (contra-prova) nas duas cópias — todas reprovam como devem, `exit 0`:

```
$ python tools/automacao/runtime/roda_testes_runtime.py --contra-prova   # nas duas cópias
ISCA_EXIT_COM_DEFEITO=0
ISCA_EXIT_SEM_DEFEITO=0
```

sha256 das cópias (confirmam que são arquivos distintos do repo):

```
1875fef1708ee149f1a0e63ff505f5955c00ef373cb40d52ec1c90d0e9bdb8a9  cp_f4_com_defeito/.../coletor.py   (defeito plantado)
dee03a8fd16d95730ede993a14747406a37ba44f8a7ea97a6a666995fb7ef3e5  cp_f4_sem_defeito/.../coletor.py   (== repo)
```

---

## 5. Suite completa do runtime + não-regressão dos consumidores

```
$ python tools/automacao/runtime/roda_testes_runtime.py
 VEREDITO: VERDE (exit 0) — 9 teste(s)     EXIT_SUITE=0

$ python tools/automacao/runtime/roda_testes_runtime.py --contra-prova
 VEREDITO: VERDE (exit 0) — 16 teste(s)    EXIT_CP=0
```

Consumidores de `evidencia_runtime` (todos verdes, exit 0):

```
tools/automacao/cenarios/test_rstv.py            RESULTADO|PASSOU|cic3-rstv|...            EXIT=0
tools/automacao/cenarios/test_tooltips_shrines.py  TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0  EXIT=0
tools/automacao/aut6/test_cobertura_aut6.py      TOTAL|rodaram=24 reprovaram=0            EXIT=0
tools/automacao/aut6/test_regressoes_cor_aut6.py Ran 26 tests ... OK                      EXIT=0
tools/automacao/estilo/test_estilo_atributos.py  total: 28 | falhas: 0  TUDO OK            EXIT=0
```

(`cenarios/rstv.py`, `cenarios/tooltips_shrines.py`, `aut6/prova.py` e `estilo/estilo_atributos.py`
são módulos exercitados pelas suites acima; os módulos foram apenas lidos, não editados —
`tools/automacao/estilo/**` intocado.)

---

## 6. sha256 dos arquivos tocados

```
dee03a8fd16d95730ede993a14747406a37ba44f8a7ea97a6a666995fb7ef3e5  tools/automacao/runtime/coletor.py
57a02638b12bb641c348e75440f841cafe2592d3d270d5c7c94d8e7dad8bffca  tools/automacao/runtime/testes/t_aut4_costura_probe.py
```

Ambos os arquivos estão **untracked** (`??`) e nada foi para o stage:

```
$ git status --short tools/automacao/runtime/coletor.py tools/automacao/runtime/testes/t_aut4_costura_probe.py
?? tools/automacao/runtime/coletor.py
?? tools/automacao/runtime/testes/t_aut4_costura_probe.py
$ git diff --cached --name-only     # vazio
```

## 7. Notas

- Nenhuma trava foi enfraquecida para "ficar verde": o conserto **endurece** a decisão (o artefato
  deixa de governar o próprio veredito) e preserva o julgado OK da COR-AUT4-F3R (`chave ausente =
  runtime`, `bool true legítimo = runtime`).
- Não foi necessário tocar em `docs/automacao/AUT-4-estado.json` nem em `AUT-4-preparacao.md`:
  a regressão entrou como bloco num arquivo de teste já existente, mantendo a contagem
  testes/iscas declarada × disco.
- Scripts de apoio (fora do repo, em scratch): `repro_f4.py`, `demo_f4_presenca.py`.
