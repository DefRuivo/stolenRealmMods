# KIT-14F4 — parte04: patch de integração (identificado, NÃO aplicado)

Arquivo: `scratch/kit/KIT-14F4-1533/patch-integracao.diff` (479 linhas, `diff -u`).
Alvo no repositório: `tools/automacao/runtime/AUT4Probe/RstvPostRender.cs` (hotspot — fonte
principal compartilhada, tem mudanças manuais/PartyDriver; **não** foi tocada nesta rodada).

## Conteúdo do patch (por bloco)

1. **Leitor de texto em duas famílias vivas** — `TextoRenderizado()`, `GeometriaLegado()`,
   `LeituraLegado()`: TMP (`text` + `GetParsedText()`) e `UnityEngine.UI.Text` do host vivo
   (`text` é o próprio renderizado; nada é inferido). Mesmas chaves do leitor TMP do probe.
2. **Painel por objeto vivo** — `RstvPainel(out origem)`: campo estático do produto quando
   disponível; senão o `GameObject` do contrato (`RstvAllSkillTreesPanel`) na cena viva, com cache
   e varredura limitada a cada 10 quadros. A fonte usada é registrada em cada diagnóstico.
3. **Hover pelo nome de tipo do componente vivo** — `RstvHovers()` com
   `RoguelikeSkillTreeVisualizer.RstvSkillHover`; skill comparada por `SkillInfo.SkillName`
   (trim + case-insensitive) e tipo diferente de `Bard`. Sem inventar GUID nem mexer em filtro.
4. **Diagnóstico por guarda** — `RstvNota()` com motivo + estado vivo do mesmo quadro
   (`painel_*`, `textos_no_painel`, `hover_candidatos`, `hover_casou`, `skills_no_painel`,
   `tooltip_*`, `frame_before_open`), limitado a 120 entradas, deduplicado por motivo/90 quadros,
   exposto em `rstv_coleta.diagnostico` e `rstv_diagnostico`, com gravação incremental do JSON
   durante a espera (5 s).
5. **Teto de espera 35 s → 40 s** — abaixo da janela de 120 s do arnês (teto maior fazia o
   processo ser fechado sem prova).
6. **Captura do alvo efetivo quadro a quadro** — `_rstvObserved = PersonagemDaSessao()` até
   obter, com `frame_observado` na amostra. Nunca substituído pelo alvo esperado.
7. **`componente_do_texto`** por amostra e nota de escopo de visibilidade explícita (não é clique
   físico, oclusão nem aceite de UIUX).

## Guardas preservados (o patch NÃO afrouxa nada)

* `owners` continuam vindo de patches Harmony reais do assembly vivo; nada é removido.
* Nenhum valor de estado é fabricado; `snapshot_depois` ausente continua ausente.
* Gate full-rstv e avaliador canônico (`tools/automacao/cenarios/rstv.py`) intactos.
* Nada de RSTV/gameplay/assets/`Assembly-CSharp.dll`; nada de Bard; sem deploy no Default.
* Produtor F3 (recorder) intocado.

## Como aplicar (quando houver decisão humana)

    cd C:/dev/stolen-realm
    git apply --check scratch/kit/KIT-14F4-1533/patch-integracao.diff
    git apply scratch/kit/KIT-14F4-1533/patch-integracao.diff
    dotnet build tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj -c Release -p:DeployToBepInEx=false

(`git add` sempre por caminho explícito de arquivo, nunca de diretório.)
