# KIT-07F — entrega final (correção dos achados F1–F9)

- Cartão: **t_a7318a33** (KIT-07F) · perfil default · implementador **run640**
  (instância nova, ≠ autor run634 e ≠ revisor run636).
- Dependência honrada: parecer **KIT-07R t_96d0c463** (REPROVADO). Filhos que
  aguardam esta correção com revisão independente: KIT-08 t_e2107a63, KIT-15 t_10584ca5.
- Natureza: correção ofﬂine de ferramenta Python (stdlib). Nenhum jogo, save real,
  mod, Bard, Assembly-CSharp.dll, build, deploy, instalação ou publicação.
  Histórico da revisão preservado: nenhum artefato de `scratch/kit/KIT-07R-run636`
  foi reescrito ou removido.

## Veredito do implementador

Os nove achados F1–F9 foram corrigidos no código e demonstrados por execução
real: **RED** no módulo reprovado → **GREEN** no corrigido, com os 9 controles
que já passavam mantidos e 5 novos defeitos plantados cobrindo as travas novas.
Pedido de REVISÃO INDEPENDENTE neste mesmo cartão (não autoaprovado).

## O que mudou

- **F1** mapeamento de caminho por segmento com redação FORTE de prefixo (sem
  depender de `\b`, que falhava em `capture_tss_...`), minimização pessoal, nome
  válido no FS, colisão e nomes reservados com sufixo determinístico; manifesto,
  relatório, excluídos e `png_para_revisao` saneados (o comentário do manifest
  agora corresponde ao código).
- **F2** tratamento ESTRUTURAL de JSON (parse → redação do valor de chave de
  credencial e de prefixos em qualquer string → re-serialização VÁLIDA); cobre
  `"password:"` e aspa escapada. `aut3_lib` NÃO foi alterada (hash intacto); texto
  não-JSON continua na regex de forma da lib.
- **F3** recusa por caminhos canônicos (`realpath` + `commonpath`) de igualdade e
  de qualquer sobreposição, antes de criar/gravar; a origem nunca é escrita.
- **F4** montagem em diretório TEMPORÁRIO e troca só no sucesso: pacote final ==
  manifesto + política vigente (sem PNG/log antigo); reuso de destino não
  reconhecido é recusado, sem anunciar pacote novo.
- **F5** `manifest.json`/`relatorio.md`/marcador RESERVADOS: input homônimo é
  renomeado de forma determinística e registrado; hash e bytes refletem o disco final.
- **F6** `_pacote_reconhecido` valida identidade (marcador JSON `kit=KIT-07`),
  conteúdo (manifest), proveniência/escopo (nenhum arquivo extra/não listado) e
  recusa links; nunca limpa a origem.
- **F7** tetos em **bytes reais de saída** (conteúdo já sanitizado) + overhead
  declarado (`overhead_bytes`, default 4096) + conferência do tamanho REAL do
  pacote; rollback sem parciais e sem temp residual.
- **F8** pré-checagem de destino-arquivo (domínio, exit 1) e captura/saneamento de
  `OSError`/`Exception` na CLI (exit 2), sem traceback e sem valor/prefixo.
- **F9** classificação por TIPO: log textual em segmento de binário
  (`BepInEx/LogOutput.log`, `config.json`) entra sanitizado; `Assembly-CSharp.dll`
  e saves seguem fora com motivo.

## Evidência (todas com exit real)

| Verificação | Alvo | Resultado |
|---|---|---|
| Suite independente da revisão (24) | módulo reprovado `c5fc715b…` | **exit 1** · Ran 24 · **FAILED (failures=15)** · 0 ERROR · 0 skip |
| Suite independente da revisão (24) | módulo corrigido `98fce3ff…` | **exit 0** · Ran 24 · **OK** |
| Suite KIT-07F nova (12) | módulo corrigido | **exit 0** · Ran 12 · **OK** |
| Suite KIT-07F nova (12) | módulo reprovado | **exit 1** · Ran 12 · **FAILED (failures=10)** · 0 ERROR · 0 skip |
| Suite autor (14, regressão) | módulo corrigido | **exit 0** · Ran 14 · **OK** |
| Contra-prova por defeito | 17 defeitos plantados | **exit 0** · 17 RECUSOU · falso-verde RECUSOU |
| Contra-prova por teste | 22 alvos individuais | **exit 0** · 22 RECUSOU · 0 ACERTOU-INDEVIDO · 0 ERROR |
| Runner completo | `roda_testes_kit07.sh` | **exit 0** · VEREDITO KIT-07: VERDE |
| Scanners de credencial | cópia isolada, sem remote | nominal exit 0; planta FICTÍCIA exit 1; planta removida |

Logs: `scratch/kit/KIT-07F-run640/{author-suite.log, extra-suite-novo.log,
extra-suite-baseline-RED.log, contra-prova-defeitos.log, contra-prova-individual.log,
runner-final.log, new/review-new.log, baseline/review-baseline.log}`.
Resumo legível por máquina: `scratch/kit/KIT-07F-run640/verification-final.json`.

## Artefatos e hashes

| Arquivo | sha256 |
|---|---|
| `tools/automacao/kit07/exportador.py` | `98fce3ff8e2c9c8a026ce1e7693bfdf5bc66ab523a92a0acc94cb4725c02578c` |
| `tools/automacao/kit07/teste_exportador_kit07f.py` (novo) | `181c66bdd1850374b929f6968715d81453cf86130f680014fa8041ed7e0c8f78` |
| `tools/automacao/kit07/contra_prova_kit07.py` | `df7ad28074d6015a63cfd5598f576fe11edc2e4a3222efed9be63d5f156df9e7` |
| `tools/automacao/kit07/roda_testes_kit07.sh` | `54bfc7242fc9c0928939349c650aeea89d27e23d0f5f9b36cf7d5eca381f6601` |
| `tools/automacao/kit07/teste_exportador_kit07.py` (INALTERADA) | `2dc7ea39e0834041f7176969aced4c58a19be200e4c84137289b895f65fb4f51` |
| `tools/automacao/offline/aut3_lib.py` (INALTERADA) | `04f37b8e285ad7d429d0d01cd846523323ca0a403ce64203890e3c0538d6dc1a` |
| `docs/automacao/KIT-07F-parte01..04.md` | em `verification-final.json` |

## Como reproduzir

    cd C:/dev/stolen-realm
    export PYTHONDONTWRITEBYTECODE=1
    bash tools/automacao/kit07/roda_testes_kit07.sh          # espera exit 0 (VERDE)
    python scratch/kit/KIT-07F-run640/coleta_final.py        # RED x GREEN com exits
    python scratch/kit/KIT-07F-run640/baseline/test_review_kit07.py   # espera exit 1 (15 FAIL)
    python scratch/kit/KIT-07F-run640/new/test_review_kit07.py        # espera exit 0 (24 OK)

## Documentação

- `docs/automacao/KIT-07F-parte01.md` — abertura/escopo.
- `docs/automacao/KIT-07F-parte02.md` — linha de base RED (15 FAIL reproduzidos).
- `docs/automacao/KIT-07F-parte03.md` — correção por achado + âncoras de mutação.
- `docs/automacao/KIT-07F-parte04.md` — verificação, hashes e limites.

## Limites

runtime/pixels/desempenho/interferência NAO_EXERCITADO; corrida de substituição
entre processos não exercitada; anonimato/segredo não são universais (cobertura
por forma + revisão humana); scanners cobrem os arquivos/padrões selecionados.
Nada foi instalado, aberto, publicado ou deployado; gate humano inalterado.

## Próximo passo

Revisão independente NESTE cartão (revisor ≠ run640): confirmar F1–F9, RED/GREEN,
contra-provas com conjunto exato e hashes; fechar com `kanban_complete` somente se
corrigidos — caso contrário `kanban_request_changes`. KIT-08/KIT-15 seguem
bloqueados até essa decisão.
