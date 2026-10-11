# KIT-13 — checkpoint 03 (run661)

Contratos confirmados: executor.executar(plano, fonte, frente=...), FonteDeArquivo.ler(tipo, alvo), FrenteUnica; controle_acesso é importado pelo executor e será preservado. KIT-11 aceita autorização no plano, portanto KIT-13 traduz pacote sem autorização e acrescenta exclusivamente decisão do host (observação), ativa sempre false. Só execução offline de arquivo nesta entrega.

Directory.Build.props lido: DeployToBepInEx padrão false. Novos projetos terão alvo de bloqueio explícito caso DeployToBepInEx não seja false; build somente em sandbox. Preflight deverá exercer esse bloqueio antes do build permitido, com alvo leve sem compilação.

Detalhe API v1: DTOs de evento/leitura/veredito, IExtensionV1, registro IDisposable com ID+API exatos, limite 64 extensões, lock reentrante em callbacks (Dispose de outra thread espera callback terminar); exceções retornam FALHOU_FECHADO e diagnóstico só com tipo, sem vazar mensagem/dados. Leitura ausente não vira verde. Reentrada de Publish será recusada para evitar recursão de callbacks. Não se promete isolamento de deadlock/processo/crash de extensão maliciosa.

Exemplo: plugin BepInEx independente com estado contador observacional (nenhum patch/gameplay), fonte do estado usada também em harness .NET6 offline; adaptador opcional separado aponta para estado, publica eventos e expõe leitura/validação. Mod não referencia SDK/Core/Adapter. Harness prova lógica fora do jogo; carregamento do plugin em jogo fica NÃO_EXERCITADO.

Reuso Core: ponte opcional consumirá ICoreEvento/EstaHabilitado via host explícito, sem mudar Core, polling sem instalar/registrar hooks; contrato e limites por jogo documentados.

Próximo bloco: arquivos novos e runner de sandbox preservando fonte tracked/untracked pertinente, sem .git, credenciais/perfil ou DLL de jogo no pacote público. Nenhum build executado ainda.
