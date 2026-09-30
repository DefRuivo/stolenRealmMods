# BetterTooltips

Mod **BepInEx 5** para **Stolen Realm** que reescreve os tooltips de skills e status do jogo para eles **não mentirem por omissão**, e corrige defeitos objetivos de texto. **Não altera gameplay.**

- **GUID:** `com.gumatos.bettertooltips`
- **Versão:** 0.1.1
- **Compatível com:** Stolen Realm **v1.3.1** (versão mais recente do jogo em 30/09/2026).
- **Dependências:** nenhuma além do BepInEx 5 (que o r2modman já instala no perfil).

## O que ele faz

O jogo explica as skills no texto do tooltip, mas às vezes **deixa de fora a metade que decide o jogo**: de qual atributo vem o número, o limite de stacks, a duração, quem é afetado, o gatilho, o número de golpes. O texto não está errado — está incompleto, e o jogador decide com informação faltando.

O mod complementa esse texto:

- Todo texto do jogo passa pelo funil de localização (`OptionsManager.Localize`). O mod intercepta esse funil e compara a string com uma tabela de correções e de notas de mecânica.
- A explicação que falta é **acrescentada ao fim do tooltip**, depois dos custos e do alcance, na **cor de texto especial do próprio jogo** — assim ela se distingue do texto oficial.
- Defeitos objetivos (grafia, pontuação, espaço duplo) são corrigidos direto.

Cada correção é baseada no código do jogo (decompilado do `Assembly-CSharp.dll`), não em opinião.

## Números das auras de shrine

Os tooltips de **shrine** do jogo mostravam sempre o valor **base** — mesmo para quem tinha o bônus que multiplica a aura. O mod faz a conta com o **bônus real do personagem em foco**:

- **Auras de buff**: o valor sai já multiplicado pelo *Shrine Effect Bonus* — **Omnism I/II** (Chaos), o perk **`Worship`** (`100% increased effect from Shrines`) e o **Horn of Devotion**. Um `20%` base vira o número que você realmente recebe. A nota de cada uma das **9 chaves** (Warrior, Guardian, Conqueror, Rogue, Reaper, Seraph, Shaman, Energy e **Fury**) diz a **base** e que o valor mostrado **já inclui** esse bônus — a do `Fury` é `Base 25% damage and +25% damage taken.` com a mesma cadeia das outras.
- **Energy Coil — o rótulo segue o SINAL do total**: `Mana Costs reduced by 50%` quando o total do atributo é **negativo** (a aura empurra o custo para baixo) e `Mana Costs increased by 20%` quando fontes **positivas** do mesmo atributo — `Forbidden Power` (`+50`), `Fuel for the Flames I/II` (`+20`/`+30`) — superam a aura. Antes a linha assumia total negativo e imprimia `reduced by -20%`.
- **Linha `Your active shrine auras:`**: um bloco que lista **todas as auras de shrine que o personagem está recebendo naquele momento** (por atributo). Quem está **fora** da aura não vê a linha.
- **Decay Shrine**: a linha do jogo ganha o **dano por turno literal** (ex.: `20 damage per turn for you`), sobre a **sua** vida máxima e o **seu** bônus. Com `Worship`, dobra.
- **Flame Shrine**: o dano é **por alvo** — um item para cada personagem na área da aura (party e inimigos), porque no hover ainda não se sabe **quem vai atacar**. Cada alvo usa a vida máxima, o tipo e o bônus **dele**: o número é a **projeção do ocupante como atacante** (*if this character attacked*), e a nota diz isso.
- **Sustenance I/II**: o tooltip de cada **globule** (e dos pickups de poção) mostra a cura real — 8%, 20% ou a soma das tiers ativas — sobre a sua vida e a sua mana máximas.

> **O número é cru, antes de qualquer redução de dano** — as notas de Decay e Flame dizem isso: não entra armadura, resistência nem mitigação posterior. Quando não há prova (personagem fora da aura, atributo ausente no build, expressão não avaliável), o texto original fica **intacto** e o log diz o motivo: o mod **não estima**.

**Conferência:** os números foram escritos contra o código e os assets do jogo, e o **fator do `Worship` (o dano dobra)** foi **medido em jogo** pelo autor. A **conferência visual final das linhas novas em jogo ainda não foi feita** depois da última revisão — se algo não corresponder ao que aparece na tela, é aqui que se reporta.

## O que ele NÃO faz

- **Não altera gameplay** — nenhum valor, dano, custo ou regra muda; o mod só reescreve texto.
- **Não modifica nenhum arquivo do jogo** (nem save) e não deixa resíduo.
- **Não revela o sorteio do Chaos** — é intencional: a graça da árvore é não saber o resultado.
- **Não mostra número quando não há prova** — prefere deixar o texto original a inventar um valor.
- **Não aplica mitigação** ao número que exibe: ele é o cru da fórmula do jogo.

## Instalar

**Pelo r2modman (recomendado):** instale este pacote no perfil do Stolen Realm — o r2modman coloca a DLL em `BepInEx\plugins\BetterTooltips\`.

**Manual:**

1. Instale o **BepInEx 5 x64** no jogo (ou dê "Start modded" uma vez no r2modman, que cria a pasta).
2. Copie a pasta `BetterTooltips` para:
   ```text
   %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
   ```
   Deve ficar: `...\plugins\BetterTooltips\BetterTooltips.dll`
3. Abra o jogo. No `LogOutput.log` deve aparecer:
   ```text
   [Info   :Better Tooltips] Better Tooltips carregado.
   ```

## Como desfazer

Apague a pasta `BepInEx\plugins\BetterTooltips\` (ou desabilite o pacote no r2modman) e abra o jogo de novo. O mod não modifica nenhum arquivo do jogo e não deixa resíduo.

## Compilar do fonte

```powershell
cd BetterTooltips
dotnet build
```

Saída: `bin\Debug\netstandard2.1\BetterTooltips.dll`

As DLLs de referência (BepInEx, Unity, `Assembly-CSharp`) vêm de `..\lib\` e **nunca são distribuídas**: a `Assembly-CSharp.dll` é propriedade do jogo.
