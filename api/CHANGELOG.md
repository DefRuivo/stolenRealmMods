# Changelog — RealmApi

> Datas em ISO 8601 (BRT, UTC−03:00). Datas de implementação/auditoria não são datas de publicação.
> Auditoria documental CHG-REV: 2026-10-16. Nenhuma publicação realizada.

## 0.1.0 — versão inicial em preparação (revisado em 2026-10-16)

- Base implementada no commit `097f950` (2026-10-11); manifest e changelog de distribuição preparados localmente, ainda sem commit próprio na captura desta auditoria. Identidade própria e independente: `com.gumatos.realmapi`, namespace `Gumatos.RealmApi`, três assemblies próprios (`RealmApi.dll`, `RealmApi.Core.dll`, `RealmApi.Hooks.dll`).
- `RealmAccess.ReadProperty` oferece leitura explícita por reflexão de propriedade pública, sem cache de objetos Unity. O catálogo resolve assinaturas exatas; a instalação confere owner/postfix, desfaz instalação parcial em falha e remove apenas seu próprio owner. O plugin mantém os hooks durante a destruição do host e descarta a instalação em `Application.quitting`, não em `OnDestroy`.
- AppID 1330000, Steam build 25240684 e Unity 2022.3.62f2 são identidade documentada do alvo inspecionado, não três verificações adicionais do gate de runtime. Não há implementação geral de combate detalhado, inimigos, quests ou persistência só porque esses domínios aparecem no inventário.

- Família UI implementada em `Gumatos.RealmApi.UI`: `UIFactory`, `ActionBarUI`, `SkillTreeUI`, `MenuUI` e `TooltipHelper`. Vínculo explícito por `UiFamily.Bind`, resolução de requisitos por assinatura, guarda de thread e opt-in separado de mutação (`allowMutation: true`).
- Helpers para clonar UI nativa, ligar cliques, copiar layout, alterar texto UGUI/ícone e destruir objetos. `AddButton`/`AddTab` registram pedidos e solicitam reconstrução ao hospedeiro; não criam o elemento visual completo. TextMeshPro e preenchimento completo de tooltip não estão cobertos.
- Quatro hooks observacionais: `game.awake`, `ui.skill-tree.updated`, `ui.localized` e `combat.turn-started`. Barramento de notificações com assinatura descartável e isolamento de falhas de assinantes.
- Hooks desabilitados por padrão (`Safety.EnableHooks=false`). Mesmo com opt-in, a instalação pelo plugin exige versão do jogo `1.3.1` e SHA-256 do `Assembly-CSharp.dll` iguais à identidade declarada; valores ausentes ou divergentes recusam a instalação. Esse gate protege os hooks do plugin, não é uma trava global da família UI.
- Consumidores existentes no código do projeto: RoguelikeSkillTreeVisualizer (RSTV, `UIFactory.Clone` e `UIFactory.BindClick`), RoguelikeDebugger (sonda opcional da identidade por reflexão, mantendo modo local sem a API) e ponte observacional RealmApi → KitSdk (adaptador separado, ligado explicitamente pelo host). Esses consumidores não são incluídos neste pacote.
- Validação offline registrada em `api/docs/smoke-result.json` (2026-10-11): suíte de fumaça com 62 testes e zero falhas; assinaturas públicas UI conferidas por metadados. Esse é um resultado anterior, não uma execução nova da auditoria CHG-REV. Isso não substitui validação no processo do jogo: runtime BepInEx/Unity, gameplay, saves, multiplayer e composição visual permanecem não exercitados nesta preparação.
- Metadados e página do pacote preparados como Mod, categoria `mods` da comunidade `stolen-realm`. Ícone oficial de 256×256 fornecido pelo autor (`api/icon.png`, 107.728 bytes, SHA-256 `2b6673512d4250db…`), substituindo o placeholder anterior.

Esta entrada descreve a implementação atual, não uma publicação realizada. O empacotador do projeto já monta o pacote com `RealmApi.dll`, `RealmApi.Core.dll` e `RealmApi.Hooks.dll` juntos em `plugins/RealmApi/`, gerando `dist/gumatos-RealmApi-0.1.0.zip`. Nenhuma instalação ou publicação é autorizada por este changelog.
