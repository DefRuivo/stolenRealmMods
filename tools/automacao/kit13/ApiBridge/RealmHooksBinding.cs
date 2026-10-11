using System;
using System.Runtime.CompilerServices;
using Gumatos.KitSdk.V1;
using Gumatos.RealmApi;

// Sutura INTERNA de teste do proprio projeto: a suite offline (ApiBridgeHarness) precisa exercitar a
// fronteira de versao F4 (parte02 §2) com valores divergentes. Nao existe descoberta por reflexao no
// adaptador: e o harness que passa o par declarado; o caminho publico (Create de 5 argumentos) usa
// sempre as constantes reais. A superficie PUBLICA do adaptador e exatamente a da decisao D4.
[assembly: InternalsVisibleTo("ApiBridgeHarness")]

namespace Gumatos.KitApiBridge
{
    /// <summary>
    /// INT-R1-C2-I1 (D4/D7). Unica porta da ponte: tudo o que o adaptador precisa vem do host por
    /// parametro, nunca de descoberta (nada de reflexao, config, arquivo ou varredura de assembly).
    /// </summary>
    public static class RealmHooksBinding
    {
        /// <summary>
        /// Cria o adaptador. <paramref name="producerActive"/> e a autorizacao/atividade declarada pelo
        /// host (D5/D7): API ausente nem chega aqui; EnableHooks=false ou alvo divergente
        /// (RealmApiPlugin.cs:21-31) = false. <paramref name="session"/> e a sessao do EXPERIMENTO,
        /// validada ANTES de registrar (padrao CounterAdapter.cs:22-24).
        /// </summary>
        public static RealmHooksExtension Create(
            RegistryV1 registry,
            Signal<HookNotification> observed,
            Func<bool> producerActive,
            Func<string> session,
            Action<string> diagnostic)
            => Create(registry, observed, producerActive, session, diagnostic,
                      RealmHooksExtension.KitApi, RealmHooksExtension.ProducerVersion);

        internal static RealmHooksExtension Create(
            RegistryV1 registry,
            Signal<HookNotification> observed,
            Func<bool> producerActive,
            Func<string> session,
            Action<string> diagnostic,
            string kitApiDeclarado,
            string producerVersionDeclarada)
        {
            if (registry == null) throw new ArgumentNullException(nameof(registry));
            if (observed == null) throw new ArgumentNullException(nameof(observed));
            if (producerActive == null) throw new ArgumentNullException(nameof(producerActive));
            if (session == null) throw new ArgumentNullException(nameof(session));
            if (diagnostic == null) throw new ArgumentNullException(nameof(diagnostic));

            // F4: par declarado, string EXATA, recusa fechada (parte02 §2). Sempre antes de registrar
            // ou assinar: recusa nao deixa lease nem assinatura orfa (Count intacto).
            Exigir(kitApiDeclarado, RegistryV1.ApiVersion, "KitApi");
            Exigir(producerVersionDeclarada, ApiIdentity.Version, "ProducerVersion");

            // Sessao do host validada pela MESMA regra que o kit aplica ao EventV1 (RegistryV1.cs:16-18),
            // tambem antes de qualquer inscricao.
            var declarada = session();
            _ = new EventV1(declarada, 0, RealmHooksExtension.RegistryId, string.Empty);

            var extensao = new RealmHooksExtension(registry, producerActive, diagnostic, declarada);
            extensao.Ligar(observed, kitApiDeclarado);
            return extensao;
        }

        /// <summary>Uma regra de versao para todas as fronteiras do adaptador: igualdade ordinal.</summary>
        private static void Exigir(string declarado, string esperado, string fronteira)
        {
            if (!string.Equals(declarado, esperado, StringComparison.Ordinal))
                throw new NotSupportedException("API_INCOMPATIVEL: " + fronteira + " declarado=" + declarado + " esperado=" + esperado);
        }
    }
}
