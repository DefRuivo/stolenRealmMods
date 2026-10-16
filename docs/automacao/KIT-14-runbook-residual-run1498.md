# KIT-14 — roteiro residual após correção técnica (run1498)

Frente: KIT DE TESTE, não alteração nova de mod. O RSTV é o mod-alvo usado para qualificar a bancada.
Estado agora: não há ação do dono para resolver a falha do recorder. A correção KIT-14F3 t_26bf5ae7 e sua revisão KIT-14F3R t_59d49835 precisam terminar antes da próxima campanha. Não pedir autorização genérica de teste nem limites de performance de novo.

## O agente precisa entregar antes de chamar você

1. Recorder deve realmente observar janela/eventos e persistir contagem não zero, com sessão/frames/PNG correlacionados; configuração habilitada e mensagem carregado não bastam.
2. Leitura deve aguardar All Trees renderizada, observar conteúdo/tooltip e ciclo de abrir/fechar. O PNG atual mostra Fire, mas o dump foi lido no frame do handler e não prova essas dimensões.
3. Exercitar Runner positivo/negativo real, marcação/export in-game e medições comparáveis do recorder ativo. Identificar o que restar não exercitado sem torná-lo automaticamente trabalho humano.
4. Preparar e revisar build exata e hashes, bancada isolada, dados pessoais/registro protegidos e rollback pronto. Não instalar no Default por inferência. Sessão do dono já aberta impede novo boot automático sem decisão dele.

## O que continuará genuinamente humano

Somente em sessão supervisionada PREPARADA e anunciada pelo agente, com build identificada:
- Na run descartável, clicar fisicamente no pequeno botão de árvores ao lado dos botões da barra inferior. A cadeia atual só comprovou o handler interno; precisa confirmar alcance real do mouse/ausência de bloqueio.
- Observar a aba All Trees: barra de classes no topo e nós de Fire dentro da janela, sem sobreposição/corte. Passar o mouse numa skill e dizer se o tooltip fica legível e acima do painel; não gastar pontos.
- Fechar e reabrir a janela e reportar visualmente se apareceu cópia extra ou se algum painel ficou preso.
- Confirmar o aceite visual/funcional no KIT-G4, OU descrever o problema. Aceitar não autoriza publicação automaticamente.

Resposta curta esperada quando chegar essa etapa: botão abriu? tooltip legível? janela fechou/reabriu sem duplicar? O que ficou cortado/sobreposto? Agora NÃO execute esse roteiro numa build/perfil presumidos: a parte técnica ainda está em correção.

## Estado devolvido por esta rodada

Jogo fechado, lock livre, pasta pessoal restaurada sem junction/backup, dados/perfil/PlayerPrefs íntegros por hash. Cloud continuou OFF como já estava no início; não foi religada nem alterada. A janela de ambiente deve atender o bloco runtime pendente antes de pedir restauração global ao dono; ao devolver a máquina para uso pessoal, o operador encerra a bancada e coordena o toggle, sem prometer escrita headless de UI Steam.

Relatório: C:/dev/stolen-realm/docs/automacao/KIT-14-entrega-run1498.md.
Medidas: C:/dev/stolen-realm/scratch/kit/KIT-14-run1498/verification-final.json.
HTML local: C:/dev/stolen-realm/scratch/kit/KIT-14-run1498/postprocess/share-input/report.html.
