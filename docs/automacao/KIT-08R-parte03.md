# KIT-08R — parte 03: primeiras provas executadas

Sandbox: scratch/kit/KIT-08R-run648/sandbox. Todos os dados de teste são sintéticos; estes resultados validam a ferramenta, não o jogo.

## Comandos reais e outputs
Execução por `python -c` com subprocess.run, timeout=120, logs separados e returncode capturado:
- `python tools/automacao/kit08/teste_visualizador_kit08.py`: exit0, `Ran 21 tests ... OK` (author-suite.log).
- `python tools/automacao/kit08/contra_prova_kit08.py`: exit0, controle base OK, 7 mutações recusadas por conjunto exato + falso-verde recusado; `VERDE (8/8 defeitos recusados exato)` (author-contra.log).
- `python test_review_kit08.py`: exit1, `Ran 34 tests ... FAILED (failures=24)`, 10 OK, zero ERROR/skip (review.log).
O invólucro python -c terminou exit0, mas NÃO substitui os exits dos testes acima.

## Obstáculo de runner (não verde)
Bash iniciado por subprocess neste ambiente não encontra python: runner exit2 nas duas tentativas (author-runner.log e author-runner-absolute-python.log). Após 2 falhas MUDEI para executar diretamente suíte e contra-prova pelo interpretador real, ambas efetivamente rodadas. Runner shell ainda NAO_EXERCITADO com sucesso; isso não invalida os outputs reais das etapas diretas. Nenhum resultado fabricado.

## Achados comprovados até aqui
- Paths percent-encoded passam validação; F1 em formação, falta conferir URL resultante sem presumir navegador.
- `prova_runtime='false'`, prova vazia, fonte de critério diferente da identidade e fixture em identidade produzem PASSOU.
- Comparação de docs rotulados fixture mostra PASSOU; desaparecimento/duplicação de caso/perda de prova runtime/zero casos produzem estado OK.
- Config/personagem declarados só de um lado e mods diferentes são tratados como comparáveis.
- Aprovação sem hashes ou de mod diferente aparece VIGENTE; observação adicional no HTML: SEM aprovação também aparece VIGENTE, pois renderizar injeta stale/motivos no dict vazio.
- CLI com comparação recusada ou caso removido retorna exit0; --identidade é aplicada DEPOIS da avaliação, devolvendo exit2 onde a avaliação com identidade já aplicada tem PASSOU (simulação offline, sem reivindicação runtime).
- Imagem local existente ao lado da entrada quebra quando HTML é gravado em outra pasta, embora comando retorne exit0.
- Sessão string perdida no contexto; --identidade inexistente causa traceback/exit1 em vez de exit2.

Critérios C3/C4/C5/C7/C8/C9 FALHOU nos cenários exercitados. C6 PASSOU nos payloads HTML/atributos e inspeção CSP (não confirma efeito no browser). C10 caminho positivo e negativos exercitados; próximo bloco terá negativos individuais, mutações seletivas dos controles positivos e fechamento dos grupos de achados sem modificar produto.
