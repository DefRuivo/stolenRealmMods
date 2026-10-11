# KIT-12R — parte 01: abertura da revisão independente

Revisor: instância default/run674, task t_811b1717. Autor atual informado pelo handoff: default/run671; revisão anterior run672 não substitui esta execução. Data local medida: 2026-10-10T01:25:47-03:00.

Escopo: exclusivamente ferramentas OFFLINE KIT-12, sem alterar produto, instalar, publicar, executar jogo ou modificar política. Artefatos incrementais novos; parecer final será KIT-12R-revisao.md. Ainda NÃO há aprovação nesta parte.

## Inventário e identidade viva
NAO_EXERCITADO: hashes e cópia sandbox ainda pendentes. Orientação real: `cd "$HERMES_KANBAN_WORKSPACE" && pwd && git status --short && git branch --show-current ...`, exit 0, diretório C:/dev/stolen-realm, branch ci-validate-test. Terminal não expõe HERMES_KANBAN_TASK/RUN_ID; todas as operações de board usarão task_id explícito. Alterações tracked/untracked existentes preservadas. Nenhum KIT-12R* existia antes desta escrita.

## C1 — hash/versão/config/sessão em toda a cadeia e invalidação
NAO_EXERCITADO. Conferir implementação viva, caminho positivo e alteração controlada que invalida aprovação.

## C2 — lacuna técnica ao agente e humano apenas residual
NAO_EXERCITADO. Testar rotas positivas e entradas malformadas/contraditórias, sem atribuir trabalho automático ao dono.

## C3 — fila declarativa, limites/tentativas/sem progresso e comandos seguros
NAO_EXERCITADO. Conferir campos e executar sondas próprias em sandbox.

## C4 — determinismo sem IA e dependência Hermes opcional
NAO_EXERCITADO. Medir resultados repetidos e inspecionar chamadas externas.

## C5 — CLI integrada, fixture explícita, erro/correção/revalidação
NAO_EXERCITADO. Não usar fixture como prova runtime. Executar cadeia em cópia isolada sem credenciais/perfil remoto.

## C6 — contra-provas, travas, preservação e autoria
NAO_EXERCITADO. Rodar suites e mutações próprias; comparar hashes antes/depois. docs/SUPERVISAO.md (linhas 1–220) e docs/PROCESSO-REVISAO.md (inteiro) lidos; regras atuais do cartão prevalecem sobre paralelismo/horários legados.

## Lacunas deliberadas
Runtime AUT-4, jogo, perfil/save do dono, build C#, preflight de deploy, UI/UX, publicação e gates humanos não são autorizados/exercitados. Aprovação técnica offline não equivale ao DoD de mod.

## Próximo bloco
Ler entrega e código dirigidos, extrair critérios do pai sem repetir retorno volumoso, criar sandbox e registrar identidade dos bytes. Parecer pendente.
