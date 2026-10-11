# KIT-08F — revisão independente: APROVADO (técnico)

Reviewer run658 (perfil default, NOVA instância) ≠ implementador run654 ≠ implementador
original run643 ≠ reviewer run648. Revisão OFFLINE em 09/10/2026 (data local no terminal).
Lente da rodada 1: **Artifact** (leitura fria do diff antes da narrativa). Este parecer é
aprovação TÉCNICA do cartão — **não** é aceite humano nem DoD de mod.

## 0. Objeto

- PRODUTO alterado: `tools/automacao/kit08/visualizador.py`
  - BASELINE reprovado: `3d6d2983a845d1423859ef75f7f8e658cde7c14c0d4fe3ee23194d08a9789701`
  - ENTREGA: `bdd33622a1cec76f83636dc095df73fdfde972072cf0809007d70593cdcfa85f`
- Cópia da entrega, suíte e harness imutáveis e KIT-09 conferidos por SHA256 (seção 1).

## 1. Identidades conferidas por mim (não pela narrativa)

| artefato | sha256 | veredito |
|---|---|---|
| `tools/automacao/kit08/visualizador.py` (entrega) | `bdd33622…cdcfa85f` | == cópia `scratch/kit/KIT-08F-run654/visualizador-entrega.py` (cmp OK) |
| sandbox do reviewer `…/KIT-08R-run648/sandbox/…/visualizador.py` (baseline) | `3d6d2983…a9789701` | == baseline declarado |
| `scratch/kit/KIT-08R-run648/test_review_kit08.py` (suíte imutável) | `597b5ab38129d059e00ea17b50ba7a3b07e76a5ad904960d4f23e5b5cf435c14` | NÃO editada |
| `scratch/kit/KIT-08R-run648/review_controls.py` (harness imutável) | `575f2c4cec59b46b1f540f5c4ae325c9967e34710fc5d818f97b268eacf901cd` | NÃO editado |
| `tools/automacao/cenarios/kit09.py` | `55f01e024e5e5ffd0c28b98ef492e2790c606d57d1dab4ae9d0258fba05feabb` | inalterado |
| suíte autor `teste_visualizador_kit08.py` | `840f62e9…e079e7e` | == registro do reviewer648 |
| contra-prova autor `contra_prova_kit08.py` | `9555233e…6c876551` | == registro do reviewer648 |
| `roda_testes_kit08.sh` | `37de9d8d…07db394` | == registro do reviewer648 |
| ZIP de provas | `1cfbaa1bdb21ef00950351fa4edbe469b42ed68f1df8fe243f86a89fbe1bb4ce` (181 arq., testzip OK, sem .git/.pyc/perfil) | confere |

Escopo (diff do sandbox do reviewer648 sobre 27 arquivos × árvore viva): **só**
`visualizador.py` mudou no escopo de produto; os 8 mutantes `scratch/kit/k08/contra/D1..D8_*`
são reescritos pela própria contra-prova ao rodar (artefato de ferramenta, untracked), não
edição manual. Nenhum mod/avaliador de outra frente tocado por este cartão.

## 2. Execuções que EU rodei (workspace próprio `scratch/kit/KIT-08F-run658`, cópia byte-idêntica)

- Suíte imutável × BASELINE: `REVIEW_MODULE=<sandbox baseline> python test_review_kit08.py`
  → **Ran 34, FAILED(failures=24), 10 OK, exit 1, ERROR 0, skip 0** (`red-baseline.log`).
  Os 24 nomes cobrem F1(Security×4), F2/F5(Identity+HonestVerdicts), F3/F4, F6/F7/F8/F9
  (Integration×5) — conjunto == o parecer KIT-08R.
- Suíte imutável × ENTREGA: `REVIEW_MODULE=<live> python test_review_kit08.py`
  → **Ran 34, OK, exit 0, sem FAIL/ERROR** (`green-review.log`).
- 10 mutações seletivas APLICADAS À ENTREGA (mesmas do reviewer): cada uma derruba
  exatamente o alvo (`Ran1 FAIL1 exit1 ERROR0 SKIP0`) — `controls-corrigido.log`.
- 24/24 negativos individuais no CORRIGIDO: `Ran1 OK exit0` cada — `verify_independent.py`.
- Extra 4 do reviewer no CORRIGIDO: `Ran4 OK exit0` — `verify_independent.py`.
- Harness do reviewer no BASELINE (modo original): exit 0; `observed-effects.json` grava o
  defeito bruto (encoded_path accepted=true; without_approval_vigente=true; fixture promovido
  a PASSOU; removed/lost_runtime = OK) — `controls-baseline.log`.
- Sonda própria `verify_independent.py` (não importa scripts do implementador): **CONFORME (exit 0)**.
- Suíte autor × entrega: `Ran21 OK exit0`; contra-prova autor × entrega: **8/8 VERDE exit0**.
- Wrapper Bash `roda_testes_kit08.sh`: **exercitado, exit 0, "VEREDITO KIT-08: VERDE"**
  (`runner-run658.log`). Medido aqui (o reviewer648 teve exit2/infra).
- Scanners reais `check_padroes_segredo.py` e `check_segredos.py`: exit 0, nenhum padrão de
  credencial; não editados, sem exceção nova.

## 3. Refutação por achado (efeito medido na sonda, não mensagem)

- **F1 paths** — 5 positivos locais aceitos (`assets/capture.png`, `img/photo.PNG`,
  `a/b/c.png`, `./x.png`, `foto.jpg`); 13 negativos recusados, incluindo `%2e%2e/private.png`,
  `img/%2e%2e%2f%2e%2e%2fprivate.png`, `C%3a/windows/private.png`, `safe.png?x=1#fragment`,
  `../private.png`, `a//b`, `/abs.png`, UNC, esquema e `C:/x.png`. Confinamento lexical
  fail-closed (percent/`?`/`#`/`:`/componente vazio). **Efeito em browser/file:// segue
  INDETERMINADO** (hardening, sem alegação de exfiltração provada) — coincide com o limite honesto.
- **F2 aprovação** — ausente / vazio / sem-hashes / outro-mod / sintética / rotulo_fixture /
  fonte-divergente: **nunca VIGENTE**; positivo completo e coerente: **VIGENTE** (mantém vigência).
- **F3/F4 comparação** — igual = OK; fixture nunca promovido a PASSOU; perda de prova, caso
  removido, zero casos e id duplicado ≠ OK; defeito observado = FALHOU; config/personagem
  unilaterais e mod diferente recusados; fonte própria da candidata **não** impede comparação.
- **F5 veredito** — `prova_runtime='false'`, `evidencia=[]`, fonte/sessão contraditórias e
  fixture aninhado na identidade: não viram PASSOU.
- **F6 CLI↔API** — identidade aplicada ANTES de avaliar: `CLI={NAO_EXERCITADO:1,PASSOU:20}
  == API={PASSOU:20,NAO_EXERCITADO:1}`, exit 0.
- **F7 exit** — comparação recusada=1, caso removido=1, FALHOU=1, PASSOU=0, sem conclusão=2.
- **F8 campos/imagens** — sessão string preservada; imagem embutida em
  `data:image/png;base64,` com **bytes decodificados iguais aos originais**, gravando em outra
  pasta (exit 0); imagem ausente vira lacuna explícita e o cabeçalho deixa de afirmar
  integralmente autocontido.
- **F9 infra** — `--identidade` inexistente, JSON inválido, objeto não-dict: **exit 2, sem
  traceback**, diagnóstico controlado.

## 4. Limites honestos / ressalvas não bloqueantes

- F1 é hardening lexical; efeito em browser/CSP `file://` **não exercitado** — como declarado.
- Confinamento de imagem usa `abspath`+`commonpath` (lexical), **não** `realpath`: um symlink
  plantado dentro do pacote poderia, em tese, escapar. **Não exercitável aqui** (criação de
  symlink bloqueada por privilégio no Windows) → INDETERMINADO; fora do aceite F1 do reviewer
  (que é lexical) e de risco baixo (entrada é autoral do operador). Registrado, não bloqueia.
- Browser/pixels/UI-UX em jogo/desempenho/coletor real/round-trip runtime/gate humano/
  instalação/deploy/publicação: **NÃO exercitados** (não autorizados nesta rodada).
- `audita_docs` global não executado (mistura outras frentes; não cobre untracked novos).

## 5. Veredito

**APROVADO (técnico)** — os 9 achados F1–F9 do parecer KIT-08R estão sanados e verificados por
execução independente; a suíte imutável do reviewer fechou 34/34 sem afrouxamento; as suítes
autor (21) e contra-prova (8/8) seguem verdes; nada de produto fora do escopo foi tocado.
Aprovar este cartão libera os gates reais KIT-12 t_0a434c97 e KIT-15 t_10584ca5.
Aprovação técnica ≠ aceite humano ≠ DoD de mod.

Provas: `scratch/kit/KIT-08F-run658/` (red-baseline.log, green-review.log, controls-corrigido.log,
controls-baseline.log, verify_independent.py, sonda-run658.log, author-suite-run658.log,
contra-run658.log, runner-run658.log, scanner-*.log).
