# KIT-11R — parte 04: suite final e prova de sensibilidade

Comando real: python scratch/kit/KIT-11R-run653/test_mutations.py && python -c <subprocess captura review-final/author-baseline/author-isca>.
Mutação em fonte compilado em memória, contexto sandbox; bytes executor.py nunca editados. 12 mutações distintas, cada teste-alvo reprovou sem ERROR/skip; restauração em memória seguida de Ran 12 tests in 0.078s / OK; driver de mutações exit 0.

Mutações cobertas: true de arquivo ignorado; satisfação prematura sem polling; veredito ativo errado; timeout carimbado OBSERVADO; cancelamento carimbado OBSERVADO; versão incompatível aceita; campos executáveis aceitos (6 subtestes reprovam); autorização ativa bypass; ambiente divergente aceito; lock vivo aceito; backup corrompido; arquivo ausente carimbado satisfeito. Logs red-test_*.log e restored-controls.log; matriz mutation-results.json dentro da sandbox.

Primeira tentativa detectou um negativo do reviewer bloqueando por ambiente em vez de autorização: mutação de autorização escapou. Corrigido teste fornecendo ambiente válido, rerodado e agora a mutação deixa o teste vermelho. Não houve ajuste do produto para ficar verde. Relato inicial parte03 preservado.

## Resultado definitivo do bloco
- review-final.log: Ran 36 tests in 0.164s; FAILED (failures=24); exit 1. 12 testes OK, 24 FAIL, nenhum ERROR/skip.
- author-baseline.log: 12 teste(s), 0 falha(s); exit 0.
- author-isca.log: 13 teste(s), 1 falha(s); exit 1. Isca incondicional não comprova sensibilidade de executor (test_kit11_executor.py:318-319).
- runs.json guarda comandos e exits reais dos três subprocessos. Exit 0 do wrapper somente captura; parecer NÃO aprovado.

C8 requer_acao='false' também FALHOU após isolar ambiente: campo normalizado para True em vez de configuração recusada. Demais 23 falhas iniciais reconfirmadas.

C1/C2/C3/C4/C5/C7/C8: ACHADO/FALHOU. C6: igualdade declarada offline PASSOU, runtime NAO_EXERCITADO. C9: não execução de comandos arbitrários PASSOU para os campos conhecidos e contraprova vermelha. C10: cobertura própria insuficiente para aceitar segurança (autor verde diante de 24 violações); review offline efetivamente exercitada. C11/C12 e travas finais ainda pendentes.
