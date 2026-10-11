# KIT-07F — correção F1–F9 (parte 03: o que mudou, achado por achado)

Arquivo central: `tools/automacao/kit07/exportador.py` (antes
`c5fc715b…f382`, depois `98fce3ff…578c`). `tools/automacao/offline/aut3_lib.py`
NÃO foi alterada (hash `04f37b8e…dc1a` intacto): a correção estrutural ficou no
exportador para não regredir as bancadas AUT-3; o `aut3_lib.sanitiza` segue como
2ª linha de defesa para texto NÃO-JSON.

## F1 — nomes físicos e metadados vazavam credencial/prefixo/nome local

- Novo mapeamento de caminho por SEGMENTO (`_sanitiza_segmento` /
  `_sanitiza_caminho` / `_caminho_pacote`): cada segmento passa por
  `aut3_lib.sanitiza` + redação FORTE de prefixo + minimização pessoal + nome
  válido no FS (`<`,`>`,`:`,`"`,`/`,`\`,`|`,`?`,`*` → `_`).
- **Redação forte** (`_redigir_prefixos`): os MESMOS formatos do `aut3_lib`, mas
  sem exigir `\b`. Motivo concreto: em `capture_tss_<...>.log` o caractere antes
  do prefixo é `_` (palavra), então `\btss_...` do `aut3_lib` NÃO casa e o
  prefixo sobrevivia ao nome do arquivo.
- Colisão e nomes reservados ganham sufixo determinístico (`-entrada`, `-entrada2`),
  registrado no manifesto — a referência e o sha256 continuam apontando para o
  arquivo real gravado.
- O manifesto e o relatório passam por `_sanea_estrutura` (mesma redação/
  minimização) antes de serializar: o comentário que dizia "manifest é saneado"
  agora corresponde ao código (antes era só comentário).
- `sanear_para_saida` (stdout/stderr) usa a redação forte + minimização.

## F2 — JSON escapado e chave pontuada vazavam segredo e quebravam o JSON

- Novo tratamento ESTRUTURAL de JSON válido (`_redigir_json` / `_json_redigido`):
  faz `json.loads`, percorre a estrutura e troca por `<REDACTED>` o valor de
  qualquer chave que casa o rótulo genérico de credencial (reusa
  `aut3_lib._ROTULO_SEGREDO`; fallback local equivalente) e aplica redação de
  prefixo em todo valor string; re-serializa, portanto o resultado É JSON válido.
  Cobre `"password:"` (chave pontuada) e valor com aspa escapada.
- Texto não-JSON continua na `aut3_lib.sanitiza` (regex de forma) — inclusive
  atribuição com chave entre aspas, sem preservar valor.
- `sanitizar` = `minimizar_pessoal(_sanitiza_texto(texto))`; `_sanitiza_texto`
  escolhe estrutural (JSON) ou regex (resto).
- Sem promessa de anonimato/segredo perfeitos: a docstring do módulo agora declara
  as lacunas e a dependência de revisão humana.

## F3 — destino podia sobrescrever a origem

- `montar_pacote` compara **caminhos canônicos** (`realpath`) antes de qualquer
  escrita e recusa igualdade E sobreposição nos dois sentidos
  (`os.path.commonpath`, tolerando drives diferentes via `ValueError`).
- Nenhuma criação/gravação ocorre antes da recusa; a origem permanece intacta.

## F4 — reexportação deixava restos fora do manifesto

- Montagem em diretório TEMPORÁRIO irmão (`<destino>.kit07-build`) e troca
  (`os.rename`) só no sucesso. A exportação bem-sucedida passa a ser exatamente
  o manifesto + política vigente: PNG com opt-in desligado e log removido da
  origem não sobrevivem no pacote.
- Se o destino existir e não for pacote KIT-07 reconhecido, a exportação é
  RECUSADA (erro de domínio) e nada é anunciado como pacote novo.

## F5 — nomes reservados eram sobrescritos depois do hash

- `manifest.json`, `relatorio.md` e o marcador são RESERVADOS: um input com esse
  nome é renomeado deterministicamente (`manifest-entrada.json`), registrado no
  manifesto; o sha256/bytes refletem o disco final e nenhuma evidência selecionada
  se perde em silêncio.

## F6 — marcador inválido autorizava apagar pasta alheia

- `_pacote_reconhecido` (trava única de `limpar_temporarios` e também do reuso de
  destino) exige: diretório (não link), marcador presente e JSON válido com
  `kit == "KIT-07"`, `manifest.json` presente/válido/do mesmo kit, e
  proveniência/escopo — NENHUM arquivo fora dos reservados e dos listados.
- Link (arquivo ou diretório) recusa a limpeza. A origem nunca é alvo.
- Consequência (defesa em profundidade): uma pasta com marcador válido mas SEM
  `manifest.json` também é recusada.

## F7 — tetos contavam entrada e falha deixava parcial

- Tetos em BYTES REAIS DE SAÍDA: `_excede_teto_arquivo` mede o conteúdo já
  sanitizado (por isso `<EMAIL>` maior que `a@b.co` conta pelo que é gravado) e
  `_confere_teto_total` soma saída + overhead declarado (`overhead_bytes`, default
  `OVERHEAD_PADRAO = 4096`, exposto em `politica.para_dict()`).
- Fechamento: `_verifica_tamanho_final` mede o pacote real em disco pelo MESMO
  teto (fecha o overhead real, não só o declarado).
- Rollback: qualquer falha remove o diretório temporário; nenhum arquivo parcial
  e nenhum `*.kit07-build` sobra. Teto insuficiente recusa com `ErroExportacao`
  (não é obrigatório caber a metadata em 24 bytes).

## F8 — CLI vazava traceback e prefixo

- Pré-checagem de domínio: destino existente que NÃO é diretório → `ErroExportacao`
  (exit 1) em vez de `FileExistsError` cru.
- `main` captura `ErroExportacao` (1), `OSError` (2) e um último `Exception` (2);
  TODA saída de falha passa por `sanear_para_saida` (redação forte + minimização),
  sem traceback e sem valor/prefixo.
- Exit distinguido: 0 sucesso, 1 domínio, 2 uso/infra. Etapa ausente nunca vira verde.

## F9 — log textual selecionado era descartado como assembly

- Classificação por TIPO: binário/assembly por nome (`Assembly-CSharp*.dll`) ou
  extensão binária (`.dll`, `.pdb`, `.exe`, …), e segmento de binário
  (`bepinex`, `managed`, …) só exclui o que NÃO é extensão textual. Assim
  `BepInEx/LogOutput.log` e `BepInEx/config.json` ENTRAM sanitizados, enquanto
  `BepInEx/Assembly-CSharp.dll` e saves seguem fora com motivo registrado.

## Contratos preservados (não enfraquecidos)

- `PoliticaExportacao(incluir_png=False, …)`, `montar_pacote(origem, destino,
  politica=None, agora=None)`, `limpar_temporarios`, `motivo_exclusao`,
  `lista_revisao_png`, `sanitizar`, `MARCADOR`, `EXT_TEXTO`, `EXT_PNG`, `KIT`.
- Sem upload: nenhum caminho de rede; `permitir_upload=True` recusa antes da escrita.

## Contra-prova: âncoras de mutação atualizadas (mesmo defeito, mesmo conjunto)

Como o módulo foi refatorado, 5 das 12 âncoras do `contra_prova_kit07.py` (que
plantam o defeito numa cópia) apontavam para trechos que mudaram. Todas foram
atualizadas para o código novo, preservando o MESMO defeito e o MESMO conjunto
exato de FAIL — e `--individual` confirma cada alvo:

| Defeito | Âncora antiga | Âncora nova | Conjunto exato de FAIL (inalterado) |
|---|---|---|---|
| sanitizacao_desligada | `aut3_lib.sanitiza(texto)` em `sanitizar` | `_sanitiza_texto(texto)` em `sanitizar` | 3 testes |
| assembly_nao_excluido | condição de binário em 1 linha | condição de binário em 3 linhas (mesmas 3 cláusulas) | test_exclui_save_e_assembly |
| limite_por_arquivo_ignorado | `if tamanho > max_bytes_por_arquivo` | `return bytes_saida > max_bytes_por_arquivo` | test_limite_por_arquivo |
| limite_total_ignorado | `if total + tamanho > max_total_bytes` | `if total_previsto + bytes_novos + overhead_bytes > max_total_bytes` | test_limite_total |
| exclusao_segura_fraca | `if not os.path.isfile(marcador)` | `problema = _pacote_reconhecido(pacote)` | test_exclusao_segura_recusa_fora_e_apaga_pacote |
| destino_alheio_sobrescrito | `if not os.path.isfile(destino/MARCADOR)` | `problema = _pacote_reconhecido(destino_abs)` | test_nao_sobrescreve_destino_alheio |

`limite_total_ignorado` exigiu que a conferência final usasse o MESMO
`_confere_teto_total` (antes havia dois blocos independentes): com dois blocos, a
mutação desligaria só um e o teste passaria — oráculo enganado.

## Novos defeitos plantados (suite KIT-07F, 5)

Acrescentados ao `contra_prova_kit07.py` para cobrir as travas NOVAS com defeito
plantado (cada um exige o conjunto EXATO de FAIL na suite
`teste_exportador_kit07f.py`):

| Defeito | Trava que ele desliga | Conjunto exato de FAIL |
|---|---|---|
| prefixo_forte_desligado | redação forte de prefixo em nomes/metadados (F1) | 3 testes (nomes excluídos, PNG, colisão) |
| caminhos_canonicos_nao_verificados | recusa por caminho canônico (F3) | 2 testes (iguais e filho) |
| nome_reservado_sobrescrito | reserva de manifest.json/relatorio.md (F5) | test_nome_reservado_nao_sobrescreve_input |
| teto_real_de_saida_nao_conferido | conferência do tamanho real do pacote (F7) | test_teto_conta_bytes_reais_de_saida_sem_parcial |
| destino_arquivo_sem_precheck | pré-checagem de destino-arquivo na CLI (F8) | test_cli_destino_arquivo_exit_dominio_sem_traceback |
