# 0.1.0

Primeira versão publicada.

- **Botão "Skills" na tela Select Party** do modo Roguelike, quadrado e ao lado direito do *Choose Powerups*, na mesma linha — a linha não cresce e o *Accept Party* não muda de tamanho.
- **Abre a Skill Tree NATIVA** do jogo (a mesma de *Campaign → Change Skills*) com o contexto **real** do personagem: nível, equipamento, atributos e estado das skills.
- **Modo somente leitura**: os nós podem ser inspecionados (tooltips com os números do personagem certo, troca de abas, zoom), mas nada é aprendido ou removido. O clique no nó é bloqueado e o botão de respec fica escondido.
- Alvo do botão é o **último personagem que você adicionou** à party, resolvido no clique — cada jogador usa os seus.
- O jogo **não** tem um modo somente leitura nativo; a garantia vem de higienizar o ponto de gravação antes que ele execute, e não de bloqueá-lo.
