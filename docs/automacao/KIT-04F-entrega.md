# KIT-04F — Entrega: correções do parecer KIT-04R (Core compila + adapter SR)

Tarefa: `t_d5c98d36` (KIT-04F) · Data: 2026-10-09 · Rodada **OFFLINE** (sandbox)
Implementador: perfil `default` (run 613) · Revisor: perfil `default` (run separada)
Origem: `docs/automacao/KIT-04R-revisao.md` — parecer **REPROVADO** sobre a entrega do KIT-04 (`t_2f75985a`).

## 1. Objetivo e escopo

Fechar os **7 itens de correção** abertos pelo parecer e devolver para reconferência, provando cada
correção por execução real — inclusive **controle negativo com defeito plantado**, que o KIT-04 não
trouxe. Provas volumosas em `scratch/kit/`; pareceres por bloco em `KIT-04F-parte0{1,2,3,4}.md`.

Tocados: `tools/automacao/runtime/KIT04Core/`, `tools/automacao/runtime/KIT04Adapter.SR/`,
`docs/automacao/KIT-04-entrega.md`, `docs/automacao/KIT-04F-parte0{1..4}.md`,
`docs/automacao/schemas/core-resultado-v1.json`, `scratch/kit/…`.
**Não** tocados: `docs/automacao/KIT-04R-*.md` (histórico), mods, `Assembly-CSharp.dll`, Bard,
gameplay, perfil do dono, saves. Nada instalado/publicado; jogo não aberto; nenhum `git add`.

## 2. Correção por item, com a prova

| # | Achado do KIT-04R | Correção aplicada | Prova (execução real) |
|---|---|---|---|
| 1 | build exit 1 (3 erros CS1069/CS0103 de ScreenCapture/ImageConversion) | `KIT04Core.csproj` e `KIT04Adapter.SR.csproj` referenciam `UnityEngine.ScreenCaptureModule` e `UnityEngine.ImageConversionModule` por `$(GameManaged)` (pasta `Managed` do jogo), como o `AUT4Probe.csproj` | **build exit 0**, 0 erros, DLLs produzidas (log `kit04f-suite-repo.log`, seção "build Core"/"build Adapter") |
| 2 | `_habilitado` default `true` contradizendo a spec | default **`false`** em `CorePlugin` e em `SRAdapterPlugin`; comentários reescritos | harness: `default habilitado == false` **OK** (comportamental, não leitura de texto) |
| 3 | `LerComponentes<T>` devolvia array vazio em vez de `null` | `LerComponentes` delega a `ComponentReaderImpl<T>`; regra dura **AUSENTE ⇒ null** (array vazio proibido); `IComponentReader<T>` passa a devolver `T[]?` | harness: `AUSENTE => LerTodos/LerPorNome/LerPorTag/LerComponentes == null` **OK**; caso D do controle negativo derruba o teste |
| 4 | `KIT04Adapter.SR/` vazio (0 arquivos) | adapter entregue: `csproj` + `SRAdapterPlugin` + `SRScreenManager`/`SRCharacterManager`/`SROwnerManager`/`SRMappingManager` + `SRJson` | **build exit 0** e as 2 DLLs; `T04_adapter_completo` OK; caso F (adapter apagado) derruba a suíte |
| 5 | contrato/matriz/migração/schemas ausentes | `KIT-04F-parte02.md`: contrato **v1.0.0**, matriz de compatibilidade (Unity 2022.3.62f3 / BepInEx 5.4.23.5 / API 0.1.0), plano de migração backward-compatible, desvios declarados; novo schema `schemas/core-resultado-v1.json` | `T05_contrato_v100_e_matriz` + `T05_schemas_json_parseaveis` OK |
| 6 | hashes de placeholder (`d41d8cd9…` MD5 de vazio, `e3b0c442…` SHA256 de vazio, "a calcular") | substituídos por `sha256sum` real do disco, com nota de correção | `T05_hashes_reais_no_entregavel` OK; `sha256sum -c` sobre a lista da parte 03 → **todas OK, 0 FAILED** |
| 7 | nenhum teste / nenhum controle negativo | suíte `scratch/kit/testes/t_kit04f_contrato.py` (13 testes, harness comportamental em C#) + `scratch/kit/controle-negativo-kit04f.sh` | **6/6 casos**: verde sem defeito (exit 0), vermelho com cada um dos 5 defeitos (exit 1) — ver §4 |

## 3. Identidade dos artefatos entregues (SHA256 medido)

Código:

```
8a415edb92693a37f39cebfa92295b5fa9e120fa544bcf2c247c672ba97ce905  tools/automacao/runtime/KIT04Core/CorePlugin.cs
5f43a9e3e9d471b3fc68c0a062bb5286c286786c7419574e28ab70ca0e456bbc  tools/automacao/runtime/KIT04Core/ComponentReaderImpl.cs
587523bc9bf03b93829b4ca49c1b86dcc1a885fc737737595687f5a08d22dfa5  tools/automacao/runtime/KIT04Core/ICoreIdentidade.cs
c15fcff0c10bcefa59b41f149e646dc13a7c5d9b759585fc4e2736eb2d94b2b3  tools/automacao/runtime/KIT04Core/IdentidadeDoCoreImpl.cs
6dcc7ec5149295b40934ecb3ede0b5e69638adf392502d2f0bc44aea2ef4188d  tools/automacao/runtime/KIT04Core/IComponentReader.cs
e41bd620b4f2ef92b6b17778662aac0793bb4598ad00b0eee98b404db322c829  tools/automacao/runtime/KIT04Core/KIT04Core.csproj
9687dbd4fc81399cf94808a5a14fa955b43e5cb327426da811380c5339662b01  tools/automacao/runtime/KIT04Adapter.SR/SRAdapterPlugin.cs
af67deceb0745cde942bb2a38bd198ea602f7585f99c6c24723fa7a1e279c68d  tools/automacao/runtime/KIT04Adapter.SR/KIT04Adapter.SR.csproj
```
(a lista completa dos 29 artefatos está em `KIT-04F-parte03.md` §1 e foi conferida com `sha256sum -c`)

Documentos e provas:

```
3dfc190912e856e75b7151dfcb189b4b32bce0f13b07f1e9cf392f6982dad8e1  docs/automacao/KIT-04F-parte01.md
de79916cfbb0e5ae9b640118e3d90a17234b2fc1ffaead4fb5b993cb56bfb641  docs/automacao/KIT-04F-parte02.md
3b68591219816ebbea13a129775e1c3fab14409b4d3fc8d24bee0812fb4de59a  docs/automacao/KIT-04F-parte03.md
7bbfb40794f2788a6efa7a924a6e3f72b92c9079b1b9b49debd18c925418ecb9  docs/automacao/KIT-04F-parte04.md
30af31c6ee6dd613173344824a6ba24261230811f6605afeab1fee0f2f5c526f  docs/automacao/KIT-04-entrega.md
bd5c430ce511b4af592d798d3eaef5969728cc0e206fb6647b75e05892ee9931  docs/automacao/schemas/core-resultado-v1.json
9744abdbd924f4f7271e6f1a043840719ae4f88cdda3a2a6403ad5b7237b998b  scratch/kit/testes/t_kit04f_contrato.py
db087d58af234547fc65a0a07eeca5863bff8769ebeff35cd2e64ccfe1b81cbb  scratch/kit/testes/roda_kit04f.sh
bfd25936ddf1b32202b845b492ced21641e9b2a65171ca1fd914ed8ba96aa01e  scratch/kit/controle-negativo-kit04f.sh
```

> Nota: os hashes de `KIT-04F-parte03.md` e de `KIT-04-entrega.md` mudaram **depois** de escritos
> (correção dos dois hashes dos scripts no parte 03, que ficaram obsoletos após o ajuste de path
> `pwd -W`). Os valores acima são os medidos no estado final; `KIT-04F-parte03.md` §1 foi corrigido
> no lugar e reverificado com `sha256sum -c`.

## 4. Controle negativo (exigência central do item 7)

`scratch/kit/controle-negativo-kit04f.sh` roda a **mesma suíte** contra uma cópia em
`scratch/kit/build/kit04f-negativo/` (raiz do repositório intocada), com um defeito por caso:

| Caso | Defeito plantado | Exit | Teste que caiu |
|---|---|---|---|
| A | nenhum | **0** | — (13 testes, `OK`) |
| B | `habilitado` default volta a `true` | **1** | `T03` harness + `T04` + `T06` |
| C | `<Reference>` do `ImageConversionModule` removida | **1** | `T01` build + `T02` + `T04` + `T06` |
| D | leitor volta a devolver array vazio | **1** | `T03` harness + `T04` + `T06` |
| E | hash de arquivo-vazio de volta no entregável | **1** | `T05_hashes_reais_no_entregavel` |
| F | `KIT04Adapter.SR/` apagado | **1** | `T02` + `T04` + `T06` |

`Casos: 6 | OK: 6 | FALHOU: 0` · `VEREDITO: OK` · `CONTROLE_EXIT=0`.
Suíte contra o repositório: `Ran 13 tests … OK` · `exit=0`. Logs em `scratch/kit/logs/`.

Cada defeito derruba o teste **do item que ele reverte** — não é falha genérica.

## 5. O que NÃO foi exercitado (declarado)

- **Runtime em jogo**: telas/personagens/owners/captura de frame real exigem rodada autorizada do
  AUT-4. O harness compila as chamadas ao Unity contra stub; **não** as executa em engine.
- **Equivalência numérica** Core+Adapter vs. `runtime/out/ex1-offline.json`: INDETERMINADO (precisa
  da saída real do jogo).
- **Perfil do dono / instalação / publicação**: intocados; jogo não aberto; nenhum save carregado.

## 6. Próximo passo

Reconferência independente (revisor ≠ autor). A entrega é reconferível por:
`bash scratch/kit/testes/roda_kit04f.sh` (verde) e `bash scratch/kit/controle-negativo-kit04f.sh`
(6/6). Nada a publicar nesta rodada — o KIT-04 é infraestrutura offline, não mod.
