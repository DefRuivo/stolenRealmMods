# KIT-R0 — checkpoint 06: achados de correlação e escopo

Run 623, revisão sem intervenção em jogo. Fonte AUT4ProbePlugin.cs:320-382 mostra leitura dos objetos/ida-e-volta/aglomerados e solicitação de print em etapas distintas; `aplicacao` é metadado de arranque, não quadro da captura. `quadros_ate_a_ui` conta iterações internas, não é por si Time.frameCount. O JSON não associa observação/evento ao quadro efetivamente capturado.

Segunda imagem inspecionada: r3/02-final.png mostra LOADING/Difficulty Scaling e dica de tamanho da party. Não aparecem `Path Chosen!` nem marcador AUT4. O agregado `textos_visiveis` de r3 só lista `Path Chosen!`, bbox x=870.54 y=906.57 largura=178.92 altura=42.3, não a dica visível no PNG. Há prova real de componente TMP lido, mas NÃO concordância componente->pixels renderizados nem prova de visibilidade real. Interpretação upstream `só o texto renderizado desenhado` não está sustentada pela captura.

Restauração: antes.txt/depois.txt têm quatro hashes de perfil/saves iguais; antes inclui ainda Assembly-CSharp (hash conferido pelo revisor). Não são arquivos bit-a-bit iguais e o método do hash de árvores precisa ser recuperado para confirmar a força da afirmação. O script existente medir-dono.sh hasheia caminhos/tamanhos/mtime, NÃO bytes dos arquivos. Sua indicação Abyssus/Saved/SaveGames está documentada no detect-env como nome interno do jogo; não declarar caminho incorreto sem prova. Ainda verificar se a medição AUT-4 usou esse método ou hash de conteúdo.

Costura AUT-5 lida: aut5.py:622-641 lê observações cruas e não injeta sessão/hash do topo. Coletor possui costura explícita para isso. Consequência ainda a executar: entrada crua do probe pode perder procedência; entrada normalizada deve preservar metadados. AUT-6 possui adaptador separado e AUT-7 exige identidade por observação. Nenhuma assinatura de produto será fabricada: só o hash do probe foi medido no runtime isolado; não serve como hash de BetterFont/RSTV.

Próxima prova offline: consumir JSON real nas APIs existentes, registrar faltas/lacunas reais, verificar estado atual do perfil/locks e invariantes de arquivos. Não corrigir implementação durante a revisão.
