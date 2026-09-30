# Changelog — RoguelikeQoL

## 0.1.0

Primeira versão publicada.

- **HUD de modificadores da run**: painel sobreposto no canto superior esquerdo com os agregados da party — **Treasure Find** (`Σ DropQuantityMod`), **Gold Find** (`Σ GoldMod`) e o **Exp Mod** da batalha atual.
- Valores lidos das **mesmas fontes que o jogo usa** (`GetCharacterLootDropModifier`, `ApplyGoldModifiers`, `CurrentBattle.expModifier`) — sem número inventado.
- **Vem desligado por padrão** (`AtivarHUD = false` no `BepInEx\config\com.gumatos.roguelikeqol.cfg`). Para ligar, basta editar o `.cfg` no Notepad e reiniciar — não precisa recompilar.
- A criação do updater é **preguiçosa** (primeira UI viva, via `OptionsManager.Localize`): um GameObject criado no `Awake` do plugin é destruído pelo jogo na primeira carga de cena, e o HUD nunca aparecia.
- **Sem qualquer alteração de gameplay.**

### Correção do aplicador de ganchos (mesma versão, sem subir número)

- A troca do `PatchAll()` por **aplicação gancho a gancho** (que entrou nesta versão) veio acompanhada de um filtro de classe de gancho que exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no método**. Este mod declara o gancho pela **convenção de nome** do Harmony (`LocalizeHudTrigger.Postfix`), que o Harmony aceita exatamente como o atributo — o filtro recusava a única classe de patch: o mod **carregava, logava "carregado." e não aplicava gancho nenhum** (o silêncio parecendo sucesso; era o defeito A-1 da REV-2, em 4 mods).
- O filtro agora exige só `[HarmonyPatch]` **no TIPO** — o mesmo conjunto de classes que o `PatchAll()` processava. Medido invocando o filtro real da DLL construída: **1 de 1 classe de patch aceita e 1 método de gancho dentro** (antes: 0 de 1). Em todo o projeto, os 4 mods afetados passaram de 0/14 para **14/14** classes de patch aceitas.
- A versão **não** subiu: o defeito foi corrigido antes de qualquer download e a correção não muda nada no caminho feliz.

### Histórico de escopo

Este mod era maior e foi dividido em projetos independentes: a troca de fonte saiu como **BetterFont** e o display de stats `base (combinado)` saiu como **BetterStats**. Hoje o RoguelikeQoL tem **só** o HUD.
