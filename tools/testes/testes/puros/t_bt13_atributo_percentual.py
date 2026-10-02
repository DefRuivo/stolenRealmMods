#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BT-13 (atributos em %) — a prova de fogo VERSIONADA do valor das skills de atributo em %.

POR QUE ESTE TESTE EXISTE
-------------------------
A familia (Light's Brilliance e as seis irmas) nasceu com prova de fogo em scratch/bt13/, que e
GITIGNORED: no CI a skill nao tinha teste nenhum. Este arquivo traz a prova para a suite
versionada, lendo o fonte C# por RECORTE ESTRUTURAL (`recorte.py`) e ancorando em IDENTIFICADOR.

O QUE ELE TRAVA (o defeito que motivaria cada item)
---------------------------------------------------
  1. A CONTA E `final x pct / (100 + somaPercentual)` — NAO `pct por cento do final`. O motor
     MULTIPLICA o subtotal pela porcentagem (`valor * (1 + soma/100)`), entao o que ESTA skill
     acrescenta e `final * pct / (100 + soma)`. O teste cobre OS DOIS LADOS da confusao: o caso
     em que a skill ja esta na soma (aprendida) e a leitura ingenua erraria (20 vs 24), e o caso
     em que a soma nao a inclui (so espiada na arvore) e as duas dao o mesmo (20 vs 20).
  2. A FAMILIA VEM DO ASSET, NAO DE LISTA DIGITADA: o fonte nao cita o nome de NENHUMA das sete
     skills, e o indice sai de `Game.Instance.Skills` x `Game.Instance.LevelableCharacterAttributes`.
     O MESMO criterio, rodado sobre o censo VERSIONADO (`docs/cobertura/skills.csv`), tem de dar
     exatamente 7 skills e 9 efeitos — o numero e conferido, nao narrado.
  3. O VALOR SAI DO ATRIBUTO FINAL DO MOTOR (`personagem[atributo.name]`, o indexador -> valor
     final), a % sai do asset (`efeito.TryGetConstantAmount`) e a soma das % sai do motor
     (`GetAttributeValueByMethod(atributo, Percentage, false)`); nenhum literal e digitado.
  4. FAIL-SAFE: sem personagem, sem o asset, sem % constante, com atributo atual <= 0 ou com a
     soma anulando o denominador, NAO sai numero nenhum (a linha do jogo fica intacta).

LIMITE (o que este teste NAO prova): ele NAO executa o C# do mod nem o motor (isso pediria a
`lib/` do jogo). A ligacao com o motor e o RECORTE das propriedades e da conta no patch — o
`final x pct / (100 + soma)` que o teste recomputa em Python e a MESMA expressao do fonte.
"""
import csv
import io
import os
import re

import arcabouco as arc
import recorte as rec

META = {
    "nome": "bt13-atributo-percentual",
    "categoria": "pura",
    "requer": [],
    "descricao": "BT-13: a conta do atributo em % e `final x pct / (100 + somaPercentual)` (e nao "
                 "`pct por cento do final`), a familia sao 7 skills e 9 efeitos vindos do asset e "
                 "os dois lados da confusao sao cobertos; fail-safe sem personagem/asset/%",
}

ARQUIVO = os.path.join("BetterTooltips", "Patches", "AtributoPercentualPatch.cs")
CENSO = os.path.join("docs", "cobertura", "skills.csv")

# Os cinco atributos PRIMARIOS (a identidade deles e a mesma do motor: MightBase, ...).
PRIMARIOS = ["MightBase", "DexterityBase", "IntelligenceBase", "VitalityBase", "ReflexBase"]

# As SETE skills da familia, como o censo as traz — a conferencia e por IGUALDADE, nao por contagem.
ESPERADAS = sorted([
    "Light's Brilliance", "Light's Celerity", "Light's Endurance",
    "Light's Intuition", "Light's Strength", "Speed", "Strength",
])


# --------------------------------------------------------------- leitura do fonte ---

def _codigo():
    caminho = os.path.join(arc.raiz_do_repo(), ARQUIVO)
    with io.open(caminho, encoding="utf-8") as fh:
        return rec.codigo_efetivo(fh.read())


def _metodo(codigo, assinatura, marcas):
    bloco = rec.corpo_do_metodo(codigo, assinatura)
    rec.exigir_metodo_inteiro(bloco, assinatura, marcas)
    return bloco


# ------------------------------------------------------- conta do motor (espelho) ---

def conta_do_motor(final, soma_pct, pct):
    """A MESMA conta do fonte: `final * pct / (100 + soma das %)`."""
    return final * pct / (100.0 + soma_pct)


def conta_ingenua(final, pct):
    """A leitura OBVIA que o card alerta ser ERRADA: 'pct por cento do final'."""
    return final * pct / 100.0


# ------------------------------------------------------------------------- corpo ---

def _familia_do_censo():
    """O MESMO criterio do mod, rodado sobre o censo: skill cujo proprio `attr` aplica o metodo
    `Percentage` a um dos cinco atributos primarios. Devolve (nomes, n_efeitos)."""
    achadas, efeitos = [], 0
    leitor = csv.DictReader(io.open(os.path.join(arc.raiz_do_repo(), CENSO), encoding="utf-8-sig"))
    for linha in leitor:
        attr = linha.get("attr") or ""
        marcados = [m for m in re.finditer(r"([A-Za-z]+):Percentage:", attr) if m.group(1) in PRIMARIOS]
        if marcados:
            achadas.append(linha.get("nome"))
            efeitos += len(marcados)
    return sorted(achadas), efeitos


def _conta_e_do_motor(codigo):
    partes = _metodo(codigo, "private static List<string> MontaPartes(",
                     ("return partes;",))
    arc.exigir("float atual = personagem[atributo.name];" in partes,
               "o valor nao sai do indexador do MOTOR (`personagem[atributo.name]`, valor FINAL)")
    arc.exigir("float somaPct = personagem.GetAttributeValueByMethod(" in partes,
               "a soma das % nao sai do MOTOR (`GetAttributeValueByMethod`)")
    arc.exigir("CharacterEffectMethod.Percentage" in partes,
               "a soma nao consulta o metodo `Percentage` (o MESMO que o motor multiplica)")
    arc.exigir("float denominador = 100f + somaPct;" in partes,
               "o denominador nao e `100f + somaPct` — a soma das % sumiu da conta")
    arc.exigir("float valor = atual * pct / denominador;" in partes,
               "a conta nao e `atual * pct / denominador`")
    arc.exigir("float valor = atual * pct / 100f" not in partes,
               "o fonte usa a conta INGENUA (`atual * pct / 100f`) — 'pct por cento do final'")
    arc.exigir("efeito.TryGetConstantAmount(out pct)" in partes,
               "a % nao sai de `efeito.TryGetConstantAmount` (a API do MOTOR sobre o Amount do asset)")
    arc.exigir("SavedMap" not in codigo,
               "o fonte usa `SavedMap` (o PURO, so os pontos investidos) como se fosse o valor final")
    for var in ("atual", "pct", "somaPct"):
        arc.exigir(re.search(r"\b%s\s*=\s*[0-9]" % var, codigo) is None,
                   "ha um literal atribuido a `%s` — o operando foi DIGITADO" % var)
    return partes


def _familia_vem_do_asset(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    indice = _metodo(codigo, "private static void GaranteIndice()",
                     ("catch (Exception ex)", "_indicePronto = true;"))
    tem = _metodo(codigo, "private static bool TemPercentualEmPrimario(",
                  ("CharacterEffectMethod.Percentage",))
    prim = _metodo(codigo, "private static CharacterAttribute[] AtributosPrimarios()",
                   ("Game.Instance.LevelableCharacterAttributes",))
    nomes = [n for n in ESPERADAS if n in codigo]
    arc.exigir(not nomes,
               "o fonte CITA nome de skill da familia (lista digitada): %r" % (nomes,))
    arc.exigir("Game.Instance.LevelableCharacterAttributes" in prim,
               "os atributos primarios nao vem do MOTOR (`Game.Instance.LevelableCharacterAttributes`)")
    arc.exigir("Game.Instance.Skills" in indice,
               "o indice nao e montado varrendo o asset CARREGADO (`Game.Instance.Skills`)")
    arc.exigir("CharacterEffectMethod.Percentage" in tem,
               "o criterio da familia nao olha o metodo `Percentage`")
    arc.exigir("SkillDoTexto(original)" in tenta,
               "a skill nao e resolvida pela descricao do asset (`SkillDoTexto`)")
    return indice


def _confusao_dos_dois_lados():
    # APRENDIDA: com base 100 a ficha ja mostra 120 e a soma inclui os 20% desta skill.
    aprendida = conta_do_motor(120.0, 20.0, 20.0)
    ingenua_aprendida = conta_ingenua(120.0, 20.0)
    arc.igual(round(aprendida, 1), 20.0, "o motor acrescenta 20 (nao 24) com a skill aprendida")
    arc.igual(round(ingenua_aprendida, 1), 24.0, "a leitura ingenua daria 24")
    arc.exigir(round(aprendida, 1) != round(ingenua_aprendida, 1),
               "a prova perdeu o sentido: a conta do motor e a ingenua dao o mesmo numero")

    # SO ESPIADA: a ficha ainda mostra 100 e a soma NAO inclui a skill -> as duas concordam.
    espiada = conta_do_motor(100.0, 0.0, 20.0)
    arc.igual(round(espiada, 1), 20.0, "com a skill so espiada o valor e o mesmo 20")

    # O valor ACOMPANHA o atributo (base 150, aprendida -> ficha 180 -> 30).
    arc.igual(round(conta_do_motor(180.0, 20.0, 20.0), 1), 30.0,
              "o valor acompanha o atributo (base 150 -> 30)")
    print("        ficha 100 (espiada) -> %g | ficha 120 (aprendida) -> %g | ingenua daria %g"
          % (espiada, aprendida, ingenua_aprendida))
    print("        ficha 180 (base 150, aprendida) -> %g" % conta_do_motor(180.0, 20.0, 20.0))


def _fail_safe(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    i_monta = tenta.find("linhaComValor = linhaDoJogo.TrimEnd()")
    arc.exigir(i_monta > 0, "nao achei onde a linha e montada (`linhaDoJogo.TrimEnd()`)")
    arc.exigir("original.IndexOf('%') < 0" in tenta,
               "falta o pre-filtro barato (`original.IndexOf('%') < 0` -> return false)")
    arc.exigir(tenta.find("linhaComValor = null;") < i_monta,
               "a linha nao e zerada ANTES do calculo")
    for rotulo, guarda in (("sem personagem", "if (personagem == null)"),
                           ("nenhum atributo rendeu valor", "if (partes.Count == 0)")):
        i = tenta.find(guarda)
        arc.exigir(i >= 0, "falta o guarda '%s' (%r)" % (rotulo, guarda))
        arc.exigir(i < i_monta, "o guarda '%s' vem DEPOIS de montar a linha" % rotulo)
        ramo = rec.bloco_apos(tenta, i)
        arc.exigir("return false;" in ramo and "linhaComValor = linhaDoJogo" not in ramo,
                   "o guarda '%s' nao e fail-safe" % rotulo)
    i_catch = tenta.find("catch (Exception ex)")
    arc.exigir(i_catch > 0 and "linhaComValor = null;" in tenta[i_catch:]
               and "return false;" in tenta[i_catch:],
               "o `catch` nao devolve a linha intacta")

    partes = _metodo(codigo, "private static List<string> MontaPartes(",
                     ("return partes;",))
    i_valor = partes.find("float valor = atual * pct / denominador;")
    for rotulo, guarda in (("sem % constante", "if (!efeito.TryGetConstantAmount(out pct))"),
                           ("atributo atual <= 0", "if (atual <= 0f)"),
                           ("soma anula o denominador", "if (denominador < 1f)")):
        i = partes.find(guarda)
        arc.exigir(i >= 0, "falta o guarda de montagem '%s' (%r)" % (rotulo, guarda))
        arc.exigir(i < i_valor, "o guarda '%s' vem DEPOIS de calcular o valor" % rotulo)
        arc.exigir("continue;" in rec.bloco_apos(partes, i),
                   "o guarda '%s' nao descarta o atributo (`continue;`)" % rotulo)
    arc.exigir("efeito.CharacterEffectMethod != CharacterEffectMethod.Percentage" in partes
               and "efeito.CalculateOnSecondPass" in partes,
               "o filtro de efeito (metodo Percentage / segunda passada) sumiu")
    arc.exigir("Tooltip.ToTitleCase" in _metodo(codigo, "private static string RotuloDoAtributo(",
                                                ("Tooltip.ToTitleCase",)),
               "o rotulo do atributo nao passa pelo `Tooltip.ToTitleCase` do jogo")


def corpo():
    codigo = _codigo()
    _conta_e_do_motor(codigo)
    _familia_vem_do_asset(codigo)

    achadas, efeitos = _familia_do_censo()
    arc.igual(achadas, ESPERADAS,
              "o criterio rodado no censo tem de dar as SETE skills (%d achadas)" % len(achadas))
    arc.igual(efeitos, 9, "a familia tem de ter NOVE efeitos de atributo primario em %%")

    _confusao_dos_dois_lados()
    _fail_safe(codigo)
    print("        familia: %d skills / %d efeitos" % (len(achadas), efeitos))


if __name__ == "__main__":
    arc.main(META, corpo)
