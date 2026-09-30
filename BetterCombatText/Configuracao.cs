using System;
using BepInEx.Configuration;
using UnityEngine;

namespace BetterCombatText
{
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

            var secNomes = "2. Nomes de inimigos (combate)";
            Nomes = new EstiloTmpCfg(cfg, secNomes,
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
                tamanhoExtra: 0f);

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
                tamanhoExtra: 0f);

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
                tamanhoExtra: 0f);

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
                tamanhoExtra: 0f);

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
                tamanhoExtra: 0f);
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

        public EstiloTmpCfg(ConfigFile cfg, string sec,
            bool haloAtivo, float largura, float suavidade, string corHex, float alfa,
            bool sombraAtiva, float sombraOffX, float sombraOffY, float sombraDilate,
            float sombraSuavidade, float alfaSombra, float tamanhoExtra)
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
        }

        public Color CorContorno => Configuracao.HexComAlfa(CorContornoHex.Value, AlfaContorno.Value);
        public Color CorSombra => Configuracao.HexComAlfa(CorContornoHex.Value, AlfaSombra.Value);
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

        public EstiloTextoLegadoCfg(ConfigFile cfg, string sec,
            bool haloAtivo, float raio, string corHex, float alfa,
            bool sombraAtiva, float sombraOffX, float sombraOffY, float alfaSombra,
            bool negrito, float tamanhoExtra)
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
        }

        public Color CorContorno => Configuracao.HexComAlfa(CorContornoHex.Value, AlfaContorno.Value);
        public Color CorSombra => Configuracao.HexComAlfa(CorContornoHex.Value, AlfaSombra.Value);
    }
}
