using System;
using BetterPortuguese.Core;

internal static class StatusTests
{
    private static void Check(bool yes, string message = "BP-COMP-STATUS assertion") { if (!yes) throw new Exception(message); }

    private static void Same(string incoming, string expected, string label)
    {
        string result = StatusAgreement.Compose(incoming, out string reason);
        Check(result == expected, label + ": veio " + Quote(result) + " esperado " + Quote(expected));
        if (result != incoming) Check(reason != null && reason.StartsWith("feminino:", StringComparison.Ordinal), label + ": motivo inesperado " + Quote(reason));
        if (result == incoming) Check(result == incoming && StatusAgreement.Compose(result, out _) == result, label + ": nao e idempotente");
    }

    private static string Quote(string text) => text == null ? "<null>" : "\"" + text + "\"";

    public static void Run(Action<string, Action> test)
    {
        // Casos vistos em jogo (runs 01-06): o sufixo vem de LANG-08944 e o nome nao tem marca de genero.
        Same("Proteção Elemental Aplicado", "Proteção Elemental Aplicada", "protecao elemental");
        Same("Resistência ao Controle Aplicado", "Resistência ao Controle Aplicada", "resistencia ao controle");
        Same("Fúria de Batalha Aplicado", "Fúria de Batalha Aplicada", "furia de batalha");
        Same("Terra Ardente Aplicado", "Terra Ardente Aplicada", "terra ardente");
        Same("Aura do Conquistador Aplicado", "Aura do Conquistador Aplicada", "aura do conquistador");

        // CONTROLE NEGATIVO: masculinos e invariantes NAO podem mudar (120 de 154 ocorrencias reais).
        foreach (string masculino in new[] { "Indestrutível Aplicado", "Calor Aplicado", "Chocado Aplicado", "Reunir Aplicado", "Veneno Aplicado" })
            Same(masculino, masculino, "masculino intacto " + masculino);

        // Pilha " x2"/" x12" fica antes do sufixo, na posicao original.
        Same("Proteção Elemental x2 Aplicado", "Proteção Elemental x2 Aplicada", "pilha x2");
        Same("Aura de Energia x12 Aplicado", "Aura de Energia x12 Aplicada", "pilha x12");

        // Marcacao <color>/<b>: preserva abertura e fechamento, troca so o sufixo.
        Same("<color=#00FFFF>Proteção Elemental Aplicado</color>", "<color=#00FFFF>Proteção Elemental Aplicada</color>", "cor em volta");
        Same("<b>Maldição Aplicado</b>", "<b>Maldição Aplicada</b>", "negrito em volta do sufixo");

        // Formato nao previsto (tag de fechamento NO MEIO, antes do sufixo): fica intacto de proposito.
        Same("<b>Maldição</b> Aplicado", "<b>Maldição</b> Aplicado", "tag no meio nao e tocada");

        // Formatos nao previstos voltam intactos, com motivo.
        foreach (string estranho in new[] { "Proteção Elemental", "Proteção Elemental Aplicada", "Aplicado", "x Aplicado",
                                            "<color=#fff>Proteção <b>Elemental</b> Aplicado</color>", "Proteção Elemental Aplicado!" })
            Same(estranho, estranho, "fora do padrao " + estranho);

        test("BP-COMP-STATUS texto nulo nao lanca", () =>
        {
            Check(StatusAgreement.Compose(null, out string reason) == null && reason != null);
        });

        // Anti-regra: a troca GLOBAL (o que o cartao proibe) quebraria estes casos. A tabela nao os toca.
        test("BP-COMP-STATUS anti-regra da troca global", () =>
        {
            foreach (string caso in new[] { "Indestrutível Aplicado", "Calor Aplicado", "Reunir Aplicado" })
                Check(StatusAgreement.Compose(caso, out _) == caso);
            Check(StatusAgreement.Compose("Indestrutível Aplicado", out _) != "Indestrutível Aplicada");
        });
    }
}
