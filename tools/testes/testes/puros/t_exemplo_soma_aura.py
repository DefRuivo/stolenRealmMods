#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXEMPLO de teste de LOGICA PURA (roda sem o jogo - e o modelo do CI).

O QUE ELE CONFERE
-----------------
A escala das auras de shrine: `Mathf.Round(BASE * (1 + shrineEffectBonus/100))`.
E o mesmo defeito que o dono relatou na familia de shrines: numero somado a mao
em vez de sair do motor.

POR QUE E DE LOGICA PURA
------------------------
Nao toca em tipo do jogo: e uma formula, um arredondamento e uma tabela de
valores. Roda em qualquer lugar (Python puro, sem dotnet, sem lib/) - inclusive
no CI.

COMO ELE NAO SE ENGANARIA SOZINHO
---------------------------------
O valor esperado NAO foi calculado por este teste: vem da fixture
`soma-aura.esperado.json`, GERADA pelo oraculo em C# que usa o mesmo caminho de
conta do motor (float + Math.Round ToEven). Fixture gerada pelo proprio testado
nao prova nada; o par (entrada, esperado) tem procedencia declarada no arquivo e
e regeravel com `dotnet run --project tools/testes/fixtures/geradores/oraculo_soma_aura`.
"""
import arcabouco as arc

META = {
    "nome": "soma-aura",
    "categoria": "pura",
    "requer": [],
    "descricao": "escala de aura de shrine confere com o motor (22 cenarios + auditoria da fixture)",
}


def escala_aura(base, bonus):
    """Mathf.Round(BASE * (1 + bonus/100)) - fator e produto em FLOAT, como o motor."""
    fator = arc.f32(1.0 + arc.f32(arc.f32(bonus) / arc.f32(100.0)))
    produto = arc.f32(arc.f32(base) * fator)
    return int(round(produto))  # round() do Python == Math.Round ToEven


def escala_aura_em_double(base, bonus):
    """A versao "obvia" (double). Serve de controle para provar que a emulacao
    de float32 nao e decoracao - ver a GUARDA no fim do corpo()."""
    return int(round(float(base) * (1.0 + float(bonus) / 100.0)))


def corpo():
    entrada = arc.ler_json("soma-aura", "entrada")
    esperado = arc.ler_json("soma-aura", "esperado")
    por_id = {r["id"]: r["valor"] for r in esperado["resultados"]}

    arc.igual(len(entrada["cenarios"]), len(esperado["resultados"]),
              "quantidade de cenarios na entrada x resultados no esperado")

    # Nenhum resultado do esperado pode ficar sem cenario (sobrar informacao
    # versionada que ninguem confere e a mesma coisa que nao ter o teste).
    ids_da_entrada = {c["id"] for c in entrada["cenarios"]}
    arc.igual(sorted(set(por_id) - ids_da_entrada), [], "ids no esperado sem cenario na entrada")

    for cenario in entrada["cenarios"]:
        arc.exigir(cenario["id"] in por_id, "cenario %r sem resultado esperado" % cenario["id"])
        obtido = escala_aura(cenario["base"], cenario["bonus"])
        arc.igual(obtido, por_id[cenario["id"]],
                  "cenario %s (base=%d bonus=%d) contra o motor"
                  % (cenario["id"], cenario["base"], cenario["bonus"]))

    # A fixture afirma uma auditoria (float x double no dominio alcancavel).
    # Afirmacao de fixture que nao se confere vira folclore: refaz aqui.
    auditoria = entrada["auditoria_float_vs_double"]
    for base in auditoria["bases"]:
        for bonus in auditoria["bonus_alcancaveis"]:
            arc.igual(escala_aura(base, bonus), escala_aura_em_double(base, bonus),
                      "auditoria da fixture: float x double em base=%s bonus=%s" % (base, bonus))

    # GUARDA: emulacao de float32 so vale se ela PUDER discordar do double. Fora
    # do dominio do jogo os dois divergem; se isto deixar de acontecer, a
    # emulacao virou decoracao e a fixture precisa de novo oraculo.
    controles = [(5, -90), (25, 122)]
    divergentes = [(b, bo) for b, bo in controles
                   if escala_aura(b, bo) != escala_aura_em_double(b, bo)]
    arc.exigir(divergentes,
               "a emulacao de float32 nao divergiu de double em NENHUM controle %s - "
               "ela nao esta provando nada" % controles)
    for base, bonus in controles:
        arc.exigir(escala_aura(base, bonus) != escala_aura_em_double(base, bonus),
                   "controle base=%s bonus=%s deixou de divergir" % (base, bonus))


if __name__ == "__main__":
    arc.main(META, corpo)
