"""Harness C# OFFLINE: executa corpos reais do probe com dependencias doubles.
Nao instala probe, nao inicia jogo e nao constitui prova runtime.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile


ASSINATURAS = (
    'private void IniciarSnapshotDoModal()',
    'private Dictionary<string, object> SnapshotDoPersonagem()',
    'private object PersonagemDaSessao()',
    'private void AtualizarGuardasDepois()',
    'private static string NomeDoObjeto(object o)',
    'private static Type Tipo(string nome)',
    'private static object Estatico(Type t, string membro)',
    'private static object Membro(object obj, string membro)',
)

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


def executar(fonte, corpo_do_metodo, avaliador, identidade, observacao):
    metodos = []
    for sig in ASSINATURAS:
        body = corpo_do_metodo(fonte, sig)
        assert body, 'probe sem metodo real: ' + sig
        metodos.append(sig + '\n' + body)
    # Nao basta o helper funcionar se a maquina de estados deixou de chama-lo.
    passo = corpo_do_metodo(fonte, 'private void Passo()')
    assert 'IniciarSnapshotDoModal();' in passo, 'Passo nao captura o alvo do modal'
    with tempfile.TemporaryDirectory(prefix='aut5-modal-') as tmp:
        h = Path(tmp)
        (h / 'harness.csproj').write_text(
            '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
            '<TargetFramework>net6.0</TargetFramework><OutputType>Exe</OutputType>'
            '<LangVersion>10</LangVersion></PropertyGroup></Project>', encoding='utf-8')
        (h / 'Program.cs').write_text(STUBS + '\n'.join(metodos) + MAIN, encoding='utf-8')
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
