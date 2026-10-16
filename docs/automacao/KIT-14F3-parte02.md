# KIT-14F3 — baseline e hipótese refinada

Inventário antes de alteração: scratch/kit/KIT-14F3-run1502/baseline.json, 1866 arquivos tracked/untracked, SHA256 6257359881bdd47af51dfe40e6691ae73143ee2c88dcd5f2e9c0b0fe1c4dfd83. Sandbox contém apenas cópia de Core/Adapter sem bin/obj; fontes principais não editadas.

Preflight real 12:57 -03: nenhum processo do jogo, Cloud por app=0 lido do sharedconfig, sem junction, backup KIT16 ou lock. Não equivale a inspeção do servidor Steam. Assembly histórico de Adapter decompilado com ilspycmd exit0 para original-adapter-decompiled.cs; comparação detalhada seguirá antes de corrigir.

Segunda deficiência concreta em fonte: SRScreenManager monitora nomes genéricos InventoryPanel/SkillsPanel/etc., mas a janela real do RSTV se chama RstvSkillTreesWindow (SkillTreesWindow.cs:47). Mesmo um Update vivo não observaria essa janela. Correção deve cobrir lifecycle E resolver a janela real, sem editar o produto.

Plano de implementação: motor PlayerLoop opt-in (Core+Adapter+passivo), único e independente do MonoBehaviour destruído; medição explícita de callbacks/frame/estado do plugin e eventos oriundos de GameObject real. A ponte existente e PipelinePassivo permanecem responsáveis pelos limites; eventos receberão procedência real de engine, não rótulo runtime inventado. OFF/ausente não instalam motor. Captura real e persistência correlacionadas serão limitadas ao pipeline. Não alterar probe congelado.
