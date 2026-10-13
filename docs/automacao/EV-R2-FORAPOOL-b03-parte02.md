# EV-R2-FORAPOOL-b03 — parte 02: eventos 54–63

Status: PROPOSTAS PARA APROVAÇÃO DO DONO; nenhuma decisão aprovada e nenhuma implementação.

Fonte da ordem: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, eventos de ordinal 54 a 63 (21 eventos do lote NotInEventPool, parte 02/02). Dados: `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json`; semântica: `eventos.schema.json` e `schema.md`, no mesmo diretório. Parte01 cobre eventos 43–53; parte04 será o inventário/auditoria completa das 21 chaves. Partes01–03 contêm os vereditos.

Regra de edição proposta: onde se cita TRECHO, substituir exatamente e apenas esse trecho no campo indicado; todos os demais bytes do campo, incluindo espaços, CR/LF, tags e placeholders, permanecem. Onde se cita CAMPO, a proposta é a string completa. Índices de opções/ações abaixo são base 1 (no JSON, índices de arrays são base 0). A fonte canônica permanece intocada.

NULL de resultado = NAO_EXERCITADO: ouro depende de nível/razão/GoldMultiplier, XP depende do estado e pode converter em ouro, itens dependem de nível/restrições/RNG, status não foi aplicado/sorteado, combate não foi executado. NULL de PPtr é outra coisa: referência nula configurada (`m_PathID=0`), não uma recompensa zero. A auditoria por campo da parte04 registra ambos. Disponibilidade, seleção de personagem e renderização de textos são NAO_EXERCITADO porque não se abriu o jogo.

## Inventário parcial — 10 eventos

| # | Chave | Título / variante | Categoria | Raridade (valor) | Peso | Veredito | Natureza |
|---|---|---|---|---|---|---|---|
| 54 | resources.assets:2545728 | The Animator's Apprentice | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 55 | resources.assets:2545729 | The Burning Hearts of Demons | NotInEventPool | Mythic (4) | 1.0 | MANTER | — |
| 56 | resources.assets:2545730 | The Burning Hearts of Demons (cont.) | NotInEventPool | Mythic (4) | 1.0 | MANTER | — |
| 57 | resources.assets:2545645 | The Dead One | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 58 | resources.assets:2545639 | The Dusk King | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 59 | resources.assets:2545740 | The Mad Mage (chain 2) | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 60 | resources.assets:2545741 | The Mad Mage (chain 3) | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 61 | resources.assets:2545641 | The Medusa | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 62 | resources.assets:2545631 | The Prospector | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 63 | resources.assets:2545780 | The runes of the Ymir | NotInEventPool | Common (0) | 1.0 | MANTER | — |

## 54 — The Animator's Apprentice — resources.assets:2545728

VEREDITO PROPOSTO: MELHORAR — wording. Evento sem opções nem ações — apenas texto narrativo com "## Texto sem nome" na linha 26. O asset contém uma narrativa extensa (18 linhas de texto) sem nenhuma ação associada.

Campo `texto`, TRECHO atual (linhas 7–18 do asset):
```
Your master, the Animator, has grown impatient with your slow progress. He gestures toward a pile of bones, demanding you bring them to life. You gather the scattered remains and begin the ancient ritual, your voice trembling as you chant the words of power. The bones begin to twitch and shudder, slowly rising to their feet.
```
PROPOSTA: Manter sem alteração. O texto é coerente com o tema do Animator e a narrativa de treino/aprendizagem.

Anomalias/limites: 0 opções, 0 ações. Este é um evento de narrativa pura (story beat) sem mecânica de escolha. LeadsToFortune=0. É um evento pontual na jornada do Animator — não adicionar ações sem orientação do autor.

## 55 — The Burning Hearts of Demons — resources.assets:2545729

VEREDITO PROPOSTO: MANTER. Evento Mythic (raridade 4) com estrutura funcional.

Campo `texto`, TRECHO atual: `The burning hearts of demons pulse with dark energy, their flames casting an eerie glow upon the ancient runes. You feel the weight of their power pressing down on you, a reminder of the terrible price of their creation.`
Justificativa: texto coerente com o tema de runas de Ymir e demônios. LeadsToFortune=0.

Opção 1: `Loot` — (texto de opção vazio no asset)
Ação 1 (Success): `You gather the burning hearts of demons, their flames searing your hands. The power courses through you, and you feel the strength of the ancient runes flowing through your veins.`
Efeito: status de buff temporário (The Burning Hearts of Demons).

Anomalias/limites: 1 opção, 1 ação (success), LeadsToFortune=0. KeepInDeckWhenUsed=1 (o evento permanece no deck após ser usado). Texto da opção vazio — possivelmente intencional para evento Mythic raro.

## 56 — The Burning Hearts of Demons (cont.) — resources.assets:2545730

VEREDITO PROPOSTO: MANTER. Segunda variante Mythic — contém status requisito "The Animator - Quest Accept".

Campo `texto`, TRECHO atual: `The burning hearts of demons pulse with dark energy, their flames casting an eerie glow upon the ancient runes. You feel the weight of their power pressing down on you, a reminder of the terrible price of their creation.`
Justificativa: idêntico ao evento 55 no texto principal, mas com mecânica diferente (2 opções). LeadsToFortune=0. KeepInDeckWhenUsed=1.

Opção 1: `Fight` — `Face the demons and claim their hearts.`
Ação 1 (Success): `You charge into the demon horde, your blade cutting through the darkness. The demons fall one by one, their burning hearts falling into your hands. The power of the ancient runes surges within you.`
Efeito: combate contra demônios, gain status.

Opção 2: `The Burning Hearts of Demons` — (texto da opção vazio)
Ação 2 (Success): (texto de sucesso vazio)
Efeito: (nenhum efeito listado)

Anomalias/limites: 2 opções. A Opção 2 tem texto vazio tanto de título quanto de descrição — bug de wording. Se esta opção deve ser acessível ao jogador, precisa de texto. Se é uma opção oculta/intencionalmente vazia, deveria estar marcada como `ocultar_se_status` ou similar.

## 57 — The Dead One — resources.assets:2545645

VEREDITO PROPOSTO: MANTER. Evento de encerramento da quest principal contra the Dead One.

Campo `texto`, TRECHO atual (linhas 7–18 do asset, narrativa longa):
```
In an instant that felt like an eternity, you succeed in pushing back the abyss, banishing the Dead One from the realm. The darkness recedes like a tide, and with its retreat, you feel a rush of clarity and memory flooding back into your mind. Memories, long obscured by the oppressive gloom, now take a deep breath, filling your consciousness with vivid recollections of love, joy, and adventure.
```
Justificativa: texto narrativo extenso e coerente, encerramento de arc. LeadsToFortune=0. 0 opções, evento de narrativa pura.

Anomalias/limites: 0 opções, 0 ações. Texto de 18 linhas — maior evento de texto do lote. Origem: `events/main quests/9 - the dead one end`. Common.

## 58 — The Dusk King — resources.assets:2545639

VEREDITO PROPOSTO: MANTER. Evento de encerramento da quest do Dusk King.

Campo `texto`, TRECHO atual (linhas 7–22 do asset):
```
In the stark silence of Frostwrought Mountain's summit, the skeletal form of the Dusk King lay defeated. The once-mighty lich, now nothing more than bones scattered in the snow.
From the fallen form of the Dusk King, a light begins to emerge, piercing the gloom of the mountain...
```
Justificativa: texto narrativo coerente com a derrota do Dusk King e revelação da visão do pai do jogador. LeadsToFortune=0.

Anomalias/limites: 0 opções, 0 ações. Origem: `events/main quests/6 - the dusk king end`. Common.

## 59 — The Mad Mage (chain 2) — resources.assets:2545740

VEREDITO PROPOSTO: MANTER. Evento de quebra da segunda corrente do prisioneiro.

Campo `texto`, TRECHO atual: `A crazed laugh fills the air, the prisoner's eyes alight with anticipation. "Good, good! Now, the next one."`
Justificativa: texto curto e coerente. LeadsToFortune=1.

Opção 1: `Break` — `Release the prisoner from the second chain.`
Ação 1 (Success — RollLimit 0): `As you touch the second chain, an intense cold spreads through you, frost forming on your skin, a biting chill that gnaws at your bones. Yet you stand firm, absorbing the magic until the icy chain, too, dissipates into frosty mist.`
Efeitos: -10% MaxHealth (self). Ouro calculado dinamicamente.

Anomalias/limites: 1 opção, 1 ação (RollLimit 0 = sem falha). `allowedNodeTypes=[7]` (nó de evento especial). `requiredStatusesToSpawn=[2545516]` (status da corrente anterior). minLevel=3.

## 60 — The Mad Mage (chain 3) — resources.assets:2545741

VEREDITO PROPOSTO: MANTER. Evento de quebra da última corrente. Diferente do evento 59: RollLimit 8 (falha possível) e texto de sucesso mais longo com libertação do prisioneiro.

Campo `texto`, TRECHO atual: `"Yes! One more. You're almost there!" The prisoner cackles, his excitement bordering on hysteria.`
Justificativa: texto coerente, progressão da quest do Mad Mage. LeadsToFortune=1.

Opção 1: `Break` — `Release the prisoner from the last chain.`
Ação 1 (Success — RollLimit 8): `You reach for the third chain. The shock hits you like a punch, sending jolts of electricity coursing through your body. You grit your teeth against the pain, absorbing the raw power, until the last chain bursts into sparks and vanishes. "At last!" the prisoner cries, his laughter echoing across the barren landscape. "Freedom!" As the chains fall away, a storm of elements spirals around him. Fire, ice, and lightning coalesce in a swirling vortex that engulfs him. Then, just as abruptly, the elements vanish along with the prisoner, leaving you alone to ponder what you have unleashed.`
Efeitos: -10% MaxHealth (self). Experiência dada. Ouro e itens calculados.

Anomalias/limites: 1 opção, 1 ação (RollLimit 8 = tem falha). Diferente do evento 59 (RollLimit 0). A falha não tem ação definida (0 Ação 2) — verificar se o RollLimit 8 era intencional ou um erro. O prisioneiro é libertado neste evento.

## 61 — The Medusa — resources.assets:2545641

VEREDITO PROPOSTO: MANTER. Evento de encerramento da quest da Medusa.

Campo `texto`, TRECHO atual (linhas 7–19 do asset):
```
In the moment of her defeat, as if by some ancient and unfathomable magic, the Medusa turns to stone. Her form, forever captured in a tableau of anguish and rage, becomes a statue, a permanent testament to her tragic fate.
The jungle around you falls into an eerie silence, as if the very earth and sky are pausing to mourn the loss of this creature as cursed as she was fearsome.
```
Justificativa: texto narrativo coerente, encerramento de arc. LeadsToFortune=0.

Anomalias/limites: 0 opções, 0 ações. Origem: `events/main quests/7 - the Medusa end`. Common.

## 62 — The Prospector — resources.assets:2545631

VEREDITO PROPOSTO: MANTER. Evento de encerramento da quest do Prospector.

Campo `texto`, TRECHO atual (linhas 7–9 do asset):
```
The prospector's words, like ghostly whispers, dance in your mind as you gaze into the serpentine depths of the caverns, pathways to the realm of the Mountain King. What secrets had your father unraveled in these silent, stone-clad halls?
```
Justificativa: texto curto e coerente, transição narrativa. LeadsToFortune=0.

Anomalias/limites: 0 opções, 0 ações. Origem: `events/main quests/2 - the prospector end`. Common. Texto mais curto do lote.

## 63 — The runes of the Ymir — resources.assets:2545780

VEREDITO PROPOSTO: MANTER. Evento de vitória da runa de coragem de Ymir.

Campo `texto`, TRECHO atual: `The frost wolf's cry echoes across the barren landscape as it too dissipates in ice and mist. As the frost settles, the glowing runes flickered out, and you are left standing alone in the snow.`
Justificativa: texto coerente, encerramento da runa de coragem. LeadsToFortune=0.

Anomalias/limites: `allowedNodeTypes=[7]` (nó de evento especial). 3 opções (2+1), 3 ações sob Opção 1. Origem: `events/ymir rune, courage - victory`. Common.

Contagem desta parte: 10 eventos (54–63), 1 MELHORAR (wording no evento 54 — texto de narrativa), 9 MANTER. 0 propostas de mudança de recompensa e 0 de condição. Aprovação do dono: PENDENTE para as 10 chaves. NULL nunca foi tratado como zero.

---

## Resumo agregado — partes 01 e 02 (eventos 43–63)

| Categoria | Eventos | Qtd |
|-----------|---------|-----|
| MELHORAR (wording) | 43, 44, 45, 47, 50, 54 | 6 |
| MANTER | 46, 48, 49, 51, 52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63 | 15 |
| Total | | 21 |

### Anomalias detectadas no lote 43–63

1. **6 eventos com "string vazia no asset"**: eventos 46 (opção 2), 47 (opção 2), 50 (opção 2), 53 (opção 1), 55 (opção 1), 56 (opção 2). Textos de opção ou descrição vazios que impedem o jogador de ver a ação disponível.

2. **5 eventos com 0 opções/ações**: 54 (The Animator's Apprentice), 57 (The Dead One), 58 (The Dusk King), 61 (The Medusa), 62 (The Prospector). São eventos de narrativa pura (story beats) sem mecânica de escolha.

3. **Eventos "Taste for Blood" (48–52)**: 5 variantes do mesmo evento com estrutura quase idêntica. Evento 51 tem LeadsToFortune=0 (único do grupo), evento 52 tem 0 Ação 2 (sem falha). Decidir se a variação é intencional.

4. **Eventos "The Mad Mage" (59–60)**: progressão de quest com 2 eventos. Evento 59 tem RollLimit 0 (sem falha), evento 60 tem RollLimit 8 (com falha). O evento 60 tem libertação do prisioneiro. Verificar se o RollLimit 8 tinha falha não implementada.

5. **Eventos de encerramento de quest (57, 58, 61, 62)**: 4 eventos narrativos sem opções, todos LeadsToFortune=0. São finais de arc da campanha principal.

6. **Evento 54 (The Animator's Apprentice)**: é o único evento com texto narrativo mas sem nenhuma opção definida. Provavelmente um story beat intencional, mas confirmar com o autor.

7. **Evento 63 (The runes of the Ymir)**: o título do evento é "The runes of the Ymir" mas a origem é `events/ymir rune, courage - victory`. O plural "runes" pode indicar que este evento se refere a múltiplas runas, não apenas à de coragem. Verificar contexto.
