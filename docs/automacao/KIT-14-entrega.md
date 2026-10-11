# KIT-14 — entrega parcial: preflight documental e bloqueio humano

Cartão t_a1f38855. Implementador default/run698. Data medida: 10/10/2026, 12:37:12 -0300. Esta entrega NÃO qualifica o kit ponta a ponta e NÃO fecha o cartão.

## Resultado
PENDENTE_DECISAO_HUMANA: falta resolver os limites de performance antes da rodada. A autorização específica de sessão isolada existe no KIT-G2; não se pede novo consentimento genérico. O aceite de impacto FPS/tempo de quadro/memória/disco não possui limiar acordado registrado nas fontes consultadas.

O corpo do KIT-G2 exige pre-registro dos limites antes da rodada. A entrega do gate mantém explicitamente LACUNA e solicita definição antes do KIT-14. A aprovação independente do gate não substitui essa decisão do dono. Não foi inferido que a lacuna permite dispensar o requisito.

## Verificações realmente executadas
- Inventário git e dos artefatos KIT-14: terminal exit 0; alterações preexistentes preservadas, não atribuídas a esta execução.
- Reconferência no quadro: pais satisfeitos; KIT-G2 done com autorização isolada B1–B6; KIT-14R t_9ce7d260 todo e dependente deste cartão.
- Leitura de SUPERVISAO.md e PROCESSO-REVISAO.md, KIT-G2-entrega.md e KIT-G2-parte03.md; skills in-game-verification e stolen-realm-modding.
- Busca dirigida dos docs KIT por limites de performance: sem acordo numérico identificado; não equivale a busca universal de todas as fontes.
- Comandos registrados em scratch/kit/KIT-14-run698/preflight-leitura.json: date, git rev-parse HEAD, git branch --show-current, git diff --cached --name-only, todos exit 0; índice vazio, HEAD d82894ebe95d97f26b7989a848372c691dcb8ef6, branch ci-validate-test.
- Reconferidos em disco os hashes do probe, coletor, avaliadores e DLL de referência do jogo: iguais aos congelados KIT-G2. Isso prova identidade em disco, NÃO DLL carregada nem funcionamento em jogo.
- O JSON de evidência foi relido e confrontado integralmente após gravação. Terminal agregador exit 0. Não é preflight de deploy; build permanece proibido nesta execução sem esse preflight específico.

## Cobertura por requisito
| Requisito | Estado desta rodada | Evidência ou lacuna |
|---|---|---|
| Autorizações e dependências | PASSOU na reconferência documental | Gate B1–B6, pais satisfeitos; performance pendente separadamente |
| Build identificada e hash do pacote | NAO_EXERCITADO | Não construído nem instalado pacote |
| DLL carregada confrontada | NAO_EXERCITADO | Somente hash dos arquivos em disco |
| Clique físico → janela → conteúdo/tooltip → PNG | NAO_EXERCITADO | Nenhuma sessão ativa iniciada |
| Relatório → marcar problema → exportar | NAO_EXERCITADO | Nenhuma prova funcional nova |
| Runner RSTV e erro detectado/controle negativo em jogo | NAO_EXERCITADO | Nenhum cenário ativo; fixture não usada como runtime |
| Mod sem kit; básico sem Hermes/IA/credenciais | NAO_EXERCITADO | Sem boot/comparação funcional |
| Install/update/remove/rollback | NAO_EXERCITADO | Nenhuma instalação realizada |
| Saves de produção intactos por comparação antes/depois | NAO_EXERCITADO | Não acessados; ausência de ação não é snapshot comparativo |
| FPS/tempo de quadro/memória/disco com/sem recorder | NAO_EXERCITADO | Limiares humanos ausentes; nenhuma métrica inventada |
| Segundo ambiente/portabilidade | INDETERMINADO | Disponibilidade e funcionamento não verificados |
| Revisão técnica/visual e aceite final | NAO_EXERCITADO | Revisão KIT-14R não liberada, humano/publicação separados |

Cenários pre-registrados pelo KIT-G2: RSTV-6-readonly-personagem, RSTV-6-readonly-skills-pontos, RSTV-21-janela-ciclo, RSTV-21-tooltip-restauracao, RSTV-26-placeholders, RSTV-25b-dependencia, RSTV-geometria-clipping, tooltips_shrines e C0–C7 AUT-4: todos NAO_EXERCITADO nesta execução. Nenhuma simulação contada como prova de jogo.

## Decisão exata para desbloquear
Definir tolerâncias de queda de FPS / aumento de tempo de quadro (média e p95), memória adicional e bytes escritos em disco por rodada, com unidades, base de comparação e janela aplicável. Alternativa: o dono pode dispensar explicitamente limiares prévios e autorizar coleta exploratória, sem PASSOU/aceite de performance. Esta alternativa não foi autorizada nem escolhida pelo worker.

## Retomada, sem repetir trabalho pronto
1. Ler este relatório, checkpoints e evidência, e a decisão registrada no cartão.
2. Revalidar jogo pessoal fechado/frente única, congelamento e isolamento do ambiente pessoal.
3. Executar o preflight real de deploy antes de qualquer build; usar sandbox isolada preservando fontes tracked/untracked, redirecionamento de ambiente e DeployToBepInEx=false.
4. Executar somente B1–B6 autorizados, em perfil/save descartável, com rollback garantido e verificado; medir os critérios reais, incluindo clique físico separado do handler.
5. Registrar lacunas/cobertura por cenário e encaminhar à revisão independente já prevista quando a execução estiver concluída. Não criar revisão duplicada nem concluir para liberar dependentes enquanto o aceite do cartão não for coberto.

## Artefatos e SHA-256 medidos
- docs/automacao/KIT-14-parte01.md: 74df45b9756c4d1bea1e61cc07b45bd7ff65237c61aa0d989c5a51dd95652a0f.
- docs/automacao/KIT-14-parte02.md: 58e0fa5066a4b8b4b0783a7ccb949e6c2603f3b04af2bdb49fdd25ff03e11fff.
- scratch/kit/KIT-14-run698/preflight-leitura.json: 751ca98dc263f3a24f2a705931871bb8b8b6ce3ce2792f68b32240adbd785615.
- KIT-G2-entrega.md: 072bdf46d211c4e11e07245f8ce92bf1e3c924f56529da4b44219790e0cf7ff8.
- KIT-G2-parte03.md: 6f203071509c272ef9a37ac46bb6bd6c1394d45957a567a010702c8b0b86f6a5.
- AUT4Probe.dll: 72928ffa4a84d79dd9a8fadce9f78bd438d1f991a0c100afb30f7bf7da561a5c.
- coletor.py: 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d.
- rstv.py: f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7.
- tooltips_shrines.py: 65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199.
- lib/Assembly-CSharp.dll: 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a; somente leitura, não redistribuída.

Nenhum build, teste funcional, deploy, jogo, perfil/save, publicação, git add/commit/push, configuração/modelo/cron/prioridade ou produto modificado. Apenas os artefatos novos desta frente. Travas gerais não reexecutadas: não contadas como verdes nesta rodada.
