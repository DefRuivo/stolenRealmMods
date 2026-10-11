using System;
using Gumatos.RealmApi;
using UnityEngine;

namespace Gumatos.RealmApi.UI
{
    /// <summary>
    /// Aba/botao da barra de acao do personagem atual. MUTA UI: exige vinculo com `allowMutation:true`.
    /// O estado do botao fica nesta API; a barra nativa do jogo e quem reconstroi o visual
    /// (`Skillbar.RefreshSkillBar`), sempre depois de provar que ha slot disponivel
    /// (`Skillbar.HasAvailableSlot`). Sem hospedeiro, sem vinculo ou sem slot: falha fechado.
    /// </summary>
    public static class ActionBarUI
    {
        /// <summary>Registra um botao na barra de acao. Exige slot livre no hospedeiro nativo.</summary>
        public static void AddButton(string name, Sprite icon, Action onClick)
        {
            UiOperations.ActionBarAdd(name, icon, onClick);
        }

        /// <summary>Remove um botao registrado por esta API.</summary>
        public static void RemoveButton(string name)
        {
            UiOperations.ActionBarRemove(name);
        }

        /// <summary>Troca o icone de um botao registrado por esta API.</summary>
        public static void UpdateIcon(string name, Sprite newIcon)
        {
            UiOperations.ActionBarUpdateIcon(name, newIcon);
        }
    }
}
