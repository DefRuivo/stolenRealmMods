# KIT-14 — checkpoint 15 / run702

## Escopo reduzido de coleta efetiva
A rodada abaixo será exclusivamente boot/UI disponível sem navegação, clique, carregar personagens, demonstrador de escrita ou save. AUT4Probe buildada no run699 será reutilizada, SHA256 reconferido 679365e2b0496a33b1c9bb77a7e561b40438ae1443d4120f661b2c5f6845dc57. Isso não é recorder contínuo, nem prova o marco completo RSTV.

## Protocolo antes da execução
- Reusar preparar/restaurar do KIT-16 e preparar/rollback do KIT-03; não editar implementação desses pais.
- Perfil BepInEx isolado novo, somente AUT4Probe; cfg pela API derivar_config/escrever_cfg já existente.
- Autorizado=true, Navegar=false, DemostrarTooltip=false, AutorizaEscritaTooltip=false explícitos; orçamento 60s e timeout externo 120s.
- Jogo fechado e frente única adquirida; fechar apenas o PID novo com caminho de executável conferido.
- Prova: JSON vivo e PNG Unity quando produzidos, identidade da DLL carregada e comparação de conteúdo no rollback.
- Coletar amostras cruas de RSS/PrivateMemory/CPU do PID em janela registrada. São dados exploratórios de uma coleta, não comparação com/sem recorder e não aprovação de performance. FPS/frame e I/O não medidos continuam NAO_EXERCITADO.
- Se processo não encerrar, não restaurar link com jogo vivo. Preservar evidências e bloquear para recuperação específica.

## Limite Cloud
Não exercitar navegação/escrita de saves com Cloud pessoal sincronizando. Esta rodada não desliga Cloud e não promete isolamento remoto. Comparar os arquivos de save copiados depois: drift será achado, não mascarado por restauração local.
