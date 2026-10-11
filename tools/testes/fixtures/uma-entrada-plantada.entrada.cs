// FIXTURE PLANTADA (tools/testes/fixtures/uma-entrada-plantada.entrada.cs)
//
// NAO e codigo do mod. E um LocalizePatch.cs FALSO, com os DOIS defeitos da familia
// UMA ENTRADA POR TEXTO plantados de proposito, para os testes MORDEREM as ferramentas
// com dado plantado (docs/PLANO-DE-TESTES.md: "todo teste tem de ser MOSTRADO REPROVANDO"):
//
//   (a) chave repetida DENTRO da mesma tabela -> em C# e ArgumentException no construtor
//       estatico -> TypeInitializationException -> o LocalizePatch INTEIRO nao carrega
//       (o incidente de 29/09; tools/check_dupes.py);
//   (b) a MESMA chave em TextFixes e TextAppends -> o lookup e if/else if, a entrada de
//       TextAppends NUNCA roda (defeito objetivo do BUG-32; tools/check_chave_compartilhada.py
//       --estrito TRAVA).
//
// O teste `t_bt_uma_entrada_por_texto.py` exige que as DUAS ferramentas vejam (a) e (b) AQUI
// e nao vejam nada disso no LocalizePatch.cs de verdade.
class FontePlantada
{
    static readonly Dictionary<string, string> TextFixes = new Dictionary<string, string>
    {
        { "chave repetida no mesmo texto", "primeiro valor" },
        { "chave repetida no mesmo texto", "segundo valor" },
        { "chave nas duas tabelas", "correcao de TextFixes" },
    };

    static readonly Dictionary<string, string> TextAppends = new Dictionary<string, string>
    {
        { "chave nas duas tabelas", "nota de TextAppends (nunca roda: if/else if)" },
    };
}
