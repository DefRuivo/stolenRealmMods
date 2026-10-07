# CIC-3R2 — revisão independente do COR-CIC3 (`t_7bec518b`)

> **Quem sou eu nesta rodada.** Sou a tarefa `t_d243872d`, revisor — **não** o autor. Nada aqui publica,
> instala, deploya, abre o jogo, carrega save, edita produto, enfraquece trava ou toca `Assembly-CSharp.dll`.
> Escrevi **somente** este documento e `docs/automacao/CIC-3R2-evidencias/`; as bancadas rodaram em cópia
> **fora** do repo (`%LOCALAPPDATA%/hermes/cache/scratch/cic3r2/`) e as saídas foram gravadas na pasta de
> evidências. Nenhum build, nenhum deploy, nenhum commit, nenhuma mutação de Kanban.
>
> **Objeto:** o fechamento dos achados F1-F7 do parecer `docs/automacao/CIC-3R-revisao.md` no produto
> `tools/automacao/cenarios/rstv.py` + `test_rstv.py`, na frente "cenários automáticos RSTV para o ciclo".
> **Método:** plantio **próprio** de cada defeito (nunca leitura de relatório), lente dupla (bytes antigos do
> anexo × bytes atuais do disco), execução das CLIs reais com exit code, e conferência código × régua.
>
> **Veredito final: APROVADO** — os sete achados F1-F7 estão fechados com prova independente; nenhuma trava
> foi enfraquecida; nenhum OK novo apareceu. Duas observações **não bloqueantes** e lacunas declaradas na §6/§7.
> Esta revisão **não fecha o DoD do mod**: verificação humana em jogo e publicação seguem portões separados.

---

## 1. Estado lido (sha256 medido por MIM, no disco)

### 1.1 Produto e relatório do autor

| caminho | sha256 (medido nesta revisão) | confere com o autor? |
|---|---|---|
| `tools/automacao/cenarios/rstv.py` | `2fad23a3bc3dc48c7b2dd5cda3feda64a18d9e3d802c54dbef63696a8a032252` | **sim** |
| `tools/automacao/cenarios/test_rstv.py` | `51f7100791fbe3d179be7f88234f88e545a9f5831d8bdafcdfc6fd4f26b1c073` | **sim** |
| `docs/automacao/COR-CIC3-correcao.md` | `4565ef326296f839c42ef62f9428ff6edc40ae0c3dcc35b68f4d800900e61a3a` | **sim** |

mtime: `rstv.py` 2026-10-06 13:48:42, `test_rstv.py` 13:47:26, `COR-CIC3-correcao.md` 13:51:57.

### 1.2 Réguas

| caminho | sha256 |
|---|---|
| `docs/automacao/CIC-3R-revisao.md` (parecer; a régua dos F1-F7) | `a8416a4800180a37d309cb020e54abd9a60f4e95c41a415db51a7c196c2cb33b` |
| `docs/automacao/CICLO-VALIDACAO-escopo.md` (escopo/aceite) | `b063dfef3c359bde7bee340b5cd527b1f547903080afebdbf73b5edb2510d3b2` |
| `docs/automacao/CIC-3-entrega.md` (entrega anterior da frente) | `6a67cf8ac06aa620b14738cc91485a697800a7538c8556f7e44fe395e6ef3aab` |

### 1.3 Evidência anexada ao cartão `t_7bec518b` (hashes que eu medi)

```
524f719757977436b843bdceb8337b10db4003cba9da64ff3fea788ef327d320  rstv_524f7197.py   (= bytes ANTIGOS do produto)
a42bc2eb382247edf03736f46abc9a66b0babb3ec5fd20f58bfd3199f6d49099  prova_red_f1f7.py
968d10d5c81a5820d40c40826fa2ff0e2b2000aa454da8eb7e30f3b5c42172fa  prova_red_final.txt
47f95040e709bf8ee5f42dc56809a898ad8fc04a8b29f42143b80640aeac21ce  prova_green_final.txt
7070157d9807ccdd2fcc94cfb8fafaa6762923db505211c48f93a74c3aacc9f6  n1_verde_global.txt
5578740f351b92d1d7e1139a0cd4fa9f4767f0776ff56818e5b6c9de80f280b7  ab_log_real.txt
58ecb94772c92c3c0d73bc29890b17bc41b690abb9033408249f83d7b8885f56  gate_puros.txt
```

O anexo `rstv_524f7197.py` tem exatamente o sha256 que o parecer declara para os bytes exercitados em
05/10 (`524f7197…`) — a cópia congelada usada na lente RED é fiel ao produto anterior.

### 1.4 Dependências medidas (e deriva desde o congelamento do parecer)

| caminho | sha256 agora | parecer 05/10 | deriva? |
|---|---|---|---|
| `tools/automacao/ciclo/decisao.py` | `d6de959e73a090e43da2b5438a12ba1739d32be2bd9494c0fe9f0d84d9163933` | `d6de959e…` | não |
| `tools/automacao/runtime/coletor.py` | `c7032285e2e9828d8b3c3c9ffd41420f3a0ccebe0f75440a0b67533135f8ddae` | `0518634eda…` | **sim** |
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `5a51abaa439b90263e3b202e01a0b2b3b343fabc8cb71c9de8b3ac97b343bdd3` | `a2bd3d49…` (snapshot) | **sim** |
| `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` | `fd774259b5e8813f2f3b29e2ff805f12cb0cdab4c277116fcc8bbb7e7e3bffdd` | — | mtime 13:57 |

A deriva é **posterior** ao COR-CIC3 (13:48) e veio da frente AUT-4 (`COR-AUT4`, `t_b62359c3`, 14:05): o
`coletor.py` e o probe C# mudaram, o Release do probe foi recompilado **de novo** às 13:57. Medição de
controle: a suíte do módulo **passa** mesmo com o `coletor.py` novo (o teste `_integracao_cic5` importa o
coletor real) — a deriva da frente vizinha não quebrou esta frente (evidência `01-suite-rstv.txt`).

---

## 2. Comandos exatos, saída literal e exit code

Todos com `cd C:/dev/stolen-realm`, `PYTHONDONTWRITEBYTECODE=1` (nenhuma escrita de `__pycache__` no repo).

### 2.1 Suíte do módulo — `01-suite-rstv.txt`

```
$ python -B tools/automacao/cenarios/test_rstv.py
RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK, controles reprovam, runtime identifica
EXIT=0
```

### 2.2 Contra-prova (isca meta) — `02-contra-prova.txt`

```
$ python -B tools/automacao/cenarios/test_rstv.py --contra-prova
CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os 10 controles passarem (o REPROVADO real vem da regra)
EXIT=0
```

### 2.3 Bancada RED/GREEN do autor, reexecutada por mim — `03-bancada-red-green-do-autor.txt`

```
$ python -B .../rstv_524f7197.py --lente red      (SCRIPT prova_red_f1f7.py, --modulo rstv_524f7197.py)
MODULO .../rstv_524f7197.py sha256=524f719757977436b843bdceb8337b10db4003cba9da64ff3fea788ef327d320
TESTE _fixture_nao_vira_ok   SEM_FALHA falhas=0
TESTE _ausente               SEM_FALHA falhas=0
TESTE _lacunas               SEM_FALHA falhas=0
TESTE _controles             SEM_FALHA falhas=0
TESTE _caminho_ok            SEM_FALHA falhas=0
TESTE _cadeia                SEM_FALHA falhas=0
TESTE _fechamento_f1_f7      SEM_FALHA falhas=56
TESTE _canonico_excecao      SEM_FALHA falhas=0
TESTE _adaptadores           SEM_FALHA falhas=2
TOTAL falhas=58
RED CONFIRMADO: o modulo sob prova NAO satisfaz os testes (defeito presente)
EXIT=0

$ python -B .../prova_red_f1f7.py --modulo tools/automacao/cenarios/rstv.py --lente green
MODULO tools/automacao/cenarios/rstv.py sha256=2fad23a3bc3dc48c7b2dd5cda3feda64a18d9e3d802c54dbef63696a8a032252
... TESTE _fechamento_f1_f7  SEM_FALHA falhas=0   (todos os 9 testes 0 falhas)
TOTAL falhas=0
GREEN CONFIRMADO: 0 falhas no modulo atual
EXIT=0
```

Os **58** = 56 do bloco F1-F7 + 2 de `_adaptadores`. Na lente RED, **os sete** achados saem `OK` com o
motivo antigo: F1/F2/F4 ⇒ `NAO_EXERCITADO` esperado, obtido `OK`; F3-contagem ⇒ `REPROVADO` esperado,
obtido `OK`; F3-valores ⇒ `INDETERMINADO` esperado, obtido `OK`; F5 ⇒ idem; F6 ⇒ obtido `OK` com
`motivo='tooltip renderizado resolvido (sem placeholder)'` (o defeito do F6 literal, no motivo antigo);
F7 ⇒ idem. Confere com `prova_red_final.txt` e `prova_green_final.txt` anexados byte a byte.

### 2.4 Plantio INDEPENDENTE do revisor nos bytes atuais (CLI real) — `04-plantio-revisor-atual.txt`

Base completa = **7 OK / exit 0**. Cada defeito plantado no caso completo derruba **só o alvo** (os outros
6 seguem `OK`), provando que o defeito não é global e que o resto do caso está bem-formado:

| caso | σ alvo | estado do alvo | exit |
|---|---|---|---|
| `BASE-sem-defeito` | — | **7× OK** | 0 |
| F1a `pontos` nunca lidos | skills-pontos | `NAO_EXERCITADO` | 0 |
| F1b `skills` nunca lidas | skills-pontos | `NAO_EXERCITADO` | 0 |
| F1c par `pontos` incompleto | skills-pontos | `NAO_EXERCITADO` | 0 |
| F2a `janelas_duplicadas=null` | tooltip-restauração | `NAO_EXERCITADO` | 0 |
| F2b `=-1` | tooltip-restauração | `NAO_EXERCITADO` | 0 |
| F2c `=false` | tooltip-restauração | `NAO_EXERCITADO` | 0 |
| F2d `=[]` | tooltip-restauração | `NAO_EXERCITADO` | 0 |
| F2e `='0'` (string) | tooltip-restauração | `NAO_EXERCITADO` | 0 |
| F2f `duplicata=null` (sem a contagem) | tooltip-restauração | `NAO_EXERCITADO` | 0 |
| F2g chave de contagem ausente | tooltip-restauração | `NAO_EXERCITADO` | 0 |
| F3a `linhas T4=1` × `Dependency T4=3` | dependência | **`REPROVADO`** | 1 |
| F3b `linhas='abc'` × `Dependency=-2` | dependência | `INDETERMINADO` | 0 |
| F3c `linhas` ausentes | dependência | `INDETERMINADO` | 0 |
| F4a `x='NaN'` | geometria | `NAO_EXERCITADO` | 0 |
| F4b `largura=nan` | geometria | `NAO_EXERCITADO` | 0 |
| F4c `x=inf` | geometria | `NAO_EXERCITADO` | 0 |
| F4d `tela='fullscreen'` | geometria | `NAO_EXERCITADO` | 0 |
| F5a `dll_sha=d*64` + `hash_fonte=b*64` | (cadeia) | `INDETERMINADO` **nos 7** | 2 |
| F5b `hash_dll=d*64` + `hash_fonte=b*64` | (cadeia) | `INDETERMINADO` **nos 7** | 2 |
| F6a só `texto_bruto` (sem render) | placeholders | `NAO_EXERCITADO` | 0 |
| F7a sessões `sessao-A` + `sessao-B` | (ciclo) | `INDETERMINADO` **nos 7** | 2 |

Motivos literais (recorte): F1 `pontos: dimensao NUNCA lida (nenhum par antes/depois completo)`; F2
`janelas_duplicadas MALFORMADA (None): contagem observada valida (numero finito >= 0) e obrigatoria`;
F3a `DEFEITO: T4: linhas=1 != Dependency=3 (o criterio declara 'linhas == Dependency real')`; F3b
`T4: valor INVALIDO no confronto (linhas='abc', Dependency=-2)`; F4 `caixa_na_tela_px MALFORMADA (x='NaN')`;
F5 `hash (dll_sha) declarado com VALORES DIFERENTES na mesma observacao`; F6 `texto RENDERIZADO nao
observado (so o cru)`; F7 `observacoes de SESSOES diferentes (sessao-A, sessao-B) ... nao e prova de um
UNICO ciclo`.

### 2.5 Lente dupla: o defeito é PRÉ-EXISTENTE (não inventado no teste) — `05-dupla-lente-antigo-atual.txt`

Mesma tabela de casos, avaliada por `importlib` nos **dois** bytes. Todos **CONFIRMA**:

| caso | bytes antigos (`524f7197…`) | bytes atuais (`2fad23a3…`) |
|---|---|---|
| F1a pontos nunca lidos | `OK` | `NAO_EXERCITADO` |
| F2a `janelas_duplicadas=null` | `OK` | `NAO_EXERCITADO` |
| F2c `janelas_duplicadas=false` | `OK` | `NAO_EXERCITADO` |
| F3a 1 × 3 | `OK` | `REPROVADO` |
| F3b `'abc'` × `-2` | `OK` | `INDETERMINADO` |
| F4a `x='NaN'` | `OK` | `NAO_EXERCITADO` |
| F5a hash contraditório | `OK` | `INDETERMINADO` |
| F6a cru sem render | `OK` (**motivo antigo: `tooltip renderizado resolvido (sem placeholder)`**) | `NAO_EXERCITADO` |
| F7a sessões misturadas | `OK` | `INDETERMINADO` |

Isto é o que o item 3 do autor afirma, provado **por plantio meu** e não pela bancada dele.

### 2.6 Verde GLOBAL (variante N1 do adendo A3) nas DUAS CLIs reais — `06-n1-verde-global.txt`

Um único ciclo sintético coerente carregando F1 (`pontos` nunca lidos) **e** F2 (`janelas_duplicadas: null`),
com evidência em arquivo existente, submetido a `rstv.py` e depois a `ciclo/decisao.py`:

```
== ANTIGO (rstv=rstv_524f7197.py)
   rstv exit=0 contagem={'OK': 7}
   decisao exit=0 pronto_para_decisao=True falhas_automaticas=0 pendencias_humanas=0
== ATUAL (rstv=rstv.py)
   rstv exit=0 contagem={'OK': 5, 'NAO_EXERCITADO': 2}
   criterio RSTV-6-readonly-skills-pontos: NAO_EXERCITADO | ... pontos: dimensao NUNCA lida ...
   criterio RSTV-21-tooltip-restauracao: NAO_EXERCITADO | ... janelas_duplicadas MALFORMADA (None) ...
   decisao exit=1 pronto_para_decisao=False falhas_automaticas=2 pendencias_humanas=0
```

O buraco do A3 (`pronto_para_decisao=True` saindo de leitura incompleta) **fechou**: a lacuna volta ao
ciclo como **falha automática**, com **0 pendências humanas** — não foi empurrada ao dono. Reproduz o
`n1_verde_global.txt` anexado. Nota de método: a 1ª tentativa minha deu 7 falhas automáticas nos DOIS
bytes porque eu não tinha posto `evidencia` (a `decisao.py` exige evidência em arquivo: "sem evidencia
(label OK nao basta)") — corrigido o meu fixture, o resultado bate; a falha era do meu insumo, não do produto.

### 2.7 Trava: nenhum OK NOVO (a correção não afrouxou nada) — `07-trava-ok-novo.txt`

Estados dos 7 critérios para as **fixtures do módulo** + o artefato positivo + meus 25 casos, nos dois bytes:

- `rstv-observacoes` / `rstv-controles` / `rstv-lacunas` / `rstv-ausente`: estados **idênticos** antigo × atual;
- `rstv-positivo` (sintético, runtime injetado): **7 OK nos dois** — o caminho OK foi preservado;
- todas as diferenças são **saída** do OK (`OK → NAO_EXERCITADO/INDETERMINADO/REPROVADO`);
- `=== OK NOVO (antigo nao-OK -> atual OK): 0 ===`.

Única transição em sentido de severidade branda e **sem virar OK**: `F4c x=+infinito` era `REPROVADO`
(por acidente: `inf > tela` disparava "CLIPPING horizontal") e passou a `NAO_EXERCITADO` (dado não finito =
malformado, motivo do F4). Continua **não-verde**, continua falha automática na decisão, e agora nomeia o
defeito real. Ver lacuna L3 na §7.

### 2.8 Não-regressão (medida nesta revisão) — `08-nao-regressao-suites.txt`

| comando | resultado real | autor declarou |
|---|---|---|
| `ciclo/test_decisao.py` | 127/0, exit 0 | 127/0 exit 0 — **igual** |
| `aceite/test_relatorio_aceite.py` | **15**/0, exit 0 | 14/0 exit 0 — **um check a mais** (de outro cartão depois) |
| `ciclo/test_ciclo.py` | 48 testes OK, exit 0 | exit 0 — **igual** |
| `offline/testes/t_aut3_lib.py` | 25/0, exit 0 | exit 0 — **igual** |
| `aut6/test_cobertura_aut6.py` | rodaram=24 reprovaram=0, exit 0 | 24/0 — **igual** |
| `aut6/test_regressoes_cor_aut6.py` | 26 OK, exit 0 | 26 OK — **igual** |
| 4 suítes AUT-4 (autorização/controle negativo/manifest rollback/observação) | PASSOU, exit 0 | exit 0 — **igual** |
| `roda.sh --puros` (trava do projeto) | **88/88**, 0 reprovadas, **VERDE exit 0** | 87/87 — **um teste a mais** |
| `tools/automacao/aut5/test_aut5.py` | exit **1**, 6 falhas no caso `log-real` | exit 1, mesmas 6 — **igual** |

As 6 falhas do aut5 medidas (literal): identidade de DLL (`a DLL do perfil deveria casar com a build do
repo`, `boot esperado OK ... veio INDETERMINADO`) + as 4 da fila do RSTV-25b (`RSTV-25b-dependencia` e
`AUT5-RSTV-25b-conectores-log` voltando à fila de agente / cobrando roteiro humano). **Mesmas classes** do
que o autor relatou; nada disso passa pelo avaliador desta frente.

**Divergência em relação ao relatório do autor (na direção segura):** os três "já estava vermelho" da
frente AUT-4 que o autor listou (`t_aut4_costura_probe.py`, `t_aut4_plano.py`, `t_aut4_probe_contrato.py`)
**hoje PASSAM, exit 0** — foram consertados depois da rodada dele pelo `COR-AUT4` (`t_b62359c3`, 14:05).
Não é regressão do COR-CIC3 em nenhum dos dois sentidos; é lista desatualizada.

### 2.9 Checagens de doc e citações — `11-checagens-de-doc.txt`, `13-citacoes-conferidas.txt`

- `tools/audita_docs.py`: 5 reclamações, **nenhuma** sobre `COR-CIC3-correcao.md` (são de `docs/README.md`
  e dos relatórios `RSTV-27R*`, de outros cartões).
- `tools/checa_citacoes.py`: 4 reclamações, **nenhuma** sobre `COR-CIC3-correcao.md`.
- O `checa_citacoes` do projeto é **cego** ao padrão `arquivo.py:LINHA` usado neste doc (devolve "0 citações"
  para ele). Conferi com um verificador próprio de bancada (`check_cit.py`, script local de revisão, fora do repo): **18 citações `arquivo:linha` encontradas,
  18 resolvem, 0 pendentes** — inclusive as 7 do §1 do relatório do autor e o par decisivo `rstv.py:805-807`.

### 2.10 Diff do produto (bytes antigos × atuais) — `10-diff-produto-antigo-atual.txt`

`diff -u` = 14 hunks, +234/-40. Todos os hunks são dos F1-F7 (cabeçalho/docstrings, `_hashes_obs`/F5,
`_fecha`/F5+F7, `_contagem_observada`+F1 em `_cap_skills_pontos`, F2 na tooltip, F6 em placeholders, F3 no
loop de tiers, `_numero_finito`/`_bbox`/F4). As capacidades `RSTV-6-readonly-personagem` e
`RSTV-21-janela-ciclo`, o achado secundário S1 e o `@x@` cru **não foram tocados** — confere com o §1 do
relatório do autor.

---

## 3. Veredito por item F1-F7

| item | veredito | prova (tudo por execução própria) |
|---|---|---|
| **F1** dimensão nunca lida (skills/pontos) | **OK** | plantio F1a/F1b/F1c ⇒ `NAO_EXERCITADO` nomeando a dimensão; antigo ⇒ `OK`; base volta a 7 OK. Código: `lidas` só marca par COMPLETO (`rstv.py:550,582,593`) e o bloco `if dados:` (`:599-606`) transforma a dimensão nunca lida em motivo. |
| **F2** contagem inválida não prova ausência | **OK** | plantio F2a-F2g (`null`, `-1`, `false`, `[]`, `'0'`, `duplicata=null`, chave ausente) todos ⇒ `NAO_EXERCITADO`; antigo ⇒ `OK` para null/bool. Helper `_contagem_observada` (`:516-525`) e o `else:` do F2 (`:668-687`). |
| **F3** truthiness no confronto de dependência | **OK** | plantio F3a ⇒ **`REPROVADO`** com motivo literal `linhas=1 != Dependency=3` (exit 1); F3b ⇒ `INDETERMINADO` (`valor INVALIDO no confronto`) ; F3c (linhas ausentes) ⇒ `INDETERMINADO`. Antigo ⇒ `OK` nos três. Detalhe do ponto aberto na §5. |
| **F4** geometria não finita | **OK** | plantio F4a-F4d (`x='NaN'`, `largura=nan`, `x=inf`, `tela='fullscreen'`) ⇒ `NAO_EXERCITADO` com motivo; antigo ⇒ `OK`. `_numero_finito` (`:823-840`) + `_bbox` (`:843-879`) + a entrada de `invalido` em contrib (`:886-891`). |
| **F5** alias de hash contraditório | **OK** | plantio F5a (`dll_sha`) e F5b (`hash_dll`) com o alias `hash_fonte` bom ⇒ `INDETERMINADO` **em todos os 7 critérios**, motivo `VALORES DIFERENTES na mesma observacao`; antigo ⇒ `OK` no alvo. `_hashes_obs` devolve **conjunto** por chave canônica (`:253-275`), `_checagem_hashes` marca contradição como divergente (`:294-296`) e `_fecha` tem o ramo explícito (`:438-444`). |
| **F6** render não observado | **OK** | plantio F6a (só `texto_bruto`) ⇒ `NAO_EXERCITADO`, motivo `texto RENDERIZADO nao observado (so o cru)`; antigo ⇒ `OK` com motivo `tooltip renderizado resolvido (sem placeholder)`. O template CRU com `[N]` continua **legítimo** (o `indice-literal` só reprova no renderizado) — o teste `_adaptadores` cobre isso nos dois bytes. |
| **F7** sessões misturadas | **OK** | plantio F7a (sessão A + sessão B no mesmo ciclo) ⇒ `INDETERMINADO` **nos 7**, motivo `SESSOES diferentes ... nao e prova de um UNICO ciclo`; antigo ⇒ `OK`. O ramo (`:425-432`) está **antes** do `runtime_ok`, e `_extras` só copia `sessao` no caminho OK — onde há no máximo uma sessão. |

**Nenhum item ficou ACHADO ou INDETERMINADO.** Nenhuma trava foi enfraquecida: a §2.7 mostra 0 OK novo em
todas as fixtures do módulo + 25 casos meus, e a §2.10 mostra que a mudança está confinada aos F1-F7.

### 3.1 As quatro afirmações do autor, item por item

1. **"o verde global passou a exigir leitura completa e bem-formada de cada dimensão" — CONFIRMADO.**
   Por capacidade: personagem (alvo declarado obrigatório), skills **e** pontos (F1), `janela` com
   `aberta`+`fechada`, pai+índice+contagem (F2), render observado (F6), contagem válida dos dois lados (F3),
   bbox finita + tela (F4); e no nível global pelo N1 (§2.6, `pronto_para_decisao` cai de `True` para `False`).
   Com a ressalva da lacuna L2 (§7) — o campo `arestas_inventadas` é a exceção que sobrou.
2. **"dimensão nunca lida, contagem null/inválida, truthiness, geometria não finita, alias contraditório,
   render não observado e sessões misturadas deixam de fechar OK" — CONFIRMADO** com 21 casos plantados (§2.4).
3. **"cada F1-F7 tem prova vermelho→verde (58 falhas / 0 falhas)" — CONFIRMADO**, e mais: provei que o defeito
   é **pré-existente** nos bytes antigos por plantio próprio (§2.5), não só pela bancada do autor.
4. **"a suíte do módulo roda verde e a contra-prova reprova" — CONFIRMADO com uma precisão de wording:**
   literalmente, `--contra-prova` sai **`CONTRA-PROVA|PASSOU` exit 0** (a isca "sempre OK" deixa os 10
   controles passarem — é o resultado *correto*). A frase "a contra-prova reprova" descreve o efeito da
   isca, não o exit do comando. Ver observação O2 (§7) sobre o alcance dessa isca.

---

## 4. Conferência código × régua

- `CICLO-VALIDACAO-escopo.md:31` exige: "Ausencia/falha de cadeia => NAO_EXERCITADO/INDETERMINADO, nunca OK"
  e "esses valores devem ser confrontados com identidade/manifest da coleta, nao derivados somente de um
  rotulo runtime". O código mantém: `_evidencia_runtime` (`:307-318`) exige procedência runtime **+** sessão
  **+** `hash_fonte` **+** identidade suficiente **+** cadeia limpa; sem isso o caminho OK não existe.
- `CICLO-VALIDACAO-escopo.md:32` ("lacuna de probe/campo/coleta => falha automatizável, não ao dono por
  default"): `_extras` (`:359-389`) marca `tipo_pendencia='tecnica'` + `autorizacao_necessaria=False`, e o
  N1 confirma **0 pendências humanas** com 2 falhas automáticas — casa com o aceite #3.
- `CIC-3-entrega.md:40-42` ("AUSENTE/INDETERMINADO/NAO_EXERCITADO nunca são OK; incompleto/malformado idem"):
  o parecer apontou que isso era **falso** para F1/F2/F3/F4/F6/F7; agora a §2.4/§2.5 mostra o contrário. As
  lacunas declaradas (`lacuna_probe`) continuam declaradas, não maquiadas.
- `CIC-3R-revisao.md` §5 (F1-F7) e §9.4 (semântica de dependências): F1, F2, F4, F5, F6, F7 fechados como o
  parecer pede; F3 tratado na §5 abaixo.
- `CIC-3R-revisao.md` §5 F6 ("não cobrar reprovação do template legítimo: cobrar distinção entre não
  observado e resolvido"): o código distingue (`indice-literal` só no renderizado; `[N]` cru não reprova) —
  exatamente o pedido, sem endurecimento extra.
- O parecer reserva ao pai a decisão sobre `config_sha` relevante e sobre a costura AUT-5/coletor. O
  COR-CIC3 **não** ampliou escopo para isso (declarado no §8 do relatório dele) — verificado no diff (§2.10).

---

## 5. O ponto aberto de F3 (confirmar ou derrubar)

**O que o autor registrou:** F3 implementou **igualdade por tier**; se o pai fixar "só presença", o único
ponto a relaxar é o `elif` de igualdade em `rstv.py:805-807`.

**Medição:** o `elif` existe exatamente em `rstv.py:805-807`:
`elif v_lin is not None and v_dep is not None and v_lin != v_dep:` → defeito. É o **único** lugar que compara
as duas contagens; os ramos anteriores tratam presença/ausência por tier (`:800-804`). Confirmado: é um
ponto único e isolado.

**A semântica casa com o critério?** **SIM — não há divergência.** O próprio critério declara igualdade em
dois lugares do produto: `CAPACIDADES` ("linhas por tier **condizem com** Dependency", `rstv.py:158-159`) e
o campo `esperado` (`"linhas == Dependency real; T5 sem Dependency e legitimo"`, `rstv.py:814`). E a régua
derivada da fonte do mod é ainda mais explícita (`docs/automacao/AUT-5-relatorio.md`, §6): "a soma dos nós
com Dependency **tem de casar** com as linhas ativas — faltando linha, é o próprio sintoma do RSTV-25b;
sobrando, é conector sem Dependency", com o confronto **por tier**. O parecer (F3) pediu decisão do pai
apenas *"caso regra seja só presença"* — não é o caso: a regra declarada é igualdade.

**Consequência se o pai relaxar:** seria **enfraquecimento de trava**, e do tipo que o projeto chama de pior
defeito. Com "só presença", `linhas T4=1` × `Dependency T4=3` — que é exatamente o **sintoma do RSTV-25b**
(conector ausente) — voltaria a fechar `OK` (comprovado: nos bytes antigos, §2.5, esse caso saía `OK`).
Recomendação: **manter a igualdade**; a decisão do pai não é necessária enquanto ninguém quiser mudar o
critério. Se ele quiser mudar, a mudança é de critério e precisa da decisão do dono — não de um agente.

---

## 6. Lacunas declaradas (nunca contam como OK)

- **L1 — Runtime `NAO_EXERCITADO`.** Nenhuma leitura de jogo nesta revisão nem na correção: sem jogo, save,
  probe, build, instalação, deploy ou publicação. Todos os dados dos F1-F7 são **fixtures sintéticas
  rotuladas** (`procedencia=runtime` injetada, hashes `a*64/b*64`). Isto não atesta o mod em jogo.
- **L2 — `arestas_inventadas` malformado passa batido** (mesma classe F2/F3, **fora** dos sete itens).
  Medição: no caso completo, `arestas_inventadas="2"` (string) ⇒ critério **`OK`**; `arestas_inventadas=2`
  (número) ⇒ `REPROVADO` (`aresta de dependencia INVENTADA`). O valor é lido com `isinstance(..., (int,
  float))` (`rstv.py:767-768`) e um valor textual **não** é tratado como leitura malformada. É
  **pré-existente e intocado** pelo diff (§2.10) — o COR-CIC3 não o introduziu nem alegou cobri-lo. Não
  bloqueia F1-F7 e não afrouxa nada, mas é a mesma família de defeito ("campo presente com valor
  malformado não vira não-OK") e merece cartão próprio. Evidência: `12-investigacoes-do-revisor.txt`.
- **L3 — `F4` reclassifica `x=inf` de `REPROVADO` para `NAO_EXERCITADO`.** Não é OK nem passa a proteger
  menos (continua falha automática, agora com motivo correto), mas perde a severidade `REPROVADO` que o
  acaso do `float()`/comparação dava. Registrado para o pai; não é regressão nem requisito.
- **L4 — `docs/automacao/CIC-3-entrega.md` ainda declara `rstv.py = 524f7197…`.** O autor já registra que
  esse hash virou **histórico** e não reescreveu o documento (correto: a entrega anterior é estado
  anterior). Fica a dívida documental para o pai decidir onde ancorar o estado novo.
- **L5 — Independência nominal do revisor.** O parecer (§1) marcou `INDETERMINADO` o provenance de quem
  implementou o CIC-3. Esta revisão é um contexto novo e não-autoral (rodada `t_d243872d`, run 426, não
  participou de 335/346/355 nem de `t_7bec518b`), mas eu **não** recupero nem atesto a identidade
  administrativa do autor original — isso segue com o pai.
- **L6 — Deriva da frente vizinha.** `coletor.py`, `AUT4ProbePlugin.cs` e o Release do probe mudaram depois
  do congelamento e depois da correção (§1.4). Esta revisão mede os bytes de hoje; uma nova mudança invalida
  esta âncora (aceite #2).
- **L7 — Dados de probe ainda inexistentes.** O F3 corrige o **confronto**, não a **fonte**: o probe/coletor
  continua sem emitir linhas por tier, então `RSTV-25b` na coleta real segue `INDETERMINADO` — é lacuna
  técnica (fila de agente), não OK.

---

## 7. Observações não bloqueantes

- **O1 — Estado das suítes mudou depois da rodada do autor, na direção segura.** Aceite 15/0 (era 14/0) e
  `roda.sh --puros` 88/88 (era 87/87): testes acrescentados por outros cartões. As três suítes AUT-4 que o
  autor listou como vermelhas/pré-existentes hoje **passam** (consertadas pelo `COR-AUT4`). Nada disso é
  regressão do COR-CIC3.
- **O2 — A isca meta da contra-prova é mais fraca do que o texto sugere.** Ela troca `_fecha` por
  `sempre-OK` e verifica que os 10 controles deixam de reprovar. Medição minha: com `_fecha` trocado por um
  que **sempre levanta exceção**, os 10 controles também deixam de reprovar (`avaliar` captura a exceção e
  devolve `INDETERMINADO`), e a contra-prova **também diria `PASSOU`** — ou seja, ela não distingue "a regra
  é a fonte do REPROVADO" de "o avaliador quebrou". Isso **não** enfraquece o portão: quem prova que cada
  defeito plantado reprova de verdade é o bloco `_controles` da suíte principal (exit 0), com a `_fecha`
  real. Evidência: `12-investigacoes-do-revisor.txt`.
- **O3 — Wording do item 4 do autor.** "a contra-prova reprova" vs. o literal `CONTRA-PROVA|PASSOU`
  (exit 0). Só precisão de frase; o comando e o exit code estão certos.
- **O4 — `--out` do `rstv.py` grava o resumo com `criterios`,** que é o que a `decisao.py` aceita
  (`--criterios` aceita lista ou `{criterios:[...]}`). Sem atrito na costura entre as duas CLIs (§2.6).

---

## 8. Veredito final

**APROVADO** para o objeto desta revisão: **F1-F7 fechados** no produto, cada um com prova
vermelho→verde obtida por **plantio próprio do revisor** nos dois conjuntos de bytes, com o funil
reprovando o defeito e voltando a `OK` sem ele, com o verde global deixando de sair de leitura incompleta, e
com **nenhuma trava enfraquecida** (0 OK novo; toda diferença antigo→atual é saída do OK ou reclassificação
dentro do não-verde).

**Nada listado como "falta" que bloqueie o aceite.** As pendências registradas para o pai (não são
`CHANGES REQUESTED`; são encaminhamentos):

1. **L2** — abrir cartão para `arestas_inventadas` malformado (mesma classe F2/F3, pré-existente): aceitar
   contagem observada válida OU declarar leitura malformada; hoje `"2"` fecha `OK`.
2. **F3** — **não** relaxar o `elif` de igualdade (`rstv.py:805-807`): a semântica declarada é igualdade e
   relaxar reintroduz o sintoma do RSTV-25b como `OK`. Se o pai quiser mudar o critério, é decisão do dono.
3. **L4** — decidir onde ancorar o estado novo de `rstv.py` (o `CIC-3-entrega.md` já está histórico).
4. **L5** — provenance do CIC-3 original segue `INDETERMINADO`; esta revisão é contexto novo não-autoral,
   mas não substitui identificação administrativa.
5. **L6** — a deriva da frente AUT-4 (`coletor.py`/probe/Release 13:57) não quebrou esta frente (a suíte
   passa com o coletor novo), mas nova mudança invalida esta âncora.

**O DoD do mod NÃO está fechado por esta revisão.** Verificação humana em jogo e publicação na Thunderstore
são portões separados, do dono; e o runtime segue `NAO_EXERCITADO`.

---

## 9. Índice da evidência bruta

```
docs/automacao/CIC-3R2-evidencias/
  01-suite-rstv.txt                 suíte do módulo (saída literal + EXIT)
  02-contra-prova.txt               isca meta
  03-bancada-red-green-do-autor.txt lente RED (58 falhas) e GREEN (0) reexecutadas por mim
  04-plantio-revisor-atual.txt      plantio INDEPENDENTE, 25 casos, CLI real (estados + exit)
  05-dupla-lente-antigo-atual.txt   mesmos casos nos bytes antigos × atuais (importlib)
  06-n1-verde-global.txt            variante N1 nas duas CLIs reais (rstv.py + decisao.py)
  07-trava-ok-novo.txt              fixtures + 25 casos: toda diferença antigo→atual e 0 OK novo
  08-nao-regressao-suites.txt       decisão/aceite/ciclo/aut3/aut6/7×AUT-4/aut5/roda.sh --puros
  09-hashes.txt                     sha256 e mtime dos arquivos do objeto, dependências e anexos
  10-diff-produto-antigo-atual.txt  diff -u completo (14 hunks) dos bytes antigos × atuais
  11-checagens-de-doc.txt           audita_docs e checa_citacoes (nenhuma reclamação da COR-CIC3)
  12-investigacoes-do-revisor.txt   L2 (arestas_inventadas) e O2 (alcance da isca)
  13-citacoes-conferidas.txt        18 citações arquivo:linha do COR-CIC3 conferidas + cegueira do checa_citacoes
  14-ancora-final.txt               conferência final: hashes do objeto e suíte reexecutadas no fim da revisão
```

**Conferência final de âncora (2026-10-06 14:44 local):** `rstv.py`, `test_rstv.py` e
`COR-CIC3-correcao.md` seguem com os **mesmos** sha256 da §1.1 e a suíte + contra-prova seguem `exit 0` —
nenhuma deriva durante a revisão. Aviso de concorrência: o repo está sendo escrito por **outros** cartões
em paralelo nesta janela (`CIC-4R3-*`, `COR-AUT4R-*`, `RV-15-*` aparecem com mtime posterior a 14:30,
todos de outras frentes). Nenhum desses arquivos é meu nem passa por esta revisão; meus únicos caminhos
escritos são `docs/automacao/CIC-3R2-revisao.md` e `docs/automacao/CIC-3R2-evidencias/`.

Bancadas do revisor (fora do repo): `%LOCALAPPDATA%/hermes/cache/scratch/cic3r2/` — `plantio.py`,
`dupla_lente.py`, `n1.py`, `diff_fixtures.py`, `check_cit.py` (scripts locais de bancada, fora do repo), `gera_evidencia.sh`, `resultado_*.json`.

Revisor: tarefa `t_d243872d`, run 426, profile `default` — **não** autor de `t_7bec518b` nem do CIC-3.
Sem build, deploy, jogo, save, commit, push ou publicação nesta rodada.
