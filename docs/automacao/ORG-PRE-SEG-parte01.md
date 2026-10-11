# ORG-PRE-SEG — parte 01: triagem integral de entropia e regressão da trava

Tarefa t_5c8f7f57. Rodada local em 11/10/2026, repositório C:/dev/stolen-realm, base de entrada 8b575c6 (ORG-R1; checkpoint anterior 097f950). Escopo exclusivo: detector genérico, suíte nova e este relatório. Não reorganiza o repositório nem altera fonte de mod.

## Resultado

Baseline reproduzido: `python -B tools/check_segredos.py` retornou 1, com ZERO formatos conhecidos e **72 ocorrências de entropia em 35 arquivos**. A saída padrão mostrava só 40; a triagem enumerou as 72, inclusive ocorrências diferentes na mesma linha de JSON minificado. Não se tratava de 72 credenciais confirmadas.

Todos os achados foram classificados por contrato e proveniência: 35 marcadores AUT4, 2 sessões AUT4 com rótulo, 3 nomes de ensaio INT-R1, 15 referências a um critério KIT09, 5 hashes SHA-256 rotulados e 12 sessões KIT14. **Zero ocorrências sem classificação; zero credenciais reais identificadas nesta amostra.** Nenhum valor suspeito foi copiado para este relatório, comentários do cartão ou saída de diagnóstico; a evidência de triagem contém apenas localizadores, classe e medidas. Nenhum serviço remoto foi consultado para testar autenticação.

Depois do ajuste, os scanners reais retornaram 0. A comparação exaustiva de candidatos antes/depois mudou **exatamente as 72 decisões triadas**, não outras decisões dos arquivos versionados da amostra. Os arquivos históricos/evidências não foram removidos, redigidos nem reescritos para fazer o gate passar.

## Por que são dados públicos, não segredos de autenticação

1. **AUT4 (37 ocorrências).** `tools/automacao/runtime/coletor.py:1326-1327` gera a sessão com data/hora local e oito dígitos hex de UUID; em :1703 deriva o marcador de ida-e-volta da sessão. `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs:1590,1623` usa o marcador como texto do tooltip e deriva o corpo por sufixo fixo. O cfg, os resultados, o texto bruto do probe e a tabela histórica de AUT-4-parte03 registram esse mesmo texto. Nas 15 ocorrências em aut4probe.json, a igualdade com o campo sessão do próprio JSON foi conferida, incluindo o corpo. O marcador identifica a rodada e a releitura da UI, não autoriza acesso a serviço.
2. **INT-R1 (3).** O campo label de commands.json nomeia o ensaio m10 de propagação de exceção, suas fases baseline/RED/restaurado e o caso P15. O argv efetivamente termina em P15; exits conferidos 0/1/0. Não é argumento de autenticação. A exceção é nominal para esse ensaio/caso, não para labels arbitrários.
3. **KIT09 (15).** `tools/automacao/cenarios/kit09.py:953-956` declara o identificador do critério de ausência de aresta inventada, associado a Dependency e ao predicado de contagem zero. As demais ocorrências são consumidores/testes ou citações históricas desse identificador exato. Um literal novo no código NÃO se autoautoriza: não há leitura dinâmica de uma lista de IDs para dispensar candidatos.
4. **SHA-256 (5).** O tokenizer antigo grudava rótulo e valor numa única string. O digest de fonte restaurado foi recalculado no sandbox de KIT-10R-run663; os dois digests de artefato de KIT-14-run704 foram recalculados lendo seal.json e postprocessing-with-passive.json; o digest de DLL de jogo foi recalculado em lib/Assembly-CSharp.dll. Todos coincidiram. O quinto valor é a constante sha256Alvo usada pelo teste do debugger e encontrada na fixture local resolvida pelo alias do arcabouço. Essa fixture é local, não foi adicionada ao índice nem usada como justificativa para excluir o teste do scanner.
5. **KIT14 (12).** Os geradores locais das rodadas 702/704/710 montam a identidade a partir de run, modo fixo readonly e `datetime.now().strftime('%Y%m%d-%H%M%S')`. Fontes locais de bancada, NÃO VERSIONADAS: scratch/kit/KIT-14-run702/coleta_readonly.py, os arquivos expanded das rodadas 704/710 e a transformação de coleta_tardia.py. Foram somente lidos. As identidades documentadas são carimbos dessas coletas, não credenciais.

O harness/geradores locais e a DLL privada foram apenas lidos para esta prova. Não passam a ser arquivos públicos ou dependências do scanner/suíte. As 178 verificações locais de classificação/proveniência passaram; esse total inclui as verificações por ocorrência e não representa 178 testes unittest independentes.

## Ajuste estreito e controles de segurança

Arquivo alterado: `tools/check_padroes_segredo.py`.

- Introduz classificar_dado_publico: casamento INTEGRAL de gramáticas limitadas, nunca busca por substring. Aceita apenas os carimbos AUT4/KIT14 documentados, um critério KIT09 exato, as três fases do ensaio m10/P15 e os três rótulos de SHA-256 medidos. Hash rotulado exige exatamente 64 caracteres hex minúsculos. Datas/horas são validadas pelo calendário, não só por comprimento.
- Sufixo/prefixo opaco, nonce maior/menor, outra fase/caso, data impossível ou rótulo parecido NÃO herdam a classificação. Não existe glob de docs, whitelist de pasta ou isenção nova de arquivo.
- FORMATOS continua sendo procurado independentemente da heurística. Foi acrescentada uma guarda específica: mesmo dado público de 32+ caracteres, quando usado em campo de credencial, reprova. A guarda inclui chave JSON e os rótulos com '=' interno que a expressão antiga de atribuição não cobria por inteiro.
- LIMIAR_ENTROPIA=4.0, LIMIAR_COMPRIMENTO=32, CANDIDATO, os 13 FORMATOS e a lista anterior de ISENTOS permaneceram iguais. `tools/check_segredos.py` permaneceu byte-idêntico. A filtragem anterior de binários, hex puro e outros identificadores não foi ampliada.

A sessão AUT4 nua possui 29 caracteres e já estava fora de CANDIDATO. O teste de chave JSON cobre somente os candidatos de 32+ que realmente recebem a nova classificação no loop, e não promete corrigir o reconhecimento legado de todos os valores curtos. Os testes de atribuição textual cobrem também a sessão nua pelo formato de atribuição anterior.

## Provas executadas

| Prova local | Resultado |
|---|---|
| Scanner anterior, recomposto em memória a partir de 8b575c6, sobre a árvore atual | exit 1; 72 ocorrências herdadas |
| Scanner genérico ajustado na cópia, sobre o índice real | exit 0 |
| `python -B tools/check_segredos.py` com implementação ajustada | exit 0 |
| `python -B tools/testes/test_check_segredos.py` | exit 0; 15 testes unittest, zero falhas |
| `python -B tools/automacao/offline/testes/t_aut3_segredos.py` | exit 0; 12 verificações, zero falhas |
| Comparação integral de candidatos original/ajustado | exatamente 72 decisões diferentes, todas no inventário abaixo |
| Igualdade de FORMATOS, ISENTOS, CANDIDATO e limiares | todas satisfeitas |
| Hashes das 135 fontes .cs/.csproj da fotografia inicial | zero alterações |

A suíte nova usa repositórios Git temporários com os DOIS scanners reais. O conteúdo de docs/automacao/prova.txt é adicionado nominalmente ao índice temporário. Iscas sintéticas são montadas em partes, nunca publicadas como credenciais reais. Os **17 casos de formatos conhecidos** (cinco variantes GitHub incluídas) e o token opaco sem prefixo retornam 1 em ambos os scanners; as entradas públicas retornam 0. Também verifica segredo vizinho no mesmo arquivo, formato conhecido em binário, campo de credencial, prefixos/sufixos, datas/horas inválidas, hash rotulado com corpo não hex, máscara sem valor nem prefixo e retorno a verde depois de remover a isca.

Controles de discriminação da suíte, SOMENTE em cópias de bancada:

| Mutação deliberada | Resultado real da mesma suíte |
|---|---|
| Desativar classificação pública | exit 1; 11 falhas, 0 errors |
| Remover guarda de campo secreto | exit 1; 12 falhas, 0 errors |
| Desativar decisão de entropia | exit 1; 46 falhas, 0 errors |

Falhas contam subtests. As primeiras tentativas de desenvolvimento não foram usadas como aceite: a massa inicial de hash repetido não atingia entropia suficiente nos clones, e a sessão nua em JSON estava abaixo de 32. A massa passou a usar SHA-256 calculado de fixture sintética; o teste JSON foi delimitado aos candidatos efetivamente atingidos pela mudança. A lacuna dos rótulos com '=' em campo secreto foi corrigida pela guarda, não dispensada. Nenhum scanner/massa mutante foi instalado na árvore do dono.

## Inventário integral, sem valores

Linha começa em 1; coluna em 0, contada no texto Unicode decodificado antes do candidato. Em JSON minificado, os cinco offsets distinguem ocorrências na mesma linha. O total da tabela foi agregado por Python e conferido com 72 ocorrências/35 arquivos.

| Arquivo | Ocorrências | Classe | Linha:coluna |
|---|---:|---|---|
| docs/automacao/AUT-4-evidencias/r1-falha/resultado-r1.json | 2 | marcador-aut4 | 45:26, 242:28 |
| docs/automacao/AUT-4-evidencias/r2-incompleto/aut4probe.json | 5 | marcador-aut4 | 1:38070, 1:38262, 1:412558, 1:618582, 1:633624 |
| docs/automacao/AUT-4-evidencias/r2-incompleto/cfg-instalado.cfg | 1 | marcador-aut4 | 12:20 |
| docs/automacao/AUT-4-evidencias/r2-incompleto/lancamento.txt | 1 | sessao-aut4 | 3:0 |
| docs/automacao/AUT-4-evidencias/r2-incompleto/resultado-r2.json | 4 | marcador-aut4 | 53:26, 135:19, 139:22, 5022:28 |
| docs/automacao/AUT-4-evidencias/r3-confirmada/aut4probe.json | 5 | marcador-aut4 | 1:38070, 1:38262, 1:412555, 1:618576, 1:633614 |
| docs/automacao/AUT-4-evidencias/r3-confirmada/cfg-instalado.cfg | 1 | marcador-aut4 | 12:20 |
| docs/automacao/AUT-4-evidencias/r3-confirmada/resultado-r3.json | 4 | marcador-aut4 | 53:26, 135:19, 139:22, 4996:28 |
| docs/automacao/AUT-4-evidencias/r4-confirmada-log/aut4probe.json | 5 | marcador-aut4 | 1:38070, 1:38262, 1:412555, 1:618576, 1:633614 |
| docs/automacao/AUT-4-evidencias/r4-confirmada-log/cfg-instalado.cfg | 1 | marcador-aut4 | 12:20 |
| docs/automacao/AUT-4-evidencias/r4-confirmada-log/lancamento.txt | 1 | sessao-aut4 | 3:0 |
| docs/automacao/AUT-4-evidencias/r4-confirmada-log/resultado-r4.json | 4 | marcador-aut4 | 53:26, 135:19, 139:22, 5001:28 |
| docs/automacao/AUT-4-parte03.md | 3 | marcador-aut4 | 68:8, 69:8, 70:8 |
| docs/automacao/INT-R1-C2-I1-evidencias/commands.json | 3 | ensaio-int-r1 | 603:14, 625:14, 647:14 |
| docs/automacao/KIT-08F-entrega.md | 1 | criterio-kit09 | 97:24 |
| docs/automacao/KIT-08R-parte05.md | 1 | criterio-kit09 | 11:278 |
| docs/automacao/KIT-08R-revisao.md | 1 | criterio-kit09 | 107:229 |
| docs/automacao/KIT-09-entrega.md | 1 | criterio-kit09 | 67:2 |
| docs/automacao/KIT-09-parte02.md | 2 | criterio-kit09 | 52:11, 75:2 |
| docs/automacao/KIT-09F-parte05.md | 1 | criterio-kit09 | 17:33 |
| docs/automacao/KIT-09R-parte06.md | 1 | criterio-kit09 | 5:85 |
| docs/automacao/KIT-10R-parte06.md | 1 | sha256-rotulado | 6:29 |
| docs/automacao/KIT-14-entrega-run702.md | 1 | sessao-kit14 | 27:9 |
| docs/automacao/KIT-14-entrega-run704.md | 4 | sessao-kit14, sha256-rotulado | 15:19, 16:16, 86:18, 87:40 |
| docs/automacao/KIT-14-entrega-run710.md | 3 | sessao-kit14 | 38:20, 39:17, 40:22 |
| docs/automacao/KIT-14-parte17.md | 1 | sessao-kit14 | 6:8 |
| docs/automacao/KIT-14-parte28.md | 2 | sessao-kit14 | 8:26, 9:23 |
| docs/automacao/KIT-14-parte31.md | 1 | sha256-rotulado | 5:116 |
| docs/automacao/KIT-14-parte35.md | 1 | sessao-kit14 | 5:21 |
| docs/automacao/KIT-14-parte36.md | 1 | sessao-kit14 | 3:24 |
| docs/automacao/KIT-14-parte37.md | 1 | sessao-kit14 | 3:149 |
| tools/automacao/cenarios/kit09.py | 1 | criterio-kit09 | 953:6 |
| tools/automacao/cenarios/prova_red_kit09.py | 2 | criterio-kit09 | 103:28, 173:38 |
| tools/automacao/cenarios/test_kit09.py | 4 | criterio-kit09 | 283:6, 329:6, 531:42, 540:17 |
| tools/testes/testes/puros/t_dbg_r2_proveniencia.py | 1 | sha256-rotulado | 158:49 |

## Preservação, entrega e limites

Nenhum dos 35 arquivos de achado foi alterado. Fontes do dono foram relidas antes da edição; o scanner original foi comparado com o hash inicial antes do patch. Mudanças concorrentes de outra frente em api/README.md, tools/audita_docs.py e tools/automacao/kit15/README.md foram preservadas e NÃO pertencem ao commit de SEG. Stage/commit deve conter apenas detector, suíte e este relatório, sem git add -A/commit -a.

Evidência desta rodada: ORG-PRE-SEG-evidencias.zip, anexo do cartão, com inventário mascarado, verificações de proveniência, comparação de decisões, saídas reais dos três comandos e controles mutantes. Exclui fontes/artefatos privados lidos na triagem, dados de autenticação e raízes de bancada completas. O arquivo é evidência offline, não pacote de publicação.

Para reproduzir a trava e a suíte basta o checkout versionado, Python e Git; a rechecagem dos hashes históricos da proveniência usa a bancada local preservada. Nenhum limiar global foi relaxado. Não se afirma que a heurística detecta toda forma possível de segredo: mantiveram-se os limites/exceções legados; esta frente corrigiu exclusivamente os falsos positivos demonstrados. O scanner usa git ls-files e o conteúdo atual dos arquivos; este aceite não é varredura do histórico Git inteiro, revisão de arquivos ignorados nem autorização de publicação.

Não houve push, rewrite de histórico, deploy, build de mod, abertura/fechamento de jogo, operação de conta ou rotação. Se aparecer achado sem proveniência pública ou credencial real, bloquear para operação humana; não incluir valor em relatório. O aceite é SEG, não validação completa de CI/release nem autorização dos gates humanos. O saneamento documental e os gates posteriores permanecem com seus próprios cartões.
