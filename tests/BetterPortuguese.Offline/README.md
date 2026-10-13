# BetterPortuguese — bancada offline

Execute da raiz: `python tests/BetterPortuguese.Offline/run.py --out <pasta-nova>`.

O runner compila Debug/Release com deploy false, executa o core e confere recursos das DLLs e metadata/IL do assembly real via Cecil. StubTypes.cs fornece tipos SINTÉTICOS só para a bancada net6; o plugin real é compilado contra lib/Assembly-CSharp.dll. A ordem real de preprocessing/getters é conferida no IL, não inferida a partir dos stubs.

HarmonyCoreProbe.cs executa o mesmo core de produção com HarmonyX/MonoMod locais em métodos-isca no CLR desktop do Windows. O probe é compilado com Roslyn do SDK instalado e referências locais do .NET Framework; não precisa instalar targeting pack nem trocar o Harmony do dono. Duas ordens de registro, Original/Corrigido, clones, owner ausente, terceiro com baseline divergente e ciclo são exercitados. Ciclo não garante ordem: o teste detecta a dependência cíclica e só verifica que não se perdeu um postfix.

As fixtures geradas pelo runner têm proveniência SYNTHETIC_OFFLINE_FIXTURE e approvalTaskId sintético. NÃO são decisões editoriais e NÃO entram em Data/ ou no pacote do mod. Hash/parse/diff/tokens/config/clone têm controles negativos. Um recurso adulterado é produzido em memória para provar que SHA falha; a DLL fonte não é regravada.

Dependências: SDK .NET 6, CLR desktop Windows; lib privada do checkout para o plugin; HarmonyX/Cecil/MonoMod locais. O argumento --bepinex-core aceita o core de outro perfil autorizado como fonte de leitura das referências que faltam na lib; somente cópias de teste vão para --out/deps. Não há download, deploy ou boot.

Saídas: logs + verification.json com contagens, hashes das dependências e limites. O host CoreCLR/net6 falhou na execução deste HarmonyX antigo (AccessTools/MethodInvoker); o probe CLR desktop é a alternativa real exercitada, não um teste removido silenciosamente. UI/Mono/jogo/refresh visual/adaptadores de mods continuam NÃO EXERCITADOS.
