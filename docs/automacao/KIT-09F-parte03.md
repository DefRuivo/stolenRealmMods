# KIT-09F — parte 03: cobertura e contrato novo da suite do autor

## Suite do autor (`tools/automacao/cenarios/test_kit09.py`)

O que foi acrescentado/corrigido (sem enfraquecer asserção nenhuma):

- `_cobertura_exata` (F7): exige que `CONTROLES` e a nova tabela `AUSENCIA` cubram o
  conjunto EXATO dos 21 IDs, e roda cada ausência checando `estado != OK` e
  `prova_runtime is False`.
- `CONTROLES` ganhou 3 linhas: `render-nao-aconteceu` (o ID que faltava),
  `clique-alvo-errado` (`MainMenu/QuitButton`) e `sintetico-com-defeito`
  (sintético com defeito tem de continuar REPROVANDO). Total 24 linhas / 21 IDs + 3
  adversariais; a cobertura exata é conferida pelo teste, não por contagem manual.
- `AUSENCIA` (nova): 21 pares `(critério, campos removidos)` — a ausência de leitura não
  pode virar OK nem `prova_runtime`.
- `_sintetico_nao_qualifica` (F1): envelope sintético, lista com rótulos propagados pelo
  desempacotador e observação sintética nunca fecham OK; `origem.sintetica=true` no resumo;
  defeito em entrada sintética continua REPROVADO.
- `_normalizado_defeito_reprova` (F2/F4): usa o `normalizar_observacao` do coletor REAL —
  defeito medido REPROVA, positivo normalizado fecha OK, malformado e `inf` não são OK.
- `_dado_velho` (F6): sessão velha não qualifica NENHUM critério (nem `prova_runtime`),
  `runtime_exercitado=false`, e defeito observável não é suprimido.
- `_adaptador_coletor` (F5): o input do bloco `campos` passou a usar o alvo DECLARADO
  `BottomBar/SkillsButton` (antes `BottomBar/Skills`), porque alvo diferente do declarado
  agora REPROVA — o alvo errado ganhou controle próprio em `CONTROLES`.

## CONTRATO NOVO (declarado, não mascarado)

Antes, a suite exigia `exit 0` e 21 OK para o artefato `kit09-verdade.entrada.json`
(que se declara `sintetico=true`/`rotulo_fixture`). Depois da correção F1 esse artefato
NÃO qualifica runtime — logo a suite mudou de asserção:

- `_caminho_ok` passou a exercitar o caminho OK com uma SIMULAÇÃO POSITIVA NÃO ROTULADA
  (em memória), preservando as três asserções de OK (estado, `prova_runtime`, `sessão`);
- `_cli` passa a exigir: (1) exit 0 para simulação não rotulada (21 OK,
  `runtime_exercitado=true`), (2) exit 2 para o artefato sintético declarado (zero OK,
  `runtime_exercitado=false`, `origem.sintetica=true`), (3) exit 1 para dado velho,
  (4) exit 2 para malformado/ausente. Os três exit codes ficam distintos e exercitados.

## Prova RED durável (F7)

`tools/automacao/cenarios/prova_red_kit09.py` (novo, no repositório e não só em scratch):
12 mutações, cada uma neutralizando UMA guarda específica do `kit09.py`, com a checagem
normativa correspondente. O fonte do repositório nunca é reescrito (mutação in-memory) e
o SHA256 é conferido antes/depois; além disso o driver materializa o mutante de
render-observado numa cópia descartável de `tools/` e roda a suite durável: a suite
REPROVA com o mutante e volta a PASSAR com o byte restaurado.
