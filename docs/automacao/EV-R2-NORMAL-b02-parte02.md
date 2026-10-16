# EV-R2-NORMAL-b02-parte02 - Correcao documental dos eventos 21-40 (Lote Normal)

Cartao: t_3456f6a9 - corretivo do cartao original t_d06fd366, derivado da revisao independente t_4c07d669.
Arquivo gerado em: 2026-10-13 (Hora oficial do Brasil).
Documento SUBSTITUI, na leitura, a analise de `docs/automacao/EV-R2-NORMAL-b02-parte01.md`.
O arquivo parte01 e o original **nao foram alterados**: esta correcao e um artefato novo (parte02).

Status: **PROPOSTA** para aprovacao do dono. Nada foi implementado, nenhum asset/DLL foi tocado,
nenhuma fonte de EV-R1 foi modificada, nada foi publicado e nenhum `git push` foi executado.

Escopo: **20 eventos da categoria Normal, ordinais 21-40** (20 eventos unicos).
Ordem dos ordinais: ordem das secoes do JSON/markdown da categoria Normal (alfabetica por titulo),
nunca path_id crescente.

Fontes (somente leitura) e hashes no momento da geracao:
- `eventos_json` -> `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json` sha256 `4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13`
- `lote_normal_md` -> `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-Normal-v2.md` sha256 `83b30ada3d78e596b8c7c0784d5e741b43654b14ab02d5377d8a1b245b84f146`
- `schema` -> `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.schema.json` sha256 `6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc`
- `catalogo` -> `C:/dev/stolen-realm/docs/cobertura/EV-R1/catalogo-referencias.json` sha256 `94077cc887621933abe7bbbbd96e91c5a887478dba8fd000b8f4a4129c3745a5`

Estado de runtime: **NAO_EXERCITADO**. Nenhuma conclusao deste documento depende de execucao no jogo.
Quantidades finais de ouro/XP/loot, sorteios, exibicao de texto na tela e a localizacao selecionada
permanecem nao exercitados (ver `cobertura.nao_exercitado` do eventos.json).

---

## 0. Como ler este documento

| Rotulo | Significado |
|---|---|
| **PROPOSTA DE CONTEUDO** | proposta de conteudo novo para o evento (texto ou valor de configuracao), ancorada no que a fonte ja configura |
| **SUGESTAO DE CORRECAO DO ORIGINAL** | defeito literal medido no texto ingles do proprio asset (ortografia, pontuacao, espaco). Nao e o texto que sera exibido ao jogador hoje; e o literal da fonte que se sugere corrigir |
| **REFUTACAO** | afirmacao da parte01 que a medicao desmente, com o valor real e o caminho na fonte |
| **MANTER** | nenhuma alteracao proposta; manutencao justificada pelo que a fonte ja entrega |
| **MELHORAR** | existe ao menos uma proposta concreta com JSONPath, antes literal e depois exato |

Convencoes de caminho: os JSONPath sao relativos a `eventos.json` (`$.eventos[N]`), em que `N` e
simultaneamente o ordinal da categoria Normal (no array, o indice 0 e o unico evento AfterBattle e o bloco
Normal comeca no indice 1; portanto indice global = ordinal Normal).
Indices de lista sao 0-based; o campo `indice` dentro dos objetos e 1-based (ex.: `opcoes[1]` tem `indice` 2).

Textos de proposta sao escritos **em ingles**, preservando o idioma da fonte; nenhuma traducao PT-BR e
apresentada como texto de asset. Onde houver leitura em portugues, ela aparece como comentario, nunca como literal.

---

## 1. Identidades canonicas da faixa 21-40

Conferido contra `eventos.json` (categoria Normal, ordem do array) e contra os cabecalhos `##` de
`lote-Normal-v2.md`: **20/20 titulos identicos nas duas fontes**.

| # | chave | id | titulo | nome_asset | categoria | raridade | peso | disabled | opcoes |
|---|---|---|---|---|---|---|---|---|---|
| 21 | `resources.assets:2545552` | `00336dd6-9e0d-4a6a-ae09-a285d9a259be` | Boss Fight - Roland | - | Normal | Common(0) | 1.0 | 1 | 2 |
| 22 | `resources.assets:2545554` | `959c1e65-17c3-4405-ab03-47aa9a326334` | Brawler's Brew | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 23 | `resources.assets:2545555` | `9c907851-1c3e-4d43-9286-96559cbfda7f` | Carved Monolith | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 24 | `resources.assets:2545556` | `2ce0dad6-cbb4-4b82-a5fc-5a8eaa096d16` | Carved Rune | - | Normal | Common(0) | 1.0 | 0 | 1 |
| 25 | `resources.assets:2545560` | `19b06250-69cc-41bb-9972-530129c41bf2` | Challenger's Gong | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 26 | `resources.assets:2545562` | `cc9cedb8-b215-4800-b84e-f96c1993fcd3` | Cursed Chest | - | Normal | Rare(2) | 1.0 | 0 | 2 |
| 27 | `resources.assets:2545565` | `4c984e21-93c7-4f85-b9dc-524df02adf00` | Cursed Chest | Cursed Mimic Chest | Normal | Rare(2) | 1.0 | 0 | 2 |
| 28 | `resources.assets:2545563` | `6b49fc7c-abec-4c0c-8cba-3742c795ec50` | Cursed Clock | - | Normal | Common(0) | 1.0 | 0 | 1 |
| 29 | `resources.assets:2545569` | `4361a58d-cc5f-4507-a3a6-c4bc74ffaba7` | Cursed Tome | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 30 | `resources.assets:2545572` | `385b8352-0189-42e2-905c-ee6b0dae867e` | Dark Discoveries | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 31 | `resources.assets:2545573` | `03048d72-af64-4337-8ae9-7475981d36e5` | Dead Adventurer | - | Normal | Common(0) | 1.0 | 1 | 2 |
| 32 | `resources.assets:2545576` | `31c21c13-d1fb-4be8-9d45-299dbad44e9e` | Desecrated Statue of the First Mountain King | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 33 | `resources.assets:2545577` | `06f45978-e4ec-44bf-b216-cd3c84686572` | Disturbing Diner | - | Normal | Common(0) | 1.0 | 0 | 3 |
| 34 | `resources.assets:2545578` | `5777d2ca-8fca-485d-92c8-239f6da0e8a4` | Dwarven Drinking Contest | - | Normal | Common(0) | 1.0 | 1 | 2 |
| 35 | `resources.assets:2545579` | `7b6c58f0-2671-429e-9807-780a7695d9d8` | Dwarven Sentry Wall | - | Normal | Common(0) | 1.0 | 0 | 1 |
| 36 | `resources.assets:2545580` | `534013a8-7402-4b00-95aa-dbd337d35ccf` | Dwarven Tomb | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 37 | `resources.assets:2545581` | `7022fe7d-f9fb-4407-82ef-4e10f5d45d68` | Dwarven Tribute | - | Normal | Legendary(3) | 1.0 | 0 | 1 |
| 38 | `resources.assets:2545582` | `4af726e7-657e-403a-883b-e3221fdd700c` | Edwin's Demise | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 39 | `resources.assets:2545583` | `2779cca5-013a-4bbc-ba32-e7d25ef7c8b7` | Elder Tree | - | Normal | Common(0) | 1.0 | 0 | 2 |
| 40 | `resources.assets:2545584` | `b0370015-64ef-4d3c-ac98-d2468992d12d` | Enchanted Axe | - | Normal | Common(0) | 1.0 | 0 | 1 |

Observacoes de identidade:
- Ordinal 27: titulo do evento `Cursed Chest`, `nome_asset` `Cursed Mimic Chest` e `EventNameOverride` `Cursed Chest`;
  e a segunda variante da arca da faixa (a primeira e o ordinal 26).
- Ordinais 26 e 27 tem textos identicos entre si; ordinais 31 e 34 tem textos, opcoes e efeitos identicos entre si.
- Nenhum dos 20 eventos repete chave ou id: 20 chaves unicas e 20 ids unicos (ver Analise C).

---

## 2. Supersessao explicita das afirmacoes da parte01

### 2.1 Identidade: as 20 chaves da parte01 estao deslocadas

A parte01 usou chaves de `resources.assets:2545402` a `resources.assets:2545421`, nenhuma delas
pertencente a esta faixa. **0/20 pares titulo+chave corretos.** O deslocamento e sistematico (a chave
usada e ~150 menor que a real), o que produziu a cascata de analises sobre eventos que nao sao estes.

| ordinal | chave da parte01 (falsa) | chave real | titulo da parte01 (quando falso) | titulo real |
|---|---|---|---|---|
| 21 | `resources.assets:2545402` | `resources.assets:2545552` | Boss Fight - Roland (titulo correto; raridade/peso/texto falsos) | Boss Fight - Roland |
| 22 | `resources.assets:2545403` | `resources.assets:2545554` | correto | Brawler's Brew |
| 23 | `resources.assets:2545404` | `resources.assets:2545555` | Cursed Coin Toss -> Carved Monolith | Carved Monolith |
| 24 | `resources.assets:2545405` | `resources.assets:2545556` | Carved Rune (titulo correto) | Carved Rune |
| 25 | `resources.assets:2545406` | `resources.assets:2545560` | correto | Challenger's Gong |
| 26 | `resources.assets:2545407` | `resources.assets:2545562` | correto | Cursed Chest |
| 27 | `resources.assets:2545408` | `resources.assets:2545565` | Cursed Mimic Chest -> Cursed Chest (2a variante) | Cursed Chest |
| 28 | `resources.assets:2545409` | `resources.assets:2545563` | correto | Cursed Clock |
| 29 | `resources.assets:2545410` | `resources.assets:2545569` | correto | Cursed Tome |
| 30 | `resources.assets:2545411` | `resources.assets:2545572` | correto | Dark Discoveries |
| 31 | `resources.assets:2545412` | `resources.assets:2545573` | correto | Dead Adventurer |
| 32 | `resources.assets:2545413` | `resources.assets:2545576` | correto | Desecrated Statue of the First Mountain King |
| 33 | `resources.assets:2545414` | `resources.assets:2545577` | correto | Disturbing Diner |
| 34 | `resources.assets:2545415` | `resources.assets:2545578` | Disturbing Statue -> Dwarven Drinking Contest | Dwarven Drinking Contest |
| 35 | `resources.assets:2545416` | `resources.assets:2545579` | correto | Dwarven Sentry Wall |
| 36 | `resources.assets:2545417` | `resources.assets:2545580` | correto | Dwarven Tomb |
| 37 | `resources.assets:2545418` | `resources.assets:2545581` | correto | Dwarven Tribute |
| 38 | `resources.assets:2545419` | `resources.assets:2545582` | Dwarven Forge -> Edwin's Demise | Edwin's Demise |
| 39 | `resources.assets:2545420` | `resources.assets:2545583` | Dwarven Market -> Elder Tree | Elder Tree |
| 40 | `resources.assets:2545421` | `resources.assets:2545584` | correto | Enchanted Axe |

### 2.2 As cinco acusacoes da revisao e o que a medicao mostra

| # | Acusacao da revisao | Situacao apos a medicao | Evidencia |
|---|---|---|---|
| 1 | As 20 chaves estao erradas; 0/20 pares titulo+chave | CONFIRMADA | Secao 2.1; ordinal 21 = `resources.assets:2545552`, Common, peso 1.0, disabled 1, texto de 80 ch, opcoes Laugh/Cower |
| 2 | Titulos inventados em 23/27/34/38/39 | CONFIRMADA; titulos reais: Carved Monolith, Cursed Chest (2a variante), Dwarven Drinking Contest, Edwin's Demise, Elder Tree | Secao 1 e blocos 23/27/34/38/39; cada um teve a acao real reanalisada, nao apenas renomeada |
| 3 | Alegacao de Failure ausente em 26/28/35/36/40 e falsa | CONFIRMADA. Acao Failure presente e medida em 26 (limiar 0), 28 (1), 35 (1), 36 (1), 40 (1) | Efeitos reais: Cursed (26), Slowed (28), -30% max HP + Severely Burned (35), Weakened (36), -20% max HP + Mortally Wounded (40) |
| 4 | Vazios narrativos sao 24/37; disabled sao 21/31/34; Brawler's Brew (22) esta habilitado com Drink/Leave | CONFIRMADA, com precisao: 24 tem `\n` (1 caractere) e 37 tem cadeia vazia; disabled = 21, 31, 34; 22 tem disabled=0 e exatamente 2 opcoes, Drink e Leave | Analise C e blocos 22/24/31/34/37 |
| 5 | Falta veredito MANTER/MELHORAR por evento e inventario; investigacao vaga; portugues misturado | CONFIRMADA e corrigida: 20/20 vereditos com justificativa (secao 3), 19 propostas com JSONPath/antes/depois, 65 refutacoes, texto integralmente em PT-BR | Secoes 3, 4 e 5 |

### 2.3 Contagens da parte01 versus medicao

| Afirmacao da parte01 | Valor medido | Correcao |
|---|---|---|
| 3 eventos com `texto` vazio (21, 24, 37) | 2 eventos sem narrativa: 24 (`\n`) e 37 (`""`) | o 21 tem texto de 80 caracteres |
| 2 eventos com `disabled: 1` (22, 31) | 3 eventos: 21, 31, 34 | o 22 esta habilitado (disabled=0) |
| 6 eventos com 1 unica opcao (21, 24, 28, 35, 37, 40) | 5 eventos: 24, 28, 35, 37, 40 | o 21 tem 2 opcoes (Laugh, Cower) |
| 5 eventos sem texto de resultado (25, 27, 29, 32, 34) | 5 eventos com pelo menos uma acao sem texto de resultado: 21, 24, 25, 29, 37 | lista e criterio estavam errados; 27, 32 e 34 tem textos de resultado completos |
| 6 eventos com rolagem sem Failure (26, 27, 28, 36, 38, 39) | 2 eventos com bonus de rolagem e sem Failure: 27 e 33 | 26, 28, 36 e 38 tem Failure; 39 nao tem rolagem |
| EVT 21 RARIDADE Boss, peso 0.1 | Common(0), peso 1.0 | nao existe raridade Boss entre os eventos da faixa; 37 e o unico Legendary |
| "6 eventos sem Failure" como defeito de tensao | 6 eventos tem Failure e 8 tem rolagem | ver Analise C |
| Distribuicao de terrenos "Plains, Underground Cave, Mountain Pass, Dark Forest, Dwarven Depths, Snowy Mountain Peak" | terrenos nomeados por `enums.json` (WaterTempleRuins, WyrmrestDesert, FreewindForest, CastleGloom, ForgottenMines, Emberlands, EmeraldJungle, FrostwroughtMountain, SunkenSwamplands, DwarvenHalls) | nomes da parte01 nao correspondem ao enum da fonte |

---

## 3. Inventario de decisoes (MANTER / MELHORAR)

| Veredito | Quantidade | Ordinais |
|---|---|---|
| MANTER | 9 | 23, 25, 28, 29, 30, 31, 33, 34, 40 |
| MELHORAR | 11 | 21, 22, 24, 26, 27, 32, 35, 36, 37, 38, 39 |

| # | titulo | veredito | propostas | natureza das propostas |
|---|---|---|---|---|
| 21 | Boss Fight - Roland | MELHORAR | 1 | texto de prompt ausente |
| 22 | Brawler's Brew | MELHORAR | 1 | ortografia (artigo indefinido) |
| 23 | Carved Monolith | MANTER | 0 | - |
| 24 | Carved Rune | MELHORAR | 2 | narrativa principal ausente; texto de resultado da acao ausente |
| 25 | Challenger's Gong | MANTER | 0 | - |
| 26 | Cursed Chest | MELHORAR | 1 | ortografia (confusao bares/bears) |
| 27 | Cursed Chest | MELHORAR | 1 | ortografia (confusao bares/bears) |
| 28 | Cursed Clock | MANTER | 0 | - |
| 29 | Cursed Tome | MANTER | 0 | - |
| 30 | Dark Discoveries | MANTER | 0 | - |
| 31 | Dead Adventurer | MANTER | 0 | - |
| 32 | Desecrated Statue of the First Mountain King | MELHORAR | 3 | espaco duplo no texto de resultado; ortografia (confusao bares/bears); quantidade de item incompativel com a narrativa |
| 33 | Disturbing Diner | MANTER | 0 | - |
| 34 | Dwarven Drinking Contest | MANTER | 0 | - |
| 35 | Dwarven Sentry Wall | MELHORAR | 1 | ortografia (quitely/quietly) |
| 36 | Dwarven Tomb | MELHORAR | 1 | ortografia (its/it's) |
| 37 | Dwarven Tribute | MELHORAR | 3 | narrativa principal ausente; texto da opcao vazio; texto de resultado da acao ausente |
| 38 | Edwin's Demise | MELHORAR | 3 | espaco inicial no texto original; ortografia (Infact/In fact); pontuacao (ponto duplo) |
| 39 | Elder Tree | MELHORAR | 2 | espaco inicial no texto da opcao; narrativa duplicada (dois inicios) |
| 40 | Enchanted Axe | MANTER | 0 | - |

Total de propostas: **19** (7 de conteudo, 12 de correcao do texto original).

---

## 4. Evento por evento

### 21 - Boss Fight - Roland

| campo | valor |
|---|---|
| chave | `resources.assets:2545552` |
| id | `00336dd6-9e0d-4a6a-ae09-a285d9a259be` |
| nome_asset | Boss Fight - Roland |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 1 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | qualquer |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545552 |
| sha256_objeto | `7c81dd08ecda2c552e12018d13a3d7f3aea070ae6f1e7072ac27b130b538df19` |

**Estado real medido.** texto = <color=#7f2b0a><b>Roland:</b></color> "Go on!  Come at me and see what happens!" (80 ch); texto_resultados_possiveis = "" (vazio); 2 opcoes: "Laugh" (Self -> Curse of the Reaper 2545422; batalha iniciar=true, BattleInfo "Boss Fight - Roland" 2544644) e "Cower" (Self -> Endurance 2545438; mesma batalha). Nenhuma rolagem (bonus [], RollLimit 0) e nenhuma acao Failure em nenhuma das duas opcoes. disabled=1; raridade Common(0); peso 1.0; NodeType Event(7); LeadsToFortune=1.

**Veredito: MELHORAR.** Narrativa de abertura presente (80 caracteres, fala de Roland) e dois ramos jogaveis com status distintos; falta apenas o prompt de selecao que os eventos irmaos usam. Nao se propoe reativar o slot disabled.

**Propostas:**

1. [PROPOSTA DE CONTEUDO] natureza: texto de prompt ausente
   - caminho: `$.eventos[21].texto_resultados_possiveis`
   - tipo de conferencia: campo integral (antes = valor exato do campo)
   - antes: ``
   - depois: `What will you do?`
   - fundamento: O literal "What will you do?" ja e usado pelos eventos 26, 27, 28 e 36 desta mesma faixa; o 21 e o unico dos cinco eventos que iniciam batalha (21, 25, 26, 27, 29) sem prompt de selecao. Sem efeito de jogo: campo e apenas texto de interface.

**Refutacoes a parte01:**

- parte01: "EVT 21 ... RARIDADE: Boss - Peso: 0.1" -> falso. 21 e Common(0) com peso 1.0 (raridade.valor=0, peso=1.0).
- parte01: "texto = (vazio)" -> falso. O texto tem 80 caracteres (fala de Roland).
- parte01: "1 unica opcao (FIGHT)" -> falso. Sao 2 opcoes: Laugh e Cower.
- parte01: chave resources.assets:2545402 -> falso. A chave real e resources.assets:2545552 (id 00336dd6-9e0d-4a6a-ae09-a285d9a259be).
- parte01: "apenas Success (RollLimit 15) ... sem Failure" -> falso quanto ao limite (RollLimit 0 em ambas as acoes) e quanto a inexistencia de Failure ser defeito: com limiar 0 nao existe ramo de falha a exigir.

**Observacoes (sem proposta):**

- O efeito da opcao 1 e "Curse of the Reaper": StatusType Fortune(1), "Increases Life Steal by 6%. Reduces Max Life by 15%." - ha troca de risco/beneficio, nao um premio puro.
- As duas opcoes conduzem a MESMA batalha (BattleInfo 2544644); a diferenca e o status concedido. Dado observado, sem alteracao proposta.
- disabled=1 registrado como decisao de configuracao do asset; nenhuma proposta de reativacao (regra de curadoria: nao reativar slots disabled por padrao).

**Referencias NULL do evento: 22 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 22 - Brawler's Brew

| campo | valor |
|---|---|
| chave | `resources.assets:2545554` |
| id | `959c1e65-17c3-4405-ab03-47aa9a326334` |
| nome_asset | Brawler's Brew |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | qualquer |
| horario | 1 (allowAtAllTimesOfDay=0) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545554 |
| sha256_objeto | `7b2e2bdccadf365a4a3054bb8a9f3d23e266bba3d5b7465e1491e5ebaf62781f` |

**Estado real medido.** texto (354 ch) termina com "I'm blind as a bat, but I've the strength of a ogre!"; 2 opcoes: "Drink" (Self -> Brawler's Brew 2545414, StatusType Fortune(1), "Might increased by {12,60}. Applies Blind at the start of your turn."; XP dar=false com razao 3.0) e "Leave" (texto imersivo, sem acao) . disabled=0; Common(0); peso 1.0; minLevel 1; allowAtAllTimesOfDay=0/allowedTimeOfDay=1 (somente noite); terreno liberado em qualquer terreno com lista de excecao [WaterTempleRuins, ForgottenMines, CastleGloom, Emberlands].

**Veredito: MELHORAR.** Evento ativo, com narrativa de 354 caracteres e duas opcoes coerentes; a unica alteracao defensavel e uma correcao ortografica pontual no texto original.

**Propostas:**

1. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: ortografia (artigo indefinido)
   - caminho: `$.eventos[22].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `the strength of a ogre!`
   - depois: `the strength of an ogre!`
   - fundamento: Antes de vogal o artigo indefinido ingles e "an". O trecho consta da nota manuscrita do alquimista dentro do proprio texto do evento.

**Refutacoes a parte01:**

- parte01: "3 opcoes (DRINK, SELL, LEAVE)" -> falso. Sao 2 opcoes: Drink e Leave.
- parte01: "Opcao 2 (SELL) tem status_requeridos: [5] - requer status Brawler's Blessing" -> falso. Nenhuma opcao desta faixa tem status_requeridos (a lista e vazia em todas as 36 opcoes dos 20 eventos).
- parte01: "disabled: 1 - evento DESLIGADO" -> falso. disabled=0; o evento esta habilitado.

**Observacoes (sem proposta):**

- O espaco duplo final em opcoes[0].efeitos[0].texto ("fuzzy." ") e cosmetico; registrado em Analise A, sem proposta.
- Nenhuma opcao desta faixa concede ouro (ouro.dar=false em todas): o evento e de status, nao de economia.

**Referencias NULL do evento: 13 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 23 - Carved Monolith

| campo | valor |
|---|---|
| chave | `resources.assets:2545555` |
| id | `9c907851-1c3e-4d43-9286-96559cbfda7f` |
| nome_asset | Carved Monolith |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | qualquer (allowOnAllTerrainTypes=1), exceto: [2] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545555 |
| sha256_objeto | `551ab679d3521dde0065580480f499a63bf97c7f4d3471bbf7da9302cd2d9bb6` |

**Estado real medido.** texto (417 ch) descreve o monolito de obsidiana e a runa esmeralda; 2 opcoes: "Activate the blessing" (Self -> Celerity 2545417, Fortune(1), "Dexterity increased by {4,20}.") e "Heal from the monolith" (Self, percentMaxHealth=50.0 e percentMaxMana=50.0 - cura real configurada). Ambas Success com RollLimit 0, sem rolagem. disabled=0; Common(0); peso 1.0; minLevel 1; terreno restrito a FreewindForest(2).

**Veredito: MANTER.** Narrativa completa (417 ch), duas escolhas com efeitos distintos e mensuraveis, sem defeito literal detectado. Nao ha proposta defensavel que nao seja preferencia de estilo.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: titulo "EVT 23: Cursed Coin Toss" -> falso. O ordinal 23 e "Carved Monolith" (resources.assets:2545555, id 9c907851-1c3e-4d43-9286-96559cbfda7f).
- parte01: "3 opcoes de escolha (HEADS, TAILS, WALK AWAY)" -> falso. Sao 2 opcoes (Activate the blessing / Heal from the monolith).
- parte01: "texto = (vazio)" -> falso. O texto tem 417 caracteres.

**Observacoes (sem proposta):**

- A opcao 2 tem cura de 50% de vida e mana maximas sem rolagem; a opcao 1 entrega status permanente de quest (Celerity, durationType=Quest). Ambas as recompensas sao medidas na fonte.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 24 - Carved Rune

| campo | valor |
|---|---|
| chave | `resources.assets:2545556` |
| id | `2ce0dad6-cbb4-4b82-a5fc-5a8eaa096d16` |
| nome_asset | Carved Rune |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | Both / None |
| minLevel | 1 |
| node types | [] (allowOnAllNodeTypes=1) |
| terreno | qualquer (allowOnAllTerrainTypes=1), exceto: [2] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 1 / 0 |
| origem | `resources.assets` path_id 2545556 |
| sha256_objeto | `ba8b885d478c890b47daa60643a44d5f2095aeb8605e98798e2ae7b17957e70d` |

**Estado real medido.** texto = "\n" (1 caractere: apenas quebra de linha); 1 opcao "Activate" com texto "Grants [o1a1_status]."; acao Success com texto "" (vazio) -> Self -> Dexterity 2545380 (StatusType Normal(0), "Dexterity increased by [0]."); batalha iniciar=false. remocoes_status contem 1 regra cujo ActionOnRemoval e referencia nula (m_PathID 0) - registrada como NULL, sem inferir remocao efetiva. disabled=0; Common(0); peso 1.0; isLesserEvent=1; StorySetting Both(2); allowedNodeTypes=[] com allowOnAllNodeTypes=0.

**Veredito: MELHORAR.** Vazio narrativo real: o campo texto contem apenas o caractere de nova linha e a acao de resultado nao tem texto. E o caso em que a correcao documental propoe conteudo, preservando o ingles da fonte.

**Propostas:**

1. [PROPOSTA DE CONTEUDO] natureza: narrativa principal ausente
   - caminho: `$.eventos[24].texto`
   - tipo de conferencia: campo integral (antes = valor exato do campo)
   - antes: `\n`
   - depois: `A flat stone tablet leans against the rock, its face cut with a single dwarven rune. The carving is worn smooth in places, as though many hands have traced it before yours.`
   - fundamento: O evento e um achado de runa que concede Dexterity; a proposta descreve apenas a cena e o objeto, sem introduzir mecanica, valor ou condicao nova. Texto em ingles para preservar o idioma da fonte.
2. [PROPOSTA DE CONTEUDO] natureza: texto de resultado da acao ausente
   - caminho: `$.eventos[24].opcoes[0].efeitos[0].texto`
   - tipo de conferencia: campo integral (antes = valor exato do campo)
   - antes: ``
   - depois: `You press your palm to the rune. A cool current climbs your arm, and your fingers feel lighter, quicker than before.`
   - fundamento: O unico efeito configurado e o status Dexterity em Self; a proposta narra exatamente esse efeito, sem acrescentar alvo, quantidade ou condicao.

**Refutacoes a parte01:**

- parte01: "texto = (vazio)" -> parcialmente impreciso: o campo tem 1 caractere ("\n"), nao cadeia vazia. O efeito pratico (nenhuma narrativa exibida) e o mesmo; o dado exato importa para a correcao.
- parte01: "Exemplo: ... itens de rarezas Uncommon/Very Rare - loot significativo" -> falso. Nao ha recompensa de item configurada (itens.dar=false); o unico efeito e o status Dexterity.
- parte01: "Opcao tem rolagem com Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. Nao ha rolagem (rolagem.bonus=[], limite_rolagem=0).

**Observacoes (sem proposta):**

- O unico evento da faixa com 3 campos de texto relevantes vazios simultaneamente (evento, opcao e resultado) e o 37; o 24 tem a opcao preenchida ("Grants [o1a1_status].").

**Referencias NULL do evento: 13 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 25 - Challenger's Gong

| campo | valor |
|---|---|
| chave | `resources.assets:2545560` |
| id | `19b06250-69cc-41bb-9972-530129c41bf2` |
| nome_asset | Challenger's Gong |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [7] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545560 |
| sha256_objeto | `b1e3e322ff0cb1c68470bc97548447ae6948883b3f2924f2793e8f60daa2ff2a` |

**Estado real medido.** texto (481 ch); 2 opcoes: "Strike" (Success RollLimit 0, com texto de resultado, batalha iniciar=true sem BattleInfo referenciado) e "Leave" (texto "The fear of the unknown grips your spirit..." e acao Success sem efeito). disabled=0; Common(0); peso 1.0; minLevel 1; terreno restrito a FrostwroughtMountain(7); LeadsToFortune=1.

**Veredito: MANTER.** Narrativa presente nas duas opcoes (481 ch no evento; texto tambem na opcao Strike) e ausencia de falha justificada pelo limiar 0. A referencia de batalha nula e NULL declarado, nao defeito demonstravel offline.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: "Chave: resources.assets:2545406" -> falso. Chave real resources.assets:2545560 (id 19b06250-69cc-41bb-9972-530129c41bf2).
- parte01: "opcoes[0].texto = (vazio no asset)" -> falso. O texto da opcao 1 e "Ring the gong and issue a challenge.".
- parte01: "2 opcoes: STRIKE (Success) e IGNORE" -> impreciso. A segunda opcao chama-se "Leave".

**Observacoes (sem proposta):**

- batalha.referencia.chave/nome sao NULL em ambas as acoes da opcao 1: registro de referencia nula, cujo motivo e "referencia nula, resultado dependente de runtime ou valor nulo do leitor". Nao se infere batalha vazia nem recompensa ausente.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 26 - Cursed Chest

| campo | valor |
|---|---|
| chave | `resources.assets:2545562` |
| id | `cc9cedb8-b215-4800-b84e-f96c1993fcd3` |
| nome_asset | Cursed Chest |
| categoria | Normal |
| raridade | Rare(2) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 3 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [3, 4, 8, 9] |
| horario | 1 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=0 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545562 |
| sha256_objeto | `8f4b22817619c32879e781c4e5ab70170c737f52d7fc9f7ee217e9dccf723a73` |

**Estado real medido.** texto (453 ch); texto_resultados_possiveis = "What will you do?"; 2 opcoes: "Open" (rolagem Intel+3 via rollBonusTypes [3]) com acao Success (RollLimit 12) e acao Failure (RollLimit 0, Self -> Cursed 2545493, "Reduces All Stats by 10% per stack"), ambas iniciando a batalha BattleInfo 2544645 "Cursed Chest Battle" (battlePointValue 16); e "Leave". XP configurado com dar=false e razao 2.0. disabled=0; Rare(2); peso 1.0; minLevel 3; LeadsToFortune=0.

**Veredito: MELHORAR.** Evento mais completo da faixa (rolagem com limiar, ramo Success e Failure, ambos com batalha referenciada e evento de vitoria encadeado). A unica alteracao defensavel e a correcao ortografica do texto original.

**Propostas:**

1. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: ortografia (confusao bares/bears)
   - caminho: `$.eventos[26].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `warped and decayed, bares the weight of forgotten sorrows`
   - depois: `warped and decayed, bears the weight of forgotten sorrows`
   - fundamento: O verbo correto e "bears" (suportar, carregar); "bares" e o verbo despir. Mesmo defeito repete-se no ordinal 27 e no 32.

**Refutacoes a parte01:**

- parte01: "Opcao 1 (OPEN) tem rolagem Intelligence +3, RollLimit 12 - mas sem acao Failure" -> falso. Existe acao Failure (acesso idx 2, RollLimit 0) que aplica o status Cursed e inicia a mesma batalha.
- parte01: "Texto de Success ... curto. Sem Failure" -> falso quanto ao Failure: o texto de falha tem 245 caracteres e descreve o nepente e o ataque dos mortos-vivos.
- parte01: "2 opcoes: OPEN e IGNORE" -> impreciso. A segunda opcao chama-se "Leave".

**Observacoes (sem proposta):**

- O campo batalha.dados_recompensa_final e NULL e explicitamente nao exercitado em runtime; nao se infere recompensa da batalha.
- O BattleInfo 2544645 encadeia VictoryEvent 2545561 = PartyEvent "Cursed Chest Battle Victory" (categoria NotInEventPool, EventNameOverride "Cursed Chest"), que entrega o loot da arca. Encadeamento medido na fonte.

**Referencias NULL do evento: 22 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 27 - Cursed Chest

| campo | valor |
|---|---|
| chave | `resources.assets:2545565` |
| id | `4c984e21-93c7-4f85-b9dc-524df02adf00` |
| nome_asset | Cursed Mimic Chest |
| categoria | Normal |
| raridade | Rare(2) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 4 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [3, 4, 8, 9] |
| horario | 1 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=0 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545565 |
| sha256_objeto | `ce41a0de26b8daeb0373533e364d569287c979cdc1d75ba4d4890cf219173d35` |

**Estado real medido.** titulo "Cursed Chest"; nome_asset "Cursed Mimic Chest"; campos_originais.EventNameOverride "Cursed Chest"; texto (453 ch) identico ao do ordinal 26; texto_resultados_possiveis = "What will you do?"; 2 opcoes: "Open" (rolagem Intel+3 com rollBonusTypes [3], mas acao unica Success com RollLimit 0, texto do mimic, batalha BattleInfo 2544645 "Cursed Chest Battle") e "Leave". disabled=0; Rare(2); peso 1.0; minLevel 4 (um a mais que o 26); LeadsToFortune=1 (o 26 tem 0).

**Veredito: MELHORAR.** Segunda variante da arca amaldicoada, com titulo de evento identico ao 26 e nome_asset proprio. Texto do evento e das opcoes identicos ao 26. A alteracao defensavel e a mesma correcao ortografica; a assimetria de rolagem fica documentada como decisao do dono.

**Propostas:**

1. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: ortografia (confusao bares/bears)
   - caminho: `$.eventos[27].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `warped and decayed, bares the weight of forgotten sorrows`
   - depois: `warped and decayed, bears the weight of forgotten sorrows`
   - fundamento: Mesma correcao do ordinal 26; o texto e literalmente o mesmo.

**Refutacoes a parte01:**

- parte01: titulo "EVT 27: Cursed Mimic Chest" -> impreciso. O titulo do evento e "Cursed Chest"; "Cursed Mimic Chest" e o nome_asset. A variante e a segunda arca da faixa.
- parte01: "Opcao 1 tem rolagem Intelligence +3, RollLimit 0 - sem rolagem real" -> o bonus e o limiar foram medidos corretamente, mas a conclusao "ambiguidade" fica substituida pelo dado: rollBonusTypes=[3] com EventResultSetting RollLimit=0.
- parte01: "Efeito de OPEN: inicia combate com Cursed Mimic (boss fight)" -> a batalha referenciada e a mesma do ordinal 26 (BattleInfo 2544645 "Cursed Chest Battle"); "boss fight" nao consta da fonte.

**Observacoes (sem proposta):**

- Assimetria medida: o 26 usa o mesmo rollBonusTypes=[3] com RollLimit 12 e ramo Failure; o 27 usa RollLimit 0 sem Failure. Nenhuma alteracao proposta sem decisao do dono, porque alteraria jogabilidade (probabilidade e efeito de falha).
- A diferenca LeadsToFortune (26=0, 27=1) e dado de configuracao, sem inferencia sobre recompensa.

**Referencias NULL do evento: 11 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 28 - Cursed Clock

| campo | valor |
|---|---|
| chave | `resources.assets:2545563` |
| id | `6b49fc7c-abec-4c0c-8cba-3742c795ec50` |
| nome_asset | Cursed Clock |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 3 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [3] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=0 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545563 |
| sha256_objeto | `cc4fd4c22fd7a756a429cc03031779717e48c779e4636a598e267c8faf96a246` |

**Estado real medido.** texto (530 ch); texto_resultados_possiveis = "What will you do?"; 1 opcao "Pull Away" com rolagem Might (rollBonusTypes [0], valor 0) e duas acoes: Success (RollLimit 8) -> XP dar=true razao 0.5 com alvo Party (OverrideTargetType 1 / TargetTypeOverride 2); Failure (RollLimit 1) -> Self -> Slowed 2545501 ("Cooldowns increased by 1 turn."). disabled=0; Common(0); peso 1.0; minLevel 3; terreno restrito a CastleGloom(3).

**Veredito: MANTER.** Existe ramo real de risco (Failure com Slowed) e recompensa de XP ao grupo no sucesso; a opcao unica e a propria configuracao do evento-tranca. Nenhum defeito literal detectado.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: "1 unica opcao (PULL AWAY) - sem escolha ... Opcao tem rolagem Might +0, RollLimit 8 - mas sem acao Failure" -> falso quanto ao Failure: a acao Failure existe (RollLimit 1, Slowed).
- parte01: "Efeitos: ouro e XP" -> falso quanto ao ouro: ouro.dar=false; a recompensa medida e XP 0.5 para o grupo.

**Observacoes (sem proposta):**

- O bonus de rolagem Might tem valor 0: o dado de atributo esta declarado sem acrescimo. Registrado como dado, sem proposta.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 29 - Cursed Tome

| campo | valor |
|---|---|
| chave | `resources.assets:2545569` |
| id | `4361a58d-cc5f-4507-a3a6-c4bc74ffaba7` |
| nome_asset | Cursed Tome |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 3 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [3] |
| horario | 1 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=0 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545569 |
| sha256_objeto | `dc037a97c9641685d5c3234ae36217091be6dfbfff712f4f0333168b923b6dd5` |

**Estado real medido.** texto (334 ch); 2 opcoes: "Read" (Success RollLimit 0, sem rolagem, texto de 459 ch, Self -> Cursed 2545493, batalha iniciar=true sem BattleInfo referenciado) e "Leave" (texto "You sense the lurking malevolence within its very essence..." e acao Success sem efeito). disabled=0; Common(0); peso 1.0; minLevel 3; LeadsToFortune=1.

**Veredito: MANTER.** Duas opcoes com texto proprio (inclusive o "Leave", que narra a recusa) e status Cursed aplicado no ramo de risco; sem defeito literal. LeadsToFortune=1 sem item configurado e dado, nao prova de recompensa ausente.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: "Opcao 1 (READ) tem rolagem Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. Nao ha rolagem (rolagem.bonus=[], limite_rolagem=0) nem ramo de falha; o custo e o status Cursed aplicado no proprio sucesso.
- parte01: "Texto de Success presente, curto" -> falso quanto ao tamanho: o texto de sucesso tem 459 caracteres.
- parte01: "Sem texto para REFUSE/CLOSE" -> falso. A opcao "Leave" tem texto de opcao completo.
- parte01: "LeadsToFortune: 1 - mas sem Fortuna visivel nos efeitos (sem item especial)" -> nao se sustenta como defeito: o indicador e de configuracao e itens.dar=false; nao se infere recompensa ausente.

**Observacoes (sem proposta):**

- O nome do asset em jogo e "Dark Tome" (marcacao <incr><indigo><b>Dark Tome</b></indigo></incr> no texto), enquanto o titulo do evento e "Cursed Tome". Observacao de rotulo, sem proposta de alteracao.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 30 - Dark Discoveries

| campo | valor |
|---|---|
| chave | `resources.assets:2545572` |
| id | `385b8352-0189-42e2-905c-ee6b0dae867e` |
| nome_asset | Dark Discoveries |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 3 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [8] |
| horario | 1 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=0 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545572 |
| sha256_objeto | `dd248b24fbb6f799f526d1300e8a2ac673885d00819a5335c376c5bda8f9f532` |

**Estado real medido.** texto (626 ch, fala do Necromante); 2 opcoes: "Accept" (Success RollLimit 0, texto de resultado, Self -> Dark Discoveries 2545510, StatusType Quest(3), "Locate and destroy the runaway experiments.") e "Leave" (Success RollLimit 0, texto de resultado "She nods her head in understanding..."). disabled=0; Common(0); peso 1.0; minLevel 3; terreno restrito a SunkenSwamplands(8).

**Veredito: MANTER.** Decisao pura (sem rolagem) com texto nos dois ramos, inclusive no "Leave"; o evento funciona como contrato de quest via status tipo Quest. Sem defeito literal.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: "Texto de Success para ACCEPT presente, curto. Sem texto para REFUSE" -> falso. A opcao "Leave" tem texto de resultado proprio.
- parte01: "Efeitos de ACCEPT: itens e status" -> falso quanto a itens: itens.dar=false; o efeito e o status de quest.
- parte01: "O REFUSE deveria ter alguma consequencia" -> proposta de design, nao defeito: o ramo de recusa tem narrativa e encerra o evento, com StatusType Quest no aceite documentando o objetivo.

**Observacoes (sem proposta):**

- Nenhuma das 36 opcoes da faixa possui status_requeridos; o evento nao depende de estado previo.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 31 - Dead Adventurer

| campo | valor |
|---|---|
| chave | `resources.assets:2545573` |
| id | `03048d72-af64-4337-8ae9-7475981d36e5` |
| nome_asset | Dead Adventurer |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 1 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | qualquer |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545573 |
| sha256_objeto | `365632d95be00436c835d4aaabdda7de861741c8198f2369c1228ad59815b418` |

**Estado real medido.** texto (54 ch) = "The yearning ghost extends her hand pleading for help."; 2 opcoes: "Reach" (Success RollLimit 0, Self -> Ethereal 2545439, Fortune(1), "Increases Physical Resistance by {10,50}%. Reduces Elemental Resistance by {5,25}%.") e "Leave" (Success, texto "You leave, but the ghost's disappointment haunts your dreams."). disabled=1; Common(0); peso 1.0; minLevel 1; LeadsToFortune=1.

**Veredito: MANTER.** Narrativa curta porem completa nos dois ramos, com status Ethereal no ramo de ajuda. disabled=1 e decisao de configuracao do asset, sem evidencia de defeito nos dados offline; reativacao nao e proposta.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: "1 opcao: REACH - da status [o1a1_status]" -> falso. Sao 2 opcoes: Reach e Leave.
- parte01: "Texto de Success presente, curto" -> correto quanto ao tamanho (54 ch no evento), mas a afirmacao ignora que o texto da opcao Leave e da acao do Leave tambem existem.
- parte01: chave resources.assets:2545412 -> falso. Chave real resources.assets:2545573 (id 03048d72-af64-4337-8ae9-7475981d36e5).

**Observacoes (sem proposta):**

- O texto e as duas opcoes deste asset sao identicos, campo a campo, aos do ordinal 34 "Dwarven Drinking Contest" (sha256 distinto: 365632d9... no 31, 2b0bd974... no 34). Ambos disabled=1: padrao de conteudo provisorio. Achado registrado; nenhuma proposta de texto inventado.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 32 - Desecrated Statue of the First Mountain King

| campo | valor |
|---|---|
| chave | `resources.assets:2545576` |
| id | `31c21c13-d1fb-4be8-9d45-299dbad44e9e` |
| nome_asset | Desecrated Statue of the First Mountain King |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 3 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [9] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=0 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545576 |
| sha256_objeto | `23f9c8d8d8927b82bd66e003ce2effed4778f4e47553242a3914521f956c3023` |

**Estado real medido.** texto (1094 ch, dialogo do Rei Montanha); 2 opcoes: "Accept" (Success RollLimit 0, Self -> Dwarf Rage! 2545511, StatusType Quest(3), statusDescription vazia) e "Loot" (Success RollLimit 0, texto "You pick up the Gold Statue Head thoughtfully...", Self, itens.dar=true, pool Unassigned(2), quantidade_configurada=0, 1 tabela com ItemInfo 2546477 "Gold Statue Head" a 100%, restricoes de tipo/raridade vazias). disabled=0; Common(0); peso 1.0; minLevel 3; terreno restrito a DwarvenHalls(9).

**Veredito: MELHORAR.** A opcao "Loot" promete no texto o item Gold Statue Head e possui tabela de loot com esse item a 100%, mas a quantidade configurada e 0. Esta e a unica proposta desta faixa que altera valor alem de texto, e ela e medida na fonte.

**Propostas:**

1. [PROPOSTA DE CONTEUDO] natureza: quantidade de item incompativel com a narrativa
   - caminho: `$.eventos[32].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.quantidade_configurada`
   - tipo de conferencia: campo integral (antes = valor exato do campo)
   - antes: `0`
   - depois: `1`
   - fundamento: A tabela de loot da propria opcao aponta para ItemInfo 2546477 "Gold Statue Head" (Rarity 3, FixedSellPrice 5000, descricao opcional "The Golden Head of the Mountain King.") com Chance 100.0, e o texto da opcao entrega explicitamente o item; com quantidade_configurada=0 nao ha unidade a conceder. Valor de destino 1 alinha configuracao e narrativa. O campo original equivalente e itemCount=0 em campos_originais.
2. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: ortografia (confusao bares/bears)
   - caminho: `$.eventos[32].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `It bares the telltale signs of looting`
   - depois: `It bears the telltale signs of looting`
   - fundamento: Mesmo defeito dos ordinais 26 e 27.
3. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: espaco duplo no texto de resultado
   - caminho: `$.eventos[32].opcoes[1].efeitos[0].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `"Oh, You wouldn't  dare!"`
   - depois: `"Oh, You wouldn't dare!"`
   - fundamento: Dois espacos entre "wouldn't" e "dare"; correcao cosmetica do literal.

**Refutacoes a parte01:**

- parte01: titulo "EVT 32: Desecrated Statue of the First Mountain King" esta correto, mas a chave resources.assets:2545413 e falsa (real: 2545576, id 31c21c13-d1fb-4be8-9d45-299dbad44e9e).
- parte01: "2 opcoes: ACCEPT e DECLINE" -> falso. A segunda opcao e "Loot".
- parte01: "Aceitar gera um quest/objetivo (ajudar o Rei Montanha)" -> correto: o aceite entrega o status tipo Quest "Dwarf Rage!" (2545511).
- parte01: "Nenhuma opcao tem rolagem (RollLimit 0, bonus: [])" -> correto para este evento, mas generalizado indevidamente no resumo da proposta.

**Observacoes (sem proposta):**

- O status Dwarf Rage! (2545511) tem statusDescription vazia na fonte: registrado como ausencia de descricao, sem inferir efeito.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 33 - Disturbing Diner

| campo | valor |
|---|---|
| chave | `resources.assets:2545577` |
| id | `06f45978-e4ec-44bf-b216-cd3c84686572` |
| nome_asset | Disturbing Diner |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [3, 8] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545577 |
| sha256_objeto | `8e803f5d3d720c229dd6534562419f95def8db73f92af0ba1cae62f2ec6f8401` |

**Estado real medido.** texto (916 ch); texto_resultados_possiveis (76 ch) = "The man remains silent, watching with disturbing patience for you to choose."; 3 opcoes, todas Success com RollLimit 0 e XP dar=true razao 0.5: "Crusty Cockroach" (rolagem Vitality+2 -> Well Fed: Stats 2545403, "Stats increased by 10%."), "Hand Soup" (rolagem Reflex+4 -> Well Fed: Treasure 2545404, "Increases item drops and gold gained by 50%.") e "Twitching Tentacle" (rolagem Dexterity+1 -> Well Fed:  Experience 2545402, "Experience gained increased by 50%."). disabled=0; Common(0); peso 1.0; minLevel 1; terrenos CastleGloom(3) e SunkenSwamplands(8).

**Veredito: MANTER.** Tres opcoes distintas, cada uma com status proprio e XP 0.5; limiar 0 em todas significa sucesso automatico, eliminando a necessidade de ramo de falha. Os bonus de rolagem presentes sao inertes nesse desenho - dado documentado, sem alteracao proposta.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: "Cada opcao tem rolagem com Vitality +2, RollLimit 0" -> impreciso: cada opcao tem atributo de rolagem proprio (Vitality+2, Reflex+4, Dexterity+1); apenas o limiar 0 e comum.
- parte01: "Sem Failure em nenhuma opcao ... ambiguidade de rolagem" -> substituido pelo dado: com RollLimit 0 nas tres acoes, nenhuma falha e alcancavel; os tres resultados sao positivos e distintos.
- parte01: "Manter as 3 opcoes" -> correto, e a manutencao e o veredito deste cartao.

**Observacoes (sem proposta):**

- os textos das opcoes 1 e 2 terminam com espaco: cosmetico, registrado em Analise A, sem proposta.

**Referencias NULL do evento: 39 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 34 - Dwarven Drinking Contest

| campo | valor |
|---|---|
| chave | `resources.assets:2545578` |
| id | `5777d2ca-8fca-485d-92c8-239f6da0e8a4` |
| nome_asset | Dwarven Drinking Contest |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 1 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | qualquer |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545578 |
| sha256_objeto | `2b0bd974e88e2dd3afa68c1a08a9bd0b9930726abab25a5693944d57368229e0` |

**Estado real medido.** titulo "Dwarven Drinking Contest"; texto (54 ch) identico ao do ordinal 31 ("The yearning ghost extends her hand pleading for help."); 2 opcoes "Reach" e "Leave" identicas em titulo, texto e efeitos (Ethereal 2545439). disabled=1; Common(0); peso 1.0; minLevel 1; LeadsToFortune=1. sha256_objeto 2b0bd974... (distinto do 31).

**Veredito: MANTER.** Asset desabilitado cujo conteudo e copia literal do ordinal 31. Nao ha narrativa propria para corrigir, e inventar texto para um slot disabled nao e proposta defensavel; o achado fica documentado para decisao do dono.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: titulo "EVT 34: Disturbing Statue" -> falso. O ordinal 34 e "Dwarven Drinking Contest" (resources.assets:2545578, id 5777d2ca-8fca-485d-92c8-239f6da0e8a4).
- parte01: "2 opcoes: CRAFT e IGNORE ... forja item com atributo bonus" -> falso. As opcoes sao Reach e Leave (status Ethereal).
- parte01: "Opcao 1 (CRAFT) tem rolagem Intelligence +3, RollLimit 10" -> falso. Nao ha rolagem neste asset.

**Observacoes (sem proposta):**

- Achado de curadoria: o asset "Dwarven Drinking Contest" carrega o mesmo conteudo do "Dead Adventurer" (texto, opcoes e efeitos identicos). Ambos disabled=1. Registrado para o dono decidir se havera conteudo proprio; nenhuma alteracao proposta neste lote.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 35 - Dwarven Sentry Wall

| campo | valor |
|---|---|
| chave | `resources.assets:2545579` |
| id | `7b6c58f0-2671-429e-9807-780a7695d9d8` |
| nome_asset | Dwarven Sentry Wall |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [4, 9] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545579 |
| sha256_objeto | `0da4075b0819d99283d1d07a5f042453636e05576af93d244d5be7a6419060c3` |

**Estado real medido.** texto (395 ch); 1 opcao "Act" com rolagem Intel+3 (rollBonusTypes [3]); acao Success (RollLimit 10) -> XP dar=true razao 1.0 alvo Party (OverrideTargetType 1 / TargetOverride 2) com texto de resultado; acao Failure (RollLimit 1) -> percentMaxHealth=-30.0 alvo Party e Self -> Severely Burned 2545499 ("Reduces Fire Resistance by 25% per stack"). disabled=0; Common(0); peso 1.0; minLevel 1; terrenos ForgottenMines(4) e DwarvenHalls(9).

**Veredito: MELHORAR.** Rolagem com limiar 10 e ramo de falha real com efeitos mensuraveis; a unica alteracao defensavel e a correcao ortografica do texto original.

**Propostas:**

1. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: ortografia (quitely/quietly)
   - caminho: `$.eventos[35].opcoes[0].efeitos[0].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `The dwarven sentry quitely apologizes and allows you safe passage.`
   - depois: `The dwarven sentry quietly apologizes and allows you safe passage.`
   - fundamento: O adverbio ingles e "quietly"; "quitely" nao existe. Correcao pontual no texto de resultado da acao Success.

**Refutacoes a parte01:**

- parte01: "1 unica opcao (ACT) - sem escolha" -> correto quanto ao numero de opcoes, mas a conclusao de defeito nao se sustenta: existe ramo de risco interno (Success/Failure).
- parte01: "Opcao tem rolagem Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. A acao Failure existe (RollLimit 1) e aplica -30% de vida maxima ao grupo e o status Severely Burned.
- parte01: "Efeitos: XP e itens" -> falso quanto a itens: itens.dar=false; os efeitos medidos sao XP 1.0 para o grupo no sucesso e debuff no fracasso.

**Observacoes (sem proposta):**

- O ramo de falha afeta o grupo inteiro (alvo Party), nao apenas o personagem que age; dado medido em campos_originais (OverrideTargetType=1, TargetTypeOverride=2).

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 36 - Dwarven Tomb

| campo | valor |
|---|---|
| chave | `resources.assets:2545580` |
| id | `534013a8-7402-4b00-95aa-dbd337d35ccf` |
| nome_asset | Dwarven Tomb |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [9, 4] |
| horario | 1 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545580 |
| sha256_objeto | `c5d450791f03749a83b90d1a555ee1ba3f26a47d691d84edc17454110f294a9c` |

**Estado real medido.** texto (385 ch); texto_resultados_possiveis = "What will you do?"; 2 opcoes: "Loot" com rolagem Might (rollBonusTypes [0], valor 0), Success (RollLimit 16) -> Self -> Horn of Devotion 2545448 (Fortune(1), durationType Permanent(3), "Increases the effect of Shrines by {50,100}%.") e Failure (RollLimit 1) -> Self -> Weakened 2545504 ("Reduces Might by 20% per stack"); e "Pay Respect" (Success RollLimit 0) -> Self -> Horn of Devotion. disabled=0; Common(0); peso 1.0; minLevel 1; LeadsToFortune=1; terrenos DwarvenHalls(9) e ForgottenMines(4).

**Veredito: MELHORAR.** Duas opcoes com desfechos diferentes (risco com rolagem versus reverencia sem risco) e recompensa comum de status permanente; a alteracao defensavel e uma correcao ortografica no texto de falha.

**Propostas:**

1. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: ortografia (its/it's)
   - caminho: `$.eventos[36].opcoes[0].efeitos[1].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `but its of no use.`
   - depois: `but it's of no use.`
   - fundamento: A contraccao de "it is" exige apostrofo; "its" e possessivo. Correcao pontual no texto de falha da opcao Loot.

**Refutacoes a parte01:**

- parte01: "Opcao 1 (LOOT) tem rolagem Might +0, RollLimit 16 - mas sem acao Failure" -> falso. A acao Failure existe (RollLimit 1, Weakened).
- parte01: "2 opcoes: LOOT e LEAVE" -> impreciso. A segunda opcao e "Pay Respect".
- parte01: "LeadsToFortune: 1 - da item especial no Success" -> falso quanto a item: Horn of Devotion e um EventStatus (Fortune, permanente), nao um item; itens.dar=false.

**Observacoes (sem proposta):**

- A recompensa das duas opcoes e o mesmo status; a diferenca e o risco da rolagem (limiar 16) versus a ausencia de rolagem em "Pay Respect". Dado medido, sem alteracao proposta.

**Referencias NULL do evento: 39 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 37 - Dwarven Tribute

| campo | valor |
|---|---|
| chave | `resources.assets:2545581` |
| id | `7022fe7d-f9fb-4407-82ef-4e10f5d45d68` |
| nome_asset | Dwarven Tribute |
| categoria | Normal |
| raridade | Legendary(3) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | Both / None |
| minLevel | 4 |
| node types | [3] (allowOnAllNodeTypes=0) |
| terreno | qualquer (allowOnAllTerrainTypes=1), exceto: [4] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=0 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545581 |
| sha256_objeto | `b88d63eee2976eda19a68254723c59bd4862cf8973abedfabac9b4e4b935b5d3` |

**Estado real medido.** texto = "" (cadeia vazia); texto_resultados_possiveis = ""; 1 opcao "Open" com texto "" e acao Success com texto ""; efeito: Self, itens.dar=true, itemPoolType None(0), quantidade_configurada=1, 1 tabela com 10 entradas do mesmo ItemInfo 2546793 "Gold Bar" (Rarity 3, FixedSellPrice 2500) a Chance 100.0; ouro dar=false com razao 0.0; XP dar=false razao 1.0. disabled=0; Legendary(3); peso 1.0; minLevel 4; StorySetting Both(2); allowAtAllLevels=0.

**Veredito: MELHORAR.** Vazio narrativo nos tres niveis (evento, opcao e resultado) no unico evento Legendary da faixa, cuja recompensa e um item fixo e verificavel. Correcao proposta em ingles, com conteudo ancorado no item concedido.

**Propostas:**

1. [PROPOSTA DE CONTEUDO] natureza: narrativa principal ausente
   - caminho: `$.eventos[37].texto`
   - tipo de conferencia: campo integral (antes = valor exato do campo)
   - antes: ``
   - depois: `A low stone altar stands at the end of the hall, its surface swept clean of dust. On it rests an ironbound chest, and beside it a dwarven plaque reads: "What is given is given back."`
   - fundamento: O evento Legendary entrega exatamente um Gold Bar; a proposta descreve a cena (altar, arca, placa) sem criar mecanica, condicao ou valor novo. Texto em ingles para preservar o idioma da fonte.
2. [PROPOSTA DE CONTEUDO] natureza: texto da opcao vazio
   - caminho: `$.eventos[37].opcoes[0].texto`
   - tipo de conferencia: campo integral (antes = valor exato do campo)
   - antes: ``
   - depois: `Open the tribute chest.`
   - fundamento: A opcao chama-se "Open" e nao tem descricao; a proposta nomeia a acao exatamente como ela e configurada (abrir a arca).
3. [PROPOSTA DE CONTEUDO] natureza: texto de resultado da acao ausente
   - caminho: `$.eventos[37].opcoes[0].efeitos[0].texto`
   - tipo de conferencia: campo integral (antes = valor exato do campo)
   - antes: ``
   - depois: `The lid swings open without a sound. Inside, resting on a bed of dust, lies a single bar of gold - the tribute, returned.`
   - fundamento: O unico efeito configurado e conceder 1 Gold Bar ao Self; a proposta narra esse resultado sem acrescentar alvo, quantidade ou condicao.

**Refutacoes a parte01:**

- parte01: "EVT 37: Dwarven Tribute ... RARIDADE: Common (0)" -> falso. A raridade e Legendary(3).
- parte01: "1 unica opcao (PAY)" -> falso. A opcao chama-se "Open".
- parte01: "Opcao tem rolagem Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. Nao ha rolagem (rolagem.bonus=[], limite_rolagem=0).
- parte01: "Efeito: da item ao anao, recebe ouro de volta" -> falso. O efeito medido e conceder 1 Gold Bar ao proprio grupo, com ouro.dar=false (razao 0.0).
- parte01: chave resources.assets:2545418 -> falso. Chave real resources.assets:2545581 (id 7022fe7d-f9fb-4407-82ef-4e10f5d45d68).

**Observacoes (sem proposta):**

- As 10 entradas da tabela apontam todas para o mesmo ItemInfo, com Chance 100.0: a recompensa e deterministica na configuracao (1 Gold Bar). O sorteio final em partida permanece NAO_EXERCITADO.

**Referencias NULL do evento: 13 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 38 - Edwin's Demise

| campo | valor |
|---|---|
| chave | `resources.assets:2545582` |
| id | `4af726e7-657e-403a-883b-e3221fdd700c` |
| nome_asset | Edwin's Demise |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [0, 3, 9] |
| horario | 1 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 1 / 0 / 0 |
| origem | `resources.assets` path_id 2545582 |
| sha256_objeto | `4323c60557614e358cbca64276e6c899c4b7854a34fb0381d4d17a5162d70901` |

**Estado real medido.** texto (1266 ch, pagina do grimorio de Edwin); 2 opcoes: "Cast" com rolagem Intel+3 (rollBonusTypes [3]), Success (RollLimit 12) -> Self -> Edwin's Enchantment 2545429 (Fortune(1), durationType Permanent(3), "Power for mana use increased by {25,50}%. Mana costs are now paid in Health instead.") e Failure (RollLimit 1) -> percentMaxHealth=-30.0 Self -> Confused 2545491 ("Reduces Intelligence by 20% per stack"); e "Leave" (texto "You think better of fleeting fame."). disabled=0; Common(0); peso 1.0; minLevel 1; LeadsToFortune=1.

**Veredito: MELHORAR.** Rolagem com limiar 12, ramo de falha com dano e status, e recompensa permanente no sucesso. Tres defeitos literais medidos no texto original, todos corrigiveis sem tocar mecanica.

**Propostas:**

1. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: espaco inicial no texto original
   - caminho: `$.eventos[38].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: ` On a worn table lays a spellbook`
   - depois: `On a worn table lays a spellbook`
   - fundamento: O texto comeca com um espaco antes de "On"; correcao de espaco inicial.
2. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: ortografia (Infact/In fact)
   - caminho: `$.eventos[38].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `Infact, only a fool`
   - depois: `In fact, only a fool`
   - fundamento: "Infact" nao e palavra em ingles; a locucao correta e "In fact".
3. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: pontuacao (ponto duplo)
   - caminho: `$.eventos[38].opcoes[0].efeitos[0].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `to fuel [his] magic..`
   - depois: `to fuel [his] magic.`
   - fundamento: O texto de sucesso termina com dois pontos finais; correcao de pontuacao no fecho da frase.

**Refutacoes a parte01:**

- parte01: titulo "EVT 38: Dwarven Forge" -> falso. O ordinal 38 e "Edwin's Demise" (resources.assets:2545582, id 4af726e7-657e-403a-883b-e3221fdd700c).
- parte01: "2 opcoes: FORGE e BUY ... ambas com rolagem Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. As opcoes sao Cast e Leave; o limiar e 12 e existe acao Failure (RollLimit 1).
- parte01: "Ambas dao itens de forja (diferentes raridades/precos)" -> falso. Nao ha recompensa de item; os efeitos sao status permanente no sucesso e dano + Confused no fracasso.

**Observacoes (sem proposta):**

- O status Edwin's Enchantment tem duracao Permanent(3): recompensa persistente no sucesso, com descricao que explicita o custo (mana paga em vida).

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 39 - Elder Tree

| campo | valor |
|---|---|
| chave | `resources.assets:2545583` |
| id | `2779cca5-013a-4bbc-ba32-e7d25ef7c8b7` |
| nome_asset | Elder Tree |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | [2] |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545583 |
| sha256_objeto | `7726757770037320fd782091ff9422fa4b42c91fb292e1668b7529300a6978c1` |

**Estado real medido.** texto (840 ch) com dupla introducao: paragrafo 1 inicia "A massive <green><b><incr>Elder Tree</incr></b></green> grows here..." e paragrafo 3 inicia "You stumble upon an entity as old as time itself: the <green><b><incr>Elder Tree</incr></b></green>."; 2 opcoes: "Rest" (Success RollLimit 0, Self, percentMaxHealth=100.0 e percentMaxMana=100.0, texto de resultado presente) e "Eat" (Success RollLimit 0, Self, XP dar=true razao 2.0). disabled=0; Common(0); peso 1.0; minLevel 1; allowAtAllLevels=1; LeadsToFortune=0; terreno restrito a FreewindForest(2).

**Veredito: MELHORAR.** Narrativa rica (840 ch), mas com duas aberturas consecutivas para a mesma arvore, a segunda repetindo o proprio nome. Duas escolhas com efeitos distintos. Correcoes propostas sao de edicao de texto.

**Propostas:**

1. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: narrativa duplicada (dois inicios)
   - caminho: `$.eventos[39].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: `A massive <green><b><incr>Elder Tree</incr></b></green> grows here. Its giant body formed not only of wood but of living stone and ore. All around it life seems to flourish as if it were the very heart of the forest.\n\nYou stumble upon an entity as old as time itself: the `
   - depois: `A massive <green><b><incr>Elder Tree</incr></b></green> grows here. Its giant body formed not only of wood but of living stone and ore. All around it life seems to flourish as if it were the very heart of the forest.\n\nIt stands regal and magnificent, its massive trunk adorned with the etchings of time, its gnarled boughs stretching out like the arms of a benevolent giant.`
   - fundamento: O trecho removido ("You stumble upon an entity as old as time itself: the ") repete a mesma apresentacao e reapresenta o nome da arvore logo apos o primeiro paragrafo; a remocao mantem a frase seguinte intacta.
2. [SUGESTAO DE CORRECAO DO ORIGINAL] natureza: espaco inicial no texto da opcao
   - caminho: `$.eventos[39].opcoes[0].texto`
   - tipo de conferencia: trecho literal (antes = substring exata do campo)
   - antes: ` Enjoy the tranquility the Elder Tree brings.`
   - depois: `Enjoy the tranquility the Elder Tree brings.`
   - fundamento: Correcao de espaco inicial no texto da opcao "Rest".

**Refutacoes a parte01:**

- parte01: titulo "EVT 39: Dwarven Market" -> falso. O ordinal 39 e "Elder Tree" (resources.assets:2545583, id 2779cca5-013a-4bbc-ba32-e7d25ef7c8b7).
- parte01: "3 opcoes: BUY, SELL, LEAVE" -> falso. Sao 2 opcoes: Rest e Eat.
- parte01: "EVT 39 marcado com LeadsToFortune: 1 mas sem Fortuna visivel" -> falso. LeadsToFortune do ordinal 39 e 0.

**Observacoes (sem proposta):**

- A opcao "Rest" concede 100% de vida e mana maximas, o maior valor de cura da faixa, sem rolagem; a opcao "Eat" concede XP com razao 2.0 ao Self. Valores medidos.

**Referencias NULL do evento: 26 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

### 40 - Enchanted Axe

| campo | valor |
|---|---|
| chave | `resources.assets:2545584` |
| id | `b0370015-64ef-4d3c-ac98-d2468992d12d` |
| nome_asset | Enchanted Axe |
| categoria | Normal |
| raridade | Common(0) |
| peso | 1.0 |
| pool | Normal |
| disabled | 0 |
| modos | Campaign, Roguelike |
| historia / full_release | NonStoryOnly / None |
| minLevel | 1 |
| node types | [7] (allowOnAllNodeTypes=0) |
| terreno | qualquer |
| horario | 0 (allowAtAllTimesOfDay=1) |
| niveis | allowAtAllLevels=1 |
| LeadsToFortune / isLesserEvent / KeepInDeckWhenUsed | 0 / 0 / 0 |
| origem | `resources.assets` path_id 2545584 |
| sha256_objeto | `02ba72eb1c8f3afcc4ddcb944a38805c814421ba45b0b8b8669b61f90e175cfb` |

**Estado real medido.** texto (283 ch); texto_resultados_possiveis (38 ch) = "Who will attempt to disrupt the magic?"; 1 opcao "Disrupt" com rolagem Dexterity+1 (rollBonusTypes [1]); Success (RollLimit 10) -> XP dar=true razao 1.0 alvo Party (OverrideTargetType 1 / TargetOverride 2); Failure (RollLimit 1) com dois efeitos: Party sem recompensa e Self com percentMaxHealth=-20.0 -> Mortally Wounded 2545497 ("Reduces Healing Received by 25% per stack"). disabled=0; Common(0); peso 1.0; minLevel 1; allowOnAllTerrainTypes=1 sem excecoes.

**Veredito: MANTER.** Narrativa presente (283 ch), prompt de selecao presente, rolagem com limiar 10 e ramo de falha com efeitos reais. A opcao unica e a configuracao do evento-sentinela; nenhum defeito literal detectado.

**Propostas:** nenhuma. Veredito MANTER conforme justificativa acima.

**Refutacoes a parte01:**

- parte01: "1 unica opcao (DISRUPT) - sem escolha" -> correto quanto ao numero de opcoes; a conclusao de defeito nao se sustenta porque existe ramo interno de risco.
- parte01: "Opcao tem rolagem Dexterity +1, RollLimit 10 - mas sem acao Failure" -> falso. A acao Failure existe (RollLimit 1) e aplica -20% de vida maxima e o status Mortally Wounded.
- parte01: "Efeito: XP e ouro" -> falso quanto ao ouro: ouro.dar=false; a recompensa medida e XP 1.0 para o grupo.

**Observacoes (sem proposta):**

- O ramo de falha tem dois efeitos distintos (Party sem recompensa e Self com debuff), sendo o unique da faixa com essa composicao. Dado medido.

**Referencias NULL do evento: 34 caminhos.**

| classe de NULL | caminho de exemplo |
|---|---|
| `$.opcoes[*].efeitos[*].batalha.dados_recompensa_final` | `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final` |
| `$.opcoes[*].efeitos[*].batalha.referencia.chave` | `$.opcoes[0].efeitos[0].batalha.referencia.chave` |
| `$.opcoes[*].efeitos[*].batalha.referencia.nome` | `$.opcoes[0].efeitos[0].batalha.referencia.nome` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.experiencia.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.itens.sorteio_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.ouro.quantidade_final` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final` |
| `$.opcoes[*].efeitos[*].efeitos[*].recompensas.status.resultado_sorteado` | `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado` |
| `$.opcoes[*].efeitos[*].evento_encadeado.chave` | `$.opcoes[0].efeitos[0].evento_encadeado.chave` |
| `$.opcoes[*].efeitos[*].evento_encadeado.nome` | `$.opcoes[0].efeitos[0].evento_encadeado.nome` |
| `$.opcoes[*].recompensas[*].padrao[*].experiencia.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].itens.sorteio_final` | `$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[*].ouro.quantidade_final` | `$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[*].status.resultado_sorteado` | `$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado` |
| `$.opcoes[*].recompensas[*].padrao[1].experiencia.quantidade_final` | `$.opcoes[0].recompensas[1].padrao[1].experiencia.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[1].itens.sorteio_final` | `$.opcoes[0].recompensas[1].padrao[1].itens.sorteio_final` |
| `$.opcoes[*].recompensas[*].padrao[1].ouro.quantidade_final` | `$.opcoes[0].recompensas[1].padrao[1].ouro.quantidade_final` |
| `$.opcoes[*].recompensas[*].padrao[1].status.resultado_sorteado` | `$.opcoes[0].recompensas[1].padrao[1].status.resultado_sorteado` |

Motivo comum registrado na fonte para essas entradas: *referencia nula, resultado dependente de runtime ou
valor nulo do leitor; veja motivo no objeto conteiner e campos_originais*. Nenhuma dessas entradas e
interpretada como zero, como recompensa ausente ou como falha de implantacao. O inventario completo,
caminho a caminho, esta na Analise B.

---

## 5. Analise A - inventario de literais do texto ingles

Todas as propostas rotuladas SUGESTAO DE CORRECAO DO ORIGINAL, com o caminho exato, o literal de origem e o
literal corrigido. Nenhuma delas foi aplicada a fonte.

| # | ordinal | natureza | caminho | antes | depois |
|---|---|---|---|---|---|
| 1 | 22 | ortografia (artigo indefinido) | `$.eventos[22].texto` | `the strength of a ogre!` | `the strength of an ogre!` |
| 2 | 26 | ortografia (confusao bares/bears) | `$.eventos[26].texto` | `warped and decayed, bares the weight of forgotten sorrows` | `warped and decayed, bears the weight of forgotten sorrows` |
| 3 | 27 | ortografia (confusao bares/bears) | `$.eventos[27].texto` | `warped and decayed, bares the weight of forgotten sorrows` | `warped and decayed, bears the weight of forgotten sorrows` |
| 4 | 32 | ortografia (confusao bares/bears) | `$.eventos[32].texto` | `It bares the telltale signs of looting` | `It bears the telltale signs of looting` |
| 5 | 32 | espaco duplo no texto de resultado | `$.eventos[32].opcoes[1].efeitos[0].texto` | `"Oh, You wouldn't  dare!"` | `"Oh, You wouldn't dare!"` |
| 6 | 35 | ortografia (quitely/quietly) | `$.eventos[35].opcoes[0].efeitos[0].texto` | `The dwarven sentry quitely apologizes and allows you safe passage.` | `The dwarven sentry quietly apologizes and allows you safe passage.` |
| 7 | 36 | ortografia (its/it's) | `$.eventos[36].opcoes[0].efeitos[1].texto` | `but its of no use.` | `but it's of no use.` |
| 8 | 38 | espaco inicial no texto original | `$.eventos[38].texto` | ` On a worn table lays a spellbook` | `On a worn table lays a spellbook` |
| 9 | 38 | ortografia (Infact/In fact) | `$.eventos[38].texto` | `Infact, only a fool` | `In fact, only a fool` |
| 10 | 38 | pontuacao (ponto duplo) | `$.eventos[38].opcoes[0].efeitos[0].texto` | `to fuel [his] magic..` | `to fuel [his] magic.` |
| 11 | 39 | narrativa duplicada (dois inicios) | `$.eventos[39].texto` | `A massive <green><b><incr>Elder Tree</incr></b></green> grows here. Its giant body formed not only of wood but of living stone and ore. All around it life seems to flourish as if it were the very heart of the forest.\n\nYou stumble upon an entity as old as time itself: the ` | `A massive <green><b><incr>Elder Tree</incr></b></green> grows here. Its giant body formed not only of wood but of living stone and ore. All around it life seems to flourish as if it were the very heart of the forest.\n\nIt stands regal and magnificent, its massive trunk adorned with the etchings of time, its gnarled boughs stretching out like the arms of a benevolent giant.` |
| 12 | 39 | espaco inicial no texto da opcao | `$.eventos[39].opcoes[0].texto` | ` Enjoy the tranquility the Elder Tree brings.` | `Enjoy the tranquility the Elder Tree brings.` |

Itens cosmeticos medidos que **nao** geram proposta (registro por transparencia):

| ordinal | caminho | achado |
|---|---|---|
| 21 | `$.eventos[21].texto` | espaco duplo em `"Go on!  Come at me` |
| 22 | `$.eventos[22].opcoes[0].efeitos[0].texto` | espaco final depois de `fuzzy." ` |
| 33 | `$.eventos[33].opcoes[0].texto`, `$.eventos[33].opcoes[1].texto` | espaco final nos dois textos |
| 33 | status `Well Fed:  Experience` (2545402) | nome com espaco duplo no catalogo, nao no evento |

---

## 6. Analise B - inventario NULL completo

Total de entradas em `ausencias` para os 20 eventos: **492**.

| ordinal | eventos | caminhos NULL |
|---|---|---|
| 21 | Boss Fight - Roland | 22 |
| 22 | Brawler's Brew | 13 |
| 23 | Carved Monolith | 26 |
| 24 | Carved Rune | 13 |
| 25 | Challenger's Gong | 26 |
| 26 | Cursed Chest | 22 |
| 27 | Cursed Chest | 11 |
| 28 | Cursed Clock | 26 |
| 29 | Cursed Tome | 26 |
| 30 | Dark Discoveries | 26 |
| 31 | Dead Adventurer | 26 |
| 32 | Desecrated Statue of the First Mountain King | 26 |
| 33 | Disturbing Diner | 39 |
| 34 | Dwarven Drinking Contest | 26 |
| 35 | Dwarven Sentry Wall | 26 |
| 36 | Dwarven Tomb | 39 |
| 37 | Dwarven Tribute | 13 |
| 38 | Edwin's Demise | 26 |
| 39 | Elder Tree | 26 |
| 40 | Enchanted Axe | 34 |

### B.21 - Boss Fight - Roland (22 caminhos NULL)

- `$.eventos[21].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[21].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[21].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[21].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[21].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[21].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[21].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[21].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[21].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[21].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[21].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[21].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[21].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[21].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[21].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[21].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[21].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[21].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[21].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[21].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[21].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[21].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.22 - Brawler's Brew (13 caminhos NULL)

- `$.eventos[22].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[22].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[22].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[22].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[22].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[22].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[22].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[22].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[22].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[22].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[22].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[22].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[22].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`

### B.23 - Carved Monolith (26 caminhos NULL)

- `$.eventos[23].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[23].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[23].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[23].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[23].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[23].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[23].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[23].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[23].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[23].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[23].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[23].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[23].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[23].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[23].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[23].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[23].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[23].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[23].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[23].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[23].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[23].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[23].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[23].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[23].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[23].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.24 - Carved Rune (13 caminhos NULL)

- `$.eventos[24].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[24].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[24].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[24].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[24].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[24].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[24].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[24].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[24].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[24].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[24].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[24].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[24].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`

### B.25 - Challenger's Gong (26 caminhos NULL)

- `$.eventos[25].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[25].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[25].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[25].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[25].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[25].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[25].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[25].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[25].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[25].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[25].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[25].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[25].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[25].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[25].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[25].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[25].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[25].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[25].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[25].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[25].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[25].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[25].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[25].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[25].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[25].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.26 - Cursed Chest (22 caminhos NULL)

- `$.eventos[26].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[26].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[26].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[26].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[26].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[26].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[26].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[26].opcoes[0].efeitos[1].batalha.dados_recompensa_final`
- `$.eventos[26].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[26].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[26].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[26].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[26].opcoes[0].efeitos[1].evento_encadeado.chave`
- `$.eventos[26].opcoes[0].efeitos[1].evento_encadeado.nome`
- `$.eventos[26].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[26].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[26].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[26].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[26].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final`
- `$.eventos[26].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final`
- `$.eventos[26].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final`
- `$.eventos[26].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado`

### B.27 - Cursed Chest (11 caminhos NULL)

- `$.eventos[27].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[27].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[27].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[27].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[27].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[27].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[27].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[27].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[27].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[27].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[27].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`

### B.28 - Cursed Clock (26 caminhos NULL)

- `$.eventos[28].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[28].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[28].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[28].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[28].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[28].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[28].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[28].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[28].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[28].opcoes[0].efeitos[1].batalha.dados_recompensa_final`
- `$.eventos[28].opcoes[0].efeitos[1].batalha.referencia.chave`
- `$.eventos[28].opcoes[0].efeitos[1].batalha.referencia.nome`
- `$.eventos[28].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[28].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[28].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[28].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[28].opcoes[0].efeitos[1].evento_encadeado.chave`
- `$.eventos[28].opcoes[0].efeitos[1].evento_encadeado.nome`
- `$.eventos[28].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[28].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[28].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[28].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[28].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final`
- `$.eventos[28].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final`
- `$.eventos[28].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final`
- `$.eventos[28].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado`

### B.29 - Cursed Tome (26 caminhos NULL)

- `$.eventos[29].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[29].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[29].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[29].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[29].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[29].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[29].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[29].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[29].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[29].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[29].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[29].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[29].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[29].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[29].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[29].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[29].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[29].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[29].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[29].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[29].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[29].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[29].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[29].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[29].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[29].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.30 - Dark Discoveries (26 caminhos NULL)

- `$.eventos[30].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[30].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[30].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[30].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[30].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[30].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[30].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[30].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[30].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[30].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[30].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[30].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[30].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[30].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[30].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[30].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[30].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[30].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[30].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[30].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[30].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[30].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[30].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[30].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[30].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[30].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.31 - Dead Adventurer (26 caminhos NULL)

- `$.eventos[31].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[31].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[31].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[31].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[31].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[31].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[31].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[31].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[31].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[31].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[31].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[31].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[31].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[31].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[31].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[31].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[31].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[31].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[31].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[31].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[31].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[31].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[31].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[31].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[31].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[31].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.32 - Desecrated Statue of the First Mountain King (26 caminhos NULL)

- `$.eventos[32].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[32].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[32].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[32].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[32].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[32].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[32].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[32].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[32].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[32].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[32].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[32].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[32].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[32].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[32].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[32].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[32].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[32].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[32].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[32].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[32].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[32].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[32].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[32].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[32].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[32].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.33 - Disturbing Diner (39 caminhos NULL)

- `$.eventos[33].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[33].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[33].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[33].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[33].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[33].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[33].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[33].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[33].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[33].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[33].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[33].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[33].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[33].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[33].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[33].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[33].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[33].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[33].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[33].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[33].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[33].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[33].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[33].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[33].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[33].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[33].opcoes[2].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[33].opcoes[2].efeitos[0].batalha.referencia.chave`
- `$.eventos[33].opcoes[2].efeitos[0].batalha.referencia.nome`
- `$.eventos[33].opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[33].opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[33].opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[33].opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[33].opcoes[2].efeitos[0].evento_encadeado.chave`
- `$.eventos[33].opcoes[2].efeitos[0].evento_encadeado.nome`
- `$.eventos[33].opcoes[2].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[33].opcoes[2].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[33].opcoes[2].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[33].opcoes[2].recompensas[0].padrao[0].status.resultado_sorteado`

### B.34 - Dwarven Drinking Contest (26 caminhos NULL)

- `$.eventos[34].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[34].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[34].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[34].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[34].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[34].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[34].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[34].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[34].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[34].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[34].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[34].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[34].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[34].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[34].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[34].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[34].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[34].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[34].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[34].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[34].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[34].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[34].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[34].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[34].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[34].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.35 - Dwarven Sentry Wall (26 caminhos NULL)

- `$.eventos[35].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[35].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[35].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[35].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[35].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[35].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[35].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[35].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[35].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[35].opcoes[0].efeitos[1].batalha.dados_recompensa_final`
- `$.eventos[35].opcoes[0].efeitos[1].batalha.referencia.chave`
- `$.eventos[35].opcoes[0].efeitos[1].batalha.referencia.nome`
- `$.eventos[35].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[35].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[35].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[35].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[35].opcoes[0].efeitos[1].evento_encadeado.chave`
- `$.eventos[35].opcoes[0].efeitos[1].evento_encadeado.nome`
- `$.eventos[35].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[35].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[35].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[35].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[35].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final`
- `$.eventos[35].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final`
- `$.eventos[35].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final`
- `$.eventos[35].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado`

### B.36 - Dwarven Tomb (39 caminhos NULL)

- `$.eventos[36].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[36].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[36].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[36].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[36].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[36].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[36].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[36].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[36].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[36].opcoes[0].efeitos[1].batalha.dados_recompensa_final`
- `$.eventos[36].opcoes[0].efeitos[1].batalha.referencia.chave`
- `$.eventos[36].opcoes[0].efeitos[1].batalha.referencia.nome`
- `$.eventos[36].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[36].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[36].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[36].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[36].opcoes[0].efeitos[1].evento_encadeado.chave`
- `$.eventos[36].opcoes[0].efeitos[1].evento_encadeado.nome`
- `$.eventos[36].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[36].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[36].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[36].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[36].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final`
- `$.eventos[36].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final`
- `$.eventos[36].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final`
- `$.eventos[36].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado`
- `$.eventos[36].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[36].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[36].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[36].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[36].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[36].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[36].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[36].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[36].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[36].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[36].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[36].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[36].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.37 - Dwarven Tribute (13 caminhos NULL)

- `$.eventos[37].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[37].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[37].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[37].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[37].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[37].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[37].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[37].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[37].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[37].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[37].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[37].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[37].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`

### B.38 - Edwin's Demise (26 caminhos NULL)

- `$.eventos[38].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[38].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[38].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[38].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[38].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[38].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[38].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[38].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[38].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[38].opcoes[0].efeitos[1].batalha.dados_recompensa_final`
- `$.eventos[38].opcoes[0].efeitos[1].batalha.referencia.chave`
- `$.eventos[38].opcoes[0].efeitos[1].batalha.referencia.nome`
- `$.eventos[38].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[38].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[38].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[38].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[38].opcoes[0].efeitos[1].evento_encadeado.chave`
- `$.eventos[38].opcoes[0].efeitos[1].evento_encadeado.nome`
- `$.eventos[38].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[38].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[38].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[38].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[38].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final`
- `$.eventos[38].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final`
- `$.eventos[38].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final`
- `$.eventos[38].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado`

### B.39 - Elder Tree (26 caminhos NULL)

- `$.eventos[39].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[39].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[39].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[39].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[39].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[39].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[39].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[39].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[39].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[39].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[39].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[39].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[39].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[39].opcoes[1].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[39].opcoes[1].efeitos[0].batalha.referencia.chave`
- `$.eventos[39].opcoes[1].efeitos[0].batalha.referencia.nome`
- `$.eventos[39].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[39].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[39].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[39].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[39].opcoes[1].efeitos[0].evento_encadeado.chave`
- `$.eventos[39].opcoes[1].efeitos[0].evento_encadeado.nome`
- `$.eventos[39].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[39].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[39].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[39].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado`

### B.40 - Enchanted Axe (34 caminhos NULL)

- `$.eventos[40].opcoes[0].efeitos[0].batalha.dados_recompensa_final`
- `$.eventos[40].opcoes[0].efeitos[0].batalha.referencia.chave`
- `$.eventos[40].opcoes[0].efeitos[0].batalha.referencia.nome`
- `$.eventos[40].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[40].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[40].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[40].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[40].opcoes[0].efeitos[0].evento_encadeado.chave`
- `$.eventos[40].opcoes[0].efeitos[0].evento_encadeado.nome`
- `$.eventos[40].opcoes[0].efeitos[1].batalha.dados_recompensa_final`
- `$.eventos[40].opcoes[0].efeitos[1].batalha.referencia.chave`
- `$.eventos[40].opcoes[0].efeitos[1].batalha.referencia.nome`
- `$.eventos[40].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final`
- `$.eventos[40].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final`
- `$.eventos[40].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final`
- `$.eventos[40].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado`
- `$.eventos[40].opcoes[0].efeitos[1].efeitos[1].recompensas.experiencia.quantidade_final`
- `$.eventos[40].opcoes[0].efeitos[1].efeitos[1].recompensas.itens.sorteio_final`
- `$.eventos[40].opcoes[0].efeitos[1].efeitos[1].recompensas.ouro.quantidade_final`
- `$.eventos[40].opcoes[0].efeitos[1].efeitos[1].recompensas.status.resultado_sorteado`
- `$.eventos[40].opcoes[0].efeitos[1].evento_encadeado.chave`
- `$.eventos[40].opcoes[0].efeitos[1].evento_encadeado.nome`
- `$.eventos[40].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final`
- `$.eventos[40].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final`
- `$.eventos[40].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final`
- `$.eventos[40].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado`
- `$.eventos[40].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final`
- `$.eventos[40].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final`
- `$.eventos[40].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final`
- `$.eventos[40].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado`
- `$.eventos[40].opcoes[0].recompensas[1].padrao[1].experiencia.quantidade_final`
- `$.eventos[40].opcoes[0].recompensas[1].padrao[1].itens.sorteio_final`
- `$.eventos[40].opcoes[0].recompensas[1].padrao[1].ouro.quantidade_final`
- `$.eventos[40].opcoes[0].recompensas[1].padrao[1].status.resultado_sorteado`

---

## 7. Analise C - agregados medidos

| medida | valor |
|---|---|
| eventos na faixa | 20 |
| chaves unicas / ids unicos | 20 / 20 |
| opcoes no total | 36 |
| acoes no total (Success + Failure) | 38 (32 Success, 6 Failure) |
| eventos sem narrativa | [24, 37] |
| eventos com disabled=1 | [21, 31, 34] |
| eventos com 1 unica opcao | [24, 28, 35, 37, 40] |
| eventos com acao Failure | [26, 28, 35, 36, 38, 40] |
| eventos com bonus de rolagem | [26, 27, 28, 33, 35, 36, 38, 40] |
| eventos com rolagem e sem Failure | [27, 33] |
| eventos que iniciam batalha | [21, 25, 26, 27, 29] |
| eventos que iniciam batalha sem BattleInfo referenciado | [25, 29] |
| eventos que concedem status | [21, 22, 23, 24, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 40] |
| eventos que concedem item | [32, 37] |
| eventos que concedem XP | [28, 33, 35, 39, 40] |
| eventos que concedem ouro | [] |
| eventos com opcao sem texto | [37] |
| eventos com acao de resultado sem texto | [21, 24, 25, 29, 37] |
| eventos com status_requeridos em alguma opcao | [] |
| LeadsToFortune=1 | [21, 22, 23, 25, 27, 29, 31, 34, 36, 38] |
| raridade | Common: [21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40]; Legendary: [37]; Rare: [26, 27] |
| peso | 1.0: [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40] |
| caminhos NULL | 492 |

---

## 8. Auditoria automatica offline

Comando executado (a partir do workspace do cartao):

```
python audit_b02.py C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b02-parte02.md
```

Para reproducao a partir desta pasta (arquivos do lote):

```
python EV-R2-NORMAL-b02-parte02-validar.py EV-R2-NORMAL-b02-parte02.md
```

Saida REAL da execucao:

```
== AUDITORIA EV-R2-NORMAL-b02-parte02 ==
documento: C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b02-parte02.md
fontes: eventos.json lote-Normal-v2.md eventos.schema.json catalogo-referencias.json

CHECK A0.documento_existe                            PASS 
CHECK A1.hashes_declarados                           PASS 4 declarados
CHECK A2.hashes_conferem                             PASS 
CHECK B1.total_20                                    PASS 
CHECK B2.ordinais_21_40                              PASS 
CHECK B3.categoria_normal                            PASS 
CHECK B4.chaves_unicas_20                            PASS 
CHECK B5.ids_unicos_20                               PASS 
CHECK B6.ordinal_nao_e_path_id                       PASS ordem por secao difere de path_id crescente
CHECK C1.secoes_no_documento                         PASS 
CHECK C2.tabela_identidade_doc                       PASS 
CHECK C3.titulos_lote_vs_eventos                     PASS 
CHECK D1.jsonpath_existe                             PASS 19 propostas
CHECK D2.antes_confere_com_fonte                     PASS 
CHECK D3.depois_difere_de_antes                      PASS 
CHECK E1.antes_depois_citados_no_doc                 PASS 19 propostas
CHECK F1.20_vereditos_publicados                     PASS 
CHECK F2.contagem_veredito_confere                   PASS {'MELHORAR': 11, 'MANTER': 9}
CHECK F3.inventario_publicado                        PASS 
CHECK G1.nulls_doc_igual_fonte                       PASS 492 caminhos
CHECK G2.nulls_existem_e_sao_nulos                   PASS 
CHECK H1.parte01_preservada                          PASS sha256 cbd464a551efb1420c0032c00c03ecbeee5933781f465a8a12d06c57ef046552
CHECK H2.fonte_intacta_contagens                     PASS eventos=256 Normal=160 opcoes=404
CHECK H3.sem_artefato_de_implementacao               PASS 

TOTAL PASS 24 FAIL 0  (propostas auditadas: 19; NULL auditados: 492; refutacoes: 65)
```

---

## 9. Pendencias e estado

- Este documento e **proposta documental**: nada foi implementado, nada foi alterado em EV-R1, no
  `Assembly-CSharp.dll`, em assets, plugins ou mods.
- Runtime **NAO_EXERCITADO**: nenhuma afirmacao aqui depende de execucao no jogo.
- Depende de aprovacao de conteudo do dono antes de qualquer implementacao.
- Achado pendente de decisao do dono: ordinal 34 carrega o conteudo do ordinal 31 (conteudo provisorio),
  ambos disabled. Nenhuma proposta de texto foi feita para esse slot.
- Achado pendente de decisao do dono: ordinal 27 tem `rollBonusTypes=[3]` com limiar 0 e sem Failure,
  enquanto o ordinal 26 (mesma batalha) usa o mesmo bonus com limiar 12 e ramo de falha.
- Sugestoes de alteracao do texto ingles original permanecem rotuladas e nao aplicadas.

Fim do documento.
