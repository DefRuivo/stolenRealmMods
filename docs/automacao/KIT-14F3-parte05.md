# KIT-14F3 — primeiro boot: mutante real, sem produtor

Campanha mutant executada exit0 (isto significa somente execução/restauração, NÃO gate verde). Sessão KIT14F3-run1502-mutant-20261015-130325. Adapter mutante cecf56e2aa0cccf9ca70cf951a83f0965f96e7f005d7b9913a58108d5c522683.

Runtime medido: 717 callbacks PlayerLoop, zero duplicações; Update do plugin0, OnDestroy1 no frame0, Unity-null=true/CLR-null=false tanto plugin quanto Core, observador continuou depois da destruição. Motor removido ao sair, contagem final0. Isto demonstra a hipótese de lifecycle e a necessidade do guarda CLR. Mutante não observou nem registrou: eventos_produzidos0, inicializacao1, passivo.eventos_total0, capturas0, apesar de party1/HUD e handler exato uma vez no frame485. PNGs reais do probe existem, portanto tela aberta sozinha não demonstra produtor.

Restauração lida: hashes IMEDIATOS production115/profile53/other-game5 iguais; PlayerPrefs exportados iguais; jogo fechado, sem junction/backup/perfil isolado, lock liberado; Cloud off preservada. Logs em cases/mutant/boot01/preserved, diagnóstico em preserved/recorder. 73 avisos/0 erros no build candidato (nulabilidade legada e nova), não declarar build sem warnings.

Detector estrito novo detect.py mede evento/frame/janela/PNG/sessão e será rodado primeiro sobre este mutante, depois sem alteração sobre o candidato. Não substitui nem enfraquece full-rstv.
