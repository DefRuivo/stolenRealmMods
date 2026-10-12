# KIT-14G-SEG2 — parte03: três boots executados; crash não reproduzido, aceite ainda aberto

Cartão `t_139f714f`, `default/run895`. Medição em 11/10/2026, 22:01–22:11 BRT (UTC−03). A autorização foi consumida exatamente como registrada: **3 boots**, par congelado do SEG2-P, probe só, dados isolados vazios, rota `Play;Roguelike;Accept`, janela de 150 s. **Nenhum quarto boot, clique de sistema, deploy no perfil real, rebuild, commit ou publicação.**

## 1. Veredito

**INCOMPLETO — não declarar corrigido nem declarar impossibilidade do handler.**

Os três boots invocaram os três handlers, sobreviveram à janela e foram encerrados normalmente pela bancada. O controle `F-marcadores` já não reproduziu a assinatura histórica `ntdll.dll/c0000005/0x4a612`. Portanto não há contraste causal que permita atribuir a ausência do crash ao gate ou ao silêncio. Além disso, a rota terminou na seleção de party, não no HUD de uma run.

A rodada fecha a lacuna operacional dos três boots pendentes, mas **não fecha o aceite original**: não foi localizada uma instrução nativa que gerasse o crash e não foi validada uma correção em jogo. O teste físico continua pendente de coordenação do operador, não de um reboot nesta rodada: o handle estava liberado e o rename passou nos três boots.

## 2. Identidade efetivamente exercitada

- Fonte `AUT4ProbePlugin.cs`: `beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193`.
- DLL: `7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee`.
- Pré-flight: DLL e cinco entradas repo/sandbox conferidos antes da rodada, exit 0.
- Cada `aut4probe.json` mede, no runtime, a mesma DLL acima. O jogo reportou versão **1.3.1**, Unity **2022.3.62f2**.
- Assembly do jogo atual e `lib/Assembly-CSharp.dll` são byte a byte iguais, SHA256 `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`; ILSpy foi usado apenas para leitura dos tipos relevantes.

Não confundir essa identidade com a dos crashes do run714: a frente INT-R1-C2-I1 retirou o patch próprio de `OptionsManager.Localize`. Nos três boots novos, o campo **runtime** `owners_harmony.por_metodo.OptionsManager.Localize.owners` é `[]`; `GUIManager.Update` tem o owner do AUT4Probe. A fonte anterior preservada em `INT-R1-C2-I1-evidencias/AUT4ProbePlugin-pre-edicoes.cs.txt:249-251` aplicava os dois ganchos.

**Hipótese, não conclusão causal:** retirar o tick reentrante disparado por Localize pode explicar a diferença. Não houve A/B dessa retirada, e os boots históricos e novos não são binariamente equivalentes. Nem o desaparecimento do crash nem seu mecanismo podem ser atribuídos apenas a essa mudança.

## 3. Resultados por boot

A duração é a medição externa monotônica do driver, desde o launch até o fim da janela, antes do fechamento deliberado.

| boot | cfg gate/estabilidade/silêncio | PID | lançamento BRT | observação | frames Play/Roguelike/Accept | Application Error |
|---|---|---:|---|---:|---|---:|
| F-marcadores | false / 0 / false | 25776 | 22:01:26.915 | 152,183 s | 251 / 251 / 251 | 0 |
| F-silencio | false / 0 / true | 7800 | 22:05:10.748 | 152,333 s | 259 / 259 / 259 | 0 |
| F-gate | true / 10 / false | 18340 | 22:08:24.757 | 152,068 s | 254 / 257 / 260 | 0 |

Em todos:

- `empty_test_data_verified=true`, `personal_save_selected=false`, `passive_plugins_installed=false`; runtime lista **um** plugin, o probe.
- Os três eventos `clique_eventos` trazem `Play`, `Roguelike`, `Accept`, caminho na hierarquia e frame. O Accept é `GUI Manager/Character Creation(Clone)/UI/Roguelike/Accept Button`.
- `steam-launch`, verificação de dados, restauração, rollback BepInEx e liberação da frente terminaram exit 0.
- O processo não desapareceu na janela; `game_closed=true` após `CloseMainWindow` dirigido apenas ao PID lançado.
- `Player-isolado.log` contém `ShutdownInProgress`, saída da thread de input e `Memory Statistics:`. Não é término abrupto no meio de `Loaded Objects now` como nos logs históricos.

### F-marcadores

Retorno dos três handlers registrado. JSON final `CONCLUIDO/concluido`, mas a navegação final **esgotou 3600 tentativas sem Skills**. O JSON diz `CurrentGuiState=ChoosingCharacter`. Os prints `01-ui.png` e `02-final.png` são idênticos e foram inspecionados: **Select Party**, `0/30`, seis slots vazios, nenhum HUD de run. `CONCLUIDO` é conclusão da coleta, não sucesso de início de run.

Último marco: tentativa 3600, frame 1366, procura `Skills`, sem alvo, cena `GameSceneNew`. Nenhum marco localiza crash, porque não houve crash.

### F-silencio

O marco `silencio_ativado apos_ultimo_estagio=3/3` comprova ativação do discriminador. Os heartbeats do próprio probe continuam até `ticks_em_silencio=14070`, frame 4949. JSON fica `INICIADO/navegando`; não há prints pós-clique nem estado final de HUD. Isso é esperado no ramo diagnóstico que retorna antes da finalização; não inventar `clique_config` final, que não foi gravado nesse boot.

O silêncio retira varredura/coleta/prints, **não** todo contato com a engine: o código segue lendo `Time` nos marcos e escrevendo JSON. Sobrevivência sem o controle morrer não discrimina causa.

### F-gate

Runtime confirma gate `true` e estabilidade configurada `10`. JSON final também termina com procura de Skills esgotada e `ChoosingCharacter`. Print inspecionado: **Select Party**, um personagem disponível, party vazia, **Game Menu sobreposto**. Não houve input de sistema pela bancada; a origem do menu sobreposto não foi isolada e não é atribuída ao operador/controlador.

Nenhum HUD de run foi observado. Não apresentar esse boot como correção comprovada.

## 4. Dois achados concretos que mudam a próxima rodada

### 4.1 O parâmetro de estabilidade não conta frames Unity

`AUT4ProbePlugin.cs:1305-1312` incrementa `_estavelQuadros` a cada chamada de `EstavelEnough`, sem conferir mudança de `Time.frameCount`. `Tick` tem múltiplas origens e não deduplica por frame (`:403-436`). A prova runtime é mais forte que o comentário do código:

| alvo F-gate | tentativas de espera | frames distintos de espera | frame do clique |
|---|---:|---|---:|
| Play | 9 | 251, 252, 253 | 254 |
| Roguelike | 9 | 254, 255, 256, 257 | 257 |
| Accept | 9 | 257, 258, 259, 260 | 260 |

Portanto `CliqueFisicoEstavel=10` significou **dez chamadas**, não dez frames. Os três cliques do controle até aconteceram no mesmo frame 251. Essa inadequação do instrumento está comprovada, mas **não** foi ligada causalmente ao `c0000005`.

Não foi alterado o instrumento congelado. A correção futura precisa definir um único avanço por frame, guardar identidade do botão, reiniciar estabilidade quando o alvo perder o gate e impedir reentrada durante `invocar`. Isso é desenho proposto, não implementação nem resultado medido nesta rodada.

Outro limite: `RegistrarClique` é chamado **depois** de `achado.invocar()` (`:1367-1388`). O próximo instrumento deve marcar separadamente entrada/retorno do handler; a falta de um marco de retorno não é uma stack nativa.

### 4.2 Accept da criação não equivale a iniciar uma run

A leitura do assembly **atual, com identidade comprovada**, corrige uma premissa da receita histórica:

- `PresetManager.AcceptCharacter` chama `GameLogic.FinalizeCharacterCreation`, depois reseta a criação (`PresetManager.cs:1035-1044`, extração offline desta rodada).
- `GameLogic.FinalizeCharacterCreation` cria o personagem, define `GUIState.ChoosingCharacter`, salva **no diretório isolado** e atualiza a lista de personagens (`GameLogic.cs:2135-2222`; mudança de GUIState em 2208).
- `CharacterChoiceManager.Update` condiciona o botão da party a existir personagem selecionado (`:146-156`). `AcceptButtonPressed` chama `AcceptCharacterChoices`; esta abre escolha de dificuldade no roguelike host, ou segue para `GameLogic.AcceptCharacterChoices`, e recusa party vazia (`:403-483`).

Isso coincide com os prints novos: o roteiro de três handlers não cobre seleção do personagem/party, confirmação de dificuldade e chegada ao HUD. Não foi reconstruída uma rota adicional por adivinhação nem clicada fora do escopo. A existência de `Character0.json` foi observada somente na área gerada pelo jogo isolado; nenhum conteúdo de save do dono foi usado como personagem.

O crash antigo pode ter acontecido durante a criação/transição, não necessariamente no início efetivo de uma run. Não reescrever os logs antigos; tratar a antiga expressão “inicia a run” como premissa que esta rodada não confirmou.

## 5. Bancada e coleta: mudanças explícitas, sem alterar o produto

Driver novo: `scratch/kit/KIT-14G-SEG2-run895/roda895.py`, executado originalmente no workspace do cartão. Reusa o driver run885 e seus helpers, sem editar essas dependências. `verification.json` registra SHA256 do wrapper realmente executado, do driver subjacente e dos três drivers expandidos.

Diferenças restritas à bancada:

1. Diretório e sessões **novos**, sem sobrescrever o fracasso de preparo run885.
2. As três chaves do cfg são anexadas e o cfg **efetivo** é copiado antes de apagar o perfil isolado; o hash bate com o driver.
3. `Player.log` é copiado da área isolada antes da restauração/limpeza; marcos e JSON vivem fora da cópia dos dados.
4. Timestamps absolutos de lançamento/fechamento registrados para correlação.
5. Export Event Log usa nomes do XML (`ProcessId`, `ModuleName`, `ExceptionCode`, `FaultingOffset`), não os índices antigos. XML bruto preservado.
6. Snapshot imediato do **perfil inteiro** antes/depois, além do snapshot do save que run885 já fazia.
7. Se o jogo continuar vivo, não restaurar/remover perfil nem liberar lock: o wrapper adiciona parada segura ao bloco final. Esse ramo não foi exercitado porque os três fechamentos funcionaram.

O snapshot imediato por boot substitui expressamente o baseline histórico do KIT-16, como já declarado no run885. Não houve restauração de saves de outro dia.

**Controle positivo da coleta de eventos:** a mesma extração XML, ampliando apenas a janela para três dias, encontrou **sete** Application Error reais anteriores do Stolen Realm. Os eventos contêm `ProcessId` hexadecimal, versão do módulo em campo separado e a assinatura histórica. O agregador filtra janela de cada boot e PID; resulta zero em cada janela. Isso comprova que a consulta não é uma coleta vazia incapaz de achar a assinatura; não é um crash novo provocado como contra-prova.

## 6. Preservação do ambiente

Medição por boot, não comparação com a descrição antiga de 106 arquivos:

| alvo | antes/depois em cada boot | novos/removidos/alterados |
|---|---:|---|
| save real | **111 / 111** | 0 / 0 / 0 |
| perfil real BepInEx completo | **53 / 53** | 0 / 0 / 0 |

O dono havia alterado os dados desde as tentativas anteriores; o conteúdo foi preservado conforme o snapshot contemporâneo. `real_linktype_fim` vazio, backup `.kit16-real` ausente. Export PlayerPrefs antes/depois idêntico em cada boot. Cloud do app explicitamente off nos marcos; o cache local do Steam mudou por execução e **não** é apresentado como intocado nem como auditoria do servidor remoto.

Após preservar logs, cfg, JSON, manifests e hashes necessários, as três áreas `dados-iso` foram removidas pelo subcomando `limpar` do KIT-16, somente com jogo fechado, caminho real normal e sem backup pendente. A prova final dessa limpeza e do estado externo está em `cleanup-state.json`. Não se conserva a cópia privada dos saves do dono como deliverable.

## 7. Verificação e evidências

`verifica895.py` foi realmente executado: **60 checks passaram**, `acceptance_met=false`. Os checks auditam identidade, cfg, três cliques, isolamento, janela externa, fechamento, shutdown do Unity, rollback, Cloud, save, perfil, registro e consulta Event Log. **Não são 60 testes de correção do crash.** Não rerodei nem reivindico novos resultados para as suítes/harnesses históricos; o produto não foi editado nem rebuildado.

Raiz da evidência: `C:/dev/stolen-realm/scratch/kit/KIT-14G-SEG2-run895/`.

- `verification.json`: resultados e limites, checks, hashes e classificação.
- `roda895.py`, `verifica895.py`: wrapper executado e auditoria por arquivo.
- `eventlog-positive-control.json`: controle positivo real, XML e nomes corretos.
- Por boot: `result.json`, `commands.json`, `LogOutput-isolado.txt`, `Player-isolado.log`, `config-efetiva.cfg`, `probe/aut4probe.json`, `probe/marcos-clique.log`, prints quando existentes.
- Por label na raiz: `*-expanded.py`, `*-identity.json`, `*-eventlog.json`, `*-pos-estado.json`, comparação/manifests do save e perfil.
- `cleanup-state.json`: readback final e remoção das cópias privadas.
- `evidencias-run895.zip`: bundle selecionado, sem DLLs do jogo, sem fontes decompilados integrais, sem saves pessoais nem exports de registro brutos.

## 8. O que falta e por que o cartão não está DONE

**NÃO EXERCITADO:** ponto nativo do `c0000005`, chegada ao HUD, efeito causal do gate/silêncio, correção de produto validada em jogo, impossibilidade de iniciar uma run por handler, input físico supervisionado.

A autorização registrada cobre exatamente três boots com este par congelado; executá-los não autoriza um quarto boot com DLL anterior, um instrumento novo ou uma rota ampliada. É necessária decisão do operador/dono para uma próxima etapa diagnóstica, por exemplo:

1. Autorizar novo A/B isolado, com identidade antiga preservada versus atual e marcos de entrada/retorno, para testar a hipótese de reentrada pelo Localize; ou
2. Coordenar o teste físico isolado, com probe sem navegação concorrente, primeiro criação e depois seleção de party/dificuldade, registrando onde aparece o sintoma.

Essas são alternativas para decidir, não promessa de runtime já aprovado. A etapa física não deve depender de o KIT-14 inteiro fechar; o grafo SEG2 → SEG1-RT → físico cria espera operacional circular se o físico for exigido para fechar SEG2. O operador precisa coordená-la diretamente se escolher esse discriminador.

Não liberar `t_a41dd22d` com uma conclusão falsa. Cartão bloqueado por decisão/escopo de nova prova, **não por handle, cota, orçamento de iterações ou incapacidade de rodar os três boots**.
