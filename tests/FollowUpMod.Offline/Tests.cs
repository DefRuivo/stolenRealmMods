using FollowUpMod;

static void Check(bool ok, string name)
{
    Console.WriteLine((ok ? "PASS " : "FAIL ") + name);
    if (!ok) Environment.ExitCode = 1;
}

// A) Grupo com ancora 15: personagem 1 e promovido ate 15 (14 niveis) e o jogo aceita.
var a = CoopLevelPolicy.DecidePromotion(1, 15, 20);
Check(a.Promote && a.TargetLevel == 15 && a.LevelsToGrant == 14 && !a.CeilingLimited,
    "promove personagem abaixo da ancora ate a ancora");

// B) Personagem 20 com ancora 15: NAO e promovido nem rebaixado; a recusa e a regra do jogo.
var b = CoopLevelPolicy.DecidePromotion(20, 15, 20);
Check(!b.Promote && b.TargetLevel == 20 && b.LevelsToGrant == 0, "acima da ancora nao promove e nunca rebaixa");

// C) Igual a ancora: nada a fazer.
var c = CoopLevelPolicy.DecidePromotion(15, 15, 20);
Check(!c.Promote && c.LevelsToGrant == 0, "nivel igual a ancora nao gera promocao");

// D) Ancora acima do teto do jogo: promove ate o teto e marca ceiling.
var d = CoopLevelPolicy.DecidePromotion(10, 25, 20);
Check(d.Promote && d.TargetLevel == 20 && d.LevelsToGrant == 10 && d.CeilingLimited,
    "ancora acima do teto promove so ate o teto e marca ceiling_limited");

// E) Sem ancora (grupo vazio): nada acontece.
var e = CoopLevelPolicy.DecidePromotion(3, 0, 20);
Check(!e.Promote && e.LevelsToGrant == 0, "sem ancora nao promove");

// F) Entre minimo e ancora: quem manda e o jogo (nao mexemos no nivel).
var f = CoopLevelPolicy.DecidePromotion(11, 10, 20);
Check(!f.Promote && f.TargetLevel == 11, "acima da ancora dentro da tolerancia fica com a regra nativa");

// G) Grupo com varios membros: minimo, maximo e promocao ate a ancora.
var levels = new[] { 15, 18, 22 };
Check(CoopLevelPolicy.GroupMinimum(levels) == 15, "minimo do grupo e o menor nivel");
Check(CoopLevelPolicy.GroupMaximum(levels) == 22, "maximo do grupo e o maior nivel");
var g = CoopLevelPolicy.DecidePromotion(5, 15, 20);
Check(g.Promote && g.TargetLevel == 15 && g.LevelsToGrant == 10, "membro 5 sobe ate a ancora 15");

// H) Lista vazia ou nula nao inventa nivel.
Check(CoopLevelPolicy.GroupMinimum(Array.Empty<int>()) == 0, "grupo vazio devolve minimo 0");
Check(CoopLevelPolicy.GroupMinimum(null!) == 0, "grupo nulo devolve minimo 0");

Console.WriteLine(Environment.ExitCode == 0 ? "ALL PASS" : "HAS FAILURES");
