# API-R1 — RUNBOOK do smoke em jogo (BepInEx real) da API-base 0.1.0

> **Tarefa desta preparação:** `t_f32becd0` (API-R1-I1, filha de API-R1 / `t_b7f6fc4a`).
> **Status deste runbook: `PREPARADO_NAO_EXERCITADO`.**
>
> Nada aqui abre ou fecha o jogo, instala no perfil do dono, carrega save ou publica. Nesta tarefa o jogo
> **não foi aberto**, nenhum arquivo foi copiado para o perfil e o runtime do BepInEx continua
> **NÃO_EXERCITADO**. O que este documento entrega é o procedimento com pré-requisitos, comandos
> reproduzíveis, critério de sucesso, critério de falha e rollback — para o **dono** autorizar (ou não) a
> rodada quando quiser.
>
> Partes numeradas da preparação: `docs/automacao/API-R1-I1-parte01.md` (alvo de deploy opt-in e provas),
> `API-R1-I1-parte02.md` (este runbook), `API-R1-I1-parte03.md` (o que fica NÃO_EXERCITADO e o que
> depende do dono). Evidências por comando: `docs/automacao/API-R1-I1-evidencias/`.
>
> Base da API (leia antes): `api/README.md`; identidade do alvo: `api/docs/target-game.json`.

---

## 0. O que a rodada prova — e o que ela NÃO prova

**Prova (é o critério desta rodada):** o BepInEx do perfil carrega o plugin `RealmApi 0.1.0`, a identidade
(versão do jogo **e** hash do `Assembly-CSharp.dll`) bate, o `HookInstallation` instala os **quatro**
hooks do catálogo e o log registra a linha de sucesso com os quatro `HookId`s — sem nenhum `LogError` do
plugin.

**Não prova (declarado):** que os postfixes **disparam** em jogo. Na base 0.1.0 o plugin **não loga
disparo de hook** — `RealmHooks.Observed` sai sem assinante (`api/Core/Contracts.cs:106-111`) e a base não
traz consumidor. Provar disparo exige um consumidor instrumentado ou um contador: frente separada.
"Os quatro ids na linha de instalação" é prova de **instalação**, não de chamada do postfix.

---

## 1. Pré-requisitos (todos obrigatórios; faltando um, não comece)

| # | Pré-requisito | Como conferir (comando reproduzível) | Medido nesta preparação |
|---|---|---|---|
| P1 | **Jogo fechado** e uma única frente controlando o jogo | `powershell -NoProfile -Command "Get-Process -Name 'Stolen Realm' -ErrorAction SilentlyContinue"` (saída vazia) | vazio (`01-perfil-antes.txt`) |
| P2 | **Autorização explícita do dono** para ESTA rodada | registro no cartão/comentário do kanban; sem isso, não instalar | **pendente — este runbook não autoriza nada** |
| P3 | .NET SDK 6.0 | `dotnet --version` | `6.0.428` |
| P4 | BepInEx instalado no perfil | `ls "$P/core" "$P/patchers"`; cabeçalho do log diz a versão | `BepInEx 5.4.23.5` |
| P5 | DLLs da API construídas | `dotnet build api/Plugin/RealmApi.csproj -c Release` → `0 Aviso(s), 0 Erro(s)` | `exit=0` (`03-build-sem-flag.txt`) |
| P6 | **Hash do `Assembly-CSharp.dll` do jogo** confere com `ApiIdentity.AssemblySha256` | `sha256sum "<JOGO>/Stolen Realm_Data/Managed/Assembly-CSharp.dll"` | `8bb4a7c5…855a` (`07-perfil-intacto-e-destino-padrao.txt`) |
| P7 | Impressão digital do perfil **antes** da rodada (para o rollback ter linha de base) | §8.1 | salva em `01-perfil-antes.txt` (hash do conjunto `8d615c0a…a436`) |
| P8 | Nada de backup de DLL dentro de `plugins/` | `find "$P/plugins" -name '*.dll.old' -o -name '*.dll.bak'` | o BepInEx varre `plugins/` **recursivamente**: cópia de DLL lá dentro vira mod carregado |

Variáveis usadas em todo este documento (bash do git-bash; ajuste se o seu ambiente mudar):

```bash
JOGO="/e/SteamLibrary/steamapps/common/Stolen Realm"
P="$HOME/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx"
```

---

## 2. Identidade das builds (conferir ANTES de instalar)

| artefato | caminho | bytes | sha256 |
|---|---|---|---|
| plugin | `api/Plugin/bin/Release/netstandard2.1/RealmApi.dll` | 8192 | `b52b66e5ce85149a624c8f09e695c3fb2d90ebf3f9746e068e727c68811d822c` |
| dependência | `api/Plugin/bin/Release/netstandard2.1/RealmApi.Core.dll` | 11776 | `5cbfcb3292660a9bcf789f4ab477ff5d8e3542b9641ab476a406aa89e847bab8` |
| dependência | `api/Plugin/bin/Release/netstandard2.1/RealmApi.Hooks.dll` | 8704 | `19470274d532fcc2d3c3f0402e0216f3b45bc24a240ab888c56c6fd9522e1b86` |
| alvo do gate | `<JOGO>/Stolen Realm_Data/Managed/Assembly-CSharp.dll` | — | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |

```bash
sha256sum api/Plugin/bin/Release/netstandard2.1/RealmApi.dll \
          api/Plugin/bin/Release/netstandard2.1/RealmApi.Core.dll \
          api/Plugin/bin/Release/netstandard2.1/RealmApi.Hooks.dll \
          "$JOGO/Stolen Realm_Data/Managed/Assembly-CSharp.dll"
```

Identidade declarada no código (a que o plugin confere em runtime): `api/Core/Contracts.cs:15-21` —
GUID `com.gumatos.realmapi`, versão `0.1.0`, `GameVersion` `1.3.1`, `SteamBuildId` `25240684`,
`AssemblySha256` `8bb4a7c5…855a`; o gate é **fail-closed**: versão **ou** hash divergentes ⇒ **zero
hooks** (`ApiIdentity.Matches`, `api/Core/Contracts.cs:24-26`).

A build **não é reproduzível byte a byte** em geral; a identidade é o **hash medido**. Depois de
reconstruir, refaça a tabela acima com `sha256sum` antes de instalar.

---

## 3. Instalação (OPT-IN explícito) e ensaio em arena isolada

O alvo de deploy é `DeployToBepInEx` em `api/Plugin/RealmApi.csproj:29`, com
`Condition="'$(DeployToBepInEx)' == 'true'"`. Sem a flag, **nada** é copiado.

### 3.1 Ensaio em ARENA ISOLADA (recomendado antes de instalar de verdade; não toca o perfil)

```bash
SB="$HOME/AppData/Local/hermes/cache/scratch/api-r1-i1-sandbox"   # pasta VAZIA qualquer
rm -rf "$SB" && mkdir -p "$SB"
dotnet build api/Plugin/RealmApi.csproj -c Release --no-restore \
    -p:DeployToBepInEx=true -p:PluginsDir="$(cygpath -w "$SB")\\"
find "$SB" -type f -exec sha256sum {} +      # os 3 assemblies, hashes = tabela da §2
```

Medido (`06-ensaio-arena-isolada.txt`): o alvo rodou, copiou os **três** assemblies para a arena e os
hashes batem byte a byte com `api/Plugin/bin/Release/netstandard2.1/`. Nada foi escrito no perfil:
`-p:PluginsDir` é propriedade **global** do MSBuild (vence a propriedade interna do alvo).
`--no-restore` exige que o projeto já tenha sido restaurado antes (um build anterior basta). **Não**
tente trocar `$(USERPROFILE)`: o restore/targeting pack dependem dele e o build quebra (testado nesta
tarefa: `146 erros CS0518`).

### 3.2 Instalação real no perfil (só com a autorização do dono)

```bash
dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=true
# saida esperada, com Importance=high:
#   Deploy: RealmApi.dll + RealmApi.Core.dll + RealmApi.Hooks.dll copiados para <PluginsDir>
find "$P/plugins/RealmApi" -type f -exec sha256sum {} +     # 3 arquivos, hashes = §2
```

São instalados os **três** assemblies na **mesma** pasta (`plugins/RealmApi/`): o plugin referencia
`RealmApi.Core.dll` e `RealmApi.Hooks.dll` (project references); sem eles o BepInEx não resolve o plugin
ao carregar.

**Prova de que o padrão não instala** (feita nesta tarefa, `03`/`04`/`05`): `dotnet build
api/Plugin/RealmApi.csproj -c Release` (sem flag) gerou `0 Aviso(s), 0 Erro(s)`, **não** imprimiu a
mensagem `Deploy:` e a impressão digital do perfil (caminho + bytes + mtime + sha256 de `plugins/` e
`config/`) ficou **idêntica** antes × depois (hash do conjunto `8d615c0a…a436` nas duas pontas). Guarda da
raiz sobre `api/`: `python tools/check_deploy_optin.py --raiz api` → `[ ok ] 1 alvo(s) de deploy` (`08`).

---

## 4. Habilitar `Safety.EnableHooks=true` (a config nasce no primeiro boot)

O plugin lê a chave em `Awake` (`api/Plugin/RealmApiPlugin.cs:21`), com **padrão `false`**:

```csharp
if (!Config.Bind("Safety", "EnableHooks", false, "Habilitar somente após autorização de teste em jogo; …").Value)
{ log.LogInfo("RealmApi 0.1.0: hooks desabilitados por Safety.EnableHooks=false"); return; }
```

1. **Boot 1 (instalação, hooks desligados):** com o jogo fechado instale a DLL (§3.2), abra o jogo uma vez
   e feche. O BepInEx **cria** `$P/config/com.gumatos.realmapi.cfg` com `EnableHooks = false`. Esperado no
   log: a linha de "hooks desabilitados" (`RealmApiPlugin.cs:22`).
2. Edite a config e troque o valor:

```ini
[Safety]
## Habilitar somente após autorização de teste em jogo; a versão e hash precisam coincidir.
# Setting type: Boolean
# Default value: false
EnableHooks = true
```

   ```bash
   grep -n "EnableHooks" "$P/config/com.gumatos.realmapi.cfg"    # tem de dizer: EnableHooks = true
   ```

3. **Boot 2 (rodada):** abra o jogo de novo. A config é lida **no boot** — não há hot-reload.

---

## 5. Critério de SUCESSO (ler `<PERFIL>/BepInEx/LogOutput.log`)

Arquivo: `$P/LogOutput.log`. O BepInEx **recria** o log a cada boot; identifique o boot desta rodada pela
primeira linha (ela traz a data/hora), por exemplo:

```
[Message:   BepInEx] BepInEx 5.4.23.5 - Stolen Realm (12/09/2026 21:34:42)
```

| # | O que ler | Como conferir | Aceite |
|---|---|---|---|
| S1 | plugin carregado | `grep -n "Loading \[RealmApi 0.1.0\]" "$P/LogOutput.log"` | 1 linha, **depois** do cabeçalho do boot desta rodada |
| S2 | contagem de plugins | `grep -n "plugins to load" "$P/LogOutput.log"` | 1 a mais que no boot anterior (medido no perfil atual, sem a API: `9 plugins to load`) |
| S3 | **linha de identidade + hooks instalados** | `grep -n "RealmApi 0.1.0: target" "$P/LogOutput.log"` | exatamente a linha abaixo, com os **4** ids |
| S4 | nenhum erro do plugin | `grep -nE "RealmApi: (alvo incompat|instalação recusada)" "$P/LogOutput.log"` | **nenhuma** linha |
| S5 | hash do alvo conferido de forma independente | §2 (comando do `sha256sum`) | igual a `8bb4a7c5…855a` |

Linha de sucesso (literal do código, `api/Plugin/RealmApiPlugin.cs:33`):

```
RealmApi 0.1.0: target 1.3.1 / build-inspecionado 25240684; hooks=game.awake,ui.skill-tree.updated,ui.localized,combat.turn-started
```

Ordem dos ids na linha: a de `HookInstallation.InstalledIds` (dicionário) — **conferir o conjunto**, não a
ordem. Catálogo: `api/Core/Contracts.cs:60-65`.

No `LogOutput.log` cada linha sai como `[Info   :   RealmApi] <mensagem>` / `[Error  :   RealmApi]
<mensagem>` — o BepInEx usa o **nome** do plugin como origem do log (medido no perfil atual, ex.
`[Info   :Better Stats] Better Stats carregado.` em `<PERFIL>/BepInEx/LogOutput.log:41`). Por isso os
greps acima casam o **texto** da mensagem e não o prefixo.

**Nota honesta sobre o hash:** a linha de sucesso **não** imprime o sha256 (só versão e build id). O hash
aparece no log **apenas no caso de divergência** (S4 / §6, linha de recusa). Por isso S5 é obrigatório: a
conferência do hash é feita **pelo operador**, com o comando da §2 — não presuma que o log traz esse dado.

---

## 6. Critério de FALHA (e o que cada sintoma significa)

| Sintoma no `LogOutput.log` | Linha de origem | Significado | Ação |
|---|---|---|---|
| `RealmApi 0.1.0: hooks desabilitados por Safety.EnableHooks=false` | `RealmApiPlugin.cs:22` | config ainda em `false` | refazer §4 (editar + **reabrir** o jogo) |
| `RealmApi: alvo incompatível; nenhum hook instalado. Application.version=… assembly.sha256=…` | `RealmApiPlugin.cs:30` (`LogError`) | **recusa por divergência**: `Application.version` ≠ `1.3.1` ou hash ≠ `8bb4a7c5…855a`; zero hooks instalados | comparar os valores impressos com a §2; se o jogo atualizou de verdade, isto é a trava funcionando — **não** editar a identidade no código sem refazer a análise (`api/README.md`, "Como atualizar") |
| `RealmApi: instalação recusada: <exceção>` | `RealmApiPlugin.cs:35` (`LogError`) | falha ao resolver/patchar (`MissingMemberException`, `MissingMethodException "esperado 1 alvo, encontrados N"`, `Owner/postfix ausente`, duplicidade) — assinatura do jogo mudou ou catálogo inconsistente | rollback (§8) e reabrir a análise do hook citado pela exceção |
| Linha S3 presente, mas com **menos de 4** ids | — | hook não instalado — **não** deve acontecer: `Install` é tudo-ou-nada e desfaz o que já patchou | tratar como falha; anexar o log e bloquear a rodada |
| `[Error` de outro mod | — | não é falha desta rodada, mas contamina a leitura | registrar separadamente; a rodada só julga linhas do `RealmApi` |
| Jogo **fecha/crasha** ao entrar em partida | — | risco residual dos postfixes | rollback imediato (§8), guardar `LogOutput.log` e o `Player.log`, bloquear a rodada |

Regra de leitura: **ausência de linha não é sucesso**. Sem S3, a rodada é `NÃO_EXERCITADO` (não
"verde por omissão").

---

## 7. Encerramento da rodada

Não é um teste de gameplay: o objetivo é o boot e a instalação. Sequência mínima:

1. Boot com a config ligada e, se o dono quiser, uma partida curta (é onde `combat.turn-started` /
   `ui.skill-tree.updated` existiriam) — **observação apenas**.
2. Fechar o jogo **graciosamente** (`CloseMainWindow`); não usar `taskkill` cego.
3. Copiar `LogOutput.log` (e o `Player.log` se houve partida) para fora do perfil, junto das evidências da
   rodada. O `LogOutput.log` fica em `<PERFIL>/BepInEx/LogOutput.log`; o `Player.log` do jogo, em
   `%USERPROFILE%\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm\Player.log` (medido: existe,
   1259021 bytes). **Não** guardar cópia de DLL dentro de `plugins/`.
4. Aplicar §8 (rollback) e conferir a impressão digital contra a linha de base de P7.

---

## 8. ROLLBACK (dois níveis; o executor decide pelo risco)

### 8.1 Linha de base (antes de instalar)

```bash
for base in "$P/plugins" "$P/config"; do find "$base" -type f | sort | while read -r f; do
    printf "%s  %s  %s  %s\n" "${f#$base/}" "$(stat -c %s "$f")" "$(stat -c %y "$f" | cut -d. -f1)" \
        "$(sha256sum "$f" | cut -d' ' -f1)"; done; done > perfil-antes.txt
grep -cE '  [0-9]+  [0-9]{4}-[0-9]{2}-[0-9]{2} ' perfil-antes.txt   # medido nesta preparacao: 30 arquivos
```

### 8.2 Nível 1 — desligar os hooks (rollback de 10 segundos, não exige remover arquivo)

```bash
# com o JOGO FECHADO: edite $P/config/com.gumatos.realmapi.cfg e volte para
#   EnableHooks = false
```

Efeito: no próximo boot o plugin registra "hooks desabilitados" e **nenhum** postfix é instalado
(`RealmApiPlugin.cs:21-22`). É o rollback preferido quando o objetivo é só parar de observar.

### 8.3 Nível 2 — desinstalar do perfil

```bash
# com o JOGO FECHADO:
rm -rf "$P/plugins/RealmApi"                       # os 3 assemblies (pasta criada pelo deploy)
rm -f  "$P/config/com.gumatos.realmapi.cfg"        # opcional: apaga a config do plugin
test -e "$P/plugins/RealmApi" && echo RESIDUO || echo "perfil limpo"
```

Se você guardou cópia do `LogOutput.log`/evidência, guarde **fora** do perfil. Backup de DLL **nunca**
dentro de `plugins/`: o BepInEx varre `plugins/` recursivamente e o arquivo passa a ser varrido como mod.

### 8.4 Prova de perfil limpo

```bash
for base in "$P/plugins" "$P/config"; do find "$base" -type f | sort | while read -r f; do
    printf "%s  %s  %s  %s\n" "${f#$base/}" "$(stat -c %s "$f")" "$(stat -c %y "$f" | cut -d. -f1)" \
        "$(sha256sum "$f" | cut -d' ' -f1)"; done; done > perfil-depois.txt
diff perfil-antes.txt perfil-depois.txt     # sem saida = perfil identico a linha de base
grep -ril RealmApi "$P/plugins" "$P/config" | wc -l   # tem de ser 0
```

O grep de resíduo olha **exatamente** `"$P/plugins"` e `"$P/config"` — o mesmo escopo da linha de base de
8.1 —, de propósito:

- `$P/LogOutput.log` fica **fora**: ele é a evidência da rodada e **cita** o mod (a linha de identidade
  `RealmApi 0.1.0: target …` do §5 S3 sai dele). Se ele entrasse no grep, uma rodada bem-sucedida seguida de
  rollback bem-sucedido acusaria "resíduo" — contradição com o `diff`, que estaria limpo.
- `$P/cache/` (por exemplo `cache/chainloader_typeloader.dat`) também fica fora: é índice interno do
  BepInEx e casa nome de mod instalado.
- O `LogOutput.log` **não** entra na impressão digital de propósito (o jogo escreve nele no boot). Todo o
  resto de `plugins/` e `config/` tem de voltar byte a byte ao estado de 8.1.

Se quiser conferir por que o escopo é só esse, rode os dois e compare (a diferença é o próprio log):

```bash
grep -ril RealmApi "$P" | wc -l                        # >= 1 depois de uma rodada (o LogOutput.log)
grep -ril RealmApi "$P/plugins" "$P/config" | wc -l    # tem de ser 0 = sem residuo em plugins/ e config/
```

---

## 9. NÃO_EXERCITADO nesta preparação (declaração explícita)

- **Runtime BepInEx/Unity: NÃO_EXERCITADO.** O jogo **não foi aberto** nesta tarefa; nenhuma linha deste
  runbook foi executada em sessão viva. O plugin nunca foi carregado pelo jogo.
- **Instalação no perfil `r2modman`: NÃO_EXERCITADA.** O deploy real (§3.2) **não** foi executado: o que se
  provou é (a) o build padrão não instala (§3, provas `03`/`04`/`05`) e (b) o alvo funciona, em **arena
  isolada** (§3.1, prova `06`).
- **Habilitar `Safety.EnableHooks=true` e ler o log: NÃO_EXERCITADO** (§4, §5).
- **Disparo dos quatro hooks: NÃO_EXERCITADO** — e, na base 0.1.0, **não é observável pelo log** (§0).
- **Rollback: NÃO_EXERCITADO em jogo** (§8) — o procedimento é comando, os caminhos foram medidos, mas
  nada foi instalado para depois remover.
- **Publicação (Thunderstore): não feita** — ato separado e explicitamente autorizado.
- **`Assembly-CSharp.dll`: não modificado e não redistribuído.** A API é **observacional** (quatro
  postfixes); nenhuma capacidade de cancelar/substituir argumento ou resultado.

---

## 10. Rastreabilidade

- Alvo de deploy opt-in: `api/Plugin/RealmApi.csproj:29` (alvo `DeployToBepInEx`), comentário acima dele.
- Evidências por comando: `docs/automacao/API-R1-I1-evidencias/01`…`10`
  (`01`/`04`/`05` impressão digital do perfil antes × depois; `02`/`08` guarda do opt-in; `03` build sem
  flag; `06` ensaio em arena isolada; `07` perfil intacto + destino padrão; `08` smoke offline 25/25;
  `09` tentativa descartada via `-p:USERPROFILE`; `10` correções da revisão rodada 1 — escopo do grep de
  resíduo, linha do alvo e contagem de linhas).
- Partes da tarefa: `docs/automacao/API-R1-I1-parte01.md`, `parte02.md`, `parte03.md`, `parte04.md`.
- Base da API: `api/README.md`, `api/docs/target-game.json`, `api/docs/smoke-result.json`.
- Gate de deploy da raiz: `Directory.Build.props`, `tools/check_deploy_optin.py`,
  `tools/release-check.sh` (modo `--instalar-no-perfil` é o único caminho que passa
  `-p:DeployToBepInEx=true`).

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
