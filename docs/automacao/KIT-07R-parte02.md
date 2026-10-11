# KIT-07R — parte 02: leitura das fontes e hipóteses de refutação

Revisor run 636 != implementador run 634. Fontes lidas por read_file: exportador.py (427 linhas), teste_exportador_kit07.py (261), contra_prova_kit07.py (246), roda_testes_kit07.sh (57). SUPERVISAO lido até final; PROCESSO-REVISAO inteiro. Os scanners reais também foram lidos, sem execução ainda.

## Sanitização / manifest — INDETERMINADO (hipóteses concretas)
exportador.py:302 afirma que manifest/relatório passam pela saída saneada, mas linhas 303–311 gravam JSON/relatório/marcador sem chamar sanear_para_saida. Caminhos incluídos, excluídos e png_para_revisao vêm diretamente dos nomes da origem (217,223,226,248,260,288). Provar vazamento por nome de arquivo/usuário, além do bypass JSON já reconhecido pelo autor.

## Preservação / exclusão segura — INDETERMINADO (hipóteses concretas)
montar_pacote não compara origem/destino e aceita destino com mero marcador (201–206); reexportação não remove arquivos antigos. limpar_temporarios confia somente na presença de um arquivo marcador (355–372). Provar caso origem==destino, resíduo de PNG ao desligar opt-in, colisão manifest/relatorio e marcador inválido sem tocar dados reais.

## Limites de disco — INDETERMINADO (hipótese concreta)
Teto usa tamanho da entrada (229–237,270), não saída sanitizada nem manifest/relatório/marcador. Provar efeito em bytes reais de disco e falha parcial.

## Screenshots / upload / caminhos nominais — INDETERMINADO
PNG opt-in e aviso estão no código; verificar execução. Ausência de imports de rede é evidência estática, não prova isolada de passividade. Suite do autor cobre 14 testes; contra-prova possui 12 mutações e controles. Não declarar verde antes de reproduzir em sandbox própria.

Nenhum produto modificado. Próximo bloco: script próprio para inventariar/copiar arquivos entregues tracked/untracked sem .git/perfil/credenciais e executar testes limitados com evidência redigida.
