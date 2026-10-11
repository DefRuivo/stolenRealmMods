#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT-07 - Exportador de evidencias com privacidade e retencao.

Monta um pacote COMPARTILHAVEL de ocorrencias (JSON + logs selecionados +,
opcionalmente, PNG) sem segredo e sem dado pessoal desnecessario.

Principios (testados em `teste_exportador_kit07.py` e `teste_exportador_kit07f.py`):
  * sanitizacao por PADROES GENERICOS (regex de forma), sem lista de valores
    fixos. JSON VALIDO e tratado de forma ESTRUTURAL (redige o valor de qualquer
    chave que pareca credencial e re-serializa mantendo JSON valido), o que cobre
    chave pontuada ("password:") e valor com aspa escapada; texto livre cai na
    regex de forma do `aut3_lib.sanitiza` (2a linha de defesa da AUT-3). Soma-se a
    minimizacao de dado pessoal (caminho de usuario, e-mail, host, IP privado,
    nome local). NAO ha promessa de segredo/anonimato perfeitos: as lacunas sao
    explicitas e a revisao humana continua obrigatoria.
  * NOMES e METADADOS tambem sao saida: caminho fisico, manifest (incluidos,
    excluidos, png_para_revisao) e relatorio passam pela mesma redacao/minimizacao,
    com mapeamento consistente e tratamento de colisao; a escrita minimizada nao
    invalida o sha256/bytes registrados.
  * EXCLUSAO obrigatoria de saves e de assemblies proprietarios do jogo; cada
    exclusao e registrada com motivo (nunca silenciosa). A classificacao e por
    TIPO de arquivo: um log textual selecionado (ex.: BepInEx/LogOutput.log) entra
    sanitizado; binarios/saves seguem fora.
  * screenshots (PNG) NAO sao sanitizados automaticamente e ficam DESLIGADOS por
    padrao: o humano lista, revisa e exclui antes de exportar. O relatorio traz o
    aviso explicito - nao ha promessa de sanitizacao automatica de imagem.
  * SEM upload por padrao: o modulo nao importa nem oferece caminho de rede.
  * a ORIGEM nunca e escrita: destino igual ou aninhado na origem (caminhos
    canonicos) e recusado ANTES de criar/gravar qualquer coisa.
  * limites de disco contam BYTES REAIS DE SAIDA (conteudo ja sanitizado) somados
    ao overhead de metadata declarado na politica; a montagem ocorre num diretorio
    temporario com troca so no sucesso (rollback, sem arquivos parciais).
  * exclusao segura: so apaga pacote KIT-07 PROPRIO (marcador valido + manifest
    valido + nenhum arquivo extra/nao listado/link); nunca a origem nem pasta alheia.

Uso:
    python tools/automacao/kit07/exportador.py --origem <dir> --destino <dir> \\
        [--incluir-png] [--max-arquivo-mb N] [--max-total-mb N]
    python tools/automacao/kit07/exportador.py --revisar-png --origem <dir>

Exit: 0 = pacote montado; 1 = erro de dominio (origem/destino invalido, limite
estourado, tentativa de upload); 2 = erro de uso/infraestrutura (I/O, argumentos).
Falha de etapa NUNCA vira verde.

Sem dependencia externa: so a stdlib.
"""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import sys
import time

# --- reuso da infraestrutura entregue (nao duplicar) -------------------------
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(_AQUI)))  # raiz do repo
_OFFLINE = os.path.join(_RAIZ, "tools", "automacao", "offline")
if _OFFLINE not in sys.path:
    sys.path.insert(0, _OFFLINE)

try:
    import aut3_lib  # noqa: E402  (sanitiza / sha256_bytes / sha256_file)
except ImportError as _erro:  # pragma: no cover - so em layout quebrado
    sys.stderr.write("ERRO KIT-07: aut3_lib ausente (%s)\n" % _erro)
    raise SystemExit(2)

KIT = "KIT-07"
MARCADOR = ".kit07-pacote"
MARCADOR_VERSAO = 1
NOMES_RESERVADOS = ("manifest.json", "relatorio.md", MARCADOR)
_RESERVADOS_LOWER = set(nome.lower() for nome in NOMES_RESERVADOS)
_SUFIXO_TEMP = ".kit07-build"
# Overhead de metadata declarado na politica (manifest + relatorio + marcador).
OVERHEAD_PADRAO = 4096

# Extensoes tratadas como TEXTO (podem ser sanitizadas).
EXT_TEXTO = {".json", ".log", ".txt", ".csv", ".md", ".jsonl", ".xml", ".yml", ".yaml"}
# Extensoes de imagem (nunca sanitizadas automaticamente).
EXT_PNG = {".png", ".jpg", ".jpeg", ".bmp"}

# SAves: nada disto pode entrar no pacote.
EXT_SAVE = {".sav", ".es3", ".save", ".srm", ".bak"}
SEG_SAVE = {"saves", "savedata", "savegames", "savegame", "backup-save"}
# Assemblies/binaros proprietarios e dependencias do jogo.
EXT_BINARIO = {".dll", ".pdb", ".so", ".dylib", ".exe", ".lib", ".a", ".mdb", ".deps.json"}
SEG_BINARIO = {"managed", "mono", "bepinex", "assembly-csharp", "dotnet"}
RE_BINARIO = re.compile(r"(?i)^assembly-csharp.*\.dll$")

# Rotulo generico de credencial: reusa o do aut3_lib quando disponivel (a lista
# e explicita e revisavel, sem VALORES). Fallback local equivalente se a lib
# trocar o nome interno.
_ROTULO = getattr(aut3_lib, "_ROTULO_SEGREDO", None) or (
    r"(?:pass(?:word|wd|phrase)|secret|token|api[_-]?key|apikey|"
    r"auth(?:orization)?|auth[_-]?token|access[_-]?key|"
    r"client[_-]?secret|private[_-]?key|credential)")
_RE_ROTULO = re.compile(r"(?i)\b" + _ROTULO + r"\b")

# FORMATOS de credencial dos scanners publicos (os MESMOS do aut3_lib). O aut3_lib
# ancora o prefixo com \b; um nome de arquivo como "capture_tss_..." NAO tem
# fronteira ali ('_' e caractere de palavra), entao o prefixo sobreviveria. Estes
# padroes repetem a forma SEM a fronteira inicial, so para REDIGIR saida/nome.
_PADROES_FORTES = tuple(re.compile(re.sub(r"^\\b", "", padrao))
                        for padrao in aut3_lib.PADROES_SEGREDO)


# ---------------------------------------------------------------------------
# Sanitizacao / minimizacao
# ---------------------------------------------------------------------------
# Minimizacao de dado PESSOAL por FORMA (sem valores fixos no codigo).
_RE_USUARIO_WIN = re.compile(r"(?i)\b[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s\"']+")
_RE_USUARIO_NIX = re.compile(r"(?i)/(?:home|Users)/[^\s/\"']+")
_RE_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_RE_IP_PRIV = re.compile(
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}"
    r"|127\.0\.0\.1)\b")
# Caracteres invalidos em nome de arquivo (Windows) - trocados por '_'.
_RE_NOME_INSEGURO = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def minimizar_pessoal(texto, nomes_extras=()):
    """Troca caminho de usuario / e-mail / IP privado / nome local por rotulo.

    `nomes_extras` sao valores conhecidos da sessao (ex.: usuario e host locais
    vindos do ambiente) - derivados em execucao, nunca codificados como constante.
    """
    if not texto:
        return texto
    texto = _RE_USUARIO_WIN.sub("<USUARIO>", texto)
    texto = _RE_USUARIO_NIX.sub("<USUARIO>", texto)
    texto = _RE_EMAIL.sub("<EMAIL>", texto)
    texto = _RE_IP_PRIV.sub("<IP>", texto)
    for nome in nomes_extras:
        if nome and len(nome) >= 3:
            texto = re.sub(re.escape(nome), "<LOCAL>", texto)
    return texto


def _redigir_prefixos(texto):
    """Redige prefixos conhecidos de credencial SEM exigir fronteira de palavra.

    Cobre o caso em que o prefixo vem colado a '_' (nome de arquivo, campo CI),
    onde o `\\b` do aut3_lib nao encontra fronteira.
    """
    for padrao in _PADROES_FORTES:
        texto = padrao.sub("<REDACTED>", texto)
    return texto


def _redigir_json(valor):
    """Percorre a estrutura JSON e redige o valor sob chave de credencial.

    Opera na estrutura DECODIFICADA: por isso cobre chave pontuada ("password:")
    e valor com aspa escapada, e a re-serializacao continua sendo JSON VALIDO.
    Em qualquer outro texto aplica a redacao de prefixos conhecidos.
    """
    if isinstance(valor, dict):
        novo = {}
        for chave, item in valor.items():
            if isinstance(chave, str) and _RE_ROTULO.search(chave):
                novo[chave] = "<REDACTED>" if item is not None else item
            else:
                novo[chave] = _redigir_json(item)
        return novo
    if isinstance(valor, list):
        return [_redigir_json(item) for item in valor]
    if isinstance(valor, str):
        return _redigir_prefixos(valor)
    return valor


def _json_redigido(texto):
    """JSON redigido (string VALIDA) ou None quando o texto nao e JSON."""
    try:
        estrutura = json.loads(texto)
    except (ValueError, TypeError):
        return None
    return json.dumps(_redigir_json(estrutura), ensure_ascii=False,
                      indent=2, sort_keys=True)


def _sanitiza_texto(texto):
    """JSON valido -> redacao estrutural; outro texto -> regex de forma do aut3_lib."""
    estrutural = _json_redigido(texto)
    if estrutural is not None:
        return estrutural
    return aut3_lib.sanitiza(texto)


def sanitizar(texto, nomes_extras=()):
    """Camada unica de conteudo: forma (segredo) + minimizacao (dado pessoal)."""
    if texto is None:
        return texto
    return minimizar_pessoal(_sanitiza_texto(texto), nomes_extras)


def sanear_para_saida(texto, nomes_extras=()):
    """Garante que NADA impresso (stdout/stderr/relatorio) carregue segredo.

    Redacao total do que casa padrao de credencial: aqui nao preservamos contexto
    (e saida para humano/CI), so evitamos qualquer valor/prefixo vazar.
    """
    if texto is None:
        return texto
    return minimizar_pessoal(aut3_lib.sanitiza(_redigir_prefixos(texto)), nomes_extras)


def _sanea_estrutura(valor, nomes_extras=()):
    """Saneia recursivamente um objeto de metadata (manifest/relatorio)."""
    if isinstance(valor, dict):
        return dict((chave, _sanea_estrutura(item, nomes_extras))
                    for chave, item in valor.items())
    if isinstance(valor, list):
        return [_sanea_estrutura(item, nomes_extras) for item in valor]
    if isinstance(valor, str):
        return minimizar_pessoal(_redigir_prefixos(valor), nomes_extras)
    return valor


def _nome_seguro(nome):
    """Nome de arquivo valido no FS a partir de um rotulo ja redigido."""
    limpo = _RE_NOME_INSEGURO.sub("_", nome)
    limpo = limpo.strip(" .")
    return limpo or "_"


def _sanitiza_segmento(segmento, nomes_extras=()):
    """Redige/minimiza UM segmento de caminho e devolve nome valido no FS."""
    if not segmento:
        return segmento
    limpo = aut3_lib.sanitiza(segmento)
    limpo = _redigir_prefixos(limpo)
    limpo = minimizar_pessoal(limpo, nomes_extras)
    return _nome_seguro(limpo)


def _sanitiza_caminho(rel_origem, nomes_extras=()):
    """Caminho relativo saneado (rotulo), sem tratamento de colisao."""
    return "/".join(_sanitiza_segmento(parte, nomes_extras)
                    for parte in rel_origem.split("/"))


def _caminho_pacote(rel_origem, nomes_extras, usados):
    """Caminho do arquivo DENTRO do pacote: saneado, seguro e sem colisao.

    `usados` guarda os caminhos ja reservados nesta exportacao. Nomes reservados
    do proprio exportador (manifest.json/relatorio.md/marcador) e duplicatas
    ganham sufixo deterministico, registrado no manifesto (referencia intacta).
    """
    rel = _sanitiza_caminho(rel_origem, nomes_extras)
    chave = rel.lower()
    if chave in _RESERVADOS_LOWER or chave in usados:
        raiz, ext = os.path.splitext(rel)
        rel = "%s-entrada%s" % (raiz, ext)
        contador = 2
        while rel.lower() in _RESERVADOS_LOWER or rel.lower() in usados:
            rel = "%s-entrada%d%s" % (raiz, contador, ext)
            contador += 1
    usados.add(rel.lower())
    return rel


# ---------------------------------------------------------------------------
# Politica e classificacao
# ---------------------------------------------------------------------------
class ErroExportacao(Exception):
    """Erro de dominio do exportador (origem/destino invalido, limite, upload...)."""


class PoliticaExportacao(object):
    def __init__(self, incluir_png=False, max_bytes_por_arquivo=8 * 1024 * 1024,
                 max_total_bytes=64 * 1024 * 1024, permitir_upload=False,
                 nomes_extras=(), overhead_bytes=OVERHEAD_PADRAO):
        self.incluir_png = bool(incluir_png)
        self.max_bytes_por_arquivo = int(max_bytes_por_arquivo)
        self.max_total_bytes = int(max_total_bytes)
        # O modulo NAO possui caminho de upload; deixar isto True e erro explicito.
        self.permitir_upload = bool(permitir_upload)
        self.nomes_extras = tuple(nomes_extras)
        # Overhead declarado da metadata, contado no teto total (bytes de saida).
        self.overhead_bytes = int(overhead_bytes)

    def para_dict(self):
        return {
            "incluir_png": self.incluir_png,
            "max_bytes_por_arquivo": self.max_bytes_por_arquivo,
            "max_total_bytes": self.max_total_bytes,
            "permitir_upload": self.permitir_upload,
            "overhead_bytes": self.overhead_bytes,
        }


def motivo_exclusao(caminho):
    """Devolve o motivo pelo qual o arquivo NAO pode entrar no pacote, ou None."""
    base = os.path.basename(caminho).lower()
    ext = os.path.splitext(base)[1]
    norm = os.path.normpath(caminho).replace("\\", "/").lower()
    segmentos = set(p for p in norm.split("/") if p)

    if ext in EXT_SAVE or any(s in segmentos for s in SEG_SAVE):
        return "save"
    # Binario/assembly: nome de assembly, extensao binaria, ou segmento de
    # binario (ex.: BepInEx) com tipo NAO textual - um log textual selecionado
    # entra sanitizado; DLL/save/binario seguem fora.
    if (RE_BINARIO.match(base) or ext in EXT_BINARIO
            or (segmentos & SEG_BINARIO and ext not in EXT_TEXTO)):
        return "assembly_proprietario"
    return None


def lista_revisao_png(origem):
    """PNGs encontrados na origem, para revisao/exclusao MANUAL antes de exportar."""
    achados = []
    if not os.path.isdir(origem):
        return achados
    for raiz, _dirs, arquivos in os.walk(origem):
        for nome in sorted(arquivos):
            if os.path.splitext(nome)[1].lower() in EXT_PNG:
                achados.append(os.path.relpath(os.path.join(raiz, nome), origem)
                               .replace("\\", "/"))
    return sorted(achados)


# ---------------------------------------------------------------------------
# Tetos de disco (bytes REAIS de saida)
# ---------------------------------------------------------------------------
def _excede_teto_arquivo(bytes_saida, politica):
    """Teto POR ARQUIVO medido no conteudo ja sanitizado (bytes de saida)."""
    return bytes_saida > politica.max_bytes_por_arquivo


def _confere_teto_total(total_previsto, bytes_novos, politica, referencia):
    """Teto TOTAL em bytes de saida + overhead declarado -> erro de dominio."""
    if total_previsto + bytes_novos + politica.overhead_bytes > politica.max_total_bytes:
        raise ErroExportacao(
            "limite total de saida excedido ao incluir %s (%d + %d + %d > %d)"
            % (referencia, total_previsto, bytes_novos, politica.overhead_bytes,
               politica.max_total_bytes))


def _verifica_tamanho_final(pacote, politica):
    """Confere o pacote REAL em disco contra o teto total (fecha o overhead real)."""
    total = 0
    for raiz, _dirs, arquivos in os.walk(pacote):
        for nome in arquivos:
            total += os.path.getsize(os.path.join(raiz, nome))
    # Mesmo teto da montagem: fecha o overhead REAL (nao apenas o declarado).
    _confere_teto_total(total, 0, politica, "pacote final")
    return total


# ---------------------------------------------------------------------------
# Montagem do pacote
# ---------------------------------------------------------------------------
def _sha256_bytes(dados):
    return hashlib.sha256(dados).hexdigest()


def _ler_texto(caminho):
    with open(caminho, "rb") as fh:
        bruto = fh.read()
    return bruto, bruto.decode("utf-8", "replace")


def _eh_subcaminho(filho, pai):
    """True se `filho` esta dentro de `pai` (comparacao por caminho canonico)."""
    try:
        return os.path.commonpath([filho, pai]) == pai
    except ValueError:  # drives diferentes
        return False


def _pacote_reconhecido(pacote):
    """None se `pacote` e um pacote KIT-07 PROPRIO e integro; senao, o motivo.

    Valida identidade (marcador), conteudo (marcador e manifest parseaveis com
    kit correto), proveniencia/escopo (nenhum arquivo fora dos reservados e dos
    listados no manifest) e recusa links. E a trava de limpar_temporarios.
    """
    if os.path.islink(pacote) or not os.path.isdir(pacote):
        return "recusado: %s nao e um diretorio de pacote KIT-07" % pacote
    caminho_marcador = os.path.join(pacote, MARCADOR)
    if not os.path.isfile(caminho_marcador):
        return "recusado: %s nao e um pacote KIT-07 (sem marcador)" % pacote
    try:
        with io.open(caminho_marcador, encoding="utf-8") as fh:
            marcador = json.load(fh)
    except (OSError, ValueError):
        return "recusado: marcador ilegivel ou invalido em %s" % pacote
    if not isinstance(marcador, dict) or marcador.get("kit") != KIT:
        return "recusado: %s nao e um pacote KIT-07 (marcador invalido)" % pacote
    caminho_manifest = os.path.join(pacote, "manifest.json")
    if not os.path.isfile(caminho_manifest):
        return "recusado: %s sem manifest.json (proveniencia ausente)" % pacote
    try:
        with io.open(caminho_manifest, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, ValueError):
        return "recusado: manifest ilegivel ou invalido em %s" % pacote
    if not isinstance(manifest, dict) or manifest.get("kit") != KIT:
        return "recusado: manifest de outro kit em %s" % pacote
    listados = set()
    for item in manifest.get("arquivos", []):
        if isinstance(item, dict) and isinstance(item.get("caminho"), str):
            listados.add(item["caminho"].replace("\\", "/").lower())
    for raiz, dirs, arquivos in os.walk(pacote):
        for nome in list(dirs):
            if os.path.islink(os.path.join(raiz, nome)):
                return "recusado: %s contem link de diretorio" % pacote
        for nome in arquivos:
            alvo = os.path.join(raiz, nome)
            if os.path.islink(alvo):
                return "recusado: %s contem link" % pacote
            rel = os.path.relpath(alvo, pacote).replace("\\", "/").lower()
            if rel not in _RESERVADOS_LOWER and rel not in listados:
                return "recusado: %s contem arquivo nao listado (%s)" % (pacote, rel)
    return None


def _construir_pacote(origem, temp, politica, agora=None):
    """Escreve arquivos + metadata DENTRO de `temp` e devolve o manifest."""
    incluir_png = politica.incluir_png
    nomes = politica.nomes_extras
    arquivos = []
    excluidos = []
    usados = set()
    png_revisao = sorted(_sanitiza_caminho(p, nomes)
                         for p in lista_revisao_png(origem))
    bytes_saida = 0

    for raiz, _dirs, nomes_arq in os.walk(origem):
        for nome in sorted(nomes_arq):
            absoluto = os.path.join(raiz, nome)
            rel_origem = os.path.relpath(absoluto, origem).replace("\\", "/")
            base = os.path.basename(rel_origem).lower()
            ext = os.path.splitext(base)[1]
            rotulo = _sanitiza_caminho(rel_origem, nomes)

            motivo = motivo_exclusao(rel_origem)
            if motivo:
                excluidos.append({"caminho": rotulo, "motivo": motivo})
                continue
            if ext in EXT_PNG and not incluir_png:
                excluidos.append({"caminho": rotulo, "motivo": "png_opt_in"})
                continue

            if ext in EXT_PNG:
                relativo = _caminho_pacote(rel_origem, nomes, usados)
                with open(absoluto, "rb") as fh:
                    dados = fh.read()
                if _excede_teto_arquivo(len(dados), politica):
                    excluidos.append({"caminho": rotulo,
                                      "motivo": "excede_limite_por_arquivo",
                                      "bytes": len(dados)})
                    continue
                _confere_teto_total(bytes_saida, len(dados), politica, relativo)
                destino_arq = os.path.join(temp, *relativo.split("/"))
                os.makedirs(os.path.dirname(destino_arq), exist_ok=True)
                with open(destino_arq, "wb") as fh:
                    fh.write(dados)
                bytes_saida += len(dados)
                arquivos.append({
                    "caminho": relativo, "bytes": len(dados),
                    "sha256": _sha256_bytes(dados), "sanitizado": False,
                    "tipo": "imagem",
                    "aviso": "imagem NAO sanitizada automaticamente; revisar antes de compartilhar",
                })
            elif ext in EXT_TEXTO:
                relativo = _caminho_pacote(rel_origem, nomes, usados)
                _bruto, texto = _ler_texto(absoluto)
                limpo = sanitizar(texto, nomes)
                dados = limpo.encode("utf-8")
                if _excede_teto_arquivo(len(dados), politica):
                    excluidos.append({"caminho": rotulo,
                                      "motivo": "excede_limite_por_arquivo",
                                      "bytes": len(dados)})
                    continue
                _confere_teto_total(bytes_saida, len(dados), politica, relativo)
                destino_arq = os.path.join(temp, *relativo.split("/"))
                os.makedirs(os.path.dirname(destino_arq), exist_ok=True)
                with open(destino_arq, "wb") as fh:
                    fh.write(dados)
                bytes_saida += len(dados)
                arquivos.append({
                    "caminho": relativo, "bytes": len(dados),
                    "sha256": _sha256_bytes(dados),
                    "sanitizado": limpo != texto,
                    "tipo": "texto",
                })
            else:
                # Formato binario desconhecido: nao entra (nao sabemos se carrega segredo).
                relativo = rotulo
                excluidos.append({"caminho": relativo, "motivo": "formato_binario_desconhecido"})
                continue

    por_motivo = {}
    for item in excluidos:
        por_motivo[item["motivo"]] = por_motivo.get(item["motivo"], 0) + 1

    avisos = []
    if png_revisao:
        avisos.append(
            "%d imagem(ns) detectada(s): screenshots podem conter nomes de personagem, "
            "chat ou dados pessoais. Revise/exclua manualmente antes de exportar; NAO ha "
            "sanitizacao automatica de imagem." % len(png_revisao))

    diagnostico = {
        "incluidos": len(arquivos),
        "excluidos": len(excluidos),
        "por_motivo": por_motivo,
        "bytes_incluidos": bytes_saida,
        "overhead_bytes": politica.overhead_bytes,
        "png_para_revisao": png_revisao,
        "upload": False,
        "avisos": avisos,
    }
    manifest = {
        "kit": KIT,
        "gerado_em": agora or time.strftime("%Y-%m-%dT%H:%M:%S"),
        "origem": "ocorrencias",
        "politica": politica.para_dict(),
        "arquivos": sorted(arquivos, key=lambda a: a["caminho"]),
        "excluidos": sorted(excluidos, key=lambda a: a["caminho"]),
        "diagnostico": diagnostico,
    }
    # F1: o manifesto tambem e SAIDA - nomes, rotulos e avisos passam pela mesma
    # redacao/minimizacao antes de serializar (nao ha valor/prefixo no JSON).
    manifest = _sanea_estrutura(manifest, nomes)
    manifest_json = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
    with io.open(os.path.join(temp, "manifest.json"), "w", encoding="utf-8") as fh:
        fh.write(manifest_json)

    with io.open(os.path.join(temp, "relatorio.md"), "w", encoding="utf-8") as fh:
        fh.write(_relatorio(manifest))

    with io.open(os.path.join(temp, MARCADOR), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"kit": KIT, "versao": MARCADOR_VERSAO,
                             "gerado_em": manifest["gerado_em"]}))

    return manifest


def montar_pacote(origem, destino, politica=None, agora=None):
    """Monta o pacote em `destino` e devolve o dicionario do manifest.

    Nunca escreve na origem: destino igual ou aninhado na origem (caminhos
    canonicos) e recusado ANTES de qualquer escrita. Se `destino` ja existir e nao
    estiver vazio, exige ser um pacote KIT-07 reconhecido; a nova exportacao
    substitui o pacote anterior por inteiro (sem sobras de politica/selecao
    antiga). A montagem ocorre num diretorio temporario; a troca e so no sucesso
    (rollback sem arquivos parciais).
    """
    politica = politica or PoliticaExportacao()
    if politica.permitir_upload:
        raise ErroExportacao("upload nao e suportado por este exportador")
    if not os.path.isdir(origem):
        raise ErroExportacao("origem inexistente: %s" % origem)

    origem_real = os.path.realpath(os.path.abspath(origem))
    destino_real = os.path.realpath(os.path.abspath(destino))
    if (origem_real == destino_real
            or _eh_subcaminho(destino_real, origem_real)
            or _eh_subcaminho(origem_real, destino_real)):
        raise ErroExportacao(
            "recusado: destino sobreposto a origem (nunca escrever a origem): %s"
            % destino)

    destino_abs = os.path.abspath(destino)
    if os.path.exists(destino_abs):
        if not os.path.isdir(destino_abs):
            raise ErroExportacao("destino existe e nao e um diretorio: %s" % destino)
        if os.listdir(destino_abs):
            problema = _pacote_reconhecido(destino_abs)
            if problema:
                raise ErroExportacao(
                    "destino nao vazio e nao e pacote KIT-07 reconhecido: %s" % destino)

    temp = destino_abs + _SUFIXO_TEMP
    pai = os.path.dirname(temp)
    if pai:
        os.makedirs(pai, exist_ok=True)
    shutil.rmtree(temp, ignore_errors=True)
    try:
        os.makedirs(temp, exist_ok=True)
        manifest = _construir_pacote(origem, temp, politica, agora)
        _verifica_tamanho_final(temp, politica)
    except BaseException:
        shutil.rmtree(temp, ignore_errors=True)
        raise
    if os.path.exists(destino_abs):
        shutil.rmtree(destino_abs)
    os.rename(temp, destino_abs)
    return manifest


def _relatorio(manifest):
    diag = manifest["diagnostico"]
    linhas = [
        "# KIT-07 - relatorio de exportacao",
        "",
        "Gerado em: %s" % manifest["gerado_em"],
        "",
        "## Resumo",
        "",
        "- arquivos incluidos: %d" % diag["incluidos"],
        "- arquivos excluidos: %d" % diag["excluidos"],
        "- bytes de saida incluidos: %d" % diag["bytes_incluidos"],
        "- overhead de metadata: %d" % diag["overhead_bytes"],
        "- upload: %s" % ("sim" if diag["upload"] else "nao"),
        "",
        "## Excluidos por motivo",
        "",
    ]
    for motivo, qtd in sorted(diag["por_motivo"].items()):
        linhas.append("- %s: %d" % (motivo, qtd))
    if not diag["por_motivo"]:
        linhas.append("- (nenhum)")
    linhas += ["", "## Avisos", ""]
    if diag["avisos"]:
        linhas += ["- " + a for a in diag["avisos"]]
    else:
        linhas.append("- (nenhum)")
    linhas += ["", "## Integridade", "", "Cada arquivo do pacote tem sha256 no manifest.json.", ""]
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Exclusao segura
# ---------------------------------------------------------------------------
def limpar_temporarios(pacote):
    """Apaga APENAS um pacote KIT-07 PROPRIO e integro (ver `_pacote_reconhecido`).

    Recusa caminho sem marcador/conteudo valido, com arquivo nao listado, com
    link, ou que nao seja diretorio - nunca apaga a origem nem pasta arbitraria.
    Devolve a lista de caminhos removidos.
    """
    pacote = os.path.abspath(pacote)
    if not os.path.exists(pacote):
        raise ErroExportacao("pacote inexistente: %s" % pacote)
    problema = _pacote_reconhecido(pacote)
    if problema:
        raise ErroExportacao(problema)
    removidos = []
    for raiz, dirs, arquivos in os.walk(pacote, topdown=False):
        for nome in arquivos:
            alvo = os.path.join(raiz, nome)
            os.remove(alvo)
            removidos.append(alvo)
        for nome in dirs:
            alvo = os.path.join(raiz, nome)
            try:
                os.rmdir(alvo)
            except OSError:
                pass
    shutil.rmtree(pacote, ignore_errors=True)
    return removidos


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-07 - exportador de evidencias")
    ap.add_argument("--origem", required=True)
    ap.add_argument("--destino")
    ap.add_argument("--revisar-png", action="store_true",
                    help="apenas lista os PNGs para revisao manual e sai")
    ap.add_argument("--incluir-png", action="store_true")
    ap.add_argument("--max-arquivo-mb", type=int, default=8)
    ap.add_argument("--max-total-mb", type=int, default=64)
    args = ap.parse_args(argv)

    nomes = [os.environ.get("USERNAME"), os.environ.get("USER"),
             os.environ.get("COMPUTERNAME"), os.environ.get("HOSTNAME")]

    def _erro(texto):
        # Toda saida de falha passa pela redacao: nada de valor/prefixo/traceback.
        sys.stderr.write(sanear_para_saida(texto, nomes))

    try:
        if not os.path.isdir(args.origem):
            _erro("ERRO KIT-07: origem inexistente: %s\n" % args.origem)
            return 2

        if args.revisar_png:
            for png in lista_revisao_png(args.origem):
                # nome de arquivo e dado de saida: passa pela mesma redacao.
                print(sanear_para_saida(png, nomes))
            return 0

        if not args.destino:
            _erro("ERRO KIT-07: --destino obrigatorio\n")
            return 2

        politica = PoliticaExportacao(
            incluir_png=args.incluir_png,
            max_bytes_por_arquivo=args.max_arquivo_mb * 1024 * 1024,
            max_total_bytes=args.max_total_mb * 1024 * 1024,
            nomes_extras=nomes,
        )
        manifest = montar_pacote(args.origem, args.destino, politica)
    except ErroExportacao as erro:
        _erro("ERRO KIT-07: %s\n" % erro)
        return 1
    except OSError as erro:
        # I/O e caminho: dominio de infraestrutura (2), sempre sanado.
        _erro("ERRO KIT-07 (infra): %s: %s\n" % (type(erro).__name__, erro))
        return 2
    except Exception as erro:  # noqa: BLE001 - ultima barreira da CLI
        _erro("ERRO KIT-07 (infra): %s: %s\n" % (type(erro).__name__, erro))
        return 2

    diag = manifest["diagnostico"]
    print("KIT-07: %d incluidos, %d excluidos, %d bytes, upload=%s"
          % (diag["incluidos"], diag["excluidos"], diag["bytes_incluidos"],
             "sim" if diag["upload"] else "nao"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
