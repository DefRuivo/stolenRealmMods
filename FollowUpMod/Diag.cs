using System;
using System.IO;
using BepInEx;

namespace FollowUpMod
{
    /// <summary>
    /// Log em arquivo proprio, independente do logger do BepInEx. Serve para provar que um
    /// hook FOI chamado quando o LogOutput.log nao mostra a linha (dúvida real durante a
    /// validacao em jogo: patch anexado e nenhuma linha).
    /// </summary>
    /// <summary>Sonda de vida: prova que QUALQUER prefixo/postfix deste plugin roda neste processo.</summary>
    [HarmonyLib.HarmonyPatch(typeof(Character), "get_Level")]
    internal static class DiagProbePatch
    {
        [HarmonyLib.HarmonyPostfix]
        private static void Postfix()
        {
            Diag.CountProbe();
        }
    }

    internal static class Diag
    {
        private static int _probe;

        internal static void ReportAssemblies()
        {
            try
            {
                var copias = 0;
                foreach (var a in System.AppDomain.CurrentDomain.GetAssemblies())
                    if (a.GetName().Name == "Assembly-CSharp") copias++;
                Write("Assembly-CSharp carregado x" + copias
                    + " | typeof(Character).Assembly.Location=" + typeof(Character).Assembly.Location
                    + " | Harmony tipo=" + typeof(HarmonyLib.Harmony).Assembly.Location);
            }
            catch (System.Exception ex) { Write("ReportAssemblies falhou: " + ex.GetType().Name); }
        }

        internal static void CountProbe()
        {
            // Grava as primeiras chamadas: prova imediata de que o hook roda NESTE processo.
            if (++_probe > 3) return;
            Write("sonda viva get_Level x" + _probe);
        }

        private static readonly object Gate = new object();
        internal static readonly string Path =
            System.IO.Path.Combine(Paths.BepInExRootPath, "FollowUpMod.diag.log");

        internal static void Write(string message)
        {
            try
            {
                lock (Gate)
                    File.AppendAllText(Path, DateTime.Now.ToString("HH:mm:ss.fff") + " " + message + Environment.NewLine);
            }
            catch { }
        }
    }
}
