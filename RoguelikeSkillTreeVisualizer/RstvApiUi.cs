using System;
using Burst2Flame;
using Gumatos.RealmApi;
using Gumatos.RealmApi.UI;
using UnityEngine;
using UnityEngine.Events;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// INT-R1-C4 (11/10) — a PONTE do mod para a familia <c>UI</c> da API propria
    /// (<c>Gumatos.RealmApi.UI</c>, namespace do projeto <c>api/</c>). Ela existe para que a plumbing de
    /// UI GENERICA do mod (clonar um objeto nativo e ligar um clique) deixe de ser escrita a mao aqui e
    /// passe a ser UMA implementacao so, a da API.
    ///
    /// ESCOPO: so' os dois primitivos que a API cobre de forma EXATAMENTE EQUIVALENTE ao que o mod ja'
    /// fazia — <c>UIFactory.Clone</c> e <c>UIFactory.BindClick</c>. O que a API NAO cobre de forma
    /// equivalente continua como estava, com o motivo medido em
    /// <c>docs/automacao/INT-R1-C4-parte01.md</c> secao 6 e <c>parte02</c>:
    ///   * TEXTO: <c>UIFactory.SetText</c> so' cobre <c>UnityEngine.UI.Text</c> e falha fechado em
    ///     TextMeshPro (<c>api/Plugin/Ui/UIFactory.cs:81-87</c>); o mod rotula com <c>TextMeshProUGUI</c>;
    ///   * BUSCA: <c>UIFactory.FindChild</c> LANCA quando o filho nao existe (<c>UIFactory.cs:62-68</c>);
    ///     o mod usa <c>Transform.Find</c> + tratamento de nulo (reaproveitar o clone existente);
    ///   * ABAS/BOTOES DE BARRA: <c>ActionBarUI</c>/<c>SkillTreeUI</c>/<c>MenuUI</c> REGISTRAM o pedido e
    ///     mandam o hospedeiro nativo reconstruir; quem cria o elemento visual aqui e' o mod, a partir de
    ///     um prefab nativo — usar a API mudaria o comportamento;
    ///   * <c>NativeUiHelpers.ClearClickListeners</c>/<c>DisableLocalizers</c>: nao existem na familia
    ///     <c>UI</c> (a lista de 21 assinaturas nao tem equivalente) e continuam no mod.
    ///
    /// POR QUE A EQUIVALENCIA E' PROVADA (e nao suposta): o fonte do jogo
    /// (<c>lib/UnityEngine.CoreModule.dll</c>, tipo <c>UnityEngine.Object</c>) mostra que
    /// <c>Instantiate(Object original, Transform parent)</c> chamado com DOIS argumentos cai em
    /// <c>Instantiate(original, parent, instantiateInWorldSpace: false)</c>, e <c>UIFactory.Clone</c>
    /// faz exatamente <c>Object.Instantiate(template, parent, false)</c> e depois nomeia o clone — o
    /// mesmo par de efeitos, na mesma ordem. <c>UIFactory.BindClick</c> faz
    /// <c>go.GetComponent&lt;Button&gt;().onClick.AddListener(onClick)</c>, o mesmo
    /// <c>AddListener</c> que o mod chamava. Comparacao literal e comando reprodutivel em
    /// <c>docs/automacao/INT-R1-C4-parte02.md</c>.
    ///
    /// VINCULO: a familia <c>UI</c> da API e' COMPORTAMENTAL (muta a UI) e so' funciona depois de um
    /// <c>UiFamily.Bind</c> integral, com <c>allowMutation: true</c>, no thread do vinculo (o thread
    /// principal do Unity). A ponte vincula PREGUICOSAMENTE, na primeira chamada, e reusa o vinculo
    /// (a API ja' nega uso fora do thread dele). Ela NAO tem fallback silencioso: se o vinculo nao
    /// fechar, a operacao lanca e o caminho do mod que chamou (todos os ganchos sao aplicados um a um,
    /// em try/catch — regra TRV-1 do repositorio) registra o motivo no log, em vez de injetar UI pela
    /// metade.
    ///
    /// HOSPEDEIRO: o unico hospedeiro que os dois primitivos desta ponte poderiam precisar e' o
    /// <c>GUIManager</c> (familia <c>UIFactory</c>). Ele e' entregue quando existe — <c>Bind</c> aceita
    /// hospedeiro nulo (aquela familia fica indisponivel e falha fechado so' quando usada), e
    /// <c>Clone</c>/<c>BindClick</c> nao consultam hospedeiro nenhum. Os outros tres hospedeiros
    /// (<c>CurrentCharacterUI</c>, <c>SkillTreeManager</c>, <c>MenuTabManager</c>) desta entrega ficam
    /// nulos DE PROPOSITO: o mod nao usa as familias que dependem deles (ver o escopo acima), e
    /// preencher um hospedeiro que nao e' usado seria assumir um caminho ao vivo que a API nao pede.
    /// </summary>
    internal static class RstvApiUi
    {
        /// <summary>Vinculo vigente da familia <c>UI</c> (a API e' a dona do estado).</summary>
        internal static bool Vinculada
        {
            get { return UiFamily.IsBound; }
        }

        /// <summary>Ultimo motivo de falha do vinculo (null quando vinculou). So' para log/diagnostico.</summary>
        internal static string UltimoMotivo { get; private set; }

        /// <summary>
        /// Fecha o vinculo da familia <c>UI</c> se ainda nao houver um. Idempotente: com vinculo vigente
        /// nao faz nada (nem re-resolve os 17 requisitos). Reusa o vinculo do processo — esta entrega tem
        /// um consumidor so'.
        /// </summary>
        internal static void AsegurarVinculo()
        {
            if (UiFamily.IsBound)
            {
                return;
            }

            try
            {
                UiHosts hosts = new UiHosts
                {
                    // Hospedeiro honesto: o manager de UI do jogo, quando ele ja' existe (pode ser nulo no
                    // primeiro quadro; a familia UIFactory so' consulta hospedeiro no Clone de 1 argumento,
                    // que esta ponte nao usa).
                    GuiManager = GUIManager.instance
                };

                // O assembly do JOGO e' o proprio Assembly-CSharp: o mod ja' compila contra ele (o .csproj
                // referencia lib/Assembly-CSharp.dll), e a API resolve os 17 requisitos por metadados nele.
                UiFamily.Bind(typeof(GUIManager).Assembly, hosts, allowMutation: true);

                UltimoMotivo = null;
                Plugin.Log.LogInfo("RSTV INT-R1-C4: familia 'UI' da API vinculada (allowMutation=true) — " +
                                   "clone/clique de UI passam a vir de Gumatos.RealmApi.UI.");
            }
            catch (Exception e)
            {
                UltimoMotivo = e.GetType().Name + ": " + e.Message;
                Plugin.Log.LogError("RSTV INT-R1-C4: NAO foi possivel vincular a familia 'UI' da API — " +
                                    "a plumbing de UI desta chamada nao sera executada (" + UltimoMotivo +
                                    "). O mod depende de com.gumatos.realmapi; confira a versao instalada.");
                throw;
            }
        }

        /// <summary>
        /// Clona <paramref name="molde"/> sob <paramref name="pai"/> com o nome dado. EQUIVALENTE ao par
        /// <c>Object.Instantiate(molde, pai)</c> + <c>clone.name = nome</c> que o mod escrevia a mao
        /// (medido: o overload de 2 argumentos do jogo cai em <c>instantiateInWorldSpace: false</c>, que
        /// e' o mesmo argumento de <c>UIFactory.Clone</c>).
        /// </summary>
        internal static GameObject Clonar(GameObject molde, Transform pai, string nome)
        {
            AsegurarVinculo();
            return UIFactory.Clone(molde, pai, nome);
        }

        /// <summary>
        /// Liga <paramref name="acao"/> ao <c>onClick</c> do botao <paramref name="alvo"/>.
        /// EQUIVALENTE ao <c>AddListener</c> direto que o mod escrevia a mao.
        ///
        /// ATENCAO (RSTV-12, aceite ANTERIOR que esta entrega NAO reabre): quem precisa DESCARTAR o
        /// <c>onClick</c> SERIALIZADO do molde continua chamando
        /// <c>NativeUiHelpers.ClearClickListeners</c> ANTES desta ponte — trocar a INSTANCIA do evento e'
        /// o unico jeito (a familia <c>UI</c> da API nao expoe esse primitivo).
        /// </summary>
        internal static void LigarClique(GameObject alvo, UnityAction acao)
        {
            AsegurarVinculo();
            UIFactory.BindClick(alvo, acao);
        }
    }
}
