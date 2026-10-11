# KIT-13R — controles negativos próprios e do autor concluídos

Comando real: python scratch/kit/KIT-13R-run664/review_mutations.py py && python scratch/kit/KIT-13R-run664/review_mutations.py cs
Exit0. Todos14 testes Python próprios e13 C# próprios mostrados reprovando individualmente: baseline0 → fonte sandbox mutado → teste único exit1 → fonte byte-restaurado → teste único exit0. Python RED exigiu FAIL/AssertionError, Ran1, zeroERROR; C# exigiu build exit0 e Ran1 failures1. Nenhum erro de compilação/timeout foi chamado RED. Logs e before/after SHA em review-mutations-{py,cs}/results.json.

Mutações próprias incluíram: bool em timeout, orçamento/tamanho/JSON/chaves, permissão e leitura negada, lock deliberadamente bypassado, literal de alvo hardcoded, promoção indevida a runtime, fonte ruim promovida; DTO4097 aceito, null reader/validator virando OBSERVADO/PASSOU, snapshot sem cópia, entrada velha usada após reposição, unregistration removida, exclusão sem lock durante reader concorrente, lease do adaptador não removida e exceção do observador vazando. Apenas cópia isolada mutada; não foi necessário mudar produto para ficar verde.

Comando real: python tools/automacao/kit13/prove_mutations.py scratch/kit/KIT-13R-run664 --group cs && ... --group extra
Exit0.17 C# e2 extras 0->1->0, fontes restaurados. Com as14 Python do bloco anterior, as33 mutações do autor foram reproduzidas pelo reviewer, além das27 próprias.

Travas readonly executadas após controles: python tools/check_segredos.py (inclui motor genérico) && python tools/check_dupes.py && python tools/audita_docs.py → exit0 conjunto, cada comando chegou ao final verde.874 versionados; TextFixes101/TextAppends197 sem duplicadas; docs nenhuma inconsistência. Estas CLIs não cobrem untracked! Scanner dirigido dos novos fontes/evidências e readback final ainda pendentes; não interpretar como autorização de release.

Nenhum ACHADO nos critérios exercitados. C3/C8 PASSOU offline com discriminação real. C4 operação arbitrária/autorização de pacote REFUTADAS nos ataques cobertos, não é segurança universal de C# trusted-code. C7 ainda aguarda conferir ZIP/manifestos/fontes/DLL após todas mutações. Runtime/humano/UIUX/IL2CPP continuam NAO_EXERCITADO/INDETERMINADO, não verdes.
