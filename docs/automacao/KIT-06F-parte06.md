# KIT-06F — parte 06: testes, prova negativa e cobertura

Suite do autor: 35 -> 45 testes (10 novos de contrato F1-F6); `Ran 45 tests OK exit0`.
Contra-prova: 13 -> 37 defeitos plantados, cada um com o conjunto EXATO declarado.
Cobertura medida por AST: 45/45 testes com pelo menos uma prova negativa (era 18/35).
Nenhum self.fail; nenhum teste enfraquecido.
Autoteste do discriminador: 9/9 exit0.
Runner real `bash tools/automacao/kit06/roda_testes_kit06.sh`: VEREDITO KIT-06:
VERDE (exit0).

Ajustes de expectativa declarados (com contrato, nao ocultando):
- `test_iniciar_duas_vezes_degrada` -> `test_f7_alterna_observacao_liga_desliga`;
- `test_pausa_delega_ao_pipeline`: posse do construtor entra na lista de chamadas;
- `test_contrato_kit07_declarado` -> `test_contrato_kit07_declarado_honesto`.
