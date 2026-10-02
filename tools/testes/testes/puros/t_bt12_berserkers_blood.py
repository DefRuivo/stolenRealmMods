#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BT-12 (Beserker's Blood) — a prova de fogo VERSIONADA do valor dinamico da passiva.

POR QUE ESTE TESTE EXISTE
-------------------------
A prova de fogo da BT-12 (e a tabela de casos da BT-12A) vive em `scratch/bt12/`, que e
GITIGNORED: no CI a skill nao tinha teste nenhum. Este arquivo traz a prova para a suite
versionada e, com ela, a TABELA DE CASOS — que passa a existir no repositorio como a fixture
`bt12-berserkers-blood.entrada.json` (17 variantes EQUIVALENTES e 15 formas RECUSADAS).

O QUE ELE TRAVA (o defeito que motivaria cada item)
---------------------------------------------------
  1. O VALOR SAI DA VIDA PERDIDA DO MOTOR. O fonte le `personagem.HealthRatioInverse` (a FRACAO
     de vida que falta, propriedade do motor) e faz `bonus = razaoPerdida * fator`; nenhum
     literal e atribuido a `razaoPerdida`. Trocar por constante reprova.
  2. O FATOR SAI DA FORMULA DO ASSET. `FatorDaFormula(skill)` le `AttributeEffects[i].Amount`
     (`Game.Instance.Skills`); nenhum literal e atribuido a `fator`. Cravar o `100` reprova.
  3. A ANCORA ACEITA AS VARIANTES EQUIVALENTES E RECUSA O QUE NAO E A MESMA CONTA. O parser
     ancora em `HealthRatioInverse` e le a EQUIVALENCIA, nao a grafia: ordem dos fatores trocada,
     sufixo `f`/`F`, parenteses (na expressao inteira ou num lado) e espacamento LIVRE leem o
     fator; campo trocado (`HealthRatio`), `SavedMap`, o termo como texto/indice, termo NEGATIVO,
     multiplicador NAO-CONSTANTE (`* Source.DamageMod`), soma/divisao/segunda multiplicacao,
     embrulho que muda o valor (`Mathf.Max(1, ...)`) e a forma sem o termo CONTINUAM RECUSADAS
     (a linha do jogo fica INTACTA) em vez de lidas pela metade.
  4. FAIL-SAFE. Sem o fator legivel, sem personagem em foco ou sem vida maxima, a linha fica
     intacta: os guardas retornam false ANTES de montar o texto, e o `catch` tambem.
  5. O FORMATO (a trava da BT-12F). O valor entra no formato da FAMILIA: a frase do jogo TERMINA
     no ponto, o mod CORTA esse ponto e SOLDA o parenteses no fim, fechando a frase de novo em
     `).` — a linha montada termina em `).` e NUNCA tem `. (` no MEIO. Antes da BT-12F o patch
     colava o parenteses DEPOIS do ponto (`... gain 1% increased damage. (<cor>23.3</cor>%
     increased damage right now)`): o ponto no MEIO e a frase sem fechar, o mesmo defeito que a
     BT-10F tinha consertado no Reaper's Toll.

LIMITE (o que este teste NAO prova): ele NAO executa o C# do mod nem COMPILA o parser (isso
pediria dotnet e a lib/ do jogo — o `scratch/bt12/parser_csharp.py` faz isso, fora do CI). A
ligacao com o motor e o RECORTE ESTRUTURAL do fonte: as propriedades lidas, a ancora do parser,
a forma da conta e o FORMATO (os DOIS ramos de retorno com o ponto final preservado).
O espelho em Python roda a MESMA tabela de casos e o mesmo `InsereValorNaLinha`.
"""
import csv
import io
import json
import os
import re

import arcabouco as arc
import recorte as rec

META = {
    "nome": "bt12-berserkers-blood",
    "categoria": "pura",
    "requer": [],
    "descricao": "BT-12/BT-12A/BT-12F: o fator do Beserker's Blood sai da formula do asset, a "
                 "ancora aceita as variantes EQUIVALENTES (ordem trocada, sufixo f, parenteses, "
                 "espaco) e RECUSA campo trocado, SavedMap, termo negativo e multiplicador "
                 "nao-constante (tabela versionada de 17 aceitos + 15 recusados); a 'vida perdida' "
                 "sai do motor e o formato fecha em ').' sem '. (' no meio (trava da BT-12F)",
}

ARQUIVO = os.path.join("BetterTooltips", "Patches", "BerserkersBloodPatch.cs")
CENSO = os.path.join("docs", "cobertura", "skills.csv")

# A EXPRESSAO do asset, como o censo versionado a traz (a mesma do dump do jogo).
# As variantes nomeadas que o card exige — o corpo confere que cada uma cai no lado certo.
EQUIVALENTES_NOMEADAS = {
    "ordem dos fatores trocada": ("100 * Source.HealthRatioInverse", 100.0),
    "sufixo f": ("Source.HealthRatioInverse * 100f", 100.0),
    "parenteses na expressao inteira": ("(Source.HealthRatioInverse * 100)", 100.0),
    "espacamento livre (sem espaco)": ("Source.HealthRatioInverse*100", 100.0),
    "termo entre parenteses": ("(Source.HealthRatioInverse) * 100", 100.0),
}
RECUSADAS_NOMEADAS = {
    "campo trocado": "Source.HealthRatio * 100",
    "SavedMap": "Source.SavedMap * 100",
    "termo negativo": "-Source.HealthRatioInverse * 100",
    "multiplicador nao-constante": "Source.HealthRatioInverse * Source.DamageMod",
    "soma depois da multiplicacao": "Source.HealthRatioInverse * 100 + 5",
    "sem a ancora": "100",
}


# --------------------------------------------------------------- leitura do fonte ---

def _codigo():
    caminho = os.path.join(arc.raiz_do_repo(), ARQUIVO)
    with io.open(caminho, encoding="utf-8") as fh:
        return rec.codigo_efetivo(fh.read())


def _metodo(codigo, assinatura, marcas):
    bloco = rec.corpo_do_metodo(codigo, assinatura)
    rec.exigir_metodo_inteiro(bloco, assinatura, marcas)
    return bloco


def _linha_do_censo(nome):
    leitor = csv.DictReader(io.open(os.path.join(arc.raiz_do_repo(), CENSO), encoding="utf-8-sig"))
    for linha in leitor:
        if (linha.get("nome") or "").strip() == nome:
            return linha
    raise arc.Falhou("a skill %r nao esta no censo %s (versionado)" % (nome, CENSO))


# --------------------------------------------------- o MESMO parser do C# (espelho) ---

def sem_espacos(texto):
    return "".join(texto.split())


def tira_parenteses_de_fora(texto):
    texto = texto.strip()
    while len(texto) >= 2 and texto[0] == "(" and texto[-1] == ")":
        profundidade, fecha_no_fim = 0, True
        for i, c in enumerate(texto):
            if c == "(":
                profundidade += 1
            elif c == ")":
                profundidade -= 1
                if profundidade == 0 and i != len(texto) - 1:
                    fecha_no_fim = False
                    break
        if not fecha_no_fim or profundidade != 0:
            break
        texto = texto[1:-1].strip()
    return texto


def eh_referencia_simples(texto):
    if not texto.endswith("HealthRatioInverse"):
        return False
    corte = len(texto) - len("HealthRatioInverse")
    if corte == 0:
        return True
    if texto[corte - 1] != ".":
        return False
    return all(c.isalnum() or c in "_." for c in texto[:corte - 1])


def ultima_virgula_de_topo(texto, inicio, fim):
    profundidade, ultima = 0, -1
    for i in range(inicio, fim):
        c = texto[i]
        if c == "(":
            profundidade += 1
        elif c == ")":
            profundidade -= 1
        elif c == "," and profundidade == 0:
            ultima = i
    return ultima


def eh_referencia_da_razao(lado):
    termo = sem_espacos(tira_parenteses_de_fora(lado.strip()))
    embrulho = "Mathf.Round("
    if termo.startswith(embrulho) and termo.endswith(")"):
        fecha = len(termo) - 1
        virgula = ultima_virgula_de_topo(termo, len(embrulho), fecha)
        if virgula < 0:
            return False
        referencia = termo[len(embrulho):virgula]
        casas = termo[virgula + 1:fecha]
        return eh_referencia_simples(referencia) and casas.isdigit()
    return eh_referencia_simples(termo)


def tenta_numero(lado):
    texto = sem_espacos(tira_parenteses_de_fora(lado.strip()))
    if texto and texto[-1] in ("f", "F"):
        texto = texto[:-1]
    if not texto:
        return None
    tem_digito = False
    for c in texto:
        if c.isdigit():
            tem_digito = True
        elif c not in ".,":
            return None
    if not tem_digito:
        return None
    try:
        return float(texto.replace(",", "."))
    except ValueError:
        return None


def le_fator(formula):
    """Espelho de `BerserkersBloodPatch.LeFatorDaFormula` + auxiliares. Devolve float ou None."""
    if not formula or "HealthRatioInverse" not in formula:
        return None
    expressao = tira_parenteses_de_fora(formula.strip())
    estrela, multiplicacoes, profundidade = -1, 0, 0
    for i, c in enumerate(expressao):
        if c == "(":
            profundidade += 1
        elif c == ")":
            profundidade -= 1
            if profundidade < 0:
                return None
        elif c == "*" and profundidade == 0:
            multiplicacoes += 1
            estrela = i
    if profundidade != 0 or multiplicacoes != 1:
        return None
    esquerda = expressao[:estrela].strip()
    direita = expressao[estrela + 1:].strip()
    termo_na_esquerda = "HealthRatioInverse" in esquerda
    termo_na_direita = "HealthRatioInverse" in direita
    if termo_na_esquerda == termo_na_direita:
        return None
    lado_da_ancora = esquerda if termo_na_esquerda else direita
    lado_do_numero = direita if termo_na_esquerda else esquerda
    if not eh_referencia_da_razao(lado_da_ancora):
        return None
    return tenta_numero(lado_do_numero)


def insere_valor(linha_do_jogo, valor):
    """Espelho de `BerserkersBloodPatch.InsereValorNaLinha`: o valor entra ANTES do ponto final,
    no formato da FAMILIA — corta o ponto, solda o parenteses e fecha de novo em `.`. A linha que
    NAO termina em ponto nao ganha um pedaco cortado; as duas terminam em `).`."""
    corpo = (linha_do_jogo or "").rstrip()
    sufixo = " (<color=#CBB396>%s</color>%% increased damage right now)" % valor
    if corpo.endswith("."):
        return corpo[:-1] + sufixo + "."
    return corpo + sufixo + "."


# ------------------------------------------------------------------------- corpo ---

def _valor_e_vida_perdida_do_motor(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    arc.exigir("personagem.HealthRatioInverse" in tenta,
               "a 'vida perdida' nao sai de `personagem.HealthRatioInverse` (a FRACAO do motor)")
    arc.exigir("razaoPerdida * fator" in tenta,
               "a conta nao e `bonus = razaoPerdida * fator` (a mesma da formula do asset)")
    arc.exigir("personagem.MaxHealth" in tenta,
               "a guarda nao usa a vida MAXIMA do motor (`personagem.MaxHealth`)")
    arc.exigir("ShrineAuraPatch.ReceptorDaTooltip()" in tenta,
               "o personagem nao e o RECEPTOR da tooltip (caminho RV-26/RV-28/RV-33)")
    arc.exigir(re.search(r"\brazaoPerdida\s*=\s*[1-9]", codigo) is None,
               "ha um literal NAO-NULO atribuido a `razaoPerdida` — a fracao foi DIGITADA")
    arc.exigir("SavedMap" not in codigo,
               "o fonte usa `SavedMap` (o PURO, so os pontos investidos), nao o valor FINAL do motor")
    return tenta


def _fator_vem_do_asset(codigo):
    fator = _metodo(codigo, "private static float FatorDaFormula(SkillInfo skill)",
                    ("LeFatorDaFormula(efeito.Amount",))
    arc.exigir("AttributeEffects" in fator and "efeito.Amount" in fator,
               "o fator nao e lido de `AttributeEffects[i].Amount` (a EXPRESSAO do asset)")
    arc.exigir("Game.Instance.Skills" in codigo,
               "a skill nao vem do asset CARREGADO (`Game.Instance.Skills`)")
    arc.exigir(re.search(r"\bfator\s*=\s*[1-9]", codigo) is None,
               "ha um literal NAO-NULO atribuido a `fator` — o fator foi DIGITADO")


def _ancora_e_a_equivalencia(codigo):
    le = _metodo(codigo, "private static bool LeFatorDaFormula(string formula, out float fator)",
                 ("TentaNumero(ladoDoNumero",))
    arc.exigir('TermoDaFormula = "HealthRatioInverse"' in codigo,
               "a ancora nao e a propriedade `HealthRatioInverse` (a que a formula do asset le)")
    arc.exigir("formula.IndexOf(TermoDaFormula, StringComparison.Ordinal) < 0" in le,
               "o parser nao exige a ancora na formula (leria o primeiro numero da string)")
    arc.exigir("TiraParentesesDeFora(formula" in le,
               "o parser nao normaliza os parenteses de fora (variante de GRAFIA, nao de conta)")
    arc.exigir("multiplicacoes != 1" in le,
               "o parser nao exige UMA multiplicacao de topo (soma/divisao/2a multiplicacao passariam)")
    arc.exigir("EhReferenciaDaRazao(ladoDaAncora)" in le and "TentaNumero(ladoDoNumero" in le,
               "um lado tem de ser REFERENCIA a HealthRatioInverse e o outro UM numero constante")
    razao = _metodo(codigo, "private static bool EhReferenciaDaRazao(string lado)",
                    ("EhReferenciaSimples(termo)",))
    arc.exigir("Mathf.Round(" in razao and "EhReferenciaSimples" in razao,
               "o unico embrulho aceito (Mathf.Round) ou a referencia simples sumiram")
    ref = _metodo(codigo, "private static bool EhReferenciaSimples(string texto)",
                  ("char.IsLetterOrDigit(c)",))
    arc.exigir("corte == 0" in ref and "texto[corte - 1] != '.'" in ref,
               "a referencia deixou de exigir o termo no FIM (sufixo colado passaria)")


def _tabela_de_casos():
    casos = arc.ler_json("bt12-berserkers-blood", "entrada")
    arc.exigir(len(casos["equivalentes"]) == 17,
               "a fixture deixou de ter as 17 variantes equivalentes (tem %d)" % len(casos["equivalentes"]))
    arc.exigir(len(casos["recusadas"]) == 15,
               "a fixture deixou de ter as 15 formas recusadas (tem %d)" % len(casos["recusadas"]))
    for caso in casos["equivalentes"]:
        lido = le_fator(caso["formula"])
        arc.exigir(lido is not None and abs(lido - float(caso["fator"])) < 1e-4,
                   "a variante EQUIVALENTE (%s) nao foi lida: %r -> %r (esperado %s)"
                   % (caso["por"], caso["formula"], lido, caso["fator"]))
    for caso in casos["recusadas"]:
        lido = le_fator(caso["formula"])
        arc.exigir(lido is None,
                   "a forma RECUSADA (%s) foi lida pela metade: %r -> %r (tem de recusar)"
                   % (caso["por"], caso["formula"], lido))
    return casos


def _variantes_nomeadas():
    for rotulo, (formula, esperado) in EQUIVALENTES_NOMEADAS.items():
        lido = le_fator(formula)
        arc.exigir(lido is not None and abs(lido - esperado) < 1e-4,
                   "variante '%s' (%r) devia ler %s, veio %r" % (rotulo, formula, esperado, lido))
    for rotulo, formula in RECUSADAS_NOMEADAS.items():
        arc.exigir(le_fator(formula) is None,
                   "a forma '%s' (%r) NAO foi recusada — a linha do jogo sairia errada"
                   % (rotulo, formula))


def _formula_do_asset():
    linha = _linha_do_censo("Beserker's Blood")
    attr = linha["attr"]
    arc.exigir("HealthRatioInverse" in attr,
               "a formula do asset no censo perdeu a ancora: %r" % attr)
    formula = attr.split("Base:", 1)[1].rstrip(",").strip()
    arc.igual(le_fator(formula), 100.0,
              "o parser le o fator da formula do asset (%r)" % formula)
    return formula


def _formato_termina_em_ponto_paren(codigo):
    """O FORMATO (a trava que faltava, BT-12F): a frase do jogo TERMINA no ponto, o mod CORTA o
    ponto e SOLDA o parenteses no fim, fechando de novo em `).`. O defeito que isto prende e o
    formato ANTIGO — `... gain 1% increased damage. (<cor>23.3</cor>% increased damage right
    now)` — com o ponto no MEIO da frase e o parenteses depois dele."""
    ins = _metodo(codigo,
                  "private static string InsereValorNaLinha(string linhaDoJogo, string valor)",
                  ('sufixo + "."',))
    # O SUFIXO: abre com `" (<color=#"` (o `(` colado no espaco, NUNCA depois do ponto).
    arc.exigir('" (<color=#"' in ins,
               "o sufixo nao abre com `\" (<color=#\"` — o `(` tem de vir colado no espaco, "
               "nunca depois do ponto (o `. (` e a assinatura do defeito da BT-12F)")
    arc.exigir('". (<color=#"' not in ins,
               "o sufixo abre com `\". (<color=#\"` — o parenteses DEPOIS do ponto, o defeito "
               "da BT-12F (o ponto fica no MEIO da frase)")
    arc.exigir("</color>% increased damage right now)" in ins,
               "o sufixo do valor nao fecha em `</color>% increased damage right now)`")
    arc.exigir("+ valor" in ins,
               "o sufixo nao carrega o VALOR calculado")
    arc.exigir('CorDoValorDoMotor = "CBB396"' in codigo,
               "a cor do valor deixou de ser o literal do motor (`#CBB396`) que o espelho monta")
    # Os DOIS ramos de retorno (linha que JA termina em ponto e linha que nao) fecham em `).`.
    retornos = [l.strip() for l in ins.splitlines() if l.strip().startswith("return ")]
    arc.exigir(len(retornos) == 2,
               "a montagem da linha deixou de ter os DOIS ramos de retorno (tem %d)" % len(retornos))
    for linha in retornos:
        arc.exigir(linha.rstrip().endswith('+ ".";'),
                   "um ramo de retorno nao fecha o formato com o ponto final: %r" % linha)
    arc.exigir("corpo.Substring(0, corpo.Length - 1) + sufixo" in ins,
               "o ramo do ponto nao TIRA o ponto antes de anexar o sufixo — o valor cairia "
               "DEPOIS do ponto (o defeito da BT-12F)")
    arc.exigir('corpo.EndsWith(".", StringComparison.Ordinal)' in ins,
               "o patch nao trata a linha que JA termina em ponto (inseriria dois pontos)")
    # O COMPORTAMENTO do espelho nos DOIS ramos do formato.
    frase = "For every 1% of health missing, gain 1% increased damage"
    com_ponto = insere_valor(frase + ".", "23.3")
    sem_ponto = insere_valor(frase, "23.3")
    arc.exigir(com_ponto.endswith(").") and sem_ponto.endswith(")."),
               "a linha montada nao termina em `).`: %r / %r" % (com_ponto, sem_ponto))
    arc.exigir(". (" not in com_ponto and ". (" not in sem_ponto,
               "a linha montada tem `. (` no meio da frase (o defeito da BT-12F): %r"
               % (com_ponto if ". (" in com_ponto else sem_ponto))
    arc.exigir(com_ponto.count(".") == sem_ponto.count("."),
               "inserir valor duplicou/comeu o ponto final: %r / %r" % (com_ponto, sem_ponto))
    return com_ponto


def _fail_safe(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    i_monta = tenta.find("linhaComValor = InsereValorNaLinha")
    arc.exigir(i_monta > 0, "nao achei onde a linha e montada (`InsereValorNaLinha`)")
    arc.exigir(tenta.find("linhaComValor = null;") < i_monta,
               "a linha nao e zerada ANTES do calculo (default de linha intacta)")
    for rotulo, guarda in (("fator ilegivel", "if (fator <= 0f)"),
                           ("sem personagem", "if (personagem == null)"),
                           ("sem vida maxima", "if (vidaMaxima <= 0f)")):
        i = tenta.find(guarda)
        arc.exigir(i >= 0, "falta o guarda '%s' (%r)" % (rotulo, guarda))
        arc.exigir(i < i_monta, "o guarda '%s' vem DEPOIS de montar a linha" % rotulo)
        ramo = rec.bloco_apos(tenta, i)
        arc.exigir("return false;" in ramo and "linhaComValor = Insere" not in ramo,
                   "o guarda '%s' nao e fail-safe" % rotulo)
    i_catch = tenta.find("catch (Exception ex)")
    arc.exigir(i_catch > 0 and "linhaComValor = null;" in tenta[i_catch:]
               and "return false;" in tenta[i_catch:],
               "o `catch` nao devolve a linha intacta (`linhaComValor = null; return false;`)")


def corpo():
    codigo = _codigo()
    _valor_e_vida_perdida_do_motor(codigo)
    _fator_vem_do_asset(codigo)
    _ancora_e_a_equivalencia(codigo)
    casos = _tabela_de_casos()
    _variantes_nomeadas()
    formula = _formula_do_asset()
    _fail_safe(codigo)
    linha = _formato_termina_em_ponto_paren(codigo)

    # DEMONSTRACAO (nao prova): a formula acompanha a vida perdida com o fator do asset.
    fator = le_fator(formula)
    arc.exigir(fator is not None, "a formula do asset deixou de ser lida")
    fator = float(fator or 0.0)
    amostra = {p: round(p / 100.0 * fator, 1) for p in (0, 25, 50, 100)}
    arc.igual(amostra[50], 50.0, "metade da vida faltando com fator 100 -> +50% de dano")
    print("        fator do asset = %s | faltando 0/25/50/100%% -> +%s/+%s/+%s/+%s"
          % (fator, amostra[0], amostra[25], amostra[50], amostra[100]))
    print("        tabela: %d equivalentes lidas, %d recusadas" %
          (len(casos["equivalentes"]), len(casos["recusadas"])))
    print("        linha montada (formato da familia, BT-12F): " + linha)


if __name__ == "__main__":
    arc.main(META, corpo)
