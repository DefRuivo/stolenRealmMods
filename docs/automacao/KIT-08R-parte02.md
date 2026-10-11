# KIT-08R — parte 02: identidade e hipóteses dirigidas

C1 PASSOU (identidade inicial). Sandbox própria C:/dev/stolen-realm/scratch/kit/KIT-08R-run648/sandbox; cópia de 27 arquivos Python/JSON/shell de KIT-08 e dependências cenarios/aut3, tracked e untracked preservados byte a byte, sem .git/remotes/perfil/credenciais nem assemblies do jogo. Terminal Python exit 0, NO_GIT=True. Inventário completo em scratch/kit/KIT-08R-run648/identity-before.json.

SHA256 vivo e copiado, conferindo com entrega:
- visualizador.py: 3d6d2983a845d1423859ef75f7f8e658cde7c14c0d4fe3ee23194d08a9789701
- teste_visualizador_kit08.py: 840f62e9da178ea6c21af5f8a37e0fc0022b14999832bbfbc3395d5dfe079e7e
- contra_prova_kit08.py: 9555233e989e76e691b42d3977063ab9399623f0593110294d3076476c876551
- roda_testes_kit08.sh: 37de9d8de93f65b74eaf2df6296a63e9298a557479b78d3a08b4e3a1407db394
- avaliador vivo KIT-09: 55f01e024e5e5ffd0c28b98ef492e2790c606d57d1dab4ae9d0258fba05feabb

Código inteiro dirigido lido (visualizador 565 linhas, suíte 220, contra-prova 144, runner 49). Há hipóteses que exigem prova antes de virar achado:
1. referencia_local_segura não resolve URL percent-encoded (`%2e%2e/`), separadores/drive codificados nem verifica confinamento/existência do arquivo.
2. comparação ignora origem_sintetica do documento, usa estado cru para regressão, e caso ausente/identidade parcial pode parecer OK.
3. aprovacao_stale considera somente hashes presentes no registro; qualquer dict sem hashes aparece VIGENTE.
4. veredito_tecnico usa bool(prova_runtime), aceita string `false`; identidade de critério não confrontada com documento vivo.
5. CLI avalia antes de --identidade; retorno não leva em conta comparação recusada/FALHOU; campos sessao string são descartados na renderização.
6. Referências de imagens são relativas ao HTML de saída, não ao input; não há cópia/embedding da imagem. Rótulo autocontido pode não corresponder ao efeito.

Esses pontos ainda INDETERMINADOS até execução independente. Nenhum produto editado. Runtime/browser/pixels NAO_EXERCITADO; não se converterá fixture em comprovação em jogo.
