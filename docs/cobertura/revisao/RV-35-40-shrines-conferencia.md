# RV-35..RV-40 — Conferência das auras de shrine (Warrior/Guardian/Conqueror/Rogue/Reaper/Seraph)

Data: 03/10/2026 · Status: **CONFERIDO — 0 divergências** · Tarefa de LEITURA (nenhum código alterado).

Objetivo: confirmar, no código decompilado, o **VALOR base** de cada aura de shrine deste lote e o **fator de escala**,
e conferir com a fórmula de referência:

```
Mathf.Round(BASE * (1 + ShrineEffectBonus / 100))
```

## Fontes usadas (todas verificadas nesta rodada)

- **Decompilado** (regenerado nesta rodada com `ilspycmd 8.2.0` a partir de
  `E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed/Assembly-CSharp.dll`):
  `%LOCALAPPDATA%\hermes\cache\scratch\cs\Assembly-CSharp.decompiled.cs` — **371.804 linhas** (mesma contagem do
  decompile de referência do RV-19). O cache havia sido podado; foi regerado.
- **Censo**: `docs/cobertura/status.csv` (coluna `efeitos` = fórmula real do `AttributeEffects` de cada status).
- **Valores esperados**: `tools/dados/shrines-esperado.csv`.
- Doc de referência: `docs/cobertura/revisao/RV-19-shrines.md` §2.

## Método (por que duas fontes)

O cache de expressões compiladas do assembly (`CompiledDynamicExpresso`) é um **dicionário chaveado pela STRING da
fórmula** — a fórmula com `BASE=20` existe **uma única vez** e é compartilhada por Warrior/Guardian/Conqueror/Rogue (e
Dwarven). Logo o decompilado prova **que a base existe e qual é o fator**, mas **não** liga sozinho a aura ao número; o
vínculo aura → base sai do `AttributeEffects` de cada status (censo `efeitos`). As duas leituras foram cruzadas.

## Resultado por shrine (RV-35..RV-40)

| # | Shrine | Atributo alvo | BASE esperado | BASE confirmado | Eixo X | Fórmula (linha do decompilado) | Prova no censo | Veredito |
|---|--------|---------------|---------------|-----------------|--------|--------------------------------|----------------|----------|
| RV-35 | Warrior Aura | `DamageMod` | 20 | **20** | Target | `Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))` — **l.66061** (corpo l.66100: `Mathf.Round(20f * (1f + target87["ShrineEffectBonus"] / 100f))`) | `status.csv:547` | **OK** |
| RV-36 | Guardian Aura | `DamageReduction` | 20 | **20** | Target | idem acima — **l.66061/66100** | `status.csv:216` | **OK** |
| RV-37 | Conqueror Aura | `CritChance` | 20 | **20** | Target | idem acima — **l.66061/66100** | `status.csv:77` | **OK** |
| RV-38 | Rogue Aura | `DodgeChance` | 20 | **20** | Target | idem acima — **l.66061/66100** | `status.csv:402` | **OK** |
| RV-39 | Reaper Aura | `LifeOnHit` | 8 | **8** | Target | `Mathf.Round(8 * (1 + (Target["ShrineEffectBonus"] / 100)))` — **l.66348** (corpo l.66387: `Mathf.Round(8f * (1f + target82["ShrineEffectBonus"] / 100f))`) | `status.csv:387` | **OK** |
| RV-40 | Seraph Aura | `HealthPerTurnPercent` | 10 | **10** | Target | `Mathf.Round(10 * (1 + (Target["ShrineEffectBonus"] / 100)))` — **l.66389** (corpo l.66428: `Mathf.Round(10f * (1f + target81["ShrineEffectBonus"] / 100f))`) | `status.csv:418` | **OK** |

Todas as 6 batem com a fórmula de referência; o fator de escala é **`1 + ShrineEffectBonus/100`** em todas, sem termo de
nível nem de atributo secundário.

### Linhas exatas do censo (coluna `efeitos`)

```
547:Warrior Aura,   DamageMod:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))
216:Guardian Aura,  DamageReduction:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))
 77:Conqueror Aura, CritChance:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))
402:Rogue Aura,     DodgeChance:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))
387:Reaper Aura,    LifeOnHit:Base:Mathf.Round(8 * (1 + (Target["ShrineEffectBonus"] / 100)))
418:Seraph Aura,    HealthPerTurnPercent:Base:Mathf.Round(10 * (1 + (Target["ShrineEffectBonus"] / 100)))
```

## Valor escalado (Mathf.Round half-to-even) — conferência aritmética

| Shrine | BASE | b=0 | b=+8 (Omnism I) | b=+20 (Omnism II) | b=+50 | b=+100 (Horn of Devotion) |
|--------|------|-----|-----------------|--------------------|-------|-----------------------|
| Warrior / Guardian / Conqueror / Rogue | 20 | 20 | 22 | 24 | 30 | 40 |
| Reaper | 8 | 8 | 9 | 10 | 12 | 16 |
| Seraph | 10 | 10 | 11 | 12 | 15 | 20 |

## Divergências

**Nenhuma.** Os 6 valores base conferidos (20, 20, 20, 20, 8, 10) batem exatamente com o esperado, e as 6 fórmulas usam
o mesmo fator de escala `1 + ShrineEffectBonus/100` com `X = Target` (o receptor da aura), como o esperado.

## Observações (limitações de método, não defeitos)

- O decompilado **não** liga aura → base (o dicionário é por string); a base de cada aura é provada pelo `AttributeEffects`
  do status no censo (`efeitos`) e, na origem, por `resources.assets` (RV-19 §2). As duas fontes concordam.
- Fórmulas de base **10** existem **duas** na família e são distintas: `Target` (l.66389 → Seraph/Shaman) e `Source`
  (l.66102 → Decay). Este lote usa a de `Target`; a de `Source` (Decay) está fora do escopo RV-35..40.
- `Mathf.Round` do Unity = half-to-even; nos valores desta tabela não há ponto médio `.5`, então não há ambiguidade.
