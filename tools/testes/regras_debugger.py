#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_debugger.py - as regras do DUMP (RoguelikeDebugger) em codigo testavel (TST-5).

O QUE ESTE MODULO E
-------------------
A biblioteca da familia de testes do dump. Ela existe para uma regra morar num lugar
so e para que os testes nao digitem nem regex nem conta:

  * CARREGA o `tools/census.py` do repositorio (read-only) - as MESMAS regexes que o
    censo usa (`LINE`, `FIELD`, `DESC`), nunca uma copia digitada;
  * LE o fonte VIVO do dump (`RoguelikeDebugger/EfeitosInfo.cs` e os patches) e diz o
    que esta ESTRUTURALMENTE preso (recorte por casamento de chaves, `recorte.py`);
  * TRANSCREVE o que NAO roda sem o jogo (Unity `Material`/`AssetBundle` nao se
    instanciam fora da partida): o `Limpa` (saneamento) e o `Descreve` por REFLEXAO x
    por CAST.

A REGRA QUE ELE AJUDA A PRENDER (docs/DEBUGGER.md)
--------------------------------------------------
1. `desc=` continua por ULTIMO na linha; campo novo entra ANTES dele.
2. Nenhum valor pode conter `|` (o separador do censo) nem quebra de linha - o `|`
   TRUNCA a extracao em SILENCIO (`FIELD` usa `[^|]+`), a quebra perde a linha toda.
3. Um tipo concreto NOVO tem de sair no dump SEM RECOMPILAR: a leitura e por
   REFLEXAO, nunca por cast `as GeneralEffect` (o cast devolve null em silencio e o
   dado - com o tipo junto - desaparece do dump). Foi um defeito REAL do mod.
4. As categorias e as colunas do censo sao contrato: nenhum campo pode desaparecer.

O QUE ESTE MODULO NAO PROVA
---------------------------
Nao executa o C# do mod (pediria a `lib/` do jogo e um harness por test). A ligacao
entre o modelo e o codigo e a checagem ESTRUTURAL do fonte vivo.
"""
import importlib.util
import os
import re

import arcabouco as arc
import recorte as rec

# --------------------------------------------------------------- localizacao ---

FONTES = {
    "efeitos": os.path.join("RoguelikeDebugger", "EfeitosInfo.cs"),
    "status": os.path.join("RoguelikeDebugger", "Patches", "ActionStatusInventoryPatch.cs"),
    "skill": os.path.join("RoguelikeDebugger", "Patches", "SkillInventoryPatch.cs"),
    "item": os.path.join("RoguelikeDebugger", "Patches", "ItemInventoryPatch.cs"),
    "powerup": os.path.join("RoguelikeDebugger", "Patches", "PowerupInventoryPatch.cs"),
}

# Marcadores do inicio da linha `[Categoria] '...'` no `Plugin.Log.LogInfo($"...")`.
MARCADOR_STATUS = "\"[Status] '"
MARCADOR_SKILL = "\"[Skill] '"
MARCADOR_ITEM = "\"[Item] '"
MARCADOR_ITEMMOD = "\"[ItemMod] '"
MARCADOR_POWERUP = "\"[Powerup] '"
MARCADOR_SUMMON = "\"[Summon] '"


# -------------------------------------------------------------------- fontes ---

def caminho_do_repo(*partes):
    return os.path.join(arc.raiz_do_repo(), *partes)


def le_fonte(chave):
    """Le um arquivo do dump pelo apelido de `FONTES`."""
    caminho = caminho_do_repo(FONTES[chave])
    arc.exigir(os.path.isfile(caminho), "nao achei o fonte do dump: %s" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def le_censo_texto():
    caminho = caminho_do_repo("tools", "census.py")
    arc.exigir(os.path.isfile(caminho), "nao achei tools/census.py no repo")
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def carrega_censo():
    """Importa `tools/census.py` (read-only; o import so compila as regexes)."""
    caminho = caminho_do_repo("tools", "census.py")
    spec = importlib.util.spec_from_file_location("census_tst5", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- regexes do censo ---

def chaves_do_field(censo):
    """As chaves que o `FIELD` do censo reconhece (o grupo `key`, em ordem)."""
    m = re.search(r"\(\?P<key>([^)]+)\)", censo.FIELD.pattern)
    arc.exigir(m, "nao achei o grupo `key` no FIELD do census.py (o alternation mudou de forma?)")
    return m.group(1).split("|")


def cabecalhos_do_censo(censo):
    """`{categoria: (arquivo, [colunas])}` lido do proprio `CATS`."""
    return {cat: (arquivo, list(colunas)) for cat, (arquivo, colunas) in censo.CATS.items()}


# ---------------------------------------------------------------- o que o fonte emite ---

def campos_emitidos(codigo, marcador):
    """A lista ORDENADA de `<campo>=` que o `Plugin.Log.LogInfo($"...")` monta.

    Le o texto EFETIVO (sem comentario - citacao em comentario nao e codigo), tira as
    interpolacoes `{expr}` e devolve os nomes de campo na ordem em que saem na linha.
    E o que permite dizer `desc=` e o ULTIMO sem digitar a ordem no teste.
    """
    efetivo = rec.codigo_efetivo(codigo)
    i = efetivo.find(marcador)
    arc.exigir(i >= 0, "nao achei o marcador %r no fonte" % marcador)
    j = efetivo.find(");", i)
    arc.exigir(j > i, "nao achei o fim do LogInfo ();) apos %r" % marcador)
    trecho = efetivo[i:j]
    sem_interpolacao = re.sub(r"\{[^{}]*\}", "", trecho)   # tira {expr}
    return re.findall(r"([a-z][A-Za-z0-9]*)=", sem_interpolacao)


# ---------------------------------------------------------------- parser do censo ---

def confere_linha(censo, linha):
    """Aplica as regexes do censo a UMA linha.

    Devolve `(cat, nome, campos, desc, falhas)`. `campos` so traz o que a WHITELIST do
    `FIELD` reconhece; `desc` e None quando o `DESC` nao casa (linha truncada).
    """
    falhas = []
    m = censo.LINE.match(linha)
    if not m:
        return None, None, {}, None, ["LINE nao casou (o prefixo de categoria/`'nome' |` mudou)"]
    rest = m.group("rest")
    campos = {k: v.strip() for k, v in censo.FIELD.findall(rest)}
    dm = censo.DESC.search(rest)
    if dm is None:
        falhas.append("DESC nao achou `desc=\"...\"` ancorado no fim da linha")
    return m.group("cat"), m.group("name"), campos, (dm.group("desc") if dm else None), falhas


def contrato_da_linha(censo, linha, emitidos=None):
    """As violacoes do CONTRATO do censo na linha (vazia = ok).

    O contrato (docs/DEBUGGER.md, "Como estender sem quebrar o censo"):
      * `desc=` e o ULTIMO campo - qualquer campo depois dele perde a descricao;
      * nenhum valor tem `|` (o `FIELD` usa `[^|]+`: um `|` no valor TRUNCA o campo
        em silencio) nem quebra de linha (perde a linha inteira).
    """
    falhas = []
    if "\n" in linha or "\r" in linha:
        falhas.append("a entrada tem quebra de linha (o dump e UMA linha por entrada)")
    m = censo.LINE.match(linha)
    if not m:
        return ["LINE nao casou (o prefixo de categoria/`'nome' |` mudou)"]
    rest = m.group("rest")
    if censo.DESC.search(rest) is None:
        falhas.append("DESC nao ancorou no fim: ha campo DEPOIS do `desc=` (a descricao some)")
    if emitidos is not None and (not emitidos or emitidos[-1] != "desc"):
        falhas.append("o fonte NAO emite `desc=` por ULTIMO (ultimo=%r)"
                      % (emitidos[-1] if emitidos else None))
    for seg in rest.split(" | "):
        if "=" not in seg:
            continue
        chave, valor = seg.split("=", 1)
        chave = chave.strip()
        if chave == "desc":
            continue
        if "|" in valor:
            falhas.append("o valor do campo %r tem '|' - o FIELD trunca em silencio" % chave)
    return falhas


# ---------------------------------------------------------------- saneamento (Limpa) ---

def limpa(s):
    """ESPELHO do `EfeitosInfo.Limpa` (e dos `Limpa` dos patches).

    `(s ?? "").Replace("\\n", " ").Replace("\\r", " ").Replace("|", "/")
              .Replace("\\"", "'").Trim()`
    """
    return (s or "").replace("\n", " ").replace("\r", " ") \
                    .replace("|", "/").replace('"', "'").strip()


def valor_do_campo(v):
    """ESPELHO do `EfeitosInfo.Valor`: asset->nome, vazio/null->`-`, array->`[N]`."""
    if v is None:
        return "-"
    if isinstance(v, str):
        return "-" if v == "" else limpa(v)
    if isinstance(v, (list, tuple, dict)):
        return "[%d]" % len(v)
    return limpa(str(v))


def falhas_do_limpa(codigo):
    """O `Limpa(string s)` do fonte vivo faz as QUATRO trocas + Trim (a regra 2)?"""
    falhas = []
    efetivo = rec.codigo_efetivo(codigo)
    try:
        bloco = rec.corpo_do_metodo(efetivo, "public static string Limpa(string s)")
    except arc.Falhou as erro:
        return ["ESTRUTURA: nao recortei o `Limpa(string s)`: %s" % erro]
    for alvo, o_que in (
        (r'.Replace("\n", " ")', "quebra de linha LF -> espaco"),
        (r'.Replace("\r", " ")', "quebra de linha CR -> espaco"),
        (r'.Replace("|", "/")', "o separador '|' -> '/' (sem ele o FIELD trunca)"),
        (r'''.Replace("\"", "'")''', "aspas -> apostrofo"),
        (".Trim()", "apara as pontas"),
    ):
        if alvo not in bloco:
            falhas.append("o `Limpa` perdeu a troca de %s (procurei %r)" % (o_que, alvo))
    return falhas


def falhas_do_marcador(codigo):
    """O marcador `!erro:<Tipo>` (RD-2F) tem de ser SEGURO para o parser: sem `|`."""
    falhas = []
    efetivo = rec.codigo_efetivo(codigo)
    if 'return "!erro:" + e.GetType().Name;' not in efetivo:
        falhas.append("nao achei o marcador `\"!erro:\" + e.GetType().Name` (RD-2F)")
    # O prefixo do marcador e o nome de um tipo C#: nenhum dos dois tem '|' ou aspas
    # nem espaco - entao o marcador nunca quebra/trunca o censo.
    for texto, o_que in (("!erro:", "o prefixo"), ("NullReferenceException", "um tipo de exemplo")):
        if any(c in texto for c in ("|", '"', "\n")):
            falhas.append("%s do marcador tem caractere proibido: %r" % (o_que, texto))
    if "Convert.ToBase64" in efetivo or "Escape(" in efetivo:
        falhas.append("o marcador foi escapado em vez de limpo - nao e o desenho do RD-2F")
    return falhas


def falhas_do_valor(codigo):
    """O `Valor(object v)` manda string vazia para `-` e passa o texto pelo `Limpa`?"""
    falhas = []
    efetivo = rec.codigo_efetivo(codigo)
    try:
        bloco = rec.corpo_do_metodo(efetivo, "private static string Valor(object v)")
    except arc.Falhou as erro:
        return ["ESTRUTURA: nao recortei o `Valor(object v)`: %s" % erro]
    if 'return "-";' not in bloco:
        falhas.append("`Valor` perdeu o `-` do valor nulo/vazio (vazio nao vira valor inventado)")
    if 'Limpa(s)' not in bloco:
        falhas.append("`Valor` perdeu o `Limpa(s)` - um valor de string sairia CRU no dump")
    if "v as string" not in bloco and "(string)" not in bloco:
        falhas.append("`Valor` nao trata string explicitamente")
    return falhas


def falhas_do_saneamento(codigo_efeitos, codigo_status):
    """Todas as checagens estruturais do SANEAMENTO (Limpa + Valor + marcador)."""
    return falhas_do_limpa(codigo_efeitos) + falhas_do_valor(codigo_efeitos) \
        + falhas_do_marcador(codigo_status)


# ---------------------------------------------------------------- reflexao x cast ---

class GeneralEffect(object):
    """Implementacao 1 de `IEffectInfo` (o unico tipo que o cast antigo enxergava)."""

    def __init__(self, action=""):
        self.Action = action


class CharacterVariableEffectInfo(object):
    """Implementacao 2 (a que o cast antigo DESCARTAVA - o defeito real do mod)."""

    def __init__(self, effect_target="", character_variable_attribute="", amount=""):
        self.EffectTarget = effect_target
        self.CharacterVariableAttribute = character_variable_attribute
        self.Amount = amount


class TerceiroEffectInfo(object):
    """A TERCEIRA implementacao, SIMULADA: o que a reflexao pega sem recompilar."""

    def __init__(self, kind="", value=""):
        self.Kind = kind
        self.Value = value


def _um_por_reflexao(o):
    campos = sorted(vars(o).keys())
    corpo = ";".join("%s=%s" % (k, valor_do_campo(vars(o)[k])) for k in campos)
    return "%s{%s}" % (type(o).__name__, corpo)


def descreve_por_reflexao(arr):
    """ESPELHO do `EfeitosInfo.Descreve`: `indice:Tipo{campo=valor;...}; ...`.

    Le pelo TIPO CONCRETO de cada elemento (`GetType()`/`GetFields`/`GetValue`),
    publica o `Name` do tipo e NUNCA filtra por cast.
    """
    if not arr:
        return ""
    partes = []
    for i, o in enumerate(arr):
        if o is None:
            partes.append("%d:null" % i)
        else:
            partes.append("%d:%s" % (i, _um_por_reflexao(o)))
    return "; ".join(partes)


def descreve_por_cast(arr):
    """O DEFEITO ANTIGO (`e as GeneralEffect`): so o GeneralEffect aparece.

    Todo elemento de outro tipo concreto devolve null no cast e o dado - COM O TIPO
    JUNTO - desaparecia do dump em silencio.
    """
    partes = []
    for i, o in enumerate(arr):
        if isinstance(o, GeneralEffect):
            partes.append("%d:GeneralEffect{Action=%s}" % (i, valor_do_campo(o.Action)))
    return "; ".join(partes)


def descreve(rotulo, arr):
    if rotulo == "reflexao":
        return descreve_por_reflexao(arr)
    if rotulo == "cast":
        return descreve_por_cast(arr)
    raise arc.Falhou("modelo desconhecido: %r" % rotulo)


def falhas_da_reflexao(codigo_efeitos, codigo_status):
    """O caminho do dump usa REFLEXAO (e nao cast) para publicar o tipo concreto?"""
    falhas = []
    efetivo = rec.codigo_efetivo(codigo_efeitos)

    # 1. O overload de `IEffectInfo[]` (o array que o cast antigo percorria) existe e
    #    delega ao core com `origemIEffectInfo = true`.
    try:
        descreve_ip = rec.corpo_do_metodo(efetivo, "public static string Descreve(IEffectInfo[] arr)")
    except arc.Falhou as erro:
        falhas.append("ESTRUTURA: o overload `Descreve(IEffectInfo[])` sumiu: %s" % erro)
        descreve_ip = ""
    if descreve_ip and "DescreveCore(arr, true)" not in descreve_ip:
        falhas.append("`Descreve(IEffectInfo[])` nao delega a `DescreveCore(arr, true)`")

    # 2. O core enumera o array por REFLEXAO (GetValue), nunca por cast.
    try:
        core = rec.corpo_do_metodo(efetivo, "private static string DescreveCore(Array arr, bool origemIEffectInfo)")
    except arc.Falhou as erro:
        falhas.append("ESTRUTURA: nao recortei o `DescreveCore(Array, bool)`: %s" % erro)
        core = ""
    if core:
        if "arr.GetValue(i)" not in core:
            falhas.append("`DescreveCore` nao le o elemento por reflexao (`arr.GetValue(i)`)")
        if "Um(o, origemIEffectInfo)" not in core:
            falhas.append("`DescreveCore` nao delega ao `Um(o, origemIEffectInfo)`")

    # 3. O `Um` publica o NOME DO TIPO CONCRETO e os campos por reflexao.
    try:
        um = rec.corpo_do_metodo(efetivo, "private static string Um(object o, bool origemIEffectInfo)")
    except arc.Falhou as erro:
        falhas.append("ESTRUTURA: nao recortei o `Um(object, bool)`: %s" % erro)
        um = ""
    if um:
        for exigido, o_que in (
            ("o.GetType()", "o TIPO CONCRETO do elemento (`o.GetType()`)"),
            ("t.Name", "o NOME do tipo, lido do `Type` (`t.Name`)"),
            ("sb.Append(nome).Append('{')", "o NOME do tipo PUBLICADO na saida "
             "(`sb.Append(nome).Append('{')` - o `indice:Tipo{...}` do dump)"),
            ("GetFields(BindingFlags.Public | BindingFlags.Instance)",
             "os campos por reflexao (`GetFields(BindingFlags.Public | BindingFlags.Instance)`)"),
            ("f.GetValue(o)", "o valor de cada campo por reflexao (`f.GetValue(o)`)"),
        ):
            if exigido not in um:
                falhas.append("`Um` perdeu %s (procurei %r)" % (o_que, exigido))
        if "as GeneralEffect" in um:
            falhas.append("`Um` faz CAST `as GeneralEffect` sobre a interface: um tipo NOVO "
                          "some do dump em silencio (o defeito que a RV-8b-0g consertou)")
        if "!(o is GeneralEffect)" not in um:
            falhas.append("`Um` perdeu o contador do defeito (`!(o is GeneralEffect)`) - "
                          "sem ele nao ha a prova, no log, de quantos o cast descartaria")

    # 4. O patch de status publica o `efTipos` pelo caminho de REFLEXAO.
    efetivo_st = rec.codigo_efetivo(codigo_status)
    if not re.search(r"EfeitosInfo\.Descreve\(s\.Effects\)", efetivo_st):
        falhas.append("o `[Status]` nao publica o `efTipos` via `EfeitosInfo.Descreve(s.Effects)` "
                      "(a reflexao sobre `IEffectInfo[]`)")
    return falhas


# ------------------------------------------------------------------ o teste final ---

if __name__ == "__main__":
    raise SystemExit("regras_debugger.py e biblioteca dos testes; rode tools/testes/roda_testes.py")
