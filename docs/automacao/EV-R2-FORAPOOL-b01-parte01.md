# EV-R2-FORAPOOL-b01 — parte 01: eventos 1–7

Status: PROPOSTAS PARA APROVAÇÃO DO DONO; nenhuma decisão aprovada e nenhuma implementação.
Fonte da ordem: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, primeiras 7 das 84 seções `## `. Dados: `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json`; semântica: `eventos.schema.json` e `schema.md`, no mesmo diretório. O catálogo e a auditoria completa das 21 chaves constam da parte04. Partes01–03 contêm os vereditos; parte04 é o inventário/auditoria, não propostas adicionais.

Regra de edição proposta: onde se cita TRECHO, substituir exatamente e apenas esse trecho no campo indicado; todos os demais bytes do campo, incluindo espaços, CR/LF, tags e placeholders, permanecem. Onde se cita CAMPO, a proposta é a string completa. Índices de opções/ações abaixo são base 1 (no JSON, índices de arrays são base 0). A fonte canônica permanece intocada.

NULL de resultado = NAO_EXERCITADO: ouro depende de nível/razão/GoldMultiplier, XP depende do estado e pode converter em ouro, itens dependem de nível/restrições/RNG, status não foi aplicado/sorteado, combate não foi executado. NULL de PPtr é outra coisa: referência nula configurada (`m_PathID=0`), não uma recompensa zero. A auditoria por campo da parte04 registra ambos. Disponibilidade, seleção de personagem e renderização de textos são NAO_EXERCITADO porque não se abriu o jogo.

## Inventário parcial — 7 eventos

| Nº | Chave | Título / variante | Categoria | Raridade (valor) | Peso relativo | Veredito proposto | Natureza |
|---|---|---|---|---|---|---|---|
| 1 | resources.assets:2545637 | Admiral Blackbeard / End | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 2 | resources.assets:2545545 | Bonefire / Roguelike Victory | NotInEventPool | Uncommon (1) | 1.0 | MELHORAR | wording |
| 3 | resources.assets:2545547 | Bonefire / Campaign Victory | NotInEventPool | Rare (2) | 1.0 | MELHORAR | wording |
| 4 | resources.assets:2545557 | Challenger's Gong / Victory 1 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 5 | resources.assets:2545558 | Challenger's Gong / Victory 2 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 6 | resources.assets:2545559 | Challenger's Gong / Victory 3 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 7 | resources.assets:2545649 | Consumed by Rage / Master of Rage - 1 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |

## 01 — Admiral Blackbeard — resources.assets:2545637

VEREDITO PROPOSTO: MELHORAR — wording. Manter recompensa, raridade, peso, pool e condições.

Campo `texto`, TRECHO atual: `an abyss where greed and power has led him.`
PROPOSTA EXATA: `an abyss where greed and power have led him.`
Campo `texto`, TRECHO atual: `The memories unveiled by these magical artifacts paints pictures of lives that had once been`
PROPOSTA EXATA: `The memories unveiled by these magical artifacts paint pictures of lives that had once been`
Justificativa: concordância de sujeitos plurais; não alterar a história do pai, dos dragões, da moeda ou do destino Frostwrought Mountain.

Anomalias/limites: `disabled=0`, `EditorOnly=0`; 0 opções; `texto_resultados_possiveis=""`. Texto longo com CR e `<br/>` deve permanecer. Não preencher o resultado vazio nem criar botão/recompensa. Há referência de vitória de `resources.assets:2545638` em `eventos.json`, `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`; ser NotInEventPool não prova inutilidade. Fluxo de continuação com 0 opções: NAO_EXERCITADO, sem jogo.

## 02 — Bonefire (Roguelike) — resources.assets:2545545

VEREDITO PROPOSTO: MELHORAR — wording. Preservar o título estilizado `Bonefire`, não assumir erro por ser diferente de `bonfire`.

Campo `texto`, TRECHO atual: `Despite your growing fatigue, you fight with relentless determination. Shattering bone after bone, extinguishing the eerie light in the skeletons' hollow eye sockets.`
PROPOSTA EXATA: `Despite your growing fatigue, you fight with relentless determination, shattering bone after bone and extinguishing the eerie light in the skeletons' hollow eye sockets.`
Campo opção 1 `texto`, CAMPO atual: `Sit by the fire and recover your strength.`
PROPOSTA EXATA: `Sit and recover your strength.`
Campo opção 2 `texto`, CAMPO atual: `""` (string vazia).
PROPOSTA EXATA: `Open the skill reroll menu.`
Campo opção 3 `texto`, CAMPO atual: `""` (string vazia).
PROPOSTA EXATA: `Level up your Fortunes to your character level.`
Justificativa: corrigir fragmento gramatical; a narrativa apaga a fogueira, portanto não prometer repouso ao lado de fogo aceso; explicar opções vazias usando apenas `openSkillRerollMenu=1` e `levelUpFortunesToCharacterLevel=1` dos campos originais. Não antecipar reroll concluído nem adicionar custo/skill garantida.

Anomalias/limites: `disabled=0`; 3 opções sem requisito/ocultação configurados. Resultado global e texto da ação Rest vazios; descrições das opções 2–3 vazias. Rest configura 50.0 em percentMaxHealth e percentMaxMana, não valor absoluto nem alvo final comprovado. Opções 2–3 têm 0 efeitos padrão, mas flags especiais ativas: NÃO são opções sem função comprovada. Entrada de vitória `resources.assets:2545546`. NULL finais/PPtrs: parte04; NAO_EXERCITADO aplicação da recuperação, menu e evolução de Fortunes.

## 03 — Bonefire (Campaign) — resources.assets:2545547

VEREDITO PROPOSTO: MELHORAR — wording; manter recuperação e Prepared.

Campo `texto`, TRECHO atual: `Despite your growing fatigue, you fight with relentless determination. Shattering bone after bone, extinguishing the eerie light in the skeletons' hollow eye sockets.`
PROPOSTA EXATA: `Despite your growing fatigue, you fight with relentless determination, shattering bone after bone and extinguishing the eerie light in the skeletons' hollow eye sockets.`
Campo opção 2 `texto`, CAMPO atual: `Take time to prepare for what's ahead.`
PROPOSTA EXATA: `Take time to prepare for what's ahead and gain Prepared for this quest.`
Justificativa: corrigir o fragmento e nomear o status configurado sem inventar valor de loot final. `Prepared`, `resources.assets:2545391`, é duração Quest no JSON; descrição autoral informa aumento de itens/ouro em 20%. Não mudar os modificadores.

Anomalias/limites: `disabled=0`; 2 opções sem ocultação configurada; resultado global e 2 textos de ação vazios. Rest configura 50.0 de percentMaxHealth/percentMaxMana. Manter filtros Campaign, horário configurado e terrenos, não fundir com a variante roguelike. Entrada de vitória `resources.assets:2545548`. NULL/PPtrs detalhados na parte04; recuperação e Prepared efetivos NAO_EXERCITADO.

## 04 — Challenger's Gong (Victory 1) — resources.assets:2545557

VEREDITO PROPOSTO: MELHORAR — wording. Manter as ondas de combate e encadeamento.

Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who will listen to his pleas?`
PROPOSTA EXATA: `Who will face the next challengers?`
Justificativa: não há súplica no texto; a pergunta deve refletir a escolha ligada ao desafio, sem alterar alvo ou dificuldade. Sua exibição é NAO_EXERCITADO, pois depende da UI.

Anomalias/limites: `disabled=0`; 1 opção Fight sem ocultação; resultado global e ação vazios. `batalha.iniciar=true`, referência direta NULL por PPtr=0, mas existem 4 inimigos forçados (Master Leo/Donnie/Mikey/Raph) e VictoryEvent `resources.assets:2545558`; não classificar a batalha como ausente. Entrada `resources.assets:2545560`. RewardModifiers/expressões não foram executados; não converter fórmulas em recompensa garantida. Parte04 registra os campos nulos.

## 05 — Challenger's Gong (Victory 2) — resources.assets:2545558

VEREDITO PROPOSTO: MELHORAR — wording. Manter tags e o nome Ronin.

Campo `texto`, TRECHO atual: `Battles erupte,`
PROPOSTA EXATA: `Battles erupt,`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who will listen to his pleas?`
PROPOSTA EXATA: `Who will confront Ronin?`
Justificativa: erro ortográfico e prompt herdado sem relação com o confronto. Não afirmar funcionamento da escolha sem UI.

Anomalias/limites: `disabled=0`; 1 opção Fight sem ocultação; resultado global e ação vazios. Batalha ativa, PPtr de batalha NULL e 1 inimigo forçado `resources.assets:2545135`; vitória leva a `resources.assets:2545559`. Entrada de `resources.assets:2545557`. Não inferir luta quebrada pela referência NULL. Aplicação dos overrides e renderização NAO_EXERCITADO.

## 06 — Challenger's Gong (Victory 3) — resources.assets:2545559

VEREDITO PROPOSTO: MELHORAR — wording. Manter Bloodied Bargain e os números originais.

Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who will take the ?`
PROPOSTA EXATA: `Who will receive the reward?`
Campo opção 1 `texto`, CAMPO atual: `You bear the honor of victory.`
PROPOSTA EXATA: `You bear the honor of victory and receive Bloodied Bargain.`
Justificativa: pergunta incompleta e prêmio pouco explícito. O efeito padrão tem um candidato fixo Bloodied Bargain (`resources.assets:2545412`, Fortune, Permanent, sortear=false); apenas nomear, não fixar `{8,40}` ou substituir tokens.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; resultado global e ação vazios; BattleOverrideInfo ainda contém inimigo Ronin e VictoryEvent para a própria chave, MAS `batalha.iniciar=false`. É configuração residual, não prova de loop ativo. Entrada de `resources.assets:2545558` e autorreferência inativa. Não limpar essas configurações nesta proposta. Aplicação de Fortune e comportamento efetivo NAO_EXERCITADO.

## 07 — Consumed by Rage — resources.assets:2545649

VEREDITO PROPOSTO: MELHORAR — wording; manter condição, penalidade e remoção de status.

Campo `texto`, TRECHO atual: `Each bares horns sprouting from their skulls`
PROPOSTA EXATA: `Each bears horns sprouting from their skulls`
Campo opção 1 `texto`, CAMPO atual: `Slay the Wendigo.`
PROPOSTA EXATA: `Slay the wendigos.`
Campo opção 2 `texto`, CAMPO atual: `No amount of anger can convince you to stay.`
PROPOSTA EXATA: `Leave the pass. This choice applies Enfeebled and is configured to remove Rage Unleashed.`
Campo opção 2, ação 1 `texto`, TRECHO atual: `Courage and determination bleeds away`
PROPOSTA EXATA: `Courage and determination bleed away`
Justificativa: bear/bare, concordância e plural coerente com os 4 inimigos configurados. Explicitar a penalidade já existente: candidato `Enfeebled` (`resources.assets:2545494`, Quest) e regra de remoção `ActionStatus.Name == "Rage Unleashed"`; não transformar Leave em saída neutra nem inventar uma penalidade nova.

Anomalias/limites: `disabled=0`; 2 opções sem ocultação configurada. Prompt `Who will listen to his pleas?` também destoa; proposta adicional de CAMPO: `Who will face the wendigos?`. Fight inicia batalha, referência NULL por PPtr=0, 4 entradas do inimigo `resources.assets:2545299`, vitória `resources.assets:2545650`. Não encontrada entrada de outro PartyEvent na leitura inicial; a busca completa do catálogo na parte04 verifica vínculos de status, sem tratar ausência como evento inacessível. NAO_EXERCITADO: alvo efetivo, stacks de Enfeebled, remoção de Rage Unleashed e resultado do combate.

Contagem desta parte: 7 eventos, 7 MELHORAR (wording), 0 MANTER; 0 propostas de mudança de recompensa e 0 de condição. Aprovação do dono: PENDENTE para as 7 chaves. NULL nunca foi tratado como zero.
