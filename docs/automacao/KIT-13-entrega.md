# KIT-13 — entrega de implementação OFFLINE (run661)

Cartão:t_adc1fbfa. Implementador:perfil default/run661, instância separada das revisões dos pais. Revisão independente PRECRIADA:t_596ee4f5 (KIT-13R), ainda pendente. Concluir esta FASE de implementação libera a filha; não é autoaprovação, aceite humano, runtime nem publicação/DoD de mod.

## Entregável

SDK C#1.0.0 `Gumatos.KitSdk.V1` em tools/automacao/kit13/SDK,sem dependência Unity/BepInEx/jogo. API de eventos,leitores,validadores; registro IDisposable; erros isolados e versões incompatíveis diagnosticadas.

Pacotes `KIT13/scenario/1` em JSON, schema fechado e validador sem dependência externa. Operações SOMENTE menu/tela/condicao observacionais. Sem código executável,imports dinâmicos por pacote,paths de DLL,ações ativas ou autorização embutida. Tradução reusa KIT11.Executor/FonteDeArquivo/FrenteUnica (que reusa controle_acesso/coletor) em vez de criar outra engine. Permissão externa do host,ativa sempre false. CLI é offline e não expõe caminho de jogo.

Exemplo de plugin ExampleMod BepInEx independe de kit; biblioteca ExampleState própria contém CounterState. Adaptador OptionalAdapter separado e CoreBridge opcional,sem mudar mods/Core. `CorePluginBinding` usa facade dos métodos públicos realmente existentes,sem cast inválido ou suposição de Awake/ordem de carga. Uso explícito compilável em Harness/Standalone/CoreHarness.

Fonte de uso/contrato/limites/comandos/desfazer:tools/automacao/kit13/README.md. Implementação:27 arquivos novos no diretório kit13 (manifesto exato em source-hashes.json). Nenhum arquivo de implementação pré-existente foi editado.

## Veredito por critério (prova do implementador; não parecer independente)

| Critério | Resultado offline | Prova e limite |
|---|---|---|
| API versionada eventos/leitores/validadores | PASSOU | SDK compilado; Harness17 casos exit0; ApiVersion1.0.0/exato; versão2.0.0 recusada sem inscrição; mutação do guard derruba caso version/exit1. |
| Registro/desregistro seguro | PASSOU | unregister,replacement,mid-publish,dispose-waits,duplicate,disposed; reentradaPublish/limite64; cada teste 0->1->0 com mutação real,fonte restaurado por SHA. Monitor serializa callbacks; Dispose aguardando callback comprovado offline. |
| Erro de extensão isolado | PASSOU | evento defeituoso não impede próximo assinante; leitor/validador excepcionando viramFALHOU_FECHADO; leitura AUSENTE não aprova. Diagnóstico limitado64 não registra mensagem/stack. Código confiável não é sandbox contra deadlock/crash/processo hostil. |
| Pacotes declarativos estritos | PASSOU | test_packages14 casos+subcasos; tipos,campos extras/ausentes,operações,UTF8/chaves duplicadas,tamanho,ID,timeout(inclusive NaN/inf/inteiro enorme),budget/adapter/API. Schema JSON mais invariantes do validador runtime em README. |
| Sem execução arbitrária/autorização no pacote | PASSOU | keys fechadas:authorization/autorizacao/shell/module/assembly/signature/credenciais/op click/exec recusados; to_plan só esperas e host booleano estrito; CLI sem flag sai2 e não lê fonte nem adquire lock. Fonte de extensão C# só vem do host confiável. |
| Mod independente/adaptador opcional | PASSOU na lógica; jogo NÃO_EXERCITADO | Standalonecount2 com SDK/Adapter/Core fisicamente ausentes; ExampleModcompila. PEReader da DLL confirma refs BepInEx/ExampleState/netstandard e estado só netstandard; controlesmod/state exit0,adaptador dependente doSDK exit1. Sem carregar BepInEx em jogo. |
| Cenário sem recompilar kit | PASSOU | CLI menu vs skills gera alvosMainMenu/Skills eobservaçãoexit0,sóJSONtroca; test_switchconfere fonte unchanged;mutaçãodehardcodeMainMenuderruba teste/exit1. |
| Uso semHermes/IA/credenciais/assinatura | PASSOU offline | Pythonstdlib e dotnet via processos normais;nuget.configsem fontes;nenhuma chamada modelo/servidor/conta;exemplos/harness executados de fato sem agente dentro do processo. Compilar mods/ponte requer refs locais do loader/Unity,não redistribuídas. |
| Adaptador por jogo/limites | DOCUMENTADO; runtime INDETERMINADO | README explicitaMono/StolenRealm e ausência de garantiaUnity/IL2CPP;CoreBridgecompila+CoreHarnessfake0->1enabled.Nenhuma prova universal,navegaçãoougameplayreal. |
| NenhumaDLLproprietária publicada | PASSOU noartefato | ZIPfonte44entradas,zeroDLL/.git/perfil/credencial;bytesreabertos/hashconferidos.Nadapublicado.Entradaslib/game-refsomenteinternasàcompilação. |

## Execuções reais e evidências

Caminhos abaixo são relativos à raiz C:/dev/stolen-realm. Evidências volumosas são ferramentas/saídas de bancada em scratch/kit,não arquivos de release de mod.

1. `python tools/automacao/kit13/prove_offline.py --out scratch/kit/KIT-13-run661-final` →exit0.
   -8projetos:preflightDeployToBepInEx=true→exit1;false→exit0. Build só iniciou após exercício dos guards.
   -Buildsmod/harness/standalone/core→exit0;logs listam erros/avisos reais.
   -Harness17tests/failures0;unittest14tests/OK/exit0,nenhumskip.
   -Standalone-no-kitexit0;CoreBridgeexit0(serviçoICoreEventofalso).
   -CLInegadaexit2;menu/skillsexit0;fonteausenteexit1.ResultadoslidosdoJSON,todosruntime_exercitado=false.
2. `python tools/automacao/kit13/prove_mutations.py scratch/kit/KIT-13-run661-final --group py`→exit0,14/14 RED comprovados.
3. Mesmo comando `--group cs`→exit0,17/17 RED comprovados.
4. Mesmo comando `--group extra`→exit0,2/2 RED(Standalone/CoreBridge).
   Cada mutação:fonte sandbox alterado,testebaseline0→mutante1→restaurado0,SHAigualantes/depois. Buildmutanteprecisaexit0;errodecompilação/timeout não vale comoRED.NenhumaAssertionErrorartificial,no-source-live-mutation.
5. Inspector offline PEReader em scratch/kit/KIT-13-run661-inspector:buildexit0apóspreflightrecusadoexit1;mod/stateindependência0;controledadaptação dependente1.
6. Readback207arquivosbaselinevivos/sandboxiguais;20DLLshashesiguaisapósmutações;sem.git. `after-mutations.json` registra lists de mismatchvazias.
7. Travasrepo readonly:check_segredos(incluicheck_padroes_segredo),check_dupes,audita_docsexit0. CobremVERSIONADOS,nãovalidamautomaticamenteuntracked. ScannerDIRIGIDOcommesmosmotores:37arquivospróprios/docsatéparte10,zeroachado,exit0;entregafinalpartesposterioresserãoescaneadasseparadamente.

Localização:
- scratch/kit/KIT-13-run661-final/commands.json (argv/cwd/exit/timeout/log)
- scratch/kit/KIT-13-run661-final/logs/*.log
- scratch/kit/KIT-13-run661-final/cli-{denied,menu,skills,missing}.json
- scratch/kit/KIT-13-run661-final/mutations-{cs,py,extra}/results.json +logsnominais
- scratch/kit/KIT-13-run661-final/{baseline,verification,after-mutations,directed-scan,source-hashes,final-summary}.json
- scratch/kit/KIT-13-run661-inspector/{Program.cs,Inspector.csproj,results.json,mod.log,state.log,negative-adapter.log}
- Checkpointsdocs/automacao/KIT-13-parte01.md até parte11.md,sem sobrescrever histórico.

## Fonte disponibilizada e hashes

Pacote local não publicado:scratch/kit/KIT-13-run661-final/KIT-13-sdk-v1-source.zip
44entradas(27próprias+17fontes/propsreutilizados),102589bytes,zeroDLL,CRC/bytesverificadosdepoisdeabrir.
SHA256:8b85276e39b196279f8cae8c2120b40a656c965da821b806605db37c43e5efcf.

Manifestode27fontespróprioscomSHA256completo:source-hashes.json.NenhummanifestoinventaSHAdeconteúdovazio.

Principaisfontes:
- SDK/RegistryV1.cs:9f2eabdd5da1a3796e7c191f241ff5687d9fb876d51a0bd03117ed1789187700
- packages.py:60f65437a167d5c08ba09647e1d45a265a1c7d28463793f57bb432546b5ea3c6
- test_packages.py:27479be9f3641f1a47792f203a87d9c9a2ae8f238fd61f8cfb679d43c87de94b
- prove_mutations.py:2e37d310d218ebd3c957f8bf4e1cff262957be3895c6520b2890d46e22423269
- CoreBridge/CorePluginBinding.cs:2ee793247db90d948d300811aa84cbb2d3d782112723aa16a262cce3cc749051
- README.md:e96431c59469ee4b16c33a8682bb4003e2814b08420a1543a2d7b8de1faa420c

DLLsinternasbuild(provenientesSOMENTEdasandbox;nomes/caminhoscompletosemverification.json):
- SDK:fa2e0435e4c31f5de008d8c28b6f97587b74ba3d6040a97074379444395c1130
- ExampleMod:7ea0d473dd54ac8038096db777fafb9bb9da2838dca4528029d6bddcab96ef8a
- ExampleState:b5e93b5433a791b9f826b8d3d3cd29c2cbffcafd893c0634f617bf4d2875d458
- CoreBridge:6842b27f0ee20c3b639b3cbe748cf75e9f0312d43f2e0570bb0ce4cdd0583532

DependênciasreusadasSEMedição:
- kit11/executor.py:bf03f81b018157b4c73194df6ace95f00998fb77594047fd92eca0fe57fac3e9
- runtime/coletor.py:159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d
- runtime/controle_acesso.py:379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457

## Lacunas explícitas e próximo passo

NÃO_EXERCITADO:carregamento/modfuncionandoemjogo,BepInExlifecycle/ordemdecarga,UIUX,frame/pixels/personagemreal,navegação/runtimeAUT4,deploy/instalação/save/perfildodono/Thunderstore/IL2CPP/desempenhoemjogo. Não há alteração de UI/UX nem gameplay nesta entrega;se integraçãofuturacriarUI,pedirárevisão de design.

CoreHarness usaICoreEventofalso,JSONexampleséfixture,counter/frameãosintéticos;nenhumvotoPASSOUofflineéprovaruntime. Código de extensãoéconfiável;errocomumisoladonãoprotegehostcontraC#malicioso/crash/bloqueio.EstaéaAPI/pacotedofuturohost,nãogarantiauniversal.

KIT-13R:t_596ee4f5 deve conferir critérios/hashes no disco vivo,executar própria sandbox e refutar versões/pacoteautorizante/import/arbitrário/leases/readers/moddependente.Não apenas reproduzir texto doautor. Autor não participou da revisão. Grafo já contém revisor;nenhumfilhonovo/cronalterado/política/prioridade/modelomodificados.

Semgitadd/commit/push,sempublicação,seminstalar/abrir/fecharjogo. Implementação offline concluída;revisão independente e gates humanos ainda pendentes.
