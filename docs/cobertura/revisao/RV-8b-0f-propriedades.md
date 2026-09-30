# RV-8b-0f — Propriedades da ação (habilitador)

> Entregue 29/09. Fecha a classe de dúvida que **não é atributo**: limite de alvos,
> alcance, knockback, nº de golpes, cooldown, cargas, condição de uso, status aplicado,
> chance de proc e gatilho.

## O que o dump passou a trazer

Duas linhas novas no `LogOutput.log` (dump de boot do `RoguelikeDebugger`):

| linha | nº | o que traz |
|---|---:|---|
| `[ActionProps] 'nome'` | **276** | tipo, benefício, alvos (`Selection`, `RangeSelection`, `Blast`, `SimpleRange`, flags `ali`/`ini`/`self`), alcance, knockback, nº de golpes, cooldown, cargas, condição de uso + texto de falha, `statusAplicados`, `statusFonte`, `chances` |
| `[Trigger] 'nome'` | **76** | `TriggerType`, `Condition`, `AddBasicAttackToActionList`, `GeneralEffects` |

## Correção de uma anotação minha

O `RangeAdderAttributes` que eu tinha registrado no quadro como "campo do `ActionInfo`"
**não é** campo público: é `Dictionary<DamageType, string>` **privado** do
`ActionProperties` (l.317488) — um cache de nome de atributo. O "alcance por hex" chega
por **atributo** (`Patient Hunter` concede `RangeTypeAdderRanged`), e isso o campo
`attr` do dump de skill já cobria desde o RV-8b-0.

## Os 3 abertos do Ranger

### `Marked Prey` — RESOLVIDO, e o texto está certo

```
[Trigger] 'Marked Prey' | tipo=OnHittingDamaging | cond= | addBasicAttack=nao
```

A dúvida era se "Attacks now apply Marked Prey" prometia demais (se o gatilho fosse só
ataque básico). Não promete: `OnHittingDamaging` = **qualquer hit que cause dano**. Não
existe valor `OnBasicAttack` no enum (são 29, de `OnHittingAny` a
`OnGettingHitAnyIncludingProcs`) — quem decide é este par. E o `addBasicAttack=nao` é da
outra flag (`AddBasicAttackToActionList`): ela controla a **lista de ações** que o
gatilho executa, não a condição de disparo. Ler isso como "só ataque básico" seria erro.

### `Rally` — RESOLVIDO no valor: é **+3**, não +2

```
[ActionProps] 'Rally' | tipo=FreeAction | nAlvos=1 | alvos=[...;range=0;ali=0;ini=0;self=1] | cooldown=3
[Status] 'Rally' | efeitos=TurnFreeMovementPoints:Base:3 | efeitosDano=Target['FreeMovementPoints'] = Target['FreeMovementPoints'] + 3
```

O `+3` mora num **status**, não num `GeneralEffect` — por isso a ação do `Rally` tem
`nEfeitos=0` e o dump anterior não respondia. A wiki (v.19) dizia 2: **perdeu pela 4ª
vez**. Fonte do valor: o asset do status, dentro do jogo.

**Aberto novo, achado por este dump:** a ação tem `self=1` (só em si) enquanto o texto
promete "all allies within 4 hexes". `ITargetInfo` tem **uma única** implementação no
assembly (`TargetInfo`), então não é cast faltando — ou o alcance de área vem de outro
lugar que ainda não despejo, ou o texto promete mais do que a ação faz. **Precisa de
teste em jogo:** dar `Rally` ao lado de um aliado e ver se ele recebe o buff.

### `Volley` — não é legível pelo dump

```
texto do jogo : Shoot up to 5 enemies near the target area ...
texto da wiki : 3
[ActionProps]  : nAlvos=1 | alvos=[...;range=8;ini=1] | blast vazio | hits=- | chances vazio | statusAplicados vazio
```

A contagem de alvos não está em nenhum campo público da ação. Fica valendo **o texto do
jogo** (fonte primária) contra a wiki (v.19, que já perdeu 4 vezes) — e a limitação fica
registrada, em vez de virar "corrigido" sem prova.

## Classe nova medida: chance de proc

76 gatilhos despejados; **10** usam `Source.GetRollResult(N)`:

| skill | chance | tooltip diz? |
|---|---:|---|
| `Reverberate` | 33% | sim |
| `Show Stopper` | 25% | sim |
| `Aid` · `Harm` · `Thunder Struck` | 10% | sim |
| `Circle of Life` · `Echo` · `Fabricate` · `Fade` · `Quick Hands` | 50% | sim |

**As 10 já dizem o número na tooltip — zero pendência nesta classe.**

## Como reconferir

```bash
bash scratch/test-cycle.sh 30 "Debugger"     # abre e fecha o jogo
python scratch/analisa_2f.py                 # lé o log e reconfere estes 3 casos
```
