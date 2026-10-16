# KIT-G4-PREP — RUNBOOK DO DONO (uma página, linguagem de jogador)

> Rodada de aceite do kit (opção B do material de decisão). Você só clica e olha. O agente monta tudo
> antes e coleta tudo depois. **Nada é instalado no seu perfil, nenhum save seu é tocado, nada é
> publicado.** Este runbook **não foi executado** — é o roteiro que fica pronto para virar um clique só.

**Fonte de decisão desta rodada:** `KIT-G4-material-de-decisao.md` (opções A/B/C) —
`C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_728bc587/KIT-G4-material-de-decisao.md`,
12867 B, sha256 `4023691da846a28f87da566c647d1ca94d47a364b1d2548f4e5cb06ef13cf8b7`
(anexo 621 do cartão `t_728bc587` / KIT-G4-MAT, `done`, run 1488). Passo residual do dono:
`docs/automacao/KIT-14-runbook-residual-run1471.md` § "Só depois: mão/olho do dono".

## Quando você é chamado — e quando NÃO é (fail-closed)

O material de decisão é explícito: a opção B é **qualificação final primeiro** (integrar/revisar o
candidato, concluir observação passiva, janela/tooltip, Runner, exportação, atualizar o pacote e obter
KIT-14R) e **só depois** a participação humana curta. Convocar você antes disso queima o seu tempo.

**Você NÃO deve ser convocado enquanto `scratch/kit/runtime-iso/BepInEx/plugins/` não contiver o build
candidato nomeado (RSTV + RealmApi) com hash registrado.** Sem o mod instalado no BepInEx isolado a
janela **All Trees não existe** e o passo 4 não tem o que inspecionar. Hoje esse diretório **não
existe** (`scratch/kit/runtime-iso` ausente) e nenhum passo automatizado instala o mod sob teste —
condição declarada e ainda **não satisfeita**.

## Por que esta rodada existe

O gate RSTV integral continua **FALHOU (exit 1)**: o log diz que montou a árvore, mas a imagem final
mostrava Character/inventário, não os nós; e não houve clique físico (`physical_click=false` — o
parâmetro chamado `CliqueFisico=true` só acrescenta guardas ao handler, não move o mouse). O que falta
é o juízo que agente não pode dar: **você olhar a janela**.

## O que VOCÊ faz, na ordem

1. O agente avisa **"ambiente pronto"** e abre o jogo pelo **seu** Steam. Você não clica em Play no
   Steam.
2. **Play → Roguelike**, escolha o personagem descartável indicado e chegue à **run** (o caminho até o
   HUD já é automático e comprovado — não há clique especial aqui).
3. Avise **"na run"**. O agente marca o tempo e começa a coleta.
4. **Na barra inferior da run, clique no botão `Skills`** (é por ali que a árvore abre; o mesmo modal
   que o agente indicar). **Não procure botão de Skills na tela Select Party — ele foi removido do
   jogo.** Use o **mouse físico**, uma vez.
5. Responda **separadamente**:
   - "a janela **abriu**" / "**não abriu**" / "abriu mas o controle está encoberto/interceptado";
   - "o conteúdo (Fire/nós) **apareceu**" / "apareceu vazio";
   - o texto está "**legível**" / "**cortado**" / "com **sobreposição**".
6. **Passe o mouse sobre uma skill**: "o **tooltip aparece**" / "não aparece" e, se aparecer, se o
   texto está "legível" / "ilegível" / "cortado". Confirme também que **nenhum ponto foi gasto** e que
   nada foi alterado (a árvore é somente leitura nesta prova).
7. Se quiser, na mesma sessão, clique `Accept` uma vez como jogador normal (observação de brinde, sem
   custo) e diga se entrou na run normalmente. **Isto não substitui o aceite** — ver abaixo.
8. Feche o jogo você mesmo quando eu pedir (ou me diga para fechar) — eu nunca mato o processo à força.

## O que você responde no fim (três vereditos separados)

1. A inspeção física funcionou? (sim / não / não sei)
2. A UI/UX está aceitável? (aceitável / tem defeito: qual / não avaliável)
3. Você concede o **aceite final do kit**? (concedo / não concedo — motivo)
   *(Aceitar o kit **não** publica nada: publicação é ato separado, autorizado à parte.)*

## Relato seu de 11/10 — será avaliado antes de repetir

Em **11/10/2026, ~23:47 BRT**, você relatou ter chegado ao HUD e visto **Skills legível**
(KIT14G-SEG2/run897, entrega 899, `RELATORIO.txt`). É prova histórica útil, mas com probe inerte e
configuração **diferente** da campanha de 15/10 — falta provar **equivalência ao candidato**, não
fingir que você nunca testou. Por isso este roteiro é **curto e de uma sessão**: é a reconfirmação do
que você já viu, no build atual, e não uma repetição do zero.

## Fusão com o SEG2 — declarada de propósito

O antigo runbook SEG2 (`KIT-14G-SEG2-runbook-clique-fisico.md`) testava `Accept`/crash; os seus "2
minutos" **não são medida do trabalho restante** e ele **não substitui** este aceite. A fusão aqui é
mantida **de propósito** e por um motivo só: o passo `Accept` (item 7) custa **zero** para você quando
você já está no jogo e serve de observação lateral da correção Select Party→HUD. O **produto** desta
rodada continua sendo o passo 4–6 (janela All Trees / tooltip / legibilidade) — os vereditos do fim
são os do KIT-G4.

## O que o agente faz ANTES (para o seu tempo ser só o clique)

Fechar/confirmar o jogo fechado; travar a frente única; verificar Cloud per-app `1330000` **OFF**;
`runtime-isolado.sh preparar`; **instalar o candidato nomeado (RSTV+RealmApi) no isolado com hash**;
`kit16-save-isolado.sh preparar` (snapshot sha256 + cópia descartável + junction do caminho exato);
`verificar`; só então avisar "ambiente pronto".

## O que o agente faz DEPOIS (você já pode sair)

Fechar **só o PID próprio** (nunca `taskkill /IM`); copiar o `LogOutput.log` isolado antes do rollback;
`verificar` (diff do que a rodada escreveu no isolado); coletar `Player.log` e Event Log
`Application Error` id 1000 (módulo/exceção/offset); `restaurar` exigindo **"diretório REAL restaurado
BYTE A BYTE idêntico"** e registro PlayerPrefs idêntico (sha256 antes == depois); `runtime-isolado.sh
rollback`; reconfirmar Cloud `cloudenabled=0` e ausência de junction/backup/lock. Você não transcreve
nada.

## Se o jogo morrer

O agente encerra a sessão, **remove o junction, faz o rename inverso, compara os hashes**, devolve o
registro PlayerPrefs e te diz o que a evidência mostrou — com o próximo passo já decidido (correção no
probe **ou** documentação da limitação do jogo). Nenhuma conclusão é declarada sem a evidência.
