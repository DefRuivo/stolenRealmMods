# AUT-3R2 — revisão final independente da bancada AUT-3 (t_49075ea4)

Revisor **não-autor** (run 352, spawned do lane `review`). HEAD `f526fe9b71f5` @ `ci-validate-test`.
Escopo: o **estado acumulado** da bancada AUT-3 — `tools/automacao/offline/**`, sua suíte e o
artefato `docs/automacao/AUT-3-resultado.json`/`AUT-3-resumo.md` — depois dos consertos AUT-3F,
AUT-3F e AUT-3F2. Nada de deploy, jogo, save, install, commit, push ou publicação. Kanban: só a
transição de veredito desta rodada. Produto **não editado** por esta revisão (o único arquivo novo
é este `.md`); o perfil do dono só foi lido por hash.

Método: leitura fria do código **antes** do resumo do autor, seguida de **execução real em cópia
isolada** (nunca no repo real). Evidências em
`C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_49075ea4\`
(`review_evidence.json`, `full_result.json`, `full_summary.md`, `refutacao.json`,
`snapshot_before.json`, `snapshot_after.json`, `review_aut3.py`, `refuta_aut3.py`).

## Hashes do que foi revisado (sha256 do disco, iguais aos declarados na AUT-3F2)

```
aut3_lib.py                     04f37b8e285ad7d429d0d01cd846523323ca0a403ce64203890e3c0538d6dc1a
bancada_aut3.py                 8d0d85c1990fe23c76ab17b0353f3a5da19dfb7c51cff78f1980858a891cd6d7
contra_provas.py                01e62e200ad2e46a2280beba776e5c1f2a2727a712ac8c0c183779bc6a5b57c6
testes/t_aut3f2_achados.py      e19ee61f8eaec575876046eedc61649795ae1d8d64b4078679e582617a741d7d
testes/t_aut3_lib.py            25df1bb71aa2e570e000cd1d29d69bb9a8085981c22d854c8e2023797ea53621
testes/t_aut3_isolamento.py     3b6b8372f485f968fd83897771d02b3f59b694925453eb0e822bd9e8e9b68a89
testes/t_aut3_segredos.py       f3eb39963c1b7fb0aed2665c623e1814185c4dfcef43f019dabcf4a0d652941f
testes/t_aut3_runner.py         eea0a022d8d19a78128c17f9dbb765dd65c82e8712ca6e07669dcd1993c77cef
```

## Veredito por critério do corpo da tarefa

| # | critério | veredito | prova |
|---|---|---|---|
| 1 | comando único que roda o aplicável por mod | **OK** | `python tools/automacao/offline/bancada_aut3.py --jogo` numa cópia: exit 0, VERDE, 6 builds · 11 conferidores · 3 suítes · 5 contra-provas (`full_result.json`, sha256 `5be2b73cf177…`) |
| 2 | builds sem deploy, ≤6, sem tocar no perfil | **OK** | 6/6 `-c Release -p:DeployToBepInEx=false`; env + props isolando `USERPROFILE/APPDATA/LOCALAPPDATA` sob o scratch e `NUGET_PACKAGES` real; guarda de opt-in **antes** de buildar (`preflight_deploy`: estado OK, `bloqueou=false`) |
| 3 | suite | **OK** | `85 PASSOU` (puros) · `1 PASSOU` (jogo) · `49 PROVA_OK + 14 PASSOU` (prova de fogo) — exit 0 nos três |
| 4 | conferidores (duplicatas, chaves, notas, versões, patches, segredos, pacotes, docs) | **OK** | 11/11 exit 0, incluindo `pacotes_preflight` e `audita_docs` |
| 5 | docs reescritas preservadas | **OK** | só `check_notas_redundantes` escreve; roteado ao sandbox; `--sem-sandbox` ⇒ `NAO_EXERCITADO` (nunca verde) |
| 6 | JSON + resumo com comandos, exit, tempos e hashes | **OK** | `estados_separados` = fonte · Release · perfil · pacote (sha da DLL dentro do zip × Release); nada de conteúdo de config |
| 7 | distinguir puro/estrutura de comportamento runtime | **OK** | `--jogo` só lê `lib/` (não abre o jogo, não lê `LogOutput`); 12 critérios de runtime saem `NAO_EXERCITADO` com motivo |
| 8 | contra-provas em cópias isoladas (reprova o defeito, aprova depois) | **OK** | 5/5 `PROVA_OK` (defeito exit 1 → correção exit 0) no FULL que eu rodei |
| 9 | erro de comando/build **não pode virar verde** | **OK (refutado 3×)** | ver tabela abaixo: defeito de build ⇒ `REPROVADO`; fases puladas ⇒ `REPROVADO`; defeito estrutural ⇒ `REPROVADO` |
| 10 | perfil intacto por hash | **OK** | snapshot independente (walk + sha256, sem usar o produto): perfil BepInEx **51 arquivos, 0 criados / 0 removidos / 0 alterados** antes×depois de todas as rodadas; `guarda_perfil.intacto=true` (28 de plugins+config) |
| 11 | cobertura alinhada à matriz AUT-2 | **OK (com ressalva F4)** | 20/20 critérios com estado: `OK_OFFLINE 8 · PARCIAL 0 · NAO_EXERCITADO 12 · REPROVADO 0`, matriz sha `8503010272d7` |

### Refutação independente do critério 9 (o aceite central), CLI real, cópia isolada

| cenário | comando | resultado literal |
|---|---|---|
| fases puladas | `--sem-build --sem-suite --sem-contra-provas` | exit **1**, `veredito REPROVADO`, `fases_puladas=[builds, contra_provas, suite, suite_jogo]`, `qualquer_verde=false` |
| defeito de BUILD plantado (erro de sintaxe em `BetterFont/Plugin.cs`) | `--jogo` | exit **1**, `REPROVADO`, `build_BetterFont=REPROVOU`, cobertura `REPROVADO 1`, perfil intacto |
| defeito ESTRUTURAL plantado (chave duplicada em `LocalizePatch.cs`) | `--sem-suite --sem-contra-provas` | exit **1**, `REPROVADO`, `check_dupes=REPROVOU` (+`audita_docs`) |

Ou seja: **nenhum caminho testado transformou falha em verde**, e o perfil ficou intacto nas três.

## Correções das rodadas anteriores — reexecutadas, não confiadas ao relatório

- **AUT-3R (4 itens):** (1) isolamento `USERPROFILE/APPDATA` + props MSBuild — visto em
  `isolamento.env`/`isolamento.props` da minha rodada; (2) guarda de repo recursivo — agora
  `git ls-files -z --others --exclude-standard`, **502 arquivos** no meu FULL, dos quais
  **54 de `tools/automacao/` e 27 de `docs/automacao/`** (o furo antigo tinha **0** desses);
  (3) fases puladas não ficam verdes — refutação acima; (4) prefixo de segredo — `_detalhe`
  sanitiza **antes** de truncar; varredura do meu JSON: `hits_credencial=[]`, `<REDACTED>` 0,
  nenhum valor com forma de token.
- **AUT-3FR/A1 (guarda git FAIL-CLOSED):** `_git_lista_z` levanta `GuardaGitIndisponivel` em
  timeout/`erro_lancamento`/exit≠0; `main()` captura, **não builda** e grava `repo_intacto=None`
  (INDETERMINADO). Confirmado por leitura no código atual e pelos controles do AUT-3F2R (22/22).
- **AUT-3FR/A2/A3:** `sanitiza` cobre PEM inteiro (inclusive truncado) e atribuição genérica;
  `area_trabalho()` mantém os testes fora da Temp local do Windows — `0` dirs `t-aut3*` na Temp
  local após as minhas rodadas.

## Achados (não bloqueiam; nenhum é defeito de comportamento)

- **F1 · baixo · procedência do artefato em `docs/`.** O `AUT-3-resultado.json` do repo
  (sha `9c1aa582…`, `gerado_em 15:47`) foi produzido pelo código **anterior** à AUT-3F2 e não tem
  os campos acrescentados depois (`isolamento`, `preflight_deploy`, `guarda_repo.erro`,
  `fases_puladas`). Ele **não é reproduzível** pelos hashes atuais; a saída FULL do código atual é
  a que produzi em cópia (`5be2b73cf177…`, VERDE, mesmos sha por mod: `06dae5aa/2c07f5e9/5a3c001a/
  270f311b/99c15679/454587a0`). Não regenerei o arquivo do repo de propósito (reescreveria doc
  curado e o efeito colateral foi proibido nas rodadas anteriores). Correção sugerida, quando
  alguém tocar nisso: gravar no JSON o hash da própria bancada que o gerou.
- **F2 · baixo · rótulo quando `--sem-build`.** Sem build, o sandbox não tem `bin/Release`, então
  `pacotes_preflight` sai `REPROVOU` e o veredito é `REPROVADO` em vez de `INCOMPLETO`. **Não é
  verde em nenhum dos casos** (já registrado pela AUT-3FR); só o rótulo difere.
- **F3 · informativo · `zip != Release` em M4/M6.** `dist/gumatos-BetterTooltips-0.1.3.zip`
  (`80bba4543d2a`) e `dist/gumatos-RoguelikeSkillTreeVisualizer-0.3.2.zip` (`c2ce4862c2fd`) não
  batem com o Release do working tree — esperado: o zip é a versão **já publicada** (imutável) e o
  Release reflete a fonte de hoje. A bancada **declara** a divergência na própria evidência; fica
  registrado para ninguém ler M4/M6 como "pacote == fonte atual".
- **F4 · ressalva de escopo na cobertura.** Os critérios M2 ("estilo preservado"), M4
  ("invariantes") e M6 ("janela read-only") têm componentes **runtime/visual** que o AUT-3 não
  cobre; o rótulo `OK_OFFLINE` vale para a parte offline (build/hash/zip) e o próprio registro traz
  `motivo: publicacao online e validacao em jogo seguem FORA do AUT-3`. Não é falso verde, mas
  quem ler a matriz deve ler o motivo junto.
- **F5 · higiene/hotspot.** Durante a minha janela, **outros agentes** alteraram
  `tools/automacao/cenarios/*`, `tools/automacao/ciclo/*`, `docs/automacao/CIC-5R-revisao.md` e
  criaram `docs/automacao/AUT-4R2-revisao.md` — nenhum deles por causa desta rodada (o AUT-3 só
  escreve na cópia). `hotspot: tools/automacao/` — várias frentes aterrissando na mesma árvore;
  .pyc de `tools/**/__pycache__/` apareceram no repo real (untracked) por essas rodadas.

## O que esta revisão NÃO confirma (não canonizar)

- **Runtime de jogo**: `T-RSTV21/25B/26`, `S-RV-26…34`, `BUG34` seguem `NAO_EXERCITADO` (exigem
  jogo e/ou o dono; AUT-4/5/6). `T-RSTV25B` continua `INDETERMINADO` (LogOutput do próximo boot).
- **Publicação online / local↔online**: fora do AUT-3.
- **Aceite humano e DoD**: não avaliados aqui; a bancada automatizada **não** substitui o aceite do
  dono nem a publicação. Verde offline ≠ runtime ≠ DoD.
- As medições valem para o HEAD `f526fe9b71f5` e para as mudanças visíveis no disco nesta janela.

> AUT-3R2 não publica, não aprova deployment e não substitui o aceite humano do DoD.
