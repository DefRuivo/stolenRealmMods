# Cobertura de tooltips — Stolen Realm (RV-7)

> **Censo do que existe para revisar.** Sem esta lista fechada, "revisar todas as
> tooltips" é promessa que não dá pra conferir. Gerado em **29/09/2026**.

## Números

| Categoria | Arquivo | Entradas | Observação |
|---|---|---:|---|
| Skills / spells | `skills.csv` | **451** | 31 são da árvore **Bard → `intocavel`** (regra do projeto) |
| Status / efeitos | `status.csv` | **560** | coluna `classe` separa debuff/buff |
| Itens base | `itens.csv` | **905** | |
| Afixos de item | `afixos.csv` | **285** | |
| Powerups | `powerups.csv` | **79** | 19 powerups; uma linha por **nível**, porque o tooltip é por nível |
| | | **2.280** | **2.249 revisáveis** (2.280 − 31 Bard) |

### Cortes por tipo

**Skills por árvore** (define a divisão do `RV-8`) — Shadow 41 · Ranger 40 · Nature 39 ·
Warrior 39 · Thief 38 · Light 36 · Monk 36 · Chaos 33 · Fire 32 · Cold 31 ·
**Bard 31 (intocável)** · Lightning 30 · Basic 15 · Innate 10.

**Status por tipo e classe** — Normal 457 (260 buff / 97 debuff / 100 indefinido) ·
Fortune 83 (48 / 10 / 25) · Quest 14 · QuestItem 6.
→ **107 debuffs** já identificados: é o primeiro lote do `RV-9`.

**Itens por tipo** — Weapon 301 · Armor 118 · Commodity 98 · Head 83 · Material 81 ·
Consumable 66 · Ring 62 · Amulet 60 · Shield 33 · Tool 3.

**Afixos** — Prefix 192 · Suffix 90 · EndGame 3.

## Como usar

Cada CSV tem uma coluna **`status`** — é o checklist:

| status | significa |
|---|---|
| `pendente` | ainda não revisado (estado inicial de tudo) |
| `revisado` | conferido contra o código + fontes externas, e o texto atual está correto |
| `corrigido` | revisado **e** o texto foi alterado no `BetterTooltips` |
| `intocavel` | fora de escopo conscientemente (hoje: árvore Bard) |

Abre bem no Excel / Google Sheets / LibreOffice — dá pra filtrar por `arvore`,
`tipo` ou `classe` e ir marcando. **Ao terminar cada lote, atualize o CSV** — é ele
que o `RV-13` (auditoria) vai ler pra provar a cobertura.

> A coluna `classe` do `status.csv` é **pista, não verdade**: sai do sinal dos efeitos
> de atributo e, quando não há número, da redação da descrição. Status que não caíram
> em nenhum dos dois ficam `indefinido` (145 hoje). Corrija a coluna ao revisar.

## Critério de "revisado"

Vale para toda categoria (é a regra do projeto):

1. A mecânica é conferida **no código** (`Assembly-CSharp`) — é a fonte da verdade;
2. O texto é triangulado contra **≥2 fontes independentes** (wiki, Discord, Reddit,
   patch notes **mais recentes**, guias Steam, mods open-source);
3. Divergência → **o código vence**, e a fonte é registrada junto da correção;
4. A correção, quando existe, é conferida **no jogo** (texto no arquivo-fonte não
   garante texto no jogo — ver os pitfalls da skill).

## Como regerar

O censo sai do dump de boot do **RoguelikeDebugger** (nenhuma leitura manual):

```bash
bash scratch/test-cycle.sh 30 "Inventário"   # abre o jogo, coleta o dump, fecha
python tools/census.py                       # gera/atualiza os CSVs desta pasta
```

O `tools/census.py` lê o `LogOutput.log` do perfil e escreve os 5 arquivos.
Se você mexer num mod, rebuilde antes de rodar o ciclo.

**A coluna `status` sobrevive à regeneração** — o script carrega os status do arquivo
anterior antes de reescrever, então o trabalho de revisão não é perdido ao rodar o censo
de novo. (Só evite marcar status com o CSV aberto no Excel, que pode regravar por cima.)

Ferramentas de apoio:

- `python tools/check_fix_keys.py` — confere se as chaves das tabelas do `BetterTooltips`
  existem mesmo nos textos do jogo. Uma chave com um espaço a mais (ou escrita de memória
  em vez de copiada do asset) **nunca dispara**, e a falha é silenciosa.
- `python tools/audit_tooltips.py [arvore]` — auditoria de conteúdo das skills (RV-8b):
  tipo de dano declarado, valor dinâmico presente, área mencionada, descrições curtas e
  **famílias de redação divergentes**. Escreve `docs/cobertura/auditoria-tooltips.md`.
- `python tools/scan_tokens.py` — a varredura da gramática de texto (RV-8a).
- Relatório de cada lote fica em `docs/cobertura/revisao/`.

## Vocabulário da coluna `status`

| status | significado |
|---|---|
| `pendente` | ainda não revisada |
| `revisado` | conferida contra o código e ≥2 fontes externas; o texto atual está certo |
| `corrigido` | tinha defeito e foi corrigida no `BetterTooltips` |
| `sem-explicacao` | **não deve ser explicada** por escolha de design (flavor) — sai da auditoria |
| `intocavel` | árvore Bard: não revisar nem alterar |

> **O censo é o estado ANTES.** Ele é gerado a partir do jogo, então mostra o texto
> original — não o que o `BetterTooltips` corrige em tempo de execução. As auditorias
> continuam acusando o que já foi corrigido; quem diz o que já está pronto é o `status`.

## Gramática dos textos (essencial para revisar)

O mesmo `[...]` significa coisas diferentes conforme a categoria — extraído do código
(`Tooltip`), em 29/09:

| Categoria | Pipeline | O que o colchete significa |
|---|---|---|
| `skills`, `status`, `powerups` | `Tooltip.ApplyDescriptionExpressions` | `[N]` = **índice da N-ésima expressão** do asset (o jogo avalia e colore em `<color=#CBB396>`); `[[X]]` = atributo (vira `<b>nome</b>`); `@x@` = negrito |
| `itens`, `afixos` | `OptionsManager.Localize(...).Replace("[token]", valor)` | `[level value]`, `{SKL=...}`, `[15]` = **token nomeado de template**, trocado pelo próprio chamador |

Consequência prática nas categorias de **expressão**: um `[` que não seja seguido de
dígito faz o jogo devolver `Parsing Error with: X` **no lugar do tooltip inteiro**; e um
índice de 2+ dígitos (`[10]`) é lido só pelo primeiro dígito — o jogo remove 3 caracteres
e usa a **expressão errada**. Em itens/afixos, o mesmo padrão é normal.

A varredura `python tools/scan_tokens.py` → `alerta-tokens.md` aplica essa regra:
em 29/09 deu **0 alertas** nas categorias de expressão e **102 ocorrências esperadas**
de template em itens/afixos. Ou seja: **não há placeholder vazando** no jogo hoje —
o que sobra para o `RV-8` é revisão de **conteúdo** (mecânica × texto), não de sintaxe.

## O que este censo AINDA não cobre

Honestidade sobre o limite atual — falta censo para:

- **Tutoriais / mensagens de sistema** — passam pelo `OptionsManager.Localize`, mas
  não há dump deles ainda;
- **Strings de UI em geral** (menus, botões, avisos);
- **Texto de quests e eventos** fora do que aparece nos status (os 14 `Quest` e
  6 `QuestItem` do `status.csv` cobrem só uma parte);
- **Descrições de ação** (as linhas de "o que a ação faz" no combate).

Isso é o escopo do `RV-12`. Até lá, "cobertura total" vale para as 5 categorias acima.
