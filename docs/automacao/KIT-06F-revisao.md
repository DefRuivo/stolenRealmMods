# KIT-06F — REVISAO INDEPENDENTE (run645, revisor != implementador run641)

Cartao t_73f0779f. Revisor run645 (perfil default) reconferindo a entrega do
implementador run641 no MESMO cartao. Ordem: `kanban_show` antes de tocar arquivo.
Rodada 1 de revisao do KIT-06F (nenhum `changes_requested` previo neste cartao):
lente ARTEFATO — li o fonte frio primeiro e so depois comparei com o handoff.

Lentes: artefato (leitura fria do fonte), execucao (rodei tudo de novo, nos
fontes vivos e nos fontes ANTIGOS preservados do run638) e contrato (F1-F8 do
cartao). Nao editei nenhum arquivo de implementacao.

## 1. Fontes vivos reconferidos por SHA256 (batem com a entrega)
```
7afcfe2707f206136ec8c9de79149c8e672aa8ab17c1343ce83e1c109dd2f1d5  tools/automacao/runtime/controle_acesso.py
4e09f97ded34a6deafe5f0e653b81202c327e798c82b1ba98b524a01e019084e  tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs
6fbd5ad31df492fe849e432cd7944f14c81bb5a23c6c025226ecebcdbed7c64c  tools/automacao/runtime/harness-controle/Program.cs
f1926c59e84e711fa9d10071daa613ebf25d4f1fdd0205d45c9e4a0473519069  tools/automacao/kit06/teste_controle_acesso.py
d76b124439d9e648af1ac0c165f928df52d7a2ec44626c8c8b92a59539261df7  tools/automacao/kit06/contra_prova_kit06.py
```
Doc KIT-06F-parte01..06 + entrega: SHA256 conferem com
`scratch/kit/KIT-06F-run641/verificacao-final.json` (DOCS_OK, 7/7).

Fonte ORIGINAL do revisor preservado para reconferencia:
`scratch/kit/KIT-06R-run638/test_revisao_kit06.py` = 68d6283d...cc7a (igual ao
SHA declarado no `handoff-verificado.json` do run638). A copia feita pelo
implementador difere apenas na linha `ROOT` (aponta para os fontes vivos) — o
corpo do oraculo e identico.

## 2. Execucoes INDEPENDENTES (revisor run645)

A/B com o oraculo ORIGINAL do revisor, sem alterar uma linha, contra os fontes
ANTIGOS do run638 (preservados) e contra os fontes VIVOS:

| Prova | ANTES (fonte antigo) | DEPOIS (fonte vivo) |
|---|---|---|
| oraculo Python do revisor (14) | Ran 14, FAILED (failures=10), exit1 | Ran 14, OK, exit0 |
| oraculo C# do revisor (12) | 4 OK / 8 FAIL, exit1 | 12 OK / 0 FAIL, exit0 |

Outras execucoes minhas:
```
suite do autor (viva)            : Ran 45 tests, OK, exit0
contra-prova por regra           : 37 iscas, 0 falhas, exit0
meu medidor de cobertura (AST)   : 45 testes, 37 iscas, uniao=45, 0 sem prova, 0 fantasma, exit0
runner shell real (roda_testes_kit06.sh): VEREDITO KIT-06: VERDE, exit0
harness normal                   : 44 OK / 0 FALHA, exit0
harness --defeito guard          : 3 falhas EXATAS, exit0
harness --defeito ataque         : 2 falhas EXATAS, exit0
harness --defeito inventado      : nome nao suportado, exit2
build isolado (-c Release -p:DeployToBepInEx=false):
    exit0, 0 Erros / 65 Avisos, DLL na copia isolada;
    hash plugins+scripts do perfil do dono IDENTICO antes/depois (sem deploy)
preflight deploy                 : true->sentinela=true (exit0); default->false (exit0); false->false (exit0)
```
Fontes antigos usados no A/B: controle_acesso.py 2e21f539...787e2f (sandbox do
run638) e PonteControleRSTV.cs 6bfe3db1...db6bbbf (sandbox do run638). As libs
KIT04Core (PipelinePassivo.cs 8aec5b8a..., Json.cs 587a36ec...) sao as mesmas
antes/depois, como declarado.

## 3. F7 (falso verde) — refeito por mim com defeito REAL plantado pelo revisor

Plantei eu mesmo o defeito real (`ConsomeInput { get { return false; } }` ->
`true`) numa copia, e rodei o harness ANTIGO (preservado do run638) e o NOVO:

| Cenario | ANTES | DEPOIS |
|---|---|---|
| normal | exit1 (43 OK/1 FALHA) | exit1 -> `guard_sem_foco.sem_consumo_input` |
| `--defeito guard` | **exit0 com 4 falhas = FALSO VERDE** | exit1 "FALSO VERDE / conjunto != declarado", falha EXTRA: `guard_sem_foco.sem_consumo_input` |
| `--defeito inventado` | **exit0 = FALSO VERDE** (nome nem existia) | exit2 "defeito NAO suportado" |

Ou seja: o oraculo de conjunto EXATO discrimina de verdade; nao houve
afrouxamento (a checagem passou de "alguma falha" para "conjunto identico").

## 4. F1-F8 — veredito por item

- F1 (config vazia/rejeitada nao reativa defaults): CORRIGIDO nos dois caminhos.
  `if atalhos is None: atalhos = atalhos_padrao()` + `dict(atalhos)`; `{}` e
  config inteiramente rejeitada ficam DESABILITADOS; motivos preservados em
  `problemas_atalhos`/`problemas_config` no resumo e no CLI. Provado pelo
  oraculo do revisor (2 testes) e por iscas (`atalhos_vazio_reativa_defaults`).
- F2 (OBSERVAR liga/desliga + RETOMAR despachado + parar sem terminal):
  CORRIGIDO. `alternar_observacao`/`AlternarObservacao`; `retomar`/
  `RetomarInterno` com efeito real sobre o pipeline; 2o F7 desliga e pausa.
  Documentacao (topo do modulo) agora casa com o efeito.
- F3 (indicador = efeito; ausencia != coleta): CORRIGIDO. Construtor assume a
  posse pausando o pipeline; `sem_pipeline` e degradacao explicita
  (`coleta_sem_pipeline`); indicador "parado" com pipeline que RECUSA registrar.
- F4 (export nao descarta o que anuncia): CORRIGIDO. Export traz
  `coleta` (eventos com id/dados/quadro, degradacoes, rejeitados, lacunas,
  pedidos/capturas retidas), `trilha_controle`, `degradacoes_controle`,
  `correlacao` sessao_controle/sessao_coleta e `lacunas_honestas`;
  `runtime=NAO_EXERCITADO` (nao fabrica runtime). Paridade C# observada
  (sem lista de capturas no C# porque o core nao expoe captura — "quando
  aplicavel").
- F5 (falha-segura de IO): CORRIGIDO. `exportar`/`ExportarInterno` capturam
  OSError/IOException, degradam `export_falha_io`, devolvem None, nao emitem
  evento de sucesso e nao sobrescrevem a sentinela (sentinela conferida).
- F6 (integridade da evidencia): **PARCIAL** — ver secao 5 (achado).
- F7 (falso verde): CORRIGIDO e reconferido com defeito real proprio (secao 3).
- F8 (contrato KIT-07 honesto): CORRIGIDO. `contrato_kit07()` diz
  `status_kit07=GATE_NAO_SATISFEITO`, `api_kit07_existe=True` (a API
  `montar_pacote` existe em tools/automacao/kit07/exportador.py:548),
  `integracao_efetiva=False`, `export_bruto_local=True`,
  `pacote_compartilhavel=False`; nao adota o exportador reprovado nem duplica
  sanitizacao.

## 5. ACHADO (bloqueia): F6 incompleto no caminho ANINHADO (Python e C#)

Alegação da entrega (parte05): "C# ... `DocumentoExport` usa essas copias".
Nao e verdade para `coleta.eventos`/`capturas`: `_coleta_documento` (Python)
faz `bloco["eventos"] = p.eventos()` e `ColetaDocumento` (C#) faz
`b["eventos"] = _pipeline.Eventos()` — e os acessores do pipeline devolvem
**copia rasa** (`[dict(e) for e in self._eventos]` / `new Dictionary<>(e)`), de
modo que os sub-dicionarios `dados` e `quadro` continuam sendo os OBJETOS
INTERNOS.

Prova do revisor (ambas exit1):
```
scratch/kit/KIT-06R-run645/probe_f6_aninhado.py   (Python)
  doc["coleta"]["eventos"][0]["quadro"]["nota"] = "ALTERADO PELO CONSUMIDOR"
  -> doc2 quadro.nota    = 'ALTERADO PELO CONSUMIDOR'  <== CONTAMINADO
  -> interno quadro.nota = 'ALTERADO PELO CONSUMIDOR'  <== CONTAMINADO (evidencia retida do pipeline!)
  -> doc2 dados.injetado = 'ALTERADO'                  <== CONTAMINADO
  (top-level 'tipo' NAO propaga: 'clique_recebido' — a copia e rasa, so o aninhado vaza)
  marcacao apos mutacao externa = 'original' (preservada — o caso que o F6 provou)
VEREDITO PROBE: PROPAGACAO INTERNA DETECTADA, exit1

scratch/kit/KIT-06R-run645/cs-probe/  (C#)
  doc2 quadro.nota    = ALTERADO PELO CONSUMIDOR
  interno quadro.nota = ALTERADO PELO CONSUMIDOR
  marcacao apos mutacao externa = original
VEREDITO PROBE C#: PROPAGACAO INTERNA DETECTADA, exit1
```
Contra o aceite F6 literal — "Devolver snapshots defensivos coerentes,
**inclusive objetos aninhados quando necessario**" — o item nao esta satisfeito:
o `DocumentoExport` AINDA expoe dicionarios internos mutaveis (os aninhados do
pipeline reusado), e um consumidor que muta o documento corrompe a evidencia
retida e as exportacoes seguintes. O caso plano (marcacoes.descricao) foi
corrigido; o aninhado nao. Nao e nit de estilo: e integridade de evidencia, o
proprio objeto do F6.

## 6. Limites do revisor

- Nao editei implementacao; nao commitei/adicionei/publichei; sem deploy,
  instalacao, jogo, save, foco ou publicacao.
- Builds so em copia isolada com `-p:DeployToBepInEx=false`; perfil do dono
  conferido intacto por hash de plugins+scripts.
- TEMP/TMP/TMPDIR apontados para `scratch/kit/KIT-06R-run645/tmp` nesta rodada.
- UI real/overlay, input do engine, runtime/pixels/foco: NAO_EXERCITADO (KIT-G2).
  PonteControleRSTV ainda nao e chamada por SRAdapterPlugin.Update.
- KIT-07: o texto do descritor ("KIT-07R REPROVADO; KIT-07F em correcao") era
  correto no instante da entrega; o KIT-07F (t_a7318a33) foi aprovado em 22:14,
  logo o texto ficara desatualizado. NAO e defeito do F8 (a integracao era e
  continua opcional/gated, e nao foi declarada como feita); registrar para quem
  pegar a integracao.

## 7. VEREDITO: MUDANCAS SOLICITADAS (F6 aninhado, 1 item; 7/8 achados OK)

Correcao minima exigida (nova rodada no mesmo cartao, mesma instancia de
implementacao ou outra, com hash novo):
1. Python (`_coleta_documento`) e C# (`ColetaDocumento`): entregar COPIA
   PROFUNDA de TODA estrutura derivada do pipeline que entra no documento
   (`eventos`, `capturas`, e qualquer outra com sub-dicionario), de modo que
   mutar o documento devolvido NAO altere a evidencia retida nem exportacoes
   posteriores. Pode reusar o `CopiaValor` ja existente no C#; no Python use
   copia profunda no limite (nao reescreva o pipeline do KIT-05F).
2. Prova positiva E prova negativa da correcao nos DOIS caminhos: teste que
   muta o aninhado e exige que a evidencia interna fique intacta; isca na
   contra-prova (defeito plantado) mostrando o teste reprovando ANTES.
3. Reexecutar: oraculos do revisor (14 py / 12 C#), suite do autor,
   contra-prova, harness normal+--defeito, build isolado. Corrigir a alegacao da
   doc parte05 ("DocumentoExport usa essas copias") para que seja verdadeira.
4. Entregar hashes/comandos/exits novos; revisor em nova instancia reconfere
   ANTES da conclusao. KIT-15 continua gated por este cartao.

Evidencia do revisor: `scratch/kit/KIT-06R-run645/` (probes, logs, sandbox A/B,
medidor de cobertura) e este documento.
