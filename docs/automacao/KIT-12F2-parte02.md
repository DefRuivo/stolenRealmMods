# KIT-12F2 — o que mudou no produto (parte 02)

Produto alterado: **apenas** `tools/automacao/kit12/integracao.py`.
- Baseline (run674): `7785d8c1f624ff263b4ac89ad36e3ab9952db17d5a233d12affada091da8af87`
- Corrigido: `480a9a02b7a2f13bb51d4bce32c29897ff944cfca00fd6431a924877a44da25c`

Nenhum mod, dado de jogo, politica, `Assembly-CSharp.dll`, Bard/gameplay ou trava foi tocado.
`test_kit12_integracao.py` e `prove_ciclo.py` permanecem byte a byte.

## F1R — config explicitamente solicitada ausente nunca aprova

`criterios_da_cadeia`, bloco (2d): para cada entrada de `ident["configs_ausentes"]` (so existe
quando a rodada PEDIU a config em `configs` e a medicao falhou) e criada a lacuna nomeada

    cadeia/config-ausente/<rel>  (estado NAO_EXERCITADO, tipo_pendencia coleta_tecnica)

e todos os OK sao rebaixados (`rebaixar_ok`). Efeito: INCOMPLETO/exit2 com lacuna que volta ao
AGENTE. Config nao fornecida (`configs=[]`) continua opcional — nao vira dependencia obrigatoria.

## F3R — instrumento solicitado ilegivel nao cai em fallback

`identidade_cadeia` ja marcava `dll_probe_sha_origem="probe-ilegivel"` quando `--probe-dll` era
pedido e os bytes nao podiam ser medidos, mas o confronto seguia para o alias `dll_sha` e aprovava.
Bloco (2e): quando a origem medida e `probe-ilegivel`, cria a lacuna

    cadeia/instrumento-probe-ilegivel  (NAO_EXERCITADO)

e rebaixa os OK — sem fallback silencioso. Instrumento apenas DECLARADO (sem `--probe-dll`)
continua o limite declarado permitido; instrumento MEDIDO coerente segue positivo; divergente
segue rebaixando (comportamento anterior preservado).

## F4R — coleta malformada vira causa tecnica, nunca traceback

Nova `_validar_observacoes(doc)` substitui a iteracao direta. `observacoes` ausente/nulo/tipo
nao-lista lista-com-elementos-invalidos produzem CAUSA tecnica em `coleta.erro` (ex.:
`envelope com 'observacoes' do tipo int (esperado: lista de objetos): entrada INVALIDA de
instrumento, nao defeito de produto`). Isso alimenta `rebaixar_ok` ("coleta invalida") e a CLI
emite resultado ESTRUTURADO com INCOMPLETO/exit2 — sem `TypeError`, sem exit1, sem zero verde.
Formatos legitimamente aceitos (lista de objetos, ou lista top-level) seguem inalterados.

## F5R — saneamento alcanca TODOS os criterios

`montar_fila` ganhou um segundo laco apos o laco por item: para todo criterio que NAO gerou item
de fila (ex.: OK valido), os campos executaveis sao removidos do criterio e a proposta fica
registrada em `criterio["propostas_nao_executadas"]` (local explicito e NAO executavel), com
`criterio_sanitizado=True`. O laco por item passou a guardar a MESMA proposta no criterio
(idempotente: reconstruir a fila nao perde auditoria) e a semear a lista a partir do criterio.
Nova `propostas_do_resultado(criterios, fila)` agrega as propostas de criterios e itens,
deduplicando por (criterio, campo, origem) — o `resultado["propostas_nao_executadas"]` passa a
conter tambem as propostas de criterios sem fila. Nada e executado; nenhum caminho de execucao
foi adicionado.

## F2R — relatorio obrigatorio indisponivel impede a aprovacao

O relatorio (`_relatorio`, dec+criterios) passou a ser montado ANTES de `classificar_estado`.
Se `relatorio.disponivel` for False (modulo AUT-7 ausente ou excecao de montagem, ex.: OSError),
e criada a lacuna

    relatorio/indisponivel  (NAO_EXERCITADO, com o motivo preservado)

a cadeia e anexada a ela, a fila e RECALCULADA (a pendencia chega ao agente) e so entao o estado e
classificado -> INCOMPLETO/exit2. Nunca se fabrica texto de relatorio. O positivo (relatorio
presente) mantem APROVADO_OFFLINE/0 inalterado.

## Cabecalho do modulo

Item 6 do docstring do modulo documenta F1R–F5R. Nenhuma constante publica (`CAMPOS_EXECUTAVEIS`,
`CAMPOS_CADEIA`, estados, exits) foi alterada.
