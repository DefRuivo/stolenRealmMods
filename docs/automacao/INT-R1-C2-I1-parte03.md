# INT-R1-C2-I1 — parte 03: fechamento, reprodutibilidade e o que NÃO foi exercitado

Cartão `t_a706b09c`. Parte 01 = a ponte (entregável A). Parte 02 = o `AUT4Probe` (entregável B).
Esta parte é o fechamento: como reproduzir tudo do zero, o que ficou fora do exercício, e os limites
respeitados.

---

## 1. Como reproduzir (comandos exatos desta rodada)

```bash
# 1) suite offline da ponte (17 testes) + evidencia JSON
dotnet build tools/automacao/kit13/ApiBridgeHarness/ApiBridgeHarness.csproj -c Release -p:DeployToBepInEx=false
dotnet tools/automacao/kit13/ApiBridgeHarness/bin/Release/net6.0/ApiBridgeHarness.dll todos <saida.json>
#    esperado: "Ran 17 tests; failures=0; OFFLINE_ONLY", exit 0

# 2) prova de nao-decorativo (10 mutacoes 0->1->0, sandbox proprio)
python tools/automacao/kit13/prove_bridge_mutations.py --out <diretorio NOVO>
#    esperado: "BRIDGE_MUTATIONS_PASSOU|10|<dir>", exit 0; verification.json com live_changed: []

# 3) preflight offline (erro fechado se DeployToBepInEx != 'false')
dotnet msbuild tools/automacao/kit13/ApiBridge/ApiBridge.csproj -t:Kit13OfflinePreflight -p:DeployToBepInEx=true   # exit 1, "KIT13:"
dotnet msbuild tools/automacao/kit13/ApiBridge/ApiBridge.csproj -t:Kit13OfflinePreflight -p:DeployToBepInEx=false  # exit 0

# 4) os dois builds do entregavel B
dotnet build tools/automacao/runtime/AUT4Probe/Companheiro/Companheiro.csproj -c Release -p:DeployToBepInEx=false
dotnet build tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj -c Release -p:DeployToBepInEx=false

# 5) a medicao de cobertura da parte 02
dotnet build api/tools/Inspect/Inspect.csproj -c Release
dotnet api/tools/Inspect/bin/Release/net6.0/Inspect.dll targets lib/Assembly-CSharp.dll
ilspycmd lib/Assembly-CSharp.dll -t OptionsManager
```

Resultados medidos nesta rodada: (1) `Ran 17 tests; failures=0` exit 0; (2) 10 RED provados com sha256
restaurado; (3) exit 1 / exit 0 como acima; (4) companheiro 0 avisos/0 erros, probe 0 erros e **1 aviso**
`MSB3277` de resolução de referências (`netstandard2.1` × `Assembly-CSharp`) que **já existia antes das
edições** — conferido removendo o companheiro de cena e reconstruindo: o aviso continua
(`grep MSB3277` no log), e nenhuma `<Reference>` foi adicionada ou removida pelo cartão.

`AUT4Probe.csproj` não tem alvo de deploy (`:18`), então nenhum build escreveu no perfil r2modman.

## 2. Evidências gravadas (tudo em `docs/automacao/INT-R1-C2-I1-evidencias/`)

| Arquivo | O que é |
|---|---|
| `suite-17-testes-baseline.json` | evidência JSON da suíte completa (17 testes, `offline: true`) |
| `suite-baseline.log`, `suite-final.log` | saída da suíte antes das mutações e no fim (verde de novo) |
| `mutations.json` | por mutação: fonte, substituições, testes vermelhos, sha256 antes/restaurado |
| `verification.json` | `live_changed: []`, `sandbox_divergente_do_baseline: []`, `mutacoes: 10`, suíte final |
| `commands.json` | todos os comandos do script com o exit code observado (inclui os preflights) |
| `m*-RED-*.log` | os logs de vermelho, um por mutação e por asserção derrubada |
| `inspect-targets-optionsmanager.json` | saída do `api/tools/Inspect targets` (recorte do binário alvo) |
| `ilspycmd-optionsmanager-localize.txt` | cross-check independente com `ilspycmd` |
| `AUT4ProbePlugin-pre-edicoes.cs.txt` + `edicoes-aut4probe.diff` | reconstrução pré-edição e o diff das 5 edições (com o limite de 1 linha declarado na parte 02) |

## 3. NAO_EXERCITADO consolidado (com motivo) — nada aqui foi promovido a verde

| Item | Por quê |
|---|---|
| Harmony real (`HookInstallation.Install`), postfix no `Assembly-CSharp`, `EnableHooks=true` | exige o jogo; o cartão proíbe instalar/abrir/deployar |
| Adaptador dentro do processo do jogo, com hook real | idem |
| Companheiro carregado por `Assembly.Load` no `BepInEx/plugins` | idem (é deploy) |
| Rodada em jogo do `AUT4Probe` comparando com `AUT-4-evidencias/` | idem; a igualdade com a ponte off foi conferida por leitura |
| Clique/navegação do probe (`t_139f714f`, `0xc0000005`) | fora do escopo: a API 0.1.0 é observacional e não dirige input |
| `api/**` fiação do host (`RealmApiPlugin` construindo o adaptador — D5/D7) | frente nova; este cartão entrega o adaptador, não a fiação do plugin |

## 4. Limites respeitados

- **Nenhum** arquivo congelado foi alterado: `api/Core/Contracts.cs`
  (`7970780440d1682a…`) e `kit13/SDK/RegistryV1.cs` (`9f2eabdd5da1a379…`) com os mesmos sha256 da linha
  de base do pai; `prove_mutations.py`, `prove_offline.py`, `packages.py`, `test_packages.py` e
  `examples/*.json` não foram tocados (a prova nova é um script **novo**, ao lado).
- Nada de `git add`/`commit`/`push`; nenhuma instalação; nenhum deploy no perfil r2modman; o jogo não foi
  aberto; nenhum token/PAT em arquivo, log ou resumo.
- `AUT4ProbePlugin.cs` fora das 5 edições da parte 02 não foi tocado; `LeituraAgregados.cs` (sujo por
  outro cartão) não foi aberto.

## 5. Próximo passo natural (não executado aqui)

Fiação do host: `RealmApiPlugin` (ou o driver do instrumento) chamando
`RealmHooksBinding.Create(registry, RealmHooks.Observed, producerActive, session, diagnostic)` com
`producerActive` = `EnableHooks && ApiIdentity.Matches(...)` e `session` = a sessão da rodada. Isso é
frente nova (mexe em `api/Plugin`, congelado aqui) e continua sem prova em jogo até uma rodada
autorizada.
