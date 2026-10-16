# KIT-14F4 — parte 02 — baseline e alvo real

Sandbox criada em scratch/kit/KIT-14F4-run1525/sandbox, copiando os cinco fontes congelados do F2 e csproj do principal. Baseline e hashes dos fontes principais em baseline-source.json/principal-before.json. Nenhum fonte principal alterado.

Decompilação da DLL efetivamente ensaiada RSTV SHA256 1d0b85e8d0f30d10c4fe7c4e044d30380537e8801a7d39875192459a2e51d5cc: RunButton.OpenForTarget resolve RunTargets.Resolve e passa Character explícito a SkillTreesTab.Abrir; All Trees hospeda RstvAllSkillTreesPanel; IniciarSessaoReadOnly consome alvo explícito e ReadOnlySession.Begin. No roteiro de party única, RunTargets.Resolve usa CurrentlySelectedCharacter quando presente e local. Snapshot pré-abertura pode capturar essa referência independentemente e confrontá-la com ReadOnlySession.Target depois do handler. Não será preenchido observado copiando esperado.

Hover real usa RstvSkillHover.OnPointerEnter -> Tooltip.ShowSkillTooltip(Item.SkillInfo, Target, showCanLevelDetail:false); handler de saída esconde tooltip. Fechamento nativo CharacterMenusManager.CloseWindow fecha o host. Nenhum clique físico é inferido. Fireball (Fire T2) é o alvo explícito previsto na configuração do instrumento; GUID será lido do objeto vivo, não inventado.

Falha histórica confirmada na saída run1524: coleta no próprio frame do handler, somente rótulo da aba, snapshots nulos, sete capacidades não exercitadas. Correção em desenvolvimento: fase opt-in delimitada de espera por frame/estado, coleta descendente do painel e tooltip, ciclo completo e prova de owners ligada a objeto/assembly/método vivo. Sem mudanças no avaliador/filtro ou no produtor aprovado.
