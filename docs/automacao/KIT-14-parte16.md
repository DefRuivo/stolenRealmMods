# KIT-14 — checkpoint 16 / run702

## Execução real do harness
Terminal: test_guardas.py Ran 5 tests / OK, exit 0; py_compile passou. Controles offline verificam recusa de jogo existente, raiz reutilizada, hash errado e fonte alterada. Mutação seletiva em memória remove só o guard do jogo e aceita o input anteriormente recusado: prova da guarda, não runtime.

Primeira coleta_readonly.py: exit 1 antes de lock/install/boot, front-check exit 127. stderr: /bin/bash não encontrou caminho com barras Windows removidas (C:dev...). Result/result.json e commands.json iniciais preservados. Jogo permaneceu fechado.

## Correção somente no harness descartável
Bash e caminhos descobertos por terminal; Git bash existe em C:/Program Files/Git/bin/bash.exe. Troquei invocação ambígua 'bash' por esse executável e script em formato forward-slash. Evidência da segunda tentativa terá diretório novo attempt02, para não reescrever o resultado inicial. Nenhum arquivo do produto/pais editado.

## Diagnósticos
write_file/py_compile não acharam erro sintático. Pyright apresenta inferência estreita de RESULT e import dinâmico do coletor; são avisos de análise estática do harness, não escondidos nem tratados como build C# validado. O coletor já existe e será importado de caminho lido, sem inventar API.

## Estado
Nada instalado/aberto nesta primeira tentativa. Limites readonly/Cloud/proibição de navegação permanecem. Retomada não rebuilda nem refaz offline do run699.
