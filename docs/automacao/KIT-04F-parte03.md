# KIT-04F — parte 03: identidade SHA256 real + suíte de teste e controle negativo

Tarefa `t_d5c98d36` (KIT-04F) · 2026-10-09 · offline. Cobre os **itens 6 e 7** do parecer KIT-04R.
Os resultados de execução (exit codes, saídas) ficam em `KIT-04F-parte04.md`; aqui está a
**identidade dos artefatos** e a **descrição verificável** da suíte.

## 1. Hashes SHA256 medidos (estado final entregue)

Medidos com `sha256sum` sobre os arquivos no disco (não copiados de relatório anterior):

```
5f43a9e3e9d471b3fc68c0a062bb5286c286786c7419574e28ab70ca0e456bbc  tools/automacao/runtime/KIT04Core/ComponentReaderImpl.cs
8a415edb92693a37f39cebfa92295b5fa9e120fa544bcf2c247c672ba97ce905  tools/automacao/runtime/KIT04Core/CorePlugin.cs
6dcc7ec5149295b40934ecb3ede0b5e69638adf392502d2f0bc44aea2ef4188d  tools/automacao/runtime/KIT04Core/IComponentReader.cs
fefbbf4b3ba6175bc4d6267db03ec656753ad1b433a94e6c23dddd038b1aa5de  tools/automacao/runtime/KIT04Core/ICoreEvento.cs
587523bc9bf03b93829b4ca49c1b86dcc1a885fc737737595687f5a08d22dfa5  tools/automacao/runtime/KIT04Core/ICoreIdentidade.cs
d947b6241bdffe63eae95d1dca9e03add0da61efb3e406ce7f98ca58dafd602e  tools/automacao/runtime/KIT04Core/ICoreSession.cs
e9dc4f152f19d722db5fcd7a3dca4c611dcf3f4582c73b19ec06e230faacefad  tools/automacao/runtime/KIT04Core/IdentidadeDoCore.cs
c15fcff0c10bcefa59b41f149e646dc13a7c5d9b759585fc4e2736eb2d94b2b3  tools/automacao/runtime/KIT04Core/IdentidadeDoCoreImpl.cs
0f8275097c4df8ba734d725fa47d313ab95632bbfe50751436a78b9535986e29  tools/automacao/runtime/KIT04Core/IPictureCapture.cs
587a36ec00dfef196efce374b034234d80c21cd9507e7a709a342d10d06efb04  tools/automacao/runtime/KIT04Core/Json.cs
e41bd620b4f2ef92b6b17778662aac0793bb4598ad00b0eee98b404db322c829  tools/automacao/runtime/KIT04Core/KIT04Core.csproj
9687dbd4fc81399cf94808a5a14fa955b43e5cb327426da811380c5339662b01  tools/automacao/runtime/KIT04Adapter.SR/SRAdapterPlugin.cs
5f32ec1d66cf28714f6fd5051bd4beed9e6d141d8106763204cfe5a48305f63e  tools/automacao/runtime/KIT04Adapter.SR/SRCharacterManager.cs
41e4dd93fe2100f4a42b363bda029733f6a6f599e044429583540fa1a7ed7ef1  tools/automacao/runtime/KIT04Adapter.SR/SRJson.cs
37241c35ed5adefcde00fd2bf34776d05e92fc9a436a0b53e9c804cd4ecf28cb  tools/automacao/runtime/KIT04Adapter.SR/SRMappingManager.cs
189a6d73036c691416e84748c7b37a3046564ab3a573afd923fcb1c754e75b78  tools/automacao/runtime/KIT04Adapter.SR/SROwnerManager.cs
d362adaa8e52ef1d24f5d85c490b01697026a09cb7101ac53e20a0465e0050b1  tools/automacao/runtime/KIT04Adapter.SR/SRScreenManager.cs
af67deceb0745cde942bb2a38bd198ea602f7585f99c6c24723fa7a1e279c68d  tools/automacao/runtime/KIT04Adapter.SR/KIT04Adapter.SR.csproj
30af31c6ee6dd613173344824a6ba24261230811f6605afeab1fee0f2f5c526f  docs/automacao/KIT-04-entrega.md
3dfc190912e856e75b7151dfcb189b4b32bce0f13b07f1e9cf392f6982dad8e1  docs/automacao/KIT-04F-parte01.md
de79916cfbb0e5ae9b640118e3d90a17234b2fc1ffaead4fb5b993cb56bfb641  docs/automacao/KIT-04F-parte02.md
bd5c430ce511b4af592d798d3eaef5969728cc0e206fb6647b75e05892ee9931  docs/automacao/schemas/core-resultado-v1.json
9744abdbd924f4f7271e6f1a043840719ae4f88cdda3a2a6403ad5b7237b998b  scratch/kit/testes/t_kit04f_contrato.py
db087d58af234547fc65a0a07eeca5863bff8769ebeff35cd2e64ccfe1b81cbb  scratch/kit/testes/roda_kit04f.sh
bfd25936ddf1b32202b845b492ced21641e9b2a65171ca1fd914ed8ba96aa01e  scratch/kit/controle-negativo-kit04f.sh
2989dec13146c371afb9a1b1076cf2747a7c34847a70bec4eadbb84496066ec8  scratch/kit/testes/kit04f/harness/BepInExStub.cs
b639c71564a75237a21ae5c053f5b0766f9b563cb894377a7c7f33d232374281  scratch/kit/testes/kit04f/harness/Program.cs
11584718261b561342502dc765f667c9eac8f8385b6a2f06b5aca33ad266b91b  scratch/kit/testes/kit04f/harness/UnityEngineStub.cs
```

O hash deste próprio `KIT-04F-parte03.md` e do `-parte04.md` não constam acima (auto-referência é
impossível); o revisor os mede a partir do disco.

## 2. A suíte (`scratch/kit/testes/t_kit04f_contrato.py`)

`python` (stdlib `unittest`), offline. Raiz dos artefatos parametrizável por `KIT04F_ROOT` — é o
que permite ao controle negativo rodar **a mesma suíte** contra uma cópia com defeito.

Exit code: **0** = tudo verde; **1** = qualquer falha.

| Classe | Teste | O que produz (efeito real, não mensagem de sucesso) |
|---|---|---|
| `T01_BuildCore` | build do csproj entregue | copia para sandbox isolada, roda `dotnet build -c Release -p:DeployToBepInEx=false`, exige **exit 0** e `KIT04Core.dll` no disco |
| `T02_BuildAdapter` | build do adapter | idem, exige **exit 0** e as 2 DLLs (`KIT04Adapter.SR.dll` + `KIT04Core.dll`) |
| `T03_HarnessComportamental` | comportamento | compila e **executa** os fontes reais do Core sobre stub de UnityEngine/BepInEx; exige `HARNESS: VERDE` e exit 0 |
| `T04_ContratoEstatico` | módulos/adapter | `$(GameManaged)` presente, `lib/` sem os módulos, `habilitado=false` na fonte, leitor com regra AUSENTE⇒null, adapter com os 6 arquivos |
| `T05_DocumentosEHashe` | contrato e hashes | `KIT-04F-parte02.md` com 1.0.0/matriz/migração/schemas; schemas parseáveis; **nenhum hash de arquivo-vazio** no entregável |
| `T06_IdentidadeDosArtefatos` | coerência | mede o SHA256 dos fontes vivos e exige que constem desta parte 03 |

### O harness comportamental (o que ele prova e o que NÃO prova)

`scratch/kit/testes/kit04f/harness/` contém `UnityEngineStub.cs`, `BepInExStub.cs` e `Program.cs`.
O harness instancia o `KIT04Core.CorePlugin` **real** (fonte do repositório), chama o `Awake`
privado por reflexão e checa 23 asserções: default `habilitado=false`, `NAO_EXERCITADO`,
`CapturarPNG` bloqueado quando desligado e funcionando quando ligado (caminho
`ScreenCapture`/`ImageConversion` que antes nem compilava), `AUSENTE ⇒ null` em
`LerTodos`/`LerPorNome`/`LerPorTag`/`Inventariar`, identidade SHA256 da própria DLL, e o
serializador JSON (`System.Text.Json` valida a saída de `Json.Serialize`).

**Limite declarado:** o stub torna as chamadas ao Unity *compiláveis*, não *executadas* em runtime
de engine. O que é provado é o **comportamento do código do Core**; execução em jogo é
NÃO_EXERCITADO (fora do escopo autorizado). O stub está marcado como tal no próprio arquivo.

## 3. O controle negativo (`scratch/kit/controle-negativo-kit04f.sh`)

Copia os artefatos vivos para `scratch/kit/build/kit04f-negativo/` (raiz do repo **não** é tocada),
planta **um** defeito por caso e roda a mesma suíte com `KIT04F_ROOT` na sandbox.

| Caso | Defeito plantado | Exit esperado |
|---|---|---|
| A | nenhum (sandbox limpa) | **0** (verde) |
| B | `Config.Bind("Modo","habilitado", true …)` (item 2 revertido) | **1** |
| C | remove a `<Reference>` do `UnityEngine.ImageConversionModule` (item 1 revertido) | **1** |
| D | `Presente(...)` volta a `=> achados;` (item 3 revertido: array vazio em vez de null) | **1** |
| E | hash de arquivo-vazio reintroduzido em `KIT-04-entrega.md` (item 6 revertido) | **1** |
| F | `KIT04Adapter.SR/` apagado (item 4 revertido) | **1** |

Critério do item 7: **verde sem defeito, vermelho com cada defeito, exit codes distintos**.
Os logs por caso ficam em `scratch/kit/logs/`. O veredito consolidado está na `KIT-04F-parte04.md`.
