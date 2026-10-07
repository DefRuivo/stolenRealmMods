# AUT-4F — correção dos achados da AUT-4R2 e da CIC-5R no coletor de runtime

Tarefa: **`t_fc40b2a7`** (AUT-4F) · Rodada: **07/10/2026**, **OFFLINE**.
Autor: perfil `default`. Escopo de escrita: `tools/automacao/runtime/**` e `docs/automacao/AUT-4*`.
Pareceres-fonte lidos antes de tocar em código: `docs/automacao/AUT-4R2-revisao.md` (veredito
REPROVADO) e `docs/automacao/CIC-5R-revisao.md` (veredito CHANGES REQUESTED). Os cartões-filhos
(`t_b8b9822e` AUT-4, `t_431dba37` CIC-5) seguem bloqueados e voltam para re-review quando este
fechar.

**Regras cumpridas:** nenhum jogo aberto/encerrado, nenhum save tocado, **nenhum probe instalado**,
**nenhum deploy** (`AUT4Probe.csproj` não tem alvo `DeployToBepInEx`; build com a flag em `false`),
**nada commitado/staged**, perfil do dono intacto (`plugins/` sem `AUT4Probe`). `lib/Assembly-CSharp.dll`,
fontes de mods, `ciclo/`, `cenarios/` de produto e o board não foram tocados.

---

## 1. O que a frente encontrou (confirmação no parecer **e no código**, antes de corrigir)

Ao conferir cada achado contra o estado real do repositório, descobriu-se que **parte dele já havia
sido fechada** por uma cadeia de correções posterior aos pareceres (`COR-AUT4`,
`COR-AUT4-F2/F3/F4`, com pareceres próprios em `docs/automacao/COR-AUT4*`). Nada foi aceito por
leitura de relatório: cada item foi **reproduzido por execução** e a trava conferida com **defeito
plantado** (§4). O que estava aberto de fato foi corrigido nesta frente.

| achado | parecer | estado encontrado no código (medido) | ação nesta frente |
|---|---|---|---|
| **A1** grave — driver confirma sem prova de execução | AUT-4R2 | **já fechado** (`provas_de_execucao`: sessão da rodada no `.cfg`/JSON + JSON mais novo + log com chainloader e linha de vida + prints com bytes>0 e mtime posterior) | contra-prova (§4). Defeito plantado `A1` derruba `t_aut4_execucao.py` |
| **A2** grave — `campos_alvo` não governa o veredito | AUT-4R2 | **já fechado** (`validar_alvos` = `PlanoInvalido` fora do schema; alvo `AUSENTE`/`NAO_APLICAVEL` = lacuna) | contra-prova (§4) |
| **A3** médio — rótulo do artefato não tem precedência | AUT-4R2 | **já fechado** (`consolidar_probe`: FIXTURE do próprio artefato vence o chamador) | contra-prova (§4) |
| **A4** médio — `status`/`fase` do probe fora do veredito | AUT-4R2 | **já fechado** (`STATUS_PROBE_FALHA`/`FASES_PROBE_FALHA` rebaixam; silêncio não aprova) | contra-prova (§4) |
| **A5** médio — rollback inexato para DIRETÓRIOS | AUT-4R2 | **já fechado** (`snapshot_dirs` + `dirs_pre_existentes` preservados) | contra-prova (§4) |
| **A6** médio — sem instrumento de ida-e-volta | AUT-4R2 | **já fechado** (`DemostrarTooltip`/`MarcadorIdaEVolta` no probe + driver exige o marcador) | contra-prova (§4) |
| **A7** documental — estado/DLL/contagens desatualizados | AUT-4R2 | **já fechado** por `t_aut4_estado_docs.py` (lista declarada == disco, hash declarado == bytes) — **mas voltou a ficar STALE**: `driver_sha256` apontava `b92c46c3…` e as contagens eram 9 testes/16 iscas | **atualizado**: `driver_sha256` = bytes atuais, `runner_sha256` novo, +1 teste e +6 iscas declarados |
| **S-1** grave — saída pré-existente aceita como desta rodada | CIC-5R | **já fechado** (mesma trava do A1) | contra-prova (§4) |
| **R-1** grave — `hash_fonte` (sha da **DLL**) confrontado com `fonte_sha` | CIC-5R | **já fechado** nos adaptadores (`_ALIAS_HASH`: `hash_fonte`/`hash_dll` → `dll_sha`) | travado por teste no `t_aut4_cic5r.py` (R-1) + defeito plantado |
| **R-2** médio — CLI `--executar` sem `--perfil` estoura antes do gate | CIC-5R | **ABERTO** (`os.path.abspath` na 1ª linha de `executar_rodada`) | **corrigido** (§2) |
| **R-3** médio — catch do probe grava `status=ERRO` sem `fase`; espera queima o teto | CIC-5R | **ABERTO** (`_esperar_estado` parava só por `fase`) | **corrigido** (§2) |
| **R-4** grave (risco) — `finally` encerra o lançador; `encerrar_imagem` mata por imagem | CIC-5R | **ABERTO** (`taskkill /F /IM` mataria todas as instâncias; comentário falso) | **corrigido** (§2) |
| **R-5** médio — runner de contra-prova aceita qualquer `exit==1` (crash conta como prova) | CIC-5R | **ABERTO**: a própria execução mostrava 2 de 16 iscas reprovando por `excecao inesperada` | **corrigido** (§2) |
| **S-2** backlog — `campos_alvo` só do topo/1º cenário | CIC-5R | **ABERTO** (`_alvos_do_plano` lia `cenarios[0]`) | **corrigido** (§2) |
| **S-3** backlog — campo EXTRA alvo nunca vira lacuna | CIC-5R | **já fechado** (o laço de lacunas usa os alvos efetivos validados contra `CAMPOS_TODOS`) | travado por teste + defeito plantado |

---

## 2. O que mudou nesta frente (`coletor.py`, `roda_testes_runtime.py`)

### R-2 — o gate vem ANTES de normalizar caminhos
`executar_rodada` chamava `os.path.abspath(perfil_dir)` na 1ª linha, **antes** de
`decidir_autorizacao`; com `--executar` sem `--perfil` (o default do CLI) isso dava
`TypeError: path should be string…` e **exit 1**, em vez do `NAO_EXERCITADO`/exit 2 prometido.
Agora `decidir_autorizacao` roda primeiro, e uma rodada autorizada **sem destino explícito**
(`perfil_dir`/`out_dir` vazios) sai `NAO_EXERCITADO`/exit 2 com o motivo nomeando o que falta —
nunca o perfil do dono por acidente.

### R-3 — a espera para por ESTADO TERMINAL (`fase` **ou** `status`)
O catch do `Tick` do probe (`AUT4ProbePlugin.cs:299-303`) grava `_res["status"]="ERRO"` **sem** setar
`_res["fase"]` (quem escreve `fase=concluido` é o `Finalizar()`, que o catch não chama). Como a
espera parava só por `fase ∈ FASES_TERMINAIS`, um erro do instrumento **queimava o teto inteiro**
(medido pelo revisor: 0,622 s de 0,6 s). `_esperar_estado` agora também para com
`status ∈ STATUS_TERMINAIS_ESPERA` (`STATUS_PROBE_OK + STATUS_PROBE_FALHA`) e registra o `status`
lido. O conserto ficou **no coletor** (arquivo único desta frente, single-writer); o probe não foi
tocado — o coletor passa a tolerar o artefato que ele realmente emite.

### R-4 — encerra SÓ os PIDs que nasceram nesta rodada
O `Popen` encerrado no `finally` é o **lançador** (`steam.exe`), não o jogo (no Windows o jogo é
processo à parte, que recebe o `--doorstop`), e `taskkill /F /IM <imagem>` mata **todas** as
instâncias da imagem — inclusive a que o dono já tinha aberta. O comentário/docstring que afirmava
"encerra SÓ a instância que a rotina lançou" era **falso** e foi corrigido. Agora:

* `pids_da_imagem(imagem)` fotografa os PIDs via `tasklist` (`None` = não deu para medir);
* a fotografia é feita **antes** do `Popen`;
* `planejar_encerramento` (função **pura**, testável sem tocar processo) decide:
  `pids_depois − pids_antes` → encerra **por PID** (`taskkill /F /PID`); sem medição → **RECUSA**
  (fail-closed) e registra o motivo em `resultado["encerramento"]`.

### R-5 — o controle negativo não aceita crash como prova
`roda_testes_runtime.py` marcava `PROVA OK` para **qualquer** `exit == 1`, e o arcabouço converte
**exceção inesperada** em exit 1 também. Nova função `classificar_contra_prova(codigo, saida)` exige
a linha `RESULTADO|REPROVOU|` (reprovação por `Falhou`/assert) **e** rejeita `excecao inesperada`.
As 2 iscas que reprovavam por exceção (`cp_aut4_isca_ausente_ok`, `cp_aut5_isca_topo_sem_hash_ok`)
passaram a reprovar por **assert explícito** — hoje as 22 iscas reprovam pelo caminho certo.

### S-2 — `campos_alvo` de TODOS os cenários governa o veredito
`_alvos_do_plano` lia o topo **ou** `cenarios[0]`; com 2+ cenários, o requisito por campo do 2º em
diante era descartado em silêncio (e, se `campos_alvo` existisse só no 2º, o plano voltava a mirar
os 13 campos de todo `TMP_Text`). Agora é a **união** validada do topo e de **todos** os cenários.
`_demostrar_do_plano` (mesma raiz) também passa a considerar qualquer cenário.

### Ajuste de guarda (documentado, não é afrouxamento)
`t_aut4_estado_docs.py` recusava as strings antigas com `"2 iscas" not in texto`; com a contagem
correta em **22 iscas** a substring "2 iscas" passa a existir dentro do próprio número correto — o
guard literal recusaria o dado certo. Trocado por fronteira de dígito (`(?<!\d)2 iscas`,
`(?<!\d)6/6`): a intenção (contagem antiga não sobrevive no doc) é a mesma, sem falso positivo.

---

## 3. Comandos exatos e saída literal (exit real)

```
$ python tools/automacao/runtime/roda_testes_runtime.py
[PASSOU] testes\t_aut4_autorizacao.py
[PASSOU] testes\t_aut4_cic5r.py
[PASSOU] testes\t_aut4_controle_negativo.py
[PASSOU] testes\t_aut4_costura_probe.py
[PASSOU] testes\t_aut4_estado_docs.py
[PASSOU] testes\t_aut4_execucao.py
[PASSOU] testes\t_aut4_manifest_rollback.py
[PASSOU] testes\t_aut4_observacao.py
[PASSOU] testes\t_aut4_plano.py
[PASSOU] testes\t_aut4_probe_contrato.py
==========================================================================
 VEREDITO: VERDE (exit 0) — 10 teste(s)          EXIT=0

$ python tools/automacao/runtime/roda_testes_runtime.py --contra-prova
(22 iscas) VEREDITO: VERDE (exit 0)             EXIT=0
   -> NENHUMA isca reprova por "excecao inesperada" (R-5 fechado)
```

Consumidores (não-regressão, rodados no repo):

```
python tools/automacao/cenarios/test_rstv.py              -> RESULTADO|PASSOU|cic3-rstv|…        EXIT=0
python tools/automacao/cenarios/test_tooltips_shrines.py  -> rodaram=28 reprovaram=0              EXIT=0
python tools/automacao/ciclo/test_ciclo.py                -> Ran 48 tests … OK                   EXIT=0
python tools/automacao/ciclo/test_decisao.py              -> total: 127 | falhas: 0  TUDO OK     EXIT=0
python tools/automacao/aut6/test_cobertura_aut6.py        -> rodaram=24 reprovaram=0              EXIT=0
python tools/automacao/aut6/test_regressoes_cor_aut6.py   -> Ran 26 tests … OK                   EXIT=0
python tools/automacao/estilo/test_estilo_atributos.py    -> total: 28 | falhas: 0  TUDO OK      EXIT=0
python tools/automacao/aceite/test_relatorio_aceite.py    -> total: 15 | falhas: 0  TUDO OK      EXIT=0
python tools/testes/roda_testes.py                        -> VEREDITO: VERDE (exit 0)            EXIT=0
```

Build do probe **sem instalar**, em cópia fora do repo, com `USERPROFILE`/`APPDATA`/`LOCALAPPDATA`
redirecionados:

```
$ dotnet build -c Release --no-incremental -v q -p:DeployToBepInEx=false AUT4Probe.csproj
    1 Aviso(s)   (MSB3277 System.Net.Http — herdado das DLLs do jogo)
    0 Erro(s)                                                     BUILD_EXIT=0
```

Identidade do artefato (A7): a DLL do repo é `fd774259…` e o **rebuild do MESMO fonte** na cópia deu
`724a1514…` — ou seja, **não é reproduzível byte a byte** (build sem `-p:PathMap`); identidade =
hash **declarado**, nunca "compila igual". O `coletor.py` **não** é compilado (é Python) e o probe
**não foi alterado** nesta frente: a fonte segue `5a51abaa…`, como declarado.

---

## 4. Contra-prova: defeito plantado ⇒ REPROVADO; sem defeito ⇒ OK

Script: `docs/automacao/AUT-4F-evidencias/planta_defeitos_aut4f.py`. Ele copia `tools/` + `docs/` para
uma pasta **fora do repo** (`%TEMP%\aut4f-planta`), planta **um** defeito por vez (a substituição
exata que reintroduz o comportamento reprovado), roda a suíte e a contra-prova e registra os **exit
codes reais**. Log: `docs/automacao/AUT-4F-evidencias/planta-defeitos.log`; resultados brutos:
`planta-defeitos-resultados.json`.

```
[CONTROLE      ] suite exit=0 (sem defeito)  contra-prova exit=0 (sem defeito)
[A1            ] suite exit=1 REPROVADO | reprovaram: t_aut4_execucao.py
[A2            ] suite exit=1 REPROVADO | reprovaram: t_aut4_costura_probe.py, t_aut4_execucao.py
[A3            ] suite exit=1 REPROVADO | reprovaram: t_aut4_costura_probe.py
[A4            ] suite exit=1 REPROVADO | reprovaram: t_aut4_costura_probe.py
[A5            ] suite exit=1 REPROVADO | reprovaram: t_aut4_execucao.py
[A6            ] suite exit=1 REPROVADO | reprovaram: t_aut4_execucao.py
[S-3           ] suite exit=1 REPROVADO | reprovaram: t_aut4_cic5r.py
[R-1           ] suite exit=1 REPROVADO | reprovaram: t_aut4_cic5r.py
[R-2           ] suite exit=1 REPROVADO | reprovaram: t_aut4_cic5r.py
[R-3           ] suite exit=1 REPROVADO | reprovaram: t_aut4_cic5r.py
[R-4           ] suite exit=1 REPROVADO | reprovaram: t_aut4_cic5r.py
[R-5           ] suite exit=1 REPROVADO | reprovaram: t_aut4_cic5r.py
[S-2           ] suite exit=1 REPROVADO | reprovaram: t_aut4_cic5r.py
 resumo: 13 defeitos plantados; travados por teste: 13/13
```

Observação honesta sobre a coluna da contra-prova: nas linhas em que o defeito **satisfaz** a
afirmação falsa de uma isca (ex.: A2 faz `cp_aut5_isca_alvo_nao_lido_ok` PASSAR quando ela tem de
reprovar), a própria corrida `--contra-prova` sai vermelha — é sinal **redundante** de que o defeito
voltou, não uma falha da frente.

---

## 5. Testes e iscas novos

* **+1 teste**: `tools/automacao/runtime/testes/t_aut4_cic5r.py` — regressão de R-1, R-2, R-3, R-4,
  R-5, S-2 e S-3, com controles positivos (caminho legítimo continua fechando) e negativos (hash de
  outra build continua divergindo; isca que passa continua vermelha).
* **+6 iscas** (todas reprovam — vistas passando contra o código com o defeito plantado):
  `cp_aut4f_isca_cli_sem_perfil_estoura`, `cp_aut4f_isca_espera_queima_teto`,
  `cp_aut4f_isca_encerrar_por_imagem_mata_todas`, `cp_aut4f_isca_contraprova_aceita_excecao`,
  `cp_aut4f_isca_alvos_2o_cenario_ignorado`, `cp_aut4f_isca_campo_extra_ausente_ok`.
* **+2 iscas corrigidas** (R-5): as duas que reprovavam por exceção agora reprovam por assert.
* `docs/automacao/AUT-4-estado.json`: `driver_sha256`/`runner_sha256` atualizados, listas de
  testes/iscas iguais às do disco (10 testes / 22 iscas), contagens e seção
  `achados_cic5r_corrigidos_aut4f`. `AUT-4-preparacao.md` cita os números reais (10/10, 22 iscas).

---

## 6. sha256 do que foi tocado

```
68866a7ce101044b314587a32199d8709f87f97b6749fa1d86dc0978605a1595  tools/automacao/runtime/coletor.py
7906c1692bf349aff006039f73bbc8c59ef4e2a7a588210c348227be4dfb157e  tools/automacao/runtime/roda_testes_runtime.py
96386ddfc087354adf593801ee546106cb83a7a844c23806a34422773e8bd9ab  tools/automacao/runtime/testes/t_aut4_cic5r.py
e72e80f94792ccbb6f5c2effa64341d383cc0185f5cac8d57ed6ddbae51ebc93  tools/automacao/runtime/testes/t_aut4_estado_docs.py
0ca120807161b2bbb0920ecf5e6dae11dd66139d8c1a5dcc5e85caa67fddd4ab  .../testes/contra-prova/cp_aut4_isca_ausente_ok.py
7299e3e4ee1fcbce2dd8e7cc88e2a190c29d45eb3e304d7620e9553d9cf34cdd  .../testes/contra-prova/cp_aut5_isca_topo_sem_hash_ok.py
680d1d2cb413cf6d5ff7fbefa869aac9f740198e09ae156d53d24e4f6ad2ecb7  .../cp_aut4f_isca_alvos_2o_cenario_ignorado.py
a4a8e26b797964397e3c6b58273cd5b06f7eccb47a0fae2881acd6b83d8b1d8f  .../cp_aut4f_isca_campo_extra_ausente_ok.py
0c91db3d04a7fc4bdf095efd9cc485041e65bbabead1317b4ede7b7ea72605b7  .../cp_aut4f_isca_cli_sem_perfil_estoura.py
6b130082a34d1074c49281a15d204a9e041a296abc89ab7cc2e3a45e5d48fcd4  .../cp_aut4f_isca_contraprova_aceita_excecao.py
92e06f3ccbf34ecfe49317565c935f855a9ba02a1d6c82c0a700f5770f04816e  .../cp_aut4f_isca_encerrar_por_imagem_mata_todas.py
539d8b3eefca4f59067b03d393f7c110b2b6681f6dfce7b1638d4df4b9cd5c53  .../cp_aut4f_isca_espera_queima_teto.py
d7d676e8f5ad8dbccdee0353d77707b2e0c71b5628b0211b22820e4e8d86507f  docs/automacao/AUT-4-estado.json
f30959628c804e8b57b9a5c637cdf63b51f44abe67222b63df5b3220ac1f6383  docs/automacao/AUT-4-preparacao.md
6437e5896298581b41ab2045f9e9d42418efe31bc106763615f78b7df770e967  docs/automacao/AUT-4F-evidencias/planta_defeitos_aut4f.py
```

`tools/automacao/runtime/` e `docs/automacao/` seguem **untracked** (`??`) e nada foi para o stage
(`git diff --cached --name-only` vazio). O fonte do probe **não mudou**: `5a51abaa…`.

---

## 7. Lacunas declaradas (NÃO exercitadas — e não viram OK)

* **Runtime em jogo segue NÃO EXERCITADO**: emissão real dos campos num objeto vivo, PNG pela API do
  `ScreenCapture`, `owners` Harmony vivos, navegação por handler real de UI, ida-e-volta real
  (`DemostrarTooltip=true`), rollback contra o **perfil real** e lançamento por Steam. Nada disso foi
  rodado: a rodada runtime exige **autorização explícita do dono** e uma frente única controlando o
  jogo (probe novo ⇒ instalar + iniciar; sem hot-reload).
* O gate de autorização do probe segue provado **estaticamente** (contrato no fonte) e no contrato do
  driver; em execução, não.
* `encerrar_imagem` (R-4) teve a **decisão** exercitada por função pura; o `taskkill /F /PID` real
  **não** foi disparado (nenhum processo de jogo existe nesta rodada) — e não deve ser disparado numa
  máquina com o jogo do dono aberto.
* `pids_da_imagem` depende do `tasklist` do Windows; onde ele faltar, o encerramento é recusado
  (comportamento projetado e testado na decisão), não exercitado em ambiente sem `tasklist`.
