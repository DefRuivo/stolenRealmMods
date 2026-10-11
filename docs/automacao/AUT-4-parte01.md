# AUT-4 — parte 01: abertura da rodada de execução (estado de partida e plano)

> Cartão `t_b8b9822e` (AUT-4) · worker perfil `default` · run 622 · **2026-10-09, ~18:4x BRT**.
> Artefato NOVO e numerado (regra do controlador: nada é sobrescrito). Este documento **não** é
> aceite da rodada: registra o estado de partida e o procedimento que será executado.
> `docs/automacao/AUT-4-preparacao.md`, `AUT-4-runbook-rodada-autorizada.md` e
> `AUT-4-estado.json` **não foram editados** por esta rodada.

## 1. Por que esta rodada existe

A preparação OFFLINE do AUT-4 foi revisada e aprovada por execução própria (AUT-4R3 run 509,
AUT-4R4 run 530): suíte verde, contra-prova verde, hashes × disco casando, perfil do dono intacto.
O que **sempre** ficou de fora — e que as duas revisões escalaram como GATE HUMANO — é a **rodada
em jogo**: leitura viva, PNG pela API do Unity, owners Harmony, ida-e-volta, rollback executado.

O gate **KIT-G1** (`t_49c93c37`, revisão run 620, aprovado com 1 caveat) registra a autorização do
dono para a **rodada mínima em ambiente ISOLADO**:

- **perfil**: área isolada (`scratch/kit/runtime-iso/BepInEx`), **fora** do perfil pessoal do dono;
- **build**: o probe identificado, `AUT4Probe.dll` sha256 `407c5c63…` (identidade = hash declarado);
- **ações**: instalar o probe na área isolada, iniciar/encerrar a instância de **teste**, coletar UI —
  **somente leitura**;
- **janela**: sessão de teste com o jogo do dono FECHADO e **uma única frente**; teto por rodada
  `OrcamentoSegundos` (120 s) + `--timeout` do driver; encerramento imediato ao fim.
- **NÃO autorizado**: carregar save, navegar por UI, publicar, tocar o perfil do dono.

O mecanismo de isolamento em jogo **já foi provado** em `t_09e856b1` (KIT-03G1 parte 04): o jogo
lançado via `steam -applaunch 1330000 --doorstop-enabled true --doorstop-target-assembly
<cópia>/BepInEx/core/BepInEx.Preloader.dll` sobe o BepInEx **a partir da cópia**, carrega só o plugin
da cópia, escreve o `LogOutput` **dentro da cópia**, e o perfil/saves do dono ficam bit-a-bit
idênticos (rodada reproduzida 2×, exit 0).

## 2. Estado de partida (medido, não presumido)

| item | medido em 2026-10-09 ~18:4x BRT | consequência |
|---|---|---|
| processo do jogo | **AUSENTE** (`tasklist | grep -i stolen` → vazio) | não é preciso declarar reinício; frente runtime livre |
| `lib/Assembly-CSharp.dll` | sha256 `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` | **intacta** |
| fonte do probe | `AUT4Probe/AUT4ProbePlugin.cs` `48afd3c4…` | = `probe_fonte_sha256` do estado |
| **DLL do probe** | `AUT4Probe/bin/Release/AUT4Probe.dll` `407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7` | = `probe_dll_sha256` do estado **e** = A2 do KIT-G1 |
| driver | `coletor.py` `adb48dca…` | = `driver_sha256` |
| runner | `roda_testes_runtime.py` `7906c169…` | = `runner_sha256` |
| controle negativo | `controle_negativo.py` `053c0026…` | = `driver_controle_negativo_sha256` |

Os quatro hashes foram reconferidos por `sha256sum` **nesta rodada** (não lidos do JSON).

## 3. Plano da rodada (o que será executado, comandos reais)

1. **Fase A (offline, repetível)** — `python tools/automacao/runtime/roda_testes_runtime.py` (15/15) e
   `--contra-prova` (31 iscas), para provar que o instrumento está verde NO estado atual do disco.
2. **Fase B (pré-voo)** — criar a raiz isolada `scratch/aut4-runtime-iso/` **fora** do perfil do dono;
   copiar `<perfil do dono>/core/` para `<iso>/BepInEx/core/`; conferir que a área isolada **não**
   está dentro do perfil do dono (containment, como no KIT-03G1); confirmar jogo fechado e frente única.
3. **Fase C (rodada)** — `python tools/automacao/runtime/coletor.py --plano <plano-da-rodada>
   --executar --autorizado --jogo-disponivel --confirmar-coleta coleta --perfil <iso>/BepInEx
   --out-dir <iso>/out --dll-probe <AUT4Probe.dll> --timeout 300 --out <resultado.json>
   --encerrar-imagem "Stolen Realm.exe"`.
   O driver: instala o probe na cópia → escreve o `.cfg` derivado (Sessao + HashFonte + Autorizado) →
   lança por doorstop → espera estado (chainloader + JSON do probe) → lê → consolida → **rollback
   exato** no `finally` → encerra **só o PID que nasceu nesta rodada** (gracioso `CloseMainWindow`).
4. **Fase D (pós-rodada)** — julgar a leitura com `--detectar`; conferir `manifest`, `rollback` e
   `restauracao.limpo`; remover a área isolada; conferir que o perfil/saves do dono não mudaram.

**Navegação: DESLIGADA** (`Navegar=false`). `demostrar_tooltip=true` (porta opt-in de ida-e-volta: o
próprio probe chama o handler REAL `Tooltip.ShowTooltip(marcador)` e relê `Tooltip.Title`).

## 4. Limites declarados deste artefato

- `AUSENTE` / `NAO_EXERCITADO` / `INDETERMINADO` **nunca** serão apresentados como OK.
- Se a rodada não fechar leitura válida, o artefato seguinte dirá **INCOMPLETO/AUSENTE** com o motivo
  medido — não haverá dado sintético nem leitura inventada.
- Automação **não** substitui o aceite humano nem a publicação do DoD.
- O probe é instrumento TEMPORÁRIO: sai no rollback e não vira dependência de mod nenhum.
