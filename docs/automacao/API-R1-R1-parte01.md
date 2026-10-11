# API-R1-R1 — parte 01: revisão independente da API-base (rodada 1)

Tarefa: `t_d87ea54d` (API-R1-R1), filha de API-R1 (`t_b7f6fc4a`). Repo auditado: `C:/dev/stolen-realm`.
Quem revisa é outra run, não a implementadora; **nenhum arquivo de implementação foi editado** nesta tarefa.
Este arquivo é NOVO (não existia `docs/automacao/API-R1-R1-*` antes desta rodada).

Contexto da rodada: as 3 tentativas anteriores desta tarefa morreram em `rate_limited` (exit 75) sem
produzir nada; esta é a 4ª. O material auditado é o estado do repo nesta rodada, que já inclui a
contribuição da filha API-R1-I1 (`t_f32becd0`) no `api/Plugin/RealmApi.csproj`.

Escopo autorizado: revisão apenas. **Runtime em jogo NÃO autorizado** (o jogo não foi aberto); sem
publicação; `execute_code` não usado.

---

## 0. Reprodução própria (o que eu rodei, com resultado real)

| Comando | Resultado medido nesta rodada |
|---|---|
| `dotnet --version` | `6.0.428` |
| `dotnet build api/Core/RealmApi.Core.csproj -c Release` | 0 Aviso(s), 0 Erro(s) |
| `dotnet build api/Hooks/RealmApi.Hooks.csproj -c Release` | 0 Aviso(s), 0 Erro(s) |
| `dotnet build api/Plugin/RealmApi.csproj -c Release` | 0 Aviso(s), 0 Erro(s) |
| `dotnet build api/Smoke/RealmApi.Smoke.csproj -c Release` | 0 Aviso(s), 0 Erro(s) |
| `dotnet build api/tools/Inspect/Inspect.csproj -c Release` | 0 Aviso(s), 0 Erro(s) |
| `api/Smoke/bin/Release/net472/RealmApi.Smoke.exe C:/dev/stolen-realm/lib/Assembly-CSharp.dll C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll` | `Ran 25 tests; failures: 0`, **exit 0** |
| `diff` da saída acima contra `api/docs/smoke-output.txt` | **IDENTICO** (byte a byte, 25 PASS + linha de NAO_EXERCITADO) |
| `grep -ril -E 'biblioteca-de-terceiros\|biblioteca-de-terceiros' api/ docs/automacao/API-R1-*.md` | **0 arquivos** (exit 1) |
| `dotnet run --project api/tools/Inspect/Inspect.csproj -c Release -- targets lib/Assembly-CSharp.dll` | roda (exit 0) e o JSON gerado é **byte-idêntico** a `api/docs/game-targets.json` (diff vazio) |
| `sha256sum lib/Assembly-CSharp.dll` | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |
| `sha256sum <jogo>/Stolen Realm_Data/Managed/Assembly-CSharp.dll` | **mesmo hash** (7712768 bytes) — identidade do alvo confirmada fora do repo |
| `grep -a 'buildid' appmanifest_1330000.acf` | `25240684` (appid `1330000`) |
| `grep -a -o -E '2022\.3\.[0-9a-f.]+' globalgamemanagers` | `2022.3.62f2` |
| `grep -a -o -E '1\.3\.[0-9]' globalgamemanagers` | `1.3.1` |
| `sha256sum api/Plugin/.../RealmApi.dll` (após rebuild nesta rodada) | `b52b66e5ce85149a624c8f09e695c3fb2d90ebf3f9746e068e727c68811d822c` — **igual** ao declarado na `API-R1-parte06.md` §1 |
| `find <perfil r2modman>/plugins -newermt "2026-10-11 00:00"` | vazio |
| `ls <perfil>/config \| grep -i realm` | nada (`RealmApi` **não** existe no perfil: nem plugin, nem `.cfg`) |

Os 5 builds são incrementais (o repo já tinha `obj/`/`bin/` da rodada da implementadora), mas o
`RealmApi.dll` reconstruído sai com o **mesmo SHA-256** da rodada anterior, então o binário conferido é o
mesmo objeto auditado.

---

## 1. LENTE CONTRACT — a base promete só o que cumpre?

### 1.1 Catálogo × `api/docs/game-targets.json`

`HookCatalog.All` (`api/Core/Contracts.cs:60-65`) tem exatamente 4 descritores. Comparei campo a campo com
o metadado real do assembly instalado (`api/docs/game-targets.json`, regerado por mim — byte-idêntico):

| HookId | Descritor (Contracts.cs:61-64) | `game-targets.json` | Veredito |
|---|---|---|---|
| `game.awake` | `Burst2Flame.Game::Awake`, `isStatic=false`, `System.Void`, 0 params | `System.Void Burst2Flame.Game::Awake()`, `isStatic:false`, `parameters: []` | bate |
| `ui.skill-tree.updated` | `SkillTreeManager::UpdateSkillTreeItems`, `false`, `System.Void`, 0 params | `System.Void SkillTreeManager::UpdateSkillTreeItems()`, `false`, `[]` | bate |
| `ui.localized` | `OptionsManager::Localize`, **`true`**, `System.String`, (`System.String`, `LanguageGender`, `Gender`) | `System.String OptionsManager::Localize(System.String,LanguageGender,Gender)`, `isStatic:true`, params `original:System.String`, `languageGender:LanguageGender`, `characterGender:Gender` | bate |
| `combat.turn-started` | `GameLogic::StartNewTurn`, `false`, `System.Void`, 0 params | `System.Void GameLogic::StartNewTurn()`, `false`, `[]` | bate |

**4/4 batem** em tipo exato (FullName), `isStatic`, retorno e lista de parâmetros na ordem. Não há
descrição prometendo hook que não exista no assembly, nem o inverso (`game-targets.json` lista outros
métodos de `Character` — `ModifyHealth` 5 e 8 params, `PerformAction` ×2, `ProcessDeath`,
`ProcessSkillTriggers` — que **não** são hooks; eles estão lá como material de referência para as famílias
futuras, e o README é explícito em que essas famílias "**não estão implementadas**" e "não há promessa de
compatibilidade" (`api/README.md:67-68`).

`HookDescriptor.Resolve` (`Contracts.cs:46-54`) é honesto sobre o próprio alcance: `assembly.GetType`
com `throwOnError:false` e `ignoreCase:false` (sem *short name*), filtro por `FullName` de tipo de retorno
e `SequenceEqual` da lista de tipos de parâmetro, `DeclaredOnly` (não procura em hierarquia nem em outros
assemblies), e exige **exatamente 1** match (`if (matches.Length!=1) throw MissingMethodException`).

### 1.2 Gate `ApiIdentity.Matches` é fail-closed?

`Contracts.cs:24-26`: `string.Equals(version, GameVersion, Ordinal) && string.Equals(sha256, AssemblySha256, OrdinalIgnoreCase)`.

- `null` em qualquer lado → `false` (não lança, não aceita) — coberto por `identity-null-fails-closed`.
- String vazia → `false`.
- Divergência em qualquer dos dois → `false`; só o par (versão, hash) correto passa.
- Testes negativos no smoke: `identity-wrong-version` (1.3.2) e `identity-wrong-hash` (64 zeros).

Ligação do gate no plugin (`api/Plugin/RealmApiPlugin.cs`): `Safety.EnableHooks` default **`false`** (:21)
→ `return` antes de qualquer coisa; com `true`, hasheia o assembly **do processo atual**
(`game.Location`, :27-28) e chama `Matches` (:29); divergência → `LogError` + `return` com
`installation` nula. Qualquer exceção do bloco (ex.: `Single()` não achar Assembly-CSharp, IO no
`File.OpenRead`) é capturada em :35 e vira `LogError`, sem instalar. **Fail-closed confirmado no código.**

### 1.3 O README nega explicitamente o que não foi implementado?

Sim, em dois lugares: `api/README.md:67-68` (famílias do inventário não implementadas, "não há stub
silencioso") e `api/README.md:151-159` (seção "NÃO exercitado nesta entrega": runtime BepInEx, deploy no
perfil, famílias restantes, publicação). `api/docs/README.md` fecha com "Nenhum documento nesta pasta
declara suporte às famílias ainda não implementadas". A promessa observacional (nunca cancela/reescreve
argumento ou resultado) está em `api/README.md:42` e é estruturalmente verdadeira: `Signal.Publish` e
`RealmHooks.Emit` são `internal` (`Contracts.cs:91,109`), então o consumidor **não tem API** para publicar
evento nem para alterar `__args`/`__result`.

**Lente 1: sem achado bloqueante.** Uma imprecisão de documentação na tabela de identidade → achado **D3**.

---

## 2. LENTE HONESTIDADE DA PROVA

- **O smoke prova o que diz provar?** Ele separa explicitamente três coisas: (a) mecânica no CLR com
  fixtures, (b) metadados do alvo real (`actual-game-hook-metadata`, via Mono.Cecil sobre
  `lib/Assembly-CSharp.dll`), (c) hash do assembly real (`actual-game-hash`). O que ele **não** prova —
  disparo dos postfixes no Unity/BepInEx — está declarado na própria saída do programa
  (`NAO_EXERCITADO: ...`), em `api/docs/smoke-result.json` (`scope.notExercised`) e em `api/README.md:113-114`.
- **Fixtures declaradas como artificiais?** Sim, em 4 lugares independentes: comentário do fonte
  (`api/Smoke/Program.cs:93`), `api/docs/smoke-result.json` → `fixturesNotice`, `api/docs/README.md` e
  `api/README.md:113-114`. O teste `exact-qualified-type` (`Program.cs:30`) até declara uma classe
  `Game` no namespace global (`Program.cs:94`) para provar que o resolve **não** usa nome curto.
- **`Ran 25 tests; failures: 0` é reproduzível pelo comando do README?** Sim — o comando de
  `api/README.md:103-105` foi copiado tal como está e deu exit 0 com 25 PASS; a saída é byte-idêntica ao
  `api/docs/smoke-output.txt` versionado.
- **Algum número de documento está estimado em vez de medido?** Varri os artefatos:
  - `API-R1-parte02.md` havia estimado o ZIP em 146.883 bytes e a `parte03.md` **corrigiu para 146.843**
    ("NÃO 146.883", medido por `stat().st_size`). Erro assumido e corrigido por escrito — honesto.
  - `parte06` §2: as 5 contagens do inventário (57 tipos / 271 métodos / 143 campos / 50 propriedades /
    13 eventos) **conferem com o próprio JSON** — recomputei somando os arrays de
    `api/docs/contract-inventory.json` e os totais batem exatamente com o bloco `counts`.
  - `parte06` §1: SHA-256 do `RealmApi.dll` da rodada (`b52b66e5…`) — **reproduzido** por mim no rebuild.
  - `parte04`: SHA-256 do Harmony `lib` = perfil (`1a21cc03…`) — **reproduzido** por mim.
  - Nenhum número lido foi achado como estimativa apresentada como medida.

**Lente 2: sem achado bloqueante.** Um documento ficou desatualizado depois de uma tarefa filha → **D2**.

---

## 3. LENTE HARMONY

`api/Hooks/HookInstallation.cs` (69 linhas) analisado linha a linha:

| Pergunta | Onde | Veredito |
|---|---|---|
| `Dispose` remove só o próprio owner? | `:63` `harmony.UnpatchSelf()` (owner = `ApiIdentity.Guid`, `:31` do plugin) | sim — e a prova é empírica: `foreign-owner-preserved` (`Program.cs:78-85`) instala um postfix de outro `Harmony("…smoke.foreign")` e confirma, **depois** do `Dispose`, que `GetPatchInfo(method).Owners.Contains(other.Id)==true` |
| `Dispose` é idempotente? | `:61-62` flag `disposed` + `Interlocked`-free early return | sim; `real-harmony-hooks-dispatch-and-cleanup` chama `Dispose()` **duas vezes** (`Program.cs:75`) e depois invoca `StartNewTurn()` verificando que **não** houve nova notificação (`received.Count==4`) |
| Alvo ausente/duplicado deixa **zero** patches? | `:25` resolve **todos** os descritores (`.ToArray()`) antes de criar sessão/patchar; `:26-27` checa IDs e `MethodBase` duplicados antes; `:34-44` só então patcha, dentro de `try/catch { session.Dispose(); throw; }` (`:47`) | sim — nada é aplicado antes da validação completa, e a rede de segurança desfaz patches parciais. `missing-target-zero-patches` (`Program.cs:57-60`) prova: Install com 1 válido + 1 ausente lança `MissingMemberException` e **nenhum** owner fica no método válido; `duplicate-target-rejected` (`:61`) prova o mesmo para alvo repetido |
| Owner de terceiros sobrevive? | `UnpatchSelf` só remove o `Id` desta instância | sim (teste acima) |
| Resolução recusa overload ambíguo? | `Contracts.cs:50-52`: match por nome **e** `IsStatic` **e** `ReturnType.FullName` **e** `SequenceEqual` dos tipos de parâmetro; `matches.Length!=1` → `MissingMethodException` | sim, por construção. Observação: o repositório testa "0 matches" (`absent-target-rejected`) e "assinatura errada" (`wrong-signature-rejected`), mas **não** há caso de teste para "2 matches". Em C# dois métodos não podem diferir só pelo retorno, então o caso é praticamente inatingível por IL compilado por C# — é uma lacuna residual de teste, não um defeito (ver OBS-2) |
| Formas de postfix suportadas são as prometidas? | `:29-31` só aceita (instância + `System.Void`) ou (estático + `System.String`); qualquer outra forma → `NotSupportedException` antes de patchar | sim; o README (`:140-142`) declara que forma diferente "exige decisão de arquitetura" |

Detalhe adicional conferido: `Notify` (`:53-58`) só emite se a sessão está `active` **e** o `MethodBase`
está no dicionário `installed` — depois do `Dispose` (`active=null`, `installed.Clear()`) não há emissão
fantasma, o que é exatamente o que o teste do `Dispose` duplo mede.

**Lente 3: limpa.** Nenhum achado.

---

## 4. LENTE ISOLAMENTO E LIMITES

- **Vazamento do mod antigo:** `grep -ril -E 'biblioteca-de-terceiros|biblioteca-de-terceiros' api/ docs/automacao/API-R1-*.md`
  → **0 arquivos**. Ampliei a busca: `StolenRealmMod`, `ModAPI`, `CustomModAPI`, `com.StolenRealm` → 0 cada;
  o único hit de `Modding` em `api/` é a **palavra genérica** na linha 1 do README ("API de **modding**
  própria"), não o nome do pacote. Os únicos GUIDs citados em `api/` são `com.gumatos.realmapi` e os 4
  sufixos de fixture do smoke (`.smoke.dup/.foreign/.missing/.second`) — todos nossos.
- **Inventário anonimizado:** recomputei os 57 nomes de tipo de `api/docs/contract-inventory.json`:
  **57/57** começam por `Gumatos.RealmApi.ContractReference`. O `Inspect` faz a neutralização em
  `Program.cs:11-18` (mapeia o tipo base de plugin, o tipo com `BepInPlugin` e o nome do assembly);
  `sourceSha256` é hash, não nome.
- **Assembly do jogo não referenciado em tempo de compilação:** nenhum `.csproj` de `api/` referencia
  `Assembly-CSharp` (grep em `api/*/*.csproj` e `api/tools/Inspect/*.csproj`). As referências externas são
  `0Harmony`, `BepInEx`, `UnityEngine`, `UnityEngine.CoreModule` (motor/loader, com `<Private>false</Private>`)
  e, em Smoke/Inspect, `Mono.Cecil`/`MonoMod.*`/`BepInEx` do core do r2modman. Independente do teste
  `no-game-assembly-dependency`, rodei `Inspect plugin api/Plugin/bin/.../RealmApi.dll`: `assemblyReferences`
  = `netstandard 2.1`, `BepInEx 5.4.23.5`, `RealmApi.Hooks`, `UnityEngine.CoreModule`, `RealmApi.Core` —
  **sem** `Assembly-CSharp`.
- **Assembly do jogo não redistribuído:** `lib/` está no `.gitignore` (linha 3) e `git ls-files lib/` está
  vazio — inclusive `Assembly-CSharp.dll`, que é apenas lido (hash/metadados) do disco da máquina.
- **Nenhum deploy/publish:** `Directory.Build.props` da raiz define `DeployToBepInEx=false` por padrão, e o
  alvo em `api/Plugin/RealmApi.csproj:29` só roda com `Condition="'$(DeployToBepInEx)' == 'true'"`. Nesta
  rodada rodei os 5 builds **sem** a flag.
- **Perfil r2modman intocado:** nenhum arquivo em `plugins/` com data ≥ 2026-10-11 00:00; não existe pasta
  `RealmApi` em `plugins/` nem `com.gumatos.realmapi.cfg` em `config/`.

**Lente 4: limpa.** Uma observação de higiene de repositório → **OBS-1**.

---

## 5. LENTE GUIA DE ATUALIZAÇÃO (`api/README.md:116-136`)

| Passo | Comando/caminho existe? | Executável como está? |
|---|---|---|
| 1. Reconferir identidade | `sha256sum lib/Assembly-CSharp.dll` existe e confere | sim (a quebra de linha do `sha256sum` deixa `version`+`hash` na linha 81-82 por conferir; ver D4) |
| 2. Regerar superfície | `dotnet run --project api/tools/Inspect/Inspect.csproj -c Release -- targets lib/Assembly-CSharp.dll > api/docs/game-targets.json` | **sim, e reproduz `game-targets.json` byte-idêntico** (comando `targets` existe em `Inspect/Program.cs:33-36`) |
| 3. Recomparar | "o smoke já cobre isso" → `actual-game-hook-metadata` (`Program.cs:37-44`) | sim |
| 4. Ajustar código / remover hook | instrucional | sim, e a regra "não invente alvo alternativo silencioso" é coerente com o comportamento do código (falha ausente = zero patches, não substituição) |
| 5. Reconstruir e rodar o smoke | "os cinco `dotnet build` acima" | **parcialmente** — os 5 funcionam, mas dependem de um pré-requisito não listado no README (achado **D1**) |
| 6. Regravar evidências | instrucional | sim |
| 7. Runtime só com autorização | coerente com `Safety.EnableHooks=false` | sim |

**Fail-closed na mudança de versão:** correto. Numa atualização do jogo, `Application.version` muda e/ou o
hash do `Assembly-CSharp` muda; `Matches` exige **igualdade ordinal dos dois** e o plugin emite `LogError`
com os valores observados e instala zero hooks. O caso oposto (jogo atualizado que por acaso mantenha
`Application.version` *e* hash) é impossível enquanto o hash for do assembly carregado no processo. Não há
caminho de instalação parcial: `HookInstallation.Install` valida tudo antes de patchar (lente 3).

### Achado da lente 5 (D1)

`api/README.md:81-82` lista como pré-requisitos apenas ".NET SDK 6.0" e "os DLLs de referência em `lib/`".
Mas `api/Smoke/RealmApi.Smoke.csproj:3` e `api/tools/Inspect/Inspect.csproj:3` têm
`BepInExCoreDir` default = `$(USERPROFILE)/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core`
e consomem `0Harmony.dll`, `Mono.Cecil.dll`, `MonoMod.RuntimeDetour.dll`, `MonoMod.Utils.dll`, `BepInEx.dll`
**de lá**, não de `lib/`. Prova por comando (teste negativo):

```
dotnet build api/Smoke/RealmApi.Smoke.csproj   -c Release -p:BepInExCoreDir=C:/nonexistent-core  -> 2 Erro(s)
dotnet build api/tools/Inspect/Inspect.csproj  -c Release -p:BepInExCoreDir=C:/nonexistent-core  -> 1 Erro(s)
```

Ou seja: o passo 5 do guia ("os cinco `dotnet build`") **não é executável num checkout limpo sem o perfil
r2modman** (ou sem `-p:BepInExCoreDir=`), e o README não diz isso. Também omite que `Smoke` precisa das
dependências transitivas `MonoMod.*` e que o README cita `UnityEngine*.dll` como se viesse de `lib/` — para
Smoke/Inspect a origem é outra.

---

## 6. Achados (mudanças pedidas — todas de documentação, nenhuma de código)

Nenhum defeito funcional foi encontrado em contrato, gate ou Harmony. Os 4 itens abaixo são correções
documentais concretas:

- **D1 — Pré-requisitos incompletos no `api/README.md` (`:81-82`) e passo 5 do guia (`:132`).** Smoke e
  Inspect exigem o `BepInEx/core` do perfil r2modman (ou `-p:BepInExCoreDir=<outro>`), o que não está
  declarado. Comandos de prova: os dois builds negativos acima (2 e 1 erro).
  *Correção pedida:* acrescentar o pré-requisito (caminho default + propriedade `BepInExCoreDir` + a lista
  real de DLLs de Smoke/Inspect) e ajustar a origem dos `UnityEngine*.dll`.
- **D2 — `docs/automacao/API-R1-parte06.md` §3 afirma algo que o repo já contradiz.** O documento diz que
  "não existe alvo de deploy em nenhum `.csproj` de `api/`"; desde API-R1-I1 existe
  `api/Plugin/RealmApi.csproj:29` (`DeployToBepInEx`, opt-in). A regra deste cartão proíbe sobrescrever
  artefato de outra tarefa, então **não editei**: peço uma nota de errata no artefato da rodada seguinte ou
  a marcação do §3 como histórico.
  *Prova:* `grep -n 'DeployToBepInEx' api/Plugin/RealmApi.csproj` → linhas 19-31; `api/README.md:92-98` já
  descreve o alvo corretamente (o README novo está certo; o artefato antigo é que está obsoleto).
- **D3 — Tabela de identidade do README superdeclara o gate (`api/README.md:13-25`).** O título diz
  "Versão alvo do jogo (**obrigatória, fail-closed**)" para 5 campos e a frase da linha 24 diz "Se
  **qualquer um** desses valores divergir, a API não instala hook nenhum". O gate só compara **2**:
  `Application.version` e `sha256` do `Assembly-CSharp` (`Contracts.cs:24-26`). AppID, build Steam e versão
  Unity **não** são verificados em runtime; `BepInProcess("Stolen Realm.exe")` casa o **nome** do
  executável, não o AppID. *Correção pedida:* marcar por linha o que é verificado em runtime (2 campos) e o
  que é apenas identidade documentada do alvo (3 campos), ou trocar "qualquer um desses valores" por
  "versão do jogo ou hash do Assembly-CSharp".
- **D4 — Ressalva da `parte03` não chegou ao README.** `API-R1-parte03.md` diz explicitamente que a string
  `1.3.1` foi lida **estruturalmente** do objeto `PlayerSettings` de `globalgamemanagers` e que isso "NÃO
  comprova o nome semântico do campo", portanto **não** deve ser chamado de leitura de
  `Application.version` em runtime. O README, porém, é o documento do consumidor e não repete a ressalva,
  embora seja exatamente esse valor que o gate compara em execução. O comportamento continua fail-closed
  (se `Application.version` não for `1.3.1`, zero hooks), mas um consumidor pode concluir que a igualdade
  já foi exercitada — ela **não** foi (runtime NÃO_EXERCITADO).
  *Correção pedida:* uma linha no README (ou marcador `NÃO_EXERCITADO` no campo `gameVersion`) registrando
  que `Application.version` nunca foi observado em execução; a igualdade só será provada no runbook de
  runtime (`docs/automacao/API-R1-runbook-runtime.md`).

### Observações (não pedem mudança, registro para o dono)

- **OBS-1 — `api/` está inteiramente *untracked*:** `git status --short api/` → `?? api/` e
  `git ls-files api/` → 0 arquivos; o módulo entregue não tem registro de versão no git. Sem risco de
  lixo: `.gitignore` cobre `bin/` e `obj/` (linhas 1-2), então um `git add api/` levaria só fontes,
  `.csproj`, `docs/`, `LICENSE` e `README.md`.
- **OBS-2 — lacuna residual de teste (lente 3):** não existe caso `Resolve` com **2** matches. Em C# é
  inatingível (dois membros não podem diferir apenas pelo retorno), então o guarda
  `matches.Length!=1` é apenas cinto de segurança; registro como limite conhecido, não como defeito.
- **OBS-3 — passo 1 do guia** não dá comando para `buildid`/`globalgamemanagers` (dá só o **nome** do
  arquivo `appmanifest_1330000.acf`) e o passo 2 usa redirecionamento de shell (`>`), que não vale em
  `cmd.exe`. Nada quebra no bash do repo.

---

## 7. Veredito

**APROVADO COM RESSALVAS (nenhum defeito funcional).**

Reproduzi por conta própria, com resultado real e nesta rodada: os **5 `dotnet build`** (0 avisos / 0 erros
cada), o **smoke completo** (`Ran 25 tests; failures: 0`, exit 0, saída byte-idêntica ao
`api/docs/smoke-output.txt`), o **grep de vazamento** (0 arquivos em `api/` e nos artefatos `API-R1-*`), o
comando do **passo 2** do guia (regerou `game-targets.json` byte-idêntico) e a **identidade do alvo**
(hash/AppID/build/Unity conferidos direto na instalação e em `lib/`), além de confirmar que o perfil
r2modman não foi tocado e que nenhum `.csproj` de `api/` referencia ou redistribui `Assembly-CSharp.dll`.

O contrato promete exatamente os 4 hooks que existem e eles batem 4/4 com o metadado real; o gate é
fail-closed de fato (nulo/vazio/divergente recusam, e a exceção também recusa); o Harmony remove só o
próprio owner, é idempotente, deixa zero patches em alvo ausente/duplicado, preserva owner de terceiros e
recusa forma de postfix não suportada; o guia de atualização é fail-closed e seus comandos existem
(exceto pela dependência não declarada do `BepInEx/core`).

As mudanças pedidas são **D1–D4**, todas de documentação, e não invalidam a base 0.1.0 como observacional.
Os limites declarados (runtime NÃO_EXERCITADO, sem publicação, sem deploy no perfil, famílias restantes não
implementadas) foram verificados como verdadeiros neste repo.

Recomendação ao dono: fechar a base 0.1.0 e encaminhar D1–D4 como correção documental na rodada seguinte;
o único item que muda o que um terceiro consegue fazer seguindo o README do zero é **D1**.
