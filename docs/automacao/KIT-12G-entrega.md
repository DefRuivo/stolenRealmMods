# KIT-12G — entrega da rodada 3 (correcao do F5 da revisao run670)

Cartao: `t_0a434c97` · implementador: `default run671` (instancia nova) · autorizacao do dono
07/10/2026 (implementacao/revisao OFFLINE, fila serial) · HEAD base e final `d82894e`.
Partes: `KIT-12G-parte01.md` (plano), `KIT-12G-parte02.md` (detalhe do codigo).

## 1. F5 (bloqueante) — o que o revisor mediu e o que foi corrigido

`confrontar_coleta` / bloco (2c) comparavam `coleta_meta["hash_fonte"]` com `ident["fonte_sha"]`,
mas o PRODUTOR VIVO escreve em `hash_fonte` o sha256 da DLL do INSTRUMENTO (probe):
`runtime/coletor.py:636-637` e `:651-652`, `AUT4ProbePlugin.cs:180`, e a evidencia real
`docs/automacao/AUT-4-evidencias/r3-confirmada/aut4probe.json` (`hash_fonte` ==
`identidade.hash_dll_do_probe` == `407c5c63…`). A convencao do alias esta no repo em
`ciclo/test_decisao.py:562-563`, `aut6/cobertura.py:270-277`, `aut5/test_aut5.py:563` e
`cenarios/kit09-verdade.entrada.json`. Efeito medido pelo revisor (S10/S11): toda coleta legitima
rebaixada e o unico valor aceito era um valor que nenhum produtor escreve.

Correcao (os 4 itens do parecer):

1. **Campo canonico do instrumento**: `identidade_cadeia` passou a resolver `dll_probe_sha`
   (`instrumento_da_coleta`): MEDIDO quando ha bytes (`--probe-dll`, ou
   `identidade.arquivo_dll_do_probe` existente em disco), senao DECLARADO pelo envelope
   (`identidade.hash_dll_do_probe`, `identidade.dll_sha`, `dll_sha` de topo), com a origem
   registrada (`dll_probe_sha_origem` = `medido-cli`/`medido-arquivo`/`declarado-coleta`).
   O alias documentado `hash_fonte == dll_sha` e o ultimo recurso (formato `kit09-verdade`).
   **`fonte_sha` nunca confere procedencia de coleta** — o fallback `hash_fonte or fonte_sha` de
   `carregar_coleta` foi REMOVIDO.
2. **Fixture/teste do envelope REAL**: `test_kit12_integracao.py:campos_do_envelope_real()` le
   `AUT-4-evidencias/r3-confirmada/aut4probe.json` e o teste FALHA se o invariante do produtor
   (`hash_fonte == identidade.hash_dll_do_probe`) mudar; o envelope das provas e montado nesse
   formato. Teste-armadilha proprio: coleta com `hash_fonte` = `fonte_sha` da rodada ->
   `cadeia/coleta-contraditoria/hash_fonte` + nenhum OK (falha se a confrontacao voltar para
   `fonte_sha`); `prove_ciclo.py` tem a mesma etapa (3c) montada a partir do `fonte_sha` MEDIDO.
3. **Fail-closed preservado**: bytes que nao casam com nenhum campo da identidade seguem
   INCOMPLETO/exit 2; envelope conforme NAO e rebaixado (etapa 1 do `prove_ciclo` e sondas
   S11/S11b/CP abaixo: `APROVADO_OFFLINE`/exit 0, zero lacuna `cadeia/coleta-*`).
4. **S10**: `carregar_coleta` le e CONFRONTA `fonte_sha`/`config_sha`/`versao`/`sessao`
   declarados pela coleta (topo e/ou bloco `identidade`) com a identidade da rodada; divergencia
   -> lacuna `cadeia/coleta-contraditoria/<campo>` + rebaixamento; divergencia entre topo e
   `identidade` -> `cadeia/coleta-incoerente/<campo>`. Instrumento apenas DECLARADO (sem bytes em
   disco) e registrado como limite (`coleta.instrumento_origem`, `resultado["limites"]`), sem
   inventar medicao e sem rebaixar envelope conforme.

Novo tipo de lacuna: `cadeia/coleta-incoerente/<campo>` (hash_fonte contra o instrumento que a
propria coleta declara; e instrumento medido != declarado). `confrontar_coleta` continua
devolvendo LISTA de achados (compativel); `confronto_da_coleta` devolve `(achados, confronto)`.

## 2. Provas (execucao real, saidas com exit e caminhos)

| prova | comando | resultado |
|---|---|---|
| suite | `python tools/automacao/kit12/test_kit12_integracao.py` | **Ran 30 tests / OK, exit 0** |
| isca | `... --isca` | **14/14 mutacoes discriminadas, controle restaurado exit 0** |
| CLI sandbox | `python tools/automacao/kit12/prove_ciclo.py --out scratch/kit/KIT-12G-run671` | exits **2 -> 1 -> 2 -> 2 -> 2 -> 2 -> 3**, `PROVA|PASSOU` |
| sondas do implementador | `python scratch/kit/KIT-12G-run671/sondas_implementador.py scratch/kit/KIT-12G-run671` | ver tabela abaixo |
| travas | `check_segredos.py` / `check_padroes_segredo.py` / `check_dupes.py` / `audita_docs.py` | **exit 0** cada |

Etapas da CLI (sandbox externa, copia de `tools/` + mod de fixture + DLL de INSTRUMENTO de
fixture + `git init`, sem `.git` remoto/perfil do dono — `git remote -v` vazio, confirmado):

1. `1-fixture-marcada` (envelope do produtor, instrumento MEDIDO por `--probe-dll`):
   INCOMPLETO/exit 2; `hash_fonte_confronto = confere`, campo `dll_probe_sha(medido)`,
   `dll_probe_sha_origem = medido-cli`, **zero** lacuna `cadeia/coleta-*`;
2. `2-defeito-plantado`: REPROVADO/exit 1 com a fila (criterio + causa/caminho + prova);
3. `3-correcao-controlada`: INCOMPLETO/exit 2, defeito some, nenhum OK;
3b. `3b-coleta-hash-de-outros-bytes` (`0`*64): INCOMPLETO/2 + `cadeia/coleta-contraditoria/hash_fonte`;
3c. `3c-coleta-hash-dos-arquivos-fonte` (hash = `fonte_sha` da rodada): INCOMPLETO/2 +
   `cadeia/coleta-contraditoria/hash_fonte` — a convencao ERRADA do F5 nao confere;
3d. `3d-envelope-incoerente`: INCOMPLETO/2 + `cadeia/coleta-incoerente/hash_fonte`;
4. `4-verificar-apos-mudanca-de-config`: exit 3 (aprovacao anterior INVALIDADA).

Sondas proprias do implementador (`scratch/kit/KIT-12G-run671/sondas-implementador.json`):

| sonda | estado | exit | confronto | lacunas |
|---|---|---|---|---|
| S11 envelope do produtor + instrumento medido | APROVADO_OFFLINE | 0 | confere | — |
| S11b envelope do produtor + instrumento declarado | APROVADO_OFFLINE | 0 | confere | — |
| S2 hash de outros bytes | INCOMPLETO | 2 | contraditoria | `cadeia/coleta-contraditoria/hash_fonte` |
| S9 `fonte_sha` (convencao antiga) | INCOMPLETO | 2 | contraditoria | `cadeia/coleta-contraditoria/hash_fonte` |
| contra-prova alias `dll_sha` | APROVADO_OFFLINE | 0 | confere | — |
| S10 coleta declarando cadeia do mod de outros bytes | INCOMPLETO | 2 | confere (hash_fonte) | `.../coleta-contraditoria/fonte_sha`, `.../versao` |
| envelope incoerente | INCOMPLETO | 2 | incoerente | `cadeia/coleta-incoerente/hash_fonte` |

Fixtures MARCADAS nunca viram prova de runtime: todas as coletas das provas sao
`procedencia=fixture`/`rotulo_fixture`/`evidencia_runtime=false` e o resultado continua
`com_prova_runtime = 0` (a avaliacao nao vira OK/PASSOU).

## 3. Arquivos e hashes (sha256)

- `tools/automacao/kit12/integracao.py` — **7785d8c1f624ff263b4ac89ad36e3ab9952db17d5a233d12affada091da8af87**
  (antes, run669: `ae61678c7b5cca65295693ef2f0611865dca651ed7b39a352407d58236a0d13b`)
- `tools/automacao/kit12/test_kit12_integracao.py` — **25284c7075633042efc6445a5856d5a24e40d152ccdb593d6cb94d661e96da8c**
  (antes, run669: `78f09d5b1a5bfda8324e8ae4cebe711aa4a61de209fffdfb1e082ec8723cec4f`)
- `tools/automacao/kit12/prove_ciclo.py` — **4fc01b81572bdfbbea4cc3af33f1fb845659f23bc689cc94068e2d85b973b750**
  (antes, run669: `494c70b66714ae58ebba99784e430fb6ab794664f3841e0f5802de29f8a69897`)
- `tools/automacao/kit12/pertinencia.json` — `b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320`
  (INALTERADO desde run667)
- `scratch/kit/KIT-12G-run671/prova.json` — `d908266eeb95b9c4f4c241aa430eeb532acf9288dafb1a13a8aaf1466370a6bd`
- `scratch/kit/KIT-12G-run671/sondas-implementador.json` — `ec02491e421f4ab7da7579bf55f9e36d773fcd38ce25dc7a5acef5157973cf13`

Escopo: so `tools/automacao/kit12/{integracao.py,test_kit12_integracao.py,prove_ciclo.py}` e os
docs `KIT-12G-*` + `scratch/kit/KIT-12G-run671/`. `pertinencia.json`, CIC-1/CIC-2/CIC-5, KIT-10,
AUT-5/6/7 e `relatorio_aceite.py` foram apenas REUSADOS (nenhuma dependencia compartilhada
editada); nenhum arquivo de mod, nenhum `Assembly-CSharp.dll`, nenhum Bard/gameplay. Nada de
`git add`/`commit`/`push`; HEAD `d82894e` intacto e `git remote -v` vazio na sandbox.

## 4. Nota de COMPATIBILIDADE (muda o veredito de sondas antigas — de proposito)

A sonda S9 da revisao run668 ("coleta declarando o hash DA RODADA" -> `confere`) usava o
`fonte_sha` como "hash da rodada". Aceitar isso ERA o defeito F5: agora esse caso e
CONTRADITORIA (`cadeia/coleta-contraditoria/hash_fonte`). A contra-prova equivalente ("a correcao
nao virou trava cega") passa a ser: coleta declarando o instrumento MEDIDO (`--probe-dll`) ou o
alias/instrumento declarado coerente -> `confere` e o OK offline sobrevive — medido aqui nas
sondas S11/S11b/CP (APROVADO_OFFLINE/exit 0) e nos testes
`test_positivo_coleta_com_instrumento_da_rodada_mantem_o_ok` (casos a e b) e
`test_positivo_envelope_real_do_produtor_confere_sem_rebaixar`.

## 5. Limites declarados (nao sao verdes)

- Jogo/probe/save/perfil real, runtime AUT-4 (coleta real), UI/UX/pixels, build C#,
  pre-flight de deploy, instalacao, publicacao, gates KIT-G1..G4 e aceite humano/DoD:
  **NAO_EXERCITADO**. Fixture nao comprova runtime.
- Instrumento apenas DECLARADO pela coleta (bytes do probe ausentes) e aceito como DECLARACAO
  (`coleta.instrumento_origem = declarado-coleta`, listado em `resultado["limites"]`): um envelope
  internamente coerente sem bytes em disco nao pode ser verificado offline — o verificador
  independente entra com `--probe-dll` (medicao dos bytes). Isso e limite declarado, nao medicao
  inventada.
- Envelope SEM bloco de instrumento (`identidade.*`) e sem alias `dll_sha` correspondente segue
  INCOMPLETO/exit 2 (fail-closed): nenhum campo da identidade casa com os bytes -> nao confere.
- F3/F4 da revisao run668 seguem como divida declarada (fail-closed), nao tocados nesta rodada.
- `dll_probe_sha` viaja na cadeia (entra no `cadeia_sha`) mas NAO entra na lista de invalidacao
  (`invalidar_anterior` continua sobre fonte/DLL/config/versao): o instrumento nao e byte do mod,
  e um probe removido ao fim da rodada invalidaria a aprovacao por ausencia de arquivo.
- Achado de terceiro nao corrigido aqui (produto de outro cartao): `kit10_cenarios._criterio(obs=None)`
  levanta `AttributeError` no caminho de oraculo indisponivel; AUT-7 emite `classe=runtime` com
  `procedencia=execucao` (normalizado em lacuna nomeada pela costura, preservando o original).
