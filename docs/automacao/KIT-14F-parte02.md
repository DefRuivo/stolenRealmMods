# KIT-14F — parte 02: RED antes / GREEN depois dos 3 defeitos (evidência executada)

Cartão `t_c46abdf7`; autor `default/run706` (continuação de run705, que produziu a parte01).
Complementa `KIT-14F-parte01.md` **sem sobrescrever** nada. Nenhum build foi instalado no
perfil do dono (`DeployToBepInEx` default = false), nenhum clique de sistema, nenhum
`execute_code`, nenhum commit.

## 0. Onde está a prova

Raiz: `scratch/kit/KIT-14F-run706/`

| arquivo | o que é |
|---|---|
| `log-baseline-adapter-parte1e2.txt` | **ANTES** (defeitos 1 e 2) — harness contra a build baseline do Adapter |
| `log-baseline-probe-parte3.txt` | **ANTES** (defeito 3) — harness contra a build baseline do probe |
| `log-consertado-todas.txt` | **DEPOIS** — o MESMO harness contra as builds consertadas |
| `baseline-adapter/` | DLL do Adapter **pré-conserto** (fonte = a build entregue no KIT-14/run699, a que o run704 testou) |
| `baseline-probe/` | DLL do probe **pré-conserto** (fonte = `git show HEAD:...AUT4ProbePlugin.cs`) |
| `_sha-consertado.txt` | sha256 dos dois fontes consertados, conferido depois de restaurar (`sha256sum -c` = OK/OK) |

O teste é um só (`tools/automacao/runtime/harness-kit14f`, novo). O que muda entre ANTES e
DEPOIS é **a build exercitada**, via `--adapter-bin=<dir>` / `--probe-bin=<dir>`; o binário do
harness é o mesmo. Cada parte roda em **processo próprio** (o harness re-executa a si mesmo),
porque as partes compartilham estado estático do Adapter/Core.

## 1. Defeito 1 — Adapter estoura em `Awake` com NullReferenceException

**Como estava errado (código vivo, baseline run699):** `[BepInDependency]` ausente, `Awake`
lia `var core = CorePlugin.Instancia;` e seguia usando `core` sem guarda. Com o Chainloader
listando o Adapter antes do Core (run704, `LogOutput` isolado linhas 19–20), `core` é null →
`core.Passivo` estoura.

**Como está agora:** `SRAdapterPlugin` declara `[BepInDependency("com.gumatos.kit04.core")]`;
`Awake` chama `TentarVincular()`, que é idempotente, NUNCA derreferencia null, declara
`_estadoVinculo="aguardando_core"` quando o Core ainda não subiu, e o `Update` retoma o
vínculo quadro a quadro.

**Evidência `--parte1` (mesmo teste, mesma ordem Adapter-antes-de-Core):**

```
ANTES (baseline-adapter)                              DEPOIS (consertado)
[FALHA] Adapter.Awake NAO estoura ... NRE             [OK] Adapter.Awake NAO estoura ...
[FALHA] declara vinculo PENDENTE -> _estadoVinculo=   [OK] declara vinculo PENDENTE (aguardando_core)
[FALHA] declara [BepInDependency] -> deps=[]          [OK] declara [BepInDependency] (com.gumatos.kit04.core)
[FALHA] TentarVincular AUSENTE no Adapter             [OK] vinculo conclui (sem excecao)
                                                      [OK] ponte da trilha passiva criada
                                                      [OK] estado do vinculo = ligado
                                                      [OK] conclui nos 3 quadros simulados (idempotente)
                                                      [OK] a ponte NAO e recriada a cada quadro
verificacoes: 1 OK, 4 FALHA                           verificacoes: 9 OK, 0 FALHA
```

Correção acessória medida nesta rodada: o Harmony era aplicado ANTES de marcar o vínculo, e
uma falha no patching deixava o Adapter ligado mas **sem estado declarado**. O vínculo agora é
marcado antes e o patching ficou em `try/catch`, com o resultado em `HarmonyEstado`
(no harness sai `falhou: TypeInitializationException ... HarmonyLib.AccessTools`, que é
esperado fora do jogo).

## 2. Defeito 2 — recorder (trilha passiva) sem contagem comprovada

**Antes:** o defeito 1 matava o `Awake`, então a ponte nunca nascia e não havia o que contar
(o run704 registrou exatamente isso: recorder não inicializado, sem arquivo).

**Agora:** `--parte2` usa a ponte REAL criada pelo Adapter, alimenta transições/clique pelo
MESMO método que o `Update` chama (`AlimentarPassivo(bool[],bool,long)`) e exige contagem > 0
**e** arquivo lido de volta do disco.

```
ANTES (baseline-adapter)                              DEPOIS
[FALHA] recorder produz contagem -> o Adapter nem    [OK] recorder capturou CONTAGEM > 0 (passivo.eventos_total=3)
        subiu: NRE em SRAdapterPlugin.Awake()         [OK] recorder registrou os eventos no livro (3)
[FALHA] recorder produz arquivo -> sem trilha         [OK] eventos tem tipo 'passivo_*'
                                                      [OK] arquivo de resultado (bytes>0, lido de volta)
                                                      [OK] arquivo contem os eventos capturados
verificacoes: 0 OK, 2 FALHA                           verificacoes: 5 OK, 0 FALHA
```

## 3. Defeito 3 — navegação acha 0 botões / sem Skills

**Como estava (baseline HEAD do probe):** `TentarNavegar()` varria `Recursos<Button>()` **uma
vez**, gravava `estagio=procurar` com `botoes_ativos`/`achou_skills` e encerrava: sem espera,
sem contagem de tentativas, sem teto, sem motivo quando não achava, e sem costura injetável para
exercitar a escolha fora do jogo (era o `botoes_ativos=0` do run704, na tela de LOADING).

**Como está agora** (`AUT4ProbePlugin.TentarNavegar`): espera por quadros com **tentativas** e
**teto** explícitos (`NavegacaoTentativasMax=12`, sobreponível por config), grava um estágio
`resumo` com `estado` (`aguardando`/`invocado`/`esgotado`/`falha`), `tentativas`,
`tentativas_max` e `motivo`; invoca o handler **exatamente uma vez** quando o alvo aparece e
para de tentar; e tem a **porta injetável** `PortaDeBotoes` (default null = varredura real da
engine) usada pelo teste.

```
ANTES (baseline-probe)                                DEPOIS
[FALHA] navegacao grava um RESUMO (estagio=resumo)    [OK] navegacao grava um RESUMO (estagio=resumo)
[FALHA] resumo declara numero de TENTATIVAS           [OK] resumo declara numero de TENTATIVAS
[FALHA] resumo declara TETO de tentativas             [OK] resumo declara TETO de tentativas
[FALHA] resumo declara MOTIVO quando esgota           [OK] resumo declara MOTIVO quando esgota
[NAO_EX] caminho positivo: probe sem porta injetavel  [OK] ESPERA e encontra o alvo no 3o quadro
                                                      [OK] invoca o handler EXATAMENTE uma vez
                                                      [OK] para de tentar depois de invocar
verificacoes: 0 OK, 4 FALHA, 2 NAO_EXERCITADO         verificacoes: 7 OK, 0 FALHA
```

Saída real do estágio esgotado (12 quadros com 0 botões — o quadro do run704):

```
estagio=procurar tentativa=12 tentativas_max=12 botoes_ativos=0 achou_skills=False
estagio=resumo estado=esgotado tentativas=12 tentativas_max=12
  motivo=nenhum botao ativo com rotulo contendo 'Skills' em 12 quadros (quadros com 0 botoes ativos na ultima leitura: True)
```

## 4. Duas armadilhas do harness que precisaram ser consertadas (não são do produto)

Ambas ficam declaradas porque **já produziram diagnóstico falso** nesta rodada:

1. **`m_CachedPtr` — "null falso" do `UnityEngine.Object`.** `UnityEngine.Object` sobrecarrega
   `==` e trata como NULL qualquer objeto sem objeto nativo
   (`IsNativeObjectAlive(o) => o.GetCachedPtr() != IntPtr.Zero`, conferido por decompilação em
   `lib/UnityEngine.CoreModule.dll`). Como o harness cria os plugins por
   `FormatterServices.GetUninitializedObject`, `m_CachedPtr` ficava 0 e **`core == null`
   devolvia TRUE para um Core EXISTENTE** — o vínculo nunca concluía e o conserto parecia
   errado. `LigarBaseUnityPlugin` agora marca `m_CachedPtr` (um plugin real sempre tem objeto
   nativo). Um plugin de jogo sempre tem esse ponteiro, então isto é artefato do harness.
2. **`GetUninitializedObject` não roda inicializador de campo.** `CorePlugin.Identidade` fica
   null e `ResultadoFinal()` estourava NRE. `CompletarInicializadoresDePropriedade` preenche o
   que o inicializador faria. Também artefato do harness (a Unity usa o construtor normal).
3. Menor: o opt-in `_habilitado` do Core é campo de **instância** (`LigarOptIn` procurava
   estático e devolvia `false` em silêncio).

## 5. NAO_EXERCITADO (com motivo) — o que este cartão NÃO provou

- **Chainloader real do BepInEx ordenando os plugins dentro do jogo.** Exige o jogo aberto;
  proibido boot/clique não supervisionado nesta rodada. A ordem observada no run704 é
  **simulada** chamando `Awake` do Adapter antes do Core. O `[BepInDependency]` (que é o
  mecanismo de ordenação do BepInEx 5) foi verificado **por atributo**, não por efeito.
- **Recorder capturando de um jogo real em execução.** Exige jogo aberto + build instalada.
  A contagem (3) e o arquivo vêm da trilha REAL alimentada por estado SINTÉTICO.
- **Navegação clicando um `Button` REAL do jogo.** O alvo é servido pela porta injetável; o
  caminho `Recursos<Button>()` + `onClick.Invoke()` da engine não foi executado (offline ele
  dispara `ECall`). O caminho de engine **é** o default do código (porta nula), mas não foi
  medido aqui.
- **Harmony patchando de verdade** (`HarmonyEstado = "falhou: TypeInitializationException ..."`
  no harness). Fora do jogo não há runtime de detours; em jogo é esperado "aplicado".
- **Performance/overhead do recorder** (o run704 declarou NAO_EXERCITADO e este cartão não
  reabriu): sem mesmo cenário interativo e sem contadores de frame, nada foi medido.
- **Build instalada no perfil do dono / aceite humano de UI.** Proibido por este cartão.

## 6. Como reproduzir (sem jogo, sem instalar nada)

```bash
cd C:/dev/stolen-realm
# CLARO (consertado)
./tools/automacao/runtime/harness-kit14f/bin/Release/net6.0/harness-kit14f.exe
# VERMELHO do defeito 1+2 (build baseline do Adapter)
./tools/.../harness-kit14f.exe --parte1 --parte2 \
  --adapter-bin="C:/dev/stolen-realm/scratch/kit/KIT-14F-run706/baseline-adapter"
# VERMELHO do defeito 3 (build baseline do probe)
./tools/.../harness-kit14f.exe --parte3 \
  --probe-bin="C:/dev/stolen-realm/scratch/kit/KIT-14F-run706/baseline-probe"
```
Exit: 0 = tudo verde · 1 = algo REPROVOU · 2 = uso/infra. As DLLs baseline são artefatos
**congelados** desta rodada; o `bin/Release` do repositório permanece com as builds consertadas.

## 7. Arquivos de implementação tocados (só o necessário)

- `tools/automacao/runtime/KIT04Adapter.SR/SRAdapterPlugin.cs` (+`BepInDependency`,
  `TentarVincular`/`LerCore`, `AlimentarPassivo`, `HarmonyEstado`, estado do vínculo declarado)
- `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` (navegação com espera/teto/motivo +
  `PortaDeBotoes`; **nada** mais do probe foi alterado)
- `tools/automacao/runtime/harness-kit14f/{Program.cs,harness-kit14f.csproj}` (teste novo)
- `tools/automacao/runtime/core/CorePlugin.cs`: **não** ficou alterado (uma hipótese
  intermediária de causa-raiz foi testada e revertida; sha conferido)
