# CIC-2 — correção funcional: prova de runtime VINCULANTE e roteiro humano só residual real

Tarefa: `t_fd25da44` (CIC-2 reaberta; achados da revisão `CIC-2R`). Contrato de referência:
`docs/automacao/CICLO-VALIDACAO-escopo.md`, seção **"Correcoes funcionais da primeira
integracao"**. Sob `docs/SUPERVISAO.md` e `docs/PROCESSO-REVISAO.md`.

**Escopo exclusivo tocado:** `tools/automacao/ciclo/decisao.py`, `tools/automacao/ciclo/test_decisao.py`
e este documento. Não toquei em `ciclo.py` (CIC-1 o está alterando em paralelo), em `cenarios/**`
(CIC-3/4), no produto, no probe, no board/`KANBAN.md`. **Nenhum build, jogo, install, save,
commit, push ou publicação.** Toda prova é execução offline em `scratch/`.

## Por que (o que a CIC-2R chamou de "secundário" e o pai reclassificou)

A CIC-2R registrou três achados como backlog "não bloqueante". Eles são o **objetivo central** do
ciclo (falso verde e transferência indevida de trabalho ao humano), então viraram correção:

| achado CIC-2R | defeito real | o que passou a valer |
|---|---|---|
| **3a** `prova_runtime` ignorado | um critério `estado=OK` + `procedencia=runtime` com **`prova_runtime=false`** virava `OK_VINCULANTE`; aprovava por rótulo | runtime OK exige a **cadeia de prova** completa; `prova_runtime=false` NUNCA vincula |
| **5a** toda lacuna de runtime virava `autorizacao` | lacuna de probe/campo/coleta ia ao dono como "autorize um run" | lacuna técnica é **falha automática** (fila de agente); só autorização **explícita** vai ao dono |
| **5b** instrução específica perdida | `julgamento_humano` (texto) não chegava ao roteiro | a instrução **específica** entra no roteiro, não a genérica |

## Regras novas (contrato positivo de runtime)

Um critério `classe=runtime` `estado=OK` só é **prova vinculante** com a **cadeia completa**,
confrontada com a identidade/manifest da coleta — nunca derivada só do rótulo `runtime`:

1. `prova_runtime is True` (ausente/false ⇒ não vincula);
2. `sessao` não vazia (e igual à da identidade, quando ela declara);
3. `fonte_sha` e `dll_sha` no critério (em `fonte_sha`/`hash_fonte` no topo ou em `hashes`),
   conferidos contra a identidade — hash de outra build invalida a aprovação;
4. `config_sha` **quando `config_relevante`** é verdadeiro (a config pode vir por caminho, ex.
   `config/*.cfg` na identidade);
5. evidência **atual**: cada caminho existe, o `sha256` declarado bate com o arquivo, e, quando a
   identidade traz o **manifest da coleta** (`{artefatos:[{arquivo,sha256}]}`), o sha do arquivo
   bate com o manifest.

Falha/ausência de qualquer item da cadeia ⇒ `FALHA_AUTOMATICA` com severidade `NAO_EXERCITADO`
(equivale a NAO_EXERCITADO/INDETERMINADO do contrato), **nunca OK**. Fixtures seguem fixtures
(mesmo com todos os valores combinando). Critério `offline` continua provando por evidência +
identidade suficiente, sem exigir a cadeia de runtime.

## Regras novas (quem vai ao dono)

Para `NAO_EXERCITADO`/`INDETERMINADO` de `classe=runtime`, o **padrão passou a ser falha
automática** (lacuna de probe/campo/coleta/preparacao). Vai ao dono **somente** com sinal
explicito no critério:

- `autorizacao_necessaria is True` **ou** `tipo_pendencia == "autorizacao"` → `autorizacao`;
- `tipo_pendencia == "julgamento_visual"` **ou** `julgamento_humano`/`requer_humano` visual → `julgamento_visual`.

`tipo_pendencia == "tecnica"` (que os adaptadores CIC-3/4 já emitem) **não** é sinal humano.
A instrução específica (`julgamento_humano`/`instrucoes_humanas`) é preservada no item do roteiro.

## Prova real (comandos e saídas verdadeiras)

Tudo em scratch; nenhuma execução de jogo/build.

### 1) Testes — `python tools/automacao/ciclo/test_decisao.py`

```
total: 117 | falhas: 0
TUDO OK            # exit 0 (reproduzido 2× seguidas, idêntico)
```

Cobertura nova (fora das 4 travas antigas de fixture/evidência/identidade/hash): prova_runtime=false,
cadeia runtime ausente, hash de fonte divergente, sessão divergente, config relevante sem/`com
config_sha`, manifest incoerente × coerente, evidência ausente com sha, lacuna técnica → agente,
autorização explícita → humano, `tipo_pendencia=julgamento_visual`, sem sinal → agente, instrução
específica preservada, e 3 CLI reais novas (runtime OK, prova_runtime=false, contrato).

### 2) Contra-prova (mutantes) — o teste REPROVA quando a verificação é removida

```
M1 "confia no rótulo" (identidade_suficiente->True, _verifica_evidencia->[])   total: 117 | falhas: 12  exit=1
M2 "ignora prova_runtime/cadeia" (_cadeia_runtime->[])                         total: 117 | falhas: 13  exit=1
M3 "manda toda lacuna ao humano" (_sinal_humano->autorizacao por padrão)       total: 117 | falhas:  9  exit=1
```

- **M2 reprova exatamente o repro do CIC-2R** (`prova_runtime=false`) e as travas de cadeia —
  é a prova de que o mutante que confia no rótulo é sempre reprovado.
- M3 reprova as travas de "lacuna técnica vai ao agente".
- M1 reprova as travas de evidência/identidade/hash (as antigas).

### 3) CLI real com as saídas REAIS dos avaliadores (CIC-3/CIC-4), capturadas, sem esperar os irmãos

```
python tools/automacao/cenarios/rstv.py --observacoes tools/automacao/cenarios/rstv-observacoes.entrada.json \
    --out scratch/cic2-correcao/captura-cic3.json           # exit 2 (fixture)
python tools/automacao/cenarios/tooltips_shrines.py --observacoes tools/automacao/cenarios/shrines-observacoes.exemplo.json \
    --out scratch/cic2-correcao/captura-cic4.json --json    # exit 2 (fixture)
# criterios = captura-cic3.criterios + captura-cic4.criterios (14 critérios, ambos fixture)
python tools/automacao/ciclo/decisao.py --criterios scratch/cic2-correcao/criterios-combinados.json \
    --resultado scratch/cic2-correcao/out-combinado.json --texto     # exit 1
```

Resumo do CLI sobre as saídas reais capturadas:

```
resumo: {mods:2, criterios:14, ok_vinculantes:0, falhas_automaticas:2,
         pendencias_humanas:0, nao_conta_como_prova:14}
pronto: False — "NAO: 2 falha(s) automatica(s) volta(m) ao ciclo; nada disso vai ao dono"
roteiro humano: 0 item(ns)          # nenhuma lacuna técnica empurrada ao dono
falhas automaticas: [RoguelikeSkillTreeVisualizer:sem-prova-vinculante, BetterTooltips:sem-prova-vinculante]
```

Fixture nunca vira OK, e a lacuna vira fila de agente — **nada no roteiro humano**.

### 4) Correção no caso misto (demonstra as 4 rotas)

Caso sintético do contrato (cadeia completa, autorização explícita, lacuna técnica, rótulo falso):

```
resumo: {mods:3, criterios:5, ok_vinculantes:1, falhas_automaticas:2,
         pendencias_humanas:2, nao_conta_como_prova:0}   exit=1
roteiro humano (2, especifico):
- [BetterTooltips] JULGAR visual/UX: CONFIRMAR a linha azul do feed na tela (criterios: BT-visual)
- [RoguelikeSkillTreeVisualizer] AUTORIZAR rodada runtime: Autorizar UMA frente runtime (AUT-4/5/6) ...
falhas automaticas (2, NAO ao dono):
- [RoguelikeSkillTreeVisualizer] RSTV-lacuna: lacuna tecnica de runtime (probe/campo/coleta/preparacao): automatizavel ...
- [BetterTooltips] BT-label-falso: cadeia de prova runtime incompleta: prova_runtime ausente/false (runtime nao se aprova por rotulo) (nunca OK por rotulo)
```

Repare: (a) a instrução **específica** ("CONFIRMAR a linha azul do feed na tela") está no roteiro;
(b) `prova_runtime=false` foi para falha automática, **não** ao dono.

## Hashes (working tree, branch `ci-validate-test`)

```
b95ddc382ce46bb11c18ebb7b815ce109698299c6bd9678f766e7a7c0e63bfd9  tools/automacao/ciclo/decisao.py
0182750c91bb9861a67c0b2dd3466c2a8c6251fa7e92d7d3d8a3ece4bf73fdf8  tools/automacao/ciclo/test_decisao.py
```

## Efeito na integração (importante para o pai)

- `consolidar(criterios, identidade, aceite_humano=None)` **mantém a assinatura** e todas as chaves
  do contrato (`por_mod`, `falhas_automaticas`, `pendencias_humanas`, `pronto_para_decisao`,
  `aceite_humano`, `publicacao`), além de `roteiro_humano`/`resumo`/`aceite_inconsistente`/`identidade`.
  Cada item ganhou campos de rastreio (`prova_runtime`, `sessao`, `julgamento_humano`, `tipo_pendencia`,
  `autorizacao_necessaria`, `lacuna_probe`). `ciclo.py` (CIC-1) segue compatível.
- **Consequência esperada:** cobertura de runtime que hoje chega como `NAO_EXERCITADO` sem sinal
  explícito passa a cair em `falhas_automaticas` (fila de agente) em vez de virar autorização. Quem
  realmente precisa de **autorização** deve marcar `autorizacao_necessaria=true` /
  `tipo_pendencia="autorizacao"`; visual, `tipo_pendencia="julgamento_visual"`.
- **Produtores CIC-3/CIC-4:** critério de runtime `OK` agora precisa carregar `prova_runtime=true`,
  `sessao`, `fonte_sha`, `dll_sha` (+ `config_sha` quando config relevante) e evidência/manifest
  coerentes — os adaptadores já emitem `prova_runtime`, `lacuna_probe` e `tipo_pendencia`; falta a
  cadeia de sessão/fonte/dll no critério. Registrado para os donos de CIC-3/CIC-4 (fora do meu escopo).

## O que esta correção NÃO resolve (honesto)

- **Nenhuma rodada runtime/build/jogo.** Os `runtime OK` negativos/positivos dos testes usam evidência
  de arquivo local plausível, **não** medição de jogo. Provar runtime real depende das frentes AUT-4/5/6.
- `identidade_suficiente` continua exigindo `fonte_sha` **E** `dll_sha` (a definição da CIC-2R §6 ficou
  registrada; alinhar com o CIC-1 é decisão do pai, não toquei em `ciclo.py`).
- Não integrei ao runner `tools/testes/roda_testes.py` (pertence ao pai): `test_decisao.py` roda sozinho
  com exit 0/1/2 e linhas `RESULTADO|...`.
- Sem deploy, jogo, save, instalação, commit, push ou publicação nesta rodada.
