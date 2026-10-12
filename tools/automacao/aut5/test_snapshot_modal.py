"""Harness C# OFFLINE do modal: PREFLIGHT ESTATICO sempre; execucao opt-in.

ORG-AUT5-FIX (t_2d9f22b1) — o instrumento congelado NAO se ajusta a harness
defasado. Duas premissas do harness antigo eram falsas:
  * exigia a visibilidade LITERAL `private` em `Tipo`, e a fonte congelada declara
    `internal static Type Tipo(string nome)` (AUT4ProbePlugin.cs:1879);
  * exigia `IniciarSnapshotDoModal();` INLINE no corpo de `Passo`, quando a cadeia
    real e `Passo:469 -> PassoLeitura:507 -> IniciarSnapshotDoModal:513`.
Agora o preflight aceita a visibilidade REAL (registrando-a) e percorre a CADEIA DE
CHAMADAS real, com controles negativos que so mutam COPIAS em memoria do fonte.
Nao instala probe, nao inicia jogo e nao constitui prova runtime.
A execucao (`dotnet run`) exige AUT5_AUTORIZA_COMPILACAO=1: sem isso o harness nao
compila, nao spawna processo e o grupo sai NAO_EXERCITADO.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile

# Assinaturas SEM visibilidade: a visibilidade real e resolvida e REGISTRADA.
ASSINATURAS = (
    'void IniciarSnapshotDoModal()',
    'Dictionary<string, object> SnapshotDoPersonagem()',
    'object PersonagemDaSessao()',
    'void AtualizarGuardasDepois()',
    'static string NomeDoObjeto(object o)',
    'static Type Tipo(string nome)',
    'static object Estatico(Type t, string membro)',
    'static object Membro(object obj, string membro)',
)

# Visibilidade aceita para os membros internos do probe (o reuso documentado em
# AUT4ProbePlugin.cs:715-717 e `internal`; `private` vale para um helper puro).
# `public` NAO vale: a superficie publica do plugin nao expoe leitura de objeto.
VISIBILIDADE_INTERNA_OK = ('internal', 'private')

# Controles negativos do PROPRIO preflight (defeito 3): cada um e uma SEQUENCIA de
# trocas aplicada a uma COPIA em memoria do fonte pelo chamador; o probe do
# repositorio nunca e tocado.
CONTROLES_NEGATIVOS = (
    ('visibilidade-publica',
     (('internal static Type Tipo(string nome)', 'public static Type Tipo(string nome)'),),
     'membro interno promovido a publico'),
    ('tipo-renomeado',
     (('internal static Type Tipo(string nome)', 'internal static Type TipoX(string nome)'),),
     'assinatura real ausente'),
    ('dispatch-do-driver-removido',
     (('case F_LEITURA: PassoLeitura(); break;', 'case F_LEITURA: break;'),),
     'Passo() deixou de despachar para PassoLeitura()'),
    ('captura-removida',
     (('            IniciarSnapshotDoModal();\n', ''),),
     'a captura do modal saiu de PassoLeitura()'),
    ('captura-depois-da-coleta',
     (('            IniciarSnapshotDoModal();\n', ''),
      ('            Evento("coleta_concluida");',
       '            IniciarSnapshotDoModal();\n            Evento("coleta_concluida");')),
     'a captura passou a ocorrer DEPOIS da coleta'),
)

PRE_REQUISITO = ('compilacao/execucao do harness C# (`dotnet run`): exige autorizacao '
                 'de compilacao nesta rodada (AUT5_AUTORIZA_COMPILACAO=1)')

# Trava de spawn: contador de subprocessos deste modulo (0 sem autorizacao).
SPAWNS = 0

STUBS = '''using System; using System.Collections; using System.Collections.Generic;
using System.Reflection; using System.Globalization;
namespace UnityEngine { public class Object { public string name; } }
public class Skill { public string SkillName; }
public class Character { public string CharacterName; public List<Skill> SkillsFromPoints = new(); public int UnspentSkillPoints; }
public class GameLogic { public static GameLogic instance=new(); public Character CurrentlySelectedCharacter; }
namespace RoguelikeSkillTreeVisualizer {
 internal static class ReadOnlySession {
  internal static bool Active {get;set;}
  internal static Character Target {get;set;}
 }
}
public class Json { public static Dictionary<string,object> Campos(params object[] pairs) {
 var d=new Dictionary<string,object>(); for(int i=0;i<pairs.Length;i+=2)d[(string)pairs[i]]=pairs[i+1]; return d;
} }
public class Probe {
 private object _personagemDoModal;
 private Dictionary<string,object> _snapshotAntes, _snapshotDepois;
 private string _tooltipPaiDepois;
 private object _tooltipIndiceDepois, _janelasDuplicadas;
 private List<object> _observacoes=new();
 private object TooltipVivo() {return null;}
 private string TooltipPai(object o) {return null;}
 private object TooltipIndice(object o) {return null;}
 private object JanelasDuplicadas() {return 0;}
'''
MAIN = '''
 public static void Main() {
 var a=new Character {CharacterName="MODAL_A", UnspentSkillPoints=3,
                     SkillsFromPoints=new(){new Skill{SkillName="A"}}};
 var b=new Character {CharacterName="SELECTED_B", UnspentSkillPoints=7,
                     SkillsFromPoints=new(){new Skill{SkillName="B"}}};
 foreach(var label in new[]{"selected_null", "selected_other", "selected_same"}) {
  a.UnspentSkillPoints=3;
  RoguelikeSkillTreeVisualizer.ReadOnlySession.Active=true;
  RoguelikeSkillTreeVisualizer.ReadOnlySession.Target=a;
  GameLogic.instance.CurrentlySelectedCharacter=label=="selected_null"?null:label=="selected_other"?b:a;
  var p=new Probe(); p.IniciarSnapshotDoModal();
  var obs=new Dictionary<string,object>{{"snapshot_depois",p._snapshotDepois}};
  p._observacoes.Add(obs);
  a.UnspentSkillPoints=1;
  // Fechamento limpa sessao, e outro modal pode abrir antes do ultimo quadro.
  RoguelikeSkillTreeVisualizer.ReadOnlySession.Active=false;
  RoguelikeSkillTreeVisualizer.ReadOnlySession.Target=null;
  GameLogic.instance.CurrentlySelectedCharacter=b;
  p.AtualizarGuardasDepois();
  var afterClose=new Dictionary<string,object>(p._snapshotDepois);
  RoguelikeSkillTreeVisualizer.ReadOnlySession.Active=true;
  RoguelikeSkillTreeVisualizer.ReadOnlySession.Target=b;
  p.AtualizarGuardasDepois();
  Console.WriteLine(System.Text.Json.JsonSerializer.Serialize(new {
   caso=label, antes=p._snapshotAntes, depois=obs["snapshot_depois"], depois_fechar=afterClose
  }));
 }
 foreach(var label in new[]{"inactive_session", "null_target"}) {
  RoguelikeSkillTreeVisualizer.ReadOnlySession.Active=label=="null_target";
  RoguelikeSkillTreeVisualizer.ReadOnlySession.Target=label=="null_target"?null:a;
  GameLogic.instance.CurrentlySelectedCharacter=b;
  var p=new Probe(); p.IniciarSnapshotDoModal(); p.AtualizarGuardasDepois();
  Console.WriteLine(System.Text.Json.JsonSerializer.Serialize(new {
   caso=label, antes=p._snapshotAntes, depois=p._snapshotDepois
  }));
 }
 }
}
'''


class NaoAutorizadoCompilar(RuntimeError):
    """Tentativa de executar o harness C# sem autorizacao de compilacao."""


def preflight(fonte, extrair, metodos_do_fonte, cadeia):
    """Contrato ESTATICO do harness: (problemas, info). Nao compila e nao spawna.

    `extrair(fonte, assinatura)` devolve (linha_declarada, visibilidade, corpo);
    `cadeia(fonte, entrada, alvo)` devolve (caminho, motivo).
    """
    global SPAWNS
    problemas = []
    visibilidades = {}
    for sig in ASSINATURAS:
        linha, vis, corpo = extrair(fonte, sig)
        if not corpo:
            problemas.append('probe sem metodo real: ' + sig)
            continue
        if vis not in VISIBILIDADE_INTERNA_OK:
            problemas.append('probe: %s com visibilidade %r fora de %s'
                             % (sig, vis, VISIBILIDADE_INTERNA_OK))
        visibilidades[sig] = vis
    # a captura tem de estar ALCANCAVEL a partir do driver, pela cadeia real, na
    # FASE DE LEITURA (o snapshot "antes" e tirado ali, nao numa fase qualquer)
    esperado_cadeia = ['Passo', 'PassoLeitura', 'IniciarSnapshotDoModal']
    caminho, motivo = cadeia(fonte, 'Passo', 'IniciarSnapshotDoModal')
    if caminho != esperado_cadeia:
        problemas.append('Passo() nao alcanca a captura do modal pela cadeia real %s '
                         '(veio %s; %s)' % (esperado_cadeia, caminho, motivo or ''))
    caminho_leitura, motivo_leitura = cadeia(fonte, 'Passo', 'Leitura')
    if caminho_leitura is None:
        problemas.append('Passo() nao alcanca Leitura(): %s' % motivo_leitura)
    # guarda de ORDEM: o "antes" tem de ser capturado ANTES da coleta (senao o par
    # antes/depois da leitura deixa de ser real)
    _linha, _vis, corpo_leitura = extrair(fonte, 'void PassoLeitura()')
    if not corpo_leitura:
        problemas.append('probe sem metodo real: void PassoLeitura()')
    else:
        i_cap = corpo_leitura.find('IniciarSnapshotDoModal(')
        i_col = corpo_leitura.find('ColetarObservacoes(')
        if i_cap < 0 or i_col < 0 or i_cap > i_col:
            problemas.append('PassoLeitura(): a captura do modal nao precede a coleta '
                             '(captura em %s, coleta em %s)' % (i_cap, i_col))
    info = {'visibilidades': visibilidades, 'cadeia_captura': caminho,
            'cadeia_leitura': caminho_leitura, 'spawns': SPAWNS,
            'visibilidade_ok': list(VISIBILIDADE_INTERNA_OK),
            'metodos_conferidos': len(ASSINATURAS)}
    return problemas, info


def executar(fonte, extrair, corpo_do_metodo, metodos_do_fonte, cadeia, avaliador,
             identidade, observacao):
    """Roda o C# real com o preflight verde. EXIGE autorizacao explicita.

    Sem AUT5_AUTORIZA_COMPILACAO=1 nao compila e nao spawna: levanta
    NaoAutorizadoCompilar com o pre-requisito registrado.
    """
    global SPAWNS
    if os.environ.get('AUT5_AUTORIZA_COMPILACAO') != '1':
        raise NaoAutorizadoCompilar(PRE_REQUISITO)
    problemas, _info = preflight(fonte, extrair, metodos_do_fonte, cadeia)
    assert not problemas, 'preflight do harness: ' + '; '.join(problemas)
    metodos = []
    for sig in ASSINATURAS:
        linha, vis, corpo = extrair(fonte, sig)
        assert corpo, 'probe sem metodo real: ' + sig
        metodos.append('%s %s\n%s' % (vis, linha, corpo))
    with tempfile.TemporaryDirectory(prefix='aut5-modal-') as tmp:
        h = Path(tmp)
        (h / 'harness.csproj').write_text(
            '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
            '<TargetFramework>net6.0</TargetFramework><OutputType>Exe</OutputType>'
            '<LangVersion>10</LangVersion></PropertyGroup></Project>', encoding='utf-8')
        (h / 'Program.cs').write_text(STUBS + '\n'.join(metodos) + MAIN, encoding='utf-8')
        SPAWNS += 1
        cp = subprocess.run(['dotnet', 'run', '--project', str(h / 'harness.csproj')],
                            capture_output=True, text=True, encoding='utf-8', errors='replace',
                            timeout=120)
        assert cp.returncode == 0, 'harness C# falhou: ' + cp.stdout + cp.stderr
        linhas = [json.loads(l) for l in cp.stdout.splitlines() if l.startswith('{')]
    assert len(linhas) == 5, 'harness nao executou os cinco controles'
    for linha in linhas:
        antes, depois = linha['antes'], linha['depois']
        if linha['caso'].startswith('selected_'):
            assert antes['personagem'] == depois['personagem'] == 'MODAL_A', linha
            assert antes['skills'] == depois['skills'] == ['A'], linha
            assert antes['pontos'] == 3 and depois['pontos'] == 1, linha
            assert linha['depois_fechar'] == depois, 'alvo trocou depois de fechar: ' + str(linha)
            esperado = 'REPROVADO'
        else:
            assert all(s[k] is None for s in (antes, depois)
                       for k in ('personagem', 'skills', 'pontos')), linha
            esperado = 'NAO_EXERCITADO'
        obs = observacao({'snapshot_antes': antes, 'snapshot_depois': depois})
        estado = next(c['estado'] for c in avaliador.avaliar([obs], identidade)
                      if c['id'] == 'RSTV-6-readonly-skills-pontos')
        assert estado == esperado, (linha, estado, esperado)
        print('HARNESS|%s|%s|OFFLINE' % (linha['caso'], estado))
    return linhas
