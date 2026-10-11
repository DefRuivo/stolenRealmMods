using System;
using Gumatos.RealmApi;
using UnityEngine;

namespace Gumatos.RealmApi.UI
{
    /// <summary>
    /// Abas de menu do jogo. MUTA UI: exige vinculo com `allowMutation:true`. O estado da aba fica nesta API;
    /// a reconstrucao do visual e do hospedeiro nativo (`MenuTabManager.RefreshSelected`), sempre depois de
    /// o alvo ter sido resolvido com assinatura exata no assembly do jogo.
    /// </summary>
    public static class MenuUI
    {
        /// <summary>Registra uma aba. `onOpen` recebe o GameObject nativo da aba quando o jogo a construir.</summary>
        public static void AddTab(string tabName, Action<GameObject> onOpen, Action? onClose = null)
        {
            UiOperations.MenuAdd(tabName, onOpen, onClose);
        }

        /// <summary>Remove uma aba registrada por esta API.</summary>
        public static void RemoveTab(string tabName)
        {
            UiOperations.MenuRemove(tabName);
        }
    }
}
