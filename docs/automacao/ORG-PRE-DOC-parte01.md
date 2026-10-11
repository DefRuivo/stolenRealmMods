# ORG-PRE-DOC — parte 01: reconciliação documental e proveniência verificável

Cartão t_d803c318. Base auditada: 8b575c6024fe79cebed578382820c89f78a0124e, com ORG-R1 partes01..04 já versionadas. Data local medida no terminal: 11/10/2026. Implementação e testes offline; nenhum jogo, deploy, perfil/save, push ou publicação.

## 1. Resultado e errata das contagens herdadas

A CLI original foi reproduzida antes de editar: exit1, **37 pendências**, não35. A parte04 de ORG-R1 já registrava as duas adicionais; seus quatro documentos permanecem byte-idênticos no Git.

| Classe real da pendência | Quantidade | Tratamento |
|---|---:|---|
| Scripts privados de bancada/revisão apresentados pelo auditor como ferramentas de tools/ | 7 nomes | Proveniência por ocorrência exata no catálogo, sem promover scripts locais |
| Ferramenta existente em api/tools/, omitida pelo inventário limitado a tools/ | 1 nome | Resolver caminho explícito versionado, da raiz ou relativo ao documento; qualificar menção solta no README atual da API |
| Link do guia KIT-15 que não funciona na origem | 1 | Documentar os dois layouts e incluir o guia público que estava ignorado |
| Ocorrências do harness local não versionado em snapshots/comandos/logs | 27 linhas | Proveniência histórica exata, sem reescrever evidências |
| Regra scratch/old/ mencionada como política de ignore | 1 linha | Distinguir a instrução histórica de manter a regra de uma promessa de pasta no clone |

Errata de causa: as35 pendências anteriores a ORG-R1 eram **seis** nomes privados de bancada + **uma ferramenta real da API**, um link e27 ocorrências do harness. O nome privado adicional e a menção à regra de ignore elevaram a fotografia para37. Não são oito ferramentas que precisam ser criadas.

Depois do saneamento, a CLI integrada retornou exit0 no repo vivo e no clone. Os testes novos retornaram29/29 OK em ambos. A versão final com este documento e o guia nominalmente adicionados ao índice também é conferida antes do fechamento; commit exato e logs finais estão no handoff do cartão, não em um hash autorreferente neste arquivo.

## 2. Proveniência dos sete scripts locais, sem fingir entrega no clone

Estes são **scripts privados de bancada**, não ferramentas versionadas de tools/. Sua existência/origem foi conferida no disco; nenhuma cópia foi adicionada ao repositório.

| Script de bancada | Origem local conferida |
|---|---|
| audit_details.py | workspace Kanban t_adbb8f0d, produtor das medições ORG-R1 |
| review_controls.py | scratch/kit/KIT-08R-run648 e scratch/kit/KIT-12R-run674, com cópias nas revisões F |
| scan_headers_offline.py | workspace Kanban t_48d68679/repro-limpa, reprodução offline de EV-R1 |
| verify_delivery.py | scratch/kit/KIT-12R-run674, conferência privada da revisão |
| verify_handoff.py | scratch/kit/KIT-13-run661-final, conferência privada do checkpoint |
| verify_independent.py | scratch/kit/KIT-08F-run658, sonda independente da revisão |
| verify_review.py | scratch/kit/KIT-08R-run648, conferência privada de hashes/contagens |

Workspace Kanban significa `%LOCALAPPDATA%/hermes/kanban/workspaces/<cartão>/`; scratch acima é a bancada local gitignored sob a árvore de trabalho, não parte da distribuição. Hashes/tamanhos medidos dessas origens estão em origens-locais.jsonl nas evidências. Preservar a menção de um comando que já foi executado NÃO torna o script disponível no clone nem instrui o leitor a executá-lo agora. A extensão de um log .py.log também não declara uma ferramenta distribuída.

Separadamente, `api/tools/check_ui_contract.py` existe no índice. O desenho relativo `tools/` dentro de api/README.md aponta para essa ferramenta; a menção solta na prosa foi qualificada com o caminho da raiz. O mesmo basename em um caminho inexistente continua reprovando. Nenhum fonte/contrato da API foi editado.

## 3. Errata de leitura dos snapshots do harness

ReloadProbe é um harness local gitignored, não versionado e NÃO é um dos seis mods distribuídos. O clone desta tarefa não contém o projeto; ele não foi criado nem copiado para silenciar o auditor.

- INT-R1 partes01..06 mediram a árvore local e o quadro daquela rodada. A tabela intitulada7 mods conta o harness local entre os projetos medidos: não comprova sete pacotes distribuídos. Partes05/06 registram `git ls-files` igual a0 e o ignore; conservar essas provas, sem reescrever a fotografia antiga.
- KIT-03F/KIT-03G1/KIT-16/KIT-G1R descrevem builds, cópias isoladas e linhas de log daquela rodada, não arquivos disponíveis em todo clone atual.
- A frase fonte no repo de KIT-03G1-parte03 §4 era imprecisa: refere-se ao fonte presente na **árvore local do autor**, não ao conteúdo versionado. Esta errata corrige a interpretação sem adulterar a evidência histórica.
- A linha28 de ORG-R1-parte02 pede manter uma regra scratch/old/ no .gitignore. Não afirma que essa pasta privada esteja no índice. A política/fotografia original permanece intacta.

## 4. Regra estreita e falha fechada

`tools/audita_docs_proveniencia.json` contém **41 ocorrências em21 documentos**:13 linhas sobre sete ferramentas locais e28 linhas de caminhos/contexto histórico (27 do harness +1 regra de ignore). O número é maior que o de pendências porque a seção de ferramentas agregava o diagnóstico por nome, mesmo quando havia múltiplas linhas.

Cada registro declara documento, número de linha, classe, nome, origem, justificativa, SHA-256 da linha e SHA-256 do documento completo. Os hashes de texto normalizam CRLF/LF, para a identidade sobreviver a um checkout Windows/Linux sem ignorar mudança textual. O módulo `tools/docs_proveniencia.py` valida schema, campos, hashes, documento versionado e duplicatas; catálogo ausente, ilegível, inválido ou stale acrescenta erro ao auditor.

Não há skip de docs/automacao, isenção de arquivo inteiro ou permissão global por nome. A chave reconhece só a ocorrência daquela classe/linha/nome, naquele snapshot byte-equivalente após normalizar CRLF. Editar o documento, mover a linha ou adicionar uma instrução nova não herda reconhecimento. A manutenção exige nova análise de proveniência; não há atualização automática de hashes para aprovar narrativa nova.

A regra não se aplica a links relativos, versões, dependências, contagens nem às outras classes do auditor. Os checks existentes de contexto explícito de bancada não foram ampliados. A nova resolução de ferramentas fora de tools/ exige que **todos** os caminhos explícitos da linha existam no índice; um basename sozinho não basta.

## 5. Guia KIT-15: conteúdo público que faltava no clone

O guia já existia localmente em `tools/automacao/kit15/docs/primeiro-uso.md`, mas era excluído pela regra *.md de .gitignore. Seu conteúdo público foi lido antes de incluir; foi preservado byte a byte, **6680 bytes**, SHA-256 `92bf0a5e6e54cfa31e8007554845c21b26192d8dd6fe428904704c94dda0bcc1`. Não é script privado nem harness.

O README é copiado sem transformação para docs/README.md do pacote. Um link relativo a primeiro-uso.md só funcionava no pacote; um link a docs/primeiro-uso.md só funcionaria na origem. Agora o README apresenta os dois caminhos como texto e explicita cada layout. O guia foi incluído nominalmente no índice com force apenas para esse caminho, sem alterar .gitignore, globais ou qualquer outra frente.

Sem o guia, a suíte KIT-15 no clone falhou honestamente em test_14_modo_manual_sem_python_equivale_ao_instalador:17 OK/1 FAIL. Com o documento preservado na entrega, a mesma suíte ficou **18/18 OK**, exit0. A geração/verificação do pacote e o modo manual foram exercitados pela suíte; não houve instalação no perfil do dono.

## 6. Testes discriminantes e evidências

Comando: `python tools/test_audita_docs.py -v` — **29 testes**, exit0, zero ERROR/skip. Os testes de CLI executam o auditor real em repositórios Git sintéticos explicitamente declarados, sem harness privado, bibliotecas do jogo ou perfil. Os testes do catálogo usam temporários próprios.

Fronteiras comprovadas:

- ocorrência histórica exata aceita; outra linha/documento/nome/classe não herda aprovação;
- documento/linha/hash alterados, duplicata, identidade malformada, catálogo ausente/corrompido e documento não versionado reprovam;
- CRLF/LF equivalentes mantêm reconhecimento, sem afrouxar texto;
- ferramenta atual fictícia reprova, inclusive o mesmo nome privado em nova documentação e uma nova citação no próprio snapshot;
- caminho explícito da API versionado aceita; caminho errado com o mesmo basename ou arquivo existente só no disco reprova;
- referência atual falsa ao harness ou à pasta privada reprova;
- link realmente quebrado reprova, inclusive dentro de documento com ocorrência histórica reconhecida.

Provas preservadas no artefato ORG-PRE-DOC-evidencias.zip: baseline completo/JSON, coleta de origens, suítes/CLI, integração nominal com leitura de volta e fechamento. A primeira falha KIT-15 sem guia e as tentativas de contra-prova não foram ocultadas.

## 7. Descoberta fora do escopo: contra-prova D6 em checkout CRLF

A contra-prova original KIT-15 passa no repo vivo com fontes LF: **7/7**, exit0. No clone Windows core.autocrlf=true, baseline e suíte intactos verdes, mas D6 retorna MUTACAO-INVALIDA: **6/7**, exit1. A âncora textual multiline exige LF, enquanto aplicar_defeito lê newline='' e recebe CRLF. Medição: descoberta.py vivo215 LF/0 CRLF e âncora1; clone215 CRLF e âncora LF0.

Nenhum código do KIT-15 foi alterado para resolver ou esconder essa falha. Seguimento específico criado: **t_be4d89d9, KIT15-D6-CRLF**. Deve tornar a mutação real discriminante em ambos os checkouts, sem aceitar mutação inválida como RED. Isso não impede o aceite documental desta tarefa; também não autoriza declarar todas as suítes do projeto verdes no clone.

## 8. Preservação, integração e limites

Aplicação ao repo vivo condicionada à comparação com o conteúdo-base dos três arquivos existentes. Novos arquivos só foram copiados se ausentes ou byte-idênticos; o guia já presente não foi reescrito. O hotspot api/README.md foi declarado no cartão; alteração final nessa prosa é uma única qualificação de caminho. Ferramenta de segredos e documentos de outras tarefas permaneceram fora do stage nominal desta entrega.

Mudanças: auditor, módulo e catálogo de proveniência, testes novos, dois READMEs atuais, guia público e este relatório novo. Nenhum fonte C# de mod/API, .gitignore, snapshot histórico, pacote/binário de evidência ou script privado mudou. Nenhum git add -A/commit -a, movimento, exclusão, cached removal, deploy ou push.

Auditoria documental verde NÃO significa scanners de segredo/release/build/runtime globalmente verdes. ORG-PRE-SEG conserva a propriedade de tools/check_padroes_segredo.py; sua frente e o diagnóstico AUT5 continuam independentes. O filho preexistente ORG-R1-E1 mantém os gates de saneamento; a conclusão aqui libera somente esta dependência documental, sem duplicar a frente de organização.
