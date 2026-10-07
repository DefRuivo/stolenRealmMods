# AUT5-F1 — reentrega R1/R2 apos revisao independente

Rodada OFFLINE de 2026-10-05. Este adendo substitui a prova de alvo do snapshot e a
interpretacao `cons is None == janela nao aberta` da primeira entrega em
`docs/automacao/AUT5-F1-entrega.md`. Os campos e formatos da primeira entrega
permanecem; nenhum criterio runtime foi aprovado.

## R1 — alvo efetivo e identidade do par antes/depois

`IniciarSnapshotDoModal()` captura, por reflexao, a referencia de
`RoguelikeSkillTreeVisualizer.ReadOnlySession.Target` somente quando `Active=true`.
A maquina de estados chama esse metodo no inicio de F_LEITURA. Tanto
`SnapshotDoPersonagem()` quanto `AtualizarGuardasDepois()` usam essa mesma referencia.
O fechamento da sessao (Target=null), troca do selecionado global ou abertura de
outra sessao nao trocam o personagem do par. Nao ha fallback ao selecionado.

Sem sessao ativa ou sem Target no inicio da leitura, os membros personagem/skills/pontos
saem null e o criterio fica NAO_EXERCITADO. Isso nao e um ciclo runtime concluido:
a rodada futura precisa observar o alvo efetivo com a sessao aberta no inicio da
leitura. Nao se captura tardiamente um alvo novo para inventar um "antes".
`personagem_esperado` continua pertencendo ao plano/dono, sem preenchimento automatico.

Prova executavel incorporada a `test_aut5.py`: `test_snapshot_modal.py` extrai e
executa os corpos reais de oito metodos C# sem alterar seus corpos; doubles apenas
nas dependencias Unity/jogo. O double de ReadOnlySession usa propriedades internas,
como o produto. O harness testa selecionado null, selecionado B com modal A e
selecionado igual a A; nos tres casos A passa de 3 para 1 ponto, fecha a sessao e
abre outra de B. O snapshot permanece A/1 apos fechamento e troca; o avaliador
reprova o gasto. Sessao inativa e Target null produzem NAO_EXERCITADO, nao OK.
Essa prova e OFFLINE, nao leitura em jogo nem evidencia vinculante de runtime.

## R2 — marcador faltante nao vira autorizacao

O condutor distingue falta de exercicio de falta de instrumentacao. Existindo
qualquer lado do confronto, geometria da arvore ou abertura da janela, a falta
de RSTV-24b e/ou RSTV-25 gera REPROVADO, tipo_pendencia=tecnica, com a lista dos
marcadores ausentes. A decisao os encaminha a falhas_automaticas, nao ao dono.
Sem qualquer sinal de abertura/renderizacao nem lados do confronto, continua
NAO_EXERCITADO/autorizacao. O leitor log_rstv.py nao precisou mudar nesta reentrega:
seu None significa falta de um ou dos dois lados, nao falta de exercicio.

Controles adicionados a suite: remover completamente RSTV-24b, remover completamente
RSTV-25, remover ambos mantendo janela aberta, remover um tier inteiro. Todos
reprovam. Log sem janela continua NAO_EXERCITADO; log anterior sem "por tier"
continua INDETERMINADO/tecnica, nunca OK. Campos ausentes e explicitamente null
nos tres criterios de snapshot/tooltip/geometria continuam NAO_EXERCITADO.

## Execucao real e contra-provas

- test_aut5.py: PASSOU, 10 grupos de caso, exit 0.
- test_aut5.py --contra-prova: PASSOU, exit 0.
- roda_testes_runtime.py: VERDE, 8 testes offline, exit 0.
- cenarios/test_rstv.py: PASSOU, exit 0.
- tools/testes/roda_testes.py: VERDE, 86 testes, exit 0.
- Dois builds em copia isolada no workspace: probe e mod, ambos com
  -p:DeployToBepInEx=false, exit 0 e zero erros. Cada build tem um aviso MSB3277
  de conflito System.Net.Http; nao foi escondido nem tratado fora do escopo.
- Duas mutacoes apenas em memoria/copia: snapshot lendo CurrentlySelectedCharacter
  e ramo de marcador faltante neutralizado. Harness/suite rejeitaram ambas.
  Nenhum fonte vivo precisou ser restaurado.
- Log real do dono, somente leitura: 6 OK offline, 11 NAO_EXERCITADO, exit 2.
- Fixture completa: 7 OK offline, 2 INDETERMINADO, 8 NAO_EXERCITADO, exit 2.
- Zero criterios runtime aprovados em ambos os relatorios.

Saidas, snapshots e hashes em `rework-evidence.json`, `rework-execucoes.json`,
`rework-testes.txt`, `rework-build-probe.txt`, `rework-build-mod.txt`,
`rework-rel-real.json` e `rework-rel-fixture.json`, no workspace da tarefa.
Reproduzir a verificacao adicional: `python verify_f1_rework.py` no workspace.
Ela faz dois builds isolados e rejeita as duas mutacoes; a suite cotidiana executa
somente o harness C# offline, nao compila/instala o plugin no jogo.

## Hashes desta reentrega (sha256)

- AUT4ProbePlugin.cs: afa4ee6daf6270b54ebf2651c55dd06c7c6717eff8c5787bf2c04ef38588073a
- aut5.py: 6e5e53eb6c50333f839387a8c0425c06ec111402a9a24cb3e9165698ffc8431c
- test_aut5.py: 1b42c8aab126c19894720e726290c35b62004dcaa503c45ff7f81a78e5572dc2
- test_snapshot_modal.py: 054aecb14eb53700d3f0aa28d9b51e221c82e4f93a972d5a36f15bafcb4c3e96
- Probe DLL da copia isolada: 577448a2d7ee440333d78260bb5dd815f433584a2729ea32833988558d273e84
- Mod DLL da copia isolada: 9fdbe0a18315fec387936c1c627e481293ab5f28257ffce314bd0f8099d00ac6

Conferidos intactos durante a verificacao:
- coletor.py: 0518634edaa70930a8f8173151d84aee8c20a5523fcffd9ad5842b6d5ff1faca
- SkillTreesTab.cs: 09debb76cec83c6341a177268add820dbca5bbeb5bf44c101c55619b6f179b9f
- DLL do mod no repo: 454587a031a3e89104ec8535cf4c6328e2a527238138a136adcc773c5617a948

## Limites e handoff

Nenhum jogo iniciado/encerrado, nenhum save carregado, nenhum probe instalado,
nenhum deploy/publicacao/commit. Build do probe e do mod apenas no workspace,
sem atualizar DLL do repo/perfil. Emissao provada offline; leitura em jogo ainda
requer autorizacao. A reentrega precisa de nova revisao independente.

hotspot: tools/automacao/aut5/aut5.py e test_aut5.py — AUT5-F2 t_9cee7d21 depende
desta tarefa e deve partir destes hashes apos aprovacao; suas guardas, falhas do
produto e motivos permanecem fora desta reentrega. CIC-5 permanece dono dos
bloqueadores do coletor. Nao foi criada nova tarefa nem executado o filho AUT5-F2.
