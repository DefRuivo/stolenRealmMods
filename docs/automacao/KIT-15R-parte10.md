# KIT-15R — parte 10: reprodução própria run685 e gate de correção

## Execução real

Comando python scratch/kit/KIT-15R-run685/test_resume_review.py, exit0 do coletor (NÃO aprovação do produto). Logs em scratch/kit/KIT-15R-run685/logs e verification.json. Scripts de revisão copiados byte a byte, evidências antigas intactas, sandbox535 conferida contra inventário vivo antes/depois:

LIVE_INVENTORY 535 CHANGED []
review EXIT1: Ran27 tests in15.780s; FAILED(failures=22).
extra EXIT1: Ran3 tests in0.141s; FAILED(failures=3).
author EXIT0: Ran18 tests in7.708s; OK.
control-P1-bytes EXIT1: Ran1 test; FAILED(failures=1).
P1-restored EXIT0: Ran1 test; OK.
VERIFIED: review27=22FAIL/5OK; extra3=3FAIL; ERROR0/skip0; 22 individuais e cinco controles históricos conferidos programaticamente;535 fontes vivos intactos.

O positivo P1 instala41, compara hashes individuais, remove restaurando arquivo do usuário e preserva alheio. Mutante altera bytes restaurados e produz AssertionError, não erro de setup; fonte baseline restaurado passa. Falhas F2..F10 e F12 foram reproduzidas nesta instância sem depender apenas do parecer anterior.

F1 também reconferido lendo ZIP do autor e fonte vivo: descoberta.py divergente; identidade completa em verification.json. CRC válido não prova identidade da fonte.

## Leitura direta de produto

pacote.py:216..234 confere CRC, scan e nome de manifesto, não schema/hashes/conjunto de payload. instalador.py:129..167 aceita componente ausente e recalcula hash em vez de validar declarado; :194..201 não valida schema de recibo; :309..346 copia antes do journal. scan.py:31 deixa chave JSON entre aspas passar; :79 ignora bin/obj; :89..90 ignora erro de leitura.

## Dependências operacionais

Inspecionados os três filhos. kanban_link confirmou t_d83f3ef6 KIT-15F como pai de KIT-G2 t_f19310d3, KIT-14 t_a1f38855 e KIT-G4 t_b001720d. Falta leitura posterior para verificar arestas; nenhum gate desbloqueado nem autorização alterada. Conclusão do parecer REPROVADO não libera produto. A autorização G2 registrada em09/10/2026 não é aprovação técnica deste pacote.

## Pendências do parecer

Fechar documentos e hashes por critério, conferir F11 com logs e código (zero testes não verde), checar as arestas por leitura, conservar provas e emitir KIT-15R-revisao.md uma única vez. Build/runtime/UIUX/instalação real/publicação NAO_EXERCITADO.
