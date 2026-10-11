# KIT-09R — parte 02: leitura independente da implementação

Revisor run637 != implementador run635. Lidos integralmente kit09.py (880 linhas), test_kit09.py (545 linhas), KIT-09-entrega.md (150 linhas) e restante SUPERVISAO.md. Nenhum produto editado.

## Reuso e catálogo
Leitura estática: kit09.py importa rstv.py por caminho, valida primitivas CIC-3, declara 21 critérios com capacidade_pai/cenario_origem/esperado_origem, roll-up por pior estado. AUT-5 ainda precisa ser conferido no arquivo original e o esperado precisa ser testado contra observação adversarial (não basta o rótulo da origem).
Testes do autor usam hashes/sessão sintéticos e procedência runtime simulada; isso é aceitável para testar avaliador, mas não demonstra runtime. A suite exige prova_runtime=true/runtime_exercitado=true sobre tal simulação: verificar se o empacotamento preserva declaração fixture/sintética.

## Hipóteses de refutação (não são ainda vereditos de execução)
- kit09.py:323–327/344–350 leem pai/índice/duplicatas diretamente em o, diferente dos campos normalizados usados no restante. Pode apagar defeito vindo do coletor CIC-5.
- kit09.py:475–479 converte ausência de linhas em {} e usa linhas.get(t,0), hipótese de ausência não medida tratada como zero.
- kit09.py:407–411 permite T5 com Dependency ausente; 454–455 pula T5 na regra sem aresta inventada.
- kit09.py:579–585 exige nome não vazio do alvo do clique, sem comparação com alvo Skills independente.
- kit09.py:327–330 só valida não-null no par pai/índice, sem forma do dado; iguais malformados podem aprovar.
- kit09.py:625–643 mede sessão velha em um meta-critério separado; resumir marca runtime_exercitado se qualquer OK. Verificar se velha não continua qualificando capacidades como runtime.
- --contra-prova do autor troca fechamento por sempre OK; por construção não demonstra cada regra desabilitada falhando na suite. Prova RED contém um único defeito de placeholder; ampliar controles próprios sem alterar produto.

## Próximo bloco
Inventariar hashes vivos; sandbox nova em scratch/kit/KIT-09R-run637 sem .git/credenciais/perfil; executar suite original e probes independentes, conservar stdout/stderr/exit reais. A aprovação dos critérios permanece INDETERMINADA até isso.
