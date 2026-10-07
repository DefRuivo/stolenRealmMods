# AUT-3 — resumo legivel da bancada offline

- gerado: 2026-10-05 15:47:35
- git: ci-validate-test @ f526fe9b71f5
- **veredito: VERDE**
- perfil intacto: **True** (28 arquivos hasheados)
- repo intacto: **True**
- builds: 6/6 (Release, -p:DeployToBepInEx=false)

## Builds (fonte -> DLL por hash)

| mod | estado | fonte=Release=perfil | sha | exit |
|---|---|---|---|---|
| BetterCombatText | OK | SIM | 06dae5aa7b5e | 0 |
| BetterFont | OK | SIM | 2c07f5e959af | 0 |
| BetterStats | OK | SIM | 5a3c001ad424 | 0 |
| BetterTooltips | OK | SIM | 270f311b0f7b | 0 |
| RoguelikeDebugger | OK | SIM | 99c156799380 | 0 |
| RoguelikeSkillTreeVisualizer | OK | SIM | 454587a031a3 | 0 |

## Conferidores estaticos

| id | classe | escritas_docs | estado | exit | s |
|---|---|---|---|---|---|
| check_dupes | estrutura | nao | OK | 0 | 0.097 |
| check_chave_compartilhada | estrutura | nao | OK | 0 | 0.127 |
| check_notas_redundantes | estrutura | SIM | OK | 0 | 0.098 |
| check_fix_keys | estrutura | nao | OK | 0 | 0.074 |
| check_segredos | estrutura | nao | OK | 0 | 7.012 |
| check_versoes | pacote | nao | OK | 0 | 0.075 |
| check_patches | estrutura | nao | OK | 0 | 0.502 |
| check_dependencias | pacote | nao | OK | 0 | 0.111 |
| check_deploy_optin | estrutura | nao | OK | 0 | 0.095 |
| pacotes_preflight | pacote | nao | OK | 0 | 0.095 |
| audita_docs | docs | nao | OK | 0 | 0.516 |

## Suite

- **suite_puros** (puro): exit=0, PASSOU=85
- **suite_contra_prova** (estrutura): exit=0, PASSOU=14, PROVA_OK=49
- **suite_jogo** (estrutura): exit=0, PASSOU=1

## Contra-provas (copia isolada)

| id | familia | defeito exit | apos correcao |
|---|---|---|---|
| cp_dupes | chave duplicada (INC-1: derruba o LocalizePatch inteiro) | 1 | 0 |
| cp_versoes | versao divergente (manifest != csproj) | 1 | 0 |
| cp_patches | parametro posicional do Harmony (__0) sem justificativa | 1 | 0 |
| cp_deploy_optin | alvo de deploy SEM opt-in explicito (escreveria no perfil) | 1 | 0 |
| cp_segredos | credencial plantada em arquivo RASTREADO | 1 | 0 |

## Cobertura alinhada a matriz AUT-2

matriz sha 8503010272d7 · {'OK_OFFLINE': 8, 'PARCIAL_OFFLINE': 0, 'NAO_EXERCITADO': 12, 'REPROVADO': 0}

| id | mod | estado AUT-3 | evidencia/motivo |
|---|---|---|---|
| M1 | BetterCombatText | OK_OFFLINE | build Release 0 erros; fonte->DLL = Release = perfil (06dae5aa7b5e); zip = do Release |
| M2 | BetterFont | OK_OFFLINE | build Release 0 erros; fonte->DLL = Release = perfil (2c07f5e959af); zip = do Release |
| M3 | BetterStats | OK_OFFLINE | build Release 0 erros; fonte->DLL = Release = perfil (5a3c001ad424); zip = do Release |
| M4 | BetterTooltips | OK_OFFLINE | build Release 0 erros; fonte->DLL = Release = perfil (270f311b0f7b); zip != do Release |
| M5 | RoguelikeDebugger | OK_OFFLINE | build Release 0 erros; fonte->DLL = Release = perfil (99c156799380); zip = do Release |
| M6 | RoguelikeSkillTreeVisualizer | OK_OFFLINE | build Release 0 erros; fonte->DLL = Release = perfil (454587a031a3); zip != do Release |
| T-RSTV6 | RoguelikeSkillTreeVisualizer | OK_OFFLINE | 36 testes rstv na suite: ['PASSOU', 'PROVA_OK'] |
| T-RSTV21 | RoguelikeSkillTreeVisualizer | NAO_EXERCITADO | janela read-only abre/navega/fecha e publicacao — exige jogo/dono |
| T-RSTV25B | RoguelikeSkillTreeVisualizer | NAO_EXERCITADO | precisa do LogOutput.log do proximo boot (INDETERMINADO) |
| T-RSTV26 | RoguelikeSkillTreeVisualizer | NAO_EXERCITADO | hover com numeros resolvidos — revalidacao visual em jogo |
| S-RV-26 | BetterTooltips | NAO_EXERCITADO | tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO |
| S-RV-27 | BetterTooltips | NAO_EXERCITADO | tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO |
| S-RV-28 | BetterTooltips | NAO_EXERCITADO | tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO |
| S-RV-29 | BetterTooltips | NAO_EXERCITADO | aura viva x fora da aura — leitura em jogo |
| S-RV-30 | BetterTooltips | NAO_EXERCITADO | aura de perigo com Source=null — medicao em jogo |
| S-RV-31 | BetterTooltips | NAO_EXERCITADO | agregado por atributo — leitura em jogo |
| S-RV-33 | BetterTooltips | NAO_EXERCITADO | flame/decay por alvo — leitura em jogo |
| S-RV-34 | BetterTooltips | NAO_EXERCITADO | defeito do proprio mod superado por RV-30 — revalidacao em jogo |
| BUG34 | BetterTooltips | NAO_EXERCITADO | aceite humano ja dado (KANBAN l.506); regressao de feed exige jogo |
| AUT-REUSE | transversal | OK_OFFLINE | reusa roda_testes.py (0/1/2), checa_shrines, CAP-1; nao reconstroi |

## Nao exercitado (NAO e OK)

- BUG34
- S-RV-26
- S-RV-27
- S-RV-28
- S-RV-29
- S-RV-30
- S-RV-31
- S-RV-33
- S-RV-34
- T-RSTV21
- T-RSTV25B
- T-RSTV26

> AUT-3 nao substitui aceite humano nem publicacao do DoD.
