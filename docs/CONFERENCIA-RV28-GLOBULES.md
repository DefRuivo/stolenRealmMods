# Pacote de conferência visual humana — RV-28 (globules)

> **O que é este arquivo.** É o pacote que permite a **uma pessoa** fazer a conferência visual do
> `RV-28` (cura dinâmica de vida/mana no tooltip do globule, pelo `Sustenance I/II`) **em uma sessão
> de jogo**, sem ler código: a lista final do que entrou, o caminho até a tooltip de cada membro, a
> matriz com o valor esperado, as tabelas para marcar **OK/NOK** e as referências de prova do que já
> está provado por execução.
>
> **Irmão deste arquivo:** `docs/CONFERENCIA-DONO-06-10.md` §5 é o resumo deste mesmo teste dentro da
> sessão única de cinco conferências; aqui é a versão detalhada, com as tabelas de registro.
>
> **Tempo estimado:** 10 min de preparação + a sessão de jogo. Os quatro cenários saem na mesma
> batalha quando a party tem um personagem em cada estado (sem `Sustenance` / só a I / só a II) — na
> prática eles vêm na ordem em que as tiers são aprendidas; caçar os 12 membros é o que leva tempo
> (§2.4).

Data do pacote: **06/10/2026**. Módulo conferido: `BetterTooltips` **0.1.3**.

---

## 0. Pré-condições (conferir antes de abrir o jogo)

| # | O que conferir | Como | Esperado |
|---|---|---|---|
| 0.1 | O jogo abre **modado** | r2modman → **Start modded** (o `.exe` direto roda vanilla) | o jogo abre com os mods |
| 0.2 | O BetterTooltips carregou | no `LogOutput.log` (caminho em 0.4), procurar `Loading [Better Tooltips 0.1.3]` | a linha existe |
| 0.3 | Os ganchos Harmony entraram | mesma busca: `BetterTooltips: patches Harmony aplicados (` | **`(8/8 ganchos, 8 metodos de patch)`** — N diferente = primeiro achado da sessão |
| 0.4 | Onde está o log | `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\LogOutput.log` | — (o arquivo é **truncado a cada boot**: só vale a sessão atual) |
| 0.5 | Os tooltips de ground effect estão ligados | Options → Gameplay → a opção de tooltip de ground effect (a mesma que esconde a descrição de barris) | **ligada** (é o padrão; desligada, nenhuma tooltip de globule aparece — `Tooltip.cs:1221`) |
| 0.6 | A DLL instalada é a que tem o RV-28 (opcional) | `python -c "import os;b=open(os.path.expandvars(r'%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\BetterTooltips\BetterTooltips.dll'),'rb').read();print(b.count('[Globule RV-28]'.encode('utf-16-le')))"` | **`2`** — a marca do log existe dentro da DLL instalada. **Confira por este marcador, não por sha256**: a árvore tem WIP de outras frentes e a DLL é recompilada/reinstalada a cada build (o sha256 muda de um build para o outro sem que o conteúdo do `RV-28` mude) |
| 0.7 | Um personagem **Chaos** na party | `Sustenance I/II` são passivas **Chaos** tier 1/2 (`skills.csv:401-402`); `Magic Hat III` (o que cria globule) é Chaos tier 4 (`skills.csv:243`) | um Chaos cobre as duas coisas; a party pode ter 4 personagens |

> ⚠ **O número é do personagem SELECIONADO, não do que está sob o cursor.** No tooltip de ground
> effect o receptor é o `TooltipCharacter` = `GameLogic.instance.CurrentlySelectedCharacter`
> (`ShrineAuraPatch.cs:552-590`) — é por isso que trocar de personagem muda o número, e é assim que
> se testa o cenário "sem Sustenance" (selecione um personagem que não tem a skill).

---

## 1. A lista final: quem recebeu o número e quem ficou fora

Os seis nomes abaixo são os **nomes de exibição** do jogo (o título do tooltip), medidos byte a byte
no asset — não são nomes normalizados nem inventados. A família foi fechada por varredura exaustiva
da palavra em **todos** os dados do jogo (324 ocorrências em `resources.assets`, zero nos outros
assets), e o argumento completo está em `docs/cobertura/rv28-globules.md` §2-§3.

### 1.1 Os SEIS globules — todos recebem o número

| Membro (título no tooltip) | Descrição que a tooltip mostra (é a chave do mod) | Efeito real | Número dinâmico? |
|---|---|---|---|
| `Health Globule` | `Heals for 50% of Max Health` | cura 50% da vida | **SIM** |
| `Mana Globule` | `Restores 50% of Max Mana` | restaura 50% da mana | **SIM** |
| `Cleansing Globule` | `Cleanses all debuffs` | limpa debuffs | **SIM** |
| `Energy Globule` | `Grants an additional Action Point` | +1 ponto de ação | **SIM** |
| `Refreshing Globule` | `Lowers Cooldowns by 1` | −1 de cooldown | **SIM** |
| `Power Globule` | `Increases all damage by 10%` (do ground effect) | buff: +10% de dano (não cura) | **SIM** — decisão em §1.3 |

### 1.2 Os SEIS pickups de poção (mesma regra, frente `RV-32`)

Não são "globules" pelo nome, mas são `GroundEffectType.Pickup` — o **mesmo gatilho** — e o tooltip
deles ganha a mesma cura, com o sujeito certo ("**Picking this up** also heals you for …"):

`Minor Healing Potion` / `Healing Potion` / `Major Healing Potion` (`Restores 10% / 15% / 20%
health`) e `Minor Mana Potion` / `Mana Potion` / `Major Mana Potion` (`Restores 10% / 15% / 20%
mana`).

### 1.3 O que ficou FORA (e por quê)

| Candidato a exclusão | Decisão | Justificativa |
|---|---|---|
| **`Power Globule`** (o único candidato real: é buff de dano, não cura) | **ENTRA** | o que cura é o `Sustenance`, e o texto dele no asset é literal: *"Consuming any Globule heals you for 8%/20% of max life and mana."* — o sujeito é **qualquer** globule. Deixá-lo fora seria uma lacuna visível: o jogador consome um `Power Globule`, recebe cura real, e só o tooltip dele não explica de onde veio. A implementação cobre as **duas** descrições possíveis dele (`GlobulePatch.cs:70-78`) |
| Textos que apenas **citam** globule: `Produce a random Globule on the target hex.` (`Magic Hat III`, `skills.csv:243`), `Power Globule Status` (`status.csv:370`, o **status** aplicado, não um pickup), nomes de prefab/efeito (`Cleansing/Energy/Power/Refreshing Globule Pickup`/`… End`) e as **traduções** FR/PT | **fora** | não são tooltips de um globule no chão: são a skill que o cria, o status que ele aplica, nomes internos de prefab e traduções. Nenhum deles é um membro novo da família (`docs/cobertura/rv28-globules.md` §2.1) |

**Nenhum dos seis membros da família foi excluído.** As **7 chaves** que o mod cobre para os 6
globules estão em `GlobulePatch.cs:70-78`; as 6 das poções, em `GlobulePatch.cs:93`.

> **Efeito colateral declarado (não é defeito).** A chave `Increases damage and summon damage by 10%`
> é a descrição do **status** `Power Globule` — a mesma que a nota do `RV-9` já enriquece
> (`LocalizePatch.cs:1570-1571`). Como o mod age na localização da chave, a frase do `Sustenance`
> também aparece **no tooltip do buff** `Power Globule` no personagem (por exemplo ao passar o mouse
> no ícone do buff). É o mesmo texto, o mesmo dono — registre na tabela C (§4.3) o que viu.

---

## 2. Passo a passo no jogo: chegar à tooltip de cada globule

### 2.1 De onde os globules vêm (três caminhos, todos reais)

1. **Morte de inimigo** — quem morre pode largar um pickup no próprio hex, com a chance
   `Character.BattleDropChance` (`scratch/sac1/Character.cs:12730`, dump por tipo do decompilado).
2. **Lote por turno** — a partir do **turno 4** e **a cada 4 turnos**, nasce um lote de pickups em
   hexes vazios a até 10 hexes de um personagem da party (`scratch/sac1/BattleManager.cs:132-136` e
   `:157-164`). O **tamanho do lote depende do tamanho da party** (`:161`) → **party cheia = mais
   drops por lote**.
3. **`Magic Hat III`** (Chaos, tier 4, `skills.csv:243`) — *"Produce a random Globule on the target
   hex."*: é o **único jeito de pedir um globule na hora**, sem esperar sorte de drop.

Qual membro sai é **sorteio** sobre o array `BattleDrops` (`scratch/sac1/BattleManager.cs:216`, e
`:130` é o campo) — a composição exata desse array não é legível byte a byte (limite declarado em
`docs/cobertura/rv28-globules.md` §7.3). Por isso: **nenhum membro tem endereço fixo**; o que o
pacote garante é o caminho até o hex e a leitura do resultado.

### 2.2 O passo a passo

1. Abrir o jogo pelo r2modman (**Start modded**) e cumprir §0.
2. Entrar/continuar uma **run** do modo roguelike com um personagem **Chaos** na party.
3. Numa **batalha**, gerar globules: matar inimigos (caminho 1), passar o turno (caminho 2, a partir
   do turno 4) e/ou conjurar **`Magic Hat III`** num hex livre (caminho 3).
4. **Parar de mover/agir** (com o personagem se movendo ou a câmera girando, o hover é ignorado —
   `scratch/sac1/HexCellManager.cs:239`).
5. Passar o mouse **sobre o hex do globule** (o pickup brilha no chão). A tooltip abre
   (`scratch/sac1/HexCellManager.cs:306` → `Tooltip.ShowGroundEffectTooltip`).
6. Ler o **título** (é o nome do membro: `Health Globule`, …) e o **corpo** (a descrição + a frase do
   `Sustenance`) — §3 traz o texto esperado linha por linha.
7. **Registrar** na tabela B (§4.2): membro, estado das skills naquele momento, o que apareceu,
   OK/NOK e observação.
8. Para o número mudar: **selecionar outro personagem** (o número é do selecionado — §0) ou mudar a
   ficha dele (§3.1, cenário 5) e reabrir a tooltip.
9. Ao final: ler as marcas do log (§5), que são o lado objetivo do mesmo teste.

### 2.3 Como saber o que estou vendo (e de quem é o número)

- **Título** = nome do membro (o jogo localiza o `Name` do `GroundEffectInfo` — `scratch/sac1/Tooltip.cs:1243`).
- **Corpo** = a **descrição** do ground effect (`scratch/sac1/Tooltip.cs:1245`); é nela que o mod
  anexa a frase. Depois vem `Turns Remaining: N` (`scratch/sac1/Tooltip.cs:1254`).
- **O número é do personagem selecionado** no HUD, não do que está sob o cursor (§0).

### 2.4 Aceleradores (para caber em uma sessão)

- **Party cheia** (4) → lotes maiores por turno (`BattleManager.cs:161`).
- **Batalhas com muitos inimigos** → mais mortes, mais drops na morte.
- **`Magic Hat III`** → um globule por conjuração, à vontade (cooldown/pontos de ação à parte).
- **Passar turnos numa batalha longa** → um lote novo a cada 4 turnos, sem gastar nada.
- Se um membro específico não aparecer: continuar na batalha seguinte (a lista é a mesma, o sorteio é
  que muda).

### 2.5 Se um membro não aparecer nesta sessão (protocolo honesto)

Marque a linha com **`nao sorteado`** na coluna OK/NOK, registre quantos lotes/conjurações você fez e
**não** invente o resultado. A cobertura de cada membro já está provada no fonte e nos testes (§6) —
o que a conferência acrescenta é a **prova de tela**. Um membro não sorteado deixa a linha pendente,
não reprovada.

---

## 3. A matriz de aceite, preenchida (o exemplo do dono: **100 de vida / 200 de mana**)

A frase sai do motor do mod assim (`GlobulePatch.cs:190-199`): `Consuming a Globule also heals you
for **<%>**% of your Max Health and Max Mana (**<tiers ativas>**): **<vida×%>** health and
**<mana×%>** mana with your current pools.` — nos pickups de poção, o começo é `Picking this up also
heals you for …`. Formatação: **uma casa decimal quando não é inteiro** (`46.6 health` para 233 de
vida a 20%); o caso 100/200 sai inteiro.

### 3.1 Os quatro cenários do cartão

| # | Cenário | Esperado na tooltip (100/200) | Prova |
|---|---|---|---|
| 1 | **sem `Sustenance`** (personagem selecionado sem nenhuma tier) | **nenhuma frase nova** — só a descrição do globule | `GlobulePatch.cs:176` (sem tier → devolve `""`); marca no log (§5) |
| 2 | **`Sustenance I` ativa** | `...heals you for 8% ... (Sustenance I): 8 health and 16 mana with your current pools.` | teste puro `t_rv28_globule_sustenance` (PASSOU); a % é a do motor em `acoes.csv:255` (`Target.MaxHealth * .08f`) |
| 3 | **`Sustenance II` ativa** | `...heals you for 20% ... (Sustenance II): 20 health and 40 mana with your current pools.` | idem, `acoes.csv:256` (`.20f`) |
| 4 | **vida/mana mudando** (equipar/desequipar item, power-up ou level-up) | o número **acompanha** a ficha: `MaxHealth/MaxMana` são lidos **no hover** (cache de ~1s) | `GlobulePatch.cs:182`; duas marcas com números diferentes no log (§5) |
| 5 | **as duas tiers aprendidas** (bônus do `RV-24`) | **o que o jogo tiver ativo**: `20%` (se a II substitui a I) **ou** `28%`/`56` (se as duas ficam ligadas) | o mod lê a lista ativa do jogo (`GlobulePatch.cs:232-246`), nunca soma por conta própria — `docs/cobertura/rv28-globules.md` §7.4 |

> ⚠ **O 8% × 20% × 28% é ponto aberto do `RV-24`** e **não é defeito** do que você vai ver: com uma
> tier ativa o número é 8/16 ou 20/40 (**nunca** soma a outra); com as **duas** ligadas, 28% é a
> resposta correta se o jogo mantiver as duas. Anote na observação **qual das duas apareceu** — é
> essa a medida que fecha a dúvida.

### 3.2 Por membro (o "em TODOS os globules identificados")

A frase esperada é **a mesma para os 12 membros** — o que muda é o título, a descrição base e (nos
globules de vida/mana) a leitura da ficha:

| Membro | Título na tooltip | Corpo base (antes da frase) |
|---|---|---|
| Health Globule | `Health Globule` | `Heals for 50% of Max Health` |
| Mana Globule | `Mana Globule` | `Restores 50% of Max Mana` |
| Cleansing Globule | `Cleansing Globule` | `Cleanses all debuffs` |
| Energy Globule | `Energy Globule` | `Grants an additional Action Point` |
| Refreshing Globule | `Refreshing Globule` | `Lowers Cooldowns by 1` |
| Power Globule | `Power Globule` | `Increases all damage by 10%` (se aparecer o texto do **status**, `Increases damage and summon damage by 10%`, a frase entra **dentro** da nota do `RV-9` — §1.3) |
| 6 pickups de poção (RV-32) | o nome do pickup | `Restores 10/15/20% health` · `Restores 10/15/20% mana` |

---

## 4. Checklist para preencher (é isto que volta para o quadro)

### 4.1 Tabela A — os 4 cenários do pedido

| # | Cenário | Esperado | O que a tooltip mostrou (copie o texto) | OK | NOK | Observação |
|---|---|---|---|---|---|---|
| A1 | sem Sustenance | sem número | | ☐ | ☐ | |
| A2 | Sustenance I | 8 health / 16 mana | | ☐ | ☐ | |
| A3 | Sustenance II | 20 health / 40 mana (ou 28/56 — §3.1) | | ☐ | ☐ | qual % apareceu? |
| A4 | pools variando | o número acompanha | medida 1: ______ / medida 2: ______ | ☐ | ☐ | item/power-up usado: |
| A5 | as duas tiers ativas | registrar a % (fecha o `RV-24`) | | ☐ | ☐ | |
| A6 | o resto da tooltip não mudou | título, descrição base e `Turns Remaining` intactos | | ☐ | ☐ | |

### 4.2 Tabela B — cobertura por membro (um linha por membro visto)

| # | Membro | Como apareceu (drop / lote / Magic Hat) | Estado das skills na hora | Esperado | Visto | OK | NOK | Observação |
|---|---|---|---|---|---|---|---|---|
| B1 | Health Globule | | sem / I / II | §3.2 | | ☐ | ☐ | |
| B2 | Mana Globule | | | §3.2 | | ☐ | ☐ | |
| B3 | Cleansing Globule | | | §3.2 | | ☐ | ☐ | |
| B4 | Energy Globule | | | §3.2 | | ☐ | ☐ | |
| B5 | Refreshing Globule | | | §3.2 | | ☐ | ☐ | |
| B6 | Power Globule | | | §3.2 / §1.3 | | ☐ | ☐ | |
| B7 | Minor Healing Potion | | | `Picking this up…` | | ☐ | ☐ | RV-32 |
| B8 | Healing Potion | | | `Picking this up…` | | ☐ | ☐ | RV-32 |
| B9 | Major Healing Potion | | | `Picking this up…` | | ☐ | ☐ | RV-32 |
| B10 | Minor Mana Potion | | | `Picking this up…` | | ☐ | ☐ | RV-32 |
| B11 | Mana Potion | | | `Picking this up…` | | ☐ | ☐ | RV-32 |
| B12 | Major Mana Potion | | | `Picking this up…` | | ☐ | ☐ | RV-32 |

### 4.3 Tabela C — colaterais que valem registrar

| # | O que observar | Esperado | Visto | OK | NOK |
|---|---|---|---|---|---|
| C1 | Tooltip do **buff** `Power Globule` no personagem (§1.3) | a frase aparece junto da nota do `RV-9`, no mesmo bloco | | ☐ | ☐ |
| C2 | Personagem **sem** `Sustenance` selecionado | nenhuma frase; o texto base sai igual | | ☐ | ☐ |
| C3 | Hover **fora do contexto de jogador** (inspeção/loja), se acontecer | o mod cai para "sem número", loga o motivo e o texto base fica intacto | | ☐ | ☐ |

### 4.4 Rastreabilidade (nenhum item do pedido sem linha)

| Item do pedido | Onde é conferido |
|---|---|
| lista final dos globules + quais receberam o valor + excluídos com justificativa | §1 (tabelas 1.1, 1.2, 1.3) |
| passo a passo de reprodução no jogo | §2 |
| matriz de aceite preenchida no exemplo 100/200 | §3.1 |
| sem Sustenance → sem número | **A1** |
| Sustenance I → 8 / 16 | **A2** |
| Sustenance II → 20 / 40 | **A3** |
| vida/mana variando → o número acompanha | **A4** |
| em **todos** os globules identificados | **B1-B6** (poções: B7-B12, `RV-32`) |
| espaço para OK/NOK por linha + observação | §4.1, §4.2, §4.3 |
| referências de prova do que já está provado | §6 |

---

## 5. As marcas do log (o lado objetivo do mesmo teste)

Caminho: `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\LogOutput.log` — **truncado
a cada boot**, então confira **na mesma sessão**. Para ver as marcas do `RV-28` (no git-bash):

```bash
grep -a "Globule RV-28" "$APPDATA/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log"
```

Formato das marcas possíveis (uma por combinação — o mod não repete a mesma linha; teto de 200):

| Marca | Significa | Corresponde a |
|---|---|---|
| `[Globule RV-28] '<descrição>': <personagem> nao tem Sustenance ativa -> sem numero` | o selecionado não tem a skill | **A1** / **C2** |
| `[Globule RV-28] '<descrição>': <personagem> <tiers> = <pct>% -> <frase>` | a frase saiu; `<tiers>` diz qual tier o jogo tem ativa | **A2, A3, A5, B1-B12** |
| `[Globule RV-28] sem numero: …` (personagem em foco, atributo ausente, pools zerados) | o mod caiu para "sem número" **por decisão explícita e logada** | **C3** |
| `[Globule RV-28] frase do Sustenance falhou (tooltip intacto): …` | erro inesperado; a tooltip fica **intacta** | **NOK** (achado) |

Notas para ler o log: (a) o `<personagem>` é o **selecionado** (§0); (b) o número na frase inclui a
vida/mana daquele hover — **duas marcas com números diferentes na coluna da frase** são a prova do
cenário **A4**; (c) se a marca não aparecer ao passar o mouse, o hover não chegou ao globule
(§2.2 passo 4) ou os tooltips de ground effect estão desligados (§0.5).

---

## 6. Referências de prova (o que já está provado, e onde)

| Afirmação | Prova |
|---|---|
| `Sustenance I` = 8% e `Sustenance II` = 20% de vida **e** mana, texto do asset | `docs/cobertura/skills.csv:401-402` |
| O **motor** aplica 8%/20% (`Target.MaxHealth * .08f` / `.20f`) | `docs/cobertura/acoes.csv:255-256` |
| O gatilho é `TriggerType.OnGlobulePickup`, disparado por **qualquer** `GroundEffectType.Pickup` | `scratch/sac1/TriggerType.cs:33` (`OnGlobulePickup = 30`) e `scratch/sac1/GroundEffect.cs:256-257` |
| O **próprio jogo** testa a fiação das duas tiers em `OnGlobulePickup` | `ChaosSkillTest.SustenanceI` / `SustenanceII` (`AssertTriggerWiring`), dump por tipo em `scratch/sac1/ChaosSkillTest.cs:4660` e `:4739`; no decompilado monolítico: **l.183433** e **l.183512** (os dois testes afirmam o **gatilho**, não o valor) |
| O texto base das duas tiers no mod (fix `max life` → `max health`, `RV-14`) | `BetterTooltips/Patches/LocalizePatch.cs:1487-1492` (⚠ o corpo do cartão citava `856-861`, que é **outra** entrada) |
| O número **não cria chave nova** (INC-1): é composto no postfix e anexado à nota da própria descrição | `BetterTooltips/Patches/LocalizePatch.cs:2775-2790`; decisão em `docs/cobertura/rv28-globules.md` §10 |
| As 7 chaves dos 6 globules e as 6 dos pickups de poção | `BetterTooltips/Patches/GlobulePatch.cs:70-78` e `:93` |
| O caminho do hover até a tooltip de ground effect | `scratch/sac1/HexCellManager.cs:306` → `scratch/sac1/Tooltip.cs:1219-1254` (título `:1243`, corpo `:1245`, `Turns Remaining` `:1254`); a opção que a desliga em `scratch/sac1/Tooltip.cs:1221` |
| O número é do personagem **selecionado** (precedente `RV-22`/`RV-50`) | `BetterTooltips/Patches/ShrineAuraPatch.cs:552-590` |
| De onde os globules vêm na run | `scratch/sac1/Character.cs:12730` (morte) e `scratch/sac1/BattleManager.cs:130, 132-136, 157-164, 216` |
| A família são **seis** (+ seis poções), com nome e descrição medidos no asset, e nenhuma delas troca o corpo por descrição de status | `docs/cobertura/rv28-globules.md` §2-§4; dump do instrumento em `scratch/vg1/out/groundeffects-do-jogo.json` (as 12 entradas com `statuses: 0` = o corpo é a `Description` do próprio ground effect) |
| As **guardas** do tooltip (assinatura explícita, try/catch com queda para sem número, atributo existe antes da leitura, alvo nulo, nunca somar tier I+II) | `BetterTooltips/Patches/GlobulePatch.cs:121` (`AtributoExiste`), `:143`, `:162`, `:176`, `:182`, `:204`, `:246`; §11 de `docs/cobertura/rv28-globules.md` |
| A matriz numérica 8/16 e 20/40 pasou, e 28/56 **não** aparece com uma tier ativa | `tools/testes/testes/puros/t_rv28_globule_sustenance.py` + `tools/testes/regras_rv28_globule.py`; **prova de fogo física** (4 defeitos plantados no fonte real, cada um reprovado pelo motivo certo e o arquivo restaurado byte a byte) em `tools/testes/rv28-globule-prova-de-fogo.py` e no log `tools/testes/rv28-globule-prova-de-fogo.log`; contra-prova em `tools/testes/contra-prova/cp_rv28_globule_soma_a_mao.py` e `cp_rv28_globule_ok.py` |
| O `Power Globule` **entra** na regra (é buff de dano, não cura) | decisão e leitura do asset em `docs/cobertura/rv28-globules.md` §4 |
| `8% × 20% × 28%` segue **indeterminado** para o Sustenance | `docs/cobertura/rv28-globules.md` §7.4 (ponto aberto do `RV-24`) |
| Precedente do valor dinâmico no tooltip (shrine) | `RV-22`/`RV-24` — `docs/cobertura/revisao/RV-19-shrines.md` (nota do Dwarven, `Source` do receptor) |

> As referências marcadas `scratch/sac1/…` são o **dump por tipo** do decompilado (bancada, fora do
> controle de versão) — o comando para regerar qualquer tipo é
> `ilspycmd -t <Tipo> lib/Assembly-CSharp.dll` (`docs/cobertura/rv28-globules.md` §8). As referências
> do repositório (`BetterTooltips/…`, `docs/…`) são conferidas por
> `python tools/checa_citacoes.py docs/CONFERENCIA-RV28-GLOBULES.md`.

---

## 7. Limites deste pacote (o que ele **não** prova)

1. **Não é prova de runtime por si só.** O que está provado por execução é o caminho (compila, está
   instalado, as guardas passam, a matriz numérica 8/16 e 20/40 e as 4 iscas do teste). O número **na
   tela** é o que esta conferência produz — até hoje o `LogOutput.log` tem **zero** marcas
   `[Globule RV-28]` (ninguém hoverou um globule depois da blindagem).
2. **8/20/28** (as duas tiers) é ponto aberto do `RV-24`: o cenário A5 mede, não julga.
3. O **sorteio** dos drops é do jogo: um membro pode não sair na sua sessão (§2.5).
4. O comportamento do **Power Globule** com a descrição do status depende de qual descrição o jogo
   exibe naquele tooltip — o mod cobre as duas (§1.3).
5. Este pacote **não** cobre a publicação da versão nova (gate `PUB-1`), que é outro card.

---

## 8. Depois da sessão

1. Preencher as tabelas A, B e C (§4) — copie o arquivo como `docs/CONFERENCIA-RV28-GLOBULES-PREENCHIDO.md`
   ou anote e cole no comentário do card.
2. Comentar o resultado no card **`t_2bd1a32c`** (o cartão-mãe do `RV-28`), com: cenários por onde
   passou, membros vistos, marcas do log (trecho colado) e **qualquer NOK com o texto visto × esperado**.
3. NOK é achado: descreva o que a tooltip mostrou **literalmente** — isso vira card de correção para o
   `BetterTooltips`.
4. Um membro `nao sorteado` **não** é NOK: registre quantas tentativas fez (deixe a linha pendente).
