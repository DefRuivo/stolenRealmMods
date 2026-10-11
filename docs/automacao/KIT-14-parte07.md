# KIT-14 — run699: preflight exercitado e sandbox preservada

## Execução real

`python scratch/kit/KIT-14-run699/preparar.py` — terminal exit 0, 10/10/2026 13:09:41 -03.

- git ls-files tracked: 874; untracked: 470; cópia: 1343 arquivos, com SHA fonte/cópia reconferidos.
- Única exclusão: arquivo preexistente `nul`, nome de dispositivo que já impediu rg. Não alterado.
- .git/remote/credenciais não copiados; `no_git=true` verificado por existência.
- Referências DLL locais copiadas para lib da sandbox; não são payload redistribuível nem evidência a empacotar.
- Snapshot somente leitura das árvores pessoais: BepInEx 53 arquivos; LocalLow do jogo 111; Abyssus 5. Hashes/path maps em personal-before.json, sem imprimir conteúdos.
- Guarda real `check_deploy_optin.py --raiz <sandbox> --json`: exit 0, alvos_de_deploy=6, sem_optin=[]. Build agora permitido apenas nessa cópia, com flag false e ambiente/propriedades redirecionados.
- Busca UTF-8 dirigida registrou somente comentários de persistentDataPath nos helpers examinados; escopo e resultados em baseline.json. Não é busca universal.

## Evidência durável

scratch/kit/KIT-14-run699/preparar.py; baseline.json; personal-before.json; prepare-result.json; deploy-preflight.stdout.json; deploy-preflight.stderr.log. O resultado será confrontado novamente no fechamento, com hashes reais.

## Isolamento runtime ainda insuficiente

Decompilação dirigida GlobalSaveDataManager (terminal exit0) confirmou Filename=Path.Combine(FileSystem.persistentDataPath, "GlobalSaveData.json"). Não existe prova nesta rodada de que a instância do jogo leria área descartável. Copiar saves ou BepInEx e verificar hash após boot não fornece a prevenção exigida pelo KIT-G2.

`hermes profile list` executado somente para descobrir assignee de eventual seguimento: apenas default listado. Não foi criado seguimento nem atribuída correção ao próprio autor.

Próximo bloco: builds identificadas, pacote e lifecycle OFFLINE reusando os CLIs entregues, controle negativo do pacote e comparação pós-rodada dos hashes. Runtime e performance permanecem NAO_EXERCITADO; nenhuma publicação, alteração de gameplay ou save pessoal.
