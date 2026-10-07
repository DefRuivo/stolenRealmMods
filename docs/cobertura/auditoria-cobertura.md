# Auditoria de cobertura das tooltips — RV-13 (fechamento "X de X")

> **Pergunta que este documento responde:** *"revisar tudo — sobrou alguma?"*
> **Data:** 03/10/2026 · HEAD `3eefd5a`.
> **Escopo:** as **5 categorias do censo do RV-7** (`skills`, `status`, `itens`, `afixos`,
> `powerups` = **2.280 linhas**). Método: **contagem por script** (`csv` do Python — aspas e
> quebras dentro de campos respeitadas; nunca a olho). **Nenhuma CSV do censo foi alterada.**
>
> **Método do passo de reprocessamento:** o censo **não foi reprocessado pelo dump** nesta
> rodada — `tools/census.py` **reescreve os 5 CSVs** a partir do `LogOutput.log` do
> RoguelikeDebugger, e a regra da tarefa proíbe tocar nas CSVs do censo. A apuração usou
> `python tools/censo_status.py` (roda sem dump, preserva a coluna) + leitura direta das CSVs
> já geradas + os vereditos-fonte em `scratch/`. Registrado em §6.

---

## 1. Veredito — o número final

## **2.280 de 2.280 entradas com veredito (100%). 2.249 de 2.249 revisáveis.**

As **2.249 revisáveis** = 2.280 − **31 `intocavel`** (árvore Bard, fora de escopo por regra do
projeto). **Zero `pendente` em qualquer das 5 categorias.**

| Categoria (arquivo) | Total | revisado¹ | corrigido | sem-explicacao | intocavel | indeterminado² | pendente | Coberta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Skills / spells (`skills.csv`) | 451 | 309 | 102 | 9 | 31 | 0 | **0** | 451/451 |
| Status / efeitos (`status.csv`) | 560 | 517 | 20 | 21 | 0 | 2 | **0** | 560/560 |
| Itens base (`itens.csv`) | 905 | 782 | 9 | 113 | 0 | 1 | **0** | 905/905 |
| Afixos de item (`afixos.csv`) | 285 | 277 | 8 | 0 | 0 | 0 | **0** | 285/285 |
| Powerups (`powerups.csv`) | 79 | 79 | 0 | 0 | 0 | 0 | **0** | 79/79 |
| **TOTAL** | **2.280** | **1.964** | **139** | **143** | **31** | **3** | **0** | **2.280/2.280** |

¹ `revisado` soma `revisado` + `nota` (nota = "texto mantido, explicação anexada" — mesma
convenção já usada no `skills.csv`). ² `indeterminado` = **revisado**, com o ponto aberto
**nomeado e localizado** (não é pendência nem chute) — lista em §2.

Conferência aritmética: `1.964 + 139 + 143 + 31 + 3 = 2.280`. Revisáveis = 2.280 − 31 =
**2.249**, todas com veredito.

---

## 2. Itens sem status (o que "sobrou")

**Nenhum item está em branco, com status desconhecido ou `pendente`.** Uma linha/valor por
script acha zero lacunas. O que existe são **3 linhas com veredito ABERTO** (`indeterminado`),
no sentido com que o projeto usa o termo: revisadas, com o ponto em aberto **registrado sem
inventar prova**:

| arquivo | nome | tipo | o que ficou aberto |
|---|---|---|---|
| `status.csv` | `Champion of Blood` | Normal/Common | "Striking enemies heals the Countess for 10% of her Max Health." — valor sem campo que o censo leia |
| `status.csv` | `Frenzy` | Normal/Common | "Action Points Increase by 1." — ponto aberto registrado no fechamento do RV-13b |
| `itens.csv` | `Anthulk Shell` | Shield/Mythic | rótulo `{SKL=Ankheg Spines}` não corresponde a nenhum asset |

Nenhum deles volta para a fila por falta de ferramenta: são **decisões registradas**. Se o dono
quiser zerar os 3, o próximo passo é explicitamente uma chamada: exportar o campo que falta (o
`MaxStacks`/`Duration` já foram exportados no commit `7b8500d`) ou conferir **em jogo**.

---

## 3. Reconciliação com as checklists RV-8..RV-12

Os vereditos de cada lote foram gravados nos artefatos-fonte e **propagados às CSVs**. A
conferência abaixo casa os números das fontes com a coluna `status`/`revisao` do censo:

**Itens + afixos + powerups — match EXATO (fonte: `scratch/rv10-12-vereditos.json`, 1.269 entradas):**

| veredito na fonte | nº | virou na CSV (`revisado`+`nota` somados) | nº |
|---|---:|---|---:|
| `revisado` + `nota` | 1.067 + 71 = **1.138** | `revisado` (itens 782 + afixos 277 + powerups 79) | **1.138** ✓ |
| `corrigido` | **17** | `corrigido` (9 + 8 + 0) | **17** ✓ |
| `sem-explicacao` | **113** | `sem-explicacao` (itens) | **113** ✓ |
| `indeterminado` | **1** | `indeterminado` (itens) | **1** ✓ |

**Status — cadeia de fechamentos (buffs JSON + commit `e452bc6` + RV-13b + `88acc70`):**

- buffs (`scratch/rv9-buffs-vereditos.json`, 393) + debuffs (133, commit `e452bc6`) = **526** →
  `revisado 470 · corrigido 15 · sem-explicacao 19 · indeterminado 22` (números do RV-13 §3);
- + as **34** da fila `?`/`Neutro` fechadas no RV-13b (`revisado 29 · corrigido 4 · sem-exp 1`);
- + as **14 indeterminadas** fechadas pelo texto do asset no commit `88acc70` (`revisado +13 ·
  corrigido +1`) → **`revisado 517 · corrigido 20 · sem-explicacao 21 · indeterminado 2` = 560**.

**Skills —** coluna `status` do `skills.csv` sempre foi a checklist mantida (RV-8):
`revisado 309 · corrigido 102 · sem-explicacao 9 · intocavel 31 = 451`.

> As colunas `status` e `revisao` do `status.csv` estão **idênticas em 560/560 linhas** (0
> divergência) — as duas ferramentas leem colunas diferentes, mesma convenção desde `05c05a4`.

---

## 4. Exceções conscientes (decisões, não pendências)

1. **Árvore Bard — 31 skills `intocavel`** (regra do projeto: o conteúdo chega na próxima
   atualização do jogo; não revisar, não alterar). São 31 de 451 skills.
2. **143 linhas `sem-explicacao`** — omissão **por design**:
   - **9 skills** (sorteio de resultado): `Aid`, `Benevolence`, `Chaos Touch`, `Coin of Chaos`,
     `Harm`, `Helping`, `Hurting`, `Malevolence`, `Touch of Chaos`;
   - **21 status** (marcadores de quest/teste/sorteio + descrição vazia): `Chaos Coin`,
     `Dwarf Rage!`, `Fate`, `Hunger for Vengeance`, `Rune of Exploding`, `Shadow-Drenched Heart`,
     `Test Event Status - Boss Event/Critical Success/Success/Test Key`, `Test Fortune`,
     `The Animator - Quest Accept`, `The Mad Mage - Part 1/2/4/5`, `Treasure of Moltendunn`,
     `Ymir Rune, Courage/Honor/Strength`, `Burning Demon Hearts`;
   - **113 itens** — `Commodity` 66 / `Material` 46 / `Tool` 1 **sem texto no asset** (110 de 113
     com descrição vazia; os 3 com texto — `Gold Statue Arm/Head/Torso` — são flavor de troféu,
     não mecânica). Nada a revisar.
3. **3 linhas `indeterminado`** (§2) — revisadas com ponto aberto registrado.
4. **Decisão adiada (RV-8b-2d):** 67 textos de skill terminam com espaço — invisível no tooltip;
   aparar tem risco de colar palavras em texto concatenado. Fica até aparecer efeito.
5. **Escopo fora do censo (RV-12):** tutoriais/mensagens de sistema, strings de UI, texto de
   quests/eventos fora dos status e descrições de ação — **não têm dump**. "Cobertura total"
   vale para as **5 categorias do censo** (declarado no `README.md`).
6. **Corpora de apoio, NÃO tooltips (fora do "X de X"):** `acoes.csv` (**276**, todas
   `pendente`) e `invocacoes.csv` (**18**, todas `pendente`) — **100% das descrições são vazias
   no asset** (0 não-vazias; `invocacoes` nem tem coluna `descricao`). Existem para viabilizar a
   verificação das skills (fórmula de dano / comportamento de invocação); nunca foram checklist
   de tooltip. `skills-detalhe.csv` (453) é companheiro idem, sem coluna de status.

---

## 5. Aguarda verificação em jogo do dono (GATE HUMANO do passo 3 — NÃO executado aqui)

Sou auditoria de cobertura: **não rodo o jogo, não instalo mod**. Fica explicitamente **aguardando
o dono conferir NO JOGO** que as correções estão instaladas de fato — é o único item não
automatizável (passo 5 do `release-check`):

- **Passo 5 do release-check:** cor/fonte das notas, texto no fim do tooltip, ficha do
  BetterStats, renderização do BetterFont e uma partida real;
- **Tabela A do `REVISAR-AO-FINAL.md`** (áreas/raios que o dump não alcança): `Cyclone Kick`,
  `Detonate`, `Meteor`, `Frost Nova`, `Volley`, `Frost Breath`, `Thunder Blast`;
- **Rótulo `Holy` × `Divine`** na ficha de personagem (pendência honesta do RV-14);
- **Os 3 `indeterminado`** (§2), se o dono quiser fechá-los por observação direta;
- **`Resist Divine` → `Resist Holy`** na ficha e num item com afixo de resistência (RV-13
  renomeação, já aplicado no código — falta o olho humano).

Nenhum desses é falha de **cobertura**: todos têm veredito registrado; falta só a confirmação
visual do dono.

---

## 6. Limitações e método (honestidade)

1. **Censo NÃO reprocessado pelo dump** nesta rodada: `tools/census.py` reescreveria os 5 CSVs, e
   a tarefa proíbe alterá-los. Usei `tools/censo_status.py` (roda sem dump e **preserva** a
   coluna) + leitura das CSVs já geradas + os JSON de vereditos em `scratch/`. O dump do
   RoguelikeDebugger existe (`…/StolenRealm/profiles/Default/BepInEx/LogOutput.log`), então
   reprocessar é possível — só não foi feito por regra desta tarefa.
2. **Não abri o jogo** (§5).
3. Contagens por **script** (`csv` do Python), cara a cara com o `README` do RV-7 (2.280 = 451 +
   560 + 905 + 285 + 79). Zero linha em branco/desconhecida e zero `pendente` nas 5 categorias.
4. Os números por categoria **mudaram desde o `RV-13-auditoria-cobertura.md` (30/09, 2.246/2.280)
   e o `RV-13b-fechamento.md` (indeterminado 16)** — porque os vereditos foram propagados
   (commits `ac5b0af`, `7298a94`, `88acc70`). Este documento lê o **estado atual (HEAD
   `3eefd5a`)**.

*Fontes: `docs/cobertura/*.csv` (os 8), `docs/cobertura/README.md`, `docs/cobertura/revisao/`
(`RV-13-auditoria-cobertura.md`, `RV-13b-fechamento.md`, `RV-9-censo.md`, `REVISAR-AO-FINAL.md`),
`scratch/rv9-buffs-vereditos.json`, `scratch/rv10-12-vereditos.json`, execução de
`tools/censo_status.py`, `git log` (`ac5b0af`, `7298a94`, `88acc70`).*
