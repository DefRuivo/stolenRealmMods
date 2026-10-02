#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FORMATO-6 — a janela de 2000 caracteres do `check_patches.py` (regra 2) virou recorte ESTRUTURAL.

POR QUE ESTE TESTE EXISTE
-------------------------
A regra 2 do `tools/check_patches.py` decide se um `[HarmonyPatch]` tem assinatura por TIPO
(`typeof(`/`nameof(`) procurando o alvo num TRECHO. Esse trecho, quando o bloco balanceado nao
era achado, era `codigo[pos:pos + 2000]` — um recorte de DISTANCIA, a mesma familia que a
FORMATO-2/3/4 fecharam dentro de `tools/testes/`: mede distancia em caracteres, entao quebra por
reformatacao (e nao por defeito) e o caminho curto para o verde vira AFROUXAR O NUMERO.

O conserto reusa `tools/testes/recorte.py` (casamento de chaves, literal-aware, FALHA ALTA): o
trecho vai do `[HarmonyPatch` ate o `}` que casa com o bloco da declaracao anotada, e quando as
chaves nao fecham ele FALHA ALTO (o consumidor trata como REPROVA) em vez de cair para uma
janela de caracteres.

O QUE ESTE TESTE PROVA (nos dois sentidos, e no repositorio inteiro)
--------------------------------------------------------------------
  1. PRIMITIVO: o recorte novo acha o `typeof` que esta DENTRO do bloco (nao so no atributo) e,
     com as chaves que nao fecham, FALHA ALTO — nao existe mais a janela de 2000 como fallback.
  2. DIRECAO 1 (edicao inofensiva nao quebra): numa fonte REAL cuja assinatura esta a MAIS de
     2000 chars do atributo (`ShrineAuraPatch.cs`), a janela removida diria "sem assinatura"
     enquanto o recorte estrutural acha; e um retoque inofensivo de 2200 chars NAO muda o
     veredito da regra 2.
  3. DIRECAO 2 (o defeito real continua pego): trocar a assinatura por TIPO por um nome em
     STRING (o defeito que a regra existe para pegar) REPROVA — num caso sintetico e num arquivo
     REAL do repo; e a janela de 2000, quando um `typeof` ALHEIO cai dentro dela, deixaria
     passar o defeito, enquanto o recorte estrutural o pega (por falha alta).
  4. REPOSITORIO INTEIRO: o veredito (o conjunto de arquivo:linha que REPROVAM) e IDENTICO
     antes e depois — o conserto nao mexeu em nenhum achado real — e a janela de 2000 nunca
     disparava em fonte valida (0 vezes), que e por que ela passava despercebida.
"""
import importlib.util
import os
import re

import arcabouco as arc

META = {
    "nome": "formato6-check-patches-janela",
    "categoria": "pura",
    "requer": [],
    "descricao": "FORMATO-6: a janela de 2000 chars do check_patches (regra 2) e recorte "
                 "estrutural (recorte.py, falha alta) — o retoque inofensivo nao quebra e o "
                 "defeito real continua pego, sem mudar nenhum veredito no repo",
}

RAIZ = arc.raiz_do_repo()
CAMINHO_CP = os.path.join(RAIZ, "tools", "check_patches.py")
FONTE_REAL = os.path.join("BetterTooltips", "Patches", "ShrineAuraPatch.cs")
FONTE_DEFEITO = os.path.join("BetterCombatText", "Patches.cs")

PADRAO_TIPO = r"\b(typeof|nameof)\s*\("


def _modulo_do_check():
    """Carrega o `check_patches.py` por caminho (como o proprio script carrega o empacotador)."""
    spec = importlib.util.spec_from_file_location("check_patches_f6", CAMINHO_CP)
    cp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cp)
    rec, arcmod = cp.carregar_recorte()
    return cp, rec, arcmod


def _separado(cp, rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as fh:
        codigo, sem_comentario, comentarios = cp.separar(fh.read())
    return codigo, sem_comentario, comentarios


def _atributos(codigo):
    """(m, linha) de cada `[HarmonyPatch\\b`, como a regra 2 os encontra."""
    return [(m, codigo[:m.start()].count("\n") + 1)
            for m in re.finditer(r"\[HarmonyPatch\b", codigo)]


def _trecho_antigo(cp, codigo, m):
    """A EXPRESSAO REMOVIDA: bloco balanceado ou, sem bloco, a janela `pos:pos + 2000`."""
    bloco = cp.bloco_chaves(codigo, m.start())
    return codigo[m.start():bloco[1]] if bloco else codigo[m.start():m.start() + 2000]


def _retoque(cp, tamanho):
    """Codigo C# inofensivo com pelo menos `tamanho` chars: sem chave, sem literal, sem typeof."""
    linhas, n = [], 0
    while n < tamanho:
        linhas.append("\n    private static int _rastro%d = 0;" % len(linhas))
        n += len(linhas[-1])
    return "".join(linhas)


# ---------------------------------------------------------------- 1. primitivo ---

SINTETICO = (
    "[HarmonyPatch]\n"
    "class Patch\n"
    "{\n"
    "    private static readonly System.Type[] Assinatura =\n"
    "        new[] { typeof(AlvoDoPatch), typeof(int) };\n"
    "}\n"
)

QUEBRADO = (
    "[HarmonyPatch]\n"
    "class Patch\n"
    "{\n"
    "    private static void Alvo()\n"
    "    {\n"
    "        return;\n"          # chaves NAO fecham de proposito
    "    typeof(AlvoDoPatch);\n"  # um typeof ALHEIO dentro dos ~2000
)


def _primitivo(cp, rec, arcmod):
    codigo, _, _ = cp.separar(SINTETICO)
    m = _atributos(codigo)[0][0]
    trecho = cp.trecho_do_patch(codigo, m.start(), rec, arcmod)
    arc.exigir(trecho.startswith("[HarmonyPatch]"), "o trecho nao comeca no atributo: %r" % trecho[:30])
    arc.exigir("typeof(AlvoDoPatch)" in trecho and trecho.rstrip().endswith("}"),
               "o recorte estrutural nao chegou ao `typeof` de DENTRO do bloco: %r" % trecho)

    codigo_q, _, _ = cp.separar(QUEBRADO)
    m = _atributos(codigo_q)[0][0]
    try:
        cp.trecho_do_patch(codigo_q, m.start(), rec, arcmod)
    except arcmod.Falhou:
        pass
    else:
        arc.exigir(False, "as chaves que NAO fecham nao falharam alto — o recorte devolveu um "
                          "pedaco em silencio (a janela de caracteres voltou?)")


# ------------------------------------------ 2. direcao 1: edicao inofensiva nao quebra ---

def _direcao_1(cp, rec, arcmod):
    codigo, sem_comentario, comentarios = _separado(cp, FONTE_REAL)

    # O `[HarmonyPatch]` BARE de classe: o atributo sozinho nao tem `typeof`/`nameof`; a
    # assinatura por TIPO esta no bloco (o atributo tipado de um metodo, dentro da classe).
    alvo = None
    for m, ln in _atributos(codigo):
        fim_attr = codigo.find("]", m.start())
        if not re.search(PADRAO_TIPO, codigo[m.start():fim_attr + 1]):
            alvo = (m, ln, fim_attr)
            break
    arc.exigir(alvo is not None, "nao achei o `[HarmonyPatch]` bare de classe em %s" % FONTE_REAL)
    m, ln, fim_attr = alvo

    nxt = re.search(PADRAO_TIPO, codigo[fim_attr + 1:])
    distancia = nxt.start() + fim_attr + 1 - m.start() if nxt else -1
    arc.exigir(distancia > 2000,
               "a prova perdeu o sentido: a assinatura de `%s` esta a %d chars (<=2000)"
               % (FONTE_REAL, distancia))

    # A JANELA REMOVIDA diria "sem assinatura" (o alvo esta FORA dos 2000); o RECORTE ESTRUTURAL acha.
    arc.exigir(re.search(PADRAO_TIPO, codigo[m.start():m.start() + 2000]) is None,
               "a janela de 2000 achou a assinatura — a prova perdeu o sentido")
    arc.exigir(re.search(PADRAO_TIPO, cp.trecho_do_patch(codigo, m.start(), rec, arcmod)) is not None,
               "o recorte estrutural NAO achou a assinatura que esta no bloco")

    # RETOQUE INOFENSIVO: 2200 chars innocuos logo depois da abertura da classe (que agora
    # ficam entre o atributo e a assinatura). O veredito da regra 2 NAO pode mudar.
    abertura = codigo.find("{", m.start())
    retocado = codigo[:abertura + 1] + _retoque(cp, 2200) + codigo[abertura + 1:]
    arc.exigir(cp.trecho_do_patch(retocado, m.start(), rec, arcmod) !=
               cp.trecho_do_patch(codigo, m.start(), rec, arcmod),
               "o retoque nao entrou no recorte — nao plantou nada")
    arc.exigir(re.search(PADRAO_TIPO, retocado[m.start():m.start() + 2000]) is None,
               "a janela de 2000 aguentou o retoque: a prova perdeu o sentido")

    def _reprovas_2(texto_codigo, sem_com):
        # a regra 2 como o main a roda: `separar` + `regra2_assinatura` sobre o texto MUTADO
        c, s, cm = cp.separar(texto_codigo)
        return cp.regra2_assinatura([(FONTE_REAL, c, s, cm)], rec, arcmod)[0]

    r_antes = _reprovas_2(codigo, sem_comentario)
    r_depois = _reprovas_2(retocado, sem_comentario)
    arc.exigir(not r_antes, "a fonte real ja reprovava antes do retoque: %r" % r_antes)
    arc.exigir(r_depois == r_antes,
               "o retoque INOFENSIVO mudou o veredito da regra 2 (`%s`): %r -> %r"
               % (FONTE_REAL, r_antes, r_depois))


# ------------------------------------------------ 3. direcao 2: o defeito real continua pego ---

DEFEITO_SINTETICO = (
    '[HarmonyPatch("set_Alvo")]\n'          # nome em STRING: o defeito que a regra existe para pegar
    "internal static class PatchRuim\n"
    "{\n"
    "    private static void Postfix() { }\n"
    "}\n"
)


def _direcao_2(cp, rec, arcmod):
    # (a) sintetico: o nome em STRING (sem typeof/nameof) tem de REPROVAR.
    codigo, _, _ = cp.separar(DEFEITO_SINTETICO)
    reprovam, total = cp.regra2_assinatura([("sintetico.cs", codigo, codigo, [])], rec, arcmod)
    arc.exigir(total == 1 and len(reprovam) == 1,
               "o defeito sintetico (nome em string) nao foi pego: reprova=%r total=%d"
               % (reprovam, total))

    # (b) REAL: `BetterCombatText/Patches.cs` — troca `[HarmonyPatch(typeof(BossHealthbar),
    # "set_BossCharacter")]` por `[HarmonyPatch("set_BossCharacter")]` (assina pelo nome). A
    # mutacao e no TEXTO CRU (o `separar` apaga o conteudo das strings, entao `codigo` nao tem
    # a string `"set_BossCharacter"` para casar).
    with open(os.path.join(RAIZ, FONTE_DEFEITO), encoding="utf-8") as fh:
        cru = fh.read()
    codigo_real, sem_real, _ = cp.separar(cru)
    antigo = '[HarmonyPatch(typeof(BossHealthbar), "set_BossCharacter")]'
    novo = '[HarmonyPatch("set_BossCharacter")]'
    arc.exigir(antigo in cru, "nao achei a assinatura tipada em %s — a prova mudou" % FONTE_DEFEITO)
    defeituoso, _, _ = cp.separar(cru.replace(antigo, novo, 1))
    reprovam, _ = cp.regra2_assinatura([(FONTE_DEFEITO, defeituoso, sem_real, [])], rec, arcmod)
    arc.exigir(len(reprovam) == 1 and reprovam[0][1] == _atributos(codigo_real)[0][1],
               "o defeito REAL em `%s` nao foi pego na linha certa: %r" % (FONTE_DEFEITO, reprovam))

    # (c) o lado da janela: com um `typeof` ALHEIO dentro dos 2000 e chaves que nao fecham, a
    #     EXPRESSAO REMOVIDA diria "tem assinatura" (passa o defeito); o recorte estrutural
    #     FALHA ALTO e o consumidor REPROVA.
    codigo_q, _, _ = cp.separar(QUEBRADO)
    m = _atributos(codigo_q)[0][0]
    arc.exigir(re.search(PADRAO_TIPO, _trecho_antigo(cp, codigo_q, m)) is not None,
               "a janela de 2000 nao achou o `typeof` ALHEIO — a prova perdeu o sentido")
    reprovam, _ = cp.regra2_assinatura([("quebrado.cs", codigo_q, codigo_q, [])], rec, arcmod)
    arc.exigir(len(reprovam) == 1 and "casamento de chaves" in reprovam[0][3],
               "com chaves que nao fecham o check NAO reprovou por falha alta: %r" % reprovam)


# ------------------------------------------------------- 4. repositorio inteiro ---

def _varredura_do_repo(cp, rec, arcmod):
    """Roda a regra 2 em TODA fonte que o check olha, com a expressao ANTIGA e com a NOVA."""
    pastas = []
    for entrada in sorted(os.listdir(RAIZ)):
        pasta = os.path.join(RAIZ, entrada)
        if os.path.isdir(pasta) and os.path.isfile(os.path.join(pasta, "Plugin.cs")):
            pastas.append(pasta)

    cs, antigos, novos, fallback = [], [], [], 0
    for pasta in pastas:
        for caminho in cp.arquivos_cs(pasta):
            with open(caminho, encoding="utf-8", errors="replace") as fh:
                codigo, sem_comentario, comentarios = cp.separar(fh.read())
            cs.append((caminho, codigo, sem_comentario, comentarios))
            rel = os.path.relpath(caminho, RAIZ).replace("\\", "/")
            for m, ln in _atributos(codigo):
                if cp.bloco_chaves(codigo, m.start()) is None:
                    fallback += 1
                if re.search(PADRAO_TIPO, _trecho_antigo(cp, codigo, m)) is None:
                    antigos.append((rel, ln))
                try:
                    achou = re.search(PADRAO_TIPO, cp.trecho_do_patch(codigo, m.start(), rec, arcmod))
                except arcmod.Falhou:
                    achou = None
                if achou is None:
                    novos.append((rel, ln))
    print("varredura do repo: %d arquivo(s) .cs | janela de 2000 disparou %d vez(es)"
          % (len(cs), fallback))
    return cs, antigos, novos, fallback


def corpo():
    cp, rec, arcmod = _modulo_do_check()
    _primitivo(cp, rec, arcmod)
    _direcao_1(cp, rec, arcmod)
    _direcao_2(cp, rec, arcmod)

    cs, antigos, novos, fallback = _varredura_do_repo(cp, rec, arcmod)
    # O conserto nao pode mudar NENHUM veredito real no repositorio.
    arc.exigir(antigos == novos,
               "o conserto mudou o veredito de algum `[HarmonyPatch]` no repo:\n  janela: %r\n  "
               "recorte: %r" % (antigos, novos))
    # E a janela nunca disparava em fonte valida — por isso passava despercebida.
    arc.exigir(fallback == 0,
               "a janela de 2000 disparou %d vez(es) no repo — a varredura do FORMATO-4 dizia 0" % fallback)
    arc.exigir(not antigos, "o repo tem %d `[HarmonyPatch]` sem assinatura por TIPO: %r" % (len(antigos), antigos))

    print("FORMATO-6: o recorte da regra 2 e estrutural (recorte.py) e falha alto; o retoque "
          "inofensivo de >2000 chars nao quebra o veredito, o defeito real (nome em string) "
          "continua pego, e o veredito do repo e identico (0 achados, 0 fallback de janela)")


if __name__ == "__main__":
    arc.main(META, corpo)
