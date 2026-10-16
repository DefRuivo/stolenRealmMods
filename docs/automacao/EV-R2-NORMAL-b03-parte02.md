# EV-R2-NORMAL-b03 — parte 02 (CORREÇÃO): eventos 41–60 (categoria Normal)

Status: PROPOSTAS PARA APROVAÇÃO DO DONO; nenhuma decisão aprovada e nenhuma implementação.

**Esta parte supersede, nominalmente, as seções 41–60 de `EV-R2-NORMAL-b03-parte01.md`** (chave de arquivo: `80f14e416c0e05302c4fed7ed2c51793cd975426013647e09887dfbb8cd813b5`), que estão reprovadas pela revisão independente `t_4c07d669`. O arquivo parte01 não foi alterado; o inventário `ev-r2-normal-b03-inventario.md` e as fontes EV-R1 também não.

Faixa exata: ordinais **41 a 60** na ordem de categoria Normal. 20 eventos, 20 ordinais únicos.

**Revisão 2 (pós-review, cartão `t_99925533`):** corrigida a justificativa de **§49 Foreboding Gem**, que afirmava `VictoryEvent nulo`. O `VictoryEvent` real é `resources.assets:2545594` «Foreboding Gem - Victory»; o que é nulo em #49 é a **referência de batalha** (`batalha.referencia.chave = null`, com o BattleInfo do próprio evento, `BattlePointValue` 16) e o `FailureEvent`. Veredito (MANTER), propostas e contagens desta parte não mudam. Auditoria (`EV-R2-NORMAL-b03-validar.py`) ganhou os checks de `VictoryEvent`/`FailureEvent`/referência de batalha por evento — o campo que havia escapado da rodada 1.

**Revisão 3 (pós-review, cartão `t_99925533`):** corrigido o §6 «Auditoria offline — comando e saída REAL», que ainda reproduzia a saída da rodada 1 (23 checks / `TOTAL 23 PASS 23 FAIL 0`) e portanto não correspondia ao script atual: o bloco foi regerado a partir da execução de agora (**28 checks**, `TOTAL 28 PASS 28 FAIL 0`), o quadro do §1 passou a «28 PASS / 0 FAIL» e a lista «O que a auditoria confere» ganhou os 5 checks ausentes (`MD_JUSTIFICATIVAS_20_EQ_JSON`, `BATALHA_VICTORY_FAILURE_INVENTARIO_20`, `EV49_BATALHA_VICTORY_EVENT_2545594`, `CATALOGO_2545594_FOREBODING_GEM_VICTORY`, `MD49_VICTORYEVENT_CORRIGIDO`). Nada além do §6/§1 mudou: vereditos (13 MANTER / 7 MELHORAR), propostas (16), identidades, GUIDs/SHA e o §49 continuam como na Revisão 2.

Fonte da ordem: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-Normal-v2.md` (160 seções) confrontada, seção a seção, com a ordem de `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json` (160 eventos da categoria Normal): **MD x JSON idênticos, 160/160**. Semântica: `eventos.schema.json` e `schema.md`. Referências: `catalogo-referencias.json`. Fontes somente leitura.

Ordem por ordinal Normal do JSON — **não** por ordem crescente de `path_id` e **não** por título (títulos repetidos existem em outras faixas).

## 0. Como ler este documento

- **Índices em BASE 1** em todos os JSONPath deste documento: `$.opcoes[1]` é a primeira opção, `$.opcoes[1].efeitos[1]` é a primeira ação dela (no JSON os arrays são base 0).
- **TRECHO vs CAMPO**: onde a proposta cita um TRECHO, somente esse trecho muda e todos os demais bytes do campo — inclusive espaços, LF, tags `<red>` e placeholders `[name]`/`[his]` — permanecem. Onde cita CAMPO, a proposta é o valor completo daquele campo.
- **Notação de escapes**: no texto deste documento, `\r` significa o caractere CR (U+000D) e `\n` significa LF (U+000A). O campo real contém os bytes; a notação existe para tornar CR e LF visíveis na leitura.
- **Natureza das propostas**: nesta faixa há **apenas** correção de dado da proposta (retratações) e **sugestões de alteração do texto original** (preenchimento de campo vazio, erro literal/gramatical, normalização de bytes CR). `$.texto` e `activationText` originais estão em inglês; os textos propostos estão em inglês, mesma língua do campo, e **não** são tradução PT-BR — nenhuma tradução é proposta aqui.
- **NULL e NAO_EXERCITADO**: `quantidade_final`, `dados_recompensa_final` e `resultado_sorteado` são NULL por dependerem de estado de partida (nível, razão de ouro/XP, RNG) **não exercitado**. Referência NULL de PPtr é outra coisa: é `m_PathID=0` configurado, não recompensa zero. Nada neste documento foi observado no jogo: **runtime NAO_EXERCITADO**.
- **Veredito**: MANTER = nenhuma alteração proposta para o evento (pode trazer SINALIZAÇÃO informativa). MELHORAR = há alteração concreta proposta e especificada. Sem alteração de balanceamento.

## 1. Retratação nominal das acusações (o que a proposta anterior afirmou e o que a fonte diz)

### A1. Títulos inventados #47–#51 e chave ausente

- **Afirmado por parte01:** parte01 nomeia #47 Eternal Flame, #48 Eternal Guard, #49 Eternal Pool, #50 Exploding Skeleton e #51 Extinguished Altar. Nenhum desses títulos existe nos 256 registros do JSON, e a chave resources.assets:2545597 não é citada em lugar nenhum do documento.
- **Fato na fonte (verificado):** Os títulos reais são #47 Etched Rune (resources.assets:2545592), #48 Fickle Fungus (:2545593), #49 Foreboding Gem (:2545595), #50 Fountain of Life (:2545596) e #51 Friend or Foe (:2545597).
- **Efeito nesta parte:** RETRATADO INTEGRALMENTE: as seções 47–51 de parte01 não correspondem a nenhum evento da faixa. Esta parte cobre os cinco eventos reais, incluindo a chave :2545597 que faltava.

### A2. GUID duplicado #46–#51 e literais de proveniência

- **Afirmado por parte01:** parte01 declara «CRÍTICO: Eventos 46–51 compartilham GUID duplicado 81c8fe59-5e3b-4e5e-b196-ec9bfcf44649» e recomenda corrigir os ids 46–51. Cita ainda, como proveniência, o GUID de #41 e os SHA de #54, #55, #56, #57 e #58 — nenhum deles existe na fonte.
- **Fato na fonte (verificado):** Nenhum dos 256 registros tem o id acusado. Os seis ids reais de #46–#51 são todos distintos: 46 81c8fe59-5e3b-4e96-8148-0e89d7ce48f7; 47 c8e5ace5-c340-450b-9d33-c0f525acb410; 48 9c731a7c-bbce-4c95-a4aa-fd9700ec70f0; 49 e4dc06e1-2425-4578-9cd7-087d78eb0d18; 50 b6728bfa-321a-4c53-98c6-9b3d4d8f1ca1; 51 a5c05b2d-a0d7-4e95-afc6-66beff7d1a6f. O único GUID duplicado real dos 256 registros é 5b740c2b-3480-48f2-997b-88c8291db0c0 em resources.assets:2545539 e :2545540 (#9 Battle e #10 Battletest Event), fora da faixa 41–60.
- **Efeito nesta parte:** RETRATADO INTEGRALMENTE: a recomendação de corrigir os ids 46–51 fica retirada; não há defeito a corrigir nesses seis eventos. A duplicação real (#9/#10) é registrada como sinalização fora do escopo desta faixa, para cartão próprio.

### A3. Campos de texto vazios

- **Afirmado por parte01:** parte01 fala em 2 vazios (#43 e #56), trata ambos como string estrita vazia e não cita #47.
- **Fato na fonte (verificado):** Vazios narrativos reais da faixa: #43 Enchanted Symbol com $.texto = '\n' (1 caractere, U+000A), #47 Etched Rune com $.texto = '\n' (1 caractere) e #56 Hard Battle com $.texto = '' (0 caracteres). São TRÊS eventos: #43 e #47 são whitespace, não string estrita vazia; #56 é string estrita vazia. Também estão vazios os activationText dos três (0 caracteres).
- **Efeito nesta parte:** CORRIGIDO: a contagem passa a 3 vazios (43, 47, 56), com a distinção whitespace vs string vazia explicitada e #47 presente.

### A4. Raridade Mythic de #54 e #58

- **Afirmado por parte01:** parte01 trata a raridade Mythic como «ANOMALIA DE RARIDADE» e propõe «baixar para Common» ou «mover para lote Mythic».
- **Fato na fonte (verificado):** #54 Gold Statue of the First Mountain King e #58 Hell Coffer têm raridade {valor:4,nome:Mythic} VERDADEIRA, categoria=Normal, peso=1.0 e pool=[{valor:0,nome:Normal}]. Não existe pool «Common»: Common é raridade, não pool. Distribuição real da faixa: 17 Common, 1 Rare (#50) e 2 Mythic (#54, #58).
- **Efeito nesta parte:** RETRATADO INTEGRALMENTE: retiradas a acusação de inconsistência e qualquer proposta de downgrade ou de movimentação de lote. Raridade e pool são campos independentes e ambos estão coerentes na fonte.

### A5. Enchanted Obelisk (#41) «sem cura»

- **Afirmado por parte01:** parte01 afirma «vida_mana tem todos os valores 0.0 — nenhuma cura ou mana é aplicada em runtime» e propõe percentCurHealth = 0.25 e percentMaxMana = 0.15.
- **Fato na fonte (verificado):** A opção 2, «Heal from the obelisk», já tem opcoes[2].efeitos[1].efeitos[1].vida_mana = {percentMaxHealth:50.0, percentMaxMana:50.0, percentCurHealth:0.0, percentCurMana:0.0}: 50% de vida e de mana MÁXIMAS estão configurados. A opção 1 grava o status Brilliance (resources.assets:2545415, «@Intelligence@ increased by {4,20}», duração Quest, tipo Fortune).
- **Efeito nesta parte:** RETRATADO INTEGRALMENTE: não existe cura zero demonstrada em #41 e a proposta 0.25/0.15 é retirada — além de sem base, 0.25/0.15 seriam frações, enquanto os campos do jogo são percentuais (a fonte grava 50.0).

### A6. Opções inventadas em #53, #59 e #60

- **Afirmado por parte01:** parte01 descreve #53 com as opções «Attack» e «Sneak past»; #59 com «Enter» e «Close»; #60 com «Disable — Brave the flames to disable the trap».
- **Fato na fonte (verificado):** #53 Goblin Scout Tower tem UMA opção, «Strike silently» (rolagem Dexterity +1): Success com limite_rolagem 12 e sem batalha, e Failure com limite_rolagem 1 iniciando batalha com 1 inimigo forçado. #59 Hell Gate tem «Wait» e «Leave». #60 Hold your Breath tem UMA opção, «Claim» (Vitality +2, Success com limite 14, Failure com limite 0 e -35 percentMaxHealth em Self).
- **Efeito nesta parte:** RETRATADO INTEGRALMENTE: as propostas de melhorar, renomear ou subtitular opções inexistentes são retiradas; nenhuma opção é criada, removida ou renomeada.

### A7. Contagens do corpo, ordinal de #60 e português

- **Afirmado por parte01:** parte01 fecha com «MANTER 14» e «MELHORAR 6» listando 13 e 7 nomes, numera Hold your Breath como 56 no quadro de visão geral (duplicando Hard Battle), usa «oubuff» (L343), «interrupto» (L366) e «goblnica» (L393) e contém 28 escapes de aspas desnecessários.
- **Fato na fonte (verificado):** As 20 seções de parte01 contêm, de fato, 13 MANTER e 7 MELHORAR; Hold your Breath é o ordinal 60 (resources.assets:2545609); as palavras corretas são «ou buff», «interruptor» e «goblínica».
- **Efeito nesta parte:** CORRIGIDO: esta parte usa o ordinal 60 para Hold your Breath, fecha em 13 MANTER / 7 MELHORAR e não usa escapes de aspas nem os erros de digitação citados.

Sétima retratação (A7) fecha também as correções de forma exigidas: contagens do corpo, ordinal de Hold your Breath, português e escapes.

## 2. Inventário real — 20 eventos (41–60)

| # | Chave | Id (GUID) | Título | Categoria | Raridade (valor) | Peso | disabled | Pool | Opts | Veredito | Natureza |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 41 | `resources.assets:2545585` | `36c51484-b50b-4627-a9a7-64d221a22f1a` | Enchanted Obelisk | Normal | Common (0) | 1.0 | 0 | Normal | 2 | **MANTER** | — |
| 42 | `resources.assets:2545587` | `3bda807e-075d-45e3-afe7-b9d0f9d4b34c` | Enchanted Pumpkin Patch | Normal | Common (0) | 1.0 | 0 | Normal | 2 | **MANTER** | — |
| 43 | `resources.assets:2545588` | `51200c46-6ca9-4e5e-b68d-ee6424dee157` | Enchanted Symbol | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MELHORAR** | SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (vazio) - inglês (EN) |
| 44 | `resources.assets:2545589` | `ad2b9f6c-46c8-4e66-ae0d-8825c3948d41` | Entangled Boar | Normal | Common (0) | 1.0 | 0 | Normal | 2 | **MANTER** | — |
| 45 | `resources.assets:2545590` | `db1ccfd4-c6d4-4dc1-9f7f-8966d93ceb32` | Eruption! | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MANTER** | — |
| 46 | `resources.assets:2545591` | `81c8fe59-5e3b-4e96-8148-0e89d7ce48f7` | Etched Monolith | Normal | Common (0) | 1.0 | 0 | Normal | 2 | **MANTER** | — |
| 47 | `resources.assets:2545592` | `c8e5ace5-c340-450b-9d33-c0f525acb410` | Etched Rune | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MELHORAR** | SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (vazio) - inglês (EN) |
| 48 | `resources.assets:2545593` | `9c731a7c-bbce-4c95-a4aa-fd9700ec70f0` | Fickle Fungus | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MANTER** | — |
| 49 | `resources.assets:2545595` | `e4dc06e1-2425-4578-9cd7-087d78eb0d18` | Foreboding Gem | Normal | Common (0) | 1.0 | 0 | Normal | 2 | **MANTER** | — |
| 50 | `resources.assets:2545596` | `b6728bfa-321a-4c53-98c6-9b3d4d8f1ca1` | Fountain of Life | Normal | Rare (2) | 1.0 | 0 | Normal | 1 | **MANTER** | — |
| 51 | `resources.assets:2545597` | `a5c05b2d-a0d7-4e95-afc6-66beff7d1a6f` | Friend or Foe | Normal | Common (0) | 1.0 | 1 | Normal | 2 | **MANTER** | — |
| 52 | `resources.assets:2545598` | `37dc56cd-600f-46b8-b0cc-eae8e0e9f0c7` | Furnace Trap | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MANTER** | — |
| 53 | `resources.assets:2545599` | `a443b122-b3e5-4f42-b4b0-bd74a648d40d` | Goblin Scout Tower | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MANTER** | — |
| 54 | `resources.assets:2545601` | `a93098ef-da50-40e2-a216-4b0f4e258fda` | Gold Statue of the First Mountain King | Normal | Mythic (4) | 1.0 | 0 | Normal | 2 | **MELHORAR** | SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (normalização de bytes CR) - inglês (EN) |
| 55 | `resources.assets:2545602` | `22d9580c-8a7f-45c3-88cc-bb27e307203c` | Grinder Trap | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MANTER** | — |
| 56 | `resources.assets:2545603` | `e77a13db-782d-4e5a-b196-ec9bfcf44649` | Hard Battle | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MELHORAR** | SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (vazio) - inglês (EN) |
| 57 | `resources.assets:2545604` | `9b45cc6c-33cb-4936-acc7-76140acef17f` | Heavy Safe | Normal | Common (0) | 1.0 | 0 | Normal | 2 | **MANTER** | — |
| 58 | `resources.assets:2545606` | `f41a780b-f4aa-455c-b26f-895129f63261` | Hell Coffer | Normal | Mythic (4) | 1.0 | 0 | Normal | 2 | **MELHORAR** | SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (erro literal) - inglês (EN) |
| 59 | `resources.assets:2545608` | `afb86d83-6268-409d-a05d-14709b6713f6` | Hell Gate | Normal | Common (0) | 1.0 | 0 | Normal | 2 | **MELHORAR** | SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (gramática e bytes CR) - inglês (EN) |
| 60 | `resources.assets:2545609` | `12d253b1-8643-427b-8f35-8b1f402b1c07` | Hold your Breath | Normal | Common (0) | 1.0 | 0 | Normal | 1 | **MELHORAR** | SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (normalização de bytes CR) - inglês (EN) |

`sha256_objeto` de cada evento está conferido contra a fonte (20/20) e aparece na seção de cada evento.

## 3. Contagens e inventário de decisões

| Item | Valor |
|---|---|
| Eventos na faixa | 20 (ordinais únicos 41–60) |
| Veredito MANTER | 13 — 41, 42, 44, 45, 46, 48, 49, 50, 51, 52, 53, 55, 57 |
| Veredito MELHORAR | 7 — 43, 47, 54, 56, 58, 59, 60 |
| Propostas com `antes` literal conferido na fonte | 16 |
| Raridades | Common 17, Rare 1 (#50), Mythic 2 (#54, #58) |
| Eventos desativados (`disabled=1`) | 1 (#51) |
| Opções na faixa | 30 |
| Ações que iniciam batalha | 9 ações em 8 eventos (42, 49, 51, 53, 54, 56, 58, 59) |
| Textos narrativos vazios | 3 (#43 `\n`, #47 `\n`, #56 `''`) |
| Fontes validadas intactas na auditoria desta parte | 11/11 |
| Checks da auditoria offline | 28 PASS / 0 FAIL |

As contagens acima são as mesmas do corpo: **13 MANTER / 7 MELHORAR** (parte01 fechava em 14/6 listando 13 e 7 — corrigido em A7).

## 4. Vereditos e propostas por evento (41–60)

### 41 — Enchanted Obelisk — `resources.assets:2545585`

- **Id (GUID):** `36c51484-b50b-4627-a9a7-64d221a22f1a`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[2], minLevel=1, isLesserEvent=0, LeadsToFortune=1, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `bb1c733ab8dd48a07f5c6a8f0e67e355eeab059af353513444b732d8f20b4773`
- **`$.texto`:** 423 caracteres. Início: "Rising from the earth like the tooth of some gargantuan beast, an obelisk crafted entirely from limestone, ancient and weathered stands proud and defi"...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Activate the blessing | "Press the palm of your hand upon the obelisk." | bonus=[] | 1 | Success | 0 | não |
| 2 | Heal from the obelisk | "Draw the energy from the limestone obelisk." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. As duas opções são distintas em efeito E em narrativa: «Activate the blessing» grava o status Brilliance (opcoes[1].efeitos[1].efeitos[1].recompensas.status.candidatos[1] = resources.assets:2545415, «@Intelligence@ increased by {4,20}», duração Quest) e «Heal from the obelisk» grava vida_mana {percentMaxHealth:50.0, percentMaxMana:50.0} em Self. Os activationText de sucesso também diferem entre as opções («a pulse of energy courses through» contra «The magic flows into»). Não há cura zero, não há texto idêntico entre as opções e não há defeito de configuração demonstrado. Sem alteração proposta.

**Sinalizações (sem proposta):**

- Chave e GUID reais desta seção diferem dos que parte01 citou: o GUID acusado 36c51484-b50b-4681-9e7f-6006b9c27192 não existe; o real é 36c51484-b50b-4627-a9a7-64d221a22f1a (ver A2 e A5).

**Retratação:** Supersede a seção 41 e as recomendações 1–2 de parte01 (cura inerte e valores 0.25/0.15).

### 42 — Enchanted Pumpkin Patch — `resources.assets:2545587`

- **Id (GUID):** `3bda807e-075d-45e3-afe7-b9d0f9d4b34c`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[2], minLevel=3, isLesserEvent=0, LeadsToFortune=1, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `f31efea298e25649e5a4700a97cb56f42ac5aeb5ada90c0ecf3731e776c3eb00`
- **`$.texto`:** 609 caracteres. Início: "You stumble upon an unlikely sight: an <orange><b><incr>Enchanted Pumpkin Patch</incr></b></orange>, nestled amidst the wilderness. Vibrant pumpkins o"...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Take | "Reach down and take a <orange><b><incr>Pumpkin</incr></b></orange>." | bonus=[] | 1 | Success | 0 | **inicia** |
| 2 | Leave | "As enticing as it seems, some treasures are not meant to be taken." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. «Take» inicia batalha no sucesso (opcoes[1].efeitos[1].batalha.iniciar = true, referência resources.assets:2544645 «Cursed Chest Battle», 1 ForcedEnemy com m_PathID 2545119 e VictoryEvent :2545586) e o texto de sucesso descreve exatamente a armadilha do espantalho («a sudden grip, cold and iron-hard»). «Leave» não inicia batalha nem aplica efeito. Texto e configuração estão alinhados. Sem alteração proposta.

**Sinalizações (sem proposta):**

- O GUID real é 3bda807e-075d-45e3-afe7-b9d0f9d4b34c; o literal citado por parte01 (3bda807e-075d-454a-b095-476036a90c8f) não existe.

### 43 — Enchanted Symbol — `resources.assets:2545588`

- **Id (GUID):** `51200c46-6ca9-4e5e-b68d-ee6424dee157`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[], allowedTerrainTypes=[2], minLevel=1, isLesserEvent=1, LeadsToFortune=0, história=Both, modos=Campaign/Roguelike
- **SHA256 do objeto:** `e508ca5622b66018a7cf3fade82e758bc934fd2abe87637ef10ed575673f8a51`
- **`$.texto`:** apenas whitespace (1 caractere): `\n`

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Activate | "Grants [o1a1_status]." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MELHORAR** — natureza: SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (vazio) - inglês (EN)

MELHORAR. Evento menor (isLesserEvent=1) sem nenhuma narrativa: $.texto = '\n' (1 caractere) e $.opcoes[1].efeitos[1].campos_originais.activationText = '' (0 caracteres). A única descrição de opção é «Grants [o1a1_status].», remissão ao candidato do catálogo (status Intelligence, resources.assets:2545387). O evento concede um status real, mas o jogador não recebe contexto algum. Proponho texto exato, em inglês, para os dois campos vazios e uma descrição autoral no lugar da remissão; não proponho mudar título, status, raridade, peso ou condições. Textos propostos em inglês, mesma língua do campo original — NÃO é tradução PT-BR.

**Propostas concretas:**

| # | JSONPath | antes (literal) | depois (literal) | Nota |
|---|---|---|---|---|
| 1 | `$.texto` | `\n` | `A symbol is etched into the stone here, its lines too regular to be anything natural and too worn to be recent. A faint warmth comes off the mark, as though something patient were waiting inside it.` | CAMPO completo (hoje whitespace). Sugestão de texto original, inglês (EN). |
| 2 | `$.opcoes[1].efeitos[1].campos_originais.activationText` | `` | `You lay your hand against the symbol. The warmth climbs your arm, your thoughts sharpen to a fine edge, and the mark dims to a dull, spent grey.` | CAMPO completo (hoje vazio). Sugestão de texto original, EN. Não altera o status concedido. |
| 3 | `$.opcoes[1].texto` | `Grants [o1a1_status].` | `Trace the symbol's lines and take what it offers.` | CAMPO completo. Substitui a remissão ao placeholder por descrição autoral. |

**Sinalizações (sem proposta):**

- O placeholder [o1a1_status] não prova falha de renderização: o JSON resolve o candidato (Intelligence, resources.assets:2545387) e o resultado efetivo depende do runtime, que NÃO foi exercitado.

### 44 — Entangled Boar — `resources.assets:2545589`

- **Id (GUID):** `ad2b9f6c-46c8-4e66-ae0d-8825c3948d41`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[1], minLevel=1, isLesserEvent=0, LeadsToFortune=1, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `31dde506c7176062328d57a18261c88ca218d33aa437a5783d92b39115b50703`
- **`$.texto`:** 540 caracteres. Início: "A <green><b><incr>Wild Boar</incr></b></green>, powerfully built and grim-eyed, is caught in a thorny snare. The thick Bristlethorn, is tough as twist"...
- **`$.texto_resultados_possiveis`:** "Who will approach the boar?"

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Help | "Attempt to free the boar." | bonus=[] | 1 | Success | 11 | não |
| 1 | Help | "Attempt to free the boar." | bonus=[] | 2 | Failure | 1 | não |
| 2 | Leave | "The potential risks are too great." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. «Help» tem rolagem automática (bonus vazio) com Success em limite_rolagem 11 e Failure em limite_rolagem 1; o sucesso concede o status «Boar Charm» (resources.assets:2545413, invocação de Wild Boar) e a falha aplica -30 percentMaxHealth em Self junto do status «Restrained» (2545498, «Reduces @Reflex@ by @20%@ per stack»). «Leave» não tem efeito. Narrativa de sucesso e falha bem diferenciadas, efeito real conferido. Sem alteração proposta.

**Sinalizações (sem proposta):**

- O GUID real é ad2b9f6c-46c8-4e66-ae0d-8825c3948d41; o literal citado por parte01 (ad2b9f6c-46c8-4e6e-b196-ec9bfcf44649) não existe.

### 45 — Eruption! — `resources.assets:2545590`

- **Id (GUID):** `db1ccfd4-c6d4-4dc1-9f7f-8966d93ceb32`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[5], minLevel=1, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `0e8a3cccff2f445fd82bacc042f7ea18779fbde286ca2b77f42914f42bafdb25`
- **`$.texto`:** 480 caracteres. Início: "Suddenly, the ground beneath your feet quakes, and a deafening rumble echoes through the air. The peaceful serenity is shattered as a <red><b><incr>Vo"...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | React | "Flee the cataclysmic eruption." | bonus=['Reflex'] | 1 | Success | 10 | não |
| 1 | React | "Flee the cataclysmic eruption." | bonus=['Reflex'] | 2 | Failure | 1 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. Opção única «React» com rolagem bonus = [{valor:4,nome:Reflex}]: Success em limite 10 concede experiência a Party com razão 0.5; Failure em limite 1 concede XP 0.5 a Party e aplica -30 percentMaxHealth em Self junto do status «Severely Burned» (resources.assets:2545499, «Reduces @Fire Resistance@ by @25%@ per stack»). As quantidades finais são NULL por dependerem de estado de partida (NAO_EXERCITADO). Sem alteração proposta.

### 46 — Etched Monolith — `resources.assets:2545591`

- **Id (GUID):** `81c8fe59-5e3b-4e96-8148-0e89d7ce48f7`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[2], minLevel=1, isLesserEvent=0, LeadsToFortune=1, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `5daf04431c2b5148f22c757a252933a9132e9cb6c5cc2b1f4cc2ea1a79049f80`
- **`$.texto`:** 431 caracteres. Início: "A monolith stands like a sentinel, its massive form casting a long shadow over the sun-baked ground. Crafted from stone, weathered by time, it holds a"...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Activate the blessing | "Press the palm of your hand upon the monolith." | bonus=[] | 1 | Success | 0 | não |
| 2 | Heal from the monolith | "Draw the energy from the stone monolith." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. O id real é 81c8fe59-5e3b-4e96-8148-0e89d7ce48f7, distinto de todos os demais: NÃO há GUID duplicado nesta faixa. As duas opções diferem em efeito (a opção 1 grava o status «Strength» em Self; a opção 2 grava vida_mana 50%/50%) e em texto de sucesso. Sem alteração proposta.

**Retratação:** Supersede integralmente a seção 46 e a «ANOMALIA CRÍTICA» de GUID duplicado (ver A2).

### 47 — Etched Rune — `resources.assets:2545592`

- **Id (GUID):** `c8e5ace5-c340-450b-9d33-c0f525acb410`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[], allowedTerrainTypes=[2], minLevel=1, isLesserEvent=1, LeadsToFortune=0, história=Both, modos=Campaign/Roguelike
- **SHA256 do objeto:** `bab84edef10b964b93c30517de03df1555746a02c540f5f6670bab99f0c28309`
- **`$.texto`:** apenas whitespace (1 caractere): `\n`

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Activate | "Grants [o1a1_status]." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MELHORAR** — natureza: SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (vazio) - inglês (EN)

MELHORAR. Evento menor (isLesserEvent=1, história Both) sem narrativa: $.texto = '\n' (1 caractere) e $.opcoes[1].efeitos[1].campos_originais.activationText = '' (0 caracteres). A descrição da opção é «Grants [o1a1_status].». O status concedido é real e distinto do de #43 («Might», resources.assets:2545388). Este evento foi OMITIDO por parte01, que o substituiu pelo título inexistente «Eternal Flame», e passa a ser tratado explicitamente aqui. Proponho texto exato, em inglês, para os dois campos vazios.

**Propostas concretas:**

| # | JSONPath | antes (literal) | depois (literal) | Nota |
|---|---|---|---|---|
| 1 | `$.texto` | `\n` | `A single rune is cut deep into the floor, its channels dark with age. Nothing about it is lit, yet the air above it bends as though seen through heat.` | CAMPO completo (hoje whitespace). Sugestão de texto original, inglês (EN). |
| 2 | `$.opcoes[1].efeitos[1].campos_originais.activationText` | `` | `[name] crouches and presses [his] palm flat against the rune. Strength floods through [him] - brief, blunt and unmistakable - and the mark goes dark.` | CAMPO completo (hoje vazio). Sugestão de texto original, EN. Placeholders [name] e [his] preservados no padrão do jogo. |
| 3 | `$.opcoes[1].texto` | `Grants [o1a1_status].` | `Press your hand to the rune and take its strength.` | CAMPO completo. Substitui a remissão ao placeholder por descrição autoral. |

**Sinalizações (sem proposta):**

- O placeholder [o1a1_status] não prova falha de renderização (mesmo motivo de #43); runtime NAO_EXERCITADO.

**Retratação:** A seção 47 de parte01 (título «Eternal Flame», GUID inexistente e texto inventado) é substituída integralmente por este evento real.

### 48 — Fickle Fungus — `resources.assets:2545593`

- **Id (GUID):** `9c731a7c-bbce-4c95-a4aa-fd9700ec70f0`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[], minLevel=1, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `52179e662513f40e253b3b7a9652e3c6703a1c71935ecac52931ffd5264a1235`
- **`$.texto`:** 579 caracteres. Início: "Even amidst the fantastical nature of your journey, this particular fungus stands as a peculiar sight that draws you closer.  With a cautious curiosit"...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Resist | "Do your best to weather the poison." | bonus=[] | 1 | Success | 10 | não |
| 1 | Resist | "Do your best to weather the poison." | bonus=[] | 2 | Failure | 0 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. Opção única «Resist»: Success em limite 10 (XP 0.5 a Party) e Failure em limite 0 (-30 percentMaxHealth em Self junto do status «Enfeebled»). O texto original já descreve a nuvem de esporos tóxicos, coerente com a rolagem de resistência. Sem alteração proposta.

**Retratação:** A seção 48 de parte01 (título inventado «Eternal Guard», GUID duplicado falso) é substituída integralmente por este evento real.

### 49 — Foreboding Gem — `resources.assets:2545595`

- **Id (GUID):** `e4dc06e1-2425-4578-9cd7-087d78eb0d18`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[4], minLevel=1, isLesserEvent=0, LeadsToFortune=1, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `29d4e6dd01286594affbb4420e4af66f313016e908f282c47fefbcff9a094d75`
- **`$.texto`:** 844 caracteres. Início: "This cave, previously draped in a sullen darkness, comes alive in a feverish light. The source of this illumination is a <red><b><incr>Giant Ruby</inc"...
- **`$.texto_resultados_possiveis`:** "What will you do?"

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Take | "Grab the ruby before someone else does." | bonus=[] | 1 | Success | 0 | **inicia** |
| 2 | Leave | "Pull yourself away from the allure of the ruby." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. «Take» inicia batalha no sucesso (batalha.iniciar = true, com ForcedEnemies vazio e referência nula — usa o BattleInfo do próprio evento, BattlePointValue 16 —, com VictoryEvent = `resources.assets:2545594` «Foreboding Gem - Victory» e FailureEvent nulo) e o texto descreve a corrida pela gema e o confronto com os outros aventureiros; «Leave» não tem batalha. LeadsToFortune=1 e terreno [4]. Configuração e narrativa estão coerentes entre si. Sem alteração proposta.

**Sinalizações (sem proposta):**

- Bytes residuais: $.opcoes[1].efeitos[1].campos_originais.activationText termina com «\r\n\r» (2 CR, ambos no fim da string). Não proponho alteração porque, sendo fim de string, não há quebra visível nem efeito de conteúdo — fica registrado para referência. Os casos com CR no MEIO da string (54, 59 e 60) recebem proposta de normalização.

### 50 — Fountain of Life — `resources.assets:2545596`

- **Id (GUID):** `b6728bfa-321a-4c53-98c6-9b3d4d8f1ca1`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Rare (valor 2) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[], allowedTerrainTypes=[], minLevel=1, isLesserEvent=1, LeadsToFortune=0, história=Both, modos=Campaign/Roguelike
- **SHA256 do objeto:** `45e46d1a3b9b31e148b453b0858e21e55334678c86ef8b685e09bdc18d02e6bc`
- **`$.texto`:** 42 caracteres. Início: "An enchanted fountain brimming with magic."...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Drink | "Restore health and mana." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. «Drink» aplica vida_mana {percentMaxHealth:10.0, percentMaxMana:10.0} em Self, com Success único em limite 0 e sem ação de falha. O texto é curto (42 caracteres) mas funcional; isLesserEvent=1 e raridade Rare (valor 2) são campos reais e coerentes. Sem alteração proposta.

### 51 — Friend or Foe — `resources.assets:2545597`

- **Id (GUID):** `a5c05b2d-a0d7-4e95-afc6-66beff7d1a6f`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=1, allowedNodeTypes=[0], allowedTerrainTypes=[], minLevel=2, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `b4e3230706ea00e4052c2cc129c289171ac57f6f9c3c7b3e77fbf11ab8fc5130`
- **`$.texto`:** 116 caracteres. Início: "You hear jovial banter as you approach your supposed enemies. Perhaps this situation can be handled more delicately."...
- **`$.texto_resultados_possiveis`:** "What will you do?"

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Persuade | "Convince them you are allies not enemies." | bonus=[] | 1 | Success | 10 | não |
| 1 | Persuade | "Convince them you are allies not enemies." | bonus=[] | 2 | Failure | 0 | **inicia** |
| 2 | Fight | "Straightforward battle is the best way to handle any situation." | bonus=[] | 1 | Success | 0 | **inicia** |

**VEREDITO: MANTER** — natureza: —

MANTER. Evento DESATIVADO (condicoes.disabled=1) — o único da faixa — com allowedNodeTypes=[0]. As opções reais são «Persuade» (Success em limite 10: vida_mana +20/20 em Self, XP 1.0 e itens com limitItemTypes=1 e raridades [1,2,3]; Failure em limite 0 com batalha) e «Fight» (batalha no sucesso único). Estar desativado não autoriza reativar nem remover conteúdo por padrão, e não há defeito demonstrado nas opções reais. Sem alteração proposta.

**Retratação:** A seção 51 de parte01 (título inexistente «Extinguished Altar», chave ausente) é substituída integralmente por este evento real.

### 52 — Furnace Trap — `resources.assets:2545598`

- **Id (GUID):** `37dc56cd-600f-46b8-b0cc-eae8e0e9f0c7`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[], minLevel=1, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `b01526f476347afe1a0a0ffc793b0bcc86a49f6197fa7ec8345cbe27f0c93d45`
- **`$.texto`:** 459 caracteres. Início: "Your path is obstructed by an elaborate trap - a deadly <red><b><incr>Furnace</incr></b></red> of ancient design, capable of reducing even the sturdie"...
- **`$.texto_resultados_possiveis`:** "Who will attempt to disable the trap?"

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Disable | "Brave the flames to disable the trap." | bonus=['Reflex'] | 1 | Success | 10 | não |
| 1 | Disable | "Brave the flames to disable the trap." | bonus=['Reflex'] | 2 | Failure | 1 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. «Disable» com rolagem bonus = [{valor:4,nome:Reflex}]: Success em limite 10 concede XP a Party (razão 1.0); Failure em limite 1 concede XP 0.5 a Party e aplica -30 percentMaxHealth em Self junto do status «Severely Burned». O sha256_objeto do evento é exatamente o citado por parte01 (b01526f476347afe1a0a0ffc793b0bcc86a49f6197fa7ec8345cbe27f0c93d45). Sem alteração proposta.

### 53 — Goblin Scout Tower — `resources.assets:2545599`

- **Id (GUID):** `a443b122-b3e5-4f42-b4b0-bd74a648d40d`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[1, 2], minLevel=3, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `f7f106030888328f5e0db7a89bfd7dc09d12e3d753d3b3a21f696bed6c34103c`
- **`$.texto`:** 290 caracteres. Início: "High above on a weathered timber tower, stands the solitary figure of a <green><incr><b>Goblin Ranger</b></incr></green>. His keen eyes scan the horiz"...
- **`$.texto_resultados_possiveis`:** "What will you do?"

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Strike silently | **vazio** | bonus=['Dexterity'] | 1 | Success | 12 | não |
| 1 | Strike silently | **vazio** | bonus=['Dexterity'] | 2 | Failure | 1 | **inicia** |

**VEREDITO: MANTER** — natureza: —

MANTER, com sinalizações. O evento tem UMA opção real, «Strike silently» (rolagem bonus = [{valor:1,nome:Dexterity}]): Success em limite 12 concede XP 1.0 a Party sem iniciar batalha; Failure em limite 1 inicia batalha com 1 inimigo forçado. Não existem as opções «Attack» e «Sneak past» atribuídas por parte01 e não há defeito demonstrado nas opções reais. Sem alteração proposta.

**Sinalizações (sem proposta):**

- $.opcoes[1].texto (descrição da opção) está vazio (''). O mesmo ocorre em #56 («Fight!») e, no campo equivalente, em #43 e #47. Regra desta parte: só proponho texto onde o EVENTO não tem narrativa alguma ($.texto e activationText vazios: casos 43, 47 e 56); descrição de opção vazia isolada não é defeito por si — registrada sem proposta.
- O fato de o texto de falha repetir a abertura do texto de sucesso («With an expert hand, [name] strikes...») é estilo do asset, não erro de dado.

**Retratação:** Supersede integralmente a seção 53 de parte01 (opções inventadas e MELHORAR sobre opção inexistente).

### 54 — Gold Statue of the First Mountain King — `resources.assets:2545601`

- **Id (GUID):** `a93098ef-da50-40e2-a216-4b0f4e258fda`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Mythic (valor 4) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[4], minLevel=4, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `1fbfa5e7f19f8df65be36dee00d47356bd2b33dbcc9595c4e2dec7e08f17e74a`
- **`$.texto`:** 594 caracteres. Início: "A statue, towering and grand, gleams with a lustre untouched by time. The magnificent statue, cast from pure gold, is a testament to the great skill a"...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Steal | "Give into temptation and take what you can." | bonus=[] | 1 | Success | 0 | **inicia** |
| 2 | Leave | "You can't bring yourself to destroy this monument, the essence of a rich and proud dwarven culture.\r" | bonus=[] | — | **sem ação configurada** | — | — |

**VEREDITO: MELHORAR** — natureza: SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (normalização de bytes CR) - inglês (EN)

MELHORAR. Identidade, raridade (Mythic, valor 4), pool (Normal), peso, condições e efeitos estão corretos e NÃO são propostos para mudança (ver A4). O defeito real é de bytes: o asset mistura CR LF com LF. $.opcoes[1].efeitos[1].campos_originais.activationText («Steal») usa «\r\n\r\n» no meio do texto, enquanto o restante do campo usa «\n\n», e $.opcoes[2].texto («Leave») termina com «\r». Proponho apenas normalizar para o padrão do próprio campo; nenhuma palavra, tag ou placeholder é alterado.

**Propostas concretas:**

| # | JSONPath | antes (literal) | depois (literal) | Nota |
|---|---|---|---|---|
| 1 | `$.opcoes[1].efeitos[1].campos_originais.activationText` | `determination.\r\n\r\nYou pause awkwardly` | `determination.\n\nYou pause awkwardly` | TRECHO. Remove 2 caracteres CR; preserva LF, espaços e os demais bytes. |
| 2 | `$.opcoes[2].texto` | `dwarven culture.\r` | `dwarven culture.` | TRECHO final. Remove 1 CR final; preserva todo o resto, inclusive o apóstrofo e o ponto. |

**Sinalizações (sem proposta):**

- $.opcoes[1].efeitos[1].batalha.referencia = resources.assets:2544646 «Gold Statue of the First Mountain King Battle», com 2 ForcedEnemies: BattleInfo própria do evento, coerente. Registrado, sem proposta.

**Retratação:** Supersede a seção 54 de parte01: a «ANOMALIA DE RARIDADE» e o downgrade para Common ficam retirados (A4), e os GUID/SHA citados por parte01 não correspondem à fonte.

### 55 — Grinder Trap — `resources.assets:2545602`

- **Id (GUID):** `22d9580c-8a7f-45c3-88cc-bb27e307203c`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[], minLevel=1, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `cb553ab3c082faf152bd47cabba6d79301c8d58d8e411673bf80b3e72c439bd6`
- **`$.texto`:** 328 caracteres. Início: "The path ahead is a gauntlet of death. A monstrous contraption of grinding gears and rotating spindles, bristling with razor-sharp spikes. It spins wi"...
- **`$.texto_resultados_possiveis`:** "Who will attempt to disable the trap?"

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Disable | "Dodge through the Trap to reach the kill switch." | bonus=['Dexterity'] | 1 | Success | 10 | não |
| 1 | Disable | "Dodge through the Trap to reach the kill switch." | bonus=['Dexterity'] | 2 | Failure | 1 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. «Disable» com rolagem bonus = [{valor:1,nome:Dexterity}]: Success em limite 10 concede XP 1.0 a Party; Failure em limite 1 aplica -30 percentMaxHealth em Party junto do status «Visually Impaired». Texto, rolagem e efeitos são internamente coerentes, e o sha256_objeto real é cb553ab3c082faf152bd47cabba6d79301c8d58d8e411673bf80b3e72c439bd6 (o literal citado por parte01, e7c7c5b9e3b7e4a8f1d2c6b5a9e8d7c6b5a4e3d2c1b0a9f8e7d6c5b4a3e2d1c0, não existe). Não proponho alteração de balanceamento.

**Sinalizações (sem proposta):**

- Divergência de alvo, registrada SEM proposta: #55 é o único evento da faixa cujo dano de falha mira Party; #52, armadilha irmã, mira Self e dá XP de consolo a Party. Se o dono decidir uniformizar, os campos seriam: campo `alvo` da falha em $.opcoes[1].efeitos[2].efeitos[1].alvo.tipo_override; candidato Party (2) -> Self (0); valor hoje {valor:2,nome:Party}; condição: somente o efeito de -30 percentMaxHealth e o status «Visually Impaired» daquela ação. NÃO é proposta deste parecer e não altera o veredito MANTER.

### 56 — Hard Battle — `resources.assets:2545603`

- **Id (GUID):** `e77a13db-782d-4e5a-b196-ec9bfcf44649`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[1], allowedTerrainTypes=[], minLevel=1, isLesserEvent=0, LeadsToFortune=0, história=Both, modos=Campaign/Roguelike
- **SHA256 do objeto:** `c95004f9f8eb50fc117071dceafe7a4c4220cfe0d2e0e1ee338adc6b1ea445f4`
- **`$.texto`:** VAZIO - string estrita vazia (0 caracteres).

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Fight! | **vazio** | bonus=[] | 1 | Success | 0 | **inicia** |

**VEREDITO: MELHORAR** — natureza: SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (vazio) - inglês (EN)

MELHORAR. É o único evento de combate da faixa (allowedNodeTypes=[1], história Both) e está totalmente sem texto: $.texto = '' (0 caracteres, string estrita vazia), $.texto_resultados_possiveis = '', $.opcoes[1].texto = '' e o activationText do sucesso único = ''. A única opção, «Fight!», inicia batalha (batalha.iniciar = true com referência nula: usa o BattleInfo do próprio evento; itens restritos a possibleItemTypes=[0] e raridades [1,2,3]). Proponho texto exato, em inglês, para os três campos vazios; não altero título, opção, ids, batalha nem recompensa.

**Propostas concretas:**

| # | JSONPath | antes (literal) | depois (literal) | Nota |
|---|---|---|---|---|
| 1 | `$.texto` | `` | `A wall of armed figures bars the way, weapons already bared. No words are offered and none are asked for - only the scrape of steel and the first rush of boots on stone.` | CAMPO completo (hoje vazio). Sugestão de texto original, inglês (EN). |
| 2 | `$.opcoes[1].texto` | `` | `Draw your weapon and meet them head on.` | CAMPO completo (hoje vazio). Sugestão de texto original, EN. |
| 3 | `$.opcoes[1].efeitos[1].campos_originais.activationText` | `` | `Steel meets steel, and the fight is joined.` | CAMPO completo (hoje vazio). Sugestão de texto original, EN. |

**Retratação:** Supersede a seção 56 de parte01: o documento anterior descrevia «Hard Battle» com GUID duplicado falso, «Nulls: 7» e textos de sucesso e falha inexistentes — o evento tem UMA ação, Success, com batalha.

### 57 — Heavy Safe — `resources.assets:2545604`

- **Id (GUID):** `9b45cc6c-33cb-4936-acc7-76140acef17f`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[], minLevel=4, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `848015627b3cfaf0c5cdea5144437fc249f23bd796a7487927c1ddda3882d78f`
- **`$.texto`:** 486 caracteres. Início: "You stand around a <b><gold><incr>Hulking Safe</incr></gold></b>, its matte black exterior reflecting the dim torchlight. The solid steel structure is"...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Attempt | "Try and crack the safe." | bonus=['Dexterity'], misteriosa=true | 1 | Success | 14 | não |
| 1 | Attempt | "Try and crack the safe." | bonus=['Dexterity'], misteriosa=true | 2 | Failure | 1 | não |
| 2 | Leave | "You simply do not have the time to linger here for hours attempting to crack the safe." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MANTER** — natureza: —

MANTER. «Attempt» com rolagem bonus = [{valor:1,nome:Dexterity}] e rolagem misteriosa (misteriosa=true, texto_misterioso vazio): Success em limite 14 concede ouro a Party com razão 15.0 (quantidade_final NULL = NAO_EXERCITADO) e itens restritos a raridades [3,4]; Failure em limite 1 aplica os status «Confused» e «Fatigued». «Leave» não tem efeito. Sem alteração proposta.

**Sinalizações (sem proposta):**

- O sha256_objeto real é 848015627b3cfaf0c5cdea5144437fc249f23bd796a7487927c1ddda3882d78f; o literal citado por parte01 (c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6e5d4) não existe.

### 58 — Hell Coffer — `resources.assets:2545606`

- **Id (GUID):** `f41a780b-f4aa-455c-b26f-895129f63261`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Mythic (valor 4) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[5], minLevel=3, isLesserEvent=0, LeadsToFortune=1, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf24592222c64aca`
- **`$.texto`:** 575 caracteres. Início: "Suspended above a stone pedestal is a <red><b><incr>Hell Coffer</red></b></incr>, an object of legend and fear. Encrusted with jagged obsidian and ado"...
- **`$.texto_resultados_possiveis`:** "What will you do?"

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Open | "Attempt to loot the Hell Coffer." | bonus=[] | 1 | Success | 0 | **inicia** |
| 2 | Leave | "Think better of falling for this devlish trap." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MELHORAR** — natureza: SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (erro literal) - inglês (EN)

MELHORAR. Identidade, raridade (Mythic, valor 4), pool (Normal) e LeadsToFortune=1 estão corretos e não são propostos para mudança (ver A4). O defeito real é lexical: $.opcoes[2].texto («Leave») escreve «devlish», forma que não existe em inglês («devilish»). Correção literal de uma palavra, sem tocar efeitos, batalha (a opção 1 usa resources.assets:2544646 com 7 ForcedEnemies) nem raridade.

**Propostas concretas:**

| # | JSONPath | antes (literal) | depois (literal) | Nota |
|---|---|---|---|---|
| 1 | `$.opcoes[2].texto` | `Think better of falling for this devlish trap.` | `Think better of falling for this devilish trap.` | TRECHO. Substitui «devlish» por «devilish»; o restante do campo fica inalterado. |

**Retratação:** Supersede a seção 58 de parte01: a «ANOMALIA DE RARIDADE» e o MELHORAR por raridade ficam retirados (A4). O sha256_objeto real é f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf24592222c64aca; o literal de parte01, de comprimento incompatível, não existe.

### 59 — Hell Gate — `resources.assets:2545608`

- **Id (GUID):** `afb86d83-6268-409d-a05d-14709b6713f6`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[], minLevel=3, isLesserEvent=0, LeadsToFortune=1, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `f3aead888ba541398e19755201c914cabfae95a44aaabd17880419a34e0cb22d`
- **`$.texto`:** 505 caracteres. Início: "In a conflagration of heat and ash, a <red><b><incr>Hell Gate</incr></b></red> erupts into existence before you. Its molten edges twist and writhe, th"...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Wait | "See what exits the portal to satisfy your curiosity." | bonus=[] | 1 | Success | 0 | **inicia** |
| 2 | Leave | "No amount of curiosity can convince you wait around to see what exits this Infernal Portal." | bonus=[] | 1 | Success | 0 | não |

**VEREDITO: MELHORAR** — natureza: SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (gramática e bytes CR) - inglês (EN)

MELHORAR. As opções reais são «Wait» e «Leave» — nenhuma opção é criada, renomeada ou removida (ver A6). O texto de «Leave» tem erro gramatical (falta «to» antes de «wait around») e o activationText de «Wait» mistura CR LF com LF em dois pontos, além de faltar o espaço depois da vírgula em «"Wrong turn,"he mutters». Proponho a correção literal e a normalização de bytes; nada mais muda.

**Propostas concretas:**

| # | JSONPath | antes (literal) | depois (literal) | Nota |
|---|---|---|---|---|
| 1 | `$.opcoes[2].texto` | `No amount of curiosity can convince you wait around to see what exits this Infernal Portal.` | `No amount of curiosity can convince you to wait around to see what exits this Infernal Portal.` | TRECHO. Insere «to». O restante do campo fica inalterado. |
| 2 | `$.opcoes[1].efeitos[1].campos_originais.activationText` | `confusion.\r\n\r\n"Wrong turn,"he mutters` | `confusion.\n\n"Wrong turn," he mutters` | TRECHO. Remove 2 CR e insere 1 espaço depois da vírgula; preserva LF e o restante do campo. |
| 3 | `$.opcoes[1].efeitos[1].campos_originais.activationText` | `surprised?"\r\n\r\nDespite the dire circumstances` | `surprised?"\n\nDespite the dire circumstances` | TRECHO. Remove 2 CR; preserva LF e o restante do campo. |

**Sinalizações (sem proposta):**

- O sucesso de «Wait» inicia batalha (1 ForcedEnemy) e aplica «Severely Burned» em Self; a narrativa descreve Lord Infernicus emergindo do portal. Registrado como observação de design, sem proposta.

**Retratação:** Supersede a seção 59 de parte01 (opções inventadas «Enter» e «Close», subtítulos propostos e MELHORAR por clareza sobre opções inexistentes).

### 60 — Hold your Breath — `resources.assets:2545609`

- **Id (GUID):** `12d253b1-8643-427b-8f35-8b1f402b1c07`
- **Categoria / Pool:** Normal / Normal
- **Raridade / Peso:** Common (valor 0) / 1.0
- **Condições:** disabled=0, allowedNodeTypes=[7], allowedTerrainTypes=[0], minLevel=4, isLesserEvent=0, LeadsToFortune=0, história=NonStoryOnly, modos=Campaign/Roguelike
- **SHA256 do objeto:** `fc04832c3fe0f3f7b99c1346012c7b53c517cd60ac477653fb70764f2fa579e3`
- **`$.texto`:** 811 caracteres. Início: "A magical reef, completely out of place on dry land, captures your attention instantly. It is as if a slice of the ocean was suddenly transported and "...

**Opções e ações (base 1):**

| Opção | Título | Descrição (`$.opcoes[N].texto`) | Rolagem | Ação | Resultado | limite_rolagem | Batalha |
|---|---|---|---|---|---|---|---|
| 1 | Claim | "Swim towards the treasure." | bonus=['Vitality'] | 1 | Success | 14 | não |
| 1 | Claim | "Swim towards the treasure." | bonus=['Vitality'] | 2 | Failure | 0 | não |

**VEREDITO: MELHORAR** — natureza: SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL (normalização de bytes CR) - inglês (EN)

MELHORAR. Ordinal corrigido: Hold your Breath é o ordinal 60 (resources.assets:2545609) — parte01 o numerava 56 no quadro de visão geral, duplicando Hard Battle (ver A7). A opção real é ÚNICA, «Claim» (rolagem bonus = [{valor:2,nome:Vitality}]): Success em limite 14 concede XP 1.0 e itens (raridades [3,4]) a Party; Failure em limite 0 aplica -35 percentMaxHealth em Self. Nenhuma opção é criada ou renomeada (ver A6). O defeito real é de bytes: em $.texto o separador entre o primeiro e o segundo parágrafo é «\r\n\r\n», enquanto o restante do campo usa «\n\n».

**Propostas concretas:**

| # | JSONPath | antes (literal) | depois (literal) | Nota |
|---|---|---|---|---|
| 1 | `$.texto` | `tube of water.\r\n\r\nGlowing fish` | `tube of water.\n\nGlowing fish` | TRECHO. Remove 2 CR; preserva LF, espaços e o restante do texto (811 caracteres hoje). |

**Retratação:** Supersede a seção 60 de parte01 (título «Disable — Brave the flames to disable the trap», copiado de Furnace Trap, e RollLimit 14/0 descritos como ambíguos) e corrige o ordinal do evento no quadro de visão geral.

## 5. Degrau de confiança e limites

- Toda a análise é **offline**: foram lidos `eventos.json`, `lote-Normal-v2.md`, `eventos.schema.json`, `catalogo-referencias.json` e a proposta anterior. O jogo não foi aberto, nenhuma DLL/plugin foi tocado, nenhuma fonte foi editada, não houve commit, publicação ou push.
- **NAO_EXERCITADO**: quantidades finais de ouro/XP/loot, sorteios de status, escolha de personagem, renderização dos textos e o resultado efetivo das batalhas. Nenhuma afirmação deste documento depende de observação no jogo.
- Os `activationText` citados são os textos autorais gravados no asset (`campos_originais.activationText`), não o que aparece em tela.
- Fora de escopo deste cartão e **não analisados aqui**: o GUID duplicado real de #9 Battle / #10 Battletest Event (`5b740c2b-3480-48f2-997b-88c8291db0c0`, `resources.assets:2545539`/`:2545540`), registrado para cartão próprio; e as faixas 1–40 / 61–160, tratadas em seus próprios cartões.

## 6. Auditoria offline — comando e saída REAL

Comando executado (workspace local):

```
cd C:/dev/stolen-realm/docs/automacao
python EV-R2-NORMAL-b03-validar.py
```

Saída real (exit 0), resumida linha a linha:

```
PASS SOURCES_11_UNCHANGED | {"inputs": 11, "unchanged": 11, "changed": []}
PASS NORMAL_COUNT_160 | 160
PASS MD_EQUALS_JSON_NORMAL_ORDER | {"md_sections": 160, "json_normal": 160, "iguais": true}
PASS GUID_UNICOS | {'total': 256, 'unicos': 255}
PASS GUID_DUPLICADO_REAL_UNICO | {"5b740c2b-3480-48f2-997b-88c8291db0c0": ["resources.assets:2545539", "resources.assets:2545540"]}
PASS GUID_ACUSADO_AUSENTE | {'literal': '81c8fe59-5e3b-4e5e-b196-ec9bfcf44649', 'existe_em_algum_evento': False}
PASS IDENTIDADE_20_POSICOES | {'divergencias': []}
PASS SHA256_OBJETO_20 | {'divergencias': []}
PASS MD_JUSTIFICATIVAS_20_EQ_JSON | {"eventos": 20, "divergencias": []}
PASS P01_LITERAIS_FALSOS | {"guid_ocorrencias": 14, "guid_distintos": ["36c51484-b50b-4681-9e7f-6006b9c27192", "3bda807e-075d-454a-b095-476036a90c8f", "81c8fe59-5e3b-4e5e-b196-ec9bfcf44649", "ad2b9f6c-46c8-4e6e-b196-ec9bfcf44649"], "sha_ocorrencias": 5, "sha_distintos": ["333e0b56943d6300e6306e37748201d4d1879648572c5e4b5b89d12c00d9f737", "c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6e5d4", "d6c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6e5", "e7c7c5b9e3b7e4a8f1d2c6b5a9e8d7c6b5a4e3d2c1b0a9f8e7d6c5b4a3e2d1c0", "f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf2459222c64aca"], "sha_comprimentos": [63, 64]}
PASS P01_SHA58_COMPRIMENTO_INCOMPATIVEL | {"literal": "f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf2459222c64aca", "comprimento": 63, "existe_na_fonte": false, "sha_real_58": "f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf24592222c64aca"}
PASS P01_LITERAL_ACUSADO_PRESENTE_NO_DOC | True
PASS VAZIOS_43_47_56 | [{"ordinal": 43, "titulo": "Enchanted Symbol", "repr": "'\\n'", "len": 1, "estrito_vazio": false, "somente_whitespace": true}, {"ordinal": 47, "titulo": "Etched Rune", "repr": "'\\n'", "len": 1, "estrito_vazio": false, "somente_whitespace": true}, {"ordinal": 56, "titulo": "Hard Battle", "repr": "''", "len": 0, "estrito_vazio": true, "somente_whitespace": false}]
PASS CR_INVENTARIO | [{"ordinal": 49, "jsonpath": "$.opcoes[1].efeitos[1].campos_originais.activationText", "cr": 2, "posicao": "FIM"}, {"ordinal": 54, "jsonpath": "$.opcoes[1].efeitos[1].campos_originais.activationText", "cr": 2, "posicao": "MEIO"}, {"ordinal": 54, "jsonpath": "$.opcoes[2].texto", "cr": 1, "posicao": "FIM"}, {"ordinal": 59, "jsonpath": "$.opcoes[1].efeitos[1].campos_originais.activationText", "cr": 4, "posicao": "MEIO"}, {"ordinal": 60, "jsonpath": "$.texto", "cr": 2, "posicao": "MEIO"}]
PASS ANTES_LITERAIS_CONFERIDOS | {"pass": 16, "falhas": []}
PASS VEREDITOS_13_7 | {"MANTER": 13, "MELHORAR": 7, "outros": []}
PASS ORDINAIS_UNICOS_41_60 | [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
PASS EV41_CURA_50_50 | {"percentMaxHealth": 50.0, "percentMaxMana": 50.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}
PASS EV54_EV58_MYTHIC_POOL_NORMAL | {"54": {"rar": {"valor": 4, "nome": "Mythic"}, "pool": ["Normal"]}, "58": {"rar": {"valor": 4, "nome": "Mythic"}, "pool": ["Normal"]}}
PASS EV53_UMA_OPCAO_STRIKE_SILENTLY | {"opcoes": ["Strike silently"], "acoes": [["Success", 12, false], ["Failure", 1, true]]}
PASS EV59_WAIT_LEAVE | ['Wait', 'Leave']
PASS EV60_HOLD_YOUR_BREATH_ORDINAL_60 | {'titulo': 'Hold your Breath', 'chave': 'resources.assets:2545609', 'opcoes': ['Claim']}
PASS BATALHA_VICTORY_FAILURE_INVENTARIO_20 | [{"ordinal": 42, "opcao": 1, "acao": 1, "resultado": "Success", "referencia": "resources.assets:2544645", "victory_event": 2545586, "failure_event": 0, "forced_enemies": [{"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545119}, "ForcedEnemyMods": [], "IsSuperUnique": 0}], "battle_point_value": 8}, {"ordinal": 49, "opcao": 1, "acao": 1, "resultado": "Success", "referencia": null, "victory_event": 2545594, "failure_event": 0, "forced_enemies": [], "battle_point_value": 16}, {"ordinal": 51, "opcao": 1, "acao": 2, "resultado": "Failure", "referencia": null, "victory_event": 0, "failure_event": 0, "forced_enemies": [], "battle_point_value": 8}, {"ordinal": 51, "opcao": 2, "acao": 1, "resultado": "Success", "referencia": null, "victory_event": 0, "failure_event": 0, "forced_enemies": [], "battle_point_value": 8}, {"ordinal": 53, "opcao": 1, "acao": 2, "resultado": "Failure", "referencia": null, "victory_event": 0, "failure_event": 0, "forced_enemies": [{"OverrideEnemyName": 1, "NameOverride": "Goblin Ranger", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545104}, "ForcedEnemyMods": [], "IsSuperUnique": 1}], "battle_point_value": 8}, {"ordinal": 54, "opcao": 1, "acao": 1, "resultado": "Success", "referencia": "resources.assets:2544646", "victory_event": 2545600, "failure_event": 0, "forced_enemies": [{"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545080}, "ForcedEnemyMods": [], "IsSuperUnique": 1}, {"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545081}, "ForcedEnemyMods": [], "IsSuperUnique": 1}], "battle_point_value": 8}, {"ordinal": 56, "opcao": 1, "acao": 1, "resultado": "Success", "referencia": null, "victory_event": 0, "failure_event": 0, "forced_enemies": [], "battle_point_value": 8}, {"ordinal": 58, "opcao": 1, "acao": 1, "resultado": "Success", "referencia": "resources.assets:2544646", "victory_event": 2545605, "failure_event": 0, "forced_enemies": [{"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545247}, "ForcedEnemyMods": [], "IsSuperUnique": 1}, {"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545249}, "ForcedEnemyMods": [], "IsSuperUnique": 1}, {"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545250}, "ForcedEnemyMods": [], "IsSuperUnique": 1}, {"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545251}, "ForcedEnemyMods": [], "IsSuperUnique": 0}, {"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545251}, "ForcedEnemyMods": [], "IsSuperUnique": 0}, {"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545251}, "ForcedEnemyMods": [], "IsSuperUnique": 0}, {"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545251}, "ForcedEnemyMods": [], "IsSuperUnique": 0}], "battle_point_value": 8}, {"ordinal": 59, "opcao": 1, "acao": 1, "resultado": "Success", "referencia": null, "victory_event": 2545607, "failure_event": 0, "forced_enemies": [{"OverrideEnemyName": 0, "NameOverride": "", "CharacterInfo": {"m_FileID": 0, "m_PathID": 2545159}, "ForcedEnemyMods": [], "IsSuperUnique": 0}], "battle_point_value": 8}]
PASS EV49_BATALHA_VICTORY_EVENT_2545594 | {"referencia": null, "VictoryEvent": {"m_FileID": 0, "m_PathID": 2545594}, "FailureEvent": {"m_FileID": 0, "m_PathID": 0}, "ForcedEnemies": [], "BattlePointValue": 16}
PASS CATALOGO_2545594_FOREBODING_GEM_VICTORY | [{"file": "resources.assets", "path_id": 2545594, "script": "PartyEvent", "nome": "Foreboding Gem - Victory"}]
PASS MD49_VICTORYEVENT_CORRIGIDO | {"frase_falsa_presente": false, "frase_correta_presente": true, "victory_event_citado": true, "failure_event_nulo_citado": true}
PASS INVENTARIO_DISTRIBUICOES | {"raridades": {"Common": 17, "Rare": 1, "Mythic": 2}, "disabled": [51], "opcoes_total": 30, "acoes_com_batalha": [[42, 1, 1, "Success"], [49, 1, 1, "Success"], [51, 1, 2, "Failure"], [51, 2, 1, "Success"], [53, 1, 2, "Failure"], [54, 1, 1, "Success"], [56, 1, 1, "Success"], [58, 1, 1, "Success"], [59, 1, 1, "Success"]], "eventos_com_batalha": [42, 49, 51, 53, 54, 56, 58, 59]}
PASS SEM_PROPOSTA_DE_BALANCEAMENTO | ['SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (erro literal) - ingles (EN)', 'SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (gramatica e bytes CR) - ingles (EN)', 'SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (normalizacao de bytes CR) - ingles (EN)', 'SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (vazio) - ingles (EN)', '—']
TOTAL 28 PASS 28 FAIL 0
OUT C:\dev\stolen-realm\docs\automacao\EV-R2-NORMAL-b03-validacao.json
```

O script lê as fontes em modo somente leitura e grava `EV-R2-NORMAL-b03-validacao.json` (mesmo diretório). Os dados estruturados que originam este documento estão em `EV-R2-NORMAL-b03-propostas.json`, gerados por `EV-R2-NORMAL-b03-gerar-propostas.py` a partir de `eventos.json` (também somente leitura).

### O que a auditoria confere

- **SOURCES_11_UNCHANGED**: PASS
- **NORMAL_COUNT_160**: PASS
- **MD_EQUALS_JSON_NORMAL_ORDER**: PASS
- **GUID_UNICOS**: PASS
- **GUID_DUPLICADO_REAL_UNICO**: PASS
- **GUID_ACUSADO_AUSENTE**: PASS
- **IDENTIDADE_20_POSICOES**: PASS
- **SHA256_OBJETO_20**: PASS
- **MD_JUSTIFICATIVAS_20_EQ_JSON**: PASS
- **P01_LITERAIS_FALSOS**: PASS
- **P01_SHA58_COMPRIMENTO_INCOMPATIVEL**: PASS
- **P01_LITERAL_ACUSADO_PRESENTE_NO_DOC**: PASS
- **VAZIOS_43_47_56**: PASS
- **CR_INVENTARIO**: PASS
- **ANTES_LITERAIS_CONFERIDOS**: PASS
- **VEREDITOS_13_7**: PASS
- **ORDINAIS_UNICOS_41_60**: PASS
- **EV41_CURA_50_50**: PASS
- **EV54_EV58_MYTHIC_POOL_NORMAL**: PASS
- **EV53_UMA_OPCAO_STRIKE_SILENTLY**: PASS
- **EV59_WAIT_LEAVE**: PASS
- **EV60_HOLD_YOUR_BREATH_ORDINAL_60**: PASS
- **BATALHA_VICTORY_FAILURE_INVENTARIO_20**: PASS
- **EV49_BATALHA_VICTORY_EVENT_2545594**: PASS
- **CATALOGO_2545594_FOREBODING_GEM_VICTORY**: PASS
- **MD49_VICTORYEVENT_CORRIGIDO**: PASS
- **INVENTARIO_DISTRIBUICOES**: PASS
- **SEM_PROPOSTA_DE_BALANCEAMENTO**: PASS

## 7. Pedido ao dono

1. Aprovar (ou não) as 16 propostas textuais desta parte — todas em inglês, nenhuma de balanceamento.
2. Confirmar a retratação das sete acusações (A1–A7) e o abandono das recomendações de corrigir GUIDs 46–51 e de rebaixar/mover a raridade de #54/#58.
3. Decidir, se quiser, a uniformização de alvo registrada em #55 (SINALIZAÇÃO, hoje fora do veredito MANTER).

