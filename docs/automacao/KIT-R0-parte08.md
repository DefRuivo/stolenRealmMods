# KIT-R0 — checkpoint 08: dois bloqueadores reproduzidos

Run 623. Há evidência runtime real, mas base NÃO qualificada para o kit.

F1 — fixture falsa-verde na CLI, reproduzido:
Comando `python scratch/kit/KIT-R0-run623/fixture_cli_audit.py`, exit 0 do auditor. Cópias rotuladas do JSON real são controle OFFLINE, nunca runtime. Mesma leitura, dois caminhos:
- topo procedencia=fixture/rotulo_fixture presente: `--detectar` CONFIRMADA/exit 0; consolidação sem `--detectar` FIXTURE/exit 2.
- topo evidencia_runtime=false: `--detectar` CONFIRMADA/exit 0; consolidação FIXTURE/exit 2.
Prova: fixture-cli-results.json e logs top-fixture-*/top-runtime-false-*. O lane CLI coletor.py:1871-1877 perde procedência e rótulo do topo ao chamar o detector com contexto só sessão/hash. Isto viola explicitamente `nenhum JSON fixture qualifica a base`; 15/31 testes verdes não cobrem este bypass.

F2 — diretório de saves monitorado não cobre o save do Stolen Realm:
- A árvore hashada por runtime-isolado.sh e medir-dono.sh é %LOCALAPPDATA%/Abyssus/Saved/SaveGames (5 arquivos, 4 .sav + .vdf).
- Decompilação local executada por ilspycmd (exit 0) do Assembly-CSharp intacto: GlobalSaveDataManager.Filename = Path.Combine(FileSystem.persistentDataPath, "GlobalSaveData.json"); FileSystem.persistentDataPath retorna Application.persistentDataPath (cache sem inicialização).
- Medição read-only atual: %LOCALAPPDATA%/../LocalLow/Burst2Flame Entertainment/Stolen Realm existe, 101 arquivos, contém GlobalSaveData.json. Abyssus não contém esse arquivo. save-path-audit.json registra somente metadados/hashes, não conteúdo de saves.
- Logo antes.txt/depois.txt não provaram preservação dos saves corretos. Além disso os hashes de árvore upstream são de metadados, não bytes. Sem baseline anterior correta, NÃO é possível atestar retroativamente `bit-a-bit intactos`; não há afirmação de dano.

Arquivos de decompilação proprietária permanecem só em scratch/kit/KIT-R0-run623, não serão anexados/publicados nem incorporados à documentação como dump.

F3 — efeito visual não correlacionado: JSON marca Path Chosen! como desenhado, PNG da mesma sessão só mostra LOADING/dica. Sem frame por leitura/captura e sem regra de oclusão, visibilidade renderizada é INDETERMINADA.

F4 — AUT-5 aceita ler cru, mas perde metadados em 24/24; normalizado preserva. A cadeia até avaliador de geometria ainda acusa clipping em objetos inativos/não do RSTV carregado (RSTV-geometria-clipping REPROVADO) — não atribuir ao mod ausente.

F5 — G1 somente leitura versus demonstrador ShowTooltip: a prova bruta é válida, mas chama handler que escreve título/corpo. Não há autorização específica desse efeito no gate, nem restauração do título medida. Exige decisão sobre rodada futura; nenhum consentimento inferido pelo revisor.

Veredito final será REPROVADO para qualificação da base, sem negar o runtime realmente exercitado. Correção offline e nova rodada especificamente autorizada/revisada devem anteceder a liberação segura dos dependentes.
