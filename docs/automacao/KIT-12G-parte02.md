# KIT-12G parte02 — implementacao da correcao F5 (run671)

## 1. O que mudou em `tools/automacao/kit12/integracao.py`

1. `CAMPOS_CADEIA` ganhou `dll_probe_sha` (a identidade da DLL do INSTRUMENTO viaja com a
   cadeia e entra no `cadeia_sha`). Constantes novas:
   `CAMPOS_INSTRUMENTO = ("hash_dll_do_probe",)`, `ALIAS_COLETA_DLL = ("dll_sha",)`,
   `CAMPOS_DECLARADOS_CONFRONTAVEIS = ("fonte_sha", "config_sha", "versao", "sessao")`.
2. `instrumento_da_coleta(coleta_meta, probe_dll=None)` -> `(sha, origem, arquivo)`:
   medicao primeiro (`--probe-dll` -> `medido-cli`; `identidade.arquivo_dll_do_probe` existente em
   disco -> `medido-arquivo`), depois declaracao canonica da coleta
   (`identidade.hash_dll_do_probe`, `identidade.dll_sha`, `dll_sha` de topo -> `declarado-coleta`).
3. `carregar_coleta` le e PRESERVA os campos que o produtor escreve: `hash_fonte` (alias
   `hash_dll`), instrumento declarado, caminho da DLL do probe, `declarados`
   (`fonte_sha`/`config_sha`/`versao`/`sessao` do topo e/ou do bloco `identidade`) e
   `incoerencias` (topo x identidade). O fallback `hash_fonte or fonte_sha` (a raiz do F5) foi
   REMOVIDO.
4. `_avaliar_coleta` substitui a antiga `confrontar_coleta` (que continua existindo como
   wrapper compativel, devolvendo a lista de achados):
   - `hash_fonte` ausente -> `ausente`;
   - `hash_fonte` != instrumento MEDIDO -> `contraditoria` (via `instrumento-medido`);
   - `hash_fonte` != instrumento declarado PELA PROPRIA coleta -> `incoerente`;
   - instrumento medido != instrumento declarado -> `incoerente` (`hash_dll_do_probe`);
   - sem instrumento nenhum: vale o alias documentado `hash_fonte == ident["dll_sha"]`;
   - `fonte_sha` NUNCA confere procedencia de coleta;
   - (S10) cada campo declarado pela coleta e confrontado com a identidade da rodada; divergencia
     -> `contraditoria`, campo sem par na identidade -> registrado como `nao-confrontavel`
     (sem lacuna).
5. Bloco (2c) de `criterios_da_cadeia` cria lacunas nomeadas por tipo:
   `cadeia/coleta-ausente/<campo>`, `cadeia/coleta-contraditoria/<campo>`,
   `cadeia/coleta-incoerente/<campo>` — sempre com `rebaixar_ok` (fail-closed). O `coleta` de
   cada criterio carrega `hash_fonte_confronto`, `hash_fonte_campo_identidade`,
   `instrumento_sha/origem/arquivo`, `campos_declarados_pela_coleta` e `confrontos_declarados`.
6. `identidade_cadeia(..., coleta_meta=, probe_dll=)`, `cadeia(..., probe_dll=)`,
   `verificar(..., probe_dll=)` (a verificacao reusa o `coleta` guardado) e CLI ganhou
   `--probe-dll`. `limites` declara o limite (instrumento apenas declarado) e o `_imprimir`
   mostra `dll_probe_sha`/origem.

## 2. Provas executadas (rodada 1 desta correcao)

- suite: `python tools/automacao/kit12/test_kit12_integracao.py` -> **Ran 30 tests / OK**
  (exit 0). 6 testes novos + o antigo `test_positivo_coleta_com_hash_conferido_mantem_o_ok`
  reescrito (ele usava `hash_fonte == fonte_sha`, a convencao ERRADA que o F5 introduziu).
- isca: `--isca` -> **14/14 mutacoes discriminadas**, controle restaurado verde (exit 0).
  5 guardas novas: `confronto_volta_para_fonte_sha`, `instrumento_medido_ignorado`,
  `incoerencia_da_coleta_ignorada`, `instrumento_declarado_ignorado`,
  `campo_declarado_pela_coleta_ignorado`. A mutacao `coleta_contraditoria_ignorada` (run669)
  foi reapontada para o novo texto do fonte.
- CLI em sandbox externa (`prove_ciclo.py` reescrito no formato do PRODUTOR VIVO):
  exits **2 -> 1 -> 2 -> 2 -> 2 -> 2 -> 3** e `PROVA|PASSOU`:
  1. fixture marcada + envelope do produtor + `--probe-dll` (medido) -> INCOMPLETO/2, procedencia
     `confere` pelo campo `dll_probe_sha(medido)`, zero lacuna `cadeia/coleta-*`;
  2. defeito plantado -> REPROVADO/1 com fila (criterio + causa/caminho + prova);
  3. correcao controlada -> INCOMPLETO/2 sem OK;
  3b. `hash_fonte` de outros bytes -> INCOMPLETO/2 + `cadeia/coleta-contraditoria/hash_fonte`;
  3c. `hash_fonte` = `fonte_sha` da RODADA (convencao errada do F5) -> INCOMPLETO/2 +
     `cadeia/coleta-contraditoria/hash_fonte` — etapa-armadilha: falha se a confrontacao voltar
     para `fonte_sha`;
  3d. envelope incoerente com o instrumento que ele mesmo declara -> INCOMPLETO/2 +
     `cadeia/coleta-incoerente/hash_fonte`;
  4. `--verificar` apos mudar a config -> exit 3.
- referencia REAL do formato: `docs/automacao/AUT-4-evidencias/r3-confirmada/aut4probe.json`
  (`hash_fonte == identidade.hash_dll_do_probe == 407c5c63…`, invariante checado pelo teste e
  registrado em `prova.json.formato_do_envelope.referencia_real.invariante=true`).

## 3. Nota de COMPATIBILIDADE (muda o resultado das sondas de rodadas anteriores)

- A sonda S9 da revisao run668 ("coleta declarando o hash DA RODADA" -> `confere`) usava o
  `fonte_sha` como "hash da rodada". Agora isso e **CONTRADITORIA por definicao** — aceitar
  `fonte_sha` era exatamente o defeito F5. A contra-prova equivalente ("a correcao nao virou
  trava cega") passa a ser: coleta declarando o instrumento MEDIDO (`--probe-dll`) ou o
  `dll_sha`/instrumento declarado coerente -> `confere` e o OK offline sobrevive (teste
  `test_positivo_coleta_com_instrumento_da_rodada_mantem_o_ok`, caso (a) e (b), e etapa 1 do
  `prove_ciclo.py`).
- `confrontar_coleta(coleta_meta, ident)` continua devolvendo LISTA de achados (compativel);
  `confronto_da_coleta` devolve `(achados, confronto)` com o registro de qual campo conferiu.
- `carregar_coleta` NAO le mais `doc["fonte_sha"]` como `hash_fonte` (era a origem do F5).

NAO_EXERCITADO: jogo/probe/save/perfil real, runtime AUT-4, UI/UX/pixels, build C#,
pre-flight de deploy, instalacao, publicacao, gates KIT-G1..G4 e aceite humano/DoD.
