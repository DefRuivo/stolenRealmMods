# COR-AUT4R — revisão independente do fechamento dos 6 achados da AUT-4R2

Objeto: **COR-AUT4** (`t_b62359c3`, DONE 06/10 14:05) — fechamento de A1/A2 (graves), A3/A4/A5/A6 (médios)
e A7 (documental) da revisão independente **AUT-4R2** (`docs/automacao/AUT-4R2-revisao.md`), na frente
**AUT-4** "Coleta runtime reutilizável e segura por objetos Unity" (`t_b8b9822e`, BLOCKED por gate humano
de autorização de rodada runtime).

Revisor: agente independente (`default`, tarefa `t_d99241fd`, run 428) — **não é o autor**.
Data da revisão: **2026-10-06 14:20→14:43 (-03:00)**.
HEAD do repo no momento da leitura: `f526fe9` (98 entradas de `git status --porcelain` de outras frentes;
nenhuma tocada por esta revisão).

Escopo executado: **só leitura de bytes + execução OFFLINE**. Nenhum jogo aberto/encerrado, nenhum save
tocado, nenhum probe instalado, nenhum deploy no perfil do dono, nenhum build no repo, nenhum commit/push,
nenhum arquivo de produto editado. Toda execução rodou sobre **cópia fora do repo**
(`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4r/`), com os defeitos plantados em cópias
descartáveis. Meus únicos arquivos no repo: este parecer + `docs/automacao/COR-AUT4R-evidencias/`.

Regras lidas antes de começar: `docs/SUPERVISAO.md` (sha256 `88620fc7…`, 279 linhas) e `.hermes.md`
(sha256 `dd57b6da…`, 43 linhas) — ambos listados em `COR-AUT4R-evidencias/hashes.txt`.

---

## 0. Resumo do veredito

| item | veredito | uma linha |
|---|---|---|
| A1 (grave) | **ACHADO (baixo) — parcial** | as três provas existem e reprovam como deviam (a/b medidas); a prova **(c) não é datada**: um PNG de rodada ANTERIOR no `out_dir` reusado satisfaz `prints_ok` e a rodada fecha `CONCLUIDO`/exit 0 |
| A2 (grave) | **ACHADO (grave) — reaberto** | o alvo não lido só vira lacuna quando o valor é `null` (forma da FIXTURE). O artefato REAL do probe emite **`""`** (`GetParsedText()` → `string.Empty`, medido no `lib/Unity.TextMeshPro.dll` do jogo) e `""` conta como **PRESENTE** ⇒ `CONFIRMADA`/`CONCLUIDO` com a lacuna escondida |
| A3 (médio) | **ACHADO (médio)** | só `procedencia: fixture` **ou** (`evidencia_runtime:false` **E** `rotulo_fixture`) tem precedência; `evidencia_runtime:false` **sozinho** é ignorado, vira runtime e confirma |
| A4 (médio) | **OK (com prova)** | 4 estados terminais + instrumento mudo rebaixam, exit ≠ 0; isca reprova e o defeito plantado derruba a suíte |
| A5 (médio) | **OK (com prova)** | diretório pré-existente (inclusive vazio) sobrevive ao rollback; isca reprova e o defeito plantado derruba a suíte |
| A6 (médio) | **ACHADO (médio) — parcial** | a porta opt-in **existe** no fonte E no binário (o driver exercita o probe de hoje); mas a exigência aceita `{"conferiu": true}` **sem** o marcador gerado pelo driver ⇒ `CONCLUIDO`/exit 0 |
| A7 (documental) | **OK (com prova)** | estado/doc casam com o disco (trava verde, hashes declarados == medidos, listas == disco, `9/9` e `11 iscas` reais); `AUT-3-*` do repo real **não** foram sobrescritos (mtime/hash de 05/10 15:47–15:49) |
| Bancada offline (autor) | **INDETERMINADO** | não re-executada (6 builds Release); caminho de escrita e de build conferido no código — ver §5 |

**Veredito final: CHANGES REQUESTED** — 4 correções exatas na §6. Nada em jogo foi exercitado e isso
segue NÃO EXERCITADO (não é OK) — §5.

---

## 1. Estado lido (sha256 que EU medi nos bytes do disco)

Arquivos do produto e réguas (medição completa em `COR-AUT4R-evidencias/hashes.txt`):

| arquivo | sha256 medido | mtime |
|---|---|---|
| `tools/automacao/runtime/coletor.py` | `c7032285e2e9828d8b3c3c9ffd41420f3a0ccebe0f75440a0b67533135f8ddae` | 06/10 13:59:22 |
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `5a51abaa439b90263e3b202e01a0b2b3b343fabc8cb71c9de8b3ac97b343bdd3` | 06/10 13:53:18 |
| `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` | `fd774259b5e8813f2f3b29e2ff805f12cb0cdab4c277116fcc8bbb7e7e3bffdd` | 06/10 13:57:50 |
| `tools/automacao/runtime/AUT4Probe/Json.cs` | `ae30a1ac059bcf62067047926c13bf43079b30552073540a2f5654551b6b32c6` | 05/10 15:41:13 |
| `tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj` | `347770d091a6a173cbebb988fb30d2a7a73df4d64e316033812e4220869057f4` | 05/10 15:52:08 |
| `tools/automacao/runtime/roda_testes_runtime.py` | `769ec5cab2ba5eadbc69535fe85588c618c74727f9625a31fa50fa191ab81f59` | 05/10 15:52:21 |
| `docs/automacao/COR-AUT4-entrega.md` | `02187dae05a7403b1c7eb38962d65a2891277689512a988bb888ff36a44532f0` | 06/10 14:04:30 |
| `docs/automacao/AUT-4-estado.json` | `fbcc44e21aefa8fb3fbe4702709baf4fc62fc1f2620eabd37970c6f26fe47c31` | 06/10 13:59:34 |
| `docs/automacao/AUT-4-preparacao.md` | ver `hashes.txt` | 06/10 13:54 |
| `docs/automacao/AUT-4R2-revisao.md` (régua que reprovou) | `2cdf07abd58d51db722bbe796beae183af6220148aceedcaaa855fc0a74d1fdf` | 05/10 19:55:14 |
| `docs/automacao/AUT-4R-revisao.md` | `c78c4bc1893ea9498f246652ed18da414bdb2745f32e43ed2009dd1ca3c4e4b3` | 05/10 17:59:41 |
| `docs/automacao/CIC-5R-revisao.md` | `12af8522f8d9780214ec2701ad184d486e0cee19ff13ef7d0252fa08ae1a3cfe` | 05/10 20:14:26 |
| `docs/SUPERVISAO.md` | `88620fc7f35db0091e10d86626475f7a53cba25d05b1f6139b14b69ee254d9a9` | 02/10 17:34:50 |
| `lib/Unity.TextMeshPro.dll` (jogo, para o §4) | ver `hashes.txt` | — |

Os três hashes que o autor declara em `COR-AUT4-entrega.md` (coletor `c7032285…`, fonte do probe `5a51abaa…`,
DLL `fd774259…`) **conferem byte a byte** com o que eu medi, e batem com o declarado em
`AUT-4-estado.json` (`probe_fonte_sha256` / `probe_dll_sha256`). Deriva durante a revisão: **`[]`** —
nenhum byte do conjunto medido mudou enquanto eu revisava.

Os 9 testes, as 11 iscas, as 4 fixtures e os 3 docs `AUT-3-*` do repo real seguem intocados (mtime de
05/10 15:47–15:49; hashes em `hashes.txt`).

---

## 2. Comandos exatos + saída literal + exit code

Cópia usada (bytes idênticos ao repo, conferidos por sha256 antes de rodar):
`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4r/copia/`
(só `tools/testes/`, `tools/automacao/runtime/`, `tools/automacao/offline/` e
`docs/automacao/AUT-4-estado.json` + `AUT-4-preparacao.md`).

```
$ cd <copia> && python tools/automacao/runtime/roda_testes_runtime.py
==========================================================================
 AUT-4 runtime — suite offline
==========================================================================
[PASSOU] testes\t_aut4_autorizacao.py
[PASSOU] testes\t_aut4_controle_negativo.py
[PASSOU] testes\t_aut4_costura_probe.py
[PASSOU] testes\t_aut4_estado_docs.py
[PASSOU] testes\t_aut4_execucao.py
[PASSOU] testes\t_aut4_manifest_rollback.py
[PASSOU] testes\t_aut4_observacao.py
[PASSOU] testes\t_aut4_plano.py
[PASSOU] testes\t_aut4_probe_contrato.py
==========================================================================
 VEREDITO: VERDE (exit 0) — 9 teste(s)
EXIT=0
```

```
$ cd <copia> && python tools/automacao/runtime/roda_testes_runtime.py --contra-prova
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut4_isca_ausente_ok.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut4_isca_coleta_sem_autorizacao.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_alvo_fora_do_schema.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_alvo_nao_lido_ok.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_dir_pre_existente_removido.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_procedencia_do_chamador.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_sem_autorizacao_executa.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_sem_prova_execucao.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_sem_prova_ida_volta.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_status_erro_confirma.py
[PROVA OK (reprovou como devia)] testes\contra-prova\cp_aut5_isca_topo_sem_hash_ok.py
==========================================================================
 VEREDITO: VERDE (exit 0) — 11 teste(s)
EXIT=0
```

Saídas literais completas (inclusive os `RESULTADO|REPROVOU|…` de cada isca):
`COR-AUT4R-evidencias/suite-literal.log` e `COR-AUT4R-evidencias/contra-prova-literal.log`.

**Contra-prova de verdade (defeito plantado por MIM, nos bytes atuais, em cópia descartável).**
Para cada achado revertí a correção correspondente no `coletor.py` da cópia e medi
(`COR-AUT4R-evidencias/planta_defeitos.py`, log `planta_defeitos.log` e `planta_defeitos_suite.log`):

```
ACHADO A1  isca cp_aut5_isca_sem_prova_execucao.py        exit=0  PASSOU   -> runner --contra-prova: VERMELHO (exit 1)
           suite: t_aut4_execucao REPROVOU "A1/E: rodada que NAO escreveu nada NAO pode dar exit 0"
ACHADO A2  isca cp_aut5_isca_alvo_nao_lido_ok.py          exit=0  PASSOU   -> VERMELHO (exit 1)
           isca cp_aut5_isca_alvo_fora_do_schema.py       exit=0  PASSOU   -> VERMELHO (exit 1)
           suite: t_aut4_costura_probe "A2: alvo NAO_APLICAVEL (nao lido) TEM de contar como lacuna"
                  t_aut4_plano "caso invalido 'campos_alvo_typo' foi ACEITO pelo validador"
                  t_aut4_execucao "A2/I: objeto inativo com alvo nao lido NAO pode consolidar CONFIRMADA"
                  (+ t_aut4_controle_negativo e t_aut4_observacao)
ACHADO A3  isca cp_aut5_isca_procedencia_do_chamador.py   exit=0  PASSOU   -> VERMELHO (exit 1)
           suite: t_aut4_costura_probe "fixture rotulada tem de sair FIXTURE, nunca runtime"
ACHADO A4  isca cp_aut5_isca_status_erro_confirma.py      exit=0  PASSOU   -> VERMELHO (exit 1)
           suite: t_aut4_costura_probe "A4: probe ERRO/erro nao pode consolidar CONFIRMADA"
ACHADO A5  isca cp_aut5_isca_dir_pre_existente_removido.py exit=0 PASSOU   -> VERMELHO (exit 1)
           suite: t_aut4_execucao "A5/L: pasta do probe PRE-EXISTENTE nao pode ser removida no rollback"
ACHADO A6  isca cp_aut5_isca_sem_prova_ida_volta.py       exit=0  PASSOU   -> VERMELHO (exit 1)
           suite: t_aut4_execucao "A6/J: sem a prova de ida-e-volta o driver NAO confirma"
```

Leitura: **nenhuma isca é decorativa** — tirar a correção faz a isca PASSAR e o runner ficar VERMELHO,
e a suíte (que prende o comportamento correto) também cai. Vermelho→verde está medido, por mim.

Provas de contexto do probe (o driver exercita o probe que existe HOJE):

```
$ ilspycmd -t Aut4Probe.Aut4ProbePlugin tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll
  -> 1484 linhas; o BINÁRIO contém: Config.Bind("Geral","Sessao",…), _sessao = _sessaoCfg.Value ?: carimbo,
     Config.Bind("Geral","DemostrarTooltip", false, …), _demostrar.Value -> DemostrarIdaEVolta(),
     _res["ida_e_volta"] = {… "conferiu" …}, status "NAO_EXERCITADO"/"SEM_UI"/"ORCAMENTO_ESTOURADO"/"CONCLUIDO"
     (dump: COR-AUT4R-evidencias/ilspy-AUT4ProbePlugin.cs)

$ grep -n "Chainloader startup complete" \
    "$APPDATA/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log"
88:[Message:   BepInEx] Chainloader startup complete        # a string que o driver exige EXISTE no log real
$ grep -c "AUT4 PROBE" <mesmo log>  -> 0                    # o probe nunca rodou no perfil do dono
```

---

## 3. Veredito por item (A1–A7)

### A1 — GRAVE — **ACHADO (baixo) — parcial**

O que se afirmou: três provas (sessão do driver no `.cfg` + JSON mais novo que o lançamento; log da rodada
com fim do chainloader E linha de vida do probe; prints existentes com bytes>0); faltando qualquer uma ⇒
`NAO_EXERCITADO`/`INCOMPLETO`, exit ≠ 0.

**OK com prova, para (a) e (b):** `sessao_da_rodada()` gera `AUT4-<carimbo>-<uuid>` (visto:
`AUT4-20261006-143955-d942a75a`), entra no `.cfg` como `Sessao` e a evidência tem de trazê-la de volta
(`sessao_confere`); `json_mais_novo` compara mtime × `lancamento_epoca`; o driver **apaga** o
`LogOutput.log` antes de lançar e exige `Chainloader startup complete` **e** `"AUT4 PROBE:"` — a segunda
string é emitida pela própria fonte do probe (21 ocorrências; `Marco` → `Logger.LogInfo` → `LogOutput.log`)
e existe no log real do dono em produção. Faltas ⇒ exit 2 (`NAO_EXERCITADO`) ou exit 1 (`INDETERMINADO`),
medido nas iscas E/F/G/H e pela planta A1.

**ACHADO A1-c (a prova (c) não é datada).** `provas_de_execucao()` aceita qualquer arquivo existente com
`bytes>0` no caminho listado. O `out_dir` é **reusado por desenho** (o próprio driver escreve
`cfg-instalado.cfg`, `lancamento.txt`, `aut4probe-consumido.json` lá e não limpa nada). Um PNG de uma
rodada ANTERIOR, no mesmo `out_dir`, faz `prints_ok=True` mesmo que a rodada de hoje **não** tenha
produzido imagem. Repro literal (`adversarial_aut4r.log`, sonda S1):

```
rodada com PNG VELHO no out_dir : status=CONCLUIDO exit=0
   prints=[{'arquivo': '…/out-s1-velho/01-ui.png', 'existe': True, 'bytes': 108}]
CONTROLE out_dir novo (sem PNG) : status=INDETERMINADO exit=1
   prints=[{'arquivo': '…/out-s1-novo/01-ui.png', 'existe': False, 'bytes': 0}]
```

Controle negativo: com out_dir novo, a MESMA rodada cai para `INDETERMINADO`/exit 1. Ou seja, o que
distingue os dois desfechos é o arquivo velho, não a execução.

### A2 — GRAVE — **ACHADO (grave) — reaberto**

O que se afirmou: `campos_alvo` governa (alvo não lido = lacuna ⇒ `INCOMPLETO`; alvo fora do schema ⇒
`PlanoInvalido`).

**O que está de pé:** `validar_alvos()` recusa alvo fora do schema (medido: CLI `--saida-probe` com
`campos_alvo=["field_typo"]` → `"status": "PLANO_INVALIDO"`, `EXIT=2`), e a lacuna por alvo
`AUSENTE`/`NAO_APLICAVEL` funciona — para o valor `null`. A planta A2 derruba 5 testes, o que mostra que a
correção existe.

**Onde cai:** `coletor._estado_do_campo()` (l.191–196) classifica como `AUSENTE` **apenas** `None` e as 7
strings de `AUSENTES`; **string vazia `""` é `PRESENTE`** (e `[]`/`{}` também). O artefato REAL do probe
não emite `null` no caso que motivou o A2 — emite `""`:

```
$ ilspycmd -t TMPro.TMP_Text lib/Unity.TextMeshPro.dll      (COR-AUT4R-evidencias/tmp-getparsedtext.txt)
public virtual string GetParsedText() {
    if (m_textInfo == null) { return string.Empty; }        // "" — nunca null
    … return new string(array);                             // "" quando characterCount == 0
}
```

e o probe faz `"texto_renderizado", Trunc(Seguro(() => t.GetParsedText()) as string, 600)`, onde
`Trunc` só devolve `null` para **entrada** `null` (`if (s == null) return null;`). Logo, para o objeto com
o mesh não gerado (o caso `NAO_APLICAVEL` do A2), o artefato traz `texto_renderizado: ""`; `""` é
`PRESENTE`, não entra em `lacunas`, e o ramo do fallback inativo nem dispara (ele exige
`estado == "AUSENTE"`). A fixture `probe-saida-exemplo.entrada.json` codifica `null` — **é por isso que a
suíte fica verde**.

Repro literal, caminho completo `executar_rodada` (`adversarial_vazio.log`, sonda V1):

```
V1   artefato REAL (texto_renderizado='') : rodada=CONCLUIDO exit=0 consolidado=CONFIRMADA lacunas=[]
V1c  CONTROLE (texto_renderizado=null, forma da fixture): rodada=INCOMPLETO exit=1
                                                        consolidado=INCOMPLETO lacunas=['texto_renderizado']
```

Controle negativo: trocar `""` por `null` (a forma da fixture) na MESMA rodada faz a lacuna reaparecer.
Além do caso central, contêineres vazios também passam por "lidos":

```
V(owners)   valor=[] -> estado=PRESENTE lacunas=[] ok=True
V(keywords) valor={} -> estado=PRESENTE lacunas=[] ok=True
V(cores)    valor={} -> estado=PRESENTE lacunas=[] ok=True
```

**Observação secundária (mesmo item, sem falso-OK):** o alvo inválido só é recusado **tarde** no caminho
executável. `executar_rodada` **não** chama `validar_plano`; com `campos_alvo=["field_typo"]` a rodada
instala o probe, escreve o `.cfg` e **lança** antes de falhar:

```
executar_rodada com campos_alvo=['field_typo'] -> status=ERRO exit=1
   motivo='PlanoInvalido: campos_alvo fora do schema: field_typo (validos: objeto, caminho, …)'
   passos executados: 6 | lancamento: True
   efeitos no perfil (rollback): ['BepInEx\\LogOutput.log','BepInEx\\config\\com.gumatos.aut4probe.cfg',
                                  'BepInEx\\plugins\\AUT4Probe\\AUT4Probe.dll']  modificados=[]
```

Não é falso-OK (exit ≠ 0, rollback correto), mas o plano inválido deveria barrar antes de tocar o perfil —
e sai `ERRO`/exit 1, não `PLANO_INVALIDO`/exit 2 como no caminho CLI.

### A3 — MÉDIO — **ACHADO (médio)**

O que se afirmou: o rótulo do artefato tem precedência sobre a procedência declarada.

**O que está de pé:** `procedencia: fixture` no artefato vence o chamador ⇒ `FIXTURE`/exit 2 (isca
`cp_aut5_isca_procedencia_do_chamador` reprova; planta A3 derruba `t_aut4_costura_probe`).

**Onde cai:** a precedência é reconhecida em **duas** formas — `declarada == "fixture"` **ou**
(`evidencia_runtime is False` **E** `bool(rotulo)`). O artefato que se declara **`evidencia_runtime: false`
sem `rotulo_fixture`** (e sem `procedencia`) cai no `else`: a procedência vira `runtime` e o próprio campo
declarado é **invertido** para `true` no resultado. Repro literal (`adversarial_aut4r.log`, sonda S3):

```
artefato declara evidencia_runtime=false -> status=CONFIRMADA exit=0 evidencia_runtime=True
```

(entrada: artefato sem `procedencia`/`rotulo_fixture`, com `evidencia_runtime: false`, sessão+hash no topo,
`status: CONCLUIDO` e a observação ativa com todos os alvos lidos). O artefato diz "isto NÃO é evidência de
runtime" e o driver publica `evidencia_runtime: true` + `CONFIRMADA`.

### A4 — MÉDIO — **OK (com prova)**

`consolidar_probe` rebaixa quando `status ∈ {NAO_EXERCITADO, SEM_UI, ERRO, ORCAMENTO_ESTOURADO}` ou
`fase ∈ {nao-exercitado, sem-ui/sem_ui, erro, orcamento-estourado}` (⇒ `ERRO` se o status for `ERRO`,
senão `INCOMPLETO`, exit 1) e **também** quando o instrumento não declara status nenhum
("silêncio não é aprovação"). Medido: a suíte verde traz os 4 estados + instrumento mudo; a planta A4 faz a
isca `cp_aut5_isca_status_erro_confirma` PASSAR (`exit=0`) e o runner/suíte ficarem VERMELHOS. O probe
real (fonte e binário) emite exatamente esses status (`NAO_EXERCITADO`/`SEM_UI`/`ORCAMENTO_ESTOURADO`/
`CONCLUIDO`, decompilado no `ilspy-AUT4ProbePlugin.cs`). Sem ressalva.

### A5 — MÉDIO — **OK (com prova)**

`snapshot_dirs()` registra a existência dos diretórios antes/depois; `planejar_rollback` separa
`dirs_criados` de `dirs_pre_existentes`; `executar_rollback` recebe `preservar=dirs_pre_existentes` e
`_remover_dirs_vazios` para no diretório preservado. Medido: caso L da suíte (pasta vazia
`BepInEx/plugins/AUT4Probe` pré-existente sobrevive; a DLL nascida na rodada é removida); a isca
`cp_aut5_isca_dir_pre_existente_removido` reprova como devia; a planta A5 (rollback sem `preservar`) faz a
isca passar e derruba `t_aut4_execucao` ("A5/L: pasta do probe PRE-EXISTENTE nao pode ser removida"). Sem
ressalva.

### A6 — MÉDIO — **ACHADO (médio) — parcial**

O que se afirmou: existe porta opt-in de ida-e-volta (LEITURA) no probe, **exigida pelo driver**.

**O que está de pé (prova dupla):** a porta existe **na fonte de hoje** (`Config.Bind("Geral",
"DemostrarTooltip", false, …)`, `MarcadorIdaEVolta`, `DemostrarIdaEVolta()` chamando
`ChamarShowTooltip()` → `Tooltip.ShowTooltip` real (assinatura ≥6 params) e **re**lendo `Tooltip.Title`,
gravando `ida_e_volta {marcador, titulo_lido, titulo_renderizado_lido, conferiu}`) **e no binário**
(`ilspycmd` no `AUT4Probe.dll`: `if (_demostrar.Value) { … DemostrarIdaEVolta(); }`,
`_res["ida_e_volta"] = … "conferiu"`). O driver exige a prova quando o plano tem `demostrar_tooltip`
(sem ela → `INDETERMINADO`/exit 1: caso J e isca `cp_aut5_isca_sem_prova_ida_volta`), e com ela fecha
(caso K, exit 0). **O driver exercita o probe que existe hoje.**

**Onde cai:** a exigência é satisfeita por uma autodeclaração **sem o marcador do driver**. O teste é
`conferiu and (not ida_volta.get("marcador") or marcador == marcador_ida_volta)` — o marcador é opcional.
Repro literal (`adversarial_aut4r.log`, sonda S4):

```
sem marcador    : status=CONCLUIDO exit=0 ida_e_volta_ok=True      <-- artefato {“conferiu”: true} apenas
com marcador    : status=CONCLUIDO exit=0 ida_e_volta_ok=True      (controle positivo)
marcador ERRADO : status=INDETERMINADO exit=1 ida_e_volta_ok=False (controle: o check SÓ dispara se o
                                                                    marcador vier)
```

Ou seja: a trava pega marcador **errado**, mas não pega marcador **ausente** — e o marcador único
(`AUT4-IDA-E-VOLTA-<sessão>`) é justamente o que amarra a prova a ESTA rodada.

### A7 — INFORMATIVO (documentação) — **OK (com prova)**

- `t_aut4_estado_docs.py` (verde) trava três coisas: listas declaradas == disco (9 testes, 11 iscas, 4
  fixtures), `probe_dll_sha256` == bytes da DLL em disco e `probe_fonte_sha256` == bytes do `.cs`,
  `probe_dll_reprodutivel_byte_a_byte == false`, e o doc humano com os números reais (`9/9` e `11 iscas`,
  proibido manter `6/6` / `2 iscas`).
- Medido por mim: os hashes declarados conferem com os meus (§1); a lista de iscas do estado (11) é
  exatamente o que o runner descobre; `AUT-4-preparacao.md` cita "9 testes offline + 11 iscas de
  contra-prova" e a tabela antes→depois por achado, sem `6/6`/`2 iscas`.
- `AUT-4-estado.json` agora traz `probe_dll_identidade` = "HASH DECLARADO … não é reproduzível byte a
  byte" — que é a leitura honesta (o rebuild em sandbox da AUT-4R2 deu um terceiro hash).
- Docs `AUT-3-*` do repo real **não** foram sobrescritos: continuam com mtime 05/10 15:47:07,
  15:49:10 e 15:49:10 e hashes `0efe68d2…`/`9c1aa582…`/`89f0fe66…` (medidos antes e depois de tudo).
  `bancada_aut3.py` escreve em `os.path.join(repo, "docs", "automacao", "AUT-3-*")` — isto é, no caminho
  do `--repo` (a cópia), não no repo real.

---

## 4. Divergência fonte × artefato do probe (o risco residual do próprio parecer)

O `AUT4ProbePlugin.cs` derivou depois do congelamento (mtime 13:53:18) e a DLL foi recompilada depois
(13:57:50) — mas **hoje o par casa**: os dois hashes estão declarados e conferem com os bytes, e o
**binário decompilado** contém o contrato do A1/A6 que a fonte declara. Não há divergência de *contrato*:

| contrato | fonte de hoje | binário de hoje (ilspy) |
|---|---|---|
| `Sessao` lida do `.cfg` e vencendo o carimbo local (A1) | sim | `_sessaoCfg = Config.Bind<String>("Geral","Sessao","")`; `_sessao = IsNullOrWhiteSpace ? carimbo : _sessaoCfg.Value` |
| porta opt-in de ida-e-volta (A6) | sim, default `false` | `Config.Bind<bool>("Geral","DemostrarTooltip", false, …)` + `if (_demostrar.Value) { … DemostrarIdaEVolta(); }` + `_res["ida_e_volta"]` com `"conferiu"` |
| 10 chaves do `.cfg` que o driver escreve | 10 binds | 10 binds (incl. `MarcadorIdaEVolta`) |
| chaves que o driver lê do JSON | `status`/`fase`/`sessao`/`hash_fonte`/`observacoes`/`prints`/`ida_e_volta` | todos gravados em `_res` |

A divergência **existe onde importa**, e é de **valor**, não de contrato: **o artefato do probe emite `""`
onde a fixture emite `null`** para o caso "não lido" (`GetParsedText()` → `string.Empty`, medido no
`lib/Unity.TextMeshPro.dll` do jogo; `Trunc` só devolve `null` para entrada `null`). O coletor foi
endurecido contra a **fixture**, não contra o **artefato**. Consequência: o A2 (§3) e o A6 (§3) ficam
verdes na bancada e furados no artefato. Fechar essa distância exige que a fixture
(`probe-saida-exemplo.entrada.json`) codifique a **forma real** do probe e que o critério de "lido" trate
vazio como não-lido.

---

## 5. Lacunas declaradas (NUNCA OK)

- **Rodada runtime EM JOGO: NÃO EXERCITADA.** Emissão real de campos em sessão viva, PNG pela API do
  Unity, owners Harmony vivos, navegação por handler real e rollback **em jogo**: nada disso rodou — esta
  revisão é 100% offline, como a entrega. Continua dependendo de **autorização explícita do dono**
  (CIC-5, `t_431dba37`).
- **Ida-e-volta em jogo: NÃO EXERCITADA.** O instrumento existe (fonte+binário) e o driver o exige, mas
  nunca rodou em sessão viva.
- **Gate de autorização do probe**: testado estaticamente (contrato da fonte) e no contrato do driver —
  não em execução.
- **Bancada offline AUT-3 (6 builds Release, 11 conferidores, `suite_puros` 87, `contra_prova` 49,
  `suite_jogo`): INDETERMINADO** — não re-executei (custo de 6 builds) e os números do `AUT-3-resumo.md`
  que o autor cita são auto-relato guardado fora do repo. Verifiquei por leitura de código o que dava para
  verificar sem re-executar: o build da bancada usa `-p:DeployToBepInEx=false` + `-p:PathMap`
  (`bancada_aut3.py:320`) e ela grava os `AUT-3-*` no caminho do `--repo`. A parte que eu **executei**
  (suíte 9/9 e contra-prova 11/11 sobre a cópia) está verde e medida na §2.
- Esta revisão **não fecha o DoD** e **não substitui o aceite humano**. AUT-4 e CIC-5 **não** foram
  desbloqueados por mim.

---

## 6. Verdicto final: **CHANGES REQUESTED**

O que falta, exatamente (todas são **reforço** de trava, nenhuma exige afrouxar critério — se a correção de
qualquer uma exigir mudar o critério do aceite, PARE e leve ao dono):

1. **A2 (grave, reaberto) — vazio não é leitura.** Em `coletor._estado_do_campo`, tratar como **não lido**
   string vazia/só-espaços e contêineres vazios (`""`, `[]`, `{}`), e não só `None`/as strings de
   `AUSENTES`. Ajustar `fixtures/probe-saida-exemplo.entrada.json` para codificar a forma REAL do
   artefato (`texto_renderizado: ""` no objeto sem mesh) — hoje ela codifica `null` e é o que mantém a
   suíte verde — e acrescentar a isca correspondente (`cp_*_isca_alvo_vazio_ok.py`).
   Repro: `adversarial_vazio.log` V1 (`CONCLUIDO`/exit 0 com `""`) × V1c (`INCOMPLETO`/exit 1 com `null`).
2. **A6 (médio) — exigir o marcador do driver.** Remover a escape `not ida_volta.get("marcador")`:
   marcador **ausente** ou diferente do gerado pelo driver ⇒ não conferido. Acrescentar isca
   (`cp_*_isca_ida_volta_sem_marcador.py`).
   Repro: `adversarial_aut4r.log` S4 (`sem marcador → CONCLUIDO exit 0`).
3. **A3 (médio) — precedência do "não é runtime".** Tratar `evidencia_runtime is False` **sozinho**
   (sem rótulo) como declaração de fixture (nunca consolidar como runtime) ou exigir declaração explícita
   de procedência no artefato. Acrescentar isca.
   Repro: `adversarial_aut4r.log` S3 (`evidencia_runtime=false → CONFIRMADA exit 0`, campo invertido p/
   `true`).
4. **A1-c (baixo) — datar os prints.** Exigir que cada arquivo de `prints` tenha mtime ≥ lançamento desta
   rodada (ou limpar do `out_dir` os artefatos da rodada anterior antes de lançar). Acrescentar isca.
   Repro: `adversarial_aut4r.log` S1 (PNG velho ⇒ `CONCLUIDO` exit 0; `out_dir` novo ⇒ `INDETERMINADO`).

E o secundário, junto do item 1: **validar o plano ANTES de instalar/lançar** no caminho executável
(`executar_rodada` não chama `validar_plano`; hoje um `campos_alvo` inválido só é recusado depois de
instalar o probe, escrever o `.cfg` e lançar, e sai `ERRO`/exit 1 em vez de `PLANO_INVALIDO`/exit 2).

Aprovado no que está medido e verde: A4, A5 e A7, mais os itens (a) e (b) do A1 e a **existência** da
porta de ida-e-volta do A6 (fonte + binário). **Sem "aprovado no geral"**: os 4 pontos acima bloqueiam o
fechamento, e nada em jogo pode ser tratado como OK.

---

## 7. Evidências (em `docs/automacao/COR-AUT4R-evidencias/`)

| arquivo | o que é |
|---|---|
| `hashes.txt` | sha256 de cada arquivo medido por mim (produto, réguas, docs `AUT-3-*`, `lib/Unity.TextMeshPro.dll`) |
| `suite-literal.log` / `contra-prova-literal.log` | a suíte 9/9 (exit 0) e a contra-prova 11/11 (exit 0) sobre a cópia, saída literal |
| `planta_defeitos.py` / `planta_defeitos.log` | planta o defeito de A1–A6 na cópia e mostra a isca PASSANDO e o runner VERMELHO |
| `planta_defeitos_suite.log` | qual teste da suíte cai com cada defeito plantado |
| `adversarial_aut4r.py` / `.log` | sondas S1 (PNG velho), S2 (vazio), S3 (`evidencia_runtime=false`), S4 (ida-e-volta sem marcador) + controles |
| `adversarial_vazio.py` / `.log` | sonda V1/V1c do A2 com a forma REAL do artefato + `owners=[]`/`keywords={}`/`cores={}` |
| `ilspy-AUT4ProbePlugin.cs` | `ilspycmd -t Aut4Probe.Aut4ProbePlugin` do binário de hoje (prova que o binário traz o A1/A6) |
| `tmp-getparsedtext.txt` | `ilspycmd -t TMPro.TMP_Text lib/Unity.TextMeshPro.dll` → `GetParsedText()` devolve `string.Empty` |

Reprodução: copiar `tools/testes/`, `tools/automacao/runtime/`, `tools/automacao/offline/`,
`docs/automacao/AUT-4-estado.json` e `docs/automacao/AUT-4-preparacao.md` para uma pasta fora do repo e
rodar os scripts de evidência com `python` a partir dela (eles escrevem só em `tempfile`).
