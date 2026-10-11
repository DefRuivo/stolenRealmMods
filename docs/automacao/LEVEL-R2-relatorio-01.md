# LEVEL-R2 — relatório 01: baseline, fontes e plano de execução

Cartão: `t_918314e9` (LEVEL-R2, implementação). Workspace: `C:/dev/stolen-realm/.worktrees/level-r2`
(branch `wt/t_918314e9`, worktree linkado, `.git` presente no início do run).
Modelo: deepseek-flash / provider deepseek. Deploy: **nunca** (`-p:DeployToBepInEx=false`); jogo não é aberto;
perfil/saves do dono não são tocados.

## 1. Fontes lidas (não copiadas para o repo)

Pacote do pai `t_8d6efbf5` via `kanban_attachments(task_id='t_8d6efbf5')` →
`C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_8d6efbf5\LEVEL-R1-entrega.zip`
(66020 bytes, sha256 `2cfe27a6c39187a50dd00313ccfe4692d0ee9ee530427eef32a73aeb63d2c69e`).

Extraído **fora do worktree**, no scratch desta instância:
`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/level-r2-src/` (21 membros, CRC OK no unzip).
O scratch temporário do pai **não** foi usado.

Partes lidas: 01…08. Normativas: **parte05** (especificação) com emendas da **parte06** (prevalece);
parte07 = índice. `evidence/root-result.il.txt` lido integralmente (629 linhas; método
`Root::SendGameCompleteFromServer`, bloco alvo IL_0092..IL_00a8).

## 2. Baseline técnico do ambiente

- `dotnet --info`: SDK **6.0.428** (Base Path `C:\Program Files\dotnet\sdk\6.0.428`) — é o único SDK instalado.
  Consequência: o harness de testes precisa mirar **net6.0** (não net8).
- `lib/` está no `.gitignore` na raiz do repo → o worktree **não** tem `lib/`. As referências do novo
  `.csproj` apontam para `..\..\..\lib` (a `lib` comum do repo principal, `C:/dev/stolen-realm/lib`),
  em modo **leitura externa**, sem copiar DLL para dentro do worktree.
- DLL de referência analisada: `C:/dev/stolen-realm/lib/Assembly-CSharp.dll`. Hash exigido pela
  especificação: `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`
  (conferido no relatório 02).

## 3. Plano (ordem canônica do cartão)

1. Conferir hash da DLL de referência; materializar a pasta nova do mod.
2. Spike de harness: carregar `Assembly-CSharp.dll` em processo .NET 6 e obter o IL real de
   `Root.SendGameCompleteFromServer` **sem** abrir o jogo (Harmony `PatchProcessor.GetOriginalInstructions`).
   Se falhar 2x, mudar de abordagem (ex.: leitura por metadata) em vez de insistir.
3. Núcleo do mod: `Plugin/HarmonyBootstrap`, `Policy` (teto/avanço/guarda numérica), `XpBackend`
   (F20/D20 reais, extensão linear, inversa), `Ledger` (sidecar v1, escrita atômica),
   `RewardPolicy` (level de consulta), patches (transpiler do resultado, getter `MaxLevel`,
   XP escopado, `ExperienceLevelDidSet`, UI, recompensas).
4. Build real `-p:DeployToBepInEx=false` + harness real exercitando: matriz de níveis, guardas,
   roundtrip/inversa de XP, ledger (reload/corrompido/falha de escrita/reset), config menor,
   correspondência estrutural única do transpiler sobre o IL real do jogo.
5. Relatórios numerados 02…N com provas de execução, hashes, NAO_EXERCITADO explícito, e pacote
   de revisão (sem DLL de jogo/corpus).

## 4. Regras de operação deste run

- Não sobrescrever relatórios: cada arquivo novo é numerado (`LEVEL-R2-relatorio-NN.md`).
- Não usar `execute_code` headless; executar via terminal/harness real.
- Comando que falha 2x → troca de abordagem.
- Nenhum PASS fabricado: o que não for exercitável é declarado `NAO_EXERCITADO` com motivo.
