#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NIV3-1 — o bloco de nivel 3 que NAO e a linha de auras passa pelo laco das notas.

O DEFEITO (latente, achado pela revisao do RV-17)
------------------------------------------------
O prefixo `CorEOrdemDoTooltip` (`LocalizePatch.cs`) move para o FIM do tooltip tudo o que o mod
escreveu — a nota pelo CONTEUDO (`_conteudosDeNota`) e a linha azul do nivel 3 pelo MARCADOR. Mas
so a `Your active shrine auras:` era alcancada: o bloco `Your skills on this status:`
(`StatusSkillSynergyPatch`) e escrito por OUTRO gancho (o postfix de
`Tooltip.ApplyDescriptionExpressions`, que roda ANTES do `ShowTooltip`) e o `_conteudosDeNota` o
exclui de proposito (`EhBlocoDoNivel3`). Ele ficava onde o motor o deixou.

CONSEQUENCIA: numa tooltip com NOTA e a linha de sinergia, a nota era remanejada para o FIM e ficava
DEPOIS da linha azul — e a linha azul deixava de ser a ultima, exatamente o que
`docs/TEXTO-TOOLTIPS.md` §9.1 promete ("a linha azul do nivel 3 — auras ativas / skills no status — e
sempre a ultima"). Hoje e LATENTE: so `Chilled` e `Poisoned` geram o bloco e nenhum dos dois recebe
nota. O buraco real e de TESTE — nenhum caso cobria bloco de nivel 3 que nao fosse a aura.

A DECISAO (explicita, e uma so)
-------------------------------
**(a) o bloco de sinergia passa a ser tratado como os outros.** Ele E nivel 3 — o §1 do documento ja
o classifica assim (linha 3(b), o caso do Frost Bite/CHL-1) —, entao ele vai para o FIM junto das
notas, na ordem do texto de origem, e a linha de auras (quando existe) continua por ULTIMO. Manter
duas regras de ordem no MESMO nivel seria declarar uma excecao para varrer o defeito para baixo do
tapete; a alternativa (b) exigiria reescrever a propria definicao do nivel 3, nao so o §9.1.

O QUE ESTE TESTE PRENDE
-----------------------
  1. ESTRUTURA, no fonte: o prefixo recolhe a sinergia pelo MARCADOR (`StatusSkillSynergyPatch.
     Marcador`, nunca pela cor), ANTES do laco das notas, e a remontagem continua devolvendo a cauda
     do nivel 3 por ULTIMO (o `corpo += "\\n\\n" + aura;` da linha de auras); o bloco continua sendo
     escrito com UMA quebra CRUA pelo patch (quem poe a linha em branco e o prefixo).
  2. COMPORTAMENTO, no material REAL: `Chilled` e `Poisoned` (os dois produtores do bloco hoje) com
     uma nota REAL das tabelas — o caso que hoje NAO existe e por isso o defeito passou. Antes da
     correcao a nota sai DEPOIS da linha azul (2 defeitos); depois, 0 defeito.
  3. O DEFEITO REPRODUZIDO nas duas metades: `contra-prova/cp_nivel3_sinergia_isca.py` (a regra de
     HOJE, sem o recolhimento) REPROVA pelo motivo certo; `..._ok.py` (a regra corrigida) passa.
  4. O CHECADOR NAO E VAZIO: defeitos plantados tem de ser VISTOS.
  5. A AURA NAO E TOCADA: as auras de shrine (o material aprovado pelo dono) saem BYTE A BYTE
     identicas com e sem a correcao — a prova de que o alvo da sinergia nao mexeu nelas; e os cinco
     casos de formato do RV-17 (`regras_formato.casos()`) tambem saem identicos.
"""
import os
import re

import arcabouco as arc
import recorte as rec
import regras_cor as reg
import regras_formato as fmt
import regras_nivel3 as n3

META = {
    "nome": "nivel3-sinergia",
    "categoria": "pura",
    "requer": [],
    "descricao": "NIV3-1: o bloco de nivel 3 da SINERGIA (Your skills on this status) passa pelo laco "
                 "do prefixo e vai para o FIM — a linha azul deixa de ficar atras da nota remanejada, "
                 "e as auras de shrine saem identicas",
}


def _codigo_do_patch(nome_arquivo):
    """O fonte SEM os comentarios (citacao nao e codigo)."""
    caminho = os.path.join(os.path.dirname(reg.FONTE_MOD), nome_arquivo)
    with open(caminho, encoding="utf-8") as fh:
        return re.sub(r"//[^\n]*", "", fh.read())


def _bloco_do_metodo(codigo, assinatura):
    """O METODO INTEIRO por CASAMENTO DE CHAVES — nunca por janela de caracteres.

    FORMATO-3: a versao anterior recortava uma JANELA FIXA de 3800 caracteres a partir da
    assinatura. O metodo tem 3371, entao a margem era de 429 — e o NIV3-1 ja consumiu ~260
    dela. Uma edicao INOFENSIVA (um log a mais, um local a mais) empurraria a ultima linha
    conferida para fora da janela e o teste reprovaria por motivo ALHEIO ao defeito — e o
    caminho curto para o verde seria AFROUXAR a janela. Aqui o recorte e o metodo de verdade,
    do tamanho que ele tiver: a funcao e a MESMA que o `t_formato_notas` usa (`recorte.py`),
    escrita uma vez e reutilizada por todos os pontos de chamada.
    """
    bloco = rec.corpo_do_metodo(codigo, assinatura)
    # GUARDA PERMANENTE: ou o recorte e o metodo INTEIRO (fecha nas chaves e traz o fim), ou
    # FALHA ALTO. E o que impede a janela de voltar sem que alguem apague o guarda.
    rec.exigir_metodo_inteiro(bloco, assinatura, MARCAS_DO_PREFIXO)
    return bloco


# As assinaturas lidas deste fonte (o nome mudar REPROVA dizendo qual sumiu, nunca passa vazio).
ASSINATURA_DO_PREFIXO = "private static void Prefix(ref string description)"

# As linhas que PROVAM que o recorte e o metodo INTEIRO (FORMATO-3): a extracao da sinergia
# pelo MARCADOR, a extracao da nota, a cauda do nivel 3 (`corpo += "\n\n" + aura;`) e o
# `description = corpo;`/`catch` do fim. Uma janela corta ANTES disso — o guarda reprova.
MARCAS_DO_PREFIXO = (
    "StatusSkillSynergyPatch.Marcador, out sinergia)",
    "bool achouNota = TirarNotaDoMod(ref description, out nota);",
    'corpo += "\\n\\n" + aura;',
    "if (achouSinergia)",
    "description = corpo;",
    "catch (Exception e)",
)


def _estrutura_no_fonte(codigo=None):
    codigo = _codigo_do_patch("LocalizePatch.cs") if codigo is None else codigo
    prefixo = _bloco_do_metodo(codigo, ASSINATURA_DO_PREFIXO)
    # (a) A SINERGIA E RECOLHIDA PELO MARCADOR — nunca pela cor, e com o MESMO `TirarBloco` da aura.
    arc.exigir(re.search(r"TirarBloco\(ref description, corAura, mesmaCor,\s*"
                         r"StatusSkillSynergyPatch\.Marcador, out sinergia\)", prefixo),
               "o prefixo tem de recolher o bloco de sinergia pelo MARCADOR do nivel 3 "
               "(`StatusSkillSynergyPatch.Marcador`), com o mesmo `TirarBloco` da linha de auras — "
               "sem isso o bloco fica atras da nota remanejada (o defeito do NIV3-1)")

    # (b) ANTES do laco das notas: a extract da sinergia nao pode depender do que as notas fizeram.
    i_sinergia = prefixo.find("StatusSkillSynergyPatch.Marcador, out sinergia)")
    i_notas = prefixo.find("bool achouNota = TirarNotaDoMod(ref description, out nota);")
    arc.exigir(i_sinergia >= 0 and i_notas > i_sinergia,
               "o recolhimento da sinergia tem de vir ANTES do laco das notas (sinergia em %d, "
               "notas em %d)" % (i_sinergia, i_notas))

    # (c) A CAUDA DO NIVEL 3 CONTINUA POR ULTIMO: a remontagem segue com a mesma linha de sempre, e
    #     ela e a ULTIMA coisa recolocada (o `aura` carrega a sinergia na frente quando ela existe).
    i_fim = prefixo.find('corpo += "\\n\\n" + aura;')
    arc.exigir(i_fim > i_notas,
               "a cauda do nivel 3 (sinergia + linha de auras) tem de ser a ULTIMA coisa recolocada, "
               "depois das notas — o `corpo += \"\\n\\n\" + aura;` sumiu ou subiu")
    arc.exigir("if (achouSinergia)" in prefixo and "sinergia :" in prefixo,
               "a sinergia tem de entrar na CAUDA do nivel 3 (a linha de auras por ultimo quando as "
               "duas existem) — e nao num append proprio, que deixaria a aura fora do lugar")

    # (d) O BLOCO CONTINUA IDENTIFICADO PELO MARCADOR NO REGISTRO DE NOTAS: o `EhBlocoDoNivel3` segue
    #     mantendo o bloco FORA do `_conteudosDeNota` (ele nao e nota do nivel 2 e nao pode ser
    #     movido como se fosse uma).
    arc.exigir("EhBlocoDoNivel3(conteudo)" in codigo,
               "o `RegistrarBlocosDeNota` tem de continuar excluindo o bloco do nivel 3 do registro "
               "de notas (`EhBlocoDoNivel3`) — o bloco de sinergia nao e uma nota do nivel 2")

    # (e) O PATCH DA SINERGIA CONTINUA ESCREVENDO UMA QUEBRA CRUA — quem poe a LINHA EM BRANCO e o
    #     prefixo (era o segundo defeito do caminho: o bloco saia colado na descricao).
    patch = _codigo_do_patch("StatusSkillSynergyPatch.cs")
    arc.exigir(re.search(r'return "\\n<color=#" \+ LocalizePatch\.CorDaLinhaDeAuras\(\)', patch),
               "o `StatusSkillSynergyPatch.Bloco` tem de continuar escrevendo UMA quebra (a linha em "
               "branco e responsabilidade do prefixo, pelo `AnexarNota`/`InicioDoSeparador`)")


# ------------------------------------------------------------------------------- prova ---
# O RETOQUE INOFENSIVO que a prova planta EM MEMORIA (nunca no arquivo): codigo a mais no
# INICIO do Prefix, do tipo que o NIV3-1 ja fez (~260 caracteres). Ele NAO toca nenhum dos
# marcadores conferidos — so ocupa espaco, que e o que uma janela de caracteres nao tolera.
# Tem de passar da margem de 429 que a janela de 3800 tinha; se alguem o encurtar, a prova
# reprova (a janela antiga voltaria a aguentar, e a prova nao demonstraria nada).
RETOQUE_INOFENSIVO = (
    "\n                string rastroDoRecorte = \"retoque inofensivo do recorte estrutural\";"
    "\n                int tamanhoDoRastro = rastroDoRecorte.Length;"
    "\n                if (tamanhoDoRastro > 0)"
    "\n                {"
    "\n                    rastroDoRecorte = rastroDoRecorte + \" [\" + tamanhoDoRastro + \"]\";"
    "\n                }"
    "\n                string outroRastro = string.Concat(rastroDoRecorte, \"/\", tamanhoDoRastro);"
    "\n                int somaDoRastro = tamanhoDoRastro + outroRastro.Length;"
    "\n                if (somaDoRastro > 0)"
    "\n                {"
    "\n                    outroRastro = outroRastro + \" :: \" + somaDoRastro.ToString();"
    "\n                }"
    "\n                string _ = outroRastro + rastroDoRecorte;"
)

# A JANELA que o defeito do FORMATO-3 usava (o numero que a tarefa cita). So existe aqui, na
# prova, para DEMONSTRAR por que ela nao serve — em nenhum caminho de checagem.
JANELA_ANTIGA = 3800


def _o_recorte_e_estrutural():
    """PROVA NOS DOIS SENTIDOS (FORMATO-3), em COPIA EM MEMORIA — o arquivo verdadeiro nao e tocado.

    (1) o RETOQUE INOFENSIVO no Prefix NAO pode quebrar o recorte nem a checagem;
    (2) o DEFEITO REAL (a sinergia deixar de ser recolhida pelo marcador) TEM de continuar sendo
        pego, pelo motivo certo;
    (3) e a JANELA ANTIGA (3800) teria estourado no retoque — o que sobra de prova de que o
        conserto era necessario (sem essa metade, o recorte estrutural seria feitio, nao conserto).
    """
    codigo = _codigo_do_patch("LocalizePatch.cs")
    arc.exigir(len(RETOQUE_INOFENSIVO) >= 430,
               "o retoque inofensivo encolheu (%d < 430): ele nao passaria da margem que a janela "
               "de %d tinha, e a prova (3) nao demonstraria nada" % (len(RETOQUE_INOFENSIVO),
                                                                     JANELA_ANTIGA))

    # (1) O RETOQUE: codigo a mais logo depois do `{` de abertura do Prefix, sem tocar marcador.
    retocado = codigo.replace(ASSINATURA_DO_PREFIXO + "\n            {",
                              ASSINATURA_DO_PREFIXO + "\n            {" + RETOQUE_INOFENSIVO, 1)
    arc.exigir(retocado != codigo, "o retoque nao achou a abertura do Prefix — a prova nao plantou nada")
    for marca in MARCAS_DO_PREFIXO:
        arc.exigir(marca not in RETOQUE_INOFENSIVO,
                   "o retoque carrega um marcador conferido (%r) — nao e inofensivo" % marca)
    bloco = _bloco_do_metodo(retocado, ASSINATURA_DO_PREFIXO)
    for marca in MARCAS_DO_PREFIXO:
        arc.exigir(marca in bloco,
                   "o retoque INOFENSIVO quebrou o recorte: `%s` caiu fora do bloco" % marca)
    _estrutura_no_fonte(retocado)   # ...e a checagem INTEIRA continua verde no fonte retocado

    # (3) A JANELA ANTIGA teria cortado: o que a prova demonstra.
    i_assin = retocado.find(ASSINATURA_DO_PREFIXO)
    na_janela = retocado[i_assin:i_assin + JANELA_ANTIGA]
    arc.exigir(not all(m in na_janela for m in MARCAS_DO_PREFIXO),
               "a janela de %d aguentou o retoque — sem isso a prova nao demonstra que o conserto "
               "era necessario (o metodo encolheu? o retoque encurtou?)" % JANELA_ANTIGA)

    # (2) O DEFEITO REAL: a sinergia deixa de ser recolhida pelo MARCADOR. A checagem tem de pegar.
    defeito = codigo.replace("StatusSkillSynergyPatch.Marcador, out sinergia)", "out sinergia)", 1)
    arc.exigir(defeito != codigo, "o plantio do defeito nao achou a extracao da sinergia")
    try:
        _estrutura_no_fonte(defeito)
    except arc.Falhou as erro:
        arc.exigir("StatusSkillSynergyPatch" in str(erro) or "sinergia" in str(erro),
                   "o defeito real foi pego, mas por um motivo que nao e o do NIV3-1: %s" % erro)
    else:
        arc.exigir(False, "o DEFEITO REAL (sinergia nao recolhida pelo marcador) PASSOU — a "
                          "checagem sobre o recorte e decoracao")


def _checador_nao_e_vazio():
    """Defeitos plantados tem de ser VISTOS — o checador nao pode ser decoracao."""
    marcador = n3.marcador_da_sinergia()
    nota = "Reduces all damage you take."
    bom = ("D" + n3.NL * 2 + "Duration Type: Normal" + n3.NL * 2
           + "<color=#CBB396>" + nota + "</color>" + n3.NL * 2
           + "<color=#00D7FF>" + marcador + " Frostbite I +2% damage per stack.</color>")
    arc.igual(n3.defeitos(bom, [nota], marcador), [],
              "um texto no formato CERTO nao pode ser acusado: %r" % bom)

    plantados = {
        "a nota depois da linha azul":
            ("D" + n3.NL * 2 + "Duration Type: Normal" + n3.NL * 2
             + "<color=#00D7FF>" + marcador + " X.</color>" + n3.NL * 2
             + "<color=#CBB396>" + nota + "</color>"),
        "a linha azul sumiu":
            ("D" + n3.NL * 2 + "Duration Type: Normal" + n3.NL * 2
             + "<color=#CBB396>" + nota + "</color>"),
        "duas linhas em branco seguidas":
            ("D" + n3.NL * 3 + "<color=#00D7FF>" + marcador + " X.</color>"),
        "linha em branco orfa (sem bloco nosso depois)":
            ("D" + n3.NL * 2 + "AP Cost: 1" + n3.NL * 2
             + "<color=#00D7FF>" + marcador + " X.</color>"),
        "quebra no fim do tooltip":
            ("D" + n3.NL * 2 + "<color=#00D7FF>" + marcador + " X.</color>" + n3.NL),
    }
    for nome, texto in plantados.items():
        achados = n3.defeitos(texto, [nota], marcador)
        arc.exigir(achados,
                   "o checador NAO viu o defeito plantado '%s': %r" % (nome, texto))


def _as_auras_de_shrine_nao_sao_tocadas():
    """A PROVA de que o alvo da sinergia NAO mexeu no material aprovado do dono.

    Duas metades:
      * o caso de SHRINE (`regras_formato.caso_shrine()`, com a linha `Your active shrine auras:`)
        sai BYTE A BYTE identico com e sem o recolhimento da sinergia — ele nao tem sinergia nenhuma;
      * os CINCO casos de formato do RV-17 (`regras_formato.casos()`) tambem saem identicos.
    """
    caso = fmt.caso_shrine()
    arc.exigir(n3.marcador_da_sinergia() not in caso["texto"],
               "o caso de shrine NAO pode carregar o marcador da sinergia (senao a prova nao diz nada)")
    com = n3.aplica_o_prefixo(caso["texto"], caso["registro"], com_sinergia=True)
    sem = n3.aplica_o_prefixo(caso["texto"], caso["registro"], com_sinergia=False)
    arc.igual(com, sem,
              "o caso de SHRINE mudou por causa do recolhimento da sinergia - o material aprovado "
              "pelo dono nao pode depender disso")

    for caso in fmt.casos():
        esperado = fmt.aplica_com_a_regra(caso, "rv17")
        obtido = n3.aplica_o_prefixo(caso["texto"], caso["registro"], com_sinergia=True)
        arc.igual(obtido, esperado,
                  "o caso '%s' do RV-17 mudou com a correcao do NIV3-1" % caso["rotulo"])


def _a_contra_prova():
    isca = os.path.join(arc.DIR_CONTRA_PROVA, "cp_nivel3_sinergia_isca.py")
    ok = os.path.join(arc.DIR_CONTRA_PROVA, "cp_nivel3_sinergia_ok.py")
    for caminho in (isca, ok):
        arc.exigir(os.path.isfile(caminho), "a contra-prova do NIV3-1 sumiu: %s" % caminho)

    cod_isca, saida_isca = arc.executar_arquivo(isca)
    arc.igual(arc.ler_meta(isca).get("esperado"), "reprovar",
              "a isca do NIV3-1 tem de declarar `esperado: reprovar` no META")
    arc.igual(cod_isca, arc.EXIT_FALHOU,
              "a isca (a regra de HOJE, sem o recolhimento) tinha de REPROVAR (exit 1); saida: %s"
              % (saida_isca.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir(n3.MOTIVO_DO_DEFEITO in saida_isca,
               "a isca tinha de reprovar PELO MOTIVO do nivel 3 (a nota devolvida depois da linha "
               "azul), nao por outra coisa: %s"
               % (saida_isca.strip().splitlines() or ["<sem saida>"])[-1])

    cod_ok, saida_ok = arc.executar_arquivo(ok)
    arc.igual(cod_ok, arc.EXIT_OK,
              "a metade corrigida tinha de PASSAR (exit 0); saida: %s"
              % (saida_ok.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir("fecha o formato" in saida_ok,
               "a metade ok tinha de provar que o formato de hoje fecha; saida: %s"
               % (saida_ok.strip().splitlines() or ["<sem saida>"])[-1])
    arc.igual(_sem_bloco_do_defeito(isca), _sem_bloco_do_defeito(ok),
              "a isca e a metade ok divergem fora do bloco do defeito - nao sao o mesmo teste")


def _sem_bloco_do_defeito(caminho):
    """O texto a partir do `def corpo` sem as linhas do BLOCO-DO-DEFEITO (a metade que muda)."""
    with open(caminho, encoding="utf-8") as fh:
        linhas = fh.read().splitlines()
    inicio = next((n for n, linha in enumerate(linhas) if linha.startswith("def corpo")), None)
    arc.exigir(inicio is not None, "%s nao tem `def corpo`" % caminho)
    dentro, guardadas = False, []
    for linha in linhas[inicio:]:
        if linha.strip().startswith("# >>> BLOCO-DO-DEFEITO"):
            dentro = True
            continue
        if linha.strip().startswith("# <<< BLOCO-DO-DEFEITO"):
            dentro = False
            continue
        if not dentro:
            guardadas.append(linha)
    return "\n".join(guardadas)


def corpo():
    # ------------------------------------------------------- 1. ESTRUTURA NO FONTE
    _o_recorte_e_estrutural()
    _estrutura_no_fonte()

    # ------------------------------------------------------- 2. O MATERIAL E REAL
    casos = n3.casos()
    arc.igual([c["rotulo"] for c in casos], ["Chilled", "Poisoned"],
              "os dois produtores do bloco hoje (status.csv:71 e :336)")
    _chave, nota = n3.primeira_nota_real()
    arc.exigir(nota.strip(), "a nota do material tem de ser REAL (das tabelas)")
    for caso in casos:
        arc.exigir(caso["marcador"] in caso["texto"] and n3.NL + "<color=#00D7FF>" in caso["texto"],
                   "o material de '%s' tem de carregar o bloco do nivel 3 na cor da paleta"
                   % caso["rotulo"])
        arc.exigir(caso["notas"] and caso["notas"][0] in caso["registro"],
                   "a nota de '%s' tem de estar REGISTRADA pelo conteudo (o prefixo a acha assim)"
                   % caso["rotulo"])

    # ------------------------------------------------------- 3. ANTES ERRADO / DEPOIS CERTO
    linhas = []
    for caso in casos:
        antes, depois = n3.antes_e_depois(caso)
        defeitos_antes = n3.defeitos(antes, caso["notas"], caso["marcador"])
        defeitos_depois = n3.defeitos(depois, caso["notas"], caso["marcador"])

        arc.exigir(defeitos_antes,
                   "'%s': o desenho de HOJE tinha de quebrar o formato (o defeito tem de aparecer)"
                   % caso["rotulo"])
        arc.exigir(any("ULTIMA" in d for d in defeitos_antes),
                   "'%s': o defeito de hoje tinha de aparecer pelo motivo do nivel 3, e saiu por: %s"
                   % (caso["rotulo"], defeitos_antes))
        arc.igual(defeitos_depois, [],
                  "formato QUEBRADO em '%s' com a correcao: %s | texto: %r"
                  % (caso["rotulo"], defeitos_depois, depois[-200:]))

        # a posicao exata: a NOTA antes da SINERGIA, e a sinergia por ULTIMO.
        i_nota = depois.find(caso["notas"][0])
        i_sinergia = depois.find(caso["marcador"])
        arc.exigir(0 <= i_nota < i_sinergia,
                   "'%s': a nota tem de vir ANTES da linha azul (nota em %d, sinergia em %d)"
                   % (caso["rotulo"], i_nota, i_sinergia))
        arc.igual(depois[i_sinergia:].rstrip()[-len(reg.FECHA_COR):], reg.FECHA_COR,
                  "'%s': a linha azul tem de fechar o tooltip" % caso["rotulo"])

        linhas.append("%s: ANTES a nota saia DEPOIS da linha azul (%s); DEPOIS a nota vem antes e a "
                      "linha azul fecha o tooltip (%s)"
                      % (caso["rotulo"], defeitos_antes[0][:52], "0 defeito"))

    # ------------------------------------------------------- 4. O CHECADOR NAO E VAZIO
    _checador_nao_e_vazio()

    # ------------------------------------------------------- 5. A AURA APROVADA NAO E TOCADA
    _as_auras_de_shrine_nao_sao_tocadas()

    # ------------------------------------------------------- 6. A CONTRA-PROVA
    _a_contra_prova()

    print("NIV3-1 fechado: o bloco de nivel 3 da SINERGIA passa pelo prefixo (recolhido pelo marcador, "
          "antes do laco das notas) e vai para o FIM junto das notas, com a linha de auras por ultimo "
          "quando as duas existem; as auras de shrine e os 5 casos do RV-17 saem IDENTICOS; "
          + " | ".join(linhas) + "; a isca REPROVOU e a metade corrigida PASSOU")


if __name__ == "__main__":
    arc.main(META, corpo)
