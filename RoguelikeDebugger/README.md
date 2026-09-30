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
- **Itens** — inventário dos itens (tipo, raridade, descrição opcional, atributos, proporção de armadura, ação de consumível) e dos afixos.
- **Powerups** — inventário dos powerups do roguelike, uma linha por nível.
- **Loot, ouro e experiência** — as decisões de roll, os modificadores aplicados e os valores concedidos.

É a fonte dos CSVs de cobertura em `docs/cobertura/` dos outros mods do projeto (ex.: o censo que alimenta a revisão de tooltips do BetterTooltips). Sem ele, revisar texto é leitura de prosa; com ele, cada número do tooltip pode ser cruzado com o código.

> **Por que ele não entra em pacote "para amigos":** o dump é enorme e despeja **milhares** de linhas no log a cada boot, deixando o `LogOutput.log` ilegível para quem só quer jogar.

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

## Compilar do fonte

```powershell
cd RoguelikeDebugger
dotnet build
```

Saída: `bin\Debug\netstandard2.1\RoguelikeDebugger.dll`

As DLLs de referência (BepInEx, Unity, `Assembly-CSharp`) vêm de `..\lib\` e **nunca são distribuídas**: a `Assembly-CSharp.dll` é propriedade do jogo.
