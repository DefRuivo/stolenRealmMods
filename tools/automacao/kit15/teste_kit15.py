#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teste_kit15.py - suite offline do pacote instalavel KIT-15.

Roda com: python tools/automacao/kit15/teste_kit15.py
Exit: 0 = tudo verde; 1 = falha; 2 = erro de infraestrutura (sem interpretador/layout).
Nada aqui abre o jogo, instala no perfil do dono, publica ou usa rede.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
import unittest
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

try:
    import contra_prova_kit15  # noqa: E402
    import descoberta  # noqa: E402
    import instalador  # noqa: E402
    import pacote  # noqa: E402
    import scan  # noqa: E402
except Exception as _exc:  # pragma: no cover - infra
    print("ERRO-INFRA KIT-15 suite: import falhou: %s" % _exc, file=sys.stderr)
    sys.exit(2)

try:
    RAIZ = pacote._raiz_repo()
except Exception as _exc:  # pragma: no cover - infra
    print("ERRO-INFRA KIT-15 suite: raiz do repo indisponivel: %s" % _exc, file=sys.stderr)
    sys.exit(2)
_TMP = None
_PACOTE_BASE = None


def setUpModule():
    global _TMP, _PACOTE_BASE
    _TMP = tempfile.mkdtemp(prefix="kit15-suite-")
    _PACOTE_BASE = os.path.join(_TMP, "pacote-base")
    os.makedirs(_PACOTE_BASE)
    rc, rel = pacote.montar(_PACOTE_BASE)
    if rc != 0:
        raise RuntimeError("pre-condicao do teste falhou: pacote base nao ficou limpo: %s" % rel["veredito"])


def tearDownModule():
    if _TMP and os.path.isdir(_TMP):
        shutil.rmtree(_TMP, ignore_errors=True)


def novo_destino(nome):
    caminho = os.path.join(_TMP, "destinos", nome)
    os.makedirs(caminho, exist_ok=True)
    return caminho


def copia_pacote(nome):
    """Copia o pacote base para um diretorio novo (para mutar sem afetar os outros testes)."""
    destino = os.path.join(_TMP, "pacotes", nome)
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    shutil.copytree(os.path.join(_PACOTE_BASE, "staging"), destino)
    return destino


def arquivos_instalados(destino):
    recibo = instalador.ler_recibo(destino)
    return recibo["arquivos"] if recibo else []


def atualizar_manifesto(pacote, rel):
    """KIT-15F/F2: o manifesto do pacote e AUTORITATIVO. Quando um teste altera de proposito
    uma fonte do pacote, ele TEM de refazer o hash declarado -- senao a alteracao e
    (corretamente) recusada como adulteracao."""
    caminho = os.path.join(pacote, instalador.ARQ_MANIFESTO)
    with open(caminho, "r", encoding="utf-8") as fh:
        man = json.load(fh)
    cid = rel.split("/")[1]
    alvo_rel = "/".join(rel.split("/")[2:])
    comp = next(c for c in man["componentes"] if c["id"] == cid)
    arq = next(a for a in comp["arquivos"] if a["rel"] == alvo_rel)
    arq["sha256"] = instalador.sha256_arquivo(os.path.join(pacote, rel))
    arq["bytes"] = os.path.getsize(os.path.join(pacote, rel))
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2, ensure_ascii=False)


class TesteManifesto(unittest.TestCase):
    def test_01_recipe_e_manifesto_do_pacote(self):
        recipe = instalador.carregar_json(os.path.join(AQUI, "manifesto.json"))
        self.assertEqual(recipe["schema"], "kit-rstv/manifesto/1")
        ids = {c["id"]: c for c in recipe["componentes"]}
        self.assertTrue(ids["core"]["obrigatorio"])
        self.assertTrue(ids["adapter"]["obrigatorio"])
        self.assertTrue(ids["recorder"]["obrigatorio"])
        self.assertFalse(ids["runner"]["obrigatorio"])
        self.assertFalse(ids["viewer"]["obrigatorio"])
        man = instalador.carregar_json(os.path.join(_PACOTE_BASE, "staging", instalador.ARQ_MANIFESTO))
        self.assertEqual(man["schema"], "kit-rstv/manifesto/1")
        self.assertEqual(man["pacote"], "kit-rstv")
        self.assertTrue(man["total_arquivos"] > 20)


class TestePacote(unittest.TestCase):
    def test_02_zip_candidato_limpo(self):
        rel = instalador.carregar_json(os.path.join(_PACOTE_BASE, "pacote-relatorio.json"))
        self.assertEqual(rel["veredito"], "PACOTE_LIMPO")
        self.assertIsNone(rel["zip_testzip"])
        self.assertEqual(rel["scan_total"], 0)
        self.assertTrue(os.path.isfile(rel["zip"]))
        self.assertIn("NAO_EXECUTADA", rel["publicacao"])
        # hashes do relatorio conferem com o zip em disco
        self.assertEqual(instalador.sha256_arquivo(rel["zip"]), rel["zip_sha256"])

    def test_03_zip_sem_dll_proprietaria_nem_perfil(self):
        rel = instalador.carregar_json(os.path.join(_PACOTE_BASE, "pacote-relatorio.json"))
        with zipfile.ZipFile(rel["zip"]) as zf:
            nomes = zf.namelist()
        proibidos = [n for n in nomes if n.lower().endswith((".dll", ".pdb", ".exe", ".so", ".dylib"))]
        self.assertEqual(proibidos, [], "pacote nao pode conter binario: %s" % proibidos)
        for n in nomes:
            self.assertNotIn(".git/", n)
            self.assertNotIn("__pycache__", n)
            self.assertNotIn("/bin/", "/" + n)
        self.assertIn("kit-rstv.manifest.json", nomes)
        self.assertIn("tools/instalador.py", nomes)
        self.assertIn("docs/README.md", nomes)

    def test_04_verificar_zip_real(self):
        rel = instalador.carregar_json(os.path.join(_PACOTE_BASE, "pacote-relatorio.json"))
        rc, ver = pacote.verificar(rel["zip"])
        self.assertEqual(rc, 0)
        self.assertEqual(ver["veredito"], "OK")
        self.assertTrue(ver["tem_manifesto"])
        self.assertEqual(ver["scan_total"], 0)


class TesteInstalacao(unittest.TestCase):
    def test_05_instalar_confere_todos_os_hashes(self):
        pac = copia_pacote("instalar")
        destino = novo_destino("t05")
        rc, dados = instalador.instalar(pac, destino)
        self.assertEqual(rc, 0, dados)
        recibo = instalador.ler_recibo(destino)
        self.assertEqual(recibo["schema"], "kit-rstv/instalado/1")
        self.assertTrue(len(recibo["arquivos"]) == dados["arquivos_total"])
        for arq in recibo["arquivos"]:
            alvo = os.path.join(destino, arq["rel"])
            self.assertTrue(os.path.isfile(alvo), arq["rel"])
            self.assertEqual(instalador.sha256_arquivo(alvo), arq["sha256"], arq["rel"])
        rc, st = instalador.status(destino)
        self.assertEqual(rc, 0)
        self.assertEqual(st["estado"], "INSTALADO")

    def test_06_manifesto_do_pacote_bate_com_o_instalado(self):
        pac = copia_pacote("instalar-manifesto")
        destino = novo_destino("t06")
        instalador.instalar(pac, destino)
        man = instalador.carregar_json(os.path.join(pac, instalador.ARQ_MANIFESTO))
        esperado = {}
        for comp in man["componentes"]:
            for a in comp["arquivos"]:
                esperado["components/%s/%s" % (comp["id"], a["rel"])] = a["sha256"]
        for arq in arquivos_instalados(destino):
            if arq["rel"].startswith("components/"):
                self.assertEqual(arq["sha256"], esperado[arq["rel"]], arq["rel"])

    def test_07_instalar_preserva_arquivo_local_alheio(self):
        pac = copia_pacote("preserva")
        destino = novo_destino("t07")
        extra = os.path.join(destino, "meu-arquivo-local.txt")
        with open(extra, "w", encoding="utf-8") as fh:
            fh.write("anotacao do modder que NAO pertence ao pacote\n")
        instalador.instalar(pac, destino)
        self.assertTrue(os.path.isfile(extra))
        instalador.remover(destino)
        self.assertTrue(os.path.isfile(extra), "arquivo alheio nao pode ser removido")
        with open(extra, "r", encoding="utf-8") as fh:
            self.assertIn("anotacao do modder", fh.read())

    def test_08_atualizar_muda_so_o_arquivo_divergente(self):
        pac = copia_pacote("atualiza")
        destino = novo_destino("t08")
        instalador.instalar(pac, destino)
        antes = {a["rel"]: os.path.getmtime(os.path.join(destino, a["rel"])) for a in arquivos_instalados(destino)}
        time.sleep(1.1)  # mtime tem resolucao de 1s em alguns FS
        alvo_rel = "components/core/Json.cs"
        alvo_src = os.path.join(pac, alvo_rel)
        dados = open(alvo_src, "rb").read()
        with open(alvo_src, "wb") as fh:
            fh.write(dados + b"\n// marcador de atualizacao do teste\n")
        atualizar_manifesto(pac, alvo_rel)

        rc, info = instalador.instalar(pac, destino)
        self.assertEqual(rc, 0, info)
        self.assertEqual(info["arquivos_escritos"], 1, "somente o arquivo alterado deve ser reescrito")
        depois = {a["rel"]: os.path.getmtime(os.path.join(destino, a["rel"])) for a in arquivos_instalados(destino)}
        for rel, mt in antes.items():
            if rel == alvo_rel:
                self.assertNotEqual(mt, depois[rel], "o arquivo alterado deveria mudar")
            else:
                self.assertEqual(mt, depois[rel], "arquivo identico nao pode ser reescrito: %s" % rel)
        with open(os.path.join(destino, alvo_rel), "rb") as fh:
            self.assertIn(b"marcador de atualizacao do teste", fh.read())

    def test_09_rollback_devolve_bytes_originais(self):
        pac = copia_pacote("rollback")
        destino = novo_destino("t09")
        instalador.instalar(pac, destino)
        original = os.path.join(destino, "components/core/Json.cs")
        sha_original = instalador.sha256_arquivo(original)
        alvo_src = os.path.join(pac, "components/core/Json.cs")
        with open(alvo_src, "wb") as fh:
            fh.write(b"// fonte sensivelmente diferente\n")
        atualizar_manifesto(pac, "components/core/Json.cs")
        instalador.instalar(pac, destino)
        self.assertNotEqual(instalador.sha256_arquivo(original), sha_original)
        rc, dados = instalador.rollback(destino)
        self.assertEqual(rc, 0, dados)
        self.assertEqual(instalador.sha256_arquivo(original), sha_original)
        self.assertEqual(dados["operacao_revertida"], "instalar")

    def test_10_remover_restaura_estado_anterior(self):
        pac = copia_pacote("remover")
        destino = novo_destino("t10")
        # arquivo que JA existia antes do kit e sera sobrescrito
        pre_rel = "components/core/Json.cs"
        pre_existente = os.path.join(destino, pre_rel)
        os.makedirs(os.path.dirname(pre_existente), exist_ok=True)
        conteudo_antes = b"// versao do usuario que estava aqui ANTES do kit\n"
        with open(pre_existente, "wb") as fh:
            fh.write(conteudo_antes)
        sha_antes = instalador.sha256_arquivo(pre_existente)

        rc, _ = instalador.instalar(pac, destino)
        self.assertEqual(rc, 0)
        self.assertNotEqual(instalador.sha256_arquivo(pre_existente), sha_antes)
        criados = [a["rel"] for a in arquivos_instalados(destino) if a["rel"] != pre_rel]

        rc, dados = instalador.remover(destino)
        self.assertEqual(rc, 0, dados)
        self.assertEqual(dados["problemas"], [])
        self.assertEqual(instalador.sha256_arquivo(pre_existente), sha_antes,
                         "o arquivo pre-existente deve voltar byte a byte")
        self.assertFalse(os.path.isfile(os.path.join(destino, instalador.ARQ_RECIBO)))
        for rel in criados:
            self.assertFalse(os.path.isfile(os.path.join(destino, rel)), "criado pelo kit deveria sair: %s" % rel)

    def test_11_remover_sem_recibo_e_rollback_sem_transacao_falham(self):
        destino = novo_destino("t11")
        rc, dados = instalador.remover(destino)
        self.assertEqual(rc, 1)
        self.assertIn("recibo", dados["erro"])
        rc, dados = instalador.rollback(destino)
        self.assertEqual(rc, 1)
        self.assertIn("transacao", dados["erro"])

    def test_12_hash_divergente_apos_escrita_dispara_rollback(self):
        pac = copia_pacote("hash-ruim")
        destino = novo_destino("t12")
        original_copy2 = shutil.copy2

        def copy_corrompido(src, dst, *a, **kw):
            resultado = original_copy2(src, dst, *a, **kw)
            if "components" in dst.replace("\\", "/") and dst.endswith(".cs"):
                with open(dst, "ab") as fh:
                    fh.write(b"// corrupcao injetada pelo teste\n")
            return resultado

        import unittest.mock as mock
        with mock.patch.object(instalador.shutil, "copy2", side_effect=copy_corrompido):
            rc, dados = instalador.instalar(pac, destino)
        self.assertEqual(rc, 1, dados)
        self.assertEqual(dados["erro"], "hash divergente apos escrita")
        self.assertEqual(dados["rollback"], "ok")
        # o rollback automatico nao pode deixar arquivo parcial para tras
        leftover = []
        for atual, _, arquivos in os.walk(destino):
            for a in arquivos:
                rel = os.path.relpath(os.path.join(atual, a), destino).replace("\\", "/")
                if rel.startswith("components/"):
                    leftover.append(rel)
        self.assertEqual(leftover, [], "rollback deve remover o que a transacao criou")

    def test_13_selecao_de_componentes_e_sem_opcionais(self):
        pac = copia_pacote("selecao")
        destino = novo_destino("t13")
        rc, dados = instalador.instalar(pac, destino, componentes=["core"], com_opcionais=False)
        self.assertEqual(rc, 0, dados)
        rels = {a["rel"] for a in arquivos_instalados(destino)}
        self.assertTrue(any(r.startswith("components/core/") for r in rels))
        self.assertFalse(any(r.startswith("components/adapter/") for r in rels))
        self.assertFalse(any(r.startswith("components/viewer/") for r in rels))
        rc, dados = instalador.instalar(pac, novo_destino("t13b"), componentes=["inexistente"])
        self.assertEqual(rc, 1)
        self.assertIn("desconhecido", dados["erro"])

    def test_14_modo_manual_sem_python_equivale_ao_instalador(self):
        """Uso basico SEM a ferramenta: copiar a arvore do pacote a mao e conferir hashes
        contra o manifesto embutido. Prova que o payload e autossuficiente."""
        pac = copia_pacote("manual")
        destino = novo_destino("t14")
        man = instalador.carregar_json(os.path.join(pac, instalador.ARQ_MANIFESTO))
        for comp in man["componentes"]:
            shutil.copytree(os.path.join(pac, comp["origem_dir"]),
                            os.path.join(destino, "components", comp["id"]), dirs_exist_ok=True)
            for a in comp["arquivos"]:
                alvo = os.path.join(destino, "components", comp["id"], a["rel"])
                self.assertEqual(instalador.sha256_arquivo(alvo), a["sha256"], a["rel"])
        shutil.copytree(os.path.join(pac, "tools"), os.path.join(destino, "tools"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(pac, "docs"), os.path.join(destino, "docs"), dirs_exist_ok=True)
        self.assertTrue(os.path.isfile(os.path.join(destino, "docs", "primeiro-uso.md")))
        # remocao manual: tirar a pasta do kit nao deixa rastro do kit
        shutil.rmtree(os.path.join(destino, "components"))
        self.assertFalse(os.path.isdir(os.path.join(destino, "components")))


class TesteDescoberta(unittest.TestCase):
    def test_15_descoberta_sem_usuario_fixo(self):
        ambiente = {"HOME": os.path.join(_TMP, "home-fake"), "USERPROFILE": os.path.join(_TMP, "home-fake")}

        def _norm(p):
            return (p or "").replace("\\", "/")
        # KIT-15F/F8: o padrao depende do LAYOUT. A expectativa tem de ser calculada das MESMAS
        # DUAS entradas que a implementacao usa -- env do processo (KIT15_RAIZ/KIT_RSTV_RAIZ) e a
        # raiz de repositorio acima DESTA copia -- e nao de uma fonte diferente.
        # KIT-15F/run688 (achado F11): antes o teste perguntava a layout a
        # raiz_do_repositorio(descoberta.AQUI) (o local da copia) enquanto destino_do_kit usava
        # raiz_efetiva (que honra KIT15_RAIZ). Com o sandbox da contra-prova fora da arvore o
        # baseline verde virava vermelho: o veredito dependia de ONDE fica a copia. Agora a
        # expectativa vem das duas fontes do contrato, entao vale em qualquer localizacao e ainda
        # pega uma raiz_efetiva que deixe de honrar a env.
        raiz_declarada = None
        for chave in ("KIT15_RAIZ", descoberta.ENV_RAIZ):
            valor = os.environ.get(chave)
            if valor and os.path.isdir(os.path.join(valor, "tools", "automacao")):
                raiz_declarada = os.path.abspath(valor)
                break
        raiz_acima_da_copia = descoberta.raiz_do_repositorio(descoberta.AQUI)
        raiz_esperada = raiz_declarada or raiz_acima_da_copia
        destino, origem = descoberta.destino_do_kit(ambiente=ambiente, usar_repo=False)
        self.assertEqual(origem, "padrao-home")
        self.assertTrue(destino.startswith(os.path.join(_TMP, "home-fake")))
        destino, origem = descoberta.destino_do_kit(ambiente=ambiente)
        if raiz_esperada:
            self.assertEqual(origem, "padrao-repo")
            esperado = _norm(os.path.join(raiz_esperada, "dist", "kit-rstv"))
            self.assertEqual(_norm(destino), esperado)
        else:
            self.assertEqual(origem, "padrao-home")
            self.assertTrue(destino.startswith(os.path.join(_TMP, "home-fake")))

        ambiente_env = dict(ambiente, KIT_RSTV_HOME=os.path.join(_TMP, "env-home"))
        destino, origem = descoberta.destino_do_kit(ambiente=ambiente_env)
        self.assertEqual(origem, "ambiente:KIT_RSTV_HOME")
        self.assertEqual(destino.replace("\\", "/"), os.path.join(_TMP, "env-home").replace("\\", "/"))

        explicito = os.path.join(_TMP, "explicito")
        destino, origem = descoberta.destino_do_kit(explicito=explicito, ambiente=ambiente_env)
        self.assertEqual(origem, "argumento")
        self.assertEqual(destino.replace("\\", "/"), explicito.replace("\\", "/"))

        # config do usuario tem prioridade sobre o padrao do repo
        conf_dir = os.path.join(_TMP, "conf")
        os.makedirs(conf_dir, exist_ok=True)
        with open(os.path.join(conf_dir, descoberta.NOME_ARQUIVO_CONFIG), "w", encoding="utf-8") as fh:
            json.dump({"destino": os.path.join(_TMP, "do-config")}, fh)
        destino, origem = descoberta.destino_do_kit(ambiente=ambiente, caminho_config=conf_dir)
        self.assertEqual(origem, "config")
        self.assertEqual(destino.replace("\\", "/"), os.path.join(_TMP, "do-config").replace("\\", "/"))

        # sem HOME/APPDATA o destino e INDETERMINADO, nao inventado
        destino, origem = descoberta.destino_do_kit(ambiente={}, usar_repo=False)
        self.assertEqual(origem, "indeterminado")
        self.assertIsNone(destino)

    def test_16_nenhum_nome_de_usuario_embutido_no_codigo(self):
        usuario = os.environ.get("USERNAME") or os.environ.get("USER") or "Pichau"
        for nome in ("descoberta.py", "instalador.py", "pacote.py", "scan.py"):
            with open(os.path.join(AQUI, nome), "r", encoding="utf-8") as fh:
                texto = fh.read()
            self.assertNotIn("C:\\Users", texto.replace("\\\\", "\\"))
            self.assertNotIn(usuario, texto, "%s nao pode conter nome de usuario fixo" % nome)


class TesteScan(unittest.TestCase):
    def test_17_scan_controle_negativo_e_limpo(self):
        base = os.path.join(_TMP, "scan")
        limpo = os.path.join(base, "limpo")
        os.makedirs(limpo, exist_ok=True)
        with open(os.path.join(limpo, "nota.md"), "w", encoding="utf-8") as fh:
            fh.write("# nota de bancada\nsem credencial aqui\n")
        self.assertEqual(scan.varrer(limpo), [])

        sujo = os.path.join(base, "sujo")
        os.makedirs(sujo, exist_ok=True)
        # segredo sintetico montado em runtime (nao existe literal no fonte)
        chave = "AKIA" + "ABCDEFGHIJKLMNOP"
        with open(os.path.join(sujo, "config.txt"), "w", encoding="utf-8") as fh:
            fh.write("aws_key=" + chave + "\n")
        achados = scan.varrer(sujo)
        self.assertTrue(achados, "planta de credencial tem de ser detectada")
        self.assertEqual(achados[0]["tipo"], "segredo")

        binario = os.path.join(base, "combinario")
        os.makedirs(binario, exist_ok=True)
        with open(os.path.join(binario, "Assembly-CSharp.dll"), "wb") as fh:
            fh.write(b"MZ\x00\x00binario de jogo que NAO pode ser distribuido")
        achados = scan.varrer(binario)
        self.assertTrue(any(a["tipo"] == "binario-proibido" for a in achados))

    def test_18_scan_pega_dll_dentro_do_zip(self):
        zpath = os.path.join(_TMP, "com-dll.zip")
        with zipfile.ZipFile(zpath, "w") as zf:
            zf.writestr("components/core/ok.cs", "// fonte\n")
            zf.writestr("components/core/Assembly-CSharp.dll", b"MZ binario proibido")
        achados = scan.varrer(zpath)
        self.assertTrue(any(a["tipo"] == "binario-proibido" for a in achados))
        rc, ver = pacote.verificar(zpath)
        self.assertEqual(rc, 1)
        self.assertEqual(ver["veredito"], "ACHADO")


class TesteContraProva(unittest.TestCase):
    """KIT15-D6-CRLF: a ancora da contra-prova tem de discriminar no checkout LF E no CRLF.

    Antes da correcao, aplicar_defeito ancorava so no estilo LF: num clone Windows com
    core.autocrlf=true (arquivos CRLF) a ancora MULTILINE do D6 nao casava, o defeito virava
    MUTACAO-INVALIDA e a contra-prova fechava "baseline verde, 6/7" -- falso verde de
    ferramenta. Estes testes usam arquivos SINTETICOS proprios, e nao o modulo vivo, para
    continuarem validos mesmo quando o defeito D6 esta aplicado na copia sandbox.
    """

    CONTEUDO = ("def alvo(explicito=None):\n"
                "    if explicito:\n"
                "        return explicito\n"
                "    return None\n")
    DEFEITO = {
        "id": "sintetico-ancora-multiline",
        "arquivo": "alvo.py",
        "patches": [("    if explicito:\n        return explicito",
                     "    if False:\n        return explicito")],
        "alvo": ["sintetico"],
    }

    def _sandbox(self, nome, dados):
        sb = os.path.join(_TMP, "contra-prova", nome)
        os.makedirs(sb, exist_ok=True)
        caminho = os.path.join(sb, self.DEFEITO["arquivo"])
        with open(caminho, "wb") as fh:
            fh.write(dados)
        return sb, caminho

    def test_19_ancora_multiline_casa_em_lf_e_em_crlf(self):
        for rotulo, quebra, crlf_esperado in (("lf", "\n", 0), ("crlf", "\r\n", 4)):
            sb, caminho = self._sandbox(rotulo, self.CONTEUDO.replace("\n", quebra).encode("utf-8"))
            ok, motivo = contra_prova_kit15.aplicar_defeito(sb, self.DEFEITO)
            self.assertTrue(ok, "%s: ancora multiline nao casou: %s" % (rotulo, motivo))
            dados = open(caminho, "rb").read()
            esperado = self.CONTEUDO.replace("    if explicito:", "    if False:") \
                                    .replace("\n", quebra).encode("utf-8")
            self.assertEqual(dados, esperado,
                             "%s: so o trecho ancorado pode mudar (estilo de quebra intacto)" % rotulo)
            self.assertEqual(dados.count(b"\r\n"), crlf_esperado)
        self.assertEqual(contra_prova_kit15.estilo_de_quebra(b"a\r\nb\r\n"), "\r\n")
        self.assertEqual(contra_prova_kit15.estilo_de_quebra(b"a\nb\n"), "\n")
        self.assertIsNone(contra_prova_kit15.estilo_de_quebra(b"a\r\nb\n"))

    def test_20_ancora_ausente_ou_ambigua_e_recusada_sem_tocar_bytes(self):
        original = self.CONTEUDO.encode("utf-8")
        # (a) ancora ausente: 0 ocorrencias
        sb, caminho = self._sandbox("ausente", original.replace(b"    if explicito:\n", b""))
        antes = open(caminho, "rb").read()
        ok, motivo = contra_prova_kit15.aplicar_defeito(sb, self.DEFEITO)
        self.assertFalse(ok, "ancora ausente NAO pode ser aceita como mutacao")
        self.assertIn("0 vezes", motivo)
        self.assertEqual(open(caminho, "rb").read(), antes, "recusa nao pode escrever no arquivo")

        # (b) ancora ambigua: 2 ocorrencias
        sb, caminho = self._sandbox("ambigua", original + original[original.index(b"    if explicito"):])
        antes = open(caminho, "rb").read()
        ok, motivo = contra_prova_kit15.aplicar_defeito(sb, self.DEFEITO)
        self.assertFalse(ok, "ancora ambigua NAO pode ser aceita como mutacao")
        self.assertIn("2 vezes", motivo)
        self.assertEqual(open(caminho, "rb").read(), antes)

    def test_21_quebras_mistas_nao_sao_adivinhadas(self):
        sb, caminho = self._sandbox("misto", b"# cabecalho\r\n"
                                             b"def alvo(explicito=None):\n"
                                             b"    if explicito:\n"
                                             b"        return explicito\n")
        antes = open(caminho, "rb").read()
        ok, motivo = contra_prova_kit15.aplicar_defeito(sb, self.DEFEITO)
        self.assertFalse(ok, "quebras mistas tem de virar recusa explicita, nunca adivinhacao")
        self.assertIn("mistas", motivo)
        self.assertEqual(open(caminho, "rb").read(), antes)


if __name__ == "__main__":
    try:
        _ucarregador = unittest.TestLoader()
        _usuite = _ucarregador.loadTestsFromModule(sys.modules[__name__])
        _resultado = unittest.TextTestRunner(verbosity=2).run(_usuite)
    except Exception as exc:  # pragma: no cover - infra
        print("ERRO-INFRA KIT-15 suite: %s" % exc, file=sys.stderr)
        sys.exit(2)
    # KIT-15F/F11: resultado ESTRUTURADO -- a contra-prova (e a revisao) nao podem depender
    # de expressao regular sobre a saida para saber se a suite realmente rodou.
    _resumo = {
        "suite": "kit15/teste_kit15",
        "tests": _resultado.testsRun,
        "failures": [t.id() for t, _ in _resultado.failures],
        "errors": [t.id() for t, _ in _resultado.errors],
        "skipped": len(_resultado.skipped),
        "ok": _resultado.wasSuccessful(),
    }
    _destino_resultado = os.environ.get("KIT15_RESULT")
    if _destino_resultado:
        with open(_destino_resultado, "w", encoding="utf-8") as _fh:
            json.dump(_resumo, _fh, indent=2, ensure_ascii=False)
    print("KIT15-SUITE|tests=%d|failures=%d|errors=%d|skipped=%d|ok=%s"
          % (_resumo["tests"], len(_resumo["failures"]), len(_resumo["errors"]),
             _resumo["skipped"], _resumo["ok"]))
    sys.exit(0 if _resultado.wasSuccessful() else 1)
