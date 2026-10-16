# DBG-R2 — Parte 04: entrega, contagens e fechamento

Cartão `t_3b7c681b` (INT-R1-C3). Partes 01–03 estão nos arquivos numerados; esta fecha com índice,
contagens, aceite item a item, e o que **não** foi exercitado.

## 1. Índice do que foi entregue

| artefato | o que é |
|---|---|
| `RoguelikeDebugger/Proveniencia.cs` | **novo** — mede a identidade e emite o bloco `DBG-PROV-V1` |
| `RoguelikeDebugger/Plugin.cs` | editado (aditivo): carimbo antes dos ganchos, estado depois, rodapé no `quitting` |
| `docs/DBG-PROVENIENCIA.md` | **novo** — registro do instrumento: formato, veredito, consumo, dependência opcional, limites |
| `tools/verifica_proveniencia_debugger.py` | **novo** — verificador (exit 0/2/1) |
| `tools/testes/regras_proveniencia.py` | **novo** — biblioteca da família (importa o verificador real; hashes intocados) |
| `tools/testes/testes/puros/t_dbg_r2_proveniencia.py` | **novo** — teste puro (96 testes da suíte: 1 a mais que antes) |
| `tools/testes/fixtures/dbg-r2-*.entrada.log` | **novos** — 4 dumps versionados (completo / sem proveniência / truncado / incoerente) |
| `tools/testes/dbg-r2-prova-reprovando.log` | evidência da prova física vermelho→verde (5 rodadas) |
| `docs/automacao/DBG-R2-parte01..03.md` | escopo+desenho+fatia P0 / implementação+build / verificador+prova |
| `docs/automacao/DBG-R2-parte02-build.log` | log integral do `dotnet build` isolado |
| `docs/automacao/DBG-R2-parte04-suite-puros.log` | log integral da suíte pura (117 linhas) |

Nada foi instalado, publicado, ou rodado no jogo. O DLL do perfil do dono segue com sha256
`55bc6250…34e6` e mtime de 07/10/2026.

## 2. Contagens

- Fontes do debugger: **12 → 13** arquivos `.cs` (novo: `Proveniencia.cs`); o `.csproj` intocado.
- Arquivos do mod com sha256 **alterado**: **1** (`Plugin.cs`). Com sha256 **idêntico**: 11
  (10 `Patches/*.cs` + `EfeitosInfo.cs` + `.csproj`).
- Campos do carimbo exigidos pelo verificador: **21** (13 `inicio` + 6 `estado` + 2 `fim`), todos
  presentes no C# (conferido campo a campo pelo teste).
- Fixtures: **4** · iscas embutidas no teste: **13** · alvos adulterados: **3** ·
  mutações físicas vermelho→verde: **3** · rodadas do runner na evidência física: **5**.
- `dotnet build` (cópia isolada, `-p:DeployToBepInEx=false`): **0 Erros**, 1 Aviso (`MSB3277`,
  idêntico ao build de controle sem as mudanças).
- Suíte pura: **96 rodaram, 95 passaram, 1 reprovou** — a reprovação (§3) é **pré-existente e alheia
  a este cartão**.
- Runtime em jogo: **NAO_EXERCITADO**.

## 3. A reprovação da suíte (declarada, não escondida)

`deploy-optin-repo` reprova porque `tools/check_deploy_optin.py` varre o repo **inteiro** e encontra
`deploy-negative/ruim.csproj` deixados por outro cartão dentro de `scratch/kit/KIT-14-run699` e
`KIT-14-run710` (um deles até com XML inválido). Provas de que **não é deste cartão**:

- os arquivos acusados têm mtime de **10/10/2026** (13:11 e 17:46) — antes desta rodada (11/10);
- o `.csproj` do RoguelikeDebugger tem sha256 **inalterado** (`d2df3d9a…8541`), e o teste puro deste
  cartão confere isso;
- o teste puro novo passa (`dbg-r2-proveniencia`) e nada mais toca `scratch/`.

Limpeza de `scratch/` está **fora do escopo** deste cartão (o limite é não mexer no que é de outros
cartões). Registrado como achado para o controlador.

## 4. Aceite, item a item

| critério | situação | evidência |
|---|---|---|
| parte numerada | ✅ partes 01–04 em `docs/automacao/DBG-R2-*` | — |
| verificador que **reprova** dump sem proveniência | ✅ exit 1 | parte 03 §2.1 (fixture e o dump real do dono) |
| caso negativo obrigatório **provado vermelho→verde** | ✅ 3 mutações físicas: marca, contrato de campo, ordem | `tools/testes/dbg-r2-prova-reprovando.log` (rodadas 1→5) |
| `dotnet build` 0 erros em cópia isolada com `-p:DeployToBepInEx=false` | ✅ | `DBG-R2-parte02-build.log`; perfil do dono intocado |
| fontes do debugger conferidas por sha256 antes/depois | ✅ 11 intocadas, 1 alterada, 1 nova | parte 02 §1 e `regras_proveniencia.INTOCADOS` |
| runtime em jogo NAO_EXERCITADO | ✅ declarado | parte 02 §5, parte 03 §5, §5 abaixo |
| dependência opcional da API | ✅ reflexão + `.csproj` intocado | parte 02 §4 |
| fatia P0 (o que cobre / o que fica fora) | ✅ tabela item a item | parte 01 §4 |
| achado de passividade registrado no instrumento | ✅ campos `matrizFlame`/`modoLeitura` + NOTA no verificador | parte 01 §4.1, `docs/DBG-PROVENIENCIA.md` |
| limites: sem instalar/abrir o jogo/publicar/reescrever ganchos/tocar KIT-LEVEL | ✅ | hashes intocados; build sem deploy; nenhum arquivo de KIT/LEVEL tocado |

## 5. NAO_EXERCITADO (declarado, nunca estimado)

1. **Runtime**: nenhuma linha do carimbo foi emitida por um processo real — o formato é o do fonte
   e o contrato é conferido campo a campo, mas a emissão em jogo não foi observada.
2. **Rodapé em saída abrupta**: `Application.quitting` não dispara em kill/crash por definição da
   Unity; o resultado (TRUNCADO) é o desejado, mas não medido em partida.
3. **`appmanifest` em runtime**: a leitura do build Steam foi exercitada só por fixture.
4. **Consumo pelo censo**: nenhuma automação passou a exigir o carimbo (decisão de escopo: o censo
   continua funcionando sozinho); o uso em pipeline é proposta, não implementação.
5. **Efeito dos ganchos**: o cartão não muda comportamento de log dos ganchos; isso não foi
   reexecutado em jogo.

## 6. Como reconferir (sem jogo)

```
cd /c/dev/stolen-realm
python tools/testes/roda_testes.py --teste tools/testes/testes/puros/t_dbg_r2_proveniencia.py
python tools/verifica_proveniencia_debugger.py tools/testes/fixtures/dbg-r2-proveniencia.entrada.log --alvo api/docs/target-game.json   # 0
python tools/verifica_proveniencia_debugger.py tools/testes/fixtures/dbg-r2-sem-proveniencia.entrada.log --alvo api/docs/target-game.json   # 1
cd "$HERMES_KANBAN_WORKSPACE/isolado/RoguelikeDebugger" && dotnet build RoguelikeDebugger.csproj -c Release -p:DeployToBepInEx=false
```

## 7. Frentes que ficam PARA FORA (não implementar aqui)

- **P0 DBG14** — gate ativo separado da matriz Flame, default off, com teste que detecta escrita em
  cache/`MissingExpressions` (a matriz hoje sempre entra quando o hook aplica).
- **P0 DBG01/DBG02/DBG03/DBG05/DBG06 e P1/P2/P3** da matriz `DBG-R1-parte05-matriz.csv` (arquivo
  dentro do ZIP da entrega do cartão pai `t_9e2325d7`, em
  `%USERPROFILE%\AppData\Local\hermes\kanban\attachments\t_9e2325d7\DBG-R1-entrega.zip` — **não**
  existe na árvore do repositório) — cada um é um cartão próprio (a tabela da parte 01 §4 diz, item
  a item, o que este cartão cobre).
- **Envelope por registro** (frame/owner em cada linha do dump) — este cartão carimba o **dump**, não
  cada linha.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
