# KIT-09R — parte 03: reprodução e achados medidos

Sandbox: scratch/kit/KIT-09R-run637/sandbox. Preparação real: python scratch/kit/KIT-09R-run637/preparar.py, exit0, 456 arquivos do escopo tools tracked/untracked + entrega/prova RED copiados byte a byte, sem .git. Manifesto: scratch/kit/KIT-09R-run637/baseline.json. Sem build/jogo/deploy.

## Identidade
Hashes vivos conferem com a entrega (kit09.py a4f7587641174960affab6be73590071fe181c86de919dbb87cceb28025f6586; test_kit09.py consta no manifesto; fixtures identidade/verdade/la/velho e prova-red também). rstv.py e coletor.py conferem com os hashes declarados; não foram editados pela revisão.

## Provas reproduzidas
Suite autor exit0, RESULTADO|PASSOU; contra-prova autor exit0, 21 controles; RED autor exit0, suite verde0 -> placeholder neutralizado -> REPROVOU1 específico -> hash restaurado idêntico -> verde0. Logs suite-autor.log, contra-autor.log e red-autor.log no diretório de evidências.
Fronteira CIC-3 reproduzida: test_rstv.py exit1, esperado 'OK', obtido 'NAO_EXERCITADO', log fronteira-cic3.log; não alterada.

## Suite independente
Comando real: python test_review_kit09.py (wrapper subprocess guarda stdout/stderr e exit em suite-review.log).
Resultado literal: Ran 30 tests in 0.181s; FAILED (failures=19). Exit1; 11 passaram; zero ERROR e zero skip. Casos e resultados integrais em review-summary.json e measurements.json.

## Achados confirmados (agrupamento preliminar)
F1 — fixture sintética vira prova runtime: CLI original sobre kit09-verdade.entrada.json (contém sintetico=true e rotulo_fixture) devolve 21 OK, runtime_exercitado=true, prova_runtime=true. Fixture com procedencia=fixture é recusada, mas rótulo/sintético contradizendo procedencia=runtime é ignorado. Saída cli-synthetic-result.json.
F2 — adaptador CIC-5 perde pai/índice/anti-duplicação: normalizar_observacao REAL conserva campos; 3 positivos e 3 defeitos chegam a NAO_EXERCITADO porque regras leem o topo em vez de campos. Snapshot skills/pontos passa pela mesma normalização e detecta gasto/mutação (controle da costura).
F3 — Dependency/arestas: linhas ausentes ou string retornam ausência-legítima OK; mapas vazios retornam arestas OK; T5 sem leitura Dependency vira zero implícito; T5 com aresta inventada retorna sem-aresta-inventada OK. São 5 falhas independentes; outros critérios podem reprovar o conjunto, não validam o falso OK individual.
F4 — dados malformados iguais aprovados: pais []/[]; índice 'bad'/'bad'; índice -1/-1; pontos inf/inf retornam OK. 4 falhas.
F5 — clique em MainMenu/QuitButton retorna clique-físico OK: só exige alvo não vazio, não alvo Skills da run independente.
F6 — dado velho reprova meta (PASSOU) porém outras capacidades continuam OK/prova_runtime=true (FALHOU), produzindo qualificação contraditória da rodada atual.

## Itens que passaram no controle offline
Placeholder no render reprovado; clipping detectado; geometria NaN nunca OK; gasto 5->3 e skills alteradas detectados em snapshot NORMALIZADO real; handler não implica clique; ativo não implica desobstrução; nenhuma observação vira NAO_EXERCITADO. Isto comprova somente regras exercitadas, não jogo.

Próximo bloco: verificar cobertura declarada dos 21 controles, plantar defeitos seletivos na sandbox, executar travas pertinentes e encaminhar correção + reconferência sem modificar produto.
