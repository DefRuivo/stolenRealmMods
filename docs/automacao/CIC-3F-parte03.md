# CIC-3F — parte 03 — RED especifico e restauracao byte a byte (offline)

Sandbox: `%USERPROFILE%/AppData/Local/hermes/cache/scratch/cic3f` (fora do repositorio).
Nenhum arquivo do repositorio foi mutado para produzir o RED; a mutacao ocorre SO na sandbox.

## 8. RED-A — o vermelho PRE-EXISTENTE (a fronteira do cartao), em sandbox

Copia do `test_rstv.py` do HEAD (SHA 460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262,
identico ao citado no cartao) contra o `rstv.py` VIVO (SHA f8d0aad...):

    $ python tools/automacao/cenarios/test_rstv.py
    RESULTADO|REPROVOU|cic3-rstv|hash_fonte == dll_sha tem de amarrar a build
      (integracao CIC-5/R-1): esperado 'OK', obtido 'NAO_EXERCITADO'
    EXIT=1

Reproduz exatamente a mensagem do cartao. Prova que a causa e a do diagnostico (parte 02), nao
uma suposicao.

## 9. RED-B — as NOVAS travas discriminam (a suite corrigida tem de reprovar sem o filtro)

Sandbox propria com `tools/{testes,automacao/{cenarios,runtime}}`. Copia do `test_rstv.py`
CORRIGIDO contra o `rstv.py` com o filtro NEUTRALIZADO (isca, so na sandbox):

    # mutacao (ancora unica, _e_alvo):
    def _e_alvo(obs, cid, guids=MOD_GUIDS):
        """..."""
        return True, None  # SANDBOX-RED: filtro neutralizado

    $ python tools/automacao/cenarios/test_rstv.py
    RESULTADO|REPROVOU|cic3-rstv|observacao de OUTRO mod
      (com.gumatos.bettertooltips,com.gumatos.betterfont) nao e alvo do RSTV:
      NAO_EXERCITADO, nunca OK: esperado 'NAO_EXERCITADO', obtido 'OK'
    EXIT=1

Ou seja: sem o filtro, um objeto de OUTRO mod fecharia OK — e a nova trava (3a) PEGA isso.
As travas 3a/3b nao sao decorativas: elas discriminam o filtro.

## 10. Restauracao byte a byte

    $ sha256sum tools/automacao/cenarios/rstv.py   (sandbox mutada -> restaurada da copia)
    f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7
    $ diff -q rstv-orig.bak tools/automacao/cenarios/rstv.py
    (diff vazio) -> RESTAURADO BYTE A BYTE

O SHA restaurado e IDENTICO ao do cartao (`f8d0aad...`). A suite corrigida contra o `rstv.py`
restaurado volta a PASSOU/exit0. O `rstv.py` do repositorio NUNCA foi tocado (SHA do repo
conferido inalterado na parte 04).

## 11. Correcao do padrao

O ajuste nao altera `rstv.py` nem o filtro: muda APENAS o caso de teste em
`test_rstv.py`. A protecao (filtro KIT-R0F) fica intacta e passa a ser EXERCITADA pelo caso
CIC-3, com expectativa declarada para alvo e para nao-alvo.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
