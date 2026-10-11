# KIT-03G1 — Prova runtime EM JOGO (rodada autorizada) — parte 03: reconhecimento e plano

Cartão: `t_09e856b1` (KIT-03G1) · Worker: perfil `default` · Run atual iniciado 2026-10-09 17:59 BRT.
Continuação de `KIT-03G1-parte01.md` (desenho/obstáculo) e `-parte02.md` (execução offline/veredito do gate).

## 1. Autorização recebida (muda o estado do gate)

Comentário do dono no cartão (09/10 18:00), verbatim:

> UNBLOCK: AUTORIZADO PELO DONO (09/10 18:00): o jogo esta fechado (nenhum processo Stolen Realm;
> LogOutput parou as 17:55). Execute o ciclo de prova runtime do cartao: instalar o mod no perfil,
> abrir o jogo, verificar pelo LOG, fechar. Respeitar: opt-in -p:DeployToBepInEx=true, sem tocar
> Assembly-CSharp.dll, sem publicar.

Isto destrava exatamente o que a parte 02 §5 registrou como bloqueio (`needs_input`): o modo `run`
do `scratch/kit/runtime-isolado.sh` passa a ser executável.

## 2. Medições desta rodada (antes de qualquer ação — por detecção, não por presunção)

| Item | Medição | Como foi medido |
|---|---|---|
| Processo do jogo | **AUSENTE** | `tasklist | grep -i stolen` → vazio (exit 1) |
| Lock de frente única | **LIVRE** | `bash scratch/kit/front-unica.sh status` → "Lock ativo: NAO", exit 0 |
| `LogOutput.log` do dono | 1.744.007 bytes, mtime **17:55** | `ls -la` do perfil (parou de crescer: sessão encerrada) |
| Saves do dono | 5 arquivos, mtimes **08/10** | `ls -la` de `%LOCALAPPDATA%\Abyssus\Saved\SaveGames` |
| Perfil do dono | existe, `core/` com **18** arquivos | `ls` do perfil r2modman |
| `ReloadProbe.dll` (probe a instalar) | existe | `scratch/kit/build/20261009_152651/ReloadProbe/bin/Debug/netstandard2.1/ReloadProbe.dll` |
| Jogo | `E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm.exe` (set 12) | `ls` |
| Doorstop no jogo | `winhttp.dll` + `doorstop_config.ini` (`enabled = true`) | leitura do `doorstop_config.ini` |
| Steam | `C:\Program Files (x86)\Steam\steam.exe` existe | `ls` |

## 3. Como o isolamento é obtido (mecanismo, conferido no código)

O `run` **não** escreve no perfil do dono. Ele:

1. copia o `core/` do dono para `<KITS_DIR>/runtime-iso/BepInEx/core` (containment conferido ANTES de criar);
2. instala o probe em `<KITS_DIR>/runtime-iso/BepInEx/plugins/KitRuntimeProbe/ReloadProbe.dll`;
3. lança o jogo por `steam -applaunch 1330000 --doorstop-enabled true --doorstop-target-assembly <CÓPIA>\core\BepInEx.Preloader.dll`.

O ponto do mecanismo: o BepInEx deriva sua RAIZ da pasta onde está o `BepInEx.Preloader.dll` que o
doorstop carrega. Como o alvo é a **cópia**, tudo que o BepInEx grava (plugins/, config/,
`LogOutput.log`) cai na cópia — o `doorstop_config.ini` do jogo (raiz) só é lido, nunca escrito.

## 4. Marcador (o que a verificação usa como prova de boot)

`ReloadProbe/Plugin.cs` (fonte no repo, 13 linhas) faz `Logger.LogInfo("ReloadProbe v1 carregado.")`
no `Awake`. O `MARCADOR` default do script é exatamente `ReloadProbe v1 carregado.` — conferido
antes de rodar. Se essa linha não aparecer no `LogOutput` da CÓPIA, o veredito é FALHOU.

## 5. Plano desta rodada (ordem)

1. `runtime-isolado.sh status` (somente leitura) — confirma jogo fechado, lock livre, hashes do dono.
2. `runtime-isolado.sh run` com `WAIT_SECONDS` generoso — abre o jogo, espera o marcador no log
   ISOLADO, verifica hashes do dono antes/depois, fecha SOMENTE o PID que ele abriu
   (`CloseMainWindow`), e faz rollback exato da área isolada.
3. Conferir os `.sav`/plugins/core do dono depois (mtime + hash) — prova de que nada dele mudou.
4. Reexecutar `bash scratch/kit/run-isolation-tests.sh` e o harness offline, para verificar a
   hipótese registrada na parte 02 §2 (Teste 6 vermelho só por causa da sessão viva do dono).

Limites declarados de antemão: a prova vai **até o boot/menu** (nenhum save é carregado); o
`-p:DeployToBepInEx=true` (opt-in de deploy) **não é usado** aqui porque o isolamento é justamente
*instalar na cópia, não no perfil* — o opt-in de deploy será registrado como não-aplicado nesta
rodada. `Assembly-CSharp.dll` não é tocado em nenhum passo. Nada é publicado.
