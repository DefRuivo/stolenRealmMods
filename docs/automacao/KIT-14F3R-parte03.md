# KIT-14F3R — parte 03: evidência primária e limites de serialização

A imagem real preservada passivo-a06417bd08394e0994aa677f1c5b38f1.png foi carregada e inspecionada: All Trees selecionada, Fire selecionada, árvore visível. Não prova clique físico, tooltip ou adequação final de UI/UX. O próximo detector calculará o SHA.

expanded.py: snapshot imediato em 141 precede launch146–149; recibo de arquivos vivos190 precede fechamento220 e preserve236–250; restauração255; hash de PlayerPrefs259; snapshot pós263; rollback265; limpeza268; lock275. Leitura do código e comandos arquivados aponta ordem compatível, sem modificar esse harness.

Limitação concreta do material: isolamento/registro.json NÃO é JSON, mas duas linhas registro_antes_sha256/registro_depois_sha256 iguais. isolamento/restauracao.json contém caminhos Windows sem escapes e SHA com barra invertida (JSON inválido). Um parser json.loads independente reprovou1; não foi convertido nem reescrito. Isto é formato legado do harness, não prova automática de dano nos dados. Será reportado com a força exata: recibos textuais comparáveis, não JSON válido. Manifests e código do comparador precisam sustentar a restauração independentemente do nome da extensão.

Core PipelinePassivo mantém literal NAO_EXERCITADO (:395), limites e confirmação por hash real; pedido e confirmação são distintos. A DLL Core usada permanece congelada: fonte principal serve apenas para entendimento, identidade deve vir do input preservado/assembly real.
