# KIT-14 — checkpoint 50, run1014

## Dependências atualizadas e escopo residual
- t_f067088e DONE por run1010: implementação OFFLINE R2 corrigiu os dois achados da revisão R1, mas não promoveu ao principal, não executou runtime e explicitamente exige NOVA autorização de boots. A conclusão não é parecer independente R2 nem eliminação comprovada do crash nativo.
- t_a41dd22d DONE/revisado por run912: somente livro geral com 1 inicializacao confirmado. Passivo zero; não qualifica RSTV/Runner/performance.
- t_9ce7d260 TODO: revisão final KIT-14 existente permanece dependente, sem duplicação/liberação indevida.
- Lida entrega run916 e checkpoint48: não repetir prova upstream911 já conferida; concentrar verificação offline no pacote R2 recém-entregue.

## Evidência real desta retomada
Terminal exit0; data local 2026-10-12T21:08:04-03:00.
Pacote R2 anexado: SHA256 a4511b9a9f38ecbd273d904627851e206fe8483fd1a2586685339d3063f04d9d; 197316 bytes; 46 entradas; testzip=null (CRC íntegro). Extração própria, caminho novo: scratch/kit/KIT-14-run1014/upstream-r2. Extração validou ausência de caminhos absolutos e traversal; não executou scripts do pacote.

Hashes medidos diretamente:
- Probe principal: beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193, 109397 bytes.
- Probe R2 no clone: 547d10ec2a07f98718f742ee037930c474c6cae42fc22c871e955ffe056c695e, 113942 bytes.
- Core principal fonte: 192e463675e2056f3476df2bd3f094e4795e67a130c4392c973c63619b282c59.
- Core principal DLL: 0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d, 34304 bytes.

## Próximo bloco autorizado
Conferir todos os membros selados; ler regressões/manifesto e executar harness OFFLINE em cópia própria (saídas sob scratch/kit/KIT-14-run1014). Nenhum build antes de preflight, nenhuma promoção cega de hotspot, nenhum boot sem orçamento explícito. Relatar separadamente o verde offline, a integração ausente e os critérios runtime não exercitados. Limiares continuam dispensados (B), sem pedido repetido de consentimento genérico.
