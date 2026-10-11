#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REFLEXAO x CAST no dump (TST-5) - o defeito que apagava dado COM O TIPO junto.

O QUE ESTE TESTE PRENDE (e por que existe)
------------------------------------------
`ActionStatusInfo.Effects` e `ActionInfo.Effects` sao `IEffectInfo[]` - uma interface
VAZIA (sem membros). O dump ANTIGO fazia `e as GeneralEffect` para ler o campo `Action`;
em todo elemento cujo tipo concreto NAO fosse `GeneralEffect` o cast devolvia `null` e o
dado **desaparecia do dump, com o tipo junto** (nao dava nem para saber que faltava). A
RV-8b-0g consertou trocando o cast por REFLEXAO (`EfeitosInfo.Descreve`): percorre o
`System.Array`, publica `indice:Tipo{campo=valor}` e o NOME DO TIPO CONCRETO de cada
elemento. O proposito declarado no fonte: *um terceiro implementador de `IEffectInfo`
sai no dump SEM RECOMPILAR*.

ESTE TESTE EXIGE
----------------
  1. O MODELO (o que roda sem o jogo): com as DUAS implementacoes reais e uma TERCEIRA
     SIMULADA, a reflexao publica os TRES tipos; o cast so enxerga `GeneralEffect` e
     perde o resto EM SILENCIO. O terceiro tipo e a prova de que a reflexao escala.
  2. O FONTE VIVO (`EfeitosInfo.cs`): `Descreve`/`DescreveCore`/`Um` leem por reflexao
     (`GetType`/`GetFields`/`GetValue`), publicam `t.Name` e NAO fazem cast na interface;
     o contador `!(o is GeneralEffect)` (a medida do defeito) continua la.
  3. O patch de status publica o `efTipos` pelo caminho de REFLEXAO.
  4. A isca: cada defeito plantado numa copia em memoria faz a checagem REPROVAR.

PROVA DE FOGO
-------------
Isca embutida por defeito (em memoria) + a prova FISICA no fonte real (o cast plantado
no `EfeitosInfo.cs`, o teste rodado, o arquivo restaurado byte a byte com sha256) em
`tools/testes/debugger-prova-de-fogo.log`.

O QUE ESTE TESTE NAO PROVA
--------------------------
Nao executa o C# do mod. O modelo Python espelha a conta; a ligacao com o motor e a
ESTRUTURA do fonte vivo (recorte por casamento de chaves, ancorado em identificador).
"""
import arcabouco as arc
import regras_debugger as rd

META = {
    "nome": "debugger-reflexao-cast",
    "categoria": "pura",
    "requer": [],
    "descricao": ("um tipo concreto NOVO de IEffectInfo sai no dump por REFLEXAO (sem "
                  "recompilar) e o cast `as GeneralEffect` perde o dado em silencio; o "
                  "fonte vivo le por reflexao e publica o Nome do tipo (isca embutida)"),
}


def _matriz():
    """As duas implementacoes REAIS + a TERCEIRA simulada (a que o cast nao ve)."""
    return [
        rd.GeneralEffect(action="10 * Level"),
        rd.CharacterVariableEffectInfo(effect_target="Target",
                                       character_variable_attribute="DamageMod",
                                       amount="Mathf.Round(20 * (1 + (bonus / 100)))"),
        rd.TerceiroEffectInfo(kind="Novo", value="3"),
    ]


def corpo():
    # ------------------------------------------------ 1. o MODELO (sem o jogo)
    arr = _matriz()
    reflexao = rd.descreve("reflexao", arr)
    cast = rd.descreve("cast", arr)

    for tipo in ("GeneralEffect", "CharacterVariableEffectInfo", "TerceiroEffectInfo"):
        arc.exigir(tipo in reflexao,
                   "a REFLEXAO nao publicou o tipo concreto %r - um tipo novo sumiria do "
                   "dump: %r" % (tipo, reflexao))
    arc.exigir("CharacterVariableEffectInfo" not in cast and "TerceiroEffectInfo" not in cast,
               "o cast NAO pode enxergar os tipos de outra implementacao: %r" % cast)
    arc.igual(cast.count("GeneralEffect"), 1,
              "o cast antigo so devolve o unico GeneralEffect (o defeito)")
    arc.igual(reflexao.count(":"), 3,
              "a reflexao tem de publicar os TRES elementos, um por indice: %r" % reflexao)
    arc.exigir("Kind=Novo" in reflexao and "Value=3" in reflexao,
               "a reflexao nao publicou os CAMPOS do terceiro tipo: %r" % reflexao)

    # Com SO as duas implementacoes conhecidas, a reflexao ja cobre as duas (o caso
    # real da montagem); o terceiro prova que NAO ha lista fechada de tipos.
    dois = rd.descreve("reflexao", arr[:2])
    arc.exigir("CharacterVariableEffectInfo" in dois and "TerceiroEffectInfo" not in dois,
               "com dois elementos a reflexao cobriu o que existe: %r" % dois)

    # ------------------------------------------------ 2. o FONTE VIVO
    cod_efeitos = rd.le_fonte("efeitos")
    cod_status = rd.le_fonte("status")
    falhas = rd.falhas_da_reflexao(cod_efeitos, cod_status)
    arc.exigir(not falhas,
               "o caminho de reflexao do dump regrediu em %d ponto(s):\n  - %s"
               % (len(falhas), "\n  - ".join(falhas)))

    # ------------------------------------------------ 3. as ISCAS embutidas (o fonte MORDE)
    iscas = {}

    # (a) o defeito ORIGINAL: o cast volta para dentro do `Um`.
    alvo = "Type t = o.GetType();\n            string nome = t.Name;"
    if cod_efeitos.count(alvo) == 1:
        iscas["cast-no-Um"] = cod_efeitos.replace(
            alvo, "Type t = o.GetType();\n            string nome = (o as GeneralEffect) != null ? \"GeneralEffect\" : \"?\";")

    # (b) a enumeracao deixa de ser por reflexao.
    alvo = "o = arr.GetValue(i);"
    if cod_efeitos.count(alvo) == 1:
        iscas["sem-GetValue"] = cod_efeitos.replace(alvo, "o = arr.GetValue(0);")

    # (c) o `Um` deixa de publicar o NOME do tipo.
    alvo = "sb.Append(nome).Append('{');"
    if cod_efeitos.count(alvo) == 1:
        iscas["sem-nome-do-tipo"] = cod_efeitos.replace(alvo, "sb.Append(\"Tipo\").Append('{');")

    arc.exigir(set(iscas) >= {"cast-no-Um", "sem-GetValue", "sem-nome-do-tipo"},
               "as ancoras do plantio nao acharam o trecho do `EfeitosInfo.cs`: %s"
               % sorted(iscas))
    for nome in sorted(iscas):
        f = rd.falhas_da_reflexao(iscas[nome], cod_status)
        arc.exigir(f, "o defeito plantado '%s' PASSOU pela checagem (ela nao morde)" % nome)

    # (d) o patch de status deixa de ler o `IEffectInfo[]` por reflexao.
    alvo = "EfeitosInfo.Descreve(s.Effects)"
    arc.exigir(cod_status.count(alvo) == 1, "ancora `Descreve(s.Effects)` nao e unica")
    f_st = rd.falhas_da_reflexao(cod_efeitos, cod_status.replace(alvo, "EfeitosInfo.Descreve(s.AttributeEffects)"))
    arc.exigir(f_st, "trocar o campo do `efTipos` (Effects -> AttributeEffects) NAO mordeu")

    # ------------------------------------------------ 4. o MODELO tambem MORDE
    # Se o modelo usasse o cast, o terceiro tipo sumiria - e o teste acima reprovaria.
    arc.exigir(rd.descreve("cast", arr) != rd.descreve("reflexao", arr),
               "a isca do modelo (cast x reflexao no terceiro tipo) nao morde")

    print("reflexao x cast: reflexao publica os 3 tipos (2 reais + 1 simulado), o cast so 1; "
          "fonte vivo por reflexao; %d isca(s) do fonte reprovam pela razao certa" % len(iscas))


if __name__ == "__main__":
    arc.main(META, corpo)
