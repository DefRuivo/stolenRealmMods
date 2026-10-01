# Plano de testes (padrao do projeto)

## Por que isto existe

Hoje quase tudo que provou qualidade foi **olho humano** ou **leitura de codigo**. Duas das travas mecanicas
deste projeto ja deram verde no estado errado: o `check_patches` aprovou um aplicador que cobria ZERO ganchos,
e a conferencia de shrines so nao aprovou o formato antigo porque se recusou a compara-lo. A regra que fica:

> **Todo teste tem de ser MOSTRADO REPROVANDO.** Planta o defeito, roda, ve falhar; tira o defeito, roda, ve passar.
> Teste que nunca falhou nao e teste - e decoracao.

## Como rodar (sem depender do jogo para o que nao depende)

* Testes de LOGICA PURA (formulas, formatacao, parsers, tabelas, filtros) rodam com `dotnet test` ou um runner
  simples, referenciando o projeto do mod. Nao precisam do jogo e podem rodar em CI quando o `lib/` estiver disponivel la.
* Testes que precisam de tipos do jogo (Unity/Mathf, TMP, Character) rodam LOCAL, com o `lib/` da maquina do
  desenvolvedor (que e gitignored). Eles declaram isso no cabecalho e falham com mensagem clara quando o `lib/` falta.
* Testes de CENA (o que so aparece em partida) continuam sendo roteiro para o dono, mas o que da para capturar em
  LOG tem de ser capturado em log e conferido pela ferramenta - nao transcrito a mao.

## Vocabulario de cenario (usar estes nomes nas tarefas)

**EXCESSO DE SHRINE**: Worship (+100), Omnism II (+20), Horn of Devotion (+50/+100), os dois juntos, tres bencaos
acumuladas, varias auras no MESMO atributo, stacks do mesmo status, dois personagens na mesma aura.

**BORDAS**: valor zero, valor negativo (Energy), total que arredonda para zero, fracao (.5 e -0.4), minimo 1 do
Flame, vida maxima 3 (Decay), atributo inexistente (o indexador do motor LANCA), aura viva sem representacao
(Dwarven), contribuicao maior que o total.

**INVARIANTES** (valem para todo mod, e cada um vira teste):
1. Todo numero exibido e o do MOTOR - nada somado a mao.
2. A lista de auras se diz completa: nenhuma aura viva pode sumir em silencio.
3. Mods nao se referenciam entre si (zero ocorrencia do nome/GUID de um no codigo do outro).
4. Falha e sempre do lado reversivel e declarada no log, nunca em silencio.
5. Assinatura de patch por TIPO, parametro por NOME, nunca por indice.
6. Marcador de vida no boot e contagem REAL de ganchos aplicados.
7. Nenhum numero, cor ou texto sem procedencia (o repo e a fonte).
