# KIT-04R — Parecer de revisão independente da entrega KIT-04

**Cartão:** t_0451c587 · **Revisor:** instância separada do implementador (perfil `default`, run 607)
**Escopo revisado:** entrega do cartão t_2f75985a (KIT-04 "Extrair Core genérico e adapter Stolen Realm do AUT4Probe")
**Data:** 2026-10-09 · **Modalidade:** offline, sandbox. Nenhum jogo, save, perfil, instalação ou publicação.
**Provas volumosas:** `docs/automacao/KIT-04R-parte01.md` (identidade), `-parte02.md` (build/execução),
`-parte03.md` (refutações + parecer por critério). Este arquivo é o parecer de fechamento.

**Veredito global: REPROVADO.**

---

## 1. O que foi revisado e como

Re-revisão (a rodada 1, run 600, também reprovou). Não herdei transcript; reconstruí a
identidade dos arquivos do zero, medi hashes, e **reproduzi por execução própria** os achados,
em cópia isolada com `-p:DeployToBepInEx=false`.

Sandbox: `C:/Users/Pichau/AppData/Local/hermes/cache/scratch/kit-revisao{,-positivo}`
(fora do repositório). Jogo não estava aberto (`tasklist` → nenhum processo "Stolen").

## 2. Identidade dos artefatos revisados (SHA256, medido por mim)

Código Core — `tools/automacao/runtime/KIT04Core/`:

| Arquivo | SHA256 |
|---|---|
| CorePlugin.cs | 312708879cc70263eab6dadbf0f9725cf027a11263dc2da570d579d0787bd010 |
| IdentidadeDoCore.cs | e9dc4f152f19d722db5fcd7a3dca4c611dcf3f4582c73b19ec06e230faacefad |
| Json.cs | 587a36ec00dfef196efce374b034234d80c21cd9507e7a709a342d10d06efb04 |
| IComponentReader.cs | 8e077ff16146b8335a560bdf9589da964d75bba9444471c6022198c55fe3b9d8 |
| ICoreEvento.cs | fefbbf4b3ba6175bc4d6267db03ec656753ad1b433a94e6c23dddd038b1aa5de |
| ICoreSession.cs | d947b6241bdffe63eae95d1dca9e03add0da61efb3e406ce7f98ca58dafd602e |
| IPictureCapture.cs | 0f8275097c4df8ba734d725fa47d313ab95632bbfe50751436a78b9535986e29 |
| KIT04Core.csproj | a5b3c719dd9aab8ddde20f7600025994e55cf770d6f88e6bb4ab3e652194fb18 |

Documentos:
`KIT-04-entrega.md` = f8d256d0409c7cc3b56b784738846cb060f1c7a5df5782947a60890c71b6372c
`KIT-04-core-especificacao.md` = 4701dab5e17227382a87e14af2345d3dbed615c778a7a4d705516e656926f093

Adapter: `tools/automacao/runtime/KIT04Adapter.SR/` — **DIRETÓRIO VAZIO** (0 arquivos).

## 3. Provas de execução (exit codes reais)

1. **Build do entregue** (cópia isolada, sem alteração): `dotnet build -c Release -p:DeployToBepInEx=false`
   → **EXIT 1**, `3 Erro(s) / 18 Aviso(s)`:
   - `CorePlugin.cs(228,49) CS1069` — `UnityEngine.ScreenCapture` (encaminhado p/ ScreenCaptureModule)
   - `CorePlugin.cs(231,29) CS0103` — `ImageConversion`
   - `CorePlugin.cs(261,39) CS1069` — `UnityEngine.ScreenCapture`
   Nenhuma DLL produzida.
2. **Caminho positivo / defeito neutralizado** (só o bloco de captura alterado): → **EXIT 0**, `0 Erro(s)`,
   `KIT04Core.dll` (14848 B). Prova que os 3 erros são os **únicos** bloqueadores e estão localizados.
3. **Instrumento de origem** `AUT4Probe.csproj` em sandbox: → **EXIT 0**, `0 Erro(s)`, 1 aviso MSB3277;
   DLL `407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7` (inalterada).
4. **Cross-refs**: nenhum `csproj` referencia KIT04; nenhuma DLL referencia KIT04Core;
   perfil r2modman sem "KIT04"; `lib/Assembly-CSharp.dll` intacta (`8bb4a7c5…`).

## 4. Parecer por critério (resumo — detalhe na parte03)

| Critério | Veredito |
|---|---|
| Core compila (A1/B1) | **FALHOU** |
| DLL do Core produzida (A3) | **FALHOU** |
| Adapter SR existe/compila (A4) | **FALHOU** |
| `_habilitado` default false (B2) | **FALHOU** (default `true`, contradiz spec e os próprios comentários) |
| Hashes reais no entregável (C5) | **FALHOU** (hashes de placeholder / de entrada vazia) |
| Itens do entregável concluídos (C6) | **FALHOU** (2 `[x]` / 13 `[ ]`; "Status: INICIADO") |
| Contrato v1.0.0, matriz, plano de migração, schemas (C1-C4) | **ACHADO** (ausentes) |
| `LerComponentes<T>` retorna null (B5) / `ICoreIdentidade` (B10) | **ACHADO** (retorna `Array.Empty`; interface substituída por classe estática) |
| `{"status":"NAO_EXERCITADO"}` se desabilitado (B3) | **ACHADO** (código presente, inalcançável como default e não executável) |
| `CapturarPNG` false se indisponível (B6) | **ACHADO** (é o caminho que não compila) |
| Identidade SHA256 da própria DLL (B4) | **INDETERMINADO** (não executável) |
| Interface `IComponentReader<T>` (B9) | **OK** |
| Eventos em lista / Json sem deps (B7/B8) | **OK (estático)** |
| Instrumento de origem intacto (A5) | **OK** |

Legenda de vereditos distintos: OK · ACHADO · FALHOU · INDETERMINADO. Ausência/timeout/etapa
pulada **nunca** registrados como verde.

## 5. Refutações exigidas (detalhe e evidência na parte03)

- **Regressão na migração:** o instrumento de origem **não** regrediu (compila, DLL idêntica);
  a migração **introduziu** regressão no Core (perdeu o mecanismo `GameManaged`/ScreenCaptureModule).
- **Interferência do instrumento no produto:** **REFUTADO** — nada referencia o KIT04; nada instalado;
  `Assembly-CSharp.dll` intacta.
- **Dependência obrigatória dos mods:** **REFUTADO** para o Core (nenhuma referência, sem
  `Assembly-CSharp`); **INDETERMINADO** para o Adapter (diretório vazio).

## 6. Conclusão e próximo passo

A entrega do KIT-04 **não fecha**: não compila, o adapter não existe e a seção de "saídas reais"
do entregável contém hashes fabricados. Corrige-se no implementador (correção aberta no cartão
filho **KIT-04F**, itens abaixo), sem tocar em arquivos vivos fora do escopo e sem apagar histórico.

Itens de correção abertos em **KIT-04F**:
1. Referenciar `UnityEngine.ScreenCaptureModule` e `UnityEngine.ImageConversionModule` no
   `KIT04Core.csproj` (mecanismo `GameManaged` como no `AUT4Probe.csproj`) → build exit 0.
2. `_habilitado` default **false** (spec §118) e coerência dos comentários.
3. `LerComponentes<T>` retornar `null` (não `Array.Empty`) quando ausente (spec §89).
4. Criar o adapter `KIT04Adapter.SR/` (csproj + SRAdapterPlugin + telas/personagens/owners/mapeamentos).
5. Entregar matriz de compatibilidade, plano de migração backward-compatible, schemas JSON e a versão do contrato.
6. Substituir os hashes de placeholder por hashes SHA256 reais (`sha256sum` medido).
7. Adicionar controle negativo/defeito plantado verificável (o KIT-04 não trouxe nenhum teste).

**Nada foi publicado, instalado, aberto ou modificado no produto.** Nenhum arquivo vivo do
escopo foi editado; só foram criados os documentos `docs/automacao/KIT-04R-*.md`.
