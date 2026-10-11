# KIT-13R — baseline reproduzido pelo revisor run664

Comando: python tools/automacao/kit13/prove_offline.py --out scratch/kit/KIT-13R-run664
Exit0 real. Runner lido antes de executar: copia fontes tracked/untracked de tools/automacao + Directory.Build.props e referências locais selecionadas, sem .git/perfil/credenciais. Ambiente filho redirecionado à sandbox. Não modifica fonte vivo; build só após preflight.

Saídas reais: preflight-denied-0..7 exit1; preflight-safe-0..7 exit0; build-mod/harness/standalone/core exit0; csharp-tests/standalone-no-kit/core-bridge/python-tests exit0; cli-denied2, menu0, skills0, missing1. Linha final KIT13 BASELINE PASSOU; game NAO_EXERCITADO. Logs e comandos completos em scratch/kit/KIT-13R-run664/logs e commands.json; readback independente ainda pendente.

C1/C5/C8: PASSOU no baseline offline do autor reproduzido em cópia nova pelo revisor; não basta para parecer final. Standalone prova CounterState, não lifecycle BepInEx real. CoreHarness fake, não runtime.
C2/C4: leitura packages.py mostra validação de campos exatos, operações menu/tela/condicao, import somente executor.py fixo, bool estrito de autorização do host e modo sempre observacao/ativa=false. Inputs hostis próprios ainda pendentes.
C3: RegistryV1 lock serializa callbacks e usa snapshot+identidade de entry; exceções ordinary são isoladas e diagnostics bounded. Código confiável pode bloquear/crash; README delimita isso corretamente. Novos casos de lifecycle próprios pendentes.
C6: README declara Mono/Stolen Realm, nenhuma promessa universal/IL2CPP, uso Python stdlib e .NET sem Hermes/IA; execução real acima não usou serviços IA. Refs locais só para compilação. PASSOU documental, dependências binárias ainda pendentes.
C7: preservação e hashes precisam conferência independente (não confiar somente verificação do runner).

Filha t_10584ca5 KIT-15 inspecionada: distribuição depende desta revisão e do gate KIT-G3. Se aparecer ACHADO, criar conserto e ligá-lo a KIT-15 antes de concluir o parecer reprovado, preservando dependências e histórico.

Próximo bloco: leitura adaptadores/manifestos/testes, hashes/readback e suíte independente. Nenhum deploy/instalação/jogo/publicação exercitado.
