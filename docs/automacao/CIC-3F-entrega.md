# CIC-3F — entrega (reconciliacao da fixture RSTV com o filtro de alvo)

Cartao: t_fa708909. Autor: worker default, run 694. Data: 2026-10-10. Escopo: SOMENTE OFFLINE.
Artefatos desta rodada (novos, nao sobrescritos): docs/automacao/CIC-3F-parte01.md,
-parte02.md, -parte03.md, -parte04.md, -entrega.md.

## Resultado em uma frase

O vermelho da fronteira (`hash_fonte == dll_sha tem de amarrar a build`) era o caso CIC-3
provando o contrato de hash sobre um objeto que, pelo filtro KIT-R0F, NUNCA e alvo do RSTV
(a fixture do probe mede objetos de bettertooltips/betterfont). O ajuste da o alvo LEGITIMO e
EXPLICITO ao caso que prova hashes e passa a exigir/registrar a exclusao explicada dos nao-alvos.
O filtro nao foi tocado, nem enfraquecido; `rstv.py`/`coletor.py`/fixture ficam com SHA intacto.

## Unico arquivo alterado

tools/automacao/cenarios/test_rstv.py
  460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262 (== HEAD, o do cartao)
  -> d2d0f218592172cd430359432d41dce8257c4b66188ae0e166f57b0b88787717

Ajuste restrito ao bloco (3) de `_integracao_cic5`, em 7 sub-casos com quem-e-alvo declarado:

  (3a) NAO-ALVO (owners de outro mod, formato REAL do coletor): NAO_EXERCITADO, com motivo
       nomeando os owners alheios e a exclusao por alvo. Nunca OK, nunca REPROVADO.
  (3b) INATIVO: objeto oculto excluido MESMO com owner RSTV -> NAO_EXERCITADO (motivo INATIVO).
  (3c) ALVO RSTV EXPLICITO (owners=[GUID RSTV]): hash_fonte(sha da DLL) == dll_sha -> OK,
       propaga dll_sha e prova_runtime=True.
  (3d) ALVO RSTV com DEFEITO (`*0` no render) -> REPROVADO (filtro nao suprime defeito).
  (3e) convencao ANTIGA (hash_fonte == fonte_sha) no mesmo alvo -> NAO fecha OK.
  (3f) cadeia AUSENTE (sem hash_fonte) no alvo -> NAO fecha OK (dado incompleto).
  (3g) hash DIVERGENTE declarado na mesma observacao (F5) -> NAO fecha OK.

Sem promover a fixture real a runtime: `procedencia=fixture` e o caso (2) "fixture nao fecha OK"
seguem intactos.

## Provas de execucao (exit/stdout/SHA/paths)

RED-A (pre-existente, sandbox, test_rstv.py do HEAD == 460ef... contra rstv.py vivo == f8d0aad...):
  RESULTADO|REPROVOU|cic3-rstv|hash_fonte == dll_sha tem de amarrar a build (integracao CIC-5/R-1):
    esperado 'OK', obtido 'NAO_EXERCITADO'   EXIT=1
RED-B (suite CORRIGIDA contra rstv.py SEM filtro, isca em sandbox):
  RESULTADO|REPROVOU|... "observacao de OUTRO mod (com.gumatos.bettertooltips,com.gumatos.betterfont)
    nao e alvo do RSTV: NAO_EXERCITADO, nunca OK: esperado 'NAO_EXERCITADO', obtido 'OK'"  EXIT=1
  -> as novas travas discriminam o filtro.
Restauracao byte a byte: rstv.py de sandbox volta a f8d0aad... (diff -q vazio).
VERDE: test_rstv.py EXIT=0 PASSOU; --contra-prova EXIT=0; test_kit09.py EXIT=0 PASSOU;
  test_tooltips_shrines.py EXIT=0 (28/0/0); travas repo check_segredos/check_padroes_segredo/
  check_dupes/audita_docs todas EXIT=0.

Sandboxes (fora do repositorio): %USERPROFILE%/AppData/Local/hermes/cache/scratch/cic3f/{red,red-antigo}.

## Integridade

rstv.py / coletor.py / probe-saida-exemplo.entrada.json: SHA identicos ao cartao (inalterados).
test_rstv.py: unico alterado (antes == HEAD 460ef...; depois d2d0f218...).

## Limites e garantias

SOMENTE OFFLINE. Sem produto/mod/gameplay/Bard/Assembly-CSharp; sem deploy/probe/jogo/navegacao/
save/publicacao; politicas/modelos/crons/prioridades inalterados. Runtime/desempenho/UIUX
NAO_EXERCITADO. Sem sempreOK, sem remocao/alargamento do filtro, sem promover fixture a runtime.
Sem segredos em logs/handoff. Reutilizadas as primitivas/suite existentes (nenhuma infra nova).

## Pendencia

Revisao INDEPENDENTE por instancia nova no MESMO cartao (kanban_request_review), conforme o aceite.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
