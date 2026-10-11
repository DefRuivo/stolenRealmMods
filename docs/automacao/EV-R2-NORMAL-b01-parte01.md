# EV-R2-NORMAL-b01 - Propostas de melhoria: Eventos 1-20 (Lote Normal)

**Arquivo gerado em**: 2026-10-11  
**Fonte**: `docs/cobertura/EV-R1/lote-Normal-v2.md` (eventos 1-20)  
**Status**: PROPOSTA para aprovacao do dono

---

## Evento 1 - A Test of Fear
- **Chave**: `resources.assets:2545531`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "The yearning ghost extends her hand pleading for help."
- **Opcoes**: 2 (Reach / Leave)
- **Anomalias**: `disabled: 1`, campos `chave` e `nome` NULL
- **Veredito**: MELHORAR
- **Justificativa**: Evento desativado (`disabled: 1`). O texto e genrico - a mesma frase aparece em Eventos 8 (Barbarian Fisherman) e 14 (Blood of the Abyss). Provavel placeholder de desenvolvimento que nunca foi finalizado.
- **Proposta**: Reativar (`disabled: 0`) e reescrever o texto original com algo tematico, ex: "A ghostly figure flickers at the edge of your vision, its spectral fingers reaching out with desperate longing." Se nao houver conteudo definido para este evento, considerar desistir do slot e redistribuir o peso para eventos existentes.
- **Campos NULL**: `chave` (GUID do evento nao populado), `nome` (nome do evento nao populado). Isso sugere que o evento nunca foi integrado corretamente no pipeline de deploy.

---

## Evento 2 - Acid Trap
- **Chave**: `resources.assets:2545532`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "You come across a statue of a snake carved from what appeares to be solid stone. Its gemstone eyes gleam dangerously, as a cloud of greenish fumes billow forth from its maw. An acrid, burning smell fills the air, stinging your nostrils forcing you back. Someone with the constitution to weather the poisonous fumes might be able to jam the deadly Acid Trap."
- **Opcoes**: 1 (Disable)
- **Anomalias**: typo "appeaures" (deveria ser "appears")
- **Veredito**: MELHORAR
- **Justificativa**: Typo "appeaures" no texto original. A opcao unica (Disable) e limitada - nao ha opcao de ignorar/passar sem desarmar.
- **Proposta**: Corrigir para "appears". Avaliar adicionar uma opcao "Leave" para permitir ao jogador evitar o risco.

---

## Evento 3 - Alchemist's Workbench
- **Chave**: `resources.assets:2545533`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "You stumble across an ornate table cluttered with scrolls, flasks, and various arcane implements - clearly an Alchemist's Workbench. The air is thick with the scent of ancient herbs and lingering magic, a tantalizing aroma for any adventurer. On the table lay an open scroll, the elegant elvish script detailing recipes for various magical potions. The instructions, although intricate, are clear enough."
- **Opcoes**: 3 (Potion of Power, Mixture of Motion, Tonic of Toughness)
- **Anomalias**: Todas as 3 opcoes tem `misteriosa: true` e `roll_bonus: ['']` (bonus vazio). Descricoes das opcoes estao vazias (string vazia no asset).
- **Veredito**: MELHORAR
- **Justificativa**: As opcoes tem descricoes vazias no asset, o que significa que o jogador ve apenas o nome da pocao sem saber o que ela faz. O `roll_bonus` vazio tambem e suspeito - pode indicar que a mecanica de rolagem nao esta implementada corretamente.
- **Proposta**: Adicionar descricoes para cada opcao explicando os efeitos (ex: "Potion of Power - Increase your Strength attribute") e investigar por que `roll_bonus` esta vazio.

---

## Evento 4 - Ambush
- **Chave**: `resources.assets:2545534`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "A silence hangs heavy and foreboding. You feel a shiver of unease, a sense of impending danger that seems to seep from the shadows. Your hand instinctively strays to the handle of your weapon..."
- **Opcoes**: 1 (Steel Yourself)
- **Anomalias**: `disabled: 1`, campos `chave`, `nome` e `dados_recompensa_final` NULL
- **Veredito**: MELHORAR
- **Justificativa**: Evento desativado. O texto e atmosferico mas curto demais. Apenas uma opcao limita a agencia do jogador.
- **Proposta**: Reativar e expandir. Adicionar opcao "Fight" (atacar os atacantes) para dar escolha real.

---

## Evento 5 - Archery Competition
- **Chave**: `resources.assets:2545535`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "In a forest clearing, an unexpected challenge has been set by an even more unexpected challenger. Gobin Hood, a goblin of monstrous strength, challenges your intrepid band of adventurers to an unconventional test of archery. Not the usual sissy elf game, Gobin Hood growls, hefting his crude bow made from gnarled ironwood. We ain't aiming for some painted dot. We're smashing through the target! The target mentioned is no simple slab of wood, but a formidable barricade, several planks thick, far more robust than any normal target."
- **Opcoes**: 2 (Accept / Leave)
- **Anomalias**: Nenhuma.
- **Veredito**: MANTER
- **Justificativa**: Texto bem escrito, imersivo, com bom humor. Duas opcoes claras. Sem anomalias detectadas.

---

## Evento 6 - Armor Chest
- **Chave**: `resources.assets:2545536`
- **Categoria**: Normal | **Raridade**: Uncommon | **Peso**: 1.0
- **Texto original**: VAZIO (string vazia no asset)
- **Opcoes**: 1 (Open)
- **Anomalias**: Texto vazio, `roll_bonus: ['']`
- **Veredito**: MELHORAR
- **Justificativa**: Um cofre sem descricao e um erro grave. O jogador abre um cofre sem saber o que esperar. A raridade "Uncommon" sugere um evento mais rico.
- **Proposta**: Escrever texto descritivo. Exemplo: "A heavy wooden chest, reinforced with iron bands and covered in faded runes, stands at the crossroads. The lock appears old but intact."

---

## Evento 7 - Armor Chest
- **Chave**: `resources.assets:2545537`
- **Categoria**: Normal | **Raridade**: Uncommon | **Peso**: 1.0
- **Texto original**: VAZIO (string vazia no asset)
- **Opcoes**: 1 (Open)
- **Anomalias**: Texto vazio, `roll_bonus: ['']`
- **Veredito**: MELHORAR
- **Justificativa**: Identico ao Evento 6 - duplicata funcional. Ambos sao "Armor Chest" com a mesma estrutura (1 opcao, Open). O jogo pode tratar como eventos distintos, mas para o jogador sao redundantes.
- **Proposta**: Manter apenas um, ou diferenciar os dois: Event 6 = cofre com armadura, Event 7 = cofre com outro tipo de item. Escrever textos distintos para cada.

---

## Evento 8 - Barbarian Fisherman
- **Chave**: `resources.assets:2545538`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "The yearning ghost extends her hand pleading for help." (mesmo texto do Evento 1)
- **Opcoes**: 2 (Reach / Leave)
- **Anomalias**: `disabled: 1`, mesmo texto que Evento 1 (ghost), `LeadsToFortune: 1`
- **Veredito**: MELHORAR
- **Justificativa**: Texto copiado de Evento 1 ("A Test of Fear") - o jogador espera encontrar um pescador barbaro mas recebe texto sobre um fantasma. Isso e erro de conteudo.
- **Proposta**: Reescrever completamente o texto original para um pescador barbaro. Exemplo: "A massive barbarian sits on a mossy rock by the river, casting a crude fishing line into the water. He turns to you with a grizzled smile."

---

## Evento 9 - Battle
- **Chave**: `resources.assets:2545539`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 5.0
- **Texto original**: VAZIO (string vazia no asset)
- **Opcoes**: 1 (Fight!)
- **Anomalias**: Texto vazio, campos `chave`, `nome`, `dados_recompensa_final` NULL, `roll_bonus: ['']`
- **Veredito**: MELHORAR
- **Justificativa**: Evento com peso 5.0 (alto) mas sem texto e sem dados de recompensa populados. E um evento de batalha generico - sem contexto, o jogador ve apenas "Fight!" sem saber contra o que.
- **Proposta**: Adicionar texto descritivo. Exemplo: "A feral beast lunges from the brush, fangs bared and eyes burning with rage." Investigar por que `dados_recompensa_final` e NULL - pode indicar que o sistema de recompensas de batalha nao foi configurado.

---

## Evento 10 - Battletest Event
- **Chave**: `resources.assets:2545540`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 5.0
- **Texto original**: VAZIO (string vazia no asset)
- **Opcoes**: 1 (Fight!)
- **Anomalias**: `disabled: 1`, campos `chave`, `nome`, `dados_recompensa_final` NULL, `roll_bonus: ['']`
- **Veredito**: MELHORAR
- **Justificativa**: Desativado. "Battletest" soa como evento de teste que nunca foi removido. Sem texto, sem recompensa, sem identificacao.
- **Proposta**: Se for realmente um evento de teste, remove-lo. Se for um evento intencional (ex: arena de treino), reescrever com texto e recompensas.

---

## Evento 11 - Bear Trap
- **Chave**: `resources.assets:2545541`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "An unexpected impediment blocks your path ahead. A Bewitched Bear Trap, snaps its iron jaws open and shut with an insatiable hunger. A cruel and cunning device crafted with malicious intent. This is more than a mere mechanical contraption. Sinister magic is at play. Someone will have to disarm it to ensure safe passage."
- **Opcoes**: 1 (Overpower)
- **Anomalias**: Nenhuma.
- **Veredito**: MANTER
- **Justificativa**: Texto bem escrito e tematico. Acao clara. Sem anomalias.

---

## Evento 12 - Below Zero
- **Chave**: `resources.assets:2545542`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "A bizarre fungal growth blocks your path ahead, its blue luminescence radiating an unnerving cold that freezes the very air around it. You recognize it as a Frostcap, an ancient form of magical fungi. It saps the warmth from its surroundings to survive. Delicate snowflakes, out of place in this environment, dance and whirl about its icy aura."
- **Opcoes**: 1 (Escape)
- **Anomalias**: Nenhuma.
- **Veredito**: MANTER
- **Justificativa**: Texto criativo e imersivo. Sem anomalias detectadas.

---

## Evento 13 - Between Worlds
- **Chave**: `resources.assets:2545543`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "A spectral maiden extends her hand towards you, her hollow eyes filled with a silent yearning, a call for help that whisperes across the ages."
- **Opcoes**: 2 (Reach / Leave)
- **Anomalias**: typo "whisperes" (deveria ser "whispers"), `roll_bonus: ['', '']` (bonus vazio)
- **Veredito**: MELHORAR
- **Justificativa**: Tipografia "whisperes" -> "whispers". O texto e bom mas curto. Os `roll_bonus` vazios podem indicar que a mecanica de sorte nao esta implementada.
- **Proposta**: Corrigir typo. Avaliar expandir o texto para dar mais contexto a "donzela espectral".

---

## Evento 14 - Blood of the Abyss
- **Chave**: `resources.assets:2545544`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: "The yearning ghost extends her hand pleading for help." (mesmo texto dos Eventos 1 e 8)
- **Opcoes**: 2 (Reach / Leave)
- **Anomalias**: `disabled: 1`, mesmo texto placeholder dos eventos 1 e 8, `LeadsToFortune: 1`
- **Veredito**: MELHORAR
- **Justificativa**: Desativado + texto copiado de evento de fantasma (incompativel com "Blood of the Abyss").
- **Proposta**: Reescrever texto para algo relacionado ao abismo/sangue. Exemplo: "A crimson glow pulses from a fissure in the rock face, the air thick with a coppery scent. The ground trembles faintly, as though something vast stirs below."

---

## Evento 15 - Bonefire
- **Chave**: `resources.assets:2545546`
- **Categoria**: Normal | **Raridade**: Rare | **Peso**: 1.0
- **Texto original**: "A ghastly pyre dances with unnatural, green flames. It is a bonfire, fueled by an ominous collection of human bones that emits an eerie glow. As you watch the flickering flames, a wave of unnatural weariness descends upon you. The fire seems to burn not just with bones, but with the very life-force of those who gaze upon it..."
- **Opcoes**: 2 (Rest / Leave)
- **Anomalias**: `roll_bonus: ['', '']`, `dados_recompensa_final: null`
- **Veredito**: MANTER
- **Justificativa**: Texto atmosferico e tematico. Sem anomalias criticas.

---

## Evento 16 - Bonefire
- **Chave**: `resources.assets:2545548`
- **Categoria**: Normal | **Raridade**: Rare | **Peso**: 1.0
- **Texto original**: "A ghastly pyre dances with unnatural, green flames. It is a bonfire, fueled by an ominous collection of human bones that emits an eerie glow. As you watch the flickering flames, a wave of unnatural weariness descends upon you. The fire seems to burn not just with bones, but with the very life-force of those who gaze upon it..." (identico ao Evento 15)
- **Opcoes**: 2 (Rest / Leave)
- **Anomalias**: `roll_bonus: ['', '']`, `dados_recompensa_final: null`
- **Veredito**: MANTER
- **Justificativa**: Texto identico ao Evento 15. Podem ser intencionalmente duplicados (dois bonefires distintos no mapa) ou acidental. Sem erros de conteudo.

---

## Evento 17 - Bonfire
- **Chave**: `resources.assets:2545549`
- **Categoria**: Normal | **Raridade**: Uncommon | **Peso**: 1.0
- **Texto original**: "The flames of a Bonfire dance in the air, their warmth spreading like a welcoming embrace. Nothing like a warm fire to rest from your troubles."
- **Opcoes**: 3 (Rest / Reroll Skill / Level Up Fortunes)
- **Anomalias**: `roll_bonus: ['', '', '']`, `dados_recompensa_final: null`
- **Veredito**: MANTER
- **Justificativa**: Texto simples mas funcional. 3 opcoes boas. Sem anomalias criticas.

---

## Evento 18 - Bonfire
- **Chave**: `resources.assets:2545551`
- **Categoria**: Normal | **Raridade**: Uncommon | **Peso**: 1.0
- **Texto original**: "The flames of a Bonfire dance in the air, their warmth spreading like a welcoming embrace. Nothing like a warm fire to rest from your troubles." (identico ao Evento 17)
- **Opcoes**: 2 (Rest / Prepare)
- **Anomalias**: `roll_bonus: ['', '']`
- **Veredito**: MANTER
- **Justificativa**: Identico ao 17 no texto, mas com opcoes diferentes (Prepare em vez de Reroll Skill e Level Up Fortunes). Podem ser variantes intencionais do mesmo evento.

---

## Evento 19 - Bonfire Story
- **Chave**: `resources.assets:2545550`
- **Categoria**: Normal | **Raridade**: Uncommon | **Peso**: 1.0
- **Texto original**: VAZIO (string vazia no asset)
- **Opcoes**: 1 (Rest)
- **Anomalias**: Texto vazio
- **Veredito**: MELHORAR
- **Justificativa**: "Bonfire Story" sugere um evento narrativo na fogueira - texto vazio e inaceitavel para um evento que deve contar uma historia.
- **Proposta**: Escrever texto de narracao. Exemplo: "As you sit by the fire, a story surfaces from the ashes of the past..." - ou remover o evento se o conteudo narrativo ainda nao foi definido.

---

## Evento 20 - Boss
- **Chave**: `resources.assets:2545553`
- **Categoria**: Normal | **Raridade**: Common | **Peso**: 1.0
- **Texto original**: VAZIO (string vazia no asset)
- **Opcoes**: 1 (Fight!)
- **Anomalias**: Campos `chave`, `nome`, `dados_recompensa_final` NULL, `roll_bonus: ['']`
- **Veredito**: MELHORAR
- **Justificativa**: Um evento "Boss" sem texto e sem dados de recompensa e um erro grave. O jogador precisa saber contra quem esta lutando.
- **Proposta**: Adicionar texto descritivo do boss e investigar o campo `dados_recompensa_final` NULL. Exemplo: "A towering figure emerges from the darkness, its silhouette wreathed in shadow. The boss awaits."

---

## Inventario de Decisoes - Lote Normal (Eventos 1-20)

| Evento | Titulo | Veredito | Motivo principal |
|--------|--------|----------|-----------------|
| 1 | A Test of Fear | MELHORAR | disabled + texto placeholder duplicado + campos NULL |
| 2 | Acid Trap | MELHORAR | typo "appeaures" + opcao unica |
| 3 | Alchemist's Workbench | MELHORAR | descricoes de opcoes vazias + roll_bonus vazio |
| 4 | Ambush | MELHORAR | disabled + texto curto + opcao unica |
| 5 | Archery Competition | MANTER | Sem anomalias |
| 6 | Armor Chest | MELHORAR | texto vazio |
| 7 | Armor Chest | MELHORAR | texto vazio + duplicata do evento 6 |
| 8 | Barbarian Fisherman | MELHORAR | texto copiado do evento 1 (fantasma) |
| 9 | Battle | MELHORAR | texto vazio + dados_recompensa_final NULL + peso alto (5.0) |
| 10 | Battletest Event | MELHORAR | disabled + texto vazio + campos NULL + nome de teste |
| 11 | Bear Trap | MANTER | Sem anomalias |
| 12 | Below Zero | MANTER | Sem anomalias |
| 13 | Between Worlds | MELHORAR | typo "whisperes" + roll_bonus vazio |
| 14 | Blood of the Abyss | MELHORAR | disabled + texto copiado do evento 1 |
| 15 | Bonefire | MANTER | Sem anomalias criticas |
| 16 | Bonefire | MANTER | Sem anomalias criticas (duplicata do 15, possivelmente intencional) |
| 17 | Bonfire | MANTER | Sem anomalias criticas |
| 18 | Bonfire | MANTER | Sem anomalias criticas (variante do 17) |
| 19 | Bonfire Story | MELHORAR | texto vazio |
| 20 | Boss | MELHORAR | texto vazio + dados_recompensa_final NULL |

**Resumo**: MANTER = 6 eventos (Eventos 5, 11, 12, 15, 16, 17, 18)  
**Resumo**: MELHORAR = 13 eventos (Eventos 1, 2, 3, 4, 6, 7, 8, 9, 10, 13, 14, 19, 20)  
**Total analisado**: 20 de 20

---

## Anomalias consolidadas

| Tipo | Quantidade | Eventos afetados |
|------|-----------|-----------------|
| Texto vazio | 6 | 6, 7, 9, 10, 19, 20 |
| disabled: 1 | 5 | 1, 4, 8, 10, 14 |
| Campos NULL (chave/nome) | 7 | 1, 4, 9, 10, 14, 20 |
| Texto duplicado (ghost placeholder) | 3 | 1, 8, 14 |
| Duplicata funcional (mesmo titulo/opcao) | 1 par | 6 e 7 |
| Typo no texto | 2 | 2 ("appeaures"), 13 ("whisperes") |
| roll_bonus vazio | 13 | Todos exceto 5 |
| dados_recompensa_final: null | 6 | 4, 9, 10, 15, 16, 20 |
