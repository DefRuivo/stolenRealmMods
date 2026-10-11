#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_kit12_integracao.py - testes OFFLINE da costura KIT-12 (positivos, controles negativos e isca).

O QUE ESTE ARQUIVO PROVA (e o que NAO prova)
--------------------------------------------
Exercita `integracao.cadeia()` contra um SANDBOX proprio (copia de `tools/`, um mod de
fixture com DLL de fixture, `git init`) e contra um mapa de pertinencia real:

  * POSITIVO: cadeia completa com identidade suficiente -> criterios com a cadeia anexada,
    estado INCOMPLETO quando o unico que falta e o residual de runtime (fixture MARCADA nunca
    aprova) e estado APROVADO_OFFLINE alcancavel quando TODOS os criterios sao OK offline com
    evidencia real;
  * CONTROLES NEGATIVOS: arquivo alterado sem mapa, observacao fora de pertinencia, coleta
    ausente/ilegivel, identidade insuficiente, campo executavel proposto (`comando`/`argv`),
    fixture que REPROVA, sem-progresso, limite de tentativas, mudanca de config/versao;
  * ISCA (`--isca`): mutacoes SELETIVAS no fonte do modulo (copia) - cada guard mutado faz o
    teste-regressao correspondente REPROVAR. Mutante que passa verde = a suite e um carimbo.

**Sandbox NAO e jogo: nada aqui prova runtime.** Fixture marcada continua fixture.
Convencao: unittest (`Ran N tests`), exit 0 = todos PASSOU, 1 = algum REPROVOU, 2 = nao rodou.

USO
---
    python tools/automacao/kit12/test_kit12_integracao.py
    python tools/automacao/kit12/test_kit12_integracao.py --isca
    KIT12_INTEGRACAO=<caminho> python tools/automacao/kit12/test_kit12_integracao.py   # alvo alternativo
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
AUTOMACAO = os.path.dirname(AQUI)
TOOLS = os.path.dirname(AUTOMACAO)
REPO_REAL = os.path.dirname(TOOLS)

CAMINHO_INTEGRACAO = os.environ.get("KIT12_INTEGRACAO") or os.path.join(AQUI, "integracao.py")

_SBX = {"caminho": None}
_INT = {"mod": None}


def scratch_base():
    """Area de trabalho EXTERNA ao repo: sandbox e provas nao podem cair dentro do repositorio."""
    for cand in (os.environ.get("BH_AGENT_WORKSPACE"),):
        if cand and os.path.isdir(cand):
            return cand
    local = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    cand = os.path.join(local, "hermes", "cache", "scratch")
    os.makedirs(cand, exist_ok=True)
    return cand


def integracao():
    """O modulo sob teste (o vivo ou o `KIT12_INTEGRACAO` da isca)."""
    if _INT["mod"] is None:
        spec = importlib.util.spec_from_file_location("kit12_int_teste", CAMINHO_INTEGRACAO)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _INT["mod"] = mod
    return _INT["mod"]


def sandbox():
    """Sandbox com `tools/` copiado, mod de fixture e git - construida UMA vez por processo."""
    if _SBX["caminho"]:
        return _SBX["caminho"]
    base = os.path.join(scratch_base(), "kit12-teste-sandbox")
    if os.path.isdir(base):
        shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    shutil.copytree(os.path.join(REPO_REAL, "tools"), os.path.join(base, "tools"),
                    ignore=shutil.ignore_patterns("__pycache__", "bin", "obj", ".git"))

    mod = os.path.join(base, "BetterStats")
    os.makedirs(mod)
    _escrever(os.path.join(mod, "Plugin.cs"),
              "// FIXTURE de sandbox: NAO e o Plugin.cs real do mod\npublic class Plugin { }\n")
    _escrever(os.path.join(mod, "BetterStats.csproj"),
              "<Project Sdk=\"Microsoft.NET.Sdk\">\n  <PropertyGroup>\n"
              "    <Version>1.0.2</Version>\n  </PropertyGroup>\n</Project>\n")
    dll = os.path.join(mod, "bin", "Release", "netstandard2.1", "BetterStats.dll")
    os.makedirs(os.path.dirname(dll))
    with open(dll, "wb") as fh:  # BYTES DE FIXTURE (nao e DLL compilada)
        fh.write(b"KIT12-FIXTURE-DLL-BYTES\n")
    _escrever(os.path.join(base, "BepInEx", "config", "com.gumatos.betterstats.cfg"),
              "[Geral]\nAtivo = true\n")
    r = subprocess.run(["git", "init", "-q", base], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise RuntimeError("git init falhou no sandbox: %s" % r.stderr.decode("utf-8", "replace"))
    _SBX["caminho"] = base
    return base


def _escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)


def _cfg(base):
    return os.path.join(base, "BepInEx", "config", "com.gumatos.betterstats.cfg")


def obs_fixture(caminho, texto="10 (15)", mod="BetterStats", saved=10, final=15, extras=None,
                doc_extras=None):
    """Coleta de FIXTURE marcada (procedencia fixture + rotulo_fixture + evidencia_runtime=False)."""
    item = {"tipo": "atributos_base_final", "mod": mod, "objeto": "Attributes_Text",
            "atributo": "Strength", "texto_renderizado": texto, "personagem": "Hero",
            "personagem_display": "Hero", "saved_map": {"Strength": saved},
            "atributos_finais": None, "atributos_final": {"Strength": final}}
    if extras:
        item.update(extras)
    doc = {"esquema": "KIT-12/teste-coleta/1", "procedencia": "fixture", "rotulo_fixture": True,
           "evidencia_runtime": False, "sessao": "fixture-kit12-teste", "observacoes": [item]}
    if doc_extras:
        doc.update(doc_extras)
    _escrever(caminho, json.dumps(doc, ensure_ascii=False, indent=2))
    return caminho


def _saida(nome):
    return os.path.join(scratch_base(), "kit12-teste-out", nome)


# ---------------------------------------------------------------- produtor vivo (rodada 3)

ENVELOPE_AUT4_REAL = os.path.join(REPO_REAL, "docs", "automacao", "AUT-4-evidencias",
                                  "r3-confirmada", "aut4probe.json")


def campos_do_envelope_real():
    """Campos DECLARADOS do envelope REAL do produtor vivo (AUT-4 r3-confirmada).

    Le o artefato vivo - nao uma copia inventada - e confere o invariante do produtor:
    `hash_fonte` == `identidade.hash_dll_do_probe` (o sha256 da DLL do probe, medido em disco).
    Se o artefato real sumir/mudar de forma, o teste FALHA em vez de herdar uma fixture
    auto-consistente com a implementacao (o defeito F5 da revisao run670).
    """
    with open(ENVELOPE_AUT4_REAL, encoding="utf-8") as fh:
        real = json.load(fh)
    ident = real.get("identidade") or {}
    assert real.get("hash_fonte"), "envelope real sem hash_fonte"
    assert ident.get("hash_dll_do_probe"), "envelope real sem identidade.hash_dll_do_probe"
    assert real["hash_fonte"] == ident["hash_dll_do_probe"], \
        "o produtor vivo declara hash_fonte == hash_dll_do_probe (procedencia da DLL do probe)"
    return {"sessao": real.get("sessao"), "hash_fonte": real["hash_fonte"],
            "hash_dll_do_probe": ident["hash_dll_do_probe"],
            "hash_fonte_declarado": ident.get("hash_fonte_declarado"),
            "arquivo_dll_do_probe": ident.get("arquivo_dll_do_probe")}


def escrever_probe(base, nome, conteudo=b"KIT12-PROBE-DLL-FIXTURE\n"):
    """(caminho, sha256) de uma DLL de INSTRUMENTO de fixture em disco (bytes, sem build)."""
    caminho = os.path.join(base, "probe", nome)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "wb") as fh:
        fh.write(conteudo)
    return caminho, hashlib.sha256(conteudo).hexdigest()


def envelope_do_produtor(caminho, *, hash_fonte, sessao, arquivo_dll_do_probe=None,
                         hash_dll_do_probe=None, mod="BetterStats", texto="10 (15)",
                         doc_extras=None, observacao_extras=None):
    """Envelope no FORMATO DO PRODUTOR VIVO: `hash_fonte` da DLL do instrumento + `identidade`.

    A observacao e de FIXTURE marcada: fixture testa o avaliador e nao comprova runtime.
    """
    item = {"tipo": "atributos_base_final", "mod": mod, "objeto": "Attributes_Text",
            "atributo": "Strength", "texto_renderizado": texto, "personagem": "Hero",
            "personagem_display": "Hero", "saved_map": {"Strength": 10},
            "atributos_finais": None, "atributos_final": {"Strength": 15}}
    if observacao_extras:
        item.update(observacao_extras)
    doc = {"esquema": "AUT-4/1", "rotulo_fixture": True, "sintetico": True,
           "evidencia_runtime": False, "sessao": sessao, "hash_fonte": hash_fonte,
           "identidade": {"hash_dll_do_probe": hash_dll_do_probe or hash_fonte,
                          "hash_fonte_declarado": hash_dll_do_probe or hash_fonte,
                          "arquivo_dll_do_probe": arquivo_dll_do_probe},
           "observacoes": [item]}
    if doc_extras:
        doc.update(doc_extras)
    _escrever(caminho, json.dumps(doc, ensure_ascii=False, indent=2))
    return caminho


# ==========================================================================


class IntegracaoKIT12(unittest.TestCase):
    """Costura KIT-12: pertinencia, cadeia, fila declarativa, invalidacao e honestidade."""

    @classmethod
    def setUpClass(cls):
        cls.int = integracao()
        cls.base = sandbox()
        # Saidas NOVAS por rodada: resultado guardado de execucao anterior invalidaria/somaria
        # historico e o teste mediria o resto da suite anterior, nao a costura.
        out = os.path.join(scratch_base(), "kit12-teste-out")
        shutil.rmtree(out, ignore_errors=True)
        os.makedirs(out, exist_ok=True)

    # ---------------------------------------------------------------- positivos

    def test_positivo_cadeia_completa_leva_identidade_aos_criterios(self):
        """Positivo: fixture marcada -> criterios com cadeia anexada, nenhum OK, exit 2 (residual)."""
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"],
                            observacoes_path=obs_fixture(_saida("o1.json")),
                            configs=[_cfg(self.base)], resultado_path=_saida("r1.json"))
        self.assertEqual(r["estado"], "INCOMPLETO")
        self.assertEqual(r["exit_code"], 2)
        self.assertEqual(r["criterios_resumo"]["OK"], 0)
        self.assertEqual(r["criterios_resumo"]["com_prova_runtime"], 0)
        self.assertTrue(r["criterios"], "a avaliacao produziu criterios")
        for c in r["criterios"]:
            self.assertEqual(c.get("cadeia_sha"), r["cadeia_sha"])
            self.assertEqual(c.get("fonte_sha"), r["identidade"]["fonte_sha"])
            self.assertEqual(c.get("dll_sha"), r["identidade"]["dll_sha"])
            self.assertEqual(c.get("config_sha"), r["identidade"]["config_sha"])
            self.assertEqual(c.get("versao"), "1.0.2")
            self.assertEqual(c.get("sessao"), "fixture-kit12-teste")
        self.assertEqual(sorted(r["pertinencia"]["mods"]), ["BetterStats"])
        self.assertEqual(r["pertinencia"]["mods"]["BetterStats"]["cenarios"],
                         ["KIT-10/atributos/base-vs-final", "AUT-7/atributos"])
        self.assertTrue(r["relatorio_texto"], "o relatorio humano curto foi montado")

    def test_positivo_aprovado_offline_com_criterio_ok_e_evidencia_real(self):
        """Positivo de estado: criterio OK offline com evidencia REAL -> APROVADO_OFFLINE/exit 0."""
        ev = os.path.join(self.base, "BetterStats", "Plugin.cs")
        criterios = [{"id": "offline/exemplo", "mod": "BetterStats", "estado": "OK",
                      "classe": "offline", "procedencia": "execucao", "esperado": "build limpo",
                      "observado": "build limpo", "motivo": "", "evidencia": [ev],
                      "tarefa_origem": "t_0a434c97"}]
        ident = {"fonte_sha": "a" * 64, "dll_sha": "b" * 64, "raiz": self.base}
        dec = self.int.decisao().consolidar(criterios, ident)
        self.assertEqual(dec["falhas_automaticas"], [])
        estado, codigo = self.int.classificar_estado(criterios, dec, False, False)
        self.assertEqual((estado, codigo), ("APROVADO_OFFLINE", 0))

    def test_determinismo_duas_rodadas_geram_o_mesmo_resultado(self):
        """Duas rodadas com a mesma entrada: JSON canonico identico (sem o campo de tempo)."""
        obs = obs_fixture(_saida("o-det.json"))
        a = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=obs,
                            configs=[_cfg(self.base)])
        b = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=obs,
                            configs=[_cfg(self.base)])
        a.pop("gerado_em"), b.pop("gerado_em")
        self.assertEqual(json.dumps(a, sort_keys=True, ensure_ascii=False),
                         json.dumps(b, sort_keys=True, ensure_ascii=False))

    # ------------------------------------------------- controles negativos

    def test_neg_arquivo_alterado_sem_mapa_e_declarado(self):
        """Arquivo alterado sem mapa NAO desaparece: vira lacuna declarada (nunca verde)."""
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs", "docs/qualquer.md"],
                            observacoes_path=obs_fixture(_saida("o2.json")))
        self.assertEqual(r["pertinencia"]["nao_mapeados"], ["docs/qualquer.md"])
        ids = [c["id"] for c in r["criterios"]]
        self.assertIn("pertinencia/arquivo-sem-mapa/docs/qualquer.md", ids)
        self.assertEqual(r["exit_code"], 2)

    def test_neg_observacao_fora_da_pertinencia_nao_e_avaliada_e_e_declarada(self):
        """Observacao de mod nao alterado nao entra na avaliacao e nao e silenciada."""
        obs = obs_fixture(_saida("o3.json"), mod="BetterTooltips")
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=obs)
        ids = [c["id"] for c in r["criterios"]]
        self.assertTrue(any(i.startswith("pertinencia/observacao-fora/") for i in ids), ids)
        self.assertIn("coleta/BetterStats", ids)
        self.assertNotIn("BetterTooltips", r["pertinencia"]["mods"])
        self.assertEqual(r["criterios_resumo"]["OK"], 0)

    def test_neg_coleta_ausente_declarada_e_nao_aprova(self):
        """Coleta ausente: erro declarado, nenhum criterio OK, exit 2."""
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"],
                            observacoes_path=_saida("inexistente.json"))
        self.assertTrue(r["coleta"]["erro"])
        self.assertEqual(r["criterios_resumo"]["OK"], 0)
        self.assertEqual(r["exit_code"], 2)

    def test_neg_fixture_reprovada_vira_reprovado_com_causa_na_fila(self):
        """Defeito plantado na fixture: REPROVADO/exit 1 e a fila aponta CAUSA e PROVA."""
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"],
                            observacoes_path=obs_fixture(_saida("o4.json"), texto="10 (99)"),
                            configs=[_cfg(self.base)])
        self.assertEqual(r["estado"], "REPROVADO")
        self.assertEqual(r["exit_code"], 1)
        alvo = [f for f in r["fila_correcao"]
                if f["criterio"] == "KIT-10/atributos/base-vs-final/Attributes_Text"]
        self.assertEqual(len(alvo), 1, r["fila_correcao"])
        self.assertEqual(alvo[0]["roteamento"], "causa")
        self.assertIn("BetterStats/Plugin.cs", alvo[0]["caminhos"])
        self.assertTrue(alvo[0]["prova"])
        self.assertFalse(alvo[0]["execucao_automatica"])

    def test_neg_correcao_controlada_revalida_e_nao_vira_ok(self):
        """Erro -> correcao controlada (sandbox) -> revalidacao: o defeito SOME e nao vira OK."""
        defeito = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"],
                                  observacoes_path=obs_fixture(_saida("o5a.json"), texto="10 (99)"))
        self.assertEqual(defeito["exit_code"], 1)
        corrigido = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"],
                                    observacoes_path=obs_fixture(_saida("o5b.json"), texto="10 (15)"))
        self.assertEqual(corrigido["exit_code"], 2)  # fixture nunca aprova: residual de runtime
        self.assertEqual(corrigido["criterios_resumo"]["REPROVADO"], 0)
        alvo = [c for c in corrigido["criterios"]
                if c["id"] == "KIT-10/atributos/base-vs-final/Attributes_Text"]
        self.assertEqual(len(alvo), 1)
        self.assertEqual(alvo[0]["estado"], "NAO_EXERCITADO")
        # nenhum item da fila daquele criterio pode carregar severidade REPROVADO
        for f in corrigido["fila_correcao"]:
            if f["criterio"] == "KIT-10/atributos/base-vs-final/Attributes_Text":
                self.assertNotEqual(str(f.get("severidade")), "REPROVADO")
        falhas = [f for f in corrigido["falhas_automaticas"]
                  if f.get("id") == "KIT-10/atributos/base-vs-final/Attributes_Text"]
        for f in falhas:
            self.assertNotEqual(str(f.get("severidade")), "REPROVADO")

    def test_neg_sem_progresso_e_detectado(self):
        """Mesma fonte + mesmas falhas em duas rodadas: sem_progresso=True (nao reescreve verde)."""
        saida = _saida("r-prog.json")
        obs = obs_fixture(_saida("o6.json"), texto="10 (99)")
        a = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=obs,
                            resultado_path=saida)
        self.assertFalse(a["tentativas"]["sem_progresso"])
        b = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=obs,
                            resultado_path=saida)
        self.assertTrue(b["tentativas"]["sem_progresso"])
        self.assertEqual(b["tentativas"]["numero"], 2)
        self.assertTrue(b["tentativas"]["sem_progresso_motivo"])

    def test_neg_limite_de_tentativas_escala_ao_supervisor(self):
        """Limite de tentativas estourado com falhas: ESCALADO/exit 1, destino supervisor (nao dono)."""
        saida = _saida("r-lim.json")
        obs = obs_fixture(_saida("o7.json"), texto="10 (99)")
        for _ in range(2):
            self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=obs,
                            resultado_path=saida, limite=1)
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=obs,
                            resultado_path=saida, limite=1)
        self.assertEqual(r["estado"], "ESCALADO")
        self.assertEqual(r["exit_code"], 1)
        self.assertEqual(r["destino_escalonamento"], "supervisor")
        self.assertIn("supervisor", r["motivo_escalacao"])

    def test_neg_campo_executavel_proposto_nao_e_executado(self):
        """Fila DECLARATIVA: `comando`/`argv` propostos sao movidos, e NADA e executado."""
        criterios = [{"id": "x/reprovado", "mod": "BetterStats", "estado": "REPROVADO",
                      "classe": "offline", "procedencia": "execucao", "esperado": "ok",
                      "observado": "ruim", "motivo": "defeito", "evidencia": ["BetterStats/Plugin.cs"],
                      "tarefa_origem": "t", "comando": "rm -rf /", "argv": ["cmd", "/c", "del"],
                      "comando_correcao": "echo pwned"}]
        from unittest import mock
        with mock.patch("subprocess.run", side_effect=AssertionError("EXECUTOU COMANDO DA FILA")):
            fila = self.int.montar_fila(criterios, {"falhas_automaticas": []},
                                        {"fonte_sha": "a" * 64, "dll_sha": "b" * 64,
                                         "cadeia_sha": "c" * 64})
        self.assertEqual(len(fila), 1)
        item = fila[0]
        for campo in ("comando", "argv", "comando_correcao"):
            self.assertNotIn(campo, item)
        campos = sorted(p["campo"] for p in item["propostas_nao_executadas"])
        self.assertEqual(campos, ["argv", "comando", "comando_correcao"])
        self.assertFalse(item["execucao_automatica"])
        self.assertEqual(item["cadeia_sha"], "c" * 64)

    def test_neg_config_mudou_invalida_aprovacao_anterior(self):
        """Mudanca de config (parte da cadeia) INVALIDA o resultado guardado -> exit 3."""
        # Config FORA do repo: uma config dentro do sandbox entraria tambem no `fonte_sha`
        # (untracked), e o teste mediria a fonte, nao o campo `config_sha` da cadeia.
        cfg = _saida("cfg-teste.cfg")
        _escrever(cfg, "[Geral]\nAtivo = true\n")
        saida = _saida("r-inv.json")
        self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"],
                        observacoes_path=obs_fixture(_saida("o8.json")), configs=[cfg],
                        resultado_path=saida)
        ok = self.int.verificar(self.base, saida, configs=[cfg])
        self.assertTrue(ok["valido"])
        self.assertEqual(ok["exit_code"], 0)
        _escrever(cfg, "[Geral]\nAtivo = false\n")  # mudanca de CONFIG
        try:
            ruim = self.int.verificar(self.base, saida, configs=[cfg])
            self.assertFalse(ruim["valido"])
            self.assertEqual(ruim["exit_code"], 3)
            self.assertIn("config", ruim["motivo"])
        finally:
            _escrever(cfg, "[Geral]\nAtivo = true\n")

    def test_neg_versao_diferente_invalida(self):
        """Versao faz parte da cadeia: versao diferente invalida o resultado guardado."""
        saida = _saida("r-ver.json")
        self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"],
                        observacoes_path=obs_fixture(_saida("o9.json")), resultado_path=saida)
        ruim = self.int.verificar(self.base, saida, versao="9.9.9")
        self.assertFalse(ruim["valido"])
        self.assertEqual(ruim["exit_code"], 3)
        self.assertIn("versao", ruim["motivo"])

    def test_neg_identidade_insuficiente_derruba_o_ok(self):
        """Identidade insuficiente (sem dll) NUNCA deixa OK sobreviver."""
        criterios = [{"id": "x", "mod": "BetterStats", "estado": "OK", "classe": "offline",
                      "procedencia": "execucao", "evidencia": ["BetterStats/Plugin.cs"]}]
        self.int.rebaixar_ok(criterios, "sem identidade")
        self.assertEqual(criterios[0]["estado"], "NAO_EXERCITADO")
        self.assertFalse(self.int.identidade_suficiente({"fonte_sha": "a" * 64}))
        self.assertFalse(self.int.identidade_suficiente({"dll_sha": "b" * 64}))
        self.assertTrue(self.int.identidade_suficiente({"fonte_sha": "a" * 64, "dll_sha": "b" * 64}))

    def test_neg_avaliacao_vazia_nunca_aprova(self):
        """Zero criterios NAO e aprovacao: avaliacao vazia sai INCOMPLETO/exit 2."""
        estado, codigo = self.int.classificar_estado([], {"falhas_automaticas": []}, False, False)
        self.assertEqual((estado, codigo), ("INCOMPLETO", 2))

    def test_neg_avaliador_que_levanta_vira_lacuna_transversal_preservada(self):
        """Avaliador que levanta EXCECAO nao some: vira lacuna `avaliador/erro` transversal."""
        class Quebrado(object):
            @staticmethod
            def avaliar(obs, ident):
                raise RuntimeError("avaliador quebrado de proposito")

        int_ = self.int
        salvo = int_.kit10
        int_.kit10 = lambda: Quebrado
        try:
            criterios, meta = int_.criterios_da_cadeia(
                self.base, {"mods": {"BetterStats": {"cenarios": [], "frentes": [], "fonte": []}},
                            "nao_mapeados": []},
                [{"tipo": "atributos_base_final", "mod": "BetterStats"}],
                {"fonte_sha": "a" * 64, "dll_sha": "b" * 64}, {"fixture": False}, {})
        finally:
            int_.kit10 = salvo
        ids = [c["id"] for c in criterios]
        self.assertIn("avaliador/erro", ids)
        self.assertEqual(meta["fora_da_pertinencia"], [])
        estado, codigo = int_.classificar_estado(criterios, {"falhas_automaticas": []}, False, False)
        self.assertEqual((estado, codigo), ("INCOMPLETO", 2))

    def test_neg_alteracao_mapeia_cenarios_pertinentes(self):
        """A pertinencia e DADO: mod alterado -> cenarios/frentes declarados no mapa."""
        pert = self.int.carregar_pertinencia()
        sel = self.int.mapear(["BetterTooltips/Plugin.cs", "RoguelikeDebugger/Plugin.cs"], pert)
        self.assertEqual(sorted(sel["mods"]), ["BetterTooltips", "RoguelikeDebugger"])
        self.assertIn("KIT-10/shrines/contexto-dano-fonte-receptor",
                      sel["mods"]["BetterTooltips"]["cenarios"])
        self.assertEqual(sel["nao_mapeados"], [])
        sem = self.int.mapear([], pert, mods_explicitos=["ModInexistente"])
        self.assertEqual(sem["nao_mapeados"], ["<mod-sem-mapa>:ModInexistente"])

    def test_neg_declaracao_incoerente_do_avaliador_vira_lacuna_nomeada(self):
        """classe runtime + procedencia execucao nao e defeito do produto: vira lacuna, original guardado."""
        incoerente = {"id": "AUT-7/BetterStats/runtime-x", "mod": "BetterStats",
                      "estado": "INDETERMINADO", "classe": "runtime", "procedencia": "execucao"}
        norm, originais = self.int.normalizar_declaracoes([dict(incoerente)])
        self.assertEqual(len(originais), 1)
        self.assertEqual(originais[0], incoerente)
        self.assertEqual(norm[0]["id"], "avaliador/declaracao-incoerente/AUT-7/BetterStats/runtime-x")
        self.assertEqual(norm[0]["estado"], "NAO_EXERCITADO")
        self.assertEqual(norm[0]["classe"], "offline")
        self.assertIn("INCOERENTE", norm[0]["motivo"])

    # ------------------------------------------- procedencia confrontada (F1) / fila (F2)

    def test_neg_coleta_hash_contraditorio_nao_aprova(self):
        """F1/S2: coleta com hash_fonte de OUTROS bytes -> lacuna declarada, nenhum OK, exit 2."""
        obs = obs_fixture(_saida("o-contra.json"), doc_extras={"hash_fonte": "0" * 64})
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=obs,
                            configs=[_cfg(self.base)])
        ids = [c["id"] for c in r["criterios"]]
        self.assertIn("cadeia/coleta-contraditoria/hash_fonte", ids)
        self.assertEqual(r["criterios_resumo"]["OK"], 0)
        self.assertEqual(r["exit_code"], 2)
        self.assertNotEqual(r["estado"], "APROVADO_OFFLINE")
        for c in r["criterios"]:
            self.assertEqual(c["coleta"]["hash_fonte_confronto"], "contraditoria")

    def test_neg_coleta_sem_hash_declarado_nao_aprova(self):
        """F1: coleta SEM `hash_fonte` e ausencia de procedencia -> lacuna, nenhum OK."""
        criterios = [{"id": "offline/exemplo", "mod": "BetterStats", "estado": "OK",
                      "classe": "offline", "procedencia": "execucao", "esperado": "bom",
                      "observado": "bom", "motivo": "", "evidencia": [], "tarefa_origem": "t"}]
        criterios, _ = self._com_avaliador(criterios, {"hash_fonte": None, "fixture": False})
        ids = [c["id"] for c in criterios]
        self.assertIn("cadeia/coleta-ausente/hash_fonte", ids)
        self.assertEqual([c["estado"] for c in criterios if c["id"] == "offline/exemplo"],
                         ["NAO_EXERCITADO"])
        self.assertNotIn("OK", [c["estado"] for c in criterios])

    def test_positivo_coleta_com_instrumento_da_rodada_mantem_o_ok(self):
        """Contra-prova de F1: coleta COERENTE com a rodada -> o OK offline sobrevive.

        Rodada 3: a procedencia da coleta e conferida contra a cadeia da DLL/INSTRUMENTO
        (`dll_probe_sha`) ou o alias documentado `hash_fonte == dll_sha` - nunca contra
        `fonte_sha`. Os dois caminhos de aceitacao sao exercitados aqui.
        """
        criterio = {"id": "offline/exemplo", "mod": "BetterStats", "estado": "OK",
                    "classe": "offline", "procedencia": "execucao", "esperado": "bom",
                    "observado": "bom", "motivo": "", "evidencia": [], "tarefa_origem": "t"}
        # (a) alias documentado: hash_fonte == ident["dll_sha"]
        criterios, _ = self._com_avaliador([criterio], {"hash_fonte": "b" * 64, "fixture": False})
        alvo = [c for c in criterios if c["id"] == "offline/exemplo"]
        self.assertEqual(len(alvo), 1)
        self.assertEqual(alvo[0]["estado"], "OK")
        self.assertEqual(alvo[0]["coleta"]["hash_fonte_confronto"], "confere")
        self.assertEqual(alvo[0]["coleta"]["hash_fonte_campo_identidade"], "dll_sha")
        estado, codigo = self.int.classificar_estado(criterios, {"falhas_automaticas": []}, False, False)
        self.assertEqual((estado, codigo), ("APROVADO_OFFLINE", 0))
        # (b) instrumento declarado pela coleta (DLL do probe != DLL do mod): tambem confere
        criterios, _ = self._com_avaliador([dict(criterio)],
                                          {"hash_fonte": "d" * 64, "fixture": False,
                                           "instrumento_declarado": "d" * 64},
                                          ident_extra={"dll_probe_sha": "d" * 64,
                                                       "dll_probe_sha_origem": "declarado-coleta"})
        alvo = [c for c in criterios if c["id"] == "offline/exemplo"]
        self.assertEqual([c["estado"] for c in alvo], ["OK"])
        self.assertEqual(alvo[0]["coleta"]["hash_fonte_confronto"], "confere")
        self.assertTrue(str(alvo[0]["coleta"]["hash_fonte_campo_identidade"]).startswith("dll_probe_sha"))
        self.assertNotIn("cadeia/coleta-", " ".join(c["id"] for c in criterios))
        estado, codigo = self.int.classificar_estado(criterios, {"falhas_automaticas": []}, False, False)
        self.assertEqual((estado, codigo), ("APROVADO_OFFLINE", 0))

    def test_neg_coleta_com_hash_dos_arquivos_fonte_nao_e_procedencia(self):
        """F5 (rodada 3): `hash_fonte` = hash dos ARQUIVOS-FONTE do mod NAO e procedencia.

        Este e o teste-armadilha do defeito F5: se a confrontacao voltar a apontar para
        `ident["fonte_sha"]` (o erro corrigido), o valor abaixo (== fonte_sha da rodada)
        passaria como `confere` e o OK sobreviveria -> o teste FALHA.
        """
        criterio = {"id": "offline/exemplo", "mod": "BetterStats", "estado": "OK",
                    "classe": "offline", "procedencia": "execucao", "esperado": "bom",
                    "observado": "bom", "motivo": "", "evidencia": [], "tarefa_origem": "t"}
        criterios, _ = self._com_avaliador([criterio], {"hash_fonte": "a" * 64, "fixture": False})
        ids = [c["id"] for c in criterios]
        self.assertIn("cadeia/coleta-contraditoria/hash_fonte", ids)
        alvo = [c for c in criterios if c["id"] == "offline/exemplo"]
        self.assertEqual([c["estado"] for c in alvo], ["NAO_EXERCITADO"])
        self.assertFalse(alvo[0]["prova_runtime"])
        self.assertEqual(alvo[0]["coleta"]["hash_fonte_confronto"], "contraditoria")
        self.assertNotIn("OK", [c["estado"] for c in criterios])
        estado, codigo = self.int.classificar_estado(criterios, {"falhas_automaticas": []}, False, False)
        self.assertEqual((estado, codigo), ("INCOMPLETO", 2))

    def test_positivo_envelope_real_do_produtor_confere_sem_rebaixar(self):
        """F5 item 2: envelope nos MOLDES DO PRODUTOR VIVO (envelope real) -> confere.

        Campo canonico do instrumento: `identidade.hash_dll_do_probe` == `hash_fonte` (medido da
        DLL do probe). Sem bytes do probe em disco resta a DECLARACAO do proprio envelope, que e
        registrada como tal - e nenhuma lacuna de procedencia e criada. Se a confrontacao voltar
        para `fonte_sha`, o hash real do envelope nao confere e este teste FALHA.
        """
        real = campos_do_envelope_real()
        env = envelope_do_produtor(_saida("o-envelope-real.json"), hash_fonte=real["hash_fonte"],
                                   sessao="fixture-kit12-envelope-real",
                                   arquivo_dll_do_probe=real["arquivo_dll_do_probe"])
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=env,
                            configs=[_cfg(self.base)])
        ids = [c["id"] for c in r["criterios"]]
        self.assertNotIn("cadeia/coleta-contraditoria/hash_fonte", ids)
        self.assertNotIn("cadeia/coleta-incoerente/hash_fonte", ids)
        self.assertNotIn("cadeia/coleta-ausente/hash_fonte", ids)
        self.assertEqual(r["identidade"]["dll_probe_sha"], real["hash_dll_do_probe"])
        self.assertNotEqual(r["identidade"]["dll_probe_sha"], r["identidade"]["fonte_sha"])
        self.assertEqual(r["coleta"]["hash_fonte"], real["hash_fonte"])
        confrontos = {c["coleta"]["hash_fonte_confronto"] for c in r["criterios"] if c.get("coleta")}
        self.assertEqual(confrontos, {"confere"})
        # limite DECLARADO (nao medicao inventada): sem bytes do probe, a origem e a declaracao
        self.assertEqual(r["identidade"]["dll_probe_sha_origem"], "declarado-coleta")
        self.assertTrue(any("procedencia da coleta" in x for x in r["limites"]))
        # a fixture marcada continua fixture: nada vira OK/prova de runtime
        self.assertEqual(r["criterios_resumo"]["OK"], 0)
        self.assertEqual(r["criterios_resumo"]["com_prova_runtime"], 0)
        self.assertEqual(r["exit_code"], 2)

    def test_positivo_instrumento_medido_em_disco_confere_e_derruba_se_mudar(self):
        """F5 item 1/3: bytes do instrumento MEDIDOS em disco (`--probe-dll`) confirmam;
        bytes que nao casam com NENHUM campo da identidade continuam INCOMPLETO/exit 2."""
        probe, sha = escrever_probe(self.base, "AUT4Probe.dll", b"KIT12-PROBE-BYTES-A\n")
        env = envelope_do_produtor(_saida("o-probe-medido.json"), hash_fonte=sha,
                                   sessao="fixture-kit12-probe-medido", arquivo_dll_do_probe=None)
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=env,
                            configs=[_cfg(self.base)], probe_dll=probe)
        self.assertEqual(r["identidade"]["dll_probe_sha_origem"], "medido-cli")
        self.assertEqual(r["identidade"]["dll_probe_sha"], sha)
        for c in r["criterios"]:
            if c.get("coleta"):
                self.assertEqual(c["coleta"]["hash_fonte_confronto"], "confere")
                self.assertEqual(c["coleta"]["hash_fonte_campo_identidade"], "dll_probe_sha(medido)")
        # os MESMOS bytes do instrumento mudaram: a coleta passa a referir OUTROS bytes -> exit 2
        probe2, sha2 = escrever_probe(self.base, "AUT4Probe.dll", b"KIT12-PROBE-BYTES-B\n")
        self.assertNotEqual(sha, sha2)
        r2 = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=env,
                             configs=[_cfg(self.base)], probe_dll=probe2)
        ids = [c["id"] for c in r2["criterios"]]
        self.assertIn("cadeia/coleta-contraditoria/hash_fonte", ids)
        self.assertEqual(r2["criterios_resumo"]["OK"], 0)
        self.assertEqual(r2["exit_code"], 2)
        for c in r2["criterios"]:
            if c.get("coleta"):
                self.assertEqual(c["coleta"]["hash_fonte_confronto"], "contraditoria")

    def test_neg_coleta_incoerente_com_o_instrumento_que_ela_mesma_declara(self):
        """F5: `hash_fonte` != instrumento declarado pela PROPRIA coleta -> lacuna nomeada."""
        criterio = {"id": "offline/exemplo", "mod": "BetterStats", "estado": "OK",
                    "classe": "offline", "procedencia": "execucao", "esperado": "bom",
                    "observado": "bom", "motivo": "", "evidencia": [], "tarefa_origem": "t"}
        criterios, _ = self._com_avaliador([criterio], {"hash_fonte": "e" * 64, "fixture": False,
                                                       "instrumento_declarado": "f" * 64},
                                          ident_extra={"dll_probe_sha": "f" * 64,
                                                       "dll_probe_sha_origem": "declarado-coleta"})
        ids = [c["id"] for c in criterios]
        self.assertIn("cadeia/coleta-incoerente/hash_fonte", ids)
        alvo = [c for c in criterios if c["id"] == "offline/exemplo"]
        self.assertEqual([c["estado"] for c in alvo], ["NAO_EXERCITADO"])
        self.assertNotIn("OK", [c["estado"] for c in criterios])

    def test_neg_coleta_declara_cadeia_do_mod_de_outros_bytes(self):
        """S10 (revisao run670): campos de cadeia declarados pela COLETA sao CONFRONTADOS.

        Os 4 (+ sessao) nao podem divergir da identidade da rodada nem entre topo e `identidade`.
        """
        criterio = {"id": "offline/exemplo", "mod": "BetterStats", "estado": "OK",
                    "classe": "offline", "procedencia": "execucao", "esperado": "bom",
                    "observado": "bom", "motivo": "", "evidencia": [], "tarefa_origem": "t"}
        coleta = {"hash_fonte": "b" * 64, "fixture": False,
                  "declarados": {"fonte_sha": "9" * 64, "versao": "9.9.9"},
                  "incoerencias": []}
        criterios, _ = self._com_avaliador([dict(criterio)], coleta)
        ids = [c["id"] for c in criterios]
        self.assertIn("cadeia/coleta-contraditoria/fonte_sha", ids)
        self.assertIn("cadeia/coleta-contraditoria/versao", ids)
        alvo = [c for c in criterios if c["id"] == "offline/exemplo"]
        self.assertEqual([c["estado"] for c in alvo], ["NAO_EXERCITADO"])
        confrontos = {x["campo"]: x["resultado"] for x in alvo[0]["coleta"]["confrontos_declarados"]}
        self.assertEqual(confrontos.get("fonte_sha"), "contraditoria")
        self.assertEqual(confrontos.get("versao"), "contraditoria")
        self.assertEqual(alvo[0]["coleta"]["campos_declarados_pela_coleta"],
                         {"fonte_sha": "9" * 64, "versao": "9.9.9"})
        # contra-prova: os MESMOS campos com os valores da rodada nao criam lacuna
        coleta_ok = {"hash_fonte": "b" * 64, "fixture": False,
                     "declarados": {"fonte_sha": "a" * 64, "versao": "1.0.2"}, "incoerencias": []}
        criterios, _ = self._com_avaliador([dict(criterio)], coleta_ok)
        self.assertNotIn("cadeia/coleta-contraditoria/fonte_sha", [c["id"] for c in criterios])
        self.assertNotIn("cadeia/coleta-contraditoria/versao", [c["id"] for c in criterios])
        self.assertEqual([c["estado"] for c in criterios if c["id"] == "offline/exemplo"], ["OK"])

    def test_positivo_envelope_real_com_instrumento_medido_confere(self):
        """F5 item 1+2: envelope do produtor + bytes do instrumento medidos -> `confere` medido.

        Aqui o instrumento NAO e aceito por declaracao: o sha256 e medido dos bytes em disco e
        tem de casar exatamente com o `hash_fonte` do envelope.
        """
        real = campos_do_envelope_real()
        probe, sha = escrever_probe(self.base, "probe-real-equivalente.dll",
                                    b"KIT12-PROBE-EQUIVALENTE-AO-ENVELOPE-REAL\n")
        env = envelope_do_produtor(_saida("o-real-medido.json"), hash_fonte=sha,
                                   sessao="fixture-kit12-real-medido", arquivo_dll_do_probe=probe)
        r = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=env,
                            configs=[_cfg(self.base)], probe_dll=probe)
        self.assertEqual(r["identidade"]["dll_probe_sha_origem"], "medido-cli")
        self.assertEqual(r["identidade"]["dll_probe_sha"], sha)
        self.assertNotEqual(sha, real["hash_fonte"])  # bytes de fixture != DLL do probe do jogo
        for c in r["criterios"]:
            if c.get("coleta"):
                self.assertEqual(c["coleta"]["hash_fonte_confronto"], "confere")
        self.assertNotIn("cadeia/coleta-contraditoria/hash_fonte",
                         [c["id"] for c in r["criterios"]])
        # declaracao != medicao: o envelope declara outro instrumento -> INCOERENCIA medida
        env2 = envelope_do_produtor(_saida("o-real-medido-incoerente.json"), hash_fonte=sha,
                                    sessao="fixture-kit12-real-medido",
                                    arquivo_dll_do_probe=probe,
                                    hash_dll_do_probe="f" * 64,
                                    doc_extras={"hash_fonte": "f" * 64})
        r2 = self.int.cadeia(self.base, alterados=["BetterStats/Plugin.cs"], observacoes_path=env2,
                             configs=[_cfg(self.base)], probe_dll=probe)
        ids = [c["id"] for c in r2["criterios"]]
        self.assertIn("cadeia/coleta-incoerente/hash_dll_do_probe", ids)
        self.assertEqual(r2["criterios_resumo"]["OK"], 0)

    def test_neg_criterio_com_hash_de_bytes_antigos_e_rebaixado_e_preservado(self):
        """F1/S8: criterio OK declarando fonte_sha/dll_sha antigos -> rebaixado (nao sobrescrito mudo)."""
        antigo = {"id": "KIT-10/teste/base-vs-final/Attributes_Text", "mod": "BetterStats",
                  "estado": "OK", "classe": "offline", "procedencia": "execucao",
                  "esperado": "15", "observado": "15", "motivo": "", "evidencia": [],
                  "tarefa_origem": "t", "fonte_sha": "0" * 64, "dll_sha": "1" * 64}
        criterios, _ = self._com_avaliador([antigo], {"hash_fonte": "a" * 64, "fixture": False})
        ids = [c["id"] for c in criterios]
        for campo in ("fonte_sha", "dll_sha"):
            self.assertIn("cadeia/declaracao-contraditoria/%s/%s" % (antigo["id"], campo), ids)
        alvo = [c for c in criterios if c["id"] == antigo["id"]]
        self.assertEqual(len(alvo), 1)
        self.assertEqual(alvo[0]["estado"], "NAO_EXERCITADO")
        self.assertFalse(alvo[0]["prova_runtime"])
        self.assertTrue(alvo[0]["declaracao_sobrescrita"])
        declarados = {d["campo"]: d["declarado"] for d in alvo[0]["declaracoes_contraditorias"]}
        self.assertEqual(declarados, {"fonte_sha": "0" * 64, "dll_sha": "1" * 64})
        self.assertEqual(alvo[0]["fonte_sha"], "a" * 64)  # identidade da rodada, com a marca acima
        self.assertNotIn("OK", [c["estado"] for c in criterios])
        estado, codigo = self.int.classificar_estado(criterios, {"falhas_automaticas": []}, False, False)
        self.assertEqual((estado, codigo), ("INCOMPLETO", 2))

    def test_neg_campo_executavel_nao_sobrevive_no_criterio(self):
        """F2: o campo executavel sai do CRITERIO (e do item) e fica registrado como proposta."""
        criterio = {"id": "x/reprovado", "mod": "BetterStats", "estado": "REPROVADO",
                    "classe": "offline", "procedencia": "execucao", "esperado": "ok",
                    "observado": "ruim", "motivo": "defeito", "evidencia": [], "tarefa_origem": "t",
                    "comando": "rm -rf /", "argv": ["cmd", "/c", "del"],
                    "script_correcao": "corrige.sh"}
        from unittest import mock
        with mock.patch("subprocess.run", side_effect=AssertionError("EXECUTOU COMANDO DA FILA")):
            fila = self.int.montar_fila([criterio], {"falhas_automaticas": []},
                                        {"fonte_sha": "a" * 64, "dll_sha": "b" * 64,
                                         "cadeia_sha": "c" * 64})
        # o CRITERIO foi sanitizado: nenhum campo executavel viaja em `resultado["criterios"]`
        for campo in ("comando", "argv", "script_correcao"):
            self.assertNotIn(campo, criterio)
            self.assertNotIn(campo, fila[0])
        self.assertTrue(criterio["criterio_sanitizado"])
        propostas = fila[0]["propostas_nao_executadas"]
        self.assertEqual(sorted(p["campo"] for p in propostas),
                         ["argv", "comando", "script_correcao"])
        self.assertEqual({p["origem"] for p in propostas}, {"criterio"})
        self.assertFalse(fila[0]["execucao_automatica"])

    def test_neg_campo_executavel_do_avaliador_nao_vaza_no_resultado(self):
        """F2 ponta a ponta: criterio do avaliador com `comando` nao sai executavel no resultado."""
        criterio = {"id": "KIT-10/teste/base-vs-final/Attributes_Text", "mod": "BetterStats",
                    "estado": "REPROVADO", "classe": "offline", "procedencia": "execucao",
                    "esperado": "15", "observado": "99", "motivo": "defeito",
                    "evidencia": [], "tarefa_origem": "t", "comando": "rebuild && deploy"}
        r = self._cadeia_com_avaliador([criterio])
        for c in r["criterios"]:
            self.assertNotIn("comando", c)
        self.assertIn("comando", [p["campo"] for p in r["propostas_nao_executadas"]])
        self.assertTrue(any(p["origem"] == "criterio" for p in r["propostas_nao_executadas"]))

    # ---------------------------------------------------------------- auxiliares

    def _selecao(self):
        return {"mods": {"BetterStats": {"cenarios": ["KIT-10/atributos/base-vs-final"],
                                         "frentes": [], "fonte": ["BetterStats/Plugin.cs"]}},
                "nao_mapeados": []}

    def _com_avaliador(self, criterios, coleta_meta, ident_extra=None):
        """Roda `criterios_da_cadeia` com um avaliador DECLARADO pelo teste (sem jogo/IA)."""
        class Falso(object):
            @staticmethod
            def avaliar(obs, ident):
                return [dict(c) for c in criterios]

        int_ = self.int
        salvo = int_.kit10
        int_.kit10 = lambda: Falso
        ident = {"fonte_sha": "a" * 64, "dll_sha": "b" * 64, "cadeia_sha": "c" * 64,
                 "versao": "1.0.2", "sessao": coleta_meta.get("sessao")}
        ident.update(ident_extra or {})
        meta = dict(coleta_meta)
        meta.setdefault("caminho", _saida("coleta-inexistente.json"))
        try:
            return int_.criterios_da_cadeia(
                self.base, self._selecao(),
                [{"tipo": "atributos_base_final", "mod": "BetterStats", "objeto": "Attributes_Text"}],
                ident, meta, {})
        finally:
            int_.kit10 = salvo

    def _cadeia_com_avaliador(self, criterios):
        class Falso(object):
            @staticmethod
            def avaliar(obs, ident):
                return [dict(c) for c in criterios]

        int_ = self.int
        salvo = int_.kit10
        int_.kit10 = lambda: Falso
        try:
            return int_.cadeia(self.base, alterados=["BetterStats/Plugin.cs"],
                               observacoes_path=obs_fixture(_saida("o-aval.json")))
        finally:
            int_.kit10 = salvo


# ==========================================================================
# isca: mutacao SELETIVA no fonte do modulo (nunca AssertionError artificial)
# ==========================================================================

MUTACOES = [
    ("fixture_pode_aprovar", "def rebaixar_ok(criterios, motivo):",
     "def rebaixar_ok(criterios, motivo):\n    return criterios", "test_neg_identidade_insuficiente"),
    ("fila_executa_campo",
     "                if campo not in CAMPOS_EXECUTAVEIS:\n                    continue",
     "                if False:\n                    continue", "test_neg_campo_executavel"),
    ("invalidacao_desligada", "def invalidar_anterior(prev, ident):",
     "def invalidar_anterior(prev, ident):\n    return False, \"\"", "test_neg_config_mudou"),
    ("nunca_incompleto", "    if tem_lacuna or falhas:\n        return ESTADO_INCOMPLETO, EXIT_INCOMPLETO",
     "    if False:\n        return ESTADO_INCOMPLETO, EXIT_INCOMPLETO", "test_neg_correcao_controlada"),
    ("sem_progresso_desligado", "def classificar_estado(criterios, dec, escala, invalidado):",
     "def classificar_estado(criterios, dec, escala, invalidado):\n    escala = False", "test_neg_limite"),
    ("sem_anexar_cadeia", "    criterio[\"cadeia_sha\"] = ident.get(\"cadeia_sha\")",
     "    criterio[\"cadeia_sha\"] = None", "test_positivo_cadeia_completa"),
    # --- guardas da correcao F1/F2 (revisao run668)
    ("coleta_contraditoria_ignorada",
     "    hash_coleta = _texto(meta.get(\"hash_fonte\")) or None",
     "    hash_coleta = None", "test_neg_coleta_hash_contraditorio"),
    ("declaracao_do_criterio_sobrescrita",
     "            if str(declarado) != str(esperado):",
     "            if False:", "test_neg_criterio_com_hash_de_bytes_antigos"),
    ("criterio_nao_sanitizado",
     "                    valor = fonte.pop(campo)",
     "                    valor = fonte.get(campo)", "test_neg_campo_executavel_nao_sobrevive"),
    # --- guardas da correcao F5 (revisao run670): procedencia da coleta x cadeia da DLL
    ("confronto_volta_para_fonte_sha",
     "    ident_dll = _texto(ident.get(\"dll_sha\")) or None",
     "    ident_dll = _texto(ident.get(\"fonte_sha\")) or None",
     "test_neg_coleta_com_hash_dos_arquivos_fonte"),
    ("instrumento_medido_ignorado",
     "    elif medido and inst_sha and hash_coleta != inst_sha:",
     "    elif False:", "test_positivo_instrumento_medido_em_disco"),
    ("incoerencia_da_coleta_ignorada",
     "    elif decl_inst and hash_coleta != decl_inst:",
     "    elif False:", "test_neg_coleta_incoerente_com_o_instrumento"),
    ("instrumento_declarado_ignorado",
     "    decl = _texto(meta.get(\"instrumento_declarado\")) or None",
     "    decl = None", "test_positivo_envelope_real_do_produtor"),
    ("campo_declarado_pela_coleta_ignorado",
     "        elif declarado != esperado:",
     "        elif False:", "test_neg_coleta_declara_cadeia_do_mod_de_outros_bytes"),
]

_FONTE = {"texto": None}


def _fonte_original():
    if _FONTE["texto"] is None:
        with open(os.path.join(AQUI, "integracao.py"), encoding="utf-8") as fh:
            _FONTE["texto"] = fh.read()
    return _FONTE["texto"]


def rodar_isca():
    """Cada mutacao seletiva DEVE derrubar o teste-regressao correspondente (senao a suite e carimbo)."""
    original = _fonte_original()
    # Arvore de `tools/` ESPELHADA em area externa: o modulo resolve os irmaos por `__file__`
    # (ciclo.py, decisao.py, kit10, pertinencia.json). Mutar num diretorio solto quebraria por
    # ausencia de irmao, nao pela mutacao - a isca mediria o motivo errado.
    raiz_mut = os.path.join(scratch_base(), "kit12-teste-mut")
    shutil.rmtree(raiz_mut, ignore_errors=True)
    os.makedirs(raiz_mut)
    shutil.copytree(os.path.join(REPO_REAL, "tools"), os.path.join(raiz_mut, "tools"),
                    ignore=shutil.ignore_patterns("__pycache__", "bin", "obj", ".git"))
    mutante = os.path.join(raiz_mut, "tools", "automacao", "kit12", "integracao.py")
    problemas, ok = [], 0
    ambiente = dict(os.environ)
    ambiente["KIT12_INTEGRACAO"] = mutante
    for nome, alvo, troca, teste in MUTACOES:
        if alvo not in original:
            problemas.append("%s: alvo da mutacao nao encontrado no fonte" % nome)
            continue
        _escrever(mutante, original.replace(alvo, troca, 1))
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--so", teste],
                           env=ambiente, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if r.returncode == 0:
            problemas.append("%s: mutante PASSOU verde em %s (suite nao discrimina)" % (nome, teste))
        else:
            ok += 1
        print("ISCA|%s|%s|exit=%s" % (nome, teste, r.returncode))
    _escrever(mutante, original)
    r2 = subprocess.run([sys.executable, os.path.abspath(__file__), "--so", "test_positivo"],
                        env=ambiente, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if r2.returncode != 0:
        problemas.append("controle restaurado: suite voltou a reprovar no fonte original (exit %s)"
                         % r2.returncode)
        print("ISCA_SAIDA_CONTROLE|%s" % r2.stdout.decode("utf-8", "replace")[-2000:])
    print("ISCA|controle_restaurado|test_positivo|exit=%s" % r2.returncode)
    for p in problemas:
        print("ISCA_FALHA|%s" % p)
    print("ISCA|mutacoes_discriminadas=%d/%d|falhas=%d" % (ok, len(MUTACOES), len(problemas)))
    return 1 if problemas else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Testes offline da costura KIT-12.")
    ap.add_argument("--isca", action="store_true", help="mutacoes seletivas: cada guard deve derrubar seu teste")
    ap.add_argument("--so", default=None, help="roda so os testes cujo nome contem este texto")
    args = ap.parse_args(argv)
    if args.isca:
        return rodar_isca()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(IntegracaoKIT12)
    if args.so:
        suite = unittest.TestSuite(t for t in suite if args.so in t.id())
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
