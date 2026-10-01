using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using HarmonyLib;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// Intercepta OptionsManager.Localize(string original, LanguageGender, Gender) — o funil
    /// por onde passa TODO texto localizado do jogo — e altera o valor final (__result).
    ///
    /// Postfix = roda DEPOIS do método original. Recebemos:
    ///   - original : a string de entrada (texto em inglês, que é a base do jogo)
    ///   - __result : o valor que o método vai retornar; com `ref` podemos substituí-lo
    ///
    /// Por que Postfix e não Prefix: queremos o texto FINAL (já localizado/processado),
    /// e queremos que o jogo continue fazendo o trabalho dele — só complementamos a saída.
    /// </summary>
    [HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]
    public static class LocalizePatch
    {
        // Explicações adicionadas ao final do texto.
        //
        // Treasure Find — MECÂNICA CONFIRMADA (código + teste em jogo):
        //   - o efeito do powerup soma +20 por nível ao atributo "DropQuantityMod" (5 níveis → +100)
        //   - GameLogic.GetCharacterLootDropModifier soma o atributo de TODOS os personagens da party
        //   - o roll de loot multiplica a chance de cada item por esse modificador
        // Logo: +X% Treasure Find = +X% de chance de drop, acumulando com a party.


        /// <summary>
        /// Duas correcoes de acabamento pedidas em teste:
        ///
        /// (a) A COR. Quem troca o marcador #C8B090 pela cor de explicacao do jogo e o gancho DAS
        ///     NOTAS (`Postfix` de `OptionsManager.Localize`), no FIM dele — a cor e resolvida
        ///     sobre o texto que aquele gancho acabou de montar, e NAO depende de prioridade de
        ///     gancho nenhuma. COR-2 (01/10): antes disso a cor era um postfix `Priority.High`
        ///     SEPARADO e o marcador nunca era trocado, porque na 0Harmony do jogo a prioridade
        ///     ordena DESCENDENTE (maior roda primeiro) e o gancho da cor rodava ANTES do gancho
        ///     que acrescenta as notas — ele olhava um texto que ainda nao tinha marcador. Ver o
        ///     comentario do `Postfix`, a bancada `scratch/cor2/` e docs/TEXTO-TOOLTIPS.md §7.
        ///
        /// (b) A POSICAO. O jogo monta o tooltip como [descricao], uma quebra de linha e depois
        ///     [custos e alcance]
        ///     (ShowSkillTooltip, l.214400-214455 do decompilado), e a explicacao entra na
        ///     descricao - ou seja, ficava ANTES dos custos. Em vez de mudar a tabela (que e
        ///     chaveada pelo texto da descricao), este prefix pega o bloco ja colorido e o
        ///     move para o fim do corpo, que e o texto entregue a `ShowTooltip`.
        ///
        ///     COR-3 (01/10) — DE QUE BLOCO SE ESTA FALANDO. "o bloco ja colorido" era lido como
        ///     "o primeiro bloco da cor do nivel 2", e essa leitura deixou de valer quando a cor
        ///     do nivel 2 passou a ser aplicada de verdade: `Tooltip.specialDescColor` vale
        ///     `#CBB396`, o MESMO literal que o motor escreve nos valores dinamicos das skills —
        ///     o primeiro bloco dessa cor numa tooltip com dano e o VALOR DE DANO, nao a nossa
        ///     nota. O prefixo passou a achar a nota pelo CONTEUDO (`_conteudosDeNota`), e o
        ///     `#CBB396` do jogo fica onde esta. Ver o comentario de `_conteudosDeNota`.
        /// </summary>
        [HarmonyPatch]
        internal static class CorEOrdemDoTooltip
        {
            /// <summary>Diagnostico 1x: diz no log se o prefix achou o bloco (ou nao).</summary>
            private static bool _diagnosticadoCor;

            /// <summary>
            /// Assinatura EXATA (13 tipos, na ordem) do overload de ShowTooltip que recebe o corpo do
            /// tooltip. Fonte: decompilado do Assembly-CSharp.dll (`ilspycmd -t Tooltip -il`):
            ///   instance void Tooltip::ShowTooltip(string, string,
            ///     class [UnityEngine.CoreModule]UnityEngine.Sprite, string, class TooltipOffsetInfo,
            ///     valuetype [UnityEngine.CoreModule]UnityEngine.Color,
            ///     valuetype System.Nullable`1&lt;UnityEngine.Vector3&gt;, bool, bool, float32,
            ///     valuetype System.Nullable`1&lt;ControlGlyphInfo&gt;, string, bool)
            /// `TooltipOffsetInfo` e CLASSE (vai como tipo puro); `ControlGlyphInfo` e STRUCT, entao o
            /// slot nullable dele e `Nullable&lt;ControlGlyphInfo&gt;` (`ControlGlyphInfo?`).
            /// </summary>
            private static readonly Type[] AssinaturaDoShowTooltip = new Type[]
            {
                typeof(string),                 // __0 title
                typeof(string),                 // __1 subtitle
                typeof(UnityEngine.Sprite),     // __2 icon
                typeof(string),                 // __3 description  <- o slot que o prefix reescreve
                typeof(TooltipOffsetInfo),      // __4 tooltipOffsetInfo
                typeof(UnityEngine.Color),      // __5 titleTextColor
                typeof(UnityEngine.Vector3?),   // __6 hoveringElementScreenPos
                typeof(bool),                   // __7 showIcon
                typeof(bool),                   // __8 isItem
                typeof(float),                  // __9 alpha
                typeof(ControlGlyphInfo?),      // __10 controlGlyphInfo
                typeof(string),                 // __11 footerText
                typeof(bool)                    // __12 showEquipped
            };

            /// <summary>
            /// Mira o overload de ShowTooltip que recebe o corpo do tooltip por LISTA EXPLICITA DE
            /// TIPOS (mesmo padrao do `ShrineAuraPatch` l.303-304), NUNCA mais "o primeiro metodo
            /// chamado ShowTooltip com mais de 4 parametros": era assim antes e, se o jogo reordenasse
            /// os parametros ou surgisse uma segunda sobrecarga, o slot mudaria EM SILENCIO (o mesmo
            /// defeito que ja derrubou o jogo com um patch lendo o slot de um float).
            /// Sem o metodo por assinatura exata o gancho NAO e aplicado — nunca um alvo escolhido por
            /// engano — e o motivo fica escrito no log.
            /// </summary>
            private static System.Reflection.MethodBase TargetMethod()
            {
                try
                {
                    System.Reflection.MethodInfo alvo =
                        AccessTools.Method(typeof(Tooltip), "ShowTooltip", AssinaturaDoShowTooltip);
                    if (alvo != null)
                    {
                        return alvo;
                    }
                    Plugin.Log.LogError("BetterTooltips: Tooltip.ShowTooltip com a assinatura de 13 "
                        + "parametros NAO foi encontrado — o gancho de cor/ordem do tooltip NAO sera "
                        + "aplicado nesta sessao (nunca um metodo escolhido por engano).");
                    return null;
                }
                catch (Exception e)
                {
                    Plugin.Log.LogError("BetterTooltips: falha ao resolver Tooltip.ShowTooltip pela "
                        + "lista de tipos — gancho de cor/ordem NAO aplicado: " + e.Message);
                    return null;
                }
            }

            /// <summary>Move as explicacoes para o fim (depois de custos e alcance).
            ///
            /// RV-27: com DUAS cores no mesmo tooltip (a nota na cor especial do jogo e a linha de
            /// auras ativas no azul do proprio jogo) mover so o PRIMEIRO bloco embaralharia a ordem —
            /// a linha azul ficaria ANTES da nota. Entao os dois blocos sao retirados e recolocados na
            /// ordem desejada: nota primeiro, linha de auras por ULTIMO, cada um com exatamente uma
            /// linha em branco antes (regra do `AnexarNota`).
            /// </summary>
            /// PARAMETRO POR NOME, nunca por indice: `ref string description` casa com o 4o parametro do
            /// metodo do jogo pelo NOME DELE (`ShowTooltip(string title, string subtitle, Sprite icon,
            /// string description, ...)`), nao pela posicao. O `ref __3` antigo dependia do slot 3 e o
            /// alvo era achado por reflexao "o primeiro ShowTooltip com mais de 4 parametros" — se a
            /// assinatura mudasse, `__3` passaria a apontar para outro tipo EM SILENCIO (foi exatamente
            /// essa a familia de defeito que quebrou o jogo em batalha). O `TargetMethod` acima agora
            /// resolve pela lista de 13 tipos, entao nome e posicao ficam amarrados.
            /// O corpo roda a cada hover (gancho QUENTE): qualquer falha e registrada UMA vez por motivo
            /// e o texto do jogo sai INTACTO.
            private static void Prefix(ref string description)
            {
                // Snapshot: o corpo abaixo remove blocos coloridos pelo caminho; se algo lancar no meio,
                // devolvemos EXATAMENTE o texto que o jogo montou (nunca um texto pela metade).
                string textoDoJogo = description;
                try
                {
                    if (string.IsNullOrEmpty(description))
                    {
                        return;
                    }
                    string corNota = string.IsNullOrEmpty(_corEspecialDoJogo) ? MarcadorCorDeExplicacao : _corEspecialDoJogo;
                    string corAura = CorDaLinhaDeAuras();
                    bool mesmaCor = string.Equals(corNota, corAura, StringComparison.OrdinalIgnoreCase);

                    // Se as cores coincidirem (a leitura da paleta falhou e a linha caiu na cor das notas),
                    // a ULTIMA ocorrencia e a linha de auras — ela e a ultima coisa anexada ao texto.
                    // O bloco da linha de auras so e aceito se comecar com o marcador dela: assim nenhum
                    // bloco colorido do proprio jogo (com a MESMA cor de status) entra na conta.
                    string aura;
                    bool achouAura = TirarBloco(ref description, corAura, mesmaCor, ShrineAuraPatch.MarcadorLinhaDeAuras, out aura);
                    // COR-3: a NOSSA nota e achada pelo CONTEUDO, nunca pela cor — depois que a cor
                    // do nivel 2 e aplicada ela e o mesmo `#CBB396` dos valores do motor, e "o
                    // primeiro bloco dessa cor" seria o VALOR DE DANO da skill (era ele que ia para
                    // o fundo). Ver `_conteudosDeNota`.
                    //
                    // RV-17 (01/10) — TODAS AS NOTAS, NA ORDEM DO TEXTO. Uma tooltip pode ter DUAS
                    // notas do nivel 2: os dois casos reais (`Shapeshift Dragonkin`, que tem o `[0]`
                    // do Armor, e o buff `Miniature`) trazem DOIS blocos FUNDIDOS no valor do
                    // `TextFixes` (os dois estao no fonte). Extrair so a primeira — que era o que a
                    // versao anterior fazia — deixava a SEGUNDA onde ela estava, ANTES do `AP Cost`, e
                    // a ordem de leitura invertia (a 2a nota na frente da 1a). O formato e UM: cada
                    // bloco vai para o FIM na ordem em que aparece, uma linha em branco antes de
                    // cada, e a linha azul do nivel 3 continua por ultimo. Ver
                    // docs/TEXTO-TOOLTIPS.md §9.
                    List<string> notas = new List<string>();
                    string nota;
                    bool achouNota = TirarNotaDoMod(ref description, out nota);
                    while (achouNota)
                    {
                        notas.Add(nota);
                        achouNota = TirarNotaDoMod(ref description, out nota);
                    }

                    if (!achouAura && notas.Count == 0)
                    {
                        if (!_diagnosticadoCor)
                        {
                            _diagnosticadoCor = true;
                            Plugin.Log.LogInfo("BetterTooltips: ShowTooltip interceptado SEM o bloco (procurando "
                                + "<color=#" + corNota + "> e <color=#" + corAura + ">)");
                        }
                        return;
                    }
                    if (!_diagnosticadoCor)
                    {
                        _diagnosticadoCor = true;
                        Plugin.Log.LogInfo("BetterTooltips: ShowTooltip interceptado, blocos movidos para o fim (nota #"
                            + corNota + ", auras ativas #" + corAura + ")");
                    }

                    string corpo = description.TrimEnd();
                    foreach (string blocoNota in notas)
                    {
                        corpo += "\n\n" + blocoNota;
                    }
                    if (!string.IsNullOrEmpty(aura))
                    {
                        corpo += "\n\n" + aura;
                    }
                    description = corpo;
                }
                catch (Exception e)
                {
                    description = textoDoJogo;
                    RegistrarFalhaIgnorada("prefix de cor/ordem do Tooltip.ShowTooltip", e);
                }
            }

            /// <summary>
            /// Tira do corpo o PRIMEIRO (ou o ULTIMO) bloco `&lt;color=#hex&gt;...&lt;/color&gt;`, junto
            /// com a LINHA EM BRANCO que o `AnexarNota` escreveu antes dele (`InicioDoSeparador`), e
            /// devolve o bloco ja aparado nas pontas.
            /// `exigir` (opcional) so aceita o bloco que contiver esse trecho — usado na linha de auras,
            /// que tem marcador proprio, para nao confundir com blocos do jogo na MESMA cor.
            /// Sem bloco que sirva -> false (e o corpo fica como estava).
            /// </summary>
            private static bool TirarBloco(ref string corpo, string hex, bool ultimo, string exigir, out string bloco)
            {
                bloco = null;
                if (string.IsNullOrEmpty(corpo) || string.IsNullOrEmpty(hex))
                {
                    return false;
                }
                const string fechamento = "</color>";
                string abre = "<color=#" + hex + ">";
                int i = ultimo
                    ? corpo.LastIndexOf(abre, StringComparison.Ordinal)
                    : corpo.IndexOf(abre, StringComparison.Ordinal);
                while (i >= 0)
                {
                    int f = corpo.IndexOf(fechamento, i, StringComparison.Ordinal);
                    if (f < 0)
                    {
                        return false;
                    }
                    int ini = InicioDoSeparador(corpo, i);
                    int fim = f + fechamento.Length;
                    string texto = corpo.Substring(ini, fim - ini).TrimStart('\n').TrimEnd();
                    if (string.IsNullOrEmpty(exigir) || texto.IndexOf(exigir, StringComparison.Ordinal) >= 0)
                    {
                        bloco = texto;
                        corpo = corpo.Remove(ini, fim - ini);
                        return true;
                    }
                    if (ultimo)
                    {
                        if (i == 0)
                        {
                            return false;
                        }
                        i = corpo.LastIndexOf(abre, i - 1, StringComparison.Ordinal);
                    }
                    else
                    {
                        i = corpo.IndexOf(abre, i + 1, StringComparison.Ordinal);
                    }
                }
                return false;
            }

            /// <summary>
            /// Tira do corpo o bloco de UMA nota do mod, reconhecida pelo CONTEUDO
            /// (`_conteudosDeNota`, alimentado por `RegistrarBlocosDeNota`) — nunca pela cor.
            ///
            /// COR-3 (01/10): a busca por cor ("o primeiro bloco do nivel 2") so e segura enquanto a
            /// cor da nota NAO existir em nenhum bloco do jogo. Como `Tooltip.specialDescColor` vale
            /// exatamente o `#CBB396` que o motor escreve nos valores dinamicos, o primeiro bloco
            /// dessa cor numa tooltip de skill e o VALOR DE DANO — e era ele que o prefixo movia para
            /// o fundo. Por conteudo, um numero do motor nunca casa com a frase da nota.
            ///
            /// UMA nota por chamada — e o CHAMADOR chama em LACO, porque uma tooltip pode ter DUAS
            /// notas do nivel 2. Os dois casos reais estao no fonte e nos testes (`Shapeshift
            /// Dragonkin`, que tem o `[0]` do Armor, e o buff `Miniature`): nos dois o valor FUNDIDO
            /// do `TextFixes` carrega DOIS blocos com o marcador. A versao anterior deste comentario
            /// afirmava que o mod anexava UMA nota por tooltip e nunca duas; era FALSO, e era
            /// exatamente o que deixava a segunda nota para tras, ANTES do `AP Cost`, invertendo a
            /// ordem de leitura. O bloco removido leva junto a linha em branco que o `AnexarNota`
            /// escreveu antes dele (`InicioDoSeparador`), e o texto devolvido e o mesmo que o
            /// `TirarBloco` devolvia.
            /// </summary>
            private static bool TirarNotaDoMod(ref string corpo, out string nota)
            {
                nota = null;
                if (string.IsNullOrEmpty(corpo))
                {
                    return false;
                }
                const string fechamento = "</color>";
                const string abertura = "<color=#";
                int i = 0;
                while (i < corpo.Length)
                {
                    int j = corpo.IndexOf(abertura, i, StringComparison.Ordinal);
                    if (j < 0)
                    {
                        return false;
                    }
                    int fechaTag = corpo.IndexOf('>', j);
                    if (fechaTag < 0)
                    {
                        return false;
                    }
                    int f = corpo.IndexOf(fechamento, fechaTag, StringComparison.Ordinal);
                    if (f < 0)
                    {
                        return false;
                    }
                    if (_conteudosDeNota.Contains(corpo.Substring(fechaTag + 1, f - fechaTag - 1)))
                    {
                        int ini = InicioDoSeparador(corpo, j);
                        int fim = f + fechamento.Length;
                        nota = corpo.Substring(ini, fim - ini).TrimStart('\n').TrimEnd();
                        corpo = corpo.Remove(ini, fim - ini);
                        return true;
                    }
                    i = f + 1;
                }
                return false;
            }

            /// <summary>
            /// Onde comeca o trecho que sera REMOVIDO do corpo: o bloco em `posicao` mais a LINHA
            /// EM BRANCO que o `AnexarNota` escreveu antes dele (as duas quebras), quando elas
            /// existem.
            ///
            /// RV-17 (01/10) — POR QUE AS DUAS, E NAO UMA. O prefixo tira a nota do meio do corpo e
            /// a recoloca no fim. Consumindo so UMA quebra, a outra ficava para tras e o tooltip
            /// saia com uma linha em branco ORFA entre a descricao e o `AP Cost` (o bloco saiu
            /// dali, mas a marca dele ficou): medido no caminho real, `descricao\n\nNOTA\nAP Cost`
            /// virava `descricao\n\nAP Cost`. Nenhuma quebra do texto do JOGO e tocada: o
            /// `AnexarNota` apara o fim da descricao antes de escrever o separador dele, entao as
            /// duas quebras, quando existem, sao NOSSAS. Quando so existe uma (as entradas
            /// FUNDIDAS do `TextFixes`, ex. `Recover [0]% of max mana each turn. \n<color...`),
            /// so ela e consumida — o separador de uma quebra do proprio jogo fica. Ver
            /// docs/TEXTO-TOOLTIPS.md §9.
            /// </summary>
            private static int InicioDoSeparador(string corpo, int posicao)
            {
                int ini = posicao;
                if (ini > 0 && corpo[ini - 1] == '\n')
                {
                    ini--;
                    if (ini > 0 && corpo[ini - 1] == '\n')
                    {
                        ini--;
                    }
                }
                return ini;
            }
        }
        /// <summary>
        /// NIVEL 2 da convencao de cores (docs/TEXTO-TOOLTIPS.md §1/§2) — explicacao de TERMOS e
        /// CALCULOS. A cor NAO e escolhida por nos: e `Tooltip.specialDescColor`, o campo do prefab
        /// que o PROPRIO jogo usa para os blocos de DESCRICAO anexados — o par
        /// `specialTitleColor`+`specialDescColor` monta o bloco "Special" do tooltip de item
        /// (bancada do decompilado: `scratch/rv22/tooltip.cs:1854-1855` e `1950-1951`).
        ///
        /// PROVA DE QUE NAO E A COR DOS NOMES DE STATUS: quem colore os nomes de status/atributo
        /// e `specialTextColor` (`tooltip.cs:608`/`627`, o token `{STA=}` e o `@atributo@`), um
        /// campo DIFERENTE. A escolha por `specialDescColor` foi medida em 29/09 (BT-9) contra
        /// print do proprio jogo: o bloco de descricao anexado sai bege, nao no azul de status.
        ///
        /// COR-2 (01/10) — LEITURA DATADA DO PROPRIO ASSET (nao de print): os TRES componentes
        /// `Tooltip` do jogo (level1 pid 15581/15605 e resources.assets pid 2591822) trazem
        /// `specialDescColor` = `skillStatusColor` = `specialTextColor` = `specialTitleColor` =
        /// **#CBB396**. Ou seja: o bege medido por pixel em 29/09 e este campo (a diferenca
        /// `#C8B090` x `#CBB396` e do print/antialiasing, nao de campo). A leitura do asset foi
        /// validada contra o log de runtime: o mesmo leitor devolve `GUIManager.coldColor` =
        /// `#00D7FF`, exatamente o que a sessao de 01/10 logou ao ler o campo em jogo
        /// (`scratch/cor2/le_cores_do_tooltip.py`, `le_guimanager_cores.py` e `tooltip_cores.json`).
        ///
        /// `MarcadorCorDeExplicacao` e o valor medido do bloco do jogo (bege) usado como marcador
        /// nas tabelas: ele e um hex valido, entao o texto continua legivel se a leitura falhar, e
        /// o log avisa. O marcador NAO e a cor final — quem manda no tooltip e o campo lido em
        /// runtime (`#CBB396`).
        /// </summary>
        internal static string _corEspecialDoJogo;

        /// <summary>Marcador do nivel 2. Procedencia: medicao por pixel do bloco de descricao de
        /// status do jogo em 29/09 (BT-9c, `#C8B090`); o valor do campo `Tooltip.specialDescColor`
        /// no asset, lido em 01/10 (COR-2), e `#CBB396` — o marcador e so o valor de reserva.
        /// Fonte declarada: `Tooltip.specialDescColor`. Ver docs/TEXTO-TOOLTIPS.md §2.</summary>
        internal const string MarcadorCorDeExplicacao = "C8B090";

        /// <summary>
        /// Envolve uma nota do NIVEL 2 no marcador de cor (o postfix de prioridade alta troca o
        /// marcador pela cor real do tooltip). Toda nota acrescentada por codigo passa por aqui —
        /// nota sem marcador sai no tom do corpo do tooltip (o nivel 1) e vira uma explicacao que
        /// se confunde com a descricao do jogo. O texto NAO muda: so ganha o markup em volta.
        /// </summary>
        private static string NotaDeExplicacao(string nota)
        {
            if (string.IsNullOrEmpty(nota))
            {
                return nota;
            }
            return "<color=#" + MarcadorCorDeExplicacao + ">" + nota.Trim() + "</color>";
        }

        /// <summary>O bloco que comeca logo depois do marcador pertence ao NIVEL 3 (linha de auras
        /// ativas ou bloco de sinergia status x skill de `StatusSkillSynergyPatch`)? Serve para a
        /// troca de cor do nivel 2 NAO repintar um bloco do nivel 3 que caiu no mesmo marcador de
        /// reserva — sem isso os dois niveis colapsam em silencio (achado do COR-1).</summary>
        private static bool ComecaBlocoDoNivel3(string texto, int posicaoDoMarcador)
        {
            int i = posicaoDoMarcador + MarcadorCorDeExplicacao.Length;
            if (i >= texto.Length || texto[i] != '>')
            {
                return false;
            }
            return EhBlocoDoNivel3(texto.Substring(i + 1));
        }

        /// <summary>O texto que ABRE um bloco do NIVEL 3 e o marcador de texto proprio dele
        /// ("Your active shrine auras:" / "Your skills on this status:"), nunca uma cor — por isso
        /// a checagem serve tanto para o texto cru quanto para o conteudo ja extraido.</summary>
        private static bool EhBlocoDoNivel3(string texto)
        {
            return texto.StartsWith(ShrineAuraPatch.MarcadorLinhaDeAuras, StringComparison.Ordinal)
                || texto.StartsWith(StatusSkillSynergyPatch.Marcador, StringComparison.Ordinal);
        }

        /// <summary>
        /// O CONTEUDO das notas que este mod escreveu — o texto entre as tags de cor dos blocos que
        /// nasceram com o marcador. E a chave de identificacao da NOSSA nota dentro do tooltip ja
        /// montado.
        ///
        /// COR-3 (01/10) — POR QUE POR CONTEUDO, E NAO POR COR. A cor do nivel 2
        /// (`Tooltip.specialDescColor`, lida em runtime) vale `#CBB396` — o MESMO literal que o
        /// motor usa nos valores dinamicos que ele mesmo escreve
        /// (`ApplyDescriptionExpressions`, `<color=#CBB396>` na l.2327 do decompilado, e
        /// `GetDamageString`, l.2276, com `<size=...><color=#CBB396>NN</color></size>`). Depois que
        /// `ComACorDoJogo` troca o marcador pela cor do campo, o bloco da NOSSA nota fica com o
        /// mesmo hex dos valores do jogo — e o `CorEOrdemDoTooltip` ("o primeiro bloco dessa cor")
        /// passava a pegar o VALOR DE DANO da skill e move-lo para o FUNDO do tooltip. A cor nao
        /// distingue os dois papeis; o CONTEUDO distingue: o valor do motor e um numero (ou um
        /// rotulo curto), a nota e uma frase que este mod escreveu.
        ///
        /// Bloco do NIVEL 3 que caiu no marcador de reserva fica FORA da lista: ele tem identidade
        /// propria (o marcador de texto da linha de auras / do bloco de sinergia) e nao pode ser
        /// confundido com uma nota do nivel 2.
        /// </summary>
        private static readonly HashSet<string> _conteudosDeNota = new HashSet<string>(StringComparer.Ordinal);

        /// <summary>Registra o conteudo de cada bloco que nasceu com o marcador. Roda ANTES da troca
        /// de cor e vale ate quando a leitura do campo falha (o bloco fica no marcador e continua
        /// identificavel) — ver `_conteudosDeNota`.</summary>
        private static void RegistrarBlocosDeNota(string texto)
        {
            string abre = "<color=#" + MarcadorCorDeExplicacao + ">";
            int i = 0;
            while (i < texto.Length)
            {
                int j = texto.IndexOf(abre, i, StringComparison.Ordinal);
                if (j < 0)
                {
                    return;
                }
                int f = texto.IndexOf("</color>", j + abre.Length, StringComparison.Ordinal);
                if (f < 0)
                {
                    return;
                }
                int inicio = j + abre.Length;
                string conteudo = texto.Substring(inicio, f - inicio);
                if (!EhBlocoDoNivel3(conteudo))
                {
                    _conteudosDeNota.Add(conteudo);
                }
                i = f + 1;
            }
        }

        internal static string ComACorDoJogo(string texto)
        {
            if (string.IsNullOrEmpty(texto) || texto.IndexOf(MarcadorCorDeExplicacao, StringComparison.Ordinal) < 0)
            {
                return texto;
            }
            // COR-3: registra o CONTEUDO das notas ANTES de trocar a cor. Depois da troca o bloco da
            // nota fica com a mesma cor dos valores do motor e so o conteudo o distingue (ver
            // `_conteudosDeNota`). Vale tambem quando a leitura do campo falha (o bloco continua no
            // marcador e o registro ja foi feito).
            RegistrarBlocosDeNota(texto);
            if (_corEspecialDoJogo == null)
            {
                try
                {
                    Tooltip t = GUIManager.instance != null ? GUIManager.instance.tooltip : null;
                    _corEspecialDoJogo = t != null
                        ? UnityEngine.ColorUtility.ToHtmlStringRGB(t.specialDescColor)
                        : string.Empty;
                    Plugin.Log.LogInfo("BetterTooltips: cor do jogo para explicacoes = #" + _corEspecialDoJogo);
                }
                catch (Exception ex)
                {
                    _corEspecialDoJogo = string.Empty;
                    Plugin.Log.LogWarning("BetterTooltips: nao consegui ler specialDescColor (" + ex.Message + "); mantendo o fallback.");
                }
            }
            if (string.IsNullOrEmpty(_corEspecialDoJogo))
            {
                return texto;
            }
            // NIVEL 2 apenas: percorre as ocorrencias do marcador e troca SO as que abrem bloco de
            // explicacao. O bloco do nivel 3 que caiu no marcador de reserva fica como esta (o
            // nivel 3 tem a cor propria dele, resolvida por `CorDaLinhaDeAuras`).
            var sb = new System.Text.StringBuilder(texto.Length);
            int i2 = 0;
            while (i2 < texto.Length)
            {
                int j = texto.IndexOf(MarcadorCorDeExplicacao, i2, StringComparison.Ordinal);
                if (j < 0)
                {
                    sb.Append(texto, i2, texto.Length - i2);
                    break;
                }
                sb.Append(texto, i2, j - i2);
                sb.Append(ComecaBlocoDoNivel3(texto, j) ? MarcadorCorDeExplicacao : _corEspecialDoJogo);
                i2 = j + MarcadorCorDeExplicacao.Length;
            }
            return sb.ToString();
        }

        /// <summary>
        /// RV-27 — a COR da LINHA DE AURAS ATIVAS ("Your active shrine auras: ..."), o unico texto do
        /// mod que nao e explicacao de mecanica da skill, e sim ESTADO AGREGADO do personagem.
        ///
        /// POR QUE NAO UM HEX FIXO: nao existe azul em constante nenhuma do jogo. Varredura do
        /// Assembly-CSharp.dll (literais `&lt;color=#RRGGBB&gt;`) devolve so CBB396 (43 usos), FFFFFF (5),
        /// 808080, CFCFCF, FF9C00 e 00000000 — paleta quente/neutra. A cor tem de vir, como as
        /// outras, de um CAMPO de cor do PROPRIO tooltip lido em runtime.
        ///
        /// ORDEM DE PREFERENCIA (cores do jogo, nenhuma escolhida a mao):
        ///   1) `Tooltip.skillStatusColor` — a cor que o PROPRIO jogo usa nos tooltips para os blocos de
        ///      STATUS anexados (nome + descricao do status): decompiado `Tooltip.ShowTooltip`,
        ///      l.213588 e l.213618 (`"&lt;i&gt;&lt;color=#" + skillStatusColor + "&gt;" + status.Name + "&lt;/color&gt;&lt;/i&gt;"`).
        ///      E o analogo exato desta linha: texto sobre o ESTADO do personagem, nao sobre a mecanica
        ///      da skill.
        ///      COR-2 (01/10) — LEITURA DATADA: este campo vale **#CBB396** no asset (e o MESMO bege
        ///      dos campos `special*` do nivel 2), entao ele NUNCA passa no `EhAzul` e esta linha
        ///      sempre cai no elo seguinte — foi o que a sessao de 01/10 mostrou no log ("azul da
        ///      paleta lido em GUIManager.coldColor = #00D7FF", sem NENHUMA linha de
        ///      skillStatusColor). O elo 1 e, por tanto, um elo MORTO hoje; a fonte DECLARADA da cor
        ///      do nivel 3 na especificacao do dono (`docs/TEXTO-TOOLTIPS.md` §1/§2) NAO se sustenta
        ///      — o azul em uso e o do elo 2. Fato medido, nao decisao: quem escolhe a cor do nivel 3
        ///      e o dono (ver §7 e o relato do COR-2). O elo fica onde esta para nao mudar a escolha
        ///      dele em silencio.
        ///   2) `GUIManager.coldColor` — o azul do tipo de dano Cold, usado nos tooltips pelo par
        ///      `Tooltip.GetDamageTypeColor` -> `GlobalSettingsManager.GetDamageTypeColor`
        ///      (decompiado l.214898, `GetItemInfoDetails` do tooltip de arma). Valor medido em
        ///      01/10: `#00D7FF` (o MESMO que o log de runtime imprime) — e o azul que o tooltip
        ///      usa de fato.
        ///   3) `GUIManager.manaColor` — o azul da Mana (COR-1, 01/10): terceiro elo da MESMA paleta da
        ///      HUD (`scratch/sac1/GUIManager.cs:250`), azul por papel, para a reserva do nivel 3 nao
        ///      depender de dois campos so.
        ///   4) Se nenhum deles for um azul legivel (ou o tooltip ainda nao existir), devolve o
        ///      marcador "#C8B090" — a linha sai na MESMA cor das notas, em vez de sair sem cor, e o
        ///      log AVISA O COLAPSO (niveis 2 e 3 na mesma cor). Nenhum hex inventado entra no codigo;
        ///      o achado e a correcao estao em docs/TEXTO-TOOLTIPS.md §5.
        ///
        /// So esta linha (e o bloco `Your skills on this status`, o caso do Frost Bite) passa por aqui:
        /// `ComACorDoJogo` (as notas do nivel 2) continua intocado.
        /// </summary>
        internal static string CorDaLinhaDeAuras()
        {
            if (_corAuraDoJogo == null)
            {
                _corAuraDoJogo = LerCorAzulDoJogo();
                if (_corAuraDoJogo == null)
                {
                    _corAuraDoJogo = MarcadorCorDeExplicacao;
                    Plugin.Log.LogWarning("BetterTooltips: nenhuma cor azul da paleta do jogo disponivel "
                        + "(skillStatusColor/coldColor/manaColor) — a linha de auras ativas sai na cor das notas "
                        + "(#" + MarcadorCorDeExplicacao + "): os NIVEIS 2 e 3 COLAPSARAM nesta sessao.");
                }
                else
                {
                    Plugin.Log.LogInfo("BetterTooltips: cor da linha de auras ativas = #" + _corAuraDoJogo);
                }
            }
            return _corAuraDoJogo;
        }

        /// <summary>Hex da linha de auras ativas, resolvido uma vez (o tooltip e remontado a cada hover).</summary>
        internal static string _corAuraDoJogo;

        private static string LerCorAzulDoJogo()
        {
            try
            {
                Tooltip t = GUIManager.instance != null ? GUIManager.instance.tooltip : null;
                if (t != null && EhAzul(t.skillStatusColor))
                {
                    string cor = UnityEngine.ColorUtility.ToHtmlStringRGB(t.skillStatusColor);
                    Plugin.Log.LogInfo("BetterTooltips: azul da paleta lido em Tooltip.skillStatusColor (status do jogo em tooltip) = #" + cor);
                    return cor;
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("BetterTooltips: nao consegui ler skillStatusColor (" + ex.Message + ").");
            }
            try
            {
                if (GUIManager.instance != null && EhAzul(GUIManager.instance.coldColor))
                {
                    string cor = UnityEngine.ColorUtility.ToHtmlStringRGB(GUIManager.instance.coldColor);
                    Plugin.Log.LogInfo("BetterTooltips: azul da paleta lido em GUIManager.coldColor (cor do dano Cold) = #" + cor);
                    return cor;
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("BetterTooltips: nao consegui ler coldColor (" + ex.Message + ").");
            }
            try
            {
                // COR-1 (01/10): TERCEIRO elo azul da MESMA paleta da HUD. Sem ele, a reserva do nivel 3
                // dependia de DOIS campos e caia no marcador do nivel 2 (niveis colapsados).
                if (GUIManager.instance != null && EhAzul(GUIManager.instance.manaColor))
                {
                    string cor = UnityEngine.ColorUtility.ToHtmlStringRGB(GUIManager.instance.manaColor);
                    Plugin.Log.LogInfo("BetterTooltips: azul da paleta lido em GUIManager.manaColor (cor de Mana) = #" + cor);
                    return cor;
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("BetterTooltips: nao consegui ler manaColor (" + ex.Message + ").");
            }
            return null;
        }

        /// <summary>Azul = o canal B nao perde para os outros dois e a cor nao e cinza/quase branca.
        /// (Serve de SANIDADE: se o build mudar a cor de status para bege, a linha nao vira uma copia
        /// silenciosa das notas.)</summary>
        private static bool EhAzul(UnityEngine.Color c)
        {
            float excesso = (c.b - c.r) + (c.b - c.g);
            return c.b >= c.r && c.b >= c.g && c.b > 0.35f && excesso > 0.05f;
        }

        // ---------------------------------------------------------------------------------------
        // COR-2 (01/10) — AQUI MORAVA O `CorDoJogoPostfix` ([HarmonyPostfix, Priority.High]).
        //
        // Ele estava ERRADO por construcao: `Priority.High` (600) e o gancho das notas e `Normal`
        // (400), e na 0Harmony que o jogo carrega a prioridade ordena DESCENDENTE — `PatchSorter`
        // -> `PatchInfoSerialization.PriorityComparer` devolve `-priority.CompareTo(value)`
        // (bancada: `scratch/cor2/PatchInfoSerialization.cs:48-58`), e o `HarmonyManipulator`
        // emite as chamadas na ordem da lista ja ordenada (`scratch/cor2/HarmonyManipulator.cs:646`).
        // Ou seja: o gancho da cor rodava PRIMEIRO, sobre um texto que ainda NAO tinha marcador
        // nenhum (as notas sao acrescentadas pelo `Postfix` Normal), e o `#C8B090` das tabelas
        // chegava ao tooltip sem troca.
        //
        // A PROVA EMPIRICA: a linha que `ComACorDoJogo` imprime ao ler o campo
        // ("cor do jogo para explicacoes = #...") nao existe em NENHUM log, nem na sessao de
        // 01/10 feita COM a DLL do perfil — enquanto as linhas do gancho das notas e do
        // `ShowTooltip` (com o `#C8B090` literal no texto final) estao la. O unico jeito de o
        // gancho da cor nao ler o campo e ele nunca ter visto o marcador.
        //
        // O CONSERTO nao foi reordenar (isso manteria a dependencia de uma regra de prioridade
        // que ja foi lida errada uma vez): a cor passou a ser aplicada no FIM do gancho DAS NOTAS
        // (`Postfix` -> `AplicarNotasDoFunil` -> `ComACorDoJogo`). Sem gancho de cor separado nao
        // existe ordem para errar. Ver docs/TEXTO-TOOLTIPS.md §7.
        // ---------------------------------------------------------------------------------------

        private static readonly Dictionary<string, string> TextAppends = new Dictionary<string, string>
        {
            // RV-12 powerup: Damage Reduction (Lv5)
            { "+ 20% Damage Reduction",
              "\n<color=#C8B090>Reduces all damage you take. Applied before Resistances and Armor.</color>" },
            // RV-12 powerup: Damage Reduction (Lv4)
            { "+ 16% Damage Reduction",
              "\n<color=#C8B090>Reduces all damage you take. Applied before Resistances and Armor.</color>" },
            // RV-12 powerup: Damage Reduction (Lv3)
            { "+ 12% Damage Reduction",
              "\n<color=#C8B090>Reduces all damage you take. Applied before Resistances and Armor.</color>" },
            // RV-12 powerup: Damage Reduction (Lv2)
            { "+ 8% Damage Reduction",
              "\n<color=#C8B090>Reduces all damage you take. Applied before Resistances and Armor.</color>" },
            // RV-12 powerup: Damage Reduction (Lv1)
            { "+ 4% Damage Reduction",
              "\n<color=#C8B090>Reduces all damage you take. Applied before Resistances and Armor.</color>" },
            // RV-15 Chaos: Chaos Cloud - o sorteio do elemento e o dodge sao testes SEPARADOS.
            { "Summons a cloud of chaos that strikes 3 times. At every strike each damage type has a @50%@ chance to deal *0 damage.",
              "\n<color=#C8B090>The 50% roll only decides whether each element lands; the damage can still be dodged, and those are two separate rolls.</color>" },
            // RV-15 Chaos: Chaos Crash - o sorteio do elemento e o dodge sao testes SEPARADOS.
            { "Hurls a bolt of chaos dealing damage to a single target. Every damage type has a 50% chance to deal *0 damage.",
              "\n<color=#C8B090>The 50% roll only decides whether each element lands; the damage can still be dodged, and those are two separate rolls.</color>" },
            // RV-15 Chaos: Chaos Curse - o sorteio do elemento e o dodge sao testes SEPARADOS.
            { "Curses the target to take damage. Each element has a @50%@ chance to deal *0 damage every turn.",
              "\n<color=#C8B090>The 50% roll only decides whether each element lands; the damage can still be dodged, and those are two separate rolls.</color>" },
            // RV-15 Chaos: Chaos Cut - o sorteio do elemento e o dodge sao testes SEPARADOS.
            { "Summons a whirling blade of chaos in a line. Every damage type has a 50% chance to deal *0 damage.",
              "\n<color=#C8B090>The 50% roll only decides whether each element lands; the damage can still be dodged, and those are two separate rolls.</color>" },
            // RV-15 Chaos: Replicate - o sorteio do elemento e o dodge sao testes SEPARADOS.
            { "Creates a clone of yourself that can cast your abilities. The Replicate Clone explodes for damage on death, each element has a @50%@ chance to deal *0 damage.",
              "\n<color=#C8B090>The 50% roll only decides whether each element lands; the damage can still be dodged, and those are two separate rolls.</color>" },
            // RV-9 buffs: Vengeful - Increases damage dealt by 15%. Stacks up to 10 times, one stack 
            { "Increases damage dealt by 15%.",
              "\n<color=#C8B090>Stacks up to 10 times, one stack per ally killed.</color>" },
            // RV-9 buffs: Vampiric Aura - @Life steal@ increased. Increases life steal by 50%. The aura re
            { "@Life steal@ increased.",
              "\n<color=#C8B090>Increases life steal by 50%. The aura reaches 3 hexes from its source and applies to allies inside it.</color>" },
            // RV-9 buffs: Vampiric Aura - @Life steal@ increased by 5%. The aura reaches 3 hexes from its 
            { "@Life steal@ increased by 5%.",
              "\n<color=#C8B090>The aura reaches 3 hexes from its source and applies to allies inside it.</color>" },
            // RV-9 buffs: Vampiric Aura - @Life steal@ increased by 20%. The aura reaches 3 hexes from its
            { "@Life steal@ increased by 20%.",
              "\n<color=#C8B090>The aura reaches 3 hexes from its source and applies to allies inside it.</color>" },
            // RV-9 buffs: Vampiric Aura - @Life Steal@ increased by 5%. The aura reaches 3 hexes from its 
            { "@Life Steal@ increased by 5%.",
              "\n<color=#C8B090>The aura reaches 3 hexes from its source and applies to allies inside it.</color>" },
            // RV-9 buffs: Vampire Lord Aura - @Life steal@ increased by 50%. The aura reaches 3 hexes from its
            { "@Life steal@ increased by 50%.",
              "\n<color=#C8B090>The aura reaches 3 hexes from its source and applies to allies inside it.</color>" },
            // RV-9 buffs: Unyielding Contender - Grants 50% increased Armor, Magic Armor, and Max Health. Lasts 2
            { "Grants 50% increased Armor, Magic Armor, and Max Health.",
              "\n<color=#C8B090>Lasts 2 turns.</color>" },
            // RV-9 buffs: Titan Bloom - Increases Max Health and Damage by [0]%. Stacks. Stacks up to 5 
            { "Increases Max Health and Damage by [0]%. Stacks.",
              "\n<color=#C8B090>Stacks up to 5 times.</color>" },
            // RV-9 buffs: Thunder Charged - The next damage you deal causes a Thunder Bolt to strike your ta
            { "The next damage you deal causes a Thunder Bolt to strike your target. Stacks.",
              "\n<color=#C8B090>Stacks up to 8 times.</color>" },
            // RV-9 buffs: Spectral Binding - Invincible: it cannot be damaged.
            { "Will leave when finished playing with you.",
              "\n<color=#C8B090>Invincible: it cannot be damaged.</color>" },
            // RV-9 buffs: Shield of Retribution - REMOVIDA em 30/09 (BUG-32): o texto "Shielded from [0] damage."
            // tambem e usado pelo status Shield of Light, que NAO tem explosao - a nota mentia para ele.
            // A skill Shield of Retribution ja descreve a explosao no proprio texto.
            // RV-9 buffs: Seal of Salvation - REMOVIDA em 30/09 (BUG-32): "Restores *0 health per turn." tambem e
            // usado por Regenerate e Lingering Light (aura=nao) - a nota do selo mentia para eles. A skill
            // Seal of Salvation ja diz "All allies within 3 hexes of you heal" no proprio texto.
            // RV-9 buffs: Seal of Protection - It reaches allies within 3 hexes of the seal's bearer.
            { "Decreases damage taken by 10%.",
              "\n<color=#C8B090>It reaches allies within 3 hexes of the seal's bearer.</color>" },
            // RV-9 buffs: Perfect Rage - Also increases the healing this character does by the same perce
            { "Cannot control your character. Increases damage by [0]%. Grants enrage.",
              "\n<color=#C8B090>Also increases the healing this character does by the same percentage.</color>" },
            // RV-9 buffs: Patient Hunter - Gains a stack at the end of your turn, and moving removes the st
            { "Damage increased by 10%, Range increased by 1 per stack.",
              "\n<color=#C8B090>Gains a stack at the end of your turn, and moving removes the status.\nAlso increases the healing this character does by the same percentage.</color>" },
            // RV-9 buffs: Overgrow - Current health is increased by the same percentage and goes back
            { "Increases Damage Dealt and Max Health by 25%.",
              "\n<color=#C8B090>Current health is increased by the same percentage and goes back down when the status ends.\nAlso increases the healing this character does by the same percentage.</color>" },
            // RV-9 buffs: Overflowing Energy - Power of Mana increases the damage and healing of abilities that
            { "Increases @Mana Costs@ by {4,20}%, power of all @Mana Abilites@ by {8,40}% and @Intelligence@ by {3,15}.  <i><color=#808080>The energies of a Mana Spring swell within you!</i></color> ",
              "\n<color=#C8B090>Power of Mana increases the damage and healing of abilities that cost Mana.\nIt does not change how much Mana they cost, it does nothing for abilities that cost no Mana,\nand it does not change the duration or the bonuses of the statuses those abilities apply.</color>" },
            // RV-9 buffs: Overcharge - Lasts 2 turns.
            { "Adds *0 lightning damage to your next basic attack.  Can stack up to 10 times.",
              "\n<color=#C8B090>Lasts 2 turns.</color>" },
            // RV-9 buffs: Otherworldly Tether - While the tether lasts the Dead One is Invincible: it takes no d
            { "The Dead One's tether to this world wanes.  Lasts [0] more round(s).",
              "\n<color=#C8B090>While the tether lasts the Dead One is Invincible: it takes no damage and harmful statuses cannot be applied to it.</color>" },
            // RV-9 buffs: Necronomicon - <color=#808080>You carry the Necronomicon! Changes your @Skeleta
            { "<i><color=#808080>You carry the Necronomicon!</i></color>   Changes your @Skeletal Summons@ into something... stronger. Increases Summon Damage and Health by {5,25}%",
              "\n<color=#C8B090>Your skeletal summons are raised as Undead instead: Undead Berserker, Undead Ranger and Undead Wizard.</color>" },
            // RV-9 buffs: Muse - Mana costs reduced. Allies within 4 hexes of the caster: Muse I 
            { "Mana costs reduced.",
              "\n<color=#C8B090>Allies within 4 hexes of the caster: Muse I reduces Mana Costs by 10%, Muse II by a further 15%.</color>" },
            // RV-9 buffs: Mark of the Alpha - <color=#808080>"Look at me, I'm the alpha now! Changes your @Nat
            { "<i><color=#808080>\"Look at me, I'm the alpha now!</i></color>   Changes your @Nature Summons@ into @Pack Summons@. Increases Summon Damage and Health by {5,25}%",
              "\n<color=#C8B090>Pack summons are fixed instead of random: Timber Wolf, Tundra Wolf and Dire Wolf.</color>" },
            // RV-9 buffs: Ivory Dragon Scale - Gain the ability to shapeshift into a White Dragonkin. <color=#8
            { "Gain the ability to shapeshift into a White Dragonkin.  <i><color=#808080>\"Imbued with a gentle radiance, it serves as a testament to the enduring strength of the forces of light\"</i></color> ",
              "\n<color=#C8B090>While transformed you gain: Dragonkin Holy Slash, Dragonkin Holy Breath and Dragonkin Holy Blast.</color>" },
            // RV-9 buffs: Invincible - Invincible. Cannot take damage.
            { "Invincible.",
              "\n<color=#C8B090>Cannot take damage.</color>" },
            // RV-9 buffs: Inspiring Aura - Damage increased by 60%. The aura reaches 3 hexes from its sourc
            { "Damage increased by 60%.",
              "\n<color=#C8B090>Also increases the healing this character does by the same percentage.</color>" },
            // RV-9 buffs: Immunity - Can only be harmed by destroying Soul Fetishes. Immune to moveme
            { "Can only be harmed by destroying Soul Fetishes.  Immune to movement imparing effects.",
              "\n<color=#C8B090>Also grants immunity to effects that Disable the character (they cannot perform actions).</color>" },
            // RV-9 buffs: Holy Ground - Targets in holy ground receive healing. Heals each turn while th
            { "Targets in holy ground receive healing.",
              "\n<color=#C8B090>Heals each turn while the target stays in the holy ground.</color>" },
            // RV-9 buffs: Greater Heal - o texto "Healed." e compartilhado com Heal e Lesser Heal, que curam
            // por Spell Power (nao full). Nota generica desde 30/09 (BUG-32).
            { "Healed.",
              "\n<color=#C8B090>Restores health. The amount depends on the effect that applied it.</color>" },
            // RV-9 buffs: Glory - \n Also cannot be targeted by harmful skills, and harmful status
            { "Immune to damage.",
              "\n<color=#C8B090>Also cannot be targeted by harmful skills, and harmful statuses do not apply.</color>" },
            // RV-9 buffs: Giant - \n Also increases the healing you do by the same percentage.
            { "Damage and Health increased by 25% Size increased by 25%",
              "\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Fury - \n Also increases the healing you do by the same percentage.
            // RV-43 (01/10): era a UNICA das 9 chaves de aura de shrine SEM a base e SEM a cadeia do
            // Shrine Effect Bonus, e sem dizer que e aura de SHRINE. A base e 25/25 (status.csv:205:
            // `DamageMod:Base:Mathf.Round(25 * (1 + Target["ShrineEffectBonus"] / 100))` e
            // `DamageReduction:Base:Mathf.Round(-25 * (1 + ...))` = +25% de dano tomado), o MESMO
            // modelo das outras 8 (l.933-946, 1002, 1032). A frase de cura FICA: nao e falsa (o motor
            // soma DamageMod a cura) - so entrou o que faltava. A chave continua SO em `TextAppends`
            // (o texto original do jogo nao mudou); `check_chave_compartilhada.py --estrito` = 0.
            { "Damage increased by [0]%. Damage taken increased by [0]%. ",
              "\n<color=#C8B090>Base 25% damage and +25% damage taken; the value shown already includes the Shrine Effect Bonus. Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Evolution - \n Also increases the healing you do by the same percentage.
            { "Damage increased by 5% per stack.  Can stack up to 10 times.",
              "\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Enraged - \n Also immune to being Chilled, Frozen, Stunned or Disabled.
            { "Immune to all movement impairing effects and knockback.",
              "\n<color=#C8B090>Also immune to being Chilled, Frozen, Stunned or Disabled.</color>" },
            // RV-9 buffs: Enduring Evasion - o "2" saiu da nota em 30/09 (BUG-32): o texto e compartilhado com
            // Evasion e Uncanny Evasion, que concedem UMA carga. A contagem fica no texto de cada skill.
            { "Dodging incoming attacks.",
              "\n<color=#C8B090>Guarantees a dodge (100% chance) against incoming attacks; each dodge spends one charge.</color>" },
            // RV-9 buffs: Dodging Strikes - \n Each stack adds another 8%; you gain one stack per strike.
            { "Dodge chance increased by 8%.",
              "\n<color=#C8B090>Each stack adds another 8%; you gain one stack per strike.</color>" },
            // RV-9 buffs: Destructive - Lasts 3 turns. Also increases the healing you do by the same per
            { "Damage increased by 50% ",
              "\n<color=#C8B090>Lasts 3 turns.\nAlso increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Courage of the Ymir - Also works with Fist weapons, and it does not apply while wieldi
            { "Increases your @Action Points@ by @1@. If you are using a One-Handed Sword, Axe, Hammer, Gun, or Wand.  <i><color=#808080>You carry the Speed of the Ymir!</color></i>",
              "\n<color=#C8B090>Also works with Fist weapons, and it does not apply while wielding a two-handed weapon.</color>" },
            // RV-9 buffs: Control Resistance - Also halves the effect of Chilled.
            { "Has a [0]% chance to resist any control effects.",
              "\n<color=#C8B090>Also halves the effect of Chilled.</color>" },
            // RV-9 buffs: Combo Breaker - Each stack is consumed by your next damaging or healing skill.
            { "Damage and healing from non basic skills increased by 10%.",
              "\n<color=#C8B090>Each stack is consumed by your next damaging or healing skill.</color>" },
            // RV-9 buffs: Call of the Reaper - Also increases the healing you do by the same percentage.
            { "Increases @Damage@ by {6,30}%. Increases @Damage Taken@ by 10%.  <i><color=#808080>\"Judge not a life until its final breath, for the Reaper's touch brings truth to death.\"</i></color>  ",
              "\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Break The Ice - It also boosts your first healing, and the bonus is consumed by 
            { "Your first attack in battle deals 100% additional damage.",
              "\n<color=#C8B090>It also boosts your first healing, and the bonus is consumed by your first damaging or healing cast.</color>" },
            // RV-9 buffs: Bottled Wrath - Also increases the healing you do by the same percentage.
            { "Damage increased by 50%. Damage taken increased by 25%.",
              "\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Bottled Rage - Also increases the healing you do by the same percentage.
            { "Damage increased by 30%. Damage taken increased by 15%.",
              "\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Bottled Irritation - Also increases the healing you do by the same percentage.
            { "Damage increased by 10%. Damage taken increased by 5%.",
              "\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Bottled Fury - Also increases the healing you do by the same percentage.
            { "Damage increased by 40%. Damage taken increased by 20%.",
              "\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Bottled Anger - Also increases the healing you do by the same percentage.
            { "Damage increased by 20%. Damage taken increased by 10%.",
              "\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Blood Frenzy - Lasts 2 turns. Also increases the healing you do by the same per
            { "Increases damage dealt and life steal by 25%.",
              "\n<color=#C8B090>Lasts 2 turns.\nAlso increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Battle Fury - Lasts 3 turns. Also increases the healing you do by the same per
            { "Increases damage dealt by 30%.",
              "\n<color=#C8B090>Lasts 3 turns.\nAlso increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Antidote - Lasts 2 turns.
            { "Immune to poisoned.",
              "\n<color=#C8B090>Lasts 2 turns.</color>" },
            // RV-9 debuffs: Visually Impaired - Only ranged attacks and skills lose range; melee range is un
            { "Reduces @Range@ by @3@ per stack.",
              "\n<color=#C8B090>Only ranged attacks and skills lose range; melee range is unchanged.</color>" },
            // RV-9 debuffs: The Bad Bloom - Reapplied each turn to enemies in range of the flower.
            { "Enemies gain 2 stacks of poison.",
              "\n<color=#C8B090>Reapplied each turn to enemies in range of the flower.</color>" },
            // RV-9 debuffs: Test Event Status - Critical Failure - All attributes reduced by 5%.
            { "Critical Failure",
              "\n<color=#C8B090>All attributes reduced by 5%.</color>" },
            // RV-9 debuffs: Taunted - You can only target the taunter, and you are forced to attac
            { "Forced to attack the taunter. Damage reduced by 20%.",
              "\n<color=#C8B090>You can only target the taunter, and you are forced to attack them.</color>" },
            // RV-9 debuffs: Taunted - You can only target the taunter, and you are forced to attac
            { "Taunted.",
              "\n<color=#C8B090>You can only target the taunter, and you are forced to attack them.</color>" },
            // RV-9 debuffs: Stunned - Cannot move or perform actions.
            { "Stunned.",
              "\n<color=#C8B090>Cannot move or perform actions.</color>" },
            // RV-9 debuffs: Slowed - Only abilities whose base cooldown is 2 or more are affected
            { "@Cooldowns@ increased by @1@ turn.",
              "\n<color=#C8B090>Only abilities whose base cooldown is 2 or more are affected: 1-turn cooldowns stay at 1, and basic attacks are unaffected.</color>" },
            // RV-9 debuffs: Sludge Bolt - Only ranged attacks and skills lose range; melee range is un
            { "Lowers movement and range by 1 and lowers Damage by 10% per stack.",
              "\n<color=#C8B090>Only ranged attacks and skills lose range; melee range is unchanged.</color>" },
            // RV-9 debuffs: Sludge - Only ranged attacks and skills lose range; melee range is un
            { "Lowers movement and range by 1 and lowers Damage by 5% per stack.",
              "\n<color=#C8B090>Only ranged attacks and skills lose range; melee range is unchanged.</color>" },
            // RV-9 debuffs: Sleep - Cannot move or perform actions; damage taken is increased by
            { "Asleep.",
              "\n<color=#C8B090>Cannot move or perform actions; damage taken is increased by 50%.</color>" },
            // RV-9 debuffs: Shapeshift: Box - While in the box you cannot move or use abilities.
            { "Shapeshifted into a box. Damage taken increased by 100%.",
              "\n<color=#C8B090>While in the box you cannot move or use abilities.</color>" },
            // RV-9 debuffs: Restricted Range III - Only ranged abilities are affected.
            { "Range is reduced by 6 Hexes.",
              "\n<color=#C8B090>Only ranged abilities are affected.</color>" },
            // RV-9 debuffs: Restricted Range II - Only ranged abilities are affected.
            { "Range is reduced by 4 Hexes.",
              "\n<color=#C8B090>Only ranged abilities are affected.</color>" },
            // RV-9 debuffs: Restricted Range I - Only ranged abilities are affected.
            { "Range is reduced by 2 Hexes.",
              "\n<color=#C8B090>Only ranged abilities are affected.</color>" },
            // RV-9 debuffs: Decaying - Current health is reduced by the same percentage and comes b
            { "Max Health reduced by 25%.",
              "\n<color=#C8B090>Current health is reduced by the same percentage and comes back when the status ends. This cannot kill.</color>" },
            // RV-9 debuffs: Enfeebled - Also reduces the healing this character does by the same per
            { "Reduces @Damage@ by @20%@ per stack.",
              "\n<color=#C8B090>Also reduces the healing this character does by the same percentage.</color>" },
            // RV-9 debuffs: Damage Reduced by 50% - Also reduces the healing this character does by the same per
            { "Damage reduced by 50%.",
              "\n<color=#C8B090>Also reduces the healing this character does by the same percentage.</color>" },
            // RV-9 debuffs: Damage Reduced by 20% - Also reduces the healing this character does by the same per
            { "Damage reduced by 20%.",
              "\n<color=#C8B090>Also reduces the healing this character does by the same percentage.</color>" },
            // RV-9 debuffs: Damage Reduced by 5% - Also reduces the healing this character does by the same per
            { "Damage reduced by 5%.",
              "\n<color=#C8B090>Also reduces the healing this character does by the same percentage.</color>" },
            // RV-9 debuffs: Curse of Weakness - Also reduces the healing this character does by the same per
            { "Damage reduced by 25%.",
              "\n<color=#C8B090>Also reduces the healing this character does by the same percentage.</color>" },
            // RV-9 debuffs: Curse of Frailty - Resistances reduce their damage type by the listed %. If a r
            { "Reduces Physical resistance by 25%.",
              "\n<color=#C8B090>Resistances reduce their damage type by the listed %. If a resistance goes negative, that damage type is amplified instead.</color>" },
            // RV-9 debuffs: Consumption (SKILL - chave exclusiva). A nota de stack morava AQUI desde
            // 30/09 (BUG-32/BUG-31) e foi FUNDIDA na entrada de `TextFixes` em 30/09 (RV-25): a chave
            // estava nas DUAS tabelas e o if/else if fazia a de `TextAppends` nunca rodar. Uma entrada
            // por texto — procurar por "Devour the life force" em `TextFixes`.
            // RV-9 debuffs: Blood Howl - Lasts 2 turns.
            { "Attackers lifesteal for [0]%.",
              "\n<color=#C8B090>Lasts 2 turns.</color>" },
            // RV-9 debuffs: Blind - Skill range is reduced to 1 hex.
            { "Blind.",
              "\n<color=#C8B090>Skill range is reduced to 1 hex.</color>" },
            // RV-9 debuffs: Aura of Lightning - The aura reaches 3 hexes from its source.
            { "*0 lightning damage dealt to enemies within the aura each time they perform an action.",
              "\n<color=#C8B090>The aura reaches 3 hexes from its source.</color>" },
            // RV-9 debuffs: Aura of Frost - The aura reaches 3 hexes from its source, and it damages ene
            { "Deals *0 cold damage per turn while in the aura.",
              "\n<color=#C8B090>The aura reaches 3 hexes from its source, and it damages enemies that start their turns inside it.</color>" },
            // RV-9 debuffs: Aura of Flame - The aura reaches 3 hexes from its source.
            { "[0] fire damage dealt to enemies within the aura.",
              "\n<color=#C8B090>The aura reaches 3 hexes from its source.</color>" },
            // RV-9 debuffs: Aura of Flame - The aura reaches 3 hexes from its source.
            { "*0 fire damage dealt to enemies within the aura.",
              "\n<color=#C8B090>The aura reaches 3 hexes from its source.</color>" },
            // Shapeshift Werewolf - as habilidades da forma saem do `CharacterInfo` do personagem substituido:
            // campo `modelo=` do dump de STATUS (`ModelChangeCharacter.Skills`). Texto dizia
            // apenas "gain new abilities".
            { "Shapeshift into a @Werewolf@. Empowers your basic attack and gain new abilities. Increases @Max Health@ by 10%.",
              "\n<color=#C8B090>While transformed you gain: a stronger basic attack, Blood Howl and Cursed Bite.</color>" },
            // Shapeshift Dire Werewolf - as habilidades da forma saem do `CharacterInfo` do personagem substituido:
            // campo `modelo=` do dump de STATUS (`ModelChangeCharacter.Skills`). Texto dizia
            // apenas "gain new abilities".
            { "Shapeshift into a @Dire Werewolf@. Basic attack and abilities are further empowered. Increases @Max Health@ by 20%.",
              "\n<color=#C8B090>While transformed you gain: a further empowered basic attack, Greater Blood Howl and Greater Cursed Bite.</color>" },
            // Shapeshift Vampire Bat - as habilidades da forma saem do `CharacterInfo` do personagem substituido:
            // campo `modelo=` do dump de STATUS (`ModelChangeCharacter.Skills`). Texto dizia
            // apenas "gain new abilities".
            { "Shapeshift into a @Vampire Bat@. Gain new abilities. @Movement@ increased. Immune to @attacks of opportunity@.",
              "\n<color=#C8B090>While transformed you gain: Energy Drain.</color>" },
            // Break The Ice - o texto ficava vago e o teste do PROPRIO jogo diz o mecanismo:
            // COLD_Status_BreakTheIce
            { "The first time you deal damage or healing in battle, it's effectiveness is increased by 100%.",
              "\n<color=#C8B090>That bonus is consumed by your first damaging cast.</color>" },
            // Cyclone Kick - o texto ficava vago e o teste do PROPRIO jogo diz o mecanismo:
            // o teste do jogo: "the enemy was not pulled adjacent"
            { "Deals *0 physical damage. Pulls enemies within 4 hexes towards you. Targets are crippled for 1 turn. ",
              "\n<color=#C8B090>The pull drags them the whole way: they land on a hex adjacent to you.</color>" },
            // Fire Breath - o texto nao dava o alcance. Fonte: campo `alvos` do `ActionProps`
            // (blast=Distance(Source.Cell) <= 4 + IsSameHemisphere + DistanceFromLine < 3f/2f).
            { "Breath fire dealing *0 fire damage to all enemies in a cone. ",
              "\n<color=#C8B090>The cone reaches 4 hexes from you.</color>" },
            // Frost Breath - o texto nao dava o alcance. Fonte: campo `alvos` do `ActionProps`
            // (blast=Distance(Source.Cell) <= 4 + IsSameHemisphere + DistanceFromLine < 3f/2f).
            { "Deals *0 cold damage each turn.",
              "\n<color=#C8B090>Hits everything in a cone reaching 4 hexes from you.</color>" },
            // Stunning Slam tem texto PROPRIO (cita o {STA=Stunned}); o `Slam` e o `Crushing`
            // Slam dividem um texto identico e ficam com uma entrada so. Fonte do alcance: o
            // campo `alvos` do `ActionProps`.
            { "Deals *0 weapon damage and applies {STA=Stunned} to all enemies within a line for 1 turn.",
              "\n<color=#C8B090>The line reaches 5 hexes from you.</color>" },
            // Slam - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): Cell.Distance(Source.Cell) <= 5 && Cell.IsSameHemisphere(...) && Cell.DistanceFromLine(...) < 3f/2f
            { "Deals *0 weapon damage to all enemies within a line.",
              "\n<color=#C8B090>The line reaches 5 hexes from you.</color>" },
            // Ice Lance - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): ... Distance(Source.Cell) <= 10 ... (mesma forma de linha)
            { "The caster hurls a razor-like shard of ice piercing foes in a line dealing *0 cold damage. ",
              "\n<color=#C8B090>The line reaches 10 hexes from you.</color>" },
            // Breath of Winter - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): ... Distance(Source.Cell) <= 4 ... (cone de 3 hexes de largura)
            { "Conjures the breath of a frost dragon dealing *0 cold damage to all enemies in a cone. ",
              "\n<color=#C8B090>The cone reaches 4 hexes from you.</color>" },
            // Lightning Breath - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): ... Distance(Source.Cell) <= 4 ... (cone de 3 hexes de largura)
            { "Breath lightning dealing *0 lightning damage to all enemies in a cone. ",
              "\n<color=#C8B090>The cone reaches 4 hexes from you.</color>" },
            // Charge - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): rsel=Source.Cell.IsInSixLine(Cell, 7) && Source.Cell.HasDirectPath(Cell)
            { "Charges to the target and deals *0 weapon damage to all enemies in your path.",
              "\n<color=#C8B090>The path is a line of up to 7 hexes.</color>" },
            // Informacao que o texto nao dava e que o usuario observou em jogo: a corrente pode
            // voltar no MESMO alvo. Fonte no codigo (`ActionInfo`): `ProjectileChain` +
            // `ProjectileChainCount` + `ProjectileChainTarget` e, decisivo,
            // `public bool ChainSameTarget = true` - o mesmo alvo pode ser atingido de novo,
            // entao o "5" conta SALTOS, nao inimigos distintos. O teste do jogo corrobora:
            // ele tem dois inimigos e basta ("Chain Lightning chained to the second enemy").
            { "Conjures a lightning bolt that chains up to 5 enemies near the target dealing *0 lightning damage to each target.  ",
              "\n<color=#C8B090>The 5 counts the chain's HOPS, not different enemies: the bolt can hit the same enemy again, so with only two enemies in range it bounces between them.</color>" },
            // "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lugar nenhum.
            // Fonte: `num36 = properties.CostsMana ? source["ManaPowerMod"] : 0f` somado em
            // `num29`, que multiplica dano E cura (`num9 *= num46`). O JOGO usa o termo
            // "power of mana using abilities" em `Forbidden Power` e no proprio `Rainstorm`.
            { "Increase the mana cost of all skills by 20% and increase the power of mana using skills by 40%.",
              "\n<color=#C8B090>Power of Mana increases the damage and healing of abilities that cost Mana.\nIt does not change how much Mana they cost, it does nothing for abilities that cost no Mana,\nand it does not change the duration or the bonuses of the statuses those abilities apply.</color>" },
            // "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lugar nenhum.
            // Fonte: `num36 = properties.CostsMana ? source["ManaPowerMod"] : 0f` somado em
            // `num29`, que multiplica dano E cura (`num9 *= num46`). O JOGO usa o termo
            // "power of mana using abilities" em `Forbidden Power` e no proprio `Rainstorm`.
            { "Increase the mana cost of all skills by an additional 30% and increase the power of mana using skills by an additional 60%.",
              "\n<color=#C8B090>Power of Mana increases the damage and healing of abilities that cost Mana.\nIt does not change how much Mana they cost, it does nothing for abilities that cost no Mana,\nand it does not change the duration or the bonuses of the statuses those abilities apply.</color>" },
            // "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lugar nenhum.
            // Fonte: `num36 = properties.CostsMana ? source["ManaPowerMod"] : 0f` somado em
            // `num29`, que multiplica dano E cura (`num9 *= num46`). O JOGO usa o termo
            // "power of mana using abilities" em `Forbidden Power` e no proprio `Rainstorm`.
            { "Calls down a magical rain that increases potency of Mana using abilities by 50% for allies within the area. Lasts 2 turns.",
              "\n<color=#C8B090>Power of Mana increases the damage and healing of abilities that cost Mana.\nIt does not change how much Mana they cost, it does nothing for abilities that cost no Mana,\nand it does not change the duration or the bonuses of the statuses those abilities apply.</color>" },
            // ---- Escala por NÍVEL (RV-8b-2g) ----
            // Fonte: código do jogo. `GetFlatDamageValue(level, rarity) =
            // Mathf.Ceil(FlatDamageNodes.GetMultipler((int)level) * GetStatRarityMod(rarity))`
            // — é uma CURVA DE NÍVEL, não um atributo. O valor atual já aparece na tooltip
            // (é o [0]); o que faltava era dizer COM O QUE ele escala, que era a pergunta
            // legítima do jogador ("invisto em Might para isso melhorar?").
            // São as 5 skills do jogo que usam essa curva (Huntsman I/II, Thorns I/II e
            // Vengeful Shadows); a chave "Physical damage increased by [0]." cobre as duas
            // Huntsman porque as duas escalam igual.
            { "Grants [0] Return Physical Damage.",  "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Grants an additional [0] Return Physical Damage.",  "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Grants [0] Return Shadow Damage.",  "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Physical damage increased by [0].",  "\n<color=#C8B090>Scales with your character level.</color>" },

            // Segunda leva (RV-8b-2i): a varredura `tools/check_scaling.py` percorreu as
            // fórmulas de TODAS as skills e achou 9 que escalam com `Source.Level` sem
            // dizer isso no texto. Cinco já estavam cobertas acima (a curva FlatDamage) e
            // estas são as outras. A `Shapeshift Dragonkin` entra pela tabela de
            // correções: quem está nas DUAS tabelas só executa a correção, então uma
            // explicação aqui ficaria código morto.
            // Não cobertas de propósito: Attack Power (70 skills) e Spell Power (~65) —
            // são o caminho padrão de dano, o valor já aparece na tooltip e repetir
            // "escala com ataque" em 135 skills seria ruído, não informação.
            { "@Intelligence@ grants [0] @Armor@ and @Magic Armor@ per point.  Current Bonus: [1]",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Damage caused steals [0] points of @Dexterity@. Lasts the entire battle. Stacks up to 10 times.",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Damage caused steals [0] points of @Intelligence@. Lasts the entire battle. Stacks up to 10 times.",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Damage caused steals [0] points of @Might@. Lasts the entire battle. Stacks up to 10 times.",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Envelopes the target in living vines that increase @armor@ and @magic armor@ by [0] and causes the target to regenerate *0 @health@ each turn.",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Increases all attributes by [0]. In addition, 10% of your highest attribute value is added to all other attributes.  Current Bonus: [1]",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Encases the friendly target in a dome of ice granting [0] Armor and Magic Armor for the duration. Immobilizes the target.",
              "\n<color=#C8B090>Scales with your character level.</color>" },

            // ---- O que cada INVOCAÇÃO faz (RV-8b-2h) ----
            // Fonte: os assets do jogo, via dump. `ActionInfo.Summons` é a lista de
            // CharacterInfo e `CharacterInfo.SkillsAndAI[].Skill` são as habilidades da
            // criatura - a tooltip só diz o NOME de cada bicho, nunca o que ele faz.
            // `herdaStats=nao` em todas estas: o invocado NÃO herda seus atributos, então
            // nenhuma delas escala com o que você investe.
            // Uma linha por criatura: com três nomes e suas habilidades numa linha só o
            // texto fica ilegível no tooltip. O \n é o mesmo separador que o jogo usa nos
            // textos dele; e só ASCII, para não depender de glifo na fonte do jogo.
            { "Summons a Raven, Coyote, or Raccoon to fight for you.",
              "\n<color=#C8B090>One is summoned at random:\n- Raven: Melee Attack, Evasion\n- Raccoon: Melee Attack, Steal Action\n- Coyote: Melee Attack, Cripple\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summons a Stag, Wolf, or Boar to fight for you.",
              "\n<color=#C8B090>One is summoned at random:\n- Stag: Melee Attack, Stunning Kick\n- Wolf: Melee Attack, Howl\n- Boar: Melee Attack, Fracture\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summons a Bear, Moose, or Panther to fight for you.",
              "\n<color=#C8B090>One is summoned at random:\n- Bear (a Grizzly): Stunning Slam, Wild Cleave\n- Moose: Melee Attack, Ground Slam\n- Panther: Melee Attack, Shadow Walk\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summons a Tundra Wolf to fight for you.",
              "\n<color=#C8B090>Tundra Wolf: Melee Attack, Howl\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summons a Dire Wolf to fight for you.",
              "\n<color=#C8B090>Dire Wolf: Melee Attack, Blood Howl\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summon a grizzly to fight your enemies.",
              "\n<color=#C8B090>Grizzly: Stunning Slam, Wild Cleave\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summon a wolf to fight your enemies.",
              "\n<color=#C8B090>Wolf: Melee Attack, Howl\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summon a Raven to fight your enemies. ",
              "\n<color=#C8B090>Raven: Melee Attack, Evasion\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Raise an Undead Ranger to fight by your side.",
              "\n<color=#C8B090>Undead Ranger: Ranged Attack, Hide In Shadows\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Raise an Undead Berserker to fight by your side.",
              "\n<color=#C8B090>Undead Berserker: Bleeding Cleave\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },

            // Brambles e Ice Wall NAO invocam bicho: sao objetos destrutiveis que bloqueiam
            // hexes. Passam pelo MESMO caminho de beneficio dos bichos (CreateDestructible
            // -> ProcessSummonMasterStats, com `casterStatsToBenefitFrom` setado), entao
            // tambem ganham Might/Int. A diferenca que importa e outra: entram com
            // `addToSummonList: false` - NAO contam como summon, e efeitos que contam
            // invocacoes (Ecosystem) nao os veem. Por isso a frase deles fala de "nao conta
            // como summon" em vez de repetir a dos bichos.
            // A flag `BenefitFromCasterStats` e lida SO neste caminho de destrutivel (l.41998
            // -> CreateDestructible): NAO governa os bichos, que recebem os efeitos do dono
            // incondicionalmente no CreateSummon. Chama-la de "herdaStats" foi rotulo meu e
            // induzia a conclusao errada ("nao herda = nao escala").
            { "Summon brambles to block 4 hexes. Attackers will take physical damage when striking the brambles. Lasts 4 turns.",
              "\n<color=#C8B090>Benefits from your Might and Intelligence, but does not count as a summon.</color>" },
            { "Summon pillars of ice to block 4 hexes blocking enemy's line of sight. Attackers take cold damage.  Lasts 4 turns.",
              "\n<color=#C8B090>Benefits from your Might and Intelligence, but does not count as a summon.</color>" },

            // ---- Omissao: o texto nao pode estar certo pela METADE (RV-8b-3, 29/09) ----
            // Regra do usuario: se o resultado depende de algo que o texto nao diz, e defeito.
            // Achado por tools/check_omissao.py (classes O1..O6).
            // Ascendancy: o status concede 20% e DURA 5 TURNOS; a skill so dizia o 20%.
            { "Increases the target allies' stats by 20%.",
              "\n<color=#C8B090>Lasts 5 turns.</color>" },
            // Touch of Chaos: REVERTIDO a pedido do usuario (29/09). A arvore do Chaos e
            // divertida justamente por NAO revelar os resultados - Coin of Chaos, Benevolence,
            // Malevolence, Hurting e Helping seguem omitidos DE PROPOSITO. Nao "corrigir"
            // isto de novo: e design, nao omissao. Ver a excecao do Chaos na regra de omissao.

            // ---- O que INFLUENCIA a cura e o dano holy (arvore Light, 29/09) ----
            // Fonte: GetActionDamage, l.38843-38859. O multiplicador da cura e o MESMO do
            // dano holy:
            //     float num24 = source["DamageModHealing"];         // <- "Holy Power"
            //     float num26 = target?["HealingReceivedBonus"];
            //     num7 *= 1f + num24 / 100f;    // dano holy
            //     num9 *= 1f + num24 / 100f;    // cura
            //     num9 *= 1f + num26 / 100f;    // cura, pelo lado do ALVO
            // A BASE da cura vem de `Source.SpellPower('Light')` - e `SpellPower(type)`
            // devolve **`AttackPower`** (l.36040): entao escala com arma/Might, NAO com
            // Inteligencia. As curas por % de vida (`Healing Hand`, `Divine Intervention`)
            // nao tem essa base e por isso levam so a linha do Holy Power.
            // "Holy Power" e o nome que o PROPRIO JOGO usa: `Empowered Light` diz "Increases
            // Holy Power and Healing Received by 10%" e o efeito dela e `DamageModHealing` -
            // o mesmo atributo que multiplica a cura aqui.
            { "Restores target's health by *0.",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "Restores *0 health to all allies within 2 hexes of target.",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.\nReduced by effects that lower the target's healing received.\nThe 2-hex area is centred on the chosen TARGET, not on the caster.</color>" },
            { "Target restores *0 health per turn. ",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "All allies within 3 hexes of you heal for *0 per turn. ",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "Restores the target to full health.",
              "\n<color=#C8B090>Healing scales with your Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "Summons a radiant light applying {STA=Blind} to the target dealing *0 Holy damage.",
              "\n<color=#C8B090>Damage scales with your Attack Power and Holy Power.</color>" },
            { "Breathe out a stream of holy light dealing *0 holy damage to all enemies and healing *0 to all allies in range.",
              "\n<color=#C8B090>Damage and healing scale with your Attack Power and Holy Power.\nHealing is reduced by effects that lower the target's healing received.</color>" },
            { "Expel a powerful celestial light blinding enemies and dealing *0 holy damage to all enemies and healing *1 to all allies in range.",
              "\n<color=#C8B090>Damage and healing scale with your Attack Power and Holy Power.\nHealing is reduced by effects that lower the target's healing received.</color>" },
            // Fechamento do lote da Light (29/09): quatro que tambem escalam e nao diziam.
            // `Holy Ground` era o caso mais enganoso - o STATUS dele guarda o valor na chave
            // `HolyDamage`, mas o teste do proprio jogo prova que CURA:
            //   Assert(caster.Health > hp, "Holy Ground did not heal the caster standing on it")
            // A chave e so o slot de armazenamento; o multiplicador de Holy Power entra
            // igual (num7 *= 1 + DamageModHealing/100).
            { "Consecrate an area of ground to heal allies that stand upon it. Heals *0 per turn for 3 turns. ",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.</color>" },
            { "Any target you heal with Cure, Regenerate, Healing Hand, Mass Cure, or Divine Intervention also receives an additional healing over time effect restoring *0 health for 3 turns.",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.</color>" },
            { "Calls down a shield that protects the target absorbing *0 damage. ",
              "\n<color=#C8B090>Absorption scales with your Attack Power and Holy Power.</color>" },
            { "Conjures a shield imbued with holy flame absorbing *0 damage. Upon shield depletion, it explodes and deals *0 holy damage to all foes in a 3 hex radius.",
              "\n<color=#C8B090>Damage and absorption scale with your Attack Power and Holy Power.</color>" },

            // ---- Explicações de mecânica: powerups e status (BT-3..BT-8) ----
            // Fonte: o código do jogo (Assembly-CSharp, decompilado). Cada bloco abaixo
            // diz no próprio comentário qual atributo/método confirma a mecânica.
            { "+ 20% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },
            { "+ 40% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },
            { "+ 60% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },
            { "+ 80% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },
            { "+ 100% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },

            // Gold Find — MECÂNICA VERIFICADA NO CÓDIGO (confirmação empírica via RoguelikeDebugger):
            //   - ApplyGoldModifiers lê character["GoldMod"] somado à party e multiplica o ouro
            //   - usado na distribuição de ouro pós-batalha (PostBattleManager), recompensas de
            //     aventura/quest e ouro de eventos
            //   - "GoldMod" é um asset CharacterAttribute; efeitos de powerup viram contribuições
            //     de atributo (mecanismo provado na BT-3)
            { "+ 10% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },
            { "+ 20% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },
            { "+ 30% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },
            { "+ 40% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },
            { "+ 50% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },

            // Damage and Healing — VERIFICADO: soma no atributo "DamageMod" base, que entra
            // em (1 + (DamageMod + DamageMod<Tipo> + ManaPowerMod)/100) × (1+AbilityPower/100)
            // para TODOS os tipos de dano E para a cura (DamageModHealing usa a mesma base).
            { "+ 5% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },
            { "+ 10% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },
            { "+ 15% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },
            { "+ 20% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },
            { "+ 25% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },

            // Damage Reduction — VERIFICADO: atributo "DamageReduction" vira camada
            // multiplicativa (1 - (DamageReduction + Resilience + TakeCover)/100) na cadeia
            // de redução de dano. Texto GERADO DINAMICAMENTE (BuildDamageReductionNote) com
            // a ordem real do GlobalSettings (padrão: redução geral → resists → armadura).

            // Movement — VERIFICADO: soma ao atributo "FreeMovementPoints" (movimento por turno).
            // (RV-5: versão não-redundante — o original já diz "additional movement")
            { "Gain 1 additional movement",  "\n<color=#C8B090>Each movement point lets you move one extra hex per turn.</color>" },
            { "Gain 2 additional movement",  "\n<color=#C8B090>Each movement point lets you move one extra hex per turn.</color>" },

            // Range — VERIFICADO: o powerup alimenta "RangeTypeAdderRanged" (o melee não
            // muda — dump: RangeMelee=0, RangeRanged=2 com Lv2). Texto reflete ranged.
            { "Gain 1 additional range",  "\n<color=#C8B090>Increases the range of your ranged attacks and skills. Does not apply to certain skills.</color>" },
            { "Gain 2 additional range",  "\n<color=#C8B090>Increases the range of your ranged attacks and skills. Does not apply to certain skills.</color>" },

            // Skill Options — VERIFICADO: RoguelikeManager.GetSkillChoices(numOpcoesBase +
            // character["AdditionalRoguelikeSkillOptions"]) → mais opções na escolha de skill.
            { "Skill Options +1",  "\n<color=#C8B090>Increases the number of skill choices offered when leveling up.</color>" },
            { "Skill Options +2",  "\n<color=#C8B090>Increases the number of skill choices offered when leveling up.</color>" },

            // Attribute Points — VERIFICADO: UnspentStatPoints = base + (Level-1) ×
            // (NumStatsPerNewLevel + AdditionalRoguelikeAttributesPointsPerLevel).
            { "Attribute Points Per Level +1",  "\n<color=#C8B090>Grants additional attribute points each time you level up.</color>" },
            { "Attribute Points Per Level +2",  "\n<color=#C8B090>Grants additional attribute points each time you level up.</color>" },
            { "Attribute Points Per Level +3",  "\n<color=#C8B090>Grants additional attribute points each time you level up.</color>" },

            // Resists — VERIFICADO: dano do elemento × (1 - Resist/100), camada multiplicativa
            // na cadeia de redução (case DamageReductionCalcOrder.Resists em ApplyAction).
            { "[[ResistCold]] +10%",  "\n<color=#C8B090>Reduces Cold damage you take.</color>" },
            { "[[ResistCold]] +15%",  "\n<color=#C8B090>Reduces Cold damage you take.</color>" },
            { "[[ResistCold]] +20%",  "\n<color=#C8B090>Reduces Cold damage you take.</color>" },
            { "[[ResistFire]] +10%",  "\n<color=#C8B090>Reduces Fire damage you take.</color>" },
            { "[[ResistFire]] +15%",  "\n<color=#C8B090>Reduces Fire damage you take.</color>" },
            { "[[ResistFire]] +20%",  "\n<color=#C8B090>Reduces Fire damage you take.</color>" },
            { "[[ResistLightning]] +10%",  "\n<color=#C8B090>Reduces Lightning damage you take.</color>" },
            { "[[ResistLightning]] +15%",  "\n<color=#C8B090>Reduces Lightning damage you take.</color>" },
            { "[[ResistLightning]] +20%",  "\n<color=#C8B090>Reduces Lightning damage you take.</color>" },
            { "[[ResistPhysical]] +10%",  "\n<color=#C8B090>Reduces Physical damage you take.</color>" },
            { "[[ResistPhysical]] +15%",  "\n<color=#C8B090>Reduces Physical damage you take.</color>" },
            { "[[ResistPhysical]] +20%",  "\n<color=#C8B090>Reduces Physical damage you take.</color>" },

            // Summon Damage & Health — VERIFICADO: atributos SummonDamageMod/SummonHealthMod.
            { "+ 5% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },
            { "+ 10% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },
            { "+ 15% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },
            { "+ 20% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },
            { "+ 25% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },

            // Skill Tree Removal — VERIFICADO: remove árvores do pool de escolhas;
            // MinimumTreesRemaining=4; texto "can only be chosen at level 1" vem do próprio jogo.
            { "Skill Tree Removals +1",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +2",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +3",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +4",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +5",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +6",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +7",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +8",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            // RV-19 shrines — familia de auras de shrine: base + cadeia do Shrine Effect Bonus.
            // A chave do Flame nao tem numero no texto: a LINHA recebe o numero DINAMICO no postfix
            // (RV-26) e a NOTA carrega o resto.
            // TX-1 (01/10) — TODAS as notas desta familia foram ENXUGADAS (pedido do dono, com print):
            // o VALOR fica EM CIMA (a linha branca do jogo e, no Flame, a lista por alvo colada nela) e a
            // explicacao cabe em UMA frase. "Textos muito grandes nao necessariamente sao bons".
            // O QUE SAIU do tooltip e VIVE no documento (docs/cobertura/revisao/RV-19-shrines.md
            // §2.2/§3/§4.3/§6.1): a tabela de % por tipo de inimigo, a lista de fontes do Shrine Effect
            // Bonus (Omnism I/II, perk Worship, Horn of Devotion), o "Minimum 1" do Flame e a repeticao
            // da projecao — tooltip nao e lugar de tabela.
            // O QUE NAO PODE CAIR e continua em toda nota que fala do dano: (1) o numero do Flame e o
            // dano de RETORNO de quem ATACA; (2) ele sai da vida maxima DO ATACANTE, nao da de quem
            // apenas esta na aura; (3) e PRE-REDUCAO de dano.
            // RV-30 (30/09): a lista de fontes do bonus ganhou o PERK do jogo "Worship" ("100% increased
            // effect from Shrines", valor 100 nos assets, ao lado do CharacterInfo T2_Worshiper) porque
            // era exatamente o caso do usuario em jogo: com o perk, a aura sai ×2 e a nota nao explicava
            // o dobro (parecia numero inventado pelo mod). Nenhum numero foi "ajustado" — o valor da
            // expressao do jogo e o do personagem; o que faltava era a procedencia estar completa.
            // RV-34 (30/09) — O FATOR DO ShrineEffectBonus ENTRA NAS DUAS AURAS DE PERIGO, e a nota do
            // FLAME volta a falar dele. O RV-26/33 tinha concluido que o `Source` da formula era o
            // personagem VAZIO do shrine (`Source = Root.WorldCharacter`, o que o hover entrega —
            // l.214179/214182) e que, por isso, `(1 + Source["ShrineEffectBonus"]/100)` valia 1: o fator
            // foi OMITIDO das duas formulas. O dono do jogo MEDIU em jogo (30/09): com o perk `Worship`
            // (+100 em `ShrineEffectBonus`, um PERK DO PERSONAGEM) o dano por turno DOBRA. O fator vale 2
            // e quem ele le e o PROPRIO personagem que leva o dano (a vitima no Decay; cada alvo da lista
            // no Flame). Correcao no `ShrineAuraPatch`: as constantes passaram a ser o RHS do asset byte
            // a byte e a avaliacao usa `Source` = `Target` = o personagem avaliado; o prefix tambem troca
            // o Source VAZIO do shrine pelo receptor (as expressoes dos status do Decay e do Flame leem
            // `Source[...]`: sem isso a linha diria "Take 10%" enquanto o dano real dobra). Medicao em
            // jogo vence leitura de asset — hierarquia de fontes do projeto.
            // RV-33 (30/09) — DE QUEM E A VIDA MAXIMA: o dano do Flame e % da vida maxima DE QUEM
            // DISPARA a aura, o ATACANTE (TriggerType `OnGettingHitDamaging` no asset + Condition
            // `Source.IsEnemy(Target)` + `Targets = Cell.IsCurrentHex(Target)`; e a chamada do motor e
            // `target.ProcessSkillTriggers(source, ..., OnGettingHitDamaging)` — decompilado l.40075 —
            // com `this` = quem FOI acertado e o `target` do gatilho = o atacante). Ou seja: a acao roda
            // na celula do atacante. RV-43 (01/10): no HOVER ninguem sabe quem vai atacar, entao a lista
            // por alvo e uma PROJECAO — cada ocupante da aura e projetado COMO SE fosse o atacante, e o
            // numero sai da vida maxima DELE (hipotese explicita, aceita pelo dono). O texto da nota diz
            // isso ("if this character attacked") e NAO afirma mais que a vida usada nao e a de quem esta
            // na aura: essa frase contradizia a propria lista. Prova
            // completa no cabecalho do ShrineAuraPatch. Aqui fica so o texto FIXO (a regra e a escala);
            // a lista DINAMICA por alvo (`FraseAlvosDoFlame`) entra DENTRO deste mesmo bloco de cor para
            // nao existirem dois blocos iguais. RV-34: o numero E a % saem com o MESMO fator do
            // ShrineEffectBonus (o do proprio personagem avaliado) e o texto diz, em uma marca curta, que
            // o valor e ANTES DAS REDUCOES DE DANO — pedido explicito do dono do jogo (sem isso o numero
            // parece prometer o dano que aparece na tela e nao bate).
            // TX-1 (01/10): a nota virou UMA frase ("The attacker takes this damage in return, based on
            // its own Max Health and not on the health of the one it attacked, before damage reduction.")
            // e a LISTA por alvo subiu para o comeco do bloco (`FraseAlvosDoFlame`). Os tres fatos
            // acima estao, palavra por palavra, nessa frase — nenhum numero e nenhuma afirmacao de
            // mecanica saiu dela; o que saiu foi a TABELA (percentuais por tipo, fontes do bonus,
            // minimo 1), que ja esta no documento.
            { "Attackers take Fire Damage.",
              "\n<color=#C8B090>The attacker takes this damage in return, based on its own Max Health and not on the health of the one it attacked, before damage reduction.</color>" },
            // RV-33/RV-34 (30/09) — o dano do Decay e % da vida maxima DO PROPRIO PORTADOR da aura (Target
            // do proc = quem esta na aura; o gatilho roda no inicio do turno DELE) VEZES o ShrineEffectBonus
            // DELE (RV-34: medido em jogo, com Worship dobra). O numero literal sai na linha
            // (LinhaDecayComValor); aqui ficam a escala, a origem do bonus, o fato de nao existir minimo e
            // a marca de que o valor e ANTES DAS REDUCOES DE DANO.
            // TX-1 (01/10): a nota virou UMA frase ("Raw damage, before damage reduction: your own Max
            // Health multiplied by the percentage shown, which already includes your own Shrine Effect
            // Bonus, and it can be 0."). O que saiu foi a TABELA (% por tipo de inimigo e fontes do
            // bonus — documento RV-19 §3/§4.3). NO DECAY OS TRES FATOS DO FLAME NAO VALEM e afirmar
            // qualquer um deles seria FALSO: aqui quem leva o dano e quem esta NA AURA (o proc roda no
            // comeco do turno DELE), a vida maxima lida e a DELE e nao ha atacante nenhum. O que a nota
            // preserva e a vida maxima DO PORTADOR ("your own Max Health"), o fator do bonus DELE e a
            // marca de PRE-REDUCAO — sem os dois primeiros o numero pareceria sair da vida de outra
            // pessoa (erro da familia, corrigido em RV-33/RV-34).
            { "Take [0]% of your Max Health in Shadow Damage per turn.",
              "\n<color=#C8B090>Raw damage, before damage reduction: your own Max Health multiplied by the percentage shown, which already includes your own Shrine Effect Bonus, and it can be 0.</color>" },
            { "Damage increased by [0]%. ",
              "\n<color=#C8B090>Base 20%; the value shown already includes the Shrine Effect Bonus.</color>" },
            { "Reduces Damage taken by [0]%. ",
              "\n<color=#C8B090>Base 20%; the value shown already includes the Shrine Effect Bonus.</color>" },
            { "Critical hit chance increased by [0]%.",
              "\n<color=#C8B090>Base 20%; the value shown already includes the Shrine Effect Bonus.</color>" },
            { "Increases dodge chance by [0]%.",
              "\n<color=#C8B090>Base 20%; the value shown already includes the Shrine Effect Bonus.</color>" },
            { "Lifesteal increased by [0]%.",
              "\n<color=#C8B090>Base 8%; the value shown already includes the Shrine Effect Bonus.</color>" },
            { "Decreases the cost of mana using abilities by [0]%.",
              "\n<color=#C8B090>Base 50%; the value shown already includes the Shrine Effect Bonus.</color>" },
            { "Your attacks have a [0]% chance to stun the target.",
              "\n<color=#C8B090>Base 20%; the value shown already includes the Shrine Effect Bonus.</color>" },
        };

        // Primeiras correções reais de texto — apenas digitação/espaçamento observados
        // no jogo, sem nenhuma afirmação de gameplay. Chave = texto original exato.
        private static readonly Dictionary<string, string> TextFixes = new Dictionary<string, string>
        {
            // RV-11/RV-10: Warmachine Gauntlet
            { "10% chance to cast Level [level value] {SKL=Meteor} when Striking.",
              "10% chance to cast Level [level value] {SKL=Meteor} when striking." },
            // RV-11/RV-10: Twisted Dagger
            { "Striking with this weapon applies 2 stack of Poison.",
              "Striking with this weapon applies 2 stacks of Poison." },
            // RV-11/RV-10: Potion of Vigor
            { "Vitality increased by 10 for 5 turns.",
              "Vitality increased by 5 for 5 turns." },
            // RV-11/RV-10: Ksvaldir
            { "Applies Hunger Ksvaldir: Sacrifices 10% of your max health per turn.",
              "Applies Hunger of Ksvaldir: Sacrifices 10% of your max health per turn." },
            // RV-11/RV-10: Goblin Bone Axe
            { "Weapon attacks apply 1 stacks of bleeding.",
              "Weapon attacks apply 1 stack of bleeding." },
            // RV-11/RV-10: Fallen Cleric Robes
            { "10% chance on hit to cast Level [level value] {SKL=Consumption}",
              "10% chance on hit to cast Level [level value] {SKL=Consumption}." },
            // RV-11/RV-10: Dragon Fist
            { "5% chance to cast Level [level value] {SKL=Thunder Bolt} when hitting an enemy with any ability.  5% chance to cast Level [level value] {SKL=Frost Nova} when hitting an enemy with any ability.  5% chance to cast Level [level value] {SKL=Fireball} when hitting an enemy with any ability.",
              "5% chance to cast Level [level value] {SKL=Thunder Bolt} when hitting an enemy with any ability. 8% chance to cast Level [level value] {SKL=Frost Nova} when hitting an enemy with any ability. 5% chance to cast Level [level value] {SKL=Fireball} when hitting an enemy with any ability." },
            // RV-11/RV-10: Dead One's Phylactery
            { "Grants the passive Grants the passive skill {SKL=Lich Lord}.",
              "Grants the passive skill {SKL=Lich Lord}." },
            // RV-11/RV-10: Ancient Staff
            { "Increases the power and cost of all @Mana Abilites@ by 5% of your Max Mana.",
              "Increases the power and cost of all @Mana Abilities@ by 5% of your Max Mana." },
            // RV-11/RV-10: Savior
            { "Holy power increased by [15]%",
              "Holy Power increased by [15]%" },
            // RV-11/RV-10: Physician
            { "Holy power increased by [6]%",
              "Holy Power increased by [6]%" },
            // RV-11/RV-10: Mender
            { "Holy power increased by [3]%",
              "Holy Power increased by [3]%" },
            // RV-11/RV-10: Healer
            { "Holy power increased by [9]%",
              "Holy Power increased by [9]%" },
            // RV-11/RV-10: Doctor
            { "Holy power increased by [12]%",
              "Holy Power increased by [12]%" },
            // RV-14 terminologia: Regenerating | max life -> max health

            { "5% of your max life regenerated per turn.",
              "5% of your max health regenerated per turn." },
            // RV-14 terminologia: Shaman Aura | maximum mana -> max mana

            { "Recover [0]% of maximum mana each turn. ",
              "Recover [0]% of max mana each turn. \n<color=#C8B090>Base 10%; the value shown already includes the Shrine Effect Bonus.</color>" },
            // RV-14 terminologia: Curse of the Reaper | max life -> max health

            { "Increases @Life Steal@ by 6%. Reduces @Max Life@ by 15%.  <i><color=#808080>\"A thirst so deep, it blurs the lines, Til we're but marionettes of our own designs.\"</i></color>",
              "Increases @Life Steal@ by 6%. Reduces @Max Health@ by 15%.  <i><color=#808080>\"A thirst so deep, it blurs the lines, Til we're but marionettes of our own designs.\"</i></color>" },
            // RV-14 terminologia: Berserker's Rage | max life -> max health

            { "Increases Damage and Damage Taken by 25%. Increases max life by 15%.",
              "Increases Damage and Damage Taken by 25%. Increases max health by 15%." },
            // RV-14 terminologia: Sustenance II | max life -> max health

            { "Consuming any Globule heals you for 20% of max life and mana.",
              "Consuming any Globule heals you for 20% of max health and mana." },
            // RV-14 terminologia: Sustenance I | max life -> max health

            { "Consuming any Globule heals you for 8% of max life and mana.",
              "Consuming any Globule heals you for 8% of max health and mana." },
            // RV-14 terminologia: Gathering Storm | maximum mana -> max mana

            { "Increases @maximum mana@ by 20%.",
              "Increases @max mana@ by 20%." },
            // RV-14 terminologia: Ecosystem | max life -> max health

            { "Every summon active increases the @Max Life@, @Damage@ and @Healing@ of you and your summons by 5%.",
              "Every summon active increases the @Max Health@, @Damage@ and @Healing@ of you and your summons by 5%." },
            // RV-14 terminologia: Soul Fracture | maximum health -> max health
            { "@Maximum health@ and @maximum mana@ lowered by 25%.",
              "@Max health@ and @max mana@ lowered by 25%." },
            // RV-14 terminologia: Seraph Aura | maximum health -> max health
            { "Recover [0]% of maximum health each turn. ",
              "Recover [0]% of max health each turn. \n<color=#C8B090>Base 10%; the value shown already includes the Shrine Effect Bonus.</color>" },
            // RV-14 terminologia: Salvation | maximum health -> max health
            { "@Maximum health@ increased by 10% per stack.",
              "@Max health@ increased by 10% per stack." },
            // RV-14 terminologia: Immortal Night | maximum health -> max health
            { "@Maximum health@ and @maximum mana@ lowered by 25% per stack.",
              "@Max health@ and @max mana@ lowered by 25% per stack." },
            // RV-14 terminologia: Focused Strike | damage received -> damage taken
            { "Increases damage received by 20%.",
              "Increases damage taken by 20%." },
            // RV-14 terminologia: Warrior's Boon | maximum health -> max health
            { "Heals 25% of your maximum health and removes all negative statuses. Can be used when Disabled.",
              "Heals 25% of your max health and removes all negative statuses. Can be used when Disabled." },
            // RV-14 terminologia: Reaper's Toll | maximum health -> max health
            { "Every enemy that dies heals you for 10% of your maximum health.",
              "Every enemy that dies heals you for 10% of your max health." },
            // RV-14 terminologia: Rage | damage received -> damage taken
            { "Increases @Damage dealt@ and @Max Life@ by 15%.  Increases @damage received@ by 15%.",
              "Increases @Damage dealt@ and @Max Health@ by 15%.  Increases @damage taken@ by 15%." },
            // RV-14 terminologia: Into the Fray | maximum health -> max health
            { "For every enemy within 3 hexes of your character gain 3% @increased Damage@ and 3% @Maximum Health@.",
              "For every enemy within 3 hexes of your character gain 3% @increased Damage@ and 3% @Max Health@." },
            // RV-14 terminologia: Hunger | maximum health -> max health
            { "Grants 10% @mana steal@.  Sacrifices 10% maximum health per turn.",
              "Grants 10% @mana steal@.  Sacrifices 10% max health per turn." },
            // RV-14 terminologia: Endless Night | maximum health -> max health
            { "Gain 2% of your maximum health as @Additional Shadow Damage@.   Current Shadow Damage Increase: [0].",
              "Gain 2% of your max health as @Additional Shadow Damage@.   Current Shadow Damage Increase: [0]." },
            // RV-14 terminologia: Dark Pact | maximum health -> max health
            { "Increase the effectiveness of your damage and healing skills by 30%.   Maximum health reduced by 20%.",
              "Increase the effectiveness of your damage and healing skills by 30%.   Max health reduced by 20%." },
            // RV-14 terminologia: Consumption | maximum health -> max health
            // RV-25 (30/09): esta chave tambem existia em `TextAppends` (a nota de stack) e, como o
            // lookup e if/else if na MESMA chave, a entrada de `TextAppends` NUNCA rodava: a nota nao
            // aparecia em jogo e NAO havia erro no log. UMA entrada por texto: fica esta, que carrega o
            // fix de terminologia do RV-14, com a nota FUNDIDA nela no formato do `AnexarNota` (uma
            // linha em branco + bloco na cor do jogo). A entrada de `TextAppends` foi apagada.
            { "Devour the life force of all enemies within 2 hexes dealing *0 Shadow Damage and giving you 10% @Maximum Health@ for each enemy effected.",
              "Devour the life force of all enemies within 2 hexes dealing *0 Shadow Damage and giving you 10% @Max Health@ for each enemy effected.\n\n<color=#C8B090>Each stack grants another 10% Max Health; you gain one stack per enemy hit.</color>" },
            // RV-14 terminologia: Bone Collector | maximum health -> max health
            { "Every enemy slain grants 6% @maximum health@ and @Increased Damage@.  Lasts the duration of the battle.  Stacks up to 5 times.",
              "Every enemy slain grants 6% @max health@ and @Increased Damage@.  Lasts the duration of the battle.  Stacks up to 5 times." },
            // RV-14 terminologia: Bless | maximum health -> max health
            { "Bless all allies within 5 hexes.  Increases @damage@, @maximum health@, and @maximum Mana@ by 10%.",
              "Bless all allies within 5 hexes.  Increases @damage@, @max health@, and @max mana@ by 10%." },
            // RV-14 terminologia: Berserker's Rage | damage received -> damage taken
            { "Increases @Damage dealt@ and @damage received@ by 25%. Increases @Max Life@ by 15%.",
              "Increases @Damage dealt@ and @damage taken@ by 25%. Increases @Max Health@ by 15%." },
            // RV-14 terminologia: Saint | Divine Resistance -> Holy Resistance
            { "Divine Resistance increased by 5%",
              "Holy Resistance increased by 5%" },
            // RV-14 terminologia: God | Divine Resistance -> Holy Resistance
            { "Divine Resistance increased by 15%",
              "Holy Resistance increased by 15%" },
            // RV-14 terminologia: Angel | Divine Resistance -> Holy Resistance
            { "Divine Resistance increased by 10%",
              "Holy Resistance increased by 10%" },
            // RV-9 buffs: Toxic
            { "Applies @2@ @poison@ when striking Applies @2@ @poison@ when struck",
              "Applies @2@ @poison@ when striking. Applies @2@ @poison@ when struck." },
            // RV-9 buffs: Rampaging
            { "Increased damage by 50% All resistances lowered by 25% Control Resistance",
              "Increased damage by 50%. All resistances except Holy lowered by 25%. Control Resistance" },
            // RV-9 buffs: Power Globule
            { "Increases damage and summon damage by 10%",
              "Increases damage and summon damage by 10%.\n<color=#C8B090>Also increases the healing this character does by the same percentage.</color>" },
            // RV-9 buffs: Point Blank
            { "Ranged spells deal damage the closer you are. Calculates how much ranged you have and the closer you are from your max range the more damage you deal.",
              "Increases damage by 50%.\n<color=#C8B090>Also increases the healing this character does by the same percentage.</color>" },
            // RV-9 buffs: Miniature
            { "Movement increased by 3 Action Points increased by 1 Max Health reduced by 25% Damage reduced by 25%",
              "Movement increased by 3. Action Points increased by 1. Max Health reduced by 25%. Damage reduced by 25%.\n<color=#C8B090>Also reduces the healing this character does by the same percentage.</color>\n<color=#C8B090>Current health is reduced by the same percentage and comes back when the status ends. This cannot kill.</color>" },
            // RV-9 buffs: Incalculable Rage
            { "Grants 1 additional Action Points. Lowers movement points by 6.",
              "Grants 1 additional Action Point. Lowers movement points by 6." },
            // RV-9 buffs: Growing Hatred
            { "Grants 1 additional Action Point. Increases Damage Taken by 25%.",
              "Grants 1 additional Action Point." },
            // RV-9 buffs: Eye Drops
            { "Immune to Bleeding.",
              "Immune to Blind." },
            // RV-9 debuffs: Reduced Resistances III
            { "All Resistances reduced by 30%",
              "All Resistances except Holy reduced by 30%" },
            // RV-9 debuffs: Reduced Resistances II
            { "All Resistances reduced by 20%",
              "All Resistances except Holy reduced by 20%" },
            // RV-9 debuffs: Reduced Resistances I
            { "All Resistances reduced by 10%",
              "All Resistances except Holy reduced by 10%" },
            // RV-9 debuffs: Haunt
            { "Deals *0 damage. Lifesteals for 8%.",
              "Deals *0 damage. Lifesteals for 2.5%." },
            // RV-9 debuffs: Curse of Ruin
            { "All stats reduced by 15%",
              "Might, Dexterity, Intelligence, Vitality and Recovery reduced by 15%" },
            // RV-9 debuffs: Exhaustion
            { "Cannot receive additional actions points.  Caused by receiving additional action points this turn.",
              "Cannot receive additional action points.  Caused by receiving additional action points this turn." },
            // RV-9 debuffs: Chi Strike
            { "Your damage dealt is reduced by 20%",
              "Your damage dealt is reduced by 20%." },
            // DEFEITO DE TEXTO: o asset exige o proximo alvo dentro de 3 hexes
            // (`chainAlvo=... Cell.InRange(LastCell, 3)`), nao 2.
            { "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.  Each time you strike a target it increases your dodge chance by 8%.  Lasts 2 turns. ",
              "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 3 hexes to strike again. Strikes up to 4 times.  Each time you strike a target it increases your dodge chance by 8%.  Lasts 2 turns. " },
            // DEFEITO DE TEXTO: idem `Dodging Strikes` (`Cell.InRange(LastCell, 3)`).
            { "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.  Each time you hit increases the damage of Power Strikes by 50%.",
              "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 3 hexes to strike again. Strikes up to 4 times.  Each time you hit increases the damage of Power Strikes by 50%." },
            // DEFEITO DE TEXTO (2 em 1): "up to 4 times" com `DashMaxChainCount=3` (os irmaos
            // dizem 4 E tem 4, o laco `DashChainCount < DashMaxChainCount` produz
            // exatamente o campo) e "within 2 hexes" com `InRange(LastCell, 3)`
            // (`InRange(c, n) => Distance <= n`). Se a dev subir o asset, esta chave sai.
            { "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.",
              "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 3 hexes to strike again. Strikes up to 3 times." },
            // ---- RV-13 (29/09): "Resist Divine" -> "Resist Holy" ----
            // O jogo e incoerente consigo mesmo: o DANO e "holy" (`TargetStored['HolyDamage']`, e o
            // texto do `Dragonkin Holy Slash` diz "holy damage"), mas a RESISTENCIA se chama "Divine".
            // Fonte: a string "Resist Divine" NAO existe no assembly (0 ocorrencias) - ela e uma CHAVE
            // de localizacao nos assets do jogo (resources.assets: {\"Key\":\"Resist Divine\",\"Value\":...}),
            // que e exatamente o que este patch intercepta. O campo interno `ResistDivine` NAO e tocado.
            // PROVA (29/09, decisao do usuario + conferencia no motor):
            //   (a) os 4 IRMAOS seguem "Resist <tipo de dano>" - `Resist Physical` (28 chaves),
            //       `Resist Lightning` (28), `Resist Fire` (28), `Resist Cold` (28) - e so o
            //       sagrado quebra o padrao com `Resist Divine` (26): e DEFEITO, nao escolha;
            //   (b) o dano se chama "Holy" nas chaves do jogo (`"Holy"` 33x, `HolyDamage` 7x);
            //   (c) o rotulo da FICHA DE PERSONAGEM passa pelo funil que este patch intercepta:
            //       InventoryManager.UpdateStats l.125419 =
            //       `OptionsManager.Localize(Attribute.GetStatMenuDisplayName())`, e
            //       `GetStatMenuDisplayName()` so aparece em 2 lugares no assembly (a propria
            //       definicao, l.319838, e essa linha). Prefabs de UI usam
            //       `OptionsManager.LocalizeUIText` (PrefabLocalizer, l.156306/156310) - o mesmo
            //       funil, ja comprovadamente coberto pelos textos de UI e dicas de loading.
            // Se o jogo um dia padronizar para "Holy", estas duas entradas podem sair.
            { "Resist Divine", "Resist Holy" },
            { "Resistance Divine", "Resistance Holy" },
            // ---- Textos de UI e dicas de loading (fontes: o log do boot do jogo) ----
            // Não estão no censo de tooltips (que cobre skills/status/itens/afixos/
            // powerups). O defeito era o espaço duplo deixado depois do ponto.
            {
                "Shops are refreshed every time your party completes a quest.  Check back often for new loot!",
                "Shops are refreshed every time your party completes a quest. Check back often for new loot!"
            },
            {
                "A well timed healing or mana potion can turn the tide of battle. ",
                "A well timed healing or mana potion can turn the tide of battle."
            },

            // ---- RV-8b, arvore Shadow (29/09) ----
            // Só gramática/espacamento, sem tocar em mecânica. A chave é o texto EXATO
            // do asset (espaços duplos e espaço no fim contam).
            {
                // Haunt: o texto dizia "Lifesteals for 6%" e o codigo faz
                // `SourceStored['HealingForced'] = Source['MaxHealth'] * .025f` - 2,5%.
                // Alem disso o PROPRIO texto do status diz 8%: os tres numeros divergiam.
                // Vale o codigo (regra do projeto: ele vence em divergencia), entao o texto
                // da skill passa a dizer 2,5%. O 8% do status e inconsistencia de dados do
                // jogo e NAO se conserta por aqui: status nao estao no dicionario de
                // localizacao, e um campo bruto do asset (fica para o RV-9).
                "Deals *0 shadow damage to the target every turn for 3 turns. @Life Steals@ for 6%.   @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.",
                "Deals *0 shadow damage to the target every turn for 3 turns. @Life Steals@ for 2.5%. @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities."
            },
            {
                // "creates an poison gas cloud applies" -> artigo errado + falta conectivo
                "The caster creates an poison gas cloud applies @4@ stacks of {STA=Poisoned} within 2 hexes of the selected target.",
                "The caster creates a poison gas cloud that applies @4@ stacks of {STA=Poisoned} within 2 hexes of the selected target."
            },
            {
                // "a Undead Wizard" -> artigo errado (som de vogal)
                // RV-8b-2 (lote Shadow): a explicacao da invocacao entra AQUI, dentro do
                // valor, e nao no TextAppends - quem esta nas duas tabelas so executa a
                // correcao, e uma explicacao no appends nunca rodaria. Fonte das
                // habilidades e o dump `[Summon]` (CharacterInfo.SkillsAndAI[].Skill);
                // O beneficio de Might/Int vale para TODO summon (o CreateSummon aplica
                // ProcessSummonMasterStats incondicionalmente); o que muda entre eles e o
                // que o bicho FAZ, nao se ele escala. Ver o bloco do Brambles abaixo.
                "Raise a Undead Wizard to fight by your side.",
                "Raise an Undead Wizard to fight by your side.\n<color=#C8B090>Undead Wizard: Bone Explosion, Consumption, Ghost Armor\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                // espaco duplo no meio + espaco sobrando no fim
                "Completely negates the next attack.  Lasts until hit. ",
                "Completely negates the next attack. Lasts until hit."
            },
            {
                // espaco sobrando no fim
                "Crush the target's soul dealing *0 @Shadow Damage@ increased by your Max Health. ",
                "Crush the target's soul dealing *0 @Shadow Damage@ increased by your Max Health."
            },

            // ---- RV-8b, padronizacao pela MAIORIA (29/09) ----
            // Regra do projeto: quando skills irmas divergem na redacao, vale o padrao da
            // maioria - e a maioria costuma estar no proprio NOME da skill. Levantado por
            // tools/audit_tooltips.py (checagem E2).
            // Nomes: "Raise Skeletal Archer/Mage/Warrior" -> descricoes diziam "Summon".
            {
                "Summon a skeletal archer to fight by your side.",
                "Raise a skeletal archer to fight by your side.\n<color=#C8B090>Skeletal Archer: Ranged Attack\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                "Summon a skeletal mage to fight by your side.",
                "Raise a skeletal mage to fight by your side.\n<color=#C8B090>Skeletal Mage: Frost Nova, Fireball, Twister, Ghost Armor\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                "Summon a skeletal warrior to fight by your side.",
                "Raise a skeletal warrior to fight by your side.\n<color=#C8B090>Skeletal Warrior: Melee Attack, Cleave\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                // Unico invocador com fecho diferente: 6 usam "by your side", 1 usava "for you".
                "Raise a Mighty Iron Golem to fight for you.",
                "Raise a Mighty Iron Golem to fight by your side.\n<color=#C8B090>Iron Golem: Ground Slam\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                // Familia "Shapeshift *": 3 abrem com "Shapeshift into", esta abria com
                // "Gain the ability to shapeshift into" (mesma redacao, mais verbosa).
                // O "Scales with" tambem entra aqui (RV-8b-2i): a formula e
                // `10 * Source.Level`, e quem esta nas duas tabelas so executa a CORRECAO
                // - uma explicacao no TextAppends para este texto nunca rodaria.
                "Gain the ability to shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilities, and resistance based on the color you choose. Increases @Armor@ by [0].",
                "Shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilities, and resistance based on the color you choose. Increases @Armor@ by [0].\n<color=#C8B090>Scales with your character level.</color>\n<color=#C8B090>The Dragonkin grants a Slash, a Breath and an Orb of its element: Shadow, Frost, Lightning, Fire or Holy.</color>"
            },

            // ---- RV-8b-2, grafia/gramatica (29/09) ----
            // Levantado por varredura em TODAS as 417 skills: "benefical" (3x),
            // "additonal" (2x), "abilites" (1x) e "the damage of by" (3x).
            // Aqui so a GRAFIA: espaco duplo e espaco no fim ficam a cargo da regra geral
            // de normalizacao no fim do postfix (uma entrada por frase seria centenas).
            {
                // "additonal" -> "additional"
                "Sacrifice 15% of your maximum health in exchange for an additonal action this turn.  Applies {STA=Exhaustion}.",
                "Sacrifice 15% of your max health in exchange for an additional action this turn.  Applies {STA=Exhaustion}."
            },
            {
                // "abilites" -> "abilities"
                "Increase the range of all non-melee abilites by 1 hex. ",
                "Increase the range of all non-melee abilities by 1 hex. "
            },
            {
                // "increases the damage of by X%" -> "increases the damage by X%"
                "Deals *0 weapon damage. Every hex between you and your target increases the damage of by 10%.  Called Shot cannot be dodged or blocked.",
                "Deals *0 weapon damage. Every hex between you and your target increases the damage by 10%.  Called Shot cannot be dodged or blocked."
            },
            {
                // "benefical" -> "beneficial"
                "Deals *0 weapon damage, removes 1 random benefical status from the target and lowers the target's @Resistance@ by 20% for 2 turns.",
                "Deals *0 weapon damage, removes 1 random beneficial status from the target and lowers the target's @Resistance@ by 20% for 2 turns."
            },
            {
                "Deals *0 weapon damage. Removes 1 random benefical status from the target.",
                "Deals *0 weapon damage. Removes 1 random beneficial status from the target."
            },
            {
                // "additonal" -> "additional"
                "Every enemy slain on your turn grants 1 additonal AP.  Can only grant up to 1 additional AP per turn.",
                "Every enemy slain on your turn grants 1 additional AP.  Can only grant up to 1 additional AP per turn."
            },
            {
                "Deals *0 shadow damage and removes a random benefical status from the target. If a status is removed, the target suffers an additional *0 shadow damage.",
                "Deals *0 shadow damage and removes a random beneficial status from the target. If a status is removed, the target suffers an additional *0 shadow damage."
            },
            {
                // "increases the damage of by 10%" -> "increases the damage by 10%"
                "Deals *0 weapon damage.  Every hex between you and your target increases the damage of by 10%. ",
                "Deals *0 weapon damage.  Every hex between you and your target increases the damage by 10%. "
            },
            {
                // "increases the damage of by 15%" -> "increases the damage by 15%"
                "Deals *0 weapon damage.  Every hex between you and your target increases the damage of by 15%. ",
                "Deals *0 weapon damage.  Every hex between you and your target increases the damage by 15%. "
            },

            // ---- RV-8b-2e, concordancia e pontuacao (29/09) ----
            // Levantado por varredura em TODAS as 417 skills, com o PADRAO DO JOGO como
            // régua: "1 turns" aparece 1x em 417 (os outros usam "1 turn"); e das 8
            // descricoes sem ponto final, 6 sao o padrao "Current Bonus: [0]" (termina em
            // valor dinamico, e sao 6 de 6 -> fica como esta). Sobram estas 3, cujos
            // irmaos TEM ponto: Frozen Orb/Sun Fire (Bleeding Shot e Entangle tem) e
            // Pack Summoning I (II e III tem).
            {
                // unico caso de concordancia errada no jogo inteiro
                "Infects enemies with Stunning Spores applying {STA=Stun} for 1 turns.",
                "Infects enemies with Stunning Spores applying {STA=Stun} for 1 turn."
            },
            {
                "Hurls a ball of Ice dealing *0 cold damage to all targets in range. Applies 5 stacks of {STA=Chilled}",
                "Hurls a ball of Ice dealing *0 cold damage to all targets in range. Applies 5 stacks of {STA=Chilled}."
            },
            {
                "Hurls a ball of flame dealing *0 fire damage to all targets in range. Applies 10 stacks of {STA=Heat}",
                "Hurls a ball of flame dealing *0 fire damage to all targets in range. Applies 10 stacks of {STA=Heat}."
            },
            {
                "Summons a Timber Wolf to fight for you",
                "Summons a Timber Wolf to fight for you.\n<color=#C8B090>Timber Wolf: Melee Attack, Cripple\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            // ---- RV-17 (varredura FINAL de terminologia): sobras do RV-14 ----
            // Regras JA DECIDIDAS e aceitas (maioria do censo + vocabulario do MOTOR):
            //   `maximum health` / `max life` -> `max health`   (motor: Max Health 147 x Maximum Health 45 x Max Life 22)
            //   `maximum mana`                -> `max mana`     (motor: Max Mana 30 x Maximum Mana 22)
            //   `damage received`             -> `damage taken` (censo: 40 x 4)
            // As 10 entradas abaixo ficaram FORA da rodada do RV-14 (29/09) por um motivo
            // mecanico: o texto do jogo ja tinha nota em `TextAppends` e, como o lookup e
            // if/else if na MESMA chave, corrigir o texto exigia MOVER a entrada - e uma
            // chave nas duas tabelas quebra o mod inteiro (INC-1). A nota foi FUNDIDA no
            // valor, no formato do `AnexarNota` (uma linha em branco + bloco na cor do
            // jogo), e a entrada de `TextAppends` foi APAGADA: uma entrada por texto.
            // RV-9 buffs: Rage - Current health is increased by the same percentage and goes back
            // RV-17: Rage (status) - max life + damage received -> padrao do jogo; nota movida de TextAppends.
            { "Increases damage dealt and max life by 15%. Increases damage received by 15%.",
              "Increases damage dealt and max health by 15%. Increases damage taken by 15%.\n\n<color=#C8B090>Current health is increased by the same percentage and goes back down when the status ends.\nAlso increases the healing this character does by the same percentage.</color>" },
            // RV-9 buffs: Bone Collector - Stacks up to 5 times. Also increases the healing you do by the s
            // RV-17: Bone Collector - maximum health -> padrao do jogo; nota movida de TextAppends.
            { "@Maximum health@ and @Damage Dealt@ increased by 6% per stack.",
              "@Max health@ and @Damage Dealt@ increased by 6% per stack.\n\n<color=#C8B090>Stacks up to 5 times.\nAlso increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Bless - Also increases the healing you do by the same percentage.
            // RV-17: Bless (status) - maximum health + maximum mana -> padrao do jogo; nota movida de TextAppends.
            { "@Maximum health@ and @maximum mana@ increased by 10%.  @Damage dealt@ increased by 10%.",
              "@Max health@ and @max mana@ increased by 10%.  @Damage dealt@ increased by 10%.\n\n<color=#C8B090>Also increases the healing you do by the same percentage.</color>" },
            // RV-9 buffs: Berserking - Lasts 3 turns. The bonus is your missing health as a percentage:
            // RV-17: Berserking - maximum health -> padrao do jogo; nota movida de TextAppends.
            { "Maximum health increased by 25% Deals more damage at lower health",
              "Max health increased by 25% Deals more damage at lower health\n\n<color=#C8B090>Lasts 3 turns.\nThe bonus is your missing health as a percentage: up to +100% damage at 1 health.</color>" },
            // RV-9 buffs: Angered - Lasts 3 turns. Also increases the healing you do by the same per
            // RV-17: Angered - max life -> padrao do jogo; nota movida de TextAppends.
            { "Increases damage dealt by 25%. Increases max life and damage taken by 15%.",
              "Increases damage dealt by 25%. Increases max health and damage taken by 15%.\n\n<color=#C8B090>Lasts 3 turns.\nAlso increases the healing you do by the same percentage.</color>" },
            // RV-9 debuffs: Frozen - REMOVIDA em 30/09 (BUG-32): "Cannot move or perform actions." tambem e o
            // texto do status Stunned, que NAO ignora Chilled - a nota mentia para ele. Sem texto exclusivo
            // do Frozen para recebe-la.
            // RV-9 debuffs: Diseased - Current health is reduced by the same percentage and comes b
            // RV-17: Diseased - maximum health -> padrao do jogo; nota movida de TextAppends.
            { "Maximum health reduced by 15%.",
              "Max health reduced by 15%.\n\n<color=#C8B090>Current health is reduced by the same percentage and comes back when the status ends. This cannot kill.</color>" },
            // RV-9 debuffs: Consumption - Each stack grants another 10% Max Health; you gain one stack
            // RV-17: Consumption (status 10%) - maximum health -> padrao do jogo; nota movida de TextAppends.
            { "@Maximum health@ reduced by 10%.",
              "@Max health@ reduced by 10%.\n\n<color=#C8B090>Each stack grants another 10% Max Health; you gain one stack per enemy hit.</color>" },
            // RV-9 debuffs: Consumption - a nota de stack saiu DESTA chave em 30/09 (BUG-32/BUG-31): o texto
            // "Max Health increased by 10%." e compartilhado com a skill Endurance I (bonus FIXO, sem stack).
            // A nota mora agora na chave exclusiva da SKILL Consumption (entrada "Devour the life force...").
            // RV-9 debuffs: Consumption - Each stack grants another 10% Max Health; you gain one stack
            // RV-17: Consumption (status 20%) - maximum health -> padrao do jogo; nota movida de TextAppends.
            { "@Maximum health@ reduced by 20%.",
              "@Max health@ reduced by 20%.\n\n<color=#C8B090>Each stack grants another 10% Max Health; you gain one stack per enemy hit.</color>" },
            // OMISSAO (nao mentir por omissao): o efeito real e
            // `Mathf.Min(Target.Health - 1, Target['MaxHealth'] * .1f)`. Os 10% do texto
            // estao certos, mas o `Min` com `Health - 1` garante que NAO MATA - e o texto
            // nao dizia. Muda a decisao de quem hesita em usar num aliado quase morto.
            // RV-17: Cauterize - maximum health -> padrao do jogo; nota movida de TextAppends.
            { "Removes all negative statuses from friendly target but inflicts 10% of target's maximum health as fire damage. Can be used when Disabled.",
              "Removes all negative statuses from friendly target but inflicts 10% of target's max health as fire damage. Can be used when Disabled.\n\n<color=#C8B090>This cannot reduce the target below 1 health.</color>" },
            // RV-17: Healing Hand - maximum health -> padrao do jogo; nota movida de TextAppends.
            { "The caster reaches out in aid healing 30% of target's maximum health.",
              "The caster reaches out in aid healing 30% of target's max health.\n\n<color=#C8B090>Healing scales with your Holy Power.\nReduced by effects that lower the target's healing received.</color>" },

            // ---- RV-13b (30/09): as duas `corrigido` do fechamento do censo (RV-13b §5) ----
            // RV-13b: Raise Skeletal Lackey | o efeito do asset reduz CINCO coisas
            // (`MaxHealth:Multiplicative:.5, DamageMod:Multiplicative:.5, Armor:Multiplicative:.5,
            // DodgeChance:Multiplicative:.5, MagicArmor:Multiplicative:.5`) e o texto listava
            // quatro: sem o Magic Armor, quem le le UMA mitigacao caindo quando caem DUAS.
            // `Multiplicative:.5` = -50% esta provado pelo irmao `Transcendence` (ja `revisado`:
            // "Reduces @Max Health@ by {50,35}%" = `MaxHealth:Multiplicative:{.5,.65}`).
            // `ModelScaleMultiplier:Set:-40` nao entra: e escala visual, nao atributo.
            { "Max Health, Damage, Armor, and Dodge Chance reduced by 50%.",
              "Max Health, Damage, Armor, Magic Armor, and Dodge Chance reduced by 50%." },
            // RV-13b: Warrior's Blade | a familia de efeito identico escreve com a preposicao -
            // `Destructive` ("Damage increased by 50% ", ja `revisado`) e `Empowered Blood`
            // ("Increases damage dealt by 50%.", ja `revisado`) - e esta entrada perdeu o `by`.
            // Mesmo efeito (`DamageMod:Base:50`, o status `Warrior Shrine Explosion`, RV-19 §2).
            { "Damage increased 50%.",
              "Damage increased by 50%." },

            // ---- ENC-1 (01/10): encantamento de elemento nao e so para ATAQUE, e para HIT ----
            // O texto dizia "add *0 <elemento> damage to attacks" e a mecanica e mais larga.
            // FONTE DA VERDADE (asset + motor, nao prosa):
            //   - o gatilho do status do encantamento (`resources.assets`: `COLD_Status_EnchantCold`,
            //     `FIRE_Status_EnchantFire`, `LIGHTNING_Status_EnchantLightning` e os dois irmas
            //     `Status_EnchantHoly`/`Status_EnchantShadow`) tem TriggerType = 0
            //     (`OnHittingDamaging`, enum em `scratch/sac1/TriggerType.cs:4`) — o inteiro no asset e
            //     o 1o campo de `SkillTrigger` (`scratch/sac1/SkillTrigger.cs:9`), lido logo antes da
            //     string de Condition; controle do metodo no `Toxic`, cujos DOIS gatilhos saem 0
            //     ("when striking") e 1 ("when struck"), e no `Flame Shrine Aura` (1, ja provado).
            //   - a Condition do MESMO gatilho e
            //     `(ActionProperties.IsAttackPowerBased || ActionProperties.IsSpellPowerBased) &&
            //     Source.IsEnemy(Target)`: cai em qualquer dano que o personagem encantado cause a um
            //     INIMIGO cuja fonte seja Attack Power OU Spell Power (`ActionProperties.cs:69/85`,
            //     `ActionInfo.IsAttackPowerBased => BenefitType == BenefitType.AttackPower`,
            //     `ActionInfo.cs:728/730`).
            //   - o disparo do motor e `source.ProcessSkillTriggers(target, properties,
            //     TriggerType.OnHittingDamaging, ...)`, um por tipo de dano, DENTRO do loop de dano de
            //     `ApplyAction` (`scratch/sac1/Character.cs:11348-11373`) — vale para ataque corpo a
            //     corpo, ranged e SPELL. NAO vale para dano de retorno: essas acoes sao aplicadas com
            //     `procSkillTriggers: false` (`Character.cs:11302-11318`).
            // Assim "hits" (a palavra do enum) + "including spells" (o caso que o dono citou) — em uma
            // linha, sem enumeracao. A lista completa do que conta como hit fica no relatorio da ENC-1.
            { "Enchants the target's weapon to add *0 fire damage to attacks. ",
              "Enchants the target's weapon to add *0 fire damage to hits, including spells. " },
            { "Enchants the target's weapon to add *0 cold damage to attacks. ",
              "Enchants the target's weapon to add *0 cold damage to hits, including spells. " },
            { "Enchants the target's weapon to add *0 lightning damage to attacks. ",
              "Enchants the target's weapon to add *0 lightning damage to hits, including spells. " },

        };

        private static readonly HashSet<string> _appliedFixes = new HashSet<string>();
        private static readonly HashSet<string> _appliedAppends = new HashSet<string>();

        /// <summary>BUG-33: rotulos de status que a guarda pulou — log UMA vez por chave, para a
        /// prova em jogo sair no `LogOutput.log` no mesmo formato das notas aplicadas.</summary>
        private static readonly HashSet<string> _rotulosDeStatusAvisados = new HashSet<string>();

        /// <summary>Marcador de vida: o postfix já recebeu texto em inglês nesta sessão.</summary>
        private static bool _loggedAlive;

        // Powerups de atributo: "+ N to Might/Dexterity/Intelligence/Vitality/Reflex".
        // Os efeitos por ponto são os MESMOS que o tooltip de stats do jogo mostra
        // (Tooltip.ShowMainStatTooltip), com os valores lidos do GlobalSettings em runtime.
        private static readonly Regex AttributePowerupRegex = new Regex(
            @"^\+\s*\d+\s+to\s+(Might|Dexterity|Intelligence|Vitality|Reflex)$",
            RegexOptions.Compiled);

        private static readonly Regex DamageReductionRegex = new Regex(
            @"^\+\s*\d+%\s+Damage Reduction$",
            RegexOptions.Compiled);

        // Statuses que concedem atributos (BT-6a): descrições como
        // "Might increased by [0]." (status) ou "Dexterity increased by 30." (poções).
        // Mesma explicação dinâmica dos powerups.
        private static readonly (Regex Pattern, string Attribute)[] StatusAttributeRules =
        {
            (new Regex(@"^Might increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Might"),
            (new Regex(@"^Dexterity increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Dexterity"),
            (new Regex(@"^Intelligence increased\.$|^Intelligence increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Intelligence"),
            (new Regex(@"^Vitality increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Vitality"),
            (new Regex(@"^Reflex increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Reflex"),
        };

        // BT-6c: Fortunes que concedem atributos, formato "@Might@ increased by {12,60}."
        private static readonly (Regex Pattern, string Attribute)[] FortuneAttributeRules =
        {
            (new Regex(@"^@Might@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Might"),
            (new Regex(@"^@Dexterity@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Dexterity"),
            (new Regex(@"^@Intelligence@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Intelligence"),
            (new Regex(@"^@Vitality@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Vitality"),
            (new Regex(@"^@Reflex@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Reflex"),
        };

        // BT-6b: statuses que reduzem resistências — explicar a mecânica de resistência
        // (fórmula verificada: dano × (1 - Resist/100); resistência negativa AMPLIFICA o dano).
        private const string ResistanceExplainSuffix =
            "\nResistances reduce their damage type by the listed %. If a resistance goes negative, that damage type is amplified instead.";

        private static readonly string[] ResistanceReductionPrefixes =
        {
            "Elemental resistance reduced by 5% per stack",                       // Heat
            "Reduces @Cold Resistance@ by @25%@ per stack",                       // Frostbitten
            "Reduces @Fire Resistance@ by @25%@ per stack",                       // Severely Burned
            "Reduces @Physical Resistance@ by @25%@ per stack",                   // Sundered
            "Reduces Elemental resistances by 25%",                               // Curse of Elements
            "@Resistance@ lowered by 20%",                                        // Fracture / Dispelling Fracture
            "@Resistances@ lowered by 20%. Reduces healing received by 50%",      // Mortal Fracture
        };

        // BT-7a: glossário de mecânicas nos tooltips de skills — definições tiradas
        // das descrições dos PRÓPRIOS status do jogo (inventário da BT-6, sem invenção).
        // A exclusão evita redundância quando o texto já define o termo (ex.: a
        // descrição do status Stealth já menciona o crítico garantido).
        // REGRA: nada relacionado a Bard/música (Crescendo, Harmony, Songs) — a árvore
        // chega na próxima atualização do jogo; não mexer.
        // Rótulos da ficha de personagem que NUNCA devem receber explicação
        // (ex.: a linha "Life Steal" do bloco de Stats é só um número + nome).
        private static readonly HashSet<string> GlossaryLabelExclusions = new HashSet<string>
        {
            "Life Steal",
            "Lifesteal",
            "% Life Steal",
            "% Lifesteal",
            "Stealth",
            "Enrage",
            "Marked Prey",
        };

        /// <summary>
        /// Rótulos curtos ("Life Steal", "Life Steal: 15%", "% Life Steal", "X Applied")
        /// são exibição pura e não devem receber explicação do glossário.
        /// </summary>
        private static bool IsGlossaryLabel(string original)
        {
            string t = original.Trim();
            if (GlossaryLabelExclusions.Contains(t) || t.EndsWith(" Applied"))
            {
                return true;
            }
            if (t.Length <= 24)
            {
                string low = t.ToLower();
                if (low.StartsWith("life steal") || low.StartsWith("lifesteal"))
                {
                    return true;
                }
            }
            return false;
        }

        private static readonly (Regex Match, string Append, string ExcludeIfContains)[] SkillGlossaryRules =
        {
            (new Regex(@"\bStealth\b", RegexOptions.Compiled),
             "\nStealth: attacking from stealth has 100% critical hit chance.",
             "critical hit chance"),
            (new Regex(@"Marked Prey", RegexOptions.Compiled),
             "\nMarked Prey: increases damage taken by 10% per stack.",
             "Damage taken"),
            // BT-7b: Enrage — status do jogo: "Immune to all movement impairing effects
            // and knockback." (verificado: statuses TriggersEnrage rolam StatusResistImpairment
            // em alvos com CanEnrage; troca de fase limpa esses statuses).
            (new Regex(@"\bEnrage\b", RegexOptions.Compiled),
             "\nEnraged characters are immune to movement impairing effects and knockback.",
             "immune to"),
            // BT-7b: Life Steal — RV-7: TEXTO OFICIAL do jogo (localização + patch notes v0.22):
            // "Life Steal heals you for a percentage of your Max Health each time you hit.
            // Reduced for area of effect abilities." — o código atual calcula a partir da
            // vida perdida do ALVO; pendente confirmação empírica via [LifeSteal] debug.
            (new Regex(@"Life Steal|Lifesteal", RegexOptions.Compiled),
             "\nLife Steal: heals you for a percentage of your Max Health each time you hit. Reduced for area of effect abilities.",
             "heals you for"),
        };

        // BT-8: afixos de itens — mecânicas verificadas no código (Character.ApplyAction):
        /// <summary>
        /// Junta a nota ao texto com EXATAMENTE uma linha em branco entre eles.
        /// O texto do jogo costuma terminar com quebras de linha proprias e a concatenacao crua
        /// somava mais uma -> vazio desnecessario no tooltip (reportado pelo usuario em
        /// `Chain Lightning` e `Breath of Winter`). O TrimEnd so roda em texto que RECEBE nota;
        /// o resto continua sem ser aparado (regra do projeto).
        /// </summary>
        private static string AnexarNota(string texto, string nota)
        {
            if (string.IsNullOrEmpty(nota))
            {
                return texto;
            }

            return texto.TrimEnd() + "\n\n" + nota.TrimStart(new char[] { '\n' });
        }

        // Armor: dano - (Armor/ArmorPerDamagePointReduction), com cap maxArmorReductionPercent.
        // Resists: dano × (1 - Resist/100) por elemento.
        // Só disparam em textos com verbo de modificação ("increased/added/...") para não
        // poluir rótulos simples (ex.: o label "Armor" da ficha de stats).
        private static readonly Regex ArmorAffixRegex = new Regex(@"\bArmor\b", RegexOptions.Compiled);

        // Afixos "Armor increased by N%" cujo ASSET concede Armor E Magic Armor no mesmo valor,
        // mas cujo texto cita so Armor. Verificados um a um nos assets pelos agentes (RV-11:
        // IM[Armor%N,MagicArmor%N]). Entram AQUI e nao como entrada em TextAppends de proposito:
        // o dicionario e if/else, entao uma entrada estatica TIRARIA a explicacao de mitigacao
        // (BuildArmorNote) desse mesmo texto - trocaria informacao em vez de somar.
        private static readonly HashSet<string> ArmorQueTambemDaMagicArmor = new HashSet<string>
        {
            "Armor increased by 5%",
            "Armor increased by 35%",
            "Armor increased by 15%",
            "Armor increased by [50]% Movement points lowered 1",
            "Armor increased by 25% Movement points lowered",
            "Armor increased by [30]% Movement points lowered 1",
            "Armor increased by 45% Movement points lowered",
            "Armor increased by 20%",
            "Armor increased by 25%",
            "Armor increased by [60]% Movement points lowered 1",
            "Armor increased by [20]% Movement points lowered 1",
            "Armor increased by 35% Movement points lowered",
            "Armor increased by 45%",
            "Armor increased by [40]% Movement points lowered 1",
            "Armor increased by 10%",
        };

        // Armor usado como FONTE de outro valor (ex.: `Battle Ready` e `Diamond Ice`: "1% of your
        // @Armor@ value is added to your character as @Additional Weapon Damage@"). Nesses casos a
        // nota de mitigacao nao interessa ao jogador - reportado pelo usuario em 30/09.
        private static readonly Regex ArmorValueSourceRegex = new Regex(@"Armor@?\s+value", RegexOptions.Compiled);
        private static readonly Regex ResistAffixRegex = new Regex(@"\bResistance\w*\b", RegexOptions.Compiled);

        /// <summary>
        /// BUG-33 (01/10, print do dono) — NOMES de status do PROPRIO JOGO que NAO podem receber
        /// as notas de mecanica de Armor/Resistencia. Sao ROTULOS, e o rotulo e o texto que o
        /// FEED DE COMBATE localiza.
        ///
        /// O QUE O PRINT MOSTRA NO FEED:
        ///     Necrodancer applied Increased Armor
        ///     Armor blocks damage: each 10 Armor reduces damage taken by 1 (capped at 90% of the
        ///     incoming damage). Armor and Magic Armor do not reduce Shadow damage.
        /// Esse texto nao existe no jogo: nao esta no Assembly-CSharp (0 ocorrencias de
        /// "Armor blocks damage") nem em `resources.assets` (0 em UTF-8 e em UTF-16LE). Ele e o
        /// `BuildArmorNote()` deste arquivo, com os valores lidos em runtime
        /// (`GlobalSettings.ArmorPerDamagePointReduction` e `maxArmorReductionPercent`).
        ///
        /// POR QUE ELE IA PARA O FEED: o feed monta a linha com TEMPLATE + o NOME do status —
        /// `OptionsManager.Localize(Game.Instance.ActionStatuses[statusIndex].Name)`
        /// (`Root.SendMessageWindowMessage`, decompilado l.144600; o template
        /// "[source] applied [status] on [target]" nasce em `ApplyStatus`, l.111812). O funil
        /// deste patch ve SO O TEXTO, e "Increased Armor" casa a regra de afixo (tem verbo — a
        /// checagem e `Contains("increased"/"added"/"lowered"/"reduced"/"granted")` — E a palavra
        /// "Armor"), entao a nota era anexada ao NOME.
        /// PROVA NO LOG do dono (30/09): `BetterTooltips: explicacao adicionada a
        /// 'Increased Armor'` — a chave que casou foi o NOME do status.
        ///
        /// O QUE **NAO** MUDA: a explicacao continua na DESCRICAO de cada um destes status (texto
        /// diferente, continua casando a regra), e `Tooltip.ShowActionStatusTooltip` (l.213909)
        /// monta o CORPO da tooltip com `OptionsManager.Localize(actionStatusInfo.Description)` —
        /// ou seja, o corpo da tooltip do status segue identico.
        ///
        /// ESCOPO MEDIDO (censo `docs/cobertura/status.csv`, que vem do proprio
        /// `Game.get_ActionStatuses` — a MESMA lista que o feed usa): dos 560 status, 4 nomes
        /// casam as regras de afixo; NENHUM nome de skill/acao/item/afixo/powerup casa (0 de
        /// 451 + 276 + 905 + 285 + 79). Estes 4 sao, portanto, o escopo real hoje — se o jogo
        /// acrescentar um status novo com verbo + "Armor"/"Resistance" no NOME, ele reaparece no
        /// feed: o censo e a varredura que denunciam.
        /// </summary>
        private static readonly HashSet<string> RotulosDeStatusSemNota = new HashSet<string>
        {
            // status.csv:248 — descricao: "@Armor@ and @Magic Armor@ increased by [0].  "
            "Increased Armor",
            // status.csv:388 — descricao: "All Resistances reduced by 10%"
            "Reduced Resistances I",
            // status.csv:389 — descricao: "All Resistances reduced by 20%"
            "Reduced Resistances II",
            // status.csv:390 — descricao: "All Resistances reduced by 30%"
            "Reduced Resistances III",
        };

        private static string BuildArmorNote()
        {
            var gs = GlobalSettingsManager.instance?.globalSettings;
            if (gs == null)
            {
                return null;
            }
            return "\nArmor blocks damage: each " + gs.ArmorPerDamagePointReduction.ToString("0.##") +
                " Armor reduces damage taken by 1 (capped at " +
                gs.maxArmorReductionPercent.ToString("0.##") +
                "% of the incoming damage). Armor and Magic Armor do not reduce Shadow damage.";
        }

        private static string BuildAttributeEffects(string attribute)
        {
            var gs = GlobalSettingsManager.instance?.globalSettings;
            if (gs == null)
            {
                return null;
            }

            switch (attribute)
            {
                case "Might":
                    return "\nEffects per point:\n" +
                        $"+{gs.AbilityPwrPerMight.ToString("0.##")}% Damage & Healing\n" +
                        $"+{gs.AbilityPwrPerMightSummon.ToString("0.##")}% Summon Damage\n" +
                        $"+{gs.ArmorPercPerMight.ToString("0.##")}% Armor & Magic Armor";
                case "Dexterity":
                    return "\nEffects per point:\n" +
                        $"+{gs.CritRatingPerDex.ToString("0.##")} Crit Rating\n" +
                        $"+{gs.CritDamagePerDex.ToString("0.##")}% Crit Damage\n" +
                        $"1 Movement Per {gs.MovementPointPerDexInterval} Dex (Max 3)";
                case "Intelligence":
                    return "\nEffects per point:\n" +
                        $"+{gs.ManaPerInt.ToString("0.##")} Max Mana\n" +
                        $"+{gs.MaxManaPercPerInt.ToString("0.##")}% Max Mana\n" +
                        $"1 Skill Range Per {gs.RangePerIntInterval} Int (Max 3)\n" +
                        $"+{gs.SummonLifePerInt.ToString("0.##")}% Summon Health";
                case "Vitality":
                    return "\nEffects per point:\n" +
                        $"+{gs.MaxHealthPerVit.ToString("0.##")} Max Health\n" +
                        $"+{gs.MaxHealthPercPerVit.ToString("0.##")}% Max Health";
                case "Reflex":
                    return "\nEffects per point:\n" +
                        $"+{gs.DodgeRatingPerReflex.ToString("0.##")} Dodge Rating\n" +
                        $"+{gs.DodgeCounterChancePerReflex.ToString("0.##")}% Dodge Counter Chance\n" +
                        $"+{gs.OppAttackPercDmgPerReflex.ToString("0.##")}% Opportunity Attack Damage\n" +
                        $"+{gs.OppAttackPercDmgPerReflex.ToString("0.##")}% Counter Attack Damage\n" +
                        $"1 Counter Attack a turn Per {gs.ExtraCounterAttacksPerReflexInterval} Reflex (Max 3)";
                default:
                    return null;
            }
        }

        /// <summary>
        /// Nota dinâmica do Damage Reduction (RV-5/RV-7): lê a ordem de redução de dano real
        /// do GlobalSettings e mostra a cadeia completa do cálculo.
        /// Padrão do jogo: GeneralReduction → Resists → Armor.
        /// </summary>
        private static string BuildDamageReductionNote()
        {
            try
            {
                var gs = GlobalSettingsManager.instance?.globalSettings;
                if (gs == null)
                {
                    return null;
                }
                var order = gs.DamageReductionOrder;
                if (order == null || order.Length == 0)
                {
                    return null;
                }
                var names = new List<string>();
                bool foundGeneral = false;
                foreach (var stage in order)
                {
                    string s = stage.ToString();
                    if (s == "GeneralReduction")
                    {
                        foundGeneral = true;
                        continue;
                    }
                    if (foundGeneral)
                    {
                        names.Add(
                            s == "Resists" ? "Resistances" :
                            s == "Armor" ? "Armor" : s);
                    }
                }
                if (foundGeneral && names.Count > 0)
                {
                    // Redação do usuário (18:55): "Applied before X and Y" —
                    // lista somente as etapas que vêm DEPOIS da redução geral.
                    return "\nReduces all damage you take. Applied before "
                        + string.Join(" and ", names) + ".";
                }
                return "\nReduces all damage you take.";
            }
            catch
            {
                return "\nReduces all damage you take.";
            }
        }

        /// <summary>
        /// Gancho MAIS QUENTE do projeto: TODO texto de interface do jogo passa por
        /// <c>OptionsManager.Localize</c>. O corpo (as tabelas + as regras dinamicas) roda em
        /// <c>AplicarNotasDoFunil</c>, DENTRO de try/catch: uma excecao inesperada (indexador, regex,
        /// NRE) NAO pode escapar para dentro do metodo do jogo — ela e registrada uma vez por motivo
        /// distinto e o texto que o jogo produziu e devolvido INTACTO.
        /// Com tudo funcionando o caminho e exatamente o de antes: o corpo nao mudou.
        ///
        /// COR-2 (01/10) — A COR DO NIVEL 2 E APLICADA NO FIM DESTE GANCHO (ultima linha do
        /// try), DEPOIS das notas. Ordem de gancho NAO decide mais nada aqui: a cor e resolvida
        /// sobre o texto que este mesmo metodo acabou de montar. O motivo esta escrito onde o
        /// gancho de cor separado vivia (acima da tabela `TextAppends`) — resumo: na 0Harmony do
        /// jogo a prioridade ordena DESCENDENTE, entao um postfix `Priority.High` rodava ANTES
        /// deste e nunca via o marcador. Ver docs/TEXTO-TOOLTIPS.md §7.
        /// </summary>
        private static void Postfix(string original, ref string __result)
        {
            string textoDoJogo = __result;
            try
            {
                AplicarNotasDoFunil(original, ref __result);
                // Unico ponto de aplicacao da cor do nivel 2 (nenhum gancho separado). Idempotente:
                // sem marcador no texto, `ComACorDoJogo` devolve o texto como veio.
                __result = ComACorDoJogo(__result);
            }
            catch (Exception e)
            {
                __result = textoDoJogo;
                RegistrarFalhaIgnorada("postfix do funil OptionsManager.Localize", e);
            }
        }

        /// <summary>
        /// Motivos de falha ja registrados: o log sai UMA vez por motivo DISTINTO (tipo + mensagem),
        /// nunca a cada chamada — este funil roda em todo texto localizado do jogo e um erro repetido
        /// encheria o LogOutput.log em um frame. O teto de 25 motivos limita o pior caso.
        /// </summary>
        private static readonly HashSet<string> _falhasRegistradas = new HashSet<string>();

        private static void RegistrarFalhaIgnorada(string gancho, Exception e)
        {
            try
            {
                string motivo = gancho + " | " + e.GetType().FullName + ": " + e.Message;
                if (_falhasRegistradas.Count >= 25 || !_falhasRegistradas.Add(motivo))
                {
                    return;
                }
                Plugin.Log.LogError("BetterTooltips: falha IGNORADA em " + gancho
                    + " (texto do jogo mantido intacto) — " + motivo);
            }
            catch
            {
                // nem o proprio log pode derrubar o jogo
            }
        }

        /// <summary>Corpo do postfix do funil — inalterado desde antes do try/catch. Ver `Postfix`.</summary>
        private static void AplicarNotasDoFunil(string original, ref string __result)
        {
            if (original == null || __result == null)
            {
                return;
            }

            // Só mexemos quando o texto exibido é o inglês original
            // (em outros idiomas o resultado vem traduzido e não tocamos).
            if (__result != original)
            {
                return;
            }

            // Marcador de vida: prova no log que o postfix está recebendo texto em inglês.
            // O patch só loga quando MUDA algo; sem esta linha, um boot em que nenhuma
            // string conhecida apareceu parece "mod morto" no log.
            if (!_loggedAlive)
            {
                _loggedAlive = true;
                string amostra = original.Length > 60 ? original.Substring(0, 60) + "..." : original;
                Plugin.Log.LogInfo($"BetterTooltips: postfix ativo (1a localizacao em ingles: '{amostra}')");
            }

            if (TextFixes.TryGetValue(original, out string fixedText))
            {
                __result = fixedText;
                if (_appliedFixes.Add(original))
                {
                    Plugin.Log.LogInfo($"BetterTooltips: corrigido '{original}' -> '{fixedText}'");
                }
            }
            else if (TextAppends.TryGetValue(original, out string append))
            {
                __result = AnexarNota(__result, append);
                if (_appliedAppends.Add(original))
                {
                    Plugin.Log.LogInfo($"BetterTooltips: explicação adicionada a '{original}'");
                }
            }
            else
            {
                // Powerups de atributo: espelha os "Effects Per Point" do tooltip de stats.
                Match m = AttributePowerupRegex.Match(original);
                if (m.Success)
                {
                    string effects = BuildAttributeEffects(m.Groups[1].Value);
                    if (effects != null)
                    {
                        __result = AnexarNota(__result, NotaDeExplicacao(effects));
                        if (_appliedAppends.Add(original))
                        {
                            Plugin.Log.LogInfo($"BetterTooltips: efeitos por ponto adicionados a '{original}'");
                        }
                    }
                }
                else
                {
                    // Damage Reduction (RV-5): nota dinâmica com a ordem de redução.
                    if (DamageReductionRegex.IsMatch(original))
                    {
                        string note = BuildDamageReductionNote();
                        if (note != null)
                        {
                            __result = AnexarNota(__result, NotaDeExplicacao(note));
                            if (_appliedAppends.Add(original))
                            {
                                Plugin.Log.LogInfo($"BetterTooltips: ordem de redução adicionada a '{original}'");
                            }
                        }
                    }

                    // Statuses que concedem atributos (BT-6a): mesma explicação dinâmica.
                    bool appended = false;
                    foreach (var rule in StatusAttributeRules)
                    {
                        if (rule.Pattern.IsMatch(original))
                        {
                            string effects = BuildAttributeEffects(rule.Attribute);
                            if (effects != null)
                            {
                                __result = AnexarNota(__result, NotaDeExplicacao(effects));
                                appended = true;
                            }
                            break;
                        }
                    }

                    // Fortunes que concedem atributos (BT-6c).
                    if (!appended)
                    {
                        foreach (var rule in FortuneAttributeRules)
                        {
                            if (rule.Pattern.IsMatch(original))
                            {
                                string effects = BuildAttributeEffects(rule.Attribute);
                                if (effects != null)
                                {
                                    __result = AnexarNota(__result, NotaDeExplicacao(effects));
                                    appended = true;
                                }
                                break;
                            }
                        }
                    }

                    // Statuses que reduzem resistências (BT-6b): mecânica de resistência.
                    if (!appended)
                    {
                        foreach (var prefix in ResistanceReductionPrefixes)
                        {
                            if (original.StartsWith(prefix, StringComparison.Ordinal))
                            {
                                __result = AnexarNota(__result, NotaDeExplicacao(ResistanceExplainSuffix));
                                appended = true;
                                break;
                            }
                        }
                    }

                    // Glossário de mecânicas nos tooltips de skills (BT-7a).
                    if (!appended)
                    {
                        foreach (var rule in SkillGlossaryRules)
                        {
                            if (IsGlossaryLabel(original))
                            {
                                break;
                            }
                            if (rule.Match.IsMatch(original) &&
                                !original.Contains(rule.ExcludeIfContains))
                            {
                                __result = AnexarNota(__result, NotaDeExplicacao(rule.Append));
                                appended = true;
                                break;
                            }
                        }
                    }

                    // Afixos de itens (BT-8): Armor e Resistências.
                    if (!appended)
                    {
                        string low = original.ToLower();
                        bool hasVerb = low.Contains("increased") || low.Contains("added") ||
                            low.Contains("lowered") || low.Contains("reduced") ||
                            low.Contains("granted");
                        // BUG-33: quando o texto e o NOME de um status (`RotulosDeStatusSemNota`), a
                        // nota de mecanica NAO entra — o feed de combate localiza esse NOME
                        // (`Root.SendMessageWindowMessage` l.144600) e a explicacao aparecia colada
                        // nele. A DESCRICAO do mesmo status e outro texto e continua recebendo a nota,
                        // que e a que serve ao jogador no corpo da tooltip.
                        bool ehRotuloDeStatus = RotulosDeStatusSemNota.Contains(original);
                        if (ehRotuloDeStatus && _rotulosDeStatusAvisados.Add(original))
                        {
                            Plugin.Log.LogInfo($"BetterTooltips: nota de mecanica NAO anexada ao NOME de "
                                + $"status '{original}' (BUG-33: o feed de combate localiza o nome; "
                                + "a explicacao continua na descricao do status)");
                        }
                        if (!ehRotuloDeStatus && hasVerb && ArmorAffixRegex.IsMatch(original) &&
                            !ArmorValueSourceRegex.IsMatch(original) &&
                            !original.Contains("blocks damage"))
                        {
                            string note = BuildArmorNote();
                            if (note != null)
                            {
                                if (ArmorQueTambemDaMagicArmor.Contains(original))
                                {
                                    note = "\nAlso increases Magic Armor by the same amount." + note;
                                }

                                // NIVEL 2: a nota inteira (inclusive o acrescimo de Magic Armor) entra
                                // no MESMO bloco de cor — a cor do nivel 2 e uma so por explicacao.
                                __result = AnexarNota(__result, NotaDeExplicacao(note));
                                appended = true;
                            }
                        }
                        else if (!ehRotuloDeStatus && hasVerb && ResistAffixRegex.IsMatch(original) &&
                            !original.Contains("Summon resistance") &&
                            !original.Contains("resistances reduce"))
                        {
                            __result = AnexarNota(__result, NotaDeExplicacao(ResistanceExplainSuffix));
                            appended = true;
                        }
                    }

                    if (appended && _appliedAppends.Add(original))
                    {
                        Plugin.Log.LogInfo($"BetterTooltips: explicação adicionada a '{original}'");
                    }
                }
            }

            // Normalizacao de espacos (RV-8b-2): o padrao do jogo e UM espaco depois do
            // ponto (116 ocorrencias contra 77), mas varias frases vem com dois e a
            // diferenca APARECE no tooltip. E regra geral de proposito: vale para todo
            // texto localizado (skills, status, itens, dicas), nao so para as skills que a
            // varredura achou - centenas de entradas na tabela nao escalariam.
            // Roda DEPOIS das tabelas porque as chaves de TextFixes casam com o texto
            // ORIGINAL, espacos duplos inclusos.
            // NAO aparamos o fim: espaco sobrando no fim nao aparece no tooltip, e aparar
            // poderia colar palavras se o jogo concatenar strings.
            if (__result.Contains("  "))
            {
                string antes = __result;
                while (__result.Contains("  "))
                {
                    __result = __result.Replace("  ", " ");
                }
                if (_appliedFixes.Add("espacos:" + antes))
                {
                    Plugin.Log.LogInfo($"BetterTooltips: espacos normalizados em '{antes}'");
                }
            }
            // RV-26/RV-33 (30/09) — os VALORES do Flame Shrine POR ALVO NA ÁREA. A chave não tem `[0]`, e
            // o número único "para você" que a RV-26 mostrava SAIU (RV-33): quem leva o dano é o
            // atacante, e o atacante é desconhecido no hover. O que dá para calcular é o dano de CADA
            // personagem que tem o status da aura vivo (party e inimigos) — a lista entra DENTRO do bloco
            // da nota: ela e um pedaco da MESMA nota (o bloco e a unidade do valor), e um segundo bloco
            // seria um bloco a mais sem ser uma nota a mais. RV-17 (01/10): o `CorEOrdemDoTooltip` hoje
            // move TODAS as notas, na ordem — o motivo de manter UM bloco e a coesao do texto, nao mais
            // a extracao (que antes so pegava o primeiro). A linha azul do RV-31 continua por último.
            if (original == ShrineAuraPatch.ChaveFlame)
            {
                string alvos = ShrineAuraPatch.FraseAlvosDoFlame(original);
                if (!string.IsNullOrEmpty(alvos))
                {
                    // TX-1 (01/10) — VALOR PRIMEIRO: a lista por alvo entra no COMECO do bloco da nota (o
                    // leitor ve os numeros logo depois da linha branca do jogo), nao no fim. E o MESMO
                    // bloco de cor: a lista e um pedaco da mesma nota, nao uma segunda nota (RV-17: a
                    // extracao hoje move TODAS as notas, na ordem — o que se preserva aqui e a coesao
                    // do texto). Sem bloco colorido, a frase vira bloco proprio.
                    const string abreNota = "<color=#" + MarcadorCorDeExplicacao + ">";
                    int abre = __result.IndexOf(abreNota, StringComparison.Ordinal);
                    __result = abre >= 0
                        ? __result.Insert(abre + abreNota.Length, alvos + " ")
                        : AnexarNota(__result, "\n" + abreNota + alvos + "</color>");
                }
            }

            // RV-33 (30/09) — o DANO POR TURNO do Decay Shrine na LINHA ORIGINAL. A chave tem `[0]` (a %
            // que o motor resolve) e a linha passa a trazer o dano literal calculado pela MESMA fórmula
            // da ação `Decay Aura Proc`, avaliada pelo interpretador do jogo com Target = o personagem em
            // foco (quem está na aura) — o caso que o dono do jogo descreveu: 100 de vida -> 10 por turno.
            // Sem número provado, a linha do jogo fica INTACTA.
            if (original == ShrineAuraPatch.ChaveDecay)
            {
                string linhaDecay = ShrineAuraPatch.LinhaDecayComValor(original);
                if (!string.IsNullOrEmpty(linhaDecay))
                {
                    __result = __result.Replace(original, linhaDecay);
                }
            }

            // RV-28 (30/09) — a cura do `Sustenance` no tooltip de todo GLOBULE, com o valor do
            // personagem em foco (Max Health/Max Mana) e a % lida das skills ATIVAS do jogo (nunca
            // "I"/"II" cravados: a lista já vem resolvida pelo `SkillsThatReplace` de cada uma).
            // `AnexarNota` põe exatamente uma linha em branco antes do bloco, como todas as notas.
            if (GlobulePatch.EhGlobule(original))
            {
                string sustenance = GlobulePatch.FraseSustenance(original);
                if (!string.IsNullOrEmpty(sustenance))
                {
                    // A chave do Power Globule já carrega bloco colorido (nota do RV-9 em `TextFixes`):
                    // a frase entra DENTRO do mesmo bloco — ela completa a mesma nota (RV-17: o
                    // `CorEOrdemDoTooltip` hoje move todas as notas, na ordem; o que se preserva aqui e
                    // que a frase e um pedaco de UMA nota, nao uma nota nova).
                    int fim = __result.LastIndexOf("</color>", StringComparison.Ordinal);
                    __result = fim >= 0
                        ? __result.Substring(0, fim) + " " + sustenance + __result.Substring(fim)
                        : AnexarNota(__result, "\n<color=#" + MarcadorCorDeExplicacao + ">" + sustenance + "</color>");
                }
            }

            // RV-22/RV-23/RV-27 — acumulado de shrines (30/09): linha dinâmica com as auras de shrine
            // VIVAS no RECEPTOR (personagem em foco), com o bônus real dele
            // (ShrineAuraPatch.AcumuladoShrines). O número individual de cada shrine fica dinâmico
            // pelo prefix do ShrineAuraPatch: o ShowGroundEffectTooltip monta os parâmetros com
            // Source = WorldCharacter (personagem vazio) e SEM Target, então o [0] saía sempre
            // na base — o prefix preenche o receptor para o motor calcular com Omnism/Horn.
            // RV-29: a linha é filtrada pelo status VIVO do receptor (`AurasVivas`) — fora das auras de
            // shrine, `AcumuladoShrines` devolve vazio e nada é anexado.
            // RV-31: o CONTEÚDO é o AGREGADO de todas as auras vivas (um item por atributo, com o valor
            // final lido do próprio personagem) — `original` (a chave do shrine aberto) entra só no log
            // e no pré-filtro `IsShrineKey`; não decide mais o que a linha mostra.
            // A LINHA vai no azul da paleta do jogo (RV-27) e o `CorEOrdemDoTooltip` a coloca por
            // ÚLTIMO, depois da nota da shrine, mantendo uma linha em branco antes de cada bloco.
            if (ShrineAuraPatch.IsShrineKey(original))
            {
                string acumulado = ShrineAuraPatch.AcumuladoShrines(original);
                if (!string.IsNullOrEmpty(acumulado))
                {
                    __result = AnexarNota(__result, acumulado);
                }
                Plugin.Log.LogInfo($"[Shrine RV-23] chave '{original}' -> resultado final: '{(__result.Length > 140 ? __result.Substring(0, 140) + "..." : __result)}'");
            }
        }
    }
}
