# RoguelikeSkillTreeVisualizer

- **Version:** 0.3.9
- **Author:** gumatos
- **Tested on:** Stolen Realm 1.4.9, Steam public build 26878331, in Roguelike mode.
- **Requires:** BepInEx 5 and RealmApi 0.1.2 or newer, installed as separate packages.

Opens a read-only view of the native skill tree for the current character. Use **Skills** where the button is available, the tree tab in the Roguelike character menu, or the configurable **F10** shortcut. The mod does not spend skill points or change gameplay. Available classes still depend on what the game exposes.

This update keeps the added tab from crowding the native header controls. The header and its buttons were checked at 1920×1080 and 1600×900. In Brazilian Portuguese the tab reads **Árvores**.

## Install and configure

Use r2modman to install the package and its dependencies in your Stolen Realm profile. For a manual install, place the `plugins/RoguelikeSkillTreeVisualizer/` folder in `BepInEx/plugins/` and install the dependencies separately. To adjust the shortcut, edit `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg` after the first modded launch. The Visualizer does not require RealmApi's optional hooks to be enabled.

## Uninstall or build

Disable the mod in r2modman or remove only its own folder from `BepInEx/plugins/`. Keep RealmApi if other mods rely on it. With local references in place, build using `dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj -c Release -p:DeployToBepInEx=false`.

## Português (BR)

Abre as árvores de habilidades no modo Roguelike para consulta, sem gastar pontos. A aba **Árvores** não cobre os botões nativos do cabeçalho nas duas resoluções testadas.
