# KIT-07R — parte 03: inventário vivo e obstáculo do launcher

Executado `python scratch/kit/KIT-07R-run636/setup_review.py` (duas tentativas, exit 1). Cópia de 11 arquivos vivos conferida byte a byte em scratch/kit/KIT-07R-run636/isolated, sem .git. Identidades em identity-before.json e baseline tools em tools-before.json.

Hashes confirmados iguais ao handoff do implementador:
- exportador.py: c5fc715b083685ec209138d0dc56e0f9dc19abcabd9e430493746d6f2a625382
- teste_exportador_kit07.py: 2dc7ea39e0834041f7176969aced4c58a19be200e4c84137289b895f65fb4f51
- contra_prova_kit07.py: e4cc31d4a46e224c1287f66ea5dad8ef131d41d24353b3b9ea1a97310605272e
- roda_testes_kit07.sh: 26ceff5dcdbeae4715052741f8bce02a48724a952acdb04a85b1ad5a6fd5f17d
- aut3_lib.py (dependência): 04f37b8e285ad7d429d0d01cd846523323ca0a403ce64203890e3c0538d6dc1a
- KIT-07-entrega.md: 3991d8aa9e86c550600c3f008d1d4d2e10affadc9a70231c98a40dc52b099d58

## Runner — NAO_EXERCITADO até aqui
O subprocesso `bash` lançado pelo Python encontrou /bin/bash que não resolveu o caminho Windows (exit 127), tanto com separador nativo quanto com slash. Não é defeito do produto comprovado. Abordagem muda: runner invocado diretamente no terminal hospedeiro com cwd na sandbox e caminhos relativos; execução Python própria não invocará bash.

Suite/contra-prova ainda não verdes. Somente script de revisão alterado (uma troca de path separator); nenhuma fonte do produto alterada. Copiados apenas arquivos do escopo e dependências/scanners, não o repositório inteiro, sem .git remoto/perfil/credenciais.
