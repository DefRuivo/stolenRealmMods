# INT-R1-C6 — parte 03: contagens fechadas e as listas de borda

Toda contagem abaixo é **reproduzível** por `python tools/gera_dump_chaveado.py` seguido de
`python tools/gera_dump_chaveado.py --conferir`. A fonte em máquina é
`docs/cobertura/DUMP-CHAVEADO-LANG-R1-contagens.json`
(sha256 `5e7ce87ff8d7fdafc6cb2a473c7743f1f37d7de9b4e4faadc94625608040b200`).

## 1. Os três baldes do cartão

O escopo pediu três contagens: **quantas chaves vieram da tabela**, **quantas ficaram no caminho
de asset** e **quantas não foram encontradas em nenhum dos dois**.

| Balde | Itens | Como foi decidido |
|---|---:|---|
| **CHAVEADO** (veio da tabela do LANG-R1) | **650** | item de skill/aura cuja descrição casa com uma chave da tabela (tier declarado item a item) |
| **ASSET CRU** (status e afins; caminho antigo `tools/census.py` + `docs/cobertura/*.csv`) | **667** | item da PARTE 2 do dump de tooltips (status) ou do recorte de debuffs — é campo bruto de asset (`KANBAN.md:262`, registro **BT-6**) |
| **NÃO ENCONTRADO** (nem chave, nem asset cru) | **0** | item de skill/aura sem chave na tabela — nestas fontes não existe nenhum |
| **total** | **1317** | |

Dentro dos 667 de asset cru: **645** têm texto que **coincide** com uma chave da tabela (fica
anotado no dump como `chave coincidente (nao usar como fonte)` — chave existir na tabela não prova
que a tela que a usa seja essa) e **22** não casam com chave nenhuma. Os 22 estão listados no dump
novo (seção "Lista do ASSET CRU cujo texto nao esta na tabela") e no JSON: são **7 itens** (6 textos
distintos — Transcendence aparece nos dois arquivos) com texto ausente da tabela, mais **15 itens**
sem descrição nenhuma no dump.

| Item | Status | Motivo |
|---|---|---|
| Transcendence (Fortune/Mythic) | revisado | texto não está na tabela (contado 2×: `tooltips` e `debuffs`) |
| Destructive (Normal/Common) | revisado | texto não está na tabela |
| Necronomicon (Fortune/Mythic) | revisado | texto não está na tabela |
| Overflowing Energy (Fortune/Rare) | revisado | texto não está na tabela |
| Will of the Shaman (Fortune/Rare) | revisado | texto não está na tabela — no dump de origem a descrição está **truncada** |
| Ball Lightning (Fortune/Mythic) | revisado | texto não está na tabela |
| Burning Demon Hearts, Dwarf Rage!, Hunger for Vengeance, Rune of Exploding, Shadow-Drenched Heart, Test Fortune, The Animator - Quest Accept, The Mad Mage - Part 1 / 2 / 4 / 5, Treasure of Moltendunn, Ymir Rune Courage / Honor / Strength | sem-explicacao | **sem descrição no dump** (15 itens; o censo já os marca `_(sem-explicacao)_`) |

## 2. Por arquivo de origem

| Origem | itens | skill/aura (chaveado) | status (asset cru) | tiers dos chaveados |
|---|---:|---:|---:|---|
| `docs/cobertura/DUMP-TOOLTIPS-REVISAO.md` | 1024 | 464 | 560 | exato 394 · normalizado 41 · casefold 29 |
| `docs/cobertura/DUMP-DEBUFFS-REVISAO.md` | 107 | 0 | 107 | — |
| `docs/cobertura/DUMP-PASSIVAS-REVISAO.md` | 186 | 186 | 0 | exato 157 · normalizado 16 · casefold 13 |
| **TOTAL** | **1317** | **650** | **667** | exato 551 · normalizado 57 · casefold 42 |

Os 464 de skill/aura do dump de tooltips = **451 skills** (PARTE 1) + **13 auras de shrine**
(PARTE 3); os 560 de status = PARTE 2 (308 buff / 107 debuff / 145 indefinido, os números que o
próprio dump declara).

## 3. Duplicidade entre os arquivos (para a contagem não enganar)

`DEBUFFS` e `PASSIVAS` são **recortes** do `TOOLTIPS`. Os 1317 itens somam **1210** pares
distintos `(título, descrição)` — **107** itens são repetição exata de outro já presente (é o
recorte de debuffs inteiro). As passivas **não** colidem por título porque no dump de tooltips elas
aparecem com o sufixo `[PASSIVA]` no título. Quem quiser o número de tooltips distintas: **1210**,
não 1317.

## 4. Conferência por comando (o aceite pede contagem conferida)

```bash
$ python tools/gera_dump_chaveado.py --conferir
conferencia do dump gerado (docs/cobertura/DUMP-CHAVEADO-LANG-R1.md):
  linhas '- fonte: TABELA-LANG-R1' :    650   esperado chaveado        650
  linhas '- fonte: ASSET-CRU'       :    667   esperado asset cru       667
  linhas '- fonte: NAO-ENCONTRADO'  :      0   esperado nao encont.       0
  itens com linha de fonte          :   1317   esperado itens          1317
  RESULTADO: OK
$ echo $?
0
```

O `--conferir` relê o **markdown gerado** (não confia no JSON): conta as linhas `- fonte:` de cada
tipo, soma e compara com o total. Um item do dump novo tem exatamente uma linha `- fonte:`
(9180 linhas de arquivo, 1317 itens), então a soma fecha em 1317.

Confere também o tamanho do artefato: `docs/cobertura/DUMP-CHAVEADO-LANG-R1.md` =
526.679 B, sha256 `408ad3ad13681096b2c3279ff0f2a97193b92754f2ad35448e7907842f891694`.

## 5. O que ficou de fora desta contagem (limite medido, não ignorado)

- Os 667 status são contados como **asset cru** por decisão registrada (BT-6), **mesmo** quando o
  texto coincide com uma chave (645 casos). Se algum dia se provar que a tooltip de status é
  resolvida pelo dicionário, esses 645 mudam de balde — o dump novo já traz a contagem deles
  separada justamente para não perder a informação.
- Itens que o dump de origem **não tem** (itens, afixos, powerups, invocações) não entram nesta
  contagem: eles estão nos censos `docs/cobertura/*.csv` e o cartão não pediu migrá-los.
