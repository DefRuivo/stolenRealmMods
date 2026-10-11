# KIT-14G — parte05: rodada de runtime (run712) — navegação avançou 3 telas; run QUEBRA o jogo

Cartão `t_0e656658`, implementador `default/run712`, 10/10/2026. Complementa parte01–04.
Fonte de verdade por máquina: `scratch/kit/KIT-14G-run712/verification.json`.
Bancada: `scratch/kit/KIT-14G-run712/roda.py` + boots `mapa`, `roteiro1`, `roteiro2`,
`roteiro3`, `roteiro3b`, `roteiro4`, `roteiro5`, `roteiro6` (cada um com `result.json`,
`probe/aut4probe.json`, `probe/recorder.json`, `probe/01-ui.png`, `LogOutput-isolado.txt`).

## 1. Defeito de produto corrigido (navegação não saía do menu)

O casador do roteiro era só **substring**: o estágio `Play` casava também o banner
**`PLAY NOW!`** e o clique caía no anúncio — a tela **não mudava** (medido no boot `mapa`,
parte04 §2.4). Correção em `AUT4ProbePlugin.cs::TentarNavegar`:

- **IGUALDADE (case-insensitive) primeiro**; **substring só como FALLBACK** (rótulos
  compostos, ex. `Skills Tree Btn`) e o alvo por NOME continua valendo para o botão sem
  rótulo do RSTV.

Rebuild com `-p:DeployToBepInEx=false`, **0 erro**:

| artefato | sha256 |
|---|---|
| `AUT4ProbePlugin.cs` (fonte) | `594c8add629476c131635eccf0bd8f6dee4fd469803ad94e622c5b5dcf15bdcb` |
| `AUT4Probe/bin/Release/AUT4Probe.dll` | `1d496dbc14667334efcb3757e6324261426dfaa7a851f948be0b192a90737f6b` (anterior `687b72f1…`) |

Verificação offline da correção (executada):
- `harness-kit14f.exe` (partes 1–4) **PASSOU**: 10 / 5 / 21 / 14 OK, 0 FALHA →
  `scratch/kit/KIT-14G-run712/logs-harness-kit14f.log`;
- `roda_testes_runtime.py` **VERDE 16/16** → `logs-suite-runtime.log`;
- `--contra-prova` **VERDE 33/33** → `logs-contra-prova.log`;
- docs de identidade sincronizados: `AUT-4-estado.json`, `AUT-4-preparacao.md`,
  `AUT-4-runbook-rodada-autorizada.md` (senão as travas `t_aut4_estado_docs`/`t_aut4_runbook` reprovam).

## 2. Navegação REAL até a criação de personagem (itens 2 e 3)

Cada boot parte de **dados isolados vazios**, Cloud do app `1330000` **OFF**
(`require_cloud_off` e `production_diff().equal` conferidos antes de cada boot), perfil
BepInEx temporário (o perfil do dono **não** recebeu nada).

**Mapa real dos botões (`botoes_vistos`), acumulado por boot:**

- menu inicial: `Play`, `Online`, `Options`, `Backers`, `Exit Game` + banners
  `PLAY NOW!`, `WISHLIST NOW!`, `WISHLIST ON STEAM!`, `OUT NOW ON STEAM!`,
  `Discord Btn (1)`, `Email`, `Version Text`;
- após `Play` → `Campaign`, `Roguelike`, `Back`;
- após `Roguelike` → tela `CreatingCharacter` (`CurrentGuiState`): `Accept`, `Next`,
  `Change Skills`, `Minus`, `Plus`, `Button Right`, `Button Left`, `Unlock …` e os
  atributos `8`,`10`,`11`,`12`,`13`,`14`,`16`;
- após `Accept` → o jogo cria `Character0.json` (`TimeAcquiredString 10/10/2026 19:19:51`).

Ou seja, **a correção de casamento destravou a navegação**: os boots `roteiro1` e
`roteiro2` percorreram, por handler, `Play → Roguelike → CreatingCharacter`
(`rota_estagios_clicados` 1 e 3; `CurrentGuiState` `InMainMenu` → `CreatingCharacter`).
O PNG `01-ui.png` de cada boot **conferido por visão** casa com o mapa.

**Recoleta pós-navegação (item 3) — OK no mecanismo**: em cada boot que finalizou,
`recoleta.apos_navegacao = true` e `recoleta.frame` é o **mesmo quadro** do pedido do PNG
(`eventos_frame`: ex. roteiro2 leitura/pedido `1307`; run710 tinha leitura 157 × PNG 1352).
Os objetos lidos passam a ser do estado navegado, não do loading.

## 3. BLOQUEIO MEDIDO: entrar na RUN derruba o jogo

Ao clicar `Accept` (início da run roguelike), o jogo **cria o personagem e então
EN CERRA/crasha** ~9 s depois, em ambiente isolado de dados vazios:

- medido por log externo de processos (`scratch/kit/KIT-14G-run712/proc_log.txt`):
  o `Stolen Realm.exe` lançado desaparece ~30 s após o launch, na mesma janela em que um
  processo irmão de vida curta aparece e some;
- `Player.log` isolado termina **sem erro** após o load da cena; `backtrace` **vazio**;
- o crash **não é causado por clique indevido do probe**: no boot `roteiro6` a rota ficou
  **não esgotada** (`Play;Roguelike;Accept;__nunca_casa__`), então o probe **não clica mais
  nada** no HUD — e o jogo **mesmo assim** crashou;
- reproduzido em `roteiro5` e `roteiro6` (e nos boots 3/3b/4 o guard de processo irmão
  abortou no mesmo instante). Sobrevivem só os boots que **não** entram na run.

Consequência: a **tela do HUD da run** (onde vive o botão do RSTV) é **inalcançável** nesta
configuração: o jogo morre ao entrar na run com **dados isolados vazios**. Não é o botão do
RSTV ausente (o RSTV nem foi instalado) — é o próprio jogo encerrando o processo.

**Item 2 fica NAO_EXERCITADO** (alvo RSTV não alcançado); o que **ficou provado** é a rota
`Play → Roguelike → CreatingCharacter` por handler, com mapa real das telas.

## 4. Recorder (item 1) — consumidor provado; trilha VAZIA; trilha da run perdida no crash

`probe/recorder.json` é **gravado dentro do processo** (o run710 levava a trilha embora no
rollback). Nos boots que finalizaram (`mapa`, `roteiro1`, `roteiro2`):

- `identidade.hash_dll_do_core = hash_fonte_declarado = 84d911a8…` (**conferem**);
- `passivo.runtime = "NAO_EXERCITADO"`, `eventos: []`, `eventos_total = 0`,
  `capturas_solicitadas = 0`.

Isto é **leitura medida** (a contagem real do recorder), **não 0 inventado**. Porém:
os boots que **entraram na run** — os únicos que gerariam interação observável — **crasharam
antes de `LerRecorder()`**, então a trilha passiva que existia **na memória do processo foi
perdida junto com o crash** (o Core não escreve arquivo próprio; só expõe `ResultadoFinal()`).

**Item 1 fica NAO_EXERCITADO** quanto a `eventos_contados > 0`: o consumidor e a prova de
identidade funcionam; a contagem > 0 depende de uma run que não crasha.

## 5. Ambiente ao fim (nada do dono tocado)

- diretório de dados do dono restaurado **byte a byte** (`kit16-save-isolado.sh restaurar`:
  "identico ao snapshot antes"); `production_diff().equal = True` (111/111);
- **sem junction**; `front-unica.sh release` liberado; **0** processos `Stolen Realm`;
- perfil do dono **sem** `plugins/AUT4Probe`, **sem** `KitPassive`, **sem**
  `com.gumatos.aut4probe.cfg`; Cloud do app `1330000` permanece **OFF** (janela do dono);
- nenhum commit, nenhum deploy, nenhuma publicação.

## 6. NÃO EXERCITADO (declarado, sem número inventado)

HUD da run / botão do RSTV (jogo crasha ao entrar na run com dados vazios — bloqueio medido);
`eventos_contados > 0` do recorder; RSTV instalado no HUD; clique físico / aceite UI-UX (dono);
Runner positivo/negativo; RSTV sem kit; FPS/frame/IO comparáveis com e sem recorder
(o dono dispensou limiares — **nenhum número de performance foi medido ou inventado**);
segundo ambiente.
