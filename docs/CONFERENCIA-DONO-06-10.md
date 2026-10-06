# Conferência do dono — sessão única (06/10/2026)

Uma sessão de jogo, cinco conferências. Cada item abaixo diz **o que olhar**, **o que é certo** e
**o que responder**. Tudo o que está aqui foi derivado do código do jogo e do que **está instalado**
no seu perfil agora (evidência em §0) — nada pedido "de cabeça".

---

## 0. O que está instalado (e o que NÃO está)

Conferido por mtime + decompilação da DLL que o jogo carrega (ilspycmd sobre
`...\profiles\Default\BepInEx\plugins\<mod>\<mod>.dll`):

| Mod | DLL do perfil | Fonte mais nova no repo |
|---|---|---|
| BetterTooltips | **05/10 13:36** | `LocalizePatch.cs` 06/10 13:50 ⚠ não instalado |
| RoguelikeSkillTreeVisualizer | **05/10 13:32** | `Patches.cs` 06/10 13:46, `SkillTreesTab.cs` 06/10 13:53 ⚠ não instalado |

Marcadores confirmados **dentro da DLL instalada**: `Your active shrine auras:`,
`Consuming any Globule heals you for 8` / `...20`, `CorDaLinhaDeAuras` (a cor azul vinda do jogo),
as notas de Flame/Decay e os `RSTV DIAG: botao 'Skills' ...` (tela Select Party, HUD da run,
janela do level-up).

⚠ **Consequência prática:** o que você editei/foi editado hoje (13:46–13:53) **não está no jogo**.
Se algo não aparecer como este roteiro diz, o primeiro suspeito é isso — e instalar é ato deliberado
(avisa antes, jogo fechado), não parte da conferência.

---

## 1. Antes de abrir (30 s)

1. Abrir pelo r2modman → **Start modded** (não o .exe direto: o .exe roda vanilla).
2. No boot, procurar no `LogOutput.log` a linha de ganchos: **`patches Harmony aplicados (N/N)`** e
   anotar o N. Um N diferente do esperado é o primeiro achado da sessão.

---

## 2. Party Select — janela de só-leitura (RSTV-26 / RSTV-27)

Na tela de escolha de party do roguelike, o botão quadrado **`Skills`** fica à direita do
`Choose Powerups`.

- [ ] Abre a árvore nativa em modo somente-leitura.
- [ ] **Nenhum `*0` literal** em lugar nenhum (era o defeito do RSTV-26: dano não resolvido).
- [ ] O **rodapé** (mana / cooldown / alcance / duração) pertence ao **personagem em foco**.
- [ ] Trocar o personagem em foco e conferir que o rodapé **acompanha** (era o RSTV-27: rodapé lendo
      `TooltipCharacter` nulo e caindo no personagem errado).
- [ ] Fechar com **X** e com **Esc**: fecha, não trava.
- [ ] Depois de fechar: **nenhum ponto gasto, nenhuma skill alterada** (é só-leitura de verdade —
      `AcceptSkillChanges` higienizado, `ResetSkillPoints` bloqueado).

---

## 3. Na run — botão de Skills (RSTV-6)

O botão `Skills` deve aparecer **ao lado do botão de movimentação / apontar o hex**.

Casos de risco a percorrer (é o corpo do RSTV-6):

- [ ] (a) abrir a árvore no **seu turno** e fechar
- [ ] (b) abrir durante o **turno de um inimigo**
- [ ] (c) abrir com a **mira de hex ativa**
- [ ] (d) abrir e **avançar o turno** com ela aberta
- [ ] (e) abrir **duas vezes**
- [ ] (f) fechar com **X** e com **Esc**
- [ ] (g) abrir, fechar e conferir que **nada mudou** (somente leitura)

O que tem de continuar igual: **movimentação, mira de hex, mochila, Esc/B**.
Desligar se incomodar: config `AtivarBotao=false`.

---

## 4. Tooltips de shrine — o coração do pedido

Para **cada** shrine: primeiro com o personagem **dentro** da aura, depois **fora**.

- [ ] **RV-29** — a linha só aparece quando o personagem em foco **realmente tem** aquela aura.
      Fora da aura → **não aparece**. Entrar → aparece. Sair → desaparece. Trocar de personagem em
      foco não pode deixar resíduo do anterior.
- [ ] **RV-31** — a linha **SOMA todas** as auras de shrine ativas naquele personagem, não só a do
      shrine cuja tooltip está aberta.
- [ ] **RV-44** — o número é a **CONTRIBUIÇÃO da aura**, não o total da ficha. (O defeito antigo:
      Fury com bônus 100 dizia o total do personagem, ex. 75%, quando a aura valia 50%.)
- [ ] **RV-27** — a linha sai em **AZUL** (cor lida do próprio jogo) e no **FUNDO** do tooltip, e
      **nenhuma outra nota** mudou de cor.
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

### ⚠ Correção de premissa: "Worship" NÃO EXISTE

A investigação (RV-30 / RV-48 / CHK-1) provou: **`worship` tem ZERO ocorrências no código do jogo**.
O único rastro é o `T2_Worshiper`, uma habilidade de **inimigo** — não é perk do jogador. Os casos
reais de bônus são **0**, **+8** (Omnism I), **+20** (Omnism II) e **+100** (Horn of Devotion).

O "dano dobrado" que motivou o caso +100 era um **defeito de `Source` injetado (RV-34), corrigido no
RV-30 (03/10)**. Então: **não procurar "Worship" em lugar nenhum** na tela — e se algum texto ainda
citar isso, é achado.

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
3. O dano do Decay mostrado **bate com o dano que você recebe** ao passar o turno na aura?
   (esta é a prova que fecha a dúvida do fator de escala)
4. O botão `Skills` aparece no lugar certo na run? Os 7 casos de risco passaram?
5. A janela só-leitura tem `*0` em algum lugar? O rodapé acompanha o personagem em foco?

---

## 7. Depois da sessão

Os 7 cartões do quadro (`RV-26, 27, 28, 29, 31, 33, 34`) são **a mesma conferência** que este
documento cobre — foram criados em 30/09 e o trabalho deles já foi entregue pelas rodadas
RV-23/24/30/35–48 (todos `done`). Com a sua sessão registrada, os sete fecham juntos, com este
roteiro como evidência — em vez de sete conferências separadas.

Fora do escopo desta sessão (gates separados): autorização da rodada runtime do probe (CIC-5) e a
publicação das versões novas.
