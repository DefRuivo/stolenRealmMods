using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Gumatos.KitApiBridge;
using Gumatos.KitSdk.V1;
using Gumatos.RealmApi;

/// <summary>
/// INT-R1-C2-I1 — suite OFFLINE da ponte RealmApi -> KitSdk. Roda sem jogo, sem BepInEx, sem Harmony,
/// sem Unity: exercita o RegistryV1, o Signal&lt;T&gt; e o HookNotification REAIS (os tres sao CLR puro).
///
/// INSTRUMENTACAO DECLARADA (nao e atalho escondido): o produtor so publica por dentro — o construtor de
/// HookNotification (Contracts.cs:75) e Signal&lt;T&gt;.Publish (Contracts.cs:91) e RealmHooks.Emit
/// (Contracts.cs:109) sao internal. api/ e CONGELADO neste cartao, entao o harness injeta pela via
/// interna por reflexao (metodo Producao). O caminho Harmony real (HookInstallation.Install -> postfix
/// -> RealmHooks.Emit) fica NAO_EXERCITADO.
/// </summary>
static class Program
{
    private const string Id = RealmHooksExtension.RegistryId;
    private const string Sessao = "offline-bridge-661";

    private static void Check(bool condicao, string mensagem = "assertion") { if (!condicao) throw new Exception(mensagem); }

    private static T Throws<T>(Action acao) where T : Exception
    {
        try { acao(); } catch (T erro) { return erro; }
        throw new Exception("EXPECTED_" + typeof(T).Name);
    }

    // ------------------------------------------------------------------ instrumentacao de bancada

    private static class Producao
    {
        private static readonly ConstructorInfo? Ctor = typeof(HookNotification).GetConstructor(
            BindingFlags.Instance | BindingFlags.NonPublic, null,
            new[] { typeof(string), typeof(object), typeof(object[]), typeof(object) }, null);
        private static readonly MethodInfo? Enviar = typeof(Signal<HookNotification>).GetMethod("Publish", BindingFlags.Instance | BindingFlags.NonPublic);
        private static readonly MethodInfo? EmitirInterno = typeof(RealmHooks).GetMethod("Emit", BindingFlags.Static | BindingFlags.NonPublic);

        public static HookNotification Notificacao(string hookId, object? instancia, object?[] argumentos, object? resultado)
        {
            if (Ctor == null) throw new Exception("HookNotification..ctor interno nao encontrado");
            return (HookNotification)Ctor.Invoke(new object?[] { hookId, instancia, argumentos, resultado })!;
        }

        public static void Publicar(Signal<HookNotification> sinal, HookNotification notificacao, Action<Exception>? relatar = null)
        {
            if (Enviar == null) throw new Exception("Signal<T>.Publish interno nao encontrado");
            Enviar.Invoke(sinal, new object?[] { notificacao, relatar });
        }

        public static void Emitir(string hookId, object? instancia, object?[] argumentos, object? resultado, Action<Exception>? relatar = null)
        {
            if (EmitirInterno == null) throw new Exception("RealmHooks.Emit interno nao encontrado");
            EmitirInterno.Invoke(null, new object?[] { hookId, instancia, argumentos, resultado, relatar });
        }
    }

    private sealed class Testemunha : IExtensionV1
    {
        public readonly List<EventV1> Eventos = new List<EventV1>();
        public Action<EventV1>? AoReceber;
        public void OnEvent(EventV1 valor) { lock (Eventos) Eventos.Add(valor); AoReceber?.Invoke(valor); }
        public ReadingV1 Read(string key) => new ReadingV1("AUSENTE");
        public VerdictV1 Validate(string key, ReadingV1 observado, string esperado) => new VerdictV1("NAO_EXERCITADO");
    }

    private sealed class Bancada : IDisposable
    {
        public readonly RegistryV1 Registry = new RegistryV1();
        public readonly Signal<HookNotification> Sinal = new Signal<HookNotification>();
        public readonly Testemunha Testemunha = new Testemunha();
        public readonly List<string> Diagnostico = new List<string>();
        public bool ProdutorAtivo;
        public string SessaoDeclarada = Sessao;
        public RealmHooksExtension? Ponte;
        private readonly IDisposable? testemunhaLease;

        public Bancada(bool ativo = true, bool comTestemunha = true)
        {
            ProdutorAtivo = ativo;
            if (comTestemunha) testemunhaLease = Registry.Register("testemunha", RegistryV1.ApiVersion, Testemunha);
        }

        public RealmHooksExtension Ligar(Func<bool>? produtor = null)
        {
            Ponte = RealmHooksBinding.Create(Registry, Sinal, produtor ?? (() => ProdutorAtivo), () => SessaoDeclarada, Diagnostico.Add);
            return Ponte;
        }

        public void Notificar(string hookId, object?[]? argumentos = null, object? resultado = null, object? instancia = null)
            => Producao.Publicar(Sinal, Producao.Notificacao(hookId, instancia, argumentos ?? new object?[0], resultado));

        public ReadingV1 Ler(string chave) => Registry.Read(Id, chave);

        public void Dispose() { Ponte?.Dispose(); testemunhaLease?.Dispose(); Registry.Dispose(); }
    }

    // ------------------------------------------------------------------ assercoes P1..P16

    private static Dictionary<string, Action> Testes() => new Dictionary<string, Action>
    {
        ["P1"] = () =>
        {
            using var b = new Bancada(comTestemunha: false);
            b.Ligar();
            Check(RealmHooksExtension.KitApi == "1.0.0", "KitApi declarado");
            Check(RealmHooksExtension.ProducerVersion == "0.1.0", "ProducerVersion declarado");
            Check(b.Registry.Count == 1, "Count==1 (so o adaptador)");
            Check(b.Ler("hooks.count").Status == "OBSERVADO" && b.Ler("hooks.count").Value == "0", "id realmapi.hooks responde");
            Check(b.Registry.Read("realmapi.hook", "hooks.count").Status == "AUSENTE", "id e exato");
            Check(RealmHooksExtension.RegistryId == "realmapi.hooks");
        },

        ["P2"] = () =>
        {
            using var b = new Bancada(comTestemunha: false);
            var erro = Throws<NotSupportedException>(() => RealmHooksBinding.Create(
                b.Registry, b.Sinal, () => true, () => b.SessaoDeclarada, b.Diagnostico.Add, "2.0.0", RealmHooksExtension.ProducerVersion));
            Check(erro.Message.Contains("API_INCOMPATIVEL"), "mensagem: " + erro.Message);
            Check(b.Registry.Count == 0, "recusa nao registra nada");
            // O KitSdk ja recusa kit divergente no Register (RegistryV1.cs:92), entao so a contagem nao
            // diz QUEM recusou. Com um registry JA descartado, a recusa so pode ser a do adaptador:
            // se a checagem F4 nao viesse antes, o Register lancaria ObjectDisposedException.
            var descartado = new RegistryV1();
            descartado.Dispose();
            Throws<NotSupportedException>(() => RealmHooksBinding.Create(
                descartado, b.Sinal, () => true, () => b.SessaoDeclarada, b.Diagnostico.Add, "2.0.0", RealmHooksExtension.ProducerVersion));
            Throws<NotSupportedException>(() => RealmHooksBinding.Create(
                descartado, b.Sinal, () => true, () => b.SessaoDeclarada, b.Diagnostico.Add, RealmHooksExtension.KitApi, "0.2.0"));
        },

        ["P3"] = () =>
        {
            using var b = new Bancada();
            var erro = Throws<NotSupportedException>(() => RealmHooksBinding.Create(
                b.Registry, b.Sinal, () => true, () => b.SessaoDeclarada, b.Diagnostico.Add, RealmHooksExtension.KitApi, "0.2.0"));
            Check(erro.Message.Contains("API_INCOMPATIVEL"), "mensagem: " + erro.Message);
            Check(b.Registry.Count == 1, "so a testemunha no registro");
            for (var i = 0; i < 3; i++) b.Notificar("ui.localized", new object?[] { "t" + i }, "r");
            Check(b.Testemunha.Eventos.Count == 0, "nenhuma assinatura no Signal");
            Check(b.Diagnostico.Count == 0, "recusa e silenciosa no canal de diagnostico");
        },

        ["P4"] = () =>
        {
            foreach (var sessao in new[] { string.Empty, "   ", new string('s', 129) })
            {
                using var b = new Bancada();
                Throws<ArgumentException>(() => RealmHooksBinding.Create(b.Registry, b.Sinal, () => true, () => sessao, b.Diagnostico.Add));
                Check(b.Registry.Count == 1, "so a testemunha: sem lease orfao");
                b.Notificar("ui.localized", new object?[] { "t" }, "r");
                Check(b.Testemunha.Eventos.Count == 0, "sem assinatura orfa");
            }
            using var c = new Bancada();
            Throws<ArgumentException>(() => RealmHooksBinding.Create(c.Registry, c.Sinal, () => true, () => null!, c.Diagnostico.Add));
            Check(c.Registry.Count == 1, "sessao nula tambem recusada");
            using var d = new Bancada();
            d.SessaoDeclarada = new string('x', 128);
            d.Ligar();
            Check(d.Ler("hooks.count").Status == "OBSERVADO", "128 e o limite aceito");
        },

        ["P5"] = () =>
        {
            using var b = new Bancada(ativo: false);
            b.Ligar();
            for (var i = 0; i < 3; i++) b.Notificar("ui.localized", new object?[] { "t" + i }, "r");
            Check(b.Testemunha.Eventos.Count == 0, "produtor inativo nao publica EventV1");
            Check(b.Ler("hooks.count").Status == "NAO_EXERCITADO", "NAO_EXERCITADO, nunca OBSERVADO 0");
            Check(b.Ler("hooks.unknown").Status == "NAO_EXERCITADO");
            Check(b.Ler("hook.ui.localized.count").Status == "NAO_EXERCITADO");
            Check(b.Registry.Count == 2, "registra mesmo inativo (lease e de ciclo de vida)");
        },

        ["P6"] = () =>
        {
            using var b = new Bancada();
            b.Ligar();
            Check(b.Ler("hooks.count").Status == "OBSERVADO" && b.Ler("hooks.count").Value == "0", "0 com produtor ativo e OBSERVADO");
            for (var i = 0; i < 3; i++) b.Notificar("ui.localized", new object?[] { "t" + i }, "r");
            Check(b.Ler("hooks.count").Value == "3", "contador real: " + b.Ler("hooks.count").Value);
            Check(b.Ler("hooks.count").Status == "OBSERVADO");
            using var c = new Bancada(ativo: false);
            c.Ligar();
            for (var i = 0; i < 3; i++) c.Notificar("ui.localized", new object?[] { "t" + i }, "r");
            c.ProdutorAtivo = true;
            Check(c.Ler("hooks.count").Value == "0", "nada acumulou com produtor inativo");
            Check(c.Ler("hooks.count").Status == "OBSERVADO");
        },

        ["P7"] = () =>
        {
            using var b = new Bancada();
            b.Ligar();
            for (var i = 0; i < 3; i++) b.Notificar("ui.localized", new object?[] { "t" + i }, "r" + i);
            Check(b.Testemunha.Eventos.Count == 3, "um EventV1 por notificacao conhecida");
            for (var i = 0; i < 3; i++)
            {
                var evento = b.Testemunha.Eventos[i];
                Check(evento.Kind == "ui.localized", "Kind==HookId");
                Check(evento.Session == Sessao, "Session declarada pelo host");
                Check(evento.Frame == i, "Frame ordinal: " + evento.Frame);
                Check(evento.Data.Contains("quadro=" + i), "marca quadro=ordinal: " + evento.Data);
                Check(evento.Data.Contains("r" + i), "resultado no resumo");
            }
        },

        ["P8"] = () =>
        {
            using var b = new Bancada();
            b.Ligar();
            b.Notificar("game.desconhecido", new object?[] { "t" }, "r");
            Check(b.Testemunha.Eventos.Count == 0, "HookId fora do catalogo nao vira evento");
            Check(b.Ler("hooks.unknown").Status == "OBSERVADO" && b.Ler("hooks.unknown").Value == "1", "conta o desconhecido");
            Check(b.Ler("hooks.count").Value == "0", "desconhecido nao entra no total");
            Check(b.Ler("hook.game.desconhecido.count").Status == "AUSENTE", "chave fora do vocabulario");
            var veredito = b.Registry.Validate(Id, "hook.game.desconhecido.count", b.Ler("hook.game.desconhecido.count"), "1");
            Check(veredito.Status == "NAO_EXERCITADO", "veredito sobre o desconhecido: " + veredito.Status);
            Check(veredito.Status != "PASSOU");
        },

        ["P9"] = () =>
        {
            using var b = new Bancada();
            b.Ligar();
            b.Notificar("ui.localized", new object?[] { "a" }, "r");
            b.Notificar("ui.localized", new object?[] { "b" }, "r");
            b.Notificar("game.awake");
            Check(b.Ler("hook.ui.localized.count").Value == "2", "conta so aquele hook");
            Check(b.Ler("hook.game.awake.count").Value == "1");
            Check(b.Ler("hook.combat.turn-started.count").Status == "OBSERVADO" && b.Ler("hook.combat.turn-started.count").Value == "0", "hook do catalogo sem evento = 0 OBSERVADO");
            foreach (var chave in new[] { "hooks.localized.count", "hook.ui.localized", "hook.ui.localized.counts", "hook..count", string.Empty, "hooks.count.total" })
                Check(b.Ler(chave).Status == "AUSENTE", "chave fora do vocabulario: " + chave);
            Check(b.Ler("hooks.unknown").Value == "0");
        },

        ["P10"] = () =>
        {
            using var b = new Bancada();
            b.Ligar();
            b.Notificar("ui.localized", new object?[] { "curto" }, new string('x', 10000));
            Check(b.Testemunha.Eventos.Count == 1, "EventV1 aceito: nada de ArgumentException");
            var dados = b.Testemunha.Eventos[0].Data;
            Check(dados.Length <= 4096, "Data<=4096: " + dados.Length);
            Check(dados.Contains("TRUNCADO"), "marcador de truncamento presente");
            Check(dados.Length >= 4000, "truncamento nao e maior do que o necessario: " + dados.Length);
            Check(dados.Contains("curto"), "o comeco do dado sobrevive");
            Check(b.Diagnostico.Count == 0, "nenhuma excecao engolida");
        },

        ["P11"] = () =>
        {
            using var b = new Bancada();
            b.Ligar();
            var argumentos = new object?[] { "ORIGINAL-A" };
            b.Notificar("ui.localized", argumentos, "r1");
            var dados1 = b.Testemunha.Eventos[0].Data;
            argumentos[0] = "MUTADO-A";
            b.Notificar("ui.localized", new object?[] { "DOIS-B" }, "r2");
            Check(b.Testemunha.Eventos.Count == 2);
            Check(b.Testemunha.Eventos[0].Data == dados1, "o Data ja publicado nao muda");
            Check(dados1.Contains("ORIGINAL-A") && !dados1.Contains("MUTADO-A"), "copia da lista (Contracts.cs:76): " + dados1);
            Check(b.Testemunha.Eventos[1].Data.Contains("DOIS-B"), "cada evento resume os SEUS argumentos: " + b.Testemunha.Eventos[1].Data);
            Check(!b.Testemunha.Eventos[1].Data.Contains("ORIGINAL-A"), "sem referencia viva entre eventos");
        },

        ["P12"] = () =>
        {
            var relatos = 0;
            using (var b = new Bancada())
            {
                b.Ligar(() => throw new InvalidOperationException("SEGREDO_P12_NAO_DEVE_VAZAR"));
                var tarefa = Task.Run(() =>
                {
                    for (var i = 0; i < 3; i++)
                        Producao.Publicar(b.Sinal, Producao.Notificacao("ui.localized", null, new object?[] { "t" }, "r"), _ => Interlocked.Increment(ref relatos));
                });
                Check(tarefa.Wait(2000), "OnEvent de outro thread nao pode travar (limite 2s)");
                Check(relatos == 0, "excecao do adaptador NAO chega ao canal do produtor");
                Check(b.Testemunha.Eventos.Count == 0, "host que falha = inativo (fail-closed)");
                Check(b.Diagnostico.Any(d => d.Contains("InvalidOperationException")), "canal de diagnostico guarda o TIPO");
                Check(!string.Join("|", b.Diagnostico).Contains("SEGREDO_P12_NAO_DEVE_VAZAR"), "a mensagem do host nao vaza");
            }
            using (var c = new Bancada())
            {
                c.Ligar();
                var tarefa = Task.Run(() =>
                {
                    for (var i = 0; i < 5; i++) Producao.Publicar(c.Sinal, Producao.Notificacao("game.awake", null, new object?[0], null));
                });
                Check(tarefa.Wait(2000), "publicacao de outro thread nao trava");
                Check(c.Testemunha.Eventos.Count == 5, "entregou as 5");
                Check(c.Registry.Read(Id, "hooks.count").Value == "5", "contador consistente entre threads");
            }
        },

        ["P13"] = () =>
        {
            using var a = new Bancada(comTestemunha: false);
            var ruim = new Testemunha { AoReceber = _ => throw new Exception("SEGREDO_DO_KIT_13") };
            using var leaseRuim = a.Registry.Register("testemunha.ruim", RegistryV1.ApiVersion, ruim);
            var boa = new Testemunha();
            using var leaseBoa = a.Registry.Register("testemunha.boa", RegistryV1.ApiVersion, boa);
            a.Ligar();
            a.Notificar("ui.localized", new object?[] { "t" }, "r");
            Check(boa.Eventos.Count == 1, "o adaptador continua entregando as demais");
            var diarioDoKit = string.Join("|", a.Registry.Diagnostics());
            Check(diarioDoKit.Contains("evento") && diarioDoKit.Contains("Exception"), "kit guarda o TIPO: " + diarioDoKit);
            Check(!diarioDoKit.Contains("SEGREDO_DO_KIT_13"), "kit nao guarda a mensagem");
            Check(a.Diagnostico.Count == 0, "quem isola e o kit: o adaptador nao viu excecao");

            using var c = new Bancada();
            c.Ligar(() => throw new InvalidOperationException("SEGREDO_HOST_13"));
            c.Notificar("ui.localized", new object?[] { "t" }, "r");
            Check(c.Testemunha.Eventos.Count == 0, "host que falha nao publica");
            Check(c.Diagnostico.Count == 1, "uma entrada de diagnostico: " + c.Diagnostico.Count);
            Check(c.Diagnostico[0].Contains("InvalidOperationException"), "guarda o TIPO: " + c.Diagnostico[0]);
            Check(!c.Diagnostico[0].Contains("SEGREDO_HOST_13"), "nao guarda a mensagem");
            Check(c.Diagnostico[0].Length <= 512, "limitado por entrada");
            for (var i = 0; i < 100; i++) c.Notificar("ui.localized", new object?[] { "t" }, "r");
            Check(c.Diagnostico.Count == 64, "canal limitado (espelha RegistryV1.cs:81): " + c.Diagnostico.Count);
        },

        ["P14"] = () =>
        {
            using var b = new Bancada();
            var ponte = b.Ligar();
            b.Notificar("ui.localized", new object?[] { "a" }, "r");
            Check(b.Testemunha.Eventos.Count == 1);
            var registrosAntes = b.Registry.Count;
            ponte.Dispose();
            ponte.Dispose();
            Check(b.Registry.Count == registrosAntes - 1, "lease liberado");
            Check(b.Registry.Read(Id, "hooks.count").Status == "AUSENTE", "extensao fora do registro");
            for (var i = 0; i < 3; i++) b.Notificar("ui.localized", new object?[] { "a" }, "r");
            Check(b.Testemunha.Eventos.Count == 1, "assinatura removida: zero eventos novos");
            // Chamada DIRETA no adaptador ja descartado: existe corrida real — o Signal tira um SNAPSHOT
            // dos handlers (Contracts.cs:93), entao um Publish em voo pode chamar o callback depois do
            // Dispose. Sem a guarda, o adaptador publicaria sem lease.
            ponte.OnEvent(Producao.Notificacao("ui.localized", null, new object?[] { "a" }, "r"));
            Check(b.Testemunha.Eventos.Count == 1, "OnEvent direto depois do Dispose nao entrega");
            Check(ponte.Read("hooks.count").Value == "1", "contador nao cresce depois do Dispose");
            b.Ponte = null;
        },

        ["P15"] = () =>
        {
            using var a = new Bancada(comTestemunha: false);
            var reentrante = new Testemunha { AoReceber = _ => a.Registry.Publish(new EventV1(Sessao, 0, "reentrante", "eco")) };
            using var lease1 = a.Registry.Register("testemunha.reentrante", RegistryV1.ApiVersion, reentrante);
            var observadora = new Testemunha();
            using var lease2 = a.Registry.Register("testemunha.b", RegistryV1.ApiVersion, observadora);
            a.Ligar();
            a.Notificar("ui.localized", new object?[] { "t" }, "r");
            Check(observadora.Eventos.Count == 1, "sem publicacao aninhada pelo kit");
            var diarioDoKit = string.Join("|", a.Registry.Diagnostics());
            Check(diarioDoKit.Contains("InvalidOperationException"), "EVENTO_REENTRANTE registrado pelo kit: " + diarioDoKit);
            Check(a.Diagnostico.Count == 0, "o kit isolou: nada chegou ao adaptador");

            using var c = new Bancada(comTestemunha: false);
            var relatos = 0;
            var gatilho = new Testemunha
            {
                AoReceber = _ => Producao.Publicar(c.Sinal, Producao.Notificacao("game.awake", null, new object?[0], null), _ => Interlocked.Increment(ref relatos))
            };
            using var lease3 = c.Registry.Register("testemunha.gatilho", RegistryV1.ApiVersion, gatilho);
            var observador = new Testemunha();
            using var lease4 = c.Registry.Register("testemunha.observador", RegistryV1.ApiVersion, observador);
            c.Ligar();
            Producao.Publicar(c.Sinal, Producao.Notificacao("ui.localized", null, new object?[] { "t" }, "r"), _ => Interlocked.Increment(ref relatos));
            Check(relatos == 0, "o adaptador nao lanca para o log do produtor");
            Check(c.Diagnostico.Any(d => d.Contains("InvalidOperationException")), "o adaptador nao engole a excecao do kit: registra o TIPO (" + string.Join("|", c.Diagnostico) + ")");
            Check(observador.Eventos.Count == 1, "uma entrega so: sem recirculacao");
        },

        ["P16"] = () =>
        {
            using var b = new Bancada();
            var relatos = 0;
            b.Ponte = RealmHooksBinding.Create(b.Registry, RealmHooks.Observed, () => b.ProdutorAtivo, () => b.SessaoDeclarada, b.Diagnostico.Add);
            Producao.Emitir("ui.localized", null, new object?[] { "hello" }, "localized:hello", _ => Interlocked.Increment(ref relatos));
            Check(b.Testemunha.Eventos.Count == 1, "caminho do produtor (RealmHooks.Emit -> RealmHooks.Observed) entrega");
            Check(b.Testemunha.Eventos[0].Kind == "ui.localized" && b.Testemunha.Eventos[0].Session == Sessao);
            Check(b.Testemunha.Eventos[0].Data.Contains("localized:hello"), "resultado string no resumo");
            Check(relatos == 0, "nada lancou no canal do produtor");
            Check(b.Registry.Read(Id, "hooks.count").Value == "1");
        },

        ["P17"] = () =>
        {
            // Entregavel B: o caminho de CONSUMO do AUT4Probe (companheiro -> testemunha -> gatilho do
            // instrumento) roda offline: nem o companheiro nem a ponte tocam Unity/BepInEx.
            var recebidos = new List<string>();
            var ativo = true;
            var ligacao = Gumatos.KitApiBridge.AUT4.PonteAut4.Ligar(
                texto => { lock (recebidos) recebidos.Add(texto); }, () => Sessao, () => ativo);
            Producao.Emitir("ui.localized", null, new object?[] { "hello" }, "localized:hello");
            Check(recebidos.Count == 1, "o instrumento recebeu o gatilho: " + recebidos.Count);
            Check(recebidos[0].StartsWith("ui.localized|", StringComparison.Ordinal), "gatilho com o HookId: " + recebidos[0]);
            Check(recebidos[0].Contains("quadro=0"), "quadro ordinal no gatilho: " + recebidos[0]);
            Producao.Emitir("game.desconhecido", null, new object?[0], null);
            Check(recebidos.Count == 1, "hook fora do catalogo nao vira gatilho");
            ativo = false;
            Producao.Emitir("ui.localized", null, new object?[] { "x" }, "y");
            Check(recebidos.Count == 1, "produtor inativo nao vira gatilho");
            ativo = true;
            ligacao.Dispose();
            ligacao.Dispose();
            Producao.Emitir("ui.localized", null, new object?[] { "z" }, "w");
            Check(recebidos.Count == 1, "Dispose desliga o gatilho");
            Check(((Gumatos.KitApiBridge.AUT4.PonteAut4.Ligacao)ligacao).Diagnostics().Length == 0, "sem diagnostico na operacao normal");
        }
    };

    private static int Main(string[] args)
    {
        var filtro = args.Length > 0 && args[0] != "todos" ? args[0] : null;
        var destino = args.Length > 1 ? args[1] : "evidencia-api-bridge.json";
        var testes = Testes();
        var resultados = new List<object>();
        var falhas = 0;
        var contagem = 0;
        foreach (var teste in testes.Where(p => filtro == null || p.Key == filtro))
        {
            contagem++;
            try { teste.Value(); Console.WriteLine("PASS|" + teste.Key); resultados.Add(new { teste = teste.Key, status = "PASS" }); }
            catch (Exception erro)
            {
                falhas++;
                Console.WriteLine("FAIL|" + teste.Key + "|" + erro.GetType().Name + "|" + erro.Message);
                resultados.Add(new { teste = teste.Key, status = "FAIL", erro = erro.GetType().Name, mensagem = erro.Message });
            }
        }
        if (contagem == 0) { Console.WriteLine("NAO_EXERCITADO: caso ausente"); return 2; }
        var evidencia = JsonSerializer.Serialize(new
        {
            esquema = "INT-R1-C2-I1/api-bridge-harness/1",
            sessao = Sessao,
            offline = true,
            runtime_do_jogo = "NAO_EXERCITADO",
            filtro,
            contagem,
            falhas,
            testes = resultados,
            instrumentacao_declarada = "injecao pelo membro interno do produtor (HookNotification..ctor, Signal<T>.Publish, RealmHooks.Emit) via reflexao: api/ esta congelado neste cartao",
            nao_exercitado = new[]
            {
                "Harmony real (HookInstallation.Install) e postfix no Assembly-CSharp",
                "BepInEx carregando RealmApi.dll com EnableHooks=true",
                "Adaptador dentro do processo do jogo"
            }
        }, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(destino, evidencia);
        Console.WriteLine($"Ran {contagem} tests; failures={falhas}; OFFLINE_ONLY");
        Console.WriteLine("evidencia: " + Path.GetFullPath(destino));
        return falhas == 0 ? 0 : 1;
    }
}
