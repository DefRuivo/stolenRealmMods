# KIT-12 revisao rodada 2 (run670) — parte04: ACHADO BLOQUEANTE F5 (contrato do produtor vivo)

O aceite do cartao exige "Hash/versao/config/sessao atravessam toda cadeia" e "evidencia identifica
... versao, hash DLL/fonte/config quando pertinente". A correcao F1 da rodada 2 introduziu uma
CONFRONTACAO da coleta (`confrontar_coleta`, integracao.py l.493) — mas ela foi ligada ao campo
canonico ERRADO. Medido, nao inferido.

## O que o produtor vivo escreve

Contrato do coletor/probe, lido no proprio codigo e na evidencia REAL de runtime:

    tools/automacao/runtime/coletor.py:636-637
      "O hash de fonte e o sha256 da DLL do probe (medido em disco, nunca 'compila igual')."
    tools/automacao/runtime/coletor.py:651-652
      if not ident["hash_fonte"]:  ident["hash_fonte"] = ident["dll_sha256"]
    tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs:180   _res["hash_fonte"] = _hashFonte.Value
    docs/automacao/AUT-4-evidencias/r3-confirmada/aut4probe.json   (EVIDENCIA REAL)
      hash_fonte              = 407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7
      identidade.hash_dll_do_probe = 407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7
      identidade.arquivo_dll_do_probe = ...\BepInEx\plugins\AUT4Probe\AUT4Probe.dll
    + a convencao esta escrita no repo em 4 lugares:
      tools/automacao/ciclo/test_decisao.py:562-563  ("o `hash_fonte` do coletor CIC-5 e o sha da DLL,
        entao uma rodada coerente declara hash_fonte == dll_sha")
      tools/automacao/aut6/cobertura.py:270-277      (alias `hash_fonte`/`hash_dll` -> `dll_sha`)
      tools/automacao/aut5/test_aut5.py:563          ("hash_fonte": ident["dll_sha"])
      tools/automacao/cenarios/kit09-verdade.entrada.json  ("`hash_fonte` segue o contrato REAL do
        coletor CIC-5 (sha256 da DLL do probe) e por isso casa com `dll_sha`")

Ou seja: **`coleta.hash_fonte` e o sha256 da DLL do PROBE** (o instrumento), nao o hash dos
arquivos-fonte do mod.

## F5 (BLOQUEANTE) — a confrontacao compara com `ident["fonte_sha"]`, que nenhum produtor vivo popula

`integracao.py` `confrontar_coleta` (l.493-511) e `criterios_da_cadeia` bloco `(2c)` (l.656-672)
comparam `coleta_meta["hash_fonte"]` com `ident["fonte_sha"]`, e `ident["fonte_sha"]` vem de
`ciclo.identidade(repo)` = hash dos ARQUIVOS-FONTE do mod (`fonte_arquivos: 526`), enquanto
`ident["dll_sha"]` e o hash da DLL do MOD (`dlls.BetterStats`). Nenhum deles e a DLL do probe.

Sonda S11 (minha) — envelope escrito EXATAMENTE como o produtor vivo escreve
(`hash_fonte` = sha256 da DLL do probe em disco, `identidade.hash_dll_do_probe` igual):

    estado INCOMPLETO | exit 2 | OK 0
    fonte_sha da rodada (arquivos-fonte do mod)     9df43f9484bce469
    dll_sha da rodada (DLL do mod)                  f4805186c7b7859d
    hash_fonte declarado pela coleta (DLL do probe) 564e6ec3eb112b22
    lacunas: ['cadeia/coleta-contraditoria/hash_fonte']
    motivo: "coleta declara hash_fonte 564e6ec3eb112b22 mas a identidade da rodada e
             9df43f9484bce469: a coleta refere OUTROS bytes (procedencia CONTRADITORIA);
             nada desta coleta aprova"

Efeito: uma coleta LEGITIMA (a unica forma que o probe/coletor sabe produzir) e sempre rebaixada a
"procedencia CONTRADITORIA" e a rodada inteira cai para INCOMPLETO. A costura, como entregue, **nao
consegue aprovar nenhuma rodada real** — falha fechada ao contrario do defeito da rodada 1, mas
igualmente nao operavel. Pior: o unico `hash_fonte` que ela aceita como "confere" e aquele que
declara o hash dos ARQUIVOS-FONTE do mod (sonda S9), que o produtor nunca escreve.
S10 (mesma raiz) completa o quadro: campos que a coleta declare a mais (`dll_sha`/`config_sha`/
`versao`) nao sao lidos nem confrontados (`carregar_coleta` l.376-378 so carrega
`caminho/sessao/hash_fonte/fixture/quantidade/envelope/erro`) — medido: coleta com
`hash_fonte` da rodada e `dll_sha`/`config_sha`/`versao` estranhos -> APROVADO_OFFLINE/exit 0.

## Por que a suite nao pegou isso

`prove_ciclo.py` `coleta()` (l.92-105) e `test_kit12_integracao.py` escrevem `hash_fonte` = hash dos
ARQUIVOS-FONTE da rodada (a convencao da implementacao, nao a do produtor). Com o fixture
auto-consistente, `Ran 24 tests OK` e `PROVA|PASSOU` passam sem tocar o contrato real. Fixture
exercita o avaliador; ela nao comprova o envelope do coletor — exatamente a distincao que o proprio
cartao faz ("fixture nao comprova runtime").

## Correcao minima exigida (F5)

1. Ligar a confrontacao ao campo canonico que o produtor vivo popula: confrontar o que a coleta
   declara (`hash_fonte`) contra a identidade que a rodada possui para a DLL do probe — carregando
   `dll_probe_sha` na identidade da cadeia — OU aceitar explicitamente o alias documentado pelo
   repo (`hash_fonte` == `dll_sha`) em vez de `fonte_sha`, sem deixar ambiguidade de campo.
2. Alinhar os fixtures (`prove_ciclo.py`, `test_kit12_integracao.py`) ao envelope REAL do produtor e
   derivar o teste do contrato (usar como entrada o `docs/automacao/AUT-4-evidencias/r3-confirmada/
   aut4probe.json`), de modo que o teste FALHE se a confrontacao voltar a ser ligada em `fonte_sha`.
3. Manter a trava de bytes estranhos: envelope com hash que nao casa com NENHUM campo da identidade
   continua INCOMPLETO/exit 2; envelope conforme NAO pode ser rebaixado.
4. Confrontar tambem os campos adicionais que a coleta declare (`dll_sha`/`config_sha`/`versao`) ou
   declarar esse limite no proprio modulo (S10).
