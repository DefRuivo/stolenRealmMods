#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_acesso.py - KIT-06: plano de CONTROLE de uso SEM TERMINAL.

O que este modulo resolve
-------------------------
Dar ao modder/jogador controles simples, por ATALHO, para usar o instrumento de
observacao (KIT-05F) sem terminal, sem Hermes e sem IA:

  * `observar`        - liga/desliga a observacao PASSIVA (coleta);
  * `pausar`          - pausa / retoma a coleta (delega ao pipeline KIT-05F);
  * `marcar_problema` - MARCACAO MANUAL de um problema, com contexto;
  * `exportar`        - grava o resultado em arquivo local (acessivel sem IA).

Garantias (contrato deste modulo, provadas por teste offline)
-------------------------------------------------------------
1. ATALHOS CONFIGURAVEIS por arquivo (JSON) com validacao: acao desconhecida,
   tecla reservada (chat) e CONFLITO entre atalhos sao RECUSADOS, nunca aceitos
   em silencio.
2. GUARDS de contexto: com chat aberto / digitando, ou com a UI de
   REMAPEAMENTO aberta, ou SEM FOCO no jogo, nenhum atalho dispara (registro de
   degradacao explicita). Isso evita disparar coleta enquanto o humano escreve.
3. SEM FOCO FORCADO e SEM ENCERRAR A SESSAO DO DONO: o modulo nao expoe acao de
   foco e nao fecha o jogo; `parar_observacao` apenas para de coletar.
4. INICIAR OBSERVACAO NUNCA AUTORIZA MODO ATIVO (trava dura): nao existe acao
   ativa e `habilitar_modo_ativo` sempre falha com degradacao. O instrumento e
   passivo por construcao.
5. AUSENCIA DE CONFLITO COM INPUT: o modulo apenas LE o estado das teclas
   (`consome_input=False`); nao suprime, nao reenvia e nao emula input.
6. INDICADOR DE COLETA: `indicador()` devolve estado, contexto e contagens para
   a UI desenhar (a UI real e KIT-G2; aqui provamos o dado).
7. EXPORTACAO SEM HERMES/IA: `exportar()` grava um JSON local com caminho padrao
   e rotulo `runtime=NAO_EXERCITADO`.
8. CONTRATO KIT-07: `contrato_kit07()` declara o formato de export consumivel
   por KIT-07 sem acoplar (KIT-07 ainda nao implementado).

LIMITE HONESTO: isto e a LOGICA do plano de controle (offline). A UI real e a
leitura de teclas do engine dependem de KIT-G2 e da rodada autorizada do dono;
runtime/pixels/jogo permanecem NAO_EXERCITADO.
"""
import argparse
import json
import os
import sys
import time
import uuid

ESQUEMA_ATALHOS = "KIT-06/atalhos/1"
ESQUEMA_CONTROLE = "KIT-06/controle/1"
ESQUEMA_EXPORT = "KIT-07/export/1"   # contrato declarado para KIT-07

# --------------------------------------------------------------- acoes --------
OBSERVAR = "observar"
PARAR_OBSERVACAO = "parar_observacao"
PAUSAR = "pausar"
RETOMAR = "retomar"
MARCAR_PROBLEMA = "marcar_problema"
EXPORTAR = "exportar"

ACOES_CONHECIDAS = (OBSERVAR, PARAR_OBSERVACAO, PAUSAR, RETOMAR,
                    MARCAR_PROBLEMA, EXPORTAR)

# Acoes ATIVAS proibidas: nao existem no plano de controle (trava dura).
ACOES_ATIVAS = frozenset((
    "clique_emitido", "emitir_clique", "save", "salvar", "equipar",
    "modificar", "habilitar_modo_ativo", "modo_ativo", "executar_acao",
))

# Teclas RESERVADAS por padrao: as usadas para abrir/escrever no CHAT. Um atalho
# do instrumento nunca pode ocupar tecla de digitacao de texto.
TECLAS_RESERVADAS_PADRAO = (
    "Return", "KeypadEnter", "T", "Y", "Slash", "Backspace", "Space",
)

# Acoes cujo alvo padrao e alternar (ligar/desligar).
ACOES_ALTERNAVEIS = (OBSERVAR, PAUSAR)

MOTIVO_GUARD_CHAT = "guard_chat"
MOTIVO_GUARD_REMAPEAMENTO = "guard_remapeamento"
MOTIVO_GUARD_SEM_FOCO = "guard_sem_foco"
MOTIVO_SEM_BINDING = "sem_binding"
MOTIVO_TECLA_DESCONHECIDA = "tecla_desconhecida"

# Sentinela de "campo NAO informado" (F-KIT06R: limpar janela=None). Distingue
# `atualizar_contexto(janela=None)` (LIMPAR a janela corrente) de omitir o
# argumento (manter o valor atual).
_SEM_VALOR = object()


class ErroControleAcesso(ValueError):
    """Entrada invalida de CONFIGURACAO/uso (nao e evento do jogo)."""


# --------------------------------------------------------------- atalhos ------
def valida_atalhos(atalhos, teclas_reservadas=None):
    """Valida um mapa acao->tecla e devolve (mapa_normalizado, problemas).

    `problemas` e uma lista de motivos; ATALHO com problema e REMOVIDO do mapa
    normalizado (nunca aceito em silencio). Motivos:
      * `acao_desconhecida`     - acao fora de ACOES_CONHECIDAS;
      * `acao_ativa_proibida`   - acao ATIVA (trava dura do modo passivo);
      * `tecla_reservada`       - tecla de chat;
      * `tecla_vazia`           - binding vazio;
      * `conflito_tecla`        - a MESMA tecla em dois atalhos.
    """
    reservadas = set(teclas_reservadas or TECLAS_RESERVADAS_PADRAO)
    problemas = []
    norm = {}
    if not isinstance(atalhos, dict):
        raise ErroControleAcesso("atalhos precisa ser um dicionario acao->tecla")
    usadas = {}
    for acao, tecla in atalhos.items():
        acao = str(acao)
        if acao in ACOES_ATIVAS:
            problemas.append((acao, "acao_ativa_proibida"))
            continue
        if acao not in ACOES_CONHECIDAS:
            problemas.append((acao, "acao_desconhecida"))
            continue
        tecla = "" if tecla is None else str(tecla).strip()
        if not tecla:
            problemas.append((acao, "tecla_vazia"))
            continue
        if tecla in reservadas:
            problemas.append((acao, "tecla_reservada"))
            continue
        if tecla in usadas:
            problemas.append((acao, "conflito_tecla"))
            problemas.append((usadas[tecla], "conflito_tecla"))
            norm.pop(usadas[tecla], None)
            continue
        usadas[tecla] = acao
        norm[acao] = tecla
    # remove duplicatas preservando ordem
    vistos = set()
    limpos = []
    for acao, motivo in problemas:
        if (acao, motivo) not in vistos:
            vistos.add((acao, motivo))
            limpos.append((acao, motivo))
    return norm, limpos


def carrega_atalhos(caminho):
    """Le o JSON de atalhos (`{"teclas_reservadas": [...], "atalhos": {...}}`)."""
    with open(caminho, encoding="utf-8") as fh:
        doc = json.load(fh)
    if not isinstance(doc, dict):
        raise ErroControleAcesso("config de atalhos precisa ser um objeto JSON")
    atalhos = doc.get("atalhos", doc if "atalhos" not in doc else {})
    reservadas = doc.get("teclas_reservadas")
    norm, problemas = valida_atalhos(atalhos, reservadas)
    return norm, problemas, reservadas


def atalhos_padrao():
    """Mapa padrao minimo (teclas de funcao, fora do chat)."""
    return {OBSERVAR: "F7", PAUSAR: "F8", MARCAR_PROBLEMA: "F9",
            EXPORTAR: "F10"}


def _copia_profunda(valor):
    """Copia PROFUNDA de estruturas JSON (dict/list/tuple); espelha `CopiaValor` C#.

    F6 (KIT-06F): o documento de export precisa ser um SNAPSHOT DEFENSIVO
    *inclusive dos objetos ANINHADOS*. Os acessores do pipeline devolvem copia
    RASA (o dict do evento e novo, mas `dados`/`quadro` continuam sendo os
    objetos internos). Sem a copia profunda, mutar
    `doc["coleta"]["eventos"][i]["quadro"|"dados"]` corromperia a EVIDENCIA
    INTERNA do pipeline e os exports seguintes.
    """
    if isinstance(valor, dict):
        return {k: _copia_profunda(v) for k, v in valor.items()}
    if isinstance(valor, (list, tuple)):
        return [_copia_profunda(v) for v in valor]
    return valor


# -------------------------------------------------------------- controle ------
class ControleAcesso(object):
    """Plano de controle: estado da coleta, contexto, marcacao e export."""

    def __init__(self, atalhos=None, teclas_reservadas=None,
                 limite_marcacoes=200, limite_degradacoes=200,
                 id_sessao=None, relogio=None, pasta_export=None,
                 pipeline=None, teto_problemas=50):
        if limite_marcacoes < 1 or limite_degradacoes < 1:
            raise ErroControleAcesso("limites precisam ser >= 1")
        if teto_problemas < 0:
            raise ErroControleAcesso("teto_problemas nao pode ser negativo")
        # F1 (KIT-06R): mapa EXPLICITAMENTE VAZIO desabilita os bindings; so
        # `None` (nao informado) usa os padroes. Configuracao recusada nunca
        # reativa binding nao aprovado.
        if atalhos is None:
            atalhos = atalhos_padrao()
        atalhos = dict(atalhos)
        self.atalhos, self.problemas_atalhos = valida_atalhos(
            atalhos, teclas_reservadas)
        self.limite_marcacoes = int(limite_marcacoes)
        self.limite_degradacoes = int(limite_degradacoes)
        self.teto_problemas = int(teto_problemas)
        self.id_sessao = id_sessao or ("sessao-" + uuid.uuid4().hex[:8])
        self._relogio = relogio
        self.pasta_export = pasta_export
        self.pipeline = pipeline

        self.modo = "passivo"
        self._observando = False
        self._contexto = {
            "janela": None,
            "chat_aberto": False,
            "digitando": False,
            "remapeando": False,
            "foco_no_jogo": True,
        }
        self._marcacoes = []
        self._degradacoes = []
        self._contagem_degradacoes = {}
        self.eventos_controle = []          # trilha das acoes efetivadas
        self.consome_input = False          # so LE teclas
        self.foco_forcado = 0               # trava: nunca muda o foco
        self.encerrou_sessao = False        # trava: nunca encerra a sessao
        self.modo_ativo_pedidos = 0
        # F3 (KIT-06R): OWNERSHIP EXPLICITO da coleta. Comecando DESLIGADO com
        # pipeline ligado, o pipeline comeca PAUSADO — o indicador "parado" nao
        # pode coexistir com coleta escondida. Nenhum booleano finge efeito.
        if self.pipeline is not None and hasattr(self.pipeline, "pausar") \
                and not self._pipeline_pausado():
            self.pipeline.pausar()
            self._pausado_por_controle = True
        else:
            self._pausado_por_controle = self._pipeline_pausado()

    def _pipeline_pausado(self):
        """True so se HA pipeline e ele esta pausado (ausencia != pausa)."""
        return bool(self.pipeline is not None
                    and hasattr(self.pipeline, "esta_pausado")
                    and self.pipeline.esta_pausado())

    # ------------------------------------------------------------- util ------
    def _agora(self):
        if self._relogio is None:
            return int(time.monotonic() * 1000)
        return int(self._relogio())

    def _degrada(self, motivo, detalhe=None):
        self._contagem_degradacoes[motivo] = \
            self._contagem_degradacoes.get(motivo, 0) + 1
        item = {"motivo": motivo, "ts_ms": self._agora(),
                "sessao": self.id_sessao}
        if detalhe:
            item["detalhe"] = detalhe
        self._degradacoes.append(item)
        while len(self._degradacoes) > self.limite_degradacoes:
            self._degradacoes.pop(0)
        return item

    # -------------------------------------------------------- contexto ------
    def atualizar_contexto(self, janela=_SEM_VALOR, chat_aberto=None,
                           digitando=None, remapeando=None, foco_no_jogo=None):
        """Atualiza o CONTEXTO corrente (chamado pela UI/ponte a cada quadro).

        `janela=None` LIMPA a janela corrente (contrato F-KIT06R); omitir o
        argumento mantem o valor atual (sentinela `_SEM_VALOR`).
        """
        if janela is not _SEM_VALOR:
            self._contexto["janela"] = janela
        for chave, valor in (("chat_aberto", chat_aberto),
                             ("digitando", digitando),
                             ("remapeando", remapeando),
                             ("foco_no_jogo", foco_no_jogo)):
            if valor is not None:
                self._contexto[chave] = bool(valor)
        return dict(self._contexto)

    def contexto(self):
        return dict(self._contexto)

    def _guard_bloqueia(self):
        """Devolve o motivo de guard bloqueante, ou None.

        Chat aberto / digitando e remapeamento bloqueiam ATALHOS do instrumento
        (o humano esta escrevendo ou reconfigurando). Sem foco no jogo tambem
        bloqueia: NUNCA forcamos foco para capturar o atalho.
        """
        c = self._contexto
        if c.get("chat_aberto") or c.get("digitando"):
            return MOTIVO_GUARD_CHAT
        if c.get("remapeando"):
            return MOTIVO_GUARD_REMAPEAMENTO
        if not c.get("foco_no_jogo"):
            return MOTIVO_GUARD_SEM_FOCO
        return None

    # ---------------------------------------------------------- teclas -----
    def tecla_para_acao(self, tecla):
        for acao, t in self.atalhos.items():
            if t == tecla:
                return acao
        return None

    def processar_tecla(self, tecla, descricao=None):
        """Processa UMA tecla pressionada. Devolve o evento da acao ou None.

        Barrado (sempre com degradacao explicita, nunca silencioso):
          * guard de contexto (chat/remapeamento/sem foco) -> degradacao;
          * tecla sem atalho -> `sem_binding`;
          * acao que exige observacao ativa (ex.: exportar sem nada) -> ver acao.
        """
        motivo = self._guard_bloqueia()
        if motivo is not None:
            self._degrada(motivo, detalhe="tecla=%s ignorada pelo guard" % tecla)
            return None
        acao = self.tecla_para_acao(tecla)
        if acao is None:
            self._degrada(MOTIVO_SEM_BINDING, detalhe="tecla=%s" % tecla)
            return None
        return self.executar(acao, descricao=descricao)

    def executar(self, acao, descricao=None, caminho=None):
        """Executa uma ACAO CONHECIDA (chamavel tambem pela UI, sem teclado)."""
        if acao in ACOES_ATIVAS:
            self._degrada("acao_ativa_proibida", detalhe="acao=%s" % acao)
            return None
        if acao not in ACOES_CONHECIDAS:
            self._degrada("acao_desconhecida", detalhe="acao=%s" % acao)
            return None

        if acao == OBSERVAR:
            return self.alternar_observacao()
        if acao == PARAR_OBSERVACAO:
            return self.parar_observacao()
        if acao == PAUSAR:
            return self.alternar_pausa()
        if acao == RETOMAR:
            return self.retomar()
        if acao == MARCAR_PROBLEMA:
            return self.marcar_problema(descricao)
        if acao == EXPORTAR:
            return self.exportar(caminho)
        return None

    # -------------------------------------------------------- observar -----
    def iniciar_observacao(self):
        return self._iniciar_observacao()

    def _iniciar_observacao(self):
        """Liga a observacao PASSIVA. Nunca autoriza modo ativo."""
        if self._observando:
            self._degrada("ja_observando",
                          detalhe="observacao ja estava ligada")
            return None
        if self.pipeline is None:
            self._degrada("coleta_sem_pipeline",
                          detalhe="iniciar observacao sem pipeline ligado; "
                                  "coleta NAO operante (lacuna honesta)")
        self._observando = True
        self.modo = "passivo"          # trava dura: sempre passivo
        if self.pipeline is not None and hasattr(self.pipeline, "retomar"):
            self.pipeline.retomar()
            self._pausado_por_controle = False
        return self._evento(OBSERVAR, {"modo": self.modo})

    def parar_observacao(self):
        """Para de COLETAR. Nao fecha o jogo nem a sessao do dono."""
        if not self._observando:
            self._degrada("nao_observando",
                          detalhe="parar_observacao sem observacao ativa")
            return None
        self._observando = False
        if self.pipeline is not None and hasattr(self.pipeline, "pausar"):
            try:
                self.pipeline.pausar()
                self._pausado_por_controle = True
            except Exception as exc:            # pragma: no cover - defensivo
                self._degrada("pipeline_pausar_falhou", detalhe=str(exc))
        return self._evento(PARAR_OBSERVACAO, {"coleta": "encerrada"})

    def retomar(self):
        """RETOMAR (F2 KIT-06R): retoma a coleta PAUSADA de forma explicita.

        Efeito real: o pipeline volta a coletar e a observacao fica LIGADA
        (senao o indicador diria "parado" enquanto coleta — F3). Sem pipeline ou
        sem pausa pendente degrada explicitamente; nunca no-op silencioso.
        """
        if self.pipeline is None or not hasattr(self.pipeline, "esta_pausado"):
            self._degrada("sem_pipeline", detalhe="retomar sem pipeline ligado")
            return None
        if not self.pipeline.esta_pausado():
            self._degrada("ja_retomado", detalhe="nao ha coleta pausada")
            return None
        self.pipeline.retomar()
        self._pausado_por_controle = False
        if not self._observando:
            self._observando = True
            self.modo = "passivo"
        return self._evento(RETOMAR, {"pausado": False, "observando": True})

    def observando(self):
        return self._observando

    def alternar_observacao(self):
        return self.parar_observacao() if self._observando \
            else self._iniciar_observacao()

    # --------------------------------------------------------- pausar ------
    def alternar_pausa(self):
        """Pausa/retoma a COLETA. Pausa vale tanto para o controle quanto p/ o
        pipeline (KIT-05F invalida pendencias com lacuna explicita)."""
        if not self._observando:
            self._degrada("pausar_sem_observacao",
                          detalhe="nao ha coleta para pausar")
            return None
        if self.pipeline is None:
            self._degrada("sem_pipeline", detalhe="pausa sem pipeline ligado")
            return None
        pausado = self._pipeline_pausado()
        if pausado:
            self.pipeline.retomar()
            self._pausado_por_controle = False
            return self._evento(RETOMAR, {"pausado": False})
        self.pipeline.pausar()
        self._pausado_por_controle = True
        return self._evento(PAUSAR, {"pausado": True})

    # ---------------------------------------------------------- marcar -----
    def marcar_problema(self, descricao=None, severidade="media", janela=None):
        """MARCACAO MANUAL: um problema apontado pelo humano, com contexto.

        Exige observacao ATIVA (sem coleta nao ha a que ancorar a marcacao).
        Marca durante pausa e permitido (o humano anota o que viu); o fato de
        estar pausado e registrado na propria marcacao.
        """
        if not self._observando:
            self._degrada("marcar_sem_observacao",
                          detalhe="marcacao manual exige observacao ativa")
            return None
        if len(self._marcacoes) >= self.teto_problemas:
            self._degrada("teto_problemas_atingido",
                          detalhe="teto_problemas=%d" % self.teto_problemas)
            return None
        pausado = bool(self.pipeline is not None
                       and self.pipeline.esta_pausado())
        marcacao = {
            "esquema": ESQUEMA_CONTROLE,
            "id": "mk-" + uuid.uuid4().hex[:8],
            "sessao": self.id_sessao,
            "ts_ms": self._agora(),
            "descricao": descricao if descricao is not None else "(sem descricao)",
            "severidade": severidade,
            "janela": janela if janela is not None
                      else self._contexto.get("janela"),
            "pausado_no_momento": pausado,
            "foco_forcado": False,
        }
        self._marcacoes.append(marcacao)
        while len(self._marcacoes) > self.limite_marcacoes:
            self._marcacoes.pop(0)
        return self._evento(MARCAR_PROBLEMA, {"marcacao_id": marcacao["id"]})

    def marcacoes(self):
        return [dict(m) for m in self._marcacoes]

    # -------------------------------------------------------- exportar -----
    def _pasta_export_padrao(self):
        """Pasta local padrao do export (acessivel sem Hermes/IA, sem terminal
        sofisticado: um caminho fixo e conhecido)."""
        if self.pasta_export:
            return self.pasta_export
        raiz = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))          # raiz do repo pelo layout
        return os.path.join(raiz, "scratch", "kit", "KIT-06", "export")

    def exportar(self, caminho=None):
        """Grava o export em arquivo LOCAL. Sem Hermes, sem IA, sem credencial.

        F5 (KIT-06R): falha-segura. Erro de IO (pasta que e arquivo, sem
        permissao) NAO propaga, NAO emite evento de sucesso e NAO sobrescreve
        conteudo alheio: degrada explicito e devolve None.
        """
        if not self._observando and not self._marcacoes:
            self._degrada("exportar_sem_dados",
                          detalhe="nada para exportar (sem observacao e sem marcacao)")
            return None
        pasta = self._pasta_export_padrao()
        if caminho is None:
            caminho = os.path.join(
                pasta, "kit06-%s-%d.json" % (self.id_sessao, self._agora()))
        else:
            if not os.path.isabs(caminho):
                caminho = os.path.join(pasta, caminho)
        doc = self.documento_export()
        try:
            pasta_destino = os.path.dirname(caminho)
            if pasta_destino and not os.path.isdir(pasta_destino):
                os.makedirs(pasta_destino)
            with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=2)
        except OSError as exc:
            self._degrada("export_falha_io",
                          detalhe="%s: %s" % (type(exc).__name__, exc))
            return None
        self._evento(EXPORTAR, {"caminho": os.path.abspath(caminho)})
        return os.path.abspath(caminho)

    def _coleta_documento(self):
        """Bloco de coleta REAL (F4): reusa o pipeline KIT-05F; nao fabrica runtime."""
        p = self.pipeline
        bloco = {"pipeline_ligado": p is not None, "lacunas_honestas": []}
        if p is None:
            bloco["lacunas_honestas"].append(
                "sem pipeline ligado: coleta NAO operante "
                "(nenhum evento/dado retido)")
            return bloco
        resumo = p.resumo() if hasattr(p, "resumo") else {}
        eventos = p.eventos() if hasattr(p, "eventos") else []
        # F6 (KIT-06F): SNAPSHOT DEFENSIVO PROFUNDO. Os acessores do pipeline
        # devolvem copia RASA (o dict do evento e novo, mas `dados`/`quadro`
        # aninhados seguem por REFERENCIA). Sem a copia profunda, um consumidor
        # que mutasse `doc["coleta"]["eventos"][i]["quadro"]` corromperia a
        # EVIDENCIA INTERNA do pipeline e os exports seguintes.
        bloco["resumo"] = _copia_profunda(resumo)
        bloco["eventos"] = _copia_profunda(eventos)
        bloco["degradacoes"] = _copia_profunda(
            p.degradacoes() if hasattr(p, "degradacoes") else [])
        bloco["rejeitados"] = _copia_profunda(
            p.rejeitados() if hasattr(p, "rejeitados") else [])
        bloco["lacunas"] = _copia_profunda(
            p.lacunas() if hasattr(p, "lacunas") else [])
        if hasattr(p, "captura_de"):
            bloco["capturas"] = _copia_profunda(
                [c for c in (p.captura_de(e.get("id")) for e in eventos) if c])
        if hasattr(p, "pedidos_retidos"):
            bloco["pedidos_retidos"] = int(p.pedidos_retidos())
        if hasattr(p, "capturas_retidas"):
            bloco["capturas_retidas"] = int(p.capturas_retidas())
        if not self._observando:
            bloco["lacunas_honestas"].append(
                "controle parado: os eventos retidos sao HISTORICO, "
                "nao coleta ativa")
        if self._observando and not self._pipeline_pausado() and not eventos:
            bloco["lacunas_honestas"].append(
                "coleta ativa sem eventos retidos ate o momento (lacuna honesta)")
        return bloco

    def documento_export(self):
        """Documento de export (contrato KIT-07 declarado), com a EVIDENCIA real.

        F4 (KIT-06R): inclui eventos/dados/pedidos/falhas/capturas do pipeline,
        as degradacoes e a trilha de controle, com CORRELACAO sessao/quadro e
        lacunas honestas. Nao anuncia o que descarta.
        """
        sessao_coleta = None
        if self.pipeline is not None and hasattr(self.pipeline, "id_sessao"):
            sessao_coleta = self.pipeline.id_sessao
        return {
            "esquema": ESQUEMA_EXPORT,
            "esquema_controle": ESQUEMA_CONTROLE,
            "sessao": self.id_sessao,
            "origem": "controle-offline (KIT-06); runtime=NAO_EXERCITADO",
            "runtime": "NAO_EXERCITADO",
            "runtime_exercitado": False,
            "modo": self.modo,
            "observando": self._observando,
            "consome_input": self.consome_input,
            "foco_forcado": self.foco_forcado,
            "encerrou_sessao": self.encerrou_sessao,
            "contexto": dict(self._contexto),
            "marcacoes": self.marcacoes(),
            "problemas_atalhos": [list(p) for p in self.problemas_atalhos],
            "indicador": self.indicador(),
            "correlacao": {
                "sessao_controle": self.id_sessao,
                "sessao_coleta": sessao_coleta,
            },
            "trilha_controle": _copia_profunda(
                [dict(e) for e in self.eventos_controle]),
            "degradacoes_controle": self.degradacoes(),
            "coleta": self._coleta_documento(),
        }

    # ------------------------------------------------------- indicador -----
    def indicador(self):
        """Dado do INDICADOR DE COLETA (a UI desenha; aqui devolvemos o dado).

        F3 (KIT-06R): o estado EFEITO. Ausencia de pipeline e DEGRADACAO
        explicita ("sem_pipeline"), distinta de coleta funcional; nada aqui
        autoriza modo ativo.
        """
        pausado = self._pipeline_pausado()
        if not self._observando:
            estado = "parado"
        elif self.pipeline is None:
            estado = "sem_pipeline"
        elif pausado:
            estado = "pausado"
        else:
            estado = "observando"
        coleta_operante = bool(self._observando and self.pipeline is not None
                               and not pausado)
        eventos = 0
        if self.pipeline is not None and hasattr(self.pipeline, "resumo"):
            eventos = int(self.pipeline.resumo().get("eventos_total", 0) or 0)
        return {
            "estado": estado,
            "texto": "COLETA: %s | janela=%s | eventos=%d | marcacoes=%d"
                     % (estado, self._contexto.get("janela") or "-",
                        eventos, len(self._marcacoes)),
            "janela": self._contexto.get("janela"),
            "eventos": eventos,
            "marcacoes": len(self._marcacoes),
            "modo": self.modo,
            "pipeline_ligado": self.pipeline is not None,
            "coleta_operante": coleta_operante,
        }

    def texto_indicador(self):
        return self.indicador()["texto"]

    # ---------------------------------------------------- trava modo ativo -
    def habilitar_modo_ativo(self, *args, **kwargs):
        """TRAVA DURA: o instrumento e PASSIVO. Nunca autoriza modo ativo.

        Existe apenas para tornar a recusa EXPLICITA e testavel; sempre falha.
        """
        self.modo_ativo_pedidos += 1
        self._degrada("modo_ativo_proibido",
                      detalhe="iniciar/observar nao autoriza modo ativo")
        return None

    # ------------------------------------------------------------ trilha ---
    def _evento(self, acao, detalhes=None):
        ev = {"acao": acao, "ts_ms": self._agora(), "sessao": self.id_sessao,
              "contexto": dict(self._contexto)}
        if detalhes:
            ev.update(detalhes)
        self.eventos_controle.append(ev)
        while len(self.eventos_controle) > self.limite_degradacoes:
            self.eventos_controle.pop(0)
        return ev

    def degradacoes(self):
        return [dict(d) for d in self._degradacoes]

    def resumo(self):
        ind = self.indicador()
        return {
            "esquema": ESQUEMA_CONTROLE,
            "sessao": self.id_sessao,
            "modo": self.modo,
            "observando": self._observando,
            "pausado": self._pipeline_pausado(),
            "coleta_operante": bool(self._observando and self.pipeline is not None),
            "consome_input": self.consome_input,
            "foco_forcado": self.foco_forcado,
            "encerrou_sessao": self.encerrou_sessao,
            "modo_ativo_pedidos": self.modo_ativo_pedidos,
            "atalhos": dict(self.atalhos),
            "problemas_atalhos": [list(p) for p in self.problemas_atalhos],
            "marcacoes": len(self._marcacoes),
            "teto_problemas": self.teto_problemas,
            "degradacoes": len(self._degradacoes),
            "degradacoes_por_motivo": dict(self._contagem_degradacoes),
            "indicador": ind,
            "runtime": "NAO_EXERCITADO",
            "runtime_exercitado": False,
        }


# -------------------------------------------------------------- KIT-07 --------
def contrato_kit07():
    """Contrato de export consumivel por KIT-07 (declarado, NAO acoplado).

    F8 (KIT-06R): o descritor antigo dizia `NAO_IMPLEMENTADO`, mas a API
    `montar_pacote` JA existe (tools/automacao/kit07/exportador.py). O estado
    HONESTO e: API existe, porem o exportador esta REPROVADO no KIT-07R e a
    correcao KIT-07F ainda corre; a integracao efetiva esta BLOQUEADA por gate.
    Este export continua BRUTO/LOCAL — NAO e pacote sanitizado/compartilhavel.
    """
    return {
        "esquema": ESQUEMA_EXPORT,
        "versao": 1,
        "produtor": "KIT-06/controle_acesso",
        "status_kit07": "GATE_NAO_SATISFEITO (API existe; KIT-07R REPROVADO, "
                        "correcao KIT-07F em andamento)",
        "api_kit07_existe": True,
        "api_kit07": "tools/automacao/kit07/exportador.py::montar_pacote "
                     "(nao integrada por gate)",
        "integracao_efetiva": False,
        "motivo_integracao": "exportador KIT-07 reprovado no KIT-07R; aguarda "
                             "KIT-07F aprovado — nenhum consumidor adotado "
                             "automaticamente",
        "export_bruto_local": True,
        "pacote_compartilhavel": False,
        "aviso": "o export KIT-06 e BRUTO/LOCAL (pode conter dados crus): NAO e "
                 "pacote sanitizado nem compartilhavel; nao usar sem gate",
        "campos_obrigatorios": [
            "esquema", "sessao", "origem", "runtime", "modo", "observando",
            "marcacoes", "indicador", "coleta", "correlacao",
        ],
        "garantias": [
            "runtime=NAO_EXERCITADO ate rodada autorizada",
            "foco_forcado=0 e encerrou_sessao=False",
            "marcacoes com contexto (janela, pausa, severidade)",
            "export reusa o pipeline KIT-05F (eventos/dados/pedidos/lacunas) "
            "com correlacao sessao/quadro; nao fabrica runtime",
        ],
        "acoplamento": "nenhum: consumidor OPCIONAL e explicito; fluxo basico "
                       "sem Hermes/IA/terminal",
    }


# ---------------------------------------------------------------- CLI ---------
class RelogioMutavel(object):
    def __init__(self, inicio=0):
        self.t = int(inicio)

    def avanca(self, ms):
        self.t += int(ms)
        return self.t

    def __call__(self):
        return self.t


def _correr_roteiro(roteiro, controle=None, pipeline=None, relogio=None):
    """Reproduz um roteiro offline (lista de passos) no plano de controle.

    Passos aceitos: {"acao": ...} | {"tecla": ...} | {"contexto": {...}} |
    {"avanca": ms}. Devolve (controle, eventos) com o ESTADO no fim.
    """
    rel = relogio if relogio is not None else RelogioMutavel(0)
    ctrl = controle or ControleAcesso(relogio=rel, pipeline=pipeline)
    for passo in roteiro:
        if "avanca" in passo:
            rel.avanca(passo["avanca"])
            continue
        if "contexto" in passo:
            ctrl.atualizar_contexto(**passo["contexto"])
            continue
        if "tecla" in passo:
            ctrl.processar_tecla(passo["tecla"], descricao=passo.get("descricao"))
            continue
        if "acao" in passo:
            ctrl.executar(passo["acao"], descricao=passo.get("descricao"),
                          caminho=passo.get("caminho"))
            continue
        raise ErroControleAcesso("passo invalido: %r" % (passo,))
    return ctrl, ctrl.eventos_controle


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="KIT-06: plano de controle offline (observar/pausar/marcar/exportar).")
    ap.add_argument("--atalhos", help="JSON de atalhos (acao->tecla)")
    ap.add_argument("--roteiro", help="JSON com roteiro offline de passos")
    ap.add_argument("--out", help="grava o resumo neste arquivo")
    ap.add_argument("--dump-contrato-kit07", action="store_true",
                    help="imprime o contrato KIT-07 declarado")
    args = ap.parse_args(argv)

    if args.dump_contrato_kit07:
        print(json.dumps(contrato_kit07(), ensure_ascii=False, indent=2))
        return 0

    atalhos = None
    problemas = []
    if args.atalhos:
        atalhos, problemas, _ = carrega_atalhos(args.atalhos)
    ctrl = ControleAcesso(atalhos=atalhos)
    eventos = []
    if args.roteiro:
        with open(args.roteiro, encoding="utf-8") as fh:
            roteiro = json.load(fh)
        if isinstance(roteiro, dict):
            roteiro = roteiro.get("roteiro", [])
        ctrl, eventos = _correr_roteiro(roteiro, ctrl)
    resumo = ctrl.resumo()
    resumo["problemas_config"] = [list(p) for p in problemas]
    resumo["eventos"] = eventos
    resumo["contrato_kit07"] = contrato_kit07()
    texto = json.dumps(resumo, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto)
    print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
