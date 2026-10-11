# KIT-10G — parte 06: correção F5/F6/F7 aplicada e provada

## Correções no aspecto A (`_asp_contexto_dano`, `tools/automacao/kit10/kit10_cenarios.py`)

- **F5** `if dano is None:` → lacuna "`dano_observado` ausente: o dano do ground effect NAO foi
  medido". Antes a checagem só rodava `if dano is not None` e o conjunto fechava OK sem medição.
- **F7** `fonte is None` → lacuna (campo NÃO MEDIDO ≠ FALHOU); só `abs(float(fonte)) > 1e-9`
  (medido e não-zero) vira defeito RV-34.
- **F6** campo CRU `receptor_campo` separado de `receptor`; `receptor_exercitado = campo presente
  E ≠ 0`. Ausente/0 → lacuna "o eixo `Target` do RECEPTOR NAO foi exercitado" (com 0, `Source` e
  `Target` coincidem e o eixo não é provado). A acusação da tooltip foi **gateada** por
  `receptor_exercitado`: sem o bônus medido o esperado dependeria de valor não medido (não se
  rotula FALHOU).
- **Extra (mesma classe)**: `aura_buff` ausente → a metade "tooltip do RECEPTOR" do aspecto NÃO
  foi medida → lacuna (o OK do aspecto afirma as DUAS leituras).
- `defeito` e `lacunas` agora são listas; `if defeito: REPROVADO elif lacunas: NAO_EXERCITADO`.
  Defeito MEDIDO continua vencendo lacuna (R10 do revisor segue REPROVADO).

## Provas reais desta rodada

- Suíte `test_kit10_cenarios.py`: **28/28 PASSOU, exit 0** (eram 24; +4 guardas F5/F6/F7+tooltip).
- `--isca`: `ISCA|OK|defeito plantado detectado`, exit 0.
- 4 guardas novas na suíte (G4-dano-ausente, G5-receptor-ausente, G6-fonte-ausente,
  G7-buff-ausente) + 4 testes individuais registrados em `CASOS`.
- **Probe do próprio revisor reexecutado** (`scratch/kit/KIT-10R2-run657/probe_revisor2.py` e
  `probe_revisor3.py`; saída `scratch/kit/KIT-10-run659-probe-revisor.txt`):
  - F5: R8 dano AUSENTE `OK True` → **`NAO_EXERCITADO/False`**; R9 (dano ausente + buff medido)
    idem; R10 (dano errado, controle) segue **REPROVADO**.
  - F6: R3 receptor ausente `OK True` → **`NAO_EXERCITADO/False`**.
  - F7: R2 fonte ausente `REPROVADO` → **`NAO_EXERCITADO/False`**.
  - R1 (positivo) segue **OK/True**; R4/R5/R6/R7 inalterados.

## Próximo bloco

- Prova-RED durável das guardas novas (mutar cada uma → lacuna escapa para OK/True).
- Reexecutar o driver RED da rodada 1 (F1/F2/F3) e o probe da rodada 1 (`probe_revisor.py`).
- CLI em fixture (exit 2, OK=0), reuso CIC-4, travas do repo.
- Fechamento em `KIT-10-entrega-final2.md` + hashes; pedir nova revisão independente.
