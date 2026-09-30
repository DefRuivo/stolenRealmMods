# BetterStats

Mod **BepInEx 5** para **Stolen Realm** que mostra os números de stats e atributos na **ficha de personagem** e na **tela de level up**, no formato **`base (combinado)`**. **Não altera gameplay.**

- **GUID:** `com.gumatos.betterstats`
- **Versão:** 1.0.0
- **Compatível com:** Stolen Realm **v1.3.1** (versão mais recente do jogo em 30/09/2026).
- **Dependências:** nenhuma além do BepInEx 5 (que o r2modman já instala no perfil).

## O que ele faz

O jogo mostra só um número final de cada atributo (Might, Dexterity, Vitality, Intelligence, Reflex). Isso esconde quanto veio de **pontos investidos** e quanto veio de **powerups, equipamento e skills** — justamente a informação que você precisa na hora de decidir onde investir.

O mod exibe os dois:

```text
Might        12 (18)
             ^^   ^^
             |    +-- valor FINAL (com powerups, equipamento e skills aplicados)
             +-- valor PURO (pontos investidos, de character.SavedMap)
```

- Funciona no painel **Attributes** da tela de inventário/personagem (`InventoryManager.UpdateStats`) e na tela de **level up** do roguelike (`RoguelikeManager`).
- De quebra, **corrige o layout** dessa coluna de valores: ela era alinhada à esquerda num X fixo e o texto vazava para fora do painel.
- Nenhum número é inventado: o valor puro vem do `SavedMap` do personagem e o combinado dos atributos finais do `Game`. O mod só formata o texto.

## Instalar

**Pelo r2modman (recomendado):** instale este pacote no perfil do Stolen Realm — o r2modman coloca a DLL em `BepInEx\plugins\BetterStats\`.

**Manual:**

1. Instale o **BepInEx 5 x64** no jogo (ou dê "Start modded" uma vez no r2modman, que cria a pasta).
2. Copie a pasta `BetterStats` para:
   ```text
   %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
   ```
   Deve ficar: `...\plugins\BetterStats\BetterStats.dll`
3. Abra o jogo. No `LogOutput.log` deve aparecer:
   ```text
   [Info   :Better Stats] Better Stats carregado.
   ```

## Como desfazer

Apague a pasta `BepInEx\plugins\BetterStats\` (ou desabilite o pacote no r2modman) e abra o jogo de novo. O mod não modifica nenhum arquivo do jogo e não deixa resíduo.

## Compilar do fonte

```powershell
cd BetterStats
dotnet build
```

Saída: `bin\Debug\netstandard2.1\BetterStats.dll`

As DLLs de referência (BepInEx, Unity, `Assembly-CSharp`) vêm de `..\lib\` e **nunca são distribuídas**: a `Assembly-CSharp.dll` é propriedade do jogo.
