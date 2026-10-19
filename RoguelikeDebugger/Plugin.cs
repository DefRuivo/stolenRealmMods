using System;
using System.Collections.Generic;
using System.Reflection;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;

namespace RoguelikeDebugger
{
    /// <summary>
    /// RoguelikeDebugger — mod de INVESTIGAÇÃO: apenas logs, nenhuma alteração de gameplay.
    /// Registra mecânicas internas no LogOutput.log para confirmarmos como o jogo funciona.
    /// </summary>
    [BepInPlugin("com.gumatos.roguelikedebugger", "Roguelike Debugger", "0.1.4")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log { get; private set; }

        private void Awake()
        {
            Log = Logger;

            // DBG-R2: a proveniencia sai ANTES dos ganchos, de proposito. Se o arranque morrer no
            // meio da aplicacao dos patches, a identidade do que ia ser observado ja' esta' no log -
            // que e' exatamente o caso em que a falta de dado no censo seria lida (errado) como
            // falta do fato no jogo.
            Proveniencia.Cabecalho();

            Logger.LogInfo("Roguelike Debugger carregado.");

            ResumoGanchos resultado = AplicarPatches();

            // Tres estados no log: INICIADO (cabecalho) -> ABERTO/PARCIAL (aqui) -> FECHADO
            // (rodape). Sem o rodape o dump esta' truncado; o verificador
            // (tools/verifica_proveniencia_debugger.py) nao deixa isso passar como "completo".
            Proveniencia.Estado(resultado.Ok, resultado.Total, resultado.Metodos, resultado.Falhas,
                                resultado.Aplicado("FlameEvalVoidPatch"));

            // Unico sinal de "o dump FECHOU": o BepInEx nao escreve rodape nenhum no LogOutput.log.
            // Mesmo evento que a API usa (api/Plugin/RealmApiPlugin.cs:32).
            Application.quitting += AoFechar;
        }

        private static void AoFechar()
        {
            Proveniencia.Fim("saida-do-jogo");
        }

        /// <summary>
        /// Contagem REAL do que foi aplicado. Existe para o carimbo de proveniencia (DBG-R2): o
        /// Estado no log declara `ganchosOk=n/n`, os nomes que falharam e se a matriz Flame entrou
        /// (`PARCIAL` quando algum gancho nao aplicou). Nao muda nenhum gancho.
        /// </summary>
        private sealed class ResumoGanchos
        {
            internal int Total;
            internal int Ok;
            internal int Metodos;
            internal readonly List<string> Falhas = new List<string>();
            internal readonly List<string> Aplicados = new List<string>();

            internal bool Aplicado(string nome)
            {
                return Aplicados.Contains(nome);
            }
        }

        /// <summary>
        /// Aplica os ganchos UM A UM, em vez de <c>PatchAll()</c>.
        ///
        /// <c>PatchAll()</c> e tudo-ou-nada: um gancho so que falhasse (tipo ou assinatura que mudou
        /// numa versao do jogo) deixaria TODOS os outros sem aplicar — e em silencio; num mod de
        /// diagnostico isso e o pior caso (o log sai incompleto sem ninguem perceber). Com o laco
        /// abaixo, o gancho que falha fica escrito no log com o nome dele e os outros continuam. O
        /// resumo usa a contagem REAL, nunca um numero fixo. Mesmo modelo do
        /// RoguelikeSkillTreeVisualizer; quando tudo da certo os patches aplicados sao EXATAMENTE os
        /// mesmos de antes.
        /// </summary>
        private static ResumoGanchos AplicarPatches()
        {
            var resultado = new ResumoGanchos();
            var harmony = new Harmony("com.gumatos.roguelikedebugger");
            var falhas = resultado.Falhas;
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
                Log.LogError("Roguelike Debugger: nao deu para listar os tipos do mod — nenhum gancho aplicado: " + e);
                return resultado;
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
                    resultado.Aplicados.Add(tipo.Name);
                    Log.LogInfo("Roguelike Debugger: gancho aplicado — " + tipo.Name + " (" + quantos +
                                " metodo(s) do jogo).");
                }
                catch (Exception e)
                {
                    falhas.Add(tipo.Name);
                    Log.LogError("Roguelike Debugger: FALHA ao aplicar o gancho " + tipo.Name + " — " + e.Message);
                }
            }

            string linhaResumo = "Roguelike Debugger: patches Harmony aplicados (" + ganchosOk + "/" + ganchosTotal +
                            " ganchos, " + metodosOk + " metodos do jogo).";

            resultado.Total = ganchosTotal;
            resultado.Ok = ganchosOk;
            resultado.Metodos = metodosOk;

            if (falhas.Count == 0)
            {
                Log.LogInfo(linhaResumo);
                return resultado;
            }

            Log.LogError(linhaResumo + " GANCHOS QUE FALHARAM: " + string.Join(", ", falhas.ToArray()) +
                         ". O mod continua de pe, mas o log do recurso que dependia deles nao sai nesta sessao.");
            return resultado;
        }

        /// <summary>
        /// Classe de gancho = tem <c>[HarmonyPatch]</c> no TIPO (declarado, nao herdado) — a MESMA
        /// condicao que o <c>PatchAll()</c> exigia para processar a classe.
        ///
        /// AQUI NAO SE EXIGE <c>[HarmonyPrefix]</c>/<c>[HarmonyPostfix]</c> NO METODO: os ganchos
        /// deste mod (as 10 classes de <c>Patches/*.cs</c>) sao declarados pela CONVENCAO DE NOME do
        /// Harmony (metodo chamado <c>Postfix</c>), que o Harmony aceita exatamente como aceita o
        /// atributo — os nomes sao <c>Prefix</c>/<c>Postfix</c>/<c>Transpiler</c>/<c>Finalizer</c>.
        /// Exigir o atributo PULA os ganchos deste mod: o mod carrega, loga "carregado." e nao aplica
        /// nada — o silencio parecendo sucesso. Uma classe com <c>[HarmonyPatch]</c> e sem metodo de
        /// patch apenas nao registra nada (<c>Patch()</c> devolve lista vazia), sem efeito colateral —
        /// e o mesmo conjunto que o <c>PatchAll()</c> processaria. Mesmo filtro do BetterTooltips.
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
