# KIT-10 — parte 04: correção aplicada e reprodução das provas (F1/F2/F3)

Rodada: implementador run655 (correção do request_changes do KIT-10R / run651).
Arquivos corrigidos (ambos já existentes nesta frente, nada de outro mod tocado):

- `tools/automacao/kit10/kit10_cenarios.py`
- `tools/automacao/kit10/test_kit10_cenarios.py`

## O que mudou (por achado)

### F1 — `_asp_por_evento` sem whitelist de evento (ALTO)
Antes: `if estagio in ESTAGIOS_DE_BOOT: defeito... elif not estagio: NAO_EXERCITADO ...`
→ `estagio="banana"` + `evento_id` caía no ramo final e fechava `OK/prova_runtime=True`.
Agora: `elif estagio not in ESTAGIOS_DE_EVENTO:` → **NAO_EXERCITADO**, com dois motivos
distintos (sem `estagio` declarado vs. `estagio` fora da whitelist). Um estágio inventado nunca
mais entra no ramo que fecha OK.

### F2 — `_asp_worship_dobro` ignorava aura viva sem item (ALTO)
Antes: `if got is None: continue` → com `itens_observados={}` (ou item ausente para uma aura)
sobrava `defeito=[]` e o critério fechava `OK/prova_runtime=True`.
Agora: a aura viva sem item entra numa lista `faltando`; o estado passa a ser
`REPROVADO` (se houver defeito medido) → `NAO_EXERCITADO` (se houver aura não medida) → `OK`
(somente com todas as auras medidas). `observado` carrega `sem_observacao` com as auras não
medidas. `itens_observados` que não seja mapa também cai em "tudo não medido" (nunca OK).
Comportamento confirmado preservado: o "dobro" do gatilho (DWA-2) continua esperado por instância.

### F3 — `_asp_contexto_dano` não media a tooltip e aprovava (MÉDIO)
Antes: a guarda `if aura_buff and atributo and aura_buff in auras ...` não rodava quando o buff
estava fora da tabela → a tooltip do receptor não era medida e o critério fechava
`OK/prova_runtime=True`.
Agora: `lacuna` registra (a) buff declarado fora da tabela / sem atributo, e (b) `contrib` ausente
com esperado independente disponível. Ordem de estado: `REPROVADO` > `NAO_EXERCITADO` (lacuna) >
`OK`. `observado["lacuna"]` documenta o motivo na evidência.

### F4 — discrepância de handoff do `test_estilo_atributos.py`
Medido nesta rodada (run655), não atribuído ao KIT-10:

    $ python tools/automacao/estilo/test_estilo_atributos.py
    ESTILO_EXIT=1
    total: 28 | falhas: 1
    REPROVADAS: medicao offline REAL: roda a suite do projeto e nao deixa mod sem familia de teste
    (log completo: scratch/kit/KIT-10-run655-estilo.txt)

Ou seja: o exit REAL é **1**, não 0 como o resumo do implementador anterior declarou; a causa é
um mod sem família de teste detectado pela medição offline real (escritores concorrentes de outra
frente — o KIT-10 não toca `tools/automacao/estilo/` nem família `t_*`).

## Provas executadas nesta rodada (saídas reais)

1. **Suite KIT-10** (`python tools/automacao/kit10/test_kit10_cenarios.py`): **24/24 PASSOU,
   exit 0** (antes eram 17 casos; +5 guardas novas +2 testes de isca).
2. **Isca** (`--isca`): `ISCA|OK|defeito plantado detectado`, **exit 0**.
3. **Probe do próprio revisor KIT-10R** (`scratch/kit/KIT-10R-run651/probe_revisor.py`,
   reexecutado nesta rodada, saída em `scratch/kit/KIT-10-run655-probe-revisor.txt`):

       P2 estagio=banana        -> NAO_EXERCITADO False   (antes: OK True)
       P3 worship sem itens     -> NAO_EXERCITADO False   (antes: OK True)
       P3b worship item ausente -> NAO_EXERCITADO False   (antes: OK True)
       P4 buff fora da tabela   -> NAO_EXERCITADO False   (antes: OK True)
       P5 alvo fora da tabela   -> NAO_EXERCITADO False

   É a refutação do revisor, reexecutada contra o fonte corrigido: os quatro falsos-OK sumiram.
