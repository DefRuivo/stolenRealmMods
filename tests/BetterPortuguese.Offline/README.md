# BetterPortuguese — bancada offline

Execute da raiz: `python tests/BetterPortuguese.Offline/run.py --out <pasta-nova>`.

A contagem esperada de chaves alteradas é lida de `BetterPortuguese/Data/manifest.json` (`coverage.changedKeys`); `--expected-changes N` só é necessário para candidatos experimentais.

O runner compila Debug/Release com deploy false, executa o core e confere recursos das DLLs e metadata/IL do assembly real via Cecil. StubTypes.cs fornece tipos SINTÉTICOS só para a bancada net6; o plugin real é compilado contra lib/Assembly-CSharp.dll. A ordem real de preprocessing/getters é conferida no IL, não inferida a partir dos stubs.

HarmonyCoreProbe.cs executa o mesmo core de produção com HarmonyX/MonoMod locais em métodos-isca no CLR desktop do Windows. O probe é compilado com Roslyn do SDK instalado e referências locais do .NET Framework; não precisa instalar targeting pack nem trocar o Harmony do dono. Duas ordens de registro, Original/Corrigido, clones, owner ausente, terceiro com baseline divergente e ciclo são exercitados. Ciclo não garante ordem: o teste detecta a dependência cíclica e só verifica que não se perdeu um postfix.

As fixtures geradas pelo runner têm proveniência SYNTHETIC_OFFLINE_FIXTURE e approvalTaskId sintético. NÃO são decisões editoriais e NÃO entram em Data/ ou no pacote do mod. Hash/parse/diff/tokens/config/clone têm controles negativos. Um recurso adulterado é produzido em memória para provar que SHA falha; a DLL fonte não é regravada.

Dependências: SDK .NET 6, CLR desktop Windows; lib privada do checkout para o plugin; HarmonyX/Cecil/MonoMod locais. O argumento --bepinex-core aceita o core de outro perfil autorizado como fonte de leitura das referências que faltam na lib; somente cópias de teste vão para --out/deps. Não há download, deploy ou boot.

Saídas: logs + verification.json com contagens, hashes das dependências e limites. O host CoreCLR/net6 falhou na execução deste HarmonyX antigo (AccessTools/MethodInvoker); o probe CLR desktop é a alternativa real exercitada, não um teste removido silenciosamente. Esta suíte não abre a UI/Mono/jogo nem prova refresh visual.

BP-MODS-1: ModTests valida as 177 regras e cada uma das 222 ocorrências de notas coloridas extraídas de TextAppends/TextFixes pelo parser canônico tools/tabelas.py (114 blocos distintos). mod_probe.py também recorta literalmente os métodos de ordenação do BT para BTOrder.generated.cs, com hash e linhas de proveniência. ModsHarmonyProbe executa os hooks reais do adaptador e esse recorte em métodos SINTÉTICOS no CLR: 32 combinações de notas/sinergia/aura e paletas distintas/coincidentes, igualdade exata de separadores e ordem, controles BP off/inglês/versão/assembly ausente, exceção e status vinculado criado depois do prefix. Não patcheia nenhum alvo do jogo. O runner exige também o fonte de BetterTooltips deste checkout. A prova Unity é separada em docs/automacao/BP-MODS-entrega.md.

A medição de alocação reutiliza o isolamento GC do BP-COMP, sem aumentar o orçamento (<1024 bytes/100.000 chamadas) nem escolher a melhor amostra. Falhar em iniciar/encerrar a região sem GC reprova. A contra-prova desta entrega injeta uma alocação por chamada e deve reprovar.
