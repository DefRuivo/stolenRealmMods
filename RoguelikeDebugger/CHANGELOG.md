# Changelog — RoguelikeDebugger

> Ferramenta de **desenvolvimento**, não mod de jogador.

## Não lançado

- **Efeitos por TIPO CONCRETO (RV-8b-0g).** Os arrays `Effects` (de status e de ação) são `IEffectInfo[]`, interface vazia: o cast `e as GeneralEffect` que o dump usava para ler o `Action` devolve `null` em todo elemento de outro tipo, e o dado desaparecia do dump (2 entradas do censo de tooltips ficaram `indeterminado` por isso). Agora:
  - campos novos `nEfeitosTot` / `efTipos` (status e ação): tamanho do array e **tipo concreto + campos de cada elemento**, lidos por reflexão;
  - `nAttrEf` / `attrTipos` (status e skill) e `consEf` (item) para os `AttributeEffects` e a ação de consumível;
  - `nTrig` / `trigEf` no `[Status]`: os gatilhos do status (tipo, efeitos, condição, status) — antes não saíam;
  - linha de resumo por categoria, `[Efeitos] resumo (...): total= | porTipo= | naoGeneralEffect=`.
  - `desc=` continua por último e nenhum valor contém `|` ou aspas: o formato antigo não muda.
  - Versão **não** subiu: os campos de dump deste mod entram sem bump (o `<Version>` é o marco de release; confira `python tools/check_versoes.py`).

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
