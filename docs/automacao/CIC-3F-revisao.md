# CIC-3F — revisao independente (round 1 / lente ARTIFACT)

Cartao: t_fa708909. Implementador: worker default, run 694. Revisor: instancia nova, run 697
(sessao distinta, sem contato com o implementador). Data: 2026-10-10. Escopo: SOMENTE OFFLINE.

Veredito: **APROVADO** (kanban_complete). Nenhum arquivo de implementacao foi editado pelo revisor.

## 1. O que foi revisado

Unico arquivo de implementacao alterado (conferido por `git diff` frio + `git status`):

    tools/automacao/cenarios/test_rstv.py
      460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262 (== HEAD, o do cartao)
      -> d2d0f218592172cd430359432d41dce8257c4b66188ae0e166f57b0b88787717

Diff: 60 insercoes / 4 remocoes, CONFINADO ao bloco (3) de `_integracao_cic5` (uma unica hunca).
Nenhuma outra mudanca de escopo. `_fecha`, o filtro de alvo e as primitivas ficaram intactos.

SHA conferidos pelo revisor (inalterados, iguais aos do cartao):

    tools/automacao/cenarios/rstv.py                                      f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7
    tools/automacao/runtime/coletor.py                                    159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d
    tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json     bb37d9a2e4fddec8d955aa5b1354e6672d45063fe8256fb616b25c17d7262754

Confirmado o diagnostico do cartao: a fixture REAL do probe mede `owners =
com.gumatos.bettertooltips,com.gumatos.betterfont`, e `rstv.MOD_GUIDS =
("com.gumatos.roguelikeskilltreevisualizer",)` — ou seja, nao e alvo do RSTV pelo filtro
KIT-R0F (`_e_alvo`), que so exclui o que DECLARA nao ser alvo.

## 2. Reproducao independente (execucao propria, nao releitura)

Sandbox propria do revisor, fora do repositorio:
`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cic3f-rev697/sb` (copia de `tools/`, sem `.git`).

    [R1] RED pre-existente — suite do HEAD (460ef...) x rstv.py vivo (f8d0aad...)
         RESULTADO|REPROVOU|cic3-rstv|hash_fonte == dll_sha tem de amarrar a build
           (integracao CIC-5/R-1): esperado 'OK', obtido 'NAO_EXERCITADO'
         EXIT=1   (mensagem identica a do cartao; stderr vazio; sandbox sem .git)

    [R2] suite CORRIGIDA (d2d0f218) no MESMO sandbox sem .git
         RESULTADO|PASSOU|cic3-rstv|...
         EXIT=0      -> o vermelho de fronteira esta fechado.

    [R3] DISCRIMINACAO DO FILTRO (isca propria): `_e_alvo` neutralizado (`return True, None`)
         na copia do sandbox, suite corrigida -> 
         RESULTADO|REPROVOU|cic3-rstv|observacao de OUTRO mod
           (com.gumatos.bettertooltips,com.gumatos.betterfont) nao e alvo do RSTV:
           NAO_EXERCITADO, nunca OK: esperado 'NAO_EXERCITADO', obtido 'OK'
         EXIT=1      -> a sub-caso (3a) e trava REAL, nao decorativa.
         Restauracao: `diff -q` vazio; sha do rstv.py do sandbox volta a f8d0aad... (byte a byte).

    [R4] DISCRIMINACAO DO CONTRATO DE HASH (isca propria): `divergentes = []` em `_fecha`
         (divergencia de hash ignorada) -> suite corrigida REPROVOU, EXIT=1
         ("hash_fonte divergente -> INDETERMINADO: esperado 'INDETERMINADO', obtido
          'NAO_EXERCITADO'"). Restauracao byte a byte conferida (sha f8d0aad...).

    [R5] Sonda propria de estados (script do revisor, le o rstv.py/coletor.py do repo sem editar
         nada, reproduz a cadeia real probe -> coletor.normalizar_observacao -> avaliar):
         docs/automacao/CIC-3F-revisao.md evidencia: sonda.log
         V1 alvo RSTV explicito + hash_fonte == dll_sha           -> OK
         V2 alvo RSTV + hash_fonte DIVERGENTE ("b"*64)            -> INDETERMINADO  (nunca OK)
         V3 alvo RSTV + hash_fonte == fonte_sha (convencao antiga) -> INDETERMINADO  (nunca OK)
         V4 alvo RSTV + hash_fonte AUSENTE                        -> NAO_EXERCITADO (dado incompleto)
         V5 owners ALHEIOS (fixture real) + hash correto          -> NAO_EXERCITADO (excluido por ALVO)
         V7 alvo RSTV + defeito '*0' no render                    -> REPROVADO      (filtro nao suprime defeito)
         V8 alvo RSTV + hash_dll contraditorio na mesma obs (F5)  -> INDETERMINADO  (nunca OK)
         V9 INATIVO + owners RSTV + hash correto                  -> NAO_EXERCITADO (excluido por INATIVO)
         SONDA|PASSOU|contrato de hash discrimina sobre alvo explicito; filtro exclui
                      nao-alvo e INATIVO

  => o caso que prova os hashes (3c) e' load-bearing: com hash divergente/ausente/convencao
     antiga o MESMO alvo NAO fecha OK. A prova do contrato nao virou decorativa.

## 3. Suite e costura reexecutadas (no repositorio, apos o ajuste)

    python tools/automacao/cenarios/test_rstv.py                 PASSOU  EXIT=0
    python tools/automacao/cenarios/test_rstv.py --contra-prova   PASSOU  EXIT=0
        ("isca 'sempre OK' deixou os 10 controles passarem (o REPROVADO real vem da regra)")
    python tools/automacao/cenarios/test_kit09.py                 PASSOU  EXIT=0
    python tools/automacao/cenarios/test_tooltips_shrines.py      TOTAL|rodaram=28 reprovaram=0 nao_rodaram=0  EXIT=0
    python tools/check_segredos.py                                EXIT=0
    python tools/check_padroes_segredo.py                         EXIT=0
    python tools/check_dupes.py                                   EXIT=0
    python tools/audita_docs.py                                   EXIT=0

## 4. Mapa aceite -> evidencia (refutacao tentada em cada item)

1. Quem e alvo x outro mod/boot/inativo declarado em cada caso -> sub-casos (3a)-(3g) com
   comentario e assertivas explicitas; refutado por leitura fria do diff (uma hunca, so o bloco 3).
2. Caso que prova hashes com alvo LEGITIMO explicito -> (3c); refutacao propria: V1/V2/V3/V4
   mostram que o estado OK depende do hash correto. NAO_EXERCITADO explicado aparece para
   nao-alvo (3a: motivo nomeia os owners alheios) e INATIVO (3b: motivo "INATIVO").
3. Sem promover fixture real a runtime -> fixture com SHA intacto; bloco (1) segue exigindo
   `status=FIXTURE`/exit2 e bloco (2) segue exigindo "formato REAL do coletor (fixture) NAO pode
   fechar OK"; `procedencia=fixture` preservado.
4. Demonstrar: hash divergente (V2/V8, caso 3g), ausente (V4, caso 3f), owners errados (V5, caso 3a),
   inativo (V9, caso 3b), alvo com DEFEITO REPROVADO (V7, caso 3d), dado incompleto nunca OK (V4, 3f) -> OK.
5. RED especifico + restauracao byte a byte -> R1/R3/R4, todas com sha de volta a f8d0aad...
6. Nao substituir protecao por sempreOK, nao remover/alargar filtro -> diff nao toca `_fecha` nem
   `_e_alvo`/`MOD_GUIDS`; `rstv.py` com SHA identico ao do cartao; contra-prova ainda discrimina.

Nenhuma regressao nao relacionada: unico arquivo de implementacao alterado nos ultimos minutos e
`test_rstv.py` (+ os relatorios CIC-3F novos); o teste de outro mod (tooltips/shrines) segue 28/0/0.

## 5. Ressalvas (nao bloqueiam)

* Sub-casos (3e)/(3f)/(3g) afirmam `estado != "OK"` (nao o estado exato). O estado exato
  (INDETERMINADO / NAO_EXERCITADO) e' coberto pelo caso 7 da suite e pela sonda R5. Preferencia
  de robustez, nao defeito.
* (3a) le `norm[0]["campos"]["owners"]["valor"]` direto da forma normalizada do coletor: se o
  coletor mudar de forma, o teste falha com KeyError (ruidoso, nao silencioso) — aceitavel.
* Limites: runtime/UIUX/desempenho/build/deploy/publicacao NAO_EXERCITADO; nada de produto/mod/
  gameplay/Bard/Assembly-CSharp; sem segredos neste parecer nem nos relatorios do autor.

## 6. Evidencia do revisor (durable, em repo `scratch/` git-ignorado)

    scratch/kit/CIC-3F-run697/sonda_revisor.py               c30b214015ea255fdd995161e045c3a441e8e76cbbb524907865181b493fb676  (sonda R5)
    scratch/kit/CIC-3F-run697/sonda.log                      0bf53756ac530413fc8a89c53ac62815182c0c1e4f04a945bf02a59b34d45237  (saida R5)
    scratch/kit/CIC-3F-run697/R1-red-preexistente.log        60cac981e9d9045a9dc63ba3106928b73009a877623856bea7185f2239af739a
    scratch/kit/CIC-3F-run697/R2-suite-corrigida.log         1b09b9e01bb73b8c90d71ca8487bd81234ade7c439edd5331683d1e72f1b84e6
    scratch/kit/CIC-3F-run697/R3-isca-filtro-removido.log    028762c5b01502ce9afe982c4fbc6f6b2fbc423e557e6db86db2eab55426d2f2
    scratch/kit/CIC-3F-run697/R4-isca-hash-ignorado.log      57f325ec75e52a3ccf745f02a97b5ae74b31d4632b7d9fe39640ca1367590eb5

Copia de trabalho usada nas provas R1-R4 (fora do repositorio, pode ser descartada):
`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cic3f-rev697/sb/`.

Reproducao das provas do revisor (nao depende de nada acima alem do repo):

    mkdir -p <sandbox>; cp -r tools <sandbox>/            # copia de tools/, sem .git
    git show HEAD:tools/automacao/cenarios/test_rstv.py > <sandbox>/tools/automacao/cenarios/test_rstv.py
    (cd <sandbox> && python tools/automacao/cenarios/test_rstv.py)          # R1 -> EXIT=1
    cp tools/automacao/cenarios/test_rstv.py <sandbox>/tools/automacao/cenarios/   # suite corrigida
    (cd <sandbox> && python tools/automacao/cenarios/test_rstv.py)          # R2 -> EXIT=0
    python scratch/kit/CIC-3F-run697/sonda_revisor.py C:/dev/stolen-realm   # R5 -> SONDA|PASSOU, EXIT=0

