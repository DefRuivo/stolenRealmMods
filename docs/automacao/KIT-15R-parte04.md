# KIT-15R — parte 04: primeiras execuções e dependências

Terminal em sandbox própria, TMP/TEMP/TMPDIR corrigidos e tempfile.gettempdir medido = C:/dev/stolen-realm/scratch/kit/KIT-15R-run678/tmp.

## C5 ACHADO confirmado F1 — artefato antigo
Diff real ZIP/vivo de descoberta.py modifica comportamento de raiz_efetiva (fontes de ambiente e fallback). ZIP a04ffc59125cff05ce2b994049709cb6375ca7fdfc4118150cdae0913dae0f97 != vivo 10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86. Não é apenas timestamp/README. ZIP autor CRC válido não elimina a deriva.

## Suíte autor e contra-prova
python sandbox/tools/automacao/kit15/teste_kit15.py: Ran 18 tests in 5.081s, OK. Contra-prova em sandbox sem bin/obj: baseline verde, 6/7 recusados; D7 SEM-EFEITO, CONTRA-PROVA|FALHOU. Esse D7 depende da presença de bin/obj do ambiente do autor, não planta sua própria isca. Não contar como prova negativa verde. A chamada terminal agrupada terminou exit 0 devido ao último comando montar; exits individuais serão recapturados em runner independente. Logs D1..D7 e resultado: scratch/kit/KIT-15R-run678/contra-autor/.

## C5 positivo em sandbox
pacote.py montar --saida scratch/kit/KIT-15R-run678/pacote-proprio --json: PACOTE_LIMPO; 42 membros, 164928 bytes, CRC null, scan 0; SHA256 a524746a8292d3be417c209a9e493c8a07295f22f46ac9c511633e7c7bd352ad. Relatório próprio em pacote-proprio/pacote-relatorio.json; 29 arquivos de componentes mais 12 ferramenta/docs (total_arquivos só conta componentes).

## C2 dependências — leitura real
Runner executor.py:64-67,126-131 importa ../runtime/coletor.py, mas pacote põe recorder em ../recorder. Viewer visualizador.py:38-39 importa cenarios/kit09.py ausente. Integracao.py:91-95 depende de pertinencia.json, ciclo/ciclo.py, ciclo/decisao.py, kit10/kit10_cenarios.py, aceite/relatorio_aceite.py não selecionados pelo recipe. Exercitar funções/CLI no ZIP limpo antes de fechar achado.
C# Adapter ProjectReference ../KIT04Core/KIT04Core.csproj (pacote chama pasta core) e referências ../../../../lib; Core/Adapter têm GameManaged fixo em E:/SteamLibrary. Sem build: preflight não executado e não autorizado buscar dados do jogo/perfil. Prova de resolução lexical será feita no ZIP extraído; compilação e runtime continuam NAO_EXERCITADO.

## C3 e C4
Uso básico sem SDK/Python, exemplos SDK/cenários e comandos da documentação ainda sujeitos à prova própria. Fonte e ferramentas disponíveis não equivalem a kit executável independente.
