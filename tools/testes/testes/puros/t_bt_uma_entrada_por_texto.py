#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UMA ENTRADA POR TEXTO (TST-3, cenario 1) - morde o check_dupes e o check_chave_compartilhada.

O QUE ESTE TESTE PRENDE
-----------------------
As tabelas do `LocalizePatch` sao `Dictionary<string,string>`:

  * chave repetida na MESMA tabela -> `Add` estoura `ArgumentException` no construtor estatico
    -> `TypeInitializationException` -> o LocalizePatch INTEIRO nao carrega (o incidente de
    29/09). Quem detecta: `tools/check_dupes.py`.
  * a MESMA chave em `TextFixes` e `TextAppends` -> o lookup e if/else if na mesma chave, entao
    a de `TextAppends` NUNCA roda (a nota some em silencio, sem erro no log). Defeito objetivo
    do BUG-32; `tools/check_chave_compartilhada.py --estrito` TRAVA a release.

A REGRA DO PLANO ("mostre reprovando") e respeitada MORDENDO com dado PLANTADO: a fixture
`uma-entrada-plantada.entrada.cs` carrega os DOIS defeitos, e o teste exige que as ferramentas
os VEJAM la - e nao vejam NADA disso no `LocalizePatch.cs` de verdade. Chamar a ferramenta so
no arquivo limpo nao provaria nada.

A metade que REPROVA (a isca) e `tools/testes/contra-prova/cp_bt_uma_entrada_isca.py`; a
metade que PASSA e `..._ok.py`; quem casa as duas e `t_bt_contra_prova.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "bt-uma-entrada-por-texto",
    "categoria": "pura",
    "requer": [],
    "descricao": "check_dupes morde a chave duplicada plantada e o --estrito trava a chave nas duas tabelas; o LocalizePatch.cs real passa nas duas",
}


def corpo():
    real = R.le_fonte()

    # 0. As tabelas que o teste depende existem (nome trocado aqui quebraria o pin, nao o teste).
    R.pin(real, "private static readonly Dictionary<string, string> TextFixes",
          "a tabela TextFixes tem de estar no LocalizePatch.cs")
    R.pin(real, "private static readonly Dictionary<string, string> TextAppends",
          "a tabela TextAppends tem de estar no LocalizePatch.cs")

    plantado = arc.ler_texto("uma-entrada-plantada", "entrada", "cs")
    caminho_plantado = arc.caminho_fixture("uma-entrada-plantada", "entrada", "cs")

    # 1. MORDER o check_dupes com a chave repetida PLANTADA.
    dup = R.chaves_duplicadas(plantado, "TextFixes")
    arc.igual(dup, {"chave repetida no mesmo texto": 2},
              "o check_dupes tem de VER a chave repetida plantada em TextFixes")

    # 2. MORDER o check_chave_compartilhada (BINARIO, --estrito) com a chave nas DUAS tabelas.
    codigo, saida = R.roda_chave_compartilhada(caminho_plantado)
    arc.igual(codigo, 1, "o --estrito tinha de TRAVAR o fonte plantado (exit 1); saida: %s"
              % saida.strip().splitlines()[-1:])
    arc.exigir("chave nas duas tabelas" in saida,
               "o --estrito tinha de NOMEAR a chave plantada; saida: %s" % saida[-400:])

    # 3. O REAL tem de estar limpo nas DUAS checagens (senao a tabela do mod esta quebrada HOJE).
    arc.igual(R.chaves_duplicadas(real, "TextFixes"), {},
              "ha chave DUPLICADA em TextFixes no LocalizePatch.cs de verdade")
    arc.igual(R.chaves_duplicadas(real, "TextAppends"), {},
              "ha chave DUPLICADA em TextAppends no LocalizePatch.cs de verdade")
    arc.igual(R.chaves_nas_duas_tabelas(real), [],
              "ha chave nas DUAS tabelas no LocalizePatch.cs de verdade")

    codigo_real, saida_real = R.roda_chave_compartilhada(R.LOCALIZE)
    arc.igual(codigo_real, 0, "o LocalizePatch.cs real tinha de PASSAR no --estrito; saida: %s"
              % saida_real.strip().splitlines()[-1:])

    print("check_dupes mordeu a chave repetida plantada; --estrito travou a chave nas duas "
          "tabelas; o LocalizePatch.cs real passa nas duas")


if __name__ == "__main__":
    arc.main(META, corpo)
