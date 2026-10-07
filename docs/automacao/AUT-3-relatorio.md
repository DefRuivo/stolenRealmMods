# AUT-3 — bancada de revisão estática e regressão (t_49075ea4)

Entrega: um **comando único**, offline, que roda a revisão aplicável por mod e
pelas dependências reais e **não toca no perfil do dono**.

    python tools/automacao/offline/bancada_aut3.py --jogo

Saída: `docs/automacao/AUT-3-resultado.json` (dados) + `docs/automacao/AUT-3-resumo.md`
(leitura). Exit `0` = VERDE · `1` = REPROVADO · `2` = INCOMPLETO (algo não exercitado).

## O que roda (reuso dos verificadores existentes)

- **Build** dos 6 mods, `-c Release -p:DeployToBepInEx=false`, **dentro de um sandbox**
  (cópia descartável do repo) e com `-p:PathMap=<sandbox>=<repo>`. O PathMap torna a DLL
  do sandbox **byte-idêntica** à de origem, então o build prova `fonte → DLL` por hash,
  sem alterar `bin/` nem o perfil. Limite de 6 builds respeitado (1 por mod).
- **Suite** (`tools/testes/roda_testes.py`): `--puros` (puro/CI), `--jogo` (estrutura de
  comportamento, precisa só da `lib/`, **não abre o jogo**) e `--contra-prova` (prova de
  fogo do próprio runner). Sem sandbox nenhum; roda na cópia.
- **Conferidores estáticos**: `check_dupes`, `check_chave_compartilhada --estrito`,
  `check_notas_redundantes`, `check_fix_keys`, `check_segredos`, `check_versoes`,
  `check_patches`, `check_dependencias --local`, `check_deploy_optin`,
  `pack-thunderstore --so-conferir` (pre-flight, nada é zipado), `audita_docs`.
- **Contra-provas** (`contra_provas.py`): planta defeito conhecido numa cópia isolada,
  exige REPROVAÇÃO; desfaz, exige APROVAÇÃO.

## Efeitos colaterais inspecionados

Um conferidor **reescreve** texto curado: `check_notas_redundantes.py` grava
`docs/cobertura/revisao/RV-15-notas-redundantes.md` (via `preserva_curado.grava`) — por
isso, e só por isso, ele é roteado para o **sandbox**; no modo `--sem-sandbox` ele sai
como `NAO_EXERCITADO`, nunca como verde. Os demais conferidores usados são **somente
leitura**. **Não** são executados (regenerariam dados/docs curados): `grava_shrines_esperado`,
`census`, `censo_status`, `check_omissao`, `check_scaling`, `scan_tokens`, `verify_tree`,
`audit_tooltips`, `importa_beneficio` (cada um com `open(..., 'w')` próprio).

## Resultado real desta rodada (exit 0, VERDE)

- **6/6 builds** OK; nos 6, `sandbox == Release == perfil` por sha256 (ex.: BetterTooltips
  `270f311b0f7b`, RSTV `454587a031a3`). Prova `fonte → DLL` **e** `bin == perfil`.
- **11/11 conferidores** exit 0 (inclui pre-flight de pacotes e auditoria de docs).
- **Suite**: 85 testes puros PASSOU · 1 de jogo PASSOU · contra-prova do runner
  `49 PROVA_OK + 14 PASSOU` (iscas reprovando como devem).
- **5/5 contra-provas** `PROVA_OK`: chave duplicada (INC-1), versão divergente,
  parâmetro posicional `__0`, alvo de deploy sem opt-in, credencial plantada — cada uma
  com defeito `exit=1` e, após correção, `exit=0`.
- **Perfil intacto por hash** e **repo intacto por hash** (o guarda tem precedência: se
  qualquer um mudar, o veredito vira REPROVADO mesmo com tudo verde).
- Estados separados no JSON: **fonte · Release · perfil · pacote** (sha do DLL dentro do
  zip x Release), sem imprimir conteúdo de config.

## Cobertura alinhada à matriz AUT-2

`docs/automacao/AUT-3-resultado.json → cobertura` mapeia os 20 critérios da
`AUT-2-matriz.json`: **8 OK_OFFLINE · 0 PARCIAL · 12 NAO_EXERCITADO · 0 REPROVADO**.
M1–M6 ficam OK_OFFLINE (build + perfil + zip por hash) e T-RSTV6 OK_OFFLINE (36 testes
rstv verdes, incluindo iscas). Os 12 restantes (T-RSTV21/25B/26, S-RV-26…34, BUG34) são
runtime e saem **NAO_EXERCITADO com motivo** — nunca OK.

## Lacunas (explícitas, não cobertas)

- **Runtime de jogo**: RV-49/números das auras de perigo, tooltips de shrine em tela,
  hover do RSTV (T-RSTV26), camada read-only da janela (T-RSTV21) e a regressão de feed
  do BUG-34 exigem jogo/dono (AUT-4/5/6).
- **T-RSTV25b** segue INDETERMINADO: precisa do `LogOutput.log` do próximo boot.
- **Publicação online** não é verificada aqui (nem local↔online); AUT-3 não publica.
- **Ressalvas da revisão AUT-2R** (docs corrigidos por outro agente, fora do escopo):
  exclusões reais = 2 (não 6), o `LogOutput.log` existe, BetterTooltips tem 48 registros,
  e o "sem drift" histórico não é recomprovável. AUT-3 **não editou** esses documentos.

## Garantias

Não instala, não abre/fecha o jogo, não carrega save, não faz push/commit, não publica,
não muta o board, não regenera doc curada. Só stdlib. Para desfazer: apagar
`tools/automacao/offline/` e `docs/automacao/AUT-3-*`. AUT-3 **não** substitui aceite
humano nem a publicação do DoD.
