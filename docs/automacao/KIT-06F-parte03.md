# KIT-06F — parte 03: F1, F2 e F3 (Python/C#)

F1 (config vazia/rejeitada nao reativa defaults):
`atalhos = dict(atalhos or atalhos_padrao())` virou `if atalhos is None:
atalhos = atalhos_padrao()` + `dict(atalhos)`. Mapa {} explicitamente vazio
permanece DESABILITADO; so None usa padroes; config recusada nao liga binding.
C# ja preservava mapa vazio (controle positivo confirmado).

F2 (contrato de acoes consistente + parar sem terminal):
- OBSERVAR virou LIGA/DESLIGA (alterna): 2o F7 DESLIGA a coleta e PAUSA o pipeline.
- RETOMAR passou a ser DESPACHADO (`retomar()` Python / `RetomarInterno` C#):
  retoma a coleta pausada e liga a observacao (senao o indicador diria "parado"
  coletando). Sem pipeline/sem pausa -> degradacao explicita, nunca no-op.
- "Parar sem terminal": o proprio toggle do F7 (o padrao nao ganha 5o atalho).

F3 (indicador = efeito; ausencia != coleta):
- Com pipeline ligado e observacao DESLIGADA o pipeline NASCE PAUSADO (Python ctor
  e C# ctor pausam), assumindo a posse da coleta: o indicador "parado" casa com
  "nao coleta".
- Sem pipeline, estado = "sem_pipeline" (degradacao explicita `coleta_sem_pipeline`),
  distinto de coleta funcional; `coleta_operante` exposto e False nesse caso.
- Iniciar observacao continua NUNCA autorizando modo ativo.

Interpretacao de contrato (sem ocultar historico): o teste do autor
`test_iniciar_duas_vezes_degrada` contradizia o topo do modulo ("liga/desliga");
foi SUBSTITUIDO por `test_f7_alterna_observacao_liga_desliga`, e
`test_pausa_delega_ao_pipeline` teve a expectativa ajustada (1a chamada = `pausar`
de posse do construtor). Nada de None/toggle foi mascarado.
