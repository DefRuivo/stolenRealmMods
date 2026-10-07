#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cobertura.py - AUT-6: cobertura automatizada de TOOLTIPS/SHRINES por personagem.

TAREFA: `t_775eb4ae` (AUT-6) — cobrir RV-26/27/28/29/31/33/34 reusando `checa_shrines`, as
tabelas GERADAS e as fixtures; regressao do Armor ja aceito pelo dono (BUG-34), sem reabrir o bug.

O QUE ESTE MODULO E (E O QUE ELE NAO E)
---------------------------------------
E o AVALIADOR de um conjunto de OBSERVACOES (`avaliar(observacoes, identidade) -> criterios`),
no contrato v1 do ciclo (`docs/automacao/CICLO-VALIDACAO-escopo.md` §Contrato de integracao).
NAO e um coletor: ele nao abre jogo, nao instala probe e nao inventa emissao. O que o mod NAO
loga (ex.: corpo renderizado da tooltip, cor da linha azul) so entra por uma observacao do
coletor runtime (AUT-4) ou fica `NAO_EXERCITADO` - nunca vira OK.

POR QUE ELE EXISTE SEPARADO DO `tools/automacao/cenarios/tooltips_shrines.py` (CIC-4)
-----------------------------------------------------------------------------------
O CIC-4 cobre 4 casos no mesmo contrato. Este modulo cobre o DELTA pedido pela AUT-6 (globule,
entrar/sair de aura, dedupe/stacking, bonus Omnism/Horn+teto/piso, corpo/nota, a divergencia do
RV-49 e a metade "corpo da tooltip COM a nota" da regressao do Armor) e o faz sobre a
INFRAESTRUTURA ESTAVEL: `tools/checa_shrines.py` (conferidor, importado de verdade),
`tools/dados/*.csv` (tabelas GERADAS), `docs/cobertura/acoes.csv` (a formula do motor),
`resources.assets` (offsets DOCUMENTADOS) e as fixtures versionadas. Ele NAO importa o modulo do
CIC-4 porque aquele arquivo e area exclusiva de outro agente e estava sendo ESCRITO durante esta
rodada (hotspot declarado no relatorio) - os dois emitem o MESMO contrato e o pai integra.

REGRA DE OURO (a mesma do conferidor, e a oposta do `check_patches` que deixou passar falso OK):
**AUSENCIA NAO E APROVACAO.** Sem observacao, sem campo ou sem linha no log => `NAO_EXERCITADO`
com o motivo nomeando o passo TECNICO que falta; `INDETERMINADO` quando o dado existe mas e de
OUTRA build (hash divergente). Fixture NUNCA prova runtime (`prova_runtime=False`).

FONTES DO ESPERADO (nenhuma "de cabeca"; cada criterio cita a fonte)
-------------------------------------------------------------------
* contribuicao das auras de buff / itens sem atributo (RV-26/28/31/44/46):
  `tools/dados/shrines-esperado.csv`, GERADO por `tools/gera_shrines_esperado.py` a partir do
  censo (`docs/cobertura/status.csv`) e de `resources.assets`; cada linha cita `fonte_base`.
* dano das auras de PERIGO (Decay/Flame, RV-33/34): `tools/dados/shrines-percentuais.csv`
  (% por TIPO de inimigo, com o offset do asset) + a formula `max(1, round(...))` do eixo
  `Source` (RV-30) - o MESMO caminho que o `checa_shrines.py` usa.
* globule (RV-28/32): `docs/cobertura/acoes.csv` - a acao real do motor
  (`Sustenance I Proc` -> `Target.MaxHealth * .08f`; `Sustenance II Proc` -> `.20f`).
* TETO/PISO do atributo (RV-46/RV-50c): `resources.assets` nos offsets DOCUMENTADOS
  (`DamageReduction` `MaxValue=50` @1519603860; `ManaCostMod` `MinValue=-75` @1519616544 -
  `tools/fixtures/shrines-piso-cru.log`, `tools/testes/testes/puros/t_shrine_piso_cru.py`).
  Sem o asset o criterio e `NAO_EXERCITADO` (nunca chute).
* corpo/nota (RV-26/27) e Armor (BUG-34): o CONTRATO do fonte
  (`BetterTooltips/Patches/LocalizePatch.cs` - `BuildArmorNote`, `TextFixes`) e a fixture
  rotulada do feed/texto flutuante.

USO
---
    python tools/automacao/aut6/cobertura.py --observacoes X.json [--identidade '{"fonte_sha":"...","dll_sha":"..."}']
    python tools/automacao/aut6/cobertura.py --casos tools/automacao/aut6/casos-aut6.json --observacoes X.json
    python tools/automacao/aut6/cobertura.py --offline        # cobertura dos casos + fontes do esperado

Exit codes: 0 = todos os criterios com prova; 1 = pelo menos um REPROVADO; 2 = INCOMPLETO
(NAO_EXERCITADO/INDETERMINADO ou nenhum criterio com prova de runtime) - **ausencia nunca e OK**.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import struct
import sys
try:
    from . import prova, validacoes
except ImportError:  # CLI direto
    import prova
    import validacoes

normalizar_aut4 = prova.normalizar_aut4

AQUI = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(AQUI))
REPO = os.path.dirname(TOOLS)

if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
import checa_shrines as checa  # noqa: E402  (infra pronta - NAO reimplementar o parser)

ESPERADO = os.path.join(TOOLS, "dados", "shrines-esperado.csv")
PERCENTUAIS = os.path.join(TOOLS, "dados", "shrines-percentuais.csv")
ACOES = os.path.join(REPO, "docs", "cobertura", "acoes.csv")
CASOS_PADRAO = os.path.join(AQUI, "casos-aut6.json")

TAREFA_PADRAO = "t_775eb4ae"
MOD_PADRAO = "BetterTooltips"
ESQUEMA = "AUT-6/aut6/1"

EXIT_OK, EXIT_REPROVADO, EXIT_INCOMPLETO = 0, 1, 2

# Identidade minima (mesmo contrato v1/CIC-2): sem ela uma observacao de runtime NUNCA aprova.
IDENTIDADE_CAMPOS = ("fonte_sha", "dll_sha", "config_sha", "sessao")
PROCEDENCIAS = ("execucao", "runtime", "fixture")

MARCA_LINHA = "Your active shrine auras:"       # ancora da linha azul (RV-31/44)
NOTA_ARMOR = "blocks damage"                     # fragmento estavel do `BuildArmorNote` (BUG-34)
NOTA_SHRINE = "Shrine Effect Bonus"              # a nota da familia de shrine fala do bonus
# RV-30 (03/10): as duas auras de PERIGO leem `Source["ShrineEffectBonus"]` e num ground effect o
# `Source` e o personagem VAZIO do shrine -> bonus 0. Mesma constante do oraculo
# (`tools/testes/regras_shrine.py:BONUS_DA_FONTE`) e do conferidor (`checa_shrines.py`, §Limites 10).
BONUS_DA_FONTE = 0.0

# Rotulos que NUNCA sao valor medido (mesma regra do AUT-4).
AUSENTES = ("AUSENTE", "NAO EXERCITADO", "NÃO EXERCITADO", "NAO_EXERCITADO",
            "INDETERMINADO", "INDETERMINATE", "-", "")

# Limites do atributo (RV-46/RV-50c) - offset DOCUMENTADO no asset, nao adivinhado.
# (campo, offset, citacao) - o offset e o MESMO ponto que o mod le em runtime.
LIMITES_ASSET = {
    "DamageReduction": ("MaxValue", 1519603860,
                        "resources.assets@1519603860 (tools/fixtures/shrines-piso-cru.log; "
                        "tools/testes/testes/puros/t_shrine_piso_cru.py)"),
    "ManaCostMod": ("MinValue", 1519616544,
                    "resources.assets@1519616544 (tools/fixtures/shrines-piso-cru.log; "
                    "tools/testes/testes/puros/t_shrine_piso_cru.py)"),
}
ASSETS_CANDIDATOS = (
    r"E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/resources.assets",
    r"C:/Program Files (x86)/Steam/steamapps/common/Stolen Realm/Stolen Realm_Data/resources.assets",
    r"D:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/resources.assets",
)

# Marcador do globule (RV-28/32) - `Marca` do GlobulePatch: `[Globule RV-28] <linha>`.
RE_GLOBULE = re.compile(r"^\[[A-Za-z]+\s*:\s*Better Tooltips\]\s*\[Globule RV-28\]\s*(?P<p>.+)$")
RE_GLOBULE_NUM = re.compile(
    r"^'(?P<chave>.*?)': (?P<char>.+?) (?P<tiers>.+?) = (?P<pct>[0-9.]+)% -> (?P<frase>.*)$")
RE_GLOBULE_HEALTH = re.compile(r"(?P<h>[0-9.]+) health and (?P<m>[0-9.]+) mana with your current pools")
# A acao real do motor no censo (`docs/cobertura/acoes.csv`): `Target.MaxHealth * .08f`.
RE_ACAO_PCT = re.compile(r"Target\.MaxHealth \* (?P<f>\.?[0-9]+(?:\.[0-9]+)?)f")

# --------------------------------------------------------------- fontes (carregam o esperado)


def carrega_tabelas():
    """As tabelas GERADAS. Ausente = defeito do repositorio: FALHA dura, nunca chute."""
    tabela = checa.carrega_esperado(ESPERADO)
    pct = checa.carrega_percentuais(PERCENTUAIS)
    if not tabela or not pct:
        raise SystemExit(2)
    return tabela, pct


_TABELAS = None


def _sha256(caminho):
    """sha256 de um arquivo do repo (o `casos_sha256` da rodada) - None se ausente."""
    if not caminho or not os.path.isfile(caminho):
        return None
    with open(caminho, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _casos_caminho(casos):
    return casos if isinstance(casos, str) and casos else CASOS_PADRAO


def _tabelas():
    """As tabelas GERADAS, carregadas 1x e compartilhadas pelos casos."""
    global _TABELAS
    if _TABELAS is None:
        _TABELAS = carrega_tabelas()
    return _TABELAS


def acoes_sustenance(caminho=ACOES):
    """`{nome_da_acao: fracao}` das acoes do Sustenance, lido do censo de ACOES.

    Fonte independente (a acao do motor, nao o log do mod): `Sustenance I Proc` -> 0.08 e
    `Sustenance II Proc` -> 0.20. Ausente => `{}` (o caso vira NAO_EXERCITADO, nunca chute).
    """
    if not os.path.isfile(caminho):
        return {}
    saida = {}
    with open(caminho, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            nome = (r.get("nome") or "").strip()
            if nome not in ("Sustenance I Proc", "Sustenance II Proc"):
                continue
            m = RE_ACAO_PCT.search(r.get("efeitos") or "")
            if m:
                saida[nome] = float(m.group("f"))
    return saida


def _procura_asset(caminho=None):
    if caminho:
        return caminho if os.path.isfile(caminho) else None
    for c in ASSETS_CANDIDATOS:
        if os.path.isfile(c):
            return c
    return None


def limite_no_asset(atributo, asset=None):
    """(rotulo, valor, citacao) do TETO/PISO do atributo lido do asset, ou None.

    Le o MESMO ponto documentado (float no offset) que o mod le em runtime. Nunca adivinha:
    atributo sem offset documentado ou asset ausente => None.
    """
    info = LIMITES_ASSET.get(atributo)
    if not info:
        return None
    rotulo, offset, cit = info
    caminho = _procura_asset(asset)
    if not caminho:
        return None
    with open(caminho, "rb") as fh:
        fh.seek(offset)
        bruto = fh.read(4)
    if len(bruto) != 4:
        return None
    return (rotulo, float(struct.unpack("<f", bruto)[0]), cit)


# --------------------------------------------------------------- contrato (identidade/estado)


def identidade_de(ident):
    """Normaliza a identidade da rodada: (suficiente, faltando, kwargs)."""
    ident = ident or {}
    faltando = [c for c in IDENTIDADE_CAMPOS
                if not (isinstance(ident.get(c), str) and ident[c].strip())]
    return (not faltando), faltando, ident


def _rotulo(obs):
    """Procedencia DECLARADA da observacao. Ausente/desconhecida NUNCA vira runtime."""
    if prova.fixture(obs):
        return "fixture"
    p = obs.get("procedencia")
    if isinstance(p, str) and p.strip() in PROCEDENCIAS:
        return p.strip()
    if obs.get("rotulo_fixture") is True or obs.get("evidencia_runtime") is False:
        return "fixture"
    return "execucao"


def _evidencia_obs(obs):
    """Evidencia = artefato REALMENTE lido pela observacao (nunca a tabela do esperado).

    Fail-closed: caminho declarado que NAO existe no disco nao conta como evidencia - a cadeia de
    runtime exige um artefato de verdade (log/objeto da rodada), nao um carimbo.
    """
    if obs.get('_evidencias_verificadas'):
        return obs['_evidencias_verificadas']
    ev = []
    for x in (obs.get("evidencia") or []):
        if isinstance(x, dict):
            ev.append(dict(x))
            continue
        p = str(x)
        cand = p if os.path.isabs(p) else os.path.join(REPO, p)
        if os.path.isfile(cand):
            ev.append(p)
    obj = obs.get("objeto")
    if isinstance(obj, str) and obj.strip():
        cand = obj if os.path.isabs(obj) else os.path.join(REPO, obj)
        if os.path.isfile(cand):
            ev.append(obj)
    return ev


def _hashes_obs(obs):
    """Hashes declarados pela observacao, sob as chaves canonicas.

    `hash_fonte`/`hash_dll` do coletor = cadeia da DLL -> `dll_sha` (alias R-1 do CIC-5R).
    """
    d = {}
    for alias, canonico in (("hash_fonte", "dll_sha"), ("hash_dll", "dll_sha")):
        v = obs.get(alias)
        if isinstance(v, str) and v.strip():
            d[canonico] = v.strip()
    for chave in ("fonte_sha", "dll_sha", "config_sha"):
        v = obs.get(chave)
        if isinstance(v, str) and v.strip():
            d[chave] = v.strip()
    return d


def _cadeia(obs, ident_kw):
    """CADEIA de runtime confrontada com a identidade da rodada. (estado, motivo) ou (None, None)."""
    if not ident_kw["suficiente"]:
        return ("NAO_EXERCITADO",
                "identidade insuficiente (falta %s): observacao de runtime NAO aprova sem "
                "fonte_sha/dll_sha (automatizavel: anexar a identidade da rodada)"
                % ", ".join(ident_kw["faltando"]))
    if not str(obs.get("sessao") or "").strip():
        return ("NAO_EXERCITADO", "runtime sem sessao: cadeia de coleta incompleta")
    declarados = _hashes_obs(obs)
    if obs['sessao'] != ident_kw['kwargs']['sessao']:
        return ('INDETERMINADO', 'sessao obsoleta: observacao difere da identidade da rodada')
    aliases = [obs.get(k) for k in ('hash_fonte', 'hash_dll', 'dll_sha') if obs.get(k)]
    if len(set(aliases)) > 1:
        return ('INDETERMINADO', 'aliases de hash da DLL contraditorios')
    faltam = [k for k in ('fonte_sha', 'dll_sha', 'config_sha') if not declarados.get(k)]
    if faltam:
        return ('NAO_EXERCITADO', 'observacao sem campos tecnicos: ' + ', '.join(faltam))
    if not str(obs.get('objeto') or '').strip():
        return ('NAO_EXERCITADO', 'observacao sem o objeto medido (alvo do criterio)')
    if not (str(obs.get('cenario') or '').strip() or str(obs.get('superficie') or '').strip()):
        return ('NAO_EXERCITADO', 'observacao sem cenario/superficie: nao associa a medida ao caso')
    if not declarados:
        return ("NAO_EXERCITADO",
                "rotulo runtime SEM hash da build: o rotulo sozinho nao amarra aos bytes - a "
                "observacao so aprova com o hash (hash_fonte/DLL) confrontado com a identidade")
    conhecidos = {k: ident_kw["kwargs"][k] for k in ("fonte_sha", "dll_sha", "config_sha")
                  if isinstance(ident_kw["kwargs"].get(k), str) and ident_kw["kwargs"][k].strip()}
    divergentes = sorted(k for k, v in declarados.items() if k in conhecidos and conhecidos[k] != v)
    if divergentes:
        return ("INDETERMINADO",
                "observacao de OUTRA build (hash %s difere da identidade da rodada)"
                % ", ".join(divergentes))
    nao_confirmados = sorted(k for k in declarados if k not in conhecidos)
    if nao_confirmados:
        return ("NAO_EXERCITADO",
                "hash declarado que a identidade/manifest nao conhece (%s): cadeia incompleta"
                % ", ".join(nao_confirmados))
    estado, motivo, refs = prova.conferir(obs, ident_kw['kwargs'], REPO)
    if estado:
        return estado, motivo
    obs['_evidencias_verificadas'] = refs
    return (None, None)


def _decisao(obs, ident_kw):
    """(estado, prova_runtime, motivo) para um valor que BATEU. Nunca OK sem a cadeia."""
    _ULTIMA_CADEIA.clear()
    rotulo = _rotulo(obs)
    if obs.get('_conflito_normalizacao'):
        return ('INDETERMINADO', False, 'campos normalizados contradizem campos do topo')
    if str(obs.get('status', '')).upper() in ('ERRO', 'ERROR', 'INDETERMINADO') or obs.get('ok') is False:
        return ('INDETERMINADO', False, 'coleta declara erro/ok=false; nao comprova medida')
    if rotulo == "fixture":
        return ("OK", False,
                "fixture: avalia o avaliador; NAO prova runtime (a decisao separa fixture de "
                "prova - CICLO-VALIDACAO-escopo.md, contrato v1)")
    if rotulo != "runtime":
        return ("NAO_EXERCITADO", False,
                "observacao sem rotulo de runtime confiavel (procedencia=%r): rotulo "
                "ausente/desconhecido NUNCA vira runtime (prova exige cadeia, nao rotulo)"
                % rotulo)
    estado, motivo = _cadeia(obs, ident_kw)
    if estado:
        return (estado, False, motivo)
    # Contrato positivo de runtime: a CADEIA (sessao + hashes da identidade) vai no criterio para
    # o consumidor (decisao.py) reconferir contra a identidade/manifest - nao so um rotulo.
    if obs.get('ambiente_prova') == 'teste_contrato':
        return ('OK', False, 'TESTE DE CONTRATO em sandbox: bytes completos, nao prova produto/runtime')
    _ULTIMA_CADEIA.update(_cadeia_do_criterio(obs, ident_kw))
    return ("OK", True, "valor bateu com o esperado INDEPENDENTE e a cadeia de runtime fecha "
                        "(sessao/hash/manifest/evidencia confrontados com a identidade)")


# Estado de RODADA (o avaliador e single-thread, chamado uma vez por rodada): a identidade
# confrontada vai em todo criterio e a CADEIA da ultima decisao vai no criterio de runtime.
_RODADA = {}
_ULTIMA_CADEIA = {}


def _cadeia_do_criterio(obs, ident_kw):
    """Sessao da observacao + hashes da identidade confrontada (contrato positivo de runtime)."""
    d = {}
    for key in ('cenario', 'personagem', 'objeto', 'superficie', 'ambiente_prova', 'origem'):
        if key in obs:
            d[key] = obs[key]
    if obs.get("sessao"):
        d["sessao"] = obs["sessao"]
    for chave in ("fonte_sha", "dll_sha", "config_sha"):
        v = _hashes_obs(obs).get(chave)
        if isinstance(v, str) and v.strip():
            d[chave] = v.strip()
    return d


def _crit(caso, pid, estado, esperado, observado, motivo, obs_rotulo, prova_runtime,
          evidencia, extra=None):
    crit = {
        "id": "%s/%s" % (caso["id"], pid) if pid else caso["id"],
        "mod": caso.get("mod", MOD_PADRAO),
        "estado": estado,
        "classe": "runtime" if obs_rotulo == "runtime" else "offline",
        "procedencia": obs_rotulo,
        "prova_runtime": bool(prova_runtime),
        "esperado": esperado,
        "observado": observado,
        "evidencia": list(evidencia or []),
        "motivo": motivo,
        "tarefa_origem": caso.get("tarefa_origem", TAREFA_PADRAO),
        "tarefas_rv": list(caso.get("rv") or []),
        "cenario": caso['id'],
    }
    if estado in ("NAO_EXERCITADO", "INDETERMINADO"):
        crit["autorizacao_necessaria"] = False
        crit["tipo_pendencia"] = "coleta_tecnica"
    if _RODADA:
        crit["identidade_rodada"] = dict(_RODADA)
    if prova_runtime and _ULTIMA_CADEIA:
        crit.update(_ULTIMA_CADEIA)
        crit['config_relevante'] = True
    if extra:
        crit.update(extra)
    return crit


def _nao_ok(estado, motivo):
    return estado, motivo


# --------------------------------------------------------------- leitura das observacoes


def _texto_feed(obs):
    feed = obs.get("feed")
    if isinstance(feed, list):
        return "\n".join(str(x) for x in feed)
    if isinstance(feed, str):
        return feed
    return ""


def _adaptar(observacoes):
    saida = []
    for o in observacoes:
        if not isinstance(o, dict):
            continue
        raw = prova.achatar(o)
        c = dict(raw)
        c["_raw"] = raw
        c["rotulo"] = _rotulo(raw)
        c["feed_txt"] = _texto_feed(raw)
        c["coleta"] = checa.coleta(c["feed_txt"]) if c["feed_txt"] else None
        c["render"] = raw.get("texto_renderizado") or ""
        saida.append(c)
    return saida


def _as_obs(o):
    return {"rotulo": o["rotulo"], "_raw": o}


def _achar_acumulado(obs_list, aura, nome, bonus):
    """Acha a linha RV-31 acumulado de (aura, char, bonus) no feed de alguma observacao."""
    for o in obs_list:
        if not o["coleta"]:
            continue
        for a in o["coleta"]["acumulado"]:
            if (a["char"] == nome and abs(a["bonus"] - float(bonus)) < 1e-9
                    and aura in a["auras"]):
                return o, a
    return None, None


def _item_de(a, atributo):
    for it in a["itens"]:
        if it["atributo"] == atributo:
            return it
    return None


def _fonte_buff(aura, atributo, bonus):
    for r in _tabelas()[0]:
        if r["aura"] == aura and r["atributo"] == atributo and float(r["caso_bonus"]) == float(bonus):
            return float(r["contribuicao_esperada"]), r.get("fonte_base", ESPERADO)
    return None, None


def _esperado_perigo(aura, tipo, maxhealth):
    """Dano esperado (eixo `Source` = 0, RV-30) - a MESMA conta do `checa_shrines.py`."""
    pct = _tabelas()[1][aura]
    t = (tipo or "").lower()
    if t not in pct:
        return None, None
    fator = 1.0 + float(BONUS_DA_FONTE) / 100.0
    valor = float(checa.round_half_even(maxhealth * (pct[t] / 100.0) * fator))
    if aura == "Flame Shrine Aura":
        valor = max(1.0, valor)
    return valor, "tools/dados/shrines-percentuais.csv (%s/%s) + eixo Source=0 (RV-30)" % (aura, tipo)


# --------------------------------------------------------------- casos: RW por tipo


def _caso_atributo(caso, obs_list, ident_kw):
    """RV-26/28: valor da linha por personagem (receptor/source), duas pessoas, dedupe."""
    crits = []
    for p in caso.get("personagens") or []:
        nome, bonus = p.get("nome"), float(p.get("bonus", 0))
        pid = "%s/bonus=%s" % (p.get("id", nome), checa.fmt(bonus))
        esp, fonte = _fonte_buff(caso["aura"], caso["atributo"], bonus)
        esperado = {"valor": esp,
                    "fonte": "%s <- %s" % (ESPERADO, fonte) if esp is not None else
                             "SEM linha na tabela gerada para (%s/%s/bonus=%s)"
                             % (caso["aura"], caso["atributo"], checa.fmt(bonus)),
                    "grandeza": "contribuicao das auras (RV-44)"}
        o, a = _achar_acumulado(obs_list, caso["aura"], nome, bonus)
        if o is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                               "sem linha RV-31 acumulado de char=%s bonus=%s aura=%s no feed "
                               "(coletar o hover com esse personagem DENTRO da aura)"
                               % (nome, checa.fmt(bonus), caso["aura"]),
                               "execucao", False, []))
            continue
        if esp is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                               "a tabela gerada NAO tem (%s/%s/bonus=%s): regenerar com "
                               "tools/gera_shrines_esperado.py"
                               % (caso["aura"], caso["atributo"], checa.fmt(bonus)),
                               o["rotulo"], False, _evidencia_obs(o["_raw"])))
            continue
        it = _item_de(a, caso["atributo"])
        obs_val = None if it is None else it["contrib"]
        extra = {"personagem": nome, "bonus": bonus, "superficie_feed": o["relatorio"],
                 "instancias": a.get("instancias") or []}
        if obs_val is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                               "a linha existe mas NAO traz o item '%s' (aura viva sem item? "
                               "ver RV-46 AVISO)" % caso["atributo"],
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        if abs(obs_val - esp) > 1e-9:
            crits.append(_crit(caso, pid, "REPROVADO", esperado, obs_val,
                               "contribuicao difere do esperado independente (dif=%+g): "
                               "valor de OUTRO personagem, soma entre personagens ou "
                               "contribuicao multiplicada (RV-46)" % (obs_val - esp),
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        st, pr, motivo = _decisao(o["_raw"], ident_kw)
        crits.append(_crit(caso, pid, st, esperado, obs_val, motivo, o["rotulo"], pr,
                           _evidencia_obs(o["_raw"]), extra))
    return crits


def _caso_sem_atributo(caso, obs_list, ident_kw):
    """RV-28/46: item proprio da aura sem atributo (Dwarven/Decay/Flame)."""
    crits = []
    for p in caso.get("personagens") or []:
        nome, bonus = p.get("nome"), float(p.get("bonus", 0))
        pid = "%s/bonus=%s" % (p.get("id", nome), checa.fmt(bonus))
        esp, fonte = _fonte_buff(caso["aura"], "", bonus)
        esperado = {"valor": esp, "fonte": "%s <- %s" % (ESPERADO, fonte),
                    "grandeza": caso.get("rotulo", "item sem atributo (RV-46)")}
        if esp is None or not fonte:
            crits.append(_crit(caso, pid, 'NAO_EXERCITADO', esperado, None,
                               'fonte independente ausente: item sem atributo nao tem esperado',
                               'execucao', False, []))
            continue
        o, a = _achar_acumulado(obs_list, caso["aura"], nome, bonus)
        if o is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                               "sem linha RV-31 acumulado de char=%s bonus=%s aura=%s"
                               % (nome, checa.fmt(bonus), caso["aura"]),
                               "execucao", False, []))
            continue
        chave = caso.get("chave_item", "Stun chance")
        obs_val = a["sem_atributo"].get(chave)
        extra = {"personagem": nome, "bonus": bonus, "superficie_feed": o["relatorio"]}
        if obs_val is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                               "a linha existe mas nao traz o item '%s' da aura sem atributo "
                               "(o item proprio e o que torna a aura verificavel - RV-46)"
                               % chave, o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        if esp is not None and abs(float(obs_val) - esp) > 1e-9:
            crits.append(_crit(caso, pid, "REPROVADO", esperado, obs_val,
                               "item '%s' difere do esperado independente (dif=%+g)"
                               % (chave, float(obs_val) - esp),
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        st, pr, motivo = _decisao(o["_raw"], ident_kw)
        crits.append(_crit(caso, pid, st, esperado, obs_val, motivo, o["rotulo"], pr,
                           _evidencia_obs(o["_raw"]), extra))
    return crits


def _caso_perigo(caso, obs_list, ident_kw):
    """RV-33/34: dano por alvo (Decay = vida do PORTADOR; Flame = vida do ATACANTE projetado)."""
    crits = []
    for alvo in caso.get("alvos") or []:
        nome, tipo = alvo.get("nome"), alvo.get("tipo")
        bonus = float(alvo.get("bonus", 0))
        pid = "%s/tipo=%s/bonus=%s" % (nome, tipo, checa.fmt(bonus))
        esp = None
        fonte = None
        achado = None
        for o in obs_list:
            if not o["coleta"]:
                continue
            for d in o["coleta"]["decay"]:
                if (caso["aura"] == "Decay Shrine Aura" and d["char"] == nome
                        and abs(d["bonus"] - bonus) < 1e-9 and d["dano"] is not None):
                    achado = (o, d["dano"], d["mh"], d.get("tipo"))
            for f in o["coleta"]["flame"]:
                if (caso["aura"] == "Flame Shrine Aura" and f["nome"] == nome
                        and abs(f["bonus"] - bonus) < 1e-9
                        and (f["tipo"] or "").lower() == (tipo or "").lower()):
                    achado = (o, f["dano"], f["mh"], f["tipo"])
        if achado is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO",
                               {"valor": None, "fonte": "tools/dados/shrines-percentuais.csv",
                                "grandeza": "dano por alvo (RV-33/34)"}, None,
                               "sem linha de dano para alvo=%s tipo=%s bonus=%s (%s na area)"
                               % (nome, tipo, checa.fmt(bonus),
                                  "dentro do Decay" if caso["aura"].startswith("Decay")
                                  else "atacando dentro do Flame"),
                               "execucao", False, []))
            continue
        o, dano, mh, tipo_log = achado
        esp, fonte = _esperado_perigo(caso["aura"], tipo_log if caso["aura"].startswith("Flame")
                                      else tipo, mh)
        esperado = {"valor": esp, "fonte": fonte, "maxhealth": mh,
                    "grandeza": "dano por alvo (RV-33/34)"}
        extra = {"alvo": nome, "tipo": tipo_log, "bonus": bonus,
                 "superficie_feed": o["relatorio"]}
        if esp is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, dano,
                               "tipo '%s' fora da tabela de percentuais gerada" % tipo_log,
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        if abs(dano - esp) > 1e-9:
            crits.append(_crit(caso, pid, "REPROVADO", esperado, dano,
                               "dano difere do esperado independente (dif=%+g): o eixo dos "
                               "dados ou a vida do personagem certo mudou (RV-30/33/34)"
                               % (dano - esp), o["rotulo"], False,
                               _evidencia_obs(o["_raw"]), extra))
            continue
        st, pr, motivo = _decisao(o["_raw"], ident_kw)
        crits.append(_crit(caso, pid, st, esperado, dano, motivo, o["rotulo"], pr,
                           _evidencia_obs(o["_raw"]), extra))
    return crits


def _caso_globule(caso, obs_list, ident_kw):
    """RV-28/32: cura dinamica do Sustenance no tooltip do globule, por personagem.

    O esperado da % vem da ACAO do motor (`docs/cobertura/acoes.csv`), nao do log; a vida/mana
    saem do POOL declarado no corpo da frase (entrada, nao esperado).
    """
    crits = []
    acoes = acoes_sustenance()
    for p in caso.get("personagens") or []:
        nome = p.get("nome")
        pid = p.get("id", nome)
        achado = None
        for o in obs_list:
            for linha in o["feed_txt"].splitlines():
                m = RE_GLOBULE.match(linha)
                if not m:
                    continue
                n = RE_GLOBULE_NUM.match(m.group("p").strip())
                if not n or (caso.get("chave") and n.group("chave") != caso["chave"]):
                    continue
                if n.group("char") == nome:
                    achado = (o, n)
        if achado is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO",
                               {"pct": None, "tiers": p.get("tiers"),
                                "fonte": ACOES, "grandeza": "cura do Sustenance (RV-28/32)"}, None,
                               "sem linha `[Globule RV-28]` de char=%s chave=%r no feed "
                               "(hover no globule com o personagem em foco)"
                               % (nome, caso.get("chave")), "execucao", False, []))
            continue
        o, n = achado
        # As TIERS sao entrada DECLARADA pelo log (o jogo escolhe quais estao ativas); a % de cada
        # uma vem da ACAO do motor (fonte independente). O caso tambem declara as tiers esperadas:
        # divergencia => a rodada nao e o cenario pedido.
        tiers = [t.strip() for t in re.split(r"\s+and\s+", n.group("tiers").strip()) if t.strip()]
        fonte = "%s (%s)" % (ACOES, ", ".join("%s -> %.2f" % (t, acoes.get(t + " Proc", 0.0))
                                              for t in tiers))
        esp_pct = None
        if tiers and all((t + " Proc") in acoes for t in tiers):
            esp_pct = round(sum(acoes[t + " Proc"] for t in tiers) * 100.0, 1)
        esperado = {"pct": esp_pct, "tiers": tiers, "fonte": fonte,
                    "grandeza": "cura do Sustenance (RV-28/32)"}
        pct_log = float(n.group("pct"))
        extra = {"personagem": nome, "chave": n.group("chave"),
                 "tiers_log": n.group("tiers"), "frase": n.group("frase")}
        if p.get("tiers") and [t.strip() for t in p["tiers"]] != tiers:
            crits.append(_crit(caso, pid, "REPROVADO", dict(esperado, tiers_caso=p["tiers"]),
                               {"tiers_log": tiers},
                               "as tiers ativas do log (%s) nao sao as do cenario (%s)"
                               % (", ".join(tiers), ", ".join(p["tiers"])),
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        if esp_pct is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, pct_log,
                               "acao do Sustenance ausente no censo de acoes (%s): sem fonte "
                               "independente para a %% - nao comparar contra o log" % ACOES,
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        if abs(pct_log - esp_pct) > 0.05:
            crits.append(_crit(caso, pid, "REPROVADO", esperado, pct_log,
                               "%% do Sustenance difere da acao do motor (dif=%+g)"
                               % (pct_log - esp_pct), o["rotulo"], False,
                               _evidencia_obs(o["_raw"]), extra))
            continue
        mh = p.get("max_health")
        mm = p.get("max_mana")
        if mh is None or mm is None:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, pct_log,
                               "observacao sem o POOL declarado (max_health/max_mana): a frase "
                               "carrega o numero e nao da para conferir sem o pool",
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        m = RE_GLOBULE_HEALTH.search(n.group("frase"))
        if not m:
            crits.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, pct_log,
                               "frase do globule sem o par 'health/mana with your current "
                               "pools' (formato do GlobulePatch mudou?)",
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        h_log, m_log = float(m.group("h")), float(m.group("m"))
        h_esp = round(mh * esp_pct / 100.0, 1)
        m_esp = round(mm * esp_pct / 100.0, 1)
        if abs(h_log - h_esp) > 0.05 or abs(m_log - m_esp) > 0.05:
            crits.append(_crit(caso, pid, "REPROVADO",
                               {"pct": esp_pct, "health": h_esp, "mana": m_esp, "fonte": fonte,
                                "grandeza": "cura do Sustenance (RV-28/32)"},
                               {"health": h_log, "mana": m_log},
                               "frase nao fecha com o pool declarado x a %% do motor",
                               o["rotulo"], False, _evidencia_obs(o["_raw"]), extra))
            continue
        st, pr, motivo = _decisao(o["_raw"], ident_kw)
        crits.append(_crit(caso, pid, st, esperado, pct_log, motivo, o["rotulo"], pr,
                           _evidencia_obs(o["_raw"]), extra))
    return crits


def _caso_entrar_sair(caso, obs_list, ident_kw):
    """RV-29/31: DENTRO da aura a linha aparece; FORA nao aparece.

    O caso declara o CENARIO (personagem + espera) e cada observacao daquele personagem tem de
    DECLARAR `dentro_da_aura` - sem a declaracao nao ha valor-verdade (NAO_EXERCITADO), e uma
    declaracao que CONTRADIZ o cenario e INDETERMINADO (a rodada nao e a pedida).
    """
    crits = []
    alvo = caso.get("personagem")
    esperado_base = {"aura": caso["aura"], "linha_visivel": bool(caso.get("dentro_da_aura")),
                     "fonte": "BetterTooltips/Patches/ShrineAuraPatch.cs (AurasVivas: filtro "
                              "pela lista viva Character.ActionStatuses - RV-29/31)"}
    obs_alvo = [o for o in obs_list if o["_raw"].get("personagem") == alvo]
    if not obs_alvo:
        return [_crit(caso, None, "NAO_EXERCITADO", esperado_base, None,
                      "nenhuma observacao do personagem %r na rodada: a coleta tem de nomear o "
                      "personagem em foco para o caso entrar/sair ter valor" % alvo,
                      "execucao", False, [])]
    for o in obs_alvo:
        dentro = o["_raw"].get("dentro_da_aura")
        if dentro is None:
            crits.append(_crit(caso, None, "NAO_EXERCITADO", esperado_base, None,
                               "a observacao NAO declara se o personagem estava DENTRO ou FORA "
                               "da aura: sem isso o teste nao tem valor-verdade (entrar e sair e "
                               "o proprio caso)", "execucao", False, []))
            continue
        if bool(dentro) != bool(caso.get("dentro_da_aura")):
            crits.append(_crit(caso, None, "INDETERMINADO", esperado_base,
                               {"dentro_da_aura": bool(dentro)},
                               "a rodada declara `dentro_da_aura=%s` e o cenario pede %s: nao e "
                               "a rodada do caso (a propria declaracao nao pode ser o esperado)"
                               % (bool(dentro), bool(caso.get("dentro_da_aura"))),
                               o["rotulo"], False, _evidencia_obs(o["_raw"])))
            continue
        achado = None
        if o["coleta"]:
            for a in o["coleta"]["acumulado"]:
                if a["char"] == alvo and caso["aura"] in a["auras"]:
                    achado = a
        if caso.get("dentro_da_aura"):
            if achado is None:
                crits.append(_crit(caso, None, "REPROVADO", esperado_base, {"linha": False},
                                   "personagem declarado DENTRO da aura e a linha NAO apareceu: "
                                   "o filtro da lista viva sumiu com uma aura viva (RV-29)",
                                   o["rotulo"], False, _evidencia_obs(o["_raw"]),
                                   {"personagem": alvo}))
                continue
            st, pr, motivo = _decisao(o["_raw"], ident_kw)
            crits.append(_crit(caso, None, st, esperado_base,
                               {"linha": True, "itens": achado["itens"]}, motivo,
                               o["rotulo"], pr, _evidencia_obs(o["_raw"]),
                               {"personagem": alvo}))
            continue
        if achado is not None:
            crits.append(_crit(caso, None, "REPROVADO", esperado_base,
                               {"linha": True, "auras": achado["auras"]},
                               "a linha apareceu com o personagem FORA da aura: o filtro da "
                               "lista viva regrediu (RV-29)", o["rotulo"], False,
                               _evidencia_obs(o["_raw"]), {"personagem": alvo}))
            continue
        st, pr, motivo = _decisao(o["_raw"], ident_kw)
        crits.append(_crit(caso, None, st, esperado_base, {"linha": False}, motivo,
                           o["rotulo"], pr, _evidencia_obs(o["_raw"]), {"personagem": alvo}))
    return crits


def _caso_dedupe(caso, obs_list, ident_kw):
    """RV-31/46: a MESMA aura repetida na lista viva conta UMA vez (o motor soma instancias)."""
    nome, bonus = caso["personagem"], float(caso.get("bonus", 0))
    esp, fonte = _fonte_buff(caso["aura"], caso["atributo"], bonus)
    esperado = {"valor": esp, "instancias_min": caso.get("instancias_min", 2),
                "fonte": "%s <- %s (a contribuicao conta a aura 1x, nao por instancia)"
                         % (ESPERADO, fonte),
                "grandeza": "contribuicao deduplicada (RV-31/46)"}
    o, a = _achar_acumulado(obs_list, caso["aura"], nome, bonus)
    if o is None:
        return [_crit(caso, None, "NAO_EXERCITADO", esperado, None,
                      "sem linha RV-31 acumulado de char=%s bonus=%s aura=%s"
                      % (nome, checa.fmt(bonus), caso["aura"]), "execucao", False, [])]
    if esp is None:
        return [_crit(caso, None, "NAO_EXERCITADO", esperado, None,
                      "a tabela gerada NAO tem (%s/%s/bonus=%s): regenerar com "
                      "tools/gera_shrines_esperado.py"
                      % (caso["aura"], caso["atributo"], checa.fmt(bonus)),
                      o["rotulo"], False, _evidencia_obs(o["_raw"]))]
    contagem = 0
    for bruto in a.get("instancias") or []:
        m = re.match(r"^(?P<nome>.+?) x(?P<n>[0-9]+)$", bruto.strip())
        if m and m.group("nome") == caso["aura"]:
            contagem = int(m.group("n"))
    it = _item_de(a, caso["atributo"])
    obs_val = None if it is None else it["contrib"]
    if contagem < int(caso.get("instancias_min", 2)):
        return [_crit(caso, None, "NAO_EXERCITADO", esperado, obs_val,
                      "a rodada nao exercitou a REPETICAO da aura (instancias de %s=%d < %s): "
                      "entrar/sair da area (re)entrada cria status novo - repetir a coleta"
                      % (caso["aura"], contagem, caso.get("instancias_min", 2)),
                      o["rotulo"], False, _evidencia_obs(o["_raw"]),
                      {"instancias": a.get("instancias") or []})]
    if obs_val is None:
        return [_crit(caso, None, "NAO_EXERCITADO", esperado, None,
                      "linha sem o item '%s'" % caso["atributo"], o["rotulo"], False,
                      _evidencia_obs(o["_raw"]), {"instancias": a.get("instancias")})]
    if abs(obs_val - esp) > 1e-9:
        return [_crit(caso, None, "REPROVADO", esperado, obs_val,
                      "contribuicao multiplicada pelas %d instancias (RV-46): esperado %s "
                      "(a aura 1x), obtido %s" % (contagem, checa.fmt(esp), checa.fmt(obs_val)),
                      o["rotulo"], False, _evidencia_obs(o["_raw"]),
                      {"instancias": a.get("instancias")})]
    st, pr, motivo = _decisao(o["_raw"], ident_kw)
    return [_crit(caso, None, st, esperado, obs_val,
                  "%s; instancias=[%s] descartadas da conta (RV-46)" % (motivo, ", ".join(a.get("instancias") or [])),
                  o["rotulo"], pr, _evidencia_obs(o["_raw"]),
                  {"instancias": a.get("instancias") or []})]


def _caso_limite(caso, obs_list, ident_kw, asset=None):
    """RV-46/RV-50c: TETO/PISO do atributo - total no limite, contribuicao nao cortada."""
    nome, atributo = caso["personagem"], caso["atributo"]
    limite = limite_no_asset(atributo, asset)
    if limite is None:
        return [_crit(caso, None, "NAO_EXERCITADO",
                      {"valor": None, "fonte": LIMITES_ASSET.get(atributo, ("?", 0, "sem offset documentado"))[2],
                       "grandeza": "teto/piso do atributo (RV-46/50c)"}, None,
                      "limite de '%s' sem offset DOCUMENTADO no asset ou asset ausente: nao se "
                      "compara contra o log do proprio mod (fonte independente obrigatoria)"
                      % atributo, "execucao", False, [])]
    rotulo_asset, valor_asset, citacao = limite
    esperado = {"valor": valor_asset, "campo": rotulo_asset, "fonte": citacao,
                "grandeza": "teto/piso do atributo (RV-46/50c)"}
    achado = None
    for o in obs_list:
        if not o["coleta"]:
            continue
        c = o["coleta"]
        chave = (nome, atributo)
        if atributo == "DamageReduction" and chave in c["tetos"]:
            achado = (o, "teto", c["tetos"][chave], c["cru"].get(chave))
        elif chave in c["pisos"]:
            achado = (o, "piso", c["pisos"][chave], c["cru"].get(chave))
    if achado is None:
        return [_crit(caso, None, "NAO_EXERCITADO", esperado, None,
                      "sem linha `RV-46 %s` de char=%s atributo=%s no feed"
                      % ("teto" if rotulo_asset == "MaxValue" else "piso", nome, atributo),
                      "execucao", False, [])]
    o, qual, valor_log, cru = achado
    extra = {"personagem": nome, "limite": qual, "cru": cru}
    if abs(valor_log - valor_asset) > 1e-9:
        return [_crit(caso, None, "REPROVADO", esperado, valor_log,
                      "o %s logado difere do asset (dif=%+g): ler o offset documentado de novo "
                      "e conferir o build" % (rotulo_asset, valor_log - valor_asset),
                      o["rotulo"], False,
                      _evidencia_obs(o["_raw"]), extra)]
    # A contribuicao da aura nao pode ter sido cortada: ela sai da tabela gerada, nao do total.
    esp_contrib, fonte = _fonte_buff(caso.get("aura", ""), atributo, float(caso.get("bonus", 0)))
    o2, a = _achar_acumulado(obs_list, caso.get("aura", ""), nome, float(caso.get("bonus", 0)))
    if esp_contrib is None or a is None or _item_de(a, atributo) is None:
        return [_crit(caso, None, 'NAO_EXERCITADO', esperado, None,
                      'limite exige contribuicao preservada e fonte independente',
                      o['rotulo'], False, _evidencia_obs(o['_raw']), extra)]
    if esp_contrib is not None and a is not None:
        it = _item_de(a, atributo)
        if it is not None and abs(it["contrib"] - esp_contrib) > 1e-9:
            return [_crit(caso, None, "REPROVADO",
                          dict(esperado, contribuicao=esp_contrib, fonte_contrib=fonte),
                          {"contrib": it["contrib"], "total": it["total"]},
                          "a CONTRIBUICAO foi cortada pelo limite: o teto corta o TOTAL, nunca "
                          "a contribuicao da aura (RV-50c)", o["rotulo"], False,
                          _evidencia_obs(o["_raw"]), extra)]
    regex = checa.RE_TETO if rotulo_asset == 'MaxValue' else checa.RE_PISO
    linhas = []
    for linha in o['feed_txt'].splitlines():
        match = regex.search(linha.split('[Shrine RV-23] ', 1)[-1])
        if match and match['char'] == nome and match['atributo'] == atributo:
            linhas.append(match)
    if not linhas or any(m['cru'] is None for m in linhas):
        return [_crit(caso, None, 'NAO_EXERCITADO', esperado, None,
                      'limite sem total/cru/flag no-limite medidos', o['rotulo'], False,
                      _evidencia_obs(o['_raw']), extra)]
    for m in linhas:
        total, bruto = checa.numero(m['total']), checa.numero(m['cru'])
        clampado = min(bruto, valor_asset) if rotulo_asset == 'MaxValue' else max(bruto, valor_asset)
        flag = m['no_teto'] if rotulo_asset == 'MaxValue' else m['no_piso']
        if abs(total-clampado) > 1e-9 or (flag == 'sim') != (abs(total-valor_asset) < 1e-9):
            return [_crit(caso, None, 'REPROVADO', dict(esperado, total_clampado=clampado),
                          {'total': total, 'cru': bruto, 'flag': flag},
                          'total/valor cru/flag no-limite contradizem o clamp', o['rotulo'], False,
                          _evidencia_obs(o['_raw']), extra)]
    it = _item_de(a, atributo)
    ultimo = linhas[-1]
    total = checa.numero(ultimo['total'])
    total_item = it['total']
    flag = ultimo['no_teto'] if rotulo_asset == 'MaxValue' else ultimo['no_piso']
    if flag != 'sim':
        return [_crit(caso, None, 'NAO_EXERCITADO', esperado, total,
                      'cenario nao exercitou o total no limite', o['rotulo'], False,
                      _evidencia_obs(o['_raw']), extra)]
    if abs(total_item-total) > 1e-9:
        return [_crit(caso, None, 'REPROVADO', dict(esperado, total=total), total_item,
                      'total da contribuicao contradiz total clampado', o['rotulo'], False,
                      _evidencia_obs(o['_raw']), extra)]
    st, pr, motivo = _decisao(o["_raw"], ident_kw)
    if pr:
        st2, pr2, motivo2 = _decisao(o2['_raw'], ident_kw)
        if not pr2 or o['_raw'].get('sessao') != o2['_raw'].get('sessao'):
            st, pr, motivo = st2 or 'INDETERMINADO', False, 'contribuicao sem cadeia compativel: ' + motivo2
    return [_crit(caso, None, st, dict(esperado, contribuicao=esp_contrib),
                  {'limite': valor_log, 'total': total, 'cru': checa.numero(ultimo['cru']),
                   'flag': flag, 'contribuicao': it['contrib']}, motivo, o["rotulo"], pr,
                  _evidencia_obs(o["_raw"]) + _evidencia_obs(o2['_raw']), extra)]


def _corpo_um(caso, obs_list, ident_kw):
    """RV-26/27: o CORPO renderizado da tooltip de shrine traz a LINHA e a NOTA."""
    esperado = {"contem": [MARCA_LINHA], "nota": caso.get("nota_fragmento", NOTA_SHRINE),
                "fonte": "BetterTooltips/Patches/LocalizePatch.cs + ShrineAuraPatch.cs "
                         "(linha 'Your active shrine auras:' e a nota do Shrine Effect Bonus)"}
    superficie = caso.get("superficie", "tooltip_shrine")
    achado = next((o for o in obs_list
                   if o["render"] and o["_raw"].get("superficie") == superficie), None)
    if achado is None:
        return [_crit(caso, None, "NAO_EXERCITADO", esperado, None,
                      "sem observacao da superficie %r com texto renderizado (o corpo NAO esta "
                      "no log do mod; coletar o objeto vivo com o AUT-4)" % superficie,
                      "execucao", False, [])]
    estado, motivo = validacoes.corpo(achado)
    if estado:
        return [_crit(caso, None, estado, esperado, achado['render'], motivo,
                      achado['rotulo'], False, _evidencia_obs(achado['_raw']))]
    falta = [m for m in esperado["contem"] if m not in achado["render"]]
    if falta:
        return [_crit(caso, None, "REPROVADO", esperado, {"faltando": falta},
                      "o corpo da tooltip de shrine nao traz a linha (%s): a linha azul "
                      "regrediu no texto renderizado (RV-26/27)" % ", ".join(falta),
                      achado["rotulo"], False, _evidencia_obs(achado["_raw"]))]
    if esperado["nota"] and esperado["nota"] not in achado["render"]:
        return [_crit(caso, None, "NAO_EXERCITADO",
                      esperado, {"nota_ausente": esperado["nota"]},
                      "corpo sem a nota do Shrine Effect Bonus: com bonus ZERO a nota nao "
                      "aparece por desenho - coletar tambem o caso com Omnism/Horn",
                      achado["rotulo"], False, _evidencia_obs(achado["_raw"]))]
    st, pr, motivo = _decisao(achado["_raw"], ident_kw)
    return [_crit(caso, None, st, esperado, {"linha": True, "nota": True}, motivo,
                  achado["rotulo"], pr, _evidencia_obs(achado["_raw"]))]


def _armor_um(caso, obs_list, ident_kw):
    """BUG-34 (regressao, `reabre_bug=False`): feed/texto flutuante SEM a nota; corpo COM a nota.

    Duas superficies, dois criterios: o log/texto flutuante de combate NUNCA pode carregar a
    nota de Armor (`blocks damage`), e o CORPO da tooltip do status TEM de continuar com ela.
    """
    crits = []
    base = {"regressao_de": "BUG-34", "reabre_bug": False}
    sup_feed = caso.get("superficie_feed", "feed")
    sup_corpo = caso.get("superficie_corpo", "tooltip_status")
    obs_feed = [o for o in obs_list if o["_raw"].get("superficie") == sup_feed]
    texto_feed = "\n".join(o["feed_txt"] + '\n' + o["render"] for o in obs_feed)
    esperado_feed = {"ausente": NOTA_ARMOR,
                     "fonte": "BetterTooltips/Patches/LocalizePatch.cs (EmTextoDeFeed: o funil "
                              "pula Armor/Resistencia dentro de Root.SendMessageWindowMessage e "
                              "OverheadMessageDisplay.SpawnOverheadMessage)"}
    if not obs_feed or not texto_feed.strip():
        crits.append(_crit(caso, "feed", "NAO_EXERCITADO", esperado_feed, None,
                           "sem observacao da superficie %r (texto de FEED/texto flutuante): a "
                           "regressao exige o texto de combate observado" % sup_feed,
                           "execucao", False, [], dict(base)))
    elif NOTA_ARMOR in texto_feed:
        crits.append(_crit(caso, "feed", "REPROVADO", esperado_feed, {"contem": NOTA_ARMOR},
                           "a nota de Armor VAZOU para o feed/texto flutuante (regressao do "
                           "BUG-34; o diagnostico NAO e reaberto)", obs_feed[0]["rotulo"], False,
                           _evidencia_obs(obs_feed[0]["_raw"]), dict(base)))
    else:
        o = obs_feed[0]
        st, pr, motivo = _decisao(o["_raw"], ident_kw)
        crits.append(_crit(caso, "feed", st, esperado_feed, {"ausente": True},
                           "regressao OK: a nota NAO voltou ao feed (%s)" % motivo,
                           o["rotulo"], pr, _evidencia_obs(o["_raw"]), dict(base)))
    corpo = next((o for o in obs_list
                  if o["_raw"].get("superficie") == sup_corpo and o["render"]), None)
    esperado_corpo = {"presente": NOTA_ARMOR,
                      "fonte": "BetterTooltips/Patches/LocalizePatch.cs (BuildArmorNote: a nota "
                               "continua no CORPO da tooltip do status)"}
    if corpo is None:
        crits.append(_crit(caso, "corpo", "NAO_EXERCITADO", esperado_corpo, None,
                           "sem observacao do CORPO da tooltip do status (superficie=%s): o "
                           "texto da tooltip nao sai no log do mod - coletar o objeto vivo"
                           % sup_corpo, "execucao", False, [], dict(base)))
    elif NOTA_ARMOR not in corpo["render"]:
        crits.append(_crit(caso, "corpo", "REPROVADO", esperado_corpo, {"ausente": NOTA_ARMOR},
                           "a nota de Armor SUMIU do corpo da tooltip (regressao do BUG-34, "
                           "lado oposto do vazamento)", corpo["rotulo"], False,
                           _evidencia_obs(corpo["_raw"]), dict(base)))
    else:
        estado, erro = validacoes.corpo(corpo)
        st, pr, motivo = (estado, False, erro) if estado else _decisao(corpo["_raw"], ident_kw)
        crits.append(_crit(caso, "corpo", st, esperado_corpo, {"presente": True},
                           ("regressao OK: o corpo da tooltip continua com a nota (%s)" % motivo)
                           if pr else motivo,
                           corpo["rotulo"], pr, _evidencia_obs(corpo["_raw"]), dict(base)))
    return crits


def _caso_divergencia_rv49(caso, obs_list, ident_kw):
    """RV-34/49: registra a DIVERGENCIA dos fatos atuais - nunca vira OK por mudar a formula."""
    esperado = {
        "fato_30_09": "com o prefix do RV-34 o numero do dano 'dobrava' com bonus (medição em jogo)",
        "fato_30_09_fonte": "docs/cobertura/revisao/RV-19-shrines.md + scratch/task_worship.md",
        "fato_03_10": "o RV-30 para de escrever `Source`; as auras de PERIGO avaliam com "
                      "`Source=null` (bonus do SHRINE, 0) e o numero NAO escala com o jogador",
        "fato_03_10_fonte": "BetterTooltips/CHANGELOG.md (RV-48/RV-30) + tools/dados/shrines-esperado.csv (coluna eixo=Source)",
        "decisao": "RV-49 PENDENTE do dono: medir em jogo com/sem Omnism/Horn e decidir a versao",
        "regra": "registrar a divergencia SEM alterar a formula para ficar verde",
    }
    return [_crit(caso, None, "INDETERMINADO", esperado, None,
                  "divergencia registrada: os dois fatos coexistem e a decisao (RV-49) e do dono; "
                  "a automacao NAO escolhe a versao nem ajusta a formula para fechar verde",
                  "runtime", False, [],
                  {"autorizacao_necessaria": False, "tipo_pendencia": "divergencia_de_medicao",
                   "lacuna_probe": "RV-49: as duas medicoes coexistem; resolver por coleta/ajuste "
                                   "rastreavel (nunca escolher a versao para obter verde)",
                   "decisao": "RV-49", 'instrucoes_humanas':
                   'RV-49: decidir a versao diante das medicoes conflitantes de 30/09 e 03/10; '
                   'nao alterar formulas para obter verde.'})]


def _mesclar(resultados):
    """Pior resultado por ID; nenhuma medicao posterior desaparece."""
    groups = {}
    for c in resultados:
        groups.setdefault(c['id'], []).append(c)
    out = []
    severidade = {'OK': 0, 'NAO_EXERCITADO': 1, 'INDETERMINADO': 2, 'REPROVADO': 3}
    for cs in groups.values():
        c = dict(max(cs, key=lambda x: severidade[x['estado']]))
        c['medicoes'] = [{'estado': x['estado'], 'observado': x['observado'],
                          'evidencia': x['evidencia'], 'motivo': x['motivo']} for x in cs]
        c['evidencia'] = [e for x in cs for e in x['evidencia']]
        c['prova_runtime'] = c['estado'] == 'OK' and all(x['prova_runtime'] for x in cs)
        if not c['prova_runtime']:
            for key in ('sessao', 'fonte_sha', 'dll_sha', 'config_sha'):
                c.pop(key, None)
        out.append(c)
    return out


def _caso_corpo(caso, obs_list, ident_kw):
    superficie = caso.get('superficie', 'tooltip_shrine')
    candidatos = [o for o in obs_list if o['_raw'].get('superficie') == superficie]
    if not candidatos:
        base = _corpo_um(caso, [], ident_kw)
        o = {'_raw': {}, 'rotulo': 'execucao'}
        candidatos_estilo = [o]
    else:
        base = _mesclar([c for o in candidatos for c in _corpo_um(caso, [o], ident_kw)])
        candidatos_estilo = candidatos
        alvos = {(o['_raw'].get('personagem'), o['_raw'].get('objeto'), o['_raw'].get('sessao'))
                 for o in candidatos if o['rotulo'] == 'runtime'}
        if len(alvos) > 1:
            for c in base:
                c.update(estado='INDETERMINADO', prova_runtime=False,
                         motivo='corpos de alvos/sessoes diferentes sem cenario inequívoco')
    styles = []
    for o in candidatos_estilo:
        for pid, (st, motivo), esperado, observado in validacoes.estilo(o['_raw']):
            pr = False
            if st is None:
                st, pr, motivo = _decisao(o['_raw'], ident_kw)
                visual_st, visual_motivo = validacoes.corpo(o)
                if visual_st:
                    st, pr, motivo = visual_st, False, visual_motivo
            styles.append(_crit(caso, pid, st, esperado, observado, motivo,
                                o['rotulo'], pr, _evidencia_obs(o['_raw'])))
    return base + _mesclar(styles)


def _caso_armor(caso, obs_list, ident_kw):
    sup_feed, sup_corpo = caso.get('superficie_feed', 'feed'), caso.get('superficie_corpo', 'tooltip_status')
    feeds = [o for o in obs_list if o['_raw'].get('superficie') == sup_feed]
    corpos = [o for o in obs_list if o['_raw'].get('superficie') == sup_corpo]
    resultados = []
    for o in feeds or [None]:
        # Evaluate EVERY combat and body measurement independently; never first-win.
        cs = _armor_um(caso, [o] if o else [], ident_kw)
        resultados.extend(c for c in cs if c['id'].endswith('/feed'))
    for o in corpos or [None]:
        cs = _armor_um(caso, [o] if o else [], ident_kw)
        resultados.extend(c for c in cs if c['id'].endswith('/corpo'))
    floats = [o for o in obs_list if o['_raw'].get('superficie') == 'flutuante']
    # Legacy combined fixture surface is useful only as a logic test, not runtime coverage.
    if not floats and feeds and all(o['rotulo'] == 'fixture' for o in feeds):
        floats = feeds
    if not floats:
        resultados.append(_crit(caso, 'flutuante', 'NAO_EXERCITADO',
                                {'ausente': NOTA_ARMOR, 'fonte': 'BetterTooltips/Patches/LocalizePatch.cs EmTextoDeFeed'}, None,
                                'sem coleta separada do texto flutuante Armor', 'execucao', False, [],
                                {'regressao_de': 'BUG-34', 'reabre_bug': False}))
    for o in floats:
        if not o['render']:
            st, pr, motivo = 'NAO_EXERCITADO', False, 'texto flutuante renderizado ausente'
        elif NOTA_ARMOR in o['render']:
            st, pr, motivo = 'REPROVADO', False, 'nota Armor vazou no texto flutuante'
        else:
            visual_st, visual_motivo = validacoes.corpo(o)
            st, pr, motivo = ((visual_st, False, visual_motivo) if visual_st
                              else _decisao(o['_raw'], ident_kw))
        resultados.append(_crit(caso, 'flutuante', st,
                                {'ausente': NOTA_ARMOR, 'fonte': 'BetterTooltips/Patches/LocalizePatch.cs EmTextoDeFeed'},
                                o['render'], motivo, o['rotulo'], pr, _evidencia_obs(o['_raw']),
                                {'regressao_de': 'BUG-34', 'reabre_bug': False}))
    return _mesclar(resultados)


def _transicao(casos, obs_list, ident_kw):
    """Temporal: mesmo alvo, sessao e sequencia estritamente crescente."""
    cs = [c for c in casos if c.get('tipo') == 'entrar_sair']
    if not cs:
        return []
    caso = dict(cs[0], id='S-rv29-transicao-mesmo-personagem')
    esperado = {'mesmo_personagem': True, 'mesma_sessao': True, 'ordem': 'dentro -> fora',
                'fonte': 'docs/automacao/AUT-6; Character.ActionStatuses'}
    pares = []
    for dentro in obs_list:
        a = dentro['_raw']
        if a.get('dentro_da_aura') is not True:
            continue
        for fora in obs_list:
            b = fora['_raw']
            if b.get('dentro_da_aura') is not False:
                continue
            if not a.get('personagem') or a.get('personagem') != b.get('personagem'):
                continue
            if not a.get('sessao') or a.get('sessao') != b.get('sessao'):
                continue
            ia, ib = a.get('sequencia'), b.get('sequencia')
            if not isinstance(ia, int) or isinstance(ia, bool) or not isinstance(ib, int) or isinstance(ib, bool) or ia >= ib:
                continue
            pares.append((dentro, fora))
    if not pares:
        return [_crit(caso, None, 'NAO_EXERCITADO', esperado, None,
                      'sem entrar/sair do MESMO personagem na MESMA sessao em ordem medida',
                      'execucao', False, [])]
    resultados = []
    for a, b in pares:
        checks = []
        for o, dentro in ((a, True), (b, False)):
            local = dict(caso, personagem=o['_raw']['personagem'], dentro_da_aura=dentro)
            checks.extend(_caso_entrar_sair(local, [o], ident_kw))
        c = _mesclar(checks)[0]
        c['esperado'] = esperado
        c['observado'] = {'personagem': a['_raw']['personagem'], 'sessao': a['_raw']['sessao'],
                         'sequencias': [a['_raw']['sequencia'], b['_raw']['sequencia']]}
        resultados.append(c)
    return _mesclar(resultados)


HANDLERS = {
    "atributo": _caso_atributo,
    "sem_atributo": _caso_sem_atributo,
    "perigo": _caso_perigo,
    "globule": _caso_globule,
    "entrar_sair": _caso_entrar_sair,
    "dedupe": _caso_dedupe,
    "limite": _caso_limite,
    "corpo_tooltip": _caso_corpo,
    "armor": _caso_armor,
    "divergencia_rv49": _caso_divergencia_rv49,
}


# --------------------------------------------------------------- API


def avaliar(observacoes, identidade=None, casos=None, asset=None):
    """Contrato v1: `(observacoes, identidade) -> lista de criterios`."""
    dados = casos if isinstance(casos, dict) else _carrega_casos(casos or CASOS_PADRAO)
    obs_list = _adaptar(observacoes or [])
    for o in obs_list:
        o["relatorio"] = o["_raw"].get("relatorio") or o["_raw"].get("id") or "observacao"
    _suf, _fal, _kw = identidade_de(identidade)
    ident_kw = {"suficiente": _suf, "faltando": _fal, "kwargs": _kw}
    _RODADA.clear()
    for chave in ("fonte_sha", "dll_sha", "config_sha"):
        if isinstance(_kw.get(chave), str) and _kw[chave].strip():
            _RODADA[chave] = _kw[chave].strip()
    _RODADA["observacoes"] = [o["relatorio"] for o in obs_list]
    _RODADA["casos_sha256"] = _sha256(_casos_caminho(casos)) if not isinstance(casos, dict) else "casos-em-memoria"
    crits = []
    consumo = {}   # observacao (por identidade) -> casos que a consumiram (E7: ambiguidade)
    for caso in dados.get("casos") or []:
        scoped = []
        for o in obs_list:
            cen = o['_raw'].get('cenario')
            if o['rotulo'] != 'runtime' or cen is None:
                # Runtime SEM cenario declarado e ELEGIVEL, mas a ambiguidade fica registrada:
                # consumir a mesma observacao em mais de um caso vira INDETERMINADO abaixo.
                scoped.append(o)
            elif caso['id'] == cen or (isinstance(cen, list) and caso['id'] in cen):
                scoped.append(o)
        for o in scoped:
            if o['rotulo'] == 'runtime':
                consumo.setdefault(id(o['_raw']), []).append(caso['id'])
        tipo = caso.get("tipo")
        fn = HANDLERS.get(tipo)
        if fn is None:
            crits.append(_crit(caso, None, "INDETERMINADO",
                               {"tipo": tipo}, None,
                               "tipo de caso desconhecido pelo avaliador: %r" % tipo,
                               "execucao", False, []))
            continue
        if tipo in ("limite",):
            novos = fn(caso, scoped, ident_kw, asset=asset)
        elif tipo in ("divergencia_rv49",):
            novos = fn(caso, scoped, ident_kw)
        else:
            if tipo in ('atributo', 'sem_atributo', 'perigo', 'globule', 'dedupe'):
                fixtures = [o for o in scoped if o['rotulo'] != 'runtime']
                runtimes = [o for o in scoped if o['rotulo'] == 'runtime']
                batches = ([fixtures] if fixtures else []) + [[o] for o in runtimes]
                novos = _mesclar([c for batch in batches or [[]] for c in fn(caso, batch, ident_kw)])
            else:
                novos = fn(caso, scoped, ident_kw)
        for c in novos:
            if c['procedencia'] == 'runtime':
                c['observacoes_elegiveis'] = sorted({id(o['_raw']) for o in scoped
                                                     if o['rotulo'] == 'runtime'})
        crits.extend(novos)
    ambiguas = {chave for chave, casos_ in consumo.items() if len(set(casos_)) > 1}
    for c in crits:
        if c['procedencia'] == 'runtime' and ambiguas & set(c.get('observacoes_elegiveis') or []):
            if c['estado'] == 'OK':
                c.update(estado='INDETERMINADO', prova_runtime=False,
                         motivo='observacao sem cenario consumida por mais de um caso: ambiguidade '
                                '(associar cenario/alvo na coleta)')
        c.pop('observacoes_elegiveis', None)
    crits.extend(_transicao(dados.get('casos') or [], obs_list, ident_kw))
    # CIC-2 tambem precisa enxergar incompletude por criterio, nao so exit da CLI. O criterio
    # so existe na RODADA DECLARADA (o conjunto com o caso da divergencia do RV-49): em recorte
    # de caso isolado ele nao aparece e a incompletude vem dos proprios criterios.
    if not any(c.get('tipo') == 'divergencia_rv49' for c in dados.get('casos') or []):
        return crits
    obrigatorios = [c for c in crits if c.get('tipo_pendencia') != 'decisao_dono']
    if not obrigatorios:
        return crits  # isolamento de decisao residual, nao rodada de aceite do produto
    lacunas = [c['id'] for c in obrigatorios if c['estado'] != 'OK' or not c['prova_runtime']]
    completo = bool(obrigatorios) and not lacunas
    cobertura = {'id': 'S-aut6-completude-runtime', 'rv': [], 'mod': MOD_PADRAO}
    evidencia = [e for c in obrigatorios for e in c['evidencia']]
    crits.append(_crit(cobertura, None, 'OK' if completo else 'NAO_EXERCITADO',
                       {'todos_criterios_runtime': True, 'fonte': 'tools/automacao/aut6/casos-aut6.json'},
                       {'obrigatorios': len(obrigatorios), 'lacunas': lacunas},
                       'todos os criterios obrigatorios tem prova runtime' if completo else
                       'completude runtime ausente por criterio: ' + ', '.join(lacunas),
                       'runtime', completo, evidencia,
                       {'autorizacao_necessaria': False, 'tipo_pendencia': 'coleta_tecnica'}))
    return crits


def _carrega_casos(caminho):
    if not os.path.isfile(caminho):
        raise SystemExit("FALHA(2): casos ausentes: %s" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def resumo(crits):
    r = {"total": len(crits), "OK": 0, "REPROVADO": 0, "NAO_EXERCITADO": 0, "INDETERMINADO": 0,
         "com_prova_runtime": 0}
    for c in crits:
        r[c["estado"]] = r.get(c["estado"], 0) + 1
        if c.get("prova_runtime"):
            r["com_prova_runtime"] += 1
    return r


def exit_de(crits):
    r = resumo(crits)
    if r["REPROVADO"]:
        return EXIT_REPROVADO
    if r["NAO_EXERCITADO"] or r["INDETERMINADO"] or not crits or r["com_prova_runtime"] != r['total']:
        return EXIT_INCOMPLETO
    return EXIT_OK


def matriz_cobertura(casos, crits):
    """Cobertura por TAREFA (RV): o que foi exercitado e em que estado."""
    por_rv = {}
    for c in crits:
        for rv in c.get("tarefas_rv") or []:
            por_rv.setdefault(rv, {}).setdefault(c["estado"], []).append(c["id"])
    for caso in casos.get("casos") or []:
        for rv in caso.get("rv") or []:
            por_rv.setdefault(rv, {})
    return por_rv


def _offline(casos, asset=None):
    """Sem observacao nenhuma: prova que AUSENCIA devolve INCOMPLETO e imprime a matriz."""
    crits = avaliar([], None, casos, asset=asset)
    r = resumo(crits)
    print("AUT-6 offline (nenhuma observacao):", json.dumps(r, ensure_ascii=False))
    print("exit esperado: 2 (ausencia NAO e aprovacao) -> obtido %d" % exit_de(crits))
    print("\nCOBERTURA POR TAREFA (RV):")
    for rv, est in sorted(matriz_cobertura(casos, crits).items()):
        print("  %-10s %s" % (rv, ", ".join("%s=%d" % (k, len(v)) for k, v in sorted(est.items())) or "sem criterio"))
    return EXIT_INCOMPLETO if exit_de(crits) == EXIT_INCOMPLETO and r["OK"] == 0 else EXIT_REPROVADO


def main(argv=None):
    ap = argparse.ArgumentParser(description="AUT-6: cobertura automatizada de tooltips/shrines "
                                             "por personagem (RV-26/27/28/29/31/33/34).")
    ap.add_argument("--observacoes", help="JSON com a lista de observacoes da rodada")
    ap.add_argument("--identidade", help="JSON com a identidade da rodada (fonte_sha/dll_sha/...)")
    ap.add_argument("--casos", default=CASOS_PADRAO)
    ap.add_argument("--asset", help="resources.assets (default: autodetecta)")
    ap.add_argument("--offline", action="store_true",
                    help="sem observacoes: prova que a ausencia devolve INCOMPLETO")
    ap.add_argument("--json", dest="saida", help="grava os criterios em JSON")
    args = ap.parse_args(argv)

    casos = _carrega_casos(args.casos)
    if args.offline or not args.observacoes:
        return _offline(casos, args.asset)
    with open(args.observacoes, encoding="utf-8") as fh:
        obs = json.load(fh)
    ident = json.loads(args.identidade) if args.identidade else None
    crits = avaliar(obs, ident, casos, asset=args.asset)
    r = resumo(crits)
    print("AUT-6: %s" % json.dumps(r, ensure_ascii=False))
    for c in crits:
        marca = {"OK": "OK  ", "REPROVADO": "REPRO", "NAO_EXERCITADO": "NAO ", "INDETERMINADO": "INDET"}[c["estado"]]
        print("  %s %-46s %s" % (marca, c["id"], c["motivo"][:110]))
    print("\npor estado: OK=%d REPROVADO=%d NAO_EXERCITADO=%d INDETERMINADO=%d "
          "(com prova runtime: %d)"
          % (r["OK"], r["REPROVADO"], r["NAO_EXERCITADO"], r["INDETERMINADO"],
             r["com_prova_runtime"]))
    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as fh:
            json.dump(crits, fh, ensure_ascii=False, indent=2)
    return exit_de(crits)


if __name__ == "__main__":
    sys.exit(main())
