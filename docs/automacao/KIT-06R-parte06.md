# KIT-06R — parte 06: fechamento das lacunas de execução

## Runner completo exercitado em shell real PASSOU

Alternativa simples, sem substituir política: `bash scratch/kit/KIT-06R-run638/sandbox/tools/automacao/kit06/roda_testes_kit06.sh` no terminal real: `Ran 35 tests`, OK; 13 iscas/falhas 0; autoteste 9/9; `VEREDITO KIT-06: VERDE (exit 0)`, exit 0.
`PYTHON='C:/nao/existe/python.exe' bash scratch/kit/KIT-06R-run638/sandbox/tools/automacao/kit06/roda_testes_kit06.sh`: saída interpretador inexistente, exit 2. As tentativas subprocess bash e parser bloqueado permanecem no histórico; não são verdes nem atribuídas ao produto. O runner direto funciona sem .git.

## Cobertura negativa honestamente medida

Python AST enumerou 35 testes; FAILs nos 13 logs de isca somam 18 testes distintos mostrados reprovando. 17 não mostrados reprovando pelo driver do autor; lista completa em cobertura-negativa.json. Esta revisão mostrou os quatro oráculos próprios positivos reprovando com defeitos reais, mas não alega cobertura negativa total dos 35 do autor. Correção deve completar essa evidência sem inserir self.fail arbitrário nem enfraquecer trava.

## Contenção de temporários: desvio e ajuste

Consulta do ambiente real encontrou TEMP/TMP/TMPDIR=%USERPROFILE%/AppData/Local/Temp (diferente do contexto inicial). O harness do autor usa Path.GetTempPath e de fato deixou kit06-harness-0.json (770 bytes) em Temp/harness-controle-kit06; isso é export sintético do harness, não mod/deploy/perfil/save, mas ficou fora do workspace. Não apagado nem atribuído ao dono. Suíte/contra-prova do autor também utilizam tempfile sem dir explícito. Esta revisão registra o desvio; executou `export TMPDIR=.../KIT-06R-run638/tmp`, TEMP e TMP iguais, e criou a pasta própria para subsequentes testes. Nenhum futuro teste deve herdar Temp do sistema sem verificar. Não alegar ausência absoluta de escrita externa nesta revisão.

## Parecer consolidado provisório

REPROVADO offline: F1 configuração reativada; F2 toggle/retomar; F3 indicador sem efeito; F4 export incompleto; F5 IO sem falha-segura; F6 alias mutável de evidência C#; F7 falso verde no harness; F8 integração KIT-07 ausente/descritor obsoleto. F8 não exige usar exportador ainda reprovado sem guard: precisa contrato opcional correto e gate explícito caso KIT-07 indisponível, não string NAO_IMPLEMENTADO falsa nem export bruto confundido com pacote privado.
Contexto limpar None fica INDETERMINADO (não conta como achado); UI real/engine/runtime NAO_EXERCITADO. Identidade/preservação dos 188 arquivos medidos conferem; execução positiva nominal e controles negativos próprios têm logs reais. Próximo passo: registrar correção em nova instância, gate de KIT-15 e revisão independente da correção. Não alterar produto nesta frente.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
