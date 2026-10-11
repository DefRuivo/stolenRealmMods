# KIT-08F — entrega: correção F1–F9 do visualizador (t_ac0f78f7, run654, perfil default)

Implementador: instância run654 (NOVA; != implementador original run643 != reviewer
run648). Implementação OFFLINE, 09/10/2026, sem jogo/save/perfil/instalação/deploy/
build/publicação/navegação/rede/credenciais/IA. Aprovação técnica NÃO é DoD.

## 1. Identidades e escopo

| artefato | sha256 |
|---|---|
| BASELINE reprovado `tools/automacao/kit08/visualizador.py` | `3d6d2983a845d1423859ef75f7f8e658cde7c14c0d4fe3ee23194d08a9789701` |
| ENTREGA (corrigido) `tools/automacao/kit08/visualizador.py` | `bdd33622a1cec76f83636dc095df73fdfde972072cf0809007d70593cdcfa85f` |
| cópia da entrega `scratch/kit/KIT-08F-run654/visualizador-entrega.py` | `bdd33622…` (idêntica) |
| cópia byte a byte do baseline `…/sandbox/tools/automacao/kit08/visualizador.py` | `3d6d2983…` (idêntica) |
| suíte imutável copiada (NÃO editada) `test_review_kit08.py` | `597b5ab38129d059e00ea17b50ba7a3b07e76a5ad904960d4f23e5b5cf435c14` (igual ao ZIP KIT-08R) |
| harness imutável copiado (NÃO editado) `review_controls.py` | `575f2c4cec59b46b1f540f5c4ae325c9967e34710fc5d818f97b268eacf901cd` (igual) |
| ZIP de provas `scratch/kit/KIT-08F-run654-evidencias.zip` | `1cfbaa1bdb21ef00950351fa4edbe469b42ed68f1df8fe243f86a89fbe1bb4ce` (181 arquivos) |

Único arquivo de PRODUTO alterado: `tools/automacao/kit08/visualizador.py` (untracked no
index; a suíte autor, a contra-prova e o KIT-09 NÃO foram editados). Docs novos:
`docs/automacao/KIT-08F-parte01.md`, `-parte02.md`, este arquivo. Nada de mods,
Assembly-CSharp.dll, Bard/música, gameplay, perfil/save, crons, modelos, política ou
prioridades. Nenhum `git add`/commit/push.

## 2. Prova principal — suíte imutável do reviewer

Comando (a suíte lê `REVIEW_MODULE`, nada no arquivo é editado):

    cd scratch/kit/KIT-08F-run654
    REVIEW_MODULE=<baseline sandbox>   python test_review_kit08.py   -> Ran 34, FAILED(failures=24), 10 OK, exit 1   (RED preservado) -> red-baseline.log / review.log / recon-red.log
    REVIEW_MODULE=<entrega corrigida>  python test_review_kit08.py   -> Ran 34, OK, exit 0                            (verde)         -> green-review.log / recon-green.log

Os 24 negativos do RED batem com os 24 grupos F1–F9 do parecer; a suíte corrigida fica
34/34 sem ERROR e sem skip. Nenhum teste foi editado, pulado ou afrouxado.

## 3. Reconferência exata (`scratch/kit/KIT-08F-run654/reconferencia.py`, exit 0)

- RED no baseline: `Ran34 FAIL=24 OK=10 exit=1 ERROR0 SKIP0`.
- VERDE no corrigido: `Ran34 OK exit=0`.
- 10 mutações seletivas dos positivos aplicadas AO CORRIGIDO: cada uma derruba
  exatamente o teste alvo (`Ran1 FAIL1 exit1 ERROR0 SKIP0`) — escape, csp, fixture,
  failure, human, stale, ref, matching, different, reuse.
- 24 negativos rodados individualmente no corrigido: `24/24 Ran1 OK exit0 ERROR0 SKIP0`.
- Extra do reviewer no corrigido: `Ran4 OK exit=0`.
- Contagem das 11 âncoras de mutação no fonte corrigido: 1x cada.

## 4. Suítes autor preservadas

- `python tools/automacao/kit08/teste_visualizador_kit08.py` → `Ran 21 tests, OK`, exit 0.
- `python tools/automacao/kit08/contra_prova_kit08.py` → `VEREDITO KIT-08 contra-prova:
  VERDE (8/8 defeitos recusados exato)`, exit 0 (inclui o falso-verde D7 recusado).
- Wrapper `bash tools/automacao/kit08/roda_testes_kit08.sh` foi EXERCITADO neste
  ambiente: exit 0, `VEREDITO KIT-08: VERDE (exit 0)` → runner.log. (O reviewer run648
  obteve exit 2/INDETERMINADO por infra do subshell; aqui o interpretador foi
  resolvido, e o resultado foi medido, não inferido.)

## 5. Harness do próprio reviewer contra o BASELINE

`python review_controls.py` (sem `REVIEW_MODULE`, logo módulo = sandbox baseline) →
exit 0: 10 mutações seletivas OK, `NEGATIVES 24 each Ran1 FAIL exactly exit1 ERROR0
SKIP0`, Extra `Ran4 FAIL4 ERROR0 SKIP0` → controls-run.log. `observed-effects.json`
registra o defeito bruto (`%2e%2e` aceito, `without_approval_vigente: true`,
`fixture_comparison` promovendo PASSOU, `removed`/`lost_runtime` = OK). Nada foi
enfraquecido para tornar o corrigido verde.

## 6. Controles positivos/efeitos no CORRIGIDO (`controles-corrigido.py`, exit 0)

Efeito medido, não mensagem — `effects-corrected.json`:

- F1: positivos locais aceitos; `%2e%2e/private.png`, `img/%2e%2e%2f…`, `C%3a/…`,
  `safe.png?x=1#fragment`, `../`, rede/UNC/absoluto/`a//b` recusados.
- F2: ausente/vazia/sem-hashes/outro-mod/sintética/incompleta NÃO são VIGENTE;
  positivo completo e coerente SEGUE VIGENTE.
- F3: fixture nunca PASSOU; perda de prova = FALHOU; caso removido = FALHOU
  (`regressoes=['removido']`); duplicados e zero casos ≠ OK; contexto igual = OK;
  defeito observado = FALHOU.
- F4: mod diferente RECUSA; config/personagem de um lado só RECUSA; fonte/DLL próprias
  da candidata NÃO impedem comparação.
- F5: `prova_runtime='false'`, `evidencia=[]`, fonte/sessão contraditórias e
  `identidade.rotulo_fixture` não viram PASSOU.
- F6: CLI `--identidade` exit 0 e contagem CLI == API (`{PASSOU:20,
  NAO_EXERCITADO:1}`) — identidade aplicada ANTES de avaliar.
- F7: comparação recusada → exit 1; caso removido → exit 1; FALHOU → 1; PASSOU → 0;
  sem conclusão → 2.
- F8: sessão string preservada; imagem local embutida `data:image/png;base64,` com
  BYTES conferidos por decodificação; gravar em outra pasta não quebra; imagem ausente
  vira lacuna explícita e o cabeçalho deixa de afirmar autocontido.
- F9: `--identidade` inexistente → exit 2 sem traceback; entrada malformada → exit 2.

## 7. Scanners (motores reais, não CLI git)

- `python tools/check_padroes_segredo.py` → 874 versionados, 0 padrões, exit 0.
- `python tools/check_segredos.py` → 874 versionados + 276 de área de teste, 0 padrões,
  exit 0.
- Lista explícita de 74 arquivos do escopo com os MESMOS motores (o diretório kit08 é
  untracked, então `git ls-files` não o cobre): 20 achados heurísticos PRESERVADOS em
  bruto — o id público `KIT09-RSTV25b-sem-aresta-inventada` (34 chars, entropia 4.2) nos
  fontes KIT-09 e nos docs do reviewer, e os exemplos do próprio `check_segredos.py`
  dentro da cópia de sandbox. **Zero achados no visualizador entregue.** Scanners não
  editados, sem exceção nova. (`scanners-raw.log`, `scanners-explicitos.log`.)

## 8. Limites honestos (não alegados como feitos)

Browser/CSP aplicada em `file://`, pixels, acessibilidade visual, JavaScript do engine,
UI/UX em jogo, desempenho, coletor real, round-trip de runtime, gate humano,
instalação/deploy/publicação: NÃO exercitados nesta autorização. O ganho de F1 é
hardening lexical (percent/consulta/fragmento deixam de ser aceitos); efeito
específico em browser segue INDETERMINADO — não há alegação de exfiltração provada.
Fixtures/harness próprios são software offline, não prova de jogo. Aprovação técnica
deste cartão ≠ aceite humano ≠ DoD de mod. Não executei `audita_docs` global (mistura
outras frentes e não cobre untracked novos).

## 9. Handoff

Revisão independente pedida no MESMO cartão (`kanban_request_review`), outra instância,
para tentar refutar F1–F9. KIT-12 t_0a434c97 e KIT-15 t_10584ca5 seguem gated por este
cartão. Em blocker genuíno, `kanban_block` com prova.
