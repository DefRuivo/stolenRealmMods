# KIT-14G — parte01: reconhecimento, estado medido e impedimento de runtime

Cartão: t_0e656658. Implementador: default/run711. Data local: 10/10/2026 18:10 -03:00.
Escopo lido: `docs/automacao/KIT-14-runbook-residual-run710.md`, `KIT-14-entrega-run710.md`,
`scratch/kit/KIT-14-run710/final/verification.json`. Nada de produto/mod editado; nenhum
commit/push/publicação.

## 1. Achado bloqueante (medido, não suposto)

O residual pressupõe exercitar RUNTIME (subir o jogo isolado, navegar até a tela onde o
botão do RSTV existe, ler a trilha do recorder). O estado do Steam Cloud MUDOU desde o
run710 e agora IMPEDE esse boot com segurança.

Prova executada: `scratch/kit/KIT-14G-run711/estado-antes.json`
(sha256 `97ea72cb96a026476ce765f6c1fcc67bc5b6dbaedc42c12cbc419a93764cdc86`), produzido por
`scratch/kit/KIT-14G-run711/medir_estado.py` (somente leitura, grava arquivo NOVO em modo `x`).

| campo | run710 (17:59) | run711 (18:10) |
|---|---|---|
| `sharedconfig.vdf` bloco `1330000` → `cloudenabled` | `["0"]` (off) | **`["1"]` (ON)** |
| `configuration_off` | true | **false** |
| `1330000/remotecache.vdf` mtime | 17:54:13 | 18:08:46 |
| arquivos do dono declarados no remotecache | — | **21** (`Character0..Character16`, `GlobalSaveData.json`, `ItemStash.json`, `QuestSaveReport…`, `TransmogList.json`), `syncstate=1` |

Leitura: o diretório de dados do jogo
(`%USERPROFILE%\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm`) **é objeto de
Steam Cloud hoje**, e os 21 arquivos são exatamente os saves do dono. A mesma medição
confirma o resto intacto: 111/111 arquivos iguais à baseline KIT-16, caminho real **sem**
junction, jogo fechado (0 processos).

Por que isso bloqueia (e não é preciosismo):

1. o guard do próprio harness recusa o boot — `require_cloud_off()`
   (`scratch/kit/KIT-14-run704/suporte.py:69`) levanta `RuntimeError('Cloud app config is
   not explicitly off')`; o boot do run710 só andou porque estava off;
2. o isolamento do KIT-16 (`scratch/kit/kit16-save-isolado.sh`) troca o diretório de dados
   por um **junction** para uma cópia descartável. Com Cloud ligado, o Steam pode
   **importar os saves do dono para dentro da área isolada** (a premissa de "dados vazios"
   cai e o dono é carregado — proibido pelo aceite) e, na saída, **enviar de volta** o que a
   rodada deixou no lugar do save real;
3. editar o VDF para desligar o Cloud, ou clicar na UI do Steam, é input de sistema / mexer
   no config do dono — ambos proibidos no aceite e já recusados no run710
   ("nenhuma edição VDF/input alternativo");
4. `computer_use` está indisponível sem supervisão: não há como o agente desligar o toggle.

Consequência honesta: **nenhum boot de runtime foi feito nesta rodada.** Os itens 1–3 do
escopo que dependem de jogo vivo ficam preparados e verificados OFFLINE, mas declarados
NÃO_EXERCITADO no runtime. O item 4 (Runner/mod sem kit/medições) fica NÃO_EXERCITADO por
depender dos itens 1–3.

## 2. O que o escopo pede, mapeado no código real

Leitura do instrumento e do produto (não presumido):

- **Recorder** = "trilha passiva" do KIT-04. Ninguém a lê em processo hoje:
  `KIT04Adapter.SR/SRAdapterPlugin.cs:224 AlimentarPassivo()` grava eventos no Core
  (`core.RegistrarEvento("passivo_" + tipo, …)`) e o resultado consolidado vive em
  `core/CorePlugin.cs:152 ResultadoFinal()` (`eventos`, `eventos_descartados`, `passivo`).
  Faltava o **consumidor**: nada no boot chama `ResultadoFinal()`/`ObterEventos()`.
  Também é opt-in duplo: `Modo/habilitado=true` (Core) **e** `Modo/habilitado=true` +
  `Modo/passivoHabilitado=true` (Adapter) — o harness do run710 subia o Adapter ligado mas
  a trilha passiva desligada, então o recorder não podia ter evento nenhum.
- **Botão alvo**: não é um botão com rótulo "Skills" no menu. A busca do probe
  (`AUT4Probe/AUT4ProbePlugin.cs:956 TentarNavegar`) procura `Button` ativo com rótulo
  contendo `Skills`; o botão do RSTV chama-se `RstvRunSkillTreeButton`
  (`RoguelikeSkillTreeVisualizer/RunButton.cs:64`) e **não tem rótulo** (o glifo substitui o
  texto, `AparenciaDoClone` desliga o TMP). Ele vive na barra de baixo do HUD (run), que o
  jogo só liga em `InTown/InWorldMap/InCutscene/InBattle` (`GUIManager.Update`), e o clique
  exige `Root.PlayingRoguelike` (`RunTargets.GateOk`). Ou seja: **para o alvo existir, o
  roteiro precisa atravessar menu → Play → criação → seleção → run**, exatamente o que
  falta; e o critério de busca do probe (rótulo) nunca casaria com esse botão — precisa
  aceitar o NOME do objeto e/ou o contexto de HUD.
- **Recoleta pós-navegação**: hoje `ColetarObservacoes()` roda uma vez em `PassoLeitura`
  (`_res["observacoes"]`), e a navegação vem DEPOIS; o print `01-ui` sai já na fase de
  navegação (`PassoNavegacao`). É a origem do descasamento frame157 × PNG1352–1356 relatado.

## 3. Plano executado nesta rodada (sem runtime)

1. instrumento: rota de navegação por ESTÁGIOS dirigida por cfg (rótulos vindos do `.cfg`,
   não do código), incluindo casar por NOME de objeto do alvo RSTV e registrar todos os
   botões ativos de cada quadro (para o roteiro ser ajustável sem recompilar);
2. instrumento: **consumidor do recorder** — ler por reflexão
   `KIT04Core.CorePlugin.ResultadoFinal()` no fim da rodada e gravar arquivo novo
   (`recorder.json`) com contagem de eventos, depositando antes do rollback;
3. instrumento: **recoleta depois da navegação** e print do MESMO instante da leitura;
4. verificação OFFLINE (teste executado) + build isolado com hash novo;
5. handoff com o que ficou NÃO_EXERCITADO e o pedido humano (Cloud).

## 4. NÃO_EXERCITADO (declaração explícita)

- boot de runtime do jogo, navegação real, botão do RSTV, PNG de tela, trilha do recorder
  em processo: NÃO_EXERCITADO (Cloud ON — item 1);
- Runner ativo positivo/negativo, RSTV sem kit, FPS/frame/I-O comparáveis: NÃO_EXERCITADO;
- nenhuma medição de performance foi inventada.
