# KIT-03R — Revisão independente de KIT-03 (parte 01: escopo, identidade e achados estáticos)

Revisor: instância separada do implementador (worker default, run 603). Data: 2026-10-09.
Escopo revisado: KIT-03 (`docs/automacao/KIT-03-entrega.md`) e os scripts citados em `scratch/kit/`.
Modo: OFFLINE, somente leitura no produto; nenhum build instalado, nenhum jogo aberto, nenhuma publicação.
Sandbox de execução: `scratch/kit-revisao/sandbox/` (cópia; sem .git remoto, sem perfil do dono).

## Artefato revisado — identidade (SHA256, medido com sha256sum nesta sessão)

| Arquivo | SHA256 | Bytes |
|---|---|---|
| docs/automacao/KIT-03-entrega.md | d7203e671bfdb4a13b829ff6185f109bc7db330fd6fe3d80077403081b6b9ce5 | 8746 |
| scratch/kit/run-isolation-tests.sh | 9faa67e531571c9306d97855717673226ff154b4a618c474da50808ff2cb62eb | 10105 |
| scratch/kit/detect-env.sh | 996fa18e5a62ea1b42a0a440f10948d4ad0cd30ffe6b99011e84992371b57b8e | 6481 |
| scratch/kit/snapshot.sh | 4f826b1a33964103473192918daa0dd2ac4852f36cd37d9a373952a998a4222a | 6070 |
| scratch/kit/isolacao.sh | de87e727722851dc24d4f45a94045740a68bce79074950e384997de104917c45 | 7568 |
| scratch/kit/front-unica.sh | cddcfd357374f6c90e39f1570a9209969f8aed0b82a34dc20532464e08b2281b | 6140 |

Nota: `detect-any.sh` citado no handoff do cartão-pai NÃO existe no disco (`ls scratch/kit/detect-any.sh` → exit 2). Ver critério C1/C9.

## Critérios de aceite desta revisão

- C1 Identidade dos arquivos vivos (hashes no entregável)
- C2 Detecção de ambiente (detect-env.sh) exercitada no caminho positivo
- C3 Snapshot recursivo + rollback exato, com controle negativo (defeito plantado)
- C4 Prova de isolamento de saves não tautológica
- C5 Front única / PID / preservação da sessão do dono
- C6 Ausência de caminhos pessoais fixos (portabilidade)
- C7 Ausência de resíduos de instalação no perfil do dono / plugins
- C8 Runner orquestrador: exit code fiel, sem falso-verde (skip ≠ pass)
- C9 Reuso de infraestrutura (AUT-4Probe, CAP-1, CIC-1..5, AUT-5/6/7) sem duplicar
- C10 Build isolado com `-p:DeployToBepInEx=false`
- C11 Escopo: nada instalado/publicado/modificado no produto

## Achados estáticos iniciais (leitura do código — a CONFIRMAR por execução)

A1. **`run-isolation-tests.sh` aborta no contador** (linha 59): o script usa `set -euo pipefail` e logo em seguida `((TOTAL++))`. Em bash, `((0++))` tem status de saída 1 (valor antigo 0), então `set -e` mata o script na primeira linha de contagem. Se confirmado, o runner nunca chega ao Teste 1 e todo o "TODOS OS TESTES PASSARAM" do entregável é não reprodutível.
A2. **Tautologia na prova de isolamento**: `isolacao.sh` cria o save descartável DENTRO de `ISOLATED_SAves_DIR` e depois compara se ele está fora de `SAVES_DIR`; a resposta é verdadeira por construção, sempre — não é prova de isolamento, é identidade de variável. Não há controle negativo.
A3. **Caminho de saves errado/placeholder**: `isolacao.sh` usa `SAVES_DIR=${SAVES_DIR:-$LOCALAPPDATA/Abyssus/Saved/SaveGames}` — "Abyssus" não é Stolen Realm (o entregável declara `%LOCALAPPDATA%Low\Burst2Flame Entertainment\Stolen Realm\Saved\`). Caminho fixo de outro produto.
A4. **Caminhos de infraestrutura errados no Teste 6**: `$KITS_DIR/../tools/automacao/runtime/coletor.py` resolve para `scratch/tools/...` (não existe; o real é `tools/automacao/...` na raiz). `$KITS_DIR/../cap1/rotina-cap1.sh` resolve para `scratch/cap1/...` (existe por coincidência).
A5. **Skip contado como PASS**: no Teste 6 o ramo "Alguns componentes faltam" chama `skip` mas incrementa `PASSED`; e o exit code final é 0 sempre que `FAILED==0`, logo etapa pulada vira entrega verde. Contraria o aceite ("etapa pulada nunca verde").
A6. **Entregável sem hashes**: seção "Hashes SHA256: A preencher" e "Hash SHA256 deste arquivo: (a ser preenchido)" — a identidade dos arquivos vivos exigida pelo cartão não foi registrada.
A7. **Política x implementação**: o entregável promete ferramenta `scratch/kit/rollback.sh`; o que existe é `snapshot.sh` (rollback como subcomando). Nome/contrato divergentes.

## Vereditos (parciais — fecham nas partes seguintes)

- C1: ACHADO (A6, + `detect-any.sh` inexistente)
- C4: ACHADO provável (A2) — confirmar por execução
- C6: ACHADO provável (A3) — confirmar
- C8: ACHADO provável (A1, A5) — confirmar por execução
- C9: ACHADO provável (A4) — confirmar por execução
- C2, C3, C5, C7, C10, C11: pendentes de execução no sandbox
