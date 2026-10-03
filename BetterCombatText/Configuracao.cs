using System;
using BepInEx.Configuration;
using UnityEngine;

namespace BetterCombatText
{
    /// <summary>
    /// O FUNDO atras do texto, para a sombra ser escolhida pelo CONTRASTE COM ELE (BCT-3).
    ///
    /// <para><b>Por que existe:</b> o BCT-2 escolhia a sombra pela luminancia da LETRA. O dono
    /// relatou em 02/10 que <b>nao via sombra nenhuma</b> nos nomes de inimigo: a letra do nome e
    /// CLARA e o campo de batalha do Stolen Realm e ESCURO, entao a sombra saia <c>#000000</c> —
    /// preto sobre escuro, contraste zero. Um drop shadow so aparece quando contrasta com o que
    /// esta atras dele; quem manda e o FUNDO, nao a letra.</para>
    /// </summary>
    internal enum FundoSombra
    {
        /// <summary>Nao declarado: a sombra segue a luminancia da LETRA (a regra do BCT-2).</summary>
        Auto,

        /// <summary>Cenario ESCURO (o campo de batalha): a sombra visivel e a CLARA.</summary>
        Escuro,

        /// <summary>Cenario CLARO: a sombra visivel e a ESCURA.</summary>
        Claro,
    }

    /// <summary>
    /// Todas as chaves do .cfg do mod, num lugar so. Nada aqui toca o jogo: so le o arquivo
    /// (<c>BepInEx/config/com.gumatos.bettercombattext.cfg</c>) e guarda os valores.
    ///
    /// <para><b>Falha-segura:</b> qualquer chave invalida (hex torto, numero fora de faixa) cai
    /// num clamp/valor padrao e NAO derruba o plugin — quem chama passa por try/catch.</para>
    /// </summary>
    internal sealed class Configuracao
    {
        // ---------------- 1. Geral ----------------
        public readonly ConfigEntry<bool> Ativar;
        public readonly ConfigEntry<bool> LogDetalhado;
        public readonly ConfigEntry<bool> DiagnosticoArranque;

        // -------- 1. Geral: sombra ADAPTATIVA (BCT-2) --------
        // Chaves NOVAS. Com SombraAdaptativa=false o mod volta EXATAMENTE ao
        // comportamento FIXO antigo (sombra = cor do contorno). Procedencia das
        // cores: tools/testes/fixtures/cores-do-jogo.entrada.json.
        public readonly ConfigEntry<bool> SombraAdaptativa;
        public readonly ConfigEntry<string> CorSombraClaraHex;
        public readonly ConfigEntry<string> CorSombraEscuraHex;

        // ---------------- 2. Nomes de inimigos em combate (TMP) ----------------
        public readonly EstiloTmpCfg Nomes;

        // ---------------- 3. Rotulos/stacks de buff e debuff (UI.Text legado) ----------------
        public readonly EstiloTextoLegadoCfg Rotulos;

        // ---------------- 4. Texto do dado nos eventos (TMP) ----------------
        public readonly EstiloTmpCfg EventosDado;
        public readonly ConfigEntry<bool> EventosAtivar;

        // ---------------- 5. Extra ----------------
        public readonly EstiloTmpCfg NumeroDeVida;
        public readonly ConfigEntry<bool> AplicarNumeroDeVida;

        // ---------------- 6. Tooltip de status (nome do buff/debuff) ----------------
        public readonly EstiloTmpCfg TooltipStatus;
        public readonly ConfigEntry<bool> TooltipAtivar;

        public Configuracao(ConfigFile cfg)
        {
            Ativar = cfg.Bind("1. Geral", "Ativar", true,
                "CHAVE MESTRA. Coloque false para o mod nao alterar NADA (nem material, nem fonte, " +
                "nem contorno). E a unica linha que voce precisa mudar para desligar tudo.");
            LogDetalhado = cfg.Bind("1. Geral", "LogDetalhado", false,
                "true = escreve uma linha no LogOutput.log a cada superficie tratada (util para diagnostico). " +
                "false = so o resumo de arranque e os avisos.");
            DiagnosticoArranque = cfg.Bind("1. Geral", "DiagnosticoNoArranque", true,
                "true (padrao) = UMA vez no arranque o mod procura os componentes alvo em cena e escreve no " +
                "log a fonte, o material compartilhado e o shader de cada um — 100% leitura, nada e alterado. " +
                "E por esse bloco que se sabe o que o jogo usa de verdade. Custo: uma varredura de cena por " +
                "passo (5s) ate achar um alvo ou ate 240s. false = nenhuma varredura de cena acontece " +
                "(custo zero) e o log so registra que o diagnostico esta desligado. Ligue para testar, " +
                "desligue para jogar sem ele.");

            // --- Sombra ADAPTATIVA (BCT-2, pedido do dono 02/10; CORRIGIDA no BCT-4) ----------
            // A sombra CLARA e o BRANCO PURO (#FFFFFF). O padrao ANTIGO era o #CBB396 — que e a
            // PROPRIA cor de texto do jogo (specialDescColor/highlightedColor) e a cor comum do
            // nome do inimigo: a sombra saia IGUAL a letra (contraste zero — o defeito de 02/10).
            // A sombra ESCURA e o preto neutro (#000000). A leitura e a luminancia da cor REAL da
            // letra (Color.grayscale: 0.299R + 0.587G + 0.114B).
            SombraAdaptativa = cfg.Bind("1. Geral", "SombraAdaptativa", true,
                "true (padrao) = sombra ADAPTATIVA: o mod le a cor da letra e escolhe a sombra " +
                "pela luminancia - letra ESCURA ganha sombra CLARA e letra CLARA ganha sombra " +
                "ESCURA. false = comportamento FIXO antigo (a sombra e sempre a cor do contorno, " +
                "independente da letra).");
            CorSombraClaraHex = cfg.Bind("1. Geral", "CorSombraClara", "FFFFFF",
                "Cor (RRGGBB, sem #) da sombra CLARA. Padrao FFFFFF = branco puro. O #CBB396 " +
                "era a PROPRIA cor de texto do jogo (highlightedColor/specialDescColor) e a sombra " +
                "clara ficava igual a letra do inimigo (invisivel/blob) — por isso o branco. A " +
                "sombra so sai clara quando ELA contrasta com a letra (a lei do contraste). " +
                "So vale com SombraAdaptativa = true.");
            CorSombraEscuraHex = cfg.Bind("1. Geral", "CorSombraEscura", "000000",
                "Cor (RRGGBB, sem #) da sombra para letra CLARA (luminancia >= 0.5). Padrao " +
                "000000 = preto neutro (o padrao de sempre). So vale com SombraAdaptativa = true.");

            var secNomes = "2. Nomes de inimigos (combate)";
            // BCT-3: o dono confirmou em 02/10 que o CAMPO DE BATALHA e ESCURO ("nao ve nenhuma
            // sombra nos nomes"). Como o nome do inimigo e uma cor CLARA, o BCT-2 (sombra pela
            // luminancia da LETRA) dava sombra #000000 - invisivel ali. Declarando o fundo ESCURO,
            // a sombra passa a ser a CLARA. BCT-4: a sombra clara e o BRANCO (#FFFFFF) e nao o
            // #CBB396 (que era a PROPRIA cor da letra do inimigo -> blob). BCT-5: o FUNDO so
            // PROPÕE a polaridade — o VETO DA LETRA (Configuracao.UsaSombraClara) manda: a letra
            // #CBB396 e CLARA, entao a sombra sai ESCURA (#000000), que CONTRASTA com a fonte,
            // como o dono pediu. O alfa subiu de 0.35 para 0.65: a sombra escura a 35% sobre o
            // campo era fraca demais para se ver (era o "sombra da mesma cor da fonte": a sombra
            // translucida se confundia com o proprio glifo). O CONTORNO continua leve (alfa 0.10)
            // — ele nao e a sombra.
            Nomes = new EstiloTmpCfg(cfg, secNomes,
                haloAtivo: true,
                largura: 0.22f,
                suavidade: 0.05f,
                corHex: "000000",
                alfa: 0.95f,
                sombraAtiva: true,
                sombraOffX: 0.35f,
                sombraOffY: -0.35f,
                sombraDilate: 0.00f,
                sombraSuavidade: 0.05f,
                alfaSombra: 0.75f,
                tamanhoExtra: 0f,
                fundo: "escuro");

            var secRotulos = "3. Rotulos de buff/debuff (combate)";
            Rotulos = new EstiloTextoLegadoCfg(cfg, secRotulos,
                haloAtivo: true,
                raio: 1.0f,
                corHex: "000000",
                alfa: 0.10f,
                sombraAtiva: true,
                sombraOffX: 1.0f,
                sombraOffY: -1.0f,
                alfaSombra: 0.50f,
                negrito: true,
                tamanhoExtra: 0f,
                fundo: "auto");

            var secDado = "4. Eventos (texto do dado)";
            EventosAtivar = cfg.Bind(secDado, "Ativar", true,
                "Liga/desliga SO o realce do texto do dado nos eventos de rolagem. " +
                "Independente do resto: desligar aqui nao mexe no combate.");
            EventosDado = new EstiloTmpCfg(cfg, secDado,
                haloAtivo: true,
                largura: 0.12f,
                suavidade: 0.60f,
                corHex: "000000",
                alfa: 0.35f,
                sombraAtiva: true,
                sombraOffX: 0.10f,
                sombraOffY: -0.10f,
                sombraDilate: 0.10f,
                sombraSuavidade: 0.50f,
                alfaSombra: 0.40f,
                tamanhoExtra: 0f,
                fundo: "auto");

            var secExtra = "5. Extra";
            AplicarNumeroDeVida = cfg.Bind(secExtra, "AplicarNoNumeroDeVida", false,
                "Opcional: aplica o mesmo halo no numero de vida que flutua sobre as unidades em combate " +
                "(l.210529 Healthbar.healthbarText). Desligado por padrao — fora do pedido original.");
            NumeroDeVida = new EstiloTmpCfg(cfg, secExtra + " (numero de vida)",
                haloAtivo: true,
                largura: 0.10f,
                suavidade: 0.60f,
                corHex: "000000",
                alfa: 0.10f,
                sombraAtiva: false,
                sombraOffX: 0.10f,
                sombraOffY: -0.10f,
                sombraDilate: 0.10f,
                sombraSuavidade: 0.50f,
                alfaSombra: 0.30f,
                tamanhoExtra: 0f,
                fundo: "auto");

            // ---------------------------------------------------------------------------
            //  6. Tooltip de status. DESLIGADO por padrao de proposito:
            //  o nome do buff/debuff so aparece no tooltip generico do jogo
            //  (Tooltip.ShowActionStatusTooltip, l.213903 -> ShowTooltip(...) l.213952), e o
            //  Tooltip.Title/Description (l.212957/212965) e O MESMO componente usado pelos
            //  tooltips de skill, item e powerup. Ligar aqui instancia o material DESSES
            //  componentes e o halo passa a valer para TODOS os tooltips do jogo — fora do
            //  pedido ("efeito so nos textos alvo"). Quem quiser, liga sabendo disso.
            // ---------------------------------------------------------------------------
            var secTooltip = "6. Tooltip de status (nome do buff/debuff)";
            TooltipAtivar = cfg.Bind(secTooltip, "Ativar", false,
                "DESLIGADO por padrao. O nome do buff/debuff nao tem rotulo proprio em combate: ele so " +
                "aparece no tooltip generico do jogo, e o componente que o desenha (Tooltip.Title/Description) " +
                "e o MESMO dos tooltips de skill/item/powerup. Ligando, o halo tambem aparece nesses tooltips. " +
                "Com false, nada e tocado.");
            TooltipStatus = new EstiloTmpCfg(cfg, secTooltip,
                haloAtivo: true,
                largura: 0.10f,
                suavidade: 0.60f,
                corHex: "000000",
                alfa: 0.10f,
                sombraAtiva: true,
                sombraOffX: 0.10f,
                sombraOffY: -0.10f,
                sombraDilate: 0.10f,
                sombraSuavidade: 0.50f,
                alfaSombra: 0.35f,
                tamanhoExtra: 0f,
                fundo: "auto");
        }

        /// <summary>Le "RRGGBB" (aceita "#RRGGBB") com alfa separado, em try/catch.</summary>
        internal static Color HexComAlfa(string hex, float alfa)
        {
            var c = Color.black;
            try
            {
                var s = (hex ?? "").Trim().TrimStart('#');
                if (s.Length == 6)
                {
                    int r = Convert.ToInt32(s.Substring(0, 2), 16);
                    int g = Convert.ToInt32(s.Substring(2, 2), 16);
                    int b = Convert.ToInt32(s.Substring(4, 2), 16);
                    c = new Color(r / 255f, g / 255f, b / 255f, 1f);
                }
            }
            catch
            {
                // hex invalido -> preto (nunca derruba)
                c = Color.black;
            }
            c.a = Mathf.Clamp01(alfa);
            return c;
        }

        // ============================================================================
        //  SOMBRA ADAPTATIVA (BCT-2) - a regra PURA
        //
        //  A luminancia e exatamente a `Color.grayscale` do Unity
        //  (0.299R + 0.587G + 0.114B). O limiar 0.5 divide a paleta do jogo como o dono
        //  decidiu (procedencia: tools/testes/fixtures/cores-do-jogo.entrada.json):
        //
        //    luminancia <  0.5  -> letra ESCURA -> sombra CLARA  (CorSombraClara, #FFFFFF)
        //    luminancia >= 0.5  -> letra CLARA  -> sombra ESCURA (CorSombraEscura, #000000)
        //
        //  BCT-4: a sombra CLARA era o #CBB396 — que e a PROPRIA cor de texto do jogo e a cor
        //  comum do nome do inimigo. A sombra saia IGUAL a letra. Agora e o BRANCO PURO, e a lei
        //  `ContrasteComALetra < ContrasteMinimo` vira o balde quando a cor escolhida nao
        //  contrasta com a LETRA (ver `UsaSombraClara`).
        //
        //  Tabela medida (fixture, 02/10): caem na sombra CLARA apenas o `shadowColor`
        //  #F000FF (0.395, magenta escuro); ficam na sombra ESCURA o `fireColor` #FF5353
        //  (0.527), `coldColor` #00D7FF (0.609), `manaColor` #66A8FF (0.620),
        //  `healingColor` #6BFF6F (0.762), `lightningColor` #EFFF00 (0.867),
        //  `neutralColor` #F4FF00 (0.873), `highlightedColor` #CBB396 (0.717),
        //  `positiveColor` #64FF6A (0.752), `negativeColor` #FF5353 (0.527) e
        //  `physicalColor` #FFFFFF (1.000).
        // ============================================================================

        /// <summary>Limiar de luminancia que separa letra ESCURA de letra CLARA (BCT-2).</summary>
        internal const float LimiarLuminancia = 0.5f;

        /// <summary>
        /// BCT-4 — CONTRASTE MINIMO entre a luminancia da LETRA e a da sombra escolhida. Abaixo
        /// disto as duas cores sao "a mesma cor" para o olho e a sombra vira um blob/invisivel —
        /// foi o defeito relatado em 02/10: o nome do inimigo tem letra <c>#CBB396</c> e a sombra
        /// do balde claro tambem saia <c>#CBB396</c> (a MESMA cor).
        /// </summary>
        internal const float ContrasteMinimo = 0.2f;

        /// <summary>A luminancia da cor, igual a <c>Color.grayscale</c> do Unity.</summary>
        internal static float Luminancia(Color c)
        {
            return 0.299f * c.r + 0.587f * c.g + 0.114f * c.b;
        }

        /// <summary>BCT-4: o quanto a sombra <paramref name="sombra"/> contrasta com a
        /// <paramref name="corLetra"/> (a diferenca das luminancias — 0 = mesma cor).</summary>
        internal static float ContrasteComALetra(Color corLetra, Color sombra)
        {
            return Mathf.Abs(Luminancia(corLetra) - Luminancia(sombra));
        }

        /// <summary>true = a cor e uma letra ESCURA (luminancia abaixo do limiar) -> sombra clara.</summary>
        internal static bool LetraEscura(Color c)
        {
            return Luminancia(c) < LimiarLuminancia;
        }

        /// <summary>Le o valor do config ("auto"/"escuro"/"claro") no enum do FUNDO (BCT-3).</summary>
        internal static FundoSombra FundoSombraDe(string valor)
        {
            switch ((valor ?? "").Trim().ToLowerInvariant())
            {
                case "escuro":
                    return FundoSombra.Escuro;
                case "claro":
                    return FundoSombra.Claro;
                default:
                    return FundoSombra.Auto; // inclui "auto" e qualquer valor invalido
            }
        }

        /// <summary>
        /// A sombra CLARA e a que aparece? (BCT-3/BCT-4/BCT-5) O FUNDO <b>propoe</b> a polaridade
        /// (num fundo ESCURO a sombra escura teria contraste zero com ele; num fundo claro, e a
        /// clara que some) e, sem fundo declarado (<see cref="FundoSombra.Auto"/>), vale a
        /// luminancia da LETRA (a regra do BCT-2).
        ///
        /// <para><b>BCT-5 — O VETO DA LETRA (o conserto de 02/10, a SEGUNDA rodada):</b> a proposta
        /// do fundo CAI quando ela poe a sombra do <b>MESMO lado</b> da luminancia da letra. A lei
        /// do dono e o CONTRASTE COM A FONTE: <b>fonte CLARA -> sombra ESCURA; fonte ESCURA ->
        /// sombra CLARA</b>. Era por isso que a sombra do nome do inimigo continuava "da mesma cor
        /// da fonte": a letra e CLARA (<c>#CBB396</c>, luminancia 0.717) e o fundo escuro mandava a
        /// sombra CLARA — <c>#CBB396</c> (o valor que o <c>.cfg</c> herdou de um build antigo) ou
        /// <c>#FFFFFF</c> (o default do codigo). O BCT-4 tentava pegar isso por um LIMIAR (0.2),
        /// mas bege <c>#CBB396</c> contra branco <c>#FFFFFF</c> difere so 0.283 — passava, e a
        /// sombra saia CLARA sobre uma fonte CLARA. Aqui nao ha limiar que decida: o LADO decide.
        /// Só entao a lei numerica do BCT-4 (<see cref="ContrasteMinimo"/>) age, como rede de
        /// seguranca contra um balde mal configurado.</para>
        /// </summary>
        internal static bool UsaSombraClara(Color corLetra, Color clara, Color escura, FundoSombra fundo)
        {
            bool usarClara;
            switch (fundo)
            {
                case FundoSombra.Escuro:
                    usarClara = true;      // BCT-3: fundo escuro -> sombra CLARA
                    break;
                case FundoSombra.Claro:
                    usarClara = false;     // BCT-3: fundo claro  -> sombra ESCURA
                    break;
                default:
                    usarClara = LetraEscura(corLetra);   // auto: a regra do BCT-2 (luminancia da LETRA)
                    break;
            }

            // BCT-5 — O VETO DA LETRA: a sombra tem de ficar do LADO OPOSTO da luminancia da
            // letra. Se a proposta do fundo poe a sombra do MESMO lado (clara-sobre-clara ou
            // escura-sobre-escura), ela VIRA. E a lei do dono: fonte CLARA -> sombra ESCURA.
            if (usarClara != LetraEscura(corLetra))
            {
                usarClara = !usarClara;
            }

            // BCT-4 — a LEI numerica: se ainda assim a cor escolhida nao contrastar com a LETRA e
            // o outro balde contrastar MAIS, o outro vence (rede contra um balde mal configurado).
            Color escolhida = usarClara ? clara : escura;
            Color oposta = usarClara ? escura : clara;
            if (ContrasteComALetra(corLetra, escolhida) < ContrasteMinimo
                && ContrasteComALetra(corLetra, oposta) > ContrasteComALetra(corLetra, escolhida))
            {
                usarClara = !usarClara;
            }
            return usarClara;
        }

        /// <summary>
        /// A REGRA de escolha da sombra, isolada e sem efeito colateral (BCT-2/BCT-3/BCT-4).
        /// Com <paramref name="adaptativa"/> = false devolve a cor FIXA antiga
        /// (<paramref name="fixa"/>) — o comportamento de antes da tarefa. Com true escolhe
        /// entre <paramref name="clara"/> e <paramref name="escura"/> por
        /// <see cref="UsaSombraClara"/>: o FUNDO declarado manda na POLARIDADE (BCT-3),
        /// sem fundo declarado vale a luminancia da LETRA (BCT-2) e, em qualquer caso, o balde
        /// VIRA se a cor escolhida nao contrastar com a LETRA (a lei do BCT-4). O alfa e sempre o
        /// da secao (<paramref name="alfa"/>).
        /// </summary>
        internal static Color CorSombraAdaptativa(Color corLetra, bool adaptativa, Color fixa,
            float alfa, Color clara, Color escura, FundoSombra fundo = FundoSombra.Auto)
        {
            Color escolhida = adaptativa
                ? (UsaSombraClara(corLetra, clara, escura, fundo) ? clara : escura)
                : fixa;
            escolhida.a = Mathf.Clamp01(alfa);
            return escolhida;
        }

        /// <summary>Sombra clara, ainda sem alfa - o alfa vem da secao.</summary>
        public Color CorSombraClara => HexComAlfa(CorSombraClaraHex.Value, 1f);

        /// <summary>Sombra escura (letra clara), ainda sem alfa - o alfa vem da secao.</summary>
        public Color CorSombraEscura => HexComAlfa(CorSombraEscuraHex.Value, 1f);
    }

    /// <summary>Faixa de ajuste comum as superficies TMP (distance field).</summary>
    internal sealed class EstiloTmpCfg
    {
        public readonly ConfigEntry<bool> HaloAtivo;
        public readonly ConfigEntry<float> LarguraContorno;
        public readonly ConfigEntry<float> SuavidadeContorno;
        public readonly ConfigEntry<string> CorContornoHex;
        public readonly ConfigEntry<float> AlfaContorno;
        public readonly ConfigEntry<bool> SombraAtiva;
        public readonly ConfigEntry<float> SombraOffsetX;
        public readonly ConfigEntry<float> SombraOffsetY;
        public readonly ConfigEntry<float> SombraDilate;
        public readonly ConfigEntry<float> SombraSuavidade;
        public readonly ConfigEntry<float> AlfaSombra;
        public readonly ConfigEntry<float> TamanhoFonteExtra;
        // BCT-3: o FUNDO atras do texto ("auto"/"escuro"/"claro"). Declarado, ele MANDA na
        // escolha da sombra (contraste com o fundo > luminancia da letra).
        public readonly ConfigEntry<string> FundoTexto;

        public EstiloTmpCfg(ConfigFile cfg, string sec,
            bool haloAtivo, float largura, float suavidade, string corHex, float alfa,
            bool sombraAtiva, float sombraOffX, float sombraOffY, float sombraDilate,
            float sombraSuavidade, float alfaSombra, float tamanhoExtra, string fundo)
        {
            HaloAtivo = cfg.Bind(sec, "Halo", haloAtivo,
                "Contorno/halo em volta das letras (material do TextMeshPro). Desligue para nao tocar no contorno.");
            LarguraContorno = cfg.Bind(sec, "LarguraContorno", largura,
                "Espessura do contorno, em unidades de fonte SDF (_OutlineWidth). Faixa util: 0 a 0.5. " +
                "0.10 = fino; 0.25 = grosso.");
            SuavidadeContorno = cfg.Bind(sec, "SuavidadeContorno", suavidade,
                "Borramento do contorno (_OutlineSoftness). ALTO = halo suave; baixo (0) = contorno duro. " +
                "0.5-0.8 da o efeito de 'sombreamento radial' pedido.");
            CorContornoHex = cfg.Bind(sec, "CorContorno", corHex,
                "Cor do contorno no formato RRGGBB (sem #). Padrao 000000 = preto.");
            AlfaContorno = cfg.Bind(sec, "AlfaContorno", alfa,
                "Opacidade do contorno, 0 a 1. PADRAO 0.10 = os 10% pedidos pelo dono.");
            SombraAtiva = cfg.Bind(sec, "Sombra", sombraAtiva,
                "Sombra difusa (_Underlay, o 'drop shadow' do TextMeshPro). Ligada por padrao para reforcar a leitura.");
            SombraOffsetX = cfg.Bind(sec, "SombraOffsetX", sombraOffX, "Deslocamento X da sombra (-1 a 1).");
            SombraOffsetY = cfg.Bind(sec, "SombraOffsetY", sombraOffY, "Deslocamento Y da sombra (-1 a 1).");
            SombraDilate = cfg.Bind(sec, "SombraDilate", sombraDilate, "Engrossamento da sombra (_UnderlayDilate).");
            SombraSuavidade = cfg.Bind(sec, "SombraSuavidade", sombraSuavidade, "Borramento da sombra (_UnderlaySoftness).");
            AlfaSombra = cfg.Bind(sec, "AlfaSombra", alfaSombra, "Opacidade da sombra, 0 a 1.");
            TamanhoFonteExtra = cfg.Bind(sec, "TamanhoFonteExtra", tamanhoExtra,
                "Soma no tamanho da fonte. 0 = NAO MEXE no tamanho (padrao). Valores tipicos: +0.5 a +2.");
            FundoTexto = cfg.Bind(sec, "Fundo", fundo,
                "O FUNDO atras deste texto, que decide a COR da sombra (BCT-3). 'escuro' = cenario " +
                "escuro: a sombra tem de ser CLARA, senao some (era o defeito dos nomes de inimigo no " +
                "campo de batalha). 'claro' = cenario claro: a sombra tem de ser ESCURA. 'auto' = nao " +
                "declarado: a sombra segue a luminancia da LETRA (a regra antiga). O que importa aqui e o " +
                "CONTRASTE da sombra com o que esta atras dela — nao a cor da letra.");
        }

        public Color CorContorno => Configuracao.HexComAlfa(CorContornoHex.Value, AlfaContorno.Value);
        public Color CorSombra => Configuracao.HexComAlfa(CorContornoHex.Value, AlfaSombra.Value);

        /// <summary>O FUNDO declarado desta superficie (BCT-3), lido do config.</summary>
        public FundoSombra Fundo => Configuracao.FundoSombraDe(FundoTexto.Value);

        /// <summary>
        /// A cor da sombra para ESTA cor de letra (BCT-2/BCT-3/BCT-4). Com SombraAdaptativa=false
        /// devolve o comportamento FIXO antigo (<see cref="CorSombra"/>); com true, o FUNDO
        /// declarado manda na polaridade (fundo escuro -> sombra clara) e, sem fundo declarado, a
        /// luminancia da letra decide (a regra do BCT-2). Em qualquer caso o balde VIRA se a cor
        /// escolhida nao contrastar com a LETRA (a lei do BCT-4). O alfa continua sendo o da secao
        /// (<see cref="AlfaSombra"/>).
        /// </summary>
        public Color CorSombraPara(Color corLetra)
        {
            return Configuracao.CorSombraAdaptativa(corLetra, Plugin.Cfg.SombraAdaptativa.Value,
                CorSombra, AlfaSombra.Value, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura,
                Fundo);
        }
    }

    /// <summary>
    /// Superficie que NAO e TextMeshPro: os rotulos de stack/turno dos icones de status sao
    /// <c>UnityEngine.UI.Text</c> legado (l.174762/174764), que desenha com atlas de bitmap e
    /// nao tem material distance field — o halo suave e impossivel ali. Este bloco so expoe
    /// contorno duro (4 copias), sombra dura, negrito e tamanho.
    /// </summary>
    internal sealed class EstiloTextoLegadoCfg
    {
        public readonly ConfigEntry<bool> HaloAtivo;
        public readonly ConfigEntry<float> RaioContorno;
        public readonly ConfigEntry<string> CorContornoHex;
        public readonly ConfigEntry<float> AlfaContorno;
        public readonly ConfigEntry<bool> SombraAtiva;
        public readonly ConfigEntry<float> SombraOffsetX;
        public readonly ConfigEntry<float> SombraOffsetY;
        public readonly ConfigEntry<float> AlfaSombra;
        public readonly ConfigEntry<bool> Negrito;
        public readonly ConfigEntry<float> TamanhoExtra;
        // BCT-3: o FUNDO declarado (ver EstiloTmpCfg.FundoTexto).
        public readonly ConfigEntry<string> FundoTexto;

        public EstiloTextoLegadoCfg(ConfigFile cfg, string sec,
            bool haloAtivo, float raio, string corHex, float alfa,
            bool sombraAtiva, float sombraOffX, float sombraOffY, float alfaSombra,
            bool negrito, float tamanhoExtra, string fundo)
        {
            HaloAtivo = cfg.Bind(sec, "Halo", haloAtivo,
                "Contorno duro (componente Outline do Unity) nos rotulos 'x3' e no contador de turnos. " +
                "ATENCAO: este texto e UI.Text legado, NAO tem fonte distance field — o contorno aqui e " +
                "duro (4 copias), nunca suave. Para halo suave nestes rotulos seria preciso trocar os " +
                "componentes por TextMeshPro (mudanca grande, fora do escopo deste mod).");
            RaioContorno = cfg.Bind(sec, "RaioContorno", raio,
                "Distancia do contorno duro, em pixels da UI. 1.0 e discreto; 2.0 e bem visivel.");
            CorContornoHex = cfg.Bind(sec, "CorContorno", corHex,
                "Cor do contorno no formato RRGGBB (sem #). Padrao 000000 = preto.");
            AlfaContorno = cfg.Bind(sec, "AlfaContorno", alfa,
                "Opacidade de CADA uma das 4 copias do contorno duro (0 a 1). PADRAO 0.10 = os 10% pedidos. " +
                "Como o contorno duro nao borra, se ficar fraco demais suba para 0.25-0.40.");
            SombraAtiva = cfg.Bind(sec, "Sombra", sombraAtiva,
                "Sombra dura atras do rotulo (componente Shadow). E o que mais ajuda a ler em fundo claro.");
            SombraOffsetX = cfg.Bind(sec, "SombraOffsetX", sombraOffX, "Deslocamento X da sombra, em pixels.");
            SombraOffsetY = cfg.Bind(sec, "SombraOffsetY", sombraOffY, "Deslocamento Y da sombra, em pixels.");
            AlfaSombra = cfg.Bind(sec, "AlfaSombra", alfaSombra, "Opacidade da sombra, 0 a 1.");
            Negrito = cfg.Bind(sec, "Negrito", negrito,
                "Deixa os rotulos em negrito (FontStyle.Bold). Ganho de leitura grande, custo zero.");
            TamanhoExtra = cfg.Bind(sec, "TamanhoFonteExtra", tamanhoExtra,
                "Soma no tamanho da fonte do rotulo. 0 = NAO MEXE no tamanho (padrao).");
            FundoTexto = cfg.Bind(sec, "Fundo", fundo,
                "O FUNDO atras do rotulo, que decide a COR da sombra (BCT-3): 'escuro' = a sombra " +
                "tem de ser CLARA, senao some; 'claro' = tem de ser ESCURA; 'auto' = segue a " +
                "luminancia da LETRA (regra antiga).");
        }

        public Color CorContorno => Configuracao.HexComAlfa(CorContornoHex.Value, AlfaContorno.Value);
        public Color CorSombra => Configuracao.HexComAlfa(CorContornoHex.Value, AlfaSombra.Value);

        /// <summary>O FUNDO declarado desta superficie (BCT-3), lido do config.</summary>
        public FundoSombra Fundo => Configuracao.FundoSombraDe(FundoTexto.Value);

        /// <summary>
        /// A cor da sombra para ESTA cor de rotulo (BCT-2/BCT-3), no caminho LEGADO (UI.Text).
        /// Com SombraAdaptativa=false devolve o comportamento FIXO antigo
        /// (<see cref="CorSombra"/>); com true, o FUNDO declarado manda e, sem fundo declarado,
        /// vale a luminancia da letra (a regra do BCT-2). O alfa e o da secao
        /// (<see cref="AlfaSombra"/>).
        /// </summary>
        public Color CorSombraPara(Color corLetra)
        {
            return Configuracao.CorSombraAdaptativa(corLetra, Plugin.Cfg.SombraAdaptativa.Value,
                CorSombra, AlfaSombra.Value, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura,
                Fundo);
        }
    }
}
