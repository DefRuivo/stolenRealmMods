# KIT-16 — REVISAO INDEPENDENTE (t_2886b6de)

> Revisor: perfil `default`, run **701** (sessao nova) — **nao** e o implementador (run 700).
> Rodada: **1** (zero `changes_requested` no historico) — lente **ARTIFACT** (leitura fria do
> entregavel, antes/junto do resumo do implementador) reforcada por execucao propria.
> Data: 2026-10-10 (BRT, UTC-03:00). Nenhum arquivo de implementacao foi editado pelo revisor.

## VEREDITO: APROVADO

Os criterios de aceite do cartao foram mapeados a evidencia e todos passaram nas minhas
proprias medicoes. As lacunas declaradas pelo implementador foram conferidas e sao
**honestas** (nao escondem defeito). Ressalvas nao-bloqueantes em §5.

## 1. Mapeamento criterio -> evidencia (conferido por mim)

| criterio do cartao | evidencia | como conferi |
|---|---|---|
| 1. localizar o `persistentDataPath` efetivo e qualquer outro dir de dados, **por codigo/log** | `KIT-16-parte01/02` + dump `Assembly-CSharp.decompiled.cs` | `grep -c persistentDataPath` = **31** (bate com o doc); `FileSystem.persistentDataPath => _cachedPersistentDataPath ?? Application.persistentDataPath` na linha 106729 e **zero atribuicoes** a `_cachedPersistentDataPath` no dump; consumidores (`Character{N}.json`, `GlobalSaveData.json`, `SaveFile.db`, `ItemStash`, `TransmogList`, `QuestSave*`, `CrossPromo`, `logs.txt`, screenshots, multiplayer) todos sob `pdp` |
| 1b. segundo local de dados (nao-diretorio) | registro `HKCU\Software\Burst2Flame Entertainment` | tratado por export/delete/import; conferido por hash (abaixo) |
| 2. snapshot SHA256 por arquivo ANTES | `scratch/kit/KIT-16-run700/run-real-3/antes.manifest` (10856 B, sha256 `62e0aeea…`) e `antes.sha256` = o mesmo hash | `sha256sum` = `62e0aeea556478d34d16af59d93a0d1370ac275bf5c6d69246c9401a27c3ac61` identico |
| 3. isolamento comprovado (junction NTFS no caminho exato + rename reversivel) | `kit16-save-isolado.sh` preparar/restaurar + `kit16-junction.ps1` | li o script frio: rename `REAL -> REAL.kit16-real`, junction criado por `New-Item -ItemType Junction`, remocao por **`RemoveDirectoryW`** (nao `Remove-Item -Recurse`/`rm -rf`, que atravessariam o link); guarda recusa com o jogo aberto e recusa containment da area isolada dentro do dir do dono |
| 3b. escrita real ATRAVES do junction | `run-real{,-2,-3}/verificar-diff.json` | diff de conteudo na copia isolada: `Player.log` + `Player-prev.log` alterados nas 3 rodadas; na 2a/3a tambem 4 arquivos novos de `Unity/…/Analytics/ArchivedEvents/<ts>.*` — arquivos que so o **processo do jogo** (log nativo do Player Unity e analytics) escreve |
| 4. restauracao ao estado do snapshot, com evidencia antes/depois | `run-real{,-2,-3}/restauracao.json` (`restauracao_rc: 0`, `falhas: 0`) + `registro.json` (`antes == depois`) | reproduzi a comparacao final por fora do harness (abaixo) |
| 5. uma execucao no ambiente isolado com o hash do dir REAL inalterado | 3 rodadas reais (PIDs 26332/23356/10096, `steam -applaunch 1330000`) | **medicao independente minha, pos-tudo**: `python tree_snapshot.py comparar KIT-16-run700/run-real-3/antes.manifest "C:/Users/Pichau/AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm"` -> `{"total_antes":111,"total_depois":111,"novos":[],"removidos":[],"alterados":[],"igual":true}`, **exit 0** |
| ACEITE: script/runbook + hashes antes/depois + declaracao do exercitado/nao | `scratch/kit/kit16-save-isolado.sh` (runbook §9 do `KIT-16-entrega.md`) + §6 "o que NAO foi exercitado" | lido; sem numero/dado sintetico encontrado |

## 2. Integridade dos artefatos (sha256 medidos por mim, iguais aos declarados)

    scratch/kit/kit16-save-isolado.sh        3a571db3298dd6b4c999445df390aa5745b2f4da157c0666bb6365c3815b93da   (23134 B)
    scratch/kit/kit16-junction.ps1           41e942e458186949c04146090a1426634020592b01a08727524db718787896a2   (2379 B)
    scratch/kit/kit16-controle-negativo.sh   5b710dadbe33abe1038e88f401856d5606c1a9bca2af1144eeaf4d6556878bc8   (4283 B)
    docs/automacao/KIT-16-parte01.md         bceab0c43e40c3b28143e05bfa7988d4b9d04e3c4c6a4c9f4afbd6064b08fb5c
    docs/automacao/KIT-16-parte02.md         3db4895bcec0ccb2cc66a523520e12207bd3e2b4ea5a6129b440437460a37754
    docs/automacao/KIT-16-parte03.md         08be2951435ca6d4189f617a66ae62fe1af8230a1491ffb14d43f7abc499e978
    KIT-16-run700/dump/Assembly-CSharp.decompiled.cs  873a2d1dc153fcd7191100bb481f4bd681374f68e38c8241c0172e7c91465407  (17815971 B)
    KIT-16-run700/run-real-3/LogOutput-isolado.txt    640966e58fb7c44bc0cbde7835a796d4bb21c41d8f3f98ced60a0c39c21786f4  (855 B)

Evidencias de rodada tambem conferidas por hash, todas iguais ao doc §8: `run-real/preparar.json`
`1f45e0be…`, `run-real/verificar-diff.json` `3c1bc875…`, `run-real-2/verificar-diff.json`
`0b110da9…`, `run-real-3/verificar-diff.json` `7cad7fcf…`, `controle-negativo/resultado.json`
`58fede59…`. Nada sobrescrito: os arquivos sao novos e o `KIT-16-entrega.md` nao tem hash
pre-declarado (o handoff citou tamanho 11690 B, conferido).

## 3. Provas que EU reproduzi (nao apenas li)

1. **Dir real intacto e sem residuo.** O caminho real responde `state` = **`real`** (nao junction);
   `ls` de `.../Burst2Flame Entertainment/` mostra apenas `Stolen Realm` — **nenhum** `*.kit16-real`.
   O `LogOutput.log` do perfil do dono tem mtime **10/10 00:03**, anterior as rodadas (13:37–13:43).
2. **Registro restaurado de fato (medicao viva).** `reg.exe export "HKCU\Software\Burst2Flame
   Entertainment"` agora, hasheado por mim: `31bb4e1f0530c749817c207d6843b07a2e9e0726c0e703b40d1bc705def0bd7b`
   — **igual** ao `registro_antes/registro_depois` das 3 rodadas e ao par `kit16-iso/registro-antes.reg` /
   `registro-depois.reg` (ambos 1263206 B, mesmo hash). Ou seja, o ramo do dono esta hoje no estado pre-rodada.
3. **Fixture completa, independente, em sandbox meu** (`$TMPDIR/kit16-rev`, dir ficticio de 3 arquivos):
   `KIT16_FIXTURE=1 bash kit16-save-isolado.sh fixture` -> `VERIFICAR: OK`, `RESTAURAR: OK`,
   `FIXTURE: OK`, **exit 0**; diff classificou `novos [Character99.json, CrossPromo/c.txt]` e
   `alterados [GlobalSaveData.json]`; a arvore "real" ficou `igual: true`.
4. **Controle negativo reexecutado por mim** (copias do harness/ps1/tree_snapshot em sandbox proprio, sem
   tocar as evidencias entregues) -> **3/3**: NC-A junction ausente => `verificar` exit 1 "nao e junction";
   NC-B conteudo adulterado => `restaurar` exit 1 "DIVERGE do snapshot antes"; NC-C ciclo limpo => exit 0.
   **Nao e verde tautologico** — o mesmo comparador que aprova NC-C reprova NC-B na minha propria execucao.
5. **Achado negativo conferido no codigo (nao ha escrita fora do alvo):**
   `Application.dataPath` (8 ocorrencias) e usado para LEITURA (`StreamingAssets`, `AssetBundles`,
   demo PolyFew); `Directory.CreateDirectory` aparece so para `CacheDirectory = pdp/CrossPromo`;
   `temporaryCachePath`/`SpecialFolder`/`MyDocuments`/`LocalLow` = **0** ocorrencias.
   O diretorio de instalacao `E:\SteamLibrary\...\Stolen Realm` **nao tem nenhum arquivo modificado**
   depois de 10/10 13:30 (sem `output_log.txt`; `redirect_output_log = false` no `doorstop_config.ini`)
   => a rodada nao escreveu fora do caminho isolado + registro.
6. **Achado de valor para o KIT-14 (conferido).** `runtime-isolado.sh` (KIT-03) de fato **nao** passa
   `--doorstop-mono-dll-search-path-override` (grep: so `--doorstop-enabled` + `--doorstop-target-assembly`);
   o log isolado preservado mostra `BepInEx 5.4.23.5`, `1 plugin to load`, `Loading [Reload Probe 1.0.0]`,
   `ReloadProbe v1 carregado.` e **zero** ocorrencias de `r2modmanPlus-local` no log isolado.
7. **Preservacao.** `git rev-parse HEAD` = `d82894ebe95d97f26b7989a848372c691dcb8ef6` (inalterado);
   `git status` sem nada staged; o jogo nao estava rodando; nenhum build/deploy/publicacao/commit.

## 4. Lacunas declaradas pelo implementador — conferidas e consideradas honestas

- **Escrita de SAVE pelo jogo NAO_EXERCITADA**: os diffs mostram que nas 3 rodadas o jogo escreveu
  apenas `Player.log`/`Player-prev.log`/eventos de Analytics — **nao** tocou `Character*.json`,
  `GlobalSaveData.json`, `SaveFile.db`. O implementador declara isso explicitamente (§6) e nao
  apresenta isso como provado. O que esta provado e o **redirecionamento do caminho** (o processo
  escreveu arquivos de log/analytics dentro da area isolada, e a prova de escrita atraves do junction
  passa no `verificar`), nao a escrita de save. Correto e sem exagero.
- **Navegacao/UI/mods de gameplay/desempenho/segunda instalacao**: NAO_EXERCITADO, declarado (objeto do KIT-14).
- **Risco residual Steam Cloud** (app 1330000 com `autocloud lastexit`): medido e declarado; o conteudo
  que mudou na area isolada foram logs/analytics, e os arquivos de save tinham conteudo identico ao do dono.
  Decisao do dono, nao do revisor.

## 5. Ressalvas NAO-BLOQUEANTES (nao reabrem o cartao)

1. A area isolada `scratch/kit/kit16-iso/` (copia dos dados + `antes.manifest` + exports de registro)
   continua no disco — o passo `limpar` do runbook nao foi executado. Nao e residuo no diretorio do
   dono (verificado) nem defeito do mecanismo; e lixo de scratch que o proximo consumidor pode remover.
2. `parte02` §A cita a linha `92798` entre os usos de `Application.dataPath`; ela e de
   `streamingAssetsPath` (mesma familia, leitura). Detalhe de citacao, sem efeito no veredito.
3. O harness escreve a prova de escrita (`.kit16-prova-escrita.txt`) dentro do caminho real — passa pelo
   junction e e apagada em seguida; nao altera o dir do dono (o `verificar` roda com o junction ativo).

## 6. O que esta revisao NAO aprova

Aprovacao tecnica desta revisao **nao** e aceite humano, nao e publicacao de DoD e nao autoriza
runtime/navegacao do KIT-14 por si so: o KIT-14 apenas deixa de ter este cartao como dependencia
pendente. A escrita de save pelo jogo, a cadeia UI/PNG/relatorio e as metricas de desempenho
continuam NAO_EXERCITADAS.
