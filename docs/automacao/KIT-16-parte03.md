# KIT-16 — parte 03: harness entregue e PROVA OFFLINE do mecanismo

run 700 · 2026-10-10 · continua de `KIT-16-parte02.md`

## A. ARTEFATOS NOVOS (nenhum arquivo pre-existente sobrescrito)

| caminho | bytes | papel |
|---|---|---|
| `scratch/kit/kit16-save-isolado.sh` | 22.879 | harness: `status`/`preparar`/`verificar`/`restaurar`/`run`/`fixture`/`limpar` |
| `scratch/kit/kit16-junction.ps1` | 2.379 | junction NTFS: `state`/`create`/`remove` (remove com `RemoveDirectoryW` — so o link) |
| `scratch/kit/kit16-controle-negativo.sh` | 4.380 | controle negativo do harness (3 controles) |
| `scratch/kit/KIT-16-run700/dump/Assembly-CSharp.decompiled.cs` | 17.815.971 | varredura da Fase 1 (ilspycmd, exit 0) |

Reuso (nao reimplementado): `tree_snapshot.py` (sha256 por arquivo), `front-unica.sh`
(frente unica), `runtime-isolado.sh` (BepInEx isolado do KIT-03) e `cp -a`/`mv`
(rename no mesmo volume).

### A.1 Por que um helper PowerShell separado (e por que nao `rm -rf`)

`rm -rf` do MSYS e `Remove-Item -Recurse` do PowerShell 5.1 **seguem** o junction e
apagam o CONTEUDO DO ALVO (exatamente o dado descartavel que queremos preservar
para medir). O helper remove o link com `RemoveDirectoryW` (kernel32), que
**remove so o reparse point**. Verificado no controle NC-A: depois do `remove`, o
alvo continua existindo (`[[ -d "$alvo" ]]` = SIM).

## B. PROVA OFFLINE DO MECANISMO (executada, com resultado real)

Ciclo completo em FIXTURE (diretorio de teste — o perfil/save do DONO nao foi
tocado nesta prova):

    KIT16_FIXTURE=1 REAL_DIR=.../fixture-dono/Stolen Realm ISO_ROOT=.../fixture-iso \
      EVID_DIR=.../fixture-evid bash kit16-save-isolado.sh fixture     # exit 0

Saida real (resumida, exit 0):

    1/5 snapshot de CONTEUDO ... manifesto sha256=db3169e1c0ca4f567907d66c5be65e68236740e4576381864c487f1b38fd368e
    2/5 copia descartavel ... arquivos na copia: 3
    3/5 (fixture: registro real nao e tocado)
    4/5 rename do diretorio REAL -> .../Stolen Realm.kit16-real
    5/5 junction ... Junction -> ...\fixture-iso\dados-do-jogo
    OK: escrita no caminho REAL apareceu na COPIA ISOLADA (junction transparente)
    DIFF: novos [Character99.json, CrossPromo/c.txt]; alterados [GlobalSaveData.json]
    OK: diretorio REAL restaurado BYTE A BYTE identico ao snapshot antes
    FIXTURE: OK

Prova de transparencia do junction com PROCESSO NATIVO: `printf > jt2/novo.txt` pelo
caminho do link apareceu em `jt_alvo/novo.txt` (teste do helper) e, no ciclo do
harness, `.kit16-prova-escrita.txt` escrita no caminho REAL foi lida de volta na
copia isolada. Isso e I/O de sistema de arquivos real, nao simulacao.

## C. CONTROLE NEGATIVO (executado — `scratch/kit/kit16-controle-negativo.sh`, exit 0)

    NC-A junction ausente        -> `verificar` exit=1, "nao e junction"       OK
    NC-B conteudo do dono mexido -> `restaurar` exit=1, "DIVERGE do snapshot"  OK
    NC-C ciclo limpo (positivo)  -> `fixture` exit=0, "FIXTURE: OK"            OK
    CONTROLE NEGATIVO: OK (3/3), exit 0

Interpretacao: o harness **reprova** quando o isolamento nao esta no lugar
(NC-A) e quando o conteudo devolvido ao caminho real nao bate com o snapshot
(NC-B); e o verde do NC-C nao e tautologico porque o mesmo comparador falha em
NC-B. Evidencias: `scratch/kit/KIT-16-run700/controle-negativo/nc-{a,b,c}/`.

## D. O QUE AINDA NAO FOI EXERCITADO NESTE PONTO

- **Rodada com o JOGO de verdade** sob o junction (proxima fase): e o que prova
  que o jogo respeita o redirecionamento. Enquanto isso nao rodar, o status e
  `NAO_EXERCITADO` para o jogo — a prova acima e do MECANISMO, nao do jogo.
- **Registro (PlayerPrefs)**: o export/delete/import esta implementado e sera
  exercitado na rodada real; nesta fase (fixture) foi desligado de proposito
  (`FIXTURE=1` nao toca o ramo real do registro).
- **BepInEx isolado**: fica a cargo do `runtime-isolado.sh` (KIT-03), chamado pelo
  `run` deste harness; nao foi exercitado nesta fase offline.

## E. RISCO RESIDUAL REGISTRADO (Steam Cloud)

`localconfig.vdf` (userdata 37602317) mostra o app 1330000 com
`"cloud": {"last_sync_state": "synchronized"}` — Cloud ativo. Medidas: (1) o
snapshot/restauracao inclui `steam_autocloud.vdf`, portanto o estado local volta
identico; (2) o diff da area isolada **mede** exatamente quais arquivos a rodada
tocou; (3) o que o Cloud tiver recebido durante a janela fica **declarado** no
fechamento. Nao ha como desligar o Cloud sem editar a configuracao do Steam do
dono — o que este cartao nao faz.
