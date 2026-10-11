#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT-08 - suite offline do visualizador HTML local (unittest, sem rede/jogo).

Roda com ou sem modulo mutado: o modulo SOB TESTE e carregado de
`KIT08_MODULO` (default = ../visualizador.py), e o avaliador KIT-09 de
`KIT08_KIT09` (default = tools/automacao/cenarios/kit09.py). Assim a
contra-prova roda ESTA suite contra um `visualizador.py` com defeito plantado
e confere o conjunto EXATO de testes que devem falhar.

Execucao real: `python tools/automacao/kit08/teste_visualizador_kit08.py`.
"""
import importlib.util
import json
import os
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))


def _carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CAMINHO_MOD = os.environ.get("KIT08_MODULO") or os.path.join(AQUI, "visualizador.py")
V = _carregar("kit08_visualizador_sob_teste", CAMINHO_MOD)

FIXTURE_VERDADE = os.path.join(RAIZ, "tools", "automacao", "cenarios",
                               "kit09-verdade.entrada.json")
FIXTURE_IDENT = os.path.join(RAIZ, "tools", "automacao", "cenarios",
                             "kit09-identidade.json")

PAYLOAD = '<img src=x onerror="alert(1)"><script>alert(2)</script>'


def _criterio(cid="KIT09-x", estado="OK", **kw):
    c = {"id": cid, "mod": "RoguelikeSkillTreeVisualizer", "estado": estado,
         "classe": "runtime", "procedencia": "runtime", "esperado": "e",
         "observado": "o", "evidencia": ["scratch/kit/k08/prova.json"],
         "motivo": "ok", "tarefa_origem": "t_x", "prova_runtime": True,
         "fonte_sha": "a" * 64, "dll_sha": "b" * 64, "config_sha": "c" * 64,
         "sessao": "S1", "origin_campo": "ignorado"}
    c.update(kw)
    return c


def _doc(**kw):
    d = {"esquema": "KIT-08/sessao/1", "mod": "RoguelikeSkillTreeVisualizer",
         "identidade": {"fonte_sha": "a" * 64, "dll_sha": "b" * 64, "config_sha": "c" * 64},
         "build": {"id": "build-1", "versao_jogo": "2022.3.62f3", "bepinex": "5.4.23.5"},
         "sessao": {"id": "S1"}, "criterios": [_criterio()]}
    d.update(kw)
    return d


class TestEscape(unittest.TestCase):
    def test_escapar_payload_vira_texto(self):
        out = V.escapar(PAYLOAD)
        self.assertNotIn("<script", out)
        self.assertNotIn("<img", out)
        self.assertIn("&lt;script&gt;", out)
        self.assertIn("&quot;", out)

    def test_escapar_none_e_vazio(self):
        self.assertEqual(V.escapar(None), "")


class TestHtmlSeguro(unittest.TestCase):
    def _html(self):
        doc = _doc(criterios=[_criterio(observado=PAYLOAD, motivo=PAYLOAD, id="KIT09-a")])
        doc["imagens"] = {"KIT09-a": "http://evil.example/x.png"}
        return V.renderizar(doc)

    def test_html_sem_tag_script_de_dado(self):
        h = self._html()
        self.assertNotIn("<script", h)
        self.assertIn("&lt;script&gt;", h)

    def test_html_sem_rede(self):
        h = self._html()
        self.assertNotIn("http://", h)
        self.assertNotIn("https://", h)
        self.assertNotIn('src="//', h)

    def test_csp_script_none(self):
        h = self._html()
        self.assertIn("script-src 'none'", h)
        self.assertNotIn("script-src 'unsafe-inline'", h)

    def test_imagem_remota_recusada(self):
        h = self._html()
        self.assertIn("recusada", h)
        self.assertNotIn("evil.example", h)

    def test_campos_por_caso_presentes(self):
        h = V.renderizar(_doc())
        for rot in ("esperado", "observado", "motivo/prova", "prova", "sessao",
                    "fonte/dll/config", "lacunas"):
            self.assertIn(rot, h)

    def test_secao_humana_separada_e_pendente(self):
        h = V.renderizar(_doc())
        self.assertIn("Aceite HUMANO", h)
        self.assertIn("PENDENTE (nao concedido", h)

    def test_determinismo_bytes(self):
        d = _doc()
        self.assertEqual(V.renderizar(d), V.renderizar(json.loads(json.dumps(d))))


class TestReferenciaLocal(unittest.TestCase):
    def test_aceita_relativa(self):
        for ref in ("scratch/kit/k08/x.png", "a/b.json"):
            ok, _ = V.referencia_local_segura(ref)
            self.assertTrue(ok, ref)

    def test_recusa_esquemas_e_absolutos(self):
        for ref in ("http://x/a.png", "https://x", "javascript:alert(1)",
                    "data:image/png;base64,AAA", "file:///etc/passwd",
                    "//host/a.png", "/abs/a", "C:/win/a", "\\\\net\\s\\a",
                    "a/../../b", "a//b", "", "  ", "a\nb"):
            ok, motivo = V.referencia_local_segura(ref)
            self.assertFalse(ok, "deveria recusar %r (motivo=%r)" % (ref, motivo))


class TestComparacao(unittest.TestCase):
    def test_contexto_compativel_compara(self):
        base = _doc(criterios=[_criterio(estado="OK", prova_runtime=True)])
        cand = _doc(criterios=[_criterio(estado="REPROVADO", prova_runtime=False)])
        r = V.comparar(base, cand)
        self.assertTrue(r["comparavel"])
        self.assertEqual(r["estado"], "FALHOU")
        self.assertEqual(r["regressoes"], ["KIT09-x"])

    def test_contexto_incompativel_recusa(self):
        base = _doc()
        cand = _doc()
        cand["identidade"] = dict(cand["identidade"])
        cand["build"] = dict(cand["build"], versao_jogo="2022.9.99f9")
        r = V.comparar(base, cand)
        self.assertFalse(r["comparavel"])
        self.assertEqual(r["estado"], "INDETERMINADO")
        self.assertTrue(r["motivos"])

    def test_contexto_incompleto_recusa(self):
        base = _doc(build={"id": "b"})  # sem versao_jogo/bepinex
        cand = _doc()
        r = V.comparar(base, cand)
        self.assertFalse(r["comparavel"])


class TestAprovacaoStale(unittest.TestCase):
    def test_stale_quando_fonte_muda(self):
        aprov = {"fonte_sha": "OLD", "dll_sha": "b" * 64}
        ctx = {"fonte_sha": "NEW", "dll_sha": "b" * 64}
        stale, motivos = V.aprovacao_stale(aprov, ctx)
        self.assertTrue(stale)
        self.assertTrue(any("FONTE ALTERADA" in m for m in motivos))

    def test_vigente_quando_igual(self):
        aprov = {"fonte_sha": "a" * 64}
        stale, _ = V.aprovacao_stale(aprov, {"fonte_sha": "a" * 64})
        self.assertFalse(stale)

    def test_stale_quando_contexto_atual_omite_hash(self):
        stale, motivos = V.aprovacao_stale({"dll_sha": "b" * 64}, {})
        self.assertTrue(stale)


class TestVeredito(unittest.TestCase):
    def test_fixture_nunca_passa(self):
        # estado OK, mas sem prova de runtime / procedencia fixture -> NAO PASSOU
        self.assertNotEqual(V.veredito_tecnico(_criterio(prova_runtime=False)), "PASSOU")
        c = _criterio(procedencia="fixture")
        self.assertNotEqual(V.veredito_tecnico(c), "PASSOU")
        self.assertEqual(V.veredito_tecnico(_criterio(estado="REPROVADO",
                                                       prova_runtime=False)), "FALHOU")
        self.assertEqual(V.veredito_tecnico(_criterio(estado="NAO_EXERCITADO",
                                                       prova_runtime=False)), "NAO_EXERCITADO")
        self.assertEqual(V.veredito_tecnico(_criterio(estado="INDETERMINADO",
                                                       prova_runtime=False)), "INDETERMINADO")

    def test_passa_so_com_runtime(self):
        self.assertEqual(V.veredito_tecnico(_criterio()), "PASSOU")

    def test_fixture_rotulada_nunca_passa_no_doc(self):
        d = _doc(criterios=[_criterio()])  # OK + prova_runtime=True
        d["rotulo_fixture"] = "sessao-sintetica"
        self.assertTrue(V.origem_sintetica(d))
        cont = V._contagem(V._itens_de(d), V.origem_sintetica(d))
        self.assertNotIn("PASSOU", cont)
        self.assertEqual(cont.get("NAO_EXERCITADO"), 1)
        self.assertIn("ORIGEM SINTETICA/FIXTURE", V.renderizar(d))
        # sem o rotulo, o mesmo criterio PASSA (controle positivo)
        self.assertIn("PASSOU", V._contagem(V._itens_de(_doc())))


class TestReusoKit09(unittest.TestCase):
    def test_fixture_sintetica_nunca_ok(self):
        with open(FIXTURE_VERDADE, encoding="utf-8") as fh:
            entrada = json.load(fh)
        with open(FIXTURE_IDENT, encoding="utf-8") as fh:
            ident = json.load(fh)
        entrada = dict(entrada)
        entrada["identidade"] = ident
        doc = V.montar_doc(entrada)
        criterios = V._itens_de(doc)
        self.assertEqual(len(criterios), 21)
        self.assertTrue(all(V.veredito_tecnico(c) != "PASSOU" for c in criterios))
        h = V.renderizar(doc)
        self.assertNotIn("<script", h)


if __name__ == "__main__":
    unittest.main(verbosity=2)
