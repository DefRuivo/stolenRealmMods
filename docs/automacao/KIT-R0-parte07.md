# KIT-R0 — checkpoint 07: costura executada e estado atual

Comando real `python scratch/kit/KIT-R0-run623/integration_audit.py && bash scratch/kit/front-unica.sh check`, exit 0. Script importa módulos existentes da sandbox, não altera implementação. Saídas: integration-results.json, consolidado-revisor.json, profile-now.json.

Costura medida sobre r3 real:
- AUT-5 cru: 24 observações, sessão/hash/procedência runtime presentes em 0/24.
- AUT-5 após coletor normalizar: 24/24 com sessão/hash/procedência runtime. A integração crua anunciada pelo docstring não preserva o contexto do topo.
- Avaliador RSTV/AUT-5: 6 NAO_EXERCITADO e 1 REPROVADO, tanto cru quanto normal; 0 provas runtime de RSTV. Inspecionar o REPROVADO antes de atribuir defeito ao mod, que nem carregou no perfil isolado.
- AUT-6 normal: 23 NAO_EXERCITADO, 1 INDETERMINADO, 0 provas runtime; casos de tipo limite excluídos explicitamente para evitar varredura de assets proprietários fora do escopo.
- AUT-7 normal: 10 NAO_EXERCITADO, 1 INDETERMINADO, 0 provas runtime.
Nenhum hash do probe foi apresentado como identidade de um mod não carregado. Esses resultados não são validação funcional dos mods; comprovam consumo/recusa pelos avaliadores existentes e lacunas reais.

Verificação atual independente de restauração:
- processo Stolen ausente (tasklist /FO CSV /NH, exit 0).
- scratch/aut4-runtime-iso ausente.
- lock disponível (check exit 0); nenhum lock adquirido pelo revisor.
- resíduos AUT4 no perfil do dono: 0.
- hashes de metadados de core (18 arquivos), plugins (21), diretório de saves declarado (5) e SHA256 do LogOutput batem com antes.txt.

Achado importante de força da prova: o algoritmo hash_tree de runtime-isolado.sh:101-105 hasheia caminhos/tamanhos/mtime, NÃO conteúdo. A reprodução Python do mesmo algoritmo deu exatamente os hashes upstream. Portanto a afirmação `bit-a-bit intactos` não decorre daquela linha de base. Snapshot novo de conteúdo foi feito pelo revisor, mas não pode retroagir e fabricar hash de bytes anterior à rodada. Não há evidência de corrupção, há prova anterior insuficiente para a afirmação forte.

Único perfil real disponível confirmado por `hermes profile list`: default. Independência nesta revisão é nova instância/run 623 contra run 622, não troca de perfil. Não mudar modelo/política.
