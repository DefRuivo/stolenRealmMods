# AUT-3R3 — terceira revisão independente da bancada AUT-3 (t_70ef8571)

Revisor **não-autor** (nenhuma linha desta bancada foi escrita por mim). Escopo: o estado
acumulado da AUT-3 — `tools/automacao/offline/**` + suíte + `docs/automacao/AUT-3-*` — depois de
AUT-3F, AUT-3F2 e das revisões AUT-3R/AUT-3R2. HEAD `f526fe9` @ `ci-validate-test`,
`git status --porcelain` = 82 (antes e depois desta rodada).

Nada de deploy, jogo, save, install, probe, commit, push ou publicação. Kanban: esta rodada **não**
move a tarefa AUT-3 (`t_49075ea4`, em review por outra frente) — só registra o veredito. O perfil
do dono foi apenas lido por hash. O produto/runner não foi editado; o único arquivo novo no repo é
**este** `.md`.

Método: execução real em **cópias isoladas** (nunca no repo real) + leitura fria do código e das
alegações, tentando refutá-las por controles negativos próprios (não reaproveitei os controles do
autor nem os da AUT-3R2). Evidências em
`C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_70ef8571\` (`reviewed-hashes.json`,
`full-result.json`, `full-summary.md`, `controls.json`, `controls2.json`, `controls3.json`,
`before.json`, `after.json`, `external-diff.json`, `executions.json`, scripts `review.py`,
`controls*.py`).

## Hashes do que foi revisado (sha256 do disco)

Todos **iguais** aos declarados na AUT-3F2/AUT-3R2 — o que revisei é o que foi entregue:

```
aut3_lib.py                 04f37b8e285ad7d429d0d01cd846523323ca0a403ce64203890e3c0538d6dc1a
bancada_aut3.py             8d0d85c1990fe23c76ab17b0353f3a5da19dfb7c51cff78f1980858a891cd6d7
contra_provas.py            01e62e200ad2e46a2280beba776e5c1f2a2727a712ac8c0c183779bc6a5b57c6
testes/t_aut3_lib.py        25df1bb71aa2e570e000cd1d29d69bb9a8085981c22d854c8e2023797ea53621
testes/t_aut3_isolamento.py 3b6b8372f485f968fd83897771d02b3f59b694925453eb0e822bd9e8e9b68a89
testes/t_aut3_segredos.py   f3eb39963c1b7fb0aed2665c623e1814185c4dfcef43f019dabcf4a0d652941f
testes/t_aut3_runner.py     eea0a022d8d19a78128c17f9dbb765dd65c82e8712ca6e07669dcd1993c77cef
testes/t_aut3f2_achados.py  e19ee61f8eaec575876046eedc61649795ae1d8d64b4078679e582617a741d7d
AUT-2-matriz.json           8503010272d7…
AUT-3-resultado.json        9c1aa58244ed…   (inalterado por mim, antes e depois)
AUT-3-resumo.md             89f0fe669672…
DLLs Release/perfil         06dae5aa7b5e · 2c07f5e959af · 5a3c001ad424 · 270f311b0f7b · 99c156799380 · 454587a031a3
```

Os 8 hashes de código e de teste continuam byte-idênticos no disco **depois** de toda a minha
rodada (reconferido): o veredito vale para exatamente esta árvore.

## Veredito por critério do corpo da tarefa

| # | critério | veredito | prova |
|---|---|---|---|
| 1 | comando único roda o aplicável por mod/dependências | **OK** | `bancada_aut3.py --repo <cópia> --ancora <repo real> --jogo` → exit 0, **VERDE**, `fases_puladas=[]`, 6 builds · 11 conferidores · 3 suítes · 5 contra-provas |
| 2 | builds sem deploy, ≤6, sem tocar no perfil | **OK** | 6/6 `-c Release -p:DeployToBepInEx=false`, `PathMap` cópia→repo real, env/`props` MSBuild isolando USERPROFILE/APPDATA/LOCALAPPDATA; `preflight_deploy` OK (7 alvos), `bloqueou=false` |
| 3 | fonte→DLL = Release = perfil por hash | **OK** | os 6 `fonte_dll_provada=true`; sha da cópia, do `bin/Release` e do **perfil do dono** idênticos por mod |
| 4 | suíte | **OK** | puros **85 PASSOU**; contra-prova do runner **49 PROVA_OK + 14 PASSOU**; jogo **1 PASSOU** — exit 0 nos três |
| 5 | conferidores (duplicatas, chaves, notas, versões, patches, segredos, pacotes, docs) | **OK** | 11/11 exit 0 (inclui `pacotes_preflight --so-conferir` e `audita_docs`) |
| 6 | docs curadas preservadas | **OK** | `check_notas_redundantes` escreve de fato (mtime do `RV-15-notas-redundantes.md` **mudou dentro do sandbox** da minha rodada, `1791240886`) e só ele escreve; em `--sem-sandbox` sai `NAO_EXERCITADO` **e o arquivo da cópia não foi tocado** (mtime idêntico antes/depois) |
| 7 | JSON + resumo com comandos, exit, tempos e hashes | **OK** | `estados_separados` = fonte · Release · perfil · pacote; `comando`, `exit_code`, `segundos`, `sha_*` por item (ver ressalva F1 sobre o artefato publicado) |
| 8 | distinguir puro/estrutura de runtime; `--jogo` não é prova de jogo | **OK** | `suite_jogo` só lê `lib/`; nenhum `Stolen Realm.exe` em execução e `LogOutput.log`/`Player.log` com mtime **anterior** à minha janela (nenhum boot modado) |
| 9 | erro de comando/build **não vira verde** | **OK (refutado 5×)** | tabela abaixo: build quebrado, opt-in removido, dir sem `.git`, segredo plantado, fases puladas/omitidas — todas não-VERDE |
| 10 | perfil intacto por hash + ambiente restaurado | **OK** | 46 arquivos (plugins+config+core) **idênticos** antes×depois; **0** de 51 arquivos do perfil com mtime dentro da janela; `guarda_perfil.intacto=true` |
| 11 | cobertura alinhada à matriz AUT-2 | **OK com ressalva de escopo (F4)** | 20/20 critérios com estado: `OK_OFFLINE 8 · PARCIAL 0 · NAO_EXERCITADO 12 · REPROVADO 0`; matriz sha `8503010272d7` |
| 12 | cenários ausentes **não** recebem aprovação | **OK** | os 12 de runtime saem `NAO_EXERCITADO` com motivo; fases omitidas entram em `nao_exercitados` e derrubam o veredito (C1/C6) |

### Controles negativos independentes (cópias isoladas; CLI real)

| id | defeito/omissão plantada | resultado literal |
|---|---|---|
| **C2** | erro de sintaxe em `BetterFont/Plugin.cs` (cópia) | exit **1**, `REPROVADO`, `build_BetterFont=REPROVOU`, `fonte_dll_provada=false`; os outros 5 builds OK; perfil intacto |
| **C3** | `Condition` de opt-in removida de `BetterFont.csproj` (cópia) | `preflight_deploy=REPROVOU`, **`builds_executados=0`**, `fases=['optin_bloqueou']`, exit 1 `REPROVADO` — a guarda bloqueia **antes** de qualquer build tocar `$USERPROFILE`; perfil intacto |
| **C4** | repo de cópia **sem `.git`** | exit 1, `REPROVADO`, `repo_intacto=null`, `guarda_repo.erro=['antes: … exit 128 …','depois: …']`, builds 0, **sem traceback** |
| **C5** | credencial **falsa** (`tss_`+32) em arquivo rastreado da cópia | `check_segredos=REPROVOU` com `<REDACTED: 36 chars>` no detalhe; token/prefixo **ausentes** de stdout, stderr, resumo e JSON (`token_no_json=false`); exit 1 `REPROVADO` |
| **C6** | builds feitos, `--sem-suite --sem-contra-provas` | exit **2**, `INCOMPLETO`, `fases_puladas=['suite','contra_provas']`, `fase:suite`/`fase:contra_provas` em `nao_exercitados`, 6/6 builds OK, perfil intacto → **fase omitida nunca é verde** |
| **C1** | `--sem-build --sem-suite` | exit **1**, `REPROVADO` (ver F2: sem `bin/` no sandbox, `pacotes_preflight` reprova) — **não** VERDE em nenhum caso |
| **C7** | unidade, CLI real | comando inexistente ⇒ `erro_lancamento` ⇒ `NAO_EXERCITADO`; `git` real com `timeout=0.001s` ⇒ `timeout` ⇒ `NAO_EXERCITADO`; `git` real OK ⇒ `OK`; `veredito([OK,NAO_EXERCITADO])=INCOMPLETO`, `([OK,REPROVOU])=REPROVADO`, `([])=INCOMPLETO` |

Confirmação de reprodução: a minha rodada FULL produziu veredito, builds, hashes por mod,
`estados_separados` e resumo de cobertura **iguais** ao `AUT-3-resultado.json`/`AUT-3-resumo.md`
entregues; as únicas diferenças de campo são as voláteis (`gerado_em`, paths, tempos) — ver F1.

## Achados (não bloqueiam; nenhum é falso verde)

- **F1 · baixo · procedência do artefato** — confirmado de forma independente: o
  `AUT-3-resultado.json` do repo (sha `9c1aa58244ed`, `gerado_em 15:47`) é **anterior à AUT-3F/F2** e
  não tem `isolamento`, `preflight_deploy`, `fases_puladas` nem `guarda_repo.erro`/`criados/
  alterados`; o `AUT-3-resumo.md` também é anterior (não traz a linha "fases puladas"). A saída do
  código **atual** é a minha (campos presentes, mesmo veredito e mesmos sha por mod). Sugestão já
  registrada na AUT-3R2: gravar no JSON o hash da própria bancada que o gerou. Não regenerei os
  arquivos do repo de propósito (seria reescrever artefato do autor nesta rodada).
- **F2 · baixo · rótulo com `--sem-build`** — sem build não existe `bin/Release` no sandbox interno,
  então `pacotes_preflight` reprova e o rótulo sai `REPROVADO` em vez de `INCOMPLETO` (C1). Em
  `C6` (builds feitos, suíte/contra-provas omitidas) o rótulo correto aparece: `INCOMPLETO`.
  Nenhum dos dois é verde.
- **F3 · informativo · `zip != Release` em M4/M6** — confirmado: a evidência de pacote escolhe o
  **último** zip (ordem lexicográfica) do `dist/` cujo nome contém o mod
  (`gumatos-BetterTooltips-0.1.3.zip` `80bba4543d2a`, RSTV `c2ce4862c2fd`), que é a versão **já
  publicada**; a divergência em relação ao Release de hoje é declarada na própria evidência e não
  rebaixa o estado. Não é falso verde, mas ninguém deve ler "zip" como "pacote == fonte atual".
- **F4 · ressalva de escopo na cobertura** — M2 ("estilo preservado"), M4 ("invariantes") e M6
  ("janela read-only") têm componente runtime/visual fora do AUT-3; o `OK_OFFLINE` vale só para a
  parte offline, e o próprio item carrega o motivo.
- **F5 · hotspot (repetido)** — durante a minha janela, **outras frentes** escreveram na árvore:
  `tools/automacao/ciclo/{decisao.py,test_decisao.py}`, `tools/automacao/cenarios/{rstv.py,
  test_rstv.py,tooltips_shrines.py,test_tooltips_shrines.py,rstv-positivo.entrada.json,
  shrines-controle-negativo.json}`, `docs/automacao/{CIC-3-entrega,CIC-4-entrega,CIC-5R-revisao,
  AUT-4R2-revisao}.md` (reconferência final do snapshot inicial: 11 arquivos; `external-diff.json`).
  Nenhum desses é escrito pela bancada — ela só grava `docs/automacao/AUT-3-resultado.json`/
  `AUT-3-resumo.md` **dentro do `--repo`, sempre uma cópia** — e os arquivos da AUT-3
  (`aut3_lib.py`, `bancada_aut3.py`, `contra_provas.py`, testes) permaneceram byte-idênticos do
  começo ao fim. `hotspot: tools/automacao/` — várias frentes (CIC-*/AUT-4R*) aterrissando na mesma
  árvore ao mesmo tempo.

## Lacunas — o que esta revisão NÃO confirma (não canonizar)

- **Runtime de jogo**: `T-RSTV21/25B/26`, `S-RV-26…34`, `BUG34` seguem `NAO_EXERCITADO` (exigem
  jogo e/ou o dono; AUT-4/5/6). `T-RSTV25B` continua **INDETERMINADO** (LogOutput do próximo boot).
- **Publicação online / local↔online**: fora do AUT-3 — não verificada.
- **Aceite humano e DoD**: não avaliados; verde offline ≠ runtime ≠ DoD. A bancada **não** substitui
  o aceite do dono nem a publicação na Thunderstore.
- As medições valem para o HEAD `f526fe9` e para exatamente os hashes acima; mudança de fonte
  invalida esta rodada (foi reconferido que a árvore não mudou durante a revisão).

> AUT-3R3 não publica, não aprova deployment, não instala, não abre o jogo e não substitui o aceite
> humano do DoD.
