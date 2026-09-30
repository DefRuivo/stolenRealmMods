> ⚠️ **Ferramenta de desenvolvimento — NÃO é um mod de jogador.**
> Este pacote não melhora nada na experiência de jogar. Ele existe para **investigar as mecânicas
> internas do Stolen Realm** durante o desenvolvimento de outros mods.

# RoguelikeDebugger

Mod **BepInEx 5** de **investigação** para **Stolen Realm**: faz **dump dos dados internos do jogo** no `LogOutput.log` para que as mecânicas possam ser confirmadas no código, não de ouvir falar.

- **GUID:** `com.gumatos.roguelikedebugger`
- **Versão:** 0.1.0
- **Compatível com:** Stolen Realm **v1.3.1** (versão mais recente do jogo em 30/09/2026).
- **Dependências:** nenhuma além do BepInEx 5 (que o r2modman já instala no perfil).

## O que ele faz

**Apenas logs. Nenhuma alteração de gameplay.** Ele registra no `LogOutput.log`:

- **Skills** — inventário de skills do jogo (nome, descrição, expressões, ações concedidas, efeitos de atributo, gatilhos) e as propriedades das **ações** (alcance, alvos, número de golpes, cooldown, cargas, status aplicados).
- **Status** — inventário dos status/buffs/debuffs com os efeitos de atributo e a descrição.
- **Efeitos por tipo concreto** — os arrays `Effects` de status e de ação são `IEffectInfo[]` (interface vazia): o dump publica o tamanho do array, o **tipo concreto de cada elemento** e os campos daquele tipo (por reflexão), mais os gatilhos do status. Ver a seção "Efeitos por tipo concreto" abaixo.
- **Itens** — inventário dos itens (tipo, raridade, descrição opcional, atributos, proporção de armadura, ação de consumível) e dos afixos.
- **Powerups** — inventário dos powerups do roguelike, uma linha por nível.
- **Loot, ouro e experiência** — as decisões de roll, os modificadores aplicados e os valores concedidos.

É a fonte dos CSVs de cobertura em `docs/cobertura/` dos outros mods do projeto (ex.: o censo que alimenta a revisão de tooltips do BetterTooltips). Sem ele, revisar texto é leitura de prosa; com ele, cada número do tooltip pode ser cruzado com o código.

> **Por que ele não entra em pacote "para amigos":** o dump é enorme e despeja **milhares** de linhas no log a cada boot, deixando o `LogOutput.log` ilegível para quem só quer jogar.

## O que ele NÃO faz

- **Não altera gameplay nem o save** — a única saída do mod é texto no `LogOutput.log`.
- **Não melhora a experiência de jogar** — é ferramenta de investigação, não mod de jogador.
- **Não envia dado nenhum para fora**: tudo fica no log local, no seu computador.

## Instalar

Este pacote só faz sentido para quem vai **desenvolver/investigar**.

1. Instale o **BepInEx 5 x64** no jogo (ou dê "Start modded" uma vez no r2modman, que cria a pasta).
2. Copie a pasta `RoguelikeDebugger` para:
   ```text
   %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
   ```
   Deve ficar: `...\plugins\RoguelikeDebugger\RoguelikeDebugger.dll`
3. Abra o jogo uma vez (o dump sai no boot, não precisa entrar em partida) e leia:
   ```text
   ...\BepInEx\LogOutput.log
   ```
   O log é **sobrescrito a cada início** do jogo.

## Como desfazer

Apague a pasta `BepInEx\plugins\RoguelikeDebugger\` (ou desabilite o pacote no r2modman) e abra o jogo de novo. O mod não modifica nenhum arquivo do jogo e não deixa resíduo.

## Efeitos por tipo concreto (RV-8b-0g)

O campo `Effects` de status e de ação é `IEffectInfo[]` — uma **interface vazia** (l.322255 do decompilado). O dump antigo lia cada elemento com `e as GeneralEffect` (`Patches/ActionStatusInventoryPatch.cs:84` e `Patches/SkillInventoryPatch.cs:367`) para publicar o campo `Action`. Em todo elemento cujo tipo concreto **não** seja `GeneralEffect` esse cast devolve `null` e o dado desaparecia do dump — foi o que deixou 2 entradas do censo de tooltips como `indeterminado`. A montagem tem **duas** implementações da interface:

| Tipo concreto | Campos | Onde |
|---|---|---|
| `GeneralEffect` | `Action` | l.322250 |
| `CharacterVariableEffectInfo` | `EffectTarget`, `CharacterVariableAttribute`, `Amount` | l.320295 |

Campos novos (sempre **antes** de `desc=`, que continua por último; nenhum valor com `|` nem aspas dentro):

| Categoria | Campos novos |
|---|---|
| `[Status]` | `nEfeitosTot` (`Effects.Length`), `efTipos` (índice:tipo{campos} de **cada** elemento), `nAttrEf`, `attrTipos` (os `AttributeEffects` por reflexão), `nTrig`, `trigEf` (gatilhos do status: tipo, efeitos, condição e status aplicados) |
| `[Action]` | `nEfeitosTot`, `efTipos` |
| `[Skill]` | `nAttrEf`, `attrTipos` |
| `[Item]` | `consEf` (efeitos da ação de consumível, por tipo concreto) |

Depois de cada categoria sai uma linha de resumo, `[Efeitos] resumo (status|skills|acoes|itens): total=N | porTipo={Tipo=N; ...} | naoGeneralEffect=N`. É a prova, no próprio log, de que existe elemento que **não** é `GeneralEffect` — e de quantos o cast antigo descartava. O `naoGeneralEffect` conta só os elementos de array `IEffectInfo[]` (os `Effects`); `AttributeEffects` e `SkillTrigger.GeneralEffects` são arrays de tipo **concreto** e nunca perderam dado.

Exemplo de saída (`efTipos`):

```text
efTipos=0:GeneralEffect{Action=Target.Health -= 5}; 1:CharacterVariableEffectInfo{Amount=MaxHealth * 0.1f;CharacterVariableAttribute=<nome do asset>;EffectTarget=Target}
```

A leitura é por **reflexão** (`EfeitosInfo.cs`), não por cast: cobre os dois tipos sem referenciar nenhum deles e, se o jogo ganhar um terceiro tipo numa versão futura, ele aparece no dump sem recompilar o mod. `SkillTrigger.GeneralEffects` é `GeneralEffect[]` (array **concreto**, l.45797): naquele caminho o cast nunca falhou — o que faltava era o campo existir no dump.

> Os CSVs do censo em `docs/cobertura/` só recebem as colunas que o parser de `tools/census.py` conhece. Estes campos saem no **log** e entram no CSV quando o parser for estendido.

## O que só se confirma com o jogo aberto

Esta mudança foi verificada por **compilação** (0 erros) e por um teste **offline** que exercita a reflexão contra os tipos reais do `Assembly-CSharp` (um projeto console descartável, fora do pacote, que referencia `..\lib\Assembly-CSharp.dll` e compila o mesmo `EfeitosInfo.cs`). O que **só sai com o jogo rodando**:

- os **números** do dump: quantos status/ações têm elemento que não é `GeneralEffect` e quantos são (`[Efeitos] resumo`). Nenhum número sai daqui antes de rodar — o mod só publica o que lê do jogo;
- **qual** é o tipo concreto em `Champion of Blood` e `Frenzy`: o mod imprime o nome do tipo e os campos de cada elemento, e é essa leitura que fecha as 2 entradas `indeterminado` do censo;
- se o `Amount`/`CharacterVariableAttribute` desses dois casos explica o que o texto promete (é leitura de dado, não de prosa).

Como conferir (jogo aberto uma vez; o dump sai no boot, não precisa entrar em partida):

```text
...\BepInEx\LogOutput.log
```

```bash
# o resumo de tipos por categoria (a prova do defeito antigo)
grep -a "\[Efeitos\] resumo" "$APPDATA/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log"
# as duas entradas que ficaram indeterminadas no censo
grep -aE "'(Champion of Blood|Frenzy)'" "$APPDATA/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log"
```

## Compilar do fonte

```powershell
cd RoguelikeDebugger
dotnet build
```

Saída: `bin\Debug\netstandard2.1\RoguelikeDebugger.dll`

As DLLs de referência (BepInEx, Unity, `Assembly-CSharp`) vêm de `..\lib\` e **nunca são distribuídas**: a `Assembly-CSharp.dll` é propriedade do jogo.
