#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""observacao_passiva.py - KIT-05F: observacao PASSIVA e captura por eventos (RSTV).

ESCOPO
------
Estende a coleta pontual (AUT-4 / CAP-1 / Core KIT-04) para OBSERVAR uma sessao
autorizada enquanto o humano joga, com o PRIMEIRO conjunto de eventos RSTV:

  * `clique_recebido`        - um clique FOI RECEBIDO pelo jogo (so observacao);
  * `janela_aberta`          - uma janela de fato abriu;
  * `janela_fechada`         - uma janela de fato fechou;
  * `tooltip`                - um tooltip apareceu / foi restaurado;
  * `falha_clique_sem_janela`- clique recebido SEM janela dentro do timeout
                               (evento DERIVADO, com motivo + timeout).

MODO PASSIVO (trava dura)
-------------------------
O modulo so aceita TIPOS OBSERVADOS. Qualquer tipo ATIVO (clique emitido, save,
equipar, modificacao, acao) e REJEITADO e registrado como degradacao explicita.
Nada aqui clica, salva, equipa ou modifica o jogo.

HONESTIDADE (correcoes KIT-05F F1-F6)
-------------------------------------
* F1 - PEDIDO != CAPTURA. `registrar_captura` apenas REGISTRA UM PEDIDO
  (`estado="solicitada"`); ele NUNCA marca `captura_apos_atualizacao_visual`.
  A confirmacao exige `confirmar_captura` com evento existente, sessao/evento
  coincidentes, ARQUIVO PNG REAL em disco, quadro estritamente POSTERIOR ao
  quadro do evento e hash SHA256 do arquivo. Sem isso, sai degradacao explicita
  (`captura_sem_png_real`/`captura_quadro_nao_posterior`/...) — nunca "pixels
  provados". `simultaneidade_afirmada` e sempre False.
* F2 - PAUSA. Em pausa, `registrar`, `registrar_captura`, `confirmar_captura` e
  `verificar_timeouts` sao barrados. Ao pausar, as pendencias cujo intervalo
  perdeu observacao sao INVALIDADAS com lacuna explicita (`lacunas`) e NAO viram
  falha de timeout ao retomar (observacao interrompida nao e evidencia de
  "clique sem janela").
* F3 - DEDUP POR FONTE. O estado e lembrado POR FONTE (janela/contexto) e nao
  globalmente: janelas distintas com dados iguais coexistem, abrir->fechar->
  reabrir sobrevive e estados intercalados constantes nao geram spam.
  `clique_recebido` continua DISCRETO (cada clique e um fato novo).
* F4 - LIMITES. TODO estado auxiliar (degradacoes, rejeitados, pendentes,
  memoria de dedup, pedidos de captura, capturas por evento, lacunas) tem limite
  explicito proprio (`limite_aux`, sobrescrivel) com contadores AGREGADOS de
  descarte por motivo; eviccao/expirencia limpam referencias orfas.
* F5 - TIMEOUT. A janela so resolve a pendencia DENTRO do prazo registrado.
  Vencimentos sao materializados (motivo + clique_id + janela + timeout reais)
  ANTES de processar uma abertura tardia, e a abertura tardia nao apaga o
  historico de timeout.
* F6 - REPLAY. `_correr_entradas` devolve o ESTADO RETIDO (mesma politica de
  fila/retencao), nunca listas paralelas ilimitadas; o export do CLI e coerente
  com os totais e rotulado como fixture/offline (`runtime=NAO_EXERCITADO`).

O runtime em jogo (emissao real pelo Core C#) NAO e exercitado aqui: este modulo
e a LOGICA do pipeline, provada por testes offline reais.
"""
import argparse
import collections
import hashlib
import json
import os
import sys
import time
import uuid

ESQUEMA = "KIT-05F/observacao-passiva/2"

# Primeiro conjunto de eventos RSTV OBSERVADOS (passivos por natureza).
CLIQUE_RECEBIDO = "clique_recebido"
JANELA_ABERTA = "janela_aberta"
JANELA_FECHADA = "janela_fechada"
TOOLTIP = "tooltip"
# Evento DERIVADO (o pipeline o gera; o observador nao o envia).
FALHA_CLIQUE_SEM_JANELA = "falha_clique_sem_janela"

TIPOS_OBSERVADOS = (CLIQUE_RECEBIDO, JANELA_ABERTA, JANELA_FECHADA, TOOLTIP)

# Tipos ATIVOS proibidos no modo passivo (clique/save/equipamento/modificacao).
TIPOS_ATIVOS = frozenset((
    "clique_emitido", "click_emitido", "emitir_clique",
    "save", "salvar", "save_game", "carregar_save",
    "equipar", "equipamento", "desequipar",
    "modificacao", "mutacao", "action_triggered", "acao_executada",
))

# Chaves de dados que denunciam ACAO (nao observacao) — rejeitadas em modo passivo.
CHAVES_ATIVAS = frozenset((
    "acao_executada", "clique_emitido", "salvou", "equipou", "modificou",
    "escrita", "mutou", "aplicou",
))

# Fonte de contexto usada quando o evento nao traz janela explicita.
FONTE_GLOBAL = "<global>"

# Estados possiveis de uma solicitacao de captura.
CAPTURA_SOLICITADA = "solicitada"
CAPTURA_CONFIRMADA = "confirmada"
CAPTURA_NAO_CONFIRMADA = "nao_confirmada"


class ErroObservacaoPassiva(ValueError):
    """Entrada invalida (uso incorreto do modulo, nao evento do jogo)."""


def _ms(relogio):
    """Le o relogio injetavel (ms). Default: monotonic em ms."""
    if relogio is None:
        return int(time.monotonic() * 1000)
    return int(relogio())


def _assinatura(tipo, dados, janela):
    """Assinatura de ESTADO (F3): tipo + janela + dados relevantes ordenados."""
    itens = tuple(sorted(
        (str(k), repr(v)) for k, v in (dados or {}).items()
        if k not in ("quadro", "captura", "ts_ms")
    ))
    return (tipo, janela, itens)


def _sha256_arquivo(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


class ObservacaoPassiva(object):
    """Pipeline de observacao passiva: dedup por fonte, fila, retencao, teto,
    pausa, timeout e captura em duas fases (pedido -> confirmacao)."""

    def __init__(self, fila_max=200, retencao_max=500, retencao_ms=60000,
                 teto_capturas=10, timeout_janela_ms=1500,
                 id_sessao=None, relogio=None, limite_aux=None,
                 fonte="offline-fixture"):
        if fila_max < 1 or retencao_max < 1:
            raise ErroObservacaoPassiva("fila_max e retencao_max precisam ser >= 1")
        if teto_capturas < 0:
            raise ErroObservacaoPassiva("teto_capturas nao pode ser negativo")
        # F4: limite explicito de TODO estado auxiliar. Default: o teto de
        # retencao declarado (finito) — pode ser sobrescrito pelo chamador.
        if limite_aux is None:
            limite_aux = retencao_max
        if limite_aux < 1:
            raise ErroObservacaoPassiva("limite_aux precisa ser >= 1")
        self.fila_max = int(fila_max)
        self.retencao_max = int(retencao_max)
        self.retencao_ms = int(retencao_ms)
        self.teto_capturas = int(teto_capturas)
        self.timeout_janela_ms = int(timeout_janela_ms)
        self.limite_aux = int(limite_aux)
        self.id_sessao = id_sessao or ("sessao-" + uuid.uuid4().hex[:8])
        self._relogio = relogio
        self.fonte = fonte

        self.modo = "passivo"
        self._pausado = False
        # ---- estado retido (TODO limitado) ----
        self._eventos = []          # fila (mais antigo primeiro)
        self._degradacoes = []
        self._rejeitados = []
        self._ultimo_estado = collections.OrderedDict()   # F3: fonte -> assinatura
        self._pendentes = collections.OrderedDict()       # clique_id -> pendencia
        self._pedidos = collections.OrderedDict()         # captura_id -> pedido
        self._captura_por_evento = collections.OrderedDict()  # evento_id -> captura
        self._lacunas = []
        self._falhas_materializadas = []
        # ---- contadores agregados (nao crescem em memoria) ----
        self._capturas_solicitadas = 0
        self._capturas_confirmadas = 0
        self._capturas_recusadas = 0
        self._degradacoes_total = 0
        self._degradacoes_descartadas = 0
        self._rejeitados_total = 0
        self._rejeitados_descartados = 0
        self._pendentes_descartados = 0
        self._estados_descartados = 0
        self._lacunas_total = 0
        self._contagem_degradacoes = collections.Counter()
        self._contagem_rejeitados = collections.Counter()
        self._quadros = 0           # contador de quadros observados

    # --------------------------------------------------------------- helpers ---
    def _agora(self):
        return _ms(self._relogio)

    def _degrada(self, motivo, tipo=None, detalhe=None):
        """Registra degradacao com teto (F4) + contador agregado por motivo."""
        self._degradacoes_total += 1
        self._contagem_degradacoes[motivo] += 1
        item = {
            "motivo": motivo,
            "tipo": tipo,
            "ts_ms": self._agora(),
            "sessao": self.id_sessao,
        }
        if detalhe:
            item["detalhe"] = detalhe
        self._degradacoes.append(item)
        while len(self._degradacoes) > self.limite_aux:
            self._degradacoes.pop(0)
            self._degradacoes_descartadas += 1
        return item

    def _rejeita(self, tipo, motivo, **extra):
        """Rejeicao com teto (F4) + contador agregado."""
        self._rejeitados_total += 1
        self._contagem_rejeitados[motivo] += 1
        item = {"tipo": tipo, "motivo": motivo, "ts_ms": self._agora(),
                "sessao": self.id_sessao}
        item.update(extra)
        self._rejeitados.append(item)
        while len(self._rejeitados) > self.limite_aux:
            self._rejeitados.pop(0)
            self._rejeitados_descartados += 1
        return item

    def _lembra_estado(self, fonte, assinatura):
        """Memoria de dedup por fonte (F3) com teto LRU (F4)."""
        if fonte in self._ultimo_estado:
            del self._ultimo_estado[fonte]
        self._ultimo_estado[fonte] = assinatura
        while len(self._ultimo_estado) > self.limite_aux:
            self._ultimo_estado.popitem(last=False)
            self._estados_descartados += 1

    def _descarta_referencias(self, evento_id):
        """F4: eviccao/expirencia nao deixam referencia orfa de captura."""
        self._captura_por_evento.pop(evento_id, None)
        for cid, ped in list(self._pedidos.items()):
            if ped.get("evento_id") == evento_id:
                del self._pedidos[cid]

    def _enfileira(self, evento):
        """Fila limitada + retencao por tamanho (o mais antigo sai primeiro)."""
        self._eventos.append(evento)
        while len(self._eventos) > self.fila_max:
            sai = self._eventos.pop(0)
            self._descarta_referencias(sai["id"])
            self._degrada("fila_cheia", tipo=sai.get("tipo"),
                          detalhe="fila_max=%d" % self.fila_max)
        if len(self._eventos) > self.retencao_max:
            for sai in self._eventos[:-self.retencao_max]:
                self._descarta_referencias(sai["id"])
            self._eventos = self._eventos[-self.retencao_max:]

    def _adiciona_pendente(self, clique_id, janela, prazo_ms):
        """Pendencia de janela com teto (F4)."""
        self._pendentes[clique_id] = {"janela": janela, "prazo_ms": prazo_ms}
        while len(self._pendentes) > self.limite_aux:
            cid, pend = self._pendentes.popitem(last=False)
            self._pendentes_descartados += 1
            self._degrada("pendente_descartado", tipo=CLIQUE_RECEBIDO,
                          detalhe="clique_id=%s janela=%s" % (cid, pend.get("janela")))

    # ------------------------------------------------------------------ API ----
    def pausar(self):
        """F2: pausa segura. Invalida pendencias de intervalo NAO observado."""
        if not self._pausado:
            agora = self._agora()
            self._pausado = True
            self._degrada("pausado", detalhe="pausa segura iniciada")
            invalidadas = list(self._pendentes.keys())
            self._pendentes.clear()
            if invalidadas:
                self._lacunas_total += 1
                self._lacunas.append({
                    "inicio_ms": agora, "fim_ms": None, "motivo": "pausa",
                    "pendencias_invalidadas": invalidadas,
                })
                while len(self._lacunas) > self.limite_aux:
                    self._lacunas.pop(0)
                self._degrada(
                    "observacao_interrompida", tipo=CLIQUE_RECEBIDO,
                    detalhe="%d pendencia(s) invalidada(s) por pausa; intervalo nao "
                            "observado (sem falha de timeout)" % len(invalidadas))
        return self._pausado

    def retomar(self):
        if self._pausado:
            self._pausado = False
            for lac in reversed(self._lacunas):
                if lac["fim_ms"] is None:
                    lac["fim_ms"] = self._agora()
                    break
        return self._pausado

    def esta_pausado(self):
        return self._pausado

    def lacunas(self):
        return [dict(l) for l in self._lacunas]

    def registrar(self, tipo, dados=None, janela=None, quadro=None):
        """Registra um evento OBSERVADO. Devolve o evento, ou None se barrado.

        Barrado (sempre com degradacao/rejeicao explicita, nunca silencioso):
          * pausa ativa            -> degradacao `pausado`;
          * tipo ATIVO             -> rejeitado `tipo_ativo`;
          * tipo desconhecido      -> rejeitado `tipo_desconhecido`;
          * chave de ACAO nos dados-> rejeitado `dado_ativo`;
          * estado repetido DA FONTE -> dedup `sem_mudanca` (nao e evento novo).
        """
        dados = dict(dados or {})
        agora = self._agora()

        if self._pausado:
            self._degrada("pausado", tipo=tipo, detalhe="entrada descartada em pausa")
            return None

        if tipo in TIPOS_ATIVOS:
            self._rejeita(tipo, "tipo_ativo")
            self._degrada("tipo_ativo", tipo=tipo,
                          detalhe="modo passivo nao emite acao")
            return None
        if tipo not in TIPOS_OBSERVADOS:
            self._rejeita(tipo, "tipo_desconhecido")
            self._degrada("tipo_desconhecido", tipo=tipo,
                          detalhe="fora do primeiro conjunto de eventos RSTV")
            return None
        ativas = sorted(k for k in dados if k in CHAVES_ATIVAS)
        if ativas:
            self._rejeita(tipo, "dado_ativo", chaves=ativas)
            self._degrada("dado_ativo", tipo=tipo,
                          detalhe="chaves de acao: %s" % ",".join(ativas))
            return None

        # F3 - Deduplicacao POR FONTE: o mesmo ESTADO repetido NAQUELA fonte nao
        # vira evento novo. `clique_recebido` e DISCRETO (cada clique e um fato).
        fonte = janela if janela is not None else FONTE_GLOBAL
        assinatura = _assinatura(tipo, dados, janela)
        if tipo != CLIQUE_RECEBIDO:
            if self._ultimo_estado.get(fonte) == assinatura:
                self._degrada("sem_mudanca", tipo=tipo,
                              detalhe="estado repetido na fonte %s (dedup por mudanca)"
                                      % fonte)
                return None
            self._lembra_estado(fonte, assinatura)

        self._quadros += 1
        evento = {
            "esquema": ESQUEMA,
            "id": uuid.uuid4().hex,
            "sessao": self.id_sessao,
            "tipo": tipo,
            "ts_ms": agora,
            "dados": dados,
            "quadro": {
                "indice": self._quadros if quadro is None else quadro,
                "captura_solicitada": False,
                "solicitacao_id": None,
                "captura_apos_atualizacao_visual": False,
                "captura_id": None,
                "captura_sha256": None,
                "simultaneidade_afirmada": False,
                "nota": "PEDIDO de captura nao e captura; a confirmacao exige PNG "
                        "real posterior ao evento. Simultaneidade nao e afirmada.",
            },
        }
        if janela is not None:
            evento["janela"] = janela

        # Espera de janela: um clique com `janela` fica PENDENTE por timeout.
        if tipo == CLIQUE_RECEBIDO and janela is not None:
            self._adiciona_pendente(evento["id"], janela,
                                    agora + self.timeout_janela_ms)
        elif tipo == JANELA_ABERTA and janela is not None:
            self._processa_abertura(janela, agora)

        self._enfileira(evento)
        return evento

    def _processa_abertura(self, janela, agora):
        """F5: materializa vencimentos ANTES de processar a abertura.

        Uma abertura TARDIA (depois do prazo) nao apaga o historico: a pendencia
        vencida e materializada como falha e a abertura fica registrada como
        ``janela_tardia_sem_resolucao`` (nao resolve nada).
        """
        tardias = [cid for cid, pend in self._pendentes.items()
                   if pend["janela"] == janela and agora > pend["prazo_ms"]]
        if tardias:
            self._degrada("janela_tardia_sem_resolucao", tipo=JANELA_ABERTA,
                          detalhe="janela=%s abertura depois do prazo; "
                                  "%d pendencia(s) vencida(s)"
                                  % (janela, len(tardias)))
        self._materializar_vencidos(agora)
        self._resolve_janela(janela, agora)

    def _resolve_janela(self, janela, agora):
        """Resolve os cliques pendentes DAQUELA janela SOMENTE dentro do prazo."""
        for cid, pend in list(self._pendentes.items()):
            if pend["janela"] != janela:
                continue
            if agora <= pend["prazo_ms"]:
                del self._pendentes[cid]
            else:
                # Abertura tardia NAO apaga o vencimento (F5): a pendencia
                # permanece e sera materializada como falha.
                self._degrada("janela_tardia_sem_resolucao", tipo=JANELA_ABERTA,
                              detalhe="janela=%s clique_id=%s (abertura depois do "
                                      "prazo)" % (janela, cid))

    def _materializar_vencidos(self, agora):
        """Cria `falha_clique_sem_janela` para pendencias vencidas (F5)."""
        criados = 0
        for cid, pend in list(self._pendentes.items()):
            if agora < pend["prazo_ms"]:
                continue
            evento = {
                "esquema": ESQUEMA,
                "id": uuid.uuid4().hex,
                "sessao": self.id_sessao,
                "tipo": FALHA_CLIQUE_SEM_JANELA,
                "ts_ms": agora,
                "dados": {
                    "clique_id": cid,
                    "janela_alvo": pend["janela"],
                    "motivo": "clique recebido sem janela dentro do timeout",
                    "timeout_ms": self.timeout_janela_ms,
                    "prazo_ms": pend["prazo_ms"],
                },
                "quadro": {
                    "indice": self._quadros,
                    "captura_solicitada": False,
                    "solicitacao_id": None,
                    "captura_apos_atualizacao_visual": False,
                    "captura_id": None,
                    "captura_sha256": None,
                    "simultaneidade_afirmada": False,
                    "nota": "falha observada apos o timeout; sem simultaneidade "
                            "afirmada",
                },
            }
            del self._pendentes[cid]
            self._enfileira(evento)
            self._falhas_materializadas.append(evento)
            criados += 1
            while len(self._falhas_materializadas) > self.limite_aux:
                self._falhas_materializadas.pop(0)
        return criados

    def verificar_timeouts(self):
        """Entrega as falhas de timeout materializadas (F2: em pausa, nada).

        Devolve a lista de eventos de falha criados. Cada falha carrega
        `motivo`, `timeout_ms`, `prazo_ms` e aponta o `clique_id` de origem.
        """
        if self._pausado:
            self._degrada("pausado", detalhe="verificar_timeouts barrado em pausa")
            return []
        self._materializar_vencidos(self._agora())
        criados = self._falhas_materializadas
        self._falhas_materializadas = []
        return criados

    # ------------------------------------------------------------- captura -----
    def registrar_captura(self, evento_id, caminho=None, indice_quadro=None):
        """F1: registra um PEDIDO de captura PNG para um evento (duas fases).

        Devolve o pedido (`estado="solicitada"`) ou None. NAO marca
        `captura_apos_atualizacao_visual`: pedido nunca equivale a captura
        confirmada. Recusa: evento inexistente, pausa, teto de capturas e
        `indice_quadro` anterior ao quadro do evento.
        """
        evento = self._por_id(evento_id)
        if evento is None:
            self._capturas_recusadas += 1
            self._degrada("captura_evento_inexistente", detalhe=str(evento_id))
            return None
        if self._pausado:
            self._capturas_recusadas += 1
            self._degrada("pausado", tipo=evento.get("tipo"),
                          detalhe="pedido de captura barrado em pausa "
                                  "(intervalo nao observado)")
            return None
        if self._capturas_solicitadas >= self.teto_capturas:
            self._capturas_recusadas += 1
            self._degrada("teto_capturas_atingido", tipo=evento.get("tipo"),
                          detalhe="teto_capturas=%d" % self.teto_capturas)
            return None
        indice_evento = int(evento["quadro"]["indice"])
        if indice_quadro is not None and int(indice_quadro) < indice_evento:
            self._capturas_recusadas += 1
            self._degrada("captura_quadro_anterior", tipo=evento.get("tipo"),
                          detalhe="quadro pedido=%s anterior ao evento=%s"
                                  % (indice_quadro, indice_evento))
            return None

        self._capturas_solicitadas += 1
        captura_id = "cap-" + uuid.uuid4().hex[:8]
        pedido = {
            "captura_id": captura_id,
            "evento_id": evento_id,
            "sessao": self.id_sessao,
            "caminho": caminho,
            "indice_quadro": indice_quadro,
            "estado": CAPTURA_SOLICITADA,
            "apos_atualizacao_visual": False,
            "simultaneidade_afirmada": False,
            "ts_ms": self._agora(),
        }
        self._pedidos[captura_id] = pedido
        while len(self._pedidos) > self.limite_aux:
            cid, velho = self._pedidos.popitem(last=False)
            if velho.get("estado") == CAPTURA_SOLICITADA:
                self._degrada("pedido_captura_descartado", detalhe=cid)
        evento["quadro"]["captura_solicitada"] = True
        evento["quadro"]["solicitacao_id"] = captura_id
        return pedido

    def confirmar_captura(self, captura_id, caminho=None, indice_quadro=None,
                          hash_=None, evento_id=None, sessao=None):
        """F1: CONFIRMA a captura com evidencia real; sem isso, nada confirmado.

        Exige: pedido existente; nao pausado; sessao/evento coincidentes; PNG
        real em disco; quadro ESTRITAMENTE posterior ao quadro do evento; hash
        SHA256 do arquivo igual ao declarado (quando declarado). Devolve o dict
        da captura confirmada, ou None (com degradacao explicita).
        """
        pedido = self._pedidos.get(captura_id)
        if pedido is None:
            self._capturas_recusadas += 1
            self._degrada("confirmacao_sem_pedido", detalhe=str(captura_id))
            return None
        if self._pausado:
            self._capturas_recusadas += 1
            self._degrada("pausado", detalhe="confirmacao de captura barrada em pausa")
            return None
        if sessao is not None and sessao != self.id_sessao:
            self._capturas_recusadas += 1
            self._degrada("captura_sessao_divergente",
                          detalhe="pedido=%s recebido=%s" % (self.id_sessao, sessao))
            return None
        if evento_id is not None and evento_id != pedido["evento_id"]:
            self._capturas_recusadas += 1
            self._degrada("captura_evento_divergente",
                          detalhe="pedido=%s recebido=%s"
                                  % (pedido["evento_id"], evento_id))
            return None
        evento = self._por_id(pedido["evento_id"])
        if evento is None:
            self._capturas_recusadas += 1
            self._degrada("captura_evento_inexistente",
                          detalhe=str(pedido["evento_id"]))
            return None

        caminho = caminho if caminho is not None else pedido.get("caminho")
        if not caminho or not os.path.isfile(caminho):
            self._capturas_recusadas += 1
            pedido["estado"] = CAPTURA_NAO_CONFIRMADA
            self._degrada("captura_sem_png_real", tipo=evento.get("tipo"),
                          detalhe="sem arquivo PNG em %s" % (caminho,))
            return None
        try:
            sha = _sha256_arquivo(caminho)
        except OSError as exc:
            self._capturas_recusadas += 1
            pedido["estado"] = CAPTURA_NAO_CONFIRMADA
            self._degrada("captura_ilegivel", tipo=evento.get("tipo"),
                          detalhe="%s: %s" % (caminho, exc))
            return None
        if hash_ is not None and hash_.lower() != sha:
            self._capturas_recusadas += 1
            pedido["estado"] = CAPTURA_NAO_CONFIRMADA
            self._degrada("captura_hash_divergente", tipo=evento.get("tipo"),
                          detalhe="declarado=%s medido=%s" % (hash_, sha))
            return None
        ind = indice_quadro if indice_quadro is not None else pedido.get("indice_quadro")
        indice_evento = int(evento["quadro"]["indice"])
        if ind is None or int(ind) <= indice_evento:
            self._capturas_recusadas += 1
            pedido["estado"] = CAPTURA_NAO_CONFIRMADA
            self._degrada("captura_quadro_nao_posterior", tipo=evento.get("tipo"),
                          detalhe="quadro=%s evento=%s (exige > evento)"
                                  % (ind, indice_evento))
            return None

        captura = {
            "captura_id": captura_id,
            "evento_id": pedido["evento_id"],
            "sessao": self.id_sessao,
            "caminho": caminho,
            "caminho_absoluto": os.path.abspath(caminho),
            "indice_quadro": int(ind),
            "indice_quadro_evento": indice_evento,
            "apos_atualizacao_visual": True,
            "sha256": sha,
            "tamanho_bytes": os.path.getsize(caminho),
            "simultaneidade_afirmada": False,
            "estado": CAPTURA_CONFIRMADA,
            "ts_ms": self._agora(),
        }
        pedido["estado"] = CAPTURA_CONFIRMADA
        evento["quadro"]["captura_apos_atualizacao_visual"] = True
        evento["quadro"]["captura_id"] = captura_id
        evento["quadro"]["captura_sha256"] = sha
        self._captura_por_evento[pedido["evento_id"]] = captura
        while len(self._captura_por_evento) > self.limite_aux:
            self._captura_por_evento.popitem(last=False)
        self._capturas_confirmadas += 1
        del self._pedidos[captura_id]
        return captura

    def captura_de(self, evento_id):
        """Captura CONFIRMADA daquele evento (pedido nao conta como captura)."""
        return self._captura_por_evento.get(evento_id)

    def pedido_de(self, captura_id):
        return self._pedidos.get(captura_id)

    def pedidos_retidos(self):
        """F4: quantos pedidos de captura estao retidos (limitado)."""
        return len(self._pedidos)

    def capturas_retidas(self):
        """F4: quantas capturas confirmadas estao retidas (limitado)."""
        return len(self._captura_por_evento)

    # ------------------------------------------------------------- expiracao ---
    def expirar(self):
        """Aplica retencao (idade + tamanho) e limpa referencias orfas (F4)."""
        agora = self._agora()
        antes = len(self._eventos)
        if self.retencao_ms > 0:
            self._eventos = [e for e in self._eventos
                             if agora - e["ts_ms"] < self.retencao_ms]
        if len(self._eventos) > self.retencao_max:
            self._eventos = self._eventos[-self.retencao_max:]
        vivos = {e["id"] for e in self._eventos}
        for eid in list(self._captura_por_evento.keys()):
            if eid not in vivos:
                del self._captura_por_evento[eid]
        for cid, ped in list(self._pedidos.items()):
            if ped["evento_id"] not in vivos:
                del self._pedidos[cid]
        removidos = antes - len(self._eventos)
        if removidos and self.retencao_ms > 0:
            self._degrada("retencao", detalhe="%d evento(s) expirado(s)" % removidos)
        return removidos

    # ---------------------------------------------------------------- leitura --
    def _por_id(self, evento_id):
        for e in self._eventos:
            if e["id"] == evento_id:
                return e
        return None

    def eventos(self):
        return [dict(e) for e in self._eventos]

    def degradacoes(self):
        return [dict(d) for d in self._degradacoes]

    def rejeitados(self):
        return [dict(r) for r in self._rejeitados]

    def pausado(self):
        return self._pausado

    def resumo(self):
        por_tipo = {}
        for e in self._eventos:
            por_tipo[e["tipo"]] = por_tipo.get(e["tipo"], 0) + 1
        return {
            "esquema": ESQUEMA,
            "sessao": self.id_sessao,
            "modo": self.modo,
            "fonte": self.fonte,
            "runtime": "NAO_EXERCITADO",
            "runtime_exercitado": False,
            "pausado": self._pausado,
            "eventos_total": len(self._eventos),
            "eventos_por_tipo": por_tipo,
            # "capturas" e LEGADO: conta SOLICITACOES, nunca confirmacao de PNG.
            "capturas": self._capturas_solicitadas,
            "capturas_solicitadas": self._capturas_solicitadas,
            "capturas_confirmadas": self._capturas_confirmadas,
            "capturas_recusadas": self._capturas_recusadas,
            "teto_capturas": self.teto_capturas,
            "fila_max": self.fila_max,
            "retencao_max": self.retencao_max,
            "retencao_ms": self.retencao_ms,
            "timeout_janela_ms": self.timeout_janela_ms,
            "limite_aux": self.limite_aux,
            "degradacoes": len(self._degradacoes),
            "degradacoes_total": self._degradacoes_total,
            "degradacoes_descartadas": self._degradacoes_descartadas,
            "degradacoes_motivos": sorted(self._contagem_degradacoes),
            "degradacoes_por_motivo": dict(self._contagem_degradacoes),
            "rejeitados": len(self._rejeitados),
            "rejeitados_total": self._rejeitados_total,
            "rejeitados_descartados": self._rejeitados_descartados,
            "rejeitados_por_motivo": dict(self._contagem_rejeitados),
            "pendentes": len(self._pendentes),
            "pendentes_descartados": self._pendentes_descartados,
            "lacunas": len(self._lacunas),
            "lacunas_total": self._lacunas_total,
            "simultaneidade_afirmada": False,
        }


# --------------------------------------------------------------------- CLI -----

class RelogioMutavel(object):
    """Relogio controlavel em ms: permite `{"acao": "avanca", "ms": N}` no roteiro."""

    def __init__(self, inicio=0):
        self.t = int(inicio)

    def avanca(self, ms):
        self.t += int(ms)
        return self.t

    def __call__(self):
        return self.t


def _correr_entradas(entradas, relogio=None, **cfg):
    """Reproduz um roteiro de entradas (lista) no pipeline. Usado pelo CLI/testes.

    F6: devolve (obs, eventos, falhas) onde `eventos` e o ESTADO RETIDO pelo
    pipeline no fim da rodada (mesma politica de fila/retencao) — nao ha lista
    paralela ilimitada. `falhas` sao as falhas de timeout RETIDAS.
    """
    rel = relogio if relogio is not None else RelogioMutavel(0)
    obs = ObservacaoPassiva(relogio=rel, **cfg)
    for ent in entradas:
        tipo = ent.get("tipo")
        acao = ent.get("acao")
        if acao == "avanca":
            rel.avanca(ent.get("ms", 0))
            continue
        if acao == "pausar":
            obs.pausar()
            continue
        if acao == "retomar":
            obs.retomar()
            continue
        if acao == "expiar":
            obs.expirar()
            continue
        if acao == "verificar_timeouts":
            obs.verificar_timeouts()
            continue
        if acao == "capturar":
            obs.registrar_captura(ent.get("evento_id"), caminho=ent.get("caminho"),
                                  indice_quadro=ent.get("indice_quadro"))
            continue
        if acao == "confirmar":
            obs.confirmar_captura(ent.get("captura_id"), caminho=ent.get("caminho"),
                                  indice_quadro=ent.get("indice_quadro"),
                                  hash_=ent.get("hash"))
            continue
        obs.registrar(tipo, dados=ent.get("dados"),
                      janela=ent.get("janela"), quadro=ent.get("quadro"))
    eventos = obs.eventos()
    falhas = [e for e in eventos if e.get("tipo") == FALHA_CLIQUE_SEM_JANELA]
    return obs, eventos, falhas


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="KIT-05F: pipeline de observacao passiva (offline).")
    ap.add_argument("--entradas", required=True,
                    help="JSON com a lista de entradas observadas")
    ap.add_argument("--out", help="grava o resumo (JSON) neste arquivo")
    args = ap.parse_args(argv)

    with open(args.entradas, encoding="utf-8") as fh:
        entradas = json.load(fh)
    if isinstance(entradas, dict):
        cfg = entradas.get("config", {})
        entradas = entradas.get("entradas", [])
    else:
        cfg = {}
    obs, eventos, falhas = _correr_entradas(entradas, **cfg)
    resumo = obs.resumo()
    # F6: export coerente com o estado RETIDO; rotulado fixture/offline.
    resumo["origem"] = "fixture-offline (nao e runtime; nao prova pixels nem jogo)"
    resumo["eventos_retidos"] = eventos
    resumo["falhas_retidas"] = falhas
    resumo["degradacoes_lista"] = obs.degradacoes()
    resumo["lacunas_lista"] = obs.lacunas()
    texto = json.dumps(resumo, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto)
    print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
