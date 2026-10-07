# RV-29 — a linha de auras de shrine só sai quando o personagem TEM a aura viva

Cartão: `t_8f1b6e7d` · Nota de fechamento do implementador · 07/10/2026

Esta nota responde aos três entregáveis do cartão: (1) onde está o filtro pelo estado vivo, (2) qual é o
**critério de match** do status usado como filtro, (3) o resultado da conferência de **semântica**
(entra / sai / nunca entrou / aura de outro membro) e o **roteiro** dos 4 cenários de aceite.

---

## 1. O que a linha faz hoje (o filtro vive em `AurasVivas`)

Arquivo: `BetterTooltips/Patches/ShrineAuraPatch.cs` (fonte VIVO do mod).

* `AcumuladoShrines(chaveDaTooltip)` monta a linha azul. Ela **não** decide mais o conteúdo pela
  definição do shrine aberto (o defeito antigo). O portão de visibilidade é:
  `List<ActionStatus> ativas = AurasVivas(receptor);` e, se `ativas.Count == 0`, devolve `""` — sem
  linha nenhuma — e loga `RV-31 sem linha: <char> nao tem aura de shrine viva agora`.
* `AurasVivas(receptor)` lê a **lista VIVA do PRÓPRIO personagem em foco**
  (`receptor.ActionStatuses`) e devolve só os status de aura de shrine que ele está recebendo **agora**.
* O **valor** continua saindo do caminho já correto: o total do indexador do motor
  (`Character[atributo]`) e a contribuição das auras do `ActionStatusInfo.AttributeEffects` REAL,
  avaliada pelo interpretador do jogo. **Nada** é derivado da `ActionStatuses`: ela é usada **somente
  como predicado de visibilidade**, exatamente como o cartão pede.

O filtro por personagem é o vínculo da RS-29: `AurasVivas` nunca varre `AllCharacters` — com dois
personagens na mesma aura, cada um conta a aura UMA vez com o próprio `ShrineEffectBonus`. Isso está
preso por teste (`tools/testes/testes/puros/t_shrine_dois_personagens.py`), inclusive com isca embutida
que faz `AurasVivas` ler `AllCharacters` e exige que a checagem REPROVE.

## 2. Critério de match do status (não é heurística de nome solta)

O match é por **igualdade exata de `ActionStatusInfo.Description`** contra o conjunto `ShrineKeys`
(`ShrineAuraPatch.cs`, as 12 strings). A justificativa de ser o critério do JOGO:

* a `Description` do status de aura é **o mesmo texto que o tooltip do shrine mostra** — o hover do
  ground effect lê `GroundEffectInfo.ActionStatuses[0].Description` (decompilado `Tooltip`
  l.214180), que é o objeto cujo `Description` é o `ShrineKeys`;
* é o **mesmo conjunto** que o `LocalizePatch` usa como pré-filtro de família — não há uma lista
  paralela que possa divergir;
* é igualdade de string **exata** (Ordinal) contra um conjunto fechado, não `Contains`/substring nem
  nome de aura por partes.

Observação de escopo: esta é uma decisão do projeto (RV-31/RV-46) e **supera** o recorte mais estreito
esboçado no corpo original do cartão ("a aura DESTE shrine"). A linha se chama *"Your active shrine
auras"* no plural e agrega **todas** as auras de shrine vivas do personagem em foco — mas continua
saindo **só** quando ele tem pelo menos uma. Se o dono quiser o recorte por shrine, é mudança de escopo
(pedir cartão novo), não deste filtro.

## 3. Semântica conferida contra o motor (entra / sai / nunca entrou)

Verificado no código do jogo (decompilado nesta rodada com `ilspycmd` sobre `lib/Assembly-CSharp.dll`;
dump em `scratch/rv29/`). O status da aura é criado **por personagem**, contra o `Source` do ground
effect (o shrine), quando o personagem entra na área:

| Pergunta | Resposta do motor | Fonte |
|---|---|---|
| Entra na área → ganha o status? | **Sim.** `GameLogic.ProcessGroundEffects` vê que a célula do personagem é afetada e chama `GroundEffect.AddGroundEffectedPlayer` → `GameLogic.CreateActionStatus(Source, player, statusInfo, …)`. | `GameLogic.cs` l.5560-5664 (add em l.5655) · `GroundEffect.cs` l.102-172 (criação em l.158) |
| Sai da área → perde o status? | **A saída da área tira o personagem de `EffectedPlayers`, mas só REMOVE o status quando `ActionStatusInfo.Infinite`.** As auras de shrine **não** são `Infinite` → o status **permanece até a própria duração expirar**. Ou seja: a linha desaparece quando o motor realmente remove o status — que é a leitura CORRETA do estado vivo (enquanto o status existe, o motor ainda aplica o efeito). | `GroundEffect.cs` l.174-216 (guard do `Infinite` em **l.206**) · chamada em `GameLogic.cs` l.5659 |
| Nunca entrou na área? | **Nunca ganha status** (`AddGroundEffectedPlayer` nunca roda) → **nunca** sai linha. | idem acima |
| Aura concedida a outro membro do party → o personagem em foco ganha? | O status é criado **por personagem que entra**, contra o `Source` do ground effect, independente de quem ativou o shrine. Ativar o shrine (`GroundEffect.Activate`) só cria o visual. Então: quem entra recebe o próprio status e é ele quem mostra a linha — cada um com o próprio `ShrineEffectBonus`. | `GroundEffect.cs` l.297-308 (Activate) · `GameLogic.cs` l.5600-5660 (laço por personagem) |

O caso "personagem que SAI" foi conferido **na prática pelo dono em 06/10** (comentário no cartão:
"com o personagem DENTRO da aura a linha sai correta, e FORA da aura ela nao aparece. O ciclo entrar/sair
foi conferido na pratica"). O matiz do `Infinite=False` (a saída imediata não remove o status) é a
explicação do porquê de a linha refletir o **estado vivo** e não o passo do personagem — coerente com o
que foi visto em jogo.

## 4. Evidência medida em jogo (log real, não sintético)

`scratch/cap1/out/log-anterior-antes-da-rotina.log` (log de boot real, BepInEx 5.4.23.5, 12/09/2026):

* **11** linhas `RV-31 sem linha: Necrodancer nao tem aura de shrine viva agora (tooltip '…')`
  → o **mesmo** personagem, sem aura viva, NÃO recebe linha;
* **91** linhas `RV-31 acumulado: auras=[…] char=Necrodancer bonus=… -> …` → o **mesmo** personagem,
  com aura viva, recebe a linha com o valor.

Mesmo personagem nos dois estados = o filtro responde ao estado vivo, não ao shrine aberto.
(`grep -c "RV-31 sem linha" …` = 11; `grep -c "RV-31 acumulado" …` = 28 no arquivo, 91 ocorrências de
`char=Necrodancer`.)

## 5. Roteiro da conferência humana (os 4 cenários de aceite)

Pré-requisito: `bash scripts/artefatos-conferencia.sh` (lê o disco, prova que a DLL instalada é a do
repo). Referência de número esperado: `docs/CONFERENCIA-DONO-06-10.md` §4 (tabela base → bônus).

1. **FORA da aura** — parar o personagem em foco fora da área do shrine e hover no shrine.
   *Esperado:* a linha `Your active shrine auras:` **não aparece**.
2. **ENTRA na aura** — mover o personagem para dentro da área, terminar o movimento e hover de novo.
   *Esperado:* a linha aparece, com o valor da tabela (ex.: Rogue base 20; com bônus +100 → 40).
3. **SAI da aura** — sair da área. *Esperado:* a linha some (quando o motor remove o status; ver §3).
4. **Troca de personagem em foco** — alternar o personagem em foco (A dentro da aura, B fora) e hover
   nos dois. *Esperado:* cada um mostra (ou não) a SUA linha, com o SEU número e o SEU `bonus=` — sem
   resíduo do anterior (nem linha sobrando, nem valor do outro).
5. **Não regredir o defeito antigo** — com o personagem dentro da aura, os números continuam corretos
   (inclusive variando com o turno/stack), como em §4 de `docs/CONFERENCIA-DONO-06-10.md`.

No log (`BepInEx/LogOutput.log`, chave `[Shrine RV-23]`): o cenário 1/4 emite
`RV-31 sem linha: <char> nao tem aura de shrine viva agora`; o 2/4 emite
`RV-31 acumulado: auras=[…] char=<char> bonus=<b> -> …`.

## 6. Estado do artefato (medido nesta rodada)

* **Fonte compila**: `dotnet build -c Release` em `BetterTooltips/` → **0 erros** (1 aviso pré-existente
  de `System.Net.Http`).
* **DLL instalada == build do repo**: sha256 da `BetterTooltips.dll` do perfil
  (`…/profiles/Default/BepInEx/plugins/BetterTooltips/BetterTooltips.dll`) =
  `6533f4368ec75c68caa2a3e51fbc1f2e74bed9f7b905d2ba055b890aee8ec7d`, **byte-idêntica** à Release
  recém-construída. Ou seja: o filtro do RV-29 **está no jogo** que o dono conferiu.
* **Testes puros**: `python tools/testes/roda_testes.py --puros` → **93 rodados, 93 passaram, 0
  reprovaram** (1 excluído por categoria: `jogo`). Inclui toda a família de shrines:
  `t_shrine_dois_personagens`, `t_shrine_contra_prova`, `t_shrine_excesso_*`,
  `t_rv50_shrine_personagem`, `t_rv30_shrine_fonte`.

## 7. O que ainda depende do dono (gate humano)

Os cenários 1-3 já têm aceite registrado em jogo (06/10). Falta o **eyeball final** do dono no cenário
**4** (troca de personagem em foco sem resíduo) e a reconfirmação de 1-3 na sessão única de fechamento
de `docs/CONFERENCIA-DONO-06-10.md` §4/§6. Nada de código pendente.
