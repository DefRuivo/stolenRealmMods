#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes REAIS do orquestrador CIC-1 (tools/automacao/ciclo/ciclo.py).

Cada teste tem controle NEGATIVO: o que tem de dar igual quando nada muda e o
que tem de mudar quando a fonte muda. O modo CLI e exercitado de verdade
(subprocesso), incluindo a invalidacao por mudanca de bytes e o REUSO de um
AUT-3 cujo snapshot NAO corresponde mais aos bytes atuais.

Cobre as correcoes funcionais da 1a integracao (CICLO-VALIDACAO-escopo, secao
"Correcoes funcionais"):
  * reuso de AUT-3 confronta o snapshot da fonte contra os bytes ATUAIS;
  * identidade suficiente = fonte_sha E dll_sha (igual a decisao.py);
  * estado/exit/resumo/fila incorporam as falhas_automaticas da decisao;
  * sem progresso com limite ESCALA ao supervisor tecnico (nao ao dono);
  * a fila aponta a CAUSA ou marca explicitamente desconhecida.

    python tools/automacao/ciclo/test_ciclo.py

Exit 0 = todos passaram · 1 = algum falhou.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ciclo  # noqa: E402

PY = sys.executable
CICLO = os.path.join(AQUI, "ciclo.py")
MOD_DLL = "BetterTooltips/bin/Release/netstandard2.1/BetterTooltips.dll"


def _git(repo, *args):
    r = subprocess.run(["git"] + list(args), cwd=repo, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, universal_newlines=True)
    if r.returncode != 0:
        raise RuntimeError("git %s falhou: %s" % (" ".join(args), r.stderr))
    return r.stdout


def _escrever(repo, rel, texto, binario=False):
    caminho = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    if binario:
        with open(caminho, "wb") as fh:
            fh.write(texto)
    else:
        with open(caminho, "w", encoding="utf-8") as fh:
            fh.write(texto)
    return caminho


def _mini_repo(base, nome="mini", com_dll=True, com_checker=True):
    """Repo git minimo e REAL (o git e a base da identidade de fonte).

    `com_dll` cria uma DLL Release ficticia (sem ela dll_sha e None e a
    identidade e INSUFICIENTE -- nunca APROVADO). `com_checker` cria o
    arquivo-evidencia do conferidor `check_x`.
    """
    repo = os.path.join(base, nome)
    os.makedirs(repo, exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "teste@local")
    _git(repo, "config", "user.name", "teste")
    _escrever(repo, "a.py", "VALOR = 1\n")
    if com_checker:
        _escrever(repo, "tools/check_x.py", "raise SystemExit(0)\n")
    if com_dll:
        _escrever(repo, MOD_DLL, b"DLL-FALSA-CIC1", binario=True)
    _git(repo, "add", "-A")

    return repo


def _aut3_ok():
    return {
        "veredito": "VERDE",
        "builds": [], "suite": [], "contra_provas": [],
        "checagens": [
            {"id": "check_x", "mod": "BetterTooltips", "classe": "estrutura", "desc": "conferidor",
             "estado": "OK", "exit_code": 0, "comando": "python tools/check_x.py"},
        ],
        "guarda_perfil": {"intacto": True}, "guarda_repo": {"intacto": True},
        "fases_puladas": [], "builds_executados": 0, "limite_builds": 6,
    }


def _aut3_reprovado(detalhe="chave duplicada plantada"):
    d = _aut3_ok()
    d["veredito"] = "REPROVADO"
    d["checagens"] = [
        {"id": "check_x", "mod": "BetterTooltips", "classe": "estrutura", "desc": "conferidor",
         "estado": "REPROVOU", "exit_code": 1, "comando": "python tools/check_x.py",
         "detalhe": detalhe},
    ]
    return d


def _com_snapshot(aut3, repo):
    """Preenche o snapshot de fonte do AUT-3 com os bytes ATUAIS do repo.

    Sem esse snapshot um AUT-3 reusado NAO prova os bytes atuais (nova rodada).
    """
    d = json.loads(json.dumps(aut3))
    snap = ciclo.snapshot_fonte(repo)
    d.setdefault("guarda_repo", {})["sha_antes"] = dict(snap)
    d.setdefault("guarda_repo", {})["sha_depois"] = dict(snap)
    d.setdefault("estados_separados", {})["fonte"] = dict(snap)
    d["repo"] = os.path.abspath(repo)
    d["ciclo_identidade"] = ciclo.identidade(repo)
    return d


def _com_snapshot_vazio(aut3):
    d = json.loads(json.dumps(aut3))
    d.setdefault("guarda_repo", {})["sha_antes"] = {}
    d["repo"] = "C:/repo-que-nao-existe"
    return d


class BaseCiclo(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="cic1-teste-", dir=ciclo.area_trabalho())
        self.repo = _mini_repo(self.base)

    def tearDown(self):
        # objetos .git sao read-only no Windows: rmtree puro falha e a sobra
        # contamina a proxima rodada de teste (foi o que encheu o scratch).
        ciclo._remover_arvore(self.base)

    def _cli(self, *args):
        r = subprocess.run([PY, CICLO] + list(args), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True, encoding="utf-8")
        return r.returncode, r.stdout, r.stderr

    def _aut3_no_repo(self, aut3, repo=None):
        """Escreve o AUT-3 em docs/automacao (excluido do universo do snapshot)."""
        repo = repo or self.repo
        return _escrever(repo, "docs/automacao/AUT-3-resultado.json",
                         json.dumps(aut3, ensure_ascii=False))


class TestIdentidade(BaseCiclo):
    def test_identidade_estavel_e_sensivel_a_bytes(self):
        i1 = ciclo.identidade(self.repo)
        self.assertTrue(i1["fonte_sha"], "identidade precisa ter fonte_sha")
        self.assertEqual(i1["fonte_sha"], ciclo.identidade(self.repo)["fonte_sha"])
        _escrever(self.repo, "a.py", "VALOR = 2\n")
        i2 = ciclo.identidade(self.repo)
        self.assertNotEqual(i1["fonte_sha"], i2["fonte_sha"])
        _escrever(self.repo, "b.py", "NOVO = True\n")
        i3 = ciclo.identidade(self.repo)
        self.assertNotEqual(i2["fonte_sha"], i3["fonte_sha"])

    def test_identidade_tem_dll_sha_quando_ha_release(self):
        ident = ciclo.identidade(self.repo)
        self.assertTrue(ident["dll_sha"], "com bin/Release presente dll_sha nao pode ser None")
        self.assertIn("BetterTooltips", ident["dlls"])

    def test_identidade_fail_closed_sem_git(self):
        sem_git = os.path.join(self.base, "sem-git")
        os.makedirs(sem_git, exist_ok=True)
        _escrever(sem_git, "x.py", "x=1\n")
        with self.assertRaises(RuntimeError):
            ciclo.identidade(sem_git)

    def test_identidade_suficiente_exige_fonte_e_dll(self):
        # Igual a decisao.py: fonte_sha E dll_sha. So fonte NAO basta (nunca OK).
        self.assertTrue(ciclo.identidade_suficiente({"fonte_sha": "a" * 64, "dll_sha": "b" * 64}))
        self.assertFalse(ciclo.identidade_suficiente({"fonte_sha": "a" * 64, "dll_sha": None}))
        self.assertFalse(ciclo.identidade_suficiente({"fonte_sha": "a" * 64}))
        self.assertFalse(ciclo.identidade_suficiente({"fonte_sha": None, "dll_sha": "b" * 64}))
        self.assertFalse(ciclo.identidade_suficiente(None))


class TestSnapshotReuso(BaseCiclo):
    def test_snapshot_confere_aprova(self):
        aut3 = _com_snapshot(_aut3_ok(), self.repo)
        ok, motivo, det = ciclo.confrontar_snapshot(aut3, self.repo)
        self.assertTrue(ok, motivo)
        self.assertEqual(det.get("alterados_total"), 0)
        self.assertEqual(det.get("criados_total"), 0)

    def test_snapshot_divergente_reprova(self):
        aut3 = _com_snapshot(_aut3_ok(), self.repo)
        _escrever(self.repo, "a.py", "VALOR = 999\n")  # muta a fonte depois do snapshot
        ok, motivo, det = ciclo.confrontar_snapshot(aut3, self.repo)
        self.assertFalse(ok, "snapshot velho NAO pode ser assinado com a fonte nova")
        self.assertIn("diverg", motivo)
        self.assertGreaterEqual(det.get("alterados_total", 0), 1)

    def test_snapshot_ausente_insuficiente(self):
        aut3 = _com_snapshot_vazio(_aut3_ok())
        ok, motivo, _ = ciclo.confrontar_snapshot(aut3, self.repo)
        self.assertFalse(ok)
        self.assertIn("snapshot", motivo.lower())

    def test_snapshot_arquivo_novo_conta_como_divergencia(self):
        aut3 = _com_snapshot(_aut3_ok(), self.repo)
        _escrever(self.repo, "novo_agente.py", "x = 1\n")  # outro agente escreveu
        ok, _, det = ciclo.confrontar_snapshot(aut3, self.repo)
        self.assertFalse(ok)
        self.assertGreaterEqual(det.get("criados_total", 0), 1)


class TestCriteriosEFila(BaseCiclo):
    def test_falha_vira_item_de_fila_declarativo(self):
        ident = ciclo.identidade(self.repo)
        criterios = ciclo.criterios_aut3(_aut3_reprovado(), ident)
        fila = ciclo.montar_fila(criterios, ident)
        self.assertEqual(len(fila), 1)
        item = fila[0]
        self.assertTrue(item["requer_nova_rodada"])
        self.assertFalse(item["execucao_automatica"], "fila nao executa comando de correcao")
        self.assertEqual(item["fonte_sha"], ident["fonte_sha"])
        self.assertIn("check_x", item["criterio"])
        self.assertTrue(item["evidencia"], "a evidencia (script conferidor) tem de ir na fila")
        self.assertIn("instrucao", item)

    def test_tudo_ok_gera_fila_vazia(self):
        ident = ciclo.identidade(self.repo)
        criterios = ciclo.criterios_aut3(_aut3_ok(), ident)
        self.assertEqual(ciclo.montar_fila(criterios, ident), [])
        self.assertFalse(ciclo.criterios_reprovados(criterios))

    def test_guarda_violada_reprova(self):
        ident = ciclo.identidade(self.repo)
        aut3 = _aut3_ok()
        aut3["guarda_repo"] = {"intacto": False}
        criterios = ciclo.criterios_aut3(aut3, ident)
        guarda = [c for c in criterios if c["id"] == "guarda_repo"][0]
        self.assertEqual(guarda["estado"], "REPROVADO")

    def test_sem_identidade_build_nao_vira_ok(self):
        aut3 = _aut3_ok()
        aut3["builds"] = [{"id": "build_X", "mod": "X", "estado": "OK", "exit_code": 0,
                           "sha_sandbox": "abc", "fonte_dll_provada": True}]
        criterios = ciclo.criterios_aut3(aut3, {"fonte_sha": "a" * 64, "dll_sha": None})
        b = [c for c in criterios if c["id"] == "build_X"][0]
        self.assertEqual(b["estado"], "NAO_EXERCITADO")

    def test_contra_prova_ok_e_reprovada(self):
        ident = ciclo.identidade(self.repo)
        aut3 = _aut3_ok()
        aut3["contra_provas"] = [
            {"id": "cp_um", "veredito": "PROVA_OK", "exit_com_defeito": 1, "exit_apos_correcao": 0,
             "arquivo": "BetterX/Patch.cs"},
            {"id": "cp_dois", "veredito": "PROVA_FALHOU", "exit_com_defeito": 0,
             "exit_apos_correcao": 0, "arquivo": "BetterX/Patch.cs"},
        ]
        criterios = ciclo.criterios_aut3(aut3, ident)
        por_id = {c["id"]: c["estado"] for c in criterios}
        self.assertEqual(por_id["cp_um"], "OK")
        self.assertEqual(por_id["cp_dois"], "REPROVADO")
        fila = ciclo.montar_fila(criterios, ident)
        item = [f for f in fila if f["criterio"] == "cp_dois"][0]
        self.assertFalse(item["causa_desconhecida"])
        self.assertEqual(item["causa"], "BetterX/Patch.cs")
        self.assertEqual(item["caminhos"], ["BetterX/Patch.cs"])

    def test_fila_aponta_causa_ou_desconhecido_explicito(self):
        ident = {"fonte_sha": "a" * 64, "dll_sha": "b" * 64}
        c_sem = ciclo._criterio("check_dup", "BetterTooltips", "REPROVADO", "offline",
                                "execucao", "sem duplicata", "exit=1", ["tools/check_dupes.py"],
                                "chave duplicada")
        fila = ciclo.montar_fila([c_sem], ident)
        self.assertTrue(fila[0]["causa_desconhecida"])
        self.assertEqual(fila[0]["caminhos"], [])
        self.assertEqual(fila[0]["roteamento"], "desconhecido")
        self.assertEqual(fila[0]["tarefa_origem"], "desconhecido")
        self.assertNotEqual(fila[0]["tarefa_origem"], ciclo.TAREFA,
                            "nao assinar o defeito com a tarefa do orquestrador por padrao")
        c_com = ciclo._criterio("cp_x", "X", "REPROVADO", "offline", "execucao", "e", "o",
                                ["tools/check.py"], "m", causa="BetterX/Patch.cs")
        fila2 = ciclo.montar_fila([c_com], ident)
        self.assertFalse(fila2[0]["causa_desconhecida"])
        self.assertEqual(fila2[0]["caminhos"], ["BetterX/Patch.cs"])

    def test_cobertura_runtime_e_residual_nao_falha(self):
        ident = ciclo.identidade(self.repo)
        aut3 = _aut3_ok()
        aut3["cobertura"] = {"itens": [
            {"id": "T-RSTV21", "mod": "RSTV", "estado": "NAO_EXERCITADO", "motivo": "precisa jogo"},
            {"id": "M1", "mod": "X", "estado": "OK_OFFLINE", "evidencia_aut3": "build ok"},
            {"id": "M9", "mod": "X", "estado": "REPROVADO", "evidencia_aut3": "quebrou"},
        ]}
        criterios = ciclo.criterios_aut3(aut3, ident)
        por_id = {c["id"]: (c["estado"], c["classe"]) for c in criterios}
        self.assertEqual(por_id["cobertura:T-RSTV21"], ("NAO_EXERCITADO", "runtime"))
        self.assertEqual(por_id["cobertura:M1"][0], "OK")
        self.assertEqual(por_id["cobertura:M9"][0], "REPROVADO")
        self.assertFalse([c for c in criterios if c["id"] == "cobertura:T-RSTV21" and c["estado"] == "OK"])


class TestTentativasEInvalidacao(BaseCiclo):
    def _prev(self, fonte_sha, fila, numero=1, seguidas=0):
        return {"esquema": ciclo.ESQUEMA, "identidade": {"fonte_sha": fonte_sha},
                "fila_correcao": fila, "estado": "REPROVADO",
                "tentativas": {"numero": numero, "sem_progresso_seguidas": seguidas}}

    def test_sem_progresso_quando_fonte_e_falhas_iguais(self):
        fila = [{"criterio": "check_x"}]
        prev = self._prev("a" * 64, fila)
        t = ciclo.avaliar_tentativas(prev, {"fonte_sha": "a" * 64}, fila)
        self.assertTrue(t["sem_progresso"])
        self.assertEqual(t["sem_progresso_seguidas"], 1)
        self.assertFalse(t["invalidou_anterior"])
        self.assertEqual(t["numero"], 2)

    def test_fonte_nova_invalida_anterior_e_nao_e_sem_progresso(self):
        fila = [{"criterio": "check_x"}]
        prev = self._prev("a" * 64, fila)
        t = ciclo.avaliar_tentativas(prev, {"fonte_sha": "b" * 64}, fila)
        self.assertFalse(t["sem_progresso"])
        self.assertTrue(t["invalidou_anterior"], "fonte mudou -> rodada anterior invalidada")

    def test_invalidacao_durante_rodada(self):
        self.assertEqual(ciclo.avaliar_invalidacao("a", "a"), (False, ""))
        inv, motivo = ciclo.avaliar_invalidacao("a", "b")
        self.assertTrue(inv)
        self.assertIn("mudou", motivo)
        self.assertTrue(ciclo.avaliar_invalidacao(None, "b")[0])

    def test_verificar_resultado(self):
        r = {"identidade": {"fonte_sha": "a" * 64, "dll_sha": "b" * 64}}
        self.assertEqual(ciclo.verificar_resultado(r, {"fonte_sha": "a" * 64, "dll_sha": "b" * 64})[0], True)
        self.assertFalse(ciclo.verificar_resultado(r, {"fonte_sha": "a" * 64, "dll_sha": "c" * 64})[0])
        self.assertFalse(ciclo.verificar_resultado(r, {"fonte_sha": "a" * 64})[0])
        self.assertEqual(ciclo.verificar_resultado(r, {"fonte_sha": "b" * 64})[0], False)
        self.assertEqual(ciclo.verificar_resultado({}, {"fonte_sha": "a" * 64})[0], False)

    def test_resultado_aut3_precisa_ser_reescrito(self):
        self.assertTrue(ciclo.resultado_reescrito(None, 10.0))
        self.assertFalse(ciclo.resultado_reescrito(10.0, 10.0))
        self.assertTrue(ciclo.resultado_reescrito(10.0, 11.0))
        self.assertFalse(ciclo.resultado_reescrito(10.0, None))


class TestEscalonamento(BaseCiclo):
    def test_limite_de_numero_escalona_ao_supervisor(self):
        escalar, motivo, destino = ciclo.avaliar_escalonamento(True, {"numero": 6, "sem_progresso_seguidas": 0}, 5)
        self.assertTrue(escalar)
        self.assertEqual(destino, "supervisor")
        self.assertIn("supervisor", motivo.lower())
        self.assertIn("nao", motivo.lower())  # explicita que NAO e o dono
        self.assertIn("dono", motivo.lower())

    def test_sem_progresso_no_limite_escalona(self):
        escalar, motivo, destino = ciclo.avaliar_escalonamento(True, {"numero": 3, "sem_progresso_seguidas": 5}, 5)
        self.assertTrue(escalar, "sem progresso no limite tem de ESCALAR, nao so avisar")
        self.assertEqual(destino, "supervisor")
        self.assertIn("supervisor", motivo.lower())

    def test_sem_progresso_abaixo_do_limite_nao_preenche_motivo(self):
        escalar, motivo, destino = ciclo.avaliar_escalonamento(True, {"numero": 2, "sem_progresso_seguidas": 2}, 5)
        self.assertFalse(escalar)
        self.assertEqual(motivo, "", "motivo_escalacao nao pode contradizer escala=False")
        self.assertEqual(destino, "ciclo")

    def test_sem_falha_nunca_escalona(self):
        escalar, motivo, _ = ciclo.avaliar_escalonamento(False, {"numero": 99, "sem_progresso_seguidas": 99}, 5)
        self.assertFalse(escalar)
        self.assertEqual(motivo, "")


class TestDecisaoOpcional(BaseCiclo):
    def test_carregar_decisao_informa_presenca(self):
        modulo, erro, presente = ciclo.carregar_decisao()
        if presente:
            self.assertIsNotNone(modulo)
            self.assertTrue(hasattr(modulo, "consolidar"))
        else:
            self.assertIsNone(modulo)
            self.assertIn("decisao.py", erro)

    def test_decisao_minima_nao_aprova_sem_dll(self):
        ident = {"fonte_sha": "a" * 64, "dll_sha": None}
        d = ciclo.decisao_minima(ciclo.criterios_aut3(_aut3_ok(), ident), ident, [])
        for chave in ("por_mod", "falhas_automaticas", "pendencias_humanas",
                      "pronto_para_decisao", "aceite_humano", "publicacao"):
            self.assertIn(chave, d)
        self.assertFalse(d["pronto_para_decisao"], "identidade insuficiente nunca fica pronta")

    def test_fallback_sem_modulo_preserva_lacuna_runtime_e_paridade(self):
        from unittest.mock import patch
        ident = ciclo.identidade(self.repo)
        criterio = ciclo._criterio("runtime_ausente", "BetterTooltips", "NAO_EXERCITADO",
                                  "runtime", "runtime", "prova real", "ausente", [],
                                  "campo de coleta ausente")
        modulo, _, presente = ciclo.carregar_decisao()
        self.assertTrue(presente, "controle de paridade exige CIC-2 real")
        assert modulo is not None
        real = modulo.consolidar([criterio], ident)
        # Simula ausencia real de arquivo sem tocar no decisao.py compartilhado.
        with patch.object(ciclo, "AQUI", self.base):
            mod, erro, presente = ciclo.carregar_decisao()
            self.assertFalse(presente)
            self.assertIsNone(mod)
            fallback, aviso = ciclo.consolidar_decisao([criterio], ident, [], mod, erro, presente)
        self.assertIsNone(aviso)
        self.assertFalse(fallback["pronto_para_decisao"])
        self.assertEqual(fallback["pendencias_humanas"], [])
        self.assertEqual({f["id"] for f in fallback["falhas_automaticas"]},
                         {f["id"] for f in real["falhas_automaticas"]})
        self.assertEqual(fallback["pronto_para_decisao"], real["pronto_para_decisao"])
        fila = ciclo.fila_da_decisao(fallback, [], ident)
        self.assertEqual([f["criterio"] for f in fila], ["runtime_ausente"])
        self.assertTrue(fila[0]["requer_nova_rodada"])
        # Controle positivo: sem lacunas e identidade suficiente nao bloqueia.
        limpo = ciclo.decisao_minima([], ident, [])
        self.assertTrue(limpo["pronto_para_decisao"])

    def test_fallback_fila_existente_impede_pronto(self):
        ident = ciclo.identidade(self.repo)
        d = ciclo.decisao_minima([], ident, [{"id": "lacuna", "motivo": "coleta ausente"}])
        self.assertFalse(d["pronto_para_decisao"])

    def test_consolidar_usa_modulo_quando_existe(self):
        ident = {"fonte_sha": "a" * 64, "dll_sha": "b" * 64}

        class Fake:
            @staticmethod
            def consolidar(criterios, identidade, aceite_humano=None):
                return {"por_mod": {"transversal": []}, "pronto_para_decisao": True}

        d, aviso = ciclo.consolidar_decisao([], ident, [], Fake, None, presente=True)
        self.assertEqual(d["origem_decisao"], "decisao.py")
        self.assertTrue(d["pronto_para_decisao"])
        self.assertIsNone(aviso)

    def test_decisao_quebrada_nao_esconde_erro(self):
        class Ruim:
            @staticmethod
            def consolidar(criterios, identidade, aceite_humano=None):
                raise ValueError("boom")

        d, aviso = ciclo.consolidar_decisao([], {"fonte_sha": "a" * 64, "dll_sha": "b" * 64},
                                            [], Ruim, None, presente=True)
        self.assertEqual(d["origem_decisao"], "minima_no_ciclo")
        self.assertTrue(aviso, "decisao.py presente e quebrada NAO pode cair calado no fallback")
        self.assertIn("boom", aviso)

    def test_decisao_ausente_pode_usar_minima(self):
        d, aviso = ciclo.consolidar_decisao([], {"fonte_sha": "a" * 64, "dll_sha": None},
                                            [], None, "decisao.py ausente", presente=False)
        self.assertEqual(d["origem_decisao"], "minima_no_ciclo")
        self.assertIsNone(aviso, "ausencia do modulo (pre-integracao) nao e falha tecnica")


class TestCLI(BaseCiclo):
    def test_cli_reprovado_gera_fila_e_exit1(self):
        aut3 = self._aut3_no_repo(_com_snapshot(_aut3_reprovado(), self.repo))
        saida = os.path.join(self.base, "r1.json")
        code, out, err = self._cli("--repo", self.repo, "--resultado", saida,
                                   "--aut3-resultado", aut3)
        self.assertEqual(code, 1, "esperava REPROVADO (1); stdout=%s stderr=%s" % (out, err))
        r = ciclo.carregar_json(saida)
        self.assertEqual(r["estado"], "REPROVADO")
        self.assertEqual(len(r["fila_correcao"]), 1)
        self.assertEqual(r["tentativas"]["numero"], 1)
        self.assertNotEqual(r["identidade"]["fonte_sha"], None)
        self.assertTrue(r["reuso"]["snapshot_ok"])

    def test_cli_tudo_ok_aprova_e_exit0(self):
        aut3 = self._aut3_no_repo(_com_snapshot(_aut3_ok(), self.repo))
        saida = os.path.join(self.base, "ok.json")
        code, out, err = self._cli("--repo", self.repo, "--resultado", saida,
                                   "--aut3-resultado", aut3)
        self.assertEqual(code, 0, "esperava APROVADO (0); stdout=%s stderr=%s" % (out, err))
        r = ciclo.carregar_json(saida)
        self.assertEqual(r["estado"], "APROVADO_OFFLINE")
        self.assertEqual(r["fila_correcao"], [])
        self.assertTrue(r["decisao"]["pronto_para_decisao"])

    def test_cli_reuso_snapshot_divergente_nao_aprova(self):
        aut3 = self._aut3_no_repo(_com_snapshot(_aut3_ok(), self.repo))
        saida = os.path.join(self.base, "r-snap.json")
        code, out, err = self._cli("--repo", self.repo, "--resultado", saida,
                                   "--aut3-resultado", aut3)
        self.assertEqual(code, 0, "rodada 1 devia aprovar; %s%s" % (out, err))
        _escrever(self.repo, "a.py", "VALOR = 999\n")
        code, out, err = self._cli("--repo", self.repo, "--resultado", saida,
                                   "--aut3-resultado", aut3)
        self.assertEqual(code, 2, "reuso de snapshot divergente = INCOMPLETO/nova rodada, nao %s; %s%s"
                         % (code, out, err))
        r = ciclo.carregar_json(saida)
        self.assertEqual(r["estado"], "INCOMPLETO")
        self.assertFalse(r["reuso"]["snapshot_ok"])
        self.assertIn("diverg", r["reuso"]["snapshot_motivo"])
        ok = [c for c in r["criterios"] if c["estado"] == "OK"]
        self.assertEqual(ok, [], "criterios de um snapshot divergente nao podem ficar OK")

    def test_cli_reuso_snapshot_ausente_nao_aprova(self):
        aut3 = self._aut3_no_repo(_com_snapshot_vazio(_aut3_ok()))
        saida = os.path.join(self.base, "r-vazio.json")
        code, out, err = self._cli("--repo", self.repo, "--resultado", saida,
                                   "--aut3-resultado", aut3)
        self.assertEqual(code, 2, "sem snapshot => INCOMPLETO; %s%s" % (out, err))
        r = ciclo.carregar_json(saida)
        self.assertEqual(r["estado"], "INCOMPLETO")
        self.assertFalse(r["reuso"]["snapshot_ok"])

    def test_cli_sem_dll_nao_aprova_e_mostra_falhas(self):
        repo = _mini_repo(self.base, nome="sem-dll", com_dll=False)
        aut3 = _escrever(repo, "docs/automacao/AUT-3-resultado.json",
                         json.dumps(_com_snapshot(_aut3_ok(), repo), ensure_ascii=False))
        saida = os.path.join(self.base, "sem-dll.json")
        code, out, err = self._cli("--repo", repo, "--resultado", saida,
                                   "--aut3-resultado", aut3)
        self.assertNotEqual(code, 0, "sem dll_sha a identidade e insuficiente: nunca APROVADO")
        r = ciclo.carregar_json(saida)
        self.assertNotEqual(r["estado"], "APROVADO_OFFLINE")
        self.assertFalse(r["decisao"]["pronto_para_decisao"])
        resumo = json.loads(out)
        self.assertGreaterEqual(resumo["falhas_automaticas"], 1,
                                "o resumo curto NAO pode esconder as falhas tecnicas")
        self.assertIn("pronto", resumo)

    def test_cli_decisao_discorda_do_ciclo_e_rebaixa_aprovado(self):
        repo = _mini_repo(self.base, nome="sem-checker", com_dll=True, com_checker=False)
        aut3 = _escrever(repo, "docs/automacao/AUT-3-resultado.json",
                         json.dumps(_com_snapshot(_aut3_ok(), repo), ensure_ascii=False))
        saida = os.path.join(self.base, "sem-checker.json")
        code, out, err = self._cli("--repo", repo, "--resultado", saida,
                                   "--aut3-resultado", aut3)
        r = ciclo.carregar_json(saida)
        self.assertNotEqual(r["estado"], "APROVADO_OFFLINE",
                            "decisao com falha automatica NAO pode conviver com APROVADO")
        self.assertNotEqual(code, 0)
        ids = [f["criterio"] for f in r["fila_correcao"]]
        self.assertIn("check_x", ids, "a falha da decisao tem de entrar na fila do ciclo")

    def test_cli_escalona_por_sem_progresso(self):
        aut3 = self._aut3_no_repo(_com_snapshot(_aut3_reprovado(), self.repo))
        saida = os.path.join(self.base, "r-lim.json")
        for _ in range(4):
            code, out, err = self._cli("--repo", self.repo, "--resultado", saida,
                                       "--aut3-resultado", aut3, "--limite", "3")
        r = ciclo.carregar_json(saida)
        self.assertTrue(r["escala"], "sem progresso no limite tem de escalar")
        self.assertEqual(r["estado"], "ESCALADO")
        self.assertEqual(code, 1)
        self.assertIn("supervisor", r["motivo_escalacao"].lower())

    def test_cli_mudanca_de_fonte_invalida_aprovacao(self):
        aut3 = self._aut3_no_repo(_com_snapshot(_aut3_ok(), self.repo))
        saida = os.path.join(self.base, "ok2.json")
        code, out, err = self._cli("--repo", self.repo, "--resultado", saida,
                                   "--aut3-resultado", aut3)
        self.assertEqual(code, 0, err)
        code, out, err = self._cli("--repo", self.repo, "--verificar", saida)
        self.assertEqual(code, 0, "esperava VALIDO; %s%s" % (out, err))
        _escrever(self.repo, "a.py", "VALOR = 99\n")
        code, out, err = self._cli("--repo", self.repo, "--verificar", saida)
        self.assertEqual(code, 3, "esperava INVALIDADO (3); %s%s" % (out, err))
        v = json.loads(out)
        self.assertFalse(v["valido"])
        self.assertIn("mudou", v["motivo"])

    def test_cli_segunda_rodada_detecta_invalidacao_da_anterior(self):
        aut3 = self._aut3_no_repo(_com_snapshot(_aut3_reprovado(), self.repo))
        saida = os.path.join(self.base, "r2.json")
        self._cli("--repo", self.repo, "--resultado", saida, "--aut3-resultado", aut3)
        _escrever(self.repo, "a.py", "VALOR = 3\n")
        aut3b = self._aut3_no_repo(_com_snapshot(_aut3_ok(), self.repo))
        self._cli("--repo", self.repo, "--resultado", saida, "--aut3-resultado", aut3b)
        r = ciclo.carregar_json(saida)
        self.assertEqual(r["tentativas"]["numero"], 2)
        self.assertTrue(r["tentativas"]["invalidou_anterior"])

class TestRegressaoReal(BaseCiclo):
    def preparar_motor(self):
        raiz = os.environ.get("CICLO_REPO_TESTE", ciclo.RAIZ_PADRAO)
        offline = os.path.join(self.repo, "tools", "automacao", "offline")
        shutil.copytree(os.path.join(raiz, "tools", "automacao", "offline"), offline,
                        ignore=shutil.ignore_patterns("__pycache__"))
        for nome in ("check_dupes.py", "check_chave_compartilhada.py", "tabelas.py"):
            shutil.copy2(os.path.join(raiz, "tools", nome), os.path.join(self.repo, "tools", nome))
        return "BetterTooltips/Patches/LocalizePatch.cs"

    def test_falha_correcao_revalidacao_motor_real(self):
        rel = self.preparar_motor()
        limpo = ('TextFixes = new Dictionary<string, string> { { "alvo", "valor" } };\n'
                 'TextAppends = new Dictionary<string, string> { { "outro", "nota" } };\n')
        defeito = limpo.replace('{ "alvo", "valor" }', '{ "alvo", "valor" }, { "alvo", "duplicata" }')
        _escrever(self.repo, rel, defeito)
        saida = os.path.join(self.base, "ciclo.json")
        argv = ("--repo", self.repo, "--trabalho", os.path.join(self.base, "rodadas"),
                "--resultado", saida, "--checagem", "check_dupes")
        code, out, err = self._cli(*argv)
        self.assertEqual(code, 1, out + err)
        r1 = ciclo.carregar_json(saida)
        self.assertEqual(r1["fila_correcao"][0]["criterio"], "check_dupes")
        _escrever(self.repo, rel, limpo)
        code, out, err = self._cli(*argv)
        self.assertEqual(code, 0, out + err)
        r2 = ciclo.carregar_json(saida)
        self.assertEqual(r2["estado"], "APROVADO_REGRESSAO")
        self.assertFalse(r2["escopo"]["full"])
        self.assertEqual(r2["fila_correcao"], [])
        self.assertEqual(r2["falhas_automaticas"], [])
        self.assertTrue(r2["tentativas"]["invalidou_anterior"])
        self.assertTrue(r2["reuso"]["snapshot_ok"])

    def test_reuso_cli_motor_real_rejeita_dll_trocada_e_ausente(self):
        rel = self.preparar_motor()
        _escrever(self.repo, ".gitignore", "bin/\n")
        _git(self.repo, "rm", "--cached", MOD_DLL)
        _escrever(self.repo, rel, 'TextFixes = new Dictionary<string, string> { { "alvo", "valor" } };\n'
                  'TextAppends = new Dictionary<string, string> { { "outro", "nota" } };\n')
        saida = os.path.join(self.base, "original.json")
        argv = ("--repo", self.repo, "--trabalho", os.path.join(self.base, "rodadas"),
                "--resultado", saida, "--checagem", "check_dupes")
        code, out, err = self._cli(*argv)
        self.assertEqual(code, 0, out + err)
        original = ciclo.carregar_json(saida)
        prova = original["aut3_meta"]["resultado_aut3"]
        bytes_prova = Path(prova).read_bytes()
        ident = ciclo.identidade(self.repo)
        reuso = os.path.join(self.base, "reuso.json")
        code, out, err = self._cli("--repo", self.repo, "--resultado", reuso, "--aut3-resultado", prova)
        self.assertEqual(code, 0, out + err)
        for novo in (b"DLL-TROCADA", None):
            with self.subTest(dll=novo):
                if novo is None:
                    os.remove(os.path.join(self.repo, MOD_DLL))
                else:
                    _escrever(self.repo, MOD_DLL, novo, binario=True)
                atual = ciclo.identidade(self.repo)
                self.assertEqual(ident["fonte_sha"], atual["fonte_sha"])
                code, out, err = self._cli("--repo", self.repo, "--verificar", saida)
                self.assertEqual(code, 3, out + err)
                code, out, err = self._cli("--repo", self.repo, "--resultado", reuso, "--aut3-resultado", prova)
                self.assertEqual(code, 2, out + err)
                r = ciclo.carregar_json(reuso)
                self.assertFalse(r["reuso"]["snapshot_ok"])
                self.assertIn("DLL", r["reuso"]["snapshot_motivo"])
                self.assertFalse(r["decisao"]["pronto_para_decisao"])
                self.assertTrue(r["fila_correcao"])
                self.assertFalse(any(c["estado"] == "OK" for c in r["criterios"]))
                self.assertEqual(Path(prova).read_bytes(), bytes_prova, "reuso nao reassina a prova")
        _escrever(self.repo, MOD_DLL, b"DLL-FALSA-CIC1", binario=True)
        code, out, err = self._cli("--repo", self.repo, "--resultado", reuso, "--aut3-resultado", prova)
        self.assertEqual(code, 0, out + err)
        # Prova legada sem vinculo DLL tambem precisa de nova rodada.
        legado = ciclo.carregar_json(prova)
        legado.pop("ciclo_identidade", None)
        caminho_legado = os.path.join(self.base, "legado.json")
        with open(caminho_legado, "w", encoding="utf-8") as fh:
            json.dump(legado, fh)
        code, out, err = self._cli("--repo", self.repo, "--resultado", reuso, "--aut3-resultado", caminho_legado)
        self.assertEqual(code, 2, out + err)
        self.assertFalse(ciclo.carregar_json(reuso)["decisao"]["pronto_para_decisao"])

    def test_checagem_desconhecida_nao_aprova(self):
        self.preparar_motor()
        code, out, err = self._cli("--repo", self.repo, "--trabalho", os.path.join(self.base, "rodadas"),
                                   "--resultado", os.path.join(self.base, "invalido.json"),
                                   "--checagem", "check_inventado")
        self.assertEqual(code, 2, out + err)

    def test_dll_ignorada_pelo_git_invalida(self):
        _escrever(self.repo, ".gitignore", "bin/\n")
        _git(self.repo, "rm", "--cached", MOD_DLL)
        ident = ciclo.identidade(self.repo)
        _escrever(self.repo, MOD_DLL, b"OUTRA-DLL", binario=True)
        atual = ciclo.identidade(self.repo)
        self.assertEqual(ident["fonte_sha"], atual["fonte_sha"])
        self.assertFalse(ciclo.verificar_resultado({"identidade": ident}, atual)[0])

    def test_copia_preserva_dist_e_rejeita_destino_interno(self):
        _escrever(self.repo, "dist/prova.zip", b"ARTEFATO", binario=True)
        destino = os.path.join(self.base, "copia")
        ciclo.copiar_repo(self.repo, destino)
        self.assertTrue(os.path.isfile(os.path.join(destino, "dist/prova.zip")))
        with self.assertRaises(OSError):
            ciclo.copiar_repo(self.repo, os.path.join(self.repo, "copia"))
        self.assertTrue(os.path.isfile(os.path.join(self.repo, "a.py")))


class TestLockDaArea(BaseCiclo):
    def test_lock_vivo_bloqueia_e_liberado_libera(self):
        area = os.path.join(self.base, "area")
        caminho, erro = ciclo.tomar_lock(area)
        self.assertIsNone(erro, erro)
        self.assertTrue(os.path.isfile(caminho))
        caminho2, erro2 = ciclo.tomar_lock(area)
        self.assertIsNone(caminho2)
        self.assertIn("outra rodada", erro2)
        ciclo.liberar_lock(caminho)
        caminho3, erro3 = ciclo.tomar_lock(area)
        self.assertIsNone(erro3, erro3)
        ciclo.liberar_lock(caminho3)

    def test_lock_obsoleto_de_pid_morto_e_retomado(self):
        area = os.path.join(self.base, "area2")
        os.makedirs(area, exist_ok=True)
        _escrever(area, "ciclo.lock", "999999")
        caminho, erro = ciclo.tomar_lock(area)
        self.assertIsNone(erro, erro)
        self.assertTrue(caminho)
        ciclo.liberar_lock(caminho)

    def test_rodada_com_area_ocupada_nao_aprova_nem_escreve_copia(self):
        area = os.path.join(self.base, "area3")
        lock, _ = ciclo.tomar_lock(area)
        saida = os.path.join(self.base, "bloqueado.json")
        code, out, err = self._cli("--repo", self.repo, "--trabalho", area,
                                   "--resultado", saida, "--checagem", "check_x")
        self.assertEqual(code, 2, out + err)
        r = ciclo.carregar_json(saida)
        self.assertEqual(r["estado"], "INCOMPLETO")
        self.assertEqual(r["aut3_meta"]["modo"], "bloqueado")
        self.assertFalse(os.path.isdir(os.path.join(area, "ciclo-copia")),
                         "rodada bloqueada nao pode comecar a copia")
        ciclo.liberar_lock(lock)


if __name__ == "__main__":
    unittest.main(verbosity=2)
