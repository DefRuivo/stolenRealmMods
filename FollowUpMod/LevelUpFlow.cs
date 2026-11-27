using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

namespace FollowUpMod
{
    /// <summary>
    /// Ordem por ETAPA, nao por nivel. O fluxo nativo percorre `LevelUpSequenceOrder` DENTRO de
    /// cada entrada de `CharactersWaitingForLevelUp` (RoguelikeManager.cs:403-433), entao uma
    /// promocao de 17 niveis mostrava skills>itens>atributos 17 vezes. Aqui a fila e ROTACIONADA:
    /// ao confirmar, a entrada volta para o fim com a etapa seguinte, de modo que todos os
    /// personagens/entradas esgotam Skills, depois todos esgotam Items, e por fim um UNICO bloco
    /// de atributos encerra a fila.
    /// </summary>
    internal static class LevelUpFlow
    {
        private enum Fase
        {
            Skills,
            Items,
            Attributes
        }

        private sealed class Estado
        {
            internal Fase Fase = Fase.Skills;
        }

        private static readonly ConditionalWeakTable<CharacterLevelUpInfo, Estado> Estados =
            new ConditionalWeakTable<CharacterLevelUpInfo, Estado>();

        /// <summary>Devolve true quando tratou a confirmacao (o chamador pula o metodo nativo).</summary>
        internal static bool Handle(RoguelikeManager manager)
        {
            if (manager == null) return false;
            var fila = manager.CharactersWaitingForLevelUp;
            if (fila == null || fila.Count == 0) return false;

            var info = fila[0];
            if (info == null || info.Character == null) return false;

            // Reroll usa a mesma fila e deve continuar no caminho nativo (uma etapa so).
            if (info.IsReroll) return false;

            try
            {
                var estado = Estados.GetOrCreateValue(info);
                Diag.Write("nivel: confirmar fase=" + estado.Fase + " personagem=" + info.Character.CharacterName
                    + " fila=" + fila.Count);

                switch (estado.Fase)
                {
                    case Fase.Skills:
                        if (manager.SelectedSkillOption != null)
                            info.Character.AddSkill(manager.SelectedSkillOption.SkillInfo);
                        estado.Fase = Fase.Items;
                        Rotacionar(fila, info);
                        Reabrir(manager, fila);
                        return true;

                    case Fase.Items:
                        if (manager.SelectedItemSlot != null)
                            GameLogic.instance.GiveItem(manager.SelectedItemSlot.Item, info.Character);
                        estado.Fase = Fase.Attributes;
                        Rotacionar(fila, info);
                        Reabrir(manager, fila);
                        return true;

                    default:
                        // Bloco unico de atributos: encerra todas as entradas deste personagem.
                        int removidas = 0;
                        for (int i = fila.Count - 1; i >= 0; i--)
                        {
                            var entrada = fila[i];
                            if (entrada != null && ReferenceEquals(entrada.Character, info.Character))
                            {
                                fila.RemoveAt(i);
                                removidas++;
                            }
                        }
                        Diag.Write("nivel: atributos encerrados; entradas removidas=" + removidas
                            + " restantes=" + fila.Count);
                        if (fila.Count > 0) Abrir(manager, fila[0]);
                        else manager.Close();
                        return true;
                }
            }
            catch (Exception ex)
            {
                // Nunca deixar a UI de subida de nivel travada: em caso de falha, fluxo nativo.
                Diag.Write("fluxo de nivel falhou: " + ex.GetType().Name + ": " + ex.Message);
                return false;
            }
        }

        private static void Rotacionar(List<CharacterLevelUpInfo> fila, CharacterLevelUpInfo info)
        {
            fila.Remove(info);
            fila.Add(info);
        }

        private static void Reabrir(RoguelikeManager manager, List<CharacterLevelUpInfo> fila)
        {
            if (fila.Count == 0)
            {
                manager.Close();
                return;
            }
            var proxima = fila[0];
            var estado = Estados.GetOrCreateValue(proxima);

            // Sem pontos sobrando nao ha o que mostrar na fase de atributos.
            if (estado.Fase == Fase.Attributes && proxima.Character != null && proxima.Character.UnspentStatPoints <= 0)
            {
                Concluir(manager, fila, proxima);
                return;
            }
            Abrir(manager, proxima);
        }

        private static void Concluir(RoguelikeManager manager, List<CharacterLevelUpInfo> fila, CharacterLevelUpInfo alvo)
        {
            for (int i = fila.Count - 1; i >= 0; i--)
            {
                var entrada = fila[i];
                if (entrada != null && ReferenceEquals(entrada.Character, alvo.Character)) fila.RemoveAt(i);
            }
            if (fila.Count > 0) Abrir(manager, fila[0]);
            else manager.Close();
        }

        private static void Abrir(RoguelikeManager manager, CharacterLevelUpInfo info)
        {
            manager.OpenSkillSelectWindow(info, zeroOutAlpha: false);
            // OpenSkillSelectWindow sempre volta para LevelUpSequenceOrder[0]; aqui a janela
            // precisa refletir a etapa da entrada que esta sendo resolvida.
            manager.CurLevelUpStage = Estagio(Estados.GetOrCreateValue(info).Fase);
        }

        private static LevelUpStage Estagio(Fase fase)
        {
            switch (fase)
            {
                case Fase.Skills: return LevelUpStage.Skills;
                case Fase.Items: return LevelUpStage.Items;
                default: return LevelUpStage.Attributes;
            }
        }
    }
}
