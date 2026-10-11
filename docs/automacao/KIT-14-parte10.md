# KIT-14 — run699: fechamento parcial antes do bloqueio runtime

## Provas finais já obtidas

- Definições compiladas FileSystem e GlobalSaveDataManager conservadas em compiled-*.txt, com stderr/exit em compiled-results.json; ambas decompilações exit0, DLL somente leitura.
- Quatro travas do repo vivo: check_segredos/check_padroes_segredo/check_dupes/audita_docs exit0 cada. Saídas brutas em logs/gate-*; escopo versionado declarado, não aprovação universal de todos os untracked.
- Reconferência final terminal (13:17:26 -03): front-unica.sh check OK/exit0; STOLEN_PROCESS_COUNT=0; HEAD d82894ebe95d97f26b7989a848372c691dcb8ef6; índice vazio.
- As etapas offline concluídas são as de parte09 e offline-result-resume.json; erros iniciais preservados como histórico.

## Impedimento técnico específico para o restante

A infraestrutura entregue não demonstra que o jogo consumirá um persistentDataPath/save de TESTE antes do acesso ao estado pessoal. Runtime-isolado copia apenas o BepInEx; isolacao.sh copia saves/cria marcador sem encanamento ao processo; coletor lança a instalação normal via Steam com argumento de doorstop. FileSystem e GlobalSaveDataManager compilados confirmam que o caminho de save vem de Application.persistentDataPath nesse caminho observado.

Não contornar com troca dos saves pessoais, patch do assembly do jogo, alteração de gameplay ou presunção de que USERPROFILE/APPDATA mudam o save consumido pelo Unity/Steam. Esses envs foram redirecionados apenas para os subprocessos OFFLINE de build/ferramentas, não como prova de isolamento runtime.

Próximo passo concreto: disponibilizar uma instância/conta/ambiente de teste cujo caminho persistente esteja comprovadamente separado, OU entregar isolamento preventivo do save em uma frente especializada com revisão independente e controles negativos antes do boot. Não requer nova autorização genérica ou novos limiares: KIT-G2 B1–B6 e opção B já existem. Apenas default está disponível na lista real de perfis; não atribuir seguimento ao próprio worker nem inventar especialista.

## Cobertura residual

Todos os cenários ativos RSTV e C1–C7 AUT-4: NAO_EXERCITADO em jogo. C0/controles de lógica somente offline não viram controle em jogo. Clique físico/PNG/relatório interativo e exportação; mod sem kit; comparação funcional com/sem recorder; FPS/média/p95/memória/disco do recorder: NAO_EXERCITADO. Segundo ambiente runtime limpo: não qualificado, sem alegar portabilidade. Revisão visual, aceite humano e publicação: separados e pendentes.

Preparação do relatório consolidado e inventário SHA de evidências em arquivos novos; não liberar KIT-14R enquanto os aceites nomeados continuarem não cobertos.
