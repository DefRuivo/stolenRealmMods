# INT-R1 — parte 06: fecho, aceite e como reconferir

## 1. Veredito da tarefa

A API-R1 **substitui** muito pouco do que existe hoje — e isso é o achado principal, não um fracasso.
Medido: a base 0.1.0 entrega **4 hooks observacionais** que não alteram argumento nem resultado
(`api/Core/Contracts.cs:58-66`; `api/README.md:42,145-146`). Quase toda frente viva do projeto **muta**
estado (reescreve texto, muda UI, clica, dirige jogo), o que está fora do contrato observacional.
Onde a API **tem** valor, ela tem valor alto e específico:

1. **Proveniência/identidade fail-closed** — resolve a lacuna nº 1 da auditoria do debugger ("qual DLL
   observou") → **C3**.
2. **Família `UI` do inventário** — cobre literalmente a plumbing de UI mais cara do repo (RSTV) → **C1**,
   com consumidor **C4**.
3. **Hook `ui.localized`** — transforma cobertura de tabelas de texto em medição → **C5**.
4. **Contrato único** entre o núcleo da API e o SDK do kit — hoje há duplicação real → **C2**.

E **não** vale migrar: BetterFont, BetterStats, BetterCombatText, o patch do BetterTooltips, os 14 ganchos do
debugger, o clique do AUT4Probe, os censos, os scripts offline, a auditoria de tooltips e todos os gates
humanos — cada um com o motivo escrito na parte 05 §2.1.

## 2. Aceite pedido × entregue

| Pedido | Onde está | Estado |
|---|---|---|
| Partes numeradas | `INT-R1-parte01..06.md` (6 arquivos novos) | ENTREGUE |
| Matriz frente × API × ganho × risco | parte 02 §1 (18 linhas) + priorização por ganho×risco (parte 02 §2) | ENTREGUE |
| Cartões criados com dependência explícita | parte 05 §1 — 6 cartões (`t_9fa61e7e`, `t_2ea91249`, `t_3b7c681b`, `t_84ca88d4`, `t_c6b435f8`, `t_ee99ccc4`) + grafo | ENTREGUE |
| Lista do que não vale migrar e por quê | parte 05 §2.1 (13 linhas) + §2.2 | ENTREGUE |
| Método (a)..(e) por frente | parte 02 §1 (colunas "como é hoje / com a API / ganho / risco / custo") | ENTREGUE |
| ADENDO 1 — 4 baldes p/ tudo vivo | parte 03 §1 (33 linhas) + contagens por balde + checklist dos 6 itens confirmado/refutado/ampliado (§2) | ENTREGUE |
| ADENDO 2 — mod a mod, 6 campos | parte 04 (7 mods × (a)..(f)) + resumo de vereditos (§8) | ENTREGUE |
| Limite "não migrar nada nesta tarefa" | respeitado: nenhum mod editado, nenhum deploy, jogo não aberto, nenhum arquivo existente sobrescrito | CUMPRIDO |

## 3. Como reconferir (comandos reais desta rodada)

```bash
# 1) Os 4 hooks e a natureza observacional da API
sed -n '58,66p'   /c/dev/stolen-realm/api/Core/Contracts.cs
sed -n '42,42p;67,68p;145,146p' /c/dev/stolen-realm/api/README.md

# 2) Tamanho do inventário e as 7 famílias (contrato NÃO implementado)
python -c "import json;d=json.load(open('api/docs/contract-inventory.json',encoding='utf-8'));print(d['counts'])"

# 3) Os 21 cartões vivos e os 6 novos
python -c "import sqlite3;c=sqlite3.connect(r'C:\Users\Pichau\AppData\Local\hermes\kanban.db');print([r for r in c.execute(\"select id,status,title from tasks where status not in ('done','archived') order by id\")])"

# 4) Tamanho de cada mod (linhas de .cs) e ausência de BepInDependency
for m in BetterCombatText BetterFont BetterStats BetterTooltips RoguelikeDebugger RoguelikeSkillTreeVisualizer ReloadProbe; do find $m -name '*.cs' | xargs wc -l | tail -1; grep -rc 'BepInDependency' $m --include=*.cs | grep -v ':0'; done

# 5) ReloadProbe: defasado JÁ tratado (não gera cartão)
git -C /c/dev/stolen-realm check-ignore -v ReloadProbe/ReloadProbe.csproj
git -C /c/dev/stolen-realm ls-files ReloadProbe | wc -l    # -> 0

# 6) Anexos que fundamentam o ADENDO 1 (LANG-R1 e DBG-R1)
head -1 "$HOME/AppData/Local/hermes/kanban/attachments/t_2a6474ff/localizacao-ptbr.csv"
head -40 "$HOME/AppData/Local/hermes/kanban/attachments/t_2a6474ff/relatorio-suspeitos.md"
```

Contagens fechadas desta rodada: **553** cartões no banco (424 arquivados, 108 done, 21 vivos → 27 depois
desta rodada); **18** linhas na matriz; **33** linhas nos 4 baldes; **7** mods auditados; **6** cartões
criados; **6** arquivos de relatório novos.

## 4. NAO_EXERCITADO (consolidado) — com motivo

- **Runtime**: nenhum mod e nenhuma DLL da API foram carregados pelo BepInEx no processo do jogo. Nenhuma
  rodada de jogo foi autorizada nesta tarefa.
- **Deploy no perfil r2modman**: não feito (opt-in `-p:DeployToBepInEx=true` não usado).
- **A família `UI` da API**: contrato inventariado, **não** código — C1 é implementação, C4 é consumo.
- **A proveniência do debugger (C3)**: desenho, não medição.
- **A cobertura das tabelas do BetterTooltips (C5)**: não medida; exigiria rodar o instrumento com o jogo
  aberto.
- **Paridade tabela LANG-R1 × tabelas do BetterTooltips**: não medida nesta rodada (é o C6).
- **Os 6 cartões criados**: não executados; são análise, não entrega.
- **Contagens do debugger em jogo**: auditadas por leitura de fonte
  (`DBG-R1-parte07.md` §5 admite o mesmo).

## 5. Riscos residuais que o aceite humano deve olhar

1. **C1 pode virar uma API "de terceiro" para o próprio repo.** Ao migrar o RSTV (C4), o mod passa a ter
   contrato com a API — a decisão de versionamento (C2) precisa estar tomada **antes** de C4 fechar, senão o
   repo cria a sua própria versão do problema do `biblioteca-de-terceiros` (API que não acompanha o jogo).
2. **A API é fail-closed por desenho.** Qualquer frente que passe a depender dela **para de funcionar** quando
   o jogo atualizar. É o comportamento correto para instrumento; é discutível para mod de apresentação — e é
   exatamente o motivo do `[NADA A FAZER]` do BetterFont.
3. **Duplicação benigna de ponto de patch**: hoje três coisas patcham `OptionsManager.Localize` (hook
   `ui.localized` da API, gatilho do BetterFont, tabelas do BetterTooltips). Harmony suporta; ninguém foi
   alterado. Registrado como risco conhecido, não como cartão.

## 6. Encaminhamento

Trabalho de **implementação, self-review e verificação** desta análise está concluído (artefatos escritos e
cartões criados). A revisão independente é necessária porque o produto aqui é **decisão de arquitetura**
(dois núcleos de contrato, um veredito `[MIGRAR]` bloqueado por família inexistente e seis cartões novos com
dependência no grafo) — errar isso custa caro nas próximas frente. Nenhum cartão foi fechado por esta
análise; todos os 6 nascem abertos com dono explícito.
