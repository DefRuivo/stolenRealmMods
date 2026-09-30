# RoguelikeSkillTreeVisualizer

**Status: IMPLEMENTADO (RSTV-2, aguardando conferência em jogo).** Esta pasta guarda o **ícone do mod**
(que o Thunderstore exige, 256×256), esta nota e o código:

| arquivo | papel |
|---|---|
| `Plugin.cs` | `[BepInPlugin]` + `PatchAll()` (o `Awake` NÃO cria GameObject: isso roda no chainloader) |
| `Patches.cs` | os 7 ganchos Harmony, cada um com a linha do decompilado no comentário |
| `SelectPartyButton.cs` | RSTV-2a: clona o `roguelikePowerupButton`, encolhe a linha e trata o clique |
| `PartyTargets.cs` | RSTV-2b: ordem de adição local (o jogo não guarda essa ordem) |
| `SkillTreeReadOnly.cs` | RSTV-2c/2d: abre a Skill Tree nativa e mantém a sessão somente leitura |
| `RstvHost.cs` | `MonoBehaviour` criado de forma preguiçosa (Update do mod) |

Seguindo o padrão dos outros mods do repositório: uma pasta na raiz, com o `.csproj`,
o `Plugin.cs` e o alvo `DeployToBepInEx` (não existe `src/`, decisão registrada na PKG-1).

**Alvo de compatibilidade:** Stolen Realm **v1.3.1** (versão mais recente do jogo em 30/09/2026) — o pacote Thunderstore declarará esta versão quando o mod for lançado.

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

## Roteiro de conferência em jogo (RSTV-2)

1. Compilar e instalar: `dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj`
   (sem a propriedade `DeployToBepInEx=false` ele copia a DLL para o perfil do r2modman).
2. Abrir o jogo modded e ir em **Roguelike → Select Party**. Marcadores de vida no `LogOutput.log`:
   `RSTV-2: botao 'Skills' injetado ... largura da linha N -> N px` (as duas larguras devem bater) e
   `RSTV-2: gancho de adicao/remocao da party ATIVO`.
3. Adicionar 2 personagens meus à party (clique nos tiles) → o log diz qual virou o alvo; clicar num
   terceiro e removê-lo → o alvo volta para o último que ficou.
4. Clicar no botão quadrado **Skills** (colado à direita do `Choose Powerups`). Esperado:
   `RSTV-2: skill tree read-only aberta para '<nome>' (nivel N, M skills, 0 pontos)` e a árvore nativa
   por cima da tela de party, com as skills aprendidas acesas e o resto cinza/`CannotObtain`.
5. Na árvore: passar o mouse nos nós (tooltip com os números do personagem real), trocar de aba,
   tentar clicar num nó → `RSTV-2: clique na arvore BLOQUEADO (read-only)`. O botão `Respec Build` não
   aparece; o rodapé mostra `0 points available`.
6. Fechar (X ou Esc) → `RSTV-2: modo somente leitura encerrado (nada foi gravado no personagem)`.
   Conferir que `Accept Party`, a Current Party e os Powerups continuam intactos.
7. Repetir abrindo/fechando 3× e depois aceitar a party — a árvore não pode aparecer presa atrás
   nem empurrar a UI.

## Riscos conhecidos (não verificáveis sem abrir o jogo)

- O sprite/âncora/`LayoutGroup` da linha vivem no prefab (`resources.assets`, 1,7 GB, não aberto):
  o mod mede em runtime, compensa a largura e **loga** o modo de layout usado. Se o log mostrar
  `childForceExpandWidth`, a linha não cresce mas os botões vizinhos se redistribuem.
- Z-order: a Skill Tree é instanciada sob outro ramo do canvas. O mod compara os índices de irmão e,
  se a árvore estiver atrás da tela de party, move o ramo para o fim e restaura ao fechar (logado).
- `GameLogic.CurrentlySelectedCharacter` é ajustado para o personagem alvo (é de onde `SkillTreeManager`
  e o `Tooltip` leem o contexto). Isso também marca aquele personagem como `IsPartyLeader` e libera o
  lock da câmera — o mesmo que o jogo faz ao selecionar um personagem no mundo.

