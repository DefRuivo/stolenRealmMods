# KIT-13 — entrega final OFFLINE (run 661)

Este documento é o índice final legível da entrega. O registro inicial KIT-13-entrega.md e os checkpoints foram preservados, sem sobrescrita.

Cartão: t_adc1fbfa. Implementador: default/run661. Revisão independente precriada: t_596ee4f5 (KIT-13R), ainda pendente, por outra instância. Concluir a fase de implementação libera essa revisão; não constitui autoaprovação, aceite humano, prova em jogo, autorização de deploy ou publicação/DoD.

## O que foi implementado

27 arquivos novos em tools/automacao/kit13, enumerados com hashes em source-hashes.json:

- SDK C# 1.0.0, namespace Gumatos.KitSdk.V1: eventos, leitores, validadores e registro IDisposable. Núcleo netstandard2.1 sem Unity/BepInEx/jogo.
- Pacotes JSON KIT13/scenario/1, schema fechado e validador Python stdlib. Só esperas menu/tela/condicao; nenhuma autorização, código, DLL, import dinâmico por pacote, shell ou ação ativa.
- Tradução para executor/FonteDeArquivo/FrenteUnica do KIT-11. A autorização vem exclusivamente do host, é bool estrito, e ativa é sempre false. Reuso real de controle_acesso/coletor pelo executor; nenhuma engine de navegação ou avaliador AUT/CIC duplicado.
- ExampleMod BepInEx e ExampleState: contador observacional independente do kit. Não alteram gameplay/UI nem aplicam patches. OptionalAdapter separado expõe leitura/validação/eventos, sem dependência obrigatória no mod.
- CoreBridge opcional reutiliza ICoreEvento/Json. CorePluginBinding cria facade dos métodos públicos do Core, sem cast inválido nem assumir ordem de Awake. A ponte exige autorização externa e Core habilitado, não limpa auditoria.
- Harness, Standalone e CoreHarness; runners de sandbox, mutações seletivas, exemplos JSON e README com contrato, comandos, limites e desfazer.

Nenhum arquivo de implementação pré-existente foi editado. Builds apenas em cópia isolada, com DeployToBepInEx=false e referências locais de compilação. Nenhum perfil/save/jogo/publicação foi tocado.

## Veredito por aceite — prova do autor, não revisão independente

| Aceite | Resultado | Evidência e limite |
|---|---|---|
| API versionada de eventos/leitores/validadores | PASSOU offline | SDK compilado, Harness 17 casos exit0. API exata 1.0.0; 2.0.0 recusada sem registro, diagnóstico API_INCOMPATIVEL. Guard removido derruba caso version. |
| Registro/desregistro seguro | PASSOU offline | Inscrições únicas/limitadas; lease antiga não remove nova; unsubscribe durante Publish; reentrada recusada; Dispose de outra thread aguarda callback terminar. Casos correspondentes 0->1->0 com mutação real. |
| Erro de extensão isolado | PASSOU offline | Listener defeituoso não impede próximo; leitor/validador com exceção/null falham fechado. Leitura AUSENTE não aprova. Diagnóstico retém no máximo64 tipos de erro, sem mensagem/stack. Código C# é confiável, não sandbox contra crash/deadlock/malícia. |
| Pacotes declarativos estritos | PASSOU offline | 14 unittest + subcasos de tipos, campos, versão, adapter, duplicatas JSON, UTF8/tamanho, passos/IDs, allowlist, timeout e orçamento. Schema e invariantes adicionais estão documentados. |
| Sem execução arbitrária/autorização embutida | PASSOU offline | Campos desconhecidos recusados, incluindo authorization/autorizacao/shell/module/assembly/signature; click/exec recusados. Host decide observação. CLI negada exit2 sem ler fonte nem adquirir lock. Extensão em código é registrada explicitamente pelo host, nunca carregada pelo pacote. |
| Mod independente e adaptador opcional | PASSOU na lógica; jogo NÃO_EXERCITADO | Standalone count2 com SDK/Adapter/Core fisicamente ausentes. Plugin compila. Inspeção CLR: mod referencia só BepInEx/ExampleState/netstandard; estado só netstandard. Controle negativo Adapter referencia SDK e reprova. |
| Cenário sem recompilar kit | PASSOU offline | Troca de menu.json por skills.json produz alvos MainMenu/Skills com fonte do kit intacta; test_switch confirma. Hardcode plantado no tradutor reprova. |
| Uso sem Hermes/IA/credenciais/assinatura | PASSOU offline | Processos Python/dotnet normais executaram exemplos/harness; Python stdlib, projetos sem NuGet e nuget.config sem fontes. Nenhum modelo, servidor, conta, rede ou assinatura comercial exigido. Compilar plugin/ponte requer refs locais não distribuídas. |
| Adaptador por jogo, não universal Unity/IL2CPP | DOCUMENTADO; runtime INDETERMINADO | README delimita Mono/Stolen Realm, inicialização/main thread e falta de suporte universal. CoreHarness usa serviço falso; não prova Core carregado em jogo. |
| Não publicar DLL proprietária | PASSOU no artefato | ZIP fonte reaberto e conferido byte a byte: zero DLL/.git/perfil/credencial. Não houve publicação. Refs binárias ficaram só na sandbox local. |

API/contrato: cadastro com ID único e API exata, máximo64 extensões; Publish usa snapshot e revalida identidade. Evento tem sessão/kind <=128 chars, frame >=0, data <=4096. Leitura tem status tipado e valor <=4096; veredito tem status tipado e motivo <=512. Código lento/bloqueante não é isolado: callback não deve esperar lock externo que Dispose segura. CounterState/CounterAdapter são exemplos para main thread, não estado Unity thread-safe.

Pacotes: UTF8 <=65536 bytes, chaves JSON únicas, steps1..32, IDs de passo únicos, textos não brancos/limitados, timeout finito >0 <=60s, soma <=120s e condições do vocabulário KIT11. O adapter declarado deve coincidir com o host; não é nome de módulo para import. CLI aceita somente offline-file.v1, sempre runtime_exercitado=false/OFFLINE_ONLY.

## Execuções reais

Raiz: C:/dev/stolen-realm. Provas em scratch/kit são saídas/ferramentas de bancada, não release de mod.

1. `python tools/automacao/kit13/prove_offline.py --out scratch/kit/KIT-13-run661-final` — exit0.
   - 8 projetos: preflight deploy=true recusado exit1; false permitido exit0. Build só começou após exercer os guards.
   - Builds mod/harness/standalone/core: exit0. Logs registram avisos e erros reais.
   - Harness: Ran17 tests, failures0. Python: Ran14 tests, OK, sem skip.
   - Standalone sem kit: exit0. CoreHarness: exit0, disabled=0/enabled=1, serviço ICoreEvento falso.
   - CLI negada exit2; menu/skills exit0; fonte ausente exit1. Resultados lidos dos arquivos; todos runtime_exercitado=false.
2. `python tools/automacao/kit13/prove_mutations.py scratch/kit/KIT-13-run661-final --group py` — exit0,14/14 controles.
3. Mesmo comando `--group cs` — exit0,17/17 controles.
4. Mesmo comando `--group extra` — exit0,2/2 controles (Standalone/CoreBridge).

Total33 mutações de implementação reais, cada caso baseline0 -> mutante1 -> restaurado0, SHA igual antes/depois. O mutante C# precisava compilar exit0; erro de compilação/timeout não conta como RED. Não houve AssertionError artificial nem mudança nos testes para aceitar mutantes. Somente fontes sandbox foram mutados.

5. Inspector PEReader/MetadataReader: preflight recusado exit1, build exit0, mod/state independência exit0; adaptador dependente do SDK reprova exit1. DLL não foi carregada no jogo.
6. Readback após todas as mutações:207 fontes baseline iguais no vivo/sandbox;20 hashes DLL iguais; nenhum mismatch; sandbox sem.git.
7. Travas repo readonly: check_segredos (inclui check_padroes_segredo), check_dupes, audita_docs exit0. Cobrem versionados. Scanner dirigido dos mesmos motores nos novos arquivos:37 fontes/docs até parte10, zero candidato, exit0; documentos finais terão varredura complementar.

Caminhos de reprodução:
- scratch/kit/KIT-13-run661-final/commands.json e logs/*.log
- scratch/kit/KIT-13-run661-final/cli-{denied,menu,skills,missing}.json
- scratch/kit/KIT-13-run661-final/mutations-{cs,py,extra}/results.json e logs individuais
- scratch/kit/KIT-13-run661-final/{baseline,verification,after-mutations,directed-scan,source-hashes,final-summary}.json
- scratch/kit/KIT-13-run661-inspector: fonte do inspector, results.json e logs mod/state/negative-adapter
- tools/automacao/kit13/README.md: uso sem IA, contrato, comandos de prova/CLI e como desfazer.

## Artefato local e identidade

Fonte disponibilizada, NÃO publicada:
C:/dev/stolen-realm/scratch/kit/KIT-13-run661-final/KIT-13-sdk-v1-source.zip
44 entradas (27 próprias +17 fontes/props reutilizados),102589 bytes,zero DLL; CRC e bytes verificados ao reabrir.
SHA256:8b85276e39b196279f8cae8c2120b40a656c965da821b806605db37c43e5efcf.

source-hashes.json contém todos os27 hashes próprios. Principais SHA256:
- SDK/RegistryV1.cs:9f2eabdd5da1a3796e7c191f241ff5687d9fb876d51a0bd03117ed1789187700
- packages.py:60f65437a167d5c08ba09647e1d45a265a1c7d28463793f57bb432546b5ea3c6
- test_packages.py:27479be9f3641f1a47792f203a87d9c9a2ae8f238fd61f8cfb679d43c87de94b
- prove_mutations.py:2e37d310d218ebd3c957f8bf4e1cff262957be3895c6520b2890d46e22423269
- CoreBridge/CorePluginBinding.cs:2ee793247db90d948d300811aa84cbb2d3d782112723aa16a262cce3cc749051
- README.md:e96431c59469ee4b16c33a8682bb4003e2814b08420a1543a2d7b8de1faa420c

DLLs internas da sandbox (nomes/caminhos completos em verification.json):
- SDK:fa2e0435e4c31f5de008d8c28b6f97587b74ba3d6040a97074379444395c1130
- ExampleMod:7ea0d473dd54ac8038096db777fafb9bb9da2838dca4528029d6bddcab96ef8a
- ExampleState:b5e93b5433a791b9f826b8d3d3cd29c2cbffcafd893c0634f617bf4d2875d458
- CoreBridge:6842b27f0ee20c3b639b3cbe748cf75e9f0312d43f2e0570bb0ce4cdd0583532

Dependências reutilizadas sem edição:
- kit11/executor.py:bf03f81b018157b4c73194df6ace95f00998fb77594047fd92eca0fe57fac3e9
- runtime/coletor.py:159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d
- runtime/controle_acesso.py:379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457

## Lacunas e handoff

NÃO_EXERCITADO: carregamento/funcionamento do plugin em jogo, BepInEx lifecycle/ordem de carga, UI/UX, frames/pixels/personagem real, navegação/runtime AUT4, deploy/instalação/save/perfil do dono, Thunderstore, IL2CPP e desempenho em jogo. Não há mudança de UI/UX nesta entrega; integração futura que crie UI exigirá revisão de design.

CoreHarness é fake, exemplos JSON são fixtures e contador/frame são sintéticos. Nenhum PASSOU offline certifica runtime. Sessão/quadro são informados pelo host; pacote não certifica procedência nem inventa hashes. Código C# confiável pode agir com permissões do processo, fora da segurança do pacote declarativo.

Próximo passo: KIT-13R/t_596ee4f5, por outra instância, deve verificar hashes/estado vivo, executar sandbox própria e tentar refutar execução arbitrária, autorização embutida, compatibilidade/leases, falhas de leitores/validadores e mod dependente do kit. Não apenas reproduzir o relatório do autor. Implementador não fez revisão independente nem criou revisão duplicada.

Nenhum git add/commit/push, publicação, alteração de política/modelo/cron/prioridade ou jogo aberto/fechado. Implementação offline concluída; revisão independente e gates humanos continuam pendentes.
