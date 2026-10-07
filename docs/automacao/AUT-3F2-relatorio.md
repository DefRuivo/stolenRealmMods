# AUT-3F2 — conserto dos achados da AUT-3FR (t_2eb1c5db)

Fecha os 3 achados da `AUT-3FR-revisao.md`. Escopo: `tools/automacao/offline/**`, seus
testes e este relatório — **sem** alterar pareceres/relatórios anteriores (`AUT-3-*`,
`AUT-3F-*`, `AUT-3FR-*` intactos). HEAD `f526fe9b71f5` @ `ci-validate-test`. Nenhum
deploy, install, jogo, save, commit/push ou publicação. **Kanban NÃO mutado.**
Método: TDD (RED antes / GREEN depois) + CLI real em execução isolada.

> **Prioridade (instrução do dono, ao vivo):** entregar primeiro o **A1** (falso verde do
> git), que é o aceite direto da bancada. A2/A3 são secundários. Por isso **NÃO houve nova
> rodada FULL** (`--jogo`, 6 builds) nesta tarefa; o FULL segue como o último da AUT-3F.

## A1 (médio) — guarda de repo FAIL-CLOSED · ENTREGUE e VALIDADO

**Antes:** `_git_lista_z` ignorava `exit_code`/`stderr`/`timeout` e devolvia `[]`. Num dir
sem `.git` (exit 128) ou com o git ausente, `snapshot_repo = {}` ⇒ `comparar_snapshot({},{})`
= `intacto=True`. O guarda afirmava "intacto" **sem ter lido nada** — falso verde.

**Agora:** `_git_lista_z` **levanta `GuardaGitIndisponivel`** quando a listagem não pode ser
feita (timeout / `erro_lancamento` / `exit != 0`). `main()`:
- captura a falha em `repo_antes`/`repo_depois` e registra em `guarda_repo.erro`;
- **não builda** com guarda cega (`fases_puladas += {builds, guarda_repo_indisponivel}`);
- `repo_intacto=None` (INDETERMINADO — nunca `True`) e injeta `NAO_EXERCITADO` no veredito;
- exit **não-zero** e **sem traceback** (a exceção tipada é tratada).
Repo git **válido e vazio** (exit 0, stdout vazio) **não** é erro ⇒ `[]` / `{}`.

**Prova (CLI real, dir sem `.git`):**
```
python tools/automacao/offline/bancada_aut3.py --repo <dir-sem-git> --sem-build --sem-suite \
    --sem-contra-provas --sem-sandbox --jogo
exit=1  veredito=REPROVADO  "repo_intacto": null
guarda_repo.intacto=None  arquivos=None
guarda_repo.erro=['antes: git ls-files -z: exit 128 (fatal: not a git repository ...)',
                  'depois: git ls-files -z: exit 128 (...)', ]
```
Antes da correção a MESMA chamada imprimia `"repo_intacto": true` (capturado no RED).

## A2 (baixo) — sanitização · IMPLEMENTADO (secundário)

`sanitiza` agora cobre, além dos prefixos conhecidos, **explicitamente**: o **bloco PEM
inteiro** (cabeçalho + corpo base64 + rodapé, e o mesmo bloco **truncado** na captura) e
**atribuição genérica** (`password`/`secret`/`token`/`api_key`/`client_secret`/…) com valor
entre aspas ou sem aspas, preservando rótulo + separador. `_detalhe` **sanitiza ANTES de
truncar** (senão o corte deixaria fragmento). Não há promessa de pegar segredo arbitrário —
a lista é explícita e revisável. Credenciais 100% fictícias nos testes.

## A3 (baixo) — scratch dos testes · IMPLEMENTADO (secundário)

Novo `aut3_lib.area_trabalho()`: `$BH_AGENT_WORKSPACE` → `$TMPDIR` →
`<LOCALAPPDATA>/hermes/cache/scratch` → `gettempdir()` (último recurso); exporta
`TMP/TEMP/TMPDIR` para os subprocessos. Os 5 `t_aut3*.py` usam
`TemporaryDirectory(..., dir=aut3_lib.area_trabalho())`. Verificado: **0 dirs** `t-aut3*`
na Temp local do Windows.

## TDD — RED antes / GREEN depois

| teste | RED (contra o código antigo) | GREEN |
|---|---|---|
| `testes/t_aut3f2_achados.py` (novo) | **57 checagens · 30 falhas** (A1/A2/A3), incl. `repo_intacto: true` | **64 · 0 falhas** exit 0 |
| `t_aut3_lib.py` (A3) | — | **25 · 0** exit 0 |
| `t_aut3_isolamento.py` (A3) | — | **46 · 0** exit 0 |
| `t_aut3_segredos.py` (A3) | — | **12 · 0** exit 0 |
| `t_aut3_runner.py` (A3) | — | **7 · 0** exit 0 |

Assertions A1 cobertas: dir não-repo → levanta; git ausente (comando inexistente real +
`run_cmd` simulado) → levanta; **CLI real** sem `.git` e com git ausente → exit≠0,
`repo_intacto=null`, sem `Traceback`; falha na leitura **depois** → não vira intacto/verde;
repo **válido vazio** → `[]`/`{}`; repo válido com arquivo novo → detecta criado, intacto False.

## Hashes (sha256) e arquivos tocados

```
tools/automacao/offline/aut3_lib.py                 04f37b8e285ad7d429d0d01cd846523323ca0a403ce64203890e3c0538d6dc1a
tools/automacao/offline/bancada_aut3.py             8d0d85c1990fe23c76ab17b0353f3a5da19dfb7c51cff78f1980858a891cd6d7
tools/automacao/offline/contra_provas.py            01e62e200ad2e46a2280beba776e5c1f2a2727a712ac8c0c183779bc6a5b57c6  (inalterado)
tools/automacao/offline/testes/t_aut3f2_achados.py  e19ee61f8eaec575876046eedc61649795ae1d8d64b4078679e582617a741d7d  (novo)
tools/automacao/offline/testes/t_aut3_lib.py        25df1bb71aa2e570e000cd1d29d69bb9a8085981c22d854c8e2023797ea53621
tools/automacao/offline/testes/t_aut3_isolamento.py 3b6b8372f485f968fd83897771d02b3f59b694925453eb0e822bd9e8e9b68a89
tools/automacao/offline/testes/t_aut3_segredos.py   f3eb39963c1b7fb0aed2665c623e1814185c4dfcef43f019dabcf4a0d652941f
tools/automacao/offline/testes/t_aut3_runner.py     eea0a022d8d19a78128c17f9dbb765dd65c82e8712ca6e07669dcd1993c77cef
docs/automacao/AUT-3F2-relatorio.md                 (este relatório — novo)
```
Evidências em `C:/Users/Pichau/AppData/Local/hermes/cache/scratch/aut3f2/`
(`red_achados.txt`, `green_achados.txt`, `green_t_aut3_*.txt`, `snap_antes.json`,
`snap_depois.json`).

## Ausência de efeito colateral (repo/perfil REAL)

Snapshot independente (git ls-files + walk, sem usar o produto AUT-3), antes/depois:

| leitura | antes | depois |
|---|---|---|
| repo (arquivos hasheados) | 462 | 463 |
| criados | — | só `testes/t_aut3f2_achados.py` (autorizado) |
| alterados | — | só os 6 arquivos AUT-3F2 acima (todos autorizados) |
| removidos | — | nenhum |
| perfil BepInEx (plugins+config) | 28 | 28 · **intacto** |
| Temp local do Windows (`t-aut3*`) | — | **0** |
| `git status --porcelain` / HEAD | 82 · `f526fe9b71f5` | 82 · `f526fe9b71f5` |

## Lacunas / não coberto (não é OK)

- **Rodada FULL (`--jogo`, 6 builds) NÃO executada nesta tarefa** (instrução do dono: não
  ampliar escopo). O A1 foi validado pelo CLI real nas fases offline/sem-build; a correção
  também roda nos builds quando o FULL for reexecutado pelo pai/revisor.
- **Runtime de jogo e publicação** seguem fora (`NAO_EXERCITADO`), como na AUT-3F.
- Correção aplicada no A2 durante o GREEN: o helper `_redigir_assign_quoted` usava
  `group(5)`, inexistente (as aspas são o mesmo grupo 3) — o próprio teste pegou o
  `IndexError`; corrigido para `group(3)`.
- **Não marcar done** — o pai faz a revisão independente. AUT-3F2 não substitui aceite
  humano nem publicação do DoD.
