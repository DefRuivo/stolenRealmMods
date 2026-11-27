using FollowUpMod;

static void Check(bool ok, string name)
{
    Console.WriteLine((ok ? "PASS " : "FAIL ") + name);
    if (!ok) Environment.ExitCode = 1;
}

// A) Grupo nivel 15: personagem 1 e aceito e sobe ate 15.
var d1 = CoopLevelPolicy.DecideLevelDelta(1, 15, 20);
Check(d1.Accepted && d1.TargetLevel == 15 && d1.LevelsToGrant == 14 && !d1.CeilingLimited,
    "aceita personagem abaixo do grupo e concede 14 niveis");

// B) Personagem 20 em grupo 15: recusado, nunca rebaixado.
var d2 = CoopLevelPolicy.DecideLevelDelta(20, 15, 20);
Check(!d2.Accepted && d2.TargetLevel == 20 && d2.LevelsToGrant == 0,
    "recusa personagem acima do grupo sem rebaixar");

// C) Igual ao minimo: aceito, zero niveis.
var d3 = CoopLevelPolicy.DecideLevelDelta(15, 15, 20);
Check(d3.Accepted && d3.LevelsToGrant == 0, "aceita nivel igual sem conceder nada");

// D) Grupo acima do teto do jogo: promove ate o teto e marca ceiling.
var d4 = CoopLevelPolicy.DecideLevelDelta(10, 25, 20);
Check(d4.Accepted && d4.TargetLevel == 20 && d4.LevelsToGrant == 10 && d4.CeilingLimited,
    "grupo acima do teto promove so ate o teto e marca ceiling_limited");

// E) Sem grupo anterior (minimo 0): aceita, zero niveis.
var d5 = CoopLevelPolicy.DecideLevelDelta(3, 0, 20);
Check(d5.Accepted && d5.LevelsToGrant == 0, "aceita sem concessao quando nao ha grupo anterior");

// F) Grupo com muitos membros: promove ate o menor nivel.
var levels = new[] { 15, 18, 22 };
Check(CoopLevelPolicy.GroupMinimum(levels) == 15, "minimo do grupo e o menor nivel");
Check(CoopLevelPolicy.GroupMaximum(levels) == 22, "maximo do grupo e o maior nivel");
var d6 = CoopLevelPolicy.DecideLevelDelta(5, CoopLevelPolicy.GroupMinimum(levels), 20);
Check(d6.Accepted && d6.TargetLevel == 15 && d6.LevelsToGrant == 10, "membro 5 entra no nivel 15 mesmo com membros 18 e 22");

// G) Lista vazia ou nula nao inventa nivel.
Check(CoopLevelPolicy.GroupMinimum(Array.Empty<int>()) == 0, "grupo vazio devolve minimo 0");
Check(CoopLevelPolicy.GroupMinimum(null!) == 0, "grupo nulo devolve minimo 0");

Console.WriteLine(Environment.ExitCode == 0 ? "ALL PASS" : "HAS FAILURES");
