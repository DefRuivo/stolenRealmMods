# KIT-05R — parte 02: leitura fria e desenho dos controles

Reviewer run 630; implementer run 629. Não há aprovação nesta etapa.

## Leitura efetivamente realizada

Leitura integral de observacao_passiva.py (460 linhas), teste_observacao_passiva.py (261), runner (33), contra_prova.py (115) e restante da supervisão (241–279). Busca dirigida em C# encontrou CorePlugin.cs:208 com lista de eventos simples e RegistrarEvento, sem pipeline Python naquele resultado; integração será conferida por inventário de usos completo (não inferida de busca truncada).

## Riscos concretos a executar em sandbox

- Captura (módulo linhas 291–321) marca atualização visual verdadeira sem checar arquivo, sequência de quadro, sessão ou atualização. `indice_quadro` pode preceder o evento. O teste do autor apenas confere o bool que o método acabou de definir: não prova PNG/pixels nem efeito.
- Pausa não é consultada em registrar_captura/verificar_timeouts, só registrar. Conferir captura e geração de falha durante pausa.
- `_ultima_chave` é global e ignora janela/quadro. Repetição A/B/A pode gerar spam; janelas A e B com dados iguais podem ser confundidas.
- `_degradacoes`, `_rejeitados`, `_pendentes` e `_resolvidos` não têm limites/retensão. Conferir crescimento com fila_max pequeno, sem chamar runtime.
- `_resolve_janela` resolve sem comparar prazo; uma janela tardia pode apagar falha ocorrida.
- `_correr_entradas` acumula eventos numa lista paralela ilimitada, mesmo quando a fila retida expira/descarta. Conferir divergência CLI eventos_total versus eventos exportados.
- Runner usa `git rev-parse` e contra-prova sob scratch. Executar numa cópia sem .git. Ausência de dependência portátil é achado, não verde.
- Contra-prova aceita qualquer exit não-zero com nome do teste no output (linhas 91–94); execução independente verificará cada FAILURE específico e ausência de ERROR/timeout, não só a frase VERDE.

## Limites preservados

Somente análise offline. Os eventos aceitos são dados sintéticos, não observação real do jogo. Nenhum arquivo de mod/produto foi editado; nenhum build (C# não mudou nesta entrega), deploy ou jogo. Próximo bloco: cópia/hash de fontes e testes reais do reviewer.
