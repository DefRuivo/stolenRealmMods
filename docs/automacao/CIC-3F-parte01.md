# CIC-3F — parte 01 — inventario e causa raiz (offline)

Cartao: t_fa708909 (CIC-3F: Reconciliar fixture da suite RSTV com filtro de alvo sem enfraquecer travas)
Autor: worker default, run 694. Data: 2026-10-10.
Escopo: SOMENTE OFFLINE. Sem produto/mod/gameplay/Bard/Assembly-CSharp; sem build/deploy/probe/jogo.
Runtime/desempenho/UIUX: NAO_EXERCITADO.

## 1. SHA256 dos vivos (conferidos nesta rodada)

- tools/automacao/cenarios/test_rstv.py = 460ef5356dd927677c9ea26ac36ec91adfcbf3c20fec6e258b2aeb904a7e0262
  (confere com o cartao)
- tools/automacao/cenarios/rstv.py = f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7
  (confere com o cartao)
- tools/automacao/runtime/coletor.py = presente (SHA a registrar na parte 02; o cartao cita
  159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d)
- tools/automacao/runtime/fixtures/probe-saida-exemplo.entrada.json =
  bb37d9a2e4fddec8d955aa5b1354e6672d45063fe8256fb616b25c17d7262754 (confere com o cartao)

## 2. Achado a reconciliar

A suite `tools/automacao/cenarios/test_rstv.py`, no caso "cic3-rstv", guarda a expectativa
`hash_fonte == dll_sha` (integracao CIC-5 / regra R-1). Em sandbox sem `.git` o caso da
`NAO_EXERCITADO` (exit 1) porque a fixture do probe declara `owners` de bettertooltips/
betterfont, isto e, objetos que NAO sao alvos do RSTV.

O filtro KIT-R0F (`_e_alvo`/`_selecionar_alvos` em rstv.py) e legitimo e EXCLUI de forma
conservadora apenas o que declara explicitamente nao ser alvo:
- objeto INATIVO na hierarquia;
- `owners` nao vazio SEM o GUID do mod sob teste (objeto de outro mod/boot).

Portanto o vermelho nao e regressao do kit09.py; e um descompasso entre (a) a fixture/expectativa
do caso CIC-3 e (b) o filtro de alvo real. A trava NAO pode ser enfraquecida (nada de sempreOK,
nada de remover/alargar o filtro) — o ajuste correto e declarar em cada caso QUEM e alvo RSTV e
quem e outro mod/boot/inativo, mantendo a protecao.

## 3. Proximo passo

- parte 02: ler o caso `cic3-rstv` de test_rstv.py e as fixtures `rstv-*.entrada.json`,
  mapeando owners declarados x expectativa.
- parte 03: reproduzir o RED especifico (exit/stdout/stderr/paths) sem alterar o vivo.
- parte 04+: ajuste minimo + suite verde + costura test_kit09.py + restauracao byte a byte.

Artefato gerado por write_file (verified). Sem segredos.
