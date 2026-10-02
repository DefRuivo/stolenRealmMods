#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FORMATO-9 — a formula da aura lida do asset tem de ser UNICA na janela (nunca a 1a em silencio).

POR QUE ESTE TESTE EXISTE
-------------------------
`tools/gera_shrines_esperado.py: bases_do_asset` lia a BASE das 3 auras sem atributo de personagem
(Dwarven/Decay/Flame) dentro de uma JANELA de bytes de `resources.assets` (RV-19 §8) devolvendo a
PRIMEIRA formula que casava. A FORMATO-7 MEDIU o defeito latente: se o offset documentado sair do
lugar, OUTRA formula da mesma forma cai na janela e a primeira vence EM SILENCIO, com citacao
plausivel — deslocar a janela do `Decay` 1 byte a frente da formula devolve a base do `Dwarven`
(20 `Target`) no lugar do 10 `Source`.

O CONTRATO NOVO (FORMATO-9)
---------------------------
A janela e o RECORDE do status (RV-19 §8) e a formula do EIXO documentado da aura (`Target` no
Dwarven; `Source` no Decay e no Flame) tem de ser UNICA nela:
  * 0 formulas do eixo            -> SystemExit nomeando o range e quantas achou;
  * >1 base DISTINTA do eixo      -> SystemExit nomeando o range e as bases;
  * copias IDENTICAS da formula   -> contam como UMA (o RV-19 §8 documenta a MESMA string 2x no
    Dwarven: o que o gerador recusa e a AMBIGUIDADE, nunca a repeticao do mesmo valor).

O QUE ESTE TESTE PROVA (nos dois sentidos, sem o jogo)
------------------------------------------------------
  1. ACEITA o que e unico: uma formula do eixo -> devolve base, eixo e a citacao do offset; duas
     copias IDENTICAS -> devolve (a repeticao documentada nao e ambiguidade); uma formula do eixo
     com OUTRA do outro eixo ao lado -> devolve a do eixo (o alheio nao e candidato).
  2. REPROVA ALTO o silencio: 0 formulas do eixo na janela (o caso da FORMATO-7) e 2 bases
     DISTINTAS -> `SystemExit` nomeando o range e as quantidades. A regra ANTIGA (transcrita aqui,
     devolver a primeira) devolvia a formula ALHEIA na MESMA janela — e "mostrado reprovando": o
     caso que era silencioso deixa de ser.
  3. NAO mudou o que ja era certo: as 3 janelas do repositorio (constantes de `AURAS_ASSET`) sao
     as de RV-19 §8 com o FIM no PROXIMO status da familia, o eixo esperado e o documentado, e —
     quando o `resources.assets` do install esta presente — as 3 bases e citacoes continuam as
     mesmas e o probe da FORMATO-7 falha alto. Sem o asset, esta parte e apenas nao exercitada
     (o teste continua puro e verde); o que ela cobra no CI e a forma das constantes.
"""
import importlib.util
import os
import tempfile

import arcabouco as arc

META = {
    "nome": "formato9-janela-aura",
    "categoria": "pura",
    "requer": [],
    "descricao": "FORMATO-9: a base da aura no asset exige UMA formula do eixo documentado na "
                 "janela (0 ou >1 base distinta -> SystemExit); a 1a nao vence em silencio",
}

RAIZ = arc.raiz_do_repo()
CAMINHO_GERADOR = os.path.join(RAIZ, "tools", "gera_shrines_esperado.py")


def _gerador():
    spec = importlib.util.spec_from_file_location("gera_shrines_esperado_f9", CAMINHO_GERADOR)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g


def _formula(base, eixo):
    """A MESMA forma que o `RE_FORMULA_STATUS` do gerador exige (espaco unico, ASCII)."""
    return ('Mathf.Round(%g * (1 + (%s["ShrineEffectBonus"] / 100)))' % (base, eixo)).encode("latin-1")


def _asset_sintetico():
    """Um 'resources.assets' minimo: formulas posicionadas por offset, terminadas em NUL."""
    buf = bytearray(b"\x00" * 7000)

    def poe(off, base, eixo):
        f = _formula(base, eixo)
        buf[off:off + len(f)] = f
        buf[off + len(f)] = 0

    poe(1000, 7, "Source")               # (a) unica
    poe(2000, 9, "Source")               # (b) copia identica ...
    poe(2100, 9, "Source")               #     ... da mesma formula
    poe(3000, 7, "Source")               # (c) duas bases distintas
    poe(3100, 10, "Source")
    poe(4000, 20, "Target")              # (d) so o OUTRO eixo (o caso da FORMATO-7)
    poe(6000, 7, "Source")               # (e) do eixo + um alheio ao lado
    poe(6100, 20, "Target")

    caminho = os.path.join(tempfile.mkdtemp(prefix="f9-"), "resources.assets")
    with open(caminho, "wb") as fh:
        fh.write(bytes(buf))
    return caminho


def _comportamento_antigo(asset, aura, janela):
    """A transcricao EXATA do `bases_do_asset` de ANTES da FORMATO-9: devolve a 1a que casa."""
    bruto = _gerador().ler_janela(asset, janela[0], janela[1])
    pos = bruto.find(b"Mathf.Round(")
    while pos >= 0:
        txt = bruto[pos:pos + 120].split(b"\x00", 1)[0].decode("latin-1", errors="replace")
        m = _gerador().RE_FORMULA_STATUS.search(txt)
        if m:
            return float(m.group(1)), m.group(2), "resources.assets@%d" % (janela[0] + pos)
        pos = bruto.find(b"Mathf.Round(", pos + 1)
    raise SystemExit("antigo: nao achou")


def _reprova(asset, aura, eixo, janela):
    """Chama o gerador NOVO e devolve a mensagem do SystemExit (ou levanta `arc.Falhou`)."""
    try:
        _gerador().bases_do_asset(asset, aura, eixo, janela)
    except SystemExit as erro:
        return str(erro)
    raise arc.Falhou("a janela %r do eixo %r NAO falhou alto — devolveu uma base em silencio"
                     % (janela, eixo))


def _aceita(asset, aura, eixo, janela):
    return _gerador().bases_do_asset(asset, aura, eixo, janela)


def corpo():
    asset = _asset_sintetico()

    # 1. ACEITA o unico ------------------------------------------------
    base, eixo, fonte = _aceita(asset, "sintetica", "Source", (900, 1200))
    arc.exigir(base == 7.0 and eixo == "Source" and fonte.endswith("@1000"),
               "a janela com UMA formula do eixo nao devolveu (7, Source, @1000): (%r, %r, %r)"
               % (base, eixo, fonte))

    base, eixo, fonte = _aceita(asset, "sintetica", "Source", (1900, 2200))
    arc.exigir(base == 9.0 and fonte.endswith("@2000"),
               "copias IDENTICAS da mesma formula (o caso documentado do Dwarven) foram recusadas: "
               "(%r, %r)" % (base, fonte))

    base, eixo, fonte = _aceita(asset, "sintetica", "Source", (5900, 6200))
    arc.exigir(base == 7.0 and eixo == "Source",
               "a formula do OUTRO eixo ao lado virou candidata: (%r, %r)" % (base, eixo))

    # 2. REPROVA ALTO o silencio (e o ANTIGO aceitava) -----------------
    msg_estrangeiro = _reprova(asset, "sintetica", "Source", (3900, 4200))
    arc.exigir("3900..4200" in msg_estrangeiro,
               "a falha do eixo ausente NAO nomeia o range: %r" % msg_estrangeiro)
    arc.exigir("nenhuma formula do eixo 'Source'" in msg_estrangeiro,
               "a falha do eixo ausente NAO diz que nao ha formula do eixo: %r" % msg_estrangeiro)
    arc.exigir("1 ocorrencia" in msg_estrangeiro,
               "a falha NAO diz quantas ocorrencias achou: %r" % msg_estrangeiro)

    msg_distintas = _reprova(asset, "sintetica", "Source", (2900, 3200))
    arc.exigir("2900..3200" in msg_distintas and "2 bases DISTINTAS" in msg_distintas,
               "a falha de bases distintas NAO nomeia range+bases: %r" % msg_distintas)

    msg_vazia = _reprova(asset, "sintetica", "Source", (5000, 5100))
    arc.exigir("5000..5100" in msg_vazia and "0 ocorrencia" in msg_vazia,
               "a janela sem NENHUMA ocorrencia nao falhou nomeando range+0: %r" % msg_vazia)

    # "Mostrado reprovando": a MESMA janela pela regra ANTIGA devolvia a formula ALHEIA em silencio.
    antigo = _comportamento_antigo(asset, "sintetica", (3900, 4200))
    arc.exigir(antigo == (20.0, "Target", "resources.assets@4000"),
               "a regra antiga nao reproduziu o silencio esperado (base alheia do Dwarven): %r" % (antigo,))
    arc.exigir(antigo[0] != 7.0,
               "a prova perdeu o sentido: a regra antiga JA devolvia a base certa")

    # 3. NAO mudou o que ja era certo (constantes do repositorio) ------
    g = _gerador()
    esperadas = {
        "Dwarven Aura": ("Target", (1517115056, 1517116232)),
        "Decay Shrine Aura": ("Source", (1517113960, 1517115056)),
        "Flame Shrine Aura": ("Source", (1517120720, 1517121808)),
    }
    vistas = {a[0]: (a[2], a[3]) for a in g.AURAS_ASSET}
    arc.exigir(vistas == esperadas,
               "as janelas/eixos de AURAS_ASSET mudaram (o fim tem de ser o PROXIMO status de "
               "RV-19 §8): %r" % (vistas,))

    real = g.procura_asset()
    if real:
        for aura, (eixo, janela) in esperadas.items():
            base, eixo_obtido, fonte = g.bases_do_asset(real, aura, eixo, janela)
            arc.exigir(eixo_obtido == eixo and fonte.startswith("resources.assets@"),
                       "janela real de %s mudou de forma: (%r, %r)" % (aura, eixo_obtido, fonte))
        # o probe da FORMATO-7 (janela do Decay deslocada): tem de falhar alto, nao devolver o Dwarven.
        _reprova(real, "Decay Shrine Aura", "Source", (1517114277, 1517116000))
        print("com o install presente: as 3 janelas reais batem e o probe da FORMATO-7 falha alto")

    print("FORMATO-9: a base da aura exige UMA formula do eixo documentado na janela — o unico e "
          "aceito, a copia identica tambem (o Dwarven 2x), e 0 formulas do eixo ou 2 bases "
          "distintas FALHAM alto nomeando o range (a 1a nao vence em silencio)")


if __name__ == "__main__":
    arc.main(META, corpo)
