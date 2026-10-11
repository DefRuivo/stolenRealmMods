# KIT-13 — SDK 1.0.0 e cenários declarativos

Ferramenta offline opt-in para modders. Uso básico exige Python 3 (stdlib) e .NET SDK 6 para compilar os exemplos; NÃO exige Hermes, IA, conta, credencial, rede, assinatura ou assinatura comercial. `nuget.config` não tem fontes de pacotes: projetos sem dependências NuGet. Não instala nada, não abre jogo, não carrega save, não publica.

## Dois pontos de extensão, com fronteiras diferentes

1. Código C# CONFIÁVEL registrado pelo host em `Gumatos.KitSdk.V1.RegistryV1`. `IExtensionV1` tem `OnEvent`, `Read`, `Validate`. O SDK não carrega assemblies, procura plugins, importa scripts nem executa nomes vindos de JSON. Código C# pode fazer tudo que o processo permite: isto NÃO é sandbox contra extensão maliciosa; erro comum de callback é isolado, deadlock/crash/bloqueio não.
2. JSON de cenário é SOMENTE DADO. Schema `KIT13/scenario/1`, API exata `1.0.0`, operações permitidas `menu`, `tela`, `condicao` (só esperas observacionais). Nenhum shell, caminho de DLL, módulo Python, função, clique, salvar, deploy ou autorização no pacote. Campos desconhecidos são erro, não instruções ignoradas. A CLI só observa arquivo offline, nunca um jogo real.

## API C# e ciclo de vida

`Register(id, "1.0.0", extension)` retorna `IDisposable`: guardar lease e chamar Dispose no teardown do host. ID único, `[a-z][a-z0-9.-]{0,63}`, até 64 inscrições. Versão diferente lança `NotSupportedException` com `API_INCOMPATIVEL`; não há fallback silencioso. V1 permanece namespace/assembly versionado; mudar protocolo exige nova versão e compatibilidade deliberada.

`Publish(EventV1(session, frame, kind, data))` distribui a snapshot e revalida identidade antes de cada callback. Desregistrar dentro do callback é permitido. Inscrição feita durante Publish só recebe o evento seguinte. Lease velho não remove reinscrição nova. Publish reentrante é recusado. O lock serializa chamadas: Dispose de outra thread aguarda callback terminar; depois do retorno nenhum callback daquela lease fica em voo. Não segurar lock externo que callback precise ao aguardar Dispose; não bloquear o main thread com extensão lenta.

Evento: sessão e kind não vazios, <=128 chars; frame >=0; data <=4096 chars. Reading: `OBSERVADO`, `AUSENTE`, `NAO_EXERCITADO`, `FALHOU_FECHADO`; valor <=4096. Verdict: `PASSOU`, `FALHOU`, `NAO_EXERCITADO`, `FALHOU_FECHADO`; motivo <=512. Leitura não observada/registro ausente não pode aprovar validação. Exceção/null em leitor/validador vira falha fechada; exceção em listener não impede outros. Diagnósticos últimos64: ID/operação/tipo da exceção, sem mensagem/stack/dados que podem conter segredo.

Não confundir estes verdicts de lógica com aprovação humana/UIUX/publicação. Eventos/sessão/quadro são informados pelo host; pacote não certifica procedência nem inventa hash/frame/personagem. Harness usa sessão `offline-run661`, frame sintético e contador, nenhum personagem.

## Exemplo mod independente + adaptador opcional

`ExampleState` contém o estado contador e evento Changed. `ExampleMod` é plugin BepInEx (GUID com.gumatos.kit13.example, versão1.0.0) que incrementa contador observacional uma vez no Awake e loga. Não altera jogo/gameplay/UI nem aplica patches. Só referencia BepInEx/Unity e biblioteca do próprio estado. NUNCA referencia SDK/Core/adaptador nem os exige no BepInDependency. Fonte de referência em `lib/` é apenas para compilação local, não distribuir.

`Standalone` usa EXATAMENTE CounterState do mod, só com biblioteca do estado, e roda sem SDK fisicamente presente. Isso prova lógica do mod sem kit, NÃO carregamento BepInEx em jogo. A prova de carregamento/funcionamento no jogo permanece NÃO_EXERCITADO até gate humano autorizado.

`OptionalAdapter.CounterAdapter(state, registry, session)` pode ser instanciado explicitamente por host confiável após opt-in e descoberta válida de state. Dispose desinscreve Changed e lease. Leitor `example.counter` / key `count`, comparação exata com esperado externo. `Harness/Program.cs` é exemplo compilável de montagem, uso e descarte; não há patch obrigatório no mod. CounterState/CounterAdapter são para a thread do jogo; a serialização multithread do SDK não torna o estado Unity thread-safe. Remover adaptador/SDK não impede contador do mod funcionar.

`CoreBridge` OPCIONAL reusa `KIT04Core.ICoreEvento` e `Json`, sem editar Core. `CorePluginBinding.Create(core, hostObservationAuthorized)` monta facade dos métodos públicos do Core (EventosImpl é internal). Chamar no main thread depois de inicialização explicitamente confirmada pelo host, nunca assumir CorePlugin.Instancia/Awake pela ordem de DLLs. Func de permissão é só do host; enabled exige permissão E EstaHabilitado. A lease só publica no Core enquanto habilitado. Leitor `events.count` observa contagem do serviço, não histórico incremental nem prova de render. A ponte não limpa a auditoria. CoreHarness usa serviço falso: não comprova Core/BepInEx vivos no jogo.

## Rodar sem Hermes/IA (OFFLINE)

Da raiz do repo, com Python e dotnet disponíveis:

    python tools/automacao/kit13/prove_offline.py --out scratch/kit/KIT-13-minha-rodada

Use diretório NOVO: o runner recusa sobrescrever provas existentes. Ele copia fontes vivos tracked/untracked pertinentes de tools/automacao, sem bin/obj/.git/perfil/credenciais; bibliotecas locais apenas na sandbox. Exerce preflight em TODOS os projetos: propriedade de deploy true deve falhar; false deve passar. Só então compila com `-p:DeployToBepInEx=false`. Estado e provas são lidos de volta, com exits/logs/hashes. Referências Core usam módulos Unity locais do Stolen Realm; se faltarem o runner falha honestamente.

CLI de cenário (sem build):

    python tools/automacao/kit13/packages.py tools/automacao/kit13/examples/menu.json tools/automacao/kit13/examples/state.json --lock scratch/kit/minha-frente.lock --output scratch/kit/menu-resultado.json --allow-offline-observation

Trocar apenas menu.json por skills.json muda o alvo sem recompilar kit. Remover flag de autorização retorna `NAO_EXERCITADO`/exit2 sem ler a fonte. Arquivo ausente/condição não satisfeita dá timeout/FALHOU/exit1. Config inválida dá FALHOU_FECHADO/exit1. Observação offline satisfeita dá OBSERVADO/exit0, sempre `runtime_exercitado=false`/`OFFLINE_ONLY`. Nome de pasta de output deve existir; CLI não cria diretório nem aceita instrução de saída no pacote. Lock é caminho escolhido pelo HOST; no jogo futuro usar a frente única compartilhada KIT11, nunca lock arbitrário por pacote para contornar serialização.

JSON estrito em `scenario-v1.schema.json`; validação Python adicional obrigatória: UTF8 <=65536 bytes, chaves JSON únicas, steps1..32, IDs de passo únicos, textos não brancos e limitados, timeout finito >0 <=60s, soma <=120s, vocabulário condicao do KIT11. Adapter declarado deve coincidir com o adapter do host (CLI só `offline-file.v1`); ele NÃO é nome de módulo para import automático. Permissão do host tem bool estrito; modo ativo sempre false na tradução KIT13. Reuso REAL: executor/FonteDeArquivo/FrenteUnica de KIT11, que reusa controle_acesso/coletor. Nenhuma engine de navegação/avaliação AUT5/6/7/CIC duplicada.

## Provar que os testes pegam defeitos

Após prova baseline no diretório novo:

    python tools/automacao/kit13/prove_mutations.py scratch/kit/KIT-13-minha-rodada --group cs
    python tools/automacao/kit13/prove_mutations.py scratch/kit/KIT-13-minha-rodada --group py
    python tools/automacao/kit13/prove_mutations.py scratch/kit/KIT-13-minha-rodada --group extra

Muta APENAS fonte sandbox, cada caso 0->1->0 e hash original restaurado. Erro de build não conta como teste vermelho. Nenhum AssertionError artificial substitui mutação. Diretórios de evidência por grupo não são sobrescritos. Revisão independente deve tentar seus próprios defeitos, não só repetir relatório.

## Adaptador por jogo — limites obrigatórios

SDK puro não depende de Unity, mas serviço REAL de leitura/eventos/telas depende de engine, versão, backend, API e lifecycle daquele jogo. Este exemplo BepInEx é Mono/netstandard2.1 e compilado com refs locais de Stolen Realm; IL2CPP precisa loader/interops/refs e adaptador próprio, não foi exercitado e não se promete compatibilidade universal Unity/IL2CPP. Nenhum dado de fixture certifica jogo/runtime. Mapeamento de menus/Skills é só exemplo de chave de arquivo, não navegação real.

Autoriza-se apenas implementação/revisão offline neste cartão. Instalar, abrir/fechar jogo, usar perfil/save, navegar ou publicar exigem autorização específica/gates humanos, ausentes aqui. Não distribuir Assembly-CSharp, Unity/BepInEx refs, credenciais ou logs do dono. Não modificar mods existentes para depender do SDK. Sem hot-reload presumido. Não fazer deploy em build de teste; todos estes projetos recusam propriedade diferente de false.

Desfazer esta entrega: remover somente tools/automacao/kit13 e documentos KIT-13 produzidos nesta frente (não outros KIT-13R). Nenhuma instalação precisa ser revertida nesta rodada, pois não houve instalação. Arquivos já modificados pelo dono em outras frentes permanecem intactos.
