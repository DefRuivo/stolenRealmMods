# COR-AUT6 — correção dos nove achados E1–E9 do avaliador AUT-6 (t_6fcb39da)

Tarefa: `t_6fcb39da` (COR-AUT6) · origem: revisão independente AUT-6R (`t_9df16709`, anexos
`REVIEW-AUT-6R.md`, `AUT-6R-evidencias.zip`, `refutacao-resultados.json`,
`integracao-decisao.json`) · revisão seguinte: `t_4200d240`.

Trabalho **OFFLINE**: nenhum build de produto, nenhum deploy no perfil, jogo/save/publicação
intocados. Instalação e restauração em runtime continuam **NÃO EXERCITADAS**.

## Escopo e arquivos

Escrita exclusiva em `tools/automacao/aut6/**` (mais um teste novo na suite pura do projeto e
este relatório). `tools/automacao/runtime/coletor.py`, `tools/automacao/ciclo/decisao.py` e o
hotspot `tools/automacao/cenarios/tooltips_shrines.py` **não foram editados** — o AUT-6 consome
o normalizador real do AUT-4 por adaptador, sem competir pela escrita.

| Arquivo | Estado | sha256 |
|---|---|---|
| `tools/automacao/aut6/cobertura.py` | alterado (base = `a935f573…`, o mesmo hash da revisão) | `e33fb037ab0303e33765331ba5cd06194bb4e1343d534fcbcab9726290ea8c0d` |
| `tools/automacao/aut6/test_cobertura_aut6.py` | alterado (base = `867a098c…`) | `c30dc3f5f81166596aa0c24a59daee070c4ddc5a85e934b8caca93f4e97dc54a` |
| `tools/automacao/aut6/prova.py` | **novo** | `2d952323f1ffbd09223d8f231ed324f3c2cf584994c3ddc50eb018885d9381cb` |
| `tools/automacao/aut6/validacoes.py` | **novo** | `a78c7850fad219a8267be31c7efb1f1c06f155e5117e8e3d76de9316cb767923` |
| `tools/automacao/aut6/suporte_testes.py` | **novo** (emissor de contrato) | `7f5a795a293d519ec6cd2244d227bc327bb55b9ca446fdd57ecacb7c41334c24` |
| `tools/automacao/aut6/test_regressoes_cor_aut6.py` | **novo** (26 regressões E1–E9) | `e109029ca58e58198cef6d42818ddf1f4e34616c01f20d34c3cd4ac9da29f4d3` |
| `tools/testes/testes/puros/t_aut6_cor_e1_e9.py` | **novo** (liga as duas suites na suite pura) | `6db9148c7f029139adf2b89c235a0543f3bd2465f8ced0936bfeb9a5e5069c95` |

Intocados: `casos-aut6.json` (`ade76e34…`), `observacoes_fixture.py` (`52a299ae…`),
`observacoes-fixture.json` (`78c446e5…`), tabelas geradas, fixtures, `checa_shrines.py`, DLLs e
produto. As alterações manuais do dono foram preservadas: a base conferida byte a byte contra o
snapshot da revisão antes de qualquer edição (`snapshot/tools/automacao/aut6/*` do zip).

## Correção por item

Protocolo comum a E1/E3/E5/E6/E7/E9: prova de runtime passou a ser **vínculo verificável**, não
rótulo. `prova.py` exige, para cada critério de runtime:

1. evidência com `{caminho, sha256, ponteiro}` (JSON Pointer RFC 6901) apontando para a
   observação **dentro dos bytes** do artefato;
2. o `sha256` do arquivo batendo com o **manifest da coleta** (e o arquivo existindo);
3. **todo** valor consumido (medida, objeto, personagem, cenário, superfície) presente no
   artefato e idêntico — valor inventado no topo vira `INDETERMINADO`;
4. `sessao`/`fonte_sha`/`dll_sha`/`config_sha` **lidos do próprio artefato** (nunca copiados da
   identidade) e a sessão da observação confrontada com a identidade da rodada (sessão velha →
   `INDETERMINADO`); aliases de hash contraditórios (`hash_fonte` × `dll_sha`) → `INDETERMINADO`;
5. artefato rotulado fixture (ou com `evidencia_runtime=false`) continua fixture, mesmo
   re-rotulado `runtime`, e **o rótulo de teste não pode ser removido dos bytes**
   (`ambiente_prova=teste_contrato` → `INDETERMINADO`).

**E1 — fixture contraditória e arquivo alheio viravam OK vinculante.**
`_rotulo()` consulta a contradição **antes** da procedência declarada (fixture vence sempre) e
`_evidencia_obs`/`prova.conferir` rejeitam arquivo existente sem hash+ponteiro e arquivo fora do
manifest. Replay: `fixture-contraditoria` sai `OK` **de fixture** (`prova_runtime=false`,
`CIC-2=NENHUM vinculante`); `evidencia-alheia` → `NAO_EXERCITADO` nos 3 critérios (antes: 2 OK
vinculantes).

**E2 — 19 fixture + 1 pseudo-runtime davam CLI exit 0.**
`exit_de()` exige `com_prova_runtime == total` e conjunto não vazio; o avaliador passou a emitir
o critério agregado `S-aut6-completude-runtime`, que acusa **por id** cada critério obrigatório
sem prova. Replay: `misto-19-fixtures-1-runtime` → `exit 2`, `OK 7`, `NAO_EXERCITADO 17`,
`com_prova_runtime=0` (antes `exit 0`).

**E3 — sessão velha e fonte/config ausentes.**
Sessão da observação é confrontada com a identidade (`INDETERMINADO` na divergência) e
`fonte_sha`/`dll_sha`/`config_sha` passaram a ser **obrigatórios na observação** — os valores do
critério saem da observação, não da identidade. Replay: `sessao-antiga-config-fonte-ausentes` →
3× `NAO_EXERCITADO` (antes `OK`).

**E4 — teto/piso aprovavam total impossível e contribuição ausente.**
`_caso_limite` passou a validar, por linha do feed: `total == clamp(cru, MaxValue|MinValue)`,
consistência da flag `no-teto/no-piso` com o cru, **total no limite exercitado**, item de
contribuição presente, contribuição igual à tabela gerada e igual ao total clampado, com cadeia
de prova nos dois registros. Replay: `limites-total-impossivel` → **2× REPROVADO** ("total/valor
cru/flag no-limite contradizem o clamp", exit 1 — antes 2 OK vinculantes);
`limites-sem-contribuicao` → 2× `NAO_EXERCITADO` ("limite exige contribuicao preservada e fonte
independente").

**E5 — corpo inativo/erro/vermelho aprovava render.**
Critério novo de corpo: exige o artefato medido (objeto/personagem), `ativo_na_hierarquia is
True` e `visivel_na_tela is True`; inativo/invisível → `INDETERMINADO`; `status=ERRO`/`ok=false`
→ `INDETERMINADO` em qualquer critério. Cor e posição técnicas viraram **dois critérios
medidos**: `S-rv26-corpo-linha-nota/cor` (span × controle azul independente do jogo) e
`/posicao` (retângulos da linha e do corpo + "último bloco"), com `NAO_EXERCITADO` quando o campo
técnico não existe. Replay: `corpo-inativo-erro-vermelho` → `INDETERMINADO` no corpo + 2×
`NAO_EXERCITADO` (antes `OK` vinculante).

**E6 — feed benigno mascarava vazamento no texto flutuante.**
A regressão do BUG-34 virou **três superfícies independentes** (`feed`, `corpo`, `flutuante`),
cada uma medida por si (`texto_renderizado` **e** feed, sem `or`), e a superfície flutuante é
exigida ou fica `NAO_EXERCITADO` — o modo combinado só serve para fixture (lógica), nunca para
cobertura de runtime. Aceite humano do BUG-34 preservado (`reabre_bug=false`). Replay:
`armor-feed-mascara-flutuante` → `/feed` **REPROVADO** + `/corpo` e `/flutuante`
`NAO_EXERCITADO` (antes passava).

**E7 — primeiro corpo positivo mascarava regressão posterior.**
Corpos e medições do mesmo cenário são avaliados **um a um** e mesclados pelo pior estado, com
todas as medições preservadas em `medicoes[]`; alvo/cenário/sessão diferentes sem cenário
inequívoco → `INDETERMINADO`. Observação de runtime **sem cenário declarado** é elegível, mas se
mais de um caso a consumir, todos os critérios dela ficam `INDETERMINADO` (ambiguidade
registrada). Replay: `corpo-regressao-posterior-ignorada` → 3× `NAO_EXERCITADO` com as duas
medições no critério (antes ignorava a segunda).

**E8 — costura AUT-4 → AUT-6 → CIC-2.**
`cobertura.normalizar_aut4()` chama o `normalizar_observacao` **real** do AUT-4 e **preserva**
os campos que o schema dele não transporta (origem, alvo, superfície, sessão/hash/config), sem
fabrica-los a partir da identidade; `prova.conferir` exige que cada um deles exista **nos bytes**
do artefato. `S-rv29-transicao-mesmo-personagem` mede entrar→sair do **mesmo** personagem na
**mesma** sessão com sequências crescentes (par diferente → `NAO_EXERCITADO`). RV-49 deixou de
ser "decisão residual": sai `classe=runtime`, `INDETERMINADO`, com os **dois fatos preservados**
(`fato_30_09`/`fato_03_10`) e `lacuna_probe` nomeando a divergência, o que o CIC-2 classifica
como **falha automática** (`pronto_para_decisao=false`). Replay: `costura-aut4-normalizado` →
3× `NAO_EXERCITADO` (antes `OK`).

**E9 — oráculo Dwarven ausente aprovava 3 critérios.**
Item sem atributo agora exige **fonte independente**: sem linha na tabela gerada, o critério é
`NAO_EXERCITADO` **antes** de olhar a observação (ausência de oráculo nunca vira OK). Replay:
`dwarven-oraculo-ausente` → 3× `NAO_EXERCITADO` ("fonte independente ausente: item sem atributo
nao tem esperado", antes 3 OK runtime).

Nenhuma fórmula Flame/Decay/Dwarven foi alterada; nenhuma linha do RV-49 foi apagada; o critério
de completude nunca falha sozinho (só quando outro critério já está sem prova), portanto não
protege nenhum outro item.

## Prova

**Replay dos 14 ensaios de `refutar.py`** (`AUT-6R-evidencias.zip`), no snapshot corrigido, com
`refutacao-resultados.json` e `integracao-decisao.json` regerados
(`replay-14-final.log`):

| ensaio | exit antes | exit agora | leitura |
|---|---|---|---|
| controle-fixture | 0 (OK vinculante) | 2 | fixture nunca vincula (`com_prova_runtime=0`) |
| controle-vazio | 2 | 2 | ausência não aprova |
| controle-globule-errado | 1 | 1 | o defeito plantado continua reprovando |
| E1 fixture-contraditoria | 0 | 2 | `OK` de fixture, `prova_runtime=false` |
| E1 evidencia-alheia | 0 | 2 | 3× `NAO_EXERCITADO` |
| E2 misto-19-fixtures-1-runtime | 0 | 2 | completude incompleta por critério |
| E3 sessao-antiga-config-fonte-ausentes | 0 | 2 | 3× `NAO_EXERCITADO` |
| E4 limites-total-impossivel | 0 | 1 | 2× `REPROVADO` no clamp |
| E4 limites-sem-contribuicao | 0 | 2 | 2× `NAO_EXERCITADO` |
| E5 corpo-inativo-erro-vermelho | 0 | 2 | `INDETERMINADO` + 2× `NAO_EXERCITADO` |
| E6 armor-feed-mascara-flutuante | 0 | 1 | `/feed` `REPROVADO` |
| E7 corpo-regressao-posterior-ignorada | 0 | 2 | as duas medições medidas |
| E8 costura-aut4-normalizado | 0 | 2 | superfície/cenário ausentes nos bytes |
| E9 dwarven-oraculo-ausente | 0 | 2 | 3× `NAO_EXERCITADO` |

**Nenhum** dos 14 ensaios produziu `prova_vinculante` no consumidor CIC-2
(`integracao-decisao.json`: `vinculantes=NENHUM` em todos). Os controles positivos fixturados
seguem aprovando a lógica (21 OK de fixture no `controle-fixture`) e o caminho positivo de
**contrato** (bytes+manifest próprios, `ambiente_prova=teste_contrato`) fecha cadeia — e mesmo
assim sai `prova_runtime=false`, com motivo "TESTE DE CONTRATO … nao prova produto/runtime".
Amostras completas de teste são distinguíveis de produto por `ambiente_prova`/`origem` gravados
nos bytes, e removê-los dos bytes vira `INDETERMINADO`.

**Suites**

| comando | resultado |
|---|---|
| `tools/automacao/aut6/test_cobertura_aut6.py` | 24/24 PASSOU (exit 0) |
| `tools/automacao/aut6/test_cobertura_aut6.py --isca` | 25/25 PASSOU (isca morde: 11 critérios reprovados) |
| `tools/automacao/aut6/test_regressoes_cor_aut6.py` | 26/26 OK (E1–E9, um teste por achado + completude + ambiguidade) |
| `tools/testes/roda_testes.py --puros` | 86/86 (85 anteriores + `aut6-cor-e1-e9`) — VERDE |
| gates: `check_dupes`, `check_notas_redundantes`, `check_chave_compartilhada --estrito`, `check_segredos`, `check_versoes`, `check_deploy_optin`, `check_patches`, `audita_docs` | exit 0 |
| `tools/automacao/aut6/cobertura.py --offline` | exit 2 (ausência não é aprovação) |

Todos os números desta seção saem de execução real no snapshot (`gates-corrigido.json`,
`replay-14-final.log`, `suite-pura-final.log`, `refutacao-resultados.json`,
`integracao-decisao.json`, `hashes-corrigido.json`).

## Achado fora do escopo (fechado depois pela `t_1e7a19aa`)

`tools/checa_citacoes.py` saía **1** com uma pendência **pré-existente** e alheia ao AUT-6:
`docs/automacao/AUT5-F1-entrega.md:15` (hoje `:20` — a nota de reentrega no topo do documento
deslocou o trecho em 5 linhas) citava o fonte do probe **sem o prefixo `tools/automacao/`**,
caminho que não existe no repositório. Documento de outra frente: não foi tocado aqui.

Duas ressalvas de precisão, medidas depois (execução de 05/10/2026 21:14):

- este parágrafo, ao **citar** o caminho curto, criava uma **segunda** pendência da mesma
  ferramenta no próprio relatório — logo "1 pendência" não era mais a árvore deixada pelo AUT-6
  (a ferramenta acusava 2).
- 14 dos 16 usos do probe **com caminho** (pasta + nome do arquivo) no repositório já eram
  completos; os 2 incompletos eram justamente `docs/automacao/AUT5-F1-entrega.md:20` e este
  parágrafo.

A tarefa `t_1e7a19aa` corrigiu as duas citações para
`tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` e `tools/checa_citacoes.py` volta a sair
**0** (execução de 05/10/2026 21:14: 141 citações/menções em 119 documentos, 141 conferidas,
**0 pendências**). A pendência nunca foi do AUT-6 — a fonte dela é o documento da frente AUT-5.

## Lacunas / NÃO EXERCITADO

- **Runtime real**: nenhuma coleta, nenhuma instalação/restauração do probe, nenhum boot — a
  cadeia exige `manifest` da coleta e evidência com ponteiro; nada disso existe nesta rodada.
  `instalacao/restore = NÃO EXERCITADO`.
- **Aceite humano em jogo e publicação**: estados separados, fora desta tarefa; nenhum mod
  fechado, nenhuma versão publicada.
- **Superfícies sem campo medido** (`cor`, `posicao`, `flutuante`, `transicao`) ficam
  `NAO_EXERCITADO` até a coleta emitir os campos — é a lacuna que o AUT-4/coletor precisa fechar.
- **Contrato do adaptador**: `normalizar_aut4` depende de o probe emitir `objeto`, `cenario`/
  `superficie` e `personagem` por observação. Sem esses campos o caminho de runtime fica
  `NAO_EXERCITADO` — por desenho, mas é requisito novo para o coletor, e é onde a próxima
  rodada deve olhar primeiro.
