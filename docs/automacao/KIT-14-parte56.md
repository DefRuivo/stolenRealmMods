# KIT-14 — run1442, checkpoint 56

Bancada identificada preparada SEM BOOT em scratch/kit/KIT-14-run1442/inputs. Driver novo reutiliza o driver expandido run911 e suas funções de snapshot; usa R2 seguro do pacote já auditado, não a fonte antiga principal. Sem builds ou promoção de produto.

Identidades medidas:
- AUT4Probe DLL: 1cacad9269927ec9a802691ab477abad055b2a779cda44331770af0338ad7879; fonte: 547d10ec2a07f98718f742ee037930c474c6cae42fc22c871e955ffe056c695e.
- Core DLL: 0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d; fonte: 192e463675e2056f3476df2bd3f094e4795e67a130c4392c973c63619b282c59.
- Adapter DLL: d1b383c6cfeae198e77f96047ead39c1a54678f24888c110fed60a9561dded50.
- RSTV DLL existente: 1d0b85e8d0f30d10c4fe7c4e044d30380537e8801a7d39875192459a2e51d5cc. Correspondência dessa DLL com fontes atuais não afirmada: nenhum rebuild. Identidade carregada ainda não medida.

Teste real do driver: 7 tests, exit 0 (tests-green.log). Inclui fixture NTFS descartável, com preparar/fixture/restaurar efetivos; guarda de jogo aberto recusou preparação, exit 3. Mutante do comparador: 2 tests, 2 failures, exit 1 (tests-mutant.log), provando detecção de reescrita mesmo tamanho e adição/remoção. Fixture não é runtime.

Rota pretendida: dados vazios/quarentena pessoal -> Play;Roguelike;Accept -> botão RstvRunSkillTreeButton, via handler, EsperarInteractable=true e gate adicional=true/10 frames. Não prova clique físico. Driver retém logs/config/recorder antes do rollback, recusa restaurar com jogo vivo e confirma PlayerPrefs/dados/perfil após restauração.

Nenhum boot até este checkpoint. Bloqueio histórico por autorização não será repetido; rechecagem de processo/frente/Cloud ocorre dentro do próprio driver antes do lançamento. Preflight de deploy/build não aplicável: nenhuma build executada, apenas cópias identificadas para perfil temporário.
