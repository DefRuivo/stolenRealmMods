# KIT-14 — entrega parcial run721: dependência runtime ainda aberta

Tarefa t_a1f38855; implementação documental default/run721; revisão independente pendente no filho existente t_9ce7d260. NÃO é aceite do KIT-14 nem DoD. Esta retomada não executou runtime nem alterou produto.

## Resultado real

Em 11/10/2026 02:24:02 -03, terminal exit 0:
- `bash scratch/kit/front-unica.sh status`: `Lock ativo: NAO`, `Lock disponivel`.
- consulta readonly `Get-Process -Name "Stolen Realm"`: array vazio `[]`.
- `git diff --cached --name-only`: vazio.
- branch inicial reconferida: ci-validate-test; alterações manuais preexistentes preservadas.

Identidades vivas calculadas por hashlib.sha256 no terminal, todas correspondentes às entregas SEG1/SEG2:

| Arquivo | SHA256 | Bytes |
|---|---|---:|
| tools/automacao/runtime/core/CorePlugin.cs | 192e463675e2056f3476df2bd3f094e4795e67a130c4392c973c63619b282c59 | 15219 |
| tools/automacao/runtime/core/bin/Release/KIT04Core.dll | 0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d | 34304 |
| tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs | ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2 | 104974 |
| tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll | 95069e9cbc5e1e7784f80b34589e54cf19651969cddad86b6a35d9b94c89a865 | 75776 |
| docs/automacao/KIT-14G-SEG2-parte01.md | 925c0af686718319f940aaae1edd55cb7a4fa22b8ff6ba648745b0a218a8f94e | 10329 |
| docs/automacao/KIT-14G-SEG1-entrega.md | b81890412caf415bebc54949da86291dd1b1c983a4e5bce91a18287d8e915b4b | 9323 |

## Bloqueio por dependência, não consentimento genérico

O KIT-14G concluído aprovou um relatório com lacunas explícitas. Não provou HUD/RSTV nem recorder eficaz. O Core SEG1 corrigido ainda não foi medido em boot real. O novo probe SEG2 só teve verificação offline; seu cartão t_139f714f está BLOCKED e a medição discriminadora do encerramento 0xc0000005 em Accept segue pendente.

Já existe tarefa específica KIT14G-SEG1-RT t_a41dd22d para provar evento inicializacao/contagem >0 e identidade do Core em runtime, dependente de SEG1 e SEG2. Essa prova é pré-requisito do KIT-14; não será duplicada nem executada por esta frente. Encaminhamento: registrar t_a41dd22d como pai de KIT-14 e aguardar sua conclusão revisada, que depende antes da resolução medida de SEG2. A transição de board será reconferida após a escrita.

Não pedir KIT-G2/A/B de novo. A autorização in-process existente não elimina a necessidade de resolver o crash e revisar o instrumento. Nome da configuração `CliqueFisico` não significa que um clique de mouse físico foi executado nem prova raycast/oclusão completos. Clique de sistema continua proibido nesta sessão; o residual físico/design permanece no runbook do dono.

## Cobertura desta retomada

PASSOU: leitura de task/pais/filho de revisão, presença e hashes de artefatos, ausência de processo do jogo e lock runtime na sondagem.
INDETERMINADO: eficácia runtime da build nova (nenhum boot desta retomada).
NÃO_EXERCITADO: clique físico → janela → conteúdo/tooltip → PNG → relatório; Runner positivo/negativo; mod sem kit; performance comparável; segundo ambiente; aceite visual humano. Offline/install/update/remove/rollback do run699 não repetidos e não atribuídos a esta build nova.

Steam Cloud não foi alterada e seu estado atual não foi medido nesta retomada; não alegar OFF/ON com base em medições antigas. Saves/perfil/junction não foram manipulados, e não houve snapshot novo que prove igualdade com baseline histórico. A deriva legítima do dono documentada em SEG1-RT não será revertida: a futura rodada exige snapshot imediato antes/depois, declaração da troca e preservação dos dois conjuntos/bytes/hashes.

## Arquivos desta retomada e próximo passo

Novos: docs/automacao/KIT-14-parte43.md, KIT-14-parte44.md e este KIT-14-entrega-run721.md. Nenhuma edição de código, build, boot, instalação, commit, publicação, teste novo ou número de performance produzido.

Após SEG2 e SEG1-RT concluídos/revisados, retomar só cenários faltantes em ambiente isolado: conferir Cloud atual/frente/junction, congelar identidades, usar baseline pessoal imediato sem restaurar snapshot antigo, coletar recorder e export antes do rollback, recapturar pós-navegação e instalar RSTV identificado somente no perfil temporário. Base com/sem recorder deve ser comparável; limiares permanecem dispensados e dado ausente não vira estimativa. Não concluir/liberar KIT-14R antes de cumprir o aceite técnico.
