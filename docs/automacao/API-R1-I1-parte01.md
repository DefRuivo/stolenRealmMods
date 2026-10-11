# API-R1-I1 — parte 01: alvo de deploy OPT-IN no `api/Plugin/RealmApi.csproj` (com provas)

Tarefa `t_f32becd0` (API-R1-I1, filha de API-R1 / `t_b7f6fc4a`). Partes seguintes:
`API-R1-I1-parte02.md` (runbook), `API-R1-I1-parte03.md` (não exercitado e pendências).
Evidências por comando: `docs/automacao/API-R1-I1-evidencias/01`…`09`.

Regra que governa esta parte: `Directory.Build.props` (raiz) define `DeployToBepInEx=false` por padrão e
**todo** alvo que copia para o perfil exige `Condition="'$(DeployToBepInEx)' == 'true'"`. O padrão dos mods
do repo é: `AfterTargets="Build"`, destino em
`$(USERPROFILE)\AppData\Roaming\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\$(AssemblyName)\`,
`MakeDir` + `Copy` + `Message`. O alvo novo segue esse padrão, com duas decisões próprias:

1. copia **três** arquivos (`RealmApi.dll`, `RealmApi.Core.dll`, `RealmApi.Hooks.dll`) — os dois últimos
   são project references do plugin e **sem eles o BepInEx não resolve o plugin** ao carregar;
2. o destino é a propriedade `PluginsDir` **com default condicional** (`Condition="'$(PluginsDir)' == ''"`),
   o que permite **ensaiar** o deploy em pasta isolada (`-p:PluginsDir=…`) sem tocar o perfil do dono.
   Propriedade global do MSBuild vence a propriedade interna, então o opt-in continua sendo a **única**
   chave do alvo: `Condition` na tag `<Target>`.

## 1. O que foi editado

`api/Plugin/RealmApi.csproj:29` (o arquivo tinha 17 linhas; ficou com 42 — o alvo foi acrescentado no fim,
antes de `</Project>`),
diff efetivo da edição:

```
+  <Target Name="DeployToBepInEx" AfterTargets="Build" Condition="'$(DeployToBepInEx)' == 'true'">
+    <PropertyGroup>
+      <PluginsDir Condition="'$(PluginsDir)' == ''">$(USERPROFILE)\AppData\Roaming\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\$(AssemblyName)\</PluginsDir>
+    </PropertyGroup>
+    <ItemGroup>
+      <ApiDeployFile Include="$(TargetPath)" />
+      <ApiDeployFile Include="$(TargetDir)RealmApi.Core.dll" />
+      <ApiDeployFile Include="$(TargetDir)RealmApi.Hooks.dll" />
+    </ItemGroup>
+    <MakeDir Directories="$(PluginsDir)" />
+    <Copy SourceFiles="@(ApiDeployFile)" DestinationFolder="$(PluginsDir)" />
+    <Message Importance="high" Text="Deploy: RealmApi.dll + RealmApi.Core.dll + RealmApi.Hooks.dll copiados para $(PluginsDir)" />
+  </Target>
```

Antes deste cartão o módulo `api/` **não tinha alvo de deploy nenhum** (era assim que o `api/README.md`
estava escrito, e continuava verdade). Coerência de documentação: a seção "Como construir" e a lista de
NÃO exercitado do `api/README.md` foram atualizadas para descrever o alvo novo e apontar para o runbook —
nenhuma outra afirmação do README foi tocada.

## 2. Provas (todas por comando; saída bruta em `docs/automacao/API-R1-I1-evidencias/`)

| evidência | comando | resultado medido |
|---|---|---|
| `01-perfil-antes.txt` | impressão digital do perfil (`plugins/` + `config/`: caminho, bytes, mtime, sha256) com o jogo fechado | 30 arquivos; nenhuma pasta/arquivo `RealmApi` no perfil; hash do conjunto `8d615c0af3dffe61d6417f03d3a9c8f81fe23b02640f8d75c7e3d17b4273a436` |
| `02-guarda-optin.txt` | `python tools/check_deploy_optin.py` (raiz) e `--raiz api` | `--raiz api`: `[ ok ] 1 alvo(s) de deploy, todos com Condition="'$(DeployToBepInEx)' == 'true'"` (exit 0). Na raiz: 3 achados **pré-existentes, todos em `scratch/`** (fixtures de teste negativo do KIT-14: `scratch/kit/KIT-14-run699/deploy-negative/ruim.csproj`, `…/KIT-14-run710/deploy-negative/ruim.csproj` e um XML inválido em backup do `…/KIT-14-run699/instalacao-local-resume/`), **nenhum** em `api/` |
| `03-build-sem-flag.txt` | `dotnet build api/Plugin/RealmApi.csproj -c Release` | `0 Aviso(s), 0 Erro(s)`, exit 0; a mensagem `Deploy:` **não** aparece (grep = 0 linhas) |
| `04-perfil-depois.txt` | mesma impressão digital, depois do build | mesmos 30 arquivos, mesmos bytes/mtime/sha256 |
| `05-antes-x-depois.txt` | `diff` dos dois arquivos + hash do conjunto | hash do conjunto **igual** (`8d615c0a…a436`); 30 = 30 registros; `plugins/RealmApi` **não existe**; `config/com.gumatos.realmapi.cfg` **não existe** |
| `06-ensaio-arena-isolada.txt` | `dotnet build … -c Release --no-restore -p:DeployToBepInEx=true -p:PluginsDir="<arena vazia>\\"` | alvo **executou**: 3 DLLs copiadas para a arena, hashes idênticos aos de `api/Plugin/bin/Release/netstandard2.1/` (`RealmApi.dll` `b52b66e5…822c`, `Core` `5cbfcb32…bab8`, `Hooks` `19470274…1b86`) |
| `07-perfil-intacto-e-destino-padrao.txt` | impressão digital após o ensaio + `dotnet msbuild … -preprocess` | perfil **ainda** idêntico (`8d615c0a…a436`); o pré-processamento mostra o destino padrão do alvo (`…\profiles\Default\BepInEx\plugins\$(AssemblyName)\` com `USERPROFILE`) e a `Condition` do opt-in — provado **sem** executar o alvo |
| `08-smoke-e-guarda.txt` | `dotnet build api/Smoke/RealmApi.Smoke.csproj -c Release` + `RealmApi.Smoke.exe lib/Assembly-CSharp.dll api/Plugin/bin/Release/netstandard2.1/RealmApi.dll` | `Ran 25 tests; failures: 0`, exit 0 — a edição do `.csproj` não quebrou a API |
| `09-tentativa-userprofile-descartada.txt` | `dotnet build … -p:DeployToBepInEx=true -p:USERPROFILE="<arena>"` | **descartada**: trocar `USERPROFILE` derruba a resolução do targeting pack (`146 Erro(s)` CS0518/CS0246) e nada é copiado. Registrada porque foi testada; a via adotada é `-p:PluginsDir` |

Respostas diretas ao aceite desta parte:

- **"build SEM a flag não copia nada"**: `03` (0 erros, sem mensagem `Deploy:`) + `05`
  (`plugins/RealmApi` inexistente, 30 = 30 arquivos).
- **"o perfil r2modman não foi tocado"**: `01` × `04` × `07` — hash do conjunto idêntico nas três leituras,
  com o jogo fechado e nenhum processo `Stolen Realm` em execução.
- **"o alvo funciona"**: `06` — executado de verdade, com a flag, escrevendo só na arena isolada.
- **"não há alvo sem opt-in em `api/`"**: `02` — guarda da raiz (`tools/check_deploy_optin.py`), o mesmo
  gate que o `tools/release-check.sh` roda antes de buildar.

## 3. Limites desta parte

- O **deploy real** (`dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=true`) **não
  foi executado**: instalar no perfil exige autorização explícita do dono (LIMITES do cartão).
- Nenhum arquivo do jogo, do perfil, do `lib/` ou do `Assembly-CSharp.dll` foi criado, alterado ou
  removido; só ficaram edições **dentro do repo** (`api/Plugin/RealmApi.csproj`, `api/README.md`) e os
  arquivos novos de documentação/evidência.
- O ensaio da arena isolada **não é** prova de que o BepInEx carrega o plugin: é prova do **alvo de
  deploy**. O runtime continua NÃO_EXERCITADO (`API-R1-I1-parte03.md`).
