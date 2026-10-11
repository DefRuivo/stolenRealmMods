# KIT-14 — run699: frente disponível; isolamento de save ainda não provado

## Saídas reais

Terminal em C:/dev/stolen-realm, exit 0 (10/10/2026 13:07:18 -03):

- front-unica.sh check: OK, lock disponível.
- PowerShell somente leitura: STOLEN_PROCESS_COUNT=0.
- Python pathlib: RUNTIME_ISO_EXISTS=False.
- Inventário dirigido encontrou tools/check_deploy_optin.py e testes puros t_deploy_optin_guarda.py/t_deploy_optin_repo.py.

Não foi iniciado, encerrado ou navegado nenhum jogo.

## Descoberta adicional

Directory.Build.props lido: DeployToBepInEx default=false. check_deploy_optin.py lido: guarda XML dos targets e destinos ao perfil, CLI --raiz/--json, exit0/1. Será exercitado sobre sandbox antes de build; a existência do arquivo não conta como teste verde.

KIT-15 README lido: pacote 0.1.0 local, ferramentas stdlib; instruções para montar/verificar/install/update/remove/rollback e uso extraído sem Hermes/IA/credenciais. Compilar componentes em jogo não foi provado pela entrega anterior.

isolacao.sh lido no bloco dirigido: save-isolate apenas copia arquivos; prove-isolation cria test_marker.txt e confronta containment. Isso não prova que o processo do jogo consome um save descartável. Não executar save-restore (escreveria no local pessoal).

G1-evidencia-run.sh lido: conserva evidência do runtime-isolado; copia Player.log de LocalLow pessoal. Não serve como prova de isolamento do persistentDataPath da instância de teste nem deve ser lançado com navegação presumindo esse isolamento.

## Próxima prova dirigida

Verificar a definição compilada de FileSystem/persistentDataPath e o lançamento real do coletor, sem dumps completos, para descobrir se há um caminho já entregue de redirecionamento de saves. Em paralelo lógico, preparar sandbox sem .git/credenciais com fontes tracked/untracked e exercitar as operações offline autorizadas. Nenhuma mudança de produto ou mecanismo de save será feita para tornar a auditoria verde.

Decisão B permanece aplicada: não há bloqueio por limiar. Métricas em jogo ainda NAO_EXERCITADO por falta de rodada efetiva.
