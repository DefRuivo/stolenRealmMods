# KIT-08 — parte04: contra-prova verde, exemplo real e verificação de segurança

## Contra-prova (defeito plantado → conjunto EXATO de testes falha)

`python tools/automacao/kit08/contra_prova_kit08.py` → **exit 0**, VERDE (8/8):

```
CONTROLE_base|OK|suite real verde (exit 0)
D1_escape_desligado      RECUSOU  {test_escapar_payload_vira_texto, test_html_sem_tag_script_de_dado}
D2_csp_script_inline     RECUSOU  {test_csp_script_none}
D3_referencia_sempre_segura RECUSOU {test_recusa_esquemas_e_absolutos, test_imagem_remota_recusada, test_html_sem_rede}
D4_contexto_sempre_compativel RECUSOU {test_contexto_incompativel_recusa, test_contexto_incompleto_recusa}
D5_stale_ignorado        RECUSOU  {test_stale_quando_fonte_muda, test_stale_quando_contexto_atual_omite_hash}
D6_ok_sem_runtime_passa  RECUSOU  {test_fixture_nunca_passa}
D8_guard_fixture_desligado RECUSOU {test_fixture_rotulada_nunca_passa_no_doc}
D7_falso_verde_sem_efeito RECUSOU (defeito inofensivo NAO pode ser aceito)
VEREDITO KIT-08 contra-prova: VERDE (8/8 defeitos recusados exato)
```

## Runner completo (suite + contra-prova)

`bash tools/automacao/kit08/roda_testes_kit08.sh` → **exit 0**:
`Ran 21 tests ... OK` + contra-prova VERDE → `VEREDITO KIT-08: VERDE`.
Log: `scratch/kit/k08/rodada.log`.

## Exemplo REAL do coletor/avaliador + fixtures rotuladas

1. **Reuso do KIT-09** (avaliador real, não duplicado): `kit09-verdade.entrada.json`
   (fixture sintética, 21 critérios) → **21 NAO_EXERCITADO**, nenhum PASSOU,
   `stale=False`, exit 2. Prova de que fixture rotulada não vira prova de runtime
   também no visualizador: `scratch/kit/k08/smoke-verdade.html`.

2. **Comparação baseline × candidata com contexto compatível** + aprovação STALE,
   3 fixtures ROTULADAS novas (`tools/automacao/kit08/fixtures/`):
   ```
   python tools/automacao/kit08/visualizador.py \
     --entrada tools/automacao/kit08/fixtures/sessao-candidata.fixture.json \
     --baseline tools/automacao/kit08/fixtures/sessao-baseline.fixture.json \
     --aprovacao tools/automacao/kit08/fixtures/aprovacao-antiga.fixture.json \
     --saida scratch/kit/k08/relatorio-exemplo.html
   KIT-08: bytes=6823 sha256=67a7f581... contagem={"FALHOU":1,"NAO_EXERCITADO":1} stale=True  (exit 1)
   ```
   Verificado no HTML gerado: `class="reg"` (regressão janela REPROVADO vs baseline),
   `estado: <b>FALHOU`, `STALE (INVALIDADA)`, `PENDENTE (nao concedido`.

## Verificação de segurança do HTML produzido (sinal ≠ efeito: leitura do arquivo)

```
grep -c "<script" relatorio-exemplo.html   -> 0
grep -o 'http[^"]*' relatorio-exemplo.html -> http-equiv=      (só a meta CSP; nenhum URL remoto)
```
CSP do arquivo: `default-src 'none'; ... script-src 'none'; base-uri 'none'; form-action 'none'`.

## Achados/lacunas registrados

1. **Referência recusada ecoava o valor** → corrigido (o motivo nunca reproduz o
   valor, que pode vir de dado recebido).
2. **Contra-prova D1/D2/D3/D8 exigiram calibração do discriminador** (âncora única,
   conjunto exato): achado do processo, não defeito do entregável.
3. **Limite honesto:** `veredito_tecnico` confia nos campos de procedência do
   upstream (`prova_runtime`/`procedencia`); por isso há a guarda
   `origem_sintetica(doc)` que REBAIXA PASSOU quando o próprio doc se rotula
   fixture/sintético. Um documento NÃO rotulado com `prova_runtime=True` forjado
   ainda seria apresentado como PASSOU — a origem é responsabilidade de quem
   produz o artefato (KIT-09/coletor); o visualizador não é um autenticador.
4. **Runtime/pixels/desempenho: NAO_EXERCITADO** (exige rodada autorizada do dono;
   fora do escopo offline).

**Checkpoint parte04:** suíte+contra-prova verdes, exemplo real gerado e verificado;
próximo = escrever `KIT-08-entrega.md` e pedir revisão.
