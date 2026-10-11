# KIT-06F — parte 07: correcao do F6 no caminho ANINHADO (rodada de retorno)

Origem: revisao independente do KIT-06F (run645 != implementador run641) em
`docs/automacao/KIT-06F-revisao.md`. Rerodada como run650 no mesmo cartao
(t_73f0779f), perfil default. 7 de 8 achados reconferidos OK pelo revisor; ele
BLOQUEOU o F6 no caminho aninhado. Esta parte documenta so essa correcao.

## Achado (reproduzido, nao pelo resumo)

`_coleta_documento` (py) e `ColetaDocumento` (C#) colocavam `eventos`/`capturas`
do pipeline por REFERENCIA: os acessores `eventos()`/`Eventos()` devolvem copia
RASA (o dict de topo e novo, mas `dados`/`quadro` ANINHADOS continuam sendo os
objetos internos do pipeline). Efeito: mutar
`doc["coleta"]["eventos"][i]["quadro"|"dados"]` corrompia a EVIDENCIA INTERNA do
pipeline e TODOS os exports seguintes (o consumidor "hostil" envenenava a
propria prova). O aceite do F6 exige snapshots defensivos "inclusive objetos
ANINHADOS quando necessario"; o caso plano (`marcacoes`) ja estava corrigido.

## Correcao (raiz, nos dois caminhos)

- Python: helper `_copia_profunda` (espelha `CopiaValor` do C#) aplicado a TODA
  estrutura derivada do pipeline que entra no documento: `resumo`, `eventos`,
  `degradacoes`, `rejeitados`, `lacunas`, `capturas`; e a `trilha_controle`
  (eventos de controle com `contexto` aninhado, mesma classe de defeito).
- C#: `ColetaDocumento` passa a devolver `CopiaValor(...)` de
  `Resumo()/Eventos()/Degradacoes()` do pipeline (`CopiaValor` e o helper
  recursivo ja existente para dicts/listas aninhados).
- Doc parte05 corrigida: a afirmacao "DocumentoExport usa essas copias" agora
  vale tambem para `coleta` (antes valia so para marcacoes/degradacoes/trilha).

## Prova negativa por EXECUCAO (reprovar ANTES, discriminar DEPOIS)

Probe do revisor preservado verbatim — Python `probe_f6_aninhado.py` e C#
`cs-probe/` (run645), sem alterar uma linha:

- Python, fonte PRE-correcao (run641 sem a copia profunda, gerado em
  `antes-prefix/` por `gera_prefix.py`): `campos contaminados = 4`,
  VEREDITO "PROPAGACAO INTERNA DETECTADA", **exit1** (`probe-antes.log`).
- Python, fonte VIVO: `limpos=6 contaminados=0`, "sem propagacao interna",
  **exit0** (`probe-depois.log`).
- C#, fonte PRE-correcao (`antes-cs/`, so o adapter revertido): `campos
  contaminados = 2`, "PROPAGACAO INTERNA DETECTADA", **exit1** (`csprobe-antes.log`).
- C#, fonte VIVO: `campos contaminados = 0`, **exit0** (`csprobe-depois.log`).

Teste novo e isca (nesta rodada):

- `TestCorrecoesKit06F.test_F6_coleta_aninhado_snapshot_defensivo` (suite py).
- Isca `coleta_aninhado_por_referencia` na contra-prova: reverte
  `bloco["eventos"] = _copia_profunda(eventos)` -> `= eventos`; exige o conjunto
  EXATO `{test_F6_coleta_aninhado_snapshot_defensivo}` reprovando. `[OK]`.
- C#: `VerificaEvidenciaDefensiva()` no harness, IDs
  `evidencia.coleta_aninhado_somente_leitura` e
  `evidencia.coleta_dados_somente_leitura`. Isca C# = build do MESMO harness
  contra o adapter PRE-correcao: NORMAL `44 OK / 2 FALHA` **exit1** (os 2 IDs
  novos reprovam) e `--defeito guard` **exit1** recusando 2 falhas EXTRAS
  (`harness-prefix-normal.log`) — sem falso verde. Contra o adapter vivo:
  `46 OK / 0 FALHA` **exit0**.

## Comandos -> exit (run650, TEMP/TMP/TMPDIR no scratch da tarefa)

```
python tools/automacao/kit06/teste_controle_acesso.py            -> Ran 46 tests OK exit0
python tools/automacao/kit06/contra_prova_kit06.py               -> 38 iscas, 0 falhas exit0
python tools/automacao/kit06/contra_prova_kit06.py --autoteste   -> 9/9 exit0
bash   tools/automacao/kit06/roda_testes_kit06.sh                -> VERDE exit0
python scratch/kit/KIT-06R-run638/test_revisao_kit06.py          -> 14/14 exit0   (oraculo py do revisor)
dotnet run --project scratch/kit/KIT-06F-run650/oraculo-cs -c Release
                                                                 -> 12 OK/0 FAIL exit0 (oraculo C# do revisor)
python scratch/kit/KIT-06R-run645/probe_f6_aninhado.py           -> exit0  (probe py do revisor)
dotnet run --project scratch/kit/KIT-06F-run650/cs-probe -c Release
                                                                 -> exit0  (probe C# do revisor)
dotnet run --project tools/automacao/runtime/harness-controle -c Release
                                                                 -> 46 OK/0 FALHA exit0
dotnet run ... -- --defeito guard                                 -> 3 falhas EXATAS exit0
dotnet run ... -- --defeito inventado                             -> exit2 (nome nao suportado)
dotnet build <sandbox>/.../KIT04Adapter.SR.csproj -c Release -p:DeployToBepInEx=false
                                                                 -> 0 Erros, 65 Avisos exit0 (DLL na copia)
preflight deploy default/true/false                               -> sentinela ausente/escrita/ausente
perfil do dono (plugins+scripts) antes/depois                     -> hash IDENTICO
```

Cobertura negativa medida por AST (script independente do revisor): 46 testes,
38 mutacoes, uniao 46, 0 testes sem prova negativa, 0 nomes fantasma.

## Hashes (sha256sum)

```
379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457  tools/automacao/runtime/controle_acesso.py
cad1bcc26cf10d4d754e8e96c076fc39c6dd13ca05486dbe73581e0163cc9084  tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs
e864ac9dbf86dba3403986b8bd6d5adfc43f9caf80a5f0672a927df1a9aebe81  tools/automacao/runtime/harness-controle/Program.cs
375edb6f28c1de10b2346ebc3aab248abc2f5be36caf9771e9b0eaff32e2b1fa  tools/automacao/kit06/teste_controle_acesso.py
d4a2cbb77313e3d63ceb7fb41869cc006e4eaa16375d53e27d77287321a7fbc4  tools/automacao/kit06/contra_prova_kit06.py
```

## Limites

UI real/input do engine/runtime/pixels: NAO_EXERCITADO (KIT-G2). Sem instalar,
abrir/fechar jogo, save, foco, publicacao, Assembly-CSharp.dll, Bard, gameplay.
Sem commit/add/push. KIT-07 sem integracao efetiva (gate nao satisfeito).
A reconferencia final e do revisor em NOVA instancia.
