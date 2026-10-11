using Gumatos.RealmApi;
using UnityEngine;

namespace Gumatos.RealmApi.UI
{
    /// <summary>
    /// Tooltip nativo do jogo. MUTA UI: exige vinculo com `allowMutation:true`.
    /// `HideTooltip` delega 1:1 ao membro nativo verificado (`Tooltip.HideTooltip`).
    /// `ShowTooltip` resolve o tooltip nativo (`GUIManager.tooltip`), guarda o pedido e torna o tooltip visivel;
    /// o preenchimento nativo completo (`Tooltip.ShowTooltip`, 13 parametros do jogo) fica declarado como
    /// NAO_EXERCITADO nesta entrega — ver api/README.md.
    /// </summary>
    public static class TooltipHelper
    {
        /// <summary>Pede a exibicao do tooltip nativo com titulo, descricao e (opcional) icone.</summary>
        public static void ShowTooltip(string title, string description, Sprite? icon = null)
        {
            var host = UiOperations.TooltipShow(title, description, icon);
            if (host is not Component component)
                throw new System.InvalidOperationException("Hospedeiro do tooltip nao e um Component do Unity");
            component.gameObject.SetActive(true);
        }

        /// <summary>Esconde o tooltip nativo (delegacao 1:1 a `Tooltip.HideTooltip`).</summary>
        public static void HideTooltip()
        {
            UiOperations.TooltipHide();
        }
    }
}
