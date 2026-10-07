# AUT-4 — RUNBOOK da rodada autorizada (coleta runtime por objetos Unity)

> **Tarefa:** `t_ef6e8a29` (filha da AUT-4 / `t_b8b9822e`). Consolida, em UM lugar, a
> prova offline já revisada e o procedimento da rodada **em jogo** — que só acontece
> **quando o dono autorizar**.
>
> **Status deste runbook: `PREPARADO_NAO_EXERCITADO`.** Nada aqui abre/encerra o jogo,
> instala o probe, carrega save ou publica. A rodada runtime está **NÃO EXERCITADA** —
> e assim está declarado em todo artefato desta frente.
>
> **AUTOMAÇÃO NÃO SUBSTITUI ACEITE HUMANO NEM A PUBLICAÇÃO DO DoD.** O que este pacote
> entrega é preparação verificável e um procedimento com critérios de aceite. Quem
> aceita a rodada e quem publica o DoD é o dono/operador humano — nenhum veredito
> automático (nem `CONFIRMADA`) publica, instala ou promove nada.
>
> Documentos irmãos (não duplicados aqui): `AUT-4-preparacao.md` (o que foi construído,
> achado por achado), `AUT-4-contrato-restauracao.md` (rollback exato),
> `AUT-4-estado.json` (estado legível por máquina), `AUT-4R3-revisao.md` (revisão
> independente da preparação offline).

---

## 0. Regras invioláveis (valem para TODA a rodada)

1. **Não editar** `lib/Assembly-CSharp.dll`, nada de Bard, nem gameplay. Modificar
   comportamento de jogo não é objetivo desta frente.
2. **Não enfraquecer travas**: gate de autorização, prova de execução, veredito
   negativo, rollback fail-closed e frente única são requisitos — não conveniências.
3. **Build sempre** com `-p:DeployToBepInEx=false` (e, por padrão, sem nenhuma flag de
   deploy). Compilar **nunca** escreve no perfil.
4. Sem autorização explícita: **não instalar, não iniciar, não encerrar** o jogo, **não
   carregar save**, **não publicar**.
5. **Uma única frente controla o jogo.** Declarar outra frente **derruba** a rodada
   (`--frente-ativa` ⇒ `NAO_EXERCITADO`).
6. `AUSENTE` / `NAO_EXERCITADO` / `INDETERMINADO` **nunca são OK**. Não há "verde por
   omissão".
7. **Nunca** fabricar evidência: sem leitura do objeto vivo, o resultado é incompleto —
   jamais um dado sintético. `dados_sinteticos` é **sempre** `False` e `hot_reload`
   **sempre** `False`.
8. O probe é **instrumento temporário**: não vira dependência de nenhum mod e não fica
   instalado no perfil do dono depois da rodada.

---

## 1. Gates de autorização (todos exigidos; faltando um, a rodada NÃO age)

| # | Gate | Como se prova | O que acontece se faltar |
|---|---|---|---|
| G1 | **Autorização explícita do dono** para ESTA rodada | `--autorizado` (default é desautorizado) | `NAO_EXERCITADO` / exit 2, zero observação |
| G2 | **Acesso ao jogo agora** | `--jogo-disponivel` | `NAO_EXERCITADO` / exit 2 (`modo=autorizado-sem-jogo`) |
| G3 | **Confirmação literal da rodada** | `--confirmar-coleta coleta` (valor exato) | `NAO_EXERCITADO` / exit 2 |
| G4 | **Frente única** | **não** passar `--frente-ativa` | `NAO_EXERCITADO` / exit 2 (`modo=frente-duplicada`) — o lançador nem roda |
| G5 | **Perfil isolado no controle negativo** | raiz isolada explícita, fora do perfil do dono | `exigir_perfil_isolado` **RECUSA** (fail-closed) — a DLL do dono não é movida |
| G6 | **Jogo aberto sem o probe carregado** | `--jogo-aberto` sem `--probe-carregado` | declara **REINÍCIO NECESSÁRIO** / exit 2 — **sem hot-reload** |
| G7 | **Hash da build conferido antes de instalar** | sha256 do fonte e da DLL (§2) | rodada sem identidade: não começa |
| G8 | **Somente leitura** na janela de coleta | plano sem `navegar` (ou navegação autorizada) e sem save/combate | fora do escopo autorizado — **não fazer** |

Os gates G1–G4 e G6 são exercitados pelo CLI offline (resultados reais em §6.2). O G5 é
fail-closed por construção e testado (`t_aut4_controle_isolado.py`). G7 é a trava de
identidade (§2). G8 é regra de operação.

---

## 2. Identidade da build (hashes **frozen** — conferir antes de instalar)

| artefato | caminho | sha256 |
|---|---|---|
| fonte do probe | `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `48afd3c41cf3ba97c93e5fc2d6b02ca58298939bf4b2a51f0ccd159ec96e3e94` |
| componentes do probe | `tools/automacao/runtime/AUT4Probe/LeituraAgregados.cs` | `2506ec6478dd5a6bd445f2726c6595015f877f5e6465201d10c12a439c36cab0` |
| componentes do probe | `tools/automacao/runtime/AUT4Probe/IdentidadeDoProbe.cs` | `c23574f324f7a70ddeb2edb484daf292ebd92fc07eb0304bfbf343e58d27bfa6` |
| serializador | `tools/automacao/runtime/AUT4Probe/Json.cs` | `ae30a1ac059bcf62067047926c13bf43079b30552073540a2f5654551b6b32c6` |
| projeto | `tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj` | `347770d091a6a173cbebb988fb30d2a7a73df4d64e316033812e4220869057f4` |
| **DLL do probe** | `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` | `407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7` |
| driver/coletor | `tools/automacao/runtime/coletor.py` | `adb48dca024120db91b65e28b8842b7f303ca1725359cdaf4deab5530ae1dd46` |
| controle negativo | `tools/automacao/runtime/controle_negativo.py` | `053c0026f97c8541294c81e9d0011df4f3d970756f6ab8bc1d96a98fa9296659` |
| runner offline | `tools/automacao/runtime/roda_testes_runtime.py` | `7906c1692bf349aff006039f73bbc8c59ef4e2a7a588210c348227be4dfb157e` |

**Regras de identidade (não negociáveis):**

- **Identidade do artefato = hash DECLARADO**, nunca "compila igual". A DLL do probe
  **não é reproduzível byte a byte** (build sem `-p:PathMap`): um rebuild do **mesmo
  fonte** gera **outro** hash. O hash acima é o da DLL que está em disco hoje.
- A rodada runtime **rebuilda da fonte** e **confere** o sha256 **antes** de instalar.
  O sha256 da DLL conferida vira o `HashFonte` do `.cfg` — é ele que liga cada
  observação à build medida.
- A evidência de runtime só vale se carregar esse `HashFonte` **e** a `Sessao` da
  rodada (ver §3.3 e §5.3).
- `lib/Assembly-CSharp.dll` (a DLL do JOGO) é intocada:
  sha256 `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`.

Conferência:

```bash
sha256sum tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs \
          tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll \
          tools/automacao/runtime/coletor.py
```

O teste `t_aut4_runbook.py` (suite offline) **trava este runbook contra o disco**: os
hashes acima têm de casar byte a byte com os arquivos, e as contagens citadas (§6.1)
têm de ser as reais.

---

## 3. Configuração da rodada

### 3.1 Plano de coleta (`--plano`, esquema `AUT-4/1`)

Obrigatório: `esquema = "AUT-4/1"`, bloco `autorizacao.coleta_autorizada` (bool),
`cenarios` (lista não vazia). Cada cenário exige `nome` e `alvos` (lista não vazia), e
pode declarar `campos_alvo`, `esperado`, `navegar`, `demostrar_tooltip`.

- **`alvos`** = objetos/campos a LER (ex.: `Tooltip.Title`, `Tooltip.Description`,
  `TMP_Text@ativo`).
- **`campos_alvo`** = **governa o veredito**. Alvo fora do schema semântico é
  `PLANO_INVALIDO` (typo não é critério). Campo-alvo em `AUSENTE`/`NAO_APLICAVEL` vira
  **lacuna** ⇒ `INCOMPLETO` — o fallback de objeto inativo é **informação, nunca
  satisfação do critério**.
- **`esperado`** = a expectativa declarada; é contra ela que o detector diz `NO`.

Campos que o coletor sabe medir (schema de `campos_alvo`): `objeto`, `caminho`,
`ativo_na_hierarquia`, `texto_bruto`, `texto_renderizado`, `fonte`, `material`,
`shader`, `keywords`, `cores`, `geometria`, `owners`, `personagem` — mais os extras que
o probe real emite: `componente`, `visivel_na_tela`, `shader_suportado`,
`tamanho_fonte`, `nota_texto_renderizado`.

Fixture de partida (rotulada, **nunca** evidência):
`tools/automacao/runtime/fixtures/plano-exemplo.entrada.json`.

### 3.2 `.cfg` derivado do probe (`coletor.derivar_config` → `escrever_cfg`)

O driver escreve o `.cfg` — **ninguém** o escreve à mão. Chaves (formato BepInEx,
`Chave = valor` sob `[Geral]`):

| chave | papel | default |
|---|---|---|
| `Autorizado` | liga a leitura; **deriva** da autorização da rodada | `false` |
| `OutDir` | pasta de saída (JSON/PNG) | — |
| `OrcamentoSegundos` | teto de tempo da rodada | `120` |
| `Navegar` | navegação por handler real (só quando autorizado) | `false` |
| `PerfilDir` | perfil usado (isolado quando aplicável) | `""` |
| `HashFonte` | sha256 da build medida (liga a evidência à DLL) | sha da DLL instalada |
| `MaxTextos` | teto de `TMP_Text` lidos por rodada | `400` |
| `Sessao` | identidade DESTA rodada (gerada pelo driver) | — |
| `DemostrarTooltip` | porta **OPT-IN** de ida-e-volta | `false` |
| `MarcadorIdaEVolta` | marcador injetado e relido na ida-e-volta | `""` |

### 3.3 Caminhos vigiados / rollback

Contrato: `BepInEx/plugins/AUT4Probe/AUT4Probe.dll`,
`BepInEx/config/com.gumatos.aut4probe.cfg`, `BepInEx/LogOutput.log` — **mais** a
varredura das árvores inteiras `BepInEx/plugins` e `BepInEx/config` (o BepInEx varre
`plugins/` **recursivamente**: arquivo que nasce ali vira mod carregado). Detalhes em
`AUT-4-contrato-restauracao.md`.

### 3.4 Comandos (CLI do coletor)

```bash
RT=tools/automacao/runtime
P=tools/automacao/runtime/fixtures/plano-exemplo.entrada.json   # trocar pelo plano da rodada

# (a) default OFFLINE — não age
python $RT/coletor.py --plano $P

# (b) julgar um JSON de probe já existente (detector)
python $RT/coletor.py --plano $P --detectar --saida-probe <aut4probe.json>

# (c) jogo JÁ ABERTO — só LE instrumentação já carregada
python $RT/coletor.py --plano $P --jogo-aberto [--probe-carregado]

# (d) RODADA executável (gated) — só na rodada AUTORIZADA
python $RT/coletor.py --plano $P --executar \
    --autorizado --jogo-disponivel --confirmar-coleta coleta \
    --perfil <perfil-ISOLADO> --out-dir <out_dir> \
    --dll-probe $RT/AUT4Probe/bin/Release/AUT4Probe.dll --timeout 180

# (e) controle negativo ISOLADO (offline, stub; nunca o lançador real)
python $RT/controle_negativo.py --plano $P --base <raiz-ISOLADA> \
    --dll-probe $RT/AUT4Probe/bin/Release/AUT4Probe.dll [--autorizado --stub python <stub.py>]
```

`--encerrar-imagem` só existe para rodada **real** (contra stub ele é recusado).

---

## 4. Cenários da rodada e o que cada um prova

Todos abaixo estão **NÃO EXERCITADOS** hoje (nenhum rodou em jogo). A coluna
"fecha / reprova" diz qual veredito é aceitável.

| id | cenário | leitura / alvo | observado (a registrar) | esperado | fecha / reprova |
|---|---|---|---|---|---|
| C0 | **Controle negativo isolado** (offline, já exercitável) | stub que não escreve leitura | `NAO_EXERCITADO`, zero observação | detector NÃO confirma | fecha: `NAO_EXERCITADO`; `CONFIRMADA` = DEFEITO |
| C1 | **Leitura de objeto vivo** | `Tooltip.Title`/`Description`, `TMP_Text@ativo` | texto cru **e** renderizado, ativo, fonte/material/shader/keywords, cores, geometria | campo lido não-vazio e coerente com o objeto | fecha: `CONFIRMADA`; alvo não lido ⇒ `INCOMPLETO` |
| C2 | **PNG pela API do Unity** | `ScreenCapture.CaptureScreenshot` | arquivo existente com `bytes > 0` e **posterior ao lançamento** | print válido | fecha: `prints_ok`; print ausente/velho ⇒ `INDETERMINADO` |
| C3 | **Owners Harmony vivos** | `owners` no JSON | owners atribuídos aos objetos lidos | owner coerente com o mod instrumentado | fecha: `owners` presentes |
| C4 | **Navegação por handler real** | `Navegar=true` | handler real de UI acionado; OCR/coordenada só fallback **declarado** | navegação sem OCR como prova primária | fora do escopo se não autorizado |
| C5 | **Ida-e-volta** | `DemostrarTooltip=true` + `MarcadorIdaEVolta` | `ida_e_volta {marcador, titulo_lido, titulo_renderizado_lido, conferiu}` | `conferiu == true` com o marcador do driver | reprova: `INDETERMINADO` sem a prova |
| C6 | **Rollback exato** | manifest + `restauracao` | criados/modificados/removidos; diretório pré-existente **preservado** | perfil idêntico ao de antes (`limpo: true`) | reprova: `RESIDUO` / exit ≠ 0 |
| C7 | **Encerramento** | gracioso (`CloseMainWindow`) → forçado por PID só como fallback | ordem executada e registrada | jogo fechado sem `taskkill /IM` cego | sem medição dos PIDs, RECUSA |

---

## 5. Passo a passo da rodada (quando autorizada)

### Fase A — antes de pedir autorização (offline, repetível)
1. `python tools/automacao/runtime/roda_testes_runtime.py` → **VERDE, 15/15, exit 0**.
2. `python tools/automacao/runtime/roda_testes_runtime.py --contra-prova` → **VERDE,
   31 iscas reprovam como deviam, exit 0**.
3. Conferir hashes (§2) e `docs/automacao/AUT-4-estado.json` contra o disco.

### Fase B — pré-voo (depois do "sim" do dono, jogo **fechado**)
1. **Fechar o jogo** (gracioso) e confirmar que não há `Stolen Realm.exe` (§9.1).
2. Criar a **raiz isolada** da rodada e o `out_dir` (nunca dentro do perfil do dono).
3. Instalar o probe **na raiz isolada** com o sha256 conferido (§2).
4. Arquivar/remover o `LogOutput.log` do perfil alvo (um boot **trunca** o log; o boot
   desta rodada tem de ser o único log lido).
5. Confirmar **uma única frente** controlando o jogo.

### Fase C — rodada
1. Executar o comando (d) de §3.4.
2. O driver: instala → escreve o `.cfg` (com `Sessao` + `HashFonte`) → lança pelos
   argumentos de doorstop → **espera ESTADO** (chainloader + JSON do probe, com teto) →
   lê → consolida → **rollback exato** no `finally`.
3. **Não** prometer nem esperar hot-reload: probe novo ⇒ instalar + iniciar.

### Fase D — pós-rodada
1. Consumir `manifest` + `rollback` + `restauracao` (§4/C6). Resíduo ⇒ **perfil sujo**:
   não se apresenta como limpo; restaurar do backup.
2. Julgar a leitura com `--detectar` (§3.4-b) — vocabulário fechado
   `CONFIRMADA | NO | AUSENTE | NAO_EXERCITADO | INCOMPLETO`.
3. Registrar observado × esperado por cenário (§4) e as **lacunas**.
4. Submeter ao **aceite humano** (§7). Automatismo nenhum publica.

---

## 6. Evidências (o que coletar, onde, o que cada uma prova)

### 6.1 Resultados offline JÁ OBTIDOS (reproduzíveis; não são prova de runtime)

| o que | comando | resultado real observado |
|---|---|---|
| suite offline | `python tools/automacao/runtime/roda_testes_runtime.py` | **VERDE (exit 0)** — 15/15 |
| contra-prova | `... --contra-prova` | **VERDE (exit 0)** — 31 iscas, todas por `RESULTADO\|REPROVOU\|`, zero por exceção |
| controle negativo isolado (sem autorização) | `controle_negativo.py --plano … --base <iso> --dll-probe …` | **`NAO_EXERCITADO` / exit 2**, zero observação, `dados_sinteticos=false` |
| controle negativo isolado (com stub que não lê) | `... --autorizado --stub python <stub.py>` | **`NAO_EXERCITADO` / exit 2**, rollback exato (`restauracao.limpo=true`), DLL e `.cfg` removidos da área isolada |

Contagem de referência no disco: **15 testes** (`testes/t_*.py`) e **31 iscas**
(`testes/contra-prova/cp_*.py`). O `t_aut4_estado_docs.py` trava essa contagem.

**Ambiente de execução da suite (importa):** a suite é **hermética** quando o
`APPDATA`/`USERPROFILE`/`LOCALAPPDATA` são redirecionados para uma pasta de trabalho
(como nas revisões independentes) — é assim que ela é reproduzível. Com o ambiente
**real** e o **jogo aberto**, `t_aut4_controle_isolado.py` REPROVA: a checagem de
integridade do perfil do dono (impressão `bytes:mtime_ns`) vê o `LogOutput.log` do dono
crescendo sozinho, por causa do jogo vivo — **causa externa**, não efeito da rodada
(ver §9.1). O resultado é o mesmo comando em dois ambientes: verde no hermético,
vermelho-explicado com o jogo aberto.

### 6.2 Contratos de autorização exercitados via CLI (saída real, offline)

| comando | observado | exit |
|---|---|---|
| `--plano P` (default) | `NAO_EXERCITADO`, `modo=offline`, `dados_sinteticos=false` | 2 |
| `--plano P --autorizado` | `NAO_EXERCITADO`, `modo=autorizado-sem-jogo` | 2 |
| `--plano P --autorizado --jogo-disponivel --confirmar-coleta coleta` | `AUTORIZADO`, `pode_coletar=true`, plano de 6 passos + manifest previsto | 0 |
| `--plano P --jogo-aberto` | `NAO_EXERCITADO` — "o probe NAO esta carregado … exigiria REINICIAR (nao ha hot-reload)" | 2 |
| `--plano P --jogo-aberto --probe-carregado` | `PRONTO_PARA_LER` (somente leitura) | 0 |
| `--plano P … --frente-ativa` | `NAO_EXERCITADO`, `modo=frente-duplicada` | 2 |
| `--plano P --detectar --saida-probe <fixture>` | `INCOMPLETO` — "ha lacuna: alvo(s) nao lido(s) `texto_renderizado`" | 1 |

### 6.3 Evidência da rodada em jogo (a coletar na Fase C)

Em `<out_dir>`: `aut4probe.json` (leitura), PNG(s), `log-anterior.log` (backup com
bytes/sha256), `rollback-backup/**`, `lancamento.txt` (argv + pid + sessão),
`cfg-instalado.cfg`, o JSON de resultado do driver (manifest + rollback + restauração).

Uma evidência de runtime só é **válida** se: procedência `runtime`; `evidencia_runtime`
ausente ou `True` (qualquer outra forma PRESENTE ⇒ `FIXTURE`/exit 2); `Sessao` **desta**
rodada; JSON **mais novo** que o lançamento; `LogOutput.log` com o fim do chainloader
**e** a linha de vida do probe; `prints` não vazio com `bytes > 0` **posteriores** ao
lançamento. Falta de sessão ⇒ `NAO_EXERCITADO`/exit 2; falta de log/print ⇒
`INDETERMINADO`/exit 1.

---

## 7. Critérios de aceite da rodada (checklist do aceite HUMANO)

| # | critério | observado×esperado | prova | reprova quando |
|---|---|---|---|---|
| AC1 | **Autorização e frente única respeitadas** | gates G1–G4 verdes | decisão do driver no JSON | qualquer gate ausente e a rodada agiu |
| AC2 | **Identidade da build** | sha256 da DLL = declarado; `HashFonte` no `.cfg` e no JSON | §2 | hash divergente |
| AC3 | **Leitura ida-e-volta** | campo lido no objeto vivo **e** `ida_e_volta.conferiu == true` | `aut4probe.json` | `INDETERMINADO` / sem marcador |
| AC4 | **PNG pela API do Unity** | arquivo existe, `bytes > 0`, posterior ao lançamento | manifest | print ausente/velho |
| AC5 | **Owners Harmony vivos** | owners atribuídos | JSON | owners vazios |
| AC6 | **Detector sabe dizer NÃO** | leitura negando a expectativa ⇒ `NO`; sem leitura ⇒ `AUSENTE` | `--detectar` | `CONFIRMADA` sem leitura válida |
| AC7 | **Rollback exato** | `restauracao.limpo == true`; diretório pré-existente preservado | `restauracao`/manifest | `RESIDUO`/divergência |
| AC8 | **Encerramento em 2 etapas** | gracioso → forçado por PID | registro do encerramento | `taskkill` cego / sem medição |
| AC9 | **Nada fabricado** | `dados_sinteticos == false`, `hot_reload == false` em todo retorno | JSON | qualquer dado sintético |
| AC10 | **Aceite humano e DoD** | revisão humana da evidência; publicação **separada** | este runbook + revisão | automação publicando/promovendo por conta própria |

Regra de leitura do aceite: **`AUSENTE` / `NAO_EXERCITADO` / `INDETERMINADO` nunca são
OK**; `INCOMPLETO` e `NO` são resultados **legítimos** (o detector funcionou), mas não
são `CONFIRMADA`. Automatismo não substitui aceite humano nem publicação do DoD.

---

## 8. Lacunas conhecidas (declaradas; **não** são OK)

- Leitura real do objeto vivo: **NÃO EXERCITADA**.
- PNG pela API do Unity em jogo: **NÃO EXERCITADO**.
- Owners Harmony em sessão viva: **NÃO EXERCITADO**.
- Navegação por handler real de UI: **NÃO EXERCITADA**.
- Rollback **executado em jogo** (o plano e a execução contra stub estão testados):
  **NÃO EXERCITADO**.
- Ida-e-volta em jogo (`DemostrarTooltip=true` em rodada autorizada): **NÃO
  EXERCITADA** — o instrumento existe e o driver o **exige**, mas nunca rodou em sessão
  viva.
- Gate de autorização do probe: testado **estaticamente** (contrato do fonte) — não em
  execução.
- Lane `--detectar`: lê artefato **já existente** e **não** passa `provas` (sem
  `provas.ok` e sem atualidade de sessão). Garante o **status de conclusão**
  obrigatório. Quem precisa da prova de execução usa `--executar`.
- DLL do probe **não reproduzível byte a byte**: a identidade é o **hash declarado**.
- Não há verificação **em jogo** do encerramento (`CloseMainWindow` → `taskkill /F
  /PID`): o que está provado é a **ordem** e a execução com **executor injetado**.

---

## 9. Falhas conhecidas e o que fazer

### 9.1 Jogo ABERTO durante a preparação (visto nesta consolidação)
Se o jogo estiver rodando, o `LogOutput.log` do perfil do dono **cresce sozinho** — e a
checagem de integridade do controle negativo (`perfil_dono_intacto`, por
`bytes:mtime_ns`) **acusa** essa mudança, por um motivo **externo** ao controle. Não é
efeito colateral da rodada, mas invalida a leitura automática daquela checagem.
⇒ O controle negativo isolado (e a rodada) devem rodar com o jogo **fechado** / **uma
única frente**; se rodar com o jogo aberto, **declarar** que a impressão do dono
derivou por escrita do próprio jogo.

### 9.2 Outras falhas
- `RESIDUO` / exit ≠ 0 ⇒ perfil sujo: **não** apresentar como limpo; restaurar do
  backup (`out_dir/rollback-backup/**`).
- `NAO_EXERCITADO` por falta de prova ⇒ reiniciar o jogo (não há hot-reload).
- `status=ERRO` do instrumento ⇒ resultado rebaixado para `ERRO`/`INCOMPLETO`, exit ≠ 0.
- `PLANO_INVALIDO` (alvo fora do schema) ⇒ corrigir o plano, nunca "só ignorar" o alvo.

---

## 10. O que NÃO fazer

- Não fazer commit / push / publicação / promoção a partir desta frente.
- Não editar arquivos de mod, perfil do dono, `KANBAN`, `CAP-1` original nem docs de
  outro ciclo.
- Não mover a DLL do perfil do dono sem autorização explícita.
- Não usar OCR/coordenada como **prova primária** (só fallback **declarado**).
- Não deixar o probe instalado depois da rodada.
- Não declarar "verde" sem a leitura — silêncio não é aprovação.

---

## 11. Rastreabilidade

- Preparação e achados: `docs/automacao/AUT-4-preparacao.md`,
  `docs/automacao/AUT-4-contrato-restauracao.md`,
  `docs/automacao/AUT-4-estado.json`.
- Revisões independentes: `docs/automacao/AUT-4R2-revisao.md`,
  `docs/automacao/AUT-4R3-revisao.md`.
- Instrumento: `tools/automacao/runtime/AUT4Probe/**`, `coletor.py`,
  `controle_negativo.py`.
- Provas offline: `tools/automacao/runtime/testes/t_*.py` e
  `testes/contra-prova/cp_*.py` (runner `roda_testes_runtime.py`).
- Elo deste runbook com o disco: `tools/automacao/runtime/testes/t_aut4_runbook.py`
  (isca: `testes/contra-prova/cp_aut4_isca_runbook_hash_velho.py`).
