# KIT-13R — suítes próprias verdes, sem promover runtime

Reviewer escreveu ferramentas próprias apenas em scratch/kit/KIT-13R-run664 (suite não importou testes do implementador): test_review_packages.py, review-cs/Program.cs, review-cs/Review.csproj e run_review_cs.py. Fonte do produto não foi editado.

Comando real: PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s scratch/kit/KIT-13R-run664 -p test_review_packages.py -v
Exit0; Ran14 tests in0.713s OK; sem error/skip. Conferências: versão exata, campos extras em ambos níveis, op allowlist, numeric bool/NaN/inf/orçamento120, JSON duplicado aninhado, limite65536, id/steps, adapter incompatível sem import, permissão bool, negação SEM chamada a leitura/aquisição (traps observados zero), troca alvos sem mudar fonte, inválido/'false'/mapa vazio não verdes, lock ocupado preservado byte a byte e target literal sem execução/código.

Comando real: python tools/automacao/kit13/prove_mutations.py scratch/kit/KIT-13R-run664 --group py
Exit0;14 mutações reais do autor reproduzidas por reviewer: cada0->1->0, fontes restaurados. Não substitui os controles próprios ainda pendentes.

Comando real: python scratch/kit/KIT-13R-run664/run_review_cs.py
Exit0. Preflight reviewer:true exit1 e false exit0 ANTES de build; build Review exit0/0warnings/0errors. Ran13 tests; failures=0. Suíte própria exercita DTO boundaries, versão, falhas ordinárias/diagnósticos sem mensagem, reader/validator null, estados não observados sem chamar validador, Publish reentrante/reset, inscrição durante Publish, substituição durante Publish, leitor que desregistra a própria lease, Dispose aguarda reader concorrente, teardown/recriação de adaptador e mod imune ao observador que lança exceção.

Inspector CLR próprio (PEReader sem carregar DLL):
- Gumatos.KitExampleMod refs netstandard,BepInEx,Gumatos.KitExampleState → exit0
- Gumatos.KitExampleState refs netstandard → exit0
- Controle negativo Gumatos.KitExampleAdapter refs netstandard,Gumatos.KitSdk,Gumatos.KitExampleState → exit1
Logs reais em review-logs e review-commands.json. Dependência obrigatória de SDK/Core/Adapter REFUTADA no binário do mod e estado; controle discriminante real. Carregamento de plugin BepInEx/jogo NAO_EXERCITADO.

Parecer ainda não fechado: falta provar cada teste próprio reprovando com defeito real, mutações C#/extra do autor, scans/ZIP e readback final. Nenhum ACHADO nos casos já executados.
