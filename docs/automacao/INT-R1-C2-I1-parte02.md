# INT-R1-C2-I1 — parte 02: o AUT4Probe consumindo pelo hook (entregável B)

Cartão `t_a706b09c`, mesmo cartão da parte 01. Aqui está o que mudou no instrumento, a **medição de
cobertura** que a parte 03 do cartão pai pediu, e o aceite por leitura/diff.

---

## 1. A medição que a parte 03 pediu (feita, não presumida)

`NAO_EXERCITADO` no pai: "quantos overloads de `OptionsManager.Localize` existem em
`lib/Assembly-CSharp.dll`". Medido nesta rodada, com duas ferramentas independentes:

```
dotnet build api/tools/Inspect/Inspect.csproj -c Release
dotnet api/tools/Inspect/bin/Release/net6.0/Inspect.dll targets lib/Assembly-CSharp.dll   # 'targets' filtra por NOME
ilspycmd lib/Assembly-CSharp.dll -t OptionsManager
```

Resultado (evidências: `…/inspect-targets-optionsmanager.json` e
`…/ilspycmd-optionsmanager-localize.txt`; `lib/Assembly-CSharp.dll` sha256
`8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`, o mesmo do `ApiIdentity`):

| Achado | Valor |
|---|---|
| Métodos com o nome `Localize` no tipo `OptionsManager` | **1** |
| Assinatura dele | `public static string Localize(string original, LanguageGender languageGender = …, Gender characterGender = …)` |
| Outros nomes parecidos (não são o alvo) | `LocalizeEnum<T>(…)`, `LocalizeUI(bool force = false)` |

**Consequência declarada (e ela corrige a premissa do pai):** `GanchoTodos("OptionsManager","Localize")`
**não** pegava "todos os overloads" — pegava **o único** que existe, que é **exatamente** a assinatura
declarada pelo hook `ui.localized` (`api/Core/Contracts.cs:63`). Ou seja: trocar o patch próprio do probe
pelo evento da API **não muda a cobertura**, porque não havia overload nenhum a mais para cobrir. O que
muda é **quem instala o patch daquele alvo** — passa a ser a API (dona do alvo), e não o instrumento.
Nada aqui é escondido: se existissem N>1 overloads, a cobertura cairia para 1 e isso estaria escrito.

## 2. As 5 edições no `AUT4ProbePlugin.cs`

Antes: 1957 linhas (`wc -l`), md5 `d30997fcdc8c79af7dfdd42521dd6b0f`. Depois: **2008 linhas**, sha256
`6d8a3205075c54553765471f1372b0016bf5f4915b320698601da3c208e95ced`. Nada de reformatação.

| # | Onde (depois) | O que | Natureza |
|---|---|---|---|
| 1 | `:77-85` | campos `_ponteApiCfg` (config nova) e `_ponteApi` (ligação opcional) | adição |
| 2 | `:214-218` | `Config.Bind("Geral","PonteApiHook", false, …)` — **default FALSE** | adição |
| 3 | `:265-271` | `GanchoTodos("OptionsManager","Localize")` **SAIU**; entrou `LigarPonteOpcional()` (com o motivo escrito no próprio código) | substituição |
| 4 | `:327-367` | `GanchoTodos(...)` (que ficou morto) → `LigarPonteOpcional()`: `Assembly.Load("Gumatos.KitApiBridge.AUT4")` por NOME EXATO, dentro de `try/catch`, atrás da config | substituição |
| 5 | `:643-646` | `Finalizar()` desfaz a ponte (`Dispose` idempotente) | adição |

Prova do diff linha-local (o arquivo **já estava sujo por outros cartões** — hotspot registrado no
cartão pai — então `git diff` mistura cartões e não isola este): a inversa exata das 5 edições foi
aplicada por âncora e está em
`docs/automacao/INT-R1-C2-I1-evidencias/AUT4ProbePlugin-pre-edicoes.cs.txt`, com o diff em
`…/edicoes-aut4probe.diff` (**5 hunks**, +62/−10). Limite declarado dessa reconstrução: ela difere do
pré-edição real em **uma linha** — a linha em branco entre `_dir = _outDir.Value;` e
`_orcamentoSeg = _orcamento.Value;`, que a edição #2 consumiu; por isso o hunk 2 aparece com um
`+1/−1` a mais do que a edição real. Os outros 4 hunks são exatos.

O que **não** foi tocado (blocos "fica"/"INTACTO" da parte 03): `_harmony` (:262), `Gancho("GUIManager",
"Update")` (:264), `InstalarNoPlayerLoop` (:268-296), `PostfixDoGancho` (:387), `Aplicar` (:369), o motor
por quadro, a coleta por reflexão e o clique/navegação (`t_139f714f`).

## 3. Aceite por leitura/diff

1. **Nenhuma chamada de patch em `Localize` restante.** `grep -n "OptionsManager" AUT4ProbePlugin.cs`
   devolve 4 linhas, nenhuma delas é patch: `:78` e `:217` (comentário/config), `:265` (comentário do
   que saiu) e **`:1006`**, que é a tabela `FUNIS` (`:1004-1010`) usada por `OwnersDosFunils()` — ela
   **lê** os donos Harmony do método para o inventário do JSON; não instala nada. `GanchoTodos` não
   existe mais como método (verificado por `grep`).
2. **Diff linha-local**: ver §2.
3. **Config `false` (default) e sem companheiro ⇒ saída de hoje.** Por leitura: `LigarPonteOpcional()`
   retorna na primeira linha (`if (!_ponteApiCfg.Value) { Marco(...); return; }`), sem tocar em
   `Assembly.Load`; e, mesmo com `PonteApiHook=true`, a ausência do companheiro cai no `catch` que só
   registra `Marco`/`LogWarning`. Não há novo campo no JSON de saída, nenhum marco obrigatório novo e
   nenhuma leitura a mais — o único acréscimo é `_passos["ponte_api"]` no `Finalizar`. Rodada em jogo:
   **NAO_EXERCITADO** (este cartão não abre o jogo); a comparação com `docs/automacao/AUT-4-evidencias/`
   fica para a rodada autorizada.
4. **Arquivo relido imediatamente antes de cada edição**: cada `patch` foi aplicado contra o conteúdo
   lido na hora; o arquivo não mudou sob meus pés durante a rodada (1957 → 2008 = exatamente as 5 hunks).

## 4. O companheiro (por que ele existe e o que ele prova)

`tools/automacao/runtime/AUT4Probe/Companheiro/` — projeto **separado**, `netstandard2.1`, **sem Unity e
sem BepInEx**, `AssemblyName=Gumatos.KitApiBridge.AUT4`, referências `kit13/SDK/KitSdk.csproj` e
`kit13/ApiBridge/ApiBridge.csproj`. `PonteAut4.Ligar(Action<string> observacao, Func<string> sessao,
Func<bool> produtorAtivo)` (assinatura fixada: o probe resolve por nome e tipos exatos) registra a
testemunha do instrumento no `RegistryV1` (`id "aut4.probe"`), cria o adaptador com
`RealmHooks.Observed` e devolve um `IDisposable` que desfaz tudo (adaptador → lease → registry).
Build medido: **0 avisos / 0 erros**.

`AUT4Probe.csproj` ganhou `<Compile Remove="Companheiro/**" />` — sem isso o globbing padrão compilaria
`PonteAut4.cs` dentro do instrumento (o companheiro é carregado em runtime, não é referência dura).

**Por que `Assembly.Load` aqui e não na ponte do kit:** a nota
"No assembly loading, script execution, authorization" (`SDK/RegistryV1.cs:47-48`) protege o contrato de
**extensões do kit**; o probe é instrumento de bancada e uma referência dura o deixaria sem carregar
sempre que a API não estivesse instalada. O load é por **nome exato**, sem varredura, sem sondagem de
versão; ausente = comportamento de hoje.

**Thread:** o gatilho chega no mesmo thread em que o postfix do probe chegava (o `Signal` publica no
thread do hook — `api/Core/Contracts.cs:79`), então o despacho de `Tick` não muda de natureza.

## 5. Prova executada do caminho de consumo (P17)

O companheiro **não** referencia Unity/BepInEx, então o caminho de consumo roda offline e é exercitado
pela própria suíte: **P17** (`ApiBridgeHarness/Program.cs`) liga a `PonteAut4`, emite `ui.localized`
pelo caminho do produtor (`RealmHooks.Emit`), e mede: o gatilho chega uma vez com o `HookId` e
`quadro=0`; hook fora do catálogo **não** vira gatilho; `producerActive()==false` **não** vira gatilho;
`Dispose` (duas vezes) desliga e nada mais chega; diagnóstico vazio na operação normal. Saída da suíte:
`Ran 17 tests; failures=0` (parte 01).

## 6. NAO_EXERCITADO desta parte (com motivo)

- Ponte ligada **dentro do jogo**, com a API instalada e `EnableHooks=true`: **NAO_EXERCITADO** — exige
  instalação no perfil e jogo aberto (proibido neste cartão).
- Clone do companheiro + `ApiBridge.dll` + `KitSdk.dll` + `RealmApi.Core.dll` no `BepInEx/plugins` e o
  `Assembly.Load` resolvendo de verdade: **NAO_EXERCITADO** (mesma razão: é deploy).
- Rodada em jogo comparando a saída do probe com `docs/automacao/AUT-4-evidencias/`: **NAO_EXERCITADO**
  — a igualdade de saída com a ponte desligada foi conferida **por leitura de código** (§3.3).
