#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BT-18 — o patch das passivas de inimigo (`PassivaInimigoPatch`): a tabela da Onda 1, a
nota idempotente, os DOIS ganchos e o placeholder do Redemptive (Onda 2).

O QUE ESTE TESTE PRENDE (e por que existe)
-----------------------------------------
A BT-18 e a primeira familia de texto do mod cujo valor NAO sai de uma tabela de NUMERO
pronto: os passivos de inimigo nao tem valor no enum nem na descricao (relatorio
`docs/cobertura/revisao/BT-18-passivas-inimigo.md`, §0/§1). O que da para fazer com dado
provado e anexar CONTEXTO (as condicoes do gatilho, §10.2) e, num caso, o numero que a
PROPRIA localizacao do jogo traz (§10.4); o `Redemptive` nao tem numero em lugar nenhum (§5)
e fica no PLACEHOLDER documentado, a preencher apos medicao em jogo. Este teste trava:

  1. A TABELA da Onda 1 — as QUATRO descricoes exibidas cobertas, as notas SEM eco (o mesmo
     criterio do `tools/check_notas_redundantes.py`, >= 6 palavras em sequencia) e SEM chave
     duplicada (um `Dictionary` C# estoura com chave repetida — a familia do INC-1). Toda nota
     que traz NUMERO tem de ter a procedencia (as condicoes do gatilho §10.2 / a localizacao do
     jogo §10.4) no comentario da PROPRIA entrada.
  2. A NOTA IDEMPOTENTE — `TentaAnexar` devolve null quando a nota JA esta no texto: e o que
     permite os DOIS ganchos (Localize + ShowUniversalTooltip) rodarem para a MESMA descricao
     sem duplicar.
  3. Os DOIS GANCHOS — alvo declarado por TIPO (nunca `__N`), parametro por NOME, protegidos
     por try/catch, e a nota no bloco do NIVEL 2 (marcador `#C8B090`).
  4. O PLACEHOLDER do Redemptive (Onda 2) — a tabela `ValoresPendentesDeMedicao` EXISTE,
     marcada, com o valor ainda `null` (= NAO medido) e um TODO: nenhum numero inventado.
  5. A ISCA — cada checagem e vista REPROVANDO sobre uma copia mutada em MEMORIA (um teste
     que nunca falhou nao e teste, e decoracao).

NAO executa o C# do mod (isso pediria a `lib/` do jogo): o modelo em Python espelha a REGRA
de anexo e a checagem ESTRUTURAL do fonte e quem amarra os dois.
"""
import os
import re
import sys

import arcabouco as arc

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import tabelas as _tab                    # noqa: E402  o parser UNICO das tabelas do mod
import check_notas_redundantes as _ckn    # noqa: E402  o criterio de ECO do projeto
import recorte as _rec                    # noqa: E402  o recorte ESTRUTURAL de fonte

META = {
    "nome": "bt18-passivas-inimigo",
    "categoria": "pura",
    "requer": [],
    "descricao": ("BT-18: a tabela da Onda 1 (4 descricoes de EnemyMod, notas sem eco e sem "
                  "chave duplicada, numero sempre com procedencia no comentario), a nota "
                  "IDEMPOTENTE (dois ganchos, sem duplicar), os ganchos por TIPO/por NOME com "
                  "try/catch e a nota no bloco do nivel 2, e o PLACEHOLDER do Redemptive "
                  "(valor ainda null, TODO) — sem numero digitado a mao"),
}

FONTE = os.path.join("BetterTooltips", "Patches", "PassivaInimigoPatch.cs")

# As QUATRO descricoes exibidas da Onda 1 (o texto EXATO do campo `description` do asset,
# copiado do relatorio BT-18 §4.2 — a chave do tooltip). Se a cobertura mudar, este conjunto
# muda DE PROPOSITO (o teste E a lista).
DESCRICOES_ONDA1 = {
    "Regenerates health every turn.",
    "Teleports randomly when struck",
    "Applies Curse on striking and when struck",
    "Gains increased damage for each ally killed",
}

NOME_MOD_REDEMPTIVE = "Redemptive"
DESCRICAO_REDEMPTIVE = "Heals allies on death"
MIN_PALAVRAS_ECO = _ckn.MIN_PALAVRAS_ECO

PROCEDENCIA = ("\u00a710", "PROCEDENCIA", "localizacao")   # §10.x / a palavra / a fonte


# ------------------------------------------------------------------ leitura do fonte

def _le(caminho_rel):
    with open(os.path.join(arc.raiz_do_repo(), caminho_rel), encoding="utf-8") as fh:
        return fh.read()


def _entradas(fonte, nome_tabela):
    """(linha, comentario, chave, valor) de TODAS as entradas da tabela `nome_tabela`."""
    bloco, k = _tab.bloco(fonte, nome_tabela)
    return _tab.entradas(bloco, fonte[:k].count("\n") + 1)


def _comentario_da_entrada(fonte, chave):
    """O bloco de comentario IMEDIATAMENTE ACIMA da linha do `{` da entrada da `chave`.

    Lido por LINHA (nao pelo `comentario` do parser): o `entradas()` do `tabelas.py` consome
    os comentarios antes do `{` da TABELA, entao o comentario da PRIMEIRA entrada nao chega
    nele. Aqui a ancoragem e a linha que contem o literal da chave.
    """
    i = fonte.find('"' + chave + '"')
    arc.exigir(i >= 0, "nao achei a chave %r no fonte" % chave)
    inicio_linha = fonte.rfind("\n", 0, i) + 1
    coleta = []
    for linha in reversed(fonte[:inicio_linha].split("\n")):
        t = linha.strip()
        if not t:
            continue
        if t.startswith("//"):
            coleta.append(t)
            continue
        break
    return " ".join(reversed(coleta))


def _corpo_metodo(fonte, assinatura):
    """O corpo do metodo por CASAMENTO DE CHAVES (nunca por janela de caracteres)."""
    return _rec.corpo_do_metodo(fonte, assinatura)


# ---------------------------------------------------------------- checagens (acumulam)

def _checa_tabela(fonte, falhas):
    """1. A tabela da Onda 1: chaves exatas, notas sem eco e numero com procedencia."""
    try:
        entradas = _entradas(fonte, "NotasPorDescricao")
    except ValueError as erro:
        falhas.append("ESTRUTURA: nao achei a tabela `NotasPorDescricao` (%s)" % erro)
        return
    chaves = [c for _l, _com, c, _v in entradas]
    if len(chaves) != len(set(chaves)):
        repetidas = sorted({c for c in chaves if chaves.count(c) > 1})
        falhas.append("CHAVE DUPLICADA na tabela (o Dictionary C# estoura no construtor "
                      "estatico): %s" % repetidas)
    if set(chaves) != DESCRICOES_ONDA1:
        falhas.append("a cobertura da Onda 1 mudou: esperava %d descricoes, achei %d "
                      "(faltando=%s; sobrando=%s)"
                      % (len(DESCRICOES_ONDA1), len(set(chaves)),
                         sorted(DESCRICOES_ONDA1 - set(chaves)),
                         sorted(set(chaves) - DESCRICOES_ONDA1)))
    for linha, _com, chave, valor in entradas:
        if not valor.strip():
            falhas.append("l.%d: nota VAZIA para %r" % (linha, chave[:60]))
            continue
        # ECO (mesmo criterio do RV-15): a nota que repete o texto nao acrescenta nada.
        n = _ckn.maior_sequencia_comum(_ckn.desmarca(valor), _ckn.desmarca(chave))
        if n >= MIN_PALAVRAS_ECO:
            falhas.append("l.%d: a nota ECOa %d palavras da descricao: %r"
                          % (linha, n, valor[:70]))
        # PROCEDENCIA: toda nota com digito tem de ter a prova no comentario da entrada.
        if re.search(r"\d", valor):
            junto = _comentario_da_entrada(fonte, chave)
            if not any(p in junto for p in PROCEDENCIA):
                falhas.append("l.%d: a nota %r tem NUMERO sem procedencia no comentario da "
                              "entrada (marque §10.x / PROCEDENCIA / localizacao)"
                              % (linha, valor[:60]))


def _checa_idempotencia(fonte, falhas):
    """2. `TentaAnexar` devolve null quando a nota JA esta no texto (o guarda do IndexOf)."""
    if not re.search(r"textoExibido\.IndexOf\(\s*nota\s*,\s*StringComparison\.Ordinal\s*\)"
                     r"\s*>=\s*0", fonte):
        falhas.append("FAIL-SAFE: `TentaAnexar` nao confere se a nota JA esta no texto "
                      "(`IndexOf(nota, StringComparison.Ordinal) >= 0`) — os dois ganchos "
                      "duplicariam")
    m = re.search(r"if\s*\(\s*textoExibido\.IndexOf\([^)]*\)\s*>=\s*0\s*\)\s*\{(.*?)\}", fonte, re.S)
    if not m or "return null;" not in m.group(1):
        falhas.append("FAIL-SAFE: o ramo 'nota ja anexada' tem de devolver null (nada escrito)")


def _checa_ganchos(fonte, falhas):
    """3. Os dois ganchos: alvo por TIPO, parametro por NOME, try/catch, nivel 2."""
    if not re.search(r"\[HarmonyPatch\(typeof\(OptionsManager\),\s*"
                     r"nameof\(OptionsManager\.Localize\)\)\]", fonte):
        falhas.append("GANCHO A: falta o postfix em `OptionsManager.Localize` (o funil)")
    if not re.search(r"\[HarmonyPatch\(typeof\(Tooltip\),\s*"
                     r"nameof\(Tooltip\.ShowUniversalTooltip\),\s*new Type\[\]", fonte):
        falhas.append("GANCHO B: falta o postfix em `Tooltip.ShowUniversalTooltip` com a "
                      "assinatura por TIPO (`new Type[]`)")
    if not re.search(r"private static void Postfix\(string original, ref string __result\)", fonte):
        falhas.append("GANCHO A: o postfix tem de receber o parametro por NOME "
                      "(`string original, ref string __result`)")
    if not re.search(r"private static void Postfix\(ref string description\)", fonte):
        falhas.append("GANCHO B: o postfix tem de receber `ref string description` (por NOME)")
    if re.search(r"__\d+\b", _rec.codigo_efetivo(fonte)):
        falhas.append("POSICIONAL: o patch declara um parametro `__N` do Harmony (proibido)")
    for rotulo, assinatura in (("A", "private static void Postfix(string original, ref string __result)"),
                               ("B", "private static void Postfix(ref string description)")):
        try:
            corpo = _corpo_metodo(fonte, assinatura)
        except arc.Falhou as erro:
            falhas.append("GANCHO %s: nao recortei o corpo (%s)" % (rotulo, erro))
            continue
        if "try" not in corpo or "catch" not in corpo:
            falhas.append("GANCHO %s: o postfix tem de estar em try/catch (gancho quente)" % rotulo)
    if "LocalizePatch.MarcadorCorDeExplicacao" not in fonte:
        falhas.append("COR: a nota nao usa o marcador do nivel 2 (`LocalizePatch."
                      "MarcadorCorDeExplicacao`) — sai no tom do corpo do tooltip")


def _checa_placeholder(fonte, falhas):
    """4. O placeholder do Redemptive: tabela marcada, valor null (= nao medido) e TODO."""
    if not re.search(r'NomeModRedemptive\s*=\s*"Redemptive"', fonte):
        falhas.append("ONDA 2: falta a identidade do mod (`NomeModRedemptive = \"Redemptive\"`)")
    if not re.search(r'DescricaoRedemptive\s*=\s*"Heals allies on death"', fonte):
        falhas.append("ONDA 2: falta a descricao exibida do Redemptive (a chave do tooltip)")
    if not re.search(r"ValoresPendentesDeMedicao\s*=\s*new Dictionary", fonte):
        falhas.append("ONDA 2: falta a tabela de PLACEHOLDER `ValoresPendentesDeMedicao`")
    if "TODO(BT-18)" not in fonte:
        falhas.append("ONDA 2: o placeholder tem de estar MARCADO (`TODO(BT-18)`) para o valor "
                      "ser preenchido apos medicao em jogo")
    if not re.search(r"\{\s*NomeModRedemptive\s*,\s*null\s*\}", fonte):
        falhas.append("ONDA 2: a entrada do Redemptive no placeholder tem de estar em `null` "
                      "enquanto o valor NAO for medido em jogo (nada de numero inventado)")
    if "skillTriggers" not in fonte or ".Actions" not in fonte:
        falhas.append("ONDA 2: a resolucao tem de ler o gatilho do asset "
                      "(`skillTriggers` -> `.Actions`)")


# ------------------------------------------------------------------------- iscas

def _iscas(fonte):
    """(rotulo, fonte_mutada, checagem, marca) — cada defeito numa COPIA EM MEMORIA."""
    iscas = []

    # (1) CHAVE DUPLICADA na tabela (a familia do INC-1).
    alvo = '{ "Regenerates health every turn.",'
    if fonte.count(alvo) == 1:
        iscas.append(("chave-duplicada",
                      fonte.replace(alvo, '{ "Teleports randomly when struck",', 1),
                      _checa_tabela, "CHAVE DUPLICADA"))

    # (2) Nota que ECOA a descricao (>= 6 palavras em sequencia) — a familia do RV-15.
    alvo = '"Only harmful abilities apply it, and only while the target does not already have Curse."'
    if fonte.count(alvo) == 1:
        iscas.append(("nota-ecoando",
                      fonte.replace(alvo, '"Applies Curse on striking and when struck, always."', 1),
                      _checa_tabela, "ECOa"))

    # (3) NUMERO sem procedencia: tira §10.x / PROCEDENCIA / localizacao de TODO o fonte.
    sem_proc = (re.sub(r"\u00a710\.\d", "", fonte)
                .replace("PROCEDENCIA", "").replace("localizacao", ""))
    if sem_proc != fonte:
        iscas.append(("numero-sem-procedencia", sem_proc, _checa_tabela, "sem procedencia"))

    # (4) O guarda de idempotencia some.
    alvo = 'if (textoExibido.IndexOf(nota, StringComparison.Ordinal) >= 0)'
    if fonte.count(alvo) == 1:
        iscas.append(("sem-idempotencia",
                      fonte.replace(alvo, "if (false)", 1),
                      _checa_idempotencia, "IndexOf"))

    # (5) O alvo do gancho B perde a assinatura por TIPO.
    alvo = '[HarmonyPatch(typeof(Tooltip), nameof(Tooltip.ShowUniversalTooltip), new Type[]'
    if fonte.count(alvo) == 1:
        iscas.append(("gancho-sem-tipo",
                      fonte.replace(alvo,
                                    '[HarmonyPatch(typeof(Tooltip), nameof(Tooltip.ShowUniversalTooltip)'),
                      _checa_ganchos, "assinatura por TIPO"))

    # (6) O placeholder do Redemptive deixa de estar em `null` (numero inventado).
    alvo = "{ NomeModRedemptive, null }"
    if fonte.count(alvo) == 1:
        iscas.append(("placeholder-com-numero",
                      fonte.replace(alvo, '{ NomeModRedemptive, "Heals allies for 50 on death." }', 1),
                      _checa_placeholder, "medido"))

    return iscas


def _anexa(texto, nota, marcador="C8B090"):
    """ESPELHO da ultima linha de `TentaAnexar`: TrimEnd + linha em branco + bloco do nivel 2.
    Devolve None quando nao ha nota OU quando ela JA esta no texto (idempotencia)."""
    if not nota:
        return None
    if nota in texto:
        return None
    return texto.rstrip() + "\n\n<color=#%s>%s</color>" % (marcador, nota)


# -------------------------------------------------------------------------- teste

def corpo():
    fonte = _le(FONTE)
    arc.exigir(len(fonte) > 3000, "o %s veio curto/vazio: a leitura mudou de lugar?" % FONTE)

    # 1..4 — as checagens no fonte VIVO.
    falhas = []
    _checa_tabela(fonte, falhas)
    _checa_idempotencia(fonte, falhas)
    _checa_ganchos(fonte, falhas)
    _checa_placeholder(fonte, falhas)
    arc.exigir(not falhas,
               "o PassivaInimigoPatch regrediu em %d ponto(s):\n  - %s"
               % (len(falhas), "\n  - ".join(falhas)))

    # 5 — as iscas: cada checagem TEM de reprovar pela marca certa.
    iscas = _iscas(fonte)
    esperado = {"chave-duplicada", "nota-ecoando", "numero-sem-procedencia", "sem-idempotencia",
                "gancho-sem-tipo", "placeholder-com-numero"}
    arc.exigir({r for r, _f, _c, _m in iscas} >= esperado,
               "faltou isca embutida: as ancoras do plantio nao acharam o trecho (%s)"
               % ", ".join(sorted(r for r, _f, _c, _m in iscas)))
    for rotulo, mutada, checagem, marca in iscas:
        fs = []
        checagem(mutada, fs)
        arc.exigir(fs, "o defeito plantado '%s' PASSOU pela checagem (ela nao pega a classe)"
                   % rotulo)
        arc.exigir(any(marca in x for x in fs),
                   "o defeito '%s' foi pego, mas nao por %r: %s"
                   % (rotulo, marca, " | ".join(fs)))

    # O MODELO da tabela: as 4 descricoes, e o anexo idempotente (a regra do C# transcrita).
    entradas = _entradas(fonte, "NotasPorDescricao")
    notas = {c: v for _l, _com, c, v in entradas}
    arc.igual(len(notas), 4, "a tabela da Onda 1 tem de ter as 4 descricoes")
    for chave, nota in notas.items():
        primeira = _anexa(chave, nota)
        if primeira is None:
            raise arc.Falhou("o anexo tem de montar o texto da descricao: %r" % chave[:50])
        arc.exigir(primeira.endswith("</color>"),
                   "o anexo tem de fechar o bloco do nivel 2: ...%r" % primeira[-60:])
        arc.igual(primeira.count(nota), 1, "o anexo escreve a nota UMA vez")
        arc.exigir(_anexa(primeira, nota) is None,
                   "a 2a passada com a nota JA no texto tem de devolver null (sem duplicar)")
    arc.exigir(_anexa("uma descricao qualquer", None) is None,
               "descricao fora da tabela nao pode receber nota")

    print("PassivaInimigoPatch: 0 falha(s) no fonte vivo; %d defeito(s) plantado(s) reprovam "
          "pela razao certa" % len(iscas))
    print("Onda 1: %d descricao(oes) de EnemyMod cobertas (%s); Onda 2: Redemptive com "
          "placeholder em null (a preencher apos medicao em jogo)"
          % (len(notas), "; ".join(sorted(notas))))


if __name__ == "__main__":
    arc.main(META, corpo)
