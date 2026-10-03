using System;
using System.Collections.Generic;
using System.Reflection;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace BetterTooltips
{
    /// <summary>
    /// Plugin BetterTooltips — melhora textos, tooltips e descrições do Stolen Realm.
    ///
    /// [BepInPlugin] registra o mod no BepInEx com:
    ///   - GUID:    identificador único do mod (padrão: dominio.dono.nome)
    ///   - Nome:    nome legível exibido nos logs
    ///   - Versão:  versão do mod
    ///
    /// Os ganchos Harmony são aplicados UM A UM (ver `AplicarPatches`), cada um com o seu log e um
    /// resumo com a CONTAGEM REAL — nunca em bloco, para que um gancho que falhe não derrube os
    /// outros em silêncio.
    /// </summary>
    [BepInPlugin("com.gumatos.bettertooltips", "Better Tooltips", "0.1.2")]
    public class Plugin : BaseUnityPlugin
    {
        /// <summary>
        /// Logger estático para as classes de patch poderem logar.
        /// </summary>
        internal static ManualLogSource Log { get; private set; }

        /// <summary>
        /// Awake() é chamado pelo BepInEx quando o plugin é carregado,
        /// logo no início do jogo (antes da primeira cena carregar).
        /// </summary>
        private void Awake()
        {
            Log = Logger;
            Logger.LogInfo("Better Tooltips carregado.");

            AplicarPatches();
        }

        /// <summary>
        /// Aplica os ganchos UM A UM, em vez de <c>PatchAll()</c>.
        ///
        /// <c>PatchAll()</c> é tudo-ou-nada: se um gancho só falhasse (assinatura que mudou numa versão
        /// do jogo, alvo que não resolve), a exceção subia dali e os DEMAIS ganchos não eram aplicados —
        /// o mod morria em silêncio. Com o laço abaixo, o gancho que falha fica escrito no log com o
        /// nome dele e o resto continua funcionando.
        ///
        /// O resumo usa a contagem REAL (quantos ganchos de quanto, e quantos métodos de patch cada um
        /// registrou), nunca um número fixo: é por ele que se descobre, lendo o log, que um gancho não
        /// entrou.
        /// </summary>
        private static void AplicarPatches()
        {
            // Harmony cria um "patch room" identificado pelo GUID.
            Harmony harmony = new Harmony("com.gumatos.bettertooltips");
            List<string> falhas = new List<string>();
            int ganchosTotal = 0;
            int ganchosOk = 0;
            int metodosOk = 0;

            Type[] tipos;
            try
            {
                tipos = typeof(Plugin).Assembly.GetTypes();
            }
            catch (Exception e)
            {
                Log.LogError("BetterTooltips: nao deu para listar os tipos do mod — nenhum gancho aplicado: " + e);
                return;
            }

            for (int i = 0; i < tipos.Length; i++)
            {
                Type tipo = tipos[i];
                if (!EhClasseDeGancho(tipo))
                {
                    continue;
                }

                ganchosTotal++;
                try
                {
                    PatchClassProcessor processador = harmony.CreateClassProcessor(tipo);
                    List<MethodInfo> aplicados = processador.Patch();
                    int quantos = aplicados != null ? aplicados.Count : 0;
                    metodosOk += quantos;
                    ganchosOk++;
                    Log.LogInfo("BetterTooltips: gancho aplicado — " + tipo.Name + " (" + quantos +
                                " metodo(s) de patch).");
                }
                catch (Exception e)
                {
                    falhas.Add(tipo.Name);
                    Log.LogError("BetterTooltips: FALHA ao aplicar o gancho " + tipo.Name + " — " + e.Message);
                }
            }

            string resumo = "BetterTooltips: patches Harmony aplicados (" + ganchosOk + "/" + ganchosTotal +
                            " ganchos, " + metodosOk + " metodos de patch).";

            if (falhas.Count == 0)
            {
                Log.LogInfo(resumo);
                return;
            }

            Log.LogError(resumo + " GANCHOS QUE FALHARAM: " + string.Join(", ", falhas.ToArray()) +
                         ". O mod continua de pe, mas o recurso que dependia deles nao existe nesta sessao.");
        }

        /// <summary>
        /// Classe de gancho = tem <c>[HarmonyPatch]</c> no TIPO (declarado, não herdado).
        ///
        /// Aqui NÃO se exige <c>[HarmonyPrefix]</c>/<c>[HarmonyPostfix]</c> no método: este mod usa a
        /// convenção do Harmony (métodos chamados <c>Prefix</c>/<c>Postfix</c>) em
        /// <c>LocalizePatch.Postfix</c> e <c>CorEOrdemDoTooltip.Prefix</c> — exigir o atributo pularia
        /// esses dois ganchos, ou seja, mudaria o que o mod faz. Uma classe com <c>[HarmonyPatch]</c> e
        /// sem método de patch apenas não registra nada (<c>Patch()</c> devolve lista vazia), sem
        /// efeito colateral — é o mesmo conjunto que o <c>PatchAll()</c> processaria.
        /// </summary>
        private static bool EhClasseDeGancho(Type tipo)
        {
            try
            {
                if (tipo == null || !tipo.IsClass)
                {
                    return false;
                }

                return tipo.GetCustomAttributes(typeof(HarmonyPatch), false).Length > 0;
            }
            catch (Exception)
            {
                // atributo com tipo que nao resolve (versao de jogo diferente): nao e gancho nosso
                return false;
            }
        }
    }
}
