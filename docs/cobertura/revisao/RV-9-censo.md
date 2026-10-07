# RV-9 — Censo dos status (buffs e debuffs)

Gerado por `tools/censo_status.py`. **Alvo do pedido:** revisar todos os buffs e
debuffs e seus tooltips, **na mesma linha de formato das skills** (o processo completo
está descrito no RV-9 do `KANBAN.md`).

## Onde estamos

| grupo | entradas | pendentes |
|---|---|---|
| `Normal` | 457 | 0 |
| `Fortune` | 83 | 0 |
| `Quest` | 14 | 0 |
| `QuestItem` | 6 | 0 |

**Pendentes no grupo `Normal` (buffs/debuffs): 0 de 457.**

> O corte **buff x debuff** ainda não está no CSV: depende do `BenefitType` do status
> (em investigação por agente). Enquanto isso o agrupamento é pelo `tipo` do asset.
> Quando o campo for dumpado, este censo ganha a coluna e a fila é reordenada:
> **Harmful (debuffs) → Beneficial (buffs) → Quest/Fortune/resto**.

## Fila de trabalho — DEBUFFS PRIMEIRO (primeiros 60 pendentes)

| nome | tipo | raridade | efeitos | revise |
|---|---|---|---|---|

## Como o veredito entra

Os mesmos quatro estados das skills, na coluna `revisao` do `status.csv`:
- `revisado` — conferido no asset/código, texto de pé;
- `corrigido` — o texto mudou (entra no `TextFixes`);
- `sem-explicacao` — omissão **por design** (ex.: os sorteios do Chaos);
- `intocavel` — não se mexe (ex.: árvore Bard).

Status **não** estão no dicionário de localização: são campos brutos do asset, então a
correção é em **runtime (Harmony)**, não em tabela de texto.
