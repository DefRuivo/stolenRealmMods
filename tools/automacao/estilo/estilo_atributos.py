#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""estilo_atributos.py - AUT-7: medicao de ESTILO, ATRIBUTOS e DUMP (t_674c5976).

O QUE ESTE MODULO E
-------------------
A frente AUT-7 do ciclo automatico. Ele mede QUATRO mods e devolve criterios no
contrato do `docs/automacao/CICLO-VALIDACAO-escopo.md`:

    avaliar(observacoes, identidade) -> lista de criterios            (runtime)
    medir_offline(repo, out_dir, identidade) -> (criterios, meta)     (offline)

  * BetterFont          - troca de fonte + PRESERVACAO de cor/contorno/underlay e config;
  * BetterCombatText    - superficies ALVO, contraste/polaridade da sombra,
                          idempotencia e ausencia de vazamento no level-up;
  * BetterStats         - base PURA (`SavedMap`) x atributo FINAL do motor, formato e
                          GEOMETRIA da coluna de valores;
  * RoguelikeDebugger   - contrato/saneamento do dump e censo.

REUSO (regra do projeto: nao reconstruir infraestrutura pronta)
---------------------------------------------------------------
  * A MEDICAO OFFLINE roda a SUITE REAL do projeto (`tools/testes/roda_testes.py`,
    `--puros` e `--contra-prova`) e NAO reimplementa build, suite nem conferidor.
    Cada teste vira UM criterio, com a saida do runner gravada e hasheada.
  * O modelo do BetterCombatText (luminancia, baldes de sombra, contraste, alfa
    minimo, superficies alvo, tipos do level-up) e LIDO de `tools/testes/regras_bct.py`
    - a formula nao e copiada para ca.
  * A lista de propriedades que o BetterFont TEM de transportar e LIDA de
    `tools/testes/regras_bf_estilo.py` (`PRECISA_COPIAR`, `PRECISA_LIGAR`).
  * O recorte ESTRUTURAL do `BetterStats/Plugin.cs` usa `tools/testes/recorte.py`
    (casamento de chaves, nunca janela de caracteres).
  * A IDENTIDADE (`fonte_sha`/`dll_sha`) e a do CIC-1 (`ciclo.identidade`): sem ela
    NADA vira OK.

O QUE ESTE MODULO NAO FAZ
-------------------------
Nao instala probe, nao abre/fecha o jogo, nao carrega save, nao compila, nao
publica, nao muta o board e nao regenera doc curada. `NAO_EXERCITADO`/`AUSENTE`/
`INDETERMINADO` NUNCA e OK. **Fixture testa o AVALIADOR, nao comprova runtime**:
com procedencia `fixture` a ausencia de defeito sai `NAO_EXERCITADO` (nunca OK),
mas um DEFEITO plantado continua `REPROVADO` - e assim que o controle negativo
prova que a regra pega o defeito.

"CARREGADO" NAO E "EFICAZ": nenhum criterio daqui afirma que o mod funciona no
jogo. O offline prova ESTRUTURA no fonte/suite; o runtime exige leitura de objeto
vivo, com cadeia de prova (sessao + fonte_sha + dll_sha) e evidencia em arquivo.

CLI
---
    python tools/automacao/estilo/estilo_atributos.py --repo C:/dev/stolen-realm \
        --out-dir <dir-de-evidencia> [--observacoes obs.json] [--identidade ident.json] \
        [--sem-suite] [--validar-plano plano.json] [--out saida.json] [--texto]

A identidade de `--identidade` pode DECLARAR o hash da config (`config_sha`, ou um bloco
`config`/`hashes` com `sha256`): e assim que o criterio de config do BetterFont fecha OK
sem depender do CIC-1 (achado A2). Sem essa declaracao o criterio sai LACUNA dizendo o que
falta - nunca REPROVADO por um hash que a rodada nao tem como declarar.

Exit: 0 = ha criterio OK e nenhum REPROVADO · 1 = algum REPROVADO ·
      2 = nada exercitado (so NAO_EXERCITADO/INDETERMINADO) ou nao deu para medir.
"""
import argparse
import math
import configparser
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
TOOLS = os.path.join(RAIZ, "tools")
TESTES = os.path.join(TOOLS, "testes")
for _p in (TESTES, TOOLS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ESQUEMA = "AUT-7/estilo/1"
TAREFA = "t_674c5976"
MODS = ("BetterFont", "BetterCombatText", "BetterStats", "RoguelikeDebugger")

OK, REPROVADO, NAO_EXERCITADO, INDETERMINADO = (
    "OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")
EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2
CLASSES = ("offline", "runtime")
PROCEDENCIAS = ("execucao", "runtime", "fixture")

# Rotulos que NUNCA sao valor medido (mesma regra do AUT-3/AUT-4).
AUSENTES = ("AUSENTE", "NAO EXERCITADO", "NÃO EXERCITADO", "NAO_EXERCITADO",
            "INDETERMINADO", "INDETERMINATE", "-", "")

# Suite pura por mod (prefixo do arquivo de teste, como o runner publica).
SUITE_DO_MOD = {
    "BetterFont": "t_bf_",
    "BetterCombatText": "t_bct_",
    "BetterStats": "t_bs_",
    "RoguelikeDebugger": "t_debugger_",
}
# Iscas (controle NEGATIVO) por mod, em `tools/testes/contra-prova/`.
ISCA_DO_MOD = {
    "BetterFont": "cp_bf_",
    "BetterCombatText": "cp_bt_",
    "BetterStats": "cp_bs_",
    "RoguelikeDebugger": "cp_debugger_",
}

# ATRIBUICAO a indice/propriedade de `SavedMap`/`character` = escrita no personagem.
# O `=` tem de vir COLADO no fechamento do indice (sem `)`, `;` ou `{` no meio):
# sem essa ancora o padrao casa texto solto e acusa escrita que nao existe.
_RE_ESCRITA_NO_PERSONAGEM = re.compile(
    r"(?:SavedMap|character)\s*(?:\.\w+)?\s*\[[^\]]*\]\s*(?:\[[^\]]*\]\s*)?=[^=]")

# Fontes principais de cada mod (rastreabilidade do que foi medido no fonte vivo).
FONTES_DO_MOD = {
    "BetterFont": ("BetterFont/Plugin.cs",),
    "BetterCombatText": ("BetterCombatText/Plugin.cs", "BetterCombatText/TextStyler.cs",
                         "BetterCombatText/Configuracao.cs", "BetterCombatText/Patches.cs"),
    "BetterStats": ("BetterStats/Plugin.cs",),
    "RoguelikeDebugger": ("RoguelikeDebugger/EfeitosInfo.cs",
                          "RoguelikeDebugger/Patches/SkillInventoryPatch.cs",
                          "RoguelikeDebugger/Patches/ActionStatusInventoryPatch.cs"),
}

_CACHE = {}


# ------------------------------------------------------------------ utilidades ---

def _sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _ev(caminho):
    """Evidencia de um arquivo REAL: caminho absoluto + sha256. Inexistente sai fora."""
    if not caminho:
        return None
    try:
        caminho = os.path.abspath(caminho)
        if not os.path.isfile(caminho):
            return None
        return {"caminho": caminho, "sha256": _sha256(caminho)}
    except OSError:
        return None


def _evs(*caminhos):
    return [e for e in (_ev(c) for c in caminhos) if e]


def _modulo(nome, caminho):
    """Carrega um modulo do repositorio pelo caminho, com cache. Falha -> None."""
    chave = "mod:" + nome
    if chave in _CACHE:
        return _CACHE[chave]
    try:
        spec = importlib.util.spec_from_file_location(nome, caminho)
        m = importlib.util.module_from_spec(spec)
        sys.modules[nome] = m
        spec.loader.exec_module(m)
    except Exception:
        m = None
    _CACHE[chave] = m
    return m


def _ciclo():
    return _modulo("aut7_ciclo", os.path.join(TOOLS, "automacao", "ciclo", "ciclo.py"))


def _coletor():
    return _modulo("aut7_coletor", os.path.join(TOOLS, "automacao", "runtime", "coletor.py"))


def _rec():
    return _modulo("aut7_recorte", os.path.join(TESTES, "recorte.py"))


def _bct():
    return _modulo("aut7_regras_bct", os.path.join(TESTES, "regras_bct.py"))


def _bf_estilo():
    return _modulo("aut7_regras_bf_estilo", os.path.join(TESTES, "regras_bf_estilo.py"))


def _ler(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _escrever(caminho, texto):
    pasta = os.path.dirname(os.path.abspath(caminho))
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)


def _ausente(v):
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip() in AUSENTES or v.strip().upper() in AUSENTES
    return False


def identidade_do_repo(repo):
    """Identidade do CIC-1 (fonte_sha + dll_sha). Fail-closed: sem ela, nada OK."""
    ciclo = _ciclo()
    if ciclo is None:
        return {}, "orquestrador CIC-1 (ciclo.py) indisponivel: sem identidade, nada vira OK"
    try:
        ident = ciclo.identidade(repo)
    except Exception as erro:
        return {}, "identidade indisponivel (%s: %s)" % (type(erro).__name__, erro)
    if not isinstance(ident, dict):
        return {}, "identidade em formato inesperado"
    return dict(ident), None


def _criterio(cid, mod, estado, classe, procedencia, esperado, observado, motivo,
              evidencia=None, extra=None):
    c = {
        "id": cid, "mod": mod, "estado": estado, "classe": classe,
        "procedencia": procedencia, "esperado": esperado, "observado": observado,
        "evidencia": list(evidencia or []), "motivo": motivo, "tarefa_origem": TAREFA,
    }
    if extra:
        c.update(extra)
    return c


def _cadeia(obs, identidade):
    """Cadeia de prova de runtime: a OBSERVACAO tem de declarar sessao/fonte/DLL.

    A identidade da rodada NAO preenche a cadeia (seria a prova se auto-assinar):
    ela serve para CONFRONTAR. Falta de sessao/hash => a observacao nao identifica a
    build medida; hash declarado que DIVERGE da identidade => bytes de outra rodada.
    """
    ident = identidade if isinstance(identidade, dict) else {}
    sessao = obs.get("sessao")
    fonte = obs.get("fontes_sha") or obs.get("fonte_sha") or obs.get("hash_fonte_repo")
    # `hash_fonte`/`hash_dll` do coletor CIC-5 sao o sha da DLL do probe (alias do CIC-3/4).
    dll = obs.get("dll_sha") or obs.get("hash_dll") or obs.get("hash_fonte")
    faltando = [n for n, v in (("sessao", sessao), ("fonte_sha", fonte), ("dll_sha", dll))
                if not str(v or "").strip()]
    divergentes = []
    if ident.get("sessao") and sessao != ident["sessao"]:
        divergentes.append("sessao diverge da identidade")
    for nome, declarado, conhecido in (
            ("fonte_sha", fonte, ident.get("fonte_sha")),
            ("dll_sha", dll, ident.get("dll_sha"))):
        if str(declarado or "").strip() and str(conhecido or "").strip() \
                and str(declarado) != str(conhecido):
            divergentes.append("%s declarado (%s...) difere da identidade (%s...)"
                               % (nome, str(declarado)[:12], str(conhecido)[:12]))
    return faltando, divergentes, {"sessao": sessao, "fonte_sha": fonte, "dll_sha": dll}


def _fecha(estado, obs, identidade):
    """(estado_final, prova_runtime, problema). Fixture NUNCA vira OK."""
    proc = _procedencia(obs)
    if obs.get("rotulo_fixture") is True or obs.get("evidencia_runtime") is False:
        proc = "fixture"
    if proc == "fixture":
        if estado == REPROVADO:
            return REPROVADO, False, None
        return (NAO_EXERCITADO, False,
                "procedencia fixture: testa o AVALIADOR, nao comprova runtime")
    if proc == "runtime":
        faltando, divergentes, _ = _cadeia(obs, identidade)
        if divergentes:
            return (INDETERMINADO, False, "; ".join(divergentes))
        if faltando and estado == OK:
            return (NAO_EXERCITADO, False,
                    "cadeia de prova runtime incompleta (%s): nunca OK por rotulo"
                    % ", ".join(faltando))
        if estado == OK and (not ident_suficiente(identidade) or not _vinculo_obs(obs)):
            return NAO_EXERCITADO, False, "identidade/evidencia de bytes vinculada a observacao ausente"
        return estado, estado == OK, None
    return NAO_EXERCITADO, False, "procedencia nao runtime"


def _evidencia_obs(obs):
    """Caminhos de evidencia que a PROPRIA observacao declara (so os que existem)."""
    brutos = []
    for chave in ("evidencia", "evidencias"):
        v = obs.get(chave)
        if isinstance(v, str):
            brutos.append(v)
        elif isinstance(v, list):
            for x in v:
                brutos.append(x if isinstance(x, str) else (x or {}).get("caminho"))
    for chave in ("arquivo", "caminho_do_json", "aut4probe"):
        v = obs.get(chave)
        if isinstance(v, str):
            brutos.append(v)
    return _evs(*[b for b in brutos if b])


def _com_extra(c, obs, identidade, prova, **campos):
    """Injeta a cadeia de prova + extras e avisa se a cadeia ficou incompleta."""
    faltando, divergentes, cadeia = _cadeia(obs, identidade)
    c.update(cadeia)
    c["prova_runtime"] = bool(prova)
    c.update(campos)
    avisos = list(faltando and ["faltando: " + ", ".join(faltando)] or []) + divergentes
    if avisos and c.get("estado") == OK:
        c["motivo"] = str(c.get("motivo", "")) + " | cadeia de prova: " + "; ".join(avisos)
    return c


def ident_suficiente(ident):
    return all(re.fullmatch(r"[0-9a-fA-F]{64}", str(ident.get(k) or "")) for k in ("fonte_sha", "dll_sha"))


def _vinculo_obs(obs):
    def limpo(o):
        return {k: v for k, v in o.items() if k not in ("evidencia", "evidencias", "arquivo", "caminho_do_json", "aut4probe")}
    def contem(v):
        if isinstance(v, dict):
            if limpo(v) == limpo(obs): return True
            return any(contem(x) for x in v.values())
        return isinstance(v, list) and any(contem(x) for x in v)
    brutos = obs.get("evidencia") or obs.get("evidencias") or []
    if not isinstance(brutos, list): brutos = [brutos]
    for e in brutos:
        if not isinstance(e, dict) or not e.get("sha256"): continue
        path = e.get("caminho")
        try:
            if _sha256(path) != e["sha256"]: continue
            texto = _ler(path)
            if obs.get("log") and texto == obs.get("log_texto") and e.get("sessao") == obs.get("sessao"):
                return True
            if contem(json.loads(texto)): return True
        except (OSError, ValueError, TypeError): pass
    return False


# ------------------------------------- cobertura da fotografia (achado A6 / COR-AUT7-F2)
# A fotografia tem de ser SUPERCONJUNTO das ENTRADAS que a suite LE. Na primeira rodada da
# COR-AUT7-F2 ela cobria os 4 mods MEDIDOS + `tools/testes` + `tools/automacao/estilo` +
# `tools/*.py` (+ dist/zip e bin/ como artefatos), e por isso um defeito plantado numa ENTRADA
# MEDIDA fora disso - `tools/fixtures/bf-efeito-no-boot.json`, lido por `t_bf_diag_orcamento` -
# mantinha `cache_valido=true` com prova velha e o criterio saia OK/OK_VINCULANTE (parecer
# COR-AUT7-F2, rodada 425). A lista abaixo foi medida com gancho de auditoria (`sys.addaudithook`
# em `open`/`listdir`/`scandir`/`glob.glob`) sobre a rodada viva das duas suites: 318 arquivos
# lidos sob o repo, todos cobertos pelas raizes/padroes/artefatos declarados aqui.
#
# Mods que a ferramenta MEDE x mods cuja FONTE a suite LE: `BetterTooltips` e
# `RoguelikeSkillTreeVisualizer` nao geram criterio do AUT-7, mas os testes os leem
# (`t_bt10`/`t_bt11`/`t_formato6`/`t_rstv*`), entao a fotografia tem de cobri-los.
MODS_DA_ARVORE = MODS + ("BetterTooltips", "RoguelikeSkillTreeVisualizer")
# Raizes varridas por INTEIRO (arquivo a arquivo): as entradas que a suite le.
# `scratch/` entra porque `t_deploy_optin_repo` varre a ARVORE INTEIRA atras de projetos e
# `regras_formato.py` le o extrato `scratch/rv22/tooltip.cs` quando ele existe.
RAIZES_DA_FOTOGRAFIA = MODS_DA_ARVORE + ("tools", "lib", "docs/cobertura", "ReloadProbe", "scratch")
# Arquivos soltos lidos fora das raizes (`arcabouco.py` usa para achar a raiz do repo).
ARQUIVOS_DA_FOTOGRAFIA = ("docs/PLANO-DE-TESTES.md",)
# Padroes varridos na ARVORE INTEIRA (inclusive fora das raizes): as guardas de projeto
# varrem a raiz atras de `.csproj`/Directory.Build.*, entao um projeto NOVO em qualquer lugar
# muda o resultado da suite.
PADROES_DA_FOTOGRAFIA = ("**/*.csproj", "**/*.props", "**/*.targets")
# Fora da fotografia DE PROPOSITO (enumerado tambem na doc do AUT-7):
#   * `.git`, `.worktrees`, `node_modules`, `.vs`: nao sao entrada de teste;
#   * `bin`, `obj`, `__pycache__`: artefatos DERIVADOS - o bytecode e escrito pela propria
#     rodada (cobri-lo invalidaria a fotografia contra si mesma); as DLLs de `bin/` entram
#     pelo bloco `artefatos`;
#   * `dist/` fora de `*.zip`, `release/`, `NuGet/`: saidas de build/publicacao;
#   * `docs/automacao/**` (inclui `AUT-7-relatorio.md`, `AUT-7-resultado.json` e as pastas de
#     evidencia): SAO SAIDA da propria ferramenta; cobri-las invalidaria o cache a cada
#     regeracao de relatorio.
DIRS_FORA_DA_FOTOGRAFIA = (".git", ".worktrees", "bin", "obj", "__pycache__", "node_modules", ".vs")


def _fotografa_um(raiz, p, arquivos):
    if any(x in p.parts for x in DIRS_FORA_DA_FOTOGRAFIA):
        return
    arquivos[p.relative_to(raiz).as_posix()] = _sha256(p)


def _arquivos_que_a_suite_le(repo):
    """Conjunto de caminhos (com sha256) que a suite LE, declarado por raiz/padrao.

    Conjunto de CAMINHOS, nao so de conteudo: arquivo que ENTRA ou SAI tambem invalida
    (um `.csproj` novo em `scratch/` muda a guarda de deploy; uma fixture apagada muda o
    teste que a le).
    """
    raiz = Path(repo)
    arquivos = {}
    for rel in RAIZES_DA_FOTOGRAFIA:
        base = raiz / rel
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file():
                _fotografa_um(raiz, p, arquivos)
    for rel in ARQUIVOS_DA_FOTOGRAFIA:
        p = raiz / rel
        if p.is_file():
            arquivos[rel] = _sha256(p)
    for padrao in PADROES_DA_FOTOGRAFIA:
        for p in sorted(raiz.glob(padrao)):
            if p.is_file():
                _fotografa_um(raiz, p, arquivos)
    return arquivos


def _artefatos_medidos(repo):
    """Artefatos de BUILD que a suite MEDE, fora da arvore de fonte (achado A6).

    A suite le a DLL do PACOTE (`dist/gumatos-<Mod>-*.zip`, `regras_bct.py:267`) e as DLLs
    de `<Mod>/bin/<config>/` (`candidatos_de_dll`, `regras_bct.py:482-506`;
    `regras_rel.py:95`). Sao artefatos gitignored, entao a varredura de fonte NAO os ve:
    sem eles na fotografia, plantar o defeito da regra de ouro so no pacote (ou so em
    `bin/`) mantinha `cache_valido=true` e a prova velha saia OK/OK_VINCULANTE.

    Nao mede nada aqui: so hasheia o que existe. Artefato que ENTRA ou SAI muda a
    fotografia, como qualquer outra fonte.
    """
    raiz = Path(repo)
    artefatos = {}
    for caminho in sorted(raiz.glob("dist/*.zip")):
        if caminho.is_file():
            artefatos[caminho.relative_to(raiz).as_posix()] = _sha256(caminho)
    for mod in MODS_DA_ARVORE:
        base = raiz / mod / "bin"
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.dll")):
            if p.is_file():
                artefatos[p.relative_to(raiz).as_posix()] = _sha256(p)
    return artefatos


def fotografia_suite(repo):
    raiz = Path(repo)
    return {"arquivos": _arquivos_que_a_suite_le(repo), "artefatos": _artefatos_medidos(repo),
            "raizes": list(RAIZES_DA_FOTOGRAFIA), "arquivos_soltos": list(ARQUIVOS_DA_FOTOGRAFIA),
            "padroes": list(PADROES_DA_FOTOGRAFIA),
            "fora": list(DIRS_FORA_DA_FOTOGRAFIA),
            "comando": [sys.executable, "tools/testes/roda_testes.py", ["--puros", "--contra-prova"], "--json"],
            "python": sys.version}


# ============================================================ MEDICAO OFFLINE ===

def rodar_runner(repo, destino, contra_prova=False, timeout=1800):
    """Roda a SUITE REAL do projeto (runner unico) e grava a saida como evidencia.

    Devolve (exit_code, dados|None, destino, erro). Nao reimplementa nada do
    runner: o que ele imprime e o que vale; saida que nao for JSON = nao mediu.
    """
    flag = "--contra-prova" if contra_prova else "--puros"
    argv = [sys.executable, os.path.join(repo, "tools", "testes", "roda_testes.py"),
            flag, "--json"]
    erro = None
    codigo = None
    saida = ""
    try:
        proc = subprocess.run(argv, cwd=repo, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout)
        saida = proc.stdout.decode("utf-8", "replace")
        erro = (proc.stderr.decode("utf-8", "replace") or "").strip()[:600]
        codigo = proc.returncode
    except Exception as e:
        erro = "%s: %s" % (type(e).__name__, e)
    _escrever(destino, saida)
    try:
        dados = json.loads(saida)
    except ValueError:
        dados = None
    return codigo, dados, destino, erro


def _estado_do_registro(registro):
    """Mapeia (esperado, estado) do runner para o estado do criterio.

    `esperado=passar` -> PASSOU=OK · REPROVOU=REPROVADO · NAO_RODOU=NAO_EXERCITADO.
    `esperado=reprovar` (isca) -> PROVA_OK=OK · PROVA_FALHOU=REPROVADO; uma isca que
    PASSA e defeito do proprio controle negativo (REPROVADO).
    """
    esperado = str(registro.get("esperado") or "passar").strip().lower()
    estado = str(registro.get("estado") or "").strip().upper()
    if esperado.startswith("reprov"):
        return {"PROVA_OK": OK, "PROVA_FALHOU": REPROVADO,
                "PASSOU": REPROVADO, "NAO_RODOU": NAO_EXERCITADO}.get(estado, INDETERMINADO)
    return {"PASSOU": OK, "REPROVOU": REPROVADO,
            "NAO_RODOU": NAO_EXERCITADO}.get(estado, INDETERMINADO)


def _abs_do_teste(dados, registro):
    raiz = str((dados or {}).get("raiz") or "").strip()
    rel = str(registro.get("arquivo") or "").strip()
    return os.path.join(raiz, rel) if (raiz and rel) else None


def _mod_do_arquivo(base):
    for m, prefixo in SUITE_DO_MOD.items():
        if base.startswith(prefixo):
            return m
    for m, prefixo in ISCA_DO_MOD.items():
        if base.startswith(prefixo):
            return m
    return None


def criterios_da_suite(dados, arquivo_json, rotulo):
    """Um criterio por teste do runner, por mod. Roda REAL, evidencia REAL."""
    criterios = []
    for registro in (dados or {}).get("testes", []) or []:
        base = os.path.basename(str(registro.get("arquivo") or ""))
        mod = _mod_do_arquivo(base)
        if mod is None:
            continue
        criterios.append(_criterio(
            "AUT-7/%s/%s/%s" % (mod, rotulo, registro.get("nome") or base), mod,
            _estado_do_registro(registro), "offline", "execucao",
            "esperado=%s (suite do projeto)" % (registro.get("esperado") or "passar"),
            "estado no runner=%s" % registro.get("estado"),
            (registro.get("detalhe") or "saida do runner unico")[:300],
            _evs(arquivo_json, _abs_do_teste(dados, registro))))
    return criterios


def _resumo_por_mod(dados):
    resumo = {}
    for registro in (dados or {}).get("testes", []) or []:
        mod = _mod_do_arquivo(os.path.basename(str(registro.get("arquivo") or "")))
        if mod:
            resumo.setdefault(mod, []).append(
                {"arquivo": os.path.basename(str(registro.get("arquivo"))),
                 "nome": registro.get("nome"), "esperado": registro.get("esperado"),
                 "estado": registro.get("estado")})
    return resumo


def medir_betterstats(repo, evidencia_json):
    """Medicao ESTRUTURAL do BetterStats (nao existe familia `t_bs_*` na suite).

    Le o FONTE vivo com o recorte ESTRUTURAL do projeto e verifica o contratado do
    BS-1/BS-1a: base PURA do `SavedMap`, final do motor, formato `base (final)`,
    geometria deslocada UMA vez (idempotente) e falha-segura. NAO e prova de jogo:
    e prova de ESTRUTURA no fonte versionado (mesma natureza das regras_bf/bct).
    """
    rel_src = "BetterStats/Plugin.cs"
    caminho = os.path.join(repo, rel_src)
    rec = _rec()
    detalhe = {"fonte": rel_src, "checks": []}
    if rec is None or not os.path.isfile(caminho):
        return [_criterio(
            "AUT-7/BetterStats/estrutural/indisponivel", "BetterStats", NAO_EXERCITADO,
            "offline", "execucao", "recorte estrutural do BetterStats/Plugin.cs",
            "recorte indisponivel",
            "recorte.py ausente ou BetterStats/Plugin.cs nao encontrado", _evs(caminho))], detalhe

    efetivo = rec.codigo_efetivo(_ler(caminho))

    def corpo(assinatura):
        try:
            return rec.corpo_do_metodo(efetivo, assinatura)
        except Exception:
            return ""

    getbase = corpo("internal static float GetBaseValue(")
    post_inv = corpo("private static void Postfix(InventoryManager __instance, Character character)")
    post_rog = corpo("private static void Postfix(RoguelikeManager __instance)")
    shift = corpo("private static void ShiftValuesColumn(")
    build = corpo("internal static string BuildInventoryValue(")

    escrita_no_personagem = _RE_ESCRITA_NO_PERSONAGEM.findall(efetivo)

    def tem(texto, *marcas):
        return bool(texto) and all(m in texto for m in marcas)

    checks = (
        ("base-do-savedmap",
         "a base exibida sai do valor PURO do personagem (`character.SavedMap[baseAttr.Guid]`), "
         "com fallback declarado para o valor do motor",
         tem(getbase, "SavedMap", "ContainsKey(baseAttr.Guid)", "SavedMap[baseAttr.Guid]")
         and "character[baseAttr.name]" in getbase),
        ("final-do-motor",
         "o valor COMBINADO sai da lista FINAL do motor "
         "(`LevelableCharacterAttributesFinal` + `character[finalAttrs[i].name]`), com o par "
         "base em `LevelableCharacterAttributes`",
         tem(post_inv, "LevelableCharacterAttributes", "LevelableCharacterAttributesFinal",
             "character[finalAttrs[i].name]")
         and tem(post_rog, "LevelableCharacterAttributesFinal", "character[finalAttrs[i].name]")),
        ("sem-gameplay",
         "o mod NAO escreve em atributo/`SavedMap` do personagem (so reescreve o texto exibido)",
         not escrita_no_personagem and "SetAttribute" not in efetivo
         and "AddAttribute" not in efetivo),
        ("geometria-deslocada-uma-vez",
         "a coluna de valores e deslocada UMA vez (guarda `_shiftedValues`); deslocar a cada "
         "quadro acumularia e jogaria o texto para fora do painel",
         tem(shift, "anchoredPosition", "p.x - 40f", "_shiftedValues")
         and re.search(r"if\s*\(\s*_shiftedValues\s*\)", shift) is not None
         and re.search(r"_shiftedValues\s*=\s*true", shift) is not None),
        ("falha-segura",
         "os dois ganchos sao try/catch e guardam nulo (personagem, holder, StatValues): "
         "o diagnostico nunca derruba a UI",
         tem(post_inv, "try", "catch", "character == null", "AttributesValuesMainHolder == null")
         and tem(post_rog, "try", "catch", "StatValues == null")),
        ("formato-base-combinado",
         "base == combinado mostra SO o base (sem `10 (10)`) e o parentese encolhe pela tag "
         "`<size=` do TMP quando o quadrado e estreito",
         tem(build, "combinedVal == baseVal", "<size=", "FormatBaseCombined")
         and "FormatBaseCombined" in post_rog),
    )
    criterios = []
    for cid, esperado, condicao in checks:
        detalhe["checks"].append({"id": cid, "ok": bool(condicao)})
        criterios.append(_criterio(
            "AUT-7/BetterStats/estrutural/%s" % cid, "BetterStats",
            OK if condicao else REPROVADO, "offline", "execucao", esperado,
            "estrutura encontrada no fonte" if condicao else "estrutura AUSENTE no fonte",
            "recorte estrutural (chaves) do %s" % rel_src, _evs(caminho, evidencia_json)))
    return criterios, detalhe


def defeito_do_betterstats(src, qual):
    """DEFEITO plantado (controle negativo do PROPRIO medidor)."""
    if qual == "base-do-final":
        return src.replace("character.SavedMap[baseAttr.Guid]", "character[baseAttr.name]")
    if qual == "geometria-sem-guarda":
        return src.replace("p.x - 40f", "p.x")
    raise ValueError("defeito desconhecido: %r" % qual)


def medir_offline(repo, out_dir, identidade=None, rodar=True, timeout=1800):
    """Mede os QUATRO mods offline: suite REAL do projeto + estrutura do BetterStats."""
    repo = os.path.abspath(repo)
    os.makedirs(out_dir, exist_ok=True)
    meta = {"esquema": ESQUEMA, "tarefa": TAREFA, "repo": repo, "out_dir": os.path.abspath(out_dir),
            "suites": {}, "fontes": {}, "mods": list(MODS),
            "identidade": {k: v for k, v in (identidade or {}).items()
                           if k in ("fonte_sha", "dll_sha", "dlls")}}
    for mod, rels in FONTES_DO_MOD.items():
        meta["fontes"][mod] = [{"rel": r, "caminho": os.path.abspath(os.path.join(repo, r)),
                                "sha256": (_ev(os.path.join(repo, r)) or {}).get("sha256")}
                               for r in rels]

    json_puros = os.path.join(out_dir, "suite-puros.json")
    json_cp = os.path.join(out_dir, "suite-contra-prova.json")
    snapshot = fotografia_suite(repo)
    # A COBERTURA da fotografia fica registrada no proprio resultado (nao so no codigo): quem
    # le o JSON gerado ve o que invalida o cache e o que fica fora DE PROPOSITO.
    meta["fotografia"] = {
        "raizes": list(RAIZES_DA_FOTOGRAFIA), "arquivos_soltos": list(ARQUIVOS_DA_FOTOGRAFIA),
        "padroes": list(PADROES_DA_FOTOGRAFIA), "fora": list(DIRS_FORA_DA_FOTOGRAFIA),
        "arquivos": len(snapshot.get("arquivos") or {}),
        "artefatos": len(snapshot.get("artefatos") or {}),
        "o_que_fica_fora": ("`bin`/`obj`/`__pycache__` (DERIVADOS: o bytecode e escrito pela propria "
                            "rodada); `dist/*.zip` e `<Mod>/bin/**/*.dll` nao ficam de fora - entram "
                            "no bloco `artefatos`; `docs/automacao/**`, `release/` e `NuGet/` sao "
                            "SAIDA de ferramenta/build, nao entrada de teste"),
        "como_foi_medida": ("gancho de auditoria (`sys.addaudithook` em open/listdir/scandir/glob) "
                            "sobre a rodada viva das duas suites: todo arquivo lido sob o repo esta "
                            "coberto por estas raizes/padroes/artefatos (fora `__pycache__`)")}
    cache_path = os.path.join(out_dir, "suite-vinculo.json")
    if rodar:
        codigo_p, dados_p, _, erro_p = rodar_runner(repo, json_puros, False, timeout)
        codigo_c, dados_c, _, erro_c = rodar_runner(repo, json_cp, True, timeout)
        if fotografia_suite(repo) == snapshot:
            _escrever(cache_path, json.dumps({"fotografia": snapshot, "resultados": {p: _sha256(p) for p in (json_puros, json_cp)}}, sort_keys=True))
        else:
            dados_p = dados_c = None
            erro_p = erro_c = "drift durante suite; nenhuma prova"
    else:
        codigo_p = codigo_c = None
        vinculo = _ler_json_se_existir(cache_path) or {}
        valido = vinculo.get("fotografia") == snapshot and all(
            os.path.isfile(p) and (vinculo.get("resultados") or {}).get(p) == _sha256(p)
            for p in (json_puros, json_cp))
        dados_p = _ler_json_se_existir(json_puros) if valido else None
        dados_c = _ler_json_se_existir(json_cp) if valido else None
        erro_p = erro_c = "cache atual verificado" if valido else "cache ausente/obsoleto: rerodar suite"
        meta["cache_valido"] = valido

    for rotulo, json_path, codigo, dados, erro in (
            ("puros", json_puros, codigo_p, dados_p, erro_p),
            ("contra_prova", json_cp, codigo_c, dados_c, erro_c)):
        meta["suites"][rotulo] = {
            "arquivo": json_path, "exit_runner": codigo, "erro": erro,
            "contagem": (dados or {}).get("contagem"),
            "sha256": (_ev(json_path) or {}).get("sha256")}

    criterios = criterios_da_suite(dados_p, json_puros, "puro")
    criterios += criterios_da_suite(dados_c, json_cp, "controle-negativo")

    por_mod = {}
    for c in criterios:
        por_mod.setdefault(c["mod"], []).append(c)
    for mod in MODS:
        testes = [c for c in por_mod.get(mod, []) if "/puro/" in c["id"]]
        iscas = [c for c in por_mod.get(mod, []) if "/controle-negativo/" in c["id"]]
        if not testes:
            criterios.append(_criterio(
                "AUT-7/%s/suite-ausente" % mod, mod, NAO_EXERCITADO, "offline", "execucao",
                "familia de teste puro do mod na suite do projeto (`%s*`)" % SUITE_DO_MOD[mod],
                "nenhum teste do mod na suite",
                "lacuna TECNICA de medicao offline: sem familia de teste puro na suite, "
                "a prova deste mod tem de vir de outra via"))
        if testes and not iscas:
            criterios.append(_criterio(
                "AUT-7/%s/controle-negativo-ausente" % mod, mod, NAO_EXERCITADO, "offline",
                "execucao", "isca do mod tem de ser MOSTRADA REPROVANDO (`%s*`)" % ISCA_DO_MOD[mod],
                "nenhuma isca do mod rodou",
                "lacuna TECNICA: prova que nunca reprovou nao vale como prova",
                _evs(json_cp, json_puros)))

    crit_bs, detalhe_bs = medir_betterstats(repo, json_puros)
    criterios += crit_bs
    meta["betterstats"] = detalhe_bs
    meta["testes_por_mod"] = _resumo_por_mod(dados_p)
    meta["iscas_por_mod"] = _resumo_por_mod(dados_c)
    return criterios, meta


def _ler_json_se_existir(caminho):
    try:
        return json.loads(_ler(caminho))
    except Exception:
        return None


# ============================================================ AVALIACAO RUNTIME ==
# O que SO o jogo mede. Le o formato REAL do probe AUT-4 (campos planos) e do
# coletor CIC-5 (`campos` normalizado). Nada de campo inventado: o que a coleta
# nao emite sai como LACUNA declarada, com o proximo passo TECNICO nomeado.

def _obs_lista(observacoes):
    if isinstance(observacoes, dict):
        v = observacoes.get("observacoes")
        if isinstance(v, list):
            return [o for o in v if isinstance(o, dict)]
        return [observacoes] if observacoes else []
    if isinstance(observacoes, list):
        return [o for o in observacoes if isinstance(o, dict)]
    return []


def _campo(obs, nome):
    """Le um campo nas DUAS formas reais (probe cru / coletor normalizado)."""
    campos = obs.get("campos")
    if isinstance(campos, dict) and isinstance(campos.get(nome), dict):
        v = campos[nome].get("valor")
        return None if _ausente(v) else v
    v = obs.get(nome)
    return None if _ausente(v) else v


def _procedencia(obs):
    p = str(obs.get("procedencia") or "").strip().lower()
    return p if p in PROCEDENCIAS else "execucao"


def _nome(obs):
    return str(_campo(obs, "objeto") or _campo(obs, "caminho") or "<sem-nome>")


def _hex_do_campo(v):
    """`#RRGGBBAA (r=...)` -> (RRGGBB, alfa|None). Formato do probe AUT-4."""
    if not isinstance(v, str):
        return None, None
    m = re.search(r"#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?", v)
    if not m:
        return None, None
    alfa = int(m.group(2), 16) / 255.0 if m.group(2) else None
    return m.group(1).upper(), alfa


def _controlar_por_mod(obs_list):
    """Agrupa por objeto/caminho as leituras LIGADO/DESLIGADO (marca `mod_ativo`)."""
    pares = {}
    for o in obs_list:
        if _campo(o, "fonte") is None:
            continue
        marca = o.get("mod_ativo")
        desligado = (marca is False) or (isinstance(marca, str)
                                         and marca.strip().lower() in ("false", "desligado", "off"))
        pares.setdefault(_nome(o), {})["desligado" if desligado else "ligado"] = o
    return pares


def _material(o):
    return _campo(o, "propriedades_material")


def _props_completas(o):
    """TODAS as propriedades efetivas do material + keywords de shader, do fonte vivo."""
    bf = _bf_estilo()
    props = {p for grupo in bf.PRECISA_COPIAR.values() for p in grupo}
    mat, kw = _material(o), _campo(o, "shader_keywords")
    if not isinstance(mat, dict) or not props <= set(mat):
        return False
    for nome in props:
        v = mat[nome]
        if nome == "_ClipRect":
            if not (isinstance(v, list) and len(v) == 4 and all(_numero(x) for x in v)):
                return False
        elif nome.endswith("Color"):
            if _hex_do_campo(v)[1] is None:
                return False
        elif not _numero(v):
            return False
    return (isinstance(kw, list) and bool(kw)
            and all(isinstance(k, str) and k.strip() for k in kw)
            and all(type((_campo(o, "keywords") or {}).get(k)) is bool for k in bf.PRECISA_LIGAR))


def _numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _cor_completa(o):
    """Cor da LETRA e da sombra/contorno com hex COMPLETO (e alfa quando houver)."""
    cores = _campo(o, "cores")
    if not isinstance(cores, dict):
        return False
    if _hex_do_campo(cores.get("texto"))[0] is None:
        return False
    alvo = _hex_do_campo(cores.get("sombra"))[0] or _hex_do_campo(cores.get("contorno"))[0]
    if alvo is None:
        return False
    return all(type((_campo(o, "keywords") or {}).get(k)) is bool
               for k in _bf_estilo().PRECISA_LIGAR)


def _estilo_completo(o):
    """Controle de ESTILO completo: material efetivo + cores + keywords (regra do BF)."""
    cores = _campo(o, "cores")
    return (_props_completas(o) and _cor_completa(o)
            and isinstance(cores, dict)
            and all(_hex_do_campo(cores.get(k))[0] is not None
                    for k in ("texto", "face", "contorno", "sombra")))


def _resultado_grupo(cid, mod, esperado, observacoes, identidade, erros=(), lacunas=(), extra=None):
    obs = observacoes[0] if observacoes else {}
    evidencia = [ev for o in observacoes for ev in _evidencia_obs(o)]
    estado = REPROVADO if erros else NAO_EXERCITADO if lacunas or not observacoes else OK
    problemas = list(lacunas)
    if estado == OK:
        for o in observacoes:
            e, prova, problema = _fecha(OK, o, identidade)
            if e != OK:
                estado = INDETERMINADO if e == INDETERMINADO else NAO_EXERCITADO
                problemas.append(problema or "controle sem prova")
    motivo = "; ".join(list(erros) + problemas) or "todos os controles completos confrontados"
    c = _criterio(cid, mod, estado, "runtime", _procedencia(obs), esperado,
                  {"objetos": [_nome(o) for o in observacoes], "erros": list(erros), "lacunas": problemas},
                  motivo, evidencia, extra)
    if estado != OK:
        c.update(lacuna_probe=motivo, tipo_pendencia="coleta_tecnica", autorizacao_necessaria=False)
    return [_com_extra(c, obs, identidade, estado == OK)]


def _asp_betterfont(cid, mod, obs_list, identidade):
    leituras = [o for o in obs_list if _campo(o, "fonte") is not None]
    grupos = {}
    erros, lacunas = [], []
    for o in leituras:
        grupos.setdefault(_nome(o), []).append(o)
        if type(o.get("mod_ativo")) is not bool or not _estilo_completo(o):
            lacunas.append(_nome(o) + ": controle/material efetivo/keywords completos ausentes")
    for nome, os in grupos.items():
        lig = [o for o in os if o.get("mod_ativo") is True]
        des = [o for o in os if o.get("mod_ativo") is False]
        if len(lig) != 1 or len(des) != 1:
            lacunas.append(nome + ": controle ligado/desligado ausente ou ambiguo")
            continue
        l, d = lig[0], des[0]
        if _campo(l, "fonte") == _campo(d, "fonte"):
            erros.append(nome + ": fonte nao trocou")
        for campo in ("cores", "keywords", "propriedades_material", "shader_keywords"):
            vl, vd = _campo(l, campo), _campo(d, campo)
            if isinstance(vl, dict) and isinstance(vd, dict):
                # Conjunto COMPLETO dos dois lados (achado A1): comparar so a INTERSECCAO
                # deixava chave que existe de um lado so sem nenhuma medicao.
                so_um_lado = sorted(set(vl) ^ set(vd))
                if so_um_lado:
                    erros.append(nome + ": " + campo + " com chave de um lado so: "
                                 + ", ".join(so_um_lado))
                if any(vl[k] != vd[k] for k in set(vl) & set(vd)):
                    erros.append(nome + ": " + campo + " mudou")
            elif vl is not None and vd is not None and vl != vd:
                erros.append(nome + ": " + campo + " mudou")
        if l.get("sessao") != d.get("sessao"):
            lacunas.append(nome + ": controles de sessoes distintas")
    if not leituras:
        lacunas.append("controle ligado/desligado no mesmo objeto ausente")
    return _resultado_grupo(cid, mod, "fonte trocada preservando TODAS propriedades efetivas e keywords",
                            leituras, identidade, erros, lacunas)


def _asp_betterfont_config(cid, mod, obs_list, identidade):
    leituras = [o for o in obs_list if _campo(o, "config") or o.get("config_sha")]
    erros, lacunas = [], []
    bf = _bf_estilo()
    defaults = bf.defaults_com_linha(_ler(os.path.join(RAIZ, "BetterFont", "Plugin.cs")))
    # Hashes de config que a IDENTIDADE da rodada declara (via `--identidade`, sem depender
    # do CIC-1). Achado A2: a identidade do CIC-1 traz so fonte_sha/dll_sha/dlls; exigir o
    # hash DENTRO dela tornava o criterio insatisfazivel e REPROVAVA config legitimo.
    hashes_ident = _hashes_config(identidade)
    for o in leituras:
        cfg = _campo(o, "config")
        if not isinstance(cfg, dict) or not isinstance(cfg.get("valores"), dict):
            lacunas.append("config sem chaves/valores lidos")
            continue
        caminho = cfg.get("caminho")
        sha = o.get("config_sha") or cfg.get("sha256")
        if not caminho or not os.path.isfile(caminho) or not sha:
            lacunas.append("arquivo/hash config ausente")
            continue
        if _sha256(caminho) != sha:
            erros.append("config: os bytes do arquivo nao batem com o sha declarado")
        elif not hashes_ident:
            lacunas.append("config: a identidade da rodada nao declara hash de config - bytes "
                           "conferidos, mas sem procedencia declarada o criterio nao fecha OK "
                           "(anexar `config_sha` na identidade do `--identidade`)")
        elif sha not in hashes_ident:
            erros.append("config: sha declarado difere do hash de config da identidade da rodada")
        cp = configparser.ConfigParser(); cp.optionxform = str
        cp.read(caminho, encoding="utf-8-sig")
        for chave, meta in defaults.items():
            valores = [cp[sec][chave].strip().lower() for sec in cp.sections() if chave in cp[sec]]
            declarado = cfg["valores"].get(chave)
            if len(valores) != 1 or type(declarado) is not bool:
                lacunas.append("config chave ausente/ambigua: " + chave)
            elif valores[0] not in ("true", "false") or declarado != (valores[0] == "true"):
                erros.append("config valor difere do arquivo: " + chave)
            elif declarado != meta["valor"]:
                erros.append("config diverge do default contratado: " + chave)
    if not leituras:
        lacunas.append("config/chaves/valores ausentes")
    return _resultado_grupo(cid, mod, "config real: bytes, identidade, chaves e defaults confrontados",
                            leituras, identidade, erros, lacunas, {"config_relevante": True,
                            "config_sha": (leituras[0].get("config_sha") if leituras else None)})


def _hashes_config(identidade):
    achados = set()
    def visitar(v):
        if isinstance(v, dict):
            for k, x in v.items():
                if k in ("sha256", "config_sha", "hash_config") and isinstance(x, str):
                    achados.add(x)
                elif isinstance(x, (list, dict)):
                    visitar(x)
        elif isinstance(v, list):
            for x in v: visitar(x)
    visitar({k: v for k, v in identidade.items() if "config" in k})
    return achados


def _asp_betterfont_visual(cid, mod, obs_list, identidade):
    """BetterFont: aceite VISUAL da fonte (alteracao de UI exige revisao de design)."""
    instrucao = ("Abrir o jogo com o BetterFont ativo e conferir, em tooltip, texto de combate "
                 "e UI, se a fonte ficou legivel e sem corte; registrar o aceite.")
    return [_criterio(
        cid, mod, NAO_EXERCITADO, "runtime", "runtime",
        "em jogo: a fonte aplicada e legivel e coerente com a UI (hierarquia, tamanho, "
        "entrelinha) e nenhuma tela ficou com texto cortado",
        "julgamento humano ainda nao pronunciado",
        "o DoD exige revisao de UI/UX para alteracao de fonte: o dado tecnico nao substitui "
        "o olho no jogo",
        None, {"tipo_pendencia": "julgamento_visual", "autorizacao_necessaria": True,
               "julgamento_humano": instrucao, "instrucoes_humanas": instrucao})]


def _superficies_no_alvo(alvo, superficies):
    """Superficies canonicas presentes no alvo por TOKEN, nunca por substring (achado A3).

    `sup = SUPERFICIES_DO_BCT` traz `Healthbar` e `BossHealthbar`; casar por substring
    (`s.lower() in alvo`) fazia `Healthbar` ser dada como medida sempre que a leitura era de
    `BossHealthbar`, e 6 leituras marcavam as 7 superficies -> OK/OK_VINCULANTE sem NENHUMA
    medicao da superficie de verdade. O casamento exige fronteira de token dos dois lados
    (o alvo real costuma vir como `BossHealthbar_Text`, com `_` como separador).
    """
    texto = str(alvo or "").lower()
    return [s for s in superficies
            if re.search(r"(?<![0-9a-z])" + re.escape(str(s).lower()) + r"(?![0-9a-z])", texto)]


def _asp_bettercombat_text(cid, mod, obs_list, identidade):
    bct = _bct()
    sup = list(bct.SUPERFICIES_DO_BCT)
    leituras, achadas, erros, lacunas = [], set(), [], []
    for o in obs_list:
        alvo = _nome(o) + " " + str(_campo(o, "componente") or "")
        superficies = _superficies_no_alvo(alvo, sup)
        if not superficies: continue
        leituras.append(o); achadas.update(superficies)
        cores, kw = _campo(o, "cores") or {}, _campo(o, "keywords") or {}
        letra, a = _hex_do_campo(cores.get("texto"))
        sombra, alfa = _hex_do_campo(cores.get("sombra") or cores.get("contorno"))
        if letra is None or sombra is None or a is None or alfa is None or type(kw.get("OUTLINE_ON")) is not bool:
            lacunas.append(_nome(o) + ": cores/alfa/keywords ausentes")
            continue
        if not kw["OUTLINE_ON"] or sombra != str(bct.sombra_para(letra)).upper().lstrip("#"):
            erros.append(_nome(o) + ": sombra/polaridade incorreta")
        if bct.contraste_com_a_letra(letra, sombra) < bct.CONTRASTE_MINIMO or alfa < bct.ALFA_SOMBRA_MINIMA:
            erros.append(_nome(o) + ": contraste/alfa insuficiente")
    if set(sup) - achadas:
        lacunas.append("superficies canonicas ausentes: " + ", ".join(sorted(set(sup) - achadas)))
    return _resultado_grupo(cid, mod, "todas superficies canonicas com cor/alfa/contraste/polaridade",
                            leituras, identidade, erros, lacunas, {"superficies_medidas": sorted(achadas)})


def _asp_bct_idempotencia(cid, mod, obs_list, identidade):
    sup = _bct().SUPERFICIES_DO_BCT
    grupos = {}
    erros, lacunas = [], []
    for o in obs_list:
        if _superficies_no_alvo(_nome(o), sup):
            grupos.setdefault(_nome(o), []).append(o)
    leituras = [o for os in grupos.values() for o in os]
    for nome, os in grupos.items():
        if len(os) < 2 or len({o.get("estagio") for o in os}) < 2:
            lacunas.append(nome + ": duas aplicacoes/releituras independentes ausentes")
        for chave in ("leitura_id", "evento_id", "timestamp"):
            if any(not o.get(chave) for o in os) or len({o.get(chave) for o in os}) != len(os):
                lacunas.append(nome + ": identidade independente ausente/duplicada " + chave)
        if len({o.get("sessao") for o in os}) != 1:
            lacunas.append(nome + ": sessoes distintas")
        if any(not _cor_completa(o) for o in os):
            lacunas.append(nome + ": cor/sombra/keywords incompletos")
        valores = {json.dumps([_campo(o, "cores"), _campo(o, "keywords"), _material(o)], sort_keys=True) for o in os}
        if len(valores) > 1:
            erros.append(nome + ": efeito mudou entre leituras")
    if not grupos: lacunas.append("nenhum alvo BCT relido")
    return _resultado_grupo(cid, mod, "mesmo objeto/sessao; estagios/eventos/leituras distintos e efeito estavel",
                            leituras, identidade, erros, lacunas)


def _asp_bct_sem_vazamento_levelup(cid, mod, obs_list, identidade):
    tipos = list(_bct().TIPOS_DO_LEVELUP)
    leituras = [o for o in obs_list if o.get("nao_deve_exibir_efeito") is True]
    erros, lacunas, achados = [], [], set()
    for o in leituras:
        tipo = o.get("tipo_levelup")
        if o.get("contexto") != "level-up" or tipo not in tipos or not any(x in _nome(o) for x in ("Title", "Description")):
            lacunas.append(_nome(o) + ": contexto/alvo level-up nao comprovado")
        else: achados.add(tipo)
        controle = o.get("controle_nativo")
        if not (_props_completas(o) and _cor_completa(o)) \
                or not isinstance(controle, dict) \
                or not (_props_completas(controle) and _cor_completa(controle)):
            lacunas.append(_nome(o) + ": material/controle nativo incompleto")
            continue
        leituras_controle = _fecha(OK, controle, identidade)
        if leituras_controle[0] != OK:
            lacunas.append(_nome(o) + ": controle nativo sem prova: " + str(leituras_controle[2]))
        if _nome(o) != _nome(controle) or o.get("sessao") != controle.get("sessao") or controle.get("mod_ativo") is not False:
            lacunas.append(_nome(o) + ": controle de outro alvo/sessao ou BCT ativo")
        for campo in ("cores", "keywords", "shader_keywords", "propriedades_material"):
            if _campo(o, campo) != _campo(controle, campo):
                erros.append(_nome(o) + ": efeito difere do estilo nativo: " + campo)
    if set(tipos) - achados: lacunas.append("tipos level-up ausentes: " + ", ".join(sorted(set(tipos) - achados)))
    return _resultado_grupo(cid, mod, "level-up real: todos tipos e alvos comparados ao estilo nativo desligado",
                            leituras, identidade, erros, lacunas, {"tipos_do_levelup": tipos})


def _asp_betterstats_base_final(cid, mod, obs_list, identidade):
    """BetterStats: base PURA x valor FINAL do motor (o texto exibido tem de bater)."""
    esperado = ("na ficha/level-up o texto sai `base (final)`, com a base do valor PURO "
                "investido e o final do motor; `character[nome]` NAO serve como base")
    painel = [o for o in obs_list
              if _campo(o, "texto_renderizado")
              and re.search(r"\d+\s*\(\s*\d+\s*\)", str(_campo(o, "texto_renderizado")))]
    if not painel:
        return [_criterio(
            cid, mod, NAO_EXERCITADO, "runtime", "runtime", esperado,
            "nenhum texto `base (final)` nas observacoes",
            "lacuna TECNICA dupla: (a) a rodada runtime nao foi autorizada e (b) o probe nao "
            "emite os valores de atributo do personagem (SavedMap x final), sem os quais o "
            "texto exibido nao pode ser confrontado com a fonte do numero",
            None, {"lacuna_probe": "valores de atributo do personagem (SavedMap + final) por "
                                   "atributo, para confrontar com o texto medido",
                   "tipo_pendencia": "coleta_tecnica", "autorizacao_necessaria": False})]
    obs = painel[0]
    return [_criterio(
        cid, mod, INDETERMINADO, "runtime", _procedencia(obs), esperado,
        str(_campo(obs, "texto_renderizado"))[:200],
        "texto `base (final)` encontrado, mas SEM os valores de atributo do personagem na "
        "coleta nao da para provar que a base e o PURO do SavedMap (e nao a copia do motor)",
        _evidencia_obs(obs), {"tipo_pendencia": "coleta_tecnica", "autorizacao_necessaria": False,
                              "lacuna_probe": "valores de atributo do personagem por atributo"})]


def _asp_betterstats_geometria(cid, mod, obs_list, identidade):
    """BetterStats: a coluna de valores NAO pode vazar do painel (geometria)."""
    esperado = ("a caixa do texto de valores cabe DENTRO do painel de atributos (sem "
                "clipping/saida lateral), com deslocamento unico e nao acumulado")
    com_geo = [o for o in obs_list if _campo(o, "geometria")]
    if not com_geo:
        return [_criterio(
            cid, mod, NAO_EXERCITADO, "runtime", "runtime", esperado,
            "nenhuma observacao com `geometria`",
            "lacuna TECNICA: o probe emite a caixa do TEXTO (`caixa_na_tela_px` + `tela`), mas "
            "NAO a caixa do PAINEL de atributos - sem a do painel nao ha contra o que comparar",
            None, {"lacuna_probe": "caixa (bbox) do painel de atributos, alem da do texto",
                   "tipo_pendencia": "coleta_tecnica", "autorizacao_necessaria": False})]
    obs = com_geo[0]
    geo = _campo(obs, "geometria") or {}
    caixa = geo.get("caixa_na_tela_px") or {}
    return [_criterio(
        cid, mod, INDETERMINADO, "runtime", _procedencia(obs), esperado,
        "caixa do texto=%s tela=%s" % (json.dumps(caixa, ensure_ascii=False), geo.get("tela")),
        "ha geometria do TEXTO, mas falta a do PAINEL: sem ela o clipping nao pode ser provado "
        "(nem negado) por dado",
        _evidencia_obs(obs), {"tipo_pendencia": "coleta_tecnica", "autorizacao_necessaria": False,
                              "lacuna_probe": "bbox do painel de atributos"})]


def _asp_betterstats_visual(cid, mod, obs_list, identidade):
    """BetterStats: aceite VISUAL do layout (BS-1a aguarda validacao visual)."""
    instrucao = ("Com o BetterStats ativo, abrir a ficha de personagem (painel Attributes) e a "
                 "tela de level-up: conferir que `base (final)` cabe no painel, sem vazar a "
                 "borda e sem quebra de linha.")
    return [_criterio(
        cid, mod, NAO_EXERCITADO, "runtime", "runtime",
        "em jogo: a coluna de valores cabe no painel nas DUAS telas (ficha e level-up)",
        "julgamento humano ainda nao pronunciado (BS-1a aguarda validacao visual)",
        "so a estrutura foi medida offline; numeros/geometria runtime seguem nao comprovados; aceite visual separado",
        None, {"tipo_pendencia": "julgamento_visual", "autorizacao_necessaria": True,
               "julgamento_humano": instrucao, "instrucoes_humanas": instrucao})]


def _asp_debugger_dump(cid, mod, obs_list, identidade):
    """Debugger: contrato/saneamento do dump medido no LOG de um boot novo."""
    esperado = ("no LogOutput.log do MESMO boot: as linhas do dump saem com `desc=` por ULTIMO, "
                "sem `|` e sem quebra de linha no valor")
    logs = [o for o in obs_list if o.get("log") and o.get("boot_novo") is True]
    if not logs:
        return [_criterio(
            cid, mod, NAO_EXERCITADO, "runtime", "runtime", esperado,
            "nenhum log de boot NOVO com a DLL atual",
            "rodada runtime ainda nao autorizada: log de sessao anterior NAO prova os bytes "
            "atuais (precedente AUT-4R: log velho nao assina fonte nova). O contrato e o "
            "saneamento ja tem prova ESTRUTURAL na suite pura (t_debugger_*)",
            None, {"tipo_pendencia": "autorizacao", "autorizacao_necessaria": True,
                   "lacuna_probe": "LogOutput.log de um boot com a DLL atual (sessao + hash)",
                   "instrucoes_humanas": (
                       "Autorizar UMA rodada de boot com os mods atuais (SEM carregar save): "
                       "abrir o jogo ate o menu com o RoguelikeDebugger ativo e encerrar; o "
                       "LogOutput.log dessa sessao e a evidencia.")})]
    regras = _modulo("aut7_regras_debugger", os.path.join(TESTES, "regras_debugger.py"))
    censo = regras.carrega_censo()
    erros, lacunas, categorias = [], [], set()
    for obs in logs:
        reconhecidas = 0
        for linha in str(obs.get("log_texto") or "").splitlines():
            if censo.LINE.match(linha):
                reconhecidas += 1
                cat, nome, campos, desc, falhas = regras.confere_linha(censo, linha)
                categorias.add(cat)
                erros.extend(falhas + regras.contrato_da_linha(censo, linha))
                if desc is not None and "|" in desc: erros.append("pipe dentro do valor desc")
                # LIMITE DECLARADO (achado A4): o `|` DENTRO de um valor so e detectavel quando
                # vem COLADO ao valor (`FIELD = [^|]+` trunca em silencio). No formato que o
                # produto usa (" | " como separador), um valor com " | " dentro NAO e detectado
                # aqui - `contrato_da_linha` devolve [] e a linha passa por valida.
                colunas = censo.CATS.get(cat, (None, []))[1]
                # So as colunas que o parser do censo REALMENTE le do log (as derivadas -
                # `arvore`/`status` - nao saem da linha) e `descricao` que casa com `desc`.
                lidas = set(regras.chaves_do_field(censo)) | {"descricao"}
                faltam = (set(colunas) & set(regras.chaves_do_field(censo))) - set(campos)
                if faltam: lacunas.append("colunas ausentes: " + ", ".join(sorted(faltam)))
            elif "desc=" in linha:
                erros.append("linha declarada dump nao reconhecida pelo parser real")
        if not reconhecidas: lacunas.append("log vazio/sem linhas reconhecidas")
    if set(censo.CATS) - categorias:
        lacunas.append("categorias canonicas ausentes: " + ", ".join(sorted(set(censo.CATS) - categorias)))
    return _resultado_grupo(cid, mod, esperado, logs, identidade, erros, lacunas,
                            {"boot_novo": True, "categorias_reconhecidas": sorted(categorias)})


def _asp_debugger_censo(cid, mod, obs_list, identidade):
    """Debugger: censo lido do dump do boot (categorias/colunas sao contrato)."""
    esperado = ("as categorias e colunas do censo saem do dump do boot atual (nenhum campo "
                "desaparece); o censo NAO e regenerado aqui (escreve doc curada)")
    obs_log = [o for o in obs_list if o.get("log") and o.get("boot_novo") is True]
    if not obs_log:
        return [_criterio(
            cid, mod, NAO_EXERCITADO, "runtime", "runtime", esperado,
            "nenhum dump de boot novo para ler o censo",
            "rodada runtime ainda nao autorizada (mesmo log do boot do criterio de contrato); "
            "o `census.py` NAO e executado nesta frente porque reescreve doc curada",
            None, {"tipo_pendencia": "autorizacao", "autorizacao_necessaria": True,
                   "lacuna_probe": "dump do boot atual para conferir categorias/colunas do censo"})]
    obs = obs_log[0]
    return [_criterio(
        cid, mod, INDETERMINADO, "runtime", _procedencia(obs), esperado,
        "ha log de boot, mas a conferencia das CATEGORIAS/COLUNAS do censo exige regenerar o "
        "censo (escreve doc curada) - fora do escopo desta frente",
        "o dado do dump existe; a conferencia de censo e um passo separado e autorizado",
        _evidencia_obs(obs), {"tipo_pendencia": "coleta_tecnica", "autorizacao_necessaria": False})]


# (id, mod, avaliador). Cada avaliador devolve LISTA de criterios.
_ASPECTOS = (
    ("AUT-7/BetterFont/runtime-preservacao-estilo", "BetterFont", _asp_betterfont),
    ("AUT-7/BetterFont/runtime-config", "BetterFont", _asp_betterfont_config),
    ("AUT-7/BetterFont/runtime-visual", "BetterFont", _asp_betterfont_visual),
    ("AUT-7/BetterCombatText/runtime-superficies-contraste", "BetterCombatText",
     _asp_bettercombat_text),
    ("AUT-7/BetterCombatText/runtime-idempotencia", "BetterCombatText", _asp_bct_idempotencia),
    ("AUT-7/BetterCombatText/runtime-sem-vazamento-levelup", "BetterCombatText",
     _asp_bct_sem_vazamento_levelup),
    ("AUT-7/BetterStats/runtime-base-vs-final", "BetterStats", _asp_betterstats_base_final),
    ("AUT-7/BetterStats/runtime-geometria", "BetterStats", _asp_betterstats_geometria),
    ("AUT-7/BetterStats/runtime-visual", "BetterStats", _asp_betterstats_visual),
    ("AUT-7/RoguelikeDebugger/runtime-contrato-dump", "RoguelikeDebugger", _asp_debugger_dump),
    ("AUT-7/RoguelikeDebugger/runtime-censo", "RoguelikeDebugger", _asp_debugger_censo),
)


def avaliar(observacoes, identidade=None):
    """Contrato do ciclo: criterios de RUNTIME das observacoes + identidade.

    Nunca levanta por dado ausente/malformado: o aspecto inteiro vira INDETERMINADO
    com o id canonico preservado. Sem identidade suficiente NADA sai OK.
    """
    obs = _obs_lista(observacoes)
    ident = identidade if isinstance(identidade, dict) else {}
    criterios = []
    for cid, mod, fn in _ASPECTOS:
        try:
            itens = fn(cid, mod, obs, ident)
            criterios += [c for c in (itens or []) if isinstance(c, dict)]
        except Exception as erro:
            criterios.append(_criterio(
                cid, mod, INDETERMINADO, "runtime", "execucao", "avaliar sem excecao",
                "erro ao avaliar: %s: %s" % (type(erro).__name__, erro),
                "observacao malformada derrubou o aspecto (id canonico preservado)", None,
                {"lacuna_probe": "observacao malformada", "tipo_pendencia": "coleta_tecnica"}))
    return criterios


def validar_plano_aut4(caminho_plano):
    """Prova OFFLINE de que o plano de coleta do AUT-7 e consumivel pelo coletor AUT-4."""
    coletor = _coletor()
    if coletor is None:
        return {"ok": False, "motivo": "coletor AUT-4 (tools/automacao/runtime/coletor.py) "
                                       "indisponivel"}
    try:
        plano = json.loads(_ler(caminho_plano))
    except Exception as erro:
        return {"ok": False, "motivo": "plano ilegivel: %s" % erro}
    try:
        validado = coletor.validar_plano(plano)
        rodada, codigo = coletor.planejar_rodada(validado, autorizado=False, jogo_disponivel=False)
    except Exception as erro:
        return {"ok": False, "motivo": "plano recusado pelo contrato do AUT-4: %s: %s"
                                       % (type(erro).__name__, erro)}
    return {"ok": True, "esquema": validado.get("esquema"),
            "cenarios": [c.get("nome") for c in validado.get("cenarios", [])],
            "status_da_rodada_sem_autorizacao": (rodada.get("resultado") or {}).get("status"),
            "exit_code": codigo, "arquivo": os.path.abspath(caminho_plano)}


# --------------------------------------------------------------------- resumo ---

def resumir(criterios, identidade=None, medicao=None):
    contagem = {OK: 0, REPROVADO: 0, NAO_EXERCITADO: 0, INDETERMINADO: 0}
    por_mod = {}
    for c in criterios or []:
        e = c.get("estado", INDETERMINADO)
        contagem[e] = contagem.get(e, 0) + 1
        b = por_mod.setdefault(c.get("mod", "transversal"),
                               {OK: 0, REPROVADO: 0, NAO_EXERCITADO: 0, INDETERMINADO: 0})
        b[e] = b.get(e, 0) + 1
    ident = identidade if isinstance(identidade, dict) else {}
    return {
        "esquema": ESQUEMA, "tarefa": TAREFA,
        "identidade": {"fonte_sha": ident.get("fonte_sha"), "dll_sha": ident.get("dll_sha"),
                       "suficiente": bool(str(ident.get("fonte_sha") or "").strip())
                       and bool(str(ident.get("dll_sha") or "").strip()),
                       "erro": ident.get("_erro")},
        "mods": list(MODS), "total": len(criterios or []), "contagem": contagem,
        "por_mod": por_mod, "criterios": criterios or [], "medicao": medicao,
    }


def exit_de(criterios):
    estados = [c.get("estado") for c in criterios or []]
    if REPROVADO in estados:
        return EXIT_FALHOU
    if OK in estados:
        return EXIT_OK
    return EXIT_NAO_RODOU


def texto_de(criterios, resumo):
    linhas = ["AUT-7 - medicao de estilo/atributos/dump (t_674c5976)",
              "identidade suficiente: %s" % ("SIM" if resumo["identidade"]["suficiente"] else "NAO"),
              "criterios: %d | OK=%d REPROVADO=%d NAO_EXERCITADO=%d INDETERMINADO=%d"
              % (resumo["total"], resumo["contagem"][OK], resumo["contagem"][REPROVADO],
                 resumo["contagem"][NAO_EXERCITADO], resumo["contagem"][INDETERMINADO]), ""]
    for mod in MODS:
        do_mod = [c for c in criterios if c.get("mod") == mod]
        linhas.append("== %s (%d criterios)" % (mod, len(do_mod)))
        for c in do_mod:
            linhas.append("  [%-15s] %s" % (c.get("estado"), c.get("id")))
            linhas.append("      observado: %s" % str(c.get("observado"))[:160])
            if c.get("estado") in (NAO_EXERCITADO, INDETERMINADO, REPROVADO):
                linhas.append("      motivo: %s" % str(c.get("motivo"))[:200])
        linhas.append("")
    linhas.append("> AUT-7 NAO substitui aceite humano nem publicacao do DoD.")
    return "\n".join(linhas)


def _carrega_json_arg(valor):
    """Aceita ARQUIVO ou JSON inline (a mesma convencao do CIC-3/CIC-4)."""
    if valor is None:
        return None
    if os.path.isfile(valor):
        return json.loads(_ler(valor))
    return json.loads(valor)


def main(argv=None):
    ap = argparse.ArgumentParser(description="AUT-7: mede estilo/atributos/dump (offline + runtime).")
    ap.add_argument("--repo", default=RAIZ)
    ap.add_argument("--out-dir", default=os.path.join(os.path.expandvars("%TEMP%"), "aut7-estilo"))
    ap.add_argument("--observacoes", help="JSON com observacoes de runtime (lista ou resultado AUT-4)")
    ap.add_argument("--identidade", help="JSON com fonte_sha/dll_sha (default: deriva do repo)")
    ap.add_argument("--sem-suite", action="store_true",
                    help="nao roda a suite; reusa os JSON ja gravados em --out-dir "
                         "(a fotografia cobre as ENTRADAS que a suite LE - 6 mods, tools/**, "
                         "lib/**, docs/cobertura/**, ReloadProbe/**, scratch/**, docs/PLANO-DE-TESTES.md "
                         "e os projetos *.csproj/*.props/*.targets da arvore - E os artefatos de build "
                         "que ela MEDE: dist/*.zip e <Mod>/bin/**/*.dll; o que fica fora esta no bloco "
                         "`medicao.fotografia` do resultado)")
    ap.add_argument("--sem-runtime", action="store_true", help="nao avalia aspecto de runtime")
    ap.add_argument("--validar-plano", help="valida um plano de coleta AUT-4 (offline, sem agir)")
    ap.add_argument("--out", help="grava o resumo (JSON) neste arquivo")
    ap.add_argument("--texto", action="store_true", help="imprime tambem a leitura humana")
    args = ap.parse_args(argv)

    identidade = {}
    erro_ident = None
    if args.identidade:
        try:
            identidade = _carrega_json_arg(args.identidade)
        except Exception as erro:
            print("ERRO: nao li --identidade (arquivo ou JSON): %s" % erro, file=sys.stderr)
            return EXIT_NAO_RODOU
    if not identidade:
        identidade, erro_ident = identidade_do_repo(os.path.abspath(args.repo))
    if erro_ident:
        identidade = dict(identidade)
        identidade["_erro"] = erro_ident

    criterios, meta = medir_offline(os.path.abspath(args.repo), os.path.abspath(args.out_dir),
                                    identidade, rodar=not args.sem_suite)
    if not args.sem_runtime:
        obs = None
        if args.observacoes:
            try:
                obs = json.loads(_ler(args.observacoes))
            except Exception as erro:
                print("AVISO: nao li --observacoes: %s" % erro, file=sys.stderr)
        criterios += avaliar(obs or [], identidade)

    if args.validar_plano:
        meta["valida_plano"] = validar_plano_aut4(args.validar_plano)

    resumo = resumir(criterios, identidade, meta)
    texto = json.dumps(resumo, ensure_ascii=False, indent=2, default=str)
    if args.out:
        _escrever(args.out, texto)
    print(texto)
    if args.texto:
        print("\n" + texto_de(criterios, resumo))
    return exit_de(criterios)


if __name__ == "__main__":
    sys.exit(main())
