# DBG-R2 — Parte 01: escopo fechado, fatia P0 e desenho do instrumento

Cartão `t_3b7c681b` (INT-R1-C3). Nasce da auditoria DBG-R1 (`t_9e2325d7`, aprovada em review) e da
API própria (`t_b7f6fc4a`, done). **Nada aqui foi exercitado em jogo** — a rodada é offline.

> **Onde estão os artefatos do cartão pai (review rodada 1, item 4).** `DBG-R1-parte07.md` e
> `DBG-R1-parte05-matriz.csv` são citados neste documento mas **não existem na árvore do
> repositório** (`find . -path ./scratch -prune -o -path ./.worktrees -prune -o -name "*DBG-R1*"
> -print` → 0 linhas; a árvore só tem `docs/automacao/DBG-R2-*`). Eles estão no pacote de entrega do
> cartão `t_9e2325d7`:
> `C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_9e2325d7\DBG-R1-entrega.zip`
> (entradas `docs/automacao/DBG-R1-parte05-matriz.csv` e `docs/automacao/DBG-R1-parte07.md`); o
> `DBG-R1-parte07.md` também está solto nessa mesma pasta. Os números usados aqui foram conferidos
> dentro desse ZIP: a matriz tem 20 linhas (8 P0 / 8 P1 / 3 P2 / 1 P3).

## 1. O problema, medido

Os censos `docs/cobertura/*.csv` são gerados por `tools/census.py` a partir do **dump de boot do
RoguelikeDebugger** (`LogOutput.log` do perfil). O censo lê linhas no formato
`[Info   :Roguelike Debugger] [<Categoria>] '<nome>' | chave=valor | ...` (regex `LINE`/`FIELD`/`DESC`
em `tools/census.py:52-66`).

O que o dump **não** diz hoje, e que a auditoria elegeu como lacuna nº 1
(`DBG-R1-parte07.md` §1 — arquivo do ZIP da entrega do pai, ver o quadro no topo):

1. **Qual DLL foi observada.** A ausência de um dado no CSV pode ser (a) o jogo não tem o dado ou
   (b) o dump veio de outro build — e as duas leem igual.
2. **Se o dump terminou.** `LogOutput.log` é truncado a cada arranque do BepInEx e não tem rodapé:
   sessão interrompida e sessão completa são indistinguíveis.
3. **Quem observou.** A DLL do debugger (versão/hash) não aparece no dump.
4. **Se a leitura foi passiva.** Anotado, **não consertado aqui** (§4).

### 1.1 Prova de que o debugger só LÊ arquivos (não há sidecar de runtime)

O que se quer provar é que o debugger **não escreve** arquivo nenhum em runtime — logo o escopo
"cada dump/sidecar" se resolve em **um** instrumento: o próprio fluxo de log.

    cd /c/dev/stolen-realm
    # escritas de runtime no debugger -> 0 ocorrências (rc=1)
    grep -rn "StreamWriter\|File\.WriteAll\|File\.AppendAll\|File\.Create\|File\.OpenWrite" \
        --include=*.cs RoguelikeDebugger/ | grep -v /obj/ ; echo "rc=$?"
    rc=1
    # varredura ampla, para NÃO esconder as leituras que existem -> 9 ocorrências, todas de leitura
    grep -rn "File\.\|Path\.\|StreamWriter\|WriteAll" --include=*.cs RoguelikeDebugger/ \
        | grep -v /obj/ | wc -l
    9

As 9 são **exatamente** leituras: `File.OpenRead` (1), `File.Exists` (2), `File.ReadAllLines` (2),
`Path.Combine`/`Path.GetFullPath`/`Path.GetDirectoryName` (4) — todas em
`RoguelikeDebugger/Proveniencia.cs`, linhas 233, 260, 261, 262, 267, 319, 493, 494 e 499. Nenhum
`StreamWriter`, nenhuma escrita, nenhum arquivo de runtime.

> Correção de prova (review rodada 1, item 1): a versão anterior deste parágrafo citava o comando
> amplo com o resultado "(0 ocorrências)", que **não reproduz** — ele lista as 9 leituras de
> `Proveniencia.cs` (criadas pela própria implementação deste cartão). Ficam separadas as duas
> medidas: **0 escritas** (o que o cartão precisa provar) e **9 leituras** (o número real do comando
> amplo).

Ou seja: o escopo "cada dump/sidecar" se resolve em **um** instrumento — o cabeçalho/rodapé de
proveniência no próprio fluxo de log. Os `*.csv` são **derivados offline** (`tools/census.py`) e
herdam a proveniência do log de origem; não existe segundo arquivo de runtime para carimbar.

## 2. Desenho: bloco `DBG-PROV-V1` no fluxo do debugger

Três linhas, todas com o mesmo marcador de versão do formato (`DBG-PROV-V1`) para o verificador
ancorar. Campos separados por ` | `, no mesmo estilo do dump atual.

```
[Roguelike Debugger] [Proveniencia] DBG-PROV-V1 inicio | versaoJogo=1.3.1 | buildSteam=25240684 | sha256Alvo=<64hex> | dllDebugger=RoguelikeDebugger@0.1.2 | sha256Dll=<64hex> | identidade=<api|local> | apiPresente=<sim|nao> | apiEnableHooks=<sim|nao|desconhecido> | apiVersao=<v|-> | apiSha256=<64hex|-> | alvoConforme=<sim|nao|indeterminado> | inicioEm=<ISO-8601 UTC> | estadoDump=INICIADO
[Roguelike Debugger] [Proveniencia] DBG-PROV-V1 estado | estadoDump=<ABERTO|PARCIAL> | ganchosOk=<n>/<n> | ganchosFalhos=<nenhum|lista> | metodos=<n> | matrizFlame=<aplicada|ausente> | modoLeitura=<passivo|ativo>
[Roguelike Debugger] [Proveniencia] DBG-PROV-V1 fim | estadoDump=FECHADO | motivo=saida-do-jogo
```

Este esboço reflete o formato **implementado** — os campos exigidos pelo verificador
(`OBRIGATORIOS_INICIO`/`OBRIGATORIOS_ESTADO`/`OBRIGATORIOS_FIM` em
`tools/verifica_proveniencia_debugger.py:51-57`) e o emitido pelo C#
(`RoguelikeDebugger/Proveniencia.cs`: cabeçalho, `Estado(...)`, `Fim(...)`). A descrição de
referência campo-a-campo é `docs/DBG-PROVENIENCIA.md`.

> Correção de prova (review rodada 1, item 3): a versão anterior deste esboço omitia `inicioEm=` na
> linha `inicio` e `matrizFlame=`/`modoLeitura=` na linha `estado` — os três são **exigidos** pelo
> verificador e emitidos pelo C#, e o esboço era o único lugar desatualizado.

Regras de decisão do desenho:

- **O cabeçalho sai ANTES de aplicar os patches.** Se o arranque morrer no meio, a identidade já
  está no log (é justamente o caso em que o dump fica pela metade e alguém leria a falta como fato).
- **O rodapé sai em `Application.quitting`** (mesmo evento que a API usa em
  `api/Plugin/RealmApiPlugin.cs:32`). É o único sinal de "o dump fechou" disponível sem inventar
  heartbeat.
- **`sha256Alvo` é calculado, não digitado**: hash do arquivo da assembly do jogo carregada
  (`Assembly-CSharp`), pelo `Location` dela — mesma técnica de `RealmApiPlugin.cs:25-28`.
- **`buildSteam` vem do `appmanifest_1330000.acf`** (pai do diretório do jogo, layout padrão Steam).
  Se não der para ler, o campo sai **explícito** como `desconhecido` — nunca vazio e nunca estimado.
- **`identidade=api` só quando a API existe E `EnableHooks=true`** (lido do `.cfg` da API). Nos
  demais casos `identidade=local` com `apiPresente`/`apiEnableHooks` declarados. A API é lida por
  **reflexão** e **nunca** por referência de projeto: o debugger continua funcionando sozinho
  (dependência opcional declarada no log). Prova em §5.
- **Fail-closed do lado de quem lê**: o verificador (§3) reprova dump sem cabeçalho; **não** existe
  caminho em que a ausência do bloco passe como "tudo certo".

## 3. Verificador (offline, stdlib, sem jogo)

`tools/verifica_proveniencia_debugger.py <log> [--alvo api/docs/target-game.json]`

| veredito | exit | quando |
|---|---|---|
| APROVADO (dump completo) | 0 | cabeçalho com **todos** os campos exigidos preenchidos, sha256 em 64 hex, `buildSteam` conhecido, linha `estado` com `ABERTO`, linha `fim` com `FECHADO` e (com `--alvo`) `sha256Alvo` batendo com o alvo |
| TRUNCADO (proveniência ok, dado incompleto) | 2 | falta a linha `fim`, ou `estadoDump=PARCIAL`, ou identidade incompleta (`buildSteam=desconhecido`) |
| REPROVADO | 1 | sem cabeçalho `DBG-PROV-V1`, campo obrigatório ausente/vazio, sha256 fora de 64 hex, ou divergência com `--alvo` |

O veredito 2 existe de propósito: um dump com proveniência válida mas **não fechado** não pode ser
lido como "o dado não existe". Só o 0 libera essa leitura.

## 4. Fatia P0 da auditoria: o que ESTE cartão cobre e o que fica FORA

A matriz é `DBG-R1-parte05-matriz.csv` — **esse caminho não existe na árvore do repositório**
(`find . -path ./scratch -prune -o -path ./.worktrees -prune -o -name "*DBG-R1*" -print` → 0); ele
está dentro de
`C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_9e2325d7\DBG-R1-entrega.zip`, entrada
`docs/automacao/DBG-R1-parte05-matriz.csv`, na mesma pasta do `DBG-R1-parte07.md` solto. A matriz tem
20 linhas (8 P0, 8 P1, 3 P2, 1 P3) — contagem conferida dentro do ZIP. Os P0 que tocam
proveniência/integridade/passividade:

| id | lacuna (resumo) | neste cartão |
|---|---|---|
| **DBG16** | logs sem envelope temporal; sem hash da DLL realmente carregada nem sessão | **COBERTO** — é o núcleo deste cartão: `sha256Alvo` + `sha256Dll` + `buildSteam` + `identidade` + marcador de fim. Envelope **por registro** (frame/owner em cada linha) fica FORA (é P0 de outro cartão; aqui o envelope é o do dump). |
| **DBG20** | verde offline não prova cobertura nem integridade; falta controle negativo | **COBERTO EM PARTE** — controle negativo obrigatório (`dump sem cabeçalho` reprovado, provado vermelho→verde). Os demais cenários do P0 (joins de idioma, fronteiras, schema) ficam FORA. |
| **DBG01** | classe de gancho vazia conta como OK; alvo não comprova disparo | **NÃO COBERTO** — só o **relatório** de contagem entra na linha `estado` (`ganchosOk=n/n`, `ganchosFalhos=...`). Falhar classe vazia de saúde e contador de disparo por patch ficam FORA. |
| **DBG02** | contagem estável não garante lista completa por categoria | **FORA** (snapshot por GUID/fingerprint por categoria é outro cartão). |
| **DBG03** | exceção no 1º item pode abortar o laço de status/itens | **FORA** (guarda por campo/entrada é outro cartão). |
| **DBG05** | CSV principal não transporta tags; sidecar mecânico versionado | **FORA** (sidecar mecânico é outro cartão; aqui não se muda schema de CSV). |
| **DBG06** | dedup nome+descrição pode colapsar níveis de powerup | **FORA** (chave categoria/GUID/nível é outro cartão). |
| **DBG14** | matriz Flame não é observação passiva estrita (`EvalVoid` + escrita em `MissingExpressions`) | **FORA, registrado aqui** (§4.1). Não implementar gate ativo neste cartão. |

P1/P2/P3 (DBG04, DBG07–DBG13, DBG15, DBG17–DBG19) **não são escopo** — nem implementação nem
prova.

### 4.1 Registro do achado de passividade (não consertado aqui)

A matriz Flame altera estado: `RoguelikeDebugger/Patches/FlameShrineProcPatch.cs:278-284,350`
chamam `EvalVoid` e escrevem em `MissingExpressions`. Logo um dump gerado com a matriz ligada **não é
leitura estrita**: o próprio instrumento provoca a escrita que registra. Neste cartão isso vira
**campo do instrumento, não correção**: a linha `estado` do bloco declara
`modoLeitura=<passivo|ativo>` — `ativo` quando há matriz Flame aplicada, `passivo` caso contrário.
O gate ativo separado, default off, com teste que detecta escrita em cache, é trabalho de outro
cartão (P0 DBG14).

## 5. Como a dependência da API fica OPCIONAL (e provada)

O que se prova é duplo: **(a)** o `.csproj` do debugger não referencia a API, e **(b)** nenhum tipo
da API é usado por compilação — o único contato é o **literal da string** do nome do tipo, resolvido
por reflexão.

    cd /c/dev/stolen-realm
    # (a) sem referência de projeto -> 0, rc=1
    grep -n "RealmApi\|Gumatos" RoguelikeDebugger/RoguelikeDebugger.csproj ; echo "rc=$?"
    rc=1
    # (b) sem `using Gumatos.*` no debugger -> 0, rc=1
    grep -rn "using Gumatos" RoguelikeDebugger/ ; echo "rc=$?"
    rc=1
    # inventário do contato real (é string, não compilação):
    grep -rn "RealmApi" RoguelikeDebugger/ | grep -v /obj/
    RoguelikeDebugger/Plugin.cs:41:            // Mesmo evento que a API usa (api/Plugin/RealmApiPlugin.cs:32).
    RoguelikeDebugger/Proveniencia.cs:42:    /// Quando o `RealmApi` (`Gumatos.RealmApi.ApiIdentity`) esta' carregado E com `EnableHooks=true`
    RoguelikeDebugger/Proveniencia.cs:395:                        tipo = assemblies[i].GetType("Gumatos.RealmApi.ApiIdentity", false, false);

> Correção de prova (review rodada 1, item 2): a versão anterior citava
> `grep -rn "RealmApi" RoguelikeDebugger/` como prova de "0". O comando **não** dá 0 — dá as 3 linhas
> acima (o literal em `Proveniencia.cs:395`, a doc em `:42` e um comentário em `Plugin.cs:41`). As
> provas válidas são (a) e (b); o contato que existe é o literal da string, o que **reforça** a
> propriedade "dependência opcional" em vez de contradizê-la.

A leitura da identidade da API é por `AppDomain.CurrentDomain.GetAssemblies()` → tipo
`Gumatos.RealmApi.ApiIdentity` → campos por reflexão. Ausente a API, o debugger **não** falha: loga
`identidade=local apiPresente=nao` e segue com o dado calculado localmente.

## 6. Aceite deste cartão (o que será provado nas partes seguintes)

1. parte numerada (esta e as seguintes);
2. verificador que **reprova** dump sem proveniência — caso negativo obrigatório, provado
   vermelho→verde (log de execução dos testes na parte 03);
3. `dotnet build` do mod com **0 erros** em cópia isolada com `-p:DeployToBepInEx=false`;
4. fontes do debugger conferidas por sha256 antes/depois (só `Plugin.cs` muda; os 10 arquivos de
   `Patches/*.cs` ficam com hash idêntico);
5. runtime em jogo declarado **NAO_EXERCITADO**.

Limites respeitados: sem instalar, sem abrir o jogo, sem publicar, sem reescrever os ganchos
existentes, sem editar `Assembly-CSharp.dll`, sem tocar nos cartões do KIT/LEVEL.
