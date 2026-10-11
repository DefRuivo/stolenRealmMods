# KIT-07F — correção F1–F9 (parte 02: linha de base RED, reprodução do parecer)

## Objetivo

Reproduzir, sem tocar nos artefatos da revisão (run636), os 15 FAIL da suite
independente de 24 testes no módulo REPROVADO, para que o GREEN posterior seja
comparável item a item.

## Método

- Baseline isolada: `scratch/kit/KIT-07F-run640/baseline/` — cópia da suite
  independente (`test_review_kit07.py`) + `isolated/` com o módulo reprovado
  (`exportador.py` sha256 `c5fc715b083685ec209138d0dc56e0f9dc19abcabd9e430493746d6f2a625382`,
  idêntico ao auditado) e `aut3_lib.py` (`04f37b8e…dc1a`). Sem `.git`, sem perfil,
  sem credencial. Nada em `scratch/kit/KIT-07R-run636` foi escrito nesta correção.
- Linha de base da entrega do autor (hash original) preservada em
  `scratch/kit/KIT-07F-run640/exportador.py.baseline-c5fc715b`.

## Comando e resultado

    python scratch/kit/KIT-07F-run640/baseline/test_review_kit07.py
    -> exit 1 / Ran 24 tests / FAILED (failures=15) / zero ERROR / zero skip

Os 15 nomes de FAIL batem exatamente com o parecer KIT-07R:

    test_F1_filename_secret_absent_package_and_manifest
    test_F1_personal_metadata_minimized
    test_F2_escaped_quote_secret_redacted_valid_json
    test_F2_punctuation_key_secret_redacted
    test_F3_destination_inside_source_rejected
    test_F3_same_source_destination_rejected
    test_F4_reexport_png_off_removes_old_image
    test_F4_reexport_removed_log_absent
    test_F5_reserved_names_do_not_invalidate_hash
    test_F6_invalid_marker_does_not_authorize_delete
    test_F7_failed_export_not_partial
    test_F7_output_size_limit_actual
    test_F7_sanitized_expansion_perfile_limit
    test_F8_cli_io_error_never_leaks_prefix
    test_F9_selected_bepinex_log_not_discarded

Log preservado: `scratch/kit/KIT-07F-run640/baseline/review-baseline.log`.

## Leitura

- Baseline RED reproduzida 15/24 com os MESMOS nomes do parecer (nenhum achado
  foi "esquecido" nem trocado por outro).
- Os 9 testes que já passavam continuam passando (não houve compensação de
  cobertura): a correção precisa manter os 9 e virar os 15.
