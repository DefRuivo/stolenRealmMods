# KIT-15R — parte 02: leitura fria, hipóteses a exercitar

Reviewer default/run678 != implementer/run677. Somente leitura e docs novas até aqui.

Leitura real dos fontes (UTF-8): instalador.py completo, pacote.py completo, manifesto.json completo, scan.py completo, README.md e primeiro-uso.md, teste_kit15.py até linha 290.

## C1 — hipóteses ainda INDETERMINADAS
- instalador.py:150-188 recalcula SHA dos arquivos encontrados, em vez de validar hashes declarados em componentes[].arquivos; :132-133 aceita origem ausente como lista vazia. Testar pacote corrompido e componente obrigatório ausente.
- :341-370 só reverte divergência de hash após copy2; exceção de I/O pode deixar transação parcial sem recibo/log. Testar falha injetada após primeira escrita, medir disco.
- :399 ação criado na remoção pode fazer rollback apagar em vez de recriar arquivo removido. Testar instalar -> remover -> rollback -> status.
- :335-339 arquivo idêntico pré-existente não recebe backup original. Testar instalar/remover e preservação desse arquivo.
- :368 recibo é substituído apenas pelos itens selecionados. Testar atualização reduzindo opcionais e arquivos órfãos.

## C2/C3 — hipóteses ainda INDETERMINADAS
Pacote copia fontes C# e scripts Python em components/<id>, não DLLs. Recorder apenas três scripts; Runner/Viewer/Integração apenas um cada. Ainda conferir imports fora dessa seleção e executar ZIP extraído sem repo do autor. Uso básico sem SDK/Python não provado por copiar texto: test_14 confere bytes por Python, não funcionamento do kit para usuário sem Python.

## C4 — leitura documental
READMEs e primeiro-uso existem; primeiro-uso recomenda verificar ZIP na pasta extraída, depois rodar testes/empacotamento em tools. pacote.py depende de raiz contendo tools/automacao e recipe aponta origens do repo. Conferir caminho publicado na prática. Primeiro-uso afirma hash com manifesto e rollback sem parcial: sujeito aos testes acima.

## C5/C6 — hipóteses ainda INDETERMINADAS
pacote.py:216-234 não lê/valida conteúdo do manifesto, apenas presença, CRC e scan; main sem --json acessa zip_membros ausente no relatório verificar. Testar comando documentado e mutação de membro com CRC válido. scan.py exclui dirs .git/bin/obj antes de checar e ignora erros de leitura; JSON atribuições com chave entre aspas podem não casar regex. Exercitar nominal e defeitos sintéticos.

Todos os pontos acima são hipóteses de revisão, não vereditos finais. Próximo bloco: inventário/hashes e sandbox própria, execução real.
