# CIC-2 (2ª correção) — cadeia, manifest e roteiro: o que fecha, o que NÃO pode fechar

Tarefa: `t_fd25da44` (CIC-2 reaberta após a revisão). Contrato de referência:
`docs/automacao/CICLO-VALIDACAO-escopo.md` (seção **"Correcoes funcionais da primeira
integracao"**, itens do objetivo central: falso verde + transferência indevida de trabalho ao
dono). Sob `docs/SUPERVISAO.md` e `docs/PROCESSO-REVISAO.md`. Rodada anterior:
`docs/automacao/CIC-2-correcao.md`.

**Escopo exclusivo tocado:** `tools/automacao/ciclo/decisao.py`,
`tools/automacao/ciclo/test_decisao.py` e este documento. Nada em `ciclo.py`, `cenarios/**`,
produto, probe, board/`KANBAN.md`, docs de outros. **Nenhum build, jogo, install, save, commit,
push ou publicação.**

## O achado da revisão e o que mudou

Comentário da revisão: *"Integracao e objetivo central: `prova_runtime=False` jamais vinculante;
lacuna tecnica/coleta/campos vai agentes, somente permissao real/julgamento visual vai dono.
Reconciliar contrato com produtores e preservar instrucao concreta."* As três correções abaixo
atacam exatamente isso — e **nenhuma** é endurecimento secundário: cada uma é um caminho de
**falso verde** ou de **trabalho humano perdido**.

| # | defeito real (antes) | o que passou a valer |
|---|---|---|
| **1** | hash declarado pelo critério em bloco **aninhado** (`hashes`/`cadeia`) era lido só para "existe?", nunca confrontado: um critério podia declarar `fonte_sha` velho num bloco aninhado e fechar OK | todo hash declarado (`fonte_sha`/`dll_sha`/`config_sha`, no topo **ou** aninhado) é confrontado com a identidade; divergente ⇒ `FALHA_AUTOMATICA` |
| **2** | o manifest do **critério** sobrescrevia o manifest da **coleta** para o mesmo arquivo — o critério se absolvia sozinho | o manifest da coleta manda; contradição ⇒ `FALHA_AUTOMATICA` ("manifest do criterio contradiz o da coleta") |
| **3** | agregar o roteiro por `(mod, tipo)` **descartava** as instruções dos critérios seguintes (dois pedidos visuais distintos ⇒ só o primeiro chegava ao dono) | instruções distintas ficam **todas** no item (`instrucoes`) + `instrucoes_por_criterio` diz qual critério pediu o quê |

`instrucoes` passa a ser multi-linha (uma por critério); o resumo humano imprime cada uma em sua
linha e mantém `(criterios: ...)`.

## O que eu NÃO apertei — e por quê (contrato com os produtores)

Testei dois apertos "óbvios" e **voltei atrás** ao rodar as suítes dos produtores: os dois
quebram CIC-3/CIC-4, ou seja, não são lacuna do `decisao.py` e sim decisão de contrato:

1. **exigir `sessao` na identidade** — `docs/automacao/CIC-2-correcao.md` regra 2 diz
   "igual à da identidade, **quando ela declara**", e `test_tooltips_shrines.py::t_runtime_verde_integra_decisao`
   consolida com identidade `{fonte_sha, dll_sha, raiz}` (sem `sessao`) esperando **7 OK_VINCULANTES**;
2. **exigir sha por arquivo na evidência de runtime** — o adaptador CIC-4 entrega a evidência como
   **caminho do artefato lido** (`_evidencia_obs`), e a mesma suíte espera OK com esse formato.

Nos dois casos o aperto reprovaria rodada legítima do produtor ⇒ seria falso **vermelho** e
retrabalho. Os dois comportamentos ficaram **pinados em teste** (nomeados `CONTRATO: ...`) para
que ninguém os aperte em silêncio: se o pai quiser endurecer, é mudança de contrato dos
produtores, não deste módulo.

## Prova real (comandos e saídas verdadeiras; tudo offline, em scratch)

### 1) Testes do módulo

```
$ python tools/automacao/ciclo/test_decisao.py
total: 127 | falhas: 0
TUDO OK            # exit 0  (eram 117 checagens; +10 desta rodada)
```

### 2) As suítes dos PRODUTORES continuam verdes (não quebrei os irmãos)

```
$ python tools/automacao/cenarios/test_rstv.py              # exit 0
$ python tools/automacao/cenarios/test_tooltips_shrines.py  # exit 0
```

### 3) Contra-prova: cada regra nova REPROVA quando removida (mutante)

```
M4_cadeia_aninhada_ignorada       exit=1  REPROVADAS: hash de cadeia aninhado divergente -> falha tecnica (nao OK)
M5_manifest_do_criterio_sobrepoe  exit=1  REPROVADAS: manifest do criterio nao sobrescreve o da coleta -> falha tecnica
M6_roteiro_so_primeira_instrucao  exit=1  REPROVADAS: agregacao preserva as DUAS instrucoes no roteiro
$ python tools/automacao/ciclo/test_decisao.py      # módulo real
total: 127 | falhas: 0 | TUDO OK                    # exit 0
```

Manifesto de M5 **isolado** de propósito: a coleta declara o sha **real** (bate com o disco) e o
critério declara outro sha para o **mesmo** arquivo — sem a regra, o critério se absolveria.

### 4) CLI real sobre as saídas REAIS dos avaliadores (capturadas, sem esperar os irmãos)

```
$ python tools/automacao/cenarios/rstv.py --observacoes tools/automacao/cenarios/rstv-observacoes.entrada.json
$ python tools/automacao/cenarios/tooltips_shrines.py --observacoes tools/automacao/cenarios/shrines-observacoes.exemplo.json --json
# cada um: exit=2 (fixture), 7 criterios
$ python tools/automacao/ciclo/decisao.py --criterios <14 criterios dos dois> \
      --identidade <{fonte_sha,dll_sha}> --repo <REPO> --resultado saida.json --texto
EXIT=1
resumo: {mods: 2, criterios: 14, ok_vinculantes: 0, falhas_automaticas: 2,
         pendencias_humanas: 0, nao_conta_como_prova: 14}
roteiro humano: 0 item(ns)
falhas automaticas: [RoguelikeSkillTreeVisualizer:sem-prova-vinculante, BetterTooltips:sem-prova-vinculante]
```

Fixture nunca vira OK e **nada** de lacuna é empurrado ao dono (0 itens no roteiro).

### 5) Caso misto com as 4 rotas + integração com o CIC-1

Critério **positivo gerado pelo produtor real** (CIC-3 `rstv.avaliar` com observação de runtime +
manifest do AUT-4) + visual + autorização + lacuna técnica + rótulo falso:

```
DECISAO caso misto: exit=1
resumo: {mods: 2, criterios: 5, ok_vinculantes: 1, falhas_automaticas: 2,
         pendencias_humanas: 2, nao_conta_como_prova: 0}

ROTEIRO HUMANO (residual) — 2 item(ns):
- [BetterTooltips] JULGAR visual/UX:
    * CONFIRMAR a linha azul do feed na tela
    (criterios: BT-visual)
- [RoguelikeSkillTreeVisualizer] AUTORIZAR rodada runtime:
    * Autorizar UMA frente runtime (AUT-4/5/6) e reexecutar o ciclo; sem autorizacao nada em jogo e lido.
    (criterios: RSTV-autoriza)

FALHAS AUTOMATICAS (voltam ao ciclo, NAO ao dono) — 2:
- [RoguelikeSkillTreeVisualizer] RSTV-lacuna: lacuna tecnica de runtime (probe/campo/coleta/preparacao) ...
- [BetterTooltips] BT-label-falso: cadeia de prova runtime incompleta: prova_runtime ausente/false ...

PRONTO PARA DECISAO: NAO   ACEITE HUMANO: NAO_PRONUNCIADO   PUBLICACAO: NAO_VERIFICADO
```

Integração com o CIC-1 exercitada com a decisão **real** acima (sem rodar o ciclo/AUT-3, que são
do CIC-1):

```
carregar_decisao: presente=True erro=None modulo=True
consolidar_decisao: origem=decisao.py pronto=False okv=1 falhas=2 aviso=None
criterio positivo do produtor: RSTV-26-placeholders -> OK_VINCULANTE
fila_da_decisao: 2 item(ns)   (execucao_automatica=False nos dois)
```

`aviso=None` = a decisão real consolidou (não caiu no fallback mínimo); as falhas automáticas
viram **fila declarativa** de agente, sem comando executado automaticamente.

## Achado para o pai (fora do meu escopo, NÃO consertei)

Os dois produtores discordam sobre o significado do MESMO campo do coletor CIC-5:

- `cenarios/rstv.py` (`_ALIAS_HASH`, l.97): `hash_fonte` → **`dll_sha`** ("o `hash_fonte` do
  coletor CIC-5 e o sha da DLL");
- `cenarios/tooltips_shrines.py` (`_chain_extra`, l.389): `hash_fonte` → **`fonte_sha`**.

Para o `decisao.py` os dois chegam coerentes (cada critério copia os hashes da identidade), mas a
rodada **crua** do probe é lida com semânticas opostas — quem autorizar a frente runtime vai
precisar de uma resposta única. Registrado aqui, sem tocar nos dois arquivos.

## Estado dos artefatos

```
sha256 (working tree)  tools/automacao/ciclo/decisao.py
d6de959e73a090e43da2b5438a12ba1739d32be2bd9494c0fe9f0d84d9163933
sha256 (working tree)  tools/automacao/ciclo/test_decisao.py
d6a1b1e9a7b987b6e5d18e9b3fe3122afadab77f76707f786f76cb7d33c06205
```

(sha256 real acima) · capturas e decisões em `cic2-cli/` no workspace da tarefa
(`captura-cic3.json`, `captura-cic4.json`, `decisao-produtores.json`, `decisao-misto.json`).

## O que esta rodada NÃO resolve (honesto)

- **Nenhuma rodada runtime/build/jogo.** O positivo de runtime dos testes usa evidência de arquivo
  local + manifest montado pelo `coletor.montar_manifest`, **não** medição de jogo; provar runtime
  real depende das frentes AUT-4/5/6 autorizadas.
- O alinhamento de semântica de `hash_fonte` entre CIC-3/CIC-4 (acima) fica com o pai.
- Nada de board/`KANBAN.md`, commit, push, publicação, deploy ou jogo nesta rodada.
