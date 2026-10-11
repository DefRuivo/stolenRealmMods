#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teste_controle_acesso.py - KIT-06: suite OFFLINE do plano de controle.

Cobre o aceite do cartao `t_66ff87b5`:
  * atalhos configuraveis com validacao (acao desconhecida/ativa, tecla
    reservada e CONFLITO recusados);
  * guards de chat/digitando/remapeamento/sem foco (atalho nao dispara);
  * iniciar observacao NUNCA autoriza modo ativo (trava dura);
  * sem foco forcado e sem encerrar a sessao do dono;
  * marcacao manual com contexto;
  * indicador de coleta (estado/texto/contagens);
  * exportacao local sem Hermes/IA + contrato KIT-07 declarado;
  * integracao com o pipeline KIT-05F (pausa/retomada reais).

Nao abre o jogo, nao instala probe, nao toca no perfil do dono.

Execucao:
    python tools/automacao/kit06/teste_controle_acesso.py
"""
import importlib.util
import json
import os
import tempfile
import unittest


def _acha(nome, rel):
    base = os.path.dirname(os.path.abspath(__file__))
    cand = os.path.join(base, nome)
    if os.path.isfile(cand):
        return cand
    atual = base
    for _ in range(8):
        cand = os.path.join(atual, *rel)
        if os.path.isfile(cand):
            return cand
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    raise RuntimeError("nao encontrei %s a partir de %s" % (nome, base))


def _carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ca = _carrega("kit06_controle_acesso",
              _acha("controle_acesso.py", ("tools", "automacao", "runtime",
                                           "controle_acesso.py")))
op = _carrega("kit05_observacao_passiva",
              _acha("observacao_passiva.py", ("tools", "automacao", "runtime",
                                              "observacao_passiva.py")))

REL_MODULO = ("tools", "automacao", "runtime", "controle_acesso.py")


class PipelineFalso(object):
    """Pipeline minimo: registra chamadas de pausa/retomada para inspecao."""

    def __init__(self, pausado=False, eventos=0):
        self._pausado = pausado
        self._eventos = eventos
        self.chamadas = []

    def pausar(self):
        self.chamadas.append("pausar")
        self._pausado = True

    def retomar(self):
        self.chamadas.append("retomar")
        self._pausado = False

    def esta_pausado(self):
        return self._pausado

    def resumo(self):
        return {"eventos_total": self._eventos}


def relogio(inicio=0):
    return ca.RelogioMutavel(inicio)


# ============================================================ atalhos ==========
class TestAtalhos(unittest.TestCase):

    def test_padrao_valido(self):
        norm, problemas = ca.valida_atalhos(ca.atalhos_padrao())
        self.assertEqual([], problemas)
        self.assertIn(ca.OBSERVAR, norm)
        self.assertEqual("F7", norm[ca.OBSERVAR])

    def test_acao_desconhecida_recusada(self):
        norm, problemas = ca.valida_atalhos({"voar": "F1"})
        self.assertEqual({}, norm)
        self.assertIn(("voar", "acao_desconhecida"), problemas)

    def test_acao_ativa_proibida(self):
        norm, problemas = ca.valida_atalhos({"habilitar_modo_ativo": "F1"})
        self.assertEqual({}, norm)
        self.assertIn(("habilitar_modo_ativo", "acao_ativa_proibida"), problemas)

    def test_tecla_reservada_recusada(self):
        norm, problemas = ca.valida_atalhos({ca.OBSERVAR: "Return"})
        self.assertEqual({}, norm)
        self.assertIn((ca.OBSERVAR, "tecla_reservada"), problemas)

    def test_tecla_vazia_recusada(self):
        norm, problemas = ca.valida_atalhos({ca.OBSERVAR: "   "})
        self.assertEqual({}, norm)
        self.assertIn((ca.OBSERVAR, "tecla_vazia"), problemas)

    def test_conflito_entre_atalhos_recusado(self):
        norm, problemas = ca.valida_atalhos({ca.OBSERVAR: "F7", ca.PAUSAR: "F7"})
        self.assertNotIn(ca.OBSERVAR, norm)
        self.assertNotIn(ca.PAUSAR, norm)
        self.assertIn((ca.PAUSAR, "conflito_tecla"), problemas)

    def test_carrega_atalhos_de_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "atalhos.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump({"teclas_reservadas": ["Return"],
                           "atalhos": {ca.OBSERVAR: "F7", ca.PAUSAR: "Return"}},
                          fh)
            norm, problemas, reservadas = ca.carrega_atalhos(p)
        self.assertEqual(["Return"], reservadas)
        self.assertEqual({"F7"}, set(norm.values()))
        self.assertIn((ca.PAUSAR, "tecla_reservada"), problemas)

    def test_config_nao_dict_levanta(self):
        with self.assertRaises(ca.ErroControleAcesso):
            ca.valida_atalhos(["F7"])


# ============================================================ guards ===========
class TestGuards(unittest.TestCase):

    def _ctrl(self):
        return ca.ControleAcesso(relogio=relogio())

    def test_chat_bloqueia_e_degrada(self):
        c = self._ctrl()
        c.atualizar_contexto(chat_aberto=True)
        self.assertIsNone(c.processar_tecla("F7"))
        self.assertFalse(c.observando())
        self.assertIn(ca.MOTIVO_GUARD_CHAT,
                      c.resumo()["degradacoes_por_motivo"])

    def test_digitando_bloqueia(self):
        c = self._ctrl()
        c.atualizar_contexto(digitando=True)
        self.assertIsNone(c.processar_tecla("F7"))
        self.assertIn(ca.MOTIVO_GUARD_CHAT,
                      c.resumo()["degradacoes_por_motivo"])

    def test_remapeando_bloqueia(self):
        c = self._ctrl()
        c.atualizar_contexto(remapeando=True)
        self.assertIsNone(c.processar_tecla("F7"))
        self.assertIn(ca.MOTIVO_GUARD_REMAPEAMENTO,
                      c.resumo()["degradacoes_por_motivo"])

    def test_sem_foco_bloqueia_sem_forcar_foco(self):
        c = self._ctrl()
        c.atualizar_contexto(foco_no_jogo=False)
        self.assertIsNone(c.processar_tecla("F7"))
        self.assertEqual(0, c.foco_forcado)
        self.assertIn(ca.MOTIVO_GUARD_SEM_FOCO,
                      c.resumo()["degradacoes_por_motivo"])

    def test_guards_nao_consomem_input(self):
        c = self._ctrl()
        self.assertFalse(c.consome_input)

    def test_tecla_sem_binding_degrada(self):
        c = self._ctrl()
        self.assertIsNone(c.processar_tecla("Keypad7"))
        self.assertIn(ca.MOTIVO_SEM_BINDING,
                      c.resumo()["degradacoes_por_motivo"])


# ======================================================== observar/pausar =====
class TestObservar(unittest.TestCase):

    def test_iniciar_observacao_modo_passivo(self):
        c = ca.ControleAcesso(relogio=relogio())
        ev = c.processar_tecla("F7")
        self.assertIsNotNone(ev)
        self.assertEqual(ca.OBSERVAR, ev["acao"])
        self.assertTrue(c.observando())
        self.assertEqual("passivo", c.modo)

    def test_f7_alterna_observacao_liga_desliga(self):
        # CONTRATO KIT-06F: OBSERVAR e LIGA/DESLIGA (como documentado no topo
        # do modulo). O 2o F7 DESLIGA a coleta — NAO e degradacao "ja_observando".
        # Com pipeline, desligar PAUSA a coleta: indicador "parado" == sem coleta.
        pf = PipelineFalso()
        c = ca.ControleAcesso(relogio=relogio(), pipeline=pf)
        ev = c.processar_tecla("F7")
        self.assertEqual(ca.OBSERVAR, ev["acao"])
        self.assertTrue(c.observando())
        ev2 = c.processar_tecla("F7")
        self.assertIsNotNone(ev2)
        self.assertEqual(ca.PARAR_OBSERVACAO, ev2["acao"])
        self.assertFalse(c.observando())
        self.assertTrue(pf.esta_pausado())

    def test_parar_nao_encerra_sessao_do_dono(self):
        c = ca.ControleAcesso(relogio=relogio())
        c.executar(ca.OBSERVAR)
        c.executar(ca.PARAR_OBSERVACAO)
        self.assertFalse(c.observando())
        self.assertFalse(c.encerrou_sessao)

    def test_pausar_sem_observacao_degrada(self):
        c = ca.ControleAcesso(relogio=relogio(), pipeline=PipelineFalso())
        self.assertIsNone(c.processar_tecla("F8"))
        self.assertIn("pausar_sem_observacao",
                      c.resumo()["degradacoes_por_motivo"])

    def test_pausa_delega_ao_pipeline(self):
        pf = PipelineFalso()
        c = ca.ControleAcesso(relogio=relogio(), pipeline=pf)
        # OWNERSHIP KIT-06F: ao ligar o controle com pipeline, ele NASCE pausado
        # (indicador "parado" == sem coleta). Logo a 1a chamada e o `pausar` do
        # construtor; depois `retomar` (iniciar observacao) e o ciclo pausa/retoma.
        self.assertEqual(["pausar"], pf.chamadas)
        c.executar(ca.OBSERVAR)
        c.executar(ca.PAUSAR)
        self.assertTrue(pf.esta_pausado())
        c.executar(ca.PAUSAR)          # alterna -> retoma
        self.assertFalse(pf.esta_pausado())
        self.assertEqual(["pausar", "retomar", "pausar", "retomar"], pf.chamadas)


class TestIntegracaoKit05F(unittest.TestCase):
    """Integracao REAL com o pipeline KIT-05F (mesmo objeto)."""

    def test_pausa_do_controle_pausa_o_pipeline(self):
        obs = op.ObservacaoPassiva(relogio=relogio(), fonte="teste-kit06")
        c = ca.ControleAcesso(relogio=relogio(), pipeline=obs)
        c.executar(ca.OBSERVAR)
        c.executar(ca.PAUSAR)
        self.assertTrue(obs.esta_pausado())
        # em pausa o pipeline barra registro (KIT-05F F2)
        self.assertIsNone(obs.registrar("clique_recebido", janela="InventoryPanel"))
        c.executar(ca.PAUSAR)          # retoma
        self.assertFalse(obs.esta_pausado())
        self.assertIsNotNone(obs.registrar("clique_recebido",
                                           janela="InventoryPanel"))

    def test_indicador_le_eventos_do_pipeline(self):
        obs = op.ObservacaoPassiva(relogio=relogio(), fonte="teste-kit06")
        c = ca.ControleAcesso(relogio=relogio(), pipeline=obs)
        c.executar(ca.OBSERVAR)
        obs.registrar("clique_recebido", janela="InventoryPanel")
        self.assertEqual(1, c.indicador()["eventos"])


# ========================================================= modo ativo =========
class TestTravaModoAtivo(unittest.TestCase):

    def test_habilitar_modo_ativo_sempre_falha(self):
        c = ca.ControleAcesso(relogio=relogio())
        self.assertIsNone(c.habilitar_modo_ativo())
        self.assertEqual(1, c.modo_ativo_pedidos)
        self.assertEqual("passivo", c.modo)
        self.assertIn("modo_ativo_proibido",
                      c.resumo()["degradacoes_por_motivo"])

    def test_executar_acao_ativa_recusada(self):
        c = ca.ControleAcesso(relogio=relogio())
        self.assertIsNone(c.executar("save"))
        self.assertIn("acao_ativa_proibida",
                      c.resumo()["degradacoes_por_motivo"])

    def test_observar_nao_abre_porta_ativa(self):
        c = ca.ControleAcesso(relogio=relogio())
        c.executar(ca.OBSERVAR)
        self.assertIsNone(c.executar("emitir_clique"))
        self.assertEqual("passivo", c.modo)
        self.assertFalse(hasattr(c, "executar_acao"))


# ========================================================= marcacao ============
class TestMarcacao(unittest.TestCase):

    def test_marcar_exige_observacao(self):
        c = ca.ControleAcesso(relogio=relogio())
        self.assertIsNone(c.marcar_problema("botao sumiu"))
        self.assertIn("marcar_sem_observacao",
                      c.resumo()["degradacoes_por_motivo"])

    def test_marcar_registra_contexto(self):
        c = ca.ControleAcesso(relogio=relogio(), pipeline=PipelineFalso())
        c.executar(ca.OBSERVAR)
        c.atualizar_contexto(janela="InventoryPanel")
        ev = c.processar_tecla("F9", descricao="tooltip cortado")
        self.assertEqual(ca.MARCAR_PROBLEMA, ev["acao"])
        m = c.marcacoes()[0]
        self.assertEqual("tooltip cortado", m["descricao"])
        self.assertEqual("InventoryPanel", m["janela"])
        self.assertFalse(m["foco_forcado"])

    def test_marcar_durante_pausa_permitido(self):
        pf = PipelineFalso()
        c = ca.ControleAcesso(relogio=relogio(), pipeline=pf)
        c.executar(ca.OBSERVAR)
        c.executar(ca.PAUSAR)
        self.assertIsNotNone(c.marcar_problema("vi o bug"))
        self.assertTrue(c.marcacoes()[0]["pausado_no_momento"])

    def test_teto_problemas_respeitado(self):
        c = ca.ControleAcesso(relogio=relogio(), pipeline=PipelineFalso(),
                              teto_problemas=2)
        c.executar(ca.OBSERVAR)
        self.assertIsNotNone(c.marcar_problema("a"))
        self.assertIsNotNone(c.marcar_problema("b"))
        self.assertIsNone(c.marcar_problema("c"))
        self.assertIn("teto_problemas_atingido",
                      c.resumo()["degradacoes_por_motivo"])


# ========================================================= export ==============
class TestExport(unittest.TestCase):

    def test_export_sem_dados_recusado(self):
        with tempfile.TemporaryDirectory() as d:
            c = ca.ControleAcesso(relogio=relogio(), pasta_export=d)
            self.assertIsNone(c.exportar())
            self.assertIn("exportar_sem_dados",
                          c.resumo()["degradacoes_por_motivo"])

    def test_export_grava_arquivo_local_sem_ia(self):
        with tempfile.TemporaryDirectory() as d:
            c = ca.ControleAcesso(relogio=relogio(), pasta_export=d,
                                  pipeline=PipelineFalso())
            c.executar(ca.OBSERVAR)
            c.marcar_problema("contraste baixo")
            caminho = c.exportar()
            self.assertTrue(os.path.isfile(caminho))
            with open(caminho, encoding="utf-8") as fh:
                doc = json.load(fh)
        self.assertEqual(ca.ESQUEMA_EXPORT, doc["esquema"])
        self.assertEqual("NAO_EXERCITADO", doc["runtime"])
        self.assertEqual(1, len(doc["marcacoes"]))
        self.assertEqual(0, doc["foco_forcado"])
        self.assertFalse(doc["encerrou_sessao"])

    def test_export_aceita_caminho_relativo_na_pasta(self):
        with tempfile.TemporaryDirectory() as d:
            c = ca.ControleAcesso(relogio=relogio(), pasta_export=d,
                                  pipeline=PipelineFalso())
            c.executar(ca.OBSERVAR)
            caminho = c.exportar("meu-export.json")
            self.assertEqual(os.path.join(d, "meu-export.json"), caminho)

    def test_contrato_kit07_declarado_honesto(self):
        # CONTRATO KIT-06F: a API existe, mas a integracao esta BLOQUEADA pelo
        # gate (KIT-07R REPROVADO). O descritor nao pode mentir "NAO_IMPLEMENTADO"
        # nem fingir pacote compartilhavel.
        contrato = ca.contrato_kit07()
        self.assertEqual(ca.ESQUEMA_EXPORT, contrato["esquema"])
        self.assertIn("GATE_NAO_SATISFEITO", contrato["status_kit07"])
        self.assertTrue(contrato["api_kit07_existe"])
        self.assertFalse(contrato["integracao_efetiva"])
        self.assertTrue(contrato["export_bruto_local"])
        self.assertFalse(contrato["pacote_compartilhavel"])
        self.assertIn("marcacoes", contrato["campos_obrigatorios"])
        self.assertIn("coleta", contrato["campos_obrigatorios"])


# ========================================================= indicador ===========
class TestIndicador(unittest.TestCase):

    def test_indicador_transicoes(self):
        pf = PipelineFalso()
        c = ca.ControleAcesso(relogio=relogio(), pipeline=pf)
        self.assertEqual("parado", c.indicador()["estado"])
        c.executar(ca.OBSERVAR)
        self.assertEqual("observando", c.indicador()["estado"])
        c.executar(ca.PAUSAR)
        self.assertEqual("pausado", c.indicador()["estado"])
        self.assertIn("COLETA:", c.texto_indicador())

    def test_indicador_mostra_contexto_e_marcacoes(self):
        c = ca.ControleAcesso(relogio=relogio(), pipeline=PipelineFalso())
        c.executar(ca.OBSERVAR)
        c.atualizar_contexto(janela="MapPanel")
        c.marcar_problema("x")
        ind = c.indicador()
        self.assertEqual("MapPanel", ind["janela"])
        self.assertEqual(1, ind["marcacoes"])
        self.assertIn("MapPanel", ind["texto"])


# ========================================================= roteiro =============
class TestRoteiro(unittest.TestCase):

    def test_roteiro_offline_completo(self):
        roteiro = [
            {"contexto": {"janela": "InventoryPanel"}},
            {"tecla": "F7"},                        # observar
            {"contexto": {"chat_aberto": True}},
            {"tecla": "F9", "descricao": "ignorar"},   # guard: nao marca
            {"contexto": {"chat_aberto": False}},
            {"tecla": "F9", "descricao": "tooltip cortado"},
            {"tecla": "F8"},                        # pausar
            {"tecla": "F8"},                        # retomar
        ]
        prog = None
        ctrl, eventos = ca._correr_roteiro(
            roteiro, pipeline=PipelineFalso())
        self.assertEqual(1, len(ctrl.marcacoes()))
        self.assertEqual("tooltip cortado", ctrl.marcacoes()[0]["descricao"])
        self.assertIn(ca.MOTIVO_GUARD_CHAT,
                      ctrl.resumo()["degradacoes_por_motivo"])
        acoes = [e["acao"] for e in eventos]
        self.assertEqual([ca.OBSERVAR, ca.MARCAR_PROBLEMA, ca.PAUSAR,
                          ca.RETOMAR], acoes)


# =============================================== correcoes KIT-06F (F1-F8) ====
class TestCorrecoesKit06F(unittest.TestCase):
    """Prova POSITIVA das correcoes F1-F8 (contrato revisado no KIT-06F)."""

    def test_F1_mapa_vazio_nao_reativa_defaults(self):
        c = ca.ControleAcesso(atalhos={})
        self.assertEqual({}, c.atalhos)
        self.assertIsNone(c.processar_tecla("F7"))
        self.assertFalse(c.observando())

    def test_F1_mapa_totalmente_rejeitado_nao_reativa(self):
        norm, problemas = ca.valida_atalhos({ca.OBSERVAR: "Return"})
        self.assertEqual({}, norm)
        self.assertTrue(problemas)
        c = ca.ControleAcesso(atalhos=norm)
        self.assertIsNone(c.processar_tecla("F7"))
        self.assertFalse(c.observando())

    def test_F2_retomar_despachado_tem_efeito(self):
        pf = PipelineFalso()
        c = ca.ControleAcesso(atalhos={ca.OBSERVAR: "F7", ca.PAUSAR: "F8",
                                       ca.RETOMAR: "F6"},
                              relogio=relogio(), pipeline=pf)
        c.processar_tecla("F7")
        c.processar_tecla("F8")
        self.assertTrue(pf.esta_pausado())
        ev = c.processar_tecla("F6")
        self.assertEqual(ca.RETOMAR, ev["acao"])
        self.assertFalse(pf.esta_pausado())

    def test_F2_parar_sem_terminal_pelo_toggle(self):
        pf = PipelineFalso()
        c = ca.ControleAcesso(relogio=relogio(), pipeline=pf)
        c.executar(ca.OBSERVAR)
        self.assertTrue(c.observando())
        c.executar(ca.OBSERVAR)              # 2o toque = PARAR sem terminal
        self.assertFalse(c.observando())
        self.assertTrue(pf.esta_pausado())

    def test_F3_indicador_sem_pipeline_e_lacuna(self):
        c = ca.ControleAcesso(relogio=relogio())
        c.executar(ca.OBSERVAR)
        ind = c.indicador()
        self.assertEqual("sem_pipeline", ind["estado"])
        self.assertFalse(ind["coleta_operante"])
        self.assertIn("coleta_sem_pipeline",
                      c.resumo()["degradacoes_por_motivo"])

    def test_F3_parado_nao_coleta_no_pipeline(self):
        obs = op.ObservacaoPassiva(relogio=relogio(), fonte="teste-kit06f")
        c = ca.ControleAcesso(relogio=relogio(), pipeline=obs)
        self.assertEqual("parado", c.indicador()["estado"])
        self.assertIsNone(obs.registrar("clique_recebido",
                                        janela="InventoryPanel"))

    def test_F4_export_inclui_evento_degradacao_e_correlacao(self):
        with tempfile.TemporaryDirectory() as d:
            obs = op.ObservacaoPassiva(relogio=relogio(), fonte="teste-kit06f")
            c = ca.ControleAcesso(relogio=relogio(), pipeline=obs,
                                  pasta_export=d, id_sessao="sessao-f4")
            c.processar_tecla("F7")
            ev = obs.registrar("clique_recebido", janela="InventoryPanel")
            c.atualizar_contexto(chat_aberto=True)
            c.processar_tecla("F9")
            c.atualizar_contexto(chat_aberto=False)
            with open(c.exportar(), encoding="utf-8") as fh:
                doc = json.load(fh)
        texto = json.dumps(doc)
        self.assertIn(ev["id"], texto)
        self.assertIn("guard_chat", texto)
        self.assertEqual("sessao-f4", doc["correlacao"]["sessao_controle"])
        self.assertEqual(obs.id_sessao, doc["correlacao"]["sessao_coleta"])
        self.assertEqual(1, doc["indicador"]["eventos"])

    def test_F5_export_falha_io_sem_propagar(self):
        with tempfile.TemporaryDirectory() as d:
            blocker = os.path.join(d, "arquivo")
            with open(blocker, "w", encoding="utf-8") as fh:
                fh.write("sentinela")
            c = ca.ControleAcesso(relogio=relogio(), pasta_export=blocker)
            c.executar(ca.OBSERVAR)
            self.assertIsNone(c.exportar())
            with open(blocker, encoding="utf-8") as fh:
                self.assertEqual("sentinela", fh.read())
            self.assertIn("export_falha_io",
                          c.resumo()["degradacoes_por_motivo"])

    def test_F6_janela_none_limpa_e_omitir_mantem(self):
        c = ca.ControleAcesso(relogio=relogio(), pipeline=PipelineFalso())
        c.executar(ca.OBSERVAR)
        c.atualizar_contexto(janela="InventoryPanel")
        c.atualizar_contexto(janela=None)         # LIMPA
        c.marcar_problema("fora")
        self.assertIsNone(c.marcacoes()[0]["janela"])
        c.atualizar_contexto(janela="MapPanel")
        c.atualizar_contexto(chat_aberto=True)    # OMITE janela -> mantem
        self.assertEqual("MapPanel", c.contexto()["janela"])

    def test_F6_marcacoes_snapshot_defensivo(self):
        c = ca.ControleAcesso(relogio=relogio(), pipeline=PipelineFalso())
        c.executar(ca.OBSERVAR)
        c.marcar_problema("original")
        fora = c.marcacoes()
        fora[0]["descricao"] = "alterada fora"
        self.assertEqual("original", c.marcacoes()[0]["descricao"])

    def test_F6_coleta_aninhado_snapshot_defensivo(self):
        """F6 (KIT-06F): o snapshot defensivo vale TAMBEM para os objetos
        ANINHADOS do pipeline (`coleta.eventos[*].quadro`/`dados`). Mutar o
        documento exportado NAO pode contaminar a evidencia interna retida nem
        os exports seguintes — o F6 do KIT-06R so cobria o caso plano
        (`marcacoes`)."""
        obs = op.ObservacaoPassiva(relogio=relogio(), fonte="teste-f6-aninhado")
        c = ca.ControleAcesso(relogio=relogio(), pipeline=obs,
                              id_sessao="sessao-f6-aninhado")
        c.executar(ca.OBSERVAR)
        obs.registrar("clique_recebido", janela="InventoryPanel")

        doc = c.documento_export()
        evento = doc["coleta"]["eventos"][0]
        self.assertIsInstance(evento.get("quadro"), dict)
        evento["quadro"]["nota"] = "ALTERADO PELO CONSUMIDOR"
        evento["dados"]["injetado"] = "ALTERADO"

        doc2 = c.documento_export()
        ev2 = doc2["coleta"]["eventos"][0]
        interno = obs.eventos()[0]
        self.assertNotEqual("ALTERADO PELO CONSUMIDOR", ev2["quadro"].get("nota"))
        self.assertNotIn("injetado", ev2["dados"])
        # a evidencia INTERNA do pipeline tambem fica intacta
        self.assertNotEqual("ALTERADO PELO CONSUMIDOR",
                            interno["quadro"].get("nota"))
        self.assertNotIn("injetado", interno["dados"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
