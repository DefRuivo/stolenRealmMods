# KIT-14 — run1471 — primeiro boot novo restaurado

Bancada nova scratch/kit/KIT-14-run1471/driver.py reutiliza run1442 e KIT16, adiciona somente RealmApi.dll/Core/Hooks identificados. Sem build ou edição do produto.

Seis testes de bancada executados: candidato6/6 exit0; mutante que religa recorder fez1 failure/exit1; candidato verde depois. Testes incluem remoção recursiva de instrumentos para mod sem kit, recusa de API corrompida e guards de processo/Cloud/junction/snapshot/rollback. Logs tests-mutant.log e tests-green.log.

Boot recorder-on real exit0, sessão KIT14-run1471-recorder-on-20261014-142325, PID8844. BepInEx carrega5 plugins e RSTV0.3.3 aplica15/15 ganchos; erro de dependência resolvido na bancada. RealmApi0.1.0 carregada, hooks opcionais explicitamente false.

Rota Play/Roguelike/Accept permanece Select Party; Skills esgotado3600 tentativas. Recorder1 inicializacao, passivo0. Logo carregamento PASSOU, janela/RSTV/recorder passivo NÃO provados. Não reutilizar CONCLUIDO como aceite.

Rollback leu115 dados/53 perfil/5 outro jogo iguais, PlayerPrefs export igual, jogo fechado, sem junction/backup/perfil temporário, lock liberado. Cloud OFF inicial/final sem alteração nossa; cache mtime alterou durante Steam. Próximo boot só após guard atual dentro do driver.

Próximo: coletar mesmo cenário com recorder desligado e boot básico RSTV+API sem nenhum instrumento. Sem limiares, medição exploratória, não representar idle sem eventos como custo de recorder em atividade.
