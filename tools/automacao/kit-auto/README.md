# kit-auto — bancada de auto-avaliação do kit (KIT-AUTO)

Avalia o kit sem humano: sobe a bancada isolada, aciona as ações do kit pelo driver interno
(`auto-command.txt` lido no `PostLateUpdate`, guardas reais, opt-in `[AutoAvaliacao] habilitado=true`),
coleta o log do RoguelikeDebugger e os artefatos do kit, e assere sobre eles. Não usa `computer_use`,
não injeta input do SO, não deploya no perfil do dono, não publica e não concede aceite
(`kit_verdict=NOT_GRANTED`).

    python tools/automacao/kit-auto/runner.py run                     # bancada completa (2 boots)
    python tools/automacao/kit-auto/runner.py evaluate --out <boot01> # reavalia evidência (não abre o jogo)
    python tools/automacao/kit-auto/test_auto.py --evidence <boot01> --out <dir-novo>
    python tools/automacao/kit-auto/prove_guard.py

Exit codes: 0 = asserções verdes e contraprova vermelha pelo motivo certo; 1 = asserção falhou;
2 = evidência inutilizável/erro. Entrega e matriz: `docs/automacao/KIT-AUTO-entrega.md`.

Requisitos: jogo fechado, Cloud do app 1330000 OFF, `dotnet` no PATH, `lib/` com os assemblies do
jogo. Insumos são pinados por SHA-256 em `dependencies.json` e `frozen-inputs.json`; drift aborta o
run antes do build.
