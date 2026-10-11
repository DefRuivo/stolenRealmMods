# KIT-10R2 — Revisao independente (rodada 2, lente EXECUTION) — veredito: REQUEST_CHANGES

- Cartao: `t_bbad760d` (KIT-10). Implementador desta rodada: **run655** (KIT-10F). Revisor: **run657**, instancia nova.
- Rodada 2 (1 `changes_requested` previo — run651). Lente da rodada 2: **Execution** — tudo abaixo foi RODADO.
- Nenhum arquivo do implementador foi editado por este revisor.

## 1. Correcoes pedidas na rodada 1 — REPRODUZIDAS E APROVADAS

O proprio probe que ACHOU os defeitos (`scratch/kit/KIT-10R-run651/probe_revisor.py`) foi reexecutado:

```
P2 estagio=banana           -> NAO_EXERCITADO False   (era OK True)
P3 worship sem itens        -> NAO_EXERCITADO False   (era OK True)
P3b worship item ausente    -> NAO_EXERCITADO False   (era OK True)
P4 buff fora da tabela      -> NAO_EXERCITADO False   (era OK True)
P5 alvo fora da tabela      -> NAO_EXERCITADO False   (inalterado)
```
F1 (`elif estagio not in ESTAGIOS_DE_EVENTO` -> NAO_EXERCITADO), F2 (`faltando` para aura viva sem
item), F3 (`lacuna` para buff fora da tabela/contrib ausente): **presentes e eficazes** no fonte
(`kit10_cenarios.py` l.420-431 / l.355-375 / l.284-294). Positivos intactos; RED novo 3/3 load-bearing.

## 2. Veredito por criterio

| # | Criterio do cartao | Veredito |
|---|---|---|
| 1 | Relacionar tooltip/contexto/dano e fonte/receptor corretos em shrines | **REPROVADO** (F5, F6) |
| 2 | Preservar Worship confirmado; nao remover o dobro | **PASSOU** (R6 OK / R7 REPROVADO quando o dobro some; RED B load-bearing) |
| 3 | BetterStats base SavedMap/final | **PASSOU** (reuso AUT-7 28/28; estruturais OK) |
| 4 | BetterFont/BetterCombatText por EVENTO, nao prefab de boot | **PASSOU** no aspecto C (R4 evento OK/True; R5 prefab REPROVADO); BetterFont proprio herda a lacuna F4 (outra frente) |
| 5 | Debugger contrato sem truncar | **PASSOU** (D-ok / D-pipe / D-truncado; RED D) |
| 6 | Criterios independentes, varias superficies e controles negativos | **PARCIAL** — falta controle para F5/F6 |
| 7 | Campos apenas necessarios por caso; runtime ausente nao recebe OK | **REPROVADO** (F5, F6) |
| 8 | Nao modificar mods/gameplay | **PASSOU** (`git status`: frente so criou `tools/automacao/kit10/` + `docs/automacao/KIT-10*`) |
| 9 | Reuso AUT-6/7, CIC-4, checa_shrines com identidade atual | **PASSOU** (CIC-4 28/28 exit0; AUT-7 reuso exit0) |

## 3. Achados NOVOS (impedem aprovar)

### F5 (ALTO) — `dano_observado` ausente ainda vira OK/prova_runtime=True
`_asp_contexto_dano`: `dano_observado` nao entra em guarda nenhuma. Com `fonte_bonus=0`, sem
`aura_buff` e sem `dano_observado`, `defeito=[]` e o fechamento promove a `OK/True`; o `motivo`
afirma "dano do ground effect bate com o oraculo" **sem nenhum dano medido**.
Prova (probe proprio, `scratch/kit/KIT-10R2-run657/probe_revisor3.py`):
```
R8  dano AUSENTE              -> OK True   ('dano do ground effect bate com o oraculo ...')
R9  dano AUSENTE + buff medido-> OK True
R10 dano ERRADO (CONTROLE)    -> REPROVADO False  <-- a checagem funciona QUANDO o dano existe
```
Violacao direta de "runtime ausente nao recebe OK". **Correcao minima:** `dano_observado` ausente
-> `NAO_EXERCITADO` (nunca OK) + controle negativo novo na suite + guarda RED.

### F6 (MEDIO) — `receptor_bonus` ausente assume 0 e a afirmacao do eixo Target fica vazia
`receptor = float(_campo(obs,"receptor_bonus") or 0)`. Ausente == 0 -> com `contrib_observada`
coerente com bonus 0 fecha `OK/True` e afirma "a tooltip de buff le o bonus do RECEPTOR (eixo
Target)". Com bonus 0, leitura por `Source` e por `Target` dao o MESMO valor: o eixo (o ponto do
aspecto A) **nao foi exercitado**.
Prova: `R3 receptor ausente -> OK True`. **Correcao minima:** `aura_buff` declarado + `receptor_bonus`
ausente -> `NAO_EXERCITADO`.

### F7 (BAIXO) — `fonte_bonus` ausente vira REPROVADO (classificacao)
`R2 fonte ausente -> REPROVADO False`: campo nao medido rotulado como defeito DETECTADO. Nao e'
falso-OK, mas confunde FALHOU com NAO_EXERCITADO, que o cartao manda distinguir.

## 4. F4 — redeclaracao (nao atribuida ao KIT-10)
`python tools/automacao/estilo/test_estilo_atributos.py` na arvore viva: **exit 1**,
`total: 28 | falhas: 1` — "medicao offline REAL: ... nao deixa mod sem familia de teste"
(BetterFont/mod sem familia; causa de outra frente). O handoff run655 declara exit 1 corretamente
em `KIT-10-entrega-final.md`; a supersessao do `KIT-10-entrega.md` (que dizia exit 0) foi feita. **OK.**

## 5. Execucoes reais desta rodada (exit)
- suite `test_kit10_cenarios.py`: **24/24 exit 0**; `--isca`: **exit 0**
- probe run651 reexecutado: P2/P3/P3b/P4 -> NAO_EXERCITADO/False; **exit 0**
- RED antigo 5/5 **exit 0**; RED novo 3/3 **exit 0**
- CLI fixture: **exit 2**, OK=0, com_prova_runtime=0
- reuso CIC-4 `test_tooltips_shrines.py`: **28/28 exit 0**
- `test_estilo_atributos.py`: **exit 1** (lacuna externa, declarada)
- travas: check_segredos / check_padroes_segredo / check_dupes / audita_docs **4/4 exit 0**

## 6. Proxima acao exigida do implementador
Corrigir F5 e F6 (F7 junto, e' barato), reexecutar a prova-RED das guardas novas e pedir nova revisao
independente NESTE cartao. Nao enfraquecer nenhuma guarda existente. Prova de runtime/UIUX/build/
deploy/pacote/publicacao: **NAO_EXERCITADO** (fora do escopo offline autorizado).

## Artefatos
- probes: `scratch/kit/KIT-10R2-run657/probe_revisor2.py`, `probe_revisor3.py`
- saida estilo: `scratch/kit/KIT-10R2-run657-estilo.txt`
- partes: `docs/automacao/KIT-10R2-parte01.md`, `KIT-10R2-parte02.md`
