# KIT-10R — run663 — parte03: leitura dirigida

Não altera partes anteriores. Fonte vivo lido: tools/automacao/kit10/kit10_cenarios.py, test_kit10_cenarios.py, entrega vigente KIT-10-entrega-final2.md, início dos avaliadores CIC-4/AUT-7 e regras_shrine.py/regras_debugger.py. Hashes e execuções pendentes, portanto leitura não promove a PASSOU runtime.

## Confronto inicial por critério

1. Contexto/dano: código nas linhas 224–358 usa regras_shrine.percentuais/auras_da_tabela/dano/escala. Expected não é recebido da observação. Source=0 e Target=bonus do receptor distintos. Guardas de ausência anteriores estão presentes. INDETERMINADO até execução. Refutação adicional: os comparadores `abs(float(...)-esperado)>1e-9` não contêm checagem de finitude; tentar NaN em dado observado/fonte.
2. Worship: linhas 363–423 distinguem gatilho por instância e atributo 1x; ausência de item é lacuna. INDETERMINADO até execução. Refutação adicional: `viva.get('instancias',1)` e max(1,...) podem esconder contagem ausente/inválida; aura não reconhecida pode ser tratada como atributo.
3. BetterStats: reuso literal AUT-7 em avaliar, linhas 561–568; id de base/final depende da coleta. Código AUT-7 descreve lacuna do probe para SavedMap/final; não aceitar reuso como prova de cobertura completa. INDETERMINADO.
4. Estilo/evento: linhas 428–486 exigem alvo BCT canônico + whitelist + evento_id. Cores/material/keywords são delegados ao AUT-7, não medidos no aspecto novo. INDETERMINADO.
5. Debugger: linhas 491–532 filtram somente linhas que casam censo.LINE e delegam contrato/parser. Refutação adicional: misturar linha válida com linha malformada pode silenciar o defeito por cobertura parcial. INDETERMINADO.
6. Guardas/controle: testes do autor têm 28 CASOS e 9 guardas; cadeia de teste escreve arquivo real mas continua simulação offline. Leitura sozinha não é prova; fixture não comprova runtime.
7. Escopo: sem edição de implementação; run663 independente de659/662; sem build/deploy/jogo. O teste de estilo historicamente variável terá saída registrada desta rodada, não inferida.

## Próximo bloco

Preparar sandbox própria com cópia de fontes/dados/documentação permitidos tracked/untracked, manifesto de bytes/SHA e sem binários proprietários/credenciais/.git. Executar autor e controles próprios, registrar outputs completos e exits.
