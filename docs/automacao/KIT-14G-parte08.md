# KIT-14G — parte08: A/B da causa do encerramento — RESULTADO e veredito

Cartão `t_0e656658`, run714. Complementa parte01–07. Bancada desta parte:
`scratch/kit/KIT-14G-run714/roda714.py` + boots `A-sem-passivo`, `B-semeado`, `C-sem-nada`,
`D-probe-play`, `E-sem-navegar`. Estado por máquina: `scratch/kit/KIT-14G-run714/verification.json`.

A revisão run713 exigiu: *"provar a causa real da morte do processo — colher Event Log/WER/crash
dump e rodar 1 A/B que separe (a) dados vazios de (b) isolamento/mods instrumentais. Qual
candidato sobrevive determina se isto é defeito corrigível ou limitação genuína."*

**Veredito: NENHUM dos dois candidatos sobrevive. Os dois estão ELIMINADOS por medição, e o
gatilho foi isolado num terceiro fator: a NAVEGAÇÃO POR CLIQUE do probe.** O defeito é
**corrigível** — não é limitação de ambiente.

## 1. Matriz completa das 10 execuções (todas com dados isolados via junction, Cloud 1330000 OFF)

| boot | módulos instalados | dados do dir isolado | navegação | rota | desfecho |
|---|---|---|---|---|---|
| `mapa` (run712) | probe+Core+Adapter | vazios | sim | `Play` | **viveu 120,7 s** |
| `roteiro1` | probe+Core+Adapter | vazios | sim | `Play` | **viveu 121,4 s** |
| `roteiro2` | probe+Core+Adapter | vazios | sim | `Play;Roguelike` | **viveu 120,2 s** |
| `roteiro3` | probe+Core+Adapter | vazios | sim | `…;Accept` | MORREU (29,4 s) |
| `roteiro3b` | probe+Core+Adapter | vazios | sim | `…;Accept` | MORREU |
| `roteiro4` | probe+Core+Adapter | vazios | sim | `…;Accept` | MORREU (25,9 s) |
| `roteiro5` | probe+Core+Adapter | vazios | sim | `…;Accept` | MORREU (25,8 s) |
| `roteiro6` | probe+Core+Adapter | vazios | sim | `…;Accept;__nunca_casa__` | MORREU (25,7 s) |
| **A** (run714) | **PROBE SÓ** | vazios | sim | `…;Accept` | **MORREU (23,1 s)** |
| **B** (run714) | probe+Core+Adapter | **SEMEADOS (96 itens do dono)** | sim | `…;Accept` | **MORREU (24,8 s)** |
| **C** (run714) | **NENHUM** (0 plugins) | vazios | — | — | **viveu 118,0 s** |
| **D** (run714) | **PROBE SÓ** | vazios | sim | `Play` | **viveu 122,3 s** |
| **E** (run714) | **PROBE SÓ** | vazios | **NÃO** (`Navegar=false`) | `…;Accept` (declarada) | **viveu 121,9 s** |

Todas as mortes têm a MESMA assinatura do Event Log: `Stolen Realm.exe` / módulo `ntdll.dll` /
exceção `0xc0000005` / deslocamento `0x4a612` (ver parte06 §1). Todas as vidas longas terminam com
o relatório de desligamento do Unity no `Player.log`; todas as mortes terminam sem ele, no meio da
carga da cena (`Loaded Objects now: 42275/42277`).

## 2. Candidato (a) "dados isolados vazios" — ELIMINADO

Boot **B**: mesma bancada do `roteiro5`, mesmo roteiro, com o diretório isolado **semeado por
cópia somente-leitura do snapshot do dono** (96 itens: `Character0..16.json`, `GlobalSaveData.json`,
`ItemStash.json`, … obtidos de `dados-iso/copia-nao-usada-privada`, que o KIT-16 produz copiando o
diretório real — o diretório real do dono fica RENOMEADO ao lado durante a rodada e nenhum byte
dele é escrito). Resultado: **morreu igual**, `c0000005`/`ntdll`/`0x4a612`, 31,1 s.

⇒ "premissa 'dados vazios' incompatível com início de run" (o palpite do run712) está **morto por
medição**: com os dados reais do dono dentro, o jogo morre do mesmo jeito, no mesmo ponto.

## 3. Candidato (b) "isolamento / mods instrumentais" — ELIMINADO, com o culpado separado

Dois boots separam a coisa em três pedaços:

- **C — bancada isolada com ZERO plugins** (`LogOutput` do BepInEx: "*0 plugins to load*"): o jogo
  **viveu 118,0 s**, `Player.log` de 16.300 B com desligamento limpo, **nenhuma** entrada nova no
  Event Log. ⇒ **o mecanismo de isolamento (junction + BepInEx isolado + profile trocado + launch
  via Steam com doorstop) NÃO é a causa.** O candidato "isolamento" cai.
- **A — probe SÓ, sem KIT04 Core e sem Adapter** (`mods_carregados.total = 1`): **morreu** com a
  assinatura idêntica. ⇒ **o KIT04 Core/Adapter NÃO é a causa.** O candidato "mods instrumentais"
  cai (o que o run712 não tinha testado: ele só excluiu o *clique* do probe, mantendo a *presença*
  do Core/Adapter — exatamente a lacuna que a revisão apontou).

## 4. O gatilho medido: a NAVEGAÇÃO POR CLIQUE

- **D — probe SÓ, rota `Play`** (navegação ligada): viveu 122,3 s. ⇒ o probe pode clicar e o jogo
  sobrevive;
- **E — probe SÓ, rota `Play;Roguelike;Accept` declarada mas `Navegar=false`** (o probe observa,
  imprime os dois PNGs e termina: `status=CONCLUIDO`, `duracao_s=9,9`, `eventos_frame.fim=358`):
  **viveu 121,9 s**; nenhuma entrada nova no Event Log. ⇒ **a mera presença do probe, com o mesmo
  roteiro declarado, não derruba nada**;
- qualquer boot em que a navegação **clicou** o roteiro até o estágio `Accept` morreu.

Cruzando: **o que derruba o jogo é o CLIQUE sintético que inicia a run** — não o roteiro declarado,
não o probe observando, não os dados, não os mods, não o isolamento. O `onClick.Invoke()` do botão
`Accept` (o único caminho de clique do instrumento, `AUT4ProbePlugin.cs:1030`) leva o jogo a
`c0000005` em `ntdll`.

**Correção de rota (importante):** a leitura do run712 — "o jogo crasha por causa da premissa de
dados vazios ao entrar na run" — está **errada**. E a leitura de parte05 §3 ("3/3b/4 = guarda
abortou" vs "5/6 = crash medido") também: ver parte06 §1.2/§3.

## 5. Porta que ficou aberta (o que ainda NÃO sei)

Não isolei **onde** no caminho do clique o `c0000005` nasce: pode ser
(i) o `onClick.Invoke()` chamado fora do contexto de input da engine (`Input`/EventSystem) — a run
sobe por um caminho que a engine não esperava;
(ii) o jogo realmente quebrando ao iniciar uma run nesta configuração (dados reais, já sem Cloud);
(iii) interação probe×jogo no mesmo quadro do clique.
O discriminador já está desenhado e é exatamente o que falta: **um boot com clique FÍSICO**
(`Input`) no lugar do `onClick.Invoke()`. Isso não é possível pela bancada (clique de sistema é
proibido sem supervisão) — e é, por desenho, a **etapa visual do dono** do KIT-14. Ou seja: a
rodada do dono (cliques físicos) passa a ter valor diagnóstico direto:
**se com clique físico a run sobe, o defeito é do instrumento (corrigível e nosso); se com clique
físico também morre, o defeito é do jogo/ambiente e a premissa de automação por handler cai.**

Classificação do item 1 do escopo: **defeito CORRÍGIVEL, localizado no caminho de clique do
instrumento**, com a fronteira exata declarada acima — não é limitação genérica de ambiente.

## 6. NÃO EXERCITADO (sem número inventado)

- HUD da run / botão do RSTV instalado: continua NAO_EXERCITADO (o clique que iniciaria a run mata
  o processo);
- `eventos_total > 0` do recorder: NAO_EXERCITADO (depende do HUD; ver parte07);
- clique físico / aceite UI-UX: do dono;
- Runner positivo/negativo; RSTV sem kit; FPS/frame/IO (limiares dispensados pelo dono);
- o ponto exato do `c0000005` dentro do caminho de clique (§5).

## 7. Ambiente ao fim (medido agora)

dados do dono **111/111 byte a byte**, `production_diff().equal = True`, **sem junction**,
**0 processos** `Stolen Realm`, perfil r2modman **sem** `plugins/AUT4Probe` e **sem**
`plugins/KitPassive`, Cloud do app `1330000` **OFF**. Nenhum commit, nenhum deploy, nenhuma
publicação. As cinco bancadas novas (`A`–`E`) rodaram com a limpeza blindada do
`roda714.py` — os sete passos de restauração (`dados-verificar`, `dados-restaurar`,
`bepinex-rollback`, `front-release`) saíram **exit 0** em todas, inclusive nas que morreram (o que
no run712 não acontecia: lá o `PowerShell rc=1` abortava a limpeza e deixava o `bepinex-iso` para trás).
