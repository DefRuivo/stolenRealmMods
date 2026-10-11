# KIT-14G — parte02: instrumento (roteiro, alvo por nome, recoleta, consumidor do recorder)

Cartão `t_0e656658`, implementador `default/run711`, 10/10/2026. Complementa a parte01.
Nada de **produto/mod** editado: as mudanças são no **instrumento** (`AUT4Probe`) e no
harness offline. Nenhum deploy, commit, push ou publicação.

## 1. O que mudou, e por quê (arquivo por arquivo)

| arquivo | mudança | motivo (lacuna do residual) |
|---|---|---|
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | 2 chaves novas de `.cfg`: `NavegarRota`, `NavegarAlvoNome`; roteiro em estágios em `TentarNavegar`; rótulo do candidato cai para o **nome do GameObject** quando não há texto; `botoes_vistos` gravado no JSON; `Recoletar()` chamado por `PassoNavegacao` **antes** do print; `LerRecorder()` + `recorder.json`; `recorder.json` entra no manifesto/rollback | itens 1–3 do escopo |
| `tools/automacao/runtime/harness-kit14f/Program.cs` | parte4 (aditiva) + `--parte4` na lista e no agregado | prova OFFLINE das novidades |

Detalhe do que cada peça resolve (o mapa completo está no runbook §3.2, atualizado):

1. **Roteiro em estágios** (`NavegarRota`, `;`-separado): o alvo do RSTV vive no HUD da RUN
   (`InTown/InWorldMap/InCutscene/InBattle`, `Root.PlayingRoguelike`). A busca única por
   `Skills` (KIT-14F) não tinha como chegar lá — ela olhava a tela em que o probe nasceu.
   Com roteiro, cada estágio é clicado **uma vez** e a fase de navegação continua até o alvo
   final (ou o teto esgotar). **Roteiro vazio = comportamento histórico**, então nada do
   KIT-14F mudou de semântica.
2. **Alvo por NOME** (`NavegarAlvoNome`, default `RstvRunSkillTreeButton`): o botão do RSTV
   **não tem rótulo** (`RunButton.cs`: o texto é desligado, o glifo é o rótulo). Sem o
   fallback `rótulo = nome do GameObject`, ele era invisível para a escolha do alvo — e essa
   era a razão real de "Skills ausente" no menu, não um defeito do mod.
3. **`botoes_vistos`** (`{rótulo/nome -> 1ª tentativa em que apareceu ATIVO}`): é o **insumo**
   do roteiro. Uma rodada com `NavegarRota` vazio colhe os rótulos reais das telas; só então
   o roteiro é escrito. Roteiro adivinhado não seria prova.
4. **Recoleta pós-navegação** (`Recoletar()`), chamada em `PassoNavegacao` **antes** do print
   `01-ui`: relê objetos, inventário, textos visíveis, reinicia o snapshot do modal e registra
   o quadro (`_res["recoleta"].frame`). Corrige o descasamento do run710 (objetos do quadro
   do *loading*, PNG de centenas de quadros depois).
5. **Consumidor do recorder** (`LerRecorder()`): lê
   `KIT04Core.CorePlugin.Instancia.ResultadoFinal()` **por reflexão** (o probe não referencia
   `KIT04Core.dll` e continua compilando sem o Core), conta os eventos e grava
   `recorder.json` ao lado do JSON do probe — **no processo, antes do rollback**, que é
   exatamente o que o run710 perdeu. Sem Core carregado sai `status = AUSENTE` + motivo:
   ausência **declarada**, nunca `0` inventado.

Lado seguro: os campos novos têm guardas de `null` porque uma instância montada fora do
`Awake` (o harness offline usa `GetUninitializedObject`) não roda inicializador de campo. A
primeira prova com a build intermediária `d2ce391cbd3b05ac223deac0af434e82d8ce03542fe7d852bd77a3c16b878744`
saiu **VERMELHA** na parte3 (3 FALHA: `invocacoes=0`, resumo `estado=falha` com
`NullReferenceException`) — o vermelho foi corrigido com guardas no produto e re-medido; a
saída vermelha não foi preservada como arquivo (foi observada em console nesta rodada, e o
hash da build que a produziu está declarado acima para auditoria).

## 2. Build (executado)

```
dotnet build tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj -c Release -p:DeployToBepInEx=false
=> 0 Erro(s), 1 Aviso (MSB3277 System.Net.Http, herdado — o mesmo das rodadas anteriores)
```

| artefato | sha256 |
|---|---|
| `AUT4Probe/AUT4ProbePlugin.cs` (fonte) | `c32bbbd41e21d85ef05370fde091aac4e094239a2875b6faccae56d28c01019e` |
| `AUT4Probe/bin/Release/AUT4Probe.dll` (build exercitada) | `687b72f1a630e32b655925408189b9cb73011ee7c33c1b9eb389e3239b89b1a8` |

(DLL anterior em disco: `5781417af99a45fd9066b52e2e52ceeb72047413c237980869c6fb80a8da68e7`.)
`DeployToBepInEx=false` explícito. Perfil do dono conferido **depois** do build: **não há**
`BepInEx/plugins/AUT4Probe` nem `com.gumatos.aut4probe.cfg` no perfil `Default` — o build não
instalou nada.

Docs que declaram identidade foram atualizados para os hashes NOVOS (senão a trava
`t_aut4_estado_docs`/`t_aut4_runbook` reprova, e com razão): `AUT-4-estado.json`,
`AUT-4-preparacao.md` e `AUT-4-runbook-rodada-autorizada.md` (§2 + chaves novas em §3.2).

## 3. Prova executada (offline)

| comando | resultado | log |
|---|---|---|
| `harness-kit14f.exe --probe-bin=<nova build>` (partes 1–4, processo próprio por parte) | **PASSOU** — parte1 10 OK, parte2 5 OK, parte3 21 OK, **parte4 14 OK**; 0 FALHA; agregado `RESULTADO\|PASSOU` | `logs/harness-kit14f-agregado.log` |
| `roda_testes_runtime.py` (suite offline do instrumento) | **VERDE, exit 0**, 16 testes | `logs/suite-runtime-offline.log` |
| `roda_testes_runtime.py --contra-prova` | **VERDE, exit 0**, 33 iscas reprovaram como deviam | `logs/contra-prova.log` |
| `check_segredos` / `check_padroes_segredo` / `check_dupes` / `audita_docs` | exit 0 nos quatro | `logs/check_*.log`, `logs/audita_docs.log` |
| `tools/testes/roda_testes.py` | 92/94; **as 2 reprovações são pré-existentes** (`deploy-optin-repo` e `referencias-lib` apontam fixtures de `scratch/kit/build/**` e `scratch/kit/KIT-14-run699|710/**`, nada desta rodada) | `logs/suite-repo.log` |

O que a parte4 prova (executado, com porta injetável servindo 3 telas diferentes):

- menu (`Play`) → criação (`Roguelike`) → HUD da run (`RstvRunSkillTreeButton`, **sem
  rótulo**): **3 invocações**, o alvo por último, casado pelo NOME;
- o roteiro **não** pegou o botão `Continue` que estava ativo em todos os quadros (escolha
  por estágio, não "o primeiro ativo");
- `_rotaEtapa == 2`, resumo `estado=invocado` citando os estágios gastos, `botoes_vistos` com
  os três rótulos;
- `PassoNavegacao` **chama** `Recoletar` (IL) e o rastro da tentativa fica em `_passos`;
- `LerRecorder` existe, roda e, **sem o Core carregado**, declara `status=AUSENTE` com motivo.

## 4. NÃO_EXERCITADO (declaração explícita)

- **jogo em execução**: navegação real, clique no botão do RSTV, PNG de tela, contagem real
  de eventos do recorder com a trilha passiva ligada, Runner positivo/negativo, RSTV sem kit
  e FPS/frame/I-O comparáveis: **NÃO_EXERCITADO** (bloqueio da parte01 §1 — Steam Cloud ligado
  para o app `1330000`);
- a contagem real do recorder exige o jogo: offline o que se prova é o **consumidor** e a
  **declaração de ausência**;
- **roteiro com os rótulos reais** das telas do Stolen Realm: os rótulos saem de
  `botoes_vistos` de uma rodada de jogo (o menu tem 10 botões) — aqui as telas são servidas
  pela porta injetável, porque roteiro adivinhado não é prova.
