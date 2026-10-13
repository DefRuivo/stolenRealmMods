# KIT-14 — checkpoint 51, run1014: auditoria offline R2 executada

## Execução real
python scratch/kit/KIT-14-run1014/verify_r2.py terminou exit0. Logs, comandos, exits e manifestos em scratch/kit/KIT-14-run1014/execution.

- Pacote: 45 payloads selados sem divergência; 46 membros incluindo manifesto.
- Sandbox próprio: 41 arquivos de entrada copiados e conferidos por SHA256; sem .git/credenciais/perfil do dono. DLL candidata veio do pacote, não do perfil instalado.
- Harness precompilado upstream copiado e executado, sem rebuild independente (limitação explícita).
- Partes1–5: respectivamente 10/5/21/14/52 checks OK, zero falhas; agregado calculado 102 OK e 8 NAO_EXERCITADO (não verdes).
- Mutante default inseguro: exit1, 28 asserts falhos; seleção antiga: exit1, 6 asserts falhos; evidência errada: exit1, 3 asserts falhos. Todos alcançaram o assert esperado sem exceção inesperada.
- Candidato após mutantes: parte5 exit0, 52 OK/0 falhas/1 NAO_EXERCITADO.
- Readback gerou 15 documentos de configuração/eventos de execuções offline (inclui negativos; não é captura de jogo). Caminhos e hashes em config-readback.json.
- Quatro arquivos principais monitorados por hash ficaram iguais; principal continua SEM EsperarInteractable.

## Resultado limitado
Os dois achados R1 foram refutados/retestados no candidato R2 offline. Essa auditoria não instalou/copiou produto no principal e não comprova causalidade ntdll, ausência de crash nativo, mouse, RSTV/Skills, passivo em jogo, Runner, performance ou segundo ambiente. Nova autorização runtime continua ausente; os três boots anteriores foram consumidos. Autorização genérica A/B e dispensa de limiares não foram reabertas.

## Passo seguinte
Conferir último readback de evidências/estado sem intervenção, entregar relatório parcial run1014 e registrar needs_input com o pedido mínimo de orçamento/rota da próxima rodada. Integração identificada do R2 continua anterior ao boot; preservar hotspot/ponte e alterações manuais. Não liberar KIT14R enquanto o aceite integral não estiver exercitado.
