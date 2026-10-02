#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BT-11 (Hunger) — a prova de fogo VERSIONADA do valor dinamico da passiva `Hunger`.

POR QUE ESTE TESTE EXISTE
-------------------------
O caminho do valor do `Hunger` nasceu com prova de fogo propria (scratch/bt11/, tres iscas:
numero digitado, valor constante e ancora errada na %), mas ela vive em `scratch/`, que e
GITIGNORED — no CI estas tres skills nao tinham NENHUM teste. Este arquivo traz a prova para a
suite versionada, lendo o fonte C# por RECORTE ESTRUTURAL (`recorte.py`, casamento de chaves,
literal-aware, FALHA ALTO) e ancorando em IDENTIFICADOR — nunca em numero de linha: o
`LocalizePatch.cs` e os patches mudam toda hora.

O QUE ELE TRAVA (o defeito que motivaria cada item)
---------------------------------------------------
  1. O VALOR SAI DA VIDA MAXIMA DO MOTOR. O fonte le `personagem.MaxHealth` (propriedade
     FINAL do motor, com gear/powerups/skills) e NAO crava nenhum literal em `vida`. Se alguem
     trocar por constante, o numero deixa de acompanhar o personagem — e o item reprova.
  2. A % SAI DO ASSET EM RUNTIME. A skill vem de `Game.Instance.Skills` e a % de
     `LePercentual(skill.Description, ...)`; nenhum literal NAO-NULO e atribuido a `pct`. Cravar
     o `10` reprova (o asset e a fonte, nao o mod).
  3. O PARSER ANCORA EM `health` — NAO PEGA A PRIMEIRA %. A descricao do `Hunger` tem DUAS
     porcentagens ("Grants 10% @mana steal@.  Sacrifices 10% maximum health per turn."): a do
     MANA (primeira) e a do SACRIFICIO. Hoje as duas valem 10 por COINCIDENCIA do asset; o
     teste roda uma descricao SINTETICA onde elas DIVERGEM (5% mana x 12% sacrificio) e exige o
     12 — a ancora em `health` e o que garante isso. O atalho da "primeira %" daria 5.
  4. O FORMATO TERMINA EM `).`. O valor entra como parentese no fim da frase do jogo
     (` (... health per turn for you).`) — a linha montada tem de fechar em `).`.
  5. FAIL-SAFE. Sem personagem em foco ou sem vida maxima, a linha do jogo fica INTACTA: os
     dois guardas retornam `false` ANTES de montar o texto (nada de numero meio calculado), e o
     `catch` tambem devolve a linha intacta.

LIMITE (o que este teste NAO prova): ele NAO executa o C# do mod (isso pediria a `lib/` do jogo
e um harness por test); a ligacao com o motor e o RECORTE das propriedades que o patch le
(`Character.MaxHealth`, `Character.MaxHealth`/`Health` pelo indexador) e a descricao do asset,
que este teste carrega do CENSO versionado (`docs/cobertura/skills.csv`).
"""
import csv
import io
import os
import re

import arcabouco as arc
import recorte as rec

META = {
    "nome": "bt11-hunger",
    "categoria": "pura",
    "requer": [],
    "descricao": "BT-11: o valor do Hunger sai da vida MAXIMA do motor e da % do asset em runtime, "
                 "o parser ancora em 'health' (e nao pega a primeira % do texto), o formato termina "
                 "em ').' e sem personagem/vida maxima a linha fica intacta",
}

ARQUIVO = os.path.join("BetterTooltips", "Patches", "HungerPatch.cs")
CENSO = os.path.join("docs", "cobertura", "skills.csv")

# As descricoes que o teste roda no parser. A do ASSET vem do censo versionado (o texto real do
# jogo); a DIVERGENTE e sintetica, com a mesma forma, para provar que a ancora escolhe a % do
# SACRIFICIO quando as duas NAO coincidem.
DESCRICAO_DIVERGENTE = "Grants 5% @mana steal@.  Sacrifices 12% maximum health per turn."


# --------------------------------------------------------------- leitura dos fontes ---

def _arquivo(relativo):
    caminho = os.path.join(arc.raiz_do_repo(), relativo)
    with io.open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _codigo():
    """O fonte EFETIVO (sem comentario) — a prosa do comentario nao e codigo e nao pode
    satisfazer uma checagem estrutural."""
    return rec.codigo_efetivo(_arquivo(ARQUIVO))


def _metodo(codigo, assinatura, marcas):
    """Recorte ESTRUTURAL do metodo inteiro, com o guarda que impede a volta da janela."""
    bloco = rec.corpo_do_metodo(codigo, assinatura)
    rec.exigir_metodo_inteiro(bloco, assinatura, marcas)
    return bloco


def _linha_do_censo(nome):
    leitor = csv.DictReader(io.open(os.path.join(arc.raiz_do_repo(), CENSO), encoding="utf-8-sig"))
    for linha in leitor:
        if (linha.get("nome") or "").strip() == nome:
            return linha
    raise arc.Falhou("a skill %r nao esta no censo %s (versionado)" % (nome, CENSO))


# ------------------------------------------------------- o MESMO parser do C# (espelho) ---

def le_percentual(descricao):
    """Espelho de `HungerPatch.LePercentual`: ancora em `health` e anda para tras ate a ULTIMA
    `%` antes dela. Devolve float ou None (nada de adivinhar)."""
    if not descricao:
        return None
    ancora = descricao.lower().find("health")
    if ancora < 0:
        return None
    fim = descricao.rfind("%", 0, ancora + 1)
    if fim < 0:
        return None
    ini = fim
    while ini > 0 and (descricao[ini - 1].isdigit() or descricao[ini - 1] in ".,"):
        ini -= 1
    if ini >= fim:
        return None
    try:
        return float(descricao[ini:fim].replace(",", "."))
    except ValueError:
        return None


def le_percentual_ingenua(descricao):
    """A leitura ERRADA que a ancora existe para evitar: a PRIMEIRA `%` do texto (a do mana
    steal). Serve de contraprova do item 3 — nao e o que o mod faz."""
    fim = descricao.find("%")
    if fim < 0:
        return None
    ini = fim
    while ini > 0 and (descricao[ini - 1].isdigit() or descricao[ini - 1] in ".,"):
        ini -= 1
    return float(descricao[ini:fim].replace(",", ".")) if ini < fim else None


def formata(x):
    """O `ToString("0.#", InvariantCulture)` do C#: uma casa, sem `.0` sobrando."""
    texto = "%.1f" % round(float(x), 1)
    return texto[:-2] if texto.endswith(".0") else texto


def valor_do_motor(vida, pct):
    """A MESMA conta do patch: `vida * pct / 100f`, formatada com `0.#`."""
    return formata(vida * pct / 100.0)


def insere_valor(linha_do_jogo, valor):
    """Espelho de `HungerPatch.InsereValorNaLinha`: o valor entra ANTES do ponto final."""
    corpo = (linha_do_jogo or "").rstrip()
    sufixo = " (<color=#CBB396>%s</color> health per turn for you)" % valor
    if corpo.endswith("."):
        return corpo[:-1] + sufixo + "."
    return corpo + sufixo + "."


# ------------------------------------------------------------------------- corpo ---

def _valor_vem_do_motor(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    arc.exigir("personagem.MaxHealth" in tenta,
               "o valor nao sai de `personagem.MaxHealth` (a vida maxima FINAL do motor)")
    arc.exigir("vida * pct / 100f" in tenta,
               "a conta nao e `sacrificio = vida * pct / 100f` (a mesma do efeito do asset)")
    arc.exigir("ShrineAuraPatch.ReceptorDaTooltip()" in tenta,
               "o personagem nao e o RECEPTOR da tooltip (caminho RV-26/RV-28/RV-33)")
    arc.exigir(re.search(r"\bvida\s*=\s*[0-9]", tenta) is None,
               "ha um literal NAO-NULO atribuido a `vida` — a vida maxima foi DIGITADA")
    arc.exigir(re.search(r"\bsacrificio\s*=\s*[0-9]", tenta) is None,
               "ha um literal NAO-NULO atribuido a `sacrificio` — o valor virou CONSTANTE")
    return tenta


def _pct_vem_do_asset(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    skill = _metodo(codigo, "private static SkillInfo SkillDoHunger()", ("Game.Instance.Skills",))
    pct = _metodo(codigo, "private static float PercentualDaSkill(SkillInfo skill)", ("_pctLido",))
    arc.exigir("PercentualDaSkill(skill)" in tenta,
               "a % nao sai de `PercentualDaSkill(skill)`")
    arc.exigir("LePercentual(skill.Description" in pct,
               "a % nao sai de `LePercentual(skill.Description, ...)` (o texto do asset)")
    arc.exigir("Game.Instance.Skills" in skill,
               "a skill nao vem do asset CARREGADO (`Game.Instance.Skills`)")
    arc.exigir(re.search(r"\bpct\s*=\s*[1-9]", codigo) is None,
               "ha um literal NAO-NULO atribuido a `pct` — a porcentagem foi DIGITADA")


def _parser_ancora_em_health(codigo):
    le = _metodo(codigo, "private static bool LePercentual(string descricao, out float pct)",
                 ("float.TryParse(numero",))
    arc.exigir('descricao.IndexOf("health"' in le,
               "o parser nao ancora na palavra `health` da frase de vida maxima")
    arc.exigir("descricao.LastIndexOf('%', ancora)" in le,
               "a % lida nao e a ULTIMA antes da ancora (`LastIndexOf('%', ancora)`)")
    arc.exigir("descricao.IndexOf('%')" not in le,
               "o parser usa a PRIMEIRA % do texto (`IndexOf('%')` cru) — pegaria a do mana steal")

    do_asset = _linha_do_censo("Hunger")
    descricao_do_asset = do_asset["descricao"]
    arc.exigir(descricao_do_asset.count("%") == 2,
               "a descricao do Hunger no censo deixou de ter DUAS %% (tem %d): %r"
               % (descricao_do_asset.count("%"), descricao_do_asset))
    arc.igual(le_percentual(descricao_do_asset), 10.0,
              "o parser le a %% do SACRIFICIO na descricao do asset")
    arc.igual(le_percentual(DESCRICAO_DIVERGENTE), 12.0,
              "com %% DIVERGENTES (5%% mana x 12%% sacrificio) o parser tem de devolver o SACRIFICIO")
    arc.exigir(le_percentual_ingenua(DESCRICAO_DIVERGENTE) == 5.0,
               "a contraprova perdeu o sentido: a 'primeira %%' deveria dar 5")
    arc.exigir(le_percentual(DESCRICAO_DIVERGENTE) != le_percentual_ingenua(DESCRICAO_DIVERGENTE),
               "a ancora e a 'primeira %%' dao o mesmo numero — o caso nao separa as duas leituras")
    return descricao_do_asset


def _formato_termina_em_ponto_paren(codigo):
    ins = _metodo(codigo, "private static string InsereValorNaLinha(string linhaDoJogo, string valor)",
                  ('sufixo + "."',))
    arc.exigir("health per turn for you)" in ins,
               "o sufixo do valor nao fecha em `health per turn for you)`")
    # Os DOIS ramos do formato (linha que ja termina em ponto e linha que nao) tem de fechar em `).`.
    retornos = [l.strip() for l in ins.splitlines() if l.strip().startswith("return ")]
    arc.exigir(len(retornos) == 2,
               "a montagem da linha deixou de ter os DOIS ramos de retorno (tem %d)" % len(retornos))
    for linha in retornos:
        arc.exigir(linha.rstrip().endswith('+ ".";'),
                   "um ramo de retorno nao fecha o formato com o ponto final: %r" % linha)
    arc.exigir('corpo.EndsWith(".", StringComparison.Ordinal)' in ins,
               "o patch nao trata a linha que JA termina em ponto (inseriria dois pontos)")
    # O comportamento do espelho nos DOIS ramos do formato.
    com_ponto = insere_valor("Sacrifices 10% maximum health per turn.", "23.3")
    sem_ponto = insere_valor("Sacrifices 10% maximum health per turn", "23.3")
    arc.exigir(com_ponto.endswith(").") and sem_ponto.endswith(")."),
               "a linha montada nao termina em `).`: %r / %r" % (com_ponto, sem_ponto))
    arc.exigir(com_ponto.count(".") == sem_ponto.count("."),
               "inserir valor duplicou/comeu o ponto final: %r / %r" % (com_ponto, sem_ponto))
    return ins


def _fail_safe(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    i_monta = tenta.find("linhaComValor = InsereValorNaLinha")
    arc.exigir(i_monta > 0, "nao achei onde a linha e montada (`InsereValorNaLinha`)")
    arc.exigir(tenta.find("linhaComValor = null;") < i_monta,
               "a linha nao e zerada ANTES do calculo (default de linha intacta)")

    for rotulo, guarda in (("sem personagem", "if (personagem == null)"),
                           ("sem vida maxima", "if (vida <= 0f)"),
                           ("sem a % do asset", "if (pct <= 0f)")):
        i = tenta.find(guarda)
        arc.exigir(i >= 0, "falta o guarda '%s' (%r)" % (rotulo, guarda))
        arc.exigir(i < i_monta, "o guarda '%s' vem DEPOIS de montar a linha" % rotulo)
        ramo = rec.bloco_apos(tenta, i)
        arc.exigir("return false;" in ramo,
                   "o guarda '%s' nao devolve false (o texto seguia adiante)" % rotulo)
        arc.exigir("linhaComValor = Insere" not in ramo,
                   "o guarda '%s' monta a linha mesmo assim — nao e fail-safe" % rotulo)

    i_catch = tenta.find("catch (Exception ex)")
    arc.exigir(i_catch > 0, "nao achei o `catch` que garante a linha intacta na excecao")
    cauda = tenta[i_catch:]
    arc.exigir("linhaComValor = null;" in cauda and "return false;" in cauda,
               "o `catch` nao devolve a linha intacta (`linhaComValor = null; return false;`)")


def corpo():
    codigo = _codigo()
    _valor_vem_do_motor(codigo)
    _pct_vem_do_asset(codigo)
    descricao_do_asset = _parser_ancora_em_health(codigo)
    _formato_termina_em_ponto_paren(codigo)
    _fail_safe(codigo)

    # DEMONSTRACAO (nao prova): a mesma formula acompanha a vida maxima, e a linha montada.
    pct = le_percentual(descricao_do_asset)
    valores = {v: valor_do_motor(v, pct) for v in (100, 200, 233, 500)}
    arc.igual(valores[200], "20", "a formula e linear na vida maxima (200%% -> 20)")
    linha = insere_valor("Sacrifices 10% max health per turn.", valores[233])
    arc.exigir("<color=#CBB396>23.3</color>" in linha,
               "a linha do valor nao cita o valor na cor do motor: %r" % linha)
    print("        100->%s 200->%s 233->%s 500->%s" % tuple(valores[v] for v in (100, 200, 233, 500)))
    print("        " + linha)


if __name__ == "__main__":
    arc.main(META, corpo)
