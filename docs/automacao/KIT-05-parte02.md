# KIT-05 — parte 02: inventário da infra viva e plano de implementação

Cartão `t_e9e569f8` · 2026-10-09 · offline.

## 1. O que já existe (reusar, não duplicar)

| Peça | Caminho | Papel hoje |
|---|---|---|
| Core (C#) | `tools/automacao/runtime/KIT04Core/` | sessão/identidade/eventos/captura PNG; evento = lista ILIMITADA e simples (`EventosImpl`) |
| Adapter SR (C#) | `tools/automacao/runtime/KIT04Adapter.SR/` | telas/personagens/owners SR; inerte com `habilitado=false` |
| Probe (C#) | `tools/automacao/runtime/AUT4Probe/` | instrumento de origem, intacto |
| Coletor (py) | `tools/automacao/runtime/coletor.py` | driver opt-in; normaliza leitura crua, injeta sessão/hash, consolida por campo |
| Avaliador RSTV (py) | `tools/automacao/cenarios/rstv.py` | 7 capacidades RSTV; funil de honestidade (AUSENTE≠OK, fixture≠runtime) |
| Avaliador AUT-5 (py) | `tools/automacao/aut5/aut5.py` | costura/observações |
| Schemas | `docs/automacao/schemas/evento-v1.json` etc. | já definem `tipo` de evento (`state_change`, `ui_update`, `data_read`, `action_triggered`, `error`) |

## 2. Lacuna que o KIT-05 preenche

O `ICoreEvento`/`EventosImpl` de hoje só **acumula** eventos numa lista sem teto. Faltam, e
são o escopo do KIT-05:

1. primeiro conjunto de eventos RSTV (clique recebido, janela aberta/fechada, tooltip,
   **falha clique-sem-janela com motivo/timeout**);
2. modo **passivo** com trava (sem clique/save/equipamento/modificação);
3. **deduplicação por mudança** (estado repetido não vira evento);
4. **fila limitada** (teto de eventos) com descarte declarado;
5. **retenção** (idade/tamanho) e **teto de capturas** (PNG);
6. **pausa segura** e **degradação explícita** (nunca silenciosa);
7. correlação **id de evento + dados + quadro** da captura APÓS a atualização visual,
   sem afirmar simultaneidade;
8. **sem captura contínua indiscriminada**.

## 3. Onde implemento (offline e verificável)

A lógica do pipeline (dedup/fila/retenção/teto/pausa/degradação/correlação) é **lógica pura**
e não precisa do Unity → implemento em Python, com testes offline **reais** (execução com
exit code), em:

- `tools/automacao/runtime/observacao_passiva.py` — módulo do pipeline de observação passiva;
- `tools/automacao/runtime/testes/test_observacao_passiva.py` — suite de testes reais.

O lado runtime (C#) do Core fica **declarado como mapeamento** nesta entrega, com o contrato
explícito; a emissão em jogo é **NÃO_EXERCITADA** (exige rodada autorizada do dono, fora do
escopo deste cartão). Não invento saída de jogo.

## 4. Regra de honestidade (herdada)
AUSENTE/repetido/malformado nunca vira "observado"; degradação sempre declarada com motivo.
Fixture/teste offline prova o pipeline, não o runtime.

## Progresso
- [x] Inventário da infra viva (seções 1–2).
- Próximo bloco: implementar `observacao_passiva.py`.
