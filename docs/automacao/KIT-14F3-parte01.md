# KIT-14F3 — abertura da implementação (run1502)

Data local medida: 15/10/2026 12:55 -03. Cartão t_26bf5ae7; implementação independente da coleta run1498. Revisão dependente preexistente: t_59d49835; não será executada nem autoaprovada por este autor.

Escopo: somente instrumento em sandbox. Não alterar RSTV, probe principal/hotspots, Default, gameplay, Assembly-CSharp.dll, políticas ou publicação. Estado inicial: main; uma alteração rastreada preexistente em docs/automacao/EV-R2-NORMAL-b08-parte144.md e arquivos não rastreados de outras frentes (listagem em saída real de git status). Serão preservados por inventário e hash antes de editar.

Leitura inicial: SRAdapterPlugin.cs possui produtor apenas no Update do BaseUnityPlugin (158–186); isto ainda é hipótese de causa, não prova de execução. O método público AlimentarPassivo recebe estados, portanto ensaio direto com booleanos não conta como runtime. O candidato deve observar engine viva, correlacionar sessão/frame/janela e persistir eventos antes do rollback. PipelinePassivo.Resumo não será reetiquetado.

Critérios a provar: assembly congelado/lifecycle; build com DeployToBepInEx=false após controles de deploy; ON com transição real e eventos >0; OFF/config ausente sem motor/callback/evento; mutante sem produtor reprovado pelo mesmo detector; unicidade do motor; restauração imediata verificada de saves/PlayerPrefs/perfil/Cloud. Boot proibido se o jogo já estiver aberto; nunca fechar sessão alheia.

Esta abertura não é resultado nem aceite. Gate completo KIT14, render pós-frame, tooltip, Runner, controles físicos e performance continuam fora do aceite desta correção.
