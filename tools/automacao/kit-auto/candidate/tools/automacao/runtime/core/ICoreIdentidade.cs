// KIT-04 Core - Interface de identidade do instrumento (contrato v1.0.0)
using System.Collections.Generic;

namespace KIT04Core
{
    /// <summary>
    /// Contrato de identidade do Core (spec §"ICoreIdentidade", fecha a lacuna L1 da AUD-1):
    /// o JSON do instrumento precisa dizer QUAL binário leu, não só qual sessão rodou.
    /// Implementação: <see cref="IdentidadeDoCoreImpl"/> (delega para o serviço estático
    /// <see cref="IdentidadeDoCore"/>, reusado do AUT4Probe).
    /// </summary>
    public interface ICoreIdentidade
    {
        /// <summary>
        /// Calcula a identidade do assembly carregado e devolve os campos
        /// (hash_fonte_declarado, hash_dll_do_core, arquivo_dll_do_core, bytes_dll_do_core, erro).
        /// </summary>
        Dictionary<string, object> CalcularIdentidade(string hashFonteDeclarado);

        /// <summary>
        /// Calcula SHA256 de um arquivo em disco.
        /// </summary>
        string CalcularHashSha256(string caminhoArquivo);
    }
}
