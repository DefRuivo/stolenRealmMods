# KIT-07 — parte 03: implementação e execução real

## Arquivos criados (implementação)
- `tools/automacao/kit07/exportador.py` — módulo (sanitização + minimização +
  pacote + manifest/hash + exclusões + limites + exclusão segura + CLI).
- `tools/automacao/kit07/teste_exportador_kit07.py` — suíte unittest (14 testes).
- `tools/automacao/kit07/contra_prova_kit07.py` — 12 defeitos plantados + controle
  falso-verde, com discriminador estrito.
- `tools/automacao/kit07/roda_testes_kit07.sh` — runner sem `.git` (layout próprio).

Reuso (não duplicado): `aut3_lib.sanitiza`/`sha256_file` (AUT-3); padrão de
suíte+contra-prova e runner do KIT-05F.

## Execução real (comando + resultado)
Comando: `bash tools/automacao/kit07/roda_testes_kit07.sh`
- Suíte do autor: `Ran 14 tests ... OK` — exit 0.
- Contra-prova por defeito: 12/12 `RECUSOU` (cada defeito plantado reprovou o
  conjunto EXATO de testes esperado) — VERDE.
- Contra-prova por teste (`--individual`): 12/12 alvos reprovando SOZINHOS — VERDE.
- Controle falso-verde: `RECUSOU` (defeito em `test_limite_por_arquivo` declarado
  como `test_minimiza_pessoal` → conjunto diferente → recusado).
- VEREDITO KIT-07: VERDE (exit 0).

## Achados reais durante a implementação (registrados, não escondidos)
1. **Teste de CLI incompleto (corrigido).** A 1ª versão só checava
   stdout/stderr/manifest/relatorio; o conteúdo dos arquivos JSON/log
   EMPACOTADOS não era verificado — uma mutação que desliga a sanitização
   passava. O teste foi ampliado para varrer todo arquivo textual do pacote.
2. **Limite do sanitizador compartilhado (documentado).** Chave JSON cujo NOME
   termina em pontuação + dois-pontos (ex.: `"password:"`) dribla a 1ª linha de
   `aut3_lib.sanitiza`: o rótulo casa, a aspa de fechamento da chave vira a aspa
   do valor e o valor real sobrevive. O fixture do teste foi corrigido para a
   forma realista (`"password": "..."`), que É redigida. Fica registrado como
   limitação conhecida do módulo compartilhado (não é escopo do KIT-07 alterar
   a AUT-3); o assunto vira observação na entrega para o revisor conferir.
3. **Carregador de teste individual (corrigido).** `loadTestsFromName(name, mod)`
   não acha método de classe; passou a usar `TesteExportador.<metodo>` (o modo
   `--individual` antes rodava 0 testes).

## Cobertura do aceite
| Item do cartão | Trava / teste |
|---|---|
| JSON+PNG+logs selecionados | `montar_pacote` (PNG opt-in) |
| manifest/hash + diagnóstico | `test_manifest_hash_confere` + `diagnostico` |
| excluir saves/assemblies | `test_exclui_save_e_assembly` |
| sanitizar por padrão genérico | `test_sanitiza_segredo_ficticio_*`, `test_minimiza_pessoal` |
| aviso de screenshot + revisão | `test_png_desligado_por_padrao`, `lista_revisao_png` |
| sem upload por padrão | `test_sem_upload_na_fonte` |
| limites de disco | `test_limite_por_arquivo`, `test_limite_total` |
| exclusão segura | `test_exclusao_segura_recusa_fora_e_apaga_pacote` |
| sem vazar valor/prefixo | `test_cli_nao_vaza_prefixo` (stdout/stderr/JSON/log) |

Runtime/pixels/desempenho: **NAO_EXERCITADO** (exige rodada autorizada do dono).
