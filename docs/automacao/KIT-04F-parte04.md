# KIT-04F — parte 04: resultados de execução (suíte, controle negativo, build)

Tarefa `t_d5c98d36` (KIT-04F) · 2026-10-09 · offline. Complementa a `KIT-04F-parte03.md` (§2 e §3)
com as **saídas reais** medidas. Nada aqui é resumo de intenção: cada linha tem um `exit` e um log.

## 1. Build dos csproj entregues (cópia isolada, `-p:DeployToBepInEx=false`)

```
dotnet build KIT04Core/KIT04Core.csproj            -c Release -p:DeployToBepInEx=false  -> EXIT 0, 0 Erro(s), 18 Aviso(s)
dotnet build KIT04Adapter.SR/KIT04Adapter.SR.csproj -c Release -p:DeployToBepInEx=false  -> EXIT 0, 0 Erro(s), 19 Aviso(s)
```

Os três erros do parecer (`CorePlugin.cs(228,49) CS1069`, `(231,29) CS0103`, `(261,39) CS1069`)
**não ocorrem**: o caminho de captura compila.

## 2. Suíte de contrato contra o repositório

Comando: `bash scratch/kit/testes/roda_kit04f.sh`
Log: `scratch/kit/logs/kit04f-suite-repo.log`

```
Ran 13 tests in 5.046s
OK
runner KIT-04F — exit=0
```

O harness comportamental imprimiu `HARNESS: VERDE` com as 23 asserções em `OK`
(entre elas: `default habilitado == false`, `AUSENTE => LerTodos null`,
`habilitado => CapturarPNG true`, `PNG escrito em disco`, `IdentidadeDoCore.Sha256('abc') confere`).

## 3. Controle negativo (defeito plantado) — veredito

Comando: `bash scratch/kit/controle-negativo-kit04f.sh`
Logs por caso: `scratch/kit/logs/<caso>.log`

```
  OK      [A-limpo]                    exit=0 (esperado 0)  Ran 13 tests in 8.908s
  OK      [B-habilitado-default-true]  exit=1 (esperado 1)  Ran 13 tests in 7.328s
  OK      [C-sem-modulo-captura]       exit=1 (esperado 1)  Ran 13 tests in 7.697s
  OK      [D-leitor-array-vazio]       exit=1 (esperado 1)  Ran 13 tests in 7.607s
  OK      [E-hash-placeholder]         exit=1 (esperado 1)  Ran 13 tests in 6.141s
  OK      [F-adapter-ausente]          exit=1 (esperado 1)  Ran 13 tests in 4.420s

Casos: 6  |  OK: 6  |  FALHOU: 0
VEREDITO: OK — suite VERDE sem defeito (exit 0) e VERMELHA com cada defeito (exit 1)
CONTROLE_EXIT=0
```

Exit codes **distintos** (0 vs 1) — critério do item 7 satisfeito.

### 3.1 Qual teste caiu em cada caso (o defeito é discriminado, não só "quebrou")

| Caso | Testes que reprovaram (do log do caso) |
|---|---|
| B | `T03_harness_roda_e_fica_verde` (default virou `true`), `T04_habilitado_default_false_na_fonte`, `T06` [CorePlugin.cs] |
| C | `T01_build_core_exit0_e_dll` (o build **falha** sem o módulo), `T02_build_adapter`, `T04_modulos_captura_referenciados`, `T06` [KIT04Core.csproj] |
| D | `T03_harness_roda_e_fica_verde` (array vazio no lugar de null), `T04_lercomponentes_ausente_vira_null`, `T06` [ComponentReaderImpl.cs] |
| E | `T05_hashes_reais_no_entregavel` |
| F | `T02_build_adapter_exit0_e_dlls`, `T04_adapter_completo`, `T04_adapter_desabilitado_por_padrao`, `T06` |

Cada defeito derruba o teste **correspondente** ao item que ele reverte — não é uma falha
genérica. Os testes de identidade (`T06`) também caem porque o artefato alterado deixa de bater
com o hash declarado: é o efeito colateral esperado de adulterar o arquivo.

## 4. O que NÃO foi exercitado (declarado, nunca verde por omissão)

- **Runtime em jogo** (telas, personagens, owners, captura real de frame): exige rodada autorizada
  do AUT-4. O stub do harness compila as chamadas ao Unity, não as executa em engine.
- **Equivalência numérica** Core+Adapter vs. `runtime/out/ex1-offline.json`: precisa da saída real
  do jogo; INDETERMINADO.
- **Perfil do dono / instalação / publicação**: intocados. O jogo não foi aberto. Builds sempre em
  `scratch/kit/build/…`, com `-p:DeployToBepInEx=false`.
