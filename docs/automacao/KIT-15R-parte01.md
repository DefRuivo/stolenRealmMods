# KIT-15R — parte 01: abertura e critérios independentes

Cartão t_effde07f; reviewer default/run678 (nova instância, não autor); implementer default/run677, t_10584ca5. Data local medida por terminal: 2026-10-10T02:20:50-03:00. Workspace C:/dev/stolen-realm; branch medida ci-validate-test. Revisão estritamente OFFLINE; nenhum produto será corrigido por este revisor, nenhum jogo/perfil/deploy/publicação autorizado.

kanban_show confirma pai concluído e dependências satisfeitas. Lidos docs/SUPERVISAO.md, docs/PROCESSO-REVISAO.md, cartão KIT-15 e docs/automacao/KIT-15-entrega.md. git status --short: alterações manuais e fontes untracked presentes; preservá-los, copiar arquivos vivos para sandbox própria. Inventário e hashes ainda não medidos. Relatório do autor é hipótese a refutar, não evidência independente.

## C1 Instalar, atualizar, remover e rollback
NAO_EXERCITADO. Verificar efeitos no disco e backups, não mensagens de sucesso; testar falhas e estado modificado pelo usuário.

## C2 Dependências reais e versões
INDETERMINADO. Conferir fontes e conteúdo do ZIP, imports executáveis após extração em ambiente limpo.

## C3 Descoberta/seleção sem usuário fixo e uso básico sem SDK/Python
INDETERMINADO. Autor entrega fonte, declara build C# não exercitado e modo manual sem rollback. Confrontar com aceite sem SDK/Python e pacote instalável.

## C4 READMEs PT-BR/EN, primeiro uso, exemplos, changelog e compatibilidade medida
INDETERMINADO. Conferir documentação entregue e limitações reais; nenhuma alegação de runtime a partir de fixture.

## C5 ZIP candidato limpo, identidade fonte/artefato
NAO_EXERCITADO. Medir ZIP do autor, gerar próprio em sandbox, CRC e hashes por membro.

## C6 Scan de segredos/conteúdo e DLL proprietária
NAO_EXERCITADO. Exercitar nominal e controles sintéticos; sem ler credenciais reais.

## C7 Não publicação/instalação do dono, preservação e independência
PASSOU na abertura: não executado comando de instalação/publicação nem alteração de produto. Confirmação final pendente. Runtime/UI-UX/gates humanos/build sem preflight permanecem NAO_EXERCITADO.

## C8 Prova discriminante e encaminhamento
NAO_EXERCITADO. Rodar suíte autor e controles, mais oráculos próprios com falha demonstrada; achados voltam ao implementador em cartão de correção independente, sem apagar histórico.

Artefato incremental novo conforme regra vigente do cartão; fechamento único em KIT-15R-revisao.md quando o parecer estiver concluído.
