# CIC-3F — parte 04 — execucao verde, travas repo e SHA (offline)

## 12. Suite alvo apos o ajuste (repositorio real)

    $ python tools/automacao/cenarios/test_rstv.py
    RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK,
      controles reprovam, runtime identifica
    EXIT=0

    $ python tools/automacao/cenarios/test_rstv.py --contra-prova
    CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os 10 controles passarem
      (o REPROVADO real vem da regra)
    EXIT=0

## 13. Costura KIT-09 (test_kit09.py)

    $ python tools/automacao/cenarios/test_kit09.py
    RESULTADO|PASSOU|kit09-rstv|KIT-09: 21 criterios pequenos rastreaveis RSTV;
      fixture/ausente/malformado nunca OK; 21 controles reprovam; handler != clique;
      ativo nao prova obstrucao; dado velho reprova
    EXIT=0

## 14. Teste de OUTRO mod (nao podia quebrar)

    $ python tools/automacao/cenarios/test_tooltips_shrines.py
    TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0
    EXIT=0

## 15. Travas do repositorio

    $ python tools/check_segredos.py        -> EXIT=0 (nenhum padrao de credencial; 874 versionados)
    $ python tools/check_padroes_segredo.py -> EXIT=0 (nenhum padrao de credencial)
    $ python tools/check_dupes.py           -> EXIT=0 (TextFixes 101 / TextAppends 197, sem duplicadas)
    $ python tools/audita_docs.py           -> "nenhuma inconsistencia encontrada", EXIT=0

## 16. Integridade dos vivos (SHA256)

    rstv.py      f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7  (INALTERADO vs cartao)
    coletor.py   159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d  (INALTERADO vs cartao)
    probe-saida-exemplo.entrada.json
                 bb37d9a2e4fddec8d955aa5b1354e6672d45063fe8256fb616b25c17d7262754  (INALTERADO vs cartao)
    test_rstv.py ANTES 460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262 (== HEAD)
    test_rstv.py DEPOIS d2d0f218592172cd430359432d41dce8257c4b66188ae0e166f57b0b88787717 (UNICO alterado)

A fixture real NAO foi promovida a runtime: `procedencia=fixture`/`label` intactos, o caso (2)
continua exigindo ZERO OK no formato real do coletor. Nao houve sempreOK, nem remocao/alargamento
do filtro, nem edicao de produto/mod/gameplay/Bard/Assembly-CSharp. Sem deploy/probe/jogo/save/publicacao.

Limites: runtime/desempenho/UIUX NAO_EXERCITADO (tudo offline).
