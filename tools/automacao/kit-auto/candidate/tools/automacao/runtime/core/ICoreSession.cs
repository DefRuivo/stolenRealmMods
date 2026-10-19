// KIT-04 Core - Interface de sessão
namespace KIT04Core
{
    /// <summary>
    /// Gerencia sessão do Core: ID único, data/hora, ambiente.
    /// Sem sessão ativa, nenhum evento pode ser registrado.
    /// </summary>
    public interface ICoreSession
    {
        /// <summary>
        /// Registra nova sessão com ID único, data/hora e ambiente.
        /// </summary>
        /// <param name="idSessao">ID único da sessão (ex: "sessao-001")</param>
        /// <param name="data">Data/hora em ISO 8601</param>
        /// <param name="ambiente">Ambiente de execução (dev/teste/prod)</param>
        void Registrar(string idSessao, string data, string ambiente);

        /// <summary>
        /// Retorna o ID da sessão atual ou null se não houver sessão.
        /// </summary>
        string ObterIdSessao();

        /// <summary>
        /// Retorna true se sessão existe e está ativa.
        /// </summary>
        bool EstaAtiva();
    }
}
