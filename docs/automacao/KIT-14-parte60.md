# KIT-14 — run1471 — causa concreta encontrada

Leitura direta de LogOutput-isolado.txt: linha21 BepInEx rejeitou RSTV0.3.3 por dependência ausente com.gumatos.realmapi >=0.1.0. Havia4 plugins candidatos, apenas3 carregados (probe/Core/Adapter). Não é falha de clique nem prova de crash.

Probe: rota Play/Roguelike/Accept invocada por handlers em quadros440/449/458; busca Skills esgotou3600 tentativas, GUI ChoosingCharacter. CONCLUIDO é término do coletor e NÃO sucesso RSTV. Recorder: apenas inicializacao=1, passivo.eventos_total=0, runtime=NAO_EXERCITADO.

PNG carregado visualmente: Select Party, Riley nível1 disponível, party vazia, Choose Powerups/Accept Party. Sem loading, sem Skills/janela RSTV. Os dois PNG são idênticos. São prova de captura da tela nativa, não da janela requerida.

Próximo ajuste dentro do escopo: corrigir somente montagem da bancada com a dependência REAL do RSTV, conferindo binário/config; nenhuma alteração de produto. Não repetir a rota sabidamente incapaz sem esse ajuste. Busca de arquivos devolveu resultado suspeito (.git/.worktrees em vez de csproj); usar inventário dirigido por Python, não adotar esse resultado.

Nenhum boot novo nesta retomada. Se binário/dependência disponível e preflight íntegro, nova rodada isolada com instrumentos identificados; registrar previamente negativos e preservação. Não prometer qualificação integral pelo simples fim do probe.
