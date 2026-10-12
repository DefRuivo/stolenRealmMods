# ORG-AUT5-DIAG — parte 02: congelamento, hashes e handoff

Continuação da investigação `t_ceceef6b`, offline em 11/10/2026. As causas e reproduções estão em `docs/automacao/ORG-AUT5-DIAG-parte01.md`. Este documento não autoriza restaurar runtime, abrir jogo ou reconstruir instrumento.

## 1. Confronto com o handoff KIT14G-SEG2-P

Foi lido o cartão `t_c36c7082`, incluindo implementação (run 840) e revisão aprovada (run 842). O handoff registra o par restaurado e preflight sem runtime. A fonte de referência documental atual é `docs/automacao/KIT-14G-SEG2-receita-congelada.md:7–8`, não o par antigo descrito na receita histórica.

Confronto MEDIDO diretamente nesta tarefa:

| Artefato | SHA-256 antes e depois | Bytes |
|---|---|---:|
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193` | 109397 |
| `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` | `7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee` | 77824 |

Ambos coincidem com a receita e com o handoff. O fonte também coincide com o da cópia ORG-R1 e com seu hash arquivado. As chaves CliqueFisico, CliqueFisicoEstavel e SilencioAposClique estão presentes em `AUT4ProbePlugin.cs:173–187`; não foram tocadas. Nem o fonte nem a DLL tiveram escrita, rebuild ou deploy nesta investigação.

A receita `:38` conserva uma nota histórica sobre o PROBE_SHA anterior do sandbox; o handoff posterior diz que o atualizou. Essa nota NÃO foi usada como hash atual e NÃO foi reescrita. Não se executou preflight da bancada nem se tomou o sucesso anterior como validação runtime atual. A prova deste cartão é apenas dos bytes no repo e da compatibilidade dos testes estáticos com a estrutura lida.

A conclusão da revisão KIT14G-SEG2-P sobre congelamento não equivale a exigir que testes antigos procurem private. O par atual contém Leitura/Tipo internal e captura por PassoLeitura. O diagnóstico propõe ajustar a ferramenta que confronta o instrumento, nunca o instrumento congelado para satisfazer ferramenta defasada.

## 2. Hashes físicos da evidência investigada

Os seis itens abaixo são byte-idênticos entre repo principal, cópia ORG-R1 e os hashes físicos de `source-hashes.json` dentro do zip original. Isso separa deriva já presente na baseline de alteração causada por esta investigação.

| Arquivo | SHA-256 físico |
|---|---|
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193` |
| `tools/automacao/aut5/test_aut5.py` | `b624c5785ff5d44e9071317d14c4c7aa5f674287e3492fa189add8f614192062` |
| `tools/automacao/aut5/test_snapshot_modal.py` | `054aecb14eb53700d3f0aa28d9b51e221c82e4f93a972d5a36f15bafcb4c3e96` |
| `tools/automacao/aut5/aut5.py` | `02e76929f1aa7c931863d6149902125d91132fdd0fd064fbc0d533480eb89c7b` |
| `tools/automacao/aut5/fixtures/log-completo.log` | `574f8f7b9fd4bbbd119ea78d17017153e17a5aff4b06694f0fc1fd85ea633094` |
| `RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj` | `5d8bb0c12835e5d6f9c5fa64d924cd4407b52149eb984983232025c174e345cb` |

Cuidado de comparação: aut5.py tem 963 terminações CRLF, e o csproj tem 124. Seus blobs Git usam LF. O SHA-256 de aut5.py apenas normalizado EM MEMÓRIA para LF é `08e2860f1e9ff6eb48d594871de61696a22679484bbcd64931e10f38c375fee4`; o do csproj é `47ca611fdc998a9cef90a46f3923e994e00022fb555a0ee8a10a46d829f21eb6`. Esses valores coincidem com os blobs `097f950`. Não se normalizou nenhum arquivo físico para conseguir identidade; hash físico e hash de blob não devem ser confundidos.

O script de diagnóstico conferiu 1632 arquivos tracked existentes antes da investigação: zero bytes alterados durante os testes. Conferiu também os três inputs lidos do perfil (log, DLL RSTV, config): igualdade antes/depois. O fonte congelado e a DLL foram reconferidos especificamente. Os únicos arquivos novos no repo desta entrega são as partes 01 e 02 deste relatório; scripts, provas e cópias privadas ficam no workspace.

## 3. O que foi e não foi demonstrado

DEMONSTRADO offline:

1. A fixture 0.3.2 não satisfaz a premissa do positivo em fonte 0.3.3. Ajuste local exclusivo da string de versão muda REPROVADO para INDETERMINADO, sem inventar identidade da DLL nem fechar runtime.
2. Leitura e Tipo existem como internal. Todos os sete campos observacionais existem no corpo real, e os quatro campos finais são atualizados. O coletor os preserva.
3. O harness original para antes de compilar por assinatura de Tipo; sua premissa adicional de chamada inline em Passo também não corresponde à estrutura atual.
4. A expressão de viewport da suíte contém string constante truthy e não verifica o dado que sua mensagem diz verificar.
5. A DLL RSTV do perfil existe e difere tanto da baseline reconstruída anteriormente quanto da DLL principal. Log-real é integração dependente do ambiente, incluída incondicionalmente na suíte.
6. O par fonte/DLL AUT4Probe coincide com KIT14G-SEG2-P e permaneceu intacto.

NAO_EXERCITADO:

- suíte AUT5 completa e contra-prova completas nesta investigação;
- compilação/execução C# do harness (proibidas neste escopo);
- emissão/leitura dos campos em sessão viva, correlação temporal de snapshot/tooltip, pixels/viewport reais;
- build/reprodutibilidade/equivalência funcional das três DLLs RSTV;
- preflight/boot atuais da bancada SEG2, restauração de runtime, save ou autorização de rodada;
- CI remoto, aceite visual, decisão de publicação.

Não é válido transformar o êxito do script diagnóstico em PASSOU da suíte ou em aprovação do instrumento/runtime. Os estados originais divergentes foram preservados.

## 4. Follow-up especializado criado, sem execução neste cartão

Cartão `t_2d9f22b1`: ORG-AUT5-FIX — corrigir deriva do contrato de testes AUT5 sem alterar AUT4Probe congelado. Perfil default (único perfil listado por `hermes profile list` nesta máquina), modelo `gpt-6.1-sol`, provider `openai-codex`. Depende desta investigação; não altera os gates da organização.

Decisões de contrato carregadas no corpo do filho:

- separar teste offline hermético de integração log-real opt-in; integração ausente não pode virar PASSOU por omissão;
- manter a regra do avaliador: versão divergente REPROVADO; bytes não identificados INDETERMINADO; ausente/null nunca OK;
- corrigir o reconhecimento da visibilidade e da cadeia de chamada real, preservando os corpos do instrumento;
- verificar o dado aninhado por ligação Leitura → Geometria, com controles negativos em material de teste;
- preservar o par congelado, receitas, fontes do produto, perfil e evidências históricas;
- não executar build, inclusive dotnet run indireto do harness, deploy ou jogo; se compilação adicional for indispensável, registrar NAO_EXERCITADO e pedir autorização em cartão próprio, nunca inferir permissão;
- produzir provas RED-GREEN de cada defeito sem aprovação sintética de runtime. Não declarar suíte/harness completo verde sem execução real permitida.

Não foi criado cartão para alterar produto, refazer congelamento ou reinstalar DLLs. A divergência de identidade não autoriza deploy corretivo. As mudanças de parser/testes ficam para o especialista do filho, após revisão deste relatório.

## 5. Artefatos e reprodução

Workspace da tarefa: `C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_ceceef6b`. Nessa localização estão `investigate_aut5.py`, `diagnostic-evidence.json`, `ORG-R1-baseline-test-aut5-copia.txt`, os quatro relatórios de leitura e a matriz de fixtures OFFLINE. Esses arquivos são NOVOS; nenhum output do pai foi sobrescrito.

`investigate_aut5.py` recusa sobrescrever sua evidência ou cópia. Para reproduzir em outro diretório autorizado, copiar o script para workspace vazio, conservar disponíveis as entradas registradas e executar `python -B investigate_aut5.py`. O script compara o par congelado antes de agir e bloqueia subprocessos após a preparação de leitura. Ele não é remediação nem procedimento de runtime.

O pacote de evidência da entrega não inclui a DLL congelada, a DLL do mod, DLLs do jogo nem cópia integral do perfil/log real. Os hashes e resultados bastam ao handoff. O cartão segue para revisão do artefato; não há filho de revisão precriado que exija fechar este pai antecipadamente.
