# ORG-R2-GATE — conferência e integração do handoff ORG-R2-E1 (t_a5b7b22a)

Papel deste cartão: GATE. Ele **confere e integra** o resultado da implementação `t_f03077f4`
(commit `26e3fda`), NÃO reaplica o bloco de `.gitignore` nem executa desindexação genérica.
Fotografia da conferência: 11/10/2026 18:04 -03:00, repo `C:/dev/stolen-realm`, branch `ci-validate-test`.

Plano de origem: `docs/automacao/ORG-R1-parte01..04.md` (auditoria `t_adbb8f0d`).
Relatório da implementação conferida: `docs/automacao/ORG-R2-EXEC-parte01.md`.

---

## 1. O que a implementação declarou

- Commit único e exclusivo da frente: `26e3fda62bcc01952adcccdbd944f14e60603b7b`, 2 arquivos.
- `git rm --cached`: ZERO (lista aprovada de remoções do índice era vazia).
- `git ls-files -ci --exclude-standard`: 34 → 0.
- `.gitignore`: 85 → 140 linhas; sha256 `2754421fd82b6881191348894cd8312364fc309d7384b834b8766ba2150f4a4a`.

## 2. Conferência (comando → resultado real)

| Verificação | Comando | Resultado |
| --- | --- | --- |
| Commit existe e é único | `git show --stat 26e3fda` | 2 arquivos: `.gitignore` (+63/-4) e `docs/automacao/ORG-R2-EXEC-parte01.md` (+85) |
| Nenhum arquivo apagado no commit | `git show --name-status --format="" 26e3fda \| grep -c '^D'` | `0` |
| Conteúdo conferido do `.gitignore` | `sha256sum .gitignore` | `2754421fd82b6881191348894cd8312364fc309d7384b834b8766ba2150f4a4a` (idêntico ao declarado) |
| Rastreados que casam com ignore | `git ls-files -ci --exclude-standard \| wc -l` | `0` |
| Rastreados antes/depois | `git ls-tree -r --name-only 1a82539 \| wc -l` → `26e3fda` | `1639` → `1640` (só o relatório novo) |
| Regras novas de ignore | `grep -n '^/scratch/\*\|^/\.worktrees/\|^/kanban/kanban.db\*\|^/nul' .gitignore` | linhas 51, 99, 101, 103 |
| Exceções nominais da frente | `awk 'NR>86 && /^!/' .gitignore \| wc -l` | `34` (linhas 105–140) |
| `.gitignore` intacto desde o commit | `git diff --stat 26e3fda HEAD -- .gitignore` | vazio |
| `dist/.gitkeep` segue rastreado | `git ls-files --error-unmatch dist/.gitkeep` | ok |
| `lib/` privado ignorado | `git check-ignore -v -n --no-index lib/Assembly-CSharp.dll` | `.gitignore:3:lib/` |
| Scratch genérico continua ignorado | probes `scratch/kit/data.txt`, `scratch/foo.py`, `scratch/backups/x.dll`, `scratch/um-dump.json` | linhas 51 (`/scratch/*`), 69, 64, 66 — todos ignorados |

## 3. Prova de que nada saiu do disco (os 34 caminhos)

Lista dos 34 caminhos (32 logs de fixture/prova + `scratch/test-cycle.sh` + `tools/automacao/kit15/docs/primeiro-uso.md`),
verificada um a um com `git ls-files --error-unmatch`, `test -f` e `git check-ignore -v -n --no-index`:

- fora do índice: `0`
- fora do disco: `0`
- sem negação nominal como regra final: `0`

Exemplos da regra final reproduzidos:

```
.gitignore:105:!/scratch/test-cycle.sh	scratch/test-cycle.sh
.gitignore:107:!/tools/automacao/kit15/docs/primeiro-uso.md	tools/automacao/kit15/docs/primeiro-uso.md
.gitignore:109:!/tools/automacao/aut5/fixtures/log-completo.log	tools/automacao/aut5/fixtures/log-completo.log
```

Ou seja: os 34 continuam rastreados E no disco, e a regra que os salva do `*.log`/`/scratch/*` é uma
exceção nominal por caminho (nunca uma árvore).

## 4. Justificativa de cada linha nova (as 4 famílias do bloco ORG-R2)

- `/.worktrees/` — worktrees locais são repositórios independentes; indexá-los criaria gitlink.
- `/kanban/kanban.db*` — evita que o banco-isca local e sidecars entrem no índice.
- `/nul` — arquivo reservado do Windows criado por redirecionamento local; ignorar, nunca apagar.
- `!/scratch/test-cycle.sh` — ferramenta mantida (por ORG-R3 passa a shim legado em `scratch/`).
- `!/tools/automacao/kit15/docs/primeiro-uso.md` — guia de ferramenta rastreado (casaria com `*.md` da linha 20).
- 32 × `!/tools/.../prova*.log` e fixtures — provas e fixtures intencionais, não dumps efêmeros; escopo por arquivo.

O bloco tem comentário de cabeçalho explicando por que a lista de `git rm --cached` desta frente é vazia.

## 5. Aceite do repositório (pós-conferência)

- `python tools/audita_docs.py` → **RC=0**, "nenhuma inconsistencia encontrada".
- `python tools/check_segredos.py` → **RC=0**, "nenhum padrao de credencial encontrado".

## 6. Observação de concorrência (registro honesto)

Durante esta conferência, outra frente commitou no mesmo branch: `8757001`
("KIT15-D6-CRLF: contra-prova discrimina em clone Windows CRLF"). Isso levou os rastreados de 1640 → 1641
(1 doc novo + 3 arquivos de `tools/automacao/kit15`). Não afeta o aceite do R2:

- `.gitignore` sem diff entre `26e3fda` e `HEAD` (sha256 preservado);
- `git ls-files -ci --exclude-standard` continua `0`;
- os 34 caminhos da frente continuam intactos no índice e no disco.

As edições paralelas do dono na árvore de trabalho (`tools/automacao/aut5/test_aut5.py`,
`tools/automacao/aut5/test_snapshot_modal.py` e os docs `ORG-AUT5-*` não versionados) foram
preservadas — nenhum comando desta frente as tocou.

## 7. Limites respeitados por este gate

Nada foi reaplicado, desindexado, apagado, movido, renomeado, buildado, deployado ou empurrado:
- `git rm --cached`: **0** comando executado por este cartão;
- `git add -A` / `git commit -a`: **não usados** (o único arquivo adicionado por este cartão é este relatório);
- nenhuma edição em `.gitignore`, em fonte de mod, em `dist/` ou em histórico.

## 8. Integração

R2 fecha com o índice limpo de rastreados-que-casam-com-ignore e com as exceções nominais declaradas.
Isso destrava a frente de movimentos (`t_873a563d` / `t_c299dd97`), que pode executar
`scratch/test-cycle.sh` → `tools/test-cycle.sh` com a política de ignore já estável
(aqui o caminho antigo fica apenas como shim legado, coberto pela exceção nominal da linha 105).
