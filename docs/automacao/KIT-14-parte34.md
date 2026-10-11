# KIT-14 — parte34 / preflight e builds reais run710

Provas em scratch/kit/KIT-14-run710. preparar.py exit0, prepare.log: 874 tracked+512 untracked inventariados,1385 copiados (nul excluído), sandbox sem .git; referências proprietárias só locais. Snapshots pessoais53/111/5 arquivos. Cloud app1330000 cloudenabled=[0],111/111 dados iguais ao manifesto KIT16 sha25662e0aeea556478d34d16af59d93a0d1370ac275bf5c6d69246c9401a27c3ac61. Frente livre, jogo fechado, diretório real sem junction; estado residual histórico KIT16 não reutilizado.

python scratch/kit/KIT-14-run710/test_build.py:2 testes OK,exit0. Preflight real6 alvos sem optin faltante,controle negativo XML exit1 antes de builds; preflight antes de cada build exit0. AUT4Probe e Adapter/Core compilados na sandbox,-p:DeployToBepInEx=false e USERPROFILE/APPDATA/LOCALAPPDATA isolados; ambos builds exit0. Logs integrais em logs/,comandos em build-results.json. Hashes novos por build sandbox (não são os históricos5781417a):
- AUT4Probe.dll 35e845c0c1a71da83454372dd5452b7463b1edf668d0e59e88eaf17b5240e582
- KIT04Core.dll 84d911a8a6edaf8b081812ccb92b781e7bbc42553a0fbdfad64056616bdc8040
- KIT04Adapter.SR.dll 2a4386bde036d15d8fd2c0f814b0af1ca5fd8d8edf73a04114d794f9900796a8

Harness novo de bancada coleta.py reusa wrappers run704/run702 e finally original intacto. Identidade hash fonte Core declarada corrigida no cfg temporário (antes era DLL no campo fonte); produto não editado. Navegar=true,default12,sem demonstração/escrita tooltip,60s,dados vazios.

python test_guardas.py:11 testes OK exit0; MESMO teste --defeito-cloud:11 testes1FAIL exit1 (RuntimeError não levantado ao remover a guarda). AST prova finally sem alteração. Leitura dos fontes apontou que Core.ResultadoFinal é API,mas não escritor automático; não prometer arquivo recorder sem leitura runtime.

Próximo: executar só sessões faltantes with/without-passive com DLLs atuais, medir e ler logs/PNG/rollback. Cliques OS não tentados. Nenhuma conclusão funcional/overhead antecipada.
