# INT-R1-C4 — parte 04: correções da revisão da rodada 1 (2 defeitos documentais)

Cartão `t_84ca88d4`. A revisão da rodada 1 **aprovou o código** (build 0 erros; suíte 95/94/1 com o
vermelho `deploy-optin-repo` pré-existente e alheio reproduzido; equivalência confirmada por
`ilspycmd` + SHA-256; pontos presos realmente presos; fail-closed dentro de `try`/`catch`) e
**reprovou por duas afirmações falsas no próprio entregável**. As duas correções são de texto; o
código não mudou uma linha. Nada foi sobrescrito: `INT-R1-C4-parte01.md` §6 item 2 foi reescrito no
lugar (o item ERRADO não pode continuar no entregável) e o antes/depois integral está abaixo.

## 1. [ALTO] `INT-R1-C4-parte01.md` §6 item 2 — overload do `Instantiate` afirmado errado

**Texto ERRADO (antes da correção):**

> 2. **Clone com pai diferente do molde**: `UIFactory.Clone` clona com `Instantiate(template, parent,
>    false)` (`UIFactory.cs:33`); o mod usa `Instantiate(obj, parent)` (equivalente a
>    `worldPositionStays: true`). Com o MESMO pai os dois sao equivalentes na pratica; com pai
>    diferente NAO sao. Ver parte 02 para o criterio aplicado ponto a ponto.

**Por que era falso (medido, não estimado).** O overload de DOIS argumentos do jogo não é
`worldPositionStays: true` — ele cai em `false`, isto é, é literalmente a MESMA chamada que
`UIFactory.Clone` faz. Reproduzido nesta rodada, com o mesmo DLL e o mesmo SHA-256 do artefato:

```
sha256(lib/UnityEngine.CoreModule.dll) = 80d43e5f8d52964e3ec0ac514076c3e2ee032af8d9c0c3ef511dfdd9067eee8e
ilspycmd -t UnityEngine.Object C:/dev/stolen-realm/lib/UnityEngine.CoreModule.dll

  l.321: public static Object Instantiate(Object original, Transform parent)
  l.323:     return Instantiate(original, parent, instantiateInWorldSpace: false);
  l.363: public static T Instantiate<T>(T original, Transform parent) where T : Object
  l.365:     return Instantiate(original, parent, worldPositionStays: false);
```

E a diferença real do primitivo (também medida, a mesma citada na correção): o overload de
TRÊS argumentos devolve `Instantiate(original)` (sem pai) quando o pai é nulo:

```
  l.327: public static Object Instantiate(Object original, Transform parent, bool instantiateInWorldSpace)
  l.329-332:     if (parent == null) { return Instantiate(original); }
```

Enquanto `UIFactory.Clone` LANÇA em `template`/`parent` nulo: `api/Plugin/Ui/UIFactory.cs:31-32`.

**Consequência que o texto errado criava.** Como estava, o §6 declarava NÃO-equivalente um ponto que
a entrega MIGROU: `RoguelikeSkillTreeVisualizer/RemovalWindowSkillsButton.cs:232` clona com pai
(área do cabeçalho) DIFERENTE do pai do molde (botão do rodapé). Pela regra daquele §6 a migração
seria mudança de comportamento; pelo IL medido, não é. O entregável ainda se contradizia: o próprio
`INT-R1-C4-parte02.md` §1 media o contrário ("o overload de DOIS argumentos que o mod usava já é
`worldPositionStays = false`").

**Texto CORRIGIDO (agora no arquivo, §6 item 2):** resumo — o clone é **EQUIVALENTE** e por isso foi
migrado; a chamada é a MESMA para QUALQUER pai (prova reproduzida acima e em `parte02.md` §1); as
duas diferenças REAIS do primitivo são (a) o lançamento em nulo de `UIFactory.Clone` contra o
fallback `Instantiate(original)` do jogo — sem efeito, porque os 7 pontos checam pai/molde antes de
clonar — e (b) o nome do clone, que a API aplica pelo parâmetro `name` e o mod aplicava logo depois
com `clone.name = ...`.

## 2. [MÉDIO] `tools/testes/testes/puros/t_int_r1_c4_familia_ui.py:28` — contagem falsa

**Antes:** `7. AS ISCAS (caso negativo): cinco defeitos plantados EM MEMORIA tem de REPROVAR ...`
**Depois:** `7. AS ISCAS (caso negativo): oito defeitos plantados EM MEMORIA tem de REPROVAR ...`

O arquivo implementa 8 (7a com 3 casos + 7b, 7c, 7d, 7e, 7f — `t_int_r1_c4_familia_ui.py:110-171`) e
o próprio arquivo dizia 8 na META (`l.53`) e no `print` (`l.175`), e `parte03.md:13,61` também dizem
8. Agora os quatro números batem. Contagem é prova (regra 5 do cartão).

## 3. Varredura de consistência (para não sobrar eco da afirmação falsa)

```
grep -rn "worldPositionStays: true|worldPositionStays = true|cinco defeitos|pai diferente" \
     docs/automacao/INT-R1-C4-parte01.md docs/automacao/INT-R1-C4-parte02.md \
     docs/automacao/INT-R1-C4-parte03.md tools/testes/testes/puros/t_int_r1_c4_familia_ui.py \
     tools/testes/regras_int_r1_c4.py api/README.md
-> exit 1 (0 ocorrencias). A UNICA citacao que sobra do termo esta no proprio parte04.md, que o
   reproduz ENTRE ASPAS como o texto ERRADO corrigido — o entregavel (parte01..03 + teste + regras)
   nao carrega mais a afirmacao.

grep -rn "oito|8 defeitos plantados" docs/automacao/INT-R1-C4-parte03.md \
     tools/testes/testes/puros/t_int_r1_c4_familia_ui.py
-> t_int_r1_c4_familia_ui.py:28 "oito", :53 "8", parte03.md:13, :61 "8"  (todos iguais)
```

## 4. O que NÃO mudou (e por isso não foi reexecutado do zero)

* Código: zero linha alterada (as duas correções são texto/docs). O diff segue só de plumbing de UI.
* Nada do que a revisão já aprovou foi tocado: build, suíte, equivalência, pontos presos, dependência.

## 5. Medido nesta rodada (não estimado)

| Verificação | Comando | Resultado |
|---|---|---|
| Build Release sem deploy | `dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj -c Release -p:DeployToBepInEx=false` | **0 Erro(s)**, 1 Aviso MSB3277 pré-existente |
| Suíte | `python tools/testes/roda_testes.py --puros` | 95 rodaram / 94 passaram / **1 reprovou** — o MESMO vermelho `deploy-optin-repo` (sobras de scratch KIT-14, alheias) |
| Teste novo | `int-r1-c4-familia-ui` | **[PASSOU]** |
| IL (mesmo SHA-256) | `sha256sum lib/UnityEngine.CoreModule.dll` + `ilspycmd -t UnityEngine.Object` | `80d43e5f…e8e`, l.321-324 `instantiateInWorldSpace: false` |
| CI do repo | `tools/check_segredos.py` / `check_versoes.py` / `check_patches.py` / `check_dependencias.py` | exit 0 nos quatro |

Evidências: `INT-R1-C4-evidencias/08-rodada2-build.txt`, `09-rodada2-suite.txt`,
`10-rodada2-correcoes.txt`.

Runtime em jogo: **NAO_EXERCITADO** (o cartão proíbe abrir o jogo; a validação visual é do dono).

Reprovações da rodada 1 (as duas) estão fechadas; o cartão volta para revisão.
