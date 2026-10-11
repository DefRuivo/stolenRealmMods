#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""integracao.py - KIT-12: costura `alteracao -> cenarios pertinentes -> coleta -> avaliadores -> relatorio`.

O QUE ESTE MODULO E
-------------------
A COSTURA que faltava entre as pecas ja entregues do ciclo CIC. Ele NAO reimplementa
nada: reaproveita, por caminho,

  * `tools/automacao/ciclo/ciclo.py`        (CIC-1) - identidade de fonte/DLL dos bytes
    atuais, fila DECLARATIVA, limite de tentativas, sem-progresso, escalonamento e
    invalidacao por mudanca de fonte;
  * `tools/automacao/ciclo/decisao.py`      (CIC-2) - classificacao "nunca OK por rotulo",
    roteiro humano residual e falhas automaticas;
  * `tools/automacao/kit10/kit10_cenarios.py` - AVALIADOR dos cenarios (criterios do
    contrato v1, marca de fixture propagada fail-closed);
  * `tools/automacao/aceite/relatorio_aceite.py` (AUT-7) - relatorio por mod e o texto
    curto para humano;
  * `tools/automacao/kit12/pertinencia.json` - DADO declarativo mod -> cenarios/frentes.

O que este modulo acrescenta (e so isso):

  1. PERTINENCIA: arquivos alterados do repo -> mods -> cenarios pertinentes. Arquivo
     alterado SEM mapa, mod sem observacao coletada e avaliador indisponivel viram
     LACUNA declarada (nunca silencio, nunca verde).
  2. CADEIA DE IDENTIDADE UNICA: `fonte_sha` + `dll_sha` + `config_sha` + `versao` +
     `sessao` atravessam pertinencia, coleta, criterios, fila e relatorio; o agregado
     `cadeia_sha` viaja em todos eles. Mudanca de qualquer um INVALIDA a aprovacao
     anterior (exit 3).
  3. FILA DECLARATIVA: reusa `ciclo.montar_fila`/`ciclo.fila_da_decisao` e SANITIZA -
     qualquer campo executavel (`comando`, `argv`, `shell`, `exec`, `cmd`, `subprocess`)
     proposto por agente/LLM e MOVIDO para `propostas_nao_executadas`, tanto no ITEM da
     fila quanto no proprio CRITERIO (que senao viajaria executavel para decisao/relatorio).
     NAO existe, neste modulo, caminho de execucao de comando: a fila e para um agente/supervisor
     ler.
  4. PROCEDENCIA CONFRONTADA (fail-closed, rodada 3): a coleta DECLARA os mesmos bytes da rodada?
     O `hash_fonte` da coleta e, por convencao do PRODUTOR VIVO, o sha256 da DLL do INSTRUMENTO
     (probe) - nunca o hash dos arquivos-fonte. Ele e confrontado contra a CADEIA DA DLL
     (`dll_probe_sha` MEDIDO quando disponivel -> `--probe-dll` ou o arquivo que a coleta declara
     em `identidade.arquivo_dll_do_probe`; senao a DLL DECLARADA pela propria coleta; senao o
     alias documentado `hash_fonte == ident["dll_sha"]`) e os campos de cadeia que a coleta
     declarar (`fonte_sha`/`config_sha`/`versao`/`sessao`) sao confrontados com a identidade.
     Divergencia ou ausencia NAO e reescrita em silencio: vira LACUNA nomeada, o valor declarado
     fica preservado (`declaracoes_contraditorias`) e o OK cai (NAO_EXERCITADO). Um instrumento
     apenas DECLARADO (sem bytes em disco para medir) e registrado como LIMITE explicito
     (`coleta.instrumento_origem`), sem rebaixar envelope conforme.
  5. Lacuna tecnica volta ao AGENTE (falha automatica); ao dono so vai o que o criterio
     declarar explicitamente como autorizacao/julgamento visual (`decisao.py` decide).
  6. FRONTEIRAS FECHADAS (KIT-12F, achados F1R-F5R da revisao independente run674):
     config EXPLICITAMENTE solicitada e nao medida (F1R) e instrumento de coleta explicitamente
     solicitado e ilegivel/ausente (F3R) viram LACUNA tecnica nomeada (INCOMPLETO/2), sem
     fallback silencioso; relatorio obrigatorio INDISPONIVEL - modulo ausente ou excecao de
     montagem (F2R) - impede a aprovacao por lacuna/fila (exit 2), sem inventar texto; coleta com
     `observacoes` de tipo invalido (F4R) vira CAUSA tecnica estruturada, nunca traceback/exit1
     nem zero silencioso; e o saneamento de campo executavel alcanca TODOS os criterios, mesmo os
     sem item de fila (F5R), preservando a proposta como auditoria NAO executavel.

O QUE ESTE MODULO NAO PROVA
---------------------------
Fixture testa o AVALIADOR: fixture MARCADA nunca vira prova de runtime (vira
NAO_EXERCITADO). Rodada de coleta em jogo (AUT-4) NAO faz parte deste modulo e exige
autorizacao especifica. Nada aqui instala, abre jogo, carrega save, commita ou publica.
Sem IA, sem rede, sem credencial: stdlib apenas e validacao/relatorio DETERMINISTAS.

CLI
---
    python tools/automacao/kit12/integracao.py --repo <repo> \
        --alterados BetterStats/Plugin.cs --observacoes <obs.json> \
        --resultado <saida.json> [--config <cfg>] [--mod <Nome>] [--limite N]

    python tools/automacao/kit12/integracao.py --repo <repo> --verificar <saida.json>

Exit: 0 = APROVADO_OFFLINE · 1 = REPROVADO/ESCALADO · 2 = INCOMPLETO (lacuna tecnica:
volta ao agente) · 3 = INVALIDADO por mudanca de fonte/DLL/config/versao.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
AUTOMACAO = os.path.dirname(AQUI)
TOOLS = os.path.dirname(AUTOMACAO)
RAIZ_PADRAO = os.path.dirname(TOOLS)

PERTINENCIA_PADRAO = os.path.join(AQUI, "pertinencia.json")
CAMINHO_CICLO = os.path.join(AUTOMACAO, "ciclo", "ciclo.py")
CAMINHO_DECISAO = os.path.join(AUTOMACAO, "ciclo", "decisao.py")
CAMINHO_KIT10 = os.path.join(AUTOMACAO, "kit10", "kit10_cenarios.py")
CAMINHO_ACEITE = os.path.join(AUTOMACAO, "aceite", "relatorio_aceite.py")

ESQUEMA = "KIT-12/cadeia/1"
TAREFA = "t_0a434c97"
LIMITE_PADRAO = 5

OK = "OK"
REPROVADO = "REPROVADO"
NAO_EXERCITADO = "NAO_EXERCITADO"
INDETERMINADO = "INDETERMINADO"

EXIT_OK = 0
EXIT_FALHOU = 1
EXIT_INCOMPLETO = 2
EXIT_INVALIDADO = 3

ESTADO_OK = "APROVADO_OFFLINE"
ESTADO_REPROVADO = "REPROVADO"
ESTADO_ESCALADO = "ESCALADO"
ESTADO_INCOMPLETO = "INCOMPLETO"
ESTADO_INVALIDADO = "INVALIDADO_POR_MUDANCA"

# Vocabulario do KIT-11: campo com ESTE nome e dado, NUNCA instrucao executavel.
CAMPOS_EXECUTAVEIS = ("comando", "argv", "shell", "exec", "cmd", "subprocess",
                      "script_correcao", "comando_correcao", "correcao_comando")

# Campos da cadeia de identidade que atravessam TODA a cadeia.
CAMPOS_CADEIA = ("fonte_sha", "dll_sha", "config_sha", "versao", "sessao", "dll_probe_sha")

# PROCEDENCIA DA COLETA (rodada 3, corrige F5 da revisao run670).
# O PRODUTOR VIVO escreve em `hash_fonte` o sha256 da DLL do INSTRUMENTO de coleta (o probe),
# NAO o hash dos arquivos-fonte do mod:
#   - runtime/coletor.py:636-637 ("o hash de fonte e o sha256 da DLL do probe") e :651-652;
#   - runtime/AUT4Probe/AUT4ProbePlugin.cs:180 (`_res["hash_fonte"] = _hashFonte.Value`);
#   - evidencia real AUT-4-evidencias/r3-confirmada/aut4probe.json (`hash_fonte` ==
#     `identidade.hash_dll_do_probe` == sha256 da AUT4Probe.dll);
#   - convencao do repo: ciclo/test_decisao.py:562-563, aut6/cobertura.py:270-277 (alias
#     `hash_fonte`/`hash_dll` -> canonico `dll_sha`), aut5/test_aut5.py:563 e
#     cenarios/kit09-verdade.entrada.json (`hash_fonte` == `identidade.dll_sha`).
# Portanto a procedencia da coleta e confrontada contra a CADEIA DA DLL/INSTRUMENTO, nunca
# contra `fonte_sha` (hash dos arquivos-fonte).
CAMPOS_INSTRUMENTO = ("hash_dll_do_probe",)      # bloco `identidade` do probe AUT-4
ALIAS_COLETA_DLL = ("dll_sha",)                  # alias documentado: hash_fonte == dll_sha
# Campos da CADEIA DO MOD que a coleta pode declarar (topo ou bloco `identidade`) e que sao
# CONFRONTADOS com a identidade da rodada. `dll_sha` NAO entra aqui: ele e o alias do
# instrumento/cadeia de DLL (semantica dupla seria a ambiguidade de campo que gerou o F5).
CAMPOS_DECLARADOS_CONFRONTAVEIS = ("fonte_sha", "config_sha", "versao", "sessao")

_CACHE = {}


class DependenciaAusente(RuntimeError):
    """Dependencia do ciclo NAO empacotada neste layout (KIT-15F/F9)."""


class ModuloAusente:
    """Sentinel EXPLICITO para uma dependencia ausente neste layout.

    Diferente de `None`, ele nunca e confundido com um modulo carregado: `modo_reduzido`
    e True, `__bool__` e False e QUALQUER acesso a atributo levanta `DependenciaAusente`.
    Assim o chamador pode declarar a lacuna em vez de fingir verde -- e a funcao publica
    (`ciclo()`, `decisao()`, ...) nunca devolve `None` silencioso."""

    modo_reduzido = True

    def __init__(self, nome, caminho):
        self.nome = nome
        self.caminho = caminho

    def __getattr__(self, item):
        raise DependenciaAusente(
            "modulo %s indisponivel neste layout (dependencia nao empacotada): %s"
            % (self.nome, self.caminho))

    def __bool__(self):
        return False

    def __repr__(self):
        return "ModuloAusente(%s)" % self.nome


def _disponivel(mod):
    """True SOMENTE para modulo real carregado; nunca para o sentinel reduzido."""
    return mod is not None and not getattr(mod, "modo_reduzido", False)


# ==========================================================================
# reuso (import por caminho) - nunca duplicar o que ja existe
# ==========================================================================

def _modulo(nome, caminho):
    if nome in _CACHE:
        return _CACHE[nome]
    if not os.path.isfile(caminho):
        _CACHE[nome] = ModuloAusente(nome, caminho)
        return _CACHE[nome]
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:  # modulo presente e quebrado: reportar como ausencia explicita
        _CACHE[nome] = ModuloAusente(nome, caminho)
        return _CACHE[nome]
    _CACHE[nome] = mod
    return mod


def ciclo():
    return _modulo("kit12_ciclo", CAMINHO_CICLO)


def decisao():
    return _modulo("kit12_decisao", CAMINHO_DECISAO)


def kit10():
    return _modulo("kit12_kit10", CAMINHO_KIT10)


def aceite():
    return _modulo("kit12_aceite", CAMINHO_ACEITE)


# ==========================================================================
# infraestrutura minima (stdlib)
# ==========================================================================

def agora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha256_file(caminho):
    if not caminho or not os.path.isfile(caminho):
        return None
    h = hashlib.sha256()
    try:
        with open(caminho, "rb") as fh:
            for bloco in iter(lambda: fh.read(1 << 20), b""):
                h.update(bloco)
    except OSError:
        return None
    return h.hexdigest()


def sha256_mapa(mapa):
    """sha256 canonico de um {chave: valor} (ordem estavel, separador fixo) - deterministico."""
    itens = "\n".join("%s\t%s" % (k, (mapa.get(k) or "")) for k in sorted(mapa or {}))
    return hashlib.sha256(itens.encode("utf-8")).hexdigest()


def _texto(v):
    return str(v).strip() if isinstance(v, str) else ""


def _rel(caminho):
    return str(caminho or "").replace("\\", "/")


def _ler_json(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def _escrever_json(caminho, dados):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=2)


# ==========================================================================
# 1. pertinencia: alteracao -> mod -> cenarios
# ==========================================================================

def carregar_pertinencia(caminho=None):
    """Le o mapa declarativo. Fail-closed: sem mapa nao ha pertinencia, nao ha verde.

    KIT-15F/F9: no layout DISTRIBUIDO o mapa nao e empacotado. Em vez de levantar (o que
    derrubava a integracao inteira), devolve um mapa VAZIO marcado `modo_reduzido`, de forma
    que todo arquivo alterado sai como `nao_mapeado` -> LACUNA -> nada fica verde. O caminho
    do repositorio do autor (mapa presente) permanece identico."""
    caminho = caminho or PERTINENCIA_PADRAO
    if not os.path.isfile(caminho):
        return {"schema": "KIT-12/pertinencia/1", "mods": {}, "modo_reduzido": True,
                "lacunas": ["mapa de pertinencia nao empacotado: %s" % caminho]}
    doc = _ler_json(caminho)
    if not isinstance(doc, dict) or not isinstance(doc.get("mods"), dict):
        raise RuntimeError("mapa de pertinencia invalido (sem `mods`): %s" % caminho)
    return doc


def mods_alterados(repo, base=None, lista=None):
    """Arquivos alterados do repo (tracked modificados + untracked), ordenados.

    `lista` explicita vence (usada pelos testes/sandbox, determinismo). Sem `lista`,
    o git e a fonte: se o git nao responder, levanta - sem lista nao ha pertinencia.
    """
    if lista:
        return sorted({_rel(p) for p in lista if _texto(p)})
    caminhos = set()
    r = subprocess.run(["git", "status", "--porcelain", "-z"], cwd=repo,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise RuntimeError("git status indisponivel em %s (exit %s)" % (repo, r.returncode))
    for tok in r.stdout.decode("utf-8", "replace").split("\0"):
        if len(tok) > 3:
            caminhos.add(_rel(tok[3:]))
    if base:
        r2 = subprocess.run(["git", "diff", "--name-only", "-z", base], cwd=repo,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r2.returncode != 0:
            raise RuntimeError("git diff indisponivel em %s (exit %s)" % (repo, r2.returncode))
        caminhos |= {_rel(p) for p in r2.stdout.decode("utf-8", "replace").split("\0") if p}
    return sorted(caminhos)


def mapear(alterados, pertinencia, mods_explicitos=None):
    """{mod: cenarios/frentes/fonte/arquivos} + arquivos sem mapa.

    Um arquivo alterado que nao casa com nenhum `caminhos` do mapa NAO desaparece:
    ele sai em `nao_mapeados` e vira lacuna declarada.
    """
    mapa_mods = pertinencia.get("mods") or {}
    saida, nao_mapeados = {}, []
    for caminho in sorted(set(alterados or [])):
        achado = None
        for mod in sorted(mapa_mods):
            for prefixo in sorted(mapa_mods[mod].get("caminhos") or []):
                pref = _rel(prefixo).rstrip("/")
                if caminho == pref or caminho.startswith(pref + "/") or caminho == _rel(prefixo):
                    achado = mod
                    break
            if achado:
                break
        if not achado:
            nao_mapeados.append(caminho)
            continue
        d = saida.setdefault(achado, {
            "mod": achado, "arquivos": [],
            "cenarios": list(mapa_mods[achado].get("cenarios") or []),
            "frentes": list(mapa_mods[achado].get("frentes") or []),
            "fonte": list(mapa_mods[achado].get("fonte") or []),
        })
        d["arquivos"].append(caminho)

    for mod in sorted(set(mods_explicitos or [])):
        if mod in saida:
            continue
        if mod not in mapa_mods:
            nao_mapeados.append("<mod-sem-mapa>:%s" % mod)
            continue
        saida[mod] = {"mod": mod, "arquivos": [],
                      "cenarios": list(mapa_mods[mod].get("cenarios") or []),
                      "frentes": list(mapa_mods[mod].get("frentes") or []),
                      "fonte": list(mapa_mods[mod].get("fonte") or [])}
    for mod in sorted(saida):
        saida[mod]["arquivos"] = sorted(saida[mod]["arquivos"])
    return {"mods": {m: saida[m] for m in sorted(saida)}, "nao_mapeados": sorted(nao_mapeados)}


# ==========================================================================
# 2. identidade: fonte + DLL + config + versao + sessao  ->  cadeia_sha
# ==========================================================================

_RE_VERSIONE = re.compile(r"<Version>\s*([^<\s]+)\s*</Version>")


def versao_do_csproj(repo, mod):
    """Versao declarada no csproj do mod (leitura ESTATICA, sem build). None se ausente."""
    caminho = os.path.join(repo, mod, "%s.csproj" % mod)
    if not os.path.isfile(caminho):
        return None
    try:
        with open(caminho, encoding="utf-8", errors="replace") as fh:
            texto = fh.read()
    except OSError:
        return None
    m = _RE_VERSIONE.search(texto)
    return m.group(1) if m else None


def identidade_cadeia(repo, *, configs=(), versao=None, sessao=None, mods=None,
                      coleta_meta=None, probe_dll=None):
    """Identidade UNICA da rodada. A mesma atravessa coleta, criterios, fila e relatorio.

    `dll_probe_sha` e a identidade da DLL do INSTRUMENTO de coleta (probe): MEDIDA quando ha
    bytes em disco (`--probe-dll` ou o arquivo declarado pela coleta), senao DECLARADA pela
    propria coleta - com a origem registrada em `dll_probe_sha_origem`. E contra essa cadeia
    (e o alias `dll_sha`) que a procedencia da coleta e confrontada, nunca contra `fonte_sha`.
    """
    c = ciclo()
    base = {}
    erro = None
    if not _disponivel(c):
        erro = "orquestrador CIC-1 (ciclo.py) indisponivel: sem identidade, nada vira OK"
    else:
        try:
            base = c.identidade(repo)
        except Exception as ex:  # noqa: BLE001
            erro = "identidade indisponivel (%s: %s)" % (type(ex).__name__, ex)
            base = {}

    cfg, cfg_ausentes = {}, []
    for ref in configs or []:
        rel = _rel(ref)
        h = sha256_file(ref if os.path.isabs(ref) else os.path.join(repo, rel))
        if h:
            cfg[rel] = h
        else:
            cfg_ausentes.append(rel)

    versoes = {}
    if versao is None:
        for mod in sorted(mods or []):
            v = versao_do_csproj(repo, mod)
            if v:
                versoes[mod] = v
        versao = "+".join(versoes[m] for m in sorted(versoes)) if versoes else None

    inst_sha, inst_origem, inst_arquivo = instrumento_da_coleta(coleta_meta, probe_dll)
    ident = {
        "fonte_sha": base.get("fonte_sha"),
        "dll_sha": base.get("dll_sha"),
        "dll_probe_sha": inst_sha,
        "dll_probe_sha_origem": inst_origem,
        "dll_probe_sha_arquivo": inst_arquivo,
        "config_sha": sha256_mapa(cfg) if cfg else None,
        "configs": cfg,
        "configs_ausentes": sorted(cfg_ausentes),
        "versao": versao,
        "versoes_por_mod": versoes,
        "sessao": sessao,
        "fonte_arquivos": base.get("fonte_arquivos"),
        "dlls": base.get("dlls") or {},
        "erro": erro,
    }
    ident["cadeia_sha"] = sha256_mapa({k: ident.get(k) for k in CAMPOS_CADEIA})
    return ident


def identidade_suficiente(ident):
    c = ciclo()
    if _disponivel(c):
        return bool(c.identidade_suficiente(ident))
    return bool(_texto((ident or {}).get("fonte_sha")) and _texto((ident or {}).get("dll_sha")))


# ==========================================================================
# 3. coleta: observacoes + procedencia (fixture NUNCA vira runtime)
# ==========================================================================

def declara_fixture(doc):
    """Mesma regra do KIT-10: procedencia fixture / rotulo_fixture / sintetico / evidencia_runtime=False."""
    k = kit10()
    if _disponivel(k) and hasattr(k, "_declara_fixture"):
        return bool(k._declara_fixture(doc))
    if not isinstance(doc, dict):
        return False
    if _texto(doc.get("procedencia")).lower() == "fixture":
        return True
    if doc.get("rotulo_fixture") is True or doc.get("sintetico") is True:
        return True
    return doc.get("evidencia_runtime") is False


def _declarados_na_coleta(doc):
    """(declarados, incoerencias) dos campos de cadeia do MOD que a COLETA declara.

    Le no TOPO e no bloco `identidade` (as duas formas vivas no repo: envelope do AUT-4 e
    `cenarios/kit09-verdade.entrada.json`). Divergencia entre as duas formas e INCOERENCIA
    declarada, nao silencio. `dll_sha` NAO entra aqui (e o alias do instrumento, ver
    `CAMPOS_DECLARADOS_CONFRONTAVEIS`).
    """
    declarados, incoerencias = {}, []
    if not isinstance(doc, dict):
        return declarados, incoerencias
    bloco = doc.get("identidade") if isinstance(doc.get("identidade"), dict) else {}
    for campo in CAMPOS_DECLARADOS_CONFRONTAVEIS:
        topo = _texto(doc.get(campo)) or None
        dentro = _texto(bloco.get(campo)) or None
        if topo and dentro and topo != dentro:
            incoerencias.append({"campo": campo, "topo": topo, "identidade": dentro})
        valor = topo or dentro
        if valor:
            declarados[campo] = valor
    return declarados, incoerencias


def instrumento_da_coleta(coleta_meta, probe_dll=None):
    """(sha, origem, arquivo) da DLL do INSTRUMENTO de coleta.

    Prioridade: MEDICAO - bytes em disco, via `--probe-dll` ou o arquivo que a coleta declara em
    `identidade.arquivo_dll_do_probe` - > DECLARACAO canonica da propria coleta
    (`identidade.hash_dll_do_probe`; na sequencia `identidade.dll_sha` e `dll_sha` de topo, o
    alias documentado). Sem bytes para medir, o instrumento e DECLARADO e o limite fica
    registrado (`origem="declarado-coleta"`), sem inventar medicao.
    """
    meta = coleta_meta or {}
    if probe_dll:
        h = sha256_file(probe_dll)
        return (h, "medido-cli" if h else "probe-ilegivel", os.path.abspath(probe_dll))
    arq = _texto(meta.get("instrumento_arquivo")) or None
    if arq:
        h = sha256_file(arq if os.path.isabs(arq) else os.path.abspath(arq))
        if h:
            return h, "medido-arquivo", arq
    decl = _texto(meta.get("instrumento_declarado")) or None
    if decl:
        return decl, "declarado-coleta", arq
    return None, None, arq


def _validar_observacoes(doc):
    """(observacoes, erro) do campo `observacoes` de um envelope declarado (F4R, fail-closed).

    Formato inesperado NAO vira excecao de infraestrutura (traceback/exit1) nem zero silencioso
    (que pareceria aprovacao): vira CAUSA tecnica declarada. Elemento que nao e objeto tambem e
    dado invalido, nunca uma observacao avaliada.
    """
    if "observacoes" not in doc:
        return [], "envelope sem o campo `observacoes` (esperado: lista de objetos)"
    valor = doc.get("observacoes")
    if valor is None:
        return [], "envelope com `observacoes` nulo (esperado: lista de objetos)"
    if not isinstance(valor, list):
        return [], ("envelope com `observacoes` do tipo %s (esperado: lista de objetos): entrada "
                    "INVALIDA de instrumento, nao defeito de produto" % type(valor).__name__)
    obs, invalidos = [], 0
    for item in valor:
        if isinstance(item, dict):
            obs.append(item)
        else:
            invalidos += 1
    if invalidos:
        return obs, ("envelope com %d elemento(s) de `observacoes` que nao sao objetos (entrada "
                     "INVALIDA de instrumento, nao defeito de produto)" % invalidos)
    return obs, None


def carregar_coleta(caminho):
    """(observacoes, meta) da coleta. Ausente/ilegivel => observacoes vazias + erro declarado."""
    meta = {"caminho": os.path.abspath(caminho) if caminho else None, "sessao": None,
            "hash_fonte": None, "fixture": False, "quantidade": 0, "envelope": False,
            "instrumento_declarado": None, "instrumento_arquivo": None,
            "declarados": {}, "incoerencias": [], "erro": None}
    if not caminho:
        meta["erro"] = "coleta ausente (--observacoes nao informado)"
        return [], meta
    if not os.path.isfile(caminho):
        meta["erro"] = "coleta ausente: %s" % caminho
        return [], meta
    try:
        doc = _ler_json(caminho)
    except (ValueError, OSError) as ex:
        meta["erro"] = "coleta ilegivel: %s" % ex
        return [], meta

    envelope = doc if isinstance(doc, dict) else None
    if isinstance(doc, dict):
        obs, obs_erro = _validar_observacoes(doc)
        bloco = doc.get("identidade") if isinstance(doc.get("identidade"), dict) else {}
        meta["envelope"] = True
        meta["sessao"] = _texto(doc.get("sessao")) or None
        # `hash_fonte` (canonico do produtor) ou `hash_dll` (alias do AUT-6). NUNCA `fonte_sha`:
        # o hash dos arquivos-fonte nao e procedencia de coleta (F5 da revisao run670).
        meta["hash_fonte"] = _texto(doc.get("hash_fonte") or doc.get("hash_dll")) or None
        meta["instrumento_declarado"] = (
            _texto(bloco.get("hash_dll_do_probe"))
            or _texto(bloco.get("dll_sha"))
            or _texto(doc.get("dll_sha")) or None)
        meta["instrumento_arquivo"] = (_texto(bloco.get("arquivo_dll_do_probe"))
                                       or _texto(doc.get("arquivo_dll_do_probe")) or None)
        meta["declarados"], meta["incoerencias"] = _declarados_na_coleta(doc)
        meta["fixture"] = declara_fixture(doc)
        if obs_erro:  # F4R: entrada invalida declarada como CAUSA tecnica (nunca traceback/zero verde)
            meta["erro"] = obs_erro
    elif isinstance(doc, list):
        obs = [o for o in doc if isinstance(o, dict)]
    else:
        meta["erro"] = "coleta em formato inesperado (%s)" % type(doc).__name__
        return [], meta

    if any(declara_fixture(o) for o in obs):
        meta["fixture"] = True
    meta["quantidade"] = len(obs)
    return obs, meta


def pertinentes(observacoes, selecao):
    """(dentro, fora) - observacao de mod nao selecionado NAO e silenciada, e declarada."""
    mods = set(selecao.get("mods") or {})
    dentro, fora = [], []
    for obs in observacoes or []:
        mod = _texto(obs.get("mod"))
        (dentro if mod in mods else fora).append(obs)
    return dentro, fora


# ==========================================================================
# 4. criterios: avaliador real + cadeia + lacunas declaradas
# ==========================================================================

def _criterio_lacuna(cid, mod, motivo, esperado, observado, evidencia=None, extra=None):
    c = {"id": cid, "mod": mod or "transversal", "estado": NAO_EXERCITADO,
         "classe": "offline", "procedencia": "execucao", "prova_runtime": False,
         "esperado": esperado, "observado": observado, "evidencia": list(evidencia or []),
         "motivo": motivo, "tarefa_origem": TAREFA, "tipo_pendencia": "coleta_tecnica",
         "autorizacao_necessaria": False}
    if extra:
        c.update(extra)
    return c


def anexar_cadeia(criterio, ident, origem=None):
    """A identidade da rodada ATRAVESSA o criterio (fonte/dll/config/versao/sessao/cadeia_sha)."""
    for campo in CAMPOS_CADEIA:
        if ident.get(campo) is not None:
            criterio[campo] = ident.get(campo)
    criterio["cadeia_sha"] = ident.get("cadeia_sha")
    if origem:
        criterio["coleta"] = dict(origem)
        caminho = origem.get("caminho")
        if caminho and os.path.isfile(caminho):
            ev = list(criterio.get("evidencia") or [])
            if caminho not in ev:
                ev.append(caminho)
                criterio["evidencia"] = ev
    return criterio


def anexar_causa(criterio, selecao, repo):
    """Aponta a CAUSA quando o mapa declarar um arquivo-fonte que EXISTE (prova de caminho)."""
    if criterio.get("causa"):
        return criterio
    mod = criterio.get("mod")
    for cand in (selecao.get("mods") or {}).get(mod, {}).get("fonte") or []:
        rel = _rel(cand)
        if os.path.isfile(os.path.join(repo, rel)):
            criterio["causa"] = rel
            ev = list(criterio.get("evidencia") or [])
            if rel not in ev:
                ev.append(rel)
            criterio["evidencia"] = ev
            break
    return criterio


def rebaixar_criterio(criterio, motivo):
    """Rebaixa UM criterio OK e ANEXA o motivo (usado pelas contradicoes medidas da cadeia).

    Diferente de `rebaixar_ok`, atinge um criterio especifico: a contradicao e daquele criterio,
    nao da rodada inteira. Nada e apagado - o que ele declarava fica preservado no proprio
    criterio (`declaracoes_contraditorias`) e na lacuna nomeada.
    """
    if criterio.get("estado") == OK:
        criterio["estado"] = NAO_EXERCITADO
        criterio["prova_runtime"] = False
    criterio["motivo"] = (motivo + " | antes: " + str(criterio.get("motivo") or "")).strip()
    return criterio


def rebaixar_ok(criterios, motivo):
    """Nenhum OK sobrevive quando a prova nao vale (identidade/coleta). Igual ao CIC-1."""
    for c in criterios:
        if c.get("estado") == OK:
            c["estado"] = NAO_EXERCITADO
            c["prova_runtime"] = False
            c["motivo"] = (motivo + " | antes: " + str(c.get("motivo") or "")).strip()
    return criterios


def _avaliar_coleta(coleta_meta, ident, probe_dll=None):
    """(achados, confronto) da procedencia da coleta. Fail-closed, sem ambiguidade de campo.

    O `hash_fonte` da coleta e o sha256 da DLL do INSTRUMENTO (probe) - convencao do produtor
    vivo (ver `CAMPOS_INSTRUMENTO`). Confronto, em ordem:
      * instrumento MEDIDO (bytes em disco, `--probe-dll` ou `arquivo_dll_do_probe`) e
        AUTORITATIVO: divergencia do `hash_fonte` e CONTRADICAO;
      * a coleta deve ser COERENTE com o instrumento que ela mesma declara, e o arquivo medido
        deve bater com essa declaracao (senao INCOERENCIA declarada);
      * instrumento apenas DECLARADO e aceito como tal (limite registrado, sem medir bytes que
        nao existem em disco) desde que o `hash_fonte` seja igual a ele;
      * sem instrumento nenhum, vale o alias documentado `hash_fonte == ident["dll_sha"]`;
      * bytes que nao casam com NENHUM campo da identidade continuam INCOMPLETO/exit 2.
    Tambem confronta os campos de cadeia declarados pela COLETA (`fonte_sha`/`config_sha`/
    `versao`/`sessao`) contra a identidade da rodada (S10 da revisao run670).

    Nada e sobrescrito em silencio: cada divergencia vira achado com `declarado` e `identidade`.
    """
    meta = coleta_meta or {}
    ident = ident or {}
    hash_coleta = _texto(meta.get("hash_fonte")) or None
    inst_sha, inst_origem, inst_arquivo = instrumento_da_coleta(meta, probe_dll)
    ident_inst = _texto(ident.get("dll_probe_sha")) or None
    ident_origem = _texto(ident.get("dll_probe_sha_origem")) or None
    if ident_inst is not None:
        # A identidade da rodada manda: ela ja resolveu medicao/declaracao/alias.
        inst_sha, inst_origem = ident_inst, (ident_origem or inst_origem)
    else:
        inst_sha, inst_origem = None, None
    decl_inst = _texto(meta.get("instrumento_declarado")) or None
    ident_dll = _texto(ident.get("dll_sha")) or None
    medido = inst_origem in ("medido-cli", "medido-arquivo")

    achados = []
    confronto = {"hash_fonte": "sem-identidade", "coleta_hash_fonte": hash_coleta,
                 "instrumento_sha": inst_sha, "instrumento_origem": inst_origem,
                 "instrumento_arquivo": inst_arquivo, "declarado_pela_coleta": decl_inst,
                 "campo_identidade": None, "identidade_dll_sha": ident_dll,
                 "confrontos": []}

    if inst_sha is None and ident_dll is None:
        # Identidade insuficiente: ja derruba todo OK adiante (`identidade_suficiente`), com
        # motivo proprio. Nao ha o que confrontar aqui.
        return achados, confronto

    if hash_coleta is None:
        achados.append({"campo": "hash_fonte", "declarado": None,
                        "identidade": inst_sha or ident_dll, "tipo": "ausente"})
        confronto["hash_fonte"] = "ausente"
    elif decl_inst and hash_coleta != decl_inst:
        # A coleta contradiz o instrumento que ELA MESMA declara.
        achados.append({"campo": "hash_fonte", "declarado": hash_coleta, "identidade": decl_inst,
                        "tipo": "incoerente", "via": "instrumento-declarado-pela-coleta"})
        confronto["hash_fonte"] = "incoerente"
    elif medido and inst_sha and hash_coleta != inst_sha:
        achados.append({"campo": "hash_fonte", "declarado": hash_coleta, "identidade": inst_sha,
                        "tipo": "contraditoria", "via": "instrumento-medido"})
        confronto["hash_fonte"] = "contraditoria"
        confronto["campo_identidade"] = "dll_probe_sha(medido)"
    elif not medido and inst_sha and hash_coleta != inst_sha:
        achados.append({"campo": "hash_fonte", "declarado": hash_coleta, "identidade": inst_sha,
                        "tipo": "contraditoria", "via": "instrumento-da-rodada"})
        confronto["hash_fonte"] = "contraditoria"
        confronto["campo_identidade"] = "dll_probe_sha"
    elif not inst_sha and ident_dll and hash_coleta != ident_dll:
        # Sem instrumento nenhum: vale o alias documentado `hash_fonte == dll_sha`.
        achados.append({"campo": "hash_fonte", "declarado": hash_coleta, "identidade": ident_dll,
                        "tipo": "contraditoria", "via": "alias-dll_sha"})
        confronto["hash_fonte"] = "contraditoria"
        confronto["campo_identidade"] = "dll_sha"
    else:
        confronto["hash_fonte"] = "confere"
        confronto["campo_identidade"] = ("dll_probe_sha(medido)" if medido else
                                         "dll_probe_sha" if inst_sha else
                                         "dll_probe_sha(declarado)" if decl_inst else "dll_sha")

    # Instrumento MEDIDO x instrumento DECLARADO pela coleta: os dois nao podem divergir.
    if medido and decl_inst and inst_sha and decl_inst != inst_sha:
        achados.append({"campo": "hash_dll_do_probe", "declarado": decl_inst,
                        "identidade": inst_sha, "tipo": "incoerente",
                        "via": "declaracao-x-medicao"})
        if confronto["hash_fonte"] == "confere":
            confronto["hash_fonte"] = "incoerente"
    if medido and not decl_inst:
        confronto["campo_identidade"] = "dll_probe_sha(medido)"

    # (S10) Campos de cadeia declarados pela COLETA x identidade da RODADA.
    for incoerencia in meta.get("incoerencias") or []:
        achados.append({"campo": incoerencia["campo"], "declarado": incoerencia["topo"],
                        "identidade": incoerencia["identidade"], "tipo": "incoerente",
                        "via": "topo-x-identidade-da-coleta"})
    for campo, declarado in sorted((meta.get("declarados") or {}).items()):
        esperado = _texto(ident.get(campo)) or None
        entrada = {"campo": campo, "declarado": declarado, "identidade": esperado,
                   "tipo": "contraditoria", "via": "campo-declarado-pela-coleta"}
        if esperado is None:
            # Identidade sem esse campo: nada a confrontar, mas a declaracao fica registrada.
            entrada["tipo"] = "nao-confrontavel"
        elif declarado != esperado:
            achados.append(entrada)
        confronto["confrontos"].append({"campo": campo, "declarado": declarado,
                                        "identidade": esperado,
                                        "resultado": ("confere" if declarado == esperado
                                                      else "nao-confrontavel" if esperado is None
                                                      else "contraditoria")})
    return achados, confronto


def confrontar_coleta(coleta_meta, ident):
    """Achados da procedencia da coleta (compativel: devolve a LISTA de achados)."""
    return _avaliar_coleta(coleta_meta, ident)[0]


def confronto_da_coleta(coleta_meta, ident):
    """(achados, confronto) - versao com o registro de QUAL campo da identidade conferiu."""
    return _avaliar_coleta(coleta_meta, ident)


def confrontar_cadeia_declarada(criterios, ident):
    """Confere o que o CRITERIO ja declara contra a identidade da RODADA.

    Criterio que declara `fonte_sha`/`dll_sha`/`config_sha`/`versao`/`sessao` de OUTROS bytes
    aponta para outra rodada: a declaracao e uma CONTRADICAO medida (o CIC-2 a reprova quando
    chega crua) e NAO pode ser reescrita em silencio pela costura. O valor declarado fica
    preservado no criterio e a contradicao e devolvida campo a campo.
    """
    contradicoes = []
    for c in criterios:
        for campo in CAMPOS_CADEIA:
            declarado = c.get(campo)
            esperado = (ident or {}).get(campo)
            if declarado in (None, "") or esperado in (None, ""):
                continue
            if str(declarado) != str(esperado):
                achado = {"criterio": c.get("id"), "campo": campo,
                          "declarado": declarado, "identidade": esperado}
                contradicoes.append(achado)
                c.setdefault("declaracoes_contraditorias", []).append(dict(achado))
                c["declaracao_sobrescrita"] = True
    return contradicoes


def normalizar_declaracoes(criterios):
    """Separa declaracoes INCOERENTES do avaliador (classe x procedencia) do conjunto avaliado.

    Regra do CIC-2: `classe=runtime` com `procedencia` != runtime (e o inverso) e uma
    declaracao incoerente. Isso NAO e defeito do produto nem prova: e uma lacuna da
    cadeia de coleta/avaliacao que volta ao AGENTE. Devolve (criterios_normalizados,
    originais) preservando o criterio ORIGINAL integral para auditoria.
    """
    normalizados, originais = [], []
    for c in criterios:
        classe = _texto(c.get("classe")).lower()
        proc = _texto(c.get("procedencia")).lower()
        motivo = None
        if classe == "runtime" and proc not in ("runtime",):
            motivo = ("classe runtime com procedencia %r: declaracao INCOERENTE do avaliador "
                      "(nao e prova nem defeito do produto; lacuna de coleta/avaliacao)" % proc)
        elif classe == "offline" and proc == "runtime":
            motivo = ("classe offline com procedencia runtime: declaracao INCOERENTE do avaliador "
                      "(nao e prova nem defeito do produto; lacuna de coleta/avaliacao)")
        if motivo is None:
            normalizados.append(c)
            continue
        originais.append(dict(c))
        lacuna = _criterio_lacuna(
            "avaliador/declaracao-incoerente/%s" % c.get("id"), c.get("mod"),
            motivo + " | criterio original: %s (estado=%s, motivo=%s)"
            % (c.get("id"), c.get("estado"), str(c.get("motivo") or "")[:200]),
            str(c.get("esperado") or ""), str(c.get("observado") or ""),
            evidencia=list(c.get("evidencia") or []))
        lacuna["criterio_original"] = c.get("id")
        lacuna["declaracao_original"] = {"classe": c.get("classe"), "procedencia": c.get("procedencia"),
                                        "estado": c.get("estado")}
        normalizados.append(lacuna)
    return normalizados, originais


def criterios_da_cadeia(repo, selecao, observacoes, ident, coleta_meta, pertinencia):
    """(criterios, meta) - avaliador real (KIT-10) sobre as observacoes PERTINENTES + lacunas."""
    criterios = []

    k10 = kit10()
    dentro, fora = pertinentes(observacoes, selecao)
    if _disponivel(k10) and dentro:
        # O avaliador carrega seus oraculos de `tools/testes` (ex.: regras_shrine.py ->
        # `import arcabouco`): sem isso, o oracle nao carrega e o aspecto quebra. Cabe a
        # COSTURA garantir o pre-requisito do avaliador, nao reimplementa-lo.
        for extra in (os.path.join(TOOLS, "testes"), AUTOMACAO):
            if os.path.isdir(extra) and extra not in sys.path:
                sys.path.insert(0, extra)
        try:
            criterios += [c for c in k10.avaliar(dentro, ident) if isinstance(c, dict)]
        except Exception as ex:  # noqa: BLE001
            criterios.append(_criterio_lacuna(
                "avaliador/erro", "transversal",
                "avaliador KIT-10 levantou %s: %s" % (type(ex).__name__, ex),
                "avaliar sem excecao", "excecao"))
    elif k10 is None:
        criterios.append(_criterio_lacuna(
            "avaliador/indisponivel", "transversal",
            "avaliador KIT-10 indisponivel (%s): nada foi avaliado" % CAMINHO_KIT10,
            "avaliador presente", "ausente"))

    # Criterio de OUTRO mod (avaliador de suite emite para todos os alvos): fica FORA da
    # pertinencia desta rodada e NAO vira criterio nem defeito do produto. Nada e apagado:
    # ele e declarado em `fora_da_pertinencia` no resultado (o silencio seria a mentira).
    mods_selecionados = set(selecao.get("mods") or {})
    mods_conhecidos = set((pertinencia.get("mods") or {}))
    principais, fora_da_pertinencia = [], []
    for c in criterios:
        mod = _texto(c.get("mod"))
        # So cai fora o criterio de um mod CONHECIDO do mapa que nao foi alterado nesta rodada.
        # `transversal`/mod desconhecido fica: e lacuna da propria avaliacao e nao pode sumir.
        fora_da_rodada = bool(mod) and mod in mods_conhecidos and mod not in mods_selecionados
        if fora_da_rodada:
            fora_da_pertinencia.append({"id": c.get("id"), "mod": mod, "estado": c.get("estado"),
                                        "classe": c.get("classe"),
                                        "motivo": str(c.get("motivo") or "")[:300]})
            continue
        principais.append(c)
    criterios = principais
    # (2b) declaracao INCOERENTE do avaliador (classe x procedencia): nao e defeito do produto
    # nem prova. Vira LACUNA nomeada que volta ao agente, e o criterio ORIGINAL fica preservado
    # byte a byte em `criterios_originais_do_avaliador` (nada e reescrito em silencio).
    criterios, originais_incoerentes = normalizar_declaracoes(criterios)

    for i, obs in enumerate(fora):
        criterios.append(_criterio_lacuna(
            "pertinencia/observacao-fora/%d" % (i + 1), "transversal",
            "observacao de mod %r nao pertence a esta rodada (%s): NAO foi avaliada"
            % (_texto(obs.get("mod")) or "<sem-mod>", ", ".join(sorted(mods_selecionados)) or "nenhum"),
            "observacao pertinente ao mod alterado",
            _texto(obs.get("objeto")) or "<sem nome>"))

    for caminho in selecao.get("nao_mapeados") or []:
        criterios.append(_criterio_lacuna(
            "pertinencia/arquivo-sem-mapa/%s" % caminho, "transversal",
            "arquivo alterado sem mapa de pertinencia (%s): nenhum cenario foi escolhido para ele; "
            "declarar no pertinencia.json ou justificar" % caminho,
            "arquivo mapeado a um mod/cenario", caminho))

    if not mods_selecionados:
        criterios.append(_criterio_lacuna(
            "pertinencia/sem-alteracao", "transversal",
            "nenhum mod alterado/declarado nesta rodada: nada a validar",
            "mod alterado", "nenhum"))

    for mod in sorted(mods_selecionados):
        tem_obs = any(_texto(o.get("mod")) == mod for o in dentro)
        if not tem_obs:
            criterios.append(_criterio_lacuna(
                "coleta/%s" % mod, mod,
                "nenhuma observacao coletada para %s (cenarios pertinentes: %s): lacuna TECNICA "
                "de coleta - volta ao agente, nao ao dono"
                % (mod, ", ".join(selecao["mods"][mod].get("cenarios") or []) or "nenhum"),
                "observacao do cenario pertinente", "nenhuma",
                extra={"cenarios": selecao["mods"][mod].get("cenarios") or [],
                       "frentes": selecao["mods"][mod].get("frentes") or []}))

    # (2c) PROCEDENCIA CONFRONTADA. A coleta DECLARA os mesmos bytes da rodada? O `hash_fonte` da
    # coleta e o sha256 da DLL do INSTRUMENTO (probe) - confrontado contra a cadeia da DLL, nunca
    # contra `fonte_sha` (F5 da revisao run670). Divergencia NAO e sobrescrita em silencio: vira
    # LACUNA declarada e derruba o OK (fail-closed).
    achados_coleta, confronto = confronto_da_coleta(coleta_meta, ident)
    for achado in achados_coleta:
        via = achado.get("via") or ""
        if achado["tipo"] == "ausente":
            motivo = ("coleta NAO declara hash_fonte: sem procedencia de bytes nao ha como ligar a "
                      "observacao a identidade da rodada (%s); nada desta coleta aprova"
                      % str(achado["identidade"])[:16])
        elif achado["tipo"] == "incoerente":
            motivo = ("coleta declara %s=%s e o mesmo campo vale %s para a rodada/instrumento (%s): "
                      "declaracao INCOERENTE - nada desta coleta aprova"
                      % (achado["campo"], str(achado["declarado"])[:16],
                         str(achado["identidade"])[:16], via))
        else:
            motivo = ("coleta declara %s=%s mas a identidade da rodada aponta %s (%s): a coleta "
                      "refere OUTROS bytes (procedencia CONTRADITORIA); nada desta coleta aprova"
                      % (achado["campo"], str(achado["declarado"])[:16],
                         str(achado["identidade"])[:16], via))
        criterios.append(_criterio_lacuna(
            "cadeia/coleta-%s/%s" % (achado["tipo"], achado["campo"]), "transversal", motivo,
            str(achado["identidade"]), str(achado["declarado"] or "<ausente>"),
            evidencia=[coleta_meta.get("caminho")] if coleta_meta.get("caminho") else []))
        rebaixar_ok(criterios, motivo)

    # (2d) F1R - config EXPLICITAMENTE solicitada e NAO medida: lacuna tecnica NOMEADA (volta ao
    # agente), nao aprovacao silenciosa. Config nao fornecida/opcional nao vira dependencia nova:
    # so o que a rodada pediu (`configs`) e nao mediu dispara isto.
    faltantes = sorted(ident.get("configs_ausentes") or [])
    for rel in faltantes:
        motivo = ("config explicitamente solicitada e NAO medida (%s): arquivo de entrada "
                  "requerido da rodada ausente/ilegivel; nada aprova ate a config ser medida ou a "
                  "solicitacao ser removida" % rel)
        criterios.append(_criterio_lacuna(
            "cadeia/config-ausente/%s" % rel, "transversal", motivo,
            "config da rodada medida", "ausente", extra={"config": rel}))
    if faltantes:
        rebaixar_ok(criterios, "config requerida ausente: %s" % ", ".join(faltantes))

    # (2e) F3R - instrumento de coleta EXPLICITAMENTE solicitado (`--probe-dll`) e NAO medido
    # (bytes ausentes/ilegiveis): SEM fallback silencioso para o alias `dll_sha`. Lacuna tecnica
    # de INSTRUMENTO. Instrumento apenas DECLARADO (sem --probe-dll) segue o limite declarado.
    if _texto(ident.get("dll_probe_sha_origem")) == "probe-ilegivel":
        motivo = ("instrumento de coleta explicitamente solicitado (--probe-dll) e NAO medido: "
                  "bytes ausentes/ilegiveis em %s; a procedencia NAO cai para o alias dll_sha - "
                  "lacuna tecnica de INSTRUMENTO"
                  % (ident.get("dll_probe_sha_arquivo") or "<sem caminho>"))
        criterios.append(_criterio_lacuna(
            "cadeia/instrumento-probe-ilegivel", "transversal", motivo,
            "bytes do instrumento medidos", "ilegivel"))
        rebaixar_ok(criterios, motivo)

    achados_criterio = confrontar_cadeia_declarada(criterios, ident)
    for achado in achados_criterio:
        motivo = ("criterio declara %s de OUTROS bytes (declarado=%s, identidade da rodada=%s): "
                  "declaracao CONTRADITORIA - rebaixado em vez de sobrescrito em silencio"
                  % (achado["campo"], str(achado["declarado"])[:16], str(achado["identidade"])[:16]))
        criterios.append(_criterio_lacuna(
            "cadeia/declaracao-contraditoria/%s/%s" % (achado["criterio"], achado["campo"]),
            "transversal", motivo, str(achado["identidade"]), str(achado["declarado"])))
        for candidato in criterios:
            if candidato.get("id") == achado["criterio"]:
                rebaixar_criterio(candidato, motivo)

    origem = {"caminho": coleta_meta.get("caminho"), "sessao": coleta_meta.get("sessao"),
              "fixture": bool(coleta_meta.get("fixture")), "hash_fonte": coleta_meta.get("hash_fonte"),
              "hash_fonte_confronto": confronto.get("hash_fonte"),
              "hash_fonte_campo_identidade": confronto.get("campo_identidade"),
              "instrumento_sha": confronto.get("instrumento_sha"),
              "instrumento_origem": confronto.get("instrumento_origem"),
              "instrumento_arquivo": confronto.get("instrumento_arquivo"),
              "campos_declarados_pela_coleta": coleta_meta.get("declarados") or {},
              "confrontos_declarados": confronto.get("confrontos") or []}
    for c in criterios:
        anexar_cadeia(c, ident, origem)
        if c.get("estado") != OK:
            anexar_causa(c, selecao, repo)

    if not identidade_suficiente(ident):
        rebaixar_ok(criterios, "sem identidade de fonte/DLL suficiente: nada vira OK")
    if coleta_meta.get("erro"):
        rebaixar_ok(criterios, "coleta invalida: %s" % coleta_meta["erro"])
    if coleta_meta.get("fixture"):
        rebaixar_ok(criterios, "coleta MARCADA como fixture: testa o avaliador, nao comprova runtime")
    meta = {"fora_da_pertinencia": fora_da_pertinencia,
            "declaracoes_incoerentes": originais_incoerentes,
            "observacoes_fora": len(fora)}
    return criterios, meta


# ==========================================================================
# 5. fila declarativa (reuso CIC-1 + sanitizacao de campo executavel)
# ==========================================================================

def montar_fila(criterios, dec, ident):
    """Fila de correcao DECLARATIVA: reusa o CIC-1 e acrescenta a cadeia + sanitizacao.

    Nada aqui e executado. Campo executavel que o CETICO/agente tenha proposto (no criterio
    ou no proprio item) sai do lugar executavel e vira `propostas_nao_executadas`.
    """
    c = ciclo()
    if not _disponivel(c):
        base = []
    else:
        base = c.montar_fila(criterios, ident)
        base += c.fila_da_decisao(dec, base, ident)
    por_criterio = {c.get("id"): c for c in criterios if isinstance(c, dict)}
    ids_com_item = {item.get("criterio") for item in base}
    fila = []
    for item in base:
        item = dict(item)
        crit = por_criterio.get(item.get("criterio")) or {}
        # Sementes ja registradas no criterio (idempotente: reconstruir a fila nao perde proposta).
        propostas = [dict(p) for p in (crit.get("propostas_nao_executadas") or [])]
        for origem, fonte in (("fila", item), ("criterio", crit)):
            for campo in sorted(list(fonte)):
                if campo not in CAMPOS_EXECUTAVEIS:
                    continue
                if origem == "criterio":
                    # Sanitiza o CRITERIO tambem: sem isso o campo executavel continuaria viajando
                    # em `resultado["criterios"]` para decisao/relatorio, mesmo fora da fila.
                    valor = fonte.pop(campo)
                    crit["criterio_sanitizado"] = True
                else:
                    valor = item.pop(campo) if campo in item else fonte.get(campo)
                propostas.append({"campo": campo, "valor": valor, "origem": origem})
        if propostas:
            item["propostas_nao_executadas"] = propostas
            item["motivo_recusa"] = ("campo executavel proposto por agente/LLM: registrado como "
                                     "DECLARACAO; o ciclo nao executa comando de correcao")
            if crit:
                # O criterio guarda a MESMA proposta: sanear o criterio e reconstruir a fila nao
                # faz a auditoria desaparecer; o resultado agrega de forma deduplicada.
                crit["propostas_nao_executadas"] = propostas
        item["execucao_automatica"] = False
        item["cadeia_sha"] = ident.get("cadeia_sha")
        item["prova"] = list(item.get("evidencia") or [])
        item.setdefault("quem_executa", "agente")
        fila.append(item)

    # (F5R) SANEAMENTO GLOBAL: o criterio que NAO gera item de fila (ex.: OK valido) tambem nao
    # pode transportar campo executavel para decisao/relatorio. Sanear TODOS os criterios,
    # independente do estado/entrada na fila, sem apagar auditoria (a proposta fica registrada
    # em local explicito e NAO executavel, mesmo sem item).
    for crit in criterios:
        if not isinstance(crit, dict) or crit.get("id") in ids_com_item:
            continue
        propostas = []
        for campo in sorted(list(crit)):
            if campo not in CAMPOS_EXECUTAVEIS:
                continue
            valor = crit.pop(campo)
            propostas.append({"campo": campo, "valor": valor, "origem": "criterio"})
        if propostas:
            crit["criterio_sanitizado"] = True
            crit["propostas_nao_executadas"] = propostas
    return fila


def propostas_do_resultado(criterios, fila):
    """Toda proposta de campo executavel movida para DECLARACAO, com a origem preservada.

    Cobre o criterio que gerou item de fila E o que NAO gerou (ex.: OK): em qualquer estado o
    conteudo proposto sai do lugar executavel e continua AUDITAVEL aqui. Deduplica por
    (criterio, campo, origem) - o mesmo achado nao entra duas vezes.
    """
    out, vistos = [], set()
    for crit in criterios:
        if not isinstance(crit, dict):
            continue
        for p in crit.get("propostas_nao_executadas") or []:
            chave = (crit.get("id"), p.get("campo"), p.get("origem"))
            if chave in vistos:
                continue
            vistos.add(chave)
            out.append(dict(p, criterio=crit.get("id")))
    for item in fila:
        for p in item.get("propostas_nao_executadas") or []:
            chave = (item.get("criterio"), p.get("campo"), p.get("origem"))
            if chave in vistos:
                continue
            vistos.add(chave)
            out.append(dict(p, criterio=item.get("criterio")))
    return out


# ==========================================================================
# 6. invalidacao da aprovacao anterior
# ==========================================================================

def invalidar_anterior(prev, ident):
    """Mudanca de fonte/DLL/config/versao INVALIDA a aprovacao anterior (nunca reassina log)."""
    if not isinstance(prev, dict) or prev.get("esquema") != ESQUEMA:
        return False, ""
    p = prev.get("identidade") or {}
    if not isinstance(p, dict):
        return False, ""
    rotulos = {"fonte_sha": "fonte", "dll_sha": "DLL", "config_sha": "config", "versao": "versao"}
    for campo in ("fonte_sha", "dll_sha", "config_sha", "versao"):
        antes, agora = p.get(campo), (ident or {}).get(campo)
        if (antes or None) != (agora or None):
            return True, ("%s mudou desde a rodada anterior (antes=%s agora=%s): aprovacao "
                          "anterior INVALIDADA" % (rotulos[campo], str(antes)[:12], str(agora)[:12]))
    return False, ""


# ==========================================================================
# 7. estado / exit
# ==========================================================================

def classificar_estado(criterios, dec, escala, invalidado):
    """(estado, exit). REPROVADO (defeito) e INCOMPLETO (lacuna tecnica) sao DISTINTOS."""
    falhas = list(dec.get("falhas_automaticas") or [])
    tem_reprov = any(c.get("estado") == REPROVADO for c in criterios) or \
        any(str(f.get("severidade")) == REPROVADO for f in falhas)
    tem_lacuna = any(c.get("estado") in (NAO_EXERCITADO, INDETERMINADO) for c in criterios)
    if invalidado:
        return ESTADO_INVALIDADO, EXIT_INVALIDADO
    if not criterios:
        # Avaliacao VAZIA nao e aprovacao: sem nenhum criterio nao ha o que aprovar.
        return ESTADO_INCOMPLETO, EXIT_INCOMPLETO
    if escala:
        return ESTADO_ESCALADO, EXIT_FALHOU
    if tem_reprov:
        return ESTADO_REPROVADO, EXIT_FALHOU
    if tem_lacuna or falhas:
        return ESTADO_INCOMPLETO, EXIT_INCOMPLETO
    return ESTADO_OK, EXIT_OK


# ==========================================================================
# 8. a rodada (costura completa)
# ==========================================================================

def cadeia(repo, *, alterados=None, base=None, mods=None, caminho_pertinencia=None,
           observacoes_path=None, configs=(), resultado_path=None, limite=0,
           identidade_extra=None, probe_dll=None):
    """Executa a costura e devolve o resultado estruturado (tambem gravado em `resultado_path`)."""
    repo = os.path.abspath(repo)
    pertinencia = carregar_pertinencia(caminho_pertinencia)
    alterados_efetivos = mods_alterados(repo, base=base, lista=alterados)
    selecao = mapear(alterados_efetivos, pertinencia, mods_explicitos=mods)

    observacoes, coleta_meta = carregar_coleta(observacoes_path)
    ident = identidade_cadeia(repo, configs=configs,
                              sessao=coleta_meta.get("sessao"),
                              mods=sorted(selecao.get("mods") or {}),
                              coleta_meta=coleta_meta, probe_dll=probe_dll)
    if identidade_extra:
        ident.update(identidade_extra)
        ident["cadeia_sha"] = sha256_mapa({k: ident.get(k) for k in CAMPOS_CADEIA})

    criterios, avalia_meta = criterios_da_cadeia(repo, selecao, observacoes, ident, coleta_meta,
                                                 pertinencia)

    dec_mod, dec_erro = decisao(), None
    ident_decisao = dict(ident)
    ident_decisao["raiz"] = repo
    if _disponivel(dec_mod):
        try:
            dec = dec_mod.consolidar(criterios, ident_decisao)
        except Exception as ex:  # noqa: BLE001
            dec_erro = "decisao.consolidar falhou: %s: %s" % (type(ex).__name__, ex)
            dec = {}
    else:
        dec_erro = "decisao.py (CIC-2) indisponivel: sem classificacao, nada e aprovado"
        dec = {}
    if dec_erro:
        criterios.append(_criterio_lacuna(
            "decisao/indisponivel", "transversal", dec_erro, "decisao.py consolida", "falhou"))
        dec.setdefault("falhas_automaticas", []).append(
            {"id": "decisao/indisponivel", "mod": "transversal", "severidade": NAO_EXERCITADO,
             "motivo_decisao": dec_erro, "evidencia": [], "tarefa_origem": TAREFA})
        dec.setdefault("pendencias_humanas", [])
        dec.setdefault("por_mod", {})
        dec.setdefault("resumo", {})

    fila = montar_fila(criterios, dec, ident)

    prev = None
    if resultado_path and os.path.isfile(resultado_path):
        try:
            cand = _ler_json(resultado_path)
            if isinstance(cand, dict) and cand.get("esquema") == ESQUEMA:
                prev = cand
        except (ValueError, OSError):
            prev = None
    invalidado_por_anterior, motivo_invalidacao = invalidar_anterior(prev, ident)

    c = ciclo()
    if _disponivel(c):
        tent = c.avaliar_tentativas(prev, ident, fila)
        limite_efetivo = limite or LIMITE_PADRAO
        tem_falha = bool(criterios_reprovados(criterios)) or bool(dec.get("falhas_automaticas"))
        escala, motivo_escalacao, destino = c.avaliar_escalonamento(tem_falha, tent, limite_efetivo)
    else:
        tent = {"numero": 1, "limite": limite or LIMITE_PADRAO, "sem_progresso": False,
                "sem_progresso_seguidas": 0, "invalidou_anterior": False, "motivo_sem_progresso": ""}
        limite_efetivo, escala, motivo_escalacao, destino = (limite or LIMITE_PADRAO), False, "", "ciclo"
    tent["limite"] = limite_efetivo

    rel_texto, rel_estrutura = _relatorio(dec, criterios)

    # (F2R) relatorio obrigatorio INDISPONIVEL (modulo ausente ou excecao de montagem) NAO pode
    # aprovar: vira lacuna tecnica NOMEADA que volta ao agente (nunca texto inventado) e a fila e
    # recalculada para transportar a pendencia. A classificacao do estado acontece DEPOIS disso,
    # por isso o relatorio passa a ser montado ANTES de classificar.
    if not rel_estrutura.get("disponivel"):
        motivo_rel = ("relatorio obrigatorio INDISPONIVEL (%s): nada e aprovado sem o relatorio; "
                      "lacuna tecnica volta ao agente"
                      % (rel_estrutura.get("motivo") or "motivo nao declarado"))
        lac_rel = _criterio_lacuna("relatorio/indisponivel", "transversal", motivo_rel,
                                   "relatorio da entrega disponivel", "indisponivel")
        anexar_cadeia(lac_rel, ident, None)
        criterios.append(lac_rel)
        fila = montar_fila(criterios, dec, ident)

    estado, codigo = classificar_estado(criterios, dec, escala, invalidado_por_anterior)

    resultado = {
        "esquema": ESQUEMA, "tarefa": TAREFA, "gerado_em": agora(), "repo": repo,
        "alterados": alterados_efetivos,
        "pertinencia": selecao,
        "identidade": ident,
        "cadeia_sha": ident.get("cadeia_sha"),
        "coleta": coleta_meta,
        "criterios": criterios,
        "criterios_resumo": _resumo_criterios(criterios),
        "fora_da_pertinencia": avalia_meta.get("fora_da_pertinencia") or [],
        "declaracoes_incoerentes": avalia_meta.get("declaracoes_incoerentes") or [],
        "decisao": dec,
        "falhas_automaticas": dec.get("falhas_automaticas") or [],
        "pendencias_humanas": dec.get("pendencias_humanas") or [],
        "fila_correcao": fila,
        "propostas_nao_executadas": propostas_do_resultado(criterios, fila),
        "tentativas": {"numero": tent.get("numero"), "limite": tent.get("limite"),
                       "sem_progresso": tent.get("sem_progresso"),
                       "sem_progresso_seguidas": tent.get("sem_progresso_seguidas"),
                       "sem_progresso_motivo": tent.get("motivo_sem_progresso"),
                       "invalidou_anterior": invalidado_por_anterior,
                       "motivo_invalidacao": motivo_invalidacao},
        "escala": escala, "motivo_escalacao": motivo_escalacao, "destino_escalonamento": destino,
        "relatorio": rel_estrutura, "relatorio_texto": rel_texto,
        "estado": estado, "exit_code": codigo,
        "limites": [
            "nao instala, nao abre/fecha jogo, nao carrega save, nao commita, nao publica",
            "fixture testa o AVALIADOR; fixture nao comprova runtime",
            "a fila e DECLARATIVA: nao ha caminho de execucao de comando neste modulo",
            "aprovacao tecnica NAO e aceite humano nem DoD",
            "procedencia da coleta confrontada contra a cadeia da DLL/INSTRUMENTO (dll_probe_sha) e "
            "o alias documentado dll_sha; `fonte_sha` NAO e procedencia de coleta",
            "instrumento apenas DECLARADO pela coleta (sem bytes em disco) e confrontado como "
            "declaracao registrada em `coleta.instrumento_origem`; medicao independente dos bytes "
            "exige `--probe-dll` ou `identidade.arquivo_dll_do_probe` presente",
        ],
    }
    if resultado_path:
        _escrever_json(os.path.abspath(resultado_path), resultado)
    return resultado


def criterios_reprovados(criterios):
    return [c for c in criterios if c.get("estado") == REPROVADO]


def _resumo_criterios(criterios):
    cont = {OK: 0, REPROVADO: 0, NAO_EXERCITADO: 0, INDETERMINADO: 0}
    for c in criterios:
        cont[c.get("estado")] = cont.get(c.get("estado"), 0) + 1
    return {"total": len(criterios), **cont,
            "com_prova_runtime": sum(1 for c in criterios if c.get("prova_runtime") is True)}


def _relatorio(dec, criterios):
    a = aceite()
    if not _disponivel(a) or not dec:
        return "", {"disponivel": False,
                    "motivo": "relatorio_aceite.py (AUT-7) indisponivel ou decisao ausente"}
    try:
        rev = a._revisoes(None) if hasattr(a, "_revisoes") else {
            "revisoes": {"AUT-3R": "PENDENTE", "AUT-5R": "PENDENTE", "AUT-6R": "PENDENTE"},
            "consolidacao_final": False,
            "motivo": "consolidacao final depende de revisao independente"}
        rel = a.montar_relatorio(dec, criterios, {})
        texto = a.texto_do_relatorio(rel, rev)
        return texto, {"disponivel": True, "por_mod": rel.get("por_mod"),
                       "tecnico": rel.get("tecnico"), "revisoes": rev}
    except Exception as ex:  # noqa: BLE001
        return "", {"disponivel": False,
                    "motivo": "relatorio_aceite falhou: %s: %s" % (type(ex).__name__, ex)}


# ==========================================================================
# 9. verificacao de resultado guardado
# ==========================================================================

def verificar(repo, resultado_path, *, configs=(), versao=None, probe_dll=None):
    """Um resultado guardado ainda vale para os bytes/DLL/config/versao atuais?"""
    repo = os.path.abspath(repo)
    if not resultado_path or not os.path.isfile(resultado_path):
        return {"esquema": ESQUEMA, "modo": "verificar", "valido": False,
                "motivo": "resultado ausente: %s" % resultado_path,
                "exit_code": EXIT_INVALIDADO}
    try:
        prev = _ler_json(resultado_path)
    except (ValueError, OSError) as ex:
        return {"esquema": ESQUEMA, "modo": "verificar", "valido": False,
                "motivo": "resultado ilegivel: %s" % ex, "exit_code": EXIT_INVALIDADO}
    if not isinstance(prev, dict) or prev.get("esquema") != ESQUEMA:
        return {"esquema": ESQUEMA, "modo": "verificar", "valido": False,
                "motivo": "resultado nao e deste esquema (%s)" % ESQUEMA,
                "exit_code": EXIT_INVALIDADO}
    # A versao da RODADA GUARDADA e reconferida contra os bytes de agora (csproj do mod),
    # nao herdada do proprio resultado - senao uma troca de versao passaria despercebida.
    mods_guardados = sorted((prev.get("pertinencia") or {}).get("mods") or {})
    versao_efetiva = versao
    if versao_efetiva is None and mods_guardados:
        versoes = [versao_do_csproj(repo, m) for m in mods_guardados]
        versoes = [v for v in versoes if v]
        versao_efetiva = "+".join(versoes) if versoes else None
    ident = identidade_cadeia(repo, configs=configs, versao=versao_efetiva,
                              sessao=(prev.get("identidade") or {}).get("sessao"),
                              coleta_meta=prev.get("coleta"), probe_dll=probe_dll)
    invalidado, motivo = invalidar_anterior(prev, ident)
    return {"esquema": ESQUEMA, "modo": "verificar", "repo": repo,
            "resultado": os.path.abspath(resultado_path),
            "cadeia_sha_resultado": prev.get("cadeia_sha"),
            "cadeia_sha_atual": ident.get("cadeia_sha"),
            "valido": not invalidado, "motivo": motivo or "resultado corresponde aos bytes atuais",
            "exit_code": EXIT_INVALIDADO if invalidado else EXIT_OK}


# ==========================================================================
# 10. CLI
# ==========================================================================

def _imprimir(r):
    if r.get("modo") == "verificar":
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    dec = r.get("decisao") or {}
    resumo = {
        "esquema": r["esquema"], "estado": r["estado"], "exit_code": r["exit_code"],
        "cadeia_sha": str(r.get("cadeia_sha"))[:12],
        "fonte_sha": str((r.get("identidade") or {}).get("fonte_sha"))[:12],
        "dll_sha": str((r.get("identidade") or {}).get("dll_sha"))[:12],
        "config_sha": str((r.get("identidade") or {}).get("config_sha"))[:12],
        "dll_probe_sha": str((r.get("identidade") or {}).get("dll_probe_sha"))[:12],
        "dll_probe_sha_origem": (r.get("identidade") or {}).get("dll_probe_sha_origem"),
        "versao": (r.get("identidade") or {}).get("versao"),
        "sessao": (r.get("identidade") or {}).get("sessao"),
        "mods": sorted((r.get("pertinencia") or {}).get("mods") or {}),
        "nao_mapeados": (r.get("pertinencia") or {}).get("nao_mapeados") or [],
        "coleta": {"caminho": (r.get("coleta") or {}).get("caminho"),
                   "fixture": (r.get("coleta") or {}).get("fixture"),
                   "quantidade": (r.get("coleta") or {}).get("quantidade"),
                   "hash_fonte": (r.get("coleta") or {}).get("hash_fonte"),
                   "instrumento_origem": (r.get("identidade") or {}).get("dll_probe_sha_origem"),
                   "erro": (r.get("coleta") or {}).get("erro")},
        "criterios": r.get("criterios_resumo"),
        "fora_da_pertinencia": len(r.get("fora_da_pertinencia") or []),
        "declaracoes_incoerentes": len(r.get("declaracoes_incoerentes") or []),
        "falhas_automaticas": len(r.get("falhas_automaticas") or []),
        "pendencias_humanas": len(r.get("pendencias_humanas") or []),
        "fila": len(r.get("fila_correcao") or []),
        "propostas_nao_executadas": len(r.get("propostas_nao_executadas") or []),
        "tentativa": r["tentativas"]["numero"], "limite": r["tentativas"]["limite"],
        "sem_progresso": r["tentativas"]["sem_progresso"],
        "invalidou_anterior": r["tentativas"]["invalidou_anterior"],
        "motivo_invalidacao": r["tentativas"]["motivo_invalidacao"],
        "escala": r["escala"], "motivo_escalacao": r["motivo_escalacao"],
        "pronto_para_decisao": dec.get("pronto_para_decisao"),
        "motivo_pronto": dec.get("motivo_pronto_para_decisao"),
    }
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="KIT-12 - costura alteracao -> cenarios pertinentes -> coleta -> avaliadores -> relatorio.")
    ap.add_argument("--repo", default=RAIZ_PADRAO, help="repositorio dos bytes atuais")
    ap.add_argument("--alterados", action="append", default=None,
                    help="arquivo alterado (repetivel); sem isso usa o git status do repo")
    ap.add_argument("--base", default=None, help="ref do git para diff (opcional)")
    ap.add_argument("--mod", action="append", default=None,
                    help="mod declarado explicitamente (repetivel); atalho quando o git nao esta disponivel")
    ap.add_argument("--pertinencia", default=None, help="mapa declarativo (padrao: kit12/pertinencia.json)")
    ap.add_argument("--observacoes", default=None, help="coleta (envelope do probe ou lista de observacoes)")
    ap.add_argument("--probe-dll", default=None,
                    help="caminho da DLL do INSTRUMENTO de coleta (probe): a procedencia da coleta "
                         "e confrontada contra o sha256 MEDIDO desses bytes")
    ap.add_argument("--config", action="append", default=None,
                    help="arquivo de config relevante (repetivel) - entra no config_sha da cadeia")
    ap.add_argument("--versao", default=None, help="versao da rodada (padrao: le o csproj do mod alterado)")
    ap.add_argument("--resultado", default=None, help="onde gravar/ler o resultado (JSON)")
    ap.add_argument("--limite", type=int, default=0, help="limite de tentativas (padrao %d)" % LIMITE_PADRAO)
    ap.add_argument("--verificar", default=None,
                    help="verifica se um resultado guardado ainda corresponde aos bytes atuais")
    args = ap.parse_args(argv)

    if args.verificar:
        saida = verificar(args.repo, args.verificar, configs=args.config or [], versao=args.versao,
                          probe_dll=args.probe_dll)
        _imprimir(saida)
        return saida["exit_code"]

    if args.limite < 0:
        ap.error("--limite deve ser positivo")

    r = cadeia(args.repo, alterados=args.alterados, base=args.base, mods=args.mod,
               caminho_pertinencia=args.pertinencia, observacoes_path=args.observacoes,
               configs=args.config or [], resultado_path=args.resultado, limite=args.limite,
               probe_dll=args.probe_dll,
               identidade_extra=({"versao": args.versao} if args.versao else None))
    _imprimir(r)
    return r["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
