# Revisar ao final — o que depende de olho humano

Gerado em **29/09/2026**, com 8 de 11 árvores fechadas (Shadow, Light, Monk, Thief, Fire,
Cold, Warrior, Chaos). Faltam **Lightning, Basic, Innate** e os **3 abertos da Nature**.

Este arquivo é a lista do que **não** fecha por código/dump e precisa de você — em jogo ou
como decisão. Cada item diz **por que** está aqui, para você julgar sem reler o histórico.

---

## A) Verificações em jogo — áreas e raios que o dump não alcança

Em **nenhum** destes o texto foi tratado como defeito: o texto está de pé e a limitação é da
ferramenta (`alcanceHits` e `hexesAtiv` não trazem a área nessas skills). Basta usar a skill e
ver se o comportamento bate com o texto.

| árvore | skill | o texto diz | o que olhar |
|---|---|---|---|
| Monk | **`Cyclone Kick`** | "pulls enemies within **4** hexes" | o **destino** está provado pelo teste (*"not pulled adjacent"*) e virou nota; falta o **4** do alcance — conferir em jogo |
| Fire | **`Detonate`** | "all foes within **2** hexes of your character" | o raio do estouro (é self-cast) |
| Fire | **`Meteor`** | "deals *0 fire damage within **2** hexes" | o teste confirma o **fogo que permanece** (*"the fire left by Meteor did not burn the pinned enemy"*); falta só o raio de 2 |
| Cold | **`Frost Nova`** | "within **2** hexes of the caster" | o raio — atenção: o teste imprime *"dealt X **to the centre** and Y"*, o que sugere **queda de dano** fora do centro; o texto não menciona |
| Ranger | **`Volley`** | "Shoot up to **5** enemies ... The arrow can chain to targets within" | o texto DIZ 5 + o chain, mas o dump não tem o campo — conferir contando em jogo |
| Nature | **`Frost Breath`** | "Deals *0 cold damage **each turn**" | a ação é golpe único e não há trigger no dump — conferir em jogo se realmente repete |
| — | **`Thunder Blast`** (Dragonkin) | "Applies **10 stacks** of Shocked" | **é habilidade de DRAGONKIN**, não skill de árvore (descoberto pelo campo `modelo=` do dump) — explica não ter teste nem campos na skill; faltar só o `numStacks` |

---

## B) Correções de texto já aplicadas — vale uma conferida visual

Todas foram decididas com evidência de código. Estão aqui só para você ver o **resultado** no
tooltip e confirmar que ficou legível.

| skill | o que mudou | por quê |
|---|---|---|
| `Dashing Strikes` | "up to **3** times" (era 4) **e** "within **3** hexes" (era 2) | o asset tem `DashMaxChainCount=3` e `Cell.InRange(LastCell, 3)`; dois irmãos (4/4) provaram a semântica |
| `Dodging Strikes` / `Power Strikes` | "within **3** hexes to strike again" (era 2) | mesmo `InRange(LastCell, 3)` |
| `Cauterize` | ganhou "This cannot reduce the target below 1 health." | o efeito é `Mathf.Min(Target.Health - 1, MaxHealth * .1f)` — **não mata**, e o texto não dizia |
| `Haunt` | "**2,5%**" (era 6%) | `SourceStored['HealingForced'] = Source['MaxHealth'] * .025f` |
| `Mass Cure` | ganhou "The 2-hex area is centred on the chosen TARGET, not on the caster." | confirmado por você em jogo |
| `Break The Ice` | ganhou "That bonus is consumed by your first damaging cast." | o texto já diz os 100%; o **consumo** vem do teste *"+100% until the first damaging cast"*. Uma primeira versão repetia o texto e foi corrigida |
| `Cyclone Kick` | ganhou "The pull drags them the whole way: they land on a hex adjacent to you." | teste *"the enemy was not pulled adjacent"* — "towards you" ≠ adjacente |
| 3 formas | ganharam "While transformed you gain: ..." (Werewolf: basic attack + Blood Howl + Cursed Bite; Dire: idem, maior; Vampire Bat: Energy Drain) | campo `modelo=` do dump (`ModelChangeCharacter.Skills`) |
| `Shapeshift Dragonkin` | a lista das 3 habilidades por cor anexada ao texto corrigido | mesmo campo; entrou no `TextFixes` porque uma entrada no `TextAppends` para esse texto **nunca rodaria** |
| `Chain Lightning` | ganhou "The 5 counts the chain's **HOPS**, not different enemies: the bolt can hit the same enemy again, so with only two enemies in range it bounces between them." | **sua observação em jogo** + `ChainSameTarget = true` no `ActionInfo` (o mesmo alvo pode ser reatingido) |
| `Slam` / `Crushing Slam` / `Stunning Slam` | ganharam "The line reaches **5** hexes from you." | `blast=Distance(Source.Cell) <= 5 && IsSameHemisphere(...) && DistanceFromLine(...) < 3f/2f` |
| `Ice Lance` | ganhou "The line reaches **10** hexes from you." | o mesmo formato de linha com `<= 10` |
| `Breath of Winter` / `Lightning Breath` | ganharam "The cone reaches **4** hexes from you." | o mesmo formato de linha (cone de 3 hexes de largura) com `<= 4` |
| `Charge` | ganhou "The path is a line of up to **7** hexes." | `rsel=Source.Cell.IsInSixLine(Cell, 7) && Source.Cell.HasDirectPath(Cell)` |
| 18 skills de invocação | bloco com o bicho + as habilidades dele + "Does not copy your attributes / Your Might raises its damage; your Intelligence, its health." | lido de `CreateSummon` (não copia atributos, mas escala com Might e Int) |
| `Brambles` / `Ice Wall` | "Benefits from your Might and Intelligence, but does not count as a summon." | `addToSummonList: false` |
| `Fuel for the Flames I/II`, `Rainstorm` | explicação do **Power of Mana** (o que afeta e o que não) | `ManaPowerMod` só em ação com custo de mana; não mexe no custo nem nos status |
| 4 skills de cura/escudo da Light | linha de escala (Attack Power + Holy Power) | `GetActionDamage` multiplica dano e cura por `DamageModHealing` |
| 12 skills de escala por nível | "Scales with your character level." | `GetFlatDamageValue(level, rarity)` |
| 97 notas ao todo | estilo **negrito→** cor e posição do jogo | a cor vem de `specialDescColor` do prefab, não de escolha minha (BT-9) |

### Fechado NO CÓDIGO — não precisa de olho (29/09)

**`Resist Divine` → `Resist Holy`** (e `Divine Resistance` → `Holy Resistance` nos 3 afixos
`Angel`/`God`/`Saint`). A dúvida era: *a ficha de personagem passa pelo funil que o mod
intercepta?* Passa — `InventoryManager.UpdateStats` l.125419 é
`OptionsManager.Localize(Attribute.GetStatMenuDisplayName())`, e `GetStatMenuDisplayName()` só
existe em **2 lugares** do assembly (a própria definição, l.319838, e essa linha); prefabs de UI
usam `PrefabLocalizer` → `OptionsManager.LocalizeUIText` (l.156306/310), o mesmo funil (e o mod
já cobre textos de UI e dicas de loading, o que prova que o hook pega esse caminho).

E é **defeito, não gosto**: os 4 irmãos no motor seguem `Resist <tipo de dano>` — `Resist
Physical` 28 chaves, `Resist Lightning` 28, `Resist Fire` 28, `Resist Cold` 28 — e só o sagrado
ficava em `Resist Divine` 26, com o dano chamado `Holy` (33 chaves + `HolyDamage` 7). Corrigido no
RV-13 (rótulo) e completado no RV-14 (os 3 afixos). O campo interno `ResistDivine` **não** é
tocado — a mudança é só de exibição.

## C) Inconsistências do PRÓPRIO jogo (não corrigir no mod — fila do RV-9)

Aqui o "defeito" é do dado do jogo, não do tooltip. Registrado para decidir depois se vira
correção em runtime (como o RV-9 prevê) ou se fica como está.

- **`Wrath of the  Righteous`** — espaço **duplo** no próprio **nome** da skill.
- **`Haunt`** — o status interno diz **8%**; o código faz **2,5%**. O texto da skill foi para 2,5%.
- **`Enchant Fire`** — a descrição interna do **status** diz "a **chance** to deal"; o teste do
  jogo mostra que a básica encantada **sempre** causa dano. O texto da skill está certo.
- **`Ice Slash` / `Thunder Slash`** — o `expr` da **descrição** usa `Source.SpellPower() * .5f *
  Source.DamageModFire` (modificador de **fogo**) em duas skills de gelo e elétrico: o **número
  exibido** no tooltip sai calculado com o stat errado. O dano **real** está certo (`Frost Slash` →
  `TargetStored['ColdDamage']`, `Thunder Slash` → `TargetStored['LightningDamage']`, ambos com
  `AttackPower * 1.2f`). Como o número vem de um token dinâmico (`*0`), **não dá para corrigir por
  texto** — só por patch de código. Decidir no RV-9.
- **`Melee Attack Healing` / `Ranged Attack Healing`** — vêm com `dano=Physical` no asset, enquanto
  os irmãos `Staff Attack Healing` / `Unarmed Attack Healing` vêm com `dano=Healing`. Pode ser só
  a nomenclatura do dump, mas o funcional (curar em aliado) não tem teste no assembly para fechar.
- **`Crippled` × `Slow`** — **0** ações do jogo aplicam `Crippled` e **5** aplicam `Slow`
  (incluindo uma skill chamada `Cripple`). O texto "crippled" é a convenção do jogo; não mexi.
- **`Abyssal Night`** — `expr 2.3f` na skill e `2.1f` na ação; o `*N` do tooltip vem da ação,
  então o 2.3 é vestigial (não aparece no texto).
- **`Detonate`/`Meteor`/`Cyclone Kick`** — o campo `maxChain` é o teto de **alvos encadeados**,
  não o raio; em `Cyclone Kick` ele vale 4, o mesmo número do texto ("4 hexes").

---

## D) O que NÃO foi revisado — por regra

- **Árvore Bard (31 skills)** — intocável por decisão do projeto (conteúdo chega na próxima
  atualização do jogo). Não revisar, não alterar.
- **8 skills do Chaos** em `sem-explicacao`: `Aid`, `Benevolence`, `Chaos Touch`, `Harm`,
  `Helping`, `Hurting`, `Malevolence`, `Touch of Chaos` — omitidas **por design**: a graça do
  Chaos é não saber o resultado.
- **67 textos com espaço no fim** (RV-8b-2d) — decisão adiada: hoje é invisível e apara-lo tem
  risco de colar palavras em texto concatenado.

---

## E) Riscos técnicos do mod — checar se o jogo for atualizado

- **O hook de `Tooltip.ShowTooltip`** (que move a nota para depois dos custos/alcance) resolve
  o alvo por reflexão: `AccessTools.GetDeclaredMethods(typeof(Tooltip))` filtrando `ShowTooltip`
  com **mais de 4 parâmetros**. Se a assinatura mudar, o movimento para de funcionar.
- **A leitura de `specialDescColor`** (cor das notas) vem do **prefab** do tooltip. Se vier
  vazio, o mod cai no bege `#C8B090` (medido do bloco do jogo) e registra no log.
- **Alvos de patch** — cada patch tem de ficar na classe do seu alvo (`OptionsManager.Localize`
  em `LocalizePatch`; `ShowTooltip` na classe própria com `TargetMethod`). Cruzar os dois
  gera `HarmonyException: IL Compile Error` e **nada roda silenciosamente** — foi o bug do BT-9.
- **Diagnóstico no log** (usar sempre que algo parecer não aplicar):
  `ShowTooltip interceptado...`, `cor do jogo para explicacoes = #RRGGBB`,
  `explicação adicionada a '...'`.
- **Ordem de prioridade do Harmony**: em **prefix** é decrescente; em **postfix** é **crescente**
  (`Priority.Low` roda **primeiro**). Foi o que atrasou a cor por dois ciclos.

---

## F) Decisões fechadas com uma suposição — revisitáveis

- **Tiers que SOMAM** (quando duas tiers compartilham um status, o valor é acumulado):
  `Masochism` 2/5, `Momentum` 2/3/5, `Omnism` 8/20, `Variety` 40/100.
- **"Cripple" é o vocabulário do jogo para `Slow`** — pela regra do padrão da maioria (5 de 5).
- **Invocação não COPIA atributos, mas ESCALA com eles**: Might → dano, Intelligence → vida.
- **`Brambles`/`Ice Wall`** são destrutíveis que ganham Might/Int mas **não contam como summon**.
- **`InRange(cell, N)` é inclusivo** (`Distance <= N`) — provado na l.120624 do decompilado.
- **A cor das explicações** veio medida por pixel das suas imagens (`#C8B090`), não do prefab,
  como reserva.

---

## Como usar

1. Abra o jogo numa sessão e vá pela **tabela A** (é o grosso e não bloqueia nada).
2. Dê uma olhada nas correções da **tabela B** — só para confirmar legibilidade.
3. O que decidir sobre a **seção C** (inconsistências do jogo) vira o escopo do **RV-9**.
4. A **seção E** só importa se o jogo receber atualização.
