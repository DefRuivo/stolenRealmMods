# CIC-3-L2R — revisão independente da correção do campo `arestas_inventadas` (`t_f7cc7cbb`)

> **Quem sou eu nesta rodada.** Sou a tarefa de revisão (subagente revisor) — **não** o autor. Nada aqui
> publica, instala, deploya, abre o jogo, carrega save, builda, commita ou toca o produto. Escrevi
> **somente** este documento; as bancadas rodaram em cópia **fora** do repo
> (`%LOCALAPPDATA%/hermes/cache/scratch/rev_l2/`). Nenhum `git add`, nenhum commit, nenhuma mutação de Kanban.
>
> **Objeto:** o fechamento do achado residual **L2** do parecer `docs/automacao/CIC-3R2-revisao.md`
> (§7 L2 / linhas ~344-350): no campo `arestas_inventadas`, a forma **malformada** (`"2"` string) fechava
> critério `OK` enquanto o número canônico `2` REPROVAVA — classe F2/F3 do projeto ("o artefato/campo
> governa o próprio veredito"). O produto é `tools/automacao/cenarios/rstv.py` + `test_rstv.py`.
> **Método:** sonda **própria** (não a do autor), leitura do código × régua, tabela antes × depois com
> `rstv-ORIGINAL.py`, brute-force de 2039 valores e contra-prova em **cópia** fora do repo.
>
> **Veredito final: APROVADO COM RESSALVAS.** A correção fecha o L2 e **não** enfraquece a trava: nenhum
> caso sai de `REPROVADO` para `OK` (2039 entradas varridas; exatamente **uma** sai de `REPROVADO` — o
> `+inf`, e vai para `NAO_EXERCITADO`, nunca `OK`). **Ressalva (não OK):** o **critério 6 do cartão não foi
> cumprido** — não existe relatório de execução no disco (item 8 abaixo).

---

## 1. Estado lido (sha256 medido por MIM, no disco)

| caminho | sha256 (medido nesta revisão) |
|---|---|
| `tools/automacao/cenarios/rstv.py` | `e1ad69fc6128b7403363dd4efeefaf9614d1be0437fe71f90079ebb5547bf60f` |
| `tools/automacao/cenarios/test_rstv.py` | `460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262` |
| `tools/automacao/cenarios/test_tooltips_shrines.py` | `8fcba1c3ba8af9ff8bcf4b3db115a333e6799d364ea3fe8102cfbf971b9df885` |
| `tools/automacao/cenarios/tooltips_shrines.py` | `65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199` |
| `tools/automacao/runtime/coletor.py` (só lido) | `dee03a8fd16d95730ede993a14747406a37ba44f8a7ea97a6a666995fb7ef3e5` |
| `tools/testes/arcabouco.py` (harness) | `08b4dd51c1d2bd851cf0d5d2b2f038dbe3f1094ab4c625ed63a7a4dc97c20afb` |
| `docs/automacao/CIC-3R2-revisao.md` (a régua) | `a5013f42484b6b518f8b884b6ea7d7284e8376f98d0a24683ca081a0a2c8b8cc` |

mtime do produto: `rstv.py` e `test_rstv.py` = **2026-10-06 16:24**. `tools/automacao/` é **untracked**
(`git status`: `?? tools/automacao/`), então `git diff` não o alcança — a lente "bytes antigos ∕ bytes atuais"
usa a cópia congelada `rstv-ORIGINAL.py` (§2 item 5).

### 1.1 Confirmação de que os bytes atuais == cópia "FIXADO" do autor (não é prova, só rastreio)

```
$ sha256sum tools/automacao/cenarios/rstv.py "…/scratch/l2/rstv-FIXADO.py"
e1ad69fc6128b7403363dd4efeefaf9614d1be0437fe71f90079ebb5547bf60f *tools/automacao/cenarios/rstv.py
e1ad69fc6128b7403363dd4efeefaf9614d1be0437fe71f90079ebb5547bf60f *…/scratch/l2/rstv-FIXADO.py
```

O `rstv.py` do repo e o `rstv-FIXADO.py` do autor têm o **mesmo sha256** — o que está no disco é o que o
autor congelou. (A cópia do autor **não** vale como prova; foi usada apenas para casar bytes.)

---

## 2. Verificação POR ITEM

### Item 1 — `arestas_inventadas="2"` (string) NÃO fecha OK — **OK**

Prova **própria** (sonda `rev_l2/probe_l2_rev.py`, que monta a própria observação base e chama
`avaliar` direto no `rstv.py` do repo; NÃO é a tabela do autor):

```
$ python probe_l2_rev.py tools/automacao/cenarios/rstv.py tools/automacao/cenarios   # (executado em cópia-fora, apontando para o repo)
{"caso": "str-2", "valor": "str:'2'", "estado": "NAO_EXERCITADO", "defeito": false,
 "motivo": "campo AUSENTE/incompleto nao vira OK — `arestas_inventadas` MALFORMADA ('2'): exigida contagem observada valida (numero finito >= 0); forma textual/nao numerica/negativa nao prova ausencia de aresta inventada"}
```

Estado = `NAO_EXERCITADO`, motivo **nomeia** "MALFORMADA ('2')", `defeito=false` (não é defeito plantado,
é leitura malformada declarada) e `prova_runtime` é `false`. **Nunca OK.** O mesmo vale para `"NaN"`,
`"Infinity"`, `"-1"`, `"abc"`, `""`, `"  "` (ver item 3).

Arquivo:linha do mecanismo: derivação em `rstv.py:521-530` (`_contagem_observada`); uso em
`rstv.py:780-788`.

### Item 2 — canônico legítimo preservado — **OK**

```
int-0      int:0     -> OK
float-0.0  float:0.0 -> OK
int-1      int:1     -> REPROVADO  (DEFEITO: … INVENTADA …)
int-2      int:2     -> REPROVADO  (DEFEITO: … INVENTADA …)
float-2.0  float:2.0 -> REPROVADO  (DEFEITO: … INVENTADA …)
bool-True  bool:True -> OK
bool-False bool:False-> OK
none       NoneType  -> OK
ausente    <AUSENTE> -> OK
```

`inteiro/float >= 0` (inclusive `0`, `0.0` e `-0.0`) fecha `OK`; `> 0` REPROVA com o motivo histórico
`"DEFEITO: aresta de dependencia INVENTADA (sem Dependency real)"` (mantido em `rstv.py:788`); `bool True/False`,
`None` explícito e chave ausente seguem `OK` — mesma linha de guarda `not isinstance(arestas, bool)`
(`rstv.py:780`) e guarda de contribuição `arestas is None` (`rstv.py:768`). Todos esses eram `OK` também
no `rstv-ORIGINAL.py` (§ item 5, zero mudança).

### Item 3 — bordas — **OK**

| valor | antes (`ORIGINAL`) | depois (repo) | fecha OK? |
|---|---|---|---|
| `""` (string vazia) | OK | NAO_EXERCITADO | não |
| `2.5` (float não inteiro) | REPROVADO | REPROVADO | não |
| `[]`, `[1,2]`, `{}`, `{"a":1}`, `()` | OK | NAO_EXERCITADO | **não** |
| `-1`, `-2.5` (negativos) | OK | NAO_EXERCITADO | não |
| `float('inf')` | REPROVADO | NAO_EXERCITADO | não |
| `float('-inf')` | OK | NAO_EXERCITADO | **não** |
| `float('nan')` | OK | NAO_EXERCITADO | **não** |

**Nenhuma** borda fecha `OK` indevidamente. Observação de mérito: `2.5` (float finito `> 0`) é tratado como
"contagem válida, porém > 0" ⇒ `REPROVADO`; não fecha OK, então não há vazamento — é escolha semântica
aceitável (um artefato só manda `2.5` se estiver inventando).

### Item 4 — CIRCULARIDADE — **OK** (não é circular)

O predicado é **semântica fixa do campo**, não leitura do próprio artefato:

```python
def _contagem_observada(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    f = float(v)
    return f if math.isfinite(f) and f >= 0 else None
```

"Contagem" = número finito `>= 0`, booleano fora — **hardcoded** (`rstv.py:521-530`). O código **não** lê
nenhum schema/tipo declarado dentro da observação para decidir o que é válido, e o `esperado` do critério é
texto humano-autoral (`rstv.py:837-838`), não dado do artefato. É exatamente o mesmo padrão já aceito em F2
(`rstv.py:679`) e F3 (`rstv.py:803-814`). **Não** há o defeito F2/F3 aqui.

### Item 5 — A TRAVA NÃO FOI ENFRAQUECIDA — **OK** (com 1 transição declarada)

Antes × depois no **mesmo caso base** (sonda própria; tabela completa de 29 casos em
`rev_l2/{original,fixado}.jsonl`). Brute-force de **2039** valores (inteiros `-1000..1000`, floats,
`±inf`, `NaN`, strings, `bool`, `None`, listas/dicts/tuplas/set/`object()`), carregando as **duas** versões
no mesmo processo:

```
casos testados: 2039
transicoes totais: 1025
-> de OK para nao-OK (fortalecimento/endurecimento): 1024
-> de REPROVADO para nao-REPROVADO: 1 [('inf', 'REPROVADO->NAO_EXERCITADO')]
-> de REPROVADO para OK (ENFRAQUECIMENTO GRAVE): []
-> outras (de NAO_EXERCITADO/INDETERMINADO): 0 []
```

- **Zero** transições `REPROVADO → OK` (e zero transições vindas de `NAO_EXERCITADO`/`INDETERMINADO`).
- **1024** transições `OK → não-OK`: são as formas malformadas que antes "passavam" e agora viram lacuna
  declarada — **endurecimento**, não afrouxamento.
- **Exatamente uma** transição para fora de `REPROVADO`: `arestas_inventadas = +inf` `REPROVADO → NAO_EXERCITADO`.
  É a **única** mudança de estado nesse sentido (prova analítica: o conjunto `REPROVADO` antigo era
  `{int/float, não-bool, > 0}`; o novo é `{finito, > 0}`; a diferença é só `+inf`). Corresponde à classe de
  mudança já registrada e aceita no parecer da régua (§7 **L3**: `x=inf` sai de `REPROVADO` para
  `NAO_EXERCITADO`, "não é OK nem passa a proteger menos"). O `+inf` **não** fecha OK: vira lacuna técnica
  com motivo nomeado. `NaN`/`-inf`, que antes fechavam `OK` por acaso, agora também não fecham.
- Constatação por `diff`: o `diff -u rstv-ORIGINAL.py rstv.py` tem **apenas 2 hunks** — o comentário do
  cabeçalho e o bloco `arestas` (linhas 769-788). F2/F3 já usavam `_contagem_observada` no ORIGINAL; logo,
  toda e qualquer diferença de comportamento é atribuível só a esse hunk. `DIFF_EXIT=1`.

### Item 6 — não-regressão — **OK**

```
$ python tools/automacao/cenarios/test_rstv.py
RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK, controles reprovam, runtime identifica
EXIT=0

$ python tools/automacao/cenarios/test_tooltips_shrines.py
… 28 linhas RESULTADO|PASSOU|… 
TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0
EXIT=0
```

Consumidores extra (leitura): `tools/automacao/aut5/test_aut5.py` → `EXIT=0` (`RESULTADO|PASSOU|aut5-rstv|16 casos …`);
`tools/automacao/aut5/test_snapshot_modal.py` → `EXIT=0`. **Nenhum** consumidor em `tools/automacao/runtime/`
referencia o campo (`grep -rln "arestas_inventadas\|RSTV-25b" tools/automacao/runtime/` → vazio); o `coletor.py`
foi apenas lido. Nenhum teste pulado; um teste pulado nunca seria contado como verde.

### Item 7 — CONTRA-PROVA em cópia FORA do repo — **OK**

Espelho criado em `rev_l2/{verde,vermelho}/` a partir do `tools/` do repo (mesma sha256
`e1ad69fc…`). No `vermelho`, o hunk `arestas` foi revertido para o `isinstance(..., (int,float))… > 0`
antigo (`sha256 = 31f7d361e27b7fbf55dbafd1a59ca047ddf60f25bbdf97486b1ff74528b2e5fb`). `__pycache__` removido
de ambos para não mascarar bytecode.

```
$ python verde/tools/automacao/cenarios/test_rstv.py
RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK, controles reprovam, runtime identifica
EXIT_VERDE=0

$ python vermelho/tools/automacao/cenarios/test_rstv.py
RESULTADO|REPROVOU|cic3-rstv|L2-string-numero (valor='2'): esperado NAO_EXERCITADO, obtido OK (motivo='leitura runtime completa com identidade suficiente'): esperado 'NAO_EXERCITADO', obtido 'OK'
EXIT_VERMELHO=1
```

O defeito plantado reproduz **exatamente** o achado L2 (`"2"` fechando `OK`) e o runner fica **VERMELHO
exit 1**; sem o defeito, **VERDE exit 0**. Nada disso dentro do repo.

### Item 8 — Critério 6 do cartão (relatório no disco) — **ACHADO (entrega incompleta)**

Busca no disco (só leitura):

```
$ find docs -iname '*L2*'                         -> (vazio)
$ grep -rln "CIC-3-L2" docs/                      -> (vazio, exit 1)
$ find docs/automacao -maxdepth 1 -type f -newermt "2026-10-06 15:00"
  … COR-AUT4-F2-relatorio.md, COR-AUT4-F3-relatorio.md, COR-AUT4-F4-entrega.md, COR-AUT4-F4R-revisao.md …
  (nenhum CIC-3-L2-*.md)
$ grep -rln "arestas_inventadas" docs/ (fora de cenarios)
  docs/automacao/CIC-3R2-revisao.md , docs/automacao/CIC-3R2-evidencias/12-investigacoes-do-revisor.txt
  (a régua e a evidência do achado — NÃO um relatório do autor)
```

**Não existe** relatório da execução do CIC-3-L2 no disco. O critério 6 do cartão pede
"Relatorio com arquivo:linha, comandos exatos, saida literal com exit code e sha256 dos arquivos tocados" —
não cumprido. A correção de código está correta, mas **a entrega do cartão está incompleta**.

---

## 3. Lacunas declaradas (nunca contam como OK)

- **L-a — Autenticidade do "antes" (`rstv-ORIGINAL.py`).** `tools/automacao/` é untracked, então o
  `rstv-ORIGINAL.py` do scratch **não** é atestável por `git`. Ele é corroborado por três fatos medidos:
  (i) o `diff` contra o produto atual tem **só** o hunk do L2; (ii) o bloco antigo contém exatamente o
  `isinstance(..., (int,float)) and ... > 0` que o parecer da régua cita em `rstv.py:767-768`; (iii) o
  comportamento antes × depois casa com o descrito. Ainda assim, a **fonte de verdade do "antes"** usada no
  item 5 é a minha própria reconstrução analítica + brute-force, não a cópia do autor.
- **L-b — Nenhuma medição de runtime.** Tudo é fixture sintética rotulada (`procedencia=runtime` injetada,
  hashes `1*64/2*64`). Nada aqui atesta o mod em jogo; verificação humana em jogo e publicação seguem portões
  separados.
- **Não exercitado:** não rodei o probe/coletor contra o jogo, não builda, não instala; a integração
  CIC-5 é exercitada de forma indireta por `test_rstv.py` (que passou), não por leitura real do produto.
- **Fora de escopo:** a correção **não** foi commitada (o diretório segue untracked). Não é defeito do fix,
  mas o estado "no repo" não é durável a um `clean`.

## 4. Veredito global: **APROVADO COM RESSALVAS**

1. A correção **fecha o L2** (itens 1-3 OK, prova própria) e **não enfraquece a trava** (item 5 OK: nenhum
   `REPROVADO → OK`; a única perda de `REPROVADO` é o `+inf`, que vai para `NAO_EXERCITADO`, nunca OK, e é a
   classe já aceita em §7 L3 da régua).
2. Itens 4 (não circular), 6 (não-regressão) e 7 (contra-prova VERMELHO/VERDE) **OK**.
3. **Ressalva / ACHADO (item 8):** o critério 6 do cartão não foi cumprido — falta o relatório no disco.
   Enquanto ele não existir, o cartão **não** pode ser dado por "done".
