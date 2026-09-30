# Changelog — RoguelikeDebugger

> Ferramenta de **desenvolvimento**, não mod de jogador.

## 0.1.0

Primeira versão publicada.

- **Dump dos dados internos do jogo no `LogOutput.log`** (apenas logs, nenhuma alteração de gameplay):
  - **Skills**: inventário com nome, descrição, expressões de descrição, ações concedidas, efeitos de atributo e gatilhos.
  - **Ações** (`[ActionProps]` / `[Trigger]`): tipo, alvos, alcance máximo, knockback, número de golpes, cooldown, cargas, condições de uso, chances e status aplicados.
  - **Status**: inventário de buffs/debuffs com efeitos de atributo e descrição.
  - **Itens e afixos**: tipo, raridade, descrição opcional, atributos, proporção de armadura e ação de consumível.
  - **Powerups**: inventário do roguelike, uma linha por nível.
  - **Loot, ouro e experiência**: os rolls, os modificadores aplicados e os valores concedidos.
- É a fonte dos CSVs de cobertura em `docs/cobertura/` usados pelos outros mods do projeto.
- **Não distribuir para amigos**: enche o log com milhares de linhas a cada boot.
