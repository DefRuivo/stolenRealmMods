# KIT-14F3 — iteração diagnóstica run1519

Sandbox nova: scratch/kit/KIT-14F3-run1519; inventário baseline SHA256 d48790cc9af03f82f2df25390f4a202535be99a8de2b86517e57c681b66d8a88. Sandbox run1502 e detector preservados. Adicionados somente contadores de observações/janelas e diagnóstico ponte habilitada/transições/mesmo pipeline para distinguir barreiras; nenhum evento fabricado.

Preflight leu jogo fechado, Cloud app0, nenhum lock/junction/backup. Driver expandido lido: checa processo antes de isolar e imediatamente antes de lançar, preserva provas, fecha somente PID próprio com CloseMainWindow, restaura dados/PlayerPrefs e compara hashes antes de liberar lock. Boot novo ainda não é aceite.

Build diagnóstico real: preflight deploy negativo1/positivo0, candidato0 e mutante0, com DeployToBepInEx=false. Adapter candidato2c2cda4135b5b5d648bc165d33d4228150ec24075e84d8e7cefa2e7de5c831c8; mutante9a469e44ce065eb8ca6431e4f724967ee86e3577ebc6f3ff329414371e4e362e. Core/probe/RSTV continuarão congelados. Novos testes permanecem sem inferir clique físico.
