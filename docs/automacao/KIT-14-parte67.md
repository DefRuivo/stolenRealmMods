# KIT-14 — run1498: primeiro efeito real e lacuna técnica

Boot recorder-on executado de verdade: sessão KIT14-run1498-recorder-on-20261015-123958, PID17988, campanha exit0. Prova result.json aponta 115 arquivos dados/53 perfil/5 outro jogo iguais por tamanho/hash/conjuntos e PlayerPrefs restaurado; processo fechado, sem junction/backup/perfil temporário, lock liberado. Cloud per-app toggle0 inicial/final preservado; cache Steam mudou e não afirmamos servidor intacto.

Seis testes novos do wrapper passaram; o MESMO teste com require_cloud_off removido da fonte gerada reprovou exit1/1 falha. Nenhum teste é declarado runtime por isso.

Rota F2 agora completa sete etapas, party1/personagem Aspen/HUD ativo, alvo exato RstvRunSkillTreeButton uma vez no quadro515. DLL carregada calculada pelo próprio probe ba0f22b2… igual à congelada. Screenshot 02-final.png foi efetivamente visto: All Trees selecionada, barra de classes e árvore Fire VISÍVEIS. Diferente da tentativa anterior F2 (PNG de inventário); nenhum dado anterior foi reescrito. Frames PNG pedidos515/522, concluídos522/529.

Mas o recorder ON continua com inicialização1/passivo0/runtime NAO_EXERCITADO. Não contar carregamento como observação passiva. JSON da leitura é anterior ao render final e contém textos de outras janelas, logo não promover todo o inventário a árvore medida. Investigar identificação/configuração do Adapter e o caminho já entregue da ponte antes de classificar como humano. Clique físico continua false; tooltip/Runner ativo/marcação in-game ainda não exercitados.
