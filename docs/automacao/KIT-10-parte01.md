# KIT-10 — parte 01: escopo, inventário de arquivos vivos e plano

Cartão `t_bbad760d` (KIT-10). Pai de gate: `t_01f65801` (KIT-09F) concluído. Filho de revisão já
criado: `t_896796be` (KIT-10R). Perfil `default`. Rodada **OFFLINE**: nenhum jogo/save/perfil/
probe/deploy/publicação/commit. Nenhum mod nem gameplay é alterado nesta tarefa.

## 1. Objetivo (do corpo do cartão)

"Expandir gradualmente depois do RSTV com reuso de AUT-6/7, CIC-4 e oráculos existentes."
Completar os cenários que faltam para: **tooltips** (contexto/dano, fonte×receptor), **shrines**
(axis Source/Target, Worship confirmado), **estilo** (BetterFont/BetterCombatText por EVENTO, não
prefab de boot) e **atributos** (BetterStats base `SavedMap` × final), **Debugger** (contrato sem
truncar texto).

## 2. Critério de aceite (paráfrase do corpo)

1. Relacionar tooltip/contexto/dano e fonte/receptor corretos em shrines.
2. Preservar comportamento **Worship confirmado**; NÃO remover o "dobro" para tornar teste verde.
3. BetterStats: base `SavedMap` / final do motor.
4. BetterFont e BetterCombatText: material/keywords/cores e superfícies **por evento**, não prefab de boot.
5. Debugger: contrato sem truncar texto.
6. Critérios independentes rastreáveis, várias superfícies e **controles negativos**.
7. Completar campos apenas necessários por caso; **runtime ausente NÃO recebe OK**.
8. Não modificar mods/gameplay nesta tarefa.

## 3. Inventário dos arquivos VIVOS que esta frente pode reusar (lidos, não editados)

| Arquivo | Papel atual | Reuso em KIT-10 |
| --- | --- | --- |
| `tools/automacao/cenarios/tooltips_shrines.py` | CIC-4: avaliador tooltips/shrines por personagem (978 l.) | camada a ESTENDER com os cenários que faltam |
| `tools/automacao/cenarios/test_tooltips_shrines.py` | 24 casos + isca (CIC-4) | padrão de teste |
| `tools/automacao/cenarios/shrines-casos.json` | 4 cenários declarativos | base dos cenários novos |
| `tools/checa_shrines.py` | leitura dos marcadores `[Shrine RV-23]` + `esperado_buff` + regexes | importado como módulo (não reescrito) |
| `tools/testes/regras_shrine.py` | oráculo Python (escala/dano) | esperado independente de Dwarven/Decay/Flame |
| `tools/automacao/estilo/estilo_atributos.py` | AUT-7: avalia estilo (BF/BCT/BS/Debugger), offline + runtime | reuso dos avaliadores por mod |
| `tools/testes/regras_bct.py`, `regras_bf_estilo.py`, `regras_debugger.py` | modelos/contratos lidos | esperado independente do estilo |
| `docs/dados/shrines-esperado.csv`, `shrines-percentuais.csv` | tabelas GERADAS (fonte da verdade) | esperado rastreável |
| `tools/automacao/cenarios/kit09.py` | KIT-09/RSTV: critérios pequenos | modelo de estrutura de entregável |

## 4. Lacunas a fechar (mapeadas do corpo)

- **L1 (tooltip/contexto/dano, fonte×receptor):** o eixo `Target`/`Source` do shrine já existe na
  tabela, mas falta o cenário que prova que o dano do ground-effect lê a fonte VAZIA (bonus 0) e a
  tooltip do RECEPTOR lê o bonus DO receptor.
- **L2 (Worship / "dobro"):** existe comportamento confirmado onde a MESMA aura viva conta 1× por
  personagem e o motor soma instâncias (`instancias=`). É preciso um cenário que **preserve** o
  comportamento confirmado e um controle negativo que prova que REMOVER o dobro NÃO pode virar verde.
- **L3 (BetterStats SavedMap/final):** já coberto no offline (estrutural AUT-7), mas a superfície de
  EVENTO (level-up vs ficha) não tem cenário.
- **L4 (BF/BCT por evento):** o avaliador AUT-7 já exige superfícies canônicas, mas falta o controle de
  que a leitura é do EVENTO (level-up/dano) e não do prefab de boot.
- **L5 (Debugger sem truncar):** o contrato `contrato_da_linha` tem limite DECLARADO (valor com " | "
  dentro não é detectado). Falta cenário de controle negativo que mostre o truncamento.

## 5. Plano de execução

1. Ler `RV-19-shrines.md` (Worship, eixo Source/Target) e `regras_shrine.py` para o oráculo.
2. Ler o teste CIC-4 e o `regras_bct.py`/`regras_bf_estilo.py`/`regras_debugger.py`.
3. Escrever o módulo KIT-10 (`tools/automacao/kit10/kit10_cenarios.py`) que REUSA
   `tooltips_shrines.avaliar` e `estilo_atributos.avaliar` e ACRESCENTA os cenários L1–L5 com
   critérios independentes, várias superfícies e controles negativos.
4. Escrever o teste (`test_kit10_cenarios.py`) com casos RED→GREEN + isca; rodar e registrar exit real.
5. Fechar `docs/automacao/KIT-10-entrega.md` com resumo, caminhos e hashes.

## 6. Regras de prova (herdadas)

- Fixture testa o AVALIADOR; NUNCA prova runtime (`prova_runtime=False`, exit 2).
- Ausência ≠ aprovação: sem observação/campo/linha → `NAO_EXERCITADO`, nunca OK.
- Só a cadeia (`sessao` + `fonte_sha`/`dll_sha` confrontados + evidência do artefato lido) fecha OK.
- Um defeito plantado continua `REPROVADO` mesmo com procedência `fixture` (é assim que o controle
  negativo prova a regra).

> Checkpoint 01. Próximo bloco: leitura dirigida dos oráculos e do teste CIC-4.
