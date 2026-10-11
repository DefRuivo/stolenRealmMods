# KIT-12G — correcao da rodada 3 (F5 da revisao run670)

Tarefa: t_0a434c97 · implementador: run671 · autorizacao do dono 07/10/2026 (implementacao/revisao
OFFLINE, fila serial). HEAD base: d82894e. Runtime/jogo/build/deploy/publicacao: NAO_EXERCITADO.

## 1. O que o revisor run670 mediu (F5, bloqueante)

`tools/automacao/kit12/integracao.py`, `confrontar_coleta` (l.493-511) e bloco `(2c)` de
`criterios_da_cadeia` (l.656-672) comparam

    coleta_meta["hash_fonte"]   x   ident["fonte_sha"]

mas o PRODUTOR VIVO escreve em `hash_fonte` o sha256 da **DLL do INSTRUMENTO (probe)**, nunca o
hash dos arquivos-fonte do mod:

- `tools/automacao/runtime/coletor.py:636-637` — "O hash de fonte e o sha256 da DLL do probe
  (medido em disco, nunca 'compila igual')"; `:651-652` — `hash_fonte = dll_sha256` do probe.
- `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs:180` — `_res["hash_fonte"] = _hashFonte.Value`.
- Evidencia REAL `docs/automacao/AUT-4-evidencias/r3-confirmada/aut4probe.json`:
  `hash_fonte == identidade.hash_dll_do_probe == 407c5c63…`, medido da DLL
  `…\BepInEx\plugins\AUT4Probe\AUT4Probe.dll` (`bytes_dll_do_probe = 50176`).
- Convencao escrita no repo: `ciclo/test_decisao.py:562-563` ("o `hash_fonte` do coletor e o sha da
  DLL, entao uma rodada coerente declara `hash_fonte == dll_sha`"), `aut6/cobertura.py:270-277`
  (`_hashes_obs`: alias `hash_fonte`/`hash_dll` -> canonico `dll_sha`), `aut5/test_aut5.py:563`
  (`contexto = {"hash_fonte": ident["dll_sha"]}`), `cenarios/kit09-verdade.entrada.json`
  (`hash_fonte == identidade.dll_sha`).

Consequencia medida nas sondas S10/S11 do revisor: **toda coleta legitima e rebaixada**
(INCOMPLETO/exit 2, lacuna `cadeia/coleta-contraditoria/hash_fonte`) e o **unico valor aceito**
(hash dos arquivos-fonte) e um valor que **nenhum produtor escreve**. A suite nao pegava porque
`prove_ciclo.py:92-105` e o teste declaravam `hash_fonte` = hash dos arquivos-fonte (fixture
auto-consistente com a implementacao, nao com o produtor).

## 2. Correcao a implementar (os 4 itens exigidos no parecer)

1. CONFRONTAR CONTRA O CAMPO CANONICO DO INSTRUMENTO: a identidade da rodada passa a carregar
   `dll_probe_sha` (sha256 da DLL do INSTRUMENTO de coleta), obtido por MEDICAO
   (`--probe-dll <caminho>` ou o arquivo declarado pela coleta em
   `identidade.arquivo_dll_do_probe`, quando existir em disco) e, na falta de medicao, pela
   DECLARACAO canonica da propria coleta (`identidade.hash_dll_do_probe` / `identidade.dll_sha` /
   `dll_sha` de topo), com o alias documentado `hash_fonte == dll_sha` como ultimo recurso
   (`ident["dll_sha"]`). `fonte_sha` NAO confere mais procedencia de coleta.
2. FIXTURE/TESTE DERIVADOS DO ENVELOPE REAL: os campos de
   `docs/automacao/AUT-4-evidencias/r3-confirmada/aut4probe.json` viram a base do envelope de
   prova; teste novo FALHA se a confrontacao voltar a apontar para `fonte_sha`.
3. FAIL-CLOSED PRESERVADO: bytes que nao casam com NENHUM campo da identidade continuam
   INCOMPLETO/exit 2; envelope conforme NAO e rebaixado.
4. S10 (mesma raiz): `carregar_coleta` passa a ler e CONFRONTAR `fonte_sha`/`config_sha`/`versao`/
   `sessao` declarados pela coleta (topo e bloco `identidade`) contra a identidade da rodada;
   contradicao vira lacuna nomeada + rebaixamento. Instrumento apenas DECLARADO (nao medido) fica
   registrado como limite explicito em `coleta.instrumento_origem` e em `limites` — sem rebaixar
   envelope conforme (limite declarado, nao lacuna disfarcada).

## 3. Itens a cobrir (checklist desta rodada)

- [ ] ler `integracao.py` (identidade, carregar_coleta, confrontar_coleta, bloco 2c), `prove_ciclo.py`,
      suite `test_kit12_integracao.py`, envelope real e convencao do produtor (feito — item 1)
- [ ] implementar `dll_probe_sha` na identidade + `--probe-dll` na CLI/API
- [ ] implementar confronto da coleta por campo canonico + alias + declaracao canonica
- [ ] implementar confronto dos campos declarados pela coleta (`fonte_sha`/`config_sha`/`versao`/`sessao`)
- [ ] refazer fixture/`prove_ciclo.py` a partir do envelope REAL (com passo de erro->correcao->revalidacao)
- [ ] suite: testes novos (envelope real confere; rewire para `fonte_sha` FALHA; S10 contradicao; medicao)
- [ ] isca de mutacoes: novas mutacoes discriminadas + controles restaurados
- [ ] provas reais: suite, isca, CLI em sandbox (exits), travas check_segredos/check_padroes_segredo/
      check_dupes/audita_docs
- [ ] entregavel `docs/automacao/KIT-12G-entrega.md` com hashes e limites
- [ ] handoff `kanban_request_review` (implementer/reviewer, resumo+paths+hashes)

NAO vai ser tocado: `pertinencia.json`, CIC-1/CIC-2/CIC-5/KIT-10 (reuso intacto), nenhum arquivo de
mod, nenhuma dependencia compartilhada. Nada de git add/commit/push.
