# LEVEL-RT-INGAME — rodada 1 (instrumento, bancada isolada): 1, 2 e 5 PROVADOS; 3 e 4 PENDENTES

Cartão: `t_fc484826`. Data: 15/10/2026, 18:05–18:43 BRT. Modelo: `deepseek-flash`.
Escopo desta rodada: **decisão do método + preparação da bancada + primeira tentativa automatizada**.

## 1. Método de prova escolhido (e por quê)

**Escolhido: variante (a) ampliada — instrumento chama o MÉTODO REAL do jogo.**
O instrumento (`scratch/level-rt/probe/`, `LvlRtProbe`) roda dentro do jogo na bancada isolada e chama
`Root.SendGameCompleteFromServer(0, exp, gold, false, 1f, true, false, 0f)` — **o mesmo método que o jogo
chama quando o jogador vence uma batalha** (`GameLogic.Update` → bloco `gameComplete` → linha 111092 do
corpus). Nada de estado inventado: o que é induzido é *a vitória* (chegar ao estado sem jogar até lá); o
caminho do nível/recompensa é o código do jogo com o patch do mod no meio.

- **Por que não (b) save preparado:** o save do dono **já é** o cenário ideal (run roguelike em andamento
  com `Wyatt`, guid `7de0b71f-…`, `ExperienceLevel 20.0` = exatamente no teto). Não é preciso preparar nada;
  a cópia isolada do KIT-16 leva esse save para a bancada.
- **Por que não (c) probe do kit (AUT4Probe):** o aceite do kit está congelado/rebaixado a último na fila
  (atualização do operador de 15/10). O caminho `Play → Roguelike → <tela>` do AUT4Probe termina em
  *Select Party com party vazia* (run1442/run1471) — não cobre jurisdição de nível.
- **O que a variante (a) NÃO cobre:** ela não prova que um jogador **consegue vencer uma batalha** no nível
  21 (isso é gameplay normal e continua `NAO_EXERCITADO`); prova que o **teto 20 deixa de barrar o avanço
  e a recompensa** — que é exatamente o que o mod promete.
- **O que falta para o método ficar completo:** carregar o RUN SALVO (party roguelike no nível 20). Esta
  rodada não conseguiu; ver §4.

## 2. Bancada (técnica de segurança obrigatória — cumprida)

`scratch/kit/kit16-save-isolado.sh` (dados: snapshot sha256-por-arquivo → cópia descartável → rename do
diretório real → junction) + `scratch/kit/runtime-isolado.sh` (BepInEx: cópia do `core/` + plugins
instalados SÓ na cópia) + `front-unica.sh` (frente única) + export/import do registro (PlayerPrefs).
Instrumentado por `scratch/level-rt/driver.py` (modos `com-mod` / `sem-mod`).

Resultado de integridade da rodada `com-mod` (verificado duas vezes: no `finally` do driver e depois, à mão,
no fechamento `scratch/level-rt/fechar.py` porque o shell do agente morreu no meio):

| Alvo | antes | depois | igual |
|---|---|---|---|
| dados do dono (`LocalLow/…/Stolen Realm`) | 115 arquivos | 115 | **byte a byte** (`new=[] removed=[] changed=[]`) |
| perfil do dono (`r2modmanPlus-local/…/Default/BepInEx`) | 53 | 53 | **byte a byte** |
| outro jogo (`Abyssus/Saved/SaveGames`) | 5 | 5 | **byte a byte** |
| PlayerPrefs (export `.reg`) | — | — | **sha256 igual** |
| Steam Cloud app 1330000 | `cloudenabled=['0']` | `cloudenabled=['0']` | **OFF antes e depois** |
| junction / backup / lock / área isolada | — | — | **restaurados/ausentes** ao fim |

Jogo fechado por `CloseMainWindow` **do PID próprio** (nunca `taskkill`). O jogo do dono estava fechado na
largada (gate da política de 13/10 respeitado).

## 3. O QUE FOI PROVADO (itens 1, 2 e 5 do cartão)

Binários identificados por sha256 (hash do DLL = hash do que foi instalado na cópia):

    mod       RoguelikeUnlimitedLevelProgression.dll  888973e08073a971899db2797ae61d0fb2405f6eb55f23e74d39c36abdbcc06e
    instrumento LvlRtProbe.dll                        (hash em run-com-mod/inputs.json)
    fontes do mod  Plugin.cs a860b9e1… | BattleResultTranspiler.cs f62fd414… | GameplayPatches.cs 493919e2… | Policy.cs 7bf6b964…

**1. O plugin carrega — nome NOVO, no log do jogo na bancada isolada**
(`run-com-mod/preservado/LogOutput.log:19-24`):

    [Info   :   BepInEx] Loading [Roguelike Unlimited Level Progression 0.1.1]
    [Info   :Roguelike Unlimited Level Progression] Roguelike Unlimited Level Progression 0.1.1 (com.gumatos.roguelikeunlimitedlevelprogression) carregado.
    [Info   :Roguelike Unlimited Level Progression] Ledger em …\bepinex-iso\BepInEx\config\com.gumatos.roguelikeunlimitedlevelprogression\receipts

**2. O patch aplica — evidência que o PRÓPRIO mod registra, sem nenhum erro/exceção de Harmony no log:**

    [Info   :Roguelike Unlimited Level Progression] Grupo de gameplay aplicado: 20 alvos; janela estrutural encontrada 1x
    [Info   :Roguelike Unlimited Level Progression] politica efetiva: MaxLevel(config)=0 (sem teto voluntario) RewardQueryLevel=20 Verbose=False
    [Warning:Roguelike Unlimited Level Progression] v0.1 singleplayer: em PlayingMultiplayer a progressao ampliada permanece desligada …

`grep -c "Harmony\|Exception\|Error" LogOutput.log` no trecho do mod: **0** (as únicas linhas `Error` do log
são do próprio BepInEx/Unity, não do mod). A "janela estrutural encontrada 1x" é a exigência do transpiler
crítico (exatamente uma correspondência): o patch do núcleo **entrou**.

De quebra, a rodada também mediu **em jogo** o teto vanilla: `vanilla_max_level=20` (lido de
`GlobalSettingsManager.instance.roguelikeManager.RoguelikeMaxLevel` pelo instrumento).

**5. Integridade:** tabela do §2.

## 4. O QUE **NÃO** FOI PROVADO (itens 3 e 4) — e por quê, com evidência

`Root.SendGameCompleteFromServer` só amplia quem está na party da run (`GameLogic.ControlledCharacters` =
`NetworkingManager.MyPartyCharacters`) **com o run roguelike carregado**. Nas duas rodadas desta sessão a
party ficou **vazia** e o instrumento (por guarda anti-prova-falsa: só invoca se houver personagem de nível
≥ 20) **não invocou nada** — nenhum número foi forjado:

- rodada A (cliques por rótulo): `Play` → `Roguelike` → a tela que abre é de **criação/configuração**
  (`gui=CreatingCharacter`, textos `Characters`, `Path Chosen!`, árvores e powerups), party `[]`;
  `status_final=limite_de_cliques_atingido`, `run_detectado=False`, `invocado=False`.
- rodada B (sem UI): invocação direta de `MainMenu.ChooseRoguelikeMode()` + `MainMenu.StartSinglePlayer(true)`
  (o caminho do botão *Continue*) → `resume_run_salvo = "…invocados sem excecao"`, mas a party continuou
  `[]` (`estado_periodico`: `gui=CreatingCharacter playing_roguelike=True vanilla_max_level=20 party=[]`).
  O par salvo do dono estava na cópia (`QuestSaveRoguelike.json`) — o que não resolveu foi o **carregamento
  do run pela UI/menu**.

Conclusão honesta desta rodada: **offline + carga/patch em jogo provados; teto 20 → 21 e recompensa ainda
`NAO_EXERCITADO` em jogo**, por uma dificuldade de *chegar ao run salvo*, não por defeito encontrado no mod.

## 5. RUNBOOK curto (linguagem de jogador) — o clique humano que falta

Bancada montada pelo agente (nada no seu save/perfil; Steam Cloud desligada; hashes antes/depois). O que
**você** faz, com o mouse, sem mexer em nada mais:

1. Eu monto a bancada e abro o jogo (não clique no Steam).
2. Na tela inicial: **Play → Roguelike** e siga pelo caminho que você usa **normalmente para continuar a run
   em andamento** (a que tem o **Wyatt no nível 20**), até aparecer a run/mapa com o grupo carregado.
3. Avise: *"estou na run"*. Eu já estou logando tudo — o instrumento então chama a vitória de um nó e mostra
   no log o nível **antes** e **depois** (e a tela de recompensa, se abrir).
4. Se aparecer tela de escolha de recompensa (skill/item/atributo), **só me diga o que apareceu** — não
   precisa escolher nada.
5. Repito o MESMO cenário com o mod desativado (caso negativo): o nível tem de ficar em 20 e nenhuma
   recompensa aparecer.
6. No fim eu fecho o jogo, restauro a bancada, confiro os hashes e te digo o resultado.

## 6. Artefatos (nada fora das bancadas)

    scratch/level-rt/driver.py                 bancada (KIT-16 + KIT-03) + A/B, com restauração no finally
    scratch/level-rt/probe/                    instrumento (C#) + csproj — NUNCA instalado no perfil do dono
    scratch/level-rt/run-com-mod/              rodada A: inputs.json, commands.json, private-baseline.json,
                                               preservado/{LogOutput.log,Player.log,lvlrt-evidencias/evidencia.json}
    scratch/level-rt/fechar.py + fechamento.json   fechamento à mão (o shell do agente morreu no meio da rodada B)
    scratch/level-rt/run-sem-mod/              (a criar na rodada do caso negativo)
