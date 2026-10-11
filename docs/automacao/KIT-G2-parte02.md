# KIT-G2 — parte02: inventario/hashes congelados, acoes e cenarios ativos, controle negativo

> Complementa `KIT-G2-parte01.md`. Nao sobrescreve arquivo existente (regra de artefato
> incremental). Numeros aqui sao **medidos no disco** em 2026-10-10 BRT, nao inventados.

## 1. Inventario de artefatos a REUSAR (nao duplicar infraestrutura entregue)

| artefato | caminho | papel |
|---|---|---|
| probe AUT-4 | `tools/automacao/runtime/AUT4Probe/**` | monitor (leitura do objeto vivo + PNG pela API do Unity) |
| driver/coletor | `tools/automacao/runtime/coletor.py` | executor (instala -> cfg -> lanca -> espera estado -> le -> rollback) |
| controle negativo isolado | `tools/automacao/runtime/controle_negativo.py` | baseline/controle (fail-closed, recusa perfil do dono) |
| runner offline | `tools/automacao/runtime/roda_testes_runtime.py` | suite offline + contra-prova (pre-voo) |
| frente unica | `tools/automacao/runtime/controle_acesso.py` | trava de frente unica |
| cenario RSTV | `tools/automacao/cenarios/rstv.py` | avaliador de capacidades RSTV |
| cenario tooltips/shrines | `tools/automacao/cenarios/tooltips_shrines.py` | avaliador de tooltips/atributos |
| pacote instalavel | `tools/automacao/kit15/**` (pacote.py, instalador.py, descoberta.py, scan.py, manifesto.json) | pacote kit-rstv 0.1.0 (KIT-15F) |
| runbook | `docs/automacao/AUT-4-runbook-rodada-autorizada.md` | procedimento da rodada + gates G1–G8 |
| medidor do perfil do dono | `scratch/kit/medir-dono.sh` | baseline do perfil/saves (arvore + LogOutput + saves) |

## 2. Hashes medidos no gate (identidade = HASH DECLARADO, nunca "compila igual")

| artefato | sha256 (medido 2026-10-10) |
|---|---|
| `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` | `72928ffa4a84d79dd9a8fadce9f78bd438d1f991a0c100afb30f7bf7da561a5c` |
| `tools/automacao/runtime/coletor.py` | `159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d` |
| `tools/automacao/cenarios/rstv.py` | `f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7` |
| `tools/automacao/cenarios/tooltips_shrines.py` | `65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199` |
| `lib/Assembly-CSharp.dll` (DLL do JOGO, intocada) | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |

Hashes de fonte/componentes/driver do runbook AUT-4 (conferiveis byte a byte em
`AUT-4-runbook-rodada-autorizada.md` §2) valem como identidade congelada desta rodada:
`AUT4ProbePlugin.cs` `f798c490…`, `LeituraAgregados.cs` `f3985436…`, `IdentidadeDoProbe.cs`
`c23574f3…`, `Json.cs` `ae30a1ac…`, csproj `347770d0…`, `controle_negativo.py` `053c0026…`,
`roda_testes_runtime.py` `7906c169…`.

## 3. Acoes e cenarios ATIVOS pre-registrados (o que a rodada vai fazer)

> Distincao: **ACAO** = o que o operador/executor faz; **CENARIO** = o que se observa.
> Todos abaixo hoje estao **NAO_EXERCITADO** em jogo (nenhum rodou em sessao viva).

### 3.1 Marco RSTV (primeira frente runtime) — KIT-14 entrega
1. Clique **fisico** (input do engine) em um alvo de UI.
2. Janela de resultado aberta (leitura do objeto vivo).
3. Conteudo/tooltip lido (cru + renderizado) + PNG pela API do Unity.
4. Relatorio gerado a partir da observacao.
5. Marcar problema e exportar.

### 3.2 Cenarios do Runner (capacidades RSTV, ids reais do codigo em `rstv.py`)
`RSTV-6-readonly-personagem`, `RSTV-6-readonly-skills-pontos`, `RSTV-21-janela-ciclo`,
`RSTV-21-tooltip-restauracao`, `RSTV-26-placeholders`, `RSTV-25b-dependencia`,
`RSTV-geometria-clipping`; e os criterios de `tooltips_shrines.py` (tooltips/atributos).
Cada cenario exige **esperado independente** e devolve cobertura real x nao exercitado.

### 3.3 Cenarios de coleta AUT-4 (runbook §4) — instrumento/monitor
C0 controle negativo isolado · C1 leitura de objeto vivo · C2 PNG pela API do Unity ·
C3 owners Harmony vivos · C4 navegacao por handler real · C5 ida-e-volta ·
C6 rollback exato · C7 encerramento (gracioso -> forcar por PID).

### 3.4 Demonstracao de erro detectado (KIT-14)
Executar um cenario de **controle negativo do Runner** e provar que o avaliador diz
`NO`/`REPROVADO`/`AUSENTE`/`INCOMPLETO` (o instrumento sabe dizer NAO), nunca verde por omissao.

## 4. Baseline e controle negativo (como o "NAO" e provado)

- **C0 (isolado, offline, exercitavel):** stub que NAO escreve leitura deve dar
  `NAO_EXERCITADO`/exit 2, zero observacao, `dados_sinteticos=false`. `CONFIRMADA` aqui = DEFEITO.
- **Fixtures negativas rotuladas:** `cenarios/rstv-ausente.entrada.json`,
  `rstv-lacunas.entrada.json`, `rstv-controles.entrada.json`,
  `runtime/fixtures/cenarios-negativos.entrada.json` — devem sair negativas
  (nunca confirmar); marcas de fixture forcam `FIXTURE`/nao-runtime.
- **Detector `--detectar`:** leitura que nega a expectativa ⇒ `NO`; sem leitura ⇒ `AUSENTE`;
  status de conclusao ausente ⇒ `INCOMPLETO` ("silencio nao e aprovacao").
- **Baseline do dono:** `scratch/kit/medir-dono.sh` antes/depois — arvore de `core/`,
  `plugins/`, `LogOutput.log` (bytes:mtime_ns) e `SaveGames` devem ser **identicos**
  (perfil/save de producao intactos). Diferenca ⇒ declarar causa (jogo do dono aberto) ou FALHA.
- **Baseline "sem recorder":** medir o mesmo cenario com e sem o recorder para separar
  efeito do instrumento de efeito do jogo.

## 5. Congelamento de artefatos durante a coleta

- Antes de lancar: registrar sha256 dos artefatos do §2 + snapshot do perfil isolado.
- Durante a coleta: nenhuma edicao nos artefatos monitorados; JSON leva `Sessao` desta rodada
  e `HashFonte` (sha da build medida).
- Depois: reconferir os sha256; divergencia ⇒ marcador de integridade quebrado (nao verde).
- Uma unica frente (`controle_acesso.py`); jogo do dono fechado; sem hot-reload presumido.
