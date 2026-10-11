# INT-R1-C5 — parte 04: runbook da rodada AUTORIZADA (a medicao em jogo)

Nada deste runbook foi executado nesta rodada: o runtime em jogo e `NAO_EXERCITADO` por decisao do
cartao (a rodada depende de autorizacao do dono). Ele existe para que a rodada seja **uma sequencia de
comandos com veredito**, nao uma sessao de tentativa e erro.

Pre-requisitos: `lib/` do jogo no repo (17 DLLs) e o jogo fechado. Os passos 2, 3, 7 e 8 escrevem no
perfil do dono; **nenhum outro** escreve.

## Passo a passo

```bash
# 0. instrumento verde ANTES de tudo (offline, nao abre o jogo)
python tools/cobertura_ui_localized.py --prova
# -> "Ran 11 tests; failures: 0" e exit 0. Se vermelho, PARE: a trava do mod esta sem prova.

# 1. compilar o probe (nao instala nada)
dotnet build tools/automacao/runtime/LocalizedProbe/LocalizedProbe.csproj -c Release
# -> 0 avisos / 0 erros. A DLL sai em tools/automacao/runtime/LocalizedProbe/bin/Release/netstandard2.1/

# 2. (escreve no perfil) copiar os QUATRO arquivos para a MESMA pasta do plugin
#    destino: %APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\LocalizedProbe\
#      LocalizedProbe.dll
#      RealmApi.dll  RealmApi.Core.dll  RealmApi.Hooks.dll   <- de api/Plugin/bin/Release/netstandard2.1/
#    Sem RealmApi.Core/Hooks o BepInEx nao resolve o probe (nao ha project-reference em runtime).

# 3. (escreve no .cfg) config/com.gumatos.localizedprobe.cfg
#      Autorizado = true
#      Saida = <caminho>\int-r1-c5-observacao-ui-localized.jsonl
#      Sessao = <identidade da rodada>
#    ATENCAO: o cfg nasce sozinho no 1o boot com Autorizado=false; o driver sobrescreve depois.

# 4. abrir o jogo e NAVEGAR (inventario, arvore de skills, tooltips de skill/status/item, level-up)
#    A leitura acontece em toda localizacao em ingles. Fechar o jogo.
#    Conferir no LogOutput.log a linha "LocalizedProbe carregado." (marcador de boot).

# 5. medir (offline; a observacao e runtime)
python tools/cobertura_ui_localized.py \
    --observacoes docs/automacao/runtime/observacao-ui-localized.jsonl \
    --json scratch/int-r1-c5-relatorio-runtime.json
# -> procedencia: runtime; listas de LACUNAS / ENTRADAS QUE NAO RODARAM / NUNCA SERVIDAS
#    e o resumo por categoria e por arquivo.

# 6. aceitar o resultado como contrato (baseline) - so DEPOIS de olhar as listas
python tools/cobertura_ui_localized.py \
    --observacoes docs/automacao/runtime/observacao-ui-localized.jsonl \
    --baseline-out docs/cobertura/revisao/cobertura-ui-localized-baseline.json

# 7. a partir daqui o passo 7b do ritual fica OK e passa a morder:
bash tools/release-check.sh          # 7b. COBERTURA = OK (runtime + baseline verde)

# 8. (escreve no perfil) ROLLBACK: apagar plugins/LocalizedProbe/ e o
#    config/com.gumatos.localizedprobe.cfg criados na rodada; reconferir que
#    plugins/ tem so o que tinha antes.
```

## Como saber que a rodada deu certo (e como saber que NAO deu)

| Sinal | Leitura |
|---|---|
| `Ran 11 tests; failures: 0` (passo 0) | o instrumento esta inteiro antes da coleta |
| `LocalizedProbe carregado.` no log | o plugin subiu (sem isso o JSONL nao existe) |
| JSONL com `"procedencia":"runtime"` e `"hash_fonte"` = `8bb4a7c5...7855a` | a medicao pertence a ESTE build do jogo (gate de identidade passou) |
| JSONL vazio / `{"status":"NAO_EXERCITADO"}` | `Autorizado=false`, ou identidade divergente, ou o hook nao resolveu — o `motivo` esta escrito no proprio arquivo |
| Mediao com `procedencia: FIXTURE` | nao e evidencia de jogo; o passo 7b continua `PENDENTE` |

## Custo/risco da rodada

- Escreve em `plugins/LocalizedProbe/` e em `config/com.gumatos.localizedprobe.cfg` — **so isso**; nao
  toca em saves, nao toca no `Assembly-CSharp.dll`, nao instala mod nenhum, nao mexe no `BetterTooltips`.
- Leitura pura: o probe **assina** `ui.localized` pela API observacional (nao altera `__result`); o
  `BetterTooltips`, esse sim, reescreve o texto — e e justamente o que se quer medir.
- Custo de tempo: 1 build (segundos) + 1 boot com navegacao (minutos).
- Se o gate de identidade divergir (jogo atualizado), o probe **nao** instala o hook — fail-closed, sem
  medicao errada: a API tem de ser atualizada antes (`api/README.md`, guia de atualizacao).
