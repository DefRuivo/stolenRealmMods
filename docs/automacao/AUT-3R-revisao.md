# AUT-3R — revisão independente da AUT-3 (t_70ef8571)

Revisor AUT-3R (não-autor). HEAD f526fe9 @ ci-validate-test. Escopo: `docs/automacao/AUT-3-*` + `tools/automacao/offline/**`.
`AUT-3-resultado.json` sha256 `9c1aa58244ed…` (confere); `AUT-2-matriz.json` `8503010272d7`.
Reexecução: runner em cópia scratch (`--repo <scratch>/repo --trabalho <scratch>/trabalho --jogo`), 6 builds `-p:DeployToBepInEx=false`, PathMap ancorado no repo REAL (a DLL embute o path do repo → harness de sandbox).
Side effects: perfil (28 hashes) e repo (112 entradas) **intactos**; `AUT-3-resultado.json/resumo` reais byte-idênticos. Nenhuma escrita no repo real.

## Por critério
- **Reexecução (≤6 builds, sem deploy): APROVADO** — 6/6 OK; fonte=Release=perfil; sha `06dae5aa·2c07f5e9·5a3c001a·270f311b·99c15679·454587a0` == entrega.
- **Suite/checagens entregues: APROVADO** — 11/11 checks; 85 puros; 49 PROVA_OK+14 PASSOU; 1 jogo.
- **Contra-provas entregues: APROVADO** — 5/5 PROVA_OK (defeito exit 1 → correção 0).
- **Contra-provas INDEPENDENTES: APROVADO** — 10/10: versões via README, dupes(última entrada), dependência fantasma, deploy sem opt-in, faltante/timeout/exit, PARCIAL/NAO/REPROVADO.
- **Cobertura/T-RSTV6: APROVADO** — resumo idêntico 8 OK·0 PARCIAL·12 NAO·0 REPROVADO; 36 testes rstv; isca PROVA_OK não rebaixa; uma rstv REPROVOU ⇒ T-RSTV6 REPROVADO (NC6c). Não é runtime falso.
- **--jogo não é prova de jogo: APROVADO** — só `t_exemplo_referencias_lib` (lê `lib/`, PE válida); não abre jogo, não carrega save, não lê `LogOutput`; não vende log velho.
- **PathMap × fonte→DLL: APROVADO** — produto alterado não casa (build OK sem fonte provada ⇒ `PARCIAL_OFFLINE`, NC6a).
- **Sandbox/isolamento: ALTERAÇÕES NECESSÁRIAS** — builds herdam USERPROFILE/APPDATA reais (`run_cmd env=None`, bancada_aut3.py:158); o deploy fica contido só pela flag+`Condition`; e os builds rodam **antes** de `check_deploy_optin` (:340→:341) → csproj que perca a Condition escreveria no perfil real antes do guarda (o hash pega depois; o dano já ocorreu). Redirecionar USERPROFILE/APPDATA do sandbox nos builds.
- **Guardas/untracked: ALTERAÇÕES NECESSÁRIAS** — `guarda_repo` não hasheia diretórios não-rastreados (`git status -z` colapsa `tools/automacao/` e `docs/automacao/`): 78 arquivos, 0 desses; arquivos soltos não-rastreados entram.
- **Veredito parcial: ALTERAÇÕES NECESSÁRIAS** — `--sem-build`/`--sem-suite` (ou sem `--jogo`, que omite `suite_jogo`) mantêm VERDE; só contra-prova ausente vira NAO_EXERCITADO (:350).
- **Segredos: ALTERAÇÕES NECESSÁRIAS** — `check_segredos.py:52`/`check_padroes_segredo` imprimem 14 chars do token achado e o runner grava a saída não-OK em `detalhe` (600c) → prefixo parcial iria ao JSON. Nenhum token real nos outputs hoje.
- **AUT-REUSE: ACHADO baixo** — `OK_OFFLINE` hardcoded (:303), não derivado de prova.

## Erro esperado × falso verde
Fiel: faltante/timeout ⇒ `NAO_EXERCITADO`; exit≠esperado ⇒ `REPROVOU`; build sem fonte ⇒ `PARCIAL`; rstv vermelha ⇒ `REPROVADO`. **Nenhum erro virou verde.**

## Lacunas (não OK)
12 critérios runtime `NAO_EXERCITADO`: T-RSTV21/25B/26, S-RV-26..34, BUG34 — exigem jogo/dono (AUT-4/6). T-RSTV25B **INDETERMINADO** (LogOutput do próximo boot). Publicação online fora do AUT-3.

## Veredito
**APROVADO** nos critérios centrais (reprodução, coerência de veredito, contra-provas, `--jogo`, T-RSTV6); **ALTERAÇÕES NECESSÁRIAS** em isolamento do sandbox, cobertura do guarda de repo, veredito com fases puladas e impressão de segredos — nenhuma refuta o VERDE offline entregue, mas endurecer antes de canonizar.
Comandos: harness scratch (PathMap→repo real); `t_aut3_lib` 19/19; `t_aut3_runner` 6/6; negctrl 10/10.
