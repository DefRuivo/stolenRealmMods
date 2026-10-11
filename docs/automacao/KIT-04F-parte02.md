# KIT-04F — parte 02: contrato v1.0.0, matriz de compatibilidade, migração e schemas

Tarefa `t_d5c98d36` (KIT-04F) · 2026-10-09 · offline. Cobre o **item 5** do parecer KIT-04R
("versão do contrato coerente, matriz de compatibilidade, plano de migração e schemas JSON").

Regra desta parte: tudo que aparece aqui foi conferido contra o **código no disco**, não contra
a especificação (`KIT-04-core-especificacao.md`) — onde os dois divergirem, a divergência está
declarada como **desvio**, não escondida.

## 1. Versão do contrato

**Contrato do Core KIT-04 = v1.0.0** (versionamento semântico MAJOR.MINOR.PATCH).
`MAJOR` = quebra de assinatura de interface; `MINOR` = acréscimo compatível; `PATCH` = correção.
Todos os artefatos do Core carregam `[BepInPlugin("com.gumatos.kit04.core", …, "0.1.0")]`;
o `0.1.0` é a versão do **plugin/assembly**, o `1.0.0` é a versão do **contrato de interfaces**.
Os dois números são independentes e é essa a confusão que o parecer apontou como ausente.

## 2. Interfaces entregues (o que existe, como está)

| Interface | Arquivo | Assinatura implementada | Situação |
|---|---|---|---|
| `ICoreSession` | `ICoreSession.cs` | `Registrar(string,string,string)`, `ObterIdSessao()`, `EstaAtiva()` | igual à spec |
| `ICoreEvento` | `ICoreEvento.cs` | `RegistrarEvento(string,string,Dictionary<string,object>?=null)`, `ObterEventos()`, `LimparEventos()` | igual à spec |
| `ICoreIdentidade` | `ICoreIdentidade.cs` | `CalcularIdentidade(string)`, `CalcularHashSha256(string)` | **criada no KIT-04F** (o KIT-04 entregou só a classe estática — achado B10 do parecer) |
| `IComponentReader<T>` | `IComponentReader.cs` | `T[]? LerTodos()`, `T[]? LerPorNome(string)`, `T[]? LerPorTag(string)`, `Inventariar(int)` | **desvio declarado** (ver §2.1) |
| `IPictureCapture` | `IPictureCapture.cs` | `CapturarPNG(string,int,int)`, `EstaDisponivel()`, `ObterUltimaCaptura()` | igual à spec |

Implementações concretas: `CorePlugin` (BepInEx), `SessionImpl`/`EventosImpl`/`PictureCaptureImpl`
(internos de `CorePlugin.cs`), `ComponentReaderImpl<T>` (**criada no KIT-04F** — antes
`IComponentReader<T>` não tinha implementação alguma, era interface vestigial),
`IdentidadeDoCoreImpl` (delega para o serviço estático `IdentidadeDoCore`).

### 2.1 Desvios declarados em relação à especificação

1. **`IComponentReader<T>` retorna `T[]?` (nullable), não `T[]`.** A spec (§"Ler componentes") manda
   retornar `null` quando o componente não existe, mas a assinatura não-nulável tornava isso
   inexprimível — era exatamente a incoerência do achado B5. Com `Nullable enable`, `T[]?` é a
   única forma de o contrato expressar "AUSENTE ⇒ null". Regra dura do leitor:
   **array vazio é proibido** (não distingue "não existe" de "existe e é vazio").
2. **Identidade como classe estática + adaptador de instância.** `IdentidadeDoCore` continua
   estático (código provado, reusado do AUT4Probe); a interface `ICoreIdentidade` é satisfeita por
   `IdentidadeDoCoreImpl`, exposto em `CorePlugin.Identidade`. Nada de "interface sem implementação".
3. **`CapturarPNG` ignora `largura`/`altura`** (parâmetros mantidos por contrato, mas a captura usa
   a resolução do frame via `ScreenCapture.CaptureScreenshotAsTexture()`). Comportamento da spec,
   assinatura preservada — registrado aqui porque o parecer cobrou coerência.

## 3. Matriz de compatibilidade

| Componente | Versão | Papel | Situação |
|---|---|---|---|
| Unity (Stolen Realm) | 2022.3.62f3 | runtime do jogo | alvo do adapter; **não exercitado** nesta rodada |
| BepInEx | 5.4.23.5 | host do plugin (Mono) | `BepInEx.dll` vindo de `lib/` |
| Harmony (`0Harmony`) | embarcado no BepInEx | hooks do adapter | `lib/0Harmony.dll` |
| biblioteca-de-terceiros | 0.1.0 | API do jogo | **não referenciada** pelo Core nem pelo adapter |
| `Assembly-CSharp` (jogo) | build atual | só o adapter toca | `lib/Assembly-CSharp.dll`, `Private=false` |
| .NET SDK de build | 6.0.428 | compilador | `TargetFramework` = `netstandard2.1` |
| `UnityEngine.ScreenCaptureModule` | pasta `Managed` do jogo | captura PNG | via `$(GameManaged)` |
| `UnityEngine.ImageConversionModule` | pasta `Managed` do jogo | `EncodeToPNG` | via `$(GameManaged)` |

O Core **não** depende de `Assembly-CSharp`, de `biblioteca-de-terceiros` nem do jogo — só o adapter.
Prova: nenhum `csproj` do produto referencia `KIT04*` (verificado por busca no repositório).

## 4. Plano de migração backward-compatible

O KIT-04 refatora o `AUT4Probe` (instrumento) em Core genérico + adapter SR. O AUT4Probe **não é
consumido por nenhum mod** (verificado no parecer: nenhum csproj/DLL do produto o referencia),
então não há consumidor externo a quebrar — a migração é interna ao kit.

| Estágio | Passo | Regra de compatibilidade | Rollback |
|---|---|---|---|
| 0 | Estado atual: `AUT4Probe/` intacto (DLL `407c5c63…`) | — | — |
| 1 | Core `KIT04Core` (novo, opt-in `habilitado=false`) | não altera nada do AUT4Probe | apagar `KIT04Core/` |
| 2 | Adapter `KIT04Adapter.SR` (novo, opt-in `habilitado=false`) | `ProjectReference` para o Core; sem efeito com o kit desligado | apagar `KIT04Adapter.SR/` |
| 3 | Coexistência: AUT4Probe **e** KIT04 no disco, ambos desligados por padrão | nenhum conflito de GUID (`com.gumatos.aut4probe` ≠ `com.gumatos.kit04.*`) | desabilitar no `.cfg` |
| 4 | Substituição (fora do escopo do KIT-04F) | só com rodada autorizada em jogo e equivalência provada | manter AUT4Probe |

**Regra de aceitação de schema (reusada do KIT-02):** `schema_version <= 1.0.0` → processa;
`schema_version > 1.0.0` → modo seguro + log; desconhecida → rejeita com erro claro e hash.
Ninguém "adivinha" o formato.

## 5. Schemas JSON

Os schemas do kit já existem em `docs/automacao/schemas/` (criados pelo KIT-02) e são
estruturalmente válidos — verificados por parse nesta rodada:

| Schema | Versão | Hash SHA256 |
|---|---|---|
| `evento-v1.json` | 1.0.0 | `77e26af5d412257833a0e4b9c4e473b73eaf14e6048be418e41e22b9d51a3998` |
| `cenario-v1.json` | 1.0.0 | `c6f0724232b8f8a3956c71b3701d7f5f2374fb44ce46d4cb3b7d6b119adc7c52` |
| `sessao-v1.json` | 1.0.0 | `ce896f91c69910bf8ff60bfcf6b17dd6d01a947854c782fd5ec0d76517adbbf7` |

**Novo no KIT-04F:** `docs/automacao/schemas/core-resultado-v1.json` — formaliza o objeto que o
Core devolve em runtime (`CorePlugin.ResultadoFinal()`), que até então só existia como código.
Sem ele, o "contrato v1.0.0" seria prosa sem forma verificável.

### O que é INDETERMINADO (declarado, não escondido)

- O **conteúdo real** das telas/personagens que o adapter coleta em jogo é **INDETERMINADO**:
  exige rodada autorizada do AUT-4 (jogo aberto). O que se prova offline é que o adapter compila,
  liga no Core e fica inerte com `habilitado=false`.
- A **equivalência numérica** Core+Adapter vs. `runtime/out/ex1-offline.json` (prometida pela spec
  §"Equivalência provada") é **INDETERMINADA** pela mesma razão: sem execução em jogo não há saída
  para comparar. Declarado aqui para não passar por verde.
