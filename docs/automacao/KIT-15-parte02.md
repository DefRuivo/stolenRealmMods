# KIT-15 — parte 02: inventário dos fontes vivos e desenho do pacote

Sessão: worker run 677 (default) · data 2026-10-10 · repo `C:/dev/stolen-realm`
Método: `sha256sum` real sobre os fontes vivos (saída bruta em
`scratch/kit/KIT-15-run677/componentes-hashes.txt`). Nada foi editado; esta parte é inventário + desenho.

## 1. Inventário dos componentes (arquivo → sha256 medido)

### 1.1 Core (C# — `tools/automacao/runtime/KIT04Core/`) — obrigatório
| arquivo | sha256 |
|---|---|
| ComponentReaderImpl.cs | 5f43a9e3e9d471b3fc68c0a062bb5286c286786c7419574e28ab70ca0e456bbc |
| CorePlugin.cs | 77e2d1cb31cf83d471f47c0d6b20d1f337ebcaca103b9775b25144b622095234 |
| IComponentReader.cs | 6dcc7ec5149295b40934ecb3ede0b5e69638adf392502d2f0bc44aea2ef4188d |
| ICoreEvento.cs | fefbbf4b3ba6175bc4d6267db03ec656753ad1b433a94e6c23dddd038b1aa5de |
| ICoreIdentidade.cs | 587523bc9bf03b93829b4ca49c1b86dcc1a885fc737737595687f5a08d22dfa5 |
| ICoreSession.cs | d947b6241bdffe63eae95d1dca9e03add0da61efb3e406ce7f98ca58dafd602e |
| IdentidadeDoCore.cs | e9dc4f152f19d722db5fcd7a3dca4c611dcf3f4582c73b19ec06e230faacefad |
| IdentidadeDoCoreImpl.cs | c15fcff0c10bcefa59b41f149e646dc13a7c5d9b759585fc4e2736eb2d94b2b3 |
| IPictureCapture.cs | 0f8275097c4df8ba734d725fa47d313ab95632bbfe50751436a78b9535986e29 |
| Json.cs | 587a36ec00dfef196efce374b034234d80c21cd9507e7a709a342d10d06efb04 |
| PipelinePassivo.cs | 8aec5b8aaaf5da39035864cf1d850a10536c00c51a6e16032167eae62eaed10c |
| KIT04Core.csproj | e41bd620b4f2ef92b6b17778662aac0793bb4598ad00b0eee98b404db322c829 |

### 1.2 Adapter Stolen Realm (C# — `tools/automacao/runtime/KIT04Adapter.SR/`) — obrigatório
| arquivo | sha256 |
|---|---|
| PonteControleRSTV.cs | cad1bcc26cf10d4d754e8e96c076fc39c6dd13ca05486dbe73581e0163cc9084 |
| PontePassivaRSTV.cs | 0fd696e62144203580ed4187887f57c7d9ccd90a9b886fe0e10b10d65c404e65 |
| SRAdapterPlugin.cs | 5029329e960449239bcf8986512b60234c933498644f3b10198b1c840b9647e2 |
| SRCharacterManager.cs | 5f32ec1d66cf28714f6fd5051bd4beed9e6d141d8106763204cfe5a48305f63e |
| SRJson.cs | 41e4dd93fe2100f4a42b363bda029733f6a6f599e044429583540fa1a7ed7ef1 |
| SRMappingManager.cs | 37241c35ed5adefcde00fd2bf34776d05e92fc9a436a0b53e9c804cd4ecf28cb |
| SROwnerManager.cs | 189a6d73036c691416e84748c7b37a3046564ab3a573afd923fcb1c754e75b78 |
| SRScreenManager.cs | 8c0d7b3dde8480c43687e01cd61380a13c9aa1fc610aa1aee4887a5054f6de13 |
| KIT04Adapter.SR.csproj (Version 0.1.0) | 9f1511bdc19a796dc0a2f86d0ef1e9427827609797ddae0e219bd7f00bf00bc0 |

### 1.3 Recorder (Python — `tools/automacao/runtime/`) — obrigatório
| arquivo | sha256 |
|---|---|
| coletor.py | 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d |
| observacao_passiva.py | 63124b86ccea6a5b46494836f41c0d48011987c4aaaf2fa5261a84f757e1b869 |
| controle_acesso.py | 379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457 |

### 1.4 Runner (Python — `tools/automacao/kit11/executor.py`) — opcional
| arquivo | sha256 |
|---|---|
| executor.py (VERSAO_EXECUTOR=1) | bf03f81b018157b4c73194df6ace95f00998fb77594047fd92eca0fe57fac3e9 |

### 1.5 Viewer (Python — `tools/automacao/kit08/visualizador.py`) — opcional
| arquivo | sha256 |
|---|---|
| visualizador.py | bdd33622a1cec76f83636dc095df73fdfde972072cf0809007d70593cdcfa85f |

### 1.6 Integração KIT-12 e SDK KIT-13 (reuso, não recriado)
| arquivo | sha256 |
|---|---|
| kit12/integracao.py | 480a9a02b7a2f13bb51d4bce32c29897ff944cfca00fd6431a924877a44da25c |
| kit13/packages.py | 60f65437a167d5c08ba09647e1d45a265a1c7d28463793f57bb432546b5ea3c6 |
| kit13/SDK/RegistryV1.cs (API 1.0.0) | 9f2eabdd5da1a3796e7c191f241ff5687d9fb876d51a0bd03117ed1789187700 |
| kit13/SDK/KitSdk.csproj (Version 1.0.0) | d81fc947dfdcc8b379f8ceeabc80a3f9dc96606e318089e165e5c20b9e9e08ce |

**Checagem de identidade**: os hashes acima conferem com o que os pareceres de revisão
declararam (PonteControleRSTV `cad1bcc2…` aprovado em KIT-06F; coletor `159ff2aa…`,
controle_acesso `379d680f…`, executor `bf03f81b…`, visualizador `bdd33622…` (KIT-08F),
integracao `480a9a02…` (KIT-12F2), packages `60f65437…`/RegistryV1 `9f2eabdd…` (KIT-13R)).
Ou seja: o pacote aponta para os fontes **aprovados**, não para cópias divergentes.

## 2. Desenho do pacote

### 2.1 Nome e versão
- Pacote: `kit-rstv` — "Stolen Realm Test Kit" (distribuição **local**, candidata).
- Versão do pacote: **0.1.0** (candidato; sem tag/push/publicação — atos de KIT-G4).
- Versões por componente: core `0.4.0` (declarada na spec KIT-04, csproj sem `<Version>`),
  adapter `0.1.0` (csproj), recorder `1`, runner `1` (`VERSAO_EXECUTOR`), viewer `1.0`,
  sdk `1.0.0` (csproj). Versões lidas do fonte quando existem; onde não existem, declaradas
  como constantes do manifesto, marcadas com a origem (`csproj` | `codigo` | `declarado`).

### 2.2 Layout instalado (sem usuário fixo)
```
<destino>/
  kit-rstv.manifest.json      # identidade, versões, componentes, hashes, deps
  components/
    core/         ...        # fontes C# do Core (sem bin/obj)
    adapter/      ...        # fontes C# do Adapter
    recorder/     ...        # python do recorder
    runner/       ...        # opcional
    viewer/       ...        # opcional
    integracao/   ...        # opcional
    sdk/          ...        # opcional
  tools/                     # instalador/pacote/scan (empacotados junto)
  docs/                      # README PT-BR/EN, primeiro uso, changelog, exemplos
  .kit-rstv-installed.json   # recibo da instalação (componentes, hashes, backup)
```
`<destino>` é descoberto nesta ordem: `--destino` explícito → `KIT_RSTV_HOME` →
`KIT_RSTV_HOME` no arquivo de configuração do usuário → padrão
`<raiz do repositório>/dist/kit-rstv` quando existir layout de repo, senão
`<HOME do usuário>/kit-rstv`. Nunca um caminho com nome de usuário embutido no código.

### 2.3 FLUXO instalador (obrigatório)
`instalar` / `atualizar` / `remover` / `rollback` / `status`:
- toda escrita é precedida de cópia de segurança em `<destino>/../.kit-rstv-backup-<ts>` ou `.bak` por arquivo;
- atualização só troca arquivo cujo hash difere; preserva arquivo local não pertencente ao manifesto (não apaga alteração manual);
- `remover` restaura o que existia antes (rollback) e, sem estado anterior, remove apenas o que o recibo declara;
- verificação de hash **depois** de cada escrita (lê de volta). Falha = rollback automático + exit ≠ 0.

### 2.4 Ferramenta empacotada
`pacote.py` gera `kit-rstv-0.1.0.zip` a partir do manifesto, com allowlist de fontes
(sem `bin/`, `obj/`, `__pycache__`, `.git`, perfil, DLL proprietária). O zip leva junto o
próprio instalador e o scan, de modo que o receptor não precisa instalar SDK para **usar**
(o build C# é opcional e posterior). Uso básico documentado sem Python: extração manual do
zip + remoção manual (passo a passo em `docs/primeiro-uso.md`), exercitado por teste.

### 2.5 Provas exigidas nesta frente (offline)
1. instalar em diretório limpo → hashes conferidos contra o manifesto;
2. atualizar com fonte alterado → só o alterado muda, rollback devolve bytes originais;
3. remover → estado anterior restaurado (rollback) e rastro apagado;
4. descoberta de paths sem usuário fixo (3 estratégias + override);
5. zip candidato gerado, reaberto (`testzip`), sem DLL proprietária/segredo;
6. scan de segredos com controle negativo (planta sintética tem de reprovar);
7. suite própria + contra-prova (defeito plantado tem de reprovar) com exit 0/1/2 distintos.

## 3. Limites declarados (honestos)
- NÃO_EXERCITADO: jogo/BepInEx em runtime, carregamento do plugin, UI/UX, deploy no perfil do dono.
- Build C# exige .NET SDK local e referências Unity do jogo — o pacote **não** redistribui `lib/`.
- Publicação (push/tag/GitHub Release/Thunderstore/`publicar:true`) pertence a KIT-G4 — não executada.
