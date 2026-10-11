#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""executor.py - KIT-11F: executor DETERMINISTICO de cenarios conhecidos, permissoes separadas.

OBJETIVO (cartoes `t_f2129aea` -> correcao `t_2a38d1d3` KIT-11F)
----------------------------------------------------------------
Reusar coletor/driver para EXECUTAR cenarios CONHECIDOS sob autorizacao, sem IA improvisando:
uma maquina de estados que ESPERA menu/tela/condicao (nunca "sleep cego"), com HANDLERS por tipo,
DIAGNOSTICO do que faltou e TIMEOUT explicito por passo, FRENTE UNICA, CANCELAMENTO/ROLLBACK exatos
e ENCERRAMENTO apenas da instancia que a propria execucao criou.

GARANTIAS (contrato deste modulo, provadas por teste offline)
-------------------------------------------------------------
1. FALHA FECHADA em config: esquema ausente/errado, `versao` fora das compativeis, `modo`
   desconhecido, `passos` vazio, `timeout_s` ausente/None/NaN/inf/<=0 e `requer_acao` nao
   booleano RECUSAM a execucao (`ConfigInvalida`) — nunca "age por default".
2. NAO EXECUTA COMANDO ARBITRARIO de cenario: passo que declare campo executavel
   (`comando`/`argv`/`shell`/`exec`/`cmd`/`subprocess`) e RECUSADO, assim como chave que
   colida com uma ACAO ATIVA da trava dura do `controle_acesso` (reuso real, nao citacao).
   O executor so ESPERA condicoes CONHECIDAS (`menu`/`tela`/`condicao`), nunca roda comando
   vindo do plano.
3. PERMISSOES SEPARADAS E TIPADAS: `observacao_autorizada` libera apenas OBSERVAR; passo
   `requer_acao` (ou `modo=ativo`) exige `ativa_autorizada` SEPARADA. NENHUMA entrada ou
   override aceita coercao (`'false'` NAO vira True); sem autorizacao de observacao o executor
   NAO LE a fonte e sai `NAO_EXERCITADO` (exit 2 na CLI). Observacao NUNCA concede acao nem
   encerramento.
4. MODO ATIVO exige perfil/save de TESTE verificados (marcadores confrontados com a fonte);
   sem eles, RECUSA antes de qualquer acao.
5. FRENTE UNICA OBRIGATORIA: lock por PID+token adquirido com `O_CREAT|O_EXCL` (atomico, sem
   janela `exists`->`open`); frente viva (ou nao mensuravel) RECUSA; retomada de lock morto
   nunca remove lock de terceiro. A frente NAO e opcional na API nem ausente na CLI.
6. RESULTADO TERMINAL preservado: o `finally` roda rollback/encerramento/liberacao como fases
   SEPARADAS (cada uma com erro estruturado proprio) e NAO substitui CONCLUIDO/TIMEOUT/
   CANCELADO por ROLLBACK/ENCERRAMENTO. Efeito verificado determina o erro; mensagem de sucesso
   nao substitui estado lido.
7. ROLLBACK MINIMO: remove SO o que esta execucao criou, preserva diretorios e `dir_backup`
   PREEXISTENTES (snapshot_dirs + subdiretorio proprio de backup) e confere o estado final.
8. ENCERRAMENTO COMPROVADO: so PIDs PROPRIOS (criados por esta execucao), com autorizacao de
   acao e liveness MENSURAVEL; PIDs externos que nasceram durante a observacao e liveness
   `None` NUNCA disparam fechamento (nem forcam `taskkill` na duvida).
9. CANCELAMENTO rechecado ANTES de declarar satisfacao e antes de efeitos; cancelamento lido
   na ultima leitura NAO e ignorado.
10. REUSO, nunca duplicacao: `coletor.py` (snapshot/rollback/encerramento) e `controle_acesso.py`
    (vocabulario de acoes ativas proibidas).

LIMITE HONESTO
--------------
Isto e a LOGICA offline do executor. A NAVEGACAO REAL e o CLIQUE FISICO sao qualificados em
KIT-14 (apos KIT-G2). Nada aqui abre/fecha o jogo, instala probe, carrega save ou publica.
A fonte de estado e INJETAVEL: `FonteDeArquivo` (offline real) nos testes e um stub nos testes;
no runtime autorizado a fonte sera o probe/coletor (KIT-14).
"""
import argparse
import importlib.util
import json
import math
import os
import shutil
import sys
import tempfile
import time
import uuid

AQUI = os.path.dirname(os.path.abspath(__file__))
AUTOMACAO = os.path.dirname(AQUI)                      # tools/automacao
def _resolver_runtime():
    """Diretorio que contem coletor.py/controle_acesso.py (KIT-15F/F9).

    - repositorio do autor: `tools/automacao/runtime`;
    - layout DISTRIBUIDO (pacote extraido): componentes IRMAOS -- `components/recorder`,
      onde o Recorder e de fato empacotado (o antigo caminho fixo `runtime` nao existia no
      pacote e quebrava o Runner)."""
    candidatos = [
        os.environ.get("KIT11_RUNTIME") or "",
        os.path.join(AUTOMACAO, "runtime"),
        os.path.join(os.path.dirname(AQUI), "recorder"),
        os.path.join(AQUI, "recorder"),
    ]
    for c in candidatos:
        if c and os.path.isfile(os.path.join(c, "coletor.py")):
            return c
    return os.path.join(AUTOMACAO, "runtime")


RUNTIME = _resolver_runtime()           # tools/automacao/runtime (repo) ou components/recorder (pacote)

ESQUEMA_EXECUTOR = "KIT-11/executor/1"
VERSAO_EXECUTOR = 1
VERSOES_COMPATIVEIS = (1,)

TIPOS_ESPERA = ("menu", "tela", "condicao")
CONDICOES_CONHECIDAS = frozenset((
    "jogo_aberto", "probe_carregado", "perfil_de_teste", "save_de_teste",
    "menu_principal_visivel", "autorizacao_ativa",
))
# Campo executavel em passo de cenario: RECUSADO (nao rodamos comando de cenario).
CAMPOS_EXECUTAVEIS = ("comando", "argv", "shell", "exec", "cmd", "subprocess")
MODOS = ("observacao", "ativo")

# Frente unica: caminho DETERMINISTICO do lock (pode ser trocado por parametro/CLI).
NOME_LOCK_PADRAO = "kit11-frente-unica.lock"

# ------------------------------------------------------------- estados ---------
INATIVO = "INATIVO"
VALIDANDO = "VALIDANDO"
PERMISSOES = "PERMISSOES"
AMBIENTE = "AMBIENTE"
FRENTE = "FRENTE"
AGUARDANDO = "AGUARDANDO"
CONCLUIDO = "CONCLUIDO"
TIMEOUT = "TIMEOUT"
CANCELADO = "CANCELADO"
NAO_EXERCITADO = "NAO_EXERCITADO"
ROLLBACK = "ROLLBACK"              # nome de FASE de cleanup (nao e estado terminal)
ENCERRAMENTO = "ENCERRAMENTO"      # nome de FASE de cleanup (nao e estado terminal)
FALHOU_FECHADO = "FALHOU_FECHADO"

VEREDITO_PASSOU = "PASSOU"
VEREDITO_FALHOU = "FALHOU"
VEREDITO_CANCELADO = "CANCELADO"
VEREDITO_FECHADO = "FALHOU_FECHADO"
VEREDITO_OBSERVADO = "OBSERVADO"
VEREDITO_NAO_EXERCITADO = "NAO_EXERCITADO"

ESTADO_DO_VEREDITO = {
    CONCLUIDO: VEREDITO_PASSOU,
    TIMEOUT: VEREDITO_FALHOU,
    CANCELADO: VEREDITO_CANCELADO,
    FALHOU_FECHADO: VEREDITO_FECHADO,
    NAO_EXERCITADO: VEREDITO_NAO_EXERCITADO,
}
# Estados TERMINAIS: o cleanup NUNCA os substitui (F6).
ESTADOS_TERMINAIS = frozenset((CONCLUIDO, TIMEOUT, CANCELADO, FALHOU_FECHADO, NAO_EXERCITADO))


class ConfigInvalida(ValueError):
    """Config do plano/fonte nao cumpre o contrato: FAIL CLOSED (nunca age por default)."""


class FrenteOcupada(RuntimeError):
    """Ja existe frente ativa (ou nao mensuravel): uma unica frente por vez."""


# ------------------------------------------------------------- reuso -----------
def coletor():
    """Importa `runtime/coletor.py` como modulo (reuso, sem editar)."""
    caminho = os.path.join(RUNTIME, "coletor.py")
    spec = importlib.util.spec_from_file_location("kit11_aut4_coletor", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_CONTROLE = None


def controle_acesso():
    """Importa `runtime/controle_acesso.py` como modulo (reuso REAL da trava dura).

    Usado como vocabulario de ACOES ATIVAS proibidas: um passo do plano nao pode declarar
    chave que colida com uma acao ativa (`clique_emitido`, `salvar`, `modo_ativo`, ...).
    """
    global _CONTROLE
    if _CONTROLE is None:
        caminho = os.path.join(RUNTIME, "controle_acesso.py")
        spec = importlib.util.spec_from_file_location("kit11_controle_acesso", caminho)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        _CONTROLE = modulo
    return _CONTROLE


def _acoes_ativas_proibidas():
    """Vocabulario (frozenset) de acoes ativas proibidas vindo do controle_acesso."""
    try:
        return frozenset(str(a).lower() for a in controle_acesso().ACOES_ATIVAS)
    except Exception as erro:                                  # fail-closed honesto
        raise ConfigInvalida("trava de acoes ativas indisponivel (controle_acesso): %s" % erro)


def caminho_frente_padrao():
    """Lock padrao da frente unica: caminho DETERMINISTICO e compartilhado na maquina."""
    return os.path.join(tempfile.gettempdir(), NOME_LOCK_PADRAO)


# ------------------------------------------------------------- validacao -------
def _booleano(valor, onde):
    """Aceita SOMENTE bool. Nada de bool('false') == True (F1)."""
    if isinstance(valor, bool):
        return valor
    raise ConfigInvalida("%s precisa ser booleano (True/False), veio %r" % (onde, valor))


def _timeout_finito(valor, onde):
    """`timeout_s` obrigatorio, finito e positivo (F3)."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ConfigInvalida("%s: 'timeout_s' obrigatorio e numerico, veio %r" % (onde, valor))
    if not math.isfinite(float(valor)):
        raise ConfigInvalida("%s: 'timeout_s' precisa ser FINITO, veio %r" % (onde, valor))
    if float(valor) <= 0:
        raise ConfigInvalida("%s: 'timeout_s' precisa ser > 0, veio %r" % (onde, valor))
    return float(valor)


def validar_plano_execucao(plano):
    """Valida e normaliza o plano. FALHA FECHADA (`ConfigInvalida`) se algo desconhecido."""
    if not isinstance(plano, dict):
        raise ConfigInvalida("plano nao e um objeto JSON")
    if plano.get("esquema") != ESQUEMA_EXECUTOR:
        raise ConfigInvalida("esquema ausente ou errado: esperado %r, veio %r"
                             % (ESQUEMA_EXECUTOR, plano.get("esquema")))
    versao = plano.get("versao")
    if not isinstance(versao, int) or isinstance(versao, bool):
        raise ConfigInvalida("versao ausente ou nao inteira: %r" % (versao,))
    if versao not in VERSOES_COMPATIVEIS:
        raise ConfigInvalida("versao incompativel: %r nao esta em %r"
                             % (versao, list(VERSOES_COMPATIVEIS)))
    modo = plano.get("modo")
    if modo not in MODOS:
        raise ConfigInvalida("modo desconhecido: %r (validos: %s)" % (modo, ", ".join(MODOS)))
    aut = plano.get("autorizacao")
    if not isinstance(aut, dict):
        raise ConfigInvalida("plano sem o bloco 'autorizacao'")
    if "observacao_autorizada" not in aut:
        raise ConfigInvalida("autorizacao sem 'observacao_autorizada'")
    _booleano(aut["observacao_autorizada"], "autorizacao.observacao_autorizada")
    if "ativa_autorizada" in aut:
        _booleano(aut["ativa_autorizada"], "autorizacao.ativa_autorizada")
    passos = plano.get("passos")
    if not isinstance(passos, list) or not passos:
        raise ConfigInvalida("plano sem 'passos' (lista nao vazia)")
    proibidas = _acoes_ativas_proibidas()
    norm = []
    for i, passo in enumerate(passos):
        if not isinstance(passo, dict):
            raise ConfigInvalida("passo %d nao e um objeto" % i)
        nome = str(passo.get("nome") or "").strip()
        if not nome:
            raise ConfigInvalida("passo %d sem 'nome'" % i)
        tipo = passo.get("tipo")
        if tipo not in TIPOS_ESPERA:
            raise ConfigInvalida("passo %r: tipo desconhecido %r (validos: %s)"
                                 % (nome, tipo, ", ".join(TIPOS_ESPERA)))
        alvo = passo.get("alvo")
        if alvo is None or (isinstance(alvo, str) and not alvo.strip()):
            raise ConfigInvalida("passo %r sem 'alvo'" % nome)
        if tipo == "condicao" and str(alvo) not in CONDICOES_CONHECIDAS:
            raise ConfigInvalida("passo %r: condicao desconhecida %r (conhecidas: %s)"
                                 % (nome, alvo, ", ".join(sorted(CONDICOES_CONHECIDAS))))
        proibidos = [k for k in CAMPOS_EXECUTAVEIS if k in passo]
        if proibidos:
            raise ConfigInvalida("passo %r declara campo executavel %s: o executor NAO roda "
                                 "comando de cenario" % (nome, ", ".join(proibidos)))
        ativas = sorted(str(k) for k in passo if str(k).lower() in proibidas)
        if ativas:
            raise ConfigInvalida("passo %r declara acao ativa proibida pelo controle de acesso: %s"
                                 % (nome, ", ".join(ativas)))
        if "requer_acao" in passo:
            requer = _booleano(passo["requer_acao"], "passo %r.requer_acao" % nome)
        else:
            requer = False
        teto = _timeout_finito(passo.get("timeout_s"), "passo %r" % nome)
        norm.append({"nome": nome, "tipo": tipo, "alvo": str(alvo),
                     "timeout_s": teto, "requer_acao": requer})
    saida = dict(plano)
    saida["modo"] = modo
    saida["passos"] = norm
    saida["autorizacao"] = {"observacao_autorizada": aut["observacao_autorizada"],
                            "ativa_autorizada": aut.get("ativa_autorizada", False)}
    return saida


# ------------------------------------------------------------- permissoes ------
def decidir_permissoes(plano, autorizacao=None):
    """Separa OBSERVAR de AGIR. Tipos ESTRITOS em TODAS as entradas/overrides (F1)."""
    if autorizacao is None:
        aut = (plano or {}).get("autorizacao") or {}
    else:
        if not isinstance(autorizacao, dict):
            raise ConfigInvalida("override de autorizacao nao e um objeto: %r" % (autorizacao,))
        aut = autorizacao
    if "observacao_autorizada" in aut:
        obs = _booleano(aut["observacao_autorizada"], "autorizacao.observacao_autorizada")
    else:
        obs = False
    if "ativa_autorizada" in aut:
        ativa = _booleano(aut["ativa_autorizada"], "autorizacao.ativa_autorizada")
    else:
        ativa = False
    passos = (plano or {}).get("passos") or []
    ativos = [p["nome"] for p in passos if p.get("requer_acao")]
    quer_agir = (plano or {}).get("modo") == "ativo" or bool(ativos)
    base = {"observacao_autorizada": obs, "ativa_autorizada": ativa,
            "modo": (plano or {}).get("modo"), "passos_ativos": ativos}
    if not quer_agir and not obs:
        base.update({"permite_observar": False, "permite_agir": False, "status": NAO_EXERCITADO,
                     "motivo": ("observacao NAO autorizada: nenhuma leitura e feita "
                                "(observacao != acao)")})
        return base
    if not quer_agir:
        base.update({"permite_observar": True, "permite_agir": False, "status": "OBSERVACAO",
                     "motivo": "plano so observa: observacao NAO concede acao"})
        return base
    if not ativa:
        base.update({"permite_observar": obs, "permite_agir": False, "status": FALHOU_FECHADO,
                     "motivo": ("passo ativo exige autorizacao SEPARADA ('ativa_autorizada'): "
                                "observacao NAO concede acao")})
        return base
    base.update({"permite_observar": obs, "permite_agir": True, "status": "AUTORIZADO",
                 "motivo": "modo ativo com autorizacao separada"})
    return base


# ------------------------------------------------------------- fonte/handlers ---
def _satisfeito_estrito(valor, origem):
    """`satisfeito` precisa ser BOOLEANO. String 'false' NAO promove verde (F2)."""
    if not isinstance(valor, bool):
        raise ConfigInvalida("%s: 'satisfeito' nao e booleano (%r) — resposta NAO satisfeita"
                             % (origem, valor))
    return valor


def _consultar(fonte, passo):
    """Handler REAL: pergunta a fonte e normaliza a resposta. Resposta invalida -> fail closed."""
    if not hasattr(fonte, "ler"):
        raise ConfigInvalida("fonte de estado sem o metodo 'ler' (contrato do executor)")
    resposta = fonte.ler(passo["tipo"], passo["alvo"])
    if not isinstance(resposta, dict) or "satisfeito" not in resposta:
        raise ConfigInvalida("fonte devolveu resposta invalida para o passo %r" % passo["nome"])
    satisfeito = _satisfeito_estrito(resposta["satisfeito"], "fonte do passo %r" % passo["nome"])
    return {"satisfeito": satisfeito,
            "observado": resposta.get("observado"),
            "diagnostico": resposta.get("diagnostico") or ""}


class FonteDeArquivo(object):
    """Fonte de estado OFFLINE REAL: le um JSON `{"estado": {"<tipo>:<alvo>": ...}}`.

    Cada chave pode ser `true`/`false` ou `{"satisfeito": bool, "observado": ..., "diagnostico": ...}`.
    Arquivo ausente NAO e satisfeito (falha fechada, nunca "assume OK"); JSON invalido e resposta
    com `satisfeito` nao booleano viram `ConfigInvalida` com diagnostico estruturado (sem estourar
    `JSONDecodeError` cru). A leitura NAO tem side-effect.
    """

    def __init__(self, caminho):
        self.caminho = caminho

    def ler(self, tipo, alvo):
        chave = "%s:%s" % (tipo, alvo)
        if not os.path.isfile(self.caminho):
            return {"satisfeito": False, "observado": None,
                    "diagnostico": "arquivo de estado ausente: %s" % self.caminho}
        try:
            with open(self.caminho, encoding="utf-8") as fh:
                doc = json.load(fh)
        except Exception as erro:
            raise ConfigInvalida("estado ilegivel em %s: %s: %s"
                                 % (self.caminho, type(erro).__name__, erro))
        mapa = doc.get("estado", {}) if isinstance(doc, dict) else {}
        if not isinstance(mapa, dict):
            raise ConfigInvalida("estado invalido em %s: 'estado' nao e um objeto" % self.caminho)
        valor = mapa.get(chave)
        if isinstance(valor, dict):
            satisfeito = _satisfeito_estrito(valor.get("satisfeito"),
                                             "estado '%s' de %s" % (chave, self.caminho))
            return {"satisfeito": satisfeito,
                    "observado": valor.get("observado"),
                    "diagnostico": valor.get("diagnostico") or ""}
        if valor is True:
            return {"satisfeito": True, "observado": True, "diagnostico": ""}
        return {"satisfeito": False, "observado": valor,
                "diagnostico": "estado '%s' ainda nao satisfeito" % chave}


def verificar_ambiente_de_teste(fonte, perfil_de_teste=None, save_de_teste=None):
    """MODO ATIVO exige perfil/save de TESTE verificados: o esperado e CONFRONTADO com a fonte."""
    motivos = []
    leituras = {}
    if not perfil_de_teste:
        motivos.append("'perfil_de_teste' nao declarado (modo ativo exige perfil de teste)")
    if not save_de_teste:
        motivos.append("'save_de_teste' nao declarado (modo ativo exige save de teste)")
    for chave, esperado in (("perfil_de_teste", perfil_de_teste), ("save_de_teste", save_de_teste)):
        if not esperado:
            continue
        try:
            leitura = _consultar(fonte, {"tipo": "condicao", "alvo": chave, "nome": chave})
        except ConfigInvalida as erro:
            motivos.append("%s: leitura invalida (%s)" % (chave, erro))
            continue
        leituras[chave] = {"esperado": esperado, "observado": leitura.get("observado"),
                           "satisfeito": leitura["satisfeito"]}
        if not leitura["satisfeito"] or str(leitura.get("observado")) != str(esperado):
            motivos.append("%s: esperado %r, observado %r"
                           % (chave, esperado, leitura.get("observado")))
    return {"ok": not motivos, "motivos": motivos, "leituras": leituras}


# ------------------------------------------------------------- frente unica -----
def _pid_vivo_padrao(pid):
    try:
        return coletor()._pid_vivo(pid)
    except Exception:
        return None


class FrenteUnica(object):
    """Lock de FRENTE UNICA por PID+token.

    Aquisicao ATOMICA (`O_CREAT|O_EXCL`): nao existe janela `exists`->`open` em que dois
    chamadores ganham o mesmo lock. Frente viva (ou nao mensuravel) RECUSA; retomada de lock
    MORTO so remove o lock que ele proprio leu como morto (nunca o de terceiro vivo).
    """

    def __init__(self, caminho, pid=None, vivo=None, token=None):
        self.caminho = caminho
        self.pid = os.getpid() if pid is None else int(pid)
        self.vivo = vivo or _pid_vivo_padrao
        self.token = token or uuid.uuid4().hex
        self.obtida = False

    def _ler(self):
        try:
            with open(self.caminho, encoding="utf-8") as fh:
                doc = json.load(fh)
            return doc if isinstance(doc, dict) else None
        except Exception:
            return None

    def _recusa_ocupada(self, doc):
        dono = doc.get("pid") if isinstance(doc, dict) else None
        if dono is None:
            raise FrenteOcupada("lock %s ilegivel/sem pid: RECUSADO (fail-closed)"
                                % self.caminho)
        estado = self.vivo(dono)
        if estado is None:
            raise FrenteOcupada("nao deu para medir o pid %r do lock %s: RECUSADO "
                                "(fail-closed)" % (dono, self.caminho))
        if estado:
            raise FrenteOcupada("frente ja ativa (pid %r): uma unica frente por vez" % dono)

    def obter(self):
        pai = os.path.dirname(self.caminho)
        if pai:
            os.makedirs(pai, exist_ok=True)
        doc = {"pid": self.pid, "token": self.token, "quando": time.time()}
        for _tentativa in (1, 2):
            try:
                fd = os.open(self.caminho, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                atual = self._ler()
                self._recusa_ocupada(atual)          # levanta se viva/nao mensuravel/ilegivel
                # Lock MORTO: so retoma se o conteudo nao mudou entre a leitura e a remocao
                # (nunca apaga lock de terceiro que acabou de nascer).
                if self._ler() != atual:
                    raise FrenteOcupada("lock %s mudou durante a retomada: RECUSADO"
                                        % self.caminho)
                try:
                    os.remove(self.caminho)
                except OSError as erro:
                    raise FrenteOcupada("nao deu para remover lock morto %s: %s"
                                        % (self.caminho, erro))
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(doc, fh)
            self.obtida = True
            return {"ok": True, "caminho": self.caminho, "pid": self.pid, "token": self.token}
        raise FrenteOcupada("frente unica disputada em %s: RECUSADO apos retomada de lock morto"
                            % self.caminho)

    def liberar(self):
        """Remove o lock SOMENTE se ainda for o NOSSO (token confere)."""
        if not self.obtida:
            return False
        doc = self._ler()
        if isinstance(doc, dict) and doc.get("token") == self.token:
            try:
                os.remove(self.caminho)
            except OSError:
                pass
            self.obtida = False
            return True
        return False


# ------------------------------------------------------------- espera ----------
def aguardar_passo(fonte, passo, relogio, dormir, intervalo_s, cancelado):
    """Espera MENU/TELA/CONDICAO ate satisfazer, TIMEOUT ou CANCELAMENTO. Diagnostico por passo.

    O orcamento do passo e FINITO e obrigatorio (`timeout_s`); a espera entre leituras e
    limitada ao ORCAMENTO RESTANTE (`min(intervalo_s, restante)`), nunca um sleep cego maior que
    o deadline (F3). O cancelamento e rechecado ANTES e DEPOIS de cada leitura (F8).
    """
    limite = passo.get("timeout_s")
    inicio = relogio()
    tentativas = 0
    ultimo = None

    def _cancelado(motivo):
        return {"estado": CANCELADO, "tentativas": tentativas,
                "decorrido_s": round(relogio() - inicio, 3),
                "observado": (ultimo or {}).get("observado"),
                "diagnostico": motivo}

    def _fechado(erro):
        return {"estado": FALHOU_FECHADO, "tentativas": tentativas,
                "decorrido_s": round(relogio() - inicio, 3), "observado": None,
                "diagnostico": "fonte invalida: %s" % erro}

    while True:
        if cancelado():
            return _cancelado("cancelado pelo chamador durante a espera")
        tentativas += 1
        try:
            ultimo = _consultar(fonte, passo)
        except ConfigInvalida as erro:
            return _fechado(erro)
        if cancelado():
            return _cancelado("cancelado pelo chamador durante a ultima leitura")
        if ultimo["satisfeito"]:
            return {"estado": "SATISFEITO", "tentativas": tentativas,
                    "decorrido_s": round(relogio() - inicio, 3),
                    "observado": ultimo.get("observado"),
                    "diagnostico": ultimo.get("diagnostico") or ""}
        decorrido = relogio() - inicio
        if limite is not None and decorrido >= limite:
            return {"estado": TIMEOUT, "tentativas": tentativas,
                    "decorrido_s": round(decorrido, 3), "observado": ultimo.get("observado"),
                    "diagnostico": ("nao encontrou %s %r em %.3fs (%d tentativas); ultimo: %s"
                                    % (passo["tipo"], passo["alvo"], limite, tentativas,
                                       ultimo.get("diagnostico") or ultimo.get("observado")))}
        espera = intervalo_s
        if limite is not None:
            espera = min(intervalo_s, max(0.0, limite - decorrido))
        if espera > 0:
            dormir(espera)


# ------------------------------------------------------------- executor --------
def _intervalo_valido(intervalo_s):
    """Intervalo de polling: finito e >= 0 (F3)."""
    if isinstance(intervalo_s, bool) or not isinstance(intervalo_s, (int, float)):
        return False
    return math.isfinite(float(intervalo_s)) and float(intervalo_s) >= 0


def executar(plano, fonte, *, autorizacao=None, relogio=None, dormir=None, intervalo_s=0.0,
             cancelado=None, frente=None, perfil_de_teste=None, save_de_teste=None,
             area_trabalho=None, relativos=(), imagem=None, pids_medir=None, pid_vivo=None,
             executar_cmd=None, dir_backup=None, pids_criados=None):
    """Executa o cenario CONHECIDO.

    A frente unica e OBRIGATORIA: sem `frente` explicita o executor adquire a frente padrao
    (`caminho_frente_padrao()`), nunca executa sem lock. O resultado terminal NUNCA e substituido
    pelas fases de cleanup, que rodam isoladas (erros vao para `res["cleanup_erros"]`).
    """
    relogio = relogio or time.monotonic
    dormir = dormir or time.sleep
    cancelado = cancelado or (lambda: False)

    res = {"esquema": ESQUEMA_EXECUTOR, "versao": VERSAO_EXECUTOR, "estado": INATIVO,
           "estados": [INATIVO], "veredito": None, "passos": [], "permissoes": None,
           "ambiente": None, "frente": None, "rollback": None, "encerramento": None,
           "motivo": None, "diagnostico": [], "lacunas": [], "cleanup_erros": [],
           "runtime_exercitado": False}

    def _muda(estado):
        res["estado"] = estado
        res["estados"].append(estado)

    _muda(VALIDANDO)
    try:
        plano = validar_plano_execucao(plano)
    except ConfigInvalida as erro:
        _muda(FALHOU_FECHADO)
        res["motivo"] = "config invalida: %s" % erro
        res["diagnostico"].append(str(erro))
        return _fecha(res)

    if not _intervalo_valido(intervalo_s):
        _muda(FALHOU_FECHADO)
        res["motivo"] = ("intervalo de polling invalido (precisa ser finito e >= 0): %r"
                         % (intervalo_s,))
        res["diagnostico"].append(res["motivo"])
        return _fecha(res)

    try:
        perms = decidir_permissoes(plano, autorizacao)
    except ConfigInvalida as erro:
        _muda(FALHOU_FECHADO)
        res["motivo"] = "autorizacao invalida: %s" % erro
        res["diagnostico"].append(str(erro))
        return _fecha(res)

    res["permissoes"] = perms
    if perms["status"] == FALHOU_FECHADO:
        _muda(FALHOU_FECHADO)
        res["motivo"] = perms["motivo"]
        res["diagnostico"].append(perms["motivo"])
        return _fecha(res)
    if perms["status"] == NAO_EXERCITADO:
        # NADA foi lido/feito: nao adquire frente, nao faz backup, nao le fonte, nao encerra.
        _muda(NAO_EXERCITADO)
        res["motivo"] = perms["motivo"]
        res["diagnostico"].append(perms["motivo"])
        return _fecha(res)
    _muda(PERMISSOES)

    agindo = perms["permite_agir"]
    if agindo:
        amb = verificar_ambiente_de_teste(fonte, perfil_de_teste, save_de_teste)
        res["ambiente"] = amb
        if not amb["ok"]:
            _muda(FALHOU_FECHADO)
            res["motivo"] = "perfil/save de teste nao verificados: %s" % "; ".join(amb["motivos"])
            res["diagnostico"].extend(amb["motivos"])
            return _fecha(res)
    _muda(AMBIENTE)

    if frente is None:
        frente = FrenteUnica(caminho_frente_padrao())
    try:
        res["frente"] = frente.obter()
    except FrenteOcupada as erro:
        _muda(FALHOU_FECHADO)
        res["motivo"] = "frente unica: %s" % erro
        res["diagnostico"].append(str(erro))
        return _fecha(res)
    _muda(FRENTE)

    col = None
    before = after = None
    dirs_antes = dirs_depois = None
    pids_antes = pids_depois = None
    backups = {}
    token = uuid.uuid4().hex
    dir_backup_proprio = False          # F7: so removemos o que ESTA execucao criou
    pids_proprios = set()
    for p in (pids_criados or ()):
        try:
            pids_proprios.add(int(p))
        except (TypeError, ValueError):
            continue
    terminal = False
    try:
        # ---- setup (DENTRO do try: excecao aqui TAMBEM libera a frente no finally, F8)
        if area_trabalho and relativos:
            col = col or coletor()
            before = col.snapshot_arquivos(area_trabalho, relativos)
            dirs_antes = col.snapshot_dirs(area_trabalho, relativos)
            if before:
                if dir_backup is None:
                    dir_backup = tempfile.mkdtemp(prefix="kit11-backup-")
                else:
                    # F7: NUNCA apagar o diretorio do chamador — backup em subdiretorio PROPRIO.
                    dir_backup = os.path.join(dir_backup, ".kit11-backup-%s" % token)
                    os.makedirs(dir_backup, exist_ok=True)
                dir_backup_proprio = True
                for rel in before:
                    origem = os.path.join(area_trabalho, rel)
                    destino = os.path.join(dir_backup, rel)
                    os.makedirs(os.path.dirname(destino) or dir_backup, exist_ok=True)
                    shutil.copy2(origem, destino)
                    backups[rel] = destino
        if imagem and pids_medir:
            pids_antes = pids_medir(imagem)

        # ---- execucao dos passos
        quebrou = False
        for passo in plano["passos"]:
            rec = {"nome": passo["nome"], "tipo": passo["tipo"], "alvo": passo["alvo"],
                   "requer_acao": passo["requer_acao"], "estado": None, "tentativas": 0,
                   "decorrido_s": 0.0, "observado": None, "diagnostico": None}
            if passo["requer_acao"] and not agindo:
                rec["estado"] = FALHOU_FECHADO
                rec["diagnostico"] = "passo ativo sem autorizacao separada (observacao != acao)"
                res["passos"].append(rec)
                _muda(FALHOU_FECHADO)
                res["motivo"] = rec["diagnostico"]
                terminal = True
                quebrou = True
                break
            _muda(AGUARDANDO)
            rec.update(aguardar_passo(fonte, passo, relogio, dormir, intervalo_s, cancelado))
            res["passos"].append(rec)
            if rec["estado"] == CANCELADO:
                _muda(CANCELADO)
                res["motivo"] = "cancelado durante o passo %r" % passo["nome"]
                res["diagnostico"].append(rec["diagnostico"] or res["motivo"])
                terminal = True
                quebrou = True
                break
            if rec["estado"] == TIMEOUT:
                _muda(TIMEOUT)
                res["motivo"] = "timeout no passo %r" % passo["nome"]
                res["diagnostico"].append(rec["diagnostico"] or res["motivo"])
                terminal = True
                quebrou = True
                break
            if rec["estado"] == FALHOU_FECHADO:
                _muda(FALHOU_FECHADO)
                res["motivo"] = "passo %r: %s" % (passo["nome"], rec["diagnostico"])
                res["diagnostico"].append(rec["diagnostico"] or res["motivo"])
                terminal = True
                quebrou = True
                break
        if not quebrou:
            _muda(CONCLUIDO)
            terminal = True
    except Exception as erro:
        # Falha NAO estruturada virou falha ESTRUTURADA (nunca escapa nem mascara o estado).
        res["cleanup_erros"].append("execucao: %s: %s" % (type(erro).__name__, erro))
        res["diagnostico"].append("excecao durante a execucao: %s: %s"
                                  % (type(erro).__name__, erro))
        if not terminal:
            _muda(FALHOU_FECHADO)
            res["motivo"] = "excecao durante a execucao: %s: %s" % (type(erro).__name__, erro)
            terminal = True
    finally:
        # F6/F8: ROLLBACK EXATO da area de trabalho — FASE ISOLADA, NAO muda o veredito.
        if area_trabalho and relativos and before is not None:
            try:
                col = col or coletor()
                after = col.snapshot_arquivos(area_trabalho, relativos)
                dirs_depois = col.snapshot_dirs(area_trabalho, relativos)
                plano_rb = col.planejar_rollback(before, after, dirs_antes, dirs_depois)
                acoes = col.executar_rollback(area_trabalho, plano_rb, backups)
                residuo = None
                if hasattr(col, "verificar_sem_residuo"):
                    residuo = col.verificar_sem_residuo(area_trabalho, relativos, before,
                                                        dirs_antes)
                res["rollback"] = {"plano": plano_rb, "acoes": acoes, "residuo": residuo}
            except Exception as erro:
                res["cleanup_erros"].append("rollback: %s: %s" % (type(erro).__name__, erro))

        # F5: ENCERRAMENTO — so PIDs PROPRIOS, com autorizacao de acao e liveness mensuravel.
        if imagem:
            try:
                col = col or coletor()
                pids_depois = pids_medir(imagem) if pids_medir else None
                plano_enc = col.planejar_encerramento(imagem, pids_antes, pids_depois)
                plano_enc["pids_criados_por_esta_execucao"] = sorted(pids_proprios)
                if plano_enc.get("pids"):
                    # delta NAO e propriedade: so fechamos o que ESTA execucao criou.
                    plano_enc["pids"] = [p for p in plano_enc["pids"] if p in pids_proprios]
                if not agindo:
                    plano_enc["modo"] = "recusado-sem-autorizacao-de-acao"
                    plano_enc["recusado"] = True
                    plano_enc["pids"] = []
                    plano_enc["motivo"] = ("encerramento exige autorizacao de ACAO "
                                           "(ativa_autorizada): observacao NAO encerra")
                elif not plano_enc.get("pids"):
                    plano_enc["modo"] = "nada-de-propriedade"
                    plano_enc["motivo"] = ("nenhum PID criado por esta execucao: nada a encerrar "
                                           "(delta de PIDs nao e propriedade)")
                else:
                    medir = pid_vivo or (lambda p: col._pid_vivo(p))
                    if any(medir(p) is None for p in plano_enc["pids"]):
                        plano_enc["modo"] = "recusado-sem-medicao"
                        plano_enc["recusado"] = True
                        plano_enc["pids"] = []
                        plano_enc["motivo"] = ("liveness NAO mensuravel: RECUSADO (nunca escala "
                                               "forca na duvida)")
                acoes = col.encerrar_processos(plano_enc, executar=executar_cmd,
                                               pid_vivo=pid_vivo)
                res["encerramento"] = {"plano": plano_enc, "acoes": acoes}
            except Exception as erro:
                res["cleanup_erros"].append("encerramento: %s: %s" % (type(erro).__name__, erro))

        # libera a frente (so se for a nossa) — SEMPRE, mesmo com erro acima.
        try:
            res["frente_liberada"] = frente.liberar()
        except Exception as erro:
            res["cleanup_erros"].append("liberar frente: %s: %s" % (type(erro).__name__, erro))

        # limpa SOMENTE o diretorio de backup PROPRIO (o do chamador fica intacto, F7).
        if dir_backup and dir_backup_proprio:
            try:
                shutil.rmtree(dir_backup, ignore_errors=True)
            except Exception as erro:
                res["cleanup_erros"].append("limpar backup: %s: %s" % (type(erro).__name__, erro))

    res["runtime_exercitado"] = False        # offline: nenhuma leitura de jogo nesta rodada
    res["lacunas"].append("navegacao real/clique fisico: KIT-14 (apos KIT-G2)")
    return _fecha(res)


def _fecha(res):
    res["veredito"] = ESTADO_DO_VEREDITO.get(res["estado"], res["estado"])
    if res["estado"] == CONCLUIDO and res.get("permissoes") \
            and not res["permissoes"]["permite_agir"]:
        res["veredito"] = VEREDITO_OBSERVADO
    return res


# ------------------------------------------------------------- CLI -------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-11 — executor deterministico (offline).")
    ap.add_argument("--plano", required=True, help="JSON do plano de execucao")
    ap.add_argument("--estado", help="JSON de estado para a FonteDeArquivo (offline)")
    ap.add_argument("--saida", help="grava o resultado JSON")
    ap.add_argument("--frente", help="caminho do lock da frente unica (default: %s)"
                                     % caminho_frente_padrao())
    args = ap.parse_args(argv)

    try:
        with open(args.plano, encoding="utf-8") as fh:
            plano = json.load(fh)
    except Exception as erro:
        print("ERRO: plano ilegivel (%s: %s) — NAO_EXERCITADO" % (type(erro).__name__, erro))
        return 2
    fonte = FonteDeArquivo(args.estado) if args.estado else None
    if fonte is None:
        print("ERRO: sem --estado nao ha fonte; este executor nao improvisa leitura (fail-closed)")
        return 2
    frente = FrenteUnica(args.frente) if args.frente else None
    res = executar(plano, fonte, frente=frente)
    texto = json.dumps(res, indent=2, ensure_ascii=False)
    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as fh:
            fh.write(texto)
    print(texto)
    veredito = res["veredito"]
    if veredito in (VEREDITO_PASSOU, VEREDITO_OBSERVADO):
        return 0
    if veredito == VEREDITO_NAO_EXERCITADO:
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
