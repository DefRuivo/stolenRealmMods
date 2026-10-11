# KIT-04R — Revisão independente (parte 01: identidade dos arquivos vivos)

**Revisor:** instância separada do implementador (perfil default, run 607 do cartão t_0451c587).
**Implementador do escopo revisado:** t_2f75985a (KIT-04, run encerrado pelo operador).
**Data:** 2026-10-09. **Modalidade:** offline, sandbox. Nenhum jogo, save, perfil, instalação ou publicação.
**Lente desta rodada:** artefato (leitura fria) + execução em cópia isolada.

## O que está sendo revisado

Escopo entregue pelo KIT-04 (t_2f75985a): extração de um Core genérico e de um
adapter Stolen Realm a partir do AUT4Probe, entregues no disco como
`docs/automacao/KIT-04-entrega.md` e `docs/automacao/KIT-04-core-especificacao.md`,
com o código novo sob `tools/automacao/runtime/KIT04Core/` e `.../KIT04Adapter.SR/`.

Trata-se de **re-revisão**: a rodada 1 (run 600) reprovou. Esta instância não herda
o transcript anterior; reconstrói a identidade dos arquivos do zero e reproduz por
execução própria.

## Inventário de arquivos vivos do KIT-04 (hashes medidos por mim, 2026-10-09)

Caminho base: `C:/dev/stolen-realm`

### Documentos de entrega (planejamento)

| Arquivo | SHA256 |
|---|---|
| docs/automacao/KIT-04-entrega.md (9615 B, mtime 10-08 19:00) | (medido abaixo) |
| docs/automacao/KIT-04-core-especificacao.md (6228 B, mtime 10-08 19:03) | (medido abaixo) |

### Código novo — KIT04Core (7 fontes, 628 linhas)

| Arquivo | Linhas | SHA256 |
|---|---|---|
| KIT04Core/CorePlugin.cs | 266 | 312708879cc70263eab6dadbf0f9725cf027a11263dc2da570d579d0787bd010 |
| KIT04Core/IComponentReader.cs | 36 | 8e077ff16146b8335a560bdf9589da964d75bba9444471c6022198c55fe3b9d8 |
| KIT04Core/ICoreEvento.cs | 30 | fefbbf4b3ba6175bc4d6267db03ec656753ad1b433a94e6c23dddd038b1aa5de |
| KIT04Core/ICoreSession.cs | 28 | d947b6241bdffe63eae95d1dca9e03add0da61efb3e406ce7f98ca58dafd602e |
| KIT04Core/IdentidadeDoCore.cs | 79 | e9dc4f152f19d722db5fcd7a3dca4c611dcf3f4582c73b19ec06e230faacefad |
| KIT04Core/IPictureCapture.cs | 31 | 0f8275097c4df8ba734d725fa47d313ab95632bbfe50751436a78b9535986e29 |
| KIT04Core/Json.cs | 158 | 587a36ec00dfef196efce374b034234d80c21cd9507e7a709a342d10d06efb04 |
| KIT04Core/KIT04Core.csproj | — | a5b3c719dd9aab8ddde20f7600025994e55cf770d6f88e6bb4ab3e652194fb18 |

### Adapter Stolen Realm

`tools/automacao/runtime/KIT04Adapter.SR/` — **DIRETÓRIO VAZIO confirmado**
(`find ... -type f` não retorna nada; `ls -la` mostra apenas `.` e `..`, mtime 10-08 19:03).
Não há `.csproj`, `.cs`, README ou qualquer arquivo no adapter.

## Achado preliminar de identidade

- O Core existe como fontes (7 arquivos) e um `.csproj` (netstandard2.1).
- O **adapter Stolen Realm não existe**: a pasta anunciada na especificação
  (`KIT-04-entrega.md` §"Estrutura proposta") está vazia. Confirma o achado da rodada 1.
- Os arquivos de entrega são **documentos de planejamento** — `KIT-04-entrega.md`
  termina em "**Status:** INICIADO — inventário completo realizado". Os checkboxes
  de §2–§5 (extração, adapter, doc/contrato, validação offline) seguem **não marcados**.

## Próximos blocos

1. Leitura fria de `CorePlugin.cs` e do `.csproj`; verificar os 3 erros de compilação
   relatados (ScreenCapture/ImageConversion) e o design `PatchAll()`/`OnDestroy()`.
2. Build em cópia sandbox com `-p:DeployToBepInEx=false`.
3. Caminho positivo + defeito plantado (controle negativo).
4. Refutações: regressão na migração, interferência no produto, dependência obrigatória dos mods.
