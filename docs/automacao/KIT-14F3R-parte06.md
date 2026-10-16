# KIT-14F3R — parte 06: assembly e causa

A decompilação inicial sem referências tinha avisos de resolução IL. Repetida de forma explícita com ilspycmd -r C:/dev/stolen-realm/lib para runtime candidato, plugin candidato e runtime recompilado pelo revisor: três exits0, zero avisos Unknown result type. Não atualizar ferramenta nem baixar assemblies foi necessário.

Leitura do assembly candidato confirma cadeia não sintética: GameObject.Find + activeInHierarchy + instance/path + Time.frameCount + Input.GetMouseButtonDown alimentam a ponte; candidato emite, mutante Tick não tem esse produtor. O diagnóstico OnDestroy no frame0 do log e fake-null no frame1 com Update0 demonstram perda do MonoBehaviour antes do produtor antigo; não apenas hipótese de configuração. Novo PlayerLoop permanece vivo até captura posterior e remove callback na saída.

A restrição de runtime=NAO_EXERCITADO não foi falsificada; evidência real é externa e correlacionada ao evento. O clique segue handler, não físico. Host All Trees tem declaração nominal em fonte e assembly, não evento inventado de RstvSkillTreesWindow.

Pendente desta revisão: finalizar comparação semântica build/assembly e recibos finais; classificar limitação de recibos históricos com extensão .json inválida sem alterar prova antiga. Nenhum defeito funcional do produtor demonstrado até aqui.
