# EV-R2-FORAPOOL-b01 — parte 05: fechamento documental e limites das provas

Esta parte é um fechamento incremental novo; não substitui as partes01–04 nem contém propostas adicionais. Entrega final: 5 partes Markdown (3 de propostas, 1 de inventário/auditoria e 1 de fechamento). A contagem de 4 partes citada no final da parte04 era o estado anterior a este fechamento.

## Resultado executado

Comando no workspace de `t_2c6ae577`: `python validar.py`.
Saída real: `Ran 20 tests in 7.147s`, `OK`, exit code 0.
Log estruturado: `docs/automacao/EV-R2-FORAPOOL-b01-validacao.json`.

21/21 eventos na ordem das primeiras 21 seções de `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md` (84 seções no lote completo). 30 opções e 30 ações em `eventos.json`. 56 substituições textuais propostas em 53 campos distintos; todas são wording. 21 vereditos propostos MELHORAR, 0 MANTER; NÃO há aprovação automática. Em todas as 21 chaves, a recompensa e a condição são propostas como MANTER.

Os testes conferiram o inglês atual contra o canônico, unicidade dos trechos, identidades/metadados, 3 partes de 7 eventos, 21 auditorias, tags/controles/tokens preservados, contagens, NULL com motivos, referências catalogadas e hashes das 5 fontes. Controles negativos rejeitaram trecho inexistente, recompensa fabricada, mudança de condição e chave fora do intervalo. A simulação textual ocorreu somente em memória, para escrever propostas completas, não em jogo/canônico.

Não foi executada validação integral com biblioteca JSON Schema nesta rodada; `eventos.schema.json` foi lido para conferir o contrato dos campos. Os 20 testes são documentais específicos deste lote, não a suíte histórica da extração EV-R1 e não um teste de Unity/jogo.

## Interpretação rigorosa da auditoria

Em `docs/automacao/EV-R2-FORAPOOL-b01-parte04.md`, `resolvida=True` significa que existe uma entrada de metadados em `catalogo-referencias.json.resumos` para aquela referência. NÃO significa que o asset externo ou o runtime foi executado/decodificado.

As 21 referências `m_Script` usam `external:1:1910`. O resumo canônico registra external=`globalgamemanagers.assets` e reason=`Referência externa de script/apresentação; não é definição PartyEvent local.`. Assim, o `None / None` mostrado para nome/tipo nessa referência é ausência desses dois campos no resumo externo, não um PPtr nulo nem uma recompensa NULL. As 21 referências externas foram apenas consultadas no catálogo; validação do asset externo: NAO_EXERCITADO, fora do escopo documental.

Nos 21 objetos, a auditoria encontrou 94 ocorrências de PPtr NÃO nulo, com 94 entradas correspondentes de metadados no catálogo (21 externas e 73 locais). São ocorrências por caminho, NÃO 94 assets distintos. Também encontrou 47 referências de entrada, incluindo ListHolderEvents e campos residuais; NÃO são 47 execuções observadas.

A projeção sem duplicação de `opcoes[].recompensas`, `campos_originais` e `ausencias` tem 260 campos NULL: 142 resultados NAO_EXERCITADO com motivos de estado/runtime/RNG e 118 campos chave/nome de referências nulas por PPtr=0. Há 52 strings vazias nos campos explicitamente inventariados; esse censo não abrange todos os strings internos de UI, fórmulas e rolagens.

Os PPtrs crus `m_PathID=0` são sentinelas autorais (inclusive GameObject, prefabs, efeitos consumidos, GeneratedBattle, Victory/Failure/MapToForce e callbacks opcionais). Não são resultados runtime. A tabela abaixo completa a sinalização de referências nulas fora da projeção normalizada; NÃO soma esses valores aos 260 NULL nem declara defeitos. Fonte: `eventos.json`, `campos_originais`, contagem recursiva de objetos com m_PathID=0; motivos: ausência configurada, função do campo depende do contexto/flag. Aplicação desses campos: NAO_EXERCITADO, sem jogo.

| Nº | Chave | PPtrs crus com m_PathID=0 |
|---|---|---|
| 1 | resources.assets:2545637 | 3 |
| 2 | resources.assets:2545545 | 21 |
| 3 | resources.assets:2545547 | 15 |
| 4 | resources.assets:2545557 | 8 |
| 5 | resources.assets:2545558 | 8 |
| 6 | resources.assets:2545559 | 8 |
| 7 | resources.assets:2545649 | 15 |
| 8 | resources.assets:2545561 | 9 |
| 9 | resources.assets:2545564 | 21 |
| 10 | resources.assets:2545566 | 14 |
| 11 | resources.assets:2545567 | 14 |
| 12 | resources.assets:2545568 | 9 |
| 13 | resources.assets:2545571 | 9 |
| 14 | resources.assets:2545574 | 9 |
| 15 | resources.assets:2545586 | 8 |
| 16 | resources.assets:2545594 | 9 |
| 17 | resources.assets:2545575 | 14 |
| 18 | resources.assets:2545600 | 9 |
| 19 | resources.assets:2545605 | 15 |
| 20 | resources.assets:2545607 | 9 |
| 21 | resources.assets:2545610 | 9 |
| TOTAL | 21 objetos | 236 |

## Handoff

Aprovação PENDENTE para todas as 21 chaves. O dono pode manter ou rejeitar cada proposta; nenhuma foi implementada. Nenhum outro lote (eventos 22–84) foi analisado como proposta deste cartão.

O cartão `t_8e74c724` é o filho pré-criado de revisão humana dos 84 eventos NotInEventPool e depende deste lote e dos demais lotes. Conforme o protocolo do grafo, concluir a FASE DOCUMENTAL deste cartão libera a dependência; a aprovação continua no filho. Não solicitar revisão do mesmo cartão em paralelo, pois duplicaria a revisão já prevista no grafo. Esta conclusão não equivale a aprovar as propostas.

Nenhum commit/push, abertura de jogo, build/deploy ou edição de DLL/plugin/asset foi realizado. As 5 fontes em `C:/dev/stolen-realm/docs/cobertura/EV-R1/` permanecem com os hashes registrados nas partes04 e no log de validação.
