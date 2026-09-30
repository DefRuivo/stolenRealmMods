# RV-13 — Auditoria de cobertura (a prova "X de X")

> **Tarefa:** fechar o ciclo do "revisar tudo" — reprocessar o censo (RV-7), comparar com os
> checklists de RV-8..RV-12, conferir que as correções estão **instaladas de fato** e registrar
> o número final + a lista de exceções conscientes. Ticket no quadro: `t_533f2bf0`
> ("RV-13: Auditoria de cobertura - provar que 100% das tooltips foram revisadas").
> **Gerado em:** 30/09/2026. Método: leitura + contagens por script (módulo `csv` do Python,
> nunca a olho). **Nenhum arquivo existente foi alterado** — só este relatório foi criado.

---

## 1. Veredito — o número final

**2.246 de 2.280 entradas do censo têm veredito registrado (98,5%).**

Das **2.249 revisáveis** (2.280 − 31 intocáveis da árvore Bard):

- **2.215 de 2.249 revisadas (98,5%)** — 1.917 `revisado` (inclui as notas de explicação) + 134
  `corrigido` + 141 `sem-explicacao` + 23 `indeterminado` (revisados com ponto aberto registrado,
  não chutados) + 31 `intocavel`;
- **34 pendentes (1,5%)** — todas em `status.csv`, a fila "resto" do RV-9 (ver §6.1);
- **0 pendentes** em skills (451/451), itens (905/905), afixos (285/285) e powerups (79/79).

> O denominador é o censo do RV-7: **2.280 entradas em 5 categorias** (`skills`, `status`,
> `itens`, `afixos`, `powerups`). As contagens por linha/conteúdo **não mudaram desde 29/09**;
> o que cresceu foi o material aplicado no mod (ver §4). A citação "4.319 textos" do quadro
> (RV-16) não é reproduzível a partir dos CSVs — ver §7.

## 2. Tabela por categoria

| Categoria (arquivo) | Total | revisado¹ | corrigido | sem-explicacao | intocavel | indeterminado² | pendente | Coberta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Skills / spells (`skills.csv`) | 451 | 309 | 102 | 9 | 31 | 0 | **0** | 451 |
| Status / efeitos (`status.csv`) | 560 | 470 | 15 | 19 | 0 | 22 | **34** | 526 |
| Itens base (`itens.csv`) | 905 | 782 | 9 | 113 | 0 | 1 | **0** | 905 |
| Afixos de item (`afixos.csv`) | 285 | 277 | 8 | 0 | 0 | 0 | **0** | 285 |
| Powerups (`powerups.csv`) | 79 | 79 | 0 | 0 | 0 | 0 | **0** | 79 |
| **TOTAL (5 categorias do censo)** | **2.280** | **1.917** | **134** | **141** | **31** | **23** | **34** | **2.246** |

¹ `revisado` soma os vereditos `revisado` + `nota` (nota = 'texto mantido, explicação anexada' —
mesma convenção com que o `skills.csv` foi marcado: `Cyclone Kick` e `Break The Ice` têm nota e
estão `revisado`). ² `indeterminado` = revisado com ponto **registrado sem prova suficiente**
(19 buffs + 3 debuffs + 1 item) — não é pendência nem chute; a lista está em §5.

Conferência aritmética: 1.917 + 134 + 141 + 31 + 23 + 34 = **2.280**. Cobertas = 2.280 − 34 = **2.246**
(2.246 − 31 intocáveis = **2.215 de 2.249 revisáveis**).

## 3. Como o número foi apurado (e onde a checklist diverge do trabalho)

| Categoria | De onde saiu o veredito | Cobertura |
|---|---|---:|
| Skills | Coluna `status` do `skills.csv` (**a única mantida como checklist**) | 451/451 |
| Status | Workfiles `RV-9-buffs.md` (393 headers) + `RV-9-debuffs.md` (133) × as 560 linhas do CSV; vereditos dos buffs no JSON `scratch/rv9-buffs-vereditos.json`; debuffs pelo registro do commit `fc28b00` | 526/560 |
| Itens | JSON `scratch/rv10-12-vereditos.json` (905 vereditos casados texto-a-texto com o CSV) | 905/905 |
| Afixos | Mesmo JSON (285 pares casados) | 285/285 |
| Powerups | Mesmo JSON (79 vereditos restantes, 1 por nível) | 79/79 |

**Achado central da auditoria:** a coluna `status` **só foi mantida no `skills.csv`**. Nos
outros cinco CSVs com checklist (`status`, `itens`, `afixos`, `powerups` e os de apoio
`acoes`/`invocacoes`) **todas as 2.123 linhas seguem literalmente `pendente`**, inclusive as
que já têm veredito — os vereditos de RV-9..RV-12 foram gravados em JSON/relatórios e aplicados
no `LocalizePatch.cs`, mas **não propagados de volta ao CSV**. Por isso esta auditoria
reconstruiu a cobertura das fontes primárias (JSON + workfiles + relatórios) em vez de ler a
coluna. O critério do ticket ("nenhum item do censo sem status") fica, portanto, a **um passo
mecânico** de ser cumprido: gravar os vereditos nas colunas (`tools/census.py` preserva a
coluna na regeneração — não há risco de perda). Esse passo fica registrado como pendência de
fechamento (§6.2); esta auditoria é read-only por regra da tarefa.

> Correção de registro: o resultado do RV-9 no quadro diz "os 457 status `Normal` foram
> revisados". A checagem linha a linha mostra **426 de 457 `Normal`** (mais 80/83 `Fortune` e
> 20/20 `Quest`+`QuestItem`) = 526 de 560. As 31 linhas `Normal` de fora são as de classificação
> `?`/`Neutro` — contadas nas 34 pendentes (§6.1).

## 4. Conferência de instalação (código × jogo/log)

O ticket pede conferir **no jogo/log que as correções estão instaladas de fato**. Esta auditoria
não abriu o jogo (regra da tarefa), mas reuniu a evidência equivalente:

| Prova | Resultado |
|---|---|
| DLL instalada × DLL buildada | **md5 idêntico** (`ab851a676f933401a5abf6548c71b966`), ambas de 30/09 00:20 — a cópia em `plugins/BetterTooltips/` é exatamente o build da fonte atual |
| Fonte × build | `LocalizePatch.cs` mtime 30/09 00:20; último commit que o toca é `b43e376` (30/09 00:21); `git status` limpo — nada foi editado depois do build |
| `check_dupes.py` (executado hoje) | **TextFixes 86 · TextAppends 200 · duplicadas: nenhuma** (trava do INC-1 passando) |
| `check_fix_keys.py` (executado hoje) | **286 chaves · 282 no censo · 4 fora** (as 4: `Resist Divine`, `Resistance Divine` — os textos renomeados do RV-13/RV-14 — e 2 dicas de UI/loading). Desde o release-check de 29/09: +22 chaves (264→286), 72→86 fixes, 192→200 notas |
| `LogOutput.log` da última sessão (30/09 02:26) | `Better Tooltips carregado.` · **6 plugins** · **25** `explicação adicionada` · **9** `corrigido '…'` · **13** `espacos normalizados` · `corrigido 'Resist Divine' -> 'Resist Holy'` **disparando** (RV-13 fechado no código no commit `884495d` e confirmado no log) |
| Erros | **0** `ArgumentException` · **0** `TypeInitializationException`; os 249 `[Error` do log são **do jogo** (246 `CollisionMeshData` de mesh, 1 `Opp action null`, 2 `No Compiled Expression` de expressão de summon) — **nenhum dos plugins do projeto** |

**O item de RV-13 que não é cobertura** ("renomear `Resist Divine` → `Resist Holy`", fechado no
código em 29/09) está confirmado: aparece no log aplicando a correção.

## 5. Exceções conscientes (decisões, não pendências)

- **Árvore Bard — 31 skills `intocavel`** (regra do projeto: conteúdo chega na próxima
  atualização do jogo; não revisar, não alterar).
- **9 skills `sem-explicacao`** — omissão **por design** (sorteio de resultado): `Aid`,
  `Benevolence`, `Chaos Touch`, `Harm`, `Helping`, `Hurting`, `Malevolence`, `Touch of Chaos`
  (Chaos) + `Coin of Chaos` (Shadow).
- **19 buffs `sem-explicacao`** — marcadores de quest/teste/sorteio sem descrição útil:
  `Chaos Coin`, `Dwarf Rage!`, `Fate`, `Hunger for Vengeance`, `Shadow-Drenched Heart`,
  `Test Event Status - Boss Event/Critical Success/Success/Test Key`, `Test Fortune`,
  `The Animator - Quest Accept`, `The Mad Mage - Part 1/2/4/5`, `Treasure of Moltendunn`,
  `Ymir Rune, Courage/Honor/Strength`.
- **113 itens `sem-explicacao`** — `Commodity`/`Material`/`Tool` **sem texto no asset** (inertes;
  nada a explicar).
- **23 `indeterminado`** (revisados, ponto aberto **registrado sem inventar**): 19 buffs
  (`Anthulk Carapace`, `Burning Demon Hearts`, `Champion of Blood`, `Decay Shrine Aura`,
  `Elixir of the Scarlet Ox`, `Everlasting Sacrifice`, `Frenzy`, `Oculus Gem`, `Phoenix Feather`,
  `Poison Thorns`, `Ruby of Rancor` ×2, `Rune of Refreshment`, `Shapeshift: Black/Blue/Green/Red/White
  Dragonkin`, `Transcendence`), 3 debuffs (`Anthulk Venom` ×2 — o "Stacks up to N" mora em
  `ActionStatusInfo.MaxStacks`, que o dump não exportava à época — e `Curse of Death` — o efeito
  de expirar não está em campo nenhum) e 1 item (`Anthulk Shell` — o rótulo `{SKL=Ankheg Spines}`
  não corresponde a nenhum asset).
- **Decisão adiada (RV-8b-2d):** 67 textos de skill terminam com espaço — invisível no tooltip;
  aparar tem risco de colar palavras em texto concatenado. Fica como está até aparecer efeito.
- **Escopo declarado fora do censo (§7):** tutoriais/mensagens de sistema, strings de UI,
  texto de quests/eventos fora dos status, e descrições de ação — não têm dump; "cobertura total"
  vale para as 5 categorias do censo.

## 6. As pendências, uma a uma (com motivo)

### 6.1 Os 34 `pendente` reais — todos em `status.csv`

**Motivo comum:** são as linhas que a classificação automática de benefício (`IsBeneficial`/
`IsHarmful` → coluna `beneficio`) **não marcou como `Buff` nem `Debuff`** — `?` (15) ou `Neutro`
(19). Como os dois lotes do RV-9 foram exatamente "os 133 `Debuff`" e "os 393 `Buff`", estas 34
ficaram fora de ambos; são a fila "**Quest/Fortune/resto**" prevista no plano original do RV-9
(estão no censo, com texto completo, esperando o mesmo processo dos outros lotes). Não há
bloqueio de ferramenta: é trabalho do mesmo tipo já feito.

| nome | tipo | raridade | beneficio | descrição (resumida) |
|---|---|---|---|---|
| `Berserker's Rage` | Normal | Common | ? | Increases Damage and Damage Taken by 25%. Increases max life by 15%. |
| `Blackbeard's Curse` | Normal | Common | ? | Protected by Blackbeard's Chest. Invulnerable. |
| `Blood Mist` | Normal | Common | Neutro | Applies Bleeding to enemies in range. |
| `Bounty Hunter's Mark` | Normal | Common | ? | Chance of suffering critical strikes increased by 8%. Damage taken increased by 15%. |
| `Brawler's Brew` | Fortune | Rare | ? | @Might@ increased by {12,60}. Applies @Blind@ at the start of your turn. |
| `Burning Aura` | Normal | Common | Neutro | *0 fire damage dealt to enemies within the aura. |
| `Burning Aura` | Normal | Common | Neutro | [0] fire damage dealt to enemies within the aura. |
| `Chained` | Normal | Common | Neutro | Cannot move. |
| `Chilling Aura` | Normal | Common | Neutro | Deals *0 cold damage per turn while in the aura. |
| `Cupid Shot` | Normal | Common | Neutro | Charmed |
| `Dwarf King's Rage` | Normal | Common | ? | Increases damage dealt by 10%. |
| `Edwin's Enchantment` | Normal | Common | ? | Damage and healing increased by 50%. Max Health reduced by 50%. |
| `Edwin's Enchantment` | Fortune | Rare | ? | Power for mana use increased by {25,50}%. Mana costs are now paid in Health instead. |
| `Emperor's Blessing` | Normal | Common | ? | Max Health, Max Mana and Damage increased by 10%. |
| `Freeze Earth` | Normal | Common | Neutro | Applies 1 stack of Chilled. |
| `Frost Nova` | Normal | Common | Neutro | Immobilized. |
| `Ignite` | Normal | Common | Neutro | Targets in burning ground receive *0 fire damage. |
| `Immortal Night` | Normal | Common | Neutro | @Maximum health@ and @maximum mana@ lowered by 25% per stack. |
| `Marked Prey` | Normal | Common | Neutro | Damage taken increased by 10% per stack. |
| `Mind Blossom` | Normal | Common | Neutro | Charmed |
| `Pirate's Rum` | Fortune | Legendary | ? | Increases @Damage Reduction@ by {5,20}%. |
| `Raise Skeletal Lackey` | Normal | Common | Neutro | Provides invulnerability to all allies. |
| `Raise Skeletal Lackey` | Normal | Common | Neutro | Max Health, Damage, Armor, and Dodge Chance reduced by 50%. |
| `Rune of Exploding` | Normal | Common | Neutro | *(descrição vazia)* |
| `Slow Poison Aura` | Normal | Common | Neutro | Applies bleeding to enemies in range. |
| `Slow Poison Aura` | Normal | Common | Neutro | Slows and applies poison to enemies in range. |
| `Stalker's Mark` | Normal | Common | ? | Chance of suffering critical strikes increased by 12%. Damage taken increased by 25%. |
| `Stoney Visage` | Normal | Common | Neutro | Enemies gain 1 stack of Petrification when hitting Medusa. |
| `Tadashi's Armor` | Normal | Common | ? | Absorbs the next attack. |
| `Tadashi's Ritual` | Normal | Common | ? | Health cannot drop below 1. |
| `Tracker's Mark` | Normal | Common | ? | Chance of suffering critical strikes increased by 8%. Damage taken increased by 15%. |
| `Vengeful Shadows` | Normal | Common | Neutro | Attackers take [0] shadow damage. |
| `Warrior's Blade` | Normal | Common | ? | Damage increased 50%. |
| `Witch's Brew` | Normal | Common | ? | Recovery reduced by 30%. |

Notas de leitura: dois pares de assets homônimos entram na lista com textos diferentes
(`Burning Aura`, `Slow Poison Aura`, `Raise Skeletal Lackey` — analisar por asset, como manda a
regra); `Rune of Exploding` tem descrição vazia no asset; vários são buffs/auras **de inimigo**
(`Stoney Visage` cita a Medusa, `Raise Skeletal Lackey` etc.) e vários entram por **item**
(`Tadashi's`, `Edwin's`, poções de Fortune) — o processo não muda, muda só a fonte da prova.

### 6.2 Propagação dos vereditos para as colunas `status`/`revisao` dos CSVs

Mecânica e sem risco (o `census.py` preserva a coluna na regeneração): gravar nas 6 categorias
os vereditos já existentes (os mesmos que esta auditoria leu dos JSON/workfiles). É o passo que
faz o critério literal do ticket ("nenhum item do censo sem status") ficar cumprido **na
planilha**, fechando também o registro do RV-9 ("457 Normal" → 426/457, §3).

### 6.3 Escopo do RV-12 ainda sem censo

`quests/eventos` (além dos 20 status `Quest`/`QuestItem`, revisados), `tutoriais/mensagens`,
`strings de UI` e `descrições de ação` **não têm dump** — declarado no próprio
`docs/cobertura/README.md` ("O que este censo AINDA não cobre"). O RV-12 fechou os 79 níveis de
powerup; para o resto, o primeiro passo continua sendo criar o dump (patch no
`OptionsManager.Localize`, como foi feito para as 5 categorias).

### 6.4 Outras tarefas abertas que tocam tooltips (para contexto; fora do "X de X")

`RV-6` (varredura anti-redundância de estilo — `ready`), `RV-17` (formato das notas: falta a
conferência visual), `RV-18` (25 notas com valor lido em runtime), `RV-19`/`RV-20` (shrines),
`BUG-30` (dado dos eventos), `BUG-31` (nota do Endurance/Consumption em chave compartilhada),
`BUG-32` (varredura de chave compartilhada). RV-15 (notas redundantes) fechou **0 de 200**.

### 6.5 Conferência humana em jogo (sempre pendente por definição)

O passo 5 do `release-check`/do ritual: os itens 5.1–5.5 (cor/fonte das notas, texto no fim do
tooltip, ficha do BetterStats, renderização do BetterFont, partida real) e a **tabela A** do
`REVISAR-AO-FINAL.md` (áreas/raios que o dump não alcança: `Cyclone Kick`, `Detonate`, `Meteor`,
`Frost Nova`, `Volley`, `Frost Breath`, `Thunder Blast`). Nenhum deles é falha de cobertura —
é o olho humano que script nenhum substitui.

## 7. Limitações desta auditoria (honestidade de método)

1. **Não abri o jogo** (regra da tarefa): a "conferência de instalação" usou hash da DLL,
   execução do `check_dupes`/`check_fix_keys` de hoje e o `LogOutput.log` da última sessão — é
   evidência forte, mas a conferência visual continua sendo o passo 5 do release-check.
2. **A citação "4.319 textos"** (RV-16, no quadro) **não se reproduz** a partir dos artefatos
   atuais: nenhuma combinação simples das contagens por coluna dos CSVs soma 4.319. As métricas
   reproduzíveis: **2.280 linhas** nas 5 categorias; 3.832 células não-vazias de `nome`+`descrição`
   (4.450 somando `efeitos`); 20.629 células não-vazias no total dos 8 CSVs. O denominador desta
   auditoria é 2.280 — se o número do quadro vier de outra definição de "texto", registrar qual.
3. **O lote de debuffs do RV-9 não tem JSON de vereditos** (só o de buffs): os números
   (7 correções + 34 notas + 3 indeterminados + 89 revisados) vêm da mensagem do commit
   `fc28b00` e do KANBAN; o dos buffs (287/60/19/19/8) vem do JSON, que é a fonte forte.
4. **`acoes.csv` (276) e `invocacoes.csv` (18)** são **corpora de apoio**, não tooltips: 100%
   das descrições são vazias no asset (0 não-vazias em ambos — confirmado por script). Vieram
   para viabilizar a verificação das skills (fórmula de dano e comportamento de invocação) e
   nunca foram um checklist de tooltip; `skills-detalhe.csv` (453) é companheiro idem, sem
   coluna `status`. Não entram no "X de X" — coerente com o RV-16, que fala em "5 corpora".
5. Contagens por script lido com o módulo `csv` (aspas/quebras dentro de campos respeitadas);
   scripts desta auditoria em `scratch/` (gitignored): `rv13_count.py`, `rv13_cov.py`,
   `rv13_lists.py`, `rv13_lists2.py`, `rv13_recon.py`, `rv13_4319*.py`.

## 8. Critério de pronto do ticket — como está

| critério | estado |
|---|---|
| "Nenhum item do censo sem status" | **parcial**: 451/451 skills marcados; 5 categorias (2.123 linhas) com coluna não propagada (§6.2) e 34 status sem veredito (§6.1) |
| "Relatório final com contagem" | **cumprido por este documento**: **2.246 de 2.280 cobertas** (2.215 de 2.249 revisáveis) |
| "Lista das exceções conscientes" | **cumprida**: §5 (Bard 31, sem-explicação 141, indeterminados 23, decisão adiada do espaço final) |
| "Registrar no quadro" | **fora desta tarefa** (auditoria read-only): anotar o número no `KANBAN.md`/kanban ao fechar |

---

*Fontes usadas: `docs/cobertura/*.csv` (os 8), `docs/cobertura/README.md`,
`docs/cobertura/revisao/` (workfiles RV-9, relatórios RV-8b/RV-9/RV-14/RV-15, `REVISAR-AO-FINAL.md`,
`omissoes.md`), `scratch/rv9-buffs-vereditos.json`, `scratch/rv10-12-vereditos.json`,
`BetterTooltips/Patches/LocalizePatch.cs`, `git log` do repositório, `LogOutput.log` do perfil
r2modman (Default) e execução de `tools/check_fix_keys.py` e `tools/check_dupes.py`.*
