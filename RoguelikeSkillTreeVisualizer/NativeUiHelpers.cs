using System;
using UnityEngine;
using UnityEngine.UI;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// Utilidades GENERICAS de UI nativa, compartilhadas pelos botoes 'Skills' que existem (o do
    /// modal "Remove Skill Trees", o do HUD da run e o da janela do level-up) e pela aba
    /// "All Skill Trees".
    ///
    /// HISTORICO: estes estaticos nasceram dentro de <c>SelectPartyButton</c> — o botao da tela
    /// Select Party, a primeira superficie do mod (RSTV-2/RSTV-3). Em 06/10 o dono decidiu REMOVER
    /// aquela superficie (RSTV-29) e o arquivo/classe batizado com ela virou mentira: o que sobrou
    /// aqui nao e' da tela de party, e' o kit de clonagem de botao nativo que os OUTROS botoes reusam
    /// (limpeza de listeners, desligamento de localizadores, diagnostico do grupo de layout).
    ///
    /// RSTV-30 (06/10): a RECEITA DE LAYOUT saiu daqui. Ela existia para o clone do HUD dividir a
    /// linha do `Ping Button` (encolher o original e empurrar o clone para o lado) — e o dono pediu
    /// justamente o contrario: o botao foi para a barra de baixo, onde ele NAO pode encolher nem
    /// empurrar botao nativo nenhum. Os membros `SquareSide`, `ApplySquareLayout`, `WorldWidth`,
    /// `RowWidth`, `ShrinkKeepingLeftEdge`, `PlaceToTheRight`, `FindRowGroup` e `EnsureLayoutElement`
    /// ficaram sem chamador e foram apagados (medido antes de apagar: o unico chamador era o
    /// `RunButton`, que agora mede e coloca por conta propria — ver `RunButton.ColocarNaLinha`).
    /// </summary>
    internal static class NativeUiHelpers
    {
        // ---------------------------------------------------------------------------------------
        // Diagnostico de layout
        // ---------------------------------------------------------------------------------------

        /// <summary>Nome do componente de layout do container (para o log: e' o que decide se um filho
        /// novo reflui a linha ou nao). Devolve "nenhum" quando o container nao tem LayoutGroup.</summary>
        internal static string DescribeGroup(Transform parent)
        {
            if (parent == null)
            {
                return "nenhum";
            }

            LayoutGroup group = parent.GetComponent<LayoutGroup>();
            return group == null ? "nenhum" : group.GetType().Name;
        }

        // ---------------------------------------------------------------------------------------
        // Clonagem
        // ---------------------------------------------------------------------------------------

        internal static void DisableLocalizers(GameObject root)
        {
            Component[] components = root.GetComponentsInChildren<Component>(true);
            for (int i = 0; i < components.Length; i++)
            {
                Component component = components[i];
                if (component == null)
                {
                    continue;
                }

                string typeName = component.GetType().Name;
                if (typeName.IndexOf("Localiz", StringComparison.OrdinalIgnoreCase) >= 0 ||
                    typeName.IndexOf("Localize", StringComparison.OrdinalIgnoreCase) >= 0)
                {
                    Behaviour behaviour = component as Behaviour;
                    if (behaviour != null)
                    {
                        behaviour.enabled = false;
                        Plugin.Log.LogInfo("RSTV: localizador '" + typeName + "' desativado no botao clonado.");
                    }
                }
            }
        }

        /// <summary>
        /// RSTV-12: limpa TODOS os listeners de clique do botao — inclusive os PERSISTENTES
        /// (serializados no prefab) que o `RemoveAllListeners()` NAO remove.
        ///
        /// POR QUE `RemoveAllListeners()` NAO BASTA (lido do `UnityEngine.CoreModule.dll` DESTE build,
        /// `UnityEngine.Events.InvokableCallList`/`UnityEventBase`):
        ///  - o `UnityEvent` guarda DUAS listas: `m_PersistentCalls` (os listeners gravados no prefab
        ///    — o `ButtonPressedPing` do Ping Button, o `ButtonPressedSkillTree` do `Skills Tree Btn`
        ///    (o molde da RSTV-30) e o `ConfirmLevelUpSelection` do AcceptButton) e `m_RuntimeCalls`
        ///    (os de script, como o nosso);
        ///  - `UnityEventBase.RemoveAllListeners()` chama apenas `m_Calls.Clear()`, e esse `Clear()`
        ///    esvazia SO a `m_RuntimeCalls` — a lista persistente continua na instancia;
        ///  - pior: `InvokableCallList.PrepareInvoke()` concatena as PERSISTENTES **antes** das de
        ///    runtime. O listener do jogo roda PRIMEIRO e, se ele lancar (o `ConfirmLevelUpSelection`
        ///    estoura `NullReferenceException` num clone), o `UnityEvent.Invoke()` ABORTA a varredura e
        ///    o NOSSO listener nem chega a rodar — foi exatamente o stack do log de 02/10.
        ///
        /// Trocar a INSTANCIA do evento (`new Button.ButtonClickedEvent()`) descarta junto a lista
        /// persistente serializada (a instancia nova nasce sem nenhuma) — e e a partir dela que o
        /// listener do mod e instalado. `Button.onClick` tem setter publico (IL deste build).
        /// </summary>
        internal static void ClearClickListeners(Button button)
        {
            if (button == null)
            {
                return;
            }

            button.onClick = new Button.ButtonClickedEvent();
        }
    }
}
