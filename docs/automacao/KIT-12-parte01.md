# KIT-12 — Integrar alteracao, evidencia, correcao e revalidacao (artefato incremental)

Run: 667 / cartao t_0a434c97 (implementador) · filho de revisao t_811b1717 (KIT-12R)
Repo: C:/dev/stolen-realm · Branch: ci-validate-test
Meta-artefato: este arquivo e gravado em partes (`KIT-12-parteNN.md`); entregavel final em `KIT-12-entrega.md`.

## 1. Objetivo (do cartao)

Conectar a cadeia `mod alterado -> cenarios pertinentes -> coleta -> avaliadores -> relatorio`
ao ciclo CIC existente, de forma que:

- hash/versao/config/sessao atravessem TODA a cadeia;
- mudanca (hash novo) INVALIDE aprovacao anterior;
- lacuna tecnica volte ao agente; ao humano so chega autorizacao/julgamento residual;
- fila DECLARATIVA de falhas com paths/criterio/prova, limite de tentativas e deteccao de
  "sem progresso";
- NENHUM comando LLM arbitrario e executado (a fila declara; nao executa shell do modelo);
- validacao/relatorio DETERMINISTAS, sem IA permanente; integracao Hermes e OPCIONAL;
- provar CLI integrada em sandbox com fixture MARCADA e o fluxo
  erro -> correcao controlada -> revalidacao, sem fingir runtime.

## 2. Reuso obrigatorio (nao duplicar)

| ID | Cartao | O que e |
|----|--------|---------|
| CIC-1 | t_2c3e8182 | correcao/entrega do ciclo |
| CIC-2 | t_fd25da44 | entrega |
| CIC-5 | t_431dba37 | entrega (relatorio/aceite) |
| — | tools/automacao/aceite/relatorio_aceite.py | relatorio de aceite existente |
| KIT-08F | t_ac0f78f7 | visualizador de comparacao (aprovado run658) |
| KIT-10F | t_48b78ecb | cenarios KIT-10 (aprovado run666) |
| KIT-13 | t_adc1fbfa | SDK C# + pacote JSON de cenarios |
| KIT-11F | t_2a38d1d3 | executor/coleta (aprovado run660) |

Proibido: criar backend LLM novo; executar comandos LLM arbitrarios.

## 3. Criterios de aceite (veredito por item, a preencher)

- C1 cadeia propaga identidade (hash/versao/config/sessao)
- C2 mudanca invalida aprovacao anterior
- C3 lacuna tecnica -> agente; humano so residual
- C4 fila declarativa de falhas (paths/criterio/prova, limite de tentativas, sem progresso)
- C5 nao executa comando LLM arbitrario
- C6 validacao/relatorio deterministas, sem IA permanente
- C7 integracao Hermes opcional (nao dependencia)
- C8 CLI integrada em sandbox com fixture marcada
- C9 fluxo erro -> correcao controlada -> revalidacao
- C10 sem fingir runtime (fixture nao vira PASSOU/runtime)

## 4. Inventario inicial (real, lido com comando)

```
tools/automacao/{aceite,aut5,aut6,cenarios,ciclo,estilo,kit05,kit06,kit07,kit08,kit10,kit11,kit13,offline,runtime}
tools/automacao/ciclo/{ciclo.py,decisao.py,test_ciclo.py,test_decisao.py}
tools/automacao/aceite/{relatorio_aceite.py,test_relatorio_aceite.py}
tools/automacao/kit08/{visualizador.py,contra_prova_kit08.py,teste_visualizador_kit08.py,fixtures,roda_testes_kit08.sh}
tools/automacao/kit10/{kit10_cenarios.py,test_kit10_cenarios.py}
tools/automacao/kit11/{executor.py,test_kit11_executor.py}
docs/automacao/CICLO-VALIDACAO-escopo.md + CIC-1..CIC-5 (+ revisoes)
```

## 5. Blocos de trabalho (log)

- [B1] inventario de arquivos vivos + leitura dirigida do escopo CIC, ciclo.py, aceite, kit10/11.
- [B2] desenho da integracao (interface + artefatos) — a gravar.
- [B3] implementacao.
- [B4] provas reais (testes/sandbox).
- [B5] fechamento.

Status: B1 em andamento.
