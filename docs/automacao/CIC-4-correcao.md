# CIC-4 — correção: prova e contrato de runtime do avaliador tooltips/shrines (`t_6dc6484b`)

Correção dos achados **#8** e **#9** da revisão independente (`docs/automacao/CIC-4R-revisao.md`),
reaberta pelo pai, e propagação do contrato endurecido (`CICLO-VALIDACAO-escopo.md` §"Correções
funcionais da primeira integração") para integrar o avaliador ao ciclo **sem falso verde de runtime e
sem evidência fingida**.

**Escrita exclusiva desta rodada:** `tools/automacao/cenarios/tooltips_shrines.py`,
`test_tooltips_shrines.py` e este documento. Os dados `shrines-*.json` não mudaram de comportamento.
**Rodada OFFLINE:** nenhum build, jogo, install, save, commit, push ou publicação. Não toquei produto,
probe, bancada, `checa_shrines.py`, `regras_shrine.py`, `gera_shrines_esperado.py`, os CSV gerados
(o **oráculo/esperado** e a "mecânica" do motor ficaram intactos), nem `decisao.py`/`ciclo.py`/`rstv.py`.

## O que foi corrigido

| # | achado (CIC-4R) | correção | regra dura aplicada |
|---|---|---|---|
| **8** | rótulo `runtime` auto-declarado vira prova vinculante (obs sem `hash_fonte` fechava OK) | `_cadeia_runtime`: só fecha OK com a **cadeia completa confrontada** — identidade suficiente, `hash_fonte` **presente e igual** ao `fonte_sha` da rodada, `sessao`, `config_sha` quando a observação o declara, e evidência do artefato lido | prova exige cadeia, **não** rótulo; ausência/falha ⇒ `NAO_EXERCITADO`/`INDETERMINADO`, nunca OK |
| **8** | default de procedência era `runtime` | observação sem rótulo/desconhecido vira **`execucao`** (nunca runtime por default) | rótulo ausente não aprova |
| **8** | critério runtime não expunha a cadeia ao `decisao.py` | critério runtime OK passa a carregar `sessao` + `fonte_sha` + `dll_sha` (+ `config_sha` quando aplicável), confrontados com a identidade | contrato positivo de runtime |
| **9** | evidência montada sem o artefato lido (módulo verde ≠ ciclo verde) | `evidencia` só do **artefato realmente lido** (`evidencia` declarada / `objeto` que existe no repo); sem artefato ⇒ `NAO_EXERCITADO`, **nunca OK**; o CSV do esperado **não** entra como evidência da observação | não fingir evidência/caminho |
| — | `procedencia="offline"` fora do enum do contrato | trocado por **`execucao`** (só nas lacunas de fonte do esperado), com `classe` coerente | enum `execucao`/`runtime`/`fixture` |
| — | lacuna técnica virava autorização humana por default | lacuna de coleta/campo/identidade mantém `classe=runtime`/`procedencia=runtime` (**sem mascarar runtime**) + `autorizacao_necessaria=false` + `tipo_pendencia=coleta_tecnica` ⇒ `decisao.py` roteia para **falhas automáticas (fila de agente)** | só autorização/julgamento **explícito** vai ao dono |

Esperado/oráculo preservados: `_esperado_atributo`/`_esperado_perigo` e o eixo `Source` do RV-30 não
foram tocados; o esperado continua saindo das tabelas geradas + `regras_shrine`. Fixture permanece
fixture (`prova_runtime=false`) mesmo com todos os valores combinando.

## Testes (RED → GREEN, TDD)

Novos casos **RED** provados falhando contra o módulo antigo e verdes após a correção:

- `runtime-sem-evidencia-nao-aprova` (#8/#9) — rótulo runtime + hash casando, sem artefato: não fecha.
- `runtime-sem-hash-fonte-nao-aprova` (#8) — `hash_fonte` ausente ⇒ `NAO_EXERCITADO`.
- `runtime-hash-divergente-indeterminado` (#8) — `hash_fonte != fonte_sha` ⇒ `INDETERMINADO`.
- `rotulo-ausente-nao-vira-runtime` (#8) — sem rótulo não vira runtime.
- `contrato-procedencia-classe` — procedência no enum e classe coerente.
- `evidencia-vem-do-artefato-lido` (#9) — evidência = artefato lido, nunca o CSV do esperado.
- `runtime-verde-integra-decisao` — rodada **estável** (7 OK com evidência) fecha `OK`/`ok_vinculantes=7` no `decisao.py`.
- `runtime-sem-evidencia-integra-decisao` (#9) — rodada sem artefato não fica verde no módulo **nem** no ciclo.
- `lacuna-coleta-vai-pra-fila` — lacuna técnica vira falha automática, **0 pendências humanas**.

## Evidência (execução real, offline)

```
$ python tools/automacao/cenarios/test_tooltips_shrines.py
TOTAL|rodaram=21 reprovaram=0 nao_rodaram=0                          exit 0

$ python tools/automacao/cenarios/test_tooltips_shrines.py --isca
ISCA|OK|defeito plantado detectado: N1-dois-personagens-somados: ...  exit 0

$ python tools/automacao/cenarios/tooltips_shrines.py \
      --observacoes tools/automacao/cenarios/shrines-observacoes.exemplo.json
OK=7 ... com prova runtime: 0  · exit=2                              (fixture NUNCA verde)

$ python tools/testes/roda_testes.py --puros    -> 85/85, VERDE, exit 0
$ python tools/automacao/ciclo/test_decisao.py  -> 117/117 TUDO OK, exit 0   (consumidor intacto)
```

Repros do CIC-4R, agora **fechados** (script de verificação offline em scratch Hermes):

| repro | antes (CIC-4R) | agora |
|---|---|---|
| E3 runtime, identidade ok, sem `hash_fonte` | OK / `prova_runtime=true` | **NAO_EXERCITADO** / false |
| F rótulo runtime sintético, evidência vazia | módulo OK · decisão `OK_VINCULANTE` | módulo NAO_EXERCITADO · decisão `ok_vinculantes=0`, 7 falhas |
| H rodada completa **sem** evidência | módulo 7 OK · decisão REPROVADO (mismatch) | módulo **0 OK** · decisão NAO_EXERCITADO (**módulo == ciclo**) |
| J regressão BUG-34 sem evidência | OK com `evidencia=[]` | **NAO_EXERCITADO**, `evidencia=[]` |

Controle positivo (rodada estável com evidência + identidade) fecha `OK_VINCULANTE` ×7 no
`decisao.py` — não é um avaliador que nunca aprova. Controles negativos N1–N7 seguem 7/7 corretos.

## Hashes (sha256, bytes atuais)

```
c4e0a837af3e55d97aad9f0e395e36956788d62b88066cc85f9178f2ac73b4f5  tools/automacao/cenarios/tooltips_shrines.py
dcc21f07f8d2f505fbfc4f2935c2be6beb17c3ae693d43f227db1e9d79fe69e5  tools/automacao/cenarios/test_tooltips_shrines.py
6ef205481d874a3587d07ca433b41565eef29f3323a14259c978cde263f77c52  tools/automacao/cenarios/shrines-casos.json            (inalterado)
ae27c2a363f9d53834da8477131c2d490bfbb596c633f19bac4869d83da97364  tools/automacao/cenarios/shrines-controle-negativo.json (inalterado)
969b1c693956ee1c3f2de4a3ccb42a9724f502f623d91bd71030867a5e23cdec  tools/automacao/cenarios/shrines-observacoes.exemplo.json (inalterado)
```

HEAD `f526fe9` (branch `ci-validate-test`) · rodada offline `2026-10-05 ~18:48`.

## Limites / o que NÃO foi feito

- **Runtime REAL não exercitado:** nenhum jogo aberto, nenhum objeto vivo lido, nenhuma `fonte_sha`/
  `dll_sha` de sessão em jogo. Toda prova aqui é offline; o caminho AUT-4/AUT-6 vivo continua
  **NÃO EXERCITADO** por decisão da rodada.
- **Ponto de integração (pai):** o contrato agora exige que a observação declare o **artefato lido**
  (`evidencia`, ou `objeto` que resolva para arquivo). O normalizador do coletor CIC-5 **não emite**
  `evidencia` nas observações normalizadas — até o coletor/manifest anexar o artefato (log/objeto) da
  rodada, critérios de runtime saem `NAO_EXERCITADO` (fail-closed, correto). Ligar isso é do pai.
- **`decisao.py` (CIC-2) foi atualizado em paralelo** por outro agente (rótulo técnico explícito +
  cadeia runtime + manifest); a saída do CIC-4 foi **fiacada contra a versão atual** (testes de
  integração verdes). Não editei `decisao.py`/`ciclo.py`/`rstv.py`.
- Não executei build, jogo, install, save, commit, push ou publicação.
