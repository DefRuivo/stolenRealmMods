# KIT-04R — parte 03: refutações exigidas + parecer por critério

## Refutações explícitas (exigidas pelos critérios de aceitação)

### R1 — Regressão na migração?
**REFUTADO em parte / ACHADO a favor da regressão no artefato novo.**
- O instrumento de origem **não** regrediu: `AUT4Probe.csproj` compila (exit 0) e sua DLL
  mantém o hash `407c5c63…` (idêntico ao declarado nas revisões anteriores do AUT-4).
- Mas a migração **introduziu** uma regressão no Core: o `KIT04Core.csproj` não herdou o
  mecanismo `GameManaged` que o `AUT4Probe.csproj` usa para referenciar
  `UnityEngine.ScreenCaptureModule`. Resultado: o Core não compila (exit 1).

### R2 — Interferência do instrumento no produto?
**REFUTADO.**
- Nenhum `*.csproj` do repositório (mods ou outros) referencia `KIT04Core`/`KIT04Adapter`
  (`grep -rl KIT04 --include=*.csproj` → nenhum fora de `tools/automacao/runtime/KIT04*`).
- Nenhuma DLL do repositório referencia `KIT04Core` (grep binário → nenhuma).
- Perfil r2modman `Default`: nenhum arquivo com "KIT04" (`find` → vazio). Nada instalado.
- `lib/Assembly-CSharp.dll` intacta: `8bb4a7c5…` (mtime preservado).
- O Core é um plugin BepInEx separado (GUID `com.gumatos.kit04.core`), fora de qualquer pacote de mod.

### R3 — Dependência obrigatória dos mods do Core/Adapter?
**REFUTADO para o Core; INDETERMINADO para o Adapter.**
- O Core **não** é dependência dos mods: nada o referencia (R2) e ele não referencia
  `Assembly-CSharp` (0 ocorrências no csproj) — coerente com "Core é ferramenta, não dependência".
- O Adapter não pode ser avaliado: o diretório `KIT04Adapter.SR/` está **vazio**.
  Não há como provar "mods funcionam sem o kit" via adapter — mas também não há adapter a
  depender de nada.

## Parecer por critério

Legenda: OK · ACHADO · FALHOU · INDETERMINADO

### A. Build e empacotamento

| # | Critério | Veredito | Evidência |
|---|---|---|---|
| A1 | Core compila com `-p:DeployToBepInEx=false` | **FALHOU** | `dotnet build` exit 1; 3 erros (parte02 C1) |
| A2 | Erros localizados no caminho de captura | **OK (diagnóstico)** | neutralizar só a captura → exit 0 (parte02 C2) |
| A3 | DLL do Core produzida | **FALHOU** | `bin/Release/` vazio na build entregue |
| A4 | Adapter Stolen Realm existe e compila | **FALHOU** | `KIT04Adapter.SR/` vazio (0 arquivos) |
| A5 | Instrumento de origem intacto | **OK** | AUT4Probe build exit 0; DLL `407c5c63…` |

### B. Contrato (vs `KIT-04-core-especificacao.md`)

| # | Critério | Veredito | Evidência |
|---|---|---|---|
| B1 | Core compila separado do Adapter, sem `Assembly-CSharp` | **FALHOU** (não compila) / sem Assembly-CSharp OK | csproj sem Assembly-CSharp; build exit 1 |
| B2 | Config `_habilitado` **default false** | **FALHOU** | `CorePlugin.cs:129` → `Config.Bind(..., true, ...)`; spec §118 exige false; comentários do próprio arquivo (linhas 13/21) dizem "desabilitada por padrão" — contradição interna |
| B3 | Retorna `{"status":"NAO_EXERCITADO"}` se desabilitado | **ACHADO** | código existe (`ResultadoFinal`, l.108-109) mas inalcançável como default (B2) e não executável (não compila) |
| B4 | Identidade calcula SHA256 da própria DLL | **INDETERMINADO** | `IdentidadeDoCore.cs` (79 linhas) presente; não executado (Core não compila) |
| B5 | `LerComponentes<T>()` retorna null se ausente | **ACHADO** | `CorePlugin.cs:78` retorna `Array.Empty<T>()`, não `null` (spec §89 pede null) |
| B6 | `CapturarPNG` retorna false se módulo indisponível | **ACHADO** | presente (l.224-225) mas é justamente o caminho que não compila |
| B7 | Eventos em lista estruturada | **OK (estático)** | `EventosImpl` com `List<Dictionary<string,object>>` |
| B8 | JSON sem dependências externas | **OK (estático)** | `Json.cs` (158 linhas), reuso do padrao AUT4Probe |
| B9 | Interface `IComponentReader<T>` conforme spec | **OK** | `IComponentReader.cs` bate com a spec (LerTodos/LerPorNome/LerPorTag/Inventariar) |
| B10 | Interface `ICoreIdentidade` existe | **ACHADO** | spec lista `ICoreIdentidade.cs`; entregue como classe estática `IdentidadeDoCore.cs` (contrato divergente) |

### C. Entrega / documentação

| # | Critério | Veredito | Evidência |
|---|---|---|---|
| C1 | Contrato v1.0.0 | **ACHADO** | spec diz "v1.0.0" no objetivo; arquivos usam `0.1.0`; spec "aguarda implementação" |
| C2 | Matriz de compatibilidade (Unity 2022.3.62f3 / BepInEx 5.4.23.5 / API 0.1.0) | **ACHADO** | só em prosa no entregável; sem matriz |
| C3 | Plano de migração backward-compatible | **ACHADO** | ausente em `docs/automacao/KIT-04-*` |
| C4 | Schemas JSON válidos | **ACHADO** | nenhum schema do KIT-04 entregue |
| C5 | Hashes SHA256 reais de todos os documentos/fontes | **FALHOU (evidência fabricada)** | ver abaixo |
| C6 | Itens do entregável concluídos | **FALHOU** | `KIT-04-entrega.md`: 2 marcados `[x]`, 13 `[ ]`; "Status: INICIADO" |

#### C5 — detalhe (evidência fabricada no entregável)

`KIT-04-entrega.md` §"Comando 3: Hash SHA256" e §"Comando 4/5" declaram, como "saídas reais":

```
IdentidadeDoProbe.cs: d41d8cd98f00b204e9800998ecf8427e   (verificar com sha256sum real)
Json.cs:              e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
LeituraAgregados.cs:  hash a calcular
```

- `d41d8cd98f00b204e9800998ecf8427e` é o **MD5 de entrada vazia** (nem é SHA256);
- `e3b0c442…b855` é o **SHA256 de entrada vazia** (confirmado: `printf '' | sha256sum`).

Hashe mínimo real (medido por mim):

```
c23574f324f7a70ddeb2edb484daf292ebd92fc07eb0304bfbf343e58d27bfa6  IdentidadeDoProbe.cs
ae30a1ac059bcf62067047926c13bf43079b30552073540a2f5654551b6b32c6  Json.cs
2506ec6478dd5a6bd445f2726c6595015f877f5e6465201d10c12a439c36cab0  LeituraAgregados.cs
```

Ou seja: a seção "Saídas reais dos comandos executados" do entregável **não é real** —
contém hashes de placeholder. Isso é ACHADO de integridade de evidência, não apenas de forma.

## Veredito

**REPROVADO.** O escopo "KIT-04" não fecha nem o critério mais básico (build) e o adapter
anunciado não existe como arquivo. Os únicos elementos corretos são os componentes
reutilizados (Json, IComponentReader, ICoreSession, eventos) — e ainda assim com desvios de
contrato (default `true`, retorno `Array.Empty` vs `null`).

## Limitações desta revisão (declaradas)

- Runtime em jogo: **NÃO EXERCITADO** (fora de escopo; sem autorização).
- Não reexecutei a suíte offline do AUT-4 (é outro entregável; a refutação R1 usa build + hash).
- Independência é por **run/sessão**: só existe o perfil `default` no ambiente.
