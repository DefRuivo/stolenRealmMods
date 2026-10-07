# CIC-2R — revisão independente da consolidação de decisão (`decisao.py` / `test_decisao.py`)

Tarefa: `t_8ad5cea7` (CIC-2R). Revisão **read-only** da entrega CIC-2
(`docs/automacao/CIC-2-entrega.md`), do roteiro humano residual e da integração com CIC-1/CIC-3/CIC-4 e
com os controles reais das implementações CIC-3/4. Sob `docs/SUPERVISAO.md`, `docs/PROCESSO-REVISAO.md`,
`docs/automacao/CICLO-VALIDACAO-escopo.md`.

**Nada foi editado, buildado, jogado, instalado, salvo, commitado ou publicado.** Não toquei em
`decisao.py`, `test_decisao.py`, `ciclo.py`, `cenarios/**`, produto, probe, board ou `KANBAN.md`. Toda
evidência é execução offline em scratch Hermes; nenhuma medição de jogo.

## Hashes lidos (working tree, branch `ci-validate-test`)

```
836b08c811abef6d9a48d0e6258602d74695c3072d673a82f6d9fd1ea608cd48  tools/automacao/ciclo/decisao.py
699ab82e59154a5e0d5c8970f32dc2018e6c207ef4c48aeda04721fc6a2ff3c7  tools/automacao/ciclo/test_decisao.py
```

Batem com o `CIC-2-entrega.md` — o que revisei é o que foi entregue.

## Veredito geral

**APROVADO COM ACHADOS (não bloqueantes).** A regra central — *nunca OK por rótulo* — funciona para os
quatro buracos do aceite (fixture, evidência ausente, identidade insuficiente, hash de bytes antigos), e a
divergência de fixture rstv×shrines é **neutralizada**. Dois pontos cegos reais, porém secundários ao
objetivo do ciclo, ficam registrados: o consolidador ignora o sinal `prova_runtime` e não separa **lacuna
técnica** de **autorização** real; e o roteiro perde a instrução específica de `julgamento_humano`.

## Veredito por item

### 1. Fiação e contrato de saída — OK
`consolidar(criterios, identidade, aceite_humano=None)` devolve `por_mod`, `falhas_automaticas`,
`pendencias_humanas`, `pronto_para_decisao`, `aceite_humano`, `publicacao` (+ `roteiro_humano`, `resumo`,
`aceite_inconsistente`, `identidade`). `aceite_humano` e `publicacao` em campos separados, com
`NAO_PRONUNCIADO` / `NAO_VERIFICADO` por padrão. Aceite num mod com falha automática vira
`aceite_inconsistente`. Confirmado por leitura (l.460-553) e por teste.

### 2. Testes e contra-prova — OK (prova real, não decoração)
Reproduzido nesta revisão:

```
$ python tools/automacao/ciclo/test_decisao.py            total: 77 | falhas: 0   TUDO OK   exit=0
$ CIC2_DECISAO=<scratch>/decisao_mutante.py python ...    total: 77 | falhas: 10  exit=1
   (mutante: identidade_suficiente->True, _verifica_evidencia->[])
```

As 10 falhas do mutante são exatamente os três buracos (evidência/identidade/hash) + o efeito por mod.
O teste **reprova** quando a prova é removida — é teste de comportamento, não de leitura do autor.

### 3. Regra “nunca OK por rótulo” — OK para o que cobre; ACHADO para o que falta
Verificado por comportamento:

| cenário | resultado | veredito |
|---|---|---|
| `OK` sem evidência | `FALHA_AUTOMATICA`, não vai ao humano | OK |
| evidência ausente no disco | `FALHA_AUTOMATICA` | OK |
| identidade insuficiente (sem `fonte_sha`/`dll_sha`) | `FALHA_AUTOMATICA` | OK |
| `hash` de bytes antigos | `FALHA_AUTOMATICA` (“aprovacao anterior invalidada”) | OK |
| `hash` que a identidade não conhece | `FALHA_AUTOMATICA` | OK |
| `offline` `NAO_EXERCITADO` | `FALHA_AUTOMATICA` (não vai ao dono) | OK |
| `runtime` `NAO_EXERCITADO` (identidade ok) | `PENDENCIA_HUMANA` `autorizacao` | ver §5a |

**ACHADO 3a (latente) — `prova_runtime` ignorado.** `prova_runtime` não aparece em `ciclo/` (grep: 0
ocorrências). Um critério `estado=OK` + `procedencia=runtime` + **`prova_runtime=False`** vira
`OK_VINCULANTE` / `pronto_para_decisao=True` reproduzivelmente (evidência = arquivo que existe):

```
criterio {estado:OK, classe:runtime, procedencia:runtime, prova_runtime:False,
          evidencia:["tools/dados/shrines-esperado.csv"]}
-> classificacao: OK_VINCULANTE | prova_vinculante: True | pronto: True
```

Os adaptadores CIC-4 **já emitem `prova_runtime`** como sinal honesto (“fixture não prova runtime”). O
consolidador não o consome: se um critério chegar com rótulo `runtime/OK` por **qualquer** divergência
(adaptação futura, erro de rótulo), a única barreira restante é “o caminho de evidência existe” — e uma
tabela de esperado satisfaz isso. Ou seja: aprova-se por rótulo/procedência quando o rótulo está errado.
Recomendação (backlog, não hardening agora): recusar OK quando `prova_runtime is False` explicitamente, ou
fazer o campo ser o portão de prova em vez de `procedencia`.

### 4. Divergência de fixture rstv × shrines — OK (neutralizada)
Comando: alimentei o `consolidar()` com os critérios **reais** de CIC-3/CIC-4.

| fonte (fixture) | estados emitidos | consolidador | pronto |
|---|---|---|---|
| `shrines-observacoes.exemplo.json` (CIC-4) | 7× `OK` / `fixture` / `prova_runtime=False` | **7 `NAO_CONTA_COMO_PROVA`** + 1 falha sintética `sem-prova-vinculante` | `False` |
| `rstv-observacoes.entrada.json` (CIC-3) | 7× `NAO_EXERCITADO` / `fixture` | **7 `NAO_CONTA_COMO_PROVA`** + 1 falha sintética | `False` |

O consolidador **não aprova nenhum dos dois**: a checagem de fixture é por `procedencia` (passo 2, antes de
olhar `estado`), então o rótulo `OK` do adapter de shrines é ignorado. O ponto que o pai pediu verificar
**passa**. A ressalva é a de §3a: isso depende de o rótulo de `procedencia` estar certo; não há segunda
barreira quando ele também estiver errado.

### 5. Integração com CIC-1 (`ciclo.py`) — OK com ressalvas
Rodada de reuso real (ZERO builds): `ciclo.py --repo C:/dev/stolen-realm --aut3-resultado <AUT-3> --resultado <scratch>`
→ exit `0`, `APROVADO_OFFLINE`, `pendencias_runtime=12`. Decisão embutida:

```
resumo: {mods:7, criterios:53, ok_vinculantes:41, falhas_automaticas:0,
         pendencias_humanas:12, nao_conta_como_prova:0}
pronto: True — "SIM: automacao sem falhas; resta decisao humana (2 item(ns) no roteiro)"
roteiro: [('BetterTooltips','autorizacao',9), ('RoguelikeSkillTreeVisualizer','autorizacao',3)]
```

Bate **exatamente** com o `CIC-1-entrega.md` (l.73-75): 41 OK vinculantes · 0 falhas · 12 pendências → 2
itens. **O sentido de `pronto_para_decisao=True` está correto** pela definição do módulo (automação sem
falha E existe prova/pendência): é “[a automação terminou; falta decisão humana]”, não aceite nem
publicação — ambos seguem separados. A agregação em 2 itens é aritmeticamente fiel (9+3=12).

**ACHADO 5a — as 12 são mistas; “autorização de UMA rodada” superestima.** Os 12 itens vêm do
`AUT-3-resultado.json` (`cobertura.itens`): `T-RSTV21`, `T-RSTV25B`, `T-RSTV26` (RSTV) +
`S-RV-26/27/28/29/30/31/33/34` + `BUG34` (BetterTooltips). Nem todos são “o dono autoriza um run”:

- **`T-RSTV25B`** — motivo “precisa do LogOutput.log do próximo boot (INDETERMINADO)”; CIC-3 diz que o
  marcador `RSTV-25:` **não foi localizado** no log existente. É lacuna de **diagnóstico/coleta** (o mod
  pode não emitir o marcador) — não se resolve autorizando um run.
- **`T-RSTV26` / `T-RSTV21`** — revalidação **visual/UX** (hover resolvido; janela abre/navega/fecha);
  pela semântica do próprio módulo seria `julgamento_visual`, e `T-RSTV21` ainda mistura **publicação**.
- **`S-RV-*`** — CIC-4 declara que a superfície **FEED** não é emitida pelo coletor atual (lacuna técnica
  de coleta), além da leitura em jogo.

O consolidador não tem sinal para separar: **todo** `runtime NAO_EXERCITADO` vira `autorizacao`, ignorando
`lacuna_probe` e o `motivo`. Reprodução: critério runtime `NAO_EXERCITADO` com `lacuna_probe` (probe não
emite o campo) → `PENDENCIA_HUMANA` / `autorizacao`, e o roteiro imprime “Autorizar UMA frente runtime
(AUT-4/5/6) e reexecutar o ciclo”. O contrato manda o oposto: *“Pendencias tecnicas automatizaveis nao sao
transferidas ao humano.”* Isto é o “pedir para dono testar tudo” para o subconjunto técnico/visual.

Classificação correta do pai: **autorização real pode ficar residual; lacuna técnica faltando
coleta/campo/erro vai para a fila de agentes.** O consolidador ainda não faz essa distinção — *backlog*,
não bloqueio (ele cumpre literalmente a regra do contrato v1, que é cega a essa diferença; o ajuste é do
contrato/roteiro, com sinal explícito do critério, não de hardening novo).

**ACHADO 5b (menor) — instrução específica de `julgamento_humano` é perdida.** `_item()` copia só
`criterio["instrucoes_humanas"]`; o fluxo comum — critério com `julgamento_humano` (string) — não carrega
esse texto. Reproduzido:

```
criterio {julgamento_humano: "CONFIRMAR o layout do tab X ... (ESPECIFICA)"}
-> item.instrucoes_humanas: None
-> roteiro.instrucoes: "Abrir o jogo no alvo do criterio e confirmar a aparencia/UX; ..."  (genérica)
```

Contraria o contrato (“com motivo e instrucoes concretas”) e o próprio docstring do módulo. O teste
`t_runtime_julgamento_visual` cobre só o **tipo** da pendência, nunca o **texto** da instrução — por isso
não pegou. Correção mínima sugerida: `_item` também carregar `julgamento_humano` (ou `_instrucao_humana`
recebê-lo no item normalizado).

### 6. Divergências de fronteira com CIC-3/CIC-4 (integração — reportar aos revisores daqueles)
- **Enum `procedencia` divergente (CIC-4 → CIC-2).** `tooltips_shrines._crit` emite
  `procedencia="offline"` no ramo “sem linha na tabela” — valor **fora** do enum do contrato
  `(execucao, runtime, fixture)`. Reproduzido: `estado=NAO_EXERCITADO, classe=runtime,
  procedencia="offline"` → CIC-2 classifica **`FALHA_AUTOMATICA` “criterio malformado: procedencia
  invalida”**. Efeito: não vai ao humano (fail-closed, defensável), mas a razão fica errada e infla a fila
  de correção. É defeito do arquivo CIC-4 (não meu escopo de edição) — registrar para o autor/revisor de
  CIC-4. Um caso fora da tabela real reproduz o caminho (`aura` inexistente → `procedencia="offline"`).
- **Identidade “suficiente” divergente (CIC-1 × CIC-2).** `ciclo.identidade_suficiente` exige só
  `fonte_sha`; `decisao.identidade_suficiente` exige `fonte_sha` **E** `dll_sha`. Num repo sem
  `bin/Release` (dll_sha None) o ciclo poderia marcar OK de fonte que o CIC-2 rebaixa a falha automática.
  Na rodada real observada `dll_sha` existe, então não dispara — secundário.

### 7. Aceite × publicação separados, e invalidação por hash — OK
`aceite_humano` não altera `pronto_para_decisao`; `publicacao` permanece `NAO_VERIFICADO`; aceite marcado
com falha automática vira `aceite_inconsistente` sem esconder a falha; hash de bytes antigos invalida a
aprovação anterior. Tudo coberto por teste e confirmado na leitura.

## Achados → backlog (não bloqueiam o objetivo do ciclo)

1. **3a** `prova_runtime` ignorado (aprovação por rótulo quando o rótulo erra).
2. **5a** lacuna técnica/visual × autorização real: o consolidador manda todo `runtime NE` ao dono.
3. **5b** instrução específica de `julgamento_humano` perdida no roteiro.
4. **6** enum `procedencia="offline"` do CIC-4 (no arquivo dele) e definição divergente de identidade
   suficiente CIC-1×CIC-2.

## O que esta revisão NÃO confirma (só se resolve em jogo/humano)

- Nenhuma rodada runtime, build, jogo ou save. Os `runtime OK` dos testes de CIC-2 usam evidência de
  arquivo local plausível, **não** medição de jogo — não transferível para “o mod funciona em jogo”.
- A aprovação de envio (publicação) e o aceite humano seguem fora da automação e não foram tocados.
- O comportamento real do AUT4Probe em jogo (campos que hoje não emite) permanece NÃO EXERCITADO.

## Conclusão

A CIC-2 entrega o que promete no núcleo: separa prova vinculante de falha automática e de pendência
humana, reconfere a prova contra a realidade, **não aprova fixture** (rstv nem shrines), e mantém
aceite/publicação como estados separados. Os achados são de **integração e de fidelidade do roteiro**, não
de quebra da regra central — vão para backlog, sem bloquear o objetivo do ciclo.
