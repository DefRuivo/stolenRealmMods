# AUT-4 — parte 04: detector sobre a evidência REAL, aceite por critério, lacunas e veredito

> Cartão `t_b8b9822e` · worker `default` (run 622) · 2026-10-09, 18:5x BRT.
> Continua `AUT-4-parte03.md`. Este documento **não** declara o cartão concluído nem publica DoD:
> quem aceita a rodada e quem publica é o humano. O que está abaixo é medido.

## 1. O detector sobre a evidência REAL (não sobre fixture)

Os dois julgamentos abaixo foram executados por mim, **contra os `aut4probe.json` reais coletados em
jogo** (arquivos preservados em `docs/automacao/AUT-4-evidencias/`), com o mesmo binário do probe
(`--dll-probe … 407c5c63…`):

| evidência | plano | veredito | exit | `dados_sinteticos` | `hot_reload` | motivo |
|---|---|---|---|---|---|---|
| `r2` (real) | `plano-r2.json` — declara `texto_bruto`/`texto_renderizado` como alvo | **`INCOMPLETO`** | 1 | false | false | `ha lacuna: alvo(s) nao lido(s) texto_bruto, texto_renderizado — AUSENTE/INDETERMINADO nunca e OK` |
| `r3` (real) | `plano-r3.json` — alvos governantes = os campos medidos em **todo** objeto lido | **`CONFIRMADA`** | 0 | false | false | `leitura valida (sem expectativa declarada: nada a negar)` |

Mesma evidência de instrumento, dois vereditos — porque o que **governa** é o `campos_alvo` declarado.
É a demonstração, em runtime, dos achados A2/S-3: alvo declarado e não lido **vira lacuna** (não fecha
`CONFIRMADA`), e campo fora do alvo **não penaliza**. O detector **sabe dizer NÃO** com dado real:
na r2 ele recusou confirmar, nomeando os campos e o motivo.

`--detectar` preserva as invariantes: `dados_sinteticos=false` e `hot_reload=false` em **todos** os
retornos (inclusive nos negativos), e nenhum veredito negativo carrega exit 0.
(Lacuna herdada e declarada: o lane `--detectar` lê um artefato já existente e **não** passa `provas` —
a prova de execução mora no caminho `--executar`; ver `AUT-4-estado.json` →
`detector_de_ausencia.lane_cli_detectar`.)

## 2. Aceite por critério (runbook `AUT-4-runbook-rodada-autorizada.md` §7)

| # | critério | resultado medido | prova |
|---|---|---|---|
| AC1 | **Autorização e frente única** | gates G1–G4 verdes; `decisao.modo=runtime`, `pode_coletar=true`; lock de frente única adquirido/liberado | `resultado-r{2,3,4}.json` → `decisao`; `front-unica.sh` |
| AC2 | **Identidade da build** | `atualidade.dll_sha == hash_fonte == probe_hash_fonte == 407c5c63…`, `fonte_ok=true`, `sessao_ok=true`; o `HashFonte` está no `.cfg` E no JSON do probe (`identidade.hash_dll_do_probe` calculado em runtime) | `cfg-instalado.cfg`, `aut4probe.json` |
| AC3 | **Leitura ida-e-volta** | **`ida_e_volta.conferiu == true`** nas 3 rodadas, com o **marcador do driver** lido de volta = `AUT4-IDA-E-VOLTA-<sessão>` | `provas_execucao.ida_e_volta` |
| AC4 | **PNG pela API do Unity** | 2 PNG por rodada, 2,5–2,8 MB, 1920×1080, `posterior_ao_lancamento=true`; `01-ui.png` **vista**: tela de LOADING do jogo com texto renderizado | `out/r{2,3,4}/*.png` (preservados) |
| AC5 | **Owners Harmony vivos** | owners **lidos de `Harmony.GetPatchInfo` no método vivo**: `GUIManager.Update` e `OptionsManager.Localize` → `["com.gumatos.aut4probe"]` | `aut4probe.json` → `owners_harmony` |
| AC6 | **Detector sabe dizer NÃO** | r2 ⇒ `INCOMPLETO` com lacuna nomeada; r1 (sem leitura) ⇒ `NAO_EXERCITADO` com `observacoes: []` | §1 e `AUT-4-parte02.md` §3 |
| AC7 | **Rollback exato** | `restauracao.limpo == true` nas 3 rodadas; perfil/saves do dono com hash **idêntico** ao “antes” | `resultado-r*.json` → `restauracao`; `antes.txt`/`depois.txt` |
| AC8 | **Encerramento em 2 etapas** | fechou **gracioso** (`CloseMainWindow`) na 1ª tentativa, só o PID nascido na rodada (`pids_antes=[]`); o forçado não foi necessário | `resultado-r*.json` → `encerramento` |
| AC9 | **Nada fabricado** | `dados_sinteticos=false` e `hot_reload=false` em **todo** retorno (r1…r4 e detectores) | todos os JSON |
| AC10 | **Aceite humano e DoD** | **aberto** — este artefato não aprova nem publica; a rodada vai para **revisão independente** | este documento |

## 3. Lacunas declaradas (não são OK; nenhuma é maquiada)

- **Navegação por handler real de UI**: **NÃO EXERCITADA** — não autorizada pelo KIT-G1 (G8).
- **Save / combate**: **NÃO EXERCITADOS** — não autorizados.
- **Fallback de encerramento forçado por PID**: **NÃO EXERCITADO em jogo** (nas 3 rodadas o gracioso
  bastou). A *ordem* gracioso→forçado segue provada só offline (executor injetado).
- **Gate `Autorizado=false` do probe**: exercitado **offline** (suíte), não em jogo — as rodadas
  passaram `Autorizado=true` (era o objetivo).
- **Log cru**: preservado **só na r4**; nas r2/r3 o rollback exato removeu o `LogOutput` da cópia
  (comportamento correto). Os booleanos `log_chainloader`/`log_probe` das r2/r3 vêm da leitura do
  driver durante a rodada, registrados em `provas_execucao`.
- **Owners de um mod de terceiro**: não observados — no perfil isolado só o instrumento está carregado.
- **`texto_renderizado` de objeto INATIVO** sai vazio (NAO_APLICAVEL): é o TMP; só o `texto_bruto` vale
  — declarado em cada observação (`nota_texto_renderizado`).
- **Janela**: r2/r3/r4 = ~22 s de sessão cada; a r1 queimou 240 s por falha **minha** de configuração
  (`--perfil`), já explicada. Nenhuma delas excedeu o teto declarado no KIT-G1.
- **DLL do probe não é reproduzível byte a byte** (build sem `-p:PathMap`): a identidade é o **hash
  declarado** `407c5c63…` — conferido, não recompilado nesta rodada.

## 4. Veredito desta execução

**A rodada isolada autorizada FOI EXECUTADA e a leitura viva ida-e-volta existe.**
O critério que sempre esteve “NÃO EXERCITADO” deixou de estar: leitura do objeto vivo, PNG pela API do
Unity, owners Harmony lidos em execução, ida-e-volta confirmada com o marcador do driver, rollback
exato e encerramento por PID — **medidos em jogo**, em ambiente **isolado**, com o perfil e os saves do
dono **bit-a-bit intactos**. Os vereditos foram produzidos pelo próprio instrumento: `INCOMPLETO` (r2),
`CONFIRMADA` (r3 e r4) e `NAO_EXERCITADO` (r1) — **nunca** um dado fabricado.

*Isto **não** substitui o aceite humano nem a publicação do DoD.* O cartão segue para **revisão
independente** (KIT-R0/revisor), que deve tentar **refutar** esta rodada — inclusive reexecutando o
detector sobre os JSON preservados — sem reutilizar parecer antigo como aprovação.

## 5. Encerramento limpo (medido depois das rodadas)

| item | resultado |
|---|---|
| processo do jogo | **AUSENTE** (`tasklist \| grep -i stolen` → vazio) |
| área isolada | `scratch/aut4-runtime-iso` **removida** (verificado: `[ -d ]` falso) |
| lock de frente única | **liberado** (`Lock liberado`; `check` → “lock disponivel”, exit 0) |
| perfil do dono | `plugins 6eae7a3c…`, `core b1594200…`, `LogOutput 9bedadac…`, saves `04ef12fa…` — **idênticos ao início** |
| resíduo `AUT4*` no perfil do dono | **nenhum** |
| `lib/Assembly-CSharp.dll` | `8bb4a7c5…` (**intacta**) |
| repo | só arquivos **novos** (`docs/automacao/AUT-4-parte0{1,2,3,4}.md`, `docs/automacao/AUT-4-evidencias/**`); nenhum arquivo de mod/produto/KANBAN alterado |

## 6. Hashes da evidência (para o revisor conferir byte a byte)

| arquivo | sha256 |
|---|---|
| `r1-falha/resultado-r1.json` | `fca468c3fd19901239a11db8a508dbfefa6e81eb2df8052f6c7ac4b50e2270ce` |
| `r2-incompleto/resultado-r2.json` | `abf1e50c77fad3987b01c506ce9e70e5296436fa8ca01a9fe15ac8084d34af37` |
| `r2-incompleto/aut4probe.json` | `f9ffe403b707e58e134dd5e39233ba7a67e43cdf477cd923b722ac8ae0a88e05` |
| `r2-incompleto/01-ui.png` | `7205ec2cd097886e63a7a99497a1ed347f90c91df1cd4bcca17c9a8332f16221` |
| `r2-incompleto/detector-r2.json` | `25694d1bc4e76ed59d625b49b2a0f4474f4d2236523f03701fc2ed29acf96d47` |
| `r3-confirmada/resultado-r3.json` | `4e0e4d8fd65a49cc61c9e2aa9cd33bf089b8ebf46a30973b243b79d442f70372` |
| `r3-confirmada/aut4probe.json` | `5bef1c67e21365ccf84d02ff645715e254a4e1140aec77d62c6b12de689a158d` |
| `r3-confirmada/01-ui.png` | `b68a73431a5bdd3b3245e01dec693fca9be1c97ddea930cc24e1a31f36ab0757` |
| `r3-confirmada/02-final.png` | `ab8bfcf2483255e1b328b82231f5789ba7c762c1f9574bce80efc0ac6624b132` |
| `r3-confirmada/detector-r3.json` | `a6e399f0bf07b7ff33d246c0c1ad558504b2159fe6756d7e6b62721a815dacb0` |
| `r4-confirmada-log/resultado-r4.json` | `e2913309230caf44f5eac1df695107707e8656d9c9c8d0ab13354322bd3b19b4` |
| `r4-confirmada-log/aut4probe.json` | `c4296aee9957a7ea87e16f45721ecbdbd35efd8f4b02b2a4f14a5b5df8201e13` |
| `r4-confirmada-log/LogOutput-copia.log` | `e1e4e26fac891f50204900f05c9471b90277ebdaa1cfc9d3fa93acfeff992ab7` |
| `r4-confirmada-log/01-ui.png` | `bd7226e08fd82b1201a1548f567de4f285489daff1b787c9568249b656b5ea11` |
| `antes.txt` | `10b4ad5c8cd8cbf6957722e55d7e1fee8e42665d3c381d1df92d77caa49917eb` |
| `depois.txt` | `3bd24d0fc4ace2ee7572a62b2967efcd4c89c68eab3a7c5e97b07bc260c03aeb` |

Cada rodada preserva também `plano-rN.json`, `cfg-instalado.cfg` e `lancamento.txt` (argv + PID + sessão).
