# KIT-08 — parte02: contrato vivo lido e desenho do visualizador

## Contratos vivos inventariados (lidos, não editados)

- `tools/automacao/cenarios/kit09.py` — avalia cenários RSTV em critérios pequenos.
  `avaliar_cenarios(observacoes, identidade, envelope) -> [criterio]`;
  `resumir(criterios, identidade) -> {esquema, criterios_total, identidade{fonte_sha,dll_sha,
  config_sha,sessao_esperada,suficiente}, por_mod, por_capacidade, contagem, procedencias,
  sessoes_observadas, lacunas, origem{sintetica,marcas}, runtime_exercitado, reprovado,
  criterios}`.
- `tools/automacao/cenarios/rstv.py` — contrato do CRITÉRIO (`_criterio`, `_extras`, `_fecha`):
  ```
  criterio = { id, mod, estado, classe, procedencia, esperado, observado,
               evidencia[], motivo, tarefa_origem,
               prova_runtime, fonte_sha, dll_sha, [config_sha], [sessao],
               [tipo_pendencia], [autorizacao_necessaria], [lacuna_probe],
               origem_marcas[], sessoes_lidas[], capacidade_pai, cenario_origem,
               esperado_origem, tarefa_kit, alvos_julgados, [alvos_excluidos] }
  estados: OK | REPROVADO | NAO_EXERCITADO | INDETERMINADO   (pior primeiro)
  ```
- `tools/automacao/runtime/coletor.py` — formato do COLETOR (AUT-4/1): `procedencia`,
  `sessao`, `hash_fonte`, `identidade{hash_fonte_declarado,hash_dll_do_probe,...}`,
  `observacoes[]`, `prints[]`, `manifest`. Fixture rotulada nunca prova runtime.
- Fixtures vivas: `cenarios/kit09-{verdade,velho,la}.entrada.json` +
  `cenarios/kit09-identidade.json`; `runtime/fixtures/probe-saida-exemplo.entrada.json`.

## Desenho do visualizador (`tools/automacao/kit08/visualizador.py`)

Gerador de **um HTML local autocontido** (sem servidor, sem CDN, CSS inline, zero rede),
sobre stdlib. Funções puras + CLI. Consome a saída REAL do KIT-09 (reuso, sem duplicar).

API:
- `contexto_de(identidade, sessao=None, build=None) -> dict` — normaliza contexto
  (fonte_sha, dll_sha, config_sha, sessao, versao_jogo, bepinex, personagem).
- `contextos_compativeis(a, b) -> (bool, [motivo])` — comparação baseline×candidata só
  com MESMO ambiente (versao_jogo, bepinex, config_sha) e, se ambos declaram, mesma
  cena/personagem. Divergência → recusa com motivo.
- `comparar(baseline, candidata) -> dict` — se contextos incompatíveis → estado
  `INDETERMINADO` (nunca compara); senão diff por critério (id → estado A/B), com foco
  em regressões (baseline melhor que candidata).
- `aprovacao_stale(aprovacao, contexto_atual) -> dict` — `aprovacao` registra o
  `fonte_sha`/`dll_sha` contra o qual foi concedida; se o contexto atual tem fonte
  diferente → `stale=True`, motivo, e a aprovação NÃO é reapresentada como válida.
- `escapar(texto)` = `html.escape` (tudo que vem de dado passa por aqui).
- `referencia_local_segura(ref) -> (ok, motivo)` — só caminho relativo dentro do pacote;
  recusa `http(s):`, `javascript:`, `data:` de script, `\\` de rede e `..` (traversal).
- `renderizar(doc) -> str` — HTML único com, por caso/mod: esperado, observado, prova,
  imagem (se houver e segura), sessão/build/config, lacunas; seções separadas de
  **veredito técnico** e **aceite humano/publicação**; CSP meta sem `unsafe-inline`
  de script; nenhuma tag `<script>` gerada a partir de dado.
- `main()` — CLI `--entrada <json> [--identidade <json>] [--baseline <json>]
  [--saida <html>] [--aprovacao <json>]`.

`doc` de entrada (envelope de sessão para o visualizador):
```
{ "esquema": "KIT-08/sessao/1", "mod": "...", "identidade": {...}, "build": {...},
  "sessao": {...}, "resumo": <saida de kit09.resumir> | "criterios": [...],
  "baseline": {...}, "aprovacao": {...} }
```
Reuso: se vier `observacoes`+`identidade`, o visualizador chama `kit09.avaliar_cenarios`
(e `resumir`) por importação por caminho — mesma infraestrutura, sem reescrever o avaliador.

## Estados e veredito

- Técnico: PASSOU só quando o critério é `OK` **e** `prova_runtime=True` **e**
  procedência `runtime` (fixture nunca PASSOU).
- `NAO_EXERCITADO`/`INDETERMINADO` distintos de `FALHOU`; lacunas listadas.
- Aceite humano/publicação: campo separado, default "PENDENTE (não concedido)";
  a ferramenta NUNCA auto-aprova nem publica.

## Testes planejados (`tools/automacao/kit08/teste_visualizador_kit08.py`)

XSS/escape; sem rede/sem `<script>` de dado; referência local segura (recusa
javascript/data/traversal/absoluto); contexto compatível compara e incompatível recusa;
fonte alterada → aprovação STALE; campos por caso presentes; fixture nunca OK;
aceite humano separado; determinismo byte-a-byte. Contra-prova por defeito plantado
(escape off, ref remota permitida, stale aceito, incompatível comparado, auto-aprovação).

**Checkpoint parte02:** contratos lidos e desenho fixado; próximo = implementar
`visualizador.py` (parte03).
