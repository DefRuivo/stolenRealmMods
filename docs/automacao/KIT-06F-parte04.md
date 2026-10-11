# KIT-06F — parte 04: F4 e F5 (export)

F4 (export nao descarta o que anuncia): `documento_export` ganhou:
- `coleta`: reuso DIRETO do pipeline KIT-05F — `eventos` (ids/dados/quadro),
  `degradacoes`, `rejeitados`, `lacunas`, `pedidos_retidos`, `capturas_retidas`,
  `resumo`;
- `trilha_controle` (eventos do controle), `degradacoes_controle`;
- `correlacao` {sessao_controle, sessao_coleta};
- `lacunas_honestas` (ex.: sem pipeline = coleta NAO operante; parado = historico).
C# espelha via `ColetaDocumento()` + `correlacao` + `trilha_controle`.
Nao se fabrica runtime: `runtime=NAO_EXERCITADO`.

F5 (falha-segura de IO): `exportar`/`ExportarInterno` capturam OSError
(FileExistsError/IOException/UnauthorizedAccessException...), degradam
`export_falha_io` e devolvem None — SEM evento de sucesso e SEM sobrescrever
conteudo alheio. Sentinela (arquivo no lugar da pasta) preservada e testada.
