# KIT-03G1 — Isolar a prova runtime (gate após KIT-03F corrigido) — parte 01

Tarefa: `t_09e856b1` (KIT-03G1) · Data: 2026-10-09 17:35–17:45 BRT · Worker: perfil `default`
Filho de KIT-03F `t_160668bd` (APROVADO pela revisão run 611, lente ARTEFATO).
Rodada **OFFLINE** (nenhum jogo aberto por este worker, nenhum save carregado).

## 1. O que a tarefa pede

> "Quando KIT-03F for aprovado, este cartão será desbloqueado e executará a prova runtime de
> isolamento no jogo (instalar mod, abrir, verificar, fechar)."

Ou seja: provar EM JOGO que a instalação de um mod e a leitura de log acontecem DENTRO de uma
área isolada, sem tocar o perfil/saves do dono — e fechar o que se abriu.

## 2. Obstáculo real encontrado (por que a execução em jogo NÃO aconteceu)

Medido no início desta rodada, por detecção de processo (não por presunção):

    get-process -Name 'Stolen Realm'  ->  PID 7096, Responding=True
    StartTime                          ->  09/10/2026 17:32:15 (3 min antes desta rodada)
    Path                               ->  E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm.exe
    <perfil>\BepInEx\LogOutput.log     ->  escrito às 17:34 (sessão ATIVA do dono)

Consequências, todas regra do projeto:

1. **Frente runtime única** (`KIT-03-entrega.md` §3.3): já existe UMA frente runtime — a do dono.
   Abrir o jogo agora seria a segunda.
2. **Nenhuma ação no perfil/save do dono por inferência** (regra do KIT-03): a rotina herdada
   `scratch/cap1/rotina-cap1.sh` instala o probe **no perfil do dono** e encerra o jogo com
   `taskkill /F /IM "Stolen Realm.exe"` — as duas coisas proibidas aqui.
3. **`taskkill`/`kill` estão bloqueados nesta rodada** (sem usuário vivo para confirmar): fechar a
   sessão do dono não é uma ação disponível, nem autorizada.
4. O gate humano **KIT-G1** (`t_49c93c37`, "Autorizar rodada mínima AUT-4 em ambiente isolado")
   segue `blocked / needs_input` — o run em jogo não está autorizado pelo dono.

Portanto: executar a prova em jogo era **impossível sem violar três regras do projeto**. O que
sobrou fazer — e que É o corpo da tarefa ("**isolar** prova runtime") — foi entregar a prova runtime
ISOLADA e pronta, provada offline, e devolver o gate para decisão humana.

## 3. O que foi entregue (arquivos NOVOS, nada existente foi alterado)

| Arquivo | Papel |
|---|---|
| `scratch/kit/runtime-isolado.sh` | A prova runtime isolada: guarda de frente única, perfil copiado, espera por estado, verificação, rollback exato |
| `scratch/kit/controle-negativo-runtime.sh` | Controle negativo: 6 casos que provam que a prova RECUSA e REPROVA |
| `scratch/kit/logs/controle-negativo-runtime-run1.log` | Saída consolidada do controle negativo (6/6 OK, exit 0) |
| `scratch/kit/runtime-sandbox/logs/*.log` | Saída por caso (A..F) |

Nenhum arquivo da entrega KIT-03F foi tocado: os hashes dela seguem válidos (ver parte 02 §4).

## 4. Desenho do isolamento (o "como" o isolamento é provado)

`runtime-isolado.sh` isola **quatro superfícies**, cada uma com uma prova:

1. **Plugins/config** — copia `<perfil do dono>/core` para `<KITS_DIR>/runtime-iso/BepInEx/core`
   e instala o mod-probe em `<KITS_DIR>/runtime-iso/BepInEx/plugins/KitRuntimeProbe/`. O jogo é
   lançado com `--doorstop-target-assembly` apontando para a **CÓPIA** (não para o perfil do dono).
   Prova: containment — a área isolada tem de estar FORA do perfil; se estiver dentro, o script
   **recusa (exit 1) antes de criar qualquer coisa**.
2. **Log** — o `LogOutput.log` que o script lê é o da cópia. Prova: o caminho do log isolado tem de
   ser DIFERENTE do log do dono, e o marcador do plugin tem de aparecer NELE.
3. **Saves** — **nenhum save é carregado** (a prova vai só até o boot/menu) e a árvore de saves é
   hasheada antes e depois; qualquer drift derruba o veredito. Não existe "isolamento presumido".
4. **PID** — fecha **somente o PID que este script abriu**, com
   `(Get-Process -Id <pid>).CloseMainWindow()`; nunca `taskkill`/`kill` no processo do dono.

Guarda de frente única (a peça que este cartão acrescenta ao que já existia):

    jogo_rodando()  -> 0 se existir processo 'Stolen Realm'
    preparar/run    -> se jogo_rodando => RECUSA (exit 3), sem criar/abrir nada

O caminho REAL (`run`) continua implementado e gated: ele recusa com o jogo aberto (exit 3) e
recusa se o lock de frente única estiver vivo (exit 4).

## 5. Limite honesto desta entrega

- `stub` e o controle negativo: **EXERCITADOS** nesta rodada (execução real, ver parte 02).
- `run` (instalar em jogo de verdade, abrir, verificar, fechar): **NAO_EXERCITADO** — exige o jogo
  fechado e autorização (KIT-G1). Não há nenhuma afirmação de sucesso em jogo neste documento.
