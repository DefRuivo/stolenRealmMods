# KIT-14 — run704 / checkpoint 25: contexto e fronteira

Entregas runs702/703, KIT-16 e KIT-G2 foram lidas por inteiro; revisão KIT-14R t_9ce7d260 inspecionada (todo, dependente deste cartão). Não liberar filho nem criar revisão duplicada com execução incompleta.

Reuso escolhido: harness run702 para instalação/rollback KIT03 + junction/registro KIT16 + lançamento Steam com override Mono + encerramento gracioso somente por PID criado. O arquivo histórico não será alterado nem reexecutado no mesmo diretório de prova. O preflight readonly run703 também não será reexecutado sobrescrevendo evidência histórica.

Escopo de autorização: KIT-G2 permite navegação isolada por handler e observação, não save do dono. KIT16 copia os dados pessoais para área isolada: isso preserva arquivos reais, mas não transforma personagens pessoais em personagens descartáveis. Não presumir autorização para selecionar cópia de personagem do dono; qualquer cenário deve manter essa fronteira explícita.

Pendências técnicas dirigidas antes do boot: confirmar toggle Cloud atual por leitura, descobrir handlers reais existentes no AUT4/Runner, conferir identidade/pacote, decidir quais cenários podem ser exercitados sem carregar save pessoal. Clique físico será residual do dono (não se confunde com Button.onClick.Invoke).

Histórico preservado: run702 = 24 objetos/2 PNG de loading e pós-processamento; não valida Skills. Performance histórica = amostras de boot somente com probe, não delta recorder. Limiares dispensados pelo dono, números sintéticos proibidos.

Próximo bloco: preflight readonly novo e inventário dirigido das capacidades existentes. Nenhuma instalação, navegação ou escrita de save executada até este checkpoint.
