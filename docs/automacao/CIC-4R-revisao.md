# CIC-4R — revisão independente do avaliador tooltips/shrines por personagem (`t_fa36c892`)

> **SUPERADO (rodada 3, `docs/automacao/CIC-4R2-revisao.md`, 2026-10-05 ~20:10).** Os vereditos
> abaixo são fieis aos bytes de **18:29** (`c5be25b4…`/`73e04315…`) — que **não** são mais os do
> disco (`df3258e8…`/`0b643678…`, `CIC-4-entrega.md`). Os itens **#8/#9** foram corrigidos
> (`CIC-4-correcao.md`) e o disco ganhou uma variante que falsifica o critério da superfície TOOLTIP.
> Leia o CIC-4R2 como âncora; o texto abaixo fica como registro histórico, **sem edição**.

Revisor: agente diferente do autor (CIC-4, `t_6dc6484b`). Rodada **somente leitura** sobre produto/oráculos/
bancada; as únicas escritas são **este documento** e o scratch de evidência
(`.../hermes/cache/scratch/cic4r/experimento{,2,3}.py`). Nada de build, jogo, save, install, commit,
push ou publicação. Veredito por item, prova literal de ferramenta.

## Estado lido (sha256 dos bytes atuais)

```
c5be25b4f52fcd31d6979b23a10ca62abed0a904a29ffda9121573e351ab4714  tools/automacao/cenarios/tooltips_shrines.py
73e04315c999e1b498f33c11ced3960fff1e784dce099b10deef0c12906b19e5  tools/automacao/cenarios/test_tooltips_shrines.py
6ef205481d874a3587d07ca433b41565eef29f3323a14259c978cde263f77c52  tools/automacao/cenarios/shrines-casos.json
969b1c693956ee1c3f2de4a3ccb42a9724f502f623d91bd71030867a5e23cdec  tools/automacao/cenarios/shrines-observacoes.exemplo.json
ae27c2a363f9d53834da8477131c2d490bfbb596c633f19bac4869d83da97364  tools/automacao/cenarios/shrines-controle-negativo.json
836f2833d2ef50e0ee14aaebe17b551f9ed7f6a09fc029771ffced5c048824ce  tools/dados/shrines-esperado.csv   (gerado; fonte do esperado)
99174e006dd7d70560142012d1d752ce7b43113d68751c7b47f7836929e549b2  tools/dados/shrines-percentuais.csv (gerado; fonte do esperado)
a000cc178b2f93007dbf8c948ca553a1c8e9593e37aca52177bcde82e6900296  tools/checa_shrines.py      (reusado, não editado)
1ef67649463eeab2b113f1423c8c6667ff24b9162c89633608e6c2a51bf9c562  tools/testes/regras_shrine.py (oráculo, não editado)
d58ee0c931fb5efdff08189f48cbb4085a06c0fc03072c9f3fb9dcae83de5dcc  tools/gera_shrines_esperado.py (fonte, não editado)
836b08c811abef6d9a48d0e6258602d74695c3072d673a82f6d9fd1ea608cd48  tools/automacao/ciclo/decisao.py (CIC-2, não editado)
2165df50051113dc53bb984317e25c9f5a3f23edcf4d396d6acffed4bf1565f0  tools/automacao/ciclo/ciclo.py   (CIC-1, não editado)
```
Os 5 hashes do CIC-4 batem **exatamente** com os declarados em `docs/automacao/CIC-4-entrega.md`.

## Veredito por item

| # | item | veredito | prova |
|---|---|---|---|
| 1 | Contrato v1 (campos/estados/classe/procedência) | **OK** | `test ... test_tooltips_shrines.py` → 12/12 PASSOU, exit 0 (`contrato-v1` cobre os 10 campos) |
| 2 | Esperado **independente e rastreável** (não ecoa o log bruto do mod) | **OK** | esperado sai da tabela gerada + oráculo; ver M/B1/N abaixo |
| 3 | Identidade de fonte/DLL | **OK** | sem identidade → `NAO_EXERCITADO`; `hash_fonte`≠`fonte_sha` → `INDETERMINADO` (N3/N4 e E1/E2) |
| 4 | Receptor/source errado com o **mesmo número** | **OK** | C1/C2 REPROVADO; C3 NAO_EXERCITADO |
| 5 | Observação que **mistura dois personagens** | **OK** | D1 REPROVADO (feed×tooltip); L NAO_EXERCITADO (char combinado) |
| 6 | Ausência de dado/identidade **não vira OK** | **OK** | sem observação → 7 NAO_EXERCITADO, exit 2 (I); N5 |
| 7 | Fixture não prova runtime; integração com `decisao.py` | **OK** | fixture → `prova_runtime=False`, CLI exit 2; `decisao.consolidar` → `nao_conta_como_prova=7`, `ok_vinculantes=0`, falha sintética (G) |
| 8 | Rótulo `runtime` **sintético** não pode ser vendido como conclusão | **ACHADO** | F abaixo — módulo dá OK/`prova_runtime=True` e decisão dá `OK_VINCULANTE`/`pronto_para_decisao=True` |
| 9 | Integração: critério de **regressão BUG-34** sem evidência | **ACHADO (menor)** | H abaixo — módulo diz 7 OK, `decisao` REPROVA o mod |
| 10 | BUG-34 somente **regressão**, humano não reaberto | **OK** | `reabre_bug=False`, `regressao_de="BUG-34"`; `positivo-regressao-bug34` + N7 |
| 11 | Lacuna técnica não vira pedido humano | **OK** | `sem-pedido-humano` recusa "pergunt/solicit/peça"; motivos citam passo TÉCNICO |
| 12 | Tabela/fonte/oráculo intactos | **OK** | nenhum hash de `checa_shrines.py`/`regras_shrine.py`/`gera_shrines_esperado.py`/CSV alterado pela rodada |

## Prova do item 2 — esperado independente

- **B1**: feed com valor **99** no `(char,bonus)` correto → `REPROVADO` (o esperado não vem do log):
  `esperado = tools/dados/shrines-esperado.csv (Rogue Aura/DodgeChance bonus=0) <- docs/cobertura/status.csv:402`.
- **M**: cross-check direto com o CSV — `Rogue Aura/DodgeChance` 0→20, 100→40; `Dwarven Aura` 0→20, 20→24,
  100→40; `fonte_base` cita `docs/cobertura/status.csv:NNN` (9 auras de buff) e `resources.assets@offset`
  (Dwarven/Decay/Flame). O gerador (`gera_shrines_esperado.py`, lido) deriva de `status.csv` + `resources.assets`
  e **falha** se faltar fonte — não digita nem lê o log do mod.
- **N** (perigo, oráculo): `ChkGob MaxHealth=200 tipo=Fodder bonus=100 dano=28` → OK (esperado 28 = 0,14×200,
  eixo `Source=0`); `MaxHealth=100 dano=14` → OK; `dano=40` e `dano=5` → REPROVADO (esperado 14). O `MaxHealth`
  é entrada declarada (vem da observação); a **%** e o eixo vêm de `shrines-percentuais.csv` + `regras_shrine.dano`.

## Prova do item 4/5 — personagem certo

- **C1** `char=ChkRA bonus=0 -> Dodge +40%` (valor do source) → `REPROVADO` (esperado 20).
- **C2** `char=Raven bonus=100 -> Dodge +20%` (valor do receptor, = caso N2) → `REPROVADO` (esperado 40).
- **C3** bônus trocados (`ChkRA=100`, `Raven=0`) → **NAO_EXERCITADO** para os dois (o casamento é por
  `(char, bonus)` — `_achar_acumulado`, `tooltips_shrines.py` l.374-380 —, não pelo número).
- **D1** tooltip do `ChkRA` desenhando `+40%` enquanto o feed diz `+20%` → `REPROVADO` (feed×tooltip divergem,
  l.460-466). **L** `char=ChkRA,Raven` → nenhum dos dois casa → NAO_EXERCITADO.

## Prova do item 6/7 — ausência e fixture

- **I**: `avaliar([], {})` → `OK=0, NAO_EXERCITADO=7, com_prova_runtime=0`, `exit_de=2`.
- **G** (fixture → `decisao.consolidar`, identidade suficiente): `nao_conta_como_prova=7`, `ok_vinculantes=0`,
  `falhas_automaticas=1` (`BetterTooltips:sem-prova-vinculante`), `pronto_para_decisao=False`. Fixture **não**
  conta como runtime OK. Controle negativo 7/7 com o estado esperado (K).

## ACHADO #8 — rótulo `runtime` é auto-declarado e vira prova vinculante (repro)

O módulo só olha a **procedência declarada** na observação (`_adaptar_um`, l.184-188: sem `procedencia`,
sem `rotulo_fixture` e sem `evidencia_runtime`, o default é **`runtime`**), e `_decisao_runtime` (l.335-350)
só confere `hash_fonte` **quando ele vem** — observação runtime **sem** `hash_fonte` fecha OK com
`prova_runtime=True` mesmo sem amarrar a observação aos bytes (E3 nesta rodada).

Repro (scratch `experimento*.py`, nenhum jogo rodado, nenhum artefato de runtime criado; o JSON foi
**escrito à mão** com `procedencia:"runtime"`, `hash_fonte = fonte_sha` da rodada e `evidencia` apontando
para arquivos que sempre existem no repo — `shrines-esperado.csv`, `LocalizePatch.cs`, `KANBAN.md`):

```
modulo : {'total':7,'OK':7,'com_prova_runtime':7}  exit=0
decisao: por_mod={'BetterTooltips':'OK'} resumo={'ok_vinculantes':7,'falhas_automaticas':0,
          'pendencias_humanas':0,'nao_conta_como_prova':0}
         pronto_para_decisao=True  "SIM: automacao sem falhas e sem pendencia humana"
```

Ou seja: **hoje**, um conjunto 100% autoral rotulado `runtime` é apresentado como prova vinculante —
`prova_runtime` prova o **rótulo**, não o vivo. Isso viola o requisito "rótulo runtime sintético não deve ser
vendido como conclusão". Mínimo exigível (não é auditoria nova, é o requisito): **declarar** em
`CIC-4-entrega.md`/docstring que a procedência é declarada pelo coletor e que `prova_runtime=True` só vale
com `hash_fonte` presente; o fechamento real exige o instrumento AUT-4 ligado à mesma `fonte_sha`. Endurecer
(hash obrigatório + default de procedência ≠ runtime) **é decisão do dono** — este achado fica registrado com repro.

## ACHADO #9 — o critério de regressão BUG-34 pode reprovar na integração mesmo com o módulo "verde"

`_caso_regressao_feed` (l.554-582) monta a evidência **só** de `obs["evidencia"]`; a observação do caso
`runtime-completo-verde` do teste não traz `evidencia`, então o critério sai `evidencia=[]`. No módulo:
`{'OK':7,'com_prova_runtime':7}`; em `decisao.consolidar` (H):

```
S-regressao-bug34-armor  FALHA_AUTOMATICA  "evidencia/identidade nao fecham: sem evidencia (label OK nao basta)"
por_mod={'BetterTooltips':'REPROVADO'}  ok_vinculantes=6
```

O `decisao.py` está certo (fail-closed); o defeito é a **mismatch**: o caso `runtime-completo-verde` do CIC-4
não garante aprovação no ciclo. Correção: o teste/caso de regressão deve trazer `evidencia` (como a fixture
já faz) — ou registrar em `CIC-4-entrega.md` que `prova_runtime` do módulo ≠ `OK_VINCULANTE` do decisão.

## Travas rodadas (nesta ordem)

- `python tools/automacao/cenarios/test_tooltips_shrines.py` → **exit 0**, 12/12 (`TOTAL|rodaram=12 reprovaram=0`).
- `... test_tooltips_shrines.py --isca` → **exit 0**, `ISCA|OK|defeito plantado detectado: N1...`.
- `python tools/automacao/cenarios/tooltips_shrines.py --observacoes .../shrines-observacoes.exemplo.json`
  → **exit 2**, `OK=7 ... com prova runtime: 0` (fixture não é verde) — idêntico ao declarado.
- `python tools/testes/roda_testes.py --puros` → **exit 0**, `rodaram 85 / passaram 85 / reprovaram 0` (suíte intacta).

## O que esta revisão NÃO confirma (residual humano / runtime)

- O **caminho runtime real (AUT-4/AUT-6)** continua **NÃO EXERCITADO**: nenhum objeto vivo foi lido, nenhuma
  `fonte_sha`/`dll_sha` de sessão em jogo existe. Toda prova de runtime aqui é fixture — por desenho, não é
  conclusão de campo.
- **Leitura visual final** (RV-49, auras de perigo em campo) segue sendo do dono — já declarado em
  `checa_shrines.py` §Limites.
- `decisao.py`/`ciclo.py` foram lidos e exercitados só como **consumidores** do contrato; nenhuma revisão de
  mérito do CIC-1/CIC-2 é feita aqui (têm revisão própria). Observação de fronteira: `NAO_EXERCITADO` de
  `classe=runtime` entra como **autorização humana** no roteiro ("Autorizar UMA frente runtime") — coerente com
  a regra "preparação runtime não autoriza sozinha", mas convém ao pai decidir se lacuna técnica de coleta
  deve ir à fila de agente em vez de autorização.
