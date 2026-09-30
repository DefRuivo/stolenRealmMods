# Changelog — RoguelikeSkillTreeVisualizer

## 0.1.0

Primeira versão. O mod **ainda não foi conferido em jogo** — a conferência está no roteiro do `README.md`.

- **Botão `Skills` na tela Select Party** do modo Roguelike: quadrado, na mesma linha e colado à direita do *Choose Powerups*. É um clone do **botão nativo** (mesmo sprite e estados); a largura do *Choose Powerups* encolhe só o necessário, a linha **não cresce** e o *Accept Party* não muda de tamanho.
- **Abre a Skill Tree NATIVA** do jogo (a mesma de *Campaign → Change Skills*) com o contexto **real** do personagem: nível, equipamento, atributos e estado das skills. A janela nativa é reaproveitada — o mod **não reimplementa** a árvore.
- **Modo somente leitura de verdade**: tooltips (com os números do personagem certo), zoom, troca de abas e requisitos continuam funcionando; **nada é aprendido, removido ou gasto**. O clique no nó é bloqueado, o *Respec Build* fica escondido e o rodapé mostra `0 points available`.
- **Alvo do botão**: o **último personagem que VOCÊ adicionou** à party, resolvido **no clique** (nível e equipamento sempre atuais, sem cache). Cada jogador usa os seus; party local vazia = botão desabilitado.
- **Config**: `Geral` → `AtivarBotao` em `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg` (padrão `true`). Só serve para **desligar** o botão — quem não abrir o arquivo não vê diferença.
- **Diagnóstico**: cada gancho Harmony é aplicado e logado **individualmente** (um gancho que falha não derruba os outros — antes o `PatchAll()` era tudo-ou-nada); o resumo do boot traz a **contagem real** (`RSTV: patches Harmony aplicados (7/7 ganchos, 7 metodos do jogo)`); e se o botão não for injetado o log diz **por quê** (botão nativo ausente, sem `RectTransform`, exceção, config desligado) com o estado da tela.

### Notas de implementação

- O jogo **não** tem um modo somente leitura nativo: a garantia vem de **higienizar o ponto de gravação antes que ele execute**, e não de bloqueá-lo. Se essa higienização falhar, o mod **não deixa o original rodar** e fecha a janela por conta própria — zero escrita em qualquer estado.
- Nenhum arquivo do jogo é modificado; desinstalar é apagar a pasta do mod.
- Compatibilidade declarada: Stolen Realm **v1.3.1**.
- Ícone: arte do autor redimensionada para 256×256. O original de 1254×1254 **não está versionado** no repositório (ver a seção *Ícone* do `README.md`).
