# CIC-4 — entrega: avaliador executável de tooltips/shrines por personagem (`t_6dc6484b`)

**Escopo (CICLO-VALIDACAO-escopo.md §Divisão exclusiva):** `tools/automacao/cenarios/tooltips_shrines.py`,
`test_tooltips_shrines.py`, dados `shrines-*.json` e este documento. Não toca produto, probe, bancada,
`checa_shrines` nem arquivos compartilhados. Rodada **OFFLINE**: nenhum build, jogo, install, save,
commit, push ou publicação.

> Retomada após a revisão independente **CIC-4R** (`t_fa36c892`) e a **CIC-5R** (2ª passada). O trabalho
> desta rodada foi **reconferir a premissa no disco** e corrigir **somente** (a) o bloqueio funcional
> **#8** e (b) a **integração de evidência/enum/feed com a coleta real** (achado **R-1**), sem criar
> oráculos novos. `PROCESSO-REVISAO.md`/`.hermes.md` exigem revisão independente; nada aqui é aceite
> humano nem DoD.

## Reconferência do estado no disco

O `CIC-4-correcao.md` (rodada anterior, mesma tarefa) já havia corrigido #8/#9 — os hashes do módulo
batiam (`c4e0a837…`). **Reconferi por execução própria** (não por leitura do relatório):

- **#8 (rótulo runtime auto-declarado / hash opcional aprova sem prova): CORRIGIDO.** Rótulo `runtime`
  sozinho não fecha: exige cadeia (`sessao` + hash de build confrontado com a identidade + evidência do
  artefato lido). Procedência ausente/desconhecida vira `execucao` (nunca `runtime` por default).
- **#9 (evidência fingida): CORRIGIDO.** `evidencia` sai do artefato realmente lido; sem artefato ⇒
  `NAO_EXERCITADO`. Enum de procedência `execucao`/`runtime`/`fixture` correto (sem `offline`).
- **R-1 (integração com a coleta real): CORRIGIDO nesta rodada** — ver abaixo.

## R-1 — `hash_fonte` (coletor) é o sha da **DLL**; o adaptador comparava com `fonte_sha`

O coletor CIC-5 grava `hash_fonte` = sha256 da **DLL** do probe (`coletor.derivar_config`/
`provar_atualidade`); o CIC-3 já alinhou (`rstv._ALIAS_HASH = (("hash_fonte","dll_sha"),("hash_dll","dll_sha"))`).
O CIC-4 **ainda** comparava `hash_fonte` com `fonte_sha` ⇒ **toda** observação runtime legítima saía
`INDETERMINADO` ("observação de OUTRA build"). O `CIC-5R` §R-1 listava exatamente
`tooltips_shrines._cadeia_runtime` l.414-417.

**Correção (só o arquivo desta frente):** `hash_fonte`/`hash_dll` da observação passam a ser a **cadeia da
DLL** (chave canônica `dll_sha`), confrontada com a identidade; `fonte_sha`/`dll_sha` explícitos também
contam; hash divergente ⇒ `INDETERMINADO`, hash que a identidade não conhece ⇒ `NAO_EXERCITADO`. O
critério passou a **propagar `fonte_sha`/`dll_sha`/`config_sha` DA IDENTIDADE** (+ `sessao` da observação),
para o `decisao.py` reconferir (contrato positivo de runtime). **Mesmo alias do CIC-3/coletor** — não
inventei contrato; alinhei ao que a CIC-3 e o coletor já definiram.

## O que foi entregue

| arquivo | papel |
|---|---|
| `tools/automacao/cenarios/tooltips_shrines.py` | avaliador `avaliar(observacoes, identidade) -> criterios` + CLI real |
| `tools/automacao/cenarios/test_tooltips_shrines.py` | testes offline (**24 casos**, inclui os 3 RED→GREEN de R-1) + ISCA (prova de fogo do próprio teste) |
| `tools/automacao/cenarios/shrines-casos.json` | cenários (o esperado **não** é digitado: o módulo o calcula) |
| `tools/automacao/cenarios/shrines-observacoes.exemplo.json` | observações FIXTURE (trechos verbatim de logs versionados) |
| `tools/automacao/cenarios/shrines-controle-negativo.json` | 7 defeitos plantados com o estado que o avaliador TEM de devolver |

## Contrato de integração (v1) — o que o ciclo consome

`avaliar(observacoes, identidade)` devolve uma **lista de critérios**. Cada critério traz os campos do
contrato: `id, mod, estado (OK/REPROVADO/NAO_EXERCITADO/INDETERMINADO), classe (offline/runtime),
procedencia (execucao/runtime/fixture), esperado, observado, evidencia (lista de caminhos), motivo,
tarefa_origem` — mais campos rastreáveis: `prova_runtime` (bool), `sessao`, `fonte_sha`, `dll_sha` e
(nos casos que o pedem) `personagem`/`alvo`/`tipo`/`regressao_de`/`reabre_bug`.

Regras duras aplicadas (verificadas por teste):

- **Runtime nunca vira OK sem identidade suficiente.** Falta `fonte_sha`/`dll_sha` → `NAO_EXERCITADO`
  com o motivo nomeando a lacuna (`N3`). O hash de build declarado pela observação (`hash_fonte`/
  `hash_dll` = sha da **DLL** do coletor) é confrontado com a identidade: `fonte_sha` casando com
  `dll_sha` **não** fecha (`N4` → `INDETERMINADO`); a chave correta é `dll_sha` (**R-1**).
- **Ausência não é aprovação.** Sem observação, sem campo, ou sem linha na tabela gerada →
  `NAO_EXERCITADO`, nunca OK (`N5`).
- **Fixture não prova runtime.** Todo critério de fixture sai com `prova_runtime=False` e o CLI/`exit_de`
  devolve **2** no caminho só-fixture, nunca 0.
- **Lacuna técnica não é pedido humano.** Os motivos de `NAO_EXERCITADO` citam o próximo passo
  TÉCNICO (coletar/logar); o teste `sem-pedido-humano` recusa o contrário.

## Cenários cobertos

1. **Dois personagens na MESMA aura (receptor / source).** `S-dois-personagens-rogue` (ChkRA bonus 0,
   Raven bonus 100) e `S-dois-personagens-dwarven` (ChkDW0/20/100). A linha é **por personagem**: cada
   um conta a aura **uma vez** com o **próprio** bonus — nunca somada entre personagens. O esperado de
   cada um sai da tabela gerada (eixo `Target`). Defeitos pegos: soma entre personagens (`N1`) e
   bonus do próprio personagem ignorado (`N2`).
2. **Feed vs tooltip.** O valor do **FEED** (marcador de log `[Shrine RV-23] RV-31 acumulado`) e o da
   **TOOLTIP** (texto renderizado) têm de bater entre si e com o esperado independente. Divergência →
   `REPROVADO` (`N6`). Faltando uma superfície, o que falta sai `NAO_EXERCITADO`.
3. **Aura de perigo (Flame).** `S-perigo-flame`: o dano por alvo é reconferido pelo **oráculo**
   (`regras_shrine.dano`) com o eixo `Source` do shrine (bonus 0, RV-30) e a `%` por tipo da tabela de
   percentuais. Observado `MaxHealth=200 tipo=Fodder dano=28` → esperado 28 (0,14 × 200).
4. **Regressão BUG-34 (Armor) — somente.** `S-regressao-bug34-armor`: o aceite humano de 05/10
   (KANBAN.md, BUG-34) **não é reaberto**. O único critério é que a nota de Armor (`blocks damage`)
   **não volte ao feed**. Um vazamento é `REPROVADO` de regressão com `reabre_bug: false` (`N7`), não
   a reabertura do diagnóstico.

## Reuso (nada de fórmula copiada do mod)

- **Leitura:** `tools/checa_shrines.py` é importado como módulo — `coleta()` lê os marcadores, e
  `coleta()` lê os marcadores, e `RE_ITEM`/`RE_ITEM_MANA`/`ROTULO_ATRIBUTO` parseiam os itens da tooltip.
- **Esperado independente e rastreável:** `tools/dados/shrines-esperado.csv` /
  `shrines-percentuais.csv` (GERADAS por `tools/gera_shrines_esperado.py` da fonte da verdade — censo
  `docs/cobertura/status.csv` e `resources.assets`) via `checa_shrines.esperado_buff`; e
  `tools/testes/regras_shrine.py` (o oráculo Python, segunda implementação que tem de bater com o
  oráculo C#) para Dwarven e para o dano de Decay/Flame. Cada critério carrega a **fonte**
  (`arquivo:linha` / `assets@offset`) no campo `esperado` — o teste `esperado-rastreavel` exige isso.

## Adaptação pequena e lacuna de runtime (declaradas — sem inventar emissão)

O coletor AUT-4 lê **objetos vivos** (tooltip/TMP): ele **não emite** as linhas `[Shrine RV-23]`, que
são o **log do próprio mod** consumido por `checa_shrines`. Por isso o adaptador aceita duas formas,
ambas reais, sem inventar formato para o coletor:

- **(a)** observação AUT-4 normalizada/consolidada — `campos.texto_renderizado`, `campos.personagem`,
  `lacunas` → a superfície **TOOLTIP**;
- **(b)** `feed`: o texto do log com os marcadores → a superfície **FEED**.

**Lacuna de runtime declarada:** o caminho runtime NÃO foi exercitado nesta rodada (nenhum jogo). A
leitura do objeto vivo pelo AUT-4 continua **NÃO EXERCITADA**, e é por isso que todo critério de
runtime fora de fixture sai `NAO_EXERCITADO` — a lacuna é **técnica** (coletar), não um pedido ao dono.

## Evidência (execução real, offline)

Comandos e saídas reais (exit codes literais):

- `python tools/automacao/cenarios/test_tooltips_shrines.py` → **exit 0** —
  `TOTAL|rodaram=24 reprovaram=0 nao_rodaram=0` (inclui os 3 casos RED→GREEN de R-1:
  `hash-fonte-dll-casa-identidade`, `hash-fonte-source-divergente-nao-aprova`,
  `criterio-propaga-fonte-e-dll-da-identidade` — vistos FALHANDO antes da correção).
- `... test_tooltips_shrines.py --isca` → **exit 0** — `ISCA|OK|defeito plantado detectado: N1…`
  (a isca troca a espera de `N1`; a comparação não é vácua).
- `runtime-completo-verde` (caso da suíte) → **7/7 OK, `com_prova_runtime=7`, exit 0**.
- `python tools/automacao/cenarios/tooltips_shrines.py --observacoes .../shrines-observacoes.exemplo.json`
  → **exit 2** — `OK=7`, `com prova runtime: 0` (fixture **não** é verde).
- **Banca independente (Hermes scratch, FORA do repo)** `…/cic4_resume/verifica.py` → **exit 0 ·
  `RESULTADO|TUDO OK`** — exercita o repro-F do CIC-4R, E3 (sem `hash_fonte`), rótulo ausente ⇒ `execucao`,
  cadeia completa ⇒ OK + integração `decisao`, e **R-1** (`hash_fonte`=sha da DLL ⇒ **OK/prova_runtime**,
  antes `INDETERMINADO`).

Controle negativo: 7/7 defeitos plantados devolvem o estado esperado
(`N1` REPROVADO, `N2` REPROVADO, `N3` NAO_EXERCITADO, `N4` INDETERMINADO, `N5` NAO_EXERCITADO,
`N6` REPROVADO, `N7` REPROVADO).

Hashes SHA-256 (bytes atuais):

```
df3258e841f7ca9f3f81f41b277f69c63c08b0d4308dcd7c4412afff9b2ddbef  tools/automacao/cenarios/tooltips_shrines.py
0b6436783a9c779d37c970a88af34b3af4d5d365b73b70f88e74bb698b1ced95  tools/automacao/cenarios/test_tooltips_shrines.py
6ef205481d874a3587d07ca433b41565eef29f3323a14259c978cde263f77c52  tools/automacao/cenarios/shrines-casos.json             (inalterado)
969b1c693956ee1c3f2de4a3ccb42a9724f502f623d91bd71030867a5e23cdec  tools/automacao/cenarios/shrines-observacoes.exemplo.json (inalterado)
0d60f709d4252d9ff59a08bb1f5e2d4c0697b128601c60f0e538bde57ea6857a  tools/automacao/cenarios/shrines-controle-negativo.json   (só o texto de N4)
```

## Residual humano e o que NÃO foi feito

- **Reduz revisão humana residual:** o que era transcrição manual de número de shrine passa a ser
  comparação automática contra a tabela gerada; sobra ao olho humano só o que exige tela/jogo
  (o RV-49, as auras de perigo em campo, e a leitura visual final — limitações já declaradas em
  `tools/checa_shrines.py`).
- **Preserva o texto manual do dono / não reabre bug:** o critério de Armor é **só regressão**; o
  aceite humano do BUG-34 segue válido (`reabre_bug: false`).
- **Fora do escopo desta rodada:** builds, jogo, install, save, commit, push e publicação — nada
  disso foi executado. O caminho runtime do AUT-4 continua **NÃO EXERCITADO**.
- **`CIC-4-correcao.md`** (rodada anterior) declara a cadeia como `hash_fonte == fonte_sha`; essa linha
  foi **superada por R-1** (alinhamento confirmado com CIC-3/coletor). Não editei aquele arquivo (fora
  do escopo desta frente).
- **Alvos móveis nesta sessão:** `tools/automacao/ciclo/decisao.py` e `tools/automacao/cenarios/rstv.py`
  foram alterados **por outras frentes** durante a rodada; a integração do CIC-4 foi fiada contra a
  versão corrente e os testes de integração (`runtime-verde-integra-decisao`) passam. Não editei nenhum.
- **Não alterado:** `tools/checa_shrines.py`, `tools/testes/regras_shrine.py`,
  `tools/gera_shrines_esperado.py`, `tools/dados/**`, `tools/automacao/runtime/**`,
  `tools/automacao/ciclo/decisao.py`, `tools/automacao/cenarios/rstv.py`, produto, probe e bancada —
  todos lidos/reusados, nenhum editado. Nenhum secundário novo inventado.
