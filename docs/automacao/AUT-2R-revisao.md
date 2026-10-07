# AUT-2R — revisão independente do inventário AUT-2 (t_9f420f69)

Revisor: subagente AUT-2R (t_156e7eee), **não-autor**. Estado lido: HEAD `f526fe9`, branch `ci-validate-test`.
Artefato revisado: `docs/automacao/AUT-2-matriz.json` sha256 `e43e8ce0…30292` (confere com o disco); `AUT-2-contexto.md` (4772 B).

## Veredito do critério inventário: **APROVADO** (com achados não bloqueantes)
A matriz é completa e confiável: **AUT-3/AUT-4 podem partir dela**. Os achados são imprecisões documentais (contexto/cobertura) e uma evidência removida — nenhuma omissão silenciosa de arquivo de produto. Lacunas de runtime seguem explícitas e **não** herdam OK.

## OK (verificado com prova)
- Conjunto: 78 registros == `git status -z --untracked-files=all` menos os 2 arquivos de `docs/automacao` (37 M + 41 ??); diff de conjuntos vazio nos dois sentidos.
- Hashes: 78/78 `sha256` conferem com o disco; nenhum arquivo ausente.
- Categorias/mod: doc17·codigo3·dados13·teste45 = 78; BT48·transversal23·RSTV3·4×1 = 78 (batem com o resumo).
- Estados separados: `release/mods.json` `4f886b92…` e os 21 zips de `dist/` — todos os sha256 conferem; `bin==perfil` nos 6; `zip-dll==bin` só nos 4; BT (`270f311b`≠`80bba454`) e RSTV (`454587a0`≠`c2ce4862`) divergem do zip — **confirmado**.
- Publicação: 6× `publicado_online: NÃO VERIFICADO`; nenhum pacote **local** foi chamado publicado.
- BUG-34: aceite humano em `KANBAN.md:506` — **não reaberto**.
- FONTE↔DLL (refuta a causalidade só-mtime): `ilspycmd` no DLL do **perfil** acha os marcadores do fonte — RSTV-26 `ShowSkillTooltip(Item.SkillInfo, target, false,false,false)` + else, e BUG-34 `[ThreadStatic]`/patch `Root.SendMessageWindowMessage`/log (LocalizePatch l.1232).
- Fixtures/ferramentas referidas existem (`check_versoes.py`, `regras_bf_estilo.py`, `cp_rstv*`, `roda_testes.py`, `checa_shrines.py`, `ocr_tela.ps1`, `scratch/cap1/*`).
- 12 registros `tarefa:["nao_mapeada"]` são docs/READMEs — não inventaram tarefa (OK).
- Controles negativos (sandbox em memória, matriz intacta): omitir 1 registro → `OMISSAO` detectada; trocar 1 sha → `HASH_TAMPER` detectado.

## ACHADOS (por gravidade)
- **MÉDIO** | `AUT-2-contexto.md:18` — diz "Excluídos os **6** artefatos do próprio `docs/automacao`", mas a pasta tem **2** arquivos e a matriz só deixa os IDs A038/A039 sem uso (2 exclusões); o JSON não registra exclusões (`excluidos` ausente). Sem omissão de produto (78==git), mas a contagem "6" não é sustentada.
- **MÉDIO** | `AUT-2-contexto.md:49` — RSTV-25b "falta `LogOutput.log`": **FALSO**. O log existe em `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\LogOutput.log` (1.234.333 B, mtime 05/10 14:32; RSTV-20/21 presentes). Não há linha `RSTV-25:` porque o caminho de linhas de dependência não foi exercido na sessão — não por log ausente. O **INDETERMINADO** do RSTV-25b permanece, com motivo corrigido.
- **BAIXO** | matriz cobertura **M4** `evidencia_atual` — "37 alterações locais" para BetterTooltips, mas o mod tem **48** registros (37 é o total de M global).
- **INDETERMINADO** | matriz `reconciliacao_snapshots` — "SEM DRIFT" não re-verificável: os snapshots `.z` foram removidos e os sha de partida (`74ce967f`) e final (`73b1e2d7`) diferem sem explicação no JSON. O conjunto atual coincide com a matriz (impacto prático nulo), mas **falta a prova**.

## Testes executados (esta rodada, read-only)
sha256 dos 78 + set-diff contra `git status -z`; hashes de `release/mods.json`, 21 zips, 6× bin/perfil/dll-do-zip; `ilspycmd` em 2 DLLs do perfil; 2 controles negativos em memória; grep/tail do `LogOutput.log`.

## Não coberto / não aprovado
Runtime de jogo (RV-49, RSTV-25b, qualquer verificação em jogo) → AUT-4/5/6, **não aprovado aqui**. DoD de nenhum mod avaliado/aprovado. Sem build, suíte, jogo, commit ou publicação nesta rodada.
