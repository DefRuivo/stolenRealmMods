# KIT-14F3 — candidato inicial reprovado honestamente

Detector imutável executado no mutante: exit1 esperado. Primeiro candidato também reprovou exit1: callbacks693, Update0/OnDestroy1, motor removido, porém eventos0/capturas0. Não foi promovido a PASSOU. Sessão KIT14F3-run1502-on-20261015-130605; evidência preservada em cases/on. Restauração passou todos os itens.

Decompilações REAIS do candidato e produto congelado exit0: candidate-runtime.cs confirma que o bloco de produção EXISTE (não foi contaminado pelo símbolo mutante); candidate-screens.cs confirma sete nomes incluindo RstvSkillTreesWindow; frozen-window.cs confirma o mesmo nome no assembly real do RSTV. Logo não atribuir falha a nome divergente nem ao build mutante sem prova. A investigação seguirá pelo vínculo/ponte e observação real, sem mudar detector ou produto. Fontes e binaries deste primeiro ensaio serão preservados, novas iterações em diretórios novos.
