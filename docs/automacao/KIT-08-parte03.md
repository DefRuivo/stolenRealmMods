# KIT-08 — parte03: implementação do visualizador + suíte verde

## Entregues até aqui (arquivos NOVOS)

| arquivo | papel |
|---|---|
| `tools/automacao/kit08/visualizador.py` | gerador HTML local + comparação + stale + reuso KIT-09 |
| `tools/automacao/kit08/teste_visualizador_kit08.py` | 20 testes offline (unittest) |

## Prova de execução real

```
python tools/automacao/kit08/teste_visualizador_kit08.py   -> exit 0
Ran 20 tests in 0.006s
OK
```
Log: `scratch/kit/k08/suite.log`.

Reuso REAL do avaliador KIT-09 (sem duplicar):
```
python tools/automacao/kit08/visualizador.py \
  --entrada tools/automacao/cenarios/kit09-verdade.entrada.json \
  --identidade tools/automacao/cenarios/kit09-identidade.json \
  --saida scratch/kit/k08/smoke-verdade.html
KIT-08: relatorio=scratch/kit/k08/smoke-verdade.html bytes=44544 sha256=7fc310... contagem={"NAO_EXERCITADO": 21} stale=False   (exit 2 = nada exercitado)
```
A fixture SINTÉTICA do KIT-09 produz **21 NAO_EXERCITADO** (nenhum PASSOU) — a
guarda de origem do KIT-09 retira a qualificação de runtime. Prova viva de que
**fixture nunca vira PASSOU** também no visualizador.

## Nota de correção durante a implementação

O primeiro `referencia_local_segura` ecoava o valor recusado no motivo, o que
introduzia `http://evil.example/...` como TEXTO dentro do HTML (inofensivo, mas
fura a invariante "nenhuma referência remota no arquivo"). Corrigido: o motivo
**nunca** reproduz o valor recusado (referência pode ser controlada por dado
recebido). Este é um achado registrado, não escondido.

## Próximos passos

4. `contra_prova_kit08.py` (defeito plantado → conjunto exato de testes falha).
5. `roda_testes_kit08.sh` (suíte + contra-prova, exit 0/1/2).
6. Exemplo REAL + sha256 do HTML; fixtures rotuladas baseline/candidata.
7. Fechar `KIT-08-entrega.md` e pedir revisão independente.

**Checkpoint parte03:** implementação + suíte 20 OK prontas; próximo = contra-prova.
