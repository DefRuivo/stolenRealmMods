# INT-R1-C2-I1 — parte 01: a ponte (entregável A, offline)

Cartão `t_a706b09c`. Pai `t_2ea91249` (arquitetura em `INT-R1-C2-parte01..04.md`). Esta parte cobre o
**núcleo** do cartão: o adaptador RealmApi → KitSdk, executável **sem jogo**, com prova de vermelho.

---

## 1. O que foi entregue (arquivos)

| Ação | Caminho | sha256 |
|---|---|---|
| NOVO | `tools/automacao/kit13/ApiBridge/ApiBridge.csproj` | `5d3bec31da1bd3b279e69e3be2978abce4b4481c0dc61d86f63f6294382610bb` |
| NOVO | `tools/automacao/kit13/ApiBridge/RealmHooksBinding.cs` | `cc50bfc05c43cc7441c8ee58a3def2d048153b8715bf1f5f904576c83cbc6a12` |
| NOVO | `tools/automacao/kit13/ApiBridge/RealmHooksExtension.cs` | `7c282c5e2ab26fb42b035359ae1c562d44f5db01719677b82aee48ceab092e43` |
| NOVO | `tools/automacao/kit13/ApiBridgeHarness/ApiBridgeHarness.csproj` | `a67faa9d4da2243287b08f92a199324010177655abcd3992802e31ebadca3400` |
| NOVO | `tools/automacao/kit13/ApiBridgeHarness/Program.cs` | `770dcb3765cf5c04a28c466da5ee431ecfd96a9d8ed42a0b7ee4ea79e26c6ab9` |
| NOVO | `tools/automacao/kit13/prove_bridge_mutations.py` | `755d09cb1c3cffbff6856613221876862333fd292fca2d94f8b9e0ec9d4b3519` |
| NOVO | `docs/automacao/INT-R1-C2-I1-parteNN.md` + `INT-R1-C2-I1-evidencias/` | este documento e a pasta de evidência |

**Congelado, conferido por sha256 nesta rodada (idênticos à linha de base do pai):**

| Arquivo | sha256 medido agora | sha256 na linha de base | Veredito |
|---|---|---|---|
| `api/Core/Contracts.cs` | `7970780440d1682a7b3bb3d09ddc4812c7371ae5a85edf141e575caf7d48cb62` | igual | intacto |
| `tools/automacao/kit13/SDK/RegistryV1.cs` | `9f2eabdd5da1a3796e7c191f241ff5687d9fb876d51a0bd03117ed1789187700` | igual | intacto |

Nenhum `.cs` de `api/**`, `kit13/SDK/**`, `kit13/CoreBridge/**`, `prove_mutations.py`, `prove_offline.py`,
`packages.py`, `test_packages.py` ou `examples/*.json` foi aberto para escrita (a verificação
`live_changed: []` do script de mutação cobre 41 arquivos da árvore viva).

## 2. Superfície entregue (D4, sem desvio)

```
namespace Gumatos.KitApiBridge
    public static class RealmHooksBinding
        public static RealmHooksExtension Create(RegistryV1 registry, Signal<HookNotification> observed,
            Func<bool> producerActive, Func<string> session, Action<string> diagnostic)
    public sealed class RealmHooksExtension : IExtensionV1, IDisposable
        public const string KitApi = "1.0.0";
        public const string ProducerVersion = "0.1.0";
        public const string RegistryId = "realmapi.hooks";
        OnEvent(HookNotification)  -> push (o callback do Signal)
        OnEvent(EventV1)           -> eco do kit; NO-OP, para nao recircular
        Read(key)                  -> "hooks.count" | "hooks.unknown" | "hook.<hookId>.count" | AUSENTE
        Validate(key, observed, expected)
        Dispose()
```

Direção da dependência (D3) verificada pelo `csproj`: `ApiBridge -> {../SDK/KitSdk.csproj,
../../../../api/Core/RealmApi.Core.csproj}` e **nada mais** — sem `BepInEx`, `0Harmony`, `UnityEngine`,
`api/Hooks` ou `api/Plugin`. O build dos dois projetos novos dá **0 avisos / 0 erros**.

**Uma sutura interna declarada** (não é superfície pública): `RealmHooksBinding.Create` tem uma
sobrecarga `internal` com dois parâmetros extras (`kitApiDeclarado`, `producerVersionDeclarada`) e o
assembly declara `[assembly: InternalsVisibleTo("ApiBridgeHarness")]`. Motivo: a fronteira F4 é
"string exata" e as constantes dos dois núcleos (`RegistryV1.ApiVersion`, `ApiIdentity.Version`) estão
**congeladas**; sem a sutura, o único jeito de exercitar a recusa seria reflexão sobre constantes.
O caminho **público** chama o mesmo verificador com as constantes reais. Alternativa rejeitada:
editar `api/**` ou `SDK/**` (proibido neste cartão).

## 3. Prova executada

Comando (bate com o formato do `Harness/Program.cs:62` e com o `Kit13OfflinePreflight` dos outros csproj):

```
dotnet build tools/automacao/kit13/ApiBridgeHarness/ApiBridgeHarness.csproj -c Release -p:DeployToBepInEx=false
dotnet tools/automacao/kit13/ApiBridgeHarness/bin/Release/net6.0/ApiBridgeHarness.dll
```

Saída medida nesta rodada: **`Ran 17 tests; failures=0; OFFLINE_ONLY`**, exit `0`
(`docs/automacao/INT-R1-C2-I1-evidencias/suite-baseline.log` e
`suite-17-testes-baseline.json`). Preflight offline conferido nos dois projetos novos:
`-p:DeployToBepInEx=true` → exit `1` com `KIT13:`; `=false` → exit `0`
(`commands.json`, labels `preflight-negado-*`/`preflight-seguro-*`).

Cobertura das 15 asserções obrigatórias (P1..P15) + 2 asserções próprias:

| Asserção | O que ela mede | Onde no artefato |
|---|---|---|
| P1 | `KitApi="1.0.0"` exato → `Count==1`, id `realmapi.hooks`, id exato (id vizinho = AUSENTE) | `Program.cs` P1 |
| P2 | kit `2.0.0` → `NotSupportedException` com `API_INCOMPATIVEL`, `Count==0`; **com registry já descartado** a recusa só pode ser a do adaptador (senão viria `ObjectDisposedException`) | P2 |
| P3 | `ProducerVersion` divergente → recusa **e** nenhuma assinatura no Signal (prova: publicar 3 e ver zero) | P3 |
| P4 | sessão `""`, `"   "`, 129 chars e `null` → `ArgumentException` antes de registrar/assinar; 128 chars é aceito | P4 |
| P5 | `producerActive()==false` → zero `EventV1` na testemunha e `Read("hooks.count")` = `NAO_EXERCITADO`; o lease continua (`Count==2`) | P5 |
| P6 | produtor ativo: 3 publicações → `"3"`; zero → `"0"` **OBSERVADO**; inativo→ativo **não** acumula | P6 |
| P7 | 1 `EventV1` por hook conhecido, `Kind==HookId`, `Session` declarada, `Frame` 0,1,2 e `Data` com `quadro=ordinal` | P7 |
| P8 | hook desconhecido → zero evento, `hooks.unknown=="1"`, chave fora do vocabulário = AUSENTE e `Validate` = `NAO_EXERCITADO` (nunca `PASSOU`) | P8 |
| P9 | `hook.ui.localized.count` conta só aquele hook; 6 chaves fora do vocabulário = AUSENTE | P9 |
| P10 | `Result` de 10 000 chars → `Data` ≤ 4096 **com marcador** `[...TRUNCADO]`, sem `ArgumentException` e sem corte silencioso | P10 |
| P11 | mutar o array de argumentos depois da publicação não muda o `Data` já publicado, e o evento seguinte resume os **seus** argumentos (sem referência viva entre eventos) | P11 |
| P12 | `OnEvent` de outro thread (`Task.Run`) com `producerActive` que **lança** → não lança, não trava (limite 2 s), nada chega ao canal do produtor, tipo no canal de diagnóstico | P12 |
| P13 | testemunha que lança: as outras continuam recebendo, o kit guarda só o TIPO (marcador secreto ausente); canal de diagnóstico do adaptador limitado (64 entradas, ≤512 chars, sem a mensagem) | P13 |
| P14 | `Dispose` → lease liberado, assinatura removida, zero eventos novos, **`OnEvent` direto depois do Dispose não entrega**, idempotente | P14 |
| P15 | reentrância: extensão que chama `Publish` dentro do `OnEvent` → `EVENTO_REENTRANTE` registrado pelo kit; e aninhamento pelo produtor → o adaptador **não engole**: registra o TIPO e não lança | P15 |
| P16 (própria) | caminho do produtor de verdade: `RealmHooks.Emit` → `RealmHooks.Observed` entrega, `report` do produtor sem exceção | P16 |
| P17 (própria, entregável B) | o caminho de consumo do `AUT4Probe` (companheiro → testemunha → gatilho), ver parte 02 | P17 |

### Instrumentação declarada (não é atalho escondido)

O produtor **só publica por dentro**: `HookNotification..ctor` (`api/Core/Contracts.cs:75`),
`Signal<T>.Publish` (`:91`) e `RealmHooks.Emit` (`:109`) são `internal`, e `api/**` está congelado neste
cartão. A suíte injeta por esses membros **via reflexão** (classe `Producao`), que é a única via sem
editar o produtor. Consequência declarada: o caminho Harmony real (`HookInstallation.Install` → postfix
→ `Emit`) fica **NAO_EXERCITADO**.

## 4. Prova de não-decorativo (0→1→0)

```
python tools/automacao/kit13/prove_bridge_mutations.py --out <diretorio NOVO>
```

Resultado medido: **`BRIDGE_MUTATIONS_PASSOU|10|…`**, exit `0`
(`docs/automacao/INT-R1-C2-I1-evidencias/mutations.json`, `verification.json`, `commands.json`, logs
`*-RED-*.log`). O script copia a árvore para um sandbox, muta o **fonte real** lá dentro, exige build do
mutante **com sucesso** e depois `exit 1` com `FAIL|<teste>`; restaura byte a byte e confere o sha256.

| Mutação | Fonte | O que quebra | Vermelho observado |
|---|---|---|---|
| m1 gate do `OnEvent` | `ApiBridge/RealmHooksExtension.cs` | publica com produtor inativo | `P5` |
| m2 gate do `Read` | idem | `NAO_EXERCITADO` vira `OBSERVADO` | `P5` |
| m3 mapeia todo `HookId` | idem | lixo do produtor vira evento | `P8` |
| m4 sem marcador de truncamento | idem | corte silencioso do `Data` | `P10` |
| m5 referência viva dos argumentos | idem | evento usa a lista do evento anterior | `P11` |
| m6 `OnEvent`/gate do host propagam exceção | idem | exceção do consumidor no log do produtor | `P12`, `P13` |
| m7 versão por prefixo/ordem | `ApiBridge/RealmHooksBinding.cs` | aceita par incompatível | `P2`, `P3` |
| m8 `Frame = 0` fixo | `RealmHooksExtension.cs` | numeração falsa (indistinguível de "primeiro quadro") | `P7` |
| m9 `OnEvent` depois do `Dispose` | idem | corrida real do snapshot do `Signal` entrega sem lease | `P14` |
| m10 publicação propaga exceção (guarda de `OnEvent` **e** a de `Publicar`) | idem | `EVENTO_REENTRANTE` do kit vaza para o log do produtor | `P15` |

Cada mutação tem `sha256` antes = `sha256` restaurado (`mutations.json`) e a árvore **viva** termina com
`live_changed: []`, `sandbox_divergente_do_baseline: []`.

**Duas tentativas descartadas, declaradas** (não entraram como prova):
`m10` na forma "só remover a guarda de `Publicar`" e `m-dispose-nao-remove-assinatura` passavam a suíte —
a guarda redundante do `OnEvent` mascara as duas. Mutação que não derruba asserção não prova nada, então
saiu do conjunto; a versão final de `m10` remove as **duas** guardas e derruba `P15`.

## 5. NAO_EXERCITADO desta parte (com motivo)

- Harmony real (`HookInstallation.Install`), postfix no `Assembly-CSharp` e `BepInEx` carregando
  `RealmApi.dll` com `EnableHooks=true`: **NAO_EXERCITADO** — exige o jogo; este cartão não instala,
  não abre o jogo e não deploya no perfil r2modman.
- Adaptador rodando dentro do processo do jogo, com alvo real e hook real: **NAO_EXERCITADO**, mesma razão.
- `api/Plugin/RealmApiPlugin.cs` não foi alterado: o host que constrói o adaptador (D5/D7) é **frente
  nova** — este cartão entrega o adaptador e a prova offline, não a fiação do plugin.
