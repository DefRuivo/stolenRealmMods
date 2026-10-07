# AUT-3F2R — revisão independente e limitada do A1 (t_eea5b009)

Revisor ≠ autor. Escopo desta rodada: **só** refutar/provar o achado **A1** (guarda de repo
git FAIL-CLOSED) da `AUT-3F2` (`t_2eb1c5db`). Sem rodada FULL, sem build, sem jogo, sem
deploy/commit/publicação, **sem mutar o Kanban**. Nenhum arquivo de produto/jogo/save tocado;
único arquivo novo no repo é **este**.

- Estados revisados: `HEAD f526fe9b71f5` · `git status --porcelain` = 82 (antes e depois).
- Método: leitura do código + **controles independentes com CLI real**, em scratch Hermes
  (`%LOCALAPPDATA%\hermes\cache\scratch\aut3f2r\`), sem reaproveitar os mocks do autor.

## Arquivos revisados (sha256 do disco)

```
bancada_aut3.py         8d0d85c1990fe23c76ab17b0353f3a5da19dfb7c51cff78f1980858a891cd6d7
aut3_lib.py             04f37b8e285ad7d429d0d01cd846523323ca0a403ce64203890e3c0538d6dc1a
testes/t_aut3f2_achados.py  e19ee61f8eaec575876046eedc61649795ae1d8d64b4078679e582617a741d7d
docs/automacao/AUT-3F2-relatorio.md  abbd1c23a8e96269c124bdcfc80376bd1aa3efec82925ac47c1514cc0477e569
contra_provas.py        01e62e200ad2e46a2280beba776e5c1f2a2727a712ac8c0c183779bc6a5b57c6  (= relatório; inalterado)
```

Os 3 hashes de código **batem** com a tabela da AUT-3F2 — o que revisei é o que foi entregue.

## Veredito A1 — **OK (com prova)**

A correção é real e não-vacua. `_git_lista_z` (`bancada_aut3.py` l.180-196) **levanta
`GuardaGitIndisponivel`** em `timeout`, `erro_lancamento` e `exit != 0`; `main()` (l.519-585)
captura o erro, **não builda** (`fases_puladas += {builds, guarda_repo_indisponivel}`),
grava `guarda_repo.intacto = None` e sai não-zero **sem traceback**.

Prova do fail-open que o guarda impede (1 linha, sem tocar no produto):
`comparar_snapshot({}, {})["intacto"] = True` — o caminho antigo (`[]` ⇒ `{}` ⇒ intacto) é
realmente VERDE-cego; só o `raise` o corta.

### Controles independentes (CLI real; script `ctrl_aut3f2r.py`, evidência `ev_ctrl.txt`)

| # | cenário (real, salvo 3b) | resultado literal |
|---|---|---|
| C1 | `--repo` **sem `.git`** (CLI real) | `exit=1`, `"repo_intacto": null`, `guarda_repo.intacto=None`, `erro=[exit 128 (fatal: not a git repository ...)]`, `builds_executados=0`, fases `['builds','guarda_repo_indisponivel']`, veredito `REPROVADO`, sem `Traceback` |
| C2 | repo git **válido** (init+commit) | snapshot lê `a.txt`; arquivo novo ⇒ `criados=['b.txt']`, `intacto=False`; repo válido **vazio** ⇒ `[]`/`{}` **sem** levantar; CLI no repo válido ⇒ `repo_intacto=True`, `erro=[]` (**não é "sempre null"**) |
| C3a | git **ausente** real (PATH sem git, **sem mock**) | `_git_lista_z` levanta (`FileNotFoundError: [WinError 2]`); CLI real ⇒ `exit=1`, `"repo_intacto": null`, sem `Traceback` |
| C3b | git **timeout** real (`timeout=0.001s` no git REAL) | `_git_lista_z` levanta `git ls-files -z: timeout`; `avalia(timeout) == NAO_EXERCITADO` |

C3b é o único com injeção, e é **inevitável**: injeta-se só o *valor* de timeout; o `git`
executado é o real, e o `TimeoutExpired` é real. Os demais são 100% reais.
**22/22 checks PASSARAM** (`TOTAL 22 | FALHAS 0`).

## Regressão e testes do autor (reexecutados, não confiados no relatório)

| execução | resultado |
|---|---|
| `t_aut3f2_achados.py` (novo) | `total: 64 | falhas: 0`, rc=0 |
| `t_aut3_lib` \+`_isolamento` +`_segredos` +`_runner` (regressão) | 25+46+12+7 = **90**, 0 falhas (igual ao pai) |
| `tools/testes/roda_testes.py --puros` | rc=0, `{'PASSOU': 85}`, 0 falhas (full: 86, rc=0) |

## Limites / o que esta revisão NÃO confirma

- **Não houve rodada FULL** (`--jogo`, 6 builds) — está fora por instrução. O A1 foi exercido
  nas fases offline/sem-build; a correção também vale nos builds, mas isso **não** foi
  reexecutado aqui.
- **Runtime de jogo e publicação**: `NAO_EXERCITADO` (fora desta bancada) — não avaliados.
- O `main()` grava `docs/automacao/AUT-3-resultado.json`/`AUT-3-resumo.md` no `--repo`; por
  isso os controles rodaram sobre repos **de scratch**, nunca sobre o repo real (que só recebe
  este `.md`).
- A2/A3 (sanitização/scratch) foram vistos verdes nos testes, mas **não** são o foco desta
  revisão e não foram refutados item a item.
- Cache vazio: a Temp local do Windows tem **0** dirs `t-aut3*`.

## Ausência de efeito colateral

`HEAD` e `porcelain` (82) inalterados; perfil BepInEx só lido por hash; nenhum `git add`,
build, jogo, commit ou deploy. Evidências em
`%LOCALAPPDATA%\hermes\cache\scratch\aut3f2r\`: `ev_ctrl.txt`, `ev_t_aut3f2.txt`,
`ev_regressao90.txt`, `ev_roda_testes.json`, `ctrl_aut3f2r.py`.

> AUT-3F2R não publica, não aprova deployment e não substitui o aceite humano do DoD.
