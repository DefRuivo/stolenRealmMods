# EV-R2-NORMAL-b01 — parte 02: eventos 1–20 do lote Normal (correção da parte01)

Status: **PROPOSTAS PARA APROVAÇÃO DO DONO**; nada implementado no jogo, nenhuma decisão aprovada.
Natureza: documento corretivo da parte01 (`EV-R2-NORMAL-b01-parte01.md`, mantida intacta como registro da entrega reprovada).
Origem: revisão independente `t_4c07d669` (parecer: REPROVAR a parte01 e corrigir). Cartão original `t_d61a5d8d`; cartão corretivo `t_67a3887a`.

## 0. Escopo, fontes e regras

Faixa exata: seções 1–20 do lote **Normal** (20 eventos), na ordem do JSON `categoria = Normal` — a mesma ordem do `lote-Normal-v2.md`. Não se ordena por `path_id` (a faixa não é monotônica: #19=2545550 e #20=2545553 vêm depois de #18=2545551).

Fontes (somente leitura): `C:/dev/stolen-realm/docs/cobertura/EV-R1/{eventos.json, lote-Normal-v2.md, eventos.schema.json, catalogo-referencias.json}`.
Nada de jogo, DLL/plugin, balanceamento implementado, publicação, commit ou push. Ajustes manuais do dono e todas as entregas anteriores permanecem intocados.

Regra de edição proposta: onde o item diz **CAMPO**, a proposta substitui a string inteira do campo indicado; onde diz **TRECHO**, substitui exatamente o trecho citado e preserva todos os demais bytes (espaços, CR/LF, tags `<...>` e placeholders). Índices são base 1 no documento e base 0 no JSON (aqui os JSONPath já estão em base 0, prontos para uso).
Textos de jogo são mantidos em **inglês**; PT-BR aparece apenas como tradução explicitamente marcada — neste lote não há proposta de tradução.

## 1. Integridade das fontes

| Fonte | SHA256 conferido |
|---|---|
| `eventos.json` | `4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13` |
| `lote-Normal-v2.md` | `83b30ada3d78e596b8c7c0784d5e741b43654b14ab02d5377d8a1b245b84f146` |
| `eventos.schema.json` | `6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc` |
| `catalogo-referencias.json` | `94077cc887621933abe7bbbbd96e91c5a887478dba8fd000b8f4a4129c3745a5` |

Integridade verificada pela auditoria automática (seção 7): 4/4 fontes com SHA256 estável; `EV-R2-NORMAL-b01-parte01.md` inalterada em `e65daa3413e18adc1d73b6272d936f8d7d593da83e90abfbb06c34f6aee530e9`.

## 2. Semântica usada (NULL, disabled, runtime)

- **NULL de resultado** = NAO_EXERCITADO. Ouro depende de nível/razão/multiplicador, experiência depende do estado da partida, itens dependem de nível/restrições/RNG, status não foi sorteado e combate não foi executado. Campo com `null` e `motivo` explícito **não** prova defeito nem ausência de configuração.
- **NULL de PPtr** (`m_PathID = 0`) = referência nula gravada no asset, com motivo declarado. Não é GUID ausente, não é falha de deploy.
- **disabled / EditorOnly** = estado de autoria, não bug. Este documento **não** propõe reativar, remover ou criar slots/opções por inferência; onde há proposta em evento desativado, ela é explicitamente condicional à decisão do autor.
- **Renderização** (o que o jogador vê de fato na tela) é NAO_EXERCITADO: não se abriu o jogo. Nenhuma conclusão sobre exibição, substituição de tokens ou efeito final é apresentada como exercitada.

## 3. Supersessão nominal das acusações da parte01

| # | Acusação na parte01 | Situação | Consta agora em |
|---|---|---|---|
| 1 | Campo `roll_bonus` vazio em 13 eventos ("Todos exceto 5") | SUPERSEDIDA: o campo `roll_bonus` não existe no JSON; o caminho real é `$.opcoes[*].rolagem.bonus`. Bônus configurado em #2 (Vitality), #3 (Intelligence+3 nas três opções), #5 (Might+Dexterity) e #11 (Might); vazios em 26 dos 32 slots de opção. | §6 |
| 2 | #1: `chave`/`nome` NULL = "GUID do evento não populado" e "falha do pipeline de deploy" | REFUTADA: não existem campos `chave`/`nome` no topo do esquema de evento. O evento tem chave própria `resources.assets:2545531` e id `0c69ab75-e61b-4f82-9bd6-3f5b9d6cbfcf`. O NULL está em `$.opcoes[0].condicoes.status_requeridos[0].chave/nome`, com motivo `m_PathID=0`. | §5 #1 |
| 3 | Tabela de anomalias: "Campos NULL (chave/nome) = 7 eventos (1,4,9,10,14,20)" | REFUTADA: a lista traz 6 números, não 7; e PPtr nulo chave/nome aparece nos 20 eventos — não é anomalia distintiva (#1 continua tendo, porém, o placeholder sem status). | §6 |
| 4 | #9 e #20: `batalha.dados_recompensa_final` NULL = recompensa de batalha/sistema de recompensas não configurado | REFUTADA: o campo traz motivo explícito de resolução em runtime (não exercitado). NULL de resultado ≠ referência nula ≠ recompensa inexistente. | §5 #9, §5 #20 |
| 5 | #2: typo literal "appeaures" | REFUTADA: o literal real do original é `appeares`. A direção da correção (`appears`) continua válida e agora é registrada com o literal correto. | §5 #2 |
| 6 | #3: "`roll_bonus` vazio pode indicar que a mecânica de rolagem não está implementada" | REFUTADA pelo catálogo: `$.opcoes[*].rolagem.bonus=[{valor:3,nome:Intelligence}]` e as quatro ações de cada opção concedem itens reais (`itens.dar=true`, tabela `mustGetOne=1`, `Chance=100`), 12 `ItemInfo` distintos do catálogo. | §5 #3, §6 |
| 7 | #13: "`roll_bonus` vazio pode indicar que a mecânica de sorte não está implementada" | REFUTADA: bônus de rolagem vazio é o padrão da faixa (26/32 slots) e as ações de #13 são Success com `limite_rolagem=0`; nada indica rolagem quebrada. Permanece só o typo `whisperes`. | §5 #13 |
| 8 | #7: "Idêntico ao Evento 6 — duplicata funcional" | IMPRECISA: os assets diferem em `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.quantidade_configurada` (2 em #6, 1 em #7) e no caminho de recurso (`events/armor chest - roguelike` vs `events/armor chest`). | §5 #6, §5 #7, §6 |
| 9 | Resumo: "MANTER = 6 eventos" com lista de 7 | CORRIGIDA: **MANTER = 7** (#5, #11, #12, #15, #16, #17, #18); **MELHORAR = 13**. | §4, §6 |
| 10 | #10: "Se for realmente um evento de teste, removê-lo" | RETIRADA: excluir (ou reativar) conteúdo desativado por inferência não é correção de texto. A proposta de #10 é condicional e não altera `$.condicoes.disabled`. | §5 #10 |
| 11 | #1: "Reativar (`disabled: 0`)" | RETIRADA: estado de autoria. Nenhuma proposta deste documento altera `disabled`. | §5 #1, §2 |
| 12 | #4: "Reativar e expandir; adicionar opção Fight" | RETIRADA: criar opção nova é decisão de design do autor; a proposta agora é exata e incide só na descrição da opção existente e no que as ações reais mostram. | §5 #4 |
| 13 | #9: "Investigar por que `dados_recompensa_final` é NULL" | SUPERSEDIDA: o motivo está no próprio JSON (runtime não exercitado). Não há o que investigar offline. | §5 #9 |
| 14 | #16: "Texto idêntico ao 15; podem ser duplicados ou acidente" | MANTIDA como observação factual, sem tratamento de defeito: textos idênticos, porém chaves, ids e caminhos de recurso distintos. O mesmo vale para o par #17/#18. | §5 #15, §5 #16, §5 #18, §6 |
| 15 | Classe de achado "Título repetido" tratado como registro duplicado | CORRIGIDA: título repetido não é id nem chave repetidos. A única repetição real de identificador na faixa é o **id** de #9 e #10 (achado novo desta correção). | §6 |

## 4. Inventário dos 20 registros

| # | Chave (file:path_id) | id | Título | Categoria | Raridade | Peso | Veredito | Natureza |
|---|---|---|---|---|---|---|---|---|
| 1 | `resources.assets:2545531` | `0c69ab75-e61b-4f82-9bd6-3f5b9d6cbfcf` | A Test of Fear | Normal | Common (0) | 1.0 | **MELHORAR** | texto-de-opcao com placeholder sem status configurado (slot disabled observado, sem reativação proposta) |
| 2 | `resources.assets:2545532` | `c2ae71a3-938b-4960-8677-afa374d05527` | Acid Trap | Normal | Common (0) | 1.0 | **MELHORAR** | typo no texto original (sugestão de correção do ORIGINAL, não do EV-R1) |
| 3 | `resources.assets:2545533` | `6172b8ad-6e95-43e8-adf8-9c16b209974f` | Alchemist's Workbench | Normal | Common (0) | 1.0 | **MELHORAR** | descrição de opção ausente |
| 4 | `resources.assets:2545534` | `9b6cad84-c7d1-4910-94ba-537d33a5749a` | Ambush | Normal | Common (0) | 1.0 | **MELHORAR** | descrição de opção ausente + estrutura de rolagem observada |
| 5 | `resources.assets:2545535` | `053565ee-baf0-4218-a394-c9058037e80f` | Archery Competition | Normal | Common (0) | 1.0 | **MANTER** | — |
| 6 | `resources.assets:2545536` | `70c65d79-70fd-4541-b3cb-083f7055c346` | Armor Chest | Normal | Uncommon (1) | 1.0 | **MELHORAR** | texto narrativo ausente (evento de tesouro) |
| 7 | `resources.assets:2545537` | `c6676bef-432e-4eb5-bed7-46664d0b4811` | Armor Chest | Normal | Uncommon (1) | 1.0 | **MELHORAR** | texto narrativo ausente (evento de tesouro, variante de #6) |
| 8 | `resources.assets:2545538` | `c1938011-6b33-47ba-888d-cbfebce87b1c` | Barbarian Fisherman | Normal | Common (0) | 1.0 | **MELHORAR** | texto incompatível com o título (reuso literal do texto de #1/#14) |
| 9 | `resources.assets:2545539` | `5b740c2b-3480-48f2-997b-88c8291db0c0` | Battle | Normal | Common (0) | 5.0 | **MELHORAR** | texto narrativo ausente (evento de combate) |
| 10 | `resources.assets:2545540` | `5b740c2b-3480-48f2-997b-88c8291db0c0` | Battletest Event | Normal | Common (0) | 5.0 | **MELHORAR** | texto narrativo ausente em conteúdo de teste |
| 11 | `resources.assets:2545541` | `7f5372ca-ad4a-461d-bf2d-086103b7c5d2` | Bear Trap | Normal | Common (0) | 1.0 | **MANTER** | — |
| 12 | `resources.assets:2545542` | `75bdb92c-6950-454d-9419-0ada4e886f77` | Below Zero | Normal | Common (0) | 1.0 | **MANTER** | — |
| 13 | `resources.assets:2545543` | `e4acbfa7-bf37-42fb-aa13-e039e4339487` | Between Worlds | Normal | Common (0) | 1.0 | **MELHORAR** | typo no texto original (sugestão de correção do ORIGINAL) |
| 14 | `resources.assets:2545544` | `70d9f977-f25b-4f47-ac09-30f12be404f2` | Blood of the Abyss | Normal | Common (0) | 1.0 | **MELHORAR** | texto incompatível com o título (reuso literal do texto de #1/#8) |
| 15 | `resources.assets:2545546` | `ae42559a-dc07-4d70-b089-64b9aa50f829` | Bonefire | Normal | Rare (2) | 1.0 | **MANTER** | — |
| 16 | `resources.assets:2545548` | `b2cbffb6-4ee2-48f5-9c10-4fc110764f3f` | Bonefire | Normal | Rare (2) | 1.0 | **MANTER** | — |
| 17 | `resources.assets:2545549` | `13fb829a-cc27-44ce-aa4d-f3bfeb53d884` | Bonfire | Normal | Uncommon (1) | 1.0 | **MANTER** | — |
| 18 | `resources.assets:2545551` | `84b23e39-7e88-44f4-b86a-a580193d88d5` | Bonfire | Normal | Uncommon (1) | 1.0 | **MANTER** | — |
| 19 | `resources.assets:2545550` | `f0c60be1-d947-4518-8cc0-8533847a22f3` | Bonfire Story | Normal | Uncommon (1) | 1.0 | **MELHORAR** | texto narrativo ausente em evento StoryOnly |
| 20 | `resources.assets:2545553` | `6c1fb16d-e9b4-453a-8bb1-eaaa5892c4e8` | Boss | Normal | Common (0) | 1.0 | **MELHORAR** | texto narrativo ausente (evento de chefe) |

MANTER = 7 (#5, #11, #12, #15, #16, #17, #18)
MELHORAR = 13 (#1, #2, #3, #4, #6, #7, #8, #9, #10, #13, #14, #19, #20)
Total analisado = 20 de 20 · propostas exatas = 21

## 5. Registros

### 1 — A Test of Fear — resources.assets:2545531

- id: `0c69ab75-e61b-4f82-9bd6-3f5b9d6cbfcf`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=1, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/a test of fear` | sha256_objeto: `4464962ad186724bb5b607718d86af80491202fdce1ede06778b401ad523441d`
- texto original (54 chars):

```
The yearning ghost extends her hand pleading for help.
```
- opções (2):
  - 1) `Reach` — descrição: `You reach out to the ghost. Gain [o1a1_status].`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 2) `Leave` — descrição: `The chill in the air causes you to hesitate. You leave without helping.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- Texto do evento (54 chars) reaparece literalmente em #8 e #14.
- Opção 1 'Reach' pede '[o1a1_status]' no texto, mas $.opcoes[0].condicoes.status_requeridos[0] é PPtr nulo (m_PathID=0) e $.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos=[] — nenhum status é concedido.
- $.condicoes.disabled=1: registrado como estado, não como defeito a corrigir por inferência.

Propostas exatas (2):

- **1.1** [CAMPO] `$.opcoes[0].texto`
    antes: `You reach out to the ghost. Gain [o1a1_status].`
    depois: `You reach out to the ghost.`
  alvo/condição: conforme justificativa do registro; nota: Remove o token sem candidato configurado. Alternativa de autoria: configurar status real em $.opcoes[0].condicoes.status_requeridos[0] e $.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos (não propomos status inventado).

- **1.2** [CAMPO] `$.opcoes[0].efeitos[0].texto`
    antes:
```
You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.

You gain [o1a1_status].
```
    depois:
```
You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.
```
  alvo/condição: conforme justificativa do registro; nota: Idem 1.1 na prosa de ativação; mesmo placeholder, mesmo campo vazio de candidatos.

---

### 2 — Acid Trap — resources.assets:2545532

- id: `c2ae71a3-938b-4960-8677-afa374d05527`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/acid trap` | sha256_objeto: `f0884a41ba1ba4d6b4d436a31d21aa8d82819e9b0289f659d2ca11bd7e6714a1`
- texto original (393 chars):

```
You come across a statue of a snake carved from what appeares to be solid stone. Its gemstone eyes gleam dangerously, as a cloud of greenish fumes billow forth from its maw. An acrid, burning smell fills the air, stinging your nostrils forcing you back.

Someone with the constitution to weather the poisonous fumes might be able to jam the deadly <incr><b><green>Acid Trap</green></b></incr>.
```
- texto_resultados_possiveis: `Who will attempt to disable the trap?`
- opções (1):
  - 1) `Disable` — descrição: `Attempt to disable the Acid Trap.`; rolagem.bonus=[{"valor": 2, "nome": "Vitality"}]; misteriosa=False; ações: Success lim 10, Failure lim 1

**VEREDITO: MELHORAR**

Justificativa:
- Literal real do original é 'appeares' (a parte01 citou 'appeaures', que não existe na fonte).
- Opção única 'Disable' com bonus={valor:2,nome:Vitality}; Success limite 10 concede experiência (dar=true); Failure limite 1 aplica -20 percentMaxHealth e status Battered (resources.assets:2545489).
- Acrescentar opção 'Leave' seria mudança de conteúdo (decisão do autor), não correção de texto — não proposta aqui.

Propostas exatas (1):

- **2.1** [TRECHO] `$.texto`
    antes: `appeares`
    depois: `appears`
  alvo/condição: conforme justificativa do registro; nota: antes→depois do TEXTO ORIGINAL; nenhum arquivo do jogo/EV-R1 é editado.

---

### 3 — Alchemist's Workbench — resources.assets:2545533

- id: `6172b8ad-6e95-43e8-adf8-9c16b209974f`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/alchemist's workbench` | sha256_objeto: `cfb29209fae7a2ed08983392649cd8dda8021d458a6ba51a7532971bc6abf738`
- texto original (439 chars):

```
You stumble across an ornate table cluttered with scrolls, flasks, and various arcane implements - clearly an <b><blue><incr>Alchemist's Workbench</incr></blue></b>. The air is thick with the scent of ancient herbs and lingering magic, a tantalizing aroma for any adventurer.

On the table lay an open scroll, the elegant elvish script detailing recipes for various magical potions. The instructions, although intricate, are clear enough. 
```
- opções (3):
  - 1) `Potion of Power` — descrição: (vazia); rolagem.bonus=[{"valor": 3, "nome": "Intelligence"}]; misteriosa=True; ações: Success lim 1, Success lim 6, Success lim 12, Success lim 16
  - 2) `Mixture of Motion` — descrição: (vazia); rolagem.bonus=[{"valor": 3, "nome": "Intelligence"}]; misteriosa=True; ações: Success lim 1, Success lim 6, Success lim 12, Success lim 16
  - 3) `Tonic of Toughness` — descrição: (vazia); rolagem.bonus=[{"valor": 3, "nome": "Intelligence"}]; misteriosa=True; ações: Success lim 1, Success lim 6, Success lim 12, Success lim 16

**VEREDITO: MELHORAR**

Justificativa:
- As três opções têm $.opcoes[*].texto='' (vazio) e $.opcoes[*].rolagem.misteriosa=true.
- Alegação de recompensa da parte01 REFUTADA pelo catálogo: $.opcoes[0].efeitos[*].efeitos[0].recompensas.itens.dar=true com tabelas mustGetOne=1/Chance=100 — opção 1: Bottled Anger(2546488)/Rage(2546491)/Fury(2546489)/Wrath(2546492); opção 2: Oil of Momentum(2546526)/Speed(2546528)/Alacrity(2546525)/Acceleration(2546524); opção 3: Potion of Endurance(2546549)/Vitality(2546553)/Fortitude(2546550)/Life(2546551).
- $.opcoes[*].rolagem.bonus=[{valor:3,nome:Intelligence}] (RollBonusType 3=Intelligence): bônus de rolagem configurado, não vazio.
- As quatro ações de cada opção têm limite_rolagem 1/6/12/16, todas Success (sem Failure).

Propostas exatas (3):

- **3.1** [CAMPO] `$.opcoes[0].texto`
    antes: (string vazia "")
    depois: `Brew the crimson draught the scroll describes.`
  alvo/condição: conforme justificativa do registro; nota: Fundamentado na ação 1: 'should turn a bright red'.

- **3.2** [CAMPO] `$.opcoes[1].texto`
    antes: (string vazia "")
    depois: `Mix the sweet-smelling draught the scroll describes.`
  alvo/condição: conforme justificativa do registro; nota: Fundamentado na ação 1: 'should release a sweet aroma'.

- **3.3** [CAMPO] `$.opcoes[2].texto`
    antes: (string vazia "")
    depois: `Prepare the silver tonic the scroll describes.`
  alvo/condição: conforme justificativa do registro; nota: Fundamentado na ação 1: 'should turn a bright silver'.

---

### 4 — Ambush — resources.assets:2545534

- id: `9b6cad84-c7d1-4910-94ba-537d33a5749a`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=1, EditorOnly=0, minLevel=2, allowedNodeTypes=[0], historia=NonStoryOnly
- asset: `events/ambush` | sha256_objeto: `c14aef696adf3f852bca55d4819207aeaada241cd9561d5388cebf8de4cab30d`
- texto original (195 chars):

```
A silence hangs heavy and foreboding. You feel a shiver of unease, a sense of impending danger that seems to seep from the shadows. Your hand instinctively strays to the handle of your weapon... 
```
- opções (1):
  - 1) `Steel Yourself` — descrição: (vazia); rolagem.bonus=[]; misteriosa=False; ações: Success lim 10, Failure lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.opcoes[0].titulo='Steel Yourself', $.opcoes[0].texto='' (vazio).
- $.opcoes[0].efeitos[0] (Success, limite_rolagem=10) e $.opcoes[0].efeitos[1] (Failure, limite_rolagem=0) ambos com batalha.iniciar=true: a rolagem muda o texto, não o resultado (combate nos dois ramos).
- allowedNodeTypes=[0] (NodeType 0=NormalFight) e minLevel=2; $.condicoes.disabled=1 registrado como estado — não propomos reativar nem criar/remover opções.

Propostas exatas (1):

- **4.1** [CAMPO] `$.opcoes[0].texto`
    antes: (string vazia "")
    depois: `Steady your nerves — the ambush springs either way.`
  alvo/condição: conforme justificativa do registro; nota: Fundamentado nos dois textos de ação reais ('you ready yourself for battle' / 'your enemies surround you').

---

### 5 — Archery Competition — resources.assets:2545535

- id: `053565ee-baf0-4218-a394-c9058037e80f`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/archery competition` | sha256_objeto: `40deaad2cfefd75220dcba6201b25c2a8c55281336a1d4eb8491279fe121cca7`
- texto original (611 chars):

```
In a forest clearing, an unexpected challenge has been set by an even more unexpected challenger. <green><b><incr>Gobin Hood</incr></b></green>, a goblin of monstrous strength, challenges your intrepid band of adventurers to an unconventional test of archery.

"Not the usual sissy elf game," <green><b><incr>Gobin Hood</incr></b></green> growls, hefting his crude bow made from gnarled ironwood. "We ain't aiming for some painted dot. We're smashing through the target!"

The target mentioned is no simple slab of wood, but a formidable barricade, several planks thick, far more robust than any normal target.

```
- opções (2):
  - 1) `Accept` — descrição: (vazia); rolagem.bonus=[{"valor": 0, "nome": "Might"}, {"valor": 1, "nome": "Dexterity"}]; misteriosa=False; ações: Success lim 12, Failure lim 0
  - 2) `Leave` — descrição: `You have no time for the goblin's games.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MANTER**

Justificativa:
- Texto de 611 chars com falas e tags de realce; duas opções (Accept/Leave) e $.condicoes.LeadsToFortune=1.
- Accept tem $.opcoes[0].rolagem.bonus=[{0,Might},{1,Dexterity}]; Success limite 12 concede ouro (razao 6.0) e status 'Point Blank' (2545463); Failure limite 0 concede ouro (razao 3.0) e status Fatigued(2545495)/Weakened(2545504).
- 'Gobin Hood' é jogo de palavras intencional (goblin + Robin Hood), não erro de digitação.

Propostas exatas: nenhuma (MANTER).

---

### 6 — Armor Chest — resources.assets:2545536

- id: `70c65d79-70fd-4541-b3cb-083f7055c346`
- categoria: Normal | raridade: Uncommon (1) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[3], historia=Both
- asset: `events/armor chest - roguelike` | sha256_objeto: `fe77e3403acf7504728659bc8c5952f39c56057d6d675154a0f7ce3e130e09d4`
- texto original (0 chars):

```
(string vazia "")
```
- opções (1):
  - 1) `Open` — descrição: (vazia); rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.texto='' (0 chars) e a única ação (Success limite 0) também tem texto vazio.
- allowedNodeTypes=[3] (NodeType 3=Treasure), raridade Uncommon(1), $.opcoes[0].efeitos[0].efeitos[0].recompensas.itens: dar=true, quantidade_configurada=2, possibleRarities=[2,3] (ItemQuality 2=Rare,3=Legendary).
- #6 e #7 NÃO são cópias totais: #6 concede 2 itens e vem de 'events/armor chest - roguelike'; #7 concede 1 item e vem de 'events/armor chest'.

Propostas exatas (1):

- **6.1** [CAMPO] `$.texto`
    antes: (string vazia "")
    depois: `An iron-banded armor chest waits beside the path, its hinges dark with age.`
  alvo/condição: conforme justificativa do registro; nota: Cena ancorada no nó de tesouro e na raridade Uncommon do próprio asset.

---

### 7 — Armor Chest — resources.assets:2545537

- id: `c6676bef-432e-4eb5-bed7-46664d0b4811`
- categoria: Normal | raridade: Uncommon (1) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[3], historia=Both
- asset: `events/armor chest` | sha256_objeto: `f505ec92a657fcd5fb398b94e6fbe6a1f4ba7c80170c16cc7eaa1b8afbd63ad1`
- texto original (0 chars):

```
(string vazia "")
```
- opções (1):
  - 1) `Open` — descrição: (vazia); rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.texto='' (0 chars); ação única Success limite 0 com texto vazio.
- Distingue-se de #6 por direito: $.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.quantidade_configurada=1 (contra 2 em #6) e caminho de asset próprio ('events/armor chest').
- Mesmo título não implica duplicata — chaves (2545536 / 2545537), ids e caminhos de recurso são distintos.

Propostas exatas (1):

- **7.1** [CAMPO] `$.texto`
    antes: (string vazia "")
    depois:
```
A weathered armor chest lies half-buried by the roadside, a single piece of gear rattling inside.
```
  alvo/condição: conforme justificativa do registro; nota: O 'single piece' espelha quantidade_configurada=1, diferenciando a cena da de #6.

---

### 8 — Barbarian Fisherman — resources.assets:2545538

- id: `c1938011-6b33-47ba-888d-cbfebce87b1c`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=1, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/barbarian fisherman` | sha256_objeto: `7009faa486981a2d0604e0d4aacc91a2d8a9a941b9bc4a63bf30c30339ead955`
- texto original (54 chars):

```
The yearning ghost extends her hand pleading for help.
```
- opções (2):
  - 1) `Reach` — descrição: `You reach out to the ghost. Gain [o1a1_status].`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 2) `Leave` — descrição: `The chill in the air causes you to hesitate. You leave without helping.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.texto é literalmente o mesmo de #1 e #14, mas o título é 'Barbarian Fisherman'.
- As duas opções e seus textos de ação também são os do encontro do fantasma (opção 1 concede status Ethereal, 2545439).
- $.condicoes.disabled=1: registrado como estado; NÃO propomos reativar o slot.

Propostas exatas (3):

- **8.1** [CAMPO] `$.texto`
    antes: `The yearning ghost extends her hand pleading for help.`
    depois:
```
A broad-shouldered barbarian kneels at the riverbank, hauling in a catch with both hands and a grin full of broken teeth.
```
  alvo/condição: conforme justificativa do registro; nota: Alinha a cena ao título real do asset.

- **8.2** [CAMPO] `$.opcoes[0].texto`
    antes: `You reach out to the ghost. Gain [o1a1_status].`
    depois: `Lend the barbarian a hand with the line.`
  alvo/condição: conforme justificativa do registro; nota: Mantém a opção 1 como a que concede o status Ethereal do asset.

- **8.3** [CAMPO] `$.opcoes[1].texto`
    antes: `The chill in the air causes you to hesitate. You leave without helping.`
    depois: `Leave the fisherman to his catch.`
  alvo/condição: conforme justificativa do registro; nota: Os textos de ação $.opcoes[0].efeitos[0].texto e $.opcoes[1].efeitos[0].texto ainda citam fantasma/frio e exigem a mesma passagem de autoria (prosa longa não é inventada aqui).

---

### 9 — Battle — resources.assets:2545539

- id: `5b740c2b-3480-48f2-997b-88c8291db0c0`
- categoria: Normal | raridade: Common (0) | peso: 5.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[0], historia=Both
- asset: `events/battle` | sha256_objeto: `41f4d3ec3e1e4f111840587f196c8c700b71134771794a8b5fd48237ba074c9c`
- texto original (0 chars):

```
(string vazia "")
```
- opções (1):
  - 1) `Fight!` — descrição: (vazia); rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.texto='' (0 chars); $.opcoes[0].titulo='Fight!', $.opcoes[0].texto='' e o texto da ação Success também é vazio.
- batalha.iniciar=true sem ForcedEnemies e sem referencia (PPtr m_PathID=0) — o encontro é resolvido no runtime.
- $.condicoes.KeepInDeckWhenUsed=1 e peso=5.0; allowedNodeTypes=[0] (NormalFight).
- Alegação da parte01 de que dados_recompensa_final NULL significaria 'sistema de recompensas não configurado' é REFUTADA: o motivo do campo é explícito (runtime não exercitado).
- Achado novo: #9 e #10 compartilham o MESMO id 5b740c2b-3480-48f2-997b-88c8291db0c0, embora tenham chaves distintas.

Propostas exatas (1):

- **9.1** [CAMPO] `$.texto`
    antes: (string vazia "")
    depois: `Somewhere beyond the ridge, steel rings against steel — the fight is already waiting.`
  alvo/condição: conforme justificativa do registro; nota: Ancorado em batalha.iniciar=true e no nó NormalFight do asset.

---

### 10 — Battletest Event — resources.assets:2545540

- id: `5b740c2b-3480-48f2-997b-88c8291db0c0`
- categoria: Normal | raridade: Common (0) | peso: 5.0
- estados: disabled=1, EditorOnly=1, minLevel=1, allowedNodeTypes=[0], historia=Both
- asset: `events/battletest event` | sha256_objeto: `4b8aaa7c2c2a8a0afa12a9336a0c61d79570827fd6efda46995cb341f80f769a`
- texto original (0 chars):

```
(string vazia "")
```
- opções (1):
  - 1) `Fight!` — descrição: (vazia); rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.condicoes.disabled=1 E $.condicoes.EditorOnly=1 (único da faixa com EditorOnly=1); $.texto='' e textos de ação vazios.
- ForcedEnemies configurado: The Dead One (2545072); peso=5.0; KeepInDeckWhenUsed=1.
- NÃO propomos alterar $.condicoes.disabled nem excluir o slot: desativar/remover é decisão do autor, não decorrência de estar disabled.

Propostas exatas (1):

- **10.1** [CAMPO] `$.texto`
    antes: (string vazia "")
    depois: `The air here holds its breath — something has been waiting a long time to test you.`
  alvo/condição: conforme justificativa do registro; nota: PROPOSTA CONDICIONAL: só se aplica caso o autor decida manter o slot ativo; nenhuma mudança de disabled é proposta.

---

### 11 — Bear Trap — resources.assets:2545541

- id: `7f5372ca-ad4a-461d-bf2d-086103b7c5d2`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/bear trap` | sha256_objeto: `a284ca7c6cdac831f6142ebe68e08c69bbb7d47b8f565ebc8e5d37f66a4fbdcc`
- texto original (354 chars):

```
An unexpected impediment blocks your path ahead. A <red><b><incr>Bewitched Bear Trap</incr></b></red>, snaps its iron jaws open and shut with an insatiable hunger. A cruel and cunning device crafted with malicious intent. This is more than a mere mechanical contraption. Sinister magic is at play.

Someone will have to disarm it to ensure safe passage.

```
- texto_resultados_possiveis: `Who will attempt to disarm the trap?`
- opções (1):
  - 1) `Overpower` — descrição: `Attempt to overpower its rusted jaws.`; rolagem.bonus=[{"valor": 0, "nome": "Might"}]; misteriosa=False; ações: Success lim 10, Failure lim 1

**VEREDITO: MANTER**

Justificativa:
- Texto de 354 chars, $.texto_resultados_possiveis='Who will attempt to disarm the trap?' e opção única 'Overpower' com $.opcoes[0].rolagem.bonus=[{0,Might}].
- Success limite 10 concede experiência (dar=true, alvo Party); Failure limite 1 aplica -20 percentMaxHealth e status Crippled (2545492).
- Nenhum campo inconsistente; nenhuma anomalia constatada.

Propostas exatas: nenhuma (MANTER).

---

### 12 — Below Zero — resources.assets:2545542

- id: `75bdb92c-6950-454d-9419-0ada4e886f77`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/below zero` | sha256_objeto: `5e2dca15635c775c4e677f53754eea601d67bacfb970e036b17465af1cff8c0a`
- texto original (345 chars):

```
A bizarre fungal growth blocks your path ahead, its blue luminescence radiating an unnerving cold that freezes the very air around it. You recognize it as a Frostcap, an ancient form of magical fungi. It saps the warmth from its surroundings to survive. Delicate snowflakes, out of place in this environment, dance and whirl about its icy aura. 
```
- opções (1):
  - 1) `Escape` — descrição: `Struggle to leave the area before you are frozen solid.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 12, Failure lim 1

**VEREDITO: MANTER**

Justificativa:
- Texto de 345 chars; opção única 'Escape' com descrição própria.
- Success limite 12 concede experiência (dar=true, razao 0.5); Failure limite 1 aplica -20 percentMaxHealth e status Frostbitten (2545496).
- Nenhuma anomalia constatada.

Propostas exatas: nenhuma (MANTER).

---

### 13 — Between Worlds — resources.assets:2545543

- id: `e4acbfa7-bf37-42fb-aa13-e039e4339487`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/between worlds` | sha256_objeto: `473f3d0f1e65f8853c4478c463dc56410c3461cb65c1e5e20c915e0a5199a4e5`
- texto original (142 chars):

```
A spectral maiden extends her hand towards you, her hollow eyes filled with a silent yearning, a call for help that whisperes across the ages.
```
- opções (2):
  - 1) `Reach` — descrição: `You reach out to the ghost.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 2) `Leave` — descrição: `Turn away from the spirit.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- Literal real do original: 'whisperes' — achado válido preservado da parte01.
- Alegação da parte01 de que $.opcoes[*].rolagem.bonus vazio indicaria 'mecânica de sorte não implementada' é REFUTADA: bônus de rolagem vazio é o padrão da faixa (26 de 32 slots) e as ações são Success com limite_rolagem 0; nada indica rolagem quebrada.
- Opção 1 concede status Ethereal (2545439) e LeadsToFortune=1.

Propostas exatas (1):

- **13.1** [TRECHO] `$.texto`
    antes: `whisperes`
    depois: `whispers`
  alvo/condição: conforme justificativa do registro; nota: antes→depois do TEXTO ORIGINAL; nenhum arquivo do jogo/EV-R1 é editado.

---

### 14 — Blood of the Abyss — resources.assets:2545544

- id: `70d9f977-f25b-4f47-ac09-30f12be404f2`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=1, EditorOnly=0, minLevel=1, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/blood of the abyss` | sha256_objeto: `7c883f146329e80b295ca60cf3036ca03c4ff0181fb03e27c3cfbfedec734481`
- texto original (54 chars):

```
The yearning ghost extends her hand pleading for help.
```
- opções (2):
  - 1) `Reach` — descrição: `You reach out to the ghost. Gain [o1a1_status].`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 2) `Leave` — descrição: `The chill in the air causes you to hesitate. You leave without helping.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.texto é o mesmo de #1/#8, mas o título é 'Blood of the Abyss'.
- Opção 1 concede status Ethereal (2545439); LeadsToFortune=1; $.condicoes.disabled=1 registrado como estado, sem proposta de reativação.

Propostas exatas (3):

- **14.1** [CAMPO] `$.texto`
    antes: `The yearning ghost extends her hand pleading for help.`
    depois:
```
A crimson glow pulses from a fissure in the rock, and the air turns thick with the smell of old blood.
```
  alvo/condição: conforme justificativa do registro; nota: Alinha a cena ao título real do asset.

- **14.2** [CAMPO] `$.opcoes[0].texto`
    antes: `You reach out to the ghost. Gain [o1a1_status].`
    depois: `Reach toward the pulsing light.`
  alvo/condição: conforme justificativa do registro; nota: Mantém a opção 1 como a que concede o status Ethereal.

- **14.3** [CAMPO] `$.opcoes[1].texto`
    antes: `The chill in the air causes you to hesitate. You leave without helping.`
    depois: `Turn away from the fissure.`
  alvo/condição: conforme justificativa do registro; nota: Textos de ação ainda citam fantasma/frio e exigem a mesma passagem de autoria.

---

### 15 — Bonefire — resources.assets:2545546

- id: `ae42559a-dc07-4d70-b089-64b9aa50f829`
- categoria: Normal | raridade: Rare (2) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=3, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/bonefire - (roguelike)` | sha256_objeto: `ffe3892f6d9fdc3bddf7bc14a7065e90e6f9c4486f08297988c5f701b98226b1`
- texto original (328 chars):

```
A ghastly pyre dances with unnatural, green flames. It is a bonfire, fueled by an ominous collection of human bones that emits an eerie glow. As you watch the flickering flames, a wave of unnatural weariness descends upon you. The fire seems to burn not just with bones, but with the very life-force of those who gaze upon it...
```
- opções (2):
  - 1) `Rest` — descrição: `This spot looks as good as any to rest.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 2) `Leave` — descrição: `You won't risk resting under the Bonefire's ominous glow.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MANTER**

Justificativa:
- Texto de 328 chars; duas opções (Rest/Leave) com descrições próprias.
- Rest (Success limite 0) inicia batalha com referencia real 'Cursed Chest Battle' (resources.assets:2544645) e concede experiência (razao 2.0); Leave aplica Fatigued(2545495)/Enfeebled(2545494).
- Rare(2), minLevel=3, caminho 'events/bonefire - (roguelike)' — asset distinto de #16 (chave 2545548, 'events/bonefire'), apesar do texto idêntico.

Propostas exatas: nenhuma (MANTER).

---

### 16 — Bonefire — resources.assets:2545548

- id: `b2cbffb6-4ee2-48f5-9c10-4fc110764f3f`
- categoria: Normal | raridade: Rare (2) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=3, allowedNodeTypes=[7], historia=NonStoryOnly
- asset: `events/bonefire` | sha256_objeto: `f01f791fa9a87783098387dc6ddbbb75753e47dc98bc388a6ad12f4794d1511a`
- texto original (328 chars):

```
A ghastly pyre dances with unnatural, green flames. It is a bonfire, fueled by an ominous collection of human bones that emits an eerie glow. As you watch the flickering flames, a wave of unnatural weariness descends upon you. The fire seems to burn not just with bones, but with the very life-force of those who gaze upon it...
```
- opções (2):
  - 1) `Rest` — descrição: `This spot looks as good as any to rest.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 2) `Leave` — descrição: `You won't risk resting under the Bonefire's ominous glow.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MANTER**

Justificativa:
- Mesmo conteúdo autoral de #15, porém com chave (2545548), id e caminho ('events/bonefire') próprios.
- Rest inicia batalha 'Cursed Chest Battle' (2544645); Leave aplica Fatigued/Enfeebled.
- Título e texto repetidos não constituem registro duplicado: não há chave ou id repetido entre #15 e #16.

Propostas exatas: nenhuma (MANTER).

---

### 17 — Bonfire — resources.assets:2545549

- id: `13fb829a-cc27-44ce-aa4d-f3bfeb53d884`
- categoria: Normal | raridade: Uncommon (1) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[2], historia=NonStoryOnly
- asset: `events/bonfire (roguelike)` | sha256_objeto: `ef5a4f9cf0f5e7361597f9c6b6406c9da8b2d03f33689d3974bc6b298f333582`
- texto original (143 chars):

```
The flames of a Bonfire dance in the air, their warmth spreading like a welcoming embrace. Nothing like a warm fire to rest from your troubles.
```
- opções (3):
  - 1) `Rest` — descrição: `Sit by the fire and recover your strength.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 2) `Reroll Skill` — descrição: `Reroll a skill!`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 3) `Level Up Fortunes` — descrição: `Level up all your owned Fortunes to your current character level.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MANTER**

Justificativa:
- Texto de 143 chars; três opções com descrições próprias.
- Rest (Success limite 0) cura 50 percentMaxHealth e 50 percentMaxMana.
- 'Reroll Skill' NÃO é opção sem efeito: $.opcoes[1].campos_originais.openSkillRerollMenu=1; 'Level Up Fortunes' usa $.opcoes[2].campos_originais.levelUpFortunesToCharacterLevel=1. Ambos são flags reais, não recompensas vazias.
- allowedNodeTypes=[2] (NodeType 2=RestSite).

Propostas exatas: nenhuma (MANTER).

---

### 18 — Bonfire — resources.assets:2545551

- id: `84b23e39-7e88-44f4-b86a-a580193d88d5`
- categoria: Normal | raridade: Uncommon (1) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[2], historia=NonStoryOnly
- asset: `events/bonfire` | sha256_objeto: `60ab00f3731cf7f19ebb29266df4c3d5df203d57a4fa7629e549d30d42938d5a`
- texto original (143 chars):

```
The flames of a Bonfire dance in the air, their warmth spreading like a welcoming embrace. Nothing like a warm fire to rest from your troubles.
```
- opções (2):
  - 1) `Rest` — descrição: `Sit by the fire and recover your strength.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0
  - 2) `Prepare` — descrição: `Take time to prepare for what's ahead.`; rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MANTER**

Justificativa:
- Texto idêntico ao de #17, mas opções diferentes (Rest/Prepare) e caminho próprio ('events/bonfire'; #17 é 'events/bonfire (roguelike)').
- Rest cura 50 percentMaxHealth/50 percentMaxMana; Prepare concede o status 'Prepared' (2545391).
- Nenhuma anomalia constatada.

Propostas exatas: nenhuma (MANTER).

---

### 19 — Bonfire Story — resources.assets:2545550

- id: `f0c60be1-d947-4518-8cc0-8533847a22f3`
- categoria: Normal | raridade: Uncommon (1) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[2], historia=StoryOnly
- asset: `events/bonfire story` | sha256_objeto: `20080df9a376ea12397567b19009b66819d7da18865e6f94532efc9335665ac4`
- texto original (0 chars):

```
(string vazia "")
```
- opções (1):
  - 1) `Rest` — descrição: (vazia); rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.texto='' (0 chars) e $.opcoes[0].texto='' (vazio); a ação Rest tem texto próprio ('You feel well rested.').
- $.condicoes.historia=StoryOnly (StorySetting) — o asset é declaradamente narrativo e não tem narrativa.
- Rest cura 25 percentMaxHealth/25 percentMaxMana; allowedNodeTypes=[2] (RestSite).

Propostas exatas (2):

- **19.1** [CAMPO] `$.texto`
    antes: (string vazia "")
    depois:
```
You settle beside the low-burning fire, and the tale of this place slowly takes shape in the embers.
```
  alvo/condição: conforme justificativa do registro; nota: Coerente com o StorySetting=StoryOnly e com o nó de descanso.

- **19.2** [CAMPO] `$.opcoes[0].texto`
    antes: (string vazia "")
    depois: `Sit by the fire and listen.`
  alvo/condição: conforme justificativa do registro; nota: Descrição da única opção, hoje vazia.

---

### 20 — Boss — resources.assets:2545553

- id: `6c1fb16d-e9b4-453a-8bb1-eaaa5892c4e8`
- categoria: Normal | raridade: Common (0) | peso: 1.0
- estados: disabled=0, EditorOnly=0, minLevel=1, allowedNodeTypes=[5], historia=Both
- asset: `events/boss` | sha256_objeto: `7f198a787ae051007aacdeeed7e95090504ac941603aaa58410ba4fb74b62966`
- texto original (0 chars):

```
(string vazia "")
```
- opções (1):
  - 1) `Fight!` — descrição: (vazia); rolagem.bonus=[]; misteriosa=False; ações: Success lim 0

**VEREDITO: MELHORAR**

Justificativa:
- $.texto='' (0 chars); $.opcoes[0].titulo='Fight!', $.opcoes[0].texto='' e texto da ação Success vazio.
- allowedNodeTypes=[5] (NodeType 5=Boss); batalha.iniciar=true sem ForcedEnemies e sem referencia (PPtr m_PathID=0).
- Alegação da parte01 de recompensa inexistente/sistema não configurado é REFUTADA: $.opcoes[0].efeitos[0].batalha.dados_recompensa_final=null traz motivo explícito de runtime não exercitado.

Propostas exatas (1):

- **20.1** [CAMPO] `$.texto`
    antes: (string vazia "")
    depois: `The path ends at a sealed gate, and behind it something vast shifts its weight.`
  alvo/condição: conforme justificativa do registro; nota: Ancorado no nó Boss e no combate já configurado do asset.

---

## 6. Anomalias e contagens reais (recalculadas da fonte)

| Fato | Contagem | Onde (ordinais) |
|---|---|---|
| Eventos na faixa | 20 | 1–20 |
| Categoria Normal do lote inteiro | 160 | — |
| `disabled=1` | 5 | [1, 4, 8, 10, 14] |
| `EditorOnly=1` | 1 | [10] |
| Texto narrativo vazio (`""`) | 6 | [6, 7, 9, 10, 19, 20] |
| Texto idêntico ao do "yearning ghost" | 3 | [1, 8, 14] |
| Títulos repetidos | 3 grupos | Armor Chest×2, Bonefire×2, Bonfire×2 |
| **ids repetidos** (achado novo) | 1 | #9 e #10 compartilham `5b740c2b-3480-48f2-997b-88c8291db0c0` |
| ids únicos / chaves únicas | 19 / 20 | — |
| `$..rolagem.bonus` não vazio | 4 eventos | [2, 3, 5, 11] |
| Slots de opção com bônus vazio | 26 de 32 | — |
| Textos de opção vazios (`$.opcoes[*].texto=""`) | 11 | — |
| `batalha.iniciar=true` | 6 | [4, 9, 10, 15, 16, 20] |
| `batalha.dados_recompensa_final=null` com combate iniciado | 20 | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | — todos com motivo de runtime não exercitado |
| PPtr nulo `chave`/`nome` (m_PathID=0) | 20 de 20 | 1–20 (não é anomalia distintiva) |
| Raridades | Common 13 / Uncommon 5 / Rare 2 | — |
| Pesos | 1.0 ×18 / 5.0 ×2 | 5.0 em #9 e #10 |
| Typos reais no texto original | 2 | #2 `appeares`, #13 `whisperes` |

Contagens da parte01 que **não** se sustentam: `roll_bonus vazio = 13 (todos exceto 5)`, `Campos NULL = 7 eventos`. As contagens acima vêm de recálculo direto sobre `eventos.json`.

## 7. Auditoria automática (comando e saída real)

Comando executado no workspace do cartão (offline, sem jogo):

```
python EV-R2-NORMAL-b01-parte02-propostas.py   # gera a validação estruturada
python EV-R2-NORMAL-b01-parte02-validar.py --md | tee EV-R2-NORMAL-b01-parte02-auditoria.txt
python EV-R2-NORMAL-b01-parte02-render.py      # renderiza este documento
python EV-R2-NORMAL-b01-parte02-validar.py --md # confere md <-> validação (executado por último)
```

Saída real:

```
== 1. Integridade das fontes ==
PASS sha256 eventos.json :: 4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13
PASS sha256 lote-Normal-v2.md :: 83b30ada3d78e596b8c7c0784d5e741b43654b14ab02d5377d8a1b245b84f146
PASS sha256 eventos.schema.json :: 6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc
PASS sha256 catalogo-referencias.json :: 94077cc887621933abe7bbbbd96e91c5a887478dba8fd000b8f4a4129c3745a5
PASS parte01 (proposta reprovada) inalterada :: e65daa3413e18adc1d73b6272d936f8d7d593da83e90abfbb06c34f6aee530e9
PASS parte02 não sobrescreve parte01
== 2. Cobertura e identidade (20/20, ordem do JSON categoria Normal) ==
PASS 20 registros :: 20
PASS ordinais 1..20 únicos
PASS chave/id/título/categoria/raridade/peso conferem com a fonte :: []
PASS ordem posicional = ordem do JSON Normal (1..20)
== 3. Caminhos JSONPath e literais antes->depois ==
PASS todos os JSONPath resolvem na fonte :: []
PASS todos os literais 'antes' batem na fonte e depois difere :: []
PASS 20 registros com veredito e justificativa
PASS MELHORAR tem natureza e >=1 proposta exata
PASS MANTER não propõe alteração
== 4. Vereditos e contagens ==
PASS MANTER = 7 (#5,11,12,15,16,17,18) :: [5, 11, 12, 15, 16, 17, 18]
PASS MELHORAR = 13 (restantes) :: [1, 2, 3, 4, 6, 7, 8, 9, 10, 13, 14, 19, 20]
PASS fonte: 160 eventos categoria Normal, faixa = primeiros 20
PASS fonte: disabled = [1, 4, 8, 10, 14]
PASS fonte: texto vazio = [6, 7, 9, 10, 19, 20]
PASS fonte: texto do fantasma repetido = [1, 8, 14]
PASS fonte: bônus de rolagem não vazio = [2, 3, 5, 11] (slots vazios 26/32)
PASS fonte: batalha.iniciar=true = [4, 9, 10, 15, 16, 20]
PASS fonte: ids duplicados = {'5b740c2b-3480-48f2-997b-88c8291db0c0': 2} (únicos 19, chaves 20)
PASS fonte: typos originais = {2: ['appeares'], 13: ['whisperes']}
PASS fonte: PPtr nulo presente em 20/20 (não é anomalia distintiva)
PASS validação JSON coerente com os fatos
== 5. Coerência md <-> validação JSON ==
PASS md existe e tem 20 seções '### <ordinal> —' :: 20
PASS md cita todas as propostas (código + JSONPath) :: []
PASS md declara MANTER=7 / MELHORAR=13
PASS md registra supersessão nominal
PASS md marca runtime NAO_EXERCITADO
== RESULTADO ==
PASS 32 / FAIL 0 / exit 0
```

## 8. Limites deste parecer

- Runtime NAO_EXERCITADO: nada foi aberto no jogo; toda conclusão sobre exibição, resolução de tokens/placeholders, inimigos efetivos, loot/XP/ouro ou efeito final é explicitamente não exercitada.
- As propostas de texto em inglês são sugestões autorais para o dono decidir; os textos originais (asset/EV-R1) não são editados aqui.
- Eventos com `disabled=1` (#1, #4, #8, #10, #14) recebem propostas de texto/wording condicionais; nenhuma mudança de flag, nenhuma reativação e nenhuma exclusão é proposta.
- Este documento corrige a proposta documental; não implementa balanceamento, não publica e não faz push.
