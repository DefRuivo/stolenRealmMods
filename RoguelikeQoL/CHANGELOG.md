# Changelog — RoguelikeQoL

## 0.1.0

Primeira versão publicada.

- **HUD de modificadores da run**: painel sobreposto no canto superior esquerdo com os agregados da party — **Treasure Find** (`Σ DropQuantityMod`), **Gold Find** (`Σ GoldMod`) e o **Exp Mod** da batalha atual.
- Valores lidos das **mesmas fontes que o jogo usa** (`GetCharacterLootDropModifier`, `ApplyGoldModifiers`, `CurrentBattle.expModifier`) — sem número inventado.
- **Vem desligado por padrão** (`AtivarHUD = false` no `BepInEx\config\com.gumatos.roguelikeqol.cfg`). Para ligar, basta editar o `.cfg` no Notepad e reiniciar — não precisa recompilar.
- A criação do updater é **preguiçosa** (primeira UI viva, via `OptionsManager.Localize`): um GameObject criado no `Awake` do plugin é destruído pelo jogo na primeira carga de cena, e o HUD nunca aparecia.
- **Sem qualquer alteração de gameplay.**

### Histórico de escopo

Este mod era maior e foi dividido em projetos independentes: a troca de fonte saiu como **BetterFont** e o display de stats `base (combinado)` saiu como **BetterStats**. Hoje o RoguelikeQoL tem **só** o HUD.
