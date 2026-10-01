# CHK-1 — o checklist de shrines virou conferência mecânica

Data: 30/09/2026 · Status: **ferramenta entregue e provada** (gerador + conferidor + contra-prova).
Escopo: só `tools/` e `docs/`. **Nenhuma linha de código de mod foi tocada nesta rodada** — e por um
motivo concreto, explicado em §7 (há **um campo que falta no log** para a conferência ficar 100%).

Tarefa: kanban `t_57052a7c` (CHK-1). Bases dos números: `docs/cobertura/revisao/RV-19-shrines.md`
§2/§4 (provadas contra o asset e o decompilado) e o censo `docs/cobertura/status.csv`.

---

## 0. O que mudou para o dono

| | antes | depois |
|---|---|---|
| Quem calcula o esperado | uma pessoa, à mão | `tools/gera_shrines_esperado.py`, lendo a fonte da verdade |
| Quem compara | o dono, lendo a tela e transcrevendo | `tools/checa_shrines.py`, lendo o log |
| Rastro | nenhum (a transcrição errada só apareceu porque alguém mediu em jogo) | cada base sai com `arquivo:linha` (ou `assets@offset`); cada resultado sai com `char=`, `log:<linha>` e a diferença |
| Cobertura | presumida | **listada**: o que não foi exercitado sai como `AUSENTE` e a rodada **não** fecha em verde |
| Trabalho do dono | ler N numbers, conferir 3 casos, transcrever | abrir cada shrine **uma vez** e passar o mouse (roteiro em §5) |

O que **não** mudou: a leitura visual final do texto na tela continua sendo do dono (é o limite nº 1
de §6 — a ferramenta comparece com números, não com pixels).

---

## 1. A tabela de esperados — GERADA, nunca digitada

Arquivo versionado: **`tools/dados/shrines-esperado.csv`** (39 linhas = 13 pares
aura/atributo × 3 casos). Companheiro: **`tools/dados/shrines-percentuais.csv`** (a % por tipo de
inimigo do Decay e do Flame).

Comando: `python tools/gera_shrines_esperado.py` (e `--check` para provar que o arquivo versionado
ainda é o que as fontes geram).

### 1.1 De onde saiu cada BASE (a citação é parte da saída do gerador)

| Aura | Atributo | Base | Fonte (citada pelo gerador) |
|---|---|---|---|
| Warrior Aura | DamageMod | 20 | `docs/cobertura/status.csv:547` |
| Guardian Aura | DamageReduction | 20 | `docs/cobertura/status.csv:216` |
| Conqueror Aura | CritChance | 20 | `docs/cobertura/status.csv:77` |
| Rogue Aura | DodgeChance | 20 | `docs/cobertura/status.csv:402` |
| Reaper Aura | LifeOnHit | 8 | `docs/cobertura/status.csv:387` |
| Seraph Aura | HealthPerTurnPercent | 10 | `docs/cobertura/status.csv:418` |
| Shaman Aura | ManaPerTurnPercent | 10 | `docs/cobertura/status.csv:421` |
| Energy Aura | ManaCostMod | **−50** (o texto exibe 50) | `docs/cobertura/status.csv:170` |
| Fury | DamageMod | 25 | `docs/cobertura/status.csv:205` |
| Fury | DamageReduction | **−25** | `docs/cobertura/status.csv:205` |
| Dwarven Aura | (stun — sem atributo) | 20 | `resources.assets@1517115364` |
| Decay Shrine Aura | (dano/turno) | 10 | `resources.assets@1517114276` |
| Flame Shrine Aura | (dano por atacante) | 5 | `resources.assets@1517121008` |

- **9 auras de buff**: a base sai da coluna `efeitos` do censo, que traz a **expressão real do
  status do jogo** (`Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`). O gerador só
  aceita essa forma exata; qualquer outra coisa que apareça ali **aborta** (§4, CP-3).
- **Dwarven, Decay e Flame**: o censo traz `efeitos` **vazio de propósito** (RV-19 §5 — o Dwarven
  não expõe efeito e as duas outras leem `Source`), então a base vem do `resources.assets`, na
  janela documentada em RV-19 §8. O gerador imprime o **offset encontrado** (ex.: Decay
  `@1517114276`, que é a string `Mathf.Round(10 * (1 + (Source["ShrineEffectBonus"] / 100)))`).
- **% por tipo de inimigo** (Decay/Flame): lidas do campo `Effects[0].Action` das ações
  `Decay Aura Proc` / `Flame Aura Proc`, em **UTF-16LE** (a armadilha do Odin documentada em
  RV-19 §1) — ordem real dos 6 parâmetros:
  `GetValueByEnemyType(boss, champion, elite, soldier, fodder, player)`. Resultado gerado:
  Decay 5/10/12/15/20/10 %, Flame 2,5/8/10/12/14/5 %, `Mathf.Max(1,` **só** no Flame — igual a
  RV-19 §4.3.

### 1.2 Os 3 casos e o que é "contribuição" × "total"

- `contribuicao_esperada` = `Round(BASE × (1 + bônus/100))`, com o `Mathf.Round` **half-to-even**
  do Unity (é o mesmo arredondamento do motor). Casos gerados: **0**, **+20** (`Omnism II`) e
  **+100** (`Worship`). Confere com RV-19 §2.2: base 20 → 20/24/40 · base 8 → 8/10/16 ·
  base 10 → 10/12/20 · base −50 → −50/−60/−100 · 25/−25 → 25/30/50 e −25/−30/−50 ·
  Flame 5 → 5/6/10 · Decay 10 → 10/12/20.
- `total_esperado` / `resto_esperado` **só existem onde o repositório prova**: os prints do dono
  em RV-19 §9.1/§10.5 (Fury bônus 0 e 100, Rogue bônus 100) — a coluna `fonte_total` cita o
  `arquivo:linha`. Nos outros casos o total **depende do equipamento do personagem** e o campo fica
  **vazio**: total não se inventa. Quem cobra a parcela do personagem é a checagem de
  **aditividade** (§3), que vale para qualquer personagem.
- Grandeza: os valores são os **crus do atributo**. Em `DamageReduction` o texto da tela mostra o
  sinal invertido (`total +5%` = atributo −5), como em RV-19 §9.1 — o CSV guarda o valor do
  atributo (−5) e é isso que o conferidor compara.

---

## 2. Como se usa

```bash
python tools/gera_shrines_esperado.py            # (re)gera tools/dados/*.csv das fontes
python tools/gera_shrines_esperado.py --check    # trava: a tabela versionada == o que as fontes geram

python tools/checa_shrines.py                    # log do perfil do r2modman (padrão)
python tools/checa_shrines.py --log OUTRO.log    # outro log (fixture, sessão arquivada)
python tools/checa_shrines.py --so-cobertura     # só o que NÃO foi exercitado
```

Estado por linha: **OK** · **ACHADO** (difere; traz observado, esperado e a diferença) ·
**AUSENTE** (não exercitado - **não** fecha a rodada em verde) · **NAO-VER** (não verificável pela
ferramenta por desenho; só o Dwarven, e a prova dele é visual).

Exit codes: **0** = todos os casos exercitáveis bateram · **1** = houve ACHADO (reprovado) ·
**2** = não conseguiu verificar (log/tabela ausente) · **3** = nada reprovou, mas há AUSENTE
(conferência **incompleta**). O gerador: 0 = gerou; 1 = **fonte ausente/fora da forma esperada**
(FALHA em vez de chutar); 2 = arquivo do repositório ausente.

---

## 3. A rodada de exemplo

### 3.1 Log do perfil **hoje** (30/09, 19:59) — rodada real, incompleta, e por um motivo que importa

```
$ python tools/checa_shrines.py
  log     : C:\Users\Pichau\AppData\Roaming\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\LogOutput.log
  esperado: ...\tools\dados\shrines-esperado.csv (39 linhas)

-- COBERTURA POR AURA --
  Warrior Aura         bonus=0    AUSENTE  bonus=20   AUSENTE  bonus=100  AUSENTE
  ... (as 12 auras, todas AUSENTE)

-- AVISOS (linhas lidas que NAO entram em comparacao; nada de silencio) --
  [AVISO]   log:3132 linha no formato PRE-RV-44: o item traz o TOTAL do personagem
            ('Damage +50%') e NAO a contribuicao das auras ('Damage +25% (total +50%)')
            - nao comparavel. O build instalado e ANTERIOR ao RV-44: recompile e
            reinstale o BetterTooltips e repita a rodada.
  [AVISO]   9 linha(s) `chave '...' -> resultado final`: texto localizado, com o `[0]`
            AINDA no lugar (o pipeline de expressoes roda depois) - NAO traz numero de aura.

-- DUMP DO ROGUELIKEDEBUGGER (fonte independente da base das auras de buff) --
  [OK]      Warrior Aura/DamageMod: base=20 conferida contra o dump do proprio jogo
  [OK]      Guardian Aura/DamageReduction: base=20 ...
  [OK]      Reaper Aura/LifeOnHit: base=8 ...
  [OK]      Energy Aura/ManaCostMod: base=-50 ...
  [OK]      Fury/DamageReduction: base=-25 ...
  [AUSENTE] Dwarven Aura: o dump tem a coluna `efeitos` VAZIA - e o caso previsto ...

== RESULTADO ==
  OK=0  ACHADO=0  AUSENTE=39  NAO-VERIFICAVEL=3
  NAO EXERCITADOS (nenhum caso OK): Conqueror Aura, Decay Shrine Aura, Dwarven Aura,
    Energy Aura, Flame Shrine Aura, Fury, Guardian Aura, Reaper Aura, Rogue Aura,
    Seraph Aura, Shaman Aura, Warrior Aura
  INCOMPLETO: nada reprovou, mas ha caso AUSENTE - ausencia NAO e aprovacao.
exit 3
```

Duas conclusões **medidas**, não supostas:

1. O `LogOutput.log` do perfil **não tem nenhuma linha `RV-34`/`RV-44`** (contado: 0): o log é de
   **30/09 19:59** e o código `RV-44` é de **30/09 20:04** — o build que gerou aquele log é anterior.
   A prova está no próprio log: as 2 linhas `RV-31 acumulado` (3116–3152) estão no formato
   **pré-RV-44** (o item traz o **total** do personagem, não a contribuição da aura) — e a ferramenta
   **detecta o formato antigo e se recusa a comparar**, em vez de dar OK num número que não é o que
   ela mede. A DLL do perfil foi recompilada depois (**30/09 21:01**), então uma rodada nova já pode
   produzir as linhas `RV-44`; **a rodada de exemplo deste relatório é a da §3.2** (fixture) porque
   o log em disco é anterior ao conserto.
2. Mesmo sem nenhum hover válido, o **dump do `RoguelikeDebugger`** no log já permitiu conferir a
   base das **9 auras de buff contra o próprio jogo** — a segunda fonte independente do §1.

### 3.2 Rodada de exemplo em fixture (`tools/fixtures/shrines-exemplo.log`) — verde

A fixture é **sintética e está rotulada como tal** no cabeçalho do arquivo: ela reproduz, no formato
exato dos marcadores, os 3 casos das 12 auras derivados de RV-19 §10; as linhas `[Status]` do dump
são **copiadas verbatim** do log real (é dado do jogo, não inventado). Serve para provar que a
ferramenta **fecha verde quando tudo bate** e para a contra-prova de §4.

```
$ python tools/checa_shrines.py --log tools/fixtures/shrines-exemplo.log
-- COBERTURA POR AURA --
  Conqueror Aura       bonus=0    OK       bonus=20   OK       bonus=100  OK
  Decay Shrine Aura    bonus=0    OK       bonus=20   OK       bonus=100  OK
  Dwarven Aura         bonus=0    N-VER    bonus=20   N-VER    bonus=100  N-VER
  Energy Aura          bonus=0    OK       bonus=20   OK       bonus=100  OK
  Flame Shrine Aura    bonus=0    OK       bonus=20   OK       bonus=100  OK
  Fury                 bonus=0    OK       bonus=20   OK       bonus=100  OK
  Guardian Aura        bonus=0    OK       bonus=20   OK       bonus=100  OK
  Reaper Aura          bonus=0    OK       bonus=20   OK       bonus=100  OK
  Rogue Aura           bonus=0    OK       bonus=20   OK       bonus=100  OK
  Seraph Aura          bonus=0    OK       bonus=20   OK       bonus=100  OK
  Shaman Aura          bonus=0    OK       bonus=20   OK       bonus=100  OK
  Warrior Aura         bonus=0    OK       bonus=20   OK       bonus=100  OK
  ...
  [OK]      Rogue Aura           DodgeChance            bonus=100 char=ChkRA contrib=40 total=57 (log:34)
  [OK]      Flame Shrine Aura    (dano/turno)           bonus=100 alvo=ChkGob tipo=player MaxHealth=100 dano=10 (log:56)
  [OK]      Flame Shrine Aura    (dano/turno)           bonus=100 alvo=ChkGob tipo=Fodder MaxHealth=200 dano=56 (log:57)
  [OK]      Decay Shrine Aura    (dano/turno)           bonus=100 char=ChkDecay MaxHealth=233 dano=47 [tipo nao logado -> player 10%] (log:53)

-- ACEITE (total provado em jogo pelo dono; RV-19 §9.1/§10.5) --
  [OK]      Rogue Aura/DodgeChance bonus=100 char=ChkRA total=57 resto=17 (log:34)
  [OK]      Fury/DamageMod bonus=0        char=ChkF total=50  resto=25 (log:47)
  [OK]      Fury/DamageMod bonus=100      char=ChkF total=75  resto=25 (log:49)
  [OK]      Fury/DamageReduction bonus=0  char=ChkF total=-5  resto=20 (log:47)
  [OK]      Fury/DamageReduction bonus=100 char=ChkF total=-30 resto=20 (log:49)

-- ADITIVIDADE (resto = total - aura, tem de ser constante por personagem) --
  [OK]      char=ChkF DamageMod: resto=25 constante em 3 bonus
  [OK]      char=ChkRA DodgeChance: resto=17 constante em 3 bonus
  ... (10/10)

-- DUMP DO ROGUELIKEDEBUGGER --
  [OK]      Warrior Aura/DamageMod: base=20 conferida contra o dump do proprio jogo
  ... (10/10 pares aura/atributo; o Dwarven sai AUSENTE, `efeitos` vazio de proposito)

== RESULTADO ==
  OK=38  ACHADO=0  AUSENTE=0  NAO-VERIFICAVEL=3
  NAO EXERCITADOS: nenhum
  NAO VERIFICAVEIS pela ferramenta (nao bloqueiam o exit 0 - a prova e VISUAL): Dwarven Aura (bonus=0), (bonus=100), (bonus=20)
  OK: todos os casos EXERCITAVEIS da tabela bateram (3 caso(s) NAO VERIFICAVEL(is) por desenho).
exit 0
```

Três checagens **independentes** rodam na mesma passada: (a) a contribuição da aura contra a tabela
gerada; (b) a base contra o **dump do próprio jogo**; (c) o `resto` (total − aura) **constante** por
personagem/atributo — que é a prova de aditividade do RV-44 e pega o defeito descrito em RV-19 §9.1
(a linha mostrar o total como se fosse a aura).

---

## 4. CONTRA-PROVA — a ferramenta reprova quando tem de reprovar

Foi exatamente o contrário disso que deixou passar o falso OK do `check_patches`; por isso cada
prova abaixo é **literal**.

### CP-1 · erro plantado na LINHA DE LOG (Rogue, bônus +100: 40 → 41)

```
$ sed 's/...bonus=100 -> Dodge +40%.../...bonus=100 -> Dodge +41%.../' \
      tools/fixtures/shrines-exemplo.log > $TMP/erro-log.log
$ python tools/checa_shrines.py --log $TMP/erro-log.log
  Rogue Aura           bonus=0    OK       bonus=20   OK       bonus=100  ACHADO
  [ACHADO]  Rogue Aura           DodgeChance            bonus=100 char=ChkRA contrib=41 esperado=40 dif=+1 (log:34)
  [ACHADO]  char=ChkRA DodgeChance: resto varia entre 16, 17 (esperado constante)

== RESULTADO ==
  OK=37  ACHADO=2  AUSENTE=0  NAO-VERIFICAVEL=3
  REPROVADO por 2 achado(s):
    - Rogue Aura DodgeChance bonus=100: observado=41 esperado=40 dif=+1 (contribuicao das auras difere log:34)
    - (aditividade) DodgeChance bonus=todos: observado=16 esperado=16 dif=+0 (resto (total - aura) NAO e constante para ChkRA em DodgeChance log:32)
exit 1
```

Antes (a mesma fixture sem o `sed`): `OK=38 ACHADO=0 ... exit 0` (§3.2). **Antes/depois explícito:**
um byte trocado na linha 34 do log → 1 caso ACHADO com a diferença **+1** e o motivo; revertido →
volta a `exit 0`.

### CP-2 · erro plantado na TABELA DE ESPERADOS (Warrior, bônus 0: contribuição 20 → 21)

```
$ sed 's/^Warrior Aura,DamageMod,buff,20,docs\/cobertura\/status.csv:547,0,20,/...:547,0,21,/' \
      tools/dados/shrines-esperado.csv > $TMP/esperado-adulterado.csv
$ python tools/checa_shrines.py --log tools/fixtures/shrines-exemplo.log --esperado $TMP/esperado-adulterado.csv
  Warrior Aura         bonus=0    ACHADO   bonus=20   OK       bonus=100  OK
  [ACHADO]  Warrior Aura         DamageMod              bonus=0   char=ChkWA contrib=20 esperado=21 dif=-1 (log:23)

== RESULTADO ==
  OK=37  ACHADO=1  AUSENTE=0  NAO-VERIFICAVEL=3
  REPROVADO por 1 achado(s):
    - Warrior Aura DamageMod bonus=0: observado=20 esperado=21 dif=-1 (contribuicao das auras difere log:23)
exit 1
```

Só **aquele** caso reprova (precisão: os outros 37 continuam OK). E a tabela adulterada **de outra
forma** (mudar a `base` de 20 para 21) é pega pelo *cross-check* do dump:
`[ACHADO] Warrior Aura/DamageMod: base do dump=20 e esperado=21`.

### CP-3 · o GERADOR falha quando a fonte some (não chuta)

Coluna `efeitos` do Warrior esvaziada numa cópia do censo:

```
$ python tools/gera_shrines_esperado.py --status-csv $TMP/status-sem-warrior.csv
FALHA: a aura 'Warrior Aura' esta em AURAS_CSV mas a coluna `efeitos` do censo esta VAZIA na
linha 547 (docs/cobertura/status.csv) - a FONTE MUDOU. O censo e a fonte da base das 9 auras de
buff; o gerador FALHA em vez de chutar (se a coluna vazia for o novo normal dessa aura, ela passa
a ser lida do asset: AURAS_ASSET).
exit 1
```

### CP-4 · o GERADOR falha sem o `resources.assets`

```
$ python tools/gera_shrines_esperado.py --asset C:/nao/existe/resources.assets
FALHA(1): --asset aponta para um arquivo que NAO existe: C:/nao/existe/resources.assets
  -> sem a fonte, o gerador FALHA em vez de chutar.
exit 1
```

(E o caminho normal confere que nada mudou: `python tools/gera_shrines_esperado.py --check` →
`OK: a tabela versionada bate com as fontes (39 linhas de esperado, 12 percentuais).`)

---

## 5. Rotina mínima para o dono (o caminho mais curto em jogo)

**Preparo (uma vez por personagem testado):** usar o perfil que já tem o BetterTooltips
**recompilado** (o log de 30/09 19:59 é de um build anterior ao RV-44 — sem o rebuild a rodada sai
toda AUSENTE, §3.1).

**(A) Personagem sem bônus (caso `0`) — as 11 auras por hover:**

1. Entrar numa partida com **um personagem só** (evita ambiguidade de receptor no log).
2. Andar até **cada shrine** e, **parado dentro da área**, passar o mouse **uma vez** sobre o
   shrine: Warrior · Guardian · Conqueror · Rogue · Reaper · Seraph · Shaman · Energy Coil ·
   Goblin Battle Standard (Fury) · Dwarven Totem · Decay Shrine.
   - Nesse único hover saem: o número do shrine, a linha `Your active shrine auras:` (Rogue/Dodge,
     Fury/Damage+Damage taken…) e as linhas `RV-31 acumulado` / `RV-44 item` / `RV-44 soma`.
3. **Decay**: ficar **um turno inteiro** dentro da aura (o proc roda no **começo do turno do
   portador**, RV-19 §4.4) e passar o mouse depois — a linha do jogo ganha
   `(N damage per turn for you)` e o log grava `RV-34 linha do Decay: …`.
4. **Flame**: precisa de **inimigo atacando alguém que está dentro da aura** (o dano é do
   atacante, não de quem está parado — RV-19 §4.4) e um hover com alguém na área para o mod
   projetar os alvos (`RV-34 Flame alvo …`). Sem inimigo na área o log registra
   `RV-33 Flame sem alvo: ninguem com o status da aura vivo agora` — **isso não é reprovação**, é
   ausência declarada (a ferramenta mostra `AUSENTE`).
5. **Dwarven**: o número é chance de stun e **não existe atributo** para ler — não sai número no
   log. Fica `NAO-VER`: é leitura visual (a nota diz "Base 20% + bônus").

**(B) Caso `+20` (`Omnism II`, Chaos tier 2):** repetir o passo (A) com o personagem que tem
`Omnism II` (ela **substitui** a `Omnism I`; o total é 20, não 28 — RV-19 §3).

**(C) Caso `+100` (`Worship`, perk do Worshiper):** repetir o passo (A) com o personagem do perk.
O `Horn of Devotion` cobre +50/+100 pelo mesmo caminho (roll), mas **+50 não é um dos 3 casos** da
tabela — sai como AVISO ("caso não tabelado") e não como OK.

**(D) Fechar:** `python tools/checa_shrines.py` — verde (`exit 0`) só se **as 12 auras × 3 casos**
tiverem observação; o que faltar aparece na lista de `AUSENTE` e o exit é **3**.
Nas duas telas do dono (Fury sem/com `Worship`, Rogue com `Worship`) a ferramenta também confere o
**total** e o **resto** contra os prints de RV-19 §9.1/§10.5.

**O que a rotina NÃO cobre (dito, não maquiado):** o Dwarven (sem número no log); o `[0]`% do Decay
**isolado do dano** (o log imprime o dano por turno; a % só é isolável quando `MaxHealth = 100`);
o dano de **retorno** do Flame (se o bônus que multiplica é o do atacante ou o do portador — RV-19
§9(ii) continua sendo experiência em jogo); e os bônus `+8` e `+50`.

---

## 6. Limites da ferramenta (por escrito, como no cabeçalho do `check_patches`)

1. **A leitura visual final é do dono.** A ferramenta compara **números logados**; não lê a tela. Se
   o mod logar um número certo e desenhar outro (texto composto errado, bloco no lugar errado,
   `[0]` não substituído, cor/ordem), ela **não** percebe. Abrir o shrine uma vez e olhar continua
   sendo o último passo humano.
2. **As linhas `chave '…' -> resultado final` não servem de prova**: nelas o `[0]` ainda está no
   lugar (o pipeline de expressões roda depois do Localize). Não há, no log, o texto final resolvido.
3. **Dwarven é permanentemente `NAO-VER`** (não há atributo/número); o `[0]`% do Decay só é isolável
   com `MaxHealth = 100`; o **dano de retorno** do Flame não é medido por hover nenhum.
4. **A base do Dwarven, do Decay e do Flame não tem segunda fonte em log** — só o asset (o gerador
   cita o offset). O `cross-check` contra o dump do jogo cobre **só** as 9 auras de buff.
5. **A `linha do Decay` passou a logar `tipo=`** (CHK-1 §7.1, **aplicado em 01/10**): o esperado usa
   a % DO TIPO logado. Com log anterior ao conserto (campo ausente) o esperado cai na % de `player`
   (10%) e a linha do resultado **diz** isso (`[tipo nao logado -> player 10%]`).
6. **`RV-44 item` / `RV-44 soma` passaram a trazer `char=` e `bonus=`** (CHK-1 §7.2, **aplicado em
   01/10**): com os dois campos as linhas são **atribuíveis** e saem na seção `EVIDENCIA ATRIBUIDA`,
   com o caso ao lado. Sem os campos (log antigo) valem como AVISO, como antes. Quem ancora o caso
   em OK/ACHADO continua sendo a linha `RV-31 acumulado` (tem `char=`, `bonus=` e `auras=[…]`).
7. Só os **3 casos** da tabela (0/+20/+100): bônus +8 e +50 saem como AVISO.
8. Ela confere a fórmula do Flame **com `Source = Target` = o alvo projetado** (o que o mod loga);
   **não** prova de quem é o bônus no proc real (RV-19 §9(ii)).
9. Ela não confere as tabelas `TextFixes`/`TextAppends` nem o texto do jogo (isso é de outros
   gates).

---

## 7. RELATÓRIO — o que faltava no log

> **ATUALIZAÇÃO (01/10) — OS DOIS CONSERTOS DE §7.1/§7.2 FORAM APLICADOS** no
> `BetterTooltips/Patches/ShrineAuraPatch.cs`, e a ferramenta passou a CONSUMIR os campos novos
> (compatível com log anterior: os grupos são opcionais e o resultado diz quando está no formato
> antigo). A rodada que aplicou é a mesma do TX-1/`%%`/RV-45 (§7.3/§7.4). O texto original desta seção
> fica abaixo como registro do que foi medido, com o estado de cada item marcado.

A rodada que produziu este relatório travava "**NÃO edite o código de nenhum mod nesta rodada**". Ao construir o
comparador, dois campos se mostraram **insuficientes para uma conferência estrita**, e a regra
seguida foi: não inventar heurística frouxa, não mexer no mod, **marcar `AUSENTE` e relatar**.
O conserto sugerido veio pronto para virar tarefa (1 linha cada, sem tocar em fórmula nem em
texto de jogador) — **e foi o que a rodada seguinte fez**.

### 7.1 `RV-34 linha do Decay` — falta o **tipo de inimigo**

- Hoje: `RV-34 linha do Decay: <char> MaxHealth=… bonus=… -> '<linha>'`.
- O esperado do Decay depende da **% do tipo** (`player` 10% × vida × bônus). O campo existe na
  linha do Flame (`tipo=`) e **não** existe na do Decay.
- Consequência hoje: o comparador calcula com `player` (o único caminho pelo qual o mod resolve o
  receptor: o personagem em foco) e **diz isso na linha do resultado**
  (`[tipo nao logado -> player 10%]`), em vez de fingir que conferiu.
- Conserto sugerido (não aplicado): acrescentar ` tipo={TipoDoAlvo(naAura)}` ao `Marca` da linha do
  Decay (`BetterTooltips/Patches/ShrineAuraPatch.cs`, o `Marca($"RV-34 linha do Decay: …")`).
  Nenhuma fórmula e nenhum texto do jogador mudam.

**APLICADO (01/10).** O campo está na marca
(`RV-34 linha do Decay: <char> MaxHealth=… tipo=<tipo> bonus=… -> '<linha>'`) e o comparador usa a % **do
tipo logado**. Contra-prova medida com o próprio conferidor (fixture com o formato novo, 1 caso IA plantado
com `MaxHealth=100 tipo=Fodder bonus=20 dano=24`): com o campo → `[OK] … [tipo=Fodder 20%]`; **arrancando o
` tipo=Fodder` da mesma linha** (o formato antigo) → `[ACHADO] … esperado=12 ([tipo nao logado -> player 10%])
dif=+12`, exit 1. O campo é opcional no parser: log anterior ao conserto continua legível.

### 7.2 `RV-44 item` / `RV-44 soma` — faltam **`char=` e `bonus=`**

- Hoje: `RV-44 item 'DamageMod': aura=+25% total=+50% resto=+25% em [Fury]`.
- Sem `char=`/`bonus=` essas duas linhas **não são atribuíveis a um caso**; o comparador só as
  aceita como AVISO. Poderia ancorar nelas (elas são mais ricas: nomeiam o atributo e o valor por
  aura) se carregassem os dois campos.
- Conserto sugerido (não aplicado): acrescentar `char={receptor.CharacterName} bonus={BonusDoReceptor(receptor)}`
  aos dois `Marca` de `AcumuladoShrines`/`ContribuicaoDasAuras`.
- **Nota:** hoje isso **não bloqueia** a conferência — `RV-31 acumulado` (mesmo hover) carrega os
  dois campos e o valor por atributo, e é nele que o comparador se ancora.

**APLICADO (01/10).** As duas marcas ganharam os campos (nos itens eles entram antes do `em [auras…]`), e o
conferidor passou a mostrar a seção `EVIDENCIA ATRIBUIDA`, com o caso (`char=`, `bonus=`) ao lado de cada
linha — sem mudar quem ancora o OK/ACHADO (o `RV-31 acumulado`). Sem os campos (log anterior) vale o AVISO
antigo, com o mesmo texto. Contra-prova: fixture com `RV-44 soma 'DodgeChance' … char=ChkRA bonus=100` e
`RV-44 item 'DodgeChance' … char=ChkRA bonus=100` → `[EVID] caso char=ChkRA bonus=100: 2 linha(s) atribuida(s)`.

### 7.3 O que **não** é problema (verificado, não suposto)

- **Deduplicação**: o `Marca` do mod deduplica por conteúdo (cada linha sai uma vez por sessão) — o
  comparador não precisa contar repetições nem temer duplicidade.
- A ordem/rotulado dos itens (`Damage`, `Damage taken`, `Crit Chance`, `Dodge`, `Life Steal`,
  `Health per turn`, `Mana per turn`, `Mana Costs reduced by`) vem do `Format`/`TextDoEfeito` do
  mod e é **pinada** no parser: item fora desses rótulos **não** é adivinhado (sai como AVISO).
- O `−` de `ComSinal` é o U+2212 e o parser aceita U+2212 **e** ASCII `-` nos dois sinais.

### 7.4 ENCONTRADO (01/10) — o marcador saía com **DOIS sinais de porcentagem** (`+53.4%%`)

- **Sintoma (log real da partida do dono):**
  `RV-31 acumulado: … char=Raven bonus=100 -> Damage +50% (total +75%%); Crit Chance +40% (total +53.4%%)`.
  O dono vê na tela `(total +53.4%)` com **um** sinal: o marcador de log é que duplicava.
- **Causa (uma linha, no `AcumuladoShrines`):** o item era montado como
  `TextDoEfeito(…) + " (total " + TotalComSinal(nome, total) + "%)"` — e `TotalComSinal` **já devolve o
  `%`**. O literal `"%)"` acrescentava o segundo. Não é "format string": é um sinal a mais no literal.
  `LocalizePatch`/`Marca` não escapam nem colapsam `%` (varredura: nenhum `Replace("%%", …)` no mod nem
  no `Assembly-CSharp` decompilado), e não há normalização de `%` em lugar nenhum do pipeline de tooltip.
- **Por que importa para a conferência:** a linha do `RV-31 acumulado` é CONTRATO do comparador
  (`checa_shrines.py`, `RE_ITEM`), e o `%%` a quebra — foi assim que a rodada de 30/09 saiu **toda
  AUSENTE**: o `total=+35.6%%` do item do acumulado não casa com `\(total …%\)$`, o item cai em
  `nao_parseados` e nenhuma aura fecha. Um marcador diferente do que o jogador vê obrigaria a
  ferramenta a normalizar — exatamente a fragilidade que se quer eliminar.
- **Conserto aplicado na MESMA rodada** (`")` em vez de `"%)"`), junto com o do §7.5 — os dois são da
  mesma família (sinal/formato a mais na linha azul).
- **Nota de honestidade:** no CÓDIGO a mesma string (`efeito`) alimenta o log (`Marca`) e o tooltip, então
  o sinal a mais estava nos dois; o que é medível (e o que quebrou a ferramenta) é o LOG. Não há
  normalizador de `%` no pipeline (varrido no mod e no decompilado), então não se afirma que a tela tenha
  um mecanismo próprio — o que se garante, com o conserto, é que **log e tela emitem UM sinal**, que é o
  que o dono vê.

### 7.5 ENCONTRADO (01/10) — a linha azul mostrava **fração** onde o jogo mostra inteiro

- **Sintoma (print do dono):** `Crit Chance +40% (total +53.4%)` — o `+53.4%`; num caso anterior,
  `Crit Chance +38.7%`. O valor é o do motor e a fração É legítima (equipamento dá décimos de crit),
  mas a **exibição** divergia do próprio jogo, que mostra inteiro (`Crit chance increased by 54%`).
- **Convenção do jogo (decompilado `Assembly-CSharp.decompiled.cs`):**
  `InventoryManager.UpdateStats` l.125348-125356 →
  `component.text = GUIManager.instance.floatToText(Mathf.Ceil(character[atributoFinal]));`
  e `GUIManager.floatToText` (l.93303-93310) é `f.ToString()`. Isto é: **`Mathf.Ceil`, inteiro**. Há uma
  **segunda** convenção na tela de level up (`RoguelikeManager`, l.163759-163764:
  `…ToString("F0")`, arredonda ao par) — ela **não** se aplica: o número da linha azul é o da FICHA, e o
  `BetterStats` (aprovado) já aplica `Mathf.Ceil` nos dois lugares (l.179 e l.335).
- **Conserto:** `RV-45` no `ShrineAuraPatch` (`InteiroDoJogo` + `Format`/`ComSinal`/`TotalComSinal`/
  `TextDoEfeito`) — vale para a contribuição **e** para o total, em qualquer atributo fracionário
  (`CritChance`, `DodgeChance`, `ManaCostMod` do Energy etc.), com o `Ceil` aplicado ao valor **cru**
  (o `-53.4` da ficha sai `-53`, não `-54`). **Nenhuma fórmula mudou** (Decay segue `Round` sem `Max(1)`;
  Flame segue `Max(1, Round(…))`; o fator do `ShrineEffectBonus` segue vindo do interpretador do motor) —
  e as duas auras de perigo nem passam por esse formatador (os números delas são inteiros por construção,
  conferido: a fórmula do asset tem `Mathf.Round`).

---

## 8. Arquivos desta tarefa

| Arquivo | Papel |
|---|---|
| `tools/gera_shrines_esperado.py` | gerador da tabela (fontes + citação + FALHA sem fonte) |
| `tools/checa_shrines.py` | conferidor (log + dump; OK/ACHADO/AUSENTE/NAO-VER; cobertura) |
| `tools/dados/shrines-esperado.csv` | **gerado e versionado** — 13 pares aura/atributo × 3 casos |
| `tools/dados/shrines-percentuais.csv` | **gerado e versionado** — % por tipo (Decay/Flame) |
| `tools/fixtures/shrines-exemplo.log` | fixture **sintética** (rotulada) para a rodada de exemplo e a contra-prova |

`python tools/gera_shrines_esperado.py --check` e `python tools/checa_shrines.py` são os dois
comandos a rodar junto das travas de release.

---

## 9. Travas na mesma rodada (e um conserto ancilar)

Todas as travas pedidas ficaram **verdes** depois desta tarefa: `check_patches`, `check_versoes`,
`valida_pacotes`, `check_dupes`, `check_segredos`, `audita_docs` (e também `check_fix_keys`,
`check_notas_redundantes`, `check_chave_compartilhada --estrito`). Build de mod **não** foi mexido.

**Um conserto ancilar, fora do escopo dos shrines mas dentro de `tools/`** — `check_segredos.py`
estava **vermelho antes desta tarefa** (medido: `exit 1`) por um falso positivo do *motor genérico*
`tools/check_padroes_segredo.py`: ele aplicava o heurístico de **entropia** a arquivos **binários**
versionados (`docs/img/bettercombattext-icon-fonte.png`, `docs/img/roguelikedebugger-icon-fonte.png`
— arte de ícone de outra tarefa), e qualquer trecho de 32+ caracteres base64-like de um PNG tem alta
entropia **por natureza**. Conserto aplicado (3 linhas de comentário + separação texto/binário): o
heurístico de entropia roda **só em arquivos de texto**; os **formatos conhecidos** (`tss_`, `ghp_`,
chave PEM, …) continuam sendo procurados em **todos** os arquivos, binários inclusive — e a saída
passa a dizer quantos binários ficaram fora do heurístico, para não virar ponto cego.
Estado: `python tools/check_segredos.py` → `exit 0`.

Índice de docs atualizado junto (o `audita_docs` cobra os dois): `docs/README.md` — este relatório
entrou no índice de `cobertura/revisao/` e a contagem do título foi de 43 → **44** relatórios.
