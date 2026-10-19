// KIT-04 Core - Registro de eventos
using System.Collections.Generic;

namespace KIT04Core
{
    /// <summary>
    /// Gerencia registro de eventos: tipo, detalhe, dados adicionais.
    /// Eventos sao registrados para auditoria e rastreabilidade da coleta.
    /// </summary>
    public interface ICoreEvento
    {
        /// <summary>
        /// Registra evento com tipo, detalhe e dados adicionais.
        /// </summary>
        /// <param name="tipo">Tipo do evento (ex: "leitura_concluida", "captura_png", "erro")</param>
        /// <param name="detalhe">Descrição curta do evento</param>
        /// <param name="dados">Dados adicionais como dictionary</param>
        void RegistrarEvento(string tipo, string detalhe, Dictionary<string, object>? dados = null);

        /// <summary>
        /// Retorna todos os eventos registrados.
        /// </summary>
        List<Dictionary<string, object>> ObterEventos();

        /// <summary>
        /// Limpa todos os eventos registrados.
        /// </summary>
        void LimparEventos();
    }
}
