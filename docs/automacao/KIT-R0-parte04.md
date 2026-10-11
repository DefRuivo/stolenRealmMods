# KIT-R0 — checkpoint 04: execução própria vermelha e inspeção visual

Run 623. Testes executados em sandbox sem build, com USERPROFILE/APPDATA/LOCALAPPDATA/TEMP redirecionados à área de revisão. Logs integrais:
- scratch/kit/KIT-R0-run623/suite.log: runner exit 1. 13 arquivos PASSOU, 2 REPROVOU: t_aut4_estado_docs e t_aut4_runbook exigem a DLL pré-existente ignorada pelo git, que não estava na cópia. A segunda falhou por FileNotFoundError; NÃO contar como prova positiva.
- scratch/kit/KIT-R0-run623/contra-prova.log: runner exit 1; há pelo menos uma contra-prova dependente da mesma DLL. A classificação do runner rejeita exceção como prova; ainda apurar o total pelo parser.
- test-results.json registra comandos/cwd/exit reais. A chamada externa que coordena o lote exit 0 não mascara o exit 1 dos runners.

Mudança de abordagem necessária: copiar explicitamente a DLL já medida para a sandbox, sem recompilar nem instalar, e reexecutar em logs novos. Falha causada por pré-requisito de sandbox, não por modificado código de produto.

Imagem r4/01-ui.png carregada pela ferramenta de visão: captura válida de tela LOADING, cavernas, dica `Potions` e frase de healing/mana. Não aparece marcador AUT4. Origem é captura pela API indicada na fonte, não prova visual da ida-e-volta.

Código lido diretamente: AUT4ProbePlugin.cs:818-845 chama ShowTooltip, relê Title.text e GetParsedText, aceita igualdade do bruto OU renderizado. Linhas 850-867 invocam método real por reflexão. Não há restauração explícita do conteúdo do tooltip nessa função; comentário diz que jogo repinta no quadro seguinte, mas isso não foi medido. Gate G1 só autoriza leitura. Tratarei autorização da intervenção como lacuna separada, não como prova de renderização.

Nenhuma instalação/runtime/publicação realizada nesta revisão. Veredito final ainda pendente de contra-prova CLI, restauração e cadeia dos avaliadores.
