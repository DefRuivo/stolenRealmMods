# ORG-R2 — parte 01: política de `.gitignore` sem desindexar fixtures e entregas

Tarefa t_f03077f4 (frente gitignore+cached de ORG-R1). Repo C:/dev/stolen-realm, branch ci-validate-test. Fotografia de 11/10/2026 17:20 -03:00, HEAD de entrada 1a82539db5f8fc2cadffd77c38880323502d467c. Plano de origem: docs/automacao/ORG-R1-parte01..04.md (auditoria t_adbb8f0d), já com os saneamentos de baseline concluídos.

## 1) O que esta frente fez — e o que NÃO fez

Feito: apenas o bloco de `.gitignore` proposto pela parte 02 (com as erratas das partes 03/04) e este relatório, em UM commit nominal.

NÃO feito, registrado honestamente:

- ZERO `git rm --cached`. A lista aprovada de remoções do índice é VAZIA. Nenhum `git add -A`, nenhum `git commit -a`, nenhum comando recursivo genérico e nenhum `--ignore-unmatch`.
- Nenhum arquivo apagado, movido, desindexado ou reescrito. Nenhum push, deploy, build, instalação em perfil ou execução do jogo.
- Nenhuma regra de segredos alterada; nenhuma regra global nova de `*.dll`, `*.zip`, `*.json` ou `*.db`.
- Nada fora de `.gitignore` e deste relatório entrou no commit: as edições que já existiam na árvore de trabalho (frente AUT5) foram preservadas como estavam e não foram tocadas.

## 2) Estado medido ANTES da edição

`git ls-files -ci --exclude-standard` (caminhos rastreados que casam com alguma regra de ignore): **34** caminhos.

| Regra que os alcançava | Caminhos | Disposição |
|---|---:|---|
| `scratch/` (linha 49) | 1 | ferramenta mantida: scratch/test-cycle.sh |
| `*.log` (linha 16) | 32 | fixtures e provas intencionais: 1 em tools/automacao/aut5/fixtures/, 5 em tools/fixtures/, 26 em tools/testes/ |
| `*.md` (linha 20) | 1 | guia de ferramenta rastreado: tools/automacao/kit15/docs/primeiro-uso.md |

Total rastreado na entrada: 1639 caminhos. `dist/.gitkeep` rastreado. Categorias proibidas com rastreado: **0** em todas — nenhum bin/obj, nenhuma DLL/PDB, nenhum banco, nenhum cache e nenhum backup no índice.

## 3) Desvio de escopo registrado: 34, não 33

O plano (partes 02 e 04) mediu 33 rastreados-ignorados na fotografia de 097f9506: 1 ferramenta + 32 logs. A fotografia de hoje tem 34. O 34º é tools/automacao/kit15/docs/primeiro-uso.md, criado DEPOIS daquela fotografia pela reconciliação documental (commit 107ee8a, frente ORG-PRE-DOC).

A parte 02 manda comparar a nova fotografia com o plano e registrar a decisão antes de desindexar. Decisão tomada: **não desindexar**. O arquivo é o guia de primeiro uso da ferramenta KIT-15, está no índice e é apontado pela documentação da própria ferramenta; retirá-lo deixaria o clone sem o alvo dessa citação. Ele entra, portanto, como exceção NOMINAL, exatamente como os outros 33. Isso não é redução das regras de segredos nem isenção ampla: a exceção é UM caminho, não uma árvore e não um `!*.md`.

## 4) Mudança aplicada no `.gitignore`

O arquivo tinha 85 linhas; ficou com 140. Três edições:

1. Linha 49: `scratch/` → `/scratch/*`. A regra antiga ignorava o diretório inteiro; a nova ignora o CONTEÚDO e permite exceção nominal de arquivo rastreado dentro dele.
2. Comentário da regra de test-cycle: atualizado para a política de ORG-R3 (implementação promovida para tools/, permanecendo só o shim de compatibilidade).
3. Bloco ORG-R2 no fim do arquivo: 3 regras novas de ignore (`/.worktrees/`, `/kanban/kanban.db*`, `/nul`) e 34 exceções nominais (`!/scratch/test-cycle.sh`, `!/tools/automacao/kit15/docs/primeiro-uso.md` e os 32 logs).

As 85 linhas originais foram preservadas, exceto a troca pontual da regra geral de scratch e o comentário atualizado. Continuam intactas as regras de segredos, `dist/*` com `!dist/.gitkeep`, `bin/`, `obj/`, `lib/`, `NuGet/`, `__pycache__/`, `*.pyc` e as regras específicas de scratch.

## 5) Verificação pós-edição

Comandos executados na raiz do repo, com o resultado real:

| Comando | Resultado |
|---|---|
| `git ls-files -ci --exclude-standard` | 0 caminhos (era 34). Aceite principal cumprido SEM desindexar nada |
| `git ls-files \| wc -l` | 1639 (inalterado) |
| `git ls-files --error-unmatch <cada um dos 34>` | todos os 34 seguem no índice |
| teste de existência física dos 34 | todos os 34 no disco |
| `git check-ignore -v -n --no-index <os 34>` | a regra final de cada um é a negação nominal correspondente (inclui `!`), não uma regra de ignore |
| `git check-ignore -v -n --no-index scratch/kit/data.txt scratch/novo-dump.bin` | `.gitignore:51:/scratch/*` — conteúdo genérico de scratch segue fora do índice |
| `git check-ignore -v -n --no-index scratch/foo.py` | `scratch/*.py` (regra preexistente) |
| `git check-ignore --no-index -v scratch/um-dump.json .worktrees/level-r2/.git kanban/kanban.db nul` | aponta `scratch/*.json`, `/.worktrees/`, `/kanban/kanban.db*` e `/nul` |
| `git ls-files dist/` | `dist/.gitkeep` (mantido) |
| `git check-ignore --no-index -v lib/Assembly-CSharp.dll` | `lib/` (privado, ignorado) |

## 6) Validação do workflow e auditoria de docs

Passos 1 a 8 e 10 de `.github/workflows/validate.yml` executados na raiz do repo depois da edição — todos exit 0:

- `python tools/check_segredos.py` → 0 (nenhum padrão de credencial; herança de entropia já triada)
- `python tools/check_versoes.py` → 0 (6 mods alinhados)
- `python tools/check_patches.py` → 0 (2 avisos não reprovam)
- `python tools/check_fix_keys.py` → 0
- `python tools/check_dupes.py` → 0
- `python tools/check_notas_redundantes.py` → 0
- `python tools/check_chave_compartilhada.py --estrito` → 0
- `python tools/cobertura_ui_localized.py --prova` → 0 (11 testes, 0 failures)
- `python .github/scripts/valida_pacotes.py` → 0 (6 pacotes, 0 problemas)
- `python tools/audita_docs.py` → 0 (nenhuma inconsistência encontrada)

Passo 9 (empacotador, guardado): neste host existe DLL em `<Mod>/bin/Release/netstandard2.1/`, então no runner limpo é o ramo `--listar-nomes` que roda; ele foi exercitado e saiu 0. O empacotador de verdade NÃO foi executado no repo vivo, para não mexer em `dist/` — empacotar é ritual local e já foi exercitado na bancada do plano.

Rodar os passos não deixou resíduo: a impressão de estado do Git antes e depois é idêntica (mesmas modificações locais da frente AUT5, nada novo).

## 7) Limites, provas e próximo passo

- O commit desta frente contém apenas `.gitignore` e este relatório (stage nominal, por caminho).
- Nada foi apagado: os 34 caminhos seguem no índice e no disco; o conteúdo de scratch, as entregas de docs/ e os pacotes de dist/ não foram tocados.
- Não houve push, não houve reescrita de histórico e não houve desindexação: desindexar não apagaria blobs do passado, mas sairia do escopo aprovado.
- O gate R2 confere e integra este MESMO trabalho; ele NÃO deve aplicar o patch de `.gitignore` de novo. Referências, movimento de test-cycle e limpeza nominal de caches continuam em frentes próprias.
