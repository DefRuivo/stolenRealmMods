# INT-R1-C5 — parte 03: veredito para o mod, ritual, runbook da rodada autorizada e limites

## 1. O que muda para o `BetterTooltips`: NADA (veredito declarado, exigido pelo cartao §4)

| Afirmacao | Prova |
|---|---|
| Nenhum arquivo do mod foi alterado | `00-hashes-antes.txt` x `08-hashes-depois.txt`: **17 arquivos, sha256 identico** (`diff` vazio em `09-diff-hashes.txt`); `git status --porcelain BetterTooltips/` = **vazio** |
| O mod continua **standalone** | nenhum `BepInDependency` e nenhuma referencia a `RealmApi` foram adicionados; o instrumento e o probe vivem FORA do mod (`tools/`) |
| O mod **nao** migra para a API | ele precisa REESCREVER `__result` (`LocalizePatch.cs:2482-2496`); a base 0.1.0 e observacional (`api/README.md:42,145-146`) — migrar seria mudar a base, nao o mod |
| O instrumento e **opt-in** | sem observacao de runtime o passo do ritual fica `PENDENTE`; `--prova`/`--observacoes`/`--verificar` sao chamadas explicitas |

Veredito: **o mod fica como esta**. O instrumento e bancada: mede, nao conserta e nao instala.

## 2. Ligacao no ritual (passo ADJACENTE, sem renumerar nada)

`tools/release-check.sh`, entre o 7 e o 8:

```
== PASSO 7b/9 — COBERTURA (instrumento ui.localized; mod NAO muda) ==
   Ran 11 tests; failures: 0
   VERDE: todos os casos do instrumento passaram (inclui o caso NEGATIVO: ...)
...
  [ OK ]   4. CHAVES      298 chaves extraidas, 294 no censo, 4 fora
  [ OK ]   5. DUPLICADAS  TextFixes    101 entradas | duplicadas: nenhuma
  [ OK ]   7. COMPARTILH. 0 chave nas duas tabelas; 12 suspeita(s) (aviso humano)
  [PEND.]  7b. COBERTURA  Ran 11 tests; failures: 0; medicao em jogo NAO_EXERCITADA (sem docs/automacao/runtime/observacao-ui-localized.jsonl)
  [PEND.]  8. CICLO       NAO RODOU no fluxo normal ...
```

`10-release-check.txt` (saida integral do ritual). Regras do passo:

- roda `--prova` **sempre**: se a prova do instrumento ficar vermelha, o passo REPROVA (a trava do mod
  ficou sem prova) — foi assim que o caso negativo deixou de ser promessa e virou trava de release;
- se existir `docs/automacao/runtime/observacao-ui-localized.jsonl` com `procedencia: runtime`, roda a
  medicao e a TRAVA do baseline (`docs/cobertura/revisao/cobertura-ui-localized-baseline.json`);
- observacao de FIXTURE ou ausente -> `PENDENTE` (nao reprova, mas **nao** se disfarca de aprovado).

`10-release-check.txt` registra o veredito final do ritual: **REPROVADO — passo 3 (BUILD)**, e o achado
nao e desta rodada: a guarda `check_deploy_optin.py` varre o repositorio INTEIRO e tropeca em iscas de
rodadas anteriores sob `scratch/kit/KIT-14-run699|run710/` (mtime **2026-10-10**; `scratch/` e gitignored,
`.gitignore:49`; `find scratch -name '*.csproj' -newermt '2026-10-11 04:32:00'` = vazio) — prova em
`11-achados-passo3-pre-existentes.txt`. Nenhum `.csproj` desta rodada entra na varredura do passo 3 (o
probe vive em `tools/automacao/runtime/LocalizedProbe/`, fora do `-maxdepth 2`). Limpar as iscas de
`scratch/` e de outra frente; aqui so se registra que o vermelho **pre-existe** e nao vem daqui.

No CI (`.github/workflows/validate.yml`, passo `7b`): roda SO `python tools/cobertura_ui_localized.py
--prova` — offline, sem jogo, sem perfil.

## 3. Runbook da rodada AUTORIZADA (a medicao em jogo)

Ordem e o que cada passo prova. Nada aqui foi executado nesta rodada.

1. `dotnet build tools/automacao/runtime/LocalizedProbe/LocalizedProbe.csproj -c Release`
   -> prova: compila (ja medido: 0 avisos/0 erros).
2. Copiar para `.../profiles/Default/BepInEx/plugins/LocalizedProbe/` os **quatro** arquivos:
   `LocalizedProbe.dll`, `RealmApi.dll`, `RealmApi.Core.dll`, `RealmApi.Hooks.dll`
   (as duas ultimas vem do build de `api/Plugin/RealmApi.csproj`; sem elas o BepInEx nao resolve o probe).
   -> escreve no perfil do dono: e a unica etapa que faz isso, e e ele quem autoriza.
3. `BepInEx/config/com.gumatos.localizedprobe.cfg`: `Autorizado = true`,
   `Saida = <caminho>/int-r1-c5-observacao-ui-localized.jsonl`, `Sessao = <identidade da rodada>`.
4. Abrir o jogo e navegar (inventario, arvore de skills, tooltips, level-up) — a leitura acontece em
   toda localizacao em ingles. Fechar o jogo.
5. `python tools/cobertura_ui_localized.py --observacoes docs/automacao/runtime/observacao-ui-localized.jsonl --json <relatorio.json>`
   -> le `procedencia: runtime`, a lista de **lacunas** (textos servidos que nenhuma tabela cobre), as
   `entradas que nao rodaram` (INC-1/INC-2 em jogo) e as `chaves mortas`.
6. Aceitar o resultado: `--baseline-out docs/cobertura/revisao/cobertura-ui-localized-baseline.json`
   (nasce com `procedencia: runtime` e o sha256 das tabelas). A partir dai o passo 7b do ritual fica
   `OK` e passa a morder quando alguem remover uma entrada cobrada.
7. Remover o probe do perfil e restaurar o `.cfg` (a rodada cria o cfg sozinho; o rollback e parte da
   rodada, como no AUT-4).

## 4. Achados desta rodada (com o rotulo certo)

Medidos sobre a fixture derivada do censo (`04-relatorio-fixture.txt`), portanto **candidatos**, nao
conclusoes de jogo:

- **4 chaves das tabelas fora de todo o censo**: `Resist Divine` e `Resistance Divine` (grafia
  duplicada — uma das duas provavelmente nunca dispara) e as duas dicas de loading. As dicas ja estavam
  declaradas fora do censo; as duas de Resist sao **candidata a chave morta** a conferir na rodada em jogo.
- **34 entradas nunca servidas** pela fixture — inclui as 4 acima mais 30 chaves que o instrumento nao
  indexa por `descricao` (batem so na coluna `nome` de outros CSVs). Numero a reavaliar com a observacao
  de runtime, que serve o texto de verdade.
- **0 chaves nas duas tabelas** (BUG-32 limpo hoje, confirmado tambem pelo passo 7 do ritual: `0 chave
  nas duas tabelas; 12 suspeita(s)`).
- **distribuicao da cobertura**: as tabelas cobrem sobretudo skills/status/powerups (85/107/54 textos do
  censo); itens e afixos aparecem com 9 cada. Isso descreve o que o mod se propoe a cobrir — nao e
  lacuna por si, e a rodada em jogo diz o que falta de verdade.

## 5. NAO_EXERCITADO (com o motivo)

- **Runtime em jogo (o JSONL de `procedencia: runtime`)**: exigiria instalar o probe no perfil do dono e
  abrir o jogo — rodada autorizada, nao pedida nesta tarefa (o cartao manda declarar `NAO_EXERCITADO`).
- **Carregamento do `LocalizedProbe` pelo BepInEx e a assinatura do hook em processo**: so existe em jogo.
  O que esta exercitado e a compilacao (0 avisos/0 erros) e a constante do gate (sha256 conferido).
- **A medicao com observacao de runtime e a TRAVA sobre ela**: exercitadas sobre fixture e sobre os
  testes versionados; sobre runtime, nao.
- **Instalacao, deploy, publicacao**: nada foi instalado, nada foi publicado, o perfil nao foi tocado e o
  jogo nao foi aberto nesta rodada.
