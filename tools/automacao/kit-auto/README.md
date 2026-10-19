# kit-auto — bancada de auto-avaliação do kit (KIT-AUTO)

Avalia o kit sem humano: sobe a bancada isolada, aciona as ações do kit pelo driver interno
(`auto-command.txt` lido no `PostLateUpdate`, guardas reais, opt-in `[AutoAvaliacao] habilitado=true`),
coleta o log do RoguelikeDebugger e os artefatos do kit, e assere sobre eles. Não usa `computer_use`,
não injeta input do SO, não deploya no perfil do dono, não publica e não concede aceite
(`kit_verdict=NOT_GRANTED`).

    python tools/automacao/kit-auto/runner.py run                     # bancada completa (2 boots)
    python tools/automacao/kit-auto/runner.py evaluate --out <boot01> # reavalia evidência (não abre o jogo)
    python tools/automacao/kit-auto/test_auto.py --evidence <boot01> --out <dir-novo>
    python tools/automacao/kit-auto/test_live_contract.py             # contrato foco/heartbeat (offline)
    python tools/automacao/kit-auto/prove_guard.py                    # defeito plantado na guarda (offline)
    python tools/automacao/kit-auto/prove_live_contract.py            # defeitos plantados no contrato (offline)

## Pré-requisitos de ambiente (a bancada espera, nunca força)

O despacho interno usa o MESMO guard do atalho (`ProcessarAcao -> GuardBloqueia`), então:

- **desktop interativo** (sessão com tela; RDP desconectado/serviço não serve);
- **a janela do jogo precisa assumir o primeiro plano** sozinha depois do launch do Steam;
- **não interagir com outras janelas durante o run** — clique/troca de foco derruba
  `foco_no_jogo` e a bancada para de despachar;
- foco **nunca** é forçado: `SetForegroundWindow`/clique/`computer_use` é input sintético, proibido;
- um boot por caso, sensível a timing (≈3–5 min por run completo);
- jogo fechado no início, Cloud do app 1330000 OFF, `dotnet` no PATH, `lib/` com os assemblies do jogo.

Quando o pré-requisito não é atendido, o run NÃO é reportado como falha de avaliação: aborta com
`exit 2` / `outcome=environment_prerequisite_unmet` e nomeia a causa (`blocked_reason` =
`focus_not_granted`, `focus_lost`, `live_engine_stalled`, `live_engine_never_fresh`) em
`RESULTADO.json` e no `result.json` do boot. Defasagem curta de heartbeat (carregamento) é tolerada
(8 amostras consecutivas, idade > 5 s). Detalhes: `live_guard.py` e §6 da entrega.

Exit codes: 0 = asserções verdes e contraprova vermelha pelo motivo certo; 1 = asserção falhou;
2 = evidência inutilizável/erro **ou** pré-requisito de ambiente não atendido (ver `outcome`);
3 = boot bloqueado por ambiente (processo filho). Entrega e matriz: `docs/automacao/KIT-AUTO-entrega.md`.

Requisitos: jogo fechado, Cloud do app 1330000 OFF, `dotnet` no PATH, `lib/` com os assemblies do
jogo. Insumos são pinados por SHA-256 em `dependencies.json` e `frozen-inputs.json`; drift aborta o
run antes do build.
