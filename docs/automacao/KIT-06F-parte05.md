# KIT-06F — parte 05: F6, F7 e F8

F6 (integridade da evidencia):
- Python `atualizar_contexto(janela=None)` agora LIMPA a janela (sentinela
  `_SEM_VALOR` distingue omitir de limpar); contrato explicado.
- C# `Marcacoes()/Degradacoes()/Eventos()` devolvem COPIA PROFUNDA (`CopiaValor`
  recursivo, dicionarios aninhados) e `DocumentoExport` usa essas copias.
  `LimparJanela()` da paridade ao Python. Alterar o snapshot externo NAO muda
  mais a evidencia interna.
- CORRECAO KIT-06F (ver parte07): o bloco `coleta` reusa o pipeline e ate aqui
  entrava por REFERENCIA (os acessores do pipeline devolvem copia RASA). O
  snapshot defensivo agora e PROFUNDO tambem nesse caminho aninhado, nos dois
  lados (Python `_copia_profunda`; C# `CopiaValor` em `ColetaDocumento`). A
  afirmacao de que "DocumentoExport usa essas copias" passou a valer para
  `coleta` — antes valia so para `marcacoes`/`degradacoes`/`trilha`.

F7 (falso verde do harness): Program.cs reescrito. Cada verificacao tem ID
ESTAVEL; `Defeitos` declara o CONJUNTO EXATO de IDs que devem falhar por defeito
("guard" = 3 IDs de guard_chat; "ataque" = 2 IDs de config). Verde SO com conjunto
identico; nome nao suportado -> exit2; falha extra/ausente -> exit1. Prova
antes/depois com o MESMO defeito real (ConsomeInput false->true):
- ANTES (oraculo fraco): normal exit1(2 FALHA); --defeito guard exit0 FALSO VERDE;
  --defeito inventado exit0 FALSO VERDE.
- DEPOIS: normal exit1 apontando guard_sem_foco.sem_consumo_input; --defeito guard
  exit1 (falha EXTRA recusada); --defeito inventado exit2.
Testes NAO afrouxados: a checagem mudou de "alguma falha" para "conjunto exato".

F8 (contrato KIT-07 honesto): `contrato_kit07()` deixa de afirmar
NAO_IMPLEMENTADO (a API montar_pacote existe) e declara
`status_kit07=GATE_NAO_SATISFEITO`, `api_kit07_existe=True`,
`integracao_efetiva=False`, `export_bruto_local=True`, `pacote_compartilhavel=False`
e o motivo (KIT-07R REPROVADO; KIT-07F em correcao). Nao se integra exportador
reprovado nem se duplica sanitizacao; fluxo basico sem Hermes/IA/terminal.
