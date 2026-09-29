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
| `corrigido` | revisado **e** o texto foi alterado no `BetterTexts` |
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

## O que este censo AINDA não cobre

Honestidade sobre o limite atual — falta censo para:

- **Tutoriais / mensagens de sistema** — passam pelo `OptionsManager.Localize`, mas
  não há dump deles ainda;
- **Strings de UI em geral** (menus, botões, avisos);
- **Texto de quests e eventos** fora do que aparece nos status (os 14 `Quest` e
  6 `QuestItem` do `status.csv` cobrem só uma parte);
- **Descrições de ação** (as linhas de "o que a ação faz" no combate).

Isso é o escopo do `RV-12`. Até lá, "cobertura total" vale para as 5 categorias acima.
