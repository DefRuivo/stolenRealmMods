# KIT-15F — entrega da correção (F1..F12)

Cartão: t_d83f3ef6. Data: 10/10/2026.
Implementação: `default` (run686 + retomada run687) — instância implementadora, **não** os revisores
`default/run678` / `default/run685`. Base: parecer `docs/automacao/KIT-15R-revisao.md` (REPROVADO).

## Veredito desta entrega

Correção **implementada e re-provada** contra os oráculos imutáveis do revisor, mantidos byte a byte.
A entrega está pronta para a **revisão independente obrigatória** (`kanban_request_review`).
Ela **não** é aprovação do produto, **não** é aceite humano, **não** é DoD e **não** desbloqueia
KIT-G2 / KIT-14 / KIT-G4.

## Arquivos corrigidos (vivos, com hash)

| Arquivo | sha256 |
|---|---|
| `tools/automacao/kit15/instalador.py` | `aa9e0081fe828f45dbba30f5d242fabcc4a16d2f2fdf2823154f8cf225533ef0` |
| `tools/automacao/kit15/pacote.py` | `9015f6037fce153281239d6f6b065bb02fd04dde94193d2773fa501c8280bf30` |
| `tools/automacao/kit15/scan.py` | `ef69990e0fc5960794cf0b6df80535a1592c1d04088d47f702414819a689804b` |
| `tools/automacao/kit15/teste_kit15.py` | `72caddfbffa0538592c7a61ede1494ca4d9215815c0301f684d0a9994e332ef7` (run689; era `57473e60…` no run687 — ver parte 03) |
| `tools/automacao/kit15/contra_prova_kit15.py` | `2a7e110ffa07c48e54a3017f0e4060899a3066670dd40f1ea68152b6226cfd73` |
| `tools/automacao/kit15/manifesto.json` | `5821ffbf2543cc6f3804e2f50f2f3e958b014e84597c2042e1ebfe0df31537ff` |
| `tools/automacao/kit15/roda_testes_kit15.sh` | `2a0c73b89b004e3adb9c31b3e0fb17a8b4c7237e7b3ff1c895cf9bb1dc185cfd` |
| `tools/automacao/kit15/README.md` | `80f6127fada8491daeee4036556f5c4dec4596376d04ad5feefa4ec64e95ef3f` |
| `tools/automacao/kit15/README.en.md` | `8ef07862e1132df7dd874c1fb11a540491d5897fbef30c682c03aba47cfd3b4d` |
| `tools/automacao/kit15/docs/primeiro-uso.md` | `92bf0a5e6e54cfa31e8007554845c21b26192d8dd6fe428904704c94dda0bcc1` |
| `tools/automacao/kit15/descoberta.py` (inalterado) | `10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86` |

Relatório do pacote: `scratch/kit/KIT-15F-run687/pacote-proprio/pacote-relatorio.json`.

## Prova por achado (todas re-executadas nesta retomada)

| # | Achado (KIT-15R) | Como foi fechado | Teste que prova | Resultado |
|---|---|---|---|---|
| F1 | ZIP com `descoberta.py` divergente da fonte viva | ZIP regerado das fontes congeladas; conferência de **todos** os membros | `verify_f1.py` | 42 membros, 41 payload, **0 divergentes**, `origem_viva_sem_membro=[]` |
| F2 | manifesto/recibo não autoritativos | `validar_manifesto`/`validar_recibo` (schema, tipos, obrigatórios, fechamento exato, hash declarado) | `test_F2_*` (5) + `test_extra F2_empty_receipt_not_installed` | 6/6 OK |
| F3 | OSError deixa fonte sem recibo/journal | transação antes da cópia + reversão de falha de I/O | `test_F3_copy_exception_must_not_leave_partial` | OK |
| F4 | rollback da remoção não restaurava | ação reversa corrigida + leitura de volta (API e CLI) | `test_F4_rollback_removal_restores_all_files` | OK |
| F5 | preexistente apagado / dono perdido / órfãos | propriedade explícita e seleção sem órfãos | `test_F5_*` (3) | 3/3 OK |
| F6 | backup corrompido restaurado com rc0 | falha fechada com backup corrompido/ausente | `test_F6_remove_refuses_corrupted_original_backup` | OK |
| F7 | `verificar` sem `--json` dava KeyError/exit 1 | saída e exits corrigidos nos dois modos | `test_F7_verifier_documented_cli` | OK |
| F8 | suíte/repack/shell dependiam do layout do autor | layout distribuído autossuficiente | `test_F8_*` (3) | 3/3 OK |
| F9 | dependências transitivas e ProjectReference quebrados | closures fechados nos componentes; docs corrigidas | `test_F9_*` (4) | 4/4 OK |
| F10 | JSON/`bin/`/erro de IO escapavam do scanner | padrões JSON, sem poda de `bin/`, `erro-io` | `test_F10_*` (3) + `P4`/`P5` | 5/5 OK |
| F11 | contra-prova aceitava Ran0/ERROR como RED | RED honesto lido de resultado estruturado | `contra_prova_kit15.py` + isca própria | 7/7 recusados; isca = **FALSO-VERDE**, exit 1 |
| F12 | traversal de `id`/`rel` escrevia fora do destino | confinamento antes de efeitos | `test_F12_*` (2) | 2/2 OK |

## Suites e oráculos

| Suite | Origem | Resultado |
|---|---|---|
| Oráculo de revisão (imutável, 27 testes) | `scratch/kit/KIT-15R-run678/test_review_kit15.py` sha `1efb6c18…6a449` | **27 OK / 0 FAIL / 0 ERROR / 0 skip**, exit 0 |
| Oráculo extra (imutável, 3 testes) | `scratch/kit/KIT-15R-run678/test_extra_kit15.py` sha `e68eb481…9d56` | **3 OK**, exit 0 |
| Suíte do autor (18 testes) | `tools/automacao/kit15/teste_kit15.py` | **18 OK**, exit 0 |
| Contra-prova (8 execuções) | `tools/automacao/kit15/contra_prova_kit15.py` | baseline verde + **7/7 defeitos recusados**, exit 0 |
| Controle negativo de F11 | isca que quebra a suíte antes de rodar | **FALSO-VERDE ×7 / FALHOU**, exit 1 |

Nenhum ERROR, nenhum skip e nenhuma ausência foi contabilizado como verde. O `red/green` seletivo foi
exercitado: a contra-prova muda um módulo por vez e exige RED com o conjunto de falhas exato.

## Artes e evidências (scratch/kit/KIT-15F-run687/)

- `pacote-proprio/kit-rstv-0.1.0.zip` — sha256 `f1f927fd12eb7314ace62d92b2e550db2c22d7e7143068699a8f9a9341a959bc`, 174455 bytes, 42 membros.
- `verify_f1.py` + `verification.json` — identidade membro-a-membro (0 divergências).
- `review-results.json`, `review-out.txt` — oráculo de revisão.
- `extra-results.json`, `extra-out.txt` — oráculo extra.
- `autor-result.json`, `autor-out.txt` — suíte do autor.
- `contra-out.txt`, `contra/contra-prova.json` — contra-prova.
- `f11-bait/`, `f11-bait-out/contra-prova.json`, `f11-bait-out.txt` — controle negativo de F11.
- `shim/`, `pacote-relatorio-stdout.txt` — ambiente e relatório do pacote.

Baselines históricos preservados: `scratch/kit/KIT-15R-run678/` e `scratch/kit/KIT-15R-run685/`
**não** foram sobrescritos. As cópias dos oráculos usadas aqui têm hash idêntico ao original.

## Decisões registradas (para o revisor contestar se quiser)

1. **Composição do pacote fixa em 41 payloads.** O oráculo P1 exige recibo com exatamente 41 arquivos
   e F2 exige fechamento manifesto↔pacote. Logo, o pedido de F9 por "exemplos/contrato/schema" foi
   atendido **fechando os closures reais**, não empacotando membros novos.
2. **Docs do pacote × docs do repositório.** O link foi corrigido para valer no pacote (onde o README
   fica ao lado de `primeiro-uso.md`), com nota sobre o caminho no repositório de origem.
3. **`bash` do WSL.** O runner de shell precisa de um bash que entenda caminhos do Windows. Isso está
   declarado como **não medido** na doc do pacote; no ambiente sem WSL o mesmo script roda verde.

## Limites desta entrega (não medido)

Runtime no jogo (BepInEx/plugin/UI/personagem), build e deploy C#, segundo host, Linux/macOS,
publicação. Nada foi instalado no perfil do dono, nenhum jogo foi aberto/fechado, nenhum save tocado,
nenhum push/tag/Release/Thunderstore executado. Gates humanos e DoD permanecem separados.

## Correção do achado F11 pedida na revisão independente (run688 → run689)

A revisão independente run688 (revisor ≠ implementador) devolveu `changes_requested` com **um**
achado bloqueante em F11: a contra-prova declarava `FALHOU` sobre um baseline verde quando a sandbox
ficava fora da árvore (o default dela), porque `test_15` comparava a expectativa de layout com a
implementação usando **dois resolvedores diferentes** (o caminho da cópia × a env `KIT15_RAIZ`).

Corrigido em `tools/automacao/kit15/teste_kit15.py` (único arquivo de produto alterado;
`descoberta.py` intacto): a expectativa do padrão de destino passa a ser derivada das **mesmas duas
fontes** do contrato (env do processo + raiz acima da cópia), sem perguntar ao código sob teste qual
é o layout — assim o teste não fica tautológico.

Re-provado no run689: mesmo veredito nas 3 localizações de sandbox (`TMPDIR`, dentro do repo,
`TMPDIR` ausente) = **OK / baseline verde / 7/7**; `bash tools/automacao/kit15/roda_testes_kit15.sh`
= **VERDE exit 0**; oráculos imutáveis 27 OK + 3 OK; suíte do autor 18 OK; isca F11 = `FALHOU`
exit 1; **controle positivo novo** (cópia fora da árvore + `raiz_efetiva` mutada) = só
`test_15` falha, 0 ERROR/skip, exit 1. Provas, matriz de localização e hashes:
`docs/automacao/KIT-15F-parte03.md` e `scratch/kit/KIT-15F-run689/`.
Pacote regerado nesta rodada: `scratch/kit/KIT-15F-run689/pacote-proprio/kit-rstv-0.1.0.zip`
sha256 `197cb1efeb2ea814a9ccfed9115cda3b956bec5728347fcf24c3fd89cdc1a00b`, 175059 bytes, 42 membros,
`PACOTE_LIMPO` (o `CHANGELOG.md` do kit também recebeu a nota da correção).

## Próximo passo

Revisão nativa independente (`kanban_request_review`) por instância ≠ implementadora, com
implementer/reviewer, caminhos, hashes e estas provas. Só depois da reconferência independente a
correção é `complete`. Concluir KIT-15R/15F **não** autoriza KIT-G2 `t_f19310d3`, KIT-14 `t_a1f38855`
nem KIT-G4 `t_b001720d`.
