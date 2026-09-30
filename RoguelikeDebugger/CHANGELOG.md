# Changelog — RoguelikeDebugger

> Ferramenta de **desenvolvimento**, não mod de jogador.

## 0.1.1

**Correção do aplicador de ganchos: a 0.1.0 publicada carregava a ferramenta e não aplicava gancho nenhum — nenhum dump saía.**

- A troca do `PatchAll()` por **aplicação gancho a gancho** veio acompanhada de um filtro de classe de gancho que exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no método**. Este mod declara os 10 ganchos pela **convenção de nome** do Harmony (método `Postfix` em cada classe de `Patches/`), que o Harmony aceita exatamente como o atributo — o filtro recusava as 10 classes: a ferramenta **carregava, logava "carregado." e não dumpava nada** (o silêncio parecendo sucesso; era o defeito A-1 da REV-2, em 4 mods).
- O filtro agora exige só `[HarmonyPatch]` **no TIPO** — o mesmo conjunto de classes que o `PatchAll()` processava. Medido invocando o filtro real da DLL construída: **10 de 10 classes de patch aceitas e 10 métodos de gancho dentro** (antes: 0 de 10). Em todo o projeto, os 4 mods afetados passaram de 0/14 para **14/14** classes de patch aceitas.
- **Ganchos aplicados um a um** (mesmo endurecimento, mesma release): `CreateClassProcessor(...).Patch()` por classe de gancho, uma linha de log por gancho e resumo com a **contagem real** — um gancho que falhe não derruba os outros nove.
- **Ícone definitivo** (arte do dono em `docs/img/roguelikedebugger-icon-fonte.png`, 1254x1254): redimensionado para os **256x256** que a Thunderstore exige e embutido no pacote. Sai o **placeholder** de 946 bytes com as iniciais que o empacotador gerava (`--gerar-icones`), que era o que estava indo no zip. A arte-fonte continua versionada em `docs/img/` — o repositório guarda as duas.

### Dump: efeitos por TIPO CONCRETO (RV-8b-0g)

- Os arrays `Effects` (de status e de ação) são `IEffectInfo[]`, interface vazia: o cast `e as GeneralEffect` que o dump usava para ler o `Action` devolve `null` em todo elemento de outro tipo, e o dado desaparecia do dump (2 entradas do censo de tooltips ficaram `indeterminado` por isso). Agora:
  - campos novos `nEfeitosTot` / `efTipos` (status e ação): tamanho do array e **tipo concreto + campos de cada elemento**, lidos por reflexão;
  - `nAttrEf` / `attrTipos` (status e skill) e `consEf` (item) para os `AttributeEffects` e a ação de consumível;
  - `nTrig` / `trigEf` no `[Status]`: os gatilhos do status (tipo, efeitos, condição, status) — antes não saíam;
  - linha de resumo por categoria, `[Efeitos] resumo (...): total= | porTipo= | naoGeneralEffect=`.
  - `desc=` continua por último e nenhum valor contém `|` ou aspas: o formato antigo não muda.
- **A versão subiu (0.1.0 → 0.1.1) por causa da correção do aplicador acima:** a 0.1.0 que está no ar carrega o defeito e versão publicada na Thunderstore é imutável. Este dump novo é o mesmo que estava em "Não lançado".

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

