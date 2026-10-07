# CIC-3-L2 — entrega: `arestas_inventadas` deriva o TIPO esperado (contagem observada)

Rodada: **CIC-3-L2**, cartão `t_f7cc7cbb` (status `review`). Escopo: `tools/automacao/cenarios/rstv.py`
+ `test_rstv.py`. Este documento **é o critério 6 do cartão** (“relatório de execução no disco”),
que o parecer independente `docs/automacao/CIC-3-L2R-revisao.md` (§ item 8) deu como **não cumprido**.

> **Quem sou eu nesta rodada.** Sou a tarefa de entrega do relatório faltante — **documentador**, não autor
> da correção. A correção de código é a do cartão; os comandos, a tabela de formas e a contra-prova abaixo
> foram **reexecutados/medidos por MIM** contra os bytes atuais. **Não** instalei mod, **não** abri o jogo,
> **não** builda, **não** publiquei, **não** commitei, **não** criei nem mutei tarefa no Kanban. O **único**
> arquivo escrito no repo é **este**; as bancadas rodaram em cópia **fora** do repo
> (`%LOCALAPPDATA%/hermes/cache/scratch/l2-entrega/`).

---

## 1. Cartão, achado de origem e o que foi feito

- **Cartão:** `t_f7cc7cbb` (CIC-3-L2), frente “cenários automáticos RSTV para o ciclo”.
- **Achado de origem:** parecer independente `docs/automacao/CIC-3R2-revisao.md` **§7, item L2**
  (linhas ~344-350) — lacuna **L2**: no campo `arestas_inventadas`, a forma **malformada** (`"2"` string)
  fechava o critério `OK`, enquanto o número canônico `2` **reprovava** (classe F2/F3 do projeto: “o campo
  governa o próprio veredito”).
- **O que foi feito:** em `tools/automacao/cenarios/rstv.py`, `_cap_dependencia` deixa de ler
  `arestas_inventadas` como “qualquer coisa que compare igual” e passa a exigir a **contagem observada**
  (número finito `>= 0`, booleano excluído) via o helper já existente `_contagem_observada`; valor presente
  e malformado vira **motivo declarado** (`NAO_EXERCITADO`, nunca OK). Regressão nova em
  `test_rstv.py::_l2_arestas_inventadas`.
- **Este relatório** fecha o critério 6 do cartão (entrega documental que faltava).

---

## 2. Diff do que mudou (antes × depois)

### 2.1 Proveniência do “antes” — **INDETERMINADA** (declarada)

`tools/automacao/` é **untracked** (`git status --porcelain` → `?? tools/automacao/`), então **não há
commit nem `git diff`** que ateste os bytes anteriores. A cópia congelada do “antes” usada aqui é
`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/l2/rstv-ORIGINAL.py`
(sha256 `2fad23a3…`), **rotulada como provenance INDETERMINADA** por não ser atestável por git.

Corroboração (medição minha, apenas rastreio — **não** substitui atestação git): varri o disco e encontrei
**27 cópias independentes** de `rstv.py` com **exatamente** o sha do “antes” (`2fad23a3…`), criadas por
**outras tarefas** (não esta), com mtimes **anteriores** ao fix (16:24). Amostra com mtime:

```
13:48:42  .../kanban/workspaces/t_fa0e97a9/copia/tools/automacao/cenarios/rstv.py      (2fad23a3…)
13:48:42  .../cache/scratch/cor7f2rev/sb/tools/automacao/cenarios/rstv.py              (2fad23a3…)
15:38:31  .../cache/scratch/cor-aut4f2r/base_orig/tools/automacao/cenarios/rstv.py     (2fad23a3…)
16:05:56  .../cache/scratch/cp_f4_sem_defeito/tools/automacao/cenarios/rstv.py         (2fad23a3…)
16:14:43  .../cache/scratch/f4r_rev/sem/tools/automacao/cenarios/rstv.py               (2fad23a3…)
```

Observação de peso: o mtime `13:48:42` é **idêntico** ao mtime que o parecer da régua registrou para o
`rstv.py` do repo em 06/10 13:48 (CIC-3R2 §1.1), e o próprio parecer mediu o sha `2fad23a3…` como o estado
do produto naquela altura. Ou seja: o “antes” está corroborado por muitos snapshots independentes e pela
medição da régua — mas **segue sem atestação git**.

### 2.2 `diff -u` (2 hunks) — `DIFF_EXIT=1`

```
--- scratch/l2/rstv-ORIGINAL.py      2026-10-06 16:23:48  (2fad23a3…)
+++ tools/automacao/cenarios/rstv.py  2026-10-06 16:24:00  (e1ad69fc…)
@@ -74,6 +74,11 @@   (HUNK 1 — só cabeçalho/docstring)
 * **F7** sessoes: observacoes de SESSOES diferentes na mesma capacidade nao sao
   prova de um unico ciclo (INDETERMINADO) — e nenhuma sessao e copiada para o
   criterio como se fosse a do conjunto inteiro.
+* **L2** `RSTV-25b-dependencia`: `arestas_inventadas` deriva o TIPO esperado
+  (contagem: numero finito >= 0) em vez de aceitar qualquer coisa que compare
+  igual. Forma presente e MALFORMADA (texto '2', '', lista, dict, negativo,
+  'NaN') e leitura malformada declarada — nunca OK; o inteiro/float valido, o
+  booleano e a chave ausente seguem o comportamento anterior.

@@ -764,8 +769,23 @@   (HUNK 2 — o código)
             continue
         contrib.append(o)
         dados = True
-        if isinstance(arestas, (int, float)) and not isinstance(arestas, bool) and arestas > 0:
-            defeitos.append("aresta de dependencia INVENTADA (sem Dependency real)")
+        # L2 (parecer CIC-3R2, mesma classe F2/F3): `arestas_inventadas` e uma
+        # CONTAGEM — o TIPO esperado e o numero finito >= 0 (int/float), nao
+        # "qualquer coisa que compare igual". Antes, so o numero nao-bool > 0
+        # virava defeito; uma forma MALFORMADA (texto '2', '', lista, dict,
+        # negativo, 'NaN') NAO era lida como leitura malformada e fechava OK.
+        # Agora a forma presente e malformada vira motivo declarado — nunca OK.
+        # O booleano segue o comportamento historico (nao e contagem): a guarda
+        # `not isinstance(arestas, bool)` preservada.
+        if arestas is not None and not isinstance(arestas, bool):
+            contagem = _contagem_observada(arestas)
+            if contagem is None:
+                motivos.append("`arestas_inventadas` MALFORMADA (%r): exigida "
+                               "contagem observada valida (numero finito >= 0); forma "
+                               "textual/nao numerica/negativa nao prova ausencia de "
+                               "aresta inventada" % (arestas,))
+            elif contagem > 0:
+                defeitos.append("aresta de dependencia INVENTADA (sem Dependency real)")
         if linhas is None:
             motivos.append("linhas por tier AUSENTES")
             indeterminado = True
```

Só **2 hunks**; a mudança de comportamento é atribuível **só** ao hunk 2 (o hunk 1 é comentário). Antes x
depois do núcleo (o que decide o veredito):

```python
# ANTES (rótulo do "antes" INDETERMINADO) — só o número não-bool > 0 reprovava:
if isinstance(arestas, (int, float)) and not isinstance(arestas, bool) and arestas > 0:
    defeitos.append("aresta de dependencia INVENTADA (sem Dependency real)")

# DEPOIS (bytes atuais) — a forma presente deriva o TIPO (contagem observada):
if arestas is not None and not isinstance(arestas, bool):
    contagem = _contagem_observada(arestas)
    if contagem is None:
        motivos.append("`arestas_inventadas` MALFORMADA (%r): exigida contagem observada "
                       "valida (numero finito >= 0); forma textual/nao numerica/negativa "
                       "nao prova ausencia de aresta inventada" % (arestas,))
    elif contagem > 0:
        defeitos.append("aresta de dependencia INVENTADA (sem Dependency real)")
```

### 2.3 Arquivo:linha do código novo

| item | arquivo:linha |
|---|---|
| helper `_contagem_observada` (definição; semântica fixa: finito `>= 0`, bool fora) | `rstv.py:521-530` |
| uso já existente em **F2** (`janelas_duplicadas`) | `rstv.py:679` |
| uso novo em **L2** (`arestas_inventadas`) | `rstv.py:781` (bloco `if/elif` em `rstv.py:780-788`) |
| uso já existente em **F3** (confronto por tier) | `rstv.py:803-814` |

O helper é **semântica fixa do campo** (hardcoded), não leitura do próprio artefato — não reintroduz a
circularidade F2/F3.

### 2.4 Arquivo:linha dos casos novos em `test_rstv.py`

| item | arquivo:linha |
|---|---|
| docstring do módulo, item 12 (L2) | `test_rstv.py:46-47` |
| função `_l2_arestas_inventadas(R, ident)` | `test_rstv.py:394` |
| tabela de casos (positivos/malformados) | `test_rstv.py:415-458` |
| contrato “forma malformada = leitura malformada” (`tipo_pendencia=tecnica`, `lacuna_probe`) | `test_rstv.py:460-469` |
| controle “chave AUSENTE = OK” | `test_rstv.py:475` |
| chamada dentro de `corpo()` (a suíte a executa) | `test_rstv.py:656` |

---

## 3. Comandos exatos, saída literal e exit code (medidos por mim)

Todos com `PYTHONDONTWRITEBYTECODE=1` e `python -B` (nenhuma escrita de `__pycache__` no repo).

### 3.1 Suíte do módulo (esperado EXIT=0)

```
$ python -B tools/automacao/cenarios/test_rstv.py
RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK, controles reprovam, runtime identifica
EXIT=0
```

### 3.2 Suíte vizinha (esperado EXIT=0)

```
$ python -B tools/automacao/cenarios/test_tooltips_shrines.py
… 28 linhas RESULTADO|PASSOU|… 
TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0
EXIT=0
```

### 3.3 CONTRA-PROVA — cópia FORA do repo (`…/cache/scratch/l2-entrega/`)

Bancada espelhada do `tools/` do repo. **VERDE** = bytes atuais (sha `e1ad69fc…`, == repo). **VERMELHO** =
mesma árvore com o **defeito plantado** = reversão do hunk 2 para a derivação antiga de tipo
(`isinstance(arestas,(int,float)) … > 0`); sha da bancada vermelha = `94f8135c…`.

```
############ VERDE (sem defeito) ############
$ cd …/l2-entrega/verde && python -B tools/automacao/cenarios/test_rstv.py
RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK, controles reprovam, runtime identifica
EXIT_VERDE=0

############ VERMELHO (defeito plantado) ############
$ cd …/l2-entrega/vermelho && python -B tools/automacao/cenarios/test_rstv.py
RESULTADO|REPROVOU|cic3-rstv|L2-string-numero (valor='2'): esperado NAO_EXERCITADO, obtido OK (motivo='leitura runtime completa com identidade suficiente'): esperado 'NAO_EXERCITADO', obtido 'OK'
EXIT_VERMELHO=1
```

O defeito plantado reproduz **exatamente** o achado L2 (`arestas_inventadas="2"` fechando `OK`) e o runner
fica **VERMELHO exit 1** nomeando o caso `L2-string-numero`; **sem** o defeito, **VERDE exit 0**. Os três
exit codes (0/1) são distintos do código de “pulado” — nenhum teste foi pulado em nenhuma execução.

---

## 4. Tabela de formas de `arestas_inventadas` × estado (medida por mim)

Sonda **própria** (`scratch/l2-entrega/probe_tabela.py`, sha `6483ab41…`), importando o `rstv.py` **do repo**
por caminho e chamando `avaliar` direto na base completa (`_obs_completa`), extraindo o critério
`RSTV-25b-dependencia`:

| forma do campo | estado | `prova_runtime` |
|---|---|---|
| inteiro `0` | **OK** | True |
| inteiro `2` | **REPROVADO** | False |
| float `0.0` | **OK** | True |
| float `2.0` | **REPROVADO** | False |
| bool `True` | **OK** | True |
| chave **AUSENTE** | **OK** | True |
| `None` explícito | **OK** | True |
| string `"2"` | **NAO_EXERCITADO** | False |
| string vazia `""` | **NAO_EXERCITADO** | False |
| lista `[]` | **NAO_EXERCITADO** | False |
| dict `{}` | **NAO_EXERCITADO** | False |
| negativo `-1` | **NAO_EXERCITADO** | False |
| `inf` | **NAO_EXERCITADO** | False |
| `nan` | **NAO_EXERCITADO** | False |

Saída literal da sonda:

```
forma            | estado          | prova_runtime | motivo(recorte)
int 0            | OK              | True          | leitura runtime completa com identidade suficiente
int 2            | REPROVADO       | False         | DEFEITO: aresta de dependencia INVENTADA (sem Dependency real)
float 0.0        | OK              | True          | leitura runtime completa com identidade suficiente
float 2.0        | REPROVADO       | False         | DEFEITO: aresta de dependencia INVENTADA (sem Dependency real)
bool True        | OK              | True          | leitura runtime completa com identidade suficiente
chave AUSENTE    | OK              | True          | leitura runtime completa com identidade suficiente
None explicito   | OK              | True          | leitura runtime completa com identidade suficiente
string "2"       | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventadas` MALFORMADA
string vazia ""  | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventadas` MALFORMADA
lista []         | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventadas` MALFORMADA
dict {}          | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventadas` MALFORMADA
negativo -1      | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventadas` MALFORMADA
inf              | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventadas` MALFORMADA
nan              | NAO_EXERCITADO  | False         | campo AUSENTE/incompleto nao vira OK — `arestas_inventadas` MALFORMADA
EXIT_PROBE=0
```

**Leitura:** nenhuma forma malformada fecha `OK`; o canônico legítimo (`0`, `0.0`, bool, `None`, chave
ausente) preserva o comportamento anterior; `> 0` finito segue **REPROVADO** com o motivo histórico
`DEFEITO: … INVENTADA …`. Só formas **não-OK** carregam `prova_runtime=False`.

---

## 5. sha256 dos arquivos tocados/lidos e referência ao parecer

```
e1ad69fc6128b7403363dd4efeefaf9614d1be0437fe71f90079ebb5547bf60f  tools/automacao/cenarios/rstv.py            (produto — NÃO tocado por mim nesta rodada)
460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262  tools/automacao/cenarios/test_rstv.py       (teste — NÃO tocado por mim)
8fcba1c3ba8af9ff8bcf4b3db115a333e6799d364ea3fe8102cfbf971b9df885  tools/automacao/cenarios/test_tooltips_shrines.py
65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199  tools/automacao/cenarios/tooltips_shrines.py
5cec628c011e5bc5f249fc649401eed20ee65eccaf40aafa33389d7ef2792f86  tools/automacao/cenarios/rstv-identidade.json
08b4dd51c1d2bd851cf0d5d2b2f038dbe3f1094ab4c625ed63a7a4dc97c20afb  tools/testes/arcabouco.py
a05a6a30c9274af1a0f2ac33fab59193c557420e2cfe4e326cf4db0e7d221d1b  docs/automacao/CIC-3-L2R-revisao.md         (parecer que aponta o item 8)
a5013f42484b6b518f8b884b6ea7d7284e8376f98d0a24683ca081a0a2c8b8cc  docs/automacao/CIC-3R2-revisao.md           (régua do achado L2, §7)
```

Referência ao parecer de revisão **`docs/automacao/CIC-3-L2R-revisao.md`**
(sha256 `a05a6a30c9274af1a0f2ac33fab59193c557420e2cfe4e326cf4db0e7d221d1b`): veredito global
**APROVADO COM RESSALVAS**, com os itens 1-7 = OK e a **ressalva do item 8** (critério 6 do cartão —
relatório no disco — não cumprido). **Este relatório fecha essa ressalva.**

---

## 6. Lacunas declaradas (nunca contam como OK)

- **Runtime/jogo:** nada de runtime nesta rodada. Sem jogo, save, probe, build, instalação, deploy ou
  publicação; os dados do comportamento são fixtures sintéticas rotuladas (`procedencia=runtime` injetada).
  Nada aqui atesta o mod em jogo.
- **Proveniência do “antes”: INDETERMINADA.** `tools/automacao/` é **untracked**, então os bytes anteriores
  (`rstv-ORIGINAL.py`, sha `2fad23a3…`) **não** têm atestação git. Corroborados (não atestados) por 27 cópias
  independentes de outras tarefas e pela medição da régua.
- **Correção NÃO commitada.** `tools/automacao/` segue `?? tools/automacao/`; nada foi para o stage
  (`git diff --cached --name-only` → vazio). Nenhum `git add` de diretório, nenhum `git add -A`. O estado
  “no repo” não é durável a um `clean` — dívida do dono, não do fix.
- **Achado não reverificado em campo.** A contra-prova é sintética (bancada fora do repo); a verificação
  humana em jogo e a publicação seguem portões separados do dono.
- **Este documento é um relatório, não uma correção.** Se em qualquer ponto do tempo os bytes de
  `rstv.py`/`test_rstv.py` mudarem, os sha256 do §5 invalidam esta âncora.

---

## 7. Índice da bancada (fora do repo)

```
%LOCALAPPDATA%/hermes/cache/scratch/l2-entrega/
  probe_tabela.py                 sonda própria da tabela de formas (sha 6483ab41…)
  verde/tools/…/rstv.py           bytes atuais (sha e1ad69fc…, == repo)
  vermelho/tools/…/rstv.py        defeito plantado (sha 94f8135c…) → runner VERMELHO exit 1
%LOCALAPPDATA%/hermes/cache/scratch/l2/
  rstv-ORIGINAL.py                cópia congelada do “antes” (sha 2fad23a3…, proveniência INDETERMINADA)
  rstv-FIXADO.py                  cópia do “depois” do autor (sha e1ad69fc…, == repo)
```

**Conferência final:** `rstv.py` e `test_rstv.py` seguem com os mesmos sha256 do §5 após todas as
execuções desta rodada (nenhuma deriva). O único caminho escrito no repo por esta rodada é
`docs/automacao/CIC-3-L2-entrega.md`.
