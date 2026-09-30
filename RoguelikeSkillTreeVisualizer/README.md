# RoguelikeSkillTreeVisualizer

**Status: PLANEJADO — ainda não implementado.** Esta pasta por enquanto guarda o **ícone do mod**
(que o Thunderstore exige, 256×256) e esta nota. O código entra aqui quando a tarefa **RSTV-2**
começar — seguindo o padrão dos outros mods do repositório: uma pasta na raiz, com o `.csproj`,
o `Plugin.cs` e o alvo `DeployToBepInEx` (não existe `src/`, decisão registrada na PKG-1).

## O que o mod vai fazer

Adiciona um **visualizador de Skill Trees** na tela **Roguelike → Select Party**: um botão
quadrado **à direita** do `Choose Powerups` que abre a interface de Skill Trees **nativa do jogo**
(a mesma do `Campaign → Change Skills`), em modo **somente leitura**, com o contexto **real** do
personagem — Level, equipamento, atributos e estado das skills atuais.

O mod **não reimplementa** as Skill Trees: ele resolve o personagem certo e entrega a instância
real para o sistema nativo. Não há compra de skill, gasto de ponto nem qualquer escrita.

## Regras que já estão decididas

| regra | o que significa |
|---|---|
| **Personagem** | o **último que o jogador local adicionou** à Current Party — nunca o último global |
| **Multiplayer** | cada jogador usa os **seus próprios** personagens; a ação de outro jogador não muda o meu contexto |
| **Remoção** | se o último for removido, cai para o último local **ainda na party**; party vazia = botão desabilitado |
| **Contexto** | resolvido **no clique**, não quando a tela abre (Level/equipamento sempre atuais, sem cache) |
| **Read-only** | navegar, zoom, tooltips e requisitos continuam funcionando; nada que persista muda |
| **Intocáveis** | `Accept Party`, a Current Party, os Powerups, o GameMode e as regras do Roguelike |
| **UI** | o botão é **clonado de um botão nativo** (mesmo sprite/estados); a largura do `Choose Powerups` encolhe o necessário e a linha **não cresce** |

## Ícone

`icon.png` (256×256) é o ícone do pacote Thunderstore. Gerado a partir de uma arte 1254×1254 e
redimensionado para o tamanho que a plataforma aceita.

## Especificação e aceite

A especificação completa (77 itens: investigação obrigatória, estratégia de injeção, rastreio de
personagem, testes por caso) e os critérios de aceite estão registrados no quadro interno do projeto (não versionado).
