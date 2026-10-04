using System;
using Burst2Flame;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// A sessao de SOMENTE LEITURA — o estado que os ganchos do <c>Patches.cs</c> consultam para nao
    /// deixar nenhuma escrita passar (<c>AcceptSkillChanges</c>, <c>RespecButton</c>,
    /// <c>ToggleAddToSkillToAddList</c>, <c>ResetSkillPoints</c>).
    ///
    /// RSTV-16 (decisao do dono, 02/10): a JANELA read-only NATIVA separada foi APOSENTADA. O que a
    /// RSTV-15 fazia aqui — carregar a janela nativa e manter a vida dela por <c>LifecycleBlock</c>/
    /// <c>GraceSeconds</c>/whitelist de <c>GUIState</c> — saiu inteiro; quem da a vida a sessao agora e
    /// o HOSPEDEIRO ATIVO da visao (<c>SkillTreesTab</c>), que hoje tem DOIS modos: (a) o SISTEMA DE
    /// ABAS do inventario (RSTV-16) — a sessao nasce quando a aba nova e selecionada e morre quando ela
    /// deixa de ser a selecionada (o <c>Tick</c> do host le o <c>MenuTabManager.SelectedMenuTab</c>); e
    /// (b) o MODO JANELA (RSTV-21) — a janela read-only PROPRIA do mod (<c>SkillTreesWindow</c>), em que
    /// a sessao vive enquanto <c>SkillTreesWindow.Aberta</c> (raiz ligada e dono em cena) e morre ao
    /// fechamento da janela, pelo botao fechar ou por o dono sair de cena (<c>Atualizar</c>). A abertura
    /// tem DOIS corpos, um por modo: (a) inventario — <c>RunButton.OpenForTarget</c>, com o gate/alvo em
    /// <c>RunTargets.GateOk</c>/<c>Resolve</c> e destino <c>SkillTreesTab.Abrir</c>; e (b) janela
    /// (RSTV-21) — <c>RemovalWindowSkillsButton.OnClick</c> -> <c>SkillTreesTab.AbrirJanela</c>, que NAO
    /// passa por <c>RunButton</c> nem por <c>RunTargets</c> (usa o alvo do proprio modal). O fechamento da
    /// arvore nativa continua com sinal pelo postfix de <c>CharacterMenusManager.CloseSkillTreeMenu</c>
    /// (Patches.cs).
    ///
    /// O que NAO existe mais aqui (aposentado pela RSTV-16, com o porque):
    ///   * <c>ZOrder</c>/<c>EnsureAbove</c>/<c>ZOrderReference</c> — o mod nao instancia mais a janela
    ///     nativa por cima da tela, entao nao ha o que reordenar (o antigo <c>AjustarZOrder</c> do
    ///     config saiu junto);
    ///   * <c>LifecycleBlock</c>/<c>GraceSeconds</c>/whitelist de <c>GUIState</c> — a vida passa a ser
    ///     a do hospedeiro ativo (o sistema de abas OU a janela propria, RSTV-21);
    ///   * a escrita de <c>GameLogic.CurrentlySelectedCharacter</c> — o menu do inventario trabalha
    ///     sobre o personagem que o JOGO ja tem selecionado; o mod nao troca mais ninguem de lugar.
    /// </summary>
    internal static class ReadOnlySession
    {
        internal static bool Active { get; private set; }

        internal static Character Target { get; private set; }

        internal static ReadOnlyContext Context { get; private set; }

        internal static void Begin(Character target, ReadOnlyContext context)
        {
            Active = true;
            Target = target;
            Context = context;
            Plugin.Log.LogInfo("RSTV-16: modo somente leitura ATIVO (contexto=" + context + ", alvo=" +
                               (target != null ? target.CharacterName : "nenhum") +
                               ") — a vida agora e a do hospedeiro ativo (a aba do inventario ou a janela propria, RSTV-21).");
        }

        internal static void End()
        {
            if (!Active)
            {
                return;
            }

            Active = false;
            Target = null;
            Plugin.Log.LogInfo("RSTV-16: modo somente leitura encerrado (nada foi gravado no personagem).");
        }

        /// <summary>
        /// Fechamento de EMERGENCIA (chamado pelos caminhos de falha dos patches): encerra a sessao e
        /// fecha a janela do menu pelo caminho NATIVO (<c>CharacterMenusManager.CloseWindow()</c>,
        /// l.49377, que desliga o menu-pai) — sem isso o painel de abas ficaria aberto e vazio.
        /// </summary>
        internal static void Close()
        {
            End();

            try
            {
                CharacterMenusManager menu = CharacterMenusManager.Instance;
                if (menu != null)
                {
                    menu.CloseWindow();
                }

                if (GUIManager.instance != null && GUIManager.instance.tooltip != null)
                {
                    GUIManager.instance.tooltip.HideTooltip();
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-16: falha ao fechar a sessao read-only: " + e.Message);
            }
        }
    }
}
