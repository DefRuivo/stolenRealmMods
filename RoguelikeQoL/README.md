# RoguelikeQoL

Mod **BepInEx 5** para **Stolen Realm** com melhorias de qualidade de vida no **modo roguelike**. **Não altera gameplay.**

- **GUID:** `com.gumatos.roguelikeqol`
- **Versão:** 0.1.0
- **Dependências:** nenhuma além do BepInEx 5 (que o r2modman já instala no perfil).

## O que ele faz

**HUD de modificadores da run** — um painel sobreposto no canto superior esquerdo com os agregados da party:

| Linha | Significado |
|---|---|
| Treasure Find | soma de `DropQuantityMod` de todos os personagens da party |
| Gold Find | soma de `GoldMod` de todos os personagens da party |
| Exp Mod | modificador de experiência da batalha atual |

Os valores são lidos **das mesmas fontes que o jogo usa** (`GetCharacterLootDropModifier`, `ApplyGoldModifiers`, `CurrentBattle.expModifier`), então não há número inventado nem divergência com o comportamento real.

> **O HUD vem DESLIGADO por padrão.** Para ligar sem recompilar nada, edite o arquivo de config e mude `AtivarHUD = false` para `true`:
> ```text
> BepInEx\config\com.gumatos.roguelikeqol.cfg
> ```

Este mod é **só** o HUD. A troca de fonte virou o mod **BetterFont** e o display de stats `base (combinado)` virou o mod **BetterStats** — são projetos independentes, cada um pode ser instalado ou removido sozinho.

## Instalar

**Pelo r2modman (recomendado):** instale este pacote no perfil do Stolen Realm — o r2modman coloca a DLL em `BepInEx\plugins\RoguelikeQoL\`.

**Manual:**

1. Instale o **BepInEx 5 x64** no jogo (ou dê "Start modded" uma vez no r2modman, que cria a pasta).
2. Copie a pasta `RoguelikeQoL` para:
   ```text
   %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
   ```
   Deve ficar: `...\plugins\RoguelikeQoL\RoguelikeQoL.dll`
3. Abra o jogo. No `LogOutput.log` deve aparecer:
   ```text
   [Info   :Roguelike QoL] Roguelike QoL carregado — HUD DESABILITADO (AtivarHUD=false no config).
   ```
4. Para ver o HUD, mude `AtivarHUD` para `true` no `.cfg` e abra o jogo de novo.

## Como desfazer

Dois caminhos, ambos sem desinstalar nada:

- **Só desligar o HUD:** mude `AtivarHUD = false` no `BepInEx\config\com.gumatos.roguelikeqol.cfg` e reinicie o jogo.
- **Remover o mod:** apague a pasta `BepInEx\plugins\RoguelikeQoL\` (ou desabilite o pacote no r2modman) e abra o jogo de novo.

O mod não modifica nenhum arquivo do jogo e não deixa resíduo.

## Compilar do fonte

```powershell
cd RoguelikeQoL
dotnet build
```

Saída: `bin\Debug\netstandard2.1\RoguelikeQoL.dll`

As DLLs de referência (BepInEx, Unity, `Assembly-CSharp`) vêm de `..\lib\` e **nunca são distribuídas**: a `Assembly-CSharp.dll` é propriedade do jogo.
