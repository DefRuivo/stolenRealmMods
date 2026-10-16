# KIT-14F3 — desenho do candidato e execução negada

O assembly histórico decompilado confirma o Update exclusivo e guardas Unity Object.op_Equality no Core (inclusive AlimentarPassivo), portanto há uma segunda barreira se o motor for movido sem corrigir fake-null. O candidato usa ReferenceEquals no caminho passivo e conserva o teste Unity como diagnóstico separado de lifecycle, não como autorização.

Mudanças em andamento apenas em scratch/kit/KIT-14F3-run1502/sandbox: entrada do motor, retirada do produtor passivo do Update para impedir duplicação, guarda de três opt-ins e nome real RstvSkillTreesWindow. Core fonte/pipeline não alterados; no csproj COPIADO do Core somente caminhos das referências para permitir build em sandbox. O runtime usará a DLL Core congelada.

Uma chamada execute_code foi NEGADA pelo modo headless (nenhuma chamada interna executada). Não houve alteração de política ou tentativa de contorno; as edições seguem pelas ferramentas normais permitidas. Build e boot ainda não executados nesta fase.
