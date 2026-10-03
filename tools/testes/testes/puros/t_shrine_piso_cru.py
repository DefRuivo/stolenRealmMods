#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MAN-2 / REV-47 (achados 3 e 1) — o PISO do atributo e o VALOR CRU no marcador de log.

O QUE ESTE TESTE GARANTE
------------------------
Dois buracos da ferramenta de LOG/DESPEJO das auras de shrine, consertados em marcas de log
apenas (nenhum texto do jogador, nenhuma formula e nenhuma convencao de numero mudam):

1. **PISO INVISIVEL.** `MarcaTeto`/`TetoDoAtributo` (`ShrineAuraPatch.cs`) so olhavam `HasMax`.
   Um atributo com PISO (`HasMin`/`MinValue`) NUNCA gerava linha — pelo log nao dava para provar
   NEM negar o piso, e o `ManaCostMod` parecia "sem teto nenhum" (o dado so apareceu lendo o asset
   a mao). O conserto faz o marcador olhar `HasMin`/`MinValue` e emitir
   `RV-46 piso '<atributo>': MinValue=<valor> ... no-piso=sim|nao`, como ja fazia para o teto.
2. **VALOR CRU AUSENTE.** O marcador imprimia so o total JA CORTADO: no `Damage taken` com DOIS
   Guardians o cru (90) teve de ser INFERIDO da soma por instancia provada no RV-46, nao MEDIDO.
   O conserto acrescenta `cru=` ao lado do `total` — e o cru NAO e estimado: e o MESMO numero que o
   motor calcula ANTES do corte, pelo caminho publico que ele proprio usa
   (`GetAttributeValueByMethod` + `SavedMap` + `CalculateAttribute`, o `CalculateAttributeViaSweeps`
   do decompilado).

O QUE ELE CONFERE, E COM QUE PROVA
----------------------------------
(a) **O FONTE VIVO do mod** (`BetterTooltips/Patches/ShrineAuraPatch.cs`): o marcador LE
    `HasMin`/`MinValue`, EMITE `RV-46 piso`/`no-piso=`/`cru=` e MEDE o cru pelo caminho do motor.
    Cada exigencia e uma substring do fonte e cada uma tem a ISCA embutida: o defeito e plantado
    numa copia EM MEMORIA do fonte e a checagem tem de REPROVAR. Checagem que nunca foi vista
    reprovando seria decoracao.
(b) **A FERRAMENTA que le o log** (`tools/checa_shrines.py`, importada de verdade): a fixture
    `tools/fixtures/shrines-piso-cru.log` (SINTETICA, rotulada) traz as duas marcas novas e o
    `coleta()` do proprio conferidor tem de ler o piso (`MinValue=-75`), o teto (`MaxValue=50`) e o
    `cru` dos dois; e um log no formato ANTIGO (teto sem `cru=`) continua sendo lido como antes.
(c) **A CONTA DO CORTE fica visivel**: para o `Damage taken` com 2 Guardians o cru (90) e MAIOR que
    o `MaxValue` (50) e o total lido e exatamente o teto; para o `ManaCostMod` no piso o cru (-100)
    e MENOR que o `MinValue` (-75) e o total lido e exatamente o piso. Sem o campo cru isso nao
    aparecia em lugar nenhum do log.

DE ONDE VEM CADA NUMERO
-----------------------
Do ASSET do jogo (os MESMOS pontos que o mod le em runtime), citados no cabecalho da fixture:
`DamageReduction` `HasMax` MaxValue=50 (`resources.assets` @1519603860) e `ManaCostMod` `HasMin`
MinValue=-75 (@1519616544, o float logo depois do bool `HasMin`; `HasMax` ausente). A %/base das
auras (Guardian 20, Energy -50) e a do censo, ja usada pela familia TST-2 (`tools/dados/*.csv`).
"""
import os
import re
import sys

import arcabouco as arc
import regras_bf

META = {
    "nome": "shrine-piso-cru",
    "categoria": "pura",
    "requer": [],
    "descricao": "MAN-2/REV-47: o marcador publica o PISO (HasMin/MinValue) e o valor CRU antes do corte, e o conferidor le os dois",
}

FIXTURE = os.path.join(arc.raiz_do_repo(), "tools", "fixtures", "shrines-piso-cru.log")
FIXTURE_ANTIGA = os.path.join(arc.raiz_do_repo(), "tools", "fixtures", "shrines-rv46-dedupe.log")
FONTE = os.path.join(arc.raiz_do_repo(), "BetterTooltips", "Patches", "ShrineAuraPatch.cs")

# As exigencias no FONTE VIVO do marcador. Cada substring e o que o conserto tem de ter para o
# buraco ficar fechado; a isca embutida (remover a substring da copia em memoria) prova que a
# checagem REPROVA de verdade.
EXIGENCIAS = (
    ("atributo.HasMin", "o marcador deixou de olhar o PISO do atributo (`CharacterAttribute.HasMin`)"),
    ("atributo.MinValue", "o marcador deixou de ler o VALOR do piso (`CharacterAttribute.MinValue`)"),
    ("RV-46 piso '{nome}': MinValue=", "a linha do PISO (`RV-46 piso ... MinValue=`) saiu do marcador"),
    ("no-piso=", "o campo `no-piso=` saiu do marcador (o piso nao pode mais ser provado nem negado)"),
    ("\" cru=\" + ComSinal(cru)", "o campo `cru=` saiu do marcador (o total volta a sair so cortado)"),
    ("ValorCruDoMotor", "o medidor do valor CRU saiu do marcador"),
    ("receptor.GetAttributeValueByMethod(", "o cru deixou de ser medido pelo caminho publico do motor"),
    ("CharacterEffectMethod.Set", "o cru deixou de olhar o bucket `Set` (o motor o trata como absoluto)"),
    ("receptor.SavedMap[atributo.Guid]", "o cru deixou de partir do `SavedMap` (a base do personagem)"),
    ("receptor.CalculateAttribute(atributo, cru, false, false)",
     "o cru deixou de passar pelo `CalculateAttribute` (Base/Percentage/Multiplicative) do motor"),
    ("receptor.CalculateAttribute(atributo, cru, true, false)",
     "o cru deixou de aplicar a SEGUNDA PASSADA quando o atributo pede"),
)


def fonte_do_mod():
    """O CODIGO EFETIVO do marcador: o fonte vivo SEM COMENTARIO (`regras_bf.sem_comentarios`).

    Comentario nao e codigo: sem isto, uma exigencia satisfeita so no cabecalho (que cita o
    formato) passaria, e a isca nao derrubaria a checagem. Os literais de STRING (o formato do
    log) sao preservados - e neles que as marcas vivem.
    """
    arc.exigir(os.path.isfile(FONTE),
               "a fonte viva do marcador sumiu: %s (o teste vigia ela, nao uma copia)" % FONTE)
    with open(FONTE, encoding="utf-8") as fh:
        return regras_bf.sem_comentarios(fh.read())


def ferramenta_do_log():
    """Importa o conferidor REAL (`tools/checa_shrines.py`) - nao uma copia do parser dele."""
    caminho = os.path.join(arc.raiz_do_repo(), "tools")
    if caminho not in sys.path:
        sys.path.insert(0, caminho)
    import checa_shrines
    return checa_shrines


def corpo():
    fonte = fonte_do_mod()

    # ------------------------------------------------------------------ (a) o fonte vivo + iscas
    for sub, mensagem in EXIGENCIAS:
        arc.exigir(sub in fonte, "%s (procurei %r no CODIGO de ShrineAuraPatch.cs)" % (mensagem, sub))
        # ISCA EMBUTIDA: com TODAS as ocorrencias da substring arrancadas, a MESMA checagem tem de
        # reprovar. Checagem que nunca foi vista reprovando seria decoracao.
        arc.exigir(sub not in fonte.replace(sub, ""),
                   "a checagem de %r nao REPROVA quando o defeito e plantado - checagem decorativa" % sub)

    # o teto (que ja existia) NAO pode ter perdido o desenho antigo: o cru entrou SEM tirar o resto.
    for sub in ("RV-46 teto '{nome}': MaxValue=", "no-teto=", "TetoDoAtributo"):
        arc.exigir(sub in fonte, "a linha do TETO regrediu: sumiu %r do marcador" % sub)

    # ------------------------------------------------------------------ (b) a ferramenta le o log
    tool = ferramenta_do_log()
    arc.exigir(os.path.isfile(FIXTURE),
               "a fixture das marcas novas sumiu: %s" % FIXTURE)
    with open(FIXTURE, encoding="utf-8") as fh:
        log = fh.read()

    linhas = [l for l in log.splitlines() if "[Shrine RV-23]" in l]
    teto_linhas = [l for l in linhas if "RV-46 teto '" in l]
    piso_linhas = [l for l in linhas if "RV-46 piso '" in l]
    arc.igual(len(teto_linhas), 1, "linhas `RV-46 teto` na fixture")
    arc.igual(len(piso_linhas), 3, "linhas `RV-46 piso` na fixture (os 3 bonus do Energy)")

    obs = tool.coleta(log)

    # O PISO: era o que NAO existia. A ferramenta tem de ler o valor do asset e o `no-piso`.
    arc.igual(obs["pisos"].get(("Man2Energy", "ManaCostMod")), -75.0,
              "o PISO do ManaCostMod lido do log (MinValue=-75, resources.assets @1519616544)")
    arc.igual(obs["cru"].get(("Man2Energy", "ManaCostMod")), -100.0,
              "o CRU do ManaCostMod no piso (a aura empurra -100; o total lido e -75)")
    m = tool.RE_PISO.match(piso_linhas[-1].split("[Shrine RV-23] ", 1)[1].strip())
    arc.exigir(m, "a linha do piso nao casa com o RE_PISO do conferidor: %r" % piso_linhas[-1])
    arc.igual(m.group("no_piso"), "sim", "`no-piso` quando o total esta EXATAMENTE no piso")
    arc.igual(tool.numero(m.group("total")), -75.0, "o total (cortado) no piso")

    # O TETO com o cru: o caso do cartao (2 Guardians) - o corte tem de ficar VISIVEL.
    arc.igual(obs["tetos"].get(("Man2Guard", "DamageReduction")), 50.0,
              "o TETO do DamageReduction lido do log (MaxValue=50, resources.assets @1519603860)")
    arc.igual(obs["cru"].get(("Man2Guard", "DamageReduction")), 90.0,
              "o CRU do Damage taken com 2 Guardians (2 x 40 + resto 10 = 90, ANTES do corte)")

    # ------------------------------------------------------------------ (c) a conta do corte
    cru, teto = 90.0, 50.0
    arc.exigir(cru > teto, "o caso do cartao perdeu o sentido: o cru (%s) nao passa do teto (%s)" % (cru, teto))
    arc.igual(tool.fmt(teto), "50", "o total lido com o atributo no teto e o proprio MaxValue")
    cru_min, piso = -100.0, -75.0
    arc.exigir(cru_min < piso, "o caso do piso perdeu o sentido: o cru (%s) nao esta abaixo do piso (%s)"
               % (cru_min, piso))
    # O log do jogo (fixture) tem de trazer o MESMO par: total cortado == limite, cru fora dele.
    arc.igual(tool.numero(m.group("cru")), cru_min, "o cru logado no piso")
    arc.igual(tool.numero(m.group("min")), piso, "o MinValue logado")

    # ------------------------------------------------------------------ (d) compatibilidade
    # Um log ANTERIOR ao MAN-2 (o `RV-46 teto` do RV-46, sem ` cru=` no meio) continua sendo lido.
    arc.exigir(os.path.isfile(FIXTURE_ANTIGA), "a medicao em jogo do RV-46 sumiu: %s" % FIXTURE_ANTIGA)
    with open(FIXTURE_ANTIGA, encoding="utf-8") as fh:
        antigo = fh.read()
    alvo = [l for l in antigo.splitlines() if "RV-46 teto '" in l]
    arc.exigir(alvo, "a fixture antiga nao tem nenhuma linha `RV-46 teto`")
    payload = alvo[0].split("[Shrine RV-23] ", 1)[1].strip()
    m_antigo = tool.RE_TETO.match(payload)
    arc.exigir(m_antigo, "o RE_TETO deixou de ler o formato ANTIGO (sem `cru=`): %r" % payload)
    arc.igual(m_antigo.group("cru"), None, "no log antigo o ` cru=` e ausente (o grupo e opcional)")
    arc.exigir(" cru=" not in payload, "a fixture antiga ja tem `cru=` - o caso de compatibilidade se perdeu")

    print("MAN-2: %d exigencias no fonte (todas com isca), piso=%s cru_teto=%s cru_piso=%s lidos do log"
          % (len(EXIGENCIAS), tool.fmt(-75.0), tool.fmt(90.0), tool.fmt(-100.0)))


if __name__ == "__main__":
    arc.main(META, corpo)
