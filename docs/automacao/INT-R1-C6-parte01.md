# INT-R1-C6 — parte 01: insumos, artefatos e como regenerar

Cartão: `t_ee99ccc4` (INT-R1-C6, filho de `t_2a6474ff` LANG-R1). Modelo desta rodada:
`deepseek-flash`/`deepseek`. Escopo: **gerar** o dump chaveado a partir da tabela do LANG-R1 e
contar. Nada de corrigir texto, nada de abrir o jogo, nada de publicar.

## 1. O que foi entregue (novo — nada sobrescrito)

| Artefato | Caminho | Tamanho / sha256 |
|---|---|---|
| script reprodutível | `tools/gera_dump_chaveado.py` | 28.975 B de código; `python tools/gera_dump_chaveado.py` roda em ~0,3 s |
| dump NOVO (chaveado + marcação de asset cru + listas) | `docs/cobertura/DUMP-CHAVEADO-LANG-R1.md` | 526.679 B / `408ad3ad13681096b2c3279ff0f2a97193b92754f2ad35448e7907842f891694` |
| contagens em máquina | `docs/cobertura/DUMP-CHAVEADO-LANG-R1-contagens.json` | toda a contagem abaixo, com a lista dos casos de borda |

Os três dumps de origem **não** foram tocados (prova na parte 04 §3) e
`docs/cobertura/auditoria-tooltips.md` também não (é auditoria de conteúdo/mecânica — a
suspeita do operador já havia sido refutada na análise INT-R1 e continua valendo).

## 2. Insumos, com hash (para o revisor conferir que leu o mesmo arquivo)

| Insumo | Caminho | sha256 |
|---|---|---|
| tabela de localização do LANG-R1 (anexo do cartão `t_2a6474ff`) | `C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_2a6474ff\localizacao-ptbr.csv` | `951d244d0fbaad5a0388dc27ba3c99fced9fc4a5ff70a17fa0e47bf8094b30c1` |
| dump de origem (skills + status + shrines) | `docs/cobertura/DUMP-TOOLTIPS-REVISAO.md` | `7ab439c7c68c3c4118e09117535e3aa7d53e195aa1871180ec50ae0f4bbdbaaa` |
| dump de origem (recorte debuffs) | `docs/cobertura/DUMP-DEBUFFS-REVISAO.md` | `5cb5b52b5d880573fc397c2ea67c367bf8e845f46f59931f7bf9bd1de65004a4` |
| dump de origem (recorte passivas) | `docs/cobertura/DUMP-PASSIVAS-REVISAO.md` | `c9df534af8cbc37941dac5c17c976aa49ce544990c9a7d136854af77c976bcfc` |
| auditoria que **não** foi tocada | `docs/cobertura/auditoria-tooltips.md` | `476758eab785d2547cd2d817b564a2f99b3db4a9fcbb7189026e6ff4be1ed6f3` |

A tabela do LANG-R1 **não está no repo** (veio como anexo). O script procura, nesta ordem:
`--csv <caminho>` → o caminho do anexo acima → `scratch/lang-r1/localizacao-ptbr.csv`. Se não
achar, ele para com mensagem — não inventa dado.

## 3. Como rodar (o operador, do zero, sem abrir o jogo)

```bash
# 1) gerar o dump novo (nao sobrescreve nada: os nomes de saida sao novos)
python tools/gera_dump_chaveado.py

# 2) conferir a contagem lendo o PROPRIO dump gerado (nao o JSON)
python tools/gera_dump_chaveado.py --conferir     # espera "RESULTADO: OK" e exit 0

# 3) provar que os insumos e as saidas sao os mesmos que foram medidos
python tools/gera_dump_chaveado.py --hashes
```

Saída medida do passo 2 nesta rodada:

```
linhas '- fonte: TABELA-LANG-R1' :    650   esperado chaveado        650
linhas '- fonte: ASSET-CRU'       :    667   esperado asset cru       667
linhas '- fonte: NAO-ENCONTRADO'  :      0   esperado nao encont.       0
itens com linha de fonte          :   1317   esperado itens          1317
RESULTADO: OK
```

O `--conferir` é a trava: ele **não** acredita no JSON, relê o markdown gerado, conta as linhas
`- fonte:` e compara. Se o dump e o JSON divergirem, sai 1.

Reprodutibilidade byte a byte: com a data fixa (`INT_R1_C6_DATA="2026-10-11 06:25"`) e a mesma
tabela de entrada, duas gerações em arquivos distintos deram o **mesmo** sha256 no dump
(`408ad3ad13681096b2c3279ff0f2a97193b92754f2ad35448e7907842f891694`) e `cmp` não acusou
diferença; o JSON de contagens difere só no campo `saida.caminho` (o caminho que foi pedido na
chamada). Sem a variável de data, só a linha "Gerado em" muda — o script é determinístico.

## 4. Ordem de leitura do dump novo (padrão de `docs/TEXTO-TOOLTIPS.md`)

O documento `docs/TEXTO-TOOLTIPS.md` §1 fixa os três níveis na ordem do dono: **nível 1 =
descrição do jogo** (branco) → **nível 2 = nota de mecânica** (tom escuro) → **nível 3 = estado do
personagem** (azul). O dump novo respeita essa ordem e deixa explícito o que vem de onde:

1. `desc jogo (en, como esta no dump)` — nível 1, o texto do jogo (é a chave de localização);
2. `chave casada na tabela` — a chave do LANG-R1 que casa com essa descrição;
3. `pt-BR (tabela LANG-R1)` — o que o dicionário pt-BR devolve para a chave;
4. `alertas LANG-R1` + `contextos` — placeholder, tags, contexto de tela da tabela;
5. os campos de mecânica que o dump de origem já trazia (`dano`, `tags`, `attr`, `efeitos`) —
   insumo das notas de nível 2/3, **não** vem da tabela de localização;
6. `fonte` — de onde o texto veio (tabela, asset cru ou não encontrado).

Ou seja: o dump novo **não** reescreve texto nenhum (limite do cartão) e **não** decide nota de
nível 2 — ele junta, por chave, o texto do jogo + o pt-BR + os alertas, e marca a procedência.

## 5. NAO_EXERCITADO desta parte

- Renderização/quebra de linha/layout de tooltip em jogo: **não exercitado** (jogo não foi aberto
  nesta rodada — limite do cartão).
- Leitura por API/BepInEx em runtime: **não exercitado** (offline por desenho).
- Revisão linguística humana do pt-BR: **não exercitada** (decisão é do dono nos cartões LANG-C1..C5).
