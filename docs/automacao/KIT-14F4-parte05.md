# KIT-14F4 — parte05: pendências técnicas concretas e o que NÃO está coberto

Nenhuma destas pendências é "do dono" por definição: são interfaces/dados que faltam no
instrumento ou campanha separada já nomeada. Encaminhamento, sem classificar como humano.

## T1 — ler o alvo vivo da sessão read-only (bloqueia `RSTV-6-readonly-personagem`)

* Medido: o produto registra `RSTV-16: modo somente leitura ATIVO (… alvo=Cree)`; o consumidor
  lê `null` em `ReadOnlySession.Active/Target` por reflexão em todos os quadros do ciclo
  (`frame_observado=null`), embora os snapshots antes/depois estejam completos no MESMO objeto.
* Interface que falta: um acesso estável ao alvo da sessão. Opções concretas para a próxima rodada
  (uma delas basta): (a) expor no produto um getter/instância observável
  (`ReadOnlySession` por instância do host, não estático); (b) ler o alvo pelo próprio host
  (`SkillTreesTab`/`SkillTreesWindow`) que guarda o alvo da aba; (c) ler o `Character` do modal
  pelo `CharacterMenusManager`/`GameLogic.instance.CurrentlySelectedCharacter` **com o quadro da
  leitura registrado**, marcando a fonte — desde que a amostra declare a fonte realmente usada e
  nunca copie o valor esperado para o campo observado.
* Enquanto (a)/(b) não existirem, o critério permanece NAO_EXERCITADO: não se declara alvo
  conferido lendo o próprio alvo esperado.

## T2 — `RSTV-geometria-clipping` REPROVADO sob hover não-físico

* Medido: `Title` x=−333,3 e `Description` x=−419,7 (tela 1920×1080) no instante do hover por
  handler, com `physical_input=false`.
* Causa: a posição da tooltip vem do ponteiro; sem ponteiro físico a caixa ancora fora da tela.
  O dado foi mantido (não filtrado, não removido) e o aceite de UIUX/clique físico é campanha
  separada (KIT-G4).
* Encaminhamento: rodada com ponteiro real (ou `PointerEventData` posicionado no nó) antes de
  julgar geometria de tooltip; alternativamente, o detector pode receber a marca
  `ponteiro_fisico: false` como escopo declarado do dado — decisão do revisor humano, não desta
  implementação.

## T3 — `RSTV-25b-dependencia` não emitida

* O consumidor não emite `linhas_dependencia`/`dependency_por_tier`; o produto sim
  (`RSTV-25: nos com Dependency por tier — T1:0/6, T2:1/6, T3:0/7, T4:1/6, T5:0/5` no log).
* Encaminhamento: nova capacidade de coleta (contagem por tier e linhas vivas) com expectativa
  mecânica declarada — explicitamente fora do escopo desta correção ("sem fabricar
  Dependency/expectativa mecânica").

## T4 — campanha KIT14 que continua aberta

Runner, marcação/export in-game, mod sem kit funcional, performance comparável e
update/rollback continuam campanha do KIT14; esta correção não fecha o KIT14.

## Ressalva de identidade agregada (herdada, não reescrita)

`cases/*/recorder-on/inputs.json` preserva `source_set_sha256` agregado herdado do F2
(`cc43e91968a584e4b91ca2c6ec95718adaad54bb6525da53de256189e4831f0c`), enquanto o conjunto atual
com as fontes F3 recalcula (mesmo algoritmo `json.dumps(..., sort_keys=True)`) o valor
`d3c7995b52cf4da33d9c830e3cc1025724afaf23bbaae09ceaee110ae250140d`. Os hashes **individuais**
(fonte/DLL/carregados) foram conferidos e é a identidade individual que o detector usa. A prova
congelada **não** foi reescrita: a ressalva fica declarada aqui e nas guardas de identidade
agregada futuras (que devem rejeitar agregado incoerente).

## Ambientes / isolamento (por boot)

Campanha `recorder-on` com isolamento KIT16: frente única adquirida e liberada, Cloud preservado
(`app_cloudenabled: ["0"]`), snapshots imediatos de produção/perfil/outro-jogo por conjuntos,
bytes e SHA antes/depois com diff `equal: true`, PlayerPrefs restaurados, PID próprio encerrado
com `CloseMainWindow()`, sem junction/backup/perfil isolado/lock ao fim. Nenhuma sessão do dono
existia antes de cada boot (checagem do preflight recusaria).
