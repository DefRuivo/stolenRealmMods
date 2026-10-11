using System;
using System.Collections.Generic;
using Gumatos.RealmApi.Skills;

namespace Gumatos.RealmApi
{
    /// <summary>
    /// Logica da familia UI, sem UnityEngine: resolução de alvo, estado proprio (registro de abas/botoes),
    /// provas de disponibilidade no hospedeiro nativo e delegacao por reflexao. A parte visual do Unity vive
    /// nos tipos publicos de `Gumatos.RealmApi.UI` (RealmApi.dll) — aqui fica o que e exercitavel no CLR.
    /// </summary>
    internal static class UiOperations
    {
        internal sealed class ActionBarEntry
        {
            internal readonly object? Icon;
            internal readonly Action? OnClick;
            internal ActionBarEntry(object? icon, Action? onClick) { Icon = icon; OnClick = onClick; }
        }

        internal sealed class MenuEntry
        {
            internal readonly object? Builder;
            internal readonly Action? OnClick;
            internal MenuEntry(object? builder, Action? onClick) { Builder = builder; OnClick = onClick; }
        }

        internal sealed class TooltipRequest
        {
            internal readonly string Title;
            internal readonly string Subtitle;
            internal readonly object? Icon;
            internal TooltipRequest(string title, string subtitle, object? icon) { Title = title; Subtitle = subtitle; Icon = icon; }
        }

        private static readonly Dictionary<string, ActionBarEntry> actionBarButtons = new Dictionary<string, ActionBarEntry>(StringComparer.Ordinal);
        private static readonly Dictionary<SkillTree, string> skillTreeTabs = new Dictionary<SkillTree, string>();
        private static readonly Dictionary<string, MenuEntry> menuTabs = new Dictionary<string, MenuEntry>(StringComparer.Ordinal);
        private static TooltipRequest? tooltipRequest;

        internal static int ActionBarCount => actionBarButtons.Count;
        internal static int SkillTreeTabCount => skillTreeTabs.Count;
        internal static int MenuTabCount => menuTabs.Count;
        internal static TooltipRequest? TooltipRequested => tooltipRequest;
        internal static bool ActionBarHas(string id) => actionBarButtons.ContainsKey(id);
        internal static bool MenuHas(string id) => menuTabs.ContainsKey(id);

        /// <summary>Zera o estado proprio das cinco familias (chamado a cada Bind/Unbind: nada sobrevive a um vinculo).</summary>
        internal static void Reset()
        {
            actionBarButtons.Clear();
            skillTreeTabs.Clear();
            menuTabs.Clear();
            tooltipRequest = null;
        }

        // ---------------------------------------------------------------- UIFactory
        /// <summary>Hospedeiro da arvore de UI do jogo; ausente = familia indisponivel.</summary>
        internal static object FactoryHost()
        {
            UiFamily.Require(UiRequirements.FamilyFactory, false);
            return UiFamily.Host("ui.factory.host");
        }

        // ---------------------------------------------------------------- ActionBarUI
        private static object ActiveSkillbar()
        {
            var current = UiFamily.Host("ui.action-bar.host");
            var bar = UiFamily.Read("ui.action-bar.skillbar", current);
            if (bar == null) throw new InvalidOperationException("Barra de acao indisponivel: CurrentCharacterUI.ActiveSkillbar devolveu null");
            return bar;
        }

        internal static object ActionBarAdd(string id, object? icon, Action? onClick)
        {
            UiFamily.Require(UiRequirements.FamilyActionBar, true);
            if (string.IsNullOrWhiteSpace(id)) throw new ArgumentException("Id do botao vazio", nameof(id));
            if (actionBarButtons.ContainsKey(id)) throw new ArgumentException("Botao ja registrado: " + id, nameof(id));
            var bar = ActiveSkillbar();
            if (!(UiFamily.Read("ui.action-bar.probe", bar) is bool available) || !available)
                throw new InvalidOperationException("Sem slot disponivel na barra de acao: Skillbar.HasAvailableSlot() = false");
            actionBarButtons.Add(id, new ActionBarEntry(icon, onClick));
            UiFamily.Read("ui.action-bar.refresh", bar);
            return bar;
        }

        internal static object ActionBarRemove(string id)
        {
            UiFamily.Require(UiRequirements.FamilyActionBar, true);
            if (string.IsNullOrWhiteSpace(id)) throw new ArgumentException("Id do botao vazio", nameof(id));
            var bar = ActiveSkillbar();
            if (!actionBarButtons.Remove(id)) throw new InvalidOperationException("Botao nao registrado: " + id);
            UiFamily.Read("ui.action-bar.refresh", bar);
            return bar;
        }

        internal static object ActionBarUpdateIcon(string id, object? icon)
        {
            UiFamily.Require(UiRequirements.FamilyActionBar, true);
            if (string.IsNullOrWhiteSpace(id)) throw new ArgumentException("Id do botao vazio", nameof(id));
            var bar = ActiveSkillbar();
            if (!actionBarButtons.TryGetValue(id, out var entry)) throw new InvalidOperationException("Botao nao registrado: " + id);
            actionBarButtons[id] = new ActionBarEntry(icon, entry.OnClick);
            UiFamily.Read("ui.action-bar.refresh", bar);
            return bar;
        }

        // ---------------------------------------------------------------- SkillTreeUI
        internal static object SkillTreeAdd(string name, SkillTree tree)
        {
            UiFamily.Require(UiRequirements.FamilySkillTree, true);
            if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Nome da aba vazio", nameof(name));
            if (!Enum.IsDefined(typeof(SkillTree), tree)) throw new ArgumentOutOfRangeException(nameof(tree), tree, "Arvore fora do contrato");
            if (skillTreeTabs.ContainsKey(tree)) throw new ArgumentException("Aba ja registrada: " + tree, nameof(tree));
            var manager = UiFamily.Host("ui.skill-tree.host");
            if (!(UiFamily.Static("ui.skill-tree.probe") is bool active) || !active)
                throw new InvalidOperationException("Arvore de habilidades indisponivel: SkillTreeManager.IsNotNullAndIsActive = false");
            skillTreeTabs.Add(tree, name);
            UiFamily.Read("ui.skill-tree.refresh", manager);
            return manager;
        }

        internal static object SkillTreeRemove(SkillTree tree)
        {
            UiFamily.Require(UiRequirements.FamilySkillTree, true);
            if (!Enum.IsDefined(typeof(SkillTree), tree)) throw new ArgumentOutOfRangeException(nameof(tree), tree, "Arvore fora do contrato");
            var manager = UiFamily.Host("ui.skill-tree.host");
            if (!skillTreeTabs.Remove(tree)) throw new InvalidOperationException("Aba nao registrada: " + tree);
            UiFamily.Read("ui.skill-tree.refresh", manager);
            return manager;
        }

        /// <summary>Consulta pura do registro: nao muta UI, portanto nao exige opt-in de mutacao.</summary>
        internal static bool SkillTreeHas(SkillTree tree)
        {
            UiFamily.Require(UiRequirements.FamilySkillTree, false);
            if (!Enum.IsDefined(typeof(SkillTree), tree)) throw new ArgumentOutOfRangeException(nameof(tree), tree, "Arvore fora do contrato");
            return skillTreeTabs.ContainsKey(tree);
        }

        // ---------------------------------------------------------------- MenuUI
        internal static object MenuAdd(string name, object? builder, Action? onClick)
        {
            UiFamily.Require(UiRequirements.FamilyMenu, true);
            if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Nome da aba vazio", nameof(name));
            if (menuTabs.ContainsKey(name)) throw new ArgumentException("Aba ja registrada: " + name, nameof(name));
            var manager = UiFamily.Host("ui.menu.host");
            menuTabs.Add(name, new MenuEntry(builder, onClick));
            UiFamily.Read("ui.menu.instance", manager);
            return manager;
        }

        internal static object MenuRemove(string name)
        {
            UiFamily.Require(UiRequirements.FamilyMenu, true);
            if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Nome da aba vazio", nameof(name));
            var manager = UiFamily.Host("ui.menu.host");
            if (!menuTabs.Remove(name)) throw new InvalidOperationException("Aba nao registrada: " + name);
            UiFamily.Read("ui.menu.instance", manager);
            return manager;
        }

        // ---------------------------------------------------------------- TooltipHelper
        internal static object TooltipHost()
        {
            var manager = UiFamily.Host("ui.tooltip.host");
            var tooltip = UiFamily.Read("ui.tooltip.link", manager);
            if (tooltip == null) throw new InvalidOperationException("Tooltip nativo indisponivel: GUIManager.tooltip e null");
            return tooltip;
        }

        internal static object TooltipShow(string title, string subtitle, object? icon)
        {
            UiFamily.Require(UiRequirements.FamilyTooltip, true);
            if (string.IsNullOrWhiteSpace(title)) throw new ArgumentException("Titulo vazio", nameof(title));
            var tooltip = TooltipHost();
            tooltipRequest = new TooltipRequest(title, subtitle ?? string.Empty, icon);
            return tooltip;
        }

        internal static object TooltipHide()
        {
            UiFamily.Require(UiRequirements.FamilyTooltip, true);
            var tooltip = TooltipHost();
            UiFamily.Read("ui.tooltip.hide", tooltip);
            tooltipRequest = null;
            return tooltip;
        }
    }
}
