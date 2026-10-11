using Gumatos.RealmApi;
using Gumatos.RealmApi.Skills;

namespace Gumatos.RealmApi.UI
{
    /// <summary>
    /// Abas da arvore de habilidades. MUTA UI: `AddTab`/`RemoveTab` exigem vinculo com `allowMutation:true`
    /// e provam que a arvore nativa esta carregada e ativa (`SkillTreeManager.IsNotNullAndIsActive`) antes de
    /// pedir a reconstrucao (`SkillTreeManager.UpdateSkillTreeItems`). `HasTab` e consulta pura do registro
    /// desta API: nao muta, portanto nao exige opt-in de mutacao (mas ainda exige vinculo e thread).
    /// </summary>
    public static class SkillTreeUI
    {
        /// <summary>Registra uma aba de arvore de habilidade.</summary>
        public static void AddTab(string tabName, SkillTree skillTree)
        {
            UiOperations.SkillTreeAdd(tabName, skillTree);
        }

        /// <summary>Remove uma aba registrada por esta API.</summary>
        public static void RemoveTab(SkillTree skillTree)
        {
            UiOperations.SkillTreeRemove(skillTree);
        }

        /// <summary>Existe aba registrada por esta API para a arvore?</summary>
        public static bool HasTab(SkillTree skillTree)
        {
            return UiOperations.SkillTreeHas(skillTree);
        }
    }
}
