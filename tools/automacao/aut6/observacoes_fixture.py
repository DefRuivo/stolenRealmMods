#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""observacoes_fixture.py - AUT-6: monta as OBSERVACOES de FIXTURE para a prova de fogo.

POR QUE ISSO EXISTE
-------------------
O avaliador (`cobertura.py`) consome OBSERVACOES; a rodada de jogo nao esta autorizada nesta
frente, entao o caminho positivo so pode ser exercitado com FIXTURE - que **nao prova runtime**
(todo criterio sai `prova_runtime=False`, `procedencia=fixture`). O que este arquivo faz e
IMPORTAR o conteudo REAL das fixtures versionadas (`tools/fixtures/*.log`, as novas em
`tools/automacao/aut6/fixtures/`) para dentro das observacoes - o `feed` que o avaliador le e o
BYTE da fixture, nao uma string digitada aqui.

REGRA QUE ELE RESPEITA: o que o coletor runtime entrega e uma OBSERVACAO; o que este modulo
entrega e uma observacao ROTULADA `fixture`. Nenhum numero esperado mora aqui - o esperado e
calculado pelo avaliador das tabelas geradas/oraculo/asset (ver o cabecalho de `cobertura.py`).
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
FIX = os.path.join(AQUI, "fixtures")

F_EXEMPLO = os.path.join(REPO, "tools", "fixtures", "shrines-exemplo.log")
F_DEDUPE = os.path.join(REPO, "tools", "fixtures", "shrines-rv46-dedupe.log")
F_PISO = os.path.join(REPO, "tools", "fixtures", "shrines-piso-cru.log")
F_GLOBULE = os.path.join(FIX, "globule-rv28.txt")
F_ARMOR = os.path.join(FIX, "armor-bug34-superficies.txt")
F_TOOLTIP = os.path.join(FIX, "tooltip-shrine-corpo.txt")


def _ler(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _rel(caminho):
    return os.path.relpath(caminho, REPO).replace("\\", "/")


def _secoes_armor(texto):
    """Separa a fixture de Armor nas duas superficies (`[feed]` e `[corpo]`)."""
    partes, atual = {}, None
    for linha in texto.splitlines():
        if linha.strip() in ("[feed]", "[corpo]"):
            atual = linha.strip().strip("[]")
            partes[atual] = []
            continue
        if atual:
            partes[atual].append(linha)
    return {k: "\n".join(v).strip() for k, v in partes.items()}


def constroi():
    armor = _secoes_armor(_ler(F_ARMOR))
    obs = [
        # (F1) o FEED do exemplo: todas as auras de buff nos 3 bonus + o Decay + o Flame.
        {"id": "F1-feed-exemplo", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_EXEMPLO), "evidencia": [_rel(F_EXEMPLO)], "feed": _ler(F_EXEMPLO),
         "relatorio": "F1-feed-exemplo"},
        # (F2) a rodada de DEDUPE (RV-46) + o Dwarven nos 3 bonus.
        {"id": "F2-feed-dedupe", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_DEDUPE), "evidencia": [_rel(F_DEDUPE)], "feed": _ler(F_DEDUPE),
         "relatorio": "F2-feed-dedupe"},
        # (F3) teto/piso com o valor CRU (MAN-2/REV-47).
        {"id": "F3-feed-limites", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_PISO), "evidencia": [_rel(F_PISO)], "feed": _ler(F_PISO),
         "relatorio": "F3-feed-limites"},
        # (F4) o GLOBULE (RV-28/32) - fixture NOVA desta frente.
        {"id": "F4-feed-globule", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_GLOBULE), "evidencia": [_rel(F_GLOBULE)], "feed": _ler(F_GLOBULE),
         "relatorio": "F4-feed-globule"},
        # (F5) ENTRAR na aura: o personagem em foco declarado DENTRO.
        {"id": "F5-dentro-da-aura", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_EXEMPLO), "evidencia": [_rel(F_EXEMPLO)], "feed": _ler(F_EXEMPLO),
         "personagem": "ChkWA", "dentro_da_aura": True, "relatorio": "F5-dentro-da-aura"},
        # (F6) SAIR da aura: personagem declarado FORA e nenhuma linha dele no log.
        {"id": "F6-fora-da-aura", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_DEDUPE), "evidencia": [_rel(F_DEDUPE)], "feed": _ler(F_DEDUPE),
         "personagem": "ChkFora", "dentro_da_aura": False, "relatorio": "F6-fora-da-aura"},
        # (F7) o CORPO renderizado da tooltip de shrine (superficie do AUT-4, nao do log).
        {"id": "F7-corpo-shrine", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_TOOLTIP), "evidencia": [_rel(F_TOOLTIP)],
         "superficie": "tooltip_shrine", "texto_renderizado": _ler(F_TOOLTIP),
         "relatorio": "F7-corpo-shrine"},
        # (F8) o FEED de combate do Armor (superficie que NAO pode ter a nota).
        {"id": "F8-armor-feed", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_ARMOR), "evidencia": [_rel(F_ARMOR)],
         "superficie": "feed", "texto_renderizado": armor.get("feed", ""),
         "relatorio": "F8-armor-feed"},
        # (F9) o CORPO da tooltip do status (superficie que TEM de ter a nota).
        {"id": "F9-armor-corpo", "procedencia": "fixture", "rotulo_fixture": True,
         "objeto": _rel(F_ARMOR), "evidencia": [_rel(F_ARMOR)],
         "superficie": "tooltip_status", "texto_renderizado": armor.get("corpo", ""),
         "relatorio": "F9-armor-corpo"},
    ]
    return obs


DESTINO = os.path.join(AQUI, "observacoes-fixture.json")


def main(argv=None):
    obs = constroi()
    amostras = [o for o in obs if not os.path.isfile(os.path.join(REPO, o["objeto"]))]
    if amostras:
        raise SystemExit("FALHA(2): fixture ausente: %s" % amostras)
    if argv and "--gravar" in argv:
        with open(DESTINO, "w", encoding="utf-8") as fh:
            json.dump(obs, fh, ensure_ascii=False, indent=2)
        print("gravado: %s (%d observacoes)" % (DESTINO, len(obs)))
    else:
        print("observacoes de fixture: %d (nenhum arquivo escrito; use --gravar)" % len(obs))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
