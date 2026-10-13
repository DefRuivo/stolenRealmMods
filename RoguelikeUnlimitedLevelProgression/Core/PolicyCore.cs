using System;

namespace RoguelikeUnlimitedLevelProgression.Core
{
    public enum AdvanceDenial
    {
        None = 0,
        /// <summary>Fora do escopo ampliado: a comparacao vanilla (&lt; RoguelikeMaxLevel) decide.</summary>
        VanillaScope = 1,
        ModDisabled = 2,
        WrongCharacterScope = 3,
        Multiplayer = 4,
        VoluntaryCap = 5,
        NumericGuard = 6,
        SafetyBound = 7,
        TargetMissing = 8,
    }

    /// <summary>
    /// Entradas da politica de avanco. Todas as consultas ao jogo acontecem FORA deste core
    /// (em Policy), para que a decisao seja exercitavel pelo harness isolado.
    /// </summary>
    public struct AdvanceInputs
    {
        public bool ModEnabled;
        public bool IsAi;
        public bool IsRoguelikeCharacter;
        public bool IsMultiplayer;
        public bool IsRoguelikeMode;
        /// <summary>Nivel atual do personagem (int, Character.Level).</summary>
        public int Level;
        /// <summary>Teto vanilla lido do asset RoguelikeSettings.RoguelikeMaxLevel.</summary>
        public int VanillaCap;
        /// <summary>Progression.MaxLevel da config: 0 = sem teto voluntario; &gt;= 21 = teto voluntario.</summary>
        public int VoluntaryCap;
        /// <summary>Teto de representacao derivado (XpCurve.SafetyBoundLevel); 0 se indisponivel.</summary>
        public int SafetyBound;
        /// <summary>
        /// Valor observado do getter vanilla Character.MaxLevel (GlobalSettings.MaxLevel) — teto
        /// usado quando a extensao NAO esta ativa (grupo nao aplicado / multiplayer / backend
        /// indisponivel). 0 = desconhecido. Nao e um cap ampliado: e o proprio valor vanilla.
        /// </summary>
        public double VanillaMaxLevel;
        /// <summary>
        /// O personagem ainda esta dentro de Character.Load(int) (IsLoaded == false). Nesse
        /// momento ExperienceLevel ainda nao foi atribuido, logo Level e ~1.
        /// </summary>
        public bool IsLoading;
        /// <summary>
        /// Nivel salvo em CharacterSaveFile.ExperienceLevel que esta sendo carregado. So vale
        /// com IsLoading=true: o clamp de carga (Mathf.Min(MaxLevel, salvo)) NAO pode rebaixar
        /// este valor, nem no caminho vanilla.
        /// </summary>
        public double SavedLoadLevel;
        /// <summary>Curva real (F20/D20) valida e utilizavel.</summary>
        public bool CurveUsable;
        /// <summary>O proximo nivel e representavel e maior que o atual.</summary>
        public bool NextLevelRepresentable;
        /// <summary>Orcamento de pontos de atributo cabe em int/float exato.</summary>
        public bool StatBudgetOk;
        /// <summary>Os alvos Harmony do grupo de gameplay estao todos presentes/aplicados.</summary>
        public bool TargetsPresent;
    }

    /// <summary>
    /// Decisao de avanco. Substitui APENAS a comparacao `character.Level &lt; settings.RoguelikeMaxLevel`
    /// do bloco unico de Root.SendGameCompleteFromServer (parte06 §1). False = pula premio E lista.
    /// </summary>
    public static class PolicyCore
    {
        public static bool InExtendedScope(in AdvanceInputs i)
        {
            return i.ModEnabled && !i.IsAi && i.IsRoguelikeCharacter && i.IsRoguelikeMode && !i.IsMultiplayer;
        }

        /// <summary>
        /// Verdadeiro quando o avanco e permitido. Fora do escopo ampliado, reproduz a comparacao
        /// vanilla exata, para nao regredir campanha, IA nem multiplayer.
        /// </summary>
        public static bool CanAdvance(in AdvanceInputs i, out AdvanceDenial denial)
        {
            if (!InExtendedScope(in i))
            {
                denial = AdvanceDenial.VanillaScope;
                return i.Level < i.VanillaCap;
            }

            if (!i.TargetsPresent)
            {
                denial = AdvanceDenial.TargetMissing;
                return false;
            }
            if (!i.CurveUsable)
            {
                denial = AdvanceDenial.NumericGuard;
                return false;
            }
            if (!i.NextLevelRepresentable || !i.StatBudgetOk)
            {
                denial = AdvanceDenial.NumericGuard;
                return false;
            }
            if (i.VoluntaryCap > 0 && i.Level >= i.VoluntaryCap)
            {
                denial = AdvanceDenial.VoluntaryCap;
                return false;
            }
            if (i.SafetyBound > 0 && i.Level >= i.SafetyBound)
            {
                denial = AdvanceDenial.SafetyBound;
                return false;
            }
            denial = AdvanceDenial.None;
            return true;
        }

        /// <summary>
        /// Teto efetivo do getter Character.MaxLevel. Nunca devolve valor abaixo do nivel atual
        /// nem, em CARGA, abaixo do nivel salvo (nao rebaixa personagem salvo), e nunca devolve
        /// nao-finito. O teto e o limite de representacao (ou o valor vanilla observado quando a
        /// extensao nao esta ativa), reduzido pelo teto voluntario, com piso.
        /// </summary>
        public static double EffectiveMaxLevel(in AdvanceInputs i)
        {
            double bound = i.SafetyBound > 0
                ? i.SafetyBound
                : (i.VanillaMaxLevel > 0 ? i.VanillaMaxLevel : XpCurve.VanillaCapLevel);
            if (i.VoluntaryCap > 0 && i.VoluntaryCap < bound) bound = i.VoluntaryCap;

            double floor = i.Level;

            // Piso de CARGA (R3-01). Character.Load(int) executa
            //   ExperienceLevel = Mathf.Min(MaxLevel, CharacterSaveFile.ExperienceLevel)
            // ANTES de atribuir ExperienceLevel, entao Character.Level ainda e ~1 e a protecao
            // "bound > current ? bound : current" NAO cobre o nivel salvo. Enquanto o personagem
            // esta sendo carregado, o getter nunca pode devolver valor abaixo do salvo.
            if (i.IsLoading && XpCurve.IsUsableNumber(i.SavedLoadLevel) && i.SavedLoadLevel > floor)
            {
                floor = i.SavedLoadLevel;
            }

            return bound > floor ? bound : floor;
        }
    }
}
