# KIT-14 — run699: descoberta dirigida antes de runtime

Complemento incremental. Não modifica artefatos anteriores.

## Evidência lida

- AUT-4-runbook-rodada-autorizada.md §§0–5: exige identidade da build, Sessao/HashFonte, preflight de deploy, rollback e prova viva; distingue handler de clique físico.
- KIT-G2-parte03.md: método comparável com/sem recorder, substituído apenas quanto a limiares pela decisão B do cartão.
- Cartão KIT-14R t_9ce7d260 relido: todo, depende de KIT-14, já fornece revisão independente. Não foi criado outro cartão nem liberado este filho.
- Scripts existentes lidos integralmente: scratch/kit/build-preflight.sh, runtime-isolado.sh e front-unica.sh.

## Limites que precisam ser resolvidos antes de usar os scripts

runtime-isolado.sh isola BepInEx/LogOutput e mede saves pessoais por hash; o próprio cabeçalho declara que nenhum save é carregado. O lançamento run utiliza Steam/instalação normal e não fornece, neste script, redirecionamento de persistentDataPath nem instância de save descartável. Logo, não executar run/navegação presumindo que copiar BepInEx isola os saves. Um snapshot detectaria dano depois, não impediria acesso ao save pessoal.

build-preflight.sh executa um build isolado e compara metadados do perfil depois; isso não é por si só a checagem de opt-in obrigatória antes do build. Ainda preciso localizar/reusar essa checagem e o caminho autorizado de isolamento do save/instância. Nenhum build iniciado.

front-unica.sh oferece check somente leitura; não adquirir ou forçar lock de outra frente. Nenhum lock adquirido neste bloco.

## Estado

Runtime, UI, métricas e instalação: NAO_EXERCITADO. Nenhuma fixture contada como jogo. Este checkpoint registra uma lacuna técnica observada no script existente, ainda em investigação dirigida; não reabre autorização humana nem a dispensa de limiares.
