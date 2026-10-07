# AUT-4 — preparação e teste OFFLINE do coletor runtime (t_b8b9822e)

> **Rodada de PREPARAÇÃO.** Nenhum jogo foi aberto/encerrado, nenhum save tocado, nenhum probe
> instalado no perfil, nenhum build deployado. O runtime está **NÃO EXERCITADO** — e assim está
> declarado em todo artefato. Este documento é preparação; a coleta em jogo é a próxima rodada
> autorizada.
>
> **COR-AUT4 (t_b62359c3):** esta versão incorpora a correção dos 6 achados (+A7 de documentação)
> da revisão independente **AUT-4R2** (`docs/automacao/AUT-4R2-revisao.md`). Sem ela a frente AUT-4
> ficava travada. Cada achado entrou com teste **vermelho→verde** e com uma isca de contra-prova.

## O que foi construído (só em `tools/automacao/runtime/**` + este doc)

| arquivo | papel |
|---|---|
| `tools/automacao/runtime/AUT4Probe/` | **probe C#** (instrumento opt-in, somente leitura): lê o objeto vivo |
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | motor/driver + leitura (texto bruto+renderizado, ativo, fonte/material/shader/keywords, cores, geometria, contexto, owners Harmony), gate de autorização, espera de estado, orçamento, manifest+rollback, PNG por `ScreenCapture`, **sessão do driver (A1)** e **porta opt-in de ida-e-volta (A6)** |
| `tools/automacao/runtime/AUT4Probe/Json.cs` | serializador JSON mínimo (sem dependência externa) |
| `tools/automacao/runtime/coletor.py` | **driver/orquestador** (contrato + decisão de autorização + normalização de observação + **provas de execução** + manifest/rollback + **detector de ausência/indeterminado** e **identidade do resultado**), CLI opt-in |
| `tools/automacao/runtime/controle_negativo.py` | **controle negativo ISOLADO** (`exigir_perfil_isolado` fail-closed, lançamento por stub, perfil do dono medido antes/depois) |
| `tools/automacao/runtime/roda_testes_runtime.py` | runner offline (exit 0/1/2, `--contra-prova`) |
| `tools/automacao/runtime/testes/` | 15 testes offline + 31 iscas de contra-prova |
| `tools/automacao/runtime/fixtures/` | fixtures **rotuladas** (nunca evidência de runtime) |
| `docs/automacao/AUT-4-estado.json` | estado legível por máquina (listas e hashes conferidos contra o disco) |
| `docs/automacao/AUT-4-runbook-rodada-autorizada.md` | **runbook** da rodada em jogo (t_ef6e8a29): gates de autorização, hashes da build, configuração, cenários, evidências, critérios de aceite e lacunas — travado contra o disco por `t_aut4_runbook.py` |

## Reuso do CAP-1 (não reconstruído)

- Mesmo padrão do `scratch/cap1/CapProbe`: **driver no `PlayerLoop` do Unity** (o `Update` do plugin
  é destruído na 1ª cena — padrão provado no CAP-1), leitura por **reflexão** (o probe não quebra se
  o `Assembly-CSharp` mudar), `ScreenCapture.CaptureScreenshot` para o PNG, espera por **estado**
  (`GUIManager.instance.tooltip` + `TMP_Text` ativo com `GetParsedText()` não vazio) e
  **ida-e-volta** por `Tooltip.ShowTooltip(marcador)` + releitura do título.
- Formato de observação compatível com `capprobe.json`. O CAP-1 **não foi editado**.

## Correção dos achados da AUT-4R2 (o que mudou no comportamento)

| # | antes (defeito medido na revisão) | depois (COR-AUT4) |
|---|---|---|
| **A1** | o driver confirmava `CONCLUIDO` só olhando `aut4probe.json`; **JSON de rodada anterior** era consumido como se fosse desta rodada | `executar_rodada` exige **três provas independentes** (`provas_de_execucao`): (a) a evidência traz a **sessão gerada pelo driver** (chave `Sessao` no `.cfg`, devolvida no JSON) **e** o JSON é mais novo que o lançamento; (b) o `LogOutput.log` desta rodada tem o fim do chainloader **e** a linha de vida do probe; (c) `prints` não vazio, cada arquivo existindo com `bytes>0`. Falta de (a) ⇒ `NAO_EXERCITADO`/exit 2; falta de (b)/(c) ⇒ `INDETERMINADO`/exit 1 |
| **A2** | `campos_alvo` não governava: alvo não lido virava `NAO_APLICAVEL` (objeto inativo) e o cenário "fechava"; alvo inexistente/typo também fechava | campo-**alvo** em estado `AUSENTE`/`NAO_APLICAVEL` vira **lacuna** ⇒ `INCOMPLETO`/exit ≠ 0 (o fallback do inativo é informação, nunca satisfação do critério); e alvo **fora do schema** é `PlanoInvalido` (`validar_alvos` em `validar_plano`, `_alvos_do_plano` e `consolidar`) |
| **A3** | `consolidar_probe(..., procedencia='runtime')` maquiava fixture rotulada como runtime | o rótulo **lido do artefato** tem precedência: `FIXTURE`/exit 2 mesmo com o chamador pedindo runtime, com motivo registrado |
| **A4** | `status`/`fase` do probe (ERRO, SEM_UI, ORCAMENTO_ESTOURADO, NAO_EXERCITADO) não entravam no veredito | estado terminal de falha rebaixa para `ERRO`/`INCOMPLETO` com exit ≠ 0; **status ausente também não confirma** ("silêncio não é aprovação"); só `CONCLUIDO`/`OK` pode fechar `CONFIRMADA` |
| **A5** | o rollback removia **diretório pré-existente** (pasta do probe vazia) | `snapshot_dirs` + `planejar_rollback(dirs_criados/dirs_pre_existentes)` + `executar_rollback(preservar=...)`: diretório que já existia **sobrevive** (inclusive ancestrais) |
| **A6** | o aceite de "leitura ida-e-volta" não tinha instrumento no AUT-4 | porta **OPT-IN de ida-e-volta no probe**, declarada como **LEITURA**: `DemostrarTooltip` (default **false**) + `MarcadorIdaEVolta`; `DemostrarIdaEVolta()` chama o **handler real** `Tooltip.ShowTooltip(marcador)` e **relê** `Tooltip.Title`, gravando `ida_e_volta {marcador, titulo_lido, titulo_renderizado_lido, conferiu}`. O driver gera o marcador e **exige `conferiu==true`** para confirmar a rodada |
| **A7** | estado declarava DLL/contagens desatualizadas; este doc repetia as contagens antigas de testes e de iscas | estado passa a declarar **hash medido da DLL em disco**, **hash do fonte**, a **não-reprodutibilidade byte a byte** e a regra "identidade = hash declarado"; listas de testes/iscas/fixtures iguais às do disco; este doc cita os números reais. `t_aut4_estado_docs.py` trava a deriva |

## Build (compilado 1x, sem deploy)

```
cd tools/automacao/runtime/AUT4Probe
dotnet build -c Release --no-incremental -v q -p:DeployToBepInEx=false AUT4Probe.csproj
```
- **Build succeeded — 0 Error(s)**, 1 warning MSB3277 (`System.Net.Http`) herdado das DLLs do jogo
  (igual ao CapProbe). Sem flag de deploy: **o csproj não tem alvo `DeployToBepInEx`**.
- Build com `USERPROFILE`/`APPDATA`/`LOCALAPPDATA` redirecionados para pasta de trabalho.
- DLL: `AUT4Probe/bin/Release/AUT4Probe.dll` · sha256 `407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7`.
- Fonte: `AUT4Probe/AUT4ProbePlugin.cs` · sha256 `48afd3c41cf3ba97c93e5fc2d6b02ca58298939bf4b2a51f0ccd159ec96e3e94`.
- Componentes novos (AUD-1 / `t_6db50f7a`): `AUT4Probe/LeituraAgregados.cs` sha256
  `2506ec6478dd5a6bd445f2726c6595015f877f5e6465201d10c12a439c36cab0` (agregados do CAP-1 num
  componente isolado, somente leitura) e `AUT4Probe/IdentidadeDoProbe.cs` sha256
  `c23574f324f7a70ddeb2edb484daf292ebd92fc07eb0304bfbf343e58d27bfa6` (bloco `identidade` no JSON).
- **Identidade do artefato = hash DECLARADO**, nunca "compila igual": a DLL do probe **não é
  reproduzível byte a byte** (build sem `-p:PathMap`) — um rebuild do mesmo fonte gera outro hash.
  A rodada runtime deve rebuildar da fonte e **conferir** o sha256 antes de instalar.
- Perfil do dono **intacto** (verificado: nenhuma pasta `AUT4Probe` em `plugins/`).

## Testes offline (exit real)

`python tools/automacao/runtime/roda_testes_runtime.py` → **VERDE (exit 0)** — 15/15:
autorização (default offline), plano (+`campos_alvo` fora do schema), observação (AUSENTE nunca OK),
manifest/rollback, controle negativo, contrato do probe (gate/`NAO_EXERCITADO`/`PlayerLoop`/
`ScreenCapture`/owners/`Sessao`/ida-e-volta/`DeployToBepInEx` ausente + os **agregados isolados**
`LeituraAgregados.cs` e a **identidade** do fonte/DLL no JSON — L1 da AUD-1), costura probe→coletor
(A2/A3/A4), execução (A1/A2/A5/A6 contra stub, sem jogo), estado×disco (A7) e CIC-5R
(R-1..R-5/S-2/S-3), restauração/backup (`t_aut4_restauracao.py`: resíduo, ordem forçada, registro
do backup do log).

`... --contra-prova` → **VERDE (exit 0)** — as 31 iscas **reprovam como deviam** (nenhuma por
"excecao inesperada": R-5 do CIC-5R). As 7 novas iscas
(A1/A2 ×2/A3/A4/A5/A6) foram **vistas PASSANDO** contra o código antigo, ou seja: o defeito existia,
a isca o detecta e o runner acusa — e depois da correção elas reprovam.

**Fidelidade do critério de EFEITO (revisão rodada 1 de `t_6db50f7a`):** o `inventario` emitia
`criterio_de_efeito` como "espelho do critério do BetterFont" mas media a sombra por
`_UnderlayColor.a > 0` — ramo que o mod **não tem** (o BetterFont decide a sombra em
`SombraDesenhada`: keyword `UNDERLAY_ON`/`UNDERLAY_INNER` ligada **ou**
`_UnderlayOffsetX`/`_UnderlayOffsetY`/`_UnderlayDilate` ≠ 0). A sombra **inerte** do jogo (cor com
alfa, keyword desligada, offset/dilate zero) era contada como efeito pelo probe e como SEM efeito
pelo mod — número rotulado sob um critério que não é o do mod. Agora o agregado **delega a
`SombraDesenhada(m)`** (mesmo critério do BF-5) e o rótulo é **conferido contra a fonte**:
`t_aut4_probe_contrato.py §11.3` extrai o corpo de `SombraDesenhada` do `BetterFont/Plugin.cs` e do
`LeituraAgregados.cs` e exige o **mesmo conjunto de tokens** (keyword + geometria), com
`_UnderlayColor` fora do critério. Isca: `cp_aut4probe_isca_sombra_por_cor.py` (planta o critério
antigo e a geometria faltando — reprova nas duas).

**COR-AUT4-F2 (achados da revisão COR-AUT4R):** +4 iscas (A1-c/A2/A3/A6) e as correções da revisão
COR-AUT4R — vazio é NÃO LIDO (`""`/`[]`/`{}`), a prova de print é datada (posterior ao lançamento),
`evidencia_runtime: false` sozinho é declaração de fixture, e a ida-e-volta exige o marcador do driver.
Relatório em `docs/automacao/COR-AUT4-F2-relatorio.md`.

**COR-AUT4-F3 (ressalva não bloqueante da COR-AUT4-F2R):** +1 isca (a FORMA de `evidencia_runtime`).
`consolidar_probe` só confirma runtime com a chave `evidencia_runtime` AUSENTE (o probe C# real não
emite a chave) ou o bool `True` legítimo; qualquer outra forma PRESENTE — bool `False`, string
`"false"`/`"0"`, inteiro `0`, `null` — é RECUSADA como `FIXTURE` (exit 2), nunca `CONFIRMADA`.
Relatório em `docs/automacao/COR-AUT4-F3-relatorio.md`.

Contratos exercitados via CLI (`coletor.py`): default → `NAO_EXERCITADO` (exit 2); autorizado-sem-jogo
→ `NAO_EXERCITADO` (exit 2); fixture → `FIXTURE / NAO PROVA RUNTIME` (exit 2); autorizado+confirmado+
com-jogo → plano de 6 passos + rollback de 3 itens (execução reservada à próxima rodada).

## Detector de ausência/indeterminado — o detector que SABE DIZER NÃO (t_a5994af0)

`coletor.detectar_leitura` (CLI: `--detectar` com `--saida-probe`) julga uma leitura num
vocabulário **FECHADO**: `CONFIRMADA` | `NO` | `AUSENTE` | `NAO_EXERCITADO` | `INCOMPLETO`.
As regras vão nesta ordem (a primeira que casa manda):

1. `reinicio_necessario` ou `exercitado=False` → **`NAO_EXERCITADO`** (exit 2) — o caminho
   **sem acesso autorizado ao jogo** (ou sem a instrumentação carregada): nada foi lido.
2. procedência `fixture` → **`INCOMPLETO`** (exit 2) — fixture rotulada **nunca** confirma.
3. provas de execução incompletas / estado terminal de falha do instrumento / instrumento sem
   status de conclusão → **`INCOMPLETO`** (exit 1) — "silêncio não é aprovação".
4. nenhuma observação lida, ou **nenhum campo-alvo lido** → **`AUSENTE`** (exit 1).
5. leitura **válida** e a **expectativa declarada** (`esperado` no plano/cenário) **não casa** →
   **`NO`** (exit 1) — o detector diz NÃO. `NO` exige leitura: campo não lido vira `AUSENTE`,
   nunca `NO`.
6. alvo declarado não lido (**lacuna**) → **`INCOMPLETO`** (exit 1).
7. só então → **`CONFIRMADA`** (exit 0).

**Invariantes travados pelo teste:** nenhum caminho confirma sem leitura válida; `dados_sinteticos`
é **sempre** `False` (nunca fabrica); `hot_reload` é **sempre** `False`; todo veredito negativo
carrega exit ≠ 0 e motivo declarado; status desconhecido/ausente → `INCOMPLETO`
(`veredito_do_status`, "silêncio não é aprovação").

**Identidade do resultado:** todo resultado identifica **hash de fonte/DLL, configuração, cenário,
observado/esperado, evidência e lacunas** (`coletor.identificacao_do_resultado`); o caminho
executável anexa o bloco `identificacao` em **todos** os retornos, e o hash de fonte é o sha256
**medido** da DLL em disco.

Prova: `t_aut4_detector_no.py` (11 casos na fixture `cenarios-negativos`, incluindo o caso `no`) e as
iscas `cp_aut4_isca_detector_confirma_leitura_vazia.py` e
`cp_aut4_isca_detector_confirma_sem_status.py`.

**Correção da revisão AUT-4R rodada 1 (defeito grave, mesma classe do A1):** o caminho `--detectar`
**confirmava sem status de conclusão**. Um artefato com leitura válida e a expectativa casando, mas
com a chave `status` **ausente ou vazia**, saía `CONFIRMADA`/exit 0 pelo `--detectar` — enquanto o
**mesmo** artefato pelo `--saida-probe` (`consolidar_probe`) saía `INCOMPLETO`. Causa: o
curto-circuito `if st and st not in STATUS_PROBE_OK` deixava o silêncio passar. Corrigido para
`if st not in STATUS_PROBE_OK`: o status de conclusão é **OBRIGATÓRIO** (só `CONCLUIDO`/`OK`
atravessam) — alinhado com a docstring (regra 3), com o irmão `consolidar_probe` e com
`veredito_do_status(None/\"\")`. A fixture `cenarios-negativos` passou a declarar `status_conclusao` e
todo caso abaixo do portão de status o usa (o caminho positivo `CONFIRMADA` continua exercitado).
Prova: o bloco novo de `t_aut4_detector_no.py` (status `None`/`\"\"` ⇒ `INCOMPLETO`; com status
declarado ⇒ `CONFIRMADA`) e a isca `cp_aut4_isca_detector_confirma_sem_status.py`, **vista
PASSANDO** contra o defeito plantado (fora do repo) e reprovando por ASSERT depois da correção.

**Lacuna declarada no lane `--detectar`:** ele lê um artefato **já existente** e **não** passa
`provas` ao detector — nem `provas.ok` nem a atualidade da sessão são checadas nesse caminho (a
prova de execução só existe no `--executar`, que gera a sessão e o lançamento). O que o lane
garante: status de conclusão **obrigatório**. Quem precisar da prova de execução usa `--executar`.

## Controle negativo (fixture) e controle negativo ISOLADO (t_a5994af0)

`fixtures/casos-invalidos.entrada.json` traz 5 casos **invalidados** (sem procedência; runtime sem
hash/sessão; `AUSENTE` marcado OK; fixture reetiquetada de runtime; hash vazio). O teste
`t_aut4_controle_negativo.py` exige que **todos sejam recusados** — e recusa pelo motivo declarado.
Fixtures são **rotuladas** (`procedencia: fixture`, `evidencia_runtime: false`) e **nunca** podem ser
apresentadas como leitura de jogo.

O controle negativo **ISOLADO** (`controle_negativo.py`) é a prova executável de que o veredito
negativo sai **num perfil isolado**, sem tocar no perfil do dono:

- `exigir_perfil_isolado` é **FAIL-CLOSED**: perfil e `out_dir` têm de estar **dentro** de uma raiz
  isolada explícita, e a raiz isolada **não** pode estar dentro do perfil do dono. Apontar para o
  perfil do dono (ou para dentro dele) é **RECUSADO** — a DLL do dono não é movida sem autorização.
- o lançamento é por **STUB** (processo de Python): o lançador real do jogo (`steam.exe`) é
  **recusado**; sem `--stub` o caminho autorizado não roda.
- o perfil do dono é **medido antes e depois** (impressão por `stat`: `{rel: bytes:mtime_ns}`) e o
  controle **acusa** qualquer toque.
- `autorizado=False` → o driver **não age** (nenhum probe, nenhum `.cfg`, o stub não roda) e sai
  `NAO_EXERCITADO`/exit 2 com **zero** observação. `autorizado=True` + stub que não escreve leitura
  → a rodada **roda** (o argv fica em disco) e mesmo assim **não** confirma: `NAO_EXERCITADO`/exit 2,
  zero observação, `dados_sinteticos: false`.

Prova: `t_aut4_controle_isolado.py` e a isca `cp_aut4_isca_controle_negativo_no_perfil_do_dono.py`.

## Jogo aberto e frente única (t_a5994af0)

Com o jogo **JÁ ABERTO** a rodada só **LÊ** instrumentação **já carregada**
(`coletor.decidir_com_jogo_aberto`, CLI `--jogo-aberto [--probe-carregado]`). Sem o probe
carregado não há o que ler: a rodada declara **REINÍCIO NECESSÁRIO** e sai `NAO_EXERCITADO` — o
driver **nunca promete hot-reload** (`hot_reload: False` sempre), e reiniciar o jogo exige
autorização explícita do dono.

**Uma única frente controla o jogo**: `decidir_autorizacao(..., frente_ativa=True)` →
`NAO_EXERCITADO` mesmo autorizada, e no caminho executável o lançador **não chega a rodar**.

Prova: `t_aut4_jogo_aberto_frente.py` e a isca `cp_aut4_isca_jogo_aberto_promete_hot_reload.py`.

## Segurança (o que a próxima rodada vai exercer)

- **Opt-in**: `Autorizado=false` por padrão → o probe grava `{"status":"NAO_EXERCITADO"}` e não lê/navega/printa.
- **Rodada identificada**: `Sessao` (do driver) no `.cfg` e no JSON; sem ela, a rodada não confirma.
- **Prova de execução**: log (chainloader + linha de vida do probe) e `prints` com bytes > 0.
- **Rollback EXATO** (`docs/automacao/AUT-4-contrato-restauracao.md`): manifest com nome/bytes/sha256;
  rollback classifica criados/modificados/removidos — inclusive o `.cfg` que nasce sozinho na 1ª
  execução **e o arquivo que a rodada cria FORA do contrato** (`BepInEx/plugins/**` e
  `BepInEx/config/**` são varridos inteiros) — e **preserva diretório que já existia**.
- **Prova de restauração** (pos-rollback): `resultado["restauracao"]` (`verificar_sem_residuo`)
  confere o perfil contra o estado de antes; resíduo/divergência/falta/diretório sobrando ⇒ status
  `RESIDUO`/exit ≠ 0 — rodada suja **não** se apresenta como limpa (falha de rollback também é
  registrada, sem derrubar o driver).
- **Backup do log**: `LogOutput.log` é arquivado antes de lançar (`out_dir/log-anterior.log`) com
  bytes/sha256 no registro; ausência de log anterior é **declarada**, nunca inventada.
- **Encerramento em duas etapas**: fechamento **gracioso** (`CloseMainWindow`) primeiro e forçado por
  PID só como *fallback* (sem medição dos PIDs, RECUSA — `taskkill /IM` não existe no driver).
- **Timeout/espera de estado**: teto de tempo (`OrcamentoSegundos`) + espera por estado, não sleep cego.
- **Ida-e-volta opt-in** (leitura): `DemostrarTooltip`/`MarcadorIdaEVolta`, default **false**.
- **Uma frente runtime por vez**; `LogOutput.log` é truncado a cada boot → arquivar antes de lançar.

## Lacunas de runtime (declaradas; NÃO são OK)

- Nada foi exercitado em jogo: leitura real, PNG, owners em sessão viva, navegação e o rollback
  **executado** em jogo (o plano, a execução contra stub e o rollback por bytes estão testados).
- A **ida-e-volta** tem instrumento e é exigida pelo driver quando o plano pede, mas **nunca rodou
  numa sessão viva**: é **NÃO EXERCITADO**.
- O gate de autorização do probe foi testado **estaticamente** (contrato do fonte) e no contrato do
  driver, não em execução.
- O **encerramento** (`CloseMainWindow` gracioso → `taskkill /F /PID` de fallback) e o **rollback
  contra o perfil do dono** nunca rodaram: o que está provado é a **decisão**, a **ordem** e a
  execução com **executor injetado** (nenhum processo de jogo foi tocado).

## Runbook da rodada autorizada (t_ef6e8a29)

`docs/automacao/AUT-4-runbook-rodada-autorizada.md` consolida, num único documento, a prova
**offline** já revisada e o procedimento da rodada **em jogo** (que só ocorre com autorização do
dono): gates de autorização (G1–G8), identidade da build (hashes de fonte/DLL/componentes e a DLL
do jogo), configuração (plano `AUT-4/1` + as chaves do `.cfg` derivado), cenários C0–C7 com
observado/esperado, evidências, critérios de aceite AC1–AC10 e as lacunas declaradas. Deixa
explícito que **a automação não substitui o aceite humano nem a publicação do DoD**.

O runbook é **travado contra o disco**: `t_aut4_runbook.py` exige que todo sha256 citado case byte
a byte com o arquivo, que todas as chaves vivas de `coletor.CFG_CHAVES` estejam documentadas e que
as contagens de testes/iscas sejam as reais. Isca:
`testes/contra-prova/cp_aut4_isca_runbook_hash_velho.py` (afirma o falso — hash de DLL velho ou
chave de `.cfg` faltando "passariam").

## Necessidade concreta de reinício/probe (próxima rodada autorizada)

1. Autorização explícita do dono + uma única frente controlando o jogo.
2. O probe é **novo** → exige **instalar e iniciar** (não há hot-reload; declarar reinício).
3. `Autorizado=true` + `HashFonte` (sha de fonte/DLL) na rodada; perfil passado para o rollback.
4. Perfil **isolado** para o controle negativo quando possível (sem mover DLL do perfil do dono sem autorização).
5. Ao fim: consumir `manifest`+`rollback` e restaurar/remover exato o que a rodada criou.
6. Para o critério de ida-e-volta: plano com `demostrar_tooltip=true` e conferir `ida_e_volta.conferiu` no JSON.
