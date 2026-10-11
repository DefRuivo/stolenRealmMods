# KIT-R0 — checkpoint 02: fontes primárias e pontos para refutação

Run 623, 09/10/2026. Leituras: SUPERVISAO, PROCESSO-REVISAO, skills in-game-verification/stolen-realm-modding, KIT-G1-entrega, AUT-4-parte01/04. Política econômica/serial do cartão prevalece sobre paralelismo legado. Nenhuma ação runtime nova está sendo executada.

Inventário dirigido via Python (exit 0): evidências r1-r4 existem em docs/automacao/AUT-4-evidencias. JSON do probe de cada rodada ~634 KB: próximas extrações limitarão explicitamente subcampos, não inventário/amostra completos. R3 preserva 01-ui.png e 02-final.png; r2/r4 preservam apenas 01-ui.png. A afirmação upstream de dois PNG por rodada tem prova registrada pelo driver, mas o segundo PNG de r2/r4 não está disponível para inspeção independente.

Identidade extraída diretamente de r4/aut4probe.json: AUT4Probe 0.1.0, DLL 50176 bytes, hash runtime 407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7, assembly em scratch/aut4-runtime-iso/BepInEx/plugins/AUT4Probe/AUT4Probe.dll. Sessão AUT4-20261009-185335-54b1bed3; 24 observações, 488 TMP_Text, 7 ativos no inventário. Ida-e-volta registra marcador do driver igual a Tooltip.Title.text, mas título renderizado vazio: prova de leitura bruta, NÃO prova visual desse marcador.

R4/config: Navegar=false, DemostrarTooltip=true, HashFonte é hash da DLL, não hash literal do fonte C#. R4/driver: CONFIRMADA/exit 0. Owners vivos declarados para GUIManager.Update e OptionsManager.Localize. Arquivo bruto LogOutput-copia.log disponível para cruzamento independente.

Itens ainda a refutar:
- `aplicacao.roteiro_frame=0` enquanto `quadros_ate_a_ui=309`: investigar a correlação quadro/evento sem presumir erro de sessão.
- r3/r4 confirmam alvos de estrutura/material/geometria, NÃO têm texto como alvo. Não ampliar CONFIRMADA para renderização de todos os objetos.
- Controle r2 é lacuna real; ainda verificar controle negativo por divergência e integração dos avaliadores.
- Gate autoriza coleta somente leitura; chamada de ShowTooltip é demonstrador com escrita transitória de UI. Conferir o caveat da revisão G1 e restauração antes de aceitar seu escopo.
- Restauração, hashes perfil/save, cadeia completa e fonte/DLL ainda não reconferidos pelo revisor.

Nenhum veredito final emitido neste checkpoint.
