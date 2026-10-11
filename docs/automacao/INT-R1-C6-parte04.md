# INT-R1-C6 — parte 04: relatório curto (ganho, risco residual, NAO_EXERCITADO)

## 1. O que o operador ganha

- **Fonte única e regenerável para a parte chaveada.** Antes, o texto chaveado dos dumps de
  revisão era copiado à mão do censo; agora ele nasce da tabela do LANG-R1 por comando
  (`tools/gera_dump_chaveado.py`, ~0,3 s). Se o jogo atualizar e o LANG-R1 for refeito, o dump
  chaveado se refaz no mesmo passo — sem reescrever nada à mão.
- **Texto do jogo + pt-BR + alertas no mesmo lugar.** Cada item chaveado traz o inglês (a chave),
  o pt-BR que o dicionário devolve, e os alertas da tabela (`placeholder_presente`,
  `chave_sem_traducao`, `texto_longo`, …). É o insumo direto da revisão de texto — e o que os
  cartões LANG-C1..C5 aprovam é a **decisão do dono** sobre essa tabela, que este dump **não**
  altera.
- **A parte que a tabela não cobre está marcada, não apagada.** Os 667 itens de status continuam
  com o texto de asset cru e a marca explícita `fonte: ASSET-CRU (status; BT-6)`, apontando para o
  caminho antigo (`tools/census.py` + `docs/cobertura/*.csv`). Nada foi removido do quadro de
  revisão — o dump novo é aditivo.
- **Contagem conferível.** `--conferir` relê o arquivo gerado e reconta; `--hashes` mostra os
  sha256 de entradas e saídas. O revisor não precisa confiar em nenhum número desta prosa.

## 2. Risco residual (declarado, não escondido)

1. **Chave existe na tabela ≠ a tela que a usa é essa.** O casamento é por texto. A tabela tem
   variantes irmãs do mesmo texto (ex.: `LANG-02567` `Deals *0 weapon damage to target. ` e
   `LANG-02568` `…\n\nWhen targeting an ally, heals for *0.`) e o dumper de boot perde a ligação
   asset→variante. Quando o casamento não é literal, o `tier` do item diz o que mudou
   (`normalizado` 57, `casefold` 42) — **99 dos 650 chaveados** vieram por variante, não por igualdade
   byte a byte. Nenhum item deste corpus ficou ambíguo (0), mas
   "0 ambíguo" quer dizer "uma candidata em cada tier", não "a candidata é a certa".
2. **Os 645 status com chave coincidente.** 97% dos status têm texto igual a uma chave da tabela.
   Isso **não** contradiz o registro BT-6 (a descrição de status é lida do asset), mas mostra que a
   string também existe no dicionário. Quem decidir migrar tooltip de status precisa antes provar o
   caminho de código — este dump não prova, só registra a coincidência.
3. **Truncamento no dump de origem.** `Will of the Shaman` está com a descrição cortada no
   `DUMP-TOOLTIPS-REVISAO.md`; por isso ela caiu em "texto não está na tabela". É defeito do
   instrumento de censo, não da tabela — está no caminho antigo para ser resolvido lá.
4. **Duplicidade entre recortes.** `DEBUFFS` e `PASSIVAS` são recortes do `TOOLTIPS`: 1317 itens =
   1210 pares distintos (107 repetições). Quem contar "tooltips revisadas" pelo dump novo tem de
   descontar a repetição.

## 3. Prova de que nada foi sobrescrito (hashes antes = depois)

| Arquivo | sha256 antes | sha256 depois |
|---|---|---|
| `docs/cobertura/DUMP-TOOLTIPS-REVISAO.md` | `7ab439c7…4bbdbaaa` | `7ab439c7…4bbdbaaa` |
| `docs/cobertura/DUMP-DEBUFFS-REVISAO.md` | `5cb5b52b…65004a4` | `5cb5b52b…65004a4` |
| `docs/cobertura/DUMP-PASSIVAS-REVISAO.md` | `c9df534a…c976bcfc` | `c9df534a…c976bcfc` |
| `docs/cobertura/auditoria-tooltips.md` (não é de localização) | `476758ea…4be1ed6f3` | `476758ea…4be1ed6f3` |

Comando: `python tools/gera_dump_chaveado.py --hashes` (imprime os quatro hashes + o da tabela e o
das saídas). O script ainda tem uma trava explícita: se `--out` ou `--contagens` apontarem para um
dos quatro arquivos acima, ele **recusa** e sai com erro.

Arquivos apenas **acrescentados** nesta rodada (nenhum arquivo existente foi editado):

- `tools/gera_dump_chaveado.py`
- `docs/cobertura/DUMP-CHAVEADO-LANG-R1.md`
- `docs/cobertura/DUMP-CHAVEADO-LANG-R1-contagens.json`
- `docs/automacao/INT-R1-C6-parte01..04.md` (estes)

## 4. NAO_EXERCITADO (com o motivo — nunca estimado)

| O que | Por que não foi exercitado |
|---|---|
| renderização, quebra de linha e layout da tooltip no jogo | o cartão proíbe abrir o jogo; nada aqui passou por tela |
| resolução real da chave em runtime (`OptionsManager.Localize`) | só se mede com o jogo rodando e a API/BepInEx carregados |
| revisão linguística humana do pt-BR | decisão do dono (cartões LANG-C1..C5); este cartão não corrige texto |
| qual asset aponta para qual variante de chave | o dumper de boot não expõe essa ligação (risco residual §2.1) |
| tooltips de item/afixo/powerup/invocação | fora do escopo: os três dumps cobertos não os têm |

## 5. Recomendação de próximo passo (não executada)

Uma fatia futura pode fechar o risco §2.1: emitir, no dump de boot, o **id do asset** junto da
descrição (ou a chave já resolvida pelo jogo), o que transformaria o casamento por texto em
casamento por identidade. Enquanto isso não existir, o `tier` declarado item a item é o melhor
registro disponível — e é o que este dump entrega.
