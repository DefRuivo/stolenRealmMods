# Changelog — RoguelikeSkillTreeVisualizer

## 0.1.0

Primeira versão. O mod **ainda não foi conferido em jogo** — a conferência está no roteiro do `README.md`.

- **Botão `Skills` na tela Select Party** do modo Roguelike: quadrado, na mesma linha e colado à direita do *Choose Powerups*. É um clone do **botão nativo** (mesmo sprite e estados); a largura do *Choose Powerups* encolhe só o necessário, a linha **não cresce** e o *Accept Party* não muda de tamanho.
- **Abre a Skill Tree NATIVA** do jogo (a mesma de *Campaign → Change Skills*) com o contexto **real** do personagem: nível, equipamento, atributos e estado das skills. A janela nativa é reaproveitada — o mod **não reimplementa** a árvore.
- **Modo somente leitura de verdade**: tooltips (com os números do personagem certo), zoom, troca de abas e requisitos continuam funcionando; **nada é aprendido, removido ou gasto**. O clique no nó é bloqueado, o *Respec Build* fica escondido e o rodapé mostra `0 points available`.
- **Alvo do botão**: o **último personagem que VOCÊ adicionou** à party, resolvido **no clique** (nível e equipamento sempre atuais, sem cache). Cada jogador usa os seus; party local vazia = botão desabilitado.
- **Config**: `Geral` → `AtivarBotao` em `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg` (padrão `true`). Só serve para **desligar** o botão — quem não abrir o arquivo não vê diferença.
- **Diagnóstico**: cada gancho Harmony é aplicado e logado **individualmente** (um gancho que falha não derruba os outros — antes o `PatchAll()` era tudo-ou-nada); o resumo do boot traz a **contagem real** (`RSTV: patches Harmony aplicados (8/8 ganchos, 8 metodos do jogo)`); e se o botão não for injetado o log diz **por quê** (botão nativo ausente, sem `RectTransform`, exceção, config desligado) com o estado da tela.

### Correções da auditoria estática (contra o decompilado do jogo, sem rodar o jogo)

- **Segundo ponto de gravação fechado:** `SkillTreeManager.ResetSkillPoints()` (l.173274) chama
  `Character.ResetSkills()` — que zera todas as skills do personagem e enfileira o save (l.37474) —
  **sem passar pelo `AcceptSkillChanges`**. É gancho novo (8º) e é bloqueado no modo somente leitura.
- **Árvore órfã:** se a tela Select Party fechar por fora com a árvore aberta (aceitar a party muda o
  `GUIState` e o jogo fecha a tela em l.118416/l.133307/l.215520), nada no jogo fechava o
  `SkillTreeManager` — a árvore ficaria por cima do mapa com o interceptor de Esc instalado. Agora o
  host fecha a árvore quando a tela de party não está mais aberta.
- O que **não** mudou de propósito (precisa de teste em jogo, está em *Riscos conhecidos* do
  `README.md`): `CheckSkillDependancies(Character)` (l.172328, sem chamador no assembly),
  `resetButton`/`closeButton` (ligados só no prefab) e o slot único de `CancelInterceptor`.

### Notas de implementação

- O jogo **não** tem um modo somente leitura nativo: a garantia vem de **higienizar o ponto de gravação antes que ele execute**, e não de bloqueá-lo. Se essa higienização falhar, o mod **não deixa o original rodar** e fecha a janela por conta própria — zero escrita em qualquer estado.
- Nenhum arquivo do jogo é modificado; desinstalar é apagar a pasta do mod.
- Compatibilidade declarada: Stolen Realm **v1.3.1**.
- Ícone: arte do autor redimensionada para 256×256. O original de 1254×1254 **não está versionado** no repositório (ver a seção *Ícone* do `README.md`).
