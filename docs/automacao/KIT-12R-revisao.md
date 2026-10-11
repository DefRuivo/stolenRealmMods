# KIT-12R — parecer independente: REPROVADO (OFFLINE)

Cartão `t_811b1717`; revisor `default/run674` (instância nova, não autor). Produto atual implementado por `default/run671`, pai `t_0a434c97`; revisão anterior `run672` não substitui esta execução. Data local medida na abertura: 10/10/2026, 01:25:47 UTC-03. Autorização de 07/10/2026: somente implementação/revisão offline, sem runtime, instalação ou publicação.

## 1. Resultado e critério de conclusão

Revisão concluída com **cinco grupos de achados F1R–F5R** e **seis testes próprios reprovados**. Não há aprovação técnica de KIT-12. A suíte do autor e sua demonstração passam, mas não cobrem as fronteiras refutadas abaixo. Ausência técnica não pode ser verde.

Correção por nova instância: **KIT-12F `t_51ca208a`**, seguida de reconferência independente no próprio cartão. Gate adicional **KIT-12F -> KIT-15 `t_10584ca5`** criado antes do encerramento deste parecer; terminar a revisão não libera consumo de produto reprovado. Único perfil disponível medido: default; não houve alteração de modelos, prioridades ou controlador.

### Parecer por critério de aceite do pai

| Critério | Parecer | Prova e fronteira |
|---|---|---|
| C1: hash/versão/config/sessão na cadeia; mudança invalida aprovação | ACHADO / FALHOU | Propagação, contradição declarada e invalidação fonte/DLL/config/versão passam; **config solicitada ausente** e **probe explicitamente solicitado ausente** podem aprovar (F1R/F3R). |
| C2: lacuna técnica ao agente; humano só autorização/julgamento residual | ACHADO / FALHOU na omissão de lacunas | Lacuna de coleta emitida vai ao agente; limite escala ao supervisor. Porém ausências F1R/F2R/F3R não viram lacunas/fila, e entrada F4R dá traceback em vez de rota técnica. Não foi observado envio automático destas tarefas ao dono: o defeito é omitir trabalho técnico. |
| C3: fila declarativa com critério/paths/prova, limite/sem progresso; sem comando LLM arbitrário | ACHADO / FALHOU no saneamento | Causa/prova, limite e sem progresso passam. Nenhum comando proposto foi executado. **Critério OK mantém os nove campos executáveis** (F5R); contrato de transporte não é cumprido em todos os estados. |
| C4: validação/relatório deterministas sem IA; Hermes opcional | ACHADO / FALHOU na disponibilidade do relatório | Determinismo JSON (exceto gerado_em) e texto passam; stdlib e Git sem IA/Hermes/rede. **Relatório ausente ou com erro IO aprova** (F2R). |
| C5: CLI integrada sandbox, fixture marcada, erro -> correção -> revalidação sem fingir runtime | OK / PASSOU nos cenários exercitados | CLI real exits 2->1->2->2->2->2->3; defeito removido não vira prova runtime. Fixture no avaliador real: INCOMPLETO/2 e com_prova_runtime=0. Entrada malformada adicional F4R não passa. |
| C6: identidade viva, revisão independente, provas discriminantes e preservação | OK / PASSOU | Quatro hashes do handoff confirmados, inventário523 fontes/deps vivo/sandbox sem deriva; testes/exits e controles próprios abaixo. Produto não editado pelo revisor. |

## 2. Identidade dos arquivos vivos (SHA256)

Inventário real e cópia tracked/untracked de tools em sandbox própria, sem .git remoto, perfil/credenciais do dono; excluídos caches/bin/obj/arquivos de segredo. Apenas envelope JSON AUT-4 foi copiado como referência de formato, não como coleta nova/runtime.

- `tools/automacao/kit12/integracao.py`: `7785d8c1f624ff263b4ac89ad36e3ab9952db17d5a233d12affada091da8af87`
- `tools/automacao/kit12/pertinencia.json`: `b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320`
- `tools/automacao/kit12/prove_ciclo.py`: `4fc01b81572bdfbbea4cc3af33f1fb845659f23bc689cc94068e2d85b973b750`
- `tools/automacao/kit12/test_kit12_integracao.py`: `25284c7075633042efc6445a5856d5a24e40d152ccdb593d6cb94d661e96da8c`
- Envelope de referência copiado: `5bef1c67e21365ccf84d02ff645715e254a4e1140aec77d62c6b12de689a158d`.

Hashes são medidos, não apenas copiados da entrega. Identidade e baseline em `scratch/kit/KIT-12R-run674/identity.json` e `baseline.json`. Verificação própria: **523 arquivos**, `live_drift=[]`, `sandbox_drift=[]` em `final-verification.json`. Sandbox Git init exit0, remote-v exit0 com saída vazia. HEAD/branch vivos mantidos; nenhum add/commit/push.

## 3. Achados bloqueantes reproduzidos

Todos os JSON abaixo estão em `scratch/kit/KIT-12R-run674/effects/`. Oráculo independente: `test_review_kit12.py`; saída da suíte `review-suite.txt` e negativos individuais `individual-negatives.json`.

### F1R — config explicitamente requerida ausente ainda aprova

Raiz: `tools/automacao/kit12/integracao.py:347`–354 registra configs_ausentes, mas os guards `:900`–905 não invalidam essa insuficiência. `required-config-absent.json`: **APROVADO_OFFLINE/exit0**, config_sha=null, configs_ausentes preenchido, somente critério review/offline, nenhuma lacuna config.

Teste `test_missing_required_config_never_green`: Ran1, FAIL1, exit1. Controle equivalente com config existente aprova offline. Corrigir: arquivo de config **explicitamente solicitado** e não medido deve produzir lacuna técnica nomeada + fila agente + INCOMPLETO/2. Config não fornecida/opcional não deve virar nova dependência obrigatória. Cobrir múltiplas configs com ausência parcial.

### F2R — relatório ausente ou com exceção de montagem ainda aprova

Raiz: classificação em `integracao.py:1073` ocorre antes do relatório `:1075`; `_relatorio` em `:1131`–1147 retorna disponivel=false sem alimentar critério/fila/exit. `report-absent.json` e `report-io-failure.json`: **APROVADO_OFFLINE/exit0**, relatório indisponível, nenhuma lacuna relatório.

Dois testes próprios reprovam separadamente ausência e OSError (cada Ran1/FAIL1/exit1). Controle com relatório presente aprova. Corrigir: relatório obrigatório indisponível deve impedir aprovação, preservar motivo e emitir lacuna técnica/fila agente/exit2, sem fabricar texto.

### F3R — probe explicitamente solicitado ilegível cai em fallback e aprova

Raiz: `integracao.py:443`–445 retorna instrumento nulo/probe-ilegivel; confronto `:627`–669 permite alias DLL sem guard da medição explicitamente solicitada. `explicit-probe-absent.json`: **APROVADO_OFFLINE/exit0**, dll_probe_sha=null e origem=probe-ilegivel, sem lacuna instrumento.

Teste `test_requested_probe_missing_not_silently_green`: Ran1/FAIL1/exit1. Probe medido presente é controle positivo; mudar seus bytes produz **INCOMPLETO/2** e lacunas contraditória/incoerente; restaurar volta APROVADO_OFFLINE/0. Corrigir: --probe-dll solicitado e não medido exige lacuna/exit2, sem fallback silencioso. Não confundir com limite já declarado e permitido de instrumento **meramente declarado sem medição solicitada**.

### F4R — tipo inválido em observacoes aborta a CLI sem resultado técnico

Raiz: `integracao.py:477` itera campo observacoes sem validar container. Coleta com observacoes=7: **CLI real exit1, traceback=true, result_exists=false** (log `effects/malformed-cli.txt`), não INCOMPLETO/2 com causa técnica/fila.

Teste `test_malformed_observations_integer_closed` converte essa exceção em AssertionError de contrato: Ran1/FAIL1/exit1, não ERROR nem aprovação. Confirmado sem mock na CLI. Corrigir: validar formatos aceitos e elementos, declarar entrada inválida como lacuna técnica; persistir resultado estruturado, não misturar falha de infraestrutura com REPROVADO de produto.

### F5R — saneamento só alcança critérios que geram item de fila

Raiz: `integracao.py:926`–945 percorre itens da fila; CIC-1 `tools/automacao/ciclo/ciclo.py:725`–727 só monta REPROVADO, e `:764`–768 só acrescenta falhas automáticas. OK válido não produz item, portanto não é saneado.

`command-fields-OK.json`: **APROVADO_OFFLINE/0**, nove campos residuais: comando, argv, shell, exec, cmd, subprocess, script_correcao, comando_correcao, correcao_comando. Nos outros três estados (`command-fields-REPROVADO.json`, `-NAO_EXERCITADO.json`, `-INDETERMINADO.json`), resíduos=[] e propostas registradas. Teste com instrumentação subprocess não viu execução de conteúdo proposto. **Não há execução arbitrária demonstrada**; há violação do contrato de saneamento e transporte.

Corrigir: sanear todos os critérios antes de decisão/relatório/serialização, independente de estado/fila. Conservar propostas em localização explicitamente não executável mesmo sem item de fila. Reprovar tentativa de executar conteúdo sem apagar auditoria.

## 4. Execuções e controle negativo (saídas reais)

Base de evidências: `C:/dev/stolen-realm/scratch/kit/KIT-12R-run674/`. Comandos executados via terminal, subprocess com stdout+stderr/exits preservados. Não houve code_execution.

| Comando/controle | Resultado observado | Arquivo |
|---|---|---|
| python sandbox/tools/automacao/kit12/test_kit12_integracao.py | Ran30 tests / OK / exit0 | suite.txt |
| mesmo --isca | 14/14 discriminadas; cada mutante exit1, controle restaurado0 | isca.txt |
| python sandbox/tools/automacao/kit12/prove_ciclo.py --out .../cli | PROVA\|PASSOU, wrapper0; etapas2->1->2->2->2->2->3 | cli.txt; cli/prova.json; executions.json |
| python test_review_kit12.py | Ran17; 11OK/6FAIL, ERROR0/skip0, processo1 | review-suite.txt; review-suite-exit.json |
| seis negativos individuais | 6/6 Ran1, FAIL1, exit1 exato; sem ERROR/skip | individual-negatives.json; effects/test_*.txt |
| python review_controls.py | 10 controles0->1->0; uma mutação redundante fixture0->0->0 NÃO discriminou; exit1 honesto | own-mutants.json; own-mutants/ |
| python record_effects.py | efeitos persistidos; controle fixture v2 efetivo0->1->0; harness0 | observed-effects.json; fixture-control-v2.json |
| python verify_delivery.py | 523 fontes/deps intactos vivo/sandbox; 11 controles próprios discriminantes; scan dirigido109 arquivos/0achados; controle scanner positivo detectado | final-verification.json; directed-scan.json |
| check_segredos/check_padroes_segredo/check_dupes/audita_docs | exit0 cada; scanners Git874 versionados | gates.json; gate-*.txt |

Primeira tentativa de mutação fixture **não conta como prova discriminante**: KIT-10 já rebaixava fixture. História preservada. A segunda muda a classificação para promover lacuna/fixture a verde; teste real da fixture então reprova. Os **11 testes próprios verdes** têm controles negativos seletivos; os **6 vermelhos** foram confirmados individualmente. Não afirmar cobertura individual negativa dos 30 testes do autor a partir de só14 mutações.

Controles APROVADO_OFFLINE usam avaliador OFFLINE injetado como seam na costura verdadeira, com arquivo de evidência da sandbox: **não representam build, coleta real, jogo ou aprovação runtime**. As provas CLI/fixture/malformed usam avaliador real. Fonte vivo não foi alterado para fabricar aprovação.

## 5. Reuso, segurança e limites

Inspeção AST própria do código vivo: somente dois subprocess neste módulo — git status e git diff com argv explícito, sem shell=True. CIC-1/CIC-2/KIT-10/AUT-7 são importados por caminho, sem backend IA novo. Determinismo canônico e relatorio_texto confirmado; timestamps excluídos como campo declarado. Não depende de Hermes/IA/credencial para executar testes/CLI básica.

Scanners Git não cobrem untracked. Scan dirigido adicional usou motores **vivos** de formatos/entropia sobre109 arquivos explícitos incluindo produto untracked, docs próprios, scripts e provas; zero achado, ambos motores detectam sentinela sintética mantida só em memória, sem valor em log/arquivo. Isto não é garantia universal de anonimato.

Dívidas F3/F4 do parecer anterior permanecem separadas: REPROVADO com declaração incoerente normalizado como lacuna e --verificar sem repetir --config gera falso INVALIDADO (fail-closed). Não são os novos achados F1R–F5R, que abrangem falsos verdes e saneamento. Hash/bytes do produto e dependências conferidos após as mutações próprias.

**NAO_EXERCITADO / INDETERMINADO fora do escopo:** jogo/AUT-4 runtime novo, probe instalado, perfil/save do dono, eventos/frames/pixels/UIUX/personagem real/desempenho, build C# e preflight de deploy, instalação/publicação, gates KIT-G1..G4 e aceite humano/DoD. Nenhuma autorização de runtime/deploy/publicação foi inferida. Propriedade do perfil não foi medida por hash: não alegar isso.

## 6. Próximo passo e fronteira do handoff

Implementador NOVO no KIT-12F deve reproduzir baseline17=11OK/6FAIL e tornar **o mesmo oráculo imutável17OK**, sem ERROR/skip, preservando positivos, contra-provas, CLI e travas. Depois kanban_request_review com autoria/hash/path/exit; outra instância refuta F1R–F5R antes de concluir correção. Revisor674 não implementará seus próprios achados.

Encerrar KIT-12R significa **parecer REPROVADO concluído**, não KIT-12 aprovado, nem mod DONE, nem permissão de empacotar/publicar. Partes01..06 e logs antigos permanecem íntegros. O gate adicional de correção mantém KIT-15 dependente do conserto revisado.
