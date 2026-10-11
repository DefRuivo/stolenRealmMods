# KIT-07F — revisão independente (revisor run642 ≠ implementador run640)

- Cartão: **t_a7318a33** (KIT-07F) · perfil default · revisor **run642**
  (instância independente; ≠ implementador run640, ≠ autor run634, ≠ revisor KIT-07R run636).
- Objeto: correção dos achados F1–F9 do parecer **KIT-07R t_96d0c463** (REPROVADO).
- Método: leitura fria do artefato + reprodução própria (não reusa cópias do implementador).
- Veredito: **APROVADO** — F1–F9 corrigidos e comprovados; ver `kanban_complete`.

## Como foi verificado (sandbox próprio `scratch/kit/KIT-07F-run642/`)

| Verificação | Alvo | Resultado real (exit) |
|---|---|---|
| Suite independente KIT-07R (24) | **corrigido** `98fce3ff…` | exit **0** · Ran 24 · **OK** |
| Suite independente KIT-07R (24) | **reprovado** `c5fc715b…` | exit **1** · Ran 24 · **FAILED (failures=15)** · 0 ERROR · 0 skip |
| Quais testes discriminam | `c5fc715b…` | 15 exatos: **todas** as F1/F2/F3/F4/F5/F6/F7/F8/F9 + os 9 controles positivos verdes nos dois |
| Suite autor (14) | corrigido | exit **0** · Ran 14 · **OK** |
| Suite KIT-07F nova (12) | corrigido | exit **0** · Ran 12 · **OK** |
| Contra-prova por defeito | 17 defeitos plantados | exit **0** · 17 RECUSOU · falso-verde RECUSOU |
| Contra-prova por teste | 22 alvos individuais | 22 RECUSOU · 0 ACERTOU-INDEVIDO |
| Runner `roda_testes_kit07.sh` | completo | exit **0** · VEREDITO KIT-07: **VERDE** |
| Sondas do revisor (21, próprias) | corrigido | **21 PASS** · exit 0 |
| Sondas do revisor (21, próprias) | reprovado | **11 FAIL / 10 PASS** · exit 1 (RED discriminante) |
| Scanner `check_segredos.py` | cópia git própria | nominal exit **0**; planta fictícia exit **1** |
| Scanner `check_padroes_segredo.py` | cópia git própria | nominal exit **0**; planta fictícia exit **1** |

Sondas próprias cobrem, por caminhos diferentes da suite: credencial em **nome de
diretório**, nome pessoal aninhado, excluído com credencial no nome saneado no manifest,
JSON **aninhado/array** com `api_key`/`client_secret`/`password:` ainda **válido**,
origem==destino com separador diferente, reexport removendo **.json** (não só PNG/log),
hash/bytes do disco final com nomes reservados, marcador **válido** + arquivo extra alheio
(não autoriza limpeza), teto por arquivo contando **saída sanitizada expandida**, teto total
sem parciais, CLI com origem-arquivo (exit 2, sem traceback), log textual `BepInEx/LogOutput.log`
incluído e DLL de BepInEx excluída.

## Checagens de integridade/autoria

- `tools/automacao/offline/aut3_lib.py` **INALTERADA**: `git diff HEAD` vazio, sha `04f37b8e…`.
- `tools/automacao/kit07/teste_exportador_kit07.py` **INALTERADA**: sha `2dc7ea39…` **idêntico**
  à cópia histórica independente `scratch/kit/KIT-06R-run638/sandbox/.../teste_exportador_kit07.py`
  (run638, 13 min antes da correção) → a suite autor **não foi enfraquecida**.
- Módulo auditado `c5fc715b…` confirmado por cópia histórica independente (run638) — o baseline é real.
- Suite da revisão KIT-07R `e54a6be2…` usada **sem alteração** (mesmo sha do run636).
- Hashes dos docs `KIT-07F-parte01..04`/`entrega-final` conferem com `verification-final.json`.
- Sandbox sem `.git` remoto/perfil/credencial; nada de jogo/save/mod/build/deploy/publicação.

## Limites (não bloqueiam; herdados e declarados pelo implementador)

- runtime/pixels/desempenho/interferência do jogo **NAO_EXERCITADO**.
- Anonimato/segredo **não são universais**: JSON inválido/JSONL cai na 2ª linha (`aut3_lib`);
  chaves pontuadas fora da lista explícita (ex.: `api.key`) e valores arbitrários sem prefixo
  conhecido não são mascarados. Cobertura por forma + revisão humana; nada de promessa perfeita.
- Corrida de substituição entre processos (entre `rmtree` do destino antigo e `rename`) não exercitada.
- `.deps.json` em `EXT_BINARIO` é alcançado como texto (splitext devolve `.json`); não é vazamento
  (seria sanitizado), é código morto — fora do escopo F1–F9, registrado para roteamento.

## Próximo passo

Aprovação libera KIT-08 `t_e2107a63` e KIT-15 `t_10584ca5` (dependentes desta correção com
revisão independente). Este parecer **não** é aprovação de DoD humano nem autoriza gates.
