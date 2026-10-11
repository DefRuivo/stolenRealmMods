# KIT-12R — parte 03: reprodução independente e identidade medida

## Identidade PASSOU/OK
Comando real terminal Python: copiar tools com tracked/untracked (excluindo caches/bin/obj/.git/.env/chaves), copiar apenas envelope JSON de referência, git init local e git remote -v. Exit 0; remote vazio. Sandbox: C:/dev/stolen-realm/scratch/kit/KIT-12R-run674/sandbox. Inventário 523 arquivos em baseline.json; identidade dos quatro produtos em identity.json. Todos os quatro SHA256 medidos conferem com KIT-12G-entrega.md:

- integracao.py: 7785d8c1f624ff263b4ac89ad36e3ab9952db17d5a233d12affada091da8af87
- pertinencia.json: b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320
- prove_ciclo.py: 4fc01b81572bdfbbea4cc3af33f1fb845659f23bc689cc94068e2d85b973b750
- test_kit12_integracao.py: 25284c7075633042efc6445a5856d5a24e40d152ccdb593d6cb94d661e96da8c

Envelope copiado: 5bef1c67e21365ccf84d02ff645715e254a4e1140aec77d62c6b12de689a158d. Não copiado perfil nem DLL proprietária. Binários usados pela demonstração são bytes FIXTURE declarados, não assemblies compilados.

## Suite e controles do autor reproduzidos PASSOU
Terminal subprocess com cwd sandbox, BH_AGENT_WORKSPACE exclusivo test-area, LOCALAPPDATA exclusivo localapp e PYTHONDONTWRITEBYTECODE=1:

1. `python sandbox/tools/automacao/kit12/test_kit12_integracao.py`: exit 0, `Ran 30 tests in 12.530s`, `OK`. Log suite.txt.
2. Mesmo comando `--isca`: exit 0, `mutacoes_discriminadas=14/14|falhas=0`, cada mutante exit 1, controle restaurado exit 0. Log isca.txt.
3. `python sandbox/tools/automacao/kit12/prove_ciclo.py --out .../cli`: exit 0, `PROVA|PASSOU`. Etapas efetivas: 2->1->2->2->2->2->3 (últimas etapas registram incoerente antes de hash-dos-fontes). Log cli.txt, efeitos cli/prova.json e resultados intermediários. executions.json registra argv e exits reais.

C5 PASSOU nos caminhos exercitados; fixture nunca prova runtime. C1–C4 têm evidência parcial de reprodução, ainda exigem sondas próprias, incluindo indisponibilidade de dependências/config/probe, formato inválido e fila. Nenhum produto foi editado.

## Inspeção dirigida adicional
Lidos integracao.py 315–479, 445–674, 674–783, 790–1277 e testes 200–434. Pontos a refutar: configs_ausentes apenas metadata; relatório ausente pode não alterar estado; verificação guarda identidade mas não reconfirma decisão. Não transformar hipóteses em achados sem execução.

NAO_EXERCITADO continua: jogo/runtime/build/preflight/deploy/save/perfil/publicação/UIUX/humano. Provas externas de outros agentes NÃO foram tomadas como execução própria.
