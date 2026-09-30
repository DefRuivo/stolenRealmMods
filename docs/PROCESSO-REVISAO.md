# Processo de revisão (padrão do projeto)

**Regra:** toda tarefa executada neste projeto gera uma tarefa de **revisão independente**.
A revisão é o portão de qualidade **antes** de qualquer validação ou aprovação humana.
Nenhuma entrega vai para o dono (nem para a Thunderstore) sem passar por ela.

## Por que

O projeto já pagou caro por defeito que "compilou e parecia certo": um patch Harmony com
parâmetro por índice travou o jogo em batalha (112 exceções por frame), um DLL velho foi
empacotado para publicação, um relatório passou a afirmar o contrário do código, e um número
correto foi exibido com o rótulo errado. Nenhum desses foi pego pelo autor da mudança —
todos foram pegos por **outro olhar**, com prova.

## Quem revisa

**Nunca o autor.** A revisão é feita por um agente diferente, que recebe o estado final
(commit, arquivos, saída das ferramentas) e não participa da implementação. Aperfeiçoar a
própria entrega não é revisão — é continuação do mesmo trabalho.

## O que a revisão precisa entregar

1. **Veredito explícito por item**: OK (com a prova) / ACHADO (com o que está errado, onde e o
   que deveria ser) / INDETERMINADO (com o dado que falta para decidir).
2. **Prova, não opinião**: arquivo + linha, saída literal de ferramenta, offset de asset,
   resultado de decompilação. Releitura do relatório de quem executou **não** é prova.
3. **As travas rodadas**: build (0 erros), `check_dupes`, `check_chave_compartilhada --estrito`,
   `check_notas_redundantes`, `check_segredos`, `check_versoes`, `valida_pacotes`, `audita_docs`
   — as que fizerem sentido para a área.
4. **Invariantes do projeto conferidos** conforme a área: mods não se acoplam; assinatura Harmony
   por TIPO e parâmetro por NOME (nunca por índice); try/catch e falha-segura; nunca bloquear
   método de fechamento; nada de Bard/música; os ajustes manuais do dono preservados; uma entrada
   por texto nas tabelas.
5. **Contra-prova quando a entrega é uma trava**: injetar o defeito que ela deveria pegar, ver
   ela falhar, reverter e ver ela passar.
6. **O que a revisão NÃO consegue confirmar**: listar o que só se resolve em jogo (olho humano),
   em vez de dar como verificado.

## Depois da revisão

- **ACHADO** volta como tarefa de conserto (com o achado e a prova); o conserto passa por nova
  revisão do mesmo item antes de fechar.
- **OK** libera a validação humana quando ela for necessária (visual, em jogo, decisão de dono).
- A revisão **não** publica, não aprova deployment e não faz push — ela informa a decisão.

## Formato da tarefa de revisão

Título: `REV-<n>: revisar <o que foi entregue>`
Corpo: o que foi entregue (arquivos/commits) · o veredito esperado por item · as provas
exigidas · as travas a rodar · o que é só olho humano.
