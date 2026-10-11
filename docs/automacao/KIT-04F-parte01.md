# KIT-04F — parte 01: diagnóstico e correção do build do Core

Tarefa: `t_d5c98d36` (KIT-04F) · Data: 2026-10-09 · Rodada **OFFLINE** (sandbox, sem jogo)
Origem: parecer REPROVADO `docs/automacao/KIT-04R-revisao.md` (run 607).
Implementador: perfil `default` (run 613). Revisor: perfil `default` (run separada).

Este documento é **incremental** (premissa do controlador: cada bloco vira arquivo novo
numerado; nada é sobrescrito). Provas volumosas em `scratch/kit/`.

## 1. Estado de partida (medido, não relatado)

O run 612 (reclamado pelo operador) já havia aplicado parte das correções no disco.
Estado encontrado por leitura direta nesta run:

| Item KIT-04F | Estado no disco ao iniciar | O que faltava |
|---|---|---|
| 1. referenciar ScreenCaptureModule + ImageConversionModule | `KIT04Core.csproj` linhas 19-20 já usam `$(GameManaged)` | **provar** build exit 0 |
| 2. `_habilitado` default false | `CorePlugin.cs:129` já usa `false` | coerência de comentários |
| 3. `LerComponentes<T>` ⇒ `null` se ausente | ainda retornava `FindObjectsOfType<T>()` (array vazio) | **corrigir** |
| 4. adapter `KIT04Adapter.SR/` | 7 arquivos presentes | provar build exit 0 |
| 5. contrato/matriz/plano/schemas | ausentes | **entregar** |
| 6. hashes reais | placeholders em `KIT-04-entrega.md` | **substituir** |
| 7. controle negativo | ausente | **entregar** |

Nenhum arquivo vivo do produto (mods, `Assembly-CSharp.dll`, Bard) foi tocado.

## 2. Item 1 — módulos de captura (prova de execução)

`lib/` do repositório **não** contém `UnityEngine.ScreenCaptureModule.dll` nem
`UnityEngine.ImageConversionModule.dll` (confirmado por `ls lib/`). Eles existem só na pasta
`Managed` do jogo. O `KIT04Core.csproj` (e o do adapter) passam a referenciá-los por
`$(GameManaged)`, o mesmo mecanismo do `AUT4Probe.csproj`:

```xml
<GameManaged Condition="'$(GameManaged)' == ''">E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed</GameManaged>
...
<Reference Include="UnityEngine.ScreenCaptureModule"><HintPath>$(GameManaged)/UnityEngine.ScreenCaptureModule.dll</HintPath><Private>false</Private></Reference>
<Reference Include="UnityEngine.ImageConversionModule"><HintPath>$(GameManaged)/UnityEngine.ImageConversionModule.dll</HintPath><Private>false</Private></Reference>
```

### Prova: build em cópia isolada

Sandbox `scratch/kit/build/kit04f-sandbox/` com a mesma profundidade de árvore do repo
(`tools/automacao/runtime/…` + `lib/`), `bin/`/`obj/` removidos antes do build.

```
dotnet build KIT04Core/KIT04Core.csproj      -c Release -p:DeployToBepInEx=false  -> EXIT 0, 0 Erro(s), 18 Aviso(s)
dotnet build KIT04Adapter.SR/KIT04Adapter.SR.csproj -c Release -p:DeployToBepInEx=false -> EXIT 0, 0 Erro(s), 5 Aviso(s)
```

DLLs produzidas (sha256 medido no sandbox):

```
381734354514851de98de7c9c58e195ad68a88be34ea83556b1f2931dcf2c1ef  KIT04Core/bin/Release/KIT04Core.dll
0a8fbc22eb7afea7f7a5bee6f2ce1e5a34969682ae9e7682078a2e032372de99  KIT04Adapter.SR/bin/Release/KIT04Adapter.SR.dll
```

Logs: `scratch/kit/logs/kit04f-core-build.log`, `scratch/kit/logs/kit04f-adapter-build.log`.
Os 3 erros CS1069/CS0103 do parecer (CorePlugin.cs 228/231/261) **não ocorrem mais** — o Core
compila o caminho de captura que antes estava quebrado.
