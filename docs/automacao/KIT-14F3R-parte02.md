# KIT-14F3R — parte 02: leitura independente

Lidos integralmente SRPassiveRuntime.cs (235 linhas), SRAdapterPlugin.cs (248), SRScreenManager.cs (102), csproj, campaign.py e measure-panel.py do candidato final run1519. Nenhum desses arquivos foi editado.

O candidato instala delegate em PostLateUpdate (SRPassiveRuntime.cs:39–75), lê Time/GameObject/activeInHierarchy/GetInstanceID/Input (115–148), confirma captura somente em quadro posterior com arquivo existente (184–203), remove PlayerLoop e assinatura quitting (101–112). PassivoAutorizado exige Adapter + Passivo + Core (SRAdapterPlugin.cs:240–245). Bool API pública permanece separada da origem runtime. Painel atual aparece nominalmente em SRScreenManager.cs:28.

Leitura primária da sessão ON: adapter-runtime.json relata Update0/Destroy1, fake-null Unity e referência CLR viva, 670 callbacks, 0 duplicados, frame destruído1, evento1/captura1, remoção0 motores. recorder-engine.json conserva runtime=NAO_EXERCITADO e evento com engine.frame452/captura454. Isso ainda será confrontado por detector novo, identidades de arquivos e snapshots, não aceito só pelo resumo.

O medidor autoral aceita painel atual em vez da janela alternativa; não altera gate full-rstv, porém auditoria própria precisa verificar mais que os booleanos de restauração em result.json. Próxima fase examina manifests brutos, assembly e controles independentes sem boot/instalação.

Comandos de leitura/listagem: exit0. Nenhum teste funcional verde reivindicado nesta parte.
