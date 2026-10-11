# KIT-14 — run699: fronteira técnica do isolamento e preparação offline

## Provas dirigidas

Terminal exit 0: ilspycmd -t FileSystem lib/Assembly-CSharp.dll. O tipo compilado declara:

`public static string persistentDataPath => _cachedPersistentDataPath ?? Application.persistentDataPath;`

O construtor estático mostrado é vazio; não há redirecionamento por argumento/ambiente nesse tipo. Isso identifica a dependência de caminho persistente, não prova acesso em jogo. A DLL de referência não foi alterada.

coletor.py:1593–1879 lido: executar_rodada cria configuração/probe sob perfil_dir, passa os argumentos de doorstop ao Steam e chama subprocess.Popen(cmd) sem redirecionamento de caminho persistente do jogo. Rollback vigia plugins/config/log, não isola save consumido pela aplicação.

AUT4Probe.csproj e KIT04Adapter.SR.csproj lidos. Projetos sem target de deploy; Adapter referencia Core. Referências externas serão copiadas somente para sandbox local não redistribuída, nunca incluídas em pacote de evidências.

Busca na raiz encontrou obstáculo de infraestrutura: arquivo preexistente `nul` faz rg falhar (os error 1). Nenhuma mudança nesse arquivo. Abordagem muda para busca UTF-8 dirigida por Python excluindo `nul`, em vez de repetir rg.

## Decisão operacional

Não lançar a instalação pessoal via Steam nem navegar até save pessoal com scripts que isolam só BepInEx. Investigar redirecionamento já entregue antes de qualquer boot. Ausência de limiares não é o impedimento atual; decisão B segue aplicada.

Preparar sandbox dos caminhos vivos tracked/untracked, sem .git/credenciais, e executar preflight XML real antes de builds. Empacotamento/instalação local/rollback offline e controle negativo do pacote podem ser qualificados sem lançar o jogo, reusando ferramentas KIT-15. Esses resultados não serão promovidos a runtime.
