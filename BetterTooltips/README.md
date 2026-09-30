# BetterTooltips

Mod **BepInEx 5** para **Stolen Realm** que reescreve os tooltips de skills e status do jogo para eles **não mentirem por omissão**, e corrige defeitos objetivos de texto. **Não altera gameplay.**

- **GUID:** `com.gumatos.bettertooltips`
- **Versão:** 0.1.0
- **Dependências:** nenhuma além do BepInEx 5 (que o r2modman já instala no perfil).

## O que ele faz

O jogo explica as skills no texto do tooltip, mas às vezes **deixa de fora a metade que decide o jogo**: de qual atributo vem o número, o limite de stacks, a duração, quem é afetado, o gatilho, o número de golpes. O texto não está errado — está incompleto, e o jogador decide com informação faltando.

O mod complementa esse texto:

- Todo texto do jogo passa pelo funil de localização (`OptionsManager.Localize`). O mod intercepta esse funil e compara a string com uma tabela de correções e de notas de mecânica.
- A explicação que falta é **acrescentada ao fim do tooltip**, depois dos custos e do alcance, na **cor de texto especial do próprio jogo** — assim ela se distingue do texto oficial.
- Defeitos objetivos (grafia, pontuação, espaço duplo) são corrigidos direto.

Cada correção é baseada no código do jogo (decompilado do `Assembly-CSharp.dll`), não em opinião.

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
