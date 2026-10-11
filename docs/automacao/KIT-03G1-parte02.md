# KIT-03G1 — Isolar a prova runtime — parte 02: execução e veredito do gate

Continuação de `docs/automacao/KIT-03G1-parte01.md`. Data: 2026-10-09.

## 1. Controle negativo — execução real (6/6 OK, exit 0)

Comando:

    bash scratch/kit/controle-negativo-runtime.sh        # exit 0

    Caso A (REALIDADE): guarda com o jogo REALMENTE aberto
      OK: status=RONDANDO (exit 1) e preparar RECUSOU (exit 3)
    Caso B: front livre (override) + perfil/saves FALSOS + stub -> pipeline completo VERDE
      OK: stub exit 0, dono intacto, area isolada removida
    Caso C: stub plantado SEM o marcador -> tem de FALHAR
      OK: exit 1 e 'marcador ausente' no log
    Caso D: area isolada DENTRO do perfil -> containment tem de RECUSAR sem criar nada
      OK: exit 1, 'CONTAINMENT FALHOU' e nenhum diretorio criado no perfil
    Caso E: hash do dono adulterado no 'antes' -> verificar tem de FALHAR
      OK: preparar=0 e verificar exit 1 com 'saves do dono MUDARAM'
    Caso F: copia do perfil REAL do dono (somente leitura) -> preparar OK e rollback deixa o dono intacto
      OK: core/ copiado (18 arquivos = 18 do dono), rollback exit 0, dono intacto

    === RESUMO ===
    Casos OK: 6/6
    VEREDITO: OK — a prova runtime RECUSA com o jogo aberto e REPROVA nos defeitos plantados

O **Caso A é medição da realidade**, não simulação: com o jogo do dono aberto (PID 7096), `preparar`
recusou com exit 3 — nenhuma segunda frente runtime foi aberta.

### 1.1 Trechos literais (evidência)

Guarda (Caso A) — `scratch/kit/logs/A-preparar.log`:

    [17:44:05] GUARDA: 'Stolen Realm' esta RODANDO (PID 7096) — frente runtime unica.
    [17:44:05] GUARDA: nada e preparado/aberto enquanto a sessao do dono estiver viva.

Pipeline verde (Caso B) — `scratch/kit/logs/B-stub.log` (perfil e saves FALSOS, herméticos):

    OK: containment .../isoB/BepInEx FORA de .../dono/BepInEx
    OK: probe INSTALADO (ReloadProbe.dll)
    OK: estado detectado — marcador presente no LogOutput ISOLADO
    OK: log usado != log do dono
    OK: plugins/ do dono INTACTO
    OK: core/ do dono INTACTO
    OK: LogOutput do dono INTACTO
    OK: saves do dono INTACTOS
    OK: perfil e saves do dono intactos apos o rollback

Containment (Caso D) — `scratch/kit/logs/D-containment.log`:

    ERRO: CONTAINMENT FALHOU — .../dono/BepInEx/iso-dentro-do-perfil/BepInEx esta DENTRO de
    .../dono/BepInEx; nada foi criado

### 1.2 Achado colateral que vale registrar (o controle negativo funcionou "de verdade")

Na 1ª montagem do Caso B eu usei o **perfil real do dono** com o override de frente livre. O
verificador REPROVOU o passo, acusando:

    FALHOU: LogOutput do dono MUDOU

Causa: **a sessão do dono estava escrevendo o próprio `LogOutput.log`** durante o teste. O
verificador estava certo — a expectativa de "dono intacto" é inválida com um dono jogando. Isso
(a) motivou o Caso B hermético e o Caso F (cópia real, somente leitura), e (b) é o mesmo fenômeno
que derruba hoje o Teste 6 do runner do KIT-03F (abaixo).

## 2. Regressão NÃO introduzida, mas observada: Teste 6 do KIT-03F está VERMELHO por causa da sessão viva

    bash scratch/kit/run-isolation-tests.sh    -> Total 6 / Passou 5 / Falhou 1  (exit 1)
    Teste 6 (reuso do harness) -> tools/automacao/runtime/roda_testes_runtime.py reprovou (exit 1)

Executando o harness direto (`python tools/automacao/runtime/roda_testes_runtime.py`, exit 1):

    [REPROVOU] testes\t_aut4_controle_isolado.py
      RESULTADO|REPROVOU|aut4-controle-isolado|o perfil REAL do dono (r2modman) tem de ficar
      intacto: esperado [], obtido ['BepInEx\\LogOutput.log: 1276597:1791578596671322400 ->
      1277962:1791578612674061600']

Ou seja: **a única falha é o `LogOutput.log` do dono ter crescido** — a sessão viva do dono está
escrevendo nele. Nenhum arquivo do harness foi tocado nesta rodada (eu não toquei
`tools/automacao/**` nem `scratch/kit/run-isolation-tests.sh`); o vermelho é do ambiente, não da
entrega do KIT-03F. Com o jogo fechado, é de se esperar que volte a verde — **mas isso é hipótese,
não foi medido** (medir exige o jogo fechado, que é justamente o bloqueio).

## 3. Verificação de que ESTA rodada não tocou o dono

Hashes da listagem do perfil do dono e dos saves, medidos ao fim da rodada:

    core/           b159420072809cd904fcedc954ca863437e3ea1adb02af05f0a6b84f3066b535
    plugins/        6eae7a3c1b38dbc9a3574961138d7797cf3df8127229dd4ebff9ab76543ef9df
    LogOutput.log   c9e3ee449f429d99a7a95cd80d3b4f1840ac2d0d28e498d7f0238ae8da1ed9aa   (muda sozinho: sessão viva)
    Saves (árvore)  04ef12fa9df8926faad47d8969386efa3bc450cc3603a3372115cdf2a684a365

Os `*.sav` do dono seguem com mtime de 08/10 (nada de hoje): **a sessão do dono não gravou save e
esta rodada não gravou nada no perfil** — todas as escritas ficaram em `scratch/kit/runtime-sandbox/`
(removido no rollback de cada caso, exceto os logs de evidência, que ficam em `scratch/kit/logs/`).

## 4. Hashes dos artefatos desta entrega (medidos no disco)

    60495a3f14f2252b528bd816286531d0cd73fe942fcda5b3b9c37cc146c4dcc5  scratch/kit/runtime-isolado.sh
    ad45223db3b9d5aa654fb539bb5002829d07fabae7f7ff93fe0e251e461dec6a  scratch/kit/controle-negativo-runtime.sh

Arquivos da entrega KIT-03F **não foram alterados** (nenhum `patch`/`write_file` neles nesta
rodada): os 8 hashes registrados em `docs/automacao/KIT-03F-entrega.md` §4 continuam válidos.

## 5. Veredito do gate

**BLOQUEADO (`needs_input`).** Motivo:

- A prova runtime EM JOGO (instalar mod, abrir, verificar, fechar) **não pôde ser executada**:
  o dono está com o jogo aberto (PID 7096, sessão iniciada 17:32), a regra de **frente runtime
  única** proíbe a segunda frente, `taskkill`/`kill` estão bloqueados nesta rodada e o gate humano
  **KIT-G1** (`t_49c93c37`) segue sem autorização.
- O que a tarefa tinha de decidível sem o dono está entregue e **provado por execução**: a prova
  runtime está ISOLADA (perfil copiado, log próprio, saves hasheados, PID próprio) e a guarda
  RECUSA corretamente com o jogo aberto.

Para destravar, basta uma de duas coisas (decisão do dono):

1. Fechar o jogo e autorizar a rodada (`bash scratch/kit/runtime-isolado.sh run`) — ~1 min de jogo,
   menu apenas, sem carregar save; **ou**
2. Registrar em KIT-G1 a autorização da rodada mínima, para que o `run` seja disparado com o
   ambiente quiescente.

Depois de executado, `run` fecha o jogo sozinho (`CloseMainWindow` só no PID que ele abriu) e
imprime o veredito por marcador + hashes do dono.
