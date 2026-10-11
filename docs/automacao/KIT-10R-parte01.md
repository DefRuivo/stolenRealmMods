# KIT-10R — revisão independente (run651 ≠ implementador run646)

Cartão `t_bbad760d`. Revisor: instância nova (`run651`), perfil `default`. Rodada OFFLINE.
Lente da rodada 1 = **ARTEFATO** (leitura fria do entregável antes do resumo do implementador).
Nenhum arquivo do implementador foi editado por esta revisão (só arquivos novos do revisor em
`scratch/kit/KIT-10R-run651/` e este parecer).

## Veredito: REQUEST_CHANGES

O avaliador **tem defeitos corrigíveis que produzem FALSO OK** (verde com `prova_runtime=True`
sobre uma observação que o cartão manda NÃO passar). O núcleo (reuso por import, oráculo
independente, controles negativos) está bom, mas 3 buracos de aceitação precisam fechar antes
da aprovação.

## O que REPRODUZIU (aprovado)

| Alegação do handoff | Comando do revisor | Resultado |
| --- | --- | --- |
| SHA dos 3 arquivos | `sha256sum` | `e74771d4…`, `dd9a5c25…`, `b01919cf…` = **declarados** |
| Suite 17/17 exit 0 | `python tools/automacao/kit10/test_kit10_cenarios.py` | `TOTAL|rodaram=17 reprovaram=0` · **exit 0** |
| Isca exit 0 | `… --isca` | `ISCA|OK|defeito plantado detectado` · **exit 0** |
| Prova-RED 5/5 | `python scratch/kit/KIT-10-run/prova_red_kit10.py` | `PROVA-RED|PASSOU|5 mutacoes` · **exit 0** |
| Fixture não é verde | `kit10_cenarios.py --observacoes …/fixture.json` | `OK=0 … com prova runtime: 0` · **exit 2** |
| Reuso CIC-4 | `test_tooltips_shrines.py` | **exit 0** |
| Não toca mod/gameplay | `git status --porcelain` | só `tools/automacao/kit10/` + `docs/automacao/KIT-10-*` (untracked) |
| P5 (alvo fora da tabela) | probe do revisor | `NAO_EXERCITADO`, `prova_runtime=False` (correto) |

Os oráculos (`regras_shrine.dano`/`bonus_do_eixo`/`efeito_de_gatilho`) foram lidos: o esperado do
aspecto A/B sai de conta real do oráculo, não digitado. `bonus_do_eixo("Source", x)` devolve
`BONUS_DA_FONTE=0`, consistente com o defeito RV-34/Target.

## ACHADOS (refutação — mostrar reprovando)

Probe do revisor: `scratch/kit/KIT-10R-run651/probe_revisor.py`
(saída crua em `scratch/kit/KIT-10R-run651/probe_saida.txt`). Todos com cadeia RUNTIME completa
(identidade + sessão + evidência de arquivo), exatamente como o fechamento do AUT-7 exige.

### F1 (ALTO) — `_asp_por_evento` aceita estágio DESCONHECIDO como "evento"
`kit10_cenarios.py` só tem **blacklist** de boot (`ESTAGIOS_DE_BOOT`); a whitelist de evento
só é aplicada no ramo "sem estágio" (linha 388). Um `estagio` arbitrário (ex.: `"banana"`)
com `evento_id` cai direto no ramo OK (linha 404).
Reproduzido: `P2 estagio=banana -> OK, prova_runtime=True`.
Viola o requisito do cartão "superfícies por evento, não prefab de boot": um estágio que não é
de evento é declarado leitura de evento.

### F2 (ALTO) — `_asp_worship_dobro` devolve OK com `itens_observados` vazio/parcial
Se uma aura viva não tem item observado, o loop faz `continue` (linha 337) e nada reprova; sem
nenhum item observado, sobra `defeito=[]` → **OK**. O fechamento passa porque a cadeia da
observação existe — mas o número NÃO foi observado.
Reproduzido: `P3 worship sem itens -> OK, prova_runtime=True` e
`P3b worship item ausente -> OK, prova_runtime=True`.
Viola "Completar campos apenas necessários por caso; runtime ausente não recebe OK". É a MESMA
classe do F3 do KIT-09R ("mapas vazios recebem OK") que este cartão herdou como lição.

### F3 (MÉDIO) — `_asp_contexto_dano` ignora tooltip de buff não confere nada e ainda dá OK
Com `aura_buff` fora da tabela (ou `contrib` ausente), a guarda `if aura_buff and atributo and
aura_buff in auras …` (linha 281) não roda, o eixo `Target`/tooltip não é medido e o critério
sai **OK** sobre o lado do dano só.
Reproduzido: `P4 buff fora da tabela -> OK, prova_runtime=True`.
O cartão pede relacionar tooltip×contexto×dano; um OK sem medir a tooltip declarada superestima.

### F4 (discrepância de handoff — não é defeito de código do KIT-10)
O handoff afirma `test_estilo_atributos.py (reuso) exit 0`. Na árvore viva o revisor obteve
**exit 1** (`total: 28 | falhas: 1`; `BetterFont devia ter provas da suite pura`, linha 195 de
`tools/automacao/estilo/test_estilo_atributos.py`). O KIT-10 não toca mod nenhum nem família
`t_*`, então essa vermelhidão é de escritores concorrentes na árvore (AUT4Probe/oráculo/fixture
`.cs` modificados por outra frente) — não a atribuo ao KIT-10, mas **a evidência declarada não
reproduz** e o implementador deve reconferir/redeclarar com o estado real.

## Correção mínima exigida

1. **F1:** em `_asp_por_evento`, exigir `estagio in ESTAGIOS_DE_EVENTO` (whitelist) — estágio
   desconhecido → `NAO_EXERCITADO` (lacuna técnica), nunca OK.
2. **F2:** em `_asp_worship_dobro`, aura viva sem item observado → `NAO_EXERCITADO` (campo do
   caso ausente), nunca OK; e um controle negativo novo cobrindo mapa vazio/parcial.
3. **F3:** em `_asp_contexto_dano`, `aura_buff` declarada mas fora da tabela (ou `contrib`
   ausente) → `NAO_EXERCITADO`, nunca OK.
4. Reexecutar a prova-RED para os guardas novos (F1/F2/F3) e reconferir o reuso AUT-7 com o
   estado real da árvore, redeclarando o exit observado.

Após a correção, pedir nova revisão independente no MESMO cartão.
