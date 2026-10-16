# DBG-R2 — Parte 03: verificador, fixtures e prova vermelho→verde

Cartão `t_3b7c681b`. Aqui está a prova de que o instrumento **morde**: o verificador reprova dump
sem proveniência, e a suíte pura fica vermelha quando o carimbo ou o contrato regridem.

## 1. O verificador

`tools/verifica_proveniencia_debugger.py` — Python padrão, stdlib, sem jogo, sem rede.

    python tools/verifica_proveniencia_debugger.py <dump.log> [--alvo api/docs/target-game.json] [--json]

Vereditos: **0** COMPLETO · **2** TRUNCADO (proveniência ok, dado incompleto) · **1** REPROVADO.
Os campos exigidos e as regras de coerência estão detalhados em `docs/DBG-PROVENIENCIA.md`; a fatia
P0 da auditoria que este cartão cobre segue a tabela da parte 01 (§4).

Regras que fazem o verificador ser **fail-closed** (não apenas "checar presença"):

- campo obrigatório **ausente ou vazio** → REPROVADO (não existe campo exigido vazio que passe);
- `sha256Alvo`/`sha256Dll` fora de 64 hex → REPROVADO;
- `identidade=api` exige `apiPresente=sim`, `apiEnableHooks=sim`, `apiVersao` e `apiSha256` 64 hex —
  incoerência interna → REPROVADO;
- `estadoDump=ABERTO` com `ganchosOk` diferente do total → REPROVADO (o bloco não pode se
  contradizer);
- `alvoConforme=nao` (o hash medido diverge do alvo declarado pela API) → REPROVADO;
- `--alvo`: compara `sha256Alvo`, `versaoJogo` e `buildSteam` com `api/docs/target-game.json`;
- falta o rodapé, `estadoDump=PARCIAL`, ou `buildSteam=desconhecido` → TRUNCADO (2), porque um dump
  não fechado **não** pode ser lido como "o dado não existe";
- aviso que **não** muda o veredito: `modoLeitura=ativo` (matriz Flame aplicada = leitura não
  estritamente passiva) — aparece como NOTA, com a citação do fonte que escreve estado.

## 2. Fixtures versionadas (entrada + veredito esperado)

| fixture (`tools/testes/fixtures/`) | o que encena | veredito |
|---|---|---|
| `dbg-r2-proveniencia.entrada.log` | dump NOVO completo, `identidade=api`, 14/14 ganchos, rodapé | COMPLETO (0) |
| `dbg-r2-sem-proveniencia.entrada.log` | dump no formato ANTIGO (o que o mod emitia antes deste cartão) | **REPROVADO (1)** |
| `dbg-r2-truncado.entrada.log` | cabeçalho + estado, **sem rodapé** (sessão cortada) | TRUNCADO (2) |
| `dbg-r2-identidade-incoerente.entrada.log` | `identidade=api` com `apiEnableHooks=nao` | REPROVADO (1) |

Execução real (mesmos comandos do teste, aqui à mão, com o alvo versionado):

```
python tools/verifica_proveniencia_debugger.py tools/testes/fixtures/dbg-r2-proveniencia.entrada.log --alvo api/docs/target-game.json
  -> veredito: COMPLETO (exit 0); NOTA: modoLeitura=ativo ...
python tools/verifica_proveniencia_debugger.py tools/testes/fixtures/dbg-r2-sem-proveniencia.entrada.log --alvo api/docs/target-game.json
  -> veredito: REPROVADO (exit 1); MOTIVO: sem cabecalho de proveniencia (DBG-PROV-V1 inicio) ...
python tools/verifica_proveniencia_debugger.py tools/testes/fixtures/dbg-r2-truncado.entrada.log --alvo api/docs/target-game.json
  -> veredito: TRUNCADO (exit 2); AVISO: sem rodape `fim` ...
python tools/verifica_proveniencia_debugger.py tools/testes/fixtures/dbg-r2-identidade-incoerente.entrada.log --alvo api/docs/target-game.json
  -> veredito: REPROVADO (exit 1); MOTIVO: identidade=api sem apiPresente=sim e apiEnableHooks=sim
```

### 2.1 O caso REAL: o dump do dono hoje é REPROVADO

O `LogOutput.log` do perfil (3.407 linhas, 454 linhas de `[Skill]`) vem do mod antes deste cartão:

```
python tools/verifica_proveniencia_debugger.py \
  "$HOME/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log" \
  --alvo api/docs/target-game.json
  -> veredito: REPROVADO (exit 1)
     MOTIVO: sem cabecalho de proveniencia (DBG-PROV-V1 inicio): o dump nao diz qual build foi
             observado nem se terminou
```

Esse é o problema original, medido: **todo** dump que existe hoje é inauditável nesse sentido. A
partir da próxima sessão com o mod novo, o mesmo comando responde a pergunta.

## 3. A suíte pura

`tools/testes/regras_proveniencia.py` (biblioteca) + `tools/testes/testes/puros/t_dbg_r2_proveniencia.py`
(teste). Rodar:

    python tools/testes/roda_testes.py --teste tools/testes/testes/puros/t_dbg_r2_proveniencia.py

O teste **importa o verificador real do arquivo** (não uma cópia digitada) e cobre:

1. a marca `DBG-PROV-V1` idêntica no C# e no verificador;
2. o **contrato dos dois lados**: cada campo que o verificador exige existe como literal no C# vivo;
3. as 4 fixtures pelos vereditos certos, e o negativo pelo **motivo** certo;
4. o positivo COMPLETO com `identidade=api`, `alvoConforme=sim`, `sha256Alvo` = o do
   `api/docs/target-game.json`, `ganchosOk=14/14`, `FECHADO`, e a NOTA de passividade;
5. a ordem estática: `Proveniencia.Cabecalho()` **antes** de `AplicarPatches()`, rodapé por
   `Application.quitting`;
6. os 11 hashes das fontes intocadas (10 patches + `EfeitosInfo.cs` + `.csproj`) e a ausência de
   referência à API no `.csproj`;
7. **13 iscas** no dump positivo (campo removido, hash curto, contagem incoerente, `modoLeitura`
   inválido, `estadoDump` inválido, rodapé sem motivo, `apiEnableHooks` desligado com
   `identidade=api`, ...) — cada uma tem de reprovar;
8. 3 alvos adulterados (sha256, versão do jogo, build Steam) — cada um tem de reprovar o positivo;
9. **a fixture positiva não pode mudar de sha256** depois das iscas (nenhuma isca escreve no repo;
   elas vivem em `tempfile`).

## 4. Prova FÍSICA vermelho→verde

Evidência: `tools/testes/dbg-r2-prova-reprovando.log` (sandbox isolada em `LocalAppData/Temp`, fora
do repo; as fontes do sandbox batem sha256 com as do repo na última rodada). Quatro rodadas do
runner, sem editar o repositório:

| rodada | mutação aplicada no sandbox | resultado |
|---|---|---|
| 1 | nenhuma | **VERDE** (exit 0) |
| 2 | `Proveniencia.Marca` trocada para `DBG-PROV-V2` | **REPROVADO**: "o C# nao declara `Marca = 'DBG-PROV-V1'` — o verificador e o plugin divergiram de marca" |
| 3 | rodapé emite `razao=` em vez de `motivo=` | **REPROVADO**: "o verificador exige campo que o C# nao emite: fim: motivo" |
| 4 | `Cabecalho()` movido para **depois** de `AplicarPatches()` | **REPROVADO**: "o carimbo tem de sair ANTES dos ganchos (cabecalho@1131, patches@1101)" |
| 5 | fontes restauradas | **VERDE** (exit 0) |

Ou seja: as três decisões centrais do desenho (marca única, contrato de campo, ordem de emissão)
têm cada uma uma prova vermelha própria — e a volta ao verde é medida, não presumida.

## 5. Limites desta prova

- Tudo acima é **offline**. Nenhuma linha do carimbo foi emitida por um processo real: runtime
  **NAO_EXERCITADO** (sem abrir o jogo, por limite do cartão).
- O verificador valida o **carimbo** (presença/coerência/aderência ao alvo). Ele não recalcula o
  sha256 do `Assembly-CSharp` do jogo — quem mede isso é o plugin, em runtime.
- As fixtures foram escritas à mão no formato exato do `Proveniencia.cs`; a ligação formato↔código é
  garantida pelo contrato de campos (§3 item 2), não por uma emissão real.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
