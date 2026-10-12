# LEVEL-R3F1 — relatório 02: a correção, a escolha por medição e as provas

Task: `t_021bdd67` · worktree `C:/dev/stolen-realm/.worktrees/level-r2` (branch `wt/t_918314e9`).
Modelo: `deepseek-flash` / `deepseek`. Build só com `-p:DeployToBepInEx=false`; nada instalado;
jogo não aberto; save/perfil do dono intocados.

## 1. Ancoragem no código real (o que exatamente foi corrigido)

IL real de `Character::Load(int32 saveIndex)` lida da `Assembly-CSharp.dll` de referência
(`ilspycmd -il -t Character`, hash conferido) — o clamp que a R3-01 aponta:

```
IL_0883: ldarg.0
IL_0884: ldarg.0
IL_0885: call     float32 Character::get_MaxLevel()          // <-- getter patcheado pelo mod
IL_088a: ldarg.0
IL_088b: call     class Burst2Flame.CharacterSaveFile Character::get_CharacterSaveFile()
IL_0890: callvirt float32 Burst2Flame.CharacterSaveFile::get_ExperienceLevel()
IL_0895: call     float32 [UnityEngine.CoreModule]UnityEngine.Mathf::Min(float32, float32)
IL_089a: callvirt void Character::set_ExperienceLevel(float32)   // <-- valor clampado
```

Getter vanilla (`Character::get_MaxLevel`): devolve `GlobalSettingsManager.globalSettings.MaxLevel`
(= 30) para não-IA e `+Infinito` para IA. `Character.Level` (`corpus.cs` 4443-4457) é
`Mathf.FloorToInt(Mathf.Max(ExperienceLevel, 1f))` — durante o clamp, `ExperienceLevel` ainda é 0,
logo `Level == 1`. O clamp persiste em `corpus.cs:36131` (`CharacterSaveFile.ExperienceLevel =
ExperienceLevel`). Tudo confirmado por leitura independente da IL, não por reimplementação.

## 2. Escolha da correção — por medição, não por preferência

O cartão oferece (a) devolver vanilla/piso no Postfix quando detectar carga, (b) Prefix/Postfix
dedicado em `Character.Load(int)`, (c) injetar o piso no getter a partir de
`CharacterSaveFile.ExperienceLevel` quando `IsLoaded == false`.

Medição decisiva: o requisito 2 do cartão exige que o clamp de carga **não** trunque save acima de
30 no caminho de fallback. A opção (a) como escrita ("devolver o valor vanilla") devolve **30** e
`Mathf.Min(30, 35) = 30` — **não** satisfaz o requisito. Logo (a) está eliminada pelo próprio
critério do cartão, não por gosto.

Entre (b) e (c), escolhi **(c)** por três razões verificáveis:

1. **Um único ponto de decisão.** O teto efetivo já é `PolicyCore.EffectiveMaxLevel` — a mesma
   função que a bancada já alimenta. (c) acrescenta um piso a essa decisão; (b) adicionaria um
   alvo Harmony novo (`Character.Load`) que **não** é exercitável sem um `Character` real e que
   corrigiria o valor **depois** do clamp (o corpo de `Load` seguiria enxergando o valor
   truncado em leituras posteriores de `MaxLevel`/`MaxExperience`/`IsMaxLevel`).
2. **Cobre todos os caminhos, inclusive o fallback vanilla.** Como o piso é aplicado sobre o valor
   final do getter (e não só no ramo estendido), o caminho "grupo não aplicado / multiplayer /
   backend indisponível" também deixa de truncar. Era exatamente o que faltava.
3. **É provável pela bancada.** A decisão é pura (`PolicyCore`), então o teste exercita o **mesmo**
   código que roda em jogo, sem seam novo e sem depender do runtime Unity.

Nada de transpiler foi necessário — mantém-se o padrão já usado (`BattleResultTranspiler`) sem
introduzir um segundo transpiler.

## 3. A correção

`Core/PolicyCore.cs` — entradas novas e piso de carga (uma única decisão):

```csharp
public double VanillaMaxLevel;   // valor observado do getter vanilla (GlobalSettings.MaxLevel)
public bool   IsLoading;         // dentro de Character.Load(int): ExperienceLevel ainda nao atribuido
public double SavedLoadLevel;    // CharacterSaveFile.ExperienceLevel que esta sendo carregado

public static double EffectiveMaxLevel(in AdvanceInputs i)
{
    double bound = i.SafetyBound > 0
        ? i.SafetyBound
        : (i.VanillaMaxLevel > 0 ? i.VanillaMaxLevel : XpCurve.VanillaCapLevel);
    if (i.VoluntaryCap > 0 && i.VoluntaryCap < bound) bound = i.VoluntaryCap;

    double floor = i.Level;
    // Character.Load(int) faz ExperienceLevel = Mathf.Min(MaxLevel, CharacterSaveFile.ExperienceLevel)
    // ANTES de ExperienceLevel ser atribuido (Level ~ 1). Em carga o getter nunca fica abaixo do salvo.
    if (i.IsLoading && XpCurve.IsUsableNumber(i.SavedLoadLevel) && i.SavedLoadLevel > floor)
        floor = i.SavedLoadLevel;

    return bound > floor ? bound : floor;
}
```

`Runtime/Policy.cs` — o getter alimenta o piso em carga e passa a rotear o **fallback** pela mesma
decisão (antes havia `return vanillaValue` cedo demais, o que impedia qualquer piso):

```csharp
bool loading = !character.IsLoaded;
double savedLoadLevel = 0d;
if (loading) { var save = character.CharacterSaveFile; if (save != null) savedLoadLevel = save.ExperienceLevel; }

bool extended = PluginState.GameplayGroupApplied && !GameState.IsMultiplayer() && XpBackend.EnsureReady();

var inputs = new AdvanceInputs {
    ...,
    VoluntaryCap = extended ? PluginState.MaxLevelConfig : 0,
    SafetyBound  = extended ? XpBackend.SafetyBound : 0,
    VanillaMaxLevel = vanillaValue,
    IsLoading = loading,
    SavedLoadLevel = savedLoadLevel,
    ... };
double result = PolicyCore.EffectiveMaxLevel(in inputs);
if (!XpCurve.IsUsableNumber(result)) return vanillaValue;
return result;
```

Fora do escopo continua **vanilla literal** (`character.IsAI || !IsRoguelikeCharacter` e
`!PluginState.Enabled` retornam `vanillaValue` antes de qualquer piso): campanha, IA e mod desligado
seguem intactos. Fora da carga (`IsLoaded == true`) o piso não se aplica — o teto voluntário
continua valendo, como antes.

## 4. Requisitos do cartão, um a um

1. **Caminho de carga seguro** — o getter nunca devolve abaixo do salvo em carga (feito; provado
   abaixo). Cobre os dois caminhos da R3-01: teto voluntário `N` (save > N preservado) e fallback
   (save > 30 preservado).
2. **Fallback** — `IsMultiplayer()==true` / `GameplayGroupApplied==false` / `EnsureReady()==false`
   agora usam o mesmo piso: o teto vanilla 30 deixa de ser teto de **carga** quando o save é maior
   (teste `loadclamp.vanilla_fallback_does_not_truncate_above_30`).
3. **`GiveExperience`** (corpus.cs:43738) — não tocado; a prova `loadclamp.give_experience_no_downgrade`
   confirma que `Mathf.Min(MaxLevel, novoNivel)` continua ≥ nível atual (getter nunca abaixo do
   nível quando não está em carga).
4. **Teste real que pode falhar** — §5.
5. **Relatórios novos / README+CHANGELOG v0.1.1 / hashes / pacote** — relatório 03.

## 5. A prova: teste real ancorado no clamp, e contra-prova que deixa a suíte vermelha

Suíte nova `loadclamp` (12 verificações) em `tests/RoguelikeLevelProgression.Harness/Program.cs`.

**(A) Âncora na IL real** — lê `Character.Load(int)` da `Assembly-CSharp.dll` de referência com o
`IlLoader` do harness e exige a janela estrutural do clamp, **única**, sem índice de local nem
offset chumbado:

| verificação | resultado |
| --- | --- |
| `loadclamp.load_method_present` | PASS — `Character.Load(int)` encontrado na DLL real |
| `loadclamp.load_il_decoded` | PASS — IL real decodificada em 1080 instruções |
| `loadclamp.clamp_window_present_in_real_il` | PASS — janela `Mathf.Min(get_MaxLevel, CharacterSaveFile.get_ExperienceLevel)` → `set_ExperienceLevel` (índice 673) |
| `loadclamp.clamp_window_unique` | PASS — exatamente 1 janela no método |
| `loadclamp.clamped_getter_is_the_patched_one` | PASS — o getter lido pelo clamp é **o mesmo** alvo do postfix do mod |
| `loadclamp.maxlevel_postfix_registered` | PASS — `PatchRegistry` registra `MaxLevelPatches.Postfix` nesse getter |

**(B) Reprodução do clamp com o par (MaxLevel efetivo, nível salvo)** — alimenta o `PolicyCore`
**real** exatamente como `Policy.EffectiveMaxLevel` o alimenta em carga (`Level = 1`, nível salvo
vindo de `CharacterSaveFile`) e aplica o `Mathf.Min` do clamp:

| caso | MaxLevel(patcheado) | clamp | veredito |
| --- | --- | --- | --- |
| teto voluntário 25, save 30 | 30 | 30 | PASS — preservado |
| fallback vanilla (observado 30), save 35 | 35 | 35 | PASS — 30 não é teto de carga |
| config default, save 31 | 4000 | 31 | PASS |
| teto 21, save 25 | 25 | 25 | PASS |
| fora da carga, teto 25, salvo 35 | 25 | — | PASS — piso não vaza |
| `GiveExperience` nível 30, teto 25, novo 31 | 30 | 30 | PASS — não rebate abaixo do atual |

**(C) Contra-prova — replantar o defeito** (`git checkout` dos dois arquivos de volta ao commit
`cd8e4ce`, harness recompilado com o **mesmo** teste): a suíte compila e fica **VERMELHA** por
verificação, exit 1:

```
FAIL loadclamp.voluntary_cap_does_not_downgrade_saved | DOWNGRADE no clamp de carga com teto voluntario: MaxLevel=25 saved=30 -> 25
FAIL loadclamp.vanilla_fallback_does_not_truncate_above_30 | TRUNCADO no fallback vanilla: MaxLevel=20 saved=35 -> 20
FAIL loadclamp.lower_cap_does_not_downgrade_saved | downgrade com teto abaixo do save: MaxLevel=21
RESUMO: PASS=100 FAIL=3 NAO_EXERCITADO=14   (exit 1)
```

Evidência bruta: `docs/automacao/LEVEL-R3F1-evidencias/defeito-replantado-01.txt` / `.json`.

> Nota honesta sobre o modelo do fallback no contra-teste: no código **anterior** o `Policy`
> devolvia o `vanillaValue` direto (30 em jogo) sem passar pelo `PolicyCore`. O teste usa a decisão
> pura porque `Policy.EffectiveMaxLevel` exige um `Character` real; no código anterior o campo
> `VanillaMaxLevel` não existe, então o teto modelado cai em `XpCurve.VanillaCapLevel` = 20. Em
> ambos os casos o valor é < 35, logo o truncamento que a R3-01 descreve é real e o teste o pega.

O teste é deliberadamente tolerante a campos ausentes (`TrySetField` por reflexão): reverter a
correção deixa a suíte vermelha **por verificação**, não por erro de compilação.

## 6. Rodada final (com a correção)

```
dotnet build RoguelikeLevelProgression/RoguelikeLevelProgression.csproj -c Release -p:DeployToBepInEx=false
  -> 0 Erro(s), 1 Aviso(s) (MSB3277 System.Net.Http, pré-existente)
  -> RoguelikeLevelProgression.dll 57856 B  sha256 3c704bcc7877857406c535ae8a61bbe1d4fd8491c07fd623c69a5b60dc3f8c78

dotnet build tests/RoguelikeLevelProgression.Harness/RoguelikeLevelProgression.Harness.csproj
  -> 0 Erro(s), 0 Aviso(s)   RlpHarness.dll sha256 ca2f57aae0fefafc4e324a511c976b42109137bc00dfdc786d0d0402971283bf

dotnet tests/…/bin/Debug/net6.0/RlpHarness.dll <LEVEL-R3F1-evidencias> lib <BepInEx/core> <Managed>
  -> exit 0   RESUMO: PASS=103 FAIL=0 NAO_EXERCITADO=14
```

`103 = 91` (bancada LEVEL-R2, intacta) `+ 12` novas. Os 14 `NAO_EXERCITADO` são os mesmos e
honestos (aplicação real dos patches no Harmony, jogo aberto, níveis 21..31 em jogo, save/reload do
dono, UI TMP, pools reais, multiplayer real, `F20`/`D20` serializados, ciclo de vida BepInEx).

## 7. Limites (o que NÃO foi provado)

Runtime Unity/Harmony real, abrir o jogo, carregar o save do dono, multiplayer real e a aplicação
efetiva dos patches continuam **NAO_EXERCITADO** — como o cartão restringe (sem instalar, sem abrir
o jogo, sem tocar em save/perfil). O que foi provado é: a IL real do clamp, que o getter lido é o
alvo patcheado, e que a decisão real do mod, alimentada como em carga, nunca rebaixa o nível salvo.
