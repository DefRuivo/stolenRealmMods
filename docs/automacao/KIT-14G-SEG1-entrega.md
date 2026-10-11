# KIT-14G-SEG1 — o Core não criava o livro de eventos (`eventos: []` com `habilitado = true`)

Cartão: `t_21e89a61` (filho de `t_0e656658` / KIT-14G). Rodada: run719 (`default`).
Escopo: **produto** — `tools/automacao/runtime/core/CorePlugin.cs` (só ele) + evidência.
Nada foi instalado no perfil do dono, nada foi empacotado, o save do dono não foi tocado e
nenhum boot novo do jogo foi aberto nesta rodada (ver §5).

## 1. O defeito, como estava medido

Com `BepInEx/config/com.gumatos.kit04.core.cfg` em `[Modo] habilitado = true`, o Core carrega
(o BepInEx loga `Loading [KIT-04 Core Genérico 0.1.0]`) e `ResultadoFinal()` devolve:

```
"eventos": []   "eventos_descartados": 0
```

…com o bloco `passivo` **preenchido** com o `sessao` da rodada — ou seja `EstaHabilitado()` era
`true` (desabilitado, `ResultadoFinal()` devolveria só `{"status":"NAO_EXERCITADO"}` e `passivo`
seria `null`).

Evidência congelada do run712: `scratch/kit/KIT-14G-run712/{mapa,roteiro1,roteiro2}/probe/recorder.json`
(os três com `"eventos":[]`) e `probe/aut4probe.json` → bloco `recorder` (`status: LIDO`,
`eventos_contados: 0`).

## 2. Dedução fechada: `_eventos` ficou `null` porque o `Update()` nunca tickou

Três fatos, cada um medido em arquivo:

1. `ObterEventos()` é `_eventos?.ObterEventos() ?? new List<>()` e o **único** lugar que cria
   `_eventos` é `RegistrarEvento()`. Na versão medida o **único** chamador de `RegistrarEvento`
   era o **primeiro `Update()` do plugin** — `RegistrarEvento("inicializacao", "Core plugin carregado")`.
2. O `Awake()` **rodou**: `passivo`, `identidade` e `sessao` do recorder só existem porque foram
   construídos ali (config, sessão e `PipelinePassivo`); com `Awake` não executado,
   `EstaHabilitado()` estouraria NRE e o probe gravaria `status: ERRO` — ele gravou `LIDO`.
3. Logo: livro vazio + `Awake` provado + `RegistrarEvento` só no `Update` ⇒ **o `Update()` do
   plugin não executou nenhum tick** em nenhum dos boots em que o Core estava carregado.

## 3. Por que o `Update()` não roda nesta bancada (causa medida, não hipótese)

O instrumento da própria bancada (AUT4Probe) tem exatamente a mesma pergunta resolvida, e a
resposta está no próprio código dele e nos documentos do projeto:

- `scratch/cap1/CapProbe/CapProbePlugin.cs:94-99` — **"o Start/Update do plugin não roda porque a
  Unity DESTROI o GameObject do plugin na 1ª carga de cena (medido: `OnDestroy` em t=2,02s)"**;
- `docs/automacao/AUT-4-preparacao.md:30` e `docs/automacao/AUT-4-estado.json:436` — "driver no
  PlayerLoop do Unity (o `Update` do plugin é destruído na 1ª cena — padrão provado no CAP-1)";
- `tools/automacao/runtime/testes/t_aut4_probe_contrato.py:136` — o contrato **exige** o driver no
  PlayerLoop justamente para o motor não depender do `Update` do plugin.

E o vínculo com o Core é direto: os **dois** são plugins BepInEx e o chainloader adiciona os dois
componentes **no mesmo GameObject** — decompilado do `lib/BepInEx.dll` do repositório:

```
ManagerObject = new GameObject("BepInEx_Manager");
UnityEngine.Object.DontDestroyOnLoad(ManagerObject);
value2.Instance = (BaseUnityPlugin)ManagerObject.AddComponent(value4.GetType(value2.TypeName));
```

Não são dois GameObjects: é um só. Se o `Update` do componente do probe não ticka, o do componente
do Core também não — e o `Awake`, que a Unity chama **síncrono no `AddComponent`** (antes de
qualquer cena), roda sempre. Foi por isso que o `passivo` saiu preenchido e o `eventos` vazio.

### 3.1 A medição que separa as duas hipóteses (nenhum boot novo)

O probe grava a **origem dos 3 primeiros ticks** (`tick via <origem> (quadro N)`); há três drivers
independentes (gancho Harmony, subsistema no `PlayerLoop`, motor próprio) e o `Update` do plugin,
que gravaria `BepInEx.Update`. Varredura de **todos** os `scratch/**/*.log` do repositório
(`scratch/kit/KIT-14G-SEG1-run719/coleta_evidencia.py`, saída em `evidencia.json`):

| origem dos ticks registrados | n |
|---|---|
| `playerloop` (driver no PlayerLoop) | 140 |
| `gancho` (postfix de `GUIManager.Update`) | 63 |
| `motor` (MonoBehaviour próprio do probe) | 58 |
| **`BepInEx.Update` (o `Update` do plugin)** | **0** |

261 ticks registrados, **zero** pelo `Update` do plugin. E no boot do run712 (`mapa`) os três
primeiros ticks — os únicos que o instrumento loga por origem — são:

```
tick via gancho (quadro 1)
tick via gancho (quadro 2)
tick via gancho (quadro 3)
```

Isso é decisivo, não coincidência: o gancho (`GUIManager.Update`) só existe **depois** de a UI do
jogo nascer, enquanto o `Update` do plugin começaria no primeiro quadro após
`Chainloader startup complete`. Se o `Update` do plugin tivesse rodado **uma** vez, o `quadro 1`
sairia com origem `BepInEx.Update` — ele estava armado (`_autorizadoOk` já `true`, provado por
existirem ticks). A hipótese (b) do cartão ("o `Update()` roda e lança antes do `RegistrarEvento`")
fica **eliminada**: nenhuma exceção aparece no `Player.log` do boot, e uma exceção no
`RegistrarEvento` teria deixado `_eventos` já criado (vazio), mas o arranjo medido é consistente
com `_eventos == null` em todos os boots.

## 4. A correção (produto)

`CorePlugin.cs`: o evento `inicializacao` deixa de depender do `Update()` e passa a ser gravado por
`GarantirInicializacao()`, chamado no **fim do `Awake()`** — o caminho que sempre roda. O `Update()`
continua chamando o mesmo método (a flag garante **uma única** gravação) e agora **loga** quando
chega a tickar (`KIT-04 Core: primeiro Update() do plugin executado ...`), o que transforma a causa
em medida observável no próximo boot.

| | |
|---|---|
| fonte antes | `77e2d1cb31cf83d471f47c0d6b20d1f337ebcaca103b9775b25144b622095234` |
| fonte depois | `192e463675e2056f3476df2bd3f094e4795e67a130c4392c973c63619b282c59` |
| DLL Release | `tools/automacao/runtime/core/bin/Release/KIT04Core.dll` — `0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d` (34304 bytes) |
| build | `dotnet build tools/automacao/runtime/core/KIT04Core.csproj -c Release --no-incremental` → **0 Erro(s)**, 59 Aviso(s) (todos pré-existentes, de nulabilidade) |
| prova no binário | `ilspycmd` sobre a DLL: `Awake()` chama `GarantirInicializacao()`; `Update()` chama `Logger.LogInfo(...)` + `GarantirInicializacao()`; `GarantirInicializacao()` grava `inicializacao` uma vez |

O `Update()` **não** foi removido de propósito: o Core é "genérico, sem dependência de jogo
específico" (`CorePlugin.cs:1`) e em outros arranjos o `Update` funciona — a correção é
acrescentar o caminho garantido, não trocar um caminho pelo outro.

## 5. O que ficou NAO_EXERCITADO nesta rodada (e por quê)

**`ResultadoFinal().eventos` com contagem > 0 num boot real: NAO_EXERCITADO.**

A prova em boot real (a primeira metade do aceite: "com o Core habilitado num boot real,
`ResultadoFinal().eventos` contém ao menos `inicializacao`, com prova por arquivo `recorder.json` e
contagem > 0") exige **abrir o jogo** pela bancada, e nesta rodada a bancada está **ocupada**: o
cartão irmão `t_139f714f` (KIT14G-SEG2 — clique sintético / `c0000005`) está `running` e editando
`tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` ao vivo (mtime mudando a cada ~15 s durante
esta rodada). Duas rodadas de jogo simultâneas colidem em três pontos concretos:

- a trava de frente única (`scratch/kit/front-unica.sh`) existe para que só uma rodada controle o
  jogo — abrir a minha derrubaria a do irmão (ou o contrário), e nenhuma das duas seria honesta;
- `kit16-save-isolado.sh` **renomeia** o diretório real do dono e o expõe por junction durante a
  rodada: duas pipelines entrelaçadas é exatamente o cenário em que o save do dono fica renomeado;
- o driver exige `sha(fonte do probe) == sha(cópia do sandbox)`, e o irmão está reescrevendo essa
  fonte — o gate recusaria (ou pior, congelaria uma cópia intermediária).

Por isso a prova em boot real foi **delegada a um cartão filho** (`parents = [t_21e89a61,
t_139f714f]`), que só promove quando os dois terminarem.

O que **sustenta** a correção sem boot:

- o aceite admite explicitamente a alternativa "explicação medida de por que o `Update()` não roda
  nesta bancada" — é o §3, com 261 ticks observados e zero pelo `Update` do plugin;
- o caminho novo é o `Awake`, cuja execução **já está provada** na evidência congelada do run712
  (`passivo`/`identidade`/`sessao` preenchidos). A única porta que faltava para o livro existir
  passou a ser um caminho provado.

## 6. Concorrência de bancada (para o orquestrador)

`hotspot: tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` — o cartão irmão `t_139f714f`
(KIT14G-SEG2) está reescrevendo esse arquivo ao vivo; qualquer rodada de bancada (minha prova em
boot real, incluída) precisa esperar a frente única liberar. O meu diff **não** toca nesse arquivo:
mudou só `tools/automacao/runtime/core/CorePlugin.cs`.

## 7. Evidência desta rodada

- `scratch/kit/KIT-14G-SEG1-run719/coleta_evidencia.py` — coleta somente-leitura (a fonte do número).
- `scratch/kit/KIT-14G-SEG1-run719/evidencia.json` — tudo o que está citado aqui, com hashes.
- `scratch/kit/KIT-14G-SEG1-run719/coleta.stdout.log` — saída bruta.
