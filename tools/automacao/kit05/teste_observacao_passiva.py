#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teste_observacao_passiva.py - KIT-05F: testes OFFLINE reais do pipeline de
observacao passiva (`observacao_passiva.py`).

Execucao:
    python tools/automacao/kit05/teste_observacao_passiva.py
    python -m unittest tools/automacao/kit05/teste_observacao_passiva.py

Nao abre o jogo, nao instala probe, nao toca no perfil do dono. Vive fora de
`runtime/testes/` DE PROPOSITO: aquela pasta tem inventario TRAVADO pelo AUT-4
(`t_aut4_estado_docs.py`/`t_aut4_runbook.py`) que nao pertence a esta frente.

Cobertura KIT-05F: F1 (captura em duas fases: pedido != confirmacao), F2 (pausa
invalida pendencia nao observada), F3 (dedup por fonte/janela), F4 (limite de
TODO estado auxiliar sob milhares de entradas), F5 (timeout dentro do prazo),
F6 (replay/export = estado retido, rotulado fixture/offline).
"""
import base64
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest


def _acha_modulo():
    """Localiza `observacao_passiva.py`: ao lado do teste (layout de contra-prova)
    ou em `tools/automacao/runtime/` subindo a arvore."""
    base = os.path.dirname(os.path.abspath(__file__))
    if os.path.isfile(os.path.join(base, "observacao_passiva.py")):
        return os.path.join(base, "observacao_passiva.py")
    atual = base
    for _ in range(8):
        cand = os.path.join(atual, "tools", "automacao", "runtime",
                            "observacao_passiva.py")
        if os.path.isfile(cand):
            return cand
        atual = os.path.dirname(atual)
    raise RuntimeError("nao encontrei observacao_passiva.py a partir de %s" % base)


def _carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


op = _carrega("kit05_observacao_passiva", _acha_modulo())

# PNG 1x1 REAL (bytes validos, cabecalho \x89PNG) para os testes de captura.
PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQAB"
    "DQottAAAAABJRU5ErkJggg==")


class RelogioFalso(object):
    """Relogio injetavel em ms (para timeout/retencao sem esperar de verdade)."""

    def __init__(self, inicio=1000):
        self.agora = int(inicio)

    def avanca(self, ms):
        self.agora += int(ms)
        return self.agora

    def __call__(self):
        return self.agora


class Base(unittest.TestCase):
    """Utilitarios: arquivo PNG real temporario."""

    def _png_real(self):
        tmp = tempfile.mkdtemp(prefix="kit05f-png-")
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))
        caminho = os.path.join(tmp, "quadro-real.png")
        with open(caminho, "wb") as fh:
            fh.write(PNG_1X1)
        return caminho


class TesteModoPassivo(unittest.TestCase):
    def test_aceita_tipos_observados(self):
        obs = op.ObservacaoPassiva(id_sessao="s1")
        self.assertIsNotNone(obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 2}))
        self.assertIsNotNone(obs.registrar(op.JANELA_ABERTA, {"nome": "tela"}))
        self.assertIsNotNone(obs.registrar(op.JANELA_FECHADA, {"nome": "tela"}))
        self.assertIsNotNone(obs.registrar(op.TOOLTIP, {"texto": "dano"}))
        tipos = [e["tipo"] for e in obs.eventos()]
        self.assertEqual(tipos, [op.CLIQUE_RECEBIDO, op.JANELA_ABERTA,
                                 op.JANELA_FECHADA, op.TOOLTIP])

    def test_rejeita_tipo_ativo(self):
        obs = op.ObservacaoPassiva(id_sessao="s1")
        for ativo in ("clique_emitido", "salvar", "equipar", "modificacao"):
            self.assertIsNone(obs.registrar(ativo, {"alvo": "x"}))
        self.assertEqual(len(obs.eventos()), 0)
        motivos = {r["motivo"] for r in obs.rejeitados()}
        self.assertEqual(motivos, {"tipo_ativo"})
        self.assertIn("tipo_ativo", {d["motivo"] for d in obs.degradacoes()})

    def test_rejeita_tipo_desconhecido(self):
        obs = op.ObservacaoPassiva(id_sessao="s1")
        self.assertIsNone(obs.registrar("evento_inventado", {}))
        self.assertEqual(obs.rejeitados()[0]["motivo"], "tipo_desconhecido")
        self.assertEqual(len(obs.eventos()), 0)

    def test_rejeita_dado_ativo(self):
        obs = op.ObservacaoPassiva(id_sessao="s1")
        self.assertIsNone(obs.registrar(op.CLIQUE_RECEBIDO,
                                        {"x": 1, "acao_executada": "atacar"}))
        self.assertEqual(obs.rejeitados()[0]["motivo"], "dado_ativo")
        self.assertEqual(len(obs.eventos()), 0)


class TesteDeduplicacao(unittest.TestCase):
    def test_estado_repetido_nao_vira_evento(self):
        obs = op.ObservacaoPassiva(id_sessao="s1")
        e1 = obs.registrar(op.JANELA_ABERTA, {"nome": "tela"})
        e2 = obs.registrar(op.JANELA_ABERTA, {"nome": "tela"})
        self.assertIsNotNone(e1)
        self.assertIsNone(e2)
        self.assertEqual(len(obs.eventos()), 1)
        self.assertIn("sem_mudanca", {d["motivo"] for d in obs.degradacoes()})

    def test_mudanca_de_estado_vira_evento(self):
        obs = op.ObservacaoPassiva(id_sessao="s1")
        obs.registrar(op.JANELA_ABERTA, {"nome": "tela_a"})
        e2 = obs.registrar(op.JANELA_ABERTA, {"nome": "tela_b"})
        self.assertIsNotNone(e2)
        self.assertEqual(len(obs.eventos()), 2)

    def test_clique_nao_deduplica(self):
        # Clique e evento DISCRETO: dois cliques iguais sao dois fatos.
        obs = op.ObservacaoPassiva(id_sessao="s1")
        e1 = obs.registrar(op.CLIQUE_RECEBIDO, {"x": 5, "y": 5})
        e2 = obs.registrar(op.CLIQUE_RECEBIDO, {"x": 5, "y": 5})
        self.assertIsNotNone(e1)
        self.assertIsNotNone(e2)
        self.assertEqual(len(obs.eventos()), 2)

    def test_janelas_distintas_com_dados_iguais_coexistem(self):
        # F3: o estado e POR FONTE; B nao pode ser colapsada por causa de A.
        obs = op.ObservacaoPassiva(id_sessao="s1")
        self.assertIsNotNone(obs.registrar(op.JANELA_ABERTA, janela="janela_a"))
        self.assertIsNotNone(obs.registrar(op.JANELA_ABERTA, janela="janela_b"))
        self.assertEqual(len(obs.eventos()), 2)

    def test_intercalacao_constante_nao_gera_spam(self):
        # F3: alternar fontes NAO pode reinflar o mesmo estado constante.
        obs = op.ObservacaoPassiva(fila_max=1000, id_sessao="s1")
        for _ in range(100):
            obs.registrar(op.JANELA_ABERTA, {"nome": "a"}, janela="a")
            obs.registrar(op.TOOLTIP, {"texto": "constante"})
        self.assertEqual(len(obs.eventos()), 2)

    def test_abrir_fechar_reabrir_sobrevive(self):
        # F3: fechamento/reabertura legitimos NAO podem ser descartados.
        obs = op.ObservacaoPassiva(id_sessao="s1")
        obs.registrar(op.JANELA_ABERTA, janela="tela")
        obs.registrar(op.JANELA_FECHADA, janela="tela")
        self.assertIsNotNone(obs.registrar(op.JANELA_ABERTA, janela="tela"))
        self.assertEqual(len(obs.eventos()), 3)


class TesteFilaERetencao(unittest.TestCase):
    def test_fila_limitada_descarta_e_declara(self):
        obs = op.ObservacaoPassiva(fila_max=3, id_sessao="s1")
        for i in range(5):
            obs.registrar(op.TOOLTIP, {"texto": "t%d" % i})
        self.assertEqual(len(obs.eventos()), 3)
        motivos = [d["motivo"] for d in obs.degradacoes()]
        self.assertEqual(motivos.count("fila_cheia"), 2)
        self.assertEqual([e["dados"]["texto"] for e in obs.eventos()],
                         ["t2", "t3", "t4"])

    def test_retencao_por_idade(self):
        rel = RelogioFalso(1000)
        obs = op.ObservacaoPassiva(retencao_ms=1000, id_sessao="s1", relogio=rel)
        obs.registrar(op.TOOLTIP, {"texto": "velho"})
        rel.avanca(2000)
        obs.registrar(op.TOOLTIP, {"texto": "novo"})
        removidos = obs.expirar()
        self.assertEqual(removidos, 1)
        self.assertEqual([e["dados"]["texto"] for e in obs.eventos()], ["novo"])

    def test_retencao_por_tamanho(self):
        rel = RelogioFalso(1000)
        obs = op.ObservacaoPassiva(retencao_ms=0, retencao_max=2,
                                   id_sessao="s1", relogio=rel)
        for i in range(4):
            rel.avanca(10)
            obs.registrar(op.TOOLTIP, {"texto": "t%d" % i})
        self.assertEqual(len(obs.eventos()), 2)

    def test_todo_estado_auxiliar_e_limitado_sob_milhares(self):
        # F4: fila_max=2 com 1000 rodadas de spam/rejeicao NAO pode crescer
        # degradacoes, rejeitados, pendentes, pedidos nem referencias de captura.
        obs = op.ObservacaoPassiva(fila_max=2, retencao_max=2, id_sessao="s1")
        for _ in range(1000):
            obs.registrar(op.TOOLTIP, {"texto": "constante"})
            obs.registrar(op.CLIQUE_RECEBIDO, janela="a")
            obs.registrar("salvar")
        resumo = obs.resumo()
        self.assertLessEqual(len(obs.degradacoes()), 2)
        self.assertLessEqual(len(obs.rejeitados()), 2)
        self.assertLessEqual(resumo["pendentes"], 2)
        self.assertLessEqual(obs.pedidos_retidos(), 2)
        self.assertLessEqual(obs.capturas_retidas(), 2)
        # ... mas os CONTADORES agregados preservam o total real (sem lista):
        self.assertEqual(resumo["rejeitados_total"], 1000)
        self.assertGreaterEqual(resumo["degradacoes_total"], 1000)
        self.assertGreater(resumo["pendentes_descartados"], 0)

    def test_limite_aux_explicito_pode_ser_maior_finito(self):
        # F4: o limite e explicito e proprio; nao precisa ser igual ao da fila.
        obs = op.ObservacaoPassiva(fila_max=2, retencao_max=2, limite_aux=50,
                                   id_sessao="s1")
        for _ in range(500):
            obs.registrar(op.TOOLTIP, {"texto": "constante"})
        self.assertLessEqual(len(obs.degradacoes()), 50)
        self.assertGreater(len(obs.degradacoes()), 2)
        self.assertGreater(obs.resumo()["degradacoes_descartadas"], 0)


class TesteTetoCapturas(unittest.TestCase):
    def test_teto_de_capturas(self):
        obs = op.ObservacaoPassiva(teto_capturas=2, id_sessao="s1")
        ids = []
        for i in range(4):
            e = obs.registrar(op.TOOLTIP, {"texto": "t%d" % i})
            ids.append(e["id"])
        self.assertIsNotNone(obs.registrar_captura(ids[0], caminho="a.png"))
        self.assertIsNotNone(obs.registrar_captura(ids[1], caminho="b.png"))
        self.assertIsNone(obs.registrar_captura(ids[2], caminho="c.png"))
        self.assertEqual(obs.resumo()["capturas"], 2)
        self.assertIn("teto_capturas_atingido",
                      {d["motivo"] for d in obs.degradacoes()})

    def test_captura_evento_inexistente(self):
        obs = op.ObservacaoPassiva(teto_capturas=5, id_sessao="s1")
        self.assertIsNone(obs.registrar_captura("nao-existe"))
        self.assertIn("captura_evento_inexistente",
                      {d["motivo"] for d in obs.degradacoes()})


class TestePausaSegura(Base):
    def test_pausa_descarta_e_retoma(self):
        obs = op.ObservacaoPassiva(id_sessao="s1")
        obs.registrar(op.TOOLTIP, {"texto": "antes"})
        obs.pausar()
        self.assertTrue(obs.esta_pausado())
        self.assertIsNone(obs.registrar(op.TOOLTIP, {"texto": "durante"}))
        obs.retomar()
        self.assertFalse(obs.esta_pausado())
        self.assertIsNotNone(obs.registrar(op.TOOLTIP, {"texto": "depois"}))
        textos = [e["dados"]["texto"] for e in obs.eventos()]
        self.assertEqual(textos, ["antes", "depois"])
        self.assertIn("pausado", {d["motivo"] for d in obs.degradacoes()})

    def test_pausa_invalida_pendencia_nao_observada(self):
        # F2: clique -> pausa -> retoma NAO pode concluir "clique sem janela".
        rel = RelogioFalso(1000)
        obs = op.ObservacaoPassiva(timeout_janela_ms=100, id_sessao="s1",
                                   relogio=rel)
        obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 1}, janela="tela")
        obs.pausar()
        rel.avanca(200)                       # vence DENTRO da pausa
        self.assertEqual(obs.verificar_timeouts(), [])
        obs.retomar()
        self.assertEqual(obs.verificar_timeouts(), [])   # sem falsa falha
        self.assertEqual(
            [e["tipo"] for e in obs.eventos() if e["tipo"] == op.FALHA_CLIQUE_SEM_JANELA],
            [])
        self.assertIn("observacao_interrompida",
                      {d["motivo"] for d in obs.degradacoes()})
        self.assertEqual(obs.resumo()["lacunas"], 1)
        self.assertIsNotNone(obs.lacunas()[0]["fim_ms"])

    def test_pausa_bloqueia_pedido_e_confirmacao_de_captura(self):
        # F2: em pausa nao se pede nem se confirma captura.
        obs = op.ObservacaoPassiva(id_sessao="s1")
        e = obs.registrar(op.TOOLTIP, {"texto": "x"})
        caminho = self._png_real()
        pedido = obs.registrar_captura(e["id"], caminho=caminho, indice_quadro=99)
        self.assertIsNotNone(pedido)
        obs.pausar()
        self.assertIsNone(obs.registrar_captura(e["id"], caminho=caminho))
        self.assertIsNone(obs.confirmar_captura(pedido["captura_id"],
                                                indice_quadro=100))
        self.assertFalse(obs.eventos()[0]["quadro"]["captura_apos_atualizacao_visual"])
        self.assertEqual(obs.resumo()["capturas_confirmadas"], 0)


class TesteFalhaCliqueSemJanela(unittest.TestCase):
    def test_timeout_gera_falha_com_motivo(self):
        rel = RelogioFalso(1000)
        obs = op.ObservacaoPassiva(timeout_janela_ms=500, id_sessao="s1",
                                   relogio=rel)
        cli = obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 1},
                            janela="tela_skills")
        rel.avanca(600)
        falhas = obs.verificar_timeouts()
        self.assertEqual(len(falhas), 1)
        f = falhas[0]
        self.assertEqual(f["tipo"], op.FALHA_CLIQUE_SEM_JANELA)
        self.assertEqual(f["dados"]["clique_id"], cli["id"])
        self.assertEqual(f["dados"]["janela_alvo"], "tela_skills")
        self.assertEqual(f["dados"]["timeout_ms"], 500)
        self.assertTrue(f["dados"]["motivo"])
        self.assertEqual(f["dados"]["prazo_ms"], 1500)

    def test_janela_resolve_e_nao_gera_falha(self):
        rel = RelogioFalso(1000)
        obs = op.ObservacaoPassiva(timeout_janela_ms=500, id_sessao="s1",
                                   relogio=rel)
        obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 1}, janela="tela_skills")
        rel.avanca(200)
        obs.registrar(op.JANELA_ABERTA, {"nome": "tela_skills"},
                      janela="tela_skills")
        rel.avanca(600)
        falhas = obs.verificar_timeouts()
        self.assertEqual(falhas, [])

    def test_timeout_antes_do_prazo_nao_gera_falha(self):
        rel = RelogioFalso(1000)
        obs = op.ObservacaoPassiva(timeout_janela_ms=500, id_sessao="s1",
                                   relogio=rel)
        obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 1}, janela="tela")
        rel.avanca(100)
        self.assertEqual(obs.verificar_timeouts(), [])

    def test_fronteira_exata_gera_uma_falha_e_nao_duplica(self):
        # F5: prazo100 -> em t=99 nada; em t=100 exatamente UMA falha; depois nada.
        rel = RelogioFalso(0)
        obs = op.ObservacaoPassiva(timeout_janela_ms=100, id_sessao="s1",
                                   relogio=rel)
        obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 1}, janela="a")
        rel.avanca(99)
        self.assertEqual(obs.verificar_timeouts(), [])
        rel.avanca(1)
        self.assertEqual(len(obs.verificar_timeouts()), 1)
        self.assertEqual(obs.verificar_timeouts(), [])

    def test_janela_tardia_nao_apaga_vencimento(self):
        # F5: abertura em t=101 NAO pode suprimir a falha vencida em t=100.
        rel = RelogioFalso(0)
        obs = op.ObservacaoPassiva(timeout_janela_ms=100, id_sessao="s1",
                                   relogio=rel)
        obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 1}, janela="a")
        rel.avanca(101)
        obs.registrar(op.JANELA_ABERTA, janela="a")
        falhas = obs.verificar_timeouts()
        self.assertEqual(len(falhas), 1)
        self.assertEqual(falhas[0]["dados"]["janela_alvo"], "a")
        self.assertIn("janela_tardia_sem_resolucao",
                      {d["motivo"] for d in obs.degradacoes()})

    def test_janela_de_outra_identidade_nao_resolve(self):
        # F5: janela errada nao resolve pendencia de 'a'.
        rel = RelogioFalso(0)
        obs = op.ObservacaoPassiva(timeout_janela_ms=100, id_sessao="s1",
                                   relogio=rel)
        obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 1}, janela="a")
        obs.registrar(op.JANELA_ABERTA, {"nome": "b"}, janela="b")
        rel.avanca(100)
        self.assertEqual(len(obs.verificar_timeouts()), 1)


class TesteCapturaEmDuasFases(Base):
    """F1: PEDIDO nao e captura; confirmacao exige evidencia real."""

    def test_pedido_nao_confirma_captura(self):
        obs = op.ObservacaoPassiva(teto_capturas=5, id_sessao="s1")
        e = obs.registrar(op.JANELA_ABERTA, {"nome": "tela"}, quadro=100)
        pedido = obs.registrar_captura(e["id"], caminho="png-inexistente.png",
                                       indice_quadro=101)
        self.assertIsNotNone(pedido)
        self.assertEqual(pedido["estado"], op.CAPTURA_SOLICITADA)
        self.assertFalse(pedido["apos_atualizacao_visual"])
        self.assertTrue(obs.eventos()[0]["quadro"]["captura_solicitada"])
        self.assertFalse(obs.eventos()[0]["quadro"]["captura_apos_atualizacao_visual"])
        self.assertEqual(obs.resumo()["capturas_confirmadas"], 0)
        self.assertIsNone(obs.captura_de(e["id"]))

    def test_confirmacao_exige_png_real(self):
        obs = op.ObservacaoPassiva(teto_capturas=5, id_sessao="s1")
        e = obs.registrar(op.TOOLTIP, {"texto": "x"}, quadro=10)
        pedido = obs.registrar_captura(e["id"], caminho="nao-existe.png",
                                       indice_quadro=11)
        self.assertIsNone(obs.confirmar_captura(pedido["captura_id"],
                                                indice_quadro=11))
        self.assertFalse(obs.eventos()[0]["quadro"]["captura_apos_atualizacao_visual"])
        self.assertIn("captura_sem_png_real",
                      {d["motivo"] for d in obs.degradacoes()})

    def test_confirmacao_exige_quadro_posterior(self):
        obs = op.ObservacaoPassiva(teto_capturas=5, id_sessao="s1")
        caminho = self._png_real()
        e = obs.registrar(op.TOOLTIP, {"texto": "x"}, quadro=100)
        pedido = obs.registrar_captura(e["id"], caminho=caminho, indice_quadro=101)
        # quadro anterior ao evento -> recusa
        self.assertIsNone(obs.confirmar_captura(pedido["captura_id"],
                                                indice_quadro=99))
        # mesmo quadro do evento (nao posterior) -> recusa
        self.assertIsNone(obs.confirmar_captura(pedido["captura_id"],
                                                indice_quadro=100))
        self.assertFalse(obs.eventos()[0]["quadro"]["captura_apos_atualizacao_visual"])
        self.assertIn("captura_quadro_nao_posterior",
                      {d["motivo"] for d in obs.degradacoes()})

    def test_pedido_com_quadro_anterior_e_recusado(self):
        obs = op.ObservacaoPassiva(teto_capturas=5, id_sessao="s1")
        e = obs.registrar(op.TOOLTIP, {"texto": "x"}, quadro=100)
        self.assertIsNone(obs.registrar_captura(e["id"], indice_quadro=1))
        self.assertEqual(obs.resumo()["capturas"], 0)
        self.assertIn("captura_quadro_anterior",
                      {d["motivo"] for d in obs.degradacoes()})

    def test_confirmacao_exige_sessao_e_evento_coerentes(self):
        obs = op.ObservacaoPassiva(teto_capturas=5, id_sessao="s1")
        caminho = self._png_real()
        e = obs.registrar(op.TOOLTIP, {"texto": "x"}, quadro=10)
        pedido = obs.registrar_captura(e["id"], caminho=caminho, indice_quadro=11)
        self.assertIsNone(obs.confirmar_captura(pedido["captura_id"], sessao="outra"))
        self.assertIsNone(obs.confirmar_captura(pedido["captura_id"],
                                                evento_id="outro-evento"))
        self.assertIsNone(obs.confirmar_captura("pedido-inexistente"))
        self.assertIsNone(obs.confirmar_captura(pedido["captura_id"],
                                                hash_="0" * 64))
        motivos = {d["motivo"] for d in obs.degradacoes()}
        for esperado in ("captura_sessao_divergente", "captura_evento_divergente",
                         "confirmacao_sem_pedido", "captura_hash_divergente"):
            self.assertIn(esperado, motivos)
        self.assertFalse(obs.eventos()[0]["quadro"]["captura_apos_atualizacao_visual"])

    def test_confirmacao_com_png_e_quadro_posterior_confirma(self):
        obs = op.ObservacaoPassiva(teto_capturas=5, id_sessao="s1")
        caminho = self._png_real()
        e = obs.registrar(op.JANELA_ABERTA, {"nome": "tela"}, quadro=100)
        pedido = obs.registrar_captura(e["id"], caminho=caminho, indice_quadro=101)
        cap = obs.confirmar_captura(pedido["captura_id"], indice_quadro=101)
        self.assertIsNotNone(cap)
        self.assertEqual(cap["estado"], op.CAPTURA_CONFIRMADA)
        self.assertTrue(cap["apos_atualizacao_visual"])
        self.assertFalse(cap["simultaneidade_afirmada"])
        self.assertEqual(cap["indice_quadro"], 101)
        self.assertEqual(cap["indice_quadro_evento"], 100)
        self.assertEqual(cap["sha256"], __import__("hashlib").sha256(PNG_1X1).hexdigest())
        atual = obs.eventos()[0]
        self.assertTrue(atual["quadro"]["captura_apos_atualizacao_visual"])
        self.assertEqual(atual["quadro"]["captura_id"], cap["captura_id"])
        self.assertEqual(obs.resumo()["capturas_confirmadas"], 1)
        self.assertEqual(obs.captura_de(e["id"])["captura_id"], cap["captura_id"])


class TesteCorrelacaoESimultaneidade(unittest.TestCase):
    def test_nenhum_evento_afirma_simultaneidade(self):
        rel = RelogioFalso(1000)
        obs = op.ObservacaoPassiva(timeout_janela_ms=100, id_sessao="s1",
                                   relogio=rel)
        obs.registrar(op.CLIQUE_RECEBIDO, {"x": 1, "y": 1}, janela="t")
        obs.registrar(op.TOOLTIP, {"texto": "x"})
        rel.avanca(200)
        obs.verificar_timeouts()
        self.assertTrue(obs.eventos())
        for e in obs.eventos():
            self.assertFalse(e["quadro"]["simultaneidade_afirmada"])
        self.assertFalse(obs.resumo()["simultaneidade_afirmada"])

    def test_ids_unicos(self):
        obs = op.ObservacaoPassiva(id_sessao="s1")
        ids = [obs.registrar(op.TOOLTIP, {"texto": "t%d" % i})["id"]
               for i in range(5)]
        self.assertEqual(len(set(ids)), 5)


class TesteReplayCLI(unittest.TestCase):
    """F6: replay/export = estado retido, rotulado fixture/offline."""

    def test_replay_respeita_retencao_no_payload_final(self):
        obs, eventos, _ = op._correr_entradas(
            [{"tipo": op.TOOLTIP, "dados": {"texto": str(i)}} for i in range(1000)],
            fila_max=2, retencao_max=2)
        self.assertEqual(len(eventos), obs.resumo()["eventos_total"])
        self.assertEqual(len(eventos), 2)

    def test_replay_nao_guarda_lista_paralela_de_falhas(self):
        obs, eventos, falhas = op._correr_entradas(
            [{"tipo": op.CLIQUE_RECEBIDO, "dados": {"x": i}, "janela": "a"}
             for i in range(50)] + [{"acao": "avanca", "ms": 5000},
                                    {"acao": "verificar_timeouts"}],
            fila_max=2, retencao_max=2, timeout_janela_ms=100)
        self.assertEqual(len(eventos), obs.resumo()["eventos_total"])
        self.assertLessEqual(len(falhas), obs.resumo()["eventos_total"])
        self.assertEqual({e["tipo"] for e in falhas},
                         {op.FALHA_CLIQUE_SEM_JANELA} if falhas else set())

    def test_cli_rotula_fixture_offline_e_nao_promove_runtime(self):
        tmp = tempfile.mkdtemp(prefix="kit05f-cli-")
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))
        entradas = os.path.join(tmp, "entrada.json")
        saida = os.path.join(tmp, "saida.json")
        with open(entradas, "w", encoding="utf-8") as fh:
            json.dump({"config": {"fila_max": 2, "retencao_max": 2,
                                  "id_sessao": "cli-teste"},
                       "entradas": [{"tipo": op.TOOLTIP, "dados": {"texto": str(i)}}
                                    for i in range(50)]}, fh)
        with contextlib.redirect_stdout(io.StringIO()):
            rc = op.main(["--entradas", entradas, "--out", saida])
        self.assertEqual(rc, 0)
        with open(saida, encoding="utf-8") as fh:
            dados = json.load(fh)
        self.assertTrue(dados["origem"].startswith("fixture-offline"))
        self.assertEqual(dados["runtime"], "NAO_EXERCITADO")
        self.assertFalse(dados["runtime_exercitado"])
        self.assertEqual(len(dados["eventos_retidos"]), dados["eventos_total"])
        self.assertEqual(dados["eventos_total"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
