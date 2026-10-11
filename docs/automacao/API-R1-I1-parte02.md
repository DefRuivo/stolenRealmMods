# API-R1-I1 — parte 02: runbook do smoke em jogo (`docs/automacao/API-R1-runbook-runtime.md`)

Tarefa `t_f32becd0`. Parte anterior: `API-R1-I1-parte01.md`. Próxima: `API-R1-I1-parte03.md`.

## 1. O que foi entregue

Arquivo **novo**: `docs/automacao/API-R1-runbook-runtime.md` (315 linhas), status declarado em destaque:
**`PREPARADO_NAO_EXERCITADO`**. Ele é escrito para quem vai **operar** a rodada (o dono), não para quem
escreveu o código: cada passo é um comando, e cada comando é o que foi medido nesta máquina.

Estrutura e o que responde:

| § | Conteúdo | Responde a |
|---|---|---|
| §0 | o que a rodada **prova** e o que **não** prova | impede que "os 4 ids no log" seja lido como "os hooks disparam" |
| §1 | 8 pré-requisitos, cada um com comando (jogo fechado, autorização, SDK `6.0.428`, BepInEx `5.4.23.5`, DLLs construídas, hash do alvo, linha de base do perfil, nada de backup de DLL em `plugins/`) | "posso começar?" |
| §2 | tabela de identidade: 3 DLLs (bytes + sha256) e o `Assembly-CSharp.dll` do jogo (`8bb4a7c5…855a`), com o comando `sha256sum` | trava de identidade antes de instalar |
| §3 | instalação opt-in: **ensaio em arena isolada** (`-p:PluginsDir`, não toca o perfil) e instalação real (`-p:DeployToBepInEx=true`), com a prova de que o build padrão não instala | "como instalo sem risco" |
| §4 | habilitar `Safety.EnableHooks=true`: boot 1 cria a config, editar o valor, boot 2 aplica (sem hot-reload) | "como ligo os hooks" |
| §5 | critério de **SUCESSO** (S1…S5): linha de carga, contagem de plugins, **linha de identidade com os 4 `HookId`s**, ausência de `LogError`, hash conferido pelo operador | "como sei que deu certo" |
| §6 | critério de **FALHA**: tabela sintoma → linha do código → ação (config em `false`; recusa por divergência; `instalação recusada` com a exceção; menos de 4 ids; erro de outro mod; crash) | "como sei que deu errado e o que fazer" |
| §7 | encerramento (fechar graciosamente, copiar log/evidência para **fora** do perfil) | como não deixar resíduo |
| §8 | **ROLLBACK** em dois níveis (desligar a config; remover a pasta do plugin + a config), com a impressão digital antes/depois como prova de perfil limpo | "como desfaço" |
| §9 | declaração explícita do que fica **NÃO_EXERCITADO** | honestidade do escopo |
| §10 | rastreabilidade (evidências, partes, gate da raiz) | auditoria |

## 2. De onde saiu cada linha de log citada (nada de memória)

O runbook não inventa mensagem: os literais vêm do código, com `arquivo:linha` no próprio runbook:

| linha citada | origem |
|---|---|
| `RealmApi 0.1.0: hooks desabilitados por Safety.EnableHooks=false` | `api/Plugin/RealmApiPlugin.cs:22` |
| `RealmApi: alvo incompatível; nenhum hook instalado. Application.version=… assembly.sha256=…` | `api/Plugin/RealmApiPlugin.cs:30` |
| `RealmApi 0.1.0: target 1.3.1 / build-inspecionado 25240684; hooks=<ids>` | `api/Plugin/RealmApiPlugin.cs:33` |
| `RealmApi: instalação recusada: <exceção>` | `api/Plugin/RealmApiPlugin.cs:35` |
| os 4 `HookId`s (`game.awake`, `ui.skill-tree.updated`, `ui.localized`, `combat.turn-started`) | `api/Core/Contracts.cs:60-65` |
| GUID/versão/`GameVersion`/`SteamBuildId`/`AssemblySha256` | `api/Core/Contracts.cs:15-21` |
| formato das linhas do `LogOutput.log` (`[Info   :   RealmApi] …`) | medido no perfil do dono, `LogOutput.log:41` (`[Info   :Better Stats] …`) |

Conferência de que o formato do log descrito é o real (comando do runbook, na configuração de hoje, sem a
API instalada — a busca devolve vazio justamente porque a API ainda não está no perfil):

```bash
P="/c/Users/Pichau/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx"
grep -n "Loading \[RealmApi 0.1.0\]" "$P/LogOutput.log"          # hoje: nada (plugin nao instalado)
grep -n "plugins to load" "$P/LogOutput.log"                     # hoje: "9 plugins to load"
grep -nE "RealmApi: (alvo incompat|instalação recusada)" "$P/LogOutput.log"   # hoje: nada
```

## 3. Duas correções de rota registradas no runbook (para não serem repetidas)

1. **A linha de sucesso não imprime o sha256.** O código loga versão e build id; o hash só aparece no log
   **quando diverge** (`RealmApiPlugin.cs:30`). O runbook diz isso de forma explícita (§5, "Nota honesta
   sobre o hash") e torna **obrigatório** o S5 (o operador confere o hash por `sha256sum`). Sem essa nota,
   o critério de sucesso do cartão ("linha de identidade com versão/hash") seria cumprido só no papel —
   **conferir no código é o que revelou o furo**.
2. **Trocar `$(USERPROFILE)` não serve para ensaiar o deploy.** Tentado e descartado: `146 Erro(s)`
   CS0518/CS0246 (evidência `09`). O ensaio passou a usar `-p:PluginsDir=<arena isolada>`, que roda o alvo
   de verdade e escreve fora do perfil (evidência `06`).

## 4. Limite do runbook

O runbook é um **procedimento**, não uma execução. Ele não foi rodado: nenhum dos comandos de instalação,
boot, leitura de log ou rollback foi executado nesta tarefa (o jogo não foi aberto). O que está provado
por comando é o que a `API-R1-I1-parte01.md` lista (`01`…`09`) — build sem flag não instala, o alvo
funciona em arena isolada, o smoke offline segue `25 tests; failures: 0`.
