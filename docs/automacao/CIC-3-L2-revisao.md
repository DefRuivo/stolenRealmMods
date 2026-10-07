# CIC-3-L2R2 — REVISÃO INDEPENDENTE (por item) da correção do campo `arestas_inventadas`

> **Quem sou eu nesta rodada.** Sou a tarefa de **revisão independente** do cartão `t_f7cc7cbb`
> (CIC-3-L2) — **revisor ≠ autor**. Tentei **REFUTAR** a correção; não a confirmei por inércia.
> Não commitei, não fiz `git add` de diretório/`-A`, não pushei, não instalei mod, não abri o jogo,
> não publiquei, não deployei, não criei/mutei tarefa no Kanban. O **único** arquivo escrito por mim
> dentro do repo é **este** (`docs/automacao/CIC-3-L2-revisao.md`).
>
> **Objeto:** `tools/automacao/cenarios/rstv.py` + `test_rstv.py` — fechamento do achado residual **L2**
> do parecer `docs/automacao/CIC-3R2-revisao.md` (§7 L2): no campo `arestas_inventadas`, a forma
> **malformada** (`"2"` string) fechava critério `OK` enquanto o inteiro canônico `2` REPROVAVA — classe
> F2/F3 do projeto ("o campo governa o próprio veredito"). Cabeça do cartão lida em
> `%LOCALAPPDATA%/hermes/cache/scratch/l2-arestas-body.md` (sha256 `47c04824…`, critérios 1-6 conferidos).
>
> **Método:** sonda **própria** (não a do autor), **brute-force** de 2037 valores nos **dois** bytes
> (`orig` × `atual`) no mesmo processo, tabela `antes × depois`, e **contra-prova em cópia FORA do repo**
> (`%LOCALAPPDATA%/hermes/cache/scratch/l2rev/`). Todo teste foi **mostrado REPROVANDO** contra o defeito
> plantado. Exit 0/1/2 são distintos (arcabouço: `Falhou`→1, `NaoRodou`→2); nenhum teste foi pulado.

---

## 0. VEREDITO POR ITEM (resumo)

| # | Critério do cartão | Veredito | Prova (âncora) |
|---|---|---|---|
| 1 | string `"2"` não fecha OK (cai em não-OK) | **OK** | §3.1 / §3.4 |
| 2 | canônico legítimo (inteiro, bool, chave ausente) preservado | **OK** | §3.2 |
| 3 | regressão nova (string-de-número + borda: vazia, float, None) | **OK** | §3.3 |
| 4 | contra-prova em cópia fora do repo: defeito→vermelho 1, sem→verde 0 | **OK** | §3.4 |
| 5 | não-regressão (suíte do módulo + consumidores) | **OK** | §3.5 |
| 6 | relatório com arquivo:linha, comandos, exit code e sha256 | **OK** | §3.6 |

**Veredito global: APROVADO** — a correção fecha o L2, **não enfraquece a trava** (zero transição
`REPROVADO → OK`) e a entrega documental (critério 6) **existe e é reproduzível**.
Há **4 observações** (não-OK, não bloqueantes) e **pendências do dono** — §5 e §6.

---

## 1. Estado lido (sha256 medido por MIM, no disco, 2026-10-06 ~16:47)

| caminho | sha256 (medido nesta revisão) |
|---|---|
| `tools/automacao/cenarios/rstv.py` | `e1ad69fc6128b7403363dd4efeefaf9614d1be0437fe71f90079ebb5547bf60f` |
| `tools/automacao/cenarios/test_rstv.py` | `460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262` |
| `tools/automacao/cenarios/test_tooltips_shrines.py` | `8fcba1c3ba8af9ff8bcf4b3db115a333e6799d364ea3fe8102cfbf971b9df885` |
| `tools/automacao/cenarios/tooltips_shrines.py` | `65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199` |
| `tools/automacao/cenarios/rstv-identidade.json` | `5cec628c011e5bc5f249fc649401eed20ee65eccaf40aafa33389d7ef2792f86` |
| `tools/testes/arcabouco.py` (harness) | `08b4dd51c1d2bd851cf0d5d2b2f038dbe3f1094ab4c625ed63a7a4dc97c20afb` |
| `docs/automacao/CIC-3R2-revisao.md` (a régua do achado L2) | `a5013f42484b6b518f8b884b6ea7d7284e8376f98d0a24683ca081a0a2c8b8cc` |
| `docs/automacao/CIC-3-L2R-revisao.md` (revisão anterior) | `a05a6a30c9274af1a0f2ac33fab59193c557420e2cfe4e326cf4db0e7d221d1b` |
| `docs/automacao/CIC-3-L2-entrega.md` (o relatório do autor) | `f8ccfbe86853777d1f9e9dd9c487763859b04d287e2468c4b3e7c04e5ea4e80c` |

- mtime do produto: `rstv.py` e `test_rstv.py` = **2026-10-06 16:24**.
- `tools/automacao/` é **untracked** (`git status --porcelain` → `?? tools/automacao/`); nada no stage
  (`git diff --cached --name-only` → vazio). `git status` idêntico **antes e depois** de todas as minhas
  execuções (`md5` do status = `a8fd3197…` nas duas pontas) — meus testes **não** mutaram o repo.
- **Conferência de deriva:** após TODAS as execuções desta revisão, `rstv.py`/`test_rstv.py` seguem com os
  mesmos sha256 acima (nenhuma escrita minha nos alvos).

---

## 2. A "lacuna conhecida" — **REFUTO**

A premissa recebida era "não existe `docs/automacao/CIC-3-L2-*.md` no disco". **Falso.** Existem **dois**:

```
$ ls -la --time-style=full-iso docs/automacao/CIC-3-L2*
-rw-r--r-- ... 16801 2026-10-06 16:40:56 docs/automacao/CIC-3-L2-entrega.md
-rw-r--r-- ... 13612 2026-10-06 16:37:28 docs/automacao/CIC-3-L2R-revisao.md
```

O `CIC-3-L2-entrega.md` (16801 bytes, 16:40) é exatamente o **relatório de execução do critério 6** — a
ressalva que a revisão anterior (`CIC-3-L2R`, item 8) havia dado como **não cumprida**. Ele foi escrito
**depois** daquela revisão (16:37) e **fecha** a lacuna. Ver §3.6.

---

## 3. PROVA POR ITEM (comando exato + saída literal + exit code)

### Item 1 — `arestas_inventadas="2"` (string) NÃO fecha OK — **OK**

Sonda **própria** (`probe_forms.py`, sha256 `be63911b…`), montando a própria observação completa e
chamando `avaliar` no `rstv.py` **do repo**:

```
$ python -B %SCRATCH%/l2rev/probe_forms.py C:/dev/stolen-realm/tools/automacao/cenarios/rstv.py
forma                | estado          | prova_runtime | motivo(recorte)
str "2"              | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventada...
str ""               | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventada...
str " "              | NAO_EXERCITADO  | False         | ...
str "NaN"            | NAO_EXERCITADO  | False         | ...
str "Infinity"       | NAO_EXERCITADO  | False         | ...
str "abc" / "-1"     | NAO_EXERCITADO  | False         | ...
lista [] / [1,2]     | NAO_EXERCITADO  | False         | ...
dict {} / {'a':1}    | NAO_EXERCITADO  | False         | ...
tupla () / set()     | NAO_EXERCITADO  | False         | ...
negativo -1 / -2.5   | NAO_EXERCITADO  | False         | ...
-inf / nan           | NAO_EXERCITADO  | False         | ...
EXIT_PROBE=0
```

O motivo **nomeia** `` `arestas_inventadas` MALFORMADA ('2') `` e `prova_runtime=False`. **Nunca OK.**
Mecanismo: derivação em `rstv.py:521-530` (`_contagem_observada`), uso novo em `rstv.py:780-788`.
O critério **é executado** (não é código morto): `CAPACIDADES` em `rstv.py:152`, mapa
`("RSTV-25b-dependencia", _cap_dependencia)` em `rstv.py:948`, laço do `avaliar` em `rstv.py:963`.

**Contra-prova de que o defeito existia** (mesma sonda contra os bytes `orig` = bloco L2 revertido),
tabela "antes": `str "2" → OK`, `"" → OK`, `[] → OK`, `{} → OK`, `-1 → OK`, `"NaN" → OK`, `nan → OK`,
`-inf → OK`; e `int 2 → REPROVADO`. É **exatamente** a medição do achado L2.

### Item 2 — canônico legítimo preservado — **OK**

Sonda própria no repo (colunas relevantes):

```
int 0          | OK       | True    | leitura runtime completa com identidade suficiente
float 0.0      | OK       | True    | leitura runtime completa com identidade suficiente
bool True      | OK       | True    | leitura runtime completa com identidade suficiente
bool False     | OK       | True    | leitura runtime completa com identidade suficiente
None explicito | OK       | True    | leitura runtime completa com identidade suficiente
chave AUSENTE  | OK       | True    | leitura runtime completa com identidade suficiente
int 1 / 2      | REPROVADO| False   | DEFEITO: aresta de dependencia INVENTADA (sem Dependency real)
float 2.0      | REPROVADO| False   | DEFEITO: aresta de dependencia INVENTADA (sem Dependency real)
```

`int/float >= 0` fecha OK; `> 0` (finito) REPROVA com o **motivo histórico** preservado
(`rstv.py:788`); `bool`, `None` e chave ausente seguem OK. **Contra-prova por brute-force** (minha,
`brute.py`, sha256 `80404d6f…`), carregando `orig` × `atual` no mesmo processo:

```
$ python -B %SCRATCH%/l2rev/brute.py %SCRATCH%/l2rev/orig/.../rstv.py C:/dev/stolen-realm/.../rstv.py
casos testados: 2037
transicoes totais: 1028
  OK               -> NAO_EXERCITADO   : 1027  amostra=[-1000, -999, -998, ...]
  REPROVADO        -> NAO_EXERCITADO   : 1  amostra=[inf]
REPROVADO->OK (ENFRAQUECIMENTO GRAVE): 0 []
```

- **Zero** transições `REPROVADO → OK` — a trava **não** foi enfraquecida.
- 1027 transições `OK → NAO_EXERCITADO` = **endurecimento** (o TIPO passou a ser exigido).
- **1** transição para fora de `REPROVADO`: `+inf` → `NAO_EXERCITADO` (nunca OK). Há um caso a mais que
  o parecer anterior contava — ver **O1** (§5).

### Item 3 — regressão nova com string-de-número e bordas — **OK**

`test_rstv.py::_l2_arestas_inventadas` em `test_rstv.py:394`, tabela de casos em `test_rstv.py:420-437`,
contrato de leitura malformada em `test_rstv.py:460-469`, controle "chave ausente = OK" em
`test_rstv.py:471-475`, e a função **é chamada** por `corpo()` em `test_rstv.py:656`.

Casos presentes (leitura literal do fonte): `L2-string-numero "2"`, `L2-string-vazia ""`,
`L2-string-nan "NaN"`, `L2-lista []`, `L2-dict {}`, `L2-negativo -1` → `NAO_EXERCITADO` com
"MALFORMADA"; `L2-int-um/dois`, `L2-float-dois` → `REPROVADO` com "INVENTADA"; `L2-int-zero`,
`L2-float-zero`, `L2-bool-true`, `L2-none-explicito`, chave ausente → `OK`.

**Não são casos vazios:** comparando as duas tabelas (antes × depois), cada forma malformada
**flipa de OK para não-OK**, então cada uma realmente pega o defeito. As bordas "float" (`0.0` OK,
`2.0` REPROVADO) e "None explícito" (OK) estão pinadas — ver **O2** para a semântica de `None`.

### Item 4 — CONTRA-PROVA em cópia fora do repo — **OK**

Bancada em `%LOCALAPPDATA%/hermes/cache/scratch/l2rev/` (fora do repo): árvore `verde` (bytes atuais,
`rstv.py` sha `e1ad69fc…` = repo) e árvore `vermelho` (bloco L2 revertido para a derivação antiga,
`rstv.py` sha `15f4da6e…`). `__pycache__` removido de ambas.

```
$ diff -u verde/.../rstv.py vermelho/.../rstv.py
@@ -777,15 +777,8 @@
-        if arestas is not None and not isinstance(arestas, bool):
-            contagem = _contagem_observada(arestas)
-            ... (bloco novo L2) ...
+        if isinstance(arestas, (int, float)) and not isinstance(arestas, bool) and arestas > 0:
+            defeitos.append("aresta de dependencia INVENTADA (sem Dependency real)")
DIFF_EXIT=1

$ cd verde && python -B tools/automacao/cenarios/test_rstv.py
RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK, controles reprovam, runtime identifica
EXIT_VERDE=0

$ cd vermelho && python -B tools/automacao/cenarios/test_rstv.py
RESULTADO|REPROVOU|cic3-rstv|L2-string-numero (valor='2'): esperado NAO_EXERCITADO, obtido OK (motivo='leitura runtime completa com identidade suficiente'): esperado 'NAO_EXERCITADO', obtido 'OK'
EXIT_VERMELHO=1
```

O defeito plantado reproduz **exatamente** o achado L2 (`"2"` fechando `OK`), o runner fica **VERMELHO
exit 1** nomeando `L2-string-numero`, e **sem** o defeito fica **VERDE exit 0**. Nada disso dentro do repo.

**Reconfirmação da bancada do PRÓPRIO autor** (não bastasse a minha): a cópia
`%SCRATCH%/l2-entrega/vermelho/.../rstv.py` ainda existe com sha256 `94f8135c…` (o valor que o
`CIC-3-L2-entrega.md` §3.3 cita) e **reproduz** o mesmo `RESULTADO|REPROVOU|…L2-string-numero…` com
`EXIT_AUTOR_VERMELHO=1`; a `verde` (sha `e1ad69fc…`) dá `EXIT_AUTOR_VERDE=0`.

### Item 5 — não-regressão — **OK**

Suíte do módulo de cenários e os consumidores, **no repo** (`run_suites.py`, sha256 `6e44e8d9…`):

```
$ python -B tools/automacao/cenarios/test_rstv.py
RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK, controles reprovam, runtime identifica
EXIT=0

$ python -B tools/automacao/cenarios/test_tooltips_shrines.py
TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0
EXIT=0

(todos os consumidores no repo, EXIT=0)
tools/automacao/aceite/test_relatorio_aceite.py    EXIT=0 | TUDO OK
tools/automacao/aut5/test_aut5.py                  EXIT=0 | RESULTADO|PASSOU|aut5-rstv|16 casos …
tools/automacao/aut5/test_snapshot_modal.py        EXIT=0
tools/automacao/aut6/test_cobertura_aut6.py        EXIT=0 | TOTAL|rodaram=24 reprovaram=0
tools/automacao/aut6/test_regressoes_cor_aut6.py   EXIT=0 | OK
tools/automacao/ciclo/test_ciclo.py                EXIT=0 | OK
tools/automacao/ciclo/test_decisao.py              EXIT=0 | RESULTADO|PASSOU|CLI criterios ausente exit 2 …
tools/automacao/estilo/test_estilo_atributos.py    EXIT=0 | TUDO OK
```

**"Resultado equivalente ao de antes" provado.** Rodando a MESMA suíte contra as duas cópias
(`verde` = bytes atuais × `orig` = L2 revertido), o resultado é **byte a byte idêntico** nos 9
consumidores:

```
$ diff suites-verde.txt suites-orig.txt
IDENTICOS (nenhuma diferenca de comportamento nos consumidores)
```

(Os três `EXIT=1` que aparecem nas *cópias* — aut5, aut6, shrines — são **ambientais** às cópias: elas
não têm `BetterStats/` nem outras pastas da raiz do repo. Aparecem **iguais dos dois lados**, logo são
atribuíveis ao ambiente da cópia, **não** à mudança L2. No **repo** os 9 estão verdes.)

### Item 6 — Relatório no disco (arquivo:linha, comandos, exit code, sha256) — **OK**

`docs/automacao/CIC-3-L2-entrega.md` existe (16801 bytes, 16:40, sha256 `f8ccfbe8…`) e contém os quatro
elementos exigidos. **Conferi cada citação factual:**

| citação do relatório | conferência minha |
|---|---|
| `rstv.py` sha256 `e1ad69fc…`, `test_rstv.py` `460ef535…` | **casam** (§1) |
| `test_tooltips_shrines.py` `8fcba1c3…`, `tooltips_shrines.py` `65c0f3b2…` | **casam** |
| `rstv-identidade.json` `5cec628c…`, `arcabouco.py` `08b4dd51…` | **casam** |
| `CIC-3-L2R-revisao.md` `a05a6a30…`, `CIC-3R2-revisao.md` `a5013f42…` | **casam** |
| probe do autor `probe_tabela.py` sha `6483ab41…` | **casa** |
| helper `rstv.py:521-530`; F2 `679`; L2 `781` (bloco 780-788); F3 `803-814` | **casam** |
| `test_rstv.py`: `_l2_…` em `394`; contrato `460-469`; ausente `475`; chamada `656` | **casam** |
| §3.1/§3.3 saídas literais (verde/vermelho) e exit codes 0/1 | **reproduzidas** por mim (§3.4) |
| §4 tabela de formas com `EXIT_PROBE=0` | **reproduzida** pela minha sonda |

Única imprecisão: §2.4 diz "docstring …, item 12 (L2) | `test_rstv.py:46-47`" — o item 12 ocupa
`46-50`; e "tabela de casos `415-458`" — a tupla está em `420-437` (laço em `438-458`). Cosmético, não
afeta a substância (**O4**).

---

## 4. O QUE TENTEI REFUTAR (e o resultado)

| alvo de refutação | tentativa | resultado |
|---|---|---|
| **Circularidade** (o campo volta a governar o veredito) | ler se o predicado lê schema/tipo DENTRO do artefato | **não refuto**: `_contagem_observada` é semântica **hardcoded** (número finito ≥ 0, `rstv.py:521-530`), igual ao padrão F2/F3 |
| **Código morto** | grepar o mapa de capacidades | **não refuto**: `RSTV-25b-dependencia` está em `_CAPS` (`rstv.py:948`) e é iterado (`963`) |
| **Enfraquecimento da trava** | brute-force 2037 valores, 2 versões no mesmo processo | **não refuto**: `REPROVADO→OK = 0` |
| **`+inf` sair de REPROVADO** | comparar antes × depois | **confirmo como mudança declarada** (→ `NAO_EXERCITADO`, nunca OK) — **O1** |
| **Inteiro gigante (`10**400`) — OverflowError** | injetar ints enormes | **ACHO transição nova**: `REPROVADO → INDETERMINADO` (o `float(v)` estoura e o `avaliar` captura a exceção, `rstv.py:966-973`). **Não vai a OK.** O parecer anterior ("exatamente uma transição") fica **incompleto** — **O1** |
| **`None` explícito fecha OK** | comparar L2 com F2 no caso presente-porem-nulo | **confirmo assimetria** (F2=`null`→MALFORMADA; L2=`null`→OK) — **O2** |
| **`bool` é contagem** | testar `True`/`False` | `True`/`False` fecham OK — **é o que o cartão exige** (critério 2: "o bool True legítimo"); registro a nota semântica — **O3** |
| **Teste viciado** (nunca reprova) | plantar defeito e rodar | **não refuto**: vermelho exit 1 com a linha exata do achado (§3.4) |
| **Teste pulado parecendo verde** | conferir exit codes 0/1/2 | **não refuto**: `Falhou`→1, `NaoRodou`→2 (`arcabouco.py:224-247`); nenhum pulado |

---

## 5. OBSERVAÇÕES / LACUNAS DECLARADAS (não são OK, não bloqueiam o cartão)

- **O1 — `+inf` e inteiros gigantes saem de `REPROVADO` → `INDETERMINADO`/`NAO_EXERCITADO`.** Prova:
  `10**400`, `-(10**400)`, `2**1024` → `INDETERMINADO`
  (`"observacao malformada derrubou a capacidade (id canonico preservado)"`), porque `float(v)` levanta
  `OverflowError` e o `avaliar` captura (`rstv.py:966-973`); `+inf` → `NAO_EXERCITADO` (não finito).
  **Nenhum vira OK** ⇒ **não** é enfraquecimento para verde. Mas o parecer `CIC-3-L2R` (§2 item 5)
  afirma "exatamente uma transição para fora de REPROVADO (`+inf`)" — **isso é incompleto**: há também
  os inteiros acima de `~1.8e308`. A **correção** não fez essa afirmação; a **revisão anterior** sim.
- **O2 — Assimetria F2 × L2 no valor presente-porem-nulo.** Sonda `probe_assimetria.py` (sha `a9a041a3…`):

  ```
  F2 janelas_duplicadas=None   -> NAO_EXERCITADO | ... janelas_duplicadas MALFORMADA ...
  L2 arestas_inventadas=None   -> OK             | leitura runtime completa com identidade suficiente
  ```

  `F2` checa `if "…" in o` e trata `null` como MALFORMADA; `L2` usa `o.get(...)` e colapsa
  **presente-nulo × ausente** (ambos OK). É **consistente** com o critério 2 do cartão ("a chave AUSENTE
  … segue OK") e **não abre buraco novo** (`None` já era OK antes), mas deixa de fora a distinção que a
  F2 faz. **Decisão do dono:** manter (colapsar nulo↔ausente) ou exigir, como na F2, que `null` presente
  seja leitura malformada. Não alterei nada (revisor mede, não conserta).
- **O3 — `bool True`/`False` fecham OK.** É o comportamento que o cartão manda preservar (critério 2).
  Nota semântica: um `bool` **não** é contagem e, a rigor, `True` significaria "há aresta inventada" —
  mas o cartão o trata como canônico. Sem ação; registro para transparência.
- **O4 — Imprecisões cosméticas de `arquivo:linha`** no `CIC-3-L2-entrega.md` §2.4 (`46-47` vs `46-50`;
  `415-458` vs `420-458`). Não muda a substância.
- **O5 — Proveniência do "antes": INDETERMINADA.** `tools/automacao/` é untracked ⇒ o `orig` que usei é
  uma **reconstrução** (reversão do único hunk de código), não atestada por git. Corroborada pela cópia
  congelada do autor (`l2/rstv-ORIGINAL.py`, sha `2fad23a3…`) e pela medição da régua. **Não** é defeito
  do fix.
- **O6 — Nada de runtime/jogo.** Toda a evidência é de fixture rotulada; verificação humana em jogo e
  publicação seguem portões separados do dono.

---

## 6. PENDÊNCIAS (para o cartão fechar)

1. **Commit** (dono): `tools/automacao/` e `docs/automacao/` seguem **untracked** — o estado "no repo"
   não é durável a um `clean`. Dívida do dono, não do fix.
2. **Decisão do dono sobre O2** (`null` presente em `arestas_inventadas`): colapsar com ausente (atual)
   ou exigir leitura malformada como na F2.
3. **Retificar (opcional) O1** no parecer `CIC-3-L2R`: a contagem de transições para fora de `REPROVADO`
   não é "exatamente uma".
4. **Verificação em jogo / publicação** — portões separados, fora do escopo desta revisão.

---

## 7. ÍNDICE DAS BANCADAS (fora do repo)

```
%LOCALAPPDATA%/hermes/cache/scratch/l2rev/
  probe_forms.py         sonda própria da tabela de formas   (sha  be63911b…)
  probe_assimetria.py    sonda F2×L2 do presente-nulo        (sha  a9a041a3…)
  brute.py               antes×depois, 2037 casos            (sha  80404d6f…)
  planta.py              reversão do hunk L2 na cópia        (sha  cdca9483…)
  run_suites.py          suites dos consumidores             (sha  6e44e8d9…)
  suites-verde.txt == suites-orig.txt  (idênticos)           (sha  a0e56287…)
  verde/…/rstv.py        bytes atuais                        (sha  e1ad69fc…)
  vermelho/…/rstv.py     L2 revertido → runner VERMELHO 1    (sha  15f4da6e…)
  orig/…/rstv.py         idem (para o brute-force)           (sha  15f4da6e…)
%LOCALAPPDATA%/hermes/cache/scratch/l2-entrega/   (bancada do AUTOR, reconferida)
  verde/…/rstv.py        (sha e1ad69fc…) → exit 0
  vermelho/…/rstv.py     (sha 94f8135c…) → exit 1  ("L2-string-numero")
```

**Conferência final:** `rstv.py`/`test_rstv.py` seguem com `e1ad69fc…`/`460ef535…` após todas as
execuções; `git status` inalterado; o único caminho escrito por mim no repo é **este** relatório.
