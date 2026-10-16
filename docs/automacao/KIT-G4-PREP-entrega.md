# KIT-G4-PREP — entrega: pré-condições verificadas e lacunas

Cartão `t_8d3678c2` (KIT-G4-PREP), perfil default, 15/10/2026. **Nada foi executado no jogo**;
**nenhuma junction foi montada no diretório real do dono**; **nada foi instalado no perfil Default**;
**nada foi publicado**. `.git` não foi tocado.

> **Correção da revisão round 1 (changes requested).** Os três defeitos apontados foram corrigidos:
> (1) o item 13 e a lacuna §4.1 eram **falsos** — o material de decisão existe e foi **lido** neste
> reparo (a busca anterior consultou um diretório inexistente; causa raiz registrada abaixo);
> (2) runbook e entrega foram reconciliados com o material real (escopo da opção B, passo residual
> correto, All Trees pela barra inferior da run, reaproveitamento do relato de 11/10);
> (3) o runbook agora declara explicitamente a **condição fail-closed** que impede convocar o dono.

Objetivo desta entrega: deixar a rodada de aceite do KIT-G4 a **um clique** — runbook pronto
(`docs/automacao/KIT-G4-PREP-runbook-dono.md`) + encanamento validado item por item.

## 1. Pré-condições verificadas

| # | Item | Estado | Prova |
|---|------|--------|-------|
| 1 | Scripts da bancada KIT-16 existem | **PASSOU** | `scratch/kit/kit16-save-isolado.sh` (23134 B), `kit16-junction.ps1` (2379 B), `kit16-controle-negativo.sh` (4283 B), `tree_snapshot.py` (6348 B), `front-unica.sh` (8384 B), `runtime-isolado.sh` (24677 B) |
| 2 | Caminhos que os scripts derivam batem | **PASSOU** | `KITS_DIR=scratch/kit`, `REAL_DIR=<LocalLow>\Burst2Flame Entertainment\Stolen Realm` existe, `ISO_ROOT=scratch/kit/kit16-iso`, `SCRIPT_DIR`-relativo (não depende do cwd) |
| 3 | Diretório real do dono limpo | **PASSOU (17:51) → ocupado por outro cartão (17:52) → PASSOU de novo (17:53)** | 17:51: `kit16-junction.ps1 state` → `real`; `kit16-save-isolado.sh status` → `backup real: NAO`, `JOGO: FECHADO`, `Lock ativo: NAO`. 17:52: o caminho virou **`Junction -> scratch/kit/KIT-14F4-run1525/cases/on4/recorder-on/boot01/dados-iso/dados-do-jogo`**, `backup real: SIM`, `JOGO: RODANDO (PID 5744)` — **boot de outro cartão** (§1.1). 17:53: outro cartão encerrou e restaurou; `state` → `real`, `backup real: NAO`, `JOGO: FECHADO`, lock livre. |
| 4 | **Snapshot por hash funciona** (junction + sha256 + restauração byte a byte) | **PASSOU** | fixture OFFLINE própria em `$HERMES_KANBAN_WORKSPACE/fixture`: `preparar`→junction confirmado, `verificar`→"escrita no caminho REAL apareceu na COPIA ISOLADA", diff `novos[Character99.json, CrossPromo/c.txt] alterados[GlobalSaveData.json]`, `restaurar`→"diretorio REAL restaurado BYTE A BYTE identico", `FIXTURE: OK` (exit 0). Estado final do alvo: `real` (sem junction, sem backup). |
| 5 | Steam Cloud per-app do app `1330000` está desligada | **PASSOU** | `suporte.cloud_state()` (KIT-14-run704) com `STEAM_USER=steam/userdata/37602317` → `app_cloudenabled=['0']`, `configuration_off=true`. Reconferido nesta rodada por leitura direta de `.../userdata/37602317/7/remote/sharedconfig.vdf` → `"1330000" { "cloudenabled" "0" }`. Obs.: a conta `210720017` não tem entrada para o app (não é a conta em uso). |
| 6 | AppID e binário do Steam batem com os defaults dos scripts | **PASSOU** | `E:\SteamLibrary\steamapps\appmanifest_1330000.acf` existe; `C:\Program Files (x86)\Steam\steam.exe` existe; jogo em `E:\SteamLibrary\...\common\Stolen Realm\Stolen Realm.exe` |
| 7 | Lock de frente única disponível | **PASSOU (17:51) → tomado por outro cartão (17:52) → PASSOU de novo (17:53)** | 17:51: "Lock ativo: NAO / Lock disponivel". 17:52: holder `KIT14F4-run1525-on4` (PID 1601; "Processo dono: INATIVO (stale)"). 17:53: livre de novo. Este cartão não adquiriu nem liberou o lock. |
| 8 | Perfil r2modman do dono disponível como **fonte** (para copiar o `core/`) | **PASSOU** | `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx` existe (`core/`, `plugins/`, `config/`, `LogOutput.log`) |
| 9 | BepInEx isolado pronto (KIT-03 reuso) | **FALHOU / A FAZER** | `scratch/kit/runtime-iso` **AUSENTE** (reconferido). `runtime-isolado.sh preparar` precisa rodar (copia `core/` do perfil para `scratch/kit/runtime-iso`, recusa com jogo aberto, com containment). |
| 10 | Mod sob teste instalado no BepInEx isolado | **FALHOU / A FAZER** | `runtime-isolado.sh preparar` instala **um único** DLL (`PROBE_DLL`, default `build/20261009_152651/ReloadProbe/bin/Debug/netstandard2.1/ReloadProbe.dll`). **Não existe passo que instale o RSTV + RealmApi candidatos** no `plugins/` isolado. Sem isso a janela "All Trees" não aparece para o dono inspecionar. |
| 11 | Build candidato identificado | **PARCIAL** | O RSTV instalado no perfil Default é `98f19bd6263b054a36c343f0e90effbc41aca8ce8d2355849dec4597a6c4581d` — **diferente** do candidato 0.3.3 registrado no KIT-14 (`1d0b85e8d0f30d10c4fe7c4e044d30380537e8801a7d39875192459a2e51d5cc`). Ou seja: o que o dono tem instalado **não** é o artefato sob aceite. A rodada precisa apontar explicitamente qual build entra no isolado. |
| 12 | Marcador de boot do BepInEx isolado confiável | **INDETERMINADO** | `ReloadProbe.dll` default tem **4096 bytes** (múltiplo exato de 4 KiB — tamanho suspeito de stub). O marcador `"ReloadProbe v1 carregado."` no `LogOutput` isolado não foi exercitado nesta preparação. |
| 13 | Material de decisão do KIT-G4 (opções A/B/C) existe e foi lido | **PASSOU** | `C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_728bc587/KIT-G4-material-de-decisao.md`, **12867 B**, sha256 `4023691da846a28f87da566c647d1ca94d47a364b1d2548f4e5cb06ef13cf8b7` — anexo **621** do cartão `t_728bc587` (**KIT-G4-MAT**, status `done`, run 1488); acompanhado de `KIT-G4-conferencia-fontes.json` (20122 B, sha256 `cd888e42a6376203b6d139f2befe03068522f9ce37abac05f3c06b6a82c6acf5`, anexo 622). Lido na íntegra (75 linhas) neste reparo. |
| 14 | Resíduo de execução anterior na área isolada | **AVISO** | `scratch/kit/kit16-iso` tem `antes.manifest`/`antes.sha256`/`dados-do-jogo`/`registro-antes.reg`/`registro-depois.reg` de 10/10 (run700); `KIT-16-run700/` tem `cn-a/cn-b/cn-c`, `run-real*`. Não bloqueia (`preparar` faz `rm -rf` do que é dele), mas é estado velho: não confundir com prova desta rodada. |

### 1.1 Ocupação concorrente da bancada (estado no handoff) — HAZARD

Às **17:52** (handoff deste reparo) o **caminho real do dono está junctionado por OUTRO cartão**, não
por este:

- `kit16-junction.ps1 state "<real>"` → `Junction -> C:\dev\stolen-realm\scratch\kit\KIT-14F4-run1525\cases\on4\recorder-on\boot01\dados-iso\dados-do-jogo`
- `kit16-save-isolado.sh status` → `JOGO: RODANDO (PID 5744)`, `backup real: SIM`
- `Get-Process 'Stolen Realm'` → PID **5744**, `StartTime 15/10/2026 17:51:43`, `Path E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm.exe`
- `front-unica.sh status` → holder **`KIT14F4-run1525-on4`** (PID 1601), "Processo dono: INATIVO (stale)"

Leitura: o cartão **KIT-14F4 / run1525** (consumidor do recorder, `t_5f50371d`) estava executando um
boot com a bancada KIT-16 montada sobre o caminho real. **Este cartão não montou, não tocou e não
desmontou** isso (frente única alheia; desmontar seria interferir em execução de terceiro).

**Desfecho (17:53):** o outro cartão encerrou o boot e **devolveu a bancada corretamente** — `state`
→ `real`, `backup real: NAO`, `JOGO: FECHADO`, lock livre. Isso é, de brinde, uma segunda prova em
produção de que o ciclo junction→restauração funciona (a primeira foi a fixture offline, item 4) — e
por um terceiro, não por este cartão.

Consequência para o objetivo do KIT-G4-PREP: **o recurso físico é um só** — o caminho real do dono e o
lock de frente única. A ocupação foi transitória, mas o hazard permanece: enquanto qualquer outro
cartão estiver com eles, a rodada do KIT-G4 **não pode começar**, mesmo com todo o encanamento
validado. Antes de convocar o dono é preciso: (a) o jogo do outro cartão fechar; (b) a junction/backup
serem restaurados pelo dono do lock; (c) `state` voltar a `real` e `front-unica.sh` estar livre.
**`hotspot: scratch/kit/ (bancada KIT-16 + caminho real do dono)`** — dois cartões disputando o mesmo
caminho junctionado é colisão, não paralelismo.

### 1.2 Causa raiz do falso negativo do item 13 (rastreável)

A busca da rodada anterior usou `~/.hermes/kanban/attachments`. **Esse caminho não existe nesta
máquina**: `ls /c/Users/Pichau/.hermes` → `No such file or directory`. A raiz real de anexos é
`C:/Users/Pichau/AppData/Local/hermes/kanban/attachments` (126 pastas de cartão), coerente com
`HERMES_KANBAN_DB=C:\Users\Pichau\AppData\Local\hermes\kanban.db`. O passo 1 do cartão ("Leia … o
material de decisão do KIT-G4") **não havia sido executado de fato**; foi executado agora.

### 1.3 Reconciliação com o material de decisão (o que mudou no runbook)

- **Opção B = qualificação final primeiro.** O material é explícito (§4): integrar/revisar o candidato,
  concluir observação passiva, janela/tooltip, Runner e exportação, atualizar o pacote e obter KIT-14R;
  **só depois**, a participação humana curta. O runbook agora abre com essa ordem.
- **Passo residual correto:** `docs/automacao/KIT-14-runbook-residual-run1471.md` § "Só depois:
  mão/olho do dono" — ação humana mínima = clicar fisicamente **Skills no HUD/modal**, passar o mouse
  numa skill, confirmar legibilidade/recorte/sobreposição/pontos. (A fonte citada antes,
  `KIT-14-runbook-residual-run1524.md`, é o roteiro técnico da instância seguinte; ela também remete o
  veredito ao KIT-G4.)
- **All Trees abre pela barra inferior da run (botão `Skills`) ou modal indicado** — **não** pelo botão
  removido da tela Select Party (Plugin.cs:22..25). O runbook manda o dono não procurar aquele botão.
- **Relato humano de 11/10 registrado para reaproveitamento:** KIT14G-SEG2/run897, entrega 899,
  `RELATORIO.txt` (`C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_139f714f/RELATORIO.txt`)
  — dono relatou HUD alcançado e **Skills legível** (~23:47 BRT), sem screenshot do worker, com probe
  inerte e configuração diferente. O runbook manda avaliar **equivalência ao candidato** antes de
  exigir repetição, em vez de tratar como se o dono nunca tivesse testado.
- **Fusão com o SEG2 mantida de propósito, declarada:** o SEG2 testa `Accept`/crash e **não substitui**
  este aceite; seus "2 minutos" **não são medida do trabalho restante**. A fusão só aproveita a sessão
  já aberta (o clique `Accept` custa zero ao dono) como observação lateral da correção Select
  Party→HUD; o produto da rodada continua sendo janela/tooltip/legibilidade.

## 2. Condição fail-closed (não convocar o dono)

O runbook só é acionável quando **duas** condições de bancada valem ao mesmo tempo:

1. **Mod sob teste instalado.** `scratch/kit/runtime-iso/BepInEx/plugins/` precisa conter o **candidato
   nomeado (RSTV + RealmApi) com hash registrado**. Sem o mod sob teste no isolado, a janela All Trees
   **não existe** e a metade visual do roteiro (passo 4–6) não tem o que inspecionar. Hoje: diretório
   ausente (**FALHOU**, item 9) e nenhum passo instala o mod (**FALHOU**, item 10).
2. **Bancada livre.** O caminho real do dono precisa estar em `real` (sem junction, sem backup) e o
   lock de frente única livre. Às 17:52 estava **ocupada por outro cartão** (`KIT-14F4-run1525`,
   §1.1); às 17:53 foi devolvida limpa. Ou seja: a condição é satisfeita **agora**, mas é volátil —
   verificar imediatamente antes de convocar o dono, nunca com base neste relatório.

Logo **o dono NÃO deve ser convocado** por este cartão agora: falta o artefato sob aceite no isolado
(condição 1, que é a de fundo) e a bancada é disputada com outros cartões (condição 2, a re-verificar
no minuto do convite).

## 3. O que o agente faz ANTES (para o tempo do dono ser só o clique)

1. Jogo fechado: `powershell -NoProfile -Command "(Get-Process -Name 'Stolen Realm' -ErrorAction SilentlyContinue | Measure-Object).Count"` → deve dar `0`. **Se o jogo do dono estiver aberto, parar e pedir decisão pelo board** (frente única). *(Hoje está aberto, por outro cartão — §1.1.)*
2. Bancada devolvida por quem a ocupava: `kit16-junction.ps1 state "<real>"` → `real`, `kit16-save-isolado.sh status` → `backup real: NAO`; só então **`bash scratch/kit/front-unica.sh acquire`**.
3. Cloud: `python -c "...suporte.cloud_state()..."` com `STEAM_USER=.../userdata/37602317` → exigir `configuration_off=true`. **Não religar depois.**
4. BepInEx isolado: `bash scratch/kit/runtime-isolado.sh preparar` (com `PROBE_DLL` do instrumento que será usado) → cria `scratch/kit/runtime-iso/BepInEx` sem tocar no Default.
5. **(em falta — criar)** instalar no `scratch/kit/runtime-iso/BepInEx/plugins/` o **build candidato** (RSTV + RealmApi), com hash registrado. Só depois disso o passo 4 do runbook do dono tem o que inspecionar.
6. Dados isolados: `bash scratch/kit/kit16-save-isolado.sh preparar` → snapshot sha256 do real, cópia descartável, rename do real, junction do caminho exato.
7. `bash scratch/kit/kit16-save-isolado.sh verificar` (junction ativo + escrita transparente) antes de abrir o jogo.
8. Avisar o dono **"ambiente pronto"** e só então lançar pelo Steam de **uma** instância.

## 4. O que o agente faz DEPOIS (o dono já pode sair)

1. Fechar **só o PID próprio** via `CloseMainWindow()` (nunca `taskkill /IM`, nunca `kill`).
2. Copiar o `LogOutput.log` isolado **antes** do rollback (`runtime-isolado.sh rollback` apaga a área) para `EVID_DIR/LogOutput-isolado.txt`.
3. `bash scratch/kit/kit16-save-isolado.sh verificar` (diff do que a rodada escreveu na área isolada).
4. Coletar `Player.log` isolado e Event Log `Application Error` id 1000 (módulo/exceção/offset).
5. `bash scratch/kit/kit16-save-isolado.sh restaurar` → exige "diretorio REAL restaurado BYTE A BYTE identico" e registro PlayerPrefs idêntico (sha256 antes == depois).
6. `bash scratch/kit/runtime-isolado.sh rollback` → remove o isolado e prova que o perfil do dono não mudou por conjunto/tamanho/sha.
7. Reconfirmar Cloud `cloudenabled=0` e ausência de junction/backup/lock/perfil temporário.
8. Fechar os três vereditos no cartão KIT-G4 (`t_b001720d`) com a evidência; publicação continua ato separado.

Comando que abriria a rodada (nenhum deles foi executado nesta preparação):

```
bash scratch/kit/kit16-save-isolado.sh status    # read-only, ok
bash scratch/kit/runtime-isolado.sh preparar     # ainda A FAZER (runtime-iso ausente)
bash scratch/kit/kit16-save-isolado.sh preparar  # MONTARIA a junction — NÃO rodado
bash scratch/kit/kit16-save-isolado.sh verificar
bash scratch/kit/kit16-save-isolado.sh restaurar
```

## 5. Lacunas reais registradas (não improvisadas)

1. **Não há passo automatizado que instale o mod sob teste** no BepInEx isolado. `runtime-isolado.sh`
   coloca apenas um `PROBE_DLL` (linhas 294–303). Sem isso, a parte visual do runbook (janela All
   Trees) não tem conteúdo para o dono olhar. É o item 10 da tabela e a **lacuna mais séria**
   (fail-closed §2).
2. **BepInEx isolado ainda não foi criado** (`runtime-iso` ausente) — é só executar `preparar` com o
   jogo fechado, mas isso não foi feito aqui de propósito (não criar ambiente sem necessidade).
3. **`ReloadProbe.dll` de 4096 bytes** (default do `PROBE_DLL`): tamanho suspeito; o marcador de boot
   do BepInEx isolado não foi exercitado. Confirmar antes de usar como prova de carga do isolado.
4. **Build candidato x build instalado divergem** (item 11). A rodada precisa nomear o artefato.
5. **Conta Steam**: o Cloud per-app só está explicitamente `0` na conta `37602317`. Se a rodada usar
   outra conta, a pré-condição 5 cai e precisa ser refeita.
6. **Qualificação final da versão a distribuir depende de trabalho técnico fora deste cartão**
   (integração/revisão do F2, observação passiva, Runner, exportação, pacote atualizado, KIT-14R) —
   declarado no material §4 como pré-requisito da opção B, **não feito aqui**.
7. **A bancada é recurso único e é disputada por outros cartões** (§1.1). Ocupação observada
   (KIT-14F4-run1525, 17:52) foi devolvida limpa às 17:53, mas enquanto qualquer outro cartão mantiver
   a junction + o jogo + o lock, a rodada do KIT-G4 não começa. Precisa re-verificar `state`/lock no
   instante do convite ao dono — não de mais preparação técnica.

## 6. Disciplina respeitada

- **Nenhuma junction foi montada por este cartão** e nenhum processo do jogo foi aberto/fechado por
  ele. No instante da minha verificação (17:51) o caminho real estava `real`; às 17:52 ele estava
  junctionado **por outro cartão** (`KIT-14F4-run1525`) — **não toquei** (§1.1): desmontar seria
  interferir na execução de terceiro. Às 17:53 o outro cartão devolveu a bancada limpa (`real`).
- Nenhum save/perfil real lido ou escrito pela rodada (só o diretório foi **lido** para snapshot na
  fixture, e a fixture usou diretório próprio).
- Nenhum arquivo do perfil Default alterado; nenhum build, nenhum `dotnet build`, nenhum deploy.
- Nada publicado; `.git` intacto; nenhum `git add`/commit.
- Fixture usada só como prova do mecanismo (offline), nunca como prova de runtime.
- Nenhuma tarefa nova criada por subagente; nenhum `delegate_task`.
- Nenhuma credencial/segredo tocado; nenhuma ação destrutiva (sem `taskkill`, sem `rm -rf` de área
  alheia, sem edição de VDF).
