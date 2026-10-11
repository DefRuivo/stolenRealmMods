# DBG-R2 — Parte 02: implementação, build e fontes intocadas

Cartão `t_3b7c681b`. Esta parte registra o que mudou no mod, o que **não** mudou (com hash), e o
build de verificação. Nada foi instalado, publicado ou rodado no jogo.

## 1. Arquivos do mod

| arquivo | estado | sha256 antes (11/10/2026) | sha256 depois |
|---|---|---|---|
| `RoguelikeDebugger/Proveniencia.cs` | **NOVO** | — | `e1536451657876a0ae20eefc94185f558b33fa1bcc58f50fb60975e054e4debd` |
| `RoguelikeDebugger/Plugin.cs` | editado (aditivo) | `6dc931a826074f90c867dc785e6c5b5a9ee947e311002cc8107a4b714947a41c` | `122cd813cb9a456bf2594b53608fdea3cdd4299fb0383ee74315e0fe044d06b1` |
| `RoguelikeDebugger/EfeitosInfo.cs` | **intocado** | `69ffbf2ccaaee4471e0ba882b494a6e512e8c2fec9a3aa0bc226b83e2e45a450b` | idêntico |
| `RoguelikeDebugger/Patches/*.cs` (10) | **intocados** | ver lista em §1.1 | idênticos |
| `RoguelikeDebugger/RoguelikeDebugger.csproj` | **intocado** | `d2df3d9a130b3a80f14ec35f1104c119f78fccf0c247cbccaa5ed36b6c648541` | idêntico |

Comando da conferência (13 fontes antes → 14 depois, só o novo e o `Plugin.cs` mudando):

    cd /c/dev/stolen-realm
    sha256sum RoguelikeDebugger/*.cs RoguelikeDebugger/Patches/*.cs RoguelikeDebugger/RoguelikeDebugger.csproj
    diff <(antes) <(depois)

### 1.1 Hashes dos 10 ganchos existentes (inchanged, gravados no teste)

```
ActionStatusInventoryPatch  77748b53441feecdf8c92310867e0f3d0953d67519b939ebc44190f0d598e140
EventRollDebugPatch         b2d8fcdf318e616236acedcaed8c0ff4947a07cb3b23d92fdf07471739cb1c18
ExpDebugPatch               45e21c5a49d1106e64b0c66b3710f32f13df3211bb48062fcda8fa295c778d1e
FlameShrineProcPatch        4988abbf136d7699775efc71f9a900505b1e0591c8f41fb340fb4dd80d5a0a11
GoldModifierDebugPatch      d3ab912bbbfe4b9a32e13a6f6daba146fdeb63579e9939d95d7670ac11d30384
ItemInventoryPatch          d67663c092347e17f63f702da24c406d76ae8382b88f3ddc170df3067f4fb36b
LifeStealDebugPatch         ee9a54896b34d57796a4e1d27f1e24c6bc0623cfaf35214985457ae24ab91a7c
LootModifierDebugPatch      1a81a879a1af2636df3bfd35bd0124993f31435494a49b18e4f4a82cf1474b59
PowerupInventoryPatch       41cc5596459569b4af7e0e70c27075c641159d70a9bfac2b80b5e2d6cdb7b7e8
SkillInventoryPatch         629d1d1f07e697996da020fa0a9f6c30b7cc592b01a48c83f53bf406ff6e02b1
```

Esses valores estão **codificados no teste puro** (`tools/testes/regras_proveniencia.py`,
`INTOCADOS`): se qualquer gancho for reescrito, o teste reprova. O limite "não reescrever os 14
ganchos existentes" deixa de depender de inspeção manual.

## 2. O que o `Plugin.cs` ganhou (e nada mais)

Aditivo, sem tocar em gancho:

1. `Proveniencia.Cabecalho()` **antes** de `AplicarPatches()` — identidade antes de qualquer patch;
2. `AplicarPatches()` passou a devolver um `ResumoGanchos` (total/ok/métodos/falhas/nomes
   aplicados). O log antigo (`gancho aplicado — X (n metodo(s))` e o resumo `n/n`) **não mudou de
   texto**; o resumo só deixou de ser uma variável local chamada `resumo` e virou `linhaResumo`;
3. `Proveniencia.Estado(...)` depois dos patches — `ABERTO` ou `PARCIAL` (algum gancho falhou),
   `matrizFlame=aplicada|ausente` e `modoLeitura=passivo|ativo`;
4. `Application.quitting += AoFechar` → `Proveniencia.Fim("saida-do-jogo")`.
5. `using UnityEngine;` (para `Application`/`Application.version`/`Application.dataPath`).

`Proveniencia.cs` (novo, ~360 linhas) mede: versão do jogo (`Application.version`), sha256 do
`Assembly-CSharp` **carregado** (pelo `Location` da assembly), sha256 do próprio DLL, build Steam
(`appmanifest_1330000.acf`, duas pastas acima da raiz do jogo), sessão em ISO-8601 UTC, identidade
da API por reflexão, e classifica o estado do dump. Toda leitura que falha vira o literal
`desconhecido` — nenhum campo obrigatório pode sair vazio.

## 3. Build de verificação (cópia isolada, sem deploy)

Cópia isolada em `$HERMES_KANBAN_WORKSPACE/isolado` (fontes + `lib/` + `Directory.Build.props`),
fora da árvore do dono:

    cd <workspace>/isolado/RoguelikeDebugger
    dotnet build RoguelikeDebugger.csproj -c Release -p:DeployToBepInEx=false

- **0 Erros**, 1 Aviso (`MSB3277`, conflito de `System.Net.Http` vindo da referência a
  `Assembly-CSharp.dll`). O aviso **não** foi introduzido por este cartão: o mesmo build na cópia de
  controle, com o `Plugin.cs` original do git e sem `Proveniencia.cs`, dá exatamente `1 Aviso(s) /
  0 Erro(s)`.
- DLL gerada: `bin/Release/netstandard2.1/RoguelikeDebugger.dll`, sha256
  `a3bdc06e0de98a078d57b03e75138cde23a4b1a87cfb9acae97e68393ed6e8e3`.
- **Nada foi instalado**: o DLL do perfil do r2modman segue com sha256
  `55bc6250a90522f776b19dc874060fe274a27b9f0901b57720047d85314734e6` e mtime de 07/10/2026 —
  idêntico ao medido antes do build.
- Log integral: `docs/automacao/DBG-R2-parte02-build.log` (33 linhas, codificação do console do
  Windows/cp1252 — os acentos aparecem "quebrados" em leitor UTF-8; é o log bruto do comando, sem
  transcrição). Linhas decisivas: `Compilação com êxito.` / `1 Aviso(s)` / `0 Erro(s)`;
  sha256 do log `70ac7cf544ec1c2234460883f1845961483dc886dfa869c370643ce5bdea79ac`.

### 3.1 Por que o sha256 da DLL gerada não substitui o runtime

`dllDebugger`/`sha256Dll` no carimbo são medidos **em runtime**, pelo `Location` da assembly
carregada. O hash do artefato desta rodada (`a3bdc06e…`) só confere se o DLL for recompilado igual;
por isso o verificador exige 64 hex e **não** compara com um valor fixo — comparar com a DLL do dia
seria falsear o instrumento. É por isso também que a fixture positiva usa esse hash apenas como
exemplo de formato real desta rodada.

## 4. Dependência opcional da API — prova

    cd /c/dev/stolen-realm
    # (a) sem referência de projeto -> 0, rc=1
    grep -n "RealmApi\|Gumatos" RoguelikeDebugger/RoguelikeDebugger.csproj     ; echo "rc=$?"
    rc=1
    # (b) sem `using Gumatos.*` nem tipo da API por compilação -> 0, rc=1
    grep -rn "using Gumatos" RoguelikeDebugger/                               ; echo "rc=$?"
    rc=1

> Correção de prova (review rodada 1, item 2): a linha anterior citava
> `grep -rn "RealmApi" RoguelikeDebugger/*.cs RoguelikeDebugger/Patches/*.cs # 0` — esse comando
> **não** dá 0 (dá o literal do nome do tipo em `Proveniencia.cs:395` e a doc em `:42`). A prova de
> "sem referência" são (a) e (b) acima; o contato real é a **string** do nome do tipo, resolvida por
> reflexão.

O único contato é por **reflexão**, com o nome do tipo como string:
`"Gumatos.RealmApi.ApiIdentity"` (`Proveniencia.cs`, `SondaApi`), e o `EnableHooks` é lido do
`.cfg` da API (`BepInEx/config/com.gumatos.realmapi.cfg`). Ausente/desligada, o debugger segue com
`identidade=local` e `apiPresente=nao` — sem exceção, sem dependência.

## 5. NAO_EXERCITADO

- Runtime: nenhum arranque do jogo; as linhas do carimbo **nunca** foram emitidas de verdade. O
  que está provado é o formato, o contrato e o comportamento do verificador sobre fixtures
  (parte 03).
- `Application.quitting` como sinal de fechamento: comportamento conhecido da Unity 2022.3, não
  medido em partida. Se o jogo for morto de forma abrupta (kill, crash), o rodapé não sai e o
  veredito é TRUNCADO — que é o comportamento desejado, mas isso ainda não foi observado em jogo.
- Leitura do `appmanifest`: exercitada apenas pela fixture; em runtime depende do layout Steam.
