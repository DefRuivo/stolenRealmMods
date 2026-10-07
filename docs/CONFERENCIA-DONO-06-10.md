# Conferência do dono — sessão única (06/10/2026)

Uma sessão de jogo, cinco conferências. Cada item abaixo diz **o que olhar**, **o que é certo** e
**o que responder**. Tudo o que está aqui foi derivado do código do jogo e do que **está instalado**
no seu perfil agora (evidência em §0) — nada pedido "de cabeça".

---

## 0. O que está instalado (e o que NÃO está)

Esta seção é **medida, não digitada**. A tabela sai deste comando, que lê (nunca escreve) o sha256 e
o mtime das DLLs **instaladas no perfil** e das DLLs já buildadas em `<Mod>/bin/<Config>/` no repo:

```bash
bash scripts/artefatos-conferencia.sh     # leitura pura: não builda, não instala, não abre o jogo
```

Saída literal do comando, medida em **06/10 18:51** sobre o perfil
`%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins`:

| Mod | DLL do perfil | sha256 (12 primeiros) | Fonte mais nova no repo | Veredito |
|---|---|---|---|---|
| BetterTooltips | 06/10 **16:07:20** | `6533f4368ec7` | `LocalizePatch.cs` 06/10 16:07:14 · `StatusSkillSynergyPatch.cs` 06/10 15:59:19 | **INSTALADA** (byte-idêntica à build Release) |
| RoguelikeSkillTreeVisualizer | 06/10 **15:08:11** | `40e620e61082` | `SkillTreeShortcut.cs` 06/10 18:19:44 · `Plugin.cs` 06/10 18:19:44 | **INSTALADA** (byte-idêntica à build Release) · fonte do repo **MAIS NOVA** que a DLL instalada (mudança não instalada) |
| RoguelikeDebugger | 06/10 **15:32:47** | `55bc6250a905` | `FlameShrineProcPatch.cs` 06/10 15:32:40 · `EfeitosInfo.cs` 03/10 20:33:43 | **INSTALADA** (byte-idêntica à build Debug) |

O `RoguelikeDebugger` é o probe do RV-49 (§4.1). **Varredura das linhas escritas à mão** (o achado que
originou esta revisão): só a linha do **BetterTooltips** envelheceu — ela dizia `15:51:22 /
64cce414a9f2`, um hash que **não corresponde a arquivo nenhum no disco**; medido hoje é `16:07:20 /
6533f4368ec7`. As linhas do `RoguelikeSkillTreeVisualizer` (`15:08:11 / 40e620e61082`) e do
`RoguelikeDebugger` (`15:32:47 / 55bc6250a905`) **conferiam** com o disco. Nenhuma linha ficou "não deu
para medir" (as três DLLs existem no perfil). A coluna **Fonte mais nova no repo** também era digitada
à mão e envelheceu nas duas primeiras linhas; agora ela é o `find` por mtime do próprio script.

**Marcadores** — o mesmo comando confere, dentro de cada DLL instalada, os literais que os mods
imprimem (os literais .NET vivem em UTF-16 dentro da DLL; é a mesma coisa que a decompilação enxerga):

| Marcador (citado na seção 0) | DLL do perfil | Ocorrências | Veredito |
|---|---|---|---|
| `Your active shrine auras:` | BetterTooltips | 3 | PRESENTE |
| `Consuming any Globule heals you for` | BetterTooltips | 6 | PRESENTE |
| `CorDaLinhaDeAuras` | BetterTooltips | 1 | PRESENTE |
| `In the aura now (raw damage it takes as the attacker` | BetterTooltips | 1 | PRESENTE |
| `damage per turn while in the aura.` | BetterTooltips | 1 | PRESENTE |
| `RSTV DIAG: botao 'Skills'` | RoguelikeSkillTreeVisualizer | 9 | PRESENTE |
| `[FlameRV49]` | RoguelikeDebugger | 2 | PRESENTE |
| `BOOT ` | RoguelikeDebugger | 16 | PRESENTE |
| `PROC Source=` | RoguelikeDebugger | 1 | PRESENTE |
| `PROC Target=` | RoguelikeDebugger | 1 | PRESENTE |
| `PCT de ` | RoguelikeDebugger | 1 | PRESENTE |
| `DANO final[` | RoguelikeDebugger | 1 | PRESENTE |
| `MATRIZ '` | RoguelikeDebugger | 1 | PRESENTE |
| `CRU ` | RoguelikeDebugger | 1 | PRESENTE |

Leitura: `CorDaLinhaDeAuras` é a cor azul vinda do jogo; `In the aura now (...)` e `damage per turn
while in the aura.` são as notas de Flame/Decay; os `RSTV DIAG: botao 'Skills' ...` cobrem a tela
Select Party, o HUD da run e a janela do level-up; e, no `RoguelikeDebugger`, `[FlameRV49]` com
`BOOT` / `PROC` / `CRU` / `PCT` / `DANO final` / `MATRIZ` é a instrumentação do RV-49 (§4.1).

⚠ **O número vale para o build que está no perfil.** Se você deployar de novo, esta tabela envelhece
outra vez: rode `bash scripts/artefatos-conferencia.sh` antes de conferir — o comando lê o disco na
hora, não tem valor guardado. (Rodar duas vezes sem mexer em nada dá saída idêntica.)

⚠ **Consequência prática (mudou):** **tudo o que está no repo agora ESTÁ no jogo** — a única exceção é a
do `RoguelikeSkillTreeVisualizer`, na ressalva logo abaixo. Se algo não aparecer
como este roteiro diz, o primeiro suspeito **não** é build velha — é comportamento. Instalar continua
sendo ato deliberado (avisa antes, jogo fechado), fora desta conferência.

⚠ **Ressalva de 06/10 (RSTV-29) — só para o `RoguelikeSkillTreeVisualizer`:** a fonte do mod no repo já
**não tem** o botão `Skills` da tela **Select Party**, mas essa mudança **não está instalada nem
publicada** — é exatamente o que a coluna **Veredito** da tabela acima marca ("fonte do repo MAIS NOVA
que a DLL instalada"): a DLL do seu perfil é de **15:08:11** e o zip no ar (0.3.2, de 04/10) é anterior
a ela. Ou seja: em jogo você **ainda vê** aquele botão, e é por isso que o marcador
`RSTV DIAG: botao 'Skills'` (9 ocorrências) continua batendo. O roteiro usa os caminhos da §2.

---

## 1. Antes de abrir (30 s)

1. Abrir pelo r2modman → **Start modded** (não o .exe direto: o .exe roda vanilla).
2. No boot, procurar no `LogOutput.log` a linha de ganchos: **`patches Harmony aplicados (N/N)`** e
   anotar o N. Um N diferente do esperado é o primeiro achado da sessão.

---

## 2. Party Select — janela de só-leitura (RSTV-26 / RSTV-27)

Nesta tela **não existe mais botão do mod**: a `RSTV-29` (decisão do dono, 06/10) removeu o `Skills`
que ficava à direita do `Choose Powerups`. Os dois caminhos que **ficaram** — qualquer um dos dois vale
como validação:

- **Botão quadrado `Skills` do modal `Remove Skill Trees`** (canto superior direito do título do modal,
  aberto a partir desta mesma tela): abre a árvore read-only do personagem **que o modal está mostrando**.
- **Atalho `F10`** (tecla configurável em `TeclaAtalhoSkillTree`): abre a mesma árvore direto na tela de
  party, sem botão nenhum — o alvo é o último personagem **seu** que entrou na party.

Se você ainda vir um botão quadrado **na própria tela**, ao lado de `Choose Powerups`, é a build
**anterior** à RSTV-29 (a remoção ainda não está instalada nem publicada — ver a ressalva de §0): ele
não faz parte deste roteiro.

- [ ] Abre a árvore nativa em modo somente-leitura.
- [ ] **Nenhum `*0` literal** em lugar nenhum (era o defeito do RSTV-26: dano não resolvido).
- [ ] O **rodapé** (mana / cooldown / alcance / duração) pertence ao **personagem em foco**.
- [ ] Trocar o personagem em foco e conferir que o rodapé **acompanha** (era o RSTV-27: rodapé lendo
      `TooltipCharacter` nulo e caindo no personagem errado).
- [ ] Fechar com **X** e com **Esc**: fecha, não trava.
- [ ] Depois de fechar: **nenhum ponto gasto, nenhuma skill alterada** (é só-leitura de verdade —
      `AcceptSkillChanges` higienizado, `ResetSkillPoints` bloqueado).

---

## 3. Na run — botão de Skills (RSTV-6 / **RSTV-30**)

> **MUDOU NA RSTV-30 (06/10, pedido do dono em jogo).** O botão **deixou a linha do botão de apontar
> o hex** e passou para a **barra de baixo**, na mesma linha dos botões nativos de **inventário** e de
> **skills**, no vão livre antes do controle que **rotaciona a barra de skills**. E ele **não é mais
> escondido por estado**: fica **visível enquanto o HUD aparece** (inclusive fora de combate e
> enquanto outro personagem age). O que o portão decide agora é só o **clique**.
>
> ⚠ **A RSTV-30 NÃO está instalada** (o perfil tem a build de 06/10 15:08, anterior a ela). O roteiro
> abaixo é da build nova — a conferência visual é justamente o que falta para fechá-la. Como
> desempatar: na build **instalada** o botão está ao lado do botão de apontar o hex e pisca; na build
> **nova** ele está na barra de baixo e não pisca.

Onde olhar: **barra de baixo, à esquerda** — à direita dos botões de inventário e de skills e **antes
das setas** que rotacionam a barra de skills. É um quadradinho com o **ícone de árvore de skills**.

- [ ] (0) **Casa nova:** o botão está **na barra de baixo**, na linha dos botões de inventário e de
      skills — e **os botões nativos não se moveram nem encolheram**.
- [ ] (1) **Piscar (o defeito principal):** deixe um inimigo agir/andar e **não tire o olho** — o botão
      **não pode desaparecer**. No log, no máximo, a linha troca para
      `RSTV DIAG: botao 'Skills' do HUD VISIVEL na barra de baixo e SEM clique agora — <motivo>`.
- [ ] (2) **Fora de combate:** ande no **mapa** e volte para a **cidade** — o botão continua lá.
- [ ] (3) abrir a árvore no **seu turno** e fechar
- [ ] (4) abrir durante o **turno de um inimigo**
- [ ] (5) abrir com a **mira de hex ativa** — aqui o botão **continua visível** e só **não clica**
- [ ] (6) abrir e **avançar o turno** com ela aberta
- [ ] (7) abrir **duas vezes**
- [ ] (8) fechar com **X** e com **Esc**
- [ ] (9) abrir, fechar e conferir que **nada mudou** (somente leitura)

O que tem de continuar igual: **movimentação, mira de hex, mochila, Esc/B**.
Desligar se incomodar: config `AtivarBotao=false` (ou `AtivarBotaoNaRun=false` para tirar só o da run).

**Procedência dos números (se algo não bater):** a linha `RSTV-30: botao 'Skills' injetado na BARRA DE
BAIXO do HUD (...)` no `LogOutput.log` traz a **largura final** do botão, a **largura nativa**, a
**borda direita dos nativos**, o **limite medido do vizinho** e o **vão livre** — é com ela em mãos que
o ajuste é feito (nada de chute). Detalhes e o desenho da decisão:
`docs/RSTV-30-botao-na-barra-de-baixo.md`.

---

## 4. Tooltips de shrine — o coração do pedido

Para **cada** shrine: primeiro com o personagem **dentro** da aura, depois **fora**.

**RV-31 — como ficar DENTRO de duas auras de shrine ao mesmo tempo (o caso que falta na conferência).**
A aura do shrine é aplicada ao personagem em foco quando ele entra na área do `GroundEffect` e **não é
removida ao sair** (o motor só remove status `Infinite` — a aura do shrine não é; é por isso que a mesma
aura aparece repetida na lista viva, RV-46). Então as auras **acumulam**: entre na área do shrine **A**,
caminhe até a área do shrine **B** e **pare lá**. O personagem carrega as duas ao mesmo tempo. Agora
abra o tooltip do shrine **A** e, depois, o do shrine **B** — a linha azul tem de listar **AS DUAS**
(ex.: `Dodge +40% (total +57%); Life on Hit +16 (total …)`), e o conteúdo tem de ser **o mesmo nos dois
hovers**, com a aura daquele shrine entre as listadas.

O que reprova: a linha listar só a aura do shrine cuja tooltip está aberta (é exatamente a regressão que
o RV-29 deixou e o RV-31 desfez) — ou mudar de conteúdo ao trocar de shrine aberto. Procedência no log:
`RV-31 acumulado: auras=[A, B] …` traz TODAS as auras que entraram na conta daquele hover.

- [ ] **RV-29** — a linha só aparece quando o personagem em foco **realmente tem** aquela aura.
      Fora da aura → **não aparece**. Entrar → aparece. Sair → desaparece. Trocar de personagem em
      foco não pode deixar resíduo do anterior.
- [ ] **RV-31** — a linha **SOMA todas** as auras de shrine ativas naquele personagem, não só a do
      shrine cuja tooltip está aberta.
- [ ] **RV-44** — o número é a **CONTRIBUIÇÃO da aura**, não o total da ficha. (O defeito antigo:
      Fury com bônus 100 dizia o total do personagem, ex. 75%, quando a aura valia 50%.)
- [ ] **RV-27** — a linha sai em **AZUL** (cor lida do próprio jogo) e no **FUNDO** do tooltip, e
      **nenhuma outra nota** mudou de cor. Esperado: **`#00D7FF`** (azul lido em runtime de
      `GUIManager.coldColor`, a cor do dano Cold; a 1ª escolha `Tooltip.skillStatusColor` é bege e é
      pulada). A conferência é: (a) a linha `Your active shrine auras: …` está na **última** posição,
      **depois** da nota da shrine; (b) há **exatamente uma linha em branco** antes dela; (c) ela é
      azul e as demais notas seguem **beges** (`#CBB396`). Procedência da cor:
      `LocalizePatch.cs` → `CorDaLinhaDeAuras`/`LerCorAzulDoJogo`. O log traz
      `cor da linha de auras ativas = #00D7FF` no 1º hover.
- [ ] **RV-34** — a nota diz que o número é **antes das reduções de dano**.
- [ ] **RV-33 / RV-26** — Flame e Decay aparecem com **número real**, não descrição nem `*0`.

### Números esperados (base → bônus aplicado)

O bônus é `1 + ShrineEffectBonus/100`, com `Mathf.Round` half-to-even do Unity.

| Shrine / atributo | base | Omnism I (+8) | Omnism II (+20) | Horn of Devotion (+100) |
|---|---|---|---|---|
| Warrior / Guardian / Conqueror / Rogue (dano, redução, crit, dodge) | 20 | 22 | 24 | 40 |
| Reaper (life on hit) | 8 | 9 | 10 | 16 |
| Seraph (vida/turno) · Shaman (mana/turno) | 10 | 11 | 12 | 20 |
| Energy (custo de mana — exibido sem sinal, "reduced") | 50 | 54 | 60 | 100 |
| Fury (dano ganho) | +25 | +27 | +30 | +50 |
| Fury (dano tomado) | −25 | −27 | −30 | −50 |

**Decay** — dano por turno = `Round(vida máxima de QUEM ESTÁ NA AURA × % do tipo DELE)`, sem mínimo.
Você é `player` = **10%** → personagem de 100 de vida = **10 por turno**; com bônus +100 = **20**.

**Flame** — o alvo é **QUEM ATACA** quem está na aura; o dano é `Max(1, Round(vida máxima DO
ATACANTE × % do tipo DELE))` → atacante `player` = 5%. Ou seja: **não é 5% da SUA vida** — é 5% da
vida de quem te bate. Comparar com o dano que aparece de fato.

### 4.1 RV-49 — o fator `ShrineEffectBonus` nas duas auras de PERIGO (Decay e Flame)

**Premissa corrigida (06/10, cartão t_d02f9212 — cadeia elo por elo no docstring de
`BetterTooltips/Patches/ShrineAuraPatch.cs`, `FraseAlvosDoFlame`):** no caminho do **dano** dessas duas
auras o `Source` da ação é o **EXECUTOR do gatilho** — o asset do status tem `UseTriggerSource = 0` e o
motor escolhe o executor (decompilado l.41935 e l.42632) —, ou seja o `Source` é **o personagem que TEM
a aura**, e **não** o personagem vazio do shrine. Consequências:

* o **dano real** escala com o bônus de QUEM ESTÁ NA AURA: o fator `(1 + ShrineEffectBonus/100)` está
  dentro da fórmula das ações `Decay Aura Proc` / `Flame Aura Proc` (o que o log de boot confirma:
  `TargetStored['ShadowDamage'] = Mathf.Round((Target['MaxHealth'] * Target.GetValueByEnemyType(...)) *
  (1 + (Source['ShrineEffectBonus'] / 100)))`);
* o **número que a tooltip mostra** é avaliado **SEM** esse fator (a decisão do RV-30, de 03/10) — as
  duas coisas convivem de propósito, e é exatamente isso que a medição abaixo decide.

**A) Decay — personagem COM `Horn of Devotion` (+100) parado na área do Decay Shrine**

- [ ] Com o mouse no shrine, ler a linha azul: `(N damage per turn for you)`. Anotar **N** e a **vida
      máxima** do personagem em foco.
- [ ] **Passar o turno dentro da aura** e anotar o **dano que aparece na tela** no personagem.
- [ ] Controle: **tirar o `Horn`** (bônus 0), repetir os dois passos e anotar o dano de novo.

O que é certo, com vida `V` e bônus `B`: `N = Round(V × 10%)` **sempre** — o N exibido não muda com o
bônus, é a linha de hoje. O dano de tela deve ser `Round(V × 10% × (1 + B/100))`.
Com `V = 100`: **N = 10**; com +100 → **tela ≈ 20**; com bônus 0 → **tela ≈ 10**.
Leitura: **tela ≈ 2× N ⇒ o motor aplica o bônus de quem tem a aura e o N exibido NÃO o inclui**;
tela igual ao N ⇒ o RV-30 estava certo e o fator não age aqui.

**B) Flame — personagem COM +100 parado na aura, sendo atacado por um inimigo**

- [ ] Com o mouse no shrine, ler o item `In the aura now (raw damage it takes as the attacker, from the
      attacker's own Max Health): <atacante> M`. Anotar **M**, a **vida máxima** e o **tipo** do atacante.
- [ ] Anotar o **dano de fogo que o ATACANTE leva** na tela.
- [ ] Controle: repetir sem o bônus (+100 fora).

O que é certo: `M = Max(1, Round(vida máxima do ATACANTE × % do tipo dele))` — `player` 5%,
`soldier` 12%, `elite` 10%, `champion` 8%, `boss` 2,5%, `fodder` 14%. Com +100 **em você**, a tela deve
mostrar ≈ **2× M**.

**O log você não precisa ler — eu leio.** O `RoguelikeDebugger` já instalado grava, a cada proc real,
com o prefixo `[FlameRV49]`:

| linha | o que ela prova |
|---|---|
| `PROC Source=... ShrineEffectBonus=<b>` / `PROC Target=...` | **quem o motor põe em cada slot** no proc REAL (nome, `IsAI`, tipo, vida máxima e o bônus REAL de cada lado) |
| `PCT de ... -> <pct>` | a % do tipo resolvida pelo motor |
| `DANO final[i] ... ACTUAL=<d>` | o dano do motor **ANTES** da mitigação de armadura/resistência |
| `MATRIZ '<caso>' -> <chave>=<v>` (bônus 0 / 8 / 20 / 100) | a contra-prova do MESMO proc, feita pelo motor, **sem trocar equipamento** |

Se o número da tela for menor que o `ACTUAL` do log, a diferença é mitigação/resistência: o que decide é
a **razão** (dobrou × igual), não o valor absoluto.

### ⚠ Correção de premissa: "Worship" NÃO EXISTE

A investigação (RV-30 / RV-48 / CHK-1) provou: **`worship` tem ZERO ocorrências no código do jogo**.
O único rastro é o `T2_Worshiper`, uma habilidade de **inimigo** — não é perk do jogador. Os casos
reais de bônus são **0**, **+8** (Omnism I), **+20** (Omnism II) e **+100** (Horn of Devotion).

O "dano dobrado" que motivou o caso +100 **NÃO era só** o `Source` injetado pelo RV-34: a evidência de
06/10 (t_d02f9212) mostrou que, **no caminho do DANO**, o `Source` da ação é o personagem que TEM a aura
— então o motor dobra mesmo, e o que estava errado era a **atribuição** ("perk do jogador"). Logo:
**não procurar "Worship" em lugar nenhum** na tela — e se algum texto ainda citar isso, é achado. O que a
tooltip passa a mostrar por causa disso é o **RV-49** (§4.1).

---

## 5. Globule — cura do Sustenance (RV-28)

> O **pacote detalhado** desta conferência (lista final, passo a passo para chegar à tooltip de cada
> globule, matriz preenchida e tabelas de OK/NOK para registrar) é `docs/CONFERENCIA-RV28-GLOBULES.md`
> — este §5 é o resumo.

Com **Sustenance II (20%)**, um personagem de **100 de vida e 200 de mana** deve ver no tooltip do
globule: **20 de vida e 40 de mana**. Com **Sustenance I (8%)**: **8 e 16**.

- [ ] O número é **dinâmico** (muda com a vida/mana máxima do personagem em foco).
- [ ] Vale para **todos** os globules da família (`Cleansing`, `Energy`, `Health`, `Mana`, `Power` e
      `Refreshing Globule`) e também para os seis **pickups de poção**, que entram com outro sujeito
      ("Picking this up also heals you for …", não "Consuming a Globule …").
- [ ] O valor sai com **uma casa decimal** quando não é inteiro (ex.: `46.6 health` para 233 de vida a
      20%) — a cura real do motor não arredonda, então o mod não afirma inteiro. No seu caso de
      referência (100/200) sai inteiro: `20 health and 40 mana`.
- [ ] `Power Globule` **também** ganha o número: ele é buff de dano (não cura), mas a cura do
      `Sustenance` dispara ao **consumir qualquer** globule, e a frase que aparece é sobre o consumo
      ("Consuming a Globule also heals you for …"), não sobre o efeito dele. *(Correção de 06/10: este
      item dizia o contrário da decisão registrada — ver `docs/cobertura/rv28-globules.md` §4.)*
- [ ] A % é a das tiers que o jogo tem **ativas** (`Character.Skills`, já resolvida por
      `SkillsThatReplace`): **8%** com só a I, **20%** com só a II — e **28%** se o jogo mantiver as
      duas ativas, porque cada tier tem o seu próprio gatilho em `OnGlobulePickup`. O ponto 8/20/28
      segue **aberto** (RV-24); o mod **não crava nem soma por conta própria**, ele mostra o que está
      ligado. *(Correção de 06/10: o "nunca 28%" que estava aqui era a hipótese não provada.)*

---

## 6. O que responder (perguntas fechadas)

1. A linha azul aparece/some conforme dentro/fora da aura? Soma todas? Mostra a contribuição?
2. Os números batem com a tabela de §4? (se algum divergir, dizer **qual shrine, qual bônus, valor
   visto × esperado**)
3. **RV-49 — a prova que fecha a dúvida do fator de escala** (§4.1). Responder com os números:
   (a) Decay com `Horn` (+100) — o **N** da linha azul e o **dano que você recebeu na tela**;
   (b) Decay sem o `Horn` — o dano na tela;
   (c) Flame com +100 em você — o **M** do item e o **dano de fogo que o ATACANTE levou**;
   (d) Flame sem o +100 — o dano que o atacante levou.
   (Referência: **tela ≈ 2× o número exibido ⇒ o motor usa o bônus de quem tem a aura**.)
4. O botão `Skills` aparece no lugar certo na run? Os 7 casos de risco passaram?
5. A janela só-leitura tem `*0` em algum lugar? O rodapé acompanha o personagem em foco?

---

## 7. Depois da sessão

Os 7 cartões do quadro (`RV-26, 27, 28, 29, 31, 33, 34`) são **a mesma conferência** que este
documento cobre — foram criados em 30/09 e o trabalho deles já foi entregue pelas rodadas
RV-23/24/30/35–48 (todos `done`). Com a sua sessão registrada, os sete fecham juntos, com este
roteiro como evidência — em vez de sete conferências separadas.

O **RV-49** (§4.1) **entra na MESMA sessão** e é a única decisão que sai dela: os números das duas auras
de perigo (o log `[FlameRV49]` do probe é a outra metade da prova). A decisão dele vai para o `KANBAN.md`
e, se for "mudar o número", a linha do Decay/Flame é reescrita e este roteiro é refeito — por isso a
sessão é uma só.

Fora do escopo desta sessão (gates separados): autorização da rodada runtime do probe (CIC-5) e a
publicação das versões novas.
