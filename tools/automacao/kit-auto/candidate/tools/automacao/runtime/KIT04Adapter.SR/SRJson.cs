// KIT-04F Adapter — SRJson (serialização JSON para o adapter)
using KIT04Core;
using System;
using System.Collections;
using System.Collections.Generic;

namespace KIT04Adapter.SR
{
    /// <summary>
    /// Utilitários JSON para o adapter SR. Reusa KIT04Core.Json.
    /// </summary>
    public static class SRJson
    {
        /// <summary>
        /// Serializa um Dictionary para string JSON.
        /// </summary>
        public static string ParaString(Dictionary<string, object> dic)
        {
            return Json.Serialize(dic);
        }

        /// <summary>
        /// Cria um dicionário a partir de um array de pares.
        /// </summary>
        public static Dictionary<string, object> Dic(params object[] pares)
        {
            return Json.Campos(pares);
        }

        /// <summary>
        /// Converte um Dictionary para string JSON formatada.
        /// </summary>
        public static string Formatar(Dictionary<string, object> dic)
        {
            var json = Json.Serialize(dic);
            return json; // TODO: implementar indentação se necessário
        }
    }
}
