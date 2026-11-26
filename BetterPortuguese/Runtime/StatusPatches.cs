using System;
using System.IO;
using System.Linq;
using System.Reflection;
using BetterPortuguese.Core;
using HarmonyLib;

namespace BetterPortuguese.Runtime
{
    /// <summary>
    /// Grupo BP-COMP-STATUS: corrige a concordância do texto flutuante de status
    /// ("Proteção Elemental Aplicado" → "Aplicada").
    ///
    /// Fecha em três camadas: pin do Assembly-CSharp, casamento por NOME de parâmetro e try/catch no
    /// prefixo (uma exceção desliga o grupo até o próximo carregamento e devolve o texto original).
    /// Não bloqueia método de fechamento e não roda por frame: um IndexOf antecede qualquer alocação.
    /// </summary>
    internal static class StatusPatches
    {
        private static bool ready;
        private static bool failed;
        private static bool aliveReported;
        private static int corrected;
        private static Func<Settings> settings;
        private static OnceLog warnings;
        private static Action<string> info;

        public static void Install(Harmony harmony, Func<Settings> current, OnceLog limited, Action<string> log)
        {
            settings = current; warnings = limited; info = log;
            try
            {
                // Mesmo pin do grupo BP-COMP: leitura pura, sem alterar a assembly.
                string actual = Core.Resources.Sha256(File.ReadAllBytes(typeof(Tooltip).Assembly.Location));
                if (actual != Composition.AssemblySha256)
                    throw new InvalidOperationException("Assembly-CSharp SHA-256 divergente: medido " + actual + ", esperado " + Composition.AssemblySha256 + " (build homologada; re-inspecionar antes de re-pinar)");
            }
            catch (Exception ex) { warnings?.Write("BP-COMP-STATUS recusado: " + ex.Message); return; }

            try
            {
                MethodInfo target = Bindings.Exact(typeof(GameLogic), "OverheadMessage", typeof(void), false,
                    typeof(PlayerMovement), typeof(string), typeof(float), typeof(string));
                RequireArgument(target, "message", typeof(string));

                var prefix = new HarmonyMethod(typeof(StatusPatches).GetMethod(nameof(OverheadPrefix), BindingFlags.Static | BindingFlags.NonPublic))
                { priority = Priority.Last };
                harmony.Patch(target, prefix: prefix);

                var patches = Harmony.GetPatchInfo(target);
                if (patches == null || patches.Prefixes.Count(p => p.owner == Plugin.Guid) != 1)
                    throw new InvalidOperationException("ownership inesperado: GameLogic.OverheadMessage");
                foreach (string owner in patches.Owners.Where(o => o != Plugin.Guid))
                    warnings?.Write("BP-COMP-STATUS outro owner em OverheadMessage: " + owner + "; cosmetica apenas.");

                ready = true; failed = false;
                info?.Invoke("BP-COMP-STATUS: concordancia de texto flutuante registrada em GameLogic.OverheadMessage (prefixo no parametro 'message'; " + StatusAgreement.Feminine.Count + " nomes femininos).");
            }
            catch (Exception ex) { ready = false; warnings?.Write("BP-COMP-STATUS recusado: " + ex.Message); }
        }

        private static void RequireArgument(MethodInfo method, string name, Type type)
        {
            if (method == null || method.GetParameters().Count(p => p.Name == name && p.ParameterType == type) != 1)
                throw new MissingMethodException("BP-COMP-STATUS argumento ausente ou alterado: " + name);
        }

        /// <summary>
        /// Harmony casa `ref string message` pelo NOME do parâmetro. O texto final chega aqui já com o
        /// sufixo Aplicado e eventual " xN", sem cor (o jogo passa a cor em `color`).
        /// </summary>
        private static void OverheadPrefix(ref string message)
        {
            string incoming = message;
            try
            {
                if (!ready || failed || incoming == null) return;
                // Caminho rapido: nenhuma alocacao para o caso comum (dano, cura, esquiva...).
                if (incoming.IndexOf("Aplicado", StringComparison.Ordinal) < 0) return;
                if (!Enabled()) return;

                if (!aliveReported)
                {
                    aliveReported = true;
                    info?.Invoke("BP-COMP-STATUS: gancho de texto flutuante vivo.");
                }

                string result = StatusAgreement.Compose(incoming, out string reason);
                if (reason != null && reason.StartsWith("feminino:", StringComparison.Ordinal))
                {
                    corrected++;
                    if (corrected <= 3 || corrected % 50 == 0)
                        info?.Invoke("BP-COMP-STATUS: " + reason + " -> total " + corrected);
                }
                message = result;
            }
            catch (Exception ex)
            {
                // Falha fechada e definitiva: devolve o texto original e desliga o grupo.
                message = incoming;
                failed = true;
                warnings?.Write("BP-COMP-STATUS desativado por excecao: " + ex.GetType().Name + ": " + ex.Message);
            }
        }

        private static bool Enabled()
        {
            if (Composition.Enabled(settings?.Invoke(), OptionsManager.CurrentLanguage == LanguageChoice.PortugueseBrazil, out string reason)) return true;
            // OnceLog deduplica: nao vira log por frame, e trocar o idioma de volta volta a valer.
            warnings?.Write("BP-COMP-STATUS preservou vanilla: " + reason);
            return false;
        }
    }
}
