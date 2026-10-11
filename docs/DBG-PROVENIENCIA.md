# DBG-PROVENIENCIA — o carimbo `DBG-PROV-V1` do RoguelikeDebugger

Instrumento do cartão `t_3b7c681b` (INT-R1-C3 / DBG-R2). Descreve o que o dump do debugger passou a
carimbar, como conferir e o que o carimbo **não** prova. Nada aqui exige rodar o jogo.

## Por que existe

Os censos `docs/cobertura/*.csv` são regenerados por `tools/census.py` a partir do dump de boot
(`LogOutput.log` do perfil r2modman). Sem proveniência, três leituras erradas passavam:

| leitura errada | o que o carimbo responde |
|---|---|
| "o dado não está no CSV, logo não existe no jogo" | o dump veio de **outro build** / de uma sessão **cortada** |
| "a lista tem N itens" | qual `Assembly-CSharp` (sha256) e qual **build Steam** foram observados |
| "a leitura é passiva" | se a sessão usava a **matriz Flame**, que chama `EvalVoid` e escreve em `MissingExpressions` |

Origem: auditoria DBG-R1 — artefatos **do pacote de entrega do cartão `t_9e2325d7`**
(`C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_9e2325d7\DBG-R1-entrega.zip`; o
`DBG-R1-parte07.md` também está solto nessa pasta). Eles **não** existem na árvore do repositório.
`DBG-R1-parte07.md` §1, lacuna nº 1; `DBG-R1-parte05-matriz.csv`, item **DBG16**, P0.

## O que sai no log

Três linhas, emitidas pelo próprio debugger no fluxo que o censo lê (`Proveniencia.cs`):

```
[Roguelike Debugger] [Proveniencia] DBG-PROV-V1 inicio | versaoJogo=… | buildSteam=… |
    sha256Alvo=… | dllDebugger=… | sha256Dll=… | identidade=api|local | apiPresente=… |
    apiEnableHooks=… | apiVersao=… | apiSha256=… | alvoConforme=… | inicioEm=… | estadoDump=INICIADO
[Roguelike Debugger] [Proveniencia] DBG-PROV-V1 estado | estadoDump=ABERTO|PARCIAL | ganchosOk=n/n |
    ganchosFalhos=… | metodos=n | matrizFlame=aplicada|ausente | modoLeitura=passivo|ativo
[Roguelike Debugger] [Proveniencia] DBG-PROV-V1 fim | estadoDump=FECHADO | motivo=saida-do-jogo
```

- O **cabeçalho sai antes** de aplicar os ganchos (`Plugin.cs`, `Awake`): se o arranque morrer no
  meio, a identidade já está gravada.
- O **rodapé** vem de `Application.quitting` — é o único sinal de "o dump fechou" (o BepInEx não
  escreve rodapé nenhum).
- `sha256Alvo` é **medido**: hash do arquivo da assembly `Assembly-CSharp` carregada. `buildSteam`
  vem do `appmanifest_1330000.acf`. Campo que não dá para medir sai `desconhecido` — nunca vazio,
  nunca estimado.
- As linhas novas **não** interferem no censo: `tools/census.py` casa `[Categoria] 'nome' | …`, e
  `[Proveniencia]` não é uma categoria.

## Verificador

```
python tools/verifica_proveniencia_debugger.py <LogOutput.log> [--alvo api/docs/target-game.json] [--json]
```

| veredito | exit | significado |
|---|---|---|
| COMPLETO | 0 | cabeçalho completo, identidade conhecida, ganchos coerentes, rodapé presente (e tudo batendo com `--alvo`) — **só este libera** ler ausência de dado como ausência de fato |
| TRUNCADO | 2 | proveniência válida, mas dump não fechado, gancho falho (`PARCIAL`) ou identidade incompleta (`buildSteam=desconhecido`) |
| REPROVADO | 1 | sem cabeçalho, campo obrigatório vazio, sha256 fora de 64 hex, bloco incoerente ou divergência com o alvo |

Avisos **não** mudam o veredito, mas precisam ser lidos: `modoLeitura=ativo` significa que a matriz
Flame está aplicada e a sessão **não** é observação passiva estrita
(`RoguelikeDebugger/Patches/FlameShrineProcPatch.cs:278-284,350`). O gate ativo separado, default
off, é trabalho de outro cartão (P0 DBG14).

## Dependência opcional da API

Com o `RealmApi` carregado **e** `EnableHooks=true` no `.cfg` dele, o debugger lê a identidade
declarada pela API (`Gumatos.RealmApi.ApiIdentity`) por reflexão e reporta `identidade=api`; sem a
API (ausente, desligada ou tipo que não resolve) ele segue sozinho e reporta `identidade=local`. O
`.csproj` do debugger **não** referencia o projeto da API — a prova é o hash do `.csproj` inalterado
no cartão DBG-R2.

## Como conferir de novo (offline)

```
python tools/testes/roda_testes.py --teste tools/testes/testes/puros/t_dbg_r2_proveniencia.py
```

O teste carrega o verificador **real**, roda as fixtures versionadas
(`tools/testes/fixtures/dbg-r2-*.entrada.log`), cobra o contrato campo-a-campo com o C# e confere o
sha256 das fontes que **não** podiam mudar. A prova vermelho→verde está em
`tools/testes/dbg-r2-prova-reprovando.log`.

## O que o carimbo NÃO prova

Runtime: nenhum arranque do jogo foi feito na implementação deste carimbo (`NAO_EXERCITADO`). O
carimbo prova **o que** foi observado, **por quem** e **se o dump fechou** — não substitui o teste
em jogo, nem valida o conteúdo mecânico dos censos.
