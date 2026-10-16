# KIT-14F — parte 01: orientação, evidência e plano (RED antes do conserto)

Cartão: t_c46abdf7 (KIT-14F). Autor: default/run705. Data local do terminal: 2026-10-10 16:44 -03.
Workspace do kanban: `%USERPROFILE%\AppData\Local\hermes\kanban\workspaces\t_c46abdf7`.
Repositório do projeto (onde vive o código a consertar): `C:\dev\stolen-realm`, branch `ci-validate-test`.

Este artefato NÃO sobrescreve nada: é o primeiro de uma série numerada (`KIT-14F-parteNN.md`).

## 1. O que a evidência do run704 diz (lida antes de mexer)

Fonte: `docs/automacao/KIT-14-entrega-run704.md` (run704 = cartão t_a1f38855, ainda ABERTO).
Confirmado no texto, sem reinterpretar:

1. **Adapter cai em Awake com NullReferenceException.** ACHADO REAL: `Player.log` da condição
   with-passive, linha 46, `NullReferenceException` em `KIT04Adapter.SR.SRAdapterPlugin.Awake`;
   `LogOutput` isolado mostra o Chainloader listando o Adapter ANTES do Core (linhas 19–20).
   O código vivo (`tools/automacao/runtime/KIT04Adapter.SR/SRAdapterPlugin.cs`) lê
   `CorePlugin.Instancia` na linha 40 e acessa `core.Passivo` na linha 55, SEM guarda.
   A causa é hipótese compatível com a ordem observada — o run704 declarou explicitamente que
   NÃO é prova causal isolada, e que o conserto é trabalho deste cartão.
2. **Recorder efetivo não comprovado.** Não há contagem nem arquivo de saída do recorder; por
   isso o run704 se recusou a apresentar número de overhead de recorder.
3. **Handler acha 0 botões / sem Skills.** A navegação por handler in-process do `AUT4Probe`
   leu `botoes_ativos=0`, `achou_skills=false`, nenhuma invocação; o PNG das duas sessões era
   tela de LOADING (Barrels/Shrines), não Skills/RSTV.

## 2. Onde está cada defeito no código (lido nesta rodada)

- Defeito 1 — `tools/automacao/runtime/KIT04Adapter.SR/SRAdapterPlugin.cs`
  - linha 12: `[BepInPlugin("com.gumatos.kit04.adapter.sr", ...)]` — SEM nenhum `[BepInDependency]`.
    O Adapter não declara que depende do Core, então o Chainloader (BepInEx 5) não tem por que
    ordenar Core antes de Adapter.
  - linha 40: `var core = CorePlugin.Instancia;` — `CorePlugin.Instancia` é `=> _instancia!`
    (supressão de nullable), então um Core não inicializado devolve **null** sem exceção.
  - linha 55: `new PontePassivaRSTV(..., core.Passivo)` — **é aqui que estoura** (null.Passivo).
  - Definição do Core: `tools/automacao/runtime/core/CorePlugin.cs:19-20` e `_instancia = this`
    só no `Awake` (linha 173), `Passivo` criado no `Awake` (linha 205).
- Defeito 2 — o “recorder” é a trilha passiva: `CorePlugin.Passivo` (`PipelinePassivo`) alimentada
  pela ponte do Adapter (`PontePassivaRSTV`), com o resultado consolidado em
  `CorePlugin.ResultadoFinal()` (`eventos`, `passivo`, descartes). O `Update` do Adapter
  (`SRAdapterPlugin.cs:76-91`) é quem injeta as observações; se o `Awake` morre, essa trilha
  nunca existe — que é exatamente o achado do run704.
- Defeito 3 — `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs:842-867`
  (`TentarNavegar`). Chamada UMA vez, em `F_LEITURA` (linha 413), no mesmo quadro da leitura:
  - varre `Recursos<Button>()` (linha 849) e escolhe o primeiro com rótulo contendo "Skills";
  - grava `estagios` com `botoes_ativos` e `achou_skills` e **encerra** — sem espera por quadro,
    sem número de tentativas, sem motivo declarado quando não acha, e sem repetir quando a tela
    alvo ainda não existe (o caso do loading). Não há costura injetável para exercitar a escolha
    offline.

## 3. Infraestrutura reaproveitada (não reimplementar)

- `tools/automacao/runtime/harness-passivo` — harness OFFLINE em `net6.0` que compila por LINK os
  fontes reais (`core/PipelinePassivo.cs`, `KIT04Adapter.SR/PontePassivaRSTV.cs`) e prova
  ligação/estado sem abrir o jogo; exit 0 verde / 1 falha / 2 infraestrutura. É o modelo adotado.
- `tools/automacao/runtime/roda_testes_runtime.py` — runner dos testes offline (`t_*.py`).
- `tools/automacao/kit13` (`CoreBridge/CorePluginBinding.cs`) — precedente documentado:
  *“Chamar no main thread depois de inicialização explicitamente confirmada pelo host, nunca
  assumir CorePlugin.Instancia/Awake pela ordem de DLLs.”* É a mesma classe de defeito do Adapter.
- `tools/automacao/runtime/AUT4Probe` — instrumento (opt-in, somente leitura) que contém o defeito 3.
- `Directory.Build.props` — deploy é OPT-IN (`-p:DeployToBepInEx=true`); build comum NÃO copia
  nada para o perfil do dono. Toda compilação desta rodada usa o default (não instala).

## 4. Fatos medidos nesta rodada (antes de qualquer conserto)

- `dotnet --version` = 6.0.428; runtimes disponíveis: 6.0.36, 8.0.22, 10.0.12.
- Build do Adapter ATUAL (código ainda com o defeito), `-c Release`,
  `-p:GameManaged="E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed"`:
  **0 Erros** (65 avisos). Ou seja: o defeito 1 é um defeito de RUNTIME, o build não o pega —
  logo um teste vermelho aqui será vermelho por comportamento, não por build quebrado.
- Carregamento das referências reais dentro de um processo `net6.0` (sonda `probe`, ver parte 02)
  funciona: `BepInEx, Version=5.4.23.5` e `UnityEngine.CoreModule` carregam, e
  `BepInEx.BaseUnityPlugin` expõe os backing fields `<Config>k__BackingField`,
  `<Logger>k__BackingField`, `<Info>k__BackingField` — dá para montar o plugin real por reflexão
  sem a engine do jogo.

## 5. Plano de correção e prova (teste antes / depois)

| # | Defeito | Teste (mesmo arquivo antes e depois) | Antes | Depois |
|---|---------|--------------------------------------|-------|--------|
| 1 | Adapter cai em Awake (NRE) | `harness-kit14f --parte1`: monta o plugin REAL por reflexão, roda `Awake` na ORDEM OBSERVADA (Adapter antes do Core) e exige: (a) nenhuma exceção; (b) estado "aguardando Core" declarado; (c) `[BepInDependency("com.gumatos.kit04.core")]` presente; (d) após o `Awake` do Core, o vínculo conclui e cria a ponte | NRE / sem atributo / sem vínculo ⇒ REPROVA | passa |
| 2 | Recorder sem contagem/arquivo | `harness-kit14f --parte2`: usa a ponte REAL criada pelo Adapter, alimenta transições de tela e um clique pelo MESMO método que o `Update` chama, e exige contagem > 0 **e** um arquivo de resultado lido de volta do disco | 0 eventos / nenhum arquivo (a trilha nunca nasce) ⇒ REPROVA | passa |
| 3 | Navegação acha 0 botões | `harness-kit14f --parte3`: dirige o rotina de navegação do probe REAL por vários quadros, com porta injetável, e exige: espera com contagem de tentativas, motivo declarado quando esgota, e exatamente 1 invocação quando o alvo aparece | 1 etapa só, sem tentativas/motivo ⇒ REPROVA | passa |

Regras desta rodada: sem clique de sistema; sem tocar no perfil/save do dono (nada é instalado,
`DeployToBepInEx` fica no default `false`); nada de `execute_code` (só `terminal`); o que não for
exercitável sai declarado como `NAO_EXERCITADO` com motivo, nunca estimado.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
