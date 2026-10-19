// KIT-04 Core - Interface para captura de screenshot
using System.Collections.Generic;

namespace KIT04Core
{
    /// <summary>
    /// Captura screenshot do frame atual e salva em PNG.
    /// Usa UnityEngine.ScreenCaptureModule quando disponivel.
    /// </summary>
    public interface IPictureCapture
    {
        /// <summary>
        /// Captura screenshot e salva em caminho especificado.
        /// </summary>
        /// <param name="caminhoSaida">Caminho absoluto para o arquivo PNG</param>
        /// <param name="largura">Largura da captura (0 = largura atual)</param>
        /// <param name="altura">Altura da captura (0 = altura atual)</param>
        /// <returns>True se captura bem-sucedida, false caso contrario</returns>
        bool CapturarPNG(string caminhoSaida, int largura, int altura);

        /// <summary>
        /// Retorna true se modulo de captura esta disponivel no Unity.
        /// </summary>
        bool EstaDisponivel();

        /// <summary>
        /// Retorna dictionary com detalhes da ultima captura (caminho, tamanho, timestamp).
        /// </summary>
        Dictionary<string, object>? ObterUltimaCaptura();
    }
}
