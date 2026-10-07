# COR-AUT4 — entrega da correção dos 6 achados da AUT-4R2 (t_b62359c3)

Origem: `docs/automacao/AUT-4R2-revisao.md` (revisão independente que REPROVOU a AUT-4).
Escopo executado: **só** o que o parecer exige (A1/A2 graves; A3–A6 médios; A7 documentação).
Nada de rodada runtime: **nenhum jogo aberto, nenhum save tocado, nenhum probe instalado no perfil,
nenhum deploy, nenhuma publicação**. A bancada offline rodou sobre uma **cópia** do repositório.

## O que mudou (arquivo → papel)

| arquivo | o que mudou |
|---|---|
| `tools/automacao/runtime/coletor.py` | A1 (provas de execução + sessão do driver + `Sessao`/`DemostrarTooltip`/`MarcadorIdaEVolta` no `.cfg`), A2 (`campos_alvo` governa: alvo não lido = lacuna; alvo fora do schema = `PlanoInvalido`), A3 (rótulo do artefato vence o chamador), A4 (`status`/`fase` do probe no veredito), A5 (`snapshot_dirs` + rollback que preserva diretório pré-existente), A6 (exigência da prova de ida-e-volta quando o plano pede) |
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | A1 (lê a chave `Sessao` do `.cfg`; o carimbo local vira fallback declarado) e A6 (porta **opt-in** `DemostrarTooltip`/`MarcadorIdaEVolta` + `DemostrarIdaEVolta()` chamando `Tooltip.ShowTooltip` e relendo `Tooltip.Title` — **LEITURA**, default `false`) |
| `tools/automacao/runtime/testes/t_aut4_execucao.py` | stub do lançador agora lê o `.cfg`, grava log de boot + linha de vida + PNG real; casos novos A1 (E/F/G/H), A2 (I), A6 (J/K) e A5 (L) |
| `tools/automacao/runtime/testes/t_aut4_costura_probe.py` | A2 (alvo não lido ⇒ `INCOMPLETO`; alvo fora do schema ⇒ `PlanoInvalido`), A3, A4 (4 estados + instrumento mudo) |
| `tools/automacao/runtime/testes/t_aut4_plano.py` | A2: `campos_alvo` typo/misto/vazio (topo e cenário) ⇒ `PlanoInvalido` |
| `tools/automacao/runtime/testes/t_aut4_probe_contrato.py` | A1 (marcadores da chave `Sessao`) e A6 (marcadores da porta de ida-e-volta, default FALSE) |
| `tools/automacao/runtime/testes/t_aut4_estado_docs.py` | **novo** — trava a deriva do A7: lista declarada == disco, hash declarado == bytes, doc com os números reais |
| `tools/automacao/runtime/testes/contra-prova/` | **7 iscas novas** (`cp_aut5_isca_sem_prova_execucao`, `cp_aut5_isca_alvo_nao_lido_ok`, `cp_aut5_isca_alvo_fora_do_schema`, `cp_aut5_isca_procedencia_do_chamador`, `cp_aut5_isca_status_erro_confirma`, `cp_aut5_isca_dir_pre_existente_removido`, `cp_aut5_isca_sem_prova_ida_volta`) |
| `docs/automacao/AUT-4-estado.json` | A7: hash MEDIDO da DLL e do fonte, não-reprodutibilidade byte a byte, identidade = hash declarado, listas reais de testes/iscas/fixtures, tabela dos achados corrigidos |
| `docs/automacao/AUT-4-preparacao.md` | A7: números reais (9 testes / 11 iscas) e tabela antes→depois por achado |

Fora do escopo e **intocado**: nenhum arquivo de mod, perfil, config, `KANBAN.md`, `scratch/cap1/`
original, `docs/automacao/AUT-2*` ou as frentes AUT-3/AUT-5/AUT-6/AUT-7.

## sha256 do que foi escrito

```
c7032285e2e9828d8b3c3c9ffd41420f3a0ccebe0f75440a0b67533135f8ddae  tools/automacao/runtime/coletor.py
5a51abaa439b90263e3b202e01a0b2b3b343fabc8cb71c9de8b3ac97b343bdd3  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs
fd774259b5e8813f2f3b29e2ff805f12cb0cdab4c277116fcc8bbb7e7e3bffdd  tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll
```
(os hashes de todos os testes/iscas/docs estão no `AUT-3-resultado.json` da bancada e nos eventos da
tarefa; a DLL é **identidade por hash declarado** — não é reprodutível byte a byte.)

## Comandos exatos e saída real

```
$ python tools/automacao/runtime/roda_testes_runtime.py
[PASSOU] testes\t_aut4_autorizacao.py
[PASSOU] testes\t_aut4_controle_negativo.py
[PASSOU] testes\t_aut4_costura_probe.py
[PASSOU] testes\t_aut4_estado_docs.py
[PASSOU] testes\t_aut4_execucao.py
[PASSOU] testes\t_aut4_manifest_rollback.py
[PASSOU] testes\t_aut4_observacao.py
[PASSOU] testes\t_aut4_plano.py
[PASSOU] testes\t_aut4_probe_contrato.py
 VEREDITO: VERDE (exit 0) — 9 teste(s)

$ python tools/automacao/runtime/roda_testes_runtime.py --contra-prova
 VEREDITO: VERDE (exit 0) — 11 teste(s)     (as 11 iscas reprovam como deviam)

$ python tools/automacao/runtime/coletor.py --plano fixtures/plano-exemplo.entrada.json
    "status": "NAO_EXERCITADO", "pode_coletar": false
    "motivo": "coleta NAO autorizada (default do repositorio): nenhuma leitura, PNG ou navegacao sera feita"

$ python tools/automacao/runtime/coletor.py --plano fixtures/plano-exemplo.entrada.json \
      --saida-probe fixtures/probe-saida-exemplo.entrada.json --procedencia runtime
  "status": "FIXTURE", "evidencia_runtime": false
  "motivo": "o proprio artefato se declara fixture (probe-saida-exemplo): o rotulo tem
             precedencia sobre a intencao do chamador"

$ python tools/automacao/runtime/coletor.py --plano <plano com campos_alvo ["texto_bruto","field_typo"]>
{
  "esquema": "AUT-4/1",
  "status": "PLANO_INVALIDO",
  "motivo": "PlanoInvalido: campos_alvo fora do schema: field_typo (validos: objeto, caminho, ...)",
  "dados_sinteticos": false,
  "observacoes": []
}
EXIT=2

$ cd tools/automacao/runtime/AUT4Probe && dotnet build -c Release --no-incremental -v q \
      -p:DeployToBepInEx=false AUT4Probe.csproj      # USERPROFILE/APPDATA/LOCALAPPDATA isolados
    1 Aviso(s)  0 Erro(s)   (MSB3277 System.Net.Http — herdado das DLLs do jogo, igual ao CapProbe)
```

## Prova vermelho→verde por achado (medida, não descrita)

Antes da correção, as 7 iscas novas rodaram **PASSOndo** — ou seja, o defeito existia e a isca o
detecta. Depois, as mesmas 7 **reprovam**:

```
ANTES  (coletor.py 0518634e…):  7 x [PROVA FALHOU (passou quando devia reprovar)]  -> VEREDITO: VERMELHO (exit 1)
DEPOIS (coletor.py c7032285…):  11 x [PROVA OK (reprovou como devia)]              -> VEREDITO: VERDE (exit 0)
```

| achado | o que a correção faz | prova de correção |
|---|---|---|
| A1 | sem sessão desta rodada / sem JSON mais novo / sem log de boot+probe / sem print com bytes ⇒ nunca `CONCLUIDO` | `t_aut4_execucao.py` E/F/G/H + isca `cp_aut5_isca_sem_prova_execucao` |
| A2 | alvo não lido (AUSENTE/NAO_APLICAVEL) = lacuna ⇒ `INCOMPLETO`; alvo fora do schema ⇒ `PlanoInvalido` | `t_aut4_costura_probe.py`, `t_aut4_plano.py` + iscas `cp_aut5_isca_alvo_nao_lido_ok` / `cp_aut5_isca_alvo_fora_do_schema` |
| A3 | rótulo do artefato vence ⇒ `FIXTURE`/exit 2 | `t_aut4_costura_probe.py` + isca `cp_aut5_isca_procedencia_do_chamador` |
| A4 | ERRO/SEM_UI/ORCAMENTO_ESTOURADO/NAO_EXERCITADO (ou status mudo) ⇒ não `CONFIRMADA`, exit ≠ 0 | `t_aut4_costura_probe.py` + isca `cp_aut5_isca_status_erro_confirma` |
| A5 | diretório pré-existente sobrevive ao rollback | `t_aut4_execucao.py` L + isca `cp_aut5_isca_dir_pre_existente_removido` |
| A6 | instrumento de ida-e-volta opt-in no probe + exigência da prova no driver | `t_aut4_probe_contrato.py`, `t_aut4_execucao.py` J/K + isca `cp_aut5_isca_sem_prova_ida_volta` |
| A7 | estado/doc casam com o disco (trava automática) | `t_aut4_estado_docs.py` (vermelho antes de atualizar o estado/doc, verde depois) |

## Bancada offline sobre a cópia

```
$ python tools/automacao/offline/bancada_aut3.py \
      --repo <copia do repositorio> --ancora C:/dev/stolen-realm --trabalho <scratch> --jogo
{
  "veredito": "VERDE",
  "builds": 6,
  "checagens": 11,
  "suite": 3,
  "contra_provas": 5,
  "perfil_intacto": true,
  "repo_intacto": true,
  "cobertura": {"OK_OFFLINE": 7, "PARCIAL_OFFLINE": 1, "NAO_EXERCITADO": 12, "REPROVADO": 0}
}
EXIT=0
```
Detalhe (no `AUT-3-resumo.md` **dentro da cópia**, sha256 `7720d711c4c8117f0f5ce034fcfa2c5972b390e7dbfe2cad4c08bb5c08b979a8`):
`fases puladas: nenhuma` · 6/6 builds Release sem deploy (`fonte->DLL = Release = perfil` em 5;
RoguelikeSkillTreeVisualizer fica PARCIAL_OFFLINE porque a DLL instalada no perfil está desatualizada
para o fonte atual dessa frente — estado **pré-existente**, fora do escopo desta correção) ·
11/11 conferidores estáticos OK · `suite_puros` 87 PASSOU · `suite_contra_prova` 49 PROVA_OK ·
`suite_jogo` OK · 5/5 contra-provas da bancada reprovaram como deviam.

O runner escreve `docs/automacao/AUT-3-*` no caminho de `--repo`: os documentos do repositório real
**não** foram sobrescritos (seguem com o resultado de 2026-10-05 15:47).

## O que NÃO foi exercitado (declarado, não é OK)

- Emissão real de campos em sessão viva, PNG do jogo, owners em sessão viva, navegação e rollback
  **em jogo**: **NÃO EXERCITADO** (esta entrega é offline; rodada runtime exige autorização do dono).
- **Ida-e-volta em jogo**: o instrumento existe e o driver o exige, mas nunca rodou em sessão viva —
  **NÃO EXERCITADO**.
- O gate de autorização do probe continua testado **estaticamente** (contrato do fonte) e no
  contrato do driver, não em execução.
