# INT-R1-C2 — parte 02: a decisão escrita (papéis, direção da dependência, ausência do produtor)

Cartão `t_2ea91249`. Complementa a parte 01 (mapa tipo-a-tipo). Aqui não há código novo: há decisão.
Cada decisão vem com a alternativa que foi **rejeitada** e o motivo, para o revisor poder discordar de algo
concreto em vez de "achar o tom errado".

---

## 1. Decisões

### D1 — Papéis: a API é o produtor, o kit é o consumidor. Ninguém absorve ninguém.

- **Produtor**: `Gumatos.RealmApi` (`api/Core` + `api/Hooks` + `api/Plugin`). É o único lado que fala com o
  jogo: resolve `MethodInfo` por assinatura exata (`api/Core/Contracts.cs:46-54`) e instala postfixes
  Harmony (`api/Hooks/HookInstallation.cs:21-48`), com gate de identidade do alvo
  (`Contracts.cs:24-26`).
- **Consumidor**: `Gumatos.KitSdk.V1` (`tools/automacao/kit13/SDK`) e quem consome o kit (instrumentos,
  `AUT4Probe` na parte observacional, cenários declarativos). É o único lado que é executável **sem o
  jogo**: `netstandard2.1` sem nenhuma referência de Unity/BepInEx (`README.md` do kit, linha 12 do
  repositório `tools/automacao/kit13/README.md`, e o próprio `KitSdk.csproj:1-11` sem `ItemGroup`).
- **Por que não "absorver"**: as duas assimetrias são estruturais, não estéticas. (a) O produtor não pode
  depender do kit — o pacote in-game precisa continuar mínimo e não pode ganhar dependência de ferramenta
  de bancada. (b) O kit não pode depender do Unity — é exatamente isso que permite a prova offline
  (`Ran 17 tests; failures=0; OFFLINE_ONLY`, executado nesta rodada; ver parte 04). Unificar num só assembly
  forçaria uma das duas assimetrias a morrer.
- **Alternativa rejeitada**: "o kit vira o núcleo único e a API é uma extensão do kit" — isso poria a
  dependência do produtor no consumidor e obrigaria o pacote in-game a carregar tipos de bancada.

### D2 — O contrato versionado que sobrevive: **os dois, com um único ponto de contato**.

Sobrevive por inteiro, sem migração:

| Contrato | Onde vive | Versão | Quem confere |
|---|---|---|---|
| **Contrato do consumidor** (observador/leitura/veredito/registro) | `Gumatos.KitSdk.V1` (`RegistryV1.cs:6-152`) | `1.0.0` (`RegistryV1.cs:58`) | `RegistryV1.Register` (`RegistryV1.cs:92`) e `packages.py:51` |
| **Contrato do produtor** (identidade do alvo, catálogo de hooks, notificação) | `Gumatos.RealmApi` (`Contracts.cs:10-127`) | `0.1.0` do pacote (`Contracts.cs:17`) | `ApiIdentity.Matches` (`Contracts.cs:24-26`) |

O que **não** sobrevive é a pretensão de que um substitui o outro. O único ponto de contato acordado entre
os dois é **um adaptador**, novo e explicitamente listado — e nenhum dos dois núcleos ganha dependência do
outro (§D3).

### D3 — Direção da dependência: o adaptador depende dos dois; nem um núcleo depende do outro.

```
Gumatos.KitSdk.V1  ──┐
                     ├──►  Gumatos.KitApiBridge   (NOVO, netstandard2.1, offline)
Gumatos.RealmApi ────┘        │
                              └── registra-se no RegistryV1 e assina RealmHooks.Observed
```

- `Gumatos.RealmApi` **nunca** referencia `Gumatos.KitSdk`. Consequência verificável: o conjunto de hashes
  de `api/**` continua idêntico antes e depois desta frente (o build da API tem 5 projetos, 0 avisos /
  0 erros, `api/docs/smoke-result.json`).
- `Gumatos.KitSdk` **nunca** referencia `Gumatos.RealmApi` (hoje: nenhuma referência — `KitSdk.csproj`).
  O kit entregue e revisado (KIT-13 / KIT-13R) permanece **bit-a-bit** o que era.
- O adaptador é o **único** lugar autorizado a conhecer os dois nomes. Ele não carrega plugin, não instala
  patch, não abre arquivo e não autoriza nada: recebe tudo do host por parâmetro (§D7).
- **Alternativa rejeitada**: pôr a ponte dentro de `api/` (o produtor dependendo do kit) ou dentro do
  `SDK/` do kit (o contrato do consumidor ganhando um tipo que só existe quando a API existe — o kit
  deixaria de compilar/funcionar sozinho, o que o KIT-13 provou como requisito: mod e SDK funcionam sem
  dependência CLR de terceiros).

### D4 — O que vira adaptador: a **observação** coincidente, não o kit e não a API.

`RealmHooksExtension : IExtensionV1` (nome e superfície fechados aqui, para o cartão filho não decidir nada):

```csharp
namespace Gumatos.KitApiBridge
{
    public static class RealmHooksBinding
    {
        // Única porta. Tudo o que o adaptador precisa vem do host, nunca de descoberta.
        public static RealmHooksExtension Create(
            RegistryV1 registry,               // contrato do consumidor
            Signal<HookNotification> observed, // contrato do produtor (RealmHooks.Observed)
            Func<bool> producerActive,         // D7
            Func<string> session,              // D6: sessão declarada pelo host, não pelo jogo
            Action<string> diagnostic);        // canal próprio, limitado (D8)
    }

    public sealed class RealmHooksExtension : IExtensionV1, IDisposable
    {
        public const string KitApi = "1.0.0";          // par declarado (ver §2)
        public const string ProducerVersion = "0.1.0";
        // id de registro: "realmapi.hooks" (satisfaz [a-z][a-z0-9.-]{0,63} de RegistryV1.cs:93)
        // OnEvent: HookNotification -> EventV1 (push para o RegistryV1)
        // Read:    "hooks.count" | "hooks.unknown" | "hook.<hookId>.count"
        // Validate: só sobre chave de leitura; observed.Status != OBSERVADO -> NAO_EXERCITADO
    }
}
```

- **Chaves de leitura fechadas** (o adaptador é o dono do vocabulário): `hooks.count` (total aceito),
  `hooks.unknown` (chegou com `HookId` fora do catálogo conhecido), `hook.<hookId>.count` (por hook, com
  o `hookId` do catálogo, ex. `hook.ui.localized.count`). Qualquer outra chave → `AUSENTE`
  (`RegistryV1.cs:133`), nunca valor plausível.
- **Precedente, não invenção**: `CoreEventsExtension` (`tools/automacao/kit13/CoreBridge/CoreEventsExtension.cs`)
  já é exatamente este desenho para o Core KIT-04 — `OnEvent` empurra, `Read` conta, `Validate` compara, e o
  `CorePluginBinding` injeta a autorização do host (`CorePluginBinding.cs:11-16`). O que falta é o mesmo
  desenho apontado para o núcleo da **API**; esta decisão só fixa a superfície.
- **`AUT4Probe`**: a parte **observacional** que coincide com o catálogo passa a consumir pelo adaptador
  (detalhe e aceite na parte 03). O que **não** muda: o clique/navegação (`t_139f714f`), o motor por
  `PlayerLoop` e a captura de PNG — a API 0.1.0 é observacional e não dirige input
  (`docs/automacao/INT-R1-parte03.md:20`).

### D5 — Quando o produtor não está lá: três estados explícitos, nenhum "talvez".

| Estado | Como o adaptador sabe (fonte) | O que ele faz | O que o kit publica |
|---|---|---|---|
| **API não instalada** (assembly `RealmApi.Core` ausente do processo) | O **host** não constrói o adaptador. Não existe descoberta por reflexão. | nada — o adaptador não existe | nada: nenhuma inscrição, `RegistryV1.Count` sem a ponte; kit e instrumentos funcionam como hoje (KIT-13 prova `standalone_no_sdk_exit: 0`) |
| **API instalada, `EnableHooks=false`** (`RealmApiPlugin.cs:21` retorna antes de instalar) | `producerActive()` do host devolve `false` | registra-se (o lease é do ciclo de vida, não da atividade) e **não publica nenhum `EventV1`** | leituras → `NAO_EXERCITADO` (motivo: produtor inativo); `Validate` → `NAO_EXERCITADO` |
| **API instalada, `EnableHooks=true`, alvo divergente** (gate `Matches` falha, `RealmApiPlugin.cs:29-30`) | Zero notificações **e** `producerActive()` continua `false` | idem acima | idem acima |
| **API ativa** | `producerActive()` devolve `true` | publica um `EventV1` por `HookNotification` conhecida; ignora desconhecida incrementando `hooks.unknown` | leituras → `OBSERVADO` com o contador real (**inclusive 0**) |

O ponto que **exige** o `Func<bool>`: "zero notificações" é ambíguo (produtor inativo × jogo parado numa
tela sem tráfego de hooks). Sem a declaração do host, o adaptador seria obrigado a escolher entre mentir
(`OBSERVADO, 0`) ou mentir ao contrário (`AUSENTE` quando o produtor está ativo). Por isso `producerActive`
é **parâmetro obrigatório**, com o mesmo padrão já provado em `CorePluginBinding.Create(core, hostObservationAuthorized)`
(`CorePluginBinding.cs:11-16`) — **nunca** um `bool` lido de arquivo de config pelo próprio adaptador.
Alternativa rejeitada: o adaptador ler `Safety.EnableHooks`/`ApiIdentity` por reflexão — isso violaria a nota
do SDK ("No assembly loading, script execution, authorization" — `RegistryV1.cs:47-48`) e criaria um segundo
leitor não confiável da mesma config.

### D6 — O buraco real: `HookNotification` não tem sessão nem quadro.

`EventV1` **exige** `Session` não vazia (≤128) e `Frame ≥ 0` (`RegistryV1.cs:16-18`). `HookNotification`
carrega `HookId`, `Instance`, `Arguments`, `Result` (`Contracts.cs:69-77`) — **não** carrega sessão e **não**
carrega número de quadro. Decisão:

- `Session` ← `Func<string> session` do host (sessão do **experimento**, não do jogo), validada antes de
  registrar, exatamente como `CounterAdapter` valida antes de inscrever
  (`tools/automacao/kit13/OptionalAdapter/CounterAdapter.cs:22-24`).
- `Frame` ← **ordinal da observação no adaptador** (0,1,2,…), e o `Data` carrega a marca
  `quadro=ordinal`, para que ninguém confunda com o quadro Unity.
- Alternativas rejeitadas: (a) `Frame=0` fixo — 0 é um quadro legal, então seria um valor **falso
  indistinguível** de "primeiro quadro"; (b) tornar `Frame` opcional no `EventV1` — violaria o limite desta
  rodada ("não alterar o comportamento do kit entregue", KIT-13 done e revisado por KIT-13R).
- `Data` ≤ 4096 (`RegistryV1.cs:17`): o adaptador monta um resumo **limitado e truncado com marcador**
  (`HookId`, tipo do alvo, e o `Result` só quando já for `string`). Ele **não** serializa `Instance` nem
  `Arguments` em geral: `Arguments` é cópia **rasa** da lista (`Contracts.cs:76`), os objetos de dentro
  continuam vivos do Unity, e tocá-los no thread do hook pode lançar; o adaptador não pode lançar (§D8).

### D7 — Autorização: sempre do host, em código, nunca de config do adaptador.

`producerActive` e `session` são `Func<>` injetados. Justificativa: o produtor já tem o gate dele
(`EnableHooks` + sha256 do `Assembly-CSharp`, `RealmApiPlugin.cs:21-31`); o kit já recebe autorização por
parâmetro (`CorePluginBinding.cs:14` — "Permission is supplied by trusted host code, never by a
scenario/package"). O adaptador não cria um terceiro lugar onde autorização mora.

### D8 — Thread e exceção: o adaptador **não pode lançar**.

`Signal<T>.Publish` roda **no thread do hook** e o comentário é explícito: "Executa no thread do hook,
nunca despacha Unity em worker" (`Contracts.cs:79`). E o erro de listener é reportado por
`Action<Exception> report` que, na instalação real, é o logger do plugin (`HookInstallation.cs:57`,
`RealmApiPlugin.cs:31`) — ou seja, uma exceção do adaptador viraria log do **produtor**, com a mensagem
inteira (o kit, ao contrário, guarda só o **tipo** da exceção, `RegistryV1.cs:79-84`). Decisão: todo callback
do adaptador tem `try/catch` próprio, sem tocar API do Unity, e o diagnóstico vai para o canal
`Action<string> diagnostic` limitado — o produtor nunca vê exceção do consumidor.

---

## 2. Regra de versionamento única

**Uma regra, quatro fronteiras, o mesmo comportamento: string exata, recusa fechada, sem range, sem
fallback, sem descoberta.**

| # | Fronteira | String conferida | Onde está hoje | Efeito da divergência |
|---|---|---|---|---|
| F1 | extensão → kit | `"1.0.0"` | `RegistryV1.cs:58,92` (`NotSupportedException("API_INCOMPATIVEL: esperado 1.0.0")`) | recusa; `Count` intacto (teste `version`, `Harness/Program.cs:29`) |
| F2 | pacote declarativo → kit | `"1.0.0"` | `scenario-v1.schema.json:9` (`const`), `packages.py:15,51` | erro de pacote, nada é executado |
| F3 | API → jogo | `GameVersion="1.3.1"` **e** sha256 do `Assembly-CSharp` | `Contracts.cs:24-26`, usado em `RealmApiPlugin.cs:29-30` | nenhum hook instalado; API inerte |
| F4 | **adaptador → os dois** | par declarado `KitApi="1.0.0"` + `ProducerVersion="0.1.0"` | **novo** (`RealmHooksExtension`, §D4) | `NotSupportedException` com a mesma string `API_INCOMPATIVEL`; sem inscrição no `RegistryV1` e sem assinatura do `Signal` |

Politica de bump (as duas dimensões sobem por motivos diferentes, e é isso que a unificação precisa
respeitar):

- **Contrato do consumidor (`KitSdk`)**: qualquer mudança de forma ou de semântica em `EventV1`,
  `ReadingV1`, `VerdictV1` ou `IExtensionV1` → `2.0.0`. Todo adaptador compilado contra `1.0.0` passa a ser
  recusado no `Register` (comportamento já provado: `Harness/Program.cs:29`).
- **Contrato do produtor (`RealmApi`)**: `0.1.x` → `0.2.0` quando **só adiciona** hook ao catálogo
  (`Contracts.cs:58-66`); o adaptador tolera `HookId` desconhecido (conta em `hooks.unknown` e **não** emite
  veredito sobre ele). `1.0.0` quando muda a forma de `HookNotification`, remove/renomeia hook ou muda a
  semântica dos parâmetros; aí o adaptador declara o par novo e o antigo é recusado.
- **Nunca**: comparação por prefixo/range, "tenta a versão antiga", leitura da versão do outro lado por
  reflexão, default silencioso. O kit já rejeita 2.0.0 sem registro (`RegistryV1.cs:92` +
  `Harness/Program.cs:29`) e a API já rejeita alvo divergente (`Contracts.cs:24`); o adaptador herda a regra
  em vez de inventar uma terceira.
- **Onde a versão mora no adaptador**: `const` no código, não em `.cfg`/`.json`. Config é entrada não
  confiável e a regra é fail-closed; mover a versão para config abriria exatamente o furo que F1–F3 fecham.

---

## 3. O que esta decisão explicitamente **não** decide (fica para frente própria, se alguém quiser)

1. **Famílias não implementadas** do inventário (`api/docs/contract-inventory.json`: 57 tipos / 271 métodos
   / 143 campos / 50 propriedades / 13 eventos — `counts` no topo do arquivo) continuam "inventário
   inspecionado, não implementação" (`api/README.md:67-68`, citado em `INT-R1-parte01.md`). Nada aqui as
   promove.
2. **Mods que reescrevem resultado** (o postfix do `BetterTooltips` em `OptionsManager.Localize`, que muda
   `__result`) não são migráveis para a API 0.1.0, que é observacional por contrato: isso seria uma
   **extensão de forma** do produtor, frente separada (`docs/automacao/INT-R1-parte05.md:44`).
3. **Input sintético / clique do `AUT4Probe`** (`t_139f714f`, `0xc0000005`): não tocado
   (`INT-R1-parte03.md:20`).
