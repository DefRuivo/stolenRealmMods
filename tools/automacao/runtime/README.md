# AUT-4 — runtime (coletor/driver opt-in)

Coleta runtime por objetos Unity para o AUT-4. **Nada aqui abre o jogo sozinho**: a execução em
jogo é a próxima rodada autorizada (ver `docs/automacao/AUT-4-preparacao.md` e `AUT-4-estado.json`).

## Testes offline (sem jogo)

```bash
python tools/automacao/runtime/roda_testes_runtime.py              # suite (exit 0/1/2)
python tools/automacao/runtime/roda_testes_runtime.py --contra-prova  # iscas TEM de reprovar
```

## Compilar o probe (sem deploy)

```bash
cd tools/automacao/runtime/AUT4Probe && dotnet build -c Release AUT4Probe.csproj
```
O csproj **não tem alvo de deploy** — compilar não escreve no perfil do dono.

## Driver (default OFFLINE)

```bash
# default: NAO_EXERCITADO (exit 2), sem tocar em jogo
python tools/automacao/runtime/coletor.py --plano tools/automacao/runtime/fixtures/plano-exemplo.entrada.json

# só a rodada autorizada (próxima etapa) acrescenta --autorizado --jogo-disponivel --confirmar-coleta coleta
```

## Costura e rodada executavel (CIC-5)

- `--saida-probe <aut4probe.json>`: consome o JSON **REAL** do probe, injeta `sessao`/`hash_fonte` do
  topo em cada observacao (B1), preserva os 5 campos extras (B2) e consolida por **campo-alvo** (B3).
  Fixture rotulada sai `FIXTURE` (exit 2) — nunca runtime.
- `--executar` (**gated**): instala o probe no perfil isolado, escreve o `.cfg` derivado, lanca pelos
  argumentos de doorstop, espera ESTADO e faz o rollback EXATO no `finally`. Sem `--autorizado`,
  `--jogo-disponivel` e `--confirmar-coleta coleta` **NAO age** (`NAO_EXERCITADO`, exit 2).
- Detalhes e provas: `docs/automacao/CIC-5-entrega.md`.

## Regras

- Toda observação tem **procedência** (`runtime` | `fixture`); fixture nunca é evidência de jogo.
- `AUSENTE`/`INDETERMINADO`/`NAO_EXERCITADO` **nunca** contam como OK.
- O probe lê do **objeto vivo** (não de pixel/OCR); o PNG sai pela API do Unity (`ScreenCapture`).
- Ao fim da rodada: consumir `manifest` + `rollback` e restaurar/remover **exato** o que a rodada criou
  (inclusive o `.cfg` que nasce sozinho).
