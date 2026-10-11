# KIT-10 — parte 02: execução (módulo, testes, prova RED) e resultados reais

Checkpoint 02 do cartão `t_bbad760d`. Tudo OFFLINE; nenhum jogo/build/deploy/install/save/commit.

## O que foi construído (arquivos NOVOS desta frente)

| Arquivo | Papel |
| --- | --- |
| `tools/automacao/kit10/kit10_cenarios.py` | avaliador KIT-10: reusa CIC-4 + AUT-7 e acrescenta 4 aspectos |
| `tools/automacao/kit10/test_kit10_cenarios.py` | 17 casos (positivos, controles negativos, isca) |
| `scratch/kit/KIT-10-run/prova_red_kit10.py` | driver RED durável (5 mutações, uma por guarda) |
| `scratch/kit/KIT-10-run/{fixture.json,saida.json}` | prova da CLI em fixture (exit 2) |

Nada de produto/mod/probe/gameplay foi tocado. Os 4 módulos REUSADOS por import não foram editados.

## Reuso (fail-closed, por import)

`kit10_cenarios.avaliar(obs, ident)` = `tooltips_shrines.avaliar` (CIC-4) + `estilo_atributos.avaliar`
(AUT-7) + 4 aspectos novos. As fórmulas do esperado vêm do ORÁCULO (`regras_shrine`), das TABELAS
GERADAS (`shrines-esperado.csv`/`shrines-percentuais.csv`), do contrato do dump (`regras_debugger` →
`tools/census.py`) e das superfícies do BCT (`regras_bct`) — nenhuma fórmula copiada.

## Os 4 aspectos novos (o que faltava)

| id | O que prova | Defeito pego (controle negativo) |
| --- | --- | --- |
| `KIT-10/shrines/contexto-dano-fonte-receptor` | ground effect lê o dano no eixo `Source` (bonus 0); a tooltip de BUFF lê o bonus do RECEPTOR (eixo `Target`) | `fonte_bonus≠0` (o defeito do `Source` injetado, RV-34) e dano escalando com o receptor |
| `KIT-10/shrines/worship-dobro-preservado` | comportamento CONFIRMADO: aura de GATILHO conta por instância (DWA-2); aura de ATRIBUTO 1× (RV-46) | instância de gatilho colapsada em 1 item ("dobro removido") |
| `KIT-10/estilo/por-evento-nao-boot` | superfície canônica do BCT lida no EVENTO (`estagio`+`evento_id`), nunca no prefab de boot | `estagio=boot` |
| `KIT-10/debugger/sem-truncar` | contrato do dump: `desc=` por último, sem `\|` em valor, `desc` ancorada no fim | valor com `\|`; campo depois do `desc` |

## Execuções reais (exit codes literais)

- `python tools/automacao/kit10/test_kit10_cenarios.py` → `TOTAL|rodaram=17 reprovaram=0 nao_rodaram=0` · **exit 0**
- `python tools/automacao/kit10/test_kit10_cenarios.py --isca` → `ISCA|OK|defeito plantado detectado` · **exit 0**
- `python scratch/kit/KIT-10-run/prova_red_kit10.py` → `PROVA-RED|PASSOU|5 mutacoes|todas as guardas load-bearing` · **exit 0** (mutante temporário removido; o fonte original nunca é tocado)
- `python tools/automacao/kit10/kit10_cenarios.py --observacoes scratch/kit/KIT-10-run/fixture.json` → `OK=0 ... com prova runtime: 0 · exit=2` (fixture NÃO é verde)
- Reuso intacto: `test_tooltips_shrines.py` exit 0; `test_estilo_atributos.py` exit 0
- Travas do repo: `check_segredos.py` / `check_padroes_segredo.py` / `check_dupes.py` / `audita_docs.py` — todos exit 0

## Achado do RED (guarda load-bearing)

Cada mutação neutraliza UMA guarda e o defeito ESCAPA (`neutralizado=NAO_EXERCITADO`), provando que
a guarda é quem pega o defeito — não a fonte:

```
PROVA-RED|OK|A-contexto-fonte|original=REPROVADO neutralizado=NAO_EXERCITADO
PROVA-RED|OK|A-contexto-dano|original=REPROVADO neutralizado=NAO_EXERCITADO
PROVA-RED|OK|B-dobro|original=REPROVADO neutralizado=NAO_EXERCITADO
PROVA-RED|OK|C-evento|original=REPROVADO neutralizado=NAO_EXERCITADO
PROVA-RED|OK|D-dump|original=REPROVADO neutralizado=NAO_EXERCITADO
```

## Contrato respeitado

- **Runtime ausente não recebe OK**: sem identidade suficiente + cadeia + evidência do artefato
  lido, o fechamento (AUT-7 `_fecha`/`_vinculo_obs`) rebaixa para `NAO_EXERCITADO`
  (`prova_runtime=False`); fixture nunca é verde (exit 2).
- **Defeito continua REPROVADO mesmo em fixture** — é assim que o controle negativo prova a regra.
- **Lacuna técnica, não pedido humano**: os `NAO_EXERCITADO` citam o próximo passo TÉCNICO
  (`tipo_pendencia=coleta_tecnica`, `autorizacao_necessaria=False`).

> Checkpoint 02. Próximo bloco: fechar `KIT-10-entrega.md` com resumo, caminhos e hashes.
