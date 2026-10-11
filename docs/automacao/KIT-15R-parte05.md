# KIT-15R — parte 05: oráculo independente e efeitos de falha

Execução real: python scratch/kit/KIT-15R-run678/test_review_kit15.py; saída Ran 27 tests in 18.178s, FAILED (failures=21), REVIEW_EXIT=1; 0 ERROR/0 skip. Resultado bruto com todos efeitos medidos: scratch/kit/KIT-15R-run678/review-results.json. Esses testes conferem contrato esperado, não transformam defeito em OK.

## Falhas comprovadas (não hipóteses)
F2 integridade: fonte adulterado instalado exit0; Core obrigatório ausente = 29 arquivos/INSTALADO/0; arquivo não listado instalado; ZIP com fonte alterado e CRC válido = OK/0; ZIP contendo só manifesto {} = OK/0.
F3 atomicidade: OSError plantado na terceira cópia deixa dois fontes instalados, sem recibo.
F4 rollback remoção: antes41 -> depois0; rollback retorna0/problemas[] e restaura apenas recibo; status DIVERGENTE com41 faltantes.
F5 propriedade: arquivo pré-existente idêntico apagado; instalar->atualizar->remover deixa Json.cs original DO KIT; atualização --sem-opcionais perde propriedade de5 arquivos que continuam no disco.
F6 backup: remover restaura bytes 'corrupted backup' e declara0/problemas[].
F7 CLI documentada pacote.py verificar sem --json = traceback KeyError 'zip_membros', exit1.
F8 independente do repo: suite e repack extraídos = erro infra/2 (raiz tools/automacao ausente).
F9 fechamento de dependências: Runner busca components/runtime/coletor.py ausente; Viewer KIT09 ausente; integração4 módulos e pertinencia ausentes; Adapter ProjectReference não resolve.
F10 scanner: senha JSON entre aspas, bin/Assembly-CSharp.dll em diretório e erro de leitura sintético todos produzem achados[].

## Positivos reais
P1 instala41/hash individual + restaura arquivo usuário distinto + preserva alheio. P2 atualização muda1 e rollback devolve bytes. P3 corrupção na cópia é revertida sem payload parcial. P4 scan nominal/segredo AWS sintético/removido =0->1->0. P5 DLL sintética dentro ZIP detectada. Esses positivos não anulam falhas das fronteiras.

## Defeito no primeiro oráculo do revisor (histórico preservado)
Teste shell extraído estava passando INDEVIDAMENTE: bash recebeu path com backslash, exit127; assert rc!=2 aceitava127. Corrigido SOMENTE o script do revisor (as_posix e assert rc==0). Não é prova válida de shell, nem produto corrigido. Próxima execução conserva relatório inicial separado e recaptura shell real. Nenhum fonte vivo editado.

Parecer parcial REPROVADO. Ainda executar controles negativos dos5 positivos, capturar exits/logs individuais, conferir preservação e encaminhar correção ao implementador.
