# KIT-13R — parecer independente final

## Identidade e alcance

Cartão t_596ee4f5. Revisor default/run664, instância nova, não participou da implementação default/run661 (t_adc1fbfa). Lente: contrato + artefato vivo + execução adversarial própria. Parecer: APROVADO NO ESCOPO OFFLINE, com limitações explícitas. Não é aceite humano, prova de funcionamento BepInEx em jogo, instalação, publicação ou DoD.

Implementação revisada: tools/automacao/kit13, API C#1.0.0 e JSON KIT13/scenario/1. Os27 arquivos vivos próprios são byte-idênticos ao manifesto entregue; hashes completos em scratch/kit/KIT-13R-run664/final-verification.json. As dependências compartilhadas KIT11/Core/coletor/controle_acesso/Directory.Build.props também preservam os hashes baseline. Nenhum fonte de implementação foi editado pelo reviewer; defeitos plantados somente na sandbox própria. Checkpoints KIT-13R-parte01..06 preservam histórico.

Principais SHA256 conferidos diretamente:
- SDK/RegistryV1.cs: 9f2eabdd5da1a3796e7c191f241ff5687d9fb876d51a0bd03117ed1789187700
- packages.py: 60f65437a167d5c08ba09647e1d45a265a1c7d28463793f57bb432546b5ea3c6
- lib/Assembly-CSharp.dll: 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a (não modificada)
- teste Python próprio: 6f8ccc79fa0c81e3fec85f1afb310dd85ab236ba6dfb87263e8ed89c3e9434d0
- Program.cs do reviewer: bee7492672b96988eaad090b23597eca948bc7f354137a15a88aea5466e4d899
- driver de mutações próprio: 6160b22af88fca55c67af791c32e79b801f3b6d4453fc9fe4ebbc3f8af8a9e0d

## C1 — API versionada de eventos/leitores/validadores: OK / PASSOU offline

RegistryV1.cs:49-54 define IExtensionV1 e :58 API1.0.0; DTOs limitam tipos, tamanhos e estados em :14-43. Register :87-99 recusa versões incompatíveis com API_INCOMPATIVEL, sem cadastro parcial, IDs inválidos, duplicatas e excesso64. Harness autor17 e suíte C# própria13 executados exit0. Testes próprios version/dto_bounds cobrem versões1.0.1/1.0/2.0.0/linha extra e limites4096/4097,512/513,frame negativo/long.MaxValue. Guard removido/ampliado na cópia derruba o caso único exit1; restauração repassa exit0. Compatibilidade é EXATA, não promessa de aceitar versão futura.

## C2 — pacote estrito/schema/operações permitidas: OK / PASSOU offline

packages.py:35-79 valida campos EXATOS, IDs, steps1..32/únicos, timeout finito >0 <=60 e orçamento <=120. :82-102 recusa chave JSON duplicada inclusive aninhada, UTF8 inválido, NaN/Infinity e arquivo >65536B antes de carregar inteiro. scenario-v1.schema.json fecha objetos; README documenta validação Python adicional obrigatória, não schema isolado como segurança suficiente.

Suítes Python autor14 + reviewer14 verdes. Reviewer cobre extras nos dois níveis, bool/string/NaN/inf, máximo65536 e65537,2 passos60s aceitos/terceiro0.01 recusado, adapter,32 passos/id64 e duplicata aninhada. Cada método próprio tem fonte real mutado que produz Ran1 FAIL/exit1 (ERROR0/skip0), depois0. Não houve enfraquecimento de trava.

## C3 — registro/desregistro seguro, erro isolado e versão diagnosticada: OK / PASSOU offline

RegistryV1.cs:101-126 usa identidade de Entry e snapshot, não ID sozinho; :128-151 trata null/exceção e Dispose serializado. Reviewer demonstrou inscrição nova só receber próximo evento, substituição durante Publish não executar entrada removida nem nova antecipadamente, lease velha não remover nova, leitura desregistrar a si mesma, Publish reentrante recusado com estado resetado e Dispose de outra thread aguardar READER em voo. Null leitor/validador fecham; estados AUSENTE/NAO_EXERCITADO/FALHOU_FECHADO não chamam validador nem aprovam. Listener defeituoso não impede próximo; diagnóstico não retém mensagem privada. Todos positivos0, fontes sabotados1, restaurados0, C# sempre compilando antes do RED.

CounterAdapter.cs:17-25 valida sessão antes de registrar; :35-39 remove Changed+lease. Reviewer recriou adaptador após Dispose duplo e confirmou contador do mod continua independente. Código C# é CONFIÁVEL: deadlock, crash, código lento/malicioso não são isolados. Essa limitação é declarada no produto, não escondida por aprovação offline.

## C4 — sem execução arbitrária nem autorização de pacote: OK / REFUTADO nos ataques cobertos

packages.py:25-32 importa somente executor KIT11 em caminho fixo de host; nenhuma string do pacote escolhe módulo/DLL. :105-125 exige adapter do host e bool estrito; tradução sempre observacao, ativa_autorizada=false/requer_acao=false, resultado sempre OFFLINE_ONLY/runtime_exercitado=false. Shell/exec/click/deploy/campos authorization/command/output/lock/dll etc recusados antes da execução.

Reviewer executou alvo literal review.sentinel() como chave de estado, sem chamar código/criar artefato, adapter review.sentinel recusado pelo host, negação com traps de leitura/aquisição que permaneceram em0 chamadas. Mutante com permissão forçada/bypass de lock/falso runtime/hardcode foi detectado. Import de executor do próprio host e registro explícito de C#trusted NÃO equivalem a sandbox contra código confiável comprometido. A aprovação não faz promessa universal de segurança.

## C5 — exemplo mod independente, adaptador opcional e cenário sem recompilar: OK lógico / jogo INDETERMINADO

ExamplePlugin só observa CounterState e loga, sem patch/gameplay/UI. ExampleMod.csproj não referencia SDK/Core/Adapter; BepInDependency ausente. Inspector CLR próprio (PEReader, não carregamento de plugin) confirmou:
- Gumatos.KitExampleMod → netstandard,BepInEx,Gumatos.KitExampleState: exit0.
- Gumatos.KitExampleState → netstandard: exit0.
- Controle negativo Gumatos.KitExampleAdapter → netstandard,Gumatos.KitSdk,Gumatos.KitExampleState: exit1.

Standalone físico só com sua própria biblioteca do estado executou count=2; kit absent, exit0. CoreHarness fake disabled=0 enabled=1, exit0, com mutante bypass do enabled exit1. CoreEventsExtension.cs/CorePluginBinding.cs reusam ICoreEvento/Json e hostObservationAuthorized && EstaHabilitado, sem assumir ordem de Awake nem limpar auditoria.

Troca JSON menu→skills observou MainMenu→Skills sem alterar fonte/compilar kit novamente. CLI dá2 negado,0 satisfeito,1 ausente; JSONs relidos têm runtime_exercitado=false. Mod carregado/funcionando EM JOGO permanece NAO_EXERCITADO, não inferido da lógica Standalone.

## C6 — uso sem Hermes/IA e adaptador por jogo: OK / PASSOU offline e documental

Python stdlib e dotnet normais executaram exemplos, testes e ZIP extraído; não chamaram IA/Hermes/conta/credencial/assinatura. nuget.config contém packageSources clear, csproj sem PackageReference. Plugins/ponte usam referências locais não redistribuídas; os componentes puros Standalone/Harness do ZIP compilaram/rodaram em diretório limpo sem lib/ do dono.

README.md:56-60 delimita Mono/Stolen Realm/main thread/lifecycle e exige adaptador/interops específico em IL2CPP. Universal Unity/IL2CPP não é prometido. Funcionamento runtime/IL2CPP/performance em jogo: INDETERMINADO/NAO_EXERCITADO.

## C7 — hashes/preservação/ausência de DLL proprietária: OK no escopo, deriva externa registrada

Sandbox própria sem.git preservou207 fontes e20 hashesDLL baseline após todas mutações. Vivo27/27 próprios e todos compartilhados conferem. Não declarar207 vivos intocados: tools/automacao/kit10/kit10_cenarios.py foi alterado por OUTRA frente durante a rodada, de SHA256 8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092 para 974a2c14ae0985778c7fd909a39537354218c5a14ee992a5fbd8393b36746aeb. KIT13 não importa KIT10, comprovado por busca dirigida; sandbox não recebeu a deriva. Sem hotspot desta revisão (não tocou esse fonte). Audit inicial exit1 preservado; readback dirigido posterior exit0 não apaga a ocorrência.

ZIP fonte autor44 entradas/102589B, SHA256 8b85276e39b196279f8cae8c2120b40a656c965da821b806605db37c43e5efcf; ZIP evidência252/242635B, SHA256 058696f2b7978dd63b37c045506b473f4fea223e77c97ff24b481fb557085a74. Reabertos, CRC OK, membros byte-iguais aos arquivos de origem, zero DLL/MZ/.git/perfil. Nenhuma publicação foi feita; constatar ZIP local não certifica release remota inexistente.

## C8 — positivo/negativo/ausência/timeout/fixture: OK / PASSOU discriminante offline

58 testes ao final:17C#+14Python do autor,13C#+14Python próprios, todos exit0/error0/skip0. Todos58 têm contra-prova real;60 mutações fonte no total =33 do autor (incluem2 extras Standalone/Core) +27 próprias. Cada resultado de mutation foi relido programaticamente,0->1->0 e hash fonte restaurado, bad=[]. C# RED exige build0; Python RED exige FAIL não ERROR. Timeouts/build failure/ausência não contam verdes.

No estado offline inválido/'false'/mapa vazio e lock ocupado nunca OBSERVADO/PASSOU; lock alheio byte-preservado. JSON de fixture sempre qualificado OFFLINE_ONLY. Sem converter prova offline em runtime.

## Comandos reais e evidências de bancada

Raiz C:/dev/stolen-realm. Provas/ferramentas em scratch/kit são DE BANCADA, não arquivos de release de mod.

1. python tools/automacao/kit13/prove_offline.py --out scratch/kit/KIT-13R-run664 → exit0;8 preflights true1/false0 antes de4 builds mod/harness/standalone/core exit0. Logs em logs/, comandos em commands.json.
2. python scratch/kit/KIT-13R-run664/run_review_cs.py → exit0; reviewer preflighttrue1/false0, build0/0warnings/0errors,13 testes0, CLR0/0/1. review-logs e review-commands.json.
3. python -m unittest discover -s scratch/kit/KIT-13R-run664 -p test_review_packages.py -v → Ran14 OK/exit0.
4. python tools/automacao/kit13/prove_mutations.py scratch/kit/KIT-13R-run664 --group py/cs/extra (cada grupo executado separadamente) → exit0;14/17/2. mutations-*/results.json e logs.
5. python scratch/kit/KIT-13R-run664/review_mutations.py py e cs → exit0;14/13. review-mutations-*/results.json e logs individuais.
6. python scratch/kit/KIT-13R-run664/audit_final.py → exit1 EXCLUSIVAMENTE pela derivaKIT10 descrita; antes disso ZIP extraído2builds0/preflight,CLI0,scanners/gates0. audit-verification.json e audit-logs preservados.
7. python scratch/kit/KIT-13R-run664/final_readback.py → exit0;6 execuções reais novamente,58 testes0, fontes/deps/contro les conferidos. final-verification.json e final-logs.

Travas reais check_segredos (inclui check_padroes_segredo),check_dupes,audita_docs exit0 com logs; escopo Git cobre874 versionados, não untracked. Complemento dirigido dos mesmos motores em727 textos (fonte novo,docs,logs,manifestos e membros ZIP): zero hits padrão/genérico, ambos detectam controle sintético só em memória, sem valor gravado/impresso. Scanner não comprova ausência universal de segredo fora do escopo. Documentos finais terão verificação complementar no empacotamento do parecer.

## Limitações e handoff

NAO_EXERCITADO: carregar plugin em jogo/BepInEx lifecycle/ordem de carga, UI/UX/frames/pixels/personagem real, AUT4/navegação, desempenho em jogo, deploy/instalação/save/perfil do dono, Thunderstore/qualquer publicação. CoreHarness fake e frames/estado sintéticos não provam engine. Não foi medido hash do perfil do dono; nenhuma ação de escrita nele foi executada por esta revisão.

Não houve git add/commit/push, alteração de mods/Assembly-CSharp/Bard/gameplay, política/modelo/cron/prioridades, instalador/host autorizado ou jogo aberto/fechado. Nenhum ACHADO bloqueante do escopo entregue; não há tarefa de correção a criar. KIT-15 t_10584ca5 (filha inspecionada) recebe esta aprovação técnica offline; seus outros pais/gates humanos continuam obrigatórios. Concluir KIT-13R encerra o PARECER, não DoD de mod nem aprovação humana/Thunderstore.
