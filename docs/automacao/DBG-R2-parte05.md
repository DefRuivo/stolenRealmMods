# DBG-R2 — Parte 05: rodada de correção do parecer (prova documental)

Cartão `t_3b7c681b` (INT-R1-C3). Esta parte registra **apenas** o que a revisão independente rodada 1
pediu: 4 correções de **prova documental** em `DBG-R2-parte01.md` / `DBG-R2-parte02.md`. Nenhum
arquivo de código, teste, fixture, verificador ou documento de `docs/DBG-PROVENIENCIA.md` foi
alterado para "fazer o teste passar" — as edições são de citação/comando.

O parecer aprovou tecnicamente o instrumento e pediu mudanças só porque **comandos citados como
prova não reproduziam** no estado atual da árvore.

## 1. O que foi corrigido (item a item do parecer)

| # | onde | antes (não reproduzia) | depois (medido nesta rodada) |
|---|---|---|---|
| 1 | `DBG-R2-parte01.md` §1.1 | `grep -rn "File\.\|Path\.\|StreamWriter\|WriteAll" …` com resultado "(0 ocorrências)" | dois comandos separados: **0 escritas** e **9 leituras** (números reais abaixo) |
| 2 | `DBG-R2-parte01.md` §5 e `DBG-R2-parte02.md` §4 | `grep -rn "RealmApi" RoguelikeDebugger/ # 0` | provas (a) `.csproj` sem referência → 0 / rc=1 e (b) `using Gumatos` → 0 / rc=1, + inventário das 3 linhas de contato real (string, não compilação) |
| 3 | `DBG-R2-parte01.md` §2 | esboço do bloco sem `inicioEm=` e sem `matrizFlame=`/`modoLeitura=` | esboço = formato implementado (campos exigidos por `OBRIGATORIOS_INICIO`/`OBRIGATORIOS_ESTADO`) |
| 4 | `DBG-R2-parte01.md` (topo, §1, §4) e, pela mesma classe de defeito, `DBG-R2-parte04.md` §7 e `docs/DBG-PROVENIENCIA.md` "Por que existe" | citações `DBG-R1-parte05-matriz.csv` / `DBG-R1-parte07.md` como se fossem caminhos do repo | qualificadas: **não existem na árvore**; estão no ZIP da entrega de `t_9e2325d7` (caminho absoluto escrito no texto) |

O item 4 do parecer citava a parte01 e o metadata `p0_scope.matriz` do handoff. O metadata é do
handoff (não é arquivo editável); a citação errada foi corrigida **nos documentos**, incluindo
`DBG-R2-parte04.md` e `DBG-PROVENIENCIA.md`, que tinham o mesmo defeito — registrado aqui para não
parecer mudança silenciosa fora do pedido.

## 2. Medições que agora constam nos documentos (reproduzíveis)

    cd /c/dev/stolen-realm
    # item 1a — escritas de runtime no debugger: 0
    grep -rn "StreamWriter\|File\.WriteAll\|File\.AppendAll\|File\.Create\|File\.OpenWrite" \
        --include=*.cs RoguelikeDebugger/ | grep -v /obj/ ; echo "rc=$?"
    rc=1
    # item 1b — varredura ampla: 9 (todas leitura: OpenRead 1, Exists 2, ReadAllLines 2, Path.* 4)
    grep -rn "File\.\|Path\.\|StreamWriter\|WriteAll" --include=*.cs RoguelikeDebugger/ \
        | grep -v /obj/ | wc -l
    9
    # item 2a/2b — sem referência de projeto e sem using da API
    grep -n "RealmApi\|Gumatos" RoguelikeDebugger/RoguelikeDebugger.csproj ; echo "rc=$?"   # rc=1
    grep -rn "using Gumatos" RoguelikeDebugger/ ; echo "rc=$?"                              # rc=1
    # item 4 — DBG-R1 não existe na árvore (0 linhas)
    find . -path ./scratch -prune -o -path ./.worktrees -prune -o -name "*DBG-R1*" -print

As 9 linhas de leitura estão em `RoguelikeDebugger/Proveniencia.cs`: 233, 260, 261, 262, 267, 319,
493, 494, 499.

## 3. Fontes do mod: sha256 inalterado depois desta rodada

Medido depois de todas as edições de documento (nenhuma linha de C# tocada):

```
e1536451657876a0ae20eefc94185f558b33fa1bcc58f50fb60975e054e4debd  RoguelikeDebugger/Proveniencia.cs
122cd813cb9a456bf2594b53608fdea3cdd4299fb0383ee74315e0fe044d06b1  RoguelikeDebugger/Plugin.cs
69ffbf2ccaae4471e0ba882b494a6e512e8c2fec9a3aa0bc226b83e2e45a450b  RoguelikeDebugger/EfeitosInfo.cs
d2df3d9a130b3a80f14ec35f1104c119f78fccf0c247cbccaa5ed36b6c648541  RoguelikeDebugger/RoguelikeDebugger.csproj
```

Os 10 `Patches/*.cs` também batem, na ordem, com a lista de `DBG-R2-parte02.md` §1.1 / com
`regras_proveniencia.INTOCADOS` (é o próprio teste que confere).

## 4. Teste puro: VERDE depois das correções

    python tools/testes/roda_testes.py --teste tools/testes/testes/puros/t_dbg_r2_proveniencia.py

    [PASSOU ] dbg-r2-proveniencia DBG-R2: o carimbo DBG-PROV-V1 (...)
    rodaram: 1 | passaram: 1 | reprovaram: 0 | nao rodaram: 0
    VEREDITO: VERDE (exit 0)

    rc=0

O teste confere o sha256 das fontes que não podiam mudar: como as edições desta rodada foram só em
`.md`, ele continua verde sem qualquer afrouxamento.

## 5. O que esta rodada NÃO fez

- Não refez código, teste, fixture, verificador nem schema.
- Não abriu o jogo, não instalou, não publicou, não buildou de novo (o build isolado da parte 02
  segue válido: nenhum `.cs` mudou).
- Não alterou nenhum sha256 medido antes.
- Não tocou nos cartões vivos do KIT/LEVEL nem nas duas reprovações alheias da suíte
  (`deploy-optin-repo` em `scratch/kit/KIT-14-*`, `referencias-lib` em `.worktrees/level-r2`).
- Runtime segue **NAO_EXERCITADO**.
