#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_patches.py - TRV-1: as 5 regras de robustez dos patches Harmony, verificadas a maquina.

POR QUE ESTA FERRAMENTA EXISTE
------------------------------
Uma auditoria a mao dos 8 projetos do repo achou 5 defeitos de ROBUSTEZ que este projeto
paga caro para descobrir - o pior deles derivou em 112 NullReferenceException por frame e
travou uma batalha do dono: um patch que lia o ARGUMENTO ERRADO por posicao (`ref __3` num
metodo cuja assinatura tinha mudado). A auditoria levou tempo e foi feita uma vez; aqui ela
vira verificacao MECANICA, que roda a cada push e le SO o repositorio (sem compilar, sem
DLL, sem abrir o jogo).

As 5 regras, todas lidas dos .cs:

  1. POSICIONAL   - nenhum parametro posicional do Harmony (`__0`, `__1`, `__2`, ...). Um
                    indice aponta para o argumento/ tipo ERRADO quando a assinatura do jogo
                    muda, e o patch passa a mexer em outra coisa EM SILENCIO. Excecao
                    documentada: se o parametro estiver justificado em comentario do MESMO
                    bloco (a assinatura explicita por tipo e o uso do slot declarados), a
                    trava NAO reprova - mas imprime o achado como AVISO.
  2. ASSINATURA   - todo `[HarmonyPatch]` tem de ter assinatura por TIPO no bloco do patch
                    (`new Type[] { ... }` / `new[] { typeof(...) }` / `nameof(...)`), nunca
                    "o primeiro metodo chamado X". Heuristica: `typeof(`/`nameof(` no bloco.
  3. TRY/CATCH    - todo metodo de patch (Prefix/Postfix) tem de estar protegido: `try` no
                    proprio corpo, ou delegacao a um metodo do MESMO arquivo que tem `try`.
                    Sem isso, uma excecao no gancho quente (por frame, por hover) inunda o
                    log e pode derrubar a acao do jogador.
  4. MARCADOR     - todo Plugin.cs tem de logar uma linha de VIDA ("... carregado."). Se essa
                    linha nao aparece no LogOutput.log, o plugin nao carregou - e sem ela o
                    teste de ciclo conclui "carregado" sem ter como saber.
  5. APLICADOR    - cada mod tem de aplicar os ganchos UM A UM (o `processador.Patch()` do
                    projeto), nao `PatchAll()` puro: `PatchAll()` e tudo-ou-nada, um gancho
                    ruim deixa todos os outros sem aplicar e em silencio.

COMO LER A SAIDA
----------------
  REPROVA  - achado mecanico e inequivoco (regras 1 sem justificativa, 2 e 4). exit 1.
  AVISO    - achado real que o projeto ja aceitou de forma documentada (regra 1 justificada)
             ou que depende de refatoracao humana ja mapeada (regras 3 e 5). NAO reprova -
             mas e impresso com arquivo:linha, para nao virar ponto cego.

Exit codes: 0 = nada que reprova, 1 = achado que reprova, 2 = nao conseguiu verificar.

USO
---
    python tools/check_patches.py

Roda no ritual de release (tools/release-check.sh, passo 2) e no CI
(.github/workflows/validate.yml, passo 3), na mesma posicao: so le o repositorio, entao
vem ANTES do build e do ciclo do jogo - um `__3` errado nao pode chegar a ser instalado.
"""
import importlib.util
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# nome do token de posicao do Harmony: __0, __1, __2, ...
POSICIONAL = re.compile(r"__(\d+)\b")

# palavras que, num COMENTARIO do mesmo bloco, justificam um slot posicional. A charada
# e separar "documentei o slot" de "proibi o slot": o comentario que PROIBE (`NUNCA se usa
# parametro posicional`) nao pode servir de justificativa. Por isso a justificativa exige
# DUAS coisas no MESMO bloco de comentario contiguo: a palavra-chave da assinatura E o
# token no formato de DECLARACAO (`__2 = GameFunctionParameters`).
PALAVRAS_ASSINATURA = ("assinatura", "por tipo", "slot", "explicit", "ordem dos parametros")
DOC_DO_TOKEN = r"__%s\s*[=:]"

# metodos que o Harmony chama
METODOS_DE_PATCH = ("Prefix", "Postfix", "Finalizer", "Transpiler")


# ---------------------------------------------------------------------------
# leitura: separar CODIGO de COMENTARIO preservando a linha (arquivo:linha importa)
# ---------------------------------------------------------------------------

def separar(texto):
    """Devolve (codigo, sem_comentario, comentarios).

    Os TRES textos tem o MESMO comprimento e o MESMO numero de linhas (o que e apagado vira
    espaco), entao qualquer indice/linha vale nos tres:

      codigo        - strings E comentarios apagados. E sobre ele que as buscas ESTRUTURAIS
                      rodam: a mencao a `__3` dentro de um comentario/doc/string nunca vira
                      achado, e um `{` dentro de uma string nao desalinha a contagem de chaves.
      sem_comentario- so os comentarios apagados, strings INTACTAS. E sobre ele que se procura
                      o TEXTO logado (o marcador 'carregado' mora dentro de uma string).
      comentarios   - lista [(linha, conteudo)], para justificar a excecao da regra 1.
    """
    codigo, sem_comentario, comentarios = [], [], []
    i, n, linha = 0, len(texto), 1
    while i < n:
        c = texto[i]
        if c == "\n":
            codigo.append(c)
            sem_comentario.append(c)
            linha += 1
            i += 1
            continue
        # comentario de linha
        if texto.startswith("//", i):
            j = texto.find("\n", i)
            j = n if j < 0 else j
            comentarios.append((linha, texto[i:j]))
            codigo.append(" " * (j - i))
            sem_comentario.append(" " * (j - i))
            i = j
            continue
        # comentario de bloco
        if texto.startswith("/*", i):
            j = texto.find("*/", i)
            j = n if j < 0 else j + 2
            trecho = texto[i:j]
            for k, pedaco in enumerate(trecho.split("\n")):
                comentarios.append((linha + k, pedaco))
            vazio = "".join(("\n" if ch == "\n" else " ") for ch in trecho)
            codigo.append(vazio)
            sem_comentario.append(vazio)
            linha += trecho.count("\n")
            i = j
            continue
        # string normal ou verbatim ($"..." / @"..."): apaga o conteudo (evita que uma
        # chave `{` de interpolacao quebre a contagem de chaves do bloco)
        if c == '"':
            verbatim = i > 0 and texto[i - 1] == "@"
            j = i + 1
            while j < n:
                if not verbatim and texto[j] == "\\":
                    j += 2
                    continue
                if texto[j] == '"':
                    if verbatim and j + 1 < n and texto[j + 1] == '"':
                        j += 2
                        continue
                    j += 1
                    break
                if texto[j] == "\n":
                    break
                j += 1
            trecho = texto[i:j]
            codigo.append("".join(("\n" if ch == "\n" else " ") for ch in trecho))
            sem_comentario.append(trecho)
            linha += trecho.count("\n")
            i = j
            continue
        # literal de caractere ('{', '\n', '"'): sem isto um `'{'` desalinha as chaves
        if c == "'" and i + 1 < n:
            j = i + 1
            if texto[j] == "\\" and j + 1 < n:
                j += 2
            else:
                j += 1
            if j < n and texto[j] == "'":
                codigo.append("   ")
                sem_comentario.append(texto[i:j + 1])
                i = j + 1
                continue
        codigo.append(c)
        sem_comentario.append(c)
        i += 1
    return "".join(codigo), "".join(sem_comentario), comentarios


def bloco_chaves(texto, pos):
    """(inicio, fim) do primeiro bloco `{ ... }` balanceado a partir de `pos`, ou None."""
    k = texto.find("{", pos)
    if k < 0:
        return None
    prof = 0
    for p in range(k, len(texto)):
        if texto[p] == "{":
            prof += 1
        elif texto[p] == "}":
            prof -= 1
            if prof == 0:
                return (k, p)
    return None


def argumentos_da_chamada(texto, pos_do_nome):
    """Texto entre os parenteses da chamada/metodo cujo nome comeca em `pos_do_nome`."""
    j = texto.find("(", pos_do_nome)
    if j < 0:
        return None, None
    prof, p = 0, j
    while p < len(texto):
        if texto[p] == "(":
            prof += 1
        elif texto[p] == ")":
            prof -= 1
            if prof == 0:
                return j + 1, p
        p += 1
    return j + 1, len(texto)


def linha_de(texto, pos):
    return texto[:pos].count("\n") + 1


# ---------------------------------------------------------------------------
# alvos: cada pasta de projeto com Plugin.cs (inclui o harness ReloadProbe)
# ---------------------------------------------------------------------------

def carregar_empacotador():
    """O `pack-thunderstore.py` e a fonte unica do que e "mod Thunderstore"."""
    caminho = os.path.join(RAIZ, "tools", "pack-thunderstore.py")
    spec = importlib.util.spec_from_file_location("pack_thunderstore", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def arquivos_cs(pasta):
    """Todos os .cs do projeto, SEM bin/ e obj/ (codigo gerado nao e patch de ninguem)."""
    achados = []
    for base, dirs, nomes in os.walk(pasta):
        dirs[:] = [d for d in dirs if d not in ("bin", "obj")]
        for nome in sorted(nomes):
            if nome.endswith(".cs"):
                achados.append(os.path.join(base, nome))
    return sorted(achados)


def relativo(caminho):
    return os.path.relpath(caminho, RAIZ).replace("\\", "/")


# ---------------------------------------------------------------------------
# as 5 regras
# ---------------------------------------------------------------------------

DECLARACAO_METODO = re.compile(
    r"\b(?:private|public|internal|protected|static|virtual|override|sealed|async|partial)\b"
    r"(?:\s+(?:private|public|internal|protected|static|virtual|override|sealed|async))*"
    r"\s+(?:[A-Za-z_][\w<>\[\],.?]*\s+)?([A-Za-z_]\w*)\s*\(")


def metodos(codigo):
    """[(nome, linha, pos_dos_parametros, texto_dos_parametros, corpo)] das DECLARACOES de metodo.

    So declaracao (com modificador - o Harmony exige `static`): `processador.Patch()` e
    `new Harmony(...)` nao entram. E o unico lugar onde um `__N` pode ser declarado, entao e
    por aqui que a regra 1 separa DECLARACAO de USO (`__2.Target`).
    """
    achados = []
    for m in DECLARACAO_METODO.finditer(codigo):
        ini, fim = argumentos_da_chamada(codigo, m.end() - 1)
        b = bloco_chaves(codigo, m.end())
        achados.append((m.group(1), linha_de(codigo, m.start()), ini or m.end(),
                        codigo[ini:fim] if ini is not None else "",
                        codigo[b[0]:b[1]] if b else ""))
    return achados


def regra1_posicional(cs):
    """(reprovam, avisos) de parametro posicional, por arquivo.

    Procura `__N` na LISTA DE PARAMETROS das declaracoes de metodo - nunca no corpo: apontar
    cada `__2.Target` seria ruido, e o que o patch declara e o que decide qual argumento do
    jogo ele recebe.
    """
    reprovam, avisos = [], []
    for caminho, codigo, _, comentarios in cs:
        for _, _, pos, params, _ in metodos(codigo):
            for m in POSICIONAL.finditer(params):
                token = m.group(1)
                ln = linha_de(codigo, pos + m.start())
                # bloco de comentario CONTIGUO em volta (a doc costuma ficar logo acima) - a
                # justificativa tem de estar no MESMO bloco, nao em qualquer lugar do arquivo
                bloco = [txt for (l, txt) in comentarios if ln - 25 <= l <= ln + 3]
                junto = " ".join(bloco)
                tem_palavra = any(p in junto.lower() for p in PALAVRAS_ASSINATURA)
                tem_declaracao = re.search(DOC_DO_TOKEN % re.escape(token), junto) is not None
                if tem_palavra and tem_declaracao:
                    avisos.append((caminho, ln, "__" + token,
                                   "slot justificado no comentario do bloco"))
                else:
                    reprovam.append((caminho, ln, "__" + token,
                                     "parametro posicional do Harmony sem justificativa"))
    return reprovam, avisos


def regra2_assinatura(cs):
    """(reprovam, total) de classes de patch sem assinatura por TIPO."""
    reprovam, total = [], 0
    for caminho, codigo, _, _ in cs:
        for m in re.finditer(r"\[HarmonyPatch\b", codigo):
            total += 1
            ln = linha_de(codigo, m.start())
            bloco = bloco_chaves(codigo, m.start())
            trecho = codigo[m.start():bloco[1]] if bloco else codigo[m.start():m.start() + 2000]
            if not re.search(r"\b(typeof|nameof)\s*\(", trecho):
                reprovam.append((caminho, ln, "[HarmonyPatch]",
                                 "sem assinatura por TIPO (nenhum typeof/nameof no bloco)"))
    return reprovam, total


def regra3_try(cs):
    """(avisos, total) de metodos de patch fora de try/catch (direto ou por delegacao)."""
    avisos, total = [], 0
    for caminho, codigo, _, _ in cs:
        declarados = metodos(codigo)
        corpos = {}
        for nome, _, _, _, corpo in declarados:
            if nome not in corpos:
                corpos[nome] = corpo
        for nome, ln, _, _, corpo in declarados:
            if nome not in METODOS_DE_PATCH:
                continue
            total += 1
            if "try" in corpo:
                continue
            # delegacao: o corpo chama um metodo do MESMO arquivo, e esse tem try
            chamados = set(re.findall(r"\b([A-Za-z_]\w*)\s*\(", corpo))
            if any(n in corpos and "try" in corpos[n] for n in chamados):
                continue
            avisos.append((caminho, ln, nome, "patch sem try/catch (nem por delegacao)"))
    return avisos, total


def regra4_marcador(codigo, sem_comentario):
    """(ok, linha) se o Plugin.cs loga uma linha de vida ('... carregado.') por LogInfo/Log.

    A chamada e localizada no texto SEM comentario mas COM as strings intactas (o marcador mora
    dentro de uma string); os parenteses da chamada sao resolvidos no texto sem strings, para
    que um `(` dentro de um texto logado nao confunda o fim da chamada.
    """
    for m in re.finditer(r"\b(LogInfo|Log|Info|LogMessage)\s*\(", sem_comentario):
        ini, fim = argumentos_da_chamada(codigo, m.start())
        if ini is not None and "carregado" in sem_comentario[ini:fim]:
            return True, linha_de(sem_comentario, m.start())
    return False, None


def regra5_aplicador(codigo):
    """(ok, detalhe): o mod aplica os ganchos um a um em vez de PatchAll() puro?"""
    tem_patchall = re.search(r"\bPatchAll\s*\(", codigo) is not None
    tem_um_a_um = re.search(r"\.Patch\s*\(|\bCreateClassProcessor\s*\(", codigo) is not None
    if tem_um_a_um:
        return True, "aplicador proprio (gancho a gancho)"
    if tem_patchall:
        return False, "PatchAll() puro (um gancho ruim derruba os outros)"
    return False, "nenhum aplicador de patch encontrado no Plugin.cs"


# ---------------------------------------------------------------------------

def main():
    try:
        empacotador = carregar_empacotador()
    except Exception as erro:  # noqa: BLE001 - qualquer falha aqui e "nao consegui verificar"
        print("nao consegui carregar tools/pack-thunderstore.py (fonte unica do que e mod):")
        print("  %s: %s" % (type(erro).__name__, erro))
        return 2

    pastas = []
    for entrada in sorted(os.listdir(RAIZ)):
        pasta = os.path.join(RAIZ, entrada)
        if os.path.isdir(pasta) and os.path.isfile(os.path.join(pasta, "Plugin.cs")):
            pastas.append(entrada)
    if not pastas:
        print("nao achei nenhuma pasta com Plugin.cs na raiz de %s" % RAIZ)
        return 2

    mods = empacotador.descobrir_mods()
    harness = [p for p in pastas if p not in mods]

    cs = []
    por_pasta = {}
    for pasta in pastas:
        por_pasta[pasta] = []
        for caminho in arquivos_cs(os.path.join(RAIZ, pasta)):
            try:
                texto = io.open(caminho, encoding="utf-8", errors="replace").read()
            except IOError as erro:
                print("nao consegui ler %s: %s" % (relativo(caminho), erro))
                return 2
            codigo, sem_comentario, comentarios = separar(texto)
            cs.append((caminho, codigo, sem_comentario, comentarios))
            por_pasta[pasta].append((caminho, codigo, sem_comentario, comentarios))

    # projeto que nao tem [HarmonyPatch] nenhum (harness de teste) nao entra nas regras 2, 3 e 5
    def tem_patch(lista):
        return any(re.search(r"\[HarmonyPatch\b", c) for _, c, _, _ in lista)

    patchudos = [p for p in pastas if tem_patch(por_pasta[p])]

    print("repo   : %s" % RAIZ)
    print("mods   : %d (%s)" % (len(mods), ", ".join(mods) or "nenhum"))
    if harness:
        print("harness: %s (tem Plugin.cs e entra na trava, mas nao e pacote Thunderstore)"
              % ", ".join(harness))
    print("alvos  : %d projetos (%d com patch Harmony) | %d arquivos .cs (bin/ e obj/ fora)"
          % (len(pastas), len(patchudos), len(cs)))
    print()

    # ---- 1. posicional ----------------------------------------------------
    r1_reprovam, r1_avisos = regra1_posicional(cs)
    print("== REGRA 1: parametro posicional do Harmony (__0/__1/__2/...) ==")
    for caminho, ln, token, det in r1_avisos:
        print("  AVISO   %s:%d  %s  (%s)" % (relativo(caminho), ln, token, det))
    for caminho, ln, token, det in r1_reprovam:
        print("  REPROVA %s:%d  %s  (%s)" % (relativo(caminho), ln, token, det))
    if not r1_avisos and not r1_reprovam:
        print("  ok      nenhum parametro posicional declarado em patch nenhum")
    print("  -> %d sem justificativa, %d justificado(s) (aviso)"
          % (len(r1_reprovam), len(r1_avisos)))

    # ---- 2. assinatura por tipo ------------------------------------------
    r2_reprovam, r2_total = regra2_assinatura(cs)
    print("== REGRA 2: assinatura por TIPO em todo [HarmonyPatch] (typeof/nameof) ==")
    for caminho, ln, token, det in r2_reprovam:
        print("  REPROVA %s:%d  %s  (%s)" % (relativo(caminho), ln, token, det))
    print("  -> %d de %d classes de patch com assinatura por TIPO"
          % (r2_total - len(r2_reprovam), r2_total))

    # ---- 3. try/catch ----------------------------------------------------

    r3_avisos, r3_total = regra3_try(cs)
    print("== REGRA 3: todo Prefix/Postfix dentro de try/catch ==")
    for caminho, ln, token, det in r3_avisos:
        print("  AVISO   %s:%d  %s  (%s)" % (relativo(caminho), ln, token, det))
    print("  -> %d de %d metodos de patch protegidos" % (r3_total - len(r3_avisos), r3_total))

    # ---- 4. marcador de vida ---------------------------------------------
    print("== REGRA 4: marcador de vida no boot ('... carregado.') ==")
    r4_reprovam = []
    for pasta in pastas:
        caminho = os.path.join(RAIZ, pasta, "Plugin.cs")
        achado = [c for c in por_pasta[pasta] if c[0] == caminho]
        if not achado:
            r4_reprovam.append((caminho, 0, pasta, "Plugin.cs nao entrou na varredura"))
            print("  REPROVA %s  (nao entrou na varredura)" % relativo(caminho))
            continue
        ok, ln = regra4_marcador(achado[0][1], achado[0][2])
        if ok:
            print("  ok      %s:%d  log de carregamento presente" % (relativo(caminho), ln))
        else:
            r4_reprovam.append((caminho, 0, pasta, "nenhuma linha 'carregado' em LogInfo/Log"))
            print("  REPROVA %s  (sem linha de 'carregado' em LogInfo/Log)"
                  % relativo(caminho))
    print("  -> %d de %d Plugin.cs com marcador de vida"
          % (len(pastas) - len(r4_reprovam), len(pastas)))

    # ---- 5. aplicador proprio -------------------------------------------
    r5_avisos = []
    print("== REGRA 5: aplicacao gancho a gancho (nao PatchAll() puro) ==")
    for pasta in pastas:
        caminho = os.path.join(RAIZ, pasta, "Plugin.cs")
        achado = [c for c in por_pasta[pasta] if c[0] == caminho]
        if not achado:
            continue
        if not tem_patch(por_pasta[pasta]):
            print("  n/a     %-30s sem [HarmonyPatch] no projeto (nao aplica gancho)" % pasta)
            continue
        ok, detalhe = regra5_aplicador(achado[0][1])
        if ok:
            print("  ok      %-30s %s" % (pasta, detalhe))
        else:
            r5_avisos.append((caminho, 0, pasta, detalhe))
            print("  AVISO   %-30s %s" % (pasta, detalhe))
    print("  -> %d de %d projetos com patch usam aplicador proprio (aviso nos demais)"
          % (len(patchudos) - len(r5_avisos), len(patchudos)))

    # ---- contagem final ---------------------------------------------------
    reprovam = r1_reprovam + r2_reprovam + r4_reprovam
    avisos = r1_avisos + r3_avisos + r5_avisos
    print()
    print("CONTAGEM: %d projeto(s) | %d arquivo(s) .cs | %d achado(s) que REPROVAM | %d aviso(s)"
          % (len(pastas), len(cs), len(reprovam), len(avisos)))

    if reprovam:
        print(">>> TRAVA REPROVADA (TRV-1) <<<")
        for caminho, ln, token, det in reprovam:
            print("    %s:%s  %s  ->  %s" % (relativo(caminho), ln or "-", token, det))
        if r1_reprovam:
            print("    O parametro posicional aponta para o argumento ERRADO se a assinatura do")
            print("    jogo mudar - foi essa a familia de defeito que encheu o log com 112")
            print("    NullReferenceException por frame e travou a batalha. Use o NOME do")
            print("    parametro (`ref string description`) e declare a assinatura por TIPO.")
        if r4_reprovam:
            print("    Sem a linha de 'carregado' o teste de ciclo nao tem como saber se o")
            print("    plugin subiu - o silencio parece sucesso.")
        return 1

    print("==> trava OK (TRV-1): 0 posicional sem justificativa; %d/%d classes de patch com"
          % (r2_total - len(r2_reprovam), r2_total))
    print("    assinatura por TIPO; %d/%d metodos de patch protegidos; %d/%d Plugin.cs com"
          % (r3_total - len(r3_avisos), r3_total, len(pastas) - len(r4_reprovam), len(pastas)))
    print("    marcador de vida. %d aviso(s) NAO reprovam (ver 'COMO LER A SAIDA' no cabecalho)."
          % len(avisos))
    return 0


if __name__ == "__main__":
    sys.exit(main())
