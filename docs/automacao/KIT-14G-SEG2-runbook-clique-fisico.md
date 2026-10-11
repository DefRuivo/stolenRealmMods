# KIT14G-SEG2 — runbook do CLIQUE FISICO (o teste de 2 minutos do dono)

## Por que este teste decide a direcao da correcao
O instrumento (probe) clica o botao `Accept` da criacao de personagem **no primeiro quadro em que ele aparece
ativo** — e `activeInHierarchy` NAO e `interactable`. Em 8 execucoes, clicar por esse caminho derruba o
`Stolen Realm.exe` com `ntdll.dll / 0xc0000005 / offset 0x4a612` (sempre o mesmo).
Se um **clique humano**, na mesma rota e no mesmo ambiente isolado, TAMBEM derrubar o jogo, o defeito e DO JOGO
(e o kit so precisa documentar/desviar). Se NAO derrubar, o defeito e DO INSTRUMENTO (clique cedo demais),
e a correcao e no probe.

## Ambiente (preparado pelo agente, nada no seu save)
- Dados do jogo redirecionados para copia isolada (junction do KIT-16), com snapshot por hash antes/depois.
- Steam Cloud DESLIGADA (verificado em `sharedconfig.vdf`: `cloudenabled=0`).
- Game fechado antes de comecar; nenhum mod de terceiro no caminho.

## O que VOCE faz (na ordem)
1. Eu confirmo que o ambiente esta montado e religo o jogo (nada de clique em Steam).
2. Va de **Play → Roguelike** e chegue na **criacao de personagem** (nao clique em Accept ainda).
3. Avise: "na criacao". Eu marco o tempo e comeco a coleta.
4. **Clique `Accept` com o mouse**, uma vez, como um jogador normal.
5. Diga o que aconteceu:
   - (a) o jogo **fechou/crashou** -> e o jogo (mesma assinatura do probe);
   - (b) o jogo **entrou na run** e chegou ao HUD -> e o instrumento;
   - (c) travou sem fechar, tela preta, ou outro comportamento -> descreva o que viu.
6. Se entrou na run, siga ate onde der (o objetivo final do KIT-14 e a tela do **Skills** do RSTV): abra, veja a
   janela e o tooltip, e me diga se o texto esta legivel / cortado / sobreposto.

## O que eu coleto (sem voce transcrever nada)
- `Player.log` do diretorio isolado (com ou sem o relatorio de desligamento do Unity);
- Event Log (Application Error id 1000) com modulo/excecao/offset;
- hashes do diretorio de dados real (antes/depois) provando que seu save nao foi tocado;
- desligamento do Steam Cloud: confirmo que continua DESLIGADA no fim.

## Se o jogo morrer: eu restauro e te aviso
Encerro a sessao, restauro o junction e os dados, religo a Steam Cloud e te digo o que a evidencia mostrou —
com o proximo passo ja decidido (correcao no probe OU documentacao da limitacao do jogo).
