# KIT-10F — revisao independente (cartao t_48b78ecb, run666)

**Veredito: APROVADO.** Revisor independente, perfil `default`, run666 — instancia nova, distinta do
implementador run665 e do revisor de origem run663 (KIT-10R). Lente da rodada 1 (Artifact),
reforcada por execucao propria: o diff foi lido a frio ANTES do resumo do implementador e todas as
afirmacoes do handoff foram reproduzidas em sandbox proprio do revisor.

- Produto revisado: `tools/automacao/kit10/kit10_cenarios.py`
  SHA256 `899e47595d2e86ed2dda1e5bc6c425c3a0f9a70db3974f899480fde64620507c`
  (baseline reprovado `8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092`).
- Baseline antigo obtido de fonte INDEPENDENTE do implementador:
  `scratch/kit/KIT-10R-run663/sandbox/tools/automacao/kit10/kit10_cenarios.py` (sandbox do proprio
  revisor de origem), conferido por SHA.
- Nenhum arquivo de implementacao foi editado por este revisor.

## 1. Suites IMUTAVEIS do revisor (copiadas da origem, nunca editadas)

SHA conferido apos a copia: `test_review_kit10.py` `e7eddb6f3662...` e `test_wrapper_metadata.py`
`2d3a40b5f609...` (iguais aos do cartao). Rodadas em sandbox proprio (`scratch/rev666/antigo` e
`.../novo`), com o produto trocado apenas no ramo "antigo".

| suite | bytes ANTIGOS | codigo CORRIGIDO |
|---|---|---|
| `test_review_kit10.py` | `tests=45 failures=10 errors=0 skipped=0`, exit **1** | `tests=45 failures=0`, exit **0** |
| `test_wrapper_metadata.py` | `Ran 4 ... FAILED (failures=4)`, exit **1** | `Ran 4 ... OK`, exit **0** |

Discriminacao caso a caso (leitura do arquivo de resultado, nao da mensagem): nos bytes antigos os
falsos OK aparecem exatamente como o KIT-10R descreveu e no corrigido viram defeito —

| caso | antigo | corrigido |
|---|---|---|
| `nan_A_fonte_bonus` | OK/prova=True | **REPROVADO**/False |
| `nan_A_dano_observado` | OK/True | **REPROVADO**/False |
| `nan_A_contrib_observada` | OK/True | **REPROVADO**/False |
| `wrong_D_pipe_desc` (F10) | OK/True | **REPROVADO**/False |
| `wrong_D_mixed_unparsed` (F10) | OK/True | **REPROVADO**/False |
| `fixture_*` de envelope (F11) | 4× OK/True | 4× NAO_EXERCITADO/False |
| `wrong_fonte_bonus` / `wrong_dano_observado` / `wrong_contrib_observada` | REPROVADO | REPROVADO (preservado) |
| `positive_A..D` | OK/True | OK/True (preservado) |

O defeito REAL (Source injetado, dano errado, contrib errada) continua REPROVADO — a correcao fechou
a classe NaN/truncamento sem afrouxar as guardas de defeito.

## 2. Suites existentes preservadas (execucao propria)

| suite | comando | resultado |
|---|---|---|
| Autor | `python tools/automacao/kit10/test_kit10_cenarios.py` | 28/28 `PASSOU`, exit **0** |
| CIC-4 | `python tools/automacao/cenarios/test_tooltips_shrines.py` | `TOTAL rodaram=28 reprovaram=0`, exit **0** |
| RED guardas antigas | `python scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py` | `PASSOU 7 mutacoes`, exit **0** |

## 3. Guardas novas load-bearing (driver duravel, F13)

Copiei `prova_red_kit10f.py` (SHA `2379d0516373...`, identico ao do implementador) para um diretorio
proprio na MESMA profundidade (`scratch/kit/rev666-run666/`) para nao sobrescrever a evidencia dele.

`python scratch/kit/rev666-run666/prova_red_kit10f.py` -> exit **0**,
`controles=13 guardas=9`, SHA final do produto `899e4759...` (inalterado). Por guarda, o driver exige
`original=NAO-OK` e, com a neutralizacao SELETIVA, `neutralizado=OK/True`:

F8-NaN-fonte, F9-aura-inventada, F9-sem-gatilho-repetido, F9-itens-fracionario,
F9-instancias-default, F10-pipe-no-desc, F10-linha-nao-reconhecida, F12-base-errada,
F11-envelope-fixture — 9/9 escapam quando a guarda e neutralizada (nenhuma e decorativa).
O driver nunca escreve no produto: os mutantes nascem em arquivo temporario e sao apagados; a
conferencia final e SHA-antes == SHA-depois e ausencia de sobras `_red_mutante_*` (0 sobras).

O driver obsoleto `scratch/kit/KIT-10-run/prova_red_kit10.py` foi reexecutado por mim: exit **1**
(trechos `if fonte is None or abs(float(fonte))...` nao existem mais). Declaracao de superacao
CONFIRMADA e nao contada verde.

## 4. CLI (exit codes reais, resultado lido de arquivo)

- `kit10_cenarios.py --observacoes scratch/kit/KIT-10-run/fixture.json` -> exit **2**,
  `OK=0, REPROVADO=0, NAO_EXERCITADO=19`, prova runtime **0**.
- CLI envelope-fixture (`observacoes-envelope-fixture.json`, envelope `procedencia=fixture`,
  `rotulo_fixture=true`) -> exit **2**, `OK=0`, NAO_EXERCITADO 19 — o envelope nao perde a marca
  nem na CLI.

## 5. Travas e preservacao

- `check_segredos`, `check_padroes_segredo`, `check_dupes`, `audita_docs`: todos exit **0**
  ("nenhum padrao de credencial", "nenhuma inconsistencia").
- Sandboxes do implementador: `antigo/sandbox` e `novo/sandbox` com **1156** arquivos cada
  (contagem minha, igual ao `inventario.json`); **0** `.dll/.pdb/.pfx/.key`, **0** `.git`, **0**
  `BepInEx`.
- `git`: HEAD segue `d82894e` (o mesmo do inicio); `git reflog` sem commit novo; produto permanece
  **untracked** (`?? tools/automacao/kit10/`). Nenhum `git add`/`commit`/`push`.
- Nenhuma dependencia compartilhada editada: na janela do run665 (>= 2026-10-09 23:50) os unicos
  arquivos tocados fora de `scratch/` foram o proprio produto, seu `__pycache__` e os docs
  `KIT-10F-*`. CIC-4/AUT-7/`regras_*` apenas reusados (import por caminho).

## 6. Sondas adversariais proprias (coluna do revisor)

`scratch/kit/rev666-run666/sondas_rev666.py` (43 sondas) + `triagem_rev666.py` (13 casos), ambas
exit codes reais. Cobrem casos que NAO estao nas suites imutaveis nem no driver:

- F8: `inf`, `-inf`, `Infinity`, `nan`, bool, lista, dict, string nao numerica e string vazia em
  `fonte_bonus`/`receptor_bonus`/`maxhealth`/`dano_observado`/`contrib_observada` -> **todas**
  NAO-OK ou REPROVADO (nenhum falso OK). Booleano em `maxhealth` e lista/dict em medicao reprovam.
- F8 controle: string **numerica valida** (`"28"`) fecha OK — coerencia com o contrato antigo,
  nao e defeito.
- F9: itens `bool`/negativo/string-nao-numerica, `instancias` bool, aura com caixa errada, aura
  vazia, "so aura de atributo repetida" (sem gatilho repetido) -> **todos** NAO_EXERCITADO.
  Contagem fracionaria 2.5 -> NAO_EXERCITADO (nao trunca).
- F10: log so com texto neutro, linha sem `desc=`, `desc` vazio, `desc` fora de ultimo lugar,
  duas linhas (valida + declarada malformada) -> conforme a regra; `|` dentro do NOME entre aspas
  nao trunca (o parser devolve `a|b` inteiro) -> OK aceitavel.
- F11 (input do dono): `avaliar` NAO muta o envelope nem a observacao recebidos (comparacao por
  `deepcopy`) — requisito "sem modificar input do dono" satisfeito.
- F12: base errada, final errado, troca de personagem, medicao invalida (NaN/bool/lista), atributo
  trocado -> REPROVADO/NAO_EXERCITADO; positivo completo OK/True; display sem medicoes -> nunca OK.

### RESSALVA BOUNDED (nao bloqueia)

Uma **unica** lacuna residual, fora do vocabulario do achado F11 e inexistente nos dados reais: se o
ENVELOPE declarar `procedencia` com um valor fora do contrato (`"offline"`, `"execucao"`,
`"indeterminado"`, `"simulado"`, `"sintetico"`) e as observacoes internas declararem `runtime` com
cadeia completa (sessao + `fonte_sha`/`dll_sha` da identidade + evidencia em arquivo com hash
conferido), o criterio ainda fecha OK/True — a marca nao-fixture do envelope nao tange a lista.

Por que NAO bloqueia:

1. o vocabulario do contrato e exatamente `execucao`/`runtime`/`fixture`
   (`CICLO-VALIDACAO-escopo.md`; `estilo_atributos.PROCEDENCIAS`), e `AUT-7._procedencia` mapeia
   QUALQUER valor desconhecido para o default `execucao` — tratar `execucao` de envelope como taint
   puniria o valor default;
2. inspecao dos **295** envelopes-dict do repositorio: `None` 151, `fixture` 94, `runtime` 49,
   `FIXTURE` 1 (caixa alta, ja coberta por `.strip().lower()`) — **nenhum** com valor fora do
   contrato; a entrada canonica de `avaliar` e uma LISTA de observacoes;
3. o OK exige, na propria observacao, cadeia runtime completa com arquivo de evidencia hasheado —
   nao e um OK sem prova; e a classe exata do achado (marca de FIXTURE do envelope) esta fechada,
   inclusive `evidencia_runtime=false` e `sintetico=true`.

Fica registrado como divida de endurecimento para quem quiser a leitura mais conservadora
(tangir o envelope para qualquer `procedencia != "runtime"`), sem reabrir este cartao.

## 7. Limites (NAO_EXERCITADO)

Runtime real, jogo, save, perfil do dono, UI/UX/pixels, desempenho, build, preflight, deploy,
instalacao, publicacao, Bard/gameplay: NAO_EXERCITADO. Tudo o que foi executado aqui sao cadeias
OFFLINE explicitas, sem DLL. F4 (estilo historicamente variavel) permanece INDETERMINADO e o
BetterFont nao foi tocado (nenhum arquivo de mod aparece na janela do run665).

## 8. Checklist do revisor

- [x] `kanban_show` lido; implementer/reviewer por run identificados (665 != 666 != 663).
- [x] Diff lido a frio antes do resumo do implementador.
- [x] Criterio de aceite -> evidencia, item por item (suites imutaveis, autor/CIC-4/RED, guardas
      load-bearing, CLI, preservacao, travas, F13).
- [x] Suites imutaveis copiadas da origem com SHA conferido e nunca editadas.
- [x] Nenhum arquivo de implementacao editado pelo revisor.
