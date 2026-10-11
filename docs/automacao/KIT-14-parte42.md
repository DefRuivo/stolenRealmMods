# KIT-14 — parte42 / contra-prova real do selo e correção de bancada

python delivery_readback.py REPROVOU de fato,exit1,AssertionError no readback do selo. Histórico não apagado.

Leitura dirigida terminal confirmou EXATAMENTE1 divergência:final-readback.log,0bytes declarados→312bytes reais. Causa:o comando redirecionou stdout do selador para esse log,que foi incluído pelo glob ANTES de o mesmo processo emitir o resumo. Os outros238 arquivos mantêm SHA/tamanho. Selo original prova os payloads no instante da leitura,mas NÃO pode ser anunciado como imutável sem essa ressalva.

Correção limitada à bancada:não editar o selo antigo,não relaxar a comparação de payloads. Emitir selo final novo EXCLUINDO SOMENTE o log ainda sendo escrito,nunca payloads de prova;os238 arquivos restantes devem continuar passando o MESMO comparador de bytes/hash. Preservar selo/relatório/log reprovados e retomar apenas leitura final,não boots/builds/exports prontos.

Os documentos finais terão readback separado (para evitar referência circular de hash do relatório dentro do próprio selo). Resultado de delivery_readback_final.py será verde só se comparação estrita passar,data/Cloud/jogo/junction forem reconferidos e nenhuma fonte baseline divergir. Sem transformar este erro de selamento em verde de runtime do RSTV/recorder.

O limite recorder pós-rollback permanece:eficácia e inexistência durante o jogo INDETERMINADAS;medir/exportar ANTES de remover perfil. Marco/Runner/mod sem kit/comparação de performance não exercitados;KIT-14 não concluído.
