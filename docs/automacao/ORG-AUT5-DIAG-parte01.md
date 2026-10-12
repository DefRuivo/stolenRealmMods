# ORG-AUT5-DIAG — parte 01: causas separadas do baseline AUT5

Tarefa `t_ceceef6b`, investigação offline de 11/10/2026. Baseline histórico ORG-R1: `097f950677a02e964f7b43fc1b2998b8daa48c3c`. Árvore principal observada: `8b575c6024fe79cebed578382820c89f78a0124e`. Nenhuma correção implementada nesta investigação; nenhum build, deploy, jogo, bancada de boot ou publicação.

## Conclusão

A falha NÃO demonstra perda dos campos do instrumento congelado. Há três causas separadas: fixture de versão antiga contra fonte atual; testes estáticos presos a assinaturas/estrutura anteriores; teste de integração dependente da identidade dos bytes do perfil. A DLL do perfil existe: a hipótese de ausência não explica as duas mensagens de log-real medidas nesta rodada.

Há defeitos demonstrados FORA do instrumento, nos testes. Foi criado `t_2d9f22b1` (ORG-AUT5-FIX), especializado em contrato/parser AUT5, dependente da aprovação desta investigação, com pin `gpt-6.1-sol/openai-codex`. Não é dependência das frentes ORG-R2/R3/R4. A suíte `tools/automacao/aut5/test_aut5.py` não aparece em `.github/workflows/validate.yml` (arquivo completo, linhas 1–217); portanto este achado não constitui gate de CI da organização.

## 1. Procedência e escopo da prova

Evidência original: membro `baseline-test-aut5.txt` de `ORG-R1-evidencias.zip`, anexo do cartão `t_adbb8f0d`. O zip tem SHA-256 `cc8645c6ea998a52c18f9a8bca835e38e656d648e903ae351fd2c9bc46d7d061`. O membro foi lido sem modificar o zip nem o workspace do pai; uma cópia nova está em `ORG-R1-baseline-test-aut5-copia.txt`, no workspace desta tarefa.

A reprodução usou fontes da cópia isolada ORG-R1, preservadas byte a byte, e a DLL RSTV já existente nessa cópia. Não houve rebuild. Também foram lidos o fonte principal e os bytes do perfil, sem qualquer escrita neles. `diagnostic-evidence.json` registra manifestos, identidades, relatórios, casos e comparação com `source-hashes.json` da evidência original. O script novo `investigate_aut5.py` é a receita de investigação, não uma bancada runtime.

Comando executado a partir do workspace: `python -B investigate_aut5.py`, exit 0. Isso significa diagnóstico exercitado, NÃO suíte AUT5 aprovada. Foram executados 13 dos 16 grupos originais: 11 sem falha e 2 com as quatro mensagens esperadas (`positivo`, `log-real`). Os grupos `emissao-campos`, `snapshot-modal-CSharp` e `probe-normalizado` NÃO foram executados integralmente: contêm observações sintéticas com formato de runtime ou compilação indireta do harness. A emissão foi confrontada estaticamente; o harness foi chamado apenas até a rejeição original anterior à compilação. Uma trava de subprocessos estava ativa; tentativas de subprocesso após a trava: zero.

Todos os relatórios desta investigação têm zero critérios de classe runtime em OK. Nenhuma fixture recebeu sessão/hash ou procedência de runtime. Os registros locais modificados de versão continuam entradas OFFLINE, sem declaração de DLL. Não há aceite em jogo, visual ou do SEG2.

## 2. Causa A — fixture antiga, não ausência de hash

Pontos concretos:

- `tools/automacao/aut5/fixtures/log-completo.log:2` declara boot RSTV **0.3.2**.
- `RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj:14` declara **0.3.3**.
- `tools/automacao/aut5/test_aut5.py:86–119` exige INDETERMINADO para o boot da fixture e exit 2 para o relatório; seu comentário assume que a única lacuna é a ausência de identidade da DLL.
- `tools/automacao/aut5/aut5.py:308–314` reprova divergência de versão ANTES de tratar DLL não identificada em `:315–322`.

O avaliador está coerente com sua regra. É a premissa do caso positivo que deixou de corresponder ao repositório. A versão antiga já é um defeito suficiente; não pode ser apagada por falta de hash.

Matriz executada, mudando apenas a string da versão em logs LOCAIS do workspace:

| Entrada offline | Versão do log / fonte | Identifica DLL? | Boot | Exit do relatório |
|---|---|---|---|---|
| fixture intacta | 0.3.2 / 0.3.3 | não | REPROVADO | 1 |
| versão alinhada, sem perfil/hash declarado | 0.3.3 / 0.3.3 | não | INDETERMINADO | 2 |
| controle negativo antigo | 0.3.1 / 0.3.3 | não | REPROVADO | 1 |

A mesma fixture intacta também reprova com a árvore principal. Logo, este problema NÃO vem da cópia isolada nem da falta de AUT4Probe.dll. O controle positivo sem identificação da DLL NÃO vira OK; o controle negativo continua reprovando. Não foi editada a fixture versionada, a versão do produto nem o avaliador para conseguir verde.

## 3. Causa B — drift do parser/teste, campos presentes

`test_aut5.py:399` procura a assinatura literal `private Dictionary<string, object> Leitura(TMP_Text t`. A fonte congelada contém `internal Dictionary<string, object> Leitura(TMP_Text t, List<object> ownersFunil)` em `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs:718`. O acesso internal é documentado nas linhas 715–717 para reuso por `LeituraAgregados`.

O extrator da suíte (`test_aut5.py:365–382`) usa `find` da string inteira. Não achando a visibilidade private, retorna None. Daí as mensagens derivadas em `:400–404` dizem que os sete campos não são emitidos, embora todos existam no corpo real:

- snapshot_antes e snapshot_depois: fonte `:752–753`;
- tooltip_pai_antes e tooltip_pai_depois: `:754–755`;
- tooltip_indice_antes e tooltip_indice_depois: `:756–757`;
- janelas_duplicadas: `:758`.

O confronto diagnóstico localizou o corpo por sua assinatura REAL, sem alterar o fonte, e conferiu os sete campos. `AtualizarGuardasDepois()` existe em `:906–927`, atualiza o mesmo snapshot e os quatro campos finais das observações em `:923–926`. Há chamadas em `:619` e `:653`. `tools/automacao/runtime/coletor.py:103–107` preserva os sete campos no schema. Isso é prova estática de presença/costura, NÃO leitura viva nem prova de fechamento temporal correto em jogo.

A mensagem de geometria pertence à mesma cascata de extrator. O caminho real é `Leitura:747` → `Geometria(t)` → viewport em `AUT4ProbePlugin.cs:1963`. O campo aninhado tela não precisa constar como literal no corpo de Leitura. Há ainda defeito latente em `test_aut5.py:404`: a expressão usa a STRING constante `'"tela" in leitura'`, não o operador de pertinência aplicado ao corpo. Com Leitura encontrado, essa string é truthy mesmo sem o literal tela ali. Não foi corrigida neste cartão; a correção exige dataflow e controle negativo, não trocar o teste por passe livre.

## 4. Causa C — harness com duas premissas estruturais obsoletas

`tools/automacao/aut5/test_snapshot_modal.py:17` exige `private static Type Tipo(string nome)`, mas o método real é **internal** em `AUT4ProbePlugin.cs:1879–1886`. Os outros sete métodos exigidos pelo harness foram encontrados. A execução do preflight original reproduziu exatamente `probe sem metodo real: private static Type Tipo(string nome)`, antes de criar projeto/compilar ou chamar avaliador.

Há um segundo bloqueio oculto pelo primeiro: o harness `:97–98` exige `IniciarSnapshotDoModal();` diretamente no corpo de Passo. A estrutura atual é `Passo:464–475`, que despacha `F_LEITURA` para `PassoLeitura:507–544`; a captura está em `:513`, antes de `ColetarObservacoes:514`. Corrigir somente Tipo não basta. A cadeia real precisa ser verificada pelo teste, com controle negativo que remova a ligação/captura apenas em material de teste. Corpos do instrumento não devem ser ajustados para satisfazer o harness antigo.

A visibilidade internal de Leitura e Tipo já aparece no blob anterior `d82894e`, de 07/10/2026; a fase separada PassoLeitura não aparece naquele blob. A comparação delimita a deriva estrutural, mas não identifica autor ou tarefa causadora. Não há atribuição inferida ao rebuild do KIT14G-SEG2-P ou à organização.

## 5. Causa D — integração ambiental e identidade dos bytes

`test_aut5.py:506–545` lê o perfil Default da máquina. `CASOS:788` inclui log-real incondicionalmente. O caso exige DLL do perfil igual à do repo (`:515–518`); não é um teste hermético de checkout/cópia.

Na medição desta investigação, o arquivo `LogOutput.log` do perfil declara RSTV 0.3.3 nas linhas 79–80. Sua DLL existe, com 105984 bytes. Os três hashes RSTV são diferentes:

| Origem da DLL RSTV | Bytes | SHA-256 |
|---|---:|---|
| build já existente da cópia ORG-R1 | 101376 | `ed40e11c326beaccdaaa6b2d02752ac1a4086ab2fada26099752f59999a392df` |
| repo principal | 101376 | `1d0b85e8d0f30d10c4fe7c4e044d30380537e8801a7d39875192459a2e51d5cc` |
| perfil Default | 105984 | `98f19bd6263b054a36c343f0e90effbc41aca8ce8d2355849dec4597a6c4581d` |

`aut5.py:101–116` mede essas identidades. `conduzir:825–827` confronta-as por `log_rstv.py:294–297`. Log com versão atual mas identidade desigual resulta INDETERMINADO. Tanto a cópia quanto o repo principal produziram esse estado: 3 OK offline, 1 INDETERMINADO, 13 NAO_EXERCITADO; exit 2. Não foi simulado perfil com hash igual nem copiada DLL para o perfil.

Distinção necessária: AUT4Probe.dll está AUSENTE na cópia ORG-R1, mas NÃO é a DLL comparada pelo caso log-real. Os testes estáticos do instrumento leem seu C#, não essa DLL. Portanto sua ausência não explica Leitura/Tipo nem a comparação RSTV. Os bytes diferentes RSTV mostram perda de identidade para a prova, NÃO demonstram defeito de comportamento do mod; equivalência funcional e causa das diferenças binárias ficaram NAO_EXERCITADO.

## Continuação

A parte 02 registra o confronto com KIT14G-SEG2-P, hashes físicos/LF, preservação e critérios do follow-up. Nenhum resultado histórico ORG-R1, AUT5-F1/F2 ou SEG2 foi reescrito.
