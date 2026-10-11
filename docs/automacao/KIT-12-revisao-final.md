# KIT-12 — parecer final da revisao independente rodada 2 (run670) — REQUER CORRECAO (F5)

Cartao: `t_0a434c97` (KIT-12). Rodada 1 = run668 (lente Artifact, pediu F1/F2) -> implementador
run669 corrigiu e pediu reconferencia -> esta rodada 2 = run670 (lente EXECUTION: checkout e
execucao propria de tudo, nao releitura do handoff). Revisor run670 != implementador run669 !=
revisor run668. **Nenhum arquivo de produto foi editado por mim.**

Partes deste parecer: `KIT-12-revisao-final-parte01.md` (metodo), `-parte02.md` (hashes, suite,
isca, CLI), `-parte03.md` (sondas proprias, travas, escopo), `-parte04.md` (achado F5).
Provas: `scratch/kit/KIT-12R-run670-rev/` — `repository` copia isolada
(`repo/`), `suite-run670.txt`, `isca-run670.txt`, `cli-run670.txt` + `cli-run670/prova.json`,
`sondas_run670.py` + `sondas-run670-saida.txt` + `sondas-run670.json`, `sonda-s10/11*.json`,
`*-run670.txt` (travas). O diretorio da rodada 1 (`KIT-12R-run668-rev/`) NAO foi sobrescrito.

## Veredito por criterio

| # | Item | Verificacao REAL (comando/medida) | Veredito |
|---|---|---|---|
| A0 | hashes do handoff | sha256sum 4/4 batem (integracao.py ae61678c…) | PASSOU |
| A1 | suite | `python repo/tools/automacao/kit12/test_kit12_integracao.py` -> `Ran 24 tests OK` exit 0 | PASSOU |
| A2 | isca/mutacao | `--isca` -> `mutacoes_discriminadas=9/9`, `controle_restaurado exit=0`, sem skip | PASSOU |
| A3 | CLI sandbox | `prove_ciclo.py` -> exit 2/1/2/2/3, `PROVA\|PASSOU`, `problemas=[]` | PASSOU |
| F1a | coleta com hash de outros bytes | sonda S2: era APROVADO/exit 0 -> **INCOMPLETO/exit 2**, OK=0, lacuna `cadeia/coleta-contraditoria/hash_fonte` | PASSOU |
| F1b | coleta sem `hash_fonte` | sonda S2b: **INCOMPLETO/exit 2**, lacuna `cadeia/coleta-ausente/hash_fonte` | PASSOU |
| F1c | criterio declarando bytes antigos | sonda S8: cru = REPROVADO; pela costura = **INCOMPLETO/exit 2**, criterio NAO_EXERCITADO, `declaracoes_contraditorias` preserva o declarado | PASSOU |
| F1d | contra-prova (nao virou trava cega) | sonda S9: coleta declarando o hash DA RODADA -> `APROVADO_OFFLINE`/exit 0, `confere` | PASSOU |
| F2 | campo executavel | sondas S1 e S1b: `campos_residuais_no_criterio=[]`, `criterio_sanitizado=true`, 3 propostas registradas; `culpados=[]` em `criterios` e `fila_correcao` da cadeia inteira | PASSOU |
| T1 | travas do repo | check_segredos / check_padroes_segredo / check_dupes / audita_docs -> exit 0 cada | PASSOU |
| **F5** | **confrontacao da coleta ligada ao campo canonico ERRADO** | sonda S11: envelope escrito como o produtor vivo escreve (`hash_fonte` = sha256 da DLL do probe, cf. `coletor.py:636`, `AUT4ProbePlugin.cs:180` e a evidencia real `AUT-4-evidencias/r3-confirmada/aut4probe.json`) -> **INCOMPLETO/exit 2**, `cadeia/coleta-contraditoria/hash_fonte` | **FALHOU** |
| F10 | campos extras declarados pela coleta | sonda S10: coleta com `hash_fonte` correto e `dll_sha`/`config_sha`/`versao` estranhos -> APROVADO_OFFLINE/exit 0 (nao sao lidos nem confrontados) | FALHOU (mesma raiz de F5; registrar/declarar limite) |
| F3/F4 | dividas da rodada 1 (REPROVADO incoerente; `--verificar` sem `--config`) | mantidas como divida declarada, fail-closed; nao bloqueiam | DIVIDA |

F1 (como especificado na rodada 1) e F2 estao entregues e reproduzidos por execucao propria: a
sobrescrita silenciosa acabou, o rebaixamento e fail-closed, o valor declarado fica preservado e o
campo executavel sai do criterio e do item da fila. A suite e a isca nao sao carimbo: cada mutacao
nova derruba o teste-alvo (exit 1 = detectada) e o controle volta a exit 0.

## Bloqueante F5 (detalhe completo em `-parte04.md`)

A correcao introduziu a confrontacao da coleta, mas ligou-a em `ident["fonte_sha"]` (hash dos
ARQUIVOS-FONTE do mod). O produtor vivo — probe AUT4Probe + `tools/automacao/runtime/coletor.py` —
escreve em `hash_fonte` o **sha256 da DLL do probe**; o repo documenta esse contrato em
`ciclo/test_decisao.py:562-563`, `aut6/cobertura.py:270-277`, `aut5/test_aut5.py:563`,
`cenarios/kit09-verdade.entrada.json` e na evidencia real de AUT-4. Consequencia medida (S11): toda
coleta LEGITIMA cai em "procedencia CONTRADITORIA" e a rodada inteira vira INCOMPLETO — a costura
nao aprova nenhuma rodada real; e o unico valor que ela aceita como "confere" (hash dos arquivos-fonte)
e um valor que nenhum produtor escreve. Suite e CLI nao pegam isso porque os fixtures declararam
`hash_fonte` na convencao da implementacao, nao na do produtor.

Correcao minima: (1) confrontar contra o campo canonico da DLL do probe (carregar `dll_probe_sha` na
identidade) ou usar explicitamente o alias documentado `hash_fonte == dll_sha`; (2) derivar o fixture/
teste do envelope REAL (`AUT-4-evidencias/r3-confirmada/aut4probe.json`) de modo que o teste FALHE se
a confrontacao voltar a `fonte_sha`; (3) manter bytes que nao casam com nada em INCOMPLETO/exit 2;
(4) confrontar (ou declarar o limite de) `dll_sha`/`config_sha`/`versao` que a coleta declare (S10).

Nota de justica: o implementador cumpriu F1 exatamente como a rodada 1 o especificou; a rodada 1
partiu de uma premissa de campo errada. O achado e da premissa+ligacao, e a correcao pertence ao
mesmo cartao.

## Escopo

Somente `tools/automacao/kit12/{integracao.py,test_kit12_integracao.py,prove_ciclo.py}` e os docs
`KIT-12F-*` mudaram depois da rodada 1 (varredura de mtime). `pertinencia.json` inalterado
(mtime 00:18, mesmo hash). HEAD `d82894e` intacto; sem `git add`/commit/push; nenhum mod, csproj,
patch ou trava tocado; nenhum segredo, token ou dado de perfil do dono em qualquer prova.

## NAO_EXERCITADO (deliberado)

jogo/probe/save/perfil real, runtime AUT-4 (coleta real), UI/UX/pixels, build C#, pre-flight de
deploy, instalacao, publicacao, gates KIT-G1..G4, aceite humano/DoD. Fixture nao comprova runtime.

## Passo seguinte

Implementador corrige F5 (e registra S10) no MESMO cartao `t_0a434c97`, com fixtures derivados do
envelope real do produtor, e pede reconferencia com handoff nativo (implementer/reviewer, resumo +
paths + hashes). Nao aprovar, nao publicar, nao fechar o cartao antes disso.
