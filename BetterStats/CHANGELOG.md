# Changelog — BetterStats

## 1.0.0

Primeira versão publicada.

- **Mostra os stats no formato `base (combinado)`** na ficha de personagem (painel *Attributes* do inventário) e na tela de level up do roguelike: o valor **puro** (pontos investidos, de `character.SavedMap`) seguido do valor **final** entre parênteses (com powerups, equipamento e skills já aplicados).
- **Corrige o layout da coluna de valores** nessas telas: o texto era alinhado num X fixo e vazava para fora do painel.
- **Sem qualquer alteração de gameplay** — o mod só reescreve o texto exibido.

### Correção do aplicador de ganchos (mesma versão, sem subir número)

- A troca do `PatchAll()` por **aplicação gancho a gancho** (que entrou nesta versão) veio acompanhada de um filtro de classe de gancho que exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no método**. Este mod declara os ganchos pela **convenção de nome** do Harmony (`InventoryStatPatch.Postfix` e `RoguelikeStatPatch.Postfix`), que o Harmony aceita exatamente como o atributo — o filtro recusava as duas classes de patch: o mod **carregava, logava "carregado." e não aplicava gancho nenhum** (o silêncio parecendo sucesso; era o defeito A-1 da REV-2, em 4 mods).
- O filtro agora exige só `[HarmonyPatch]` **no TIPO** — o mesmo conjunto de classes que o `PatchAll()` processava. Medido invocando o filtro real da DLL construída: **2 de 2 classes de patch aceitas e 2 métodos de gancho dentro** (antes: 0 de 2). Em todo o projeto, os 4 mods afetados passaram de 0/14 para **14/14** classes de patch aceitas.
- A versão **não** subiu: o defeito foi corrigido antes de qualquer download e a correção não muda nada no caminho feliz.
