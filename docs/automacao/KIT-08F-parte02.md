# KIT-08F — parte02: correção aplicada (o que mudou e por quê)

Cartão t_ac0f78f7, run654, perfil default. Implementação em
`tools/automacao/kit08/visualizador.py`.

- BASELINE reprovado (lido de volta): sha256
  `3d6d2983a845d1423859ef75f7f8e658cde7c14c0d4fe3ee23194d08a9789701` (confere com o
  corpo do cartão). Cópia byte a byte preservada em
  `scratch/kit/KIT-08F-run654/sandbox/tools/automacao/kit08/visualizador.py` e usada
  para o RED.
- CORRIGIDO (entrega): sha256
  `bdd33622a1cec76f83636dc095df73fdfde972072cf0809007d70593cdcfa85f` (cópia idêntica em
  `scratch/kit/KIT-08F-run654/visualizador-entrega.py`). Só este arquivo de produto foi
  alterado; nenhum mod/avaliador de outra frente foi tocado.

## Mudanças, achado por achado

F1 `referencia_local_segura` — além de esquema/absoluto/UNC/traversal/vazio, agora
recusa `%` (percent-encoding decodificaria `%2e%2e` para `..`), `?`/`#`
(consulta/fragmento não é caminho de arquivo) e `:`. Os positivos locais
(`a/b.json`, `scratch/kit/k08/x.png`, `assets/capture.png`) continuam aceitos.
Isto é HARDENING lexical: efeito específico em browser (file://, CSP, resolver de
URL) NÃO foi exercitado e NÃO é alegado como exfiltração provada.

F2 `avaliacao_aprovacao` (nova) + `_secao_aprovacao` — estados distintos
`ausente|invalida|stale|vigente`. Ausência/vazio nunca renderiza "VIGENTE"; o rótulo
VIGENTE, quando legítimo, sai como `<b class="passou">` (o texto exato
`<b class="">VIGENTE</b>` não é mais produzido em nenhum caminho). Regras: sem
rótulo fixture/sintético; precisa declarar fonte_sha+dll_sha E todo hash que o
contexto atual traz (config_sha inclusive); precisa de `mod` e igual ao do contexto;
fonte alterada → STALE; hash declarado que o contexto não traz → não confirmável.
Positivo verdadeiro (completo, mod igual, hashes iguais) SEGUE VIGENTE (controlado).

F3 `comparar` — passa `origem_sintetica` de CADA lado para o veredito (fixture não
vira PASSOU); ids duplicados RECUSAM; lado sem casos RECUSA; regressão passa a ser
medida pelo RANK do VEREDITO (`PASSOU 3 > NAO_EXERCITADO 2 > INDETERMINADO 1 >
FALHOU 0 > (ausente) -1`), então perda de prova conta como regressão e caso removido
vira `(ausente)` = pior. Defeito observado continua FALHOU.

F4 `contextos_compativeis` — simetria do declarado: chave declarada de um lado só
RECUSA (`config_sha`, `personagem`, `cena`, `build_id`, `build`), divergência RECUSA,
e `mod` entra no contexto (ModA != OTHER RECUSA). Fonte/DLL seguem FORA da lista de
simetria: uma candidata com dll/fonte próprias continua comparável (controlado).

F5 `veredito_tecnico` — `prova_runtime is True` (string "false" não passa); evidência
não vazia obrigatória; `inconsistencias_do_criterio` demove quando fonte_sha/dll_sha/
config_sha/sessão do critério contradizem o contexto vivo do documento;
`origem_sintetica` agora olha também `identidade` (rotulo_fixture/sintetico
aninhados). Sem exigir autenticador criptográfico novo.

F6 `mesclar_identidade` + `main` — a identidade de `--identidade` é mesclada no
envelope ANTES de `montar_doc`/`kit09.avaliar_cenarios`. CLI e API passam a dar a
MESMA contagem (provado: 21 critérios, `{PASSOU:20, NAO_EXERCITADO:1}` nos dois).

F7 exit — agrega TODAS as etapas: FALHOU, aprovação STALE/INVALIDA ou comparação
não-OK (recusada ou com regressão) → exit 1; nada conclusivo → exit 2; verde → exit 0.
Comparação recusada e caso removido deixam de sair em exit 0.

F8 — sessão string preservada (`isinstance(str)` ANTES de coagir para dict; era
descartada); imagem local resolvida a partir da pasta da entrada, com confinamento por
`commonpath`, EMBUTIDA como `data:` (bytes reais conferidos por decodificação). Se não
resolve, a lacuna é explícita ("nao embutida") e o cabeçalho NÃO afirma autocontido.

F9 `main` — entrada e opcionais lidos dentro do `try` (`OSError`/`ValueError` →
exit 2 com diagnóstico e sem traceback); JSON malformado idem.

## Invariantes preservadas

As 11 âncoras de mutação de `contra_prova_kit08.py` e de `review_controls.py`
(`return html.escape(...)`, a CSP, `if not isinstance(ref, str):`,
`return (not motivos), motivos`, `return bool(motivos), motivos`,
`if estado == OK and provou and proc == "runtime":`,
`return "NAO_EXERCITADO" if fixture else "PASSOU"`, `if estado == REPROVADO:`/FALHOU,
`PENDENTE (nao concedido por esta ferramenta).`,
`doc["resumo"] = kit09.resumir(criterios, ident)`,
`AQUI = os.path.dirname(...)`) aparecem exatamente 1x cada — conferido por script.
