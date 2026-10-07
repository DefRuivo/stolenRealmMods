# Changelog — BetterStats

## 1.0.2

**Documentation release. No code change** — this build behaves exactly like 1.0.1; the DLL differs only in the version string it reports.

- **The package page is now in English.** The description and the README were rewritten in English, in the same shape as the other packages of this project (what it does, what it does not do, install, uninstall, build). A short Portuguese summary stays at the end of the README.
- **The build instructions were wrong about the deploy.** They said that a bare `dotnet build` would also copy the mod into the mod-manager profile. That is no longer true: the deploy is **opt-in** — a bare `dotnet build` installs **nothing**, and only `-p:DeployToBepInEx=true` copies the DLL into `<profile>\BepInEx\plugins\BetterStats\`.
- **Two notes below were stale about their own version.** The 1.0.0 section said the fix had landed "before any download" and that the version had not gone up. Neither was true: **1.0.0 was published carrying the defect**, and the fix shipped as **1.0.1**. The text now says that, in the past tense.

## 1.0.1

**Correção do aplicador de ganchos: a 1.0.0 publicada carregava o mod e não aplicava gancho nenhum.**

- A troca do `PatchAll()` por **aplicação gancho a gancho** veio acompanhada de um filtro de classe de gancho que exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no método**. Este mod declara os ganchos pela **convenção de nome** do Harmony (`InventoryStatPatch.Postfix` e `RoguelikeStatPatch.Postfix`), que o Harmony aceita exatamente como o atributo — o filtro recusava as duas classes de patch: o mod **carregava, logava "carregado." e não aplicava gancho nenhum** (o silêncio parecendo sucesso; era o defeito A-1 da REV-2, em 4 mods).
- O filtro agora exige só `[HarmonyPatch]` **no TIPO** — o mesmo conjunto de classes que o `PatchAll()` processava. Medido invocando o filtro real da DLL construída: **2 de 2 classes de patch aceitas e 2 métodos de gancho dentro** (antes: 0 de 2). Em todo o projeto, os 4 mods afetados passaram de 0/14 para **14/14** classes de patch aceitas.
- **Ganchos aplicados um a um** (mesmo endurecimento, mesma release): `CreateClassProcessor(...).Patch()` por classe de gancho, uma linha de log por gancho e resumo com a **contagem real** — um gancho que falhe não derruba o outro (são 2: ficha de personagem e level up).
- **A versão subiu (1.0.0 → 1.0.1) por causa disso:** versão publicada na Thunderstore é imutável e a 1.0.0 que estava no ar carrega o defeito — sem bump a correção não tinha caminho para o usuário. No **caminho feliz nada muda**: o conjunto de ganchos aplicados é o mesmo.

## 1.0.0

Primeira versão publicada.

- **Mostra os stats no formato `base (combinado)`** na ficha de personagem (painel *Attributes* do inventário) e na tela de level up do roguelike: o valor **puro** (pontos investidos, de `character.SavedMap`) seguido do valor **final** entre parênteses (com powerups, equipamento e skills já aplicados).
- **Corrige o layout da coluna de valores** nessas telas: o texto era alinhado num X fixo e vazava para fora do painel.
- **Sem qualquer alteração de gameplay** — o mod só reescreve o texto exibido.

### Correção do aplicador de ganchos (a nota dizia "mesma versão, sem subir número"; a versão subiu — esta é a correção que saiu na 1.0.1, seção acima)

- A troca do `PatchAll()` por **aplicação gancho a gancho** (que entrou nesta versão) veio acompanhada de um filtro de classe de gancho que exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no método**. Este mod declara os ganchos pela **convenção de nome** do Harmony (`InventoryStatPatch.Postfix` e `RoguelikeStatPatch.Postfix`), que o Harmony aceita exatamente como o atributo — o filtro recusava as duas classes de patch: o mod **carregava, logava "carregado." e não aplicava gancho nenhum** (o silêncio parecendo sucesso; era o defeito A-1 da REV-2, em 4 mods).
- O filtro agora exige só `[HarmonyPatch]` **no TIPO** — o mesmo conjunto de classes que o `PatchAll()` processava. Medido invocando o filtro real da DLL construída: **2 de 2 classes de patch aceitas e 2 métodos de gancho dentro** (antes: 0 de 2). Em todo o projeto, os 4 mods afetados passaram de 0/14 para **14/14** classes de patch aceitas.
- **A versão subiu (1.0.0 → 1.0.1), não ficou na mesma.** Esta subseção nasceu em 254c9a2 com "sem subir número", quando o conserto ainda estava só no fonte; o c3d3aab bumpou porque a 1.0.0 **já estava publicada** (portanto baixável — não "antes de qualquer download") e versão publicada na Thunderstore é imutável: sem bump a correção não tinha caminho para o usuário. É a mesma correção da seção 1.0.1 acima; no caminho feliz nada muda (o conjunto de ganchos aplicados é o mesmo).
