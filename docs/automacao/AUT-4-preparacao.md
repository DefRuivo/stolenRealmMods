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
| `tools/automacao/runtime/coletor.py` | **driver/orquestrador** (contrato + decisão de autorização + normalização de observação + **provas de execução** + manifest/rollback), CLI opt-in |
| `tools/automacao/runtime/roda_testes_runtime.py` | runner offline (exit 0/1/2, `--contra-prova`) |
| `tools/automacao/runtime/testes/` | 10 testes offline + 22 iscas de contra-prova |
| `tools/automacao/runtime/fixtures/` | fixtures **rotuladas** (nunca evidência de runtime) |
| `docs/automacao/AUT-4-estado.json` | estado legível por máquina (listas e hashes conferidos contra o disco) |

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
- DLL: `AUT4Probe/bin/Release/AUT4Probe.dll` · sha256 `fd774259b5e8813f2f3b29e2ff805f12cb0cdab4c277116fcc8bbb7e7e3bffdd`.
- Fonte: `AUT4Probe/AUT4ProbePlugin.cs` · sha256 `5a51abaa439b90263e3b202e01a0b2b3b343fabc8cb71c9de8b3ac97b343bdd3`.
- **Identidade do artefato = hash DECLARADO**, nunca "compila igual": a DLL do probe **não é
  reproduzível byte a byte** (build sem `-p:PathMap`) — um rebuild do mesmo fonte gera outro hash.
  A rodada runtime deve rebuildar da fonte e **conferir** o sha256 antes de instalar.
- Perfil do dono **intacto** (verificado: nenhuma pasta `AUT4Probe` em `plugins/`).

## Testes offline (exit real)

`python tools/automacao/runtime/roda_testes_runtime.py` → **VERDE (exit 0)** — 10/10:
autorização (default offline), plano (+`campos_alvo` fora do schema), observação (AUSENTE nunca OK),
manifest/rollback, controle negativo, contrato do probe (gate/`NAO_EXERCITADO`/`PlayerLoop`/
`ScreenCapture`/owners/`Sessao`/ida-e-volta/`DeployToBepInEx` ausente), costura probe→coletor
(A2/A3/A4), execução (A1/A2/A5/A6 contra stub, sem jogo), estado×disco (A7) e CIC-5R
(R-1..R-5/S-2/S-3).

`... --contra-prova` → **VERDE (exit 0)** — as 22 iscas **reprovam como deviam** (nenhuma por
"excecao inesperada": R-5 do CIC-5R). As 7 novas iscas
(A1/A2 ×2/A3/A4/A5/A6) foram **vistas PASSANDO** contra o código antigo, ou seja: o defeito existia,
a isca o detecta e o runner acusa — e depois da correção elas reprovam.

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

## Controle negativo

`fixtures/casos-invalidos.entrada.json` traz 5 casos **invalidados** (sem procedência; runtime sem
hash/sessão; `AUSENTE` marcado OK; fixture reetiquetada de runtime; hash vazio). O teste
`t_aut4_controle_negativo.py` exige que **todos sejam recusados** — e recusa pelo motivo declarado.
Fixtures são **rotuladas** (`procedencia: fixture`, `evidencia_runtime: false`) e **nunca** podem ser
apresentadas como leitura de jogo.

## Segurança (o que a próxima rodada vai exercer)

- **Opt-in**: `Autorizado=false` por padrão → o probe grava `{"status":"NAO_EXERCITADO"}` e não lê/navega/printa.
- **Rodada identificada**: `Sessao` (do driver) no `.cfg` e no JSON; sem ela, a rodada não confirma.
- **Prova de execução**: log (chainloader + linha de vida do probe) e `prints` com bytes > 0.
- **Rollback EXATO**: manifest com nome/bytes/sha256; rollback classifica criados/modificados/removidos
  — inclusive o `.cfg` que nasce sozinho na 1ª execução — e **preserva diretório que já existia**.
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

## Necessidade concreta de reinício/probe (próxima rodada autorizada)

1. Autorização explícita do dono + uma única frente controlando o jogo.
2. O probe é **novo** → exige **instalar e iniciar** (não há hot-reload; declarar reinício).
3. `Autorizado=true` + `HashFonte` (sha de fonte/DLL) na rodada; perfil passado para o rollback.
4. Perfil **isolado** para o controle negativo quando possível (sem mover DLL do perfil do dono sem autorização).
5. Ao fim: consumir `manifest`+`rollback` e restaurar/remover exato o que a rodada criou.
6. Para o critério de ida-e-volta: plano com `demostrar_tooltip=true` e conferir `ida_e_volta.conferiu` no JSON.
