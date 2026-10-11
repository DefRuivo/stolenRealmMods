# KIT-06 — parte 03: ponte C# de atalhos + harness offline (44/44 + controles negativos)

Cartão `t_66ff87b5` · run 633 · 2026-10-09 · offline.

## 1. Produzido neste bloco

| Arquivo | O quê |
|---|---|
| `tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs` | Núcleo C# do plano de controle (espelha `controle_acesso.py`), **sem dependência de Unity/BepInEx** |
| `tools/automacao/runtime/harness-controle/Program.cs` | Harness offline: 44 verificações |
| `tools/automacao/runtime/harness-controle/HarnessControle.csproj` | Compila por LINK `PonteControleRSTV.cs` + `PipelinePassivo.cs` + `Json.cs` |

A ponte reusa o **pipeline KIT-05F** (`PipelinePassivo`) em vez de criar outro:
pausar/retomar pelo atalho agem no MESMO pipeline da trilha passiva.

## 2. Execuções reais (exit e log)

```
$ dotnet run --project tools/automacao/runtime/harness-controle
 verificacoes: 44 OK, 0 FALHA
 VEREDITO HARNESS: VERDE (exit 0)                                  EXIT=0
 log: scratch/kit/KIT-06/harness-verde.log

$ dotnet run --project .../harness-controle -- --defeito guard
[FALHA ] guard chat: atalho NAO dispara -> acao=observar
[FALHA ] guard chat: observacao NAO iniciou
[FALHA ] guard chat: degradacao registrada -> guard_chat=0
 verificacoes: 41 OK, 3 FALHA
 VEREDITO HARNESS: VERDE do controle negativo (defeito detectado)  EXIT=0
 log: scratch/kit/KIT-06/harness-defeito-guard.log

$ dotnet run --project .../harness-controle -- --defeito ataque
[FALHA ] config: tecla reservada recusada
[FALHA ] config: nenhum atalho invalido sobrevive -> validos=1
 verificacoes: 42 OK, 2 FALHA
 VEREDITO HARNESS: VERDE do controle negativo (defeito detectado)  EXIT=0
 log: scratch/kit/KIT-06/harness-defeito-ataque.log
```

Os dois controles negativos simulam um **chamador defeituoso** (não reporta o
chat aberto; esquece de declarar as teclas de chat) e o harness os **REPROVA**.
Um `--defeito` cujo defeito NÃO seja detectado devolve `FALSO VERDE` e exit 1
(previsto no código e testado nesta rodada: foi o que aconteceu antes de eu
ajustar o defeito `ataque` para ser realmente discriminante — registro honesto).

## 3. O que o harness NÃO prova

- Não abre o jogo: **runtime, pixels, foco real e leitura real do teclado
  (engine) seguem NAO_EXERCITADO**.
- Não compila a ponte dentro do adapter Unity (a compilação do adapter inteiro é
  feita no build isolado, bloco seguinte).
- A UI/overlay real é **KIT-G2**; aqui só se prova o dado do indicador.

## 4. Progresso

- [x] parte01 · [x] parte02
- [x] parte03 (ponte C# + harness 44/44 + 2 controles negativos)
