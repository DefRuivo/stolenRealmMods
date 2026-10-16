# KIT-14 — run1471 — três boots novos completos, cobertura limitada

Executados sequencialmente recorder-on, recorder-off, without-kit; todos driver exit0 com restauração. Recorder-off: PID15920/sessão142550,52.932820s. Without-kit: PID8740/sessão142726,45.273500s. Nenhum boot paralelo.

Leitura real da configuração reescrita pelo BepInEx confirma Core/Adapter habilitado=true e passivo=true no ON, false/false no OFF. Binários iguais. O nome ambiente herdado KIT14-run1442-disposable permaneceu no cfg; sessão/paths identificam run1471 (não atribuir ao boot antigo).

Without-kit: lista BepInEx exatamente2 plugins, RealmApi0.1.0 e RSTV0.3.3;15/15 ganchos, nenhum AUT4/Core/Adapter. Isto comprova carregamento independente do kit, NÃO abertura/tooltip do RSTV, nem execução sem o host Hermes (o host continuou ativo).

Todos resultados reportam115 dados/53 perfil/5 outro jogo iguais, PlayerPrefs export igual, jogo fechado/sem junction/backup/perfil temporário, lock livre; readback independente adicional será feito, sem transformar JSON de sucesso em prova suficiente.

Performance: há amostras reais WorkingSet64/PrivateMemorySize64/CPU e marcadores Time.frameCount/realtime. Agregar somente janela comum no fim de Select Party, com valores crus e limitações. Sem eventos passivos no ON; não chamar isto custo de recorder ativo, não gerar p95 por frame ausente. Espaço será bytes dos artefatos persistidos, não I/O total de disco.

Perfis disponíveis consultados por hermes profile list: somente default. Não inventar perfil especialista nem mudar modelos/config. Rota faltante para seleção real de personagem/entrada na run exige instrumento próprio/revisão ou intervenção mínima do dono; clique OS permanece proibido nesta execução headless. Ainda não fechar KIT14 nem liberar filhos com qualificação incompleta.
