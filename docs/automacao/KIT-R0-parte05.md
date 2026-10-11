# KIT-R0 — checkpoint 05: replay CLI e contra-provas concluídos

Execução própria: `python scratch/kit/KIT-R0-run623/review_evidence.py`, exit 0. Script e saídas reais preservados em scratch/kit/KIT-R0-run623. Cópia explícita da DLL existente e Assembly-CSharp para sandbox supriu o pré-requisito ignorado pelo git; nenhum build/deploy.

Resultados medidos:
- suite-with-dll.log: 15/15 PASSOU, runner exit 0, zero exceção inesperada.
- contra-with-dll.log: 31/31 iscas reprovam por asserção esperada, runner exit 0, zero exceção inesperada. Primeiros logs vermelhos foram mantidos, não substituídos.
- detector-replay-r2: INCOMPLETO/exit 1, lacunas texto_bruto/texto_renderizado.
- detector-replay-r3 e r4: CONFIRMADA/exit 0, mas explicitamente sem expectativa declarada.
- expected-component: sobre o JSON real original r3, esperado independente `TextMeshProUGUI` casa, CONFIRMADA/exit 0.
- wrong-component: mesmo JSON real imutável, expectativa impossível distinta, NO/exit 1. Isto é contra-prova offline do avaliador sobre dado real, NÃO rodada em jogo com probe ausente.

round-audit.json registra três sessões distintas, identidade da DLL igual ao disco, hash do JSON igual ao manifest do driver e marcador de ida-e-volta igual ao cfg/driver em todas. 24 observações por sessão, mas apenas 1 ativa; não extrapolar 24 objetos para 24 textos renderizados.

Quatro PNG preservados, todos 1920x1080 com CRC de chunks válido, tamanho e SHA256 concordantes com manifest do probe. R2/r4 sem 02-final.png preservado; R3 com os dois. R4 imagem inspecionada = LOADING/Potions, marcador ausente. `textos_visiveis` do JSON registra `Path Chosen!`, embora imagem mostre LOADING: associação visual/oclusão/quadro requer análise, não afirmar simultaneidade.

Todos `aplicacao.roteiro_frame` são 0; a espera registra 315/319/309 ticks, e marcos posteriores registram tempo em segundos, não frame da captura. Ainda sem correlação exata evento->quadro PNG.

Rollback do driver r2-r4: limpo=true, resíduos/divergentes/faltando/dirs_residuo vazios; encerramento gracioso apenas dos PIDs novos 27588/33484/23996. R3/r4 `resultado.status` é CONCLUIDO, enquanto consolidado/detector é CONFIRMADA: distinção que a tabela upstream simplifica.

Filhos existentes inspecionados: KIT-05 t_e9e569f8 e KIT-11 t_f2129aea. Não há filho pré-criado de revisão deste cartão. Ambos exigem uma base segura; não liberar com aprovação implícita se houver achado bloqueante. Revisão continua na costura dos avaliadores e na restauração atual.
