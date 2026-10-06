# Pacote de conferência visual humana — RV-33 (dano real do Decay e do Flame na tooltip)

> **O que é este arquivo.** É o pacote que permite a **uma pessoa** fazer a conferência visual do
> `RV-33` **em uma sessão de jogo**, sem ler código: qual build está instalada (§0), as
> pré-condições (§1), o **checklist numerado** do Decay (§2), do Flame (§3) e da regressão visual
> (§4) — cada passo com o **RESULTADO ESPERADO explícito** (número/estado), para marcar **OK** ou
> reportar divergência —, a limitação conhecida (§5), a lista de divergências que viram **bug novo**
> com o log a capturar (§6) e as provas do que já está provado por execução (§7).
>
> **Irmãos deste arquivo:** `docs/CONFERENCIA-DONO-06-10.md` §4 (o roteiro único das conferências de
> shrine, incluindo o protocolo do **RV-49** §4.1, que entra na MESMA sessão) e
> `docs/CONFERENCIA-RV28-GLOBULES.md` (o mesmo formato, para o `RV-28`).
>
> **Cartões:** este pacote é o entregável do cartão `t_66a4486d`; o aceite é do **`t_a2a9cc39`**
> (RV-33). A decisão do fator de escala (`ShrineEffectBonus`) é do **`t_4a610a4e`** (RV-49), que
> segue **bloqueado** esperando a sua medição — e a medição dele sai na mesma sessão (§5.3).
>
> **Tempo:** ~5 min de preparação (§1) + a sessão. O Decay sai em qualquer run (só precisa do
> shrine); o Flame precisa de **inimigo atacando alguém que está na área** (o número é do atacante,
> não de quem está parado).

Data do pacote: **06/10/2026**. Módulo conferido: `BetterTooltips` **0.1.3**.

---

## 0. Rastreabilidade — qual artefato esta conferência julga

O julgamento é **do artefato instalado no perfil**, não da árvore de trabalho. A identidade dele é
por **sha256** (a árvore tem WIP de outras frentes e não está commitada):

| O quê | Valor | Como eu conferi |
|---|---|---|
| DLL instada no perfil | `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\BetterTooltips\BetterTooltips.dll` | — |
| sha256 da DLL do perfil | `6533f4368ec75c680caa2a3e51fbc1f2e74bed9f7b905d2ba055b890aee8ec7d` | `sha256sum` (06/10 16:07:20, 184.320 bytes) |
| sha256 da build `bin/Release/netstandard2.1` | **o mesmo** (`6533f436…`) | `sha256sum` — instalada byte-idêntica, `INFRA-1` |
| A DLL é posterior a TODOS os fontes | sim | `find BetterTooltips -name "*.cs" -newer <dll>` → **vazio** (a última edição é `LocalizePatch.cs`, 16:07:14, 6 s antes do link) |
| Fonte da DLL (pin por conteúdo) | `ShrineAuraPatch.cs` `ed839dc4…` · `LocalizePatch.cs` `a61987a4…` · `StatusSkillSynergyPatch.cs` `d59c5f0d…` · `Plugin.cs` `b2121fd6…` | `sha256sum` dos fontes |
| Base git | `91b8be4` + o commit **deste** pacote (`docs(RV-33): pacote de conferencia visual humana do Decay e do Flame`). A árvore tem WIP de outras frentes (**106** entradas em `git status --porcelain`) — **o commit NÃO identifica o artefato; o sha256 sim** | `git rev-parse HEAD` / `git status --porcelain` |

**Razão da auditoria (cartão `t_b62183cc`, 06/10):** a `6533f436…` é a DLL auditada — os dois
ganchos das tooltips de shrine passaram a ligar o parâmetro pelo **NOME do original** (eram `__2`,
posicional) e a nota bege do Decay deixou de afirmar de quem é o `ShrineEffectBonus`. Relatório
completo: `REPORT-t_b62183cc.md` (anexo do cartão).

> **Esta rodada NÃO recompilou nada, de propósito.** Recompilar produziria uma DLL nova (o dono
> edita os fontes em paralelo) e destruiria o vínculo auditado. O que foi feito aqui é a
> **reconferência**: DLL do perfil == build Release, nenhum fonte mais novo que a DLL, e os
> marcadores abaixo presentes **dentro** da DLL instalada.

### 0.1 O que a DLL instalada tem de novo (conferível pela própria pessoa)

Contagem de marcadores **dentro da DLL do perfil** (cada um deve dar **1**):

```bash
python - <<'PY'
import os
p = os.path.expandvars(r'%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\BetterTooltips\BetterTooltips.dll')
b = open(p, 'rb').read()
for m in ["the attacker's own", "In the aura now (raw damage it takes as the attacker",
          "damage per turn for you", "your own Max Health multiplied by the percentage shown"]:
    print(b.count(m.encode('utf-16-le')), '|', m)
PY
```

Esperado, nesta ordem: `1 the attacker's own` · `1 In the aura now (raw damage it takes as the
attacker` · `1 damage per turn for you` · `1 your own Max Health multiplied by the percentage
shown`. Qualquer `0` ⇒ a DLL do perfil **não** é a auditada (parar e avisar).

**Tudo isto é re-verificável por um comando** (nenhuma prova deste documento vive só na prosa):

```bash
python tools/checa_conferencia_rv33.py    # 40 checagens: sha256 do artefato, literais do pacote
                                          # no fonte e DENTRO da DLL, citações e os números do §2/§3
```

Ele sai `exit 0` só quando o pacote confere com o artefato instalado; se alguém editar uma frase
esperada aqui **sem** mexer no código (ou trocar a DLL), ele **reprova**. O que ele **não** prova:
runtime — a tela continua sendo humana (§7).

> **O log NÃO viu esta DLL ainda.** O `LogOutput.log` do perfil é de **06/10 15:34** e traz
> `patches Harmony aplicados (8/8 ganchos, 8 metodos de patch)` da build anterior; as marcas do
> `BetterTooltips` de shrine no log atual são **zero**. Ou seja: o §1 é a primeira vez que esta
> build carrega com o jogo e é o passo que a auditoria **não pôde** fazer offline.

---

## 1. Pré-condições (conferir antes de olhar tooltip)

| # | O que conferir | Como | **Esperado** | OK/NOK |
|---|---|---|---|---|
| 0.1 | O jogo abre **modado** | r2modman → **Start modded** (o `.exe` direto roda vanilla) | abre com os mods | ☐ |
| 0.2 | O BetterTooltips carregou | `LogOutput.log`: procurar `Better Tooltips carregado.` | a linha existe | ☐ |
| 0.3 | Os ganchos Harmony entraram | mesma busca: `BetterTooltips: patches Harmony aplicados (` | **`(8/8 ganchos, 8 metodos de patch).`** — e **nenhuma** linha `GANCHOS QUE FALHARAM` | ☐ |
| 0.4 | Onde está o log | `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\LogOutput.log` | — (**truncado a cada boot**: vale só a sessão atual) | ☐ |
| 0.5 | Os tooltips de ground effect estão ligados | Options → Gameplay → a opção de tooltip de ground effect (a mesma que esconde a descrição de barris) | **ligada** (é o padrão; desligada, o tooltip do shrine não aparece) | ☐ |
| 0.6 | A DLL é a auditada (opcional) | o one-liner do §0.1 | quatro `1`s | ☐ |
| 0.7 | O **receptor** do número | — | No **tooltip do shrine o número é do personagem SELECIONADO** (RV-50: o hover do ground effect ignora o personagem sob o cursor). **Selecione** o personagem cuja vida você quer ler, e só depois passe o mouse no shrine | ☐ |
| 0.8 | Personagem de referência | — | Um personagem da run com **MaxHealth = 100** (dá para chegar equipando/desequipando) e, para o passo D3, um de **250** (ou o mesmo levado a 250) | ☐ |
| 0.9 | Um **Flame Shrine** à mão | — | Precisa de **inimigos** dentro da área (o número é do atacante). Um **Decay Shrine** basta para os passos D* | ☐ |

**Sobre o 8/8:** foi medido no artefato instalado com a MESMA regra do `Plugin.cs` (tipo com
`[HarmonyPatch]`): são **8 classes de gancho** e 10 métodos de patch nelas —
`LocalizePatch`, `CorEOrdemDoTooltip`, `SemNotaNoFeedDeTexto`, `SemNotaNoTextoFlutuanteDeCombate`,
`LocalizePassivaInimigo`, `UniversalTooltipPassivaInimigo`, `ShrineAuraPatch`,
`StatusSkillSynergyPatch`. O segundo número do log é o de **métodos-alvo patcheados**; a build
anterior imprimia `8`. O relatório da auditoria escreveu "10/10 ganchos" — 10 é o número de
**métodos**, não de ganchos. **O que vale como aceite é `8/8` + ausência de `GANCHOS QUE FALHARAM`**;
se o segundo número vier diferente mas o primeiro for `8/8` e não houver falha, **anote na
observação** (não é NOK por si).

---

## 2. CHECKLIST — DECAY (dano por turno numérico)

Fórmula, provada byte a byte no asset e avaliada pelo interpretador do próprio jogo
(`ShrineAuraPatch.cs:961-970`): **`N = Mathf.Round(MaxHealth × % do tipo)`**, sem `Mathf.Max(1,…)`.
Para um personagem não-IA a % é **10%** (`player`, o 6º argumento de `GetValueByEnemyType`).

| # | Ação na tela | **Resultado esperado (explícito)** | OK/NOK | Observação |
|---|---|---|---|---|
| **D1** | **Selecione** o personagem de **100 de MaxHealth** e passe o mouse no **Decay Shrine** (parado dentro ou fora da área — o número sai igual) | Linha branca: **`Take 10% of your Max Health in Shadow Damage per turn (10 damage per turn for you).`** — o `(10 damage per turn for you)` é o número | ☐ | |
| **D2** | Ler o bloco **bege** logo abaixo | Exatamente: **`Raw damage, before damage reduction: your own Max Health multiplied by the percentage shown; the damage can be 0.`** — e **NÃO** deve citar `Shrine Effect Bonus` nem de quem ele é (é a correção da auditoria) | ☐ | |
| **D3** | Equipar/desequipar (ou power-up) até **250 de MaxHealth** → novo hover | Linha branca passa a **`… (25 damage per turn for you).`** (25 = Round(250 × 10%)) | ☐ | vida antes/depois: ____ / ____ |
| **D4** | Um terceiro valor qualquer de vida (ex.: 233 ou 40) → novo hover | **`N = Round(MaxHealth × 10%)`**: 233 → **23**; 40 → **4**; 100 → **10**; 250 → **25** | ☐ | visto: ____ |
| **D5** | Vida **muito baixa** (ex.: 4 ou 5) → novo hover | **0 é resultado legítimo** (o Decay não tem `Max(1)`): 4 → **`(0 damage per turn for you)`**. Aceitável: 0, 1 ou 2, desde que bata com `Round(MaxHealth × 10%)` | ☐ | visto: ____ |
| **D6** | **Parado DENTRO da aura**, passar **um turno** (o proc roda no começo do turno de quem tem a aura) e reabrir o hover | Nada muda no número; a **linha azul** do RV-31 deve aparecer por último: **`Your active shrine auras: Shadow damage per turn 10.`** (mesmo N da linha branca) — e o dano real recebido na tela é do **RV-49** (§5.3) | ☐ | |
| **D7** | Sair da aura e reabrir o hover | A **linha branca e a nota bege continuam** (o número não depende de estar na aura — é a vida máxima do selecionado); a **linha azul some** se nenhuma aura de shrine estiver viva | ☐ | |

> ⚠ **Dois números na mesma linha, e isso é esperado.** O `10%` da frase é a **escala do próprio
> shrine** e **não muda** (o mod não reescreve esse `[0]`, RV-30); o número **entre parênteses** é
> **10% da SUA vida máxima**. Com 250 de vida a linha fica `Take 10% … (25 damage per turn for you).`
> — a diferença entre o `10%` e o `25` **não é defeito**, é a leitura de duas grandezas diferentes.
> O `[0]` no texto **nunca** pode aparecer literal na tela (o motor o substitui por `10`).

---

## 3. CHECKLIST — FLAME (dano em quem ataca)

Decisão da tarefa 1 (`t_d02f9212`, opção **(a)**): **um número por personagem que está na área**,
cada um **projetado como o atacante**, e a legenda **nomeando de quem é a vida máxima**. A escala
por tipo **não** entra na tooltip (decisão do dono, TX-1: "tooltip não é lugar de tabela") — ela é
conferida pelo log (§3.F3) e vive em `docs/cobertura/revisao/RV-19-shrines.md` §4.3.

Fórmula (`ShrineAuraPatch.cs:929-939`): **`N = Mathf.Max(1, Mathf.Round(MaxHealth_do_listado × % do tipo DELE))`**.

| # | Ação na tela | **Resultado esperado (explícito)** | OK/NOK | Observação |
|---|---|---|---|---|
| **F1** | Com **alguém na área da aura** (party ou inimigo), passar o mouse no **Flame Shrine** | Linha branca: **`Attackers take Fire Damage.`** (sem número — o número do Flame **não** entra na linha original) | ☐ | |
| **F2** | Ler o **começo** do bloco bege | **`In the aura now (raw damage it takes as the attacker, from the attacker's own Max Health): <nome> <N>[; <nome2> <N2>…].`** — um item por personagem na área, separados por `; ` | ☐ | quantos nomes apareceram: ____ |
| **F3** | Conferir a **legenda** (o resto do mesmo bloco bege) | Exatamente: **`The attacker takes this damage in return, based on its own Max Health and not on the health of the one it attacked, before damage reduction.`** — a legenda diz **explicitamente** que a vida máxima é a **do atacante** (`the attacker's own Max Health`), e **não** cita `Shrine Effect Bonus` | ☐ | |
| **F4** | Conferir cada número `N` da lista | **`N = Max(1, Round(MaxHealth_do_listado × % do TIPO DELE))`** — `player` **5%** · `soldier` **12%** · `elite` **10%** · `champion` **8%** · `fodder` **14%** · `boss` **2,5%**. Exemplos: player 100 → **5**; player 200 → **10**; fodder 200 → **28**; soldier 100 → **12**; champion 100 → **8**; boss 400 → **10** | ☐ | nome/vida/tipo/N visto: |
| **F5** | **Parado DENTRO** da aura, reabrir o hover | A **linha azul** do RV-31 (por último) deve trazer o item próprio do Flame: **`Fire damage to attackers: <nome> <N>, <nome2> <N2>`** — os mesmos números da lista bege | ☐ | |
| **F6** | Ninguém com o status da aura vivo → hover | **Nenhum número**: só `Attackers take Fire Damage.` + a nota bege. **Não é falha** (ausência declarada): o log grava `RV-33 Flame sem alvo: ninguem com o status da aura vivo agora (nenhum numero)` | ☐ | |
| **F7** | Um **aliado** atacado por inimigo dentro da aura (se der) | A lista pode conter **o aliado e os inimigos**; cada número segue a **% do tipo de quem está listado**, nunca a sua | ☐ | |

> A **escala por tipo (2,5 / 8 / 10 / 12 / 14 / 5)** **não aparece na tela** — por decisão do dono
> (TX-1). O que se confere em tela é que cada `N` bate com a % do tipo daquele personagem; quem diz
> o tipo sem ambiguidade é o log (`tipo=` em §6). Tabela gerada do asset:
> `tools/dados/shrines-percentuais.csv`.

---

## 4. CHECKLIST — REGRESSÃO VISUAL (RV-31 + nota bege)

Nada disto foi tocado por esta rodada (auditoria `t_b62183cc`, §(c)-5-iii): a linha azul vem de
`CorDaLinhaDeAuras()`/`MarcadorLinhaDeAuras` (`ShrineAuraPatch.cs:1226`, `:1254`, `:1422-1423`) e a
nota bege de `MarcadorCorDeExplicacao` (`LocalizePatch.cs:426`) — mesmos hex, mesma ordem, mesma
posição. **É o que se confere aqui.**

| # | O que olhar | **Resultado esperado (explícito)** | OK/NOK | Observação |
|---|---|---|---|---|
| **R1** | A **ordem dos blocos** no tooltip do shrine | Título → **linha branca do jogo** → (linha em branco) **bloco bege** → (linha em branco) **linha azul por ÚLTIMO** | ☐ | |
| **R2** | As **cores** | Bloco bege **`#C8B090`**; linha azul na cor da paleta do jogo — **`#00D7FF`** (lida de `Tooltip.skillStatusColor`, registrada no log) | ☐ | |
| **R3** | O **formato** dos itens da linha azul | Auras de **atributo** (ex.: Warrior/Rogue) seguem `Damage +20% (total +50%)` / `Dodge +40% (total +57%)` (RV-44); as **sem atributo** são `Shadow damage per turn N` (Decay), `Fire damage to attackers: …` (Flame), `Stun chance +40%` (Dwarven) | ☐ | |
| **R4** | O resto do tooltip | Título, a descrição do ground effect e `Turns Remaining: N` **intactos**; nenhuma nota mudou de cor ou de lugar | ☐ | |
| **R5** | A lista do Flame **não** virou um bloco novo | Ela está **dentro do MESMO bloco bege** (antes da frase `The attacker takes this damage in return…`), não como bloco separado | ☐ | |

---

## 5. LIMITAÇÕES CONHECIDAS (não são defeito — nada a corrigir)

### 5.1 O dano exato que um inimigo específico levará NÃO pode ser exibido no hover (Flame)
No hover **ninguém sabe quem vai atacar**: a fórmula roda no atacante, e o atacante é escolhido pelo
jogo no momento do golpe. O que a tooltip pode dar é **um número por personagem que está na área,
cada um projetado como o atacante** (a decisão (a) da tarefa 1) — e é isso que ela dá. **Limitação do
JOGO, não do mod**; registrado no cabeçalho de `ShrineAuraPatch.cs:694-705`.
→ **Ação:** marcar ☐ aqui **confirmando que você entendeu e viu isso**; se a tela prometer um número
único e exato de dano por inimigo, **isso sim** é achado (ver §6/B3).

### 5.2 O `[0]%` da frase do Decay é a escala do SHRINE e não muda
Com 250 de vida: `Take 10% … (25 damage per turn for you).` — `10%` é a escala do shrine (o mod não
reescreve esse `[0]`, RV-30) e `25` é 10% da **sua** vida máxima. Ver o aviso do §2.

### 5.3 O número exibido NÃO inclui o `ShrineEffectBonus` (pendência do RV-49)
Os números do Decay/Flame mostrados **hoje** saem da constante **sem** o fator `(1 + ShrineEffectBonus/100)`
(RV-30 · `tools/testes/regras_rv30.py`). A evidência de 06/10 mostra que, **no caminho do dano**, o
`Source` é o personagem que **tem** a aura — ou seja o dano real **pode** ser ~2× o número exibido
quando você tem `Horn of Devotion` (+100). **Enquanto o RV-49 não medir, isso é o desenho aceito e
documentado** — divergir aqui **não** é bug do RV-33: é a medição do `t_4a610a4e`
(protocolo: `docs/CONFERENCIA-DONO-06-10.md` §4.1). Anote os dois números (o da tela e o dano real)
e cole no cartão do RV-49.

### 5.4 O número só sai quando há receptor legível
Sem personagem selecionado/válido (ou com `MaxHealth ≤ 0`), **a linha do jogo fica intacta** e o log
grava o motivo (`RV-33 Decay sem numero: nenhum receptor…` / `… receptor sem MaxHealth`). Em telas
fora do combate o número pode não aparecer — **declarado**, não defeito.

---

## 6. ONDE UMA DIVERGÊNCIA VIRA **BUG NOVO** (com o log a capturar)

Regra: **o número que a tooltip mostra tem de sair de `MaxHealth` × a % do tipo, e o log tem de
dizer o motivo quando ele não sai.** Divergência = cartão novo no `BetterTooltips`, com o **texto
literal visto na tela** × o esperado e o **trecho do log** colado.

Log do perfil (truncado a cada boot — **copie antes de reiniciar o jogo**):
`%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\LogOutput.log`

```bash
grep -a "Shrine RV-23\|Shrine RV-33\|Shrine RV-34\|Shrine RV-46\|Shrine RV-50\|Shrine RV-31\|Shrine RV-44\|Shrine RV-22\|Shrine MAN-2" \
  "$APPDATA/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log"
```

| # | Sintoma na tela | Esperado (resumo) | O que capturar no log | Vira |
|---|---|---|---|---|
| **B1** | Decay **sem** `(N damage per turn for you)` com um personagem selecionado e vivo | o número sai sempre | `RV-33 Decay sem numero: …` · `RV-34 Decay sem numero: formula e % nao avaliadas pelo interpretador` · `RV-34 Decay reserva: …` | bug novo |
| **B2** | Decay com `N` ≠ `Round(MaxHealth × 10%)` | ver D4/D5 | `RV-34 linha do Decay: <char> MaxHealth=… tipo=… bonus=… -> '<linha>'` (tem **tudo**: vida, tipo, bônus e a linha montada) | bug novo |
| **B3** | Decay com **`1` forçado** onde a conta dá `0` | 0 é legítimo (sem `Mathf.Max(1,`) | a mesma linha `RV-34 linha do Decay: …` | bug novo |
| **B4** | Flame **sem a lista** com alguém na área | lista sempre | `RV-33 Flame sem alvo: …` (só vale se **ninguém** estava na área) · `RV-34 Flame alvo '<nome>' sem numero: formula nao avaliada` · `[Shrine RV-33] alvos do Flame falharam (texto intacto): …` | bug novo |
| **B5** | Um `N` do Flame ≠ `Max(1, Round(MaxHealth × % do tipo DELE))` | ver F4 | `RV-34 Flame alvo '<nome>': MaxHealth=… tipo=… bonus=… dano=…` · `RV-46 item do Flame alvo '<nome>': …` — o `tipo=` é o que fecha a % | bug novo |
| **B6** | A linha azul **não traz** o item quando a aura está viva | nenhuma aura sai em silêncio | `RV-46 AVISO: a aura viva '<nome>' NAO virou item da linha (<motivo>)` · `RV-46 item sem atributo: '<nome>' -> '<item>'` · `RV-31 acumulado: auras=[…] …` | bug novo |
| **B7** | Linha azul **fora do lugar** (não é a última) ou **com outra cor** | §4 (R1/R2) | `BetterTooltips: cor da linha de auras ativas = #…` · `BetterTooltips: azul da paleta lido em <campo> = #…` · `BetterTooltips: nenhuma cor azul da paleta … (niveis 2 e 3 COLAPSARAM)` | bug novo |
| **B8** | Nota bege do Decay citando `Shrine Effect Bonus` (ou dono dele) / texto do Flame diferente de F3 | §0/§2 D2/§3 F3 | o texto visto (não há marca de log para nota) + `BetterTooltips: explicação adicionada a '<chave>'` | bug novo |
| **B9** | **`[0]`** literal na tela na linha do Decay | o motor substitui por `10` | `RV-34 linha do Decay: …` (a linha montada preserva o `[0]` de propósito — a substituição é do motor) | bug novo (motor) |
| **B10** | Menos de `8/8` ganchos ou qualquer `GANCHOS QUE FALHARAM` | §1.0.3 | o bloco de boot inteiro (`BetterTooltips: gancho aplicado — …` / `FALHA ao aplicar o gancho …`) | bug novo |
| **B11** | O log mostra um número e a **tela mostra outro** | os dois iguais | `RV-34 …` + `RV-46 …` + **print** da tooltip (a ferramenta mecânica não lê tela — §7.4) | bug novo |
| **B12** | Qualquer `NullReferenceException`/trava ao abrir a tooltip de shrine | nunca | `Player.log` (`%LOCALAPPDATA%Low\Burst2Flame Entertainment\Stolen Realm\Player.log`) + a pilha | bug novo (é a família do incidente do `__3`) |
| **B13** | O **número baixa mas o dano real é ~2× (ou igual) com `Horn of Devotion`** | esperado (§5.3) | `RV-34 linha do Decay: … bonus=100 …` / `RV-46 item do Flame alvo … bonus=100 …` + o dano de tela | **não é bug** — é a medição do **RV-49** (`t_4a610a4e`) |
| **B14** | Um aura de shrine some da linha azul depois de sair/voltar na área | RV-46 conta cada aura **1×** (a instância repetida vai só ao log) | `RV-46 instancias repetidas na lista viva de <char>: [<aura> xN]` | anotar (pode ser o teto do atributo, não defeito) |

**Motivos registrados quando o cálculo falha** (é a prova de que o mod preferiu não inventar número —
em qualquer um deles a **linha do jogo fica intacta**): `RV-33 Decay sem numero: nenhum receptor
(personagem em foco) disponivel` · `RV-33 Decay sem numero: receptor sem MaxHealth` · `RV-34 Decay
sem numero: formula e % nao avaliadas pelo interpretador` · `RV-34 Decay reserva: … SEM bonus de
personagem (RV-30)` · `RV-33 Flame sem alvo: ninguem com o status da aura vivo agora (nenhum
numero)` · `RV-34 Flame alvo '<nome>' sem numero: formula nao avaliada` · `[Shrine RV-33] alvos do
Flame falharam (texto intacto): <Tipo>: <msg>` · `[Shrine RV-33] valor do Decay falhou (linha
intacta): <Tipo>: <msg>` · `[Shrine RV-33] varredura de alvos falhou (<Tipo>): <msg>` · `RV-34 fator
do ShrineEffectBonus NAO aplicado: atributo ausente neste build`.

---

## 7. Referências de prova (o que já está provado, e onde)

| Afirmação | Prova |
|---|---|
| A DLL do perfil é a build auditada, posterior a todos os fontes | sha256 `6533f436…` nas duas pontas + `find -newer` vazio (§0) |
| São **8** classes de gancho (8/8) | medido no artefato instalado com a regra do `Plugin.cs:123` (tipo com `[HarmonyPatch]`); o resumo da falha está em `Plugin.cs:100-110` |
| Fórmula do **Decay** = RHS do asset, sem `Mathf.Max(1,` | `ShrineAuraPatch.cs:961-970`; asset `resources.assets@1519519282` (len 171) |
| Fórmula do **Flame** = RHS do asset, com `Mathf.Max(1,` | `ShrineAuraPatch.cs:929-939`; asset `resources.assets@1519546098` (len 187) |
| A linha branca do Decay recebe o número **antes do ponto** e preserva o `[0]` | `ShrineAuraPatch.cs:1042-1109` (montagem em `:1092-1093`); substituição em `LocalizePatch.cs:2782-2789` |
| A lista do Flame entra no **começo do bloco bege** (mesmo bloco) | `ShrineAuraPatch.cs:777-846`; inserção em `LocalizePatch.cs:2759-2775` |
| A legenda do Flame nomeia o dono da vida máxima e **não** cita o `ShrineEffectBonus` | `ShrineAuraPatch.cs:833-839` |
| A nota bege do Decay **não** afirma de quem é o fator | `LocalizePatch.cs:1391-1392` (+ comentário da correção em `:1382-1390`) |
| Itens da linha azul sem atributo: `Shadow damage per turn N` · `Fire damage to attackers: …` | `ShrineAuraPatch.cs:1968-2037` (`:2001` e `:2036`); rótulos em `:2078-2090` |
| A linha azul é montada por último, na cor da paleta | `ShrineAuraPatch.cs:1226` (marcador), `:1422-1423` (bloco); cor em `LocalizePatch.cs:608-660` (`#00D7FF` nas sessões de 01/10) |
| O receptor do tooltip do shrine é o personagem **selecionado** | `ShrineAuraPatch.cs:561-621` e `:688-691` (RV-50) |
| O número do Decay ignora o bônus do personagem (RV-30) | `ShrineAuraPatch.cs:1973-2001` (sem fator, `Source = null`); regra cobrada por `tools/testes/regras_rv30.py` |
| Percentuais por tipo (Decay 5/10/12/15/20/10 · Flame 2,5/8/10/12/14/5) | `tools/dados/shrines-percentuais.csv` (gerado do asset por `tools/gera_shrines_esperado.py`) |
| Formatos observados em log real (linha do Decay, itens do Flame/Decay, linha azul) | `tools/fixtures/shrines-rv46-dedupe.log:67-74`, `:94-98` |
| A auditoria de Harmony/chaves desta build | `REPORT-t_b62183cc.md` (anexo do cartão `t_b62183cc`): 0 parâmetro posicional, 0 chave duplicada/nas duas tabelas, 0 chave nova, suíte pura 91/91, contra-prova 50/50, cenários de shrine 28/28 |
| **Este pacote** confere com o artefato (sha256, literais no fonte e na DLL, citações e os números do §2/§3) | `python tools/checa_conferencia_rv33.py` — **40 PASSOU / exit 0** (06/10). Contra-prova: uma cópia do documento com uma frase esperada alterada → **REPROVOU / exit 1** |

### 7.4 Conferência mecânica (opcional, depois da sessão)
O jogo **loga o que renderiza**, e há um comparador que lê o log contra as tabelas geradas do asset
(ausência **nunca** vira aprovação):

```bash
python tools/gera_shrines_esperado.py --check   # a tabela versionada == o que as fontes geram
python tools/checa_shrines.py                   # log do perfil × tabelas (exit 0 = tudo com observação)
python tools/checa_shrines.py --so-cobertura     # o que NÃO foi exercitado
```

Ele **não substitui** esta conferência: **não lê a tela** — texto composto errado, `[0]` não
substituído, bloco no lugar errado ou cor trocada passam batido nele (limites em
`docs/cobertura/revisao/CHK-1-shrines-conferencia-mecanica.md` §6).

---

## 8. Depois da sessão

1. Marcar **OK** ou anotar a divergência em cada linha (§2 D1-D7, §3 F1-F7, §4 R1-R5, §5 ☐).
2. Comentar o resultado no cartão **`t_a2a9cc39`** (RV-33), com: passos por onde passou, os números
   vistos (vida → N exibido), o trecho do log e **qualquer divergência com o texto visto × esperado**.
3. Divergência = **achado**: descreva o que a tooltip mostrou **literalmente** — vira cartão novo do
   `BetterTooltips` (§6) já com o log colado.
4. **RV-49** (§5.3): os números de **tela × dano real**, com e sem `Horn of Devotion` (+100), vão no
   cartão **`t_4a610a4e`** — é essa a medição que fecha a decisão do fator. O roteiro está em
   `docs/CONFERENCIA-DONO-06-10.md` §4.1; o probe já instalado grava `[FlameRV49]` (o log desta
   sessão tem, hoje, **140 linhas de BOOT e ZERO de PROC** — o proc real nunca disparou).
5. Se algum passo **não deu para ver** (nenhum shrine do tipo na run, nenhum inimigo na aura), marque
   `nao visto` e diga quantas tentativas fez — **não** invente resultado.

## 9. Limites deste pacote

1. **Não é prova de runtime por si só.** O que está provado por execução: a DLL é a auditada
   (§0), os literais esperados existem **dentro** da DLL (§0.1), a fórmula vem do asset, a suíte e os
   cenários passam (§7). O **número na tela** é o que esta conferência produz — e o log do perfil tem
   **zero** marcas de shrine do `BetterTooltips`, porque o processo desta build nunca rodou com o jogo.
2. **Não cobre a decisão do fator** (§5.3) nem a publicação (`PUB-1`).
3. **Não diz onde achar o shrine na run.** Os shrines são ground effects do mapa; se o da vez não
   aparecer na sessão, registre `nao visto` (não é reprovação) — a existência e o texto deles estão
   provados no asset (§7).
4. **A leitura da tela é humana por definição:** o comparador mecânico confere números logados, não
   pixels nem ordem de blocos.
