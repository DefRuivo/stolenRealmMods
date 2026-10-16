# KIT-14F3 — oito casos finais executados

Final/cases contém campanhas distintas mutant/on/off/absent-flags/core-off/adapter-off/passive-off/adapter-absent, todas encerradas sem erro de driver/rollback (serão agregadas programaticamente, não por contagem mental). Mutante medidor1 esperado; ON0; demais seis medidor0 em modo de controle negativo. Core-OFF foi adicionado explicitamente para provar que Adapter+passivo ON não bastam. Sem alterar medidor para os resultados.

Nenhum controle precisou fechar sessão alheia: cada boot exigiu jogo fechado e lock livre antes de isolar. Dados, perfil, PlayerPrefs, Cloud config e ausência de junction/backup/perfil são conferidos no result.json e nos itens do medidor por caso. Ainda falta agregação de hashes/configs/estado final e entrega das fontes/DLL/patch para revisão, não há aceite automático.

Escopo offline: harness-passivo existente compila pipeline e ponte por link, mas não demonstra engine; harness-kit14f monta BaseUnityPlugin sem engine e não cobre o novo PlayerLoop. Runtime acima é a prova primária, não substituível por esses ensaios. Nenhuma suíte global de mods foi anunciada rodada.
