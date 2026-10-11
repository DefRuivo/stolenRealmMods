// KIT-04 Core - Implementação de ICoreIdentidade
using System.Collections.Generic;

namespace KIT04Core
{
    /// <summary>
    /// Implementação do contrato <see cref="ICoreIdentidade"/> sobre o serviço estático
    /// <see cref="IdentidadeDoCore"/> (que preserva o código provado do AUT4Probe).
    /// </summary>
    public class IdentidadeDoCoreImpl : ICoreIdentidade
    {
        public Dictionary<string, object> CalcularIdentidade(string hashFonteDeclarado)
            => IdentidadeDoCore.CalcularIdentidade(hashFonteDeclarado);

        public string CalcularHashSha256(string caminhoArquivo)
            => IdentidadeDoCore.Sha256(caminhoArquivo);
    }
}
