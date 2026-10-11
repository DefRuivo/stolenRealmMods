# ORG-R4-LIMPA — parte 01: exclusão nominal dos 109 caches Python e preservação do bytecode órfão

Cartão t_8dba747f (ORG-R1-E3, frente LIMPEZA). Repo C:/dev/stolen-realm, branch ci-validate-test, HEAD efafe3bdd65c42e04b934a1ea462d945bc428e4e, fotografia de 11/10/2026. Este relatório é o único arquivo versionado desta frente.

## Escopo aprovado (ORG-R1 partes 02–04)

Manifesto de evidência durável ORG-R1: 110 candidatos medidos, 3.375.997 bytes. Autorização final E1: excluir SOMENTE os 109 que têm fonte .py correspondente (3.324.108 bytes), por caminho nominal, todos sob tools/ e .github/. Preservar tools/automacao/kit10/__pycache__/_red_mutante.cpython-314.pyc, 51.889 bytes, sha256 bd7ff71d95a921608aecd92ff7232a6a5280e59e1a0a2715f165228f69513ec4, cujo _red_mutante.py não existe. Nada de `rm -rf` de árvores, nada de remover arquivo fora da lista nominal, nada de tocar em .gitignore, docs/cobertura/EV-R1, backups, lib/dist, bin/obj de probe congelado, scratch, .worktrees, nul, NuGet ou na fonte local gitignored do ReloadProbe.

## Estado encontrado na retomada (o cartão é retry)

Grande parte da exclusão já havia sido executada pela tentativa anterior DESTE MESMO cartão (execução 882, abortada por inatividade às 18:31). Medição atual contra o manifesto:

- 105 dos 109 aprovados já estavam ausentes; os diretórios __pycache__ de tools/ e .github/ têm mtime 18:17, batendo com a janela daquela execução.
- 4 aprovados ainda presentes, todos do grupo kit15: descoberta 12.584, instalador 48.430, pacote 23.587 e scan 10.005 bytes = 94.606 bytes (exatamente o grupo kit15 da tabela aprovada). Os quatro tinham sha256 IDÊNTICO ao manifesto e mtime 18:36:25, ou seja, foram reescritos por importação posterior às 18:17 e o conteúdo saiu byte a byte igual porque as fontes não mudaram. Isso confirma, por medição, que importação recria o bytecode.
- O órfão de kit10 estava presente e com hash conferido.
- `git ls-files '*.pyc'` = 0 (nenhum bytecode tracked em todo o repo).

## Exclusão executada nesta rodada

Script de bancada leu o manifesto, filtrou source_exists=true (109 itens) e, para cada caminho ainda presente no disco, revalidou ANTES de apagar: extensão .pyc, sob tools/ ou .github/, fora de subárvore proibida, fonte .py existente no momento, ausência no índice (`git ls-files --error-unmatch`) e não ser diretório. Resultado: 6 removidos individualmente com os.remove em duas passagens dentro do mesmo run — os 4 do kit15 (94.606 bytes) e, na varredura final às 18:47, 2 que reapareceram nesse meio-tempo (check_chave_compartilhada 25.545 + tabelas 15.186 = 40.731 bytes). 0 recusas, 0 diretórios removidos, 0 arquivos fora da lista.

Fechamento conferido na varredura final (18:47): 109 de 109 aprovados ausentes do disco; aprovados ainda presentes: lista vazia. Total excluído da frente: 3.324.108 bytes (135.337 nesta execução + 3.188.771 na execução anterior do cartão), verificado por interseção com o manifesto.

## Reaparecimento de caches durante a frente (medido, não conjectura)

Dois eventos de regeneração foram observados no próprio working tree enquanto a frente corria, ambos por atividade paralela (o dono edita fontes e outras frentes exercitam tools/):

- 18:36:25 — os 4 .pyc do kit15, com sha256 idêntico ao manifesto de 15:11;
- 18:45:03 — tools/__pycache__/check_chave_compartilhada.cpython-314.pyc (hash idêntico ao manifesto) e tools/__pycache__/tabelas.cpython-314.pyc (hash divergente do manifesto, compatível com fonte alterada por commit entre 15:11 e o HEAD atual).

Esses arquivos foram reexcluídos normalmente, por serem caminhos da lista nominal com fonte presente. O episódio é a demonstração empírica do mecanismo descrito abaixo: cache Python de módulo é recriado na importação, com conteúdo idêntico quando a fonte não mudou.

## Preservações conferidas

- Órfão kit10 presente, 51.889 bytes, sha256 bd7ff71d...13ec4 idêntico ao manifesto; fonte continua ausente (não foi inventado fonte).
- Arquivos NÃO listados, respeitados integralmente: tools/__pycache__/docs_proveniencia.cpython-314.pyc (6.292 bytes) e tools/automacao/kit15/__pycache__/contra_prova_kit15.cpython-314.pyc (17.776 bytes) — ambos ausentes do manifesto, portanto novos; e os 772 .pyc de scratch (a maioria em cópias de bancada do KIT), intocados porque a autorização não passa por scratch.
- `.gitignore` permanece modificado no working tree exatamente como estava ANTES desta frente (edição do dono, não reaplicada nem revertida por mim), assim como as edições do dono em tools/automacao/aut5/test_aut5.py e test_snapshot_modal.py e os quatro documentos ORG-AUT5 não versionados. Nenhum desses arquivos foi lido para escrita ou restaurado.

## Prova de ausência de sobre-remoção

O inventário físico da fotografia ORG-R1 (57.619 caminhos, 11/10 15:11) foi comparado com o disco atual. Ausências hoje: 107 caminhos, dos quais 2 dentro de .git (churn interno). Fora de .git: 105 ausências, TODAS arquivos *.pyc, TODAS pertencentes ao manifesto aprovado — e há 0 arquivos não-pyc ausentes em qualquer ponto da árvore. Nenhum arquivo extra foi removido, nem dentro dos diretórios de cache (os não-listados sobreviveram, como acima).

## Fontes: existência e hash antes/depois

Os 109 módulos aprovados mapeiam para 109 fontes .py distintas (o grupo kit15 tem 4 fontes próprias). Todas existiam antes e continuam existindo depois; sha256 de todas as 109 fontes medido antes e depois: 0 alterações. A limpeza não encostou em código — só em bytecode derivado, todos ignorados pela regra `__pycache__/` de .gitignore (linha 14, conferido com git check-ignore --no-index para amostra dos três grupos) e nenhum deles no índice.

## Bytecode é regenerável (e não é cópia única de nada)

- Bancada nova, espelho byte-exato das 109 fontes (cópia com metadados preservados) fora do repo: `py_compile` nas 109 → 109 sucessos, 0 erros, 3.514.160 bytes de .pyc produzidos.
- Os .pyc regenerados NÃO são byte-idênticos aos apagados (hash e tamanho divergem). Isso é esperado e não significa perda: o bytecode embute o co_filename e o timestamp/tamanho da fonte. Prova controlada da explicação: a mesma fonte compilada em caminho curto gerou 7.039 bytes e em caminho longo 7.078 bytes, com hash diferente.
- Os dois caches sobreviventes que ainda têm fonte (docs_proveniencia e contra_prova_kit15) têm cabeçalho timestamp batendo com tamanho e mtime atuais da fonte, isto é, não estavam obsoletos: os caches excluídos pertenciam à mesma geração e seriam válidos até a próxima importação, quando seriam recriados.
- Nada em tools/ ou .github/ importa o módulo do órfão; ninguém referencia os 109 caches por caminho (todos ignorados e não versionados).

## Testes isolados (cópia) e verificação no repo

Cópia independente da árvore versionada em efafe3b, dentro do workspace do cartão, exercitada com PYTHONDONTWRITEBYTECODE=1 para não gerar bytecode durante a limpeza. Todos os passos Python do validate.yml passaram rc=0: segredos, versoes, patches, fix_keys, dupes, notas_redundantes, chave_compartilhada --estrito, cobertura_ui_localized --prova, valida_pacotes, pack-thunderstore --listar-nomes (ramo sem DLL) e audita_docs. Contagem de .pyc na cópia após a bateria: 0 (nenhum cache criado pelos testes).

No repo do dono, com PYTHONDONTWRITEBYTECODE=1: audita_docs rc=0, "nenhuma inconsistencia encontrada"; `git status --short` idêntico antes e depois; nenhum .pyc novo criado. Não foi feito build, deploy, pacote, push nem execução do jogo. Ressalva registrada: a cópia tem 98 fontes em CRLF e 2 arquivos aut5 sem as edições do dono (divergência só de fim de linha/edição paralela, sem efeito nos instrumentos); a divergência de conteúdo foi conferida e restrita a esses 2 arquivos.

## Risco residual: cache volta

Na janela entre a exclusão anterior (18:17) e a retomada, o grupo kit15 reapareceu (18:36) e, durante a própria frente, mais dois caches de tools/ (18:45) — ambos por importação de processos paralelos. Isso é comportamento esperado, não falha: cache Python é derivado e se recria na primeira importação. A frente E2 (movimento de test-cycle) e o dono podem regenerar caches a qualquer momento; a limpeza vale como saneamento do working tree na fotografia descrita, não como estado permanente, e não deve ser reexecutada por varredura automática de *.pyc.

## Limites respeitados

Sem `rm -rf`, sem remoção por árvore, sem tocar em arquivo fora da lista nominal, sem editar .gitignore, sem desindexar (0 tracked), sem deploy, sem push, sem rodar o jogo, sem execute_code. Um único commit, stage nominal apenas deste arquivo; nenhum `git add -A` e nenhum `git commit -a`. Handoff para a política final (t_6b569699) e o gate R4 (t_c00ce910).
