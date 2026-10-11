# KIT-14 — run699: retomada offline concluída com controles reais

`python scratch/kit/KIT-14-run699/test_continuar.py` — exit 0, `Ran 5 tests in 71.912s`, 0 failure/error/skip. Execução original vermelha preservada, não apagada. Builds não repetidas.

## Correção do preparo (não do produto)

O inventário tracked/untracked omitiu três documentos vivos ignorados necessários ao pacote: CHANGELOG.md, README.en.md e docs/primeiro-uso.md de KIT-15. Suplementados somente na sandbox após conferir hashes fonte/cópia; ignored-supplement.json registra cada identidade. Montar exige PACOTE_LIMPO; verificar exige OK. Nenhuma trava do produto alterada.

Os nove hashes vivos KIT-15 citados pelo run691 foram reconferidos e coincidem com aquele handoff (pacote, instalador, manifesto, scanner, descoberta, teste, contra-prova, shell e changelog). A revisão anterior não foi reiniciada.

## Resultados reais

- Pacote correto: kit-rstv 0.1.0, 42 membros/41 payload, sem DLL/PDB/EXE; testzip sem erro. SHA256 d5f42854a5f852b813f181d302bdbcc2a90498493e7d0f3da1af0a54bf606bf7. Não publicado.
- Montar e verificar reais exit0; identidades dos membros verificadas pelo CLI.
- Suíte extraída: 18 testes, 0 failure/error/skip, exit0; subprocesso sem Hermes/IA/credenciais fornecidas. Isso prova ferramentas básicas offline, não funcionamento em jogo.
- Contra-prova extraída: exit0; baseline=True e recusados=7/7, mutações reais dos próprios componentes, stdout guardado. Não é controle em jogo.
- CLIs install/status/update/remove/rollback: exit0. Os 41 hashes instalados foram lidos e comparados.
- Arquivo instalado adulterado: status real DIVERGENTE (o CLI status continua exit0; estado lido não é confundido com sucesso funcional).
- Atualizar reparou bytes da mesma versão; não é upgrade entre versões.
- Remove apagou payload, preservou sentinela alheia; rollback da remoção restituiu os 41 hashes; nova remoção deixou AUSENTE. Journals/backups retidos pelo contrato; não alegar diretório vazio.
- ZIP com membro adulterado: verificar exit1/ACHADO; original intacto exit0/OK.
- Fonte vivo 1343 arquivos e árvores pessoais 53/111/5 novamente iguais por caminho/hash; .git ausente na sandbox.

Evidência principal: offline-result-resume.json, qualification-resume.log e logs-resume/ em scratch/kit/KIT-14-run699/. Falhas iniciais em qualification.log/offline-result.json.

## Lacunas não dispensadas

Save descartável efetivamente consumido pelo jogo ainda sem isolamento comprovado. Instalação de DLL, boot, clique físico/UI/PNG, Runner ativo, métricas com/sem recorder, segundo ambiente e aprovação visual/humana continuam NAO_EXERCITADO. A decisão B dispensa tolerâncias, não essas etapas. Nenhum resultado offline será promovido a aceite ponta a ponta.
