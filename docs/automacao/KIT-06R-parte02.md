# KIT-06R — parte 02: inspeção dirigida antes da execução

Reviewer run 638 != implementer run 633. Nenhum fonte alterado.
Lidos integralmente controle_acesso.py, PonteControleRSTV.cs, suíte/contra-prova/runner KIT-06, harness e csproj; entrega e API montar_pacote do KIT-07.

## Hipóteses que exigem reprodução (ainda INDETERMINADO)

- Python ControleAcesso.__init__ usa `atalhos or atalhos_padrao()` (linha 169): mapa vazio explícito ou config totalmente recusada pode reativar F7/F8/F9/F10.
- OBSERVAR é documentado como liga/desliga, mas executar apenas inicia (Python 283/299, C# 263/271); segundo F7 é testado pelo autor como degradação, não como desligamento.
- RETOMAR é ação conhecida/binding aceito, mas não é despachada (Python 274–293; C# 250–268).
- O indicador parte de `_observando=False`; construtor não sincroniza o pipeline existente, enquanto pipeline C# inicia `_pausado=False`. Comparar indicador com registro real antes de habilitar.
- `documento_export`/`DocumentoExport` não incluem eventos/falhas/capturas do pipeline nem a trilha de degradações; apenas contagem no indicador. Comparar arquivo produzido com esperado independente.
- KIT-07 já possui `montar_pacote(origem, destino, politica)` (exportador.py:188); KIT-06 continua afirmando NAO_IMPLEMENTADO. Verificar acessibilidade/integrabilidade concreta, não só string de esquema.
- Ponte C# Marcacoes/DocumentoExport devolvem listas novas mas dicionários vivos; examinar integridade da evidência.
- export não trata exceções de IO; exercitar caminho indisponível sem tocar perfil.

## Limites confirmados da inspeção

UI real/engine input: NAO_EXERCITADO; o próprio autor declara que SRAdapterPlugin.Update ainda não chama PonteControleRSTV. Esta revisão não instalará nem desenhará UI. Compilar um tipo morto não prova acesso sem terminal.
Constantes/properties de foco_forcado, consome_input, encerrou_sessao são sinais; aprovação de ausência de efeitos exige inspeção + execução, nunca apenas valores declarados.
Contra-prova do autor cobre 13 mutações com conjunto exato de FAIL; harness --defeito muda dados fornecidos pelo chamador, não o fonte. Reproduzir e complementar com defeito plantado próprio.

Próximo bloco: inventário/hash, sandbox própria preservando tracked/untracked do escopo, preflight e provas de comportamento reais. Nenhum verde atribuído por leitura ou relatório do autor.
