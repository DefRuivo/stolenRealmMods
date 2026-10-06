# -*- coding: utf-8 -*-
"""regras_rv28_globule.py - RV-28 (blindagem, 06/10): as GUARDAS do tooltip do globule e a MATRIZ de aceite.

O QUE ESTA BIBLIOTECA EXISTE PARA TORNAR EXECUTAVEL
---------------------------------------------------
O `RV-28` faz o tooltip de todo globule mostrar a cura do `Sustenance` com o numero da vida/mana
MAXIMAS do personagem em foco (`BetterTooltips/Patches/GlobulePatch.cs`). Isso o coloca no caminho
mais perigoso do mod: ele roda a CADA FRAME de hover, le atributo do personagem e escreve dentro do
texto que o jogo ja montou. As guardas obrigatorias (as mesmas do `RV-22`) sao:

  1. ASSINATURA EXPLICITA do metodo (sem depender de contexto implicito);
  2. `try/catch` em todo o corpo, com a queda = texto SEM numero;
  3. o ATRIBUTO EXISTE ANTES DA LEITURA — `Character.this[string]` LANCA para nome desconhecido
     (`throw new Exception("No attribute named " + attributeName)`, `Character.cs` do decompilado,
     l.3960-3973), e `Character.MaxHealth`/`MaxMana` sao `Mathf.Ceil(this["MaxHealth"/"MaxMana"])`
     (l.3660/3662). A guarda usa as consultas SEM LANCAR do jogo (`Game.GetAttribute` /
     `Game.GetVariableAttribute`, `Burst2Flame/Game.cs` l.1383-1399), que sao exatamente as duas que
     o proprio indexador consulta antes de lancar. O `catch` NAO e a guarda: ele nao pode ser o
     caminho normal do atributo ausente (isso seria engolir erro de forma indiscriminada);
  4. alvo NULO / tooltip fora de contexto de jogador (inspecao, loja, o `WorldCharacter` vazio do
     shrine) -> sem numero;
  5. NUNCA somar a mao tier I com tier II — a % sai da LISTA ATIVA do jogo (`Character.Skills`, ja
     resolvida por `SkillsThatReplace`), nunca de uma tabela de tiers do mod.

Este arquivo NAO muda comportamento de mod nenhum: e material de teste. Ele LE o fonte VIVO e a
fonte INDEPENDENTE da porcentagem (`docs/cobertura/acoes.csv`, o censo das acoes do motor), e traz
a ISCA EMBUTIDA (cada defeito plantado numa copia em memoria) — checagem que nunca foi vista
reprovando seria decoracao.
"""
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))            # tools/testes
RAIZ = os.path.dirname(os.path.dirname(DIR))                # raiz do repo
GLOBULE = os.path.join(RAIZ, "BetterTooltips", "Patches", "GlobulePatch.cs")
LOCALIZE = os.path.join(RAIZ, "BetterTooltips", "Patches", "LocalizePatch.cs")
ACOES = os.path.join(RAIZ, "docs", "cobertura", "acoes.csv")
CASOS_AUT6 = os.path.join(RAIZ, "tools", "automacao", "aut6", "casos-aut6.json")
FIXTURE_AUT6 = os.path.join(RAIZ, "tools", "automacao", "aut6", "fixtures", "globule-rv28.txt")

if DIR not in sys.path:
    sys.path.insert(0, DIR)

import arcabouco as arc      # noqa: E402
import recorte as _rec       # noqa: E402  o recorte ESTRUTURAL (casamento de chaves)


# --------------------------------------------------------------------------- #
# o FONTE vivo
# --------------------------------------------------------------------------- #

SIG_FRASE = "public static string FraseSustenance(string chaveDaTooltip)"
SIG_ATRIBUTO = "private static bool AtributoExiste(Character personagem, string nome)"
CHAMADA_GUARDA_VIDA = 'AtributoExiste(personagem, "MaxHealth")'
CHAMADA_GUARDA_MANA = 'AtributoExiste(personagem, "MaxMana")'
LEITURA_VIDA = "float vida = personagem.MaxHealth;"
LEITURA_MANA = "float mana = personagem.MaxMana;"
ALVO_NULO = "if (personagem == null)"


def le_fonte(caminho=GLOBULE):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _corpo(fonte, assinatura):
    """O CORPO INTEIRO do metodo, por casamento de chaves (nunca janela de caracteres)."""
    return _rec.corpo_do_metodo(fonte, assinatura)


# --------------------------------------------------------------------------- #
# a FONTE INDEPENDENTE da %: o censo das acoes do motor (`docs/cobertura/acoes.csv`)
# --------------------------------------------------------------------------- #

_RE_VIDA_DA_ACAO = re.compile(r"Target\.MaxHealth\s*\*\s*(\d*\.?\d+)f")


def pct_das_acoes(caminho=ACOES):
    """{tier: pct} lido da ACAO do motor — `Sustenance I Proc` = `.08f`, `II Proc` = `.20f`.

    Nada digitado: o numero sai da formula do asset de acao transcrita no censo
    (`acoes.csv:255-256`), que e a fonte independente da porcentagem (o mod le a descricao da
    skill; a acao do proc e o que o motor REALMENTE usa).
    """
    tabela = {}
    with open(caminho, encoding="utf-8", newline="") as fh:
        for linha in fh:
            linha = linha.rstrip("\r\n")
            if not linha or linha.startswith("nome,"):
                continue
            nome = linha.split(",", 1)[0].strip()
            if not nome.endswith(" Proc"):
                continue
            m = _RE_VIDA_DA_ACAO.search(linha)
            if not m:
                continue
            tabela[nome[: -len(" Proc")]] = float(m.group(1)) * 100.0
    return tabela


def pct_das_tiers(tiers, acoes=None):
    """A % que o mod mostra: a SOMA do que o JOGO tem ativo (nunca uma soma nossa).

    Cada tier que fica em `Character.Skills` tem o proprio gatilho (`Sustenance I Proc` /
    `Sustenance II Proc`) e por isso as % somam — mas SOMENTE as tiers que o jogo deixou na lista
    (a lista ja vem resolvida pelo `SkillsThatReplace` de cada skill, decompilado l.32876-32888).
    """
    acoes = acoes if acoes is not None else pct_das_acoes()
    total = 0.0
    for tier in tiers:
        total += acoes[tier]
    return total


# --------------------------------------------------------------------------- #
# a CONTA e o FORMATO do `FraseSustenance`
# --------------------------------------------------------------------------- #

def formata(x):
    """Espelha `x.ToString("0.#", CultureInfo.InvariantCulture)`: inteiro sem casa, senao UMA casa."""
    r = round(abs(x) + 1e-12, 1) if x >= 0 else -round(abs(x) + 1e-12, 1)
    if abs(r - round(r)) < 1e-9:
        return "%d" % int(round(r))
    return "%.1f" % r


def cura(vida, mana, pct):
    """Espelha `(vida * pct / 100f).ToString("0.#")` — float de 32 bits, como no C#."""
    v = arc.f32(vida)
    m = arc.f32(mana)
    p = arc.f32(pct)
    return (formata(arc.f32(arc.f32(v * p) / 100.0)),
            formata(arc.f32(arc.f32(m * p) / 100.0)))


# --------------------------------------------------------------------------- #
# AS GUARDAS (estrutura do fonte vivo)
# --------------------------------------------------------------------------- #

def guardas_do_globule(fonte):
    """As violacoes das 5 guardas obrigatorias no fonte. Lista vazia = nenhuma violacao."""
    viol = []

    if SIG_FRASE not in fonte:
        viol.append("(1) sem ASSINATURA EXPLICITA de `FraseSustenance(string chaveDaTooltip)`")
        return viol
    corpo = _corpo(fonte, SIG_FRASE)
    if not corpo.rstrip().endswith("}"):
        viol.append("(1) o recorte de `FraseSustenance` nao fecha nas chaves — nao e o metodo inteiro")

    # (2) try/catch com queda para texto SEM numero (no PROPRIO catch, sem re-lancar)
    if "try" not in corpo:
        viol.append("(2) `FraseSustenance` sem `try` — a leitura de atributo pode derrubar a tooltip")
    if "catch (Exception" not in corpo:
        viol.append("(2) `FraseSustenance` sem `catch (Exception ...)`")
    else:
        i = corpo.find("catch (Exception")
        abertura = corpo.find("{", i)
        if abertura < 0:
            viol.append("(2) o `catch (Exception ...)` nao tem corpo no fonte")
        else:
            corpo_catch = _rec.bloco_que_contem(corpo, abertura)
            if 'return "";' not in corpo_catch:
                viol.append('(2) o `catch` NAO cai para o texto SEM numero (sem `return "";` no '
                            'proprio catch)')
            if "throw" in corpo_catch:
                viol.append("(2) o `catch` RE-LANCA — a tooltip quebra em vez de cair para SEM numero")

    # (3) GUARDA DE EXISTENCIA antes de QUALQUER leitura de atributo
    for nome, chamada, leitura in (("MaxHealth", CHAMADA_GUARDA_VIDA, LEITURA_VIDA),
                                   ("MaxMana", CHAMADA_GUARDA_MANA, LEITURA_MANA)):
        pos_guarda = corpo.find(chamada)
        pos_leitura = corpo.find(leitura)
        if pos_guarda < 0:
            viol.append("(3) sem guarda de existencia do atributo %s antes da leitura" % nome)
            continue
        if pos_leitura < 0:
            viol.append("(3) nao achei a leitura `%s`" % leitura)
            continue
        if pos_guarda > pos_leitura:
            viol.append("(3) a guarda de %s roda DEPOIS da leitura (o indexador ja lancou)" % nome)

    if SIG_ATRIBUTO not in fonte:
        viol.append("(3) sem `AtributoExiste(Character, string)` — o guard nao existe")
    else:
        g = _corpo(fonte, SIG_ATRIBUTO)
        if "GetAttribute(nome)" not in g or "GetVariableAttribute(nome)" not in g:
            viol.append("(3) `AtributoExiste` nao usa as consultas que devolvem null do jogo "
                        "(`GetAttribute`/`GetVariableAttribute`)")
        if "this[" in g:
            viol.append("(3) `AtributoExiste` INDEXA o personagem — voltaria a lancar "
                        "(a guarda tem de vir antes do indexador)")

    # (4) alvo nulo / fora de contexto de jogador
    if ALVO_NULO not in corpo:
        viol.append("(4) sem o tratamento de alvo nulo (`if (personagem == null)`)")
    elif corpo.find(ALVO_NULO) > corpo.find(LEITURA_VIDA):
        viol.append("(4) o tratamento de alvo nulo roda DEPOIS da leitura do atributo")

    # (5) NUNCA somar tier I com tier II a mao
    codigo = _rec.codigo_efetivo(fonte)
    if "List<SkillInfo> skills = personagem.Skills;" not in codigo:
        viol.append("(5) as tiers nao vem da lista ATIVA do jogo (`Character.Skills`)")
    if "pct += daSkill;" not in codigo:
        viol.append("(5) a % nao e acumulada do que o jogo tem ativo (`pct += daSkill;`)")
    if "PrefixoSustenance" not in codigo or "float.TryParse" not in codigo:
        viol.append("(5) a % nao e lida da DESCRICAO do asset (`PrefixoSustenance` + `TryParse`)")
    if "vida * pct / 100f" not in codigo or "mana * pct / 100f" not in codigo:
        viol.append("(5) a conta nao usa a % lida do jogo (`vida/mana * pct / 100f`)")
    if '"Sustenance' in codigo:
        viol.append("(5) o fonte crava nome de tier em literal (tabela de tiers do mod)")
    if "if (pct <= 0f || tiers.Count == 0)" not in codigo:
        viol.append("(5) sem a queda para SEM numero quando nenhuma tier esta ativa")

    return viol


def iscas():
    """A ISCA EMBUTIDA: (nome, fonte com o defeito, o que a checagem tem de morder)."""
    fonte = le_fonte()

    # (A) sem a guarda de existencia: a leitura volta a poder lancar no indexador
    sem_guarda = _apaga_if_da_guarda(fonte)

    # (B) soma a mao (o defeito classico do projeto): 8 + 20 = 28 no lugar do que o jogo tem ativo
    soma_a_mao = fonte.replace("pct += daSkill;", "pct += 8f + 20f;")

    # (C) o catch re-lanca em vez de cair para o texto SEM numero
    re_throw = fonte.replace('catch (Exception ex)\n',
                             'catch (Exception ex)\n        {\n            throw ex;\n        }\n'
                             '        if (false)\n', 1)

    # (D) a propria guarda indexa o personagem (lanca em vez de responder)
    guarda_que_lanca = fonte.replace("if (jogo.GetAttribute(nome) != null)",
                                     "if (personagem[nome] != 0f)", 1)
    guarda_que_lanca = guarda_que_lanca.replace("return jogo.GetVariableAttribute(nome) != null",
                                                "return personagem[nome] != 0f", 1)

    return (
        ("A: sem a guarda de existencia do atributo", sem_guarda, "a guarda antes da leitura"),
        ("B: soma a mao tier I + tier II (28)", soma_a_mao, "a % vem do que o jogo tem ativo"),
        ("C: o catch re-lanca (tooltip quebra)", re_throw, "a queda para o texto SEM numero"),
        ("D: a guarda indexa o personagem (lanca)", guarda_que_lanca, "o guard nao pode indexar"),
    )


def _apaga_if_da_guarda(fonte):
    """Tira o `if (!AtributoExiste(...)) { ... }` INTEIRO (corpo inclusive), por casamento de chaves."""
    i = fonte.find('if (!AtributoExiste(personagem, "MaxHealth")')
    if i < 0:
        return fonte
    abertura = fonte.find("{", i)
    if abertura < 0:
        return fonte
    bloco = _rec.bloco_que_contem(fonte, abertura)       # o `{ ... }` do proprio `if`
    fim = fonte.find(bloco, abertura) + len(bloco)
    return fonte[:i] + fonte[fim:]


# --------------------------------------------------------------------------- #
# A MATRIZ de aceite (o exemplo do dono: personagem com 100 de vida e 200 de mana)
# --------------------------------------------------------------------------- #

VIDA_DO_DONO = 100
MANA_DO_DONO = 200


def matriz():
    """As linhas numericas do aceite — (cenario, tiers ativas, vida, mana, pct, health, mana).

    Cenario 1 (sem Sustenance -> tooltip sem numero) e cenario 5 (vida/mana mudando -> o numero
    acompanha) sao de TELA e ficam na conferencia humana; o caminho reprodutivel dos dois esta na
    docstring do teste da suite e em `docs/cobertura/rv28-globules.md` §11.
    """
    acoes = pct_das_acoes()
    linhas = []
    for cenario, tiers in ((2, ["Sustenance I"]),
                           (3, ["Sustenance II"]),
                           (4, ["Sustenance I"]),
                           (4, ["Sustenance II"])):
        pct = pct_das_tiers(tiers, acoes)
        h, m = cura(VIDA_DO_DONO, MANA_DO_DONO, pct)
        linhas.append({"cenario": cenario, "tiers": tiers, "vida": VIDA_DO_DONO,
                       "mana": MANA_DO_DONO, "pct": pct, "health": h, "mana_exibida": m})
    return linhas


def violacoes_da_isca(nome_da_isca):
    """As violacoes que a checagem aponta na fonte com o defeito `nome_da_isca` plantado.

    E o que a contra-prova usa: a isca acredita que o defeito esta limpo (a lista tem de vir
    VAZIA) e por isso REPROVA; a metade OK usa o fonte vivo.
    """
    for nome, fonte_defeituosa, _ in iscas():
        if nome == nome_da_isca:
            return guardas_do_globule(fonte_defeituosa)
    raise arc.Falhou("isca desconhecida: %r" % nome_da_isca)


def caso_globule_aut6(caminho=CASOS_AUT6):
    """O caso `S-rv28-globule-sustenance` do avaliador AUT-6 (o cenario DECLARADO por ele).

    Devolve {nome_do_personagem: {"max_health": ..., "max_mana": ..., "tiers": [...]}} — e a
    declaracao do pool, sem a qual a frase (que carrega o numero) nao pode ser conferida.
    """
    import json
    with open(caminho, encoding="utf-8") as fh:
        doc = json.load(fh)
    for caso in doc.get("casos") or []:
        if caso.get("id") == "S-rv28-globule-sustenance":
            return {p["nome"]: {"max_health": p.get("max_health"), "max_mana": p.get("max_mana"),
                                "tiers": list(p.get("tiers") or [])}
                    for p in caso.get("personagens") or []}
    return {}


def linhas_da_fixture_aut6(caminho=FIXTURE_AUT6):
    """As linhas `[Globule RV-28]` da fixture do avaliador AUT-6 (material ja aceito pelo harness).

    Devolve [{char, tiers, pct, health, mana, chave}]. E a PONTE com o harness: o modelo desta
    biblioteca tem de concordar com o que o avaliador aceitou.
    """
    re_linha = re.compile(
        r"\[Globule RV-28\]\s*'(?P<chave>[^']+)':\s*(?P<char>\S+)\s+(?P<tiers>.+?)\s*=\s*"
        r"(?P<pct>\d+(?:\.\d+)?)%\s*->.*?:\s*(?P<h>\d+(?:\.\d+)?)\s+health and\s+"
        r"(?P<m>\d+(?:\.\d+)?)\s+mana")
    linhas = []
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            m = re_linha.search(linha)
            if m:
                linhas.append({
                    "chave": m.group("chave"),
                    "char": m.group("char"),
                    "tiers": [t.strip() for t in re.split(r"\s+and\s+", m.group("tiers").strip())],
                    "pct": float(m.group("pct")),
                    "health": m.group("h"),
                    "mana": m.group("m"),
                })
    return linhas
