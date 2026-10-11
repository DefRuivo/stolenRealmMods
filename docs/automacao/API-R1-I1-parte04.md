# API-R1-I1 — parte 04: correções da revisão (rodada 1)

Tarefa `t_f32becd0`. Partes anteriores: `API-R1-I1-parte01.md` (deploy opt-in e provas),
`API-R1-I1-parte02.md` (runbook), `API-R1-I1-parte03.md` (NÃO_EXERCITADO e pendências do dono).

Esta parte existe porque a revisão da rodada 1 pediu mudanças (`kanban_request_changes`): 3 defeitos
concretos, todos de **documento** — nenhuma linha de código, `csproj`, DLL ou perfil foi tocada nesta
rodada. Mesmo escopo do cartão: preparar, não executar runtime.

## 1. Defeito D1 — o grep de resíduo do §8.4 tinha escopo largo demais

**Onde:** `docs/automacao/API-R1-runbook-runtime.md`, §8.4 (era a linha 263).

**Era:** `grep -ril RealmApi "$P" | wc -l   # tem de ser 0`.

**Por que estava errado:** o alcance do grep cobria o perfil **inteiro**, mas a impressão digital do §8.1
só olha `$P/plugins` e `$P/config`. Dois caminhos fora desse par sempre casam o nome do mod:

- `$P/LogOutput.log` — é a **evidência** da rodada e cita o mod por projeto (§5 S3 manda ler
  `RealmApi 0.1.0: target …` exatamente nesse arquivo, e o §7.3 só o **copia** para fora, não o remove).
- `$P/cache/` (ex.: `cache/chainloader_typeloader.dat`) — índice interno do BepInEx, que casa nome de
  qualquer mod instalado, não só deste.

Ou seja: a linha pedia 0 e uma rodada bem-sucedida seguida de rollback bem-sucedido devolvia ≥1 — o
operador leria "resíduo" com o `diff` do mesmo bloco limpo. O critério era **inatingível**, não apenas
ambíguo.

**Correção aplicada** (escopo idêntico ao da linha de base):

```bash
grep -ril RealmApi "$P/plugins" "$P/config" | wc -l   # tem de ser 0
```

E o texto abaixo do bloco passou a explicar **por escrito** por que `LogOutput.log` e `cache/` ficam de
fora, com um par de comandos para o operador conferir a diferença (um devolve ≥1, o outro 0).

**Prova reproduzida nesta rodada** (`docs/automacao/API-R1-I1-evidencias/10-correcoes-revisao-rodada1.txt`,
bloco D1): perfil falso com `plugins/` e `config/` **vazios**, `LogOutput.log` pós-rodada e
`cache/chainloader_typeloader.dat`:

- `grep -ril RealmApi "$P" | wc -l` → **2** (o log e o cache — a versão antiga)
- `grep -ril RealmApi "$P/plugins" "$P/config" | wc -l` → **0** (a versão corrigida, e o perfil está de fato limpo)

## 2. Defeito D2 — citação da linha do alvo no §10

**Onde:** `docs/automacao/API-R1-runbook-runtime.md`, §10 (era a linha 290).

**Era:** `api/Plugin/RealmApi.csproj:28`. **Está em:** `api/Plugin/RealmApi.csproj:29` — a linha 28 é o
`-->` que fecha o comentário acima do alvo. O §3 do mesmo runbook (linha 84) já citava 29, então o próprio
arquivo se contradizia.

**Correção:** §10 agora diz `api/Plugin/RealmApi.csproj:29`.

**Prova:** `grep -n '<Target Name="DeployToBepInEx"' api/Plugin/RealmApi.csproj` → `29:`; e
`grep -n 'RealmApi.csproj:2' docs/automacao/API-R1-runbook-runtime.md` → linhas 84 e 305, **ambas 29**
(evidência 10, bloco D2).

## 3. Defeito D3 — contagem de linhas do runbook na parte 02

**Onde:** `docs/automacao/API-R1-I1-parte02.md:7`.

**Era:** "(296 linhas)". Medido antes das correções: `wc -l` = 298. Depois das correções D1/D2 e da
atualização do §10 (que acrescentou as evidências `09`/`10` e a `parte04` à rastreabilidade):
`wc -l docs/automacao/API-R1-runbook-runtime.md` = **315**, e é esse o número que ficou na parte 02.

**Correção:** `docs/automacao/API-R1-I1-parte02.md:7` agora diz "(315 linhas)" — valor medido por `wc -l`,
não estimado.

## 4. Verificação final desta rodada (comandos e saída)

```bash
wc -l docs/automacao/API-R1-runbook-runtime.md          # contagem publicada em parte02
grep -n 'RealmApi.csproj:2' docs/automacao/API-R1-runbook-runtime.md
grep -n 'tem de ser 0' docs/automacao/API-R1-runbook-runtime.md
python tools/check_deploy_optin.py --raiz api
dotnet build api/Plugin/RealmApi.csproj -c Release      # sem flag: nao instala
api/Smoke/bin/Release/net472/RealmApi.Smoke.exe lib/Assembly-CSharp.dll api/Plugin/bin/Release/netstandard2.1/RealmApi.dll
```

Nada disto abre o jogo: são as mesmas provas de `parte01`/`parte03`, re-rodadas só para confirmar que uma
rodada de edição de **documento** não mexeu em código nem no perfil do dono. A impressão digital do perfil
(`$P/plugins` + `$P/config`, caminho/bytes/mtime/sha256) tem de continuar idêntica à linha de base
registrada em `01`/`04`/`05`/`07` (30 arquivos, hash do conjunto `8d615c0a…a436`).

## 5. O que continua NÃO_EXERCITADO

Nada muda em relação à `parte03`: **o jogo não foi aberto nesta rodada** e nenhuma linha do runbook foi
executada em sessão viva. Runtime BepInEx/Unity, instalação real no perfil, `Safety.EnableHooks=true`,
disparo dos 4 hooks e rollback em jogo seguem `NÃO_EXERCITADO` — dependem de autorização explícita do dono
(as decisões continuam listadas na `parte03` §2).
