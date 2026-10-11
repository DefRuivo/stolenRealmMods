# KIT-R0 — revisão independente da coleta mínima AUT-4

Tarefa t_9264da25. Revisor: nova instância/run 623, perfil default. Autor upstream: run 622/t_b8b9822e. Data: 09/10/2026. Workspace C:/dev/stolen-realm, branch ci-validate-test.

## Veredito

**REPROVADO para qualificação da base do kit.** Há evidência de runtime realmente exercitado; não rotulo a rodada inteira como NAO_EXERCITADO. DLL carregada, leitura bruta e capturas reais têm prova. A base, entretanto, aceita fixture como confirmação no CLI, monitora o diretório de saves errado e não correlaciona o dado de visibilidade ao quadro capturado. Não liberar esses critérios como PASSOU.

Correção aberta: **KIT-R0F t_cfdc09df**, em nova instância, implementação/testes OFFLINE somente. Vinculada como gate adicional de KIT-05 t_e9e569f8 e KIT-11 t_f2129aea. Concluir este cartão encerra o parecer de revisão, NÃO aprova a base, autoriza coleta ou publica DoD.

## Escopo e independência

Li fontes e evidências preservadas, executei os runners e CLI do produto em sandbox, importei os avaliadores existentes e inspecionei duas imagens. Não reexecutei o jogo. Não houve instalação, encerramento, navegação, save, build, publicação, commit, staging, alteração de mod ou mudança de política/modelo/cron. Somente arquivos novos KIT-R0 e evidências de revisão em scratch/kit/KIT-R0-run623.

A sandbox preservou 1025 arquivos tracked/untracked; .git/remotos/credenciais não foram copiados. DLL pré-existente e lib/Assembly-CSharp.dll foram copiados explicitamente depois, apenas como referência local para os testes; não recompilados, instalados ou distribuídos. USERPROFILE/APPDATA/LOCALAPPDATA/TEMP dos subprocessos dos runners foram redirecionados. Snapshot do workspace: nenhum arquivo preexistente mudou ou desapareceu no momento da comparação.

## Veredito por critério

| Critério | Veredito | Prova e limite |
|---|---|---|
| Autorização/frente única | ACHADO / INDETERMINADO para intervenção UI | KIT-G1 e revisão autorizam leitura até boot/menu. ShowTooltip escreve título/corpo; não há permissão específica dessa escrita no gate. Jogo agora ausente, lock disponível. |
| DLL efetivamente carregada | OK | DLL 50176 bytes, 0.1.0, hash calculado em runtime igual ao disco; log bruto r4 confirma uma carga e dois ganchos. |
| Sessão/evidência nova | OK para sessão; ACHADO para quadro | Três sessões distintas e JSON posteriores ao lançamento, hashes iguais aos manifests. Frame de aplicação é 0 do boot; não existe frame da observação/captura vinculado. |
| Objeto conhecido/leitura verificável | OK somente para leitura bruta | Marcador único do driver relido de Tooltip.Title em r2/r3/r4. Texto interpretado do marcador vazio; visibilidade/renderização NÃO comprovadas. |
| Captura válida | OK para PNG; INDETERMINADO para associação visual | Quatro PNG preservados, CRC válido, 1920x1080, SHA256/tamanho iguais ao manifest. r3/02-final mostra LOADING/Difficulty Scaling, não Path Chosen! listado no JSON. |
| Produtor -> normalizador -> avaliador | FALHOU na qualificação/procedência | Coletor normaliza metadados em 24/24; AUT-5 cru perde contexto em 24/24. CLI detector promove artefato rotulado fixture a CONFIRMADA. AUT-5/6/7 não comprovam runtime de mods que não carregaram. |
| Controle negativo | OK para capacidade offline de reprovar; NAO_EXERCITADO para boot sem probe | r2 real dá INCOMPLETO/exit 1; expectativa impossível sobre r3 real dá NO/exit 1; expectativa independente de tipo dá CONFIRMADA/exit 0. Não houve rodada comparativa sem probe. |
| Fora do perfil/save de produção e restauração | OK limitado para resíduos de perfil; FALHOU para prova de saves corretos | DLL carregada pela cópia; área isolada removida; rollback registrado limpo e zero AUT4 no perfil. Baseline compara Abyssus, não o GlobalSaveData do Stolen Realm; hashes de árvore são metadados. Preservação byte a byte dos saves corretos é INDETERMINADA. |
| DoD/aceite humano/publicação | NAO_EXERCITADO nesta revisão | Parecer técnico não concede aprovação humana/publicação. |

## Achados e reprodução

### F1 — crítico: fixture vira CONFIRMADA pela CLI

Código: tools/automacao/runtime/coletor.py:1871-1877. O mapeamento lê procedência/rótulo/evidencia_runtime do topo, mas o lane `--detectar` fornece ao detector apenas observações e contexto sessão/hash, mantendo procedência runtime por padrão.

Comando real: `python scratch/kit/KIT-R0-run623/fixture_cli_audit.py` (exit 0 do auditor). Duas cópias do dado real foram explicitamente rotuladas como controles offline, sem modificar o original:

| Controle | CLI --detectar | CLI consolidação da mesma entrada |
|---|---|---|
| procedencia=fixture + rotulo_fixture | CONFIRMADA, exit 0 | FIXTURE, exit 2 |
| evidencia_runtime=false no topo | CONFIRMADA, exit 0 | FIXTURE, exit 2 |

Prova: fixture-cli-results.json e logs top-fixture-*/top-runtime-false-* na pasta da revisão. Esse falso verde viola diretamente o aceite: nenhum JSON fixture qualifica a base. Não é resolvido pelos 15 testes/31 iscas existentes, que ficaram verdes.

### F2 — crítico: baseline dos saves errada e hash não é de bytes

scratch/kit/runtime-isolado.sh:47 aponta para %LOCALAPPDATA%/Abyssus/Saved/SaveGames; linhas 101-105 hasheiam somente caminho, tamanho e mtime. A reprodução desse algoritmo devolveu exatamente os hashes de antes.txt. Eles não são SHA256 do conteúdo da árvore.

Decompilação local por ilspycmd, exit 0, de Assembly-CSharp intacto: GlobalSaveDataManager.Filename usa FileSystem.persistentDataPath + GlobalSaveData.json; FileSystem retorna Application.persistentDataPath. Medição read-only encontrou esse arquivo em AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm, ausente de Abyssus. O diretório Stolen Realm tem 101 arquivos; o diretório monitorado tem 5 (4 .sav + .vdf). Prova: save-path-audit.json e decompilações locais dirigidas em scratch (não distribuir esses dumps).

Não há baseline de conteúdo anterior da rodada para os saves corretos. O snapshot atual do revisor não pode retroagir. Portanto a afirmação upstream `perfil/saves bit-a-bit intactos` é forte demais. Isto NÃO prova dano; prova insuficiência e alvo errado da medição.

### F3 — correlação quadro/visibilidade não demonstrada

AUT4ProbePlugin.cs:320-382 mede objetos e solicita PNG em etapas; `quadros_ate_a_ui` conta ticks internos, enquanto `aplicacao.roteiro_frame=0` é metadado do arranque. Não há frame/evento associando leitura e pixels.

LeituraAgregados.cs:155-162 considera TMP ativo e GetParsedText não vazio como visível. Em r3, textos_visiveis registra somente Path Chosen!; r3/02-final.png mostra LOADING/Difficulty Scaling. Em r4, o PNG mostra LOADING/Potions. Nenhum mostra marcador AUT4. Não posso decidir só desses dados se houve oclusão, CanvasGroup ou diferença temporal. O rótulo `desenhado` não está demonstrado. 24 observações incluem 23 objetos inativos e apenas 1 ativo.

### F4 — costura e atribuição ao alvo

AUT-5 aut5.py:622-641 não injeta metadados do topo na entrada crua: execução própria confirmou 0/24 com sessão/hash/procedência. Pelo consolidado do coletor são 24/24. O caminho normalizado é utilizável, mas não equivale à promessa de suporte cru.

RSTV-geometria-clipping dá REPROVADO (altura 0 e y+altura fora da tela) sobre objetos do boot, sem o RSTV sequer carregado. Não atribuir esse resultado a defeito do mod. Exigir seleção de cenário/objeto/atividade e identidade de produto reais. AUT-6 e AUT-7 ficaram sem prova runtime; não inserir hashes do probe como se fossem identidade dos mods.

### F5 — demonstrador ativo sob escopo somente leitura

AUT4ProbePlugin.cs:818-845 e 850-867 chama ShowTooltip e relê o título. Trata-se de escrita transitória em UI, não getter passivo. A função não restaura o título; o comentário assume repintura posterior, sem medição. A rodada acabou ao fechar o processo, e nenhuma persistência indevida foi demonstrada, mas isso não amplia a autorização G1. Nova coleta deve ser passiva ou ter permissão explícita para demonstrador/restauração.

## Execuções próprias e exits

Pasta das provas: C:/dev/stolen-realm/scratch/kit/KIT-R0-run623.

- `review_evidence.py`: exit 0. suite-with-dll.log: 15/15 PASSOU, runner exit 0. contra-with-dll.log: 31/31 iscas rejeitadas por asserção esperada, runner exit 0; zero exceção inesperada. Os primeiros logs suite.log/contra-prova.log foram vermelhos por DLL não copiada, preservados como falha de pré-requisito, não contados como aprovação.
- Replay CLI dos dados originais: r2 INCOMPLETO/exit 1; r3/r4 CONFIRMADA/exit 0, sem expectativa declarada. Componente esperado TextMeshProUGUI: CONFIRMADA/exit 0; componente impossível: NO/exit 1. Esses testes não são nova coleta runtime.
- `integration_audit.py`: exit 0. AUT-5/RSTV cru e normal: 6 NAO_EXERCITADO + 1 REPROVADO; AUT-6: 23 NAO_EXERCITADO + 1 INDETERMINADO, excluído tipo limite para não escanear assets; AUT-7: 10 NAO_EXERCITADO + 1 INDETERMINADO. Zero provas runtime de produto.
- `fixture_cli_audit.py`: exit 0 do auditor; os exits/status dos quatro CLIs estão na tabela F1.
- `tasklist`: exit 0, nenhum Stolen. `front-unica.sh check`: exit 0, lock disponível. Área isolada ausente; resíduos AUT4 no perfil 0.
- Snapshot de 1025 arquivos: changed_or_removed=[], branch preservada. Apenas arquivos KIT-R0 novos fora de scratch até a medição.

Não executei builds, suíte global de mods, check_versoes/valida_pacotes ou audita_docs/check_segredos globais nesta revisão dirigida; não qualifico esses gates como verdes. Gates dependentes de git em sandbox sem .git exigiriam isolamento adicional para evitar descoberta do .git ancestral. Nenhum preflight de deploy foi contornado; build NÃO EXERCITADO, em vez de build presumido.

## Identidades conferidas

| Artefato | SHA256 |
|---|---|
| DLL do probe no disco e no runtime | 407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7 |
| AUT4ProbePlugin.cs | 48afd3c41cf3ba97c93e5fc2d6b02ca58298939bf4b2a51f0ccd159ec96e3e94 |
| coletor.py | adb48dca024120db91b65e28b8842b7f303ca1725359cdaf4deab5530ae1dd46 |
| controle_negativo.py | 053c0026f97c8541294c81e9d0011df4f3d970756f6ab8bc1d96a98fa9296659 |
| roda_testes_runtime.py | 7906c1692bf349aff006039f73bbc8c59ef4e2a7a588210c348227be4dfb157e |
| lib/Assembly-CSharp.dll (intacta) | 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a |
| round-audit.json | e5fb5b5fd2b7a46f2a9d93990ffec243f7d1df8c21b647d118880196e084525b |
| integration-results.json | 8e3d5199bb546af31f4932d081b535ec825e1a215dca7d4b9260898f48cee83e |
| fixture-cli-results.json | 1f95743e7c1b173381ab582480c4fcac6c63fa8fd5babe187324d38b21981b2f |
| save-path-audit.json | 371d41acf575872b11745a22abb16fe4aad100eff1ef215f14885d3eb1f7f21d |
| replay-results.json | 4e80d6efb5d335615fda47c4cd5cdb1bef4c48bb489905bf18183197d3314f35 |

As partes KIT-R0-parte01..08 registram checkpoints, inclusive hipóteses posteriormente resolvidas; este parecer é o veredito final. Hash deste arquivo será calculado no manifest de fechamento, nunca autorreferenciado.

## Próximo passo

KIT-R0F corrige offline os gates/procedência/caminhos/correlação/seleção de alvo, planta defeitos e pede revisão nativa por outra instância. Nova rodada, se necessária, depende de autorização específica atual do dono e isolamento verificado dos saves corretos. Preservar evidência antiga como histórico real incompleto; não fabricar baseline, não aprovar retroativamente escrita de UI e não chamar isso de publicação/aceite humano.
