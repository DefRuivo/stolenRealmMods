# CIC-5 — entrega: coleta/normalizacao/execucao-restauracao conectavel ao ciclo (`t_431dba37`)

**Escopo exclusivo desta entrega:** `tools/automacao/runtime/**` e este documento. Nao toquei em
`ciclo/` (CIC-1), `cenarios/` (CIC-3/4), `bancada offline`, produto, probe de outra frente, `KANBAN.md`
nem board. **Rodada OFFLINE**: nenhum build de mod, nenhum jogo aberto/encerrado, nenhum save, nenhum
probe instalado no perfil do dono, nenhum commit/push/publicacao.

> Objetivo: tornar o coletor AUT-4 **conectavel ao ciclo** — costura do JSON real do probe,
> normalizacao por campo-alvo, e **caminho executavel** de instalar/lancar/esperar/reverter (que antes
> so existia como plano). A rodada minima em jogo e a **proxima rodada autorizada**, nao esta.

## O que foi entregue

| arquivo | papel |
|---|---|
| `tools/automacao/runtime/coletor.py` | costura B1/B2/B3 + caminho executavel + `provar_atualidade` + CLI |
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | **fix A3**: guarda fake-null → `ReferenceEquals` (CLR) no gancho e no motor; PlayerLoop preservado |
| `tools/automacao/runtime/testes/t_aut4_costura_probe.py` | prova B1/B2/B3 e a honestidade da fixture |
| `tools/automacao/runtime/testes/t_aut4_execucao.py` | prova instalar/lancar/esperar/reverter por **artefato em disco** |
| `tools/automacao/runtime/testes/t_aut4_probe_contrato.py` | reforco: exige `ReferenceEquals` e proibe a guarda fake-null / preserva `SetPlayerLoop` |
| `tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json` | FIXTURE no formato **exato** do `aut4probe.json` |
| `testes/contra-prova/cp_aut5_isca_sem_autorizacao_executa.py` · `cp_aut5_isca_topo_sem_hash_ok.py` | iscas (tem de reprovar) |

## Bloqueios funcionais resolvidos (prova, nao opiniao)

| # | bloqueio (AUT-4R) | como foi corrigido | prova |
|---|---|---|---|
| **B1** | observacao do probe nao tem `sessao`/`hash_fonte` (so no topo) ⇒ `ObservacaoInvalida` | `carregar_saida_probe` + `anexar_contexto` injetam o topo em cada item; `normalizar_observacao(..., contexto=...)` aceita o contexto | `t_aut4_costura_probe` (cru RECUSA; com costura OK) |
| **B2** | 5 campos uteis descartados (`componente`, `visivel_na_tela`, `shader_suportado`, `tamanho_fonte`, `nota_texto_renderizado`) | entram em `CAMPOS_EXTRAS`; atravessam a normalizacao (nunca viram lacuna) | 5 campos presentes no normalizado |
| **B3** | "os 13 campos de todo TMP_Text" ⇒ `INCOMPLETO` por objeto inativo | **campo-alvo por cenario** (`campos_alvo`) + **fallback inativo DECLARADO** (`texto_renderizado` → `NAO_APLICAVEL`, `fallback=texto_bruto`, com motivo) | inativo nao vira lacuna; **objeto ATIVO sem rendered continua lacuna** (controle negativo no mesmo teste) |
| **A3** | guarda `i == null` (operador Unity) = fake-null ⇒ gancho e motor mudos | `ReferenceEquals(i, null)` / `!ReferenceEquals(...)` no `PostfixDoGancho` e no `MotorDoProbe.Update` | decompilado da DLL: `Instancia?.Tick("gancho")` e `Instancia?.Tick("motor")` = null do CLR |
| **A1/A2** | coletor so **planejava**; `planejar_rollback` **orfao** | `executar_rodada` (instala/lanca/espera/reverte) + `executar_rollback` | `t_aut4_execucao` (4 casos, artefato em disco) |

## Caminho executavel (sem jogo, sem stub escondido)

`executar_rodada(...)` faz, com **perfil isolado**:

1. **default NAO AGE**: sem `autorizado`+`jogo_disponivel`+`confirmacao=='coleta'` retorna
   `NAO_EXERCITADO` (exit 2) **antes** de tocar em qualquer arquivo/processo (`efeitos_colaterais=[]`).
2. instala o probe no perfil indicado e **escreve o `.cfg` derivado** — `Autorizado` (da rodada),
   `PerfilDir`, `HashFonte = sha256(DLL)`, `Navegar=false`, `OrcamentoSegundos`, `MaxTextos`.
   **Sem gerar credencial nenhuma.**
3. arquiva o `LogOutput.log` anterior (um boot trunca o log) e remove-o.
4. lanca pelos **argumentos de doorstop** (`-applaunch 1330000 --doorstop-enabled true
   --doorstop-target-assembly <preloader do perfil>`). A porta e substituivel: `comando_lancamento`
   troca o **caminho absoluto do Steam** (`C:\Program Files (x86)\Steam\steam.exe`) por um **stub real**.
5. espera **ESTADO** (log com `Chainloader startup complete` + JSON do probe em fase terminal), com teto
   — nunca sleep cego.
6. le a saida do probe, pede o PNG pela API (no probe), consolida e **prova a atualidade**.
7. **`finally`**: encerra **so** o processo que a rotina lancou (`Popen`) e faz o **rollback EXATO**
   (remove o que nasceu; restaura o que mudou) — inclusive `.cfg` e `LogOutput.log`.

Prova de que **executou o artefato, nao uma mensagem inventada**: o stub grava o proprio `argv` em
disco e o teste confere que o driver passou `-applaunch`/AppID/`--doorstop-target-assembly ...Preloader.dll`;
e a observacao consolidada contem o **marcador que o stub escreveu no `aut4probe.json`** do disco.

## Atualidade fonte/DLL/sessao/manifest

`provar_atualidade` compara: sha da **DLL instalada** × `HashFonte` do **cfg** × `hash_fonte` da
**saida do probe**; marca `sessao_ok` e monta o manifest com os bytes **em disco**. O sha do proprio
`aut4probe.json` no manifest do probe e **AUTO-REFERENTE** (calculado antes do arquivo fechar) →
marcado `auto_referente=true`, `autoritativo=false`. Hash de fonte **stale ⇒ `INDETERMINADO`** (exit 1),
nunca `CONCLUIDO`. Nao abre cascata de hardening: so impede o falso OK de quem usa o manifest.

## Integracao com o ciclo (contrato v1)

- `consolidar_probe(saida_ou_caminho, plano)` devolve as **observacoes normalizadas** (com `campos`,
  `lacunas`, `nao_aplicaveis`, `sessao`,`hash_fonte`) — o formato que os adaptadores CIC-3/4 consomem em
  `avaliar(observacoes, identidade)`. `identidade` = `{fonte_sha, dll_sha}` (CIC-1); a identidade do
  probe (`hash_fonte`) casa com `dll_sha`.
- **Fixture rotulada nao vira runtime**: `consolidar_probe` **auto-detecta** (`procedencia: fixture` /
  `evidencia_runtime:false` + `rotulo_fixture`) e devolve `FIXTURE` (exit 2).
- **Nao editei** `ciclo/` nem `cenarios/`: a costura fica do lado do coletor (o adaptador traduz, o
  coletor nao impoe formato).

## Evidencia (execucao real, offline)

- `python tools/automacao/runtime/roda_testes_runtime.py` → **VERDE, 8/8, exit 0** (era 6/6).
- `... --contra-prova` → **VERDE, 4/4 iscas reprovam, exit 0** (2 novas: execucao-sem-autorizacao,
  topo-sem-hash).
- CLI exercitado (outputs reais):
  - `coletor.py --plano .../plano-exemplo...` → `NAO_EXERCITADO`, **exit 2** (`out/ex5-1.json`);
  - `coletor.py --plano ... --executar` (sem autorizacao) → `NAO_EXERCITADO`, **exit 2**,
    `efeitos_colaterais=[]`, nada criado em disco (`out/ex5-2.json`);
  - `coletor.py --plano ... --saida-probe .../probe-saida-exemplo...` → **FIXTURE, exit 2**
    (`out/ex5-3.json`) — a fixture nao prova runtime.
- Build do probe (1x, sem deploy): `dotnet build -c Release -v q AUT4Probe.csproj
  -p:DeployToBepInEx=false` → **Build succeeded, 0 Error(s)** (1 warning MSB3277 herdado).
  **Perfil do dono intacto** (sem pasta `AUT4Probe` em `plugins/`).
- Suite do projeto intacta: `python tools/testes/roda_testes.py --puros` → **exit 0**.

## Lacunas declaradas — runtime **NAO EXERCITADO**

Nada disto foi exercitado (e esta declarado, nao maquiado):

- **Lancamento real do jogo** (Steam/`.exe`) — proibido nesta rodada; o stub prova o **caminho de
  comando**, nao o jogo.
- **Emissao real dos 18 campos pelo probe em sessao viva**, PNG pela API, `owners` vivos.
- **Rollback contra o perfil real** do dono (o exercitado e contra perfil de fixture).
- **`encerrar_imagem`** (fechar o jogo por imagem) e um **opt-in explicito**, desligado por default e
  nunca acionado contra o stub. Ele faz `taskkill /IM` — e o processo do Steam nao carrega a identidade
  "foi a rotina que lancou", entao **nao existe prova automatica** de que a instancia e a da rodada; por
  isso o default e **NAO fechar** e o flag so deve ser passado na rodada autorizada de frente unica,
  depois de a rotina ter iniciado o jogo.
- **Sem hot-reload**: o probe e novo; a rodada minima **exige instalar e iniciar** o jogo.

## Proxima rodada (autorizada; NAO executada aqui)

Precisa do dono: **(a)** autorizar **uma** frente runtime (instalar probe + iniciar o jogo, **sem
save/combate**); **(b)** dizer se usa **perfil isolado** ou o dele (com rollback exato). Comando
proposto (default continua nao agindo sem os tres flags):

```bash
python tools/automacao/runtime/coletor.py \
  --plano tools/automacao/runtime/fixtures/plano-exemplo.entrada.json \
  --executar --autorizado --jogo-disponivel --confirmar-coleta coleta \
  --perfil "<PERFIL_ISOLADO>" \
  --out-dir "<OUT>" \
  --dll-probe tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll \
  --encerrar-imagem "Stolen Realm.exe"
```

## Achados secundarios (backlog; nao bloqueiam)

- **`AUT-4-estado.json` ficou STALE** (fora do meu escopo): declara `probe_dll_sha256 = e8ee229b…`, mas
  a DLL reconstruida e **`3c32f026…`**. O pai/supervisor deve atualizar esse arquivo na proxima rodada.
- **Manifest auto-referente** (A4): mitigado (`auto_referente`/`autoritativo`), sem cascata.
- **Sem segredos**: nenhuma credencial gerada, lida ou gravada.

## Arquivos e hashes (sha256)

```
2f502e0d4ca45374f7d6a06f751254eb684e962d722ebb260e6324cee8959e83  tools/automacao/runtime/coletor.py
3525c0e6fa17dae26e5742e44fd620710d18cb9177383a44474fe91d44cb048d  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs
3c32f0269ae08811e9e997a2fc5ac7c8f10e40887330aa808725bde46003df46  tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll
9a1781bd1ac7ebab846da66446f8c33fe7e3c2909b8fbf40ad5e65671de20af0  tools/automacao/runtime/testes/t_aut4_costura_probe.py
b296e5aa68517ca5855bd8502896751250de7951bfa64c6a1655f84142b669c9  tools/automacao/runtime/testes/t_aut4_execucao.py
1ee497dde5d48f60a6bd555458bfbaadafc36ddab0f2422a8fefb934fe83b0f0  tools/automacao/runtime/testes/t_aut4_probe_contrato.py
725965af1714ab4ed3bc126e7ad17632373cc5f4739011b6b913797bcbfef6f0  tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json
f1d46f05f6563e3e4cd132f32be82dbadf9afeab102702f60eee5adf793e728b  tools/automacao/runtime/testes/contra-prova/cp_aut5_isca_sem_autorizacao_executa.py
41770314bd035079180d878486f8ba8a34d41ee83a133287f2911dbb6bf53380  tools/automacao/runtime/testes/contra-prova/cp_aut5_isca_topo_sem_hash_ok.py
```

HEAD `f526fe9` (branch `ci-validate-test`) · rodada offline `2026-10-05 ~18:35`.
