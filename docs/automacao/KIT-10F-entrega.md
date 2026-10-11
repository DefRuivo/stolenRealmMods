# KIT-10F — entrega (t_48b78ecb)

Correcao dos falsos OK e da lacuna de cobertura apontados pela revisao adicional KIT-10R
(`t_896796be`, run663 != run659). Implementador: perfil `default`, run665 (instancia nova).

Estado: **implementacao + auto-verificacao concluidas; encaminhado para revisao independente**
(`kanban_request_review`). NAO e `kanban_complete`: um revisor independente tem de tentar refutar
antes. Nenhum gate humano/DoD satisfeito; nada foi publicado nem instalado.

## Escopo entregue

- Produto: `tools/automacao/kit10/kit10_cenarios.py` — SHA256
  `899e47595d2e86ed2dda1e5bc6c425c3a0f9a70db3974f899480fde64620507c` (antes
  `8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092`).
- Documentos: `docs/automacao/KIT-10F-parte01.md` (escopo/contrato de medicao),
  `docs/automacao/KIT-10F-parte02.md` (correcoes + provas), este arquivo.
- Evidencia/scripts: `scratch/kit/KIT-10F-run665/` (`prova_red_kit10f.py` + `.json`,
  `inventario_kit10f.py` + `inventario.json`, `antigo/` e `novo/` com as suites do revisor e a
  saida antes/depois, logs das travas e das CLIs).

## Achados do KIT-10R, veredito por item

| achado | esperado | entregue |
|---|---|---|
| F8 (ALTO) | NaN/inf/bool/string invalida nunca OK; ausencia != defeito; Source/dano/contrib errados continuam REPROVADO | OK — pre-guarda de tipo/finitude; NaN -> REPROVADO, ausente -> NAO_EXERCITADO |
| F9 (ALTO) | aura canonica, contagem inteira medida, sem gatilho repetido = lacuna; preservar 2 itens/2 instancias e 1 item/atributo | OK — `_inteiro_contagem` + canonicidade + dobro exercitado |
| F10 (ALTO) | toda linha declarada do dump conferida; `|` no desc reprova; logs nao-dump neutros | OK |
| F11 (ALTO) | marca de fixture (envelope OU observacao) mantem failclosed; input do dono intacto; API e CLI | OK |
| F12 (MEDIO) | adaptacao OFFLINE minima com positivo/negativos; esperado nunca do display; lacuna declarada se coleta nao emitir | OK — aspecto E + provas; coleta real NAO_EXERCITADO |
| F13 (ressalva) | declarar driver original superado e fornecer driver duravel vigente | OK |

## Prova central (mostrar reprovando e aprovando)

- Suites IMUTAVEIS do revisor (copiadas, nunca editadas):
  - bytes ANTIGOS -> `test_review_kit10.py` **45, 10 FAIL** (exit 1); `test_wrapper_metadata.py`
    **4 FAIL** (exit 1);
  - codigo CORRIGIDO -> as duas **OK** (exit 0).
- Autor 28/28, CIC-4 28/28, RED guardas antigas 7/7: PRESERVADOS.
- Guardas novas load-bearing (positivo passa; neutralizacao seletiva faz o controle falhar;
  restauracao byte-exata passa): 13 controles + 9 guardas, exit 0.
- CLI fixture e CLI envelope-fixture: exit 2 com **0 OK**.

## Limites declarados (NAO_EXERCITADO)

Runtime real, jogo, save, perfil do dono, UI/UX/pixels, desempenho, build, preflight, deploy,
instalacao, publicacao, Bard/gameplay: NAO_EXERCITADO. Todas as cadeias de teste sao simulacoes
OFFLINE explicitamente declaradas; nenhuma DLL foi usada. F4 (estilo historicamente variavel)
permanece INDETERMINADO, sem prova atual e sem mudanca no BetterFont.

## Pendencias para o revisor

1. Confirmar, por execucao propria, que as suites imutaveis FALHAM nos bytes antigos e PASSAM no
   corrigido, e que Autor/CIC-4/RED antigos seguem verdes.
2. Tentar refutar as guardas novas (F8–F12) e o aspecto E (contrato do F12 nao derivado do display).
3. Conferir a preservacao (SHA) e a ausencia de edicao em dependencia compartilhada.
