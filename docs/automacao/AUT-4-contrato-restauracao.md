# AUT-4 — contrato de ESPERA, BACKUP, MANIFESTO e RESTAURAÇÃO (rollback exato)

> Tarefa: **t_7e8f495b** (filha da AUT-4 / `t_b8b9822e`). Origem: **AUD-1**
> (`t_3feaddcc`) — lacunas **L1** (varredura/rastreabilidade do que a rodada cria) e
> **L2** (encerrar o jogo sem `taskkill`). Natureza: **offline** — nada aqui abre,
> instala ou encerra o jogo; o que se prova é o *contrato* do driver (`coletor.py`)
> por execução contra stub + executor injetado.
>
> Implementação: `tools/automacao/runtime/coletor.py` (driver) e
> `tools/automacao/runtime/testes/t_aut4_restauracao.py` (prova) + 3 iscas de
> contra-prova (`testes/contra-prova/cp_aut4rest_*`).

---

## 1. O que este contrato cobre (e o que não cobre)

Cobre, para a rodada runtime do AUT-4:

1. **espera de estado com timeout** (já existente, reusado sem reescrita);
2. **backup** do log anterior e dos arquivos do perfil que a rodada toca;
3. **manifesto** dos artefatos da rodada;
4. **restauração exata** (rollback) do que a rodada criou/modificou/removeu —
   inclusive arquivo criado **num caminho que o contrato não previu**;
5. **prova de restauração** (pos-rollback) e **fail-closed** quando sobrar resíduo;
6. **encerramento do jogo em duas etapas** (gracioso → forçado), sem `taskkill` cego.

**Não** cobre: execução real em jogo (segue **NÃO EXERCITADA** — exige autorização do
dono; ver §9), leitura de objetos vivos, PNG em jogo e navegação. O aceite humano não
é substituído por nada aqui.

---

## 2. Espera de estado com timeout (reuso — não reimplementar)

`_esperar_estado(caminho_log, caminho_json, timeout_s, poll_s)` (coletor.py) espera por
**estado**, nunca por `sleep` cego:

- `log_ok`: `LogOutput.log` com `Chainloader startup complete`;
- `json_ok`: JSON do probe legível;
- **parada por ESTADO TERMINAL**: `fase` terminal **ou** `status` terminal
  (`STATUS_TERMINAIS_ESPERA`) — o `catch` do probe grava `status=ERRO` **sem** setar
  `fase`, e parar só pela `fase` queimava o teto inteiro (R-3 do CIC-5R);
- teto (`timeout_s`, ou `OrcamentoSegundos` no orçamento do probe) sempre vale.

Testes: `t_aut4_cic5r.py` (R-3) e isca `cp_aut4f_isca_espera_queima_teto.py`.

---

## 3. O que a rodada VIGIA (o conjunto de restauração)

`caminhos_vigiados(perfil_dir, explicitos)` = **contrato explícito** ∪ **varredura das
árvores inteiras**:

| parte | caminhos |
|---|---|
| contrato (nomes fixos) | `BepInEx/plugins/AUT4Probe/AUT4Probe.dll`, `BepInEx/config/com.gumatos.aut4probe.cfg`, `BepInEx/LogOutput.log` |
| **varredura (L1)** | `BepInEx/plugins/**` e `BepInEx/config/**` — **todo** arquivo, em qualquer subpasta |

Por que a varredura: o `snapshot_arquivos` de lista fechada **não vê** o arquivo que o
probe cria num caminho fora do contrato — e o BepInEx varre `plugins/`
**recursivamente**: arquivo que nasce ali vira mod carregado. Sem a varredura,
"restaurar inclusive arquivos criados durante a coleta" seria intenção, não fato.
O `LogOutput.log` fica fora das duas árvores e por isso é vigiado explicitamente.

`snapshot_dirs` registra também a **existência dos diretórios** ancestrais: é o que
distingue "pasta que a rodada criou" de "pasta que já estava no perfil" (A5).

---

## 4. Backup

| o que | quando | onde | registro |
|---|---|---|---|
| `LogOutput.log` anterior | **antes** de lançar | `out_dir/log-anterior.log` | `resultado["backup_log"]` = `{origem, existia, backup, bytes, sha256, acao}` |
| todo arquivo vigiado que **já existia** | **antes** de lançar | `out_dir/rollback-backup/<mesmo caminho relativo>` (espelha a árvore — sem colisão de basename) | mapa `backups` + coluna `backup` no manifesto |

- O log é **removido** do perfil depois de arquivado: um boot **trunca** o log, então o
  boot desta rodada tem de ser o único log lido.
- **Ausência é declarada**: sem log anterior, `backup_log["existia"] = false` e o motivo
  fica escrito (`acao`) — nada é inventado.
- O `out_dir` **não** é restaurado: ele é a **evidência** da rodada (JSON do probe, PNG,
  cfg instalado, launcher.txt, backups). Resíduo *dentro do perfil*, não no `out_dir`.

---

## 5. Classificação e ordem da restauração (rollback exato)

`planejar_rollback(antes, depois, dirs_antes, dirs_depois)` classifica cada caminho:

| classe | significado | ação |
|---|---|---|
| `criados` | não existia antes (nasceu na rodada, **inclusive fora do contrato**) | **REMOVER** e apagar diretórios que ficarem vazios |
| `modificados` | hash diferente do de antes | **RESTAURAR** o conteúdo do backup (byte a byte) |
| `removidos` | existia antes e sumiu | **REPOR** o arquivo a partir do backup |
| `dirs_criados` | diretório que a rodada criou | **REMOVER** se ficar vazio |
| `dirs_pre_existentes` | diretório que já existia | **PRESERVAR** (nunca removido, mesmo vazio) |

`executar_rollback(raiz, plano_rb, backups, preservar=dirs_pre_existentes)` executa
nessa ordem. Arquivo sem backup sai como `sem-backup` no log de ações — **declarado**,
nunca silencioso (e `efeitos_colaterais` lista tudo que não foi `sem-backup`).

**Falha do rollback não derruba o driver**: erro de remoção/restauração (arquivo
travado/sem permissão) é registrado em `resultado["rollback_erro"]` e a **prova de
restauração** passa a acusar (§6).

---

## 6. Prova de restauração (o critério de "sem efeito residual")

`verificar_sem_residuo(raiz, relativos, antes, dirs_antes)` roda **depois** do rollback,
re-varrendo as árvores vigiadas, e devolve:

```
{ "limpo": bool,
  "residuos":    [arquivo criado que sobrou],
  "divergentes": [arquivo restaurado com hash diferente],
  "faltando":    [arquivo removido que não voltou],
  "dirs_residuo":[diretório criado pela rodada que sobrou] }
```

`limpo` só é `True` com as quatro listas vazias. O resultado da rodada carrega
`resultado["restauracao"]`, e **restauração não exata rebaixa o veredito**:

| situação | status | exit |
|---|---|---|
| restauração exata | o status do desfecho (`CONCLUIDO`/`INCOMPLETO`/...) | 0/1 |
| **resíduo/divergência/falta/diretório sobrando** | **`RESIDUO`** | **1** (≠ 0) |

Ou seja: uma rodada que deixou sujeira no perfil **não pode** ser apresentada como
limpa nem confirmada — o defeito vira texto (`motivo` nomeia cada item). É a contra-prova
de "restauração exata ... e sem efeitos residuais" **dentro do próprio artefato**, não
só no teste.

---

## 7. Manifesto da rodada

`montar_manifest_da_rodada(out_dir, perfil_dir, relativos, antes, depois, backups)` —
`resultado["manifest"]`:

1. **artefatos** — todo arquivo do `out_dir` com caminho relativo, `bytes` e `sha256`
   (a prova de *qual* arquivo saiu; arquivo ilegível sai com `erro`, não com hash forjado);
2. **arquivos_vigiados** — cada caminho vigiado com `sha256_antes`, `sha256_depois`,
   `estado` (`criado`/`modificado`/`removido`/`intocado`) e o `backup` disponível;
3. listas-resumo `criados` / `modificados` / `removidos`.

Observação de honestidade herdada: o sha do **próprio** `aut4probe.json` dentro do
manifesto do probe é auto-referente (calculado antes do arquivo fechar) — por isso a
identidade usada é o hash **medido em disco** (`provar_atualidade`), e o manifesto do
driver é o autoritativo.

---

## 8. Encerramento do jogo em duas etapas (L2)

`comandos_de_fechamento(pid)` — ordem **fixa**:

1. **gracioso**: `powershell -NoProfile -NonInteractive -Command
   "(Get-Process -Id <PID> -ErrorAction SilentlyContinue).CloseMainWindow()"` — pede ao
   jogo que feche a própria janela. É o caminho que funciona em rodada **sem usuário**,
   onde `taskkill` é bloqueado;
2. **forçado (fallback)**: `taskkill /F /PID <PID>` — **só** o PID que nasceu nesta
   rodada.

`planejar_encerramento(imagem, pids_antes, pids_depois)` decide **quem** encerrar
(`pids_depois − pids_antes`); sem medição dos PIDs → **RECUSA** (fail-closed: matar por
imagem atingiria todas as instâncias, inclusive a que o dono já tinha aberta — por isso
`/IM` não existe no driver). `encerrar_processos(plano, executar=, pid_vivo=, dormir=)`
executa a decisão: gracioso → espera → confere o PID → forçado só se ele continuar vivo
(ou se não der para confirmar). Recusa ⇒ **nenhum** comando é executado.

Os injetáveis (`executar`, `pid_vivo`, `pids_medir`, `dormir`) existem para o teste
provar a **ordem** e o **fallback** sem fechar processo nenhum.

---

## 9. Limites declarados (NÃO são OK)

- **Runtime em jogo NÃO EXERCITADO**: nada disto rodou em sessão viva (leitura real,
  PNG, owners, navegação, rollback contra o **perfil do dono**). Exige autorização
  explícita + uma única frente controlando o jogo.
- O `taskkill /F /PID` real e o `CloseMainWindow` real **nunca** foram executados contra
  jogo/processo do dono — o que está provado é a **decisão**, a **ordem** e a
  **execução com executor injetado**.
- A restauração cobre as árvores `BepInEx/plugins/**` e `BepInEx/config/**` + o log.
  Arquivo criado pela rodada **fora** dessas árvores (ex.: raiz do perfil, `BepInEx/core/`)
  não é vigiado — a rodada não deve escrever lá; se escrever, o manifesto **não** o verá.
  (Alargar o conjunto é decisão de contrato, não de implementação silenciosa.)
- Em perfil **grande** (muitos mods) o backup espelha todos os arquivos vigiados: é
  intencional (restauração exata), e é mais um motivo para a rodada usar **perfil
  isolado**.
- **Risco declarado da varredura (L1)**: qualquer arquivo que **nasça** durante a rodada
  dentro das árvores vigiadas é classificado como `criado` e **removido** no rollback —
  inclusive um `.cfg` que um mod escreva em `BepInEx/config/` durante a sessão. Isso é o
  comportamento desejado para o instrumento (o BepInEx carrega tudo que nasce em
  `plugins/`), mas é exatamente o motivo de a rodada runtime usar **perfil isolado** e
  nunca o perfil do dono: o rollback restaura o *instrumento*, e não sabe distinguir
  "arquivo do probe" de "arquivo que outro mod criou no meio do caminho".
- Builds do probe: sempre `-p:DeployToBepInEx=false`; esta frente **não** alterou
  `Assembly-CSharp.dll`, Bard/gameplay, travas, nem o CAP-1.

---

## 10. Como provar offline (comandos e desfecho)

```
cd C:/dev/stolen-realm
python tools/automacao/runtime/roda_testes_runtime.py               # suite offline
python tools/automacao/runtime/roda_testes_runtime.py --contra-prova # iscas TEM de reprovar
```

A prova específica desta frente é `testes/t_aut4_restauracao.py` (7 blocos):

| bloco | prova |
|---|---|
| `_varredura` | a varredura enxerga arquivo em subpasta de `plugins/` e o sha256 confere |
| `_backup_log` | ausência declarada; arquivamento com `bytes`/`sha256`; log removido do perfil |
| `_residuo` | limpo quando nada mudou; acusa criado/divergente/faltante/diretório |
| `_manifesto` | artefatos com sha256; `criado`/`modificado`/`intocado`/`removido`; backup nomeado |
| `_encerramento` | ordem gracioso→forçado; recusa não executa nada; fallback só com PID vivo |
| `_rodada_completa` A/B | rodada limpa (exit 0) com arquivo criado **fora do contrato** removido; log anterior restaurado byte a byte |
| `_rodada_completa` C/D | gracioso primeiro com executor **injetado**; rollback que **falha de verdade** ⇒ `RESIDUO`/exit 1 |

Iscas de contra-prova (têm de **reprovar**):

- `cp_aut4rest_isca_residuo_nao_detectado.py` — afirma que resíduo passa por "limpo";
- `cp_aut4rest_isca_forcado_primeiro.py` — afirma que o forçado vem antes do gracioso;
- `cp_aut4rest_isca_backup_log_sem_registro.py` — afirma que o backup não deixa rastro.
