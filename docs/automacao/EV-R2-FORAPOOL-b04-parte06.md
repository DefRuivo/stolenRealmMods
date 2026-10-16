# EV-R2-FORAPOOL-b04 — parte06: leitura, verificação e handoff humano

Cartão t_60b05dec. Entrega exclusivamente documental, 21/21 eventos das seções 64–84 de C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md. Nenhuma aprovação humana foi inferida.

## Onde revisar

Destino durável: C:/dev/stolen-realm/docs/automacao/.

- EV-R2-FORAPOOL-b04-parte01.md: inventário inicial das 21 chaves.
- EV-R2-FORAPOOL-b04-parte02.md: 7 análises, eventos 64–70.
- EV-R2-FORAPOOL-b04-parte03.md: 7 análises, eventos 71–77.
- EV-R2-FORAPOOL-b04-parte04.md: 7 análises, eventos 78–84.
- EV-R2-FORAPOOL-b04-parte05.md: inventário final, contagens, 336 NULL individualizados com motivo, vazios, referências nulas e status de apoio.
- EV-R2-FORAPOOL-b04-propostas-auditadas.json: propostas estruturadas e campos atuais literais.
- EV-R2-FORAPOOL-b04-fontes-eventos.json: cópia semântica exata dos 21 eventos canônicos selecionados, inclusive todos os campos originais.
- EV-R2-FORAPOOL-b04-referencias-auditadas.json: 51 resumos de apoio e 45 referências entrantes locais explícitas, sem resolução de runtime.
- EV-R2-FORAPOOL-b04-fontes-hashes.json: proveniência das fontes e do catálogo recuperado pelo git.

## Contagens verificadas

21 eventos; 19 vereditos PROPOSTOS MELHORAR/wording e 2 MANTER (68 The Sultan, 81 What Lurks). 40 campos propostos, com 43 substituições textuais; 17 prompts de seleção contextualizados. Recompensa e condição: MANTER em todas as 21 chaves. Aprovação: PENDENTE em todas.

29 opções, 28 ações, 0 overrides; 3 eventos sem opções, 2 eventos disabled=1, 0 opções com ocultação configurada e 0 hideOptionEffectText ativo. 76 strings vazias auditadas nos campos narrativos/seleção/rolagem/manuais enumerados.

336 posições NULL no canônico, inclusive projeções redundantes: 244 resultados não exercitados e 92 posições de chave/nome de referência nula, equivalentes a 46 objetos de referência nula projetada. Separadamente: 567 PPtrs literais m_PathID=0, inclusive dados originais e projeções. Não somar estas unidades como se fossem recompensas ou ocorrências no jogo. NULL nunca foi convertido em zero.

## Resultado real de verificação

Workspace de execução: C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_60b05dec/.

- python validar.py: 28 testes, 0 falhas/0 erros, OK, RC=0; saída real registrada em EV-R2-FORAPOOL-b04-validacao.json.
- Reteste após preparar replay independente: 28 testes, 0 falhas/0 erros, OK, RC=0; EV-R2-FORAPOOL-b04-validacao-reteste.json.
- ZIP de reprodução extraído em diretório NOVO repro-limpa/, com fontes completas dentro do pacote: 28 testes, 0 falhas/0 erros, OK, RC=0; EV-R2-FORAPOOL-b04-validacao-repro.json e EV-R2-FORAPOOL-b04-repro-recibo.json.

A suíte confere ordem/chaves, metadados, snapshots, textos antes literais contra campos originais, propostas completas nos Markdown, tokens/tags, NULL com motivos, efeitos/condições intactos, referências de catálogo e encadeamentos. Inclui 6 controles negativos: evento removido, recompensa final fabricada, texto antes inventado, placeholder removido, proposta em campo de recompensa e troca de ordem das chaves. Estes negativos são rejeitados, não implementados.

Validação integral por biblioteca JSON Schema: NAO_EXERCITADO, jsonschema indisponível neste interpretador. O contrato foi consultado, mas os 28 testes são assertivas documentais próprias; não afirmar validação integral de JSON Schema nem teste funcional do jogo.

O catálogo de 2399 registros/3214 resumos foi recuperado SOMENTE POR LEITURA de 097f950:docs/cobertura/EV-R1/catalogo-referencias.json. O eventos.json histórico e o atual diferem em SHA-256 porque LF/CRLF do arquivo; igualdade do JSON completo e igualdade dos bytes após normalização apenas CRLF foram verificadas. Nenhum string interno foi alterado.

## Como reproduzir sem jogo

No repositório atual:

    python C:/dev/stolen-realm/docs/automacao/EV-R2-FORAPOOL-b04-validar.py --evidence EV-R2-FORAPOOL-b04-validacao-local-NOVA.json

No pacote ZIP, extrair em diretório NOVO e executar:

    python validar.py --evidence EV-R2-FORAPOOL-b04-validacao-local-NOVA.json

O ZIP leva fontes/ completas: a suíte seleciona esse diretório antes de consultar o repositório, sem necessidade de Git ou acesso ao jogo. Nome de evidência precisa ser novo; escrita é exclusiva, para não substituir auditorias anteriores.

## Decisão humana e limites

Revisão humana já pré-criada: t_8e74c724, único filho deste cartão. Concluir a fase documental deste lote libera sua dependência, mas NÃO conclui a revisão humana dos 84 eventos nem aprova as 21 propostas. Não abrir revisão duplicada no mesmo cartão. Dono pode aceitar/rejeitar cada proposta por chave e campo; qualquer implementação posterior exige novo cartão autorizado.

NAO_EXERCITADO: runtime/UI, disponibilidade real, RNG, valores finais de ouro/XP/loot, aplicação de status, renderização de tags, comportamento de laços e combate. Motivo: a tarefa proíbe execução do jogo. Nenhum jogo foi aberto e nenhum plugin/DLL/asset/arquivo do jogo foi alterado. Fontes canônicas permanecem inalteradas; somente documentos novos são destinados ao repositório.
