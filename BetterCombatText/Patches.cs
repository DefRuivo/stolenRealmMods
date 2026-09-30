using System;
using HarmonyLib;
using TMPro;
using UnityEngine;

namespace BetterCombatText
{
    // =====================================================================================
    //  Alvos de patch — TODOS por TIPO explicito de metodo + __instance (o proprio objeto).
    //  NUNCA se usa parametro posicional (ref __0/__1/__3): no projeto isso ja derrubou o jogo
    //  com 112 NullReferenceException porque um indice apontava para o argumento errado.
    //  Cada postfix roda DEPOIS do jogo escrever o texto daquele componente, que e o momento
    //  certo para estilizar o material DAQUELE componente.
    // =====================================================================================

    // -------------------------------------------------------------------------------------
    //  1) NOME DO INIMIGO EM COMBATE — barra de vida de chefe/champion
    //     Decompilado l.26088 BossHealthbar / l.26109:  BossName.text = value.LocalizedCharacterName;
    //     BossName e TextMeshProUGUI (l.26090). Chamado por GUIManager.AssignBossHealthBars
    //     (l.118627: BossHealthbars[num].BossCharacter = enemy).
    // -------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(BossHealthbar), "set_BossCharacter")]
    internal static class PatchNomeDoChefe
    {
        private static void Postfix(BossHealthbar __instance)
        {
            if (!Plugin.Ativo)
            {
                return;
            }
            try
            {
                TextStyler.AplicarTmp(__instance.BossName, Plugin.Cfg.Nomes, "Nomes (combate)");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: nome do chefe falhou: {e.GetType().Name}: {e.Message}");
            }
        }
    }

    // -------------------------------------------------------------------------------------
    //  2) NOME DO INIMIGO + ICONES DE BUFF/DEBUFF EM COMBATE — janela de hover do personagem
    //     Decompilado l.151735 PlayerInfoWindow / l.151808:  playerName.text = ...LocalizedCharacterName;
    //     playerName e TextMeshProUGUI (l.151739) e statusIcons e StatusIcon[] (l.151747).
    //     E o caminho real de "passar o mouse no inimigo em combate" (l.121524: o setter de
    //     CurrentlyHoveringHexCell chama playerInfoWindow.ShowPlayerInfoWindow(player) para
    //     QUALQUER personagem do hex, inclusive inimigo — ShouldShowPlayerInfoWindow aceita
    //     TeamIndex != 0, l.151776).
    // -------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(PlayerInfoWindow), "ShowPlayerInfoWindow")]
    internal static class PatchHoverEmCombate
    {
        private static void Postfix(PlayerInfoWindow __instance)
        {
            if (!Plugin.Ativo)
            {
                return;
            }
            try
            {
                TextStyler.AplicarTmp(__instance.playerName, Plugin.Cfg.Nomes, "Nomes (combate)");
                AplicarStatusIcons(__instance.statusIcons);
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: hover de combate falhou: {e.GetType().Name}: {e.Message}");
            }
        }

        internal static void AplicarStatusIcons(StatusIcon[] icones)
        {
            if (icones == null)
            {
                return;
            }
            for (int i = 0; i < icones.Length; i++)
            {
                PatchRotulosDeStatus.Aplicar(icones[i]);
            }
        }
    }

    // -------------------------------------------------------------------------------------
    //  3) ROTULOS/STACKS DE BUFF E DEBUFF — "xN" e contador de turnos dos icones de status
    //     Decompilado l.174756 StatusIcon / l.174762 public Text turnCount; l.174764 public Text stackCount;
    //     escritos em UpdateStatusIcon (l.174813 -> l.174830-836) e em GUIManager.UpdateStatusIcons
    //     (l.119228 -> l.119273-274). ATENCAO: sao UnityEngine.UI.Text LEGADO (confirmado no IL:
    //     `using UnityEngine.UI; public Text stackCount;`), nao TextMeshPro — ver o comentario em
    //     TextStyler.AplicarTextoLegado. UpdateStatusIcon e privado, mas e um TIPO de metodo
    //     explicito: patchavel por nome, com __instance.
    // -------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(StatusIcon), "UpdateStatusIcon", new Type[0])]
    internal static class PatchRotulosDeStatus
    {
        private static void Postfix(StatusIcon __instance)
        {
            Aplicar(__instance);
        }

        internal static void Aplicar(StatusIcon icone)
        {
            if (!Plugin.Ativo || icone == null)
            {
                return;
            }
            try
            {
                var cfg = Plugin.Cfg.Rotulos;
                TextStyler.AplicarTextoLegado(icone.stackCount, cfg, "Rotulos (combate)");
                TextStyler.AplicarTextoLegado(icone.turnCount, cfg, "Rotulos (combate)");
                TextStyler.ReportarResumoRotulos();
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: rotulo de status falhou: {e.GetType().Name}: {e.Message}");
            }
        }
    }

    // -------------------------------------------------------------------------------------
    //  4) TEXTO DO DADO NOS EVENTOS — o NUMERO na face do dado
    //     Decompilado l.95521 DiceRollingManager.RollDice (l.95629):
    //         public TextMeshPro RollDice(int index, int rollValue) { ... obj.ResetDiceText();
    //         obj.PlayDiceAnimation(num, ...); return obj.GetResultText(num); }
    //     Devolve o TextMeshPro da face com o numero sorteado (l.95702 GetResultText filtra
    //     DiceNumbers por texto == resultado). DiceVisualSetup.DiceNumbers (l.95686) e TextMeshPro[]
    //     -> texto 3D renderizado para a RenderTexture mostrada na janela de evento. E TMP: a mesma
    //     tecnica do combate se aplica.
    // -------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(DiceRollingManager), "RollDice", new[] { typeof(int), typeof(int) })]
    internal static class PatchDadoNaFace
    {
        private static void Postfix(DiceRollingManager __instance, TextMeshPro __result)
        {
            if (!Plugin.Ativo || !Plugin.Cfg.EventosAtivar.Value)
            {
                return;
            }
            try
            {
                TextStyler.AplicarTmp(__result, Plugin.Cfg.EventosDado, "Eventos (texto do dado)");
                var setups = __instance.DiceSetups;
                if (setups != null)
                {
                    for (int i = 0; i < setups.Length; i++)
                    {
                        var faces = setups[i] != null ? setups[i].DiceNumbers : null;
                        if (faces == null)
                        {
                            continue;
                        }
                        for (int j = 0; j < faces.Length; j++)
                        {
                            TextStyler.AplicarTmp(faces[j], Plugin.Cfg.EventosDado, "Eventos (texto do dado)");
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: texto do dado falhou: {e.GetType().Name}: {e.Message}");
            }
        }
    }

    // -------------------------------------------------------------------------------------
    //  5) TEXTO DO DADO NOS EVENTOS — a linha de resultado da rolagem
    //     Decompilado l.95278 DiceRoller: TargetText / ResultText / ModifierValueText, todos
    //     TextMeshProUGUI (l.95280-284). StartRollVisuals (l.95334) e o inicio de toda rolagem
    //     (a coroutine ExecuteRoll escreve neles logo depois, l.95432-436).
    // -------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(DiceRoller), "StartRollVisuals")]
    internal static class PatchResultadoDoDado
    {
        private static void Postfix(DiceRoller __instance)
        {
            if (!Plugin.Ativo || !Plugin.Cfg.EventosAtivar.Value)
            {
                return;
            }
            try
            {
                TextStyler.AplicarTmp(__instance.TargetText, Plugin.Cfg.EventosDado, "Eventos (texto do dado)");
                TextStyler.AplicarTmp(__instance.ResultText, Plugin.Cfg.EventosDado, "Eventos (texto do dado)");
                TextStyler.AplicarTmp(__instance.ModifierValueText, Plugin.Cfg.EventosDado, "Eventos (texto do dado)");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: resultado do dado falhou: {e.GetType().Name}: {e.Message}");
            }
        }
    }

    // -------------------------------------------------------------------------------------
    //  7) OPCIONAL (default DESLIGADO) — NOME DO BUFF/DEBUFF
    //     Nao existe rotulo proprio com o nome do buff em combate: o nome so aparece no tooltip
    //     de hover. Decompilado l.212957/212965 Tooltip.Title / Tooltip.Description
    //     (TextMeshProUGUI), preenchidos em Tooltip.ShowActionStatusTooltip (l.213903), que chama
    //     ShowTooltip(OptionsManager.Localize(actionStatusInfo.Name), ...) em l.213952.
    //     POR QUE FICA DESLIGADO: Title/Description sao os MESMOS componentes dos tooltips de
    //     skill/item/powerup — instanciar o material deles faz o halo valer para o sistema de
    //     tooltip inteiro. Fica na mao do dono ligar (secao '6.' do .cfg).
    // -------------------------------------------------------------------------------------
    //  ATENCAO: este metodo tem DUAS sobrecargas no DLL (l.213903 com 10 parametros e l.213930
    //  ShowActionStatusTooltip(StatusIcon)); patch por nome sozinho estoura AmbiguousMatchException
    //  e derruba o PatchAll inteiro. Por isso a assinatura e declarada EXPLICITAMENTE aqui.
    // -------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(Tooltip), "ShowActionStatusTooltip", new[] { typeof(StatusIcon) })]
    internal static class PatchTooltipDeStatus
    {
        private static void Postfix(Tooltip __instance)
        {
            if (!Plugin.Ativo || !Plugin.Cfg.TooltipAtivar.Value)
            {
                return;
            }
            try
            {
                TextStyler.AplicarTmp(__instance.Title, Plugin.Cfg.TooltipStatus, "Tooltip de status");
                TextStyler.AplicarTmp(__instance.Description, Plugin.Cfg.TooltipStatus, "Tooltip de status");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: tooltip de status falhou: {e.GetType().Name}: {e.Message}");
            }
        }
    }

    // -------------------------------------------------------------------------------------
    //  6) OPCIONAL (default DESLIGADO) — numero de vida sobre as unidades
    //     Decompilado l.210345 Healthbar.healthbarText (TextMeshProUGUI), escrito a cada frame
    //     em Healthbar.Update (l.210527-529). Fora do pedido original; fica atras de config.
    // -------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(Healthbar), "Update", new Type[0])]
    internal static class PatchNumeroDeVida
    {
        private static void Postfix(Healthbar __instance)
        {
            if (!Plugin.Ativo || !Plugin.Cfg.AplicarNumeroDeVida.Value)
            {
                return;
            }
            try
            {
                TextStyler.AplicarTmp(__instance.healthbarText, Plugin.Cfg.NumeroDeVida, "Numero de vida (extra)");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: numero de vida falhou: {e.GetType().Name}: {e.Message}");
            }
        }
    }
}
