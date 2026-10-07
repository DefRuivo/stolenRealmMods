# CIC-5R — revisão independente da coleta integrada e do rollback do CIC-5 (`t_26a78c64`)

Revisor: agente independente (não é o autor do CIC-5). Rodada **OFFLINE**, 2026-10-05 ~20:00 BRT.
Escopo: revisar a preparação executável do coletor AUT-4 (`tools/automacao/runtime/**`) — **costura**
probe→coletor e **requisitos por campo-alvo**, e o **driver execução/rollback** — com **variantes
próprias em scratch**. Somente leitura em produto/probe; `cenarios/` lido só para confrontar o contrato.
Nenhum build, nenhum commit, nada em jogo. **Único arquivo escrito no repo:** este documento.

> Esta é a **2ª passada**. Os achados `R-1..R-9` de uma passada anterior **foram todos re-derivados
> aqui**, com execução real em cópia scratch (não repassados por confiança). `S-1..S-3` são **novos**.
> Onde a numeração de linha da passada anterior divergia, vale a **desta** revisão.

## 1. Estado medido no disco (hashes reais)

| artefato | sha256 (16 primeiros) | confere? |
|---|---|---|
| `tools/automacao/runtime/coletor.py` | `2f502e0d4ca45374` | = declarado no CIC-5 ✓ |
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `3525c0e6fa17dae2` | = declarado no CIC-5 ✓ |
| `.../AUT4Probe/bin/Release/AUT4Probe.dll` | `3c32f0269ae08811` | = CIC-5 ✓ · **≠ `AUT-4-estado.json` (`e8ee229b`)** |
| `.../roda_testes_runtime.py` | `769ec5cab2ba5ead` | — |
| `.../testes/t_aut4_execucao.py` | `b296e5aa68517ca5` | = CIC-5 ✓ |
| `.../testes/t_aut4_costura_probe.py` | `9a1781bd1ac7ebab` | = CIC-5 ✓ |
| `docs/automacao/AUT-4-estado.json` | `91bfe7bd739a4c96` | **STALE** (R-9) |
| `tools/automacao/cenarios/rstv.py` | `0f9b02f6678f2a01` | contrato confrontado (R-1) |
| `tools/automacao/cenarios/tooltips_shrines.py` | `c4e0a837af3e55d9` | contrato confrontado (R-1) |

Perfil do dono conferido **só por leitura**: `plugins/` **sem** `AUT4Probe` e **sem**
`com.gumatos.aut4probe.cfg` → o CIC-5 **não deixou resíduo** no perfil. HEAD `f526fe9`
(branch `ci-validate-test`).

## 2. Comandos exercitados (execução real, exit real)

Cópia de `tools/` em scratch (`snapshot/`); tudo roda sobre a cópia — **o repo não foi tocado**.

| comando | resultado real |
|---|---|
| `roda_testes_runtime.py` (cópia) | **VERDE, 8/8, exit 0** (confere com o pai) |
| `roda_testes_runtime.py --contra-prova` (cópia) | **VERDE, 4/4, exit 0** — mas **2 das 4** reprovam por **exceção**, não por assert (R-5) |
| `coletor.py --plano … --executar` (**sem** `--perfil`) | **exit 1, `TypeError` em `ntpath.abspath`** — não o `NAO_EXERCITADO`/exit 2 prometido (R-2) |
| minha banca `revisao_independente.py` (8 casos) | **8/8 repro confirmado, exit 0** — §6 |

## 3. Veredito por item

| # | item | veredito | prova |
|---|---|---|---|
| 1 | costura B1: `sessao`/`hash_fonte` do topo injetados por observação | **OK** | obs crua é RECUSADA; com `anexar_contexto` fecha `ok` |
| 2 | costura B2: os 5 campos extras atravessam | **PARCIAL** | atravessam ✓ — mas **nunca viram lacuna** mesmo declarados alvo (S-3) |
| 3 | B3: alvo por cenário + fallback inativo declarado | **PARCIAL** | inativo→`NAO_APLICAVEL` ✓; ativo sem rendered continua lacuna ✓; **só o 1º cenário/plano define alvos** (S-2) |
| 4 | gate default do driver: desautorizado não age | **OK** | exit 2, `efeitos_colaterais=[]`, nenhum arquivo, stub não executado |
| 5 | instalar/lançar/esperar/reverter por **artefato em disco** | **OK** | `argv` do stub em disco (`-applaunch`/AppID/`--doorstop-target-assembly …Preloader.dll`) |
| 6 | rollback EXATO (remove novo / restaura modificado) | **OK** | cfg+log pré-existentes restaurados **byte a byte**, inclusive em erro de lançamento e timeout |
| 7 | **atualidade = evidência DESTA rodada** | **REPROVADO** | JSON pré-existente (ou com `status=ERRO`) é consumido → `CONCLUIDO`/exit 0 com `log_ok=false` (**S-1**) |
| 8 | `hash_fonte` × identidade CIC-1/2/3 | **REPROVADO (bloqueio)** | R-1 |
| 9 | CLI `--executar` default honesto | **REPROVADO** | R-2 |
| 10 | espera de estado cobre `status=ERRO` do probe | **REPROVADO** | R-3 |
| 11 | encerra **só** o processo da rodada | **REPROVADO (risco)** | R-4 |
| 12 | runner de contra-prova não aceita crash como prova | **REPROVADO** | R-5 |
| 13 | probe **em sessão viva** (campos/PNG/owners/rollback reais) | **INDETERMINADO** | nada em jogo — **não aprovo runtime não exercitado** |

**Veredito global: NÃO APROVADO para a rodada runtime autorizada.** A camada offline (contrato, costura
B1/B2, gate default, rollback por bytes) está sólida e foi re-verificada por execução própria. O que
**não** fecha é (a) o caminho executável provar que a evidência é **desta** rodada e (b) a identidade de
hash. Bloqueadores: **R-1, R-2, R-3, R-4, R-5, S-1**. Backlog (não bloqueiam): **S-2, S-3**;
registro: **R-9**.

## 4. Achados bloqueadores

### S-1 — GRAVE (novo): o driver consome **saída pré-existente** e carimba `CONCLUIDO`
`executar_rodada` faz `os.makedirs(out_dir, exist_ok=True)` e depois lê `out_dir/aut4probe.json`
(`coletor.py` l.669) **sem exigir que o arquivo tenha nascido nesta rodada** e **sem exigir
`log_ok`/`json_ok` do `_esperar_estado`** (l.666-673): o `estado` é gravado no resultado, mas nunca é
condição de aceite.
Prova (meus casos 6 e 7 da banca): com um `aut4probe.json` deixado em `out_dir` **antes** da rodada e um
lançador real que **não produz log nem JSON**, o driver devolveu `exit 0` / `status=CONCLUIDO` com
`estado.log_ok=false`; o mesmo com o JSON antigo declarando `status=ERRO` (que virou `CONCLUIDO`).
O doc do CIC-5 e o `--out-dir "<OUT>"` da próxima rodada propõem justamente **reusar** a pasta. Isso fere
o aceite do ciclo ("resultado ligado aos bytes atuais, nao log velho; mudanca invalida aprovacoes
anteriores") — **não é hardening secundário**.
**Ação:** antes de lançar, **arquivar/remover** o `aut4probe.json` do `out_dir` e exigir
`estado.json_ok and estado.log_ok` (ou `sessao`/mtime coerentes com a rodada) para a consolidação falhar
em vez de carimbar verde.

### R-1 — GRAVE (integração): `hash_fonte` é sha da **DLL**; os adaptadores o comparam com `fonte_sha` (sha da **FONTE**)
O coletor deriva `hash_fonte` do **sha256 da DLL** (`derivar_config` l.442-443; `executar_rodada` l.617;
`provar_atualidade` l.529-543), e o cfg/probe repetem esse valor. Os adaptadores comparam esse **mesmo
campo** com `fonte_sha` da identidade:
- `cenarios/rstv.py` — `_hashes_obs` l.218-227 (alias `hash_fonte`→`fonte_sha`), `_checagem_hashes`
  l.230-245, `_evidencia_runtime` l.248-259, `_hash_divergente` l.262-266;
- `cenarios/tooltips_shrines.py` — `_cadeia_runtime` l.414-417: `hash_fonte != fonte_sha` ⇒
  `INDETERMINADO "observacao de OUTRA build"`.

Prova minha: com `obs.hash_fonte = dll_sha` e `identidade = {fonte_sha: SRC, dll_sha: DLL}`,
`rstv._hash_divergente(...) = True` e `rstv._evidencia_runtime(...) = False`, e
`tooltips_shrines._cadeia_runtime` devolve `INDETERMINADO`. Como `dll_sha ≠ fonte_sha` (build × fonte),
**toda** observação runtime legítima é marcada divergente — para sempre. O CIC-2 exige `fonte_sha` **E**
`dll_sha`, então a identidade distingue os dois: o contrato do campo **único** `hash_fonte` é **ambíguo**.
**Ação (uma das duas, com o contrato escrito):** (a) o coletor emite a identidade explícita (`dll_sha`
medido e, se preciso, `fonte_sha`); ou (b) os adaptadores confrontam `hash_fonte` com `dll_sha`.
Não corrigi: arquivos de outras frentes.

### R-2 — CLI `--executar` sem `--perfil` estoura **antes** do gate (exit 1, não 2)
`coletor.py` l.601-602 (`os.path.abspath(perfil_dir)` / `out_dir`) executam **antes** de
`decidir_autorizacao` (l.603). Repro real meu:
```
python tools/automacao/runtime/coletor.py --plano …/plano-exemplo.entrada.json --executar
  → TypeError: _path_normpath: path should be string, bytes or os.PathLike, not NoneType   (exit 1)
```
O doc do CIC-5 mostrou `--executar` (sem autorização) → `NAO_EXERCITADO`/exit 2, mas aquele repro passou
`--perfil`/`--out-dir`. Sem esses flags, a promessa "default não age → NAO_EXERCITADO" **quebra**. Não há
mutação (falha antes de tocar disco), mas o caminho executável não é honesto no default.
**Ação:** mover os `abspath` para **depois** do gate (ou validar args antes).

### R-3 — espera de estado ignora `status=ERRO` do probe e queima o teto inteiro
`_esperar_estado` (l.561-584) só para em `fase ∈ FASES_TERMINAIS` — e `"erro"` **está** nessa lista. Mas
o probe, no catch de `Tick` (`AUT4ProbePlugin.cs` l.256-262), grava `_res["status"]="ERRO"` **sem** setar
`_res["fase"]` (quem põe `fase="concluido"` é `Finalizar()`, l.336, que o catch **não** chama) → a `fase`
fica não-terminal. Medição minha: JSON `{fase:"lendo-objetos", status:"ERRO"}` → esperou **0,622 s de
0,6 s** (teto inteiro); controle com `fase:"erro"` → **0,018 s**. Efeito: erro do probe custa o timeout
inteiro **e** (com S-1) ainda pode ser lido como sucesso.
**Ação:** aceitar `status` terminal na espera (ou o probe setar `fase` no catch).

### R-4 — GRAVE (risco): o `finally` encerra o **lançador**, não o jogo; `encerrar_imagem` mata por imagem
`executar_rodada` lança `[steam, "-applaunch", …]`; no `finally` (l.696-713) faz `proc.terminate()` no
**Popen** = `steam.exe`, não no jogo (no Windows o jogo é processo à parte, que recebe o `--doorstop`).
Prova minha: stub-lançador real que faz `Popen(..., creationflags=DETACHED_PROCESS)` e sai → **depois** de
`executar_rodada` retornar, o driver encerrou o Popen e o **filho continuou vivo** (`vivo=True`). O Steam
real **não** foi lançado; o que está provado é o **código**. O `encerrar_imagem` usa
`taskkill /F /IM <imagem>`, que mata **todas** as instâncias da imagem — inclusive a que o dono já tinha
aberta. O default (não fechar) e o "nunca contra o stub" estão **corretos**; o comentário "encerra SÓ a
instância que a rotina lançou" é **falso** para o caminho real.
**Ação:** documentar `encerrar_imagem` como inseguro sem identidade de PID do jogo (capturar a árvore de
processos do lançador) e nunca passá-lo numa máquina com o jogo do dono aberto.

### R-5 — o runner de contra-prova aceita **qualquer** `exit==1`, inclusive crash
`roda_testes_runtime.py` l.71-74 marca `PROVA OK` quando `exit==1`; o arcabouço converte **exceção
inesperada** em exit 1 também. Na **minha própria** execução do `--contra-prova`, **2 das 4** iscas
reprovaram com `RESULTADO|REPROVOU|…|excecao inesperada` (`cp_aut4_isca_ausente_ok`,
`cp_aut5_isca_topo_sem_hash_ok`): o rótulo **não distingue crash de reprovação intencional**, então
metade do controle negativo não prova nada. **Ação:** exigir que a isca reprove por `Falhou`/assert (ou
declarar a exceção esperada) e rejeitar `excecao inesperada`.

## 5. Backlog (não bloqueiam esta rodada)

- **S-2 (novo) — requisitos por campo só do 1º cenário/plano.** `_alvos_do_plano` (l.270-279) lê
  `campos_alvo` do topo **ou** de `cenarios[0]`, e **todos** os cenários passam a usar esses alvos. Prova
  minha: plano `[{campos_alvo:[texto_bruto]}, {campos_alvo:[texto_renderizado]}]` + observação ativa com
  `texto_renderizado=null` saiu **`CONFIRMADA`/exit 0** (o 2º cenário foi ignorado). Com 1 cenário
  (rodada mínima) não bloqueia; para "requisitos por campo" como contrato, bloqueia.
- **S-3 (novo) — campo extra nunca vira lacuna.** `normalizar_observacao` l.192 só acrescenta lacuna para
  `campo in CAMPOS`; um extra declarado alvo (ex.: `shader_suportado`, que a B2 trouxe justamente por
  design/material) ausente sai `ok=True`, `lacunas=[]` — alvo declarado silenciosamente não cobrado.
  Prova minha: `alvos=["shader_suportado"]` com o campo nulo → `ok=true`.
- **R-9 (registro; pai atualiza): `docs/automacao/AUT-4-estado.json` STALE.** Declara
  `probe_dll_sha256 = e8ee229b…` (a DLL em disco é `3c32f026…`) e lista **6** testes / **2** iscas,
  enquanto o disco tem **8** e **4**. Fora do escopo de escrita do revisor.
- Manifest do próprio `aut4probe.json` é auto-referente → mitigado por `auto_referente`/`autoritativo` em
  `provar_atualidade`; sem cascata.

## 6. Minhas contra-provas (8/8 confirmadas, sem jogo)

Banca: `revisao_independente.py` + medições diretas, sobre cópia scratch de `tools/`; resultado em
`revisao-resultados.json` e evidências `rollback-erro.json`, `stale-resultado.json`,
`erro-resultado.json`, `cli-default.txt` (Hermes scratch `…/workspaces/t_26a78c64/`).

1. costura topo→obs + os 5 extras atravessam (`true`);
2. extra declarado alvo e ausente aceito (`ok=true, lacunas=[]`) — **S-3**;
3. `--executar` sem `--perfil` → exit 1 `TypeError` — **R-2**;
4. `hash_fonte`(DLL) × `fonte_sha`(fonte) divergem (`True`) — **R-1**;
5. rollback em erro de lançamento devolve DLL/cfg/log **byte a byte** (`bytes_restaurados=true`);
6. saída pré-existente, sem log desta rodada → **exit 0 / CONCLUIDO** com `log_ok=false` — **S-1**;
7. idem com `status=ERRO` no JSON → **exit 0 / CONCLUIDO** — **S-1**;
8. campos do 2º cenário ignorados → `CONFIRMADA` — **S-2**.

Extras: espera com `status=ERRO` → 0,622 s de 0,6 s (**R-3**); filho desanexado sobrevive ao `finally`
(**R-4**); `tooltips_shrines._cadeia_runtime` marca `INDETERMINADO` para observação legítima (**R-1**).

## 7. Lacunas declaradas (NÃO exercitadas — e não viram OK)

Runtime em jogo: emissão real dos 18 campos, PNG pela API do Unity, `owners` vivos, rollback contra o
perfil **real**, `encerrar_imagem`, lançamento real por Steam. Cobertura desta revisão: **offline**
(suíte + contra-prova + banca própria) e leitura de fonte. O snapshot de rollback cobre 3 caminhos do
perfil (`PROBE_REL`, `CFG_REL`, `LOG_REL`): recurso extra que o probe venha a criar no perfil **não** é
restaurado — aceitável hoje (o probe escreve em `OutDir`), mas fica registrado.

## 8. Menor próximo passo executável (requer autorização do dono)

Depois de **S-1 + R-1 + R-2** (mínimo para a rodada não dar verde falso), a rodada mínima é: instalar o
probe num **perfil isolado**, lançar pelos **argumentos de doorstop**
(`steam -applaunch 1330000 --doorstop-enabled true --doorstop-target-assembly <preloader>`),
`Navegar=false`, esperar **estado de UI com texto renderizado** (a tela de loading/menu, onde o CAP-1 já
provou o tooltip "Barrels", serve), deixar finalizar o `aut4probe.json` e restaurar/remover exato.
**Não abre save, não vai à árvore de skills, não combate.** Não autorizo a rodada aqui: é decisão do dono.

## 9. Limites desta revisão

Nada em jogo; não recompilei o probe nesta passada (a checagem de `ReferenceEquals`/`SetPlayerLoop` no
**fonte** está coberta por `t_aut4_probe_contrato.py`, que roda verde na cópia, e a DLL `3c32f026` confere
com o sha declarado pelo CIC-5); não editei produto, probe, `ciclo/`, `cenarios/`, `decisao/`, board,
`KANBAN.md`, nem o perfil. **Único arquivo escrito no repo:** este parecer.

HEAD `f526fe9` (branch `ci-validate-test`) · rodada offline `2026-10-05`, executada sobre cópia scratch
de `tools/`.
