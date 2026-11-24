using System;
using System.Collections.Generic;
using HarmonyLib;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-REM (SR-BETA-08) — a janela nativa "Remove Skill Trees" mostrava todas as arvores MENOS a
    /// do Bard, mesmo com a aba de Skills do mod listando 12 (Fire .. Chaos, Bard).
    ///
    /// POR QUE OS DOIS LADOS DIVERGIAM: a janela monta a lista por
    /// <c>RoguelikeSkillTreeRemoval.RefreshAvailableSkillTrees()</c> (chamado no <c>Open</c>), cujo
    /// predicado e' o MESMO de <c>RefreshAvailableSkillTrees</c> do manager: estar em
    /// <c>MiscSettings.SkillTabTypes</c>, nao ser Basic/Innate, passar <c>MeetsDLCRequirements</c> (que
    /// embute <c>IsDlcHidden</c>) e ter skill com <c>!Disabled &amp;&amp; !DontIncludeInTree &amp;&amp;
    /// FullReleaseModeEnabled</c>. O mod usa exatamente o mesmo criterio em <see cref="SkillTreesTab.TiposDaAba"/>,
    /// entao quando a aba lista o Bard e a janela de remocao nao, a diferenca esta no ESTADO do jogo no
    /// instante do <c>Open</c> (skills ainda nao carregadas, manager nulo, DLC mapeado depois) — e o
    /// jogador fica sem poder excluir uma arvore que o jogo tem de fato.
    ///
    /// O QUE ESTE GANCHO FAZ: depois do calculo NATIVO, reconcilia a lista com o criterio do mod,
    /// ACRESCENTANDO (nunca removendo) o que o nativo deixou de fora, e registra no log o que foi
    /// acrescentado. Duas travas de seguranca:
    ///   - lista nativa VAZIA nao e' "esquecimento", e' jogo ainda carregando: nao inventa nada;
    ///   - o mod so acrescenta tipo que ele proprio comprova visivel agora (<see cref="SkillTreesTab.TiposDaAba"/>),
    ///     nunca "todas as classes".
    /// A ordem de <c>SkillTabTypes</c> e' preservada, entao o Bard entra no fim, junto das outras.
    /// </summary>
    [HarmonyPatch(typeof(RoguelikeSkillTreeRemoval), nameof(RoguelikeSkillTreeRemoval.RefreshAvailableSkillTrees))]
    internal static class RemovalListPatch
    {
        private const string Tag = "RSTV-REM";

        [HarmonyPostfix]
        private static void Postfix()
        {
            try
            {
                // A propriedade devolve o MESMO backing list (_AvailableSkillTrees): mutar aqui muda
                // o que a janela vai popular logo em seguida.
                List<SkillType> nativa = RoguelikeSkillTreeRemoval.AvailableSkillTrees;
                if (nativa == null)
                {
                    Plugin.Log.LogInfo(Tag + ": lista nativa nula — nada a reconciliar.");
                    return;
                }

                if (nativa.Count == 0)
                {
                    // Nao e' omissao do Bard: o jogo ainda nao tem o que listar. Inventar aqui criaria
                    // uma janela de remocao com arvores que o personagem nao possui.
                    Plugin.Log.LogInfo(Tag + ": lista nativa VAZIA (jogo ainda carregando) — sem reconciliacao.");
                    return;
                }

                List<SkillType> comprovadas = SkillTreesTab.TiposDaAba();
                if (comprovadas == null || comprovadas.Count == 0)
                {
                    Plugin.Log.LogInfo(Tag + ": o mod nao comprova nenhuma arvore agora — sem reconciliacao.");
                    return;
                }

                List<SkillType> acrescentadas = new List<SkillType>();
                for (int i = 0; i < comprovadas.Count; i++)
                {
                    SkillType tipo = comprovadas[i];
                    if (!nativa.Contains(tipo))
                    {
                        nativa.Add(tipo);
                        acrescentadas.Add(tipo);
                    }
                }

                if (acrescentadas.Count == 0)
                {
                    Plugin.Log.LogInfo(Tag + ": lista de remocao ja estava completa (" + nativa.Count + " arvores: " +
                                       string.Join(", ", nativa.ConvertAll(t => t.ToString()).ToArray()) + ").");
                    return;
                }

                Plugin.Log.LogInfo(Tag + ": o jogo omitiu " + acrescentadas.Count + " arvore(s) na lista de remocao — " +
                                   "acrescentada(s): " + string.Join(", ", acrescentadas.ConvertAll(t => t.ToString()).ToArray()) +
                                   " (lista agora com " + nativa.Count + ").");
            }
            catch (Exception e)
            {
                // Gancho de lista: falhar aqui nunca pode impedir a janela nativa de abrir.
                Plugin.Log.LogWarning(Tag + ": reconciliacao falhou (" + e.GetType().Name + ": " + e.Message + ") — lista nativa intacta.");
            }
        }
    }
}
