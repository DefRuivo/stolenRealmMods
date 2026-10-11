using System;
using System.Collections.Generic;
using Gumatos.KitApiBridge;
using Gumatos.KitSdk.V1;
using Gumatos.RealmApi;

namespace Gumatos.KitApiBridge.AUT4
{
    /// <summary>
    /// INT-R1-C2-I1 (entregavel B) — ponte do INSTRUMENTO AUT4Probe.
    ///
    /// O probe deixou de patchear `OptionsManager.Localize` (alvo do hook `ui.localized`,
    /// api/Core/Contracts.cs:63). Aqui ele LIGA os dois nucleos que ja existem e entrega de volta ao
    /// probe apenas o gatilho observacional: a API instala o postfix (produtor), o adaptador
    /// `Gumatos.KitApiBridge.RealmHooksExtension` traduz a notificacao em EventV1 e esta testemunha
    /// repassa `Kind|Data` para o instrumento.
    ///
    /// Nada aqui decide autorizacao: `produtorAtivo` e `sessao` vem do probe (host), como na D7.
    /// </summary>
    public static class PonteAut4
    {
        /// <summary>Id de registro da testemunha do instrumento (o adaptador usa "realmapi.hooks").</summary>
        public const string RegistroDoInstrumento = "aut4.probe";
        /// <summary>Teto do canal de diagnostico local (sobra de seguranca; o adaptador ja limita em 64).</summary>
        public const int TetoDeDiagnostico = 64;

        /// <summary>Ligacao devolvida ao probe: Dispose remove assinatura, lease e registro.</summary>
        public sealed class Ligacao : IDisposable
        {
            private readonly RegistryV1 registro;
            private readonly IDisposable lease;
            private readonly RealmHooksExtension ponte;
            private readonly Queue<string> diagnostico = new Queue<string>();
            private bool encerrado;
            internal Ligacao(RegistryV1 registro, IDisposable lease, RealmHooksExtension ponte)
            { this.registro = registro; this.lease = lease; this.ponte = ponte; }

            internal void Anotar(string texto)
            {
                lock (diagnostico) { if (diagnostico.Count < TetoDeDiagnostico) diagnostico.Enqueue(texto); }
            }

            /// <summary>Diagnostico limitado do adaptador (so o TIPO da falha, nunca a mensagem).</summary>
            public string[] Diagnostics() { lock (diagnostico) { return diagnostico.ToArray(); } }

            public void Dispose()
            {
                if (encerrado) return;
                encerrado = true;
                try { ponte.Dispose(); } catch { }
                try { lease.Dispose(); } catch { }
                try { registro.Dispose(); } catch { }
            }
        }

        private sealed class Testemunha : IExtensionV1
        {
            private readonly Action<string> observacao;
            internal Testemunha(Action<string> observacao) { this.observacao = observacao; }
            // O contrato do kit diz que excecao de extensao vai para o diagnostico do kit (RegistryV1.cs:79-84).
            // Aqui o consumidor e o proprio instrumento: a chamada fica fechada para nao derrubar o push.
            public void OnEvent(EventV1 valor) { try { observacao(valor.Kind + "|" + valor.Data); } catch { } }
            public ReadingV1 Read(string key) => new ReadingV1("AUSENTE");
            public VerdictV1 Validate(string key, ReadingV1 observado, string esperado) => new VerdictV1("NAO_EXERCITADO");
        }

        /// <summary>
        /// Assinatura fixada: o probe resolve ESTE metodo por nome e tipos exatos
        /// (AUT4ProbePlugin.cs, `LigarPonteOpcional`). Alterar a assinatura desliga a ponte no probe.
        /// </summary>
        public static IDisposable Ligar(Action<string> observacao, Func<string> sessao, Func<bool> produtorAtivo)
        {
            if (observacao == null) throw new ArgumentNullException(nameof(observacao));
            if (sessao == null) throw new ArgumentNullException(nameof(sessao));
            if (produtorAtivo == null) throw new ArgumentNullException(nameof(produtorAtivo));

            var registro = new RegistryV1();
            var testemunha = new Testemunha(observacao);
            var lease = registro.Register(RegistroDoInstrumento, RegistryV1.ApiVersion, testemunha);
            // O canal de diagnostico do adaptador entra na propria Ligacao (fechado depois): o probe nao
            // recebe UNITY/BepInEx daqui — este assembly continua sem Unity.
            Ligacao? ligacao = null;
            var ponte = RealmHooksBinding.Create(registro, RealmHooks.Observed, produtorAtivo, sessao,
                texto => ligacao?.Anotar(texto));
            ligacao = new Ligacao(registro, lease, ponte);
            return ligacao;
        }
    }
}
