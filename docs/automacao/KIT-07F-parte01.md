# KIT-07F — correção dos achados F1–F9 (parte 01: abertura)

## Identidade e escopo

- Cartão: t_a7318a33 (KIT-07F), perfil default, run640 — instância de correção NOVA, distinta do
  implementador original (t_c364710f run634) e do revisor (t_96d0c463 run636).
- Dependência: parecer KIT-07R t_96d0c463 (REPROVADO, F1–F9). Filhos que aguardam: KIT-08 t_e2107a63,
  KIT-15 t_10584ca5.
- Workspace: C:/dev/stolen-realm, branch ci-validate-test.
- Modo: correção offline de ferramenta (Python stdlib). NENHUM jogo, save real, mod, Bard,
  Assembly-CSharp.dll, build, deploy ou publicação. Nenhuma instalação/abertura/navegação.
  Gate humano inalterado; este cartão não é tarefa de mod/DoD.

## Fontes de prova lidas (não reescritas)

- docs/automacao/KIT-07R-revisao.md (parecer final) e partes 01–07.
- tools/automacao/kit07/exportador.py (sha256 c5fc715b…f382, versão reprovada).
- tools/automacao/kit07/teste_exportador_kit07.py (suite autor, 14 testes).
- tools/automacao/kit07/contra_prova_kit07.py (12 mutações + controle falso-verde).
- tools/automacao/offline/aut3_lib.py (04f37b8e…dc1a).
- scratch/kit/KIT-07R-run636/test_review_kit07.py (suite independente, 24 testes / 15 FAIL).
- scratch/kit/KIT-07R-run636/isolated/ (cópia do módulo reprovado, hash idêntico ao auditado) —
  usada como linha de base para reproduzir o RED sem tocar nos artefatos da revisão.

## Base de trabalho desta correção

- Run dir próprio: scratch/kit/KIT-07F-run640/ (nunca sobrescreve run636).
- Linha de base RED: replicada executando a suite independente contra a cópia isolada reprovada
  (hash c5fc715b…), conforme parte02.

## Mapa achado → correção planejada (F1–F9)

| Achado | Correção planejada |
|---|---|
| F1 nomes/metadata vazam | Mapeamento de caminho por segmento: prefixos fortes sem depender de `\b`, minimização pessoal, nome seguro ao FS, tratamento de colisão; manifesto/relatório/excluídos/png_para_revisao saneados; comentário do manifest alinhado ao código |
| F2 JSON escapado/chave puntuada | Redação estrutural de JSON no exportador (parse → redigir valores sob chave de credencial e prefixos em qualquer valor → re-serializar válido); fallback regex para não-JSON; aut3_lib intacta (sem regressão nas bancadas AUT-3) |
| F3 origem == destino / sobreposição | Recusa por caminhos canônicos (realpath) de igualdade e de qualquer aninhamento antes de criar/gravar |
| F4 resíduos na reexportação | Montagem em diretório temporário e troca só no sucesso: pacote final == manifesto + política vigente, sem restos |
| F5 nomes reservados sobrescritos | Nomes reservados (manifest.json/relatorio.md/.kit07-pacote) e colisões renomeados de forma determinística e registrados no manifesto; hash reflete o disco final |
| F6 marcador inválido apaga alheio | Validação de identidade/conteúdo/proveniência/escopo (marcador JSON kit=KIT-07 + manifesto + nenhum arquivo extra/não listado/link) antes de limpar |
| F7 tetos contam entrada | Tetos em bytes REAIS de saída (sanitizada) + overhead explícito + verificação do tamanho final; montagem em temp com rollback (sem parciais) |
| F8 I/O bruto vaza prefixo | Validação proativa de destino + captura/saneamento de OSError/FX na CLI; exit 0/1/2 (domínio/infra); nada de traceback nem prefixo |
| F9 log BepInEx descartado | Classificação por tipo de arquivo: texto em segmento `bepinex` entra; assemblies/saves/binários seguem excluídos |

## Invariantes desta correção

- aut3_lib NÃO é alterada (evita regressão nas bancadas AUT-3); a correção estrutural de JSON fica no
  exportador, mantendo a trava do aut3_lib como 2ª linha para texto não-JSON.
- Infraestrutura existente reusada: suite autor, contra-prova (12 mutações + falso-verde) e a suite
  independente de 24 testes. Contudo, as âncoras de mutação que apontam para trechos refatorados serão
  atualizadas preservando o MESMO defeito e o mesmo conjunto exato de FAIL (registrado em parte própria).
- Preservado o histórico da revisão; nenhum artefato de run636 é modificado.
