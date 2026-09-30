# RoguelikeSkillTreeVisualizer

**Status: IMPLEMENTADO (RSTV-2 + fase de diagnóstico).** O botão e a árvore somente leitura estão
prontos e o mod **ainda não foi conferido em jogo** pelo autor; esta pasta guarda o **ícone do mod**
(que o Thunderstore exige, 256×256), esta nota e o código:

| arquivo | papel |
|---|---|
| `Plugin.cs` | `[BepInPlugin]`, config (`AtivarBotao`) e aplicação dos ganchos **um a um**, com contagem real no log (o `Awake` NÃO cria GameObject: isso roda no chainloader) |
| `Patches.cs` | os 7 ganchos Harmony, cada um com a linha do decompilado no comentário |
| `SelectPartyButton.cs` | RSTV-2a: clona o `roguelikePowerupButton`, encolhe a linha, trata o clique e **diagnostica por que** o botão não entrou |
| `PartyTargets.cs` | RSTV-2b: ordem de adição local (o jogo não guarda essa ordem) |
| `SkillTreeReadOnly.cs` | RSTV-2c/2d: abre a Skill Tree nativa e mantém a sessão somente leitura |
| `RstvHost.cs` | `MonoBehaviour` criado de forma preguiçosa (Update do mod) |

Seguindo o padrão dos outros mods do repositório: uma pasta na raiz, com o `.csproj`,
o `Plugin.cs` e o alvo `DeployToBepInEx` (não existe `src/`, decisão registrada na PKG-1).

**Alvo de compatibilidade:** Stolen Realm **v1.3.1** (versão mais recente do jogo em 30/09/2026) — o pacote Thunderstore declarará esta versão quando o mod for lançado.

## Para quem vai usar

**O que o botão faz**

- Aparece como um botão quadrado **`Skills`**, colado à direita do **`Choose Powerups`**, na mesma
  linha (o `Choose Powerups` encolhe o necessário e a linha não cresce; o `Accept Party` não muda).
- Abre a árvore de skills **do personagem certo**: o **último que VOCÊ adicionou** à party,
  resolvido **no clique** (o nível e o equipamento mostrados são os de agora, sem cache).
- Dentro da árvore dá para **navegar, dar zoom, trocar de aba e ler os tooltips** com os números do
  seu personagem. As skills já aprendidas aparecem acesas; o resto cinza/`CannotObtain`.
- O botão fica **desabilitado quando a sua party está vazia** e só aparece em modo Roguelike
  (segue o `Choose Powerups`).

**O que o botão NÃO faz**

- **Não gasta ponto de skill** — o rodapé mostra `0 points available`.
- **Não aprende nem remove skill** — clicar num nó é bloqueado (`read-only`) e o `Respec Build` fica
  escondido.
- **Não altera** o `Accept Party`, a Current Party, os Powerups, o GameMode nem as regras do
  Roguelike. Nenhum arquivo do jogo é modificado.
- **Não mistura jogadores** — cada jogador usa os **seus próprios** personagens; o que o outro
  adiciona à party não muda o que você vê.

O mod **não reimplementa** as Skill Trees: ele resolve o personagem certo e entrega a instância
real para o sistema nativo. Não há compra de skill, gasto de ponto nem qualquer escrita.

### Config (opcional)

`BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`:

| seção | chave | padrão | o que faz |
|---|---|---|---|
| `Geral` | `AtivarBotao` | `true` | `false` = o mod carrega, registra os ganchos, mas **não cria botão nenhum** na tela |

O padrão é o comportamento de sempre: quem não abrir o arquivo de config não vê diferença nenhuma.

### Desinstalar

1. Feche o jogo.
2. Apague a pasta do mod em `BepInEx/plugins/RoguelikeSkillTreeVisualizer/` (no perfil do r2modman
   ou na instalação manual). Nada é criado fora dela.
3. Opcional: apague `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`.

Desinstalar não deixa resíduo no jogo e não afeta save.

## Diagnóstico — como saber o que aconteceu

O mod **não falha em silêncio**: cada gancho é aplicado e logado individualmente e cada caminho de
falha escreve o motivo. No `LogOutput.log`:

| linha | significa |
|---|---|
| `Roguelike Skill Tree Visualizer 0.1.0 carregado ...` | o plugin carregou |
| `RSTV: gancho aplicado — <Classe> (N metodo(s) do jogo).` | um gancho entrou (uma linha por gancho) |
| `RSTV: patches Harmony aplicados (7/7 ganchos, 7 metodos do jogo).` | **contagem real** de ganchos aplicados; se vier `6/7`, o mesmo erro termina com `GANCHOS QUE FALHARAM:` e os nomes |
| `RSTV: FALHA ao aplicar o gancho <Classe> — <motivo>` | aquele gancho não entrou (assinatura que mudou de versão, por exemplo) |
| `RSTV DIAG: botao 'Skills' HABILITADO/DESABILITADO nesta sessao` | o config foi lido |
| `RSTV-2: botao 'Skills' injetado (NxN px) ... largura da linha A -> B px` | o botão foi criado; as duas larguras devem ser iguais |
| `RSTV DIAG: botao 'Skills' NAO injetado — <motivo>` | **por que** o botão não apareceu (botão nativo ausente, sem `RectTransform`, exceção, config desligado) |
| `RSTV DIAG: a tela Select Party esta aberta e o botao 'Skills' NAO foi injetado. motivo=...` | resumo com o estado da tela quando a injeção falha |
| `RSTV-2: clique no botao 'Skills' -> '<nome>' (nivel N).` | o clique resolveu o personagem |
| `RSTV-2: skill tree read-only aberta para '<nome>' (nivel N, M skills, 0 pontos)` | a árvore abriu |
| `RSTV-2: clique na arvore BLOQUEADO (read-only)` | o clique no nó foi barrado |
| `RSTV-2: modo somente leitura encerrado (nada foi gravado no personagem)` | fechou limpo |

## O que o mod faz (técnico)

Adiciona um **visualizador de Skill Trees** na tela **Roguelike → Select Party**: um botão
quadrado **à direita** do `Choose Powerups` que abre a interface de Skill Trees **nativa do jogo**
(a mesma do `Campaign → Change Skills`), em modo **somente leitura**, com o contexto **real** do
personagem — Level, equipamento, atributos e estado das skills atuais.

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
| **Falha** | nenhum caminho pode falhar calado: ou o log diz **por que** o botão/gancho não entrou, ou o estado duvidoso é fechado |

## Ícone

`icon.png` (256×256) é o ícone de pacote do Thunderstore — **arte de verdade do autor**
(redimensionada de uma arte 1254×1254), não um ícone genérico gerado pelo script do empacotador.
É PNG válido (RGBA) e passa na checagem de 256×256 do `tools/pack-thunderstore.py`.

**Pendente:** o arquivo **original de 1254×1254 não está versionado** neste repositório (dos outros
mods os originais ficaram em `scratch/icons-orig/`, mas o do RSTV não está lá). Se precisar
reexportar ou cortar outra versão, a arte-fonte tem de ser pedida de novo ao autor — nada de gerar
um PNG falso no lugar.

## Especificação e aceite

A especificação completa (77 itens: investigação obrigatória, estratégia de injeção, rastreio de
personagem, testes por caso) e os critérios de aceite estão registrados no quadro interno do projeto (não versionado).

## Roteiro de conferência em jogo (RSTV-2)

1. Compilar e instalar: `dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj`
   (sem a propriedade `DeployToBepInEx=false` ele copia a DLL para o perfil do r2modman).
2. Abrir o jogo modded e ir em **Roguelike → Select Party**. No `LogOutput.log` devem aparecer
   `RSTV: patches Harmony aplicados (7/7 ganchos, 7 metodos do jogo)` e
   `RSTV-2: botao 'Skills' injetado ... largura da linha N -> N px` (as duas larguras devem bater).
   Se o botão **não** aparecer, o log já diz o motivo (`RSTV DIAG: ...`, com a tela, o botão nativo e
   a party local) — não precisa adivinhar.
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
8. Opcional (config): com `AtivarBotao = false` no `.cfg`, a tela abre normal e **sem** botão nenhum;
   o log diz `RSTV DIAG: botao 'Skills' DESABILITADO nesta sessao`.

## Riscos conhecidos (não verificáveis sem abrir o jogo)

- O sprite/âncora/`LayoutGroup` da linha vivem no prefab (`resources.assets`, 1,7 GB, não aberto):
  o mod mede em runtime, compensa a largura e **loga** o modo de layout usado. Se o log mostrar
  `childForceExpandWidth`, a linha não cresce mas os botões vizinhos se redistribuem.
- Z-order: a Skill Tree é instanciada sob outro ramo do canvas. O mod compara os índices de irmão e,
  se a árvore estiver atrás da tela de party, move o ramo para o fim e restaura ao fechar (logado).
- `GameLogic.CurrentlySelectedCharacter` é ajustado para o personagem alvo (é de onde `SkillTreeManager`
  e o `Tooltip` leem o contexto). Isso também marca aquele personagem como `IsPartyLeader` e libera o
  lock da câmera — o mesmo que o jogo faz ao selecionar um personagem no mundo.
- **Fechamento de emergência:** se a higienização do commit falhar, o mod **não deixa o original
  rodar** e fecha a janela por conta própria (zero escrita) em vez de arriscar a gravação. Só
  acontece num caminho de exceção, mas vale conferir que a tela de party volta ao normal depois
  (o log diz `RSTV: falha ao higienizar AcceptSkillChanges ...`).

