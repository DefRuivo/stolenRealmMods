# AUT-4R2 — revisão independente do coletor AUT-4 (t_b8b9822e) — lente: EXECUÇÃO

Revisor: agente independente (não é autor) · tarefa `t_b8b9822e`, run 353 · 2026-10-05
Rodada **offline**: nenhum jogo aberto/encerrado, nenhum save tocado, nenhum probe instalado no
perfil do dono, nenhum build/deploy no perfil, nenhum commit/push/publicação. Tudo o que foi
executado rodou em **cópia isolada do repositório** (`$HERMES_KANBAN_WORKSPACE/sandbox`) com
`USERPROFILE`/`APPDATA`/`LOCALAPPDATA` redirecionados para pastas próprias.

Rodada 1 de revisão no registro (nenhum `changes_requested` anterior). A entrega afirmou
`AUT-4R` (segurança/contratos) e o handoff dizia 6 testes + 2 iscas; o disco tem **8 testes + 4
iscas**, i.e. houve correção **depois** do relatório AUT-4R. Por isso esta rodada **lidera pela
lente de EXECUÇÃO**: em vez de reler o relatório, rodei o coletor e as suítes em cópia isolada e
testei os contratos de honestidade com entradas adversariais.

## Estado exato que foi lido (sha256)

| artefato | sha256 |
|---|---|
| `tools/automacao/runtime/coletor.py` | `2f502e0d4ca45374f7d6a06f751254eb684e962d722ebb260e6324cee8959e83` |
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `3525c0e6fa17dae26e5742e44fd620710d18cb9177383a44474fe91d44cb048d` |
| `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` (repo) | `3c32f0269ae08811e9e997a2fc5ac7c8f10e40887330aa808725bde46003df46` |
| `docs/automacao/AUT-4-estado.json` **declara** para a DLL | `e8ee229b38fdc3d7f8800fe06606e197528ab7a112f439e2ae2665fbb47ba62d` |
| rebuild do MESMO fonte em sandbox | `c24c3e1a499caf959cbff6a3641808c103eeb77d80c62443679dbdd36df041d` |

Deriva do conjunto revisado durante a revisão: **`[]`** (nenhum dos arquivos medidos mudou enquanto
eu revisava). O `git status` do repo tem muitas modificações de outras frentes (BT/shrines/CIC) —
não foram tocadas por esta revisão.

## O que foi executado (exit real)

```
python roda_testes_runtime.py                 -> VERDE, 8/8, exit 0
python roda_testes_runtime.py --contra-prova  -> VERDE, 4/4 iscas reprovaram, exit 0
dotnet build -c Release --no-incremental -p:DeployToBepInEx=false   (cópia isolada) -> exit 0, 1 warning MSB3277
ilspycmd -t Aut4Probe.Aut4ProbePlugin <dll do repo>   -> guarda do gancho no IL: `Instancia?.Tick("gancho")`
python coletor.py --saida-probe <json adversariais>   -> exit 0 / CONFIRMADA   (ver A1)
```

O `AUT4Probe.csproj` não tem **nenhum** `<Target>` (checado por parse de XML antes de compilar), então
compilá-lo não instala nada; mesmo assim o build foi feito em cópia com `USERPROFILE`/`APPDATA`/
`LOCALAPPDATA` redirecionados. Perfil do dono intocado.

## Veredito por critério do aceite

| # | critério | veredito |
|---|---|---|
| 1 | probe lê objeto vivo (texto bruto+renderizado, ativo/visível, fonte/material/shader/keywords, cores, geometria, contexto, owners) na FONTE/BINÁRIO | **OK (fonte/binário)** — 18 chaves emitidas em `Leitura()`; IL confere com o fonte |
| 2 | PNG pela API do Unity (`ScreenCapture`) | **OK (fonte) / NÃO EXERCITADO** — o manifest registra `bytes`/`erro` por artefato, mas o driver não exige PNG presente (ver A1c) |
| 3 | navegação por handler real de UI (`Button.onClick.Invoke()` pelo rótulo; OCR só fallback) | **OK (fonte) / NÃO EXERCITADO** — exige tela com save → 2ª rodada |
| 4 | driver não depende do `Update` do plugin destruído | **OK (fonte+binário)** — PlayerLoop + `Instancia?.Tick`; o achado A3 da rodada anterior está endereçado |
| 5 | espera de estado + timeout no CAMINHO EXECUTÁVEL | **ACHADO A1** — a espera existe, mas a conclusão não depende dela |
| 6 | backup de log + manifest + restauração EXATA (inclusive arquivos criados) | **PARCIAL — ACHADO A5** (diretório pré-existente removido); arquivos e log: OK |
| 7 | controle negativo preferencialmente em perfil isolado | **OK (offline)** — o driver aceita `--perfil` isolado e o teste usa `tempdir`; em jogo NÃO EXERCITADO |
| 8 | aceite: prova reproduzível de leitura ida-e-volta | **ACHADO A6** — o probe AUT-4 não tem a prova de ida-e-volta (o CAP-1 tem) |
| 9 | aceite: detector que sabe dizer NÃO | **FALHA — A1/A2/A4** |
| 10 | aceite: sem acesso autorizado ⇒ incompleto, jamais dado fabricado | **FALHA — A1** |

## Achados (todos reproduzidos no disco, não por leitura de relatório)

### A1 — GRAVE — o driver confirma sem nenhuma evidência de que a rodada leu o jogo

`executar_rodada` monta `status=CONCLUIDO`/exit 0 olhando **só** o conteúdo de `aut4probe.json`;
`_esperar_estado` registra `log_ok`/`json_ok` mas **nenhum deles entra no veredito**. Pior: um
`aut4probe.json` **anterior à rodada** é consumido como se fosse desta rodada.

Reprodução (cópia isolada; porta de lançamento = stub que não escreve NADA):

```python
# out/aut4probe.json PRE-EXISTENTE (sessão 'SYNTHETIC-REVIEW-NOT-RUNTIME'), observação com campos completos
executar_rodada(plano, perfil_dir=perfil_vazio, out_dir=out, dll_probe=synthetic_dll,
                autorizado=True, jogo_disponivel=True, confirmacao='coleta',
                comando_lancamento=[sys.executable, '-c', 'pass'], timeout_s=1)
# -> status=CONCLUIDO, exit 0, estado={log_ok:False, json_ok:True}
```

Mesmo resultado pelo CLI (`--saida-probe <json>` → `exit 0 / status CONFIRMADA`) sem manifest, sem
prints, sem PNG, sem sessão da rodada. Isso é exatamente o caminho que o aceite proíbe ("caminho sem
acesso autorizado ao jogo retorna incompleto, jamais dados fabricados") e o desfecho que a
SUPERVISÃO chama de "sinal não é efeito".

**Correção mínima exigida:** derivar a decisão de três provas independentes — (a) a sessão da
evidência é a sessão DESTA rodada (id de sessão gerado pelo driver e injetado no `.cfg`, com o JSON
tendo de ser mais novo que o lançamento), (b) o `LogOutput.log` desta rodada contém o fim do
chainloader e a linha de vida do probe, (c) `prints` não vazio com arquivo existente e bytes>0.
Faltando qualquer uma ⇒ `NAO_EXERCITADO`/`INDETERMINADO`, exit ≠ 0.

### A2 — GRAVE — `campos_alvo` não governa o veredito; alvo não lido vira N/A e "fecha"

Com `alvos=['texto_renderizado']` e uma observação de objeto **inativo** (só `texto_bruto`), o
consolidador devolve **`CONFIRMADA` / exit 0**: o fallback declarado do inativo transforma o alvo em
`NAO_APLICAVEL` e a lacuna desaparece. Idem para `alvos=['shader_suportado']` (campo EXTRA: nunca é
lacuna por construção) e para um alvo **inexistente/typo** (`['field_typo']` → `CONFIRMADA`).
Consequência: para os casos que motivam o AUT-4 (texto/materials do RSTV) o critério de confirmação
é inalcançável — qualquer alvo pode ser silenciosamente descartado.

O teste `t_aut4_costura_probe.py` (l.84-93) **asserta** esse comportamento, i.e. a suíte está verde
onde o aceite pede vermelho. **Correção mínima:** alvo fora do schema ⇒ plano inválido; alvo alvo
AUSENTE/`NAO_APLICAVEL` ⇒ `INCOMPLETO` (o fallback é informação, nunca satisfação do critério).

### A3 — MÉDIO — procedência declarada no artefato é ignorada quando o chamador passa `runtime`

`consolidar_probe(..., procedencia='runtime')` sobre um JSON com `procedencia: fixture`,
`evidencia_runtime: false` e `rotulo_fixture` produziu `CONFIRMADA` com `evidencia_runtime: true`.
A auto-detecção existe, mas cede à intenção do chamador. **Correção mínima:** rótulo de fixture lido
do próprio artefato tem precedência (nunca consolidar como runtime).

### A4 — MÉDIO — `status`/`fase` do probe não entram no veredito

JSON com `status: ERRO`, `fase: erro` (ou `SEM_UI`, `ORCAMENTO_ESTOURADO`, `NAO_EXERCITADO`)
consolidou `CONFIRMADA`/exit 0. **Correção mínima:** estado terminal de falha do instrumento
rebaixa o resultado a `INCOMPLETO`/`ERRO`, exit ≠ 0.

### A5 — MÉDIO — rollback não é exato para DIRETÓRIOS

Com `BepInEx/plugins/AUT4Probe/` **pré-existente e vazio**, o rollback **removeu o diretório**
(`planejar_rollback` só compara arquivos; `_remover_dirs_vazios` apaga o que ficou vazio). O perfil
não volta ao estado anterior. **Correção mínima:** snapshot do estado de existência de diretórios
(não só arquivos) e não remover diretório que existia antes.

### A6 — MÉDIO — o aceite de "ida-e-volta" não tem instrumento no AUT-4

O CAP-1 (`scratch/cap1/CapProbe/CapProbePlugin.cs:1203-1214`) prova a leitura chamando
`Tooltip.ShowTooltip(<marcador>)` e lendo `Tooltip.Title.text` de volta (flag `DemoTooltip`). O
`AUT4ProbePlugin.cs` **não tem** chamada equivalente nem flag. Sem isso, "prova reproduzível de
leitura ida-e-volta" (critério do aceite) só existe se a rodada reusar o instrumento do CAP-1 —
o que precisa estar **declarado**, não implícito. **Correção mínima:** porta opt-in de
demo/marcador no probe (declarada como leitura, não como simulação) ou declarar formalmente que a
ida-e-volta vem do JSON do CAP-1 e ligar a evidência.

### A7 — INFORMATIVO — identidade do artefato e estado declarado estão desatualizados

1. `docs/automacao/AUT-4-estado.json` declara a DLL `e8ee229b…`, que não corresponde ao fonte atual
   (o binário do repo é `3c32f026…`) — e o rebuild do mesmo fonte deu um terceiro hash
   (`c24c3e1a…`): a DLL **não é reprodutível byte a byte** (esperado sem `-p:PathMap`, A9 da rodada
   anterior). Identidade do artefato = hash **declarado**, nunca "compila igual".
2. O mesmo estado declara 6 testes + 2 iscas; o disco tem **8 + 4**.
3. `AUT-4-preparacao.md` continua dizendo "6/6" e "2 iscas".

## O que NÃO foi exercitado (declarado, não é OK)

- Emissão real de campos em sessão viva, PNG do jogo, owners em sessão viva, navegação e rollback
  **em jogo** — tudo **NÃO EXERCITADO** (sem autorização de rodada; esta revisão é offline).
- O gate de autorização do `Aut4ProbePlugin` continua testado **estaticamente** (contrato por
  marcadores no fonte) e no **contrato do driver**; em execução, não.
- A suíte offline **não** cobre A1/A2/A4/A5 (ver "correção mínima" de cada um): hoje ela passa verde
  com os quatro defeitos presentes.

## Roteiro pendente para depois do conserto

Consertados A1–A6 e atualizado o estado (A7), a rodada runtime mínima continua sendo a descrita na
AUT-4R, e continua exigindo **autorização explícita do dono** para uma única frente (instalar o
probe + iniciar o jogo, sem save/combate; perfil isolado de preferência). Nada de hot-reload: é
probe novo.

## Evidência e reprodução

Arquivos brutos desta revisão (workspace da tarefa, `t_b8b9822e`):
`review-results.json` (suítes + 7 casos adversariais), `cli-adversarial.json` (CLI),
`review-build.json` (build), `reviewed-hashes.json` (hashes do estado lido). Scripts:
`review_aut4.py`, `build_review.py`. Para repetir: rodar os dois scripts com `python` dentro do
workspace (eles copiam o runtime para `sandbox/`, redirecionam `TMPDIR/TEMP/TMP`,
`USERPROFILE/APPDATA/LOCALAPPDATA` e substituem a porta de lançamento por stub — nenhum caminho
absoluto de Steam é usado).
