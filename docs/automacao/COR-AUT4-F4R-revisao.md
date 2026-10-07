# COR-AUT4-F4R — revisão independente da derivação interna de `evidencia_runtime` (coletor AUT-4)

Revisor: subagente `default` (**autor ≠ revisor**). Data: **2026-10-06**. Card: `t_0f94af86`;
tarefa-mãe revisada: **COR-AUT4-F4** (`t_1844712b`).
Escopo: `tools/automacao/runtime/coletor.py` (função `consolidar_probe` / `_mapear_saida_probe`),
`tools/automacao/runtime/testes/t_aut4_costura_probe.py` e `docs/automacao/COR-AUT4-F4-entrega.md`.

**Regras cumpridas:** nada publicado, nenhum mod instalado, jogo **não** aberto, nada commitado nem
staged (`git diff --cached` vazio), nenhum `git add`; `tools/automacao/estilo/**`, `aceite/**`, fontes dos
mods e `lib/Assembly-CSharp.dll` **não** tocados; nenhum token/PAT em arquivo/log/resumo; nenhuma tarefa
do Kanban criada ou mutada; **o conserto nunca foi revertido dentro do repo** — toda reversão/planto
ocorreu em cópias fora dele (`…/cache/scratch/f4r_rev/`).

---

## 0. Veredito por item

| # | item | veredito |
|---|---|---|
| 1 | presença derivada da ENTRADA CRUA (não da chave do artefato); autocontraditório cai em FIXTURE/exit 2 | **OK** — medido por execução; pré-conserto CONFIRMAVA (§1) |
| 2 | sentinela `_MARCA_MAPEADO` é forjável por artefato? | **OK — não forjável** por JSON/dict; só por identidade do objeto em processo (§2) |
| 3 | idempotência nos 3 caminhos (cru / arquivo / já mapeado) | **OK** — 3 caminhos + 3ª passagem + cópias (§3) |
| 4 | não-regressão dos consumidores e critério de trava | **OK** — 5 suites exit 0 e idênticas ao declarado; nenhum consumidor lê a chave interna; matriz: só endureceu (§4) |
| 5 | prova RED→GREEN alegada é reproduzível? | **OK** — RED reproduzido em cópia fora do repo, mensagem **literal** igual à do §3.1 (§5) |
| 6 | contra-prova em cópia: com defeito VERMELHO/exit 1, sem defeito VERDE/exit 0 | **OK** — medido nas duas cópias (§6) |
| 7 | alguma trava foi ENFRAQUECIDA? | **OK com ressalva** — nenhum critério julgado (F3/F3R) foi afrouxado; 6 formas flipam FIXTURE→CONFIRMADA e o relatório não registra isso (§7 → ACHADO-1) |
| 8 | falsos OK no relatório (hashes, contagens, exit codes, caminhos de teste) | **1 ACHADO de documentação** (§7/ACHADO-1); hashes, contagens, exit codes e caminhos conferem (§8) |

**Veredito final: APROVADO** — o defeito residual da COR-AUT4-F3R está fechado e o conserto é real e
mensurável. Com **1 achado de documentação não bloqueante** (ACHADO-1: o relatório apresenta como
"comportamento preservado" uma forma que **mudou** de FIXTURE/2 para CONFIRMADA/0, e afirma "nenhuma trava
foi enfraquecida" sem anotar essa mudança). Nada em jogo foi exercitado (segue NÃO EXERCITADO).

---

## 1. Item 1 — a presença sai MESMO da entrada crua? — **OK**

Artefato-sonda plantado por mim (`scratch/f4r_rev/art/`, gerado por `gerar_artefatos.py`): a fixture
`probe-saida-exemplo` **sem** `procedencia`/`rotulo_fixture`, com
`evidencia_runtime: "false"` **e** `evidencia_runtime_presente: false` (e a variante `0`):
`f4_false.json` sha256 `3446698d23b52923b2ad8538c0491eb615d6964ec22d4d50bd6764161bed1db2`
`f4_zero.json`  sha256 `024ea8d72b9552374776a4a490d495e0abdc94b5d7c30991936dff0dec55c4fa`

Comando (idêntico nas duas árvores; disparado por `roda_sondas.py` linha por linha):

```
python <raiz>/tools/automacao/runtime/coletor.py \
  --plano <raiz>/tools/automacao/runtime/fixtures/plano-exemplo.entrada.json \
  --saida-probe <scratch>/f4r_rev/art/f4_false.json \
  --alvos objeto texto_bruto fonte material shader keywords cores geometria owners
```

Saída **literal** no **REPO (com o conserto)** — cabeça do JSON + exit code:

```
{
  "esquema": "AUT-4/1",
  "status": "FIXTURE",
  "evidencia_runtime": false,
  "veredito": "NAO PROVA RUNTIME: fixture rotulada — nunca apresentar como resultado de jogo",
  "motivo": "o proprio artefato se declara fixture (evidencia_runtime='false' nao e o bool False nem o bool True: forma nao-canonica, recusada como fixture): o rotulo tem precedencia sobre a intencao do chamador",
  ...
```
exit code = **2**. A variante `presente=0` (`f4_zero.json`) dá **FIXTURE / exit 2** idem.

Saída **literal** na **cópia com o conserto revertido** (só o bloco da presença; ver §5):

```
{
  "esquema": "AUT-4/1",
  "status": "CONFIRMADA",
  "evidencia_runtime": true,
  "observacoes": [ ... ]
  "veredito": "DESFECHO CONFIRMADO nas observacoes medidas. Nota: texto_renderizado marcado(s) NAO_APLICAVEL (fallback inativo declarado) — NAO e leitura renderizada."
```
exit code = **0** → **o "antes CONFIRMAVA" está confirmado** (defeito vivo reproduzido), e o conserto
manda a mesma entrada para FIXTURE/exit 2.

## 2. Item 2 — o sentinela `_MARCA_MAPEADO` é forjável? — **OK: não por artefato**

`_MarcaMapeado` é um **objeto em memória** e a decisão é `dados.get(_CHAVE_MAPEADO) is _MARCA_MAPEADO`
(`coletor.py:502`), isto é, **identidade**, não tipo nem valor. Tentei forjar por artefato real (JSON) e
pelo caminho dict/API (`bordas_sentinela.py`, Parte C):

```
1) JSON de artefato com  "_cor_aut4_mapeado": "<mapeado-pelo-coletor>"  + ev="false" + presente=false
   -> FIXTURE / exit 2        (se a forja pegasse, presença=False -> CONFIRMADA/exit 0)
2) JSON de artefato com  "_cor_aut4_mapeado": true                      -> FIXTURE / exit 2
3) dict com marcador STRING / BOOL True / None / {} / []                -> FIXTURE / exit 2 (todos)
4) dict com marcador = INSTANCIA NOVA da mesma classe (_MarcaMapeado()) -> FIXTURE / exit 2
5) dict com marcador = o OBJETO real (_MARCA_MAPEADO)                  -> CONFIRMADA / exit 0
```

Conclusão: o sentinela **não é forjável por artefato** (JSON não reconstrói o objeto; um segundo
objeto da mesma classe não satisfaz `is`). Ele **só** é satisfeito por código no mesmo processo que
importe o nome privado (linha 5). Isso não reabre o defeito revisado — o vetor do achado F3R era **o
artefato governar o próprio veredito**, e isso está fechado. A borda (código em processo) fica registrada
como limite declarado da prova, não como achado.

## 3. Item 3 — idempotência nos 3 caminhos — **OK**

`idem_matriz.py` (Parte A), contra o módulo do repo:

```
A1 dict CRU (chave ausente)          -> CONFIRMADA/0
A2 JSON de arquivo (chave ausente)   -> CONFIRMADA/0
A3 dict JA MAPEADO (2a passagem)     -> CONFIRMADA/0
A4 dict mapeado 2x (3a passagem)     -> CONFIRMADA/0
   marcador no mapeado               -> <mapeado-pelo-coletor>
A5 mapeado via deepcopy              -> CONFIRMADA/0
C8 dict(mapeado) (copia rasa)        -> CONFIRMADA/0
C9 copy.deepcopy(mapeado)            -> CONFIRMADA/0
A6 mapeado de bool_true              -> CONFIRMADA/0
A7 mapeado do autocontraditorio      -> FIXTURE/2
A8 mapeado do forjado com sentinela  -> FIXTURE/2
```

Os três requisitos pedidos estão atendidos nos três caminhos: **chave ausente = runtime** (A1–A4,
A6, C8, C9), **bool `True` legítimo = runtime** (A6 + `bool_true` no CLI), **qualquer outra forma
presente = fixture** (A7, A8 + Parte D abaixo, 17 formas erradas → FIXTURE/exit 2). Não consegui
refutar nenhum caminho.

## 4. Item 4 — não-regressão dos consumidores e o critério de trava — **OK**

Rodadas no repo (`cwd = C:\dev\stolen-realm`), exit codes medidos por mim:

```
python tools/automacao/runtime/roda_testes_runtime.py                -> VERDE (exit 0) — 9 teste(s)
python tools/automacao/runtime/roda_testes_runtime.py --contra-prova -> VERDE (exit 0) — 16 teste(s)
python tools/automacao/cenarios/test_rstv.py                         -> RESULTADO|PASSOU|cic3-rstv|...   exit 0
python tools/automacao/cenarios/test_tooltips_shrines.py             -> TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0  exit 0
python tools/automacao/aut6/test_cobertura_aut6.py                   -> TOTAL|rodaram=24 reprovaram=0      exit 0
python tools/automacao/aut6/test_regressoes_cor_aut6.py              -> Ran 26 tests ... OK                exit 0
python tools/automacao/estilo/test_estilo_atributos.py               -> total: 28 | falhas: 0  TUDO OK     exit 0
```

Todos os números **coincidem** com os declarados no relatório do autor.

Critério de trava — comparação pré × pós conserto (não por leitura do relatório, por **medição**):

* `evidencia_runtime_presente` só existe em `tools/automacao/runtime/coletor.py` e no teste novo
  (varredura `grep -rn` em `tools/`): **nenhum consumidor lê a chave interna** — logo o conserto não pode
  afrouxar consumidor por essa via.
* matriz de comportamento (Parte B de `idem_matriz.py`): 12 formas de `evidencia_runtime` × 9 de
  `evidencia_runtime_presente` × 3 de `procedencia` = **660 passagens** comparadas entre o módulo do repo
  e o módulo com o conserto revertido:
  `iguais 436 | ENDURECEU (antes CONFIRMADA/0 → agora FIXTURE/2) 200 | AFROUXOU 12`.
  As 200 são exatamente o defeito que o F4 fecha. As **12** estão analisadas no item 7.
* o critério endurecido na COR-AUT4-F3 fica **intacto**: varredura de FORMA com `presente` ausente
  reproduz, forma por forma, a coluna "FIX" da revisão COR-AUT4-F3R §3 — só `<ausente>` e bool `True`
  confirmam; as outras 17 formas (`false`, `False`, `'FALSE'`, `' false '`, `1`, `0`, `2`, `'0'`,
  `'1'`, `'true'`, `'True'`, `null`, `[]`, `{}`, `''`, `'no'`) → **FIXTURE/exit 2**.

**Comparação do veredito: a proteção ficou IGUAL ou MAIS FORTE para todo consumidor.** Ressalva honesta:
**nenhuma** das suites de consumidores discrimina o F4 (medi: nas cópias com e sem o defeito elas dão
resultado idêntico — as falhas nas cópias são só `FileNotFoundError` de fontes de mods ausentes da cópia
parcial, iguais nos dois lados). A trava do F4 vive **exclusivamente** no bloco novo de
`t_aut4_costura_probe.py` — que é o teste que fica VERMELHO quando o conserto é revertido (§5), logo há
trava de regressão real; só não há redundância.

## 5. Item 5 — a prova RED→GREEN é reproduzível? — **OK**

Reversão **minha**, somente em cópia fora do repo (`…/f4r_rev/com/`, criada por cópia byte a byte do repo;
`sha256` do `coletor.py` revertido = `94e62e57a1be1be2467833b5687f78f60bb2933be0dd327fe31654a50b3a5523`),
trocando **apenas** o bloco da presença pelo código pré-conserto (o mesmo citado no §1 do relatório):

```
cd scratch/f4r_rev/com && python tools/automacao/runtime/roda_testes_runtime.py
[REPROVOU                                  ] testes\t_aut4_costura_probe.py
        | RESULTADO|REPROVOU|aut4-costura-probe|F4: campo presente em forma errada + presente=False tem de sair FIXTURE: esperado 'FIXTURE', obtido 'CONFIRMADA'
 VEREDITO: VERMELHO (exit 1)
EXIT_COM_DEFEITO=1
```

Mensagem **literalmente idêntica** à registrada no §3.1 do relatório do autor. Na cópia sem o defeito
(bytes == repo, `dee03a8f…`) a mesma linha sai `VERDE (exit 0) — 9 teste(s)` / `EXIT_SEM_DEFEITO=0`.
O repo **não** foi tocado: `sha256` do `coletor.py` continua `dee03a8fd16d95730ede993a14747406a37ba44f8a7ea97a6a666995fb7ef3e5`
depois de todas as provas.

Corroboração adicional: o meu revert difere do defeito plantado pelo autor
(`cp_f4_com_defeito/…/coletor.py`, `1875fef1…`) **apenas em uma linha de comentário** — as duas
reconstruções independentes do pré-conserto coincidem, e ambas coincidem com o trecho citado no §1.

## 6. Item 6 — contra-prova em cópia (fora do repo) — **OK**

```
[copia COM defeito] python tools/automacao/runtime/roda_testes_runtime.py                  -> VERMELHO (exit 1)
[copia SEM defeito] python tools/automacao/runtime/roda_testes_runtime.py                  -> VERDE (exit 0) — 9 teste(s)
[copia COM defeito] python tools/automacao/runtime/roda_testes_runtime.py --contra-prova   -> VERDE (exit 0) — 16 teste(s)   ISCA_EXIT_COM_DEFEITO=0
[copia SEM defeito] python tools/automacao/runtime/roda_testes_runtime.py --contra-prova   -> VERDE (exit 0) — 16 teste(s)   ISCA_EXIT_SEM_DEFEITO=0
```

Igual ao declarado no §4 do relatório. Observação: o defeito plantado **não** derruba nenhuma das 16
iscas (a isca de forma errada do F3 reprova nos dois lados, porque a forma errada sozinha já era tratada
pelo F3): a única rede de captura do F4 é o teste da suite. Fica registrado como sugestão de cobertura
(uma isca `cp_aut4_isca_presente_interno_mente`), não como achado.

## 7. Item 7 — alguma trava foi enfraquecida? — **OK com ressalva (ACHADO-1)**

**Nenhum critério julgado foi afrouxado.** O que a F3 endureceu continua endurecido (§4, Parte D
reproduz a coluna "FIX" da F3R §3). Nada do que a F3R julgou OK (chave AUSENTE = runtime; bool `True`
legítimo = runtime) foi alterado: as 36 passagens dessas duas formas estão no grupo "iguais".

**Ressalva medida (a única direção "mais frouxa" que a matriz encontrou — 12 de 660):** artefato que
**omite** `evidencia_runtime` mas carrega `evidencia_runtime_presente` com valor **truthy**
(`true`, `1`, `"false"`), nas duas passagens:

```
antes (revertido): FIXTURE/2        depois (repo): CONFIRMADA/0
```

Isso **não** é perda de proteção real, e a prova é a mesma matriz: no código pré-conserto, **o mesmo
artefato sem a chave `evidencia_runtime_presente` já confirmava** (`CONFIRMADA/0` — caso `sem_chave` na
cópia revertida, e a linha `AUSENTE (sem chave) | CONFIRMADA exit=0` do §3 da F3R). Ou seja, a
"severidade extra" pré-F4 nessa forma era **efeito colateral do próprio defeito** (a chave interna do
artefato era usada como marca de "já mapeado"; com ela truthy e `evidencia_runtime` ausente, o valor
`None` caía em "forma não-canônica"), e era contornável em um passo — apagar uma chave. Nada no pipeline
emite essa chave (grep: só `coletor.py` e o teste), e a recomendação do próprio parecer F3R §7 era
"derivar a presença internamente", o que **implica** exatamente esse flip. Portanto: **não é mudança de
critério de trava**; é a borda que a F4 veio fechar.

### ACHADO-1 (documentação, não bloqueante)

O relatório do autor, no §2 (tabela) e no §7, trata essa forma como comportamento preservado:

* §2, última linha da tabela: "artefato mentindo `presente=true` para chave ausente → continua runtime";
  no **pré-conserto era FIXTURE/exit 2** (medido) — não é "continuar", é **mudar**.
* §7: "Nenhuma trava foi enfraquecida para 'ficar verde'" — verdadeiro no sentido de *critério julgado*,
  mas o relatório não registra as 6 formas (×2 passagens) que **deixaram de ser recusadas**.
* O teste novo (`t_aut4_costura_probe.py:288-297`) **afirma** o comportamento novo, então a mudança foi
  deliberada — o que falta é só o registro no relatório.

**Menor conserto que fecha (documentação, 1 parágrafo):** acrescentar ao §2/§7 do
`docs/automacao/COR-AUT4-F4-entrega.md` a linha "comportamento NOVO no F4: artefato com
`evidencia_runtime_presente` truthy e `evidencia_runtime` ausente passa de FIXTURE/2 (pré-F4) para
runtime; não é perda de trava porque o mesmo artefato sem a chave interna já confirmava no código
anterior". Nada a mudar em `coletor.py`.

## 8. Item 8 — falsos OK no relatório — **nenhum em hashes/contagens/exit codes** (só o ACHADO-1)

| declarado no relatório | medido por mim | veredito |
|---|---|---|
| `coletor.py` `dee03a8f…7ef3e5` | `dee03a8fd16d95730ede993a14747406a37ba44f8a7ea97a6a666995fb7ef3e5` | **OK** |
| `t_aut4_costura_probe.py` `57a02638…d8bffca` | `57a02638b12bb641c348e75440f841cafe2592d3d270d5c7c94d8e7dad8bffca` | **OK** |
| entrega `cd751c8b…014c36` | `cd751c8b20d4903abde488afd44f3970c0be4b58b72fdbf88b097745ab014c36` | **OK** |
| `cp_f4_sem_defeito` == repo | `dee03a8f…` (medido na cópia do autor) | **OK** |
| `cp_f4_com_defeito` `1875fef1…` | `1875fef1708ee149f1a0e63ff505f5955c00ef373cb40d52ec1c90d0e9bdb8a9` | **OK** |
| suite 9 testes / contra-prova 16 | `VERDE (exit 0) — 9` / `16 teste(s)` | **OK** |
| números dos 5 consumidores | idênticos (§4) | **OK** |
| "nada commitado/staged" | `git status --short <2 arquivos>` reproduz `??` nas duas linhas; `git diff --cached --name-only` vazio | **OK** |
| linhas citadas no `coletor.py` (51, 70-71, 477, 502-505, 517, 484, 579/584) | conferidas uma a uma no arquivo | **OK** |
| bloco novo "linhas 263-330" | bloco real = 263-329 (330 é linha vazia) | OK (off-by-one irrelevante) |
| "não foi preciso tocar `AUT-4-estado.json`" | `AUT-4-estado.json` = `2d417e86…` — **hash idêntico ao que a revisão F3R mediu** (`2d417e86…`); `t_aut4_estado_docs` passa; a lista declarada de 9 testes/16 iscas casa com o disco | **OK** |
| §3.1 "RED no repo, antes do conserto" | estado histórico de arquivo **untracked** (sem registro em VCS) → não reconferível como fato passado | **INDETERMINADO como fato histórico**; a substância (RED reproduzível) **OK** por reversão em cópia (§5) |
| §2 tabela / §7 ("nenhuma trava enfraquecida") | matriz de 660 passagens | **ACHADO-1** (§7) |

## 9. Fragilidades da própria prova (declaradas)

1. **O pré-conserto não existe no repo** (arquivo untracked, sem histórico). Minha "reversão" é
   reconstrução a partir do trecho citado no §1 do relatório; ela coincide, exceto por um comentário, com
   a cópia do próprio autor — duas reconstruções independentes do mesmo comportamento, mas **não** os
   bytes originais.
2. A matriz usa **um** conjunto de `alvos` fixo. Outro conjunto move o desfecho entre `CONFIRMADA` e
   `INCOMPLETO` — mas a decisão fixture/runtime ocorre **antes** da consolidação e não depende de alvos;
   a classificação "endureceu/afrouxou" foi feita por `status`+`exit`, simetricamente nos dois lados.
3. A não-regressão dentro das **cópias** é inconclusiva (faltam fontes de mods nelas): a conclusão do
   item 4 se sustenta nas rodadas **no repo** + no `grep` + na matriz, não nas cópias.
4. `carregar_saida_probe()` devolve um dict que **não é serializável em JSON**
   (`TypeError: Object of type _MarcaMapeado is not JSON serializable`), por causa do marcador. Nenhum
   caminho vivo faz isso (`main()` serializa só o resultado do `consolidar_probe`, que não carrega a
   marca; `executar_rodada` só lê a saída por `.get`). Fica como nota para consumidor futuro.
5. Se alguém **remover** a chave do marcador de um dict já mapeado, o artefato legítimo volta a
   `FIXTURE/2` (fail-closed, não fail-open) — medido (`C10`). Não há caminho vivo que faça isso.
6. Limite permanente já julgado pela F3R §5: um artefato que simplesmente **omita** as duas chaves
   confirma como runtime (é o caminho do probe C# real, que não emite `evidencia_runtime` — `grep` = 0 no
   `.cs`). A trava é contra **formas DECLARADAS** de non-runtime, não contra artefato fabricado que
   imite o probe.

## 10. sha256 do que eu li

```
dee03a8fd16d95730ede993a14747406a37ba44f8a7ea97a6a666995fb7ef3e5  tools/automacao/runtime/coletor.py
57a02638b12bb641c348e75440f841cafe2592d3d270d5c7c94d8e7dad8bffca  tools/automacao/runtime/testes/t_aut4_costura_probe.py
cd751c8b20d4903abde488afd44f3970c0be4b58b72fdbf88b097745ab014c36  docs/automacao/COR-AUT4-F4-entrega.md
fc27798e94a17137e1081b5ff9d88d28ac2693cdd81d986cf60bac21e225157a  docs/automacao/COR-AUT4-F3R-revisao.md
2d417e861d152cf6cd508413a7eca54ff3b0a4e3b462f1f908f7a6bf417aeda2  docs/automacao/AUT-4-estado.json
d7604b2306df7dfde417702671cb13142eb2eec63ec78d0bb470f1153fc6366a  docs/automacao/AUT-4-preparacao.md
53db56e97c5e461790f348156d89313c8aa760dd756fe0db63d3e852f55259f1  .../testes/contra-prova/cp_aut5_isca_evidencia_runtime_forma_errada_ok.py
9b8893ef55d5d79f8ceb6332bacd4f3186eaba22f14c31a0231bdebcd6de7051  .../fixtures/probe-saida-exemplo.entrada.json
94e62e57a1be1be2467833b5687f78f60bb2933be0dd327fe31654a50b3a5523  MINHA copia com o conserto revertido (fora do repo)
dee03a8fd16d95730ede993a14747406a37ba44f8a7ea97a6a666995fb7ef3e5  minha copia espelho "sem defeito" (== repo)
```

Provas em `C:/Users/Pichau/AppData/Local/hermes/cache/scratch/f4r_rev/`: `gerar_artefatos.py`
(`3d715311…`), `roda_sondas.py` (`d7c1dcba…`), `idem_matriz.py` (`f508679c…`),
`bordas_sentinela.py` (`77d96f49…`), `art/` (artefatos-sonda), `saidas/` (JSON literal de cada CLI),
`com/` e `sem/` (cópias fora do repo).

## 11. O que NÃO foi exercitado (nunca OK)

Rodada runtime real em jogo (PNG pela API do Unity, `Tooltip.ShowTooltip`, owners Harmony vivos,
rollback em jogo) **não** foi exercitada — esta revisão é offline (bytes + execução Python), como manda o
card. Nada disto virou OK aqui e nada disto substitui o aceite humano.
