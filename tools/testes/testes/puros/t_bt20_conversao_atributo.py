#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BT-20 (conversao PLANA de atributo em Armor/Magic Armor) — a prova de fogo VERSIONADA do valor.

POR QUE ESTE TESTE EXISTE
-------------------------
A familia (`Body and Soul` e a irma `Invulnerable Winter`) nasceu no BT-20 (02/10). O pedido do dono:
mostrar, no tooltip, o VALOR ABSOLUTO de Armor/Magic Armor calculado com os stats ATUAIS do
personagem — numero nenhum digitado. Este teste traz a prova para a suite versionada, lendo o fonte
C# por RECORTE ESTRUTURAL (`recorte.py`) e ancorando em IDENTIFICADOR.

O QUE ELE TRAVA (o defeito que motivaria cada item)
---------------------------------------------------
  1. O VALOR SAI DO INTERPRETADOR DO PROPRIO JOGO: o `Amount` do asset e avaliado por
     `ShrineAuraPatch.ValorDaExpressao` (que faz `Game.TryEval`), nunca reescrito a mao. O teste
     reprova se houver literal atribuido ao valor ou multiplicador cravado (`* 5`).
  2. A FAMILIA VEM DO ASSET, NAO DE LISTA DIGITADA: o fonte nao cita o nome de NENHUMA das skills;
     o indice sai de `Game.Instance.Skills`. O MESMO criterio, rodado sobre o censo VERSIONADO
     (`docs/cobertura/skills-detalhe.csv`, coluna `attr`), tem de dar exatamente DUAS skills e
     QUATRO efeitos — o numero e conferido, nao narrado.
  3. O ROTULO do atributo sai do MOTOR (`CharacterAttribute.GetTooltipDisplayName`).
  4. FAIL-SAFE: sem personagem, sem efeito que avalie, o `catch` devolve a linha INTACTA.
  5. SEM REPETICAO (revisao BT-20R): skill que JA rende o valor por `DescriptionExpressions` (com
     token `[N]` na descricao) e PULADA — o valor que o motor ja mostra nao se repete. A `Body and
     Soul` (coluna `expr` VAZIA) continua recebendo a nota; a `Invulnerable Winter` (com `expr`),
     nao. Este item confere os DOIS lados no censo, nao so a presenca da guarda.

LIMITE (o que este teste NAO prova): ele NAO executa o C# do mod nem o motor (isso pediria a `lib/`
do jogo). A ligacao com o motor e o RECORTE dos identificadores no patch.
"""
import csv
import io
import os
import re

import arcabouco as arc
import recorte as rec

META = {
    "nome": "bt20-conversao-atributo",
    "categoria": "pura",
    "requer": [],
    "descricao": "BT-20: o valor de conversao de atributo em Armor/Magic Armor sai do interpretador "
                 "do jogo (`ShrineAuraPatch.ValorDaExpressao` -> `Game.TryEval`), a familia sao 2 "
                 "skills / 4 efeitos vindos do asset (nao de lista digitada), o fail-safe mantem a "
                 "linha intacta sem personagem/avaliacao e a skill que JA rende o valor por "
                 "DescriptionExpressions (token `[N]`) e PULADA (sem repeticao, revisao BT-20R)",
}

ARQUIVO = os.path.join("BetterTooltips", "Patches", "ConvercaoAtributoPatch.cs")
CENSO = os.path.join("docs", "cobertura", "skills-detalhe.csv")

# As DUAS skills da familia, como o censo as traz — a conferencia e por IGUALDADE, nao por contagem.
ESPERADAS = sorted(["Body and Soul", "Invulnerable Winter"])


# --------------------------------------------------------------- leitura do fonte ---

def _codigo():
    caminho = os.path.join(arc.raiz_do_repo(), ARQUIVO)
    with io.open(caminho, encoding="utf-8") as fh:
        return rec.codigo_efetivo(fh.read())


def _metodo(codigo, assinatura, marcas):
    bloco = rec.corpo_do_metodo(codigo, assinatura)
    rec.exigir_metodo_inteiro(bloco, assinatura, marcas)
    return bloco


# ---------------------------------------------------------------------- censo ---

def _familia_do_censo():
    """O MESMO criterio do mod, rodado sobre o censo: efeito `Armor:Base:Source[` ou
    `MagicArmor:Base:Source[` (metodo `Base`, atributo de mitigacao, `Amount` que le um stat).
    Devolve (nomes, n_efeitos)."""
    achadas, efeitos = [], 0
    leitor = csv.DictReader(io.open(os.path.join(arc.raiz_do_repo(), CENSO), encoding="utf-8-sig"))
    for linha in leitor:
        attr = linha.get("attr") or ""
        marcados = re.findall(r"(?:Armor|MagicArmor):Base:Source\[", attr)
        if marcados:
            achadas.append(linha.get("nome"))
            efeitos += len(marcados)
    return sorted(achadas), efeitos


# ------------------------------------------------------------------- checagens ---

def _valor_vem_do_motor(codigo):
    partes = _metodo(codigo, "private static List<string> MontaPartes(",
                     ("return partes;",))
    arc.exigir("ShrineAuraPatch.ValorDaExpressao(efeito.Amount" in partes,
               "o valor nao sai do avaliador do MOTOR com a `Amount` do asset (`ShrineAuraPatch."
               "ValorDaExpressao` -> `Game.TryEval`)")
    arc.exigir("efeito.Amount" in partes,
               "o fonte nao le a `Amount` do efeito do asset")
    arc.exigir(re.search(r"\bvalor\s*=\s*[0-9]", codigo) is None,
               "ha um literal atribuido a `valor` — o operando foi DIGITADO")
    arc.exigir(re.search(r"\*\s*5(f|\.0f)?\b", codigo) is None,
               "ha um multiplicador cravado (`* 5`) no fonte — o `Vitality * 5` do asset nao pode "
               "estar digitado")
    arc.exigir("TryGetConstantAmount" not in codigo,
               "o fonte trata `Amount` constante como conversao de atributo (nao e)")

    eh = _metodo(codigo, "private static bool EhConvercao(", ("Source[",))
    arc.exigir("CharacterEffectMethod.Base" in eh,
               "o criterio da familia nao olha o metodo `Base` (a conversao PLANA)")
    arc.exigir("CalculateOnSecondPass" in eh,
               "o criterio nao descarta os efeitos de segunda passada")


def _familia_vem_do_asset(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    indice = _metodo(codigo, "private static void GaranteIndice()",
                     ("_indicePronto = true;",))
    nomes = [n for n in ESPERADAS if n in codigo]
    arc.exigir(not nomes,
               "o fonte CITA nome de skill da familia (lista digitada): %r" % (nomes,))
    arc.exigir("Game.Instance.Skills" in indice,
               "o indice nao e montado varrendo o asset CARREGADO (`Game.Instance.Skills`)")
    arc.exigir("SkillDoTexto(original)" in tenta,
               "a skill nao e resolvida pela descricao do asset (`SkillDoTexto`)")


def _rotulo_do_motor(codigo):
    rotulo = _metodo(codigo, "private static string RotuloDoAtributo(",
                     ("GetTooltipDisplayName",))
    arc.exigir("GetTooltipDisplayName" in rotulo,
               "o rotulo do atributo nao sai do MOTOR (`CharacterAttribute.GetTooltipDisplayName`)")


def _fail_safe(codigo):
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    i_monta = tenta.find("linhaComValor = linhaDoJogo.TrimEnd()")
    arc.exigir(i_monta > 0, "nao achei onde a linha e montada (`linhaDoJogo.TrimEnd()`)")
    arc.exigir('original.IndexOf("armor", StringComparison.OrdinalIgnoreCase) < 0' in tenta,
               "falta o pre-filtro barato (`... IndexOf(\"armor\", OrdinalIgnoreCase) < 0` -> false)")
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
    i_filtro = partes.find("if (!EhConvercao(efeito))")
    arc.exigir(i_filtro >= 0, "falta o filtro de efeito (`if (!EhConvercao(efeito))`)")
    arc.exigir("continue;" in rec.bloco_apos(partes, i_filtro),
               "o filtro de efeito nao descarta o efeito (`continue;`)")
    i_eval = partes.find("if (!ShrineAuraPatch.ValorDaExpressao(")
    arc.exigir(i_eval >= 0, "falta o guarda da avaliacao (`if (!ShrineAuraPatch.ValorDaExpressao(`)")
    arc.exigir("continue;" in rec.bloco_apos(partes, i_eval),
               "a expressao nao avaliada nao descarta o atributo (`continue;`)")


def _guarda_sem_repeticao(codigo):
    """BT-20R: a skill que JA rende o valor pelo motor (DescriptionExpressions + `[N]`) e PULADA.

    A guarda tem de vir ANTES de montar a linha e devolver `false` (linha do jogo intacta) — o
    valor que o motor ja escreve na frase nao se repete.
    """
    tenta = _metodo(codigo, "public static bool TentaMontar(",
                    ("catch (Exception ex)", "linhaComValor = null;"))
    i_monta = tenta.find("linhaComValor = linhaDoJogo.TrimEnd()")
    i_guarda = tenta.find("if (JaRenderizadoPeloMotor(skill))")
    arc.exigir(i_guarda >= 0,
               "falta a guarda `JaRenderizadoPeloMotor(skill)` — sem ela o valor que o proprio "
               "motor JA mostra (token `[N]`) e anexado de novo (repeticao do BT-20R)")
    arc.exigir(i_guarda < i_monta,
               "a guarda de repeticao vem DEPOIS de montar a linha")
    ramo = rec.bloco_apos(tenta, i_guarda)
    arc.exigir("return false;" in ramo and "linhaComValor = linhaDoJogo" not in ramo,
               "a guarda de repeticao nao e fail-safe (tem de devolver a linha intacta)")

    guarda = _metodo(codigo, "private static bool JaRenderizadoPeloMotor(",
                     ("return false;",))
    arc.exigir("skill.DescriptionExpressions" in guarda,
               "a guarda nao olha as `DescriptionExpressions` do asset (e o que o motor usa para "
               "renderizar o `[N]`)")
    arc.exigir("Length == 0" in guarda or ".Length != 0" in guarda,
               "a guarda nao compara o tamanho do array de expressoes (expr vazia = nada renderizado)")
    arc.exigir("TemTokenNumerico(skill.Description)" in guarda,
               "a guarda nao confere o token `[N]` na descricao (o motor so substitui onde ha token)")


def _expr_do_censo():
    """nome -> coluna `expr` do censo, so para a familia: prova que a guarda morde onde deve.

    A `Invulnerable Winter` TEM expressao (o motor renderiza `Current Bonus: [1]`) e a `Body and
    Soul` tem `expr` VAZIA (a linha do jogo nao traz numero — a nota do dono e que informa).
    """
    expr = {}
    leitor = csv.DictReader(io.open(os.path.join(arc.raiz_do_repo(), CENSO), encoding="utf-8-sig"))
    for linha in leitor:
        if linha.get("nome") in ESPERADAS:
            expr[linha.get("nome")] = (linha.get("expr") or "").strip()
    return expr


def corpo():
    codigo = _codigo()
    _valor_vem_do_motor(codigo)
    _familia_vem_do_asset(codigo)
    _rotulo_do_motor(codigo)
    _fail_safe(codigo)
    _guarda_sem_repeticao(codigo)

    achadas, efeitos = _familia_do_censo()
    arc.igual(achadas, ESPERADAS,
              "o criterio rodado no censo tem de dar as DUAS skills (%d achadas)" % len(achadas))
    arc.igual(efeitos, 4, "a familia tem de ter QUATRO efeitos de conversao (Armor + MagicArmor x2)")
    print("        familia: %d skill(s) / %d efeito(s) -> %s" % (len(achadas), efeitos,
                                                                 ", ".join(achadas)))

    exprs = _expr_do_censo()
    arc.igual(exprs.get("Body and Soul"), "",
              "a `Body and Soul` tem de continuar com `expr` VAZIA — senao a guarda de repeticao "
              "mataria a nota do pedido")
    arc.exigir(exprs.get("Invulnerable Winter", "") != "",
               "a `Invulnerable Winter` tem de ter expressao (`expr` nao vazia) — e o caso da "
               "repeticao que a guarda BT-20R elimina")
    print("        expr: 'Body and Soul'=%r (nota sai) | 'Invulnerable Winter'=%r (pulada)"
          % (exprs.get("Body and Soul"), exprs.get("Invulnerable Winter")))


if __name__ == "__main__":
    arc.main(META, corpo)
