# KIT-14G-SEG2 — parte01: o caminho do clique passa a ser OBSERVÁVEL (marcos próprios + gate de clique físico)

Cartão `t_139f714f` (filho de `t_0e656658`/KIT-14G). Esta parte **não** fecha o aceite: ela entrega o
**instrumento** que faltava para isolar o ponto do `c0000005`, a **leitura da evidência já existente**
e a **receita exata** da rodada de runtime que ainda falta. Nada aqui é apresentado como medido em
jogo — o que não foi exercitado está declarado como tal (§6).

## 1. Por que os marcos vão para ARQUIVO PRÓPRIO (motivo medido, não estético)

O `LogOutput.log` do BepInEx **fica em buffer e se perde** quando o processo morre com `c0000005`:
o `LogOutput-isolado.txt` do boot `A-sem-passivo` (run714) tem **1.732 B** e termina em
`AUT4 PROBE: tick via gancho (quadro 3)` — apesar de a rodada ter vivido ~30 s e navegado até
`Accept`. O JSON do probe dos boots que morreram está **congelado** em
`status=INICIADO`, `fase=navegando`, `botoes_ativos=0` (tentativa 1), porque o `Escrever()` só
acontece em transição de fase. Ou seja: **nenhuma das duas trilhas dizia o que o instrumento fazia
no instante da morte** — e era exatamente isso que o aceite pede ("marcos de progresso no probe").

Entra o `marcos-clique.log` (`_dir/marcos-clique.log`), em `FileStream+StreamWriter` com `Flush`
por linha: a linha já está no cache do SO e **sobrevive à morte do processo**. Formato:

```
HH:mm:ss.fff nav tentativa=42/3600 quadro=1531 t=31.204 cena=Character Creation botoes=31 ativos=9 clicaveis=7 etapa=Accept(2/3) procurando=Accept achou=Accept
HH:mm:ss.fff CLIQUE quando=rota_clique rotulo='Accept' etapa=2/3 tentativa=412 quadro=1596 t=33.91 cena=Character Creation gate=False caminho='GUI Manager/Character Creation(Clone)/UI/Roguelike/.../Accept'
```

A rota em andamento (poucos quadros) é registrada em **todo** quadro; a espera pelo alvo final, a
cada 30 quadros. `marcos_clique_arquivo` e `marcos_clique_nota` entram no JSON, e `clique_eventos`
(rotulo, caminho na hierarquia, quadro, instante, cena, veredito do gate) entra em **todo** JSON
gravado — inclusive no que estiver em disco quando o processo morrer.

## 2. O gate de clique físico (`CliqueFisico`) — e o que `onClick.Invoke()` pula

`Button.OnPointerClick` só chega ao handler depois de `IsActive()`/`IsInteractable()`, e o clique
físico ainda depende do raycast: um `CanvasGroup.blocksRaycasts=false` (o padrão de "tela em
transição") **bloqueia** o clique de verdade. O `botao.onClick.Invoke()` do instrumento
(`AUT4ProbePlugin.cs:1030` no KIT-14G) **não passa por nada disso**. Com `CliqueFisico=true` o
instrumento passa a exigir, para CLICAR:

* `gameObject.activeInHierarchy` e `isActiveAndEnabled`;
* `interactable == true`;
* nenhum `CanvasGroup` com `blocksRaycasts=false` na hierarquia (respeitando `ignoreParentGroups`).

O **motivo do bloqueio** não é engolido: `MotivoDeBloqueio()` devolve o texto
(`interactable=false`, `CanvasGroup.blocksRaycasts=false em '<nome>'`, …) e ele sai no JSON como
`casou_mas_bloqueado` / `casou_mas_bloqueado_motivo` da tentativa — é o que separa *"o roteiro não
achou o botão"* de *"achou e clicou fora de tempo"*. `CliqueFisicoEstavel=N` (default 0) exige o
alvo clicável por N quadros seguidos. **Default de tudo = comportamento histórico** (gate
desligado, sem silêncio): sem as chaves no `.cfg` nada muda.

O **mapa do roteiro continua sendo de TODOS os botões ativos** (`botoes_vistos`) — o gate decide se
pode CLICAR, não o que aparece na tela. A porta offline `PortaDeBotoes` (harness) fica com o gate
**inerte**: a escolha do alvo exercitada fora do jogo é byte a byte a mesma de antes.

## 3. Modo diagnóstico `SilencioAposClique` (o discriminador que a bancada PODIA rodar)

O run714 deixou desenhado o discriminador de **clique físico** (do dono, cartão `t_a1f38855`) para
separar *(i) defeito do instrumento* de *(ii) o jogo quebrando ao iniciar a run*. Existe um segundo
discriminador, **executável pela bancada** (não é clique de sistema): com `SilencioAposClique=true`
o instrumento, **assim que clica o último estágio do roteiro**, para de tocar na engine — sem
varredura de `Button`, sem leitura, sem print; só o marco de vida a cada 30 quadros.

* run **morre** mesmo em silêncio ⇒ a morte é do **início da run** (hipótese (ii) do run714), e o
  que resta é o clique físico do dono;
* run **vive** ⇒ a morte vem do **trabalho do instrumento durante a carga da cena** (a varredura
  `Resources.FindObjectsOfTypeAll<Button>` quadro a quadro na cena que está sendo carregada) — e a
  correção é do instrumento, sem precisar de clique físico nenhum.

Isso ataca o mesmo espaço do discriminador do dono por outro ângulo, **sem clique de sistema** — foi
esta a lacuna declarada em `KIT-14G-parte08.md` §5.

## 4. Leitura da evidência JÁ existente (rota real do jogo, medido no run712)

Do `botoes_vistos` do boot **`roteiro2`** (rota `Play;Roguelike`, viveu 120,2 s) sai o roteiro real:

| tentativa | o que aparece ATIVO (1ª vez) |
|---|---|
| 270 | `Play`, `Options`, `Online`, `Exit Game`, `PLAY NOW!`, `WISHLIST NOW!`, … (menu) |
| 271 | `Roguelike`, `Campaign`, `Back` (após o clique em `Play`) |
| 273 | `Unlock <sprite…>`, `Next`, `Change Skills`, `Minus`, `Plus`, `Button Right`, `Button Left` — tela **Character Creation** (`GUI Manager/Character Creation(Clone)/UI/Roguelike/...`) |
| 358 | `Accept` (e `16`,`10`,`13`,`8`,`12`,`14`,`11`) — **~85 quadros depois** de a tela existir |

Duas consequências medidas por leitura, não supostas:

1. **`Accept` é o botão da criação de personagem** — o clique que inicia a run. Antes do run714
   isso era "o estágio `Accept`"; agora tem tela, hierarquia e quadro.
2. O instrumento clica `Accept` **no primeiro quadro em que ele aparece ATIVO** (tentativa 358) e
   `activeInHierarchy` **não é** `interactable`: nada no caminho atual distingue "botão já clicável
   de verdade" de "botão ativo mas ainda não liberado / com raycast bloqueado pela transição".
   É exatamente o que §2 passa a medir e a respeitar.

O que **continua sem prova** é o elo final: *se* `Accept` estava `interactable=false`/bloqueado
naquele quadro e *se* é isso que leva ao `c0000005` no fim da carga da cena
(`Player.log` de 4.516 B terminando em `Loaded Objects now: 42275`, §1.1 do `KIT-14G-parte06.md`).
Isso exige a rodada de §5 — **não está medido**.

## 5. Rodada de runtime que falta (receita exata, para o próximo worker)

1. **Freeze do instrumento** (não rebuildar depois): fonte `AUT4ProbePlugin.cs` =
   `ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2`, DLL
   `bin/Release/AUT4Probe.dll` = `95069e9cbc5e1e7784f80b34589e54cf19651969cddad86b6a35d9b94c89a865`
   (a DLL **não** é reproduzível byte a byte: qualquer rebuild muda o hash e obriga a repetir o
   passo 4).
2. **Sandbox da bancada**: copiar os 5 fontes + a DLL para
   `scratch/kit/KIT-14G-run712/sandbox/tools/automacao/runtime/AUT4Probe/` e pôr
   `PROBE_SHA = 95069e9c…` em `scratch/kit/KIT-14G-run712/roda.py` (o `roda714.py` valida fonte e
   DLL contra o sandbox antes de cada boot — sem isso ele recusa).
3. **`.cfg` dos boots novos**: acrescentar ao bloco `[Geral]` já anexado por `roda714.build()`
   `CliqueFisico`, `CliqueFisicoEstavel`, `SilencioAposClique` (mesma costura por `replace_once`).
4. **Três boots, rota `Play;Roguelike;Accept`** (todos com probe só, dados isolados como no
   run714):
   * `F-marcadores` — gate OFF, silêncio OFF: reproduz a morte e o **último marco** diz o ponto
     exato do caminho do clique; o `*-eventlog.json` do boot confirma `ntdll`/`c0000005`/`0x4a612`;
   * `F-silencio` — `SilencioAposClique=true`: separa instrumento × início da run (§3);
   * `F-gate` — `CliqueFisico=true` + `CliqueFisicoEstavel=10`: candidato a correção; se a run subir
     e o `botoes_vistos` alcançar o HUD, o defeito era do instrumento e está corrigido.
5. Conferir por arquivo: `probe/marcos-clique.log` (última linha = última operação),
   `probe/aut4probe.json` (`clique_eventos`, `casou_mas_bloqueado*`), `*-eventlog.json` e o
   `Player.log` do diretório isolado (com ou sem o relatório de desligamento do Unity).

## 6. NÃO EXERCITADO (sem número inventado)

* **nenhum boot rodado nesta rodada** — orçamento de execução desta sessão; o ambiente do dono não
  foi tocado (0 processos do jogo, save intacto, nenhum deploy, nenhum commit);
* **o ponto exato do `c0000005`** segue pendente (é o passo 4 acima);
* **clique físico/aceite visual** segue do dono (`t_a1f38855`);
* `run714`/`run712` continuam sendo a única medição de crash (`A`,`B`,`roteiro3/3b/4/5/6`); este
  cartão **não** refaz nem reinterpreta aqueles números.

## 7. O que está VERIFICADO nesta rodada (offline, reproduzível)

| verificação | resultado |
|---|---|
| `python tools/automacao/runtime/roda_testes_runtime.py` | **VERDE — 16 testes**, exit 0 |
| `… --contra-prova` | **VERDE — 33 testes**, exit 0 (as iscas reprovam como devem) |
| `harness-kit14f --parte1` | PASSOU — 10 OK, 0 FALHA |
| `harness-kit14f --parte2` | PASSOU — 5 OK, 0 FALHA |
| `harness-kit14f --parte3` (navegação/roteiro) | PASSOU — 21 OK, 0 FALHA |
| `harness-kit14f --parte4` (roteiro em estágios) | PASSOU — 14 OK, 0 FALHA |
| build `AUT4Probe.csproj -c Release` | 0 erro |
| `AUT-4-estado.json` / runbook / `AUT-4-preparacao.md` | identidade declarada = bytes em disco |

**Achado colateral medido e corrigido (§ dessa rodada):** acrescentar QUALQUER ECall da engine
(`Time.frameCount`, `SceneManager.GetActiveScene()`, `botao.gameObject`) ao corpo da varredura
derrubava a **parte3 do harness** com `SecurityException: ECall methods must be packaged into a
system module` (pilha de **uma** linha, em `ColetarCandidatos`): o JIT **inlina** o corpo do método
chamado. Correção: o estado de engine é capturado em campos por um método marcado
`[MethodImpl(NoInlining)]` (`CapturarEstadoDeEngine`) e os marcos leem **campo**, nunca engine; o
`gameObject` do botão ficou dentro de `Seguro(<lambda>)` (método gerado), como no código original.
A pilha da exceção passou a entrar na evidência (`resumo`/`marco` de `falha`): "falha" sem pilha não
diz ONDE o instrumento estourou.
