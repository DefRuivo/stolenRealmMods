#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BT-10 / BT-10F — o `Reaper's Toll` do BetterTooltips: FAIL-SAFE, PROCEDENCIA e FORMATO.

O QUE ESTE TESTE PRENDE (e por que existe)
------------------------------------------
O `ReaperTollPatch` (a BT-10, 01/10) e a unica familia de tooltip que NAO tinha teste
dedicado: a entrega passou por todas as travas, mas o fail-safe, o gatilho do gancho e a
procedencia do numero estavam provados SO POR LEITURA (a prova de fogo vive em `scratch/`,
que e gitignored). Este teste transforma aquela leitura em TRAVA executavel, em tres frentes:

  1. FAIL-SAFE — sem skill, sem percentual no asset, sem personagem em foco ou sem vida
     maxima, o patch NAO escreve nada e a linha do jogo fica INTACTA. E uma SEGUNDA passada
     com o texto JA MODIFICADO nao casa de novo: a identidade do gancho e a IGUALDADE EXATA
     contra a descricao do ASSET, entao o texto que ja carrega o valor deixa de ser candidato
     (se virasse "contem", a linha ganharia o `(... health for you)` DUAS vezes).

  2. PROCEDENCIA — o codigo le a PORCENTAGEM do asset (a descricao de `Game.Instance.Skills`),
     nunca de numero digitado; e le a VIDA MAXIMA do valor FINAL do motor (`Character.MaxHealth`,
     o mesmo `GetAttribute` que a formula do efeito usa), nunca do `SavedMap` puro. O teste
     REPROVA se alguem cravar um literal onde deveria ler o asset (ha a isca embutida disso).

  3. FORMATO — a BT-10F (01/10) arrumou o defeito `max health. (23.3 health for you)` (o ponto
     ficava NO MEIO da frase): a linha final termina em `).` e NUNCA tem `. (` no meio. Este
     teste e a trava que impede a regressao — ele monta o texto com o sufixo LIDO do fonte.

COMO ELE LE (FORMATO-3/FORMATO-7)
---------------------------------
NADA de numero de linha: o `LocalizePatch.cs` muda toda hora. O recorte e ESTRUTURAL
(`tools/testes/recorte.py`, casamento de chaves) e ancora em IDENTIFICADOR (assinatura de
metodo, nome de campo, literal de string). Onde a leitura cruza comentario, o texto passa por
`recorte.codigo_efetivo` primeiro (citacao em comentario nao e codigo).

O QUE ESTE TESTE NAO PROVA
--------------------------
Nao executa o C# do mod (isso exigiria a `lib/` do jogo e um harness por test). O modelo
transcrito em Python (as mesmas guardas e a mesma conta) e a ligacao entre o comportamento
esperado e o fonte vivo; o que amarra os dois e a checagem ESTRUTURAL do trecho. Ha ainda uma
isca EMBUTIDA por defeito: o proprio teste planta cada defeito numa COPIA em memoria do fonte
e exige que a checagem REPROVE pela razao certa — checagem que nunca foi vista reprovando
seria decoracao.
"""
import csv
import os
import re

import arcabouco as arc
import recorte as rec

META = {
    "nome": "bt10-reaper-toll",
    "categoria": "pura",
    "requer": [],
    "descricao": ("BT-10: o Reaper's Toll - o fail-safe nao escreve sem dado provado (e a 2a "
                  "passada nao duplica), a % vem do ASSET e a vida maxima do valor FINAL do "
                  "motor, e a linha termina em ').' sem '. (' no meio (trava da BT-10F)"),
}

FONTE_REAPER = os.path.join("BetterTooltips", "Patches", "ReaperTollPatch.cs")
FONTE_LOCALIZE = os.path.join("BetterTooltips", "Patches", "LocalizePatch.cs")
CSV_DAS_SKILLS = os.path.join("docs", "cobertura", "skills.csv")

# ------------------------------- ANCORAS (identificador, nunca linha) -----------------------

ASSINATURA_TENTA = "public static bool TentaMontar(string original, string linhaDoJogo,"
ASSINATURA_INSERE = "private static string InsereValorNaLinha(string linhaDoJogo, string valor)"
ASSINATURA_PCT = "private static float PercentualDaSkill(SkillInfo skill)"
ASSINATURA_LEPCT = "private static bool LePercentual(string descricao, out float pct)"
ASSINATURA_SKILL = "private static SkillInfo SkillDaReaperToll()"
ASSINATURA_MESMO = "private static bool MesmoTexto(string a, string b)"

# O call site no `AplicarNotasDoFunil` (LocalizePatch.cs). E a UNICA porta pela qual o valor
# sai: se `TentaMontar` devolver false, nada muda.
ANCORA_CHAMADA = ("if (ReaperTollPatch.TentaMontar(original, __result, out linhaComValor, "
                  "out notaDoCalculo))")

# A marca do nivel 1 do Reaper's Toll e a identidade do asset (uma STRING, nao um numero).
NOME_DA_SKILL = "Reaper's Toll"

# A vida maxima do personagem em foco e um DADO de cena (valor FINAL do motor). Aqui e a
# entrada de um cenario, nunca a constante de uma conta.
VIDA_MAXIMA_DE_CENA = 233.0


# ======================================================================= utilidades ====

def _le(caminho_rel):
    with open(os.path.join(arc.raiz_do_repo(), caminho_rel), encoding="utf-8") as fh:
        return fh.read()


def _exigir(falhas, condicao, mensagem):
    """Acumula (nao levanta) para que a isca embutida veja TODAS as falhas de uma vez."""
    if not condicao:
        falhas.append(mensagem)


def _corpo(codigo, assinatura, marcas, falhas, rotulo):
    """O corpo inteiro do metodo, por casamento de chaves; sem ele, a falha e do teste."""
    try:
        bloco = rec.corpo_do_metodo(codigo, assinatura)
        rec.exigir_metodo_inteiro(bloco, assinatura, marcas=marcas)
        return bloco
    except arc.Falhou as erro:
        falhas.append("ESTRUTURA (%s): %s" % (rotulo, erro))
        return ""


def _descricao_do_asset():
    """A descricao da skill `Reaper's Toll` na tabela VERSIONADA do repositorio.

    A procedencia e a tabela `docs/cobertura/skills.csv` (a leitura do asset, com o campo
    `nome` casando por IDENTIDADE). Na pratica e ela que o motor carrega em
    `Game.Instance.Skills`; o teste a usa como o texto de onde a % tem de ser lida.
    """
    with open(os.path.join(arc.raiz_do_repo(), CSV_DAS_SKILLS), encoding="utf-8", newline="") as fh:
        for linha in csv.DictReader(fh):
            if (linha.get("nome") or "").strip() == NOME_DA_SKILL:
                return (linha.get("descricao") or "").strip()
    raise arc.Falhou("nao achei a skill %r em %s" % (NOME_DA_SKILL, CSV_DAS_SKILLS))


# ================================================================= modelo transcrito ====
# As funcoes abaixo TRANSCREVEM o C# do `ReaperTollPatch` (mesmas guardas, mesma conta, mesma
# formatacao). Quem prende as duas pontas e a checagem estrutural: o modelo diz o que a regra
# FAZ, a estrutura diz que o fonte vivo AINDA e essa regra.

def le_percentual(descricao):
    """ESPELHO do `LePercentual`: o PRIMEIRO `%` da descricao do ASSET, com `,` como decimal."""
    if not descricao:
        return 0.0
    fim = descricao.find("%")
    if fim < 0:
        return 0.0
    ini = fim
    while ini > 0:
        c = descricao[ini - 1]
        if c.isdigit() or c in ".,":
            ini -= 1
            continue
        break
    if ini >= fim:
        return 0.0
    numero = descricao[ini:fim].replace(",", ".")
    try:
        return float(numero)
    except ValueError:
        return 0.0


def mesmo_texto(a, b):
    """ESPELHO do `MesmoTexto`: IGUALDADE EXATA (apos aparar as pontas), nunca `Contains`."""
    return bool(a) and bool(b) and a.strip() == b.strip()


def formata_0_1(x):
    """ESPELHO do `ToString("0.#", InvariantCulture)`: ate uma casa, sem `.0` a toa."""
    texto = "%.1f" % x
    return texto[:-2] if texto.endswith(".0") else texto


def _sufixo_do_fonte(insere, cor, valor):
    """O sufixo LIDO do C# (`string sufixo = ...;`), com a cor e o valor substituidos.

    Nao ha sufixo digitado no teste: a montagem sai da expressao do fonte. Se a forma mudar
    (por exemplo o `(` passar para depois do ponto — o defeito da BT-10F), o texto montado
    aqui muda junto e as assercoes de FORMATO acusam.
    """
    achado = re.search(r"string\s+sufixo\s*=\s*(.+?);", insere, re.S)
    if not achado:
        raise arc.Falhou("nao achei `string sufixo = ...;` no corpo do InsereValorNaLinha")
    partes = []
    for termo in achado.group(1).split("+"):
        termo = termo.strip()
        if termo == "CorDoValorDoMotor":
            partes.append(cor)
        elif termo == "valor":
            partes.append(valor)
        elif termo.startswith('"') and termo.endswith('"') and len(termo) >= 2:
            partes.append(termo[1:-1])
        else:
            raise arc.Falhou("termo inesperado na montagem do sufixo: %r" % (termo,))
    return "".join(partes)


def _ramo_do_ponto(insere):
    """(ramo_remove, fallback) do `InsereValorNaLinha`, por CASAMENTO DE CHAVES.

    `ramo_remove` e verdadeiro quando o ramo do ponto FINAL tira o ponto antes de anexar o
    sufixo (`corpo.Substring(0, corpo.Length - 1) + sufixo + "."`) — e ele que impede o
    `. (` no meio. `fallback` e o `return corpo + sufixo + ".";` de quando a linha nao
    termina em ponto.
    """
    i_if = insere.find("if (")
    if i_if < 0:
        raise arc.Falhou("nao achei o `if` do ponto final no InsereValorNaLinha")
    faixa = rec.faixa_bloco_apos(insere, i_if)
    bloco = rec.texto_da_faixa(insere, faixa)
    depois = insere[faixa[1] + 1:]
    ramo_remove = ("Substring(0, corpo.Length - 1)" in bloco) and ("sufixo" in bloco)
    fallback = re.search(r'return\s+corpo\s*\+\s*sufixo\s*\+\s*"\."\s*;', depois) is not None
    return ramo_remove, fallback


def insere_valor(linha, valor, sufixo_fn, ramo_remove):
    """ESPELHO do `InsereValorNaLinha`: tira o ponto final (quando ha o ramo) e ancora o
    sufixo ANTES de fechar a frase, sempre terminando em `).`."""
    corpo = (linha or "").rstrip()
    if ramo_remove and corpo.endswith("."):
        corpo = corpo[:-1]
    return corpo + sufixo_fn(valor) + "."


def tenta_montar(original, linha_do_jogo, descricao, pct, vida, sufixo_fn, ramo_remove,
                 igualdade=mesmo_texto):
    """ESPELHO do `TentaMontar`, na MESMA ordem das guardas do C#.

    `descricao` e a descricao do asset (None = a skill nao esta carregada); `vida` e a vida
    maxima FINAL do personagem em foco (None = nenhum personagem; <= 0 = personagem sem vida
    maxima). A `igualdade` e um parametro para a ISCA embutida poder plantar o defeito da
    guarda de identidade (a comparacao frouxa que duplicaria).
    """
    if descricao is None or not igualdade(descricao, original):
        return False, linha_do_jogo
    if not (pct > 0):
        return False, linha_do_jogo
    if vida is None or not (vida > 0):
        return False, linha_do_jogo
    valor = formata_0_1(vida * pct / 100.0)
    return True, insere_valor(linha_do_jogo, valor, sufixo_fn, ramo_remove)


# ================================================================= checagem do FONTE ====

def _checa_fonte(cod_rt, cod_lp, falhas):
    """TODAS as checagens estruturais. Acumula em `falhas`; nunca levanta por dado do fonte."""
    efetivo_rt = rec.codigo_efetivo(cod_rt)
    efetivo_lp = rec.codigo_efetivo(cod_lp)

    # ---------------------------------------------------------------- identidade / asset
    _exigir(falhas, re.search(r'NomeDaSkill\s*=\s*"%s"' % re.escape(NOME_DA_SKILL), efetivo_rt),
            "PROCEDENCIA: a identidade do asset (`NomeDaSkill = \"%s\"`) sumiu" % NOME_DA_SKILL)
    _exigir(falhas, re.search(r"Game\.Instance\.Skills", efetivo_rt),
            "PROCEDENCIA: a skill tem de sair da lista CARREGADA do jogo (`Game.Instance.Skills`)")

    # O gancho so age sob a descricao EXATA do asset: `original` e a entrada (antes do mod).
    _exigir(falhas, re.search(
        r"if\s*\(\s*skill\s*==\s*null\s*\|\|\s*!MesmoTexto\s*\(\s*skill\.Description\s*,\s*"
        r"original\s*\)\s*\)", efetivo_rt),
        "FAIL-SAFE: a porta de entrada tem de ser `skill == null || !MesmoTexto("
        "skill.Description, original)` — comparando a descricao do ASSET com a ENTRADA "
        "(`original`), nunca com a saida (`__result`/`linhaDoJogo`)")

    # ---------------------------------------------------------------- a % vem do ASSET
    tenta = _corpo(efetivo_rt, ASSINATURA_TENTA, ("catch (Exception ex)", "return false;"),
                   falhas, "TentaMontar")
    if tenta:
        _exigir(falhas, re.search(
            r"float\s+pct\s*=\s*PercentualDaSkill\s*\(\s*skill\s*\)\s*;", tenta),
            "PROCEDENCIA: a % tem de ser LIDA (`float pct = PercentualDaSkill(skill);`); um "
            "numero fixo onde deveria ler o asset e exatamente o defeito que este teste pega")
        _exigir(falhas, not re.search(r"(?<![\w.])pct\s*=\s*-?\d", tenta),
                "PROCEDENCIA: ha um literal numerico atribuido a `pct` no lugar da leitura do asset")
        pct = _corpo(efetivo_rt, ASSINATURA_PCT, ("return _pct;",), falhas, "PercentualDaSkill")
        _exigir(falhas, re.search(r"LePercentual\s*\(\s*skill\.Description\s*,", pct),
                "PROCEDENCIA: `PercentualDaSkill` tem de ler `skill.Description` (a descricao "
                "do ASSET carregado)")
        lepct = _corpo(efetivo_rt, ASSINATURA_LEPCT, ("TryParse",), falhas, "LePercentual")
        _exigir(falhas, re.search(r"descricao\.IndexOf\('%'\)", lepct),
                "PROCEDENCIA: `LePercentual` tem de achar o `%` NA DESCRICAO (`descricao.IndexOf('%')`)")
        _exigir(falhas, "float.TryParse(" in lepct,
                "PROCEDENCIA: `LePercentual` tem de converter o numero lido (`float.TryParse`)")
        skill = _corpo(efetivo_rt, ASSINATURA_SKILL, ("return null;",), falhas, "SkillDaReaperToll")
        _exigir(falhas, re.search(
            r"string\.Equals\s*\(\s*skill\.SkillName\s*,\s*NomeDaSkill\s*,", skill),
            "PROCEDENCIA: a skill tem de ser achada por `SkillName` == `NomeDaSkill` (identidade)")

    # ---------------------------------------------------------------- vida = valor FINAL
    if tenta:
        _exigir(falhas, re.search(r"float\s+vida\s*=\s*personagem\.MaxHealth\s*;", tenta),
                "PROCEDENCIA: a vida maxima tem de ser a propriedade do MOTOR "
                "(`personagem.MaxHealth`, o valor FINAL via `GetAttribute`)")
        _exigir(falhas, "SavedMap" not in tenta,
                "PROCEDENCIA: o `TentaMontar` nao pode ler o `SavedMap` (o valor PURO de pontos "
                "investidos): a cura do jogo usa o valor FINAL")
        _exigir(falhas, re.search(
            r"Character\s+personagem\s*=\s*ShrineAuraPatch\.ReceptorDaTooltip\s*\(\s*\)\s*;", tenta),
            "FAIL-SAFE: o personagem tem de ser o RECEPTOR da tooltip "
            "(`ShrineAuraPatch.ReceptorDaTooltip()`)")

    # ---------------------------------------------------------------- FAIL-SAFE (guardas)
    if tenta:
        # `null` na inicializacao: se qualquer guarda cair, o que sai e null (nada escrito).
        _exigir(falhas, tenta.count("linhaComValor = null;") >= 2,
                "FAIL-SAFE: sao DOIS os `linhaComValor = null;` (a inicializacao e o catch) — "
                "sem a inicializacao, um ramo de saida devolveria lixo")
        _exigir(falhas, re.search(r"linhaComValor\s*=\s*null\s*;\s*nota\s*=\s*null\s*;", tenta),
                "FAIL-SAFE: `linhaComValor`/`nota` tem de comecar nulos")
        _exigir(falhas, re.search(r"if\s*\(\s*pct\s*<=\s*0f\s*\)\s*\{[^}]*return\s+false\s*;", tenta, re.S),
                "FAIL-SAFE: sem percentual (`pct <= 0f`) o patch tem de sair sem escrever")
        _exigir(falhas, re.search(r"if\s*\(\s*personagem\s*==\s*null\s*\)\s*\{[^}]*return\s+false\s*;",
                                  tenta, re.S),
                "FAIL-SAFE: sem personagem em foco o patch tem de sair sem escrever")
        _exigir(falhas, re.search(r"if\s*\(\s*vida\s*<=\s*0f\s*\)\s*\{[^}]*return\s+false\s*;",
                                  tenta, re.S),
                "FAIL-SAFE: sem vida maxima (`vida <= 0f`) o patch tem de sair sem escrever")
        try:
            catch = rec.bloco_apos(tenta, tenta.index("catch (Exception ex)"))
            _exigir(falhas, "linhaComValor = null;" in catch and "nota = null;" in catch,
                    "FAIL-SAFE: o catch tambem tem de zerar a saida (excecao = linha intacta)")
        except (arc.Falhou, ValueError):
            falhas.append("FAIL-SAFE: nao achei o `catch` do `TentaMontar`")

    # ---------------------------------------------------------------- o CALL SITE
    try:
        i_if = efetivo_lp.index(ANCORA_CHAMADA)
        bloco = rec.bloco_apos(efetivo_lp, i_if)
        _exigir(falhas, "__result = linhaComValor;" in bloco,
                "FAIL-SAFE: o `__result` so pode ser trocado DENTRO do `if (TentaMontar(...))`")
        i_decl = efetivo_lp.index("string linhaComValor;")
        _exigir(falhas, i_decl < i_if,
                "FAIL-SAFE: a declaracao de `linhaComValor` tem de vir ANTES do guarda")
        _exigir(falhas, "__result =" not in efetivo_lp[i_decl:i_if],
                "FAIL-SAFE: ha escrita em `__result` ANTES do `if (TentaMontar(...))`")
    except (ValueError, arc.Falhou):
        falhas.append("FAIL-SAFE: o call site `%s` nao existe mais no AnexarNotasDoFunil"
                      % ANCORA_CHAMADA)

    # ---------------------------------------------------------------- FORMATO (BT-10F)
    insere = _corpo(efetivo_rt, ASSINATURA_INSERE, ("return corpo",), falhas, "InsereValorNaLinha")
    if insere:
        achado = re.search(r"string\s+sufixo\s*=\s*(.+?);", insere, re.S)
        _exigir(falhas, achado is not None,
                "FORMATO: nao achei a montagem do sufixo (`string sufixo = ...;`)")
        if achado:
            expr = achado.group(1).strip()
            _exigir(falhas, bool(re.match(r'" \(<color=#"\s*\+\s*CorDoValorDoMotor', expr)),
                    "FORMATO: o sufixo tem de ABRIR com `\" (<color=#\"` — o `(` colado no "
                    "espaco, NUNCA depois do ponto (e o `. (` do defeito da BT-10F)")
            _exigir(falhas, bool(re.search(r'"</color> health for you\)"\s*$', expr)),
                    "FORMATO: o sufixo tem de FECHAR em `</color> health for you)` — o paren "
                    "fecha a frase")
            _exigir(falhas, "+ valor +" in expr,
                    "FORMATO: o sufixo tem de carregar o VALOR calculado")
        _exigir(falhas, re.search(r'if\s*\(\s*corpo\.EndsWith\("\.",\s*StringComparison\.Ordinal\)\s*\)',
                                  insere),
                "FORMATO: falta o ramo que reconhece o ponto FINAL da frase do jogo")
        _exigir(falhas, re.search(
            r'corpo\.Substring\(0,\s*corpo\.Length\s*-\s*1\)\s*\+\s*sufixo\s*\+\s*"\."', insere),
            "FORMATO: o ramo do ponto tem de TIRAR o ponto antes de anexar o sufixo "
            "(`corpo.Substring(0, corpo.Length - 1) + sufixo + \".\"`) — sem isso o valor cai "
            "DEPOIS do ponto (`max health. (23.3 ...)`)")
        _exigir(falhas, re.search(r'return\s+corpo\s*\+\s*sufixo\s*\+\s*"\."\s*;', insere),
                "FORMATO: o caminho sem ponto final tambem tem de fechar em `\".\"` apos o sufixo")

    # ---------------------------------------------------------------- MESMO TEXTO exato
    mesmo = _corpo(efetivo_rt, ASSINATURA_MESMO, ("return",), falhas, "MesmoTexto")
    _exigir(falhas, re.search(
        r"string\.Equals\s*\(\s*a\.Trim\(\)\s*,\s*b\.Trim\(\)\s*,\s*StringComparison\.Ordinal\s*\)",
        mesmo),
        "FAIL-SAFE: `MesmoTexto` tem de ser IGUALDADE EXATA (`string.Equals(a.Trim(), "
        "b.Trim(), Ordinal)`): uma comparacao frouxa (`Contains`/`StartsWith`) faria o texto "
        "JA MODIFICADO casar de novo e duplicar o valor")


def falhas_da_fonte(cod_rt, cod_lp):
    """A lista de falhas do fonte (vazia = o patch esta como este teste exige)."""
    falhas = []
    try:
        _checa_fonte(cod_rt, cod_lp, falhas)
    except arc.Falhou as erro:
        falhas.append("ESTRUTURA: %s" % erro)
    except Exception as erro:  # nunca deixar o teste explodir sem dizer o porque
        falhas.append("ESTRUTURA: excecao ao ler o fonte: %s: %s" % (type(erro).__name__, erro))
    return falhas


# ================================================================== iscas embutidas ====

def defeitos_plantados(cod_rt, cod_lp):
    """Cada defeito, plantado numa COPIA em memoria do fonte, com a marca que a falha deve citar."""
    defeitos = {}

    # (1) PROCEDENCIA: numero fixo no lugar da leitura do ASSET — o defeito que o pedido nomeia.
    alvo = "float pct = PercentualDaSkill(skill);"
    if cod_rt.count(alvo) == 1:
        defeitos["pct-fixa"] = (cod_rt.replace(alvo, "float pct = 10f;"), cod_lp, "PercentualDaSkill")

    # (2) PROCEDENCIA: a vida maxima vinda do SavedMap PURO, nao do valor FINAL do motor.
    alvo = "float vida = personagem.MaxHealth;"
    if cod_rt.count(alvo) == 1:
        defeitos["vida-do-savedmap"] = (cod_rt.replace(alvo, "float vida = personagem.SavedMap[0];"),
                                        cod_lp, "MaxHealth")

    # (3) FAIL-SAFE: guarda de vida removida (sairia escrevendo com vida maxima zero).
    sem_guarda = re.sub(r"if\s*\(\s*vida\s*<=\s*0f\s*\)\s*\{[^}]*\}\s*", "", cod_rt, count=1)
    if sem_guarda != cod_rt:
        defeitos["sem-guarda-de-vida"] = (sem_guarda, cod_lp, "vida <= 0f")

    # (4) FAIL-SAFE: guarda de personagem removida.
    sem_pers = re.sub(r"if\s*\(\s*personagem\s*==\s*null\s*\)\s*\{[^}]*\}\s*", "", cod_rt, count=1)
    if sem_pers != cod_rt:
        defeitos["sem-guarda-de-personagem"] = (sem_pers, cod_lp, "sem personagem em foco")

    # (5) FAIL-SAFE: sem a inicializacao nula (um ramo de saida devolveria lixo).
    if cod_rt.count("linhaComValor = null;") >= 2:
        defeitos["sem-init-nulo"] = (cod_rt.replace("linhaComValor = null;", "", 1), cod_lp,
                                     "linhaComValor")

    # (6) FAIL-SAFE: identidade do gancho comparada com a SAIDA em vez da ENTRADA.
    alvo = "!MesmoTexto(skill.Description, original)"
    if cod_rt.count(alvo) == 1:
        defeitos["identidade-na-saida"] = (
            cod_rt.replace(alvo, "!MesmoTexto(skill.Description, linhaDoJogo)"), cod_lp,
            "MesmoTexto")

    # (7) FAIL-SAFE: `MesmoTexto` frouxo — o texto ja modificado casaria de novo (duplica).
    alvo = "string.Equals(a.Trim(), b.Trim(), StringComparison.Ordinal)"
    if cod_rt.count(alvo) == 1:
        defeitos["mesmo-texto-por-contains"] = (
            cod_rt.replace(alvo, "a.Trim().Contains(b.Trim())"), cod_lp, "Equals")

    # (8) FORMATO: o `(` do sufixo vai para DEPOIS do ponto — o defeito exato da BT-10F.
    alvo = 'string sufixo = " (<color=#"'
    if cod_rt.count(alvo) == 1:
        defeitos["formato-antes-do-ponto"] = (
            cod_rt.replace(alvo, 'string sufixo = ". (<color=#"'), cod_lp, "FORMATO")

    # (9) FAIL-SAFE no call site: a chamada deixa de estar sob o `if`.
    alvo = "if (ReaperTollPatch.TentaMontar(original"
    if cod_lp.count(alvo) == 1:
        defeitos["chamada-desprotegida"] = (
            cod_rt, cod_lp.replace(alvo, "if (true || ReaperTollPatch.TentaMontar(original"), "TentaMontar")

    return defeitos


# ===================================================================== o teste =========

def corpo():
    cod_rt = _le(FONTE_REAPER)
    cod_lp = _le(FONTE_LOCALIZE)
    arc.exigir(len(cod_rt) > 3000, "o %s veio curto/vazio: a leitura mudou de lugar?" % FONTE_REAPER)

    # --------------------------------------------------- 1. a trava no fonte VIVO
    falhas = falhas_da_fonte(cod_rt, cod_lp)
    arc.exigir(not falhas,
               "o ReaperTollPatch regrediu em %d ponto(s):\n  - %s" % (len(falhas), "\n  - ".join(falhas)))

    # --------------------------------------------------- 2. as iscas: a trava REPROVA?
    defeitos = defeitos_plantados(cod_rt, cod_lp)
    # As tres frentes pedidas (fail-safe, procedencia, formato) TEM de ter isca; sem isso o
    # teste nao demonstra que pega cada classe de defeito.
    arc.exigir(set(defeitos) >= {"pct-fixa", "vida-do-savedmap", "sem-guarda-de-vida",
                                 "sem-init-nulo", "mesmo-texto-por-contains",
                                 "formato-antes-do-ponto", "chamada-desprotegida"},
               "faltou isca embutida: as ancoras do plantio nao acharam o trecho (%s)"
               % ", ".join(sorted(defeitos)))
    for nome in sorted(defeitos):
        fonte_rt_mut, fonte_lp_mut, marca = defeitos[nome]
        f = falhas_da_fonte(fonte_rt_mut, fonte_lp_mut)
        arc.exigir(f, "o defeito plantado '%s' PASSOU pela trava (ela nao pega essa classe)" % nome)
        arc.exigir(any(marca in x for x in f),
                   "o defeito '%s' foi pego, mas nao por %r: %s" % (nome, marca, " | ".join(f)))

    # --------------------------------------------------- 3. o COMPORTAMENTO (modelo)
    descricao_do_asset = _descricao_do_asset()
    arc.exigir("%" in descricao_do_asset,
               "a descricao do asset de %r nao trouxe `%%`: %r" % (NOME_DA_SKILL, descricao_do_asset))
    pct = le_percentual(descricao_do_asset)
    arc.exigir(pct > 0,
               "o espelho do `LePercentual` nao leu a %% da descricao do asset: %r" % descricao_do_asset)
    # A % e LIDA, nao fixa: a MESMA funcao devolve outro numero para outro texto.
    arc.igual(le_percentual("Heals you for 25% of your life."), 25.0,
              "a % lida de uma descricao com 25%")
    arc.igual(le_percentual(descricao_do_asset.replace("%", "")), 0.0,
              "sem `%` na descricao, nao ha percentual (nada e inventado)")

    # O sufixo e o ramo do ponto saem do FONTE (nada de sufixo digitado no teste).
    efetivo_rt = rec.codigo_efetivo(cod_rt)
    insere = rec.corpo_do_metodo(efetivo_rt, ASSINATURA_INSERE)
    cor = re.search(r'CorDoValorDoMotor\s*=\s*"(CBB396|[0-9A-Fa-f]{6})"', efetivo_rt).group(1)
    ramo_remove, fallback = _ramo_do_ponto(insere)
    arc.exigir(ramo_remove and fallback, "o ramo do ponto/fallback mudou de forma: nao sei montar a linha")
    sufixo_fn = lambda valor: _sufixo_do_fonte(insere, cor, valor)  # noqa: E731

    # (a) PRIMEIRA passada: escreve UMA vez, na forma certa.
    ok, linha_1 = tenta_montar(descricao_do_asset, descricao_do_asset, descricao_do_asset, pct,
                               VIDA_MAXIMA_DE_CENA, sufixo_fn, ramo_remove)
    arc.exigir(ok, "com TODO dado provado o patch tinha de montar a linha")
    arc.igual(linha_1.count("health for you"), 1, "a primeira passada escreve o valor UMA vez")
    nodef = dict(descricao=descricao_do_asset, pct=pct, vida=VIDA_MAXIMA_DE_CENA,
                 sufixo_fn=sufixo_fn, ramo_remove=ramo_remove)

    # (b) FORMATO: termina em `).` e NUNCA tem `. (` no meio (a trava da BT-10F).
    arc.exigir(linha_1.endswith(")."),
               "a linha final tem de terminar em ').': %r" % linha_1[-80:])
    arc.exigir(". (" not in linha_1,
               "a linha final nao pode ter '. (' no meio (o defeito que a BT-10F consertou): %r"
               % linha_1)
    arc.exigir(("#" + cor) in linha_1,
               "o valor tem de sair na cor do valor dinamico do MOTOR (#%s): %r" % (cor, linha_1))
    valor_esperado = formata_0_1(VIDA_MAXIMA_DE_CENA * pct / 100.0)
    arc.exigir(valor_esperado in linha_1,
               "o valor da linha tem de ser a conta do motor (%s): %r" % (valor_esperado, linha_1))
    # O numero ACOMPANHA o personagem (nao e constante): outra vida maxima -> outro valor.
    _ok_outra, linha_outra = tenta_montar(descricao_do_asset, descricao_do_asset,
                                          descricao_do_asset, pct, 100.0, sufixo_fn, ramo_remove)
    dentro = r"<color=#%s>([^<]+)</color> health for you\)\." % cor
    v1 = re.search(dentro, linha_1)
    v2 = re.search(dentro, linha_outra)
    arc.exigir(v1 and v2 and v1.group(1) == valor_esperado
               and v2.group(1) == formata_0_1(100.0 * pct / 100.0) and v2.group(1) != v1.group(1),
               "o valor DENTRO do bloco tem de acompanhar a vida maxima (%s -> %s): %r"
               % (valor_esperado, formata_0_1(100.0 * pct / 100.0), linha_outra))

    # (c) FAIL-SAFE: sem skill / sem % / sem personagem / sem vida -> NADA escrito.
    # (rotulo, original, linha, descricao, vida_do_caso); o pct sai da propria descricao.
    sem_asset = "Heals you when an enemy dies."          # a linha de uma skill qualquer
    cenarios = (
        ("sem skill (asset nao carregado)", descricao_do_asset, descricao_do_asset, None,
         VIDA_MAXIMA_DE_CENA),
        ("sem % no asset", sem_asset, sem_asset, sem_asset, VIDA_MAXIMA_DE_CENA),
        ("sem personagem em foco", descricao_do_asset, descricao_do_asset, descricao_do_asset,
         None),
        ("personagem sem vida maxima", descricao_do_asset, descricao_do_asset,
         descricao_do_asset, 0.0),
    )
    for rotulo, original, linha, descricao, vida_do_caso in cenarios:
        # `sem % no asset` sai pelo `pct <= 0`; os outros, pela guarda correspondente
        pct_do_caso = le_percentual(descricao) if descricao is not None else pct
        ok_c, saida = tenta_montar(original, linha, descricao, pct_do_caso, vida_do_caso,
                                   sufixo_fn, ramo_remove)
        arc.exigir(not ok_c, "FAIL-SAFE '%s': o patch nao pode montar linha nenhuma" % rotulo)
        arc.igual(saida, linha, "FAIL-SAFE '%s': a linha do jogo tem de ficar INTACTA" % rotulo)

    # (d) SEGUNDA passada com o texto JA MODIFICADO: nao casa de novo, nao duplica.
    ok2, linha_2 = tenta_montar(linha_1, linha_1, descricao_do_asset, pct, VIDA_MAXIMA_DE_CENA,
                                sufixo_fn, ramo_remove)
    arc.exigir(not ok2, "FAIL-SAFE: a 2a passada com texto JA MODIFICADO nao pode casar de novo")
    arc.igual(linha_2, linha_1,
              "FAIL-SAFE: a 2a passada tem de devolver a MESMA linha (sem duplicar)")
    arc.igual(linha_2.count("health for you"), 1, "nada de valor duplicado na 2a passada")

    # ISCA embutida: com a comparacao FROUXA (o defeito), a 2a passada duplica — e a trava
    # estrutural (`MesmoTexto` por `string.Equals`) e quem impede.
    ok_d, linha_d = tenta_montar(linha_1, linha_1, descricao_do_asset, pct, VIDA_MAXIMA_DE_CENA,
                                 sufixo_fn, ramo_remove, igualdade=lambda a, b: True)
    arc.exigir(ok_d and linha_d.count("health for you") == 2,
               "a isca da duplicacao NAO duplicou: sem isso a guarda de identidade seria "
               "decoracao — saida: %r" % linha_d)

    print("ReaperTollPatch: 0 falha(s) no fonte vivo; %d defeito(s) plantado(s) reprovam pela razao certa"
          % len(defeitos))
    print("linha montada: ...%s" % linha_1[-96:].replace("\n", " / "))
    print("fail-safe: 4 cenarios sem dado provado ficam com a linha intacta; a 2a passada nao duplica")
    print("procedencia: %% do ASSET (lida de %s) e vida maxima do valor FINAL do motor" % CSV_DAS_SKILLS)


if __name__ == "__main__":
    arc.main(META, corpo)
