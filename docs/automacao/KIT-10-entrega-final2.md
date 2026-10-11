# KIT-10 — entrega FINAL2 (rodada run659): correção do KIT-10R2 (F5/F6/F7)

Tarefa: t_bbad760d. Implementador: run659 (perfil default, instância nova) ≠ revisores run651/run657.
Escopo OFFLINE. Nenhum mod/gameplay/probe de outra frente tocado. Sem `git add`/commit.

## O que mudou

Arquivo único de produção: `tools/automacao/kit10/kit10_cenarios.py` (aspecto A `_asp_contexto_dano`).
Guardas novas de "campo NÃO MEDIDO → NAO_EXERCITADO" (nunca OK):

- **F5** `dano_observado` ausente → lacuna (antes: o conjunto fechava `OK/prova_runtime=True`
  afirmando que o dano "bate com o oráculo" SEM nenhum dano medido).
- **F6** `receptor_bonus` ausente/**= 0** → lacuna (o eixo `Target` não é exercitado: com bônus 0
  os eixos `Source` e `Target` coincidem). A acusação da tooltip foi gateada por
  `receptor_exercitado` para não rotular como FALHOU um esperado que dependeria de valor não medido.
- **F7** `fonte_bonus` ausente → lacuna (campo NÃO MEDIDO ≠ FALHOU); só `! = 0` medido vira defeito RV-34.
- **Extras (mesma classe)**: `aura_buff` ausente → a metade "tooltip do RECEPTOR" do aspecto NÃO foi
  medida → lacuna (o OK do aspecto afirma as DUAS leituras). `lacunas` agora é lista; defeito MEDIDO
  continua vencendo lacuna (o controle R10 do revisor segue `REPROVADO`).

Arquivo de teste: `tools/automacao/kit10/test_kit10_cenarios.py` — +4 guardas (G4-dano, G5-receptor,
G6-fonte, G7-buff) no agregado `_roda_falsos_ok` (agora 9) e +4 testes individuais em `CASOS` (agora 28).

## Provas reais (com exit e caminho)

| execução | resultado | caminho/saída |
|---|---|---|
| suíte KIT-10 | **28/28 PASSOU, exit 0** | `tools/automacao/kit10/test_kit10_cenarios.py` |
| `--isca` | `ISCA\|OK\|defeito plantado detectado`, exit 0 | idem |
| prova-RED novas guardas | **PROVA-RED\|PASSOU\|7 mutacoes**, exit 0 | `scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py` |
| probe do revisor r1 | P2/P3/P3b/P4/P5 → NAO_EXERCITADO/False, exit 0 | `scratch/kit/KIT-10R-run651/probe_revisor.py` |
| probe do revisor r2 | R1 OK/True; R2/R3/R8/R9 NAO_EXERCITADO/False; R10 REPROVADO, exit 0 | `scratch/kit/KIT-10-run659-probe-revisor.txt` |
| CLI em fixture | exit 2, `OK=0, NAO_EXERCITADO=19`, prova_runtime=0 | `scratch/kit/KIT-10-run/fixture.json` |
| reuso CIC-4 | 28/28 exit 0 | `tools/automacao/cenarios/test_tooltips_shrines.py` |
| travas do repo | 4/4 exit 0 | check_segredos / check_padroes_segredo / check_dupes / audita_docs |
| estilo (F4) | **exit 0** (`total: 28 | falhas: 0`, "TUDO OK") | `scratch/kit/KIT-10-run659-estilo.txt` |

## Hashes (sha256)

- `tools/automacao/kit10/kit10_cenarios.py` = `8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092`
- `tools/automacao/kit10/test_kit10_cenarios.py` = `6cc5003e0d9facd42cf967b2da480216243b6d902376f5fc20d9c49d9e8db6e2`
- `scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py` = `aa9f232b78b0e4cda8ca6de63bcda417cb1b5c79b635ad6235151177c834c6ff`

## Lacunas e limites (não mascarados)

- **Robustez do driver RED (corrigido nesta rodada)**: a 1ª versão reusava um único nome de arquivo
  mutante na mesma pasta; o `__pycache__` reaproveitava o `.pyc` de um mutante ANTERIOR (mesmo
  tamanho+mtime) e o F5 saía `NAO_EXERCITADO` **falso**. Corrigido com `sys.dont_write_bytecode=True`
  e nome de arquivo único por probe; depois disso o driver passa **3/3 vezes** (7/7). Registrado para
  o revisor não confundir o artefato.
- **F4 (discrepância de árvore viva)**: `test_estilo_atributos.py` medido nesta rodada = **exit 0**;
  o `exit 1` declarado no run655/run657 era estado transitório de OUTRA frente (escritores
  concorrentes no mod BetterFont). O KIT-10 não toca esse mod nem a família `t_*`. Redeclarado aqui.
- Driver RED da rodada 1 **superado** pela renomeação `lacuna`→`lacunas` (G3-contrib sai
  `trecho nao encontrado`); coberto pelo driver novo (ver `KIT-10-parte07.md`).
- `runtime / UIUX / desempenho / build / deploy / pacote / publicação` = **NÃO_EXERCITADO**.
- Não substitui os gates humanos KIT-G1/G2/G3/G4, aceite humano do DoD nem gates de publicação.
- Revisão independente **obrigatória** (implementador ≠ revisor) — pedida via `kanban_request_review`.
