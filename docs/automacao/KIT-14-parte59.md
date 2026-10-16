# KIT-14 — run1471 — rodada interrompida recuperada

Inspecionados os filhos: KIT14R t_9ce7d260 revisão independente; BP5 t_49686933 e LEVEL-RT-INGAME t_fc484826 escopos posteriores. Não duplicar nem executar seus trabalhos.

Correção ao checkpoint anterior: a execução run1442 avançou DEPOIS da parte56 e deixou runtime-console.log e boot01/result.json. Portanto houve boot real upstream em14/10/2026 10:16:32, PID22132, sessão KIT14-run1442-boot01-20261014-101617. Não repetir boot só porque faltou relatório final.

Lidos driver.py, result.json e console: dez etapas registradas exit0, observed_status=CONCLUIDO,53.443288s, dois PNG de1156095 bytes com hash idêntico99bc0c349…. Isto ainda é sinal terminal do probe, NÃO prova janela/tooltip nem cadeia ponta a ponta. Conteúdo/resultados reais serão conferidos diretamente.

Rollback declarado no JSON:115 arquivos dados,53 perfil,5 outro jogo iguais antes/depois; PlayerPrefs export igual; jogo fechado, junction/backup/perfil temporário ausentes, lock liberado. Cloud OFF inicial/final (não modificada), porém remotecache mtime mudou durante boot: não alegar imutabilidade Cloud remota/cache. Readback atual antes desta descoberta também encontrou jogo fechado/diretório real sem junction.

Nesta execução run1471 ainda zero novo boot/build/deploy. Próximo: extrair campos úteis de provas/probe/recorder, conferir hashes e PNG, avaliar cobertura e lacunas, depois executar só residual necessário em bancada nova se possível.
