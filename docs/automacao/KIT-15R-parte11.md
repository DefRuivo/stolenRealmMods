# KIT-15R — parte 11: identidade fechada e falso verde reproduzido

## Execução própria final

python scratch/kit/KIT-15R-run685/test_finish_review.py → exit0 (coleta verificada, produto REPROVADO).

contra-clean → exit1, baseline=True, recusados=6/7, D7 SEM-EFEITO.
contra-planted → exit0, baseline=True, recusados=7/7, falsos-verdes=[].
Entretanto contra-planted/log-07.txt: setUpModule ERROR; Ran 0 tests; FAILED(errors=1). Este é F11, falso verde confirmado em execução própria. Fonte contra_prova_kit15.py:108 aceita substring Ran/test e :170 aprova exit1 sem validar N>0, errors/skip ou alvo_falhou. Isca C# sintética em Core/bin criada/removida só em sandbox. Nenhum ERROR foi contado como teste aprovado.

check_segredos, check_padroes_segredo, check_dupes, audita_docs → exit0 cada, logs próprios. Escopo Git dos scanners não aprova fontes untracked nem neutraliza F10 do scanner do pacote.

## Identidade medida de todos os payloads

finish-verification.json contém comparação ZIP vs fonte viva de 41 membros (42º membro é manifesto gerado). Exatamente um diverge: tools/descoberta.py. Nenhuma DLL no ZIP. ZIP SHA256 126e367b059562ff248d469201ac325142a3d5342ec84458fb75201bdf5708cb;164881bytes;42membros;CRCnull.

descoberta.py no ZIP: a04ffc59125cff05ce2b994049709cb6375ca7fdfc4118150cdae0913dae0f97
fonte vivo:10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86

12 hashes fontes vivos calculados e conservados em source_hashes.535 itens do inventário original permanecem byte-exatos, changed_live=[]; sandbox sem.git.

## Documentação e dependências

PT/EN/primeiro-uso/changelog presentes, porém link de docs/README.md:12 resolve docs/docs/primeiro-uso.md ausente. ZIPSDK sóKitSdk.csproj eRegistryV1.cs: não inclui exemplos/contratos/schema. Primeiro-uso:35 usa CLI que falha; :74 promete conferir manifesto, mas código rehash input; :75 promete atomicidade refutada pelo OSError; :107 promete rollback remoção refutado; :118 promete restaurar preexistente idêntico, que é apagado. Modo manual :125..133 só copia fontes/scripts e compara tamanhos, não demonstra operação básica sem Python/SDK. Compatibilidade do manifesto distingue Windows/Python medido de runtimeUnity/BepInEx e Linux/macOS não medidos; não promover lacunas.

## Gate lido de volta

kanban_show(t_d83f3ef6) após links confirmou children=[t_a1f38855,t_b001720d,t_f19310d3]. Portanto gates técnicos/runtime/publicação esperam correção com revisão independente. Correção já existente, sem duplicação.

Parecer final será REPROVADO: revisão concluída, produto não aprovado. Não foram alterados produto, política, modelo, cron, prioridade, gates humanos ou perfil do dono.
