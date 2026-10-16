# KIT-14 — residual mínimo após run1471

## O que NÃO repetir

Não pedir nova autorização genérica de teste: política13/10 já libera automação com jogo fechado. Não pedir limiares de performance: decisão B mantém coleta exploratória. Não refazer auditoria offline R2/run1014, boot de dependência ausente/run1442 nem os três boots de carregamento desta retomada.

## Pré-requisito técnico antes de pedir clique humano

O driver atual invoca Unity Button.onClick por rótulo. Play;Roguelike;Accept cria personagem descartável e chega Select Party, mas NÃO adiciona personagem à party e não entra na run. Select Party não tem mais botão Skills (Plugin.cs:22..25). Com RealmApi instalada, os15 ganchos carregam, mas RstvRunSkillTreeButton pertence ao HUD da run.

Trabalho necessário para frente de automação independente:
1. Identificar no assembly atual o handler REAL do seletor de personagem (não fingir que é Button) e a ação de aceitar a party. Reusar driver existente; não alterar gameplay/mod para satisfazer auditoria.
2. Estender o instrumento com seleção de personagem DESCARTÁVEL e rota até o HUD, espera de estado real, fechamento/restauração garantidos e negativas fail-closed. Build apenas em sandbox depois do preflight de deploy; preservar fonte principal e ponte.
3. Executar RSTV janela/conteúdo/tooltip/PNG/relatório, mark/export e Runner positivo/negativo no cenário real. Confirmar recorder passivo alimentado. Zero passivo não significa sucesso.
4. Repetir com recorder ON/OFF na MESMA base real, duração e configuração. Esta rodada mediu somente Select Party ociosa; não substitui recorder trabalhando.
5. Provar comportamento funcional RSTV sem kit (boot15/15 já comprovado). Identificar hash do assembly RSTV efetivamente carregado, não somente DLL copiada. Testar update/remove/rollback de versão/pacote, não só remover perfil temporário.

A máquina possui somente perfil default (hermes profile list,14/10); não inventar assignee especialista nem mudar política/modelos. O operador precisa encaminhar a frente técnica a uma autoria separada ou registrar que nova instância default assume esse escopo. O worker desta coleta não muda produto/probe principal nem auto-revisa a extensão.

## Só depois: mão/olho do dono

A bancada deve estar preparada em dados descartáveis, com Cloud OFF e hashes prévios; NÃO usar o perfil Default nem saves pessoais. O agente identifica build/sessão e a superfície em que o botão Skills realmente aparece.

Ação humana mínima: clicar fisicamente Skills no HUD/modal correspondente; passar mouse numa skill; confirmar que janela/texto/tooltip ficam legíveis, sem recorte, sobreposição ou pontos gastos. Reportar qual caso foi visto e o que divergiu. Handler CliqueFisico=true NÃO prova essa ação. Agente coleta estado/quadro/PNG/log, fecha apenas sua instância e restaura o ambiente.

Revisão independente KIT14R e aceite final permanecem separados. Cloud estava OFF no início das rodadas e foi mantida OFF; houve escrita do remotecache pelo Steam mesmo com toggle0. Religamento da campanha é residual operacional do dono, não alegado como executado nem forçado por edição de VDF/clique de OS headless.

Sem segunda instalação/máquina, portabilidade permanece não comprovada. O perfil temporário desta máquina não é um segundo ambiente independente.
