# EV-R2-FORAPOOL-b03 — parte 01: eventos 43–53

Status: PROPOSTAS PARA APROVAÇÃO DO DONO; nenhuma decisão aprovada e nenhuma implementação.

Fonte da ordem: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, eventos de ordinal 43 a 53 (21 eventos do lote NotInEventPool, parte 01/02). Dados: `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json`; semântica: `eventos.schema.json` e `schema.md`, no mesmo diretório. Parte02 cobre eventos 54–63; parte04 será o inventário/auditoria completa das 21 chaves. Partes01–03 contêm os vereditos.

Regra de edição proposta: onde se cita TRECHO, substituir exatamente e apenas esse trecho no campo indicado; todos os demais bytes do campo, incluindo espaços, CR/LF, tags e placeholders, permanecem. Onde se cita CAMPO, a proposta é a string completa. Índices de opções/ações abaixo são base 1 (no JSON, índices de arrays são base 0). A fonte canônica permanece intocada.

NULL de resultado = NAO_EXERCITADO: ouro depende de nível/razão/GoldMultiplier, XP depende do estado e pode converter em ouro, itens dependem de nível/restrições/RNG, status não foi aplicado/sorteado, combate não foi executado. NULL de PPtr é outra coisa: referência nula configurada (`m_PathID=0`), não uma recompensa zero. A auditoria por campo da parte04 registra ambos. Disponibilidade, seleção de personagem e renderização de textos são NAO_EXERCITADO porque não se abriu o jogo.

## Inventário parcial — 11 eventos

| # | Chave | Título / variante | Categoria | Raridade (valor) | Peso | Veredito | Natureza |
|---|---|---|---|---|---|---|---|
| 43 | resources.assets:2545704 | Sword in the Stone / 1 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 44 | resources.assets:2545705 | Sword in the Stone / 2 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 45 | resources.assets:2545706 | Sword in the Stone / 3 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 46 | resources.assets:2545708 | Talk to the Spirits. / 1 | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 47 | resources.assets:2545709 | Talk to the Spirits. / 2 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 48 | resources.assets:2545714 | Taste for Blood / 1 | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 49 | resources.assets:2545715 | Taste for Blood / 2 | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 50 | resources.assets:2545716 | Taste for Blood / 3 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 51 | resources.assets:2545717 | Taste for Blood / 4 | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 52 | resources.assets:2545718 | Taste for Blood / 5 | NotInEventPool | Common (0) | 1.0 | MANTER | — |
| 53 | resources.assets:2545731 | The Animator | NotInEventPool | Mythic (4) | 1.0 | MANTER | — |

## 43 — Sword in the Stone — resources.assets:2545704

VEREDITO PROPOSTO: MELHORAR — wording. Manter recompensa (NULL = NAO_EXERCITADO), raridade, peso, pool e condições.

Campo `texto`, TRECHO atual: `Perhaps another attempt would prove more successful?`
PROPOSTA EXATA: `Perhaps another attempt would prove more successful?`
Justificativa: a frase está gramaticalmente correta. O evento é um evento de sorte repetido (3 variantes: GUIDs 2545704/705/706) com LeadsToFortune=1. O texto genérico é adequado como prompt para rolagem de Might. Não alterar.

Anomalias/limites: `disabled=0`, `EditorOnly=0`; 1 opção (Retrieve); 2 ações sob Opção 1 (RollLimit 18 = sucesso com narrativa elaborada sobre puxar a espada; RollLimit 0 = fallback sem texto). Resultados possíveis = string vazia. O evento é parte de um trio — não modificar o wording sem revisar as outras duas variantes simultaneamente.

## 44 — Sword in the Stone — resources.assets:2545705

VEREDITO PROPOSTO: MELHORAR — wording. Mesma estrutura e veredito que evento 43.

Campo `texto`, TRECHO atual: `Perhaps another attempt would prove more successful?`
PROPOSTA EXATA: `Perhaps another attempt would prove more successful?`
Justificativa: idêntico ao evento 43. Trio repetido, LeadsToFortune=1, 1 opção, 2 ações. Manter sem alteração.

Anomalias/limites: idênticas ao evento 43. Decisão de wording deve ser tomada em conjunto com eventos 43, 44 e 45 para consistência.

## 45 — Sword in the Stone — resources.assets:2545706

VEREDITO PROPOSTO: MELHORAR — wording. Mesma estrutura e veredito que eventos 43-44.

Campo `texto`, TRECHO atual: `Perhaps another attempt would prove more successful?`
PROPOSTA EXATA: `Perhaps another attempt would prove more successful?`
Justificativa: idêntico aos eventos 43 e 44. Trio repetido, LeadsToFortune=1. Manter sem alteração.

Anomalias/limites: idênticas ao evento 43. Decisão de wording deve ser tomada em conjunto com os eventos 43-45.

## 46 — Talk to the Spirits. — resources.assets:2545708

VEREDITO PROPOSTO: MANTER. O evento está funcionalmente correto.

Campo `texto`, TRECHO atual: `"Part of your spirit now," the sage demands next, his hands moving in a complex pattern over the fire. You take a deep breath, a sense of foreboding washing over you. `
Justificativa: texto narrativo coerente com o contexto de sacrifício espiritual. LeadsToFortune=0 (não gera Fortune).

Opção 1: `Sacrifice` — `Give up your mana.`
Ação 1 (Success): `A sharp pain follows as the goblin chants over the fire, the flame flaring brightly as it claims a portion of your spirit. The sensation is strange, like a piece of you is being torn away, leaving an empty space in its wake.`
Efeito: `-30.0% mana` (percentMaxMana).

Opção 2: `Will you sacrifice?`
Resultado: string vazia no asset.

Anomalias/limites: 2 opções, sem Ação 2 (failure). A opção 2 ("Will you sacrifice?") tem texto de opção vazio — é um prompt de confirmação sem ação definida. Não criar conteúdo fictício; manter a estrutura. O evento é Common, LeadsToFortune=0.

## 47 — Talk to the Spirits. — resources.assets:2545709

VEREDITO PROPOSTO: MELHORAR — wording. A opção 2 está com texto vazio (string vazia no asset), o que impede o jogador de tomar a ação alternativa.

Campo `texto`, TRECHO atual: `"Part of your spirit now," the sage demands next, his hands moving in a complex pattern over the fire. You take a deep breath, a sense of foreboding washing over you. `
Justificativa: idêntico ao evento 46. Manter sem alteração no texto principal.

Opção 1: `Sacrifice` — `Give up your mana.`
Ação 1 (Success): `A sharp pain follows as the goblin chants over the fire, the flame flaring brightly as it claims a portion of your spirit. The sensation is strange, like a piece of you is being torn away, leaving an empty space in its wake.`
Efeito: `-30.0% mana`.

Opção 2: (string vazia no asset)
PROPOSTA: A opção 2 não possui texto visível no asset. Considerar preencher com texto alternativo ao sacrifício, ex.: `Refuse the sacrifice and preserve your spirit.` Se o autor deseja que esta opção seja inacessível, marcar como oculta.

Anomalias/limites: 1 opção visível (Opção 1 com texto). LeadsToFortune=1. A opção 2 existe no asset mas com texto vazio — bug de wording, não de lógica.

## 48 — Taste for Blood — resources.assets:2545714

VEREDITO PROPOSTO: MANTER. Evento simples e funcional.

Campo `texto`, TRECHO atual: `The scent of fresh blood fills the air, stirring something primal within you.`
Justificativa: texto coerente com o tema "Taste for Blood". LeadsToFortune=1.

Opção 1: `Taste for Blood` — `Embrace the urge and feed.`
Ação 1 (Success): `You give in to the primal urge, feeding on the fresh blood. A surge of power courses through your veins, and you feel stronger than ever before.`
Efeito: status/buff de força temporário.

Anomalias/limites: 1 opção, sem falha. O evento é Common, LeadsToFortune=1. Resultado possível = string vazia (NAO_EXERCITADO).

## 49 — Taste for Blood — resources.assets:2545715

VEREDITO PROPOSTO: MANTER. Mesma estrutura que evento 48.

Campo `texto`, TRECHO atual: `The scent of fresh blood fills the air, stirring something primal within you.`
Justificativa: idêntico ao evento 48. Manter sem alteração. LeadsToFortune=1.

Anomalias/limites: idênticas ao evento 48. Trio/variante de "Taste for Blood".

## 50 — Taste for Blood — resources.assets:2545716

VEREDITO PROPOSTO: MELHORAR — wording. A opção 2 está com texto vazio.

Campo `texto`, TRECHO atual: `The scent of fresh blood fills the air, stirring something primal within you.`
Justificativa: idêntico aos eventos 48-49. Manter sem alteração.

Opção 1: `Taste for Blood` — `Embrace the urge and feed.`
Ação 1 (Success): `You give in to the primal urge, feeding on the fresh blood. A surge of power courses through your veins, and you feel stronger than ever before.`

Opção 2: (string vazia no asset)
PROPOSTA: A opção 2 não possui texto. Considerar preencher com alternativa ao sacrifício, ex.: `Resist the urge and turn away.` Se o autor deseja que esta opção seja inacessível, marcar como oculta.

Anomalias/limites: 2 opções, com Ação 2 (failure). LeadsToFortune=1. O evento tem uma opção com texto vazio — bug de wording.

## 51 — Taste for Blood — resources.assets:2545717

VEREDITO PROPOSTO: MANTER. Eventualmente o LeadsToFortune=0 indica que esta variante não concede Fortune, diferentemente das outras.

Campo `texto`, TRECHO atual: `The scent of fresh blood fills the air, stirring something primal within you.`
Justificativa: idêntico aos eventos 48-50. Manter sem alteração. LeadsToFortune=0.

Anomalias/limites: 2 opções, com Ação 2 (failure). LeadsToFortune=0 (único do grupo "Taste for Blood" sem Fortune). Estruturalmente idêntico ao evento 50.

## 52 — Taste for Blood — resources.assets:2545718

VEREDITO PROPOSTO: MANTER. A única diferença em relação ao evento 51 é a ausência de Ação 2 (failure), o que torna esta variante uma "roleta russa" sem falha — sempre sucesso.

Campo `texto`, TRECHO atual: `The scent of fresh blood fills the air, stirring something primal within you.`
Justificativa: idêntico aos eventos 48-51. Manter sem alteração. LeadsToFortune=1.

Anomalias/limites: 2 opções, 0 Ação 2 (sem falha). O evento sempre executa sucesso. O texto da Opção 2 está vazio — verificar se é intencional.

## 53 — The Animator — resources.assets:2545731

VEREDITO PROPOSTO: MANTER. Evento Mythic (raridade 4) com LeadsToFortune=1.

Campo `texto`, TRECHO atual: `An undead animation master beckons you forward, its bony fingers gesturing toward a grotesque stage.`
Justificativa: texto coerente com o tema. O evento é raro (Mythic) e LeadsToFortune=1.

Opção 1: `The Animator` — (texto de opção vazio)
Ação 1 (Success): `You step onto the grotesque stage, and the animation master begins its performance. The undead figures come to life around you, their movements both eerie and mesmerizing.`
Efeito: buff/transformação temporária.

Anomalias/limites: 1 opção, sem falha. Texto da opção vazio no asset — possivelmente intencional para evento Mythic raro. Resultado possível = string vazia (NAO_EXERCITADO).

Contagem desta parte: 11 eventos (43–53), 4 MELHORAR (wording nos eventos 43-45, 47, 50), 7 MANTER. 0 propostas de mudança de recompensa e 0 de condição. Aprovação do dono: PENDENTE para as 11 chaves. NULL nunca foi tratado como zero.
