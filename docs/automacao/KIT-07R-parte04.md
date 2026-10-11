# KIT-07R — parte 04: execução independente e achados confirmados

## Reprodução do autor — PASSOU (não aprova privacidade geral)
Terminal na sandbox sem .git: `bash tools/automacao/kit07/roda_testes_kit07.sh`, exit 0. Saída real: Ran 14 tests / OK; 12 mutações recusadas; controle falso-verde recusado; modo individual mostrou 14 pares defeito/alvo (13 testes únicos), não prova o test_origem_intacta. A falta de bash resolvendo Windows via subprocess foi contornada pelo terminal hospedeiro.

## Suite própria — FALHOU
Criada em scratch/kit/KIT-07R-run636/test_review_kit07.py, sem alterar produto. Comando `python scratch/kit/KIT-07R-run636/test_review_kit07.py`: exit 1, Ran 24 tests in 0.403s, FAILED (failures=15). Nove positivos OK, quinze refutações FAIL, nenhum ERROR/skip. Assertions só mostram mensagens estáticas, não os valores/prefixos fictícios. Inputs e saídas das probes removidos no tearDown, sem publicar pacotes vazados.

## Veredito inicial por achado (comportamento exercitado)
- F1 ACHADO: nomes de arquivos com credencial sobrevivem nos paths físicos e manifest; nomes locais sobrevivem nas metadatas apesar de nomes_extras.
- F2 ACHADO: JSON password: e valor com aspa escapada vazam segredo; não basta declarar limitação da lib reusada.
- F3 ACHADO: origem marcada == destino é reescrita; destino filho da origem é aceito e modifica origem (probe limitada a max_bytes_por_arquivo=0 para não recursar).
- F4 ACHADO: reexportar PNG com opt-in desligado muda manifest mas deixa PNG antigo no disco; remover log da origem também deixa resíduo não listado no destino.
- F5 ACHADO: inputs manifest.json/relatorio.md são sobrescritos após hashing, quebrando integridade do pacote.
- F6 ACHADO: simples marcador inválido em diretório alheio autoriza apagar keep.txt; não valida conteúdo/proveniência.
- F7 ACHADO: teto de 24 bytes aceita pacote de 1045 bytes; sanitização de e-mail expande acima de teto por arquivo; erro de limite total deixa a.txt parcial sem marcador, impossível limpar com limpar_temporarios.
- F8 ACHADO: erro de I/O com destino arquivo gera traceback bruto e prefixo de credencial em stderr (detectado sem gravar stderr bruto).
- F9 ACHADO: BepInEx/LogOutput.log selecionado é descartado como assembly_proprietario.

## Positivos — PASSOU (offline e cenário limitado)
JSON nominal e hashes; saves/assemblies; PNG opt-in off + aviso; PNG opt-in on e não sanitizado; upload True recusado; origem separada intacta e limpeza nominal; limpeza comum sem marcador recusada; limite nominal por arquivo; sem socket/subprocess/os.system na exportação com audit hook.

Próximo: gravar logs seguros e métricas por probe, mostrar controles negativos dos próprios positivos, rodar scanners isolados, conferir hashes finais e rotear correção para implementador distinto. Runtime/pixels/desempenho NAO_EXERCITADO. Parecer será REPROVADO se os achados se confirmarem no fechamento; fontes do produto não serão corrigidas nesta revisão.
