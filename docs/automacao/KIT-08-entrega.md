# KIT-08 — ENTREGA: visualizador HTML local e comparação de sessões

Cartão `t_e2107a63` · perfil `default` · **offline** (sem jogo, sem save, sem
deploy, sem publicação, sem servidor/rede, sem dependência Hermes/IA/credencial).
Revisão independente no cartão-filho **t_70608c71**.

> Aprovar tecnicamente **não** equivale a aceite humano nem à publicação do DoD.
> Runtime/pixels/desempenho: **NAO_EXERCITADO**. Nada instalado/publicado/commitado.

## 0. Veredito por item do aceite

| Item do aceite (cartão) | Veredito | Prova (execução real) |
|---|---|---|
| HTML local acessível **fora do jogo, sem servidor/conta/Hermes** | **PASSOU** | `visualizador.py` gera 1 arquivo autocontido; CLI real ⇒ `bytes=6823 sha256=67a7f581…` |
| Por caso/mod: **esperado/observado** | **PASSOU** | campos no card do caso; `test_campos_por_caso_presentes` |
| Por caso/mod: **prova** | **PASSOU** | lista de evidência (caminhos validados) + `motivo`; `test_campos_por_caso_presentes` |
| Por caso/mod: **imagem** | **PASSOU (com guarda)** | `<img>` só se a referência é local segura; remota ⇒ recusada; `test_imagem_remota_recusada` |
| Por caso/mod: **sessão/build/config** | **PASSOU** | bloco de contexto (sessao, versao_jogo, bepinex, build_id, config/fonte/dll_sha) |
| Por caso/mod: **lacunas** | **PASSOU** | `lacuna_probe` + "sem prova de runtime" + origem sintética |
| Comparar baseline×candidata **só com contextos compatíveis** | **PASSOU** | `contextos_compativeis` (mínimo `versao_jogo`+`bepinex`, divergência recusada); incompatível ⇒ `INDETERMINADO`; `test_contexto_incompativel_recusa`, `test_contexto_incompleto_recusa` |
| **Fonte alterada invalida aprovação stale** | **PASSOU** | `aprovacao_stale` marca `STALE (INVALIDADA)`; `test_stale_quando_fonte_muda`; exemplo real mostra STALE |
| **Escapar texto recebido** (nada de HTML/JS) | **PASSOU** | `escapar` = `html.escape` em todo dado; `test_escapar_payload_vira_texto`, `test_html_sem_tag_script_de_dado` |
| **Não executar JS dos logs** | **PASSOU** | nenhuma tag de script gerada; CSP `script-src 'none'`; `test_csp_script_none`, `test_html_sem_tag_script_de_dado` |
| **Arquivos exportados não injetam HTML/script** | **PASSOU** | payload `<img onerror>`/`<script>` vira texto; exemplo real: `grep -c "<script" = 0` |
| **Referências são locais seguras** | **PASSOU** | `referencia_local_segura` recusa esquema/absoluto/UNC/`..`; `test_recusa_esquemas_e_absolutos` |
| **Aceite humano/publicação separados do técnico** | **PASSOU** | seção "Aceite HUMANO / PUBLICACAO" PENDENTE; `test_secao_humana_separada_e_pendente` |
| **Reusar decisão/relatório existentes** | **PASSOU** | importa `cenarios/kit09.py` (avaliador real) por caminho; `test_fixture_sintetica_nunca_ok` (21 critérios) |
| **Exemplo real do coletor + fixtures rotuladas** | **PASSOU (parcial)** | fixtures rotuladas do KIT-09 + 3 fixtures KIT-08; **coletor AUT-4 runtime NÃO exercitado** (ver lacunas) |
| **PASSOU/FALHOU/NAO_EXERCITADO/INDETERMINADO distintos** | **PASSOU** | `veredito_tecnico`; `test_fixture_nunca_passa`, `test_passa_so_com_runtime` |
| Runtime (pixels/desempenho/interferência) | **NAO_EXERCITADO** | exige rodada autorizada do dono (fora do escopo) |

## 1. Arquivos entregues (NOVOS; nenhum artefato de outra frente editado)

```
3d6d2983a845d1423859ef75f7f8e658cde7c14c0d4fe3ee23194d08a9789701  tools/automacao/kit08/visualizador.py
840f62e9da178ea6c21af5f8a37e0fc0022b14999832bbfbc3395d5dfe079e7e  tools/automacao/kit08/teste_visualizador_kit08.py
9555233e989e76e691b42d3977063ab9399623f0593110294d3076476c876551  tools/automacao/kit08/contra_prova_kit08.py
37de9d8de93f65b74eaf2df6296a63e9298a557479b78d3a08b4e3a1407db394  tools/automacao/kit08/roda_testes_kit08.sh
8985ae04b962c5d940780e2785a556a84460524720614c76dfcf0f151354e362  tools/automacao/kit08/fixtures/aprovacao-antiga.fixture.json
ea3c3384e6783d049073dc4b59ae32fb56a7241f57f5bd8fa7bcf199280a3dd5  tools/automacao/kit08/fixtures/sessao-baseline.fixture.json
730693217c53dea9929d9f1057939bd892a71dc311e1bb06997df2c218af0742  tools/automacao/kit08/fixtures/sessao-candidata.fixture.json
67a7f581c52adfadf212b5e3410c22e3dc45d05e331aba67ce61aedba395cf16  scratch/kit/k08/relatorio-exemplo.html   (exemplo REAL gerado)
```
Peças de progresso: `docs/automacao/KIT-08-parte01.md` … `-parte04.md`.
`git status` mostra apenas novos (`?? tools/automacao/kit08/`). Sem `git add -A`.

## 2. Execução real (comando + exit + caminho do log)

- `bash tools/automacao/kit08/roda_testes_kit08.sh` → **exit 0**
  (`Ran 21 tests ... OK` + contra-prova 8/8) → log `scratch/kit/k08/rodada.log`.
- `python tools/automacao/kit08/contra_prova_kit08.py` → **exit 0** VERDE (8/8 defeitos
  recusados com conjunto EXATO) → log `scratch/kit/k08/contra.log`.
- Reuso KIT-09 sobre fixture sintética ⇒ 21× `NAO_EXERCITADO` (nenhum PASSOU) →
  `scratch/kit/k08/smoke-verdade.html`.
- Exemplo baseline×candidata + aprovação antiga ⇒ `FALHOU:1 NAO_EXERCITADO:1 stale=True`
  (exit 1, como esperado) → `scratch/kit/k08/relatorio-exemplo.html`.

## 3. Travas exercitadas como RED (defeito plantado → reprova)

8 defeitos, cada um com o conjunto EXATO de testes que devem falhar: escape
desligado; CSP com `unsafe-inline` de script; referência sempre "segura"; contexto
sempre compatível; stale ignorado; `OK` sem runtime passa; guarda de fixture
desligada; **falso-verde** (defeito inofensivo) recusado. O discriminador exige o
conjunto exato — um defeito que derruba conjunto diferente é RECUSADO.

## 4. Achados/lacunas registrados (não escondidos)

1. **Correção durante a implementação:** `referencia_local_segura` ecoava o valor
   recusado no motivo, introduzindo URL como texto no HTML; corrigido (o motivo
   nunca reproduz o valor recebido).
2. **Limite honesto de autenticação:** `veredito_tecnico` confia nos campos de
   procedência do upstream (`prova_runtime`/`procedencia`). A guarda
   `origem_sintetica(doc)` REBAIXA PASSOU quando o doc se rotula fixture/sintético,
   mas um artefato NÃO rotulado com `prova_runtime=True` forjado ainda apareceria
   como PASSOU. A origem é responsabilidade de quem produz o artefato
   (KIT-09/coletor); o visualizador não é um autenticador.
3. **Coletor AUT-4 runtime NÃO exercitado:** o formato do coletor foi lido
   (`runtime/coletor.py`, `probe-saida-exemplo.entrada.json`), e o reuso é do
   avaliador KIT-09; a leitura viva do jogo permanece **NAO_EXERCITADO** (exige
   rodada AUT-4 autorizada pelo dono).
4. **Runtime/pixels/desempenho:** NAO_EXERCITADO.
5. Anonimato/segredo de imagem: PNG não é sanitizado automaticamente (herdado do
   KIT-07); o visualizador só EMBUTE o que o produtor do pacote já incluiu.

## 5. Limites desta entrega

- Sem jogo/save/deploy/instalação/publicação; nada commitado.
- Aprovar tecnicamente **não** é aceite humano nem publicação do DoD.

## 6. Passo seguinte

Revisão independente no cartão **t_70608c71 (KIT-08R)**: refutar XSS/execução de
JS de log, referência remota, comparação de contexto incompatível, aprovação
stale aceita e auto-aprovação humano; exercitar controle negativo em sandbox
própria e rodar `roda_testes_kit08.sh` contra cópia independente.
