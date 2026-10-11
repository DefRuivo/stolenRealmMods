# KIT-06R — parecer independente: REPROVADO

Cartão t_f9f88c18, reviewer run638, sessão 20261009_214531_11695d, perfil default. Implementer t_66ff87b5 run633, sessão 20261009_212534_a88c76: instâncias distintas. Data local verificada no início: 09/10/2026, 21:45:44 UTC-03. Branch ci-validate-test. Revisão offline do estado vivo, não autoaprovação nem aceite de UI/mod/publicação.

## 1. Identidade e método

Sandbox própria scratch/kit/KIT-06R-run638/sandbox: 188 arquivos vivos do escopo tools/automacao/lib/props/entrega, tracked/untracked preservados; sem .git, credenciais, caches ou perfil do dono. Cópias conferidas por SHA256 antes de testar. Nove hashes da entrega conferiram; metadados completos em identidade-inicial.json e hashes-entrega.json. Comparação posterior dos mesmos 188 arquivos vivos registrou DRIFT []. Fontes sandbox mutados só para controles negativos e restaurados byte a byte.

Identidades principais:
- tools/automacao/runtime/controle_acesso.py: 2e21f5396628f6141ea3fd66d5e60f815b95c0dfb0ac4a83c37157ee7c787e2f
- tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs: 6bfe3db1e50c18e441d266fca00bfba82c527680837a1a22d148455c5db6bbbf
- tools/automacao/kit06/teste_controle_acesso.py: e3a310679acb3e67d238c938a85b46af0a80b46f163f96289ad6b0c5d56a6186
- tools/automacao/kit06/contra_prova_kit06.py: 0374fdfe9fe000aff607f8088defcb24a7b5954af3d9961e4c879bc4e084db0d
- docs/automacao/KIT-06-entrega.md: a9cdca3b97e2bc7278bb6ffaaf597aba015f1dc0bb48be2c1954404105a3b8c3

Lidas regras docs/SUPERVISAO.md e docs/PROCESSO-REVISAO.md. Não editados fontes vivos, mods, DLL proprietária, gameplay/Bard, política/modelos/crons. Sem git add/commit/push, instalação ou publicação; nenhum jogo/save/foco/encerramento acionado.

## 2. Veredito por critério de aceite

| Critério | Parecer | Prova e limite |
|---|---|---|
| Identidade/autoria/preservação | OK / PASSOU | 9 hashes da entrega iguais; 188 hashes vivos sem drift no checkpoint; reviewer638 !=633 |
| Atalhos configuráveis | ACHADO / FALHOU F1/F2 | Config vazia/recusada reativa bindings Python; retomar aceito sem efeito; F7 não segue liga/desliga documentado |
| Indicador de coleta | ACHADO / FALHOU F3 | Parado com evento registrado; sem pipeline diz observando, reproduzido Python/C# |
| Contexto e marcação manual | OK nominal; ACHADO F6 | Contexto/descrição/pausa/teto nominal passam; snapshot C# permite adulteração externa de evidência |
| Guards chat/digitação/remapeamento/sem-foco | OK / PASSOU offline | Oráculo próprio mede ação ausente e estado não habilitado; guard removido faz teste próprio reprovar |
| Ausência de conflito com input | OK estrutural parcial; INDETERMINADO real | Recusa de duplicatas/reservadas nominal passa; configuração F1 insegura; consumo real/conflito com remapeamento do jogo não exercitados |
| Iniciar observação nunca autoriza modo ativo | OK / PASSOU offline | Todas ações ativas recusadas + habilitar_modo_ativo falha; defeito real modo=ativo detectado pelo oráculo próprio |
| Sem foco forçado | OK offline; NAO_EXERCITADO efeito em jogo | Guard bloqueia sem foco e código não chama API de foco; pixels/foco do engine não medidos |
| Sem encerrar sessão do dono | OK offline; NAO_EXERCITADO runtime | Parar pausa pipeline, não encerra jogo; inspeção sem API de lifecycle e execução nominal |
| Export acessível sem Hermes/IA | OK escrita nominal; ACHADO F4/F5 | Arquivo local real existe, mas perde evidência e IO propaga exceção |
| Integração contrato KIT-07 quando disponível | ACHADO / FALHOU F8 | API existe e consumo manual funciona; botão não integra, descritor obsoleto; KIT-07R reprovado, exigir gate antes de uso |
| Fluxo completo offline e prova negativa | ACHADO / FALHOU F2/F3/F4/F7 | 35 testes nominais passam mas próprios refutam contrato/efeito; harness negativo mascara falhas extras |
| UI/UX real, controles sem terminal em jogo | NAO_EXERCITADO | Gate KIT-G2 não autorizado; PonteControleRSTV não é chamada pelo SRAdapterPlugin.Update; não há overlay/input engine entregue |
| Runtime/pixels/interferência/desempenho | NAO_EXERCITADO | Nenhuma rodada de jogo autorizada nesta revisão |

## 3. Achados e reproduções concretas

### F1 — configuração inválida/vazia reativa padrões (Python)

tools/automacao/runtime/controle_acesso.py:169 e :600–601 usam o vazio normalizado como falsy. Esperado: vazio explícito desabilita bindings; config recusada nunca habilita binding não aprovado. Observado: {} vira F7/F8/F9/F10; observar=Return recusado produz mapa {}, mas F7 inicia observação. Testes próprios test_config_vazia_nao_reativa_defaults e test_config_totalmente_rejeitada_nao_reativa_defaults: FAIL por AssertionError, não ERROR. C# preserva mapa vazio (controle positivo).

### F2 — contratos de ações inconsistentes

controle_acesso.py:10/:283–309 e PonteControleRSTV.cs:250–281. Retomar é conhecido e validado, porém falta despacho: F6 configurado para retomar não gera evento, pipeline continua pausado. Segundo F7 continua observando apesar da documentação liga/desliga (o padrão nem oferece parar). Suite do autor afirma que segundo F7 deve degradar: isso confirma inconsistência do contrato, não corrige uso. Oráculos Python e C# reprovam. Corrigir comportamento/documentação/configuração de forma consistente; não ocultar o histórico do desacordo.

### F3 — indicador sem correspondência com efeito de coleta

controle_acesso.py:178–188/:299–309/:441–463; PonteControleRSTV.cs:99–113/:271–281/:410–433. Esperado: parado não coleta; pipeline ausente não conta como funcional. Observado: pipeline existente registra clique quadro1 enquanto indicador=parado; sem pipeline F7 indica observando. Reproduzido nos dois caminhos. Ownership/opt-in deve ser explícito, sem booleano que simule efeito ou autorização ativa.

### F4 — export descarta as evidências que anuncia

controle_acesso.py:420–438; PonteControleRSTV.cs:362–381. Evento real retido e pedido de captura são criados, mas export só guarda contagem no indicador: id do evento não existe no JSON. Guard_chat também desaparece da exportação apesar de registrado no controle. Não exporta eventos/dados/capturas/falhas/trilha/degradações/correlação. Reproduzido pela leitura posterior de arquivo real Python e documento serializado C#. Não afirmar fluxo completo a partir de contador.

### F5 — IO sem falha-segura

controle_acesso.py:398–418; PonteControleRSTV.cs:384–406. Configurar pasta de export como arquivo-sentinela e pressionar F10 propaga FileExistsError (Python) / IOException (C#). Testes capturam exceção e reprovam por asserção, não falha de setup. Sentinela C# permanece intacta. Capturar falha, comunicar indisponibilidade/erro sem evento falso de sucesso nem escrita em conteúdo alheio.

### F6 — consumidor pode alterar evidência C# interna

PonteControleRSTV.cs:378 e :474–476. Marcacoes() retorna lista nova com mesmos dicionários. Alterar descricao no snapshot externo muda marcação interna e export subsequente. Harness próprio: observado=alterada fora da ponte, FAIL. Não é ataque a gameplay: é integridade do resultado entregue. Devolver snapshots defensivos coerentes.

### F7 — falso verde do controle negativo C#

tools/automacao/runtime/harness-controle/Program.cs:38–41 e :63–76. Nomes de defeito arbitrários aceitos; sob --defeito qualquer falha vale sucesso. Defeito real plantado no fonte sandbox ConsomeInput false->true:
- normal: 43 OK/1 FALHA, exit1;
- --defeito guard: 40 OK/4 FALHA (3 esperadas +1 extra), exit0 VERDE;
- --defeito inventado: 43 OK/1 FALHA não relacionada, exit0 VERDE.
Assim falha estranha ao alvo fica escondida. Exigir conjunto exato e nomes suportados; ausência/ERROR/skip/timeout não verdes. Fonte restaurado e recompilado: 44 OK/0 FALHA exit0.

### F8 — descritor obsoleto e integração KIT-07 ausente

controle_acesso.py:398–438/:519–541; exportador KIT-07 vivo tools/automacao/kit07/exportador.py:188. Contrato afirma NAO_IMPLEMENTADO, mas API montar_pacote existe. Export KIT-06 real com e-mail sintético conserva conteúdo bruto; consumo manual por KIT-07 gera um arquivo sem e-mail bruto. Isto prova somente possibilidade nominal, não sanitização universal nem integração do botão. Arquivo bruto/local não é pacote compartilhável seguro. Handoff vivo de KIT-07R t_96d0c463 está REPROVADO; correção KIT-07F t_a7318a33 já existe. Integrar opcionalmente só quando gate satisfizer, ou declarar indisponibilidade/gate honestamente. Não integrar automaticamente exportador reprovado nem duplicar infraestrutura.

## 4. Execuções próprias, comandos e exits

Prefixos de caminhos/logs abaixo relativos a scratch/kit/KIT-06R-run638. Suite e harness usam cópia viva, não dados fabricados de runtime.

| Comando | Resultado real | Evidência |
|---|---|---|
| python prepara_revisao.py | 188 cópias verificadas, 9 hashes iguais, exit0 | identidade-inicial.json; hashes-entrega.json |
| dotnet msbuild preflight.proj -t:Build (true/default/false) | exit0 cada; sentinela true/false/false | preflight-negativo/default/explicito.log |
| python sandbox/tools/automacao/kit06/teste_controle_acesso.py | Ran35 tests OK exit0 | suite.log |
| python sandbox/tools/automacao/kit06/contra_prova_kit06.py | 13 iscas/0 falhas exit0; testes mutados exit1 | contra.log; sandbox/scratch/kit/KIT-06/contra-prova/isca-*.log |
| python .../contra_prova_kit06.py --autoteste | 9/9 exit0 | autoteste.log |
| python test_revisao_kit06.py | Ran14 tests;10 FAIL/4 OK;exit1;zeroERROR/skip | reviewer-suite.log/json |
| dotnet run --project harness-reviewer/Review.csproj -p:DeployToBepInEx=false | 12 verificações;8 FAIL/4 OK;exit1 | reviewer-csharp.log |
| dotnet run --project sandbox/.../harness-controle -p:DeployToBepInEx=false | 44 OK/0 FALHA exit0 | harness.log; harness-restaurado.log |
| harness original --defeito guard / ataque | 41/3 e42/2, exit0 cada | harness-autor-guard/ataque.log |
| harness fonte mutado normal / guard / inventado | exits1/0/0; falsa aceitação de extras | harness-defeito-real-input/falso-verde-guard/defeito-desconhecido.log |
| dotnet build sandbox/.../KIT04Adapter.SR.csproj -c Release -p:DeployToBepInEx=false | exit0;0 erros;1 aviso MSB3277 | build.log e build-raw.stdout/stderr |
| python exercita_adversarios.py | 4 negativos próprios exatos, cada Ran1/FAIL1/ERROR0/skip0;driver exit0 | cp-revisor-*.log; contra-prova-revisor.json |
| bash scratch/kit/KIT-06R-run638/sandbox/tools/automacao/kit06/roda_testes_kit06.sh (terminal real) | 35 OK +13 iscas +9/9;VERDE exit0 | output real terminal; parte06 |
| PYTHON=C:/nao/existe/python.exe bash mesmo runner | erro interpretador;exit2 | output real terminal; parte06 |
| export real KIT-06 + montar_pacote real KIT-07 | leitura bruta/email=True;pacote/email=False;1 arquivo | integracao-kit07.json; export-local/ocorrencia.json; pacote-kit07/ocorrencia.json |

DLLs da build sandbox (não instaladas nem distribuídas): Adapter ffe8108296e47661d0daf7f0fc430b3e41d069669fc7353992dd52acd97bcf45; Core b6c0a01a3dba88543439634d10fd0f3abd9a3ef7196f43170bf80ea3a9d50482.

## 5. Limitações e desvios preservados

- Um dos 10 FAIL próprios exige limpar janela com None; API usa None para manter contexto e aceita string vazia. Sem contrato explícito isso é INDETERMINADO, NÃO contado nos oito achados. Logs não foram apagados para parecer mais fortes.
- 13 mutações do autor mostram 18/35 testes distintos reprovando. Outros17 ainda não têm prova negativa individual (cobertura-negativa.json). Os quatro oráculos próprios positivos foram cada um mostrado reprovando com defeito real. Não alegar que todos35 têm prova negativa.
- Build primeira coleta text=True falhou UnicodeDecodeError console nativo; abordagem bytes conservou output e revelou build exit0. Tentativa runner por subprocess bash deu exit2; tentativa terminal agregada foi bloqueada pelo parser exit-1; shell real simples passou. Histórico em partes03/05/06.
- Ambiente real TEMP/TMP/TMPDIR apontava Temp do sistema, não scratch indicado no contexto. Harness original escreveu export sintético Temp/harness-controle-kit06/kit06-harness-0.json (770 bytes), fora do workspace. Testes do autor usam tempfile default. Não instalaram mod nem tocaram save, mas impede afirmar nenhuma escrita externa. Ambiente ajustado explicitamente para scratch/kit/KIT-06R-run638/tmp após detectar; não apagado arquivo preexistente fora do workspace.
- Sem medição before/after do perfil do dono nesta revisão: não fazer alegação de hash de perfil inalterado; segurança de build provada por sandbox/preflight/props e ausência de alvo deploy no escopo.
- UI real/engine input, runtime/pixels/foco/interferência/desempenho NAO_EXERCITADO (KIT-G2). SRAdapterPlugin.cs:64–119 não usa PonteControleRSTV. Tipo compilado não equivale a controle acessível em jogo.
- Não reexecutadas suíte AUT-4 inteira, auditorias de publicação de mods ou testes de runtime. Esta entrega já é reprovada por provas locais; não há alegação de regressão global verde.

## 6. Encaminhamento nativo e gate

Correção criada e lida de volta: KIT-06F t_73f0779f, assignee default (único perfil real), nova instância != reviewer638, depende desta revisão. Handoff exige correções F1–F8, negativos úteis, entrega incremental/hash e kanban_request_review para revisão independente no mesmo cartão (não criar revisão duplicada).
Gate escrito e lido de volta: t_73f0779f -> t_10584ca5 KIT-15. KIT-15 lista t_73f0779f entre pais insatisfeitos. Portanto concluir este parecer não libera pacote defeituoso; revisão concluída NÃO é aprovação do KIT-06/DoD.

Veredito final: REPROVADO. Próximo passo concreto: nova instância implementadora corrigir KIT-06F e devolver para reconferência independente, mantendo histórico e gates humanos. O reviewer638 não fez as correções de produto.
