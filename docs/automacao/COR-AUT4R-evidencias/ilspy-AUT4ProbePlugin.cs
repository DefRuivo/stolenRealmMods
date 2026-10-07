using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using BepInEx;
using BepInEx.Bootstrap;
using BepInEx.Configuration;
using HarmonyLib;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.LowLevel;
using UnityEngine.PlayerLoop;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace Aut4Probe;

[BepInPlugin("com.gumatos.aut4probe", "AUT-4 Probe (coletor runtime, instrumento)", "0.1.0")]
public class Aut4ProbePlugin : BaseUnityPlugin
{
	public const string Guid = "com.gumatos.aut4probe";

	public const string Versao = "0.1.0";

	private ConfigEntry<bool> _autorizado;

	private ConfigEntry<string> _outDir;

	private ConfigEntry<float> _orcamento;

	private ConfigEntry<bool> _navegar;

	private ConfigEntry<string> _perfilDir;

	private ConfigEntry<string> _hashFonte;

	private ConfigEntry<int> _maxTextos;

	private ConfigEntry<string> _sessaoCfg;

	private ConfigEntry<bool> _demostrar;

	private ConfigEntry<string> _marcador;

	internal static Aut4ProbePlugin Instancia;

	private Harmony _harmony;

	private object _personagemDoModal;

	private Dictionary<string, object> _snapshotAntes;

	private Dictionary<string, object> _snapshotDepois;

	private string _tooltipPaiAntes;

	private object _tooltipIndiceAntes;

	private bool _tooltipAntesLido;

	private string _tooltipPaiDepois;

	private object _tooltipIndiceDepois;

	private object _janelasDuplicadas;

	private readonly Dictionary<string, object> _res = new Dictionary<string, object>();

	private readonly Dictionary<string, object> _passos = new Dictionary<string, object>();

	private readonly List<string> _marcos = new List<string>();

	private readonly List<object> _observacoes = new List<object>();

	private readonly List<string> _arquivosDePrint = new List<string>();

	private string _dir;

	private string _sessao;

	private float _t0;

	private float _orcamentoSeg;

	private long _ticks;

	private int _fase;

	private int _quadros;

	private bool _concluido;

	private bool _tentouMotor;

	private string _printAtual;

	private bool _autorizadoOk;

	private static readonly string[] NomesDeAlvo = new string[8] { "Title", "Description", "Subtitle", "BigText", "FooterText", "IfEquippedText", "BossName", "playerName" };

	private const int F_ESPERA_UI = 0;

	private const int F_LEITURA = 1;

	private const int F_PRINT1 = 2;

	private const int F_FINAL = 3;

	private const int F_PRINT2 = 4;

	private const string JanelaRstvRoot = "RstvSkillTreesWindow";

	private static readonly string[][] FUNIS = new string[4][]
	{
		new string[2] { "OptionsManager", "Localize" },
		new string[2] { "GUIManager", "Update" },
		new string[2] { "Tooltip", "ShowTooltip" },
		new string[2] { "Tooltip", "ShowSkillTooltip" }
	};

	private void Awake()
	{
		//IL_0372: Unknown result type (might be due to invalid IL or missing references)
		//IL_037c: Expected O, but got Unknown
		Instancia = this;
		_autorizado = ((BaseUnityPlugin)this).Config.Bind<bool>("Geral", "Autorizado", false, "Coleta runtime OPT-IN. Default false: sem isto o probe NAO le, NAO navega e NAO tira print.");
		_outDir = ((BaseUnityPlugin)this).Config.Bind<string>("Geral", "OutDir", "C:\\dev\\stolen-realm\\scratch\\aut4\\out", "Pasta de saida (JSON + PNG).");
		_orcamento = ((BaseUnityPlugin)this).Config.Bind<float>("Geral", "OrcamentoSegundos", 120f, "Teto de tempo depois que a UI existe. Passado isso o probe encerra com o que leu.");
		_navegar = ((BaseUnityPlugin)this).Config.Bind<bool>("Geral", "Navegar", false, "Navegacao por dentro (onClick do botao). Default DESLIGADO.");
		_perfilDir = ((BaseUnityPlugin)this).Config.Bind<string>("Geral", "PerfilDir", "", "Perfil do r2modman (para o manifesto de rollback).");
		_hashFonte = ((BaseUnityPlugin)this).Config.Bind<string>("Geral", "HashFonte", "", "sha256 do fonte/DLL medido; entra em cada observacao (procedencia runtime).");
		_maxTextos = ((BaseUnityPlugin)this).Config.Bind<int>("Geral", "MaxTextos", 400, "Teto de TMP_Text lidos por rodada.");
		_sessaoCfg = ((BaseUnityPlugin)this).Config.Bind<string>("Geral", "Sessao", "", "Identidade da RODADA, gerada pelo driver. Vence o carimbo local: e ela que liga a evidencia a esta rodada (A1).");
		_demostrar = ((BaseUnityPlugin)this).Config.Bind<bool>("Geral", "DemostrarTooltip", false, "Porta OPT-IN de ida-e-volta: chama Tooltip.ShowTooltip(marcador) e RELE o titulo. E LEITURA (nao simulacao do produto) e o default e FALSE. (A6)");
		_marcador = ((BaseUnityPlugin)this).Config.Bind<string>("Geral", "MarcadorIdaEVolta", "", "Marcador unico da ida-e-volta (gerado pelo driver).");
		_dir = _outDir.Value;
		_orcamentoSeg = _orcamento.Value;
		_t0 = Time.realtimeSinceStartup;
		_sessao = (string.IsNullOrWhiteSpace(_sessaoCfg.Value) ? DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture) : _sessaoCfg.Value);
		try
		{
			Directory.CreateDirectory(_dir);
		}
		catch (Exception ex)
		{
			((BaseUnityPlugin)this).Logger.LogError((object)("AUT4 PROBE: pasta de saida '" + _dir + "': " + ex.Message));
		}
		_res["rotina"] = "AUT-4";
		_res["esquema"] = "AUT-4/1";
		_res["instrumento"] = "AUT4Probe 0.1.0 (BepInEx/plugins/AUT4Probe; removido no fim)";
		_res["aviso"] = "Coleta SOMENTE leitura; nenhum mod do pacote foi alterado.";
		_res["sessao"] = _sessao;
		_res["hash_fonte"] = _hashFonte.Value;
		_res["aplicacao"] = Aplicacao();
		_res["passos"] = _passos;
		_res["observacoes"] = _observacoes;
		if (!_autorizado.Value)
		{
			_res["status"] = "NAO_EXERCITADO";
			_res["motivo"] = "coleta NAO autorizada (Autorizado=false): nenhuma leitura, PNG ou navegacao.";
			_res["fase"] = "nao-exercitado";
			Marco("AUT4 PROBE: SEM autorizacao (Autorizado=false) - grava NAO_EXERCITADO e nao toca em nada.");
			Escrever();
			return;
		}
		_autorizadoOk = true;
		_res["status"] = "INICIADO";
		_res["fase"] = "carregado";
		Marco("AUT4 PROBE 0.1.0 carregado (coleta AUTORIZADA, somente leitura).");
		try
		{
			_harmony = new Harmony("com.gumatos.aut4probe");
			Gancho("GUIManager", "Update");
			GanchoTodos("OptionsManager", "Localize");
		}
		catch (Exception ex2)
		{
			((BaseUnityPlugin)this).Logger.LogError((object)("AUT4 PROBE: ganchos: " + ex2.GetType().Name + ": " + ex2.Message));
		}
		InstalarNoPlayerLoop();
		Escrever();
	}

	private void InstalarNoPlayerLoop()
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0005: Unknown result type (might be due to invalid IL or missing references)
		//IL_0008: Unknown result type (might be due to invalid IL or missing references)
		//IL_0028: Unknown result type (might be due to invalid IL or missing references)
		//IL_0032: Expected O, but got Unknown
		//IL_0032: Unknown result type (might be due to invalid IL or missing references)
		//IL_0033: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cb: Unknown result type (might be due to invalid IL or missing references)
		//IL_003b: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Unknown result type (might be due to invalid IL or missing references)
		//IL_009a: Unknown result type (might be due to invalid IL or missing references)
		//IL_009b: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b3: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			PlayerLoopSystem currentPlayerLoop = PlayerLoop.GetCurrentPlayerLoop();
			PlayerLoopSystem val = default(PlayerLoopSystem);
			val.type = typeof(Aut4ProbePlugin);
			val.updateDelegate = new UpdateFunction(DelegadoDeQuadro);
			PlayerLoopSystem val2 = val;
			for (int i = 0; i < currentPlayerLoop.subSystemList.Length; i++)
			{
				if (!(currentPlayerLoop.subSystemList[i].type != typeof(Update)))
				{
					PlayerLoopSystem[] array = (PlayerLoopSystem[])(((object)currentPlayerLoop.subSystemList[i].subSystemList) ?? ((object)new PlayerLoopSystem[0]));
					PlayerLoopSystem[] array2 = (PlayerLoopSystem[])(object)new PlayerLoopSystem[array.Length + 1];
					Array.Copy(array, array2, array.Length);
					array2[array.Length] = val2;
					currentPlayerLoop.subSystemList[i].subSystemList = array2;
					PlayerLoop.SetPlayerLoop(currentPlayerLoop);
					Marco("AUT4 PROBE: subsistema injetado no PlayerLoop (Update) - motor por quadro ativo.");
					return;
				}
			}
			Marco("AUT4 PROBE: NAO achei o subsistema Update no PlayerLoop.");
		}
		catch (Exception ex)
		{
			((BaseUnityPlugin)this).Logger.LogWarning((object)("AUT4 PROBE: injecao no PlayerLoop falhou: " + ex.GetType().Name + ": " + ex.Message));
		}
	}

	private void DelegadoDeQuadro()
	{
		try
		{
			Tick("playerloop");
		}
		catch
		{
		}
	}

	private void Gancho(string tipo, string metodo)
	{
		try
		{
			Type type = Tipo(tipo);
			if (type == null)
			{
				Marco("AUT4 PROBE: tipo '" + tipo + "' NAO encontrado - gancho pulado.");
				return;
			}
			MethodInfo method = type.GetMethod(metodo, BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic, null, Type.EmptyTypes, null);
			if (method == null)
			{
				Marco("AUT4 PROBE: '" + tipo + "." + metodo + "()' NAO existe - gancho pulado.");
			}
			else
			{
				Aplicar(method, tipo + "." + metodo + "()");
			}
		}
		catch (Exception ex)
		{
			((BaseUnityPlugin)this).Logger.LogWarning((object)("AUT4 PROBE: gancho " + tipo + "." + metodo + ": " + ex.Message));
		}
	}

	private void GanchoTodos(string tipo, string metodo)
	{
		try
		{
			Type type = Tipo(tipo);
			if (type == null)
			{
				return;
			}
			MethodInfo[] methods = type.GetMethods(BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
			foreach (MethodInfo methodInfo in methods)
			{
				if (!(methodInfo.Name != metodo) && !methodInfo.IsAbstract)
				{
					Aplicar(methodInfo, tipo + "." + metodo + "(" + methodInfo.GetParameters().Length + " arg)");
				}
			}
		}
		catch (Exception ex)
		{
			((BaseUnityPlugin)this).Logger.LogWarning((object)("AUT4 PROBE: ganchos " + tipo + "." + metodo + ": " + ex.Message));
		}
	}

	private void Aplicar(MethodBase alvo, string rotulo)
	{
		//IL_0016: Unknown result type (might be due to invalid IL or missing references)
		//IL_001c: Expected O, but got Unknown
		try
		{
			HarmonyMethod val = new HarmonyMethod(typeof(Aut4ProbePlugin).GetMethod("PostfixDoGancho", BindingFlags.Static | BindingFlags.NonPublic));
			_harmony.Patch(alvo, (HarmonyMethod)null, val, (HarmonyMethod)null, (HarmonyMethod)null, (HarmonyMethod)null);
			Marco("AUT4 PROBE: gancho aplicado em " + rotulo);
		}
		catch (Exception ex)
		{
			((BaseUnityPlugin)this).Logger.LogWarning((object)("AUT4 PROBE: patch em " + rotulo + " falhou: " + ex.Message));
		}
	}

	private static void PostfixDoGancho()
	{
		try
		{
			Instancia?.Tick("gancho");
		}
		catch
		{
		}
	}

	private void CriarMotor()
	{
		//IL_0015: Unknown result type (might be due to invalid IL or missing references)
		//IL_001a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0020: Expected O, but got Unknown
		if (_tentouMotor)
		{
			return;
		}
		_tentouMotor = true;
		try
		{
			GameObject val = new GameObject("AUT4Probe_Motor");
			Object.DontDestroyOnLoad((Object)val);
			val.AddComponent<MotorDoProbe>();
			Marco("AUT4 PROBE: motor proprio criado (GameObject vivo) - Update por quadro como reforco.");
		}
		catch (Exception ex)
		{
			((BaseUnityPlugin)this).Logger.LogWarning((object)("AUT4 PROBE: motor proprio: " + ex.Message));
		}
	}

	private void Update()
	{
		if (_autorizadoOk)
		{
			Tick("BepInEx.Update");
		}
	}

	internal void Tick(string origem)
	{
		if (_concluido || !_autorizadoOk)
		{
			return;
		}
		_ticks++;
		try
		{
			if (_ticks <= 3)
			{
				Marco("AUT4 PROBE: tick via " + origem + " (quadro " + _ticks + ")");
			}
			if (!_tentouMotor)
			{
				CriarMotor();
			}
			if (_fase > 0 && Time.realtimeSinceStartup - _t0 > _orcamentoSeg + 90f)
			{
				_res["status"] = "ORCAMENTO_ESTOURADO";
				Marco("AUT4 PROBE: orcamento de tempo estourado - encerrando com o que ja foi lido.");
				Finalizar();
			}
			else
			{
				Passo();
			}
		}
		catch (Exception ex)
		{
			_passos["tick.fase" + _fase] = Json.Campos("erro", ex.GetType().Name + ": " + ex.Message);
			_res["status"] = "ERRO";
			_concluido = true;
			Escrever();
		}
	}

	private void Passo()
	{
		switch (_fase)
		{
		case 0:
		{
			if (_quadros == 0)
			{
				_res["fase"] = "aguardando-ui";
				Escrever();
			}
			_quadros++;
			bool flag = false;
			bool flag2 = false;
			try
			{
				flag = UiExiste();
			}
			catch
			{
			}
			try
			{
				flag2 = flag && TemTextoVisivel();
			}
			catch
			{
			}
			if (flag && flag2)
			{
				_passos["aguardou_ui"] = Json.Campos("ok", true, "quadros_ate_a_ui", _quadros, "criterio", "GUIManager.instance.tooltip != null E existe TMP_Text ativo com GetParsedText() nao vazio (a tela desenhou)");
				_passos["mods_carregados"] = ModsCarregados();
				_passos["estado_da_tela"] = EstadoDaTela();
				LembrarTooltip();
				Ir(1, "lendo-objetos");
			}
			else if (_quadros > 90000)
			{
				_passos["aguardou_ui"] = Json.Campos("ok", false, "quadros", _quadros, "ui_existe", flag, "texto_visivel", flag2);
				_res["status"] = "SEM_UI";
				Marco("AUT4 PROBE: ABORTOU - a UI com texto na tela nao apareceu.");
				Finalizar();
			}
			break;
		}
		case 1:
			IniciarSnapshotDoModal();
			try
			{
				ColetarObservacoes();
			}
			catch (Exception ex)
			{
				_passos["coleta"] = "erro: " + ex.GetType().Name + ": " + ex.Message;
			}
			if (_demostrar.Value)
			{
				try
				{
					DemostrarIdaEVolta();
				}
				catch (Exception ex2)
				{
					_passos["ida_e_volta"] = "erro: " + ex2.GetType().Name + ": " + ex2.Message;
				}
			}
			try
			{
				_res["owners_harmony"] = OwnersHarmony();
			}
			catch (Exception ex3)
			{
				_passos["owners"] = "erro: " + ex3.GetType().Name;
			}
			try
			{
				_res["rollback"] = Rollback();
			}
			catch (Exception ex4)
			{
				_passos["rollback"] = "erro: " + ex4.GetType().Name;
			}
			if (_navegar.Value)
			{
				TentarNavegar();
			}
			PedirPrint("01-ui");
			Ir(2, "print-01");
			break;
		case 2:
			if (PrintPronto() || _quadros++ > 600)
			{
				FecharPrint("01-ui");
				Ir(3, "final");
			}
			break;
		case 3:
			AtualizarGuardasDepois();
			PedirPrint("02-final");
			Ir(4, "print-02");
			break;
		case 4:
			if (PrintPronto() || _quadros++ > 600)
			{
				FecharPrint("02-final");
				Finalizar();
			}
			break;
		}
	}

	private void Ir(int fase, string legivel)
	{
		_fase = fase;
		_quadros = 0;
		_res["fase"] = legivel;
		Escrever();
	}

	private void Finalizar()
	{
		try
		{
			AtualizarGuardasDepois();
		}
		catch
		{
		}
		try
		{
			_res["owners_harmony"] = (_res.ContainsKey("owners_harmony") ? _res["owners_harmony"] : OwnersHarmony());
		}
		catch
		{
		}
		try
		{
			_res["manifest"] = Manifest();
		}
		catch
		{
		}
		try
		{
			_res["rollback"] = Rollback();
		}
		catch
		{
		}
		_res["prints"] = _arquivosDePrint;
		_res["marcos"] = _marcos;
		_res["total_observacoes"] = _observacoes.Count;
		_res["gerado_em"] = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture);
		_res["duracao_s"] = Math.Round(Time.realtimeSinceStartup - _t0, 3);
		string text = (_res.ContainsKey("status") ? Convert.ToString(_res["status"]) : "");
		if (text != "SEM_UI" && text != "ORCAMENTO_ESTOURADO" && text != "ERRO")
		{
			_res["status"] = "CONCLUIDO";
		}
		_res["fase"] = "concluido";
		Marco("AUT4 PROBE: FIM - " + _observacoes.Count + " observacoes, " + _arquivosDePrint.Count + " prints.");
		_concluido = true;
		Escrever();
	}

	private void ColetarObservacoes()
	{
		TMP_Text[] array = Recursos<TMP_Text>();
		int num = 0;
		List<object> ownersFunil = OwnersDosFunils();
		TMP_Text[] array2 = array;
		foreach (TMP_Text val in array2)
		{
			if (!((Object)(object)val == (Object)null))
			{
				if (num >= _maxTextos.Value)
				{
					break;
				}
				bool num2 = Array.IndexOf(NomesDeAlvo, ((Object)((Component)val).gameObject).name) >= 0;
				bool flag = !string.IsNullOrEmpty(val.text);
				if (num2 || (((Component)val).gameObject.activeInHierarchy && flag))
				{
					_observacoes.Add(Leitura(val, ownersFunil));
					num++;
				}
			}
		}
		_res["observacoes"] = _observacoes;
		_res["total_tmp_text"] = array.Length;
		_res["lidos"] = num;
	}

	private Dictionary<string, object> Leitura(TMP_Text t, List<object> ownersFunil)
	{
		//IL_00d9: Unknown result type (might be due to invalid IL or missing references)
		Material mat = t.fontSharedMaterial;
		TMP_FontAsset font = t.font;
		Dictionary<string, object> dictionary = new Dictionary<string, object>();
		if ((Object)(object)mat != (Object)null)
		{
			string[] array = new string[5] { "OUTLINE_ON", "UNDERLAY_ON", "UNDERLAY_INNER", "GLOW_ON", "BEVEL_ON" };
			foreach (string kw in array)
			{
				dictionary[kw] = SeguroBool(() => mat.IsKeywordEnabled(kw));
			}
		}
		Dictionary<string, object> dictionary2 = Json.Campos("texto", CorDe(((Graphic)t).color), "face", CorDoMaterial(mat, "_FaceColor"), "contorno", CorDoMaterial(mat, "_OutlineColor"), "sombra", CorDoMaterial(mat, "_UnderlayColor"));
		return Json.Campos("objeto", ((Object)((Component)t).gameObject).name, "caminho", Caminho(t.transform), "componente", ((object)t).GetType().Name, "ativo_na_hierarquia", ((Component)t).gameObject.activeInHierarchy, "visivel_na_tela", SeguroBool(() => ((Behaviour)t).isActiveAndEnabled && ((Component)t).gameObject.activeInHierarchy), "texto_bruto", Trunc(t.text, 600), "texto_renderizado", Trunc(Seguro(() => t.GetParsedText()) as string, 600), "fonte", ((Object)(object)font != (Object)null) ? ((Object)font).name : null, "material", ((Object)(object)mat != (Object)null) ? ((Object)mat).name : null, "shader", ((Object)(object)mat != (Object)null) ? Nome(mat.shader) : null, "shader_suportado", (Object)(object)mat != (Object)null && (Object)(object)mat.shader != (Object)null && mat.shader.isSupported, "keywords", dictionary, "cores", dictionary2, "geometria", Geometria(t), "tamanho_fonte", Arred(t.fontSize), "owners", ownersFunil, "personagem", Contexto(), "snapshot_antes", _snapshotAntes, "snapshot_depois", _snapshotDepois, "tooltip_pai_antes", _tooltipPaiAntes, "tooltip_pai_depois", _tooltipPaiDepois, "tooltip_indice_antes", _tooltipIndiceAntes, "tooltip_indice_depois", _tooltipIndiceDepois, "janelas_duplicadas", _janelasDuplicadas, "nota_texto_renderizado", ((Component)t).gameObject.activeInHierarchy ? null : "objeto INATIVO: GetParsedText() sai vazio ate o TMP gerar o mesh; vale o texto_bruto.");
	}

	private Dictionary<string, object> SnapshotDoPersonagem()
	{
		object personagemDoModal = _personagemDoModal;
		object obj = null;
		object obj2 = null;
		if (personagemDoModal != null)
		{
			try
			{
				object obj3 = Membro(personagemDoModal, "SkillsFromPoints");
				if (obj3 is IEnumerable enumerable && !(obj3 is string))
				{
					List<object> list = new List<object>();
					foreach (object item in enumerable)
					{
						if (item != null)
						{
							object obj4 = Membro(item, "SkillName");
							list.Add((obj4 != null) ? Convert.ToString(obj4, CultureInfo.InvariantCulture) : NomeDoObjeto(item));
						}
					}
					obj = list;
				}
			}
			catch
			{
			}
			try
			{
				obj2 = Membro(personagemDoModal, "UnspentSkillPoints");
			}
			catch
			{
			}
		}
		Dictionary<string, object> dictionary = Json.Campos("personagem", (personagemDoModal == null) ? null : Convert.ToString(Membro(personagemDoModal, "CharacterName"), CultureInfo.InvariantCulture), "skills", obj, "pontos", obj2);
		if (obj != null)
		{
			dictionary["fonte_skills"] = "Character.SkillsFromPoints";
		}
		if (obj2 != null)
		{
			dictionary["fonte_pontos"] = "Character.UnspentSkillPoints";
		}
		return dictionary;
	}

	private void IniciarSnapshotDoModal()
	{
		_personagemDoModal = PersonagemDaSessao();
		_snapshotAntes = SnapshotDoPersonagem();
		_snapshotDepois = SnapshotDoPersonagem();
	}

	private object PersonagemDaSessao()
	{
		try
		{
			Type type = Tipo("RoguelikeSkillTreeVisualizer.ReadOnlySession");
			if (type == null || !object.Equals(Estatico(type, "Active"), true))
			{
				return null;
			}
			return Estatico(type, "Target");
		}
		catch
		{
			return null;
		}
	}

	private static string NomeDoObjeto(object o)
	{
		Object val = (Object)((o is Object) ? o : null);
		if (val != (Object)null)
		{
			return val.name;
		}
		if (o != null)
		{
			return Convert.ToString(o, CultureInfo.InvariantCulture);
		}
		return null;
	}

	private object TooltipVivo()
	{
		try
		{
			Type type = Tipo("GUIManager");
			object obj = ((type == null) ? null : Estatico(type, "instance"));
			return (obj == null) ? null : Membro(obj, "tooltip");
		}
		catch
		{
			return null;
		}
	}

	private static string TooltipPai(object tooltip)
	{
		Component val = (Component)((tooltip is Component) ? tooltip : null);
		if ((Object)(object)val == (Object)null || (Object)(object)val.transform == (Object)null || (Object)(object)val.transform.parent == (Object)null)
		{
			return null;
		}
		return Caminho(val.transform.parent);
	}

	private static object TooltipIndice(object tooltip)
	{
		Component val = (Component)((tooltip is Component) ? tooltip : null);
		if ((Object)(object)val == (Object)null || (Object)(object)val.transform == (Object)null)
		{
			return null;
		}
		return val.transform.GetSiblingIndex();
	}

	private void LembrarTooltip()
	{
		if (!_tooltipAntesLido)
		{
			object obj = TooltipVivo();
			if (obj != null)
			{
				_tooltipAntesLido = true;
				_tooltipPaiAntes = TooltipPai(obj);
				_tooltipIndiceAntes = TooltipIndice(obj);
			}
		}
	}

	private object JanelasDuplicadas()
	{
		//IL_0051: Unknown result type (might be due to invalid IL or missing references)
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			int num = 0;
			Transform[] array = Recursos<Transform>();
			foreach (Transform val in array)
			{
				if (!((Object)(object)val == (Object)null) && !((Object)(object)((Component)val).gameObject == (Object)null) && !(((Object)((Component)val).gameObject).name != "RstvSkillTreesWindow") && ((Component)val).gameObject.activeInHierarchy)
				{
					Scene scene = ((Component)val).gameObject.scene;
					if (((Scene)(ref scene)).IsValid())
					{
						num++;
					}
				}
			}
			return (num > 1) ? (num - 1) : 0;
		}
		catch
		{
			return null;
		}
	}

	private void AtualizarGuardasDepois()
	{
		Dictionary<string, object> dictionary = SnapshotDoPersonagem();
		if (_snapshotDepois != null)
		{
			_snapshotDepois["personagem"] = dictionary["personagem"];
			_snapshotDepois["skills"] = dictionary["skills"];
			_snapshotDepois["pontos"] = dictionary["pontos"];
		}
		object obj = TooltipVivo();
		_tooltipPaiDepois = ((obj == null) ? null : TooltipPai(obj));
		_tooltipIndiceDepois = ((obj == null) ? null : TooltipIndice(obj));
		_janelasDuplicadas = JanelasDuplicadas();
		foreach (object observaco in _observacoes)
		{
			if (observaco is Dictionary<string, object> dictionary2)
			{
				dictionary2["snapshot_depois"] = _snapshotDepois;
				dictionary2["tooltip_pai_depois"] = _tooltipPaiDepois;
				dictionary2["tooltip_indice_depois"] = _tooltipIndiceDepois;
				dictionary2["janelas_duplicadas"] = _janelasDuplicadas;
			}
		}
	}

	private object Contexto()
	{
		Dictionary<string, object> dictionary = new Dictionary<string, object>();
		try
		{
			Type type = Tipo("GUIManager");
			object obj = ((type == null) ? null : Estatico(type, "instance"));
			dictionary["gui_state"] = ((obj == null) ? null : Convert.ToString(Membro(obj, "CurrentGuiState"), CultureInfo.InvariantCulture));
		}
		catch
		{
		}
		try
		{
			Type type2 = Tipo("GameLogic");
			object obj3 = ((type2 == null) ? null : Estatico(type2, "instance"));
			object obj4 = ((obj3 == null) ? null : Membro(obj3, "CurrentlySelectedCharacter"));
			dictionary["tem_personagem_selecionado"] = obj4 != null;
			dictionary["personagem"] = ((obj4 == null) ? null : Convert.ToString(Membro(obj4, "CharacterName"), CultureInfo.InvariantCulture));
		}
		catch
		{
		}
		return dictionary;
	}

	private bool UiExiste()
	{
		Type type = Tipo("GUIManager");
		if (type == null)
		{
			return false;
		}
		object obj = Estatico(type, "instance");
		if (obj == null)
		{
			return false;
		}
		object obj2 = Membro(obj, "tooltip");
		if (obj2 != null)
		{
			return Membro(obj2, "Title") is TMP_Text;
		}
		return false;
	}

	private bool TemTextoVisivel()
	{
		TMP_Text[] array = Recursos<TMP_Text>();
		foreach (TMP_Text t in array)
		{
			if (!((Object)(object)t == (Object)null) && ((Component)t).gameObject.activeInHierarchy && !string.IsNullOrEmpty(t.text) && !string.IsNullOrEmpty(Seguro(() => t.GetParsedText()) as string))
			{
				return true;
			}
		}
		return false;
	}

	private Dictionary<string, object> EstadoDaTela()
	{
		Dictionary<string, object> dictionary = new Dictionary<string, object>();
		try
		{
			Type type = Tipo("GUIManager");
			object obj = ((type == null) ? null : Estatico(type, "instance"));
			dictionary["GUIManager.instance"] = obj != null;
			dictionary["CurrentGuiState"] = ((obj == null) ? null : Convert.ToString(Membro(obj, "CurrentGuiState"), CultureInfo.InvariantCulture));
			dictionary["tooltips_em_memoria"] = ((!(Tipo("Tooltip") == null)) ? Resources.FindObjectsOfTypeAll(Tipo("Tooltip")).Length : 0);
		}
		catch (Exception ex)
		{
			dictionary["erro"] = ex.GetType().Name + ": " + ex.Message;
		}
		return dictionary;
	}

	private Dictionary<string, object> ModsCarregados()
	{
		List<object> list = new List<object>();
		try
		{
			foreach (KeyValuePair<string, PluginInfo> pluginInfo in Chainloader.PluginInfos)
			{
				PluginInfo value = pluginInfo.Value;
				if (value != null && value.Metadata != null)
				{
					list.Add(Json.Campos("guid", value.Metadata.GUID, "nome", value.Metadata.Name, "versao", (value.Metadata.Version == null) ? null : value.Metadata.Version.ToString(), "instrumento", value.Metadata.GUID == "com.gumatos.aut4probe"));
				}
			}
		}
		catch (Exception ex)
		{
			return Json.Campos("erro", ex.GetType().Name + ": " + ex.Message);
		}
		return Json.Campos("total", list.Count, "plugins", list);
	}

	private List<object> OwnersDosFunils()
	{
		List<object> list = new List<object>();
		string[][] fUNIS = FUNIS;
		foreach (string[] array in fUNIS)
		{
			foreach (object item in OwnersDe(array[0], array[1]))
			{
				if (!list.Contains(item))
				{
					list.Add(item);
				}
			}
		}
		return list;
	}

	private Dictionary<string, object> OwnersHarmony()
	{
		Dictionary<string, object> dictionary = new Dictionary<string, object>();
		string[][] fUNIS = FUNIS;
		foreach (string[] array in fUNIS)
		{
			string key = array[0] + "." + array[1];
			dictionary[key] = Json.Campos("metodo_encontrado", Tipo(array[0]) != null, "owners", OwnersDe(array[0], array[1]));
		}
		return Json.Campos("criterio", "owners lidos de Harmony.GetPatchInfo no metodo vivo - nao e presuncao", "por_metodo", dictionary);
	}

	private List<object> OwnersDe(string tipo, string metodo)
	{
		List<object> list = new List<object>();
		try
		{
			Type type = Tipo(tipo);
			if (type == null)
			{
				return list;
			}
			MethodInfo[] methods = type.GetMethods(BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
			foreach (MethodInfo methodInfo in methods)
			{
				if (methodInfo.Name != metodo || methodInfo.IsAbstract)
				{
					continue;
				}
				Patches patchInfo = Harmony.GetPatchInfo((MethodBase)methodInfo);
				if (patchInfo == null || patchInfo.Owners == null)
				{
					continue;
				}
				foreach (string owner in patchInfo.Owners)
				{
					if (!list.Contains(owner))
					{
						list.Add(owner);
					}
				}
			}
		}
		catch
		{
		}
		return list;
	}

	private void TentarNavegar()
	{
		List<object> list = new List<object>();
		try
		{
			Button val = null;
			int num = 0;
			Button[] array = Recursos<Button>();
			foreach (Button b in array)
			{
				if ((Object)(object)b == (Object)null)
				{
					continue;
				}
				if (((Component)b).gameObject.activeInHierarchy)
				{
					num++;
				}
				if (!((Object)(object)val != (Object)null))
				{
					string text = Seguro(delegate
					{
						TMP_Text componentInChildren = ((Component)b).GetComponentInChildren<TMP_Text>();
						return (!((Object)(object)componentInChildren != (Object)null)) ? null : componentInChildren.text;
					}) as string;
					if (!string.IsNullOrEmpty(text) && text.IndexOf("Skills", StringComparison.OrdinalIgnoreCase) >= 0 && ((Component)b).gameObject.activeInHierarchy)
					{
						val = b;
					}
				}
			}
			list.Add(Json.Campos("estagio", "procurar", "botoes_ativos", num, "achou_skills", (Object)(object)val != (Object)null));
			if ((Object)(object)val != (Object)null)
			{
				((UnityEvent)val.onClick).Invoke();
				list.Add(Json.Campos("estagio", "clique_invocado", "objeto", ((Object)((Component)val).gameObject).name));
			}
		}
		catch (Exception ex)
		{
			list.Add(Json.Campos("estagio", "falha", "erro", ex.GetType().Name));
		}
		_passos["navegacao"] = list;
	}

	private void DemostrarIdaEVolta()
	{
		Dictionary<string, object> dictionary = new Dictionary<string, object>();
		string text = (string)(dictionary["marcador"] = (string.IsNullOrEmpty(_marcador.Value) ? ("AUT4-IDA-E-VOLTA-" + _sessao) : _marcador.Value));
		dictionary["via"] = "Tooltip.ShowTooltip(marcador) + releitura de Tooltip.Title (LEITURA ida-e-volta)";
		object obj2 = TooltipVivo();
		dictionary["tooltip_encontrado"] = obj2 != null;
		try
		{
			dictionary["chamou"] = ChamarShowTooltip(obj2, text, text + "-CORPO");
			object obj3 = ((obj2 == null) ? null : Membro(obj2, "Title"));
			TMP_Text val = (TMP_Text)((obj3 is TMP_Text) ? obj3 : null);
			string text2 = (((Object)(object)val == (Object)null) ? null : val.text);
			string text3 = (((Object)(object)val == (Object)null) ? null : val.GetParsedText());
			dictionary["titulo_lido"] = text2;
			dictionary["titulo_renderizado_lido"] = text3;
			bool flag = string.Equals(text2, text) || string.Equals(text3, text);
			dictionary["conferiu"] = flag;
			Marco("AUT4 PROBE: ida-e-volta " + (flag ? "CONFERIU" : "NAO conferiu") + " (marcador " + text + ")");
		}
		catch (Exception ex)
		{
			dictionary["erro"] = ex.GetType().Name + ": " + ex.Message;
			dictionary["conferiu"] = false;
		}
		_res["ida_e_volta"] = dictionary;
	}

	private bool ChamarShowTooltip(object tooltip, string titulo, string corpo)
	{
		//IL_009b: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c3: Unknown result type (might be due to invalid IL or missing references)
		if (tooltip == null)
		{
			return false;
		}
		MethodInfo methodInfo = tooltip.GetType().GetMethods(BindingFlags.Instance | BindingFlags.Public).FirstOrDefault((MethodInfo x) => x.Name == "ShowTooltip" && x.GetParameters().Length >= 6);
		if (methodInfo == null)
		{
			return false;
		}
		ParameterInfo[] parameters = methodInfo.GetParameters();
		object[] array = new object[parameters.Length];
		for (int i = 0; i < parameters.Length; i++)
		{
			array[i] = Type.Missing;
		}
		array[0] = titulo;
		array[1] = "";
		array[2] = null;
		array[3] = corpo;
		array[4] = null;
		if (parameters[5].ParameterType == typeof(Color))
		{
			array[5] = Color.white;
		}
		else if (parameters[5].ParameterType == typeof(Color?))
		{
			array[5] = Color.white;
		}
		methodInfo.Invoke(tooltip, array);
		return true;
	}

	private void PedirPrint(string nome)
	{
		string text = Path.Combine(_dir, nome + ".png").Replace('\\', '/');
		_arquivosDePrint.Add(text);
		_printAtual = text;
		try
		{
			ScreenCapture.CaptureScreenshot(text);
			Marco("AUT4 PROBE: print (ScreenCapture) -> " + text);
		}
		catch (Exception ex)
		{
			_passos["print_" + nome] = "erro: " + ex.GetType().Name + ": " + ex.Message;
		}
	}

	private bool PrintPronto()
	{
		try
		{
			return File.Exists(_printAtual);
		}
		catch
		{
			return false;
		}
	}

	private void FecharPrint(string nome)
	{
		bool flag = false;
		object obj = null;
		try
		{
			flag = File.Exists(_printAtual);
			if (flag)
			{
				obj = new FileInfo(_printAtual).Length;
			}
		}
		catch
		{
		}
		_passos["print_" + nome] = Json.Campos("arquivo", _printAtual, "existe", flag, "bytes", obj);
	}

	private Dictionary<string, object> Manifest()
	{
		List<object> list = new List<object>();
		foreach (string item in _arquivosDePrint.Concat(new string[1] { CaminhoJson() }))
		{
			Dictionary<string, object> dictionary = new Dictionary<string, object> { ["arquivo"] = Path.GetFileName(item) };
			try
			{
				dictionary["bytes"] = new FileInfo(item).Length;
				dictionary["sha256"] = Sha256(item);
			}
			catch (Exception ex)
			{
				dictionary["erro"] = ex.GetType().Name;
			}
			list.Add(dictionary);
		}
		return Json.Campos("esquema", "AUT-4/1", "total", list.Count, "artefatos", list);
	}

	private Dictionary<string, object> Rollback()
	{
		return Json.Campos("nota", "Rollback EXATO do que a RODADA cria. O orquestrador compara antes/depois e restaura; o .cfg nasce sozinho na 1a execucao e TEM de ser removido se nao existia.", "perfil", _perfilDir.Value, "probe_dir_perfil", string.IsNullOrEmpty(_perfilDir.Value) ? null : Path.Combine(_perfilDir.Value, "BepInEx", "plugins", "AUT4Probe"), "cfg_probe", string.IsNullOrEmpty(_perfilDir.Value) ? null : Path.Combine(_perfilDir.Value, "BepInEx", "config", "com.gumatos.aut4probe.cfg"), "arquivos_criados_pela_rodada", new List<object>(_arquivosDePrint) { CaminhoJson() }, "acao", Json.Campos("probe_dir", "REMOVER a pasta se nao existia antes", "cfg", "REMOVER se nao existia; RESTAURAR se existia", "log", "o LogOutput.log e truncado a cada boot: ARQUIVAR antes de lancar"));
	}

	private string CaminhoJson()
	{
		return Path.Combine(_dir, "aut4probe.json").Replace('\\', '/');
	}

	private void Escrever()
	{
		try
		{
			string text = CaminhoJson();
			string text2 = text + ".tmp";
			File.WriteAllText(text2, Json.Serialize(_res), new UTF8Encoding(encoderShouldEmitUTF8Identifier: false));
			if (File.Exists(text))
			{
				File.Delete(text);
			}
			File.Move(text2, text);
		}
		catch (Exception ex)
		{
			try
			{
				((BaseUnityPlugin)this).Logger.LogError((object)("AUT4 PROBE: gravar json: " + ex.GetType().Name + ": " + ex.Message));
			}
			catch
			{
			}
		}
	}

	private void Marco(string linha)
	{
		_marcos.Add(DateTime.Now.ToString("HH:mm:ss", CultureInfo.InvariantCulture) + " " + linha);
		((BaseUnityPlugin)this).Logger.LogInfo((object)linha);
	}

	private static string Sha256(string caminho)
	{
		using SHA256 sHA = SHA256.Create();
		using FileStream inputStream = File.OpenRead(caminho);
		byte[] array = sHA.ComputeHash(inputStream);
		StringBuilder stringBuilder = new StringBuilder();
		byte[] array2 = array;
		foreach (byte b in array2)
		{
			stringBuilder.Append(b.ToString("x2"));
		}
		return stringBuilder.ToString();
	}

	private static Type Tipo(string nome)
	{
		Assembly[] assemblies = AppDomain.CurrentDomain.GetAssemblies();
		foreach (Assembly assembly in assemblies)
		{
			try
			{
				Type type = assembly.GetType(nome, throwOnError: false);
				if (type != null)
				{
					return type;
				}
			}
			catch
			{
			}
		}
		return null;
	}

	private static object Estatico(Type t, string membro)
	{
		try
		{
			PropertyInfo property = t.GetProperty(membro, BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
			if (property != null)
			{
				return property.GetValue(null);
			}
			FieldInfo field = t.GetField(membro, BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
			if (field != null)
			{
				return field.GetValue(null);
			}
		}
		catch
		{
		}
		return null;
	}

	private static object Membro(object obj, string membro)
	{
		if (obj == null)
		{
			return null;
		}
		try
		{
			Type type = obj.GetType();
			PropertyInfo property = type.GetProperty(membro, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
			if (property != null && property.CanRead)
			{
				return property.GetValue(obj);
			}
			FieldInfo field = type.GetField(membro, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
			if (field != null)
			{
				return field.GetValue(obj);
			}
		}
		catch
		{
		}
		return null;
	}

	private static T[] Recursos<T>() where T : Object
	{
		try
		{
			return Resources.FindObjectsOfTypeAll<T>();
		}
		catch
		{
			return new T[0];
		}
	}

	private static string Nome(Shader s)
	{
		if (!((Object)(object)s == (Object)null))
		{
			return ((Object)s).name;
		}
		return null;
	}

	private static string Trunc(string s, int max)
	{
		if (s == null)
		{
			return null;
		}
		s = s.Replace("\r", "\\r").Replace("\n", "\\n");
		if (s.Length > max)
		{
			return s.Substring(0, max) + "...(truncado em " + max + ")";
		}
		return s;
	}

	private static string Caminho(Transform t)
	{
		try
		{
			List<string> list = new List<string>();
			Transform val = t;
			while ((Object)(object)val != (Object)null && list.Count < 12)
			{
				list.Add(((Object)val).name);
				val = val.parent;
			}
			list.Reverse();
			return string.Join("/", list.ToArray());
		}
		catch
		{
			return null;
		}
	}

	private static Dictionary<string, object> Geometria(TMP_Text t)
	{
		//IL_0049: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_0055: Unknown result type (might be due to invalid IL or missing references)
		//IL_0141: Unknown result type (might be due to invalid IL or missing references)
		//IL_0146: Unknown result type (might be due to invalid IL or missing references)
		//IL_0165: Unknown result type (might be due to invalid IL or missing references)
		//IL_016a: Unknown result type (might be due to invalid IL or missing references)
		//IL_018f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0067: Unknown result type (might be due to invalid IL or missing references)
		//IL_005f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0079: Unknown result type (might be due to invalid IL or missing references)
		//IL_0071: Unknown result type (might be due to invalid IL or missing references)
		//IL_008d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Unknown result type (might be due to invalid IL or missing references)
		//IL_0098: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			RectTransform rectTransform = t.rectTransform;
			if ((Object)(object)rectTransform == (Object)null)
			{
				return null;
			}
			Vector3[] array = (Vector3[])(object)new Vector3[4];
			rectTransform.GetWorldCorners(array);
			float num = float.MaxValue;
			float num2 = float.MaxValue;
			float num3 = float.MinValue;
			float num4 = float.MinValue;
			for (int i = 0; i < 4; i++)
			{
				Vector2 val = RectTransformUtility.WorldToScreenPoint((Camera)null, array[i]);
				if (val.x < num)
				{
					num = val.x;
				}
				if (val.y < num2)
				{
					num2 = val.y;
				}
				if (val.x > num3)
				{
					num3 = val.x;
				}
				if (val.y > num4)
				{
					num4 = val.y;
				}
			}
			object[] obj = new object[8]
			{
				"caixa_na_tela_px",
				Json.Campos("x", Arred(num), "y", Arred(num2), "largura", Arred(num3 - num), "altura", Arred(num4 - num2)),
				"tamanho_do_rect_px",
				null,
				null,
				null,
				null,
				null
			};
			object[] obj2 = new object[4] { "largura", null, null, null };
			Rect rect = rectTransform.rect;
			obj2[1] = Arred(((Rect)(ref rect)).width);
			obj2[2] = "altura";
			rect = rectTransform.rect;
			obj2[3] = Arred(((Rect)(ref rect)).height);
			obj[3] = Json.Campos(obj2);
			obj[4] = "escala";
			obj[5] = Arred(((Transform)rectTransform).lossyScale.x);
			obj[6] = "tela";
			obj[7] = Screen.width + "x" + Screen.height;
			return Json.Campos(obj);
		}
		catch
		{
			return null;
		}
	}

	private static string CorDe(Color c)
	{
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		//IL_0022: Unknown result type (might be due to invalid IL or missing references)
		//IL_0040: Unknown result type (might be due to invalid IL or missing references)
		//IL_005e: Unknown result type (might be due to invalid IL or missing references)
		//IL_007d: Unknown result type (might be due to invalid IL or missing references)
		return "#" + ColorUtility.ToHtmlStringRGBA(c) + " (r=" + Arred(c.r) + " g=" + Arred(c.g) + " b=" + Arred(c.b) + " a=" + Arred(c.a) + ")";
	}

	private static string CorDoMaterial(Material m, string prop)
	{
		//IL_0014: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			return ((Object)(object)m == (Object)null || !m.HasProperty(prop)) ? null : CorDe(m.GetColor(prop));
		}
		catch
		{
			return null;
		}
	}

	private static float Arred(float v)
	{
		return (float)Math.Round(v, 3);
	}

	private static Dictionary<string, object> Aplicacao()
	{
		//IL_0006: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0098: Unknown result type (might be due to invalid IL or missing references)
		//IL_009d: Unknown result type (might be due to invalid IL or missing references)
		string text = "";
		try
		{
			Scene activeScene = SceneManager.GetActiveScene();
			text = ((Scene)(ref activeScene)).name;
		}
		catch
		{
		}
		object[] obj2 = new object[18]
		{
			"produto",
			Application.productName,
			"versao_do_jogo",
			Application.version,
			"unity",
			Application.unityVersion,
			"cena_ativa",
			text,
			"resolucao",
			Screen.width + "x" + Screen.height,
			"plataforma",
			null,
			null,
			null,
			null,
			null,
			null,
			null
		};
		RuntimePlatform platform = Application.platform;
		obj2[11] = ((object)(RuntimePlatform)(ref platform)).ToString();
		obj2[12] = "roteiro_frame";
		obj2[13] = Time.frameCount;
		obj2[14] = "tempo_de_escala_timeScale";
		obj2[15] = Time.timeScale;
		obj2[16] = "hora_local";
		obj2[17] = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture);
		return Json.Campos(obj2);
	}

	private static object Seguro(Func<object> f)
	{
		try
		{
			return f();
		}
		catch
		{
			return null;
		}
	}

	private static bool SeguroBool(Func<bool> f)
	{
		try
		{
			return f();
		}
		catch
		{
			return false;
		}
	}
}
You are not using the latest version of the tool, please update.
Latest version is '11.1.0.9782' (yours is '8.2.0.7535-95108c96')
