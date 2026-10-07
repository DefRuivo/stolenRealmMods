<!-- Integracao do pai t_8bfbe932 (run 389). Corpo inalterado; cabecalho + Adendo sao os unicos acrescimos. -->
> **Integracao — pai `t_8bfbe932`, run 389, 2026-10-05 20:47 UTC-03.** Este arquivo substitui o parecer anterior do
> mesmo caminho, preservado byte a byte (SHA-256 `b28838ad7471090d3502f314ad43ca7d74c0de9f37a629dde89b0742663d2afc`) em
> `docs/automacao/historico/CIC-3R-revisao-2026-10-05-1828.md`. O corpo abaixo e **byte a byte** o
> parecer consolidado pela tarefa `t_52fc84cc` (run 378), SHA-256
> `d8534ec999ed5bfd67291a10bcce4d81b56627014c210fb63d899b5a8812f1d1` — sem nenhuma alteracao de conteudo.
> O `## Adendo` no fim e a verificacao independente do integrador sobre os bytes congelados.
> Nada de produto, probe, jogo, build, deploy, save, commit, push ou publicacao foi tocado aqui.

# CIC-3R — parecer consolidado e reancorado

Data: 5 de outubro de 2026. Consolidação: t_52fc84cc, run 378, profile default. Destinatário e único integrador: pai t_8bfbe932. Produto examinado: CIC-3, t_7fdce47f.

## Conclusão executiva

**ACHADO: o avaliador CIC-3 não sustenta aprovação do aceite nos bytes preservados abaixo.** A execução OFFLINE reproduziu falsos OK de leitura somente incompleta, contagem malformada de duplicatas, confronto de dependências, geometria não finita, identidade contraditória, renderização não observada e agregação de sessões distintas. Quatro casos atravessaram as duas CLIs reais como OK_VINCULANTE por critério; nenhum tornou a decisão global pronta. Não foi demonstrado defeito do mod em jogo.

**INDETERMINADO: independência nominal do revisor em relação ao autor.** O registro de autoria está incompleto. Este é impedimento de ateste independente, não aprovação tácita. A entrega deste documento conclui somente a consolidação; não fecha CIC-3, CIC-3R pai ou o DoD de qualquer mod.

**Runtime: NAO_EXERCITADO. DoD do mod: não atestado.** Fixtures e identidades sintéticas, mesmo acompanhadas por arquivos reais e hashes, não comprovam funcionamento em jogo.

## 1. Escopo, regras e independência

Normas lidas diretamente: docs/automacao/CICLO-VALIDACAO-escopo.md:3-34; docs/SUPERVISAO.md:48-88,112-121; docs/PROCESSO-REVISAO.md:17-44. PROCESSO-REVISAO.md está em docs/, não na raiz.

Escopo: consolidar a auditoria t_d2be694f/run 374 e a execução adversarial t_be5e8bc2/run 375; verificar os arquivos brutos, reproduzir a execução congelada e emitir um único artefato documental. Revisão de somente leitura do produto: nenhum fonte, teste, fixture de produto, probe ou documento no repositório foi editado. Este parecer fica no workspace para integração exclusiva do pai. Não se modificou KANBAN.md, estados de cartões de produto ou outro board; apenas a transição de entrega da própria tarefa é necessária ao lifecycle.

Sem build, deploy, instalação de probe, jogo, save de jogo, commit, push ou publicação. Escritas restritas ao workspace: reprodução OFFLINE em consolidacao378/ e este documento. Configuração, perfil e arquivos do dono não foram modificados. Não se ampliou DoD nem se impuseram observações secundárias.

Consulta direta ao cartão t_7fdce47f confirma assignee=null, runs de implementação 335/346/355 com profile=null e review_requested com implementer=null. Revisores 374/375 e consolidador 378 têm contextos novos, e não houve participação na implementação nestes contextos. Isso não comprova a identidade administrativa de quem implementou. Diferentes run/PID/lock e comentários assinados default não bastam para demonstrar agente diferente. Estado de independência: INDETERMINADO; obter provenance pelo pai antes de qualquer assinatura de aprovação. Não afirmamos que autor e revisor sejam iguais: falta comprovação de que sejam diferentes.

## 2. Evidência preservada e atualidade

Workspace-base W: C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_8bfbe932.

Insumos e resultados examinados:

- W/t_d2be694f-auditoria.txt: matriz de auditoria, leitura de contratos e lacunas. Não executou testes.
- W/exec375/HANDOFF.txt e W/exec375/resultados.json: execução original 20:15:56–20:16:00 UTC-03, comandos, argv/cwd, identidades, observações, critérios e decisões.
- W/exec375/snapshot/: bytes preservados dos fontes/dependências/documentos usados. Todas as referências de código abaixo remetem a esta cópia, não a um disco futuro mutável.
- W/repro375/resultados.json: reprodução do executor sobre a cópia congelada.
- W/consolidacao378/resultados.json e logs/inputs/outputs adjacentes: reprodução própria do consolidador, sem confiar apenas no relatório do executor.
- W/cic3_exec_375.py: mestre de reprodução inspecionado integralmente antes de executá-lo. Seu campo revisor_run=375 é constante de origem do script; a execução consolidacao378 pertence ao run 378, não representa um novo run 375.
- Arquivo durable de evidências upstream: C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_be5e8bc2/CIC3R-exec375-evidencias.zip. SHA-256 reconferido pelo consolidador: bf13be4bafe2cfac9fd4a035fb25344d1a763f46c2e4a9fe00a9ccf90d3b459a. O pai deve preservar também a reprodução consolidacao378 ao integrar; ela não faz parte desse ZIP upstream.

SHA-256 dos bytes efetivamente exercitados:

| Caminho relativo à origem/snapshot | SHA-256 |
|---|---|
| tools/automacao/cenarios/rstv.py | 524f719757977436b843bdceb8337b10db4003cba9da64ff3fea788ef327d320 |
| tools/automacao/cenarios/test_rstv.py | 2dd71104c8b3a81d9ded38ea2e44baa33a30fb4f0df0bfe5c9f64b85161a4969 |
| tools/automacao/cenarios/rstv-positivo.entrada.json | c5d06592a67276359b5f64699dba8452c97b02084efcf02a3fe7e1ad64ab64e0 |
| tools/automacao/ciclo/decisao.py | d6de959e73a090e43da2b5438a12ba1739d32be2bd9494c0fe9f0d84d9163933 |
| tools/automacao/runtime/coletor.py | 0518634edaa70930a8f8173151d84aee8c20a5523fcffd9ad5842b6d5ff1faca |
| tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs | a2bd3d49ceab1ddfe31bdbdb8fa9d56b86003f8b529d2da22ad0042700718254 |

O JSON bruto contém todos os hashes de dependências, não somente os seis acima. Conferência própria em 20:19:42 UTC-03: nenhum mismatch encontrado nos arquivos preservados presentes; os cinco fontes centrais (avaliador, teste, decisão, coletor, probe) ainda coincidiam com a origem C:/dev/stolen-realm. Conferência final desta consolidação é registrada na seção 10.

Durante a execução original mudou apenas tools/automacao/aut5/cenarios-rstv.json. Portanto a revisão vale para o snapshot medido, não atesta o plano ao vivo posterior. Na reprodução congelada do executor e na reprodução própria não houve deriva. HEAD observado upstream f526fe9 é contexto, não identidade suficiente: tools/automacao e docs/automacao estavam untracked. A cópia e seus hashes tornam estes bytes recuperáveis sem exigir commit proibido.

O parecer anterior no repositório é histórico/desancorado: declara prefixos 748bee8b/ada45fee/836b08c8/cab67bc1/5605b1fa, diferentes dos arquivos acima. Este documento propõe sua substituição pelo pai, sem apagar os registros anteriores. Não se transporta seu veredito B1–B5 nem suas linhas para o código novo.

Atualização importante: o probe atual já tem emissão de snapshots, dados de tooltip e viewport em FONTE (tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs:429-436,451-597,923). Não repetir a antiga afirmação de que esses campos não existem. Existência no C# não comprova DLL carregada, dados emitidos ou efeito no jogo.

## 3. Execução real e reutilização AUT-3/AUT-4

Ambiente medido: Python 3.14.7, Windows 11/Git Bash. Comando mestre original:

    cd "$HERMES_KANBAN_WORKSPACE" && python -B cic3_exec_375.py

Reprodução própria executada pelo consolidador:

    cd "$HERMES_KANBAN_WORKSPACE" && CIC3_REVIEW_SRC="$HERMES_KANBAN_WORKSPACE/exec375/snapshot" CIC3_REVIEW_OUT="$HERMES_KANBAN_WORKSPACE/consolidacao378" python -B cic3_exec_375.py

Retorno real: exit 0 do mestre; VARIANTES 24 ACHADOS 14 SUITES 11 MUDOU []. Exit 0 do mestre indica término da coleta, NÃO aprovação dos ataques: os 14 contraexemplos estão explicitamente registrados. Os 14 incluem a observação secundária de índice negativo; não são 14 bloqueios obrigatórios.

Cada comando abaixo usa python -B e cwd no snapshot da respectiva execução. Os logs têm o nome da suíte em exec375/ e consolidacao378/.

| Comando relativo ao snapshot | Exit final | Resultado observado |
|---|---|---|
| tools/automacao/cenarios/test_rstv.py | 0 | RESULTADO\|PASSOU |
| tools/automacao/cenarios/test_rstv.py --contra-prova | 0 | CONTRA-PROVA\|PASSOU; isca sempre-OK exposta pelos 10 controles |
| tools/automacao/ciclo/test_decisao.py | 0 | 127 checks, 0 falhas |
| tools/automacao/offline/testes/t_aut3_lib.py | 0 | 25 checks, 0 falhas |
| tools/automacao/runtime/testes/t_aut4_autorizacao.py | 0 | PASSOU |
| tools/automacao/runtime/testes/t_aut4_controle_negativo.py | 0 | PASSOU |
| tools/automacao/runtime/testes/t_aut4_costura_probe.py | 0 | PASSOU |
| tools/automacao/runtime/testes/t_aut4_manifest_rollback.py | 0 | PASSOU |
| tools/automacao/runtime/testes/t_aut4_observacao.py | 0 | PASSOU |
| tools/automacao/runtime/testes/t_aut4_plano.py | 0 | PASSOU |
| tools/automacao/runtime/testes/t_aut4_probe_contrato.py | 0 | PASSOU |

AUT-3: reaproveitado aut3_lib.run_cmd/avalia para subprocessos, classificação de exits e testes de ausência/timeout/exit inesperado. Não rodamos bancada completa, seis builds ou ciclo E2E; o relato AUT-3R3 anterior é contexto, não execução desta consolidação nem assinatura nova de log antigo.

AUT-4: testes puros reais de autorização, normalização, costura, controle negativo e manifest/rollback, com coletor real importado pela suíte RSTV e fixture de probe. Isso é costura OFFLINE exercitada, não coleta runtime. A suíte t_aut4_execucao.py e o runner completo foram omitidos conservadoramente porque incluem instalação/config e lançamento de stub autorizado em perfil sintético. Não foram contabilizados como verdes.

AUT-5: reuso dos critérios/cenários S1–S5 e leitor log_rstv previsto pela auditoria. Plano ao vivo sofreu alteração; seus totais de log não comprovam dependências desenhadas por tier. Não assinamos rodada completa AUT-5 nesta consolidação.

Falha ambiental upstream explicitada: a primeira cópia parcial omitiu tools/checa_shrines.py, e test_decisao retornou exit 1, 125 checks/1 falha. O executor completou apenas o snapshot com scripts tools/ e tools/dados; a execução final e ambas as reproduções retornam 127/0. Não houve correção no produto, nem se ocultou a tentativa malsucedida.

## 4. Rastreabilidade das sete capacidades

Estados nesta matriz são parecer de auditoria, não os estados que o próprio produto declarou. Todos os critérios runtime permanecem NAO_EXERCITADO em jogo.

| Critério / obrigação | Evidência e refutação | Parecer |
|---|---|---|
| RSTV-6-readonly-personagem: personagem igual ao alvo independente | tools/automacao/cenarios/rstv.py:393-424; suíte executada contém controles/lacunas. Conferência de nome presente, mas não prova dono do level-up/modal ou personagem diferente do CurrentlySelectedCharacter em S3. | OK limitado à presença do confronto OFFLINE; runtime INDETERMINADO. Não demonstrado E2E. |
| RSTV-6-readonly-skills-pontos: ambas dimensões inalteradas antes/depois | tools/automacao/cenarios/rstv.py:444-508. skills_sem_pontos e pontos_sem_skills fecham OK/OK_VINCULANTE. O teste aceita par somente skills, mas o critério anuncia skills/pontos completos. | ACHADO F1. |
| RSTV-21-janela-ciclo: abre E fecha | tools/automacao/cenarios/rstv.py:513-538; controles exercitados pela suíte RSTV. Flags são conferidas, porém não provam sequência/cena real, X/Esc ou retorno ao dono no jogo. | OK restrito aos controles OFFLINE; runtime INDETERMINADO. |
| RSTV-21-tooltip-restauracao: pai/índice restaurados E sem duplicata | tools/automacao/cenarios/rstv.py:543-583. duplicadas_null/negativo/false/lista aceitos; duplicada=1 reprova. | ACHADO F2; índice negativo é secundário separado. |
| RSTV-26-placeholders: ausência no texto renderizado | tools/automacao/cenarios/rstv.py:588-623. cru_sem_render fecha OK e motivo “tooltip renderizado resolvido” sem render observado; '*0' renderizado reprova. | ACHADO F6. Não cobrar reprovação do template legítimo: cobrar distinção entre não observado e resolvido. |
| RSTV-25b-dependencia: linhas condizem com Dependency; T5 sem Dependency legítimo | tools/automacao/cenarios/rstv.py:628-670. T4=1 linha/3 dependências e valores 'abc'/-2 aceitos; T5=0/0 preservado como positivo sintético. | ACHADO F3 em valores inválidos; equivalência de contagens requer decisão explícita do pai caso regra seja só presença. |
| RSTV-geometria-clipping: bbox em tela e dimensões positivas | tools/automacao/cenarios/rstv.py:675-722. x ou largura='NaN' aceitos; x=-0.5 aceito e -0.5001 reprovado respeitam tolerância vigente. | ACHADO F4; nenhuma nova régua de clipping exigida. Não comprova design. |

## 5. Variantes novas e contraexemplos

Método: usar observações sintéticas com flag sintetico=true e aviso de fixture, injetando procedencia=runtime para exercitar o ramo positivo, como o teste positivo do autor. fonte_sha=a*64, dll_sha=b*64, config_sha=c*64 são valores sintéticos, não hashes medidos do jogo. Os arquivos de evidência e manifest existem, mas seu conteúdo não veio do jogo. prova_runtime=true é declaração do avaliador atacado, não conclusão do revisor.

F1 — dimensão inteira nunca lida: skills_sem_pontos e pontos_sem_skills produzem OK/OK_VINCULANTE; ausência de um par inteiro é ignorada. Esperado: não afirmar ambas dimensões completas quando uma não foi observada. Localização: tools/automacao/cenarios/rstv.py:451-453,479-482.

F2 — contagem inválida tratada como zero: duplicadas_null, duplicadas_negativo, duplicadas_false e duplicadas_lista produzem OK/OK_VINCULANTE. A chave presente basta; a validação procura somente número positivo ou duplicata=true. Esperado: contagem observada válida para provar ausência. Localização: tools/automacao/cenarios/rstv.py:555-575.

F3 — truthiness em vez de confronto válido: dependency_contagem_diferente (T4 linhas=1/Dependency=3) e dependency_valores_invalidos (linhas='abc'/Dependency=-2) produzem OK/OK_VINCULANTE na chamada normalizar_criterio. O próprio esperado anuncia linhas == Dependency. Se o desenho de produto exige apenas existência, o pai deve fixar essa semântica e não tratar 1/3 isoladamente como correção compulsória. Tipos inválidos não sustentam o confronto em nenhuma dessas leituras. Localização: tools/automacao/cenarios/rstv.py:647-667.

F4 — valores não finitos: geometria_nan_x e geometria_nan_largura produzem OK/OK_VINCULANTE. 'NaN' é uma string JSON válida convertida por float(); as comparações não demonstram dimensão positiva/bbox dentro da tela. Esperado: dado mensurável finito, ou resultado não verde. Localização: tools/automacao/cenarios/rstv.py:682-691,702-715.

F5 — alias sobrescreve divergência explícita: hash_alias_contraditorio declara dll_sha=d*64 divergente e aliases bons b*64; produz OK/OK_VINCULANTE. _hashes_obs substitui o valor canônico antes de confrontar. Esperado: divergência declarada invalidar a cadeia, sem exigir infraestrutura criptográfica nova. Localização: tools/automacao/cenarios/rstv.py:223-254.

F6 — renderização não observada: cru_sem_render tem apenas texto_bruto='Deals [2] damage.' e produz OK/OK_VINCULANTE, com motivo de renderização resolvida. Template bruto pode ser legítimo, mas não prova o render. Localização: tools/automacao/cenarios/rstv.py:588-623.

F7 — sessões misturadas: sessoes_misturadas combina sessao-A e sessao-B; avaliar retorna OK e _extras copia a primeira sessão. Esperado: não apresentar observações de ciclos distintos como prova de um único ciclo. Localização: tools/automacao/cenarios/rstv.py:257-268,327-328,371-373. **Este caso não foi executado nas CLIs nem normalizado pelo decisor no mestre; não se afirma OK_VINCULANTE para F7.**

Observação secundária S1: indice_invalido, antes/depois=-1, produz OK/OK_VINCULANTE. Igualdade não prova índice válido, mas não exigimos isso isoladamente; F2 já bloqueia a capacidade por ausência de prova de contagem. Sem polimento compulsório ou pedido de validações adicionais fora do aceite.

Dos 24 casos, 14 não atenderam a expectativa do ataque; 10 atenderam. Os dez controles/positivos são CTRL_completo, CTRL_gasto, CTRL_fixture, CTRL_hash_diverge, CTRL_sem_identidade, CTRL_duplicada, CTRL_T5_sem_dependency, CTRL_geometria_limite, CTRL_geometria_fora_limite e CTRL_placeholder. Estados: completo/T5/limite OK sintético; gasto/duplicada/fora_limite/placeholder REPROVADO; fixture NAO_EXERCITADO/NAO_CONTA_COMO_PROVA; hash divergente INDETERMINADO; sem identidade NAO_EXERCITADO. Não são dez provas runtime.

### Propagação pelas duas CLIs

Para skills_sem_pontos, duplicadas_null, geometria_nan_x e hash_alias_contraditorio, comandos reais (P = snapshot, O = diretório da rodada, caso = um dos quatro nomes):

    python -B P/tools/automacao/cenarios/rstv.py --observacoes O/caso.input.json --identidade O/caso.ident.json --out O/caso.criterios.json
    python -B P/tools/automacao/ciclo/decisao.py --criterios O/caso.criterios.json --identidade O/caso.ident.json --repo O --resultado O/caso.decisao.json

Cada par: exits [0,1]; critério-alvo OK_VINCULANTE; pronto_para_decisao=false; seis falhas automáticas; zero pendências humanas. Arquivos e argv literais estão em resultados.json, inputs/outputs e *.cli0.log/*.cli1.log.

Conclusão exata: falso verde **por critério**, não aprovação global, publicação ou repasse integral ao dono. As outras seis capacidades não foram alimentadas nesses pares. Não executamos rodada futura com todas preenchidas; ela não pode ser inventada como aprovação global demonstrada.

## 6. Contrato transversal e seis itens de aceite

| Item normativo | Evidência / resultado | Parecer e limite |
|---|---|---|
| Contrato avaliar(observacoes, identidade), campos e IDs canônicos | Suíte test_rstv executada e código preservado; testes de esquema/conjunto/exceção. | OK restrito aos casos da suíte; não aprovação de todas as entradas possíveis. |
| Formato AUT-4 real, sem inventar campos | Import do coletor real e t_aut4_costura_probe verdes. Auditoria aponta dados de tooltip em campos versus acesso top-level e hash da DLL probe versus DLL RSTV. | INDETERMINADO para a cadeia runtime completa; hipóteses específicas abaixo, não falhas E2E medidas. |
| Fixture não prova runtime; ausência/malformado não OK | CTRL_fixture preserva NAO_CONTA_COMO_PROVA; F1/F2/F3/F4 contradizem completude/dado válido. | ACHADO no avaliador; procedência efetiva de toda a rodada é OFFLINE. |
| Cadeia fonte/DLL/sessão/config relevante e arquivo com hash | Arquivos reais/manifests sintéticos e CLIs verificáveis; controle hash divergente não verde; F5 ignora divergência e F7 mistura sessões. | ACHADO F5/F7; config observada não comprovada. Não assinar os valores herdados como leitura runtime. |
| Aceite 1: comandos/outputs reais e controles negativos | 11 comandos executados pelo predecessor e reexecutados pelo consolidador; plantios gasto/duplicata/clipping/placeholder e mutante sempre-OK. | OK quanto à execução selecionada; as refutações impedem aprovação funcional. Não suite completa do projeto. |
| Aceite 2: resultado ligado aos bytes atuais, mudança invalida | Snapshot, hashes completos, reproduções e confronto com origem; parecer anterior não coincide. | OK para a âncora desta rodada; não aprovação do disco futuro/plano AUT5 alterado. Nova mudança exige nova conferência/rodada pertinente. |
| Aceite 3: falha retorna ao ciclo, limite e motivo específico | CLIs retêm seis falhas automáticas por caso; aut3_lib testa exits/timeout. | OK parcial de roteamento no decisor; ciclo completo/limite/sem progresso INDETERMINADO nesta rodada. Não extrapolar adaptador para E2E CIC-1. |
| Aceite 4: humano recebe só residual, sem esconder falhas técnicas | Quatro decisões com zero pendências humanas e seis falhas automáticas. | OK nos casos executados para separar falhas; falso OK de um item compromete completude do relatório. ACHADO no gate, não cobrança humana de leitura técnica. |
| Aceite 5: sem deploy/jogo/save/publicação; build isolado/teto6 se houver | Não houve build ou ações proibidas; runner autorizado omitido, escritas apenas no workspace. | OK nesta rodada. Teto/flag de build não se aplicaram: nenhum build executado. |
| Aceite 6: revisão independente focada no aceite; secundários não bloqueiam | Contextos separados, provenance do autor ausente, S1 isolado. | INDETERMINADO/impedimento de ateste quanto à independência; escopo respeitado. |

Hipóteses de integração ainda não refutadas por execução específica nesta rodada: (a) normalizado completo de tooltip preserva a capacidade que o bruto permite? (b) cadeia AUT5/coletor distingue DLL do probe de DLL do mod, em vez de reetiquetar os hashes? (c) config_sha relevante foi observado ou apenas herdado da identidade? As suítes verdes não autorizam declarar estas três perguntas resolvidas. Reusar a costura existente no próximo trabalho, sem nova infraestrutura ou runtime não autorizado. O pai decide a relevância da configuração antes de exigir coleta adicional.

## 7. DoD obrigatório do mod: quatro portões separados

Fonte: docs/SUPERVISAO.md:64-88. Estes portões não são redefinidos pela automação, nem requisitos para executar a presente revisão OFFLINE. Impedem concluir o mod, não obrigam ação proibida nesta rodada.

| Condição obrigatória | Evidência disponível / falta | Estado | Responsável pela próxima decisão |
|---|---|---|---|
| D1: verificação humana em jogo confirmando efeito | Não houve jogo, carregamento/probe observado ou confirmação humana desta versão. Fixtures não suprem esse dado. | INDETERMINADO; runtime NAO_EXERCITADO | Pai agenda somente após gates técnicos e autorização; dono confirma efeito. |
| D2: nenhuma alteração ou decisão pendente no mod | Há achados técnicos F1–F7 e independência não comprovada; não se fez inventário completo das tarefas do mod. Git dirty não prova sozinho todas as pendências. | Não demonstrado; não declarar “sem pendências” | Pai identifica e resolve conjunto por mod, preservando mudanças do dono. |
| D3: nova versão na Thunderstore, publicação bem-sucedida aprovada pelo humano | Nenhuma publicação nova foi realizada/verificada; expressamente proibida nesta rodada. | INDETERMINADO/NAO_VERIFICADO | Pai mantém aprovação/publicação separadas; nada autoriza publicar agora. |
| D4: design de UI/UX e confirmação do dono no jogo | Geometria sintética não avalia contraste, layout, hierarquia, posicionamento ou sobreposição real; não há parecer visual atual comprovado aqui. | INDETERMINADO; revisão visual NAO_EXERCITADA | Agente faz avaliação de design na rodada permitida; dono confirma em jogo. |

Sem fechar DoD por testes verdes, “compila e abre”, registro documental ou declaração do executor. Reuso do aceite de versão anterior também não foi demonstrado.

## 8. Bloqueios centrais, limitações e secundários

Bloqueios do aceite CIC-3: F1/F2/F4/F5/F6/F7 e valores inválidos de F3; independência indeterminada é impedimento adicional de ateste. São refutações do objetivo já definido (falso verde, ausência/malformado/identidade incoerente), não endurecimento secundário. A contagem 1/3 de F3 depende de esclarecer a semântica declarada, não de inventar régua nova.

Bloqueios para afirmar DoD do mod: os quatro portões da seção 7 não foram demonstrados. A revisão não tenta executá-los sem autorização.

Limites da prova: nenhum runtime; nenhuma bancada AUT-3 completa, builds, AUT-4 runner completo ou ciclo E2E nesta consolidação; fontes C# não provam binário ativo; nomes/flags não garantem contexto modal real; origem ao vivo mutável não recebe aprovação pelo snapshot. Ausências técnicas devem ficar na fila do agente, não ser transformadas automaticamente em leitura manual do dono.

Secundários não exigidos: índice negativo igual antes/depois (S1); redação de lacuna_probe obsoleta; ressalvas históricas sobre @x@ bruto, nome literal T5 e rótulo de falta técnica. Não cobrar polimento, commits, novas abstrações ou segurança criptográfica adicional. Config relevante e hipóteses de costura só viram obrigação específica quando o contrato/evidência de integração as tornar necessárias.

hotspot: tools/automacao/runtime/coletor.py e tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs — mudaram desde round2b; a costura anterior não atesta os bytes novos. Nenhum deles foi editado pelo consolidador. A reprodução atual usa seus bytes congelados e não resolve todas as hipóteses E2E.

## 9. Decisões e integração reservadas ao pai

1. Integrar este único parecer em docs/automacao/CIC-3R-revisao.md do repositório, preservando os registros anteriores como histórico e os artefatos executáveis/hashes. Não atribuir sua integração a este filho.
2. Recuperar provenance de quem implementou CIC-3 ou obter revisão comprovadamente não-autoral antes de assinatura independente. Contexto novo não substitui identificação ausente.
3. Encaminhar os achados centrais com inputs/saídas ao implementador; nova revisão após correção, sem enfraquecer controles existentes. Não alterar CIC-3 nem criar cartões por este filho.
4. Fixar a semântica do confronto de dependências (igualdade de contagens ou existência), compatível com o esperado declarado; valores inválidos continuam sem prova. Decidir configuração relevante antes de ampliar obrigação de coleta.
5. Tratar hipóteses de normalização e identidades distintas na costura reutilizada; não reassinar AUT-4R2 nem plano AUT5 alterado sem prova pertinente.
6. Manter ciclo E2E, confirmação humana, design, autorização e publicação como estados separados. Não devolver ao dono as correções técnicas automatizáveis.

Não há aprovação independente, runtime ou autorização de entrega neste parecer. Há evidência reproduzível suficiente para refutar a integridade do gate CIC-3 nos bytes declarados e orientar as decisões do pai.

## 10. Verificação final da consolidação

Conferência própria final em 2026-10-05T20:23:06-03:00: 11 suítes com exit 0, 24 variantes/14 contraexemplos, os quatro pares de CLIs com exits [0,1], classificação-alvo OK_VINCULANTE, decisão global não pronta, seis falhas automáticas e zero pendências humanas por par. Estados das 24 variantes idênticos à execução upstream. Os nove arquivos vigiados (seis âncoras da tabela e três normas) continuavam com os hashes da origem iguais aos do snapshot: nenhuma deriva nesse conjunto.

Comando documental efetivamente executado:

    python -B C:/dev/stolen-realm/tools/checa_citacoes.py W/docs/automacao/CIC-3R-revisao.md --verboso

Retorno: exit 0; 3 referências/menções C# conferidas em 1 documento, 0 pendências. Checagem programática complementar: 19 referências arquivo:linha/faixa Python/Markdown/C# encontradas, nenhuma fora do arquivo preservado. A ferramenta existente cobre C# (inclusive as três faixas/lista de linhas do probe); o complemento cobre os demais caminhos e faixas. Existência da linha não equivale a validação semântica: o corpo do código citado foi também lido diretamente.

O hash final deste parecer será registrado no handoff após esta atualização documental. Só o parecer é artefato documental novo desta consolidação; JSON/logs são evidências de execução. Não houve integração no repositório; ela permanece exclusiva do pai.

---

## Adendo — verificacao independente do integrador (pai `t_8bfbe932`, run 389)

Rodada propria de verificacao (lens=execucao + contrato) sobre os bytes congelados, sem editar
produto, probe ou o corpo acima. Nada de jogo, build, deploy, save, commit, push ou publicacao.
Evidencia crua: `review389/` no workspace da tarefa `t_8bfbe932`.

### A1. Reproducao propria da execucao congelada — confere

Mesmo mestre `cic3_exec_375.py`, agora com `CIC3_REVIEW_SRC=exec375/snapshot` (fonte congelada) e
`CIC3_REVIEW_OUT=review389/`:

| medida | resultado real |
|---|---|
| suites | 11, todas exit 0 (`rstv`, `rstv --contra-prova`, `decisao` 127/0, `aut3-lib` 25/0, 6 de AUT-4) |
| deriva durante a medicao | `MUDOU []` |
| variantes | 24 executadas / 14 contraexemplos — estados identicos aos do consolidador |
| pares de CLIs (4 casos) | exits `[0, 1]`; criterio-alvo `OK_VINCULANTE`; `pronto_para_decisao=false`; 6 falhas automaticas; 0 pendencias humanas |

### A2. Referencias — conferem no snapshot, nao no disco vivo do probe

`python -B tools/checa_citacoes.py docs/automacao/CIC-3R-revisao.md --verboso` -> exit 0
(3 citacoes C# conferidas, 0 pendencias). Conferencia propria, adicional, de 19 referencias
`arquivo:linha`/faixa deste parecer contra o snapshot: todas resolvem, com o construto esperado na
faixa (`_cap_skills_pontos` 444-508, `_cap_tooltip_restauracao` 543-583, `_hashes_obs` 223-254,
probe 429-436/451-597/923, etc.). Onde a citacao NAO resolve e no disco vivo: ver A4.

### A3. Variante NOVA do integrador — N1: verde GLOBAL com leitura incompleta (nao executada nas rodadas 374/375/378)

A conclusao executiva do parecer diz que os falsos OK chegaram "por criterio" e que "nenhum tornou a
decisao global pronta". Isso e verdade para rodadas de um criterio so. Alimentando as **sete**
capacidades com um unico ciclo sintetico coerente que carrega F1 (`pontos` nunca observados) e
F2 (`janelas_duplicadas: null`):

| medida (real) | resultado |
|---|---|
| `rstv.py` / `decisao.py` | exits `[0, 0]` |
| 7 criterios | todos `OK`, `prova_runtime=true`, `OK_VINCULANTE` |
| `pronto_para_decisao` | **true** — "SIM: automacao sem falhas e sem pendencia humana; resta aceite/publicacao" |
| falhas automaticas / pendencias humanas | **0 / 0** |

Contra-prova do MESMO instrumento (para provar que ele nao e carimbo): com pontos GASTOS (5 -> 4) e,
em rodada separada, com `janelas_duplicadas=1`, os sete criterios sao reavaliados e o criterio
afetado volta `REPROVADO`/`FALHA_AUTOMATICA`, com `pronto_para_decisao=false`. Ou seja: o funil pega
o defeito de VALOR, e nao pega AUSENCIA/MALFORMADO — a mesma classe F1/F2, agora medida no nivel
GLOBAL, com zero pendencia humana. O artefato positivo do autor (`rstv-positivo.entrada.json`,
`sintetico: true`) traz as duas dimensoes e a contagem `0`; e a versao incompleta que fecha verde.

Fixture rotulada (`sintetico=true`, procedencia `runtime` INJETADA, hashes `a*64/b*64/c*64`):
**nao e prova de runtime**. Evidencia: `review389/resultados.json`, `review389/n1/flags.json`,
`n1.criterios.json`, `n1.decisao.json`, `n1b.flags.json` e os scripts `review389/n1_variante_global.py`
e `review389/n1b_contraprova.py`. Efeito no veredito: **fortalece** o ACHADO do parecer (o gate aceita
leitura incompleta como verde) e **corrige** a frase de escopo — o verde global com zero pendencia
humana E alcancavel quando o ciclo e alimentado inteiro, que e como ele deve rodar na pratica.

### A4. Deriva desde o congelamento (risco residual)

O snapshot e a ancora valida e continua intacto, mas o disco vivo ja divergiu em um dos seis bytes
declarados: `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` = `afa4ee6daf6270b5…`
(mtime 20:32:11) contra `a2bd3d49ceab1ddf…` do snapshot. As quatro fontes Python centrais
(`rstv.py` `524f7197…`, `test_rstv.py` `2dd71104…`, `decisao.py` `d6de959e…`, `coletor.py`
`0518634eda…`) seguem iguais ao snapshot. `tools/automacao/` e `docs/automacao/` continuam
**untracked** (`?? tools/automacao/`, `?? docs/automacao/`, HEAD `f526fe9`): o que garante a
recuperacao desta revisao e o snapshot preservado no workspace, nao o git.

### A5. Riscos residuais e limites

- Independencia nominal: **INDETERMINADO**. O board do CIC-3 (`t_7fdce47f`) nao registra
  assignee/profile/implementer nos runs 335/346/355. Contextos novos (374/375/378/389) nao
  substituem essa identificacao; sem ela nao ha ateste de aprovacao independente.
- Runtime: **NAO_EXERCITADO**. Fixture nao e runtime; nada deste parecer prova o mod em jogo.
- DoD do mod: **nao atestado** (os quatro portoes da secao 7 continuam separados).
- Correcao pendente: F1-F7 seguem em aberto no produto; a reconferencia do CIC-3 e trabalho
  de outra rodada, com nova revisao apos o conserto.

### A6. Recomendacao objetiva sobre reducao de revisao humana

O ciclo pode substituir revisao humana repetitiva apenas nas classes que ele ja provou: controles
plantados (valor gasto, duplicata positiva, clipping fora do limite, placeholder literal), a
separacao entre falha automatica e roteiro humano (0 pendencias humanas quando tudo fecha) e a
ancoragem por identidade/snapshot. Para a classe de AUSENCIA/MALFORMADO (F1-F7) ele **nao pode**:
o mesmo funil que reprova o valor errado entrega verde global, sem pendencia humana, quando a
dimensao nao foi lida ou a contagem veio `null` (A3). Enquanto F1-F7 nao fecharem — e o verde
global nao exigir leitura completa e bem-formada de cada dimensao do criterio — o aceite humano
continua obrigatorio; o ciclo vale como reducao de trabalho no caminho feliz, nunca como substituto
do portao. Fechados F1-F7, a recomendacao e manter em maos humanas apenas o que e de fato humano:
autorizacao da rodada runtime, julgamento visual/UX e aceite/publicacao.
