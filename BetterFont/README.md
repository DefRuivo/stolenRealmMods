# BetterFont

Mod **BepInEx 5** para **Stolen Realm** que troca a fonte renderizada do jogo por uma **serifada (Times New Roman**, com fallback Georgia / Liberation Serif). **Não altera gameplay.**

- **GUID:** `com.gumatos.betterfont`
- **Versão:** 1.0.0
- **Dependências:** nenhuma além do BepInEx 5 (que o r2modman já instala no perfil).

## O que ele faz

- Substitui a fonte de **todos os textos TMP** do jogo por um asset serifado — inclusive telas que abrem depois do boot (level up, tooltips, menus de configuração).
- A **fonte original do jogo entra como fallback** do asset serifado: ícones, glifos e símbolos que a Times New Roman não tem continuam renderizando, sem virar quadradinho.
- A varredura roda com **tempo real**, então funciona mesmo com `timeScale = 0` (é o caso dos menus do Stolen Realm, onde coroutines e `InvokeRepeating` nunca disparam).
- O updater é criado de forma **preguiçosa**, na primeira UI viva (gatilho em `OptionsManager.Localize`). Criá-lo no `Awake` do plugin não funciona: o jogo destrói o GameObject na primeira carga de cena.
- **Sem qualquer alteração de gameplay** — só a aparência do texto muda.

## Instalar

**Pelo r2modman (recomendado):** instale este pacote no perfil do Stolen Realm — o r2modman coloca a DLL em `BepInEx\plugins\BetterFont\`.

**Manual:**

1. Instale o **BepInEx 5 x64** no jogo (ou dê "Start modded" uma vez no r2modman, que cria a pasta).
2. Copie a pasta `BetterFont` para:
   ```text
   %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
   ```
   Deve ficar: `...\plugins\BetterFont\BetterFont.dll`
3. Abra o jogo. No `LogOutput.log` deve aparecer:
   ```text
   [Info   :Better Font] Better Font carregado.
   ```

## Como desfazer

Apague a pasta `BepInEx\plugins\BetterFont\` (ou desabilite o pacote no r2modman) e abra o jogo de novo. A fonte original volta no próximo boot — o mod não modifica nenhum arquivo do jogo nem deixa resíduo.

## Compilar do fonte

```powershell
cd BetterFont
dotnet build
```

Saída: `bin\Debug\netstandard2.1\BetterFont.dll`

As DLLs de referência (BepInEx, Unity, `Assembly-CSharp`) vêm de `..\lib\` e **nunca são distribuídas**: a `Assembly-CSharp.dll` é propriedade do jogo.
