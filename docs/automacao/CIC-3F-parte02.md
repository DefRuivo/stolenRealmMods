# CIC-3F — parte 02 — causa raiz confirmada e plano do ajuste (offline)

## 4. Causa raiz (confirmada por execucao)

Caso que reprova: `test_rstv.py -> _integracao_cic5`, bloco (3), linha 598:
`por_id(R.avaliar([obs_rt], ident_cic5), "RSTV-26-placeholders")` esperando `OK`.

`obs_rt = dict(norm[0])` onde `norm[0]` e a normalizacao REAL da fixture do probe
(`probe-saida-exemplo.entrada.json`), objeto `Tooltip.Title`, cujos `owners` (REAIS) sao
`com.gumatos.bettertooltips` e `com.gumatos.betterfont` — NENHUM e o GUID do mod sob teste
(`com.gumatos.roguelikeskilltreevisualizer`).

O filtro KIT-R0F (`rstv.py::_e_alvo`) entao exclui a observacao, corretamente:

    estado obtido = NAO_EXERCITADO
    motivo        = "... 1 observacao(oes) NAO-alvo excluida(s):
                     1 x sem owner do mod sob teste (owners=com.gumatos.bettertooltips,...)"

Logo o vermelho NAO e regressao do kit09.py: e o caso CIC-3 provando um contrato de hash
sobre um objeto que, pelo filtro real, NUNCA e alvo do RSTV. A trava de alvo esta CERTA; era
o CASO que faltava declarar quem e alvo.

## 5. Diagnostico por sonda (execucao, nao leitura)

Sonda offline (`.../scratch/cic3f/probe.py`) usando o `rstv.py` e o `coletor.py` REAIS:

    SEM owner  -> NAO_EXERCITADO | motivo nomeia os owners alheios e a exclusao por alvo
    COM owner RSTV (top-level) -> OK | dll_sha propagado == identidade
    COM owner RSTV + hash_fonte == fonte_sha (convencao antiga) -> INDETERMINADO

Ou seja: injetar o GUID do RSTV como owner explicito torna a observacao um ALVO LEGITIMO e
o contrato de hash volta a fechar OK — sem tocar no filtro e sem promover a fixture a runtime.

## 6. Ajuste proposto (minimo, preserva a protecao)

Somente em `tools/automacao/cenarios/test_rstv.py`, bloco (3) de `_integracao_cic5`:

- (3a) NAO-ALVO: a observacao REAL (owners de outro mod) com a MESMA cadeia -> expectativa
  NAO_EXERCITADO EXPLICADA (motivo nomeia os owners e a exclusao por alvo). Nada de OK.
- (3b) INATIVO: objeto oculto na hierarquia e excluido mesmo com owner RSTV -> NAO_EXERCITADO
  com motivo INATIVO (filtro conservador intacto).
- (3c) ALVO RSTV EXPLICITO (`owners=[GUID RSTV]`): hash_fonte do coletor == dll_sha amarra a
  build -> OK e propaga dll_sha (o caso que prova hashes ganha alvo legitimo explicito).
- (3d) ALVO RSTV real com DEFEITO (`*0` no render) -> REPROVADO (nao se suprime defeito).
- (3e) convencao ANTIGA (`hash_fonte == fonte_sha`) no MESMO alvo -> NAO fecha OK.
- (3f) cadeia AUSENTE (sem hash_fonte) no alvo explicito -> NAO fecha OK (dado incompleto).
- (3g) hash DIVERGENTE declarado na mesma observacao -> NAO fecha OK.

Proibido no ajuste: sempreOK, remover/alargar o filtro, marcar a fixture como runtime,
tocar em outros mods/testes.

## 7. Provas a produzir (partes 03+)

- RED especifico: suite corrigida contra um `rstv.py` SANDBOX com o filtro neutralizado
  (`_e_alvo` sempre True) -> as travas (3a)/(3b) tem de REPROVAR (discriminam).
- Restauracao byte a byte do `rstv.py` da sandbox (SHA f8d0aad...).
- Suite real exit0 (Ran N tests) + costura `test_kit09.py` exit0.
- SHA dos vivos inalterados; revisor independente no mesmo cartao.
