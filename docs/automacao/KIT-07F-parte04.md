# KIT-07F — correção F1–F9 (parte 04: verificação, hashes e limites)

Todas as execuções são offline (stdlib), sem jogo, save real, mod, build, deploy
ou publicação. Logs em `scratch/kit/KIT-07F-run640/`. `PYTHONDONTWRITEBYTECODE=1`.

## 1. Suite do autor (regressão) — 14 testes

    python tools/automacao/kit07/teste_exportador_kit07.py
    -> exit 0 / Ran 14 tests / OK            (author-suite.log)

Hash da suite inalterado em relação à revisão: `2dc7ea39…4f51` (nenhum teste do
autor foi enfraquecido, removido ou "ajustado para passar").

## 2. Suite independente da revisão (24 testes) — RED → GREEN

| Alvo | Comando | Resultado |
|---|---|---|
| módulo REPROVADO (baseline, hash `c5fc715b…`) | `python baseline/test_review_kit07.py` | exit 1 / Ran 24 / FAILED (failures=15) / 0 ERROR / 0 skip |
| módulo CORRIGIDO (`98fce3ff…`) | `python new/test_review_kit07.py` | exit 0 / Ran 24 / OK |

Os 15 nomes de FAIL na baseline são exatamente os do parecer (parte02). Os 24
testes passam no módulo novo — inclusive os 9 que já passavam.

## 3. Testes adicionais (KIT-07F) — 12 testes

Cobrem: nome de arquivo EXCLUÍDO e PNG saneados no caminho físico e no manifesto
(F1), colisão de nomes mascarados, recusa por caminhos canônicos equivalente e
aninhado sem parcial (F3), nome reservado sem sobrescrever input (F5), teto total
em bytes reais de saída com rollback (F7), teto por arquivo medido na SAÍDA
sanitizada (F7), erros de I/O da CLI com exit de domínio e sem traceback (F8),
log textual em segmento de binário entrando sanitizado com assembly fora (F9).

| Alvo | Resultado |
|---|---|
| módulo CORRIGIDO | exit 0 / Ran 12 / OK            (extra-suite-novo.log) |
| módulo REPROVADO (baseline) | exit 1 / Ran 12 / FAILED (failures=10) / 0 ERROR / 0 skip (extra-suite-baseline-RED.log) |

Ou seja: a MESMA suite nova REPROVA no módulo antigo (RED) e passa no corrigido
(GREEN) — ela mede o defeito, não é fixture-verde. A troca de módulo é feita por
`KIT07F_MODULE=<caminho>` (mesma suite, dois alvos).

## 4. Contra-prova (defeito plantado TEM de reprovar)

    python tools/automacao/kit07/contra_prova_kit07.py
    -> exit 0 / 17 defeitos RECUSOU / CONTROLE_falso_verde RECUSOU
       (12 defeitos da suite do autor + 5 da suite KIT-07F)   (contra-prova-defeitos.log)

Discriminador ESTRITO por defeito: exit 1, conjunto EXATO de `FAIL:`, presença de
`AssertionError`, ausência de `ERROR:`/skip e `Ran N` não vazio.

    python tools/automacao/kit07/contra_prova_kit07.py --individual
    -> exit 0 / 22 alvos RECUSOU / 0 ACERTOU-INDEVIDO / 0 ERROR  (contra-prova-individual.log)

Controle adversarial `falso_verde` RECUSADO (o conjunto de FAIL da mutação não
bate com o alvo declarado diferente).

## 5. Runner completo (porta única)

    bash tools/automacao/kit07/roda_testes_kit07.sh
    -> exit 0 / VEREDITO KIT-07: VERDE      (runner-final.log)

Sequência interna: suite autor 14 OK → suite KIT-07F 12 OK → contra-prova 17
defeitos VERDE → contra-prova individual VERDE. O runner passou a exigir a nova
seção: etapa ausente NÃO é declarada verde (`rc_suite_f` entra no veredito).

## 6. Scanners de credencial

Cópia isolada com `.git` novo LOCAL (sem remote) e `git add` explícito de cada
arquivo (nunca `-A`): `scratch/kit/KIT-07F-run640/scanner-check/`.

| Caso | check_segredos.py | check_padroes_segredo.py |
|---|---|---|
| arquivos alterados (nominal) | exit 0 | exit 0 |
| credencial FICTÍCIA plantada (`planted.txt`) | exit 1 (aponta `planted.txt`, valor `<REDACTED>`) | exit 1 (FORMATO token do Thunderstore) |

Planta removida do índice e do disco ao final; `git remote -v` vazio.
`tools/automacao/offline/aut3_lib.py` permanece com o hash da revisão.

## 7. Hashes vivos

| Arquivo | sha256 |
|---|---|
| tools/automacao/kit07/exportador.py | `98fce3ff8e2c9c8a026ce1e7693bfdf5bc66ab523a92a0acc94cb4725c02578c` |
| tools/automacao/kit07/teste_exportador_kit07f.py (novo) | `181c66bdd1850374b929f6968715d81453cf86130f680014fa8041ed7e0c8f78` |
| tools/automacao/kit07/contra_prova_kit07.py | `df7ad28074d6015a63cfd5598f576fe11edc2e4a3222efed9be63d5f156df9e7` |
| tools/automacao/kit07/roda_testes_kit07.sh | `54bfc7242fc9c0928939349c650aeea89d27e23d0f5f9b36cf7d5eca381f6601` |
| tools/automacao/kit07/teste_exportador_kit07.py (INALTERADA) | `2dc7ea39e0834041f7176969aced4c58a19be200e4c84137289b895f65fb4f51` |
| tools/automacao/offline/aut3_lib.py (INALTERADA) | `04f37b8e285ad7d429d0d01cd846523323ca0a403ce64203890e3c0538d6dc1a` |
| docs/automacao/KIT-07F-parte01..04.md, KIT-07F-entrega-final.md | ver verification-final.json |

`tools/automacao/kit07/` é diretório novo no repositório (untracked); a linha de
base do autor (`exportador.py.baseline-c5fc715b`) está preservada no run dir.

## 8. Limites / invariantes declarados

- Runtime, pixels de PNG reais, desempenho e interferência: NAO_EXERCITADO — o
  escopo é offline e sintético; nenhum jogo/save foi aberto.
- Filesystem links/races: a RECUSA de link (arquivo e diretório) na limpeza é
  testada; corrida de substituição entre processos não foi exercitada.
- Anonimato/segredo NÃO são universais: a cobertura é por FORMA (rótulo genérico
  + formatos conhecidos de prefixo + minimização de dado pessoal). O que não casar
  formato continua sendo decisão humana; PNG nunca é sanitizado automaticamente.
- Scanners cobrem os padrões/arquivos selecionados da cópia, não exportações
  arbitrárias.
- Este run NÃO altera mod, save, Assembly-CSharp.dll, nem publica/deploya; o gate
  humano permanece inalterado e a revisão independente é obrigatória.
