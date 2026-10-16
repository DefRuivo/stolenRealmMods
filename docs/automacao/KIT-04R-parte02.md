# KIT-04R — parte 02: execução real em sandbox (build)

Sandbox: `%USERPROFILE%/AppData/Local/hermes/cache/scratch/`
- `kit-revisao/`      → cópia de `tools/automacao/runtime/KIT04Core` + `lib/` + `AUT4Probe`
- `kit-revisao-positivo/` → cópia do Core com o defeito de captura neutralizado

Nenhum jogo aberto no momento da medição (`tasklist` → nenhum processo "Stolen").
Comando sempre com `-p:DeployToBepInEx=false`, nunca escreve no perfil.

## C1 — Build do artefato ENTREGUE (leitura fria, sem alteração)

```
$ cd <sandbox>/tools/automacao/runtime/KIT04Core
$ dotnet build -c Release -p:DeployToBepInEx=false
...
CorePlugin.cs(228,49): error CS1069: O nome do tipo "ScreenCapture" ... foi encaminhado para o assembly "UnityEngine.ScreenCaptureModule ..."
CorePlugin.cs(231,29): error CS0103: O nome "ImageConversion" não existe no contexto atual
CorePlugin.cs(261,39): error CS1069: ... "UnityEngine.ScreenCaptureModule" ...
    18 Aviso(s)
    3 Erro(s)
```
**EXIT = 1 (FALHOU).** Nenhuma DLL produzida. Reproduz exatamente o veredito da rodada 1
(3 erros; mesmo local). Os 3 erros são reais e localizados em `CorePlugin.cs`.

Causa raiz (evidenciada, não inferida):
- `KIT04Core.csproj` referencia `UnityEngine.CoreModule`, `UI`, `TextRenderingModule`,
  `UIModule` — mas **não** `UnityEngine.ScreenCaptureModule` nem `ImageConversionModule`.
- `lib/` do repo **não contém** `UnityEngine.ScreenCaptureModule.dll` nem
  `UnityEngine.ImageConversionModule.dll` (`ls lib/` = 16 DLLs, nenhum módulo de captura).
- O instrumento existente resolve isso por uma propriedade `GameManaged`
  (`AUT4Probe.csproj`: `E:\SteamLibrary\...\Stolen Realm_Data\Managed`) apontando
  `UnityEngine.ScreenCaptureModule` para a pasta do jogo. **O Core não herdou esse mecanismo.**
- Os dois módulos existem na instalação do jogo:
  `UnityEngine.ScreenCaptureModule.dll` (21416 B) e `UnityEngine.ImageConversionModule.dll`.

## C2 — Controle negativo + caminho positivo (defeito plantado / neutralizado)

Método: numa cópia isolada, neutralizei **apenas** o caminho de captura (2 edições em
`CorePlugin.cs`: corpo de `CapturarPNG` → `return false;` e `EstaDisponivel()` → `return false;`),
sem tocar em mais nada.

```
$ dotnet build -c Release -p:DeployToBepInEx=false   (cópia com captura neutralizada)
    19 Aviso(s)
    0 Erro(s)
EXIT = 0   →  bin/Release/KIT04Core.dll (14848 B) produzida
```

Interpretação (prova de localização, não de qualidade):
- as-delivered (com captura)  → **FALHOU** exit 1, 3 erros;
- captura neutralizada        → **PASSOU** exit 0, 0 erros, DLL gerada.

Ou seja: **os 3 erros apontados são os únicos bloqueadores de compilação do Core.**
O resto do Core (interfaces, sessão, eventos, Json, identidade) é compilável.
Isto não valida comportamento — apenas isola a falha de build ao caminho de captura PNG.

## C3 — Refutação de regressão na migração (instrumento de origem)

O instrumento de origem (AUT4Probe) **não regrediu**: compila e a DLL do repo confere com o
hash declarado nas revisões anteriores.

```
$ sha256sum tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll
407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7   (igual ao declarado em AUT-4R4)
$ dotnet build -c Release -p:DeployToBepInEx=false   (AUT4Probe em sandbox)
    1 Aviso(s) MSB3277 (System.Net.Http, herdado)
    0 Erro(s)
AUT4PROBE_BUILD_EXIT=0
```

**Refutação**: o AUT4Probe continua compilando (exit 0) e sua DLL não mudou → não há regressão
no instrumento de origem. A regressão está **no artefato novo**: o Core perdeu o mecanismo de
referência (`GameManaged`) que o AUT4Probe usa para `ScreenCaptureModule`, e por isso não compila.

## Próximo bloco

- Leitura da especificação do contrato (`KIT-04-core-especificacao.md`) para mapear critérios
  (API pequena, desabilitada por padrão, sem dependência obrigatória dos mods).
- Refutações: interferência do instrumento no produto e dependência obrigatória dos mods.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
