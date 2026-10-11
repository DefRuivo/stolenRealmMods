# KIT-10R — run663 — parte08: fechamento verificado

Complemento final ao parecer docs/automacao/KIT-10R-revisao.md; não sobrescreve arquivo/histórico.

## Empacotamento lido de volta

`python scratch/kit/KIT-10R-run663/verify_evidence.py --package`:
- baseline1156: live_changed=[] e sandbox_changed=[];
- scannerdirigido206arquivos: formatosconhecidos0, candidatoheurístico1, classificação EXATA public-source-sha-with-label (rótulo do SHA público na parte06); zero candidato não classificado;
- controles em memória de formato e entropia detectados (true/true);
- exitBRUTO do scanner continua1 (ACHADOheurístico), não enfraqueci scanner nem o declarei verde. Retorno0 do shell foi só extração de resultado.

Arquivo real C:/dev/stolen-realm/scratch/kit/KIT-10R-run663-evidencias.zip:
- SHA256 44a5f57a3c9ecc8231a14da0b73fdd29174c849590fbc9e0b892674b8085be63;
- 5.331.500bytes, 1361entradas únicas;
- ZipFile.testzip()=None (integridadeCRC confirmada);
- no_dll=true e no_git=true;
- report_included=true (parecer final dentro doZIP).
Readback: scratch/kit/KIT-10R-run663/zip-verification.json. ZIP inclui snapshot de sandbox+provas, não pacoteThunderstore nem evidência de runtime. Esta parte08 foi criada DEPOIS doZIP e fica separada, sem alegar inclusão no pacote.

## Grafo verificado nativamente

`kanban_show(t_48b78ecb)` leu conserto criado de volta: status todo, parents=[t_896796be], children=[t_0a434c97,t_a1f38855]. Logo gates de KIT12 e KIT14 confirmados, não apenas resposta de escrita de link. Perfildefault real, nova instância exigida, independente de reviewer663. Revisão técnica obrigatória same-card no conserto, nenhum cartão de revisão duplicado.

## Fechamento

Parecer REPROVADO; 49testes próprios=14FAIL/35OK, ERROR0skip0; quatrogrupos de falsosOK F8–F11 e lacuna BetterStatsF12. Positivo/negativo mostrados:35/35controles individuais Ran1FAIL/exit1 ->fonteSHArestaurado ->Ran1OK/exit0; autor28/28 e CIC428/28, REDvigente7/7. REDoriginalobsoleto exit1 declaradoF13. Nenhum produto editado, instalado ou publicado. Esta revisão pode concluir; entregaKIT10/DoD não foi aprovada e consumidores aguardam conserto t_48b78ecb.
