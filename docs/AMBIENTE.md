# Ambiente — versões, caminhos e decisões

Ambiente **reproduzível** deste projeto. Se você (ou o você do futuro) tiver que montar
a máquina de novo, é daqui que sai tudo. Tudo abaixo foi **verificado na máquina**, não
copiado de documentação de terceiro.

---

## 1. Versões validadas

| Componente | Versão | Como conferir |
|---|---|---|
| Windows | 11 x64 | — |
| **BepInEx** | **5.4.23.5** (`5.4.23.5+57f1fb8…`), **win_x64 / Mono** | `powershell -c "(Get-Item '<perfil>\BepInEx\core\BepInEx.dll').VersionInfo.FileVersion"` |
| **Unity** (engine do jogo) | **2022.3.62f2** (build `2022.3.62.7762112`) | `UnityPlayer.dll` → VersionInfo, ou o cabeçalho do `LogOutput.log` (`Running under Unity v2022.3.62.7762112`) |
| **Runtime CLR** | **Mono** — `CLR runtime version: 4.0.30319.42000` | linha do `LogOutput.log`. **Não é IL2CPP.** |
| **.NET SDK** (build dos mods) | **6.0.428** | `dotnet --version` |
| Alvo dos mods | **`netstandard2.1`**, `LangVersion 10` | `<TargetFramework>` no `.csproj` |
| Harmony | **HarmonyX** (`0Harmony.dll` do `core\` do BepInEx) | `BepInEx\core\0Harmony.dll` |
| Python (scripts de `tools/`) | **3.14.7** | `python --version` |

**Mono, não IL2CPP** — três provas: o log diz `CLR runtime version: 4.0.30319.42000`; a
pasta do jogo tem `MonoBleedingEdge\`; e o BepInEx 5 carrega pelo doorstop
(`winhttp.dll` + `doorstop_config.ini`), que é o caminho Mono. Isso importa porque os
mods são DLLs .NET gerenciadas (`netstandard2.1`), compiladas contra
`Assembly-CSharp.dll` — em IL2CPP não haveria esse assembly gerenciado para referenciar.

### Plugins que carregam no perfil `Default` (6)

| Plugin | Origem |
|---|---|
| `Script Engine 11.1` | terceiro (Thunderstore) — carrega, mas o hot-reload não funciona neste jogo (decisão: parado) |
| `Better Font 1.0.0` | projeto |
| `Better Stats 1.0.0` | projeto |
| `Better Tooltips 0.1.0` | projeto |
| `Roguelike Debugger 0.1.0` | projeto (ferramenta de dev — despeja o dump que alimenta o censo) |
| `Roguelike QoL 0.1.0` | projeto (HUD **desabilitado**: `AtivarHUD=false`) |

---

## 2. Caminhos

| O que | Onde |
|---|---|
| Repositório | `C:\dev\stolen-realm` |
| **Jogo** (Steam, appid **1330000**) | `E:\SteamLibrary\steamapps\common\Stolen Realm` |
| **Perfil do r2modman** (raiz) | `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\` — `winhttp.dll`, `doorstop_config.ini`, `mods.yml`, `BepInEx\` |
| **BepInEx do perfil** | `…\profiles\Default\BepInEx\` — `core\` (BepInEx.dll, 0Harmony.dll, Mono.Cecil…), `plugins\`, `config\`, `patchers\`, `cache\`, `scripts\` |
| Plugins dos mods | `…\BepInEx\plugins\<Mod>\<Mod>.dll` (**uma pasta por mod**) |
| **Log** | `…\BepInEx\LogOutput.log` |
| Saída de build | `<Mod>\bin\Debug\netstandard2.1\<Mod>.dll` |
| Referências de compilação | `C:\dev\stolen-realm\lib\` (`Assembly-CSharp.dll`, `BepInEx.dll`, `UnityEngine.dll`, `UnityEngine.CoreModule.dll`, `0Harmony.dll`, `Sirenix.*`) — **gitignored** (são DLLs do jogo), só para compilar |
| **Backup de DLL** | `C:\dev\stolen-realm\scratch\backups\` |
| Steam (para o ciclo de teste) | `C:\Program Files (x86)\Steam\steam.exe` (o `scratch/test-cycle.sh` aceita `$STEAM`) |

**Lançamento modded** (é o que o `scratch/test-cycle.sh` faz, e o que o r2modman faz
pelo botão *Start modded*): o jogo é aberto com o doorstop apontando para o preloader
**do perfil**, sem tocar na pasta do jogo —

```
steam.exe -applaunch 1330000 --doorstop-enabled true \
  --doorstop-target-assembly "<perfil>\BepInEx\core\BepInEx.Preloader.dll"
```

Os mods são carregados pelo BepInEx **a partir da pasta do perfil**. Nada do jogo
original é alterado: `Assembly-CSharp.dll` é **somente leitura**, referência de
compilação (`<Private>false</Private>` no `.csproj`) — **nunca distribuir nem
modificar**.

---

## 3. `StolenRealmModAPI` — **DESATIVADA** (decisão)

A `StolenRealmModAPI` é uma **biblioteca de terceiros** (Thunderstore) que estava
instalada no perfil. No build atual do jogo ela **não aplica o patch principal**:

```
AccessTools.Method: Could not find method for type GameAnalyticsSDK.Setup.Game and name Awake
StolenRealmModAPI.Skills.SkillRegistryPatches+GameAwakePatch::TargetMethod() returned an unexpected result: null
```

Ou seja: o `GameAwakePatch::TargetMethod()` devolve `null` porque a API procura
`GameAnalyticsSDK.Setup.Game.Awake`, que **este build do jogo não tem mais** (a API não
acompanhou o jogo).

**A versão 0.2.0 falha exatamente igual à 0.1.0** — a 0.2.0 foi publicada 8 minutos
depois da 0.1.0, foi baixada e instalada, e o ciclo mostrou o **mesmo erro**. Conclusão:
**atualizar não é a saída.**

**Ação tomada:** a DLL foi **renomeada** para
`…\BepInEx\plugins\StolenRealmModding-StolenRealmModAPI\StolenRealmModAPI.dll.disabled`
— o BepInEx só carrega `*.dll`, então a renomeação **desativa sem apagar**, e é
**reversível**: tirar o sufixo `.disabled` volta a ativar.

**Por que é seguro:** **nenhum mod deste projeto depende dela** — nenhum
`BepInDependency`, nenhuma referência a `StolenRealmModAPI` nos `.cs`/`.csproj`
(conferido por varredura no repositório), o log não acusa dependência quebrada, e os
mods do projeto usam Harmony direto. Com a API desativada o ciclo fecha com **6 plugins
carregando e zero erro**.

> Os mods do projeto **não** precisam da ModAPI para nada. Se algum dia um mod precisar,
> é melhor reimplementar o que for necessário do que reativar a API — ela está parada no
> build atual do jogo.

---

## 4. Regra: **backup de DLL NUNCA dentro de `plugins/`**

O BepInEx varre `plugins/` **recursivamente**: **qualquer `*.dll` lá dentro é carregado
como plugin**, inclusive dentro de uma pasta `*.bak`. Isso não é teoria — custou **dois
ciclos de teste** perdidos: o backup `…\plugins\StolenRealmModding-StolenRealmModAPI.0.1.0.bak\StolenRealmModAPI.dll`
ficou **dentro** de `plugins/` e **era carregado como mod**, mantendo vivo o erro da
ModAPI mesmo com a original já desativada.

**Regra:** backup de DLL vai para **`C:\dev\stolen-realm\scratch\backups\`** — nunca em
`…\BepInEx\plugins\`. Hoje há lá:

```
scratch\backups\StolenRealmModding-StolenRealmModAPI.0.1.0.bak\
    StolenRealmModAPI.dll, manifest.json, icon.png, README.md
```

(backup completo do pacote 0.1.0, fora do `plugins/` e fora do git).

Regras irmãs, pelo mesmo motivo:

- **Não modificar `Assembly-CSharp.dll`.** Ela é o jogo; os mods a referenciam só para
  compilar (`lib/`, gitignored).
- Desinstalar um mod = apagar `plugins\<Mod>\`. Um mod não afeta os outros.
- A árvore de skills do **Bard** é **intocável** (regra do projeto, marcada como
  `intocavel` no censo).

---

## 5. Checklist rápido para conferir o ambiente

```bash
# versões
dotnet --version                                        # 6.0.428
python --version                                        # 3.14.7
powershell -c "(Get-Item \"$env:APPDATA\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\core\BepInEx.dll\").VersionInfo.FileVersion"   # 5.4.23.5

# referências de compilação presentes
cd C:/dev/stolen-realm && ls lib/        # Assembly-CSharp.dll, BepInEx.dll, UnityEngine*, 0Harmony, Sirenix*

# a API está desativada?
ls "%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/plugins/StolenRealmModding-StolenRealmModAPI/"

# nada de DLL de backup DENTRO de plugins/  (a lista tem que ficar vazia:
# o BepInEx carregaria qualquer *.dll ali, inclusive num *.bak/)
find "%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/plugins" -path "*bak*" -name "*.dll"
```

Depois de qualquer build/instalação, valide pelo **ritual de build** descrito em
[`README.md`](README.md) §3 (build 0 erros → `check_fix_keys` → `check_dupes` → instalar
→ ciclo do jogo com o log limpo).
