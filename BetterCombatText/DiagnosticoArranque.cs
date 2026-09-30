using System;
using HarmonyLib;
using TMPro;
using UnityEngine;

namespace BetterCombatText
{
    /// <summary>
    /// Diagnostico de ARRANQUE — 100% LEITURA, nao altera nada.
    ///
    /// <para><b>Por que existe:</b> nao da para saber estaticamente (os prefabs do jogo sao
    /// MonoBehaviour sem type tree) QUAL fonte/material/shader cada componente alvo recebeu. Aqui
    /// o mod procura os componentes alvo em cena e escreve no log: nome do objeto, tipo do
    /// componente, nome da fonte TMP, nome do material COMPARTILHADO (ainda o do prefab, antes de
    /// qualquer clonagem), nome do shader e se ele e distance field (tem <c>_OutlineWidth</c>).</para>
    ///
    /// <para><b>Por que DOIS gatilhos:</b> <c>OptionsManager.Localize</c> NAO roda a cada frame — ele
    /// e chamado quando a UI ATRIBUI um texto, ou seja, num surto durante a construcao das telas, e
    /// depois para. Um gate por tempo ali perdeu a janela (medido: duas execucoes do jogo sem NENHUMA
    /// linha do diagnostico). O gatilho confiavel e <c>GUIManager.Update</c>, que roda a cada frame;
    /// os dois chamam a MESMA rotina, que executa uma vez so.</para>
    /// </summary>
    internal static class DiagnosticoRotina
    {
        private static bool _feito;
        private static bool _falhou;
        private static bool _vidaLogada;
        private static float _proximaChecagem;
        private const float EsperaMinima = 20f;
        private const float DesistirEm = 240f;

        /// <summary>Ponto unico de entrada: idempotente e a prova de excecao.</summary>
        internal static void Tentar(string origem)
        {
            if (_feito || _falhou || !Plugin.Ativo || Plugin.Cfg == null)
            {
                return;
            }
            try
            {
                if (!_vidaLogada)
                {
                    _vidaLogada = true;
                    Plugin.Log.LogInfo($"Better Combat Text: gatilho '{origem}' vivo (primeira chamada) — o patch esta rodando.");
                }
                float agora = Time.realtimeSinceStartup;
                if (agora < EsperaMinima || agora < _proximaChecagem)
                {
                    return; // cedo demais, ou ainda dentro do throttle de 2s
                }
                _proximaChecagem = agora + 2f;

                // So roda quando algum alvo ja existe em cena (ou quando ja esperamos o suficiente).
                if (!TemAlvoEmCena() && agora < DesistirEm)
                {
                    return;
                }
                _feito = true;
                Rodar();
            }
            catch (Exception e)
            {
                _falhou = true;
                Plugin.Log.LogWarning($"Better Combat Text: diagnostico de arranque falhou: {e.GetType().Name}: {e.Message}");
            }
        }

        /// <summary>Checagem barata e throttled: algum dos componentes alvo ja existe em cena?</summary>
        private static bool TemAlvoEmCena()
        {
            try
            {
                return Resources.FindObjectsOfTypeAll<PlayerInfoWindow>().Length > 0
                    || Resources.FindObjectsOfTypeAll<BossHealthbar>().Length > 0
                    || Resources.FindObjectsOfTypeAll<StatusIcon>().Length > 0
                    || Resources.FindObjectsOfTypeAll<DiceRoller>().Length > 0
                    || Resources.FindObjectsOfTypeAll<DiceVisualSetup>().Length > 0;
            }
            catch
            {
                return true; // em caso de duvida, roda o diagnostico
            }
        }

        private static void Rodar()
        {
            Plugin.Log.LogInfo("Better Combat Text: --- diagnostico de arranque (somente leitura, nada alterado) ---");

            ReportarTmp("PlayerInfoWindow.playerName (NOME DO INIMIGO no hover em combate)",
                Resources.FindObjectsOfTypeAll<PlayerInfoWindow>(), w => w != null ? w.playerName : null);

            ReportarTmp("BossHealthbar.BossName (NOME DO INIMIGO na barra de chefe)",
                Resources.FindObjectsOfTypeAll<BossHealthbar>(), b => b != null ? b.BossName : null);

            ReportarTmp("Tooltip.Title (nome do buff/debuff no tooltip, default DESLIGADO no config)",
                Resources.FindObjectsOfTypeAll<Tooltip>(), t => t != null ? t.Title : null);

            ReportarTmp("DiceRoller.ResultText (resultado do dado nos eventos)",
                Resources.FindObjectsOfTypeAll<DiceRoller>(), d => d != null ? d.ResultText : null);

            var setups = Resources.FindObjectsOfTypeAll<DiceVisualSetup>();
            int faces = 0;
            TMP_Text primeiraFace = null;
            for (int i = 0; i < setups.Length; i++)
            {
                var numeros = setups[i] != null ? setups[i].DiceNumbers : null;
                if (numeros == null)
                {
                    continue;
                }
                faces += numeros.Length;
                if (primeiraFace == null && numeros.Length > 0)
                {
                    primeiraFace = numeros[0];
                }
            }
            if (primeiraFace != null)
            {
                Descrever("DiceVisualSetup.DiceNumbers (NUMERO NA FACE DO DADO)", primeiraFace);
            }
            Plugin.Log.LogInfo($"Better Combat Text: faces de dado (TextMeshPro) encontradas: {faces} em {setups.Length} DiceVisualSetup.");

            // Rotulos de buff/debuff: UI.Text legado — aqui so se CONTA e se confirma o TIPO real.
            var icones = Resources.FindObjectsOfTypeAll<StatusIcon>();
            int comStack = 0;
            string tipoStack = "(nenhum componente de stack encontrado em cena)";
            for (int i = 0; i < icones.Length; i++)
            {
                var icone = icones[i];
                if (icone == null || icone.stackCount == null)
                {
                    continue;
                }
                comStack++;
                tipoStack = icone.stackCount.GetType().FullName;
            }
            Plugin.Log.LogInfo($"Better Combat Text: StatusIcon em cena: {icones.Length} ({comStack} com stackCount).");
            Plugin.Log.LogInfo("Better Combat Text: tipo REAL do rotulo de stack = '" + tipoStack + "' — " +
                (tipoStack.Contains("UnityEngine.UI.Text")
                    ? "UI.Text LEGADO: halo SUAVE e impossivel ali; aplicado contorno duro + sombra + negrito."
                    : "TextMeshPro: halo suave viavel."));

            var legados3D = Resources.FindObjectsOfTypeAll<TextMesh>();
            Plugin.Log.LogInfo("Better Combat Text: TextMesh legado (3D) em cena: " + legados3D.Length + " — esse tipo " +
                "(usado por DieSideAwareTextDie) NAO e tocado pelo mod; se a face do dado do seu build usar este " +
                "tipo, o numero do dado fica sem efeito (nada quebra).");

            var todosTmps = Resources.FindObjectsOfTypeAll<TMP_Text>();
            Plugin.Log.LogInfo($"Better Combat Text: total de TMP_Text em cena: {todosTmps.Length} (so os alvos sao tocados).");
            Plugin.Log.LogInfo("Better Combat Text: --- fim do diagnostico ---");
        }

        private static void ReportarTmp<T>(string rotulo, T[] donos, Func<T, TMP_Text> seletor)
            where T : UnityEngine.Object
        {
            try
            {
                if (donos == null || donos.Length == 0)
                {
                    Plugin.Log.LogInfo($"Better Combat Text: {rotulo}: nenhuma instancia em cena agora " +
                                       "(normal antes de abrir a tela correspondente).");
                    return;
                }
                TMP_Text alvo = null;
                for (int i = 0; i < donos.Length && alvo == null; i++)
                {
                    if (donos[i] == null)
                    {
                        continue;
                    }
                    try
                    {
                        alvo = seletor(donos[i]);
                    }
                    catch
                    {
                        // segue o jogo
                    }
                }
                if (alvo == null)
                {
                    Plugin.Log.LogInfo($"Better Combat Text: {rotulo}: componente ainda nao preenchido pelo jogo.");
                    return;
                }
                Descrever(rotulo, alvo);
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: diagnostico de '{rotulo}' falhou: {e.GetType().Name}: {e.Message}");
            }
        }

        private static void Descrever(string rotulo, TMP_Text alvo)
        {
            var mat = alvo.fontSharedMaterial;
            bool df = mat != null && mat.HasProperty("_OutlineWidth");
            Plugin.Log.LogInfo(
                $"Better Combat Text: {rotulo} -> objeto='{alvo.gameObject.name}', tipo={alvo.GetType().Name}, " +
                $"fonte='{(alvo.font != null ? alvo.font.name : "(nula)")}', " +
                $"material compartilhado='{(mat != null ? mat.name : "(nulo)")}', " +
                $"shader='{(mat != null && mat.shader != null ? mat.shader.name : "(nulo)")}', " +
                $"distance field (tem _OutlineWidth)={df}");
        }
    }

    /// <summary>Gatilho por frame — o confiavel (roda enquanto o GUIManager existir).</summary>
    [HarmonyPatch(typeof(GUIManager), "Update", new Type[0])]
    internal static class GatilhoDiagnosticoPorFrame
    {
        private static void Postfix()
        {
            DiagnosticoRotina.Tentar("GUIManager.Update");
        }
    }

    /// <summary>Gatilho pelo funil de texto — tambem serve de marcador de vida do patch.</summary>
    [HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]
    internal static class GatilhoDiagnosticoPorLocalize
    {
        private static void Postfix()
        {
            DiagnosticoRotina.Tentar("OptionsManager.Localize");
        }
    }
}
