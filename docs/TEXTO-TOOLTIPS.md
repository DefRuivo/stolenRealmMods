# Convenção de TEXTO e COR das tooltips (padrão do projeto)

Este é o documento de **TEXTO** da família do [`PROCESSO-REVISAO.md`](PROCESSO-REVISAO.md):
aquele diz *como* uma entrega é revisada (revisor independente, prova, travas); este diz
**como o texto de uma tooltip é montado e colorido**, para que qualquer frente futura siga
sem perguntar. Decisão do dono, 01/10/2026, na ordem exata dele.

**Regra que manda aqui (e vale para qualquer cor nova):** *cor sem procedência é número
inventado.* Nenhum `<color=#RRGGBB>` entra no código por escolha estética. Cada cor sai de
**um campo de cor do próprio jogo** lido em runtime, ou é uma **decisão datada do dono
registrada neste documento**. Não existe terceira opção.

---

## 1. Os três níveis (ordem do dono)

| Nível | O que entra | Quem escreve o texto | Cor | Fonte da cor (declarada) |
|---|---|---|---|---|
| **1. BRANCO** (padrão do jogo) | A **descrição curta** da skill/status/item, com os **valores dinâmicos por personagem** (Omnism/Horn nas auras de shrine; no Flame e no Decay, a **% da vida do personagem** como dano). | **O jogo.** O mod só corrige o que mente (grafia, termo, número) — nunca reescreve por estilo. | A cor padrão do corpo do tooltip: **nenhum `<color>` nosso** é aplicado. | O próprio tooltip do jogo: o texto vai para `Description.text` sem tag (`Tooltip.ShowTooltip`, bancada `scratch/rv22/tooltip.cs:597`). Os realces *dentro* da linha branca também são do jogo: `{STA=}`/`@atributo@` → `Tooltip.specialTextColor` (bancada `scratch/rv22/tooltip.cs:608`/`634`/`644` — a cor sai do campo na `608`; aplicada ao `{STA=}` na `634` e ao `@atributo@` na `644`), `[N]` (expressão) → literal **`#CBB396`** do motor (43 usos no Assembly). |
| **2. TOM MAIS ESCURO** | **Explicação de TERMOS e de CÁLCULOS**: glossário (`Stealth`, `Enrage`, `Life Steal`, `Marked Prey`), efeitos por ponto de atributo, ordem da redução de dano, mitigação de Armor/Resistência, a base das auras de shrine ("Base 20%; …") e as notas de stack/duração. | O mod (a nota **acrescenta**; não substitui a descrição do nível 1). | **`Tooltip.specialDescColor`** — o campo do prefab que o próprio jogo usa para os blocos de descrição anexados (o par `specialTitleColor`+`specialDescColor` do bloco `Special` do item, bancada `scratch/rv22/tooltip.cs:1854-1855`/`1950-1951`). | `Tooltip.specialDescColor` (campo do prefab em `GUIManager.tooltip`), lido em runtime. Marcador nas tabelas: **`#C8B090`** — o valor medido por pixel no bloco do jogo em 29/09 (BT-9c), usado só para o texto continuar legível se a leitura falhar. |
| **3. AZUL** | **Estado agregado do personagem**: (a) o acúmulo das **auras de shrine** do jogador — `Your active shrine auras: …`; (b) **efeitos provenientes de skills** — `Your skills on this status: …` (o caso do **Frost Bite**, CHL-1). | O mod, sempre a partir do **motor** (expressão do próprio asset avaliada pelo interpretador do jogo); nunca número escrito à mão. | **`Tooltip.skillStatusColor`** — o campo que o próprio jogo usa, no tooltip, para os **blocos de status anexados** (nome + descrição, bancada `scratch/rv22/tooltip.cs:656`/`686`); é o análogo exato de "texto sobre o ESTADO do personagem". | `Tooltip.skillStatusColor`, com os azuis da paleta da HUD como reserva: `GUIManager.coldColor` (cor do dano Cold) e `GUIManager.manaColor` (cor de Mana) — `scratch/sac1/GUIManager.cs:242`/`250`. Só entra cor aprovada pelos testes de azul (`EhAzul`). |

> **Elo contestado — ver §7.5.** A coluna "Fonte da cor (declarada)" do nível 3 declara
> `Tooltip.skillStatusColor`, mas a leitura datada do prefab (01/10) mostra que esse campo é
> **bege**, não azul — a fonte declarada **não se sustenta** e o azul do nível 3 vem da paleta
> da HUD (`GUIManager.coldColor`). Ler §7.5 antes de usar esta tabela como prova da coluna.

**A diferença entre 2 e 3 é o que o bloco É, não o gosto:** nível 2 explica a *mecânica* da
skill/status que a tooltip descreve; nível 3 mostra o *estado do personagem* (as auras que ele
está recebendo agora, as skills dele que mexem no status). A origem da cor é o que o próprio
jogo usa para cada uma dessas duas coisas.

---

## 2. Procedência de cada cor (nenhuma escolhida a dedo)

| Nível | Hex no código | Campo do jogo | Onde o jogo usa o campo | Como o mod resolve |
|---|---|---|---|---|
| 1 | — (nenhum) | — | corpo do tooltip, sem tag | não coloriza; deixa o texto do jogo passar |
| 1 (realces) | `#CBB396` (literal do motor) e `{STA=}`/`@…@` | literal + `Tooltip.specialTextColor` | `[N]` das expressões; nomes de status/atributo inline | não tocamos — é o jogo |
| 2 | `#C8B090` → (runtime) `specialDescColor` | `Tooltip.specialDescColor` | bloco `Special` (título + descrição) do tooltip de item | `ComACorDoJogo()` troca o marcador pela cor lida; se a leitura falhar, o marcador fica (hex válido) e o log avisa |
| 3 | `#C8B090` **só como último recurso** → (runtime) `skillStatusColor` / `coldColor` / `manaColor` | `Tooltip.skillStatusColor`, `GUIManager.coldColor`, `GUIManager.manaColor` | blocos de status anexados ao tooltip; cor do dano Cold; cor de Mana | `CorDaLinhaDeAuras()`: primeiro campo azul aprovado (`EhAzul`), na ordem acima; sem nenhum, cai no marcador e **loga o colapso** |

> **Elo contestado — ver §7.5.** O "elo 1" declarado do nível 3 (`Tooltip.skillStatusColor`) é
> **elo morto** nesta build: o campo é bege e nunca passa no `EhAzul`; o azul em uso é o elo 2
> (`GUIManager.coldColor`, `#00D7FF`). A fonte declarada do nível 3 **não se sustenta** — ler
> §7.5 antes de citar a coluna "Campo do jogo" do nível 3 como prova.

O `EhAzul` é a **sanidade**, não estética: se o build mudar o campo para um tom bege, a linha
do nível 3 não vira uma cópia silenciosa do nível 2 — ela passa para o próximo elo azul da
paleta. Se nenhum elo for azul, o log diz explicitamente que **os níveis 2 e 3 colapsaram**.

---

## 3. Exemplos reais (tirados das tooltips de hoje)

**A fronteira, explícita — quem escreve cada pedaço.** A distinção é a que o CÓDIGO já faz: **a base
vem do ASSET** (é o texto do jogo, com o `[0]`/`@…@` que o **motor** resolve em runtime) e **o mod
escreve só o que cada exemplo marca como "do mod"** — nunca reescreve a base por estilo. Na linha
branca o mod acrescenta o **valor por personagem**, soldado no fim da própria frase do jogo (o
sufixo do Decay abaixo é este caso; os outros valores por personagem que o mod solda na linha —
`Reaper's Toll`, `Hunger`, `Beserker's Blood` e o `(+N …)` das skills de atributo em % — seguem o
mesmo padrão). **A explicação do cálculo é sempre do mod e vai para o nível 2**; a linha de estado é
inteiramente dele (nível 3).

- **Nível 1** — linha branca do shrine:
  - `Increases dodge chance by 40%.` — **só o jogo**: a chave é `Increases dodge chance by [0]%.` e
    o `40` é o motor resolvendo o `[0]`.
  - `Take 20% of your Max Health in Shadow Damage per turn (20 damage per turn for you).` — **jogo
    + mod**: a base `Take 20% of your Max Health in Shadow Damage per turn.` é **do jogo** (a chave
    é `Take [0]% of your Max Health in Shadow Damage per turn.` e o `20%` sai do motor); o sufixo
    ` (20 damage per turn for you)` é **do mod** — montado por `ShrineAuraPatch.LinhaDecayComValor`
    (`ShrineAuraPatch.cs:850, 891`). **A linha do jogo termina no ponto**: é o mod que corta o ponto
    e solda o parêntese.
- **Nível 2** — a nota de cálculo (uma frase, sem quebra interna) — **inteiramente do mod**:
  `Base 20%; the value shown already includes the Shrine Effect Bonus.` ·
  `Armor blocks damage: each 10 Armor reduces damage taken by 1 (capped at 90% of the incoming damage). Armor and Magic Armor do not reduce Shadow damage.` ·
  `The attacker takes this damage in return, based on its own Max Health and not on the health of the one it attacked, before damage reduction.`
  (esta última é a nota do Flame: os **números por alvo** que ela traz são do mod — o texto do jogo
  para o Flame é só `Attackers take Fire Damage.`, sem número nenhum).
- **Nível 3** — o estado agregado (azul) — **inteiramente do mod** (os títulos não existem no jogo):
  `Your active shrine auras: Dodge +40% (total +57%); Damage +25% (total +50%).` (montada por
  `ShrineAuraPatch.AcumuladoShrines`, `ShrineAuraPatch.cs:1053`) ·
  `Your skills on this status: Frostbite I −2% damage per stack.` (montada por
  `StatusSkillSynergyPatch.Bloco`, `StatusSkillSynergyPatch.cs:173`)

Os três níveis convivem no mesmo tooltip, nesta ordem de leitura: descrição (1) → nota (2) →
estado (3). A posição é responsabilidade de `CorEOrdemDoTooltip` (move a nota e depois a linha
azul para o fim, uma linha em branco antes de cada bloco). **Quem** é a nota, essa função não
adivinha pela cor: ela reconhece o **conteúdo** que o mod escreveu — ver **§8**. O **formato
exato** — quantas linhas em branco, em que ordem os blocos saem e quantos blocos um tooltip pode
ter — está no **§9**.

---

## 4. O teste do nível 2 (regra do dono: informativo, mas NÃO parede de texto)

O nível 2 tem de **caber numa leitura** — o dono rejeitou parágrafo. O critério é medido pelo
parser oficial de notas, que agora também reporta comprimento:

```bash
python tools/check_notas_redundantes.py     # seção "Comprimento das notas" + exit != 0 se achar defeito de cor/redundância
```

- **Uma linha** = sem quebra de linha interna na nota (o `\n` do markup). Nota com `\n`
  interno é **parede de texto** e sai listada no relatório.
- Comprimento em caracteres é **medido e listado**, não reprovado: as notas aprovadas pelo
  dono têm tamanhos diferentes (`Base 20%; …` = 66 car.; a frase do Flame = 136 car.) e um
  teto de caracteres reprovaria texto que ele aprovou. Quem decide encurtar é o dono.
- **A cor não muda o comprimento**: os ajustes de cor desta convenção não tocam uma letra de
  nenhuma nota — a medida antes/depois é idêntica por construção.
- Nenhuma nota **aprovada pelo dono** pode ser encurtada por causa de cor. Se uma mudança de
  cor exigir mudar texto aprovado, **para e reporta** (regra do PROCESSO-REVISAO: o ajuste do
  dono vence).

---

## 5. A varredura (o que entrou em cada nível) e o achado do COR-1

Tudo o que o `BetterTooltips` anexa foi classificado. O que estava fora da convenção e foi
corrigido em 01/10 (COR-1):

| Bloco | Origem no código | Nível | Antes | Depois |
|---|---|---|---|---|
| Descrição do jogo (todas as tooltips) | `OptionsManager.Localize` sem nota | 1 | branco | branco (inalterado) |
| Notas de `TextAppends` (195) + `Flame`/`Decay`/12 auras de shrine | tabela | 2 | `#C8B090` | inalterado (**aprovado pelo dono**) |
| Notas fundidas em `TextFixes` | tabela | 2 | `#C8B090` | inalterado |
| Glossário (`Stealth`, `Marked Prey`, `Enrage`, `Life Steal`) | `SkillGlossaryRules` | 2 | **sem cor** (saía no tom do nível 1) | `NotaDeExplicacao(...)` |
| Efeitos por ponto de atributo | `BuildAttributeEffects` (+ 4 chamadas) | 2 | **sem cor** | `NotaDeExplicacao(...)` |
| Ordem da redução de dano | `BuildDamageReductionNote` | 2 | **sem cor** | `NotaDeExplicacao(...)` |
| Mitigação de Armor | `BuildArmorNote` (+ "Also increases Magic Armor") | 2 | **sem cor** | `NotaDeExplicacao(...)` |
| Mecânica de Resistência | `ResistanceExplainSuffix` (2 chamadas) | 2 | **sem cor** | `NotaDeExplicacao(...)` |
| Linha de auras ativas | `ShrineAuraPatch.AcumuladoShrines` | 3 | `CorDaLinhaDeAuras()` | inalterado |
| Bloco `Your skills on this status` (Frost Bite) | `StatusSkillSynergyPatch.Bloco` | 3 | `CorDaLinhaDeAuras()` | inalterado |

**ACHADO (a cor de 2 e 3):** os dois níveis usam **campos diferentes** do jogo
(`specialDescColor` × `skillStatusColor`) — a separação está certa. O que estava errado era o
**fallback**: `CorDaLinhaDeAuras()` caía no **mesmo marcador `#C8B090`** do nível 2 e, como o
`ComACorDoJogo()` repinta todo `#C8B090` do texto final, a linha azul podia sair **na cor do
nível 2** (níveis colapsados, em silêncio). Correção: (a) um terceiro elo azul da paleta
(`GUIManager.manaColor`); (b) o bloco do nível 3 **não é repintado** pela substituição do nível
2; (c) o log do colapso é explícito. Nenhuma cor nova foi inventada para isso.

> **COR-2 (01/10) — leitura corrigida deste achado.** O caminho "a linha azul era repintada
> pela substituição do nível 2" era **leitura de um caminho MORTO**: o `ComACorDoJogo` nunca
> rodava com o marcador no texto (ver **§7**), então não havia repintura nenhuma para observar.
> O que de fato colapsa 2 e 3 é o **fallback** do `CorDaLinhaDeAuras()` — e é isso que a
> correção do COR-1 (o terceiro elo azul + o log explícito) cobre. A leitura datada das cores
> (campo do nível 2, campo declarado do nível 3 e a paleta) está no §7.5.

---

## 6. O que NÃO entra (intocável)

- As **12 notas de shrine** enxugadas pelo dono, a **frase curta do Flame** e a **seção curada
  por ele** são intocáveis. Cor é markup; se a cor puder mudar sem tocar o texto, o texto fica.
  Se o texto tiver de mudar, **para e reporta**.
- **Bard/música**: fora de escopo até a próxima atualização do jogo (regra do projeto).
- Nada de `<b>` nas explicações: o `BetterFont` não tem face bold e o TMP cai para outra fonte
  (medido em 29/09). O negrito do jogo (`@termo@`) é do jogo, não nosso.

---

## 7. A ORDEM DOS GANCHOS (e por que a cor NÃO é um gancho separado) — COR-2, 01/10

Este capítulo existe porque o COR-1 tinha a cor certa, no lugar certo do texto e com a
procedência certa — e **mesmo assim o jogador nunca viu a cor**: ela era aplicada por um
gancho que rodava antes de existir o que colorir.

### 7.1 O fato, lido do 0Harmony que o jogo carrega

O `0Harmony.dll` do perfil é **byte a byte** o do repositório
(sha256 `1a21cc03…c1031`; `lib/0Harmony.dll`). Nele:

```csharp
// HarmonyLib.PatchInfoSerialization.PriorityComparer  (scratch/cor2/PatchInfoSerialization.cs:48-58)
if (priority != value) return -priority.CompareTo(value);   // DESCENDENTE: maior roda primeiro
```

e o emissor do IL percorre a lista **já ordenada**, na ordem
(`scratch/cor2/HarmonyManipulator.cs:646`, `WritePostfixes`). Conclusão: **em postfix, a
prioridade MAIOR roda PRIMEIRO** — o oposto do que os comentários do código diziam
(`LocalizePatch.cs` l.454-455 antes do COR-2, e o mesmo erro na l.35).

Com `CorDoJogoPostfix` em `Priority.High` (600) e o gancho das notas em `Normal` (400), o
gancho da cor rodava **antes** das notas: ele olhava um texto em que o marcador `#C8B090`
ainda não existia, não lia campo nenhum e não trocava nada. O `#C8B090` das tabelas ia
**literal** para a tela.

### 7.2 A prova empírica (a que vale mais que o código parecer certo)

Na sessão de 01/10 feita **com a DLL do perfil**
(`scratch/cap1/out/log-anterior-antes-da-rotina.log`):

> **RESSALVA (FIX-4, 01/10): a DLL do perfil é a build PRE-conserto do COR-2 — não é a build
> nova.** A sessão citada aqui (e a fixture `cores-do-jogo`, que dela copia as linhas) prova o
> comportamento da build **antiga** — o marcador `#C8B090` no texto final, a linha de leitura do
> nível 2 ausente —; **não** prova o conserto. O que prova o conserto é a bancada de ordem de
> ganchos (`scratch/cor2/ordem_ganchos_medicao.txt`) e as travas de teste, nunca esta sessão.

* a linha que o gancho da cor imprime ao **ler** o campo — `cor do jogo para explicacoes =
  #…` — **não existe em log nenhum** (0 ocorrências, e 0 da variante de erro). Se o gancho
  tivesse visto o marcador, ela estaria lá;
* enquanto isso, o log **mostra o marcador no texto final** (`ShowTooltip interceptado …
  (nota #C8B090, auras ativas #00D7FF)`) e as linhas do gancho das notas ("corrigido",
  "explicação adicionada").

Só existe uma explicação para as duas coisas juntas: **o gancho da cor rodou antes de o
marcador existir**. A fixture `cores-do-jogo` guarda essas linhas e o teste `t_cores_niveis.py`
as usa.

> **Colapso 2→3:** o "colapso" que o COR-1 acreditou ter consertado era leitura de um caminho
> **morto** (a cor do nível 2 nunca chegava ao texto, então não havia como ela repintar o
> nível 3). Não foi observado nem é reproduzível nesta build. Quem ainda colapsa 2 e 3 é o
> **fallback** do `CorDaLinhaDeAuras()` (sem nenhum elo azul, a linha azul sai no marcador) —
> e é isso que a correção do COR-1 (terceiro elo, `manaColor`) realmente cobre.

### 7.3 O caminho escolhido: a cor é aplicada PELO GANCHO DAS NOTAS, no fim dele

Duas opções existiam — reordenar de verdade (dar prioridade menor ao gancho da cor) ou fazer
o gancho das notas ler a cor por si. A escolha foi a **segunda**:

```
Postfix(string original, ref string __result)          // Normal (400) — o mesmo gancho de sempre
    AplicarNotasDoFunil(original, ref __result);       // tabelas + regras dinâmicas (a nota entra com o marcador)
    __result = ComACorDoJogo(__result);                // NÍVEL 2: a cor é resolvida sobre o texto JÁ montado
```

Por que não reordenar: **prioridade de gancho não é contrato** — ela já foi lida errado uma
vez, é invisível na leitura do código e não tem teste que a vigie. Com um único ponto de
aplicação, **não existe ordem para errar**: a cor é resolvida no mesmo instante em que a nota
é escrita. O gancho separado foi removido (o comentário longo ficou no lugar dele, acima da
tabela `TextAppends`, citando a bancada e o log).

### 7.4 Os três critérios que ficaram escritos (e vigiados por teste)

| critério | regra | quem vigia |
|---|---|---|
| **Sanidade do nível 2** | a cor da explicação tem de ser um **tom quente/bege** — nunca azul. Se o campo virar azul, os níveis 2 e 3 ficam indistinguíveis (o colapso em silêncio). É o espelho do `EhAzul` do nível 3, que já existia. | `tools/testes/testes/puros/t_cores_niveis.py` (espelho do `EhAzul` em `tools/testes/regras_cor.py`) |
| **`#808080` e outras cores do jogo** | cor dentro de um valor de `TextFixes` é **legítima quando o próprio jogo já escrevia essa cor na CHAVE** (o caso real: o bege de citação `#808080` dos status, ex. `Curse of the Reaper`). Cor que só o mod escreveu tem de ser o marcador do nível 2. | `tools/check_notas_redundantes.py` (família 4) |
| **"Explicação E efeito"** | um valor de `TextFixes` pode ser, no **mesmo texto**, a **correção** da linha do jogo (nível 1, sem cor nossa) e a **nota** (nível 2, com o marcador). A cor na chave é o que separa as duas partes: a parte corrigida não ganha cor, a nota carrega o marcador. | idem (mesma regra) |

### 7.5 Procedência das cores — leitura datada de 01/10 (o que mudou de fato)

| campo | valor lido do prefab (01/10) | o que isso diz |
|---|---|---|
| `Tooltip.specialDescColor` (nível 2, declarado) | **`#CBB396`** | o bege medido por pixel em 29/09 (`#C8B090`) é **este campo** (a diferença é do print). O campo declarado **se sustenta**. |
| `Tooltip.skillStatusColor` (nível 3, declarado) | **`#CBB396`** | **o mesmo bege**: ele **nunca passa no `EhAzul`**, então o "elo 1" do nível 3 é **elo morto** — o azul em uso é o elo 2. |
| `GUIManager.coldColor` (nível 3, reserva) | **`#00D7FF`** | é o azul que o log de runtime imprime — **é o que a linha azul usa hoje**. |
| `GUIManager.manaColor` (nível 3, reserva) | **`#66A8FF`** | terceiro elo, azul (o COR-1 o acrescentou). |
| `#808080` | literal do motor | cor de **citação/flavor do jogo** (a fala do status), preservada por nós. Nenhuma regra de nível se aplica a ela. |

**Contradição a reportar ao dono (fato medido, não decisão):** a **fonte declarada do nível 3
na especificação** (`Tooltip.skillStatusColor`, §1/§2) **não se sustenta** — o campo é bege e
não é azul nesta build; o azul do nível 3 vem da **paleta da HUD** (`coldColor`, `#00D7FF`).
O COR-2 **não mudou a cor de nada**: a escolha da cor de cada nível é do dono, e a estrutura
de três níveis ficou intacta. O que está registrado aqui é o fato. Se o dono quiser que o
nível 3 se chame "azul da paleta" na tabela (§1/§2), é uma linha de texto — **decisão dele**.

### 7.6 Cobertura da trava (COR-2): o furo fechado

Das **21 entradas de `TextFixes` com cor** (na leitura de hoje da tabela), a família 4 do
`check_notas_redundantes.py` conferia **11** e ignorava **10** — porque só olhava o formato de
**duas** quebras (`\n\n<color=#…>`). E **duas das 12 notas de shrine** moravam nas ignoradas
(`Recover [0]% of max mana/health each turn`, formato de **uma** quebra): trocar a cor de uma
nota fundida passava em silêncio.

Fechado: a varredura passa a conferir **toda cor de todo valor de `TextFixes`, em qualquer
formato** (e todo valor de `TextAppends`), com as duas regras da tabela do §7.4; e o parser da
ferramenta passou a **ver as entradas com comentário dentro do `{`** (o formato "chave em linha
própria", ex. `Shapeshift Dragonkin`) — 4 blocos de nota que **nenhuma** família via. A isca
versionada (`tools/testes/contra-prova/cp_cor_nota_fundida_isca.py`) reprova pelo motivo certo:
ela espera o comportamento antigo ("DEIXA PASSAR") e a trava de hoje pega a troca.

### 7.7 Cobertura da trava (FIX-4): o comentário de BLOCO — e o que **não** cobrimos

**Fechado (achado da REV-55).** O COR-2 fez o parser da trava ver as entradas com comentário de
**linha** (`// ...`) dentro do `{` (§7.6). O comentário de **BLOCO** (`/* ... */`) antes da chave
não era pulado: a entrada **sumia** da varredura (os blocos de nota caíam de **25 para 24**) e a
troca de cor nela **não reprovava**. As duas formas de comentário são puladas agora
(`tools/tabelas.py`, `pula_brancos_e_comentarios` — o parser único, que o `check_notas_redundantes.py`
passou a usar no PARSER-1), e o par versionado
`tools/testes/contra-prova/cp_cor_comentario_bloco_isca.py` × `..._ok.py` prova as duas metades: a
isca reprova na expectativa antiga ("DEIXA PASSAR") e a metade ok passa (a trava PEGA e cita a cor
plantada). Quem vigia o par na suite é `testes/puros/t_trava_cor_notas_fundidas.py`.

**O leitor virou UM só (PARSER-1, 01/10).** O FIX-4 fechou o buraco **numa** cópia — e o mesmo
ponto cego (comentário entre a abertura `{` e a chave) vivia em outras. A varredura do PARSER-1
achou cada cópia e todas passaram a usar o parser ÚNICO **`tools/tabelas.py`** (`bloco` +
`entradas`, que pulam `//` e `/* */` em TODO passo):

| cópia (arquivo:linha) | **o que alimenta** |
|---|---|
| `tools/tabelas.py:64` / `:181` | **o parser único** (a fonte da verdade; pular comentário de linha E de bloco) |
| `tools/check_chave_compartilhada.py:118` / `:133` | varredura **BUG-32** (chave nas duas tabelas = trava de release); é importado pelo `check_dupes.py:63` |
| `tools/check_dupes.py:63` | chave **duplicada** → `ArgumentException` derruba o `LocalizePatch` inteiro (INC-1) |
| `tools/check_notas_redundantes.py:212` / `:240` | relatório **RV-15** e a trava de release das notas (cor do nível 2 / redundância) |
| `tools/check_fix_keys.py:32` | chave × censo (passo 2 do CI) |
| `tools/check_omissao.py:80` | o que o mod já cobre (varredura de omissão) |
| `tools/check_scaling.py:59` | idem, para a escala |
| `tools/review_ledger.py:39` | livro **ANTES-E-DEPOIS** (`docs/cobertura/revisao/`) |
| `tools/testes/regras_cor.py:351` | material dos testes da família de COR + o **alcance do COR-3** (`scratch/cor3/cor3_alcance.py`, que a consome) |

Os rascunhos `scratch/cor2/levanta_cores.py:15` / `scratch/cor2/mede_furo_trava.py:13` têm cópias
antigas do leitor; são **descartáveis** (medições de uma revisão fechada) e ficaram de fora da
migração, registradas aqui. A cópia `regras_cor._entradas` era o **4º irmão** do defeito —
fechá-la corrigiu os números do alcance (§8.4). A prova REPROVANDO (leitura antiga × nova, com a
saída literal das duas e a conferência de que as **8 cópias vivas** concordam com o parser único —
`check_chave_compartilhada`, `check_dupes`, `check_notas_redundantes`, `check_fix_keys`,
`check_omissao`, `check_scaling`, `review_ledger` e `regras_cor`) é
`testes/puros/t_parser_comentario_na_chave.py`.

**Cobertura REAL do conserto de bloco (medida pelo PARSER-1R).** No fonte do produto há
**zero** casos de comentário de bloco (`/* ... */`) antes da chave (grep = 0 no
`LocalizePatch.cs`, e 0 `/*` dentro dos dois blocos). O conserto do FIX-4 é exercido, hoje,
**só pela ilha sintética** — o `_selftest` do `tabelas.py`, a `FONTE_FALSA` do
`t_parser_comentario_na_chave.py` e as iscas `cp_cor_comentario_bloco_*`. Nenhuma entrada real
depende dele; ele fica pronto para a primeira que use o formato. Não confundir "o teste passa"
com "o produto exercita".

**Decidimos NÃO cobrir (e por quê).** Além do comentário de bloco, a REV-55 levantou três
formatos como candidatos a isca. Ficaram de fora — a trava é trava de *release*, e alargar o
padrão por forma que ninguém escreve só afrouxa o que ela tranca:

| formato | por que **não** entra |
|---|---|
| `<color=#RRGGBBAA>` (cor de 8 dígitos) | nada no nosso material emite 8 dígitos: as tabelas usam `#RRGGBB` (o mesmo `ColorUtility.ToHtmlStringRGB`) e os únicos `#00000000` do repo são markup do próprio jogo (`scratch/sac1/`), que passa intocado. Cor de 8 dígitos NOSSA seria convenção nova — e convenção nova se decide na revisão, não se adivinha no regex. |
| `<color=#RRGGBB >` (espaço antes do fecha-angular) | nenhuma linha do repo escreve esse espaço (grep = 0). Aceitar espaço opcional alargaria o padrão por uma forma que ninguém escreve. |
| nota acrescentada **fora** do `AnexarNota` | é outra família de defeito. Os dois sítios que anexam nota sem `AnexarNota(__result, ...)` (`BetterTooltips/Patches/ShrineAuraPatch.cs:1221`, `BetterTooltips/Patches/StatusSkillSynergyPatch.cs:173`) são blocos do **NÍVEL 3** (`CorDaLinhaDeAuras()`), cuja regra é o `EhAzul` — coberta por `t_cores_niveis.py`, não pela família 4. Varrer "todo sítio que produz nota" pede instrumento próprio (lista branca das funções que anexam) e é tarefa à parte. |

---

## 8. A POSIÇÃO — de quem é o bloco que vai para o fundo (COR-3, 01/10)

Este capítulo existe porque o COR-2 fez a cor do nível 2 **chegar** ao bloco (era o que faltava:
§7) e, ao fazer isso, quebrou a POSIÇÃO de toda tooltip que mostra um valor do jogo. O relato do
dono, com o build instalado: *"os tooltips com dano que estavam na posição correta foram movidos
para o FUNDO do tooltip"*.

### 8.1 O fato que faltava: a cor do nível 2 é a cor dos VALORES do motor

`Tooltip.specialDescColor` vale **`#CBB396`** (§7.5) — e `#CBB396` é **o literal que o próprio
motor escreve nos valores dinâmicos**:

* `Tooltip.ApplyDescriptionExpressions` (l.2327 do decompilado): o `[N]` vira
  `<color=#CBB396>VALOR</color>`;
* `Tooltip.GetDamageString` (l.2276): o `*N` (o dano da skill) vira
  `<size=…><color=#CBB396>NN</color></size>`.

Ou seja: **nível 1 (valores do jogo) e nível 2 (nossas notas) têm o mesmo hex**, e o único jeito
de dizer qual é qual é a ORIGEM do texto, não a cor.

### 8.2 O mecanismo exato (arquivo:linha)

`CorEOrdemDoTooltip.Prefix` (`BetterTooltips/Patches/LocalizePatch.cs`, o prefixo em
`Tooltip.ShowTooltip`) tirava a nota do meio da descrição e a recolocava no fim — e a procurava
por **"o primeiro bloco da cor do nível 2"** (`TirarBloco(..., corNota, ultimo: false, …)`). No
build do dono (`BetterTooltips/bin/Release/.../BetterTooltips.dll`, 01/10 14:41) essa chamada é
literalmente:

```csharp
bool flag = TirarBloco(ref description, text2 /* corNota */, ultimo: false, null, out bloco2);
```

Enquanto a cor não era aplicada (o defeito do §7), `corNota` caía no marcador `#C8B090` — um hex
que **nenhum** bloco do jogo usa — e o alvo era sempre a nossa nota. Com o CONSERTO do §7
(`__result = ComACorDoJogo(__result)` no fim do gancho das notas), `corNota` passou a ser
`#CBB396`: o **primeiro** bloco dessa cor numa tooltip de skill passou a ser o **valor de dano**
(o `*0` da própria skill, que aparece antes da nota no texto), e era ELE que ia para o fundo — a
nota ficava onde estava. Nada de texto mudou; só o bloco escolhido (§4: a COR-1 media texto, e
por isso passou).

### 8.3 A correção: a nota é reconhecida pelo CONTEÚDO

`ComACorDoJogo` passou a **registrar o conteúdo** de cada bloco que nasceu com o marcador
(`RegistrarBlocosDeNota` → `_conteudosDeNota`) **antes** de trocar a cor — é o texto que o mod
escreveu, e ele sobrevive à troca. O prefixo passou a usar `TirarNotaDoMod`, que procura o bloco
cujo conteúdo está nesse registro. Um valor do motor é um número; a nota é uma frase — não há
como um casar com o outro. O registro acontece mesmo quando a leitura do campo falha (o bloco
fica no marcador e continua identificável).

A linha de auras (nível 3) continua sendo achada por **cor + marcador de texto** (`Your active
shrine auras:`), e por um motivo que vale registrar: o azul dela (`GUIManager.coldColor`,
`#00D7FF`) é uma cor que o motor **não** usa em bloco nenhum, e o bloco carrega marcador próprio.
Bloco do nível 3 que cai no marcador de reserva fica **fora** do registro de notas de propósito.

### 8.4 O alcance do defeito (medido, não suposto)

O defeito não era exclusivo das skills: **qualquer** tooltip com um bloco `#CBB396` do motor
mandava o primeiro deles para o fundo — a deste mesmo texto, inclusive, e o `[0]` da linha branca
de **shrine**. A prova executável está em `tools/testes/testes/puros/t_cor3_posicao.py`: ela roda
as DUAS regras sobre o MESMO texto, com material real das tabelas (2 skills com dano + a nota de
dodge das shrines), e exige que a regra antiga mande o valor para o fundo (o defeito
reproduzido) e que a do COR-3 mande a nota, deixando o valor na linha branca. A metade da regra
antiga também é rodada uma vez sobre a shrine, para o alcance ficar medido, não narrado.

**O alcance CORRIGIDO (PARSER-1, 01/10).** O número medido acima saiu, na primeira vez, de um
parser com ponto cego: o regex `regras_cor._entradas` **não via a entrada cujo comentário — `//`
ou `/* */` — fica entre a abertura `{` e a chave** (o MESMO buraco que o FIX-4 fechou no
`check_notas_redundantes.py`, §7.7; e o 4º irmão da família). Ele contava **283 chaves** e **76
atingidas**; o parser ÚNICO (`tools/tabelas.py`, que passou a ser usado por todas as cópias do
leitor) conta **298 chaves da tabela** (o dicionário `TextAppends`+`TextFixes` inteiro), **220
chaves com nota** (dessas, as cujo VALOR carrega o marcador `#C8B090`) e **83 atingidas** — cerca
de 10% a mais, todas no `TextFixes` (86 → 101 chaves). Por família: skills 39, fora-do-censo 22,
status 17, afixos 5. Os dois rótulos são **coisas diferentes**: "chaves da tabela" é o
dicionário; "chaves com nota" é o subconjunto com a NOSSA nota no valor — a primeira medição
usava o segundo rótulo para o primeiro número. A medição viva é `scratch/cor3/cor3_alcance.py`; a
prova REPROVANDO (leitura antiga × nova, com a saída literal das duas) é
`tools/testes/testes/puros/t_parser_comentario_na_chave.py`.

**Consequência para a convenção (§1/§2):** os níveis 1 e 2 compartilham o hex `#CBB396` — o que
distingue um do outro é o PAPEL do bloco (valor do motor × explicação do mod) e o lugar no
tooltip, nunca a cor. Quem depender de cor para separar os dois níveis erra exatamente como o
prefixo errou.

---

## 9. O FORMATO DAS NOTAS — a linha em branco exata e a ordem dos blocos (RV-17, 01/10)

Este capítulo existe porque a POSIÇÃO (§8) foi mexida duas vezes no mesmo dia e o que faltava
travar era o **formato**: **quantas** linhas em branco, **em que ordem** os blocos saem e **quantos
blocos** um tooltip pode ter. A revisão do COR-3 (COR-3R) achou os dois furos que este capítulo
fecha — os dois exatamente no ponto onde o defeito do §8 apareceu.

### 9.1 A regra, em uma frase

> **Depois da descrição do jogo (nível 1), cada bloco que o mod escreve vai para o FIM do corpo do
> tooltip, na ordem em que aparece no texto de origem, separado do que vem antes por EXATAMENTE
> UMA LINHA EM BRANCO — e a linha azul do nível 3 (auras ativas / skills no status) é sempre a
> última.**

Duas consequências diretas, e as duas são trava de teste:

* **o mod não escreve linha em branco em nenhum outro lugar.** Nem no fim do tooltip (o defeito do
  RV-17(a), o “vazio desnecessário” que o dono viu em `Chain Lightning` e `Breath of Winter`), nem
  **onde o bloco foi retirado** do meio do texto (o defeito do §9.4). **A exceção é do JOGO** e está
  no §9.8: o `ShowSkillTooltip` e o `ShowActionStatusTooltip` escrevem eles mesmos UMA linha em
  branco antes da **PRIMEIRA** linha de custo/metadados do caminho (`AP Cost`, `Duration Type`) —
  ela não é do mod e não pode ser apagada. Não existe exceção para as linhas de custo **seguintes**
  (§9.8.6). *(Esta redação qualificada **substitui** a frase antiga, que dizia “em nenhum outro
  lugar” sem qualificar — a leitura errada dela está registrada logo abaixo.)*
* **o FORMATO é um só.** O que muda entre os casos é **quantos blocos** o tooltip tem — um (§9.2)
  ou dois (§9.3) —, nunca o formato de cada bloco.

**BANCADA-1 (01/10) — A FRASE ANTIGA “EM NENHUM OUTRO LUGAR” FOI SUBSTITUÍDA.** Ela está **fora
deste texto** (não se afirma mais aqui): dizia “o mod não escreve linha em branco em nenhum outro
lugar” **sem qualificar** e era lida como se valesse para o tooltip inteiro — e o tooltip inteiro tem
a linha em branco do jogo. A bancada de teste montava os custos com **uma** quebra (o jogo escreve
**duas**) e o próprio checador reprovava o texto do runtime acusando “linha em branco órfã”. O lado
errado era a bancada (e aquela redação); o código do mod estava certo. A frase de hoje (o primeiro
item acima) diz só o que **o mod** escreve e nomeia a exceção do jogo. O passo a passo com os
números, os três caminhos de montagem e a prova estão no **§9.8**; a restrição da linha do jogo à
**PRIMEIRA** linha de custo de cada caminho é o **BANCADA-2 (§9.8.6)**.

**NIV3-1 (01/10) — A REGRA VALE PARA OS *DOIS* BLOCOS DE NÍVEL 3.** Havia uma exceção de fato, e
não escrita: o bloco `Your skills on this status` é escrito pelo `StatusSkillSynergyPatch` num
gancho **diferente** — o postfix de `Tooltip.ApplyDescriptionExpressions`, que roda *antes* do
`ShowTooltip` — e o prefixo `CorEOrdemDoTooltip` só recolhia a linha `Your active shrine auras:`
(o bloco de sinergia fica de fora do laço das notas por desenho: o `EhBlocoDoNivel3` o exclui do
`_conteudosDeNota`). Numa tooltip com **NOTA e sinergia** a nota era devolvida pelo fim **depois**
da linha azul, e o §9.1 deixava de ser verdade. Esse caso **não existe hoje** — só `Chilled`
(`status.csv:71`) e `Poisoned` (`status.csv:336`) geram o bloco, e nenhum dos dois recebe nota —, e
é por isso que o defeito passou sem ser visto.

**Decisão: o bloco de sinergia passa a ser tratado como os outros** — e **não** como exceção
declarada com o §9.1 reescrito. Motivo: ele **é** nível 3 (§1, linha 3(b), o caso do Frost Bite);
declarar uma ordem própria para um dos dois blocos do mesmo nível seria escrever a exceção para
varrer o defeito, e a alternativa exigiria mexer na própria definição do nível, não só nesta regra.
O bloco é recolhido pelo **marcador de texto** dele (§8.3, nunca pela cor) e devolvido no fim,
depois das notas; quando os **dois** blocos de nível 3 existem — **hoje impossível** —, a **linha de
auras continua por ÚLTIMO**, que é a ordem aprovada pelo dono.

**Por que a coexistência é impossível hoje — e por que isso NÃO é o que garante a ordem
(NIV3-1R, 01/10).** O índice do `StatusSkillSynergyPatch` olha o **`AttributeEffects`** do status, o
único lugar onde ele procura `Source["X"]`: é ali que as **9 auras com `AttributeEffects`** (as de
buff) leem `Target["ShrineEffectBonus"]`, e por isso nenhuma delas entra no índice. **Flame e Decay
também leem `Source["ShrineEffectBonus"]`** — mas na **fórmula de dano do próprio action** (a ação
`* Aura Proc`), **fora do `AttributeEffects`**, que é o único lugar que o índice varre. A redação
anterior dizia só “as auras de shrine leem `Target[...]`”, mais ampla do que o dado sustenta: quem
lesse depois poderia concluir que a impossibilidade não vale. A impossibilidade é **do índice** —
ele não vê a fórmula de dano.

**E a ordem não depende dos dados: ela é IMPOSTA NO CÓDIGO.** Mesmo que a impossibilidade acima
fosse falsa, o `CorEOrdemDoTooltip` monta a cauda de nível 3 como **sinergia + `\n\n` + linha de
auras** (`aura = sinergia + "\n\n" + aura`, `LocalizePatch.cs`) e a anexa **depois** de recolher as
notas — a linha de auras sai por ÚLTIMO **por construção**, não por acaso do que os dados de hoje
contêm. São **dois argumentos diferentes**: a impossibilidade é do índice (dado); a ordem é do
código (construção). O forte é este último.

O mesmo caminho tinha um **segundo** defeito, invisível enquanto o prefixo nem tocava no bloco: o
patch o anexa com **uma quebra crua** (e não com o `\n\n` do `AnexarNota`), então mesmo sem nota ele
saía **colado** na descrição — com o bloco passando pelo prefixo, a linha em branco desta regra deixa
de faltar.

A trava está em `t_nivel3_sinergia.py` + a contra-prova `cp_nivel3_sinergia_isca.py` × `..._ok.py`,
no material real (as descrições de `Chilled`/`Poisoned` do censo + uma nota real das tabelas), e ela
prova também que **as auras de shrine saem byte a byte idênticas** com e sem a correção.

### 9.2 O bloco, no texto montado e nas tabelas

O que o jogador lê (nível 1 → custos do jogo → nota), com `[ ]` marcando o bloco do nível 2:

```
Deals 42 lightning damage to all enemies within a line.
                                          <- linha em branco DO JOGO (l.1470 + l.1536, §9.8)
AP Cost: 2
Range: Line
                                          <- linha em branco DO MOD (o AnexarNota, separador)
[The 50% roll only decides whether each element lands; ...]
```

São, portanto, **duas** linhas em branco num tooltip de skill com nota — e elas têm donos
diferentes: a de cima é do motor (`ShowSkillTooltip`), a de baixo é do mod. A bancada de teste
precisa montar as duas (§9.8); enquanto ela montava só a de baixo, o texto que ela media não era o
do jogo.

Onde essa linha em branco **do mod** nasce, por **família de entrada** (as duas são markup, nunca
texto):

| família | como o valor está na tabela | quem põe a linha em branco |
|---|---|---|
| **acrescentada** (`TextAppends`, 197 entradas) | o valor é só a nota, e começa com `\n` | `AnexarNota(texto, nota)` = `texto.TrimEnd() + "\n\n" + nota.TrimStart('\n')` — a quebra da frente da tabela é **consumida**, e sai **uma** linha em branco |
| **fundida** (`TextFixes`, 25 blocos de nota) | o valor é o nível 1 **e** a nota, no mesmo literal | a linha em branco está **escrita no valor**; o prefixo a normaliza de qualquer forma (§9.4) |

`#808080` **não é nota**: é a cor de citação do próprio jogo (a fala do status, §7.5) e fica onde
o jogo a escreveu — nenhuma regra de nível se aplica a ela.

### 9.3 Duas notas no MESMO tooltip — a decisão (e por quê)

O comentário do código afirmava que *“o mod anexa uma por tooltip, jamais duas do nível 2”*. **É
falso**, e existem **dois casos reais**, os dois com os dois blocos dentro do MESMO valor fundido:

| entrada | as duas notas |
|---|---|
| `Shapeshift Dragonkin` (tem o `[0]` do Armor) | `Scales with your character level.` + `The Dragonkin grants a Slash, a Breath and an Orb of its element: ...` |
| buff `Miniature` (status) | `Also reduces the healing this character does by the same percentage.` + `Current health is reduced by the same percentage and comes back when the status ends. This cannot kill.` |

**Decisão: as DUAS vão para o fim, na ordem em que aparecem no texto de origem** — o formato é o
mesmo, o que muda é a contagem. Motivo: a ordem do texto é a ordem em que o autor escreveu (a
primeira nota explica o `[0]`/o valor; a segunda, o resto), e inverter isso faz o leitor ler a
explicação 2 antes da 1. Não há razão para descartar a segunda: ela é informação do mod, não
repetição — o `check_notas_redundantes.py` (§4) continua sendo quem barra redundância.

Antes/depois literal, com o mesmo material (`Miniature`, com os custos do jogo):

```
ANTES (o defeito)                         DEPOIS (o formato)
Movement increased by 3. ... -25%.        Movement increased by 3. ... -25%.
                                          <- uma linha em branco
[Current health is reduced by the ...]    AP Cost: 1
AP Cost: 1                                Range: Melee
Range: Melee                              
                                          <- uma linha em branco
                                          [Also reduces the healing ...]
                                          <- uma linha em branco
                                          [Current health is reduced by the ...]
```

No quadro acima, `ANTES` é o **defeito reproduzido** (a 2ª nota ficava atrás, antes do
`AP Cost`, e a 1ª ia para o fim — a ordem de leitura invertia) e `DEPOIS` é o que o jogo mostra
hoje. A 2ª nota **não** é reescrita nem removida: ela só muda de lugar. A linha em branco que
aparece **antes do `AP Cost`** nos dois lados do quadro é a **do jogo** (§9.8), não uma sobra — ela
existe na tooltip vanilla e não é defeito nenhum.

### 9.4 A sobra do separador (o segundo furo) — e por que ele era “órfã” no modelo errado

O prefixo **tira** a nota do meio do corpo e a recoloca no fim (§8.2). Ao tirá-la, ele consumia
**uma** quebra; o resto do separador ficava para trás. A correção é o `InicioDoSeparador`: a
extração consome o separador **inteiro** (as duas quebras que o `AnexarNota` escreveu). Nenhuma
quebra do jogo é tocada — o `AnexarNota` apara o fim da descrição antes de escrever o separador
dele; nas entradas fundidas só existe uma quebra, e ela é o separador do próprio texto, então nada
além dela é consumido.

**BANCADA-1 (01/10) — O TAMANHO DA SOBRA.** O §9.4 chamava a sobra de “linha em branco **órfã**”,
no singular, porque a bancada acreditava que o jogo escrevia **uma** quebra antes do `AP Cost`. Ele
escreve **duas** (§9.8). Com o texto REAL, consumir uma quebra deixa **duas linhas em branco
seguidas** entre a descrição e o `AP Cost` — o mesmo defeito do RV-17(a) —, e consumir o separador
inteiro é o que faz sobrar **exatamente uma**, que é a do jogo. O nome “órfã” descrevia o modelo
errado da bancada; o conserto, não: ele é o mesmo.

Antes/depois literal (`Timber Wolf`, valor fundido + custos), com o texto como o jogo o monta:

```
ANTES (consome UMA quebra)                  DEPOIS (consome o separador inteiro)
Summons a Timber Wolf to fight for you.     Summons a Timber Wolf to fight for you.
                                            <- UMA linha em branco (a do JOGO)
                                            AP Cost: 1
                                            Range: Melee
                                            <- UMA linha em branco (a do MOD)
                                            [Timber Wolf: Melee Attack, Cripple ...]

  (acima: DUAS linhas em branco seguidas
   antes do `AP Cost` — o defeito do
   RV-17(a), reprovado pela trava)
```

No quadro acima, `ANTES` é o **defeito reproduzido** (consumir uma quebra deixa a sobra) e `DEPOIS` é
o que o jogo mostra hoje.

### 9.5 A ORDEM DAS HABILIDADES nas invocações (RV-17(b))

Nas notas de **invocação**, quando a criatura tem ataque básico no asset, ele vem **primeiro**:

> **`Melee Attack` / `Ranged Attack` primeiro; as habilidades especializadas depois.**

Fonte da verdade: o dump `docs/cobertura/invocacoes.csv` (a ORDEM é a do asset). Quatro criaturas
tinham a ordem do asset **invertida** e foram reordenadas na nota — a divergência é o que prova
que a regra foi *aplicada*, e não que as notas já nasceram certas:

| criatura | ordem no ASSET (dump) | ordem na NOTA |
|---|---|---|
| `Timber Wolf` | `Cripple, Melee Attack` | `Melee Attack, Cripple` |
| `Stag` | `Stunning Kick, Melee Attack` | `Melee Attack, Stunning Kick` |
| `Moose` | `Ground Slam, Melee Attack` | `Melee Attack, Ground Slam` |
| `Panther` | `Shadow Walk, Melee Attack` | `Melee Attack, Shadow Walk` |

`Grizzly`, `Skeletal Mage`, `Undead Wizard`, `Iron Golem` e `Skeletal Archer` **não têm** ataque
básico no asset (conferido no mesmo dump) — nesses a nota lista só o que o bicho faz, e o teste
não exige básico nenhum.

### 9.6 O que ficou travado (e como)

| trava | onde | o que ela pega |
|---|---|---|
| `t_formato_notas.py` (pura) | `tools/testes/testes/puros/` | a estrutura no fonte (`AnexarNota` = uma linha em branco; o prefixo recolhe **todas** as notas em laço e devolve a linha azul por último; a extração consome o separador inteiro), o comportamento nas **quatro famílias** com material real, o defeito **reproduzido** na regra antiga, o checador **não vazio** (defeitos plantados têm de ser vistos) e a ordem das habilidades contra o dump |
| `cp_formato_notas_isca.py` × `..._ok.py` | `tools/testes/contra-prova/` | as duas metades do mesmo teste: com a regra de **antes** o tooltip sai quebrado (a isca reprova citando o motivo); com a de **hoje**, fecha |
| o espelho do nível 3 | `regras_cor._registra_blocos` | o bloco que abre com `Your active shrine auras:` / `Your skills on this status:` **não** entra no registro de notas, como no `EhBlocoDoNivel3` do C# — sem isso o teste media um comportamento que o código não tem |
| `t_nivel3_sinergia.py` (pura) | `tools/testes/testes/puros/` | o bloco de nível 3 que **não** é a linha de auras (`Your skills on this status`): é recolhido pelo **marcador**, vai para o fim **depois das notas**, e as auras de shrine saem **idênticas** com e sem a correção (material real: `Chilled`/`Poisoned` do censo + uma nota real das tabelas) — e a estrutura no C# (a extração antes do laço, a cauda de nível 3 por último) |
| `cp_nivel3_sinergia_isca.py` × `..._ok.py` | `tools/testes/contra-prova/` | as duas metades: **sem** o recolhimento a nota sai **depois** da linha azul (a isca reprova pelo motivo); com ele, fecha |
| `formato-notas.entrada.json` (a LEITURA, §9.8) | `tools/testes/fixtures/` | o caminho de montagem da tooltip no decompilado (`ShowSkillTooltip` / `ShowGroundEffectTooltip` / `ShowActionStatusTooltip`): trecho literal, linha, método e o número de quebras — contado dos escapes do próprio trecho. O teste confere os trechos contra o decompilado quando ele existe nesta máquina |
| `cp_formato_quebra_do_jogo_isca.py` × `..._ok.py` | `tools/testes/contra-prova/` | a bancada **reproduz** o jogo: a isca declara UMA quebra antes do `AP Cost` (a bancada de antes do BANCADA-1) e **reprova** imprimindo os dois textos; a metade ok declara a leitura e passa |
| `cp_formato_linha_antes_do_range_isca.py` × `..._ok.py` | `tools/testes/contra-prova/` | o checador libera **só a primeira** linha de custo de cada caminho (BANCADA-2): a isca declara o bloco inteiro (o afrouxamento) e reprova em cima do texto plantado `descricao \n\n AP Cost \n\n Range`; a metade ok declara o conjunto de hoje e passa |
| `reg.controle_das_linhas_de_custo` | `tools/testes/regras_cor.py` | a lista `custo_no_texto` (escrita à mão) passa a ter controle: cada entrada tem de aparecer literalmente no `trecho` de alguma linha da leitura — entrada que o jogo não escreve **reprova** (o teste planta `"Dodge Chance: "`) |

### 9.7 O que é decisão do dono (o que este capítulo NÃO decide)

1. **As 14 notas fundidas com UMA quebra no fonte.** Em `TextFixes`, `\n<color=#C8B090>` (uma
   quebra) e `\n\n<color=#C8B090>` (duas) convivem: são **14 × 11** blocos. No tooltip **não
   aparece diferença nenhuma** (o prefixo normaliza, §9.4), mas o fonte fica fora da convenção
   escrita — e **duas** dessas 14 são das 12 notas de shrine curadas pelo dono. Como o efeito é
   só no fonte e o texto é dele, isto **não** foi mexido: **se ele quiser alinhar, é uma linha de
   decisão dele.**
2. **O comentário do nível 3 na tabela do §1/§2** continua sendo a contradição do §7.5 (fonte
   declarada bege). Este capítulo não toca nisso.
3. **O que é “parede de texto”** (§4): comprimento é medido, não reprovado. O formato não muda
   isso — decisão dele.

---

## 9.8 A QUEBRA DO JOGO — o passo a passo, os três caminhos e a prova (BANCADA-1, 01/10)

Este é o achado mais perigoso do dia porque ataca a **base** da prova: a bancada de teste e o
runtime discordavam sobre quantas quebras de linha o jogo escreve antes do `AP Cost`, e isso decidia
se **todo teste de formato** media o jogo ou media a bancada.

### 9.8.1 O critério e o passo a passo

O critério é **o que o jogo faz**, lido do decompilado do tipo `Tooltip` (o arquivo por tipo que o
`KANBAN` cita; a integral é `Assembly-CSharp.decompiled.cs`, classe `Tooltip`). O caminho é o
`ShowSkillTooltip` (l.1308-1575 do arquivo por tipo), e os quatro pontos que decidem o texto são:

| ponto | o que o código faz | quebras acumuladas antes do próximo trecho |
|---|---|---|
| l.1470 | `original += "\n";` — dentro do `if (skill.ActionsGranted != null && …)` | **1** (o `original` passa a terminar em quebra) |
| l.1536 | `original + "\n" + OptionsManager.Localize("AP Cost: 1")` | **2** → **UMA LINHA EM BRANCO antes do `AP Cost`** |
| l.1558/1565/1572 | `original + "\n" + "Range: …"` / `"Mana Cost: …"` / `"Cooldown: …"` | 1 cada (linhas **seguidas**, sem linha em branco) |
| l.1523 (a chamada) → l.597 (`Description.text = description`) | o corpo vai **cru** para o TMP | nada colapsa: a linha em branco aparece |

Nada entre a l.1470 e a l.1536 toca o `original` — são só leituras de custo e alcance. Logo o texto
do jogo é, literalmente:

```
Deals 42 lightning damage to all enemies within a line.
                                          <- as DUAS quebras: descrição ↔ AP Cost
AP Cost: 2
Range: Line
```

E a bancada montava `texto.rstrip("\n") + "\n" + custo` — **uma** quebra, ou seja **sem** a linha em
branco. Não era um detalhe de estilo: era o texto do jogo faltando.

### 9.8.2 Os três caminhos de montagem (o que vale em cada um)

| caminho | quem monta | quebras antes do bloco final | tem `AP Cost`? |
|---|---|---|---|
| **skill** | `Tooltip.ShowSkillTooltip` (l.1308-1598) | **2** (l.1470 + l.1536) → uma linha em branco | sim (`AP Cost`, `Range`, `Blast Radius`, `Mana Cost`, `Cooldown`) |
| **status** | `Tooltip.ShowActionStatusTooltip` (l.971-1022) | **2** escritas de uma vez (`text + "\n\n" + "Duration Type"…`, l.1013); o texto sai `Trim()`ado depois (l.1015) | não — o bloco final é `Duration Type` |
| **ground effect** | `Tooltip.ShowGroundEffectTooltip` (l.1219-1304) | **nenhuma**: as partes vêm com **uma** quebra cada | **não** — não existe custo nenhum neste caminho |

No **ground effect** o corpo é `TÍTULO` + `<size>` + descrição (+ `Turns Remaining`, + linha de
TIME) + `</size>` (l.1243/1244/1254/1278/1291), e a única linha em branco é a que separa ground
effects **distintos** (o dicionário é reescrito com `"\n\n"` entre as entradas, l.1298). **A tooltip
de SHRINE é deste caminho** — e a bancada modelava `caso_shrine` como **skill**, com `AP Cost` e
`Range: Melee`. Era um texto que o jogo não monta naquele caminho.

### 9.8.3 Quem estava errado — e o que NÃO precisou mudar

* **errada: a bancada.** `regras_cor.monta_a_descricao` juntava os custos com uma quebra. Corrigido
  para as duas da l.1470 + l.1536 (constante `QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA`, conferida contra a
  leitura).
* **errada: a regra do checador.** `defeitos_de_linha_em_branco` só aceitava a linha em branco que
  separa **bloco do mod** — e por isso acusava o texto **do jogo** de “linha em branco órfã”. Agora
  ela aceita também a linha em branco seguida da **PRIMEIRA** linha de custo/metadados do **jogo**
  (`AP Cost` da skill, `Duration Type` do status — e só elas; a restrição é o **BANCADA-2**, §9.8.6),
  lidas da fixture. Ganhou o defeito simétrico: `defeitos_da_quebra_do_jogo` reprova o bloco de
  custos que ficou **sem** a linha em branco do jogo.
* **errado: o §9.2** (o exemplo mostrava o `AP Cost` colado na descrição) e o §9.1 (“não existe
  linha em branco em nenhum outro lugar”, lido como se valesse para o tooltip inteiro). O §9.3 e o
  §9.4 **mostravam** a linha em branco antes do `AP Cost` — estavam certos nesse ponto, e é essa a
  contradição interna que o BANCADA-1 fechou (§9.4 ganhou o motivo do nome “órfã”).
* **certo: o código do mod.** O `InicioDoSeparador` consumir as **duas** quebras é exatamente o que
  **preserva** a linha em branco do jogo. Consumindo uma só, o `original` (que termina com a quebra
  da l.1470) deixa **duas** linhas em branco seguidas — o defeito do RV-17(a). Não houve uma linha
  de `LocalizePatch.cs` a mudar, e a NIV3-1 (que estava no arquivo) não foi tocada.

### 9.8.4 A leitura, a fixture e a prova REPROVANDO

A leitura virou fixture versionada: `tools/testes/fixtures/formato-notas.entrada.json` — os trechos
**literais** do decompilado (com procedência, linha e método), o ramo que executa em cada um, e o
número de quebras **contado dos escapes `\n` do próprio trecho** (nada digitado à mão). O teste
confere os trechos contra o decompilado quando ele existe nesta máquina (`scratch/rv22/tooltip.cs`,
`SR_DECOMPILADO` ou o cache) e, sempre, a consistência interna (o ramo dentro do trecho; a contagem
batendo).

A prova tem as duas metades, e o caso que **separa** os dois mundos é o do caminho da skill:

```
JOGO:    "... damage.\n\nAP Cost: 1\nRange: Melee\n\n[nota]"
BANCADA: "... damage.\nAP Cost: 1\nRange: Melee\n\n[nota]"      <- a bancada de antes do BANCADA-1
```

* com a bancada de **antes** (uma quebra), `t_formato_notas.py` **REPROVA**:
  `formato QUEBRADO em 'skill com dano (TextAppends)': ["o custo 'AP Cost: 1' ficou SEM a linha em
  branco que o JOGO escreve antes dele"]`;
* com a de **hoje** (as duas da leitura), o mesmo caso **passa** — e a igualdade
  `texto_da_bancada == texto_do_runtime` é asserção, não opinião;
* a contra-prova executável é o par `cp_formato_quebra_do_jogo_isca.py` (declara 1 quebra → reprova
  citando o motivo, imprimindo os dois textos) × `..._ok.py` (declara o número da leitura → passa).

**Como se sabe que a checagem não é decorativa:** o defeito plantado “o bloco de custos sem a linha
em branco do jogo” tem de ser **visto** (`_checador_nao_e_vazio`), e o texto do runtime tem de
passar limpo — antes do BANCADA-1 ele era o texto que o checador **reprovava**.

### 9.8.5 As duas divergências menores, fechadas junto

1. **`caso_shrine` modelava uma SKILL.** A tooltip de shrine é a de **ground effect** (§9.8.2): sem
   `AP Cost`/`Range`, com título + `<size>` + `Turns Remaining` + linha de TIME. O caso foi
   reescrito com a moldura real (`regras_cor.molda_ground_effect`) e a trava agora exige que ele
   **não** traga custo de skill.
2. **a busca da nota usava `"color="`, o C# usa `"color=#"`.** `regras_cor.tira_a_nota_do_mod`
   procurava a abertura sem o `#`, mais frouxa que o `const string abertura = "<color=#"` do
   `TirarNotaDoMod`: aceitaria um `<color=Nome>` que o código não aceita. Alinhado (`ABRE_COR_COM_HASH`),
   e o par `"<color=" + hex` ganhou guarda (`_com_cerquilha`): um hex sem `#` agora **falha alto** em
   vez de montar um bloco que nenhuma busca acha.

### 9.8.6 O AFROUXAMENTO DO CONSERTO — a linha em branco SÓ na PRIMEIRA linha de custo (BANCADA-2, 01/10)

O BANCADA-1 acertou o alvo (a bancada voltou a reproduzir o jogo) e trouxe **um afrouxamento de
brinde**, medido pela revisão (BANCADA-1R) **executando** o checador: `eh_linha_do_jogo` liberava o
**bloco INTEIRO** de custo do caminho da skill — `AP Cost`, `Range`, `Blast Radius`, `Mana Cost`,
`Cooldown`. Mas o jogo só escreve a linha em branco antes da **PRIMEIRA** linha de custo de cada
caminho (o `AP Cost` da skill, l.1470+l.1536; o `Duration Type` do status, l.1013); as **seguintes**
vêm com **uma** quebra cada (l.1558/1561/1565/1572). Resultado: a forma

```
descricao \n\n AP Cost: 1 \n\n Range: Melee
```

— e as variantes com `Blast Radius`, `Mana Cost` e `Cooldown` — **reprovava** antes do BANCADA-1 e
**passava** depois dele. É uma forma que o **jogo nunca escreve**.

**A correção (restrição).** `regras_formato.linhas_do_jogo()` passa a devolver **só a primeira linha
de custo de cada caminho** — e a classificação **não é digitada à mão**: sai do `trecho` **verificado**
da fixture (`reg.primeiras_linhas_de_custo` = as entradas de `custo_no_texto` que aparecem
literalmente no `trecho` de uma linha do grupo `linhas`, os pontos onde o jogo escreve as duas
quebras, conferidos contra o decompilado). O conjunto do bloco inteiro fica em
`linhas_do_jogo_do_bloco_inteiro()` **só para a contra-prova** reproduzir o defeito.

**A borda só existe com o teste que a pega.** O caso plantado “linha em branco antes do `Range`” (e
as outras linhas seguintes) é exigido em `t_formato_notas.py` — o checador **tem** de vê-lo — e o par
`cp_formato_linha_antes_do_range_isca.py` × `..._ok.py` prova as duas metades: a isca declara o
conjunto do BANCADA-1 (bloco inteiro) e **reprova** (o texto plantado passava limpo — a borda era
cega); a metade ok declara o conjunto de hoje e **passa** (o defeito é visto). A prova medida está em
`tools/testes/bancada2-prova-linha-antes-do-range.log`.

**E a lista à mão deixou de ser sem controle.** A `custo_no_texto` (a lista que alimenta o checador)
era escrita à mão e não tinha trava: `reg.controle_das_linhas_de_custo()` agora exige que **cada**
entrada apareça literalmente no `trecho` de alguma linha da leitura — uma linha que o jogo não
escreve **reprova** —, e o teste planta uma entrada falsa (`"Dodge Chance: "`) para provar que o
controle **dispara**. As duas metades juntas são o que fecha o escopo: a derivação vem do trecho
verificado, e a lista tem um controle que reprova se alguém mexer.
